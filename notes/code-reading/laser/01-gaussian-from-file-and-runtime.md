# `Gaussian` / `from_file` profile 与 `LaserParticleContainer` 运行链

绑定源码：

- `../warpx/Source/Laser/LaserProfilesImpl/LaserProfileGaussian.cpp`
- `../warpx/Source/Laser/LaserProfilesImpl/LaserProfileFromFile.cpp`
- `../warpx/Source/Particles/LaserParticleContainer.cpp`
- `../warpx/Docs/source/usage/parameters.rst`
- `../warpx/Examples/Tests/laser_injection/`
- `../warpx/Examples/Tests/laser_injection_from_file/`

## 1. 这篇笔记回答什么

上一篇 `00-laser-profile-dispatch.md` 只把 laser 的入口和 profile 工厂字典搭起来了，但真正的工作还没讲清：

1. `GaussianLaserProfile` 到底只是一层包络，还是已经内含聚焦、chirp、STC。
2. `FromFileLaserProfile` 是一次性把整份文件读进来，还是按时间块流式读取。
3. `LaserParticleContainer` 怎样把 profile 振幅变成真实的人工天线粒子，再通过 `J/rho` 沉积把激光写入 Maxwell 求解器。

这一篇把这三层接起来。

## 2. `GaussianLaserProfile` 不是简单高斯包络

### 2.1 构造期参数

`GaussianLaserProfile::init()` 在公共参数之外，继续读取：

```cpp
utils::parser::getWithParser(ppl, "profile_waist", m_params.waist);
utils::parser::getWithParser(ppl, "profile_duration", m_params.duration);
utils::parser::getWithParser(ppl, "profile_t_peak", m_params.t_peak);
utils::parser::getWithParser(ppl, "profile_focal_distance", m_params.focal_distance);
utils::parser::queryWithParser(ppl, "zeta", m_params.zeta);
utils::parser::queryWithParser(ppl, "beta", m_params.beta);
utils::parser::queryWithParser(ppl, "phi2", m_params.phi2);
utils::parser::queryWithParser(ppl, "phi0", m_params.phi0);
```

源码位置：`LaserProfileGaussian.cpp:40-48`。

这说明 Gaussian profile 的最小合同并不是“只给个 waist 和 duration”。当前实现已经直接支持：

- 聚焦距离 `profile_focal_distance`
- carrier-envelope phase `phi0`
- spatial chirp `zeta`
- angular dispersion `beta`
- temporal chirp `phi2`

### 2.2 `stc_direction` 是强约束，不是装饰参数

源码先把 `stc_direction` 归一化，再要求它与激光平面法向 `nvec` 正交：

```cpp
WARPX_ALWAYS_ASSERT_WITH_MESSAGE(std::abs(dp2) < 1.0e-14,
    "stc_direction is not perpendicular to the laser plane vector");
```

源码位置：`LaserProfileGaussian.cpp:50-67`。

因此 `stc_direction` 的真实语义不是“偏振的另一个别名”，而是定义 STC 在天线平面内的作用方向。WarpX 随后再计算它与 `p_X` 的夹角 `theta_stc`，后面真正进入时空耦合公式的是这个角度，而不是原始向量本身。源码位置：`LaserProfileGaussian.cpp:69-83`。

### 2.3 振幅公式已经同时包含 diffraction、Gouy、chirp、STC

`fill_amplitude()` 先构造几个与单个粒子无关的复系数：

```cpp
const Real k0 = 2._rt*MathConst::pi/m_common_params.wavelength;
const Complex diffract_factor =
    1._rt + I * m_params.focal_distance * 2._rt/
    ( k0 * m_params.waist * m_params.waist );
const Complex inv_complex_waist_2 =
    1._rt /(m_params.waist*m_params.waist * diffract_factor );
const Complex stretch_factor = 1._rt + 4._rt *
    ((m_params.zeta+m_params.beta*m_params.focal_distance)*inv_tau2)
    * ((m_params.zeta+m_params.beta*m_params.focal_distance)*inv_complex_waist_2)
    + 2._rt*I*(m_params.phi2-m_params.beta*m_params.beta*k0*m_params.focal_distance)*inv_tau2;
```

源码位置：`LaserProfileGaussian.cpp:104-123`。

这些对象的分工很明确：

- `diffract_factor` 负责聚焦距离引起的复 waist 修正，因此同时编码 diffraction、wavefront curvature、Gouy 相位。
- `inv_complex_waist_2` 把 transverse Gaussian 包络变成复 envelope。
- `stretch_factor` 把 spatial chirp、angular dispersion 和 temporal chirp 一起折叠进时域展宽。

随后 WarpX 再按维度给不同 prefactor：

```cpp
#if (defined(WARPX_DIM_3D) || (defined WARPX_DIM_RZ))
const Complex prefactor = t_prefactor / diffract_factor;
#elif defined(WARPX_DIM_XZ)
const Complex prefactor = t_prefactor / amrex::sqrt(diffract_factor);
#else
const Complex prefactor = t_prefactor;
#endif
```

源码位置：`LaserProfileGaussian.cpp:131-137`。

所以 3D / RZ 与 XZ 的 Gaussian 振幅并不是同一条公式简单降维，而是显式走不同的 diffraction scaling。

### 2.4 每个天线粒子看到的振幅是什么

单粒子层面，WarpX 对每个天线粒子构造：

```cpp
const Complex stc_exponent = 1._rt / stretch_factor * inv_tau2 *
    amrex::pow((t - tmp_profile_t_peak -
        tmp_beta*k0*(Xp[i]*std::cos(tmp_theta_stc) + Yp[i]*std::sin(tmp_theta_stc)) -
        2._rt *I*(Xp[i]*std::cos(tmp_theta_stc) + Yp[i]*std::sin(tmp_theta_stc))
        *( tmp_zeta - tmp_beta*tmp_profile_focal_distance ) * inv_complex_waist_2),2);
...
const Complex exp_argument = - ( Xp[i]*Xp[i] + Yp[i]*Yp[i] ) * inv_complex_waist_2;
amplitude[i] = ( stcfactor * amrex::exp( exp_argument ) ).real();
```

源码位置：`LaserProfileGaussian.cpp:149-159`。

这里 `Xp/Yp` 已经是激光平面坐标。也就是说，Gaussian profile 输出的不是“网格场值”，而是人工天线粒子在其自身发射平面上的目标 `E` 振幅。

## 3. `from_file` profile 是按时间块流式消费文件

### 3.1 输入合同

`FromFileLaserProfile::init()` 强制要求二选一：

```cpp
WARPX_ALWAYS_ASSERT_WITH_MESSAGE (
    lasy_file_name.empty() != binary_file_name.empty(),
    "Exactly one of 'binary_file_name' and 'lasy_file_name' has to be specified");
```

源码位置：`LaserProfileFromFile.cpp:64-72`。

因此 `from_file` 不是“同时支持两个源并自动合并”的接口，而是同一个 profile 类型下的两种独占后端：

- `lasy_file_name`：需要 `openPMD=ON`
- `binary_file_name`：保留的 legacy 二进制路径

### 3.2 `time_chunk_size` 和 `delay`

初始化时，WarpX 并不会一次性把全部时间切片读进来。默认 chunk 大小就是全时域 `nt`，但允许用户改小：

```cpp
m_params.time_chunk_size = m_params.nt;
...
if(utils::parser::queryWithParser(ppl ,"time_chunk_size", temp)){
    m_params.time_chunk_size = min(temp, m_params.time_chunk_size);
}
...
utils::parser::queryWithParser(ppl, "delay", m_params.t_delay);
```

源码位置：`LaserProfileFromFile.cpp:89-101`。

随后只预读第一块：

```cpp
if (m_params.file_in_lasy_format){
    read_data_t_chunk(0, m_params.time_chunk_size);
} else{
    read_binary_data_t_chunk(0, m_params.time_chunk_size);
}
```

源码位置：`LaserProfileFromFile.cpp:103-108`。

因此：

- `time_chunk_size` 控制的是 profile 数据的缓存窗口，而不是物理 pulse 宽度。
- `delay` 是读取后再施加到 profile 时间轴上的统一位移。

### 3.3 运行时只在需要时换块

`update(t)` 的职责不是重算 envelope，而是判断是否需要加载新的时间块：

```cpp
t += m_params.t_min - m_params.t_delay;
...
if(idx_t_right >  m_params.last_time_index){
    if (m_params.file_in_lasy_format){
        read_data_t_chunk(idx_t_left, idx_t_left+m_params.time_chunk_size);
    } else{
        read_binary_data_t_chunk(idx_t_left, idx_t_left+m_params.time_chunk_size);
    }
}
```

源码位置：`LaserProfileFromFile.cpp:113-130`。

所以 `ILaserProfile::update()` 在 `from_file` 路径里承担的是缓存推进器，而不是物理振幅更新器。

### 3.4 `fill_amplitude()` 只负责插值，不再读文件

真正求每个天线粒子的振幅时，WarpX 先做同样的时间平移，如果超出数据范围则直接返回零：

```cpp
t += m_params.t_min - m_params.t_delay;
if(t < m_params.t_min ||  t > m_params.t_max){
    ...
    amplitude[i] = 0.0_rt;
    return;
}
```

源码位置：`LaserProfileFromFile.cpp:133-146`。

在有效时间区间内，再分派到三种内部插值器：

```cpp
if (m_params.file_in_lasy_format){
    if (m_params.file_in_cartesian_geom==1){
        internal_fill_amplitude_uniform_cartesian(...);
    } else {
        internal_fill_amplitude_uniform_cylindrical(...);
    }
} else{
    internal_fill_amplitude_uniform_binary(...);
}
```

源码位置：`LaserProfileFromFile.cpp:153-160`。

这说明 `from_file` 的运行时结构是：

1. `update(t)` 负责确认缓存覆盖当前时间。
2. `fill_amplitude()` 负责在当前缓存上对 `(X,Y,t)` 做插值。

### 3.5 `lasy` 的几何约定

`parse_lasy_file()` 显式区分两种 geometry：

- `thetaMode`：数据维度 `{m,t,r}`，视为 RZ 文件。源码位置：`LaserProfileFromFile.cpp:183-196`
- `cartesian`：数据维度 `{t,y,x}`，视为 Cartesian 文件。源码位置：`LaserProfileFromFile.cpp:197-213`

读取完之后，几何尺寸和边界会广播到所有 rank。源码位置：`LaserProfileFromFile.cpp:219-233`。

这意味着：

- `from_file` 并不是“只支持 3D openPMD”。
- `lasy` 的 RZ/thetaMode 文件走的是另一条专门的 cylindrical 插值路径。

## 4. `LaserParticleContainer` 的本体是人工天线粒子

### 4.1 `InitData()` 的目标不是生成场，而是布置天线粒子

顶层 `InitData()` 先在 finest level 上调用一次真正的初始化：

```cpp
InitData(maxLevel());
```

源码位置：`LaserParticleContainer.cpp:361-363`。

如果不是 continuous injection 且最终一个粒子都没放进去，WarpX 直接报警并禁用这个 laser：

```cpp
if(!do_continuous_injection && (TotalNumberOfParticles() == 0)){
    ...
    m_enabled = false;
}
```

源码位置：`LaserParticleContainer.cpp:365-370`。

也就是说，laser antenna 的最小存在形式不是一个参数对象，而是至少一批真实粒子。

### 4.2 粒子平面 spacing 来自网格，而不是用户直接指定

`InitData(int lev)` 的第一步就是：

```cpp
ComputeSpacing(lev, S_X, S_Y);
ComputeWeightMobility(S_X, S_Y);
```

源码位置：`LaserParticleContainer.cpp:378-382`。

`ComputeSpacing()` 按 `m_u_X/m_u_Y` 在各坐标轴上的投影，反推出保证“每个 finest cell 至少对应一个发射粒子”的平面 spacing：

```cpp
Sx = std::min(std::min(dx[0]/(std::abs(m_u_X[0])+eps),
                       dx[1]/(std::abs(m_u_X[1])+eps)),
                       dx[2]/(std::abs(m_u_X[2])+eps));
Sy = std::min(std::min(dx[0]/(std::abs(m_u_Y[0])+eps),
                       dx[1]/(std::abs(m_u_Y[1])+eps)),
                       dx[2]/(std::abs(m_u_Y[2])+eps));
```

源码位置：`LaserParticleContainer.cpp:744-750`。

RZ 例外更明显：

```cpp
Sx = dx[0];
Sy = 1.0;
```

源码位置：`LaserParticleContainer.cpp:751-753`。

因此天线粒子分辨率受网格控制，而不是 profile 自己决定。

### 4.3 `Transform` / `InverseTransform` 定义了“实验室坐标 <-> 激光平面坐标”

WarpX 在初始化时显式建立这两个映射：

- `Transform(i,j)`：从平面网格索引生成实验室坐标。源码位置：`LaserParticleContainer.cpp:391-409`
- `InverseTransform(pos)`：把实验室坐标投回激光平面坐标。源码位置：`LaserParticleContainer.cpp:412-424`

随后通过投影 `m_laser_injection_box` 的角点，求出需要布置的平面索引边界 `plane_lo/plane_hi`。源码位置：`LaserParticleContainer.cpp:426-458`。

这一步很关键，因为后面的 profile 计算全部在平面坐标里进行，而 containment 判定仍然要回到真实模拟域。

### 4.4 3D/XZ 与 RZ 的人工天线布局不同

普通 Cartesian/XZ/1D 路径里，每个平面位置都生成一对等权重、异号粒子：

```cpp
for (int k = 0; k<2; ++k) {
    particle_x.push_back(pos[0]);
    particle_y.push_back(pos[1]);
    particle_z.push_back(pos[2]);
}
particle_w.push_back( m_weight);
particle_w.push_back(-m_weight);
```

源码位置：`LaserParticleContainer.cpp:515-522`。

RZ 路径则不是简单复制，而是围绕轴向做 spokes 展开：

```cpp
const auto n_spokes =
    static_cast<int>((WarpX::n_rz_azimuthal_modes - 1)*m_min_particles_per_mode);
...
const Real r_weight = m_weight*2._rt*MathConst::pi*pos[0]/n_spokes;
particle_w.push_back( r_weight);
particle_w.push_back(-r_weight);
```

源码位置：`LaserParticleContainer.cpp:524-537`。

这意味着 RZ 的人工天线不是“把 3D 粒子投影成轴对称”，而是显式构造角向 spokes 和半径权重。

## 5. `Evolve()`：profile 振幅如何变成真实的 `J/rho`

### 5.1 先把时间切回实验室系

如果开了 boosted frame，laser profile 评估用的不是 boosted-frame 时间，而是：

```cpp
t_lab = 1._rt/WarpX::gamma_boost*t + WarpX::beta_boost*m_Z0_lab/PhysConst::c;
```

源码位置：`LaserParticleContainer.cpp:578-584`。

这说明 profile 的物理定义仍然固定在实验室系，boosted frame 只是天线运动和传播计算所在的数值系。

### 5.2 运行时顺序

`Evolve()` 的主链非常稳定：

1. `m_up_laser_profile->update(t_lab)`，必要时推进 from-file 数据块。源码位置：`LaserParticleContainer.cpp:586-587`
2. 可选先沉积一次 `rho` component 0。源码位置：`LaserParticleContainer.cpp:634-643`
3. `calculate_laser_plane_coordinates(...)`，把真实粒子位置转回平面坐标。源码位置：`LaserParticleContainer.cpp:650-653`
4. `fill_amplitude(...)`，为每个粒子求目标振幅。源码位置：`LaserParticleContainer.cpp:655-659`
5. `update_laser_particle(...)`，把目标振幅转成粒子动量和位置。源码位置：`LaserParticleContainer.cpp:661-664`
6. `DepositCurrent(...)`，把人工天线粒子写成 `current_fp` 和必要时的 `current_buf`。源码位置：`LaserParticleContainer.cpp:667-692`
7. 再沉积一次 `rho` component 1。源码位置：`LaserParticleContainer.cpp:696-705`

因此 WarpX 的 laser 注入并不是：

- 直接改 `E/Bfield_fp`
- 直接给边界条件塞解析场

而是：

- 先把目标 laser profile 变成人工天线粒子的位移/动量
- 再通过标准粒子沉积链把它写成网格电流

### 5.3 laser 在 MR 下也走 `fp / buf` 分流

`Evolve()` 里如果当前 level 不是 0 且 `m_deposit_on_main_grid` 打开，`np_to_deposit` 会被设为 0：

```cpp
long np_to_deposit = np;
if (lev > 0 && m_deposit_on_main_grid && has_buffer) {
    np_to_deposit = 0;
}
```

源码位置：`LaserParticleContainer.cpp:628-632`。

后续 `DepositCharge` / `DepositCurrent` 就按 `np_to_deposit` 和 `np-np_to_deposit` 把粒子分别沉到：

- `rho_fp/current_fp`
- `rho_buf/current_buf`

源码位置：`LaserParticleContainer.cpp:634-643, 676-691, 696-705`。

这说明 laser antenna 在 mesh refinement 下并不是特例路径，而是直接进入我们前面已经整理过的 coarse-fine buffer 语义。

## 6. `ContinuousInjection()` 的真实语义

`ContinuousInjection()` 不是“每步都重新生成一整个 laser pulse”，而是检查更新后的天线平面是否第一次进入当前注入盒：

```cpp
if (is_contained)
{
    m_laser_injection_box = injection_box;
    InitData();
}
```

源码位置：`LaserParticleContainer.cpp:314-321`。

这里有两个关键边界：

1. 它依赖 `m_updated_position`，也就是 `UpdateAntennaPosition(dt)` 在 boosted-frame 下更新后的天线位置。源码位置：`LaserParticleContainer.cpp:325-353`
2. `InitData()` 只在天线进入域时调用一次，而不是每个时间步反复重建整片粒子。源码注释位置：`LaserParticleContainer.cpp:318-320`

因此 laser 的 `do_continuous_injection` 更准确的理解是：

- 允许初始在域外的天线，随着 moving window / boosted-frame 相对运动在之后进入域内
- 一旦进入，再生成那一批天线粒子，由后续普通 `Evolve()` 周期性更新其发射振幅

## 7. 验证入口怎样对应源码链

### 7.1 `Examples/Tests/laser_injection/`

`laser_injection/CMakeLists.txt` 注册：

- `test_1d_laser_injection`
- `test_2d_laser_injection`
- `test_3d_laser_injection`
- 以及 1D/2D implicit 变体

它们的 analysis 不是只看 checksum，而是直接把最终场包络与理论 Gaussian envelope 对比，并检查主频是否等于 `c / wavelength`。例如：

- `analysis_1d.py`：包络和频率双断言
- `analysis_2d.py`：斜入射、非平凡偏振下的包络与频率双断言

这组 tests 在验证：

1. `GaussianLaserProfile::fill_amplitude()` 的解析包络
2. `LaserParticleContainer` 的人工天线沉积
3. Maxwell solver 接收到该电流后生成的实际传播场

### 7.2 `Examples/Tests/laser_injection_from_file/`

`laser_injection_from_file/CMakeLists.txt` 明确拆成两阶段：

- `*_prepare`：先生成 lasy/binary 文件
- 主 test：再读取这些文件做注入

analysis 脚本继续对最终场做 envelope/frequency 对照。因此它验证的是：

1. `parse_lasy_file()` / `parse_binary_file()`
2. `time_chunk_size` + `update(t)` 的时间块推进
3. `internal_fill_amplitude_uniform_*()` 的时空插值
4. 后续仍能通过人工天线粒子链生成正确场

特别是：

- `analysis_1d_boost.py` 额外覆盖 boosted-frame 时间变换
- `analysis_from_RZ_file.py` 直接覆盖 `thetaMode` / RZ lasy 路径

## 8. 这一层与上一篇、下一篇怎样衔接

和上一篇相比，这一篇已经把：

- profile 工厂字典
- Gaussian 解析 profile
- from-file/lasy/binary 流式 profile
- 人工天线粒子初始化与运行时 `J/rho` 沉积

接成了一条完整链。

下一层更自然的下钻点是：

1. `LaserProfileFieldFunction.cpp`，把 parser 自定义场函数和前两条 profile 做并排比较。
2. `update_laser_particle(...)`、`ComputeWeightMobility(...)`、`calculate_laser_plane_coordinates(...)`，把“目标振幅如何变成人工粒子轨迹与电流”再向下打穿。

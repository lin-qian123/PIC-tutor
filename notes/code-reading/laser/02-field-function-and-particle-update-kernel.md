# `parse_field_function` 与人工天线粒子更新 kernel

绑定源码：

- `../warpx/Source/Laser/LaserProfilesImpl/LaserProfileFieldFunction.cpp`
- `../warpx/Source/Particles/LaserParticleContainer.cpp`
- `../warpx/Docs/source/usage/parameters.rst`
- `../warpx/Examples/Tests/particle_absorbing_boundary/`

## 1. 这一篇补哪一层

前两篇已经把：

- `ILaserProfile` 工厂分派
- `Gaussian`
- `from_file`
- `LaserParticleContainer::InitData()/Evolve()/ContinuousInjection()`

接起来了，但还有最后一层没完全打穿：

1. `parse_field_function` 到底是不是“只给 parser 接口，剩下什么也不管”。
2. `calculate_laser_plane_coordinates()` 怎样把真实粒子位置投回激光平面。
3. `ComputeWeightMobility()` 和 `update_laser_particle()` 怎样把目标场振幅变成真正可沉积的天线粒子速度、动量和位置。

这一篇把这层补齐。

## 2. `FieldFunctionLaserProfile` 是完整场值，不是包络

### 2.1 参数合同

官方参数文档把 `parse_field_function` 定义得很直接：

```text
<laser_name>.field_function(X,Y,t)
```

这里给出的不是包络，而是完整电场函数；`X`、`Y` 是垂直于 `direction` 的激光平面坐标，`t` 是时间。文档还特别说明：

- 下面那些 Gaussian 专属参数都不会再被使用
- 即便 `wavelength` 和 `e_max` 已经显式写进函数，它们仍然必须提供，因为数值层还要消费

对应文档位置：`Docs/source/usage/parameters.rst:2189-2200`。

这和 `Gaussian`、`from_file` 的一个关键区别是：

- `Gaussian` / `from_file` 交给 profile 的是“发射平面上的目标振幅”
- `parse_field_function` 交给 profile 的是完整场值本身

### 2.2 源码实现几乎是最薄的一层

`FieldFunctionLaserProfile::init()` 只做两件事：

```cpp
utils::parser::Store_parserString(
        ppl, "field_function(X,Y,t)", m_params.field_function);
m_parser = utils::parser::makeParser(m_params.field_function,{"X","Y","t"});
```

源码位置：`LaserProfileFieldFunction.cpp:27-35`。

因此这一层不做：

- amplitude normalization
- wavelength/phase reinterpretation
- envelope construction

它只把用户表达式编译成三变量 parser。

### 2.3 运行时直接逐粒子求值

`fill_amplitude()` 的全部工作就是：

```cpp
auto parser = m_parser.compile<3>();
amrex::ParallelFor(np, [=] AMREX_GPU_DEVICE (int i) noexcept
{
    amplitude[i] = parser(Xp[i], Yp[i], t);
});
```

源码位置：`LaserProfileFieldFunction.cpp:38-47`。

这意味着：

1. `parse_field_function` 不做额外几何修正。
2. 它也不区分 envelope 和 carrier。
3. 它的数值语义完全由用户给出的 `field_function(X,Y,t)` 决定。

真正把这个场值翻译成天线粒子速度和沉积电流的工作，全部在 `LaserParticleContainer` 里。

## 3. `calculate_laser_plane_coordinates()`：把真实粒子位置投回平面坐标

这一步是三类 profile 的共同入口，因为 profile 最终都在激光平面坐标上评估。

核心实现就是对当前位置减去天线平面参考点，再分别投影到 `m_u_X`、`m_u_Y`：

```cpp
pplane_Xp[i] =
    tmp_u_X_0 * (x - tmp_position_0) +
    tmp_u_X_1 * (y - tmp_position_1) +
    tmp_u_X_2 * (z - tmp_position_2);
pplane_Yp[i] =
    tmp_u_Y_0 * (x - tmp_position_0) +
    tmp_u_Y_1 * (y - tmp_position_1) +
    tmp_u_Y_2 * (z - tmp_position_2);
```

源码位置：`LaserParticleContainer.cpp:825-833`。

几何边界：

- 3D / RZ：都显式返回 `plane_Xp` 与 `plane_Yp`
- XZ：只保留 `plane_Xp`，`plane_Yp = 0`
- 1D：两者都固定为 `0`

源码位置：`LaserParticleContainer.cpp:825-842`。

这说明 profile 接口始终是二维 `(X,Y)`，但低维几何通过把缺失方向压成零来复用同一接口。

## 4. `ComputeWeightMobility()`：先定“粒子怎么动”，再定“它要带多大权重”

`LaserParticleContainer` 不是直接根据目标场值反求电流，而是引入一个中间参数 `mobility`：

```cpp
constexpr Real eps = 0.05_rt;
m_mobility = eps/m_e_max;
m_weight = PhysConst::epsilon_0 / m_mobility;
m_weight *= AMREX_D_TERM(1._rt, * Sx, * Sy);
m_mobility = m_mobility/WarpX::gamma_boost;
```

源码位置：`LaserParticleContainer.cpp:766-780`。

这里的逻辑是：

1. 先要求峰值场下粒子速度不超过 `eps * c`，默认 `eps = 0.05`
2. 所以 `mobility` 被设为 `0.05 / e_max`
3. 再用 `epsilon_0 / mobility` 和平面粒子 spacing `Sx,Sy` 反推出单粒子权重
4. 如果在 boosted frame，还要再用 `gamma_boost` 修正 mobility

这意味着 WarpX 在这里优先约束的是“人工天线粒子不要跑得太快”，而不是“先给任意权重，再让速度自己长出来”。

## 5. `update_laser_particle()`：把目标场值变成真实的 `u` 和新位置

### 5.1 场值先变速度，再变动量

单粒子更新的第一步是根据粒子权重符号决定带电方向：

```cpp
const Real sign_charge = (pwp[i]>0) ? -1 : 1;
const Real v_over_c = sign_charge * tmp_mobility * amplitude[i];
```

源码位置：`LaserParticleContainer.cpp:903-905`。

这里正负权重粒子会得到相反速度，因此之后沉积出的电流会叠加，而净电荷尽量抵消。这就是前面 `InitData()` 总是成对创建 `+w/-w` 粒子的原因。

随后速度沿主偏振方向 `p_X` 展开：

```cpp
Real vx = PhysConst::c * v_over_c * tmp_p_X_0;
Real vy = PhysConst::c * v_over_c * tmp_p_X_1;
Real vz = PhysConst::c * v_over_c * tmp_p_X_2;
```

源码位置：`LaserParticleContainer.cpp:909-912`。

### 5.2 boosted frame 下还要减去沿传播方向的平移速度

如果开了 boosted frame，人工天线粒子除了偏振方向速度，还会再减去沿 `nvec` 的 boost 速度：

```cpp
if (gamma_boost > 1.){
    vx -= PhysConst::c * beta_boost * tmp_nvec_0;
    vy -= PhysConst::c * beta_boost * tmp_nvec_1;
    vz -= PhysConst::c * beta_boost * tmp_nvec_2;
}
```

源码位置：`LaserParticleContainer.cpp:913-918`。

这和前一篇里 `t_lab` 的回转换正好对应：profile 仍在实验室系定义，但粒子本身是在 boosted-frame 数值几何中运动。

### 5.3 动量不是简单 `u = v`

WarpX 随后用

```cpp
const Real gamma =
    static_cast<Real>(gamma_boost/std::sqrt(1. - v_over_c*v_over_c));
puxp[i] = gamma * vx;
puyp[i] = gamma * vy;
puzp[i] = gamma * vz;
```

源码位置：`LaserParticleContainer.cpp:919-924`。

因此这里的 `ux/uy/uz` 仍然延续 WarpX 粒子容器的常规约定，是相对论动量型状态变量，而不是单纯速度缓存。

### 5.4 implicit 路径为什么要单独处理

当 `push_type == Implicit` 时，`update_laser_particle()` 不直接从当前位置继续推，而是先取回 timestep 开始时缓存的：

- `x_n`
- `y_n`
- `z_n`

源码位置：`LaserParticleContainer.cpp:876-894`。

随后位置只推进半步：

```cpp
if (push_type == PushType::Implicit) {
    x = x_n[i] + vx * dt*0.5_prt;
}
else {
    x += vx * dt;
}
```

源码位置：`LaserParticleContainer.cpp:939-960`。

这和源码注释写得一致：implicit solver 会在一次 timestep 内多次调用这个函数，所以每次都必须从步初位置重置，并且要把粒子位置保持在 current deposition 期望的 time-centered 层上。源码位置：`LaserParticleContainer.cpp:876-879, 928-933`。

因此 laser antenna 并不是 implicit 求解器外面的例外分支，它也要服从 implicit particle-centering 合同。

## 6. `parse_field_function` 的当前验证入口

当前本地 checkout 里，最明确的 `parse_field_function` 用例不是一个专门的 `laser_profile_field_function` regression，而是：

- `Examples/Tests/particle_absorbing_boundary/inputs_test_1d_particle_absorbing_boundary`

其中 laser 明确写成：

```text
laser1.profile      = parse_field_function
laser1.field_function(X,Y,t) = "Emax*cos(omega0*t)*(
    if (t < t_ramp0, t / t_ramp0, if (t > t_ramp1, 1.0 - ((t - t_ramp1)/t_ramp0), 1.0)))"
```

输入位置：`particle_absorbing_boundary/inputs_test_1d_particle_absorbing_boundary:108-118`。

这说明 `parse_field_function` 当前在 regression 里的角色不是“单独验证 laser profile 数学”，而是作为某个完整边界物理场景里的驱动激光。

对应 `analysis.py` 检查的是吸收边界附近是否还残留过多负向高速电子，而不是直接检查注入场本身。源码位置：`particle_absorbing_boundary/analysis.py:1-41`。

所以这条验证链给 `parse_field_function` 的证据强度是：

- 有真实运行入口
- 但没有专门针对 profile 数学正确性的独立场断言

这也是后续 regression 映射里需要明确标出来的边界。

## 7. 这一层把哪条链闭合了

到这里，laser 主线已经可以从顶到底连成：

1. `LaserProfiles.H` 统一 `init/update/fill_amplitude`
2. `Gaussian`
3. `from_file`
4. `parse_field_function`
5. `calculate_laser_plane_coordinates()`
6. `ComputeWeightMobility()`
7. `update_laser_particle()`
8. `DepositCurrent()/DepositCharge()`

也就是说，`Laser/` 这一轮源码精读已经不再停留在 profile 名字和构造期入口，而是把“激光 profile 怎样最终变成可沉积的人工天线粒子”闭合到了真正的更新 kernel。

## 8. 下一步最自然的方向

从源码层继续往下，最自然的下钻点还有两条：

1. 把 `laser_acceleration`、implicit laser injection、boosted/MR 相关 tests 的 inputs/analysis/checksum 链继续补全。
2. 切回 `Initialization/ExternalField` 与 `WarpXMovingWindow.cpp`，把 laser 与 moving window / boosted-frame 的耦合从 particle antenna 侧再接回全局几何侧。

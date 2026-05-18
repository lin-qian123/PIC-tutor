# `Laser/` 第一轮：profile 字典、公共参数与 `LaserParticleContainer` 分派

绑定源码与文档：

- `../warpx/Source/Laser/LaserProfiles.H`
- `../warpx/Source/Laser/LaserProfilesImpl/LaserProfileGaussian.cpp`
- `../warpx/Source/Laser/LaserProfilesImpl/LaserProfileFieldFunction.cpp`
- `../warpx/Source/Laser/LaserProfilesImpl/LaserProfileFromFile.cpp`
- `../warpx/Source/Particles/LaserParticleContainer.H`
- `../warpx/Source/Particles/LaserParticleContainer.cpp`
- `../warpx/Docs/source/usage/parameters.rst`
- `../warpx/Examples/Tests/laser_injection/`
- `../warpx/Examples/Tests/laser_injection_from_file/`
- `../warpx/Examples/Tests/particle_absorbing_boundary/`

这一篇先回答三件事：

1. laser profile 在 WarpX 里如何做类型分派；
2. `lasers.names` 下面那批参数最后落到哪些对象和约束上；
3. `LaserParticleContainer` 为什么不是普通物理粒子容器，而是“人工天线粒子”。

## 1. `LaserProfiles.H` 给出的不是单个 profile，而是一套接口合同

`LaserProfiles.H` 最核心的定义不是某个具体 Gaussian 公式，而是：

```cpp
class ILaserProfile
{
public:
    virtual void init (const amrex::ParmParse& ppl,
                       CommonLaserParameters params) = 0;

    virtual void update (amrex::Real t) = 0;

    virtual void fill_amplitude (
        int np,
        amrex::Real const * Xp,
        amrex::Real const * Yp,
        amrex::Real t,
        amrex::Real* amplitude) const = 0;
};
```

这定义了 laser profile 的统一合同：

1. `init`
   - 从 `<laser_name>.*` 参数段读取 profile 专属参数；
   - 同时接收公共参数 `CommonLaserParameters`。
2. `update`
   - 给需要时间分块装载或逐步移动窗口消费的 profile 留出每步更新接口。
3. `fill_amplitude`
   - 以激光天线平面坐标 `X/Y` 和时间 `t` 为输入；
   - 为每个 laser antenna particle 生成电场幅值。

从这套接口也能看出一个关键事实：`Laser/` 模块并不直接往 `E/B` 网格写场。它只是提供“在天线粒子处应当有多大幅值”的 profile evaluator，真正写场的是后面的人工天线粒子沉积。

## 2. 公共参数先在 `LaserParticleContainer` 侧归一化，再交给 profile

公共参数结构体很小：

```cpp
struct CommonLaserParameters
{
    amrex::Real wavelength;
    amrex::Real e_max;
    amrex::Vector<amrex::Real> p_X;
    amrex::Vector<amrex::Real> nvec;
};
```

这些值不是 profile 自己从零开始解析的，而是 `LaserParticleContainer` 构造函数先统一读入并规范化：

```cpp
utils::parser::getArrWithParser(pp_laser_name, "position", m_position);
utils::parser::getArrWithParser(pp_laser_name, "direction", m_nvec);
utils::parser::getArrWithParser(pp_laser_name, "polarization", m_p_X);
utils::parser::getWithParser(pp_laser_name, "wavelength", m_wavelength);
```

同时 `e_max` 与 `a0` 必须二选一：

```cpp
const bool e_max_is_specified =
    utils::parser::queryWithParser(pp_laser_name, "e_max", m_e_max);
Real a0;
const bool a0_is_specified =
    utils::parser::queryWithParser(pp_laser_name, "a0", a0);
...
AMREX_ALWAYS_ASSERT_WITH_MESSAGE(
    e_max_is_specified ^ a0_is_specified,
    "Exactly one of e_max or a0 must be specified for the laser.\n");
```

如果给的是 `a0`，WarpX 立刻按

$$
E_{\max} = \frac{m_e \omega c}{q_e} a_0
$$

换成 `e_max`。所以 profile 实现层并不再关心 `a0`，它永远收到的是规范化后的物理场幅值。

## 3. profile 类型分派靠全局字典，不靠一串 if-else

`LaserProfiles.H` 末尾直接定义了 profile 名字到工厂 lambda 的映射：

```cpp
laser_profiles_dictionary =
{
    {"gaussian",
        [] () {return std::make_unique<GaussianLaserProfile>();} },
    {"parse_field_function",
        [] () {return std::make_unique<FieldFunctionLaserProfile>();} },
    {"from_file",
        [] () {return std::make_unique<FromFileLaserProfile>();} }
};
```

`LaserParticleContainer` 构造函数做的事情非常直接：

```cpp
pp_laser_name.get("profile", laser_type_s);
std::transform(laser_type_s.begin(), laser_type_s.end(), laser_type_s.begin(), ::tolower);
...
if(laser_profiles_dictionary.count(laser_type_s) == 0 ){
    WARPX_ABORT_WITH_MESSAGE(std::string("Unknown laser type: ").append(laser_type_s));
}
m_up_laser_profile = laser_profiles_dictionary.at(laser_type_s)();
...
m_up_laser_profile->init(pp_laser_name, common_params);
```

也就是说：

1. 参数层接受 `Gaussian` / `from_file` / `parse_field_function` 这种字符串；
2. 构造层先统一转小写；
3. 再由 profile 字典完成对象工厂分派。

这也是为什么 `Docs/source/usage/parameters.rst` 里 profile 名称要和字典保持严格一致。

## 4. 三类 profile 的职责边界

### 4.1 Gaussian：解析包络，不是直接读表

`GaussianLaserProfile::init()` 读取的是：

- `profile_waist`
- `profile_duration`
- `profile_t_peak`
- `profile_focal_distance`
- `phi0`
- `zeta`
- `beta`
- `phi2`
- `stc_direction`

它随后计算的不是一个简单的标量 envelope，而是包含：

- diffraction / Gouy phase
- focus curvature
- spatio-temporal coupling
- chirp

的复振幅系数。核心代码是：

```cpp
const Complex diffract_factor =
    1._rt + I * m_params.focal_distance * 2._rt/
    ( k0 * m_params.waist * m_params.waist );
...
const Complex stretch_factor = 1._rt + 4._rt *
    ((m_params.zeta+m_params.beta*m_params.focal_distance)*inv_tau2)
    * ((m_params.zeta+m_params.beta*m_params.focal_distance)*inv_complex_waist_2)
    + 2._rt*I*(m_params.phi2-m_params.beta*m_params.beta*k0*m_params.focal_distance)*inv_tau2;
```

所以 Gaussian profile 在 WarpX 里不是“随便给个高斯函数”，而是一个已经包含聚焦、Gouy 相位、STC 和 temporal chirp 的解析 profile。

### 4.2 `parse_field_function`：用户自己给完整场，不只给包络

`FieldFunctionLaserProfile::init()` 做的只有一件事：

```cpp
utils::parser::Store_parserString(
        ppl, "field_function(X,Y,t)", m_params.field_function);
m_parser = utils::parser::makeParser(m_params.field_function,{"X","Y","t"});
```

`fill_amplitude()` 则逐粒子直接调用 parser：

```cpp
amplitude[i] = parser(Xp[i], Yp[i], t);
```

这意味着：

1. 用户给的是完整电场函数，不只是 envelope；
2. 自变量是激光平面坐标 `X/Y` 和时间 `t`；
3. `X/Y` 不是仿真笛卡尔坐标，而是沿天线平面建立的局部坐标。

因此文档里那句“`field_function(X,Y,t)` 的 `X/Y` 未必等于 simulation `x/y`”不是文字提醒，而是直接反映了 `LaserParticleContainer::calculate_laser_plane_coordinates()` 这一层几何投影。

### 4.3 `from_file`：按时间块读 lasy/binary，不要求一次全读进内存

`FromFileLaserProfile::init()` 先强制用户二选一：

```cpp
WARPX_ALWAYS_ASSERT_WITH_MESSAGE (
    lasy_file_name.empty() != binary_file_name.empty(),
    "Exactly one of 'binary_file_name' and 'lasy_file_name' has to be specified");
```

然后根据格式选择：

- `parse_lasy_file(...)`
- `parse_binary_file(...)`

更关键的是它不是把整个时序文件一次全读入，而是维护：

- `time_chunk_size`
- `first_time_index`
- `last_time_index`

并在 `update(t)` 里按需滚动装载下一段时间片：

```cpp
if(idx_t_right >  m_params.last_time_index){
    if (m_params.file_in_lasy_format){
        read_data_t_chunk(idx_t_left, idx_t_left+m_params.time_chunk_size);
    } else{
        read_binary_data_t_chunk(idx_t_left, idx_t_left+m_params.time_chunk_size);
    }
}
```

所以 `from_file` profile 的真实工程边界是：

1. 它支持 lasy 和旧 binary 两种格式；
2. 但它的核心抽象是“时间分块加载的 field movie”；
3. `time_chunk_size` 和 `delay` 都是为了控制这条在线消费链，而不只是文件格式细节。

## 5. `LaserParticleContainer` 不是普通粒子，而是人工天线

类注释写得很直接：

```cpp
The main method to inject a laser pulse in WarpX is to use an artificial
antenna: particles evenly distributed in a given plane (one particle per
cell) move at each iteration and deposit a current J onto the grid...
```

因此它和普通 `PhysicalParticleContainer` 的根本区别是：

1. 它需要 `DepositCurrent`；
2. 但不需要普通 `FieldGather`；
3. 粒子的位移是 prescribed motion，不是 Lorentz force 推出来的。

这也是为什么它直接继承 `WarpXParticleContainer`，而不是 `PhysicalParticleContainer`。

## 6. 构造期几何约束：方向、偏振、boost、moving window

`LaserParticleContainer` 构造函数在 profile 初始化之前就完成了几何合法性检查。

### 6.1 方向和偏振必须正交

```cpp
Real const dp = std::inner_product(
    m_nvec.begin(), m_nvec.end(), m_p_X.begin(), 0.0_rt);
AMREX_ALWAYS_ASSERT_WITH_MESSAGE(std::abs(dp) < 1.0e-14,
    "Laser plane vector is not perpendicular to the main polarization vector");
```

### 6.2 boosted frame 下，laser 方向必须和 boost 方向一致

```cpp
AMREX_ALWAYS_ASSERT_WITH_MESSAGE(
    ... < 1.e-12,
    "The Lorentz boost should be in the same direction as the laser propagation");
```

随后它把天线位置从 lab 坐标转换到 boosted frame：

```cpp
m_Z0_lab = m_nvec[0]*m_position[0] + m_nvec[1]*m_position[1] + m_nvec[2]*m_position[2];
const Real Z0_boost = m_Z0_lab/WarpX::gamma_boost;
m_position[...] += (Z0_boost-m_Z0_lab)*m_nvec[...];
```

这说明文档中“boosted-frame simulation 下仍用 lab-frame 输入 laser position / wavelength / t_peak / focal_distance”的说法，不只是参数约定，而是构造函数真的会在这一层做 Lorentz 相关的几何改写。

### 6.3 continuous injection 只接受很窄的方向组合

`do_continuous_injection` 对 laser 不是泛化选项，而是有强约束：

```cpp
AMREX_ALWAYS_ASSERT_WITH_MESSAGE(
    ...,
    "do_continous_injection for laser particle only works"
    " if moving window direction and laser propagation direction are the same");
```

若再叠加 boosted frame，还要求 boost 方向当前只能是 `z`。

因此：

- 普通 species 的 `do_continuous_injection`
- laser 的 `do_continuous_injection`

虽然参数名字相同，但几何前提明显更苛刻。

## 7. 这第一轮笔记能直接支撑哪些参数和例子

当前已经足够回填的参数包括：

- `lasers.names`
- `<laser_name>.position`
- `<laser_name>.direction`
- `<laser_name>.polarization`
- `<laser_name>.e_max`
- `<laser_name>.a0`
- `<laser_name>.wavelength`
- `<laser_name>.profile`
- `<laser_name>.profile_t_peak`
- `<laser_name>.profile_duration`
- `<laser_name>.profile_waist`
- `<laser_name>.profile_focal_distance`
- `<laser_name>.phi0`
- `<laser_name>.zeta`
- `<laser_name>.beta`
- `<laser_name>.phi2`
- `<laser_name>.do_continuous_injection`
- `<laser_name>.lasy_file_name`
- `<laser_name>.binary_file_name`
- `<laser_name>.time_chunk_size`
- `<laser_name>.delay`

当前最直接的验证入口也已经明确：

1. Gaussian：
   - `Examples/Tests/laser_injection/`
2. from-file：
   - `Examples/Tests/laser_injection_from_file/`
3. field-function：
   - `Examples/Tests/particle_absorbing_boundary/`

## 8. 当前边界

这一篇还没有展开：

1. Gaussian profile 里的 STC/ chirp 公式推导；
2. `FromFileLaserProfile` 在 Cartesian / RZ / binary 下的插值细节；
3. `LaserParticleContainer::InitData()`、`ComputeWeightMobility()`、`Evolve()`、`ContinuousInjection()` 的完整沉积链。

所以下一篇最自然的是：

- `01-gaussian-and-field-function.md`

再下一篇才是：

- `02-laser-particle-container.md`

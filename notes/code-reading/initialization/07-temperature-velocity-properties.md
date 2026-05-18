# TemperatureProperties 与 VelocityProperties 精读

绑定源码：`../warpx`，分支 `pkuHEDPbranch`，commit `063f8b586f04321e13150ae3e730e0794ca75cb1`。

本笔记覆盖：

- `../warpx/Source/Initialization/TemperatureProperties.H/.cpp`
- `../warpx/Source/Initialization/GetTemperature.H/.cpp`
- `../warpx/Source/Initialization/VelocityProperties.H/.cpp`
- `../warpx/Source/Initialization/GetVelocity.H/.cpp`
- `../warpx/Docs/source/usage/parameters.rst:1701-1787`

这些文件只在 `momentum_distribution_type = maxwell_boltzmann` 或 `maxwell_juttner` 时进入主链。它们的职责不是直接生成粒子，而是把输入参数中的无量纲温度 `theta` 和漂移速度 `beta` 编译成 `InjectorMomentumBoltzmann/Juttner` 可调用的轻量 functor。

## 1. 官方物理参数：`theta` 与 `beta`

官方文档位置：`../warpx/Docs/source/usage/parameters.rst:1701-1717`。

```rst
* ``maxwell_boltzmann``: Maxwell-Boltzmann distribution that takes a dimensionless
  temperature parameter :math:`\theta` as an input, where :math:`\theta = \frac{k_\mathrm{B} \cdot T}{m \cdot c^2}`,
  :math:`T` is the temperature in Kelvin, :math:`k_\mathrm{B}` is the Boltzmann constant, :math:`c` is the speed of light, and :math:`m` is the mass of the species.
  Theta is specified by a combination of :pp:param:`<species_name>.theta_distribution_type`, ``<species_name>.theta``, and ``<species_name>.theta_function(x,y,z)`` (see below).
  For values of :math:`\theta > 0.01`, errors due to ignored relativistic terms exceed 1%.
  Temperatures less than zero are not allowed.
  The plasma can be initialized to move at a bulk velocity :math:`\beta = v/c`.
```

无量纲温度定义为：

$$
\theta = \frac{k_B T}{m c^2}.
$$

对于 Maxwell-Boltzmann，代码把每个方向的热动量标准差取为：

$$
\sigma_u = \sqrt{\theta}.
$$

这在非相对论极限成立；当 `theta > 0.01` 时，WarpX 会给出 warning。

Maxwell-Juttner 文档位置：`../warpx/Docs/source/usage/parameters.rst:1723-1738`。

```rst
* ``maxwell_juttner``: Maxwell-Juttner distribution for high temperature plasma that takes a dimensionless temperature parameter :math:`\theta` as an input, where :math:`\theta = \frac{k_\mathrm{B} \cdot T}{m \cdot c^2}`,
  :math:`T` is the temperature in Kelvin, :math:`k_\mathrm{B}` is the Boltzmann constant, and :math:`m` is the mass of the species.
  Theta is specified by a combination of :pp:param:`<species_name>.theta_distribution_type`, ``<species_name>.theta``, and ``<species_name>.theta_function(x,y,z)`` (see below).
  The Sobol method used to generate the distribution will not terminate for :math:`\theta \lesssim 0.1`, and the code will abort if it encounters a temperature below that threshold.
```

Juttner 分布用于相对论热等离子体，当前实现要求：

$$
\theta \ge 0.1.
$$

## 2. `TemperatureProperties`：读取并保存温度参数

源码位置：`../warpx/Source/Initialization/TemperatureProperties.H:16-44`。

```cpp
/* Type of temperature initialization. Used by TemperatureProperties and GetTemperature. */
enum TemperatureInitType {TempConstantValue, TempParserFunction};

struct TemperatureProperties
{
    TemperatureProperties (const amrex::ParmParse& pp, std::string const& source_name);

    /* Type of temperature initialization */
    TemperatureInitType m_type;

    /* Constant temperature value, if m_type == TempConstantValue */
    amrex::Real m_temperature;
    /* Storage of the parser function, if m_type == TempParserFunction */
    std::unique_ptr<amrex::Parser> m_ptr_temperature_parser;
};
```

这个类只保存两种温度来源：

- `TempConstantValue`：常数 `theta`；
- `TempParserFunction`：空间函数 `theta_function(x,y,z)`。

构造函数源码位置：`../warpx/Source/Initialization/TemperatureProperties.cpp:20-74`。

```cpp
TemperatureProperties::TemperatureProperties (const amrex::ParmParse& pp, std::string const& source_name) {
    // Set defaults
    amrex::Real theta = 0; // quiet GCC warning maybe-uninitialized
    std::string temp_dist_s = "constant";
    std::string mom_dist_s;

    utils::parser::query(pp, source_name, "theta_distribution_type", temp_dist_s);
    utils::parser::query(pp, source_name, "momentum_distribution_type", mom_dist_s);
    if (temp_dist_s == "constant") {
        WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
            utils::parser::queryWithParser(pp, source_name, "theta", theta),
            "Temperature parameter theta not specified");

        WARPX_ALWAYS_ASSERT_WITH_MESSAGE(theta >= 0,
            "Temperature parameter theta = " + std::to_string(theta) +
            " is less than zero, which is not allowed");
```

这里有三层约束：

1. 常数温度必须给 `<species>.theta`。
2. `theta < 0` 直接 abort。
3. Juttner 分布下 `theta < 0.1` 直接 abort。

```cpp
        WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
            mom_dist_s != "maxwell_juttner" ||
            theta >= 0.1,
            "Temperature parameter theta = " +
            std::to_string(theta) +
            " is less than minimum 0.1 allowed for Maxwell-Juttner."
        );

        if (mom_dist_s == "maxwell_boltzmann" && theta > 0.01) {
            ablastr::warn_manager::WMRecordWarning(
                "Temperature",
                std::string{"Maxwell-Boltzmann distribution has errors greater than 1%"} +
                std::string{" for temperature parameter theta > 0.01. (theta = "} +
                std::to_string(theta) + " given)");
        }
```

parser 分支：

```cpp
    else if (temp_dist_s == "parser") {
        std::string str_theta_function;
        utils::parser::Store_parserString(pp, source_name, "theta_function(x,y,z)", str_theta_function);
        m_ptr_temperature_parser =
            std::make_unique<amrex::Parser>(
                utils::parser::makeParser(str_theta_function,{"x","y","z"}));
        m_type = TempParserFunction;
    }
```

注意：parser 分支没有在构造期逐点检查 `theta >= 0` 或 Juttner 的 `theta >= 0.1`，因为函数值依赖空间位置。实际检查发生在 `InjectorMomentumBoltzmann/Juttner::getMomentum()` 的采样点上。

## 3. `GetTemperature`：把存储对象编译成 kernel functor

源码位置：`../warpx/Source/Initialization/GetTemperature.H:22-70`。

```cpp
struct GetTemperature
{
    /* Type of temperature initialization */
    TemperatureInitType m_type;

    /* Constant temperature value, if m_type == TempConstantValue */
    amrex::Real m_temperature;
    /* Temperature parser function, if m_type == TempParserFunction */
    amrex::ParserExecutor<3> m_temperature_parser;

    explicit GetTemperature (TemperatureProperties const& temp) noexcept;

    AMREX_GPU_HOST_DEVICE
    amrex::Real operator() (amrex::Real const x, amrex::Real const y, amrex::Real const z) const noexcept
    {
        switch (m_type)
        {
            case (TempConstantValue):
            {
                return m_temperature;
            }
            case (TempParserFunction):
            {
                return m_temperature_parser(x,y,z);
            }
```

构造函数把 `amrex::Parser` 编译成 `ParserExecutor<3>`：

```cpp
GetTemperature::GetTemperature (TemperatureProperties const& temp) noexcept :
    m_type{temp.m_type}
{
    if (m_type == TempConstantValue) {
        m_temperature = temp.m_temperature;
    }
    else if (m_type == TempParserFunction) {
        m_temperature_parser = temp.m_ptr_temperature_parser->compile<3>();
    }
}
```

这一步和 `InjectorMomentum` 的 tagged union 目的相同：GPU kernel 中不能携带普通 parser 对象，必须使用已编译 executor。

## 4. `VelocityProperties`：读取漂移速度方向和大小

源码位置：`../warpx/Source/Initialization/VelocityProperties.H:15-51`。

```cpp
enum VelocityInitType {VelConstantValue, VelParserFunction};

struct VelocityProperties
{
    VelocityProperties (const amrex::ParmParse& pp, std::string const& source_name);

    /* Type of velocity initialization */
    VelocityInitType m_type;

    /* Velocity direction */
    int m_dir; // Index x=0, y=1, z=2
    int m_sign_dir; // Sign of the velocity direction positive=1, negative=-1

    /* Constant velocity value, if m_type == VelConstantValue */
    amrex::Real m_velocity{0};
    /* Storage of the parser function, if m_type == VelParserFunction */
    std::unique_ptr<amrex::Parser> m_ptr_velocity_parser;
};
```

`VelocityProperties` 把 drift velocity 限制成“一个固定方向上的标量场”。方向由 `bulk_vel_dir` 决定，大小由 `beta` 或 `beta_function(x,y,z)` 决定。

构造函数源码位置：`../warpx/Source/Initialization/VelocityProperties.cpp:14-68`。

```cpp
VelocityProperties::VelocityProperties (const amrex::ParmParse& pp, std::string const& source_name)
{
    // Set defaults
    std::string vel_dist_s = "constant";
    std::string vel_dir_s = "x";

    utils::parser::query(pp, source_name, "bulk_vel_dir", vel_dir_s);

    if(vel_dir_s.empty()){
        WARPX_ABORT_WITH_MESSAGE("'<s_name>.bulk_vel_dir input ' can't be empty.");
    }

    m_sign_dir = (vel_dir_s[0] == '-') ? -1 : 1;

    const auto dir = std::tolower(vel_dir_s.back());
```

`bulk_vel_dir` 可以是 `x`、`+x`、`-x` 等形式，符号由首字符决定，方向由最后一个字符决定。然后解析方向索引：

```cpp
    if (dir == 'x'){
        m_dir = 0;
    }
    else if (dir == 'y'){
        m_dir = 1;
    }
    else if (dir == 'z'){
        m_dir = 2;
    }
    else{
        WARPX_ABORT_WITH_MESSAGE(
            "Cannot interpret <s_name>.bulk_vel_dir input '" + vel_dir_s +
            "'. Please enter +/- x, y, or z with no whitespace between the sign and"+
            " other character.");
    }
```

常数速度分支：

```cpp
    utils::parser::query(pp, source_name, "beta_distribution_type", vel_dist_s);
    if (vel_dist_s == "constant") {
        utils::parser::queryWithParser(pp, source_name, "beta", m_velocity);
        m_type = VelConstantValue;
        WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
            m_velocity > -1 && m_velocity < 1,
            "Magnitude of velocity beta = " + std::to_string(m_velocity) +
            " is greater than or equal to 1"
        );
    }
```

这里检查的是输入 `m_velocity` 本身在 `(-1,1)`。如果用户同时给 `bulk_vel_dir=-z` 和 `beta=-0.5`，`GetVelocity` 会再乘 `m_sign_dir`，得到正负号叠加后的结果。因此输入时应把方向符号和 `beta` 符号当成一个整体来理解。

parser 分支：

```cpp
    else if (vel_dist_s == "parser") {
        std::string str_beta_function;
        utils::parser::Store_parserString(pp, source_name, "beta_function(x,y,z)", str_beta_function);
        m_ptr_velocity_parser =
            std::make_unique<amrex::Parser>(
                utils::parser::makeParser(str_beta_function,{"x","y","z"}));
        m_type = VelParserFunction;
    }
```

和温度 parser 一样，位置相关 `beta` 的 `|beta|<1` 检查不能在构造期完成，而是在采样时由 `InjectorMomentum` 检查。

## 5. `GetVelocity`：带方向符号的 drift beta functor

源码位置：`../warpx/Source/Initialization/GetVelocity.H:20-88`。

```cpp
struct GetVelocity
{
    VelocityInitType m_type;

    int m_dir; //! Index x=0, y=1, z=2
    int m_sign_dir; //! Sign of the velocity direction positive=1, negative=-1

    amrex::Real m_velocity{0};
    amrex::ParserExecutor<3> m_velocity_parser;

    explicit GetVelocity (VelocityProperties const& vel) noexcept;

    AMREX_GPU_HOST_DEVICE
    amrex::Real operator() (amrex::Real const x, amrex::Real const y, amrex::Real const z) const noexcept
    {
        switch (m_type)
        {
            case (VelConstantValue):
            {
                return m_sign_dir * m_velocity;
            }
            case (VelParserFunction):
            {
                return m_sign_dir * m_velocity_parser(x,y,z);
            }
```

`direction()` 返回漂移方向索引：

```cpp
    [[nodiscard]]
    AMREX_GPU_HOST_DEVICE
    int direction () const noexcept
    {
        return m_dir;
    }
```

在 `InjectorMomentumBoltzmann/Juttner` 中，`velocity.direction()` 决定 Lorentz boost 应作用在哪一个动量分量上。

## 6. 与 `InjectorMomentumBoltzmann/Juttner` 的连接

源码位置：`../warpx/Source/Utils/SpeciesUtils.cpp:208-219`。

```cpp
} else if (mom_dist_s == "maxwell_boltzmann"){
    h_mom_temp = std::make_unique<TemperatureProperties>(pp_species, source_name);
    const GetTemperature getTemp(*h_mom_temp);
    h_mom_vel = std::make_unique<VelocityProperties>(pp_species, source_name);
    const GetVelocity getVel(*h_mom_vel);
    h_inj_mom = std::make_unique<InjectorMomentum>(InjectorMomentumBoltzmann{getTemp, getVel});
} else if (mom_dist_s == "maxwell_juttner"){
    h_mom_temp = std::make_unique<TemperatureProperties>(pp_species, source_name);
    const GetTemperature getTemp(*h_mom_temp);
    h_mom_vel = std::make_unique<VelocityProperties>(pp_species, source_name);
    const GetVelocity getVel(*h_mom_vel);
    h_inj_mom = std::make_unique<InjectorMomentum>(InjectorMomentumJuttner{getTemp, getVel});
```

这里为什么要把 `TemperatureProperties` 和 `VelocityProperties` 保存在 `h_mom_temp/h_mom_vel` 中？因为 `GetTemperature/GetVelocity` 里的 parser executor 是从这些 properties 编译出来的，properties 需要在构造期间保持 parser 所有权；随后 `InjectorMomentum` 持有的是可拷贝到 GPU 的轻量 functor。

## 7. 在 Boltzmann/Juttner 采样中的物理作用

Boltzmann 采样中：

```cpp
amrex::Real const theta = temperature(x,y,z);
if (theta < 0._rt) {
    amrex::Abort("Negative temperature parameter theta encountered, which is not allowed");
}
amrex::Real const beta = velocity(x,y,z);
if (beta <= -1._rt || beta >= 1._rt) {
    amrex::Abort("beta = v/c magnitude greater than or equal to 1");
}
amrex::Real const vave = std::sqrt(theta);
int const dir = velocity.direction();
```

Juttner 采样中：

```cpp
amrex::Real const theta = temperature(x,y,z);
if (theta < 0.1_rt) {
    amrex::Abort("Temperature parameter theta is less than minimum 0.1 allowed for Maxwell-Juttner");
}
amrex::Real const beta = velocity(x,y,z);
if (beta <= -1._rt || beta >= 1._rt) {
    amrex::Abort("beta = v/c magnitude greater than or equal to 1");
}
int const dir = velocity.direction();
```

因此，这组类的物理边界可以概括为：

- `theta(x,y,z)` 控制热分布宽度或相对论热分布采样。
- `beta(x,y,z)` 控制漂移速度大小。
- `bulk_vel_dir` 控制漂移方向，但方向必须在整个 domain 中一致。
- Maxwell-Boltzmann 是 drift frame 中非相对论热分布，再通过 flipping/Lorentz transform 到 simulation frame。
- Maxwell-Juttner 是 drift frame 中相对论热分布，再通过同类 transform 到 simulation frame。

## 8. 初始化链中的位置

这组对象的完整数据流是：

```text
<species>.momentum_distribution_type = maxwell_boltzmann / maxwell_juttner
  -> SpeciesUtils::parseMomentum()
  -> TemperatureProperties(theta_distribution_type, theta/theta_function)
  -> VelocityProperties(beta_distribution_type, beta/beta_function, bulk_vel_dir)
  -> GetTemperature / GetVelocity
  -> InjectorMomentumBoltzmann / InjectorMomentumJuttner
  -> AddPlasma/AddGaussianBeam calls getMomentum()
```

这说明 Maxwellian 初始化不是简单读 `ux_th` 参数，而是由局域 `theta` 和 drift `beta` 共同决定。后续正式书稿中应把它并入“动量分布初始化”小节，并和 `InjectorMomentum.H` 的采样公式一起讲。

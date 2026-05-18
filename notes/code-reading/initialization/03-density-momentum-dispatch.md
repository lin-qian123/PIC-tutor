# SpeciesUtils 与 InjectorMomentum 精读：从输入参数到动量采样

绑定源码：`../warpx`，分支 `pkuHEDPbranch`，commit `063f8b586f04321e13150ae3e730e0794ca75cb1`。

本笔记覆盖 `../warpx/Source/Utils/SpeciesUtils.H/.cpp` 与 `../warpx/Source/Initialization/InjectorMomentum.H`。它接在 `02-plasma-injector.md` 之后，回答一个更具体的问题：`PlasmaInjector` 读到 species 参数后，怎样把文本输入变成 kernel 可调用的密度函数和动量分布对象。

核心结论：

1. species 的 `charge`、`mass`、`species_type` 由 `SpeciesUtils::extractSpeciesProperties()` 统一解释；显式 `charge/mass` 优先于 `species_type`。
2. 密度分布由 `parseDensity()` 选择：常数、parser 函数、从文件读入三类。
3. 动量分布由 `parseMomentum()` 选择：静止、常数、高斯、高斯通量、均匀、Maxwell-Boltzmann、Maxwell-Juttner、parser、Gaussian parser。
4. `InjectorMomentum` 是一个手写 tagged union；真正注入粒子时，GPU kernel 只通过 `getMomentum()` 和 `getBulkMomentum()` 调用轻量 functor。

## 1. `SpeciesUtils` 的职责边界

源码位置：`../warpx/Source/Utils/SpeciesUtils.H:14-43`。

```cpp
namespace SpeciesUtils
{
    struct SpeciesProperties
    {
        std::optional<amrex::Real> charge;
        std::optional<amrex::Real> mass;
        std::optional<PhysicalSpecies> physical_species;
    };

    SpeciesProperties extractSpeciesProperties (const amrex::ParmParse& pp_species);

    void parseDensity (
        PlasmaInjector & plasma_injector,
        amrex::ParmParse const & pp_species_name);

    std::unique_ptr<InjectorMomentum> parseMomentum (
        amrex::ParmParse const & pp_species_name,
        std::string const & source_name);
}
```

这个头文件说明 `SpeciesUtils` 不持有粒子，也不直接生成粒子。它只做参数到对象的转换：

- `extractSpeciesProperties()` 处理物种物理属性；
- `parseDensity()` 把 `<species>.profile` 转成 `InjectorDensity`；
- `parseMomentum()` 把 `<species>.momentum_distribution_type` 转成 `InjectorMomentum`。

这是一条很重要的边界：`PlasmaInjector` 是容器，`SpeciesUtils` 是构造工具，`AddPlasma` 才是实际创建粒子的 kernel 路径。

## 2. species 类型、质量和电荷的优先级

源码位置：`../warpx/Source/Utils/SpeciesUtils.cpp:23-75`。

```cpp
SpeciesProperties
extractSpeciesProperties (const amrex::ParmParse& pp_species)
{
    std::string physical_species_name;
    std::optional<PhysicalSpecies> physical_species;
    std::optional<amrex::Real> mass;
    std::optional<amrex::Real> charge;
    pp_species.query("species_type", physical_species_name);
    if (physical_species_name != "") {
        physical_species = ConvertPhysicalSpeciesNameToType(physical_species_name);
        WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
            physical_species.has_value(),
            "<species>.species_type not recognized");
        mass = getMass(physical_species.value());
        charge = getCharge(physical_species.value());
    }
    amrex::Real user_charge = 0.0;
    if (pp_species.query("charge", user_charge)) {
        charge = user_charge;
        if (physical_species.has_value()) {
            ablastr::warn_manager::WMRecordWarning(
                "Species",
                "charge was specified but will override charge given by species_type",
                ablastr::warn_manager::WarnPriority::medium);
        }
    }
    amrex::Real user_mass = 0.0;
    if (pp_species.query("mass", user_mass)) {
        mass = user_mass;
        if (physical_species.has_value()) {
            ablastr::warn_manager::WMRecordWarning(
                "Species",
                "mass was specified but will override mass given by species_type",
                ablastr::warn_manager::WarnPriority::medium);
        }
    }
```

逐块解释：

- `species_type` 先被解析成 `PhysicalSpecies`，然后用 `getMass()` 和 `getCharge()` 得到默认质量和电荷。
- 如果用户又显式指定 `charge` 或 `mass`，WarpX 不报错，而是覆盖 `species_type` 的默认值并给 warning。
- 返回类型使用 `std::optional`，因为外部文件注入等路径可能允许属性后置或由文件决定。

物理上，这里的 `charge` 和 `mass` 会进入宏粒子权重、动量单位换算、Lorentz 更新和场电流耦合。覆盖策略意味着输入文件可以用 `species_type = electron` 作为模板，再用显式 `mass/charge` 构造非标准测试粒子。

## 3. `parseDensity()`：密度函数的三种来源

源码位置：`../warpx/Source/Utils/SpeciesUtils.cpp:80-114`。

```cpp
void
parseDensity (PlasmaInjector & plasma_injector,
              amrex::ParmParse const & pp_species_name)
{
    using namespace amrex::literals;

    std::string profile;
    pp_species_name.query("profile", profile);
    if ( profile == "constant" ){
        pp_species_name.query("density", plasma_injector.density);
        plasma_injector.m_inj_rho =
            std::make_unique<InjectorDensity>(InjectorDensityConstant{
                plasma_injector.density});
    } else if (profile == "parse_density_function") {
        std::string str_density_function;
        utils::parser::queryWithParser(pp_species_name, "density_function(x,y,z)", str_density_function);
        auto density_parser =
            std::make_unique<amrex::Parser>(
                utils::parser::makeParser(str_density_function,{"x","y","z"}));
        plasma_injector.m_inj_rho =
            std::make_unique<InjectorDensity>(InjectorDensityParser{
                std::move(density_parser)});
    } else if (profile == "read_from_file") {
        std::string read_density_from_path;
        pp_species_name.query("read_density_from_path", read_density_from_path);
        bool read_density_distributed = false;
        pp_species_name.query("read_density_distributed", read_density_distributed);
        plasma_injector.m_inj_rho =
            std::make_unique<InjectorDensity>(InjectorDensityFromFile{
                read_density_from_path, read_density_distributed});
    }
}
```

三类密度来源分别对应三种物理建模方式：

| `profile` | 对象 | 物理含义 |
|---|---|---|
| `constant` | `InjectorDensityConstant` | 均匀等离子体，`n(x)=n0` |
| `parse_density_function` | `InjectorDensityParser` | 解析输入表达式 `n(x,y,z)`，用于靶材、斜坡、通道等解析分布 |
| `read_from_file` | `InjectorDensityFromFile` | 从外部密度网格读入，适合复杂靶型或预处理数据 |

注意：这段函数只创建密度 functor，不决定生成多少粒子。真正生成时，`AddPlasma()` 会先按每个 cell 的候选粒子数创建候选，再用 `inj_rho->getDensity()` 得到宏粒子权重，并用 `density_min/density_max` 做截断。

## 4. `parseMomentum()`：文本参数到动量分布对象

源码位置：`../warpx/Source/Utils/SpeciesUtils.cpp:119-284`。

```cpp
std::unique_ptr<InjectorMomentum>
parseMomentum (const amrex::ParmParse& pp_species_name, const std::string& source_name)
{
    using namespace amrex::literals;

    std::string momentum_distribution_type;
    pp_species_name.query("momentum_distribution_type", momentum_distribution_type);

    std::unique_ptr<InjectorMomentum> inj_mom = nullptr;

    if (momentum_distribution_type == "at_rest") {
        // Set default value for unspecified parameters
        amrex::XDim3 const u = {0._rt, 0._rt, 0._rt};
        inj_mom = std::make_unique<InjectorMomentum>(InjectorMomentumConstant{u});
    } else if (momentum_distribution_type == "constant") {
        amrex::XDim3 u;
        pp_species_name.get("ux", u.x);
        pp_species_name.get("uy", u.y);
        pp_species_name.get("uz", u.z);
        inj_mom = std::make_unique<InjectorMomentum>(InjectorMomentumConstant{u});
    } else if (momentum_distribution_type == "gaussian") {
        amrex::XDim3 u_m;
        pp_species_name.get("ux_m", u_m.x);
        pp_species_name.get("uy_m", u_m.y);
        pp_species_name.get("uz_m", u_m.z);
        amrex::XDim3 u_th;
        pp_species_name.get("ux_th", u_th.x);
        pp_species_name.get("uy_th", u_th.y);
        pp_species_name.get("uz_th", u_th.z);
        inj_mom = std::make_unique<InjectorMomentum>(InjectorMomentumGaussian{u_m, u_th});
    }
```

这里先处理最常见的三类：

- `at_rest`：令归一化动量 `u=(0,0,0)`；
- `constant`：读入固定 `ux,uy,uz`；
- `gaussian`：读入均值 `ux_m,uy_m,uz_m` 和热扩展 `ux_th,uy_th,uz_th`。

WarpX 在输入层使用的 `u` 是无量纲动量：

$$
u = \gamma \beta = \frac{p}{mc}.
$$

之后写入粒子 SoA 时会乘以 `PhysConst::c`，使 `PIdx::ux/uy/uz` 存储的是 `\gamma v`，这和 pusher 中的速度/动量约定一致。

## 5. `gaussianflux`：通量注入专用动量分布

源码位置：`../warpx/Source/Utils/SpeciesUtils.cpp:145-171`。

```cpp
    } else if (momentum_distribution_type == "gaussianflux") {
        std::string injection_style = "";
        pp_species_name.queryAdd("injection_style", injection_style);
        WARPX_ALWAYS_ASSERT_WITH_MESSAGE(injection_style=="nfluxpercell",
                "gaussianflux momentum only supported with nfluxpercell injection_style");
        amrex::XDim3 u_m;
        pp_species_name.get("ux_m", u_m.x);
        pp_species_name.get("uy_m", u_m.y);
        pp_species_name.get("uz_m", u_m.z);
        amrex::XDim3 u_th;
        pp_species_name.get("ux_th", u_th.x);
        pp_species_name.get("uy_th", u_th.y);
        pp_species_name.get("uz_th", u_th.z);
        int flux_normal_axis = 2;
        int flux_direction = 1;
        std::string flux_normal_axis_string = "z";
        pp_species_name.get("flux_normal_axis", flux_normal_axis_string);
        flux_normal_axis = get_axis_index(flux_normal_axis_string);
        pp_species_name.get("flux_direction", flux_direction);
        inj_mom = std::make_unique<InjectorMomentum>(InjectorMomentumGaussianFlux{
            u_m, u_th, flux_normal_axis, flux_direction});
```

这段代码有一个硬约束：`gaussianflux` 只能与 `injection_style = nfluxpercell` 一起使用。原因是这种分布不是体注入的 Maxwellian 采样，而是“穿过某个注入面”的速度通量采样；法向速度分布需要带有速度权重。

在 kinetic theory 中，穿过面积元的粒子数通量满足

$$
d\Gamma \propto v_n f(\mathbf{v})\,d^3v,
$$

其中 `v_n` 是朝向注入面的法向速度。代码中的 `generateGaussianFluxDist()` 正是在法向方向采样这种带通量权重的分布。

## 6. `uniform`、Boltzmann、Juttner 与 parser 分支

源码位置：`../warpx/Source/Utils/SpeciesUtils.cpp:172-284`。

```cpp
    } else if (momentum_distribution_type == "uniform") {
        amrex::XDim3 u_min;
        pp_species_name.get("ux_min", u_min.x);
        pp_species_name.get("uy_min", u_min.y);
        pp_species_name.get("uz_min", u_min.z);
        amrex::XDim3 u_max;
        pp_species_name.get("ux_max", u_max.x);
        pp_species_name.get("uy_max", u_max.y);
        pp_species_name.get("uz_max", u_max.z);
        inj_mom = std::make_unique<InjectorMomentum>(InjectorMomentumUniform{u_min, u_max});
    } else if (momentum_distribution_type == "maxwell_boltzmann") {
        auto temperature_properties = TemperatureProperties(pp_species_name, source_name);
        auto velocity_properties = VelocityProperties(pp_species_name, source_name);
        inj_mom = std::make_unique<InjectorMomentum>(InjectorMomentumBoltzmann{
            std::move(temperature_properties), std::move(velocity_properties)});
    } else if (momentum_distribution_type == "maxwell_juttner") {
        auto temperature_properties = TemperatureProperties(pp_species_name, source_name);
        auto velocity_properties = VelocityProperties(pp_species_name, source_name);
        inj_mom = std::make_unique<InjectorMomentum>(InjectorMomentumJuttner{
            std::move(temperature_properties), std::move(velocity_properties)});
```

`uniform` 用区间 `[u_min,u_max]` 做每个方向独立均匀采样。`maxwell_boltzmann` 和 `maxwell_juttner` 则引入 `TemperatureProperties` 与 `VelocityProperties`，支持空间变化温度和漂移速度。

Boltzmann 与 Juttner 的物理差别：

- Maxwell-Boltzmann 是非相对论热平衡分布，适合 `kT << mc^2`；
- Maxwell-Juttner 是相对论热平衡分布，适合高温等离子体，但当前实现要求 `theta >= 0.1`。

parser 分支允许直接输入空间函数：

```cpp
    } else if (momentum_distribution_type == "parse_momentum_function") {
        std::string str_momentum_function_ux;
        std::string str_momentum_function_uy;
        std::string str_momentum_function_uz;
        utils::parser::queryWithParser(pp_species_name, "momentum_function_ux(x,y,z)", str_momentum_function_ux);
        utils::parser::queryWithParser(pp_species_name, "momentum_function_uy(x,y,z)", str_momentum_function_uy);
        utils::parser::queryWithParser(pp_species_name, "momentum_function_uz(x,y,z)", str_momentum_function_uz);
        auto parser_ux = std::make_unique<amrex::Parser>(
            utils::parser::makeParser(str_momentum_function_ux,{"x","y","z"}));
        auto parser_uy = std::make_unique<amrex::Parser>(
            utils::parser::makeParser(str_momentum_function_uy,{"x","y","z"}));
        auto parser_uz = std::make_unique<amrex::Parser>(
            utils::parser::makeParser(str_momentum_function_uz,{"x","y","z"}));
        inj_mom = std::make_unique<InjectorMomentum>(InjectorMomentumParser{
            std::move(parser_ux), std::move(parser_uy), std::move(parser_uz)});
```

这类分布适合构造空间变速的流体初态，例如膨胀靶、剪切流、旋转等。旧的 `radial_expansion` 已被移除，源码中会提示用户用 `parse_momentum_function` 替代。

## 7. `InjectorMomentumConstant/Gaussian/Uniform` 的最小实现

源码位置：`../warpx/Source/Initialization/InjectorMomentum.H:32-200`。

```cpp
struct InjectorMomentumConstant
{
    amrex::XDim3 m_u;

    AMREX_GPU_HOST_DEVICE AMREX_FORCE_INLINE
    amrex::XDim3 getMomentum (amrex::Real x, amrex::Real y, amrex::Real z,
                              amrex::RandomEngine const& engine) const noexcept
    {
        amrex::ignore_unused(x,y,z,engine);
        return m_u;
    }

    [[nodiscard]] AMREX_GPU_HOST_DEVICE AMREX_FORCE_INLINE
    amrex::XDim3 getBulkMomentum (amrex::Real x, amrex::Real y, amrex::Real z) const noexcept
    {
        amrex::ignore_unused(x,y,z);
        return m_u;
    }
};
```

`getMomentum()` 和 `getBulkMomentum()` 的区别贯穿后续代码：

- `getMomentum()` 给单个粒子采样，包含热涨落；
- `getBulkMomentum()` 给平均流速，用于 boosted-frame ballistic correction 和束流聚焦等平均运动。

高斯分布：

```cpp
struct InjectorMomentumGaussian
{
    amrex::XDim3 m_u_m;
    amrex::XDim3 m_u_th;

    AMREX_GPU_HOST_DEVICE AMREX_FORCE_INLINE
    amrex::XDim3 getMomentum (amrex::Real x, amrex::Real y, amrex::Real z,
                              amrex::RandomEngine const& engine) const noexcept
    {
        amrex::ignore_unused(x,y,z);
        return {amrex::RandomNormal(m_u_m.x, m_u_th.x, engine),
                amrex::RandomNormal(m_u_m.y, m_u_th.y, engine),
                amrex::RandomNormal(m_u_m.z, m_u_th.z, engine)};
    }
```

均匀分布：

```cpp
struct InjectorMomentumUniform
{
    amrex::XDim3 m_u_min;
    amrex::XDim3 m_u_max;

    AMREX_GPU_HOST_DEVICE AMREX_FORCE_INLINE
    amrex::XDim3 getMomentum (amrex::Real x, amrex::Real y, amrex::Real z,
                              amrex::RandomEngine const& engine) const noexcept
    {
        amrex::ignore_unused(x,y,z);
        return {amrex::Random(engine)*(m_u_max.x-m_u_min.x) + m_u_min.x,
                amrex::Random(engine)*(m_u_max.y-m_u_min.y) + m_u_min.y,
                amrex::Random(engine)*(m_u_max.z-m_u_min.z) + m_u_min.z};
    }
```

这里的设计很直接：所有分布对象都必须能在 host/device 上内联调用，避免在 GPU kernel 内做虚函数调用。

## 8. Maxwell-Boltzmann：局域热速度、漂移速度和 Lorentz 变换

源码位置：`../warpx/Source/Initialization/InjectorMomentum.H:202-284`。

```cpp
struct InjectorMomentumBoltzmann
{
    TemperatureProperties m_temperature_properties;
    VelocityProperties m_velocity_properties;

    AMREX_GPU_HOST_DEVICE AMREX_FORCE_INLINE
    amrex::XDim3 getMomentum (amrex::Real x, amrex::Real y, amrex::Real z,
                              amrex::RandomEngine const& engine) const noexcept
    {
        amrex::Real const theta = m_temperature_properties.getTemperature(x, y, z);
        if (theta < 0._rt) { amrex::Abort("theta should be > 0!"); }

        amrex::XDim3 const beta = m_velocity_properties.getBeta(x,y,z);
        amrex::Real const beta2 = beta.x*beta.x + beta.y*beta.y + beta.z*beta.z;
        if (beta2 >= 1._rt) { amrex::Abort("beta should be < 1!"); }

        amrex::XDim3 const u = {
                std::sqrt(theta)*amrex::RandomNormal(0.0_rt, 1.0_rt, engine),
                std::sqrt(theta)*amrex::RandomNormal(0.0_rt, 1.0_rt, engine),
                std::sqrt(theta)*amrex::RandomNormal(0.0_rt, 1.0_rt, engine)
            };
```

这里 `theta` 是无量纲温度：

$$
\theta = \frac{k_B T}{m c^2}.
$$

非相对论 Maxwellian 在无量纲动量近似下，每个方向的热涨落标准差是 `sqrt(theta)`。如果存在漂移速度 `beta`，代码随后执行一次从局域静止系到实验室系的 Lorentz 变换：

```cpp
        const amrex::Real inv_gamma0 = std::sqrt(1._rt - beta2);
        const amrex::Real u2 = u.x*u.x + u.y*u.y + u.z*u.z;
        const amrex::Real gamma = std::sqrt(1._rt + u2);

        const amrex::Real beta_dot_u = beta.x*u.x + beta.y*u.y + beta.z*u.z;
        const amrex::Real coeff = gamma + beta_dot_u/(1._rt + inv_gamma0);

        return {u.x + coeff*beta.x/inv_gamma0,
                u.y + coeff*beta.y/inv_gamma0,
                u.z + coeff*beta.z/inv_gamma0};
```

这对应四动量从流体静止系到实验室系的 boost。`getBulkMomentum()` 也使用同一漂移速度返回平均动量：

$$
\mathbf{u}_{bulk} = \gamma_0 \boldsymbol{\beta}.
$$

## 9. Maxwell-Juttner：相对论热分布采样

源码位置：`../warpx/Source/Initialization/InjectorMomentum.H:286-387`。

```cpp
struct InjectorMomentumJuttner
{
    TemperatureProperties m_temperature_properties;
    VelocityProperties m_velocity_properties;

    AMREX_GPU_HOST_DEVICE AMREX_FORCE_INLINE
    amrex::XDim3 getMomentum (amrex::Real x, amrex::Real y, amrex::Real z,
                              amrex::RandomEngine const& engine) const noexcept
    {
        const amrex::Real theta = m_temperature_properties.getTemperature(x, y, z);
        if (theta < 0.1_rt) { amrex::Abort("theta should be >= 0.1!"); }

        amrex::XDim3 const beta = m_velocity_properties.getBeta(x,y,z);
        amrex::Real const beta2 = beta.x*beta.x + beta.y*beta.y + beta.z*beta.z;
        if (beta2 >= 1._rt) { amrex::Abort("beta should be < 1!"); }
```

Juttner 分布是相对论热平衡分布，概率密度包含相对论能量因子。代码采用 Zenitani 2015 的采样算法；核心是先采样 Lorentz factor，再采样方向：

```cpp
        amrex::Real const xi = 1.0_rt - std::log(amrex::Random(engine));
        amrex::Real const tmp1 = std::sqrt(1._rt + theta*theta*xi*xi);
        amrex::Real const gamma = theta*xi + tmp1;
        amrex::Real const u_abs = std::sqrt(gamma*gamma - 1._rt);

        amrex::Real const cos_theta = 1._rt - 2._rt*amrex::Random(engine);
        amrex::Real const sin_theta = std::sqrt(1._rt - cos_theta*cos_theta);
        amrex::Real const phi = 2._rt*MathConst::pi*amrex::Random(engine);

        amrex::XDim3 const u = {
            u_abs*sin_theta*std::cos(phi),
            u_abs*sin_theta*std::sin(phi),
            u_abs*cos_theta};
```

然后和 Boltzmann 分支一样，把热静止系动量 Lorentz boost 到带漂移的实验室系。限制 `theta >= 0.1` 是算法适用范围限制，不是物理上 Juttner 分布不存在。

## 10. 手写 tagged union：避免 GPU kernel 中虚派发

源码位置：`../warpx/Source/Initialization/InjectorMomentum.H:459-719`。

```cpp
struct InjectorMomentum
{
    enum struct Type {
        constant,
        gaussian,
        gaussianflux,
        uniform,
        boltzmann,
        juttner,
        parser,
        gaussianparser
    };

    Type type;

    union {
        InjectorMomentumConstant constant;
        InjectorMomentumGaussian gaussian;
        InjectorMomentumGaussianFlux gaussianflux;
        InjectorMomentumUniform uniform;
        InjectorMomentumBoltzmann boltzmann;
        InjectorMomentumJuttner juttner;
        InjectorMomentumParser parser;
        InjectorMomentumGaussianParser gaussianparser;
    };
```

`InjectorMomentum` 用 `type + union` 管理多种分布对象。构造、析构和 move 都显式按 `type` 分派，运行时调用也按 `type` switch：

```cpp
    AMREX_GPU_HOST_DEVICE AMREX_FORCE_INLINE
    amrex::XDim3 getMomentum (amrex::Real x, amrex::Real y, amrex::Real z,
                              amrex::RandomEngine const& engine) const noexcept
    {
        switch (type) {
            case Type::constant : {
                return constant.getMomentum(x,y,z,engine);
            }
            case Type::gaussian : {
                return gaussian.getMomentum(x,y,z,engine);
            }
            case Type::gaussianflux : {
                return gaussianflux.getMomentum(x,y,z,engine);
            }
            case Type::uniform : {
                return uniform.getMomentum(x,y,z,engine);
            }
            case Type::boltzmann : {
                return boltzmann.getMomentum(x,y,z,engine);
            }
            case Type::juttner : {
                return juttner.getMomentum(x,y,z,engine);
            }
            case Type::parser : {
                return parser.getMomentum(x,y,z,engine);
            }
            case Type::gaussianparser : {
                return gaussianparser.getMomentum(x,y,z,engine);
            }
            default : {
                amrex::Abort("InjectorMomentum Type not recognized");
            }
        }
    }
```

这不是面向对象上的优雅写法，而是 GPU kernel 的工程选择：kernel 内不能依赖普通 C++ 虚函数表；用 `switch` 和 union 可以让对象平铺、可拷贝到 device，并保持内联调用。

## 11. 与下一步 `AddPlasma` 的接口

`SpeciesUtils` 和 `InjectorMomentum` 本身不写粒子数组。它们只给后续 kernel 暴露三个关键接口：

```cpp
auto* inj_rho = plasma_injector.getInjectorDensity(mfi.LocalIndex());
InjectorMomentum* inj_mom = plasma_injector.getInjectorMomentumDevice();
InjectorMomentum* h_inj_mom = plasma_injector.getInjectorMomentumHost();
```

在 `AddPlasma()` 中：

- `inj_rho->getDensity(x,y,z)` 决定宏粒子权重；
- `inj_mom->getMomentum(x,y,z,engine)` 决定单粒子动量；
- `h_inj_mom->getBulkMomentum(x,y,z)` 参与 boosted-frame ballistic correction。

因此从输入文件到新粒子的路径可以概括为：

```text
ParmParse species parameters
  -> SpeciesUtils::parseDensity / parseMomentum
  -> InjectorDensity / InjectorMomentum functors
  -> PlasmaInjector stores host/device copies
  -> AddPlasma/AddPlasmaFlux GPU kernels call getDensity/getMomentum
  -> particle SoA: x,y,z,w,ux,uy,uz,runtime attributes
```

下一篇笔记进入 `Particles/ParticleCreation/AddParticles.cpp`，解释这些 functor 怎样在 tile 上批量生成粒子、计算权重、处理 boosted frame、RZ/RSPHERE 坐标和 runtime 属性。

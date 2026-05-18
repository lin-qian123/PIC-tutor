# PlasmaInjector 与粒子初始分布第一轮精读

绑定源码：`../warpx`，分支 `pkuHEDPbranch`，commit `063f8b586f04321e13150ae3e730e0794ca75cb1`。

本笔记覆盖 `../warpx/Source/Initialization/PlasmaInjector.H/.cpp`、`InjectorPosition.H`、`InjectorDensity.H` 和 `Particles/ParticleCreation/DefaultInitialization.H` 的第一轮入口阅读。目标是先建立 species 初始化的总体图谱：输入参数如何被拆成位置采样、密度函数、动量分布、flux 注入、外部 openPMD 文件和运行时属性初始化。

## 1. `PlasmaInjector` 是 species 初始化参数的总容器

源码位置：`../warpx/Source/Initialization/PlasmaInjector.H:33-47`。

```cpp
///
/// The PlasmaInjector class parses and stores information about the plasma
/// type used in the particle container. This information is used to create the
/// particles on initialization and whenever the window moves.
///
class PlasmaInjector
{

public:

    /** Default constructor*/
    PlasmaInjector () = default;

    PlasmaInjector (int ispecies, const std::string& name, const amrex::Geometry& geom,
                    const std::string& src_name="");
```

这段注释给出 `PlasmaInjector` 的边界：它不是粒子容器本身，也不直接执行 PIC pusher；它解析并保存“如何创建初始粒子”的规则。这些规则既用于 simulation initialization，也用于 moving window 连续注入。

内部状态分成几组：

| 状态组 | 代表成员 | 含义 |
|---|---|---|
| 粒子数 | `num_particles_per_cell`, `num_particles_per_cell_each_dim` | 每个 cell 的宏粒子数 |
| 单粒子/多粒子 | `single_particle_pos/u/weight`, `multiple_particles_*` | 手工指定粒子 |
| 高斯束 | `x_m/y_m/z_m`, `x_rms/y_rms/z_rms`, `q_tot/N_tot/npart` | beam-like 初始化 |
| 外部文件 | `external_file`, `z_shift`, `m_openpmd_input_series` | openPMD 粒子文件 |
| flux 注入 | `surface_flux_pos`, `flux_tmin/tmax`, `flux_normal_axis`, `flux_direction` | 边界/平面/EB 注入 |
| 空间范围 | `xmin/xmax/ymin/ymax/zmin/zmax` | 初始 plasma 区域 |
| functor | `InjectorPosition`, `InjectorDensity`, `InjectorMomentum`, `InjectorFlux` | kernel 中实际调用的轻量对象 |

这说明 species 初始化不是单个函数，而是一个组合系统。

## 2. 构造函数解析通用边界和 `injection_style`

源码位置：`../warpx/Source/Initialization/PlasmaInjector.cpp:53-153`。

```cpp
PlasmaInjector::PlasmaInjector (int ispecies, const std::string& name,
    const amrex::Geometry& geom, const std::string& src_name):
#if defined(WARPX_DIM_RZ) || defined(WARPX_DIM_RCYLINDER) || defined(WARPX_DIM_RSPHERE)
    // Default radial_numpercell_power is uniform number of particles per cell
    radial_numpercell_power{0._rt},
#endif
    // Unlimited boundaries
    xmin{std::numeric_limits<amrex::Real>::lowest()},
    xmax{std::numeric_limits<amrex::Real>::max()},
    ymin{std::numeric_limits<amrex::Real>::lowest()},
    ymax{std::numeric_limits<amrex::Real>::max()},
    zmin{std::numeric_limits<amrex::Real>::lowest()},
    zmax{std::numeric_limits<amrex::Real>::max()},
    species_id{ispecies}, species_name{name}, source_name{src_name}, m_geom(geom)
{
```

默认空间边界是无限大，之后再从输入参数覆盖。周期边界下，默认注入范围会被设为 mother grid 尺寸：

```cpp
// NOTE: When periodic boundaries are used, default injection range is set to mother grid dimensions.
if( geom.isPeriodic(0) ) {
#       ifndef WARPX_DIM_1D_Z
    xmin = geom.ProbLo(0);
    xmax = geom.ProbHi(0);
#       else
    zmin = geom.ProbLo(0);
    zmax = geom.ProbHi(0);
#       endif
}
```

这防止周期方向在默认无限范围下产生不受控的注入区域。随后读取显式 `xmin/xmax/...` 和密度上下限：

```cpp
utils::parser::queryWithParser(pp_species, source_name, "xmin", xmin);
utils::parser::queryWithParser(pp_species, source_name, "ymin", ymin);
utils::parser::queryWithParser(pp_species, source_name, "zmin", zmin);
utils::parser::queryWithParser(pp_species, source_name, "xmax", xmax);
utils::parser::queryWithParser(pp_species, source_name, "ymax", ymax);
utils::parser::queryWithParser(pp_species, source_name, "zmax", zmax);

utils::parser::queryWithParser(pp_species, source_name, "density_min", density_min);
utils::parser::queryWithParser(pp_species, source_name, "density_max", density_max);
```

核心分派由 `injection_style` 决定：

```cpp
std::string injection_style = "none";
utils::parser::query(pp_species, source_name, "injection_style", injection_style);
std::transform(injection_style.begin(),
               injection_style.end(),
               injection_style.begin(),
               ::tolower);

num_particles_per_cell_each_dim.assign(3, 0);

if (injection_style == "singleparticle") {
    setupSingleParticle(pp_species);
    return;
} else if (injection_style == "multipleparticles") {
    setupMultipleParticles(pp_species);
    return;
} else if (injection_style == "gaussian_beam") {
    setupGaussianBeam(pp_species);
} else if (injection_style == "nrandompercell") {
    setupNRandomPerCell(pp_species);
} else if (injection_style == "nfluxpercell") {
    setupNFluxPerCell(pp_species);
} else if (injection_style == "nuniformpercell") {
    setupNuniformPerCell(pp_species);
} else if (injection_style == "external_file") {
    setupExternalFile(pp_species);
} else if (injection_style != "none") {
    SpeciesUtils::StringParseAbortMessage("Injection style", injection_style);
}
```

`singleparticle` 和 `multipleparticles` 分支直接 `return`，因为它们不需要通用的 density/momentum functor 体系；其余分支会继续设置 `InjectorDensity` 和 `InjectorMomentum` 并复制到设备端。

## 3. GPU 侧 functor 要求 trivially copyable

源码位置：`../warpx/Source/Initialization/PlasmaInjector.cpp:69-76`。

```cpp
#ifdef AMREX_USE_GPU
static_assert(std::is_trivially_copyable_v<InjectorPosition>,
              "InjectorPosition must be trivially copyable");
static_assert(std::is_trivially_copyable_v<InjectorDensity>,
              "InjectorDensity must be trivially copyable");
static_assert(std::is_trivially_copyable_v<InjectorMomentum>,
              "InjectorMomentum must be trivially copyable");
#endif
```

这解释了为什么 `InjectorPosition`、`InjectorDensity`、`InjectorMomentum` 没有普通 C++ 多态虚函数，而是用 union + type enum 模拟运行时分派。GPU kernel 需要能把 functor 作为简单数据复制到 device。

设备端复制示例：

```cpp
if (h_inj_mom) {
#ifdef AMREX_USE_GPU
    d_inj_mom = static_cast<InjectorMomentum*>
        (amrex::The_Arena()->alloc(sizeof(InjectorMomentum)));
    amrex::Gpu::htod_memcpy_async(d_inj_mom, h_inj_mom.get(), sizeof(InjectorMomentum));
#else
    d_inj_mom = h_inj_mom.get();
#endif
}
amrex::Gpu::synchronize();
```

因此源码讲解时要区分 `h_inj_*` 和 `d_inj_*`：前者是 host 端拥有的对象，后者是 GPU kernel 可直接调用的 device 指针。

## 4. 单粒子和多粒子输入是显式粒子列表

源码位置：`../warpx/Source/Initialization/PlasmaInjector.cpp:195-227`。

```cpp
void PlasmaInjector::setupSingleParticle (amrex::ParmParse const& pp_species)
{
    utils::parser::getArrWithParser(pp_species, source_name, "single_particle_pos", single_particle_pos, 0, 3);
    utils::parser::getArrWithParser(pp_species, source_name, "single_particle_u", single_particle_u, 0, 3);
    for (auto& x : single_particle_u) {
        x *= PhysConst::c;
    }
    utils::parser::getWithParser(pp_species, source_name, "single_particle_weight", single_particle_weight);
    add_single_particle = true;
}
```

输入中的 `single_particle_u` 被乘以 `c`，说明输入使用归一化动量或速度形式，内部保存为带量纲的 `u` 量。这一点在正式章节中要结合 WarpX 参数文档核对单位说明。

多粒子分支检查所有数组长度相同：

```cpp
WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
    ((multiple_particles_pos_x.size() == multiple_particles_pos_y.size()) &&
     (multiple_particles_pos_x.size() == multiple_particles_pos_z.size()) &&
     (multiple_particles_pos_x.size() == multiple_particles_ux.size()) &&
     (multiple_particles_pos_x.size() == multiple_particles_uy.size()) &&
     (multiple_particles_pos_x.size() == multiple_particles_uz.size()) &&
     (multiple_particles_pos_x.size() == multiple_particles_weight.size())),
    "Error: The multiple particles source quantities must all have the same number of elements");
for (auto& vx : multiple_particles_ux) { vx *= PhysConst::c; }
for (auto& vy : multiple_particles_uy) { vy *= PhysConst::c; }
for (auto& vz : multiple_particles_uz) { vz *= PhysConst::c; }
add_multiple_particles = true;
```

这两个分支适合测试和单粒子物理验证，不代表一般 plasma 初始化。

## 5. `nrandompercell` 随机位置 + 密度 + 动量

源码位置：`../warpx/Source/Initialization/PlasmaInjector.cpp:301-330`。

```cpp
void PlasmaInjector::setupNRandomPerCell (amrex::ParmParse const& pp_species)
{
    utils::parser::getWithParser(pp_species, source_name, "num_particles_per_cell", num_particles_per_cell);
#if WARPX_DIM_RZ
    if (WarpX::n_rz_azimuthal_modes > 1) {
    WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
        num_particles_per_cell>=2*WarpX::n_rz_azimuthal_modes,
        "Error: For accurate use of WarpX cylindrical geometry the number "
        "of particles should be at least two times n_rz_azimuthal_modes "
        "(Please visit PR#765 for more information.)");
    }
#endif
    // Construct InjectorPosition with InjectorPositionRandom.
    h_inj_pos = std::make_unique<InjectorPosition>(
        (InjectorPositionRandom*)nullptr,
        xmin, xmax, ymin, ymax, zmin, zmax);
```

`nrandompercell` 的位置由 `InjectorPositionRandom` 给出：

```cpp
struct InjectorPositionRandom
{
    [[nodiscard]]
    AMREX_GPU_HOST_DEVICE
    amrex::XDim3
    getPositionUnitBox (int /*i_part*/, amrex::IntVect const /*ref_fac*/,
                        amrex::RandomEngine const& engine) const noexcept
    {
        return amrex::XDim3{amrex::Random(engine), amrex::Random(engine), amrex::Random(engine)};
    }
};
```

物理含义：每个 cell 内按均匀随机数抽样宏粒子位置；再由 density functor 决定当地权重或采样权重，由 momentum functor 给出初始动量。

## 6. `nuniformpercell` 规则位置采样

源码位置：`../warpx/Source/Initialization/PlasmaInjector.cpp:427-481`。

```cpp
void PlasmaInjector::setupNuniformPerCell (amrex::ParmParse const& pp_species)
{
    // Note that for RZ, three numbers are expected, r, theta, and z.
    // For RCYLINDER, two numbers are expected, r, theta.
    // For RSPHERE, three numbers are expected, r, theta, and phi
    // For 2D, only two are expected. The third is overwritten with 1.
    // For 1D, only one is expected. The second and third are overwritten with 1.
```

不同维度需要的 `num_particles_per_cell_each_dim` 数量不同，缺失维度被填成 1：

```cpp
utils::parser::getArrWithParser(pp_species, source_name, "num_particles_per_cell_each_dim", num_particles_per_cell_each_dim);
WARPX_ALWAYS_ASSERT_WITH_MESSAGE(static_cast<int>(num_particles_per_cell_each_dim.size()) == num_required_ppc_each_dim,
                                 "num_particles_per_cell_each_dim must have " + std::to_string(num_required_ppc_each_dim) + " elements specified");

// overwrite extra dimensions with 1
for (int i = num_required_ppc_each_dim ; i < 3 ; i++) {
    num_particles_per_cell_each_dim.push_back(1);
}
```

规则位置由 `InjectorPositionRegular` 给出：

```cpp
int const ix_part = i_part / (ny*nz);  // written this way backward compatibility
int const iz_part = (i_part-ix_part*(ny*nz)) / ny;
int const iy_part = (i_part-ix_part*(ny*nz)) - ny*iz_part;
return XDim3{
    (0.5_rt + ix_part) / nx,
    (0.5_rt + iy_part) / ny,
    (0.5_rt + iz_part) / nz
};
```

这表示每个 cell 内粒子放在规则子格中心，而不是随机位置。规则采样会降低初始采样噪声，但也可能引入网格对称性，后续噪声和数值 heating 章节需要讨论。

## 7. `nfluxpercell` 是穿过平面或 EB 的连续注入

源码位置：`../warpx/Source/Initialization/PlasmaInjector.cpp:332-425`。

```cpp
void PlasmaInjector::setupNFluxPerCell (amrex::ParmParse const& pp_species)
{
    utils::parser::getWithParser(pp_species, source_name, "num_particles_per_cell", num_particles_per_cell_real);
```

flux 注入支持时间窗口：

```cpp
utils::parser::queryWithParser(pp_species, source_name, "flux_tmin", flux_tmin);
utils::parser::queryWithParser(pp_species, source_name, "flux_tmax", flux_tmax);
```

也支持从 EB 注入：

```cpp
utils::parser::queryWithParser(pp_species, source_name, "inject_from_embedded_boundary", m_inject_from_eb);
if (m_inject_from_eb) {
    AMREX_ALWAYS_ASSERT_WITH_MESSAGE( EB::enabled(),
        "Error: Embedded boundary injection is only available when "
        "embedded boundaries are enabled.");
    flux_normal_axis = 2; // Interpret z as the normal direction to the EB
    flux_direction = 1;
} else {
```

普通平面注入需要解析法向和方向：

```cpp
utils::parser::getWithParser(pp_species, source_name, "surface_flux_pos", surface_flux_pos);
std::string flux_normal_axis_string;
utils::parser::get(pp_species, source_name, "flux_normal_axis", flux_normal_axis_string);
flux_normal_axis = -1;
```

位置 functor 使用 `InjectorPositionRandomPlane`，把一个坐标固定在注入平面上，其余方向随机：

```cpp
h_flux_pos = std::make_unique<InjectorPosition>(
    (InjectorPositionRandomPlane*)nullptr,
    xmin, xmax, ymin, ymax, zmin, zmax,
    flux_normal_axis);
```

flux 本身可为常量或 parser：

```cpp
if (flux_prof_s == "constant") {
    utils::parser::getWithParser(pp_species, source_name, "flux", flux);
    // Construct InjectorFlux with InjectorFluxConstant.
    h_inj_flux.reset(new InjectorFlux((InjectorFluxConstant*)nullptr, flux));
} else if (flux_prof_s == "parse_flux_function") {
    utils::parser::Store_parserString(pp_species, source_name, "flux_function(x,y,z,t)", str_flux_function);
    // Construct InjectorFlux with InjectorFluxParser.
    flux_parser = std::make_unique<amrex::Parser>(
        utils::parser::makeParser(str_flux_function,{"x","y","z","t"}));
```

物理上，flux 注入描述的是单位面积单位时间穿过边界的粒子通量，而不是初始体密度采样。后续必须和 moving window 连续注入分开讲。

## 8. 高斯束和外部文件分支

高斯束分支读取束中心、rms 尺寸、cut、总电荷或真实粒子数、宏粒子数和可选聚焦/旋转：

```cpp
const bool q_tot_is_specified = pp_species.contains("q_tot");
const bool N_tot_is_specified = pp_species.contains("npart_real");
WARPX_ALWAYS_ASSERT_WITH_MESSAGE( q_tot_is_specified != N_tot_is_specified,
    "Error: Exactly one between q_tot and npart_real have to be specified.");
if(q_tot_is_specified){
    utils::parser::getWithParser(pp_species, source_name, "q_tot", q_tot);
}
if(N_tot_is_specified){
    utils::parser::getWithParser(pp_species, source_name, "npart_real", N_tot);
}

utils::parser::getWithParser(pp_species, source_name, "npart", npart);
```

这里强制 `q_tot` 和 `npart_real` 二选一。后续束流章节需要从总电荷、宏粒子权重和真实粒子数之间的关系展开。

外部文件分支要求 openPMD：

```cpp
void PlasmaInjector::setupExternalFile (amrex::ParmParse const& pp_species)
{
#ifndef WARPX_USE_OPENPMD
    WARPX_ABORT_WITH_MESSAGE(
        "WarpX has to be compiled with USE_OPENPMD=TRUE to be able"
        " to read the external openPMD file with species data");
#endif
    external_file = true;
    std::string str_injection_file;
    utils::parser::get(pp_species, source_name, "injection_file", str_injection_file);
```

并可从文件中读取 charge/mass，但输入文件中的 `charge`、`mass` 或 `species_type` 优先级更高：

```cpp
if (charge_from_source) {
    if (charge_is_specified) {
        ablastr::warn_manager::WMRecordWarning("Species",
            "Both '" + ps_name + ".charge' and '" +
                ps_name + ".injection_file' specify a charge.\n'" +
                ps_name + ".charge' will take precedence.\n");
    }
    else if (species_is_specified) {
        ablastr::warn_manager::WMRecordWarning("Species",
            "Both '" + ps_name + ".species_type' and '" +
                ps_name + ".injection_file' specify a charge.\n'" +
                ps_name + ".species_type' will take precedence.\n");
    }
```

## 9. `InjectorDensity` 封装 constant/parser/from-file 三类密度

源码位置：`../warpx/Source/Initialization/InjectorDensity.H:28-121`。

```cpp
// Base struct for density injector.
// InjectorDensity contains a union (called Object) that holds any one
// instance of:
// - InjectorDensityConstant  : to generate constant density;
// - InjectorDensityParser    : to generate density from parser;
// - InjectorDensityFromFile  : to generate density from file;
// The choice is made at runtime, depending in the constructor called.
// This mimics virtual functions.
struct InjectorDensity
{
```

density from file 复用 `ExternalFieldReader` / `ExternalFieldView`：

```cpp
// struct whose getDensity returns density from file.
struct InjectorDensityFromFile
{
    InjectorDensityFromFile (std::string const& a_file_name, amrex::Geometry const& a_geom, bool a_distributed);

    void clear ();

    // This function needs to be called before intializing the density
    // profile, if the openPMD data are distributed. When the openPMD data
    // are loaded in the constructor of this class, we do not know the
    // paricle containers' BoxArray and DistributionMapping yet.
```

这和外场文件读入共享同一个插值基础设施。密度文件读入不是直接成为 `rho_fp`，而是作为 injector density，用于粒子初始化采样。

## 10. 默认运行时属性初始化

源码位置：`../warpx/Source/Particles/ParticleCreation/DefaultInitialization.H:24-59`。

```cpp
/**
 * \brief This set of initialization policies describes what happens
 * when we need to create a new particle due to an elementary process.
 * For example, when an ionization event creates an electron, these
 * policies control the initial values of the electron's components.
 * These can always be over-written later.
 *
 * The specific meanings are as follows:
 *     Zero         - set the component to zero
 *     One          - set the component to one
 *     RandomExp    - a special flag for the optical depth component used by
 *                    certain QED processes, which gets a random initial value
 *                    extracted from an exponential distribution
 *
 */
enum struct InitializationPolicy {Zero=0, One, RandomExp};
```

默认属性表：

```cpp
static std::map<std::string, InitializationPolicy> initialization_policies = {
    {"w",     InitializationPolicy::Zero },
    {"ux",    InitializationPolicy::Zero },
    {"uy",    InitializationPolicy::Zero },
    {"uz",    InitializationPolicy::Zero },
#ifdef WARPX_DIM_RZ
    {"theta", InitializationPolicy::Zero},
#endif

#ifdef WARPX_QED
    {"opticalDepthBW",   InitializationPolicy::RandomExp},
    {"opticalDepthQSR",   InitializationPolicy::RandomExp}
#endif

};
```

这不是 `PlasmaInjector` 的主体，但属于粒子创建的兜底初始化层：如果某些 runtime attributes 没有被外部创建过程设置，就按策略初始化。QED optical depth 使用指数分布随机数，后续 QED 章节要回到这里解释 optical-depth Monte Carlo 的初值。

## 11. 第一轮结论

species 初始化链可以先画成：

```text
MultiParticleContainer / PhysicalParticleContainer construction
  -> per species PlasmaInjector(ispecies, species_name, geom)
     -> read bounds / density_min / density_max
     -> dispatch injection_style
        -> singleparticle / multipleparticles
        -> gaussian_beam
        -> nrandompercell
        -> nfluxpercell
        -> nuniformpercell
        -> external_file
     -> build InjectorPosition / InjectorDensity / InjectorMomentum / InjectorFlux
     -> copy trivially-copyable functors to GPU if needed

InitFromScratch()
  -> mypc->AllocData()
  -> mypc->InitData()
     -> particle creation kernels use injector functors
     -> runtime attributes initialized by DefaultInitialization policies
```

后续需要继续逐项展开：

1. `SpeciesUtils::parseDensity()` 和 `parseMomentum()` 的参数分派。
2. `InjectorMomentum.H` 中 constant、gaussian、uniform、Boltzmann、Juttner、parser 的公式。
3. `Particles/ParticleCreation/AddParticles.cpp` 和 `AddPlasmaUtilities.*` 中如何把 position/density/momentum functor 转成真实宏粒子。

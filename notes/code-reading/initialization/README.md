# Initialization 源码精读入口

绑定源码：`../warpx/Source/Initialization`。

## 模块边界

- 构建入口：`Initialization/CMakeLists.txt`、`Initialization/Make.package`。
- 子模块：`DivCleaner/`。
- 关联模块：`Utils/Parser`、`Utils/WarpXAlgorithmSelection.H`、`Particles/ParticleCreation`。

## 核心问题

- inputs 参数如何进入 `WarpX`、species、laser、solver、diagnostics。
- `PlasmaInjector` 如何组织 density、momentum、position、temperature、flux。
- 外场如何区分 grid external field 与 particle external field。
- projection div cleaner 解决哪些初始约束误差。

## 精读顺序

1. `WarpXAMReXInit.*`：AMReX、MPI、GPU、Python 初始化边界。
2. `WarpXInit.*`：全局初始化辅助函数和维度检查。
3. `WarpXInitData.cpp`：`WarpX::InitData()` 主体。
4. `ExternalField.*`：外场参数与读入。
5. `PlasmaInjector.*` 与 `Injector*.H`：species 初始分布。
6. `Utils/SpeciesUtils.*`：species 质量/电荷、密度和动量分布解析。
7. `Particles/ParticleCreation/AddParticles.cpp` 与 `AddPlasmaUtilities.*`：粒子创建 kernel。
8. `DivCleaner/ProjectionDivCleaner.*`：初始散度清理。

## 输出目标

- `00-init-callgraph.md`
- `01-external-fields.md`
- `02-plasma-injector.md`
- `03-density-momentum-dispatch.md`
- `04-particle-creation-kernels.md`
- `05-projection-div-cleaner.md`
- `06-gaussian-beam-openpmd-injection.md`
- `07-temperature-velocity-properties.md`
- `08-initialization-bootstrap.md`
- `09-preconstruct-parameter-locking.md`
- `10-readparameters-runtime-landing.md`
- `11-readparameters-combination-constraints.md`
- `12-alloclevelmfs-specialized-branches.md`
- `13-initdata-postallocation-consumption.md`
- `14-initialization-validation-map.md`
- `15-initialization-validation-map-external-relativistic-openbc.md`
- `16-initialization-validation-map-density-magnetostatic-nodal.md`
- `17-initialization-validation-map-electrostatic-sphere.md`
- `18-initialization-validation-map-dirichlet-and-effective-potential.md`
- `19-initialization-validation-map-openbc-relativistic-nodal.md`

## 当前进度

- 已完成 `00-init-callgraph.md`：梳理 `main -> WarpX::GetInstance -> InitData -> InitFromScratch/Checkpoint` 的初始化主调用图，并给出后续外场、species、projection div cleaner 的源码入口。
- 已完成 `01-external-fields.md`：区分 grid external field 与 particle external field，梳理 constant / parser / file / Python 路径的输入解析和写入位置。
- 已完成 `02-plasma-injector.md`：梳理 `PlasmaInjector` 如何把 `injection_style`、密度、动量、位置、温度和通量规则组织成 host/device 可调用对象。
- 已完成 `03-density-momentum-dispatch.md`：梳理 `SpeciesUtils` 中 density / momentum / position 解析怎样从输入字符串进入 `InjectorDensity`、`InjectorMomentum` 等具体 functor。
- 已完成 `04-particle-creation-kernels.md`：梳理 `AddParticles.cpp`、`AddPlasmaUtilities.*` 和 `PhysicalParticleContainer::InitData()` 的粒子创建与重分布主链。
- 已完成 `05-projection-div-cleaner.md`：梳理 `ProjectionDivCleaner` 在初始 `A/B` 或外场读入后如何修正离散散度误差。
- 已完成 `06-gaussian-beam-openpmd-injection.md`：梳理 Gaussian beam 注入的权重、cut、focusing、rotation、symmetrization，以及 openPMD 粒子文件读入与单位换算。
- 已完成 `07-temperature-velocity-properties.md`：梳理温度、漂移速度、thermal spread 与相关 runtime particle attributes 的初始化语义。
- 已完成 `08-initialization-bootstrap.md`：梳理 `main.cpp`、`WarpXAMReXInit.*`、`WarpXInit.*` 和 `WarpX::MakeWarpX()` 的启动层，解释 MPI/AMReX/FFT/PETSc 生命周期、AMReX 默认参数覆盖、`geometry.is_periodic` 反推、几何预解析、`geometry.dims` 契约、moving window 读参和 warning manager 初始化。
- 已完成 `09-preconstruct-parameter-locking.md`：继续细化 `MakeWarpX()` 与构造期 `ReadParameters()` 的交界，解释 `ConvertLabParamsToBoost()` 怎样先改写 geometry/tagging 参数、`CheckGriddingForRZSpectral()` 怎样先改写 AMR 分块参数、以及 moving window / boosted frame / warning policy / 容器初始化分别在哪个时机锁定或落地。
- 已完成 `10-readparameters-runtime-landing.md`：梳理 `ReadParameters()` 如何把 solver/grid/boost/moving-window 等输入真正落到 `WarpX` 成员、对象存在性开关和默认派生状态上，并解释这些状态怎样立即决定 `MultiParticleContainer`、`ParticleBoundaryBuffer`、`MultiFluidContainer`、静电 solver 与 `HybridPICModel` 的创建条件。
- 已完成 `11-readparameters-combination-constraints.md`：梳理 `grid_type`、`field_gathering`、`do_current_centering`、`current_deposition`、`particle_shape`、`use_filter`、PSATD/JRhom/Galilean/comoving 和 implicit evolve scheme 之间的组合约束，以及它们怎样继续决定 `current_fp_nodal`、`current_fp_vay`、`current_fp_non_suborbit`、`E_old`、nodal `aux` 场、filter/guard-cell 配额和 `ProjectionDivCleaner` 的初始化前置条件。
- 已完成 `12-alloclevelmfs-specialized-branches.md`：梳理 `AllocLevelMFs()` 中 `rho_fp/phi_fp/F_fp/G_fp` 的条件分配、external grid fields 与 external particle fields 的双合同、`aux` alias 何时被粒子专属外场打断，以及 `HybridPICModel`、fluids、macroscopic medium、EB/ECT 特例怎样继续扩展 field registry 并在 `InitData()` 后半段立刻被消费。
- 已完成 `13-initdata-postallocation-consumption.md`：梳理 `InitData()` 后半中 `ComputeMaxStep/PML/NCI/buffer masks` 的收尾顺序、`m_electrostatic_solver->InitData()` 与 `ComputeSpaceChargeField()` 的职责区分、`ProjectionCleanDivB()` 与初始 self-field solve 的先后、`loadExternalFields` / `AddExternalFields` 的“装填-提交”关系、fresh-run vs restart 的 callback 分叉，以及第 0 步 full/reduced diagnostics 写出的真实状态边界。
- 已完成 `14-initialization-validation-map.md`：整理 `langmuir`、`space_charge_initialization`、`dive_cleaning`、`gaussian_beam`、`effective_potential_electrostatic`、`electrostatic_sphere_eb` 与 `projection_div_cleaner` 这些 examples/regressions 如何分别覆盖 parser 初始化、`gaussian_beam`/`external_file` 注入、`initialize_self_fields`、electrostatic/EB Poisson 初始化和 `ProjectionCleanDivB()`，并明确哪些路径有显式物理断言、哪些目前主要依赖 checksum，哪些在当前本地 checkout 里还存在 analysis 脚本缺口。
- 已完成 `15-initialization-validation-map-external-relativistic-openbc.md`：补充 `load_external_field`、`relativistic_space_charge_initialization` 与 `open_bc_poisson_solver` 三组 regression，整理 grid external field / particle external field / dependency parser / restart 保真、`RelativisticExplicitES` 初始 self-field，以及 open boundary + FFT/sliced FFT relativistic Poisson 初始化各自覆盖的源码链与分析断言。
- 已完成 `16-initialization-validation-map-density-magnetostatic-nodal.md`：补充 `load_density`、`magnetostatic_eb` 与 `nodal_electrostatic` 三组 regression，整理 file-driven density profile 与 moving-window 连续注入、`labframe-electromagnetostatic + EB + initialize_self_fields` 的解析/ checksum 双层证据，以及 collocated relativistic electrostatic 初始 self-field 如何通过 reduced diagnostics 的 `chi` 与 photon 数目做零触发验证。
- 已完成 `17-initialization-validation-map-electrostatic-sphere.md`：补充 `electrostatic_sphere` 这一组 regression，整理均匀带电电子球自场膨胀的解析电场对照、lab-frame 势能账本、MR / collocated / adaptive-dt / RZ uniform-weighting 变体分别覆盖哪条初始化合同，并明确 `analysis_default_regression.py` 与 `catalyst_pipeline.py` 只是 checksum/helper 和可视化脚本。
- 已完成 `18-initialization-validation-map-dirichlet-and-effective-potential.md`：补充 `electrostatic_dirichlet_bc` 与 `effective_potential_electrostatic` 两组 regression，整理 time-dependent Dirichlet 边界势如何通过 `phi` 边界值进入 electrostatic 求解器，以及 effective-potential solver 如何在 PICMI-only 导体球绝热膨胀 benchmark 中通过电子密度径向分布和理论近似做强断言。
- 已完成 `19-initialization-validation-map-openbc-relativistic-nodal.md`：补充 `nodal_electrostatic`、`open_bc_poisson_solver` 与 `relativistic_space_charge_initialization` 三组 regression，整理 collocated relativistic electrostatic 零触发基准、open boundary + FFT/sliced FFT relativistic Poisson 初始化，以及 relativistic Gaussian beam 初始 self-field 三条不同初始化合同，并继续压缩 `electrostatic / Poisson` 这一过粗索引桶。

## 验证线索

- `Examples/Tests/load_external_field/`
- `Examples/Tests/langmuir/`
- `Examples/Tests/space_charge_initialization/`
- `Examples/Tests/dive_cleaning/`
- `Examples/Tests/gaussian_beam/`
- `Examples/Tests/effective_potential_electrostatic/`
- `Examples/Tests/electrostatic_sphere_eb/`
- `Examples/Tests/projection_div_cleaner/`
- `Examples/Tests/relativistic_space_charge_initialization/`
- `Examples/Tests/open_bc_poisson_solver/`
- `Examples/Tests/load_density/`
- `Examples/Tests/magnetostatic_eb/`
- `Examples/Tests/nodal_electrostatic/`
- `Examples/Tests/electrostatic_dirichlet_bc/`
- `Examples/Tests/effective_potential_electrostatic/`
- `Docs/source/usage/parameters.rst`

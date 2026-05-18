# WarpX 源码模块索引

生成来源：`../warpx/Source`

- 源码状态：`pkuHEDPbranch / 063f8b586f04321e13150ae3e730e0794ca75cb1`
- 目标文件数：707
- 阅读状态含义：`未读`、`已定位`、`已做笔记`、`已入正文`、`已验证`。

## 模块统计

| 模块 | 文件数 |
|---|---:|
| FDTD 场求解 | 20 |
| FDTD 算法模板 | 6 |
| Hybrid PIC 场求解 | 7 |
| Python 接口 | 12 |
| WarpX 主类 | 3 |
| ablastr 支撑层 | 78 |
| 构建系统 | 2 |
| 初始化 | 28 |
| 加速器晶格 | 17 |
| 场插值 | 6 |
| 场求解 | 9 |
| 基本过程 | 20 |
| 宏观介质 | 5 |
| 嵌入边界 | 13 |
| 工具与算法选择 | 34 |
| 并行与 AMR | 9 |
| 散度清理初始化 | 4 |
| 时间推进 | 4 |
| 沉积 | 10 |
| 流体模型 | 9 |
| 滤波器 | 9 |
| 激光 | 8 |
| 碰撞 | 62 |
| 磁静态求解 | 4 |
| 程序入口 | 1 |
| 粒子初始化 | 12 |
| 粒子排序 | 5 |
| 粒子推进器 | 11 |
| 粒子热边界 | 4 |
| 粒子系统 | 30 |
| 粒子过滤 | 2 |
| 粒子重采样 | 10 |
| 诊断与 I/O | 132 |
| 谱场求解 | 50 |
| 边界条件 | 20 |
| 隐式求解 | 18 |
| 静电求解 | 13 |
| 非线性/线性求解器 | 20 |

## 框架阶段合并

`module-inventory` 最初按 `Source/` 目录和自动关键词切出模块名，这对全量扫描有用，但和后续写作/精读计划的 15 个阶段并不完全同构。为避免后面继续在“自动模块名”和“计划阶段”之间来回跳转，当前先把整张表的模块人工并回 `docs/warpx-source-reading-framework.md` 中的阶段 0-14。

其中有两个根层例外需要显式说明：

- `Source/Fields.H` 不再保留为 `其他源码`，而归并到阶段 1 的 `WarpX 主类 / field registry`。
- `Source/Make.WarpX` 与根 `Source/Make.package` 不再保留为 `其他源码`，而归并到阶段 0 的 `构建系统`，因为它们承担的是 GNUmake 根层聚合入口，而不是运行期物理模块。

| 精读阶段 | 阶段主题 | 合并后的模块 | 文件数 |
|---|---|---|---:|
| 0 | 全局结构和阅读基础 | 构建系统 | 2 |
| 1 | 根层主类和全局状态 | 程序入口、WarpX 主类 | 4 |
| 2 | 初始化和参数系统 | 初始化、粒子初始化、散度清理初始化 | 44 |
| 3 | 全局时间推进 | 时间推进 | 4 |
| 4 | 粒子系统主干 | 粒子系统、粒子排序、粒子过滤、粒子热边界、粒子重采样 | 51 |
| 5 | gather / pusher / position update | 场插值、粒子推进器 | 17 |
| 6 | 沉积、形函数和源项同步 | 沉积 | 10 |
| 7 | 场求解器总入口 | 场求解 | 9 |
| 8 | FDTD、PML、宏观介质和 filter | FDTD 场求解、FDTD 算法模板、滤波器、宏观介质 | 40 |
| 9 | 谱求解器 PSATD | 谱场求解 | 50 |
| 10 | 静电、磁静态、隐式和非线性求解器 | 静电求解、磁静态求解、隐式求解、非线性/线性求解器 | 55 |
| 11 | 边界、嵌入边界、AMR 和通信 | 边界条件、嵌入边界、并行与 AMR | 42 |
| 12 | 碰撞、电离、QED 和多物理 | 碰撞、基本过程 | 82 |
| 13 | 流体、hybrid PIC、激光和加速器晶格 | 流体模型、Hybrid PIC 场求解、激光、加速器晶格 | 41 |
| 14 | 诊断、I/O、Python 和工具层 | 诊断与 I/O、Python 接口、工具与算法选择、ablastr 支撑层 | 256 |

## 文件清单

| 文件 | 模块 | 物理/算法主题 | 计划章节 | 讲解深度 | 初步符号 | 阅读状态 |
|---|---|---|---|---|---|---|
| `Source/AcceleratorLattice/AcceleratorLattice.H` | 加速器晶格 | beamline elements / lattice finder | 105-106 | 逐块 | AcceleratorLattice | 未读 |
| `Source/AcceleratorLattice/AcceleratorLattice.cpp` | 加速器晶格 | beamline elements / lattice finder | 105-106 | 逐块 | AcceleratorLattice::ReadLattice, AcceleratorLattice::InitElementFinder, AcceleratorLattice::UpdateElementFinder | 未读 |
| `Source/AcceleratorLattice/CMakeLists.txt` | 加速器晶格 | beamline elements / lattice finder | 105-106 | 逐块 |  | 未读 |
| `Source/AcceleratorLattice/LatticeElementFinder.H` | 加速器晶格 | beamline elements / lattice finder | 105-106 | 逐块 | AcceleratorLattice, LatticeElementFinderDevice, are, LatticeElementFinder, that, has | 未读 |
| `Source/AcceleratorLattice/LatticeElementFinder.cpp` | 加速器晶格 | beamline elements / lattice finder | 105-106 | 逐块 | LatticeElementFinder::InitElementFinder, LatticeElementFinder::AllocateIndices, LatticeElementFinder::UpdateIndices, LatticeElementFinderDevice::InitLatticeElementFinderDevice | 未读 |
| `Source/AcceleratorLattice/LatticeElements/CMakeLists.txt` | 加速器晶格 | beamline elements / lattice finder | 105-106 | 逐块 |  | 未读 |
| `Source/AcceleratorLattice/LatticeElements/Drift.H` | 加速器晶格 | beamline elements / lattice finder | 105-106 | 逐块 | Drift | 未读 |
| `Source/AcceleratorLattice/LatticeElements/Drift.cpp` | 加速器晶格 | beamline elements / lattice finder | 105-106 | 逐块 | Drift::AddElement | 未读 |
| `Source/AcceleratorLattice/LatticeElements/HardEdgedPlasmaLens.H` | 加速器晶格 | beamline elements / lattice finder | 105-106 | 逐块 | HardEdgedPlasmaLensDevice, HardEdgedPlasmaLens | 未读 |
| `Source/AcceleratorLattice/LatticeElements/HardEdgedPlasmaLens.cpp` | 加速器晶格 | beamline elements / lattice finder | 105-106 | 逐块 | HardEdgedPlasmaLens::AddElement, HardEdgedPlasmaLens::WriteToDevice, HardEdgedPlasmaLensDevice::InitHardEdgedPlasmaLensDevice | 未读 |
| `Source/AcceleratorLattice/LatticeElements/HardEdgedQuadrupole.H` | 加速器晶格 | beamline elements / lattice finder | 105-106 | 逐块 | HardEdgedQuadrupoleDevice, HardEdgedQuadrupole | 未读 |
| `Source/AcceleratorLattice/LatticeElements/HardEdgedQuadrupole.cpp` | 加速器晶格 | beamline elements / lattice finder | 105-106 | 逐块 | HardEdgedQuadrupole::AddElement, HardEdgedQuadrupole::WriteToDevice, HardEdgedQuadrupoleDevice::InitHardEdgedQuadrupoleDevice | 未读 |
| `Source/AcceleratorLattice/LatticeElements/HardEdged_K.H` | 加速器晶格 | beamline elements / lattice finder | 105-106 | 逐块 | hard_edged_fraction | 未读 |
| `Source/AcceleratorLattice/LatticeElements/LatticeElementBase.H` | 加速器晶格 | beamline elements / lattice finder | 105-106 | 逐块 | LatticeElementBase | 未读 |
| `Source/AcceleratorLattice/LatticeElements/LatticeElementBase.cpp` | 加速器晶格 | beamline elements / lattice finder | 105-106 | 逐块 | LatticeElementBase::AddElementBase, LatticeElementBase::WriteToDeviceBase | 未读 |
| `Source/AcceleratorLattice/LatticeElements/Make.package` | 加速器晶格 | beamline elements / lattice finder | 105-106 | 逐块 |  | 未读 |
| `Source/AcceleratorLattice/Make.package` | 加速器晶格 | beamline elements / lattice finder | 105-106 | 逐块 |  | 未读 |
| `Source/BoundaryConditions/CMakeLists.txt` | 边界条件 | PML / PEC / PMC / Silver-Mueller / field BC | 63-67 | 逐行 |  | 未读 |
| `Source/BoundaryConditions/FieldBoundaries.H` | 边界条件 | PML / PEC / PMC / Silver-Mueller / field BC | 63-67 | 逐行 |  | 未读 |
| `Source/BoundaryConditions/FieldBoundaries.cpp` | 边界条件 | PML / PEC / PMC / Silver-Mueller / field BC | 63-67 | 逐行 | check_periodicity_consistency, parse_field_boundaries, get_periodicity_array | 未读 |
| `Source/BoundaryConditions/Make.package` | 边界条件 | PML / PEC / PMC / Silver-Mueller / field BC | 63-67 | 逐行 |  | 未读 |
| `Source/BoundaryConditions/PEC_Insulator.H` | 边界条件 | PML / PEC / PMC / Silver-Mueller / field BC | 63-67 | 逐行 | PEC_Insulator | 未读 |
| `Source/BoundaryConditions/PEC_Insulator.cpp` | 边界条件 | PML / PEC / PMC / Silver-Mueller / field BC | 63-67 | 逐行 | XDimTransverse, ConvertIndexToCoordinate, constexpr, GetTransverseCoordinates, SetFieldOnPEC_Insulator, SetupFieldParsers, ReadTangentialFieldParser, PEC_Insulator::ApplyPEC_InsulatortoEfield | 未读 |
| `Source/BoundaryConditions/PEC_Insulator_fwd.H` | 边界条件 | PML / PEC / PMC / Silver-Mueller / field BC | 63-67 | 逐行 | PEC_Insulator | 未读 |
| `Source/BoundaryConditions/PML.H` | 边界条件 | PML / PEC / PMC / Silver-Mueller / field BC | 63-67 | 逐行 | Sigma, SigmaBox, SigmaBoxFactory, MultiSigmaBox, PML | 未读 |
| `Source/BoundaryConditions/PML.cpp` | 边界条件 | PML / PEC / PMC / Silver-Mueller / field BC | 63-67 | 逐行 | FillLo, FillHi, FillZero, MakeBoxArray_single, MakeBoxArray_multiple, MakeBoxArray, SigmaBox::define_single, SigmaBox::define_multiple | 未读 |
| `Source/BoundaryConditions/PMLComponent.H` | 边界条件 | PML / PEC / PMC / Silver-Mueller / field BC | 63-67 | 逐行 | PMLComp | 未读 |
| `Source/BoundaryConditions/PML_RZ.H` | 边界条件 | PML / PEC / PMC / Silver-Mueller / field BC | 63-67 | 逐行 | PML_RZ | 未读 |
| `Source/BoundaryConditions/PML_RZ.cpp` | 边界条件 | PML / PEC / PMC / Silver-Mueller / field BC | 63-67 | 逐行 | PML_RZ::ApplyDamping, PML_RZ::FillBoundaryE, PML_RZ::FillBoundaryB, PML_RZ::Restart, PML_RZ::PushPSATD | 未读 |
| `Source/BoundaryConditions/PML_RZ_fwd.H` | 边界条件 | PML / PEC / PMC / Silver-Mueller / field BC | 63-67 | 逐行 | PML_RZ | 未读 |
| `Source/BoundaryConditions/PML_current.H` | 边界条件 | PML / PEC / PMC / Silver-Mueller / field BC | 63-67 | 逐行 | push_ex_pml_current, push_ey_pml_current, push_ez_pml_current, damp_jx_pml, damp_jy_pml, damp_jz_pml | 未读 |
| `Source/BoundaryConditions/PML_fwd.H` | 边界条件 | PML / PEC / PMC / Silver-Mueller / field BC | 63-67 | 逐行 | Sigma, SigmaBox, SigmaBoxFactory, MultiSigmaBox, PML | 未读 |
| `Source/BoundaryConditions/WarpXEvolvePML.cpp` | 边界条件 | PML / PEC / PMC / Silver-Mueller / field BC | 63-67 | 逐行 | WarpX::DampPML, WarpX::DampPML_Cartesian, WarpX::DampJPML, WarpX::CopyJPML | 未读 |
| `Source/BoundaryConditions/WarpXFieldBoundaries.cpp` | 边界条件 | PML / PEC / PMC / Silver-Mueller / field BC | 63-67 | 逐行 | isAnyBoundary, WarpX::ApplyEfieldBoundary, WarpX::ApplyBfieldBoundary, WarpX::ApplyRhofieldBoundary, WarpX::ApplyJfieldBoundary, WarpX::ApplyElectronPressureBoundary | 未读 |
| `Source/BoundaryConditions/WarpX_PEC.H` | 边界条件 | PML / PEC / PMC / Silver-Mueller / field BC | 63-67 | 逐行 |  | 未读 |
| `Source/BoundaryConditions/WarpX_PEC.cpp` | 边界条件 | PML / PEC / PMC / Silver-Mueller / field BC | 63-67 | 逐行 | get_cell_count_to_boundary, SetEfieldOnPEC, SetBfieldOnPEC, ReflectJorRho, SetJorRho, SetNeumannOnPEC, PEC::ApplyPECtoEfield, PEC::ApplyPECtoBfield | 未读 |
| `Source/BoundaryConditions/WarpX_PML_kernels.H` | 边界条件 | PML / PEC / PMC / Silver-Mueller / field BC | 63-67 | 逐行 | warpx_damp_pml_ex, warpx_damp_pml_ey, warpx_damp_pml_ez, warpx_damp_pml_bx, warpx_damp_pml_by, warpx_damp_pml_bz, warpx_damp_pml_scalar | 未读 |
| `Source/Diagnostics/BTD_Plotfile_Header_Impl.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | enables, BTDPlotfileHeaderImpl, BTDMultiFabHeaderImpl, BTDSpeciesHeaderImpl, BTDParticleDataHeaderImpl, set_time, set_timestep, set_problo | 未读 |
| `Source/Diagnostics/BTD_Plotfile_Header_Impl.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | BTDPlotfileHeaderImpl::ReadHeaderData, BTDPlotfileHeaderImpl::AppendNewFabLo, BTDPlotfileHeaderImpl::AppendNewFabHi, BTDPlotfileHeaderImpl::WriteHeader, BTDMultiFabHeaderImpl::ReadMultiFabHeader, BTDMultiFabHeaderImpl::WriteMultiFabHeader, BTDMultiFabHeaderImpl::ResizeFabData, BTDMultiFabHeaderImpl::SetFabName | 未读 |
| `Source/Diagnostics/BTDiagnostics.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | BTDiagnostics, buffer_full, buffer_empty, NullifyFirstFlush, ResetBufferCounter, IncrementBufferFlushCounter | 未读 |
| `Source/Diagnostics/BTDiagnostics.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | BackTransformFunctor, BackTransformParticleFunctor, BTDiagnostics::DerivedInitData, BTDiagnostics::ReadParameters, BTDiagnostics::DoDump, BTDiagnostics::DoComputeAndPack, BTDiagnostics::InitializeBufferData, BTDiagnostics::DefineCellCenteredMultiFab | 未读 |
| `Source/Diagnostics/BoundaryScrapingDiagnostics.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | BoundaryScrapingDiagnostics | 未读 |
| `Source/Diagnostics/BoundaryScrapingDiagnostics.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | BoundaryScrapingDiagnostics::ReadParameters, BoundaryScrapingDiagnostics::InitializeFieldFunctors, BoundaryScrapingDiagnostics::DoComputeAndPack, BoundaryScrapingDiagnostics::DoDump, BoundaryScrapingDiagnostics::Flush | 未读 |
| `Source/Diagnostics/CMakeLists.txt` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 |  | 未读 |
| `Source/Diagnostics/ComputeDiagFunctors/BackTransformFunctor.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | BackTransformFunctor | 未读 |
| `Source/Diagnostics/ComputeDiagFunctors/BackTransformFunctor.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | BackTransformFunctor::operator, BackTransformFunctor::PrepareFunctorData, BackTransformFunctor::InitData, BackTransformFunctor::LorentzTransformZ | 未读 |
| `Source/Diagnostics/ComputeDiagFunctors/BackTransformParticleFunctor.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | SelectParticles, LorentzTransformParticles, BackTransformParticleFunctor | 未读 |
| `Source/Diagnostics/ComputeDiagFunctors/BackTransformParticleFunctor.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | BackTransformParticleFunctor::operator, BackTransformParticleFunctor::InitData, BackTransformParticleFunctor::PrepareFunctorData | 未读 |
| `Source/Diagnostics/ComputeDiagFunctors/CMakeLists.txt` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 |  | 未读 |
| `Source/Diagnostics/ComputeDiagFunctors/CellCenterFunctor.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | CellCenterFunctor | 未读 |
| `Source/Diagnostics/ComputeDiagFunctors/CellCenterFunctor.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 |  | 未读 |
| `Source/Diagnostics/ComputeDiagFunctors/ComputeDiagFunctor.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | ComputeDiagFunctor, PrepareFunctorData, InitData | 未读 |
| `Source/Diagnostics/ComputeDiagFunctors/ComputeDiagFunctor_fwd.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | ComputeDiagFunctor | 未读 |
| `Source/Diagnostics/ComputeDiagFunctors/ComputeParticleDiagFunctor.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | ComputeParticleDiagFunctor, PrepareFunctorData, InitData | 未读 |
| `Source/Diagnostics/ComputeDiagFunctors/DivBFunctor.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | DivBFunctor | 未读 |
| `Source/Diagnostics/ComputeDiagFunctors/DivBFunctor.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 |  | 未读 |
| `Source/Diagnostics/ComputeDiagFunctors/DivEFunctor.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | DivEFunctor | 未读 |
| `Source/Diagnostics/ComputeDiagFunctors/DivEFunctor.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 |  | 未读 |
| `Source/Diagnostics/ComputeDiagFunctors/EBCoveredFunctor.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | EBCoveredFunctor | 未读 |
| `Source/Diagnostics/ComputeDiagFunctors/EBCoveredFunctor.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | EBCoveredFunctor::operator | 未读 |
| `Source/Diagnostics/ComputeDiagFunctors/JFunctor.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | JFunctor | 未读 |
| `Source/Diagnostics/ComputeDiagFunctors/JFunctor.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 |  | 未读 |
| `Source/Diagnostics/ComputeDiagFunctors/JdispFunctor.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | JdispFunctor | 未读 |
| `Source/Diagnostics/ComputeDiagFunctors/JdispFunctor.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 |  | 未读 |
| `Source/Diagnostics/ComputeDiagFunctors/Make.package` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 |  | 未读 |
| `Source/Diagnostics/ComputeDiagFunctors/PartPerCellFunctor.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | PartPerCellFunctor | 未读 |
| `Source/Diagnostics/ComputeDiagFunctors/PartPerCellFunctor.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 |  | 未读 |
| `Source/Diagnostics/ComputeDiagFunctors/PartPerGridFunctor.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | PartPerGridFunctor | 未读 |
| `Source/Diagnostics/ComputeDiagFunctors/PartPerGridFunctor.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 |  | 未读 |
| `Source/Diagnostics/ComputeDiagFunctors/ParticleReductionFunctor.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | ParticleReductionFunctor | 未读 |
| `Source/Diagnostics/ComputeDiagFunctors/ParticleReductionFunctor.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 |  | 未读 |
| `Source/Diagnostics/ComputeDiagFunctors/PhiFunctor.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | PhiFunctor | 未读 |
| `Source/Diagnostics/ComputeDiagFunctors/PhiFunctor.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 |  | 未读 |
| `Source/Diagnostics/ComputeDiagFunctors/ProcessNumberFunctor.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | ProcessNumberFunctor | 未读 |
| `Source/Diagnostics/ComputeDiagFunctors/ProcessNumberFunctor.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 |  | 未读 |
| `Source/Diagnostics/ComputeDiagFunctors/RhoFunctor.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | RhoFunctor | 未读 |
| `Source/Diagnostics/ComputeDiagFunctors/RhoFunctor.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 |  | 未读 |
| `Source/Diagnostics/ComputeDiagFunctors/TemperatureFunctor.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | TemperatureFunctor | 未读 |
| `Source/Diagnostics/ComputeDiagFunctors/TemperatureFunctor.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 |  | 未读 |
| `Source/Diagnostics/Diagnostics.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | struct, Diagnostics, is, InitializeFieldFunctorsRZopenPMD, NewIteration, gettlab, settlab, set_buffer_k_index_hi | 未读 |
| `Source/Diagnostics/Diagnostics.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | Diagnostics::BaseReadParameters, Diagnostics::InitDataBeforeRestart, Diagnostics::InitDataAfterRestart, Diagnostics::InitData, Diagnostics::InitBaseData, Diagnostics::ComputeAndPack, Diagnostics::FilterComputePackFlush | 未读 |
| `Source/Diagnostics/FieldIO.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 |  | 未读 |
| `Source/Diagnostics/FieldIO.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | getVec, getReversedVec, ConstructTotalRZVectorField, ConstructTotalRZScalarField, AverageAndPackVectorField, AverageAndPackScalarField | 未读 |
| `Source/Diagnostics/FlushFormats/CMakeLists.txt` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 |  | 未读 |
| `Source/Diagnostics/FlushFormats/FlushFormat.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | FlushFormat | 未读 |
| `Source/Diagnostics/FlushFormats/FlushFormatAscent.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | aims, FlushFormatAscent | 未读 |
| `Source/Diagnostics/FlushFormats/FlushFormatAscent.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 |  | 未读 |
| `Source/Diagnostics/FlushFormats/FlushFormatCatalyst.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | aims, FlushFormatCatalyst | 未读 |
| `Source/Diagnostics/FlushFormats/FlushFormatCatalyst.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | EmptyParticleData | 未读 |
| `Source/Diagnostics/FlushFormats/FlushFormatCheckpoint.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | FlushFormatCheckpoint | 未读 |
| `Source/Diagnostics/FlushFormats/FlushFormatCheckpoint.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | FlushFormatCheckpoint::CheckpointParticles, FlushFormatCheckpoint::WriteDMaps, FlushFormatCheckpoint::WriteReducedDiagsData | 未读 |
| `Source/Diagnostics/FlushFormats/FlushFormatInSitu.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | is, aims, FlushFormatInSitu | 未读 |
| `Source/Diagnostics/FlushFormats/FlushFormatInSitu.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 |  | 未读 |
| `Source/Diagnostics/FlushFormats/FlushFormatOpenPMD.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | aims, FlushFormatOpenPMD | 未读 |
| `Source/Diagnostics/FlushFormats/FlushFormatOpenPMD.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 |  | 未读 |
| `Source/Diagnostics/FlushFormats/FlushFormatPlotfile.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | aims, FlushFormatPlotfile | 未读 |
| `Source/Diagnostics/FlushFormats/FlushFormatPlotfile.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | FlushFormatPlotfile::WriteParticles, random_filter, WriteRawMF, WriteZeroRawMF, WriteCoarseVector, WriteCoarseScalar | 未读 |
| `Source/Diagnostics/FlushFormats/FlushFormatSensei.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | aims, FlushFormatSensei | 未读 |
| `Source/Diagnostics/FlushFormats/FlushFormatSensei.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 |  | 未读 |
| `Source/Diagnostics/FlushFormats/FlushFormat_fwd.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | FlushFormat | 未读 |
| `Source/Diagnostics/FlushFormats/Make.package` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 |  | 未读 |
| `Source/Diagnostics/FullDiagnostics.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | FullDiagnostics, struct | 未读 |
| `Source/Diagnostics/FullDiagnostics.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | Diagnostics, FullDiagnostics::DerivedInitData, FullDiagnostics::InitializeParticleBuffer, FullDiagnostics::ReadParameters, FullDiagnostics::BackwardCompatibility, FullDiagnostics::Flush, FullDiagnostics::FlushRaw, FullDiagnostics::DoComputeAndPack | 未读 |
| `Source/Diagnostics/Make.package` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 |  | 未读 |
| `Source/Diagnostics/MultiDiagnostics.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | contains, MultiDiagnostics, GetDiag, diagstypes | 未读 |
| `Source/Diagnostics/MultiDiagnostics.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | MultiDiagnostics::InitData, MultiDiagnostics::InitializeFieldFunctors, MultiDiagnostics::ReadParameters, MultiDiagnostics::DoComputeAndPack, MultiDiagnostics::FilterComputePackFlush, MultiDiagnostics::FilterComputePackFlushLastTimestep, MultiDiagnostics::NewIteration | 未读 |
| `Source/Diagnostics/MultiDiagnostics_fwd.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | MultiDiagnostics | 未读 |
| `Source/Diagnostics/OpenPMDHelpFunction.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 |  | 未读 |
| `Source/Diagnostics/OpenPMDHelpFunction.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | WarpXOpenPMDFileType, num_already_flushed | 未读 |
| `Source/Diagnostics/ParticleDiag/CMakeLists.txt` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 |  | 未读 |
| `Source/Diagnostics/ParticleDiag/Make.package` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 |  | 未读 |
| `Source/Diagnostics/ParticleDiag/ParticleDiag.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | ParticleDiag | 未读 |
| `Source/Diagnostics/ParticleDiag/ParticleDiag.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 |  | 未读 |
| `Source/Diagnostics/ParticleDiag/ParticleDiag_fwd.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | ParticleDiag | 未读 |
| `Source/Diagnostics/ParticleIO.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | PhysicalParticleContainer, LaserParticleContainer::ReadHeader, LaserParticleContainer::WriteHeader, RigidInjectedParticleContainer::ReadHeader, PhysicalParticleContainer::ReadHeader, MultiParticleContainer::Restart, MultiParticleContainer::ReadHeader, storePhiOnParticles | 未读 |
| `Source/Diagnostics/ReducedDiags/BeamRelevant.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | contains, BeamRelevant | 未读 |
| `Source/Diagnostics/ReducedDiags/BeamRelevant.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | object, BeamRelevant::ComputeDiags | 未读 |
| `Source/Diagnostics/ReducedDiags/CMakeLists.txt` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 |  | 未读 |
| `Source/Diagnostics/ReducedDiags/ChargeOnEB.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | mainly, ChargeOnEB | 未读 |
| `Source/Diagnostics/ReducedDiags/ChargeOnEB.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | ChargeOnEB::ComputeDiags | 未读 |
| `Source/Diagnostics/ReducedDiags/ColliderRelevant.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | contains, ColliderRelevant, aux_header_index | 未读 |
| `Source/Diagnostics/ReducedDiags/ColliderRelevant.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | object, ColliderRelevant::ComputeDiags | 未读 |
| `Source/Diagnostics/ReducedDiags/DifferentialLuminosity.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | contains, DifferentialLuminosity, aux_header_index | 未读 |
| `Source/Diagnostics/ReducedDiags/DifferentialLuminosity.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | object, DifferentialLuminosity::ComputeDiags | 未读 |
| `Source/Diagnostics/ReducedDiags/DifferentialLuminosity2D.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | contains, DifferentialLuminosity2D | 未读 |
| `Source/Diagnostics/ReducedDiags/DifferentialLuminosity2D.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | object, DifferentialLuminosity2D::ComputeDiags, DifferentialLuminosity2D::WriteToFile | 未读 |
| `Source/Diagnostics/ReducedDiags/FieldEnergy.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | mainly, FieldEnergy | 未读 |
| `Source/Diagnostics/ReducedDiags/FieldEnergy.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | FieldEnergy::ComputeDiags, FieldEnergy::ComputeNorm2 | 未读 |
| `Source/Diagnostics/ReducedDiags/FieldMaximum.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | mainly, FieldMaximum | 未读 |
| `Source/Diagnostics/ReducedDiags/FieldMaximum.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | FieldMaximum::ComputeDiags | 未读 |
| `Source/Diagnostics/ReducedDiags/FieldMomentum.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | mainly, FieldMomentum | 未读 |
| `Source/Diagnostics/ReducedDiags/FieldMomentum.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | FieldMomentum::ComputeDiags | 未读 |
| `Source/Diagnostics/ReducedDiags/FieldPoyntingFlux.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | PoyntingStaggered, PoyntingCellCentered, PoyntingNodal, mainly, FieldPoyntingFlux, EyBx, ExBy, EzBx | 未读 |
| `Source/Diagnostics/ReducedDiags/FieldPoyntingFlux.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | FieldPoyntingFlux::ComputeDiags, FieldPoyntingFlux::ComputeDiagsMidStep, FieldPoyntingFlux::ComputePoyntingFlux, FieldPoyntingFlux::WriteCheckpointData, FieldPoyntingFlux::ReadCheckpointData | 未读 |
| `Source/Diagnostics/ReducedDiags/FieldProbe.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | struct, mainly, FieldProbe, normalize | 未读 |
| `Source/Diagnostics/ReducedDiags/FieldProbe.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | FieldProbe::InitData, FieldProbe::LoadBalance, FieldProbe::ComputeDiags, FieldProbe::WriteToFile | 未读 |
| `Source/Diagnostics/ReducedDiags/FieldProbeParticleContainer.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | is, FieldProbePIdx, defines, FieldProbeParticleContainer | 未读 |
| `Source/Diagnostics/ReducedDiags/FieldProbeParticleContainer.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | FieldProbeParticleContainer::AddNParticles | 未读 |
| `Source/Diagnostics/ReducedDiags/FieldReduction.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | contains, FieldReduction, ComputeFieldReduction | 未读 |
| `Source/Diagnostics/ReducedDiags/FieldReduction.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | FieldReduction::BackwardCompatibility, FieldReduction::ComputeDiags | 未读 |
| `Source/Diagnostics/ReducedDiags/LoadBalanceCosts.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | mainly, LoadBalanceCosts | 未读 |
| `Source/Diagnostics/ReducedDiags/LoadBalanceCosts.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | countBoxMacroParticles, LoadBalanceCosts::ComputeDiags | 未读 |
| `Source/Diagnostics/ReducedDiags/LoadBalanceEfficiency.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | mainly, LoadBalanceEfficiency | 未读 |
| `Source/Diagnostics/ReducedDiags/LoadBalanceEfficiency.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | LoadBalanceEfficiency::ComputeDiags | 未读 |
| `Source/Diagnostics/ReducedDiags/Make.package` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 |  | 未读 |
| `Source/Diagnostics/ReducedDiags/MultiReducedDiags.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | holds, MultiReducedDiags | 未读 |
| `Source/Diagnostics/ReducedDiags/MultiReducedDiags.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | MultiReducedDiags::InitData, MultiReducedDiags::LoadBalance, MultiReducedDiags::ComputeDiags, MultiReducedDiags::ComputeDiagsMidStep, MultiReducedDiags::WriteToFile, MultiReducedDiags::DoDiags, MultiReducedDiags::WriteCheckpointData, MultiReducedDiags::ReadCheckpointData | 未读 |
| `Source/Diagnostics/ReducedDiags/MultiReducedDiags_fwd.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | MultiReducedDiags | 未读 |
| `Source/Diagnostics/ReducedDiags/ParticleEnergy.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | mainly, ParticleEnergy | 未读 |
| `Source/Diagnostics/ReducedDiags/ParticleEnergy.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | object, ParticleEnergy::ComputeDiags | 未读 |
| `Source/Diagnostics/ReducedDiags/ParticleExtrema.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | mainly, ParticleExtrema, aux_header_index | 未读 |
| `Source/Diagnostics/ReducedDiags/ParticleExtrema.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | object, ParticleExtrema::ComputeDiags | 未读 |
| `Source/Diagnostics/ReducedDiags/ParticleHistogram.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | ParticleHistogram | 未读 |
| `Source/Diagnostics/ReducedDiags/ParticleHistogram.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | NormalizationType, object, ParticleHistogram::ComputeDiags | 未读 |
| `Source/Diagnostics/ReducedDiags/ParticleHistogram2D.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | ParticleHistogram2D | 未读 |
| `Source/Diagnostics/ReducedDiags/ParticleHistogram2D.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | object, ParticleHistogram2D::ComputeDiags, ParticleHistogram2D::WriteToFile | 未读 |
| `Source/Diagnostics/ReducedDiags/ParticleMomentum.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | mainly, ParticleMomentum | 未读 |
| `Source/Diagnostics/ReducedDiags/ParticleMomentum.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | object, ParticleMomentum::ComputeDiags | 未读 |
| `Source/Diagnostics/ReducedDiags/ParticleNumber.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | mainly, ParticleNumber | 未读 |
| `Source/Diagnostics/ReducedDiags/ParticleNumber.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | object, ParticleNumber::ComputeDiags | 未读 |
| `Source/Diagnostics/ReducedDiags/ReducedDiags.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | ReducedDiags | 未读 |
| `Source/Diagnostics/ReducedDiags/ReducedDiags.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | ReducedDiags::InitData | 未读 |
| `Source/Diagnostics/ReducedDiags/RhoMaximum.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | mainly, RhoMaximum | 未读 |
| `Source/Diagnostics/ReducedDiags/RhoMaximum.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | object, RhoMaximum::ComputeDiags | 未读 |
| `Source/Diagnostics/ReducedDiags/Timestep.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | contains, Timestep | 未读 |
| `Source/Diagnostics/ReducedDiags/Timestep.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | Timestep::ComputeDiags | 未读 |
| `Source/Diagnostics/WarpXIO.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | WarpX::InitFromCheckpoint | 未读 |
| `Source/Diagnostics/WarpXOpenPMD.H` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | WarpXParticleCounter, WarpXOpenPMDPlot, OpenPMDFileType | 未读 |
| `Source/Diagnostics/WarpXOpenPMD.cpp` | 诊断与 I/O | full/reduced/openPMD/BTD/checkpoint | 107-113 | 逐块 | snakeToCamel, getSeriesOptions, name2openPMD, getParticlePositionComponentLabels, getFieldAxisLabels, getFieldComponentLabels, getUnitDimension, setOpenPMDUnit | 未读 |
| `Source/EmbeddedBoundary/CMakeLists.txt` | 嵌入边界 | EB geometry / scraping / face extension | 68-70 | 逐块 |  | 未读 |
| `Source/EmbeddedBoundary/DistanceToEB.H` | 嵌入边界 | EB geometry / scraping / face extension | 68-70 | 逐块 |  | 未读 |
| `Source/EmbeddedBoundary/EmbeddedBoundaryInit.H` | 嵌入边界 | EB geometry / scraping / face extension | 68-70 | 逐块 |  | 未读 |
| `Source/EmbeddedBoundary/EmbeddedBoundaryInit.cpp` | 嵌入边界 | EB geometry / scraping / face extension | 68-70 | 逐块 | web::MarkReducedShapeCells, web::MarkUpdateCellsStairCase, web::MarkUpdateECellsECT, web::MarkUpdateBCellsECT, web::MarkExtensionCells, web::ComputeEdgeLengths, web::ComputeFaceAreas, web::ScaleEdges | 未读 |
| `Source/EmbeddedBoundary/Enabled.H` | 嵌入边界 | EB geometry / scraping / face extension | 68-70 | 逐块 |  | 未读 |
| `Source/EmbeddedBoundary/Enabled.cpp` | 嵌入边界 | EB geometry / scraping / face extension | 68-70 | 逐块 | enabled | 未读 |
| `Source/EmbeddedBoundary/Make.package` | 嵌入边界 | EB geometry / scraping / face extension | 68-70 | 逐块 |  | 未读 |
| `Source/EmbeddedBoundary/ParticleBoundaryProcess.H` | 嵌入边界 | EB geometry / scraping / face extension | 68-70 | 逐块 | NoOp, Absorb | 未读 |
| `Source/EmbeddedBoundary/ParticleScraper.H` | 嵌入边界 | EB geometry / scraping / face extension | 68-70 | 逐块 | PC, F, scrapeParticlesAtEB | 未读 |
| `Source/EmbeddedBoundary/WarpXFaceExtensions.cpp` | 嵌入边界 | EB geometry / scraping / face extension | 68-70 | 逐块 | T, CountExtFaces, ComputeSStab, constexpr, ApplyBCKCorrection, init_borrowing, shrink_borrowing, GetNeigh | 未读 |
| `Source/EmbeddedBoundary/WarpXFaceInfoBox.H` | 嵌入边界 | EB geometry / scraping / face extension | 68-70 | 逐块 | FaceInfoBox, Neighbours, addConnectedNeighbor, uint8_to_inds | 未读 |
| `Source/EmbeddedBoundary/WarpXFaceInfoBox_fwd.H` | 嵌入边界 | EB geometry / scraping / face extension | 68-70 | 逐块 | FaceInfoBox | 未读 |
| `Source/EmbeddedBoundary/WarpXInitEB.cpp` | 嵌入边界 | EB geometry / scraping / face extension | 68-70 | 逐块 | ParserIF, operator, WarpX::InitEB, WarpX::ComputeDistanceToEB | 未读 |
| `Source/Evolve/CMakeLists.txt` | 时间推进 | PIC 主循环 / 时间层 / subcycling | 12-16 | 逐行 |  | 未读 |
| `Source/Evolve/Make.package` | 时间推进 | PIC 主循环 / 时间层 / subcycling | 12-16 | 逐行 |  | 未读 |
| `Source/Evolve/WarpXComputeDt.cpp` | 时间推进 | PIC 主循环 / 时间层 / subcycling | 12-16 | 逐行 | minDim, WarpX::ComputeDt, WarpX::UpdateDtFromParticleSpeeds | 未读 |
| `Source/Evolve/WarpXEvolve.cpp` | 时间推进 | PIC 主循环 / 时间层 / subcycling | 12-16 | 逐行 | checkEarlyUnusedParams, StoreCurrent, RestoreCurrent, WarpX::SynchronizeVelocityWithPosition, WarpX::Evolve, WarpX::OneStep, WarpX::OneStep_nosub, WarpX::checkStopSimulation | 未读 |
| `Source/FieldSolver/CMakeLists.txt` | 场求解 | EM/ES/hybrid/implicit/QED field push | 46-62 | 逐块 |  | 未读 |
| `Source/FieldSolver/ElectrostaticSolvers/CMakeLists.txt` | 静电求解 | Poisson / electrostatic PIC | 57 | 逐块 |  | 未读 |
| `Source/FieldSolver/ElectrostaticSolvers/EffectivePotentialES.H` | 静电求解 | Poisson / electrostatic PIC | 57 | 逐块 | EffectivePotentialES | 未读 |
| `Source/FieldSolver/ElectrostaticSolvers/EffectivePotentialES.cpp` | 静电求解 | Poisson / electrostatic PIC | 57 | 逐块 | EffectivePotentialES::InitData, EffectivePotentialES::ComputeSpaceChargeField, EffectivePotentialES::computePhi, EffectivePotentialES::ComputeSigma, std::abs | 未读 |
| `Source/FieldSolver/ElectrostaticSolvers/ElectrostaticSolver.H` | 静电求解 | Poisson / electrostatic PIC | 57 | 逐块 | ElectrostaticSolver, InitData | 未读 |
| `Source/FieldSolver/ElectrostaticSolvers/ElectrostaticSolver.cpp` | 静电求解 | Poisson / electrostatic PIC | 57 | 逐块 | ElectrostaticSolver::ReadParameters, ElectrostaticSolver::setPhiBC, ElectrostaticSolver::computeB | 未读 |
| `Source/FieldSolver/ElectrostaticSolvers/ElectrostaticSolver_fwd.H` | 静电求解 | Poisson / electrostatic PIC | 57 | 逐块 | ElectrostaticSolver | 未读 |
| `Source/FieldSolver/ElectrostaticSolvers/LabFrameExplicitES.H` | 静电求解 | Poisson / electrostatic PIC | 57 | 逐块 | LabFrameExplicitES | 未读 |
| `Source/FieldSolver/ElectrostaticSolvers/LabFrameExplicitES.cpp` | 静电求解 | Poisson / electrostatic PIC | 57 | 逐块 | LabFrameExplicitES::InitData, LabFrameExplicitES::ComputeSpaceChargeField, LabFrameExplicitES::computePhiTriDiagonal, LabFrameExplicitES::computePhiTriDiagonal_periodic | 未读 |
| `Source/FieldSolver/ElectrostaticSolvers/Make.package` | 静电求解 | Poisson / electrostatic PIC | 57 | 逐块 |  | 未读 |
| `Source/FieldSolver/ElectrostaticSolvers/PoissonBoundaryHandler.H` | 静电求解 | Poisson / electrostatic PIC | 57 | 逐块 | PoissonBoundaryHandler, PhiCalculatorEB, EBCalcEfromPhiPerLevel, setPotentialEB | 未读 |
| `Source/FieldSolver/ElectrostaticSolvers/PoissonBoundaryHandler.cpp` | 静电求解 | Poisson / electrostatic PIC | 57 | 逐块 | PoissonBoundaryHandler::ReadParameters, PoissonBoundaryHandler::DefinePhiBCs, PoissonBoundaryHandler::BuildParsers, PoissonBoundaryHandler::BuildParsersEB | 未读 |
| `Source/FieldSolver/ElectrostaticSolvers/RelativisticExplicitES.H` | 静电求解 | Poisson / electrostatic PIC | 57 | 逐块 | RelativisticExplicitES | 未读 |
| `Source/FieldSolver/ElectrostaticSolvers/RelativisticExplicitES.cpp` | 静电求解 | Poisson / electrostatic PIC | 57 | 逐块 | RelativisticExplicitES::InitData, RelativisticExplicitES::ComputeSpaceChargeField, RelativisticExplicitES::AddSpaceChargeField, RelativisticExplicitES::AddBoundaryField | 未读 |
| `Source/FieldSolver/FiniteDifferenceSolver/ApplySilverMuellerBoundary.cpp` | FDTD 场求解 | Maxwell FDTD / PML / cleaning | 47-52 | 逐行 | FiniteDifferenceSolver::ApplySilverMuellerBoundary | 未读 |
| `Source/FieldSolver/FiniteDifferenceSolver/CMakeLists.txt` | FDTD 场求解 | Maxwell FDTD / PML / cleaning | 47-52 | 逐行 |  | 未读 |
| `Source/FieldSolver/FiniteDifferenceSolver/ComputeCurlA.cpp` | FDTD 场求解 | Maxwell FDTD / PML / cleaning | 47-52 | 逐行 | FiniteDifferenceSolver::ComputeCurlA, FiniteDifferenceSolver::ComputeCurlACylindrical, FiniteDifferenceSolver::ComputeCurlASpherical, FiniteDifferenceSolver::ComputeCurlACartesian | 未读 |
| `Source/FieldSolver/FiniteDifferenceSolver/ComputeDivE.cpp` | FDTD 场求解 | Maxwell FDTD / PML / cleaning | 47-52 | 逐行 | FiniteDifferenceSolver::ComputeDivE, FiniteDifferenceSolver::ComputeDivECartesian, FiniteDifferenceSolver::ComputeDivECylindrical, FiniteDifferenceSolver::ComputeDivESpherical | 未读 |
| `Source/FieldSolver/FiniteDifferenceSolver/ComputeGradient.cpp` | FDTD 场求解 | Maxwell FDTD / PML / cleaning | 47-52 | 逐行 | FiniteDifferenceSolver::ComputeGradient, FiniteDifferenceSolver::ComputeGradientCylindrical, FiniteDifferenceSolver::ComputeGradientSpherical, FiniteDifferenceSolver::ComputeGradientCartesian | 未读 |
| `Source/FieldSolver/FiniteDifferenceSolver/ComputeLaplacian.cpp` | FDTD 场求解 | Maxwell FDTD / PML / cleaning | 47-52 | 逐行 | FiniteDifferenceSolver::ComputeLaplacian, FiniteDifferenceSolver::ComputeLaplacianCylindrical, FiniteDifferenceSolver::ComputeLaplacianSpherical, FiniteDifferenceSolver::ComputeLaplacianCartesian, FiniteDifferenceSolver::ComputeVectorLaplacian, FiniteDifferenceSolver::ComputeVectorLaplacianCylindrical, FiniteDifferenceSolver::ComputeVectorLaplacianSpherical, FiniteDifferenceSolver::ComputeVectorLaplacianCartesian | 未读 |
| `Source/FieldSolver/FiniteDifferenceSolver/EvolveB.cpp` | FDTD 场求解 | Maxwell FDTD / PML / cleaning | 47-52 | 逐行 | FiniteDifferenceSolver::EvolveB, FiniteDifferenceSolver::EvolveBCartesian, FiniteDifferenceSolver::EvolveBCartesianECT, FiniteDifferenceSolver::EvolveBCylindrical, FiniteDifferenceSolver::EvolveBSpherical | 未读 |
| `Source/FieldSolver/FiniteDifferenceSolver/EvolveBPML.cpp` | FDTD 场求解 | Maxwell FDTD / PML / cleaning | 47-52 | 逐行 | FiniteDifferenceSolver::EvolveBPML, FiniteDifferenceSolver::EvolveBPMLCartesian | 未读 |
| `Source/FieldSolver/FiniteDifferenceSolver/EvolveE.cpp` | FDTD 场求解 | Maxwell FDTD / PML / cleaning | 47-52 | 逐行 | FiniteDifferenceSolver::EvolveE, FiniteDifferenceSolver::EvolveECartesian, FiniteDifferenceSolver::EvolveECylindrical, Br, FiniteDifferenceSolver::EvolveESpherical | 未读 |
| `Source/FieldSolver/FiniteDifferenceSolver/EvolveECTRho.cpp` | FDTD 场求解 | Maxwell FDTD / PML / cleaning | 47-52 | 逐行 | FiniteDifferenceSolver::EvolveECTRho, FiniteDifferenceSolver::EvolveRhoCartesianECT | 未读 |
| `Source/FieldSolver/FiniteDifferenceSolver/EvolveEPML.cpp` | FDTD 场求解 | Maxwell FDTD / PML / cleaning | 47-52 | 逐行 | FiniteDifferenceSolver::EvolveEPML, FiniteDifferenceSolver::EvolveEPMLCartesian | 未读 |
| `Source/FieldSolver/FiniteDifferenceSolver/EvolveF.cpp` | FDTD 场求解 | Maxwell FDTD / PML / cleaning | 47-52 | 逐行 | FiniteDifferenceSolver::EvolveF, FiniteDifferenceSolver::EvolveFCartesian, FiniteDifferenceSolver::EvolveFCylindrical, FiniteDifferenceSolver::EvolveFSpherical | 未读 |
| `Source/FieldSolver/FiniteDifferenceSolver/EvolveFPML.cpp` | FDTD 场求解 | Maxwell FDTD / PML / cleaning | 47-52 | 逐行 | FiniteDifferenceSolver::EvolveFPML, FiniteDifferenceSolver::EvolveFPMLCartesian | 未读 |
| `Source/FieldSolver/FiniteDifferenceSolver/EvolveG.cpp` | FDTD 场求解 | Maxwell FDTD / PML / cleaning | 47-52 | 逐行 | FiniteDifferenceSolver::EvolveG, FiniteDifferenceSolver::EvolveGCartesian | 未读 |
| `Source/FieldSolver/FiniteDifferenceSolver/FiniteDifferenceAlgorithms/CartesianCKCAlgorithm.H` | FDTD 算法模板 | Yee / CKC / nodal / cylindrical / spherical | 50 | 逐行 | contains, CartesianCKCAlgorithm, InitializeStencilCoefficients, ComputeMaxDt, GetMaxGuardCell, UpwardDx, DownwardDx, UpwardDy | 未读 |
| `Source/FieldSolver/FiniteDifferenceSolver/FiniteDifferenceAlgorithms/CartesianNodalAlgorithm.H` | FDTD 算法模板 | Yee / CKC / nodal / cylindrical / spherical | 50 | 逐行 | contains, CartesianNodalAlgorithm, InitializeStencilCoefficients, ComputeMaxDt, GetMaxGuardCell, UpwardDx, DownwardDx, Dxx | 未读 |
| `Source/FieldSolver/FiniteDifferenceSolver/FiniteDifferenceAlgorithms/CartesianYeeAlgorithm.H` | FDTD 算法模板 | Yee / CKC / nodal / cylindrical / spherical | 50 | 逐行 | contains, CartesianYeeAlgorithm, InitializeStencilCoefficients, ComputeMaxDt, GetMaxGuardCell, UpwardDx, DownwardDx, Dxx | 未读 |
| `Source/FieldSolver/FiniteDifferenceSolver/FiniteDifferenceAlgorithms/CylindricalYeeAlgorithm.H` | FDTD 算法模板 | Yee / CKC / nodal / cylindrical / spherical | 50 | 逐行 | contains, CylindricalYeeAlgorithm, InitializeStencilCoefficients, ComputeMaxDt, GetMaxGuardCell, UpwardDrr_over_r, DownwardDrr_over_r, UpwardDr | 未读 |
| `Source/FieldSolver/FiniteDifferenceSolver/FiniteDifferenceAlgorithms/FieldAccessorFunctors.H` | FDTD 算法模板 | Yee / CKC / nodal / cylindrical / spherical | 50 | 逐行 | FieldAccessorMacroscopic, respective | 未读 |
| `Source/FieldSolver/FiniteDifferenceSolver/FiniteDifferenceAlgorithms/SphericalYeeAlgorithm.H` | FDTD 算法模板 | Yee / CKC / nodal / cylindrical / spherical | 50 | 逐行 | contains, SphericalYeeAlgorithm, InitializeStencilCoefficients, ComputeMaxDt, GetMaxGuardCell, UpwardDrr_over_r, DownwardDrr2_over_r2, DownwardDrr_over_r | 未读 |
| `Source/FieldSolver/FiniteDifferenceSolver/FiniteDifferenceSolver.H` | FDTD 场求解 | Maxwell FDTD / PML / cleaning | 47-52 | 逐行 | FiniteDifferenceSolver | 未读 |
| `Source/FieldSolver/FiniteDifferenceSolver/FiniteDifferenceSolver.cpp` | FDTD 场求解 | Maxwell FDTD / PML / cleaning | 47-52 | 逐行 |  | 未读 |
| `Source/FieldSolver/FiniteDifferenceSolver/FiniteDifferenceSolver_fwd.H` | FDTD 场求解 | Maxwell FDTD / PML / cleaning | 47-52 | 逐行 | FiniteDifferenceSolver | 未读 |
| `Source/FieldSolver/FiniteDifferenceSolver/HybridPICModel/CMakeLists.txt` | Hybrid PIC 场求解 | Ohm 定律 / kinetic ion + fluid electron | 61, 104 | 逐行 |  | 未读 |
| `Source/FieldSolver/FiniteDifferenceSolver/HybridPICModel/ExternalVectorPotential.H` | Hybrid PIC 场求解 | Ohm 定律 / kinetic ion + fluid electron | 61, 104 | 逐行 | contains, is, ExternalVectorPotential | 未读 |
| `Source/FieldSolver/FiniteDifferenceSolver/HybridPICModel/ExternalVectorPotential.cpp` | Hybrid PIC 场求解 | Ohm 定律 / kinetic ion + fluid electron | 61, 104 | 逐行 | ExternalVectorPotential::ReadParameters, ExternalVectorPotential::AllocateLevelMFs, ExternalVectorPotential::InitData, ExternalVectorPotential::CalculateExternalCurlA, ExternalVectorPotential::AddExternalFieldFromVectorPotential, ExternalVectorPotential::UpdateHybridExternalFields | 未读 |
| `Source/FieldSolver/FiniteDifferenceSolver/HybridPICModel/HybridPICModel.H` | Hybrid PIC 场求解 | Ohm 定律 / kinetic ion + fluid electron | 61, 104 | 逐行 | contains, HybridPICModel, ElectronPressure, get_pressure | 未读 |
| `Source/FieldSolver/FiniteDifferenceSolver/HybridPICModel/HybridPICModel.cpp` | Hybrid PIC 场求解 | Ohm 定律 / kinetic ion + fluid electron | 61, 104 | 逐行 | HybridPICModel::ReadParameters, HybridPICModel::InitData, HybridPICModel::GetCurrentExternal, rho, HybridPICModel::BfieldEvolveRK, HybridPICModel::FieldPush | 未读 |
| `Source/FieldSolver/FiniteDifferenceSolver/HybridPICModel/HybridPICModel_fwd.H` | Hybrid PIC 场求解 | Ohm 定律 / kinetic ion + fluid electron | 61, 104 | 逐行 | HybridPICModel | 未读 |
| `Source/FieldSolver/FiniteDifferenceSolver/HybridPICModel/Make.package` | Hybrid PIC 场求解 | Ohm 定律 / kinetic ion + fluid electron | 61, 104 | 逐行 |  | 未读 |
| `Source/FieldSolver/FiniteDifferenceSolver/HybridPICSolveE.cpp` | FDTD 场求解 | Maxwell FDTD / PML / cleaning | 47-52 | 逐行 | FiniteDifferenceSolver::CalculateCurrentAmpere, FiniteDifferenceSolver::CalculateCurrentAmpereCylindrical, Br, FiniteDifferenceSolver::CalculateCurrentAmpereSpherical, FiniteDifferenceSolver::CalculateCurrentAmpereCartesian, FiniteDifferenceSolver::HybridPICSolveE, FiniteDifferenceSolver::HybridPICSolveECylindrical, FiniteDifferenceSolver::HybridPICSolveESpherical | 未读 |
| `Source/FieldSolver/FiniteDifferenceSolver/MacroscopicEvolveE.cpp` | FDTD 场求解 | Maxwell FDTD / PML / cleaning | 47-52 | 逐行 | FiniteDifferenceSolver::MacroscopicEvolveE, FiniteDifferenceSolver::MacroscopicEvolveECartesian | 未读 |
| `Source/FieldSolver/FiniteDifferenceSolver/MacroscopicProperties/CMakeLists.txt` | 宏观介质 | conductivity / epsilon / mu response | 51 | 逐块 |  | 未读 |
| `Source/FieldSolver/FiniteDifferenceSolver/MacroscopicProperties/MacroscopicProperties.H` | 宏观介质 | conductivity / epsilon / mu response | 51 | 逐块 | contains, MacroscopicProperties, LaxWendroffAlgo, BackwardEulerAlgo, getsigma_mf, getepsilon_mf, getmu_mf, alpha | 未读 |
| `Source/FieldSolver/FiniteDifferenceSolver/MacroscopicProperties/MacroscopicProperties.cpp` | 宏观介质 | conductivity / epsilon / mu response | 51 | 逐块 | MacroscopicProperties::ReadParameters, MacroscopicProperties::AllocateLevelMFs, MacroscopicProperties::InitData, MacroscopicProperties::InitializeMacroMultiFabUsingParser | 未读 |
| `Source/FieldSolver/FiniteDifferenceSolver/MacroscopicProperties/MacroscopicProperties_fwd.H` | 宏观介质 | conductivity / epsilon / mu response | 51 | 逐块 | MacroscopicProperties | 未读 |
| `Source/FieldSolver/FiniteDifferenceSolver/MacroscopicProperties/Make.package` | 宏观介质 | conductivity / epsilon / mu response | 51 | 逐块 |  | 未读 |
| `Source/FieldSolver/FiniteDifferenceSolver/Make.package` | FDTD 场求解 | Maxwell FDTD / PML / cleaning | 47-52 | 逐行 |  | 未读 |
| `Source/FieldSolver/ImplicitSolvers/CMakeLists.txt` | 隐式求解 | theta/semi implicit / JFNK / Picard | 59 | 逐块 |  | 未读 |
| `Source/FieldSolver/ImplicitSolvers/ImplicitOptions.H` | 隐式求解 | theta/semi implicit / JFNK / Picard | 59 | 逐块 | ImplicitOptions | 未读 |
| `Source/FieldSolver/ImplicitSolvers/ImplicitSolver.H` | 隐式求解 | theta/semi implicit / JFNK / Picard | 59 | 逐块 | WarpX, class, ImplicitSolver, GetMassMatricesPCnComp | 未读 |
| `Source/FieldSolver/ImplicitSolvers/ImplicitSolver.cpp` | 隐式求解 | theta/semi implicit / JFNK / Picard | 59 | 逐块 | ImplicitSolver::CumulateJ, ImplicitSolver::SaveE, ImplicitSolver::ComputeJfromMassMatrices, ImplicitSolver::parseNonlinearSolverParams, ImplicitSolver::SaveEoldMultifab, ImplicitSolver::InitializeMassMatrices, ImplicitSolver::PreLinearSolve, ImplicitSolver::PreRHSOp | 未读 |
| `Source/FieldSolver/ImplicitSolvers/ImplicitSolverLibrary.H` | 隐式求解 | theta/semi implicit / JFNK / Picard | 59 | 逐块 |  | 未读 |
| `Source/FieldSolver/ImplicitSolvers/ImplicitSolver_fwd.H` | 隐式求解 | theta/semi implicit / JFNK / Picard | 59 | 逐块 | ImplicitSolver | 未读 |
| `Source/FieldSolver/ImplicitSolvers/Make.package` | 隐式求解 | theta/semi implicit / JFNK / Picard | 59 | 逐块 |  | 未读 |
| `Source/FieldSolver/ImplicitSolvers/SemiImplicitEM.H` | 隐式求解 | theta/semi implicit / JFNK / Picard | 59 | 逐块 | SemiImplicitEM | 未读 |
| `Source/FieldSolver/ImplicitSolvers/SemiImplicitEM.cpp` | 隐式求解 | theta/semi implicit / JFNK / Picard | 59 | 逐块 | m_WarpX, SemiImplicitEM::Define, SemiImplicitEM::PrintParameters, SemiImplicitEM::OneStep, SemiImplicitEM::ComputeRHS | 未读 |
| `Source/FieldSolver/ImplicitSolvers/StrangImplicitSpectralEM.H` | 隐式求解 | theta/semi implicit / JFNK / Picard | 59 | 逐块 | StrangImplicitSpectralEM | 未读 |
| `Source/FieldSolver/ImplicitSolvers/StrangImplicitSpectralEM.cpp` | 隐式求解 | theta/semi implicit / JFNK / Picard | 59 | 逐块 | m_WarpX, StrangImplicitSpectralEM::Define, StrangImplicitSpectralEM::PrintParameters, StrangImplicitSpectralEM::OneStep, StrangImplicitSpectralEM::ComputeRHS, StrangImplicitSpectralEM::UpdateWarpXFields, StrangImplicitSpectralEM::FinishFieldUpdate | 未读 |
| `Source/FieldSolver/ImplicitSolvers/ThetaImplicitEM.H` | 隐式求解 | theta/semi implicit / JFNK / Picard | 59 | 逐块 | ThetaImplicitEM | 未读 |
| `Source/FieldSolver/ImplicitSolvers/ThetaImplicitEM.cpp` | 隐式求解 | theta/semi implicit / JFNK / Picard | 59 | 逐块 | m_WarpX, ThetaImplicitEM::Define, ThetaImplicitEM::OneStep, ThetaImplicitEM::ComputeRHS, ThetaImplicitEM::UpdateWarpXFields, ThetaImplicitEM::FinishFieldUpdate, ThetaImplicitEM::InitializeCurlCurlBCMasks | 未读 |
| `Source/FieldSolver/ImplicitSolvers/WarpXImplicitOps.cpp` | 隐式求解 | theta/semi implicit / JFNK / Picard | 59 | 逐块 | WarpX::SetElectricFieldAndApplyBCs, WarpX::UpdateMagneticFieldAndApplyBCs, WarpX::FinishMagneticFieldAndApplyBCs, WarpX::SpectralSourceFreeFieldAdvance, WarpX::SaveParticlesAtImplicitStepStart, WarpX::FinishImplicitParticleUpdate, WarpX::FinishImplicitField, WarpX::DepositMassMatrices | 未读 |
| `Source/FieldSolver/ImplicitSolvers/WarpXSolverDOF.H` | 隐式求解 | theta/semi implicit / JFNK / Picard | 59 | 逐块 | WarpX, WarpXSolverDOF | 未读 |
| `Source/FieldSolver/ImplicitSolvers/WarpXSolverDOF.cpp` | 隐式求解 | theta/semi implicit / JFNK / Picard | 59 | 逐块 | WarpXSolverDOF::Define, WarpXSolverDOF::fill_local_dof, WarpXSolverDOF::fill_global_dof | 未读 |
| `Source/FieldSolver/ImplicitSolvers/WarpXSolverVec.H` | 隐式求解 | theta/semi implicit / JFNK / Picard | 59 | 逐块 | WarpX, around, WarpXSolverVec, Define, Copy, linComb, increment, scale | 未读 |
| `Source/FieldSolver/ImplicitSolvers/WarpXSolverVec.cpp` | 隐式求解 | theta/semi implicit / JFNK / Picard | 59 | 逐块 | WarpXSolverVec::Define, WarpXSolverVec::Copy, WarpXSolverVec::copyFrom | 未读 |
| `Source/FieldSolver/MagnetostaticSolver/CMakeLists.txt` | 磁静态求解 | vector potential / magnetostatic fields | 58 | 逐块 |  | 未读 |
| `Source/FieldSolver/MagnetostaticSolver/MagnetostaticSolver.H` | 磁静态求解 | vector potential / magnetostatic fields | 58 | 逐块 | VectorPoissonBoundaryHandler, EBCalcBfromVectorPotentialPerLevel | 未读 |
| `Source/FieldSolver/MagnetostaticSolver/MagnetostaticSolver.cpp` | 磁静态求解 | vector potential / magnetostatic fields | 58 | 逐块 | WarpX::ComputeMagnetostaticField, WarpX::AddMagnetostaticFieldLabFrame, post_A_calculation, MagnetostaticSolver::VectorPoissonBoundaryHandler::defineVectorPotentialBCs, MagnetostaticSolver::EBCalcBfromVectorPotentialPerLevel::doInterp, MagnetostaticSolver::EBCalcBfromVectorPotentialPerLevel::operator | 未读 |
| `Source/FieldSolver/MagnetostaticSolver/Make.package` | 磁静态求解 | vector potential / magnetostatic fields | 58 | 逐块 |  | 未读 |
| `Source/FieldSolver/Make.package` | 场求解 | EM/ES/hybrid/implicit/QED field push | 46-62 | 逐块 |  | 未读 |
| `Source/FieldSolver/SpectralSolver/CMakeLists.txt` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 |  | 未读 |
| `Source/FieldSolver/SpectralSolver/Make.package` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 |  | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralAlgorithms/CMakeLists.txt` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 |  | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralAlgorithms/Make.package` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 |  | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralAlgorithms/PsatdAlgorithmComoving.H` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 | PsatdAlgorithmComoving | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralAlgorithms/PsatdAlgorithmComoving.cpp` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 | PsatdAlgorithmComoving::InitializeSpectralCoefficients, PsatdAlgorithmComoving::CurrentCorrection, PsatdAlgorithmComoving::VayDeposition | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralAlgorithms/PsatdAlgorithmGalilean.H` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 | PsatdAlgorithmGalilean | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralAlgorithms/PsatdAlgorithmGalilean.cpp` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 | PsatdAlgorithmGalilean::InitializeSpectralCoefficients, PsatdAlgorithmGalilean::InitializeSpectralCoefficientsAveraging, PsatdAlgorithmGalilean::CurrentCorrection, PsatdAlgorithmGalilean::VayDeposition | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralAlgorithms/PsatdAlgorithmGalileanRZ.H` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 | PsatdAlgorithmGalileanRZ, void | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralAlgorithms/PsatdAlgorithmGalileanRZ.cpp` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 | SpectralBaseAlgorithmRZ, PsatdAlgorithmGalileanRZ::pushSpectralFields, PsatdAlgorithmGalileanRZ::InitializeSpectralCoefficients, PsatdAlgorithmGalileanRZ::CurrentCorrection, PsatdAlgorithmGalileanRZ::VayDeposition | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralAlgorithms/PsatdAlgorithmJRhomFirstOrder.H` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 | PsatdAlgorithmJRhomFirstOrder | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralAlgorithms/PsatdAlgorithmJRhomFirstOrder.cpp` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 | PsatdAlgorithmJRhomFirstOrder::CurrentCorrection, PsatdAlgorithmJRhomFirstOrder::VayDeposition | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralAlgorithms/PsatdAlgorithmJRhomSecondOrder.H` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 | PsatdAlgorithmJRhomSecondOrder | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralAlgorithms/PsatdAlgorithmJRhomSecondOrder.cpp` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 | PsatdAlgorithmJRhomSecondOrder::InitializeSpectralCoefficients, PsatdAlgorithmJRhomSecondOrder::InitializeSpectralCoefficientsAveraging, PsatdAlgorithmJRhomSecondOrder::CurrentCorrection, PsatdAlgorithmJRhomSecondOrder::VayDeposition | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralAlgorithms/PsatdAlgorithmPml.H` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 | PsatdAlgorithmPml | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralAlgorithms/PsatdAlgorithmPml.cpp` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 | PsatdAlgorithmPml::InitializeSpectralCoefficients, PsatdAlgorithmPml::CurrentCorrection, PsatdAlgorithmPml::VayDeposition | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralAlgorithms/PsatdAlgorithmPmlRZ.H` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 | PsatdAlgorithmPmlRZ, void | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralAlgorithms/PsatdAlgorithmPmlRZ.cpp` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 | and, PsatdAlgorithmPmlRZ::pushSpectralFields, PsatdAlgorithmPmlRZ::InitializeSpectralCoefficients, PsatdAlgorithmPmlRZ::CurrentCorrection, PsatdAlgorithmPmlRZ::VayDeposition | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralAlgorithms/PsatdAlgorithmRZ.H` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 | PsatdAlgorithmRZ, void | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralAlgorithms/PsatdAlgorithmRZ.cpp` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 | and, PsatdAlgorithmRZ::pushSpectralFields, PsatdAlgorithmRZ::InitializeSpectralCoefficients, PsatdAlgorithmRZ::CurrentCorrection, PsatdAlgorithmRZ::VayDeposition | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralAlgorithms/SpectralBaseAlgorithm.H` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 | and, SpectralBaseAlgorithm | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralAlgorithms/SpectralBaseAlgorithm.cpp` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 | SpectralBaseAlgorithm::ComputeSpectralDivE | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralAlgorithms/SpectralBaseAlgorithmRZ.H` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 | and, SpectralBaseAlgorithmRZ | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralAlgorithms/SpectralBaseAlgorithmRZ.cpp` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 | SpectralBaseAlgorithmRZ::ComputeSpectralDivE | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralBinomialFilter.H` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 | SpectralBinomialFilter, getFilterArrayR, getFilterArrayZ | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralBinomialFilter.cpp` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 | SpectralBinomialFilter::InitFilterArray | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralFieldData.H` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 | SpectralFieldIndex, SpectralFieldData | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralFieldData.cpp` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 | SpectralFieldData::ForwardTransform, SpectralFieldData::BackwardTransform | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralFieldDataRZ.H` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 | SpectralFieldDataRZ | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralFieldDataRZ.cpp` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 | SpectralFieldDataRZ::FABZForwardTransform, SpectralFieldDataRZ::FABZBackwardTransform, SpectralFieldDataRZ::ForwardTransform, SpectralFieldDataRZ::BackwardTransform, SpectralFieldDataRZ::CopySpectralDataComp, SpectralFieldDataRZ::ZeroOutDataComp, SpectralFieldDataRZ::ScaleDataComp, SpectralFieldDataRZ::InitFilter | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralFieldData_fwd.H` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 | SpectralFieldIndex, SpectralFieldData | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralHankelTransform/BesselRoots.H` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 |  | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralHankelTransform/BesselRoots.cpp` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 | SecantRootFinder, GetBesselRoots | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralHankelTransform/CMakeLists.txt` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 |  | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralHankelTransform/HankelTransform.H` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 | that, HankelTransform, getSpectralWavenumbers | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralHankelTransform/HankelTransform.cpp` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 | HankelTransform::HankelForwardTransform, HankelTransform::HankelInverseTransform | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralHankelTransform/Make.package` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 |  | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralHankelTransform/SpectralHankelTransformer.H` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 | SpectralHankelTransformer | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralHankelTransform/SpectralHankelTransformer.cpp` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 | SpectralHankelTransformer::ExtractKrArray, SpectralHankelTransformer::PhysicalToSpectral_Scalar, SpectralHankelTransformer::PhysicalToSpectral_Vector, SpectralHankelTransformer::SpectralToPhysical_Scalar, SpectralHankelTransformer::SpectralToPhysical_Vector | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralKSpace.H` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 | SpectralKSpace | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralKSpace.cpp` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 |  | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralKSpaceRZ.H` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 | SpectralKSpaceRZ | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralKSpaceRZ.cpp` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 |  | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralKSpace_fwd.H` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 | class, SpectralKSpace | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralSolver.H` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 | SpectralSolver, SpectralBaseAlgorithm, defining | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralSolver.cpp` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 | of, SpectralSolver::ForwardTransform, SpectralSolver::BackwardTransform, SpectralSolver::pushSpectralFields, SpectralSolver::ComputeSpectralDivE, SpectralSolver::CurrentCorrection, SpectralSolver::VayDeposition, SpectralSolver::CopySpectralDataComp | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralSolverRZ.H` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 | SpectralSolverRZ, SpectralBaseAlgorithmRZ | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralSolverRZ.cpp` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 | of, SpectralBaseAlgorithmRZ, SpectralSolverRZ, SpectralSolverRZ::ForwardTransform, SpectralSolverRZ::BackwardTransform, SpectralSolverRZ::pushSpectralFields, SpectralSolverRZ::InitFilter, SpectralSolverRZ::ApplyFilter | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralSolverRZ_fwd.H` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 | SpectralSolverRZ | 未读 |
| `Source/FieldSolver/SpectralSolver/SpectralSolver_fwd.H` | 谱场求解 | PSATD / Galilean / Hankel / FFT | 53-56 | 逐行 | SpectralSolver | 未读 |
| `Source/FieldSolver/WarpXPushFieldsEM.cpp` | 场求解 | EM/ES/hybrid/implicit/QED field push | 46-62 | 逐块 | ForwardTransformVect, BackwardTransformVect, PSATDCurrentCorrection, PSATDVayDeposition, PSATDSubtractCurrentPartialSumsAvg, WarpX::PSATDForwardTransformEB, WarpX::PSATDBackwardTransformEB, WarpX::PSATDBackwardTransformEBavg | 未读 |
| `Source/FieldSolver/WarpXPushFieldsEM_K.H` | 场求解 | EM/ES/hybrid/implicit/QED field push | 46-62 | 逐块 | constrain_tilebox_to_guards, damp_field_in_guards | 未读 |
| `Source/FieldSolver/WarpXPushFieldsHybridPIC.cpp` | 场求解 | EM/ES/hybrid/implicit/QED field push | 46-62 | 逐块 | WarpX::HybridPICEvolveFields, WarpX::HybridPICDepositRhoAndJ, WarpX::HybridPICInitializeRhoJandB, WarpX::CalculateExternalCurlA | 未读 |
| `Source/FieldSolver/WarpXSolveFieldsES.cpp` | 场求解 | EM/ES/hybrid/implicit/QED field push | 46-62 | 逐块 | WarpX::ComputeSpaceChargeField | 未读 |
| `Source/FieldSolver/WarpX_FDTD.H` | 场求解 | EM/ES/hybrid/implicit/QED field push | 46-62 | 逐块 | warpx_computedivb | 未读 |
| `Source/FieldSolver/WarpX_QED_Field_Pushers.cpp` | 场求解 | EM/ES/hybrid/implicit/QED field push | 46-62 | 逐块 | WarpX::Hybrid_QED_Push | 未读 |
| `Source/FieldSolver/WarpX_QED_K.H` | 场求解 | EM/ES/hybrid/implicit/QED field push | 46-62 | 逐块 | calc_M, warpx_hybrid_QED_push | 未读 |
| `Source/Fields.H` | WarpX 主类 | field registry / centering / MultiFab 命名体系 | 11 | 逐块 | isFieldArray, FieldType, Direction, IndexType, PatchType | 已入正文 |
| `Source/Filter/BilinearFilter.H` | 滤波器 | bilinear / NCI Godfrey filter | 45, 53-56 | 逐块 | BilinearFilter | 未读 |
| `Source/Filter/BilinearFilter.cpp` | 滤波器 | bilinear / NCI Godfrey filter | 45, 53-56 | 逐块 | compute_stencil, BilinearFilter::ComputeStencils | 未读 |
| `Source/Filter/CMakeLists.txt` | 滤波器 | bilinear / NCI Godfrey filter | 45, 53-56 | 逐块 |  | 未读 |
| `Source/Filter/Filter.H` | 滤波器 | bilinear / NCI Godfrey filter | 45, 53-56 | 逐块 | Filter | 未读 |
| `Source/Filter/Filter.cpp` | 滤波器 | bilinear / NCI Godfrey filter | 45, 53-56 | 逐块 | Filter::ApplyStencil, Filter::DoFilter | 未读 |
| `Source/Filter/Make.package` | 滤波器 | bilinear / NCI Godfrey filter | 45, 53-56 | 逐块 |  | 未读 |
| `Source/Filter/NCIGodfreyFilter.H` | 滤波器 | bilinear / NCI Godfrey filter | 45, 53-56 | 逐块 | class, Filter, NCIGodfreyFilter | 未读 |
| `Source/Filter/NCIGodfreyFilter.cpp` | 滤波器 | bilinear / NCI Godfrey filter | 45, 53-56 | 逐块 | data, NCIGodfreyFilter::ComputeStencils | 未读 |
| `Source/Filter/NCIGodfreyFilter_fwd.H` | 滤波器 | bilinear / NCI Godfrey filter | 45, 53-56 | 逐块 | class, NCIGodfreyFilter | 未读 |
| `Source/Fluids/CMakeLists.txt` | 流体模型 | cold fluid / MUSCL-Hancock / hybrid coupling | 101-104 | 逐块 |  | 未读 |
| `Source/Fluids/Make.package` | 流体模型 | cold fluid / MUSCL-Hancock / hybrid coupling | 101-104 | 逐块 |  | 未读 |
| `Source/Fluids/MultiFluidContainer.H` | 流体模型 | cold fluid / MUSCL-Hancock / hybrid coupling | 101-104 | 逐块 | MultiFluidContainer, WarpXFluidContainer, WarpX, GetUniqueContainer | 未读 |
| `Source/Fluids/MultiFluidContainer.cpp` | 流体模型 | cold fluid / MUSCL-Hancock / hybrid coupling | 101-104 | 逐块 | MultiFluidContainer::AllocateLevelMFs, MultiFluidContainer::InitData, MultiFluidContainer::DepositCharge, MultiFluidContainer::DepositCurrent, MultiFluidContainer::Evolve | 未读 |
| `Source/Fluids/MultiFluidContainer_fwd.H` | 流体模型 | cold fluid / MUSCL-Hancock / hybrid coupling | 101-104 | 逐块 | MultiFluidContainer | 未读 |
| `Source/Fluids/MusclHancockUtils.H` | 流体模型 | cold fluid / MUSCL-Hancock / hybrid coupling | 101-104 | 逐块 | F_r, F_theta, V_calc, minmod, minmod3, maxmod, flux_N, flux_NUx | 未读 |
| `Source/Fluids/WarpXFluidContainer.H` | 流体模型 | cold fluid / MUSCL-Hancock / hybrid coupling | 101-104 | 逐块 | from, WarpXFluidContainer | 未读 |
| `Source/Fluids/WarpXFluidContainer.cpp` | 流体模型 | cold fluid / MUSCL-Hancock / hybrid coupling | 101-104 | 逐块 | exte_flags, extb_flags, boost_flags, WarpXFluidContainer::ReadParameters, WarpXFluidContainer::InitData, WarpXFluidContainer::Evolve, WarpXFluidContainer::ApplyBcFluidsAndComms, WarpXFluidContainer::AdvectivePush_Muscl | 未读 |
| `Source/Fluids/WarpXFluidContainer_fwd.H` | 流体模型 | cold fluid / MUSCL-Hancock / hybrid coupling | 101-104 | 逐块 | WarpXFluidContainer | 未读 |
| `Source/Initialization/CMakeLists.txt` | 初始化 | geometry / species / profiles / external fields | 80-86 | 逐块 |  | 未读 |
| `Source/Initialization/DivCleaner/CMakeLists.txt` | 散度清理初始化 | projection / div cleaner initialization | 86 | 逐块 |  | 未读 |
| `Source/Initialization/DivCleaner/Make.package` | 散度清理初始化 | projection / div cleaner initialization | 86 | 逐块 |  | 未读 |
| `Source/Initialization/DivCleaner/ProjectionDivCleaner.H` | 散度清理初始化 | projection / div cleaner initialization | 86 | 逐块 | ProjectionDivCleaner, runMLMG | 未读 |
| `Source/Initialization/DivCleaner/ProjectionDivCleaner.cpp` | 散度清理初始化 | projection / div cleaner initialization | 86 | 逐块 | ProjectionDivCleaner::ReadParameters, ProjectionDivCleaner::solve, ProjectionDivCleaner::setSourceFromField, correctFieldCartesian_kernel, ProjectionDivCleaner::correctField, WarpX::ProjectionCleanDivB, constexpr | 未读 |
| `Source/Initialization/ExternalField.H` | 初始化 | geometry / species / profiles / external fields | 80-86 | 逐块 | class, ExternalFieldParams, ExternalFieldView, can, ExternalFieldReader, operator | 未读 |
| `Source/Initialization/ExternalField.cpp` | 初始化 | geometry / species / profiles / external fields | 80-86 | 逐块 | class, string_to_external_field_type, constexpr, ExternalFieldReader::load_data, ExternalFieldReader::prepare, ExternalFieldReader::make_cache_box, ExternalFieldReader::getView | 未读 |
| `Source/Initialization/ExternalField_fwd.H` | 初始化 | geometry / species / profiles / external fields | 80-86 | 逐块 | ExternalFieldParams | 未读 |
| `Source/Initialization/GetTemperature.H` | 初始化 | geometry / species / profiles / external fields | 80-86 | 逐块 | GetTemperature, operator | 未读 |
| `Source/Initialization/GetTemperature.cpp` | 初始化 | geometry / species / profiles / external fields | 80-86 | 逐块 |  | 未读 |
| `Source/Initialization/GetVelocity.H` | 初始化 | geometry / species / profiles / external fields | 80-86 | 逐块 | GetVelocity, operator | 未读 |
| `Source/Initialization/GetVelocity.cpp` | 初始化 | geometry / species / profiles / external fields | 80-86 | 逐块 |  | 未读 |
| `Source/Initialization/InjectorDensity.H` | 初始化 | geometry / species / profiles / external fields | 80-86 | 逐块 | whose, InjectorDensityConstant, InjectorDensityParser, InjectorDensityFromFile, InjectorDensity, struct, InjectorDensityDeleter, getDensity | 未读 |
| `Source/Initialization/InjectorDensity.cpp` | 初始化 | geometry / species / profiles / external fields | 80-86 | 逐块 | InjectorDensity::clear, InjectorDensity::prepare, InjectorDensity::distributed, InjectorDensityFromFile::clear, InjectorDensityFromFile::prepare, InjectorDensityFromFile::distributed | 未读 |
| `Source/Initialization/InjectorFlux.H` | 初始化 | geometry / species / profiles / external fields | 80-86 | 逐块 | whose, InjectorFluxConstant, InjectorFluxParser, InjectorFlux, struct, InjectorFluxDeleter, clear, getFlux | 未读 |
| `Source/Initialization/InjectorMomentum.H` | 初始化 | geometry / species / profiles / external fields | 80-86 | 逐块 | whose, InjectorMomentumConstant, InjectorMomentumGaussian, InjectorMomentumGaussianFlux, InjectorMomentumUniform, InjectorMomentumBoltzmann, InjectorMomentumJuttner, InjectorMomentumParser | 未读 |
| `Source/Initialization/InjectorMomentum.cpp` | 初始化 | geometry / species / profiles / external fields | 80-86 | 逐块 | InjectorMomentum::clear | 未读 |
| `Source/Initialization/InjectorPosition.H` | 初始化 | geometry / species / profiles / external fields | 80-86 | 逐块 | whose, InjectorPositionRandom, InjectorPositionRandomPlane, InjectorPositionRegular, InjectorPosition, struct, getPositionUnitBox, overlapsWith | 未读 |
| `Source/Initialization/InjectorPosition_fwd.H` | 初始化 | geometry / species / profiles / external fields | 80-86 | 逐块 | InjectorPositionRandom, InjectorPositionRegular, InjectorPosition | 未读 |
| `Source/Initialization/Make.package` | 初始化 | geometry / species / profiles / external fields | 80-86 | 逐块 |  | 未读 |
| `Source/Initialization/PlasmaInjector.H` | 初始化 | geometry / species / profiles / external fields | 80-86 | 逐块 | parses, PlasmaInjector | 未读 |
| `Source/Initialization/PlasmaInjector.cpp` | 初始化 | geometry / species / profiles / external fields | 80-86 | 逐块 | PlasmaInjector::setupSingleParticle, PlasmaInjector::setupMultipleParticles, PlasmaInjector::setupGaussianBeam, PlasmaInjector::setupNRandomPerCell, PlasmaInjector::setupNFluxPerCell, PlasmaInjector::setupNuniformPerCell, PlasmaInjector::setupExternalFile, PlasmaInjector::parseFlux | 未读 |
| `Source/Initialization/SampleGaussianFluxDistribution.H` | 初始化 | geometry / species / profiles / external fields | 80-86 | 逐块 | generateGaussianFluxDist | 未读 |
| `Source/Initialization/TemperatureProperties.H` | 初始化 | geometry / species / profiles / external fields | 80-86 | 逐块 | TemperatureInitType, TemperatureProperties | 未读 |
| `Source/Initialization/TemperatureProperties.cpp` | 初始化 | geometry / species / profiles / external fields | 80-86 | 逐块 |  | 未读 |
| `Source/Initialization/VelocityProperties.H` | 初始化 | geometry / species / profiles / external fields | 80-86 | 逐块 | VelocityInitType, VelocityProperties | 未读 |
| `Source/Initialization/VelocityProperties.cpp` | 初始化 | geometry / species / profiles / external fields | 80-86 | 逐块 |  | 未读 |
| `Source/Initialization/WarpXAMReXInit.H` | 初始化 | geometry / species / profiles / external fields | 80-86 | 逐块 |  | 未读 |
| `Source/Initialization/WarpXAMReXInit.cpp` | 初始化 | geometry / species / profiles / external fields | 80-86 | 逐块 | override_default_abort_on_out_of_gpu_memory, override_default_the_arena_is_managed, override_default_omp_threads, set_device_synchronization, apply_workaround_for_warpx_numprocs, override_default_tiling_option_for_particles, set_periodicity_according_to_boundary_types, add_constants | 未读 |
| `Source/Initialization/WarpXInit.H` | 初始化 | geometry / species / profiles / external fields | 80-86 | 逐块 |  | 未读 |
| `Source/Initialization/WarpXInit.cpp` | 初始化 | geometry / species / profiles / external fields | 80-86 | 逐块 | warpx::initialization::initialize_external_libraries, warpx::initialization::finalize_external_libraries, warpx::initialization::initialize_warning_manager, warpx::initialization::check_dims, warpx::initialization::read_moving_window_parameters | 未读 |
| `Source/Initialization/WarpXInitData.cpp` | 初始化 | geometry / species / profiles / external fields | 80-86 | 逐块 | get_nppc, PrintDtDxDyDz, CheckGuardCells, PerformanceHints, CheckKnownEMSolverIssues, WriteUsedInputsFile, WarpX::PostProcessBaseGrids, WarpX::PrintMainPICparameters | 未读 |
| `Source/Laser/CMakeLists.txt` | 激光 | laser profiles / antenna / file input | 87-88 | 逐块 |  | 未读 |
| `Source/Laser/LaserProfiles.H` | 激光 | laser profiles / antenna / file input | 87-88 | 逐块 | CommonLaserParameters, should, ILaserProfile, GaussianLaserProfile, FieldFunctionLaserProfile, FromFileLaserProfile | 未读 |
| `Source/Laser/LaserProfilesImpl/CMakeLists.txt` | 激光 | laser profiles / antenna / file input | 87-88 | 逐块 |  | 未读 |
| `Source/Laser/LaserProfilesImpl/LaserProfileFieldFunction.cpp` | 激光 | laser profiles / antenna / file input | 87-88 | 逐块 | WarpXLaserProfiles::FieldFunctionLaserProfile::init | 未读 |
| `Source/Laser/LaserProfilesImpl/LaserProfileFromFile.cpp` | 激光 | laser profiles / antenna / file input | 87-88 | 逐块 | WarpXLaserProfiles::FromFileLaserProfile::init, WarpXLaserProfiles::FromFileLaserProfile::update, WarpXLaserProfiles::FromFileLaserProfile::parse_lasy_file, WarpXLaserProfiles::FromFileLaserProfile::parse_binary_file, WarpXLaserProfiles::FromFileLaserProfile::read_data_t_chunk, WarpXLaserProfiles::FromFileLaserProfile::read_binary_data_t_chunk | 未读 |
| `Source/Laser/LaserProfilesImpl/LaserProfileGaussian.cpp` | 激光 | laser profiles / antenna / file input | 87-88 | 逐块 | WarpXLaserProfiles::GaussianLaserProfile::init | 未读 |
| `Source/Laser/LaserProfilesImpl/Make.package` | 激光 | laser profiles / antenna / file input | 87-88 | 逐块 |  | 未读 |
| `Source/Laser/Make.package` | 激光 | laser profiles / antenna / file input | 87-88 | 逐块 |  | 未读 |
| `Source/Make.WarpX` | 构建系统 | GNUmake 根层聚合 / feature macros / 维度变体 | 0 | 逐块 | DIM, USE_RZ, USE_FFT, USE_PYTHON_MAIN, QED, USERSuffix | 已做笔记 |
| `Source/Make.package` | 构建系统 | 根层源文件入口 / GNUmake 聚合起点 | 0 | 逐块 | WARPX_cpp, WARPX_H, CEXE_sources, CEXE_headers | 已做笔记 |
| `Source/NonlinearSolvers/AMReXGMRES_Wrapper.H` | 非线性/线性求解器 | Newton/Picard/GMRES/PETSc/preconditioner | 59-60 | 逐块 | is, Vec, Ops, must, AMReXGMRES | 未读 |
| `Source/NonlinearSolvers/CMakeLists.txt` | 非线性/线性求解器 | Newton/Picard/GMRES/PETSc/preconditioner | 59-60 | 逐块 |  | 未读 |
| `Source/NonlinearSolvers/CurlCurlMLMGPC.H` | 非线性/线性求解器 | Newton/Picard/GMRES/PETSc/preconditioner | 59-60 | 逐块 | is, T, Ops, must, CurlCurlMLMGPC | 未读 |
| `Source/NonlinearSolvers/JacobiPC.H` | 非线性/线性求解器 | Newton/Picard/GMRES/PETSc/preconditioner | 59-60 | 逐块 | T, Ops, JacobiPC | 未读 |
| `Source/NonlinearSolvers/JacobianFunctionMF.H` | 非线性/线性求解器 | Newton/Picard/GMRES/PETSc/preconditioner | 59-60 | 逐块 | has, T, Ops, JacobianFunctionMF, precond, updatePreCondMat, setBaseSolution, setBaseRHS | 未读 |
| `Source/NonlinearSolvers/LinearFunction.H` | 非线性/线性求解器 | Newton/Picard/GMRES/PETSc/preconditioner | 59-60 | 逐块 | T, Ops, LinearFunction, create, assign, increment, scale, linComb | 未读 |
| `Source/NonlinearSolvers/LinearSolver.H` | 非线性/线性求解器 | Newton/Picard/GMRES/PETSc/preconditioner | 59-60 | 逐块 | is, Vec, Ops, must, LinearSolver, setRestartLength | 未读 |
| `Source/NonlinearSolvers/LinearSolverLibrary.H` | 非线性/线性求解器 | Newton/Picard/GMRES/PETSc/preconditioner | 59-60 | 逐块 | to | 未读 |
| `Source/NonlinearSolvers/Make.package` | 非线性/线性求解器 | Newton/Picard/GMRES/PETSc/preconditioner | 59-60 | 逐块 |  | 未读 |
| `Source/NonlinearSolvers/MatrixPC.H` | 非线性/线性求解器 | Newton/Picard/GMRES/PETSc/preconditioner | 59-60 | 逐块 | is, T, Ops, must, MatrixPC, insertOrAdd | 未读 |
| `Source/NonlinearSolvers/NewtonSolver.H` | 非线性/线性求解器 | Newton/Picard/GMRES/PETSc/preconditioner | 59-60 | 逐块 | Vec, Ops, NewtonSolver | 未读 |
| `Source/NonlinearSolvers/NonlinearSolver.H` | 非线性/线性求解器 | Newton/Picard/GMRES/PETSc/preconditioner | 59-60 | 逐块 | is, Vec, Ops, must, NonlinearSolver, Verbose | 未读 |
| `Source/NonlinearSolvers/NonlinearSolverLibrary.H` | 非线性/线性求解器 | Newton/Picard/GMRES/PETSc/preconditioner | 59-60 | 逐块 | to | 未读 |
| `Source/NonlinearSolvers/PETScKSP_Wrapper.H` | 非线性/线性求解器 | Newton/Picard/GMRES/PETSc/preconditioner | 59-60 | 逐块 | is, Vec, Ops, must, PETScKSP, solve | 未读 |
| `Source/NonlinearSolvers/PETScSNES_Wrapper.H` | 非线性/线性求解器 | Newton/Picard/GMRES/PETSc/preconditioner | 59-60 | 逐块 | is, Vec, Ops, PETScSNES | 未读 |
| `Source/NonlinearSolvers/PicardSolver.H` | 非线性/线性求解器 | Newton/Picard/GMRES/PETSc/preconditioner | 59-60 | 逐块 | Vec, Ops, PicardSolver | 未读 |
| `Source/NonlinearSolvers/Preconditioner.H` | 非线性/线性求解器 | Newton/Picard/GMRES/PETSc/preconditioner | 59-60 | 逐块 | is, T, Ops, must, Preconditioner, implementation, getPCMatrix, setName | 未读 |
| `Source/NonlinearSolvers/PreconditionerLibrary.H` | 非线性/线性求解器 | Newton/Picard/GMRES/PETSc/preconditioner | 59-60 | 逐块 |  | 未读 |
| `Source/NonlinearSolvers/WarpX_PETSc.H` | 非线性/线性求解器 | Newton/Picard/GMRES/PETSc/preconditioner | 59-60 | 逐块 | WarpXSolverVec, ImplicitSolver, SNESObj, KSPObj, MatObj, VecObj, PETScSolver_impl, uses | 未读 |
| `Source/NonlinearSolvers/WarpX_PETSc.cpp` | 非线性/线性求解器 | Newton/Picard/GMRES/PETSc/preconditioner | 59-60 | 逐块 | SNESObj, KSPObj, MatObj, VecObj, copyVec, RHSFunction, JacobianFunction, applyJacobian | 未读 |
| `Source/Parallelization/CMakeLists.txt` | 并行与 AMR | guard cells / communication / regrid | 71-77 | 逐块 |  | 未读 |
| `Source/Parallelization/GuardCellManager.H` | 并行与 AMR | guard cells / communication / regrid | 71-77 | 逐块 | computes, guardCellManager | 未读 |
| `Source/Parallelization/GuardCellManager.cpp` | 并行与 AMR | guard cells / communication / regrid | 71-77 | 逐块 | guardCellManager::Init | 未读 |
| `Source/Parallelization/Make.package` | 并行与 AMR | guard cells / communication / regrid | 71-77 | 逐块 |  | 未读 |
| `Source/Parallelization/WarpXComm.cpp` | 并行与 AMR | guard cells / communication / regrid | 71-77 | 逐块 | UpdateCurrentNodalToStag, WarpX::UpdateAuxilaryData, WarpX::UpdateAuxilaryDataStagToNodal, WarpX::UpdateAuxilaryDataSameType, WarpX::FillBoundaryB, WarpX::FillBoundaryE, WarpX::FillBoundaryF, WarpX::FillBoundaryG | 未读 |
| `Source/Parallelization/WarpXComm_K.H` | 并行与 AMR | guard cells / communication / regrid | 71-77 | 逐块 | warpx_interp | 未读 |
| `Source/Parallelization/WarpXRegrid.cpp` | 并行与 AMR | guard cells / communication / regrid | 71-77 | 逐块 | WarpX::CheckLoadBalance, WarpX::LoadBalance, ParallelDescriptor::IOProcessorNumber, WarpX::RemakeLevel, WarpX::ComputeCostsHeuristic, WarpX::ResetCosts, WarpX::RescaleCosts | 未读 |
| `Source/Parallelization/WarpXSumGuardCells.H` | 并行与 AMR | guard cells / communication / regrid | 71-77 | 逐块 |  | 未读 |
| `Source/Parallelization/WarpXSumGuardCells.cpp` | 并行与 AMR | guard cells / communication / regrid | 71-77 | 逐块 | WarpXSumGuardCells | 未读 |
| `Source/Particles/Algorithms/KineticEnergy.H` | 粒子系统 | species containers / boundaries / photon / laser particles | 17-35 | 逐块 | KineticEnergy, KineticEnergyPhotons | 未读 |
| `Source/Particles/Algorithms/Make.package` | 粒子系统 | species containers / boundaries / photon / laser particles | 17-35 | 逐块 |  | 未读 |
| `Source/Particles/CMakeLists.txt` | 粒子系统 | species containers / boundaries / photon / laser particles | 17-35 | 逐块 |  | 未读 |
| `Source/Particles/Collision/BackgroundMCC/BackgroundMCCCollision.H` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 | BackgroundMCCCollision | 未读 |
| `Source/Particles/Collision/BackgroundMCC/BackgroundMCCCollision.cpp` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 | std::sqrt, BackgroundMCCCollision::doCollisions, BackgroundMCCCollision::doBackgroundCollisionsWithinTile, BackgroundMCCCollision::doBackgroundIonization | 未读 |
| `Source/Particles/Collision/BackgroundMCC/CMakeLists.txt` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 |  | 未读 |
| `Source/Particles/Collision/BackgroundMCC/ImpactIonization.H` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 | ImpactIonizationFilterFunc, ImpactIonizationTransformFunc | 未读 |
| `Source/Particles/Collision/BackgroundMCC/Make.package` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 |  | 未读 |
| `Source/Particles/Collision/BackgroundStopping/BackgroundStopping.H` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 | class, BackgroundStopping | 未读 |
| `Source/Particles/Collision/BackgroundStopping/BackgroundStopping.cpp` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 | BackgroundStopping::doCollisions, BackgroundStopping::doBackgroundStoppingOnElectronsWithinTile, BackgroundStopping::doBackgroundStoppingOnIonsWithinTile | 未读 |
| `Source/Particles/Collision/BackgroundStopping/CMakeLists.txt` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 |  | 未读 |
| `Source/Particles/Collision/BackgroundStopping/Make.package` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 |  | 未读 |
| `Source/Particles/Collision/BinaryCollision/BinaryCollision.H` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 | performs, BinaryCollision, energy_correction_sort_by_weight_flags, doCollisionsWithinTile, constexpr | 未读 |
| `Source/Particles/Collision/BinaryCollision/BinaryCollisionUtils.H` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 | struct, nuclear_fusion_type_to_collision_type, is_two_product_fusion_type, get_collision_parameters, remove_weight_from_colliding_particle | 未读 |
| `Source/Particles/Collision/BinaryCollision/BinaryCollisionUtils.cpp` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 | get_collision_type, get_nuclear_fusion_type, CheckFusionEnergy | 未读 |
| `Source/Particles/Collision/BinaryCollision/Bremsstrahlung/BremsstrahlungFunc.H` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 | BremsstrahlungFunc, Executor, of | 未读 |
| `Source/Particles/Collision/BinaryCollision/Bremsstrahlung/BremsstrahlungFunc.cpp` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 | BremsstrahlungFunc::UploadCrossSection | 未读 |
| `Source/Particles/Collision/BinaryCollision/Bremsstrahlung/CMakeLists.txt` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 |  | 未读 |
| `Source/Particles/Collision/BinaryCollision/Bremsstrahlung/Make.package` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 |  | 未读 |
| `Source/Particles/Collision/BinaryCollision/Bremsstrahlung/PhotonCreationFunc.H` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 | PhotonCreationFunc | 未读 |
| `Source/Particles/Collision/BinaryCollision/Bremsstrahlung/PhotonCreationFunc.cpp` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 |  | 未读 |
| `Source/Particles/Collision/BinaryCollision/CMakeLists.txt` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 |  | 未读 |
| `Source/Particles/Collision/BinaryCollision/Coulomb/ElasticCollisionPerez.H` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 | of, ElasticCollisionPerez | 未读 |
| `Source/Particles/Collision/BinaryCollision/Coulomb/PairWiseCoulombCollisionFunc.H` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 | PairWiseCoulombCollisionFunc, Executor, of | 未读 |
| `Source/Particles/Collision/BinaryCollision/Coulomb/UpdateMomentumPerezElastic.H` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 | UpdateMomentumPerezElastic | 未读 |
| `Source/Particles/Collision/BinaryCollision/DSMC/CMakeLists.txt` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 |  | 未读 |
| `Source/Particles/Collision/BinaryCollision/DSMC/CollisionFilterFunc.H` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 | CollisionPairFilter | 未读 |
| `Source/Particles/Collision/BinaryCollision/DSMC/DSMCFunc.H` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 | performs, DSMCFunc, Executor, of, use_global_debye_length | 未读 |
| `Source/Particles/Collision/BinaryCollision/DSMC/DSMCFunc.cpp` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 |  | 未读 |
| `Source/Particles/Collision/BinaryCollision/DSMC/Make.package` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 |  | 未读 |
| `Source/Particles/Collision/BinaryCollision/DSMC/SplitAndScatterFunc.H` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 | defines, SplitAndScatterFunc | 未读 |
| `Source/Particles/Collision/BinaryCollision/DSMC/SplitAndScatterFunc.cpp` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 |  | 未读 |
| `Source/Particles/Collision/BinaryCollision/LinearBreitWheeler/LinearBreitWheelerCollisionFunc.H` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 | LinearBreitWheelerCollisionFunc, Executor, of, use_global_debye_length | 未读 |
| `Source/Particles/Collision/BinaryCollision/LinearBreitWheeler/LinearBreitWheelerCrossSection.H` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 | LinearBreitWheelerCrossSection | 未读 |
| `Source/Particles/Collision/BinaryCollision/LinearBreitWheeler/LinearBreitWheelerInitializeMomentum.H` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 | of, LinearBreitWheelerInitializeMomentum | 未读 |
| `Source/Particles/Collision/BinaryCollision/LinearBreitWheeler/LinearBreitWheelerUtil.H` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 | LinearBreitWheelerComputeProductMomenta | 未读 |
| `Source/Particles/Collision/BinaryCollision/LinearBreitWheeler/SingleLinearBreitWheelerCollisionEvent.H` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 | SingleLinearBreitWheelerCollisionEvent | 未读 |
| `Source/Particles/Collision/BinaryCollision/LinearCompton/LinearComptonCollisionFunc.H` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 | LinearComptonCollisionFunc, Executor, of, use_global_debye_length | 未读 |
| `Source/Particles/Collision/BinaryCollision/LinearCompton/LinearComptonInitializeMomentum.H` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 | of, LorentzTransformMomentum, LinearComptonInitializeMomentum | 未读 |
| `Source/Particles/Collision/BinaryCollision/LinearCompton/SingleLinearComptonCollisionEvent.H` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 | SingleLinearComptonCollisionEvent | 未读 |
| `Source/Particles/Collision/BinaryCollision/Make.package` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 |  | 未读 |
| `Source/Particles/Collision/BinaryCollision/NuclearFusion/BoschHaleFusionCrossSection.H` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 | BoschHaleFusionCrossSection | 未读 |
| `Source/Particles/Collision/BinaryCollision/NuclearFusion/NuclearFusionFunc.H` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 | NuclearFusionFunc, Executor, of, use_global_debye_length | 未读 |
| `Source/Particles/Collision/BinaryCollision/NuclearFusion/ProtonBoronFusionCrossSection.H` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 | ProtonBoronFusionCrossSectionTentori, ProtonBoronFusionCrossSectionBuck, ProtonBoronFusionCrossSection | 未读 |
| `Source/Particles/Collision/BinaryCollision/NuclearFusion/ProtonBoronFusionInitializeMomentum.H` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 | of, ProtonBoronFusionInitializeMomentum | 未读 |
| `Source/Particles/Collision/BinaryCollision/NuclearFusion/SingleNuclearFusionEvent.H` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 | SingleNuclearFusionEvent | 未读 |
| `Source/Particles/Collision/BinaryCollision/NuclearFusion/TwoProductFusionInitializeMomentum.H` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 | of, TwoProductFusionInitializeMomentum | 未读 |
| `Source/Particles/Collision/BinaryCollision/ParticleCreationFunc.H` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 | ParticleCreationFunc, does, NoParticleCreationFunc | 未读 |
| `Source/Particles/Collision/BinaryCollision/ParticleCreationFunc.cpp` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 |  | 未读 |
| `Source/Particles/Collision/BinaryCollision/ShuffleFisherYates.H` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 | IndependentPairHelper, ShuffleFisherYates, Initialize, shuffle | 未读 |
| `Source/Particles/Collision/BinaryCollision/TwoProductUtil.H` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 | TwoProductComputeProductMomenta | 未读 |
| `Source/Particles/Collision/BinaryCollision/VirtualPhotonCreation.H` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 |  | 未读 |
| `Source/Particles/Collision/BinaryCollision/VirtualPhotonCreation.cpp` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 | GenerateVirtualPhotons | 未读 |
| `Source/Particles/Collision/CMakeLists.txt` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 |  | 未读 |
| `Source/Particles/Collision/CollisionBase.H` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 | class, CollisionBase, doCollisions | 未读 |
| `Source/Particles/Collision/CollisionBase.cpp` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 | CollisionBase::BackwardCompatibility | 未读 |
| `Source/Particles/Collision/CollisionHandler.H` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 | that, CollisionHandler | 未读 |
| `Source/Particles/Collision/CollisionHandler.cpp` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 | CollisionHandler::doCollisions | 未读 |
| `Source/Particles/Collision/Make.package` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 |  | 未读 |
| `Source/Particles/Collision/PulsedDecay/CMakeLists.txt` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 |  | 未读 |
| `Source/Particles/Collision/PulsedDecay/Make.package` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 |  | 未读 |
| `Source/Particles/Collision/PulsedDecay/PulsedDecay.H` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 | performs, PulsedDecay | 未读 |
| `Source/Particles/Collision/PulsedDecay/PulsedDecay.cpp` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 | PulsedDecay::doCollisions | 未读 |
| `Source/Particles/Collision/ScatteringProcess.H` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 | class, ScatteringProcess, Executor, getCrossSection | 未读 |
| `Source/Particles/Collision/ScatteringProcess.cpp` | 碰撞 | MCC / binary collision / stopping / decay | 90-94 | 逐块 | ScatteringProcess::ScatteringProcess, ScatteringProcess::init, ScatteringProcess::parseProcessType, ScatteringProcess::readCrossSectionFile, ScatteringProcess::sanityCheckEnergyGrid | 未读 |
| `Source/Particles/Deposition/CMakeLists.txt` | 沉积 | charge/current/mass/temperature deposition | 36-45 | 逐行 |  | 未读 |
| `Source/Particles/Deposition/ChargeDeposition.H` | 沉积 | charge/current/mass/temperature deposition | 36-45 | 逐行 | doChargeDepositionShapeN, doChargeDepositionSharedShapeN, amrex::Gpu::gpuStream | 未读 |
| `Source/Particles/Deposition/CurrentDeposition.H` | 沉积 | charge/current/mass/temperature deposition | 36-45 | 逐行 | eb_flags, doDepositionShapeNKernel, doDepositionShapeN, doDepositionShapeNImplicit, doDepositionSharedShapeN, doEsirkepovDepositionShapeN, constexpr, doChargeConservingDepositionShapeNImplicit | 未读 |
| `Source/Particles/Deposition/Make.package` | 沉积 | charge/current/mass/temperature deposition | 36-45 | 逐行 |  | 未读 |
| `Source/Particles/Deposition/MassMatricesDeposition.H` | 沉积 | charge/current/mass/temperature deposition | 36-45 | 逐行 | setMassMatricesKernels, doDirectJandSigmaDepositionKernel, constexpr, doDirectSigmaDeposition, doVillasenorJandSigmaDepositionKernel, doVillasenorSigmaDeposition | 未读 |
| `Source/Particles/Deposition/SharedDepositionUtils.H` | 沉积 | charge/current/mass/temperature deposition | 36-45 | 逐行 | getMaxTboxAlongDim, depositComponent | 未读 |
| `Source/Particles/Deposition/TemperatureDeposition.H` | 沉积 | charge/current/mass/temperature deposition | 36-45 | 逐行 | varianceDepositionSubKernel, doVarianceDepositionShapeNKernel, doVarianceDepositionShapeN | 未读 |
| `Source/Particles/Deposition/TemperatureDepositionTypes.H` | 沉积 | charge/current/mass/temperature deposition | 36-45 | 逐行 |  | 未读 |
| `Source/Particles/Deposition/VarianceAccumulationBuffer.H` | 沉积 | charge/current/mass/temperature deposition | 36-45 | 逐行 | VarianceAccumulationBuffer | 未读 |
| `Source/Particles/Deposition/VarianceAccumulationBuffer.cpp` | 沉积 | charge/current/mass/temperature deposition | 36-45 | 逐行 | VarianceAccumulationBuffer::reset, VarianceAccumulationBuffer::get, VarianceAccumulationBuffer::get_n, VarianceAccumulationBuffer::ConvertVarianceToTemperatureAndFilter | 未读 |
| `Source/Particles/ElementaryProcess/CMakeLists.txt` | 基本过程 | ionization / QED photon emission / pair generation | 95-99 | 逐块 |  | 未读 |
| `Source/Particles/ElementaryProcess/Ionization.H` | 基本过程 | ionization / QED photon emission / pair generation | 95-99 | 逐块 | IonizationFilterFunc, IonizationTransformFunc | 未读 |
| `Source/Particles/ElementaryProcess/Ionization.cpp` | 基本过程 | ionization / QED photon emission / pair generation | 95-99 | 逐块 |  | 未读 |
| `Source/Particles/ElementaryProcess/Make.package` | 基本过程 | ionization / QED photon emission / pair generation | 95-99 | 逐块 |  | 未读 |
| `Source/Particles/ElementaryProcess/QEDInternals/BreitWheelerEngineWrapper.H` | 基本过程 | ionization / QED photon emission / pair generation | 95-99 | 逐块 | RandomEngine, PicsarBreitWheelerCtrl, BreitWheelerGetOpticalDepth, BreitWheelerEvolveOpticalDepth, BreitWheelerGeneratePairs, BreitWheelerEngine | 未读 |
| `Source/Particles/ElementaryProcess/QEDInternals/BreitWheelerEngineWrapper.cpp` | 基本过程 | ionization / QED photon emission / pair generation | 95-99 | 逐块 | BreitWheelerEngine::init_lookup_tables_from_raw_data, BreitWheelerEngine::init_builtin_tables, BreitWheelerEngine::export_lookup_tables_data, BreitWheelerEngine::compute_lookup_tables, BreitWheelerEngine::init_builtin_dndt_table, BreitWheelerEngine::init_builtin_pair_prod_table | 未读 |
| `Source/Particles/ElementaryProcess/QEDInternals/BreitWheelerEngineWrapper_fwd.H` | 基本过程 | ionization / QED photon emission / pair generation | 95-99 | 逐块 | BreitWheelerGetOpticalDepth, BreitWheelerEvolveOpticalDepth, BreitWheelerGeneratePairs, BreitWheelerEngine | 未读 |
| `Source/Particles/ElementaryProcess/QEDInternals/CMakeLists.txt` | 基本过程 | ionization / QED photon emission / pair generation | 95-99 | 逐块 |  | 未读 |
| `Source/Particles/ElementaryProcess/QEDInternals/Make.package` | 基本过程 | ionization / QED photon emission / pair generation | 95-99 | 逐块 |  | 未读 |
| `Source/Particles/ElementaryProcess/QEDInternals/QedChiFunctions.H` | 基本过程 | ionization / QED photon emission / pair generation | 95-99 | 逐块 | chi_photon, chi_ele_pos | 未读 |
| `Source/Particles/ElementaryProcess/QEDInternals/QedWrapperCommons.H` | 基本过程 | ionization / QED photon emission / pair generation | 95-99 | 逐块 | provides, PicsarQedVector, pxr_sync | 未读 |
| `Source/Particles/ElementaryProcess/QEDInternals/QuantumSyncEngineWrapper.H` | 基本过程 | ionization / QED photon emission / pair generation | 95-99 | 逐块 | RandomEngine, PicsarQuantumSyncCtrl, QuantumSynchrotronGetOpticalDepth, QuantumSynchrotronEvolveOpticalDepth, QuantumSynchrotronPhotonEmission, QuantumSynchrotronEngine | 未读 |
| `Source/Particles/ElementaryProcess/QEDInternals/QuantumSyncEngineWrapper.cpp` | 基本过程 | ionization / QED photon emission / pair generation | 95-99 | 逐块 | QuantumSynchrotronEngine::build_optical_depth_functor, QuantumSynchrotronEngine::build_evolve_functor, QuantumSynchrotronEngine::build_phot_em_functor, QuantumSynchrotronEngine::init_lookup_tables_from_raw_data, QuantumSynchrotronEngine::init_builtin_tables, QuantumSynchrotronEngine::export_lookup_tables_data, QuantumSynchrotronEngine::compute_lookup_tables, QuantumSynchrotronEngine::init_builtin_dndt_table | 未读 |
| `Source/Particles/ElementaryProcess/QEDInternals/QuantumSyncEngineWrapper_fwd.H` | 基本过程 | ionization / QED photon emission / pair generation | 95-99 | 逐块 | QuantumSynchrotronGetOpticalDepth, QuantumSynchrotronEvolveOpticalDepth, QuantumSynchrotronPhotonEmission, QuantumSynchrotronEngine | 未读 |
| `Source/Particles/ElementaryProcess/QEDInternals/SchwingerProcessWrapper.H` | 基本过程 | ionization / QED photon emission / pair generation | 95-99 | 逐块 | getSchwingerProductionNumber | 未读 |
| `Source/Particles/ElementaryProcess/QEDPairGeneration.H` | 基本过程 | ionization / QED photon emission / pair generation | 95-99 | 逐块 | PairGenerationFilterFunc, PairGenerationTransformFunc | 未读 |
| `Source/Particles/ElementaryProcess/QEDPairGeneration.cpp` | 基本过程 | ionization / QED photon emission / pair generation | 95-99 | 逐块 |  | 未读 |
| `Source/Particles/ElementaryProcess/QEDPhotonEmission.H` | 基本过程 | ionization / QED photon emission / pair generation | 95-99 | 逐块 | PhotonEmissionFilterFunc, PhotonEmissionTransformFunc, cleanLowEnergyPhotons | 未读 |
| `Source/Particles/ElementaryProcess/QEDPhotonEmission.cpp` | 基本过程 | ionization / QED photon emission / pair generation | 95-99 | 逐块 |  | 未读 |
| `Source/Particles/ElementaryProcess/QEDSchwingerProcess.H` | 基本过程 | ionization / QED photon emission / pair generation | 95-99 | 逐块 | SchwingerFilterFunc, with, SchwingerTransformFunc | 未读 |
| `Source/Particles/ExternalParticleFields.H` | 粒子系统 | species containers / boundaries / photon / laser particles | 17-35 | 逐块 | contains, ParticleFieldMetaData, ExternalParticleFields | 未读 |
| `Source/Particles/ExternalParticleFields.cpp` | 粒子系统 | species containers / boundaries / photon / laser particles | 17-35 | 逐块 | ExternalParticleFields::ReadParameters | 未读 |
| `Source/Particles/Filter/FilterFunctors.H` | 粒子过滤 | particle selection / filtering functors | 35 | 逐块 | struct, RandomFilter, UniformFilter, ParserFilter, GeometryFilter, operator | 未读 |
| `Source/Particles/Filter/Make.package` | 粒子过滤 | particle selection / filtering functors | 35 | 逐块 |  | 未读 |
| `Source/Particles/Gather/CMakeLists.txt` | 场插值 | shape factor / gather / external fields | 27 | 逐行 |  | 未读 |
| `Source/Particles/Gather/FieldGather.H` | 场插值 | shape factor / gather / external fields | 27 | 逐行 | doDirectGatherVectorField, doGatherShapeN, doGatherShapeNEsirkepovStencilImplicit, doGatherPicnicShapeN, constexpr, doGatherShapeNImplicit | 未读 |
| `Source/Particles/Gather/GetExternalFields.H` | 场插值 | shape factor / gather / external fields | 27 | 逐行 | that, GetExternalEBField, ExternalFieldInitType | 未读 |
| `Source/Particles/Gather/GetExternalFields.cpp` | 场插值 | shape factor / gather / external fields | 27 | 逐行 |  | 未读 |
| `Source/Particles/Gather/Make.package` | 场插值 | shape factor / gather / external fields | 27 | 逐行 |  | 未读 |
| `Source/Particles/Gather/ScaleFields.H` | 场插值 | shape factor / gather / external fields | 27 | 逐行 | ScaleFields | 未读 |
| `Source/Particles/LaserParticleContainer.H` | 粒子系统 | species containers / boundaries / photon / laser particles | 17-35 | 逐块 | LaserParticleContainer | 未读 |
| `Source/Particles/LaserParticleContainer.cpp` | 粒子系统 | species containers / boundaries / photon / laser particles | 17-35 | 逐块 | CrossProduct, LaserParticleContainer::ContinuousInjection, LaserParticleContainer::UpdateAntennaPosition, LaserParticleContainer::InitData, LaserParticleContainer::Evolve, LaserParticleContainer::PostRestart, LaserParticleContainer::ComputeWeightMobility, LaserParticleContainer::PushP | 未读 |
| `Source/Particles/Make.package` | 粒子系统 | species containers / boundaries / photon / laser particles | 17-35 | 逐块 |  | 未读 |
| `Source/Particles/MultiParticleContainer.H` | 粒子系统 | species containers / boundaries / photon / laser particles | 17-35 | 逐块 | MultiParticleContainer, WarpXParticleContainer, WarpX, struct, meanParticleVelocity, begin, end, MFItInfoCheckTiling | 未读 |
| `Source/Particles/MultiParticleContainer.cpp` | 粒子系统 | species containers / boundaries / photon / laser particles | 17-35 | 逐块 | MyFieldList, MultiParticleContainer::ReadParameters, MultiParticleContainer::maxParticleVelocity, MultiParticleContainer::AllocData, MultiParticleContainer::InitData, MultiParticleContainer::PostRestart, MultiParticleContainer::InitMultiPhysicsModules, MultiParticleContainer::Evolve | 未读 |
| `Source/Particles/MultiParticleContainer_fwd.H` | 粒子系统 | species containers / boundaries / photon / laser particles | 17-35 | 逐块 | MultiParticleContainer | 未读 |
| `Source/Particles/ParticleBoundaries.H` | 粒子系统 | species containers / boundaries / photon / laser particles | 17-35 | 逐块 | ParticleBoundaries, ParticleBoundariesData | 未读 |
| `Source/Particles/ParticleBoundaries.cpp` | 粒子系统 | species containers / boundaries / photon / laser particles | 17-35 | 逐块 | set_to_periodic_if_field_boundary_is_periodic, check_consistency, parse_particle_boundaries, ParticleBoundaries::Set_reflect_all_velocities, ParticleBoundaries::SetAll, ParticleBoundaries::SetThermalVelocity, ParticleBoundaries::SetBoundsX, ParticleBoundaries::SetBoundsY | 未读 |
| `Source/Particles/ParticleBoundaries_K.H` | 粒子系统 | species containers / boundaries / photon / laser particles | 17-35 | 逐块 | apply_boundary, thermalize_boundary_particle, apply_boundaries | 未读 |
| `Source/Particles/ParticleBoundaryBuffer.H` | 粒子系统 | species containers / boundaries / photon / laser particles | 17-35 | 逐块 | WARPX_EXPORT, numBoundaries, isDefinedForAnySpecies, boundaryName | 未读 |
| `Source/Particles/ParticleBoundaryBuffer.cpp` | 粒子系统 | species containers / boundaries / photon / laser particles | 17-35 | 逐块 | IsOutsideDomainBoundary, FindEmbeddedBoundaryIntersection, CopyAndTimestamp, ParticleBoundaryBuffer::redistribute, ParticleBoundaryBuffer::clearParticles, ParticleBoundaryBuffer::gatherParticlesFromDomainBoundaries, ParticleBoundaryBuffer::gatherParticlesFromEmbeddedBoundaries, ParticleBoundaryBuffer::getNumParticlesInContainer | 未读 |
| `Source/Particles/ParticleBoundaryBuffer_fwd.H` | 粒子系统 | species containers / boundaries / photon / laser particles | 17-35 | 逐块 | ParticleBoundaryBuffer | 未读 |
| `Source/Particles/ParticleCreation/AddParticles.cpp` | 粒子初始化 | species sampling / density / momentum | 21, 83-84 | 逐块 | PhysicalParticleContainer::AddParticles, PhysicalParticleContainer::ContinuousInjection, PhysicalParticleContainer::ContinuousFluxInjection, PhysicalParticleContainer::CheckAndAddParticle, PhysicalParticleContainer::AddGaussianBeam, PhysicalParticleContainer::AddPlasmaFromFile, PhysicalParticleContainer::AddPlasma, PhysicalParticleContainer::AddPlasmaFlux | 未读 |
| `Source/Particles/ParticleCreation/AddPlasmaUtilities.H` | 粒子初始化 | species sampling / density / momentum | 21, 83-84 | 逐块 | PDim3, PlasmaParserWrapper, PlasmaParserHelper, QEDHelper, scale_fac, compute_area_weights, compute_scale_fac_area_eb, rotate_momentum_eb | 未读 |
| `Source/Particles/ParticleCreation/AddPlasmaUtilities.cpp` | 粒子初始化 | species sampling / density / momentum | 21, 83-84 | 逐块 | find_overlap, find_overlap_flux, PlasmaParserHelper::getUserIntDataPtrs, PlasmaParserHelper::getUserRealDataPtrs | 未读 |
| `Source/Particles/ParticleCreation/CMakeLists.txt` | 粒子初始化 | species sampling / density / momentum | 21, 83-84 | 逐块 |  | 未读 |
| `Source/Particles/ParticleCreation/DefaultInitialization.H` | 粒子初始化 | species sampling / density / momentum | 21, 83-84 | 逐块 | struct, initializeRealValue, initializeIntValue, DefaultInitializeRuntimeAttributes | 未读 |
| `Source/Particles/ParticleCreation/FilterCopyTransform.H` | 粒子初始化 | species sampling / density / momentum | 21, 83-84 | 逐块 |  | 未读 |
| `Source/Particles/ParticleCreation/FilterCreateTransformFromFAB.H` | 粒子初始化 | species sampling / density / momentum | 21, 83-84 | 逐块 | with | 未读 |
| `Source/Particles/ParticleCreation/Make.package` | 粒子初始化 | species sampling / density / momentum | 21, 83-84 | 逐块 |  | 未读 |
| `Source/Particles/ParticleCreation/SmartCopy.H` | 粒子初始化 | species sampling / density / momentum | 21, 83-84 | 逐块 | SmartCopy, SmartCopyFactory, SrcPC, DstPC | 未读 |
| `Source/Particles/ParticleCreation/SmartCreate.H` | 粒子初始化 | species sampling / density / momentum | 21, 83-84 | 逐块 | SmartCreate, SmartCreateFactory, PartTileData, operator | 未读 |
| `Source/Particles/ParticleCreation/SmartUtils.H` | 粒子初始化 | species sampling / density / momentum | 21, 83-84 | 逐块 | SmartCopyTag, setNewParticleIDs | 未读 |
| `Source/Particles/ParticleCreation/SmartUtils.cpp` | 粒子初始化 | species sampling / density / momentum | 21, 83-84 | 逐块 |  | 未读 |
| `Source/Particles/ParticleIO.H` | 粒子系统 | species containers / boundaries / photon / laser particles | 17-35 | 逐块 | struct, of, particlesConvertUnits | 未读 |
| `Source/Particles/ParticleThermalizer/CMakeLists.txt` | 粒子热边界 | thermal boundary / rethermalization | 29, 35 | 逐块 |  | 未读 |
| `Source/Particles/ParticleThermalizer/Make.package` | 粒子热边界 | thermal boundary / rethermalization | 29, 35 | 逐块 |  | 未读 |
| `Source/Particles/ParticleThermalizer/ParticleThermalizer.H` | 粒子热边界 | thermal boundary / rethermalization | 29, 35 | 逐块 | MultiParticleContainer, WarpXParticleContainer, ParticleThermalizer | 未读 |
| `Source/Particles/ParticleThermalizer/ParticleThermalizer.cpp` | 粒子热边界 | thermal boundary / rethermalization | 29, 35 | 逐块 | ParticleThermalizer::applyThermalizer | 未读 |
| `Source/Particles/PhotonParticleContainer.H` | 粒子系统 | species containers / boundaries / photon / laser particles | 17-35 | 逐块 | PhotonParticleContainer | 未读 |
| `Source/Particles/PhotonParticleContainer.cpp` | 粒子系统 | species containers / boundaries / photon / laser particles | 17-35 | 逐块 | exteb_flags, qed_flags, PhotonParticleContainer::InitData, PhotonParticleContainer::PushPX, constexpr, PhotonParticleContainer::Evolve | 未读 |
| `Source/Particles/PhysicalParticleContainer.H` | 粒子系统 | species containers / boundaries / photon / laser particles | 17-35 | 逐块 | containing, PhysicalParticleContainer | 未读 |
| `Source/Particles/PhysicalParticleContainer.cpp` | 粒子系统 | species containers / boundaries / photon / laser particles | 17-35 | 逐块 | Data, exteb_flags, qed_flags, PhysicalParticleContainer::AllocData, PhysicalParticleContainer::BackwardCompatibility, PhysicalParticleContainer::InitData, PhysicalParticleContainer::DefaultInitializeRuntimeAttributes, PhysicalParticleContainer::Evolve | 未读 |
| `Source/Particles/Pusher/CMakeLists.txt` | 粒子推进器 | Lorentz 力 / Boris/Vay/Higuera-Cary | 22-26 | 逐行 |  | 未读 |
| `Source/Particles/Pusher/CopyParticleAttribs.H` | 粒子推进器 | Lorentz 力 / Boris/Vay/Higuera-Cary | 22-26 | 逐行 | CopyParticleAttribs | 未读 |
| `Source/Particles/Pusher/GetAndSetPosition.H` | 粒子推进器 | Lorentz 力 / Boris/Vay/Higuera-Cary | 22-26 | 逐行 | GetParticlePosition, SetParticlePosition, operator, AsStored | 未读 |
| `Source/Particles/Pusher/ImplicitPushPX.cpp` | 粒子推进器 | Lorentz 力 / Boris/Vay/Higuera-Cary | 22-26 | 逐行 | exteb_flags, qed_flags, depos_order_flags, PushXPSingleStep, constexpr, PhysicalParticleContainer::FindSuborbitParticles, PhysicalParticleContainer::SetupSuborbitParticles, PhysicalParticleContainer::ImplicitPushXP | 未读 |
| `Source/Particles/Pusher/Make.package` | 粒子推进器 | Lorentz 力 / Boris/Vay/Higuera-Cary | 22-26 | 逐行 |  | 未读 |
| `Source/Particles/Pusher/PushSelector.H` | 粒子推进器 | Lorentz 力 / Boris/Vay/Higuera-Cary | 22-26 | 逐行 | doParticleMomentumPush, constexpr | 未读 |
| `Source/Particles/Pusher/UpdateMomentumBoris.H` | 粒子推进器 | Lorentz 力 / Boris/Vay/Higuera-Cary | 22-26 | 逐行 | UpdateMomentumBoris | 未读 |
| `Source/Particles/Pusher/UpdateMomentumBorisWithRadiationReaction.H` | 粒子推进器 | Lorentz 力 / Boris/Vay/Higuera-Cary | 22-26 | 逐行 | UpdateMomentumBorisWithRadiationReaction | 未读 |
| `Source/Particles/Pusher/UpdateMomentumHigueraCary.H` | 粒子推进器 | Lorentz 力 / Boris/Vay/Higuera-Cary | 22-26 | 逐行 | UpdateMomentumHigueraCary | 未读 |
| `Source/Particles/Pusher/UpdateMomentumVay.H` | 粒子推进器 | Lorentz 力 / Boris/Vay/Higuera-Cary | 22-26 | 逐行 | UpdateMomentumVay | 未读 |
| `Source/Particles/Pusher/UpdatePosition.H` | 粒子推进器 | Lorentz 力 / Boris/Vay/Higuera-Cary | 22-26 | 逐行 | UpdatePosition, UpdatePositionImplicit, PositionNorm | 未读 |
| `Source/Particles/Resampling/CMakeLists.txt` | 粒子重采样 | thinning / leveling / weight conservation | 34 | 逐块 |  | 未读 |
| `Source/Particles/Resampling/LevelingThinning.H` | 粒子重采样 | thinning / leveling / weight conservation | 34 | 逐块 | implements, LevelingThinning | 未读 |
| `Source/Particles/Resampling/LevelingThinning.cpp` | 粒子重采样 | thinning / leveling / weight conservation | 34 | 逐块 | LevelingThinning::BackwardCompatibility | 未读 |
| `Source/Particles/Resampling/Make.package` | 粒子重采样 | thinning / leveling / weight conservation | 34 | 逐块 |  | 未读 |
| `Source/Particles/Resampling/Resampling.H` | 粒子重采样 | thinning / leveling / weight conservation | 34 | 逐块 | from, ResamplingAlgorithm, used, Resampling | 未读 |
| `Source/Particles/Resampling/Resampling.cpp` | 粒子重采样 | thinning / leveling / weight conservation | 34 | 逐块 |  | 未读 |
| `Source/Particles/Resampling/ResamplingTrigger.H` | 粒子重采样 | thinning / leveling / weight conservation | 34 | 逐块 | is, ResamplingTrigger | 未读 |
| `Source/Particles/Resampling/ResamplingTrigger.cpp` | 粒子重采样 | thinning / leveling / weight conservation | 34 | 逐块 | ResamplingTrigger::triggered | 未读 |
| `Source/Particles/Resampling/VelocityCoincidenceThinning.H` | 粒子重采样 | thinning / leveling / weight conservation | 34 | 逐块 | implements, VelocityCoincidenceThinning, struct, HeapSort, VelocityBinCalculator, operator | 未读 |
| `Source/Particles/Resampling/VelocityCoincidenceThinning.cpp` | 粒子重采样 | thinning / leveling / weight conservation | 34 | 逐块 |  | 未读 |
| `Source/Particles/RigidInjectedParticleContainer.H` | 粒子系统 | species containers / boundaries / photon / laser particles | 17-35 | 逐块 | RigidInjectedParticleContainer | 未读 |
| `Source/Particles/RigidInjectedParticleContainer.cpp` | 粒子系统 | species containers / boundaries / photon / laser particles | 17-35 | 逐块 | exteb_flags, RigidInjectedParticleContainer::InitData, RigidInjectedParticleContainer::RemapParticles, RigidInjectedParticleContainer::PushPX, RigidInjectedParticleContainer::Evolve, RigidInjectedParticleContainer::PushP, constexpr | 未读 |
| `Source/Particles/ShapeFactors.H` | 粒子系统 | species containers / boundaries / photon / laser particles | 17-35 | 逐块 | Compute_shape_factor, Compute_shifted_shape_factor, Compute_shape_factor_pair, operator, constexpr | 未读 |
| `Source/Particles/Sorting/CMakeLists.txt` | 粒子排序 | load balance / deposition locality | 33, 77 | 逐块 |  | 未读 |
| `Source/Particles/Sorting/Make.package` | 粒子排序 | load balance / deposition locality | 33, 77 | 逐块 |  | 未读 |
| `Source/Particles/Sorting/Partition.cpp` | 粒子排序 | load balance / deposition locality | 33, 77 | 逐块 | PhysicalParticleContainer::PartitionParticlesInBuffers | 未读 |
| `Source/Particles/Sorting/SortingUtils.H` | 粒子排序 | load balance / deposition locality | 33, 77 | 逐块 | fillBufferFlag, fillBufferFlagRemainingParticles, copyAndReorder, stablePartition, iteratorDistance | 未读 |
| `Source/Particles/Sorting/SortingUtils.cpp` | 粒子排序 | load balance / deposition locality | 33, 77 | 逐块 | fillWithConsecutiveIntegers | 未读 |
| `Source/Particles/SpeciesPhysicalProperties.H` | 粒子系统 | species containers / boundaries / photon / laser particles | 17-35 | 逐块 | struct | 未读 |
| `Source/Particles/SpeciesPhysicalProperties.cpp` | 粒子系统 | species containers / boundaries / photon / laser particles | 17-35 | 逐块 | Properties, from_string, get_charge, get_mass, get_name | 未读 |
| `Source/Particles/WarpXParticleContainer.H` | 粒子系统 | species containers / boundaries / photon / laser particles | 17-35 | 逐块 | of, PIdx, IntIdx, DiagIdx, WarpXParIter, from, WarpXParticleContainer, InitIonizationModule | 未读 |
| `Source/Particles/WarpXParticleContainer.cpp` | 粒子系统 | species containers / boundaries / photon / laser particles | 17-35 | 逐块 | of, WarpXParticleContainer::ReadParameters, WarpXParticleContainer::AllocData, WarpXParticleContainer::AddNParticles, WarpXParticleContainer::deleteInvalidParticles, WarpXParticleContainer::DepositCurrent, WarpXParticleContainer::DepositMassMatrices, WarpXParticleContainer::DepositCharge | 未读 |
| `Source/Particles/WarpXParticleContainer_fwd.H` | 粒子系统 | species containers / boundaries / photon / laser particles | 17-35 | 逐块 | struct, PIdx, DiagIdx, WarpXParIter, WarpXParticleContainer | 未读 |
| `Source/Python/CMakeLists.txt` | Python 接口 | callbacks / pybind / PICMI access | 114-116 | 逐块 |  | 未读 |
| `Source/Python/Make.package` | Python 接口 | callbacks / pybind / PICMI access | 114-116 | 逐块 |  | 未读 |
| `Source/Python/MultiFabRegister.cpp` | Python 接口 | callbacks / pybind / PICMI access | 114-116 | 逐块 | init_MultiFabRegister, py::arg | 未读 |
| `Source/Python/Particles/CMakeLists.txt` | Python 接口 | callbacks / pybind / PICMI access | 114-116 | 逐块 |  | 未读 |
| `Source/Python/Particles/MultiParticleContainer.cpp` | Python 接口 | callbacks / pybind / PICMI access | 114-116 | 逐块 | init_MultiParticleContainer | 未读 |
| `Source/Python/Particles/ParticleBoundaryBuffer.cpp` | Python 接口 | callbacks / pybind / PICMI access | 114-116 | 逐块 | BoundaryBufferParIter, init_BoundaryBufferParIter, init_ParticleBoundaryBuffer | 未读 |
| `Source/Python/Particles/WarpXParticleContainer.cpp` | Python 接口 | callbacks / pybind / PICMI access | 114-116 | 逐块 | init_WarpXParIter, init_WarpXParticleContainer | 未读 |
| `Source/Python/WarpX.cpp` | Python 接口 | callbacks / pybind / PICMI access | 114-116 | 逐块 | Config, get_or_throw, constexpr, init_WarpX | 未读 |
| `Source/Python/callbacks.H` | Python 接口 | callbacks / pybind / PICMI access | 114-116 | 逐块 |  | 未读 |
| `Source/Python/callbacks.cpp` | Python 接口 | callbacks / pybind / PICMI access | 114-116 | 逐块 | InstallPythonCallback, IsPythonCallbackInstalled, ExecutePythonCallback, ClearPythonCallback | 未读 |
| `Source/Python/pyWarpX.H` | Python 接口 | callbacks / pybind / PICMI access | 114-116 | 逐块 |  | 未读 |
| `Source/Python/pyWarpX.cpp` | Python 接口 | callbacks / pybind / PICMI access | 114-116 | 逐块 |  | 未读 |
| `Source/Utils/Algorithms/IsIn.H` | 工具与算法选择 | constants / moving window / parser helpers | 8, 80, 89 | 逐块 | is_in, any_of_is_in | 未读 |
| `Source/Utils/Algorithms/Make.package` | 工具与算法选择 | constants / moving window / parser helpers | 8, 80, 89 | 逐块 |  | 未读 |
| `Source/Utils/CMakeLists.txt` | 工具与算法选择 | constants / moving window / parser helpers | 8, 80, 89 | 逐块 |  | 未读 |
| `Source/Utils/Interpolate.H` | 工具与算法选择 | constants / moving window / parser helpers | 8, 80, 89 | 逐块 |  | 未读 |
| `Source/Utils/Interpolate.cpp` | 工具与算法选择 | constants / moving window / parser helpers | 8, 80, 89 | 逐块 | getInterpolatedScalar, getInterpolatedVector | 未读 |
| `Source/Utils/Interpolate_K.H` | 工具与算法选择 | constants / moving window / parser helpers | 8, 80, 89 | 逐块 |  | 未读 |
| `Source/Utils/Logo/CMakeLists.txt` | 工具与算法选择 | constants / moving window / parser helpers | 8, 80, 89 | 逐块 |  | 未读 |
| `Source/Utils/Logo/GetLogo.H` | 工具与算法选择 | constants / moving window / parser helpers | 8, 80, 89 | 逐块 |  | 未读 |
| `Source/Utils/Logo/GetLogo.cpp` | 工具与算法选择 | constants / moving window / parser helpers | 8, 80, 89 | 逐块 |  | 未读 |
| `Source/Utils/Logo/Make.package` | 工具与算法选择 | constants / moving window / parser helpers | 8, 80, 89 | 逐块 |  | 未读 |
| `Source/Utils/Make.package` | 工具与算法选择 | constants / moving window / parser helpers | 8, 80, 89 | 逐块 |  | 未读 |
| `Source/Utils/NCIGodfreyTables.H` | 工具与算法选择 | constants / moving window / parser helpers | 8, 80, 89 | 逐块 |  | 未读 |
| `Source/Utils/Parser/CMakeLists.txt` | 工具与算法选择 | constants / moving window / parser helpers | 8, 80, 89 | 逐块 |  | 未读 |
| `Source/Utils/Parser/IntervalsParser.H` | 工具与算法选择 | constants / moving window / parser helpers | 8, 80, 89 | 逐块 | is, SliceParser, contains, IntervalsParser, BTDIntervalsParser | 未读 |
| `Source/Utils/Parser/IntervalsParser.cpp` | 工具与算法选择 | constants / moving window / parser helpers | 8, 80, 89 | 逐块 | utils::parser::SliceParser::contains, utils::parser::SliceParser::nextContains, utils::parser::SliceParser::previousContains, utils::parser::IntervalsParser::contains, utils::parser::IntervalsParser::previousContainsInclusive | 未读 |
| `Source/Utils/Parser/Make.package` | 工具与算法选择 | constants / moving window / parser helpers | 8, 80, 89 | 逐块 |  | 未读 |
| `Source/Utils/Parser/ParserUtils.H` | 工具与算法选择 | constants / moving window / parser helpers | 8, 80, 89 | 逐块 | compileParser, queryWithParser, queryArrWithParser, getWithParser, getArrWithParser | 未读 |
| `Source/Utils/Parser/ParserUtils.cpp` | 工具与算法选择 | constants / moving window / parser helpers | 8, 80, 89 | 逐块 | utils::parser::Store_parserString, utils::parser::Query_parserString, utils::parser::query, utils::parser::get, utils::parser::makeParser | 未读 |
| `Source/Utils/ParticleUtils.H` | 工具与算法选择 | constants / moving window / parser helpers | 8, 80, 89 | 逐块 | HeapSortDecreasing, getCollisionEnergy, doLorentzTransform, doLorentzTransformWithU, doLorentzTransformWithP, getRandomVector, RandomizeVelocity, containsInclusive | 未读 |
| `Source/Utils/ParticleUtils.cpp` | 工具与算法选择 | constants / moving window / parser helpers | 8, 80, 89 | 逐块 | findParticlesInEachCell | 未读 |
| `Source/Utils/Physics/IonizationEnergiesTable.H` | 工具与算法选择 | constants / moving window / parser helpers | 8, 80, 89 | 逐块 |  | 未读 |
| `Source/Utils/Physics/Make.package` | 工具与算法选择 | constants / moving window / parser helpers | 8, 80, 89 | 逐块 |  | 未读 |
| `Source/Utils/Physics/write_atomic_data_cpp.py` | 工具与算法选择 | constants / moving window / parser helpers | 8, 80, 89 | 逐块 | open | 未读 |
| `Source/Utils/SpeciesUtils.H` | 工具与算法选择 | constants / moving window / parser helpers | 8, 80, 89 | 逐块 |  | 未读 |
| `Source/Utils/SpeciesUtils.cpp` | 工具与算法选择 | constants / moving window / parser helpers | 8, 80, 89 | 逐块 | StringParseAbortMessage, extractSpeciesProperties, parseDensity, parseMomentum | 未读 |
| `Source/Utils/TextMsg.H` | 工具与算法选择 | constants / moving window / parser helpers | 8, 80, 89 | 逐块 |  | 未读 |
| `Source/Utils/WarpXAlgorithmSelection.H` | 工具与算法选择 | constants / moving window / parser helpers | 8, 80, 89 | 逐块 | to, Euler | 未读 |
| `Source/Utils/WarpXConst.H` | 工具与算法选择 | constants / moving window / parser helpers | 8, 80, 89 | 逐块 |  | 未读 |
| `Source/Utils/WarpXMovingWindow.cpp` | 工具与算法选择 | constants / moving window / parser helpers | 8, 80, 89 | 逐块 | shiftMF, UpdateInjectionPosition, WarpX::MoveWindow, WarpX::ShiftGalileanBoundary, WarpX::ResetProbDomain | 未读 |
| `Source/Utils/WarpXUtil.H` | 工具与算法选择 | constants / moving window / parser helpers | 8, 80, 89 | 逐块 |  | 未读 |
| `Source/Utils/WarpXUtil.cpp` | 工具与算法选择 | constants / moving window / parser helpers | 8, 80, 89 | 逐块 | ReadBoostedFrameParameters, ConvertLabParamsToBoost, NullifyMFinstance, NullifyMF, CheckGriddingForRZSpectral, doCosts | 未读 |
| `Source/Utils/WarpXVersion.cpp` | 工具与算法选择 | constants / moving window / parser helpers | 8, 80, 89 | 逐块 | WarpX::Version, WarpX::PicsarVersion | 未读 |
| `Source/Utils/WarpX_Complex.H` | 工具与算法选择 | constants / moving window / parser helpers | 8, 80, 89 | 逐块 |  | 未读 |
| `Source/Utils/check_interp_points_and_weights.py` | 工具与算法选择 | constants / moving window / parser helpers | 8, 80, 89 | 逐块 | fine_grid_limits, coarse_grid_limits, coarsening_points_and_weights, refinement_points_and_weights | 未读 |
| `Source/WarpX.H` | WarpX 主类 | 全局状态 / 模块所有权 | 11 | 逐块 | WARPX_EXPORT, does, attribute, GetPartContainer, GetFluidContainer, GetElectrostaticSolver, GetMultiDiags, GetParticleBoundaryBuffer | 未读 |
| `Source/WarpX.cpp` | WarpX 主类 | 全局状态 / 初始化/析构 | 11 | 逐块 | AllocateCenteringCoefficients, SetDotMask, WarpX::MakeWarpX, WarpX::GetInstance, WarpX::ResetInstance, WarpX::Finalize, WarpX::ReadParameters, WarpX::BackwardCompatibility | 未读 |
| `Source/ablastr/CMakeLists.txt` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 |  | 未读 |
| `Source/ablastr/Make.package` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 |  | 未读 |
| `Source/ablastr/coarsen/CMakeLists.txt` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 |  | 未读 |
| `Source/ablastr/coarsen/Make.package` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 |  | 未读 |
| `Source/ablastr/coarsen/average.H` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 | Interp | 未读 |
| `Source/ablastr/coarsen/average.cpp` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 | Loop, Coarsen | 未读 |
| `Source/ablastr/coarsen/sample.H` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 | Interp | 未读 |
| `Source/ablastr/coarsen/sample.cpp` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 | Loop, Coarsen | 未读 |
| `Source/ablastr/constant.H` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 |  | 未读 |
| `Source/ablastr/fields/CMakeLists.txt` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 |  | 未读 |
| `Source/ablastr/fields/EffectivePotentialPoissonSolver.H` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 | computeEffectivePotentialPhi, constexpr | 未读 |
| `Source/ablastr/fields/IntegratedGreenFunctionSolver.H` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 | IntegratedPotential3D, IntegratedPotential2D, SumOfIntegratedPotential3D, SumOfIntegratedPotential2D | 未读 |
| `Source/ablastr/fields/IntegratedGreenFunctionSolver.cpp` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 | computePhiIGF | 未读 |
| `Source/ablastr/fields/Interpolate.H` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 | PoissonInterpCPtoFP | 未读 |
| `Source/ablastr/fields/Make.package` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 |  | 未读 |
| `Source/ablastr/fields/MultiFabRegister.H` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 | is_castable_to_string, class, Direction, to, is, MultiFabOwner, MultiFabRegister, getExtractedName | 未读 |
| `Source/ablastr/fields/MultiFabRegister.cpp` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 | MultiFabRegister::internal_alloc_init, MultiFabRegister::internal_alias_init, MultiFabRegister::remake_level, MultiFabRegister::internal_has, MultiFabRegister::internal_get, MultiFabRegister::internal_get_mr_levels, MultiFabRegister::internal_get_alldirs, MultiFabRegister::internal_get_mr_levels_alldirs | 未读 |
| `Source/ablastr/fields/PoissonSolver.H` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 | getMaxNormRho, interpolatePhiBetweenLevels, computePhi, constexpr | 未读 |
| `Source/ablastr/fields/VectorPoissonSolver.H` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 | computeVectorPotential, constexpr | 未读 |
| `Source/ablastr/math/CMakeLists.txt` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 |  | 未读 |
| `Source/ablastr/math/FiniteDifference.H` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 |  | 未读 |
| `Source/ablastr/math/FiniteDifference.cpp` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 | getFornbergStencilCoefficients, ReorderFornbergCoefficients | 未读 |
| `Source/ablastr/math/LinearInterpolation.H` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 | linear_interp, bilinear_interp, trilinear_interp | 未读 |
| `Source/ablastr/math/Make.package` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 |  | 未读 |
| `Source/ablastr/math/RandomSeed.H` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 |  | 未读 |
| `Source/ablastr/math/RandomSeed.cpp` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 | ablastr::math::set_random_seed | 未读 |
| `Source/ablastr/math/fft/AnyFFT.H` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 | struct, contains, FFTplan, multiply | 未读 |
| `Source/ablastr/math/fft/CMakeLists.txt` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 |  | 未读 |
| `Source/ablastr/math/fft/Make.package` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 |  | 未读 |
| `Source/ablastr/math/fft/WrapCuFFT.cpp` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 | setup, CreatePlan, DestroyPlan, Execute, cufftErrorToString | 未读 |
| `Source/ablastr/math/fft/WrapFFTW.cpp` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 | setup, CreatePlan, DestroyPlan, Execute | 未读 |
| `Source/ablastr/math/fft/WrapMklFFT.cpp` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 | setup, DestroyPlan, Execute | 未读 |
| `Source/ablastr/math/fft/WrapNoFFT.cpp` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 | setup | 未读 |
| `Source/ablastr/math/fft/WrapRocFFT.cpp` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 | setup, cleanup, assert_rocfft_status, CreatePlan, DestroyPlan, Execute, rocfftErrorToString | 未读 |
| `Source/ablastr/parallelization/CMakeLists.txt` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 |  | 未读 |
| `Source/ablastr/parallelization/KernelTimer.H` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 | KernelTimer | 未读 |
| `Source/ablastr/parallelization/MPIInitHelpers.H` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 |  | 未读 |
| `Source/ablastr/parallelization/MPIInitHelpers.cpp` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 | mpi_thread_required, mpi_init, mpi_finalize, check_mpi_thread_level | 未读 |
| `Source/ablastr/parallelization/Make.package` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 |  | 未读 |
| `Source/ablastr/particles/DepositCharge.H` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 | deposit_charge | 未读 |
| `Source/ablastr/particles/Make.package` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 |  | 未读 |
| `Source/ablastr/particles/NodalFieldGather.H` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 | constexpr | 未读 |
| `Source/ablastr/particles/ParticleMoments.H` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 | MinAndMaxPositions, MeanAndStdPositions | 未读 |
| `Source/ablastr/profiler/Make.package` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 |  | 未读 |
| `Source/ablastr/profiler/ProfilerWrapper.H` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 |  | 未读 |
| `Source/ablastr/utils/CMakeLists.txt` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 |  | 未读 |
| `Source/ablastr/utils/Communication.H` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 | FAB1, FAB2, mixedCopy | 未读 |
| `Source/ablastr/utils/Communication.cpp` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 | ParallelCopy, ParallelAdd, FillBoundary, SumBoundary, OverrideSync | 未读 |
| `Source/ablastr/utils/Enums.H` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 | struct | 未读 |
| `Source/ablastr/utils/Make.package` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 |  | 未读 |
| `Source/ablastr/utils/RelativeCellPosition.H` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 |  | 未读 |
| `Source/ablastr/utils/RelativeCellPosition.cpp` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 |  | 未读 |
| `Source/ablastr/utils/Serialization.H` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 | put_in, put_in_vec, constexpr, get_out_vec | 未读 |
| `Source/ablastr/utils/SignalHandling.H` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 | SignalHandling, signal_action_requested_labels | 未读 |
| `Source/ablastr/utils/SignalHandling.cpp` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 | sigaction, SignalHandling::parseSignalNameToNumber, SignalHandling::InitSignalHandling, SignalHandling::CheckSignals, SignalHandling::WaitSignals, SignalHandling::TestAndResetActionRequestFlag, SignalHandling::SignalSetFlag | 未读 |
| `Source/ablastr/utils/TextMsg.H` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 |  | 未读 |
| `Source/ablastr/utils/TextMsg.cpp` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 | Msg, ablastr::utils::TextMsg::Err, ablastr::utils::TextMsg::Info, ablastr::utils::TextMsg::Warn, ablastr::utils::TextMsg::Assert, ablastr::utils::TextMsg::Abort | 未读 |
| `Source/ablastr/utils/UsedInputsFile.H` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 |  | 未读 |
| `Source/ablastr/utils/UsedInputsFile.cpp` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 | ablastr::utils::write_used_inputs_file | 未读 |
| `Source/ablastr/utils/msg_logger/CMakeLists.txt` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 |  | 未读 |
| `Source/ablastr/utils/msg_logger/Make.package` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 |  | 未读 |
| `Source/ablastr/utils/msg_logger/MsgLogger.H` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 | class, represents, Msg, from, also, MsgWithCounter, MsgWithCounterAndRanks, is | 未读 |
| `Source/ablastr/utils/msg_logger/MsgLogger.cpp` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 | into, abl_msg_logger::PriorityToString, abl_msg_logger::StringToPriority, Msg::deserialize, MsgWithCounter::deserialize, MsgWithCounterAndRanks::deserialize, Logger::record_msg, Logger::collective_gather_msgs_with_counter_and_ranks | 未读 |
| `Source/ablastr/utils/msg_logger/MsgLogger_fwd.H` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 | class, Msg, MsgWithCounter, MsgWithCounterAndRanks, Logger | 未读 |
| `Source/ablastr/utils/text/CMakeLists.txt` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 |  | 未读 |
| `Source/ablastr/utils/text/Make.package` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 |  | 未读 |
| `Source/ablastr/utils/text/StreamUtils.H` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 |  | 未读 |
| `Source/ablastr/utils/text/StreamUtils.cpp` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 | ablastr::utils::text::goto_next_line | 未读 |
| `Source/ablastr/utils/text/StringUtils.H` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 | split_string | 未读 |
| `Source/ablastr/utils/text/StringUtils.cpp` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 | ablastr::utils::text::automatic_text_wrap | 未读 |
| `Source/ablastr/utils/timer/CMakeLists.txt` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 |  | 未读 |
| `Source/ablastr/utils/timer/Make.package` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 |  | 未读 |
| `Source/ablastr/utils/timer/Timer.H` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 | implements, Timer | 未读 |
| `Source/ablastr/utils/timer/Timer.cpp` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 |  | 未读 |
| `Source/ablastr/warn_manager/CMakeLists.txt` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 |  | 未读 |
| `Source/ablastr/warn_manager/Make.package` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 |  | 未读 |
| `Source/ablastr/warn_manager/WarnManager.H` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 | class, WarnManager, should | 未读 |
| `Source/ablastr/warn_manager/WarnManager.cpp` | ablastr 支撑层 | fields / particles / FFT / profiler / warnings | 71, 78, 107 | 文件级+关键内核 | MapPriorityToWarnPriority, WarnManager::GetInstance, WarnManager::RecordWarning, WarnManager::SetAlwaysWarnImmediately, WarnManager::SetAbortThreshold, WarnManager::debug_read_warnings_from_input, WarnManager::GetHeader, WarnManager::MsgFormatter | 未读 |
| `Source/main.cpp` | 程序入口 | 程序生命周期 / AMReX 初始化 | 10 | 逐行 | main | 未读 |

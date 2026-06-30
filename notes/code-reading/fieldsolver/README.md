# FieldSolver 源码精读入口

绑定源码：`../warpx/Source/FieldSolver`。

## 模块边界

- 构建入口：`FieldSolver/CMakeLists.txt`、`FieldSolver/Make.package`。
- 顶层入口：`WarpXPushFieldsEM.cpp`、`WarpXPushFieldsHybridPIC.cpp`、`WarpXSolveFieldsES.cpp`、`WarpX_QED_Field_Pushers.cpp`。
- 子模块：`FiniteDifferenceSolver/`、`SpectralSolver/`、`ElectrostaticSolvers/`、`MagnetostaticSolver/`、`ImplicitSolvers/`。

## 核心问题

- `EvolveE/B/F/G` 如何从 `WarpX::OneStep*` 分派到 FDTD、PSATD、PML 和 QED field push。
- FDTD curl、PSATD 谱更新、electrostatic Poisson、implicit residual 的离散公式是什么。
- field arrays 在 `fp/aux/cp`、rho/current、PML 和 guard cells 之间如何流动。

## 精读顺序

1. `00-fieldsolver-dispatch.md`：顶层 field push 入口、FDTD/PSATD 分派和 `EvolveE/B/F/G` 第一轮源码对应。
2. `01-fdtd-evolve-e-b.md`：FDTD solver 与 finite-difference algorithms，覆盖 Cartesian Yee/Nodal/CKC 差分算子。
3. `02-fdtd-pml.md`：FDTD PML split-field 更新、PML component 存储、`pml_has_particles` 电流项和 divergence cleaning 边界。
4. `03-pml-damping-current.md`：PML sigma profile、场 damping、电流 damping、regular/PML exchange。
5. `04-noncartesian-fdtd.md`：RZ/RCYLINDER/RSPHERE 的 cylindrical/spherical Yee 算子、mode decomposition 和轴上正则化。
6. `05-psatd-spectral-flow.md`：PSATD 主流程、FFT 数据容器、k-space、staggered shift 和 spectral algorithm 分派。
7. `06-psatd-galilean-current-correction.md`：标准/Galilean PSATD 系数、current correction 和 Vay spectral deposition。
8. `07-psatd-jrhom.md`：PSATD-JRhom 的 `psatd.JRhom` 参数、`OneStep_JRhom()` 多次源项沉积、谱数组时间层和一阶/二阶更新算法。
9. `08-psatd-rz-hankel.md`：RZ PSATD 的 Hankel transform、azimuthal modes、`Ep/Em` 谱更新、RZ current correction、Galilean RZ 和 RZ PML。
10. `09-electrostatic-magnetostatic.md`：静电 Poisson、relativistic self fields、effective potential、静磁 vector Poisson 和 `B=curl A`。
11. `11-psatd-coefficient-derivation.md`：`Tools/Algorithms/psatd.ipynb` 中 PSATD 线性系统、齐次/非齐次解、源项多项式与系数表抽取。
12. `NonlinearSolvers/` 的 `00-solver-abstractions.md`、`01-newton-picard.md`、`02-preconditioners-and-petsc.md`。
13. `12-hybrid-pic-model-deep-dive.md`：Hybrid PIC 的广义 Ohm 定律、离子/电子电流分裂、B 场 RK 子步、电子压力闭合和外部矢势分裂场。
14. `13-fieldsolver-verification-map.md`：FieldSolver 相关 regression tests 的输入文件、分析脚本、checksum 和覆盖关系索引。
15. `14-fieldsolver-analysis-criteria.md`：FieldSolver 相关 regression analysis 脚本的实际物理判据、容差、源码覆盖和“assert / checksum / 可视化”分层。
16. `15-implicit-jacobian-preconditioner-coupling.md`：`J0 + MM*(E-E0)`、`MassMatrices_PC`、`PreLinearSolve()` 和 `MatrixPC/JacobiPC/CurlCurlMLMGPC` 的消费链。
17. `16-psatd-pml-coefficient-atlas.md`：`PsatdAlgorithmPml.cpp` 中 `C1-C25`、Galilean `T2`、cleaning 分支和 PML regression 的源码系数图谱。
18. `17-psatd-x-coefficients.md`：Cartesian `PsatdAlgorithmGalilean.cpp` 中 `X1-X4`、`T2`、standard/Galilean 极限和 update placement 的源码公式图谱。
19. `18-psatd-time-averaging-coefficients.md`：Cartesian `PsatdAlgorithmGalilean.cpp` 中 time-averaged field 的 `Psi1/Psi2/Y1-Y4`、零模处理、average-field 更新式和实空间回填路径。
20. `19-psatd-jrhom-y-coefficients.md`：Cartesian `PsatdAlgorithmJRhomSecondOrder.cpp` 中 `Y1-Y8`、多项式源项积分、零模处理、ordinary field push 和 time-averaged field 累计路径。
21. `20-psatd-rz-galilean-rz-coefficients.md`：standard RZ `C/S_ck/X1-X3/X5-X6`、Galilean RZ `X1-X4/Theta2/T_rho`、`Ep/Em` 字段布局和 RZ current-correction 边界。
22. `21-psatd-comoving-coefficients.md`：regular-domain comoving PSATD 的分派优先级、`X1-X4/Theta2` 系数、current correction、参数限制和 checksum-only regression 边界。
23. `22-psatd-comoving-regression-analysis-plan.md`：`test_2d_comoving_psatd_hybrid` 的现有 checksum 边界、可直接实现的 field-energy sanity analysis、需要 `divE` 输出后才能做的 Gauss-law diagnostic 和 CMake patch 草案。
24. `23-psatd-comoving-reference-calibration.md`：把 comoving `analysis_comoving.py` 从方案推进到可提交 patch 的 reference 标定、unstable contrast、provenance 和 patch 四件套清单。
25. `24-psatd-comoving-first-stage-patch-draft.md`：把当前已验证的 `finite + spike` fallback 收成更接近 WarpX 提交流的第一阶段 patch 草案，并附上最小 helper 资产 `analysis_comoving_first_stage_draft.py`、unified diff 草案 `comoving_first_stage_patch.diff` 以及对应的 ledger 驱动生成脚本 `scripts/build_comoving_first_stage_patch.py`。
26. implicit solver 的接口细化和正文持续回填。

## 输出目标

- `00-fieldsolver-dispatch.md`：已建立，覆盖 `WarpXPushFieldsEM.cpp`、`FiniteDifferenceSolver/EvolveB.cpp`、`EvolveE.cpp`、`EvolveF.cpp`、`EvolveG.cpp`。
- `01-fdtd-evolve-e-b.md`：已建立，覆盖 `CartesianYeeAlgorithm.H`、`CartesianNodalAlgorithm.H`、`CartesianCKCAlgorithm.H` 与 `FiniteDifferenceSolver.cpp` 系数初始化。
- `02-fdtd-pml.md`：已建立，覆盖 `EvolveBPML.cpp`、`EvolveEPML.cpp`、`EvolveFPML.cpp`、`BoundaryConditions/PMLComponent.H` 和 PML 参数/理论文档。
- `03-pml-damping-current.md`：已建立，覆盖 `PML.cpp`、`PML.H`、`WarpXEvolvePML.cpp`、`WarpX_PML_kernels.H` 和 `PML_current.H`。
- `04-noncartesian-fdtd.md`：已建立，覆盖 `CylindricalYeeAlgorithm.H`、`SphericalYeeAlgorithm.H`、`EvolveB/E/F.cpp` 与 `ComputeDivE.cpp` 的 RZ/RCYLINDER/RSPHERE 分支。
- `05-psatd-spectral-flow.md`：已建立，覆盖 `WarpXPushFieldsEM.cpp::PushPSATD()`、`SpectralSolver.cpp`、`SpectralFieldData.cpp`、`SpectralKSpace.cpp`、`SpectralBaseAlgorithm.H` 和 `PsatdAlgorithmGalilean.cpp` 主更新框架。
- `06-psatd-galilean-current-correction.md`：已建立，覆盖 `PsatdAlgorithmGalilean.H/.cpp` 的 `C/S_ck/T2/X1-X4`、averaging 系数入口、`CurrentCorrection()` 和 `VayDeposition()`。
- `07-psatd-jrhom.md`：已建立，覆盖 `WarpXEvolve.cpp::OneStep_JRhom()`、`WarpX.cpp` 的 `psatd.JRhom` 参数约束、`SpectralFieldData.cpp` 时间层索引、`PsatdAlgorithmJRhomFirstOrder.cpp` 和 `PsatdAlgorithmJRhomSecondOrder.cpp`。
- `08-psatd-rz-hankel.md`：已建立，覆盖 `SpectralSolverRZ.cpp`、`SpectralFieldDataRZ.cpp`、`SpectralKSpaceRZ.cpp`、`SpectralHankelTransformer.cpp`、`HankelTransform.cpp`、`PsatdAlgorithmRZ.cpp`、`PsatdAlgorithmGalileanRZ.cpp` 和 `PsatdAlgorithmPmlRZ.cpp`。
- `09-electrostatic-magnetostatic.md`：已建立，覆盖 `WarpXSolveFieldsES.cpp`、`ElectrostaticSolvers/*`、`MagnetostaticSolver/*`、`WarpX.cpp` 的 electrostatic 参数/对象/field allocation 分支和官方 electrostatic PIC 文档。
- `10-implicit-and-hybrid.md`：已建立，覆盖 `WarpX.cpp` 的 `evolve_scheme` implicit 选择、`ImplicitSolver*` 抽象、`ThetaImplicitEM`、`SemiImplicitEM`、`StrangImplicitSpectralEM`、`WarpXSolverVec/DOF`、`WarpXPushFieldsHybridPIC.cpp` 和 `HybridPICModel/*`。
- `11-psatd-coefficient-derivation.md`：已建立，覆盖 `Tools/Algorithms/psatd.ipynb` 的 PSATD 线性系统、齐次/非齐次解、源项多项式、系数表抽取和与 `PsatdAlgorithm*` 的对应关系。
- `12-hybrid-pic-model-deep-dive.md`：已建立，覆盖 `WarpXPushFieldsHybridPIC.cpp`、`HybridPICModel.*`、`ExternalVectorPotential.*`、`HybridPICSolveE.cpp` 和 kinetic-fluid hybrid 官方理论文档。
- `13-fieldsolver-verification-map.md`：已建立，覆盖 `nci_fdtd_stability`、`nci_psatd_stability`、`electrostatic_sphere`、`implicit` 和 `ohm_solver_*` 的 CMake 注册、输入文件、分析脚本与 checksum 路径。
- `14-fieldsolver-analysis-criteria.md`：已建立，覆盖 NCI FDTD/PSATD、electrostatic sphere、implicit EM 和 hybrid Ohm solver 的 analysis 判据；明确当前只读脚本与源码，未运行本地 regression。
- `15-implicit-jacobian-preconditioner-coupling.md`：已建立，覆盖 `ImplicitSolver::InitializeMassMatrices()`、`PreLinearSolve()`、`ComputeJfromMassMatrices()`、`SyncMassMatricesPCAndApplyBCs()`、`SetMassMatricesForPC()` 以及 `MatrixPC`、`JacobiPC`、`CurlCurlMLMGPC` 对 `MassMatrices_PC` 的消费方式。
- `16-psatd-pml-coefficient-atlas.md`：已建立，覆盖 `PsatdAlgorithmPml.cpp` 的共享谱量、`C1-C9` 投影系数、`C10-C22` 无 cleaning 交叉耦合、`C23-C25` cleaning 耦合和 PML PSATD regression 映射。
- `17-psatd-x-coefficients.md`：已建立，覆盖 Cartesian `PsatdAlgorithmGalilean.cpp` 的 `X1-X4` 源码公式、标准/Galilean 极限、零模处理和 E/B 更新式中的位置。
- `18-psatd-time-averaging-coefficients.md`：已建立，覆盖 Cartesian `PsatdAlgorithmGalilean.cpp` 的 `Psi1/Psi2/Y1-Y4` 源码公式、零模处理、average-field 更新式、`update_with_rho` 前置条件和 `PSATDScaleAverageFields()/PSATDBackwardTransformEBavg()` 回填路径。
- `19-psatd-jrhom-y-coefficients.md`：已建立，覆盖 Cartesian `PsatdAlgorithmJRhomSecondOrder.cpp` 的 `Y1-Y8` 源码公式、零模处理、`a/b/c` 多项式源项、ordinary `E/B/F` 推进、time-averaged field 累计和防混写边界。
- `20-psatd-rz-galilean-rz-coefficients.md`：已建立，覆盖 standard RZ `C/S_ck/X1-X3/X5-X6`、Galilean RZ `X1-X4/Theta2/T_rho`、`Ep/Em` 字段布局、linear-J time averaging 限制、RZ current correction 和防混写边界。
- `21-psatd-comoving-coefficients.md`：已建立，覆盖 regular-domain comoving PSATD 的 `v_comoving` 分派优先级、direct deposition/update-with-rho 限制、`X1-X4/Theta2` 一般分支与特殊极限、comoving current correction 和 `test_2d_comoving_psatd_hybrid` 的 checksum-only 验证边界。
- `22-psatd-comoving-regression-analysis-plan.md`：已建立，覆盖 `test_2d_comoving_psatd_hybrid` 当前 `analysis=OFF` 的证据边界、现有 `Ex/Ey/Ez/B/J/rho` 输出可支持的 finite/energy/spike gate、缺少 `divE` 时不能声称 charge-conservation analysis，以及后续 CMake wiring 草案。
- `23-psatd-comoving-reference-calibration.md`：已建立，覆盖 `analysis_galilean.py` / `analysis_psatd_CC1.py` 可复用的 reference 模式、comoving `energy_ref` 不应借用 Galilean 数值、stable ledger vs unstable contrast 的标定流程，以及真正提交 WarpX patch 时应附带的 provenance note。
- `24-psatd-comoving-first-stage-patch-draft.md`：已建立，覆盖当前更接近 WarpX 提交流的第一阶段 `finite + spike` patch 形状、CMake wiring 草案、候选 `SPIKE_RATIO_MAX` 常量、配套 unified diff 草案、ledger 驱动重建脚本，以及为什么第一阶段故意不带 energy gate。
- 重写 `manuscript/chapters/06-field-solvers.md`。

## 验证线索

- `Examples/Tests/langmuir/`
- `Examples/Tests/electrostatic_sphere/`
- `Examples/Tests/implicit/`
- `Examples/Tests/nci_fdtd_stability/`
- `Examples/Tests/nci_psatd_stability/`

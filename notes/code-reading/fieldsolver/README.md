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
25. `24-psatd-comoving-first-stage-patch-draft.md`：把当前已验证的 `finite + spike` fallback 收成更接近 WarpX 提交流的第一阶段 patch 草案，并附上最小 helper 资产 `analysis_comoving_first_stage_draft.py`、unified diff 草案 `comoving_first_stage_patch.diff`、自动生成的 `comoving_first_stage_provenance_note.md`、`comoving_first_stage_submission_packet.md`、`comoving_first_stage_pr_draft.md` 与 `comoving_first_stage_bundle/` staging bundle，以及对应的 ledger 驱动生成脚本 `scripts/build_comoving_first_stage_patch.py`、目标 worktree 安装脚本 `scripts/stage_comoving_first_stage_patch.py`、只读审计脚本 `scripts/audit_comoving_first_stage_patch.py`、预检报告脚本 `scripts/report_comoving_first_stage_patch.py` 和只读 diff 预览脚本 `scripts/preview_comoving_first_stage_patch.py`。
26. `25-psatd-comoving-velocity-candidate-scan.md`：只沿 `v_comoving` 路径做本地 sibling 扫描，比较 stable / explicit-default / half-default / zero / positive-default 五条 velocity 候选，明确说明 default selector 不是隐藏变量、velocity-only sibling 仍不能形成 local energy ordering，而反号 `v_comoving` 只会显著抬高 spike。
27. `26-rz-psatd-validation-strong-criteria.md`：把当前 WarpX 源码树里 RZ PSATD 的 active validation 主线收成“强 analysis / 弱 analysis / checksum-only”判据表，明确指出 `test_rz_galilean_psatd*`、`test_rz_langmuir_multi_psatd*` 和 `test_rz_pml_psatd` 分别支撑哪类强论断，以及 `test_rz_psatd_JRhom_LL2` 仍缺独立 main analysis。
28. `27-rz-jrhom-ll2-analysis-direction.md`：判定 `test_rz_psatd_JRhom_LL2` 下一步更适合补哪类独立 main analysis，结论是优先走 `analysis_psatd_CC1.py` / `analysis_galilean.py` 风格的 stability-style 末态 field-energy gate，而不是直接套 Langmuir 的解析场 gate。
29. `28-rz-jrhom-reference-sibling-scan.md`：把 `test_rz_psatd_JRhom_LL2` 的 reference sibling 搜索收成可执行脚本骨架，新增 RZ 专用 ledger builder 和 candidate scan 脚本，优先比较 `JRhom / time_averaging / cleaning` 三组最小改动候选。
30. `29-rz-jrhom-first-stage-helper.md`：把 RZ JRhom LL2 第一阶段 helper 原型落成 `scripts/analysis_rz_jrhom.py`，默认收成 `finite + energy`，并把 `spike` 保留为可选增强项。
31. `30-rz-jrhom-input-numprocs-audit.md`：审计输入卡原生 `warpx.numprocs = 1 2` 在当前本机调用方式下的行为，确认当前 blocker 是 process-count mismatch，而不是 energy ordering 漂移；同时补入 scan 脚本的 `--numprocs-override` / `--command-prefix` 接口，并继续记录后续 `mpiexec -n 2` repeated/MPI 复核。
32. `31-rz-jrhom-first-stage-patch-draft.md`：把当前已通过 repeated/MPI 复核的 `finite + energy` helper 收成更接近 WarpX 提交流的第一阶段 patch 草案，并附上 helper/diff/provenance packet/PR draft/bundle 与对应生成脚本 `scripts/build_rz_jrhom_first_stage_patch.py`。
33. `32-rz-jrhom-target-checkout-workflow.md`：把 RZ JRhom first-stage bundle 再推进到目标 worktree 级别，新增目标 worktree 安装脚本 `scripts/stage_rz_jrhom_first_stage_patch.py`、只读审计脚本 `scripts/audit_rz_jrhom_first_stage_patch.py`、预检报告脚本 `scripts/report_rz_jrhom_first_stage_patch.py` 和只读 diff 预览脚本 `scripts/preview_rz_jrhom_first_stage_patch.py`。
34. implicit solver 的接口细化和正文持续回填。

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
- `24-psatd-comoving-first-stage-patch-draft.md`：已建立，覆盖当前更接近 WarpX 提交流的第一阶段 `finite + spike` patch 形状、CMake wiring 草案、候选 `SPIKE_RATIO_MAX` 常量、配套 unified diff 草案、自动生成的 provenance note / submission packet / PR draft / staging bundle、ledger 驱动重建脚本、目标 worktree 安装脚本、只读审计脚本、预检报告脚本、只读 diff 预览脚本，以及为什么第一阶段故意不带 energy gate。
- `25-psatd-comoving-velocity-candidate-scan.md`：已建立，覆盖 `v_comoving` 本地 sibling 扫描、`explicit-default-beta/half-default-beta/positive-default-beta` 三条新增候选、`comoving-velocity-scan.{md,json}` 汇总，以及为什么这轮结果进一步支持第一阶段 patch 收敛到 `finite + spike`。
- `26-rz-psatd-validation-strong-criteria.md`：已建立，覆盖 RZ Galilean/current-correction/PSB、RZ Langmuir PSATD、RZ PML PSATD 三条强 validation 主线，以及 `test_rz_psatd_JRhom_LL2` 仍是 checksum-only 的当前缺口。
- `27-rz-jrhom-ll2-analysis-direction.md`：已建立，覆盖为什么 `test_rz_psatd_JRhom_LL2` 更适合优先补 stability-style 末态 field-energy gate，而不是直接套解析 `Er/Ez` gate，以及第一阶段 reference sibling 应如何找。
- `28-rz-jrhom-reference-sibling-scan.md`：已建立，覆盖 RZ 专用 reference-ledger builder、`scan_rz_jrhom_reference_candidates.py` 的五条候选 sibling，以及后续如何把第一轮 energy/spike ordering 接成独立 main analysis。
- `29-rz-jrhom-first-stage-helper.md`：已建立，覆盖 `analysis_rz_jrhom.py` 的第一阶段 `finite + energy` helper 形态、baseline/reference 阈值导出方式、可选 spike gate 和当前 provenance 边界。
- `30-rz-jrhom-input-numprocs-audit.md`：已建立，覆盖输入卡原生 `warpx.numprocs = 1 2` 的当前本机审计、为什么 plain single-process 调用会统一触发 `process_count_mismatch`，以及后续 repeated/MPI 复核需要的 launcher 前提。
- `31-rz-jrhom-first-stage-patch-draft.md`：已建立，覆盖 `finite + energy` 第一阶段 patch 草案、候选 `ENERGY_REF/TOL_ENERGY` 常量、最小 CMake wiring、helper/diff/provenance/submission packet/PR draft/bundle 资产，以及为什么当前故意不带 spike gate。
- `32-rz-jrhom-target-checkout-workflow.md`：已建立，覆盖 RZ JRhom first-stage bundle 的 preview/audit/report/stage 四脚本、目标 checkout 的 `unstaged / partial / staged` 三档状态，以及为什么这一轮收口的是“可对目标 worktree 落地的工程链路”，而不是继续增加新的 physics gate。
- 重写 `manuscript/chapters/06-field-solvers.md`。

## 验证线索

- `Examples/Tests/langmuir/`
- `Examples/Tests/electrostatic_sphere/`
- `Examples/Tests/implicit/`
- `Examples/Tests/nci_fdtd_stability/`
- `Examples/Tests/nci_psatd_stability/`

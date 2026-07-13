# RZ axis charge source-diagnostic crosswalk

## 结论

v0.94 把当前 RZ axis residual 的源码边界固定为：

`particle deposition -> rho inverse-volume scaling` 与 `E -> divE solver diagnostic` 是两条不同的消费者路径。`rho` 和 `divE` 最后才在 reader-side contract 中被比较，因此重复稳定性可以固定 observable，却不能单凭 residual 把根因归到 deposition kernel。

源码合同由 `scripts/audit_rz_axis_charge_source_crosswalk.py` 执行，当前 checkout 的 WarpX 通过 `12/12` 个 anchors。

## 1. rho 路径

- `Source/Particles/PhysicalParticleContainer.cpp` 将粒子写入 `rho_fp`；transition-zone 粒子直接写入 coarse-geometry 的 `rho_buf`。
- `Source/Evolve/WarpXEvolve.cpp` 在所有粒子完成 charge/current deposition 后调用 `ApplyInverseVolumeScalingToChargeDensity(...)`。
- `Source/FieldSolver/WarpXPushFieldsEM.cpp` 使用 `boundary.verboncoeur_axis_correction` 选择 RZ axis volume factor：开启时为 `1/3`，关闭时为 `1/4`。
- `rho_buf` 使用 `lev-1` 的几何级别做相同外层修正。

这说明 axis correction 不是 `ChargeDeposition.H` 内部 shape 写入的局部开关，而是沉积完成后的几何归一化步骤。

## 2. divE 路径

- `Source/WarpX.cpp::ComputeDivE()` 根据 solver 选择 FDTD 或 PSATD，从 `Efield_aux` 计算临时 `divE`。
- `Source/Diagnostics/ComputeDiagFunctors/DivEFunctor.cpp` 决定 RZ temporary field 的 cell/node location，并将结果 coarsen 到 diagnostic output。
- `Source/Diagnostics/ComputeDiagFunctors/RhoFunctor.cpp` 重新调用 `GetChargeDensity(...)`，执行 boundary/filter 处理，再 `InterpolateMFForDiag(...)`。
- `Source/Diagnostics/FullDiagnostics.cpp` 把 `divE` 与 `rho` 注册为两个独立 functor。

因此 `divE-rho/epsilon_0` 的同面 residual 还混合了 solver divergence stencil、RZ location conversion、mode handling、rho-side volume scaling 以及 diagnostic coarsen/interpolation。当前证据支持 `SOURCE_DIAGNOSTIC_DISCRETIZATION_BOUNDARY`，不支持 `KERNEL_ROOT_CAUSE`。

## 3. 与运行证据的关系

v0.93 的两组 resolution family 显示 correction-on axis residual 在重复运行中稳定，并且显著高于 off-axis；这把问题从“随机运行噪声”收窄到稳定的轴/诊断边界。但 source crosswalk 仍没有证明哪一个离散算子占主导，也没有关闭 `PHYSICS-RZ-AXIS-CHARGE`。

下一步应是设计能分别消费同一面上的 raw rho、volume-scaled rho、solver-native divE 和 diagnostic-converted divE 的独立输出；在拿到这四类中间量前，不应把章节结论升级成 deposition kernel root cause。

## 4. 可复核产物

- JSON/Markdown contract：`runs/stage-c-validation/rz-axis-charge-source-diagnostic-crosswalk-v0.94/contract.{json,md}`
- 书稿引用：`manuscript/chapters/05-deposition-shapes.md` 与 `manuscript/chapters/09-literature-roadmap.md`
- 缺口登记：`docs/current-book-gap-register.md`

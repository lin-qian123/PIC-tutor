# RZ axis divergence stencil alignment

本轮沿 `DivEFunctor -> WarpX::ComputeDivE -> FiniteDifferenceSolver::ComputeDivECylindrical` 继续下钻。当前 RZ CKC/Yee 分支在 axis mode-0 使用

$$
\operatorname{div} E\big|_{r=0}=\frac{4E_r}{\Delta r}+D_z E_z,
$$

而不是普通连续近似中容易写成的 `2*Er/dr + Dz(Ez)`。独立 reader `scripts/analyze_rz_axis_divergence_stencil_contract.py` 从现有 correction-on/off `256x512` 末态读取 axis `Er/Ez/divE`，使用同一阶的纵向差分消去 `Dz(Ez)`，再比较两个径向系数。

结果显示 source-defined `4*Er/dr` 在 correction-on 与 correction-off 两个 case 中的 RMSE 都低于 naive `2*Er/dr`：

| case | naive `2*Er/dr` RMSE | source `4*Er/dr` RMSE |
|---|---:|---:|
| correction-on | `2.5968e14` | `1.7287e13` |
| correction-off | `2.5999e14` | `1.2638e14` |

合同分类为 `RZ_AXIS_STENCIL_ALIGNMENT_OBSERVED_CHARGE_BOUNDARY_OPEN`。它把 axis residual 的解释进一步收窄到“诊断输出包含 source-defined axis divergence stencil，不能用朴素 cell-centered 连续算子反推 root cause”；它仍不证明 rho inverse-volume scaling、沉积 kernel 或完整 charge closure 已正确。报告见 `runs/stage-c-validation/rz-axis-divergence-stencil-v0.98/contract.{json,md}`。

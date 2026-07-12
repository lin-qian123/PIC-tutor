# RZ + Esirkepov charge residual boundary

## 结论

当前 checkout 的官方 RZ Langmuir 输入明确使用：

- `geometry.dims = RZ`
- `algo.current_deposition = esirkepov`
- `algo.particle_shape = 1`
- `warpx.do_dive_cleaning = 1`

本项目在 case-local overlay 中额外输出 `rho` 和 `divE`，2-rank 运行结果为：

- `Er` 相对解析场误差：`1.075e-2 < 0.12`
- `Ez` 相对解析场误差：`8.240e-3 < 0.12`
- 同面 `max|divE-rho/epsilon0| / max|rho/epsilon0|`：`3.593e-3 > 1e-11`

因此当前合同是 **field PASS、charge BOUNDARY**，不能写成 RZ Esirkepov 强守恒闭合。

## 为什么官方不把它作为强 gate

WarpX 官方 `Examples/Tests/langmuir/analysis_utils.py` 明确把 `geometry.dims=RZ` 从 Esirkepov charge-conservation check 中排除，并注明该组合当前会产生较大的数值误差，需要进一步调查。这个项目结果与该上游边界一致，而不是把官方没有执行的 gate 误写成通过。

## 当前源码语义

1. `Source/WarpX.cpp:3328-3341` 的 `WarpX::ComputeDivE()` 对非-PSATD 路径调用 `m_fdtd_solver_fp[lev]->ComputeDivE(...)`。
2. `Source/Diagnostics/ComputeDiagFunctors/DivEFunctor.cpp:38-51` 在非-PSATD RZ 选择 node-centered temporary `divE`，随后在 `:68-74` 经过 diagnostic coarsen/copy。
3. `Source/Diagnostics/ComputeDiagFunctors/RhoFunctor.cpp:35-66` 重新通过 `GetChargeDensity(m_lev, true)` 得到 rho，再执行 `ApplyFilterandSumBoundaryRho` 和 `InterpolateMFForDiag`。
4. `Source/Diagnostics/FullDiagnostics.cpp:525-530` 和 `:642-653` 分别把 `divE` 与 `rho` 接到不同 functor；它们不是同一个 field MultiFab 的两个直接视图。

所以当前 `3.593e-3` 是一个 reader-side same-surface diagnostic residual。它足以证明该组合不能进入 `1e-11` 强 gate，但仅凭这个 residual 不能区分 RZ stagger/interpolation、mode treatment、inverse-volume 或 current kernel 哪一层贡献最大。

## Cleaning 对照

在保持 RZ、Esirkepov、shape=1、网格、步数和 2-rank launcher 不变的条件下，将 `warpx.do_dive_cleaning` 从 `1` 改为 `0` 做 case-local sibling：

| case | `Er` error | `Ez` error | charge residual |
|---|---:|---:|---:|
| cleaning on | `1.075e-2` | `8.240e-3` | `3.593e-3` |
| cleaning off | `2.427e-2` | `4.941e-3` | `9.693e-2` |

进一步按第一径向 cell 分层：cleaning on 的 axis/off-axis residual 为 `3.593e-3/4.293e-4`，cleaning off 为 `9.693e-2/6.540e-12`。两个 case 的全局最大值都由 axis cell 主导。关闭 cleaning 后全局 residual 约为开启时的 `26.98` 倍，说明该 reader-side boundary 同时对轴处理和 cleaning 路径敏感；但它没有把全局 residual 降到强 gate，也没有证明 cleaning 是唯一根因。因此当前最准确的分类是 `AXIS_DOMINATED_CLEANING_SENSITIVE_DIAGNOSTIC_BOUNDARY`，比较报告见 `runs/stage-c-validation/esirkepov_langmuir_rz_cleaning-comparison/contract.{json,md}`。

## Verboncoeur axis correction 对照

当前源码和官方参数文档还提供了更直接的轴控制：`boundary.verboncoeur_axis_correction` 默认是 `true`。`Source/FieldSolver/WarpXPushFieldsEM.cpp:1770-1774` 对 RZ charge density 使用 `1/3`（开启）或 `1/4`（关闭）的 axis volume factor。保持其他输入完全不变，关闭该开关的 case-local sibling 得到：

| case | `Er` error | `Ez` error | all-cell charge residual | off-axis residual |
|---|---:|---:|---:|---:|
| correction on | `1.075e-2` | `8.240e-3` | `3.593e-3` | `4.293e-4` |
| correction off | `4.280e-2` | `9.480e-3` | `5.513e-12` | `1.720e-12` |

在本 case 的 `1e-11` gate 下，关闭 correction 恢复了 charge contract，同时 field error 仍低于 `0.12`。这证明当前 residual 与 axis volume correction 强相关，但不证明全局默认值应被修改：该开关是物理/几何约定的一部分，仍需针对均匀密度、RZ modes 和不同诊断 surface 做独立验证。对照报告见 `runs/stage-c-validation/esirkepov_langmuir_rz_axis-correction-comparison/contract.{json,md}`，分类为 `AXIS_CORRECTION_OFF_RESTORES_CHARGE_GATE`。

shape 交叉对照显示，这个结论不能无条件推广到高阶 shape：shape=2/3/4 在 correction off 下的 charge residual 分别为 `2.202e-12/2.103e-12/2.063e-12`，但 `Er` field error 分别升到 `0.132/0.173/0.213`，超过 `0.12` field gate；因此 correction off 对高阶 shape 形成 charge/field tradeoff。完整矩阵见 `runs/stage-c-validation/esirkepov_langmuir_rz_shape-axis-matrix/contract.{json,md}`，分类为 `AXIS_CORRECTION_CHARGE_FIELD_TRADEOFF_BY_SHAPE`。

## 可复现入口

```bash
python scripts/analyze_esirkepov_rz_langmuir_contract.py \
  --run-dir runs/stage-c-validation/esirkepov_langmuir_rz_mpi2 \
  --output-json runs/stage-c-validation/esirkepov_langmuir_rz_mpi2/contract.json \
  --output-md runs/stage-c-validation/esirkepov_langmuir_rz_mpi2/contract.md
```

该脚本把 field failure 作为失败退出，把 charge residual 超过强 gate 保留为 `BOUNDARY`，从而不会因为 RZ 诊断边界而伪造一个绿色守恒结论。

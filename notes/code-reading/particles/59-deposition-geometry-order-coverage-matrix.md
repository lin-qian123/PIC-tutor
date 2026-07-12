# Deposition geometry/order 覆盖矩阵

第 5 章已经积累了多条 deposition runtime 和 source contract，但它们分散在不同报告中。本 note 将当前最强证据按 family、geometry、shape/order 和证据范围并排整理，避免把局部 PASS 外推成全组合覆盖。可执行生成器为 `scripts/summarize_deposition_geometry_order_coverage.py`，报告归档于 `runs/stage-c-validation/deposition-geometry-order-coverage-matrix/coverage-matrix.{json,md}`。

## 当前矩阵

| family | geometry | shape/order | 当前证据 | 证据范围 |
|---|---|---:|---|---|
| Esirkepov | `1D_Z` | 1 | field + charge PASS | Langmuir |
| Esirkepov | `XZ` | 1/2/3/4 | field + charge PASS | 2D Langmuir siblings |
| Esirkepov | `3D` | 1/2/3/4 | `64^3` shape=1/2 field + charge PASS、shape=3/4 field BOUNDARY；`128^3` refined shape=3/4 field + charge PASS | Langmuir base + refined controls |
| Esirkepov | `XZ + AMR` | 1 | field PASS；level charge BOUNDARY | 2D MR overlay |
| Esirkepov | `RZ` | 1/2/3/4 | field PASS；correction-on charge BOUNDARY；correction-off refined PASS | axis correction/resolution family |
| Esirkepov | `RCYLINDER/RSPHERE` | 1/2/3/4 | radial `Er` PASS | 不含完整 charge/Gauss-law |
| Villasenor implicit | `XZ` | 2 | energy + Gauss-law PASS | native/filtered/PICMI siblings |
| Villasenor implicit | `XZ` | 4 | cropping Gauss-law PASS | near-boundary cropping |
| Villasenor implicit | `RZ` | 2 | build/runtime BOUNDARY | 未进入物理计算 |

## 明确缺口

- RZ correction-on charge/Gauss-law 仍是 axis-dominated diagnostic boundary；field PASS 不能升级成 charge PASS。
- RCYLINDER/RSPHERE 的 shape=1/2/3/4 矩阵只覆盖径向 `Er`，不覆盖完整 charge/Gauss-law。
- 2D MR 的 `rho/divE` 逐层结果不能替代 route-count、intermediate-field 或 coarse-fine source ledger。
- RZ implicit Villasenor 当前受 PETSc 缺失和 `amrex_gmres` control 的 `SIGILL` 阻断，不能写成 physics pass/fail。
- 3D Esirkepov shape=2 已有 field + charge PASS；shape=3/4 的 `64^3` field boundary 在 `128^3` refined controls 中消失，但只有一组 refined pair，不能包装成正式 convergence order；完整 geometry/order Cartesian product 仍未声明覆盖。

因此，矩阵的用途是约束成书措辞：它可以回答“哪类证据已经存在”，但不能回答“所有组合都已验证”。源码分派合同、runtime field contract、charge contract、AMR route contract 和 implicit solver build contract 必须继续分层引用。

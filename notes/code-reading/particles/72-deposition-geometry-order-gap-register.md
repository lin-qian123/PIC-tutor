# 第 5 章 deposition geometry/order 缺口台账

本 note 把 `notes/code-reading/particles/59-deposition-geometry-order-coverage-matrix.md` 中的未闭合项提升为一个 **negative-space contract**：它检查缺口是否被明确命名、分类和接上下一步证据入口，而不是把“当前没有失败日志”误读成 PASS。

台账原则：不把缺口写成 PASS。

审计脚本：`scripts/audit_deposition_geometry_order_gap_register.py`

## 台账

| ID | 当前分类 | 下一步证据入口 |
|---|---|---|
| `rz_correction_on_charge` | `BOUNDARY` | 分离 axis-volume 与诊断路径，再讨论默认参数 |
| `radial_charge_gauss_law` | `BOUNDARY` | 建立 geometry-specific charge/Gauss-law consumer |
| `amr_route_count` | `UNPROVEN` | 接入真实 intermediate-field/route ledger |
| `rz_implicit_villasenor` | `PRE_PHYSICS_BOUNDARY` | 取得兼容 PETSc/AMReX build 后重跑 |
| `villasenor_geometry_order` | `PARTIAL` | 每次增加一个带独立 consumer 的 sibling |
| `vay_geometry_order` | `PARTIAL` | 已完成 2D/3D shape=1..4 的 2-rank Cartesian case-local family；AMR 当前由 source guard 明确拒绝，边界和完整几何组合仍待补 |
| `formal_convergence_order` | `UNPROVEN` | 固定 observable、误差范数和 resolution family 后做 study |

## 使用边界

- 这是一份缺口台账，不是 runtime PASS 清单。
- source crosswalk 只能证明入口仍存在；coverage matrix 只能证明已有证据如何分布。
- 只有带有明确 producer、consumer、输入和误差判据的 case-local contract，才可以关闭对应 runtime 缺口。
- `Esirkepov 2001` CPC 定稿 PDF 的 publisher compare 仍是独立的文献缺口，不与本台账混并。

## 可重放命令

```bash
python scripts/audit_deposition_geometry_order_gap_register.py \
  --project-root . \
  --output-json runs/stage-c-validation/deposition-geometry-order-gap-register/contract.json \
  --output-md runs/stage-c-validation/deposition-geometry-order-gap-register/contract.md
```

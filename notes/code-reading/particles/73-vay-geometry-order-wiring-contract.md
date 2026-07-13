# Vay deposition geometry/order official wiring contract

审计脚本：`scripts/audit_vay_geometry_order_wiring.py`

## 当前已接通的入口

只读核对当前 WarpX 官方测试目录后，Vay 的公开 wiring 可以具体写成：

| geometry/order | 官方入口 | consumer | 当前边界 |
|---|---|---|---|
| 2D Cartesian, shape=3 | `Examples/Tests/vay_deposition/inputs_test_2d_vay_deposition` | `analysis.py` 的 `divE-rho/epsilon_0`，`1e-3` gate；另有 checksum | 是官方 2-rank regression wiring，不等于所有 2D shape/order runtime |
| 3D Cartesian, shape=3 | `Examples/Tests/vay_deposition/inputs_test_3d_vay_deposition` | 同一 `divE-rho/epsilon_0` analysis surface；另有 checksum | 是官方 3D 入口，不等于 AMR、边界或完整 shape family |
| 2D Cartesian, shape=4 | `langmuir/inputs_test_2d_langmuir_multi_psatd_vay_deposition_particle_shape_4` | `analysis_2d.py` + checksum | 是独立高阶 sibling，不应外推为 3D shape=4 或正式收敛阶 |

源码侧同时确认：`WarpXParticleContainer.cpp` 已有 `doVayDepositionShapeN<1..4>` 分派，`CurrentDeposition.H` 对 RZ 和 1D 显式 abort，入口还禁止 implicit Vay。也就是说，当前代码表面支持的模板阶数比已接通的官方 runtime family 更宽；这正是“source support”与“runtime coverage”必须分开的地方。

## 证据分类

该合同分类为 `SOURCE_REGRESSION_WIRING_PARTIAL_RUNTIME_FAMILY`：

- 关闭“Vay 官方 2D/3D 与 shape=4 入口没有统一登记”的缺口；
- 不关闭 Vay 的完整 geometry/order runtime product；
- 不把 2D/3D shape=3 或单个 shape=4 sibling 写成正式收敛阶；
- 不把 RZ/1D source guard 当作物理失败，也不修改 `../warpx`。

## 可重放命令

```bash
python scripts/audit_vay_geometry_order_wiring.py \
  --warpx-root ../warpx \
  --output-json runs/stage-c-validation/vay-geometry-order-wiring/contract.json \
  --output-md runs/stage-c-validation/vay-geometry-order-wiring/contract.md
```

# Esirkepov 2001 paper/source/runtime crosswalk

审计日期：2026-07-13

## 本轮完成的工作

新增 `scripts/audit_esirkepov_paper_source_runtime_crosswalk.py`，把 Esirkepov 2001 的三层证据接到同一份只读 contract：

1. 预印本的 density decomposition、`Eq.(23)`、二阶 polynomial/spline algorithm 和离散 continuity scope；
2. WarpX `ShapeFactors.H`、`CurrentDeposition.H`、`WarpXParticleContainer.cpp` 的 shape difference、`one_third/one_sixth`、`invdtd`、几何写回和 dispatch/限制表面；
3. 现有 3D shape、RZ shape、RCYLINDER/RSPHERE radial family、2D MR source contract 以及 Langmuir CMake wiring。

## 结果边界

contract 通过只表示：

- 预印本的数学对象能够落到当前源码变量和 kernel 表面；
- 运行合同确实覆盖了多个 geometry/order family；
- 各 runtime 报告自己的 `PASS`、`BOUNDARY` 和 scope 仍被保留，没有被 crosswalk 汇总成全组合 PASS。

它不表示：

- ScienceDirect publisher-formatted CPC PDF 已取得；
- 预印本和 CPC 定稿已经逐页/逐式比较；
- RZ correction-on charge、AMR route-count 或 RCYLINDER/RSPHERE 完整 Gauss-law 已闭合；
- 当前 geometry/order 矩阵已经穷尽。

## 可重放命令

```bash
python scripts/audit_esirkepov_paper_source_runtime_crosswalk.py \
  --paper-dir references/04_particle_pushers_deposition_shapes/2001_EsirkepovCPC2001_Exact_charge_conservation_scheme_for_Particle-In-Cell_simulation_with_an_arbitrary_form-factor \
  --warpx-root ../warpx \
  --runs-root runs/stage-c-validation \
  --output-dir runs/stage-c-validation/esirkepov-paper-source-runtime-crosswalk
```

`runs/` 中的 JSON/Markdown 是本地运行证据，不进入 public release；本 note 只保存可复现入口和证据边界。

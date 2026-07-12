# Esirkepov Langmuir runtime contract

## 目的

把 Esirkepov 的 paper/formula/source 证据推进到当前 WarpX checkout 的真实运行层。官方 2D Langmuir input 使用 `direct`，因此本项目在 case-local 副本中只覆盖 `algo.current_deposition` 为 `esirkepov`，并补齐 `rho/divE` diagnostics；它是独立验证 sibling，不是上游已注册的 2D Esirkepov regression。

## 环境

- WarpX checkout: `../warpx`, commit `8c488b1a9`
- binary: `build_full/bin/warpx.1d...` / `warpx.3d...`
- MPI: 2 ranks
- `FI_PROVIDER=tcp`, `OMP_NUM_THREADS=1`
- producer: official `Examples/Tests/langmuir/inputs_test_*_langmuir_multi`; 2D 使用 case-local `direct -> esirkepov` overlay
- independent reader: `scripts/analyze_esirkepov_langmuir_contract.py`

## 结果

| case | plotfile | grid | official analysis | independent charge relative residual |
|---|---|---:|---|---:|
| 1D | `diags/diag1000080` | `128x1x1`, shape 1 | `Ez=1.7027849e-3 < 0.05`; charge `8.3450317e-12 < 1e-11` | `8.3450317e-12` |
| 2D | `diags/diag1000080` | `128x128x1`, shape 1 | `max(Ex,Ez)=1.2201354e-2 < 0.0503`; charge `3.5650106e-12 < 1e-11` | `3.5650106e-12` |
| 2D | `diags/diag1000080` | `128x128x1`, shape 2 | `max(Ex,Ez)=3.4095831e-2 < 0.0503`; charge `3.1326424e-12 < 1e-11` | `3.1326424e-12` |
| 2D | `diags/diag1000080` | `128x128x1`, shape 3 | `max(Ex,Ez)=4.6335800e-2 < 0.0503`; charge `4.5607474e-12 < 1e-11` | `4.5607474e-12` |
| 2D | `diags/diag1000080` | `128x128x1`, shape 4 | `max(Ex,Ez)=6.0165293e-2 < 0.07`; charge `2.8977145e-12 < 1e-11` | `2.8977145e-12` |
| 3D | `diags/diag1000040` | `64x64x64`, shape 1 | `max field error=3.4040176e-2 < 0.05`; charge `1.3029122e-12 < 1e-11` | `1.3029122e-12` |

MR overlay：`runs/stage-c-validation/esirkepov_langmuir_2d_mr_mpi2/` 使用官方 2D MR 的 `max_level=1`、ratio 4、CKC 和 filter，再覆盖 `direct -> esirkepov` 并补 `rho/divE` 输出。官方理论场误差为 `3.8068e-2 < 0.0503`，但逐层 reader contract 的 charge relative residual 为 level-0 `0.8828041`、level-1 `1.2005240`，因此分类为 `BOUNDARY`，不作为守恒 PASS。

两条 `warpx_used_inputs` 都确认 `algo.current_deposition = esirkepov` 和 `algo.particle_shape = 1`。独立 contract 还重新检查所有主要 E/B/J 字段与 `rho/divE` 为 finite。

## 证据边界

这些运行证明的是当前 checkout 在 1D/2D/3D Langmuir producer 上、并覆盖 2D shape=1/2/3/4 的 reader-side field 与 discrete `divE-rho/epsilon0` 合同；shape=0 在 `WarpX.cpp:1450` 被初始化断言拒绝，当前不支持。MR overlay 明确保留为 `BOUNDARY`，说明现有 level-wise reader/source-sync 语义还不能支撑强守恒结论。运行证据不是 bitwise kernel proof，也不覆盖 AMR route-count、RZ、边界裁剪、implicit 路径或 publisher-PDF 逐式比较。

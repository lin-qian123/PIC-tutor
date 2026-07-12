# 52 RZ Esirkepov：轴修正与分辨率的交互边界

绑定证据：

- `runs/stage-c-validation/esirkepov_langmuir_rz_mpi2/contract.json`
- `runs/stage-c-validation/esirkepov_langmuir_rz_no_verboncoeur_mpi2/contract.json`
- `runs/stage-c-validation/esirkepov_langmuir_rz_resolution128_mpi2/contract.json`
- `runs/stage-c-validation/esirkepov_langmuir_rz_resolution128_no_verboncoeur_mpi2/contract.json`
- `scripts/analyze_esirkepov_rz_langmuir_contract.py`
- `scripts/summarize_rz_esirkepov_axis_resolution_contract.py`

## 1. 四格结果

| 网格 | Verboncoeur 修正 | `Er/Ez` field | charge residual | 结论 |
|---|---|---:|---:|---|
| `64x128` | on | `1.075e-2/8.240e-3` | `3.593e-3` | field PASS，charge BOUNDARY |
| `64x128` | off | `4.280e-2/9.480e-3` | `5.513e-12` | field/charge 全部 PASS |
| `128x256` | on | `2.797e-2/3.049e-2` | `1.520e-3` | field PASS，charge BOUNDARY |
| `128x256` | off | `2.809e-2/3.662e-2` | `9.353e-12` | field/charge 全部 PASS |

这里的 field gate 是 `max(Er_error, Ez_error) < 0.12`，charge gate 是同面 `divE-rho/epsilon0 <= 1e-11`。对 `particle_shape=1`，高分辨率 correction-on 的 axis residual 相对低分辨率下降约 `2.36x`，但尚未接近 `1e-11`；correction-off 在两个分辨率上都通过。shape=2/3/4 的既有 off controls 则出现 `Er` field gate 失败，因此不能把 shape=1 的结果外推到全部 shape。

## 2. 可以得出的结论

这四格对照支持一个比“打开或关闭轴修正谁对谁错”更窄的结论：对 `particle_shape=1`，当前 RZ Esirkepov 的 axis charge residual 对轴体积修正和径向/轴向网格分辨率敏感；而既有 shape=2/3/4 对照说明 shape 也会改变 field/charge tradeoff。

- 默认 correction-on 在两个分辨率上都保持 field gate，但 axis charge residual 仍是主导误差；加密后误差下降但没有关闭。
- correction-off 在 `64x128` 和 `128x256` 上都通过 shape=1 的 field/charge 双 gate；但 shape=2/3/4 的 correction-off sibling 的 `Er` 误差分别为 `0.132/0.173/0.213`，超过 `0.12`。
- 因此不能只用 shape=1 off case 建议修改全局默认，也不能只用 higher-shape 失败结果宣称轴修正本身错误。

当前更准确的书稿表述是：轴修正是 RZ 几何语义的一部分，但其离散误差应在分辨率、shape、RZ 诊断面和 field/charge 双 gate 下分层报告。该结果是 project-level refined sibling，不修改 `../warpx` 的默认参数。

## 3. 可重复命令

```bash
python scripts/summarize_rz_esirkepov_axis_resolution_contract.py \
  --baseline-on runs/stage-c-validation/esirkepov_langmuir_rz_mpi2/contract.json \
  --baseline-off runs/stage-c-validation/esirkepov_langmuir_rz_no_verboncoeur_mpi2/contract.json \
  --refined-on runs/stage-c-validation/esirkepov_langmuir_rz_resolution128_mpi2/contract.json \
  --refined-off runs/stage-c-validation/esirkepov_langmuir_rz_resolution128_no_verboncoeur_mpi2/contract.json \
  --output-dir runs/stage-c-validation/esirkepov_langmuir_rz_axis-resolution-comparison
```

# RZ Esirkepov rho-side observable family

## 结论

将已有 RZ correction-on 2-rank plotfile 的 rho-side reader 合同扩展到 `particle_shape=1/2/3/4` 后，四个 shape 的末态都满足：

| shape | integrated-rho drift / `abs(rho)` scale | final `rho-(rho_electrons+rho_ions)` |
|---:|---:|---:|
| 1 | `6.495e-6` | `9.124e-15` |
| 2 | `2.371e-6` | `1.303e-14` |
| 3 | `2.729e-6` | `1.228e-14` |
| 4 | `3.354e-6` | `1.343e-14` |

这四项结果支持 `rho` 与 species decomposition 在末态的 reader-side 一致性；它们不关闭同面 `divE-rho/epsilon0` 的 axis residual，也不构成 current-conservation、Gauss-law 或正式 convergence order 证明。

## 可复现入口

```bash
python scripts/analyze_rz_esirkepov_rho_observable.py \
  --case 1=runs/stage-c-validation/esirkepov_langmuir_rz_mpi2 \
  --case 2=runs/stage-c-validation/esirkepov_langmuir_rz_shape2_resolution128_mpi2 \
  --case 3=runs/stage-c-validation/esirkepov_langmuir_rz_shape3_resolution128_mpi2 \
  --case 4=runs/stage-c-validation/esirkepov_langmuir_rz_shape4_resolution128_mpi2 \
  --output-dir runs/stage-c-validation/esirkepov_langmuir_rz_rho-observable-family
```

原始报告：`runs/stage-c-validation/esirkepov_langmuir_rz_rho-observable-family/contract.{json,md}`。

# 56 RZ Esirkepov：rho-side observable 与 `divE-rho` 边界分层

绑定证据：

- `runs/stage-c-validation/esirkepov_langmuir_rz_axis-correction-family/contract.json`
- `runs/stage-c-validation/esirkepov_langmuir_rz_rho-observable/contract.json`
- `scripts/analyze_rz_esirkepov_rho_observable.py`

## 1. 直接 rho/species 分解

在 shape=2/3/4 的 `128x256` correction-on refined sibling 上，直接读取同一 Full diagnostic 的：

- `rho`；
- `rho_electrons`；
- `rho_ions`；
- 三个输出时间层 `diag1000000/40/80`。

最终面计算 `rho - (rho_electrons + rho_ions)`，三个 shape 的最大相对差均约为 `1e-14`，低于 `1e-12` 的 rho-side decomposition gate。这说明当前最终 `rho` 与 species 分解在输出面上是一致的。

同时，积分电荷时间序列并不被改写成强守恒结论：中间面和末态的 net integrated charge 受到中性等离子体小差值、轴体积采样和时间演化共同影响，报告只记录它相对 `abs(rho)` 体积分量的变化，不用它替代粒子 ID/权重账本或 `divE-rho` 合同。

## 2. 与 `divE-rho` 的关系

这条 rho-side observable 不能消除 correction-on 的 `divE-rho/epsilon0` residual。更准确的分层是：

1. `rho` 与 `rho_electrons + rho_ions`：输出分解合同，当前通过；
2. `rho` 的柱坐标体积积分：直接几何 observable，记录时间序列但不包装成全局守恒证明；
3. `divE-rho/epsilon0`：field solver 与重新沉积 rho 的同面诊断合同，当前 axis cell 仍为 `O(1e-3)` boundary。

因此目前没有证据支持“rho kernel 已错误”或“全局轴修正应关闭”。现有证据只支持把问题继续定位在 field/source diagnostic compatibility、轴体积离散和同面采样语义的交界处。

## 3. 可重复命令

```bash
python scripts/analyze_rz_esirkepov_rho_observable.py \
  --case 2=runs/stage-c-validation/esirkepov_langmuir_rz_shape2_resolution128_mpi2 \
  --case 3=runs/stage-c-validation/esirkepov_langmuir_rz_shape3_resolution128_mpi2 \
  --case 4=runs/stage-c-validation/esirkepov_langmuir_rz_shape4_resolution128_mpi2 \
  --output-dir runs/stage-c-validation/esirkepov_langmuir_rz_rho-observable
```

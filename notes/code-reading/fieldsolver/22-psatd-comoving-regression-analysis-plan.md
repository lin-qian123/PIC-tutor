# Comoving PSATD regression-analysis plan

绑定源码与测试：

- `../warpx/Examples/Tests/nci_psatd_stability/CMakeLists.txt`
- `../warpx/Examples/Tests/nci_psatd_stability/inputs_test_2d_comoving_psatd_hybrid`
- `../warpx/Examples/Tests/nci_psatd_stability/analysis_galilean.py`
- `../warpx/Examples/Tests/nci_psatd_stability/analysis_psatd_CC1.py`
- `../warpx/Examples/Tests/nci_psatd_stability/analysis_default_regression.py`

## 当前事实

`test_2d_comoving_psatd_hybrid` 当前注册方式是：

```cmake
add_warpx_test(
    test_2d_comoving_psatd_hybrid
    2
    2
    inputs_test_2d_comoving_psatd_hybrid
    OFF
    "analysis_default_regression.py --path diags/diag1000400"
    OFF
)
```

它是 `WarpX_FFT` 条件下的 2D boosted-frame hybrid comoving PSATD smoke/checksum regression。自动 analysis 字段为 `OFF`，唯一自动消费者是末态 `diags/diag1000400` 的 checksum。

输入卡的关键 producer 合同是：

```ini
algo.maxwell_solver = psatd
algo.current_deposition = direct
algo.charge_deposition = standard
algo.particle_pusher = vay
psatd.use_default_v_comoving = 1
psatd.current_correction = 0
warpx.grid_type = hybrid
warpx.gamma_boost = 13.
warpx.boost_direction = z
warpx.do_moving_window = 1
warpx.use_filter = 1
diag1.fields_to_plot = Ex Ey Ez Bx By Bz jx jy jz rho
```

这意味着当前输出面可直接读取：

- `Ex/Ey/Ez`
- `Bx/By/Bz`
- `jx/jy/jz`
- `rho`

但当前没有输出 `divE`，所以不能直接套用 `analysis_galilean.py` 的 charge-conservation 分支。

## 不能直接复用的判据

`analysis_galilean.py` 做两件事：

1. 计算电场能量

$$
U_E=\sum \frac{\epsilon_0}{2}(E_x^2+E_y^2+E_z^2)
$$

并要求 `energy / energy_ref < tol_energy`。

2. 若 `psatd.current_correction=1`，读取 `divE` 与 `rho/epsilon0`，检查相对无穷范数误差。

comoving 输入卡显式设置 `psatd.current_correction=0`，且当前 `fields_to_plot` 不含 `divE`。因此 v0.31 不能声称已经具备 charge-conservation analysis。只有在输入卡改成输出 `divE` 后，才可以设计一个独立的 Gauss-law drift diagnostic。

## 现有输出可做的第一阶段 analysis

不修改 WarpX 输入卡时，可新增一个 `analysis_comoving.py`，只依赖现有 `diag1000400` 字段。它应至少包含三层 gate。

### Gate 1: finite field sanity

读取 `Ex/Ey/Ez/Bx/By/Bz/jx/jy/jz/rho`，要求全部为有限值：

```python
for name in ["Ex", "Ey", "Ez", "Bx", "By", "Bz", "jx", "jy", "jz", "rho"]:
    arr = all_data["boxlib", name].squeeze().v
    assert np.all(np.isfinite(arr))
```

这只能证明输出没有 NaN/Inf，属于 smoke analysis，不是 NCI 强判据。

### Gate 2: electric-field energy ceiling

沿用 Galilean analysis 的能量定义：

$$
U_E=\sum \frac{\epsilon_0}{2}(E_x^2+E_y^2+E_z^2).
$$

初版可以从已知 checksum baseline 对应的末态输出重新标定 `energy_ref_comoving`，并设置：

```python
err_energy = energy / energy_ref_comoving
assert err_energy < tol_energy
```

这里有两个要求：

- `energy_ref_comoving` 必须来自一次明确记录的 reference run，不能直接借用 Galilean `energy_ref`。
- `tol_energy` 应先用宽松容差保护趋势，后续再通过多平台 CI 数据收紧。

这个 gate 的证据等级比 checksum 高，因为它验证了物理相关聚合量；但它仍不是严格 NCI 增长率拟合。

### Gate 3: dominant-field shape sanity

该输入卡是 laser/plasma-channel/beam 场景，末态场不应在单个孤立网格点形成异常 spike。可增加局部峰值比值：

$$
R_E=\frac{\max |\mathbf E|}{\mathrm{p99}(|\mathbf E|)+\delta}.
$$

初版只把它作为异常探测：

```python
Emag = np.sqrt(Ex**2 + Ey**2 + Ez**2)
spike_ratio = np.max(Emag) / (np.percentile(Emag, 99) + 1e-300)
assert spike_ratio < spike_ratio_ref
```

`spike_ratio_ref` 同样必须由 reference run 标定。这个 gate 可以捕捉局部谱/边界异常，但不能替代能量或 NCI 判据。

## 需要输入卡增强的第二阶段 analysis

若要把 comoving regression 从“checksum + energy sanity”推到更强验证，应修改输入卡输出 `divE`：

```ini
diag1.fields_to_plot = Ex Ey Ez Bx By Bz jx jy jz rho divE
```

随后可新增 Gauss-law diagnostic：

$$
\epsilon_G=\frac{\|\nabla\cdot\mathbf E-\rho/\epsilon_0\|_\infty}
{\max(\|\nabla\cdot\mathbf E\|_\infty,\|\rho/\epsilon_0\|_\infty,\delta)}.
$$

但要注意：comoving 当前 `psatd.current_correction=0`，这条 gate 的解释不是“current-correction 正确”，而是“该 boosted-frame hybrid comoving 工作流在末态没有出现明显 Gauss-law drift”。如果未来开启 current correction 或换沉积方式，判据文字必须重新写。

## CMake patch 草案

第一阶段不改输入卡，只把 analysis 从 `OFF` 改成新脚本：

```cmake
add_warpx_test(
    test_2d_comoving_psatd_hybrid
    2
    2
    inputs_test_2d_comoving_psatd_hybrid
    "analysis_comoving.py diags/diag1000400"
    "analysis_default_regression.py --path diags/diag1000400"
    OFF
)
```

脚本骨架：

```python
#!/usr/bin/env python3
import sys
import numpy as np
import scipy.constants as scc
import yt

yt.funcs.mylog.setLevel(0)
ds = yt.load(sys.argv[1])
if "force_periodicity" in dir(ds):
    ds.force_periodicity()
grid = ds.covering_grid(level=0, left_edge=ds.domain_left_edge, dims=ds.domain_dimensions)

fields = {name: grid["boxlib", name].squeeze().v for name in
          ["Ex", "Ey", "Ez", "Bx", "By", "Bz", "jx", "jy", "jz", "rho"]}
for name, arr in fields.items():
    assert np.all(np.isfinite(arr)), name

Ex, Ey, Ez = fields["Ex"], fields["Ey"], fields["Ez"]
energy = np.sum(scc.epsilon_0 / 2 * (Ex**2 + Ey**2 + Ez**2))
energy_ref = ...
tol_energy = ...
assert energy / energy_ref < tol_energy
```

其中 `energy_ref/tol_energy/spike_ratio_ref` 不能凭空写死，需要先跑一次 reference 或从 CI baseline 反推出数值后再提交 WarpX 侧 patch。

## 当前原型落地状态

`PIC-tutor` 当前已经把这份方案中的第一阶段 fallback 落成原型脚本：

- `scripts/analysis_comoving.py`

它遵循 WarpX analysis helper 的基本形状，但把 gate 语义显式拆开：

- finite-field sanity：始终执行
- spike gate：可通过 `--ledger-json ... --enable-spike-gate` 打开
- energy gate：当前保留为显式可选项，不默认启用

本地自校验已经跑过两次：

```bash
python scripts/analysis_comoving.py \
  runs/fieldsolver-validation/comoving-stable-baseline/diags/diag1000400 \
  --label stable-comoving-prototype \
  --ledger-json runs/fieldsolver-validation/comoving-reference-ledgers/comoving-stable-vs-no-comoving.json \
  --enable-spike-gate
```

这条 stable baseline 当前通过 `finite + spike`。而同样命令替换成 `comoving-unstable-no-comoving/diags/diag1000400` 时，会在相同 `spike_ratio_ref_stable` 阈值下失败。也就是说，当前第一阶段 fallback 已经不只是纸面方案，而是本地可执行原型。

这进一步说明：即便后续最终决定不采用 Galilean 式 energy gate，comoving patch 第一阶段也已经有一条可落地的 `finite + spike` 路线。

## v0.31 正文边界

本书 v0.31 只记录“可落地分析方案”，不声称 WarpX 侧已经实现该 analysis。当前证据等级应写为：

| 层级 | 当前状态 | 可支持的说法 |
|---|---|---|
| checksum | 已存在 | `test_2d_comoving_psatd_hybrid` 的末态 plotfile 与 baseline 一致 |
| finite field sanity | 方案可直接实现 | 可捕捉 NaN/Inf，不是物理强判据 |
| electric energy ceiling | 需要 reference 标定 | 可成为 NCI/稳定性 proxy，但不是增长率拟合 |
| spike ratio | 需要 reference 标定 | 可捕捉局部异常，不替代能量判据 |
| Gauss-law drift | 需要输出 `divE` | 可验证末态 Gauss-law drift，但要与 `current_correction=0` 的语义分开 |

后续真正修改 WarpX regression 时，应在 PR 中同时提交 `analysis_comoving.py`、CMake wiring、必要时的 `divE` 输出变更，以及 reference 数值的来源说明。

# Comoving PSATD reference calibration and patch packaging

绑定源码与测试：

- `../warpx/Examples/Tests/nci_psatd_stability/CMakeLists.txt`
- `../warpx/Examples/Tests/nci_psatd_stability/inputs_test_2d_comoving_psatd_hybrid`
- `../warpx/Examples/Tests/nci_psatd_stability/analysis_galilean.py`
- `../warpx/Examples/Tests/nci_psatd_stability/analysis_psatd_CC1.py`
- `22-psatd-comoving-regression-analysis-plan.md`

## 目标

这份笔记不再新增一个小版本号，而是为当前 comoving PSATD 模块继续收口：把 `analysis_comoving.py` 从“可行方案”推进到“可提交 WarpX patch 的 reference 标定与打包清单”。

核心问题不是脚本怎么写，而是：

1. `energy_ref`、`tol_energy`、`spike_ratio_ref` 应该从哪里来；
2. 这些 reference 怎样像 `analysis_galilean.py` 一样有明确物理语义，而不是随便抄一次本机输出；
3. 真正提交 PR 时，哪些文件必须成包出现。

## 从现有 WarpX regression 可复用的模式

`nci_psatd_stability` 里已经有两种成熟模式。

### 模式 A：`analysis_galilean.py`

这一路不是把末态能量和“稳定运行自身”比，而是把稳定配置的末态电场能量和一个**已知不稳定参考配置**比较。也就是说，reference 的意义是“如果关闭当前稳定化机制，场能会膨胀到什么量级”。

现有脚本里，这个模式已经用于：

- Galilean vs 非 Galilean；
- current-correction 分支；
- averaged Galilean vs 不做 averaging 的 sibling。

因此它给 comoving 的启发很直接：如果要让 `energy_ref_comoving` 有和 Galilean 类似的解释，reference run 也应来自“仅关闭 comoving 稳定化关键开关”的对照输入，而不是来自任意一次稳定 baseline。

### 模式 B：`analysis_psatd_CC1.py`

这一路更简单：单独为一个 test 写死 `energy_ref = 66e6`，只保留能量比 gate。

它适合单一路径、单一路由、语义清楚的 smoke-to-stability proxy，但前提仍然是：

- reference 值有记录来源；
- 该值对应的输入卡、诊断面和字段定义不变；
- 脚本注释能说明这是哪一类 reference。

comoving patch 的第一版更接近这个模式：先做独立 `analysis_comoving.py`，再决定是否进一步扩成和 `analysis_galilean.py` 共用的 family-level 脚本。

## comoving reference 标定应遵守的约束

### 1. 不借用 Galilean 的 `energy_ref`

虽然 comoving 和 Galilean 都在 `nci_psatd_stability` 家族里，但它们不是同一个算法分支：

- 参数入口不同；
- `grid_type = hybrid`；
- 当前输入还带 moving window、filter、boosted frame 和 laser/plasma/beam runtime。

因此 `analysis_galilean.py` 里的任何 `energy_ref` 都不能直接挪过来。

### 2. reference 必须绑定到同一诊断面

当前唯一稳定的自动输出面是 `diags/diag1000400`。所以第一阶段所有 reference 都应绑定同一末态 surface：

- `energy_ref_comoving`：由 `diag1000400` 的 `Ex/Ey/Ez` 算出；
- `spike_ratio_ref`：由同一张 `diag1000400` 算出；
- 若后续补 `divE`，Gauss-law gate 也应先绑定同一末态 surface。

否则脚本一旦切到别的迭代号或别的 diagnostics，就会把“analysis 变了”和“producer 变了”混在一起。

### 3. reference 必须说明是 stable baseline 还是 unstable contrast

这一步最容易写糊。建议在脚本常量旁显式区分两类数字：

- `energy_ref_unstable`：来自 deliberately unstable contrast run，用来表达 NCI 膨胀量级；
- `spike_ratio_ref_stable`：来自当前稳定 baseline，用来表达“正常末态不会出现离散尖峰”的形状上界。

两者不要共用一个“reference”口径。因为 spike ratio 需要的是 stable envelope 上界，而 energy proxy 更适合拿 unstable contrast 来体现“稳定化是否有效”。

## 建议的标定流程

### 阶段 1：冻结 stable baseline 的统计量

先用当前 `inputs_test_2d_comoving_psatd_hybrid` 跑出一份本地 reference ledger，至少记录：

- `energy_stable`
- `spike_ratio_stable`
- `p99(|E|)`
- `max(|E|)`
- 运行命令、WarpX commit、输入卡摘要、plotfile 路径

这一步的目的不是生成最终 `energy_ref`，而是固定“正常稳定运行时，末态形状大概长什么样”。

### 阶段 2：构造单开关对照的 unstable candidate

仿照 `analysis_galilean.py` 的思路，需要一个只关闭 comoving 关键稳定化机制的 sibling 输入。这里的原则是：

- 除了目标稳定化开关外，其余 runtime scaffold 尽量不动；
- 仍然输出 `diag1000400` 同类字段；
- 目标是放大 NCI/field-energy，而不是引入另一套完全不同的物理场景。

具体切哪一个开关，目前正文只能写到“需要构造并验证”，不能提前声称已经确定。更保守的说法是：

- 候选对照应优先来自 `v_comoving` / default-comoving 路径本身；
- 如果需要再改 filter、moving window 或 deposition，那已经不是单开关对照，解释力会明显下降。

### 阶段 3：从 unstable candidate 提取 `energy_ref_unstable`

一旦对照输入确定，就从同一末态 `diag1000400` 读取：

$$
U_E = \sum \frac{\epsilon_0}{2} (E_x^2 + E_y^2 + E_z^2).
$$

然后把 `energy_ref_unstable` 和稳定路径的 `energy_stable` 同时记入标定记录。真正写进 `analysis_comoving.py` 的断言建议是：

```python
energy_ratio = energy / energy_ref_unstable
assert energy_ratio < tol_energy
```

这里 `tol_energy` 初版不应直接追到极紧，而应先覆盖：

- 本机重复运行波动；
- CI 机器差异；
- FFT / floating-point 微差。

### 阶段 4：把 spike gate 固定为 stable upper envelope

`spike_ratio` 不是 NCI 增长率 proxy，更像局部异常探测。因此它更适合写成 stable envelope：

```python
assert spike_ratio < spike_ratio_ref_stable
```

如果后续发现 stable baseline 自身波动明显，可以把它改成：

```python
assert spike_ratio < spike_ratio_ref_stable * safety_factor
```

但 `safety_factor` 必须写出来源，不能默默拍脑袋。

## 建议的 patch 包结构

当这条工作真正进入 WarpX 侧 patch 时，最小可审查包建议是四件套。

### 1. `analysis_comoving.py`

第一阶段至少包含：

- finite-value gate；
- electric-field energy ratio gate；
- spike-ratio gate；
- 常量来源注释。

### 2. CMake wiring

把 `test_2d_comoving_psatd_hybrid` 从：

```cmake
OFF
"analysis_default_regression.py --path diags/diag1000400"
```

改成：

```cmake
"analysis_comoving.py diags/diag1000400"
"analysis_default_regression.py --path diags/diag1000400"
```

这样保留 checksum side consumer，同时新增物理相关 analysis。

### 3. optional diagnostics widening

只有当第二阶段真的要做 Gauss-law drift 时，才需要把输入卡改成：

```ini
diag1.fields_to_plot = Ex Ey Ez Bx By Bz jx jy jz rho divE
```

这一步不应和第一阶段强绑。否则 patch 一次引入两件事：

- analysis wiring 变化；
- producer surface 变化。

review 时很难判断到底是哪一处改变导致结果变化。

### 4. reference provenance note

这类说明不一定非要单独建文档，但必须存在，至少包括：

- 哪个输入卡生成 stable ledger；
- 哪个 sibling 输入生成 unstable contrast；
- 统计量提取命令；
- WarpX commit；
- 得到的 `energy_ref_unstable / tol_energy / spike_ratio_ref_stable`。

没有 provenance note，后面就无法安全收紧容差，也无法解释 reference 为什么合理。

## 当前模块的闭合条件

在 `PIC-tutor` 这边，comoving PSATD 模块暂时可以把闭合条件写成三步，而不是继续拆新版本号：

1. 书稿正文已经明确当前 `analysis=OFF` 的边界，以及第一阶段/第二阶段 analysis 的证据等级差异；
2. 计划笔记已经把 reference 标定、unstable contrast、patch 包结构和 provenance 要求写清楚；
3. 下一步若继续推进，就该真的去 materialize reference ledger 或转向 RZ PSATD validation 强判据表，而不是再做一轮泛泛的“analysis 方案描述”。

## 当前仓库内已补的提取工具

为了把“materialize reference ledger”从一句话推进到真正可执行的动作，当前仓库已补入：

- `scripts/build_comoving_reference_ledger.py`

它的职责不是直接替你决定最终 `tol_energy`，而是把 stable / unstable plotfile 的关键统计量、输入卡路径、WarpX commit 和运行命令收成一份可审查 ledger。典型用法可以写成：

```bash
python scripts/build_comoving_reference_ledger.py \
  --label comoving-stable-vs-contrast \
  --stable-plotfile /path/to/stable/diags/diag1000400 \
  --unstable-plotfile /path/to/unstable/diags/diag1000400 \
  --stable-input ../warpx/Examples/Tests/nci_psatd_stability/inputs_test_2d_comoving_psatd_hybrid \
  --unstable-input /path/to/contrast_input \
  --warpx-commit 8c488b1a9 \
  --producer-command "mpirun -np 4 ./warpx inputs_test_2d_comoving_psatd_hybrid" \
  --output-stem runs/fieldsolver-validation/comoving-reference-ledgers/comoving-stable-vs-contrast
```

脚本会提取：

- `electric_energy`
- `e_mag_max`
- `e_mag_p99`
- `spike_ratio`
- 每个 `Ex/Ey/Ez/Bx/By/Bz/jx/jy/jz/rho` 的 finite/extrema 状态

若同时提供 stable / unstable 两张 plotfile，还会额外给出：

- `energy_ref_unstable`
- `spike_ratio_ref_stable`
- `stable_over_unstable_energy_ratio`
- `minimum_tol_energy_for_observed_stable_sample`

这些量是当前样本对的事实记录，不是自动推荐的最终 hard-coded tolerance。真正要不要把它们写进 WarpX patch，仍需结合重复运行和 CI 波动再判断。

## 当前结论

当前最稳妥的说法是：

- `analysis_comoving.py` 的脚本形状已经清楚；
- 真正的难点在 reference 标定与 provenance；
- 当前仓库已经把 reference ledger 工具链和一组本地样本跑通，但审计结论是“分支已验证，能量 gate 还不能定”；
- 只有当更接近 upstream regression 的 repeated/MPI contrast 也证明 non-comoving sibling 会把电场能量抬高，才适合把 `energy_ref_unstable` 硬编码进 WarpX patch。

## 2026-06-30 本地 audit 实跑结果

当前仓库已在只读 `../warpx` 前提下完成两条单进程本地运行：

1. stable baseline：
   - 输入：`../warpx/Examples/Tests/nci_psatd_stability/inputs_test_2d_comoving_psatd_hybrid`
   - 命令行覆盖：`warpx.numprocs='1 1'`
   - 末态 plotfile：`runs/fieldsolver-validation/comoving-stable-baseline/diags/diag1000400`
2. no-comoving sibling：
   - 同一输入卡
   - 命令行覆盖：`warpx.numprocs='1 1' psatd.use_default_v_comoving=0 psatd.v_comoving='0. 0. 0.'`
   - 末态 plotfile：`runs/fieldsolver-validation/comoving-unstable-no-comoving/diags/diag1000400`

对应生成的 ledger：

- `runs/fieldsolver-validation/comoving-reference-ledgers/comoving-stable-baseline.md`
- `runs/fieldsolver-validation/comoving-reference-ledgers/comoving-stable-baseline.json`
- `runs/fieldsolver-validation/comoving-reference-ledgers/comoving-stable-vs-no-comoving.md`
- `runs/fieldsolver-validation/comoving-reference-ledgers/comoving-stable-vs-no-comoving.json`

当前样本给出的关键事实是：

- stable baseline：`electric_energy = 8.1520684623101725e+14`
- no-comoving sibling：`electric_energy = 7.7864117768828750e+14`
- `stable_over_unstable_energy_ratio = 1.0469608718245416`
- `spike_ratio_ref_stable = 1.1103719982074416`
- `stable_over_unstable_spike_ratio = 0.9985705473421257`

这组数字说明两点：

1. sibling override 已经切到非 comoving 分支。运行日志里 stable baseline 会打印 `v_comoving = (0,0,-298904182.1)`，而 no-comoving sibling 不再出现该行。
2. 但这组单进程本地样本没有出现“关闭 comoving 后电场能量更高”的预期；相反 stable baseline 的能量略高。因此这里的 `energy_ref_unstable` 只能算 ledger 事实记录，不能直接充当最终 WarpX CI gate。

换句话说，`v0.32` 能诚实声称的闭合点不是“energy gate 已定”，而是“reference 标定已经从抽象方案推进到本地 audit，且 audit 结果证明还需要更接近 upstream regression 的 repeated/MPI contrast 才能定 gate”。

## 2026-06-30 本地 Galilean control experiment

为了确认“当前单进程本地样本看不出 comoving unstable-energy contrast”到底是环境问题，还是 comoving sibling 本身就不够好，当前仓库又补做了一组 control：

1. stable Galilean baseline：
   - 输入：`../warpx/Examples/Tests/nci_psatd_stability/inputs_test_2d_galilean_psatd_hybrid`
   - 命令行覆盖：`warpx.numprocs='1 1'`
2. no-Galilean sibling：
   - 同一输入卡
   - 命令行覆盖：`warpx.numprocs='1 1' psatd.use_default_v_galilean=0 psatd.v_galilean='0. 0. 0.'`

对应 ledger：

- `runs/fieldsolver-validation/galilean-reference-ledgers/galilean-stable-vs-no-galilean.md`
- `runs/fieldsolver-validation/galilean-reference-ledgers/galilean-stable-vs-no-galilean.json`

这组 control 给出的关键事实是：

- stable Galilean：`electric_energy = 6.5553743351612200e+14`
- no-Galilean sibling：`electric_energy = 7.7864117768831088e+14`
- `stable_over_unstable_energy_ratio = 0.8418992628444483`

这件事很关键，因为它说明：

1. 在这台机器上，即便没有 `mpirun/mpiexec`、只能把 `warpx.numprocs` 改成 `1 1`，单进程本地样本仍然能复现 WarpX 已知的 Galilean unstable-energy ordering。
2. 因此，comoving `no-comoving` sibling 当前没有抬高电场能量，已经不能简单归咎于“本机没有 MPI”；更可能的解释是这个 sibling 还不够贴近真正应该被视作 unstable reference 的 branch。

这里还可以再收紧一步。当前仓库里 `no-comoving` 与 `no-galilean` 这两条 sibling 的末态指标已经几乎完全重合：

- `electric_energy` 相对差异约 `3.0e-14`
- `e_mag_max` 相对差异约 `2.7e-14`
- `e_mag_p99` 相对差异约 `2.2e-14`
- `spike_ratio` 相对差异约 `5.6e-15`

这说明一旦把 `v_comoving` 或 `v_galilean` 压成零，这两条 2D hybrid boosted-frame sibling 在本机上实际上汇合到同一条 standard-PSATD unstable branch。于是问题就更清楚了：

- 对 Galilean family，这条 shared unstable branch 能形成有效的 energy ordering；
- 对 comoving family，这条 shared unstable branch 目前不能形成有效的 energy ordering。

换句话说，Galilean control experiment 把结论从“环境可能太弱”收紧成了“comoving contrast 设计乃至 gate 语义都仍需重审”。这也意味着后续若继续推进 `analysis_comoving.py`，优先级应当从“先想办法补 MPI”调整为：

- 先重新论证 comoving family 中哪一条 sibling 才真正有资格当 unstable reference；
- 同时准备一个更保守的 fallback：若 energy ordering 仍不成立，就把第一阶段 patch 重心转到 finite/spike 或其他更合适的判据；
- 再在条件允许时用更接近 upstream regression 的 MPI/并行设置复核。

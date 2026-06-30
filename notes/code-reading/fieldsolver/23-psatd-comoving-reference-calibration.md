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

## 当前结论

当前最稳妥的说法是：

- `analysis_comoving.py` 的脚本形状已经清楚；
- 真正的难点在 reference 标定与 provenance；
- 这一步应作为 comoving PSATD 模块内的继续收口，而不是单独再发一个小版本；
- 只有当 reference ledger 和 patch 四件套都齐了，才值得统一更新版本说明。

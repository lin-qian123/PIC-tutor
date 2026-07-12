# Comoving PSATD velocity-candidate scan

绑定对象：

- `../warpx/Examples/Tests/nci_psatd_stability/inputs_test_2d_comoving_psatd_hybrid`
- `scripts/scan_comoving_velocity_candidates.py`
- `runs/fieldsolver-validation/comoving-reference-ledgers/comoving-velocity-scan.md`
- `runs/fieldsolver-validation/comoving-reference-ledgers/comoving-velocity-scan.json`
- `23-psatd-comoving-reference-calibration.md`
- `24-psatd-comoving-first-stage-patch-draft.md`

## 目标

在现有 `stable baseline` / `zero-comoving` 对照已经证明

- `no-comoving` 不会抬高电场能量；
- `no-comoving` 与 `no-galilean` 实际汇合到同一条 standard-PSATD branch；

之后，下一步最自然的问题就是：如果只沿 `v_comoving` 路径本身继续做 sibling 筛选，是否能找到一个既保留单开关解释力、又真的把末态能量或 spike 指标推向“更像 unstable reference”的候选？

这份笔记就是对这个问题的第一次本地扫描。

## 扫描设计

本轮扫描故意保持范围很窄：

1. 不改 filter；
2. 不改 moving window；
3. 不改 hybrid grid；
4. 不改 deposition/pusher；
5. 只改 `psatd.use_default_v_comoving` 与 `psatd.v_comoving`。

也就是说，它不是“所有可能的 unstable contrast 搜索”，而是“只沿 comoving velocity 本身往前走一步”。

当前脚本 `scripts/scan_comoving_velocity_candidates.py` 复用了已有 stable / zero-comoving 结果，并额外生成三条候选：

- `explicit-default-beta`：关闭 default selector，但显式写入与默认值等价的 `v_comoving`
- `half-default-beta`：只保留一半默认 comoving 速度
- `positive-default-beta`：保持同样模长，但把方向反过来

基础参数来自输入卡中的：

```text
warpx.gamma_boost = 13.
psatd.use_default_v_comoving = 1
```

因此默认归一化速度模长是：

```text
beta = sqrt(1 - 1/gamma_boost^2) = 0.9970370305242862
```

## 本地运行边界

这些本地生成候选在本机上都能完整落出 `diag1000400` 和 `warpx_used_inputs`，但会出现一个重复的环境尾噪声：

```text
MPI_Finalize failed
OFI poll failed (default nic=utun6: Input/output error)
```

它发生在主计算和 plotfile 写盘之后，而不是在参数解析或主推进中途。因此当前扫描把 `diag1000400` 视为可用证据，同时把这条尾噪声单独记录下来，而不把它误判成“物理候选失败”。

## 结果汇总

来自 `comoving-velocity-scan.{md,json}` 的当前结果是：

| candidate | normalized `v_z/c` | energy / stable | spike / stable | 说明 |
|---|---:|---:|---:|---|
| stable-default-selector | `-0.9970370305242862` | `1.0000000000000000` | `1.0000000000000000` | 当前稳定基线 |
| explicit-default-beta | `-0.9970370305242862` | `1.0000000000000131` | `1.0000000000000213` | 与 stable baseline 数值重合 |
| half-default-beta | `-0.4985185152621431` | `0.9880344433922247` | `1.0025594890383713` | 能量略降，spike 略升 |
| zero-comoving | `0.0000000000000000` | `0.9551455330487159` | `1.0014314989178070` | 能量继续下降，spike 只小幅上升 |
| positive-default-beta | `0.9970370305242862` | `0.8028125321991401` | `1.0622177820830927` | spike 显著升高，但能量反而大幅降低 |

## 这轮扫描真正说明了什么

### 1. default selector 本身不是隐藏变量

`explicit-default-beta` 与 `stable-default-selector` 的 `electric_energy` 和 `spike_ratio` 在浮点舍入误差范围内完全一致。

这意味着当前 stable baseline 的“稳定性来源”确实就是默认 selector 最终写入的那组 `v_comoving` 值，而不是某个额外的 parser side effect。后续正文可以更放心地把

- `psatd.use_default_v_comoving = 1`

解释成“自动写入 `-beta_boost \hat{z}`”，而不是“还有别的隐藏 runtime 差异”。

### 2. 只减弱或移除 comoving 速度，不会给出更高的末态电场能量

`half-default-beta` 和 `zero-comoving` 都没有把 `electric_energy` 推高到 stable baseline 之上，反而分别降到

- `0.9880 x stable`
- `0.9551 x stable`

这进一步压实了上一轮 audit 的结论：在当前本机单进程场景里，沿“减弱 comoving velocity”这条最自然的 sibling 方向，能量 ordering 仍然站不住。

### 3. 反号 `v_comoving` 会显著抬高 spike，但仍然不会抬高 energy

最有信息量的候选其实是 `positive-default-beta`：

- `spike_ratio / stable = 1.0622177820830927`
- `energy / stable = 0.8028125321991401`

也就是说，**同一个 comoving family 内部，spike 和 energy 可以明显解耦。**

如果只看 spike，它比 `zero-comoving` 和 `half-default-beta` 更像“明显更坏的 sibling”；
但如果只看 energy，它却比 stable baseline 更低得多。

这条结果直接改变了当前 patch 收口的论证重点：

- `spike gate` 依然是第一阶段最可信的局部异常探测器；
- `energy gate` 不能再被当作 comoving family 的天然主判据。

### 4. 当前扫描没有找到更好的 local energy-reference sibling

从“谁能把末态电场能量抬高到 stable baseline 之上”这个标准看，这轮候选里没有胜者：

- 最高能量仍是 stable baseline 自身；
- 所有 velocity-only sibling 的 energy 都不超过 stable。

因此，当前仓库仍然不能诚实地把任何一个本地 `v_comoving` 候选写成最终 `energy_ref_unstable`。

## 对第一阶段 patch 的影响

这轮扫描实际上把第一阶段 patch 的边界又收紧了一层。

此前的结论是：

- `finite + spike` 已经有本地可执行原型；
- `energy gate` 还缺一个可信的 unstable reference。

现在可以进一步写成：

1. `v_comoving` 路径的显式等价写法已经被验证，不存在 default-selector 隐藏变量；
2. 只沿 velocity 自身做 local sibling 扫描，没有找到会抬高 energy 的候选；
3. 但反号 `v_comoving` 确实会显著抬高 spike，说明 spike 对 comoving mismatch 更敏感；
4. 因此，第一阶段 WarpX patch 继续收敛到 `finite + spike` 是有新增本地证据支撑的，而不是单纯保守。

## 下一步该怎么推进

从当前证据出发，下一步更合理的顺序是：

1. 继续把第一阶段 patch 维持在 `finite + spike`；
2. 如果还想争取 `energy gate`，不要再只沿 `v_comoving` 数值扫描，而应转向更接近 upstream regression 的 repeated/MPI contrast；
3. 如果 repeated/MPI contrast 仍然不给出更强的 energy ordering，就应明确把 comoving family 的第一阶段主 gate 定义为 `finite + spike`，把 energy gate 降级为 follow-up。

换句话说，这轮扫描不是把问题解决成“终于找到了 energy sibling”，而是把问题收口成了一个更硬的结论：

**当前 local evidence 更支持“comoving first-stage patch = finite + spike”，而不是“再坚持把 energy gate 找出来”。**

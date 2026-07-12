# RZ JRhom first-stage target-checkout workflow

绑定源码：

- `../warpx/Examples/Tests/nci_psatd_stability/CMakeLists.txt`
- `notes/code-reading/fieldsolver/rz_jrhom_first_stage_bundle/`
- `scripts/stage_rz_jrhom_first_stage_patch.py`
- `scripts/audit_rz_jrhom_first_stage_patch.py`
- `scripts/preview_rz_jrhom_first_stage_patch.py`
- `scripts/report_rz_jrhom_first_stage_patch.py`

## 目标

上一轮 `31-rz-jrhom-first-stage-patch-draft.md` 已经把 repeated/MPI 复核过的 `finite + energy` helper 收成 helper/diff/provenance/submission packet/PR draft/bundle 六类 handoff 资产，但那一轮还停在“资产已经组织好”。如果后续真要把这条 patch 交给另一个 WarpX worktree 或 reviewer，仍然缺一个更工程化的问题：目标 checkout 现在到底是 `unstaged`、`partial` 还是已经 `staged`，以及这份 bundle 将会对目标 checkout 造成什么精确改动。

因此这一轮不再继续写新的 helper 判据，而是把 RZ JRhom 线补成和 comoving 一样的 target-checkout workflow：先 preview diff，再 audit 当前状态，再生成 markdown preflight report，最后按明确命令做 `--dry-run` 或 staging。

## 当前 bundle 对目标 checkout 的最小写入面

当前 RZ bundle 只声称两个改动：

1. 在 `Examples/Tests/nci_psatd_stability/analysis_rz_jrhom.py` 新增第一阶段 helper。
2. 仅把 `test_rz_psatd_JRhom_LL2` 的 analysis 行从

```cmake
        OFF  # analysis
```

改成

```cmake
        "analysis_rz_jrhom.py diags/diag1000025"  # analysis
```

其余 checksum 行、dependency 行和任何其他 test block 都不应被改写。这也是 `stage_rz_jrhom_first_stage_patch.py` 的唯一允许写入面。

## 四个脚本的职责划分

### 1. `preview_rz_jrhom_first_stage_patch.py`

只读打印 unified diff。它直接比较：

- 目标 checkout 当前 `Examples/Tests/nci_psatd_stability/CMakeLists.txt`
- bundle 中镜像的 `analysis_rz_jrhom.py`

如果目标 checkout 已经与 bundle 一致，则只输出：

```text
target checkout already matches the current bundle
```

这一步的价值是把“将要改什么”先打印清楚，而不是直接写入。

### 2. `audit_rz_jrhom_first_stage_patch.py`

只读把目标 checkout 归类成三档：

- `unstaged`：helper 不存在，且 target test block 的 analysis 仍是 `OFF`
- `staged`：helper 与 bundle 一致，且 analysis 行与 bundle 一致
- `partial`：其余任何中间态，例如 helper 存在但内容不同，或 analysis 行被改成了自定义值

这个脚本不判断 helper 是否“物理正确”，只判断目标 worktree 与当前 bundle 是否一致。

### 3. `report_rz_jrhom_first_stage_patch.py`

在 audit 之上自动生成 markdown preflight report，固定输出：

- target root
- bundle root
- overall status
- helper status
- CMake status
- 附带 handoff docs
- 下一条推荐命令

这样接续者不需要自己再整理“下一步该跑 preview 还是 stage”。

### 4. `stage_rz_jrhom_first_stage_patch.py`

这是唯一会写文件的脚本，但默认仍要求显式传入 `--warpx-root`。`PIC-tutor` 不假定相邻 `../warpx` 一定就该被改。

推荐调用顺序固定为：

1. `python scripts/preview_rz_jrhom_first_stage_patch.py --warpx-root ../warpx`
2. `python scripts/stage_rz_jrhom_first_stage_patch.py --warpx-root ../warpx --dry-run`
3. `python scripts/stage_rz_jrhom_first_stage_patch.py --warpx-root ../warpx`
4. `python scripts/audit_rz_jrhom_first_stage_patch.py --warpx-root ../warpx`

## 本轮结论

到这一步，RZ JRhom LL2 这条线已经从：

- direction note
- sibling scan
- helper prototype
- repeated/MPI ledger
- patch draft assets

推进到：

- bundle 可预览
- target checkout 可审计
- 状态可报告
- staging 可 dry-run / 落地

这仍然不等于“已经正式上提 WarpX upstream”。它只是把上提前最后一段本地工程动作补齐了。接下来这条线的真正决策点已经很清楚：

- 要么在目标 checkout 上按当前口径 staging，并准备实际提交流程；
- 要么把这条线冻结在 `finite + energy` first-stage boundary，转去推进下一个成书模块。

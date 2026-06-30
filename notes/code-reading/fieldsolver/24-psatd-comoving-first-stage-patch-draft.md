# Comoving PSATD first-stage patch draft

绑定对象：

- `../warpx/Examples/Tests/nci_psatd_stability/test_2d_comoving_psatd_hybrid`
- `../warpx/Examples/Tests/nci_psatd_stability/CMakeLists.txt`
- `analysis_comoving_first_stage_draft.py`
- `scripts/analysis_comoving.py`
- `23-psatd-comoving-reference-calibration.md`

## 目标

这份草案不是最终要提交的 WarpX patch，而是把当前已经验证过的第一阶段 fallback 收成一个更接近 upstream 目录结构和 helper 风格的最小包。

当前草案的设计目标很克制：

1. 不引入新的 producer surface；
2. 不声称 energy gate 已经成立；
3. 先把 `finite + spike` 这条已被本地样本验证过的 analysis 路线整理成可上提的形状。

## 当前建议的 patch 形状

### 1. 新增 analysis helper

候选文件：

- `Examples/Tests/nci_psatd_stability/analysis_comoving.py`

当前在 `PIC-tutor` 中对应的草案资产是：

- `notes/code-reading/fieldsolver/analysis_comoving_first_stage_draft.py`
- `notes/code-reading/fieldsolver/comoving_first_stage_patch.diff`

它只做两件事：

- finite-field sanity
- spike-ratio gate

不做 energy gate，不做 `divE`/Gauss-law gate。

## 2. CMake wiring

当前建议的第一阶段 wiring：

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

这保留了现有 checksum surface，同时把 analysis 从 `OFF` 提升到一个真正执行的 helper。

为了避免后续再手工拼 patch，当前仓库还额外保存了一份 unified diff 草案：

- `notes/code-reading/fieldsolver/comoving_first_stage_patch.diff`

它只覆盖最小两处修改：

1. `CMakeLists.txt` 中把 comoving test 的 analysis 从 `OFF` 改成 `analysis_comoving.py`
2. 新增 `analysis_comoving.py`

### 3. 当前 hard-coded 草案常量

`analysis_comoving_first_stage_draft.py` 当前写入的候选阈值是：

```python
SPIKE_RATIO_MAX = 1.111482370205649
```

来源是：

- stable baseline `spike_ratio_ref_stable = 1.1103719982074416`
- safety factor `1.001`

这样做的目的不是宣称这个阈值已经能过全部 CI，而是为了给第一版 patch 提供一个明确、可审查、可复现实验来源的常量候选。

在当前本地样本上：

- stable comoving baseline：通过
- `no-comoving` sibling：失败

也就是说，这个阈值至少对当前 stable/contrast 对是有分辨力的。

## 为什么这里不带 energy gate

当前证据边界已经很清楚：

1. `no-comoving` 与 `no-galilean` sibling 的末态指标在本机上重合到 `1e-14` 相对误差量级，说明它们共享同一条 standard-PSATD unstable branch。
2. 对 Galilean family，这条 branch 能形成有效 energy ordering。
3. 对 comoving family，当前 stable comoving 并没有相对这条 branch 降低电场能量。

因此，若在第一阶段 patch 中仍然强行塞入 comoving `energy_ref/tol_energy`，就会把“尚未证实的 gate 语义”包装成“已经验证的 gate”。

这一步不值得冒险。更稳妥的第一阶段形状，就是把 patch 收敛到：

- finite sanity
- spike sanity
- checksum

等更好的 comoving unstable sibling 或更多平台样本到位后，再考虑第二阶段的 energy gate。

## 和 `scripts/analysis_comoving.py` 的关系

两者角色不同：

- `scripts/analysis_comoving.py`：本仓库内的可配置原型，便于继续探索 ledger、spike safety factor 和可选 energy gate。
- `analysis_comoving_first_stage_draft.py`：面向 WarpX 提交流的极简草案，目的是把第一阶段 patch 压到最小。

如果后续真的上提 WarpX patch，推荐流程是：

1. 先从 `analysis_comoving_first_stage_draft.py` 复制到 WarpX test 目录；
2. 对照 `comoving_first_stage_patch.diff` 检查 helper 文件名和 CMake wiring；
3. 仅改文件头注释、路径和必要的打印格式；
4. 保持第一阶段不引入 energy gate；
5. 单独在后续 patch 或 follow-up PR 中处理 energy gate / `divE` widening。

## 当前结论

从 `PIC-tutor` 的项目推进角度看，这份草案把当前模块又往前推了一步：

- 不再只是“文档上说可以做 `finite + spike`”
- 而是已经有了一份更接近 WarpX patch 目录结构的最小 helper 草案

这还不够支撑新的版本号，但已经足够作为下一轮继续推进的起点。

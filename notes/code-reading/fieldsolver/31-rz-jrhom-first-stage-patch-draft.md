# RZ JRhom LL2 first-stage patch draft

绑定对象：

- `../warpx/Examples/Tests/nci_psatd_stability/test_rz_psatd_JRhom_LL2`
- `../warpx/Examples/Tests/nci_psatd_stability/CMakeLists.txt`
- `analysis_rz_jrhom_first_stage_draft.py`
- `scripts/analysis_rz_jrhom.py`
- `30-rz-jrhom-input-numprocs-audit.md`

## 目标

这份草案不是最终要提交的 WarpX patch，而是把当前已经过 `mpi2` repeated/MPI 复核的 RZ JRhom LL2 helper 收成一个更接近 upstream 目录结构和 review 口径的最小包。

当前草案的设计目标很克制：

1. 不引入新的 producer surface；
2. 不声称 spike gate 已经必须一起上；
3. 先把 `finite + energy` 这条已被 `1 1` 和 `2-rank` 两轮排序共同支持的 analysis 路线整理成可上提的形状。

## 当前建议的 patch 形状

### 1. 新增 analysis helper

候选文件：

- `Examples/Tests/nci_psatd_stability/analysis_rz_jrhom.py`

当前在 `PIC-tutor` 中对应的草案资产是：

- `notes/code-reading/fieldsolver/analysis_rz_jrhom_first_stage_draft.py`
- `notes/code-reading/fieldsolver/rz_jrhom_first_stage_patch.diff`
- `notes/code-reading/fieldsolver/rz_jrhom_first_stage_provenance_note.md`
- `notes/code-reading/fieldsolver/rz_jrhom_first_stage_submission_packet.md`
- `notes/code-reading/fieldsolver/rz_jrhom_first_stage_pr_draft.md`
- `notes/code-reading/fieldsolver/rz_jrhom_first_stage_bundle/`
- `scripts/build_rz_jrhom_first_stage_patch.py`

它只做两件事：

- finite-field sanity
- energy gate

不做 spike gate，不做 `divE`/Gauss-law gate。

### 2. CMake wiring

当前建议的第一阶段 wiring：

```cmake
add_warpx_test(
    test_rz_psatd_JRhom_LL2
    RZ
    2
    inputs_test_rz_psatd_JRhom_LL2
    "analysis_rz_jrhom.py diags/diag1000025"
    "analysis_default_regression.py --path diags/diag1000025"
    OFF
)
```

这保留了现有 checksum surface，同时把 analysis 从 `OFF` 提升到一个真正执行的 helper。

为了避免后续再手工拼 patch，当前仓库还额外保存了一份 unified diff 草案：

- `notes/code-reading/fieldsolver/rz_jrhom_first_stage_patch.diff`

它只覆盖最小两处修改：

1. `CMakeLists.txt` 中把 `test_rz_psatd_JRhom_LL2` 的 analysis 从 `OFF` 改成 `analysis_rz_jrhom.py`
2. 新增 `analysis_rz_jrhom.py`

### 3. 当前 hard-coded 草案常量

`analysis_rz_jrhom_first_stage_draft.py` 当前写入的候选常量是：

```python
ENERGY_REF = 2.8020912961036427e+10
TOL_ENERGY = 9.7806649163175208e-01
```

来源是：

- mpi2 baseline `electric_energy = 2.7378937095024567e+10`
- mpi2 unstable reference `electric_energy = 2.8020912961036427e+10`
- safety factor `1.001`

这样做的目的不是宣称这个阈值已经能代表全部 future CI，而是为了给第一版 patch 提供一个明确、可审查、可复现实验来源的常量候选。

现在这些草案资产已经可以直接由下面这条命令重建：

```bash
python scripts/build_rz_jrhom_first_stage_patch.py
```

默认情况下，它读取：

- `runs/fieldsolver-validation/rz-reference-ledgers/rz-jrhom-reference-scan-mpi2.json`

并重写：

- `notes/code-reading/fieldsolver/analysis_rz_jrhom_first_stage_draft.py`
- `notes/code-reading/fieldsolver/rz_jrhom_first_stage_patch.diff`
- `notes/code-reading/fieldsolver/rz_jrhom_first_stage_provenance_note.md`
- `notes/code-reading/fieldsolver/rz_jrhom_first_stage_submission_packet.md`
- `notes/code-reading/fieldsolver/rz_jrhom_first_stage_pr_draft.md`
- `notes/code-reading/fieldsolver/rz_jrhom_first_stage_bundle/`

这一步把候选 `ENERGY_REF/TOL_ENERGY` 的来源、helper 内容、diff wiring、submission/provenance 说明、PR 草案和 staging bundle 统一绑回同一份 ledger，避免后续再出现多份文档和 helper 常量漂移。

## 为什么这里不带 spike gate

当前证据边界已经足够清楚：

1. `ll2-no-timeavg-cleaning` 在 `1 1` 和 `2-rank` 两轮里都稳定给出最高 `electric_energy`；
2. `ll2-timeavg-no-cleaning` 在两轮里都低于 baseline；
3. `cl1-timeavg-cleaning` 在两轮里都仍是源码级非法组合。

这说明第一阶段最该先收紧的，是 energy ordering 这条主合同，而不是继续把 patch 做成多重 gate。

更稳妥的第一阶段形状，就是先把 patch 收敛到：

- finite sanity
- energy sanity
- checksum

等 upstream review 真提出要更强的局部尖峰保护，再考虑第二阶段的 spike gate。

## 和 `scripts/analysis_rz_jrhom.py` 的关系

两者角色不同：

- `scripts/analysis_rz_jrhom.py`：本仓库内的可配置原型，便于继续探索 ledger、safety factor 和可选 spike gate。
- `analysis_rz_jrhom_first_stage_draft.py`：面向 WarpX 提交流的极简草案，目的是把第一阶段 patch 压到最小。

如果后续真的上提 WarpX patch，推荐流程是：

1. 先从 `analysis_rz_jrhom_first_stage_draft.py` 复制到 WarpX test 目录；
2. 对照 `rz_jrhom_first_stage_patch.diff` 检查 helper 文件名和 CMake wiring；
3. 对照 `rz_jrhom_first_stage_provenance_note.md` 保留阈值来源、`mpi2` ledger 路径和“为什么当前不带 spike gate”的 review 口径；
4. 对照 `rz_jrhom_first_stage_submission_packet.md` 保持提交摘要、review claim 和 follow-up boundary 的表述一致；
5. 对照 `rz_jrhom_first_stage_pr_draft.md` 直接复用 title/summary/out-of-scope/reviewer-checklist 的措辞；
6. 若需要直接交给另一个 worktree 或上游仓库，优先从 `rz_jrhom_first_stage_bundle/` 复制镜像目录，而不是手工重组资产。

## 当前结论

从 `PIC-tutor` 的项目推进角度看，这份草案把当前模块又往前推了一步：

- 不再只是“已有 repeated/MPI 验证过的 helper 原型”
- 而是已经有了一份更接近 WarpX patch 目录结构、review 口径和交接方式的最小 handoff 包

这还不够支撑新的版本号，但已经足够作为下一轮继续推进的起点。

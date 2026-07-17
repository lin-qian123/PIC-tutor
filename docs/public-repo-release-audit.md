# Public repository release audit

审计日期：2026-07-18

当前 release 为 v0.110；本版重新执行正式收敛 study 的第二组 12 个 2-rank producer，correction-on 14 项 repeat-slope gate 全部通过，最大绝对 slope 差为 `2.0135e-11`。分类为 `FORMAL_CONVERGENCE_REPEAT_SLOPE_GATE_PASS_CHARGE_CLOSURE_OPEN`，不把该结果写成 formal order 或 axis-charge closure。第 1--9 章入口已完成读者化审读；第 2、3、3A、4、5、8、9 章的深层证据段也已移除开发过程措辞和绝对工作区路径，并把读者入口改为相对链接。最新连续阅读将第 1--7 章和 3A 章的本地运行史改为源码快照、复现入口与适用范围；第 1 章补足 Debye 与统计尺度定义，第 2 章将时间组织和 AMR subcycling 改为离散一致性说明，第 3、3A 章将 Mermaid 源码和宽对象表改为可打印的路线表与对象落点说明，并在第 24、29、42、48 页视觉抽查。第 5 章补回形函数、守恒、时间层和 AMR 同步的读者主线，第 6 章按算法假设、可支持结论与证据边界重组，第 7 章则以边界闭合系统串联场、粒子、PML、guard cell 与 AMR。第 8 章的宽命令台账已替换为跨页的“观察量、结论与边界”矩阵，并在第 257--258 页视觉抽查；第 9 章统一为可核查性分层。其他章节的 Mermaid 清理、全书通读、route-count ledger、axis charge correctness、RZ implicit runtime、许可和公开再分发仍保持开放。

全书正文扫描确认绝对工作区路径与开发过程标记均为零。第 5 章两张宽表已由列式矩阵改为分组证据列表，并在 PDF 第 158--159 页人工复核；这只关闭该处的版式风险，不替代全书通读。

v0.78 完成 Esirkepov 2001 CPC indexed abstract 与 arXiv 预印本的 bounded compare；该 contract 只确认发表版 metadata/abstract 级算法主张已归类，不把 publisher-PDF 缺口写成已关闭。

当前 `dist/pic-tutor-v0.110.pdf` 页数以本轮构建验收为准；v0.75 及此前的构建记录均属于历史构建快照。

v0.66 审计发现合订 Markdown/HTML 含本机绝对路径和不可随公共仓库迁移的绝对链接；v0.67 已在 release 构建层修复，v0.75 延续该检查，并将验证合同摘要、文献 triage、沉积算法选择矩阵和 paper asset contract 纳入公共 allowlist；论文 `references/` 原始资产仍按逐篇许可边界排除。

v0.78 延续 `docs/public-evidence-index.{json,md}`，从本地 contract 生成去路径摘要，并加入 `docs/literature-pending-triage.md` 的 acquisition/read queue。摘要保留原始合同状态，并将 boundary、unproven、missing 分类单独标记；原始 `runs/` 仍排除，因此该摘要是公共证据目录，不是运行产物替代品。

本文件只记录发布边界和体积证据，不自动删除或移动工作区文件。真正 push 前仍需由维护者确认论文 PDF、图片和其他第三方材料的授权状态。

## 当前体积快照

| 路径 | 当前体积 | 发布判断 |
|---|---:|---|
| `runs/` | 约 3.1 GB | 本地运行产物；由 `.gitignore` 忽略，不应整体 push |
| `references/` | 约 174 MB | 逐篇检查版权/许可后再决定；不能默认整体公开 |
| `dist/` | 约 90 MB | 含多代历史 HTML/Markdown；不应把全部历史生成物当作当前 release |
| `dist/pic-tutor-v0.110.pdf` | 2,986,230 bytes / 265 页 | 当前成书候选，可单独审计后发布 |
| `dist/pic-tutor-v0.110.html` | 5,247,173 bytes | 自包含 MathJax + 15 张图片，可作为预览候选 |
| `dist/pic-tutor-v0.110.md` | 853,010 bytes | 当前合订源，可作为文本 release 候选 |

## 当前边界

- `runs/` 已加入忽略规则；本轮又忽略了根目录运行残留 `Backtrace.*` 和 `bmmntr.txt`。
- 当前书稿图表位于 `manuscript/assets/figures/`，源章节使用相对路径；`scripts/build_v96.py` 会在合订阶段解析资源。
- `dist/` 当前仍保留历史版本产物，发布时应明确选择 `v0.110`，不要按目录整体上传。
- `references/` 中的论文 PDF、MinerU 图片和讲解笔记应按论文逐项确认公开许可；本审计不把“本机可读”当作“可公开分发”。
- `README.md`、`TODO.md`、`manuscript/VERSION.md` 和本文件应在 push 前再次同步当前 release 选择。

## v0.110 建议发布清单

建议纳入公共仓库的项目内资产：

- `AGENTS.md`、`README.md`、`TODO.md`；
- `manuscript/` 书稿源、`manuscript/assets/figures/` 15 张验证图和 `manuscript/VERSION.md`；
- `scripts/build_v110.py`、`scripts/verify_v110_build.py`、`scripts/audit_reader_facing_content.py`、`scripts/audit_release_consistency.py`、`scripts/audit_rz_axis_correction_nonneutral_control.py`、`scripts/audit_rz_axis_correction_nonneutral_shape_family.py`、`scripts/audit_rz_axis_correction_nonneutral_density_triple.py`、`scripts/run_formal_convergence_repeat_family.py`、`scripts/analyze_formal_convergence_repeat_family.py`、`scripts/audit_formal_convergence_repeat_slope_gate.py` 及书稿引用的项目分析脚本；
- `docs/` 中的项目说明、验证矩阵、读者视角编辑审查和本发布审计；
- `docs/public-evidence-index.{json,md}`；
- `docs/transition-zone-route-contract.{json,md}` 与 `scripts/validate_transition_zone_route_contract.py`；
- `dist/pic-tutor-v0.110.md`、`dist/pic-tutor-v0.110.html`、`dist/pic-tutor-v0.110.pdf`，前提是维护者确认生成物的发布策略。

明确排除：

- `runs/`、`Backtrace.*`、`bmmntr.txt` 等本地运行和调试产物；
- `dist/` 中 v0.47 以前的历史生成物；
- `references/` 中未逐项确认公开许可的第三方 PDF、图片和转换产物；
- `warpx_used_inputs` 等根目录临时输出。

## 发布前命令

```bash
python scripts/build_v110.py
python scripts/verify_v110_build.py --build-log /tmp/pic-tutor-build-v110.log
python scripts/audit_release_consistency.py
git status --short
```

当前 v0.110 构建验收结果以 `scripts/verify_v110_build.py`、`scripts/audit_rz_axis_correction_nonneutral_control.py`、`scripts/audit_rz_axis_correction_nonneutral_shape_family.py`、`scripts/audit_rz_axis_correction_nonneutral_resolution_family.py`、`scripts/audit_rz_axis_correction_nonneutral_density_triple.py`、`scripts/audit_editorial_quality.py`、`scripts/audit_pdf_layout.py`、`scripts/audit_formal_convergence_preregistration.py`、`scripts/audit_formal_convergence_repeat_slope_gate.py`、`scripts/run_formal_convergence_repeat_family.py`、`scripts/analyze_formal_convergence_repeat_family.py`、`scripts/audit_rz_axis_charge_repeat_stability.py`、`scripts/analyze_rz_axis_divergence_stencil_contract.py`、`scripts/analyze_rz_axis_divergence_resolution_contract.py`、`scripts/analyze_rz_axis_divergence_fit_contract.py` 和 `scripts/audit_transition_zone_runtime_activation.py` 为准；route-count ledger、axis charge correctness、正式收敛阶、人工全书通读、许可和公开再分发仍保持开放。

v0.110 发布 allowlist 另见 `docs/v0.110-release-manifest.{json,md}`；总字节数以 manifest 的 `total_bytes` 为准，`runs/`、`references/`、历史 `dist/` 和调试残留均被排除。该 manifest 是审计输入，不自动执行 Git staging、commit 或 push。

验收脚本证明的是成书构建和资源合同，不替代第三方材料的版权审计，也不替代 GitHub 仓库最终 staged 文件清单审阅。

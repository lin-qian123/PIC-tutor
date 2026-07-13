# Public repository release audit

审计日期：2026-07-13

当前 release 为 v0.88；本版补齐 RZ Esirkepov correction-on shape=1/2/3/4 的 rho-side species decomposition 观测 family，并保留正式收敛第二组 family 的 2-rank runner 输入与产物合同。当前 MPI launcher、第二组独立 family、正式收敛阶、人工全书通读、许可和公开再分发仍保持开放。

v0.78 完成 Esirkepov 2001 CPC indexed abstract 与 arXiv 预印本的 bounded compare；该 contract 只确认发表版 metadata/abstract 级算法主张已归类，不把 publisher-PDF 缺口写成已关闭。

当前 `dist/pic-tutor-v0.88.pdf` 页数以本轮构建验收为准；v0.75 及此前的构建记录均属于历史构建快照。

v0.66 审计发现合订 Markdown/HTML 含本机绝对路径和不可随公共仓库迁移的绝对链接；v0.67 已在 release 构建层修复，v0.75 延续该检查，并将验证合同摘要、文献 triage、沉积算法选择矩阵和 paper asset contract 纳入公共 allowlist；论文 `references/` 原始资产仍按逐篇许可边界排除。

v0.78 延续 `docs/public-evidence-index.{json,md}`，从本地 contract 生成去路径摘要，并加入 `docs/literature-pending-triage.md` 的 acquisition/read queue。摘要保留原始合同状态，并将 boundary、unproven、missing 分类单独标记；原始 `runs/` 仍排除，因此该摘要是公共证据目录，不是运行产物替代品。

本文件只记录发布边界和体积证据，不自动删除或移动工作区文件。真正 push 前仍需由维护者确认论文 PDF、图片和其他第三方材料的授权状态。

## 当前体积快照

| 路径 | 当前体积 | 发布判断 |
|---|---:|---|
| `runs/` | 约 3.1 GB | 本地运行产物；由 `.gitignore` 忽略，不应整体 push |
| `references/` | 约 174 MB | 逐篇检查版权/许可后再决定；不能默认整体公开 |
| `dist/` | 约 90 MB | 含多代历史 HTML/Markdown；不应把全部历史生成物当作当前 release |
| `dist/pic-tutor-v0.88.pdf` | 3,467,472 bytes / 330 页 | 当前成书候选，可单独审计后发布 |
| `dist/pic-tutor-v0.88.html` | 5,841,331 bytes | 自包含 MathJax + 16 张图片，可作为预览候选 |
| `dist/pic-tutor-v0.88.md` | 1,154,859 bytes | 当前合订源，可作为文本 release 候选 |

## 当前边界

- `runs/` 已加入忽略规则；本轮又忽略了根目录运行残留 `Backtrace.*` 和 `bmmntr.txt`。
- 当前书稿图表位于 `manuscript/assets/figures/`，源章节使用相对路径；`scripts/build_v88.py` 会在合订阶段解析资源。
- `dist/` 当前仍保留历史版本产物，发布时应明确选择 `v0.88`，不要按目录整体上传。
- `references/` 中的论文 PDF、MinerU 图片和讲解笔记应按论文逐项确认公开许可；本审计不把“本机可读”当作“可公开分发”。
- `README.md`、`TODO.md`、`manuscript/VERSION.md` 和本文件应在 push 前再次同步当前 release 选择。

## v0.88 建议发布清单

建议纳入公共仓库的项目内资产：

- `AGENTS.md`、`README.md`、`TODO.md`；
- `manuscript/` 书稿源、`manuscript/assets/figures/` 16 张验证图和 `manuscript/VERSION.md`；
- `scripts/build_v88.py`、`scripts/verify_v88_build.py`、`scripts/audit_release_consistency.py`、`scripts/run_formal_convergence_repeat_family.py` 及书稿引用的项目分析脚本；
- `docs/` 中的项目说明、验证矩阵和本发布审计；
- `docs/public-evidence-index.{json,md}`；
- `docs/transition-zone-route-contract.{json,md}` 与 `scripts/validate_transition_zone_route_contract.py`；
- `dist/pic-tutor-v0.88.md`、`dist/pic-tutor-v0.88.html`、`dist/pic-tutor-v0.88.pdf`，前提是维护者确认生成物的发布策略。

明确排除：

- `runs/`、`Backtrace.*`、`bmmntr.txt` 等本地运行和调试产物；
- `dist/` 中 v0.47 以前的历史生成物；
- `references/` 中未逐项确认公开许可的第三方 PDF、图片和转换产物；
- `warpx_used_inputs` 等根目录临时输出。

## 发布前命令

```bash
python scripts/build_v88.py
python scripts/verify_v88_build.py --build-log /tmp/pic-tutor-build-v87-final.log
python scripts/audit_release_consistency.py
git status --short
```

当前 v0.88 构建验收结果以 `scripts/verify_v88_build.py`、`scripts/audit_editorial_quality.py`、`scripts/audit_pdf_layout.py`、`scripts/audit_formal_convergence_preregistration.py` 和 `scripts/run_formal_convergence_repeat_family.py` 为准；MPI launcher、第二组独立 family、正式收敛阶、人工全书通读、许可和公开再分发仍保持开放。

v0.88 发布 allowlist 另见 `docs/v0.88-release-manifest.{json,md}`；总字节数以 manifest 的 `total_bytes` 为准，`runs/`、`references/`、历史 `dist/` 和调试残留均被排除。该 manifest 是审计输入，不自动执行 Git staging、commit 或 push。

验收脚本证明的是成书构建和资源合同，不替代第三方材料的版权审计，也不替代 GitHub 仓库最终 staged 文件清单审阅。

# Public repository release audit

审计日期：2026-07-12

当前 `dist/pic-tutor-v0.62.pdf` 为 310 页，内含 12 张书稿验证图；v0.60 及此前的构建记录均属于历史构建快照。

本文件只记录发布边界和体积证据，不自动删除或移动工作区文件。真正 push 前仍需由维护者确认论文 PDF、图片和其他第三方材料的授权状态。

## 当前体积快照

| 路径 | 当前体积 | 发布判断 |
|---|---:|---|
| `runs/` | 约 3.1 GB | 本地运行产物；由 `.gitignore` 忽略，不应整体 push |
| `references/` | 约 174 MB | 逐篇检查版权/许可后再决定；不能默认整体公开 |
| `dist/` | 约 90 MB | 含多代历史 HTML/Markdown；不应把全部历史生成物当作当前 release |
| `dist/pic-tutor-v0.62.pdf` | 2,827,535 bytes | 当前 310 页成书候选，可单独审计后发布 |
| `dist/pic-tutor-v0.62.html` | 约 4.7 MB | 自包含 MathJax + 12 张图片，可作为预览候选 |
| `dist/pic-tutor-v0.62.md` | 约 1.0 MB | 当前合订源，可作为文本 release 候选 |

## 当前边界

- `runs/` 已加入忽略规则；本轮又忽略了根目录运行残留 `Backtrace.*` 和 `bmmntr.txt`。
- 当前书稿图表位于 `manuscript/assets/figures/`，源章节使用相对路径；`scripts/build_v62.py` 会在合订阶段解析资源。
- `dist/` 当前仍保留历史版本产物，发布时应明确选择 `v0.62`，不要按目录整体上传。
- `references/` 中的论文 PDF、MinerU 图片和讲解笔记应按论文逐项确认公开许可；本审计不把“本机可读”当作“可公开分发”。
- `README.md`、`TODO.md`、`manuscript/VERSION.md` 和本文件应在 push 前再次同步当前 release 选择。

## v0.62 建议发布清单

建议纳入公共仓库的项目内资产：

- `AGENTS.md`、`README.md`、`TODO.md`；
- `manuscript/` 书稿源、`manuscript/assets/figures/` 12 张验证图和 `manuscript/VERSION.md`；
- `scripts/build_v62.py`、`scripts/verify_v62_build.py` 及书稿引用的项目分析脚本；
- `docs/` 中的项目说明、验证矩阵和本发布审计；
- `dist/pic-tutor-v0.62.md`、`dist/pic-tutor-v0.62.html`、`dist/pic-tutor-v0.62.pdf`，前提是维护者确认生成物的发布策略。

明确排除：

- `runs/`、`Backtrace.*`、`bmmntr.txt` 等本地运行和调试产物；
- `dist/` 中 v0.47 以前的历史生成物；
- `references/` 中未逐项确认公开许可的第三方 PDF、图片和转换产物；
- `warpx_used_inputs` 等根目录临时输出。

## 发布前命令

```bash
python scripts/build_v62.py
python scripts/verify_v62_build.py --build-log /tmp/pic-tutor-build-v62-final.log
git status --short
```

当前 v0.62 构建验收结果：`pdf_pages=310`、源/合订图片链接均为 `12`、HTML 内嵌图片和图号范围检查全部通过。

v0.62 发布 allowlist 另见 `docs/v0.62-release-manifest.{json,md}`：当前包含 635 个项目文件、总计 `24,152,388` bytes；`runs/`、`references/`、历史 `dist/` 和调试残留均被排除。该 manifest 是审计输入，不自动执行 Git staging、commit 或 push。

验收脚本证明的是成书构建和资源合同，不替代第三方材料的版权审计，也不替代 GitHub 仓库最终 staged 文件清单审阅。

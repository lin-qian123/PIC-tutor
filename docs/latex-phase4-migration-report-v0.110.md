# PIC-tutor LaTeX Migration — Phase 4 Report (v0.110 → v0.120 暂定)

> 计划：`docs/latex-migration-plan.md`（Phase 4：Full-Book Closure and Edition Release）
> 基线：书稿 `v0.110`（Git 标签 `v1.0`，commit `e1faff5`）
> 本阶段：三主题全量构建、可复现双构建、版本标识、迁移报告、文档更新

## 1. 版本与产物

- **新版本标识（暂定）**：`v0.120` —— 原生 LaTeX 书稿的版本号，与 v0.110 Markdown 基线区分；**最终编号与公开发行待维护者批准**（Phase 1 决策点 + 再分发权利），不覆盖 v0.110 任何产物。
- 产物（`dist/latex/`）：

| 主题 | PDF | 页数 | 审计 | 超满 |
|---|---|---|---|---|
| academic（A4，打印优先） | `pic-tutor-v0.120-academic.pdf` | 404 | 12/12 PASS | 12（≤57 pt） |
| technical（Letter，连续阅读） | `pic-tutor-v0.120-technical.pdf` | 408 | 12/12 PASS | 7 |
| compact（A4，源码查阅） | `pic-tutor-v0.120-compact.pdf` | 373 | 12/12 PASS | 7 |

- `dist/latex/manifest.json`：累积记录三主题 PDF 的 SHA-256、源码 commit、引擎与字体、可复现标记。

## 2. 可复现性（Phase 4 退出 gate 第 1 项）

- `build_latex_book.py` 以 `SOURCE_DATE_EPOCH=0` 调用 latexmk；两次干净目录重建 **SHA-256 字节级一致**（验证记录：`8f9465bef213…`）。
- 引擎/字体已在 manifest 记录：XeTeX 3.141592653-2.6-0.999997（TeX Live 2025）、Songti SC / PingFang SC / Times New Roman / Menlo / Latin Modern Math。

## 3. 溯源与所有权（退出 gate 第 2、3 项）

全部 13 个源文件 ↔ 原生 .tex 映射（MD 保持冻结为迁移记录，不再编辑）：

| 源文件 | 目标 .tex | 状态 |
|---|---|---|
| `manuscript/VERSION.md` | `latex/frontmatter/publishing-note.tex` | 已迁移（MD 冻结） |
| `chapters/00-preface.md` | `latex/chapters/00-preface.tex` | 已迁移（MD 冻结） |
| `chapters/01-kinetic-models.md` | `latex/chapters/01-kinetic-models.tex` | 已迁移（MD 冻结） |
| `chapters/02-pic-loop.md` | `latex/chapters/02-pic-loop.tex` | 已迁移（MD 冻结） |
| `chapters/03-warpx-evolve.md` | `latex/chapters/03-warpx-evolve.tex` | 已迁移（MD 冻结） |
| `chapters/03a-warpx-initialization.md` | `latex/chapters/03a-warpx-initialization.tex` | 已迁移（MD 冻结） |
| `chapters/04-particle-pushers.md` | `latex/chapters/04-particle-pushers.tex` | 已迁移（MD 冻结） |
| `chapters/05-deposition-shapes.md` | `latex/chapters/05-deposition-shapes.tex` | 已迁移（MD 冻结） |
| `chapters/06-field-solvers.md` | `latex/chapters/06-field-solvers.tex` | 已迁移（MD 冻结） |
| `chapters/07-boundaries-amr.md` | `latex/chapters/07-boundaries-amr.tex` | 已迁移（MD 冻结） |
| `chapters/08-diagnostics-cases.md` | `latex/chapters/08-diagnostics-cases.tex` | 已迁移（MD 冻结） |
| `chapters/09-literature-roadmap.md` | `latex/chapters/09-literature-roadmap.tex` | 已迁移（MD 冻结） |
| `appendices/A-symbols.md` | `latex/appendices/A-symbols.tex` | 已迁移（MD 冻结） |

逐章溯源对比（代码块/显示公式/表格/图片）在 Phase 1–3 报告中逐项精确一致；全书内容保留抽查（各章真实句子 + 章节锚点）全部命中。自动化 PDF 健康检查（缺字/断链/缺图/空页/超满策略）三主题全 PASS。

## 4. 尚需人工复核（模型无图像输入，自动化代理已通过）

最终人工页级视觉复核清单（建议维护者对照执行）：
1. 标题页/出版说明/目录版式；
2. 章节开页与 running heads（fancyhdr 曾有 headheight 提示，已在布局中放行）；
3. 数学公式页与编号决策（当前不编号，是否引入编号待定）；
4. 代码密集页（fvextra 换行）与长表页（tabularx 跨页）；
5. 已知微超满清单（Phase 3 报告 §4.8：ch3 28.9pt、ch3a 57.4/13.7pt、ch4 5–11pt、ch5 六处 3.6–23.4pt）；
6. 14 张图的实际观感与浮动位置；
7. 卡片语义宏的视觉呈现（当前为加粗段落，是否升级为盒子待定）；
8. ch4 裸 `\clearpage` 保留/删除决策。

## 5. 发行边界

- `dist/latex/` 产物与 v0.110 一样受既有第三方材料再分发限制约束（publisher 文献等不出现在任何发行物中；`references/` 不入库）。
- 未创建 GitHub Release、未改写 `v1.0` 标签、未删除 `references/`、未选择许可证——均维持现状，待维护者决策。
- 公开分发风险登记不因本次迁移改变（LaTeX PDF 不新增第三方材料权利问题）。

## 6. 工具链与命令

```bash
python scripts/convert_markdown_chapter_to_tex.py manuscript/chapters/<NN>.md manuscript/latex/chapters/<NN>.tex   # 草稿转换（需人工规范化）
python scripts/build_latex_book.py --theme academic|technical|compact   # 干净构建 + manifest
python scripts/audit_latex_book.py --pdf dist/latex/pic-tutor-v0.120-<theme>.pdf --log build/latex/src/main-<theme>.log
```

构建树 `build/latex/` 为可丢弃中间产物（gitignore）；`manuscript/latex/` 为权威 LaTeX 源。

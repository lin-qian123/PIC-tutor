# PIC-tutor LaTeX Migration — Phase 1 Sample Report (v0.110)

> 计划：`docs/latex-migration-plan.md`（Phase 1：Native LaTeX Sample Book）
> 基线：书稿 `v0.110`（Git 标签 `v1.0`，commit `e1faff5`），275 页规范 PDF
> 范围：前言 + 第 1 章 + 第 2 章

## 1. 状态

- **构建**：`python scripts/build_latex_book.py --theme academic` 成功，产物 `dist/latex/pic-tutor-latex-sample-academic.pdf`（40 页，约 0.5 MB），`dist/latex/manifest.json` 记录 SHA-256、源码 commit、引擎与字体。
- **退出 gate 审计**：`python scripts/audit_latex_book.py` **全部 PASS**——无缺字、无未定义引用、无重复标签、无缺失文件/图、**0 处 overfull**、无硬错误、无空页、预期锚点齐全。
- 构建树 `build/latex/` 为可丢弃中间产物（已 gitignore），源树 `manuscript/latex/` 为权威源。

## 2. 溯源表（Markdown → LaTeX，样章范围）

| 源文件 | 目标 .tex | MD 行 | TeX 行 | 代码块 | 表格块 | 显示公式 | 行内公式(code/cpath) | 链接 | 卡片标签行 |
|---|---|---|---|---|---|---|---|---|---|
| `manuscript/chapters/00-preface.md` | `chapters/00-preface.tex` | 59 | 76 | 0 | 1 | 0 | 6 | 0 | 0 |
| `manuscript/chapters/01-kinetic-models.md` | `chapters/01-kinetic-models.tex` | 578 | 663 | 0 | 2 | 35 | 58 | 0 | 0 |
| `manuscript/chapters/02-pic-loop.md` | `chapters/02-pic-loop.tex` | 793 | 904 | 14 | 4 | 33 | 103 | 1 | 1 |

对照口径：
- 显示公式：MD 的 `$$` 定界行 ÷2 与 TeX 的 `\[` + `multline*` 一一对应（02 章 32 `\[` + 1 `multline*` = 33）。
- 代码块：`codeblock`/`consoleblock` 环境数与 MD 围栏块数一致（02 章 14 个）。
- 表格：MD 表格块（修正口径，分隔行不另计）与 `tabularx` 环境数一致。
- 行内 code/cpath：MD 反引号 span 数，TeX 中 `\code{...}` 与 `\cpath{...}` 合计。
- 章节内链：02 章 `[第 3 章…](03-warpx-evolve.md)` → `\chref{chap:03-warpx-evolve}{…}`（目标章未入册，按设计降级为纯文本）。

## 3. 内容保留抽查

从三个源章节抽取 17 个代表性句子（跳过代码/表格/公式行）与 6 个章节锚点，在 PDF 提取文本中逐一核对：**全部命中**。两个初判"缺失"均为误报（测试短语本身不在源文；`--` 在 LaTeX 中渲染为 en-dash `–`）。

## 4. 转换与人工规范化记录

转换助手 `scripts/convert_markdown_chapter_to_tex.py` 只产出草稿；下列为样章期间的人工规范化（记录在案，防止回归时被自动覆盖）：

1. **标题编号剥离**：MD 标题自带 `1.1 `、`2.3.1 ` 前缀，LaTeX 自动编号，转换器剥离避免"1.1 1.1"。
2. **标题中的数学**：包 `\texorpdfstring{$\omega_p$}{omega\_p}` 提供书签纯文本兜底（hyperref + unicode-math 直接转换 `\omega` 会报 `Improper alphabetic constant`）。
3. **标题中的代码**：`\cpath`（url 的 `\path`）在 moving argument（ToC/书签）中非法（`\Url Error`），标题内统一改为转义后的 `\texttt{...}`。
4. **行内代码**：无空格纯 ASCII token → 可断行的 `\cpath`（配合 `xurl` 任意字符断行）；含空格（`max_step = 1`）或含中文（`稳定`）→ 字面 `\code`（`\path` 会吞空格；Menlo 无 CJK 字形）。
5. **表格**：管道表 → `tabularx`（`ltablex` 保持跨页）＋ `L` 段落列（CJK 自动换行）；`llll` 固定列曾导致数百 pt 溢出，已弃用。
6. **超宽显示式**：02 章 2.6 的 `time-layer consistency + …` 单行显示式超宽 118 pt，规范为 `multline*` 三行（纯排版断行，无内容变化）。
7. **正文排版**：`\sloppy` + `\emergencystretch=3em` 抑制长 token 段落溢出；`\code` 中 `_`、`%` 由 `\detokenize` 保护。
8. **样章未覆盖项**：图片转换（`\includegraphics` 路径逻辑已实现但样章 0 图）、`sourceline` 卡片宏（01/02 章标签行少，卡片密集章在 Phase 3 的 05/07/08）。

## 5. 工具链记录

- XeTeX 3.141592653-2.6-0.999997（TeX Live 2025），latexmk 4.86a。
- 文档类 `ctexbook`；CJK 宋体 Songti SC、黑体 PingFang SC；Latin serif Times New Roman；mono Menlo；数学 Latin Modern Math。
- 宏包：booktabs、longtable、tabularx、ltablex、array、ragged2e、caption/subcaption、graphicx、fvextra、url、xurl、hyperref、cleveref、xcolor、tcolorbox、enumitem、fancyhdr、geometry、microtype、amsmath/mathtools/amssymb、unicode-math。

## 6. Phase 1 决策点记录（供批准）

| 决策项 | 样章采用 | 备注 |
|---|---|---|
| 文档类 | `ctexbook` | 编译验证通过 |
| 字体族 | Songti SC / PingFang SC / Times / Menlo / LM Math | 需在 build manifest 固定 |
| 代码策略 | `fvextra` Verbatim（breaklines）+ `xurl` `\cpath` | pygments 缺失，minted 不可用 |
| 表格策略 | `tabularx`（ltablex 跨页）+ `L` 段落列 | 不再用固定 `l` 列 |
| 公式编号 | 不编号（`\[`/`multline*`） | 与源稿一致；是否引入编号待全书决策 |
| 浮动策略 | figure `[htbp]`、caption 小字号加粗 | 样章无图，Phase 3 章节验证 |

## 7. 尚需人工视觉复核（模型无图像输入，以下为程序化代理）

- 标题页/前置页、目录、章节开页、公式页、代码密集页、长表页、章节边界——程序化抽查（文本锚点、缺字、空页、超满）已通过；**最终视觉验收需人工过目** PDF（40 页）。

## 8. 下一步（Phase 2：Foundation and Lifecycle Migration）

按计划顺序逐章迁移：`03-warpx-evolve` → `03a-warpx-initialization` → 附录 A →（Phase 3）04–09。每章执行：转换 → 人工规范化 → 交叉链接 → 编译 → 页级复核 → 内容溯源比对 → 所有权切换（MD 冻结为迁移记录）。

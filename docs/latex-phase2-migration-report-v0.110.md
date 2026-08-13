# PIC-tutor LaTeX Migration — Phase 2 Report (v0.110)

> 计划：`docs/latex-migration-plan.md`（Phase 2：Foundation and Lifecycle Migration）
> 基线：书稿 `v0.110`（Git 标签 `v1.0`，commit `e1faff5`）
> 范围：`03-warpx-evolve`、`03a-warpx-initialization`、附录 A（`A-symbols`）

## 1. 状态

- 三章均已完成：转换 → 人工规范化 → 纳入 `main.tex` → 干净构建 → 自动 gate 审计 → 内容保留抽查。
- 全书当前 115 页（前言 + 第 1–3A 章 + 附录 A），产物 `dist/latex/pic-tutor-latex-sample-academic.pdf`。
- 审计 `scripts/audit_latex_book.py`：**全部 PASS**——无缺字、无断链、无缺图、无空页、**3 处超满（28/14/57 pt，均在阈值内）**、无硬错误；扩展锚点覆盖第 3/3A 章与附录。

## 2. 溯源表（Phase 2 章节）

| 源文件 | 目标 .tex | MD 行 | TeX 行 | 代码块 | 表格 | 显示公式 | 行内代码span | 卡片标签行 |
|---|---|---|---|---|---|---|---|---|
| `03-warpx-evolve.md` | `chapters/03-warpx-evolve.tex` | 946 | 1128 | 23 | 9 | 9 | ~521 | 3 |
| `03a-warpx-initialization.md` | `chapters/03a-warpx-initialization.tex` | 1773 | 2107 | 63 | 4 | 10 | ~932 | 22 |
| `appendices/A-symbols.md` | `appendices/A-symbols.tex` | 131 | 190 | 0 | 5 | 2 | 78 | 0 |

对照口径：代码块（围栏 ↔ `codeblock`/`consoleblock`）、表格（MD 表格块 ↔ `tabularx`）、显示公式（`$$` 定界行÷2 ↔ `\[`+`multline*`）**逐项精确一致**；行内代码为近似（MD 反引号对含围栏内反引号，TeX 侧仅计转换后的 `\code`/`\cpath`）。

## 3. 内容保留抽查

从三章各取真实首句（源侧规范化：去反引号/加粗/`--`→en-dash）共 24 句 + 章节锚点，PDF 提取文本逐句核对：**全部命中**（初判缺失均为探测方式差异：行内截断、`_fp` 下划线字面渲染、中文引号、数学渲染）。

## 4. 转换器修复与人工规范化记录（Phase 2）

1. **列表状态机 bug（重要）**：`open_list` 原实现从不关闭更深的列表，导致兄弟项反复开新层、嵌套深度膨胀到 10 层（源文实际仅 2–5 层），触发 `Too deeply nested`。已重写为按深度正确关闭/复用；全 6 个章节重新生成，环境 begin/end 全部平衡，03a 最大深度降至 2。
2. **enumitem 深度扩展**：源书确有 5 层嵌套（03a），默认 4 层上限不足；`\setlistdepth{9}` + `\renewlist` + 各深度 label（itemize 1–9、enumerate 1–9）。
3. **表格单元格单行 `$$…$$`**（附录 A）：`$$s$$` 等行内显示式原被当成普通文本、内部 `_` 被转义；转换器新增 `SINGLE_LINE_DISPLAY_RE` 保护并归一化为 `$…$`。
4. **附录标题前缀**：`附录 A：…` 前缀剥离（ctexbook `\appendix` 自带编号）；`main.tex` 增加 `\appendix`。
5. **重新应用 2.6.1 multline 手工规范化**（转换器重新生成会覆盖手工编辑，已在 .tex 内注释提示）。
6. **已知微超满**：03 L565 表格 28 pt、03a L590 表格 14 pt、03a L1998 段落 57 pt（长代码 token 含空格不可断行），均 ≤ 阈值，留待视觉复核阶段决定是否拆行。

## 5. 工具链

与 Phase 1 相同：TeX Live 2025 + ctexbook + 已记录宏包；无新增外部依赖（enumitem 深度配置在 preamble）。

## 6. 下一步（Phase 3：Algorithm and Evidence-Dense Chapters）

按计划顺序迁移：`04-particle-pushers` → `05-deposition-shapes` → `06-field-solvers` → `07-boundaries-amr` → `08-diagnostics-cases` → `09-literature-roadmap`。注意 05/08 章含 14 张图（首次实际走 `\includegraphics` 路径）、07 章读者卡片密集、05/06 章有 `aligned` 长公式与证据矩阵表。

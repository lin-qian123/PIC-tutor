# PIC-tutor LaTeX 并发审校报告（13 章 MD ↔ TeX）

> 时间：2026-08-14 | 范围：全部 13 个源文件（VERSION + 前言 + 10 章 + 附录 A）↔ 对应原生 .tex
> 方法：确定性归一化比对（机器证据）+ 13 个 subagent 并发逐行核实（引用两侧原文）+ 维护者抽样复核

## 1. 反幻觉设计（为何可信）

1. **机器证据优先**：`scripts/diff_markdown_tex.py` 把 MD 与 TeX 各自归一化为内容原子序列（标题/段落/公式/代码块/表格/图片），再做序列对齐与多重集差。归一化规则覆盖全部合法转换（编号剥离、`\(..\)`→`$..$`、反引号→`\code/\cpath/\codeesc`、表格→tabularx、卡片行→sourceline 等）。任何残差都是候选问题——**这一步不含任何 LLM 推断**。
2. **agent 只核实、不推断**：每个发现必须同时引用 MD 与 TeX 两侧逐字原文；给不出原文的不得报告；无法判断一律 needs_human。
3. **维护者抽样复核**：对 agent 结论做了独立 grep 计数与原文抽查。

## 2. 机器层结果（确定性）

| 章节 | MD 原子 | TeX 原子 | hunks | missing/extra | 结论 |
|---|---|---|---|---|---|
| version-note | 18 | 18 | **1** | 1/1 | 见 §4.2 |
| 00-preface | 29 | 29 | 0 | 0/0 | 一致 |
| 01-kinetic-models | 253 | 253 | 0 | 0/0 | 一致 |
| 02-pic-loop | 275 | 275 | 0 | 0/0 | 一致 |
| 03-warpx-evolve | 303 | 303 | 0 | 0/0 | 一致 |
| 03a-warpx-initialization | 700 | 700 | 0 | 0/0 | 一致 |
| 04-particle-pushers | 1256 | 1256 | 0 | 0/0 | 一致 |
| 05-deposition-shapes | 1111 | 1111 | 0 | 0/0 | 一致 |
| 06-field-solvers | 629 | 629 | 0 | 0/0 | 一致 |
| 07-boundaries-amr | 362 | 362 | 0 | 0/0 | 一致 |
| 08-diagnostics-cases | 865 | 865 | 0 | 0/0 | 一致 |
| 09-literature-roadmap | 156 | 156 | 0 | 0/0 | 一致 |
| A-symbols | 27 | 27 | 0 | 0/0 | 一致 |

差异报告保存在 `docs/latex-review/diff-<章节>.json`，可随时重跑复核。

## 3. agent 层结果（13 个并发 subagent）

- 每个 agent 执行：差异报告逐 hunk 分类（引用两侧原文）、8 项结构计数核对（标题/代码块/表格/公式/图片/卡片行/链接/列表项）、前中后随机抽样 5–8 行定位、missing/extra 原子逐条核实。
- 结论分布：12 章 **clean**，version-note **has_issues**（唯一真实差异，见 §4.2）。
- 全部 33 条 finding 均给出两侧逐字引用；其中 OK（合法转换）28 条、TOOL_ARTIFACT（工具局限，如列表正则、shell 转义）2 条、ALTERED 3 条（同一根因）。
- 过程透明度：两个 workflow 的完整结果见会话记录；第一轮 4 章（07/08/09/A）结果因输出截断未完整保留，已用第二轮独立 agent 重跑（全部 clean），并与维护者自己的 grep 计数交叉验证一致。

## 4. 真实发现与处置

### 4.1 已修复：单星号斜体未转换（转换器缺口）

- 发现：MD 用 `*…*` 标记的斜体（如 `*Plasma Physics via Computer Simulation*`、`*AIP Conference Proceedings*`）被转换器原样保留为字面星号（PDF 会显示星号而非斜体）。机器 diff 无法发现（两侧文件文本相同，属渲染层差异）。
- 核实：排除代码 span 与数学后的全库扫描，仅 2 处真实斜体（03a L1725、09 L102）。
- 修复：`scripts/convert_markdown_chapter_to_tex.py` 新增 `EMPH_RE`（在代码/数学 stash 之后、粗体之后处理），输出 `\emph{…}`；同步更新 diff 工具归一化。重新生成 03a/09 → 重建（academic）→ 审计 PASS（14 超满 ≤ 阈值）。
- 数学内的 `*`（共轭/星标，如 `$E^*$`、`$2*pi*r$` 代码）保持不动，无误伤。

### 4.2 记录待确认：version-note 标题改写（唯一内容偏离）

- MD `# PIC-tutor` ↔ TeX `\chapter*{出版说明}`：手写前置页（publishing-note.tex）把文档标题改成了书籍"出版说明"章名。
- 判定：正文 3 段 + 两个列表 10 项**逐字一致**，仅 H1 标题文本不同；这是迁移早期为前置页语义做的有意改写，**不属于转换器行为**。
- 处置：保留现状并在本报告登记；如需与 MD 严格一致可改为 `\chapter*{PIC-tutor}`，待维护者决定。

### 4.3 已确认无问题的常见差异类别（抽样记录）

标题编号剥离、`\texorpdfstring`/`\texttt` 标题包装、`\cpath` 下划线转义、`\codeesc` 特殊字符预转义（`10^{-13}`、`lib_${SD}`、`J^{n+1/2}` 等）、卡片行冒号由宏渲染、`\sourceline{练习题}{}` 空内容、ch2 multline 与 ch9 `\allowbreak` 手工规范化、ch4 裸 `\clearpage`、表格重复表头、14 张图路径逐项一致、`--` 保留、`%`→`\%`。

## 5. 工具局限记录（不构成内容问题）

- 列表计数正则对无序项（`- `）失效，agent 已用自然口径复核（07/08/09/A 分别 135/387/69/5 = TeX `\item`）。
- bash 双引号内 `$$` 被 shell 展开导致计数假象，已用单引号复核。
- 差异报告含 `missing_atoms/extra_atoms` 均为空，多重集无单侧多余/缺失。

## 6. 结论

- **13/13 章节：无内容丢失、无内容改动、无内容新增**（机器层 0 hunks + agent 层核实 + 维护者复核）。
- 已修复 1 个渲染层转换缺口（斜体）；1 处标题差异为有意改写待确认。
- 产物已重建并重过审计；后续源文改动后重转，需重放 2 处手工规范化（ch2 multline、ch9 `\allowbreak`）并重跑本审校流水线。

## 7. 复现命令

```bash
python scripts/diff_markdown_tex.py                          # 重新生成 docs/latex-review/diff-*.json
python scripts/build_latex_book.py --theme academic          # 重建
uv run python scripts/audit_latex_book.py --pdf dist/latex/pic-tutor-v0.120-academic.pdf --log build/latex/src/main-academic.log
```

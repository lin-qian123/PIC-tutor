# PIC-tutor LaTeX Migration — Phase 3 Report (v0.110)

> 计划：`docs/latex-migration-plan.md`（Phase 3：Algorithm and Evidence-Dense Chapters）
> 基线：书稿 `v0.110`（Git 标签 `v1.0`，commit `e1faff5`）
> 范围：`04-particle-pushers`、`05-deposition-shapes`、`06-field-solvers`、`07-boundaries-amr`、`08-diagnostics-cases`、`09-literature-roadmap`

## 1. 状态

- **全部六章已迁移**并并入 `main.tex`（第 4–9 章 + 附录 A），原生书稿现为 **404 页**，产物 `dist/latex/pic-tutor-latex-sample-academic.pdf`（约 3.4 MB）。
- 自动退出 gate 审计 **全部 PASS**：无缺字、无断链、无缺图（**14 张图全部找到**）、无空页、无硬错误；超满 12 处（**全部 ≤ 57 pt**，策略阈值 40 处）。
- 这是全书 13 个源文件（VERSION + 前言 + 10 章 + 附录 A）中正文章节的最后一批；Phase 3 计划内的章节迁移完成。

## 2. 溯源表（Phase 3 章节，清单口径精确一致）

| 源文件 | 目标 .tex | MD 行 | TeX 行 | 代码块 | 表格 | 显示公式 | 图片 | 卡片标签行 | 章节链接 |
|---|---|---|---|---|---|---|---|---|---|
| `04-particle-pushers.md` | `04-particle-pushers.tex` | 2846 | 3367 | 52 | 6 | 64 | 0 | 12 | 0 |
| `05-deposition-shapes.md` | `05-deposition-shapes.tex` | 2437 | 3048 | 43 | 17 | 45 | 3 | 15 | 0 |
| `06-field-solvers.md` | `06-field-solvers.tex` | 2118 | 2345 | 101 | 5 | 54 | 0 | 0 | 0 |
| `07-boundaries-amr.md` | `07-boundaries-amr.tex` | 835 | 992 | 28 | 3 | 3 | 0 | 30 | 0 |
| `08-diagnostics-cases.md` | `08-diagnostics-cases.tex` | 1728 | 2171 | 43 | 5 | 17 | 11 | 15 | 0 |
| `09-literature-roadmap.md` | `09-literature-roadmap.tex` | 293 | 392 | 0 | 5 | 0 | 0 | 0 | 0 |

对照口径：代码块（围栏 ↔ `codeblock`/`consoleblock`）、显示公式（`$$` 块 ↔ `\[`）、表格（MD 表格块 ↔ `tabularx`）、图片（`![](...)` ↔ `includegraphics`）**全部精确一致**；行内代码为近似。05/08 章的 14 张图首次实际走通 `\includegraphics` 路径（图形路径 `../assets/figures/` 在构建树内解析）。

## 3. 内容保留抽查

六章真实正文句 + 章节锚点核对 PDF 提取文本：**全部命中**（初判缺失均复核为校验脚本的归一化口径差异：数学渲染、破折号、`\codeesc` 中的 `^` 等，无内容丢失）。

## 4. 转换器修复与人工规范化记录（Phase 3）

1. **`\cpath` 中 `%` 破坏参数扫描（重要）**：`\path{0.3%}` 的 `%` 在参数读取时被当注释符吞掉闭合括号，引发 `Runaway argument`。引入三类行内代码宏：`\cpath`（URL 安全字符、seqsplit 任意断行）、`\code`（detokenize、保空格）、`\codeesc`（预转义 `% # & ~ ^ \ { } $ _`）。
2. **`\code` 参数内的 `%` 同样破坏参数扫描**：`\code{0.3%}` 在 detokenize 之前 `%` 即开始注释；凡含特殊字符的 token 一律走 `\codeesc`。
3. **bash 变量 token（`lib_${SD}`）**：`$` 加入 `\codeesc` 转义表。
4. **表格单元格内数学含字面 `|`**（`$\max|x|$`）：重写列分割器为感知代码/数学 span（`$…$`、`$$…$$`、`\(…\)`、反引号）的分割，不再按裸 `|` 切。
5. **表格 X 列无法收窄（大超满 128–187 pt）**：根因是长标识符不可断行 + `\keepXColumns`；改 `\cpath`/`\codeesc` 用 `\seqsplit` 任意断行、移除 `\keepXColumns`、`<>` 加入 `\cpath` 字符集——ch5 三张表的 128/145/177/187 pt 超满全部消除。
6. **斜杠连接拉丁链不可断**（ch9 `front matter/abstract/section/PSTD/reflection/appendix`，101 pt）：LaTeX 默认不在 `/` 后断行；该单元格手工加 `\allowbreak`（已注释标记，转换器重生成会覆盖，需在最终稿重放）。
7. **ch2 2.6.1 超宽显示式**：再次应用 `multline*` 手工规范化（118 pt 消除）。
8. **已知微超满（保留，视觉复核阶段处理）**：ch3 表格 28.9 pt、ch3a 表格 13.7 pt / 段落 57 pt、ch4 5.2/11.6 pt、ch5 六处 3.6–23.4 pt——均 ≤ 57 pt，在策略阈值内。
9. **ch4 裸 `\clearpage`**（源文 Pandoc 遗迹，Phase 0 已登记）：按原样保留为分页命令，决策记录在 Phase 4 视觉复核。

## 5. 工具链

与 Phase 1/2 相同（TeX Live 2025 + ctexbook）；新增 `seqsplit` 宏包（行内代码断行）；无 pygments/minted 依赖。

## 6. 下一步（Phase 4：Full-Book Closure and Edition Release）

- 全主题构建（technical/academic/compact 三主题）与可复现性双构建验证。
- 新版本标识与 release manifest（不覆盖 v0.110 产物）。
- README/TODO/构建说明/版式审计/发行就绪审计/公开分发风险记录更新。
- 迁移报告（MD 冻结/退役清单 ↔ LaTeX 源）。
- 全书页级人工视觉复核（含上述已知微超满、卡片盒样式、公式编号决策）。

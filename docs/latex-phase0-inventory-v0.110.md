# PIC-tutor LaTeX Migration Phase 0 Inventory (v0.110)

> 生成：`scripts/inventory_latex_phase0.py`（纯标准库，可重复运行）。
> 基线：Git 标签 `v1.0`（commit `e1faff5`），书稿版本 `v0.110`，275 页规范 PDF。

## 总计

- 源行数：**14,565**（非空 10,214）
- 代码块：**367**（2,629 行；缩进围栏定界行 2）
- 表格：**68** 块 / 465 行
- 显示公式：**272**（$$ 块 272 + equation 环境 0）；行内公式 **562**（`$...$` 92 + `\(...\)` 470）；段内单行 $$..$$ 1
- 图片：**14**
- 链接：**17**（章节内链 3、图内链 14、外链 0）
- 读者卡片标签行：**100**

## 按源文件清单

| 源文件 | 角色 | 行数 | 代码块 | 表格块 | 显示公式 | 行内公式 | 图片 | 链接 | 卡片标签 | 目标 .tex |
|---|---|---|---|---|---|---|---|---|---|---|
| VERSION | version-note | 27 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | `manuscript/latex/frontmatter/publishing-note.tex` |
| 00-preface | preface | 59 | 0 | 1 | 0 | 9 | 0 | 0 | 0 | `manuscript/latex/chapters/00-preface.tex` |
| 01-kinetic-models | chapter | 578 | 0 | 2 | 35 | 78 | 0 | 0 | 0 | `manuscript/latex/chapters/01-kinetic-models.tex` |
| 02-pic-loop | chapter | 793 | 14 | 4 | 33 | 88 | 0 | 1 | 2 | `manuscript/latex/chapters/02-pic-loop.tex` |
| 03-warpx-evolve | chapter | 946 | 23 | 9 | 9 | 44 | 0 | 2 | 4 | `manuscript/latex/chapters/03-warpx-evolve.tex` |
| 03a-warpx-initialization | chapter | 1773 | 63 | 4 | 10 | 1 | 0 | 0 | 22 | `manuscript/latex/chapters/03a-warpx-initialization.tex` |
| 04-particle-pushers | chapter | 2846 | 52 | 6 | 64 | 109 | 0 | 0 | 12 | `manuscript/latex/chapters/04-particle-pushers.tex` |
| 05-deposition-shapes | chapter | 2437 | 43 | 17 | 45 | 112 | 3 | 3 | 15 | `manuscript/latex/chapters/05-deposition-shapes.tex` |
| 06-field-solvers | chapter | 2119 | 101 | 5 | 54 | 63 | 0 | 0 | 0 | `manuscript/latex/chapters/06-field-solvers.tex` |
| 07-boundaries-amr | chapter | 835 | 28 | 5 | 3 | 4 | 0 | 0 | 30 | `manuscript/latex/chapters/07-boundaries-amr.tex` |
| 08-diagnostics-cases | chapter | 1728 | 43 | 5 | 17 | 50 | 11 | 11 | 15 | `manuscript/latex/chapters/08-diagnostics-cases.tex` |
| 09-literature-roadmap | chapter | 293 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | `manuscript/latex/chapters/09-literature-roadmap.tex` |
| A-symbols | appendix | 131 | 0 | 5 | 2 | 4 | 0 | 0 | 0 | `manuscript/latex/appendices/A-symbols.tex` |

## 工具链与字体记录（本机）

- `xelatex`：XeTeX 3.141592653-2.6-0.999997 (TeX Live 2025)
- `latexmk`：Latexmk, John Collins, 27 Dec. 2024. Version 4.86a
- `pandoc`：/opt/homebrew/bin/pandoc
- 宏包：找到 17 个 / 缺失 无
- pygments：MISSING (minted external dependency)
- 中文字体（fc-list :lang=zh）：53 个，含 .Hiragino Sans GB Interface,.Hiragino Sans GB Interface W3, .Hiragino Sans GB Interface,.Hiragino Sans GB Interface W6, .LastResort, Apple LiGothic, Apple LiSung, Arial Unicode MS, Hei, Kai …

## 正文待转义字符（LaTeX 敏感，代码/数学/表格/标题之外）

- `_`：14 处
- `%`：2 处
- `\`：1 处

## 各章待转义字符样例（前 5 处）

### 01-kinetic-models

- `%` ×1：L400: 这既不是“能量只能增加 0.3%”，也不是“严格守恒”：代码取绝对值，所以正、负漂移都受约束；而阈值只约束 producer 所写出的采样时

### 04-particle-pushers

- `_` ×7：L1924: **第一层：带质量粒子的 momentum--position 链。**若改动的是  分派、 或  的显式带质量路径，先回到 。它固定一个 
- `_` ×7：L1928: **第二层：输出时间层，而不是轨道算法。**若改动的是 、diagnostic 写出时机或速度同步代码，应使用 。它以常量 (E_z) 推进
- `_` ×7：L1946: 实际排错可以遵循一个简短顺序：先问被改的是带质量 momentum/position、diagnostic time level、massl
- `%` ×1：L2204: - 粒子总能量相对初值偏离不超过 2%
- `\` ×1：L1930: \clearpage

### 05-deposition-shapes

- `_` ×4：L1152: Direct current deposition 的核心 kernel 是 。它选择一个时间中心位置，按各分量 staggering 生成
- `_` ×4：L1257: 最后的 3D 写回由三个同构的方向 prefix loop 构成。以 (J_x) 为例，等价阅读伪代码为：

### 06-field-solvers

- `_` ×2：L686: 源码先按上式把实/虚 component 组合为 (F_p,F_m)，再分别对它们应用 。这是**等价阅读伪代码**：

### 08-diagnostics-cases

- `_` ×1：L838: 、、 on particlestmpParticleIO.cppdiag_type = FullBackTransformedBoundar

## 内部章节互链（需映射为 \label/\cref）

- `03-warpx-evolve.md` ×1
- `04-particle-pushers.md` ×1
- `05-deposition-shapes.md` ×1

## 迁移计划一致性备注

- 计划原文「约 43,800 行」与实际源行数不符，本清单以实测为准（见“总计”）。
- 行内数学为 `$...$` 与 `\(...\)` 双语法混合（共 {t['inline_math']} 处），转换器需同时处理；显示数学全部为 `$$..$$` 块（272 个），无 `\[...\]`、无 equation/align 环境。
- 正文存在 1 处裸 LaTeX 命令 `\clearpage`（第 4 章 L1930），为 Pandoc 时代的排版遗迹，需在 native 章节中显式决策保留或删除。
- 存在 1 处缩进代码围栏（第 5 章 L2227，3 空格缩进 ` ```text`），转换器围栏识别必须覆盖 0–3 空格缩进。
- 正文中 `(J_x)`、`(E_z)`、`(F_p,F_m)` 等带下划线标识符以纯文本（非数学、非代码）出现，需按 `\texttt{}` 处理并转义 `_`。

## Phase 0 退出 gate 验证记录

- 清单覆盖：13 个源文件全部在表（VERSION + 前言 + 第 1--9 章含 03a + 附录 A）。
- `uv run --with pypdf python scripts/verify_v110_build.py` → `[PASS] all v0.110 artifact checks`（275 页 PDF、章节标题、图片链接、读者化合同等全部通过）。
- `uv run python scripts/audit_release_consistency.py` → `passed: true`（README/VERSION/release manifest 与 v0.110 口径一致）。
- 结论：Phase 0 退出条件满足；基线 PDF 未被 LaTeX 迁移工作改动。

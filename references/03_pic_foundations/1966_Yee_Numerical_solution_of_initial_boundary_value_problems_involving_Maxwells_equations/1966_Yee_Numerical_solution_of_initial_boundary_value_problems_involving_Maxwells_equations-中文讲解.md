# Yee 1966 索引摘要级中文讲解

## 证据范围

本笔记使用 IEEE 书目信息和 OpenAIRE/Crossref 聚合记录公开的 indexed abstract。当前没有 IEEE 原文 PDF、MinerU Markdown 或论文图表，因此不把该摘要扩写成原文推导。

## 摘要主线

摘要将 Maxwell 方程替换为一组有限差分方程，并强调场点位置的选择与边界条件之间的关系：适当安排 field points 后，可以处理包含 perfectly conducting surfaces 的边界问题。摘要还给出一个 perfectly conducting cylinder 的电磁脉冲散射示例。

对 PIC-tutor 而言，这三点只足以固定历史来源的最小边界：Yee 论文讨论的是 Maxwell initial/boundary-value problem 的 finite-difference realization，场点布局不是排版细节，而是边界可实现性的一部分；圆柱散射是摘要中明确给出的验证对象。当前不能从 indexed abstract 推出论文正文的完整 stencil、时间层公式、离散色散推导或图表数值。

## 与 PIC-tutor 的连接

- 第 2 章：为 Yee/FDTD 的 staggered field-point 与 PEC boundary 叙述提供历史来源边界；
- 第 6 章：把 `EvolveB/E`、`CartesianYeeAlgorithm` 和 CFL 说明与原始 finite-difference solver 谱系对齐；
- PML/边界章节：只引用“field placement 与 conducting boundary”这一摘要级历史动机，不宣称当前 WarpX PML 等价于论文示例。

当前证据等级：`indexed-abstract-backed + metadata-verified; IEEE full-text missing`。

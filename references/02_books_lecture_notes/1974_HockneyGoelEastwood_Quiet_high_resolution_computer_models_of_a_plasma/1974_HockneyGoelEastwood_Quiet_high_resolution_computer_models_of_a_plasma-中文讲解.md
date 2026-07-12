# Hockney、Goel 与 Eastwood 1974 摘要级中文讲解

## 证据范围

本笔记只使用 ScienceDirect 文章记录公开的摘要和书目信息。当前没有本地 publisher PDF、MinerU Markdown 或图表，因此不把摘要内容扩写成全文推导。

## 摘要主线

论文摘要提出两种高分辨率粒子模型。Quiet Particle-Mesh（QPM）使用 Gaussian-shaped charge cloud，并对势函数求解做 shaping；摘要将它描述为在保留较低计算成本的同时显著降低传统 CIC 噪声的方案。混合 Particle-Particle/Particle-Mesh（PPPM）则在 mesh 计算之外，对邻近粒子加入直接求和修正，从而让有效空间分辨率可以小于一个 mesh cell，但代价是更高的计算量和更少的适用粒子数规模。

## 与 PIC-tutor 的连接

- 第 1 章：把 finite-size cloud、mesh noise 和 sub-mesh resolution 放入同一 particle-mesh 建模谱系；
- 第 5 章：说明 shape/smoothing 与 potential correction 共同改变 source-to-field 的离散合同；
- 第 6 章：为 noise reduction、potential correction 和高分辨率 particle-mesh route 提供摘要级历史来源。

当前证据等级：`abstract-backed + metadata-verified; full-text missing`。

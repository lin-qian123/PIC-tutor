# Eastwood 与 Hockney 1974 摘要级中文讲解

## 证据范围

本笔记只使用 ScienceDirect 文章记录公开的摘要和书目信息，不把摘要级结果写成论文全文或图示已核对。

## 摘要主线

论文摘要把二维 particle-mesh 的 charge-sharing scheme 排成一个有序层级：NGP 和 CIC 是低阶入口，高阶九点方案中又比较 triangular-shaped 与 Gaussian-shaped cloud。它还引入 potential-correction coefficients，修改 Fourier potential solve 中的乘因子，用来改善短程 force law。

摘要给出的关键量化结论是 force-law 的角向各向异性可以从 NGP/CIC 约 50% 降到低于 0.5%。这条结论对本书的作用不是直接证明 WarpX 当前 kernel 已复现该数值，而是说明 shape、potential correction 和 force isotropy 在 particle-mesh 体系中属于同一套离散误差设计问题。

## 与 PIC-tutor 的连接

- 第 1 章：补充 finite-size particle 与 force-law isotropy 的历史来源；
- 第 5 章：把 shape hierarchy 与 charge-sharing / force interpolation 的关系写得更完整；
- 第 6 章：为 spectral potential correction 和 solver-side noise/anisotropy 讨论提供摘要级来源。

当前证据等级：`abstract-backed + metadata-verified; full-text missing`。

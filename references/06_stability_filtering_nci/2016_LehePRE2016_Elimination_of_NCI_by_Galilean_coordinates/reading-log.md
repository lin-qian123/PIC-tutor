# Reading Log

## 2026-06-29

- 选定 Lehe et al. 2016 作为 v0.17 的 PSATD/Galilean/NCI 核心论文。
- 从 arXiv 下载 PDF 到本论文专属目录。
- 使用 MinerU 转换 PDF，得到 Markdown 和 `images/`，并把转换产物整理到同一论文目录。
- 新增中文讲解笔记 `2016_LehePRE2016_Elimination_of_NCI_by_Galilean_coordinates-中文讲解.md`。
- 回填目标：第 6 章 Galilean PSATD 小节，连接论文公式、WarpX `PsatdAlgorithmGalilean.cpp`、官方 boosted-frame 文档和 `nci_psatd_stability` regression。

后续接续点：把论文附录中的完整系数与 WarpX 源码中的 `X1-X4`、`T2`、`theta` 逐项对表，并继续补 Kirchen POP 2016 或 Godfrey PSATD/NCI 论文。

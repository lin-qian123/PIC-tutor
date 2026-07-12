# PSATD/NCI 文献—源码—运行策略矩阵

本 note 把第 6 章已有的三条 PSATD/NCI 文献线压成同一张可审计矩阵。它的作用是说明每篇论文负责哪一种机制、正文落到哪组 WarpX 源码、由哪类 regression 消费，以及不能从一条证据外推什么。

| 文献 | 第一性机制 | WarpX 源码对位 | runtime consumer | 不能外推 |
|---|---|---|---|---|
| Godfrey, Vay & Haber 2014 | fixed-grid PSATD 的 NCI 色散、filter/interpolation/current scaling 与时间步策略 | `PsatdAlgorithm*`、`warpx.use_filter`、finite-order PSATD | `nci_psatd_stability` 的 field-energy / Gauss-law 分支 | 不能把 fixed-grid filter 说成 Galilean 表示层面的 NCI 消除 |
| Lehe et al. 2016 | Galilean 坐标、移动网格相位与离散连续性方程 | `PsatdAlgorithmGalilean.cpp`、`rho_old_mod`、`psatd.v_galilean` | Galilean/current-correction `analysis_galilean.py` | 不能把 `v_galilean` 等同 moving window，也不能把 energy gate 当作完整色散证明 |
| Kirchen et al. 2016 | relativistically drifting plasma 的 boosted-frame workflow 与物理量回变换 | `warpx.gamma_boost`、`psatd.use_default_v_galilean`、boosted-frame 配置 | boosted-frame/LPA application evidence 与 Galilean regression | 不能把应用层回变换结果缩写成所有 Galilean/RZ/JRhom 分支均等价 |

`scripts/audit_psatd_literature_strategy_contract.py` 对三篇本地 PDF、MinerU Markdown、中文讲解、reading log、章节映射、源码关键词和 runtime consumer 做检查。报告位于 `runs/stage-c-validation/psatd-literature-strategy/contract.{json,md}`；当前 contract 是索引与证据分层，不新增物理 regression，也不替代各论文的原始公式逐行核对。

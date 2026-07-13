# Vranic 2015 论文资产

- 题目：*Particle merging algorithm for PIC codes*
- 作者：M. Vranic, T. Grismayer, J. L. Martins, R. A. Fonseca, L. O. Silva
- 期刊：Computer Physics Communications 191 (2015), 65--73
- DOI：`10.1016/j.cpc.2015.01.020`
- 本地 PDF：24 页
- MinerU Markdown：`2015_Vranic2015_Particle_merging_algorithm_for_PIC_codes.md`
- 图片目录：`images/`，32 张
- 中文精读：`2015_Vranic2015_Particle_merging_algorithm_for_PIC_codes-中文讲解.md`

## 项目用途

该文为第 4 章的粒子重采样/merge 解释提供 paper-backed 来源。它解释了为什么在一个六维 phase-space cell 内把粒子压成两个新宏粒子，可以同时保持局部权重、电荷、动量和能量；第 4 章再回到 WarpX 的 `VelocityCoincidenceThinning`，说明当前实现的输入参数、调用位置和验证边界。

这不是 WarpX 当前实现的逐行等价证明，也不是 `resampling` regression 已经复现论文全部数值案例的声明。

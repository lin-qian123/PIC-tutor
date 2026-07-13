# Muraviev et al. 2021 论文资产

- 题目：Strategies for particle resampling in PIC simulations
- 作者：A. Muraviev, A. Bashinov, E. Efimenko, V. Volokitin, I. Meyerov, A. Gonoskov
- 期刊：Computer Physics Communications 260 (2021) 107826
- DOI：10.1016/j.cpc.2021.107826
- 本地 PDF：`2021_MuravievCPC2021_Strategies_for_particle_resampling_in_PIC_simulations.pdf`
- MinerU Markdown：`2021_MuravievCPC2021_Strategies_for_particle_resampling_in_PIC_simulations.md`
- 图像目录：`images/`
- 中文精读：`2021_MuravievCPC2021_Strategies_for_particle_resampling_in_PIC_simulations-中文讲解.md`
- 访问审计：`access-audit.md`
- 阅读日志：`reading-log.md`

本文系统比较 simple、leveling、global leveling、number-conservative、energy-conservative、conservative、merge 和 merge-to-random-particle 等重采样策略。论文的核心贡献是把“平均保持任意分布”形式化为 agnostic down-sampling，并将严格守恒量、空间/动量分布均匀性、局部噪声和计算成本放在同一组测试中比较。

本资产用于第 4 章重采样方法谱系和第 9 章文献路线。论文实验使用 PICADOR/hi-chi 体系；它们可作为算法和误差机制的 paper-backed 来源，但不等同于 WarpX `Resampling` 当前实现，也不证明 WarpX 已复现 QED cascade 案例。

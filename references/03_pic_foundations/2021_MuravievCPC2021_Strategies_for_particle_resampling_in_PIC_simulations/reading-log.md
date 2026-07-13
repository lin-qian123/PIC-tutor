# Muraviev 2021 reading log

1. 确认论文讨论的是 down-sampling，区分 merging、thinning 和 complete resampling。
2. 记录 agnostic down-sampling 的两个条件：至少一个宏粒子权重变为零；每个原宏粒子的期望新权重等于旧权重。
3. 按论文顺序核对公式 (1)--(7)、图 1--12 和方法名 simple、leveling、globalLev、numberT、energyT、conserv、mergeAv、merge。
4. 复核稳态等离子体测试的温度下降、Weibel 测试的密度方差和 QED cascade 测试的增长率/权重尾部结论。
5. 将论文的 PICADOR/hi-chi 结果与 WarpX `Resampling`/`VelocityCoincidenceThinning` 分开；当前只建立算法概念映射，不宣称逐行等价或 runtime 复现。

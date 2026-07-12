# Peiravi--Birdsall 1978《一维热等离子体自热》中文讲解

## 0. 论文信息与证据范围

本文是 Berkeley Electronics Research Laboratory 的技术报告 `UCB/ERL M78/32`，作者为 A. Peiravi 与 C. K. Birdsall，日期为 1978-06-12。项目内保存了 UC Berkeley Digital Collections 提供的 40 页 PDF，并用 MinerU 生成了 Markdown 和 `images/`。

这里要区分三层事实：

1. 这是机构技术报告全文，不是已确认的期刊 publisher PDF；
2. 报告正文、图和附录可以按全文顺序阅读；
3. OCR 对表格、希腊字母和部分分数存在明显噪声，复杂表格的单个数字需要回看 PDF，不能只凭 MinerU 文本机械抄录。

## 1. 摘要：比较 NGP、CIC-PIC 和 QS 的自热

报告研究一维静电热等离子体中的数值自热，比较三种 weighting：零阶 NGP、线性 CIC-PIC 和二次 spline QS。作者把自热时间定义为热能翻倍所需的时间；对单一可动电子种群和固定中和离子背景，这等价于平均电子动能增加 `kT` 的时间。

核心观察是：自热来自有限空间网格和有限时间步导致的力涨落，因此它是数值起源、随机性质，并且同时依赖 `Delta x` 与 `Delta t`。报告还指出，适当的 k-space 截断可以在已有 weighting 基础上继续延长自热时间。

## 2. Section I：模型、热加载和历史结果的关系

作者使用带动量守恒的 ES1 一维静电代码，背景模型是可动电子加固定中和离子。热初态由 Maxwellian loader 生成，并使用一阶、二阶矩修正。这里的 loader 不是附属细节：如果初始均值或二阶矩偏离目标，早期 kinetic-energy 曲线会混入 loading error，不能直接解释成 mesh heating。

报告把 Hockney 的二维热等离子体工作作为比较背景，但增加了 QS weighting，并专门考察不同 weighting 的最佳参数路径。当前报告的价值在于把“shape order 会推迟自热”进一步变成一维可扫描的参数面；它不替代 Hockney 原始二维实验。

## 3. Section II：自热时间的定义和线性增长窗口

对 `omega_p Delta t <= 0.6` 的扫描，热能随时间近似线性增长，作者据此把自热解释为随机过程，并从线性增长段定义 `tau_h`。更大的时间步会改变增长形状，出现 `t^n`、`n>1` 的非线性增长；报告没有把后者强行归入同一个随机 heating law。

![Fig. 1: NGP 不同时间步下的平均速度平方增长](images/76c5eaf5b2215a2385aecb812e54810055d6b4b61d5dce60768eab08b23ada93.jpg)

图 1 的重要方法学信息是：有序但不 quiet 的初态会在真正的线性增长前产生短暂涨落。因此拟合 `tau_h` 时，作者把时间零点和初始热能放在线性增长段开始处。对本项目来说，这直接支持一个诊断要求：不要用包含 loading transient 的整段曲线拟合长期 stochastic heating。

## 4. Section III：`N_C+N_D` 与热化时间尺度

报告在固定 `lambda_0/Delta x` 下扫描密度或同时改变 `lambda_0` 与 `Delta x`，比较 `omega_p tau_h` 与 `N_D`、`N_C+N_D` 的关系。其工程结论是：

$$
\omega_p\tau_h \propto N_C+N_D,
$$

其中 `N_D` 是 Debye 长度内的粒子数尺度，`N_C` 是由网格尺度相关的粒子数尺度。这里的具体定义和符号在 OCR 表格中有混乱，但“固定 `lambda_0/Delta x` 时与 `N_C+N_D` 近似线性”的结构在正文和图注中是一致的。

![Fig. 2: 自热时间与粒子数尺度的线性关系](images/74a062fa22e5b203a6aa9e628528f5a2890f30ee31bb25b3f4a5d84feba0d897.jpg)

![Fig. 3: 不同 `lambda_0/Delta x` 下的 `N_C+N_D` 标度](images/378a04d2ec31b880bf6eefae5cf3392a7112e098ec9aa069baf49948b988c4b0.jpg)

这条关系与 Birdsall 13-5 中 `N_C` 控制 fluctuation/heating 的回链相互支持，但不能把两篇工作的实验维度、loader、代码和参数扫描当成同一数据集。

## 5. Section IV：不同 weighting 的 optimum path

作者把归一化后的 `omega_p tau_h` 对 `lambda_D/Delta x` 作图，并寻找最长自热时间附近的时间步路径。正文和结论给出的主结果是：NGP 的峰值附近约为

$$
v_t\frac{\Delta t}{\Delta x}\simeq\frac{3}{2},
$$

而 CIC-PIC 与 QS 的峰值附近约为

$$
v_t\frac{\Delta t}{\Delta x}\simeq\frac{1}{2}.
$$

摘要页的 OCR 对 CIC/QS 分数出现过噪声，本文以正文 Section IV 和 Section VII 的重复表述为准，不把摘要 OCR 的孤立字符当作另一条物理结论。

![Fig. 4: NGP 的归一化自热时间](images/fb8314673fee94276cc0f3b0c912cef7177af94dcb5608f99534380d0b390f17.jpg)

![Fig. 5: CIC 的归一化自热时间](images/465b0627239c8578f2abd6adff0164bd0e2b996f7b240aa4013f6a80ccd66008.jpg)

![Fig. 6: QS 的归一化自热时间](images/cf2388e9c31fb375a3633f0b7ddb5eb08c25b12e253cb2fa89af630894c8ef04.jpg)

这不是一个可直接写成 WarpX 通用 `dt` 推荐值的公式。它描述的是特定的一维静电、热等离子体、ES1、weighting 和扫描参数面；对 WarpX 只能作为“必须联合观察 `v_t Delta t/Delta x`、`lambda_D/Delta x` 和 shape family”的设计依据。

## 6. Section V：高阶 weighting 的收益必须除以计算成本

报告给出的量级比较是：CIC 的自热时间最多可达到 NGP 的约 70 倍，QS 最多可达到 NGP 的约 650 倍；但每粒子每步的成本也从 NGP 的约 5 微秒增加到 CIC 的约 11.6 微秒、QS 的约 24 微秒（原报告的 CDC-7600 MFE 测量）。因此作者定义 gain：

$$
\mathrm{gain}
\equiv
\frac{\text{self-heating time increase}}
{\text{computer-time increase}}.
$$

![Fig. 7: CIC/NGP 与 QS/NGP 的自热时间比](images/bf48d541adaad55d60c9fe4dc534a2cdb307763979d4dec0536dc0a021af6189.jpg)

![Fig. 8: 第二组时间步下的 scheme ratio](images/1c3364d06b5ed5ae7052e648e0f5d53edc49d3875eb644cb6a305154c3955b72.jpg)

![Fig. 9: 第三组时间步下的 scheme ratio](images/e541f4c3c711aaf1d92a1ecebcf2d046d46091e6ec9ddb8df3bb09b46204cdd0.jpg)

表 I 给出的 gain 量级说明：提高 shape order 的收益不能只看 `tau_h`，还要除以实际粒子推进和沉积成本。这正是本书在第 5 章讨论 shape family 时需要保留的性能边界。

## 7. Section VI：k-space truncation 的额外收益

报告使用简单的 Fourier-space truncation，删除超过 `k_last` 的模式，并研究 `omega_p tau_h` 随 `k_max/k_last` 的增长。结论是：NGP 的收益近似一次方，CIC 接近二次方，QS 接近三次方；统一写作

$$
\text{gain from truncation}
\propto
\left(\frac{k_{\max}}{k_{\mathrm{last}}}\right)^{n+1},
$$

其中 `n=0,1,2` 分别对应 NGP、CIC、QS。

![Fig. 10/11: k-space truncation 与自热时间](images/d5fb15ad68921c4c8d8237a0f14f55d33f40ace6d5c79948cd5d8e27b5fd473f.jpg)

图 10 的原始 OCR 图注很嘈杂，但正文结论清楚：高阶 weighting 与高波数截断是可叠加的误差控制手段。这里的 truncation 不是 WarpX `warpx.use_filter` 的逐行等价证明；它只能提供 filter/smoothing 为什么可能延长 thermal-plasma 观测窗口的历史依据。

## 8. Section VII：结论和使用边界

报告的结论可以压成四条：

1. `tau_h` 是一个长期数值健康度指标，而不是瞬时 field regression；
2. optimum path 依赖 weighting，不能把一个 NGP 的经验比例移植给 CIC/QS；
3. 高阶 weighting 通过降低短波误差延长自热时间，但应同时计算成本 gain；
4. k-space truncation 可以进一步抑制自热，但它仍需要单独评估对物理谱和目标 mode 的影响。

## 9. Appendix A：thermal loader、矩修正和早期 transient

附录 A 从一维 Maxwellian 开始讨论随机加载。基本分布可写成

$$
f(v)=\frac{1}{\sqrt{2\pi}v_t}
\exp\left(-\frac{v^2}{2v_t^2}\right).
$$

随机数加载的矩误差大约按 `N_P^{-1/2}` 降低。作者随后构造对称加载，使奇数矩更接近零，再用 Gitomer correction 在分组内修正均值和二阶矩：

$$
\bar v=\frac{1}{m}\sum_{i=1}^{m}v_i,
\qquad
\overline{v^2}=\frac{1}{m}\sum_{i=1}^{m}v_i^2,
$$

并以缩放因子把方差拉回目标 `v_t^2`。分组太小会产生规则的多束流或截断分布；分组增大后才逐步逼近 Maxwellian。报告说明，自热研究使用了改进后的 loader，使早期 heating slope 不主要由错误的初态矩主导。

![Appendix A: 矩修正后的速度分布](images/7f292398571a72e07c16b83087bd8452d63a1cd1692f30fcbc0da3d34c5683b4.jpg)

## 10. Appendix B：QS weighting 的冷等离子体色散检查

附录 B 用冷等离子体 dispersion 检查二次 spline weighting 的实现，并把数值交叉点与理论曲线比较。这个附录的意义不是证明热等离子体长期自热已经被控制，而是先确认 weighting kernel 在一个较干净的 cold-plasma mode 上没有明显实现错误。

![Appendix B: QS weighting 的冷等离子体色散](images/80537c294505e2b2601600f86cf41467d20b3e79d9e22949fc87ea814f66d015.jpg)

## 11. Appendix C：参数扫描表的证据等级

附录 C 列出 A/B/C 各组 case 的网格、粒子数、时间步、`lambda_D/Delta x`、`N_C+N_D`、截断波数和自热时间。MinerU 把这些大表转换成 HTML table 时存在列错位和字符损坏；因此本笔记只使用正文中重复出现的 scaling、optimum path 和 order-of-magnitude 结论，不逐项复制 case 数值。

## 12. 对 PIC-tutor 的回链

- 第 5 章：shape order、charge/current weighting 和 smoothing 不只是局部 stencil 选择，也改变长期 self-heating time；性能比较应包含成本归一化。
- 第 6 章：`lambda_D/Delta x`、`v_t Delta t/Delta x` 和 high-k filter 应作为联合参数面观察；报告的 optimum path 不是当前 WarpX universal constant。
- 第 8 章：thermal-plasma diagnostics 应从线性增长段拟合 stochastic heating，排除 loader transient，并保留 phase-space / energy-history 的窗口边界。
- `uniform_plasma` / `energy_conserving_thermal_plasma`：可借鉴 `tau_h` 与 `N_C+N_D` 的观测语言，但当前 regression 只证明其本地 runtime 合同，不证明 1978 报告的全参数面。

## 13. 一句话复习

Peiravi--Birdsall 1978 把“提高 weighting order、选择合适 `v_t Delta t/Delta x`、再做 k-space truncation”组织成一条可量化的自热控制路线，但它同时提醒我们：长期数值收益必须按真实计算成本归一化，并且初始 thermal loader 的矩误差要从 heating 诊断中剥离。

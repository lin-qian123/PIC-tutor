# Godfrey et al. 2014 PSATD PIC 数值稳定性分析中文讲解

## 0. 文献与本地文件

- 论文：Brendan B. Godfrey, Jean-Luc Vay, Irving Haber, "Numerical stability analysis of the pseudo-spectral analytical time-domain PIC algorithm", Journal of Computational Physics 258, 689-704, 2014.
- DOI：https://doi.org/10.1016/j.jcp.2013.10.053
- arXiv：https://arxiv.org/abs/1305.7375
- 本地 PDF：`2014_GodfreyJCP2014_Numerical_stability_analysis_of_the_PSATD_PIC_algorithm.pdf`
- MinerU Markdown：`2014_GodfreyJCP2014_Numerical_stability_analysis_of_the_PSATD_PIC_algorithm.md`
- 图片目录：`images/`

这篇论文给第 6 章提供的是 PSATD 数值 Cherenkov 不稳定性（NCI）的基准分析框架：从 PSATD 更新式出发，写出带空间 alias 和时间 alias 的离散色散关系，再比较不同电流沉积、current scaling、数字滤波和插值阶数对增长率的影响。它不是 Galilean PSATD 论文；它更像是 Galilean 方案出现前，对“固定网格 PSATD 如何抑制 NCI”的策略谱系整理。

## 1. 摘要：PSATD 没有普通 Courant 限制，但仍有 NCI

论文首先强调 PSATD 真空 Maxwell 方程在谱空间中可解析推进，因此没有传统意义上的 Courant 时间步限制，而且电磁波数值色散显著小于 FDTD/PSTD。这一点常让人误以为 PSATD 天然免疫 NCI。作者的核心纠正是：PSATD 不消除粒子-网格系统中的 beam alias；相对论束流与虚假 beam modes 耦合时，仍会出现数值 Cherenkov 不稳定性。

摘要中的关键结论有两层：

1. PSATD 的稳定性一般优于 FDTD/PSTD，但不是无条件稳定。
2. 在合适 PSATD-Esirkepov 变体、三次插值和数字滤波组合下，时间步满足 $c \Delta t \lesssim \Delta z$ 时，NCI 可以被压到很低。

对 WarpX 写作的直接含义是：不能只写“PSATD 没有 Courant 限制，所以 boosted-frame 稳定”。应写成“PSATD 改善电磁色散，但 boosted-frame 中的 NCI 仍需要 Galilean、滤波、current correction/source integration 等策略共同约束”。

## 2. 引言：NCI 是电磁模与虚假 beam alias 的耦合

引言先回顾 FDTD、PSTD 和 PSATD 的差别。FDTD 易并行但有数值色散；PSTD 用谱空间导数但时间推进仍有 Courant 限制；PSATD 在假设电流在一个时间步内常量时解析积分 Maxwell 方程，因此真空电磁波色散更优。

随后作者指出 NCI 的来源不是 Maxwell 真空推进本身，而是相对论束流在离散时空网格上的 alias。空间网格会让束流模出现

$$
k_z' = k_z + m_z \frac{2\pi}{\Delta z}, \qquad
k_x' = k_x + m_x \frac{2\pi}{\Delta x},
$$

时间采样又会引入整数 $p$ 对应的 temporal alias。当这些虚假 beam modes 与电磁模相交时，就会产生增长。论文后面的图 1 和图 2 正是把这个图像画出来。

![图 1：PSATD normal mode 中电磁模与虚假 beam modes 的交点](images/b18b7858f9571b46d2ce63d8cb500aab9ed1ccf04fe895a68b694eeda3d9a061.jpg)

图 1 的读法是：横轴为 $k_z$，纵轴为 $\omega$，电磁模和 $m_z=-1,0,+1$ 等虚假束流模在谱空间相交；最强 NCI 通常出现在这些交点附近。

![图 2：不同 alias 的共振曲线在 k 空间中的位置](images/bf17a978597279368623be3e0f2e696ec6b6050bec71f750a07ca9fc3b606808.jpg)

图 2 把相交条件转成 $(k_z,k_x)$ 空间中的共振曲线。对本书第 6 章而言，这张图解释了为什么“滤波”通常针对高 $k$ alias 有效：许多强共振点位于接近 Nyquist 的波数区域。

## 3. PSATD 算法：从解析场推进到电荷守恒约束

第 2 节给出 PSATD 的基本推进。作者使用谱空间波矢 $\mathbf{k}$，定义

$$
C = \cos(k\Delta t), \qquad S = \sin(k\Delta t),
$$

其中 $k=|\mathbf{k}|$，光速归一化为 1。整数时间层形式为

$$
\begin{aligned}
\mathbf{E}^{n+1} ={}& C\mathbf{E}^{n}
- iS\frac{\mathbf{k}\times\mathbf{B}^{n}}{k}
- \frac{S}{k}\mathbf{J}^{n+1/2}
+ (1-C)\frac{\mathbf{k}\mathbf{k}\cdot\mathbf{E}^{n}}{k^2} \\
&+ \left(\frac{S}{k}-\Delta t\right)
\frac{\mathbf{k}\mathbf{k}\cdot\mathbf{J}^{n+1/2}}{k^2},
\end{aligned}
$$

$$
\mathbf{B}^{n+1}
= C\mathbf{B}^{n}
+ iS\frac{\mathbf{k}\times\mathbf{E}^{n}}{k}
- i(1-C)\frac{\mathbf{k}\times\mathbf{J}^{n+1/2}}{k^2}.
$$

为了推导离散色散关系，论文把磁场改写到半时间层：

$$
\mathbf{E}^{n+1}
= \mathbf{E}^{n}
- 2iS_h\frac{\mathbf{k}\times\mathbf{B}^{n+1/2}}{k}
- \frac{S}{k}\mathbf{J}^{n+1/2}
+ \left(\frac{S}{k}-\Delta t\right)
\frac{\mathbf{k}\mathbf{k}\cdot\mathbf{J}^{n+1/2}}{k^2},
$$

$$
\mathbf{B}^{n+3/2}
= \mathbf{B}^{n+1/2}
+ 2iS_h\frac{\mathbf{k}\times\mathbf{E}^{n+1}}{k},
$$

其中 $S_h=\sin(k\Delta t/2)$。这组式子的重点不是形式复杂，而是它给出一个清楚的守恒条件：如果电流满足离散连续性方程

$$
\mathbf{k}\cdot\mathbf{J}^{n+1/2}
= -i\frac{\rho^{n+1}-\rho^n}{\Delta t},
$$

那么 Gauss law 可以在推进中保持。Esirkepov 型电流沉积的价值就在这里：它把 charge conservation 变成离散算法的结构性质。

论文随后引入 current scaling：

$$
\mathbf{J} = \boldsymbol{\zeta}:\mathbf{J}_e,\qquad
\boldsymbol{\zeta}=\mathrm{diag}(\zeta_z,\zeta_x,\zeta_y),
$$

其中 $\mathbf{J}_e$ 是 Esirkepovk 电流。这个操作可以改善稳定性，但通常不再严格保持原始连续性形式，因此需要使用含 $\rho^{n+1}-\rho^n$ 或等效补偿项的电场推进式。对 WarpX 不能简单把它等同为 `psatd.current_correction`：Godfrey 这里的 $\zeta$ 是为 NCI 增长率调制而引入的 k 依赖电流因子；WarpX 的 current correction 首先是连续性和 Gauss law 约束路径。

## 4. 离散色散关系：NCI 是矩阵行列式的非物理解

第 3 节把推进式做时间 Fourier 变换，使用 leapfrog 频率表示

$$
[\omega] =
\frac{\sin(\omega\Delta t/2)}{\Delta t/2}.
$$

电磁场方程、电流响应和粒子分布函数耦合后，色散关系可写成一个 $6\times 6$ 矩阵的行列式为零：

$$
\det \mathcal{D}(\omega,\mathbf{k})=0.
$$

这条式子是全篇的分析主线。它告诉我们：NCI 增长率不是靠观察某一个更新项猜出来的，而是离散 Maxwell 推进、插值函数、空间 alias、时间 alias 和束流响应共同决定的复频率根。

第 4 节把问题化到二维冷束流，变量为 $\{E_z,E_x,B_y\}$，得到 $3\times 3$ 矩阵：

$$
\begin{pmatrix}
\xi_{z,z}+[\omega] & \xi_{z,x} & \xi_{z,y}+[k_x] \\
\xi_{x,z} & \xi_{x,x}+[\omega] & \xi_{x,y}-[k_z] \\
[k_x] & -[k_z] & [\omega]
\end{pmatrix}
\begin{pmatrix}
E_z\\E_x\\B_y
\end{pmatrix}
=0.
$$

其中

$$
[k_z]=k_z\frac{\sin(k\Delta t/2)}{k\Delta t/2},\qquad
[k_x]=k_x\frac{\sin(k\Delta t/2)}{k\Delta t/2}.
$$

所有复杂的 $\xi$ 项包含电流/场插值、alias 求和、束流速度和 current scaling。物理解释是：电磁真空模由 $[\omega]^2-[k_z]^2-[k_x]^2=0$ 控制；粒子束的虚假 alias 通过 $\xi$ 项耦合进来，使本来实频率的根获得虚部。虚部 $\operatorname{Im}\omega>0$ 就是 NCI 增长率。

## 5. 近似增长率：滤波处理高 k，共振条件定位危险区域

第 5 节给出可用于理解的近似。真空 PSATD 模满足

$$
C_0=[\omega]^2-[k_x]^2-[k_z]^2,
$$

以及

$$
\sin^2\left(\omega\frac{\Delta t}{2}\right)
=
\sin^2\left(k\frac{\Delta t}{2}\right).
$$

因此 PSATD 在这个意义上没有传统 Courant 限制。但作者提醒：当 $k\Delta t$ 过大时，高波数段的频率行为会变差，所以过滤过高 $k$ 仍然是合理选择。

共振位置可概括为

$$
k_x^r =
\left[
\left(
\left(k_z+m_z\frac{2\pi}{\Delta z}\right)v
-p\frac{2\pi}{\Delta t}
\right)^2
-k_z^2
\right]^{1/2},
$$

其中 $m_z$ 是空间 alias，$p$ 是时间 alias。这个公式把“何处会不稳定”落在 $k$ 空间位置上：当电磁模与某个 alias beam mode 相交时，对应 $k_x^r$ 附近可能出现增长。

近似共振增长率写作

$$
\operatorname{Im}(\omega)
\simeq
\frac{1}{\Delta t}
\left|
\frac{n C_2\Delta t}{4k_z}
\right|^{1/3},
$$

非共振小 $k$ 增长率近似为

$$
\operatorname{Im}(\omega)
\simeq
\frac{\sqrt{4nC_0C_2-n^2C_1^2}}{C_0\Delta t}.
$$

这两个式子给出一个重要策略划分：

- 高 $k$ 共振 alias：数字滤波通常有效，因为目标模式靠近被滤掉的谱区。
- 小 $k$ 非共振增长：单纯高 $k$ 滤波可能不够，需要 current scaling 或改变算法表示。

![图 3：三次插值加数字滤波后的近似最大增长率](images/c11fec903026dddd2b2666a6fe65566d540ce15f43117ad9b5605b516bcc02fc.jpg)

图 3 显示 current scaling 选项对增长率的影响。option (c) 在该近似下几乎消除增长，这说明 $\zeta$ 的作用不是普通平滑那么简单，而是改变了色散关系中导致非物理根的系数组合。

## 6. 数值解：current scaling、数字滤波和插值阶数的组合效果

第 6 节数值求解完整色散关系，并与 WARP 模拟增长率对比。论文定义了四种选项：

- option (a)：$\zeta_z=(k_z\Delta z/2)\cot(k_z\Delta z/2)$，$\zeta_x=(k_x\Delta x/2)\cot(k_x\Delta x/2)$，等效于实空间 Esirkepov。
- option (b)：$\zeta_z=\zeta_x=1$，即 k 空间 Esirkepov 基准情形。
- option (c)：$\zeta_x=\zeta_z$，其中 $\zeta_z$ 按论文 Eq. (55) 选取，用于降低非物理共振阶数。
- option (d)：普通节点电流沉积。

![图 6：无数字滤波、线性插值时不同 PSATD 选项的最大增长率](images/016116fbfafcd2116b21c61a3f39e5897b23ee0c28d254fa52d515bcdd8e920c.jpg)

图 6 的要点是：option (a) 在较小时间步下比 option (b)/(d) 更稳，option (c) 对 $m_z=0$ 不稳定性抑制更强。理论增长率和 WARP 模拟点符合得很好，这验证了色散关系的可用性。

论文随后加入十次 bilinear filter（含 compensation passes）。作者特别提醒，current multipliers $\zeta$ 不是数字滤波器，尽管它们会带来某种平滑效果。这个区分对 WarpX 很重要：`warpx.use_filter = 1` 对应的是滤波/平滑家族；而 Godfrey 的 $\zeta$ 是当前谱空间稳定性分析中的 current scaling。

![图 7：数字滤波因子与 current scaling 因子的 k 空间形状](images/3c97062c383a10e44c486a0de57e6c4fdfa76cf06115d146eb0debc475e1fa46.jpg)

图 7 清楚显示 filter profile 和 $\zeta$ profile 是不同对象。filter 主要压制短波噪声和高 $k$ alias；$\zeta$ 进入色散矩阵的电流耦合项，会改变非共振增长条件。

![图 8：线性插值加数字滤波后的最大增长率](images/bed4bdc00fda309d1857aff9795f99b71d84dee9966bab61c2468791d97683b1.jpg)

![图 9：三次插值加数字滤波后的最大增长率](images/f60e7844ececc2e4469ab9612a0954a8be8ff17ad8c3b25828d8a632cb19fc9c.jpg)

图 8 和图 9 是本论文最可用的工程结论：数字滤波会显著降低增长率；三次插值进一步压低 NCI；option (a)/(c) 在相当宽的时间步范围内表现良好。对本书可以概括为：

$$
\text{PSATD NCI mitigation}
\approx
\text{current strategy}
+\text{spectral filtering}
+\text{higher-order interpolation}
+\text{time-step selection}.
$$

这也是 v0.19 要补到第 6 章的“策略谱系”。

## 7. PSTD 对照：PSATD 的优势不是只有滤波

第 7 节将 PSTD 作为对照。PSTD 的真空模满足

$$
\sin^2\left(\omega\frac{\Delta t}{2}\right)
=
\left(k\frac{\Delta t}{2}\right)^2,
$$

因此有更严格的 Courant 限制。论文图 12 和图 13 表明，在同样滤波和插值条件下，PSTD 的增长率在某些时间步范围内仍比 PSATD 大。作者解释为：PSTD 仍存在小 $k_x$ 区域的 $m_z=0$ 非共振不稳定，而 PSATD 在相同条件下没有这部分贡献或贡献更小。

![图 12：PSTD 线性插值无滤波增长率](images/124e6066fc488d2c24f5466241637ad7f734762bed194fe74528ee7aac13dc62.jpg)

![图 13：PSTD 三次插值加数字滤波增长率](images/e11ebe1ccc8a46bdbca71478f37f97b9a2926fc91602e9faca956ae89f60de31.jpg)

这部分给第 6 章的一个提醒是：不要把 PSATD 的优势简单写成“谱方法都一样”。PSATD 的解析时间推进和 PSTD 的有限差分时间推进会给出不同真空色散和不同 NCI 残差。

## 8. WARP 模拟验证：增长率最后回到场能量

第 8 节用二维 LPA boosted-frame 模拟验证理论。作者记录稳定参考模拟的最终总场能 $W_{f0}$，再计算测试模拟的 $W_f/W_{f0}$，用它判断 NCI 是否增长。

![图 14：线性插值、滤波后的 WARP LPA 场能比](images/badf4b86ed7228d05c6714c2960775d1754ae07cd81a8f9b8a3b06ce601d0b02.jpg)

![图 15：三次插值、滤波后的 WARP LPA 场能比，并与 CK/FDTD 对照](images/24256a618b29a70d7227f3dd5511b7d7675f6caaa4cf62acf19d523341d80441.jpg)

这个验证方式和 WarpX 的 `nci_psatd_stability/analysis_galilean.py` 很接近：WarpX regression 也用最终电场能量相对不稳定参考值的比例来验收 NCI 是否被压住。区别在于，Godfrey 论文验证的是 WARP 中 PSATD option/filter/interpolation 的色散理论；WarpX 当前 regression 验证的是 Galilean PSATD、averaged Galilean PSATD、current correction 和 JRhom 等实现路径是否保持稳定。

## 9. 与 WarpX 第 6 章的连接

### 9.1 `warpx.use_filter = 1` 属于数字滤波家族

WarpX 的 NCI regression 输入中，例如 `../warpx/Examples/Tests/nci_psatd_stability/inputs_base_2d`、`inputs_base_3d`、`inputs_base_rz`，都能看到

```ini
warpx.use_filter = 1
```

这应连接到 Godfrey 论文中的 digital filtering 结论：滤波主要用于压低高 $k$ alias 和短波噪声。第 6 章可以说它与 Godfrey strategy family 同源，但不能直接声称 WarpX 的 filter profile 就等于论文中的十次 bilinear filter，除非进一步核源码。

### 9.2 `psatd.current_correction` 不是 Godfrey 的 $\zeta$ current scaling

WarpX NCI 输入中有多组

```ini
psatd.current_correction = 1
```

而 `analysis_galilean.py` 会在 current correction 分支检查 Gauss law。它对应的是电荷守恒/连续性方程修正和谱空间 Gauss law 约束，不能和 Godfrey 论文中的 $\zeta_z,\zeta_x$ current multipliers 混为一谈。Godfrey 的 $\zeta$ 是为降低特定 NCI 增长率而进入色散矩阵的电流缩放因子；WarpX 的 current correction 首先是守恒约束。

### 9.3 Galilean PSATD 是表示层面的 NCI 消除策略

v0.17/v0.18 已经整理 Lehe 2016 和 Kirchen 2016。Galilean PSATD 把坐标/源项表示切到随等离子体漂移的网格速度 $v_\mathrm{gal}$，当 $v_\mathrm{gal}\approx v_0$ 时，均匀漂移等离子体的主要 NCI 可从表示层面被消除或显著压低。

因此本章应把策略谱系写成：

- Godfrey 2014：固定网格 PSATD 下的 NCI 色散分析、current scaling、数字滤波、插值阶数和时间步选择。
- Lehe 2016：Galilean PSATD 通过移动坐标/源项表示消除均匀漂移 NCI。
- Kirchen 2016：把 Galilean/hybrid Yee-FFT 思路放到 boosted-frame LPA 应用中验证效率和稳定性。

### 9.4 JRhom 属于源项时间积分家族

WarpX 的 `test_3d_uniform_plasma_psatd_JRhom_CC1`、`analysis_psatd_CC1.py` 和第 6 章的 `PSATD-JRhom` 小节关注的是一个 PIC 步内 J/rho 的多次沉积与时间积分假设。它可以服务于 NCI 抑制和守恒验证，但与 Godfrey 2014 中的 $\zeta$ current scaling 不是同一机制。

## 10. 本文对 v0.19 的可引用结论

1. PSATD 解析推进改善真空电磁色散，但相对论束流 PIC 仍存在 NCI。
2. NCI 来自电磁模与空间/时间 alias beam modes 的耦合；危险区域可由共振条件定位到 $k$ 空间。
3. 数字滤波主要压制高 $k$ 共振 alias；三次插值可进一步降低增长率。
4. Godfrey 的 current scaling $\zeta_z,\zeta_x$ 是 NCI 色散控制项，不能简单等同于 WarpX 的 `psatd.current_correction`。
5. WarpX 的 NCI regression 用 `warpx.use_filter`、Galilean PSATD、time averaging、current correction、JRhom 等组合构成实现侧验收；Godfrey 2014 给它提供“为什么这些策略需要分门别类讨论”的理论基线。

## 11. 后续需要继续核对的问题

- 核 `../warpx/Source/Filter` 与输入参数，确认 `warpx.use_filter = 1` 当前实际 filter profile 和 Godfrey 论文中的 bilinear smoothing/compensation 是否有直接对应关系。
- 核 `../warpx/Source/FieldSolver/SpectralSolver` 中 current correction 的具体实现式，避免把守恒修正写成 NCI-specific current scaling。
- 若 v0.20 继续 NCI 章节，优先补 Godfrey/Vay 后续 NCI suppression 论文，或直接从 WarpX 源码反推 current correction、finite-order PSATD 和 Galilean 分支的参数表。

# 第 6 章版本化证据台账

本台账保存从第 6 章读者正文移出的版本化增量、运行交接与详细系数记录。它们仍是审查书中公式、源码定位、论文资产和 runtime 边界的证据；读者正文则按算法选择、源项时间模型与验证边界组织，不要求按 v0.x 时间顺序阅读。

这些记录不自动升级为完整理论证明、WarpX 函数级等价、完整 geometry/order 覆盖或上游 CI 接入。

## 6.6 Cartesian PSATD、Galilean 与 NCI 记录

### 6.6.1 v0.26 `X1-X4` 系数的源码公式闭环

v0.26 把 `notes/code-reading/fieldsolver/17-psatd-x-coefficients.md` 回填到正文。这里的范围限定为 Cartesian `PsatdAlgorithmGalilean.cpp`：标准 PSATD 是 `v_galilean=0` 的极限，Galilean PSATD 则通过

$$
\omega_c=\mathbf{k}_c\cdot\mathbf{v}_{gal},\qquad
T_2=\exp(i\omega_c\Delta t)
$$

把旧时刻场和旧时刻电荷项移到 Galilean 网格。源码使用 centered modified k 计算 $\omega_c$，而使用 spectral solver 的 modified k 计算

$$
\omega_s=c|\mathbf{k}_s|,\qquad
C=\cos(\omega_s\Delta t),\qquad
S_{ck}=\frac{\sin(\omega_s\Delta t)}{\omega_s}.
$$

`S_ck` 在 $\omega_s=0$ 时直接取 $\Delta t$。这个零模分支非常重要，因为 `X1-X4` 里既有 $\omega_s^2-\omega_c^2$，也有 $\theta_c^\ast-\theta_c$ 这样的分母，不能用一个通式硬算所有模式。

四个系数在源码中的角色如下：

| 系数 | Galilean 通式或标准极限 | 更新式中的位置 | 解释 |
|---|---|---|---|
| `X1` | 通式为 `(1 - theta2_c*C + i*w_c*theta2_c*S_ck)/(epsilon0*(om_s^2-w_c^2))`；零模为 `dt^2/(2 epsilon0)` | `B_new` 中的 `i*X1*(k x J)` | 电流通过 Faraday/Ampere 耦合对磁场的贡献 |
| `X2` | `w_c!=0` 时由 `c^2*(theta_c_star*X1 - theta_c*tmp)/(theta_c_star-theta_c)` 给出；标准非零模为 `c^2*(dt-S_ck)/(epsilon0*dt*om_s^2)` | `E_new` 中 `-i*X2*rho_new*k` | 新时刻电荷对纵向电场的贡献 |
| `X3` | `w_c!=0` 时由 `c^2*(theta_c_star*X1 - theta_c_star*tmp)/(theta_c_star-theta_c)` 给出；标准非零模为 `c^2*(dt*C-S_ck)/(epsilon0*dt*om_s^2)` | `E_new` 中 `+i*T2*X3*rho_old*k` | 旧时刻电荷经 Galilean 相位后的纵向贡献 |
| `X4` | `i*w_c*X1 - theta2_c*S_ck/epsilon0`；标准 PSATD 为 `-S_ck/epsilon0` | `E_new` 中的 `X4*J` | 电流对电场的直接源项 |

因此，Cartesian standard/Galilean PSATD 的核心更新可以压缩成：

$$
\mathbf{E}^{n+1}
=T_2 C\mathbf{E}^{n}
+i c^2T_2 S_{ck}(\mathbf{k}\times\mathbf{B}^{n})
+X_4\mathbf{J}
-i(X_2\rho^{n+1}-T_2X_3\rho^n)\mathbf{k},
$$

$$
\mathbf{B}^{n+1}
=T_2 C\mathbf{B}^{n}
-iT_2 S_{ck}(\mathbf{k}\times\mathbf{E}^{n})
+iX_1(\mathbf{k}\times\mathbf{J}).
$$

这两个式子也说明为什么本章不能把 `X1-X4` 写成“稳定化系数”。它们首先是 PSATD 对源项积分的解析系数：`X1/X4` 管电流源项，`X2/X3` 管电荷源项，`T2` 管 Galilean 相位。`nci_psatd_stability` regression 里的 NCI 能量比和 Gauss-law 检查，是这些系数、current correction、filter、有限阶 modified k 和输入参数共同作用后的结果，而不是某一个 `X` 系数单独承担的验证。

本节还要保留三个边界。第一，time averaging 使用 `Psi*` 和 `Y*` 系数，不能只靠 `X1-X4` 描述平均场输出。第二，JRhom 使用 `PsatdAlgorithmJRhomFirstOrder/SecondOrder`，源项时间依赖和系数体系不同。第三，RZ、Galilean RZ、PML PSATD 都有各自的系数语义，不能把 Cartesian `PsatdAlgorithmGalilean.cpp` 的 `X1-X4` 直接搬过去。

### 6.6.2 v0.27 time-averaging Psi/Y 系数的源码公式闭环

v0.27 继续收束 `notes/code-reading/fieldsolver/18-psatd-time-averaging-coefficients.md`。这一节的重点不是普通 `E/B` 推进，而是 `psatd.do_time_averaging=1` 时写入 `Ex_avg...Bz_avg` 的 average-field 输出。源码边界很明确：`PsatdAlgorithmGalilean.cpp:76-85` 只有在 `time_averaging` 打开时才分配 `Psi1_coef`、`Psi2_coef` 和 `Y1-Y4`，而 `:98-101` 又断言 time averaging 必须配合 `psatd.update_with_rho=1`。

这说明 time averaging 不是一个只依赖电流的后处理开关。平均电场里实际含有 `rho_new/rho_old`：

```cpp
fields(i,j,k,Idx.Ex_avg) = Psi1 * Ex_old
                           - I * c2 * Psi2 * (ky * Bz_old - kz * By_old)
                           + Y4 * Jx + (Y2 * rho_new + Y3 * rho_old) * kx;
```

对应的向量形式可以写成：

$$
\langle\mathbf{E}\rangle
=\Psi_1\mathbf{E}^n
-ic^2\Psi_2(\mathbf{k}\times\mathbf{B}^n)
+Y_4\mathbf{J}
+(Y_2\rho^{n+1}+Y_3\rho^n)\mathbf{k},
$$

$$
\langle\mathbf{B}\rangle
=\Psi_1\mathbf{B}^n
+i\Psi_2(\mathbf{k}\times\mathbf{E}^n)
+iY_1(\mathbf{k}\times\mathbf{J}).
$$

这里的 `avg` 仍在谱空间。`WarpXEvolve.cpp:998-1007` 随后调用 `PSATDScaleAverageFields(1/(2*dt))` 和 `PSATDBackwardTransformEBavg(...)`，把谱空间平均场变成实空间的 `Efield_avg/Bfield_avg`，供后续 gather/通信/诊断路径使用。

`InitializeSpectralCoefficientsAveraging()` 使用的共享量和 `X1-X4` 相似，但积分区间不同。它定义

$$
\omega_s=c|\mathbf{k}_s|,\qquad
\omega_c=\mathbf{k}_c\cdot\mathbf{v}_{gal},
$$

并使用

$$
\theta_c=e^{i\omega_c\Delta t/2},\quad
\theta_c^2=e^{i\omega_c\Delta t},\quad
\theta_c^3=e^{i3\omega_c\Delta t/2},
$$

以及

$$
C_1=\cos(\omega_s\Delta t/2),\quad
C_3=\cos(3\omega_s\Delta t/2),\quad
S_1=\frac{\sin(\omega_s\Delta t/2)}{\omega_s},\quad
S_3=\frac{\sin(3\omega_s\Delta t/2)}{\omega_s}.
$$

于是旧场平均权重为：

$$
\Psi_1
=
\frac{
\theta_c^3(\omega_s^2S_3+i\omega_cC_3)
-\theta_c(\omega_s^2S_1+i\omega_cC_1)
}{
\Delta t(\omega_s^2-\omega_c^2)
},
$$

$$
\Psi_2
=
\frac{
\theta_c^3(C_3-i\omega_cS_3)
-\theta_c(C_1-i\omega_cS_1)
}{
\Delta t(\omega_s^2-\omega_c^2)
}.
$$

源码里 `Psi1` 的零模标准分支为 `1`，`Psi2` 的零模标准分支为 `-dt`。这个负号不能孤立解读，因为平均电场更新式里它前面还有 `-i*c2`，平均磁场更新式里则是 `+i`。

`Y1-Y4` 的角色也要分开。源码先构造内部辅助量

$$
\Psi_3=
\begin{cases}
-i(\theta_c^3-\theta_c)/(\Delta t\,\omega_c), & \omega_c\ne0,\\
1, & \omega_c=0,
\end{cases}
$$

然后把

$$
Y_1=
\frac{1-\Psi_1-i\omega_c\Psi_2}{\epsilon_0(\omega_s^2-\omega_c^2)}
$$

放入平均磁场的 $iY_1(\mathbf{k}\times\mathbf{J})$ 项。通用非零分支下，

$$
Y_2=
\frac{
ic^2(\epsilon_0\omega_s^2Y_1-\Psi_3+\Psi_1)
}{
\epsilon_0\omega_s^2(\theta_c^2-1)
},
\qquad
Y_3=
\frac{
ic^2(\Psi_3-\Psi_1-\epsilon_0\theta_c^2\omega_s^2Y_1)
}{
\epsilon_0\omega_s^2(\theta_c^2-1)
}.
$$

`Y2` 和 `Y3` 分别乘 `rho_new` 与 `rho_old`，因此它们是 average-field 的 charge endpoint 系数。最后

$$
Y_4=\frac{\Psi_2+i\epsilon_0\omega_cY_1}{\epsilon_0}
$$

是平均电场中的直接电流项。这样读，`Y1` 和 `Y4` 都与电流有关，但一个进入磁场旋度源，一个进入电场直接源；`Y2/Y3` 则与电荷端点有关。

这也给后续写作立了一个防混写规则：Cartesian `PsatdAlgorithmGalilean.cpp` 的 average-field `Y1-Y4`、JRhom second-order 的 `Y1-Y8`、RZ/Galilean RZ 的平均场系数和 PML PSATD 的 `C1-C25` 是不同算法族内的局部命名。正文可以比较它们服务的积分对象，但不能因为名字相同就合并成一张“PSATD Y 系数表”。

### 6.6.3 v0.17 文献闭环：Lehe et al. 2016 的 Galilean PSATD

v0.17 为本节补入第一篇 PSATD/Galilean/NCI 核心论文闭环：`references/06_stability_filtering_nci/2016_LehePRE2016_Elimination_of_NCI_by_Galilean_coordinates/2016_LehePRE2016_Elimination_of_NCI_by_Galilean_coordinates-中文讲解.md`。该笔记基于本地 PDF、MinerU Markdown 和论文图片，按论文顺序记录 Galilean 坐标、离散连续性方程、PIC cycle、二维稳定性分析和准柱坐标扩展。

这篇论文对本章最重要的判断是：Galilean PSATD 不是 moving window 的同义词。它首先把坐标改成

$$
\mathbf{x}'=\mathbf{x}-\mathbf{v}_{gal}t,
$$

于是 Maxwell 方程中的时间导数变成

$$
\left(\partial_t-\mathbf{v}_{gal}\cdot\nabla'\right),
$$

并且一个时间步内的电流近似也从“固定实验室网格点上常量”改为“固定 Galilean 网格点上常量”。这正是标准 PSATD 与 Galilean PSATD 在 NCI 行为上分开的根源。

对应到 current correction，Galilean 离散连续性方程不再是简单的

$$
-i\frac{\widehat\rho^{n+1}-\widehat\rho^n}{\Delta t}
+i\mathbf{k}\cdot\widehat{\mathbf J}^{n+1/2}=0,
$$

而是带有移动网格相位：

$$
-i\frac{\widehat\rho^{n+1}-\theta^2\widehat\rho^n}{\Delta t}
+i\mathbf{k}\cdot\widehat{\mathbf J}^{n+1/2}=0,
\qquad
\theta=\exp(i\mathbf{k}\cdot\mathbf{v}_{gal}\Delta t/2).
$$

这可以直接解释上面的源码：`rho_old_mod = rho_old * exp(i*k_dot_vg*dt)` 不是任意相位技巧，而是离散连续性方程在 Galilean 网格上的旧时刻电荷项。WarpX 官方 boosted-frame 文档 `../warpx/Docs/source/theory/boosted_frame.rst` 引用的 `bf-LehePRE2016` 正是这个推导来源；`../warpx/Examples/Tests/nci_psatd_stability/analysis_galilean.py` 则把论文中的稳定性判断变成 regression gate，用最终电场能量相对不稳定参考值的比例检查 NCI 是否被压住，并在 current-correction 分支继续检查 Gauss law。

因此，本书后面讲 `psatd.use_default_v_galilean` 时，不能把它写成经验开关。它的理论含义是：在 boosted-frame 或均匀流动等离子体问题中，让 Galilean 网格速度接近背景漂移速度 $\mathbf{v}_0$，使背景等离子体在数值网格中近似静止，从而移除主要 alias resonance。论文的二维稳定性分析和 Warp/FBPIC 数值实验都显示，最大增长率只在 $\mathbf{v}_{gal}\approx\mathbf{v}_0$ 附近降到零；取反方向的 Galilean 速度并不会自动稳定。

### 6.6.4 v0.18 文献闭环：Kirchen et al. 2016 的 boosted-frame 应用证据

v0.18 继续补入 Kirchen et al. 2016：`references/06_stability_filtering_nci/2016_KirchenPOP2016_Stable_discrete_representation_of_relativistically_drifting_plasmas/2016_KirchenPOP2016_Stable_discrete_representation_of_relativistically_drifting_plasmas-中文讲解.md`。这篇论文和 Lehe et al. 2016 的分工不同：Lehe 论文负责 Galilean PSATD 的推导、离散连续性方程和稳定性分析；Kirchen 论文负责说明该离散表示如何落到 Lorentz boosted-frame 等离子体加速 workflow。

在 boosted frame 中，实验室系静止的背景等离子体会以

$$
\mathbf{v}_{plasma}=-\beta c\,\mathbf{e}_z
$$

穿过计算域。Kirchen et al. 的关键选择就是让 Galilean 网格速度取同一个漂移速度：

$$
\mathbf{v}_{gal}=\mathbf{v}_{plasma}=-\beta c\,\mathbf{e}_z.
$$

这样背景等离子体在 Galilean 网格上静止，而激光、电子束等 elongated quantities 相对网格以修正后的速度传播。这个表述能把 WarpX 官方 boosted-frame 文档中的 `bf-KirchenPOP2016` 引用落成一句实际操作原则：`psatd.use_default_v_galilean` 应理解为把 `warpx.gamma_boost` 推导出的背景漂移速度交给 Galilean PSATD，而不是打开一个无物理来源的稳定化滤波器。

Kirchen 论文的应用图也给出一个读者侧验证顺序。第一，固定所有数值参数，只在 `v_gal=0` 和 `v_gal=-\beta c` 之间切换；标准 PSATD 出现强 NCI，Galilean PSATD 稳定。第二，把 boosted-frame 结果 back-transform 回实验室系，比较 $E_z$、$E_y$、激光腰斑、脉冲长度、电子束能量、能散和归一化发射度；结果在亚百分比量级内一致。也就是说，本节不能只写“Galilean PSATD 稳定”，还要写“稳定后仍保持加速器物理量”。

这也解释了 `nci_psatd_stability` regression 和更高层 boosted-frame example 之间的关系：前者用均匀流动等离子体和电场能量比做最小稳定性 gate；Kirchen 论文提供的是应用层证据，说明同一 Galilean 表示在激光等离子体加速的 boosted-frame workflow 中既抑制 NCI，又保持实验室系物理可比性。

### 6.6.5 v0.19 文献闭环：Godfrey et al. 2014 的 PSATD NCI 策略谱系

v0.19 补入 Godfrey, Vay, Haber 2014：`references/06_stability_filtering_nci/2014_GodfreyJCP2014_Numerical_stability_analysis_of_the_PSATD_PIC_algorithm/2014_GodfreyJCP2014_Numerical_stability_analysis_of_the_PSATD_PIC_algorithm-中文讲解.md`。这篇论文在本章中的位置应放在 Lehe/Kirchen 之前的理论基线：它不是 Galilean PSATD 论文，而是固定网格 PSATD 的 NCI 色散分析和抑制策略谱系。

论文的起点是 PSATD 场推进本身。谱空间中定义

$$
C=\cos(k\Delta t),\qquad S=\sin(k\Delta t),
$$

电场更新包含旋度场项、电流项和纵向投影项：

$$
\mathbf{E}^{n+1}
= C\mathbf{E}^{n}
- iS\frac{\mathbf{k}\times\mathbf{B}^{n}}{k}
- \frac{S}{k}\mathbf{J}^{n+1/2}
+ (1-C)\frac{\mathbf{k}\mathbf{k}\cdot\mathbf{E}^{n}}{k^2}
+ \left(\frac{S}{k}-\Delta t\right)
\frac{\mathbf{k}\mathbf{k}\cdot\mathbf{J}^{n+1/2}}{k^2}.
$$

PSATD 的真空电磁模没有普通 FDTD Courant 限制，但相对论束流 PIC 仍有 NCI，因为离散粒子-网格系统中存在空间 alias 和时间 alias。Godfrey et al. 把这一点写成离散色散矩阵：

$$
\det \mathcal{D}(\omega,\mathbf{k})=0,
$$

其中束流 alias 可写作

$$
k_z'=k_z+m_z\frac{2\pi}{\Delta z},
$$

而危险的共振位置满足类似

$$
k_x^r =
\left[
\left(
\left(k_z+m_z\frac{2\pi}{\Delta z}\right)v
-p\frac{2\pi}{\Delta t}
\right)^2
-k_z^2
\right]^{1/2}.
$$

这给本章一个很重要的写作边界：`warpx.use_filter = 1` 不是随意的数值润色，而是针对高 $k$ alias 和短波共振的 filter/smoothing 家族；但 filter 也不是万能的，因为小 $k$ 非共振增长可能需要 current scaling、插值阶数、时间步或表示方式共同处理。Godfrey 论文中的 current scaling 写成

$$
\mathbf{J}=\boldsymbol{\zeta}:\mathbf{J}_e,\qquad
\boldsymbol{\zeta}=\mathrm{diag}(\zeta_z,\zeta_x,\zeta_y),
$$

它是 NCI 色散矩阵中的 k 依赖电流因子。这里必须和 WarpX regression 里的 `psatd.current_correction` 分开：`psatd.current_correction` 首先是连续性方程/Gauss law 约束路径，`analysis_galilean.py` 在 current-correction 分支还会检查 `max|divE-rho/eps0|` 相对误差；Godfrey 的 $\zeta$ 则是为压低 NCI 增长率而设计的 current scaling。

Godfrey 2014、Lehe 2016、Kirchen 2016 合起来形成一个清楚的策略谱系。Godfrey 论文讲 fixed-grid PSATD 中如何用数字滤波、三次插值、current scaling 和时间步选择降低 NCI；Lehe 论文讲 Galilean PSATD 如何通过移动坐标/源项表示，在 $v_{gal}\approx v_0$ 时从表示层面消除均匀漂移 NCI；Kirchen 论文讲这个 Galilean 表示如何落到 boosted-frame LPA workflow 并保持回变换后的物理量一致。对应到 WarpX，`nci_psatd_stability` 的 `warpx.use_filter = 1`、`psatd.current_correction`、`psatd.do_time_averaging` 和 `psatd.JRhom` 应被写成不同机制的 regression 入口，而不是同一个“稳定化开关”的不同名字。

本版新增 `scripts/audit_psatd_literature_strategy_contract.py`，把上述三篇已有全文资产、章节映射、源码关键词和 runtime consumer 统一检查为 `runs/stage-c-validation/psatd-literature-strategy/contract.{json,md}`。三篇均通过；该矩阵只说明 Godfrey 的 fixed-grid NCI 基线、Lehe 的 Galilean 表示和 Kirchen 的 boosted-frame 应用各自负责什么，不把三篇论文或其 regression 结果合并成同一个“PSATD 已验证”结论。详细表格见 `notes/code-reading/fieldsolver/35-psatd-literature-source-runtime-strategy-matrix.md`。

### 6.6.6 v0.20 源码闭环：WarpX PSATD/NCI 机制对照表

v0.20 继续把上一节的策略谱系落回 WarpX 源码。结论先写清楚：当前 WarpX 中和 NCI 稳定性相关的 filter、current correction、finite-order PSATD、Galilean representation 和 JRhom 是五组不同机制；其中源码里叫 `NCIGodfreyFilter` 的路径也不是 `nci_psatd_stability` 输入卡里常见的 `warpx.use_filter = 1`。

| 机制 | 触发入口 | 当前源码证据 | 实际操作 | 和 Godfrey 2014 的关系 |
|---|---|---|---|---|
| 实空间 bilinear/binomial-like filter | 普通 Cartesian explicit/PSATD 路径中 `warpx.use_filter = 1`，默认值由 `WarpX.cpp` 根据 `evolve_scheme` 和几何决定 | `Source/WarpX.cpp:825-842` 读取 `warpx.use_filter`、`warpx.use_filter_compensation`、`warpx.filter_npass_each_dir`；`Source/Initialization/WarpXInitData.cpp:1203-1208` 初始化 `bilinear_filter`；`Source/Filter/BilinearFilter.cpp:24-87` 构造逐方向 stencil；`Source/Filter/Filter.cpp:38-130` 应用 tensor-product stencil；`Source/Parallelization/WarpXComm.cpp:1479-1496` 和 `1677-1693` 对 current/rho 做 filter 与边界求和 | 多次卷积中心权重 `0.5`、相邻权重 `0.25` 的对称 1D stencil，再按方向组合成多维 filter；`filter_npass_each_dir` 决定 stencil 宽度 | 属于 Godfrey 论文中的 digital filtering/smoothing 家族，可以压制高 $k$ alias，但不是论文中的 current scaling 因子 $\zeta$ |
| RZ PSATD k-space binomial filter | RZ/RCYLINDER/RSPHERE 几何且 PSATD 时，`WarpX.cpp` 把 `use_filter` 转成 `use_kspace_filter` | `Source/WarpX.cpp:853-858` 在 RZ PSATD 下设置 `use_kspace_filter = use_filter` 并关闭实空间 `use_filter`；`Source/WarpX.cpp:3123-3125` 调用 `SpectralSolver::InitFilter()`；`Source/FieldSolver/SpectralSolver/SpectralBinomialFilter.cpp:18-38` 构造 k-space filter；`Source/FieldSolver/SpectralSolver/SpectralFieldDataRZ.cpp:800-848` 初始化并应用 radial/z filter；`Source/FieldSolver/WarpXPushFieldsEM.cpp:514-538` 与 `612-625` 在 spectral J/rho 上应用 | 对每个方向使用 $1-\sin^2(k\Delta/2)$ 的幂次 filter，补偿打开时再乘一个低阶补偿因子 | 仍是 spectral filtering 家族；和 Cartesian 实空间 bilinear filter 入口相同，但实现位置、作用空间和 RZ 语义不同 |
| FDTD Godfrey gather filter | `use_fdtd_nci_corr`，不是 `warpx.use_filter` | `Source/Initialization/WarpXInitData.cpp:1170-1198` 初始化两组 `NCIGodfreyFilter`；`Source/Filter/NCIGodfreyFilter.cpp:29-138` 固定 z 向 5 点 stencil 并按 gather 类型查表插值；`Source/Particles/PhysicalParticleContainer.cpp:552-563` 与 `896-970` 在粒子 gather 前过滤场；`Source/Parallelization/GuardCellManager.cpp:355-365` 为 gather 增加 z 向 guard cells | 对 field gather 使用 Godfrey 表系数构造的 z 向 5 点 filter，分别作用于 `Ex/Ey/Bz` 和 `Bx/By/Ez` 组合 | 这是 FDTD NCI corrector 的 gather-side filter；不能把它误读成 PSATD `nci_psatd_stability` 中 `warpx.use_filter = 1` 的 filter profile |

这张表给本章一个新的写作规则：以后看到 `filter` 必须先问它是实空间 source filter、RZ spectral filter，还是 FDTD gather-side Godfrey filter。三者都能和 NCI 稳定性有关，但它们不共享同一条源码路径，也不该在书中被统一写成“打开 Godfrey filter”。

`psatd.current_correction` 的边界也需要更精确。WarpX 在 `Source/WarpX.cpp:1653-1682` 根据 current deposition、divE cleaning 和用户输入决定默认值，并在 `Source/FieldSolver/WarpXPushFieldsEM.cpp:791-805`、`840-866` 把 J、rho 变换到 spectral 空间后调用 `PSATDCurrentCorrection()`。在标准连续性投影分支，核心形式可以写成

$$
\mathbf{J}_{corr}
=
\mathbf{J}
-
\frac{
\mathbf{k}\cdot\mathbf{J}
- i(\rho^{n+1}-\rho^n)/\Delta t
}{
\mathbf{k}\cdot\mathbf{k}
}
\mathbf{k}.
$$

`Source/FieldSolver/SpectralSolver/SpectralAlgorithms/PsatdAlgorithmJRhomSecondOrder.cpp:544-610` 中的 JRhom second-order current correction 就是这个投影式结构，并且源码断言它只在 `J` 常数、`rho` 线性时间依赖的组合下实现。Galilean 与 comoving 分支仍是连续性投影，只是连续性方程本身包含移动坐标相位。`Source/FieldSolver/SpectralSolver/SpectralAlgorithms/PsatdAlgorithmGalilean.cpp:634-731` 中，当 $\mathbf{k}_c\cdot\mathbf{v}_{gal}\ne0$ 时，源码先构造

$$
\rho^n_{gal}=\rho^n \exp(i\,\mathbf{k}_c\cdot\mathbf{v}_{gal}\Delta t),
$$

再用

$$
\mathbf{k}\cdot\mathbf{J}
-
\frac{\mathbf{k}_c\cdot\mathbf{v}_{gal}\,(\rho^{n+1}-\rho^n_{gal})}
{1-\exp(i\,\mathbf{k}_c\cdot\mathbf{v}_{gal}\Delta t)}
$$

替换标准分支里的连续性残差。`Source/FieldSolver/SpectralSolver/SpectralAlgorithms/PsatdAlgorithmComoving.cpp:418-503` 也沿用相同思想，只是速度来自 comoving formulation。由此可见，`psatd.current_correction` 是让 spectral current 满足离散连续性/Gauss-law 约束的 projection，不是 Godfrey 2014 中为降低 NCI 增长率引入的 $\zeta(k)$ current scaling。

finite-order PSATD 是另一条独立轴线。`Source/WarpX.cpp:1557-1590` 读取 `psatd.nox/noy/noz`，字符串 `"inf"` 会转成 `-1`，但源码随后断言：如果不是 `psatd.periodic_single_box_fft = 1`，每个方向的 FFT order 必须是正整数。因此普通 multi-box PSATD 不能写成“无限阶全局谱求解器”。`Source/WarpX.cpp:3164-3182` 把 `nox_fft/noy_fft/noz_fft`、`periodic_single_box`、`update_with_rho`、`fft_do_time_averaging`、solution type 和 J/rho time dependency 传给 `SpectralSolver`；`Source/FieldSolver/SpectralSolver/SpectralSolver.cpp:60-107` 再按 PML、comoving、Galilean、first-order JRhom、second-order standard/JRhom 的优先级选择具体 algorithm。

这也解释了 `Examples/Tests/nci_psatd_stability` 的输入卡为什么不能只按 “PSATD” 一个词归类。`inputs_base_2d` 打开 `warpx.use_filter = 1`，并设置 `psatd.nox/noy/noz = 16`；`inputs_base_3d` 同样打开 `warpx.use_filter = 1`，但有限阶为 `8`。这些 regression 不是无限阶 periodic single-box PSATD 的泛化代表，而是有限阶 PSATD、filter、Galilean/current-correction/JRhom 分支的组合测试。

| regression / analysis | 代表输入 | 脚本判据 | 本章应如何表述 |
|---|---|---|---|
| `analysis_galilean.py` 普通 Galilean / averaged Galilean | `inputs_test_2d_galilean_psatd*`、`inputs_test_3d_galilean_psatd*`、`inputs_test_rz_galilean_psatd*` | 读取最终 plotfile 的 `Ex/Ey/Ez`，用电场能量除以脚本中的不稳定参考能量，并要求低于维度/分支容差 | 这是 NCI 抑制的强 regression gate，但主判据是能量比，不是色散关系重建 |
| `analysis_galilean.py` current-correction 分支 | `inputs_test_2d_galilean_psatd_current_correction`、`inputs_test_3d_galilean_psatd_current_correction_psb` 等 | 除电场能量比外，还读取 `divE` 和 `rho`，检查 `max|divE-rho/eps0|` 的相对误差 | 这条 gate 同时覆盖稳定性和 Gauss-law/continuity projection；它不能证明 Godfrey $\zeta(k)$ current scaling 已实现 |
| RZ Galilean current-correction paired runtime | `test_rz_galilean_psatd_current_correction`、`test_rz_galilean_psatd_current_correction_psb` | 非 PSB 2-rank energy `7.536e-11` 通过但 charge `3.1805e-4 > 3e-4`；PSB single-box single-rank energy `8.163e-11`、charge `2.642e-11 < 1e-9` 均通过 | 当前项目级证据分层为 `CHARGE_BOUNDARY` 与 `PASS`；PSB 的严格 charge gate 不能外推到非 PSB 多 rank |
| `analysis_psatd_CC1.py` | `inputs_test_3d_uniform_plasma_psatd_JRhom_CC1` | 电场能量除以 `66e6` 后要求 `< 1e-8` | 这是 JRhom CC1 的 NCI 能量 gate，没有额外 charge-conservation assert |
| checksum-only RZ JRhom | `test_rz_psatd_JRhom_LL2` | CMake 中 `analysis=OFF`，只走 checksum | 只能写成 workflow/output regression，不能写成强 NCI 物理论证 |
| project-level RZ JRhom first-stage helper | 同一 `test_rz_psatd_JRhom_LL2` 的 2-rank repeated/MPI ledger | `scripts/analyze_rz_jrhom_first_stage_contract.py`：baseline `finite + energy` 通过，`ll2-no-timeavg-cleaning` reference 被拒绝 | 这是可审阅的 local validation/handoff evidence；尚未改变上游 CMake 的 `analysis=OFF` |

本版还把这条 local validation 收成可重复的交接链：`scripts/build_rz_jrhom_first_stage_patch.py` 从 `rz-jrhom-reference-scan-mpi2.json` 重建 helper、unified diff、provenance、submission packet、PR draft 和 bundle；随后 `audit`、`report`、`preview` 与 `stage --dry-run` 对只读目标 checkout 进行一致性检查。当前实际状态仍是 `unstaged`：`analysis_rz_jrhom.py` 尚未写入 `../warpx`，`test_rz_psatd_JRhom_LL2` 的 CMake 行仍为 `analysis=OFF`。因此这里交付的是可审阅、可复现的 handoff asset，不是已经进入 WarpX upstream CI 的 patch。对 bundle helper 的直接复核中，MPI=2 baseline 返回通过，`ll2-no-timeavg-cleaning` 返回拒绝；两者与独立 first-stage contract 的 `baseline_ratio=0.9770894022295227`、`reference_ratio=1.0` 一致。

把这些源码和 regression 合起来，v0.20 对 Godfrey 2014 策略谱系的落点是：

1. filtering/smoothing 在 WarpX 中至少有实空间 bilinear filter 和 RZ spectral binomial filter 两条实现；
2. 源码名为 `NCIGodfreyFilter` 的路径属于 FDTD gather-side NCI corrector，不能直接外推到 PSATD filter；
3. `psatd.current_correction` 是连续性投影，不是 Godfrey $\zeta(k)$ current scaling；
4. finite-order PSATD 由 `psatd.nox/noy/noz` 和 `periodic_single_box_fft` 共同限定，NCI tests 中常见的是有限阶分支；
5. Galilean PSATD 是表示层面的移动坐标策略，JRhom 是源项时间积分策略，二者和 filter/current correction 可以组合出不同 regression 入口，但不能合并成同一个物理机制。

### 6.6.7 v0.74 文献闭环：Vay--Godfrey 2014 review

Vay--Godfrey 2014 review 为本节的 PSATD 讨论补上统一的文献主干。论文式（15--28）从 Fourier 空间的 Maxwell 方程出发，把场分解为纵向与横向分量，并用

$$
C=\cos(c|\mathbf{k}|\Delta t),\qquad
S=\frac{\sin(c|\mathbf{k}|\Delta t)}{c|\mathbf{k}|}
$$

写出解析时间推进；当时间步足够小时，PSTD 可以看作该解析推进的极限或近似。这个推导解释了为什么 `PsatdAlgorithm` 同时需要波数、`C/S` 系数、源项时间依赖和 current correction，而不是只做一次 FFT 后的代数更新。

同一 review 的数值稳定性部分还给出 NCI 色散关系（式 39）的结构：漂移速度、网格 alias、场 gather 插值和电流沉积共同进入增长率；纵向 alias 可写为 `$k'_z = k_z + m_z 2\pi/\Delta z$`。因此 filter、插值阶数、current scaling、时间步和 Galilean/boosted-frame 表示属于不同的抑制轴线，不能用“PSATD 已稳定”一句话替代机制分析。

本书已将全文资产、43 张图和中文精读固定在上述 review 的专属目录，并通过 asset contract。映射到当前 WarpX 时继续保持三条边界：`psatd.current_correction` 是离散连续性/Gauss-law projection，不等于论文中为降低 NCI 增长率设计的 `$\zeta(k)$` current scaling；`warpx.use_filter`、RZ spectral filter 和 `NCIGodfreyFilter` 分别属于不同的 filter/gather 实现；论文中的历史 Warp/其他 PIC 结果也不自动成为当前 WarpX runtime 结果。第 6 章因此获得的是公式和机制层闭环，不是函数级等价或完整 NCI benchmark 证明。

## 6.7 JRhom 记录

### 6.7.1 v0.28 JRhom second-order Y1-Y8 系数的源码公式闭环

v0.28 把 `notes/code-reading/fieldsolver/19-psatd-jrhom-y-coefficients.md` 补成独立图谱。这个图谱的第一条规则是防混写：`PsatdAlgorithmJRhomSecondOrder.cpp` 的 `Y1-Y8` 是实系数，属于 JRhom 多项式源项积分；它们不是上一节 Cartesian Galilean/standard PSATD average-field 分支里的 complex `Y1-Y4`。

源码分配边界在 `PsatdAlgorithmJRhomSecondOrder.cpp:59-77`。`Y1-Y5` 总是分配，`Y6-Y8` 只在 `time_averaging` 打开时分配：

```cpp
Y1_coef = SpectralRealCoefficients(ba, dm, 1, 0);
Y2_coef = SpectralRealCoefficients(ba, dm, 1, 0);
Y3_coef = SpectralRealCoefficients(ba, dm, 1, 0);
Y4_coef = SpectralRealCoefficients(ba, dm, 1, 0);
Y5_coef = SpectralRealCoefficients(ba, dm, 1, 0);

if (time_averaging)
{
    Y6_coef = SpectralRealCoefficients(ba, dm, 1, 0);
    Y7_coef = SpectralRealCoefficients(ba, dm, 1, 0);
    Y8_coef = SpectralRealCoefficients(ba, dm, 1, 0);
}
```

第二条规则是时间步边界。`SpectralSolver.cpp` 在 JRhom 打开时把 `solver_dt` 除以 `m_JRhom_subintervals`，所以 `PsatdAlgorithmJRhomSecondOrder` 里看到的 $\Delta t$ 是每个 JRhom 子区间长度，而不是外层 PIC 大步长。

二阶类先把 `old/mid/new` 源项写成局部多项式：

$$
\mathbf{J}(\tau)=\mathbf{a}_J\tau^2+\mathbf{b}_J\tau+\mathbf{c}_J,
\qquad
\rho(\tau)=a_\rho\tau^2+b_\rho\tau+c_\rho.
$$

源码对应为：

```cpp
const Complex a_jx = (J_quadratic) ? (Jx_new - 2._rt * Jx_mid + Jx_old) : 0._rt;
const Complex b_jx = (J_linear || J_quadratic) ? (Jx_new - Jx_old) : 0._rt;
const Complex c_jx = (J_linear) ? (Jx_new + Jx_old)/2._rt : Jx_mid;

const Complex a_rho = (rho_quadratic) ? (rho_new - 2._rt * rho_mid + rho_old) : 0._rt;
const Complex b_rho = (rho_linear || rho_quadratic) ? (rho_new - rho_old) : 0._rt;
const Complex c_rho = (rho_linear) ? (rho_new + rho_old)/2._rt : rho_mid;
```

共享谱量仍是

$$
\omega_s=c|\mathbf{k}_s|,\qquad
C=\cos(\omega_s\Delta t),\qquad
S_{ck}=\frac{\sin(\omega_s\Delta t)}{\omega_s},
$$

并在 $\omega_s=0$ 时取 `S_ck = dt`。`Y1-Y5` 的非零模公式为：

$$
Y_1=
\frac{
(1-C)(8-\omega_s^2\Delta t^2)-4S_{ck}\omega_s^2\Delta t
}{
2\epsilon_0\Delta t^2\omega_s^4
},
$$

$$
Y_2=
\frac{
2(C-1)+S_{ck}\omega_s^2\Delta t
}{
2\epsilon_0\Delta t\,\omega_s^2
},
\qquad
Y_3=
\frac{
S_{ck}\omega_s(8-\omega_s^2\Delta t^2)-4(1+C)\omega_s\Delta t
}{
2\epsilon_0\Delta t^2\omega_s^3
},
$$

$$
Y_4=\frac{1-C}{\epsilon_0\omega_s^2},
\qquad
Y_5=
\frac{(1+C)\Delta t-2S_{ck}}
{2\epsilon_0\Delta t\,\omega_s^2}.
$$

零模分支分别是：

$$
Y_1=-\frac{\Delta t^2}{12\epsilon_0},\quad
Y_2=0,\quad
Y_3=-\frac{\Delta t}{6\epsilon_0},\quad
Y_4=\frac{\Delta t^2}{2\epsilon_0},\quad
Y_5=-\frac{\Delta t^2}{12\epsilon_0}.
$$

这些系数在 ordinary field push 里分工如下。`Y3/Y2/S_ck` 分别积分二次、一次、常量电流对电场的贡献：

```cpp
fields(i,j,k,Idx.Ex) = C * Ex_old
    + I * c2 * S_ck * (ky * Bz_old - kz * By_old)
    + Y3 * a_jx + Y2 * b_jx - S_ck/ep0 * c_jx
    + I * c2 * kx * sum_rho;
```

`Y1/Y5/Y4` 则进入磁场中的 `k x J` 多项式积分：

```cpp
fields(i,j,k,Idx.Bx) = C * Bx_old
    - I * S_ck * (ky * Ez_old - kz * Ey_old)
    - I * Y1 * (ky * a_jz - kz * a_jy)
    + I * Y5 * (ky * b_jz - kz * b_jy)
    + I * Y4 * (ky * c_jz - kz * c_jy );
```

同一组 `Y1/Y5/Y4` 还出现在电荷纵向组合里：

```cpp
const Complex sum_rho = Y1 * a_rho - Y5 * b_rho - Y4 * c_rho;
```

如果打开 `dive_cleaning`，`F` 也复用这组源项积分：

```cpp
fields(i,j,k,Idx.F) = C * F_old + S_ck * I * k_dot_E
    + I * ( Y1 * k_dot_ddJ - Y5 * k_dot_dJ - Y4 * k_dot_J_mid )
    +  Y3 * a_rho + Y2 * b_rho - S_ck/ep0 * c_rho;
```

`Y6-Y8` 只属于 time-averaged field 累计。非零模公式为：

$$
Y_6=
\frac{
\Delta t^3\omega_s^3
-3\Delta t^2\omega_s^3S_{ck}
-12\Delta t\omega_s(1+C)
+24\omega_sS_{ck}
}{
6\epsilon_0\Delta t^2\omega_s^5
},
$$

$$
Y_7=
\frac{
\Delta t\omega_s^2S_{ck}+2C-2
}{
2\epsilon_0\Delta t\omega_s^4
},
\qquad
Y_8=
\frac{\Delta t-S_{ck}}{\epsilon_0\omega_s^2}.
$$

零模分支为：

$$
Y_6=\frac{\Delta t^3}{30\epsilon_0},\quad
Y_7=-\frac{\Delta t^3}{24\epsilon_0},\quad
Y_8=\frac{\Delta t^3}{6\epsilon_0}.
$$

源码注释明确说 average-field 是累加形式，因为 JRhom 可配合 sub-cycling：

```cpp
fields(i,j,k,Idx.Ex_avg) += S_ck * Ex_old
    + I * c2 * ep0 * Y4 * (ky * Bz_old - kz * By_old)
    - I * c2 * kx * (Y6 * a_rho + Y7 * b_rho + Y8 * c_rho)
    + ( Y1 * a_jx - Y5 * b_jx - Y4 * c_jx);
```

因此 v0.28 对第 6 章的写作边界是：`Y1-Y5` 是 JRhom ordinary field push 的源项积分，`Y6-Y8` 是 JRhom time averaging 的累计积分；二者都不应和 Cartesian Galilean average-field 的 `Y1-Y4` 合并。后续如果继续拆 RZ/Galilean RZ，也要按 algorithm class 和 field layout 单独建表。

## 6.8 RZ、comoving 与算法选择记录

### 6.8.1 v0.29 RZ/Galilean RZ PSATD 系数边界

v0.29 把 `notes/code-reading/fieldsolver/20-psatd-rz-galilean-rz-coefficients.md` 补成 RZ 系数边界图谱。第一条结论先写清楚：RZ 标准 PSATD 的 `X1-X3/X5-X6` 和 Galilean RZ 的 `X1-X4/Theta2/T_rho` 不能和 Cartesian 同名系数直接合并，因为 RZ 的谱基、横向字段和 current correction 都不同。

`PsatdAlgorithmRZ.cpp:43-55` 总是分配实系数 `C/S_ck/X1-X3`，只有 linear-J time averaging 才分配 `X5/X6`。standard RZ 的非零模公式为：

$$
C=\cos(ck\Delta t),\qquad
S_{ck}=\frac{\sin(ck\Delta t)}{ck},
$$

$$
X_1=\frac{1-C}{\epsilon_0c^2k^2},
\qquad
X_2=\frac{1-S_{ck}/\Delta t}{\epsilon_0k^2},
\qquad
X_3=\frac{C-S_{ck}/\Delta t}{\epsilon_0k^2},
$$

其中 $k=\sqrt{k_r^2+k_z^2}$。零模分支为：

$$
C=1,\quad
S_{ck}=\Delta t,\quad
X_1=\frac{\Delta t^2}{2\epsilon_0},\quad
X_2=\frac{c^2\Delta t^2}{6\epsilon_0},\quad
X_3=-\frac{c^2\Delta t^2}{3\epsilon_0}.
$$

这些系数进入 `Ep/Em/Ez` 更新时，径向符号并不是 Cartesian 向量式的简单投影：

```cpp
fields(i,j,k,Ep_m) = C*Ep_old
            + S_ck*(-c2*I*kr/2._rt*Bz_old + c2*kz*Bp_old - inv_ep0*Jp)
            + 0.5_rt*kr*rho_diff;
fields(i,j,k,Em_m) = C*Em_old
            + S_ck*(-c2*I*kr/2._rt*Bz_old - c2*kz*Bm_old - inv_ep0*Jm)
            - 0.5_rt*kr*rho_diff;
```

standard RZ 的 time averaging 支持边界很窄：只允许 `psatd.time_dependency_J=linear`。若 time averaging 配合非线性 `J`，源码直接 abort。linear-J 分支中，`X5/X6` 的非零模公式为：

$$
X_5=\frac{c^2}{\epsilon_0}
\left[
\frac{S_{ck}}{\omega^2}
-\frac{1-C}{\omega^4\Delta t}
-\frac{\Delta t}{2\omega^2}
\right],
\qquad
X_6=\frac{c^2}{\epsilon_0}
\left[
\frac{1-C}{\omega^4\Delta t}
-\frac{\Delta t}{2\omega^2}
\right],
$$

其中 $\omega=ck$。零模分支为

$$
X_5=-\frac{c^2\Delta t^3}{8\epsilon_0},
\qquad
X_6=-\frac{c^2\Delta t^3}{24\epsilon_0}.
$$

`X5/X6` 在 average-field 更新中分别乘 old/new `rho` 和 old/new `J`：

```cpp
fields(i,j,k,Ep_avg_m) += S_ck * Ep_old
    + c2 * ep0 * X1 * (kz * Bp_old - I * kr * 0.5_rt * Bz_old)
    - kr * 0.5_rt * (X5 * rho_old + X6 * rho_new) + X3/c2 * Jp - X2/c2 * Jp_new;
```

Galilean RZ 又是另一套边界。`PsatdAlgorithmGalileanRZ.cpp` 只使用 `m_v_galilean[2]`，也就是轴向速度：

```cpp
const amrex::Real vz = m_v_galilean[2];
amrex::Real const kv = kz*vz;
```

它分配 `C/S_ck` 两个实系数，以及 complex `X1-X4/Theta2/T_rho`。令

$$
k_v=k_zv_z,\qquad
\nu=\frac{k_v}{ck},\qquad
\theta=e^{ik_v\Delta t/2},
$$

则源码中

$$
\Theta_2=\theta^2,\qquad
T_\rho=
\begin{cases}
-\Delta t, & k_z=0,\\
\dfrac{1-\theta^2}{ik_zv_z}, & k_z\ne0.
\end{cases}
$$

一般分支 `nu != 1 && nu != 0` 先构造

$$
x_1=\frac{\theta^\ast-C\theta+ik_vS_{ck}\theta}{1-\nu^2},
$$

再定义

$$
X_1=\frac{\theta x_1}{\epsilon_0c^2k^2},
\qquad
X_2=\frac{x_1-\theta(1-C)}{(\theta^\ast-\theta)\epsilon_0k^2},
\qquad
X_3=\frac{x_1-\theta^\ast(1-C)}{(\theta^\ast-\theta)\epsilon_0k^2},
$$

$$
X_4=ik_vX_1-\frac{\theta^2S_{ck}}{\epsilon_0}.
$$

当 `nu == 0`，Galilean RZ 回到 standard RZ 的 `X1-X3`，并取 `X4=-S_ck/epsilon0`。当 `nu == 1`，源码有专门极限分支，避免 $1-\nu^2$ 和 $\theta^\ast-\theta$ 分母退化。零模分支则取 `Theta2=1`、`X4=-dt/epsilon0`。

Galilean RZ 的更新式与 standard RZ 使用相同 `Ep/Em` layout，但旧场和 curl 项乘 `T2=Theta2`，电流直接项用 `X4`：

```cpp
fields(i,j,k,Ep_m) = T2*C*Ep_old
            + T2*S_ck*(-c2*I*kr/2._rt*Bz_old + c2*kz*Bp_old)
            + X4*Jp + 0.5_rt*kr*rho_diff;
```

电荷项中旧时刻 `rho` 也带 Galilean 相位：

```cpp
if (update_with_rho) {
    rho_diff = X2*rho_new - T2*X3*rho_old;
} else {
    rho_diff = T2*(X2 - X3)*myeps0*divE + T_rho*X2*divJ;
}
```

RZ current correction 沿 `Ep/Em/Jp/Jm` 的谱梯度方向修正，而不是 Cartesian 的 `Jx/Jy/Jz` 投影。standard RZ 使用

```cpp
Complex const F = - ((rho_new - rho_old)/dt + I*kz*Jz + kr*(Jp - Jm))/k_norm2;
fields(i,j,k,Jp_m) += +0.5_rt*kr*F;
fields(i,j,k,Jm_m) += -0.5_rt*kr*F;
fields(i,j,k,Jz_m) += -I*kz*F;
```

Galilean RZ 则把 `rho_old` 乘 `theta2`，并用 Galilean 连续性残差替换普通时间差分。两条 RZ 路径都显式不支持 Vay deposition。

所以 v0.29 对第 6 章的边界补充是：RZ 标准 PSATD、RZ time averaging、Galilean RZ 和 Cartesian/Galilean/JRhom/PML 都应各自成表。它们可以共享 `C/S_ck` 这类基础三角函数，但不能共享同一组更新式语义。

### 6.8.2 v0.30 comoving PSATD 系数与验证边界

v0.30 把 `notes/code-reading/fieldsolver/21-psatd-comoving-coefficients.md` 补成 regular-domain comoving PSATD 的系数图谱。这个分支在源码中不是 Galilean PSATD 的小选项，而是 `SpectralSolver.cpp` 里优先级最高的 regular-domain algorithm：

```cpp
if (v_comoving[0] != 0. || v_comoving[1] != 0. || v_comoving[2] != 0.)
{
    algorithm = std::make_unique<PsatdAlgorithmComoving>(...);
}
else if (v_galilean[0] != 0. || v_galilean[1] != 0. || v_galilean[2] != 0.)
{
    algorithm = std::make_unique<PsatdAlgorithmGalilean>(...);
}
```

`WarpX.cpp` 解析参数时进一步保证 `v_comoving` 与 `v_galilean` 互斥。`psatd.use_default_v_comoving=1` 只能在 `warpx.gamma_boost` 已设置时使用，并只自动填 `z` 向 normalized velocity：

```cpp
m_v_comoving[2] = -std::sqrt(1._rt - 1._rt / (gamma_boost * gamma_boost));
```

随后源码把 `m_v_comoving` 乘以 `PhysConst::c`。因此正文要区分输入卡中的“光速单位速度”和 algorithm 内部的 SI 速度。comoving 还要求 direct current deposition，强制 `psatd.update_with_rho=1`，并且不支持 Esirkepov/Villasenor、Vay deposition 或非默认 `J constant / rho linear` 时间依赖。

`PsatdAlgorithmComoving` 分配 `C/S_ck` 两个实系数，以及 complex `X1-X4/Theta2`：

```cpp
C_coef    = SpectralRealCoefficients(ba, dm, 1, 0);
S_ck_coef = SpectralRealCoefficients(ba, dm, 1, 0);
X1_coef     = SpectralComplexCoefficients(ba, dm, 1, 0);
X2_coef     = SpectralComplexCoefficients(ba, dm, 1, 0);
X3_coef     = SpectralComplexCoefficients(ba, dm, 1, 0);
X4_coef     = SpectralComplexCoefficients(ba, dm, 1, 0);
Theta2_coef = SpectralComplexCoefficients(ba, dm, 1, 0);
```

这里最容易漏掉的是两套波数的分工：`C/S_ck` 使用 finite-order modified wave number，

$$
\omega_\mathrm{mod}=c|\mathbf k_\mathrm{mod}|,\qquad
C=\cos(\omega_\mathrm{mod}\Delta t),\qquad
S_{ck}=\frac{\sin(\omega_\mathrm{mod}\Delta t)}{\omega_\mathrm{mod}},
$$

而 comoving 相位使用 infinite-order $\mathbf k$ 与 comoving velocity：

$$
k_v=\mathbf k\cdot\mathbf v_c,\qquad
\omega=c|\mathbf k|,\qquad
\nu=-\frac{k_v}{\omega},
$$

$$
\theta=e^{i\nu\omega\Delta t/2},\qquad
\Theta_2=\theta^2.
$$

一般非退化分支满足 `nu != om_mod/om`、`nu != -om_mod/om` 且 `nu != 0`。源码先构造

$$
x_1=\frac{\omega^2}{\omega_\mathrm{mod}^2-\nu^2\omega^2}
\left(\theta^\ast-\theta C+i\nu\omega\theta S_{ck}\right),
$$

再定义

$$
X_1=\frac{x_1}{\epsilon_0\omega^2},
$$

$$
X_2=\frac{c^2\left(x_1\omega_\mathrm{mod}^2-\theta(1-C)\omega^2\right)}
{(\theta^\ast-\theta)\epsilon_0\omega^2\omega_\mathrm{mod}^2},
$$

$$
X_3=\frac{c^2\left(x_1\omega_\mathrm{mod}^2-\theta^\ast(1-C)\omega^2\right)}
{(\theta^\ast-\theta)\epsilon_0\omega^2\omega_\mathrm{mod}^2},
$$

$$
X_4=i\nu\omega X_1-\frac{\theta S_{ck}}{\epsilon_0}.
$$

ordinary field push 仍使用 Cartesian `Ex/Ey/Ez/Bx/By/Bz` layout。电场中 `X4` 乘电流，`X2/X3` 分别乘 new/old charge density：

```cpp
fields(i,j,k,Idx.Ex) = C*Ex_old + S_ck*c2*I*(ky_mod*Bz_old - kz_mod*By_old)
    + X4*Jx - I*(X2*rho_new - X3*rho_old)*kx_mod;
```

磁场中 `X1` 乘 current curl：

```cpp
fields(i,j,k,Idx.Bx) = C*Bx_old - S_ck*I*(ky_mod*Ez_old - kz_mod*Ey_old)
    + X1*I*(ky_mod*Jz - kz_mod*Jy);
```

当 `nu == 0` 时，comoving `X1-X4` 退到 standard PSATD 形式：

$$
X_1=\frac{1-C}{\epsilon_0\omega_\mathrm{mod}^2},\quad
X_2=\frac{c^2(1-S_{ck}/\Delta t)}{\epsilon_0\omega_\mathrm{mod}^2},\quad
X_3=\frac{c^2(C-S_{ck}/\Delta t)}{\epsilon_0\omega_\mathrm{mod}^2},\quad
X_4=-\frac{S_{ck}}{\epsilon_0}.
$$

当 `nu == om_mod/om` 或 `nu == -om_mod/om`，源码用 `tmp1/tmp2` 与半步相位写出专门极限，避免 $\omega_\mathrm{mod}^2-\nu^2\omega^2$ 分母退化。`knorm_mod` 与 `knorm` 任一为零时也有单独分支；完全零模时：

$$
C=1,\quad S_{ck}=\Delta t,\quad \Theta_2=1,\quad
X_1=\frac{\Delta t^2}{2\epsilon_0},\quad
X_2=\frac{c^2\Delta t^2}{6\epsilon_0},\quad
X_3=-\frac{c^2\Delta t^2}{3\epsilon_0},\quad
X_4=-\frac{\Delta t}{\epsilon_0}.
$$

comoving current correction 也有自己的 continuity 残差。若 $\mathbf k\cdot\mathbf v_c\ne0$，源码使用

```cpp
const Complex theta = amrex::exp(- I * k_dot_v * dt * 0.5_rt);
const Complex den = 1._rt - theta * theta;
fields(i,j,k,Idx.Jx_mid) = Jx
    - (kmod_dot_J + k_dot_v * theta * (rho_new - rho_old) / den)
    * kx_mod / (knorm_mod * knorm_mod);
```

若 $\mathbf k\cdot\mathbf v_c=0$，则退回普通 continuity correction：

```cpp
fields(i,j,k,Idx.Jx_mid) = Jx
    - (kmod_dot_J - I * (rho_new - rho_old) / dt)
    * kx_mod / (knorm_mod * knorm_mod);
```

验证边界同样要写窄。当前 `Examples/Tests/nci_psatd_stability/CMakeLists.txt` 注册了 `test_2d_comoving_psatd_hybrid`，输入卡使用 `algo.current_deposition=direct`、`psatd.use_default_v_comoving=1`、`warpx.gamma_boost=13.`、`warpx.grid_type=hybrid`，但 analysis 字段是 `OFF`，只接了

```cmake
"analysis_default_regression.py --path diags/diag1000400"
```

所以本书目前只能把它称为 comoving boosted-frame hybrid PSATD 的 checksum regression，而不能声称它已经提供和 `analysis_galilean.py` 同等级的 NCI 增长率或稳定性强判据。

v0.30 之后，第 6 章的 PSATD 系数边界已经形成一套明确分层：Cartesian Galilean `X1-X4`、average-field `Psi/Y`、JRhom `Y1-Y8`、RZ/Galilean RZ `X/Theta/T_rho`、comoving `X1-X4/Theta2` 和 PML `C1-C25` 都按 algorithm class 分开；后续工作应从“验证强度”继续推进，而不是继续把同名符号并表。

### 6.8.3 v0.31 comoving PSATD regression analysis 方案

v0.31 把 `notes/code-reading/fieldsolver/22-psatd-comoving-regression-analysis-plan.md` 补成 `test_2d_comoving_psatd_hybrid` 的 analysis 升级方案。当前 CMake 注册是：

```cmake
add_warpx_test(
    test_2d_comoving_psatd_hybrid
    2
    2
    inputs_test_2d_comoving_psatd_hybrid
    OFF
    "analysis_default_regression.py --path diags/diag1000400"
    OFF
)
```

这表示它现在只有 checksum 自动消费者。输入卡本身已经是很明确的 boosted-frame hybrid comoving producer：

```ini
algo.maxwell_solver = psatd
algo.current_deposition = direct
psatd.use_default_v_comoving = 1
psatd.current_correction = 0
warpx.grid_type = hybrid
warpx.gamma_boost = 13.
warpx.do_moving_window = 1
warpx.use_filter = 1
diag1.fields_to_plot = Ex Ey Ez Bx By Bz jx jy jz rho
```

因此 v0.31 的第一条边界是：现有输出能支持 `Ex/Ey/Ez/Bx/By/Bz/jx/jy/jz/rho` 的 analysis，但不能直接支持 `divE-rho/epsilon0` 的 charge-conservation gate，因为 `divE` 没有输出。

可直接落地的第一阶段 analysis 应包括三类检查。第一，finite field sanity：所有输出字段都必须有限，避免 checksum 之外的 NaN/Inf 被掩盖：

```python
for name in ["Ex", "Ey", "Ez", "Bx", "By", "Bz", "jx", "jy", "jz", "rho"]:
    arr = all_data["boxlib", name].squeeze().v
    assert np.all(np.isfinite(arr))
```

第二，沿用 Galilean analysis 的电场能量 proxy：

$$
U_E=\sum \frac{\epsilon_0}{2}(E_x^2+E_y^2+E_z^2).
$$

但 `energy_ref_comoving` 不能借用 `analysis_galilean.py` 中的 Galilean reference；它必须来自 comoving reference run 或 CI baseline 的明确记录。初版脚本可以写成：

```python
energy = np.sum(scc.epsilon_0 / 2 * (Ex**2 + Ey**2 + Ez**2))
err_energy = energy / energy_ref_comoving
assert err_energy < tol_energy
```

第三，增加局部异常 spike sanity：

$$
R_E=\frac{\max |\mathbf E|}{\mathrm{p99}(|\mathbf E|)+\delta}.
$$

这个 ratio 可以发现单点谱异常或边界异常，但仍只是异常探测，不是 NCI 增长率拟合。

如果后续要把这个 regression 推到更强的 Gauss-law 证据，输入卡必须先增加：

```ini
diag1.fields_to_plot = Ex Ey Ez Bx By Bz jx jy jz rho divE
```

然后才能定义

$$
\epsilon_G=
\frac{\|\nabla\cdot\mathbf E-\rho/\epsilon_0\|_\infty}
{\max(\|\nabla\cdot\mathbf E\|_\infty,\|\rho/\epsilon_0\|_\infty,\delta)}.
$$

由于当前 comoving 输入卡设置 `psatd.current_correction=0`，这条 Gauss-law gate 的语义应写成“末态 Gauss-law drift diagnostic”，不能写成“current-correction correctness”。

v0.31 对读者的实际增量是把“checksum-only”拆成一条可执行的升级路线：

| 层级 | 当前状态 | 可支持的说法 |
|---|---|---|
| checksum | 已存在 | 末态 plotfile 与 baseline 一致 |
| finite field sanity | 可直接实现 | 捕捉 NaN/Inf，不是物理强判据 |
| electric energy ceiling | 需要 reference 标定 | 可作为稳定性 proxy，不是增长率拟合 |
| spike ratio | 需要 reference 标定 | 捕捉局部异常，不替代能量判据 |
| Gauss-law drift | 需要输出 `divE` | 验证末态 Gauss-law drift，需和 `current_correction=0` 语义分开 |

所以后续真正提交 WarpX 侧 patch 时，最小完整包应包含 `analysis_comoving.py`、CMake wiring、必要时的 `divE` 输出变更，以及 `energy_ref/tol_energy/spike_ratio_ref` 的 reference 来源说明。

### 6.8.4 comoving PSATD reference 标定与 patch 收口条件

仅把 `analysis_comoving.py` 的脚本骨架写出来，还不够形成可提交的 WarpX regression patch。真正难的部分是 reference 标定：`energy_ref`、`tol_energy` 和 `spike_ratio_ref` 不能随手抄一次本机输出，而要像 `analysis_galilean.py` 那样有清楚的物理语义和 provenance。

这里最值得借用的是 Galilean 那条现成模式。`analysis_galilean.py` 不是把稳定运行和自身比较，而是把稳定配置的末态电场能量和一个已知不稳定对照配置比较；`analysis_psatd_CC1.py` 则展示了另一种更窄的写法：单独给某一条 test 固定一个 `energy_ref`，只保留能量比 gate。comoving 的第一版 patch 更接近第二种形式，但其 reference 语义仍应继承第一种思路，也就是先明确“如果关闭当前 comoving 稳定化关键开关，末态电场能量会膨胀到什么量级”。

这意味着 comoving 不能直接借用 Galilean 分支里现成的 `energy_ref`。当前 `test_2d_comoving_psatd_hybrid` 同时打开了 hybrid grid、moving window、boosted frame、filter 和 laser/plasma/beam 场景，算法路径和 producer surface 都不同；如果把别的 family 的 reference 常量搬过来，就会把“算法不同”和“reference 不同”混成一件事。更稳妥的做法，是先在当前稳定输入上冻结一份 stable ledger，至少记下 `diag1000400` 末态的电场能量、`max(|E|)` 与 `p99(|E|)`；随后再构造一个只关闭 comoving 关键稳定化机制的 sibling 输入，从同一张 `diag1000400` 取出 `energy_ref_unstable`。这样脚本里的能量 gate 才真正有“稳定配置相对不稳定对照被压低了多少”的解释力。

局部 spike gate 则不应和能量 gate 共用同一种 reference 口径。它的用途更像异常探测，而不是 NCI 增长率 proxy，所以应优先绑定 stable envelope：拿当前稳定 baseline 的 `spike_ratio = max(|E|) / p99(|E|)` 作为上界，必要时再乘一个有来源说明的 safety factor。相反，Gauss-law drift 仍属于第二阶段工作。只有当输入卡真的把 `divE` 加入 `fields_to_plot`，并且正文明确区分“current correction 断言”和“`current_correction = 0` 情形下的末态 drift 观测”之后，才适合把它加入 patch。

`v0.32` 的实际推进，是把上面这套标定流程至少跑到一本地 audit 的粒度。当前 `PIC-tutor` 已在只读 `../warpx` 前提下，用 `inputs_test_2d_comoving_psatd_hybrid` 先跑出 stable baseline，再用命令行覆盖 `psatd.use_default_v_comoving=0` 与 `psatd.v_comoving=0` 跑出 sibling，对两张 `diag1000400` 生成 `runs/fieldsolver-validation/comoving-reference-ledgers/comoving-stable-baseline.{md,json}` 与 `comoving-stable-vs-no-comoving.{md,json}`。这一步确认了两件事：第一，override 后的运行日志里不再出现 comoving velocity 行，说明它确实切到了非 comoving 分支；第二，当前单进程样本并没有出现“关闭 comoving 后电场能量显著抬高”的预期，反而得到 `stable_over_unstable_energy_ratio = 1.0469608718245416`，也就是 stable baseline 的电场能量略高于 no-comoving sibling。

这个结果直接决定了 patch 策略边界。当前 local sample 仍然能提供 `spike_ratio_ref_stable = 1.1103719982074416` 这样的 stable envelope 候选值，也能证明 ledger/provenance 工具链是通的；但它还不能让我们诚实地把 `energy_ref_unstable = 7.786411776882875e+14` 宣称为最终 CI gate，因为这个“unstable reference”并没有在本地样本上表现出比 stable baseline 更高的电场能量。

更重要的是，后续本地 control experiment 进一步收紧了这个判断。用同一台机器、同样的 `warpx.numprocs='1 1'` 覆盖方式，对 WarpX 已经具备成熟 energy gate 的 `test_2d_galilean_psatd_hybrid` 再做一组 stable / no-Galilean sibling 对照，当前仓库在 `runs/fieldsolver-validation/galilean-reference-ledgers/galilean-stable-vs-no-galilean.{md,json}` 中得到 `stable_over_unstable_energy_ratio = 0.8418992628444483`：也就是 stable Galilean baseline 的电场能量明显低于禁用 Galilean 的 sibling。这个 control 说明“本机缺 MPI，所以单进程样本看不出 unstable contrast”并不是一个足够强的解释；至少对 Galilean family 而言，单进程本地设置仍然能复现预期的 unstable-energy ordering。

这里还有一个更硬的事实。当前 `no-comoving` 和 `no-galilean` 两个 sibling 的末态 `electric_energy`、`e_mag_max`、`e_mag_p99` 和 `spike_ratio` 在本地 ledger 中已经重合到 `1e-14` 相对误差量级；换句话说，一旦把 `v_comoving` 或 `v_galilean` 都压成零，它们在这组 2D hybrid boosted-frame 运行里就实际汇合到同一条 standard-PSATD branch。于是问题就不再是“comoving 的 unstable sibling 还没找到”，而是“当前可识别的 shared unstable branch 对 Galilean family 提供了有效 energy ordering，却没有对 comoving family 提供同样的 ordering”。

因此，更严格的说法应当是：本地 audit 已经验证了参数分支和 ledger 提取流程，但 comoving `no-comoving` sibling 当前没有给出可用的 unstable-energy contrast，这更像是 comoving family 本身未必适合直接沿用 Galilean 式 energy gate 语义，而不只是并行环境缺失。真正写入 WarpX `analysis_comoving.py` 的实现方向，接下来至少要先回答两个问题之一：要么重新选择更有解释力的 comoving sibling；要么明确承认 comoving 的第一阶段 patch 应该以 finite/spike 或其他更合适的判据为主，把 energy gate 降级为待更多样本后再定。

这条更保守的路线现在已经有了脚本原型，而不再只是文字判断。`PIC-tutor` 当前新增了 `scripts/analysis_comoving.py`：它保持 WarpX regression helper 的读取方式，但把 gate 拆成三层接口，默认始终执行 finite-field sanity，可按 ledger 启用 spike gate，而 energy gate 只有在显式传入参数时才会启用。更关键的是，这个原型已经用现有本地样本做过自校验：stable comoving baseline 能通过 `finite + spike`，而 `no-comoving` sibling 会在同一 `spike_ratio_ref_stable` 阈值下失败。于是第一个真正可执行的第一阶段 patch 形态已经变得具体起来：即便后续继续搁置 energy gate，comoving family 也已经具备一条可落地的 `finite + spike` analysis 路线。

本轮又把这组判别收成了独立的 reader-side contract：`scripts/analyze_comoving_first_stage_contract.py` 同时读取 stable baseline 和 `no-comoving` reference，要求前者通过、后者被同一 spike ceiling 拒绝。实际结果为 stable `spike_ratio=1.1103719982074416`，reference `spike_ratio=1.1119614945212388`，阈值 `1.1114823702056489`；两组输出字段都保持 finite，只有 reference 未通过 spike gate。因此这不是“两个 case 都能跑”的弱 smoke，而是对第一阶段 gate 判别力的最小正/负对照。报告归档于 `runs/fieldsolver-validation/comoving-reference-ledgers/comoving-first-stage-contract.{json,md}`。同时，能量 gate 仍明确关闭：当前本地 calibration 没有形成可解释的 unstable-energy oracle。

为了再往前逼近真正的 WarpX patch 目录结构，当前仓库还把这条路线进一步压成了一个最小 draft helper：`notes/code-reading/fieldsolver/analysis_comoving_first_stage_draft.py`，并配套 `24-psatd-comoving-first-stage-patch-draft.md` 说明其 intended wiring 和候选 `SPIKE_RATIO_MAX` 来源。这份 draft helper 的目标不是替代本地原型，而是回答另一个更实际的问题：如果下一轮真的要往 `Examples/Tests/nci_psatd_stability/` 提 patch，最小、最克制、最不夸大证据边界的第一版文件长什么样。当前答案是：只带 `finite + spike`，不带 energy gate。现在这份 helper 及其 `comoving_first_stage_patch.diff` 也已经不再是手工维护的孤立草稿，而是可以通过 `scripts/build_comoving_first_stage_patch.py` 从 `comoving-stable-vs-no-comoving.json` ledger 自动重建，从而把阈值来源、helper 内容和 CMake wiring 绑定回同一份 reference 证据。

这一轮模块收口又往前走了一步：生成链现在不只输出 helper、diff 和 provenance note，还会自动生成 `comoving_first_stage_submission_packet.md`、`comoving_first_stage_pr_draft.md`，以及镜像 WarpX 目录结构的 `comoving_first_stage_bundle/`。前者固定 scope、review claim、checklist 和 follow-up boundary；PR draft 直接给出可复用的 title、summary、out-of-scope 列表与 reviewer checklist；staging bundle 则把 `analysis_comoving.py`、patch diff 和随附说明收成可直接复制到另一个 worktree 的目录包。进一步地，`PIC-tutor` 现在还补了 `scripts/stage_comoving_first_stage_patch.py`，可以对目标 WarpX worktree 先做 dry-run，再自动复制 helper 并只改写 `test_2d_comoving_psatd_hybrid` 那一段 CMake analysis wiring，而不碰其他 test block；`scripts/audit_comoving_first_stage_patch.py` 又把同一个目标 worktree 的状态判成 `unstaged / partial / staged` 三档，避免后续连“现在到底装没装进去”都只能靠人工 grep；`scripts/report_comoving_first_stage_patch.py` 则把这份状态和下一条推荐命令写成 markdown 预检报告，方便后续接续者直接接手；而 `scripts/preview_comoving_first_stage_patch.py` 再往前一步，把目标 checkout 将会发生的 helper/CMake 改动直接打印成 unified diff。换句话说，当前 `PIC-tutor` 已经把 comoving 第一阶段 patch 从“本地可验证的 helper 草案”继续推进成“可直接整理成 upstream 提交描述并交给真实 WarpX worktree 的 handoff bundle”。这不会自动证明 energy gate 已经成立，但它把第一阶段 patch 应该如何被诚实地提交、评审和后续拆分，收成了更稳定的文字资产。

本次重建和复核把上述 handoff 链重新跑通：`scripts/build_comoving_first_stage_patch.py` 由 stable/no-comoving ledger 生成 bundle，`audit/report/preview/stage --dry-run` 均成功；直接执行 bundle helper 时 stable 返回 `0`、no-comoving 返回 `1`，独立 contract 也确认 stable `spike_ratio=1.1103719982074416` 低于 `1.1114823702056489`，reference `1.1119614945212388` 被拒绝。目标 checkout 仍保持 `unstaged`，所以本节的结论是“交接包可复现且可审阅”，不是“WarpX upstream 已接入”。

因此，comoving reference 标定这块现在的闭合条件可以重新表述为：第一，正文诚实记录当前 `analysis=OFF`、第一阶段 finite/energy/spike gate 和第二阶段 `divE` gate 之间的证据等级差异；第二，stable ledger、no-comoving sibling 和 provenance note 已经 materialize，且已确认当前单进程样本不足以直接推出最终 `energy_ref_unstable`；第三，下一步若继续做 WarpX patch，就该把重心放在更贴近 upstream regression 的 repeated/MPI contrast，而不是继续停留在抽象方案描述。达到这一步，模块本身已经足够支撑一个“local calibration audit”版本号，但还不足以声称 WarpX 侧强 analysis gate 已经定稿。

在这之后，当前仓库又沿 `v_comoving` 本身做了一轮更窄的 sibling 扫描，结果记录在 `notes/code-reading/fieldsolver/25-psatd-comoving-velocity-candidate-scan.md` 与 `runs/fieldsolver-validation/comoving-reference-ledgers/comoving-velocity-scan.{md,json}`。这轮扫描刻意不改 filter、moving window、hybrid grid 或 deposition，只比较五条 velocity 路径：stable default selector、显式写回默认 `v_comoving`、半速 `v_comoving`、零 `v_comoving` 和反号 `v_comoving`。结果有三点最关键。第一，显式默认 `v_comoving` 与 stable baseline 的 `electric_energy` 和 `spike_ratio` 在舍入误差内完全重合，说明 default selector 本身不是隐藏变量。第二，`half-default-beta` 与 `zero-comoving` 都没有把末态电场能量抬高到 stable 之上，反而分别降到 `0.9880x` 和 `0.9551x stable`，因此“只沿 velocity 自身减弱 comoving”仍然给不出可用的 local energy-reference sibling。第三，反号 `v_comoving` 会把 `spike_ratio` 推到 `1.0622x stable`，但同时把 `electric_energy` 压到 `0.8028x stable`。这说明在 comoving family 内部，spike 与 energy 已经可以明确解耦：它是一个更坏的局部异常候选，却不是一个更高能量的末态候选。于是第一阶段 patch 的收口逻辑反而更清楚了：`finite + spike` 继续是当前最有本地证据支撑的主 gate，而 `energy gate` 若还要争取，就不应继续停留在本机 `v_comoving` 数值扫描，而应转向更接近 upstream regression 的 repeated/MPI contrast。

和这条 comoving 主线并行的后备收口方向，现在也可以写得更硬了：`notes/code-reading/fieldsolver/26-rz-psatd-validation-strong-criteria.md` 已经把 RZ PSATD 当前真正的强 validation 主线收成一张判据表。当前最强的 RZ PSATD regression 并不是 `test_rz_psatd_JRhom_LL2`，而是三条分开的 active family：第一，`test_rz_galilean_psatd*` 用 `analysis_galilean.py` 提供 RZ NCI suppression 与 `current_correction/periodic_single_box_fft` 的 charge gate；第二，`test_rz_langmuir_multi_psatd*` 用 `analysis_rz.py + analysis_utils.py` 提供解析 `Er/Ez` 波形与部分 charge-conservation gate；第三，`test_rz_pml_psatd` 用 `analysis_pml_psatd_rz.py` 提供 radial PML 残余场上界。相对地，`test_rz_psatd_JRhom_LL2` 当前仍只有 checksum。

如果把这条 fallback 线也按“能支撑什么论断”拆开，当前最稳妥的写法可以先固定成下面四层：

| 层级 | 代表测试 | 当前主判据 | 正文里允许写到的强度 |
|---|---|---|---|
| 强 NCI 抑制 | `test_rz_galilean_psatd*` | `analysis_galilean.py` 的末态全域 field-energy gate；`current_correction` 分支再加 `divE-rho/\epsilon_0` gate | 可直接写成 RZ Galilean PSATD 对 drifting-plasma NCI 的强 regression |
| 强解析场 / 局部守恒 | `test_rz_langmuir_multi_psatd*` | `analysis_rz.py` 的解析 `Er/Ez` 对照；部分 sibling 再加 `analysis_utils.py` 守恒 gate | 可写成 RZ PSATD 在 Langmuir 小振幅问题上的波形正确性和部分守恒 |
| RZ Langmuir current-correction runtime | `test_rz_langmuir_multi_psatd_current_correction` | 官方 `analysis_rz.py` 与独立 contract 均通过；`Er/Ez=1.0542e-1/1.9313e-2`，charge residual `5.4781e-14` | 当前项目级 1-rank evidence 可同时支撑解析场与同面 charge-conservation；不外推到 RZ JRhom LL2 |
| Standard RZ Langmuir PSATD runtime | `test_rz_langmuir_multi_psatd` | 官方 `analysis_rz.py` 与独立 field contract 均通过；`Er/Ez=1.1617e-1/1.5194e-2 < 0.12`，`current_correction=0` | 可支撑 standard RZ PSATD 的解析场与 filter workflow；charge gate 在该 sibling 中不适用 |
| RZ Langmuir PSATD-JRhom `CL4` runtime | `test_rz_langmuir_multi_psatd_JRhom_LL4` | 官方 `analysis_rz.py` 与独立 field contract 均通过；`Er/Ez=1.0994e-1/6.4303e-2 < 0.12`，`current_correction=0` | 可支撑 RZ PSATD-JRhom `CL4` 的解析场与 filter workflow；charge gate 在该 sibling 中不适用 |
三条结果已由 `scripts/summarize_rz_langmuir_psatd_family.py` 收成 family matrix：三者都使用 `RZ + PSATD + direct`，网格维度均为 `[64,128,1]`，解析场 gate 全部通过；只有 `current-correction` 行带 `charge=PASS`，standard 与 JRhom `CL4` 行明确标成 `NOT_APPLICABLE`。这张矩阵是 family-level runtime evidence，不是所有 geometry/order 组合的收敛研究。
| 强 PML 残余场 | `test_rz_pml_psatd` | `analysis_pml_psatd_rz.py` 的全域残余 `Er/Ez` 上界 | 可写成 RZ PSATD + radial PML 的吸收残余场控制 |
| checksum-only workflow | `test_rz_psatd_JRhom_LL2` | `analysis=OFF`，只保留 final checksum | 只能写成 JRhom LL2 的输出/流程回归，不能写成独立稳定性强判据 |

这张表的意义不在于再重复一遍 CMake，而是把“RZ PSATD 已经有哪些强 gate、哪些还没有”收成一本书里可直接引用的证据等级表。这样如果 comoving 第一阶段 patch 线暂时不直接上提，第 6 章接下来的最合理推进就不是继续堆外围 patch 工具，而是补 RZ JRhom LL2 的独立 main analysis，或至少继续保持这条线的表述纪律: 已有强 gate 的 family 就按强 gate 写，没有 main analysis 的 family 就明确写成 checksum-only workflow。

沿着这条缺口继续往前压，当前仓库又把 `test_rz_psatd_JRhom_LL2` 下一步到底该补哪类 analysis 单独判定了一次，结果记录在 `notes/code-reading/fieldsolver/27-rz-jrhom-ll2-analysis-direction.md`。关键结论是：这条 RZ JRhom 路线虽然也带 `update_with_rho + do_time_averaging`，但它并不像 `langmuir/analysis_rz.py` 那样站在一个小振幅、周期、解析可写的 modal scaffold 上。相反，它当前的 producer 形状是 moving window、rigid `driver`、`driver_back`、continuous-injection `plasma_e/plasma_p`、damped longitudinal boundary，再叠 `JRhom_LL2 + div cleaning` 的 application workflow；而 diagnostics 只输出 `Er Ez Bt jr jz rho rho_driver rho_plasma_e rho_plasma_p`，并没有 `divE`、`phi` 或可直接回代理论波形的 reduced diagnostic。这意味着如果第一步就强行走 Langmuir 式解析 `Er/Ez` gate，反而要先额外定义“理论上应该长什么样”。

在当前证据下，它更像 `analysis_psatd_CC1.py` 或 `analysis_galilean.py` 那类 stability-style gate 候选，而不是解析场 gate 候选。最实际的第一阶段主判据，应先尝试补一个末态 field-energy route：先在同一 workflow 上寻找最小改动的 reference sibling，确认是否存在稳定的 energy ordering；若 ordering 成立，再决定把第一阶段脚本收成 `finite + energy`，还是 `finite + energy + spike`。换句话说，`test_rz_psatd_JRhom_LL2` 现在最需要补的不是另一张解析场表，而是一条和 `nci_psatd_stability` family 口径一致的独立 stability-style main analysis。

这一步现在也已经不再只是口头计划。当前仓库新增了 `scripts/build_rz_psatd_reference_ledger.py` 与 `scripts/scan_rz_jrhom_reference_candidates.py`，并在 `notes/code-reading/fieldsolver/28-rz-jrhom-reference-sibling-scan.md` 里固定了第一批最小改动 sibling：保持当前 workflow 不变，只比较 `JRhom` 从 `LL2 -> CL1`、关闭 `do_time_averaging`、关闭 `divE/divB cleaning`，以及它们的组合。这样下一步就可以直接去跑 `diag1000025` 的 energy/spike ordering，而不需要再手工拼接 reference sibling 和 ledger 汇总流程。

这轮本地扫描现在已经给出第一批真正可用的排序。当前 `diag1000025` surface 上，`ll2-no-timeavg-cleaning` 同时给出最高 `electric_energy` 和最高 `spike_ratio`，因此它是第一阶段最像 unstable reference 的候选；相对地，单独关掉 `divE/divB cleaning` 并不会把能量抬高，`cl1-no-timeavg-no-cleaning` 虽然会略抬高 spike，但能量仍低于 baseline，而 `cl1-timeavg-cleaning` 更是被 `PsatdAlgorithmRZ.cpp` 的源码断言直接拒绝，因为 RZ `psatd.do_time_averaging=1` 只支持 `J` 线性时间依赖。这意味着下一步已经不必继续泛泛地“搜索 reference sibling”，而是可以直接围绕 baseline 与 `ll2-no-timeavg-cleaning` 这对候选去写第一阶段 `finite + energy` helper，并把 `spike` 作为增强项保留。

这条 helper 现在也已经落成脚本原型，记录在 `notes/code-reading/fieldsolver/29-rz-jrhom-first-stage-helper.md`。当前新增的 `scripts/analysis_rz_jrhom.py` 保持了和本地 `analysis_comoving.py` 类似的接口形态，但换成 RZ 字段口径：它始终检查 `Er/Ez/Bt/jr/jz/rho` 的 finite 性，默认从 `rz-jrhom-reference-scan.json` 读取 baseline `baseline-jrhom-ll2-timeavg-cleaning` 与 unstable reference `ll2-no-timeavg-cleaning`，并把

$$
\mathrm{err\_energy} = \frac{E_{\mathrm{plotfile}}}{E_{\mathrm{ref}}}
$$

作为主 gate，再用当前 stable/reference 比值乘一个很小的 safety factor 自动导出 `tol_energy`。按当前 ledger，baseline 样本满足 `err_energy = 9.7708651502456867 \times 10^{-1}`，而 reference sibling 自身会因为 `err_energy = 1` 在同一阈值下失败。这说明 `test_rz_psatd_JRhom_LL2` 这条线已经不只是“知道下一步该写 helper”，而是已经具备了一个可直接运行的第一阶段 `finite + energy` 原型。

与此同时，`spike` 仍被刻意保留为第二层增强项，而不是第一阶段默认主合同。原因不是它没有分辨力，而是当前最需要先回答的问题，是这条 RZ JRhom workflow 能否像 `analysis_psatd_CC1.py` 那样先拥有一条稳定性主 gate。现在答案已经是肯定的：至少在 `diag1000025` 这一张 active checksum surface 上，当前仓库已经把这条主 gate 收成了可运行脚本和可追溯阈值来源。后续若 repeated/MPI 设置或更长时间窗继续支持同样 ordering，再决定是否把这条 helper 真正上提到 WarpX `Examples/Tests/nci_psatd_stability/`，以及是否把 `spike` 从可选增强项升级成正式第二 gate。

这一轮继续往 upstream 方向推进时，还多得到了一条同样重要的执行边界，记录在 `notes/code-reading/fieldsolver/30-rz-jrhom-input-numprocs-audit.md`。`test_rz_psatd_JRhom_LL2` 的输入卡本身写着 `warpx.numprocs = 1 2`，而 `CMakeLists.txt` 里它也注册成 `nprocs = 2`。当前仓库先把 `scan_rz_jrhom_reference_candidates.py` 扩成可显式切换 `--numprocs-override` 和 `--command-prefix-str` 的脚本，再用 `--numprocs-override none` 做输入卡原生审计。第一轮 plain single-process 调用确实统一触发了 `warpx.numprocs, if specified ... number of processes` 断言，说明单进程 direct invocation 与输入卡原生 `1 x 2` decomposition 的进程数合同不匹配；但这条线没有停在“缺 launcher”上。进一步搜索本机环境后，当前已经在另一个 Conda 环境里找到可用的 `mpiexec -n 2`，并用同一脚本真正重跑出 `rz-jrhom-reference-scan-mpi2.{md,json}`。结果更关键：baseline、`ll2-no-timeavg-cleaning`、`ll2-timeavg-no-cleaning` 和 `cl1-no-timeavg-no-cleaning` 都能在 2 ranks 下落出 `diag1000025`，而且 repeated/MPI 下的 energy 排序与本机 `1 1` 快速样本完全一致，仍然是 `ll2-no-timeavg-cleaning > baseline > cl1-no-timeavg-no-cleaning > ll2-timeavg-no-cleaning`。这意味着当前 `finite + energy` helper 已经不再只是本机单进程样本的临时口径，而是有了更贴近 upstream regression 形状的 2-rank 复核支持。它当然还没有自动变成 WarpX upstream 的正式 analysis，但至少“当前排序只是单进程偶然产物”这条怀疑，现在已经没有证据支撑了。

更进一步，当前仓库已经把这条 repeated/MPI 已验证的 helper 又往前收成了一套真正可交接的 handoff 资产，记录在 `notes/code-reading/fieldsolver/31-rz-jrhom-first-stage-patch-draft.md`。具体来说，`scripts/build_rz_jrhom_first_stage_patch.py` 现在会从 `rz-jrhom-reference-scan-mpi2.json` 自动重建六类产物：`analysis_rz_jrhom_first_stage_draft.py`、`rz_jrhom_first_stage_patch.diff`、`rz_jrhom_first_stage_provenance_note.md`、`rz_jrhom_first_stage_submission_packet.md`、`rz_jrhom_first_stage_pr_draft.md` 和 `rz_jrhom_first_stage_bundle/`。它们的作用和边界都很明确：第一阶段 patch 只声称 `finite + energy`，仍保留现有 checksum，不引入新的 diagnostics surface，也不把 spike gate 一起塞进第一版草案。这样一来，RZ JRhom LL2 这条线现在已经不只是“有一个本地可运行 helper”，而是已经具备了 helper、diff、review 口径和 bundle 目录一体化的上提草案。

但仅有 bundle 还不够，因为真正的接续问题不是“能不能再生成一份 diff”，而是“目标 WarpX checkout 当前到底是什么状态，这份 bundle 会对它造成什么精确改动”。因此当前仓库又补了 `notes/code-reading/fieldsolver/32-rz-jrhom-target-checkout-workflow.md`，把这一轮工程闭合点压到 target-checkout workflow：`scripts/preview_rz_jrhom_first_stage_patch.py` 只读打印 unified diff，`scripts/audit_rz_jrhom_first_stage_patch.py` 把目标 worktree 判成 `unstaged / partial / staged` 三档，`scripts/report_rz_jrhom_first_stage_patch.py` 自动生成 markdown 预检报告，而 `scripts/stage_rz_jrhom_first_stage_patch.py` 则在显式传入 `--warpx-root` 的前提下支持 dry-run 和最小写入 staging。它们共同绑定的写入面很克制：只新增 `Examples/Tests/nci_psatd_stability/analysis_rz_jrhom.py`，并只把 `test_rz_psatd_JRhom_LL2` 的 analysis 行从 `OFF` 改成 `"analysis_rz_jrhom.py diags/diag1000025"`，不碰任何其他 test block、checksum 行或 dependency 行。这样第 6 章现在已经不只是“说明如何设计这条 helper”，而是已经把“如果要把它交给另一个 WarpX checkout，应当先如何预览、审计、报告和 staging”收成了可直接执行的工程流程。换句话说，当前这条线的下一步已经不再是继续打磨 handoff 文本，而是非常具体的两种选择：要么在目标 checkout 上按当前口径做 preview/report/dry-run/stage，并准备实际提交流程；要么把它作为一个已经闭合的 first-stage boundary 暂时冻结，转去推进下一个成书模块。

截至 2026-07-12，对相邻目标 checkout `../warpx` 的只读审计结果是：整体状态为 `unstaged`；`Examples/Tests/nci_psatd_stability/analysis_rz_jrhom.py` 尚不存在；`test_rz_psatd_JRhom_LL2` 的 CMake analysis 行仍是 `OFF`。本轮重新运行 audit、dry-run 和 unified preview，三者均成功，精确改动仍只有两项：新增第一阶段 `finite + energy` helper，以及把该 test 的 analysis 行改成 `"analysis_rz_jrhom.py diags/diag1000025"`。因此当前项目可以声称“RZ JRhom first-stage handoff bundle 和目标 checkout workflow 已准备好”，但不能声称 patch 已经写入 WarpX，更不能声称 upstream regression 已经接入。

这次审计报告已写入 `notes/code-reading/fieldsolver/rz_jrhom_first_stage_target_report.md`，运行级 JSON/Markdown 快照另归档于 `runs/fieldsolver-validation/rz-reference-ledgers/rz-jrhom-first-stage-target-audit.{json,md}`。它把 bundle 状态、helper 状态、CMake 状态和下一条推荐命令固定在同一份可接续记录中；后续若要实际 staging，仍需显式传入目标 checkout 并先执行 dry-run，当前书稿工作本身不修改 `../warpx`。

### 6.8.5 PSATD/场求解器算法族决策矩阵

前面的各节分别解释了系数、源项时间依赖和验证脚本，但读者在实际阅读输入卡或源码时还需要一个横向索引。下面这张表只做算法族导航，不把同名系数强行合并；“验证强度”描述的是本项目当前 checkout 中能直接找到的证据等级，不等于算法理论上的完整正确性。

| 算法族 | 主要谱基/空间表示 | 源项时间模型 | 粒子沉积与组合限制 | 代表系数或字段 | 当前可用验证证据 |
|---|---|---|---|---|---|
| FDTD / Yee / CKC | 实空间有限差分 stencil | 按离散时间层推进 `E/B/J` | 依赖对应的 current deposition、guard-cell 和边界链；不进入 PSATD 的谱系 | Yee/CKC 差分算子、split-field PML 系数 | NCI FDTD、PML 和部分解析场 regression 可提供强判据 |
| Cartesian standard PSATD | 3D Fourier `k` 空间 | 常规 `J`/`rho` 时间依赖与可选 current correction | 与 `grid_type`、`current_deposition`、filter 和 periodic FFT 组合受约束 | `C`、`S_ck`、`K^{-2}`、`X1-X4` | Langmuir、NCI energy、Gauss-law 和部分 PML regression |
| Cartesian Galilean PSATD | Fourier `k` 空间 + Galilean moving frame | 以 `v_galilean` 修正相位和源项积分 | 与 current correction、Vay、JRhom、implicit 等存在反向兼容约束 | Galilean `X1-X4`、`Theta2`、average-field `Psi/Y` | `analysis_galilean.py` 提供较成熟的 NCI/energy 与部分 charge gate |
| Cartesian comoving PSATD | regular-domain Fourier `k` 空间 + `v_comoving` | comoving 相位、`rho` 参考层和 current correction | 当前要求 direct deposition、`update_with_rho=1`；不支持 Esirkepov/Villasenor/Vay 和 JRhom 组合 | comoving `X1-X4`、`Theta2`、comoving continuity residual | 当前有 local `finite + spike` 原型；energy reference 尚未形成可靠 ordering |
| Cartesian PSATD-JRhom | Fourier `k` 空间 + 子区间推进 | `J/rho` 在一个 PIC 步内按 constant/linear/quadratic 形式分段采样 | 不支持 Vay 和 Galilean PSATD；外层 `OneStep_JRhom()` 改写沉积与谱推进时序 | JRhom `Y1-Y8`、`E/B/F/G` 子区间更新 | `analysis_psatd_CC1.py` 有强 NCI/energy 入口；其余家族需按时间模型分别验证 |
| RZ standard / Galilean PSATD | `k_z` FFT + `k_r` Hankel/Bessel roots；`Ep/Em/Ez` 字段布局 | standard 或轴向 Galilean 相位/源项积分 | RZ mode 对称性、轴上 guard、current correction 和 time-averaging 有独立限制；不支持 Vay | standard `X1-X3/X5-X6`；Galilean `X1-X4/Theta2/T_rho` | RZ Langmuir、RZ Galilean NCI、RZ PML 可提供强判据 |
| PSATD PML | split-field spectral/PML 表示 | 吸收层内使用专用 split-field 时间推进 | 受 PML profile、方向、RZ 分支和 `C1-C25` 系数合同约束 | `C1-C25`、PML split fields | Cartesian/RZ PML residual-field analysis；论文闭环仍待 Lee/Vay 全文 |

读这张表时应先区分三种“选择”：第一是谱基或空间离散（FDTD、Cartesian Fourier、RZ Hankel/Fourier）；第二是源项时间模型（普通、Galilean/comoving、JRhom）；第三是沉积与同步组合（Direct、charge-conserving current、Vay、current correction、filter）。例如，`JRhom` 的 `Y1-Y8` 不能因为名字与 Galilean average-field 的 `Y1-Y4` 相似就合并解释；同样，RZ 的 `Ep/Em` 不是 Cartesian `Ex/Ey` 的简单改名。

验证列也应按证据等级阅读。`analysis_galilean.py`、Langmuir 解析场和 PML residual-field analysis 已经能对相应 family 提供较强的物理断言；`test_rz_psatd_JRhom_LL2` 的上游 CMake 仍是 checksum/workflow 入口，但本地 repeated/MPI ledger 已支持一个通过正/负对照的 `finite + energy` helper，二者必须分开写。comoving 同理：本地 ledger 已验证分支选择和 `finite + spike` 方向，却还没有证明可复用 Galilean 式 `energy_ref`。这张矩阵因此同时是算法选择表和证据边界表。

本轮又把这条 helper 收成独立的正/负 contract：`scripts/analyze_rz_jrhom_first_stage_contract.py` 直接读取真实 2-rank repeated/MPI 末态 plotfile，要求 baseline 被 energy ceiling 接受、`ll2-no-timeavg-cleaning` reference 被同一 ceiling 拒绝。实际 baseline energy ratio 为 `0.9770894022295227`，reference ratio 为 `1.0`，由 `1.001` safety factor 导出的阈值为 `0.9780664916317521`；六个字段 `Er/Ez/Bt/jr/jz/rho` 在两组 plotfile 中均 finite。报告位于 `runs/fieldsolver-validation/rz-reference-ledgers/rz-jrhom-first-stage-contract.{json,md}`。这仍是 project-level repeated/MPI validation，不等于 WarpX upstream CMake 已经接入 analysis；spike 只记录、不作为第一阶段主 gate。

### 6.8.6 v0.74 文献闭环：Andriyash 2016 Fourier-Bessel PSATD

本版新增 `references/03_pic_foundations/2016_AndriyashPoP2016_Laser-plasma_interactions_with_a_Fourier-Bessel_particle-in-cell_method/`：本地 9 页 PDF 已经完成 MinerU、26 张图片提取、按论文顺序中文精读和 `scripts/audit_andriyash_2016_asset_contract.py` 资产合同。它补的是 RZ/准柱坐标谱求解器的 primary-source 背景，而不是再增加一条泛泛的 PSATD 书目。

论文把空间坐标写为 `(x,r,theta)`，用角向 Fourier mode 和径向 Bessel/Hankel transform 构造柱谐基；Laplace 算子满足

$$
\widehat{\nabla^2 f}=-\omega^2\widehat f,
\qquad
\omega=\sqrt{k_x^2+k_r^2},
$$

所以 `epsilon` 和辅助场 `g` 可以在谱空间中按受迫振子解析推进，而一阶 `gradient/div/curl` 只在每步投影和粒子通信时重新计算。论文的时间步顺序是“粒子位置推进 -> 按 angular mode 沉积 `n/J` -> 谱投影 -> 解析场推进 -> 回投影 -> Lorentz force”，这与本章当前强调的 RZ 源项/场推进分层相互印证。

更重要的是，论文没有把 charge continuity 当作 Maxwell 时间积分自动解决的问题。它显式写出

$$
\partial_t n+\nabla\cdot\mathbf{j}=0
$$

并给出在 Fourier-Bessel 矩阵导数上执行的 current correction。这个来源可以帮助读者理解 WarpX RZ PSATD 中 `rho`、`Jp/Jm/Jz`、`Ep/Em/Ez` 和 current correction 为什么必须单独成层；但论文实现是 PLARES-PIC，不能直接声称与 `PsatdAlgorithmRZ` 逐函数等价。

论文 benchmark 的两条结论也保持窄化：线性激光传播中，PSATD 在较粗网格上更接近群速度理论；密度 shock 注入中，PSATD 与 FDTD 的 wake 结构接近，但电子束细结构和横向速度受到 FDTD 数值色散、数值 Cherenkov 与 Lorentz force 投影误差影响。对应的 PLARES-PIC/CALDER-CIRC 图和 `33 pC/28 pC` 电荷对照属于论文级证据，不是 WarpX plotfile 或官方 regression。

本论文包的分类是 `FULL_TEXT_MINERU_CHINESE_NOTE_VERIFIED_WARPX_EQUIVALENCE_BOUNDARY`：它关闭了“该 RZ/准柱坐标谱方法只有书目线索”的缺口，但没有关闭 WarpX runtime reproduction、PLARES-PIC 函数级映射或论文 benchmark 逐图复现。

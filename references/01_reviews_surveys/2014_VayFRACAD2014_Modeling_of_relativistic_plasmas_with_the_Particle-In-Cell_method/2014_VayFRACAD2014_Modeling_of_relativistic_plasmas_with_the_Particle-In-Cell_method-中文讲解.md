# 相对论等离子体 PIC 方法综述：Vay 与 Godfrey 2014

## 0. 论文信息与阅读边界

- **题名**：*Modeling of relativistic plasmas with the Particle-In-Cell method*
- **作者**：Jean-Luc Vay、Brendan B. Godfrey
- **发表信息**：*Comptes Rendus Mécanique* 342 (2014), 610--618，DOI `10.1016/j.crme.2014.07.006`。
- **本地资产**：9 页 PDF、MinerU Markdown、43 张图片和本中文精读。
- **论文对象**：综述标准相对论电磁 PIC、Warp 时代的 FDTD/NSFDTD/PSATD/PSTD、粒子推进、沉积、场 gather、filter 与 NCI；不是当前 WarpX 的实现论文。

本文最适合用作本书第 4、6 章的“算法谱系入口”。它把 PIC 中三个容易混写的层次分开：Maxwell 场求解器、粒子 pusher、粒子-网格投影/守恒；再把 NCI 解释为粒子 beam aliases 与数值电磁模的耦合。文中的 Warp 结果可作为历史/理论来源，但不能写成 WarpX 当前 checkout 的 runtime 结果。

## 1. 摘要与 Introduction

摘要回顾相对论电磁 PIC 的标准方法和新技术，重点是 NCI 的解析分析、抑制方法以及 Warp 数值实验。作者强调，超相对论 regime 中 NCI 最强，若没有 corrective measures，粒子束和 streaming plasma 的模拟适用范围会显著收缩。

PIC 的基本对象是网格上的电磁场和宏粒子。自然单位下 Maxwell 方程为

$$
\frac{\partial\mathbf{B}}{\partial t}=-\nabla\times\mathbf{E},
\qquad
\frac{\partial\mathbf{E}}{\partial t}=\nabla\times\mathbf{B}-\mathbf{J},
$$

$$
\nabla\cdot\mathbf{E}=\rho,
\qquad
\nabla\cdot\mathbf{B}=0.
\tag{1--4}
$$

粒子服从 Newton-Lorentz 方程

$$
\frac{d\mathbf{x}}{dt}=\mathbf{v},
\qquad
\frac{d(\gamma\mathbf{v})}{dt}
=\frac{q}{m}(\mathbf{E}+\mathbf{v}\times\mathbf{B}),
\qquad
\gamma=(1-\nu^2)^{-1/2}.
\tag{5}
$$

PIC 的闭环不是“先解场再推粒子”这么简单：粒子位置/速度产生 `rho/J`，场从网格 gather 回粒子，离散 Gauss law 和粒子投影必须同时相容。

## 2. PIC main steps 与场求解器

### 2.1 Yee/FDTD

二阶 FDTD 用 staggered Yee grid：E 位于 cell edges，B 位于 cell faces，rho 位于 nodes；图 1 是这条空间布局的几何依据。

![图 1：Yee staggered grid 的场分量布局](images/66e6c3ea9d58f09321242dcfa15d2925b03fcfc4452c037adff180a2ca44c1fd.jpg)

**图 1 解读：** staggered placement 让离散 curl 具有局部几何结构，但也意味着 field gather 需要处理不同分量的偏移。离散时间导数和 x 向差分可写为

$$
D_tG\big|^n_{i,j,k}
=\frac{G^{n+1/2}_{i,j,k}-G^{n-1/2}_{i,j,k}}{\Delta t},
$$

$$
D_xG\big|^n_{i,j,k}
=\frac{G^n_{i+1/2,j,k}-G^n_{i-1/2,j,k}}{\Delta x}.
$$

FDTD 的离散方程是

$$
D_t\mathbf{B}=-\nabla\times\mathbf{E},
\qquad
D_t\mathbf{E}=\nabla\times\mathbf{B}-\mathbf{J}.
\tag{7--8}
$$

离散 Gauss law 通常依靠初始条件和 charge-conserving current deposition 保持，而不是每步单独求解式 (9--10)。

### 2.2 NSFDTD / Cole-Karkkainen

NSFDTD 用扩展 stencil 替换部分差分算子。其关键是

$$
\nabla^*=D_x^*\hat{\mathbf{x}}+D_y^*\hat{\mathbf{y}}+D_z^*\hat{\mathbf{z}},
$$

并以

$$
D_t\mathbf{B}=-\nabla^*\times\mathbf{E},
\qquad
D_t\mathbf{E}=\nabla\times\mathbf{B}-\mathbf{J}.
\tag{11--12}
$$

替代标准 FDTD。对 cubic cells，作者给出 `alpha=7/12`、`beta=1/12`、`xi=1/48` 的 Cole-Karkkainen 取值，可在主轴方向放宽色散并达到 `Delta t = Delta x` 的 Courant limit。但 Nyquist 波长附近会出现 instability，需要滤除 source terms 的 Nyquist component。这里的 lesson 是：放宽 CFL 和降低主轴色散不等于稳定性自动成立。

### 2.3 PSATD 与 PSTD

Fourier 空间 Maxwell 方程为

$$
\partial_t\widetilde{\mathbf{E}}
=i\mathbf{k}\times\widetilde{\mathbf{B}}-\widetilde{\mathbf{J}},
\qquad
\partial_t\widetilde{\mathbf{B}}
=-i\mathbf{k}\times\widetilde{\mathbf{E}}.
\tag{15--16}
$$

若初始时满足 Gauss law 且连续性方程

$$
\partial_t\widetilde{\rho}+i\mathbf{k}\cdot\widetilde{\mathbf{J}}=0,
$$

则纵向约束随时间自动保持。把 E 和 J 分解成 longitudinal/transverse：

$$
\widetilde{\mathbf{E}}=\widetilde{\mathbf{E}}_L+\widetilde{\mathbf{E}}_T,
\qquad
\widetilde{\mathbf{J}}=\widetilde{\mathbf{J}}_L+\widetilde{\mathbf{J}}_T,
$$

横向场形成频率 `k` 的振子，纵向电场由纵向电流直接更新。假设 `J` 在一个时间步内常量，解析积分给出

$$
\widetilde{\mathbf{E}}_T^{n+1}
=C\widetilde{\mathbf{E}}_T^n
+iS\hat{\mathbf{k}}\times\widetilde{\mathbf{B}}^n
-\frac{S}{k}\widetilde{\mathbf{J}}_T^{n+1/2},
$$

$$
\widetilde{\mathbf{E}}_L^{n+1}
=\widetilde{\mathbf{E}}_L^n-\Delta t\widetilde{\mathbf{J}}_L^{n+1/2},
$$

$$
\widetilde{\mathbf{B}}^{n+1}
=C\widetilde{\mathbf{B}}^n
-iS\hat{\mathbf{k}}\times\widetilde{\mathbf{E}}^n
+i\frac{1-C}{k}\hat{\mathbf{k}}\times\widetilde{\mathbf{J}}^{n+1/2},
\tag{22--24}
$$

其中

$$
C=\cos(k\Delta t),
\qquad
S=\sin(k\Delta t).
$$

组合纵向/横向分量后得到完整 E 更新式（论文式 25）和 B 更新式（论文式 26）。该解对无粒子自洽反馈的场源没有数值色散，也没有通常意义下的 Courant limit；但“精确”依赖 `J` 在步内常量这一源项假设。

对 `S` 和 `C` 做小 `Δt` 展开并保留低阶项，PSATD 退化为 PSTD：

$$
\widetilde{\mathbf{E}}^{n+1}
=\widetilde{\mathbf{E}}^n
+i\Delta t\mathbf{k}\times\widetilde{\mathbf{B}}^{n+1/2}
-\Delta t\widetilde{\mathbf{J}}^{n+1/2},
$$

$$
\widetilde{\mathbf{B}}^{n+3/2}
=\widetilde{\mathbf{B}}^{n+1/2}
-i\Delta t\mathbf{k}\times\widetilde{\mathbf{E}}^{n+1}.
\tag{27--28}
$$

PSTD 重新引入有限时间步的数值色散和 Courant condition；PSATD 与 PSTD 不是同义词。PSATD 也可以通过 phase factors 重写到 staggered Yee grid，故 collocated/staggered 是布局选择，不是算法名称的唯一判据。

## 3. Particle push

### 3.1 Boris relativistic rotation

中心差分先写成

$$
\frac{\mathbf{x}^{i+1}-\mathbf{x}^i}{\Delta t}
=\mathbf{v}^{i+1/2},
$$

并以 `u = gamma v` 将电场半步和磁场旋转分开。Boris 序列是

$$
\mathbf{u}^-=mathbf{u}^{i-1/2}+\frac{q\Delta t}{2m}\mathbf{E}^i,
$$

$$
\mathbf{u}'=\mathbf{u}^-+\mathbf{u}^-\times\mathbf{t},
\qquad
\mathbf{u}^+=\mathbf{u}^-+\mathbf{u}'\times\frac{2\mathbf{t}}{1+t^2},
$$

$$
\mathbf{u}^{i+1/2}=\mathbf{u}^++\frac{q\Delta t}{2m}\mathbf{E}^i,
\tag{32--35}
$$

其中 `t` 包含 `q Delta t B/(2m gamma)`。这套拆分的工程优势是避免显式求解中间 gamma；但本节的 Boris 讨论属于综述来源，当前 WarpX 的实现仍应回到 `UpdateMomentumBoris.H`。

### 3.2 Lorentz-invariant velocity average

作者总结另一种以

$$
\bar{\mathbf{v}}^i
=\frac{\mathbf{v}^{i+1/2}+\mathbf{v}^{i-1/2}}{2}
\tag{36}
$$

为基础的 Lorentz-invariant formulation。先构造

$$
\mathbf{u}^*
=\mathbf{u}^i+\frac{q\Delta t}{m}
\left(\mathbf{E}^i+\frac{\mathbf{v}^{i-1/2}}{2}\times\mathbf{B}^i\right),
\tag{37}
$$

再用

$$
\mathbf{u}^{i+1/2}
=\frac{\mathbf{u}^*+(\mathbf{u}^*\cdot\mathbf{t})\mathbf{t}
+\mathbf{u}^*\times\mathbf{t}}{1+t^2}.
\tag{38}
$$

它面向超相对论粒子束中自生电场和磁场的精确抵消问题。第 4 章可以用它说明“pusher 的相对论性质”和“当前 WarpX pusher 分派”是两个证据层。

## 4. Current deposition、field gather 与 filtering

### 4.1 Current deposition 与连续性

电流用不同阶数 spline 从粒子位置和速度沉积到网格。论文强调，离散 Gauss law 的长期误差有两条路线：使用与 Yee solver 相容的 charge-conserving deposition，或使用 divergence cleaning。

对 pseudo-spectral solver，普通 deposition 未必满足 Fourier 连续性

$$
\widetilde{\rho}^{n+1}
=\widetilde{\rho}^{n}
-i\Delta t\mathbf{k}\cdot\widetilde{\mathbf{J}}^{n+1/2}.
$$

因此可对电场做 Boris correction：

$$
\widetilde{\mathbf{E}}_c^{n+1}
=\widetilde{\mathbf{E}}^{n+1}
-\frac{\mathbf{k}\cdot\widetilde{\mathbf{E}}^{n+1}+i\widetilde{\rho}^{n+1}}{k}\hat{\mathbf{k}},
$$

也可直接修正电流

$$
\widetilde{\mathbf{J}}_c^{n+1/2}
=\widetilde{\mathbf{J}}^{n+1/2}
-\frac{\mathbf{k}\cdot\widetilde{\mathbf{J}}^{n+1/2}
-i(\widetilde{\rho}^{n+1}-\widetilde{\rho}^{n})/\Delta t}{k}\hat{\mathbf{k}}.
$$

第二种修正保持横向电流不变，只替换纵向分量，使修正后电流满足连续性。这个区分直接连接到本书第 5/6 章：charge-conserving deposition、spectral current correction 和 Gauss-law analysis 不是同一个 mechanism。

### 4.2 Field gather 的三种语义

论文区分：

1. **momentum conserving**：所有场分量使用 node-centered spline；
2. **energy conserving / Galerkin**：根据 E/B 分量在 Yee grid 上的不同位置，使用偏移一个 cell 的 spline；
3. **uniform**：所有分量用相同的 spline 直接从 Yee grid gather。

momentum/energy conserving 的命名描述的是 `Δt -> 0` 极限以及有限步长下对应守恒量的偏好；uniform 方案不按这两个定义保证守恒，但在 relativistically drifting plasma 中可能有特殊稳定性优势。不能把 `particle_shape` 阶数直接当成 gather semantic。

### 4.3 Digital filtering

三点 filter 为

$$
\phi_j^f=\alpha\phi_j
+\frac{1-\alpha}{2}(\phi_{j-1}+\phi_{j+1}).
$$

对 Fourier mode `exp(ikx)`，gain 是

$$
g(\alpha,k)=\alpha+(1-\alpha)\cos(k\Delta x)
\simeq 1-(1-\alpha)\frac{(k\Delta x)^2}{2}+O(k^4).
$$

`n` 次 filter 的总 gain 是各次 gain 的乘积。若使用 compensation step，使低阶衰减项抵消，则可以在保留低波数的同时形成更尖锐的高波数 cutoff。stride `s` 只把 `k` 替换为 `sk`，因此可用少量短 stencil 组合出宽频带抑制；论文给出 stride 1/2/4 的组合相对于大量 bilinear passes 的操作量与 footprint 优势。

## 5. Numerical Cherenkov instability

NCI 来自两类离散对象的耦合：粒子按 Lagrangian 轨迹推进，场按 Eulerian 网格推进；数值电磁模和 beam aliases 的相速度不匹配，便可能共振。

高能极限下，论文把 FDTD/PSATD 的色散关系统一写成

$$
C_0+n\sum_{m_z}C_1\csc\left[
\left(\omega-k'_z\right)\frac{\Delta t}{2}\right]
+n\sum_{m_z}C_2\csc^2\left[
\left(\omega-k'_z\right)\frac{\Delta t}{2}\right]=0,
\tag{39}
$$

其中

$$
k'_z=k_z+m_z\frac{2\pi}{\Delta z}
$$

是 numerical alias。`C_0=0` 给真空电磁模，其他项给 beam mode 与 alias coupling；因此即使 `m_z=0`，仍可能出现数值共振。共振增长率大致随 `cube root of n C_2 / Delta t` 标度，非共振项大致随 `sqrt(n C_2)` 标度。

![图 2：FDTD 与 PSATD 的 normal-mode 图](images/badbf811d884ff5857e014253529dc0428691100e090e33164d8791bef1a3d4b.jpg)

![图 2 对照：PSATD normal-mode 图](images/d4a47a47d7688e78f26aaa46d08c770827d245a246d0e90afcf9026e3d6d14df.jpg)

**图 2 解读：** 对相同 relativistic beam 参数，FDTD 的数值色散电磁模与 beam aliases 更容易形成交叉；PSATD 的真空模没有通常 FDTD 那样的数值色散，但仍可能因粒子/场耦合产生 NCI。

![图 3：FDTD NCI resonances 与 growth rates](images/c5cee7fa3524c01e4a755acee5803f58a85237c719cbf12c98a1e61d2f0493e7.jpg)

![图 3 对照：NCI growth-rate 曲线](images/e77e379bf60b4d3008895ccc601b621b5ca466a3f4508fa9e85d7057f5648722.jpg)

高阶 interpolation 会压低高阶 mode，digital filtering 会直接切掉大波数；二者组合能显著降低 growth rate。论文还讨论 FDTD Galerkin 的 “magic time step”：它来自 `E_x/B_y` 在主共振附近对 `C_2` 的近似抵消；Uniform interpolation 在高 gamma 极限下于 `nu Delta t / Delta z = 0.5` 使 `C_2` 恒为零。

PSATD 变体 b1/b2 直接在 k-space 调整 field/current relation。例如 b1 调整粒子看到的 `E_x/B_y`，使 `nu=1` 时 `C_2` 解析消失；b2 设置相关 `C_3x` 系数为零。它们与 filter、插值阶数是不同的稳定化轴，不能合并成一个“打开 NCI filter”的开关。

![图 4：FDTD/PSATD NCI 最大增长率](images/c5cc80fc62cb38c50ffc26e5e1c034772f27f902fc2dc7a67d37acb789d13d81.jpg)

**图 4 解读：** 左图是 cubic interpolation + digital filtering，右图是对色散关系系数的修正。论文的重点是“增长率可以通过多个独立 mechanism 叠加压低”，而不是某个单一参数对所有几何/时间步都有效。

## 6. 结论与本书映射

论文的综述主线可压缩为：

1. FDTD、NSFDTD、PSATD、PSTD 是 field solver family；
2. Boris 与 Lorentz-invariant pusher 是 particle update family；
3. deposition、gather、filter 和 current/field correction 决定离散约束如何在粒子与网格间传递；
4. NCI 是这些层次组合后在 relativistic beam/streaming plasma 中出现的耦合 instability。

### 6.1 对第 4 章的有界贡献

可引用 Boris 半步旋转和 Lorentz-invariant velocity average 的历史公式，解释为什么相对论 pusher 不能只看非相对论 `v x B` 旋转。当前 WarpX 的 `UpdateMomentumBoris.H`、Vay 和 Higuera-Cary 分派仍必须单独按源码和 runtime contract 验证。

### 6.2 对第 6 章的有界贡献

式 (15)--(26) 给出 PSATD 的 longitudinal/transverse decomposition、`C/S` 解析推进和无传统 Courant limit 的理论入口；式 (39) 给出 NCI alias-resonance 的分析入口。当前 WarpX 的 Cartesian PSATD、Galilean/comoving、JRhom、RZ 和 PML 是不同 algorithm class，不能因为共享 `C/S` 或 `X/Y` 名字就按论文公式直接合并。

### 6.3 证据边界

论文中提到的 Warp 代码、图 2--4 的 growth-rate 曲线和 magic time step 是综述/历史数值实验来源。它们不自动证明当前 WarpX checkout 的 `analysis_galilean.py`、NCI regression、RZ PSATD 或 PML contract 已通过。当前书稿应继续遵守“论文公式、WarpX 源码、case-local runtime”三层分开记账。

## 7. 复习速记与开放问题

### 7.1 速记

**PSATD 通过 Fourier 空间解析推进降低场的数值色散，但没有消除 particle-field alias coupling；NCI 的抑制必须同时考虑 field solver、particle interpolation、current deposition、filter 和时间步。**

### 7.2 开放问题

- 论文的 NCI dispersion relation 以 Warp 为数值实验对象，当前 WarpX 需要独立复核参数、几何和 analysis consumer。
- 文中的 `magic time step` 是特定 interpolation/solver/beam 参数下的高 gamma 近似，不应写成通用稳定性定理。
- current correction、charge-conserving deposition 和 divergence cleaning 各自改变的对象不同；必须回到当前 WarpX 源码判断它们在具体 algorithm family 中的实际顺序。

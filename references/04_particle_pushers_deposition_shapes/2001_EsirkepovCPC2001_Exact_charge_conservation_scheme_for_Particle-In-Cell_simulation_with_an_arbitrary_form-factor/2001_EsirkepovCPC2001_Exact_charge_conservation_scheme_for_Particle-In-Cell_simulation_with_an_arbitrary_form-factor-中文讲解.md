# Esirkepov 1999/2001 charge-conserving current deposition 笔记

## 0. 论文信息

- 原题（当前取得的合法全文）：
  - `Exact charge conservation scheme for Particle-in-Cell simulations for a big class of form-factors`
- 作者：T. Zh. Esirkepov
- 预印本：arXiv `physics/9901047`
- 出版版对应：
  - `Exact charge conservation scheme for Particle-in-Cell simulation with an arbitrary form-factor`
  - `Computer Physics Communications 135(2), 144-153 (2001)`
  - DOI：`10.1016/S0010-4655(00)00228-9`
- 本地 PDF：
  - `2001_EsirkepovCPC2001_Exact_charge_conservation_scheme_for_Particle-In-Cell_simulation_with_an_arbitrary_form-factor.pdf`
- MinerU Markdown：
  - `2001_EsirkepovCPC2001_Exact_charge_conservation_scheme_for_Particle-In-Cell_simulation_with_an_arbitrary_form-factor.md`
- 所属主题：
  - charge-conserving current deposition
  - continuity equation
  - tensor-product form factor
- 对 `PIC-tutor` 的用途：
  - 作为第 5 章 Esirkepov current deposition 的第一手 paper-backed 来源；
  - 解释为什么电流不能只按 `q v S` 直沉，而必须从离散连续性方程反推；
  - 给 WarpX `doEsirkepovDepositionShapeN<N>()` 的 old/new shape-difference 结构提供历史算法来源。

## 1. 摘要

摘要的主结论很集中，不是泛泛说“提出一种更好的 PIC 算法”，而是明确提出：

1. 不再依赖每步再解一次 Poisson 方程去纠正电场的“势能部分”；
2. 直接构造一个在有限差分意义下严格满足连续性方程的电流定义；
3. 这套构造被作者称为 `density decomposition`；
4. 它至少适用于任意可写成一维 shape 乘积的 `n` 维 form-factor；
5. 文中用二阶抛物 spline 作为具体演示。

也就是说，这篇 paper 的第一性目标不是“再造一个 Maxwell solver”，而是：

- 在已有 FDTD / local Maxwell solver 框架内，
- 把粒子运动引起的电荷变化重新组织成一个必然满足离散连续性方程的电流。

## 2. 1 Introduction

### 2.1 引言第一段：作者把问题直接钉在 continuity equation，而不是 field correction

引言开头先说得很明确：作者要引入一个新过程 `density decomposition`，目标是构造出自动满足连续性方程的电流密度。

这里的关注点不是“怎样更准确插值电场”，而是：

- 粒子一旦移动，
- 网格上的电荷密度一定改变，
- 这个改变必须与电流散度完全配平，
- 否则 Maxwell 更新和 Gauss 定律之间就会失配。

### 2.2 引言第二段：为什么 continuity equation 足以替代每步 Poisson correction

作者回顾了标准电磁 PIC 的一个老问题：

- Maxwell 方程里既有双曲型传播方程，
- 又有椭圆型的 Gauss 约束；
- 常见做法是额外解 Poisson 方程修正电场的 potential 部分。

作者的立场是：如果离散连续性方程始终严格成立，那么可以不靠每步解 Poisson 方程来“救场”。

这就把问题从：

- “怎样事后修正 `E`”

转成了：

- “怎样先把 `J` 构造成绝不会破坏 `\partial_t \rho + \nabla \cdot J = 0` 的形式”。

### 2.3 引言第三段：已有局部守恒方法为什么还不够

作者承认，在他之前已经有局部满足连续性方程的方法，但它们主要限制在：

- 零阶 shape；
- 一阶 shape；
- 也就是比较简单的 particle cloud。

本文要解决的核心扩展就是：

- 把这条局部守恒思路推广到更一般的 form-factor；
- 尤其是推广到高阶、可分离的 tensor-product particle shapes。

### 2.4 引言第四段：这篇文章的“硬 claim”不是只有算法，还有唯一性

引言最值得注意的一句不是“推广到更多 shape”，而是作者声称：

- 这个 density decomposition 不是众多任选构造之一，
- 在给定的自然条件下，
- 它是定义粒子相关电流的唯一线性过程。

这条 claim 对 `PIC-tutor` 很重要，因为它把 Esirkepov 路径的地位从：

- “一种常见 charge-conserving trick”

提升成了：

- “在自然线性约束下被唯一挑出来的电流构造方式”。

### 2.5 引言最后两段：本文放在 PIC 历史里的位置

引言最后把文章的生态位讲清楚了：

- 它不是否认已有 Maxwell solver；
- 也不是要替代所有 Gauss-law enforcement；
- 它是专门为不想每步额外做 Poisson correction 的 local PIC/FDTD 路径，提供一个更一般的 charge-conserving current definition。

作者还明确把它和 `Birdsall-Langdon`、`Hockney-Eastwood` 这类 PIC foundations 书籍放在同一历史链条里。这也解释了为什么本项目第 5 章必须把这篇文章与源码和基础教材同时绑定，而不是只靠 WarpX kernel 自己讲话。

## 3. 2 Continuity equation in finite differences

### 3.1 这一节的主任务：把“离散 Maxwell + leapfrog particle mover”压成 continuity equation

这一节不是直接写电流公式，而是先搭出完整离散舞台：

- Maxwell 更新式；
- leapfrog 粒子推进；
- Yee 型 staggered 网格；
- 前向/后向差分算子。

作者的策略是：

1. 先把离散场方程写清楚；
2. 再说明只要离散连续性方程成立，Gauss 定律就能随时间自动保持；
3. 这样电流构造问题就被重新表述成“怎样保证 Eq.(15) 永真”。

#### 离散 Maxwell 更新

$$
\frac { { \bf { E } } ^ { n + 1 } - { \bf { E } } ^ { n } } { d t } = \nabla ^ { + } \times { \bf { B } } ^ { n + 1 / 2 } - \mathcal { J } ^ { n + 1 / 2 }
$$

$$
\frac { { \bf B } ^ { n + 1 / 2 } - { \bf B } ^ { n - 1 / 2 } } { d t } = - \nabla ^ { - } \times { \bf E } ^ { n }
$$

$$
\nabla ^ { - } \cdot \mathbf { E } ^ { n } = \rho ^ { n}
$$

**变量说明：**

- `\mathbf E^n`：整数时刻的电场；
- `\mathbf B^{n+1/2}`：半步时刻的磁场；
- `\mathcal J^{n+1/2}`：沉积到 Yee 网格对应边/面的电流；
- `\nabla^+`：前向差分；
- `\nabla^-`：后向差分。

**物理直觉：**

这里最关键的不是具体归一化，而是：

- `E`、`B`、`\rho`、`J` 不在同一类网格点上；
- 如果 `J` 的离散散度不和 `\rho` 的时间变化精确匹配，
- `\nabla\cdot E = \rho` 很快就会被破坏。

### 3.2 离散差分算子的关键性质：curl-div identity 仍然保留

作者接着定义了 `\nabla^+` 与 `\nabla^-`，并强调：

$$
\nabla ^ - \times \nabla ^ + = \nabla ^ + \times \nabla ^ - = 0
$$

$$
\nabla ^ - \cdot \nabla ^ + = \nabla ^ + \cdot \nabla ^ - = \Delta
$$

**推导过程：**

1. `\nabla^+` 与 `\nabla^-` 是相邻网格上的 forward/backward finite difference；
2. staggered placement 让 curl 后再 div 仍然抵消；
3. 因此对 Ampere 更新取散度时，磁场旋度项自动消失；
4. 剩下的唯一源项就是 `J` 的散度。

**物理直觉：**

这一步的意义是：

- 离散 Maxwell 结构本身并不阻止守恒；
- 真正决定 Gauss-law 能否自动维持的，是你喂给它的 `J` 是否满足离散连续性方程。

### 3.3 由场方程直接推出离散连续性方程

作者从离散 Maxwell 方程推出：

$$
\frac { \rho ^ { n + 1 } - \rho ^ { n } } { d t } + \nabla ^ - \cdot \mathcal { J } ^ { n + 1 / 2 } = 0
$$

这就是后面全文真正要保住的约束。

**推导过程：**

1. 对离散 Ampere 方程取 `\nabla^- \cdot`；
2. 磁场旋度项因 `\nabla^- \cdot (\nabla^+ \times B)=0` 消失；
3. 左边变成 `\nabla^- \cdot E` 的时间差；
4. 再用离散 Gauss 定律 `\nabla^- \cdot E = \rho` 代换；
5. 立刻得到 `\partial_t \rho + \nabla^- \cdot J = 0` 的离散版。

**关键点/物理意义：**

- 如果 `J` 满足这条式子，Gauss 定律会被场推进自动继承；
- 如果 `J` 不满足，后续再做 field correction 只是补救，而不是从源头守恒。

### 3.4 单粒子 charge density 的写法：shape function 是整个问题的起点

作者把总电荷密度写成所有粒子 form-factor 的和：

$$
\rho _ { i , j , k } = \sum _ { \alpha } S _ { i , j , k } ( x _ { \alpha } , y _ { \alpha } , z _ { \alpha } )
$$

并要求单粒子 shape 满足总电荷归一化：

$$
\sum _ { i , j , k } S _ { i , j , k } ( x _ { \alpha } , y _ { \alpha } , z _ { \alpha } ) = 1
$$

**物理直觉：**

这说明在这篇 paper 里，粒子不是点电荷，而是“带形状的 charge cloud”。因此后面所谓 current deposition，并不是单纯给每个 cell 填一个速度，而是要描述：

- 这片 cloud 从旧位置移动到新位置时，
- 每个网格节点上的电荷是如何重分配的。

## 4. 3 Density decomposition

### 4.1 这一节的第一性问题：单粒子移动造成的电荷变化，到底怎样分解成三个方向的电流

由于连续性方程是线性的，作者说只要解决单粒子问题就够了。

然后他引入三个方向的有限差分电流增量：

$$
\mathcal { J } _ { i , j , k } ^ { 1 } - \mathcal { J } _ { i - 1 , j , k } ^ { 1 } = - \frac { d x } { d t } W _ { i , j , k } ^ { 1 }
$$

$$
\mathcal { J } _ { i , j , k } ^ { 2 } - \mathcal { J } _ { i , j - 1 , k } ^ { 2 } = - \frac { d y } { d t } W _ { i , j , k } ^ { 2 }
$$

$$
\mathcal { J } _ { i , j , k } ^ { 3 } - \mathcal { J } _ { i , j , k - 1 } ^ { 3 } = - \frac { d z } { d t } W _ { i , j , k } ^ { 3 }
$$

这里 `W^1, W^2, W^3` 不是最终电流，而是把“电荷变化”分摊到三个方向电流差分上的中间对象。

### 4.2 density decomposition 的主约束：三方向分量加起来必须等于 shape 的总变化

作者随后给出这篇文章的核心式子：

$$
W ^ { 1 } + W ^ { 2 } + W ^ { 3 } = S ( x + \Delta x , y + \Delta y , z + \Delta z ) - S ( x , y , z )
$$

**变量说明：**

- `S(x,y,z)`：旧时刻单粒子 shape；
- `S(x+\Delta x, y+\Delta y, z+\Delta z)`：粒子位移后的 shape；
- `W^1,W^2,W^3`：把这次位移导致的电荷差分拆给三个坐标方向的中间量。

**物理直觉：**

这条式子说的其实很朴素：

- 粒子一动，电荷云的空间分布就变了；
- 这个总变化必须全部被三个方向上的电流通量解释掉；
- 不能多，也不能少。

### 4.3 为什么作者坚持“线性”构造

作者把 `W` 假定为由八个 old/new corner-like shape 值线性组合得到，理由有两条：

1. 粒子云幅值若放大，相关电流也应同比例放大；
2. 一个三维位移可以拆成三个一维位移，电流贡献应可加。

这很关键，因为它限定了允许的算法家族：

- 不是任意非线性拼凑；
- 而是在“线性 + 可加 + 守恒”这组自然条件下找唯一解。

### 4.4 唯一性条件：零位移退化、坐标置换对称性和总差分守恒

作者列出三组自然条件：

1. `W^1+W^2+W^3` 必须精确还原总 shape 差分；
2. 若某个方向位移为零，对应分量必须为零；
3. 若 shape 对坐标置换对称，且 `\Delta x = \Delta y`，则对应 `W^1=W^2`。

在这些条件下，作者声称 density decomposition 是唯一允许的线性形式。

### 4.5 `Eq.(23)` 的地位：不是“一个漂亮公式”，而是唯一性解的显式展开

这次直接从项目内 PDF 抽取第 7 页正文后，`Eq.(23)` 的整体结构已经可以比较可靠地写清。对三个方向，作者给出的显式分解是：

$$
\begin{aligned}
W^1
=&
\frac13 S(x+\Delta x,y+\Delta y,z+\Delta z)
-\frac13 S(x,y+\Delta y,z+\Delta z) \\
&+\frac16 S(x+\Delta x,y,z+\Delta z)
-\frac16 S(x,y,z+\Delta z) \\
&+\frac16 S(x+\Delta x,y+\Delta y,z)
-\frac16 S(x,y+\Delta y,z) \\
&+\frac13 S(x+\Delta x,y,z)
-\frac13 S(x,y,z),
\end{aligned}
$$

$$
\begin{aligned}
W^2
=&
\frac13 S(x+\Delta x,y+\Delta y,z+\Delta z)
-\frac13 S(x+\Delta x,y,z+\Delta z) \\
&+\frac16 S(x,y+\Delta y,z+\Delta z)
-\frac16 S(x,y,z+\Delta z) \\
&+\frac16 S(x+\Delta x,y+\Delta y,z)
-\frac16 S(x+\Delta x,y,z) \\
&+\frac13 S(x,y+\Delta y,z)
-\frac13 S(x,y,z),
\end{aligned}
$$

$$
\begin{aligned}
W^3
=&
\frac13 S(x+\Delta x,y+\Delta y,z+\Delta z)
-\frac13 S(x+\Delta x,y+\Delta y,z) \\
&+\frac16 S(x,y+\Delta y,z+\Delta z)
-\frac16 S(x,y+\Delta y,z) \\
&+\frac16 S(x+\Delta x,y,z+\Delta z)
-\frac16 S(x+\Delta x,y,z) \\
&+\frac13 S(x,y,z+\Delta z)
-\frac13 S(x,y,z).
\end{aligned}
$$

这里最值得第 5 章抓住的不是把八项都背下来，而是两条结构事实：

1. 每个方向的 `W^m` 都只由式 `(21)` 那八个 old/new corner-like shape 值线性组合而成；
2. 系数只出现两种：`1/3` 和 `1/6`。

这说明所谓 `density decomposition` 不是模糊的“把电荷差分拆开”，而是一个被唯一性条件钉死的具体线性组合。更直观地说：

- `1/3` 系数给了“沿目标方向直接发生变化”的那部分 shape；
- `1/6` 系数则把另外两方向的耦合变化平均分摊进来；
- 三个 `W^m` 加总后，刚好恢复总的 shape 差分 `S(x+\Delta x,y+\Delta y,z+\Delta z)-S(x,y,z)`。

对 WarpX 而言，这也是一个很强的 paper-to-source 信号：源码里 `one_third` / `one_sixth` 这组常数并不是实现者随手选的平滑权重，而正是这条唯一线性分解在现代 tensor-product current kernel 里的程序化残影。

如果继续往源码层压一步，这个“程序化残影”其实不是抽象类比，而是能直接落到三组 prefix loop 上。WarpX 的 `3D` Esirkepov kernel 会分别写出：

- `sdxi += (sx_old-sx_new) * yz_mixed_average`；
- `sdyj += (sy_old-sy_new) * xz_mixed_average`；
- `sdzk += (sz_old-sz_new) * xy_mixed_average`。

这里三个 `mixed_average` 的结构，都正好是 `1/3,1/6,1/6,1/3` 的 old/new 双横向组合。于是 `Eq.(23)` 在现代源码里的对应关系可以读成：

1. `W^1` 不再显式叫做 `W^1`，而是变成 `sdxi` 这组 `x` 向 prefix loop 的被加数；
2. `W^2` 对应 `sdyj`；
3. `W^3` 对应 `sdzk`。

也就是说，WarpX 不是先拿到一个总的 `S_{new}-S_{old}` 再事后分流，而是从循环拓扑上就已经把论文要求的唯一三方向分解固定进去了。

### 4.6 inheritance property：为什么 tensor-product shape 特别重要

作者接着要求 form-factor 具有降维继承性，即对某一维求和后还能保持为低一维的 form-factor。

然后他指出，PIC 中最常见、也最实用的一类 shape 正是：

$$
S _ { i , j , k } ^ { 3 D } ( x , y , z ) = S _ { i } ^ { 1 D } ( x ) S _ { j } ^ { 1 D } ( y ) S _ { k } ^ { 1 D } ( z )
$$

**物理直觉：**

这正是现代 PIC 代码最愿意实现的形态，因为：

- 一维权重好算；
- 多维直接取乘积；
- 降维、投影和边界处理也更整洁。

这条性质和 WarpX 的 `ShapeFactors.H` 十分契合。WarpX 的 current deposition 之所以能把 old/new shape 差分拆成一维权重数组再做三维组合，正是因为它默认工作在这种 tensor-product family 里。

## 5. 4 Computing of the current with second-order polynomial form-factor

### 5.1 这一节的目标不是再证明理论，而是把理论压成可编码算法

第 4 节的重要性在于：

- 它不再停留在“存在一个唯一分解”；
- 而是明确告诉你，二阶 spline shape 时，代码里应该按什么步骤算。

作者先给出一维二阶 spline：

$$
S _ { i } ^ { ( 1 D ) } ( x ) = \frac { 3 } { 4 } - ( X _ { i } - x ) ^ { 2 }
$$

$$
S _ { i \pm 1 } ^ { ( 1 D ) } ( x ) = \frac { 1 } { 2 } \left( \frac { 1 } { 2 } \mp ( X _ { i } - x ) \right) ^ { 2 }
$$

这就是常见的 bell-shaped 二阶 spline 粒子云。

### 5.2 算法步骤 1-4：先算 old shape、推进粒子、再算 new shape 和差分

作者给出的前半段算法可以压成四步：

1. 计算旧位置 `(x0,y0,z0)` 对应的一维 shape 数组 `S0`；
2. 用场推进粒子，得到新位置 `(x1,y1,z1)`；
3. 计算新位置的一维 shape 数组 `S1`；
4. 形成差分数组 `DS = S1 - S0`。

这正是今天很多 Esirkepov 实现仍保留的骨架：

- old shape；
- new shape；
- difference；
- 再把 difference 组织成守恒电流。

对 WarpX 而言，这一节最直接的 paper-to-source 对位点就是：

- `Compute_shifted_shape_factor(...)`
- old/new shape arrays 的同框对齐
- 后面沿方向的 prefix-like 累加

### 5.3 步骤 5-7：从差分数组构造 `W`，再积分成三个方向的电流

作者随后把 `W(i,j,k,m)` 写成由 `S0` 与 `DS` 组合出的显式数组，再通过

$$
\mathcal { J } _ { i , j , k } ^ { 1 } - \mathcal { J } _ { i - 1 , j , k } ^ { 1 } = - Q \frac { d x } { d t } W ( i , j , k , 1 )
$$

$$
\mathcal { J } _ { i , j , k } ^ { 2 } - \mathcal { J } _ { i , j - 1 , k } ^ { 2 } = - Q \frac { d y } { d t } W ( i , j , k , 2 )
$$

$$
\mathcal { J } _ { i , j , k } ^ { 3 } - \mathcal { J } _ { i , j , k - 1 } ^ { 3 } = - Q \frac { d z } { d t } W ( i , j , k , 3 )
$$

把它恢复成真实电流分量。

**关键点/物理意义：**

- 这里的核心不是“又定义了一个插值”；
- 而是把 `S1-S0` 的 shape 差分，变成了沿 `x/y/z` 三方向分别闭合守恒的通量。

这也是为什么第 5 章不应把 Esirkepov 简单写成“高阶版本的 `q v S`”：

- 它的第一性对象不是速度加权；
- 而是 shape difference 的守恒分解。

### 5.3.1 这一节和 WarpX 公式最直接的对位点

如果只停在论文记号 `W(i,j,k,m)`，读者还是很难一眼对应到现代源码。对当前 WarpX 来说，更直接的 paper-to-source 映射可以写成：

1. 论文里的 `S0 / S1 / DS`
   - 对应 `sx_old/sx_new`、`sy_old/sy_new`、`sz_old/sz_new` 这三组同框 old/new shape 数组；
   - `Compute_shifted_shape_factor(...)` 的职责正是保证旧 shape 可以在新 shape 的统一索引框架内做差。
2. 论文里的三个中间量 `W(...,1/2/3)`
   - 在现代源码里不再显式保留为一个独立四维数组；
   - 而是直接被吸收到 `Jx/Jy/Jz` 的方向性 prefix-like 累加里。
3. 论文里的

$$
\mathcal { J } _ { i , j , k } ^ { 1 } - \mathcal { J } _ { i - 1 , j , k } ^ { 1 }
= - Q \frac { d x } { d t } W ( i , j , k , 1 )
$$

   - 在 WarpX 中对应成

$$
\Delta J_x
\propto
\sum_{i' \le i}
\left(S_x^{old}(i')-S_x^{new}(i')\right)\,
\overline{S_yS_z},
$$

   - 也就是先沿沉积方向把 shape difference 做前缀累加，再用横向平均闭合三维耦合。

因此，WarpX 当前这条 Esirkepov 路线虽然表面上写成了 `sx_old - sx_new` 与 `one_third/one_sixth` 的显式循环，但它在算法层面仍然是论文第 3、4 节那条逻辑：

- 先把总电荷变化写成 old/new shape difference；
- 再把这个 difference 分配成三个方向的守恒通量；
- 最后让离散散度自动还原 `(\rho^{n+1}-\rho^n)/\Delta t`。

### 5.4 `|\Delta x|, |\Delta y|, |\Delta z|` 不超过一个网格步长的条件

作者在算法步骤里强调粒子单步位移不应超过一个网格步长：

$$
| x_1 - x_0 | \le d x,\quad | y_1 - y_0 | \le d y,\quad | z_1 - z_0 | \le d z
$$

**物理直觉：**

这个条件非常像现代实现里对单步轨迹局部化的要求：

- 若一步跨太远，
- 单个 old/new pair 覆盖的支撑域就会扩得很大，
- 电流构造和局部 stencil 都会更难保持整洁。

在 WarpX 里，这个问题并不总是以论文里的显式条件出现，而是体现在：

- 时间步控制；
- implicit/suborbit 轨迹恢复；
- 以及在别的算法如 Villasenor 中直接做 cell-crossing segmentation。

这里还可以再补一条 paper-level 的实现边界。预印本前文在介绍二维 mover 时明确提醒：实际 simulation 的 timestep 必须满足 Courant condition，因此二维 square mesh 下，单步位移会被限制在小于 `\Delta x/\sqrt{2}` 的量级。Esirkepov 本文在第 4 节把条件写成 `|\Delta x|, |\Delta y|, |\Delta z|` 各自不超过一个网格步长，本质上也是同一类局部化前提：先保证 one-step orbit 不会把单个 old/new support 拉成过宽的非局部对象，再在这个局部轨道上做严格守恒分解。

### 5.5 二维降维版本：为什么第三个电流分量仍然要有定义

作者最后还讨论二维情形：

- 即使变量只依赖 `(x,y)`，
- 也不能简单忘掉第三个电流分量；
- 应从三维链状粒子沿 `z` 方向平均的视角做降维。

这个讨论对 `PIC-tutor` 很有价值，因为它说明：

- reduced dimension 并不等于“随手删掉一个分量”；
- 它需要从原始三维守恒结构严格投影下来。

这和 WarpX 在 `1D_Z / XZ / RZ / RCYLINDER / RSPHERE` 中对各个 `J` 分量采取不同写回合同的逻辑是同一类问题：几何减少了，自由度和守恒关系并没有随意消失。

## 6. 5 Conclusion

结论部分其实非常克制，主要只做了三件事：

1. 重申构造出的 current density 严格满足 charge conservation law；
2. 强调它适用于一大类 form-factor；
3. 给出二阶 polynomial form-factor 的可执行算法。

所以这篇 paper 的真正价值不在花哨 benchmark，而在：

- 给出一个从离散连续性方程反推电流的通用程序；
- 并说明在自然条件下它具有唯一性。

## 7. 与 WarpX / PIC-tutor 的连接

### 7.1 可直接支撑第 5 章的论断

当前这篇预印本已经足以直接支撑第 5 章以下论断：

1. Esirkepov 路径的第一性对象是 old/new shape difference，而不是 direct `q v S`；
2. 守恒条件来自离散连续性方程，而不是后处理修补；
3. tensor-product form factor 是这条方法可以推广到高维的关键；
4. 二阶 spline 情形确实能被压成显式、可编程、局部的 deposition algorithm。

### 7.2 与 WarpX 当前源码的对应点

- `../warpx/Source/Particles/ShapeFactors.H`
  - 一维 shape 的基础定义；
  - 对应论文里的一维 form-factor 与 tensor-product 结构。
- `../warpx/Source/Particles/Deposition/CurrentDeposition.H`
  - `doEsirkepovDepositionShapeN<N>()`
  - old/new shape arrays；
  - 差分和方向累加。
- `../warpx/Source/Particles/WarpXParticleContainer.cpp`
  - `DepositCurrent()` 的 Esirkepov 分派入口。

### 7.3 当前仍未闭环的边界

- 目前拿到的是作者 arXiv 预印本，不是 CPC 出版版最终 PDF；
- `Eq.(23)` 的整体结构和 `1/3, 1/6` 系数现在已经能从项目内 PDF 直接抽取出来，但若要作为最终出版级公式引用，仍应继续对照 PDF 版面把换行和标点再手工校一遍；
- 还没有把这篇 paper 的逐段论证大规模回填到第 5 章主文；
- `Villasenor-Buneman 1992` 现已 materialize，但第 5 章距离“Esirkepov / Villasenor 两条主线都完成 paper-backed 公式级闭环”还差更细的公式誊抄和系统化正文回写。

## 8. 开放问题与个人理解

### 8.1 理论端

- 这篇文章的最硬 claim 是“唯一允许的线性过程”。后续若要在书稿里写得更强，需要把唯一性证明里实际用到的线性方程组和自由度数清楚，而不是只复述结论。
- `Eq.(23)` 现在已经可以稳定复原它的 `1/3, 1/6` 系数组合，但若要写成出版级正文，仍适合再做一次手工誊抄，把三组 `W^m` 的排版和记号统一到本书的符号风格。

### 8.2 数值/实现端

- 论文强调位移不超过单个网格步长；现代 PIC 代码在更复杂几何或 implicit 情况下怎样延伸这条假设，值得和 WarpX 当前 implicit Esirkepov / Villasenor 路径继续对照。
- 论文的算法步骤非常接近“先算 old/new shape，再构造差分”的现代 kernel 骨架，因此特别适合与 WarpX 源码做 paper-to-source mapping。

### 8.3 与 `PIC-tutor` 的连接

- 这篇 paper 已经足以把第 5 章里关于 Esirkepov 的表述，从“只靠源码观察”提升到“有第一手算法论文支撑”。
- 现在更准确的说法应是：
  - Esirkepov：已有 preprint-backed 公式主线，可继续向发表版对照推进；
  - Villasenor：已有 paper-backed 几何/局部通量主线，可继续向逐式展开推进。

## 9. 复习用速记

- Esirkepov 的核心不是 `q v S`，而是把 `S_{new} - S_{old}` 的电荷变化唯一地分解成三个方向的守恒电流。
- 这条方法之所以能推广到高维和高阶 shape，关键在于 tensor-product form-factor 与离散连续性方程的结构配合。

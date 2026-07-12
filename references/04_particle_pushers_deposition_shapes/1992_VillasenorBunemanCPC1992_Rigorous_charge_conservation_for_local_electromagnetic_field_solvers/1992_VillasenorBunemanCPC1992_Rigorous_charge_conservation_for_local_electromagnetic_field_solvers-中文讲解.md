# Villasenor-Buneman 1992 charge-conserving local field solver 笔记

## 0. 论文信息

- 原题：Rigorous charge conservation for local electromagnetic field solvers
- 作者：John Villasenor, Oscar Buneman
- 期刊：Computer Physics Communications
- 年份：1992
- DOI：`10.1016/0010-4655(92)90169-Y`
- 本地 PDF：
  - `1992_VillasenorBunemanCPC1992_Rigorous_charge_conservation_for_local_electromagnetic_field_solvers.pdf`
- MinerU Markdown：
  - `1992_VillasenorBunemanCPC1992_Rigorous_charge_conservation_for_local_electromagnetic_field_solvers.md`
- 所属主题：
  - charge-conserving current deposition
  - local electromagnetic field solver
  - particle mover with boundary-crossing decomposition
- 对 `PIC-tutor` 的用途：
  - 作为第 5 章 Villasenor current deposition 的第一手论文来源；
  - 解释为什么作者强调严格守恒、local update 和 boundary-crossing mover；
  - 给 WarpX 中 Villasenor segment loop、crossing counting 和 tighter stencil 提供历史算法背景。

## 1. 摘要与整体定位

摘要一开头就把这篇文章的核心问题说得很尖锐：作者不是单纯想“算电流”，而是要在二维半和三维电磁 PIC 里，用一种严格满足离散散度方程的方式来更新电场，而且不诉诸代价高的全局变换。

所以这篇 paper 的问题意识和后来的 Esirkepov 并不完全一样：

- 它更早；
- 它更明确地把目标钉在 `local electromagnetic field solver`；
- 它把“严格守恒”直接和“避免 expensive global transforms”绑在一起。

这也解释了为什么它在 `PIC-tutor` 第 5 章中的作用不只是“又一种 charge-conserving formula”，而是：

- Villasenor 这条路径为什么天然带有 local flux / boundary crossing / mover decomposition 的工程组织；
- 以及它为什么在叙述风格上和 Esirkepov 的 old/new shape-difference 路线完全不同。

## 2. 1 Introduction

### 2.1 引言真正针对的不是 Maxwell 方程本身，而是“local update 能否不靠全局 Poisson/FFT 仍保持严格守恒”

作者先回顾了常见做法：

- 场方程常通过 transform/spectral method 求解；
- 这种方法对理解波很自然；
- 但它是 global 的，远处数据也会参与每个 harmonic。

随后作者给出非常工程化的判断：

- 未来计算机更看重 minimization of data paths；
- 因此 field update 越 local 越好；
- 而 Maxwell 的旋度更新式本来就已经是 local 的。

真正麻烦的是散度约束：

$$
\nabla \cdot \mathbf{E} = \rho,
\qquad
\nabla \cdot \mathbf{B} = 0
$$

因为它们看起来需要远处边界条件，从而逼回全局求解。

### 2.2 这篇 paper 的关键转向：只要离散电流满足严格连续性方程，Gauss 定律可以只在初值时 enforced 一次

引言最重要的逻辑是：

1. `\partial_t \mathbf{B} = - \nabla \times \mathbf{E}` 和 `\partial_t \mathbf{E} = \nabla \times \mathbf{B} - \mathbf{J}` 可以用 staggered finite difference 做纯 local update；
2. 若初始时 `\nabla \cdot \mathbf{B} = 0`，之后它会自动保持；
3. 若电流严格满足

$$
\frac{\partial \rho}{\partial t} = - \nabla \cdot \mathbf{J},
$$

那么 `\nabla \cdot \mathbf{E} = \rho` 也会自动保持。

因此作者真正要解决的是：

- finite-difference 版本的 charge conservation law；
- 也就是电流沉积必须和离散 div/curl/time-centering 完全一致。

### 2.3 作者和前人差别的自我定位：关键不在“rigorous”三个字本身，而在“不把一般位移拆成正交 move”

引言后半段回顾了早期做法：

- Buneman 的 zero-order current weighting 会严格守恒，但噪声很大；
- Morse 和 Nielson 的 first-order current weighting 会把一般位移拆成 `\Delta x` 和 `\Delta y` 两个正交 move；
- Marder 的方法允许只是近似满足守恒，并把误差当 pseudo-current 控制。

作者强调：他们的方法和 Morse-Nielson 一样可以 rigorously satisfy continuity equation，但**关键区别**是：

- 他们不把 charge motion 拆成两次正交 move。

这句话直接决定了 `PIC-tutor` 第 5 章应该怎样写 Villasenor：

- 它不是“把 old/new shape 做差”；
- 也不是“随便拆成两个方向分别沉积”；
- 它是围绕真实 boundary crossing 的轨迹几何组织 current flux。

## 3. 2 Calculating the fluxes and currents

### 3.1 基本模型：unit-square charge + area weighting

作者先把二维情形讲得很具体：

- 网格由 unit square cells 构成；
- 粒子也被视作 unit square charge cloud；
- 其电荷均匀分布在方形面积上；
- 每次移动时，真正重要的是这个方形云扫过了哪些 cell boundary。

### 图 1：Particle-in-cell 的几何起点

![Fig.1](images/dd7117ea8f434159385deec1f481f0555234f64f0300e02e7741140016ccf8eb.jpg)

**图像描述：**

这张图把粒子画成一个与 cell 同尺度的方形电荷云，而不是点粒子。网格线把这个方形切进相邻多个 cell。

**物理含义：**

这里的 current deposition 从一开始就不是点粒子穿过单条线的事件，而是一个有限面积电荷云扫过 boundary 的几何通量问题。

**与论文内容的关联：**

这正是后面所有 `four-boundary / seven-boundary / ten-boundary` 分类的基础。

### 3.2 最简单的四边界移动：当前贡献只落在四条 boundary 上

作者先从最常见的情况入手：单步移动只影响四条 boundary。此时电流可以写成四个通量：

$$
J_{x1},\; J_{x2},\; J_{y1},\; J_{y2}.
$$

它们的明确写法是：

$$
J _ { x 1 } = \Delta x \Big ( \frac { 1 } { 2 } - y - \frac { 1 } { 2 } \Delta y \Big )
$$

$$
J _ { x 2 } = \Delta x \Big ( \frac { 1 } { 2 } + y + \frac { 1 } { 2 } \Delta y \Big )
$$

$$
J _ { y 1 } = \Delta y \Big ( \frac { 1 } { 2 } - x - \frac { 1 } { 2 } \Delta x \Big )
$$

$$
J _ { y 2 } = \Delta y \Big ( \frac { 1 } { 2 } + x + \frac { 1 } { 2 } \Delta x \Big )
$$

**变量说明：**

- `x, y`：起始时粒子中心相对 local origin 的坐标；
- `\Delta x, \Delta y`：这一步的位移；
- `J_{x1}, J_{x2}, J_{y1}, J_{y2}`：扫过四条边界的电荷通量。

**物理直觉：**

每个通量都等于：

- 沿该方向的位移深度，
- 乘上该方向边界上被扫过的平均宽度。

所以 Villasenor 路径的第一性对象不是 velocity-weighted shape，而是**boundary flux**。

### 3.2.1 这四个通量为什么已经不是简单的 `q v S`

把上面四个式子并起来看，会更清楚地看到 Villasenor 的结构不是 direct deposition：

$$
J_{x1}+J_{x2}=\Delta x,\qquad
J_{y1}+J_{y2}=\Delta y.
$$

也就是说，沿某个方向的总输运量当然仍等于该方向位移本身；但它怎样分配到上下两条或左右两条 boundary，并不是常数，而是会被

- 起始位置 `x,y`
- 以及耦合位移 `\Delta y,\Delta x`

共同改写。换句话说：

- longitudinal transport 仍受主位移控制；
- 但它落到哪一条局部 boundary、落多少，取决于电荷云的真实几何扫掠。

这正是 Villasenor 和 direct `q v S` 路线最根本的差别。后者先有速度，再用固定 shape 去加权；前者先问的是“这一步真实扫过了哪些边界、每条边界通过多少电荷通量”。

### 3.3 七边界与十边界移动：通过多段 four-boundary move 来处理

一般粒子运动不总是这么简单。若一步位移让粒子云跨过更多网格线，就会出现：

- 七边界情况；
- 十边界情况。

### 图 3：Seven-boundary case

![Fig.3](images/89d5571d3c1e75fa7393088d0c961fa53e961b3c4eb45e19fab492632da736db.jpg)

**图像描述：**

粒子这一步不再只扫过四条边界，而会涉及更多 boundary，因此被拆成两段连续的 four-boundary 子移动。

**关键解读：**

作者不是先做一个整步公式再事后修正，而是直接按真实 crossing 几何把 move 分成两段。

### 图 4：Ten-boundary case

![Fig.4](images/e9b6d8166fb3dc0905f7044663c169f3c93eda279246dd74860d82bcc49a5efa.jpg)

**图像描述：**

最复杂时，一步移动可以影响十条边界，因此要拆成三段 four-boundary 子移动。

**与 WarpX 的关联：**

这和现代 WarpX Villasenor kernel 的 segment loop 非常同构：

- 不是统一对整条 old/new orbit 做一个全局差分；
- 而是遇到 crossing 就继续切段；
- 每段只处理当前局部通量。

也就是说，这篇 1992 论文虽然写法更几何、更手工，但它已经明确展示了 Villasenor 路径的核心组织方式：**boundary-crossing-driven decomposition**。

如果继续往现代 WarpX kernel 对齐，seven-boundary / ten-boundary 其实还对应着一个更具体的问题：这一段运动里，下一条最先被撞到的 mesh boundary 到底是哪一个方向？论文当年是把这些情况拆成手工几何 case；WarpX 今天则直接在代码里比较候选 crossing 谁最早发生。`XZ/RZ` 分支会比较当前 `x`-crossing 和 `z`-crossing 的发生先后，哪个更早，就先用哪个方向截断当前 segment；`3D` 分支则把同样的判据扩成 `x/y/z` 三方向竞争。

因此，今天源码里的逻辑可以直接读成：

- 先为每个方向构造“下一条可能撞到的 crossing”；
- 选最早发生的那个；
- 用它定义当前局部 segment 的终点；
- 然后把剩余轨迹继续送回同一套局部沉积循环。

换句话说，论文里的 seven-boundary / ten-boundary 不再需要作为名字单独保留；它们在现代 WarpX 里已经变成了 repeated earliest-crossing segmentation 的自然结果。

如果再往现代 WarpX kernel 对一步，可以把这层对应说得更精确。论文 four-boundary case 里

$$
J_{x1}+J_{x2}=\Delta x,\qquad J_{y1}+J_{y2}=\Delta y
$$

说明二维 Villasenor 的主方向总输运，本质上还是由该方向位移本身决定；几何真正改写的是“这份输运怎样分到两条局部 boundary 上”。WarpX 当前 `XZ/RZ` Villasenor segment kernel 仍保留这条骨架：`Jx` 和 `Jz` 都写成

$$
\text{directional transport} \times \frac{S_{\mathrm{old}}+S_{\mathrm{new}}}{2} \times \frac{dt_{\mathrm{seg}}}{dt},
$$

也就是：

- 先由 `dx_seg` 或 `dz_seg` 给出该段主输运量；
- 再用横向 old/new node weight 的简单平均决定它落在哪两条局部 boundary 上；
- crossing 一旦变多，就继续拆成多个 obey 同一规则的局部 segment。

这相当于把论文里手工写出的 `J_{x1},J_{x2},J_{y1},J_{y2}`，改写成了现代 `segment + local weights` 版本。

## 4. 3 Field updating

### 4.1 current deposition 和 field update 在这篇 paper 里是一个整体问题

第三节把前面的 flux 直接接回 Maxwell 更新。作者的观点很明确：

- 不需要把 longitudinal `E` 单独拆出来再算；
- 只要 `J` 的有限差分沉积和连续性方程严格一致，
- 更新 `\partial_t E = \nabla \times B - J` 时，longitudinal flux 会自动按 `\rho` 的变化得到正确更新。

这说明 Villasenor 不只是一个粒子 mover 技巧，而是 whole local field solver contract 的一部分。

### 图 5：Staggered field layout

![Fig.5](images/84e13219ce5010a46f9dfc821672632a5f075a5c77e6321a9c77a989cbd87cc1.jpg)

**图像描述：**

图中给出标准 staggered cell：`J` 与 `E` 记录在 cell edge，`B` 在 cell corner，`\rho` 与 `\phi` 在 cell center。

**物理含义：**

这就是 local electromagnetic solver 的离散舞台。Villasenor 方法沉积的并不是抽象 current，而是恰好落在这个 staggered layout 所需要的位置和方向上的边界通量。

### 4.2 self-force 与 area weighting

这一节还强调了 area weighting 对 field interpolation 的意义：

- 若 self-force 不为零，cell center 会形成非物理 potential well；
- area weighting 能消掉这种 self-force。

这说明作者整篇 paper 虽然主轴是 current deposition，但它没有把 deposition 和 gather 完全分离看待，而是把它们当成同一离散系统的一对契约。

## 5. 4 Implementation

实现节有两个最重要的结论。

### 5.1 运行时路径本身就是分支式 mover

实现流程是：

1. 先判断是否为 four-boundary move；
2. 若不是，再检查 seven-boundary；
3. 必要时进入 ten-boundary routine；
4. 所有粒子 current 累积完后，再统一更新 fields。

### 图 6：整体 simulation flow

![Fig.6](images/698d9b007225f16ab0486a734d03260588ad1abb36b0dde11aef1728e2cca534.jpg)

**关键解读：**

这说明“严格守恒”不是一条附加校正，而是 simulation loop 主路径的一部分。

这里还有一条很适合和现代源码一起讲的实现边界：论文在 2D 讨论里直接指出，真实 simulation 的 timestep 还必须满足 Courant condition，因此在 square mesh 上粒子单步位移会自然受限在 `\Delta x / \sqrt{2}` 的量级。这样一来，four/seven/ten-boundary 这套分类才会保持为局部 mover，而不会一口气跨过过多网格线。对比 WarpX，现代代码不再把这条约束写成固定的几何 case table，而是：

- 要么靠 timestep 与 CFL 自然限制单步轨迹长度；
- 要么在更复杂的 implicit / boundary 场景里，直接退回 `cell_crossings -> segment loop` 的程序化分段。

### 5.2 数值验证：新 `\nabla \cdot E` 与按粒子新位置重建的 `\rho` 一致到 roundoff

作者最后做的验证很直接：

- 用 current 更新后的 `E` 去算新的 `\nabla \cdot E`；
- 再拿粒子新位置按 area weighting 重建 `\rho`；
- 二者在 roundoff 范围内一致。

这正是 paper 级的强证据边界：它不是只说“看起来守恒”，而是直接比较离散 Gauss 定律两侧。

## 6. 5 Extension to three dimensions

### 6.1 3D 不是简单把 2D 公式复制一份，而是从 volume weighting 和 face flux 重新组织

三维扩展里，area weighting 变成 volume weighting：

- 粒子是与 cell 同尺度的均匀带电立方体；
- 一般会占据八个相邻 cell；
- 与 2D 一样，真正关键的是它穿过各个 face 的通量。

### 图 8：3D particle-in-cell 几何

![Fig.8](images/ea8c410663b3092ee7c7a64ceece4a1ae64cc9c2672a53572ae82135f66f0d7b.jpg)

**图像描述：**

图中显示带电立方体侵入相邻 cell 的体积分配方式。

**物理含义：**

三维 Villasenor 仍然是“局部几何通量”逻辑，只不过二维的边界面积，变成了三维的 face area 和 volume overlap。

### 6.2 新出现的 `\Delta x \Delta y \Delta z / 12` 交叉项

三维推导里作者特别指出，通量表达式里会出现新的交叉项：

$$
\Delta x \Delta y \Delta z / 12
$$

这很重要，因为它说明：

- 3D 严格守恒不是三个 1D 规则简单并列；
- 多方向耦合会带来额外 correction term；
- 这类项正是 Villasenor 路径“几何局部而不简单”的地方。

### 6.2.1 和 WarpX `segment + local weights` 写法的对应关系

现代 WarpX 不会把这条 3D 逻辑直接写成论文里的几何分类语句，但实现上的等价结构很清楚：

1. 先用 `cell_crossings_x/y/z` 和逐段 endpoint 恢复，把整条轨迹压成多个局部 segment；
2. 对每个 segment 分别计算
   - segment center 上的 cell-based weights；
   - segment 两端上的 node-based old/new weights；
3. 再把该段的局部输运按 `this_Jx/this_Jy/this_Jz` 写回。

这里每个 segment 的 `dt_seg/dt`，以及高阶时

$$
\frac{4S_{\mathrm{bar}} + S_{\mathrm{old}} + S_{\mathrm{new}}}{6}
$$

式的局部修正，本质上都在承担论文中多方向几何耦合和交叉项的现代程序化角色。也就是说，WarpX 没有放弃 Villasenor 论文里的 3D 严格守恒逻辑，只是把它从 `four/seven/ten-boundary` 的手工分类，改写成了更通用的 `crossing-driven segment loop + local weights`。

如果再看源码里的

$$
\texttt{seg\_factor\_x}=dx_{\mathrm{seg}}/dx,\quad
\texttt{seg\_factor\_y}=dy_{\mathrm{seg}}/dy,\quad
\texttt{seg\_factor\_z}=dz_{\mathrm{seg}}/dz,
$$

就能更清楚地看到这层“子移动”语义没有丢。它们不是随手乘上的局部修正，而是当前 segment 在三个方向上分别占整步总位移的比例。换句话说，WarpX 不是把整步通量先算完再切给每一段，而是让每个 segment 只承担自己那一小段真实扫掠所对应的那部分 `Jx/Jy/Jz`。这和论文里 seven-/ten-boundary 把复杂移动拆成若干局部 four-boundary 子移动，物理意义是同一件事。

再往下看 `3D` kernel 里的 `one_third/one_sixth`，就能把它和论文里的 `\Delta x \Delta y \Delta z / 12` 再对上一层。要点不是说源码里“逐字写着同一个单项式”，而是说它保留了同一种三维 mixed-direction coupling：每个方向的 `this_Jx/this_Jy/this_Jz` 都不是只看本方向位移，而是还要把另外两个方向的 old/new node weights 按

$$
\frac13,\;\frac16,\;\frac16,\;\frac13
$$

做混合平均。这样做的作用，就是把论文里 3D 通量里那类“不能拆成三个互不相干 1D 贡献”的交叉耦合，用现代 tensor-product 局部平均的形式保存下来。也就是说，`one_third/one_sixth` 在 Villasenor 3D 路径里承担的，并不只是横向平滑，而是 3D 局部守恒耦合本身。

这里还有一条维度差异值得单独记住。WarpX 并不是在所有几何里都用完全同一套局部平均：

- 在 `XZ/RZ` kernel 中，in-plane 的 `Jx/Jz` 只面对一个横向方向，因此退化成 `(S_{old}+S_{new})/2` 的简单平均；
- 只有 out-of-plane 的 `Jy`，以及 `3D` 中每个方向的 `Jx/Jy/Jz`，才需要完整的 `1/3,1/6` tensor-product 平均。

这说明 Villasenor 的现代实现不是机械地把一套 3D 公式到处照搬，而是仍然忠实地保持了论文原本的几何层次：二维先是 “one directional flux split across two boundaries”，三维再进一步进入真正的双横向耦合。

### 图 9：Complementary mesh boundary crossings

![Fig.9](images/a67a6601a032efd9d7bacf818db49194c0a1467fb47462355044f8a07038db21.jpg)

**图像描述：**

作者用 complementary mesh 来组织粒子是否离开当前局部网格单元，并据此决定如何继续做 particle splitting。

**与 WarpX 的关联：**

WarpX 里的 Villasenor kernel虽然写法现代化得多，但核心思想仍然非常相近：

- 判断 crossing；
- 若 crossing 发生，则继续局部拆段；
- 让每段通量在当前局部 stencil 内闭合。

这也是 `Villasenor results in a tighter stencil` 这类现代总结真正的历史来源。

## 7. 6 Conclusions

结论部分很克制，核心就三点：

1. 这套方法允许 purely local electromagnetic field update；
2. 离散连续性方程被严格满足；
3. 二维与三维都可以做到，而且代价可控。

所以这篇 paper 的地位应该写成：

- 它不是只给了一个“沉积公式”；
- 它给的是一整套 local field solver + charge-conserving mover 的组织方式。

## 8. 与 WarpX / PIC-tutor 的连接

### 8.1 可直接支撑第 5 章的论断

这篇论文已经足够直接支撑第 5 章以下判断：

1. Villasenor 路径的第一性对象是 boundary-crossing-driven flux decomposition；
2. 它和 Esirkepov 的 old/new shape-difference 结构是两种不同的守恒组织方式；
3. 它天然更接近 segment/face-local 的 tighter stencil 叙述；
4. reduced geometry / 3D extension 都不是“删分量”或“复制公式”，而是从同一局部几何守恒逻辑投影而来。

### 8.2 与 WarpX 当前源码的对应点

- `../warpx/Source/Particles/Deposition/CurrentDeposition.H`
  - Villasenor explicit/implicit 入口；
  - crossing counting；
  - segment-wise deposition；
  - 局部 `this_J*` 写回。
- `../warpx/Source/Particles/WarpXParticleContainer.cpp`
  - Villasenor 的 explicit/implicit dispatch；
  - collocated/shared-memory 限制。
- `notes/code-reading/particles/42-villasenor-segment-loop-and-esirkepov-contrast.md`
  - 可直接作为本论文的源码对照读物。

### 8.3 当前仍未闭环的边界

- 目前这份中文讲解还是第一轮结构精读；
- 四/七/十边界电流公式和三维 `\Delta x \Delta y \Delta z / 12` 项还值得进一步逐式压实；
- 还没有把这些 paper-backed 论断大规模回填进第 5 章的 Villasenor 段落；
- Esirkepov 与 Villasenor 这两篇虽然现在都已经 materialize，但第 5 章距离“论文-源码-测试三线闭环”还差系统化的正文回写。

## 9. 开放问题与个人理解

### 9.1 理论端

- 这篇 paper 把 local field solver 和 charge-conserving mover 绑得很紧，因此后续写书时不能只摘 current deposition 公式而丢掉场更新语境。
- 它强调“不把一般位移拆成正交 move”，这条历史动机需要在第 5 章里被更明显地写出来。

### 9.2 数值/实现端

- 论文是以 four/seven/ten boundary mover 的几何分类来组织代码；现代 WarpX 则把这套想法更抽象地压成 crossing-driven segment loop。两者之间很适合做一次更细的 paper-to-source 映射。
- 3D 补项说明 tighter stencil 不是“更简单”，而是“更局部但仍保留必要的多方向耦合修正”。

### 9.3 与 `PIC-tutor` 的连接

- 现在第 5 章不再需要把 Villasenor 写成“只有源码、没有论文”的路线；
- 但下一步真正高价值的工作不是再建目录，而是把本论文和 `Esirkepov 2001` 一起回写成第 5 章 paper-backed 的主叙述。

## 10. 复习用速记

- Villasenor 的核心不是 old/new shape-difference，而是按真实 boundary crossing 把 charge motion 分解成局部 face flux。
- 这条路径服务的是严格守恒的 local electromagnetic field solver，因此它天然更像 segment/flux decomposition，而不是一次性整轨迹差分。

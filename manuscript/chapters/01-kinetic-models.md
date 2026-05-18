# 1. 动理学模型与 PIC 的基本思想

PIC 代码不是先有“粒子数组”和“场数组”，再去给它们找物理意义。它的上游模型是动理学方程：对每个物种，真实对象首先是相空间分布函数

$$
f_s(\mathbf{x},\mathbf{p},t),
$$

而不是单个粒子轨道。本章的任务是把这条连续模型主线压实到后面源码会反复用到的几个边界：

1. Vlasov 方程本质上是相空间守恒定律，而不只是“一个偏微分方程”。
2. Vlasov-Maxwell 与 Vlasov-Poisson 不是两套无关模型，而是同一条自洽场闭合在不同物理极限下的分支。
3. 宏粒子、权重和 shape factor 不是数值技巧附会到物理上，而是 coarse-grained kinetic model 的一部分。
4. PIC 的主要误差不是单一来源，而是采样噪声、有限粒子权重、有限网格和离散时间层共同作用的结果。

本章当前主要回链到：

- `Birdsall 1985`
- `Dawson 1983`
- 本地已读的 `WarpX` 主循环与沉积/场求解章节

其中 `Hockney-Eastwood` 与 `Yee 1966` 仍在 acquisition 阶段，当前不拿它们的未核实细节当正文证据。

## 1.1 Vlasov 方程首先是相空间守恒律

对物种 \(s\)，若忽略碰撞、衰变、电离和其他 source/sink，分布函数满足无碰撞相对论 Vlasov 方程

$$
\frac{\partial f_s}{\partial t}
+ \dot{\mathbf{x}}\cdot\nabla_{\mathbf{x}} f_s
+ \dot{\mathbf{p}}\cdot\nabla_{\mathbf{p}} f_s
=0.
$$

对带电粒子，

$$
\dot{\mathbf{x}}=\mathbf{v},
\qquad
\dot{\mathbf{p}}=q_s\left(\mathbf{E}+\mathbf{v}\times\mathbf{B}\right),
$$

因此可写成更常见的形式

$$
\frac{\partial f_s}{\partial t}
+ \mathbf{v}\cdot\nabla_{\mathbf{x}} f_s
+ q_s\left(\mathbf{E}+\mathbf{v}\times\mathbf{B}\right)\cdot\nabla_{\mathbf{p}} f_s
=0.
$$

这里真正需要记住的不是式子本身，而是它的守恒含义。把相空间速度记成

$$
\mathbf{Z}=(\mathbf{x},\mathbf{p}),
\qquad
\dot{\mathbf{Z}}=(\dot{\mathbf{x}},\dot{\mathbf{p}}),
$$

则 Vlasov 方程也可写成

$$
\frac{\partial f_s}{\partial t}+\nabla_{\mathbf Z}\cdot\left(f_s\dot{\mathbf Z}\right)=0.
$$

若相空间流满足

$$
\nabla_{\mathbf Z}\cdot\dot{\mathbf Z}=0,
$$

就得到 Liouville 图像：沿特征线传播时，分布函数值保持不变，相空间体积也不被压缩或膨胀。对后面的 PIC 来说，这一点比公式本身更基础，因为它解释了为什么：

- 粒子推进器不能随意破坏轨道拓扑；
- 离散时间推进若不尊重相空间结构，就会把数值伪耗散或伪加热写进分布函数；
- `Boris / Vay / Higuera-Cary` 这类 pusher 的比较，不只是在比轨道误差，而是在比它们怎样离散化相空间流。

## 1.2 碰撞项不是 Vlasov 的一部分，但必须保留边界

一旦考虑碰撞、衰变、外部源项或粒子数变化，更一般的 kinetic equation 应写成

$$
\frac{\partial f_s}{\partial t}
+ \mathbf{v}\cdot\nabla_{\mathbf{x}} f_s
+ q_s\left(\mathbf{E}+\mathbf{v}\times\mathbf{B}\right)\cdot\nabla_{\mathbf{p}} f_s
= C_s[f] + S_s - L_s.
$$

这里：

- \(C_s[f]\) 表示碰撞算子，可以是 Boltzmann、Landau、Fokker-Planck 或 Monte-Carlo 近似；
- \(S_s\) 表示外加源项，如电离生成、注入、衰变产物；
- \(L_s\) 表示损失项，如吸收、衰变消失、边界流出。

这条边界在 WarpX 里很重要，因为：

- 主 PIC loop 默认走的是无碰撞 Vlasov-Maxwell 主线；
- `CollisionHandler`、`field ionization`、`QED`、`ContinuousFluxInjection`、粒子边界吸收/反射，都是往这条无碰撞主线上附加 `C/S/L`；
- 它们不该被写成“另一个独立程序”，而应被理解成对同一 kinetic balance 的修改。

因此本书后面凡是讲 collisions、ionization、QED、scraping，都应问两个问题：

1. 它改的是分布函数右端的哪一项？
2. 它是在一个时间步的哪个时间层插入进去？

否则很容易把“物理过程存在”和“离散时间组织正确”混成一件事。

## 1.3 Vlasov-Maxwell：源项、约束与闭合

相对论动量与速度满足

$$
\mathbf{p}=\gamma m_s \mathbf{v},
\qquad
\gamma=\sqrt{1+\frac{|\mathbf{p}|^2}{m_s^2c^2}},
\qquad
\mathbf{v}=\frac{\mathbf{p}}{\gamma m_s}.
$$

分布函数的低阶矩给出 Maxwell 方程右端的源项：

$$
\rho(\mathbf{x},t)=\sum_s q_s\int f_s(\mathbf{x},\mathbf{p},t)\,d\mathbf{p},
$$

$$
\mathbf{J}(\mathbf{x},t)=\sum_s q_s\int \mathbf{v}(\mathbf{p})f_s(\mathbf{x},\mathbf{p},t)\,d\mathbf{p}.
$$

然后场满足

$$
\nabla\cdot\mathbf{E}=\frac{\rho}{\epsilon_0},
\qquad
\nabla\cdot\mathbf{B}=0,
$$

$$
\nabla\times\mathbf{E}=-\frac{\partial\mathbf{B}}{\partial t},
\qquad
\nabla\times\mathbf{B}=\mu_0\mathbf{J}+\frac{1}{c^2}\frac{\partial\mathbf{E}}{\partial t}.
$$

这四式里最容易被误写的是：Gauss 定律和 `div B = 0` 不是“额外条件”，而是系统闭合的一部分。只要连续性方程

$$
\frac{\partial \rho}{\partial t}+\nabla\cdot\mathbf{J}=0
$$

成立，并且初值满足约束方程，Maxwell 演化就会传播这些约束。反过来，如果离散沉积和离散场推进不一致，那么程序里最先坏掉的往往不是 curl 更新，而是：

- `divE-rho/epsilon0`
- `divB`
- 边界附近的伪电荷
- 以及随之而来的非物理电场和数值加热

这正是后面第 5 章和第 6 章为什么要反复围着 source synchronization、current correction、Gauss-law regression 打转。

## 1.4 Vlasov-Maxwell 的能量与动量守恒边界

在闭域、无外源、忽略边界通量时，连续系统满足总能量守恒：

$$
\frac{d}{dt}
\left[
\sum_s \int \gamma m_sc^2 f_s\,d\mathbf{x}\,d\mathbf{p}
+ \int \left(\frac{\epsilon_0}{2}|\mathbf{E}|^2+\frac{1}{2\mu_0}|\mathbf{B}|^2\right)d\mathbf{x}
\right]
=0.
$$

它说明两件事：

1. 粒子动能和场能不是分开各自守恒，而是可以相互交换。
2. 程序里若只监控粒子能量或只监控场能量，都不足以判断离散系统是否健康。

同理，总动量守恒应理解为“粒子动量 + 电磁场动量 + 边界 Maxwell stress”一起守恒，而不是单看粒子束团动量曲线。对后面的 implicit、hybrid、electrostatic sphere、planar pinch 和 FEL 例子，这个边界都非常关键：很多 regression 真正检查的是完整能量账本，而不是某个单独变量“看起来没漂”。

## 1.5 Vlasov-Poisson / electrostatic 极限不是另一套世界

当系统关注的是电荷分离和纵向静电响应，而电磁波传播、辐射和横向磁反馈不是主导效应时，可以把自洽场闭合约化到 Vlasov-Poisson：

$$
\frac{\partial f_s}{\partial t}
+ \mathbf{v}\cdot\nabla_{\mathbf{x}} f_s
+ q_s\mathbf{E}\cdot\nabla_{\mathbf{p}} f_s
=0,
$$

$$
\mathbf{E}=-\nabla\phi,
\qquad
-\nabla^2\phi=\frac{\rho}{\epsilon_0}.
$$

它不是凭空把 Maxwell 方程换掉，而是对应这样一组物理假设：

- transverse electromagnetic radiation 不是主要自由度；
- 场主要由电荷分离决定；
- 电磁传播时间尺度不是当前主导尺度；
- 所关心的现象更接近 Langmuir、space-charge、electrostatic expansion、Poisson boundary-value problem。

因此：

- electrostatic PIC 仍然是 kinetic PIC；
- 只是“粒子如何给场提供源项、场如何回馈粒子”这一闭合从 Maxwell 变成了 Poisson。

这也是为什么：

- 第 6 章不能把 electrostatic solver 当作“Maxwell solver 的低配版”；
- electrostatic sphere、Pierce diode、effective potential 这些例子要和 Poisson 边界条件、势能账本一起讲；
- `WarpX::OneStep()` 里 electrostatic / hybrid 路线的场解位置会和标准 electromagnetic loop 不同。

## 1.6 宏粒子不是假粒子，而是 coarse-grained 分布函数载体

PIC 的核心近似不是把等离子体变成少数真实粒子，而是用有限数量的宏粒子采样分布函数。形式上可写成

$$
f_s(\mathbf{x},\mathbf{p},t)
\approx
\sum_{p\in s} w_p
S_x(\mathbf{x}-\mathbf{x}_p(t))
S_p(\mathbf{p}-\mathbf{p}_p(t)).
$$

这里：

- \(w_p\) 是宏粒子权重；
- \(S_x\) 是空间形函数；
- \(S_p\) 常在实际 PIC 中退化成粒子自身在动量空间的离散采样。

从 `Dawson 1983` 的角度，更准确的说法是：宏粒子不是“把许多真实粒子团成一个球”的形象化故事，而是 coarse-grained kinetic model 的载体。它的目标是：

1. 用有限自由度代表连续分布；
2. 保住真正重要的低阶矩和 collective behavior；
3. 接受某些细粒度 phase-space 结构会被采样误差和 coarse graining 吞掉。

## 1.7 权重可以不同，但不是没有代价

宏粒子并不必然等权。`Dawson 1983` 讨论了

$$
q_i=-\alpha_i e,\qquad
m_i=\alpha_i m,\qquad
\frac{q_i}{m_i}=-\frac{e}{m}
$$

这一类不同电荷和质量、但相同荷质比的电子群，并说明由它们组成的加权分布函数仍满足通常的 Vlasov 方程。

这条结论的意义是：

- weighted macroparticles 从一开始就是合法的 kinetic coarse graining；
- 它允许把 phase-space 分辨率集中到真正需要的区域；
- 但它也会引入新的统计与 collisional side effects。

所以“加权宏粒子”更准确的理解不是“自适应采样免费升级”，而是：

- 你获得了 phase-space resolution redistribution；
- 但要付出更复杂的噪声、散射和统计解释代价。

这条边界对后面理解 WarpX 中：

- species 权重
- Gaussian beam / flux injection
- collision/QED product creation
- reduced-dimension weighting compensation

都很重要。

## 1.8 shape factor 不是插值细节，而是粒子-网格合同

若把粒子源项沉积到网格单元或网格点 \(i\)，最基本的电荷密度形式是

$$
\rho_i^n
=
\frac{1}{\Delta V_i}\sum_p q_p w_p S_i(\mathbf{x}_p^n).
$$

场 gather 则用同一类 shape family 从网格插值回粒子位置：

$$
\mathbf{E}_p^n=\sum_i S_i(\mathbf{x}_p^n)\mathbf{E}_i^n,
\qquad
\mathbf{B}_p^n=\sum_i S_i(\mathbf{x}_p^n)\mathbf{B}_i^n.
$$

但 `shape factor` 的意义远不止“双向插值”：

1. 它定义了宏粒子在空间上的 coarse-grained 电荷云。
2. 它决定了粒子-网格耦合的 stencil 宽度。
3. 它会系统改写短波 aliasing、self-force 和统计噪声。
4. 它直接影响 guard-cell 需求、通信宽度和算子局域性。

`Birdsall 1985` 与 `Dawson 1983` 的共同结论都指向这一点：finite-size particles 不是为了把图画得更平滑，而是为了软化 point-charge 的短程奇异作用、压低非物理 collisionality，并把系统真正保留成“长程 collective physics + 可控短程误差”。

这也是为什么后面的第 5 章必须把：

- shape factor
- charge/current deposition
- sampled density
- finite-grid effects
- aliasing

放在同一章里讲，而不是把 shape factor 单独缩成一个插值小节。

## 1.9 PIC 的噪声不是 bug，而是模型代价

把连续分布函数换成有限宏粒子之后，最基本的代价就是采样噪声。它不是代码写坏了才出现，而是：

- 有限粒子数
- 有限权重
- 有限网格
- 有限时间平均

共同带来的统计涨落。

从 `Birdsall 1985` 的 thermal-plasma 讨论看，这种噪声不能只被理解成“粒子数不够大”。更准确的图像是：

1. sampled density 会生成 alias branches；
2. shape factor 会修改 fluctuation spectrum；
3. finite `\Delta x` 和 finite `\Delta t` 会把 continuum 改写成带离散谱结构和 effective transport 的系统；
4. 若离散合同处理不好，噪声会演化成 numerical heating、drag、diffusion，甚至弱不稳定增长率的误判。

因此，本书后面凡是说“噪声更小”“结果更平滑”，都不应只停在图像层，而应继续问：

- 是 modal fluctuation level 变了？
- 是 alias branch 被压了？
- 还是只把可见图像平滑了，但守恒与统计量并没有更好？

## 1.10 Debye 长度、粒子数与统计时间尺度

`Birdsall 1985` 对 sheet model 的讨论给了一个比教科书定义更适合写进程序书的视角。

首先，Debye 长度 \(\lambda_D\) 和 Debye 球内粒子数 \(N_D\) 不是孤立的公式，而是“这个 plasma 是否能被当作 collective medium”与“统计噪声会以什么尺度渗入观测量”的共同边界。

其次，在 reduced model 下，

$$
\tau \sim \frac{2N_D}{\omega_p}
$$

更适合被理解成：

- randomization time
- correlation time
- 统计独立采样间隔

而不是整个分布完全热化成 Maxwellian 的总弛豫时间。后者通常更慢，量级更接近 \(N_D^2\)。

对 PIC 用户来说，这比“记住 Debye 长度定义”更实用，因为它直接影响：

- uniform-plasma 噪声底怎么看；
- reduced diagnostics 应平均多久；
- 弱效应、弱不稳定和 Landau damping 的 measurement window 多大才可信。

## 1.11 这一章对后面源码章节的真正约束

到这里，后续读 WarpX 代码时至少要带着下面这些硬问题，而不是只盯函数名：

1. 粒子推进器是否在离散时间层上合理近似了 Liouville 流？
2. 沉积算法是否把连续性方程离散闭合到了 `rho/J`？
3. field solver 处理的是 Maxwell 还是 Poisson，约束方程怎样传播？
4. shape factor 和 finite-size particles 是如何改写噪声、aliasing 和 self-force 的？
5. diagnostics 到底在测真实物理量，还是只在看离散噪声底的一个投影？

如果没有这几层边界，后面源码里的：

- `OneStep_nosub`
- `PushParticlesandDeposit`
- `SyncCurrentAndRho`
- `PushPSATD`
- `ElectrostaticSolver`
- `ImplicitSolver`

都会被读成“工程控制流”，而不是“连续模型的离散化实现”。

## 1.12 本章当前文献边界

本章当前正文已真正依托的文献边界是：

- `Birdsall 1985`
  - 已精读并回填：
    - sheet model 的 randomization / correlation / thermalization 时间尺度
    - finite-grid / aliasing / fluctuation / heating 主线
- `Dawson 1983`
  - 已精读并回填：
    - numerical experiment 视角
    - superparticle / weighted particles 的 kinetic 边界
    - finite-size particles + grid + FFT-Poisson 的标准 electrostatic contract

仍未在本章直接依赖其正文细节的文献是：

- `Hockney-Eastwood`
  - acquisition 尚未完成
- `Yee 1966`
  - acquisition 尚未完成

基础章节当前允许直接作为正文证据、以及哪些条目仍只能写成 acquisition / metadata 边界，现统一收口到：

- [基础章节文献清单](/Volumes/PHILIPS/programs/PIC/PIC-tutor/docs/foundations-literature-list.md)

因此本章当前版本已经足够支撑后续源码阅读，但基础文献层仍不是最终完成态。后续还需要继续：

1. 补 `Hockney-Eastwood` 或其 article-level fallback 对 weighted particles / heating estimates / optimum path 的原始证据；
2. 补 `Yee 1966` 对 staggered FDTD 与离散约束传播的原始文献入口；
3. 再把本章和第 2 章之间关于 leapfrog、CFL、Debye 长度、数值色散的边界继续压紧。

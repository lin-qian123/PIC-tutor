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

**本章的读者路线**

不要把本章当作术语表。先在 1.1--1.4 固定连续对象：什么量在相空间中守恒、哪些矩成为场的 source、能量和动量何时可以交换；再在 1.5 判断问题是否真的允许采用静电近似；随后在 1.6--1.10 判断宏粒子、权重、shape、网格和时间平均会怎样改变可见的统计量；最后用 1.11--1.14 把这些连续对象交给第 2 章的离散时间步。每经过一段，都应能回答三件事：程序实际表示什么、与哪一个连续量比较、该比较还不能保证什么。

本章的阅读支点是：

- `Birdsall 1985`
- `Dawson 1983`
- 第 2、3、5、6 章对 WarpX 主循环、沉积和场求解器的实现说明

`Hockney-Eastwood` 与 `Yee 1966` 在本书中只作为补充书目信息，而不作为可逐页核对的全文依据；本章不把无法核实的历史细节当作结论。读者应先把这里的连续模型、离散变量和误差边界读清，再进入源码章节。

## 1.1 Vlasov 方程首先是相空间守恒律

对物种 \(s\)，若忽略碰撞、衰变、电离和其他 source/sink，分布函数满足无碰撞相对论 Vlasov 方程

$$
\frac{\partial f_s}{\partial t}
+ \dot{\mathbf{x}}\cdot\nabla_{\mathbf{x}} f_s
+ \dot{\mathbf{p}}\cdot\nabla_{\mathbf{p}} f_s
=0.
$$

这里采用的归一化是

$$
dN_s=f_s(\mathbf{x},\mathbf{p},t)\,d\mathbf{x}\,d\mathbf{p},
\qquad
n_s(\mathbf{x},t)=\int f_s(\mathbf{x},\mathbf{p},t)\,d\mathbf{p}.
$$

因此，\(f_s\) 不是“某个粒子的概率标签”：它是对一个相空间体元内物种数目的密度。后面用粒子样本近似它时，必须同时说明粒子位置、动量、权重和 shape；只写出一条轨道不能定义 \(f_s\)。

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

同理，总动量守恒应理解为“粒子动量 + 电磁场动量 + 边界 Maxwell stress”一起守恒，而不是单看粒子束团动量曲线。对后面的 implicit、hybrid、electrostatic sphere、planar pinch 和 FEL 例子，这个边界都非常关键：自动化案例即使检查完整能量账本，也不能由某个单独变量“看起来没漂”来替代。

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

这是一项建模假设，不是看到某一帧电场主要沿一个方向后再补上的解释。WarpX 的 `warpx.do_electrostatic` 参数说明也明确指出：该模式不在每一步用完整 Maxwell 方程更新场，传播的电磁辐射和激光等效应不被捕获。因此，若研究目标包含传播、辐射、激光注入或横向电磁反馈，就不能用“当前图像看起来近静电”替代模型适用性的论证。

这也是为什么：

- 第 6 章不能把 electrostatic solver 当作“Maxwell solver 的低配版”；
- electrostatic sphere、Pierce diode、effective potential 这些例子要和 Poisson 边界条件、势能账本一起讲；
- `WarpX::OneStep()` 里 electrostatic / hybrid 路线的场解位置会和标准 electromagnetic loop 不同。

### 1.5.1 模型选择与验证卡：Poisson 可解不等于完整电磁问题已被解决

选择 electrostatic 路线时，先把“模型是否适合”与“这一实现是否通过指定验证”分开。下面的四层顺序可防止把一个收敛的 Poisson solve、一次通过的回归或一幅近纵向电场图误读成完整的 Vlasov--Maxwell 验证。

**第一层：先判断问题是否仍需传播电磁自由度。** 若研究对象包含激光注入、辐射传播、波的有限传播时间、横向电磁反馈或与 PML 吸收有关的反射，`warpx.do_electrostatic` 不是近似程度较高的快捷路径，而是模型对象已经变了；应回到完整 electromagnetic 路线。反之，若目标是给定边界势下的空间电荷、静电平衡或 Poisson 边值问题，才继续问 Poisson 解和边界条件是否与目标相符。参数文档的“没有 timestep 限制”只是在说该模式不由 electromagnetic CFL 限制；它既不免除粒子输运、等离子体频率、统计采样或 Poisson 误差的判断，也不授权把过大的步长写成物理上准确。

**第二层：明确实际解的是什么。** `labframe` 以所有物种合成的 \(\rho\) 解

$$
\nabla^2\phi=-\rho/\epsilon_0,
\qquad \mathbf{E}=-\nabla\phi.
$$

`labframe-electromagnetostatic` 还以合成的 \(\mathbf{J}\) 解矢势并构造静磁场；`labframe-effective-potential` 则改写 Poisson 算子以改变大 \(\omega_{pe}\Delta t\) 时的数值行为。它们不是同一个开关的三个拼写。读者若只需 electrostatic 的 \(\phi,\mathbf{E}\)，不能因为输出里出现了 \(B\) 或因为某个模式能稳定运行，就跳过所选模式的方程和适用假设。

**第三层：用一个有解析 reference 的 producer 检查指定对象。** 官方 `test_3d_electrostatic_sphere_eb` 是启用 EB 时的 3D、2-rank 案例：`max_step = 1`、`warpx.do_electrostatic = labframe`、外边界为零电势的 PEC，半径 \(R=0.1\,\mathrm{m}\) 的 embedded sphere 固定为 \(\phi_0=1\,\mathrm{V}\)。它写出 `Ex/Ey/Ez/rho/phi/eb_covered` 的 Full diagnostics，并另写 `ChargeOnEB` 的全球与八分之一球积分。这里的 producer 很窄：它构造的是给定导体势、特定几何、单步、无传播辐射主张的 Poisson/EB 问题，而不是一般带粒子动力学的 plasma benchmark。

**第四层：让 consumer 与所问问题一一对应。** 该案例的 `analysis.py` 比较全嵌入边界电荷

$$
Q_{\mathrm{th}}=4\pi\epsilon_0\phi_0R
$$

与 `eb_charge.txt` 中的数值积分，并要求相对误差小于 `0.06`；它还把八分之一权重积分与 \(Q_{\mathrm{th}}/8\) 比较，并检查 `eb_covered` 在 \([0,1]\) 内、球内带与球外带分别为 1 与 0。这三类断言分别约束全局边界电荷、加权表面积分和 EB 几何 mask。CTest 随后的 checksum 只回归指定输出基线，不能替代前三个比较。

从执行次序看，初始化阶段和每个 electrostatic 时间步都会经 `ComputeSpaceChargeField()` 组织 Poisson 场；进入该分支后，演化代码会重置 electrostatic 分量，再在粒子下一次 push 前准备可 gather 的场。与此同时，`OneStep_sub1()` 明确拒绝 electrostatic solver 与 AMR subcycling 的组合。因此下面的句子都不成立：**“Poisson 残差小，所以激光传播也正确”、“sphere 的电荷通过，所以任意 EB 几何的场都正确”、“没有 electromagnetic CFL，所以时间步不再需要物理判断”**，以及“这张单步、固定势测试证明了 electrostatic + subcycling 的路径”。

这张卡的实际交付是一张四行表：模型中保留/删去的自由度、输入 producer、各 consumer 的 reference 与阈值、以及本次结论不能外推的范围。这样才把第 1 章的连续假设接到后续第 3A 章初始化、第 6 章场求解和第 7 章 EB/PML 的不同问题上。

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

## 1.8 shape factor 不是插值细节，而是粒子-网格耦合规则

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
3. finite \(\Delta x\) 和 finite \(\Delta t\) 会把 continuum 改写成带离散谱结构和 effective transport 的系统；
4. 若离散耦合处理不好，噪声会演化成 numerical heating、drag、diffusion，甚至弱不稳定增长率的误判。

因此，本书后面凡是说“噪声更小”“结果更平滑”，都不应只停在图像层，而应继续问：

- 是 modal fluctuation level 变了？
- 是 alias branch 被压了？
- 还是只把可见图像平滑了，但守恒与统计量并没有更好？

## 1.10 Debye 长度、粒子数与统计时间尺度

`Birdsall 1985` 对 sheet model 的讨论给了一个比教科书定义更适合写进程序书的视角。

首先，在线性、近 Maxwellian 的三维等离子体中，热速率 \(v_t\)、等离子体频率和 Debye 长度可写为

$$
v_t=\sqrt{\frac{k_B T_s}{m_s}},
\qquad
\omega_{ps}=\sqrt{\frac{n_s q_s^2}{\epsilon_0m_s}},
\qquad
\lambda_{Ds}=\frac{v_t}{\omega_{ps}}
=\sqrt{\frac{\epsilon_0 k_B T_s}{n_s q_s^2}}.
$$

其中 \(n_s\) 是物种数密度，\(T_s\) 是温度，\(k_B\) 是 Boltzmann 常数。对应的 Debye 球内粒子数近似为

$$
N_D\sim (4\pi/3)n_s\lambda_{Ds}^3.
$$

这些量的精确定义会随单位制、速度矩约定、磁化程度和 reduced geometry 改变；这里使用它们是为了建立尺度判断，而不是把二维或轴对称计算机械地当成三维 Debye 球。Debye 长度 \(\lambda_D\) 和 Debye 球内粒子数 \(N_D\) 因而不是孤立的公式，而是“这个 plasma 是否能被当作 collective medium”与“统计噪声会以什么尺度渗入观测量”的共同边界。

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

## 1.11 从连续模型到 PIC 离散变量

前面的方程还没有直接变成程序里的数组。PIC 的第一步不是把分布函数存成一个高维网格，而是用带权粒子样本代表它，再用网格上的有限差分或谱变量承载场。可以把这条映射写成下面的最小对应关系：

| 连续对象 | PIC 离散载体 | 典型时间层/位置 | 在 WarpX 代码中应如何理解 |
| --- | --- | --- | --- |
| $f_s(x,p,t)$ | 物种粒子的位置、动量、权重集合 | $x_p^n,p_p^{n-1/2},w_p$ | `ParticleContainer` 中的粒子样本，不是一个逐点存储的分布函数 |
| $ρ(x,t)$ | shape-weighted charge density | $ρ^n$ 或 $\rho^{n+1/2}$ | 由粒子沉积得到；`rho_fp` 与 `rho_buf` 还可能分别属于 fine 与 coarse-buffer 路径 |
| $J(x,t)$ | trajectory-based current density | 通常跨越 $n -> n+1$ | Esirkepov/Villasenor 等 current deposition 需要 old/new 轨迹或等价的 crossing 信息 |
| $E,B$ | staggered/collocated grid fields | 由 solver 规定 | `Efield_*`、`Bfield_*` 的后缀表示时间层、网格位置或辅助副本，不能只按变量名猜物理时刻 |
| 连续性方程 | 离散 source synchronization | 每个粒子推进步或 solver stage | `SyncCurrentAndRho()`、guard exchange、AMR average-down 等共同完成可供场求解器使用的 source |

最容易被忽略的是 $ρ$ 和 $J$ 的时间语义不同。单时间层的 charge deposition 可以直接对粒子位置取样：

$$
ρ_i^n = (1 / ΔV_i) Σ_p q_p w_p S_i(x_p^n),
$$

而守恒的 current deposition 必须表达粒子从 $x_p^n$ 到 $x_p^{n+1}$ 的输运：

$$
Δt (∇_h·J)_i = ρ_i^n - ρ_i^{n+1}.
$$

这里的第二式不是说所有 current deposition 都在程序中显式先算出左右两边，而是说明它们必须满足同一条离散连续性关系。也因此，

- `DepositCharge()` 负责单时间层的 $ρ$ 采样及其时间层、几何和 AMR 桥接；
- `DepositCurrent()` 及其 Esirkepov/Villasenor 等路径负责轨迹输运产生的 $J$；
- `SyncCurrentAndRho()` 负责把不同 level、边界和 source buffer 中的结果整理成 solver 可消费的源项。

这三层不能合并成“粒子把电荷写到网格”一句话。后续第 5 章会从 kernel 角度展开，第 6 章则会继续说明不同 field solver 如何消费这些 source。附录 A 给出 `rho_fp`、`rho_buf`、`current_fp`、`current_buf` 和 `lev` 等 WarpX 实现变量的速查定义。

## 1.12 这一章对后面源码章节的真正约束

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

### 跨章交接卡：从连续对象进入离散循环

第 1 章回答“哪些物理对象必须被表示”；第 2 章回答“这些对象在一个离散时间步的什么时刻交换”。因此，进入第 2 章前，不应只带着一张函数名清单，而应先写出下列状态账本：

| 连续问题 | 必须保留的离散状态 | 进入第 2 章后首先核对 | 不能直接推出的结论 |
| --- | --- | --- | --- |
| 分布函数 \(f_s\) 怎样被近似 | 宏粒子的 \(x_p\)、\(p_p\)、\(w_p\) 与 shape | 2.2 中粒子样本如何 gather、deposit | 宏粒子数较多不自动保证相空间的每个细节都被分辨 |
| \(\rho\) 与 \(\mathbf{J}\) 怎样成为场的 source | 单时间层 \(\rho^n\) 与跨轨迹的 \(\mathbf{J}^{n+1/2}\) | 2.2--2.3 中连续性方程和 leapfrog 时间层 | 一次 charge deposition 不能替代守恒的 current deposition 或 source synchronization |
| \(\mathbf{E},\mathbf{B}\) 怎样作用于粒子又被 source 改写 | 网格位置、时间层和场表示 | 2.3--2.5 中交错 FDTD 或谱空间推进 | “有 Maxwell 方程”不说明某个 stencil、边界或 solver 组合具有可接受色散 |
| 哪些尺度必须由网格和步长承担 | \(\omega_p\)、\(\lambda_D\)、特征速度、\(\Delta t\)、\(\Delta x\) | 2.3 的时间层和可分辨尺度讨论 | CFL 可通过不表示 \(\omega_p\Delta t\)、\(\lambda_D/\Delta x\) 或统计误差已经满足物理目标 |

这张表给出一个严格的交接顺序：先说明粒子和场分别代表什么，再标出它们所在的时间层，最后才追踪程序调用。若不先区分“连续对象”“离散状态”和“可比较 observable”，就会把稳定性、守恒性与物理分辨率误当成同一类判断。第 2 章开头的接读卡将把这四类状态排成一次 \(n\rightarrow n+1\) 的实际交换顺序。

## 1.13 证据范围与继续阅读

本章下列论述可直接回到两部已提供逐段讲解的基础来源：

- `Birdsall 1985`：sheet model 的 randomization / correlation / thermalization 时间尺度，以及 finite-grid / aliasing / fluctuation / heating 主线。
- `Dawson 1983`：numerical experiment 视角、superparticle / weighted particles 的 kinetic 边界，以及 finite-size particles、网格和 FFT-Poisson 的 electrostatic contract。

下面两项适合作为后续补充阅读，但本章不依赖其未取得全文的细节：

- `Hockney-Eastwood`：加权粒子、heating estimates 和 optimum path 的经典表述。
- `Yee 1966`：staggered FDTD 与离散约束传播的原始出处。

继续阅读时，应优先回到原始论文、教材或官方文档，并为每一条主张标明它属于连续模型、离散算法还是特定代码实现；不要用其中任一层代替另外两层。第 2 章会把这里的 leapfrog、CFL、Debye 长度和数值色散接到同一条离散主循环上。

## 1.14 练习与源码定位

1. **变量桥接题**：根据 1.11 的映射表，说明为什么 `rho_fp/rho_buf` 不能直接当作两个不同物理量，并指出它们分别在哪个 AMR/source-synchronization 场景出现。
2. **尺度判断题**：给定 \(\lambda_D/\Delta x=0.5\) 和 \(v_t\Delta t/\Delta x=1.2\)，列出至少两个可能的数值风险，并说明它们分别属于空间分辨率、粒子跨单元输运还是时间推进约束。
3. **源码定位题**：从 `Source/Evolve/WarpXEvolve.cpp` 的 `OneStep_nosub()` 开始，而不是从全局搜索结果中猜入口。完成下列三步，并交付一个三行表格（函数、连续对象、调用后可认为“已准备好”的数据）：
   - 记录 `PushParticlesandDeposit()` 与 `SyncCurrentAndRho()` 的相对次序；前者对应粒子输运和源项沉积，后者应使场求解前的 `J/rho` 经滤波、guard-cell/MR 同步和边界处理而可被消费。
   - 打开 `WarpX::SyncCurrentAndRho()` 的定义，列出其中至少两项 source 数据准备动作，并说明它们为什么不能由连续方程本身自动保证。
   - 任选一个场更新分支：PSATD 路线继续定位 `PushPSATD()`（定义在 `Source/FieldSolver/WarpXPushFieldsEM.cpp`）；FDTD 路线则定位 `EvolveB()`/`EvolveE()` 的调用。说明该分支把哪一种离散 Maxwell 闭合推进到下一时间层。

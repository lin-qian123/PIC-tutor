# Higuera-Cary 2017 Structure-preserving second-order integration 笔记

## 0. 论文信息

- 标题：Structure-preserving second-order integration of relativistic charged particle trajectories in electromagnetic fields
- 作者：A. V. Higuera, J. R. Cary
- 期刊：Physics of Plasmas
- 年份：2017
- DOI：10.1063/1.4979989

## 1. 当前状态

- 已将原 PDF 保存在当前论文专属目录。
- 已通过项目内 `scripts/mineru_convert_stdlib.py` 完成 MinerU 转 Markdown。
- 已生成 `images/`。
- 下一步：
  - 按论文顺序开始第一轮中文精读。
  - 优先压实：
    - volume-preserving 与 `E x B` drift preservation 的并列目标
    - Boris / Vay / Higuera-Cary 三者的离散差异
    - 这些判断与 WarpX `UpdateMomentumHigueraCary.H` 的真实对位

## 2. 摘要与引言

### 2.1 这篇文章的第一性问题不是 boosted-frame，而是三种二阶 relativistic integrator 到底各保住了什么

摘要一上来就把比较维度压得很清楚：

- 三种方法都是 time-centered、second-order；
- 但它们保住的结构性质并不一样。

作者关心的不是一般误差阶，而是三条更硬的性质：

1. `E = 0` 时是否守恒能量；
2. crossed `E/B` 场下是否给出正确的 `\vec E \times \vec B` drift；
3. 是否 volume-preserving。

摘要的最终判决是：

- Boris：守能量、volume-preserving，但 `\vec E \times \vec B` drift 不对；
- Vay：守能量、`\vec E \times \vec B` drift 对，但不 volume-preserving；
- Higuera-Cary：三者里唯一同时保住 volume 和 `\vec E \times \vec B` drift 的二阶 relativistic momentum integrator。

### 2.2 引言给 Higuera-Cary 的定位不是“推翻 Boris”，而是补上 Boris 和 Vay 各自缺的一半

引言写得非常直接：

- Boris 的价值在于 volume preservation；
- Vay 的价值在于正确的 `\vec E \times \vec B` drift；
- 但两者各缺一块；
- 新方法的目标正是同时保住这两条性质。

所以这篇 paper 在本项目里的角色不该被写成：

- “Higuera-Cary 比 Boris/Vay 更高阶”

而应写成：

- 在同一 second-order relativistic leapfrog 家族里，
- 它重新组合了 centered average，
- 使离散系统同时保住两条关键几何/物理性质。

## 3. II. Second-order charged particle integrators

### 3.1 三种平均方式的真正分叉，不在 leapfrog 外壳，而在 magnetic rotation 里到底用哪个 centered velocity

论文从相同的 leapfrog 外壳出发：

$$
\frac { d \vec { x } } { d t } = \vec { v } ( \vec { u } ) = \vec { u } / \gamma ,
$$

$$
\frac { d \vec { u } } { d t } = ( q / m ) ( \vec { E } + \vec { v } ( \vec { u } ) \times \vec { B } ) .
$$

真正的差别是 magnetic rotation 里怎样取 centered `\bar v`。

作者给出三种选择：

#### Higuera-Cary 的新平均

$$
\bar { v } _ { new } \equiv \vec { v } \left( \frac { \vec { u } _ { i } + \vec { u } _ { f } } { 2 } \right) .
$$

#### Vay 的平均

$$
\bar { v } _ { v } \equiv \frac { \vec { v } ( \vec { u } _ { i } ) + \vec { v } ( \vec { u } _ { f } ) } { 2 } .
$$

#### Boris 的平均

$$
\bar { v } _ { b } \equiv \frac { \vec { v } \left( \vec { u } _ { i } + \vec { \epsilon } \right) + \vec { v } \left( \vec { u } _ { f } - \vec { \epsilon } \right) } { 2 } ,
$$

其中

$$
\vec { \epsilon } \equiv \frac { q \vec { E } } { 2 m } \Delta t .
$$

### 3.2 这里最重要的判断是：三者同为二阶，但 relativistic regime 下彼此偏离会越来越大

作者明确说：

- 这三种 centered choice 都只有 `O(\Delta t^2)` 误差；
- 但它们相互之间的差异会随 relativistic 程度增大而变大。

因此这篇 paper 的主轴不是简单“误差阶比较”，而是：

- 在同一二阶家族里，
- 不同的 centered average 会带来不同的结构保持性质，
- 而这些差异在高相对论运动中会被放大。

## 4. III. Explicit evaluation

### 4.1 新方法表面上是 implicit，实质上仍可显式求解

这一节的价值在于说明：

- 新平均看起来用到了 `\vec u_f`，
- 好像是 implicit scheme；
- 但经过重写后，仍然能像 Vay 那样显式求出。

作者把它写成两半步组合后，引入

$$
\vec { \beta } \equiv \frac { q \vec { B } } { 2 m } \Delta t ,
$$

以及

$$
\vec { u } _ { - } \equiv \vec { u } _ { i } + \vec { \epsilon } .
$$

最终得到新的 relativistic factor 满足的显式公式：

$$
\gamma _ { new } ^ { 2 } = \frac { 1 } { 2 } \left( \gamma _ { - } ^ { 2 } - \beta ^ { 2 } + \sqrt { ( \gamma _ { - } ^ { 2 } - \beta ^ { 2 } ) ^ { 2 } + 4 \left( \beta ^ { 2 } + | \vec { \beta } \cdot \vec { u } _ { - } | ^ { 2 } \right) } \right) .
$$

### 4.2 这就是 WarpX `UpdateMomentumHigueraCary.H` 真正该对位的地方

对本项目而言，这一节最关键的落点不是长推导本身，而是：

- WarpX `UpdateMomentumHigueraCary.H` 和 Boris 的外形很像；
- 真正的分叉点正是 `gamma` 的计算方式；
- 这和论文原文完全一致。

所以 WarpX 里的 Higuera-Cary 也不该写成：

- “另一个看起来像 Boris 的 kernel”

而应写成：

- Boris-like rotation skeleton
- 加上 Higuera-Cary 的 `\gamma_new` prescription
- 从而服务于后面两条保持性质的同时成立

### 4.3 论文公式和 WarpX kernel 可以直接逐式对上

论文里先定义

$$
\vec { \epsilon } = \frac { q \vec { E } } { 2 m } \Delta t ,
\qquad
\vec { \beta } = \frac { q \vec { B } } { 2 m } \Delta t ,
$$

以及

$$
\vec { u } _ { - } = \vec { u } _ { i } + \vec { \epsilon } .
$$

在 WarpX `UpdateMomentumHigueraCary.H` 里，这些量直接对应为：

- `qmt = 0.5*q*dt/m`
- `umx, umy, umz`
- `betax, betay, betaz`

论文的

$$
\gamma_-^2 = 1 + |\vec u_-|^2/c^2
$$

对应源码里先算出的 `gamma`。

然后论文给出

$$
\gamma _ { new } ^ { 2 } = \frac { 1 } { 2 } \left( \gamma _ { - } ^ { 2 } - \beta ^ { 2 } + \sqrt { ( \gamma _ { - } ^ { 2 } - \beta ^ { 2 } ) ^ { 2 } + 4 \left( \beta ^ { 2 } + | \vec { \beta } \cdot \vec { u } _ { - } | ^ { 2 } \right) } \right) .
$$

WarpX 里并没有先显式存 `\gamma_new^2`，而是把这条式子改写成：

- `sigma = gamma - betam`
- `ust = (u_- · beta)/c`
- `gamma = 1/sqrt(0.5*(sigma + sqrt(sigma*sigma + 4*(betam + ust*ust))))`

也就是说，源码变量 `gamma` 在这一行之后已经不是 `\gamma_-^2`，
而是

$$
\gamma_{new}^{-1}.
$$

这一点如果不写清，很容易误读成“WarpX 用了另一套不相关公式”，其实没有，它只是直接存了最后 rotation 要用的逆相对论因子。

### 4.4 论文里的 Boris-like rotation equation 也被原样压进了 WarpX 的 `t/s/u_plus` 链

论文把显式求解最后压成

$$
\vec { u } _ { + } - \vec { u } _ { - } = ( \vec { u } _ { + } + \vec { u } _ { - } ) \times \frac { \vec { \beta } } { \gamma _ { new } } .
$$

WarpX 里对应的是：

- `tx, ty, tz = gamma * beta`
- `s = 1/(1+t^2)`
- `umt = u_- \cdot t`
- `upx, upy, upz`

这条链和 Boris 的旋转骨架几乎同形，
只是把 `t` 的定义改成了基于 `\gamma_new^{-1}` 的版本。

所以源码里最值得强调的不是“它看起来像 Boris”，而是：

- 它在最小结构改动下，
- 把 Boris 的 rotation skeleton 与 Higuera-Cary 的 `\gamma_new` prescription 拼接起来了。

## 5. IV. Preservation of limiting solutions

### 5.1 三种方法在 `E = 0` 时都守能量，这不是分叉点

作者先把一个容易混淆的点排除了：

- 当 `E = 0` 时，
- Boris、Vay、Higuera-Cary 都守恒能量。

因此：

- “能不能在纯磁场里守能量”
- 不是这三者真正拉开差距的核心判据。

### 5.2 真正分叉点之一是 crossed `E/B` 下的 `\vec E \times \vec B` drift

对静止解，作者要求

$$
\Delta \vec v = 0
$$

时必须给出

$$
\bar { v } = \vec { E } \times \vec { B } / | \vec { B } | ^ { 2 } .
$$

结论是：

- Higuera-Cary 和 Vay 都给出正确的 `\vec E \times \vec B` drift；
- Boris 不行。

因此这篇文章把 Vay 的价值保留得很明确：

- Vay 不是“错误方法”；
- 它确实修好了 Boris 的 drift 缺陷；
- 只是它在 volume preservation 上又丢了一块。

## 6. V. Volume-preservation

### 6.1 Higuera-Cary 的另一条核心主张是：它和 Boris 一样 volume-preserving

这一节的核心不是一般几何修辞，而是 Jacobian 结构。

作者证明：

- Boris 是 volume-preserving；
- 新方法的两半步 Jacobian determinant 互为倒数；
- 因而总体 Jacobian 为 `1`；
- 所以新 integrator 也是 volume-preserving。

也就是说，

- Higuera-Cary 不是只“看起来像 Boris”；
- 它继承了 Boris 最重要的几何性质之一。

### 6.2 对 Vay 的批评在这篇 paper 里有很具体的形式：它的 Jacobian 一般不会 telescoping 成 `1`

作者把 Vay 的 Jacobian 写成一种 step-by-step 比值结构，并指出：

- 一般情况下它不 volume-preserving；
- 在空间变化磁场里，局部 phase-space volume 会增长或缩小；
- 这为后面的非物理轨道现象埋下了机制基础。

这里要注意边界：

- 作者没有说 Vay 在所有问题里都会立即炸掉；
- 他说的是：
  - 它缺少一个 Boris 和 Higuera-Cary 都有的结构保持性质，
  - 因而可能出现 underlying continuous system 不该有的 attractor/repeller-like behavior。

### 6.3 这篇文章里最硬的 volume-preservation 证据不是口头“结构保持”，而是两半步 Jacobian 互为倒数

作者对新方法的关键证明是：

- 先对前后半步写 Jacobian；
- 再证明两者 determinant 互为倒数；
- 因而整个一步更新的 Jacobian 为 `1`。

文中的关键结果可以压成：

$$
J _ { f , new } = 1 + \frac { \beta ^ { 2 } + ( \vec { \beta } \cdot \bar { u } _ { new } ) ^ { 2 } } { \gamma _ { new } ^ { 4 } } ,
$$

$$
J _ { i , new } = 1 + \frac { \beta ^ { 2 } + ( \vec { \beta } \cdot \bar { u } _ { new } ) ^ { 2 } } { \gamma _ { new } ^ { 4 } } ,
$$

于是整体体积保持来自：

- 前半步 determinant
- 与后半步 inverse determinant
- 的精确抵消。

这解释了为什么作者把“volume-preserving”看成一条结构性质，而不是数值上“看起来没怎么漂”。

### 6.3.1 证明链条里最关键的中间对象其实是 `I-\Omega`

作者先把后半步对 `\bar u_{new}` 的 Jacobian 写成

$$
\frac { \partial ( \vec { u } _ { f } ) } { \partial ( \bar { u } _ { n e w } ) }
=
I - \Omega
+ \frac { \vec { \beta } \times \bar { u } _ { n e w } \otimes \bar { u } _ { n e w } } { \gamma _ { n e w } ^ { 3 } } ,
$$

其中

$$
\Omega \cdot \vec V \equiv \frac{\vec\beta \times \vec V}{\gamma_{new}} .
$$

也就是说，整个 Jacobian 被拆成了：

- 一个主干 `I-\Omega`
- 再加一个 rank-one correction

这就是后面能直接套 determinant lemma 的原因。

### 6.3.2 determinant lemma 在这里不是形式操作，而是把“旋转主干”和“相对论修正”分开

作者随后写成

$$
J_{f,new}
=
\det(I-\Omega)\,
\det\!\left(
1+\frac{\bar u_{new}\cdot (I-\Omega)^{-1}\cdot (\vec\beta\times\bar u_{new})}{\gamma_{new}^3}
\right).
$$

这里最值得记住的不是每个符号，而是分工：

- `\det(I-\Omega)` 负责 Boris-like rotation skeleton 的体积贡献；
- 第二项负责相对论修正项的体积贡献；
- 两者最终重新合成一个简单标量表达式。

所以这篇 paper 的“结构保持”证明并不是抽象几何口号，而是明确把：

- 磁旋转主干
- 和额外 relativistic correction

拆开检查 Jacobian。

### 6.3.3 为什么最后会得到简单的 `J_f`

作者先算出

$$
\det(I-\Omega)=1+\beta^2/\gamma_{new}^2 ,
$$

再引入

$$
\vec Y = (I+\Omega)^{-1}\cdot \bar u_{new},
$$

并把 `\bar u_{new}\cdot (I-\Omega)^{-1}\cdot (\vec\beta\times\bar u_{new})`
改写到 `\vec Y` 上。

做完这些代数整理后，后半步 determinant 被压成

$$
J _ { f , new } = 1 + \frac { \beta ^ { 2 } + ( \vec { \beta } \cdot \bar { u } _ { new } ) ^ { 2 } } { \gamma _ { new } ^ { 4 } } .
$$

这一步的意义是：

- 复杂 Jacobian 最后只剩一个显式、正定的标量函数；
- 所以后面对前半步做同样操作时，就有机会直接比较两者是否互为逆。

### 6.3.4 真正的闭环点不是 `J_f` 本身，而是前后半步的 reciprocal relation

作者随后指出：

$$
J _ { i , new } = 1 + \frac { \beta ^ { 2 } + ( \vec { \beta } \cdot \bar { u } _ { new } ) ^ { 2 } } { \gamma _ { new } ^ { 4 } } ,
$$

这里要特别小心记号含义：

- `J_{f,new}` 是后半步映射的 Jacobian determinant；
- `J_{i,new}` 写成同一标量形式，但对应的是前半步那条反向映射链上的 determinant；
- 因此它们虽然代数表达式同形，
- 在整步组合里扮演的是互逆位置。

于是前半步与后半步的 determinant 正好互相抵消，
整体一步更新满足

$$
J_{step}=1.
$$

这才是新 integrator 被称为 volume-preserving 的真正数学内容：

- 不是“每半步都单独等于 1”
- 而是两半步的 Jacobian 乘起来等于 1

这和 Boris 的离散旋转为什么表现稳定，在结构上是同一类判断。

### 6.4 Vay 的 Jacobian 结构为什么会丢掉这一点

作者把 Vay 的 Jacobian 写成逐步比值形式：

$$
J _ { v } = \frac { J ( x _ { i } , u _ { i } ) } { J ( x _ { i } , u _ { f } ) } .
$$

这意味着：

- 分子和分母虽然形式相同，
- 但依赖的是不同的动量变量；
- 所以一般不会化成 `1`。

这正是作者后面把 resonance island / trajectory crossing 归咎于 Vay 缺少 volume-preservation 的机制基础。

### 6.4.1 论文对 Vay 也保留了一个很重要的例外边界

作者没有把 Vay 写成“必然出现 attractor/repeller”。
更准确的说法是：

- 一般空间变化场里，逐步比值不会化成 `1`；
- 但如果磁场在时空上是常量，
- 这串比值会 telescoping；
- 再加上 `J(x,u)` 在有界区域里本身有界，
- 就不会立刻推出 attractor / repeller。

所以 paper 的论证边界是：

- `Vay` 缺少一般性的 volume-preservation；
- 在 practical timestep 和更复杂轨道拓扑下会暴露问题；
- 但不是任何简单场景里都必然立刻坏掉。

## 7. VI. Numerical results

### 图 1：小时间步下，三者都能看起来“不错”

![Fig. 1 poincare small dt](images/000bab528fc794ad622449406dcaf752ce7d5ff858696da3219697b2168a0208.jpg)

**图像描述：**

- 作者选了一个 integrable relativistic test Hamiltonian；
- 用 Poincare section 在 `(y,p_y)` 平面上看轨道拓扑；
- 小时间步 `\Delta t = 1/40` 下，
- Boris、Vay、Higuera-Cary 都给出嵌套曲线。

**关键解读：**

- 这张图的作用不是证明“三者等价”；
- 而是说明只看很小时间步时，
- Vay 的问题可能完全看不出来。

### 图 2：更实际的时间步下，Vay 出现 resonance island 和轨道交叉

![Fig. 2 poincare practical dt](images/a08b4b034a0c929e2d7744cad427f3f2991aee4ca7fb0a2c6d2d2e854017d462.jpg)

**图像描述：**

- 把时间步放宽到 `\Delta t = 1/10`；
- 这更接近 simulation 里常见的时间步尺度；
- Boris 和 Higuera-Cary 仍保持嵌套拓扑；
- Vay 在 `p_y \approx 1.7` 附近出现 two-fold degenerate resonance island。

**关键解读：**

- Vay 不仅出现 resonance trapping；
- 不同轨道的 section 还会互相交叉；
- 这说明别的 invariant 也没有被很好保持；
- 于是文中的结论不是“Vay 稍微差一点”，而是：
  - 在合理时间步下，
  - 它会给出 unphysical consequences。

### 7.1 这组数值结果在本项目里的真正意义

这里最硬的对照不是 energy curve，而是：

- phase-space topology
- invariant preservation
- practical timestep 下是否引入假共振

因此 `Higuera 2017` 这篇文章和 `Vay 2008` 的职责刚好不同：

- `Vay 2008` 主打 frame-change consistency；
- `Higuera 2017` 主打 geometric/topological preservation at practical timestep。

### 7.2 它和 WarpX 当前 regression 的真实配对并不对称

对本项目而言，这篇 paper 现在最自然能接上的不是完整的 Poincare-surface-of-section reproduction，
而是本地已有的 `particle_pusher` force-free 单粒子 analysis：

- `Examples/Tests/particle_pusher/inputs_test_3d_particle_pusher`
- `Examples/Tests/particle_pusher/analysis.py`

这条 regression 当前固定：

- `algo.particle_pusher = "higuera"`
- 单个 positron
- 常量外部 `E/B`
- 满足 force-free 条件
  $$
  E_x = - v_y B_z
  $$
- 长时间推进后直接检查
  $$
  x \approx 0.
  $$

因此它提供的是：

- Higuera-Cary 在 relativistic force-free configuration 下不产生显著横向漂移误差

这和论文的 `\vec E \times \vec B` / structure-preserving 主线是相容的，
但还没有把论文第 VI 节那种 practical-timestep topology comparison 完整重建出来。

与之相对，

- `larmor`
- 当前仍只有 checksum baseline，
- 还不能被写成 Higuera-Cary 论文里 gyro/topology 结论的强本地复现。

所以当前最准确的项目内判断是：

- `particle_pusher`：能接论文的 force-free / drift-preservation 边界
- `larmor`：还只是应用级稳定性基线
- 论文里最强的 topology / resonance-island 结论，当前本地还没有 dedicated reproduction

## 8. VII. Summary 与本项目里的真实定位

### 8.1 这篇文献最终交付的不是一般“更准的 pusher”，而是一个双保持性质的 second-order relativistic integrator

通篇收束后，最准确的总结是：

- Boris 保住 volume，但不保 `\vec E \times \vec B` drift；
- Vay 保住 drift，但不保 volume；
- Higuera-Cary 同时保住 volume 和 drift，
- 且在 `E = 0` 时同样守能量，
- 在 practical timestep 下又避免了 Vay 的假共振。

### 8.2 它在 PIC-tutor 里的正确角色

对本项目而言，`Higuera 2017` 应被定位成：

- `structure-preserving relativistic Boris-like pusher paper`
- `volume + E×B drift benchmark`

而不是：

- 单纯的 Boris 改进版；
- 或和 `Vay 2008` 相同问题设定下的替代文献。

更具体地说：

- 它最直接支撑第 4 章 `UpdateMomentumHigueraCary.H` 的历史和数学边界；
- 它解释了为什么 WarpX 里 Higuera-Cary 常被放在 Boris/Vay 并列位置，
- 但其价值判断标准并不是 boosted-frame cancellation，而是 geometric preservation。

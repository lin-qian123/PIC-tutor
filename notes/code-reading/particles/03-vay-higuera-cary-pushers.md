# 03. Vay 与 Higuera-Cary pusher 源码证据

## 1. Vay pusher

`Source/Particles/Pusher/UpdateMomentumVay.H:17-77` 定义 `UpdateMomentumVay()`。

| 行号 | 作用 |
|---|---|
| `:17-24` | 文件注释说明该算法可分裂为 `FirstHalf` 和 `SecondHalf`，并引用 Vay 2008 的公式 (9)-(13)。 |
| `:37-38` | `econst=q*dt/m` 或半步值；`bconst=0.5*q*dt/m`。 |
| `:40` | 用旧动量计算 `inv_gamma`。 |
| `:42-45` | 定义 `tau=(q dt/2m) B` 和 `tausq`。 |
| `:47-49` | 构造 `u'`，包含电场项和非 `SecondHalf` 时的旧速度磁项。 |
| `:51-70` | 非 `FirstHalf` 时求解新的 \(\gamma\)、`t`、`s`，并更新动量。 |
| `:72-75` | `FirstHalf` 只返回 `u'`。 |

物理要点：Vay pusher 不是 Boris 的简单变量名变体。它通过解析求解新 \(\gamma\) 来处理相对论速度变换一致性问题，WarpX 文档参数表把 `algo.particle_pusher = vay` 引到 `param-Vaypop2008`。

## 2. Higuera-Cary pusher

`Source/Particles/Pusher/UpdateMomentumHigueraCary.H:16-65` 定义 `UpdateMomentumHigueraCary()`。

| 行号 | 作用 |
|---|---|
| `:31` | 定义半步系数 `qmt=0.5*q*dt/m`。 |
| `:33-35` | 电场半步得到 `u_minus`。 |
| `:37-48` | 用 `u_minus` 和 `beta=qmt B` 求新的 \(\gamma^{-1}\)。 |
| `:50-56` | 构造旋转向量 `t`、归一化因子 `s` 和 `u_minus dot t`。 |
| `:58-60` | 得到 `u_plus`。 |
| `:62-64` | 用 Higuera-Cary 公式加入第二个电场项和额外叉乘项，得到新动量。 |

Higuera-Cary 的结构仍然像 Boris 的 “电半步 + 磁旋转 + 电半步”，但最后一步不是 Boris 的简单第二电半步，而是包含 `upy*tz-upz*ty` 等项。WarpX 文档参数表把 `algo.particle_pusher = higuera` 引到 `param-HigueraPOP2017`。

把这段 kernel 重新和 Higuera-Cary 2017 对位，变量链可以压得更硬：

| 论文量 | WarpX 变量 |
|---|---|
| \(\vec{\epsilon} = (q\Delta t/2m)\vec E\) | `qmt*Ex/Ey/Ez` |
| \(\vec{\beta} = (q\Delta t/2m)\vec B\) | `betax/betay/betaz` |
| \(\vec u_-\) | `umx/umy/umz` |
| \(\gamma_-^2 = 1 + |\vec u_-|^2/c^2\) | `gamma` 在 `:37` 之后的值 |
| \(\sigma = \gamma_-^2-\beta^2\) | `sigma` |
| \(u_* = (\vec u_- \cdot \vec\beta)/c\) | `ust` |
| \(\gamma_{new}^{-1}\) | `gamma` 在 `:46` 之后的值 |
| \(\vec t = \vec\beta/\gamma_{new}\) | `tx/ty/tz` |
| \(s = 1/(1+t^2)\) | `s` |
| \(\vec u_+\) | `upx/upy/upz` |

这里最容易误读的一点是：源码变量 `gamma` 在函数中段被重载，前半段保存的是 \(\gamma_-^2\)，进入 `:46` 后保存的已经是 \(\gamma_{new}^{-1}\)。如果忽略这点，会误以为 WarpX 和论文用了两套无关公式；实际上只是把论文的

$$
\gamma _ { new } ^ { 2 } = \frac { 1 } { 2 } \left( \gamma _ { - } ^ { 2 } - \beta ^ { 2 } + \sqrt { ( \gamma _ { - } ^ { 2 } - \beta ^ { 2 } ) ^ { 2 } + 4 \left( \beta ^ { 2 } + | \vec { \beta } \cdot \vec { u } _ { - } | ^ { 2 } \right) } \right)
$$

直接改写成了 rotation 要消费的逆相对论因子。

论文里的 Boris-like rotation equation

$$
\vec { u } _ { + } - \vec { u } _ { - } = ( \vec { u } _ { + } + \vec { u } _ { - } ) \times \frac { \vec { \beta } } { \gamma _ { new } }
$$

也被原样压成了 `tx/ty/tz`、`s`、`umt` 和 `up*` 这条链。这说明 Higuera-Cary kernel 的关键不是“多了几个修正项”，而是：在 Boris 的 rotation skeleton 上换了 \(\gamma\) prescription，从而服务于后面 `volume-preserving + E×B drift` 的双保持结论。

Higuera-Cary 2017 对几何性质的证明也值得直接挂到源码理解后面。论文证明新 integrator 的前后半步 Jacobian determinant 互为倒数，因此整体 Jacobian 为 `1`；而 Vay 的 Jacobian 一般写成

$$
J_v = \frac{J(x_i,u_i)}{J(x_i,u_f)},
$$

通常不会化成 `1`。这就是为什么同样是二阶 relativistic mover，Higuera-Cary 在 practical timestep 下仍维持 phase-space topology，而 Vay 可能出现 resonance island 与轨道交叉。

如果把 Jacobian 证明再压细一点，最关键的不是最后那条 `J_step=1`，而是中间如何拆分。论文先把后半步 Jacobian 写成

$$
\frac{\partial u_f}{\partial \bar u_{new}}
=
I-\Omega
+ \text{rank-one correction},
$$

其中

$$
\Omega \cdot V = (\beta \times V)/\gamma_{new}.
$$

这一步把问题拆成了：

- `I-\Omega` 对应 Boris-like rotation 主干
- rank-one correction 对应 relativistic correction

然后作者用 determinant lemma 写出

$$
J_{f,new}
=
\det(I-\Omega)\times(\text{scalar correction}),
$$

并进一步得到

$$
J _ { f , new } = 1 + \frac { \beta ^ { 2 } + ( \vec { \beta } \cdot \bar { u } _ { new } ) ^ { 2 } } { \gamma _ { new } ^ { 4 } } .
$$

同样方式可得前半步的 Jacobian，因此 volume-preserving 的真正数学内容是：

- 不是每个子步单独体积不变，
- 而是前后半步的 determinant 互为逆，
- 整个一步更新的 Jacobian 才等于 `1`。

这里还要补一个记号边界：论文里 `J_{f,new}` 和 `J_{i,new}` 最后被压成同一显式标量函数，但它们对应的是后半步和前半步那两条相反方向映射上的 determinant；因此“同形”不等于“同一对象”，而是意味着两条子步在整步组合里正好处在 reciprocal 位置。

这条证明链对源码理解的意义在于：`UpdateMomentumHigueraCary.H` 不是“经验上更稳”的 kernel，而是被一条明确的 Jacobian 结构性质支撑着。

对 Vay 也要保留论文自己的例外边界。`J_v = J(x_i,u_i)/J(x_i,u_f)` 说明它一般不 volume-preserving，但论文同时指出：若磁场在时空上恒定，这串比值会 telescoping，再加上 `J(x,u)` 的有界性，就不能直接推出 attractor/repeller。因此更准确的说法是：

- Vay 缺少一般性的 volume-preservation；
- 在 practical timestep 和更复杂轨道拓扑下会暴露问题；
- 但不是每个简单场景都会立刻表现出灾难性几何失真。

## 3. 分派位置

`Source/Particles/Pusher/PushSelector.H:89-100` 将三种有质量粒子主 pusher 汇合：

- `ParticlePusherAlgo::Boris` -> `UpdateMomentumBoris()`
- `ParticlePusherAlgo::Vay` -> `UpdateMomentumVay()`
- `ParticlePusherAlgo::HigueraCary` -> `UpdateMomentumHigueraCary()`

后续还需要继续精读带 classical radiation reaction 的 Boris 变体和 implicit pusher。

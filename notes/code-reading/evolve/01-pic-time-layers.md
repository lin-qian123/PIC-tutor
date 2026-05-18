# 01. PIC 时间层与 `OneStep_nosub`

## 1. 连续方程组

显式电磁 PIC 的出发点是 Vlasov-Maxwell 系统。对每个物种 \(s\)，分布函数 \(f_s(\mathbf{x},\mathbf{p},t)\) 满足

$$
\frac{\partial f_s}{\partial t}
+\mathbf{v}\cdot\nabla_{\mathbf{x}} f_s
+q_s\left(\mathbf{E}+\mathbf{v}\times\mathbf{B}\right)\cdot\nabla_{\mathbf{p}} f_s=0,
$$

其中相对论动量和速度满足

$$
\mathbf{p}=\gamma m_s\mathbf{v},\qquad
\gamma=\sqrt{1+\frac{|\mathbf{p}|^2}{m_s^2c^2}}.
$$

电磁场满足

$$
\frac{\partial \mathbf{B}}{\partial t}=-\nabla\times\mathbf{E},
\qquad
\frac{\partial \mathbf{E}}{\partial t}=c^2\nabla\times\mathbf{B}-\frac{\mathbf{J}}{\epsilon_0},
$$

并受约束

$$
\nabla\cdot\mathbf{E}=\frac{\rho}{\epsilon_0},\qquad
\nabla\cdot\mathbf{B}=0.
$$

粒子源项由分布函数矩给出：

$$
\rho(\mathbf{x},t)=\sum_s q_s\int f_s(\mathbf{x},\mathbf{p},t)\,d\mathbf{p},
\qquad
\mathbf{J}(\mathbf{x},t)=\sum_s q_s\int \mathbf{v}f_s(\mathbf{x},\mathbf{p},t)\,d\mathbf{p}.
$$

PIC 的关键近似是用宏粒子表示 \(f_s\)，并用有限支撑形函数 \(S\) 在粒子和网格之间相互映射。

## 2. 宏粒子与形函数

把分布函数写成宏粒子和形函数的和：

$$
f_s(\mathbf{x},\mathbf{p},t)
\approx
\sum_{p\in s} w_p
S_x(\mathbf{x}-\mathbf{x}_p(t))
S_p(\mathbf{p}-\mathbf{p}_p(t)).
$$

于是网格电荷密度的典型离散形式是

$$
\rho_i^n=\frac{1}{\Delta V_i}\sum_p q_p w_p S_i(\mathbf{x}_p^n),
$$

其中 \(S_i(\mathbf{x}_p)\) 表示粒子 \(p\) 对网格点或网格单元 \(i\) 的形函数权重。场 gather 则是反向加权：

$$
\mathbf{E}_p^n=\sum_i S_i(\mathbf{x}_p^n)\mathbf{E}_i^n,
\qquad
\mathbf{B}_p^n=\sum_i S_i(\mathbf{x}_p^n)\mathbf{B}_i^n.
$$

电流沉积比电荷沉积更严格。为了让离散 Gauss 定律随时间保持一致，电流必须满足离散连续性方程：

$$
\frac{\rho_i^{n+1}-\rho_i^n}{\Delta t}
+(\nabla_h\cdot\mathbf{J}^{n+1/2})_i=0.
$$

这就是 Esirkepov、Villasenor-Buneman、Vay 等沉积算法在 PIC 代码中如此核心的原因：它们不是简单“把速度乘电荷放到网格”，而是在离散网格上表达粒子穿过 cell 的轨迹。

## 3. leapfrog 时间层

WarpX 在显式电磁路径中采用典型 leapfrog 结构。`Source/Evolve/WarpXEvolve.cpp:512-515` 的注释直接给出 `OneStep_nosub()` 的时间层：

```text
Push particle from x^{n} to x^{n+1}
              from p^{n-1/2} to p^{n+1/2}
Deposit current j^{n+1/2}
Deposit charge density rho^{n}
```

这个注释必须按时间层读：

- 位置在整数步：\(\mathbf{x}^n,\mathbf{x}^{n+1}\)。
- 动量在半整数步：\(\mathbf{p}^{n-1/2},\mathbf{p}^{n+1/2}\)。
- 电流自然处在半步：\(\mathbf{J}^{n+1/2}\)。
- 电磁场在 Yee/FDTD 路径中按 \(\mathbf{B}^{n}\to\mathbf{B}^{n+1/2}\to\mathbf{B}^{n+1}\)、\(\mathbf{E}^{n}\to\mathbf{E}^{n+1}\) 推进。

形式上可写为

$$
\frac{\mathbf{x}^{n+1}-\mathbf{x}^n}{\Delta t}
=
\mathbf{v}^{n+1/2},
$$

$$
\frac{\mathbf{p}^{n+1/2}-\mathbf{p}^{n-1/2}}{\Delta t}
=
q\left(
\mathbf{E}^{n}_{p}
+\bar{\mathbf{v}}\times\mathbf{B}^{n}_{p}
\right),
$$

其中实际相对论 pusher 会用 Boris、Vay 或 Higuera-Cary 等算法处理磁转动与相对论速度定义。本章不提前展开 pusher 内核，只强调主循环对时间层的要求。

## 4. FDTD 场更新的主结构

对无介质、无 PSATD 的显式电磁路径，`OneStep_nosub()` 在沉积和同步后执行：

| 源码位置 | 数学含义 |
|---|---|
| `Source/Evolve/WarpXEvolve.cpp:604-607` | divergence-cleaning 辅助场 \(F,G\) 先推进半步并填充 guard cells。 |
| `Source/Evolve/WarpXEvolve.cpp:609-610` | \( \mathbf{B}^{n}\to\mathbf{B}^{n+1/2} \)。 |
| `Source/Evolve/WarpXEvolve.cpp:612-621` | 真空介质走 `EvolveE(dt)`，宏观介质走 `MacroscopicEvolveE(dt)`，得到 \( \mathbf{E}^{n+1} \)。 |
| `Source/Evolve/WarpXEvolve.cpp:623-625` | 辅助场再半步，\( \mathbf{B}^{n+1/2}\to\mathbf{B}^{n+1} \)。 |
| `Source/Evolve/WarpXEvolve.cpp:627-640` | PML 阻尼与必要 guard cell 更新。 |

若忽略 PML、清洗场、宏观介质和边界，Yee 结构可概括为

$$
\mathbf{B}^{n+1/2}
=
\mathbf{B}^{n}
-\frac{\Delta t}{2}\nabla_h\times\mathbf{E}^{n},
$$

$$
\mathbf{E}^{n+1}
=
\mathbf{E}^{n}
+c^2\Delta t\nabla_h\times\mathbf{B}^{n+1/2}
-\frac{\Delta t}{\epsilon_0}\mathbf{J}^{n+1/2},
$$

$$
\mathbf{B}^{n+1}
=
\mathbf{B}^{n+1/2}
-\frac{\Delta t}{2}\nabla_h\times\mathbf{E}^{n+1}.
$$

这套公式解释了为什么 `OneStep_nosub()` 必须先完成粒子推进和电流沉积，再推进电场；电场更新需要 \(\mathbf{J}^{n+1/2}\)。

## 5. WarpX 对“同步”的工程定义

源码里的同步不是抽象概念，而是多个具体操作：

- `Source/Evolve/WarpXEvolve.cpp:558-561`：`SyncCurrentAndRho()` 执行电流和电荷同步。
- `Source/Evolve/WarpXEvolve.cpp:768-837`：PSATD 与 FDTD 对 `SyncCurrent()`、`SyncRho()` 的调用条件不同，并在最后施加 PEC 等边界对 \(\rho,\mathbf{J}\) 的处理。
- `Source/Evolve/WarpXEvolve.cpp:652-711`：`ExplicitFillBoundaryEBUpdateAux()` 管理粒子 gather 前的场 guard cells 和 auxiliary data；若 `m_is_synchronized` 为真，则先把粒子动量回退半步。

因此，本书写 WarpX 主循环时必须区分三类“同步”：

1. 粒子时间层同步：\(\mathbf{x}\) 和 \(\mathbf{p}\) 是否都在整数步。
2. 网格源项同步：沉积后的 \(\rho,\mathbf{J}\) 是否经过滤波、guard cell、AMR 跨层和边界处理。
3. 场数组同步：\(\mathbf{E},\mathbf{B},F,G\) 的 guard cells 是否足够支持下一次 field solve 或 field gather。

混淆这三类同步，是读 PIC 生产代码时最常见的错误之一。


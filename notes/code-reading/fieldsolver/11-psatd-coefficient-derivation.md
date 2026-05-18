# PSATD 系数来源：`Tools/Algorithms/psatd.ipynb`

绑定源码与文档：

- `../warpx/Tools/Algorithms/psatd.ipynb`
- `../warpx/Source/FieldSolver/SpectralSolver/SpectralAlgorithms/PsatdAlgorithmGalilean.cpp`
- `../warpx/Source/FieldSolver/SpectralSolver/SpectralAlgorithms/PsatdAlgorithmJRhomFirstOrder.cpp`
- `../warpx/Source/FieldSolver/SpectralSolver/SpectralAlgorithms/PsatdAlgorithmJRhomSecondOrder.cpp`
- `../warpx/Docs/source/theory/models_algorithms/explicit_em_pic.rst:165-360`

这份 notebook 不是运行时代码，而是 PSATD 解析系数的符号推导脚本。WarpX 里真正执行的更新式，像 `C/S_ck/T2/X1-X4`、`Y1-Y8`、零模极限、`update_with_rho` 和 JRhom 系数，都可以在这里找到它们的数学来源。

这一节要讲清楚两件事：

1. 这些系数是从什么线性系统里推出来的。
2. notebook 怎样把符号推导变成可以直接对照源码的系数表。

## 1. notebook 的建模范围

开头先固定符号版本和算法分支：

```python
import sympy as sp
from packaging.version import parse
from sympy import *  # noqa

sp.init_session()
sp.init_printing()

sp_version_compatible = "1.12.1"
if parse(sp.__version__) > parse(sp_version_compatible):
    raise ValueError(
        f"Versions of sympy>{sp_version_compatible} do not yield correct results, please use sympy<={sp_version_compatible}"
    )
```

这个限制不是形式主义。PSATD 的系数推导依赖大量矩阵对角化、指数矩阵和三角恒等式化简，SymPy 版本变动会改写表达式结构，进而影响化简结果是否和源码一致。

notebook 选择的默认分支是：

```python
divE_cleaning = True
divB_cleaning = True
J_in_time = "constant"
rho_in_time = "linear"
```

这对应 WarpX 里最核心的标准 PSATD 结构：

- `E/B` 全场推进。
- `F/G` 作为 divergence cleaning 标量。
- `J` 在一个 PIC 步里视作常量。
- `rho` 在一个 PIC 步里视作线性变化。

这也是 `PsatdAlgorithmGalilean.cpp` 和普通 PSATD 文档最常对照的那一组系数。

## 2. 从 Maxwell 方程到线性常微分方程组

notebook 先把傅里叶空间中的 Maxwell 方程写成一阶系统。核心是把 `curl` 变成 `i k x`，把 `div` 变成 `i k ·`。

源码式写法如下：

```python
# Define first-order time derivatives of the electric field
dEx_dt = I * c**2 * (ky * Bz - kz * By)
dEy_dt = I * c**2 * (kz * Bx - kx * Bz)
dEz_dt = I * c**2 * (kx * By - ky * Bx)

# Define first-order time derivatives of the magnetic field
dBx_dt = -I * (ky * Ez - kz * Ey)
dBy_dt = -I * (kz * Ex - kx * Ez)
dBz_dt = -I * (kx * Ey - ky * Ex)
```

加入 `F/G` 后，系统变成：

- `E` 多了 `i c^2 k F`
- `B` 多了 `i c^2 k G`
- `F` 满足 `∂t F = i k·E`
- `G` 满足 `∂t G = i k·B`

这一步的物理含义很重要：PSATD 不是只推进 `E/B`，而是把 Gauss-law cleaning 也纳入同一个线性系统。这样做之后，更新矩阵 `M` 才能统一对角化。

notebook 直接把所有未知量拼成向量：

```python
fields_list = [Ex, Ey, Ez, Bx, By, Bz]
if divE_cleaning:
    fields_list.append(F)
if divB_cleaning:
    fields_list.append(G)
EBFG = zeros(dim, 1)
```

然后构造线性系统矩阵：

```python
M = zeros(dim)
for i in range(M.shape[0]):
    for j in range(M.shape[1]):
        M[i, j] = dEBFG_dt[i].coeff(EBFG[j], 1)
```

这和源码里的 `SpectralBaseAlgorithm` / `PsatdAlgorithm*` 逻辑是一一对应的。运行时代码不会真的做符号对角化，但它依赖这里导出的解析系数。

## 3. 线性系统的通解和特解

notebook 把解拆成两部分：

1. 齐次系统的通解。
2. 非齐次系统的特解。

对应的公式写得很清楚：

$$
\begin{bmatrix}
\boldsymbol{E}_h(t) \\
\boldsymbol{B}_h(t) \\
F_h(t) \\
G_h(t)
\end{bmatrix}
= e^{M (t-t_n)}
\begin{bmatrix}
\boldsymbol{E}(t_n) \\
\boldsymbol{B}(t_n) \\
F(t_n) \\
G(t_n)
\end{bmatrix}
$$

以及

$$
\begin{bmatrix}
\boldsymbol{E}_{nh}(t) \\
\boldsymbol{B}_{nh}(t) \\
F_{nh}(t) \\
G_{nh}(t)
\end{bmatrix}
= -\mu_0 c^2 e^{M t} \left(\int_{t_n}^t e^{-M s}
\begin{bmatrix}
\boldsymbol{J} \\
\boldsymbol{0} \\
\rho \\
0
\end{bmatrix}
ds\right)
$$

这里的物理逻辑是：

- 齐次部分描述无源的电磁波传播。
- 非齐次部分描述电流和电荷对场的驱动。

这也是为什么 PSATD 系数最终会分裂成两组：

- homogeneous 系数，控制 `E/B/F/G` 之间的传播耦合；
- non-homogeneous 系数，控制 `J/rho` 注入到场变量里的权重。

## 4. notebook 怎样处理源项时间依赖

notebook 把 `J` 和 `rho` 写成分段多项式。默认是 `J` 常量、`rho` 线性，但它也支持线性和二次扩展。

```python
Jx_c0 = sp.symbols(r"\gamma_{J_x}", real=True)
Jy_c0 = sp.symbols(r"\gamma_{J_y}", real=True)
Jz_c0 = sp.symbols(r"\gamma_{J_z}", real=True)
Jx = Jx_c0
Jy = Jy_c0
Jz = Jz_c0
if J_in_time == "linear":
    ...
if J_in_time == "quadratic":
    ...
```

`rho` 也是同样结构：

```python
if divE_cleaning:
    rho_c0 = sp.symbols(r"\gamma_{\rho}", real=True)
    rho = rho_c0
    if rho_in_time == "linear":
        rho_c1 = sp.symbols(r"\beta_{\rho}", real=True)
        rho += rho_c1 * (s - tn)
    if rho_in_time == "quadratic":
        ...
```

这一段和 `PsatdAlgorithmJRhom*` 的关系最直接。JRhom 的所有 `Y1-Y8`，本质上就是把这类时间多项式在一个子区间上积分之后得到的封闭形式。

## 5. 矩阵对角化：PSATD 系数的数学核心

notebook 接下来做的事很朴素，也很重：

1. 对 `M` 对角化。
2. 写出 `exp(MΔt)`。
3. 把特解积分算出来。
4. 抽取每个输出量对每个输入量和源项的系数。

```python
P, D = M.diagonalize()
invP = P ** (-1)
expD = exp(D)
check_diag(M, D, P, invP)
```

然后分别构造：

```python
P1 = P
D1 = D * (t - tn)
expW1 = P1 * expD1 * invP1

P2 = P
D2 = D * t
expW2 = P2 * expD2 * invP2
```

这说明系数推导并不是“猜一个更新式”，而是从线性 ODE 的精确解出发再化简。运行时代码里那些看似复杂的三角函数和零模极限，其实就是 `exp(MΔt)` 的解析展开结果。

## 6. 结果如何变成源码里的系数表

notebook 最后把齐次和非齐次部分分别展开成系数字典：

```python
coeff_h = dict()
for i in range(dim):
    for j in range(dim):
        key = (L[i], R[j])
        coeff_h[key] = (
            EBFG_h_new[i]
            .coeff(EBFG[j], 1)
            .expand()
            .simplify()
            .rewrite(cos)
            .trigsimp()
            .simplify()
        )
```

非齐次部分也是类似，只不过右端不是场变量，而是源项系数：

```python
coeff_nh = dict()
for i in range(len(L)):
    for j in range(len(R)):
        key = (L[i], R[j])
        coeff_nh[key] = (
            EBFG_nh_new[i]
            .expand()
            .coeff(cs[j], 1)
            .expand()
            .simplify()
            .rewrite(cos)
            .trigsimp()
            .simplify()
        )
```

这就是为什么在 WarpX 的源码里你会看到一大批名字像 `C`, `S_ck`, `T2`, `X1-X4`, `Y1-Y8` 的标量系数。它们不是手写魔法常数，而是这张系数表的程序化压缩版。

## 7. 和运行时代码的对照关系

这个 notebook 对运行时代码最直接的贡献有三类：

1. `PsatdAlgorithmGalilean.cpp`
   - 标准和 Galilean PSATD 的 `C/S_ck/T2/X1-X4` 来源。
   - `update_with_rho` 的重构方式。
   - `current correction` 的源项重组。

2. `PsatdAlgorithmJRhomFirstOrder.cpp` / `PsatdAlgorithmJRhomSecondOrder.cpp`
   - `J/rho` 时间多项式积分。
   - `Y1-Y8` 以及相关特殊组合。

3. `explicit_em_pic.rst`
   - 文档里的公式并不是独立推导，而是这个 notebook 的摘要版。

所以读 PSATD 源码时，正确顺序不是先看 `cpp` 再猜公式，而是先在 notebook 里理解线性系统怎么被精确求解，再回到源码看系数如何被缓存、分支和复用。

## 8. 这一轮阅读应该记住的结论

- PSATD 的系数来源是一个带 `E/B/F/G` 的线性常微分方程组。
- 齐次项来自 `exp(MΔt)`，非齐次项来自 `∫ exp(-Ms) source(s) ds`。
- `J` 和 `rho` 的时间依赖决定了最终系数表的维度。
- `current correction`、`update_with_rho` 和 JRhom 不是零散功能，而是同一套解析解在不同物理约束下的不同投影。
- 只有把 notebook 和 `PsatdAlgorithm*` 源码一起看，PSATD 的实现才算真正闭合。

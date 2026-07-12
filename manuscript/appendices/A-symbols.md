# 附录 A：符号、时间层与源码变量

本附录服务于正文阅读和源码检索。公式中的符号采用连续模型或离散模型的常用记号；反引号中的名称则优先对应 WarpX 源码、输入文件或 diagnostics 输出中的实际字段。除特别说明外，SI 制单位适用，粒子权重 `w_p` 表示一个宏粒子代表的真实粒子数。

## A.1 连续模型符号

| 符号 | 含义 | 常见单位或类型 |
|---|---|---|
| $$s$$ | species 索引，例如 electron、ion、photon | 无量纲整数 |
| $$f_s(\mathbf{x},\mathbf{p},t)$$ | species $$s$$ 的相空间分布函数 | 依定义而定 |
| $$q_s,m_s$$ | species 电荷和静质量 | C、kg |
| $$\mathbf{x}=(x,y,z)$$ | 物理空间位置 | m |
| $$\mathbf{p}$$ | 物理动量 | kg m s$$^{-1}$$ |
| $$\mathbf{u}=\gamma\mathbf{v}$$ | 归一化动量；WarpX 粒子分量通常写作 `ux, uy, uz` | m s$$^{-1}$$ |
| $$\mathbf{v}$$ | 粒子速度 | m s$$^{-1}$$ |
| $$\gamma$$ | Lorentz 因子，$$\gamma=(1-v^2/c^2)^{-1/2}$$ | 无量纲 |
| $$c$$ | 真空光速 | m s$$^{-1}$$ |
| $$\mathbf{E},\mathbf{B}$$ | 电场和磁场 | V m$$^{-1}$$、T |
| $$\rho,\mathbf{J}$$ | 电荷密度和电流密度 | C m$$^{-3}$$、A m$$^{-2}$$ |
| $$\epsilon_0,\mu_0$$ | 真空介电常数和磁导率 | SI 常数 |
| $$w_p$$ | 宏粒子权重，代表的真实粒子数 | 无量纲或按模型定义 |
| $$S$$ | 粒子到网格的空间形函数 | 按离散归一化定义 |

## A.2 网格、时间层与离散量

| 符号 | 含义 | 在程序中的对应 |
|---|---|---|
| $$t^n$$ | 第 $$n$$ 个整数时间层 | `step`、`istep` |
| $$t^{n+1/2}$$ | 半时间层，常用于 leapfrog 电流或磁场 | `J^{n+1/2}` 等时间层语义 |
| $$\Delta t$$ | 时间步长 | `dt`、`warpx.const_dt` 或派生时间步长 |
| $$\Delta x,\Delta y,\Delta z$$ | 各方向网格间距 | `amr.n_cell`、几何 `cell_size` |
| $$i,j,k$$ | 网格单元或节点索引 | AMReX `IntVect` 分量 |
| $$\ell$$ | AMR level 索引，$$\ell=0$$ 为最粗层 | `lev`、`level` |
| $$r$$ | MPI rank 或 rank 索引 | `ParallelDescriptor::MyProc()` 等 |
| $$V_i$$ | 网格单元体积 | Cartesian 中常为 $$\Delta x\Delta y\Delta z$$ |
| $$\rho_i^n$$ | 单元/节点 $$i$$ 在时间层 $$n$$ 的电荷密度 | `rho`、`rho_fp`、`rho_buf` |
| $$\mathbf{J}_i^{n+1/2}$$ | 时间层 $$n+1/2$$ 的电流密度 | `current_fp`、`current_buf` |
| $$\nabla_h\cdot\mathbf{J}$$ | 离散散度 | 由 staggering 和差分 stencil 决定 |
| $$S_i(\mathbf{x}_p)$$ | 粒子位置对网格量 $$i$$ 的形函数值 | `ShapeFactors` 中的 shape 权重 |

## A.3 沉积、推进与场求解记号

| 符号或名称 | 含义 | 阅读提示 |
|---|---|---|
| $$\rho^n\rightarrow\mathbf{J}^{n+1/2}\rightarrow\rho^{n+1}$$ | 电荷守恒 current-deposition 主线的时间层关系 | 不能把 charge deposition 和 current deposition 当成同一个 kernel |
| `old` / `new` | 粒子在一个推进步或 segment 两端的形函数/位置状态 | Esirkepov、Villasenor kernel 中常见 |
| `relative_time` | 在同一步内取样粒子位置的相对时间参数 | 影响 source 的时间层，而不是额外推进粒子 |
| `icomp` | charge component 或时间层分量选择 | 需结合调用入口解释，不能只按名字猜测 |
| `depos_lev` | charge 沉积目标 AMR level | coarse-buffer 粒子可能直接沉积到 `lev-1` |
| `current_fp` | fine-patch current buffer | 主要对应 fine patch 粒子沉积 |
| `current_buf` | coarse-buffer current buffer | 后续还要经过同步/整理 |
| `rho_fp` / `rho_buf` | fine-patch / coarse-buffer charge buffer | 是 source route 的观测面，不等于最终 plotfile 字段 |
| `Direct` | 直接速度加权电流沉积 | 简单但不自动满足离散连续性方程 |
| `Esirkepov` | 基于轨迹与形函数差分的 charge-conserving current deposition | 重点看 density decomposition 和 prefix accumulation |
| `Villasenor` | 基于 cell crossing segment 的 charge-conserving current deposition | 重点看 crossing、segment 和局部 face flux |
| `Vay` | Vay current deposition / spectral 相关路径 | 常与 PSATD、current correction 组合讨论 |
| `FDTD` | 有限差分时域场求解器 | 依赖 staggered grid 和 CFL 限制 |
| `PSATD` | pseudo-spectral analytical time-domain 求解器 | 重点看谱空间系数、源项时间模型和周期边界假设 |
| `JRhom` | PSATD 的多次 $$J/\rho$$ 时间采样路径 | 不是多次粒子 push，而是同一轨迹的多时刻源项 |
| `PML` | 吸收边界层 | 通过 split-field 或等价谱推进吸收出射波 |

## A.4 诊断、文件与验证术语

| 名称 | 含义 |
|---|---|
| plotfile | WarpX/AMReX 网格和粒子状态的可重启或后处理输出 |
| openPMD | 粒子、网格或 reduced diagnostics 的结构化输出接口 |
| `diagNNNNNNN` | diagnostics 输出的迭代目录，例如 `diag1000000` |
| `reduced_diags` | 不保存完整场/粒子，而输出聚合标量或低维量的 diagnostics |
| `FieldProbe` | 沿指定几何路径采样场并做积分或线探针输出的诊断 |
| `BoundaryScrapingDiagnostics` | 记录穿过粒子边界的粒子及其统计量 |
| producer | 产生字段、粒子或 reduced output 的运行时路径 |
| consumer | 读取产物并执行物理、格式或性能断言的分析脚本 |
| physics gate | 对解析解、守恒量、谱或物理量的数值容差断言 |
| writer gate | 对文件、字段、维度、iteration、轴和有限非零数据的断言 |
| checksum gate | 对最终输出做确定性校验；不能自动等价为物理正确性 |
| reader-side analysis | 从已有 plotfile/openPMD 重新读取数据并验证合同的分析层 |

## A.5 常用缩写

| 缩写 | 全称 | 本书中的语境 |
|---|---|---|
| PIC | Particle-In-Cell | 粒子-网格数值方法 |
| AMR | Adaptive Mesh Refinement | 多层网格和 coarse/fine 同步 |
| CFL | Courant-Friedrichs-Lewy | 显式场推进稳定性限制 |
| NCI | Numerical Cherenkov Instability | boosted-frame / PSATD 中的数值不稳定性 |
| RZ | cylindrical geometry with azimuthal modes | WarpX 的轴对称/模态几何 |
| EB | Embedded Boundary | 嵌入边界和 cut-cell 几何 |
| MPI | Message Passing Interface | rank 间并行通信 |
| GPU | Graphics Processing Unit | device kernel 和 GPU memory 路径 |
| QED | Quantum Electrodynamics | 高场量子辐射和 pair-production 模型 |
| LWFA / PWFA | Laser / Plasma Wakefield Acceleration | 激光/束流驱动尾场应用 |

## A.6 使用规则

1. 看到 `rho`、`current_fp` 或 `current_buf` 时，先判断它属于 local kernel、level buffer、同步后场，还是最终 diagnostics 输出；同名物理量可能处于不同生命周期阶段。
2. 看到上标 $$n$$、$$n+1/2$$ 或 `relative_time` 时，先确认粒子位置、场、current 和 charge 是否处在同一个时间层；不能只根据变量名推断守恒性。
3. 看到 `analysis.py`、`analysis_default_regression.py` 或 checksum 时，先区分 physics、writer 和 checksum 三类 gate；本书第 8 章明确保留这三种证据等级的边界。
4. 看到 `lev`、`fine`、`coarse` 或 `buf` 时，先回到 AMR route 和同步顺序，再解释某个字段的数值意义。

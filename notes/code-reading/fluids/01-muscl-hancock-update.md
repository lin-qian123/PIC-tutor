# `WarpXFluidContainer::AdvectivePush_Muscl`：cold relativistic fluid 的 MUSCL-Hancock 更新

绑定源码：

- `../warpx/Source/Fluids/WarpXFluidContainer.cpp`
- `../warpx/Source/Fluids/MusclHancockUtils.H`

这一篇只看 advective term，不看 Lorentz source。当前 worktree 里，冷流体推进被明确拆成两段：

1. `GatherAndPush()` 负责 Lorentz source；
2. `AdvectivePush_Muscl()` 负责

$$
\partial_t U + \nabla\cdot F(U) = 0
$$

这一部分的守恒更新。

## 1. 守恒变量与局部速度

`N` 与 `NU` 都存在 nodal MultiFab 上。真正进入 advection 时，源码先把 `U` 从 `NU/N` 还原：

```cpp
amrex::Real Ux = (NUx_arr(i, j, k) / N_arr(i,j,k));
amrex::Real Uy = (NUy_arr(i, j, k) / N_arr(i,j,k));
amrex::Real Uz = (NUz_arr(i, j, k) / N_arr(i,j,k));
```

然后构造相对论因子：

```cpp
const amrex::Real gamma = std::sqrt(1.0_rt + (Ux*Ux + Uy*Uy + Uz*Uz)/c2 );
```

对应速度是

$$
V_\alpha = \frac{U_\alpha}{\gamma}.
$$

## 2. 第一阶段：用 limiter 预测 cell-edge half-step states

`AdvectivePush_Muscl()` 先为各个方向分配临时 edge states：

```cpp
amrex::MultiFab tmp_U_minus_x(..., 4, 1);
amrex::MultiFab tmp_U_plus_x (..., 4, 1);
...
```

四个分量对应：

- `0`: `N`
- `1`: `U_x`
- `2`: `U_y`
- `3`: `U_z`

接着在每个 cell 上计算 slope。当前 worktree 默认使用 `ave(...)` limiter：

```cpp
dU0x = ave( DownDx_N(N_arr,i,j,k), UpDx_N(N_arr,i,j,k) );
dU1x = ave( DownDx_U(N_arr,NUx_arr,Ux,i,j,k), UpDx_U(N_arr,NUx_arr,Ux,i,j,k) );
...
```

`MusclHancockUtils.H` 还同时提供了 `minmod`、`superbee` 等变体，但当前 `WarpXFluidContainer.cpp` 实际走的是 `ave` 这条 limiter。

## 3. Jacobian 线性化：源码直接按 primitive-like variables 写出 `Jx/Jy/Jz`

源码没有先抽象成通用 Riemann solver，而是在每个 cell 上直接构造 advective Jacobian 的关键项。例如 `x` 向：

```cpp
const amrex::Real Vx = Ux/gamma;
const amrex::Real J00x = Vx;
const amrex::Real J01x = N_arr(i,j,k)*(1/gamma)*(1-Vx*Vx/c2);
const amrex::Real J02x = -N_arr(i,j,k)*Uy*Ux*inv_c2_gamma3;
const amrex::Real J03x = -N_arr(i,j,k)*Uz*Ux*inv_c2_gamma3;
```

再用这些 Jacobian 项把局部斜率推进到 half step。

所以这里的 MUSCL-Hancock 不是“generic reconstruction + generic flux function”，而是把 relativistic cold-fluid Jacobian 明确写死在 kernel 里。

## 4. positivity limiter：只要 edge density 变负，就整方向清 slope

Half-step edge value 构造后，源码立即做 positivity limiting：

```cpp
positivity_limiter (U_plus_x, U_minus_x,  N_arr, i, j, k, box_x, Ux, Uy, Uz, 0);
```

注释已经写明：

- 若 `N_edge < 0`
- 则把该 cell / direction 的 slope 置零

这意味着 WarpX 的 fluid advection 在当前实现里把

$$
N \ge 0
$$

当作硬数值约束。

## 5. 第二阶段：Rusanov flux 更新守恒量

在 `MusclHancockUtils.H` 中，flux 使用的是 Rusanov 形式。

密度通量：

```cpp
amrex::Real flux_N (..., amrex::Real Vm, amrex::Real Vp)
{
    const amrex::Real c = std::max( std::abs(Vm) , std::abs(Vp) );
    return 0.5_rt*(Vm*Um(i,j,k,0) + Vp*Up(i,j,k,0))
         - (0.5_rt*c)*(Up(i,j,k,0) - Um(i,j,k,0));
}
```

随后 `AdvectivePush_Muscl()` 在第二轮 tile loop 里，用 `dF(...)` 把各方向通量差回写到 `N/NU`：

```cpp
N_arr(i,j,k) = N_arr(i,j,k)  - dt_over_dx*dF(U_minus_x,U_plus_x,i,j,k,clight,0,0) - ...;
NUx_arr(i,j,k) = NUx_arr(i,j,k) - dt_over_dx*dF(...,1,0) - ...;
...
```

这一步才是真正的 conservative update。

## 6. 非周期边界：先局部镜像 guard，再统一 `FillBoundary`

在进入 MUSCL 更新前，`ApplyBcFluidsAndComms()` 先对非周期边界的第一层 guard cell 做局部镜像复制：

```cpp
if ( (periodic_directions[2] != 1) && (k==domain.bigEnd(2)+1) ){
    N_arr(i,j,k) = N_arr(i,j,k-2);
    NUx_arr(i,j,k) = NUx_arr(i,j,k-2);
    ...
}
```

然后再统一 `FillBoundary(...)`。这说明 fluid boundary contract 不是单纯依赖 AMReX periodic fill。

## 7. RZ/RCYLINDER/RSPHERE：不是直接复用 Cartesian 通量

当前 worktree 对非 Cartesian 流体做了两层额外处理。

### 7.1 几何源项单独拆成 `centrifugal_source_rz()`

RZ / RCYLINDER / RSPHERE 下，源码先独立加入曲率项，而且用 SSP-RK3 而不是简单欧拉：

```cpp
const amrex::Real u_r_1     = F_r(r,u_r,u_theta,u_z,dt);
const amrex::Real u_theta_1 = F_theta(r,u_r,u_theta,u_z,dt);
...
```

### 7.2 通量更新改成几何面积/体积形式

RZ 分支里，源码显式写出体元 `Vij` 和径向/轴向面积 `S_A*`，再按几何守恒形式回写。

因此 current worktree 的非 Cartesian fluid 实现不是“把 Cartesian stencil 套到 RZ”，而是明确重写成几何守恒形式。

## 8. 当前 `Fluids/` 的数值边界

基于当前源码，`AdvectivePush_Muscl()` 的真实特点可以压成 5 点：

1. 它推进的是 cold relativistic fluid 的 conserved `N/NU`，不是一般 Euler 气体。
2. slope reconstruction 当前实际使用 `ave` limiter。
3. 数值通量当前使用 Rusanov。
4. density positivity 是硬约束。
5. 非 Cartesian 几何需要额外曲率源项和几何面积/体积修正。

下一篇只看这套 fluid state 怎样和 PIC 主场、外场 parser、moving window 与 hybrid 求解路径耦合。

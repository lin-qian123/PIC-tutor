# 07 Vay deposition D-field structure：temporary arrays、后处理重组与实现边界

绑定源码：

- `../warpx/Source/Particles/Deposition/CurrentDeposition.H`
- `../warpx/Source/Particles/WarpXParticleContainer.cpp`

前置阅读：

- `../notes/code-reading/particles/05-current-deposition-algorithms-near-amr-buffer.md`
- `../notes/code-reading/particles/06-charge-conserving-current-kernel-structures.md`

前两篇已经把 Direct、Esirkepov、Villasenor 在 AMR buffer 下的接口差异和 charge-conserving kernel 结构拆开了。Vay deposition 则是另一类实现：它既不是 Direct 那种直接把 \(q w_p \mathbf{v}/\Delta V\) 写到 `Jx/Jy/Jz`，也不是 Esirkepov/Villasenor 那种直接构造守恒 `J`。它先沉积一组中间量 `D`，再在第二个 kernel 里把这些量重组回三个方向。

## 1. 接口层就已经暴露出 Vay 的实现边界

`WarpXParticleContainer::DepositCurrent()` 对 Vay 的分派是：

```cpp
if (push_type == PushType::Implicit) {
    WARPX_ABORT_WITH_MESSAGE("The Vay algorithm cannot be used with implicit algorithm.");
}
doVayDepositionShapeN<...>(
    GetPosition, wp.dataPtr() + offset, uxp.dataPtr() + offset,
    uyp.dataPtr() + offset, uzp.dataPtr() + offset, ion_lev,
    jx_fab, jy_fab, jz_fab, np_to_deposit, dt, relative_time, dinv, xyzmin, lo, q, ...);
```

源码位置：`../warpx/Source/Particles/WarpXParticleContainer.cpp:836-862`。

这里有三条边界条件：

1. 不支持 implicit；
2. 不走 shared-memory current deposition；
3. 只在 3D / XZ 有实现，RZ、1D、RCYLINDER、RSPHERE 都直接 abort。

`CurrentDeposition.H` 内部的明确报错是：

- `Vay deposition not implemented in RZ geometry`
- `Vay deposition not implemented in 1D geometry`

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:2408-2417`。

因此，Vay deposition 当前是一个“显式、笛卡尔、非 shared-memory”的专门路径。

## 2. Vay 沉积的目标不是直接写 `J`，而是先写 `D`

函数注释直接写明：

```cpp
deposit D in real space and store the result in Dx_fab, Dy_fab, Dz_fab
```

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:2361-2363`。

这和 Direct / Esirkepov / Villasenor 的第一性区别是：

- 其他算法的接口语义是“把 current density 写进三个方向数组”；
- Vay 的接口语义是“先把一组 `D` 量写进 `Dx/Dy/Dz` 容器”。

虽然后续容器名字仍叫 `Dx_fab/Dy_fab/Dz_fab`，在 `DepositCurrent()` 的调用点上它们仍占用了 `jx_fab/jy_fab/jz_fab` 这组参数位，但从 kernel 语义上，它们已经不再是“普通 `Jx/Jy/Jz` 的直接沉积”。

## 3. Vay 的第一阶段：为 `D` 分配 temporary arrays

函数开头除了目标数组，还会额外分配一个临时 `temp_fab`：

```cpp
#if defined(WARPX_DIM_3D)
amrex::FArrayBox temp_fab{Dx_fab.box(), 4};
#elif defined(WARPX_DIM_XZ)
amrex::FArrayBox temp_fab{Dx_fab.box(), 2};
#endif
temp_fab.setVal<amrex::RunOn::Device>(0._rt);
amrex::Array4<amrex::Real> const& temp_arr = temp_fab.array();
```

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:2432-2440`。

这里已经能看出它和其他路径不一样：

- Direct / Esirkepov / Villasenor 都是在粒子 loop 内直接往最终输出数组累加；
- Vay 则多出一个额外的 device temporary buffer；
- 3D 需要 4 个临时分量，XZ 需要 2 个。

因此，Vay 不是单阶段 deposition，而是：

1. 粒子阶段写 temporary `D` 组合量；
2. box 级阶段再把 `temp_arr` 重组成三个方向。

## 4. Vay 仍然先构造 old/new shape，但用途不同

与 Esirkepov 类似，Vay 也会构造 old/new position 的 nodal shape：

```cpp
double sx_new[depos_order+1] = {0.};
double sx_old[depos_order+1] = {0.};
...
const int i_new = compute_shape_factor(sx_new, x_new);
const int i_old = compute_shape_factor(sx_old, x_old);
```

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:2483-2501,2514-2516`。

但和 Esirkepov 不同：

- 它不使用 `compute_shifted_shape_factor`；
- 不构造 `depos_order + 3` 的对齐数组；
- 不在单方向上做差分前缀累加。

Vay 只是把 old/new nodal weights 直接组合成若干乘积项，例如在 XZ 里：

```cpp
auto const sxn_szn = static_cast<amrex::Real>(sx_new[i] * sz_new[k]);
auto const sxo_szn = static_cast<amrex::Real>(sx_old[i] * sz_new[k]);
auto const sxn_szo = static_cast<amrex::Real>(sx_new[i] * sz_old[k]);
auto const sxo_szo = static_cast<amrex::Real>(sx_old[i] * sz_old[k]);
```

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:2533-2538`。

也就是说，Vay 用 old/new shape，但用途是生成交叉组合项，而不是生成 shape difference current。

## 5. Vay 的第一阶段本质上是在写“组合量”而不是直接写三个方向

在 XZ 情况下，若 old/new stencil 没有跨单元移动：

```cpp
amrex::Gpu::Atomic::AddNoRet(&temp_arr(..., 0),
    wq * invvol * invdt * (sxn_szn - sxo_szo));
amrex::Gpu::Atomic::AddNoRet(&temp_arr(..., 1),
    wq * invvol * invdt * (sxn_szo - sxo_szn));
```

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:2542-2546`。

而在 3D 情况下，它会写 4 个临时组合量：

```cpp
temp_arr(...,0) <- (sxn_syn_szn - sxo_syo_szo)
temp_arr(...,1) <- (sxn_syn_szo - sxo_syo_szn)
temp_arr(...,2) <- (sxn_syo_szn - sxo_syn_szo)
temp_arr(...,3) <- (sxo_syn_szn - sxn_syo_szo)
```

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:2605-2615`。

这些量都带有共同前因子：

$$
q \, \frac{1}{\Delta V} \, \frac{1}{\Delta t}.
$$

所以 Vay 的第一阶段不是“先沉积 `Jx` 再沉积 `Jy/Jz`”，而是在写一组 old/new shape 交叉差分的中间变量。

## 6. `Dy` 在第一阶段就部分写入，说明 `temp_arr` 不是简单缓存 `J`

在 XZ 路径里，除了 `temp_arr` 之外，源码还直接往 `Dy_arr` 写：

```cpp
amrex::Gpu::Atomic::AddNoRet(&Dy_arr(...),
    wqy * 0.25_rt * (sxn_szn + sxn_szo + sxo_szn + sxo_szo));
```

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:2549-2569`。

因此 `temp_arr` 不是简单的“先把所有电流缓存下来，后面再拷到 `J`”。更准确地说：

- out-of-plane 分量 `Dy` 已经在第一阶段按四个 old/new 组合平均完成了沉积；
- `temp_arr` 主要服务于其余需要重组的 `D`-field 组合量。

这说明 Vay 的临时数组语义不是通用 cache，而是算法特定的中间表示。

## 7. Vay 的第二阶段：从 `temp_arr` 重组回三个方向

粒子 loop 结束后，Vay 不会立即返回，而是再 launch 一个 box 级 `ParallelFor`。

3D 情况下：

```cpp
const amrex::Real t_a = temp_arr(i,j,k,0);
const amrex::Real t_b = temp_arr(i,j,k,1);
const amrex::Real t_c = temp_arr(i,j,k,2);
const amrex::Real t_d = temp_arr(i,j,k,3);
Dx_arr(i,j,k) += (1._rt/6._rt)*(2_rt*t_a       + t_b       + t_c - 2._rt*t_d);
Dy_arr(i,j,k) += (1._rt/6._rt)*(2_rt*t_a       + t_b - 2._rt*t_c       + t_d);
Dz_arr(i,j,k) += (1._rt/6._rt)*(2_rt*t_a - 2._rt*t_b       + t_c       + t_d);
```

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:2649-2657`。

XZ 情况下：

```cpp
Dx_arr(i,j,0) += 0.5_rt*(t_a + t_b);
Dz_arr(i,j,0) += 0.5_rt*(t_a - t_b);
```

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:2660-2665`。

这就是 Vay 与其他沉积算法最根本的结构区别：

- 其他路径：粒子 loop 内直接形成最终 `Jx/Jy/Jz`
- Vay：粒子 loop 只形成 `temp_arr` 中间量，真正的三个方向要靠第二阶段线性组合恢复

## 8. Vay 的 old/new stencil 不跨单元时，会走简化分支

源码对 “old/new leftmost index 是否相同” 做了专门分支：

- XZ：`if (i_new == i_old && k_new == k_old)`
- 3D：`if (i_new == i_old && j_new == j_old && k_new == k_old)`

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:2540,2603`。

如果 stencil 没变，它会把 old/new 组合项直接写到同一个 cell block；如果变了，才会把不同 old/new 组合项分别写到 `i_new/j_new/k_new` 和 `i_old/j_old/k_old` 对应的位置。

因此，Vay 并不是盲目把 4 项全域展开，而是根据 old/new stencil 是否移动做局部化分支。

## 9. 为什么说 Vay 与 Esirkepov / Villasenor 是“根本不同的一类”

现在可以把三类 current deposition 对比成：

1. **Direct**
   - 当前位置加 `relative_time`
   - 直接沉积 \(q w_p \mathbf{v}/\Delta V\)

2. **Esirkepov / Villasenor**
   - 显式满足离散连续性
   - 直接输出 charge-conserving `J`
   - 只是内部组织方式不同：shape-difference vs segment-loop

3. **Vay**
   - 先沉积 `D` 的中间组合量
   - 再通过第二阶段 box kernel 重组为三个方向
   - 结构上属于“两阶段重组”算法，而不是“单阶段直接沉积 `J`”

所以 Vay 和其他三类的真正差异不是“用了不同权重”，而是“输出对象和执行拓扑都不同”。

## 10. Vay 与 AMR buffer 的关系

AMR coarse-fine buffer 对 Vay 仍然只改变外层几何解释：

- `depos_lev`
- coarse 化后的 `tilebox`
- coarse `dinv`
- coarse `xyzmin`

一旦进入 `doVayDepositionShapeN()`：

- 仍然先构造 old/new nodal shape；
- 仍然先写 `temp_arr`；
- 仍然用第二阶段 kernel 重组 `Dx/Dy/Dz`。

因此，AMR buffer 并没有把 Vay 改造成 Esirkepov/Villasenor 式的 charge-conserving current deposition；它只是让 Vay 的 `D`-field 两阶段重组在 coarse patch 几何上运行。

## 11. 当前实现边界

从源码直接可见，Vay deposition 当前有以下边界：

- 不支持 implicit；
- 不支持 RZ；
- 不支持 1D / RCYLINDER / RSPHERE；
- 不支持 shared-memory current deposition；
- mass matrices 路径也直接禁止 Vay。

对应源码位置：

- `WarpXParticleContainer.cpp:612-613`
- `WarpXParticleContainer.cpp:836-838`
- `WarpXParticleContainer.cpp:1132-1133`
- `CurrentDeposition.H:2408-2417`

这说明它是一个功能明确但适用范围受限的专用沉积路径。

## 12. 下一步入口

这一层之后，粒子沉积主线再往下最自然的两条路是：

1. 回到 `Particles/` 上层，补 `particle class / attribute map`，把 `x_n`、`ux_n`、`opticalDepthQSR`、`prev_x` 等属性系统整体梳理出来。
2. 转去 `Diagnostics/`，看 `current_fp/current_buf/rho_fp/rho_buf` 最终怎样被多层 diagnostics 消费。

## 13. 当前最稳定的 regression 入口

`Examples/Tests/vay_deposition/` 当前只有 2D 和 3D 两条 active 基准，但它们共享同一个非常直接的验证合同：

1. 输入同时打开
   - `algo.current_deposition = vay`
   - `algo.maxwell_solver = psatd`
   - `warpx.grid_type = collocated`
2. 只放两颗等质量、等权重、反号的 `SingleParticle`
3. full diagnostics 显式输出 `rho` 与 `divE`
4. `analysis.py` 最后只检查

$$
\frac{\max | \nabla\cdot E - \rho/\epsilon_0 |}{\max |\rho/\epsilon_0|} < 10^{-3}.
$$

因此这组 regression 真正验证的不是：

- 单粒子轨道几何
- 电磁波传播色散
- 或某个解析场解

而是更窄也更关键的一点：

- Vay deposition 经过 `D`-field 两阶段重组之后
- 最终写出的 `J/rho`
- 是否仍足以让离散 Gauss 定律在实际推进后保持到 `1e-3` 级别

这和 Langmuir `..._vay_deposition` 变体互补：

- Langmuir 家族验证 “Vay deposition 放进完整等离子体振荡问题后，解析场解和 charge conservation 还成立”
- `Examples/Tests/vay_deposition/` 则验证 “最小两粒子骨架下，Vay deposition 自身的离散守恒合同成立”

# Parallelization 04: `WarpXComm_K.H`、`MFIter`、`ParallelFor` 与执行模型

绑定源码：

- `../warpx/Source/Parallelization/WarpXComm.cpp`
- `../warpx/Source/Parallelization/WarpXComm_K.H`
- `../warpx/Source/WarpX.H`

## 1. 这一层要回答什么

前四篇并行 / AMR 笔记已经把：

1. guard-cell 预算；
2. coarse-fine source 同步；
3. regrid / load balance；
4. substitution / transition zone

这些“做什么”讲清楚了。

但要真正读懂 WarpX 的并行层，还必须回答“它是怎么执行的”：

- `WarpXComm_K.H` 里的 device kernel 为什么写成一堆 `AMREX_GPU_DEVICE` 小函数；
- `WarpXComm.cpp` 为什么几乎处处都是 `MFIter + Array4 + ParallelFor`；
- `TilingIfNotGPU()`、`Gpu::notInLaunchRegion()`、`AMREX_USE_OMP` 的组合到底在控制什么；
- `FillBoundary` / `ParallelCopy` / `ParallelAdd` 为什么有 `do_single_precision_comms`、`nowait/finish`、`nodal_sync` 这些分支。

这一篇讲的是执行模型，不再重新解释 coarse-fine 物理意义。

## 2. `WarpXComm_K.H` 的角色：把“单点算子”从遍历逻辑里剥离出去

`WarpXComm_K.H` 不是独立模块，而是 `WarpXComm.cpp` 的 device-kernel 头文件。它的基本风格是：

- 在头文件里放 `AMREX_GPU_DEVICE AMREX_FORCE_INLINE` 小函数；
- 每个函数只负责“一个 `(i,j,k)` 点上的计算”；
- box/tile 遍历、数组抓取、OpenMP/GPU 调度放在 `.cpp` 外层完成。

这样做的直接好处是：

1. 同一个点值算子可以被多个 `ParallelFor` 调用；
2. 编译器能把小函数内联进 GPU kernel；
3. `.cpp` 层保留对 `MultiFab` / `MFIter` / 通信语义的控制，不把容器和数值公式混在一起。

因此，`WarpXComm_K.H` 的设计边界很清楚：它不是“通信层头文件”，而是通信/插值层的 **pointwise arithmetic library**。

## 3. `warpx_interp` 不是一个函数，而是一组按数据布局分层的内核

`WarpXComm_K.H` 里有多组重载的 `warpx_interp`，每组负责不同的数据布局问题：

1. coarse-to-fine 插值，fine/coarse/aux 同 stagger；
2. coarse/fine/staggered-to-nodal 的 substitution 版；
3. fine staggered 到 nodal 的简单平均版；
4. 任意阶 Fornberg 系数支持的 nodal <-> staggered centering 版。

这几组重载意味着 WarpX 并不是把所有 AMR / gather 相关插值都塞进一个“大而全 kernel”，而是按：

- coarse-fine replacement
- stagger conversion
- finite-order centering

三类任务分层。

## 4. 同-stagger 版本：`arr_aux = arr_fine + res`

最简单的 AMR substitution kernel 在 `WarpXComm_K.H` 前半段：

```cpp
arr_aux(j,k,l) = arr_fine(j,k,l) + res;
```

这里的 `res` 由 coarse residual 的线性权重插值累加得到。

执行层面上，这个 kernel 的特点是：

- 输入只有 `Array4`；
- coarse array 超出 ghost cell 的访问统一零填充；
- refinement ratio 与 staggering 都在 kernel 内局部解释；
- 不依赖 `MultiFab` 的高层方法。

所以它是一个纯 device-side stencil kernel，而不是容器方法。

## 5. stag-to-nodal substitution 版本：`tmp + (fine - coarse)`

更复杂的 AMR gather 路径在另一个重载里写成：

```cpp
arr_aux(j,k,l) = tmp + (fine - coarse);
```

执行层面上，这个式子很重要，因为它说明 WarpX 在 kernel 级别就把计算拆成了三段：

1. `tmp`：parent `aux` 到 nodal；
2. `coarse`：current coarse patch 到 nodal；
3. `fine`：current fine patch 到 nodal。

这样做的结果是：

- coarse-fine substitution
- stagger-to-nodal gather preparation

可以在一个 `ParallelFor` 里一次完成，而不需要先额外生成多张中间 nodal `MultiFab`。

这就是 WarpX 在 GPU 路径里减少全局内存往返的一种典型做法。

## 6. 任意阶 centering 版本：Fornberg 系数完全留在 kernel 参数里

`WarpXComm_K.H` 后半段的 `warpx_interp(...)` 是最通用的一版，用于 nodal <-> staggered 的 arbitrary-order centering。

它的核心特征是：

1. `dst_stag` / `src_stag` 决定当前是 nodal->staggered 还是 staggered->nodal；
2. `nox/noy/noz` 决定各方向的 centering 阶数；
3. `stencil_coeffs_*` 通过裸指针传进 kernel；
4. 内核内部只做局部零填充、索引范围计算和系数加权。

这说明 WarpX 把：

- 系数构造
- kernel 调度
- 点值插值

三层分得很开。`WarpXComm_K.H` 只关心第三层。

## 7. `WarpXComm.cpp` 的通用外壳：`MFIter -> Array4 -> ParallelFor`

`WarpXComm.cpp` 几乎反复使用同一个三段模式：

1. `for (MFIter mfi(..., TilingIfNotGPU()); mfi.isValid(); ++mfi)`
2. `Array4<Real>` / `Array4<Real const>` 抓出 tile 上的视图
3. `amrex::ParallelFor(...)` 调 device lambda

例如最早的 current centering helper 就是：

```cpp
for (MFIter mfi(dst, TilingIfNotGPU()); mfi.isValid(); ++mfi)
{
    const Box bx = mfi.growntilebox();
    auto const& src_arr = src.const_array(mfi);
    auto const& dst_arr = dst.array(mfi);
    amrex::ParallelFor(bx, [=] AMREX_GPU_DEVICE (...) noexcept
    {
        warpx_interp(...);
    });
}
```

源码位置：`../warpx/Source/Parallelization/WarpXComm.cpp:95-112`。

这个模式在：

- `UpdateCurrentNodalToStag`
- `UpdateAuxilaryDataStagToNodal`
- `UpdateAuxilaryDataSameType`
- `OwnerMask` 去重路径

里反复出现。

因此，WarpX 的执行模型不是“每个功能自己决定怎么 launch kernel”，而是极强地统一在 `MFIter + Array4 + ParallelFor` 模板上。

## 8. 为什么是 `TilingIfNotGPU()`

WarpX 在很多地方用：

```cpp
MFIter(..., TilingIfNotGPU())
```

而不是无条件 tile 或无条件不 tile。语义是：

- **CPU**：启用 tiling，让 OpenMP 线程在更小 tile 上工作，改善缓存局部性；
- **GPU**：通常不再额外 tile，因为 GPU launch 已经按 box 级 kernel 展开，额外 tiling 未必有利。

因此 `TilingIfNotGPU()` 是 WarpX/AMReX 常见的 portability 折中：同一段上层代码同时服务 CPU 和 GPU，但不强迫两端采用相同 tile 粒度。

## 9. `#pragma omp parallel if (Gpu::notInLaunchRegion())` 的含义

`WarpXComm.cpp` 经常把 `MFIter` 循环放在：

```cpp
#ifdef AMREX_USE_OMP
#pragma omp parallel if (Gpu::notInLaunchRegion())
#endif
```

下面。

这表示：

- 若当前不是 GPU launch region，则允许 OpenMP 并行化外层 tile 循环；
- 若当前是 GPU 路径，则避免再在主机侧套一层 OpenMP 并行。

这是一种很典型的 AMReX 双栈写法：同一份源码同时支持

- host-side tiled OpenMP
- device-side `ParallelFor`

但不会把两者叠在一起造成混乱。

## 10. `Array4` 是真正传进 kernel 的 ABI

WarpX 并不会把 `MultiFab` 直接传进 device lambda，而是先用：

- `array(mfi)`
- `const_array(mfi)`
- `arrays()`
- `const_arrays()`

拿到 `Array4` 或 array-of-`Array4` 视图。

这样做的原因是：

1. `Array4` 是轻量级视图，可以直接按值 capture 到 GPU lambda；
2. `MultiFab` 本身过重，也不适合作为 device-side ABI；
3. array-of-`Array4` 还能服务像 `OwnerMask` 那种多 box 同时访问的内核。

因此，`Array4` 才是 WarpX 并行 kernel 真实依赖的数据接口层。

## 11. `ParallelFor` 的三种常见形态

在这部分源码里，可以看到三种常见 launch 方式。

### 11.1 单 box

```cpp
amrex::ParallelFor(bx, [=] AMREX_GPU_DEVICE (...) noexcept { ... });
```

适合单分量或单数组逻辑。

### 11.2 多 box 同时 launch

```cpp
amrex::ParallelFor(Box(ex_aux), Box(ey_aux), Box(ez_aux), ... );
```

适合 `E/B` 三分量同时处理，避免写三个外层循环。

### 11.3 MultiFab + ncomp

```cpp
amrex::ParallelFor(fine_lev_cp, IntVect(0), ncomp,
[=] AMREX_GPU_DEVICE (int bno, int i, int j, int k, int n) { ... });
```

适合像 `OwnerMask` 去重这种：

- 需要 box 编号 `bno`
- 需要 component `n`
- 需要跨所有 FAB 的并行处理

这说明 WarpX 的 `ParallelFor` 并不是单一风格，而是按数据访问形态选 launch 形式。

## 12. `OwnerMask` 去重也走 device kernel，而不是 host-side patch-up

`SyncCurrent()` / `SyncRho()` 在 coarse-fine 回灌后，用 `OwnerMask` 去重：

```cpp
auto owner_mask = amrex::OwnerMask(fine_lev_cp, period);
auto const& mma = owner_mask->const_arrays();
auto const& sma = fine_lev_cp.const_arrays();
auto const& dma = J_fp[lev][Direction{idim}]->arrays();
amrex::ParallelFor(fine_lev_cp, IntVect(0), ncomp,
[=] AMREX_GPU_DEVICE (int bno, int i, int j, int k, int n)
{
    if (mma[bno](i,j,k) && sma[bno](i,j,k,n) != 0.0_rt) {
        dma[bno](i,j,k,n) += sma[bno](i,j,k,n);
    }
});
```

源码位置：`../warpx/Source/Parallelization/WarpXComm.cpp:1287-1299`。

这一段很能说明 WarpX 的风格：

- overlap 去重不是 host 端逐 box 修补；
- 而是先把 `OwnerMask` 也转成 `Array4` 视图；
- 再用 MultiFab 级 `ParallelFor` 一次完成。

也就是说，连“稀疏条件加法”这种逻辑也尽量保持 device-friendly。

## 13. `FillBoundary` 的双分支：AMReX 原生 nowait 路径 vs 单精度通信包装

`FillBoundaryE/B` 的内部结构揭示了另一个执行层分叉：

### 13.1 `do_single_precision_comms == true`

走 `ablastr::utils::communication::FillBoundary(...)` 包装层，一张 `MultiFab` 一张 `MultiFab` 处理。

### 13.2 否则

走 AMReX 原生：

```cpp
amrex::FillBoundaryAndSync_nowait(vec_mf, period);
amrex::FillBoundaryAndSync_finish(vec_mf);
```

或

```cpp
amrex::FillBoundary_nowait(vec_mf, period);
amrex::FillBoundary_finish(vec_mf);
```

这说明 WarpX 不只是抽象地“调用 FillBoundary”，而是根据通信精度需求决定：

- 是否使用自家通信包装；
- 是否能走更紧凑的 AMReX batched vector-of-MultiFab 路径。

## 14. `nodal_sync` 不是装饰参数，而是同步语义选择器

在 `FillBoundaryE/B` 里，若 `nodal_sync` 为真，会走：

- `FillBoundaryAndSync_nowait`
- `FillBoundaryAndSync_finish`

否则只走：

- `FillBoundary_nowait`
- `FillBoundary_finish`

区别在于：

- `FillBoundary` 只填 ghost cells；
- `FillBoundaryAndSync` 还要对 nodal overlap 做同步。

因此，WarpX 在调用侧显式决定：

- 当前只需要 ghost exchange
- 还是需要 nodal ownership reconciliation

这与前面 `OwnerMask` 去重的思路是一致的。

## 15. `m_safe_guard_cells`：执行模型里的“多做一点，换确定性”

多处 `FillBoundary*` 都写成：

```cpp
const amrex::IntVect nghost = (m_safe_guard_cells) ? mf[i]->nGrowVect() : ng;
```

这表示 WarpX 有一个很明确的执行层开关：

- 若追求最小通信量，只交换调用者要求的 `ng`；
- 若要“安全 guard cells”，则直接交换所有已分配 guard cells。

因此，`m_safe_guard_cells` 不是物理模型参数，而是 execution-policy 参数：用额外通信换更稳妥的后续 kernel 前提。

## 16. PML、平均场和 coarse patch 例外分支说明执行模型并不完全统一

虽然 `WarpXComm.cpp` 的大框架高度统一，但仍然保留了一些重要例外：

- PML 先 `Exchange`，再 `FillBoundary`
- RZ + FFT 下走 `pml_rz->FillBoundary*`
- averaged Galilean PSATD 与 PML 组合直接 `ABORT`
- `FillBoundaryAux` 只遍历到 `finest_level-1`

这些分支说明 WarpX 的执行模型是“统一骨架 + solver-specific exceptions”，不能误读成一个无条件适用的单模板。

## 17. 当前这一层的结论

`Parallelization` 模块在执行模型上有四个稳定特征：

1. `WarpXComm_K.H` 负责点值 kernel，`WarpXComm.cpp` 负责 box/tile/communication 调度；
2. 外层统一使用 `MFIter + Array4 + ParallelFor` 模式；
3. CPU/GPU 双栈通过 `TilingIfNotGPU()`、OpenMP 条件并行和 `AMREX_GPU_DEVICE` lambda 统一；
4. 通信层再按 `do_single_precision_comms`、`nodal_sync`、`m_safe_guard_cells` 等策略开关分支。

因此，WarpX 的 GPU portability 不是“把 kernel 改成 CUDA 就行”，而是靠这套分层结构维持的：

`container iteration -> lightweight views -> pointwise kernels -> communication policy switches`

## 18. 下一步应该读哪里

当前并行层已经把：

- coarse-fine 物理结构
- kernel 执行模型

都搭起来了。更自然的下一步有两条：

1. 回到 `Particles/Gather` / `Particles/Deposition`，把 `aux` / masks / partition 继续打穿到具体粒子 kernel；
2. 转去 `Diagnostics/`，看看这些 multi-level field / particle containers 如何被 diagnostics 消费。

当前更优先的是第 1 条，因为 `Boundary / AMR` 与粒子 gather/deposition 之间还差最后一层闭环。

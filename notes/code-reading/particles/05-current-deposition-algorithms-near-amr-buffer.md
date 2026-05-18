# 05 current deposition algorithms near AMR buffer：Villasenor、Vay 与 implicit charge-conserving 的差异

绑定源码：

- `../warpx/Source/Particles/WarpXParticleContainer.cpp`
- `../warpx/Source/Particles/Deposition/CurrentDeposition.H`

前置阅读：

- `../notes/code-reading/particles/04-amr-gather-deposition-buffers.md`

上一篇已经说明，AMR transition-zone 粒子会被 `PartitionParticlesInBuffers()` 重排，然后通过 `depos_lev = lev-1` 直接沉到 `current_buf`。本文继续回答另一个问题：一旦进入 buffer 路径，Villasenor、Vay、Esirkepov implicit 和 Direct implicit 到底还有哪些算法差异？

结论先写在前面：

1. 对 AMR buffer 而言，所有 current deposition 算法共享同一套 level 几何解释：`depos_lev`、coarsened tilebox、`dinv`、`xyzmin`、`domain_double`、`do_cropping`。
2. 差异不在 coarse-fine 入口，而在每种算法如何重建 old/new/mid 轨迹、是否 charge-conserving、是否需要显式 `relative_time`、是否支持 implicit。
3. 因此，AMR buffer 是“几何层复用”，不是“沉积算法层分叉”。

## 1. 所有算法先共享同一个 buffer 几何外壳

无论后面选哪种 deposition 算法，`WarpXParticleContainer::DepositCurrent()` 一开始都统一做四件事：

```cpp
if (lev == depos_lev) {
    tilebox = pti.tilebox();
} else {
    const IntVect& ref_ratio = WarpX::RefRatio(depos_lev);
    tilebox = amrex::coarsen(pti.tilebox(),ref_ratio);
}
tilebox.grow(ng_J);
const amrex::XDim3 dinv = WarpX::InvCellSize(std::max(depos_lev,0));
const amrex::XDim3 xyzmin = WarpX::LowerCorner(tilebox, depos_lev, 0.5_rt*dt);
```

源码位置：`../warpx/Source/Particles/WarpXParticleContainer.cpp:462-474,517`。

同时还会基于 `depos_lev` 构造：

- `domain_box = Geom(depos_lev).Domain()`
- `domain_double`
- `do_cropping`

源码位置：`../warpx/Source/Particles/WarpXParticleContainer.cpp:519-544`。

所以只要粒子被分到 `current_buf`，后续所有算法都是在 coarse 化后的 patch 几何上解释它的轨迹，区别只在“如何从粒子状态恢复轨迹并沉积”。

## 2. 显式 Villasenor：从当前位置和 `relative_time` 反推出 old/new 端点

显式 Villasenor 入口：

```cpp
doVillasenorDepositionShapeNExplicit<...>(
    GetPosition, wp.dataPtr() + offset,
    uxp.dataPtr() + offset, uyp.dataPtr() + offset, uzp.dataPtr() + offset, ion_lev,
    jx_arr, jy_arr, jz_arr, np_to_deposit, dt, relative_time, dinv, xyzmin,
    domain_double, do_cropping, lo, q, ...);
```

源码位置：`../warpx/Source/Particles/WarpXParticleContainer.cpp:811-833`。

它首先使用当前粒子位置和 `relative_time` 重建一步轨迹：

```cpp
amrex::Real const xp_new = xp + (relative_time + 0.5_rt*dt)*uxp[ip]*gaminv;
amrex::Real const xp_old = xp_new - dt*uxp[ip]*gaminv;
```

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:2236-2241`。

然后把这对 `old/new` 端点交给 `VillasenorDepositionShapeNKernel`。这意味着：

- 显式 Villasenor 依赖 `relative_time`；
- 但它不需要单独保存 `x_n` 或 `u_n`；
- 轨迹是从当前半步动量和一步长度直接回推出来的。

对 AMR buffer 而言，这条路径只是把 `xyzmin` 和 `domain_double` 改成 coarse patch 版本，其余逻辑不变。

## 3. 隐式 Villasenor：不再用 `relative_time`，而是显式使用 `x_n`、`u_n` 和 `u_{n+1/2}`

隐式 Villasenor 入口：

```cpp
doVillasenorDepositionShapeNImplicit<...>(
    xp_n_data, yp_n_data, zp_n_data,
    GetPosition, wp.dataPtr() + offset,
    uxp_n.dataPtr() + offset, uyp_n.dataPtr() + offset, uzp_n.dataPtr() + offset,
    uxp.dataPtr() + offset, uyp.dataPtr() + offset, uzp.dataPtr() + offset, ion_lev,
    jx_arr, jy_arr, jz_arr, np_to_deposit, dt, dinv, xyzmin, domain_double, do_cropping, lo, q, ...);
```

源码位置：`../warpx/Source/Particles/WarpXParticleContainer.cpp:776-805`。

它和显式路径最本质的差异是：

- 不再传 `relative_time`
- 直接传 `x_n`
- 同时传 `u_n` 和 `u_{n+1/2}`

kernel 内部先取当前位置 `x_{n+1/2}`，再重建：

```cpp
amrex::ParticleReal const xp_np1 = 2._prt*xp_nph - xp_n;
```

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:2347-2350`。

并通过

```cpp
const amrex::ParticleReal gaminv = GetImplicitGammaInverse(uxp_n[ip], ..., uxp_nph[ip], ...);
```

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:2332-2335`。

得到隐式平均 `gamma^{-1}`。因此，隐式 Villasenor 的 AMR buffer 路径和显式相比，区别不在 coarse-fine，而在时间层恢复方式：

- 显式：`current position + relative_time + dt`
- 隐式：`x_n + x_{n+1/2} + u_n + u_{n+1/2}`

## 4. Esirkepov implicit：同样依赖 `x_n` 和 `u_n/u_{n+1/2}`，但数学不是按 segment deposition

隐式 Esirkepov 入口：

```cpp
doChargeConservingDepositionShapeNImplicit<...>(
    xp_n_data, yp_n_data, zp_n_data,
    GetPosition, wp.dataPtr() + offset,
    uxp_n.dataPtr() + offset, uyp_n.dataPtr() + offset, uzp_n.dataPtr() + offset,
    uxp.dataPtr() + offset, uyp.dataPtr() + offset, uzp.dataPtr() + offset, ion_lev,
    jx_arr, jy_arr, jz_arr, np_to_deposit, dt, dinv, xyzmin, domain_double, do_cropping, lo, q, ...);
```

源码位置：`../warpx/Source/Particles/WarpXParticleContainer.cpp:719-748`。

它在时间层恢复上与隐式 Villasenor 很像：

- 读 `x_n`
- 从 `GetPosition()` 取 `x_{n+1/2}`
- 用 `xp_np1 = 2*x_{n+1/2} - x_n`
- 用 `GetImplicitGammaInverse(...)` 恢复隐式平均 `\gamma^{-1}`

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:1153-1183`。

但后面的数学完全不同。Esirkepov implicit 不走 Villasenor 那种“按 cell crossing 分段”路径，而是继续沿用 old/new shape 差分和 charge-conserving reconstruction。因此：

- 它和隐式 Villasenor 一样共享 AMR buffer 几何和边界裁剪；
- 但守恒电流的构造方式仍然是 Esirkepov 体系，而不是 segment-by-segment。

## 5. Vay deposition：显式-only，而且接口层就拒绝 implicit

Vay 入口非常直接：

```cpp
if (push_type == PushType::Implicit) {
    WARPX_ABORT_WITH_MESSAGE("The Vay algorithm cannot be used with implicit algorithm.");
}
doVayDepositionShapeN<...>(..., np_to_deposit, dt, relative_time, dinv, xyzmin, lo, q, ...);
```

源码位置：`../warpx/Source/Particles/WarpXParticleContainer.cpp:837-862`。

这里两个事实很重要：

1. Vay deposition 在 AMR buffer 路径上照样能工作，因为它同样接受 `depos_lev` 导出的 `dinv/xyzmin`；
2. 但它根本不支持 implicit，所以 coarse-fine buffer 下也不可能出现“implicit Vay”这条支线。

因此，若用户同时选择了：

- AMR coarse-fine buffer
- `current_deposition_algo = Vay`

这是合法组合；但若再叠加 implicit push，就会在接口层直接 abort。

## 6. `domain_double` / `do_cropping` 是 charge-conserving 路径的重要附加输入

从函数签名可以直接看出：

- 显式/隐式 Villasenor 都接收 `domain_double` 与 `do_cropping`
- 隐式 Esirkepov 也接收 `domain_double` 与 `do_cropping`
- Direct / Vay 的基础接口则只使用 `relative_time/dinv/xyzmin/lo`

对应源码位置：

- `doChargeConservingDepositionShapeNImplicit`：`CurrentDeposition.H:1117-1140`
- `doVillasenorDepositionShapeNExplicit`：`CurrentDeposition.H:2189-2209`
- `doVillasenorDepositionShapeNImplicit`：`CurrentDeposition.H:2281-2306`
- `doVayDepositionShapeN` 调用点：`WarpXParticleContainer.cpp:841-862`

这反映出一个真实差异：

- Villasenor / Esirkepov 这类 charge-conserving 路径需要明确裁剪粒子轨迹，确保吸收边界附近的段长与电流守恒一致；
- Vay / Direct 的接口更接近“在指定时间层按当前位置和速度沉积”。

因此，在 coarse-fine buffer 路径上，`domain_double` / `do_cropping` 不是 AMR 专用逻辑，但它会与 coarse patch 的边界几何绑定得更紧，因为 transition-zone 粒子本来就更接近 patch edge。

## 7. Villasenor kernel 的核心区别：按 crossing 分段

`CurrentDeposition.H` 对 Villasenor 的注释写得很直白：

- “deposit is done segment by segment”
- “segments are determined by cell crossings”
- “results in a tighter stencil”

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:2254-2258`。

而 `VillasenorDepositionShapeNKernel` 内部的主步骤也是：

1. 计算 `old/new` 端点
2. 计算总位移 `dxp/dyp/dzp`
3. 在 cell crossing 意义下决定 segments
4. 逐 segment 沉积 `wqx/wqy/wqz`

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:1544-1632`。

这说明在 AMR buffer 路径里，Villasenor 的“更紧 stencil”并不是因为 coarse-fine；而是它本来就通过 segment decomposition 组织沉积，只是这个分段轨迹现在被映射到了 coarse patch 坐标系。

## 8. 对 AMR buffer 来说，真正的分界线不是算法名，而是“需要哪些时间层信息”

从调用接口看，四类路径可以压缩成下面这张表：

| 路径 | 是否用 `relative_time` | 是否用 `x_n` | 是否用 `u_n`/`u_{n+1/2}` | 是否支持 implicit |
|---|---|---:|---:|---:|
| Direct explicit | 是 | 否 | 否 | 否 |
| Vay | 是 | 否 | 否 | 否 |
| Villasenor explicit | 是 | 否 | 否 | 否 |
| Villasenor implicit | 否 | 是 | 是 | 是 |
| Esirkepov implicit | 否 | 是 | 是 | 是 |

这张表比“是不是 buffer 粒子”更本质。因为 AMR buffer 只是决定：

- 用哪个 `depos_lev`
- 用哪个 patch 几何
- 最终沉到 `current_fp` 还是 `current_buf`

而时间层恢复方式完全由 deposition 算法和 push 类型决定。

## 9. 当前可得的最小结论

截至这一轮，可以把 AMR coarse-fine buffer 下的 current deposition 理解成两层正交结构：

1. **AMR 几何层**
   - `depos_lev`
   - coarsened tilebox
   - coarse `dinv/xyzmin`
   - `current_buf`

2. **沉积算法层**
   - Direct / Vay：依赖 `relative_time`
   - Villasenor explicit：依赖 `relative_time`，但按 crossing 分段
   - Villasenor implicit / Esirkepov implicit：依赖 `x_n`、`u_n`、`u_{n+1/2}`

两层相互组合，但并不相互改写。WarpX 没有为 coarse-fine buffer 另造一套 Villasenor、Vay 或 Esirkepov 数学；它只是把原本的 deposition 算法放到 coarse patch 几何里运行。

## 10. 下一步入口

这一层之后，最自然的接续有两条：

1. 继续把 `CurrentDeposition.H` 的 Villasenor / Esirkepov kernel 本体逐段拆开，特别是 cell crossings、old/new shape arrays 和 tighter stencil 的实际实现。
2. 转去 `Diagnostics/`，看 `current_fp/current_buf/rho_fp/rho_buf` 在同步合并后怎样进入 multi-level diagnostics 和 analysis。

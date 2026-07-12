# 36 charge deposition ABLASTR bridge and time levels：`DepositCharge()` 如何把旧/新时间层送进 `ChargeDeposition.H`

绑定源码：

- `../warpx/Source/Particles/WarpXParticleContainer.cpp`
- `../warpx/Source/ablastr/particles/DepositCharge.H`
- `../warpx/Source/Particles/Deposition/ChargeDeposition.H`

本笔记只补第 5 章里还不够清楚的一层：current deposition 的算法分叉已经很明确，但 charge deposition 更像一条“桥接合同”。它先在 `WarpXParticleContainer::DepositCharge()` 决定 shared-memory 还是普通路径、旧/新时间层与 coarse-fine 几何，再经 ABLASTR `deposit_charge(...)` 落到 `ChargeDeposition.H` 的具体 shape kernel。

## 1. `DepositCharge()` 的第一分叉不是算法，而是执行路径

`WarpXParticleContainer::DepositCharge()` 的第一层判断在
`../warpx/Source/Particles/WarpXParticleContainer.cpp:1514-1744,1745-1789`：

- `WarpX::do_shared_mem_charge_deposition = true`
  - 直接在 `WarpXParticleContainer.cpp` 内部分派 `doChargeDepositionSharedShapeN<1..4>()`
  - 进入 binning / shared tiles / tile-box max-size / GPU shared-memory 预算这套专门路径
- 否则
  - 调 `ablastr::particles::deposit_charge<WarpXParticleContainer>(...)`
  - 再由 ABLASTR 统一桥接到 `doChargeDepositionShapeN<1..4>()`

这说明 charge deposition 的主入口虽然和 current deposition 一样都在 `WarpXParticleContainer.cpp`，但“普通路径”的 kernel 调度并不留在 WarpX 容器层，而是先交给 ABLASTR 这一层通用封装。

## 2. `icomp` 决定沉到哪一个时间层，不只是 MultiFab 分量号

函数注释已经写明：

- `icomp = 0`
  - 沉旧值，`before particle push`
- `icomp = 1`
  - 沉新值，`after particle push`

对应源码在 `WarpXParticleContainer.cpp:1605-1607,1775-1776`：

```cpp
const amrex::Real dt = warpx.getdt(lev);
const amrex::Real time_shift_delta = (icomp == 0 ? 0.0_rt : dt);
const amrex::XDim3 xyzmin = WarpX::LowerCorner(tilebox, depos_lev, time_shift_delta);
```

这里关键点不是“多了一个 `if`”，而是 `xyzmin` 会因为 `icomp` 不同而带上不同的 Galilean time shift。也就是说，旧/新 `rho` component 不只是数组分量不同，而是连 tile 物理左下角的参考时间层都可能不同。

因此第 5 章里更准确的说法是：

1. `rho` 的两个 component 对应同一步内的旧/新时间层；
2. `DepositCharge()` 通过 `time_shift_delta` 把这两个时间层各自放到正确的物理坐标框架；
3. 后面的 shape kernel 只消费已经对齐好的 `xyzmin`，不再自己判断“当前是旧电荷还是新电荷”。

## 3. ABLASTR `deposit_charge(...)` 真正封装了什么

普通路径的核心桥接在
`../warpx/Source/ablastr/particles/DepositCharge.H:50-203`。

它实际封装了五件事。

### 3.1 把 WarpX 运行时 shape 压成统一的 `particle_shape`

```cpp
auto const[nox, noy, noz] = std::array<int, 3>{particle_shape, particle_shape, particle_shape};
```

这也解释了为什么调用点先 assert：

```cpp
AMREX_ALWAYS_ASSERT(WarpX::nox == WarpX::noy);
AMREX_ALWAYS_ASSERT(WarpX::nox == WarpX::noz);
```

也就是：普通 charge deposition 当前默认假定三个方向用同一阶数。

### 3.2 对 `depos_lev` / `rel_ref_ratio` 做 coarse-fine 合法性检查

```cpp
ABLASTR_ALWAYS_ASSERT_WITH_MESSAGE((depos_lev.value() == (lev-1)) ||
                                   (depos_lev.value() == (lev  )),
                                   "Deposition buffers only work for lev or lev-1");
```

这意味着 charge deposition buffer 并不是任意 level-to-level 的重映射，而只是：

- 沉回本 level
- 或沉到 `lev-1`

与第 5 章里 coarse-fine buffer 的总体描述一致。

### 3.3 在 CPU/GPU 上切换不同的暂存策略

ABLASTR 明确区分：

- GPU：
  - 直接 alias 原 `rho` MultiFab
  - `rho_fab` 指向真实目标数组
- CPU：
  - 先把 `local_rho` resize 成 tile-local FArrayBox
  - 置零
  - kernel 完成后再 `lockAdd(...)` 回真实 `rho`

对应源码：

```cpp
#ifdef AMREX_USE_GPU
amrex::MultiFab rhoi(*rho, amrex::make_alias, icomp*nc, nc);
auto & rho_fab = rhoi.get(pti);
#else
local_rho.resize(tb, nc);
local_rho.setVal(0.0);
auto & rho_fab = local_rho;
#endif
...
(*rho)[pti].lockAdd(local_rho, tb, tb, 0, icomp*nc, nc);
```

所以 `ChargeDeposition.H` 里看到的 `rho_fab` 并不总是“最终那张 `rho`”；在 CPU 路径上，它可能只是 thread-local 暂存。

### 3.4 守住 shape 与 guard-cell 的安全边界

ABLASTR 在 `DepositCharge.H:99-134` 再做了一次范围断言：

```cpp
ABLASTR_ALWAYS_ASSERT_WITH_MESSAGE(
    amrex::numParticlesOutOfRange(pti, range) == 0,
    "Particles shape does not fit within tile (CPU) or guard cells (GPU) used for charge deposition");
```

这说明 charge deposition 的 guard-cell 合同并没有完全下沉到 WarpX kernel；ABLASTR 桥接层本身就承担了一层“tile / guard 是否足够宽”的防线。

### 3.5 把 component 偏移统一封装成 `icomp*nc`

调用 kernel 时，真正看到的是一个已经偏移过的 alias 或 local FArrayBox：

- GPU alias：`make_alias, icomp*nc, nc`
- CPU 回写：`lockAdd(..., icomp*nc, nc)`

因此 `ChargeDeposition.H` 本体不需要再显式关心“旧分量还是新分量”；component 偏移在桥接层已经做完。

## 4. `ChargeDeposition.H` 的 kernel 在做什么

真正的 WarpX-specific shape kernel 在
`../warpx/Source/Particles/Deposition/ChargeDeposition.H:37-172`。

它本体非常直接，但有三个容易在正文里讲漏的事实。

### 4.1 电离态修正发生在沉积权重最前面

```cpp
amrex::Real wq = q*wp[ip]*invvol;
if (do_ionization){
    wq *= ion_lev[ip];
}
```

所以 field ionization species 的“有效电荷”不是在 species 层预先改写，而是在每次沉积时按粒子属性乘上 `ion_lev`。

### 4.2 `rho_type` 决定每个方向用 node 还是 cell 版 shape

```cpp
if (rho_type[0] == NODE) {
    i = compute_shape_factor(sx, x);
} else if (rho_type[0] == CELL) {
    i = compute_shape_factor(sx, x - 0.5_rt);
}
```

`y/z` 同理。也就是说，charge deposition 的 shape 不是单纯“拿一套 `S(x)` 到处乘”，而是会根据 `rho_fab.box().type()` 自动切换 node-centered 或 cell-centered 的局部坐标。

### 4.3 RZ 普通模态之外还会显式写入高阶方位模

在 `WARPX_DIM_RZ` 下，mode 0 写完之后还有：

```cpp
for (int imode=1 ; imode < n_rz_azimuthal_modes ; imode++) {
    amrex::Gpu::Atomic::AddNoRet(... real part ...);
    amrex::Gpu::Atomic::AddNoRet(... imag part ...);
    xy = xy*xy0;
}
```

因此 RZ charge deposition 不只是“把 Cartesian kernel 换成半径坐标”，而是会把

$$
e^{im\theta}
$$

对应的实部/虚部分量分别写入额外 component。

## 5. 这一层为什么值得单独记

如果只看 `ChargeDeposition.H`，容易误以为 charge deposition 只是：

1. 算 shape
2. 原子加到 `rho_arr`

但从整条调用链看，更准确的结构是：

```text
WarpXParticleContainer::DepositCharge
  -> 选择 shared-memory 或普通路径
  -> 决定 depos_lev / ref_ratio / icomp / xyzmin
  -> ABLASTR deposit_charge(...) 做 guard-check、CPU/GPU 暂存与 component 偏移
  -> ChargeDeposition.H 做 shape-factor 和原子加
```

对第 5 章来说，这层桥接合同很重要，因为它把三个原本容易混在一起的问题拆开了：

1. **时间层问题**：`icomp` 与 `time_shift_delta`
2. **几何问题**：`depos_lev`、`tilebox`、`xyzmin`
3. **kernel 问题**：`doChargeDepositionShapeN` 如何按 node/cell shape 真正写入 `rho_arr`

## 6. 当前可稳定写进正文的结论

截至这一轮，关于 charge deposition 可以更明确地说：

1. WarpX 的普通 charge deposition 不像 current deposition 那样在容器层按多种算法名展开；它主要通过 ABLASTR 桥接到统一的 `doChargeDepositionShapeN<1..4>()`。
2. `icomp=0/1` 不只是数组 component 约定，而是通过 `time_shift_delta` 真正对应旧/新时间层的物理参考框架。
3. CPU 与 GPU 的 charge deposition 暂存策略不同：CPU 先沉 `local_rho` 再 `lockAdd`，GPU 则直接 alias 目标 `rho`。
4. `ChargeDeposition.H` 本体主要负责 shape-factor 与原子加；guard-cell 合法性、component 偏移和 coarse-fine/tile 几何在桥接层已经先被整理好。

## 7. 当前状态与剩余边界

本笔记已经完成普通 `ablastr::particles::deposit_charge(...)` 模板的源码级核对：参数合同、`depos_lev/rel_ref_ratio` 约束、shape/guard 检查、CPU/GPU 暂存、`icomp*nc` component 偏移，以及到 `doChargeDepositionShapeN<1..4>()` 的 dispatch 都已回填第 5 章 `5.8.2-5.9`。因此“继续追普通 ABLASTR 模板位置”不再是当前主要缺口。

仍需保留的后续工作是：

1. 随 WarpX checkout 更新重新核对本笔记中的源码行号；
2. 对 `RZ` 高阶 mode 写回和 inverse-volume scaling 做独立运行级验证；
3. 将普通路径与 shared-memory 路径的性能/数值差异做成可复现实验，而不是仅凭源码推断。

第 5 章沉积线源码层下一步更适合继续补：

1. `CurrentDeposition.H` 里 direct / implicit / Villasenor 的 remaining geometry branches；
2. `SyncCurrentAndRho()` 与 source synchronization 的更强验证入口；
3. 若能取得 `Esirkepov 2001` / `Villasenor-Buneman 1992` 全文，再把这里的实现边界回连到论文里的守恒推导。

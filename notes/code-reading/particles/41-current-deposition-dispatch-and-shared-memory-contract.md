# 41 current deposition dispatch and shared-memory contract：`DepositCurrent()` 入口真正决定的是哪条接口合同

绑定源码：

- `../warpx/Source/Particles/WarpXParticleContainer.cpp`

前置阅读：

- `../notes/code-reading/particles/04-amr-gather-deposition-buffers.md`
- `../notes/code-reading/particles/37-direct-vs-villasenor-boundary-cropping-and-suborbit.md`
- `../notes/code-reading/particles/40-rz-mode-writeback-and-inverse-volume-scaling.md`

第 5 章已经把 `CurrentDeposition.H` 里的 Direct、Esirkepov、Villasenor、Vay kernel 逐步拆开了。但如果只讲 kernel，还会漏掉一个更靠前的接口事实：`WarpXParticleContainer::DepositCurrent()` 不是简单“按 runtime 选一个算法名然后调用”，它先判定当前 tile 能走哪类接口合同，再把算法分派限制在那条合同里。

## 1. 入口先固定 guard-cell 与 tile 几何合法性，而不是先看算法名

`DepositCurrent()` 的前半段先做的是：

1. 检查 `depos_lev` 只能是 `lev` 或 `lev-1`；
2. 依据维度构造 `shape_extent`；
3. 用 `numParticlesOutOfRange(pti, range) == 0` 断言粒子 shape 不会越出 tile/guard cells；
4. 再构造 `tilebox`、`dinv`、`xyzmin`、`domain_double` 和 `do_cropping`。

源码位置：`../warpx/Source/Particles/WarpXParticleContainer.cpp:397-544`。

这里最值得带走的是：算法分派之前，WarpX 先保证“这批粒子在当前 level/tile 几何上是可沉积的”。也就是说，`DepositCurrent()` 不是只负责选算法；它先定义这次沉积允许使用的几何工作区。

## 2. collocated grid 在调用层就把 charge-conserving 路径切掉

入口里有一个很硬的前置限制：

```cpp
if (WarpX::current_deposition_algo == CurrentDepositionAlgo::Esirkepov ||
    WarpX::current_deposition_algo == CurrentDepositionAlgo::Villasenor) {
    if (WarpX::grid_type == GridType::Collocated) {
      WARPX_ABORT_WITH_MESSAGE("Charge-conserving current depositions (Esirkepov and Villasenor) cannot be used with a collocated grid.");
    }
}
```

源码位置：`../warpx/Source/Particles/WarpXParticleContainer.cpp:546-550`。

这说明 collocated 限制不是 `CurrentDeposition.H` 某个 kernel 的局部细节，而是 `DepositCurrent()` 入口直接施加的全局合同：

- 只要 current deposition 算法属于 charge-conserving 家族；
- 又选择了 collocated grid；
- 整条沉积路径在进入 kernel 之前就失败。

因此正文里不能把 “Esirkepov/Villasenor 不支持 collocated” 写成边角注释，它是调用层的首要分流条件之一。

## 3. shared-memory 路径不是“所有算法的加速版”，而是一条 direct-only 接口

`do_shared_mem_current_deposition` 打开后，`DepositCurrent()` 会先进入另一条很重的准备链：

1. 取 `geom/plo/dxi/domain`；
2. 用 `pti.validbox().grow(ng_J)` 和 `shared_tilesize` 构造 binning box；
3. 用 `DenseBins` 按粒子所在 cell 给粒子分 tile bins；
4. 再由 `getMaxTboxAlongDim(...)` 求 `max_tbox_size`；
5. 最后才进入 shared-memory kernel。

源码位置：`../warpx/Source/Particles/WarpXParticleContainer.cpp:555-650`。

但这条路径并不接受一般 current deposition 算法。源码直接限定：

- `implicit`：直接 abort
- `Esirkepov`：abort
- `Villasenor`：abort
- `Vay`：abort
- 只有 `Direct` 会继续调用 `doDepositionSharedShapeN<N>()`

这意味着 shared-memory current deposition 的真实语义是：

- 它首先是一条性能接口；
- 而不是 “把现有 Direct/Esirkepov/Villasenor/Vay 统一搬进 shared memory”。

所以第 5 章若要准确，应该写成：

- shared-memory current deposition 当前只实现了 explicit direct deposition 的 tile-binned 变体；
- 不是普通 current kernel 的通用加速后端。

## 4. normal 路径里才谈得上 Direct / Esirkepov / Villasenor / Vay 的家族分派

只有在 `!do_shared_mem_current_deposition` 时，源码才进入我们平时说的那条算法分派：

- `Esirkepov`
  - explicit 走 `doEsirkepovDepositionShapeN<N>()`
  - implicit 走 `doChargeConservingDepositionShapeNImplicit<N>()`
- `Villasenor`
  - explicit 走 `doVillasenorDepositionShapeNExplicit<N>()`
  - implicit 走 `doVillasenorDepositionShapeNImplicit<N>()`
- `Vay`
  - explicit 走 `doVayDepositionShapeN<N>()`
  - implicit 直接 abort
- `Direct`
  - explicit 走 `doDepositionShapeN<N>()`
  - implicit 走 `doDepositionShapeNImplicit<N>()`

源码位置：`../warpx/Source/Particles/WarpXParticleContainer.cpp:654-930`。

因此，WarpX 当前真正的 dispatch 层次是：

1. 先决定是否允许这批粒子在当前 tile/guard-cell 几何上沉积；
2. 再决定是否走 shared-memory performance path；
3. 只有 normal path 才继续分成 Direct / Esirkepov / Villasenor / Vay 四个家族。

## 5. `domain_double/do_cropping` 并不是所有 normal-path 算法都会消费

即使进入 normal path，入口里构造的几何边界信息也不会平均分给所有算法：

- `Esirkepov` explicit/implicit：接收 `domain_double, do_cropping`
- `Villasenor` explicit/implicit：接收 `domain_double, do_cropping`
- `Vay`：不接收
- `Direct` explicit/implicit：不接收

源码位置：`../warpx/Source/Particles/WarpXParticleContainer.cpp:654-930`。

这说明 `DepositCurrent()` 入口不是只在“选哪个 kernel”，还在决定：

- 哪些算法可以消费 boundary-cropping 语义；
- 哪些算法即使运行在同一 tile 上，也只能拿到时间层与几何缩放，而拿不到可裁剪轨迹合同。

这也正是为什么 direct 不能替代 Villasenor 去承担 near-boundary / suborbit 那类场景。

## 6. 对第 5 章最值得带走的结论

`DepositCurrent()` 的稳定理解顺序应该是：

1. 它先定义沉积是否合法
   - guard-cell 是否够；
   - `depos_lev` 是否只是本层或 coarse buffer；
   - collocated 是否与当前算法兼容。

2. 它再决定走哪条接口合同
   - shared-memory: explicit direct only
   - normal path: 才有 Direct / Esirkepov / Villasenor / Vay 家族分派

3. 它最后才把几何边界语义按算法能力分配下去
   - charge-conserving 路径拿到 `domain_double/do_cropping`
   - direct/Vay 则拿不到这层合同

因此，对正文来说，`WarpXParticleContainer::DepositCurrent()` 不只是“分派表”，而是 current deposition 的总入口合同：它把 geometry legality、grid-type restriction、performance path 和 algorithm family 这四层边界先固定住，后面的 kernel 只是各自在这个入口定义的合同内工作。

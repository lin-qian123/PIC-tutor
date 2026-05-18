# 04 AMR gather/deposition buffers：`aux`、`cax`、buffer masks 与粒子 kernel 的闭环

绑定源码：

- `../warpx/Source/Particles/PhysicalParticleContainer.cpp`
- `../warpx/Source/Particles/WarpXParticleContainer.cpp`
- `../warpx/Source/Particles/Gather/FieldGather.H`
- `../warpx/Source/Particles/Sorting/Partition.cpp`

对应理论/并行前置笔记：

- `../warpx/Docs/source/theory/amr.rst`
- `../notes/code-reading/parallelization/03-amr-coarse-fine-substitution.md`
- `../notes/code-reading/parallelization/04-warpxcomm-kernel-execution-model.md`

本文只回答一个问题：上一轮已经讲清 `aux = fp + I(parent_aux-cp)`、`gather/current buffer masks` 和 `PartitionParticlesInBuffers()`。但这些对象究竟怎样进入真正的粒子 gather / push / deposition kernel？答案在 `PhysicalParticleContainer::Evolve()` 和 `WarpXParticleContainer::{DepositCurrent,DepositCharge}` 里。

## 1. `PhysicalParticleContainer::Evolve()` 先分区，再分别走 fine 与 lower-level 路径

`PhysicalParticleContainer::Evolve()` 在 tile loop 内先计算：

```cpp
long nfine_deposit = np;
long nfine_gather = np;
if (has_buffer && !do_not_push) {
    PartitionParticlesInBuffers( nfine_deposit, nfine_gather, np,
        pti, lev, WarpX::n_field_gather_buffer,
        WarpX::n_current_deposition_buffer, current_masks, gather_masks );
}
```

源码位置：`../warpx/Source/Particles/PhysicalParticleContainer.cpp:566-575`。

这里做的不是“记一个标志”，而是直接重排粒子 tile，使得：

- 前 `nfine_gather` 个粒子走 fine-level gather；
- 后 `np-nfine_gather` 个粒子走 lower-level gather；
- 前 `nfine_deposit` 个粒子走 fine-level current/rho deposition；
- 后 `np-nfine_deposit` 个粒子走 lower-level current/rho deposition。

因此，WarpX 后续 gather 和 deposition kernel 根本不需要在单粒子内再去查 mask；mask 的作用在这一步已经被转换成“粒子数组前半段”和“粒子数组后半段”。

## 2. push 前旧电荷已经分成 `rho_fp` 和 `rho_buf`

tile 内旧电荷沉积直接按上面的分区拆成两次调用：

```cpp
const long np_to_deposit = has_J_buf ? nfine_deposit : np;

amrex::MultiFab* rho = fields.get(FieldType::rho_fp, lev);
DepositCharge(pti, wp, ion_lev, rho, 0, 0,
              np_to_deposit, thread_num, lev, lev);
if (has_buffer){
    amrex::MultiFab* crho = fields.get(FieldType::rho_buf, lev);
    DepositCharge(pti, wp, ion_lev, crho, 0, np_to_deposit,
                  np-np_to_deposit, thread_num, lev, lev-1);
}
```

源码位置：`../warpx/Source/Particles/PhysicalParticleContainer.cpp:577-591`。

这段代码说明两件事：

1. `rho_fp` 接收 fine 区粒子，`depos_lev = lev`；
2. `rho_buf` 接收 transition-zone 粒子，`depos_lev = lev-1`。

也就是说，buffer 路径并不是“额外复制一份电荷”，而是 coarse-fine 界面附近粒子根本不再往当前 fine patch 的 `rho_fp` 沉积，而是转去当前 level 持有的 coarse buffer 容器 `rho_buf`。

## 3. gather 不是统一从 `aux` 取场，而是分成 `aux` 与 `cax`

`PhysicalParticleContainer::Evolve()` 的 push 分成两段。第一段处理不在 gather buffer 内的粒子：

```cpp
const long np_gather = has_E_cax ? nfine_gather : np;
const auto np_to_push = np_gather;
const auto gather_lev = lev;
PushPX(pti, exfab, eyfab, ezfab,
       bxfab, byfab, bzfab,
       Ex.nGrowVect(), e_is_nodal,
       0, np_to_push, lev, gather_lev, dt, ...);
```

源码位置：`../warpx/Source/Particles/PhysicalParticleContainer.cpp:597-617`。

这里传入的 `exfab/eyfab/...` 来自当前 level 的 `Efield_aux/Bfield_aux`。也就是说，fine interior 粒子 gather 的并不是原始 `fp` 或 `cp`，而是已经做完 substitution 的 full solution `aux`。

随后，若 `np_gather < np`，剩余粒子改走 coarse-aux 副本：

```cpp
amrex::MultiFab & cEx = *fields.get(FieldType::Efield_cax, Direction{0}, lev);
...
PushPX(pti, cexfab, ceyfab, cezfab,
       cbxfab, cbyfab, cbzfab,
       cEx.nGrowVect(), e_is_nodal,
       nfine_gather, np-nfine_gather,
       lev, lev-1, dt, ...);
```

源码位置：`../warpx/Source/Particles/PhysicalParticleContainer.cpp:640-676`。

这里关键不是字段名，而是参数对：

- `offset = nfine_gather`
- `np_to_push = np-nfine_gather`
- `lev = 当前粒子所属 fine level`
- `gather_lev = lev-1`

这就把后半段粒子明确送到“从 coarse-aux gather”的路径上。

## 4. `PushPX()` 对 AMR buffer 的真实契约只有两条

`PushPX()` 一进入就断言：

```cpp
WARPX_ALWAYS_ASSERT_WITH_MESSAGE((gather_lev==(lev-1)) ||
                                 (gather_lev==(lev  )),
                                 "Gather buffers only work for lev-1");
```

源码位置：`../warpx/Source/Particles/PhysicalParticleContainer.cpp:1341-1343`。

这说明 WarpX 当前不支持任意跨多级 gather buffer，只支持：

- `gather_lev = lev`
- `gather_lev = lev-1`

接着它按 `gather_lev` 决定 field box：

```cpp
if (lev == gather_lev) {
    box = pti.tilebox();
} else {
    const IntVect& ref_ratio = WarpX::RefRatio(gather_lev);
    box = amrex::coarsen(pti.tilebox(),ref_ratio);
}
box.grow(ngEB);
const amrex::XDim3 dinv = WarpX::InvCellSize(std::max(gather_lev,0));
const amrex::XDim3 xyzmin = WarpX::LowerCorner(box, gather_lev, 0._rt);
```

源码位置：`../warpx/Source/Particles/PhysicalParticleContainer.cpp:1349-1360,1377-1388`。

因此，buffer gather 的本质不是“在 fine box 里读 coarse data”，而是：

1. 先把当前 tilebox 按 `ref_ratio` coarsen；
2. 用 coarse level 的 `dinv` 和 `xyzmin` 重建粒子到 coarse 网格坐标的映射；
3. 再把这些 coarse-grid `Array4` 交给 `doGatherShapeN()`。

最终实际 gather 调用并不区分 fine/buffer，只是统一走：

```cpp
doGatherShapeN(xp, yp, zp, Exp, Eyp, Ezp, Bxp, Byp, Bzp,
               ex_arr, ey_arr, ez_arr, bx_arr, by_arr, bz_arr,
               ex_type, ey_type, ez_type, bx_type, by_type, bz_type,
               dinv, xyzmin, lo, n_rz_azimuthal_modes,
               nox, galerkin_interpolation);
```

源码位置：`../warpx/Source/Particles/PhysicalParticleContainer.cpp:1498-1503` 与 `../warpx/Source/Particles/Gather/FieldGather.H:2119-2183`。

也就是说，AMR buffer 不需要新的 gather kernel；它只是换了一组 `Array4 + IndexType + dinv + xyzmin + lo`。

## 5. current deposition 也分成 `current_fp` 与 `current_buf`

显式/隐式 push 之后，电流沉积同样拆成两次：

```cpp
DepositCurrent(pti, wp, uxp, uyp, uzp, ion_lev, jx, jy, jz,
               0, np_to_deposit, thread_num,
               lev, lev, dt, relative_time, push_type);
...
DepositCurrent(pti, wp, uxp, uyp, uzp, ion_lev, cjx, cjy, cjz,
               np_to_deposit, np-np_to_deposit, thread_num,
               lev, lev-1, dt, relative_time, push_type);
```

源码位置：`../warpx/Source/Particles/PhysicalParticleContainer.cpp:712-730`。

这里与 gather 完全平行：

- 前半段粒子沉到 fine patch 的 `current_fp` 或 `current_fp_non_suborbit`；
- 后半段粒子沉到 coarse buffer 容器 `current_buf`；
- buffer 路径同样只允许 `depos_lev = lev-1`。

## 6. `DepositCurrent()` 真正改变的是 tilebox、几何和 guard-cell 解释

`WarpXParticleContainer::DepositCurrent()` 一开始就声明：

```cpp
WARPX_ALWAYS_ASSERT_WITH_MESSAGE((depos_lev==(lev-1)) ||
                                 (depos_lev==(lev  )),
                                 "Deposition buffers only work for lev-1");
```

源码位置：`../warpx/Source/Particles/WarpXParticleContainer.cpp:400-403`。

然后它按 `depos_lev` 重新定义沉积 box：

```cpp
Box tilebox;
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

源码位置：`../warpx/Source/Particles/WarpXParticleContainer.cpp:462-474,436,517`。

这和 `PushPX()` 的逻辑是同一个模式：

- 粒子仍然保留 fine-level 连续位置；
- 但 deposition kernel 接收到的是 coarse 化后的 tilebox；
- `dinv`、`xyzmin`、`domain_box`、PEC cropping 判据全都以 `depos_lev` 解释。

因此，buffer current deposition 不是“先在 fine 上沉，再 restrict 到 coarse”；它一开始就在 coarse buffer patch 的几何上直接沉积。

## 7. `DepositCurrent()` 的算法分派不会因为 AMR buffer 改变

`DepositCurrent()` 后半段仍按 `current_deposition_algo` 分派：

- Esirkepov
- Villasenor
- Vay
- Direct
- 以及 shared-memory direct 变体

源码范围：`../warpx/Source/Particles/WarpXParticleContainer.cpp:546-900`。

AMR buffer 并没有引入另一套 current deposition kernel。真正变化的仍然只是：

- `offset`
- `np_to_deposit`
- `depos_lev`
- 与之相应的 `tilebox/dinv/xyzmin/domain_box`

所以 coarse-fine 粒子分流是“复用同一 deposition 算法，在不同 level 几何和不同容器上运行”，而不是“为 AMR 专门写一套 deposition 数学”。

## 8. `DepositCharge()` 也是同一个模式

`DepositCharge()` 的契约与 current 完全平行：

```cpp
WARPX_ALWAYS_ASSERT_WITH_MESSAGE((depos_lev==(lev-1)) ||
                                 (depos_lev==(lev  )),
                                 "Deposition buffers only work for lev-1");
...
if (lev == depos_lev) {
    tilebox = pti.tilebox();
} else {
    const IntVect& ref_ratio = WarpX::RefRatio(depos_lev);
    tilebox = amrex::coarsen(pti.tilebox(),ref_ratio);
}
tilebox.grow(ng_rho);
const amrex::XDim3 xyzmin = WarpX::LowerCorner(tilebox, depos_lev, time_shift_delta);
const amrex::XDim3 dinv = WarpX::InvCellSize(std::max(depos_lev,0));
```

源码位置：`../warpx/Source/Particles/WarpXParticleContainer.cpp:1494-1497,1541-1579,1737-1750`。

唯一额外区别是 `rho` 有 `icomp=0/1` 两个时间层，因此 `xyzmin` 里的时间偏移写成：

- `icomp == 0` 时 `time_shift_delta = 0`
- `icomp == 1` 时 `time_shift_delta = dt`

这对应旧电荷 \(\rho^n\) 和新电荷 \(\rho^{n+1}\)。

## 9. coarse-fine buffer 在粒子层的最小闭环

把前几篇 AMR 笔记和这里的粒子 kernel 接起来，可以得到一条完整闭环：

1. `UpdateAuxilaryData*()` 先构造 fine-level full solution `aux`；
2. `BuildBufferMasks*()` 用 transition-zone 厚度生成 `gather/current buffer masks`；
3. `PartitionParticlesInBuffers()` 用 mask 重排 tile 中粒子，得到 `nfine_gather` 和 `nfine_deposit`；
4. `PushPX()` 对前半段粒子使用 `E/Bfield_aux` 和 `gather_lev = lev`；
5. `PushPX()` 对后半段粒子使用 `E/Bfield_cax` 和 `gather_lev = lev-1`；
6. `DepositCurrent()` / `DepositCharge()` 对前半段沉到 `current_fp/rho_fp`；
7. `DepositCurrent()` / `DepositCharge()` 对后半段直接沉到 `current_buf/rho_buf`，并以 `depos_lev = lev-1` 解释 tilebox 和几何；
8. 后续 `SyncCurrent()` / `SyncRho()` 再把这些 coarse-fine source 容器并回统一通信链。

因此，WarpX 的 AMR 粒子路径不是“粒子总在 fine level 上演化，只是后处理时做 coarse-fine 修补”，而是从 gather 开始就允许 transition-zone 粒子切换到 lower-level 物理解释。

## 10. 当前边界与后续阅读点

这一层目前已经能回答：

- `aux` / `cax` / `buffer masks` 在粒子层如何真正生效；
- coarse-fine buffer 为何不需要专门的 gather/deposition kernel；
- fine interior 与 transition zone 的粒子为何可以分别使用不同 level 的场和源项容器。

但还没继续往下展开：

- `CurrentDeposition.H` 中 Villasenor / Vay / implicit charge-conserving 在 buffer 路径上的细节差异；
- `do_not_deposit`、shared-memory deposition、EB reduced shape 与 AMR buffer 的交叉作用；
- diagnostics 如何消费 `current_buf/rho_buf` 或最终合并后的多层源项。

这些可以作为后续 `Particles/Deposition` 和 `Diagnostics/` 的接续入口。

# Parallelization 03: AMR coarse-fine interface 与 substitution strategy

绑定源码：

- `../warpx/Docs/source/theory/amr.rst`
- `../warpx/Source/WarpX.H`
- `../warpx/Source/WarpX.cpp`
- `../warpx/Source/Parallelization/WarpXComm.cpp`
- `../warpx/Source/Parallelization/WarpXComm_K.H`
- `../warpx/Source/Particles/PhysicalParticleContainer.cpp`
- `../warpx/Source/Particles/Sorting/Partition.cpp`

## 1. 这一层要回答什么

前面三篇并行笔记已经把：

1. guard-cell 预算；
2. current / rho 的 coarse-fine 同步；
3. load balance / `RemakeLevel()`

这些工程结构讲清楚了。

但 AMR 真正最难的不是“怎么通信”，而是 refinement interface 附近如何同时控制：

- 粒子的 spurious self-force；
- 电磁波在 coarse-fine 界面的反射 / 放大；
- coarse 解与 fine 解的替换关系；
- 粒子到底从 fine patch 还是 parent level gather / deposit。

WarpX 官方理论文档把这层叫作 substitution method。源码里它并不是一个叫“substitution”的单函数，而是分散在：

- `E/Bfield_aux`
- `E/Bfield_cp`
- `E/Bfield_cax`
- `UpdateAuxilaryData*()`
- gather / current buffer masks
- `PartitionParticlesInBuffers()`

这一篇的目标就是把这些块拼成一条完整主链。

## 2. 理论文档里的主公式：`F(a)=F(r)+I[F(s)-F(c)]`

`Docs/source/theory/amr.rst` 对电磁 AMR 的核心写法是：

$$
F(a) = F(r) + I\bigl[F(s) - F(c)\bigr].
$$

其中：

- `r` 是 refined patch 上的 fine-resolution 场；
- `c` 是与 refined patch 同位置的 coarse patch；
- `s` 是 parent grid 上与 patch 对应的 coarse subset；
- `a` 是粒子真正 gather 的 auxiliary grid；
- `I` 是 coarse-to-fine 插值算子。

物理含义不是“把 coarse 和 fine 简单叠加”，而是：

1. parent grid 已经包含 patch 内外所有源的粗网格响应；
2. coarse patch 只包含 patch 内源在粗网格上的响应；
3. 二者相减得到“patch 外源对 patch 区域的 coarse 背景场”；
4. 再把这部分插值到 fine 网格，加到 fine patch 解上；
5. 于是 patch 区域内最终场变成“外部粗背景 + 内部细解”的替换结果。

WarpX 之所以采用这条路，而不是让 finer level 直接反向改 parent solver，是因为它要尽量保持“某一级场解不受更细级反过来污染”的结构，以减轻 coarse-fine 界面上的长程高斯误差。

## 3. 源码总接口：`aux(lev) = fp(lev) + I(aux(lev-1)-cp(lev))`

这个公式在 `WarpX.H` 里被直接写成注释：

```cpp
// This function does aux(lev) = fp(lev) + I(aux(lev-1)-cp(lev)).
// Caller must make sure fp and cp have ghost cells filled.
void UpdateAuxilaryData ();
```

源码位置：`../warpx/Source/WarpX.H:649-652`。

这已经把理论符号完全落成了真实对象：

- `fp(lev)` 对应 fine patch 解；
- `cp(lev)` 对应 coarse patch 解；
- `aux(lev-1)` 对应 parent level 的 full solution；
- `aux(lev)` 对应当前 level 给粒子 gather 的 full solution。

因此，WarpX 的 substitution 不是 field push 内部的一部分，而是每次粒子 gather 前通过 `UpdateAuxilaryData()` 显式重建出来的。

## 4. 粒子为什么需要 `aux` 而不是直接 gather `fp`

如果只让 refined patch 内所有粒子都直接 gather `fp`，那么这些粒子会失去 patch 外源通过 parent grid 传播进来的背景场贡献；如果直接 gather parent coarse field，又会丢掉 patch 内源的高分辨率解。

`aux` 的作用就是给粒子提供“完整但经过替换”的场。WarpX 在 `PhysicalParticleContainer::Evolve()` 里拿来给粒子看的就是：

```cpp
amrex::MultiFab & Ex = *fields.get(FieldType::Efield_aux, Direction{0}, lev);
amrex::MultiFab & Ey = *fields.get(FieldType::Efield_aux, Direction{1}, lev);
amrex::MultiFab & Ez = *fields.get(FieldType::Efield_aux, Direction{2}, lev);
amrex::MultiFab & Bx = *fields.get(FieldType::Bfield_aux, Direction{0}, lev);
amrex::MultiFab & By = *fields.get(FieldType::Bfield_aux, Direction{1}, lev);
amrex::MultiFab & Bz = *fields.get(FieldType::Bfield_aux, Direction{2}, lev);
```

源码位置：`../warpx/Source/Particles/PhysicalParticleContainer.cpp:479-484`。

也就是说，`aux` 不是可选诊断容器，而是粒子-场耦合的真实工作场。

## 5. Level 0 与 higher level 的角色不同

`UpdateAuxilaryDataSameType()` 开头先对 level 0 做最简单的处理：

- 若启用了 FFT time averaging，则从 `E/Bfield_avg_fp` 复制；
- 否则直接从 `E/Bfield_fp` 复制。

这一步不需要 substitution，因为 level 0 没有 parent level。

真正的 coarse-fine 替换从 `lev >= 1` 开始。代码结构是：

1. 先从 `aux(lev-1)` 拷贝出 parent coarse full solution；
2. 再减去当前 level 的 `cp(lev)`；
3. 最后把差值插值到 fine grid，并加到 `fp(lev)` 上，得到 `aux(lev)`。

这正是理论公式的逐项实现。

## 6. `UpdateAuxilaryDataSameType()`：同 stagger 情况下的 substitution

对最常见的“aux 和 fp/cp staggering 相同”情况，`UpdateAuxilaryDataSameType()` 的 `B` 路径最清楚：

```cpp
ablastr::utils::communication::ParallelCopy(dBx, *Bfield_aux[lev - 1][0], ...);
...
MultiFab::Subtract(dBx, *m_fields.get(FieldType::Bfield_cp, Direction{0}, lev), ...);
...
warpx_interp(j, k, l, bx_aux, bx_fp, bx_c, Bx_stag, refinement_ratio);
```

源码位置：`../warpx/Source/Parallelization/WarpXComm.cpp:545-603`。

这里的三步分别对应：

1. `dBx <- aux(lev-1)`：从 parent level 取 full coarse solution；
2. `dBx <- dBx - cp(lev)`：去掉 patch 内源在 coarse patch 上的粗解；
3. `bx_aux <- fp + I(dBx)`：把 coarse 背景插值到 fine grid，加回 fine patch。

`E` 的路径与之完全平行，在 `WarpXComm.cpp:628-688`。

所以从工程实现上看，WarpX 的 substitution 不是“解完方程后把两张图 blend 一下”，而是明确地做了：

`parent full solution -> subtract coarse patch -> interpolate residual -> add onto fine patch`

## 7. `WarpXComm_K.H` 内核把 substitution 写成了点值公式

最核心的 GPU 内核在 `WarpXComm_K.H` 的同-stagger 版本：

```cpp
arr_aux(j,k,l) = arr_fine(j,k,l) + res;
```

源码位置：`../warpx/Source/Parallelization/WarpXComm_K.H:83`。

这里的 `res` 就是 coarse residual `I(aux_parent - cp)` 的插值值。

而在 momentum-conserving gather、需要 stag-to-nodal 转换时，对应内核写成：

```cpp
arr_aux(j,k,l) = tmp + (fine - coarse);
```

源码位置：`../warpx/Source/Parallelization/WarpXComm_K.H:238`。

其中：

- `tmp` 是 parent `aux` 插值到 nodal 的值；
- `coarse` 是当前 coarse patch 插值到 nodal 的值；
- `fine` 是当前 fine patch 插值到 nodal 的值。

这其实还是同一个 substitution 公式，只是为了 staggered-to-nodal gather，被拆成了三个 nodal 化后的部分。

## 8. `UpdateAuxilaryDataStagToNodal()`：momentum-conserving gather 的特殊版

当粒子 gather 算法要求 nodal `aux`，而 field solver 本身仍在 staggered / mixed grid 上时，WarpX 走 `UpdateAuxilaryDataStagToNodal()`。

这一版做了两件额外工作：

1. 先把 fine / coarse / parent coarse full solution 分别插到 nodal；
2. 再在 nodal `aux` 上执行 `tmp + (fine - coarse)`。

因此，`UpdateAuxilaryData()` 的顶层分派不是为了代码风格，而是为了区分：

- same-type substitution
- stagger-to-nodal substitution

这两个真实物理路径。

## 9. `Efield_cax / Bfield_cax`：为什么还要保存“coarse aux 的拷贝”

在 `AllocLevelMFs()` 里，若 level 大于 0 且需要 field gather buffer 或者有 species 强制从主网格 gather，就会分配：

- `Efield_cax`
- `Bfield_cax`

源码位置：`../warpx/Source/WarpX.cpp:3001-3031`。

它们的角色不是另一套 solver patch，而是“copy of the coarse aux”。在 `UpdateAuxilaryDataStagToNodal()` 和 `UpdateAuxilaryDataSameType()` 里，如果 `cax` 已存在，parent coarse full solution 就可以直接 alias / copy 到它，而不是每次临时分配。

因此：

- `cp` 是“patch 内源的 coarse 解”；
- `cax` 更接近“给 buffer gather 用的 coarse full solution 副本”；
- `aux` 则是粒子最终看的 full substituted solution。

## 10. transition zone 的用户接口：`n_field_gather_buffer` 与 `n_current_deposition_buffer`

WarpX 在 `WarpX.H` 里直接把两个最关键的 AMR 用户参数写成了语义注释：

```cpp
//! With mesh refinement, particles located inside a refinement patch, but within
//! #n_field_gather_buffer cells of the edge of the patch, will gather the fields
//! from the lower refinement level instead of the refinement patch itself
static int n_field_gather_buffer;
//! With mesh refinement, particles located inside a refinement patch, but within
//! #n_current_deposition_buffer cells of the edge of the patch, will deposit their charge
//! and current onto the lower refinement level instead of the refinement patch itself
static int n_current_deposition_buffer;
```

源码位置：`../warpx/Source/WarpX.H:340-347`。

这两个参数就是理论文档里“transition cells”的运行时入口。

`WarpX.cpp` 还给出一个默认关系：

```cpp
if (n_field_gather_buffer < 0) {
    // Field gather buffer should be larger than current deposition buffers
    n_field_gather_buffer = n_current_deposition_buffer + 1;
}
```

源码位置：`../warpx/Source/WarpX.cpp:2336-2339`。

这说明 WarpX 默认认为：

- gather transition zone 至少要比 deposition buffer 宽一层；
- 否则粒子可能在刚从 coarse deposit 切回 fine gather 的位置看到更尖锐的不连续。

## 11. buffer masks：transition zone 不是抽象概念，而是显式 `iMultiFab`

只要开启了 field gather buffer 或 current deposition buffer，`AllocLevelMFs()` 就会分配：

- `gather_buffer_masks[lev]`
- `current_buffer_masks[lev]`

源码位置：`../warpx/Source/WarpX.cpp:3033-3046`。

随后 `BuildBufferMasks()` 会在每个 level 上根据 patch interior / guard / physical boundary 构建这些 mask。

`BuildBufferMasksInBox()` 的逻辑是：

```cpp
for (ii,jj,kk in neighborhood of size ngbuffer) {
    if ( gmsk(ii,jj,kk) == 0 ) {
        msk(i,j,k) = 0;
        return;
    }
}
msk(i,j,k) = 1;
```

源码位置：`../warpx/Source/WarpX.cpp:3495-3511`。

这表示一个 cell 只有在其 `ngbuffer` 邻域都保持在 patch interior 内时，mask 才为 `1`；否则为 `0`。换句话说：

- `1` 代表足够远离界面的 interior；
- `0` 代表落入 coarse-fine 过渡带，需要按 buffer 规则处理。

## 12. 粒子如何真正使用这些 masks

`PhysicalParticleContainer::Evolve()` 在每个 tile 开头取出：

```cpp
const iMultiFab* current_masks = WarpX::CurrentBufferMasks(lev);
const iMultiFab* gather_masks = WarpX::GatherBufferMasks(lev);
```

源码位置：`../warpx/Source/Particles/PhysicalParticleContainer.cpp:472-473`。

若该 level 有 buffer，就调用：

```cpp
PartitionParticlesInBuffers(
    nfine_deposit, nfine_gather, np,
    pti, lev, WarpX::n_field_gather_buffer,
    WarpX::n_current_deposition_buffer, current_masks, gather_masks );
```

源码位置：`../warpx/Source/Particles/PhysicalParticleContainer.cpp:572-574`。

这说明 transition zone 并不是在 gather kernel 内“动态 if 判断”，而是先通过分区把粒子稳定地拆成：

- 在 fine patch 上 gather/deposit 的粒子；
- 在 buffer / parent level 上 gather/deposit 的粒子。

## 13. `PartitionParticlesInBuffers()`：先按大 buffer 分，再按小 buffer 分

`Partition.cpp` 的设计很直接：

1. 先选择 `n_field_gather_buffer` 和 `n_current_deposition_buffer` 中较大的那一个；
2. 用对应的 mask 把粒子分成“fine interior”和“落入大 buffer”的两组；
3. 再在大 buffer 里，用较小 buffer 的 mask 做第二次稳定划分；
4. 得到：
   - `nfine_current`
   - `nfine_gather`

源码位置：`../warpx/Source/Particles/Sorting/Partition.cpp:61-115`。

因此，WarpX 并不是简单维护一个“buffer 粒子”集合，而是分别维护：

- 哪些粒子还能在 fine patch 上 deposition；
- 哪些粒子还能在 fine patch 上 gather。

这正好对应理论上“gather transition zone”和“deposition transition zone”可以不同宽度的设计。

## 14. species 级覆盖：`deposit_on_main_grid` / `gather_from_main_grid`

除了通用 buffer 宽度，WarpX 还允许某些 species 直接强制：

- `deposit_on_main_grid`
- `gather_from_main_grid`

在 `PartitionParticlesInBuffers()` 末尾，若这两个开关打开：

```cpp
if (m_deposit_on_main_grid && lev > 0) {
    nfine_current = 0;
}
if (m_gather_from_main_grid && lev > 0) {
    nfine_gather = 0;
}
```

源码位置：`../warpx/Source/Particles/Sorting/Partition.cpp:126-131`。

这意味着某些物种可以完全绕过 refined patch 的 gather 或 deposition，而不是只在 transition zone 内切换。

## 15. 为什么这些 transition zone 真的重要

`amr.rst` 对两类误差的判断非常明确：

1. electrostatic 情况下，靠近界面的 self-force 会快速上升；
2. electromagnetic substitution 情况下，会出现 ghost fixed charges 的残余多极场，以及低阶 Maxwell stencil 下 coarse / fine 数值色散不匹配。

WarpX 的缓解手段正好对应源码里的两个 runtime 结构：

- `n_field_gather_buffer` / `gather_buffer_masks`：让靠界面粒子直接看 parent coarse solution；
- `n_current_deposition_buffer` / `current_buffer_masks`：让靠界面粒子把源项沉积回 lower level。

这就是理论文档里“transition cells are added around the effective refined area”在代码里的真正落地。

## 16. 当前这一层的结论

WarpX 的 AMR coarse-fine interface 不是单一操作，而是三层配合：

1. **场替换层**：`UpdateAuxilaryData*()` 用 `aux = fp + I(parent_aux - cp)` 构造 full solution；
2. **过渡区控制层**：`gather_buffer_masks` / `current_buffer_masks` 把 patch 边缘变成显式 transition zone；
3. **粒子分区层**：`PartitionParticlesInBuffers()` 把粒子按 gather/deposit 目的地稳定重排。

所以第 7 章里的 refinement interface 问题，不能只讲 coarse-fine interpolation 或 `SyncCurrent()`。真正的闭环必须把：

`substitution formula -> aux fields -> buffer masks -> particle partition`

一起讲清楚。

## 17. 下一步应该读哪里

在 `Parallelization` 与 `AMR` 这一支上，当前最自然的下一步有两条：

1. 继续 `WarpXComm_K.H` 后半段和 `MFIter` / `ParallelFor`，把并行层推进到 device-kernel 执行模型；
2. 回到 `Particles/Gather` 与 `Particles/Deposition`，把 `aux` / `buffer masks` / `PartitionParticlesInBuffers()` 如何进入具体 gather/deposition kernels 再向下打穿。

当前更优先的是第 1 条，因为第 7 章的 coarse-fine interface 主问题已经有了完整主链，下一层更缺的是 GPU portability / kernel 结构。

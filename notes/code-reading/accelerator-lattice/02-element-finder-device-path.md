# AcceleratorLattice 02: element finder, lookup tables, and boosted-frame field application

绑定源码：

- `../warpx/Source/AcceleratorLattice/LatticeElementFinder.H`
- `../warpx/Source/AcceleratorLattice/LatticeElementFinder.cpp`
- `../warpx/Source/AcceleratorLattice/AcceleratorLattice.cpp`
- `../warpx/Source/Particles/Pusher/GetExternalField.H`  
  实际外场调用主链见项目其余笔记，这里只回到 lattice finder 自身。

这篇只回答一个问题：beamline 元件是怎么在粒子推进前，变成每个粒子能直接取到的 `E/B` 外场的。

## 1. finder 是按 grid 保存的，不是全局唯一表

`AcceleratorLattice::InitElementFinder()` 会在 `m_lattice_defined` 时创建：

```text
LayoutData<LatticeElementFinder>
```

然后对每个 `MFIter` tile 做：

```text
finder.InitElementFinder(lev, gamma_boost, time, mfi, *this)
```

所以 finder 的粒度不是“整个 level 一张表”，而是：

- 每个 grid/tile 一个 finder 实例

这解释了它为什么要保存：

- `m_nz`
- `m_zmin`
- `m_dz`
- `m_time`

这些都和当前 tile 的空间位置有关。

## 2. 只给会产场的元件分配 lookup table

`AllocateIndices()` 当前只会分配：

- `d_quad_indices`
- `d_plasmalens_indices`

前提分别是：

- `h_quad.nelements > 0`
- `h_plasmalens.nelements > 0`

这里再次说明一个关键边界：

- `drift` 没有 lookup table
- 因为它根本不返回场

## 3. lookup table 的单位是“每个 z-node 最近的同类元件索引”

`setup_lattice_indices()` 的输入不是粒子，而是：

- 一类元件的全部 `zs`
- 全部 `ze`
- 对应的一维 `indices`

它会对每个 `iz`：

1. 先把 node 位置写成：
   - `z_node = zmin + iz * dz`
2. 若在 boosted frame：
   - 先反变换回 lab-frame `z_node`
3. 再在同类元件之间找“最近的那一个”

这里的最近不是简单最近中心点，而是用相邻元件中点划分责任区：

- 左边界：前一个元件 `ze` 与当前元件 `zs` 的中点
- 右边界：当前元件 `ze` 与后一个元件 `zs` 的中点

因此 lookup table 的真实语义是：

- 每个 z-node 预先指向一类元件里最可能影响这里的那个元件

## 4. 更新时机会跟随时间推进

`UpdateIndices()` 每次会更新：

- `m_zmin`
- `m_time`

然后重新调用 `setup_lattice_indices(...)`。

这件事很重要，因为在：

- moving window
- boosted frame

场景下，grid 在模拟 frame 中的位置会变，lookup table 不能只在初始化时算一次。

## 5. device finder 保存的是“粒子访问所需最小集”

`LatticeElementFinderDevice::InitLatticeElementFinderDevice()` 会装入：

- 粒子位置访问器 `GetParticlePosition<PIdx>`
- `ux/uy/uz` 指针
- `dt`
- `gamma_boost`
- `uz_boost`
- 当前 tile 的 `m_nz/m_zmin/m_dz/m_time`
- quadrupole/plasmalens 的 device instance
- 两类元件的 index arrays

这说明 device finder 真正要做的工作只有一件：

- 对单粒子快速返回 lattice 外场增量

## 6. `operator()` 的真实运行链

对每个粒子，runtime 路径是：

1. 取当前位置 `x,y,z`
2. 在当前 tile 的 boost-frame index grid 上算：
   - `iz = (z - zmin) / dz`
3. 由 `ux,uy,uz` 算相对论 `gamma`
4. 算出粒子一步后的估计位置：
   - `zpvdt = z + v_z dt`
5. 如果是 boosted frame：
   - 把 `z`
   - 把 `zpvdt`
   都反变换回 lab frame
6. 分别查询：
   - nearest quadrupole
   - nearest plasma lens
7. 把两类元件返回的 `Ex/Ey/Bx/By` 累加
8. 如果是 boosted frame，再把累计场从 lab frame 变回 boosted frame
9. 最后把它们加到粒子的 `field_E* / field_B*`

这里最重要的两个点是：

- 元件内部 field getter 全都工作在 lab frame
- finder 负责 frame transform，而不是元件自己管 boost

## 7. boosted-frame 处理的真正边界

这条路径不是简单“位置反变换一下”。

它做了两次不同层次的 boost 处理：

1. 在 lookup-table 建表时
   - 用当前 `m_time`
   - 把每个 node 的 boost-frame `z_node`
   - 反变换回 lab frame
2. 在粒子取场时
   - 把粒子的 `z` 和 `zpvdt`
   - 反变换回 lab frame
   - 元件返回 lab-frame `E/B`
   - 再把这些 `E/B` 正向变回 boosted frame

所以 accelerator lattice 的 boosted 支持不是“只在 diagnostics 后处理时补一个反变换”，而是运行时 field application 本身就做了完整 frame bookkeeping。

## 8. 对项目最重要的结论

把 `AcceleratorLattice` 路径压成一句话，就是：

```text
recursive beamline input
-> host element containers
-> per-tile nearest-element lookup tables
-> device finder with particle momentum/time context
-> lab-frame hard-edged field fetch
-> optional boosted-frame transform back
-> add to particle external E/B
```

因此 accelerator lattice 当前真正值得写进正文的不是“有 beamline 配置语法”，而是：

- 它把 beamline 元件变成了 push 前可直接 gather 的粒子侧外场
- 而且这个 gather 路径已经显式兼容 boosted frame 和 moving window 的 tile/update 语义

这也是 `hard_edged_quadrupoles` 那组三条强 regression 真正闭合的对象。

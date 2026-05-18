# Parallelization 02: regrid / load balance 与 `RemakeLevel()`

绑定源码：

- `../warpx/Source/Parallelization/WarpXRegrid.cpp`
- `../warpx/Source/WarpX.cpp`
- `../warpx/Source/WarpX.H`
- `../warpx/Docs/source/usage/parameters.rst`
- `../warpx/Docs/source/usage/workflows/plot_distribution_mapping.rst`

## 1. 这一层要回答什么

前两篇已经把 guard-cell 预算、`FillBoundary` / `SumBoundary` 语义，以及 current / rho 的 coarse-fine 同步主链固定下来了。接下来必须回答另一类问题：

1. 什么时候 WarpX 会决定重新 load balance；
2. 重新分配 rank 后，哪些数据结构必须跟着重建；
3. `RemakeLevel()` 到底是“轻量改映射”，还是一次接近 level 重生的操作；
4. `LoadBalanceCosts` / `LoadBalanceEfficiency` 这些诊断量和源码里的 `costs`、`load_balance_efficiency` 是怎么对应的。

这一篇只做 `WarpXRegrid.cpp` 的 load-balance / remake-level 主链，不展开 AMR coarse-fine substitution strategy 本身。

## 2. 触发点：`CheckLoadBalance(step)`

顶层入口不是 `LoadBalance()`，而是每步检查的：

```cpp
void
WarpX::CheckLoadBalance (int step)
{
    if (step > 0 && load_balance_intervals.contains(step+1))
    {
        LoadBalance();

        // Reset the costs to 0
        ResetCosts();
    }
    if (!costs.empty())
    {
        RescaleCosts(step);
    }
}
```

源码位置：`../warpx/Source/Parallelization/WarpXRegrid.cpp:49-63`。

这里有两个容易忽略的点：

1. 判断条件用的是 `step+1`，即“下一步序号是否落在 interval 上”；
2. 即使这一轮没有真正重分布，只要 `costs` 已存在，timer 模式下仍会执行 `RescaleCosts(step)`。

因此，load balance 在 WarpX 里不是一个孤立动作，而是“周期性检查 + 条件触发 + 成本重置/重标定”的组合流程。

## 3. `LoadBalance()` 的第一步不是搬数据，而是先决定“值不值得搬”

`LoadBalance()` 开头先确保 `costs` 存在；若更新算法是 heuristic，则先重算每个 box 的代价：

```cpp
if (load_balance_costs_update_algo == LoadBalanceCostsUpdateAlgo::Heuristic)
{
    // compute the costs on a per-rank basis
    ComputeCostsHeuristic(costs);
}
```

源码位置：`../warpx/Source/Parallelization/WarpXRegrid.cpp:75-80`。

随后对每个 AMR level 单独构造候选 `DistributionMapping`。WarpX 在这里支持两条策略：

- `DistributionMapping::makeSFC(...)`
- `DistributionMapping::makeKnapSack(...)`

对应源码：

```cpp
newdm = (load_balance_with_sfc)
    ? DistributionMapping::makeSFC(*costs[lev],
                                   currentEfficiency, proposedEfficiency,
                                   false,
                                   ParallelDescriptor::IOProcessorNumber())
    : DistributionMapping::makeKnapSack(*costs[lev],
                                        currentEfficiency, proposedEfficiency,
                                        nmax,
                                        false,
                                        ParallelDescriptor::IOProcessorNumber());
```

源码位置：`../warpx/Source/Parallelization/WarpXRegrid.cpp:98-108`。

这里的关键不是“SFC 和 knapsack 二选一”本身，而是 WarpX 会同时算出：

- `currentEfficiency`
- `proposedEfficiency`

然后再用阈值判断这次重分布是否值得执行：

```cpp
doLoadBalance = (proposedEfficiency > load_balance_efficiency_ratio_threshold*currentEfficiency);
```

源码位置：`../warpx/Source/Parallelization/WarpXRegrid.cpp:115-117`。

也就是说，WarpX 不是“到点必重分布”，而是“到点先比较收益，收益足够大才改图”。

## 4. 候选映射最初只在 root 上有效

`makeSFC` / `makeKnapSack` 的调用里把“是否广播结果”设成了 `false`。因此新映射最初只在 root 上是完整的。WarpX 先在 root 上决定是否重分布，再广播：

1. `doLoadBalance`
2. 若需要重分布，再广播 `ProcessorMap`

源码路径仍在 `WarpXRegrid.cpp:109-141`。

这个设计很重要，因为：

- 不必让所有 rank 都预先生成一份候选分布；
- 若 `proposedEfficiency` 不够好，整次重分布可以直接取消；
- 真正需要全体同步时，只广播最终 `pmap`。

因此 `LoadBalance()` 的核心结构不是“everyone recompute”，而是“root propose, all ranks commit”。

## 5. `RemakeLevel()`：不是 AMR regrid，而是“同一 BoxArray 上重做 level 数据布局”

一旦某个 level 决定采纳新映射，WarpX 调用：

```cpp
RemakeLevel(lev, t_new[lev], boxArray(lev), newdm);
```

源码位置：`../warpx/Source/Parallelization/WarpXRegrid.cpp:143`。

但 `RemakeLevel()` 的真实边界比函数名更窄。它开头直接检查：

```cpp
if (ba == boxArray(lev))
{
    if (ParallelDescriptor::NProcs() == 1) { return; }
    ...
} else
{
    WARPX_ABORT_WITH_MESSAGE("RemakeLevel: to be implemented");
}
```

源码位置：`../warpx/Source/Parallelization/WarpXRegrid.cpp:174-176, 283-286`。

这说明当前 `RemakeLevel()` 只支持：

- `DistributionMapping` 变化；
- `BoxArray` 不变。

它不是“任意 AMR regrid 重建器”，而是“同一 patch 切分下的重新分配器”。

## 6. 第一层重建：field registry 先整体 remake

`RemakeLevel()` 进入主体后，最先执行的是：

```cpp
m_fields.remake_level(lev, dm);
```

源码位置：`../warpx/Source/Parallelization/WarpXRegrid.cpp:178`。

这表示所有登记在 `FieldRegister` 里的 level 级场容器都要先按新 `dm` 重建。它不是只改几张 E/B 主场，而是整个 field registry 的 level 层整体换宿主 rank。

因此，从语义上看，load balance 已经不是“把粒子重新分给别的 rank”这么简单，而是先把场数据底座整体迁到新映射上。

## 7. 第二层重建：EB 辅助数据和 cut-cell 工厂必须一起重建

若开启 EB，`RemakeLevel()` 接着重建：

- `m_eb_reduce_particle_shape`
- `m_eb_update_E`
- `m_eb_update_B`
- ECT 下的 `m_borrowing`

对应源码：

```cpp
if (eb_enabled) {
    RemakeMultiFab( m_eb_reduce_particle_shape[lev] );
    if (WarpX::electromagnetic_solver_id != ElectromagneticSolverAlgo::PSATD) {
        RemakeMultiFab( m_eb_update_E[lev][idim] );
        RemakeMultiFab( m_eb_update_B[lev][idim] );
        if (WarpX::electromagnetic_solver_id == ElectromagneticSolverAlgo::ECT) {
            m_borrowing[lev][idim] = std::make_unique<amrex::LayoutData<FaceInfoBox>>(..., dm);
        }
    }
}
```

源码位置：`../warpx/Source/Parallelization/WarpXRegrid.cpp:182-193`。

之后还要重建带 EB 支持的 `FArrayBoxFactory`：

```cpp
int const max_guard = guard_cells.ng_FieldSolver.max();
m_field_factory[lev] = amrex::makeEBFabFactory(Geom(lev), ba, dm,
                                               {max_guard, max_guard, max_guard},
                                               amrex::EBSupport::full);
InitializeEBGridData(lev);
```

源码位置：`../warpx/Source/Parallelization/WarpXRegrid.cpp:198-204`。

这一步表明：EB 不是普通附加标签。只要 rank 映射变化，cut-cell factory、borrowed-face 拓扑和 update masks 都必须跟着 level 一起再生。

## 8. 第三层重建：PSATD 谱求解器的 real-space 容器也要重配

若当前 solver 是 PSATD，`RemakeLevel()` 还要为：

- `spectral_solver_fp[lev]`
- `spectral_solver_cp[lev]`

重建 real-space `BoxArray` 与 guard cells。

Fine patch 分支会：

- 把 `ba` 转成 cell-centered；
- 按 `getngEB()` 增加 guard cells；
- RZ 与 Cartesian 分开调用 `AllocLevelSpectralSolverRZ` / `AllocLevelSpectralSolver`。

Coarse patch 分支则：

- 先把 `ba` 按 `refRatio(lev-1)` coarsen；
- 再构造 coarse real-space `BoxArray`；
- 然后按同样逻辑重建 `spectral_solver_cp[lev]`。

对应源码范围：`../warpx/Source/Parallelization/WarpXRegrid.cpp:210-253`。

因此，load balance 改变的不只是实空间 `MultiFab` 的 owner，也会波及 PSATD 的谱求解器宿主布局。

## 9. 第四层重建：加速器 lattice、buffer masks、diagnostic functors

`RemakeLevel()` 的后半段还会重置三类经常被忽略的配套结构。

### 9.1 accelerator lattice

```cpp
m_accelerator_lattice[lev]->InitElementFinder(lev, gamma_boost, gett_new(), ba, dm);
```

源码位置：`../warpx/Source/Parallelization/WarpXRegrid.cpp:257`。

这说明束流线元搜索器也依赖 box 布局，不能在重映射后沿用旧索引。

### 9.2 buffer masks

若当前 level 维护 `current_buffer_masks` / `gather_buffer_masks`，则：

```cpp
RemakeMultiFab( current_buffer_masks[lev] );
RemakeMultiFab( gather_buffer_masks[lev] );
BuildBufferMasks();
```

源码位置：`../warpx/Source/Parallelization/WarpXRegrid.cpp:270-280`。

这意味着 coarse-fine buffer 区域不是静态几何表，而是依赖当前 `DistributionMapping` 的有效/重叠布局，需要在 remake 后重新生成。

### 9.3 diagnostics

函数结束前显式调用：

```cpp
multi_diags->InitializeFieldFunctors( lev );
```

源码位置：`../warpx/Source/Parallelization/WarpXRegrid.cpp:288-290`。

WarpX 注释说 reduced diagnostics 这一步“not needed yet”，但 field functor 级别的 diagnostics 指针已经必须重绑。

## 10. `costs` 和 `load_balance_efficiency` 也会被一并重置

若该 level 已启用 `costs[lev]`，`RemakeLevel()` 会重建新的 `LayoutData<Real>` 并清零：

```cpp
costs[lev] = std::make_unique<LayoutData<Real>>(ba, dm);
...
(*costs[lev])[i] = 0.0;
setLoadBalanceEfficiency(lev, -1);
```

源码位置：`../warpx/Source/Parallelization/WarpXRegrid.cpp:259-267`。

`setLoadBalanceEfficiency()` / `getLoadBalanceEfficiency()` 则在 `WarpX.cpp` / `WarpX.H` 中把这个量挂到 `load_balance_efficiency[lev]` 上，默认值也是 `-1`。

这正好对应官方参数文档中 `LoadBalanceEfficiency` 的说明：在 costs 尚未重新积累出来之前，它输出 `-1`，最早也要到 step 2 后才可能变成有效值。

## 11. 真正的粒子迁移发生在所有 level remake 之后

`LoadBalance()` 里并不是每 remake 一个 level 就立刻移动粒子，而是等所有 level 都判断完、并且至少有一个 level 真的 load balance 之后，再统一做：

```cpp
mypc->Redistribute();
mypc->defineAllParticleTiles();
m_particle_boundary_buffer->redistribute();
reduced_diags->LoadBalance();
```

源码位置：`../warpx/Source/Parallelization/WarpXRegrid.cpp:149-159`。

这里的顺序值得记住：

1. 先 remake 各层 field / EB / solver / masks / diagnostics pointers；
2. 再 redistribute 粒子；
3. 再重建 particle tiles；
4. 再同步 particle boundary buffer；
5. 最后让 reduced diagnostics 跟上新布局。

因此，WarpX 的 load balance 是“多子系统一致提交”，不是某一类对象的局部搬家。

## 12. heuristic costs 的真实定义

`ComputeCostsHeuristic()` 很直接：每个 box 的 cost 由粒子数和 cell 数两部分组成：

```cpp
(*a_costs[lev])[pti.index()] += costs_heuristic_particles_wt*pti.numParticles();
...
const Box& gbx = mfi.growntilebox();
(*a_costs[lev])[mfi.index()] += costs_heuristic_cells_wt*gbx.numPts();
```

源码位置：`../warpx/Source/Parallelization/WarpXRegrid.cpp:304-320`。

这与官方文档一致：

$$
c = n_{\text{particle}} \, w_{\text{particle}}
  + n_{\text{cell}} \, w_{\text{cell}}.
$$

文档入口：

- `../warpx/Docs/source/usage/parameters.rst`
- `../warpx/Docs/source/usage/parameters.rst` 中 `algo.load_balance_costs_update`
- `algo.costs_heuristic_particles_wt`
- `algo.costs_heuristic_cells_wt`

而且官方文档还说明，GPU 默认权重不是固定常数，而是按 solver 与 particle shape 从单 GPU 基准测试标定出来。

## 13. timer 模式不是重算 cost，而是做 running average

`RescaleCosts(step)` 只在 `load_balance_costs_update_algo == Timers` 时生效：

```cpp
(*costs[lev])[i] *= (1._rt - 2._rt/load_balance_intervals.localPeriod(step+1));
```

源码位置：`../warpx/Source/Parallelization/WarpXRegrid.cpp:345-347`。

这说明 timer 模式的思路不是“每次都丢掉旧计时重新开始”，而是维护一个偏向近期历史的 running average。与 heuristic 的“即时粒子数/网格数估计”相比，这是两种不同的成本模型。

## 14. `LoadBalanceCosts` / `LoadBalanceEfficiency` 诊断如何落到用户侧

官方 reduced diagnostics 文档定义了两类直接对应这里源码的数据：

- `LoadBalanceCosts`
- `LoadBalanceEfficiency`

其中：

- `LoadBalanceCosts` 输出每个 box 的 cost；
- `LoadBalanceEfficiency` 输出 mean cost / max cost；
- 在 costs 尚未记录前，efficiency 输出 `-1`。

另一个实用文档是：

- `../warpx/Docs/source/usage/workflows/plot_distribution_mapping.rst`

它给出：

```python
warpx.reduced_diags_names = LBC
LBC.type = LoadBalanceCosts
LBC.intervals = 100
```

以及后处理脚本 `Tools/PostProcessing/plot_distribution_mapping.py` 的使用方式，用于把 rank layout 和 box cost 可视化。

这意味着 `WarpXRegrid.cpp` 里的 `costs` 并不是内部黑箱；它本来就被设计成能通过 reduced diagnostics 暴露给用户分析分布映射质量。

## 15. 当前这一层的结论

`WarpXRegrid.cpp` 当前讲清了三件事：

1. WarpX 的 load balance 是“周期检查 + 效率比较 + 条件采纳”的策略，而不是到点强制搬运；
2. `RemakeLevel()` 目前只支持“同一 `BoxArray`，新 `DistributionMapping`”的 level 重映射；
3. 一旦采纳新映射，需要一起重建的不只是场和粒子，还包括 EB、PSATD、buffer masks、accelerator lattice、particle boundary buffer 和 diagnostics 绑定。

所以从工程上看，load balance 在 WarpX 中更像一次“level 级事务提交”，而不是单个 MPI utility。

## 16. 下一步应该读哪里

在 `Parallelization` 里，`WarpXRegrid.cpp` 之后最自然的两条路是：

1. 转到 AMR coarse-fine interface 与 substitution strategy，把第 7 章真正补到 refinement interface 的物理问题；
2. 继续 `WarpXComm_K.H`、`MFIter`、`ParallelFor`、GPU portability，把并行层从“通信结构”推进到“device kernel 执行模型”。

当前更优先的是第 1 条，因为第 7 章还缺 coarse-fine interface 的物理闭环。

# 粒子边界、`crop_on_PEC_boundary`、boundary buffer、sorting 与 Villasenor / suborbit 的交界层

绑定源码：

- `../warpx/Source/Evolve/WarpXEvolve.cpp`
- `../warpx/Source/Particles/WarpXParticleContainer.cpp`
- `../warpx/Source/Particles/ParticleBoundaries.cpp`
- `../warpx/Source/Particles/ParticleBoundaries_K.H`
- `../warpx/Source/Particles/ParticleBoundaryBuffer.cpp`
- `../warpx/Source/Particles/Pusher/ImplicitPushPX.cpp`
- `../warpx/Docs/source/usage/parameters.rst`

前面已经分别讲过：

- boundary 参数与 PEC / PECInsulator 语义
- implicit suborbit 与 Villasenor-only 重沉积
- `analysis_vandb_jfnk_2d_cropping.py` 如何把 PEC、absorbing、cropping、suborbit 绑成一条 regression

这一篇把它们重新接回同一条源码链：粒子真正到边界时，WarpX 先做什么、后做什么，`crop_on_PEC_boundary` 究竟改变哪一段轨迹解释，boundary buffer 又是在粒子删除前还是删除后收集。

## 1. 主循环里的真实顺序不是“删掉粒子再记日志”，而是“先处理边界、先收集、后清理”

`WarpX::HandleParticlesAtBoundaries()` 的顺序是：

```cpp
mypc->ApplyBoundaryConditions();
m_particle_boundary_buffer->gatherParticlesFromDomainBoundaries(*mypc, cur_time);
...
mypc->RedistributeLocal(...)  // or Redistribute()
...
mypc->ScrapeParticlesAtEB(...);
m_particle_boundary_buffer->gatherParticlesFromEmbeddedBoundaries(...);
mypc->deleteInvalidParticles();
...
mypc->SortParticlesByBin(...);
```

这条顺序很重要：

1. 先对粒子施加 domain boundary 条件；
2. 再把越界粒子复制到 domain boundary buffer；
3. 再做粒子重分布；
4. 若有 EB，再刮擦并复制到 EB buffer；
5. 最后才真正删除 invalid 粒子；
6. 排序始终在这些边界处理之后。

所以 scraped/boundary buffer 记录依赖的是“粒子还存在、但已经被标记或已越界”的中间状态，而不是事后从剩余粒子反推。

## 2. `boundary.particle_lo/hi` 默认是 `absorbing`，但 periodic 会被 field periodic 强制接管

`ParticleBoundaries.cpp` 先用

```cpp
auto particle_boundary_lo = ... ParticleBoundaryType::Default
```

初始化，再做两步：

1. 若用户没显式给 `boundary.particle_lo/hi`，则
   `set_to_periodic_if_field_boundary_is_periodic(...)`
   把 periodic field 方向上的粒子边界也设成 periodic；
2. 若用户显式给了粒子边界，则
   `check_consistency(...)`
   强制 periodic 必须 lo/hi 都 periodic，且与 field periodic 一致。

而 `ParticleBoundaries` 运行时对象本身的默认值是：

```cpp
SetAll(ParticleBoundaryType::Absorbing);
```

所以语义上是：

- 文档默认：粒子边界吸收；
- 但如果 field periodic，粒子 periodic 会被一致性逻辑接管；
- 不能出现 field periodic 但 particle 非 periodic 的混搭。

## 3. `ApplyBoundaryConditions()` 对 absorbing 的处理只是“标记 lost”，不负责立即删除

`WarpXParticleContainer::ApplyBoundaryConditions()` 对每个粒子调用：

```cpp
ApplyParticleBoundaries::apply_boundaries(..., particle_lost, boundary_conditions, engine);
```

若 `particle_lost` 为真：

```cpp
pidw.make_invalid();
```

否则才回写位置：

```cpp
SetPosition.AsStored(i, x, y, z);
```

因此这里的 absorbing / open 语义不是“立刻把粒子从 tile 数组删掉”，而是：

- 先把 `idcpu` 标成 invalid；
- 真正物理删除推迟到后面的 `deleteInvalidParticles()`。

这和 EB 的 `ParticleBoundaryProcess::Absorb()` 是同一个模式。

## 4. absorbing 并不总是 100% 吸收，它还可以带随机反射模型

`ParticleBoundaries_K.H` 里 absorbing 分支其实是：

```cpp
if (refl_probability_xmin == 0 || amrex::Random(engine) > refl_probability_xmin) {
    particle_lost = true;
}
else
{
    x = 2*xmin - x;
    change_sign_ux = true;
}
```

也就是说，absorbing 边界可以配置成“带反射概率的统计吸收边界”：

- 默认反射概率为 0，就是纯吸收；
- 若 parser 给出非零反射概率，则 absorbing 也可能反弹。

这意味着 boundary buffer 记录的不是“所有接触 absorbing 边界的粒子”，而是“最终确实离开域、仍被判定 lost 的粒子”。

## 5. `crop_on_PEC_boundary` 不是粒子边界条件，而是沉积/implicit push 对轨道的几何裁剪开关

`particles.crop_on_PEC_boundary` 在 `WarpXParticleContainer` 构造时读入：

```cpp
pp_particles.query("crop_on_PEC_boundary", m_crop_on_PEC_boundary);
```

官方文档也明确说它只在：

- `pec`
- `pec_insulator`

边界时起作用。

但真正消费它的地方并不是 `ApplyBoundaryConditions()`，而是 deposition / implicit push 路径里构造的：

```cpp
do_cropping[idim][side] = m_crop_on_PEC_boundary &&
    boundary_is_PEC_or_PECInsulator;
```

这说明：

- `boundary.particle_lo/hi` 控制粒子是否被删、反射、热化；
- `particles.crop_on_PEC_boundary` 控制当轨道穿到 PEC / PECInsulator 场边界外时，沉积或 implicit 子步是否把轨迹截到边界。

它们是两层不同语义，不应该混为“粒子边界参数”。

## 6. 显式 current/charge deposition 在进入 Villasenor / Esirkepov 前就拿到 `do_cropping`

`WarpXParticleContainer::DepositCurrent()` 在分派沉积算法前，会构造：

```cpp
amrex::GpuArray<amrex::GpuArray<bool,2>, AMREX_SPACEDIM> do_cropping;
amrex::GpuArray<amrex::GpuArray<double,2>, AMREX_SPACEDIM> domain_double;
```

其中 `do_cropping` 只在当前 tile 贴到物理边界、且该边界是 `PEC` 或 `PECInsulator` 时才置真。

后面无论是 explicit Villasenor、Esirkepov 还是 implicit 分支，真正的 kernel 都拿到这两个量。这说明 `crop_on_PEC_boundary` 改变的是：

- old/new 轨迹恢复
- crossing segment 的有效长度
- 边界外那段轨道是否还参与沉积

而不是“沉积后再做一个简单裁剪”。

## 7. implicit / suborbit 路径里，`crop_on_PEC_boundary` 进入得更早

`ImplicitPushPX.cpp` 在子轨道循环之前同样构造：

```cpp
do_cropping[idim][side] = m_crop_on_PEC_boundary && PEC_or_PECInsulator;
```

然后在每个 suborbit 开始时先判断：

```cpp
const bool this_suborbit_out_of_bounds =
    ParticleUtils::is_out_of_bounds(xp_n, yp_n, zp_n, dinv, xyzmin, domain_double, do_cropping);
```

也就是说，对 suborbit 粒子来说，`crop_on_PEC_boundary` 不只是影响沉积尾巴，而是直接进入：

- 当前子步是否已经越界；
- 是否允许后续 push / gather / deposition；
- `PushXPSingleStep(...)` 怎样理解当前轨道与域边界的关系。

这正好解释了为什么 `analysis_vandb_jfnk_2d_cropping.py` 必须把 `particles.crop_on_PEC_boundary = 1` 和 `implicit_evolve.particle_suborbits = 1` 绑在一起测。

## 8. suborbit 路径和 `crop_on_PEC_boundary` 的交界点，正是局部 Gauss 定律最脆弱的地方

在 `ImplicitPushPX.cpp` 里，真正做 deposition 的条件是：

```cpp
if (doing_deposition && !this_suborbit_out_of_bounds) {
    ...
}
```

也就是说，一旦当前 suborbit 初始位置已经被 `do_cropping` 判成越界：

- 这段子轨道不会继续沉积；
- 也不会再把边界外轨迹贡献偷偷加到 `J` 或 mass matrices。

这就是 `analysis_vandb_jfnk_2d_cropping.py` 能用

$$
\max |\rho - \epsilon_0 \nabla\cdot E|
$$

直接打到 `crop_on_PEC_boundary + suborbit + Villasenor` 组合上的原因。

## 9. boundary buffer 收集发生在 invalid 粒子真正删除之前

`ParticleBoundaryBuffer::gatherParticlesFromDomainBoundaries()` 的 predicate 是：

```cpp
auto predicate = IsOutsideDomainBoundary{plo, phi, idim, iside};
```

它遍历当前容器里的粒子，筛出已经离开给定方向物理域的粒子，然后用：

```cpp
filterAndTransformParticles(..., CopyAndTimestamp{...})
```

复制到 pinned-memory buffer 里，并额外记录：

- `stepScraped`
- `deltaTimeScraped`
- `timeScraped`
- `nx, ny, nz`

关键点是：这一步发生在 `deleteInvalidParticles()` 之前。因此 buffer 不是从“已删粒子列表”来，而是从“当前 tile 中仍可遍历到、但位置已越界/即将失效的粒子”来。

## 10. domain boundary buffer 和 EB buffer 是两套不同 predicate，但同一套时间戳接口

domain boundary buffer 用的是越界谓词 `IsOutsideDomainBoundary`；

EB buffer 用的是：

```cpp
phi_value < 0.0
```

判断粒子是否进入 embedded boundary。

但两者最终都写入同样的附加字段：

- `stepScraped`
- `deltaTimeScraped`
- `timeScraped`
- `nx, ny, nz`

其中 EB 路径还会在 `FindEmbeddedBoundaryIntersection` 里沿轨迹回溯真实交点。说明 WarpX 把“离开 domain 边界”和“撞到 EB”统一抽象成同一类 scraped-particle event，只是 predicate 和交点恢复不同。

## 11. `save_particles_at_*` 只是开启 buffer，不改变边界物理

`ParticleBoundaryBuffer` 构造时只读每个 species 的：

- `save_particles_at_xlo/xhi/...`
- `save_particles_at_eb`

然后设置 `m_do_boundary_buffer[...]`。

文档也说得很清楚：这些参数只是把粒子复制到 scraped particle buffer，方便：

- `BoundaryScrapingDiagnostic`
- Python 接口

它们不负责改变 particle boundary condition，也不决定粒子是否被删。真正的物理边界仍然由：

- `boundary.particle_lo/hi`
- field boundary
- `crop_on_PEC_boundary`

这些参数共同决定。

## 12. sorting 在边界处理之后，作用主要是为后续 deposition / locality 服务，不参与边界物理判定

`WarpX::HandleParticlesAtBoundaries()` 末尾才会：

```cpp
mypc->SortParticlesByBin(sort_bin_size, m_sort_particles_for_deposition, m_sort_idx_type);
```

`MultiParticleContainer::SortParticlesByBin()` 又分成两种：

- `SortParticlesForDeposition(sort_idx_type)`
- 普通 `SortParticlesByBin(bin_size)`

而 `WarpXParticleContainer::DepositCurrent()` / `DepositCharge()` 自己在某些路径下也会做 tile 内 bins/sort，用于 shared-memory 或性能优化。

因此这里的排序语义是：

- 边界处理、buffer 收集、invalid 删除先完成；
- 之后才重排剩余粒子布局，为接下来一步的局域沉积/缓存效率服务。

排序不应该改变“哪些粒子被吸收、哪些被 scrape、哪些轨迹被 crop”的物理判定。

## 13. 现在可以把 `analysis_vandb_jfnk_2d_cropping.py` 和源码主链一一对上

当输入里同时设置：

- `boundary.field_lo/hi = pec`
- `boundary.particle_lo/hi = absorbing`
- `particles.crop_on_PEC_boundary = 1`
- `implicit_evolve.particle_suborbits = 1`
- `algo.current_deposition = villasenor`

真正被同时拉进来的源码层是：

1. `ApplyParticleBoundaries::apply_boundaries()` 把越界粒子标为 lost 或反射；
2. `crop_on_PEC_boundary` 让 deposition / suborbit push 把轨迹截到 PEC/PECInsulator 边界；
3. suborbit path 只对未越界的子轨道继续做 Villasenor deposition；
4. boundary buffer 在 invalid 删除前记录 scraped event；
5. `deleteInvalidParticles()` 最后才物理移除粒子。

所以 `analysis_vandb_jfnk_2d_cropping.py` 的 `drho_max` 断言，实际是在检查这整条组合链有没有在局部电荷守恒上留下破洞。

## 14. 这条链和前面几篇笔记的关系

- 和 `09-radiation-reaction-implicit-photon-pushers.md` 的关系：
  这里补的是 implicit suborbit 粒子到边界时的后处理，不是 momentum pusher 本体。
- 和 `10-implicit-suborbit-mass-matrices-jfnk.md` 的关系：
  那篇解决 `J_0 + MM(E-E_0) + J_suborbit` 的线性化分拆；这一篇补的是 suborbit 粒子在边界/PEC/cropping 下哪些轨迹还允许进入这套分拆。
- 和 `boundary/02-pec-insulator-silver-mueller.md` / `03-boundary-parameter-table.md` 的关系：
  那两篇讲参数和 field boundary 语义；这一篇把 `particles.crop_on_PEC_boundary` 真正接到粒子推进和沉积代码。

## 15. 下一步最自然的继续方向

- 继续下钻 `SortParticlesForDeposition()`、`ParticleBoundaryBuffer` 和 `BoundaryScrapingDiagnostic` 的消费侧，把 scraped particle buffer 从“生产”接到“诊断输出”。
- 或转去 `Diagnostics/` 模块，把 `BoundaryScrapingDiagnostic`、reduced diagnostics、multi-level field/particle diagnostics 统一并入同一章。 

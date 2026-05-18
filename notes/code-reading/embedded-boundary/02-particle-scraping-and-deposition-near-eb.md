# EmbeddedBoundary 02: 粒子 scraping、吸收与边界缓冲

绑定源码：

- `../warpx/Source/EmbeddedBoundary/ParticleScraper.H`
- `../warpx/Source/EmbeddedBoundary/ParticleBoundaryProcess.H`
- `../warpx/Source/EmbeddedBoundary/DistanceToEB.H`
- `../warpx/Source/Particles/WarpXParticleContainer.cpp`
- `../warpx/Source/Particles/MultiParticleContainer.cpp`
- `../warpx/Source/Particles/ParticleCreation/AddParticles.cpp`
- `../warpx/Source/Particles/ParticleBoundaryBuffer.cpp`
- `../warpx/Docs/source/usage/parameters.rst`

## 1. 这一层要回答什么

前两篇已经把 embedded boundary 的几何初始化和 ECT face extension 讲清了，但对 PIC 来说还缺最关键的一层：

1. 宏粒子什么时候会被判定“已经撞进 EB”；
2. 默认动作到底是反射、吸收还是别的处理；
3. 如果用户要求记录 scraped 粒子，数据会落到哪里；
4. signed-distance 场和法向量怎样真正参与这条链。

`ParticleScraper.H`、`ParticleBoundaryProcess.H`、`DistanceToEB.H` 和 `ParticleBoundaryBuffer.cpp` 就是在回答这些问题。

## 2. `scrapeParticlesAtEB` 的职责：检测进入 EB 的粒子并执行回调

`ParticleScraper.H` 的注释已经写得很清楚：

- 用 signed distance function 检测粒子是否进入了 embedded boundary 覆盖区；
- 回调函数 `f` 决定撞墙后的具体处理；
- 处理函数可以吸收粒子，也可以反射粒子。

核心实现是：

```cpp
ablastr::particles::compute_weights<amrex::IndexType::NODE>(
    xp, yp, zp, plo, dxi, i, j, k, W);
amrex::Real const phi_value = ablastr::particles::interp_field_nodal(i, j, k, W, phi);

if (phi_value < 0.0)
{
    ...
    amrex::RealVect normal = DistanceToEB::interp_normal(i, j, k, W, ic, jc, kc, Wc, phi, dxi);
    DistanceToEB::normalize(normal);
    ...
    f(ptd, ip, pos, normal, engine);
}
```

源码位置：`../warpx/Source/EmbeddedBoundary/ParticleScraper.H:181-208`。

因此判断标准非常直接：

- 先对 nodal `distance_to_eb` 做插值；
- 如果插值结果 `phi_value < 0`，就认为粒子已经进入 EB 覆盖区域；
- 然后再构造碰撞位置 `pos` 和边界法向 `normal`，交给用户指定的处理 functor。

这和前面 `warpx.eb_implicit_function` 文档里的符号约定是一致的：EB 内部是正值还是负值，在运行时真正决定粒子命运的是 `distance_to_eb` 的实际符号语义，而 WarpX 在这里把 `phi_value < 0` 作为“已进入被刮擦区域”的判据。

## 3. 默认处理器非常简单：`Absorb` 只是把粒子 id 置无效

`ParticleBoundaryProcess.H` 只定义了两个最小处理器：

```cpp
struct NoOp {
    template <typename PData>
    ...
    void operator() (...) const noexcept
    {}
};

struct Absorb {
    template <typename PData>
    ...
    void operator() (PData& ptd, int i, ...) const noexcept
    {
        amrex::ParticleIDWrapper{ptd.m_idcpu[i]}.make_invalid();
    }
};
```

源码位置：`../warpx/Source/EmbeddedBoundary/ParticleBoundaryProcess.H:15-33`。

也就是说，当前 WarpX 在源码主链上对 EB 粒子的默认操作不是复杂的表面物理，而只是：

- `NoOp`：什么都不做；
- `Absorb`：把粒子标记成 invalid，等待后续清理。

所以 EB 粒子“吸收”的真实实现并不是当场从 tile 删除，而是先翻转 `idcpu` 有效位。

## 4. 真正删除发生在后处理：invalid 粒子稍后统一清掉

`WarpXParticleContainer` 在粒子重分布后，会立即做一轮 EB 刮擦：

```cpp
scrapeParticlesAtEB(
    *this,
    warpx.m_fields.get_mr_levels(FieldType::distance_to_eb, warpx.finestLevel()),
    ParticleBoundaryProcess::Absorb());
deleteInvalidParticles();
```

源码位置：`../warpx/Source/Particles/WarpXParticleContainer.cpp:347-351`。

这里说明两件事：

1. 刮擦依赖的就是 `FieldType::distance_to_eb`；
2. `Absorb()` 只是先标 invalid，真正移除发生在 `deleteInvalidParticles()`。

因此，EB 吸收链条是：

`distance_to_eb 插值判定 -> Absorb 标 invalid -> deleteInvalidParticles 真删除`

而不是一步完成。

## 5. 刮擦会出现在三类场景，而不只是主推进后

当前源码里，`scrapeParticlesAtEB(..., ParticleBoundaryProcess::Absorb())` 至少出现在三类地方。

### 5.1 新粒子加入主容器后立即清理

见 `WarpXParticleContainer.cpp` 上面的 `Redistribute()` 后处理。作用是防止刚加入主容器的粒子本来就落在 EB 里面。

### 5.2 批量物种容器级刮擦

`MultiParticleContainer::ScrapeParticlesAtEB()` 直接对所有 species 调用：

```cpp
for (auto& pc : allcontainers) {
    scrapeParticlesAtEB(*pc, distance_to_eb, ParticleBoundaryProcess::Absorb());
}
```

源码位置：`../warpx/Source/Particles/MultiParticleContainer.cpp:1152-1155`。

这给出一个更上层的统一入口。

### 5.3 初始化注入、通量注入后清理

在 `AddParticles.cpp` 里，无论是普通新增粒子还是 flux 注入后的临时容器，都有：

```cpp
scrapeParticlesAtEB(
    *this,
    warpx.m_fields.get_mr_levels(FieldType::distance_to_eb, warpx.finestLevel()),
    ParticleBoundaryProcess::Absorb());
```

以及：

```cpp
scrapeParticlesAtEB(
    tmp_pc,
    warpx.m_fields.get_mr_levels(FieldType::distance_to_eb, warpx.finestLevel()),
    ParticleBoundaryProcess::Absorb());
```

源码位置：`../warpx/Source/Particles/ParticleCreation/AddParticles.cpp:1218-1223` 与 `1748-1755`。

所以 WarpX 的策略不是“先让粒子进来，后面慢慢处理”，而是只要粒子新生成或新进入容器，就尽快做一次 EB 合法性筛选。

## 6. `DistanceToEB`：法向量来自 signed-distance 的离散梯度插值

`DistanceToEB.H` 做的事很少，但很关键：

- `dot_product`
- `normalize`
- `interp_normal`

`interp_normal()` 的核心不是解析几何求法线，而是从 `phi` 的离散值构造梯度近似。

例如 3D 下 `x` 分量是：

```cpp
normal[0] += sign * phi(icstart + ii, j + jj, k + kk)
             * dxi[0] * Wc[0][wccomp] * W[1][w1comp] * W[2][w2comp];
```

源码位置：`../warpx/Source/EmbeddedBoundary/DistanceToEB.H:52-61`。

随后 `normalize()` 再把这个梯度向量单位化：

```cpp
amrex::Real const inv_norm = 1.0_rt / std::sqrt(dot_product(a, a));
```

源码位置：`../warpx/Source/EmbeddedBoundary/DistanceToEB.H:24-31`。

这说明 WarpX 里的 EB 法向不是从 STL 面片直接读取，而是从 signed-distance 场的离散梯度重建出来的。

对 `XZ` / `RZ`，`interp_normal()` 退化为二维版本；对 `1D` 明确还没实现。

## 7. 刮擦位置和法向可以被记录到 scraped particle buffer

文档参数里明确给了：

- `<species_name>.save_particles_at_eb`

说明为：

- 若 `USE_EB=TRUE`，可把撞到 EB 的粒子复制到 scraped particle buffer；
- 可通过 `BoundaryScrapingDiagnostic` 或 Python 接口访问；
- Python 侧必须手动 `clear_buffer()`，否则缓冲区会无限增长。

文档位置：`../warpx/Docs/source/usage/parameters.rst:1890-1924`。

对应的开关在 `ParticleBoundaryBuffer.cpp`：

```cpp
if (eb_enabled) { pp_species.query("save_particles_at_eb", m_do_boundary_buffer[AMREX_SPACEDIM*2][ispecies]); }
```

源码位置：`../warpx/Source/Particles/ParticleBoundaryBuffer.cpp:285`。

这里很关键的一点是：EB buffer 被编码成 boundary buffer 的最后一个槽位 `AMREX_SPACEDIM*2`，也就是说它在内部被当作“额外的一类边界面”来管理。

## 8. 进入 EB buffer 时，粒子并不是简单原样复制

`ParticleBoundaryBuffer.cpp` 里专门定义了 `FindEmbeddedBoundaryIntersection` functor。它在复制到 buffer 时，会用二分法把粒子沿反向轨迹退回到 `phi = 0` 的交点：

```cpp
amrex::Real const dt_fraction = amrex::bisect( 0.0, 1.0,
    [=] (amrex::Real dt_frac) {
        ...
        UpdatePosition(x_temp, y_temp, z_temp, ux, uy, uz, -dt_frac*dt, mass);
        ...
        amrex::Real const phi_value = ablastr::particles::interp_field_nodal(i, j, k, W, phiarr);
        return phi_value;
    } );
```

源码位置：`../warpx/Source/Particles/ParticleBoundaryBuffer.cpp:92-104`。

找到交点后，它还会记录：

- `stepScraped`
- 到边界的剩余时间分数 `delta`
- 真实 scraping 时间
- 边界法向分量

并再次通过 `DistanceToEB::interp_normal()` 得到单位法向。见 `../warpx/Source/Particles/ParticleBoundaryBuffer.cpp:105-168`。

因此，scraped particle buffer 不是简单的“死亡粒子垃圾桶”，而是一个带边界交点和法向量信息的诊断缓冲区。

## 9. 当前源码边界：默认只有吸收，没有复杂 EB 表面物理

把 `ParticleScraper.H`、`ParticleBoundaryProcess.H`、`ParticleBoundaryBuffer.cpp` 连起来看，可以得到一个很具体的边界判断：

1. WarpX 已经具备：
   - 基于 signed-distance 的撞墙检测；
   - 基于离散梯度的表面法向重建；
   - 默认吸收；
   - scraped buffer 记录与交点回溯。
2. 当前默认主链里没有看到更复杂的：
   - 通用 EB 反射模型
   - 材料依赖二次电子发射
   - 表面粗糙度散射
   - 依赖表面物性的粒子再发射

所以目前 EB 粒子边界在主源码主链上的默认语义，仍然是“检测进入 cut region 的粒子并吸收，可选把交点信息存档”。

## 10. `embedded_circle` 当前在回归索引里的正确位置

`Examples/Tests/embedded_circle/inputs_test_2d_embedded_circle` 很容易被误写成笼统的 “embedded boundary test”。当前源码树里，它的真实角色更具体：

- `warpx.do_electrostatic = labframe`
- `warpx.eb_implicit_function = -((x-0.00005)^2+(z-0.00005)^2-1e-05^2)`
- `warpx.eb_potential(x,y,z,t) = -10`
- `electrons/ar_ions.initialize_self_fields = 1`
- `coll_electrons/coll_ar_ions.type = background_mcc`
- `electrons/ar_ions.save_particles_at_eb = 1`
- `diag3.diag_type = BoundaryScraping`
- `algo.load_balance_costs_update = timers`

同时，`CMakeLists.txt` 里这条 test 是：

- `analysis = OFF`
- 只复用顶层 `analysis_default_regression.py --path diags/diag1000011 --rtol 1e-2`

因此它当前不应再写成：

- electrostatic sphere 那类解析 `phi/Er` 强基准
- point-of-contact / scraping 那类带独立几何断言的强 analysis
- 单纯的 EB geometry smoke test

它更准确的定位是：

- `2D circular embedded-boundary electrostatic + PIC-MCC + BoundaryScraping workflow baseline`

也就是说，这条 regression 当前主要覆盖的是：

1. circular `eb_implicit_function` 几何真的进入 EB2；
2. `eb_potential` 参与电静求解；
3. 预置电子/离子 `initialize_self_fields` 与导体几何共存；
4. `background_mcc` 在同一场景下持续运行；
5. `save_particles_at_eb` 与 `BoundaryScraping` 能把撞击到 EB 的粒子写到 diagnostics；
6. timer-based load balance 不把这条多物理工作流搞坏。

## 11. 当前可以得到的结构性结论

到这一层为止，embedded boundary 的粒子侧主链可以概括为：

1. `ComputeDistanceToEB()` 先生成 signed-distance 场；
2. `scrapeParticlesAtEB()` 在 nodal `phi` 上插值，`phi_value < 0` 时认为粒子已进入 EB；
3. `DistanceToEB::interp_normal()` 从离散 `phi` 梯度构造法向；
4. 默认 `ParticleBoundaryProcess::Absorb()` 只把粒子标成 invalid；
5. 后续 `deleteInvalidParticles()` 或 `Redistribute()` 才真正清理；
6. 若启用 `<species>.save_particles_at_eb = 1`，则 `ParticleBoundaryBuffer` 会把粒子回溯到 `phi=0` 交点，并记录时间与法向。

所以 WarpX 的 EB 粒子处理不是“几何裁切附带删除”，而是一条完整的：

`distance field -> hit detection -> normal reconstruction -> process functor -> deletion/buffer recording`

链条。

## 12. 验证入口

和粒子刮擦最直接相关的测试入口包括：

- `../warpx/Examples/Tests/embedded_boundary_em_particle_absorption/`
- `../warpx/Regression/Checksum/benchmarks_json/test_2d_embedded_boundary_em_particle_absorption_sh_factor_1.json`
- `../warpx/Regression/Checksum/benchmarks_json/test_2d_embedded_boundary_em_particle_absorption_sh_factor_2.json`
- `../warpx/Regression/Checksum/benchmarks_json/test_2d_embedded_boundary_em_particle_absorption_sh_factor_3.json`
- `../warpx/Regression/Checksum/benchmarks_json/test_3d_embedded_boundary_em_particle_absorption_sh_factor_1.json`
- `../warpx/Regression/Checksum/benchmarks_json/test_rz_embedded_boundary_em_particle_absorption_sh_factor_1.json`
- `../warpx/Regression/Checksum/benchmarks_json/test_2d_embedded_boundary_removal_depth_sh_factor_1.json`
- `../warpx/Regression/Checksum/benchmarks_json/test_3d_embedded_boundary_removal_depth_sh_factor_1.json`

本轮没有运行这些 case；这里只补源码和验证入口映射。

## 13. 下一步

`EmbeddedBoundary` 模块目前已经完成：

1. 初始化与 distance field
2. face extension
3. particle scraping / boundary buffer

下一步最自然的是从 `EmbeddedBoundary/` 切回更大的 `Boundary / AMR` 主线，优先进入：

1. `Parallelization/` 的 guard cells、communication、sum guard cells
2. 或 AMR coarse-fine / subcycling interface

这样才能把第 7 章从“边界与 EB”继续推进到真正的“边界与 AMR 闭环”。

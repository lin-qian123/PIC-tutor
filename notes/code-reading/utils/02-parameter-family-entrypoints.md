# 参数族入口源码图

绑定源码：

- `../warpx/Source/WarpX.cpp`
- `../warpx/Source/Initialization/WarpXAMReXInit.cpp`
- `../warpx/Source/BoundaryConditions/FieldBoundaries.cpp`
- `../warpx/Source/Particles/MultiParticleContainer.cpp`
- `../warpx/Source/Particles/WarpXParticleContainer.cpp`
- `../warpx/Source/Particles/Collision/CollisionHandler.cpp`
- `../warpx/Source/Diagnostics/MultiDiagnostics.cpp`
- `../warpx/Source/Diagnostics/Diagnostics.cpp`
- `../warpx/Source/Diagnostics/ReducedDiags/MultiReducedDiags.cpp`
- `../warpx/Source/FieldSolver/ImplicitSolvers/ThetaImplicitEM.cpp`

这篇笔记不再解释“某个参数物理上是什么意思”，而只回答一个更基础的问题：

1. 某一族参数第一次在哪里被读入；
2. 它是在全局预检查层、对象工厂层，还是实例内部配置层生效；
3. 后续查参数时，应该先打开哪个源码入口。

---

## 1. 总图

对于当前最常查的九族参数：

- `species / particles.*`
- `lasers.*`
- `diagnostics.*`
- `reduced diagnostics.*`
- `collisions.*`
- `boundary / PML / periodicity`
- `solver / electrostatic / timestep / filter`
- `psatd.*`
- `implicit_evolve.*`

WarpX 的读取结构并不是“一次性从 `parameters.rst` 映射到一个函数”，而是三层壳：

1. 全局预检查层：
   `WarpX.cpp::ReadParameters()` 先决定对象图是否需要创建、是否存在非法组合。
2. 工厂/容器层：
   `MultiParticleContainer`、`MultiDiagnostics`、`MultiReducedDiags`、`CollisionHandler`
   读取名字列表并分派具体对象。
3. 实例内部配置层：
   具体 species container、diagnostic 实例或 collision 实例再读取各自前缀下的细参数。

因此，参数索引里写“第一次解析位置”时，最好区分成：

- `global gate`
- `factory dispatch`
- `instance-local parse`

---

## 2. Species / Particles

### 2.1 全局预检查层：`WarpX.cpp::ReadParameters()`

`WarpX` 构造期会先检查 simulation 是否真的包含 species 或 laser：

```cpp
std::vector<std::string> species_names;
pp_particles.queryarr("species_names", species_names);

std::vector<std::string> lasers_names;
pp_lasers.queryarr("names", lasers_names);

if (!species_names.empty() || !lasers_names.empty()) {
    ...
}
```

这里的作用不是读取每个 species 的全部物理参数，而是：

- 决定后面是否真的需要粒子容器；
- 在更早阶段拦下和 grid / solver / geometry 有关的非法组合。

### 2.2 工厂层：`MultiParticleContainer::ReadParameters()`

真正把 `particles.species_names` 变成对象图的是这里：

```cpp
pp_particles.queryarr("species_names", species_names);
auto const nspecies = species_names.size();

...

std::vector<std::string> rigid_injected_species;
pp_particles.queryarr("rigid_injected_species", rigid_injected_species);

...

std::vector<std::string> photon_species;
pp_particles.queryarr("photon_species", photon_species);
```

这里同时做三件事：

1. 读取 species 名字列表；
2. 读取跨-species 的全局粒子选项：
   `deposit_on_main_grid`、`gather_from_main_grid`、`rigid_injected_species`、`photon_species`；
3. 把每个名字映射成容器类型：
   `Physical`、`RigidInjected`、`Photon`。

也就是说：

- `particles.species_names` 是容器工厂入口；
- `particles.rigid_injected_species`、`particles.photon_species` 不是某个单 species 的内部细节，而是对象分派开关。

### 2.3 实例内部配置层：`WarpXParticleContainer::ReadParameters()`

进入每个具体容器后，还会再做一轮更局部的读取：

```cpp
void
WarpXParticleContainer::ReadParameters ()
{
    static bool initialized = false;

    if (!initialized)
    {
        const ParmParse pp_particles("particles");
        pp_particles.query("do_tiling", do_tiling);
        initialized = true;
    }
}
```

这层很重要，因为它说明：

- 有些 `particles.*` 参数不是对象图参数，也不是单 species 参数；
- 它们属于“所有粒子容器共享的执行层合同”，例如 `do_tiling`。

而真正的 `<species_name>.*` 参数，则在更深的 species 初始化链和具体容器逻辑中继续被消费：

- `PlasmaInjector`
- `SpeciesUtils`
- `PhysicalParticleContainer`
- `InitIonizationModule`
- `InitQED`

因此，`species` 参数查找顺序应当是：

1. `WarpX.cpp::ReadParameters()` 看是否有全局门闩；
2. `MultiParticleContainer::ReadParameters()` 看是否影响容器类型；
3. 再进入对应单 species 模块。

---

## 3. Lasers

### 3.1 全局预检查层：`WarpX.cpp::ReadParameters()`

laser 是否存在，先在 `WarpX.cpp` 里和 species 一起被预检查：

```cpp
std::vector<std::string> lasers_names;
pp_lasers.queryarr("names", lasers_names);

if (!lasers_names.empty() && n_rz_azimuthal_modes < 2) {
    ...
}
```

这层主要负责：

- 判断 simulation 是否包含 laser；
- 做 geometry / RZ mode / moving-window 这类全局合法性检查。

### 3.2 工厂层：`MultiParticleContainer::ReadParameters()`

真正把 `lasers.names` 变成 laser 容器的是：

```cpp
const ParmParse pp_lasers("lasers");
pp_lasers.queryarr("names", lasers_names);
auto const nlasers = lasers_names.size();

m_laser_deposit_on_main_grid.resize(nlasers, false);
std::vector<std::string> tmp;
pp_lasers.queryarr("deposit_on_main_grid", tmp);
```

这里的职责和 species 工厂层类似：

- 读取 laser 名字列表；
- 读取跨-laser 的 AMR 行为参数：
  `lasers.deposit_on_main_grid`；
- 让后续构造函数把名字分派到 `LaserParticleContainer`。

也就是说：

- `lasers.names` 是 laser 工厂入口；
- `<laser_name>.*` 细参数不是在这里读，而是在具体 `LaserParticleContainer` / profile 内部读取。

---

## 4. Diagnostics

### 4.1 顶层工厂：`MultiDiagnostics::ReadParameters()`

普通 diagnostics 的第一入口非常明确：

```cpp
const ParmParse pp_diagnostics("diagnostics");

int enable_diags = 1;
pp_diagnostics.query("enable", enable_diags);
if (enable_diags == 1) {
    pp_diagnostics.queryarr("diags_names", diags_names);
    ndiags = static_cast<int>(diags_names.size());
}

for (int i=0; i<ndiags; i++){
    const ParmParse pp_diag_name(diags_names[i]);
    std::string diag_type_str;
    pp_diag_name.get("diag_type", diag_type_str);
    ...
}
```

这里同时完成：

1. `diagnostics.enable` 总开关；
2. `diagnostics.diags_names` 名字列表；
3. `<diag_name>.diag_type` 到 `Full / TimeAveraged / BackTransformed / BoundaryScraping`
   的工厂分派。

这意味着：

- `diagnostics.*` 先归 `MultiDiagnostics`；
- `<diag_name>.diag_type` 是对象工厂参数，不只是 writer 细节。

### 4.2 实例内部配置层：`Diagnostics.cpp`

进入具体 diagnostics 实例后，才开始读取 fields/species/filter/writer 细项：

```cpp
const bool pfield_species_specified = pp_diag_name.queryarr("particle_fields_species", m_pfield_species);
...
const bool lo_specified = utils::parser::queryArrWithParser(
    pp_diag_name, "diag_lo", m_lo, 0, AMREX_SPACEDIM);
...
const bool species_specified =
    pp_diag_name.queryarr("species", m_output_species_names);
```

所以 `<diag_name>.*` 又能继续分成两层：

- 实例级布局/物理内容参数：
  `fields_to_plot`、`particle_fields_*`、`species`、`diag_lo/hi`；
- writer/back-end 参数：
  `format`、`openpmd_*`、`adios2_*`、`file_prefix`、`plot_raw_fields*`。

### 4.3 Reduced diagnostics 顶层入口：`MultiReducedDiags`

reduced diagnostics 走的不是 `diagnostics.*`，而是单独的 warpx 根前缀：

```cpp
const ParmParse pp_warpx("warpx");
m_plot_rd = pp_warpx.queryarr("reduced_diags_names", m_rd_names);

...

const ParmParse pp_rd_name(rd_name);
std::string rd_type;
pp_rd_name.get("type", rd_type);
```

所以这组参数的定位应当是：

- `warpx.reduced_diags_names`：
  顶层工厂入口；
- `<reduced_diag>.type`：
  reduced-diagnostic 类型工厂参数；
- 其余 `<reduced_diag>.*`：
  各具体 reduced diag 子类内部读取。

---

## 5. Collisions

### 5.1 全局预检查层：`WarpX.cpp::ReadParameters()`

`WarpX.cpp` 会先检查 simulation 是否启用 collisions：

```cpp
amrex::Vector<std::string> collision_names;
pp_collisions.queryarr("collision_names", collision_names);
if (!collision_names.empty()) {
    ...
}
```

这层作用仍然是：

- 让主对象图知道后面需要 collision subsystem；
- 在更高层做 compatibility gate。

### 5.2 工厂层：`CollisionHandler`

真正把 `collisions.collision_names` 和 `<collision_name>.type` 变成对象的是：

```cpp
const amrex::ParmParse pp_collisions("collisions");
pp_collisions.queryarr("collision_names", collision_names);

for (int i = 0; i < static_cast<int>(ncollisions); ++i) {
    const amrex::ParmParse pp_collision_name(collision_names[i]);

    std::string type = "pairwisecoulomb";
    pp_collision_name.query("type", type);
    collision_types[i] = type;

    if (type == "pairwisecoulomb") { ... }
    else if (type == "background_mcc") { ... }
    else if (type == "pulsed_decay") { ... }
    ...
}
```

这层决定的是：

- 这是不是 `BinaryCollision`；
- 是不是 `BackgroundMCC`、`PulsedDecay`、`BackgroundStopping`；
- 若是 binary 分支，后半段用哪种 `CollisionFunc` / `CreationFunc` 模板。

因此：

- `collisions.collision_names`：
  collision 工厂入口；
- `<collision_name>.type`：
  collision 子系统的最关键分派参数；
- `<collision_name>.species/product_species/...`：
  后续在 `CollisionBase` 和具体 collision 分支里继续读取。

---

## 6. Boundary / PML / Periodicity

### 6.1 全局预检查层：`WarpX.cpp::ReadParameters()`

边界参数不是一开始就在某个 boundary 对象里逐项读取。

`WarpX.cpp` 先在构造前期调用统一 helper：

```cpp
field_boundary_lo = warpx::boundary_conditions::get_field_boundary_lo_hi();
field_boundary_hi = warpx::boundary_conditions::get_field_boundary_lo_hi(false);
particle_boundary_lo = warpx::boundary_conditions::get_particle_boundary_lo_hi();
particle_boundary_hi = warpx::boundary_conditions::get_particle_boundary_lo_hi(false);
```

这层的作用是：

- 在 `WarpX` 主对象创建前，把场边界和粒子边界先锁成全局状态；
- 让后续 geometry、PML、periodicity 和粒子边界逻辑能直接消费枚举值；
- 及早做不合法组合的断言。

### 6.2 helper / parser 层：`FieldBoundaries.cpp` 与 `WarpXAMReXInit.cpp`

真正把 `boundary.field_lo/hi` 字符串变成 enum 的第一入口，是：

```cpp
const amrex::ParmParse pp_boundary("boundary");

pp_boundary.getarr(field_boundary, is_lo ? "field_lo" : "field_hi");

for (int idim = 0; idim < AMREX_SPACEDIM; ++idim) {
    amrex::Parser const parser(field_boundary[idim]);
    std::string val = parser.expr();
    amrex::toLower(val);
    amrex::getEnum(val, bc_lo_hi[idim]);
}
```

而 `WarpXAMReXInit.cpp` 会进一步把它们压成 AMReX 的 periodicity 数组：

```cpp
auto field_boundary_lo = warpx::boundary_conditions::get_field_boundary_lo_hi();
auto field_boundary_hi = warpx::boundary_conditions::get_field_boundary_lo_hi(false);
...
is_periodic[idim] = (field_boundary_lo[idim] == FieldBoundaryType::Periodic &&
                     field_boundary_hi[idim] == FieldBoundaryType::Periodic) ? 1 : 0;
```

因此这组参数的三层壳应理解为：

- `global gate`：
  `WarpX.cpp` 读取 helper 返回值并把边界类型锁进运行态；
- `factory/helper dispatch`：
  `FieldBoundaries.cpp` / `ParticleBoundaries.cpp` 负责字符串到 enum 的统一解析；
- `instance-local parse`：
  后续 PML、Silver-Mueller、particle boundary process、scraping buffer 等模块只消费已解析好的枚举和几何状态。

### 6.3 这一族参数应怎样查

最容易误判的是把：

- `boundary.field_lo/hi`
- `boundary.particle_lo/hi`
- `warpx.pml_*`
- `geometry.is_periodic`

都当成“同一层输入”。

更准确的查法是：

1. 先看 `FieldBoundaries.cpp` / `ParticleBoundaries.cpp`：
   确认字符串怎样转 enum；
2. 再看 `WarpXAMReXInit.cpp`：
   确认 periodicity 怎样被反推出 AMReX geometry；
3. 最后再去 boundary / PML / particle boundary 模块看运行期消费。

---

## 7. Solver / Electrostatic / Timestep / Filter

### 7.1 全局门闩集中在 `WarpX.cpp::ReadParameters()`

这组参数没有单独的 `Multi*` 工厂层，而是直接在 `WarpX.cpp::ReadParameters()` 里决定主对象图：

```cpp
pp_warpx.query_enum_sloppy("do_electrostatic", electrostatic_solver_id, "-_");
pp_warpx.query_enum_sloppy("poisson_solver", poisson_solver_id, "-_");

queryWithParser(pp_warpx, "const_dt", m_const_dt);
queryWithParser(pp_warpx, "max_dt", m_max_dt);
pp_warpx.queryarr("dt_update_interval", dt_interval_vec);

pp_warpx.query("use_filter", use_filter);
pp_warpx.query("use_filter_compensation", use_filter_compensation);
queryArrWithParser(pp_warpx, "filter_npass_each_dir",
                   filter_npass_each_dir, 0, AMREX_SPACEDIM);
```

这里的作用不是“给某个 solver 对象补几个细节参数”，而是：

- 决定 simulation 走 electromagnetic 还是 electrostatic 主分支；
- 选 Poisson 解法；
- 决定时间步控制是否是 `const_dt / max_dt / dt_update_interval` 混合合同；
- 决定 filter 是否存在，并因此影响 guard-cell / communication 资源。

### 7.2 同层读取但语义各异的辅助族

同一个 `WarpX.cpp::ReadParameters()` block 里还会读：

```cpp
queryWithParser(pp_warpx, "pml_ncell", pml_ncell);
queryWithParser(pp_warpx, "pml_delta", pml_delta);
pp_warpx.query("pml_has_particles", pml_has_particles);

pp_warpx.query("num_mirrors", num_mirrors);
queryArrWithParser(pp_warpx, "mirror_z", mirror_z, 0, num_mirrors);
```

这些参数虽然也在 root 层被 parse，但不应和 solver 主门闩混为一谈：

- `pml_*`：
  后面会进入 boundary/PML 子系统；
- `mirror_*`：
  是 laser / in-domain mirror 合同；
- `synchronize_velocity_for_diagnostics`：
  则是 diagnostics 前置状态同步门闩。

因此这组参数的结构是：

- `global gate`：
  几乎全部在 `WarpX.cpp::ReadParameters()`；
- `factory dispatch`：
  基本没有独立 `Multi*` 工厂层；
- `instance-local parse`：
  真正的 solver / filter / diagnostics 对象随后只消费已写入的 `WarpX` 成员状态。

---

## 8. PSATD

### 8.1 顶层门闩仍在 `WarpX.cpp`

`psatd.*` 不是独立 startup 文件先处理，而是在 solver 选择完成后才进入专属 parse 块：

```cpp
if (electromagnetic_solver_id == ElectromagneticSolverAlgo::PSATD)
{
    const ParmParse pp_psatd("psatd");
    pp_psatd.query("periodic_single_box_fft", fft_periodic_single_box);
    pp_psatd.query_enum_sloppy("solution_type", m_psatd_solution_type, "-_");
    pp_psatd.query("JRhom", JRhom_input);
    pp_psatd.query("current_correction", current_correction);
    pp_psatd.query("update_with_rho", update_with_rho);
    ...
}
```

这意味着：

- `algo.maxwell_solver = psatd` 才是第一道门；
- `psatd.*` 整族参数不是总会被读取；
- 若 solver 不是 PSATD，这一族参数在本轮运行里根本不会进入有效 parse 路径。

### 8.2 PSATD 内部也有一层“小型字符串到状态”的分派

这组参数里最容易被低估的是 `JRhom` 和速度向量：

```cpp
pp_psatd.query("JRhom", JRhom_input);
...
queryArrWithParser(pp_psatd, "v_galilean", m_v_galilean, 0, 3);
queryArrWithParser(pp_psatd, "v_comoving", m_v_comoving, 0, 3);
```

也就是说，`psatd.*` 自己内部又混合了三类读取壳：

- 普通标量布尔：
  `current_correction`、`update_with_rho`；
- enum 选择：
  `solution_type`；
- parser/字符串再解释：
  `JRhom`、`v_galilean`、`v_comoving`。

因此这组参数的查法应当是：

1. 先看 `algo.maxwell_solver` 是否把主分支切到了 PSATD；
2. 再看 `WarpX.cpp` 的 PSATD 专属 parse block；
3. 最后再进入 `SpectralSolver` / `PsatdAlgorithm*` 看运行时消费。

---

## 9. Implicit / Nonlinear Solver / Preconditioner

### 9.1 第一层仍是 `algo.evolve_scheme`

implicit 参数族的真正第一入口，不是 `implicit_evolve.theta`，而是：

```cpp
pp_algo.query_enum_sloppy("evolve_scheme", evolve_scheme, "-_");
```

只有当这里分派到：

- `SemiImplicitEM`
- `ThetaImplicitEM`
- `StrangImplicitSpectralEM`

后续的 implicit solver 对象和 nonlinear solver/preconditioner 才会存在。

因此：

- `algo.evolve_scheme` 是 implicit 族的 `global gate`；
- `implicit_evolve.*` 只是对象存在之后的实例内部参数。

### 9.2 实例内部配置层：`ThetaImplicitEM.cpp`

真正的 `implicit_evolve.*` 前缀读取发生在具体 implicit solver 类内部：

```cpp
const ParmParse pp("implicit_evolve");
pp.query("theta", m_theta);
parseNonlinearSolverParams(pp);
```

这里说明 implicit 族的结构是：

- `global gate`：
  `WarpX.cpp::ReadParameters()` 里的 `algo.evolve_scheme` 和兼容性断言；
- `factory dispatch`：
  由 evolve scheme 决定构造哪种 implicit solver；
- `instance-local parse`：
  `ThetaImplicitEM` / 其它 implicit solver 再读取 `implicit_evolve.*`、nonlinear solver、preconditioner 细项。

### 9.3 这一族参数为什么不能只看 `parameters.rst`

如果只从文档表面看，很容易误以为：

- `algo.evolve_scheme`
- `implicit_evolve.theta`
- nonlinear / preconditioner 参数

是同层平铺的。

源码里更准确的关系是：

1. `algo.evolve_scheme` 先决定有没有 implicit 子系统；
2. implicit solver 构造期再读 `implicit_evolve.*`；
3. preconditioner / nonlinear solver 参数通过 `parseNonlinearSolverParams(pp)` 继续向更深层对象传播。

---

## 10. 这篇图谱如何与参数索引配合

如果只是想知道“某个参数应回哪章”，先看：

- `docs/parameter-chapter-index.md`

如果要继续追“这个参数第一次在哪个函数里把字符串变成对象图或实例配置”，先看本篇，再顺着这里的入口继续下钻。

建议的最短路径：

1. 先看 `docs/parameter-chapter-index.md` 确认章节归属；
2. 再看本篇确认它属于：
   - `global gate`
   - `factory dispatch`
   - `instance-local parse`
3. 然后才进入对应模块笔记或源码文件。

---

## 11. 当前边界

这篇笔记还没有覆盖所有参数族。

当前已经压实的入口包括：

- `species / particles`
- `lasers`
- `diagnostics / reduced diagnostics`
- `collisions`
- `boundary / PML / periodicity`
- `solver / electrostatic / timestep / filter`
- `psatd`
- `implicit`

后续自然延伸方向是：

1. 继续补 `hybrid_pic_model / macroscopic / effective potential / fluid` 这组较深的 solver-object 参数入口；
2. 再补 `EB geometry builder / boundary process callback / Python front-end` 这类更偏应用接口的参数入口；
3. 最后把参数入口图和书稿正文中的参数表做双向链接。

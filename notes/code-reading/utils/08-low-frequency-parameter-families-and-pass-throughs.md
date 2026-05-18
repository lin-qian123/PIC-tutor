# 08. 低频参数族、聚合 alias 与 pass-through 输入

这一篇不是继续解释高频物理参数，而是专门处理 `parameter-map.md` 里最后那批容易长期悬空的条目：它们大多不是“没源码”，而是落在三种更绕的输入合同里：

1. 文档把多个真实键合并写成一个 `pp:param` alias；
2. 参数真正由 AMReX 或下层对象读取，WarpX 只消费结果；
3. 参数要先经过 root gate，再在子对象或运行态 materialization 阶段生效。

当前这批代表项包括：

- `amr.ref_ratio` / `amr.ref_ratio_vect`
- `geometry.prob_lo/hi`
- `warpx.fine_tag_lo/hi`
- `warpx.ref_patch_function(x,y,z)`
- `boundary.field_lo/hi`
- `boundary.potential_lo/hi_x/y/z`
- `boundary.particle_lo/hi`
- `warpx.E/B_external_grid`
- `particles.E/B_ext_particle_init_style`
- `<fluid_species_name>.E/B_ext_init_style`
- `psatd.nox/noy/noz`
- `psatd.nx/ny/nz_guard`
- `macroscopic.sigma/epsilon/mu`
- `macroscopic.sigma/epsilon/mu_function(x,y,z)`
- `hybrid_pic_model.plasma_resistivity(rho,J)`
- `hybrid_pic_model.plasma_hyper_resistivity(rho,B)`
- `hybrid_pic_model.J[x/y/z]_external_grid_function(x,y,z,t)`
- `warpx.field_centering_nox/noy/noz`
- `warpx.current_centering_nox/noy/noz`
- `amrex.async_out`
- `amrex.async_out_nfiles`
- `warpx.field/particle_io_nfiles`
- `qed_schwinger.xmin/ymin/zmin/xmax/ymax/zmax`

## 8.1 grouped alias 不等于单一 parser key

`parameters.rst` 里有不少条目为了文档可读性，会把一组真实键合并成一个 alias 名称。源码里真正读取的仍然是拆开的键。

`geometry.prob_lo/hi` 就是最清楚的例子。WarpX 没有读取字面上的 `"prob_lo/hi"`，而是在 AMReX 初始化后分别预解析 `prob_lo` 和 `prob_hi`：

```cpp
utils::parser::getArrWithParser(
    pp_geometry, "prob_lo", prob_lo, 0, AMREX_SPACEDIM);
utils::parser::getArrWithParser(
    pp_geometry, "prob_hi", prob_hi, 0, AMREX_SPACEDIM);

pp_geometry.addarr("prob_lo", prob_lo);
pp_geometry.addarr("prob_hi", prob_hi);
```

这说明：

- 文档 alias `geometry.prob_lo/hi` 只是“成对出现”的写法；
- 真正的 parser key 仍然是 `prob_lo` 和 `prob_hi`；
- `WarpXAMReXInit.cpp::parse_geometry_input()` 还会把表达式求值后回写，保证后续 AMReX geometry 和 job-info 看到的是数值结果。

同一类 grouped alias 还包括：

- `warpx.fine_tag_lo/hi`
- `boundary.field_lo/hi`
- `boundary.particle_lo/hi`
- `boundary.potential_lo/hi_x/y/z`
- `warpx.field_centering_nox/noy/noz`
- `warpx.current_centering_nox/noy/noz`
- `psatd.nox/noy/noz`
- `psatd.nx/ny/nz_guard`
- `qed_schwinger.xmin/ymin/zmin/xmax/ymax/zmax`

这些条目在 `parameter-map` 里如果只按 alias 名字搜源码，很容易得出“没命中”的假象。

## 8.2 refinement alias 有两条真正入口

AMR patch 定义这一组里，`warpx.fine_tag_lo/hi` 和 `warpx.ref_patch_function(x,y,z)` 不是并列重复功能，而是两条互斥但可以同时声明的 refinement 入口：

```cpp
const bool fine_tag_lo_specified = utils::parser::queryArrWithParser(pp_warpx, "fine_tag_lo", lo);
const bool fine_tag_hi_specified = utils::parser::queryArrWithParser(pp_warpx, "fine_tag_hi", hi);
std::string ref_patch_function;
const bool parser_specified = pp_warpx.query("ref_patch_function(x,y,z)",ref_patch_function);
```

随后 `WarpX.cpp` 明确规定：

- `max_level > 0` 时，这两条里至少要给一条；
- 两条都给时，`fine_tag_lo/fine_tag_hi` 覆盖 parser patch；
- parser 不是立即编译成 refinement mask，而是保留为表达式入口。

因此 `warpx.ref_patch_function(x,y,z)` 属于典型的 `Store string now, consume elsewhere` 型参数，而 `warpx.fine_tag_lo/hi` 则是立即求值成 `RealVect`。

## 8.3 field / particle / potential boundary 都是“文档合并名，源码拆键读”

场边界条件的 grouped alias `boundary.field_lo/hi` 最后落在：

```cpp
pp_boundary.query_enum_sloppy("field_lo", field_boundary_lo[idim], "-_", idim);
pp_boundary.query_enum_sloppy("field_hi", field_boundary_hi[idim], "-_", idim);
```

粒子边界条件 `boundary.particle_lo/hi` 对应的是：

```cpp
pp_boundary.query_enum_sloppy("particle_lo", particle_boundary_lo[idim], "-_", idim);
pp_boundary.query_enum_sloppy("particle_hi", particle_boundary_hi[idim], "-_", idim);
```

而电静边界势 `boundary.potential_lo/hi_x/y/z` 又是第三种结构：文档把它们合并成一个族，源码仍逐个读取：

```cpp
m_boundary_potential_specified |= pp_boundary.query("potential_lo_x", potential_xlo_str);
m_boundary_potential_specified |= pp_boundary.query("potential_hi_x", potential_xhi_str);
m_boundary_potential_specified |= pp_boundary.query("potential_lo_y", potential_ylo_str);
m_boundary_potential_specified |= pp_boundary.query("potential_hi_y", potential_yhi_str);
m_boundary_potential_specified |= pp_boundary.query("potential_lo_z", potential_zlo_str);
m_boundary_potential_specified |= pp_boundary.query("potential_hi_z", potential_zhi_str);
```

所以这一组参数最稳定的索引方式不是 alias 文本，而是：

- 场边界：`FieldBoundaries.cpp`
- 粒子边界：`ParticleBoundaries.cpp`
- 电静边界势：`PoissonBoundaryHandler.cpp`

`warpx.eb_potential(x,y,z,t)` 也是这层的一部分，但它不是 `boundary.*` 前缀，而是 `PoissonBoundaryHandler` 额外从 `warpx` 前缀再拿一条 EB 电极势表达式。

## 8.4 `amr.ref_ratio` 和 `amr.ref_ratio_vect` 是 AMReX-owned 输入，WarpX 只消费结果

这一组是本轮最重要的“不要误判为空源码”的例子。

在当前本地 WarpX 源码里，没有找到 WarpX 自己直接做：

- `ParmParse("amr").query("ref_ratio", ...)`
- `ParmParse("amr").query("ref_ratio_vect", ...)`

WarpX 本地只显式预解析了：

- `n_cell`
- `max_grid_size*`
- `blocking_factor*`

但后续很多地方会消费已经构造好的 `ref_ratios` 结果，例如：

```cpp
const int max_r = (nlevs > 1) ? ref_ratios[0][moving_window_dir] : 2;
```

以及 PML / coarse-fine 相关逻辑里对 `ref_ratio` 的 coarsen、grow 和 `ncell/ref_ratio` 计算。

因此对 `amr.ref_ratio` / `amr.ref_ratio_vect` 更准确的结论是：

- 它们属于 AMReX/AmrCore 自己读取的输入；
- WarpX 本地源码主要消费已经 materialize 完成的 `ref_ratios`；
- `parameter-map` 里应把本地消费者标出来，而不要假装 WarpX 有一个单独的 `query("ref_ratio")` 入口。

## 8.5 外场聚合开关：root gate 在 `ExternalField`，粒子/流体各自再读一层

`warpx.E/B_external_grid` 不是孤立常量，而是 `ExternalFieldParams` 在 root 层按 init-style gate 读取的常量 payload：

```cpp
pp_warpx.query("B_ext_grid_init_style", B_ext_grid_s);
pp_warpx.query("E_ext_grid_init_style", E_ext_grid_s);

if (B_ext_grid_type == ExternalFieldType::constant) {
    utils::parser::getArrWithParser(pp_warpx, "B_external_grid", v_B);
}
if (E_ext_grid_type == ExternalFieldType::constant) {
    utils::parser::getArrWithParser(pp_warpx, "E_external_grid", v_E);
}
```

这说明文档条目 `warpx.E/B_external_grid` 的真实含义是：

- 只有当 `*_ext_grid_init_style = constant` 时，数组值才会被读取；
- 若 style 是 parser / file / python，则真正入口换成别的参数族；
- moving-window 和 `InitData()` 后半段会继续消费 `E_external_grid/B_external_grid` 的 materialized 结果。

粒子外场开关 `particles.E/B_ext_particle_init_style` 则是 `MultiParticleContainer::ReadParameters()` 的顶层门闩：

```cpp
pp_particles.query("B_ext_particle_init_style", m_B_ext_particle_s);
pp_particles.query("E_ext_particle_init_style", m_E_ext_particle_s);
```

然后：

- parser 路径由 `Store_parserString + makeParser` 继续展开；
- repeated-plasma-lens 在 gather 侧 `GetExternalFields.cpp` 再解释；
- `read_from_file` 不在 gather kernel 里直接加场，而是提前写回 `Efield_aux/Bfield_aux`。

fluid 外场 `<fluid_species_name>.E/B_ext_init_style` 又是相同思想的第三份实现，但读取者变成 `WarpXFluidContainer::ReadParameters()`：

```cpp
pp_species_name.query("B_ext_init_style", m_B_ext_s);
pp_species_name.query("E_ext_init_style", m_E_ext_s);
```

随后只在 parser 分支下继续读取：

- `Bx_external_function(x,y,z,t)` 等
- `Ex_external_function(x,y,z,t)` 等

这也再次证明：同样叫“外场 init style”，粒子、流体和主网格三条路径并不是一个共用 parser。

## 8.6 PSATD / centering / macroscopic / hybrid：别看文档合并名，要看真正的局部读取点

`psatd.nox/noy/noz` 在文档中是 grouped alias，源码里仍然分别查询：

```cpp
utils::parser::queryWithParser(pp_psatd, "nox", nox_fft);
utils::parser::queryWithParser(pp_psatd, "noy", noy_fft);
utils::parser::queryWithParser(pp_psatd, "noz", noz_fft);
```

而 `psatd.nx/ny/nz_guard` 则不在 `WarpX.cpp`，而是在 `GuardCellManager.cpp` 的 PSATD 守护区估算阶段被覆写：

```cpp
utils::parser::queryWithParser(pp_psatd, "nx_guard", ngFFt_x);
utils::parser::queryWithParser(pp_psatd, "ny_guard", ngFFt_y);
utils::parser::queryWithParser(pp_psatd, "nz_guard", ngFFt_z);
```

同样，`warpx.field_centering_nox/noy/noz` 和 `warpx.current_centering_nox/noy/noz` 在文档中各是一条 grouped alias，但真实入口分属两段不同逻辑：

- current centering：只有 `do_current_centering` 打开后才读
- field centering：只有 momentum-conserving gather 或 `LabFrameElectroMagnetostatic` 才读

`macroscopic.sigma/epsilon/mu` 与 `macroscopic.sigma/epsilon/mu_function(x,y,z)` 也不是“六个参数并列”，而是三对 mutually-exclusive 的 constant/parser 路径。以 `sigma` 为例：

```cpp
if (utils::parser::queryWithParser(pp_macroscopic, "sigma", m_sigma)) {
    m_sigma_s = "constant";
}
if (pp_macroscopic.query("sigma_function(x,y,z)", m_str_sigma_function) ) {
    m_sigma_s = "parse_sigma_function";
}
```

`hybrid_pic_model.plasma_resistivity(rho,J)`、`plasma_hyper_resistivity(rho,B)` 和 `J[x/y/z]_external_grid_function(x,y,z,t)` 也一样：构造期只读字符串，真正 parser 编译和 time-dependence 检查发生在 `HybridPICModel::InitData()`。

## 8.7 `amrex.async_out*` 与 `amrex.abort_on_unused_inputs` 属于 AMReX-owned pass-through

这一组参数的共同点是：文档在 WarpX 手册里列出它们，但当前本地 WarpX 源码里没有看到 WarpX 自己直接做对应 `query(...)`。

更准确地说：

- `amrex.abort_on_unused_inputs`
- `amrex.use_profiler_syncs`
- `amrex.async_out`
- `amrex.async_out_nfiles`

都属于 AMReX runtime / startup 自己消费的参数。

WarpX 本地源码只在相邻层做两类事情：

1. `WarpXAMReXInit.cpp` 覆盖一部分 AMReX 缺省值，例如 `abort_on_out_of_gpu_memory`、`omp_threads`、`the_arena_is_managed`；
2. `WarpX.cpp` 给 plotfile / particle plotfile 单独设置 WarpX 自己的 I/O fan-out：

```cpp
utils::parser::queryWithParser(pp_warpx, "field_io_nfiles", field_io_nfiles);
VisMF::SetNOutFiles(field_io_nfiles);
utils::parser::queryWithParser(pp_warpx, "particle_io_nfiles", particle_io_nfiles);
pp_particles.add("particles_nfiles", particle_io_nfiles);
```

所以这里应当区分：

- `amrex.async_out*`：AMReX-owned async plotfile runtime
- `warpx.field/particle_io_nfiles`：WarpX 自己主动透传给 `VisMF` 和 `particles_nfiles`

不要把两者混成同一个 I/O 参数层。

## 8.8 `qed_schwinger.xmin/.../zmax` 也是 grouped alias，真实入口在 `MultiParticleContainer`

Schwinger 这一组文档写成：

- `qed_schwinger.xmin/ymin/zmin/xmax/ymax/zmax`

但真正读取仍然是拆开的：

```cpp
utils::parser::queryWithParser(pp_qed_schwinger, "xmin", m_qed_schwinger_xmin);
utils::parser::queryWithParser(pp_qed_schwinger, "xmax", m_qed_schwinger_xmax);
utils::parser::queryWithParser(pp_qed_schwinger, "zmin", m_qed_schwinger_zmin);
utils::parser::queryWithParser(pp_qed_schwinger, "zmax", m_qed_schwinger_zmax);
```

3D 下才会继续读 `ymin/ymax`。而 `QEDSchwingerProcess.H` 自己并不负责读参数；它只消费已经准备好的：

- `m_threshold_poisson_gaussian`
- `m_dV`
- `m_dt`

并在 kernel 里调用 `getSchwingerProductionNumber(...)`。

所以 Schwinger 的输入层入口仍然在 `MultiParticleContainer::ReadParameters()`，不在 event kernel。

## 8.9 这一轮对参数索引的实际修正

这批低频项真正补完后，`parameter-map.md` 里应明确区分三类来源：

1. `WarpX-local parse`
   - 例如 `geometry.prob_lo`、`fine_tag_lo`、`field_centering_nox`
2. `WarpX subobject parse`
   - 例如 `potential_lo_x`、`sigma_function(x,y,z)`、`Jx_external_grid_function(x,y,z,t)`
3. `AMReX-owned / WarpX consumes result`
   - 例如 `amr.ref_ratio`、`amrex.async_out`

这三类如果继续混写成“有没有 grep 到同名字符串”，参数索引就会在低频项上持续失真。

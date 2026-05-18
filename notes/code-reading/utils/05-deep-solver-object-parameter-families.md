# 深层 solver-object 参数入口图

绑定源码：

- `../warpx/Source/WarpX.cpp`
- `../warpx/Source/Fluids/MultiFluidContainer.cpp`
- `../warpx/Source/Fluids/WarpXFluidContainer.cpp`
- `../warpx/Source/FieldSolver/FiniteDifferenceSolver/HybridPICModel/HybridPICModel.cpp`
- `../warpx/Source/FieldSolver/FiniteDifferenceSolver/MacroscopicProperties/MacroscopicProperties.cpp`
- `../warpx/Source/FieldSolver/ElectrostaticSolvers/ElectrostaticSolver.cpp`
- `../warpx/Source/FieldSolver/ElectrostaticSolvers/EffectivePotentialES.cpp`
- `../warpx/Source/FieldSolver/ElectrostaticSolvers/EffectivePotentialES.H`

这篇笔记接在 [02-parameter-family-entrypoints.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/notes/code-reading/utils/02-parameter-family-entrypoints.md) 之后。

前一篇解决的是高频参数族在：

- `global gate`
- `factory dispatch`
- `instance-local parse`

三层壳里的第一入口。

这里继续往下，只处理四组更深的 solver-object 参数：

- `fluids.*`
- `hybrid_pic_model.*`
- `macroscopic.*`
- `warpx.effective_potential_*`

它们的共同特点是：

1. 不只是 `WarpX.cpp` 里某个简单布尔门闩；
2. 往往先由 root 层决定“对象是否存在”，再在对象构造期或运行前初始化期读取细项；
3. 单看 `parameters.rst` 很容易误判成“都属于第 6 章的 solver 参数”，但源码里其实分成了不同读取时机。

---

## 1. 总图

这四组参数比前面的 `species / diagnostics / collisions` 更像“对象存在性 + 对象内部 ReadParameters + InitData”三段式：

1. `WarpX.cpp::ReadParameters()`：
   先决定对象是否需要存在。
2. `WarpX` 构造函数 / `AllocLevelMFs()`：
   再决定何时构造对象、分配附属 `MultiFab`。
3. 具体 solver/fluid 对象：
   自己读取前缀参数，并在 `InitData()` 里继续把 parser 字符串编译成运行态 executor。

因此，对这四组参数，更准确的阅读顺序是：

- `global gate`
- `object creation`
- `instance-local parse`
- `runtime materialization`

---

## 2. Fluids

### 2.1 全局门闩：`WarpX.cpp::ReadParameters()`

fluid 族的第一入口不是某个 `WarpXFluidContainer` 构造函数，而是 root 层先看有没有 fluid species：

```cpp
const ParmParse pp_fluids("fluids");
std::vector<std::string> fluid_species_names = {};
pp_fluids.queryarr("species_names", fluid_species_names);
do_fluid_species = !fluid_species_names.empty();
```

这里同时做了 compatibility gate：

```cpp
if (do_fluid_species) {
    WARPX_ALWAYS_ASSERT_WITH_MESSAGE(max_level <= 1, ...);
    WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
        electrostatic_solver_id != ElectrostaticSolverAlgo::Relativistic, ...);
}
```

所以：

- `fluids.species_names` 是这组参数真正的 `global gate`；
- 它不只是名字列表，还决定整个 fluid 子系统是否存在。

### 2.2 工厂层：`MultiFluidContainer`

真正把 `fluids.species_names` 变成对象图的是：

```cpp
const ParmParse pp_fluids("fluids");
pp_fluids.queryarr("species_names", species_names);

for (int i = 0; i < nspecies; ++i) {
    allcontainers[i] = std::make_unique<WarpXFluidContainer>(i, species_names[i]);
}
```

这一层的职责很单纯：

- 读取 fluid 名字列表；
- 构造每个 `WarpXFluidContainer`；
- 后续统一转发 `AllocateLevelMFs()`、`InitData()`、`Evolve()`、`DepositCharge()`、`DepositCurrent()`。

因此 fluid 族的 `factory dispatch` 很明确：

- `fluids.species_names` 在 root 层是 existence gate；
- 在 `MultiFluidContainer` 里是 container factory。

### 2.3 实例内部配置层：`WarpXFluidContainer::ReadParameters()`

单个 fluid species 的细参数是在这里读的：

```cpp
SpeciesUtils::extractSpeciesProperties(species_name, injection_style, charge, mass, physical_species);

const ParmParse pp_species_name(species_name);
pp_species_name.query("do_not_deposit", do_not_deposit);
pp_species_name.query("do_not_gather", do_not_gather);
pp_species_name.query("do_not_push", do_not_push);

pp_species_name.query("B_ext_init_style", m_B_ext_s);
pp_species_name.query("E_ext_init_style", m_E_ext_s);
```

如果外场风格是 parser 形式，还会继续读取并保存表达式：

```cpp
utils::parser::Store_parserString(
    pp_species_name, "Bx_external_function(x,y,z,t)", str_Bx_ext_function);
...
m_Bx_parser = std::make_unique<amrex::Parser>(
    utils::parser::makeParser(str_Bx_ext_function,{"x","y","z","t"}));
```

这一层说明：

- fluid species 并不是独立参数命名空间；
- 它直接复用 `<species_name>.*` 前缀；
- 因此 fluid species 和 particle species 在输入前缀上是同一套名字空间，但对象消费者不同。

### 2.4 运行态展开：构造期与 `InitData()`

`WarpXFluidContainer` 构造函数里，除了 `ReadParameters()`，还会立刻调用：

```cpp
SpeciesUtils::parseDensity(...)
SpeciesUtils::parseMomentum(...)
```

这意味着 fluid 族不是“等到真正演化时再 parse”。

它的运行态展开分两步：

1. 构造期就把 density/momentum injector 搭好；
2. `AllocLevelMFs()` / `InitData()` 时再把 nodal `N` 与 `NU` 多场分配并初始化到网格上。

因此这组参数的最短查找顺序是：

1. `WarpX.cpp` 看 `fluids.species_names` 是否打开子系统；
2. `MultiFluidContainer.cpp` 看对象工厂；
3. `WarpXFluidContainer.cpp` 看 `<species_name>.*` 的真实消费；
4. 再回 `SpeciesUtils` / `Injector*` 看密度和动量分派。

---

## 3. Hybrid PIC

### 3.1 全局门闩：`algo.maxwell_solver = hybrid`

`hybrid_pic_model.*` 不会独立创建对象。

第一入口仍然是：

```cpp
pp_algo.query_enum_sloppy("maxwell_solver", electromagnetic_solver_id, "-_");
```

只有当：

- `electromagnetic_solver_id == ElectromagneticSolverAlgo::HybridPIC`

时，后面的 hybrid object 才会存在。

### 3.2 对象创建层：`WarpX` 构造函数

对象存在性由 `WarpX` 构造函数直接决定：

```cpp
if (electromagnetic_solver_id == ElectromagneticSolverAlgo::HybridPIC) {
    m_hybrid_pic_model = std::make_unique<HybridPICModel>();
}
```

而 `AllocLevelMFs()` 会继续把 hybrid 专属字段注册进 field registry：

```cpp
if (WarpX::electromagnetic_solver_id == ElectromagneticSolverAlgo::HybridPIC)
{
    m_hybrid_pic_model->AllocateLevelMFs(...);
}
```

所以 hybrid 族的第二层不只是“对象被 new 出来”，还包括：

- hybrid pressure/current/external-current 多场的分配；
- optional `ExternalVectorPotential` 子对象分配。

### 3.3 实例内部配置层：`HybridPICModel::ReadParameters()`

具体参数读取在：

```cpp
const ParmParse pp_hybrid("hybrid_pic_model");

utils::parser::queryWithParser(pp_hybrid, "substeps", m_substeps);
utils::parser::queryWithParser(pp_hybrid, "gamma", m_gamma);
utils::parser::queryWithParser(pp_hybrid, "elec_temp", m_elec_temp);
const bool n0_ref_given = utils::parser::queryWithParser(pp_hybrid, "n0_ref", m_n0_ref);

pp_hybrid.query("plasma_resistivity(rho,J)", m_eta_expression);
pp_hybrid.query("plasma_hyper_resistivity(rho,B)", m_eta_h_expression);
utils::parser::queryWithParser(pp_hybrid, "n_floor", m_n_floor);
pp_hybrid.query("add_external_fields", m_add_external_fields);
```

这里可以看出 hybrid 族内部已经再次分化成三类：

- 普通数值门闩：
  `substeps`、`gamma`、`elec_temp`、`n0_ref`、`n_floor`；
- parser 字符串：
  `plasma_resistivity(rho,J)`、`plasma_hyper_resistivity(rho,B)`；
- 子对象 existence gate：
  `add_external_fields` 决定是否构造 `ExternalVectorPotential`。

### 3.4 运行前初始化：`HybridPICModel::InitData()`

这组参数并不是在 `ReadParameters()` 完就彻底落地。

`InitData()` 才真正把字符串编译成 executor：

```cpp
m_resistivity_parser = std::make_unique<amrex::Parser>(
    utils::parser::makeParser(m_eta_expression, {"rho","J"}));
m_eta = m_resistivity_parser->compile<2>();
...
m_hyper_resistivity_parser = std::make_unique<amrex::Parser>(
    utils::parser::makeParser(m_eta_h_expression, {"rho","B"}));
m_eta_h = m_hyper_resistivity_parser->compile<2>();
```

因此 `hybrid_pic_model.*` 这组参数不能只停在 `ReadParameters()`：

- `ReadParameters()` 保存字符串、检查合法性；
- `InitData()` 才把它们变成真正可在 kernel 中执行的 parser executor。

---

## 4. Macroscopic Medium

### 4.1 全局门闩：`algo.em_solver_medium = macroscopic`

`macroscopic.*` 也不是总会存在。

第一层门闩仍在 `WarpX.cpp::ReadParameters()`：

```cpp
pp_algo.query_enum_sloppy("em_solver_medium", m_em_solver_medium, "-_");
```

只有：

- `m_em_solver_medium == MediumForEM::Macroscopic`

时，这组参数才有意义。

### 4.2 对象创建与 level 分配

构造函数里会根据这个门闩决定是否创建对象；
随后 `AllocLevelMFs()` 只在 level 0 为它分配介质字段：

```cpp
if (m_em_solver_medium == MediumForEM::Macroscopic) {
    WARPX_ALWAYS_ASSERT_WITH_MESSAGE( lev==0,
        "Macroscopic properties are not supported with mesh refinement.");
    m_macroscopic_properties->AllocateLevelMFs(ba, dm, ngEB);
}
```

因此它的对象层有一个很强的实现边界：

- 不是多 level 通用服务；
- 当前明确只支持 `lev == 0`。

### 4.3 实例内部配置层：`MacroscopicProperties::ReadParameters()`

真正读取 `macroscopic.*` 的地方是：

```cpp
const ParmParse pp_macroscopic("macroscopic");

utils::parser::queryWithParser(pp_macroscopic, "sigma", m_sigma);
pp_macroscopic.query("sigma_function(x,y,z)", m_str_sigma_function);

utils::parser::queryWithParser(pp_macroscopic, "epsilon", m_epsilon);
pp_macroscopic.query("epsilon_function(x,y,z)", m_str_epsilon_function);

utils::parser::queryWithParser(pp_macroscopic, "mu", m_mu);
pp_macroscopic.query("mu_function(x,y,z)", m_str_mu_function);
```

这一层的关键不是简单的数值读取，而是每个物性量都支持两条分支：

- constant
- parser function

并且如果用户没给，就退回真空默认值并发 warning。

### 4.4 运行态展开：`InitData()`

和 hybrid 类似，真正把 parser 变成网格字段是在 `InitData()`：

- constant 分支：`setVal(...)`
- parser 分支：`InitializeMacroMultiFabUsingParser(...)`

这说明 `macroscopic.*` 的真实结构是：

- `global gate`：
  `algo.em_solver_medium`
- `object creation`：
  `m_macroscopic_properties`
- `instance-local parse`：
  `sigma/epsilon/mu` 的 constant/parser 选择
- `runtime materialization`：
  `InitData()` 把物性场写入 `MultiFab`

---

## 5. Effective Potential Electrostatic

### 5.1 顶层门闩：`warpx.do_electrostatic = labframe-effective-potential`

effective-potential 族的第一入口仍然不是它自己的类，而是 electrostatic solver 选择：

```cpp
pp_warpx.query_enum_sloppy("do_electrostatic", electrostatic_solver_id, "-_");
```

在构造函数里，对应分派是：

```cpp
else if (electrostatic_solver_id == ElectrostaticSolverAlgo::LabFrameEffectivePotential)
{
    m_electrostatic_solver = std::make_unique<EffectivePotentialES>(nlevs_max);
}
```

因此：

- `warpx.do_electrostatic` 是这组参数的真正 `global gate`；
- `warpx.effective_potential_*` 不是独立 solver family 的顶层入口，只是已选中 effective-potential 分支后的细项。

### 5.2 基类读取：`ElectrostaticSolver::ReadParameters()`

effective-potential solver 并不是从零开始 parse。

它先继承 electrostatic 基类的读取壳：

```cpp
ParmParse const pp_warpx("warpx");

utils::parser::queryWithParser(pp_warpx, "self_fields_required_precision", ...);
utils::parser::queryWithParser(pp_warpx, "self_fields_absolute_tolerance", ...);
utils::parser::queryWithParser(pp_warpx, "self_fields_max_iters", ...);
utils::parser::queryWithParser(pp_warpx, "self_fields_verbosity", ...);
utils::parser::queryWithParser(pp_warpx, "use_2d_slices_fft_solver", is_igf_2d_slices);
```

这意味着 effective-potential 族的收敛容差、迭代预算和 FFT 边界条件，不是 `EffectivePotentialES` 自己重新定义的，而是直接复用 electrostatic base contract。

### 5.3 effective-potential 特有参数的真实读取时机

这组最容易误判的点是：

- `warpx.effective_potential_factor`
- `warpx.effective_potential_time_filter_param`
- `warpx.effective_potential_density_floor`

并不是在构造函数或 `ReadParameters()` 中读取，而是在 `ComputeSigma()` 里按需读取：

```cpp
const ParmParse pp_warpx("warpx");
utils::parser::queryWithParser(pp_warpx, "effective_potential_factor", C_SI);
utils::parser::queryWithParser(pp_warpx, "effective_potential_time_filter_param", time_filter_param);
utils::parser::queryWithParser(pp_warpx, "effective_potential_density_floor", density_floor);
```

也就是说，这一族参数的层次是：

- `global gate`：
  `warpx.do_electrostatic`
- `object creation`：
  `EffectivePotentialES`
- `instance-local parse`：
  electrostatic base class 读通用 self-fields 容差
- `runtime materialization`：
  `ComputeSigma()` 每次构造有效介电函数时再读取 effective-potential 特有细项

这比普通 `ReadParameters()` 路径更“晚绑定”。

### 5.4 运行态展开的另一层：`InitData()` 与 `ComputeSigma()`

这组参数的运行态展开有两步：

1. `InitData()` 先分配并初始化
   `effective_potential_sigma`；
2. `ComputeSigma()` 每次根据总 `rho`、时间滤波和 density floor 更新 sigma。

因此 effective-potential 这组参数的最短查找顺序应当是：

1. `WarpX.cpp` 看 solver 分派；
2. `ElectrostaticSolver.cpp` 看共用容差合同；
3. `EffectivePotentialES.cpp` 看特有参数如何在 `ComputeSigma()` 里晚读取；
4. 再回 initialization / validation 地图看它怎样进入实际 benchmark。

---

## 6. 这四组参数该怎样接回章节索引

它们的章节归属并不冲突，但第一次解析位置不能混写成一个平面表：

| 参数族 | 第一次解析层 | 主要章节 |
|---|---|---|
| `fluids.*` / `<fluid_species_name>.*` | `WarpX.cpp` existence gate + `MultiFluidContainer` + `WarpXFluidContainer` | 第 3A、6 章 |
| `hybrid_pic_model.*` | `algo.maxwell_solver` gate + `HybridPICModel::ReadParameters()` | 第 6 章 |
| `macroscopic.*` | `algo.em_solver_medium` gate + `MacroscopicProperties::ReadParameters()` | 第 6 章 |
| `warpx.effective_potential_*` | `warpx.do_electrostatic` gate + `ElectrostaticSolver` / `EffectivePotentialES::ComputeSigma()` | 第 3A、6 章 |

这里最重要的不是“最终回哪章”，而是：

- `fluids.*` 和 `<species_name>.*` 前缀是交叉复用的；
- `hybrid_pic_model.*`、`macroscopic.*`、`effective_potential_*` 都不是一进入 `WarpX.cpp` 就一次性 parse 完；
- 它们都需要把 root gate、对象构造、运行前初始化和运行态 materialization 区分开。

---

## 7. 当前边界

到这里，参数入口图已经覆盖了两层：

1. 高频总入口：
   `species / laser / diagnostics / reduced diagnostics / collision / boundary / solver / psatd / implicit`
2. 更深的 solver-object 入口：
   `fluids / hybrid_pic_model / macroscopic / effective potential`

还没继续下钻的自然下一层是：

1. `external_vector_potential.*` 自身的子对象入口图；
2. `PoissonBoundaryHandler` / `boundary.potential_*` 和 electrostatic solver 的交界；
3. `effective_potential` 与 validation/examples 的更细映射；
4. `parameter-map.md` 里仍缺真实源码命中的少量尾项。

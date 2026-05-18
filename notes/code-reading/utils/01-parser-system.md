# WarpX 参数系统：`ParmParse`、parser helper 与章节索引骨架

绑定源码：

- `../warpx/Source/Utils/Parser/ParserUtils.H`
- `../warpx/Source/Utils/Parser/ParserUtils.cpp`
- `../warpx/Source/Utils/Parser/IntervalsParser.H`
- `../warpx/Source/Utils/Parser/IntervalsParser.cpp`
- `../warpx/Source/Utils/WarpXAlgorithmSelection.H`
- `../warpx/Source/WarpX.cpp`
- `../warpx/Source/Initialization/WarpXInit.cpp`
- `../warpx/Source/Initialization/WarpXAMReXInit.cpp`

这篇笔记的目标不是把某个物理模块再讲一遍，而是回答三个更基础的问题：

1. `Docs/source/usage/parameters.rst` 里的参数，在源码里到底通过什么壳进入 WarpX；
2. 为什么同样是“读参数”，WarpX 里会同时出现 `query`、`queryWithParser`、`Store_parserString`、`IntervalsParser` 和 `query_enum_sloppy`；
3. 参数索引应该怎样从“自动字符串命中”升级成“能直接回到书稿章节”的人工入口。

---

## 1. `ParmParse` 不是单个全局表，而是一组前缀命名空间

WarpX 的参数系统建立在 AMReX `ParmParse` 上，但真正使用时并不是“所有参数都丢进一个大字典”。源码里最常见的模式是先按前缀取一个局部视图：

```cpp
const ParmParse pp;                  // 无前缀参数，如 max_step、stop_time
const ParmParse pp_amr("amr");       // amr.*
const ParmParse pp_algo("algo");     // algo.*
ParmParse const pp_warpx("warpx");   // warpx.*
const ParmParse pp_geometry("geometry");
const ParmParse pp_boundary("boundary");
const ParmParse pp_psatd("psatd");
const ParmParse pp_particles("particles");
const ParmParse pp_lasers("lasers");
const ParmParse pp_collisions("collisions");
```

这意味着 `parameters.rst` 的每个前缀，本质上都对应一段明确的源码解析壳。

最上游的运行控制参数就是这样读的：

```cpp
const ParmParse pp;// Traditionally, max_step and stop_time do not have prefix.
utils::parser::queryWithParser(pp, "max_step", max_step);
utils::parser::queryWithParser(pp, "stop_time", stop_time);
```

而几何和 moving window 则在初始化辅助函数里读：

```cpp
const amrex::ParmParse pp_geometry("geometry");
const amrex::ParmParse pp_warpx("warpx");
utils::parser::queryWithParser(
    pp_warpx, "moving_window_v", moving_window_v);
utils::parser::queryWithParser(
    pp_warpx, "start_moving_window_step", start_moving_window_step);
```

因此参数索引如果只记录“命中了 `WarpX.cpp`”，信息其实还不够。至少还要记下：

- 参数前缀属于哪个 `ParmParse` 命名空间；
- 第一次被谁读取；
- 那次读取是在启动层、构造期、初始化期还是 diagnostics 写出期发生。

---

## 2. 为什么 WarpX 大量用 `queryWithParser`

`ParserUtils.H` 里最重要的一组 helper 是：

```cpp
template <typename T>
int queryWithParser (const amrex::ParmParse& a_pp, char const * const str, T& val)
{
    return a_pp.queryAsDouble(str, val);
}

template <typename T>
int queryArrWithParser (const amrex::ParmParse& a_pp, char const * const str, std::vector<T>& val)
{
    auto nvals = a_pp.countval(str);
    if (nvals > 0) {
        val.resize(nvals);
        return a_pp.queryarrAsDouble(str, nvals, val.data());
    } else {
        return 0;
    }
}
```

这里的关键不是“少打一层模板”，而是它统一允许：

- 直接写数值；
- 写依赖 `my_constants` 的表达式；
- 对数组参数逐个做 parser 求值。

例如 `warpx.cfl`、`warpx.const_dt`、`amr.n_cell`、`fine_tag_lo/hi` 这种参数，不必限定用户只能写死常数。只要 `ParmParse::queryAsDouble` 能算出的表达式，它都能先转成数值再进入 WarpX 状态。

这也解释了为什么 WarpX 初始化早期要先把 `my_constants` 注入 parser，再去读一大批几何和 solver 参数。

---

## 3. 字符串表达式和数值表达式是两条不同的入口

不是所有参数都应该立刻算成数值。对真正需要保留函数体字符串、稍后再编译的参数，WarpX 走的是 `Store_parserString` / `Query_parserString`：

```cpp
void utils::parser::Store_parserString(
    amrex::ParmParse const& pp,
    std::string const& query_string,
    std::string& stored_string)
{
    std::vector<std::string> f;
    pp.getarr(query_string, f);
    stored_string.clear();
    for (auto const& s : f) {
        stored_string += s;
    }
}
```

然后再交给：

```cpp
amrex::Parser utils::parser::makeParser (
    std::string const& parse_function, amrex::Vector<std::string> const& varnames)
{
    const amrex::ParmParse pp;
    return pp.makeParser(parse_function, varnames);
}
```

也就是说，WarpX 里至少有两类 parser 参数：

1. 读入即化成数值：
   - `queryWithParser`
   - `queryArrWithParser`
2. 先保留表达式字符串，稍后按变量名编译成可执行 parser：
   - `Store_parserString`
   - `makeParser`

前者典型是：

- `warpx.cfl`
- `warpx.max_dt`
- `amr.n_cell`

后者典型是：

- `ref_patch_function(x,y,z)`
- external field 的 `*_grid_function(x,y,z,t)`
- reduced diagnostics / particle filter 的 parser 函数

参数索引里如果不区分这两类，就很容易把“立即读出的控制参数”和“后续在 kernel/diagnostics 里执行的函数参数”混成一类。

---

## 4. `group.name` 优先级是 WarpX 自己补上的

`ParserUtils` 还有一组容易被忽略的重载：它允许“无 group 名”和“带 group 名”的参数同时存在，并规定带 group 的优先：

```cpp
template <typename T>
int queryWithParser (const amrex::ParmParse& a_pp, std::string const& group, char const * const str, T& val)
{
    const bool is_specified_without_group = a_pp.contains(str);
    const std::string grp_str = group + "." + std::string(str);
    const bool is_specified_with_group = (group.empty() ? false : a_pp.contains(grp_str));

    if (is_specified_without_group && !is_specified_with_group) {
        return queryWithParser(a_pp, str, val);
    } else {
        return queryWithParser(a_pp, grp_str.c_str(), val);
    }
}
```

这条合同很重要，因为它决定了“全局缺省”和“局部覆盖”的真实优先级。例如 diagnostics、species、collision 这类前缀化对象，经常会复用同一个字段名，但由 `<group>.<name>` 抢占优先解析权。

因此参数到章节的映射不能只看末尾名字；还要把完整前缀保留下来。`precision`、`intervals` 这种名字在不同组里语义完全不同。

---

## 5. `IntervalsParser` 说明“时间表参数”不是普通整数

WarpX 里很多“每多少步做一次”的参数，不是单个整数，而是切片语法：

```cpp
utils::parser::IntervalsParser WarpX::sort_intervals;
...
sort_intervals = utils::parser::IntervalsParser(sort_intervals_string_vec);
```

`IntervalsParser` / `SliceParser` 真正支持的不是单值，而是：

- `k`
- `i:j`
- `i:j:k`
- 多段逗号拼接

其解析逻辑在 `IntervalsParser.cpp` 里非常直接：

```cpp
if(insplit.size() == 1){ // no colon in input string. The input is the period.
    m_period = int(std::round(pp.eval<double>(insplit[0])));}
else if(insplit.size() == 2) // 1 colon in input string. The input is start:stop
{
    if (!insplit[0].empty()){
        m_start = int(std::round(pp.eval<double>(insplit[0])));}
    if (!insplit[1].empty()){
        m_stop = int(std::round(pp.eval<double>(insplit[1])));}
}
```

这说明参数索引里还有第三类值：

1. 标量数值
2. parser 字符串函数
3. 时间切片 / interval 语法

典型例子包括：

- `warpx.dt_update_interval`
- `algo.load_balance_intervals`
- `warpx.sort_intervals`
- diagnostics / reduced diagnostics / BTD 的 `intervals`

这些参数应该优先回到第 3 章、第 8 章和并行章节，而不该被误写成普通整数开关。

---

## 6. 枚举型参数真正的解析壳在 `query_enum_sloppy` 与 `AMREX_ENUM`

对算法选择类参数，WarpX 并不自己手写字符串 `if/else`，而是先在 `WarpXAlgorithmSelection.H` 定义枚举，再通过 `ParmParse` 的枚举解析读入。

例如：

```cpp
AMREX_ENUM(EvolveScheme,
           Explicit,
           ThetaImplicitEM,
           SemiImplicitEM,
           StrangImplicitSpectralEM,
           Default = Explicit);
```

以及：

```cpp
pp_warpx.query_enum_sloppy("do_electrostatic", electrostatic_solver_id, "-_");
```

这意味着像下面这些参数：

- `algo.evolve_scheme`
- `warpx.do_electrostatic`
- `warpx.poisson_solver`
- `algo.maxwell_solver`
- `algo.particle_pusher`
- `algo.current_deposition`
- `algo.field_gathering`

其真正的“第一解析层”不在具体物理 kernel，而在：

1. `WarpXAlgorithmSelection.H` 的枚举定义；
2. `WarpX.cpp::ReadParameters()` 的枚举读入；
3. 后续 `switch/if` 对对象图和 kernel 分派的消费。

因此这类参数的章节映射至少应当同时指向：

- 第 3 章或 3A 章的参数分派入口；
- 对应物理章节，如第 4/5/6/7/8 章。

---

## 7. 第一版 `ParmParse -> chapter` 映射规则

在当前书稿结构下，参数到章节可以先按“第一次决定对象图的地方”做第一落点，再按“主要被哪个物理章节解释”做第二落点。

### 7.1 第一落点：谁先读

| 参数前缀 | 第一落点 |
|---|---|
| 无前缀参数，如 `max_step`、`stop_time` | 第 3 章 `ReadParameters()/Evolve()` |
| `geometry.*`、`amr.*`、`warpx.do_moving_window` | 第 3A 章启动层 / 初始化 |
| `algo.*`、`interpolation.*`、`psatd.*` | 第 3 章分派入口；随后回第 4/5/6 章 |
| `boundary.*`、PML 相关 `warpx.*` | 第 7 章 |
| species、`particles.*`、`warpx.*_external*` | 第 3A 章与第 4 章 |
| `lasers.*` | 第 3A 章与后续 laser 笔记 |
| `diagnostics.*`、`<diag>.*`、`reduced_diags.*` | 第 8 章 |
| `collisions.*`、`<collision>.*` | 第 4 章 collision/QED 部分 |

### 7.2 第二落点：哪一章真正解释其物理语义

| 参数族 | 主要书稿章节 |
|---|---|
| 运行控制、步长、moving window、boosted frame | 第 3 / 3A 章 |
| 注入、初始分布、self-field、external field | 第 3A 章 |
| pusher、gather、particle external field、collisions、QED | 第 4 章 |
| shape / charge / current deposition | 第 5 章 |
| Maxwell、Poisson、PSATD、implicit、hybrid | 第 6 章 |
| boundary、PML、EB、AMR、parallelization | 第 7 章 |
| diagnostics、plotfile/openPMD/checkpoint、Python buffer | 第 8 章 |

---

## 8. 对 `docs/parameter-map.md` 的当前使用建议

到目前为止，`docs/parameter-map.md` 仍然有两种信息层次混在一起：

1. 自动字符串命中得到的“初步源码位置”；
2. 早期阶段里用计划编号记录的“计划章节”。

因此当前更稳妥的使用方式应当是：

1. 先用 `parameter-map.md` 找到文档行号和初步源码命中；
2. 再用 `docs/parameter-chapter-index.md` 找当前人工确认过的章节归属；
3. 最终仍回到具体源码笔记和正式章节。

也就是说，`parameter-map.md` 还是导航层，而不是最终结论层。

---

## 9. 当前阶段性判断

`ParmParse -> chapter` 这条线现在已经有了第一块稳定骨架：

- 参数命名空间怎么分；
- parser helper 怎么分三类；
- 枚举型参数的第一解析壳在哪里；
- 时间切片类参数为什么需要单独看；
- 参数落章的两级规则是什么。

下一步更自然的是：

1. 继续人工修正 `docs/parameter-map.md` 顶部一批高频 `待定` 条目；
2. 再逐步把 `species`、`laser`、`diagnostics`、`collision` 这些对象前缀扩成更细的章节索引。

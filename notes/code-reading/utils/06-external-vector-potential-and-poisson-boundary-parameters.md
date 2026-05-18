# External Vector Potential 与 Poisson Boundary 参数入口图

绑定源码：

- `../warpx/Source/WarpX.cpp`
- `../warpx/Source/FieldSolver/FiniteDifferenceSolver/HybridPICModel/ExternalVectorPotential.cpp`
- `../warpx/Source/FieldSolver/FiniteDifferenceSolver/HybridPICModel/ExternalVectorPotential.H`
- `../warpx/Source/FieldSolver/ElectrostaticSolvers/PoissonBoundaryHandler.cpp`
- `../warpx/Source/FieldSolver/ElectrostaticSolvers/PoissonBoundaryHandler.H`
- `../warpx/Source/FieldSolver/ElectrostaticSolvers/ElectrostaticSolver.cpp`
- `../warpx/Source/Initialization/WarpXInitData.cpp`
- `../warpx/Source/Python/WarpX.cpp`

这篇笔记继续沿参数系统主线往下，只处理两组更偏“子对象 + 边界条件”的参数族：

- `external_vector_potential.*`
- `boundary.potential_*` / `warpx.eb_potential(x,y,z,t)`

它们的共同特点是：

1. 都不是单纯在 `WarpX.cpp` 里一次性读完；
2. 都挂在更大的 solver-object 之下；
3. 真正的 parser 编译和运行态消费比普通参数更晚。

---

## 1. 总图

这两组参数都不适合只按：

- `global gate`
- `factory dispatch`
- `instance-local parse`

三层来理解。

更准确的结构是：

1. 上游 solver-object 先决定子对象是否存在；
2. 子对象构造期读取前缀参数；
3. `InitData()` 或 `BuildParsers()` 再把字符串编译成 parser executor；
4. 运行时更新函数再真正消费这些 executor。

因此，这两组参数更像：

- `parent gate`
- `subobject parse`
- `parser build`
- `runtime apply`

---

## 2. `external_vector_potential.*`

### 2.1 parent gate：先由 `hybrid_pic_model.add_external_fields` 决定是否存在

`external_vector_potential.*` 不是独立系统。

它的第一层门闩在 [HybridPICModel.cpp](/Volumes/PHILIPS/programs/PIC/warpx/Source/FieldSolver/FiniteDifferenceSolver/HybridPICModel/HybridPICModel.cpp)：

```cpp
pp_hybrid.query("add_external_fields", m_add_external_fields);

if (m_add_external_fields) {
    m_external_vector_potential = std::make_unique<ExternalVectorPotential>();
}
```

所以：

- `algo.maxwell_solver = hybrid` 是父级 `global gate`
- `hybrid_pic_model.add_external_fields` 是子对象 existence gate
- `external_vector_potential.*` 只有在这两层都成立时才有意义

### 2.2 子对象读取层：`ExternalVectorPotential::ReadParameters()`

真正读取 `external_vector_potential.*` 的地方是：

```cpp
const ParmParse pp_ext_A("external_vector_potential");

pp_ext_A.query("do_diva_cleaning", m_do_clean_divA);
pp_ext_A.queryarr("fields", m_field_names);
```

这组参数的第一关键点是：

- `external_vector_potential.fields` 不是普通列表
- 它是二级子对象名字表

后面所有细项都按 `<field_name>.*` 再展开：

```cpp
utils::parser::queryWithParser(pp_ext_A,
    (m_field_names[i]+".read_from_file").c_str(), read_from_file);

if (m_read_A_from_file[i]) {
    pp_ext_A.query(m_field_names[i]+".path", m_external_file_path[i]);
} else {
    pp_ext_A.query(m_field_names[i]+".Ax_external_grid_function(x,y,z)",
        m_Ax_ext_grid_function[i]);
    ...
}

pp_ext_A.query(m_field_names[i]+".A_time_external_function(t)",
    m_A_ext_time_function[i]);
```

因此它的内部结构是：

- 顶层子对象列表：
  `external_vector_potential.fields`
- 每个 field 的 source-type gate：
  `<field_name>.read_from_file`
- source-specific 参数：
  `<field_name>.path`
  或
  `<field_name>.A[x/y/z]_external_grid_function(x,y,z)`
- 统一时间包络：
  `<field_name>.A_time_external_function(t)`

### 2.3 parser build 与数据落地：`InitData()`

这组参数并不是在 `ReadParameters()` 完就可用。

`InitData()` 里才真正分成两条路径：

#### 2.3.1 文件路径

若 `read_from_file = true`：

```cpp
warpx.ReadExternalFieldFromFile(..., "A", "x");
...
```

说明这里不是 parser family，而是直接把 openPMD 文件读进：

- `<field_name>_Aext`

这组空间场。

#### 2.3.2 parser 路径

若 `read_from_file = false`：

```cpp
m_A_external_parser[i][0] = std::make_unique<amrex::Parser>(
    utils::parser::makeParser(m_Ax_ext_grid_function[i],{"x","y","z","t"}));
...
m_A_external[i][0] = m_A_external_parser[i][0]->compile<4>();
```

但这里还有一个关键限制：

```cpp
WARPX_ALWAYS_ASSERT_WITH_MESSAGE(A_ext_symbols.count("t") == 0,
    "Externally Applied Vector potential time variation must be set with A_time_external_function(t)");
```

也就是说：

- 空间分布函数虽然声明成 `(x,y,z,t)`
- 但实际不允许依赖 `t`
- 时间依赖必须单独走 `<field_name>.A_time_external_function(t)`

这就是这组参数最重要的输入合同之一。

### 2.4 runtime apply：`UpdateHybridExternalFields()`

`InitData()` 末尾会先做一次：

```cpp
UpdateHybridExternalFields(warpx.gett_new(0), warpx.getdt(0));
```

而后续真正的运行态消费在：

- `WarpXPushFieldsHybridPIC.cpp`

里多次调用 `UpdateHybridExternalFields(...)`。

因此这组参数的完整结构应当写成：

- `parent gate`：
  `algo.maxwell_solver = hybrid`
- `subobject gate`：
  `hybrid_pic_model.add_external_fields`
- `subobject parse`：
  `external_vector_potential.fields` 与 `<field_name>.*`
- `parser build / file load`：
  `InitData()`
- `runtime apply`：
  `UpdateHybridExternalFields()`

---

## 3. `boundary.potential_*` 与 `warpx.eb_potential(x,y,z,t)`

### 3.1 parent gate：先由 electrostatic / self-field 求解路径决定是否会消费

这组参数并不是单独创建一个边界对象后总会参与演化。

最上游仍取决于：

- `warpx.do_electrostatic`
- 或 electromagnetic 模式下的初始 self-field solve

对应 solver 对象里统一持有：

- `m_poisson_boundary_handler`

### 3.2 子对象读取层：`PoissonBoundaryHandler::ReadParameters()`

真正读取边界势的是：

```cpp
const ParmParse pp_boundary("boundary");

m_boundary_potential_specified |= pp_boundary.query("potential_lo_x", potential_xlo_str);
...
m_boundary_potential_specified |= pp_boundary.query("potential_hi_z", potential_zhi_str);

const ParmParse pp_warpx("warpx");
m_boundary_potential_specified |= pp_warpx.query("eb_potential(x,y,z,t)", potential_eb_str);
```

这里有两个重要事实：

1. 域边界电势和 EB 电势不在同一前缀下：
   - domain boundary：`boundary.potential_*`
   - embedded boundary：`warpx.eb_potential(x,y,z,t)`
2. `m_boundary_potential_specified` 是统一门闩：
   只要任一边界势被提供，就会把后续 Poisson 边界处理链打开。

### 3.3 solver-aware warning 层

`PoissonBoundaryHandler` 在读完参数后就会根据当前 solver 给 warning：

```cpp
if (m_boundary_potential_specified & (WarpX::electromagnetic_solver_id == ElectromagneticSolverAlgo::HybridPIC)) {
    ...
}
else if (m_boundary_potential_specified & (WarpX::electromagnetic_solver_id != ElectromagneticSolverAlgo::None)) {
    ...
}
```

这说明这组参数不是“纯局部边界细节”。

它在读取时就已经和：

- Hybrid PIC
- electromagnetic + initial Poisson solve

这两条上游大分支耦合。

### 3.4 parser build：`BuildParsers()` 与 `BuildParsersEB()`

对于普通 domain boundary：

```cpp
potential_xlo_parser = utils::parser::makeParser(potential_xlo_str, {"t"});
...
potential_xlo = potential_xlo_parser.compile<1>();
```

也就是说，`boundary.potential_lo/hi_*` 的合法自变量只有：

- `t`

而不是空间坐标。

对于 EB 电势：

```cpp
potential_eb_parser  = utils::parser::makeParser(potential_eb_str, {"x", "y", "z", "t"});
```

然后再分成两种情况：

- 若依赖空间：
  编译成 `compile<4>()`
- 若只依赖时间：
  退化成 `compile<1>()`

所以这组参数里最重要的输入合同差异是：

- `boundary.potential_*`：
  只能是时间函数
- `warpx.eb_potential(x,y,z,t)`：
  可以是时空函数，也可以退化成纯时间函数

### 3.5 BC 类型落地：`DefinePhiBCs()`

parser 编出来之后，还不会立刻写到网格上。

先要由：

```cpp
void PoissonBoundaryHandler::DefinePhiBCs (const amrex::Geometry& geom)
```

根据：

- `WarpX::field_boundary_lo/hi`
- `WarpX::poisson_solver_id`
- 几何维度

把每个边界确定成：

- `Periodic`
- `Dirichlet`
- `Neumann`

并填入：

- `lobc / hibc`
- `dirichlet_flag`

这一层说明：

- `boundary.potential_*` 本身不决定边界类型
- 它只是给 Dirichlet 边界提供数值
- 真正是否允许 Dirichlet，要先经过 `field_boundary_*` 与 Poisson solver 的组合合法性检查

### 3.6 runtime apply：`ElectrostaticSolver::setPhiBC()`

真正把边界势值写进 `phi` 的地方在：

```cpp
phi_bc_values_lo[0] = m_poisson_boundary_handler->potential_xlo(t);
...
if (dirichlet_flag[2*idim] && iv[idim] == domain.smallEnd(idim)){
    phi_arr(i,j,k) = phi_bc_values_lo[idim];
}
```

因此这组参数的完整链条是：

- `parent gate`：
  electrostatic / initial self-field solve 是否存在
- `subobject parse`：
  `boundary.potential_*` 与 `warpx.eb_potential(...)`
- `parser build`：
  `BuildParsers()` / `BuildParsersEB()`
- `BC typing`：
  `DefinePhiBCs()`
- `runtime apply`：
  `ElectrostaticSolver::setPhiBC()`

### 3.7 Python front-end 的额外入口

这组参数还有一个额外入口，不经过输入文件，而是 Python 直接改 handler 字符串：

```cpp
if (potential_lo_x != "") wx.GetElectrostaticSolver().m_poisson_boundary_handler->potential_xlo_str = potential_lo_x;
...
```

这说明：

- Python front-end 可以覆盖 handler 内部保存的字符串；
- 但这不是完整的高层重新解析流程；
- 若后续要系统梳理 Python 参数入口，需要单独补这一层。

---

## 4. 这两组参数应怎样接回参数索引

它们都不该再被写成“某个前缀 -> 某个 cpp 文件”的单层映射。

更准确的导航是：

| 参数族 | 上游门闩 | 子对象读取层 | 运行态关键点 |
|---|---|---|---|
| `external_vector_potential.*` | `algo.maxwell_solver=hybrid` + `hybrid_pic_model.add_external_fields` | `ExternalVectorPotential::ReadParameters()` | `InitData()` + `UpdateHybridExternalFields()` |
| `boundary.potential_*` | electrostatic / self-field solve 路径存在 | `PoissonBoundaryHandler::ReadParameters()` | `DefinePhiBCs()` + `setPhiBC()` |
| `warpx.eb_potential(x,y,z,t)` | 同上 | `PoissonBoundaryHandler::ReadParameters()` | `BuildParsersEB()` + Poisson/EB solve |

其中最容易误导读者的两个点是：

1. `boundary.potential_*` 只支持 `t`，不支持空间坐标；
2. `external_vector_potential.<field>.A[x/y/z]_external_grid_function(...)` 虽然形式里写了 `t`，但源码要求时间依赖必须单独走 `A_time_external_function(t)`。

---

## 5. 当前边界

到这里，参数入口图已经又补了一层：

- 高层工厂/门闩参数
- 深层 solver-object 参数
- 以及带 parser 构造和运行态 apply 的边界/子对象参数

下一步最自然的延伸方向是：

1. 把 `ExternalVectorPotential` 继续和 `HybridPICModel` 的验证入口、examples、diagnostics 输出对应起来；
2. 把 `PoissonBoundaryHandler` 与 `electrostatic_dirichlet_bc`、`open_bc_poisson_solver`、`electrostatic_sphere_eb` 这些 validation map 做更紧的双向链接；
3. 再回 [parameter-map.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/docs/parameter-map.md) 清理剩余少量真实源码命中不足的尾项。

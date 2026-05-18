# External Fields 外场初始化第一轮精读

绑定源码：`../warpx`，分支 `pkuHEDPbranch`，commit `063f8b586f04321e13150ae3e730e0794ca75cb1`。

本笔记覆盖 `../warpx/Source/Initialization/ExternalField.H`、`ExternalField.cpp` 和 `WarpXInitData.cpp` 中的 `LoadExternalFields()` / `ReadExternalFieldFromFile()`。核心问题是：WarpX 如何区分网格外场和粒子外场，如何解析 constant/parser/openPMD/Python 外场，如何把外场写入正确的 staggered `MultiFab`。

## 1. 外场类型枚举

源码位置：`../warpx/Source/Initialization/ExternalField.H:29-36`。

```cpp
enum class ExternalFieldType
{
    default_zero,
    constant,
    parse_ext_grid_function,
    read_from_file,
    load_from_python
};
```

这五类初始化方式分别对应：

| 类型 | 含义 | 主要路径 |
|---|---|---|
| `default_zero` | 默认无外加网格场 | `ExternalFieldParams` 默认值 |
| `constant` | 常量外场 | `B_external_grid` / `E_external_grid` |
| `parse_ext_grid_function` | 输入文件中的解析函数 | `amrex::Parser`，变量为 `x,y,z,t` |
| `read_from_file` | 从 openPMD 文件读入 | `ExternalFieldReader` |
| `load_from_python` | Python callback 写入 | `ExecutePythonCallback("loadExternalFields")` |

这里的枚举只描述网格外场初始化类型。粒子外场还有另一套路径，来自 `MultiParticleContainer` / particle container 的 external particle field metadata。

## 2. `ExternalFieldParams` 保存网格外场参数

源码位置：`../warpx/Source/Initialization/ExternalField.H:38-76`。

```cpp
struct ExternalFieldParams
{

    /**
    * \brief The constructor reads and stores the parameters related to the external fields.
    * "pp_warpx" must point at the "warpx" parameter group in the inputfile.
    */
    explicit ExternalFieldParams(const amrex::ParmParse& pp_warpx);

    //! Initial electric field on the grid
    amrex::GpuArray<amrex::Real,3> E_external_grid = {0,0,0};
    //! Initial magnetic field on the grid
    amrex::GpuArray<amrex::Real,3> B_external_grid = {0,0,0};

    //! Initialization type for external magnetic field on the grid
    ExternalFieldType B_ext_grid_type = ExternalFieldType::default_zero;
    //! Initialization type for external electric field on the grid
    ExternalFieldType E_ext_grid_type = ExternalFieldType::default_zero;
```

`ExternalFieldParams` 是 `warpx.*` 参数组下网格外场的参数容器。它不直接保存 `MultiFab`，只保存：

- 常量外场数值；
- `E/B` 外场初始化类型；
- 每个分量的 parser；
- openPMD 文件路径。

这说明外场参数的生命周期早于 level 数据分配：`WarpX::ReadParameters()` 中创建 `m_p_ext_field_params`，但真正的 `Efield_fp_external/Bfield_fp_external` 要在 `AllocLevelMFs()` 中按 level 和 index type 分配。

## 3. 输入字符串到外场类型的映射

源码位置：`../warpx/Source/Initialization/ExternalField.cpp:31-66`。

```cpp
template <EMFieldType T>
ExternalFieldType string_to_external_field_type(std::string s)
{
    std::transform(s.begin(), s.end(), s.begin(), ::tolower);

    if constexpr (T == EMFieldType::E){
        WARPX_ALWAYS_ASSERT_WITH_MESSAGE(s != "parse_b_ext_grid_function",
            "parse_B_ext_grid_function can be used only for B_ext_grid_init_style");
    }
    else{
        WARPX_ALWAYS_ASSERT_WITH_MESSAGE(s != "parse_e_ext_grid_function",
            "parse_E_ext_grid_function can be used only for E_ext_grid_init_style");
    }

    if ( s.empty() || s == "default"){
        return ExternalFieldType::default_zero;
    }
    else if ( s == "constant"){
        return ExternalFieldType::constant;
    }
    else if ( s == "parse_b_ext_grid_function" || s == "parse_e_ext_grid_function"){
        return ExternalFieldType::parse_ext_grid_function;
    }
    else if ( s == "read_from_file"){
        return ExternalFieldType::read_from_file;
    }
    else if ( s == "load_from_python"){
        return ExternalFieldType::load_from_python;
    }
```

这里有两个容易忽略的约束：

1. `parse_b_ext_grid_function` 只能用于 `B_ext_grid_init_style`，不能误用于 `E_ext_grid_init_style`。
2. 空字符串和 `default` 都等价于 `default_zero`。

这类检查属于输入语义检查，不是数值 kernel 的职责。正式章节讲参数时，应把这种“参数值合法性”记录到参数表里。

## 4. 常量外场和 parser 外场的读取

源码位置：`../warpx/Source/Initialization/ExternalField.cpp:69-191`。

```cpp
ExternalFieldParams::ExternalFieldParams(const amrex::ParmParse& pp_warpx)
{
    // default values of E_external_grid and B_external_grid
    // are used to set the E and B field when "constant" or
    // "parser" is not explicitly used in the input.
    std::string B_ext_grid_s;
    pp_warpx.query("B_ext_grid_init_style", B_ext_grid_s);
    B_ext_grid_type = string_to_external_field_type<EMFieldType::B>(B_ext_grid_s);

    std::string E_ext_grid_s;
    pp_warpx.query("E_ext_grid_init_style", E_ext_grid_s);
    E_ext_grid_type = string_to_external_field_type<EMFieldType::E>(E_ext_grid_s);
```

常量外场只有在 style 为 `constant` 时才强制读取数值：

```cpp
auto v_B = std::vector<amrex::Real>(3);
if (B_ext_grid_type == ExternalFieldType::constant) {
    utils::parser::getArrWithParser(pp_warpx, "B_external_grid", v_B);
}
std::copy(v_B.begin(), v_B.end(), B_external_grid.begin());

auto v_E = std::vector<amrex::Real>(3);
if (E_ext_grid_type == ExternalFieldType::constant) {
    utils::parser::getArrWithParser(pp_warpx, "E_external_grid", v_E);
}
std::copy(v_E.begin(), v_E.end(), E_external_grid.begin());
```

如果未设置 constant，临时 `v_B/v_E` 初始化为 0，所以 `B_external_grid/E_external_grid` 保持默认零。这个行为和 `default_zero` 一致。

parser 外场为每个分量创建 `amrex::Parser`：

```cpp
if (B_ext_grid_type == ExternalFieldType::parse_ext_grid_function) {

    //! Strings storing parser function to initialize the components of the magnetic field on the grid
    std::string str_Bx_ext_grid_function;
    std::string str_By_ext_grid_function;
    std::string str_Bz_ext_grid_function;

#if defined(WARPX_DIM_RZ)
    std::stringstream warnMsg;
    warnMsg << "Parser for external B (r and theta) fields does not work with cylindrical and spherical\n"
        << "The initial Br and Bt fields are currently hardcoded to 0.\n"
        << "The initial Bz field should only be a function of z.\n";
    ablastr::warn_manager::WMRecordWarning(
      "Inputs", warnMsg.str(), ablastr::warn_manager::WarnPriority::high);
    str_Bx_ext_grid_function = "0";
    str_By_ext_grid_function = "0";
#else
    utils::parser::Store_parserString(pp_warpx, "Bx_external_grid_function(x,y,z)",
      str_Bx_ext_grid_function);
    utils::parser::Store_parserString(pp_warpx, "By_external_grid_function(x,y,z)",
      str_By_ext_grid_function);
#endif
    utils::parser::Store_parserString(pp_warpx, "Bz_external_grid_function(x,y,z)",
        str_Bz_ext_grid_function);

    Bxfield_parser = std::make_unique<amrex::Parser>(
        utils::parser::makeParser(str_Bx_ext_grid_function,{"x","y","z","t"}));
```

RZ 的外部 B parser 有特殊限制：`Br/Btheta` 被硬编码为 0，`Bz` 只能是 `z` 的函数。这是几何和模式表示的限制，不是文档措辞问题。E parser 在 RZ 下直接 abort：

```cpp
#ifdef WARPX_DIM_RZ
WARPX_ABORT_WITH_MESSAGE(
    "E parser for external fields does not work with RZ -- TO DO");
#endif
```

## 5. 网格外场和粒子外场写入不同 FieldType

源码位置：`../warpx/Source/Initialization/WarpXInitData.cpp:1642-1765`。

`LoadExternalFields()` 先确定当前几何下的分量名：

```cpp
#if defined(WARPX_DIM_RZ) || defined(WARPX_DIM_RCYLINDER)
    std::array<std::string, 3> dimnames = {"r", "t", "z"};
#elif defined(WARPX_DIM_RSPHERE)
    std::array<std::string, 3> dimnames = {"r", "t", "p"};
#else
    std::array<std::string, 3> dimnames = {"x", "y", "z"};
#endif
```

随后阻止 `read_from_file` 与 moving window 同时使用：

```cpp
if ( (m_p_ext_field_params->B_ext_grid_type == ExternalFieldType::read_from_file) ||
     (m_p_ext_field_params->E_ext_grid_type == ExternalFieldType::read_from_file) ||
     (mypc->m_B_ext_particle_s == "read_from_file") ||
     (mypc->m_E_ext_particle_s == "read_from_file") ) {

    WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
        WarpX::do_moving_window == 0,
        "External fields from file are not compatible with the moving window." );
}
```

源码注释解释了原因：如果 moving window 移动，外场 `MultiFab` 也必须随窗口更新；当前文件读入路径没有实现这一点。

网格外部 B 场写到 `Bfield_fp_external`：

```cpp
if (m_p_ext_field_params->B_ext_grid_type == ExternalFieldType::parse_ext_grid_function) {
    // Initialize Bfield_fp_external with external function
    ComputeExternalFieldOnGridUsingParser(
        FieldType::Bfield_fp_external,
        m_p_ext_field_params->Bxfield_parser->compile<4>(),
        m_p_ext_field_params->Byfield_parser->compile<4>(),
        m_p_ext_field_params->Bzfield_parser->compile<4>(),
        lev, PatchType::fine, m_eb_update_B);
}
else if (m_p_ext_field_params->B_ext_grid_type == ExternalFieldType::read_from_file) {
    ReadExternalFieldFromFile(m_p_ext_field_params->external_fields_path, m_fields.get(FieldType::Bfield_fp_external,Direction{0},lev), "B", dimnames[0]);
    ReadExternalFieldFromFile(m_p_ext_field_params->external_fields_path, m_fields.get(FieldType::Bfield_fp_external,Direction{1},lev), "B", dimnames[1]);
    ReadExternalFieldFromFile(m_p_ext_field_params->external_fields_path, m_fields.get(FieldType::Bfield_fp_external,Direction{2},lev), "B", dimnames[2]);
}
```

粒子外部 B 场写到 `B_external_particle_field`，并且支持多个 map，每个 map 放到一个 component：

```cpp
if (mypc->m_B_ext_particle_s == "read_from_file") {
    const auto& metaB = mypc->m_external_particle_fields_metadata.m_B_field_metadata;
    if (!metaB.empty()) {
        // Read multiple maps: each field map goes to component ic
        for (int ic = 0; ic < static_cast<int>(metaB.size()); ++ic) {
            const std::string& path = metaB[ic].path;

            ReadExternalFieldFromFile(path,
                m_fields.get(FieldType::B_external_particle_field, Direction{0}, lev),
                "B", dimnames[0], ic);
```

这个区别非常重要：

| 外场类别 | FieldType | 作用对象 | 后续合成位置 |
|---|---|---|---|
| grid external field | `Efield_fp_external`, `Bfield_fp_external` | 网格主场 | `AddExternalFields()` 加到 `Efield_fp/Bfield_fp` |
| particle external field | `E_external_particle_field`, `B_external_particle_field` | 粒子 gather/push 看到的额外外场 | `UpdateAuxilaryData()` / particle gather 路径 |

因此不能把 “external field” 泛泛解释为一种场。它至少有“加到网格解上”和“直接给粒子用”两种物理路径。

## 6. Python 外场 callback 只在 finest level 调用

源码位置：`../warpx/Source/Initialization/WarpXInitData.cpp:1707-1710`。

```cpp
if (lev == finestLevel()) {
    // Call Python callback which might write values to external field multifabs
    ExecutePythonCallback("loadExternalFields");
}
```

Python callback 的触发条件是 `lev == finestLevel()`。这意味着用户通过 Python 写外场时，要理解 callback 的 level 语义；它不是在每个 level 的每个 `LoadExternalFields(lev)` 调用中都执行。

## 7. openPMD 读入根据目标 MultiFab 的 index type 修正坐标

源码位置：`../warpx/Source/Initialization/WarpXInitData.cpp:1767-1844`。

```cpp
void
WarpX::ReadExternalFieldFromFile (
       const std::string& read_fields_from_path, amrex::MultiFab* mf,
       const std::string& F_name, const std::string& F_component, int dest_comp)
{
#if !defined(WARPX_USE_OPENPMD)

    amrex::ignore_unused(read_fields_from_path, mf, F_name, F_component, dest_comp);
    WARPX_ABORT_WITH_MESSAGE("ReadExternalFieldFromFile requires OpenPMD support to be enabled");

#elif defined(WARPX_DIM_RCYLINDER) || defined(WARPX_DIM_RSPHERE)

    amrex::ignore_unused(read_fields_from_path, mf, F_name, F_component, dest_comp);
    WARPX_ABORT_WITH_MESSAGE("ReadExternalFieldFromFile is not supported for 1D RCYLINDER and RSPHERE");

#else
```

文件读入依赖 openPMD 支持；RCYLINDER/RSPHERE 不支持。

读入前先根据目标 `MultiFab` 的 index type 调整物理起点：

```cpp
amrex::Geometry const& geom0 = Geom(0);
auto problo = geom0.ProbLoArray();
const auto dx = geom0.CellSizeArray();
const amrex::IntVect nodal_flag = mf->ixType().toIntVect();
for (int idim = 0; idim < AMREX_SPACEDIM; ++idim) {
    if (nodal_flag[idim] == 0) { // cell center
        problo[idim] += 0.5_rt*dx[idim]; // shift by half dx
    }
}
```

这与 parser 外场的坐标偏移逻辑一致：外部文件的值要插值到目标场分量实际所在的位置。如果目标场是 cell-centered，就从 cell center 位置开始；如果是 nodal，就从节点位置开始。

最终 kernel 调用 `ExternalFieldView` 做插值：

```cpp
amrex::ParallelFor (tb,
    [=] AMREX_GPU_DEVICE (int i, int j, int k) {
        // i,j,k denote x,y,z indices in 3D xyz.
        // i,j denote r,z indices in 2D rz; k is just 0

        // ii is used for 2D RZ mode
#if defined(WARPX_DIM_RZ)
        // In 2D RZ, i denoting r can be < 0
        // but mirrored values should be assigned.
        const int ii = (i<0)?(-i):(i);
#else
        const int ii = i;
#endif

        // Physical coordinates of the grid point
        // 0,1,2 denote x,y,z in 3D xyz.
        // 0,1 denote r,z in 2D rz.
        const auto pos = amrex::RealVect{
            AMREX_D_DECL(problo[0] + ii*dx[0],
                          problo[1] + j *dx[1],
                          problo[2] + k *dx[2])};
        mffab(i,j,k, dest_comp) = external_field_view(pos);
    }
```

RZ 中 `i<0` 时使用 `ii=-i`，说明读入外场对径向负索引做镜像取值。这和 RZ guard/axis 处理有关，后续 RZ 章节需要详细展开。

## 8. `ExternalFieldReader` 做 openPMD 几何检查和插值缓存

源码位置：`../warpx/Source/Initialization/ExternalField.cpp:208-433`。

```cpp
void ExternalFieldReader::load_data (amrex::RealBox const& pbox)
{
#if defined(WARPX_USE_OPENPMD) && !defined(WARPX_DIM_RCYLINDER) && !defined(WARPX_DIM_RSPHERE)
    using namespace amrex;

    auto series = openPMD::Series(m_file, openPMD::Access::READ_ONLY);
    auto iseries = series.iterations.begin()->second;
    auto F = iseries.meshes[m_name];

    const bool c_order = F.getAttribute("dataOrder").get<std::string>() == "C";
    amrex::ignore_unused(c_order);

    auto axisLabels = F.getAttribute("axisLabels").get<std::vector<std::string>>();
    auto fileGeom = F.getAttribute("geometry").get<std::string>();
```

文件几何检查按维度分支：

```cpp
#if defined(WARPX_DIM_3D)
    WARPX_ALWAYS_ASSERT_WITH_MESSAGE(fileGeom == "cartesian", "3D can only read from files with cartesian geometry");
    if (axisLabels.at(0) == "x" && axisLabels.at(1) == "y" && axisLabels.at(2) == "z") {
        xyz_order = true;
    } else if (axisLabels.at(2) == "x" && axisLabels.at(1) == "y" && axisLabels.at(0) == "z") {
        xyz_order = false;
    } else {
        WARPX_ABORT_WITH_MESSAGE("3D expects axisLabels {x, y, z} or {z, y, x}");
    }
#elif defined(WARPX_DIM_XZ)
    WARPX_ALWAYS_ASSERT_WITH_MESSAGE(fileGeom == "cartesian", "XZ can only read from files with cartesian geometry");
```

这说明 openPMD 外场不是任意 mesh 都能读。WarpX 明确要求：

- 3D/XZ/1D_Z 使用 cartesian geometry；
- RZ 使用 `thetaMode` geometry；
- axisLabels 必须是预期顺序或其反序。

读入数据范围时，为插值多取一层并留出 roundoff 余量：

```cpp
auto ilo = int(std::floor( (plo-m_offset[idim])/m_dx[idim] ));
auto ihi = int(std::floor( (phi-m_offset[idim])/m_dx[idim] ))+1; // +1 for interpolation
--ilo; // in case there are roundoff errors
++ihi;
lo[idim] = std::max(ilo, 0);
hi[idim] = std::min(ihi, m_size[idim]-1);
```

这段与 `ExternalFieldView` 的线性/双线性/三线性插值配套：要在某个目标位置插值，至少需要包围该位置的相邻网格点；`+1` 和额外扩展用于保证边界和浮点误差情况下仍能取到需要的数据。

## 9. `ExternalFieldView` 是 kernel 中使用的轻量插值器

源码位置：`../warpx/Source/Initialization/ExternalField.H:83-172`。

```cpp
struct ExternalFieldView
{
    //! Return value for given position. Linear interpolation is
    //! performed. This returns zero if no data are available.
    AMREX_GPU_HOST_DEVICE AMREX_FORCE_INLINE
    amrex::Real operator() (amrex::RealVect const& pos) const
    {
        // Get index of the external field array
        AMREX_D_TERM(const auto i0 = static_cast<int>(std::floor( (pos[0]-offset[0])/dx[0] ));,
                     const auto i1 = static_cast<int>(std::floor( (pos[1]-offset[1])/dx[1] ));,
                     const auto i2 = static_cast<int>(std::floor( (pos[2]-offset[2])/dx[2] )));
```

3D 插值路径：

```cpp
return static_cast<amrex::Real>(
    ablastr::math::trilinear_interp<double>(
        xx0, xx0+dx[0], xx1, xx1+dx[1], xx2, xx2+dx[2],
        table(i0  ,i1  ,i2  ),
        table(i0  ,i1  ,i2+1),
        table(i0  ,i1+1,i2  ),
        table(i0  ,i1+1,i2+1),
        table(i0+1,i1  ,i2  ),
        table(i0+1,i1  ,i2+1),
        table(i0+1,i1+1,i2  ),
        table(i0+1,i1+1,i2+1),
        pos[0], pos[1], pos[2]));
```

所以文件外场进入 WarpX 后不是 nearest-cell 赋值，而是按目标位置做线性插值。物理上，这避免外部场文件网格和 WarpX 网格不完全重合时出现阶梯误差；数值上也意味着外部场文件必须覆盖 WarpX 目标位置周围的插值邻域。

## 10. 本轮结论

外场初始化主链可以总结为：

```text
ReadParameters()
  -> ExternalFieldParams(pp_warpx)
     -> B/E_ext_grid_init_style
     -> constant values / parser functions / read_fields_from_path

AllocLevelMFs()
  -> allocate Efield_fp_external / Bfield_fp_external when grid external field is non-default
  -> allocate E_external_particle_field / B_external_particle_field when particle external field reads from file

InitLevelData() / PostRestart()
  -> LoadExternalFields(lev)
     -> parser: ComputeExternalFieldOnGridUsingParser()
     -> file: ReadExternalFieldFromFile()
     -> python: ExecutePythonCallback("loadExternalFields") at finest level

Fresh run after self-field solve
  -> AddExternalFields(lev)
     -> Efield_fp += Efield_fp_external or constant E_external_grid
     -> Bfield_fp += Bfield_fp_external or constant B_external_grid
```

后续需要继续追踪两条使用路径：

1. `Parallelization/WarpXComm.cpp::UpdateAuxilaryData()` 如何把 external particle fields 加到粒子 gather 看到的 aux 场。
2. `Utils/WarpXMovingWindow.cpp` 如何在 moving window 里处理 constant/parser 外场，并为什么 read-from-file 当前被禁止。

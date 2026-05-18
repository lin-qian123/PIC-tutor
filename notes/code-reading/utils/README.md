# Utils 源码精读入口

绑定源码：`../warpx/Source/Utils`。

## 模块边界

- 构建入口：`Utils/CMakeLists.txt`、`Utils/Make.package`。
- 子模块：`Parser/`、`Physics/`、`Logo/`、`Algorithms/`。
- 主要文件：`WarpXAlgorithmSelection.H`、`WarpXConst.H`、`WarpXUtil.*`、`WarpXMovingWindow.cpp`、`ParticleUtils.*`、`SpeciesUtils.*`、`ParserUtils.*`、`IntervalsParser.*`、`IonizationEnergiesTable.H`。

## 核心问题

- 枚举型算法选择如何从字符串参数转成 C++ enum。
- parser 字符串如何保存、查询和用于 device function。
- moving window、boosted frame、species utilities 和 ionization tables 如何支撑物理模块。

## 精读顺序

1. `WarpXAlgorithmSelection.H`。
2. `WarpXConst.H`。
3. `Parser/`。
4. `WarpXUtil.*`。
5. `WarpXMovingWindow.cpp`。
6. `ParticleUtils.*`、`SpeciesUtils.*`。
7. `Physics/IonizationEnergiesTable.H`。

## 输出目标

- `00-algorithm-selection.md`
- `01-parser-system.md`
- `02-parameter-family-entrypoints.md`
- `03-moving-window-and-boost.md`
- `04-species-and-ionization-utils.md`
- `05-deep-solver-object-parameter-families.md`
- `06-external-vector-potential-and-poisson-boundary-parameters.md`
- `07-parameter-validation-links-for-boundary-and-external-fields.md`
- `08-low-frequency-parameter-families-and-pass-throughs.md`

## 当前进度

- 已完成 `01-parser-system.md`：梳理 `ParmParse` 前缀命名空间、`queryWithParser/queryArrWithParser` 与 `Store_parserString/makeParser` 的分工、`IntervalsParser` 的时间切片语法、`query_enum_sloppy + AMREX_ENUM` 的算法枚举入口，以及参数到章节索引应按“第一次解析层 + 主要物理章节”两级回填。
- 已完成 `02-parameter-family-entrypoints.md`：梳理 `species / laser / diagnostics / reduced diagnostics / collision / boundary / solver / psatd / implicit` 九组高频参数族在 `WarpX.cpp`、`WarpXAMReXInit.cpp`、`FieldBoundaries.cpp`、`MultiParticleContainer`、`MultiDiagnostics`、`MultiReducedDiags`、`CollisionHandler`、`ThetaImplicitEM` 和实例内部配置层的读取入口，明确区分 `global gate / factory dispatch / instance-local parse` 三层壳。
- 已完成 `05-deep-solver-object-parameter-families.md`：继续把参数入口图往 solver-object 深层推进，梳理 `fluids`、`hybrid_pic_model`、`macroscopic`、`effective potential` 四组参数怎样经过 root existence gate、对象构造、实例内 `ReadParameters()` 与 `InitData()/ComputeSigma()` 等运行态 materialization 层。
- 已完成 `06-external-vector-potential-and-poisson-boundary-parameters.md`：继续把参数入口图推进到 `ExternalVectorPotential` 与 `PoissonBoundaryHandler` 这类子对象和边界 parser 层，梳理 `external_vector_potential.*`、`boundary.potential_*`、`warpx.eb_potential(x,y,z,t)` 怎样经过 parent gate、subobject parse、parser build 和 runtime apply。
- 已完成 `07-parameter-validation-links-for-boundary-and-external-fields.md`：继续把参数系统主线闭合到 examples / analysis 层，梳理 `boundary.potential_* -> electrostatic_dirichlet_bc`、open-boundary Poisson -> `open_bc_poisson_solver`、effective-potential -> `effective_potential_electrostatic`、`warpx.eb_potential(x,y,z,t) -> ion_beam_extraction` 四条最稳定的 validation 链，并明确 `external_vector_potential.*` 当前仍缺独立强 regression。
- 已完成 `08-low-frequency-parameter-families-and-pass-throughs.md`：继续把 `parameter-map` 尾项从零散补丁提升成一层正式源码结论，梳理 grouped alias、AMReX-owned 输入、外场聚合开关、PSATD/centering grouped key、macroscopic/hybrid parser 参数以及 Schwinger 区域边界框，明确“文档合并名”和“真实 parser key / 本地消费者”之间的区别。

## 验证线索

- `Docs/source/usage/parameters.rst`
- boosted frame examples。

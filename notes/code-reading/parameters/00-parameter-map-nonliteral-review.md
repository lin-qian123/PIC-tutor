# Parameter map non-literal review

本笔记记录 `docs/parameter-map.md` 中没有普通字面量首参数调用、但已经完成源码结构复核的 10 条参数。它只证明参数键的拥有者、动态构造方式和读取/消费入口，不把这些证据升级成默认值、别名、完整 validation 或 runtime physics regression。

## AMReX-owned refinement inputs

- `amr.ref_ratio`：由相邻 `../amrex/Src/AmrCore/AMReX_AmrMesh.cpp` 的 `pp.queryarr("ref_ratio", ratios)` 读取；同一段代码拒绝同时提供 `ref_ratio` 与 `ref_ratio_vect`，随后把标量 ratio materialize 到每个 level 的 `ref_ratio[i]`。
- `amr.ref_ratio_vect`：同一文件通过 `pp.queryarr("ref_ratio_vect", ratios_vect, 0, nratios_vect)` 读取，并按 level/方向写入 `ref_ratio[i][n]`。WarpX 侧随后经 `WarpX::refRatio()` 使用该 `IntVect`，而不是在 `WarpX::ReadParameters()` 中重新拥有这两个输入。

## Dynamic keys

- `<species_name>.attribute.<name>(...)`：`PhysicalParticleContainer.cpp` 先读取 `addIntegerAttributes`/`addRealAttributes`，再用属性名拼接 `attribute.<name>(...)`，保存 parser 字符串并编译 7 变量 parser。
- `<collision_name>.<scattering_process>_cross_section`：DSMC 和 Background MCC 都先读取 scattering process 列表，再拼接 `<process>_cross_section` 查询截面文件。
- `<collision_name>.<scattering_process>_energy`：DSMC 在特定 reaction 类型下拼接 `<process>_energy`，并通过 parser-aware getter 读取能量。
- `<diag_name>.adios2_operator.parameters.*` / `<diag_name>.adios2_engine.parameters.*`：OpenPMD writer 用 `ParmParse::getEntries(...)` 枚举前缀下的任意键，去掉前缀后写入 operator/engine 参数 map。
- 三条 `particle_fields` 参数：`Diagnostics.cpp` 以 field name 拼接 `do_average`、`(x,y,z,ux,uy,uz)` 和 `filter(...)`；前两者编译/保存 parser，filter 以是否存在作为启用开关，随后由 `ParticleReductionFunctor` 消费。

## Audit contract

可重复审计入口：`scripts/audit_parameter_map_structured_review.py`。当前 10/10 通过；`scripts/audit_parameter_map_parser_anchors.py` 将它们标记为 `structured_review_verified`，同时保留普通 269 条 parser-call anchor、166 条 parser-literal anchor 和“runtime value semantics 仍未证明”的边界。

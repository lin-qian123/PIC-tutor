# Birdsall 3A ES1 与 WarpX 初始化/演化源码 crosswalk

第 3A 章已经把历史 `INIT -> SETRHO -> FIELDS -> SETV -> ACCEL -> MOVE -> HISTRY` 阶段链映射到现代 WarpX。本笔记和 `scripts/audit_3a_birdsall_warpx_crosswalk.py` 将这条映射固定为可重复检查：

- 历史层：3A 阶段名、静电 PIC 的职责和不可等同边界；
- 现代生命周期：`main.cpp` 的 `InitData()`/`Evolve()`、`WarpXInitData.cpp` 的 fresh/restart 和 electrostatic 初始化、`WarpXEvolve.cpp` 的 step dispatch；
- 粒子层：`PhysicalParticleContainer::InitData()`/`Evolve()`；
- 验证层：`Langmuir`、`initial_distribution`、`space_charge_initialization` 和 `projection_div_cleaner` 的分层说明；
- 资产层：项目内 Birdsall PDF 和中文讲解目录。

当前合同的意义是确认章节仍然指向当前 checkout 的代表性源码表面；它不把历史 ES1 与现代 WarpX 宣称为逐函数等价，也不把源码锚点升级为新的 runtime physics gate。

# 应用综合章源码与案例入口

本目录不重复底层模块精读，而是把已经分散在 `Initialization/`、`Particles/`、`FieldSolver/`、`Diagnostics/` 和各类 validation map 里的材料，重新收束成“一个应用问题如何从解析模型一路落到输入、源码路径、分析脚本和回归边界”的综合入口。

当前目标不是覆盖所有 physics application，而是优先收掉 `TODO.md` 里已经具备足够本地证据的大项。

## 当前条目

1. `00-langmuir-wave.md`
   - `Examples/Tests/langmuir/` 与 `langmuir_fluids/` 的应用级入口
   - 从冷等离子体解析振荡、输入骨架、源码调用链，到 analysis/checksum/PICMI 的验证分层
2. `01-uniform-plasma.md`
   - `Examples/Physics_applications/uniform_plasma/` 的应用级入口
   - 从均匀热等离子体的噪声/性能/workflow 基线，到 writer/checkpoint/restart 与邻近能量强断言测试的边界
3. `02-lwfa-pwfa.md`
   - `Examples/Physics_applications/laser_acceleration/` 与 `plasma_acceleration/` 的应用级入口
   - 把 `LWFA runtime matrix` 与 `PWFA workflow matrix` 从 moving window、boosted frame、diagnostics、MR 和 PICMI/native 前端分裂的角度重新收束成一条 wakefield acceleration 主线
4. `03-laser-targets-rpa-tnsa.md`
   - `Examples/Physics_applications/laser_ion/` 与 `plasma_mirror/` 的应用级入口
   - 把最强的 laser-target 本地入口、surface-plasma workflow baseline，以及 `RPA/TNSA` 当前仅作为机制标签而非独立本地应用树的边界一次写清
5. `04-capacitive-discharge.md`
   - `Examples/Physics_applications/capacitive_discharge/` 的应用级入口
   - 把 1D Turner benchmark、Python callback Poisson solver、DSMC 分支和 2D native/PICMI workflow baseline 收束成一条 PIC-MCC 低温等离子体主线
6. `05-magnetic-reconnection.md`
   - `Examples/Tests/ohm_solver_magnetic_reconnection/` 的应用级入口
   - 把 `HybridPICModel`、force-free-sheet 初场、reduced `FieldProbe`、重联率提取和 checksum 分层收束成一条 hybrid-PIC space-plasma 主线
7. `06-beam-collider-fel-extraction.md`
   - `diff_lumi_diag`、`beam_beam_collision`、`free_electron_laser`、`ion_beam_extraction` 与 `accelerator_lattice` 的综合入口
   - 把 luminosity 强谱基准、collider-QED 应用骨架、boosted FEL 强 benchmark、EB electrostatic extraction 与 beamline optics 强回归收束成一条束流与加速器主线

## 使用方式

- 若要理解一个应用案例“到底在验证什么”，先看本目录。
- 若要追具体模块实现，再跳回相应底层笔记：
  - 初始化：`notes/code-reading/initialization/*`
  - 粒子推进与沉积：`notes/code-reading/particles/*`
  - 场求解：`notes/code-reading/fieldsolver/*`
  - 诊断：`notes/code-reading/diagnostics/*`

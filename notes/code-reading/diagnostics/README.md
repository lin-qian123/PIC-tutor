# Diagnostics 源码精读入口

绑定源码：`../warpx/Source/Diagnostics`。

## 模块边界

- 构建入口：`Diagnostics/CMakeLists.txt`、`Diagnostics/Make.package`。
- 子模块：`ComputeDiagFunctors/`、`FlushFormats/`、`ParticleDiag/`、`ReducedDiags/`。
- 顶层：`Diagnostics.*`、`FullDiagnostics.*`、`MultiDiagnostics.*`、`WarpXOpenPMD.*`、`ParticleIO.cpp`、`FieldIO.*`、`BTDiagnostics.*`。

## 核心问题

- diagnostics 如何从参数创建、调度、计算、打包、输出。
- full diagnostics、reduced diagnostics、BTD、checkpoint、plotfile、openPMD 的数据路径有何不同。
- field functor 和 particle functor 如何处理 staggering、RZ modes、derived quantities。

## 精读顺序

1. `BoundaryScrapingDiagnostics`、`ParticleBoundaryBuffer` 与 Python scraped-particle 接口。
2. `MultiDiagnostics` 与 `Diagnostics` 基类。
3. `FullDiagnostics` 和 `ParticleDiag`。
4. `ComputeDiagFunctors`。
5. `ReducedDiags`。
6. `FlushFormats`。
7. `WarpXOpenPMD`、`ParticleIO`、restart/checkpoint。
8. `BTDiagnostics`。

## 输出目标

- `00-boundary-scraping-diagnostics-python.md`
- `01-diagnostics-dispatch.md`
- `02-field-and-particle-functors.md`
- `03-reduced-diagnostics.md`
- `04-io-formats-and-restart.md`
- `05-reduced-diagnostic-case-studies.md`
- `06-writer-comparison-and-minimal-cases.md`
- `07-output-layouts-and-reading-tools.md`
- `08-template-cases-and-boundaryscraping-example.md`
- `09-python-boundary-buffer-callback-case.md`

## 当前进度

- 已完成 `00-boundary-scraping-diagnostics-python.md`：梳理 `BoundaryScrapingDiagnostics` 如何直接绑定 `ParticleBoundaryBuffer`、为何只支持 openPMD / particle-only 输出、flush 后怎样按 boundary 清空 buffer，以及 Python `ParticleBoundaryBufferWrapper` / PICMI `ParticleBoundaryScrapingDiagnostic` 如何零拷贝消费同一份 scraped-particle 状态。
- 已完成 `01-diagnostics-dispatch.md`：梳理 `MultiDiagnostics` 的类型分派、`Diagnostics` 的 init/compute/flush 模板骨架、`FullDiagnostics` 的 field-functor 与 time-averaged 分支，以及 `ParticleDiag` 作为 species 输出配置对象而非独立粒子 buffer 的真实语义。
- 已完成 `02-field-and-particle-functors.md`：梳理 `ComputeDiagFunctors` 的字段计算层、`ParticleReductionFunctor` 作为“从粒子生成 cell field”的特殊 field functor、以及 `WarpXOpenPMD` / `FlushFormatPlotfile` 在 writer 阶段如何通过 `tmp.copyParticles(...)` 真正应用 `ParticleDiag` 的过滤与变量选择，并明确 `phi` / `E/B` on particles 只允许 `diag_type=Full`。
- 已完成 `03-reduced-diagnostics.md`：梳理 `MultiReducedDiags` 的工厂/调度角色、`ReducedDiags` 的统一表格输出协议、`FieldEnergy` / `ParticleEnergy` 这类“现算即写” reduced diagnostics，以及 `FieldPoyntingFlux` 这类需要 `WriteCheckpointData/ReadCheckpointData` 延续内部积分状态的例外。
- 已完成 `04-io-formats-and-restart.md`：梳理 `FlushFormatCheckpoint` 如何保存真正的 WarpX 运行态、`BTDiagnostics` 如何用 slice/buffer 状态机而不是瞬时输出模型生成 back-transformed diagnostics，以及 restart 链如何恢复 reduced diagnostics 的 checkpoint 数据。
- 已完成 `05-reduced-diagnostic-case-studies.md`：梳理 `FieldProbe` 如何通过 probe-particle 容器对 `E/Bfield_aux` 做 point/line/plane gather、`ParticleHistogram` / `ParticleHistogram2D` 如何分别实现一维文本 histogram 和 openPMD 二维相空间网格，以及 `LoadBalanceCosts/LoadBalanceEfficiency` 如何把 box-level 负载分布、效率标量和对应 regression 断言暴露出来。
- 已完成 `06-writer-comparison-and-minimal-cases.md`：梳理 `Diagnostics` 如何按 `format` 分派到 `plotfile/openpmd/checkpoint` 三类 writer、为什么 checkpoint 是 `FullDiagnostics` 的受限运行态序列化分支，以及 `FieldProbe`、`ParticleHistogram2D`、`LoadBalanceCosts` 在本地 examples 中可直接复用的最小输入骨架。
- 已完成 `07-output-layouts-and-reading-tools.md`：整理 `plotfile/openPMD/checkpoint` 三类输出的目录树、典型读取工具和适用场景，并补充 `yt`、`openPMD-viewer/api`、`read_raw_data.py`、`plot_distribution_mapping.py` 这些读者侧入口之间的边界。
- 已完成 `08-template-cases-and-boundaryscraping-example.md`：把 `plotfile/openPMD/checkpoint/BoundaryScraping` 四类输出统一整理成固定模板，分别给出最小输入片段、典型目录树、读取入口和适用场景，并用 `thomson_parabola_spectrometer`、`point_of_contact_eb`、`scraping` 等本地例子补上 `BoundaryScraping/openPMD` 的真实读取方式与实现边界。
- 已完成 `09-python-boundary-buffer-callback-case.md`：把 Python `ParticleBoundaryBufferWrapper` 的两种最小消费模式固定下来，分别整理“运行结束后统一检查 buffer”和“callback/在线物理里按步消费事件流”的模板，并用 `particle_boundary_scrape` 和 `spacecraft_charging` 说明它与 `BoundaryScrapingDiagnostics` 共用同一份 buffer 但清空时机不同。

## 验证线索

- `Examples/Tests/reduced_diags/`
- `Examples/Tests/restart/`
- `Examples/Tests/openpmd/` 或 openPMD 相关 examples。

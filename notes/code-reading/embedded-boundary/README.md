# EmbeddedBoundary 源码精读入口

绑定源码：`../warpx/Source/EmbeddedBoundary`。

## 模块边界

- 构建入口：`EmbeddedBoundary/CMakeLists.txt`、`EmbeddedBoundary/Make.package`。
- 主要文件：`EmbeddedBoundaryInit.*`、`WarpXInitEB.cpp`、`WarpXFaceExtensions.cpp`、`DistanceToEB.H`、`ParticleScraper.H`、`ParticleBoundaryProcess.H`、`WarpXFaceInfoBox.H`。

## 核心问题

- EB 几何如何初始化并映射到 AMReX EB 数据结构。
- face extension 如何影响 field solve 和 boundary treatment。
- 粒子如何被 EB scrape，沉积 shape 如何在 EB 附近降阶或修正。

## 精读顺序

1. `Enabled.*` 与 EB 开关。
2. `EmbeddedBoundaryInit.*` 和 `WarpXInitEB.cpp`。
3. `WarpXFaceInfoBox.H` 和 `WarpXFaceExtensions.cpp`。
4. `DistanceToEB.H`。
5. `ParticleScraper.H` 和 `ParticleBoundaryProcess.H`。

## 输出目标

- `00-eb-initialization.md`
- `01-face-extensions.md`
- `02-particle-scraping-and-deposition-near-eb.md`

## 当前进度

- 已完成 `00-eb-initialization.md`：梳理 `Enabled.*` 的运行时开关、`WarpX::InitEB()` 的 AMReX EB2 构建入口、`ComputeDistanceToEB()` 的 signed-distance 场填充，以及 `EmbeddedBoundaryInit.*` 中 reduced-shape、stair-case update、ECT edge/face update 标记的初始化逻辑。
- 已完成 `01-face-extensions.md`：梳理 `S_stab` 稳定性阈值、`flag_info_face/flag_ext_face` 语义、one-way / eight-ways extension、BCK fallback，以及 `FaceInfoBox` 如何把借用关系传给 ECT `B` 更新。
- 已完成 `02-particle-scraping-and-deposition-near-eb.md`：梳理 `scrapeParticlesAtEB()` 的 signed-distance 判定、`DistanceToEB` 法向重建、`ParticleBoundaryProcess::Absorb()` 的 invalid-id 吸收语义，以及 `save_particles_at_eb` / `ParticleBoundaryBuffer` 的交点回溯和 scraped buffer 记录。
- `EmbeddedBoundary/` 的三段主链已经基本齐全，下一步优先回到 `Boundary / AMR` 主线，进入 `Parallelization/` 或 AMR coarse-fine interface。

## 验证线索

- `Examples/Tests/embedded_boundary_cube/`
- `Examples/Tests/embedded_boundary_rotated_cube/`
- `Examples/Tests/embedded_boundary_em_particle_absorption/`
- `Examples/Tests/embedded_boundary_diffraction/`
- `Examples/Tests/embedded_circle/`
- EB 相关 reduced diagnostics。

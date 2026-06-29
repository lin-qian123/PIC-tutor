# TODO

- [x] 2026-06-29：完成 `v0.15` transition-zone 测试草案版：冻结 `manuscript/VERSION-v0.14.md`，把当前版本说明切到 `manuscript/VERSION.md` 的 v0.15，新增 `scripts/build_v15.py`，生成 `dist/pic-tutor-v0.15.md` 与 `dist/pic-tutor-v0.15.html`；第 7 章新增 `7.7.4 v0.15 dedicated transition-zone 测试草案`，写出 dedicated regression family、最小 2D MR 输入卡骨架、粒子分区预期表、现有 diagnostics 可观测边界和测试专用 instrumentation 建议。
- [x] 2026-06-29：完成 `v0.14` transition-zone validation 线索版：冻结 `manuscript/VERSION-v0.13.md`，把当前版本说明切到 `manuscript/VERSION.md` 的 v0.14，新增 `scripts/build_v14.py`，生成 `dist/pic-tutor-v0.14.md` 与 `dist/pic-tutor-v0.14.html`；第 7 章新增 `7.7.3 v0.14 transition-zone validation 应该直接检查什么`，把 startup buffer allocation、mask topology、particle partition、gather/deposition routing 和 coarse-level sync 写成 validation checklist。
- [x] 2026-06-29：完成 `v0.13` 第 7 章 HTML 审读与排版收口版：冻结 `manuscript/VERSION-v0.12.md`，把当前版本说明切到 `manuscript/VERSION.md` 的 v0.13，新增 `scripts/build_v13.py`，生成 `dist/pic-tutor-v0.13.md` 与 `dist/pic-tutor-v0.13.html`；新增 `manuscript/assets/pic-tutor-html-style.html`，改善宽表格、长源码路径、inline code、Mermaid 源码块、TOC 和打印视图的浏览器可读性。
- [x] 2026-06-29：完成 `v0.12` AMR coarse-fine 图形化证据草稿：冻结 `manuscript/VERSION-v0.11.md`，把当前版本说明切到 `manuscript/VERSION.md` 的 v0.12，新增 `scripts/build_v12.py`，生成 `dist/pic-tutor-v0.12.md` 与 `dist/pic-tutor-v0.12.html`；第 7 章已用 Mermaid 图串联 `F(s)-F(c)`、`E/Bfield_aux`、`E/Bfield_cax`、`current/rho_buf` 和 `PartitionParticlesInBuffers()`，并新增 AMR regression 证据等级表。
- [x] 2026-06-29：完成 `v0.11` AMR guard-cell/regrid 闭环草稿：冻结 `manuscript/VERSION-v0.10.md`，把当前版本说明切到 `manuscript/VERSION.md` 的 v0.11，新增 `scripts/build_v11.py`，生成 `dist/pic-tutor-v0.11.md` 与 `dist/pic-tutor-v0.11.html`；第 7 章已把 `GuardCellManager`、`WarpXComm` 和 `WarpXRegrid::RemakeLevel()` 串成 guard-cell 预算、field/source 通信和 load-balance 后重建的正文闭环。
- [x] 2026-06-29：完成 `v0.10` 边界强 analysis 路径扩写草稿：冻结 `manuscript/VERSION-v0.9.md`，把当前版本说明切到 `manuscript/VERSION.md` 的 v0.10，新增 `scripts/build_v10.py`，生成 `dist/pic-tutor-v0.10.md` 与 `dist/pic-tutor-v0.10.html`；第 7 章已把 particle domain boundary、PEC/PMC、particles in PML 和 RZ EB scraping 四条强 analysis 路径扩写成正文级判据说明。
- [x] 2026-06-29：完成 `v0.9` 边界 regression 判据索引草稿：冻结 `manuscript/VERSION-v0.8.md`，把当前版本说明切到 `manuscript/VERSION.md` 的 v0.9，新增 `scripts/build_v09.py`，生成 `dist/pic-tutor-v0.9.md` 与 `dist/pic-tutor-v0.9.html`；第 7 章已按当前 `../warpx` 的 `Examples/Tests/*/CMakeLists.txt`、输入卡和 `analysis*.py` 新增统一 regression 入口索引表，明确区分强 analysis、restart 一致性和 checksum-only 证据。
- [x] 2026-06-29：完成 `v0.8` 边界与 AMR 源码入口校准草稿：冻结 `manuscript/VERSION-v0.7.md`，把当前版本说明切到 `manuscript/VERSION.md` 的 v0.8，新增 `scripts/build_v08.py`，生成 `dist/pic-tutor-v0.8.md` 与 `dist/pic-tutor-v0.8.html`；第 7 章已按 `../warpx` 当前 `pkuHEDPbranch / 8c488b1a9` 增补边界/PML/guard-cell/AMR 源码入口地图，串联 `WarpX::MakeWarpX()`、`FieldBoundaries`、`ParticleBoundaries`、`WarpXFieldBoundaries`、`WarpXComm`、`GuardCellManager`、`WarpXRegrid` 和 boundary scraping 入口。

## v0.15 后续收口队列

- [x] 人工审读并修正 `dist/pic-tutor-v0.12.html` 暴露出的第 7 章 HTML 排版风险：宽表格、Mermaid 图、公式、inline code 和长源码路径需要项目级样式兜底。
- [x] 继续细核 `GuardCellManager.cpp`、`WarpXComm.cpp`、`WarpXRegrid.cpp` 的 AMR/regrid/guard-cell 路径，把 v0.8 入口地图扩成可讲解的正文段落。
- [x] 把 `Examples/Tests/boundaries`、`pec`、`pml`、`particles_in_pml`、`particle_boundary_scrape` 和 RZ scraping 相关 regression 入口回填到第 7 章。
- [ ] 继续完成 PSATD/Galilean/NCI/PML 论文 MinerU 笔记，补第 6-7 章的文献闭环。
- [x] 为 v0.9 规划第 7 章边界 regression 判据表，明确哪些是物理强断言、哪些只是 checksum 或 smoke。
- [x] 为 v0.10 选择 3-4 条强 analysis 路径扩写成正文：从 particle boundaries、PEC/PMC、particles-in-PML 和 RZ scraping 开始。
- [x] 为 v0.11 继续细核 `GuardCellManager.cpp`、`WarpXComm.cpp`、`WarpXRegrid.cpp`，把 AMR/regrid/guard-cell 从入口地图扩成第 7 章正文。
- [x] 为 v0.12 把 coarse-fine substitution、transition zone、`WarpXComm_K.H` 点值 kernel 和对应 regression 证据进一步图形化。
- [x] 为 v0.13 做一次第 7 章 HTML 人工审读与排版修正，尤其检查宽表格、Mermaid 图、公式和长源码路径在浏览器中的可读性。
- [x] 为 v0.14 继续补 transition-zone 专门 validation 线索：直接检查 `n_field_gather_buffer/n_current_deposition_buffer`、`E/Bfield_cax`、`current_buf/rho_buf` 和 `PartitionParticlesInBuffers()` 的分析入口。
- [x] 为 v0.15 继续把 dedicated transition-zone validation 方案推进到测试草案层：设计最小输入卡、预期粒子分区表、可观测 diagnostics/analysis 输出，以及是否需要 WarpX 侧测试专用 instrumentation。
- [ ] 为 v0.16 继续推进第 7 章 transition-zone validation：把 v0.15 草案拆成可实际落地的 WarpX regression patch 计划，包括需要新增的 route-count reduced output、mask 输出开关、analysis 断言和 CMake wiring。

- [x] 2026-06-29：完成 `v0.4` 沉积与形函数校准草稿：冻结 `manuscript/VERSION-v0.3.md`，把当前版本说明切到 `manuscript/VERSION.md` 的 v0.4，新增 `scripts/build_v04.py`，生成 `dist/pic-tutor-v0.4.md` 与 `dist/pic-tutor-v0.4.html`；第 5 章已按 `../warpx` 当前 `pkuHEDPbranch / 8c488b1a9` 重核 `ShapeFactors`、`DepositCurrent/DepositCharge`、Esirkepov/Villasenor/Vay 分派和 Langmuir / `vay_deposition` 验证入口。
- [x] 2026-06-29：完成 `v0.3` 粒子推进器校准草稿：冻结 `manuscript/VERSION-v0.2.md`，把当前版本说明切到 `manuscript/VERSION.md` 的 v0.3，新增 `scripts/build_v03.py`，生成 `dist/pic-tutor-v0.3.md` 与 `dist/pic-tutor-v0.3.html`；第 4 章已按 `../warpx` 当前 `pkuHEDPbranch / 8c488b1a9` 重核 `UpdateMomentumBoris/Vay/HigueraCary`、`PushSelector`、`PushPX` 和 `particle_pusher` 强验证入口。
- [x] 2026-06-25：完成 `v0.2` 可审校草稿：冻结 `manuscript/VERSION-v0.1.md`，把当前版本说明切到 `manuscript/VERSION.md` 的 v0.2，新增 `scripts/build_v02.py`，生成 `dist/pic-tutor-v0.2.md` 与 `dist/pic-tutor-v0.2.html`；第 2、3、3A 章已按 `../warpx` 当前 `pkuHEDPbranch / 8c488b1a9` 重核源码基线、路径和关键行号。
- [x] 2026-06-25：开始收束 `v0.1` 第一卷草稿，新增版本说明和 `scripts/build_v01.py`，把现有 11 章与附录 A 合订为 `dist/pic-tutor-v0.1.md`，并在本机存在 `pandoc` 时生成 HTML 预览；v0.1 版本说明现已冻结到 `manuscript/VERSION-v0.1.md`。本版范围限定为 PIC 主线、WarpX 主循环、初始化、推进、沉积、场求解、边界/AMR、诊断和第一批案例，尚不是完整 38 章终稿。
- [x] 2026-06-23：完成阶段性收口：复核当前工作区仍只包含 `README.md`、`TODO.md`、`docs/example-regression-map.md`、`docs/parameter-map.md` 四个文档改动；确认 `PIC-tutor` 已是 git 仓库并修正旧阻塞项；记录当前相邻 `../warpx` checkout 为 `pkuHEDPbranch / 8c488b1a9`，后续章节源码行号和实现论断仍需按写作当天重新读取本地源码。
- [x] 2026-06-14：继续收尾 `docs/example-regression-map.md` 里的 `qed` family：已把剩余 `2D openPMD / 3D Breit-Wheeler / 3D Quantum Sync / 4x Schwinger` active baseline 全部压到和 umbrella/helper/input 同级的 source-grounded 粒度，完成 `10 active baselines` 的 baseline-level closure。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 里的 `qed` active baseline：已把 `test_2d_qed_breit_wheeler.json` 再压成和 umbrella/helper/input 对称的粒度，明确写清它当前是 `same-final-plotfile particle-contract main consumer + additive checksum sibling`，并把四组 `p1..p4 -> ele*/pos*` producer 与 core analysis 的六层粒子合同重新闭合。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 里的 `qed` active baseline：已把 `test_2d_qed_quantum_sync.json` 再压成和 umbrella/helper/input 对称的粒度，明确写清它当前是 `same-final-plotfile photon-product main consumer + additive checksum sibling`，并把 producer/consumer 都钉回四组 `p1..p4 -> qsp_1..qsp_4` 的 source-product 合同。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 里的 `plasma_mirror` active baseline：已把 `test_2d_plasma_mirror.json` 再压成和 umbrella/helper/input 对称的粒度，明确写清它当前是 two-frame Full-plotfile smoke branch，但自动 regression 只消费最终 `diag1000020` 的 checksum-only 路径。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 里的 `virtual_photons` active baseline：已把 `test_3d_virtual_photons.json` 再压成和 umbrella/helper/input 对称的粒度，明确写清它当前是 `same-directory openPMD particle-only main consumer + additive checksum sibling`，并把主 analysis 收窄成单束 `GenerateVirtualPhotons` 的 `yield + spectrum + position` 三联断言。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 里的 `beam_beam_collision` active baseline：已把 `test_3d_beam_beam_collision.json` 再压成和 umbrella/helper/input 对称的粒度，明确写清它当前是 `single active slow baseline + same-directory openPMD checksum-only main surface`，而 `ColliderRelevant_beam1_beam2 + ParticleNumber` 只继续保留为供 `plot_reduced.py` 消费的 reduced plot-only side channels。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 的 `plasma_acceleration` family glue：已新增 `plasma_acceleration umbrella summary`，把这组 `8` 条 active PWFA baseline 从分散的 helper/input/baseline 描述重新收成 summary 层可直接读取的 `checksum-only only-automatic-consumer chain + 1 + 1 + 2 + 1 + 1 + 1 + 1 split`，并额外挂回 `2D native`、`3D native` 与 `3D PICMI` 三组 sibling 对照。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 里的 `plasma_acceleration` active baseline：已把 `test_3d_plasma_acceleration_picmi.json` 从偏旧的最小 PICMI 摘要改成更显式的 `3D non-boosted PICMI PWFA smoke sibling` 口径，明确写清它当前虽然仍是 `analysis=OFF`，但 producer 侧会原地 materialize moving-window `Cartesian3DGrid + beam/plasma UniformDistribution + diag1 field/particle` 这条 `10-step` in-process PICMI 主线，而自动消费者则只稳定落在最终 `diag1000010` checksum 主面。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 里的 `plasma_acceleration` active baseline：已把 `test_3d_plasma_acceleration_boosted_hybrid.json` 从偏旧的 hybrid 变体摘要改成更显式的 `3D boosted-hybrid PWFA smoke sibling` 口径，明确写清它当前虽然仍是 `analysis=OFF`，但 producer 侧完整继承 `inputs_base_3d` 的 boosted application scaffold，并只额外切出 `hybrid + no-current-centering + 25-step` 三联 smoke 分叉，而自动消费者则只稳定落在最终 `diag1000025` checksum 主面。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 里的 `plasma_acceleration` active baseline：已把 `test_3d_plasma_acceleration_boosted.json` 从偏旧的短程 checksum 摘要改成更显式的 `3D boosted PWFA smoke sibling` 口径，明确写清它当前虽然仍是 `analysis=OFF`，但 producer 侧完整继承 `inputs_base_3d` 的 boosted application scaffold，而自动消费者则只稳定落在最终 `diag1000005` checksum 主面，并与相邻 `boosted_hybrid` sibling 形成“只缩步数 vs 再切 hybrid/no-current-centering”的对照。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 里的 `capacitive_discharge` active baseline：已把 `test_2d_background_mcc.json` 从旧式“checksum 基线”起手改成更显式的 native 2D discharge+checksum 口径，明确写清它当前虽然仍是 `analysis=OFF`，但 producer 侧稳定 materialize `time-varying electrode potential + dual background_mcc + rho_electrons/rho_he_ions` 这条 native runtime，而 `diag1000050` 则继续承担唯一自动 checksum 主面。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 里的 `free_electron_laser` active baseline：已把 `test_1d_fel.json` 从旧式“checksum 基线”起手改成更显式的 dual-openPMD main-consumer 口径，明确写清它当前由 `diag_labframe` 主面和 `diag_boostedframe` side channel 共同托起 gain-length / wavelength 主链，而 checksum 仍只钉在 `diag_labframe`。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 里的 `ion_beam_extraction` active baseline：已把 `test_3d_ion_beam_extraction.json` 从旧式“checksum 基线”起手改成更显式的 same-directory main-consumer 口径，明确写清它当前是 `diag1` openPMD 主面上的 `phi/eb_covered/Dplus` 尾束能量主链，分离出来的 `bound` 只保留为未被自动消费的 side surface。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 里的 `nuclear_fusion umbrella summary`：已把 whole family 再收成更显式的 family-level glue，明确写清它当前围绕 `diag1000001/diag1000010` 双 checksum surface 展开，并由 `p-B11`、普通两产物 `D-D/D-T` 和 `D-D intraspecies` 三条 main-consumer chains 共同托起。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 里的 `nuclear_fusion` intraspecies producer 行：已把 `inputs_test_3d_deuterium_deuterium_fusion_intraspecies` 补成 source-grounded 强描述，明确写清它当前是 `20 keV`、`1e26 m^-3`、`1e4 ppc` 的单 species 热 `D-D` 多步 collision producer，并把 `dd_collision.event_multiplier = 1e10`、`reduced_diags/particle_number.txt` 主链和分离出来的 `diag1000010` checksum side surface 统一挂回同一条 intraspecies producer 合同。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 里的 `nuclear_fusion` intraspecies consumer 行：已把 `analysis_deuterium_deuterium_3d_intraspecies.py` 补成 source-grounded 强描述，明确写清它当前是只消费 `reduced_diags/particle_number.txt` 的热反应率主链，并把 `neutron` 产额差分、Higginson 2019 的 reactivity 公式、Bosch-Hale 理论值和分离出来的 `diag1000010` checksum side surface 统一挂回同一条 intraspecies consumer 合同。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 里的 `nuclear_fusion` producer 行：已把 `inputs_test_2d_proton_boron_fusion` 补成 source-grounded 强描述，明确写清它当前是单步 `2D` 五子场景 `p-B11` collision producer，并把 center-of-mass 扫能、mixed-target beam-on-target、`44 keV` 热率场景、全耗尽、欠产额分支与 `PBF1..PBF5 + diag1000001(rho)` 统一挂回同一条 producer 合同。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 里的 `nuclear_fusion` producer 行：已把 `inputs_test_3d_deuterium_deuterium_fusion` 补成 source-grounded 强描述，明确写清它当前是单步 `3D` 单子场景 `D-D` collision producer，并把 counter-streaming center-of-mass 扫能切片、`DDNHeF1` 和最终 `diag1000001(rho)` 统一挂回同一条 producer 合同。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 里的 `nuclear_fusion` shared analysis：已把 `analysis_two_product_fusion.py` 补成 source-grounded 强描述，明确写清它当前是同时服务 `D-D/D-T + 3D/RZ` sibling 的 dual-snapshot multi-contract main consumer，并把 generic 守恒合同、center-of-mass / beam-on-target 分叉，以及末尾 `rho` 守恒 side contract 统一挂回同一条 consumer 主链。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 里的 `nuclear_fusion` producer 行：已把 `inputs_test_3d_deuterium_tritium_fusion` 补成 source-grounded 强描述，明确写清它当前是单步 `3D` 两子场景 `D-T` collision producer，并把 center-of-mass 扫能切片、mixed-target beam-on-target、`DTF1/DTF2` 和最终 `diag1000001(rho)` 统一挂回同一条 producer 合同。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 里的 `nuclear_fusion` producer 行：已把 `inputs_test_3d_proton_boron_fusion` 补成 source-grounded 强描述，明确写清它当前是单步 `3D` 五子场景 `p-B11` collision producer，并把 `PBF1..PBF5`、mixed-density beam-on-target、44 keV 热率场景、全耗尽与欠产额分支统一挂回同一条 producer 合同。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 里的 `nuclear_fusion` shared analysis：已把 `analysis_proton_boron_fusion.py` 从宽泛摘要抬到 source-grounded 强描述，明确写清它当前是同时服务 `2D/3D p-B11` sibling 的 dual-snapshot multi-contract main consumer，并按五子场景分叉到 alpha yield、初始能谱、热率拟合、全耗尽与欠产额 gate。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 里的 `nuclear_fusion` 邻域：已把 `test_3d_proton_boron_fusion.json` 从旧式 checksum 摘要抬到和 `2D` sibling 同级的 source-grounded 强描述，明确写清它当前是 `3D` 五子场景 `p-B11` producer、共享 `analysis_proton_boron_fusion.py` multi-contract main consumer，以及 `diag1000001` additive checksum sibling。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 里的 `capacitive_discharge umbrella summary`：已把 whole family 收成 `4 active baselines + shared diag1000050 checksum surface + 1/1/2 mixed split`，明确拆开两条 1D Turner fixed-file main-consumer branch，以及两条共享 `diag1000050` 的 2D checksum-only sibling。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 里的 `electrostatic_sphere family summary`：已把共享 `diag1000030` 的 `RZ` duo 也收成更显式的高层 glue，明确拆开默认 `RZ + phi` 的 `Er/Ez + Ek/Ep` 主链，以及 `uniform_weighting` 只通过更均匀径向装填与 `1.2%` 能量账本容差形成的 sibling。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 里的 `electrostatic_sphere family summary`：已把共享 `diag1000030` 的 3D trio 再收成更显式的高层 glue，明确拆开默认 `relativistic` field-only、`lab_frame` 的 `field-L2 + Ek/Ep` 双主链，以及 `collocated` field-only 这三条 sibling。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 里的 `electrostatic_sphere` 邻域：已把 `test_3d_electrostatic_sphere_rel_nodal.json` 再压实一层，明确写清它当前和普通 3D 基线、`lab_frame` 共用 `diag1000030`，但只因 `warpx.grid_type = collocated` 切到 collocated field-only 主链，仍不会触发 `phi` 能量账本。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 里的 `electrostatic_sphere` 邻域：已把 `test_3d_electrostatic_sphere.json` 再压实一层，明确写清它当前是与 `lab_frame`/`rel_nodal` 共用 `diag1000030` 的默认 field-only 主链，并且不会触发 `phi` 能量账本。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 里的 `electrostatic_sphere` 邻域：已把 `test_3d_electrostatic_sphere_lab_frame.json` 再压实一层，明确写清它当前和普通 3D 基线共用 `diag1000030`，但会因 `diag2.electron.variables` 显式带 `phi` 而稳定进入 `field-L2 + Ek/Ep` 双主链。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 里的 `electrostatic_sphere` 邻域：已把 `test_3d_electrostatic_sphere_lab_frame_mr_emass_10.json` 再压实一层，明确写清它当前是 whole family 里单独落到 `diag1000002` 的 `same-final-plotfile` 分支，并且只命中放宽容差后的 field-only 主链，不会触发 `phi` 能量账本。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 里的 `single_particle` active baseline 缺口：已把 `test_1d_synchronize_velocity.json` 单独补成独立条目，明确写清它当前是 `8-step` uniform-`Ez` producer 上只消费 `diag1000005` 的 step-5 diagnostics-time synchronized-`u_z` scalar branch，并且没有 checksum sibling。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 里的 `single_particle` 邻域：已把 family summary / `analysis_synchronize_velocity.py` / `inputs_test_1d_synchronize_velocity` 再压实一层，明确写清 `test_1d_synchronize_velocity` 当前不是 final-state gate，而是 `max_step = 8` producer 上只消费 `diag1000005` 的 step-5 diagnostics-time synchronized-`u_z` scalar contract。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 里的 `space_charge_initialization` 邻域：已把 umbrella / shared `analysis.py` / `test_3d_space_charge_initialization.json` 再压实一层，明确写清当前 `Comparison.png` 只可视化 `Ex/Ey`，而 `Ez` 在 `3D` 路径上真实属于 assert-only third component，并继续与 same-final-plotfile fields-only checksum 结构闭合。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 里的 `repelling_particles` 邻域：已把 umbrella / `analysis.py` / `test_2d_repelling_particles.json` 再压实一层，明确写清当前 `diag1000200` 对主 analysis 只充当序列种子，真正被强消费的是 `diag1000020..diag1000200` 这 `10` 帧 `20`-step cadence `beta(d)` 时序，而 checksum 仍只钉最终 `diag1000200`。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 里的 `relativistic_space_charge_initialization` 邻域：已把 umbrella / `analysis_default_regression.py` / `inputs_test_3d_relativistic_space_charge_initialization` / `test_3d_relativistic_space_charge_initialization.json` 四处口径重新压平，明确写清当前 whole family 真实命中的是同一张 `diag1000001` 上的 `Ex` analytic strong gate 加 fields-only checksum，而 `By` 仅保留为 `Comparison.png` 的 side plot。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 里的 `boosted_diags` active baseline：已把 `test_3d_laser_acceleration_btd.json` 再压实一层，写清当前 `diag1` 负责 `plotfile` BTD writer 与 `diag1000003` side surface，`diag2` 负责 `openPMD` BTD writer 与 `beam.random_fraction = 0.5` 子采样合同，而 checksum 只钉在前者。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 里的 `radiation_reaction` input-level 行：已把 `inputs_test_3d_radiation_reaction` 明确补成 `5` 条 `SingleParticle` lepton sibling 的 constant-`B` classical-RR producer，写清当前 runtime split 真正落在 parallel/perpendicular/charge-sign 的 `single_particle_u` 分叉上，而末态只通过同一张 `diag1000064` 粒子动量面进入主 analysis。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 里的 `spacecraft_charging` umbrella summary：已把这条 family-level glue 明确补成 `WarpX_EB` gated 的单 active baseline，写清当前除 `diag1` same-directory openPMD main surface 外，还外挂 `diag2` end-only scraped-particle side surface，并通过 `ParticleBoundaryBufferWrapper()` 在 runtime 内做 EB potential correction。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 里的 `thomson_parabola_spectrometer` active baseline：已把 `test_3d_thomson_parabola_spectrometer.json` 明确补成 separated-surface 结构，写清当前 producer 是 `algo.maxwell_solver = none` 的 prescribed-field TPS workflow，主 `analysis.py` 只消费 `diag0 + screen/particles_at_zhi` 两条 openPMD 粒子面去重建 `detect.png`，而 `diag1` 仍只承担分离出来的 checksum side surface。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 里的 `plasma_mirror` active baseline：已把 `test_2d_plasma_mirror.json` 明确补成 `single active baseline + final diag1000020 checksum-only consumer chain`，写清当前 producer 是独立 native 2D laser-solid scaffold、`diag1000010` 只是未被自动接住的中间帧，而 WarpX 自带 README 仍把 PICMI/Analyze/Visualize 都留在 `TODO`。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 里的 `beam_beam_collision` field side helper：已把 `plot_fields.py` 明确补成只消费同目录 `diag1` openPMD full surface的 dual-slice four-panel time-series plotter，并写清它与 `plot_reduced.py` 一起构成 umbrella 下的 plot-only helper pair。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 里的 `beam_beam_collision` reduced side helper：已把 `plot_reduced.py` 明确补成只消费 `ColliderRelevant_beam1_beam2.txt + ParticleNumber.txt` 的 post-processor side helper，写清它当前会重建 centered collision-time 坐标上的 photon/NLBW normalized yield curves，并与 `plot_fields.py` 一起构成 umbrella 下的 plot-only helper pair。
- [x] 2026-05-31：继续回补 `docs/parameter-map.md` 里的 PSATD 高层 family summary：已把 `psatd.current_correction` 抬成三支 runtime family 的总汇入口，明确写清当前这整簇更高层地分成 `periodic_single_box_fft + current_correction` 的 continuity-correction family、`gamma_boost -> use_default_v_* -> v_comoving/v_galilean` 的 velocity handoff family，以及 `JRhom + solution_type + do_time_averaging` 的 residual regular-domain/runtime-subcycling family。
- [x] 2026-05-31：继续回补 `docs/parameter-map.md` 里的 PSATD runtime family split：已把 `psatd.JRhom` 明确补成与 `current_correction + periodic_single_box_fft` 不同的 residual regular-domain/runtime-subcycling family root，写清它当前会退出 `current_correction` 与 `Galilean/comoving` 接管后，再进入 `solution_type + do_time_averaging` 这套 residual 分派。
- [x] 2026-05-31：继续回补 `docs/parameter-map.md` 里的 PSATD residual regular-domain 分派桥：已把 `psatd.solution_type` 显式挂回 `Comoving-first, Galilean-second` handoff 之后的 residual 分支，明确写清它当前只在前两条优先路径都未命中后，才继续在 `PsatdAlgorithmJRhomFirstOrder/SecondOrder` 间做一二阶分派。
- [x] 2026-05-31：继续回补 `docs/parameter-map.md` 里的 PSATD averaged-field family bridge：已把 `psatd.do_time_averaging` 显式挂回 `Comoving-first, Galilean-second` 的 solver handoff，明确写清它当前不会在 `v_comoving -> PsatdAlgorithmComoving` 路径 materialize，而是稳定落在 `JRhomSecondOrder` 和 `v_galilean` 接管后的 `Galilean` 路径上。
- [x] 2026-05-31：继续回补 `docs/parameter-map.md` 里的 PSATD `Galilean/comoving` family-level 总述：已把 `warpx.gamma_boost` 补成这组默认速度链的上游根，明确写清它当前先提供唯一 boost 标量，随后由 `psatd.use_default_v_galilean / use_default_v_comoving` 物化 shared default-selector pair，再由 `psatd.v_comoving / v_galilean` 把速度值接到 `Comoving-first, Galilean-second` 的 solver-family priority。
- [x] 2026-05-31：继续回补 `docs/parameter-map.md` 里的 PSATD `Galilean/comoving` priority bridge：已把 `psatd.v_comoving` 补成 shared boosted-frame 默认速度对的下游 consumer，并明确写清它当前在常规域里优先接管 `PsatdAlgorithmComoving`，从而把后续 `psatd.v_galilean` 稳定压到只在 `v_comoving` 未命中时才生效的第二优先级。
- [x] 2026-05-31：继续回补 `docs/parameter-map.md` 里的 PSATD `Galilean/comoving` 默认速度桥：已把 `psatd.use_default_v_galilean` 与 `psatd.use_default_v_comoving` 补成 shared boosted-frame default-selector pair，明确写清它们当前共同受 `warpx.gamma_boost` gating、共同绕过手动 `v_*` parser，而真正的 solver-family 分派仍落在后续 `v_comoving / v_galilean` 非零检查；同时补清 `psatd.v_galilean` 只会在 `v_comoving` 未命中时才继续接管 Galilean 分支。
- [x] 2026-05-31：继续回补 `docs/parameter-map.md` 里的 `langmuir` PSATD 双 pivot 对照：已把 `psatd.current_correction` 与 `psatd.update_with_rho` 这对相邻输入改成更显式的并排读法，明确写清前者是 continuity-side pivot，负责是否在 continuity 假设下额外修正 `J`；后者是 field-update-side pivot，负责是否保留 `rho_old/rho_new` 并走 `E(J,ρ)` 公式，从而把这一簇 companion bridge 再收紧一层。
- [x] 2026-05-31：继续回补 `docs/parameter-map.md` 里的 `langmuir` PSATD field-update bridge：已把 `psatd.update_with_rho` 这条输入补成更显式的 source-grounded cluster pivot，明确写清它当前一头决定是否真的走 `E(J,ρ)` 与 `rho_old/rho_new` 状态面，另一头又被 `solution_type / do_time_averaging / JRhom / comoving` 这支 runtime family 共同推回到 `1`，从而与 `psatd.current_correction` 形成互补桥接。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 里的 `langmuir` PSATD companion cluster 重复项：已删掉 `psatd.periodic_single_box_fft` 那条旧版弱描述，只保留已补强的 authoritative 条目，避免 single-box front-door 这条 family bridge 在阅读时出现双版本并排。
- [x] 2026-05-31：继续回补 `docs/parameter-map.md` 里的 `langmuir` PSATD family bridge：已把 `psatd.current_correction` 这条输入补成更显式的 source-grounded cluster pivot，明确写清它当前向前连接 `periodic_single_box_fft / nox-noy-noz` 的 single-box infinite-order 分叉，向后再与 `JRhom / solution_type / do_time_averaging` 形成互斥或 companion 关系，把 `current_correction` sibling 与 `JRhom/time-averaged` sibling 稳定拆成两条 runtime family。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 里的 `langmuir umbrella summary`：已把这条 family glue 再补成更对称的 source-grounded 总述，明确写清 whole family 当前围绕 `24/16` 双末态 checksum surface 展开，并由 `1D/2D/3D/RZ/radial` 五组 shared main consumer、横切的 `analysis_utils.py` charge-conservation side helper、`test_rz_langmuir_multi_picmi` 的 in-process assert，以及两条 checksum-only PICMI sibling 共同托起。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 里的 `langmuir` 1D shared main consumer：已把 `analysis_1d.py` 这条主 analysis 补成 source-grounded 强描述，明确写清它当前只服务 `test_1d_langmuir_multi` 这一条 active baseline、稳定共吃 `diags/diag1000080` 同一张末态 plotfile，并把 `Ez` 解析场主 gate 与默认 `esirkepov` 路径下 `1e-11` 的 same-surface `divE-rho/epsilon_0` 守恒 side gate 一起钉进同一条 shared consumer 链。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 里的 `langmuir` RZ shared main consumer：已把 `analysis_rz.py` 这条主 analysis 补成 source-grounded 强描述，明确写清它当前横切整组 `RZ` active baseline、稳定共吃 `diags/diag1000080` 同一张末态 plotfile，并把 analytic `Er/Ez` 主 gate、`diag_parser/uniform/random_filter000080` 三套粒子筛选 side consumer，以及 `test_rz_langmuir_multi_psatd*` 路径独有的 `skip_component = particle_momentum_x` 分叉一起钉进同一条 shared consumer 链。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 里的 `langmuir` 3D shared main consumer：已把 `analysis_3d.py` 这条主 analysis 补成 source-grounded 强描述，明确写清它当前横切整组 `3D` active baseline、稳定共吃 `diags/diag1000040` 同一张末态 plotfile，并把 selective particle output 合同、`./diags/openpmd` 上 `iteration=40` 的粒子位置场采样，以及 `div_cleaning` sibling 独有的 `diag1000038/39/40` 三帧 side branch 一起钉进同一条 shared consumer 链。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 里的 `langmuir` 2D shared main consumer：已把 `analysis_2d.py` 这条主 analysis 补成 source-grounded 强描述，明确写清它当前横切整组 `2D` active baseline、稳定共吃 `diags/diag1000080` 同一张末态 plotfile，只在 level-0 全域 mesh 上比较 `Ex/Ez` 解析场，并把 `particle_shape_4` 的 `0.07` 容差分叉与共享 `analysis_utils.py` 守恒 side consumer 一起钉死。
- [x] 2026-05-31：继续回补 `docs/example-regression-map.md` 里的 `langmuir` shared helper：已把 `analysis_utils.py` 这条横切脚本补成 source-grounded 强描述，明确写清它当前会先解析 `./warpx_used_inputs`，再按 `esirkepov / psatd.current_correction / vay` 三路 runtime 组合决定是否叠加 same-surface `divE-rho/epsilon_0` 守恒 gate，并把容差稳定切成 `1e-11 / 1e-9 / 1e-3`，同时显式排除 `RZ + esirkepov` 与一般 `PSATD + esirkepov` 路径。
- [x] 2026-05-31：继续回补 `docs/parameter-map.md` 里的 `langmuir` PSATD 上游谱阶输入：已把 `psatd.nox/noy/noz` 这组三方向参数补成 source-grounded 强描述，明确写清它们当前不仅负责 `inf -> -1` 的 infinite-order parser 语义和 `psatd.periodic_single_box_fft` companion gate，还会继续进入 `GuardCellManager`，按 collocated/staggered/Galilean 三路分叉推导 FFT guard-cell 预算。
- [x] 2026-05-31：继续回补 `docs/parameter-map.md` 里的 `langmuir` PSATD companion cluster root：已把 `psatd.JRhom` 这条输入补成更显式的 source-grounded 描述，明确写清它当前不仅负责 `J/rho` 时间依赖字符串与 `m_JRhom_subintervals` 解析，还会继续把 `solution_type / update_with_rho / current_correction / do_time_averaging` 这组 companion 条件、`solver_dt / n_deposit / sub_dt` 子步缩放，以及 `OneStep_JRhom()` 的 averaged-field 路径一起钉在同一条主链上。
- [x] 2026-05-31：继续回补 `docs/parameter-map.md` 里的 `langmuir` PSATD time-averaging companion：已把 `psatd.do_time_averaging` 这条输入补成更强的 source-grounded 描述，明确写清它当前不是孤立小开关，而是 `solution_type=first-order` 禁用、`update_with_rho=1` 强依赖、`JRhom` 推荐 companion、`*_avg` 频谱分量与 `E/Bfield_avg_*` 分配、level-0 `aux` alias，以及 `OneStep_JRhom()` 双倍沉积/average-field 回变换的跨层 gate。
- [x] 2026-05-31：继续回补 `docs/parameter-map.md` 里的 `langmuir` PSATD 解阶数分叉：已把 `psatd.solution_type` 这条输入补成 source-grounded 强描述，明确写清它当前不是泛泛的阶数枚举，而是 `SpectralSolver` 在 `PsatdAlgorithmJRhomFirstOrder` 与 `PsatdAlgorithmJRhomSecondOrder` 之间的 solver-class dispatch gate；其中 `first-order` 还会继续约束 `psatd.do_time_averaging = 0` 与 `warpx.do_dive_cleaning == warpx.do_divb_cleaning`，并且已经能和 `JRhom_LL2` / `QQ1_nodal` 这两条 2D `langmuir` sibling 的 producer split 对齐。
- [x] 2026-05-31：继续回补 `docs/parameter-map.md` 里的 `langmuir` PSATD 邻接参数：已把 `psatd.periodic_single_box_fft` 这条输入补成 source-grounded 强描述，明确写清它当前同时承担 `nox/noy/noz` 无限阶 companion gate、`algo.current_deposition = vay` 反向兼容性边界、PSATD current backward-FFT guard-cell 预算开关，以及 `SpectralFieldData(..., periodic_single_box)` 谱侧 materialization 的 front-door，并把它和 `current_correction` 两条 2D `langmuir` sibling 的 producer split 对齐到同一层级。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Langmuir_multi_2d_psatd_QQ1_nodal.json`：已把这条 active baseline 从旧式“checksum 基线”补成 source-grounded 强描述，明确写清它当前是 `WarpX_FFT`-gated 的 `analysis_2d.py diags/diag1000080 + analysis_default_regression.py --path diags/diag1000080` 主链；producer 侧命中共享 `inputs_base_2d` 骨架上的 `JRhom = LL2 + solution_type = first-order + update_with_rho = 1 + collocated` 窄 overlay，而 shared `analysis_2d.py` 在同一张末态 plotfile 上仍只做 `Ex/Ez` 理论 Langmuir 场 gate；相对地，经 `analysis_utils.py` 调度后，这条 sibling 当前不再命中 `current_correction / vay / esirkepov` 额外守恒检查分支。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Langmuir_multi_2d_psatd_CC2_nodal.json`：已把这条 active baseline 从旧式“checksum 基线”补成 source-grounded 强描述，明确写清它当前是 `WarpX_FFT`-gated 的 `analysis_2d.py diags/diag1000080 + analysis_default_regression.py --path diags/diag1000080` 双消费者 wiring；producer 侧命中共享 `inputs_base_2d` 骨架上的 `current_correction + periodic_single_box_fft + collocated` 窄 overlay，而 main analysis 则在同一张末态 plotfile 上先做 `Ex/Ez` 理论 Langmuir 场 gate，再按 `analysis_utils.py` 命中 `current_correction` 分支对 `rho/divE` 施加 `1e-9` 的 charge-conservation gate。
- [x] 2026-05-31：继续回补 `docs/parameter-map.md` 里的 accelerator-lattice line-wrapper 参数：已把 `<element_name>.elements` 这条输入再补成 source-grounded 强描述，明确写清它当前是 `type = line` 节点的 recursive sequence payload，会把该节点直接变成嵌套 root，并沿与顶层 `lattice.elements` 同构的读取/展开/拼接链并入最终 lattice geometry。
- [x] 2026-05-31：继续回补 `docs/parameter-map.md` 里的 accelerator-lattice 顺序键：已把 `lattice.reverse` 这条输入再补成 source-grounded 强描述，明确写清它当前是 `sequence-orientation gate`，会先在 front-end 侧翻转 element/line 的展开顺序，再通过共享 `z_location` 继续改写整条 lattice 的 `[zs,ze]` 几何落点，而不是只做字面列表倒序。
- [x] 2026-05-31：继续回补 `docs/parameter-map.md` 里的 accelerator-lattice 分派键：已把 `<element_name>.type` 这条输入再补成 source-grounded 强描述，明确写清它当前是 `drift / quad / plasmalens / line` 四路 element-class dispatch gate，其中 `drift` 只 materialize 共享 `[zs,ze]` 区间、`quad/plasmalens` 才继续进入 hard-edged 场梯度与粒子 gather-time consumer，而 `line` 则只是递归 front-end wrapper。
- [x] 2026-05-31：继续回补 `docs/parameter-map.md` 里的 accelerator-lattice element-local 参数：已把 `<element_name>.ds`、`<element_name>.dEdx` 与 `<element_name>.dBdx` 这三条输入再补成 source-grounded 强描述，明确写清 `ds` 当前承担 shared `[zs,ze]` axial-extent contract，而 `dEdx/dBdx` 则共同构成 `hard-edged plasma lens` 的 `E/B` 双梯度 sibling，并直接闭合到 `hard_edged_fraction + LatticeElementFinder + GetExternalEBField` 这条粒子 runtime consumer 链。
- [x] 2026-05-31：继续回补 `docs/parameter-map.md` 与 `plasma_lens` hard-edged sibling 之间的桥接：已把 `lattice.elements` 这条输入再补成 source-grounded 强描述，明确写清它当前是 `accelerator-lattice` 的 front-end root gate，会把顶层/递归 element 序列物化成共享 `z_location` 的 hard-edged lattice，再接到 `LatticeElementFinder + GetExternalEBField` 的粒子 runtime consumer，并把 `test_3d_plasma_lens_hard_edged` 与 native `repeated_plasma_lens` 两条前端链的对照边界一起钉死。
- [x] 2026-05-31：开始回补 `docs/parameter-map.md` 与刚压平的 `plasma_lens` family 之间的桥接：已把 `particles.E/B_ext_particle_init_style` 这条输入再补成 source-grounded 强描述，明确写清它当前分成 `parser / repeated_plasma_lens / read_from_file aux-field` 三路 particle external-field 主链，并把 `native/python/boosted/short` 几条 `plasma_lens` sibling 命中 `repeated_plasma_lens`、而 `hard-edged / PICMI` 两条 sibling 分别转向 `lattice.elements / PICMI PlasmaLens` 的 family boundary 一起钉死。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/photon_pusher/analysis_default_regression.py`：已把这条 shared helper 再补成 source-grounded 强描述，明确写清它当前只服务 `test_3d_photon_pusher` 这一条 active baseline、与 shared `analysis.py` 共吃 `diag1000050` 同一张 final surface，并且在这组 wiring 上真实命中的始终只是 `yt.load(plotfile)` 这条收缩 checksum 路径。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/photon_pusher/analysis.py`：已把这条 shared main consumer 再补成 source-grounded 强描述，明确写清它当前固定命中 `diag1000050` 这张 photon-only final surface，稳定执行 `16` 个单光子 species 的直线传播/动量守恒 gate，并且脚本自身还保留一条同源 native `inputs` regenerate contract。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `photon_pusher umbrella summary`：已把这条 family glue 再补成 source-grounded 强描述，明确写清它当前不是松散的单基线说明，而是 `inputs_test_3d_photon_pusher -> analysis.py -> analysis_default_regression.py` 围绕同一张 `diag1000050` photon-only final surface 构成的三节点闭环。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `plasma_lens umbrella summary`：已把这条 family glue 再补成 source-grounded 强描述，明确写清 whole family 的 `6` 条 active baseline 统一共吃 `diag1000084` 这张 final surface，shared `analysis.py` 稳定只消费其中的 final particle contract，而 `native/python/picmi/boosted/lattice/short` 六条 sibling 则各自只切前端或 runtime overlay。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_plasma_lens_python.json`：已把这条 Python sibling 从旧式“pywarpx plasma-lens checksum 基线”再补成 source-grounded 强描述，明确写清它当前既不走 native 输入卡，也不走 PICMI object graph，而是直接拼装 `pywarpx` 参数树并原地 `warpx.init()/step()`，同时保持 `diag1000084` 为 particle-only final surface，shared `analysis.py` 继续沿用默认 `2% / 0.2%` gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_plasma_lens_picmi.json`：已把这条 PICMI sibling 从旧式“PICMI plasma-lens checksum 基线”再补成 source-grounded 强描述，明确写清它当前是在 same final surface 上把 native producer 重组为 `Cartesian3DGrid + dual ParticleListDistribution + PlasmaLens + same-name field/particle diagnostics` 的 PICMI front-end，而 shared `analysis.py` 仍只消费 final particle contract，并继续沿用默认 `2% / 0.2%` gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_plasma_lens_hard_edged.json`：已把这条 hard-edged sibling 从旧式“accelerator-lattice plasma lens checksum 基线”再补成 source-grounded 强描述，明确写清它当前是在主线 repeated-plasma-lens producer 上只把 external-field 前端替换成 `lattice.elements`，shared `analysis.py` 则先把 lattice 翻译回同构 lens-chain 语义，再继续沿用默认 `2% / 0.2%` gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_plasma_lens_boosted.json`：已把这条 boosted sibling 从旧式“boosted-frame plasma-lens checksum 基线”再补成 source-grounded 强描述，明确写清它当前是在主线 repeated-plasma-lens producer 上只切 `gamma_boost / boost_direction / boosted z-domain` 的窄 overlay，shared `analysis.py` 则先做 `z` 反变换再执行同一条 analytic lens-chain consumer，并继续沿用默认 `2% / 0.2%` gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_plasma_lens_short.json`：已把这条 short-lens sibling 从旧式“短透镜 checksum 基线”再补成 source-grounded 强描述，明确写清它当前是在主线 producer scaffold 上只切 `lens lengths/strengths_E` 的 residence-correction 参数分叉，虽然逐步落盘 `diag1.intervals = 1`，但 shared `analysis.py` 与 checksum 仍只消费末态 `diag1000084`，并显式命中放宽到 `0.023 / 0.003` 的 short-lens 容差 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/plasma_lens/analysis.py`：已把这条 shared main consumer 从宽泛“解析透镜串联强分析”再补成 source-grounded family-level 强描述，明确写清它当前统一服务 `6` 条 active regression、稳定共吃 `diag1000084` 这张 particle-only final surface，并把 `native/PICMI/lattice/boosted/short-lens` 前端与 runtime 分叉一并收进 shared final-frame analytic lens-chain consumer。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/plasma_lens/analysis_default_regression.py`：已把这条 shared checksum helper 再补成 source-grounded family-level 强描述，明确写清它当前统一服务 `6` 条 active regression、稳定共吃 `diag1000084` 这张 final plotfile surface，并且在这组 family wiring 上真实命中的始终只是 `yt.load(plotfile) + same-final-plotfile additive checksum sibling` 这条收缩 runtime path。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `plasma_lens umbrella summary`：已把这条 family-level glue 再补成 source-grounded 强描述，明确写清它当前统一覆盖 `6` 条 active regression、稳定共吃 `diag1000084` 这张 particle-only final surface，由 shared `analysis.py` 统一执行 analytic lens-chain main consumer，并把 whole family 的前端/runtime 分叉压成 `native/python/picmi/lattice/boosted/short-lens` 的 `1/1/1/1/1/1` split。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/flux_injection/analysis_flux_injection_rz.py`：已把这条 shared main consumer 从宽泛“RZ 半径带分析脚本”再补成 source-grounded family-aware 强描述，明确写清它当前固定服务 `test_rz_flux_injection` 这条 active RZ standard branch、稳定命中 `diag1000120` 这张 final surface，并把 pure-azimuthal continuous injection + uniform `Bz` producer 收缩成只消费 `r/w` 的 total-weight-and-radius-band main consumer，再外叠 same-final-plotfile additive checksum sibling。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/flux_injection/analysis_flux_injection_3d.py`：已把这条 shared main consumer 从宽泛“3D 分布分析脚本”再补成 source-grounded family-aware 强描述，明确写清它当前固定服务 `test_3d_flux_injection` 这条 active 3D standard branch、稳定命中 `diag1000002` 这张 particle-only final surface，并把 shared producer 里的两种 rejection-method、三条法向轴和正负漂移分支都串进逐 species 的 histogram main consumer，再外叠 same-final-plotfile additive checksum sibling。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/flux_injection/analysis_flux_injection_from_eb.py`：已把这条 shared main consumer 从宽泛“EB 发射分析脚本”再补成 source-grounded family-level 强描述，明确写清它当前统一服务 `test_2d/3d/rz_flux_injection_from_eb` 三条 active regression、稳定命中 shared `diag1000020` particle-only final surface，并按 `warpx_used_inputs` 分流到 `2D/3D/RZ` 三个几何重建分支，再外叠 same-final-plotfile additive checksum sibling。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_2d_flux_injection_from_eb.json`：已把这条 active baseline 从旧式 `checksum 基线` 口径再补成 source-grounded 强描述，明确写清它当前是 `analysis_flux_injection_from_eb.py diags/diag1000020 + analysis_default_regression.py --path diags/diag1000020` 的 same-final-plotfile 双链结构；producer 会 materialize `shared sphere-EB surface emission + finite time window + 2D periodic cylinder-EB overlay + particle-only final surface`，而主 analysis 则只固定消费同一张末态 plotfile 上的 `2D geometry reconstruction`、`Ntot`、`EB 外侧几何约束` 和 `u_n/u_perp/u_perp2` 直方图 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `flux_injection umbrella summary`：已把这条 family-level glue 再补成 source-grounded 强描述，明确写清它当前统一覆盖 `5` 条 active regression，稳定落成 `diag1000002 / diag1000120 / diag1000020` 的 `1/1/3` final-surface split、`3D standard / RZ standard / from-EB` 的 `1/1/3` main-consumer split，以及 shared `analysis_default_regression.py` 在这组 family wiring 上真实命中的始终只是 `yt.load(plotfile) + additive checksum sibling` 这条收缩路径。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/flux_injection/analysis_default_regression.py`：已把这条 shared helper 从宽泛“通用 checksum helper”再补成 source-grounded family-level 强描述，明确写清它当前统一服务 `5` 条 active regression、落成 `diag1000002 / diag1000120 / diag1000020` 的 `1/1/3` final-surface split，并且在当前 family 里真实命中的始终只是 `yt.load(plotfile) + additive checksum sibling` 这条收缩 runtime path。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_rz_flux_injection_from_eb.json`：已把这条 active baseline 从旧式 `checksum 基线` 口径再补成 source-grounded 强描述，明确写清它当前是 `analysis_flux_injection_from_eb.py diags/diag1000020 + analysis_default_regression.py --path diags/diag1000020` 的 same-final-plotfile 双链结构；producer 会 materialize `shared sphere-EB surface emission + finite time window + RZ overlay + higher PPC + particle-only final surface`，而主 analysis 则只固定消费同一张末态 plotfile 上的 `RZ-to-3D geometry reconstruction`、`Ntot`、`EB 外侧几何约束` 和 `u_n/u_perp/u_perp2` 直方图 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_flux_injection_from_eb.json`：已把这条 active baseline 从旧式 `checksum 基线` 口径再补成 source-grounded 强描述，明确写清它当前是 `analysis_flux_injection_from_eb.py diags/diag1000020 + analysis_default_regression.py --path diags/diag1000020` 的 same-final-plotfile 双链结构；producer 会 materialize `shared sphere-EB surface emission + finite time window + 3D overlay + particle-only final surface`，而主 analysis 则只固定消费同一张末态 plotfile 上的 `Ntot`、`EB 外侧几何约束` 和 `u_n/u_perp/u_perp2` 直方图三段 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_rz_flux_injection.json`：已把这条 active baseline 从旧式 `checksum 基线` 口径再补成 source-grounded 强描述，明确写清它当前是 `analysis_flux_injection_rz.py diags/diag1000120 + analysis_default_regression.py --path diags/diag1000120` 的 same-final-plotfile 双链结构；producer 会 materialize `120-step + RZ + single-electron azimuthal NFluxPerCell + uniform Bz` 骨架，而主 analysis 则只固定消费同一张末态 plotfile 上的 `w.sum()` 与固定半径带 `1.48 <= r <= 1.92` 双 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_flux_injection.json`：已把这条 active baseline 从旧式 `checksum 基线` 口径再补成 source-grounded 强描述，明确写清它当前是 `analysis_flux_injection_3d.py diags/diag1000002 + analysis_default_regression.py --path diags/diag1000002` 的 same-final-plotfile 双链结构；producer 会 materialize `2-step + 16^3 + Maxwell=none + periodic^3 + four-species NFluxPerCell` 骨架，而主 analysis 则只固定消费同一张末态 plotfile 上四个 species 的逐分量 `Gaussian/Gaussian-flux` histogram 并施加 `np.allclose` gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_particles_in_pml_mr.json`：已把这条 active baseline 从旧式 `checksum 基线` 口径再补成 source-grounded 强描述，明确写清它当前是 `analysis_particles_in_pml.py diags/diag1000200 + analysis_default_regression.py --path diags/diag1000200` 的 same-final-plotfile 双链结构，并额外带 `slow` 标签；producer 会 materialize `200-step + level-1 refined cube + full PML + CKC/Vay + ±x 对向单粒子` 骨架，而主 analysis 则只固定消费同一张末态 plotfile 上 finest-level 全域 `Ex/Ey/Ez` 并要求 `max_Efield < 110`。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_particles_in_pml.json`：已把这条 active baseline 从旧式 `checksum 基线` 口径再补成 source-grounded 强描述，明确写清它当前是 `analysis_particles_in_pml.py diags/diag1000120 + analysis_default_regression.py --path diags/diag1000120` 的 same-final-plotfile 双链结构，producer 会 materialize `120-step + 128x64x64 + full PML + CKC/Vay + ±x 对向单粒子` 骨架，而主 analysis 则只固定消费同一张末态 plotfile 上的全域 `Ex/Ey/Ez` 并要求 `max_Efield < 10`。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_2d_pml_x_galilean.json`：已把这条 active baseline 从旧式宽摘要再补成 source-grounded 强描述，明确写清它当前是 `WarpX_FFT` gate 下 `analysis_pml_psatd.py diags/diag1000300 + analysis_default_regression.py --path diags/diag1000300` 的双链结构，producer 侧在 shared `inputs_base_2d` 上同时覆写 `psatd.v_galilean`、`grid_type = collocated` 与 `do_pml_div{b,e}_cleaning = 1`，而主 analysis 则先在 `diag1000050` 上执行 galilean-branch 的 `energy_start` 一致性 gate，再在 `diag1000300` 上执行最终 reflectivity `< 1e-6` gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_2d_pml_x_psatd.json`：已把这条 active baseline 从旧式宽摘要再补成 source-grounded 强描述，明确写清它当前是 `WarpX_FFT` gate 下 `analysis_pml_psatd.py diags/diag1000300 + analysis_default_regression.py --path diags/diag1000300` 的双链结构，producer 侧在 shared `inputs_base_2d` 上只覆写 plain-PSATD 相关开关，而主 analysis 则先在 `diag1000050` 上执行 `energy_start` 一致性 gate，再在 `diag1000300` 上执行最终 reflectivity `< 1e-6` gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_2d_pml_x_yee.json`：已把这条 active baseline 从旧式宽摘要再补成 source-grounded 强描述，明确写清它当前是 `analysis_pml_yee.py diags/diag1000300 + analysis_default_regression.py --path diags/diag1000300` 的 same-final-plotfile 双链结构，producer 侧本体只覆写 `algo.maxwell_solver = yee`，其余 runtime scaffold 全继承自 shared `inputs_base_2d`，而主 analysis 则只固定消费 `diag1000300` 的六个场分量并对理论 reflectivity 施加 `< 5%` gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_2d_pml_x_ckc.json`：已把这条 active baseline 从旧式宽摘要再补成 source-grounded 强描述，明确写清它当前是 `analysis_pml_ckc.py diags/diag1000300 + analysis_default_regression.py --path diags/diag1000300` 的 same-final-plotfile 双链结构，producer 侧本体只覆写 `algo.maxwell_solver = ckc`，其余 runtime scaffold 全继承自 shared `inputs_base_2d`，而主 analysis 则只固定消费 `diag1000300` 的六个场分量并对理论 reflectivity 施加 `< 5%` gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_particle_pusher.json`：已把这条 active baseline 从旧式 `checksum 基线` 口径再补成 source-grounded 强描述，明确写清它当前是 `analysis.py diags/diag1010000 + analysis_default_regression.py --path diags/diag1010000` 的 same-final-plotfile 双链结构，producer 会 materialize `10000-step + giant periodic box + single positron + force-free Ex/Bz + algo.particle_pusher = higuera` 骨架，而主 analysis 则只读取单个 `particle_position_x` 并要求 `abs(x) < 1e-3`。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_particle_boundaries.json`：已把这条 active baseline 从旧式 `checksum 基线` 口径再补成 source-grounded 强描述，明确写清它当前是 `analysis.py diags/diag1000008 + analysis_default_regression.py --path diags/diag1000008` 的双链结构，producer 会 materialize `8-step + 16^3 + reflecting/absorbing/periodic` 三分支粒子边界骨架，而主 analysis 则在 `diag1000000/diag1000008` 初末态双 plotfile 上重建 relativistic 轨道并分别检查 reflecting / periodic / absorbing 三条边界语义。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_particle_absorption.json`：已把这条 active baseline 从旧式 `checksum 基线` 口径再补成 source-grounded 强描述，明确写清它当前是 `WarpX_EB` gate 下的 `analysis_absorption.py diags/diag1000060 + analysis_default_regression.py --path diags/diag1000060` 双链结构，producer 会 materialize `3D + PEC + cubic EB + forward-electron slab` scaffold，而主 analysis 则只固定消费 `diag1000040/diag1000060` 两张快照并要求电子数精确满足 `612 -> 0`。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_particle_fields_diags.json`：已把这条 active baseline 从旧式 `checksum 基线` 口径再补成 source-grounded 强描述，明确写清它当前是 `analysis_particle_diags.py + analysis_default_regression.py --path diags/diag1000200` 的双链结构，shared producer 会同一步落出 `diag1` plotfile 与 `openpmd_%T.h5` 两套 writer，而主 analysis 则用 handmade cell-centered reconstruction 对两套 diagnostics 逐项施加 `1e-12` 级强断言。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_2d_particle_attr_access_unique_picmi.json`：已把这条 sibling baseline 从旧式 `checksum 基线` 口径再补成 source-grounded 强描述，明确写清它当前不是 checksum-only，而是与普通 `particle_attr_access` 共用同一条脚本内 `real-comp 注册 + before-step 注粒子 + tile 级属性回读 + 手动电流沉积` 主链；`--unique` 名字当前没有流入额外 runtime split，外层只再叠一张独立 `diag1000010` checksum side surface。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_2d_prev_positions_picmi.json`：已把这条 sibling baseline 从旧式 `checksum 基线` 口径再补成 source-grounded 强描述，明确写清它当前不是 checksum-only，而是 `inputs_test_2d_prev_positions_picmi.py` 的脚本内 `warpx_save_previous_position` runtime-attribute index/readback 主链，以及独立 `diag1000010` checksum side surface 的双层结构。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_2d_particle_attr_access_picmi.json`：已把这条 baseline 从旧式 `checksum 基线` 口径再补成 source-grounded 强描述，明确写清它当前不是 checksum-only，而是 `inputs_test_2d_particle_attr_access_picmi.py` 的脚本内 `real-comp 注册 + before-step 注粒子 + tile 级属性回读 + 手动电流沉积` 主链，以及独立 `diag1000010` checksum side surface 的双层结构。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_2d_particle_thermal_boundary.json`：已把这条 baseline 从旧式 `checksum 基线` 口径再补成 source-grounded 强描述，明确写清它当前不是 checksum-only，而是 `inputs_test_2d_particle_thermal_boundary` materialize 的 `2D + pml/pml + thermal particle boundaries + EN/EF reduced ledgers` producer、共享 `analysis.py` 的 `EF/EN` reduced-energy growth/drift 主链，以及独立 `diag1002000` additive checksum side surface 的三层结构。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_particle_scrape_picmi.json`：已把这条 PICMI baseline 从旧式 `checksum 基线` 口径再补成 source-grounded 强描述，明确写清它当前不是 checksum-only，而是 shared `diag1000040 -> diag1000060` 主容器删粒子 consumer、脚本尾部 `ParticleBoundaryBufferWrapper()` 的 `eb` buffer size/step/weight/clear 自断言，以及同一张 `diag1000060` additive checksum sibling 的三层结构。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/particle_boundary_scrape/inputs_test_3d_particle_scrape`：已把这条 native 输入行从一句话摘要再补成 source-grounded producer 描述，明确写清它当前固定 materialize `64 x 64 x 128`、全 `none` 场边界、居中 cubic EB、`uz = 2000` 的前冲电子薄 slab、`save_particles_at_xhi/save_particles_at_eb` 双 buffer surface，以及只落 `diag1000040/diag1000060` 两张关键 snapshot 的 runtime 合同。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/diff_lumi_diag/inputs_test_3d_diff_lumi_diag_leptons`：已把这条普通 lepton 输入分叉从一句话摘要再补成 source-grounded baseline overlay 描述，明确写清它当前通过 `gaussian_beam + q_tot` 接管 shared two-beam scaffold，本身不改写 `diag1000080 + DifferentialLuminosity txt + DifferentialLuminosity2D openPMD` 这组 shared writer surface，也不带 centered fine patch。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/diff_lumi_diag/inputs_test_3d_diff_lumi_diag_leptons_mr`：已把这条 MR 输入分叉从一句话摘要再补成 source-grounded producer overlay 描述，明确写清它当前在 lepton `gaussian_beam + q_tot` 初始化上与普通分叉同构，真正新增的只有 centered `amr.max_level = 1` fine patch，而 shared `diag1000080 + DifferentialLuminosity txt + DifferentialLuminosity2D openPMD` surface 保持不变。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/diff_lumi_diag/inputs_base_3d`：已把这条共享骨架从宽泛“3D 共享骨架”再补成 source-grounded shared producer scaffold，明确写清它当前显式固定 `125 GeV` 双束对撞 runtime、末态 `diag1000080` checksum surface，以及 `DifferentialLuminosity txt + DifferentialLuminosity2D openPMD` 两条主 analysis side channel。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/reduced_diags/inputs_test_3d_reduced_diags` 里 `PX/FP*` side surfaces：已把这组 producer-side coverage 面从名字级摘要再补成 source-grounded 几何/采样描述，明确写清 `PX` 末态账本和 `FP/FP_integrate/FP_line/FP_plane` 四类 probe 的固定坐标、方向、积分方式与分辨率。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/reduced_diags/inputs_test_3d_reduced_diags`：已把这条主干输入行从宽泛“综合 reduced-diagnostics 基准”再补成 source-grounded independent producer 描述，明确写清它当前独立 materialize `3-species periodic compact-observable` runtime，并同一步落出 `EP/NP/EF/PP/PF/MF/PX/MR/FP*/FR*/Edotj` 整组 reduced surfaces 与末态 `diag1000200` full plotfile reference surface。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/reduced_diags/inputs_base_3d`：已把这条共享骨架从宽泛“最小 `LoadBalanceCosts` 骨架”再补成 source-grounded shared producer scaffold，明确写清它当前显式固定 `max_step = 3`、`128 x 32 x 128` periodic Yee 网格、单 `electrons` 冷盒、`algo.load_balance_intervals = 2`、`LBC.intervals = 1` 与 `diag1.intervals = 3`，供 native 三条 overlay 分叉直接复用。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/reduced_diags/inputs_test_3d_reduced_diags_load_balance_costs_{heuristic,timers,timers_picmi,timers_psatd}`：已把这四条输入分叉从一句话摘要再补成 source-grounded producer 描述，明确写清 native `heuristic/timers/legacy-psatd-name` 三条都只是对 `inputs_base_3d` 的极薄 overlay，而 `timers_picmi` 会独立 materialize `Cartesian3DGrid + Yee + single-electron UniformDistribution + LBC/FR/PH + diag1` 这套 PICMI front-end producer。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/reduced_diags/analysis_reduced_diags_load_balance_costs.py`：已把这条共享 helper 从宽泛“强分析”再补成 source-grounded `LBC.txt` consumer contract，明确写清它当前虽然形式上接收 `diag1000003`，但实现上完全旁路 plotfile，只按 header 动态反解每个 box block 的字段宽度，重建按 rank 聚合的累计 cost，并固定对 `i=1/2` 两帧施加 `efficiency_before < efficiency_after` gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/reduced_diags/analysis_reduced_diags_impl.py`：已把这条共享主 helper 从一句“强分析”再补成 source-grounded full-surface/reduced-ledger consumer contract，明确写清它当前会同时消费末态 `diag1000200` full plotfile 与 `EF/EP/PF/PP/MF/MR/NP/FR_Max/FR_Min/FR_Integral/Edotj.txt`，逐项重建 compact observables，并按默认 `1e-12`、single-precision `5e-3`、`field energy = 0.3` 三档容差执行交叉校验。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/implicit/analysis_2d_psatd.py`：已把这条主 helper 从一句“强分析”再补成 source-grounded FFT-gated reduced-energy consumer contract，明确写清它当前只在 `WarpX_FFT` 打开时服务 `test_2d_theta_implicit_strang_psatd`，固定只消费 `field_energy.txt + particle_energy.txt`，并对整段总能量相对漂移施加 `2.4e-14` 的机器精度 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/implicit/analysis_implicit.py`：已把这条主 helper 从一句“强分析”再补成 source-grounded dual-surface consumer contract，明确写清它当前只服务 `test_2d_theta_implicit_symmetry`，同时固定消费 `field_energy.txt + particle_energy.txt` 与末态 `diag1000400`，分别对整段总能量漂移和末态 `rho-\u03b5_0 divE` 的网格 RMS 误差施加 `2e-14` 级 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/implicit/analysis_1d.py`：已把这条主 helper 从一句“强分析”再补成 source-grounded reduced-energy consumer contract，明确写清它当前统一服务 `semi_implicit_picard / theta_implicit_picard` 两条 1D sibling，固定只消费 `field_energy.txt + particle_energy.txt`，并对整段总能量相对漂移施加按分支切换的 `2.5e-5 / 1e-14` gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/implicit/analysis_petsc_matrix.py`：已把这条主 helper 从一句“强分析”再补成 source-grounded reduced-ledger consumer contract，明确写清它当前统一服务 `2D/RCYLINDER/RZ` 三条 PETSc-LU 基线，固定只消费 `diags/reduced_files/newton_solver.txt`，并对累计 `num_steps / total_newton_iters / total_gmres_iters` 施加精确的 `1 Newton + 1 GMRES per step` gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/radiation_reaction/analysis.py`：已把这条主 helper 从一句“3D 强分析”再补成 source-grounded branch-aware consumer contract，明确写清它当前固定只消费 `diag1000064` 末态 plotfile，对 `ele_para0/ele_perp*/pos_perp2` 五个单粒子分支分别执行 `parallel invariance` 或 `Landau-Lifshitz gamma(t)` 解析 gate，并统一施加 `5%` 的逐 case 相对误差约束。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/effective_potential_electrostatic/analysis.py`：已把这条主 helper 从一句“强分析”再补成 source-grounded whole-series consumer contract，明确写清它当前共同消费 `sim_parameters.dpkl + diags/field_diag/`，对整段 openPMD 时间序列做球坐标重采样和角向平均，并把 whole-series 径向电子密度 RMS 误差统一压到 `< 0.07`。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/dive_cleaning/analysis.py`：已把这条主 helper 从一句“2D/3D 强分析”再补成 source-grounded same-final-surface consumer contract，明确写清它当前固定只消费 `diag1000128` 末态 plotfile，按 `2D/3D` 分叉到圆柱或球对称 Gaussian-Coulomb 理论场重建，对 `Ex/Ey/(Ez)` 做逐分量 `allclose` gate，并固定导出 `Comparison.png` side artifact。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/divb_cleaning/analysis.py`：已把这条主 helper 从一句“3D 强分析”再补成 source-grounded tri-frame consumer contract，明确写清它当前固定消费 `diag1000398/0399/0400` 三帧 whole-domain `G_old/divB/G_new`，用脚本内硬编码 `dt` 重建 centered-stencil 的 `c^2 div(B) = dG/dt` 离散关系，并对全域最大相对误差施加 `< 1e-1` gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/diff_lumi_diag/analysis.py`：已把这条主 helper 从一句“强分析”再补成 source-grounded dual-spectrum consumer contract，明确写清它当前固定双消费 `DifferentialLuminosity_beam1_beam2.txt` 和 `DifferentialLuminosity2d_beam1_beam2/`，分别对末时刻 `1D dL/dE` 文本谱和 `iteration=80` 的 `2D d^2L/dE1dE2` openPMD 网格施加解析双高斯误差 gate，并按 `leptons/photons` 分支切换容差。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/electrostatic_sphere/analysis_electrostatic_sphere.py`：已把这条主 helper 从一句“强分析”再补成 source-grounded shared consumer contract，明确写清它当前统一服务 `7` 条 active baseline，先对最终 plotfile 的单轴 `Ex/Ey/Ez` 或 `Er/Ez` lineout 施加解析自场膨胀 `L2` gate，再只在 `diag2` 确实带 `phi` 时继续命中 `Ek + Ep` 的 openPMD 能量账本分支，并保留 `emass_10` 与 `uniform_weighting` 的独立容差分叉。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_rz_scraping.json`：已把这条 RZ `BoundaryScraping` active baseline 从旧式 `checksum 基线` 口径补成 source-grounded 强描述，明确写清它当前不是 checksum-only，而是 `analysis_rz.py diags/diag1000037 + analysis_default_regression.py --path diags/diag1000037` 的双链；producer 侧固定 materialize `AMR + cylindrical EB + inward-ring electrons + Maxwell=none` 的纯粒子 scraping scaffold，并并排落出 `diag2` 主容器 openPMD 与 `diag3/particles_at_eb` scraped-buffer openPMD，而主 consumer 则对整段时间序列施加“remaining + scraped = initial”守恒和全量 `id` 闭合 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_rz_scraping_filter.json`：已把这条 RZ `BoundaryScraping` half-domain sibling 从旧式 `checksum 基线` 口径补成 source-grounded 强描述，明确写清它当前不是 checksum-only，而是 `analysis_rz_filter.py diags/diag1000037 + analysis_default_regression.py --path diags/diag1000037` 的双链；producer 侧与主线共用 `AMR + cylindrical EB + inward-ring electrons + Maxwell=none` scaffold，只额外把 `diag3.electron.plot_filter_function(...)= "z > 0"` 挂到 scraped-buffer surface 上，而主 consumer 则把这件事压成 `2 * scraped + remaining = initial` 的双倍补偿守恒外加全量 `z > 0` 筛选 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_rz_point_of_contact_eb.json`：已在原有强描述上再补一层 surface-split 边界，明确写清这条 RZ 单电子撞击圆柱 EB regression 当前虽然仍绑定 `analysis.py + analysis_default_regression.py --path diags/diag1/`，但主 analysis 与 checksum 并不共吃同一 surface；`diag1/` 只承担 same-directory `Er` checksum side surface，而 `analysis.py` 实际固定回读的是 `diag2/particles_at_eb` 的 `BoundaryScraping` contact-event openPMD，并在其上对 `stepScraped / deltaTimeScraped / x/y/z / nx/ny/nz` 逐项施加解析几何 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_rz_projection_div_cleaner.json`：已在原有强描述上再补一层 same-final-surface 边界，明确写清这条 RZ file-backed projection-cleaner regression 当前虽然仍绑定 `analysis.py diags/diag1000001 + analysis_default_regression.py --path diags/diag1000001`，但它并不是 main consumer 与 checksum 分离到不同输出面的结构；主 analysis 与 helper 共吃同一张 `diag1000001` plotfile，其中 analysis 专门回读 `plot_raw_fields` 落出的 `raw Bx_aux/Bz_aux` auxiliary-field surface，按柱坐标离散公式重建 interior `divB` 并施加 `< 4e-3` gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_rz_particle_boundary_interaction_picmi.json`：已在原有强描述上再补一层 writer-surface 边界，明确写清这条 RZ PICMI 镜面反射 regression 当前虽然仍绑定 `analysis.py diags/diag1/ + analysis_default_regression.py --path diags/diag1/`，但这里的 `diags/diag1/` 不是单纯 field surface，而是同名 `FieldDiagnostic + ParticleDiagnostic` 共同 materialize 的 same-directory combined openPMD；主 consumer 在其最终粒子输出上做解析反射轨道匹配，而 helper 则对同目录整体做 additive checksum。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_rz_secondary_ion_emission_picmi.json`：已在原有强描述上再补一层 writer-surface 边界，明确写清这条 RZ PICMI 次级电子发射 regression 当前虽然仍绑定 `analysis.py diags/diag1/ + analysis_default_regression.py --path diags/diag1/`，但这里的 `diags/diag1/` 同样不是单纯 field surface，而是同名 `FieldDiagnostic + ParticleDiagnostic` 共同 materialize 的 same-directory combined openPMD；主 consumer 在其最终电子输出上做反向几何匹配，而 helper 则对同目录整体做 additive checksum。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_rz_spacecraft_charging_picmi.json`：已在原有强描述上再补一层 writer-surface 边界，明确写清这条 RZ PICMI immersed-conductor charging regression 当前虽然仍绑定 `analysis.py diags/diag1/ + analysis_default_regression.py --path diags/diag1/`，但这里的 `diags/diag1/` 不是单纯 field surface，而是同名 `FieldDiagnostic + ParticleDiagnostic` 共同 materialize 的 same-directory combined openPMD main surface；相对地，`diag2` 只在末尾落盘 scraped-particle side surface，而主 consumer 继续只在 `diag1/` 上做 `phi_min(t)` 指数拟合。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_2d_particle_reflection_picmi.json`：已在原有强描述上再补一层 producer-consumer surface split，明确写清这条 2D `particle_boundary_process` regression 当前没有独立 analysis 脚本，但已经显式分成两层：主 consumer 是输入脚本在 `sim.step(10)` 后直接回读 `z_hi/z_lo` boundary buffers，对粒子数 `63/67` 与 `stepScraped = 4/8` 做 in-process 断言；相对地，`analysis_default_regression.py` 则只独占消费分离出来的 `diag1000010` final plotfile checksum side surface。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/collider_relevant_diags/analysis.py`：已把这条主 helper 从一句“强分析”再补成 source-grounded consumer contract，明确写清它当前同时固定消费 `warpx_used_inputs`、`ParticleExtrema/ColliderRelevant` reduced ledgers 和 `diag2/openpmd_%T.h5` full surface，逐项重建并硬断言 `chi`、`theta_x/theta_y`、`x/y` 统计量，以及整条 `dL_dt` luminosity 序列。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_2d_plasma_mirror.json`：已把这条 baseline 从宽泛“2D plasma-mirror 应用骨架”再补成 source-grounded producer/consumer 描述，明确写清它当前是 `single active baseline + 2-frame producer + final-only checksum consumer chain`；也就是 20-step native laser-solid scaffold 会落出 `diag1000010/diag1000020`，但 active wiring 实际只接住末态 `diag1000020`。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Physics_applications/pierce_diode/plot_sim.py`：已把这条 side helper 从一句“可视化脚本；复现 README 图”再补成 source-grounded 描述，明确写清它当前固定只消费本地 `./diags/diag1/`，复用主 analysis 同一套 Child-Langmuir 理论量，但只负责把 `u_z/E_z/J_z/phi` 重建成固定 `2x2` 四面板并落出 `Pierce_Diode.png`，不承担任何 `phi/jz` gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Physics_applications/laser_ion/plot_2d.py`：已把这条 side helper 从一句“后处理可视化脚本”再补成 source-grounded 描述，明确写清它当前默认固定消费 `diagInst` 的瞬时 openPMD full surface，并把 `rho_electrons/rho_hydrogen` 三联 density panel、`Ex/By/Ez` 三联 field panel，以及 `reducedfiles/<diag_name>.txt` 粒子谱线统一落到 `analysis/` side-artifact pipeline。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Physics_applications/laser_ion/analysis_histogram_2D.py`：已把这条 side helper 从一句“reduced diagnostic 可视化脚本”再补成 source-grounded 描述，明确写清它当前固定只消费 `diags/reducedfiles/<hist2D>` 目录，把 `field=data` 的二维 reduced histogram 按单帧或 `All` 批量转成 `Histogram_2D_<name>_iteration_<i>.png`，并显式对齐 native `ParticleHistogram2D` surface 与 PICMI 侧仍保留的 `TODO` 缺口。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Physics_applications/laser_acceleration/plot_3d.py`：已把这条 side helper 从一句“`yt.SlicePlot` 可视化 helper”再补成 source-grounded 描述，明确写清它当前固定只消费单个 plotfile 参数，沿 `y` 法向只对 `Ey/rho` 做 `SlicePlot` 双面板展示，不生成稳定 side artifact，也不参与任何自动 regression wiring。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Physics_applications/laser_acceleration/analysis_openpmd_rz.py`：已把这条 helper 行从一句“检查 RZ openPMD diagnostics”再补成 source-grounded consumer 描述，明确写清它当前固定只消费 `diags/diag1/openpmd_%T.h5`，并对 `3` 个 iterations、`8` 个 meshes、`j_t` 的 `(Nm,Nz,Nr)=(3,512,64)`、`part_per_grid/rho_electrons` dataset shape、以及 `rho_beam/rho_electrons` 的物理中心次序一次性施加 diagnostics-contract 断言。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Physics_applications/free_electron_laser/plot_sim.py`：已把这条 side helper 从一句 FEL 可视化摘要再补成 source-grounded 粒度，明确写清它当前固定只消费 `diag_labframe`，先对整条 BTD 序列提取 `|E_x|` 峰值增长曲线，再把 `iteration = 16` 的电子 `z` 向直方图和 `E_x` lineout 叠成 snapshot，对应落成 `FEL.png`。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Physics_applications/ion_beam_extraction/inputs_test_3d_ion_beam_extraction`：已把这条输入行从宽泛“3D 电静离子束抽取场景”再补成 source-grounded producer 描述，明确写清它当前不只 materialize `warpx.do_electrostatic = labframe + eb_implicit_function + eb_potential` 的 embedded-boundary 电极抽取器骨架，还会把 `Dplus/electrons` 在 `z<0` 的初始热等离子体填充、`-z/±x/±y` 五面 `NFluxPerCell + gaussianflux` 热通量补料，以及 same-directory `diag1(phi/eb_covered/rho_*) + BoundaryScraping` diagnostics surfaces 一次性落成。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Physics_applications/ion_beam_extraction/analysis_ion_beam_extraction.py`：已把这条 helper 行从宽泛“读取 `phi`、`eb_covered` 和 `Dplus` 粒子，检查 `40 keV`”再补成 source-grounded consumer 描述，明确写清它当前固定只消费 `diags/diag1/` 的 `iteration = 1000` 单帧，先把 `phi/eb_covered` 重建成电势/EB 轮廓叠图，再从同帧 `Dplus` 的 `ux/uy/uz/mass` 反算 `energy_keV`，最后仅对 `14-23 mm` 尾束窗口施加 `40 keV ±5%` 的逐粒子 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Physics_applications/beam_beam_collision/plot_fields.py`：已把这条 side helper 从一句 openPMD 可视化摘要再补成 source-grounded 粒度，明确写清它当前不消费 reduced ledgers，而是固定遍历同目录 `diag1` 的全部 iterations，并沿 `x/y` 两条切片支线把 `|E|`、`|B|`、主束 `rho` 和次级对 `rho` 重建成四宫格时序图，逐帧落成 `FIELDS_x_<iter>.png` 与 `FIELDS_y_<iter>.png`。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Physics_applications/beam_beam_collision/plot_reduced.py`：已把这条 side helper 从一句 reduced 可视化摘要再补成 source-grounded 粒度，明确写清它当前不消费 `diag1` openPMD 主面，而是固定回读 `ColliderRelevant_beam1_beam2.txt + ParticleNumber.txt`，先用 `argmax(dL_dt)` 反解对撞时刻，再把 photon/NLBW 产额重建成按总 primary beam 权重归一化、并以 `(time-coll_time)/(sigma_z/c)` 为横轴的两条 side curves。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Physics_applications/beam_beam_collision/inputs_test_3d_beam_beam_collision`：已把这条输入行从偏骨架式的 collider-QED 摘要再补成 output-surface 粒度，明确写清它当前不仅 materialize `beam1/beam2 + pho1/pho2 + ele*/pos*` 的 3D 对撞 producer，也把同目录 `diag1` 固定成 openPMD checksum main surface，并把 `ParticleNumber + ColliderRelevant_beam1_beam2` 压成只供 `plot_reduced.py` 消费的 reduced plot-only side ledgers。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/nodal_electrostatic/analysis_default_regression.py`：已把这条 helper 行从偏泛化的 checksum 描述再补成 wiring-bound 粒度，明确写清它当前只独占服务 `test_3d_nodal_electrostatic_solver` 这条 `slow` 基线，并且只命中分离出来的 `diags/diag1000010` final-plotfile checksum side surface；对应的 reduced `chi_max + photon-count` 零触发主链仍完全由 `analysis.py` 单独承担。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `load_external_field umbrella summary`：已把这条 family-level 行从偏 consumer-only 的 `2/2/4/3 shared-analysis split` 再补成 producer/consumer 双侧闭合粒度，明确写清它当前不仅在 consumer 侧收成 `3D magnetic-mirror / RZ magnetic-mirror / time-scaling / restart` 四段 shared-analysis 主链，也在 producer 侧同步收成 `3D grid/particle`、`RZ grid/particle`、`single-frequency native/PICMI`、`dual-frequency native/PICMI`、`restart continuation` 这组 `2/2/2/2/3` scaffold split。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/load_external_field/inputs_test_3d_load_external_field_particle_time`：已把这条原生单频输入行从偏 producer-only 的“验证 `read_fields_B_dependency(t)`”再补成 same-series surface 粒度，明确写清它当前不只 materialize `read_fields_B_dependency = cos(omega t + phase_B)` 的 producer，还会落出同一条 `diag1` 时间序列里的 `diag1000000/diag1000300` 这条 `pf0/pfN` field surface，先供 `analysis_time_scaling.py` 做 `Bz` 非零目标缩放比主链，再把同一末态 `diag1000300` 交给 helper 追加 checksum。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/load_external_field/inputs_test_3d_load_external_field_particle_multi_time`：已把这条原生多频输入行从偏 producer-only 的“验证 `particles.B_ext_particle_fields`”再补成 same-series surface 粒度，明确写清它当前不只 materialize `b1/b2 + cos(omega t)/cos(2 omega t)` 的 dual-field producer，还会落出同一条 `diag1` 时间序列里的 `diag1000000/diag1000300` 这条 `pf0/pfN` field surface，先供 `analysis_time_scaling.py` 做 `Bz` 零目标相消主链，再把同一末态 `diag1000300` 交给 helper 追加 checksum。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/load_external_field/inputs_test_3d_load_external_field_particle_time_picmi.py`：已把这条输入行从宽泛“PICMI particle external field 时间依赖”再补成 same-series surface 粒度，明确写清它当前不只 materialize 单频 `LoadAppliedField` producer，还会落出 `diag1000000/diag1000300` 这条 `pf0/pfN` field surface，先供 `analysis_time_scaling.py` 做 `Bz` 缩放比主链，再把同一末态 `diag1000300` 交给 helper 追加 checksum。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/load_external_field/inputs_test_3d_load_external_field_particle_time_restart`：已把这条 restart 入口从宽泛“3D restart 变体”再补成 dependency/shared-surface 粒度，明确写清它当前显式依赖 `test_3d_load_external_field_particle_time`，并把恢复后的同名 `diags/diag1000300` 同时交给 `analysis_default_restart.py` 的逐字段 reproducibility gate 与 helper 的 additive checksum。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/load_external_field/inputs_test_rz_load_external_field_particles_restart`：已把这条 restart 入口从宽泛“RZ restart 变体”再补成 dependency/shared-surface 粒度，明确写清它当前显式依赖 `test_rz_load_external_field_particles`，并把恢复后的同名 `diags/diag1000300` 同时交给 `analysis_default_restart.py` 的逐字段 reproducibility gate 与 helper 的 additive checksum。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/load_external_field/inputs_test_rz_load_external_field_grid_restart`：已把这条 restart 入口从宽泛“RZ restart 变体”再补成 dependency/shared-surface 粒度，明确写清它当前显式依赖 `test_rz_load_external_field_grid`，并把恢复后的同名 `diags/diag1000300` 同时交给 `analysis_default_restart.py` 的逐字段 reproducibility gate 与 helper 的 additive checksum。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/initial_distribution/analysis_default_regression.py`：已把这条 helper 行从宽泛“通用 checksum helper”再补成 side-surface wiring 粒度，明确写清它虽然仍是共享 `plotfile/openPMD` checksum wrapper，但在当前 `initial_distribution` wiring 上只独占服务 `test_3d_initial_distribution` 这一条 active baseline，并且只钉在分离出来的 `diags/diag1000001` final-plotfile additive checksum side surface 上；对应的 reduced histogram/beam-monitor 主消费者链则完全由 `analysis.py` 单独承担。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/load_density/inputs_test_rz_load_density_prepare.py`：已把这条 prepare 行从宽泛“生成 theta-mode density mesh”再补成 dependency-wiring 粒度，明确写清它在当前 `load_density` wiring 上同样是 `analysis=OFF + checksum=OFF` 的 dependency-only prepare sibling，会先 materialize `example-density.h5`，再显式供 `test_rz_load_density` 的 `read_density_from_path + moving-window + analysis_rz.py + analysis_default_regression.py --path diags/diag/` 主链消费。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/initial_plasma_profile/analysis_default_regression.py`：已把这条 helper 行从宽泛“通用 checksum helper”再补成 family-wiring 粒度，明确写清它虽然仍是共享 `plotfile/openPMD` checksum wrapper，但在当前 `initial_plasma_profile` wiring 上只独占服务 `test_2d_parabolic_channel_initialization` 这一条 active baseline，并把唯一自动消费者链收窄到 `diags/diag1000001 --skip-particles --rtol 1e-4` 对应的 `fields-only` final-plotfile additive checksum surface。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/laser_on_fine/inputs_test_2d_laser_on_fine`：已把这条 input 行从宽泛“2D AMR placement 场景”补成 source-grounded producer 描述，明确写清它显式 materialize `max_step = 50`、`64 x 64` 网格、`blocking_factor = 32`、中心狭长 fine patch、`x periodic / z pml`、`esirkepov + standard charge deposition + energy-conserving gather`、沿 `+z` 传播的 native `Gaussian` laser antenna，以及 `diag1.intervals = 10` 下最终落到 `diag1000050` 的 reduced-field checksum producer surface。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/laser_on_fine/analysis_default_regression.py`：已把这条 helper 行从宽泛“checksum helper”补成 source-grounded 描述，明确写清它虽然仍是共享 `plotfile/openpmd` checksum wrapper，但在当前 `laser_on_fine` wiring 上只独占服务 `test_2d_laser_on_fine` 这一条 active baseline，并把唯一自动消费者链收窄到 `diags/diag1000050` final plotfile additive checksum surface。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/larmor/inputs_test_2d_larmor`：已把这条 input 行从宽泛“2D 外部 `B_y` 回旋场景”补成 source-grounded producer 描述，明确写清它显式 materialize `max_step = 10`、`64 x 64` 网格、中心单层 MR 细化盒、四面 `pml`、constant external-`B_y` particle field、镜像 `electron/positron` `SingleParticle`、`algo.particle_shape = 3`、`warpx.do_dive_cleaning = 1`，以及并行 `diag1/diagraw` full/raw diagnostics surfaces，并最终只对接 `diag1000010` checksum-only consumer 链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/larmor/analysis_default_regression.py`：已把这条 helper 行从宽泛“本地 checksum helper”补成 source-grounded 描述，明确写清它虽然仍是共享 `plotfile/openpmd` checksum wrapper，但在当前 `larmor` wiring 上只独占服务 `test_2d_larmor` 这一条 active baseline，并把唯一自动消费者链收窄到 `diags/diag1000010` final plotfile additive checksum surface。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `laser_injection umbrella summary`：已把这条 family-level 行从 `5 active baselines + 4/1 checksum split + 2/2/1 analysis-state split + native/implicit runtime sibling` 再补成 source-grounded 更高层结构，明确写清 producer 层现在也已经同步收成 `2/2/1`：`1D native/implicit` 共用 `Gaussian antenna + z-moving-window + diag1/openpmd` 基座、`2D native/implicit` 共用 `oblique Gaussian antenna + x-moving-window + diag1@240` 基座，而 `3D` 单独落成 `axis-aligned Gaussian antenna + z-moving-window + reduced field surface` 的 checksum-main scaffold。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/laser_injection/analysis_default_regression.py`：已把这条 helper 行从宽泛“目录内 checksum helper”补成 source-grounded 描述，明确写清它虽然仍是共享 `plotfile/openpmd` checksum wrapper，但在当前 `laser_injection` wiring 上实际统一服务 `5` 条 active baseline，并已经稳定收成 `4/1` checksum-surface split，也就是 `1D/2D native/implicit -> diag1000240`，`3D -> diag1000020`；同时也写清它始终只是 same-final-plotfile additive checksum sibling，不替代 `analysis_1d.py` / `analysis_2d.py` 的强断言或 `analysis_3d.py` 的 placeholder side-analysis。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/laser_injection/inputs_test_3d_laser_injection`：已把这条 input 行从宽泛“3D Gaussian 天线注入”补成 source-grounded producer 描述，明确写清它显式 materialize `max_step = 20`、`32 x 32 x 240` 的 3D periodic/periodic/PEC 几何、axis-aligned native `Gaussian` antenna 参数、`z` 向 moving window，以及末态 `diag1@20` 的 reduced `jx/jy/jz/Ex/Ey/Ez/Bx/Bz` output surface，并最终对接 placeholder `analysis_3d.py + diag1000020` checksum 链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/laser_injection/analysis_3d.py`：已把这条 helper 行从宽泛“只是占位图”补成 source-grounded 描述，明确写清它当前只服务 `test_3d_laser_injection`、在 CMake 层不接收任何 `diag` 参数、脚本自身也不读取 plotfile/openPMD/fields，而只是本地生成一条 `1 + sin(2*pi*t)` 曲线并落出 `laser_analysis.png`；也就是说这支当前真实角色只是 placeholder side-analysis，而稳定自动消费者仍主要是 `diag1000020` final plotfile checksum。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/laser_injection/inputs_test_1d_laser_injection_implicit`：已把这条 input 行从宽泛“1D semi-implicit laser injection”补成 source-grounded producer 描述，明确写清它在普通 1D Gaussian producer 的 `352` 点 PEC 几何、antenna、`z` 向 moving window 与并行 `diag1/openpmd` surfaces 基座上，只额外分叉出 `algo.evolve_scheme = semi_implicit_em`、`newton.max_iterations = 21`、`newton.relative_tolerance = 1e-8`、`gmres.max_iterations = 1000` 与 `gmres.relative_tolerance = 1e-4` 这组 implicit solver 参数，并最终对接 shared `analysis_1d.py + diag1000240` consumer 链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/laser_injection/inputs_test_2d_laser_injection_implicit`：已把这条 input 行从宽泛“2D semi-implicit laser injection”补成 source-grounded producer 描述，明确写清它在普通 2D oblique Gaussian producer 的 `480 x 352` 几何、antenna、`x` 向 moving window 与 `diag1@240` full-plotfile surface 基座上，只额外分叉出 `algo.evolve_scheme = semi_implicit_em`、`newton.max_iterations = 21`、`newton.relative_tolerance = 1e-8`、`gmres.max_iterations = 1000` 与 `gmres.relative_tolerance = 1e-4` 这组 implicit solver 参数，并最终对接 shared `analysis_2d.py + diag1000240` consumer 链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/laser_injection/inputs_test_2d_laser_injection`：已把这条 input 行从宽泛“2D 斜入射 Gaussian 天线注入”补成 source-grounded producer 描述，明确写清它显式 materialize `max_step = 240`、`480 x 352` 的 2D PEC/periodic 几何、`esirkepov + cfl=1.0 + particle_shape=1`、oblique `Gaussian` antenna 参数、`x` 向 moving window，以及末态 `diag1@240` full-plotfile surface，并最终对接 shared `analysis_2d.py + diag1000240` consumer 链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/laser_injection/analysis_2d.py`：已把这条 helper 行从宽泛“2D 包络与主频检查”补成 source-grounded consumer 描述，明确写清它当前共同服务 `test_2d_laser_injection` 与 `test_2d_laser_injection_implicit`、只消费 `diags/diag1000240` 末态 plotfile、脚本内对 `Ex/Ey/Ez/Bx/By/Bz` 六分量逐个执行 2D Hilbert 包络与 `fft2` 主频双断言，对应阈值统一 `5%`，理论零分量还会命中 `small_num` 零场分支，并额外挂出 `plt_<component>.png` side artifacts。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/laser_injection/inputs_test_1d_laser_injection`：已把这条 input 行从宽泛“1D Gaussian 天线注入基准”补成 source-grounded producer 描述，明确写清它显式 materialize `max_step = 240`、`352` 点 1D PEC 几何、`esirkepov + cfl=0.9 + particle_shape=1`、本地 `Gaussian` antenna 参数、`z` 向 moving window，以及并行 `diag1/openpmd` full surfaces，并最终对接 shared `analysis_1d.py + diag1000240` consumer 链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/laser_injection/analysis_1d.py`：已把这条 helper 行从宽泛“1D 包络与主频检查”补成 source-grounded consumer 描述，明确写清它当前共同服务 `test_1d_laser_injection` 与 `test_1d_laser_injection_implicit`、只消费 `diags/diag1000240` 末态 plotfile、脚本内对 `Ex/Ey/Ez/Bx/By/Bz` 六分量逐个执行 Hilbert 包络与 FFT 主频双断言，对应阈值统一 `5%`，理论零分量还会命中 `small_num` 零场分支，并额外挂出 `plt_<component>.png` side artifacts。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/langmuir_fluids/inputs_test_rz_langmuir_fluid`：已把这条 input 行从宽泛“RZ 冷流体基准”补成 source-grounded producer 描述，明确写清它显式 materialize `my_constants.max_step = 80`、`64 x 128` 的 RZ 几何、`energy-conserving + esirkepov + cfl=1.0 + do_dive_cleaning=1`、电子高斯横向包络的 `parse_momentum_function` 初扰加静止离子背景，以及 `diag1(jr/jz/Er/Ez/Bt/rho)` full surface。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/langmuir_fluids/inputs_test_1d_langmuir_fluid`：已把这条 input 行从宽泛“1D 冷流体基准”补成 source-grounded producer 描述，明确写清它显式 materialize `max_step = 80`、`amr.n_cell = 128`、`1D periodic` 几何、`warpx.cfl = 0.8`、双 fluid species 的对向 `parse_momentum_function` Langmuir 初扰，以及 `diag1(Ez/jz/rho)` 加并行 `openpmd` full surface。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/langmuir_fluids/analysis_3d.py`：已把这条 helper 行从宽泛“3D 冷流体强分析”补成 source-grounded consumer 描述，明确写清它当前固定服务 `test_3d_langmuir_fluid`、只消费 `diags/diag1000040` 末态 plotfile、脚本内显式重建 `Ex/Ey/Ez/Jx/Jy/Jz/rho` 的三维 cold-fluid 理论场，其中 `J` 分量带 `dt=t/40` 的 Yee 半步补偿，最终以统一的 `error_rel < 5e-2` 收口，并额外挂出 `Langmuir_fluid_multi_analysis.png` 的 `Ez@y=0` 切片图。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/langmuir_fluids/analysis_1d.py`：已把这条 helper 行从宽泛“1D 冷流体强分析”补成 source-grounded consumer 描述，明确写清它当前固定服务 `test_1d_langmuir_fluid`、只消费 `diags/diag1000080` 末态 plotfile、脚本内显式重建 `Ez/Jz/rho` 的一维 cold-fluid 理论场，其中 `Jz` 还带 `dt=t/80` 的 Yee 半步补偿，最终以统一的 `error_rel < 0.05` 收口，并额外挂出 `langmuir_fluid_multi_1d_analysis.png` 曲线图。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/langmuir_fluids/analysis_rz.py`：已把这条 helper 行从宽泛“RZ 冷流体强分析”补成 source-grounded consumer 描述，明确写清它当前固定服务 `test_rz_langmuir_fluid`、只消费 `diags/diag1000080` 末态 plotfile、脚本内显式重建高斯径向包络下的 `Er/Ez/Jr/Jz/rho` 理论场，其中 `Jr/Jz` 还带 `dt=t/80` 的 Yee 半步补偿，最终以统一的 `error_rel < 0.08` 收口，并额外挂出以 test name 命名的 `*_analysis.png` 对比图。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/langmuir_fluids/analysis_2d.py`：已把这条 helper 行从宽泛“2D 冷流体强分析”补成 source-grounded consumer 描述，明确写清它当前固定服务 `test_2d_langmuir_fluid`、只消费 `diags/diag1000080` 末态 plotfile、脚本内显式重建 `Ex/Ez/Jx/Jz/rho` 的二维 cold-fluid 理论场，其中 `Jx/Jz` 还带 `dt=t/40` 的 Yee 半步补偿，最终以统一的 `error_rel < 0.05` 收口，并额外挂出 `Langmuir_fluid_multi_2d_analysis.png` 切片图。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/langmuir_fluids/inputs_test_2d_langmuir_fluid`：已把这条 input 行从宽泛“2D 冷流体基准”补成 source-grounded producer 描述，明确写清它显式 materialize `max_step = 80`、`128 x 128` 周期盒、`energy-conserving + cfl=1.0`、双 fluid species 反号二维 Langmuir 模态，以及 `diag1` 的 `Ex/Ez/jx/jz/rho` 输出面。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/langmuir_fluids/inputs_test_3d_langmuir_fluid`：已把这条 input 行从宽泛“3D 冷流体基准”补成 source-grounded producer 描述，明确写清它显式 materialize `40 µm` 周期立方盒、`64^3`、`esirkepov + energy-conserving + cfl=1.0`、双 fluid species 反号三维 Langmuir 模态，以及末态 `diag1` 的 `Ex/Ey/Ez/Bx/By/Bz/jx/jy/jz/part_per_cell/rho` 输出面。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `Examples/Tests/langmuir_fluids/analysis_default_regression.py`：已把这条 helper 行从宽泛“通用 checksum helper”补成 source-grounded 强描述，明确写清它虽然仍是指向共享 `../../analysis_default_regression.py` 的符号链接，但在当前 wiring 上实际统一服务 `4` 条 active cold-fluid baseline，并形成 `3+1` checksum-surface split，也就是 `1D/2D/RZ -> diag1000080`，`3D -> diag1000040`。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_langmuir_fluid.json`：已把这条残留偏弱的 baseline 统一补成更硬的 source-grounded 强描述，明确写清它与 `langmuir_fluids` 的 `1D/2D/RZ` sibling 共同命中 `analysis_3d.py diags/diag1000040 + analysis_default_regression.py --path diags/diag1000040`，producer 侧补齐了 `40 µm` 周期立方盒、`64^3`、`esirkepov + energy-conserving + cfl=1.0`、双 fluid species 反号三维 Langmuir 模态与末态 `diag1` field/current/rho surface，而 shared consumer 则只在同一张末态 plotfile 上逐分量比较解析 `E/J/rho`，不会再追加粒子版 `langmuir` 那条 selective-particle/openPMD/charge-conservation side chain。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_rz_langmuir_multi.json`：已顺手纠正文档里和当前源码不一致的一处主 gate 描述，把 `analysis_rz.py` 上的 `Er/Ez` 解析场阈值从误写的 `< 0.08` 改回源码实际的 `< 0.12`，并补清这条 native RZ 路径会继续消费三套 filter diagnostics、同时不会触发通用 `analysis_utils.py` 守恒 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_langmuir_multi_nodal.json`：已把这条残留偏弱的 baseline 统一补成更硬的 source-grounded 强描述，明确写清它同样固定命中 `analysis_3d.py diags/diag1000040 + analysis_default_regression.py --path diags/diag1000040`，producer 侧在共享 3D Langmuir scaffold 上只把 runtime 分叉切成 `direct deposition + collocated grid`，而 shared consumer 则继续执行 selective-particle output 检查、末态解析 `Ex/Ey/Ez` 主 gate 与 `openPMD` on-particle-field side consumer，同时不再触发 native 基线里的 `1e-11` 守恒 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_langmuir_multi.json`：已把这条残留偏弱的 baseline 统一补成更硬的 source-grounded 强描述，明确写清它固定命中 `analysis_3d.py diags/diag1000040 + analysis_default_regression.py --path diags/diag1000040`，producer 侧经 `inputs_base_3d` 补齐了 `esirkepov + energy-conserving + cfl=1.0`、双 species 反号动量模态、selective particle output 与 openPMD on-particle-field 这些 source boundary，而 shared consumer 则继续执行 selective-particle output 检查、末态解析 `Ex/Ey/Ez` 主 gate、`openPMD` on-particle field side consumer，并额外命中 `analysis_utils.py` 的 `1e-11` 守恒 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_rz_langmuir_multi_picmi.json`：已把这条残留偏弱的 baseline 统一补成更硬的 source-grounded 强描述，明确写清它外层虽然是 `analysis=OFF + analysis_default_regression.py --path diags/diag1000040` 的 checksum wiring，但脚本内会直接从 `Efield_aux` 取回多 azimuthal mode 的 `Er/Ez`，沿 `theta=0` 重建物理场并与解析多模 Langmuir 解比较到 `< 0.02`，同时补齐了 `CylindricalGrid(n_azimuthal_modes=3)`、双 species `GriddedLayout([2,16,2])` 和 reduced `diag1` field/particle surface 的 source boundary。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_langmuir_multi_picmi.json`：已把这条残留偏弱的 baseline 统一补成更硬的 source-grounded 强描述，明确写清它当前就是 `analysis=OFF + analysis_default_regression.py --path diags/diag1000040` 的 checksum-only active 路径，producer 侧显式走 `UniformDistribution + Species + Cartesian3DGrid + ElectromagneticSolver + Simulation` 的 PICMI front-end，并补齐 `direct` deposition、`64^3` 周期盒、`cfl=1.0`、`n_macroparticle_per_cell=[2,2,2]` 与 reduced `Ex/Jx + electrons(weighting,ux)` diagnostic surface 的 source boundary。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_langmuir_multi_psatd_JRhom_LL2_picmi.json`：已把这条残留偏弱的 baseline 统一补成更硬的 source-grounded 强描述，明确写清它只会在 `WarpX_FFT` 打开时固定命中 `analysis_3d.py diags/diag1000040 + analysis_default_regression.py --path diags/diag1000040`，producer 侧显式走 PICMI front-end，把 native `direct + PSATD + JRhom_LL2 + update_with_rho` 路径映射成 `AnalyticDistribution + Cartesian3DGrid + ElectromagneticSolver + Simulation`，并补齐 field/selective-particle/openPMD 三条 diagnostics 的 source boundary，而 shared consumer 则继续执行 selective-particle output 检查、末态解析 `Ex/Ey/Ez` 主 gate、`openPMD` on-particle field side consumer，同时不触发 `analysis_utils.py` 的通用守恒 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_langmuir_multi_psatd_div_cleaning.json`：已把这条残留偏弱的 baseline 统一补成更硬的 source-grounded 强描述，明确写清它只会在 `WarpX_FFT` 打开时固定命中 `analysis_3d.py diags/diag1000040 + analysis_default_regression.py --path diags/diag1000040`，producer 侧是在共享 3D Langmuir scaffold 上把 FFT-backed 分叉切成 `direct + PSATD + update_with_rho + do_dive/do_divb_cleaning`，并补齐 `diag1.intervals`、`diag1.fields_to_plot`、`warn-threshold` 与 `cfl=0.5773502691896258` 的 source boundary，而 shared consumer 则继续执行 selective-particle output 检查、末态解析 `Ex/Ey/Ez` 主 gate、`openPMD` on-particle field side consumer，并额外挂出 `diag1000038/39/40` 的 tri-frame `F/divE/rho` side chain，同时不触发通用 `analysis_utils.py` 守恒 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_langmuir_multi_psatd_vay_deposition_nodal.json`：已把这条残留偏弱的 baseline 统一补成更硬的 source-grounded 强描述，明确写清它只会在 `WarpX_FFT` 打开时固定命中 `analysis_3d.py diags/diag1000040 + analysis_default_regression.py --path diags/diag1000040`，producer 侧是在共享 3D Langmuir scaffold 上把 nodal FFT-backed 分叉切成 `Vay current deposition + PSATD + collocated`，并补齐 `diag1.fields_to_plot` 与 `cfl=0.5773502691896258` 的 source boundary，而 shared consumer 则继续执行 selective-particle output 检查、末态解析 `Ex/Ey/Ez` 主 gate、`openPMD` on-particle field side consumer，并额外命中 `analysis_utils.py` 的 `1e-3` 守恒 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_langmuir_multi_psatd_current_correction_nodal.json`：已把这条残留偏弱的 baseline 统一补成更硬的 source-grounded 强描述，明确写清它只会在 `WarpX_FFT` 打开时固定命中 `analysis_3d.py diags/diag1000040 + analysis_default_regression.py --path diags/diag1000040`，producer 侧是在共享 3D Langmuir scaffold 上把 nodal FFT-backed 分叉切成 `direct + PSATD + current_correction + periodic_single_box_fft + collocated`，并补齐 `diag1.fields_to_plot` 与 `cfl=0.5773502691896258` 的 source boundary，而 shared consumer 则继续执行 selective-particle output 检查、末态解析 `Ex/Ey/Ez` 主 gate、`openPMD` on-particle field side consumer，并额外命中 `analysis_utils.py` 的 `1e-9` 守恒 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_langmuir_multi_psatd_current_correction.json`：已把这条残留偏弱的 baseline 统一补成更硬的 source-grounded 强描述，明确写清它只会在 `WarpX_FFT` 打开时固定命中 `analysis_3d.py diags/diag1000040 + analysis_default_regression.py --path diags/diag1000040`，producer 侧是在共享 3D Langmuir scaffold 上把 FFT-backed 分叉切成 `esirkepov + PSATD + current_correction + periodic_single_box_fft`，并补齐 `diag1.fields_to_plot` 与 `cfl=0.5773502691896258` 的 source boundary，而 shared consumer 则继续执行 selective-particle output 检查、末态解析 `Ex/Ey/Ez` 主 gate、`openPMD` on-particle field side consumer，并额外命中 `analysis_utils.py` 的 `1e-9` 守恒 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_langmuir_multi_psatd.json`：已把这条残留偏弱的 baseline 统一补成 source-grounded 强描述，明确写清它只会在 `WarpX_FFT` 打开时固定命中 `analysis_3d.py diags/diag1000040 + analysis_default_regression.py --path diags/diag1000040`，producer 侧是在共享 3D Langmuir scaffold 上把 FFT-backed 基线分叉切成 `PSATD + cfl=0.5773502691896258`，而 shared consumer 则会同时执行 selective-particle output 检查、末态解析 `Ex/Ey/Ez` 主 gate 与 `openPMD` on-particle field side consumer，并且不会额外触发 `analysis_utils.py` 的守恒 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_2d_langmuir_multi_psatd_vay_deposition.json`：已把这条残留偏弱的 baseline 统一补成 source-grounded 强描述，明确写清它只会在 `WarpX_FFT` 打开时固定命中 `analysis_2d.py diags/diag1000080 + analysis_default_regression.py --path diags/diag1000080`，producer 侧是在共享 2D Langmuir scaffold 上把 FFT-backed non-nodal 分叉切成 `Vay current deposition + PSATD`，而 shared consumer 则继续只对同一张末态 `diag1000080` 上的解析 `Ex/Ez` 施加 `<0.0503` gate，并额外命中 `analysis_utils.py` 的 `1e-3` 守恒 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_2d_langmuir_multi_psatd_momentum_conserving.json`：已把这条残留偏弱的 baseline 统一补成 source-grounded 强描述，明确写清它只会在 `WarpX_FFT` 打开时固定命中 `analysis_2d.py diags/diag1000080 + analysis_default_regression.py --path diags/diag1000080`，producer 侧是在共享 2D Langmuir scaffold 上把 FFT-backed 分叉切成 `momentum-conserving gather + PSATD`，而 shared consumer 则继续只对同一张末态 `diag1000080` 上的解析 `Ex/Ez` 施加 `<0.0503` gate，并且不会额外触发 `analysis_utils.py` 的守恒 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_2d_langmuir_multi_psatd_JRhom_LL2.json`：已把这条残留偏弱的 baseline 统一补成 source-grounded 强描述，明确写清它只会在 `WarpX_FFT` 打开时固定命中 `analysis_2d.py diags/diag1000080 + analysis_default_regression.py --path diags/diag1000080`，producer 侧是在共享 2D Langmuir scaffold 上把 FFT-backed non-nodal 分叉切成 `PSATD + JRhom_LL2 + first-order solution_type + update_with_rho`，而 shared consumer 则继续只对同一张末态 `diag1000080` 上的解析 `Ex/Ez` 施加 `<0.0503` gate，并且不会额外触发 `analysis_utils.py` 的守恒 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_2d_langmuir_multi_psatd_current_correction.json`：已把这条残留偏弱的 baseline 统一补成 source-grounded 强描述，明确写清它只会在 `WarpX_FFT` 打开时固定命中 `analysis_2d.py diags/diag1000080 + analysis_default_regression.py --path diags/diag1000080`，producer 侧是在共享 2D Langmuir scaffold 上把 FFT-backed non-nodal 分叉切成 `esirkepov + PSATD + current_correction + periodic_single_box_fft`，而 shared consumer 则继续只对同一张末态 `diag1000080` 上的解析 `Ex/Ez` 施加 `<0.0503` gate，并额外命中 `analysis_utils.py` 的 `1e-9` 守恒 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_2d_langmuir_multi_psatd_JRhom_LL2_nodal.json`：已把这条残留偏弱的 baseline 从残留 `checksum 基线` 起手补成统一的 source-grounded 强描述，明确写清它只会在 `WarpX_FFT` 打开时固定命中 `analysis_2d.py diags/diag1000080 + analysis_default_regression.py --path diags/diag1000080`，producer 侧是在共享 2D Langmuir scaffold 上把 FFT-backed nodal 分叉切成 `PSATD + JRhom_LL2 + first-order solution_type + update_with_rho + collocated grid`，而 shared consumer 则继续只对同一张末态 `diag1000080` 上的解析 `Ex/Ez` 施加 `<0.0503` gate，并且不会额外触发 `analysis_utils.py` 的守恒 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_2d_langmuir_multi_psatd_current_correction_nodal.json`：已把这条残留偏弱的 baseline 从残留 `checksum 基线` 起手补成统一的 source-grounded 强描述，明确写清它只会在 `WarpX_FFT` 打开时固定命中 `analysis_2d.py diags/diag1000080 + analysis_default_regression.py --path diags/diag1000080`，producer 侧是在共享 2D Langmuir scaffold 上把 FFT-backed nodal 分叉切成 `direct deposition + PSATD + current_correction + periodic_single_box_fft + collocated grid`，而 shared consumer 则继续只对同一张末态 `diag1000080` 上的解析 `Ex/Ez` 施加 `<0.0503` gate，并额外命中 `analysis_utils.py` 的 `1e-9` 守恒 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_2d_langmuir_multi_psatd_vay_deposition_particle_shape_4.json`：已把这条残留偏弱的 baseline 从一句旧式 `checksum 基线` 补成 source-grounded 强描述，明确写清它只会在 `WarpX_FFT` 打开时固定命中 `analysis_2d.py diags/diag1000080 + analysis_default_regression.py --path diags/diag1000080`，producer 侧是在共享 2D Langmuir scaffold 上把 FFT-backed 分叉切成 `Vay deposition + PSATD + particle_shape=4`，而 shared consumer 则把解析 `Ex/Ez` 的主 gate 从默认 `<0.0503` 放宽到 `<0.07`，随后继续施加 `analysis_utils.py` 的 `1e-3` 守恒 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_2d_langmuir_multi_psatd_nodal.json`：已把这条残留偏弱的 baseline 从一句旧式 `checksum 基线` 补成 source-grounded 强描述，明确写清它只会在 `WarpX_FFT` 打开时固定命中 `analysis_2d.py diags/diag1000080 + analysis_default_regression.py --path diags/diag1000080`，producer 侧是在共享 2D Langmuir scaffold 上把 FFT-backed 分叉切成 `direct deposition + PSATD + collocated grid`，而 shared consumer 则继续只对同一张末态 `diag1000080` 上的解析 `Ex/Ez` 施加 `<0.0503` gate，并且不会额外触发 `analysis_utils.py` 的守恒 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_2d_langmuir_multi_nodal.json`：已把这条残留偏弱的 baseline 从一句旧式 `checksum 基线` 补成 source-grounded 强描述，明确写清它当前固定命中 `analysis_2d.py diags/diag1000080 + analysis_default_regression.py --path diags/diag1000080`，producer 侧是在共享 2D Langmuir scaffold 上把 native 分叉切成 `direct deposition + collocated grid + selective particle output`，而 shared consumer 则继续只对同一张末态 `diag1000080` 上的解析 `Ex/Ez` 施加 `<0.0503` gate，并且不会额外触发 `analysis_utils.py` 的守恒 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_2d_langmuir_multi_mr_psatd.json`：已把这条残留偏弱的 baseline 从一句旧式 `checksum 基线` 补成 source-grounded 强描述，明确写清它只会在 `WarpX_FFT` 打开时固定命中 `analysis_2d.py diags/diag1000080 + analysis_default_regression.py --path diags/diag1000080`，producer 侧是在共享 2D Langmuir scaffold 上把 MR 分叉切成 `PSATD + max_level=1 + ref_ratio=4 + centered fine-tag box + use_filter=1 + psatd.current_correction=0`，而 shared consumer 则继续只对同一张末态 `diag1000080` 上的解析 `Ex/Ez` 施加 `<0.0503` gate，并且不会额外触发 `analysis_utils.py` 的守恒 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_2d_langmuir_multi_mr_maxlevel2.json`：已把这条残留偏弱的 baseline 从一句旧式 `checksum 基线` 补成 source-grounded 强描述，明确写清它当前固定命中 `analysis_2d.py diags/diag1000080 + analysis_default_regression.py --path diags/diag1000080`，producer 侧是在共享 2D Langmuir scaffold 上把 MR 分叉切成 `amr.max_level=2 + amr.ref_ratio=2 + centered fine-tag hierarchy + CKC + use_filter=1`，而 shared consumer 则继续只对同一张末态 `diag1000080` 上的解析 `Ex/Ez` 施加 `<0.0503` gate，并且不会额外触发 `analysis_utils.py` 的守恒 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_2d_langmuir_multi_mr_momentum_conserving.json`，并校正同组 `test_2d_langmuir_multi_mr.json` 的守恒描述：已把这条残留偏弱的 baseline 从一句旧式 `checksum 基线` 补成 source-grounded 强描述，明确写清它当前固定命中 `analysis_2d.py diags/diag1000080 + analysis_default_regression.py --path diags/diag1000080`，producer 侧是在共享 2D Langmuir scaffold 上把 MR 分叉切成 `momentum-conserving gather + CKC + max_level=1 + ref_ratio=4 + centered fine-tag box + use_filter=1`，而 shared consumer 则继续只对同一张末态 `diag1000080` 上的解析 `Ex/Ez` 施加 `<0.0503` gate；同时已根据当前本地源码把普通 `mr` 路径里误写成会触发 `divE-rho/epsilon_0` 守恒 gate 的描述收回。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_2d_langmuir_multi_mr_anisotropic.json`：已把这条残留偏弱的 baseline 从一句旧式 `checksum 基线` 补成 source-grounded 强描述，明确写清它当前固定命中 `analysis_2d.py diags/diag1000080 + analysis_default_regression.py --path diags/diag1000080`，producer 侧是在共享 2D Langmuir scaffold 上把 MR 分叉切成 `CKC + max_level=1 + ref_ratio_vect=4 2 + centered fine-tag box + use_filter=1` 的各向异性 refinement，而 shared consumer 则继续只对同一张末态 `diag1000080` 上的解析 `Ex/Ez` 施加 `<0.0503` gate，并复用同一层 shared post-hook。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_2d_langmuir_multi_mr.json`：已把这条残留偏弱的 baseline 从一句旧式 `checksum 基线` 补成 source-grounded 强描述，明确写清它当前固定命中 `analysis_2d.py diags/diag1000080 + analysis_default_regression.py --path diags/diag1000080`，producer 侧是在共享 2D Langmuir scaffold 上额外打开 `CKC + max_level=1 + ref_ratio=4 + centered fine-tag box + use_filter=1` 的 MR 分叉，而 shared consumer 则继续只对同一张末态 `diag1000080` 上的解析 `Ex/Ez` 施加 `<0.0503` gate；按当前本地源码，这条普通 MR 路径不会再额外触发 `analysis_utils.py` 的 `divE-rho/epsilon_0` 守恒检查。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_2d_ionization_lab_restart.json`：已把这条残留偏弱的 baseline 从一句旧式 `checksum 基线` 补成 source-grounded 强描述，明确写清它当前固定命中 `analysis.py diags/diag1001600 + analysis_default_regression.py --path diags/diag1001600 --rtol 1e-2`，producer 侧只是 `FILE = inputs_test_2d_ionization_lab + amr.restart = ../test_2d_ionization_lab/diags/chk001000` 的 restart overlay，而 shared consumer 仍继续只对同一张末态 `diag1001600` 上的 Chen-2013 `N5_fraction` 施加 `<7%` 相对误差 gate，并在属性存在时额外检查 `particle_orig_z`。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_2d_ionization_picmi.json`：已把这条残留偏弱的 baseline 从一句旧式 `checksum 基线` 补成 source-grounded 强描述，明确写清它当前固定命中 `analysis.py diags/diag1001600 + analysis_default_regression.py --path diags/diag1001600`，producer 侧把同一条 ADK nitrogen ionization 工作流全量搬到 `picmi.Cartesian2DGrid + Species + FieldIonization + GaussianLaser + in-process step()` 前端，而 shared consumer 则继续只对同一张末态 `diag1001600` 上的 Chen-2013 `N5_fraction` 施加 `<7%` 相对误差 gate，并在属性存在时额外检查 `particle_orig_z`。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_2d_ionization_lab.json`：已把这条残留偏弱的 baseline 从一句旧式 `checksum 基线` 补成 source-grounded 强描述，明确写清它当前固定命中 `analysis.py diags/diag1001600 + analysis_default_regression.py --path diags/diag1001600`，producer 侧是一张 `N^{2+}` slab + CKC laser + `orig_z` runtime attribute 的 native lab-frame 输入卡，而 shared consumer 则继续只对同一张末态 `diag1001600` 上的 Chen-2013 `N5_fraction` 施加 `<7%` 相对误差 gate，并在属性存在时额外检查 `particle_orig_z` 全部落在 `(0, 1.5e-5)`。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_2d_ionization_boost.json`：已把这条残留偏弱的 baseline 从一句旧式 `checksum 基线` 补成 source-grounded 强描述，明确写清它当前固定命中 `analysis.py diags/diag1000420 + analysis_default_regression.py --path diags/diag1000420`，producer 侧是一张 `moving window + gamma_boost=2 + continuous-injection electrons/ions + ADK nitrogen ionization + Gaussian laser` 的 boosted 输入卡，而 shared consumer 则继续只对同一张末态 `diag1000420` 上的 Chen-2013 `N5_fraction` 施加 `<7%` 相对误差 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_2d_dive_cleaning.json`：已把这条残留偏弱的 baseline 从一句旧式 `checksum 基线` 补成 source-grounded 强描述，明确写清它当前固定命中 `analysis.py diags/diag1000128 + analysis_default_regression.py --path diags/diag1000128`，producer 侧是一张 centered at-rest Gaussian-beam + `do_dive_cleaning` + `PML` 的 2D 输入卡，而 shared consumer 则在二维分支里把 `mesh Ez` 重命名成 `Ey`，只对最终 `diag1000128` 上的圆柱近似 Gaussian Coulomb 场 `Ex/Ey` 两分量施加 `atol = 0.1 * E_th.max()` gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_reduced_diags_load_balance_costs_timers_psatd.json`：已把这条残留偏弱的 baseline 从泛泛“checksum 基线”补成 source-grounded current-checkout 边界，明确写清它当前虽然仍受 `WarpX_FFT` gate 控制，但 producer 侧并没有真正切到 `psatd`，而只是继承 `inputs_base_3d` 的 `128 x 32 x 128` periodic Yee + `LoadBalanceCosts` runtime scaffold，并把唯一 runtime 分叉固定在 `algo.load_balance_costs_update = Timers`；shared consumer 则继续完全绕过 plotfile、只对 `LBC.txt` 上的 load-balance efficiency-improvement 主链施加断言。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_reduced_diags_single_precision.json`：已把这条残留偏弱的 baseline 从宽泛 legacy 摘要补成 source-grounded current-checkout 边界，明确写清它在当前本地 `warpx` checkout 里既没有 active `CMake` wiring，也没有单独的 single-precision wrapper / 输入卡 / checksum artifact，仅剩 `analysis_reduced_diags_impl.py` 里的 `single_precision=True` 容差分支。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_particle_fields_diags_single_precision.json`：已把这条残留偏弱的 baseline 从泛泛“计划中的单精度 checksum 基线”补成 source-grounded reserve 边界，明确写清它在当前本地 `warpx` checkout 里不是 active regression，而是 `particle_fields_diags/CMakeLists.txt` 里整段仍停在 `# FIXME` 注释块中的 reserve-only sibling；不过 `analysis_particle_diags_single.py` 这个单精度 wrapper 仍然存在，并继续把共享实现层容差放宽到 `5e-3`。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_langmuir_multi_psatd_single_precision.json`：已把这条残留偏弱的 baseline 从一句旧式 `checksum 基线` 补成 source-grounded legacy 边界，明确写清它在当前本地 `warpx` checkout 里既没有 active `CMake` wiring，也没有 `Examples/Tests/langmuir` 对应的单精度 `PSATD` 输入/analysis 残留，`Regression/Checksum` 本地树里也未找到同名 artifact，因此当前只能按文档索引层 legacy name 记录。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_langmuir_multi_single_precision.json`：已把这条残留偏弱的 baseline 从一句旧式 `checksum 基线` 补成 source-grounded legacy 边界，明确写清它在当前本地 `warpx` checkout 里既没有 active `CMake` wiring，也没有 `Examples/Tests/langmuir` 单精度输入/analysis 残留，`Regression/Checksum` 本地树里也未找到同名 artifact，因此当前只能按文档索引层 legacy name 记录。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_rz_deuterium_tritium_fusion.json`：已把这条残留偏弱的 baseline 从一句 `checksum 基线` 补成 source-grounded 强描述，明确写清它当前固定命中 `analysis_two_product_fusion.py diags/diag1000001 + analysis_default_regression.py --path diags/diag1000001`，producer 侧是一张并排 materialize `2` 组 RZ `D+T -> He4+n` 子场景的输入卡，而 shared consumer 则会同时对初末态施加守恒、理论 fusion macroparticle 数、slice-by-slice yield、`xy` 各向同性分支和全域 `rho` 守恒断言。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_electrostatic_sphere_adaptive.json`：已把这条残留偏弱的 baseline 从半弱的 `checksum 基线` 摘要补成 source-grounded 强描述，明确写清它当前固定命中 `analysis_electrostatic_sphere.py diags/diag1000054 + analysis_default_regression.py --path diags/diag1000054`，producer 侧是一张 `adaptive dt + relativistic electrostatic` 的均匀电子球输入卡，`timestep` reduced diag 当前只停在 producer-side side channel，而 shared consumer 则继续只对最终 `diag1000054` 上按真实 `t_max` 反求 `r_end` 后的 `Ex/Ey/Ez` 三轴解析场 `L2 < 0.05` 合同施加 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_dive_cleaning.json`：已把这条残留偏弱的 baseline 从一句 `checksum 基线` 补成 source-grounded 强描述，明确写清它当前固定命中 `analysis.py diags/diag1000128 + analysis_default_regression.py --path diags/diag1000128`，producer 侧是一张 centered at-rest Gaussian-beam + `do_dive_cleaning` + `PML` 的输入卡，而 shared consumer 则只对最终 `diag1000128` 上的 Gaussian-beam 理论 Coulomb 场 `Ex/Ey/Ez` 三分量施加 `atol = 0.165 * E_th.max()` gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_divb_cleaning.json`：已把这条残留偏弱的 baseline 从一句 `checksum 基线` 补成 source-grounded 强描述，明确写清它当前固定命中 `analysis.py diags/diag1000400 + analysis_default_regression.py --path diags/diag1000400`，producer 侧会显式落出 `diag1000398/399/400` 三张连续 snapshot，而 shared consumer 则只对这三帧上的离散 `c^2 div(B) = dG/dt` 关系施加 `<1e-1` gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_diff_lumi_diag_photons.json`：已把这条残留偏弱的 baseline 从一句 `checksum 基线` 补成 source-grounded 强描述，明确写清它当前固定命中 `analysis.py + analysis_default_regression.py --path diags/diag1000080 --rtol 1e-2`，producer 侧把双束前端切到 `photon + parse_density_function + NUniformPerCell`，而 shared consumer 则继续只对 `1D dL/dE txt + 2D d^2L/dE_1dE_2 openPMD` 双谱施加更宽的 `2.1% / 6%` 解析对照 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_diff_lumi_diag_leptons_mr.json`：已把这条残留偏弱的 baseline 从一句 `checksum 基线` 补成 source-grounded 强描述，明确写清它当前固定命中 `analysis.py + analysis_default_regression.py --path diags/diag1000080 --rtol 1e-2`，producer 侧是在普通 `electron/positron gaussian_beam + q_tot` 双束骨架上额外打开 centered level-1 collision-region refinement，而 shared consumer 则继续只对 `1D dL/dE txt + 2D d^2L/dE_1dE_2 openPMD` 双谱施加同一组 `2% / 4%` 解析高斯对照 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_diff_lumi_diag_leptons.json`：已把这条残留偏弱的 baseline 从一句 `checksum 基线` 补成 source-grounded 强描述，明确写清它当前固定命中 `analysis.py + analysis_default_regression.py --path diags/diag1000080 --rtol 1e-2`，producer 侧是一张 `electron/positron gaussian_beam + q_tot` 双束输入卡，而 shared consumer 则完全绕过 plotfile、本体只对 `1D dL/dE txt + 2D d^2L/dE_1dE_2 openPMD` 双谱施加 `2% / 4%` 解析高斯对照 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_deuterium_deuterium_fusion_intraspecies.json`：已把这条残留偏弱的 baseline 从一句 `checksum 基线` 补成 source-grounded 强描述，明确写清它当前固定命中 `analysis_deuterium_deuterium_3d_intraspecies.py + analysis_default_regression.py --path diags/diag1000010`，producer 侧是一张 `20 keV` 的 3D thermal deuterium intraspecies 输入卡，而主 consumer 则完全绕过粒子 plotfile、只对 `reduced_diags/particle_number.txt` 反解出来的 Bosch-Hale thermal reactivity 施加 `<2%` gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_deuterium_deuterium_fusion.json`：已把这条残留偏弱的 baseline 从一句 `checksum 基线` 补成 source-grounded 强描述，明确写清它当前固定命中 `analysis_two_product_fusion.py diags/diag1000001 + analysis_default_regression.py --path diags/diag1000001`，producer 侧是一张单组 `D+D -> He3+n` center-of-mass 扫能切片输入卡，而 shared consumer 则会同时对初末态施加守恒、各向同性、理论 fusion macroparticle 数、slice-by-slice yield 和全域 `rho` 守恒断言。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_deuterium_tritium_fusion.json`：已把这条残留偏弱的 baseline 从一句 `checksum 基线` 补成 source-grounded 强描述，明确写清它当前固定命中 `analysis_two_product_fusion.py diags/diag1000001 + analysis_default_regression.py --path diags/diag1000001`，producer 侧是一张并排 materialize `2` 组 `D+T -> He4+n` 子场景的输入卡，而 shared consumer 则会同时对初末态施加守恒、各向同性、理论 fusion macroparticle 数、slice-by-slice yield 和全域 `rho` 守恒断言。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_2d_proton_boron_fusion.json`：已把这条残留偏弱的 baseline 从一句 `checksum 基线` 补成 source-grounded 强描述，明确写清它当前固定命中 `analysis_proton_boron_fusion.py diags/diag1000001 + analysis_default_regression.py --path diags/diag1000001`，producer 侧是一张并排 materialize `5` 组 `p-B11` 子场景的输入卡，而 shared consumer 则会同时对初末态施加守恒、三 alpha packing、理论 yield、thermal reactivity 和 `probability_threshold` 欠产额分支断言。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_2d_pec_field_insulator_implicit{,_restart}.json`：已把这两条残留偏弱的 baseline 从旧式一句话摘要补成 source-grounded 强描述，明确写清主线当前固定命中 `analysis_pec_insulator_implicit.py diags/diag1000020 + analysis_default_regression.py --path diags/diag1000020`，真正主合同是 `fieldenergy + poyntingflux` 的 `<1e-13` reduced-energy accounting，而 restart 变体新增的 runtime 分叉只剩 `chk000010 -> step 20` continuation。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_2d_pec_field_insulator.json`：已把这条残留偏弱的 baseline 从一句 `checksum 基线` 补成 source-grounded 强描述，明确写清它当前固定命中 `analysis=OFF + analysis_default_regression.py --path diags/diag1000010`，producer 侧是 `x_hi` 局部窗口上的 `pec_insulator` 显式 `B_y` 边界驱动 scaffold，而唯一自动消费者则只剩末态 `diag1000010` 的 checksum。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_pmc_field.json`：已把这条残留偏弱的 baseline 从一句 `checksum 基线` 补成 source-grounded 强描述，明确写清它当前固定命中 `analysis_pec.py diags/diag1000134 + analysis_default_regression.py --path diags/diag1000134`，producer 侧是在局部 parser `Ey/Bx` 外加正弦波包 scaffold 上切到 `periodic periodic pmc` 边界，而主 consumer 则只对末态全域 `Ey` 的 `±2E_in` standing-wave 振幅翻倍合同施加 `1%` gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_pec_particle.json`：已把这条残留偏弱的 baseline 从一句 `checksum 基线` 补成 source-grounded 强描述，明确写清它当前固定命中 `analysis=OFF + analysis_default_regression.py --path diags/diag1000020`，producer 侧是两颗贴近 `x_hi` PEC 边界的等质量重粒子最小 gather/deposition scaffold，而唯一自动消费者则只剩末态 `Ex/Ey/Ez/Bx/By/Bz/jx/jy/jz` 的 checksum。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_pec_field_mr.json`：已把这条残留偏弱的 baseline 从一句 `checksum 基线` 补成 source-grounded 强描述，明确写清它当前固定命中 `analysis_pec_mr.py diags/diag1000125 + analysis_default_regression.py --path diags/diag1000125`，producer 侧是在单级 `Ey/Bx` 外加正弦波包 scaffold 上切到 `level-1 refined cube`，而主 consumer 则仍只对末态 `level-0` 全域 `Ey` 的 `±2E_in` standing-wave 振幅翻倍合同施加 `5%` gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_pec_field.json`：已把这条残留偏弱的 baseline 从一句 `checksum 基线` 补成 source-grounded 强描述，明确写清它当前固定命中 `analysis_pec.py diags/diag1000125 + analysis_default_regression.py --path diags/diag1000125`，producer 侧是局部 parser `Ey/Bx` 外加正弦波包 + `periodic periodic pec` 边界，而主 consumer 则只对末态全域 `Ey` 的 `±2E_in` standing-wave 振幅翻倍合同施加 `1%` gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_particle_scrape.json`：已把这条残留偏弱的 native baseline 从一句 `checksum 基线` 补成 source-grounded 强描述，明确写清它当前固定命中 `analysis_scrape.py diags/diag1000060 + analysis_default_regression.py --path diags/diag1000060`，producer 侧是 3D cubic-EB 前冲电子 slab，而主 consumer 则只对 `diag1000040 -> diag1000060` 两张 snapshot 上的 `612 -> 0` 主容器删粒子合同施加硬断言。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_photon_pusher.json`：已把这条残留偏弱的 baseline 从一句 `checksum 基线` 补成 source-grounded 强描述，明确写清它当前固定命中 `analysis.py diags/diag1000050 + analysis_default_regression.py --path diags/diag1000050`，producer 侧是 `8 个方向 × 2 档动量幅值` 的 `16` 个单光子矩阵，而主 consumer 则只对全局最坏 `disc_pos/disc_mom` 施加 `1e-14 / eps` 直线传播与动量守恒 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_plasma_lens_hard_edged`：已把这条仍偏弱的 baseline 从一句 `checksum 基线` 补成 source-grounded 强描述，明确写清它当前真正新增的是 `lattice.elements + plasmalens*.type = plasmalens` 的 accelerator-lattice 前端分叉，而 shared `analysis.py` 会把这条 lattice 序列折回同构 lens-chain 语义后继续对末态 `x/y/ux/uy` 施加 `2% / 0.2%` gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `subcycling family summary`：已把 shared checksum helper、单张输入卡与唯一 active baseline 再压成 `single active baseline + final-plotfile checksum-only consumer chain + MR subcycling / plasma-on-main-grid producer scaffold` 的更高层结构，并写清当前 family 已稳定收敛成单条 `2D CKC + MR subcycling + moving window + continuous-injection plasma deposited on main grid` regression，而自动回归边界只压在 `diag1000250` checksum 上。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `silver_mueller family summary`：已把 shared `analysis.py`、checksum helper、四张输入卡与四条 active baseline 再压成 `4 active baselines + shared same-final-plotfile additive checksum wrapper + shared full-domain residual-field main consumer + 1/2/1 geometry-direction split` 的更高层结构，并写清当前 family 已稳定收敛成 `1D / 2D-x / 2D-z / RZ-z` 四条 active Silver-Mueller regression 共用 `diag1000500` 与全域残余场阈值主消费者链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `secondary_ion_emission family summary`：已把 shared `analysis.py`、checksum helper、单条输入脚本与唯一 active baseline 再压成 `single active baseline + same-directory openPMD additive checksum wrapper + scrape-buffer callback runtime chain + final-electron back-propagation main consumer` 的更高层结构，并写清当前 family 已稳定收敛成单条 `RZ PICMI spherical-EB secondary-emission` regression：前端是 `ParticleBoundaryBufferWrapper()` 驱动的 `afterstep` 次级发射注入链，后端是同目录 openPMD 末态电子反向几何匹配主消费者，再叠加 checksum。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `laser_on_fine family summary`：已把 checksum helper、单条输入卡与唯一 active baseline 再压成 `single active baseline + final-plotfile checksum-only consumer chain + AMR/PML laser-placement producer scaffold` 的更高层结构，并写清当前 family 已稳定收敛成单条 `2D laser-antenna-on-fine-patch` regression 只把自动回归边界压在 `diag1000050` checksum 上，而 `AMR fine patch + z向PML + Gaussian laser antenna` 仍都停在 runtime scaffold 这一层。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `rigid_injection family summary`：已把两条 analysis、checksum helper、两张输入卡与两条 active baseline 再压成 `2 active baselines + 1+1 mixed split + separated additive checksum surfaces` 的更高层结构，并写清当前 family 已稳定收敛成 `BTD` 分支的 `plotfile/openPMD dual-BTD particle consistency + lab-frame beam-width` 主链，与 `lab` 分支的 `final beam-width + initial runtime-attribute materialization` 主链，再分别叠加 `diag1000001` 与 `diag1000289` 两张 checksum surface。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `larmor family summary`：已把 checksum helper、单条输入卡与唯一 active baseline 再压成 `single active baseline + final-plotfile checksum-only consumer chain + raw/full diagnostics side producer scaffold` 的更高层结构，并写清当前 family 已稳定收敛成单条 `2D external-By gyro-motion` regression 只把自动回归边界压在 `diag1000010` checksum 上，而 MR/PML/raw-full diagnostics 仍都停在 producer side。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `accelerator_lattice umbrella summary`：已把 shared `analysis.py`、checksum helper、三张输入卡与三条 active baseline 再压成 `3 active baselines + shared same-final-plotfile additive checksum wrapper + shared final-particle quadrupole-chain main consumer + 1/1/1 runtime split` 的更高层结构，并写清当前 family 已稳定收敛成三条 active 3D hard-edged quadrupole regression 共用同一张 `diag1000050` 末态 plotfile、同一条单粒子解析透镜主消费者链，再按 `lab / boosted / moving-window` 做 runtime 分叉。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `ionization_dsmc umbrella summary`：已把多条 `analysis_*.py`、checksum helper、1D/3D 输入骨架与六条 active baseline 再压成 `6 active baselines + shared mixed checksum wrapper + 4/2 checksum-surface split + 4+1+1 analysis-state split` 的更高层结构，并写清当前 family 已稳定收敛成 `4` 条 1D reaction-specific strong branches、`1` 条 3D electron-impact strong branch、`1` 条 3D ion-impact checksum-only branch。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `ion_stopping umbrella summary`：已把 shared `analysis.py`、checksum helper、单条 active baseline 与四路径 background-stopping 输入骨架再压成 `single active baseline + same-final-plotfile additive checksum sibling + initial/final plotfile coupled stopping-replay main consumer` 的更高层结构，并写清当前 family 已稳定收敛成 `diag1000000 -> 10-step slowing-down replay -> diag1000010` 的初末两帧耦合主消费者链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `initial_distribution umbrella summary`：已把 shared `analysis.py`、checksum helper、单条 active baseline 与九组初始化输入骨架再压成 `single active baseline + separate final-plotfile additive checksum side surface + reduced-histogram/beam-monitor multi-distribution main consumer` 的更高层结构，并写清当前 family 已稳定收敛成 `九类初始化分布逐项解析闭合` 的强消费者链，加分离的 `diag1000001` 末态 plotfile checksum。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `field_ionization umbrella summary`：已把 shared `analysis.py`、checksum helper、四条 active baseline 与 lab/boost/restart/PICMI 输入骨架再压成 `4 active regressions + shared Chen-2013 N5_fraction main consumer + shared additive checksum wrapper + 1/3 output-surface split + 1/1/1/1 producer split` 的更高层结构，并写清当前 family 已稳定收敛成四条 active 2D ionization branch 共用同一条 Chen-2013 `N5_fraction` 主消费者链，再叠加 checksum wrapper。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `diff_lumi_diag umbrella summary`：已把 shared `analysis.py`、checksum helper、共享 base 输入与三条 `WarpX_FFT` gated baseline 再压成 `3 WarpX_FFT-gated active baselines + shared same-final-plotfile additive checksum sibling + reduced-ledger/openPMD dual-spectrum main consumer + 2+1 producer split` 的更高层结构，并写清当前 family 已稳定收敛成 `1D DifferentialLuminosity txt + 2D DifferentialLuminosity2D openPMD` 双谱解析主消费者链，加同一张 `diag1000080` 末态 plotfile checksum sibling。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `field_probe umbrella summary`：已把 shared `analysis.py`、checksum helper、单条 `WarpX_EB` gated baseline 与 2D single-slit 输入卡再压成 `single WarpX_EB-gated active baseline + shared same-final-plotfile additive checksum sibling + reduced-text line-probe diffraction main consumer` 的更高层结构，并写清当前 family 已稳定收敛成 `FP_line.txt` `step=500` 单缝 `sinc^2` 包络主消费者链，加同一张 `diag1000544` 末态 plotfile checksum sibling。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `point_of_contact_eb family summary`：已把 shared `analysis.py`、checksum helper、`3D/RZ` 两条 active baseline 与两张输入卡再压成 `2 WarpX_EB-gated active baselines + shared BoundaryScraping main consumer + shared same-directory checksum sibling + 1/1 geometry split` 的更高层结构，并写清当前 family 已稳定收敛成 `3D sphere + RZ cylinder` 两条 active EB baseline 共用同一条 `BoundaryScraping` 解析接触几何主消费者链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `projection_div_cleaner umbrella summary`：已把 shared `analysis.py`、checksum helper、`2D analytic / 3D file-backed / 3D callback / RZ` 四条 active regression 与相邻输入脚本再压成 `4 active regressions + shared checksum wrapper + 1/3 checksum-surface split + 1/3 main-consumer split` 的更高层结构，并写清当前 family 已稳定收敛成 `1` 条 `RZ + shared analysis.py` raw-auxiliary-field 主链，加 `3` 条脚本内 projection-cleaner `divB` 强断言 sibling。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `python_wrappers family summary`：已把 checksum helper、单条 `WarpX_FFT` gated baseline 与 PICMI 输入脚本再压成 `single WarpX_FFT-gated active baseline + final-plotfile checksum outer surface + in-process field-wrapper/PML-split main contract` 的更高层结构，并写清当前 family 已稳定收敛成 `diag1000100` outer checksum surface，加输入脚本内对 valid-domain `E/B/F/G` 与 PML split-field `pml_E/B/F/G` wrappers 的逐 component benchmark asserts。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `restart_eb family summary`：已把 active checksum helper、reserve-only restart helper、共享 `EB + PICMI + checkpoint/resume` 输入脚本与 active/FIXME wiring 再压成 `1 WarpX_EB-gated active baseline + 1 reserve-only FIXME restart sibling + shared diag1000060 output surface + single-script checkpoint/resume scaffold` 的更高层结构，并写清当前 family 已稳定分成 `active checksum-only mainline + reserve-only restart reproducibility sibling`。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `pass_mpi_communicator family summary`：已把 reserve-only baseline、shared checksum helper、offline `analysis.py` 与 split-communicator 输入脚手架再压成 `single reserve-only baseline + unwired checksum helper + dormant two-plotfile checksum-diff oracle + split-communicator producer scaffold` 的更高层结构，并写清当前 family 已稳定停在 `harness materialized but handoff/run/assert path still commented out` 的 reserve-only 状态。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `restart umbrella summary`：已把 shared checksum helper、`analysis_default_restart.py`、常开/FFT-gated/restart reserve 节点与 shared producer scaffold 再压成 `4 always-active baselines + 4 WarpX_FFT-gated baselines + 1 reserve-only FIXME sibling + shared diag1000010 checksum surface + 2/3/4 analysis-state split` 的更高层结构，并写清当前 family 已稳定收敛成 `2D runtime-component checksum-only siblings`、`3D restart reproducibility pairs` 与 `1` 条 reserve-only PICMI restart 节点。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `particle_fields_diags family summary`：已把 shared helper、双精度/单精度 analysis wrappers、共享实现层与 producer/baseline wiring 再压成 `1 active baseline + 1 reserve-only FIXME sibling + shared diag1000200 output surface + dual-writer handmade-reconstruction main consumer` 的更高层结构，并写清当前 family 已稳定收敛成 active 双精度 plotfile/openPMD 双 writer 强对照分支，加 reserve-only 单精度 sibling。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `particle_data_python family summary`：已把 checksum helper、两条 `particle_attr_access` twin baselines、`prev_positions` baseline 与两张输入脚本再压成 `3 active baselines + shared diag1000010 checksum-only surface + 2+1 script-local runtime-assert split` 的更高层结构，并写清当前 family 已稳定收敛成 `newPid/add_particles/deposit_current` runtime wrapper 自断言链，加 `prev_x/prev_z` runtime attributes 自断言链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `resampling umbrella summary`：已把 shared `analysis.py`、`analysis_default_regression.py`、三张输入卡与 `1D/2D` 三条 active baseline 再压成 `3 active baselines + shared checksum wrapper + 2+1 analysis-state split + 2/1 checksum-surface split` 的更高层结构，并写清当前 family 已稳定收敛成 `2` 条 velocity-coincidence checksum-only sibling，加 `1` 条 dual-species leveling-thinning strong-analysis sibling。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `particles_in_pml umbrella summary`：已把 `analysis_particles_in_pml.py`、`analysis_default_regression.py`、四张 native 输入卡与 `2D/3D × single-level/MR` 四条 active baseline 再压成 `4 active baselines + shared additive checksum wrapper + 2/2 geometry-AMR main-consumer split + 1/1/1/1 checksum-surface split` 的更高层结构，并写清当前 family 已稳定收敛成 finest-level 全域残余 `Ex/Ey/Ez` 主消费者链，加四张彼此分离的末态 checksum surface。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `particle_thermal_boundary family summary`：已把 `analysis.py`、`analysis_default_regression.py`、输入卡与单条 active baseline 再压成 `single active baseline + separate final-plotfile checksum side surface + reduced-energy main-consumer sibling` 的更高层结构，并写清当前 family 已稳定收敛成 `EF.txt + EN.txt` reduced-energy 主链加独立 `diag1002000` checksum side surface。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `particle_boundary_scrape family summary`：已把 `analysis_scrape.py`、`analysis_default_regression.py`、native/PICMI 两条输入路径与两条 active baseline 再压成 `2 WarpX_EB-gated active baselines + shared same-final-plotfile additive checksum wrapper + shared dual-snapshot main consumer + 1 native / 1 PICMI runtime split` 的更高层结构，并写清当前 family 已稳定收敛成 `native + PICMI` 共用 `612 -> 0` dual-snapshot 主链，而 PICMI 分支额外再挂 `ParticleBoundaryBufferWrapper` 的 `size/step/weight/clear` 自断言。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `particle_boundary_process family summary`：已把 `analysis_absorption.py`、`analysis_default_regression.py`、两条输入路径与两条 active baseline 再压成 `2 active baselines + 1+1 mixed split + separated checksum surfaces` 的更高层结构，并写清当前 family 已稳定收敛成 `2D PICMI boundary-buffer self-assert + checksum` 分支和 `3D dual-snapshot EB absorption analysis + checksum` 分支。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `single_particle family summary`：已把 `analysis.py`、`analysis_synchronize_velocity.py`、`analysis_default_regression.py`、两条输入卡与两条 active baseline 再压成 `2 active baselines + 1 active checksum branch + 1 analysis-only sibling` 的更高层结构，并写清当前 family 已稳定收敛成 `same-final-plotfile bilinear-filter + additive checksum` 分支和 `analysis-only synchronized-u_z` 分支。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `repelling_particles` family summary：已把 `analysis.py`、checksum helper、单条 baseline 与输入卡 wiring 再压成 `single active baseline + same-final-plotfile additive checksum wrapper + full-time-series beta(d) main consumer sibling` 的更高层结构，并写清当前主 analysis 不是单帧末态，而是由 `diag1000200` 反解整段 `diag10000*` 时序后做双单粒子能量账本断言。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `relativistic_space_charge_initialization` family summary：已把 `analysis.py`、checksum helper、单条 baseline 与输入卡 wiring 再压成 `single active baseline + same-final-plotfile fields-only additive checksum wrapper + relativistic Gaussian-beam Ex main consumer + By plot-only side field` 的更高层结构，并明确写清当前自动 gate 实际只落在 `Ex`，`By` 目前只停在 side visualization。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `reduced_diags umbrella summary`：已把 `analysis_reduced_diags.py`、`analysis_reduced_diags_impl.py`、`analysis_reduced_diags_load_balance_costs.py`、checksum helper、`test_3d_reduced_diags` 主干与 `load_balance_costs` 四条 sibling 再压成 `5 active regressions + shared additive checksum wrapper + 1/4 checksum-surface split + 1/3/1 main-consumer split + WarpX_FFT-gated legacy-name tail` 的更高层结构，并写清当前 family 已稳定收敛成 `compact-observable cross-check` 主干分支与 `LBC.txt` load-balance-costs sibling 分支。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `laser_injection_from_file umbrella summary`：已把 `analysis_{1d,1d_boost,2d,2d_binary,3d,rz,from_RZ_file}.py`、checksum helper、7 条 prepare-only upstream、7 条 active regression 与相邻输入路径再压成 `7 active regressions + 7 prepare-only upstream producers + shared additive checksum wrapper + 3/1/1/1/1 checksum-surface split + 4/1/1/1 consumer-family split` 的更高层结构，并写清当前 family 已稳定收敛成 `Gaussian Cartesian/RZ`、`boosted`、`legacy binary`、`RZ Laguerre/thetaMode` 四组主消费者链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `laser_injection umbrella summary`：已把 `analysis_1d.py`、`analysis_2d.py`、占位 `analysis_3d.py`、checksum helper、`1D/2D/3D + implicit` 五条 baseline 与相邻输入卡 wiring 再压成 `5 active baselines + shared additive checksum wrapper + 4/1 checksum-surface split + 2/2/1 analysis-state split + native/implicit runtime sibling` 的更高层结构，并写清当前 family 已稳定收敛成 `1D strong`、`2D strong` 与 `3D placeholder+checksum-main` 三组消费者状态。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `langmuir umbrella summary`：已把大批 `1D/2D/3D/RZ/radial` baseline、shared `analysis_{1d,2d,3d,r1d,rz}.py`、`analysis_utils.py` 与 checksum helper 再压成 `40 active baselines + shared additive checksum wrapper + 24/16 checksum-surface split + 1/18/14/5/2 geometry split + 37/1/2 analysis-state split` 的更高层结构，并写清当前 family 已稳定收敛成 `post-run shared analyses`、`RZ PICMI in-process assert` 与 `2D/3D PICMI checksum-only` 三态分叉。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `space_charge_initialization umbrella summary`：已把 shared `analysis.py`、checksum helper、`2D/3D` 两条输入卡与两条 baseline 说明再压成 `2 active baselines + shared same-final-plotfile fields-only additive checksum wrapper + 1+1 dimensional Gaussian-Coulomb main-consumer split` 的更高层结构，并写清当前 family 已稳定收敛成 `2D transverse-Coulomb` 与 `3D three-component Coulomb` 两条主消费者链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `gaussian_beam umbrella summary`：已把 `analysis_focusing_beam.py`、`analysis_rotated_beam.py`、悬空 `analysis.py` target、checksum helper、shared prepare upstream、六条 active regression 与相邻输入路径再压成 `6 active regressions + 1 prepare-only upstream producer + shared additive checksum wrapper + 5/1 checksum-surface split + 4/1/1 analysis-state split` 的更高层结构，并写清当前 family 已稳定收敛成 `closed-main`、`dangling-main`、`checksum-only` 三态分叉。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `electrostatic_sphere_eb umbrella summary`：已把 `analysis.py`、`analysis_rz.py`、`analysis_rz_mr.py`、checksum helper、五条输入路径与五条 baseline 说明再压成 `5 WarpX_EB-gated baselines + additive checksum wrapper + 3/2 checksum-surface split + 2/1/1/1 main-consumer split` 的更高层结构，并写清当前 family 已稳定收敛成 `3D ChargeOnEB+eb_covered`、`mixed_bc checksum-only`、`RZ analytic phi/Er` 与 `RZ+MR patchwise phi/Er` 四组主消费者链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `embedded_boundary_cube umbrella summary`：已把 `analysis_fields_2d.py`、`analysis_fields.py`、checksum helper、`2D/3D/macroscopic` 三条输入路径与三条 baseline 说明再压成 `3 WarpX_EB-gated baselines + shared additive checksum wrapper + 1/2 output-surface split + 1/2 geometry/runtime main-consumer split` 的更高层结构，并写清当前 family 已稳定收敛成 `2D By-only square-cavity` 与 `3D/3D-macroscopic shared By/Bz cubic-cavity` 两条主消费者链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `embedded_boundary_diffraction umbrella summary`：已把 checksum helper、单条输入卡与单条 baseline 说明再压成 `single WarpX_EB-gated baseline + same-directory openPMD additive checksum wrapper + iteration-300 first-minimum Airy main-consumer sibling` 的更高层结构，并写清当前 family 已稳定收敛成单条 `RZ cylindrical-aperture diffraction` 强消费者链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `embedded_boundary_em_particle_absorption umbrella summary`：已把 shared `analysis.py`、checksum helper、`2D/3D/RZ` 多条输入卡与多条 baseline 说明再压成 `9 WarpX_EB-gated active regressions + shared diag1 additive checksum sibling + 3/3/3 geometry split + geometry-branch time-averaged divE main consumer` 的更高层结构，并写清当前 family 已稳定收敛成 `2D/3D/RZ` 三组无静态伪电荷主链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `embedded_boundary_python_api umbrella summary`：已把 checksum helper、单条输入脚本与单条 baseline 说明再压成 `single WarpX_EB-gated baseline + plotfile-only checksum outer surface + in-process edge_lengths/face_areas geometry main contract` 的更高层结构，并写清当前 family 已稳定收敛成单条 `3D PICMI ECT + EmbeddedBoundary` wrapper 几何强断言路径。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `embedded_boundary_rotated_cube umbrella summary`：已把 checksum helper、`analysis_fields_{2d,3d}.py`、两条输入卡与两条 baseline 说明再压成 `2 WarpX_EB-gated baselines + shared additive checksum wrapper + 1/1 output-surface split + 1/1 geometry main-consumer split` 的更高层结构，并写清当前 family 已稳定收敛成 `2D rotated square cavity` 与 `3D rotated cubic cavity` 两条主分析路径。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `divb_cleaning umbrella summary`：已把 shared `analysis.py`、checksum helper、单条输入卡与单条 baseline 说明再压成 `single active baseline + same-final-plotfile additive checksum wrapper + tri-frame divB/G evolution main consumer sibling` 的更高层结构，并写清当前 family 已稳定收敛成单条 `3D hyperbolic magnetic-divergence cleaning` 强消费者链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `dive_cleaning umbrella summary`：已把 shared `analysis.py`、checksum helper、两条输入卡与两条 baseline 说明再压成 `2 active baselines + shared same-final-plotfile additive checksum wrapper + 1+1 dimensional Gaussian-field main-consumer split` 的更高层结构，并写清当前 family 已稳定收敛成 `2D cylindrical` 与 `3D spherical` 两条理论场分叉。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `electrostatic_dirichlet_bc umbrella summary`：已把 shared `analysis.py`、checksum helper、两条输入脚本与两条 baseline 说明再压成 `2 active baselines + same-final-plotfile additive checksum wrapper + whole-series boundary-phi main consumer sibling + 1+1 frontend split` 的更高层结构，并写清当前 family 已稳定收敛成 `native parser` 与 `PICMI boundary-potential` 两条前端分叉。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `effective_potential_electrostatic umbrella summary`：已把 shared `analysis.py`、checksum helper、单条输入脚本与单条 baseline 说明再压成 `single active baseline + same-directory openPMD additive checksum wrapper + sim-parameter-sidecar / whole-series radial-density main consumer sibling` 的更高层结构，并写清当前 family 已稳定收敛成单条 `3D PICMI effective-potential electrostatic` strong branch。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `electrostatic_sphere umbrella summary`：已把 shared `analysis_electrostatic_sphere.py`、checksum helper、7 条 baseline 说明与相邻输入卡 wiring 再压成 `7 active baselines + shared exact self-field-expansion main consumer + additive checksum sibling + 5/1/1 checksum-surface split + 3/1/3 analysis-state split` 的更高层结构，并写清当前 family 已稳定收敛成 `phi-enabled lab-frame`、`emass_10 relaxed-L2` 与 `relativistic/collocated/adaptive field-only` 三组主消费者分叉。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `collision umbrella summary`：已把 `1D/2D/3D/RZ Coulomb`、`pulsed_decay`、`fusion`、`DSMC split momentum push` 等多条 baseline 说明再压成 `15 active baselines + unified checksum wrapper + multi-family main-consumer split` 的更高层结构，并写清当前 family 已稳定收敛成多条 reduced / time-series / final-plotfile 主消费者链并列、再统一叠加 checksum wrapper 的 umbrella 形态。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `laser_acceleration umbrella summary`：已把 native / PICMI / boosted / MR / RZ / Python callback 多条 baseline 说明再压成 `14 active baselines + unified checksum wrapper + 3 + 11 service split + 3/1/1/3/4/2 output-surface split` 的更高层结构，并写清当前 family 已稳定收敛成 `1D fluid boosted`、`2D refined injection`、`RZ openPMD diagnostics` 三条强 analysis 分支和其余 checksum-only workflow。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `flux_injection umbrella summary`：已把 `3D standard`、`RZ standard`、`2D/3D/RZ from-EB` 五条 baseline 说明再压成 `5 active baselines + shared additive checksum wrapper + 1/1/3 analysis-family split + 1/1/3 output-surface split` 的更高层结构，并写清当前 family 已稳定收敛成 `3D distribution`、`RZ radius+flux`、`2D/3D/RZ embedded-boundary emission` 三组主消费者链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `uniform_plasma umbrella summary`：已把 `2D`、`3D non-restart`、`3D restart` 三条 baseline 说明再压成 `3 active baselines + shared diag1000010 final-plotfile surface + 2 + 1 mixed consumer split` 的更高层结构，并写清当前 family 已稳定收敛成 `2` 条 checksum-only mainline 与 `1` 条 restart reproducibility strong branch。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `virtual_photons umbrella summary`：已把 `analysis_virtual_photons.py`、`analysis_beamsize_effect.py`、checksum helper 与两条单基线说明再压成 `2 active baselines + same-directory openPMD additive checksum wrapper + 1/1 virtual-photon consumer split` 的更高层结构，并写清当前 family 已稳定收敛成 `yield+spectrum+position` 与 `beam-size smearing geometry` 两条主消费者链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `qed umbrella summary`：已把 `Breit-Wheeler yt/openPMD`、`Quantum Sync`、`Schwinger` 几组并列条目再压成 `10 active baselines + 3 writer surfaces + 4 shared main-consumer branches + additive checksum sibling` 的更高层结构，并写清当前 family 已稳定收敛成 `2/2/2/4` 的 `Breit-Wheeler plotfile / Breit-Wheeler openPMD / Quantum Sync / Schwinger` split。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `laser_ion family summary`：已把 shared `analysis_test_laser_ion.py`、checksum helper、两条输入脚本与两条 baseline 说明再压成 `2 active baselines + same-directory openPMD additive checksum wrapper + 1+1 native/PICMI mixed split` 的更高层结构，并写清当前 family 已稳定收敛成 `native physics-gated` 与 `PICMI wiring-attached-but-skipped` 两支分叉。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `plasma_mirror umbrella summary`：已把 checksum helper、单条输入卡与单条 baseline 说明再压成 `single active baseline + final-plotfile checksum-only consumer chain` 的更高层结构，并写清当前 family 已稳定收敛成单条 `2D native laser-solid` smoke regression。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `photon_pusher umbrella summary`：已把 shared `analysis.py`、checksum helper、单条输入卡与单条 baseline 说明再压成 `single active baseline + same-final-plotfile photon-only main consumer + additive checksum sibling` 的更高层结构，并写清当前 family 已稳定收敛成单条 `16-species` 直线传播/动量守恒主消费者链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `plasma_lens umbrella summary`：已把 shared `analysis.py`、checksum helper、六条输入脚本与多条 baseline 说明再压成 `6 active baselines + same-final-plotfile analytic lens-chain main consumer + additive checksum sibling + front-end/runtime split` 的更高层结构，并写清当前 family 已稳定收敛成 `native/python/picmi/lattice/boosted/short-lens` 六支共享 `diag1000084` 的主消费者链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `ohm_solver_ion_beam_instability umbrella summary`：已把 shared `analysis.py`、checksum helper、单条输入脚本与单条 baseline 说明再压成 `single active slow baseline + reduced growth-rate main consumer + separate final-plotfile checksum side surface` 的更高层结构，并写清当前 family 已稳定收敛成单条 `1D resonant ion-beam R-instability` 强消费者链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `ohm_solver_em_modes umbrella summary`：已把两条 analysis、checksum helper、两条输入脚本与两条 baseline 说明再压成 `2 active baselines + asymmetric 1D/RZ dual-consumer split + separated checksum surfaces` 的更高层结构，并写清当前 family 已稳定收敛成 `1D checksum-main + spectrogram-side` 与 `RZ spectrogram-main + checksum-side` 的不对称 split。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `ohm_solver_cylinder_compression umbrella summary`：已把 checksum helper、两条 PICMI 输入脚本与两条 baseline 说明再压成 `2 active slow baselines + 1+1 dual-main-surface checksum-only consumer chain + geometry split` 的更高层结构，并写清当前 family 已稳定收敛成 `3D/RZ` 两条 hybrid-PIC cylinder-compression checksum-only sibling。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `maxwell_hybrid_qed umbrella summary`：已把 checksum helper、单条输入卡与单条 baseline 说明再压成 `single FFT-gated baseline + same-final-plotfile phase-velocity main consumer + additive checksum sibling` 的更高层结构，并写清当前唯一 active baseline 已稳定收敛成单条 `2D hybrid-QED vacuum-dispersion` 强消费者链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `magnetostatic_eb umbrella summary`：已把 checksum helper、三条输入脚本与三条 baseline 说明再压成 `3 WarpX_EB-gated baselines + shared diag1000001 checksum surface + 1/2 native-vs-PICMI consumer split` 的更高层结构，并写清当前 family 已稳定收敛成 `native checksum-only` 与 `PICMI in-process analytic + checksum sibling` 的分叉。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `embedded_circle umbrella summary`：已把 `analysis_default_regression.py` 与单条输入卡说明再压成 `single WarpX_EB-gated baseline + plotfile-only checksum consumer chain + family-local loosened rtol` 的更高层结构，并写清当前唯一 active baseline 已稳定收敛成单条 `2D circular-EB PIC-MCC` checksum-only family。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `beam_beam_collision umbrella summary`：已把 `analysis_default_regression.py`、输入卡与两个 plot helper 再压成 `single active slow baseline + same-directory openPMD checksum-only consumer chain + plot-only side helpers` 的更高层结构，并写清当前唯一 active baseline 已稳定收敛成单条 `3D collider-QED application` checksum-only family。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `boundaries umbrella summary`：已把 shared `analysis.py`、`analysis_default_regression.py` 与单条 baseline 说明再压成 `single active baseline + same-final-plotfile additive checksum wrapper + initial/final dual-plotfile main consumer sibling` 的更高层结构，并写清当前唯一 active baseline 已稳定收敛成单条 `3D particle-domain-boundary semantics` 强消费者链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `collider_relevant_diags umbrella summary`：已把 shared `analysis.py`、`analysis_default_regression.py` 与单条 baseline 说明再压成 `single active baseline + separate checksum side surface + reduced-ledger/openPMD/used-inputs main consumer sibling` 的更高层结构，并写清当前唯一 active baseline 已稳定收敛成单条 `3D ColliderRelevant reduced-diagnostics` 强消费者链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `btd_rz umbrella summary`：已把 shared `analysis.py`、`analysis_default_regression.py` 与单条 baseline 说明再压成 `single active baseline + separate checksum side surface + back-transformed on-axis Ex phase-fit main consumer sibling` 的更高层结构，并写清当前唯一 active baseline 已稳定收敛成单条 `RZ boosted-frame Gaussian-laser BTD` 强消费者链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `boosted_diags umbrella summary`：已把 shared `analysis.py`、`analysis_default_regression.py` 与单条 baseline 说明再压成 `single active baseline + separate checksum side surface + dual-BTD/rand-subselection main consumer sibling` 的更高层结构，并写清当前唯一 active baseline 已稳定收敛成单条 `3D boosted-frame BTD` 强消费者链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `thomson_parabola_spectrometer umbrella summary`：已把 shared `analysis.py`、`analysis_default_regression.py` 与单条 baseline 说明再压成 `single active baseline + separate checksum side surface + plot-only main consumer sibling` 的更高层结构，并写清当前唯一 active baseline 已稳定收敛成单条 `3D prescribed-field TPS` 强消费者链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `free_electron_laser umbrella summary`：已把 shared `analysis_fel.py`、`analysis_default_regression.py` 与单条 baseline 说明再压成 `single active baseline + same-directory diag_labframe additive checksum wrapper + lab-frame/boosted-frame dual openPMD main-consumer sibling` 的更高层结构，并写清当前唯一 active baseline 已稳定收敛成单条 `1D boosted rigid-beam FEL` 强消费者链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `particle_boundary_interaction umbrella summary`：已把 shared `analysis.py`、`analysis_default_regression.py` 与单条 baseline 说明再压成 `single active baseline + same-directory openPMD additive checksum wrapper + same-surface mirror-trajectory main consumer sibling` 的更高层结构，并写清当前唯一 active baseline 已稳定收敛成单条 `RZ EB mirror-reflection` 强消费者链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `spacecraft_charging umbrella summary`：已把 shared `analysis.py`、`analysis_default_regression.py` 与单条 baseline 说明再压成 `single active baseline + same-directory openPMD additive checksum wrapper + whole-series phi_min fit main consumer sibling` 的更高层结构，并写清当前唯一 active baseline 已稳定收敛成单条 `RZ immersed-conductor charging` 强消费者链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `pierce_diode umbrella summary`：已把 shared `analysis_pierce_diode.py`、`analysis_default_regression.py` 与单条 baseline 说明再压成 `single active baseline + same-directory openPMD additive checksum wrapper + same-surface final-iteration Child-Langmuir phi/jz main consumer sibling` 的更高层结构，并写清当前唯一 active baseline 已稳定收敛成单条 `1D electrostatic Child-Langmuir diode` 强消费者链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `ion_beam_extraction umbrella summary`：已把 shared `analysis_ion_beam_extraction.py`、`analysis_default_regression.py` 与单条 baseline 说明再压成 `single active baseline + same-directory openPMD additive checksum wrapper + same-surface phi/eb_covered/Dplus tail-energy main consumer sibling` 的更高层结构，并写清当前唯一 active baseline 已稳定收敛成单条 `3D embedded-boundary electrode extractor` 强消费者链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `ohm_solver_ion_Landau_damping umbrella summary`：已把 shared `analysis.py`、`analysis_default_regression.py` 与单条 baseline 说明再压成 `single active slow baseline + reduced damping-curve side consumer + separate final-plotfile checksum main surface` 的更高层结构，并写清当前唯一 active baseline 已稳定收敛成单条 `2D hybrid-PIC ion-Landau-damping` 强消费者链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `ohm_solver_magnetic_reconnection umbrella summary`：已把 shared `analysis.py`、`analysis_default_regression.py` 与单条 baseline 说明再压成 `single active baseline + reduced reconnection-rate main consumer + separate final-plotfile checksum side surface` 的更高层结构，并写清当前唯一 active baseline 已稳定收敛成单条 `2D hybrid-PIC force-free-sheet reconnection` 强消费者链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `nodal_electrostatic umbrella summary`：已把单条 baseline 说明再压成 `single active slow baseline + reduced zero-trigger main consumer + separate final-plotfile checksum side surface` 的更高层结构，并写清当前唯一 active baseline 已稳定收敛成单条 `3D collocated relativistic electrostatic` 零触发强消费者链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `particle_absorbing_boundary umbrella summary`：已把 `analysis.py`、`analysis_default_regression.py` 与单条 baseline 说明再压成 `single active baseline + reduced histogram tail-weight main consumer + separate final-plotfile checksum side surface` 的更高层结构，并写清当前唯一 active baseline 已稳定收敛成单条 `1D thermalizer` 强消费者链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `radiation_reaction umbrella summary`：已把 `analysis.py`、`analysis_default_regression.py` 与单条 baseline 说明再压成 `single active baseline + same-final-plotfile parallel-invariant / perpendicular-analytic-gamma main consumer + additive checksum sibling` 的更高层结构，并写清当前唯一 active baseline 已稳定收敛成单条 `3D constant-B classical-RR` 强消费者链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `open_bc_poisson_solver umbrella summary`：已把 shared `analysis.py`、`analysis_default_regression.py` 与 `normal/sliced` 两条单基线说明再压成 `2 active FFT-gated baselines + shared diag2 openPMD Basseti-Erskine main consumer + shared diag1000001 rtol-1e-2 checksum side surface + 1+1 solver split` 的更高层结构，并写清当前这 `2` 条 active baseline 已稳定收敛成 `normal FFT` 与 `2D-slices FFT` 两条 solver sibling 共同命中同一个横向场解析强消费者链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `vay_deposition umbrella summary`：已把 shared `analysis.py`、顶层 `analysis_default_regression.py` 与 `2D/3D` 两条单基线说明再压成 `2 active FFT-gated baselines + shared same-final-plotfile discrete-Gauss-law main consumer + 1+1 separated checksum surfaces` 的更高层结构，并写清当前这 `2` 条 active baseline 已稳定收敛成 `2D/3D` 两条 geometry sibling 共同命中同一个 discrete-Gauss-law strong consumer。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `energy_conserving_thermal_plasma umbrella summary`：已把 `analysis.py`、`analysis_default_regression.py` 与 `1D/2D` 两条单基线说明再压成 `2 active baselines + shared reduced-energy main consumer + shared diag1000500 additive checksum surface + 1+1 geometry split` 的更高层结构，并写清当前这 `2` 条 active baseline 已稳定收敛成 `1D/2D` 两条 geometry sibling 共同命中同一个 reduced total-energy-drift strong consumer。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `langmuir_fluids umbrella summary`：已把 `analysis_1d.py`、`analysis_2d.py`、`analysis_3d.py`、`analysis_rz.py` 与 `analysis_default_regression.py` 这组并列 helper 再压成 `4 active baselines + same-final-plotfile analytic field/current/rho main consumer + additive checksum sibling + 1/1/1/1 geometry split` 的更高层结构，并写清当前这 `4` 条 active baseline 已稳定收敛成 `1D/2D/3D/RZ` 四条按维度分治的 cold-fluid analytic strong branches。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `load_density umbrella summary`：已把 `analysis_1d.py`、`analysis_2d.py`、`analysis_3d.py`、`analysis_rz.py` 与 `analysis_default_regression.py` 这组并列 helper 再压成 `4 active baselines + same-directory openPMD additive checksum wrapper + 4-way dimensional split + 4 prepare dependencies` 的更高层结构，并写清当前这 `4` 条 active baseline 已稳定收敛成 `1D/2D/3D/RZ` 四条按维度分治的逐 iteration `rho`-to-density main consumer，再外加四条 `example-density.h5` prepare-only 上游依赖。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `load_external_field umbrella summary`：已把 `analysis_3d.py`、`analysis_rz.py`、`analysis_time_scaling.py`、`analysis_default_restart.py` 这组并列 helper 再压成 `11 active baselines + shared diag1000300 checksum surface + 2/2/4/3 shared-analysis split` 的更高层结构，并写清当前这 `11` 条 active baseline 已稳定收敛成 `2` 条 3D PICMI magnetic-mirror 末态位置主链、`2` 条 RZ theta-mode 末态位置主链、`4` 条 `pf0/pfN` time-scaling 主链、`3` 条 same-name final-plotfile restart reproducibility 主链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `implicit umbrella summary`：已把 `implicit` 全段再压成 `8 always-active baselines + 4 PETSc-gated baselines + 1 FFT-gated baseline` 的更高层 split，并写清当前这些 active baseline 已稳定收敛成 `1D Picard`、`planar-pinch`、`PETSc curl-curl`、`JFNK Villasenor`、`cropping`、`symmetry`、`Strang spectral` 这 `7` 组 reduced-ledger / same-final-plotfile strong consumers，再统一叠加 additive checksum wrapper。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `langmuir` `PSATD umbrella summary`：已把 `2D/3D/RZ PSATD` 三段再压成 `24 active FFT-gated baselines + 2 legacy checksum-only snapshots` 的更高层 split，并写清当前 `24` 条 active baseline 已稳定收敛成 `2D analysis_2d.py + diag1000080`、`3D analysis_3d.py + diag1000040`、`RZ analysis_rz.py + diag1000080` 三条维度化 shared-analysis 主链；两个 legacy residual 则是 `test_2d_langmuir_multi_psatd_jrhom_LL2_picmi` 与 `test_3d_langmuir_multi_psatd_single_precision`。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `nci_psatd_stability` `Galilean umbrella summary`：已把 `2D/3D/RZ Galilean` 与 `2D/3D averaged Galilean` 再压成 `13 shared-analysis strong branches + 1 checksum-only hybrid residual` 的更高层 split，并写清这 `13` 条路径当前共同复用 `analysis_galilean.py + checksum --rtol 1e-8`，只是按 `dims/current_correction/do_time_averaging/periodic_single_box_fft` 分流到 `diag1000400/diag1000300/diag1000160` 三张末态 surface；而 `test_2d_galilean_psatd_hybrid` 继续保持不接入 `analysis_galilean.py` 的 checksum-only residual。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `nci_psatd_stability` `2D Galilean` family summary：已把 `test_2d_galilean_psatd`、`test_2d_galilean_psatd_current_correction`、`test_2d_galilean_psatd_current_correction_psb`、`test_2d_galilean_psatd_hybrid` 再压成 `3 shared-analysis strong branches + 1 checksum-only hybrid residual`，并写清前 `3` 条当前共同落在 `analysis_galilean.py diags/diag1000400 + checksum --rtol 1e-8` 这条 shared wiring 上，再进一步分成普通 `Galilean`、`current_correction(2e-4)`、`current_correction_psb(1e-9)` 三条 gate；而 `hybrid` 条目继续保持 `analysis=OFF` 的 checksum-only residual。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `nci_psatd_stability` `averaged Galilean` family summary：已把 `test_2d_averaged_galilean_psatd`、`test_2d_averaged_galilean_psatd_hybrid`、`test_3d_averaged_galilean_psatd`、`test_3d_averaged_galilean_psatd_hybrid` 再压成 `4 active FFT-gated sibling baselines + shared same-final-plotfile field-energy main consumer + additive checksum sibling`，并写清这 `4` 条 active baseline 当前进一步收口成 `2/2 geometry split + 1/1 hybrid split`；其中 2D pair 共享 `26208.04843478073 / 1e-6`，3D pair 共享 `14.564631643496 / 1e-4`，四条路径都不命中附加 `divE-rho/epsilon_0` charge gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `nci_psatd_stability` `RZ Galilean/current_correction` family summary：已把 `test_rz_galilean_psatd`、`test_rz_galilean_psatd_current_correction`、`test_rz_galilean_psatd_current_correction_psb` 再压成 `3 active FFT-gated sibling baselines + shared same-final-plotfile field-energy main consumer + additive checksum sibling`，并写清这 `3` 条 active baseline 当前进一步分成 `1` 条无附加 charge gate、`1` 条 `3e-4` charge gate、`1` 条 `1e-9` PSB charge gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `nci_psatd_stability` 3D `Galilean/current_correction` family summary：已把 `test_3d_galilean_psatd`、`test_3d_galilean_psatd_current_correction`、`test_3d_galilean_psatd_current_correction_psb` 再压成 `3 active FFT-gated sibling baselines + shared same-final-plotfile field-energy main consumer + additive checksum sibling`，并写清这 `3` 条 active baseline 当前进一步分成 `1` 条无附加 charge gate、`1` 条 `1e-2` charge gate、`1` 条 `1e-9` PSB charge gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `langmuir` 3D `PSATD` family summary：已把这一整段再压成 `11 active FFT-gated sibling baselines + 1 legacy checksum-only snapshot` 的更高层 split，并写清当前 `11` 条 active baseline 全部共同落在 `analysis_3d.py diags/diag1000040 + checksum` wiring 上，再进一步分成 `6` 条无附加守恒 gate、`2` 条 `1e-9` current-correction gate、`2` 条 `1e-3` Vay gate、`1` 条 tri-frame `F` evolution side chain，而 `test_3d_langmuir_multi_psatd_single_precision` 只剩 benchmark snapshot。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `langmuir` 2D `PSATD` family summary：已把这一整段再压成 `10 active FFT-gated sibling baselines + 1 legacy checksum-only snapshot` 的更高层 split，并写清当前 `10` 条 active baseline 全部共同落在 `analysis_2d.py diags/diag1000080 + checksum` wiring 上，再进一步分成 `5` 条无附加守恒 gate、`2` 条 `1e-9` current-correction gate、`3` 条 `1e-3` Vay gate，而 `test_2d_langmuir_multi_psatd_jrhom_LL2_picmi` 只剩 benchmark snapshot。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `langmuir` 2D `JRhom_LL2 PICMI` legacy 边界：已把 `test_2d_langmuir_multi_psatd_jrhom_LL2_picmi`、`langmuir/CMakeLists.txt`、`Examples/Tests/langmuir` 目录现状与 benchmark 树再补一轮一致性，明确写清这条 2D 名字当前只剩 benchmark JSON snapshot，源码树里没有对应 2D PICMI 输入或活跃 test；现行 PICMI counterpart 只在 3D 侧存在。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `langmuir` 2D `PSATD` 普通/JRhom/current-correction sibling：已把 `test_2d_langmuir_multi_psatd`、`test_2d_langmuir_multi_psatd_JRhom_LL2`、`test_2d_langmuir_multi_psatd_current_correction`、`langmuir/CMakeLists.txt`、`analysis_2d.py`、`analysis_utils.py` 与对应输入卡的 wiring 再补一轮一致性，明确写清这三条 active baseline 当前都共同落在 `analysis_2d.py diags/diag1000080 + checksum` 这组 2D FFT-gated sibling wiring 里；其中普通 `PSATD` 与 `JRhom_LL2` 只保留解析 `Ex/Ez` 主链，而 `current_correction` 这支额外命中 `1e-9` 的 `divE-rho/epsilon_0` 守恒 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `langmuir` 2D `PSATD` 相邻 sibling：已把 `test_2d_langmuir_multi_psatd_nodal`、`test_2d_langmuir_multi_psatd_momentum_conserving`、`test_2d_langmuir_multi_psatd_vay_deposition`、`langmuir/CMakeLists.txt`、`analysis_2d.py`、`analysis_utils.py` 与对应输入卡的 wiring 再补一轮一致性，明确写清这三条 active baseline 当前都共同落在 `analysis_2d.py diags/diag1000080 + checksum` 这组 2D FFT-gated sibling wiring 里；其中 `nodal` 和 `momentum_conserving` 只保留解析 `Ex/Ez` 主链，而 `vay_deposition` 这支额外命中 `1e-3` 的 `divE-rho/epsilon_0` 守恒 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `langmuir` 2D `PSATD` 尾项：已把 `test_2d_langmuir_multi_psatd_vay_deposition_nodal`、`langmuir/CMakeLists.txt`、`analysis_2d.py`、`analysis_utils.py` 与对应输入卡的 wiring 再补一轮一致性，明确写清这条 active baseline 当前已经能直接读成 `2D Vay + PSATD + collocated` 的 nodal sibling；也就是 shared `diag1000080` 上的解析 `Ex/Ez` 主链，加上 `analysis_utils.py` 额外施加的 `1e-3` `divE-rho/epsilon_0` 守恒 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `langmuir` 3D `div_cleaning` / `vay_deposition_nodal` 余项：已把 `test_3d_langmuir_multi_psatd_div_cleaning`、`test_3d_langmuir_multi_psatd_vay_deposition_nodal`、`langmuir/CMakeLists.txt`、`analysis_3d.py`、`analysis_utils.py` 与相关输入卡的 wiring 再补一轮一致性，明确写清前者当前已经能直接读成 `shared selective-particle/openPMD field main consumer + tri-frame F-evolution side chain + additive checksum`，后者则是 `slow` 的 `Vay + PSATD + collocated` sibling，并显式带 `1e-3` 的 `divE-rho/epsilon_0` 守恒 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `langmuir` 3D `nodal/gather` sibling baseline：已把 `test_3d_langmuir_multi_psatd_nodal`、`test_3d_langmuir_multi_psatd_momentum_conserving`、`test_3d_langmuir_multi_psatd_current_correction_nodal`、`langmuir/CMakeLists.txt`、`analysis_3d.py`、`analysis_utils.py`、`inputs_base_3d` 与三张输入卡的 wiring 再补一轮一致性，明确写清这组三条 active baseline 当前已经能直接读成 `3 active FFT-gated nodal/gather sibling split + shared selective-particle/openPMD field main consumer + additive checksum sibling`；也就是 shared `diag1000040` 上的 selective particle output + 解析 `Ex/Ey/Ez` 主链、`openPMD` on-particle-field side consumer，以及只在 `current_correction_nodal` 这支额外打开的 `divE-rho/epsilon_0` 守恒 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `langmuir` 3D `JRhom_LL2` sibling baseline：已把 `test_3d_langmuir_multi_psatd_JRhom_LL2`、`test_3d_langmuir_multi_psatd_JRhom_LL2_nodal`、`test_3d_langmuir_multi_psatd_JRhom_LL2_picmi`、`langmuir/CMakeLists.txt`、`analysis_3d.py`、`analysis_utils.py`、`inputs_base_3d` 与三张输入卡的 wiring 再补一轮一致性，明确写清这组三条 active baseline 当前已经能直接读成 `3 active FFT-gated JRhom sibling split + shared selective-particle/openPMD field main consumer + additive checksum sibling`；也就是 shared `diag1000040` 上的 selective particle output + 解析 `Ex/Ey/Ez` 主链、`openPMD` on-particle-field side consumer，以及 native / nodal / PICMI 三支的 producer front-end 分叉。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `langmuir` 3D `PSATD` sibling baseline：已把 `test_3d_langmuir_multi_psatd`、`test_3d_langmuir_multi_psatd_current_correction`、`test_3d_langmuir_multi_psatd_vay_deposition`、`langmuir/CMakeLists.txt`、`analysis_3d.py`、`analysis_utils.py`、`inputs_base_3d` 与三张输入卡的 wiring 再补一轮一致性，明确写清这组三条 active baseline 当前已经能直接读成 `3 active FFT-gated sibling split + shared selective-particle/openPMD field main consumer + additive checksum sibling`；也就是 shared `diag1000040` 上的 selective particle output + 解析 `Ex/Ey/Ez` 主链、`openPMD` on-particle-field side consumer，以及只在 `current_correction` / `vay` 两支额外打开的 `divE-rho/epsilon_0` 守恒 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `langmuir` RZ `PSATD` sibling baseline：已把 `test_rz_langmuir_multi_psatd`、`test_rz_langmuir_multi_psatd_current_correction`、`test_rz_langmuir_multi_psatd_JRhom_LL4`、`langmuir/CMakeLists.txt`、`analysis_rz.py`、`analysis_utils.py`、`inputs_base_rz` 与三张输入卡的 wiring 再补一轮一致性，明确写清这组三条 active baseline 当前已经能直接读成 `3 active FFT-gated sibling split + same-final-plotfile analytic-field/filter main consumer + additive checksum sibling`；也就是 shared `diag1000080` 上的解析 `Er/Ez` 主链、三套 filter diagnostics side consumer，以及只在 `current_correction` 这支额外打开的 `divE-rho/epsilon_0` 守恒 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `langmuir` core native baselines：已把 `test_1d_langmuir_multi`、`test_2d_langmuir_multi`、`test_rcylinder_langmuir_multi`、`test_rsphere_langmuir_multi`、`test_rz_langmuir_multi`、`langmuir/CMakeLists.txt`、`analysis_{1d,2d,r1d,rz}.py`、`analysis_utils.py` 与相关输入卡的 wiring 再补一轮一致性，明确写清这组 active baseline 当前已经能直接读成 `1/1/2/1 geometry split + same-final-plotfile analytic-field main consumer + additive checksum sibling`；也就是 `1D/2D/RZ` 解析场主链、`RCYLINDER/RSPHERE` 共用径向 `Er` 主链，以及 `RZ` 的三套 filter diagnostics side consumer。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `langmuir_fluids` family：已把 `test_1d_langmuir_fluid`、`test_2d_langmuir_fluid`、`test_rz_langmuir_fluid`、`langmuir_fluids/CMakeLists.txt`、`analysis_{1d,2d,rz}.py` 与三张输入卡的 wiring 再补一轮一致性，明确写清这组 active baseline 当前已经能直接读成 `1/1/1 geometry split + same-final-plotfile analytic field/current/rho main consumer + additive checksum sibling`；也就是各自末态 plotfile 上的解析 `E/J/rho` 主链加附加 checksum。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `energy_conserving_thermal_plasma` sibling baseline：已把 `test_1d_energy_conserving_thermal_plasma`、`test_2d_energy_conserving_thermal_plasma`、`energy_conserving_thermal_plasma/CMakeLists.txt`、`analysis.py` 与两张输入卡的 wiring 再补一轮一致性，明确写清这对 active baseline 当前已经能直接读成 `1+1 sibling split + shared reduced-energy main consumer + shared final-plotfile checksum surface`；也就是 `EF.txt + EP.txt` 总能量漂移主链与各自 `diag1000500` checksum surface 的双层结构。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `radiation_reaction` active baseline：已把 `test_3d_radiation_reaction`、`radiation_reaction/CMakeLists.txt`、`analysis.py` 与 `inputs_test_3d_radiation_reaction` 的 wiring 再补一轮一致性，明确写清这条 active baseline 当前已经能直接读成 `single active baseline + same-final-plotfile main consumer + additive checksum sibling`；也就是同一张末态 plotfile 上 5 个单粒子的 parallel-invariant / perpendicular-analytic-gamma 主链加附加 checksum。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `reduced_diags` family：已把 `test_3d_reduced_diags`、`test_3d_reduced_diags_load_balance_costs_{heuristic,timers,timers_picmi,timers_psatd}`、`reduced_diags/CMakeLists.txt`、`analysis_reduced_diags.py`、`analysis_reduced_diags_impl.py`、`analysis_reduced_diags_load_balance_costs.py` 与相关输入卡的 wiring 再补一轮一致性，明确写清这组 active baseline 当前已经能直接读成 `1/4 baseline split`；也就是主干 compact-observable cross-check 的 same-final-plotfile full-plotfile/reduced-ledger 主链，加上四条 `LBC.txt` efficiency-improvement 主链与独立末态 plotfile checksum side surface。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `vay_deposition` sibling baseline：已把 `test_2d_vay_deposition`、`test_3d_vay_deposition`、`vay_deposition/CMakeLists.txt`、`analysis.py` 与两张输入卡的 wiring 再补一轮一致性，明确写清这对 active baseline 当前已经能直接读成 `1+1 sibling split + shared same-final-plotfile discrete-Gauss-law consumer + additive checksum`；也就是各自末态 plotfile 上的 `rho/divE` 主链加附加 checksum。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `implicit` Strang spectral baseline：已把 `test_2d_theta_implicit_strang_psatd`、`implicit/CMakeLists.txt`、`analysis_2d_psatd.py` 与 `inputs_test_2d_theta_implicit_strang_psatd` 的 wiring 再补一轮一致性，明确写清这条 active baseline 当前已经能直接读成 `single FFT-gated active baseline + reduced-energy main consumer + separate final-plotfile checksum side surface`；也就是 `field_energy + particle_energy` 主链与独立 `diag1000020` checksum side surface 的双层结构。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `implicit` symmetry baseline：已把 `test_2d_theta_implicit_symmetry`、`implicit/CMakeLists.txt`、`analysis_implicit.py` 与 `inputs_test_2d_theta_implicit_symmetry` 的 wiring 再补一轮一致性，明确写清这条 active baseline 当前已经能直接读成 `single active baseline + same-final-plotfile reduced-energy/Gauss-law main consumer + additive checksum sibling`；也就是 `field_energy + particle_energy` 主链、同一张 `diag1000400` 末态 plotfile 上的 `divE-rho`/`num_electrons` gate，以及附加 checksum 的三层结构。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `implicit` PEC-cropping baseline：已把 `test_2d_theta_implicit_jfnk_vandb_cropping`、`implicit/CMakeLists.txt`、`analysis_vandb_jfnk_2d_cropping.py` 与 `inputs_test_2d_theta_implicit_jfnk_vandb_cropping` 的 wiring 再补一轮一致性，明确写清这条 active baseline 当前已经能直接读成 `single active baseline + same-final-plotfile Gauss-law main consumer + additive checksum sibling`；也就是同一张 `diag1000010` 末态 plotfile 上的局部 `divE-rho` 极值主链加附加 checksum。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `implicit` JFNK Villasenor sibling baseline：已把 `test_2d_theta_implicit_jfnk_vandb`、`test_2d_theta_implicit_jfnk_vandb_filtered`、`test_2d_theta_implicit_jfnk_vandb_picmi`、`implicit/CMakeLists.txt`、`analysis_vandb_jfnk_2d.py` 与三张输入卡的 wiring 再补一轮一致性，明确写清这组三条 active baseline 当前已经能直接读成 `1/1/1 sibling split + shared reduced-energy/same-final-plotfile dual-consumer chain`；也就是 `field_energy + particle_energy` 主链、同一张 `diag1000020` 末态 plotfile 上的 Gauss-law gate，以及附加 checksum 的三层结构。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `implicit` PETSc curl-curl preconditioner baseline：已把 `test_2d_curl_curl_petsc_pc`、`test_rcylinder_curl_curl_petsc_pc`、`test_rz_curl_curl_petsc_pc`、`implicit/CMakeLists.txt`、`analysis_petsc_matrix.py` 与三张输入卡的 wiring 再补一轮一致性，明确写清这组三条 active baseline 当前已经能直接读成 `1/1/1 geometry split + shared reduced-iteration main consumer + same-final-plotfile additive checksum sibling`；也就是 `newton_solver.txt` 的 exact-iteration 主链加各自末态 plotfile checksum 的双层结构。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `implicit` planar-pinch sibling baseline：已把 `test_1d_theta_implicit_planar_pinch`、`test_2d_theta_implicit_planar_pinch`、`implicit/CMakeLists.txt`、`analysis_planar_pinch.py` 与两张输入卡的 wiring 再补一轮一致性，明确写清这对 active baseline 当前已经能直接读成 `1+1 sibling split + shared reduced-ledger/final-plotfile dual-consumer chain`；也就是 `newton_solver + field_energy + particle_energy + poynting_flux` 主链、同一张 `diag1000020` 末态 plotfile 上的 Gauss-law gate，以及附加 checksum 的三层结构。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `implicit` 1D Picard sibling baseline：已把 `test_1d_semi_implicit_picard`、`test_1d_theta_implicit_picard`、`implicit/CMakeLists.txt`、`analysis_1d.py` 与两张输入卡的 wiring 再补一轮一致性，明确写清这对 active baseline 当前已经能直接读成 `1+1 sibling split + shared reduced-energy main consumer + shared final-plotfile checksum surface`；也就是 `field_energy.txt + particle_energy.txt` 总能量漂移主链与独立 `diag1000100` checksum surface 的双层结构，其中 `semi_implicit` / `theta_implicit` 只在主链里分叉到 `2.5e-5` / `1e-14` 两档容差。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `particle_absorbing_boundary` active baseline：已把 `test_1d_particle_absorbing_boundary`、`particle_absorbing_boundary/CMakeLists.txt`、`analysis.py` 与 `inputs_test_1d_particle_absorbing_boundary` 的 wiring 再补一轮一致性，明确写清这条 active baseline 当前已经能直接读成 `single active baseline + reduced histogram main consumer + separate final-plotfile checksum side surface`；也就是 `PhaseSpaceElectrons` reduced histogram 尾部权重积分主链与独立 `diagInst008000/` checksum side surface 的双层结构。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `open_bc_poisson_solver` active baseline：已把 `test_3d_open_bc_poisson_solver`、`test_3d_open_bc_poisson_solver_sliced`、`open_bc_poisson_solver/CMakeLists.txt`、`analysis.py` 与两张输入卡的 wiring 再补一轮一致性，明确写清这组 active baseline 当前已经能直接读成 `1/1 solver split`；也就是普通 `FFT` 分支和 `2D-slices FFT` 分支共同复用 `diag2` openPMD `Ex/Ey` 主链，并共享独立的 `diag1000001` checksum side surface。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `ohm_solver_magnetic_reconnection` active baseline：已把 `test_2d_ohm_solver_magnetic_reconnection_picmi`、`ohm_solver_magnetic_reconnection/CMakeLists.txt`、`analysis.py` 与 `inputs_test_2d_ohm_solver_magnetic_reconnection_picmi.py` 的 wiring 再补一轮一致性，明确写清这条 active baseline 当前已经能直接读成 `single active baseline + reduced reconnection-rate main consumer + separate final-plotfile checksum side surface`；也就是 `diags/plane.dat` 的 reduced 主链与独立 `diag1000020` checksum side surface 的双层结构。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `nodal_electrostatic` active baseline：已把 `test_3d_nodal_electrostatic_solver`、`nodal_electrostatic/CMakeLists.txt`、`analysis.py` 与 `inputs_test_3d_nodal_electrostatic_solver` 的 wiring 再补一轮一致性，明确写清这条 active baseline 当前已经能直接读成 `single active baseline + reduced-ledger main consumer + separate final-plotfile checksum side surface`；也就是 reduced `chi_max/photon-count` 零触发主链与独立 `diag1000010` checksum side surface 的双层结构。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `maxwell_hybrid_qed` family：已把 `Examples/Tests/maxwell_hybrid_qed/analysis_default_regression.py`、`analysis.py`、`inputs_test_2d_maxwell_hybrid_qed_solver` 与 `maxwell_hybrid_qed/CMakeLists.txt` 的 wiring 再补一轮一致性，明确写清这组 active wiring 当前已经能直接读成 `single FFT-gated active baseline + same-final-plotfile dual-consumer chain`；也就是 `test_2d_maxwell_hybrid_qed_solver` 把同一张 `diags/diag1000300` 末态 plotfile 同时交给 `Ey` 中轴相速度主链和附加 checksum sibling。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `uniform_plasma` family baseline：已把 `test_2d_uniform_plasma`、`test_3d_uniform_plasma` 与 `test_3d_uniform_plasma_restart` 的 producer/consumer wiring 再补一轮一致性，明确写清这组 active baseline 当前已经能直接读成 `1/1/1 baseline split`；也就是 `2D native checksum-only mainline`、`3D non-restart checksum-only mainline + restart checkpoint producer sibling`，以及 `same-final-plotfile restart reproducibility + additive rtol = 1e-12 checksum branch`。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `linear_compton` family helper：已把 `Examples/Tests/linear_compton/analysis_default_regression.py`、`linear_compton/CMakeLists.txt`、`analysis_bunch_laser.py` 与 `analysis_two_particles.py` 的 family wiring 再补一轮一致性，明确写清这条 helper 当前已经能直接读成 `2 active baselines + shared same-directory diag1 checksum surface + 1/1 main-consumer split`；也就是 `bunch_laser` 路径把同一条 `diags/diag1` openPMD surface 叠加到 `momentum-and-yield` 主链之后，而 `two_particles` 路径则把它叠加到 `complete-conversion + conservation-base` 主链之后。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `magnetostatic_eb` family：已把 `Examples/Tests/magnetostatic_eb/analysis_default_regression.py`、`magnetostatic_eb/CMakeLists.txt`、`inputs_test_3d_magnetostatic_eb`、`inputs_test_3d_magnetostatic_eb_picmi.py` 与 `inputs_test_rz_magnetostatic_eb_picmi.py` 的 family wiring 再补一轮一致性，明确写清这组 active baseline 当前已经能直接读成 `3 active baselines + shared diag1000001 checksum surface + 2/1 checksum-state split + 1/2 main-consumer split`；也就是 native 3D 路径仍是 checksum-only branch，而 3D/RZ 两条 PICMI 变体虽然在 CMake 里都写成 `analysis=OFF`，但脚本本体都会在 `sim.step(1)` 后直接从进程内 `Efield_aux/Bfield_aux` 上执行解析场双断言，其中 RZ 变体的外层 helper 还显式带 `--skip-particles`。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `do_pml_j_damping`，并修正相邻 `pml_has_particles` 的 runtime 顺序：已把 `WarpX.cpp`、`WarpXEvolve.cpp`、`WarpXEvolvePML.cpp`、官方参数文档与相邻条目的 wiring 再补一轮一致性，明确写清这条参数当前已经能直接读成 `extended-PML current-source` 小簇里的 `post-copy damping sibling`；也就是它和 `do_pml_in_domain`、`pml_has_particles` 共同挂在 `CopyJPML -> DampJPML -> EvolveEPML(push_*_pml_current)` 这条 runtime chain 上。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `particle_pusher` umbrella summary：已把 `Examples/Tests/particle_pusher/analysis.py`、`analysis_default_regression.py`、`inputs_test_3d_particle_pusher` 与 `particle_pusher/CMakeLists.txt` 的 family wiring 再补一轮一致性，明确写清这整段当前已经能直接读成 `single active baseline + same-final-plotfile additive checksum wrapper + single-scalar force-free x-residual main-consumer sibling`；也就是唯一的 `test_3d_particle_pusher` 把主 analysis 和 helper 共同钉在 `diag1010000`，而主合同只保留单个 positron 的 `abs(x) < 1e-3` gate。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `do_pml_dive_cleaning / do_pml_divb_cleaning`：已把 `WarpX.cpp`、`WarpXEvolvePML.cpp`、`WarpXMovingWindow.cpp`、`WarpXEvolve.cpp` 与官方参数文档的 wiring 再补一轮一致性，明确写清这对参数当前已经能直接读成 `PML divergence-cleaning` 小簇里的 `electric-cleaning sibling / magnetic-cleaning sibling`，共同挂在 `pml_F / pml_G damping-update + moving-window shift + post-PSATD FillBoundaryF/G` 这条 runtime chain 上。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `pml_has_particles`：已按源码当前顺序校正这条参数的同簇表述，明确写清它和 `do_pml_in_domain`、`do_pml_j_damping` 共同挂在 `CopyJPML -> DampJPML -> EvolveEPML(push_*_pml_current)` 这条 extended-PML current runtime chain 上。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `pec` helper：已把 `Examples/Tests/pec/analysis_default_regression.py`、`pec/CMakeLists.txt`、`analysis_pec.py`、`analysis_pec_mr.py` 与 `analysis_pec_insulator_implicit.py` 的 family wiring 再补一轮一致性，明确写清这条 helper 当前已经能直接读成 `7 active baselines + 2/1/3/1 checksum-surface split + 3/1/2/2 main-consumer split`；也就是 standing-wave / PMC / MR / implicit-insulator / particle / explicit-insulator 这几支现在已经能直接并排读出 shared analysis 和 checksum-only sibling 的分工。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `plasma_lens` helper：已把 `Examples/Tests/plasma_lens/analysis_default_regression.py`、`analysis.py` 与 `plasma_lens/CMakeLists.txt` 的 family wiring 再补一轮一致性，明确写清这条 helper 当前已经能直接读成 `6 active baselines + same-final-plotfile additive checksum wrapper + shared final-particle analytic lens-chain main-consumer sibling`；也就是六条 active baseline 全都共同固定消费 `diag1000084`，而 shared `analysis.py` 再在同一末态粒子 surface 上内部切到 PICMI/native 初值分支、repeated-lens/lattice 分支、optional boosted `z` 反变换，以及 short-lens 放宽容差分支。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `photon_pusher` helper：已把 `Examples/Tests/photon_pusher/analysis_default_regression.py`、`analysis.py`、`inputs_test_3d_photon_pusher` 与 `photon_pusher/CMakeLists.txt` 的 wiring 再补一轮一致性，明确写清这条 helper 当前已经能直接读成 `single active baseline + same-final-plotfile additive checksum wrapper + 16-species straight-line/momentum-conservation main-consumer sibling`；也就是 helper 和主 analysis 共同固定消费 `diag1000050`，但主合同已收窄成 `8 个方向 × 2 档动量` 光子矩阵上的最坏 `disc_pos/disc_mom` 双阈值 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `particle_thermal_boundary` helper：已把 `Examples/Tests/particle_thermal_boundary/analysis_default_regression.py`、`analysis.py`、`inputs_test_2d_particle_thermal_boundary` 与 `particle_thermal_boundary/CMakeLists.txt` 的 wiring 再补一轮一致性，明确写清这条 helper 当前已经能直接读成 `single active baseline + separate final-plotfile checksum side surface + reduced-energy main-consumer sibling`；也就是 helper 只消费 `diag1002000`，而主 analysis 继续固定回读 `EF.txt / EN.txt` 去执行场能增长和粒子总能量漂移的 reduced-ledger 主链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `embedded_boundary_diffraction` helper：已把 `Examples/Tests/embedded_boundary_diffraction/analysis_default_regression.py`、`analysis_fields.py`、`inputs_test_rz_embedded_boundary_diffraction` 与 `embedded_boundary_diffraction/CMakeLists.txt` 的 wiring 再补一轮一致性，明确写清这条 helper 当前已经能直接读成 `single active baseline + same-directory openPMD additive checksum wrapper + iteration-300 first-minimum Airy main-consumer sibling`；也就是 helper 和主 analysis 共同消费 `diag1/`，但主合同已收窄成 `iteration = 300` 上的 `E_x(r,z)` 强度图、第一极小值半径轨迹和 Airy 线性包络 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `particle_pusher` helper：已把 `Examples/Tests/particle_pusher/analysis_default_regression.py`、`analysis.py`、`inputs_test_3d_particle_pusher` 与 `particle_pusher/CMakeLists.txt` 的 wiring 再补一轮一致性，明确写清这条 helper 当前已经能直接读成 `single active baseline + same-final-plotfile additive checksum wrapper + single-scalar force-free x-residual main-consumer sibling`；也就是 helper 和主 analysis 共同固定消费 `diag1010000`，但主合同已收窄成单个 positron 的 `abs(x) < 1e-3` gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `embedded_boundary_cube` helper：已把 `Examples/Tests/embedded_boundary_cube/analysis_default_regression.py`、`analysis_fields_2d.py`、`analysis_fields.py` 与 `embedded_boundary_cube/CMakeLists.txt` 的 family wiring 再补一轮一致性，明确写清这条 helper 当前已经能直接读成 `3 active baselines + 1/2 output-surface split + 1/2 main-consumer split`；也就是 2D 分支单独走 `diag1000114 + analysis_fields_2d.py`，而 3D 普通版与 `macroscopic` 版共同走 `diag1000208 + analysis_fields.py`，其中 `macroscopic` 频率修正仍只靠 shared 3D analysis 内部的 cwd/test-name 分支触发。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `electrostatic_sphere` helper：已把 `Examples/Tests/electrostatic_sphere/analysis_default_regression.py`、`analysis_electrostatic_sphere.py` 与 `electrostatic_sphere/CMakeLists.txt` 的 family wiring 再补一轮一致性，明确写清这条 helper 当前已经能直接读成 `7 active baselines + 5/1/1 checksum-surface split + 3/1/3 analysis-state split`；也就是 `diag1000030 / diag1000002 / diag1000054` 三组末态 surface 全部继续挂到 shared `analysis_electrostatic_sphere.py`，但主 analysis 内部又分成 `phi`-enabled 能量账本分支、`emass_10` 放宽 `L2` 分支和默认 field-only `L2` 分支。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `electrostatic_sphere_eb` helper：已把 `Examples/Tests/electrostatic_sphere_eb/analysis_default_regression.py`、`analysis.py`、`analysis_rz.py`、`analysis_rz_mr.py` 与 `electrostatic_sphere_eb/CMakeLists.txt` 的 family wiring 再补一轮一致性，明确写清这条 helper 当前已经能直接读成 `5 active baselines + 3/2 checksum-surface split + 2/1/1/1 main-consumer split`；也就是 `diag1/` 这组 surface 分别挂到 3D `ChargeOnEB + eb_covered` 与 RZ+MR openPMD `phi/Er` 主链，`diag1000001` 这组 surface 则分成 mixed-BC checksum-only 和单层 RZ fields-only additive checksum。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `dive_cleaning` helper：已把 `Examples/Tests/dive_cleaning/analysis_default_regression.py`、`analysis.py` 与 `dive_cleaning/CMakeLists.txt` 的职责边界再补一轮一致性，明确写清这条 helper 当前已经能直接读成 `2 active baselines + shared diag1000128 additive checksum wrapper + dimension-branch Gaussian-field main consumer sibling`；也就是 helper 共同钉 `diags/diag1000128` 这张末态 plotfile surface，而主 `analysis.py` 继续按 2D/3D 分支重建理论高斯束 Coulomb 场，并对 `Ex/Ey/(Ez)` 逐分量施加主断言。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `divb_cleaning` helper：已把 `Examples/Tests/divb_cleaning/analysis_default_regression.py`、`analysis.py` 与 `divb_cleaning/CMakeLists.txt` 的职责边界再补一轮一致性，明确写清这条 helper 当前已经能直接读成 `single active baseline + same-final-plotfile additive checksum wrapper + tri-frame divB/G evolution main consumer sibling`；也就是 helper 只钉 `diags/diag1000400` 这张末态 plotfile surface，而主 `analysis.py` 继续固定回读 `diag1000398/0399/0400` 三帧去检查离散关系 `c^2 div(B) = dG/dt`。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `diff_lumi_diag` helper：已把 `Examples/Tests/diff_lumi_diag/analysis_default_regression.py`、`analysis.py` 与 `diff_lumi_diag/CMakeLists.txt` 的职责边界再补一轮一致性，明确写清这条 helper 当前已经能直接读成 `3 FFT-gated active baselines + shared diag1000080 checksum surface + reduced-ledger/openPMD dual-spectrum main consumer sibling`；也就是 helper 共同钉 `diags/diag1000080` 这张末态 plotfile surface，而主 `analysis.py` 继续完全绕过 `--path`，固定回读 `DifferentialLuminosity*.txt` 与 `DifferentialLuminosity2d` openPMD side channel，再按 `leptons/photons` 分支施加 1D/2D luminosity 谱主断言。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `boundaries` helper：已把 `Examples/Tests/boundaries/analysis_default_regression.py`、`analysis.py` 与 `boundaries/CMakeLists.txt` 的职责边界再补一轮一致性，明确写清这条 helper 当前已经能直接读成 `single active baseline + same-final-plotfile additive checksum wrapper + initial/final dual-plotfile main consumer sibling`；也就是 helper 只钉 `diags/diag1000008` 这张末态 plotfile surface，而主 `analysis.py` 继续在消费同一末态 surface 的同时，再旁路回读 `diag1000000` 初态去完成 reflecting / absorbing / periodic 三组粒子的 relativistic boundary-contract 主断言。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `accelerator_lattice` helper：已把 `Examples/Tests/accelerator_lattice/analysis_default_regression.py`、`analysis.py` 与 `accelerator_lattice/CMakeLists.txt` 的职责边界再补一轮一致性，明确写清这条 helper 当前已经能直接读成 `3 active baselines + same-final-plotfile additive checksum wrapper + shared final-particle quadrupole-chain main consumer sibling`；也就是 helper 只给 `diags/diag1000050` 这张末态 plotfile surface 叠加稳定性面对照，而主 `analysis.py` 继续从同一 surface 读取单个 `electron` 的 `x/z/ux`，再统一走 `boosted-to-lab optional z backtransform + hard-edged quadrupole` 的解析末态主断言。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `spacecraft_charging` helper：已把 `Examples/Physics_applications/spacecraft_charging/analysis_default_regression.py`、`analysis.py` 与 `spacecraft_charging/CMakeLists.txt` 的职责边界再补一轮一致性，明确写清这条 helper 当前已经能直接读成 `single active baseline + same-directory openPMD additive checksum wrapper + whole-series phi_min fit main consumer sibling`；也就是 helper 只给 `diags/diag1/` 这条 openPMD surface 叠加稳定性面对照，而主 `analysis.py` 继续把整段 `iterations` 展开成时间轴、回读 `phi_min(t)` 序列，再对 `(v0,tau)` 相对基准施加 `4%/20%` 的主断言。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `pierce_diode` helper：已把 `Examples/Physics_applications/pierce_diode/analysis_default_regression.py`、`analysis_pierce_diode.py` 与 `pierce_diode/CMakeLists.txt` 的职责边界再补一轮一致性，明确写清这条 helper 当前已经能直接读成 `single active baseline + same-directory openPMD additive checksum wrapper + same-surface final-iteration Child-Langmuir phi/jz main consumer sibling`；也就是 helper 只给 `diags/diag1/` 这条 openPMD surface 叠加稳定性面对照，而主 `analysis_pierce_diode.py` 继续锁定最终 iteration，对数值 `phi/jz` 与 Child-Langmuir 理论值施加统一 `< 0.2` 的双路误差主断言。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `ion_beam_extraction` helper：已把 `Examples/Physics_applications/ion_beam_extraction/analysis_default_regression.py`、`analysis_ion_beam_extraction.py` 与 `ion_beam_extraction/CMakeLists.txt` 的职责边界再补一轮一致性，明确写清这条 helper 当前已经能直接读成 `single active baseline + same-directory openPMD additive checksum wrapper + same-surface phi/eb_covered/Dplus tail-energy main consumer sibling`；也就是 helper 只给 `diags/diag1/` 这条 openPMD surface 叠加稳定性面对照，而主 `analysis_ion_beam_extraction.py` 继续固定在 `iteration=1000` 上回读 `phi/eb_covered/Dplus`，对 `z in [14,23] mm` 的离子束尾统一施加 `40 keV ±5%` 主断言。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `free_electron_laser` helper：已把 `Examples/Physics_applications/free_electron_laser/analysis_default_regression.py`、`analysis_fel.py` 与 `free_electron_laser/CMakeLists.txt` 的职责边界再补一轮一致性，明确写清这条 helper 当前已经能直接读成 `single active baseline + same-directory diag_labframe additive checksum wrapper + lab-frame + boosted-frame dual openPMD main-consumer sibling`；也就是 helper 只钉 `diags/diag_labframe` 这条 lab-frame 稳定性面，而主 `analysis_fel.py` 继续并排消费 `diag_labframe + diag_boostedframe` 两条 openPMD diagnostics 去完成双分支的增益长度与辐射波长主断言。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `collider_relevant_diags` helper：已把 `Examples/Tests/collider_relevant_diags/analysis_default_regression.py`、`analysis.py` 与 `collider_relevant_diags/CMakeLists.txt` 的职责边界再补一轮一致性，明确写清这条 helper 当前已经能直接读成 `single active baseline + separate checksum side surface + reduced-ledger/openPMD/used-inputs main consumer sibling`；也就是 `diags/diag1000001` 这条 helper 只承担附加稳定性面，而主 `analysis.py` 继续固定消费 `reducedfiles/*.txt + diag2/openpmd_%T.h5 + warpx_used_inputs` 去完成 `chi/theta` 与 `dL_dt` 主断言。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `effective_potential_electrostatic` helper：已把 `Examples/Tests/effective_potential_electrostatic/analysis_default_regression.py`、`analysis.py` 与 `effective_potential_electrostatic/CMakeLists.txt` 的职责次序再补一轮一致性，明确写清这条 helper 当前已经能直接读成 `single active baseline + same-directory openPMD additive checksum wrapper + sim-parameter-sidecar/whole-series radial-density main consumer sibling`；也就是 helper 只给 `diags/field_diag/` 叠加稳定性面对照，而主 `analysis.py` 继续依赖 `sim_parameters.dpkl` 和整段 `rho_electrons` 时序做径向 RMS 主断言。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `electrostatic_dirichlet_bc` helper：已把 `Examples/Tests/electrostatic_dirichlet_bc/analysis_default_regression.py`、`analysis.py` 与 `electrostatic_dirichlet_bc/CMakeLists.txt` 的职责次序再补一轮一致性，明确写清这条 helper 当前已经能直接读成 `2 active regressions + same-final-plotfile additive checksum wrapper + whole-series boundary-phi main consumer sibling`；也就是 helper 只钉 `diag1000100` 末态稳定性面，而主 `analysis.py` 继续回放整段 `diag1*` 序列做边界 `phi(t)` 主断言。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `btd_rz` helper：已把 `Examples/Tests/btd_rz/analysis_default_regression.py`、`analysis.py` 与 `btd_rz/CMakeLists.txt` 的职责边界再补一轮一致性，明确写清这条 helper 当前已经能直接读成 `single active baseline + separate checksum side surface + back-transformed on-axis Ex phase-fit main consumer sibling`；也就是 `diags/diag1000289` 这条 helper 只承担附加稳定性面，而主 `analysis.py` 继续固定消费 `./diags/back_rz` 去完成单次快照的 `Ex(z)` 相位中心拟合主链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `boosted_diags` helper：已把 `Examples/Tests/boosted_diags/analysis_default_regression.py`、`analysis.py` 与 `boosted_diags/CMakeLists.txt` 的职责边界再补一轮一致性，明确写清这条 helper 当前已经能直接读成 `single active baseline + separate checksum side surface + dual-BTD/rand-subselection main consumer sibling`；也就是 `diags/diag1000003` 这条 helper 只承担附加稳定性面，而主 `analysis.py` 继续固定消费 `diag2` openPMD side channel 去完成 `Ez` 一致性和粒子子采样 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `thomson_parabola_spectrometer` helper：已把 `Examples/Physics_applications/thomson_parabola_spectrometer/analysis_default_regression.py`、`analysis.py` 与 `thomson_parabola_spectrometer/CMakeLists.txt` 的职责边界再补一轮一致性，明确写清这条 helper 当前已经能直接读成 `single active baseline + separate checksum side surface + plot-only main consumer sibling`；也就是 `diags/diag1` 这条 helper 才承担自动数值稳定性面，而主 `analysis.py` 仍只是固定路径的 detector reconstruction 绘图链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `single_particle` helper：已把 `Examples/Tests/single_particle/analysis_default_regression.py`、`analysis.py`、`analysis_synchronize_velocity.py` 与 `single_particle/CMakeLists.txt` 的 family split 再补一轮一致性，明确写清这条 helper 当前已经能直接读成 `1 active checksum branch + 1 analysis-only sibling`；其中 `test_2d_bilinear_filter` 走 `diags/diag1000001` same-final-plotfile additive checksum，而 `test_1d_synchronize_velocity` 继续完全旁路 helper。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `relativistic_space_charge_initialization` helper：已把 `Examples/Tests/relativistic_space_charge_initialization/analysis_default_regression.py`、`analysis.py` 与 `CMakeLists.txt` 的 same-surface wiring 再补一轮 family-level 一致性，明确写清这条 helper 当前已经能直接读成 `single active baseline + same-final-plotfile fields-only additive checksum wrapper + shared Ex/By relativistic self-field main consumer`。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `projection_div_cleaner` helper：已把 `Examples/Tests/projection_div_cleaner/analysis_default_regression.py`、`analysis.py`、三条 PICMI 脚本尾部的 in-process `divB` strong assert 与 `projection_div_cleaner/CMakeLists.txt` 的 writer-surface / consumer wiring 再补一轮 family-level 一致性，明确写清这条 helper 当前已经能直接读成 `4 active regressions + 1/3 checksum-surface split + 1/3 main-consumer split`。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `qed` helper：已把 `Examples/Tests/qed/analysis_default_regression.py`、两条 Breit-Wheeler frontend、`analysis_quantum_sync.py`、`analysis_schwinger.py` 与 `qed/CMakeLists.txt` 的 writer-surface / consumer wiring 再补一轮 family-level 一致性，明确写清这条 helper 当前已经能直接读成 `10 active regressions + 3 writer surfaces + 4 main-consumer branches`。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `restart` helper：已把 `Examples/Tests/restart/analysis_default_regression.py`、`analysis_default_restart.py` 与 `restart/CMakeLists.txt` 的 active/reserve wiring 再补一轮 family-level 一致性，明确写清这条 helper 当前已经能直接读成 `4 always-active + 4 FFT-gated active + 1 reserve-only FIXME sibling + shared diag1000010 checksum surface`。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `reduced_diags` helper：已把 `Examples/Tests/reduced_diags/analysis_default_regression.py`、`analysis_reduced_diags.py`、`analysis_reduced_diags_impl.py`、`analysis_reduced_diags_load_balance_costs.py` 与 `diag1000200/diag1000003 + reducedfiles` wiring 再补一轮 family-level 一致性，明确写清这条 helper 当前已经能直接读成 `5 active regressions + 1/4 checksum-surface split + 1/3/1 main-consumer split`。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `radiation_reaction` helper：已把 `Examples/Tests/radiation_reaction/analysis_default_regression.py` 和 `analysis.py + diags/diag1000064` wiring 再补一轮 family-level 一致性，明确写清这条 helper 当前已经能直接读成 `single active baseline + shared diag1000064 additive checksum sibling`，而平行/垂直外磁场下的 `gamma(t)` 解析对照仍由主 analysis 消费。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `embedded_boundary_em_particle_absorption` helper：已把 `Examples/Tests/embedded_boundary_em_particle_absorption/analysis_default_regression.py` 和 `analysis.py + diags/diag1` wiring 再补一轮 family-level 一致性，明确写清这条 helper 当前已经能直接读成 `9 active regressions + shared diag1 additive checksum sibling + 3/3/3 geometry split`。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `embedded_boundary_python_api` helper：已把 `Examples/Tests/embedded_boundary_python_api/analysis_default_regression.py` 和 `analysis=OFF + diags/diag1000002` wiring 再补一轮 family-level 一致性，明确写清这条 helper 当前已经能直接读成 `single active baseline + checksum-only branch + plotfile-only diag1000002 surface`。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `embedded_boundary_rotated_cube` helper：已把 `Examples/Tests/embedded_boundary_rotated_cube/analysis_default_regression.py` 和 `analysis_fields_{2d,3d}.py + diag1000068/diag1000111` wiring 再补一轮 family-level 一致性，明确写清这条 helper 当前已经能直接读成 `2 active baselines + shared additive checksum wrapper + 1/1 output-surface split`。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `embedded_circle` helper：已把 `Examples/Tests/embedded_circle/analysis_default_regression.py` 和 `analysis=OFF + diags/diag1000011 --rtol 1e-2` wiring 再补一轮 family-level 一致性，明确写清这条 helper 当前已经能直接读成 `single active baseline + checksum-only branch + plotfile-only diag1000011 surface + family-local loosened rtol`。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `gaussian_beam` helper：已把 `Examples/Tests/gaussian_beam/analysis_default_regression.py` 和 `analysis_focusing_beam.py / analysis_rotated_beam.py / dangling analysis.py target + diag1000000/diag1000010` wiring 再补一轮 family-level 一致性，明确写清这条 helper 当前已经能直接读成 `6 active regressions + shared additive checksum wrapper + 5/1 checksum split + 4/1/1 analysis-state split`。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `flux_injection` helper：已把 `Examples/Tests/flux_injection/analysis_default_regression.py` 和 `analysis_flux_injection_{3d,rz,from_eb}.py + diag1000002/diag1000120/diag1000020` wiring 再补一轮 family-level 一致性，明确写清这条 helper 当前已经能直接读成 `5 active regressions + shared additive checksum wrapper + 1/1/3 output-surface split`。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `field_probe` helper：已把 `Examples/Tests/field_probe/analysis_default_regression.py` 和 `analysis.py + diags/diag1000544` wiring 再补一轮 family-level 一致性，明确写清这条 helper 当前已经能直接读成 `single active baseline + shared diag1000544 additive checksum sibling`，而 `FP_line.txt` `step=500` 的单缝 `sinc^2` 包络误差仍由主 analysis 消费。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `energy_conserving_thermal_plasma` helper：已把 `Examples/Tests/energy_conserving_thermal_plasma/analysis_default_regression.py` 和 `analysis.py + diags/diag1000500` wiring 再补一轮 family-level 一致性，明确写清这条 helper 当前已经能直接读成 `2 active baselines + shared diag1000500 additive checksum sibling`，而 `EF.txt + EP.txt -> total energy drift < 0.3%` 仍由主 analysis 消费。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `field_ionization` helper：已把 `Examples/Tests/field_ionization/analysis_default_regression.py` 和 `analysis.py + diag1000420/diag1001600` wiring 再补一轮 family-level 一致性，明确写清这条 helper 当前已经能直接读成 `4 active regressions + shared additive checksum wrapper + 1/3 output-surface split`，而 Chen-2013 `N5+ ~32%` 与 `particle_orig_z` gate 仍由主 analysis 消费。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `Hybrid-QED` coefficient companion：已把 `warpx.quantum_xi` 和共同的 `use_hybrid_QED -> Hybrid_QED_Push -> warpx_hybrid_QED_push` runtime chain 再补一轮 family-level 一致性，明确写清这条参数当前已经能直接读成 `kernel coefficient sibling`，会先物化成 `m_quantum_xi_c2`，再只在 `PSATD + use_hybrid_QED` 主链里进入 pre/post-PSATD 双次 field-correction kernel。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `Schwinger` spatial-mask companion：已把 `qed_schwinger.xmin/ymin/zmin/xmax/ymax/zmax` 和后续 `ComputeSchwingerGlobalBox -> SchwingerFilterFunc -> filterCreateTransformFromFAB<1> -> SchwingerTransformFunc` runtime chain 再补一轮 family-level 一致性，明确写清这组条目当前已经能直接读成 `global spatial-mask sibling -> XZ effective-thickness + weight-normalization sibling -> cell-production sampling-mode sibling -> shared production/writeback chain` 并排结构。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `Schwinger` sampling companions：已把 `qed_schwinger.y_size`、`qed_schwinger.threshold_poisson_gaussian` 和共同的 `SchwingerFilterFunc -> filterCreateTransformFromFAB<1> -> SchwingerTransformFunc` runtime chain 再补一轮 family-level 一致性，明确写清这组条目当前已经能直接读成 `XZ effective-thickness + weight-normalization sibling -> cell-production sampling-mode sibling -> shared production/writeback chain` 并排结构。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `Hybrid-QED` 邻接小簇：已把 `warpx.use_hybrid_QED`、`warpx.quantum_xi` 和后续 `Hybrid_QED_Push + warpx_hybrid_QED_push` 再补一轮 family-level 一致性，明确写清这组条目当前已经能直接读成 `family root gate -> kernel coefficient sibling -> pre/post-PSATD field-correction runtime chain` 三层结构。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `Schwinger` 邻接小簇：已把 `warpx.do_qed_schwinger`、`qed_schwinger.ele/pos_product_species` 和后续 `doQEDSchwinger() + filterCreateTransformFromFAB + setNewParticleIDs` 再补一轮 family-level 一致性，明确写清这组条目当前已经能直接读成 `family root gate -> dual product siblings -> electron/positron pair runtime chain` 三层结构。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `Breit-Wheeler` 邻接小簇：已把 `qed_bw.lookup_table_mode`、`qed_bw.chi_min` 和后续 `doQedBreitWheeler() + pair products` 再补一轮 family-level 一致性，明确写清这组条目当前已经能直接读成 `dispatch root -> optical-depth threshold sibling -> electron/positron pair runtime chain` 三层结构。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `qed_bw.lookup_table_mode`：已把这条参数再补一轮 family-level 反向指针，明确写清它当前不只是 shared BW engine/table 的初始化分派键，而是 Breit-Wheeler 小簇的 `initialization dispatch root`，会先承接 `chi_min` 这条 threshold companion，再把 `generate/load/builtin` 初始化合同与后续 `optical-depth gate + pair-creation runtime chain` 分开收口。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `qed_qs.lookup_table_mode`：已把这条参数再补一轮 family-level 反向指针，明确写清它当前不只是 shared QS engine/table 的初始化分派键，而是 Quantum Synchrotron 小簇的 `initialization dispatch root`，会先承接 `chi_min + photon_creation_energy_threshold` 两条 companion，再把 `generate/load/builtin` 初始化合同与后续 `RR/QED 分叉链 + post-append cleanup 链` 分开收口。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `qed_qs.photon_creation_energy_threshold`：已把这条参数再补一轮 family-level 反向指针，明确写清它当前不是前置 emission gate，而是 `Quantum Synchrotron` family 里 photon-emission append 链上的 `post-append energy-threshold companion`，会在新增 photon 完成 append、source optical-depth reset 和 `setNewParticleIDs(...)` 之后，只对新增区间做 `Invalid idcpu` 延迟清理标记。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `qed_bw.chi_min`：已把这条参数再补一轮 family-level 反向指针，明确写清它当前不是普通最小 `chi` 数值，而是 `Breit-Wheeler` family 里 shared BW engine/table 的 `chi-threshold sibling`，会先作为 `lookup_table_mode` 三路初始化共用的 threshold companion 写入 wrapper 持久状态，再与 photon 的 `2m_ec^2` 能量边界并排收成 pair-creation 主链前的双门槛。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `qed_qs.chi_min`：已把这条参数再补一轮 family-level 反向指针，明确写清它当前不是普通最小 `chi` 数值，而是 `Quantum Synchrotron` family 里 shared QS engine/table 的 `chi-threshold sibling`，会先作为 `lookup_table_mode` 三路初始化共用的 threshold companion 写入 wrapper 持久状态，再与 `do_classical_radiation_reaction` 并排收成 `classical RR below chi_min / QED recoil above chi_min` 的 runtime 分叉边界。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `<species>.ionization_initial_level`：已把这条参数再补一轮 family-level 反向指针，明确写清它当前不是普通初值整数，而是 `do_field_ionization` family 的 `charge-state seed branch`。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `<species>.ionization_product_species`：已把这条参数再补一轮 family-level 反向指针，明确写清它当前不是普通名字字符串，而是 `do_field_ionization` family 的 `target-container binding branch`。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `<species>.do_adk_correction`：已把这条参数再补一轮 family-level 反向指针，明确写清它当前不是孤立修正布尔，而是 `do_field_ionization` family 的 `Hydrogen-only post-ADK correction branch`。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `boundary.<species>.u_th`：已把这条参数再补一轮 family-level 反向指针，明确写清它当前不是普通热速度数值，而是 particle-boundary family 的 `species-local thermalization width branch`。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `<species>.reflection_model_*`：已把这组参数再补一轮 family-level 反向指针，明确写清它当前不是一般反射率注释，而是 particle-boundary family 的 `species-local stochastic reflection branch`。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `boundary.reflect_all_velocities`：已把这条参数再补一轮 family-level 反向指针，明确写清它当前不是孤立布尔，而是 particle-boundary family 的 `all-velocity reflection upgrade branch`。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `warpx.eb_potential(x,y,z,t)`：已把这条参数再补一轮 family-level 反向指针，明确写清它当前不是孤立 EB 字符串，而是 Poisson-boundary family 的 `EB Dirichlet companion branch`，与 `boundary.potential_lo/hi_*` 共用同一个 startup gate，但只在 EB-enabled scalar Poisson / effective-potential 分支真正 materialize。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `boundary.potential_lo/hi_x/y/z`：已把这组参数再补一轮 family-level 反向指针，明确写清它当前不是六个孤立字符串，而是 Poisson-boundary family 的 `domain-face Dirichlet parser branch`，并与 `warpx.eb_potential(x,y,z,t)` 共用同一个 startup gate。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `boundary.field_lo/hi` / `boundary.particle_lo/hi`：已把这对参数再补一轮 family-level 反向指针，明确写清它们当前不是两条并列开关，而是 boundary family 的 `field root branch` 与 `particle dependent sibling`。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `particles.deposit_on_main_grid` / `particles.gather_from_main_grid`：已把这对 species side-list 再补一轮 family-level 反向指针，明确写清它们当前不是孤立 side-list，而是 coarse-grid routing family 的 `deposition routing branch` 与 `gather routing branch`。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `warpx.n_current_deposition_buffer` / `warpx.n_field_gather_buffer`：已把这对参数再补一轮 family-level 反向指针，明确写清它们当前不是两个孤立宽度，而是 AMR particle-coupling family 的 `deposition buffer branch` 与 `gather buffer branch`。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `warpx.ref_patch_function(x,y,z)`：已把这条参数再补一轮 family-level 反向指针，明确写清它当前不是并列主入口，而是 refined-patch family 的 `fallback parser sibling`，并且旁路 boosted / moving-window early-startup rescale。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `warpx.fine_tag_lo/hi`：已把这组参数再补一轮 family-level 反向指针，明确写清它当前不是普通 bbox 对，而是 refined-patch family 的 `primary explicit-bbox branch`，并且是 boosted / moving-window early-startup rescale 的主入口。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `warpx.do_moving_window`：已把这条参数再补一轮 family-level 反向指针，明确写清它当前不是普通布尔，而是 moving-window / boosted / BTD 邻接簇里的 `family root gate`。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `warpx.start_moving_window_step` / `warpx.end_moving_window_step`：已把这两条参数再补一轮 family-level 反向指针，明确写清它们当前不是普通起止整数，而是 moving-window / boosted / BTD 邻接簇里的 `runtime-interval lower/upper gate`。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `warpx.moving_window_v`：已把这条参数再补一轮 family-level 反向指针，明确写清它当前不是普通速度输入，而是 moving-window / boosted / BTD 邻接簇里的 `window-speed scalar`。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `warpx.moving_window_dir`：已把这条参数再补一轮 family-level 反向指针，明确写清它当前不是普通方向字符串，而是 boosted / moving-window / BTD 邻接簇里的 `window-axis projector + z-only compatibility gate`。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `warpx.zmax_plasma_to_compute_max_step`：已把这条参数再补一轮 family-level 反向指针，明确写清它当前不是一般 stop 参数，而是挂在 `gamma_boost + boost_direction(z) + moving_window_dir(z)` 之后的 wakefield-specific `max_step` companion。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `warpx.compute_max_step_from_btd`：已把这条参数再补一轮 family-level 反向指针，明确写清它当前不是独立 diagnostics 开关，而是挂在 `gamma_boost + boost_direction + moving_window_dir + BTD` 之后的 runtime stop-policy companion。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 boosted-frame companion 簇：已把 `warpx.gamma_boost` 与 `warpx.boost_direction` 再补一轮并排一致性，明确写清前者当前扮演 `scalar gate + beta generator`，后者当前扮演 `axis projector + subsystem compatibility gate`，并显式收口成 `boost-strength + z-only compatibility` 两层结构。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `load_external_field` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前统一服务 `11` 条 active regression，并显式落回共享 `diag1000300` checksum surface 上的 `2/2/4/3` family-wide split。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `capacitive_discharge` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前统一服务 `4` 条 active baseline，并显式落回 `1/1/2` mixed split 与共享 `diag1000050` checksum surface。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `laser_ion` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前统一服务 `2` 条 active baseline，并显式落回 `1+1` native/PICMI mixed split。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `resampling` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前统一服务 `3` 条 active baseline，并显式落回 `2+1` mixed split 与共享 checksum surface 结构。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `relativistic_space_charge_initialization` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前只服务唯一一条 active 3D baseline，并显式落回 same-final-plotfile fields-only additive checksum 结构。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `vay_deposition` family-level helper 行：已把顶层 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前统一服务 `2D + 3D` 两条 active baseline，并显式落回 `1+1` separated-surface split。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `space_charge_initialization` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前统一服务 `2D + 3D` 两条 active baseline，并显式落回 `1+1` shared-surface fields-only split。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `virtual_photons` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前统一服务 `2` 条 active regression，并显式落回 `1/1` same-directory openPMD split。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `scraping` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前统一服务 `normal + filter` 两条 active baseline，并显式落回 `1+1` shared-surface split。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `rigid_injection` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前统一服务 `BTD + lab` 两条 active baseline，并显式落回 `1+1` mixed split 与分离 checksum surface 结构。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `accelerator_lattice` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前统一服务 `3` 条 active baseline，并与 shared `analysis.py` 共用同一个 `diags/diag1000050` final plotfile surface。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `silver_mueller` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前统一服务 `4` 条 active baseline，并与 shared `analysis.py` 共用同一个 `diags/diag1000500` final plotfile surface。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `particle_data_python` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前统一服务 `3` 条 active baseline，并独占同一个 `diags/diag1000010` checksum-only surface。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `restart_eb` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前只服务唯一一条 active baseline `test_3d_eb_picmi`，并且就是这组 family 的唯一自动消费者链；相对地，`test_3d_eb_picmi_restart` 仍停在 reserve-only sibling。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `subcycling` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前只服务唯一一条 active baseline `test_2d_subcycling_mr`，并且就是这组 family 的唯一自动消费者链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `larmor` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前只服务唯一一条 active baseline `test_2d_larmor`，并且就是这组 family 的唯一自动消费者链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `beam_beam_collision` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前只服务唯一一条 active slow baseline `test_3d_beam_beam_collision`，并且就是这组 family 的唯一自动消费者链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `plasma_mirror` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前只服务唯一一条 active baseline `test_2d_plasma_mirror`，并且就是这组 family 的唯一自动消费者链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `secondary_ion_emission` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前只服务唯一一条 active baseline `test_rz_secondary_ion_emission_picmi`，并与 shared `analysis.py` 共用同一个 `diags/diag1/` openPMD 目录。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `ion_beam_extraction` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前只服务唯一一条 active baseline `test_3d_ion_beam_extraction`，并与 shared `analysis_ion_beam_extraction.py` 共用同一个 `diags/diag1/` openPMD 目录。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `free_electron_laser` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前只服务唯一一条 active baseline `test_1d_fel`，并与 shared `analysis_fel.py` 共用同一个 `diags/diag_labframe` openPMD 主 surface。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `pierce_diode` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前只服务唯一一条 active baseline `test_1d_pierce_diode`，并与 shared `analysis_pierce_diode.py` 共用同一个 `diags/diag1/` openPMD 目录。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `spacecraft_charging` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前只服务唯一一条 active baseline `test_rz_spacecraft_charging_picmi`，并与 shared `analysis.py` 共用同一个 `diags/diag1/` openPMD 目录。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `particle_absorbing_boundary` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前只服务唯一一条 active baseline `test_1d_particle_absorbing_boundary`，并单独固定消费 `diags/diagInst008000/` checksum side surface。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `particle_boundary_interaction` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前只服务唯一一条 active baseline `test_rz_particle_boundary_interaction_picmi`，并与 shared `analysis.py` 共用同一个 `diags/diag1/` openPMD 目录。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `particle_fields_diags` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前只服务唯一一条 active 双精度 baseline `test_3d_particle_fields_diags`，而 single-precision sibling 仍停在 reserve/FIXME split。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `particle_data_python` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前统一服务 `3` 条 active baseline，并共用同一个 `diags/diag1000010` checksum-only surface。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `particle_boundary_scrape` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前统一服务 `native + PICMI` 两条 active baseline，并与 shared `analysis_scrape.py` 共用同一个 `diags/diag1000060` final plotfile surface。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `particle_boundary_process` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前统一服务 `2` 条 active baseline，并显式落回 `1+1` mixed split 与分离 checksum surface 结构。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `capacitive_discharge` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前统一服务 `4` 条 active baseline，共享 `diags/diag1000050` checksum surface，并显式落回 `1/1/2` mixed split。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `open_bc_poisson_solver` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前统一服务 `2` 条 active baseline，并显式落回共享 `diag2` openPMD `Ex/Ey` 主消费者 sibling 与共享 `diag1000001 --rtol 1e-2` checksum side surface。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `effective_potential_electrostatic` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前只服务唯一一条 active baseline `test_3d_effective_potential_electrostatic_picmi`，并与主 `analysis.py` 共用同一个 `diags/field_diag/` openPMD 目录。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `load_density` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前统一服务 `4` 条 active regression，共同固定消费同一个 `diags/diag/` openPMD 目录，并显式挂回 `4` 条 prepare-only sibling dependency。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `laser_acceleration` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前统一服务整组 `14` 条 active regression，并显式落回 `3 + 11` service split 与 `3/1/1/3/4/2` output-surface split。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `plasma_acceleration` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前不是附加 checksum，而是整组 `8` 条 active baseline 的唯一自动消费者链，并显式落回 `1 + 1 + 2 + 1 + 1 + 1 + 1` mixed split。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `uniform_plasma` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前统一服务 `3` 条 active baseline，并显式落回 `2` 条 non-restart checksum-only sibling + `1` 条 restart reproducibility additive checksum sibling 这组 `2 + 1` mixed split；三条路径都共同固定消费同一个 `diags/diag1000010` final plotfile surface。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `larmor` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前只服务唯一一条 active baseline `test_2d_larmor`，并且这条路径没有独立 analysis，唯一自动消费者链就是对末态 `diags/diag1000010` 的 checksum。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `plasma_mirror` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前只服务唯一一条 active baseline `test_2d_plasma_mirror`，并且这条路径没有独立 analysis，唯一自动消费者链就是对末态 `diags/diag1000020` 的 checksum。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `beam_beam_collision` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前只服务唯一一条 active baseline `test_3d_beam_beam_collision`，并且这条路径没有独立 analysis、还被显式标成 `slow`，因此 helper 就是整组唯一自动消费者链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `subcycling` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前只服务唯一一条 active baseline `test_2d_subcycling_mr`，并且这条路径没有独立 analysis，唯一自动消费者链就是对末态 `diags/diag1000250` 的 checksum。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `silver_mueller` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前统一服务 `test_1d_silver_mueller`、`test_2d_silver_mueller_x`、`test_2d_silver_mueller_z` 和 `test_rz_silver_mueller_z` 这 `4` 条 active baseline，并共同固定消费同一个 `diags/diag1000500` final plotfile surface；相对地，shared `analysis.py` 仍对应 Cartesian/RZ 分支化的全域残余场主消费者链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `secondary_ion_emission` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前只服务唯一一条 active baseline `test_rz_secondary_ion_emission_picmi`，并且与 shared `analysis.py` 一样共同固定消费同一个 `diags/diag1/` openPMD 目录，也就是 same-directory additive checksum wrapper。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `scraping` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前统一服务 `test_rz_scraping` 与 `test_rz_scraping_filter` 两条 active baseline，并共同固定消费同一个 `diags/diag1000037` final-plotfile checksum surface；相对地，主 physics consumers 则显式落回 `analysis_rz.py` 与 `analysis_rz_filter.py` 这组 `normal/filter` two-way split。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `rigid_injection` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前统一服务 `BTD + lab` 两条 active baseline，并分别给 `diags/diag1000001` 与 `diags/diag1000289` 这两条末态 plotfile surface 追加 checksum。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `single_particle` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前只服务 `test_2d_bilinear_filter` 这一条 checksum branch，而 `test_1d_synchronize_velocity` 仍完全旁路 helper，只走独立 physics analysis。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `particles_in_pml` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前统一服务 `2D/3D × single-level/MR` 四条 active baseline，并分别固定消费 `diag1000180 / diag1000300 / diag1000120 / diag1000200` 这四个独立末态 plotfile checksum surface。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `particle_thermal_boundary` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前只服务唯一一条 active baseline `test_2d_particle_thermal_boundary`，并显式落回“`EF/EN` reduced-energy main consumer + 分离的 `diag1002000` final-plotfile checksum side surface”这组 family split。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `particle_pusher` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前只服务唯一一条 active baseline `test_3d_particle_pusher`，并与 shared `analysis.py` 一起共同固定消费同一个末态 `diags/diag1010000` final plotfile surface。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `vay_deposition` family-level 反向指针：已把 shared `analysis.py` 与顶层 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它们当前共同对应 `2D + 3D` 两条 active baseline 的 shared main-consumer / additive-checksum split。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `virtual_photons` family-level 反向指针：已把 shared helper 再补一轮并排一致性，明确写清它当前统一服务 `2` 条 active regression，并稳定分成 `1/1` 两层主 consumer；同时也把 `analysis_beamsize_effect.py` 与 `analysis_virtual_photons.py` 分别显式落回各自的 `1/1` 分布语义。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `space_charge_initialization` family-level 反向指针：已把 shared `analysis.py` 再补一轮并排一致性，明确写清它当前统一服务 `2D + 3D` 两条 active baseline，并共同固定消费同一个末态 `diags/diag1000001` Coulomb-field main surface；同时也把 helper 显式落回同一 same-final-plotfile 的 fields-only additive checksum wrapper。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `reduced_diags` family-level 反向指针：已把 shared `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前统一服务 `5` 条 active regression，并稳定分成 `1/4` 两层主 consumer；同时也把 `analysis_reduced_diags.py` 与 `analysis_reduced_diags_load_balance_costs.py` 分别显式落回各自的 `1/4` 分布语义。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `qed` family-level 反向指针：已把 shared `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前统一服务 `10` 条 active regression，并稳定分成 `2/2/2/4` 四层主 consumer；同时也把 `analysis_breit_wheeler_yt.py`、`analysis_breit_wheeler_opmd.py`、`analysis_quantum_sync.py` 与 `analysis_schwinger.py` 分别显式落回各自的 `2/2/2/4` 分布语义。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `pml` family-level 总收口：已把 `analysis_default_regression.py` 那条 `6+1+1` mixed checksum surface 再补一轮并排一致性，明确把 `test_3d_pml_psatd_dive_divb_cleaning` 这条 `3D cleaning checksum-only sibling` 也显式挂回同一条 helper 汇总。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `pml` family-level 反向指针：已把剩余 shared analysis 与 restart helper 再补一轮并排一致性，明确写清 `analysis_pml_ckc.py`、`analysis_pml_yee.py`、`analysis_pml_psatd_rz.py` 与 `analysis_default_restart.py` 当前分别落回这组 active wiring 的 `1 / 1 / 1 / 2` 分布，也就是单条 CKC、单条 Yee、单条 RZ 与两条 restart 主消费者链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `pml` family-level 反向指针：已按当前 `pml/CMakeLists.txt` 修正 shared `analysis_default_regression.py` 的服务面计数，明确写清它当前统一服务 `8` 条 active regression，并稳定分成 `6+1+1` 三层 checksum surface；同时也把 `analysis_pml_psatd.py` 再补一轮并排一致性，明确写清它当前共享服务 `test_2d_pml_x_psatd` 与 `test_2d_pml_x_galilean` 两条 active baseline。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `plasma_lens` family-level 反向指针：已把 shared `analysis.py` 再补一轮并排一致性，明确写清它当前统一服务 `test_3d_plasma_lens`、`test_3d_plasma_lens_python`、`test_3d_plasma_lens_boosted`、`test_3d_plasma_lens_hard_edged`、`test_3d_plasma_lens_picmi` 和 `test_3d_plasma_lens_short` 这 6 条 active baseline，并共同固定消费同一个末态 `diags/diag1000084` analytic lens-chain main surface。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `particle_boundary_scrape` family-level 反向指针：已把 shared `analysis_scrape.py` 再补一轮并排一致性，明确写清它当前同时服务 `test_3d_particle_scrape` 与 `test_3d_particle_scrape_picmi` 两条 active baseline，并共同固定消费 `diag1000040 -> diag1000060` 这条双快照主容器删粒子主链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `particle_boundary_process` family-level 反向指针：已把 `analysis_absorption.py` 再补一轮并排一致性，明确写清它当前只服务唯一一条 active analysis 链 `test_3d_particle_absorption`，而同 family 的 `test_2d_particle_reflection_picmi` 仍停在输入脚本尾部自断言加 checksum 的 checksum-only 路径。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `particle_boundary_interaction` family-level 反向指针：已把 shared `analysis.py` 再补一轮并排一致性，明确写清它当前只服务唯一一条 active baseline `test_rz_particle_boundary_interaction_picmi`，并且与 helper 不是分离输出面，而是共同固定消费同一个 `diags/diag1/` openPMD 目录。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `particle_absorbing_boundary` family-level 反向指针：已把 shared `analysis.py` 再补一轮并排一致性，明确写清它当前只服务唯一一条 active baseline `test_1d_particle_absorbing_boundary`，并且与 helper 显式分成“`PhaseSpaceElectrons` reduced histogram tail-weight main consumer”与“分离的 `diagInst008000` final-plotfile checksum side surface”两层。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `ohm_solver_magnetic_reconnection` family-level 反向指针：已把 shared `analysis.py` 再补一轮并排一致性，明确写清它当前只服务唯一一条 active baseline `test_2d_ohm_solver_magnetic_reconnection_picmi`，并且与 helper 显式分成“`plane.dat` reduced reconnection-rate main consumer”与“分离的 `diag1000020` final-plotfile checksum side surface”两层。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `ohm_solver_em_modes` family-level 反向指针：已把 shared `analysis.py` 与 `analysis_rz.py` 再补一轮并排一致性，明确写清它们当前不是泛泛 family 脚本，而是分别只服务 `test_1d_ohm_solver_em_modes_picmi` 与 `test_rz_ohm_solver_em_modes_picmi` 两条 active regression，也就是这组 `1D + RZ` split 的两条 shared analysis consumer chain。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `ohm_solver_cylinder_compression` family-level 对齐：已把 shared `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前不是附加 side surface，而是整个 family 唯一自动消费者链，并稳定闭合成 `3D diag1000010 + RZ diag1000020` 的 `1+1 dual-main-surface checksum structure`。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `nodal_electrostatic` family-level 对齐：已把 shared `analysis.py` 再补一轮并排一致性，明确写清它当前只服务唯一一条 active baseline `test_3d_nodal_electrostatic_solver`，并与 helper 显式闭合成“reduced `chi_max` + photon-count zero-trigger main consumer”加“分离的 `diag1000010` final-plotfile checksum side surface”两层结构。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `warpx.do_pml_dive_cleaning` / `warpx.do_pml_divb_cleaning`：已把这两条参数一起再补硬一层，明确写清它们当前都不是泛泛“PML 清洗布尔”，而是先在 `WarpX::ReadParameters()` 里按 Cartesian/PSATD 默认链和全局 `do_dive_cleaning / do_divb_cleaning` companion 推导，再分别改写普通 PML 的 `ncompe/ncompb`、`pml_F_* / pml_G_*` 分配面，以及 `WarpXEvolvePML.cpp` 的 damping 分支和 moving-window 下的 `pml_F/pml_G` shift；其中 `do_pml_divb_cleaning` 还额外带着“非 PSATD 直接禁用、PSATD 下必须与 `do_pml_dive_cleaning` 同真同假”的硬限制。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `load_external_field` `analysis_time_scaling.py` family-level 反向指针：已把这条 shared analysis 再补一轮并排一致性，明确写清它当前不只是 `pf0/pfN` 的 `median` hard gate、`mean` soft gate 与 zero-target fallback，还在 `load_external_field/CMakeLists.txt` 里精确只服务 `4` 条 active time-dependent regression，也就是前面 family helper 已压实的 `2/2/4/3 four-way shared-analysis split` 里的 `4`。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `load_external_field` `analysis_3d.py` / `analysis_rz.py` / `analysis_default_restart.py` family-level 反向指针：已把这三条 shared analysis 再补一轮并排一致性，明确写清它们当前不只分别服务 `2/2/3` 条 active regression，还都已经显式落回相邻 helper 行那条 `2/2/4/3 four-way shared-analysis split`；这样 `load_external_field` 四条 shared analysis 现在都在 analysis-level 行本身闭合了 family 分布语义。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 PML companion 簇 family-level 收口：已把这组相邻参数再做一轮并排一致性，明确写清它们当前已经稳定分成四层，`do_pml_in_domain + pml_ncell + pml_delta` 负责几何与 sigma 剖面，`do_similar_dm_pml` 负责普通 PML 的 fine/coarse allocation graph，`pml_has_particles + do_pml_j_damping + v_particle_pml` 负责粒子/电流 source 与 damping 分支，而 `do_pml_dive_cleaning + do_pml_divb_cleaning` 则专门收口 Cartesian PSATD cleaning 子系统。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `open_bc_poisson_solver` family-level 对齐：已把 shared `analysis.py` 与 helper 再补一轮并排一致性，明确写清当前普通 FFT 与 sliced-FFT 两条 active baseline 统一共用 `diag2` openPMD `Ex/Ey` 的 Basseti-Erskine 主消费者链，同时也共用 `diag1000001` final-plotfile checksum side surface；这样这组 family 不再只是单条 baseline 细、shared analysis/helper 却没显式闭合总结构。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `projection_div_cleaner` family-level 对齐：已把 shared `analysis.py` 与 helper 再补一轮并排一致性，明确写清这组 active wiring 当前稳定分成 `1` 条 `RZ + analysis.py + checksum` 路径，以及 `3` 条脚本内自带 `divB` 强断言再叠加 checksum 的 PICMI 路径；相对地，helper 当前统一服务这 `1+3` 混合 family 的附加 checksum side surface。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `effective_potential_electrostatic` family-level 对齐：已把 shared `analysis.py` 再补一轮并排一致性，明确写清它当前只服务唯一一条 active baseline `test_3d_effective_potential_electrostatic_picmi`，并且与 helper 不是分离输出面，而是共同固定消费同一个 `diags/field_diag/` openPMD 目录。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `do_similar_dm_pml`：已把这条参数再补硬一层，明确写清它当前不只是“PML 是否使用类似母网格的 DistributionMapping”，而是 `WarpX::ReadParameters()` 读取后沿普通 `PML(...)` 构造链分别命中 fine/coarse 两套 allocation graph；它既控制 `pml_E/B/F/G`，也继续控制 `pml_j_*`、EB `pml_edge_lengths`、`MultiSigmaBox` 以及 PSATD PML spectral solver 的 `dm/cdm`，而 `RZ + FFT` 的 level-0 `PML_RZ(...)` 路径当前则完全旁路这条开关。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `warpx.do_pml_in_domain`：已把这条参数再补硬一层，明确写清它当前不只是“PML 在域内还是域外”，而是 `WarpX::ReadParameters()` 读取后同时进入普通 `PML(...)` 与 `PML_RZ(...)` 的几何构造链；在普通 PML 路径上，它会先决定是否把边界 regular box 收缩成 `grid_ba_reduced` 再生成 overlap 型 PML patch，并继续决定 `PML::Exchange(...)` 是走 valid-to-valid copy 还是只更新 regular ghost cells 的域外交互语义，同时还为 `do_pml_j_damping` 定义了 `in-domain-only` 的 companion 合法性边界。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `warpx.pml_delta`：已把这条参数再补硬一层，明确写清它当前不只是“PML 吸收剖面的特征深度”，而是 `WarpX::ReadParameters()` 读取后沿普通 `PML(...)` 构造链进入 `SigmaBox`，以 `fac = 4*c/(dx*delta^2)` 的形式直接决定 `sigma/sigma_star` 及其 `sigma_cumsum` 空间增长剖面；同时 refined/coarse PML 还会继续经过 `cdelta = delta/ref_ratio` 的 rescaling，并在 `ComputePMLFactors()` 中进一步派生成 `sigma*_fac` 指数阻尼因子，所以它控制的是 PML sigma-profile 的空间增长尺度，而不是 `pml_ncell` 那种几何层数。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `warpx.v_particle_pml`：已把这条参数再补硬一层，明确写清它当前不是泛泛“粒子 PML 特征速度”，而是 `WarpX::ReadParameters()` 先按 `c` 单位读取、再乘 `PhysConst::c` 物化成有量纲速度，然后作为 `v_sigma_sb` 一路传进 `PML -> SigmaBoxFactory -> SigmaBox`；真正被它直接改写的不是 `sigma/sigma_star` 本体，而是 `sigma_cumsum / sigma_star_cumsum` 及其派生累计因子里的 `1/v_sigma` 归一化时间尺度。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `warpx.pml_ncell`：已把这条 PML 厚度参数再补硬一层，明确写清它当前不只是“构造 PML 时传一个层数”，而是既进入普通 `PML(...)` 与 `RZ + FFT` 的 `PML_RZ(...)` 构造链，又作为 companion 继续进入 `GuardCellManager.cpp` 的 RZ+PSATD 域外 PML `ngFFT[0] = max(ngFFT[0], pml_ncell)` 下界，以及 RZ spectral solver 的 `realspace_ba / c_realspace_ba.growHi(0, pml_ncell)` 外扩链；相对地，`sigma` 剖面形状更多由相邻 `pml_delta` 控制，不是这条参数本身的直接 consumer。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `warpx.do_pml_j_damping`：已把这条 PML companion 再补硬一层，明确写清它当前不是泛泛“PML 中 J 衰减开关”，而是 `WarpX::ReadParameters()` 读取后先强制要求 `do_pml_in_domain = 1`，随后在主循环里以独立于 `pml_has_particles` 的 gate 插入 `DampJPML()`；这条 pass 又会继续 fanout 到 fine/coarse patch，并对 `pml_j_fp/pml_j_cp` 三分量按 `sigma_cumsum_fac / sigma_star_cumsum_fac` 执行 kernel 级 damping，同时只把 `particle_shape > 1 && maxLevel() > 0` 记成 warning，而不是新的兼容性 hard gate。
- [x] 2026-05-28：继续清理 `docs/parameter-map.md` 的 `warpx.pml_has_particles`：已把这条 PML companion 再补硬一层，明确写清它当前不是泛泛“PML 内是否传播粒子”，而是 `WarpX::ReadParameters()` 读取后，先在 `WarpXEvolve.cpp` 里决定是否执行 `CopyJPML()` 把 regular-grid `J` 复制进 `pml_j_*`，再在 `WarpXPushFieldsEM.cpp -> EvolveEPML.cpp` 里决定 EPML `E` 更新是否额外消费这些 `J` 项；相对地，普通 `PML(...)` 构造函数当前并不持久保存这条值，`RZ + FFT` 的 `PML_RZ` level-0 路径更是直接旁路它，所以它控制的是 PML current source 分支，而不是 PML 几何或分配。
- [x] 2026-05-28：继续清理 `docs/parameter-map.md` 的 `boundary.reflect_all_velocities`：已把这条 boundary companion 再补硬一层，明确写清它当前不是泛泛“反射时是否全翻速度”，而是 `PhysicalParticleContainer` 从全局 `ParmParse("boundary")` 读取、再复制进各 species `ParticleBoundariesData` 的 per-container runtime flag；真正命中时也不是直接改写所有边界，而是只有在 `ApplyBoundaryConditions() -> apply_boundaries(...)` 已先判定出某一轴发生 `Reflecting` 或 absorbing-stochastic-reflection 这类 sign-change 事件之后，才把原本“只翻命中法向分量”的行为升级成全动量翻号，并继续经过 `Cartesian / RZ / RSPHERE` 各自不同的速度分量重映射链。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `load_external_field` `test_3d_load_external_field_grid_picmi.json` / `test_3d_load_external_field_particle_picmi.json`：已把这两条 active 3D PICMI baseline 再补硬一层，明确写清它们当前都不是 checksum-only，而都是“同一个末态 `diag1000300` plotfile 上的 proton `x/y/z` 末态位置主消费者链 + 同面 additive checksum side surface”；两条路径的 producer 分叉也已补清，分别对应 grid-side `LoadInitialField` 与 particle-side `LoadAppliedField`。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `load_external_field` `analysis_default_restart.py`：已把这条 shared restart analysis 再补硬一层，明确写清它当前不是抽象“restart helper”，而是固定把当前 `_restart` 目录里的末态 plotfile 与 `cwd.replace("_restart", "")` 反解出的非 restart 同名末态 plotfile 做逐字段硬对照；它会对两边都 `yt.load + force_periodicity + level-0 covering_grid`，然后遍历全部 `field_list`，按 `amax(abs(dr-db)) / amax(abs(db))` 形式施加 `< 1e-12` 的最大误差 gate，而 benchmark 全零分量则退化成绝对误差必须为 `0`。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `load_external_field` 四条 `particle_time / particle_time_picmi / particle_multi_time / particle_multi_time_picmi` baseline：已再做一轮源码对齐，明确写清这四条 active regression 当前都不是“analysis/checksum 共吃同一输出面”，而都是“同一条 `diag1` 时间序列里的 `pf0=diag1000000` 与 `pfN=diag1000300` 交给 `analysis_time_scaling.py`，末态 `diag1000300` 单独交给 helper checksum”的 split-consumer 结构；同时也补清了 shared `analysis_time_scaling.py` 当前真实 gate 是 `|B0| > min_abs` mask 上的 `median` hard gate + `mean` soft gate，并且只有 `expected_ratio = 0.0` 的两条 `multi_time` 路径会启用 zero-target `effective-atol` fallback。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `load_external_field` `analysis_time_scaling.py`：已把这条 shared analysis 再补硬一层，明确写清它当前不是泛泛“比较两帧场值缩放比”，而是固定消费同一条 plotfile 时间序列里的 `pf0/pfN` 两帧，先在 `|B0| > min_abs` 的 mask 上构造 `BN/B0`，再把 `median` 作为主 gate、`mean` 作为 `10*rtol` 的软 gate；并且只有在 `expected_ratio = 0` 时才会把 `rtol` 提升成等效 `atol` 以避免纯零目标下相对容差失效。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `load_external_field` `test_rz_load_external_field_grid.json` / `test_rz_load_external_field_particles.json`：已把这两条 active RZ baseline 再补硬一层，明确写清它们当前都不是 checksum-only，而都是“同一个末态 `diag1000300` plotfile 上的 proton `r/z` 末态位置主消费者链 + 同面 additive checksum side surface”；两条路径的真正 producer 分叉也已补清，分别对应 theta-mode 的 grid external field 与 particle external field 装填。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `load_external_field` 三条 restart input-level 行：已把 `inputs_test_3d_load_external_field_particle_time_restart`、`inputs_test_rz_load_external_field_grid_restart` 与 `inputs_test_rz_load_external_field_particles_restart` 再补硬一层，明确写清它们当前都不是独立 producer，而都只是各自主线输入之上的单行 `amr.restart = ../.../chk000150` continuation split；真实命中的消费者链也都已补成“共享主线 producer -> `chk000150` restart split -> `analysis_default_restart.py` same-name final-plotfile reproducibility 对照 -> helper checksum side surface”。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `load_external_field` `test_3d_load_external_field_particle_time_restart.json`：已把这条 3D restart baseline 再补硬一层，明确写清它当前不是单频 `Bz` 缩放比主消费者链的直接延伸，而是把 restart run 的 `diag1000300` 与非 restart baseline 的同名末态 plotfile 交给 `analysis_default_restart.py` 做逐字段 reproducibility 对照，同时再把 restart 末态 `diag1000300` 单独交给 helper 做 checksum side surface；producer 侧则已补清它本体只有 `FILE = inputs_test_3d_load_external_field_particle_time` 加一行 `amr.restart = "../test_3d_load_external_field_particle_time/diags/chk000150"`，真实命中的是共享单频 particle-external-field 主线在 `chk000150` 之后的 restart continuation split。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `load_external_field` `test_3d_load_external_field_particle_multi_time.json`：已把这条原生多频 time baseline 再补硬一层，明确写清它当前不是“analysis/checksum 共吃同一输出面”，而是把同一条 `diag1` 时间序列里的 `pf0=diag1000000` 与 `pfN=diag1000300` 交给 `analysis_time_scaling.py` 做 `Bz` 相消主消费者链，同时再把末态 `diag1000300` 单独交给 helper 做 checksum side surface；producer 侧则显式命中 `particles.B_ext_particle_fields = b1 b2` 与 `cos(omega*t) / cos(2*omega*t)` 双时间依赖，并把 `omega` 专门选成在 `300` 步末态让两路时间因子变成 `+0.5` 与 `-0.5`，从而把 `Bz` 精确相消到 `0.0`。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `load_external_field` `test_3d_load_external_field_particle_multi_time_picmi.json`：已把这条多频 PICMI time baseline 再补硬一层，明确写清它当前不是“analysis/checksum 共吃同一输出面”，而是把同一条 `diag1` 时间序列里的 `pf0=diag1000000` 与 `pfN=diag1000300` 交给 `analysis_time_scaling.py` 做 `Bz` 相消主消费者链，同时再把末态 `diag1000300` 单独交给 helper 做 checksum side surface；producer 侧则显式命中两条 `LoadAppliedField(..., warpx_B_time_function=cos(omega*t) / cos(2*omega*t))`，并把 `omega` 专门选成在 `300` 步末态让两路时间因子变成 `+0.5` 与 `-0.5`，从而把 `Bz` 精确相消到 `0.0`。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `load_external_field` `test_3d_load_external_field_particle_time_picmi.json`：已把这条单频 PICMI time baseline 再补硬一层，明确写清它当前不是“analysis/checksum 共吃同一输出面”，而是把同一条 `diag1` 时间序列里的 `pf0=diag1000000` 与 `pfN=diag1000300` 交给 `analysis_time_scaling.py` 做 `Bz` 缩放比主消费者链，同时再把末态 `diag1000300` 单独交给 helper 做 checksum side surface；producer 侧则显式命中 `LoadAppliedField(..., warpx_B_time_function=\"cos(omega*t + phase)\")`，并把 `omega` 专门选成在 `300` 步末态让缩放因子精确落到 `0.5`。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `load_external_field` `analysis_default_regression.py`：已把这条 helper 再补硬一层，并按当前源码纠正服务面计数，明确写清它当前不是泛泛“本地 checksum helper”，而是在 `load_external_field/CMakeLists.txt` 里统一服务 11 条 active regression，并且全部都被钉在同一个末态 `diags/diag1000300` plotfile surface；相对地，主 consumer 当前则明确分裂成四条 shared analysis consumer chains，并且分布数已经压实为 `2/2/4/3`：`analysis_3d.py` 服务 2 条 3D PICMI 磁镜位置断言，`analysis_rz.py` 服务 2 条 RZ theta-mode 位置断言，`analysis_time_scaling.py` 服务 4 条时变外场缩放比 gate，而 `analysis_default_restart.py` 服务 3 条 restart-state reproducibility gate。因此这条 family 的真实结构现在更准确地收口成“shared final-plotfile checksum side surface + 2/2/4/3 four-way shared-analysis split”。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `open_bc_poisson_solver` `inputs_test_3d_open_bc_poisson_solver_sliced`：已把这条 sliced 输入再补硬一层，明确写清它当前本体其实只有 `FILE = inputs_test_3d_open_bc_poisson_solver` 之后再覆写一行 `warpx.use_2d_slices_fft_solver = 1`，也就是普通 open-boundary relativistic FFT Poisson producer 上的单参数求解器分叉；`diag2` openPMD `Ex/Ey` 主输出面与末态 `diag1000001` checksum side surface 都完全继承普通版，而 shared `analysis.py` 仍固定在同一 Basseti-Erskine 逐 `z` 切片消费者链上。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `nodal_electrostatic` `analysis_default_regression.py`：已把这条 helper 再补硬一层，明确写清它当前不是泛泛“本地 checksum helper”，而是在 `nodal_electrostatic/CMakeLists.txt` 里只服务 `test_3d_nodal_electrostatic_solver` 这一条 active regression，并被显式钉成 `--path diags/diag1000010`；相对地，shared `analysis.py` 当前完全绕过这条命令行参数，固定回读 `diags/reducedfiles/ParticleExtrema_beam_p.txt + ParticleNumber.txt` 去执行 `chi_max` 与 photon-count 的零触发 gate。因此这条 family 的真实结构现在已明确分成“reduced zero-trigger main consumer + separate final-plotfile checksum side surface”。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `effective_potential_electrostatic` `inputs_test_3d_effective_potential_electrostatic_picmi.py`：已把这条 input-level 行再补硬一层，明确写清它当前不是泛泛“PICMI front-end”，而是显式 materialize 一条完整的 3D effective-potential electrostatic runtime，包括 `warpx_serialize_initial_conditions=True`、按 `n_plasma/T_e/T_i/m_ion/sigma_0` 反推出 `lambda_e/v_te/v_ti/dt/diag_steps`、rank-0 序列化 `sim_parameters.dpkl`、零电势球形 `EmbeddedBoundary`、`warpx_effective_potential=True` 的 `ElectrostaticSolver`、以及共享 `diags/field_diag/` openPMD 主 surface；相邻 shared `analysis.py` 与 helper 当前都共同消费这一目录，而不是分离到独立 side surface。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `relativistic_space_charge_initialization` 邻接条目，并修正一处旧描述偏差：现已按源码重新确认 shared `analysis.py` 当前既不消费 `By`，也不是只断言 `Ex`；它实际会在同一末态 `diag1000001` plotfile 上按维度分支重建解析高斯电荷团 Coulomb 场，并对 3D 路径的 `Ex/Ey/Ez` 三个分量统一施加 `tolerance_rel = 0.175` 的 `np.allclose` 强断言。因此 `test_3d_relativistic_space_charge_initialization.json` 现在更准确地收口成“same-final-plotfile three-component Coulomb-field main consumer + fields-only additive checksum”，而不是旧文案里的 `Ex` 单分量 gate 加 `By≈Ex/c` side path。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `gaussian_beam` `inputs_test_3d_focusing_gaussian_beam_from_openpmd_prepare.py`：已把这条 prepare 行再补硬一层，明确写清它当前不是泛泛“openPMD 准备脚本”，而是在 `gaussian_beam/CMakeLists.txt` 里被单独注册成 `analysis=OFF + checksum=OFF` 的 dependency-only upstream producer；它固定 `np.random.seed(0)` 与 `125 GeV / 2e6 macroparticles / focal_distance = 4*sigmaz` 这一整套聚焦束团常量，先在焦点面生成 `x/y/z/ux/uy/uz` Gaussian 样本，再通过 `x/y -= (focal_distance-z)*u_{x,y}/u_z` 把横向位置推回上游，最后用 `openpmd_api` 实际写出同时供 native `external_file` 与 PICMI `FromFileDistribution` 两条 active baseline 共用的 `openpmd_generated_particles.h5`，并显式 materialize `weighting/mass/charge/positionOffset` 与 `momentum.unit_SI = m_e*c`。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `gaussian_beam` `inputs_test_3d_focusing_gaussian_beam_from_openpmd_picmi.py`：已把这条 PICMI input-level 行再补硬一层，明确写清它当前命中的是 `shared prepare -> FromFileDistribution` producer，并并排 materialize `./diags/openpmd/` closed-main-consumer surface 与 `diag1000000` checksum side surface。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `gaussian_beam` `test_3d_rotated_gaussian_beam.json`：已把这条 rotation 主线再补硬一层，明确写清它当前真实结构是 `openPMD` 粒子 closed main consumer + `diag1000000` checksum side surface，并和同 family 的 focusing / photons / `from_openpmd_picmi` 三条 closed-main-consumer baseline 对齐到同一粒度。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `gaussian_beam` `test_3d_focusing_gaussian_beam.json`：已把这条电子束主线再补硬一层，明确写清它当前真实结构是 `openPMD` 粒子 closed main consumer + `diag1000000` checksum side surface，并和同 family 的 `photons` / `from_openpmd_picmi` 两条 closed-main-consumer baseline 对齐到同一粒度。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `gaussian_beam` `test_3d_focusing_gaussian_beam_photons.json`：已把这条 photon-species active baseline 再补硬一层，明确写清它当前真实结构是 `openPMD` 粒子 closed main consumer + `diag1000000` checksum side surface，只是 producer 侧把电子束版的 `q_tot` 路径切成了 `species_type=photon + npart_real`。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `gaussian_beam` `test_3d_gaussian_beam_picmi.json`：已把这条 active baseline 再补硬一层，明确写清它当前是彻底的 checksum-only 路径，唯一自动消费者就是 `diag1000010` final plotfile，而双物种 `GaussianBunchDistribution` 与 diagnostics CLI surface 都只通过这张末态输出间接受约束。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `gaussian_beam` PICMI `from_openpmd` baseline 邻接条目：已把 `test_3d_focusing_gaussian_beam_from_openpmd_picmi.json` 再补硬一层，明确写清这条 active baseline 当前真实结构是 `shared prepare -> FromFileDistribution producer -> ./diags/openpmd/` closed main consumer + `diag1000000` checksum side surface，并和相邻 native 版的 `dangling analysis target` 形成直接对照。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `gaussian_beam` native `from_openpmd` baseline 邻接条目：已把 `test_3d_focusing_gaussian_beam_from_openpmd.json` 再补硬一层，明确写清这条 active baseline 当前真实结构是 `prepare -> external_file producer -> ./diags/openpmd/` 粒子主面 + `diag1000000` checksum side surface，只是名义上的 `analysis.py` 在本地 checkout 中仍然悬空，主消费者链没有真正闭合。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `gaussian_beam` native `from_openpmd` 邻接条目：已把 `inputs_test_3d_focusing_gaussian_beam_from_openpmd` 再补硬一层，明确写清这条 active regression 当前真实落成的是 `prepare -> external_file producer + ./diags/openpmd/` 粒子主面 + `diag1000000` checksum side surface，只是 CMake 声称的 `analysis.py` 在本地 checkout 中仍然悬空。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `gaussian_beam` helper 邻接条目：已把 `analysis_default_regression.py` 再补硬一层，明确写清它当前在整个 family 上不是单一 side surface，而是同时覆盖四条 `diag1000000` 分离 checksum side surface、一条 `analysis.py` 缺失下的 dangling wiring，以及 `test_3d_gaussian_beam_picmi` 这条 `diag1000010` checksum-only 主面。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `space_charge_initialization` helper / 2D baseline 邻接条目：已把 `analysis_default_regression.py` 与 `test_2d_space_charge_initialization.json` 再补硬一层，明确写清这组 active regression 当前都走 same-final-plotfile 结构，`analysis.py` 固定消费 `diag1000001` 上的解析 Coulomb 场对照，而 helper 只在同一 plotfile 上追加 fields-only checksum。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `load_density` helper / Cartesian baseline 邻接条目：已把 `analysis_default_regression.py` 与 `test_{1d,2d,3d}_load_density.json` 再补硬一层，明确写清这组 Cartesian active regression 当前都不是“主 analysis 与 checksum 分离到不同输出面”的结构，而是把同一个 `diags/diag/` openPMD 目录同时交给逐 iteration `rho`-to-density 解析闭合主消费者链和附加 checksum。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `electrostatic_dirichlet_bc` baseline 邻接条目：已把 `test_2d_dirichlet_bc{,_picmi}.json` 再补硬一层，明确写清这两条 active regression 当前都不是“主 analysis 与 checksum 分离到不同输出面”的结构，而是把同一个末态 `diag1000100` plotfile 同时交给 shared `analysis.py` 的边界 `phi(t)` 时间序列消费者链和附加 checksum。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `ohm_solver_cylinder_compression` baseline 邻接条目：已把 `test_{3d,rz}_ohm_solver_cylinder_compression_picmi.json` 再补硬一层，明确写清这两条 active regression 当前都没有独立 analysis，唯一自动消费者链就是 low-resolution test-branch 的 final plotfile checksum，分别固定落在 `diag1000010 --rtol 5e-4` 与 `diag1000020 --rtol 1e-6`。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `ohm_solver_cylinder_compression` input-level 邻接条目：已把 `inputs_test_{3d,rz}_ohm_solver_cylinder_compression_picmi.py` 再补硬一层，明确写清两条 active 路径当前都总是命中 `--test` 分支，都会并排 materialize file-backed + analytical `A_external`、Python 初始 `B_z(r)` loader 与单一 `ions` Grad-Shafranov producer，只是 3D / RZ 分别落到 `diag1000010` / `diag1000020` 这两张低分辨率 plotfile diagnostics surface。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `ohm_solver_cylinder_compression` helper 邻接条目：已把 `analysis_default_regression.py` 再补硬一层，明确写清它当前在整个 family 上不是附加 side surface，而是两条 active regression 的唯一自动消费者链，分别统一消费 3D `diags/diag1000010` 与 RZ `diags/diag1000020` 两张 final plotfile surface。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `ohm_solver_em_modes` helper 邻接条目：已把 `analysis_default_regression.py` 再补硬一层，并修正原条目里的文字残差，明确写清它当前只服务两条 active regression 的分离 final checksum surface：1D 分支的 `diags/field_diag000250` 和 RZ 分支的 `diags/diag1000100`；相对地，两条主 analysis 仍分别固定回读 reduced text / `field_diags` side surface。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `ohm_solver_ion_Landau_damping` / `ohm_solver_ion_beam_instability` helper 邻接条目：已把两条 `analysis_default_regression.py` 再补硬一层，明确写清它们当前都只是各自 active baseline 的独立 final-plotfile checksum side surface；相对地，`field_data.txt` 这条 reduced 主消费者链仍分别固定由 shared `analysis.py` 回读和消费。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `ohm_solver_magnetic_reconnection` helper 邻接条目：已把 `analysis_default_regression.py` 再补硬一层，明确写清它当前只是 `test_2d_ohm_solver_magnetic_reconnection_picmi` 的独立 `diags/diag1000020` plotfile checksum side surface；主 analysis 仍固定回读 `sim_parameters.dpkl + diags/plane.dat`，因此 helper 本身并不消费任何重联率数值 gate。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `ionization_dsmc` `analysis_default_regression.py`：已把这条 helper 的当前 family 服务面再补硬一层，明确写清它在 1D 四条 reaction path 上统一消费 `diags/diag` openPMD 目录，而在 3D 两条 ionization 变体上统一消费最终 `diags/diag1000250` plotfile，因此当前真实结构是 “1D openPMD checksum surfaces + 3D final-plotfile checksum surfaces” 的混合 side-consumer。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `capacitive_discharge` `analysis_1d.py` 与 `test_1d_background_mcc_picmi.json`：已把这条 1D background-MCC 分支再补硬一层，明确写清 `analysis_1d.py` 当前和 DSMC 分支一样，既不读 plotfile 也不读 openPMD，而是固定回读 `run_sim()` 尾部导出的 `ion_density_case_1.npy`，再与脚本内硬编码 Turner case-1 密度数组做单条 `np.allclose`；同时也补清这条 active regression 当前真实结构是 “averaged ion-density `.npy` main consumer + external Poisson-solver callback path + separate `diag1000050` checksum side surface”。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `capacitive_discharge` `analysis_dsmc.py`、`inputs_base_1d_picmi.py` 与 `test_1d_dsmc_picmi.json`：已把这条 1D DSMC 分支再补硬一层，明确写清 `analysis_dsmc.py` 当前既不读 plotfile 也不读 openPMD，而是固定回读 `run_sim()` 尾部 `np.save(...)` 落下来的 `ion_density_case_1.npy`，再与脚本内硬编码 Turner case-1 密度数组做单条 `np.allclose`；同时也补清这条 active regression 当前真实结构是 “averaged ion-density `.npy` main consumer + separate `diag1000050` checksum side surface”。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `ionization_dsmc` `analysis_ionization_dsmc_1d.py`：已把这条 shared 1D ionization analysis 再补硬一层，明确写清它当前把 `./diags/diag` 固定成输入、把 iteration 钉死在 `100`，只对 `uz > 1e-3` 的 `Hneutral/Hplus` fast-beam 粒子做 `weights * uz` 通量直方图重建，并与 `H_on_H2_ionization.dat` 截面表插值得到的双指数理论通量做双阈值 `allclose`；`Beam_fluxes.png` 只是 side output，不是额外 gate。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `collision` `analysis_collision_3d_isotropization.py` 与 `test_3d_collision_iso{,_subcycle}.json`：已把 shared isotropization analysis 和两条 active baseline 再补硬一层，明确写清 `analysis_collision_3d_isotropization.py` 当前只消费单个末态 plotfile，从最终电子分布重建 `Tx/Ty`，再与脚本内硬编码 `dt = 1.4e-17`、`ne = 1.116e28`、`CoulombLog = 2.0` 和 `nt = 100` 驱动的 isotropization ODE 理论解比较，并统一要求最坏相对误差 `< 5%`；同时也补清 `subcycle` 版当前真正新增的只是 `const_dt` 放大 10 倍但 `collision1.ndt_subcycle = 10` 保持碰撞步长不变的 runtime 分叉。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `collision` `analysis_collision_1d_correct_conservation.py` 与 `analysis_collision_1d_Bremsstrahlung.py`：已把这两条 1D 邻接 analysis 行再补硬一层，明确写清 `correct_conservation` 当前是真正的双快照主消费者链，直接从 `diag1000000/diag1000010` 读取 `ionsA/ionsB` 的加权三向总动量并按 `u=p/m` 重建相对论总动能，再分别对总动量漂移施加 `1e-14`、对总动能漂移施加 `1e-10` 的 gate；同时也补清 `Bremsstrahlung` 当前主消费的其实是 `diags/reducedfiles/particle_energy.txt`、`particle_momentum.txt` 与 `particle_number.txt` 三套 reduced ledger，并分别对总能量、总动量、末段 `dE/dx` 与每步新生 photon 数施加源码内硬编码阈值。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `collision` `analysis_collision_1d.py` 与 `test_1d_collision_z.json`：已把 shared 1D analysis 和这条 active baseline 再补硬一层，明确写清 `analysis_collision_1d.py` 当前只消费单个末态 `diag1000600`，在 analysis 侧按粒子权重把同一 `ions` species 重新拆成 `groupA/groupB` 两群体，并只对低密度流入群体 A 的 `TApar` 相对 Higginson 2020 参考解 `6.15e3 eV` 施加 `< 2%` gate；同时也补清这条 active regression 当前是真正的 same-plotfile dual-consumer wiring，而不是 checksum-only。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `collision` `analysis_collision_rz.py` 与 `test_rz_collision.json`：已把 shared RZ analysis 和这条 active baseline 再补硬一层，明确写清 `analysis_collision_rz.py` 当前只锁定 `j=0/150` 两帧，并直接对所有粒子施加 `max(abs(px1-px2) + abs(py1-py2)) < 1e-15` 的首末横向动量不变 gate；同时也补清这条 active regression 的 checksum wiring 不是普通共面消费，而是 `analysis_default_regression.py --path diags/diag1000150 --skip-particles` 的 fields-only side surface。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `collision` `analysis_collision_3d.py` 与 `test_3d_collision_xyz.json`：已把 shared 3D analysis 和这条 active baseline 再补硬一层，明确写清 `analysis_collision_3d.py` 当前消费的是整段 `diag1` plotfile 时间序列、对电子/离子平均 `v_x` 差值做指数拟合 gate，并且 unlike 2D PICMI 分支，它总会继续检查 `diag_parser_filter/diag_uniform_filter/diag_random_filter` 三套 3D 粒子筛选 diagnostics；同时也补清 `test_3d_collision_xyz` 当前真实结构是 “time-series main consumer + additive checksum”，producer 侧还额外挂出 `ndt_supercycle = 10`。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `collision` `analysis_collision_2d.py` 与 `test_2d_collision_xz_{global_debye,picmi}`：已把 shared analysis 和两条 active baseline 再补硬一层，明确写清 `analysis_collision_2d.py` 当前消费的是整段 `diag1` plotfile 时间序列、对电子/离子平均 `v_x` 差值做指数拟合 gate，并且只有 native 路径才继续检查 `diag_parser_filter/diag_uniform_filter/diag_random_filter`；同时也补清 `global_debye` 版当前真实命中的是 `use_global_debye_length = 1 + CoulombLog = -1.0` 的 runtime 分叉，而 PICMI 版当前真实命中的是 `Cartesian2DGrid + Simulation + in-process execution` 前端，并显式跳过第二阶段的粒子筛选 diagnostics 检查。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `collision` split-momentum 三条 active baseline：已把 `test_2d_collisions_split_momentum_push_{electrostatic,electromagnetic,electromagnetic_vay}.json` 再补硬一层，明确写清这三条回归当前都不是 checksum-only，而是共享同一条 `diags/reducedfiles/field_energy.txt + particle_energy.txt` reduced-energy 主分析链，并分别通过 `warpx.do_electrostatic = labframe`、`algo.current_deposition = esirkepov`、`algo.particle_pusher = vay` 形成不同 runtime 分叉，同时把 `diags/diag1/` 保留为独立 openPMD checksum side surface。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `collision` `test_2d_charge_exchange_dsmc` 邻接条目：已把 `analysis_test_2d_collisions_split_momentum_push.py` 与 `test_2d_charge_exchange_dsmc.json` 再补硬一层，明确写清这条 active regression 当前不是“analysis/checksum 共吃同一输出面”，而是由共享 reduced-energy analysis 固定消费 `diags/reducedfiles/field_energy.txt + particle_energy.txt` 来做 electrostatic 分支下的总能量 / equipartition gate，再由 helper 单独消费 `diags/diag1/` openPMD checksum；同时也补清 producer 侧实际命中的是 `electrons + Heplus + He` electrostatic DSMC charge-exchange scaffold。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `collision` helper / `pulsed_decay` 邻接条目：已把 `analysis_collision_3d_pulsed_decay.py`、`analysis_default_regression.py` 与 `test_3d_collision_pulsed_decay.json` 再补硬一层，明确写清 `collision` family 的 helper 当前实际服务的是混合 `plotfile/openPMD` checksum surface，而 `test_3d_collision_pulsed_decay` 当前不是“analysis/checksum 共吃同一输出面”，而是由主 analysis 固定消费 `diags/reduced_files/particle_number.txt` 来重建 0D 高斯衰变模型并对最终 ion 总权重施加 `< 0.5%` gate，再由 helper 单独消费 `diag1025000` 末态 plotfile checksum。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `boundaries` helper/baseline 邻接条目：已把 `analysis_default_regression.py` 与 `test_3d_particle_boundaries.json` 再补硬一层，明确写清这条 active regression 当前不是 checksum-only，而是由主 analysis 同时消费末态 `diag1000008` 与反解出的初态 `diag1000000` 来执行 reflecting / absorbing / periodic 三类粒子的 relativistic 解析推进与边界映射断言，再由 helper 对同一个 `diag1000008` 末态 plotfile 叠加附加 checksum；同时也确认 helper 在这条 family 上实际只命中 plotfile 分支。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `pierce_diode` family 条目：已把 `analysis_pierce_diode.py`、`inputs_test_1d_pierce_diode` 与 `plot_sim.py` 再补硬一层，明确写清这条 family 当前是 1D electrostatic Child-Langmuir diode producer，主 analysis 只在最终 openPMD iteration 上对 `phi/jz` 两个量施加 `< 20%` 的相对误差 gate，而 `plot_sim.py` 只是复现 README 里 `u_z/E_z/J_z/phi` 四幅图的 README figure helper。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `pierce_diode` baseline/helper 条目：已把 `analysis_default_regression.py` 与 `test_1d_pierce_diode.json` 再补硬一层，明确写清这条 active regression 当前不是 checksum-only，而是把主 analysis 与附加 checksum 同时绑定到同一个 `diags/diag1/` openPMD 目录；其中主 analysis 只对最终 iteration 的 `phi/jz` 施加 `< 20%` 相对误差 gate，而 helper 在这条 family 上实际只命中 openPMD 分支。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `plasma_mirror` helper 条目：已把 `analysis_default_regression.py` 再补硬一层，明确写清 `plasma_mirror` 当前唯一 active wiring 只把最终 `diags/diag1000020` plotfile 交给 checksum helper，因此它在这条 family 上实际上只命中 plotfile 分支；同时也再次确认本地并不存在独立 reflectivity / harmonic analysis。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `spacecraft_charging` helper/baseline 邻接条目：已把 `analysis_default_regression.py` 与 `test_rz_spacecraft_charging_picmi.json` 再补硬一层，明确写清这条 active regression 当前把主 analysis 与附加 checksum 同时绑定到同一个 `diags/diag1/` openPMD 目录，因此 helper 的 plotfile 分支在这条 family 上实际上没有被命中，而 `phi_min(t)` 的 `v0/tau` 指数拟合 gate 仍完全由主 analysis 消费。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `thomson_parabola_spectrometer` helper/baseline 条目：已把 `analysis_default_regression.py` 与 `test_3d_thomson_parabola_spectrometer.json` 再补硬一层，明确写清这条 active regression 当前不是“analysis/checksum 共吃同一输出面”，而是由主 analysis 固定消费 `diag0 + screen/particles_at_zhi` 两条 openPMD 粒子 side channel 来重建 `detect.png`，再由 helper 单独消费 `diags/diag1` checksum surface。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `uniform_plasma` helper/restart 邻接条目：已把 `analysis_default_regression.py` 与 `test_3d_uniform_plasma_restart.json` 再补硬一层，明确写清这组 family 当前三条 active wiring 都只把 `diag1000010` plotfile 交给 checksum helper，因此 openPMD 回退分支在本 family 上没有被命中；同时 restart 变体的主 analysis 与附加 checksum 也都是叠加在同一个末态 `diag1000010` plotfile 上。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `uniform_plasma` 2D 主线条目：已把 `test_2d_uniform_plasma.json` 再补硬一层，明确写清它并不共用 3D 的 `inputs_base_3d`，而是一张独立 2D 周期热电子输入卡；当前只落一个末态 `diag1000010` Full plotfile，并由 checksum helper 作为唯一自动消费者链消费。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `virtual_photons` helper/baseline 条目：已把 `analysis_default_regression.py` 与 `test_3d_virtual_photons.json` 再补硬一层，明确写清本 family 当前 active wiring 只把 `diags/diag1` openPMD 粒子目录交给主 analysis 和 checksum helper 共同消费，因此 helper 的 plotfile 分支在本 family 上没有被命中，而总数/能谱/坐标三条主合同仍完全由 `analysis_virtual_photons.py` 负责。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `virtual_photons` beamsize-effect 条目：已把 `test_3d_beamsize_effect.json` 再补硬一层，明确写清这条 active regression 和 `test_3d_virtual_photons` 一样，也是主 analysis 与 checksum helper 共用同一个 `diags/diag1` openPMD 粒子目录；其中主 analysis 只消费单次粒子输出，并对 beam-size smearing 开/关两支虚光子云施加三条不对称位置合同。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `collider_relevant_diags` helper/baseline 条目：已把 `analysis_default_regression.py`、`inputs_test_3d_collider_diagnostics` 与 `test_3d_collider_diagnostics.json` 再补硬一层，明确写清这条 active regression 当前不是“analysis/checksum 共吃同一输出面”，而是由主 analysis 固定消费 `reducedfiles/*.txt + diag2 openPMD + warpx_used_inputs` 来交叉校验 `chi`、散射角统计和 `dL/dt`，再由 helper 单独消费 `diag1000001` plotfile checksum surface。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `boosted_diags` helper/baseline 条目：已把 `analysis.py`、`analysis_default_regression.py` 与 `test_3d_laser_acceleration_btd.json` 再补硬一层，明确写清这条 active regression 当前由主 analysis 同时消费 `diag1000003` plotfile 与固定 `diag2/openpmd_%T.h5` side channel 来校验双 BTD writer 一致性和 `beam.random_fraction = 0.5` 子采样，再由 checksum helper 对同一个 `diag1000003` plotfile 叠加附加基线。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `plasma_lens` Python baseline 条目：已把 `test_3d_plasma_lens_python.json` 再补硬一层，明确写清这条 active regression 当前不是 checksum-only，而是固定绑定到 shared `analysis.py diags/diag1000084`；producer 侧通过 `pywarpx` 顶层参数对象直接物化 repeated-plasma-lens 参数表并走 `warpx.init(); warpx.step(max_step)`，consumer 侧则继续对最终 `x/y` 位置与 `ux/uy` 动量施加默认 `2% / 0.2%` 相对误差 gate。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `plasma_lens` PICMI baseline 条目：已把 `test_3d_plasma_lens_picmi.json` 再补硬一层，明确写清这条 active regression 当前不是 checksum-only，而是固定绑定到 shared `analysis.py diags/diag1000084`；producer 侧通过 `Cartesian3DGrid + dual ParticleListDistribution + PlasmaLens applied-field + sim.step(max_steps)` 物化 repeated-plasma-lens 前端，consumer 侧则优先读取 `electrons.dist0/dist1.*` 这组 PICMI 参数，再继续对最终 `x/y` 位置与 `ux/uy` 动量施加默认 `2% / 0.2%` 相对误差 gate。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `plasma_lens` short baseline 条目：已把 `test_3d_plasma_lens_short.json` 再补硬一层，明确写清这条 active regression 当前虽然会每一步落一帧 `diag1`，但 CMake 仍只把末态 `diag1000084` 交给 shared `analysis.py`；同时也补清 short-lens 分叉真正新增的是 residence-correction 场景，以及 analysis 会把位置/速度容差从默认 `0.02 / 0.002` 放宽到 `0.023 / 0.003`。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `plasma_lens` boosted baseline 条目：已把 `test_3d_plasma_lens_boosted.json` 再补硬一层，明确写清这条 active regression 当前不是 checksum-only，而是固定绑定到 shared `analysis.py diags/diag1000084`；producer 侧只在主线 repeated-plasma-lens scaffold 上新增 `warpx.gamma_boost = 2` 与改写后的 `z` 几何域，consumer 侧则先把末态 `z` 反变换回 lab frame，再继续对最终 `x/y` 位置与 `ux/uy` 动量施加默认 `2% / 0.2%` 相对误差 gate。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `plasma_lens` baseline 条目：已把 `test_3d_plasma_lens.json` 再补硬一层，明确写清这条 active regression 当前不是 checksum-only，而是固定绑定到 shared `analysis.py diags/diag1000084`，由它从两颗末态测试电子回放 repeated-plasma-lens 解析链，并对最终 `x/y` 位置与 `ux/uy` 动量施加默认 `2% / 0.2%` 相对误差 gate，再附加 checksum。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `spacecraft_charging` 条目：已把 shared `analysis.py` 与 `test_rz_spacecraft_charging_picmi.json` 再补硬一层，明确写清主 analysis 当前把 `diags/diag1/` 当成 openPMD `phi_min(t)` 时间序列，按脚本内固定 `dt = 1.27e-8` 还原时间后拟合 `v0 * (1-exp(-t/tau))`，并对 `(v0, tau)` 相对基准的误差施加 `4%/20%` 双阈值；同时也补清这条 active regression 只有在 `WarpX_EB` 打开时才会注册，并附加 `diags/diag1/` checksum。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `plasma_mirror` baseline 条目：已把 `inputs_test_2d_plasma_mirror` 与 `test_2d_plasma_mirror.json` 再补硬一层，明确写清这条 active regression 当前是独立 native 2D laser-solid 输入卡，内联 Gaussian `laser1`、`electrons/ions` 双 species 与带前后 exponential ramp、中心 `2*nc` plateau 的固体靶；同时也补清它虽然会落出 `diag1000010` 与 `diag1000020` 两帧 Full plotfile，但 CMake 实际只消费最终 `diag1000020` checksum，且 WarpX 自带 `README.rst` 仍明确标注 PICMI/Analyze 都还是 TODO。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `plasma_acceleration` 3D PICMI baseline 条目：已把 `inputs_test_3d_plasma_acceleration_picmi.py` 与 `test_3d_plasma_acceleration_picmi.json` 再补硬一层，明确写清这条 active regression 当前是 `Cartesian3DGrid + ElectromagneticSolver + Simulation(max_steps=10)` 的 3D moving-window PICMI front-end，直接用 period=`max_steps` 的 `diag1` field/particle surface 原地跑到 `diag1000010`；同时也补清脚本没有独立 input-file materialization，且 WarpX 自带 `README.rst` 仍明确把这条 PICMI 路径标成尚未启用 boosted frame 的 TODO。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `plasma_acceleration` 1D PICMI baseline 条目：已把 `inputs_test_1d_plasma_acceleration_picmi.py` 与 `test_1d_plasma_acceleration_picmi.json` 再补硬一层，明确写清这条 active regression 当前是 `Cartesian1DGrid + ElectromagneticSolver + Simulation(max_steps=1000)` 的 1D moving-window PICMI front-end，直接用 period=`max_steps` 的 `diag1` field/particle surface 原地跑到 `diag1001000`；同时也补清脚本没有独立 input-file materialization，且 WarpX 自带 `README.rst` 仍明确把这类 PICMI 路径标成尚未启用 boosted frame 的 TODO。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `plasma_acceleration` 2D boosted baseline 条目：已把 `inputs_test_2d_plasma_acceleration_boosted` 与 `test_2d_plasma_acceleration_boosted.json` 再补硬一层，明确写清它当前不是 shared `inputs_base_2d` 的 overlay，而是一张独立 2D boosted 输入卡，直接内联 `gamma_boost = 10`、rigid `driver/beam`、`species_type = electron/hydrogen` 的 `plasma_e/plasma_p`、`parse_density_function` 余弦 ramp-to-plateau plasma 与 `do_continuous_injection = 1`；同时也补清这条 active regression 当前没有独立 analysis 或中间 diagnostics gate，真正自动消费的只是最终 `diag1000020` 的 20-step smoke checksum surface。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `plasma_acceleration` boosted baseline 条目：已把 `inputs_test_3d_plasma_acceleration_boosted` 与 `test_3d_plasma_acceleration_boosted.json` 再补硬一层，明确写清这条 active regression 当前输入侧本体几乎只有 `FILE = inputs_base_3d + max_step = 5`，真正命中的仍是 shared boosted PWFA 主骨架，其中包括 rigid `driver/beam`、反向补偿 `driverback`、余弦 ramp-to-plateau `plasma_e/plasma_p` 与 `do_continuous_injection = 1`；同时也补清它当前没有独立 analysis 或中间 diagnostics gate，真正自动消费的只是最终 `diag1000005` 的 5-step smoke checksum surface。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `plasma_acceleration` 2D MR gather 分叉条目：已把 `inputs_test_2d_plasma_acceleration_mr_momentum_conserving` 与 `test_2d_plasma_acceleration_mr_momentum_conserving.json` 再补硬一层，明确写清它相对普通 `mr` 版当前唯一新增的 runtime 分叉就是 `algo.field_gathering = momentum-conserving`，并且两条回归连最终 writer surface 都完全共形，都会只落出并消费同一个 `diag1000400` checksum 面。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `ohm_solver_magnetic_reconnection` 邻接条目：已把 `analysis.py` 与 `test_2d_ohm_solver_magnetic_reconnection_picmi.json` 再补硬一层，明确写清 shared analysis 当前固定回读 `sim_parameters.dpkl + diags/plane.dat`，先重排平面探针数据再输出 `diags/reconnection_rate.png`；只有在 `not sim.test` 分支上才会继续消费 `diags/fields/*.npz` 去生成 `mag_reconnection.mp4` 场线动画，且这条动画链不参与自动 gate。与此同时，这条 active regression 当前真实结构也补成了“`plane.dat` reduced reconnection-rate main consumer + 独立 `diag1000020` final-plotfile checksum side surface”。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `ohm_solver_ion_beam_instability` baseline wiring：已把 `test_1d_ohm_solver_ion_beam_picmi.json` 再补硬一层，明确写清这条 active regression 当前不是“analysis/checksum 共吃同一输出面”，而是由 shared `analysis.py` 固定消费 `diags/field_data.txt` 这条 reduced growth-rate surface，在 resonant 分支上对 `m=4,5,6` 三个 Fourier 模于 `10 < tΩ_i < 40` 窗口内的 RMS 偏差施加源码内硬编码 `np.isclose` gate；外层 helper 则只对独立的末态 `diags/diag1002500` plotfile 做附加 checksum。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `ohm_solver_ion_beam_instability` 邻接条目：已把 `analysis.py` 与 `inputs_test_1d_ohm_solver_ion_beam_picmi.py` 再补硬一层，明确写清 shared analysis 当前固定回读 `sim_parameters.dpkl + diags/field_data.txt`，先重排 `By(z,t)` 栈并输出全时空 stack plot，再在 resonant 分支上只对 `m=4,5,6` 三个 Fourier 模于 `10 < tΩ_i < 40` 窗口内的 RMS 偏差施加源码内硬编码 `np.isclose` gate；同时也补清 1D active input 当前真实命中的是 `--test --dim 1 --resonant` 分支下的双离子漂移 producer，其中 `field_data.txt` 是主增长率 surface，`diag1002500` 是 checksum side surface，而 `energies.npy/openpmd_004000.h5` 只属于离线 side output。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `ohm_solver_ion_Landau_damping` shared analysis 条目：已把 `analysis.py` 再补硬一层，明确写清它当前固定回读 `sim_parameters.dpkl + diags/field_data.txt`，先按 `step` 重排 `Ez(z,t)` 栈并做空间 FFT，再只取第 `m` 阶 Fourier 模的衰减轨迹，与 Munoz et al. (2018) Fig. 14b 硬编码表按 `T_ratio` 插值得到的理论阻尼率曲线叠图；整个脚本当前没有任何 `assert`，自动 gate 仍主要来自外层 `diag1000100` checksum。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `ohm_solver_em_modes` 1D 邻接条目：已把 `analysis.py` 再补硬一层，明确写清这条 shared Cartesian analysis 当前不是独立强回归，而是固定回读 `sim_parameters.dpkl + diags/par_field_data.txt|perp_field_data.txt` 的 reduced-text side consumer，先重排时间/空间堆栈再做 2D FFT，并把 parallel `R/L` 或 perpendicular `X/Bernstein` 理论色散线叠到命名谱图上；整个脚本当前没有任何 `assert`，自动 gate 仍主要来自外层 checksum。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `ohm_solver_em_modes` RZ 邻接条目：已把 `analysis_rz.py` 与 `inputs_test_rz_ohm_solver_em_modes_picmi.py` 再补硬一层，明确写清 shared RZ analysis 当前固定回读 `sim_parameters.dpkl + diags/field_diags`，对 `E_y` 做径向插值、手写 Hankel 投影和 `z/t` 双 FFT，生成完整 `F_kw` 频谱与 `spectrograms.npz/normal_modes_disp.png`，并只在 `sim.test` 条件下对四个固定振幅样本做 `np.allclose`；同时也补清输入侧真实命中的是 `--test` 分支下的 `CylindricalGrid + HybridPICSolver + AnalyticInitialField(Bz)` metallic-cylinder producer，并把 `field_diags` 与 `diag1000100` 分别压实成主 analysis surface 与独立 checksum side surface。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `plasma_acceleration` 相邻 baseline 条目：已把 `test_3d_plasma_acceleration_mr_picmi.json` 与 `test_3d_plasma_acceleration_boosted_hybrid.json` 再补硬一层，明确写清前者当前是在 non-boosted PICMI front-end 内硬编码 `grid.add_refined_region(...)`、两步 in-process 执行后只落 `diag1000002` 的 checksum surface；后者则是在 shared boosted PWFA 主骨架上只切到 `warpx.grid_type = hybrid + warpx.do_current_centering = 0`，并在 `diag1.intervals = 10000` 不变的前提下把 smoke 长度拉到 `25` 步，最终仍只消费 `diag1000025`。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `plasma_acceleration` helper 条目：已把目录内 `analysis_default_regression.py` 的真实服务面补硬，明确写清这组 8 条 active PWFA application regression 当前全部都是 `analysis=OFF + analysis_default_regression.py --path ...` 的纯 checksum surface、没有独立 physics consumer；同时也补清 `test_3d_plasma_acceleration_picmi` 在 WarpX 自带 `README.rst` 里仍被明确标注为尚未启用 boosted frame，因此当前真实命中的是 non-boosted PICMI front-end 路径。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `laser_ion` 主线条目：已把 `analysis_test_laser_ion.py`、`test_2d_laser_ion_acc.json` 与 `test_2d_laser_ion_acc_picmi.json` 一起补硬，明确写清 shared analysis 当前只在 native 路径真正执行 `diagInst` 末 5 帧 `E_z` 后处理平均对 `diagTimeAvg` 原位平均的 `rtol=1e-12` 强断言；而 PICMI 路径虽然在 CMake 上已经绑了同一个 analysis，但由于脚本里的 `TODO: implement intervals parser for PICMI`，当前运行时会直接跳过这条 physics gate，只剩附加 checksum。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `laser_acceleration` 1D boosted fluid 支线：已把 `analysis_1d_fluid_boosted.py`、`inputs_test_1d_laser_acceleration_fluid_boosted` 与 `test_1d_laser_acceleration_fluid_boosted.json` 一起补硬，明确写清这条 active regression 当前固定命中独立的 `fluids.species_names = electrons ions` boosted fluid WFA producer、native Gaussian laser、`BackTransformed` diagnostics，以及末态 `diag1000001` 上 `Ez/Jz/rho` 相对脚本内 nonlinear fluid ODE 理论解的最坏误差 `< 0.30` consumer，再附加 checksum。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `laser_acceleration` 2D MR PICMI 支线：已把 `inputs_test_2d_laser_acceleration_mr_picmi.py` 与 `test_2d_laser_acceleration_mr_picmi.json` 一起补硬，明确写清这条 active regression 当前不是 shared `inputs_base_2d` 的薄封装，而是直接在 PICMI front-end 内 materialize `64 x 512` moving-window 网格、`refined_regions=[[1,[-5,-35] um,[5,-25] um]]`、常密度 plasma、Gaussian `beam`、Gaussian laser 与 `inputs_2d_picmi` materialization + in-process execution 链；对应 baseline 则固定走 `analysis=OFF + analysis_default_regression.py --path diags/diag1000200` 的 final checksum consumer。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `laser_acceleration` helper / RZ openPMD 条目：已把目录内 `analysis_default_regression.py` 的真实服务面补硬，明确写清它当前同时服务 4 条带独立 analysis 的变体和 11 条 `analysis=OFF + checksum` workflow；同时也把 `inputs_test_rz_laser_acceleration_opmd` 与 `test_rz_laser_acceleration_opmd.json` 一起补硬，明确写清这条 active regression 当前固定绑定到 RZ openPMD writer 的 iteration-count、mesh-shape、per-species `rho` 排序与物理中心位置消费者链，再附加 checksum。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `refined_injection` 主线条目：已把 `analysis_refined_injection.py`、`inputs_test_2d_refined_injection` 与 `test_2d_refined_injection.json` 一起补硬，明确写清这条 active regression 当前不是 checksum-only，而是固定绑定到末态 `diag1000200` 上的粒子总账本 gate 和 refinement-edge 前方 `rho` 线切片 `<0.5%` 均匀性 gate；同时也补清输入侧真实命中的是 shared `inputs_base_2d` 上 `amr.ref_ratio_vect = 2 1 + warpx.refine_plasma = 1` 的窄 producer 分叉。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `rigid_injection` 主线条目：已把 `analysis_rigid_injection_{btd,lab}.py`、`inputs_test_2d_rigid_injection_{btd,lab}` 与 `test_2d_rigid_injection_{btd,lab}.json` 一起补硬，明确写清 BTD 版当前固定消费 plotfile/openPMD 双 `BackTransformed` 粒子输出并对 lab-frame 束宽施加强断言，而 lab 版当前固定消费末态 rigid-beam 束宽与初态 `orig_z / center` runtime-attribute materialization gate，再附加 checksum。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `laser_acceleration` 3D 余项 active baseline 行：已把 `test_3d_laser_acceleration_python.json` 与 `test_3d_laser_acceleration_single_precision_comms.json` 一起补硬，明确写清前者当前覆盖的是 native `inputs_base_3d` 经 `sim.load_inputs_file(...)` 载入后的 Python-extension runtime 与双 `afterstep` callback 可达性路径，而后者当前覆盖的是 shared `inputs_base_3d` 上唯一新增的 `warpx.do_single_precision_comms = 1` communication/runtime 分叉，再附加同一 `diags/diag1/` checksum consumer。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `btd_rz` 主线条目：已把 shared `analysis.py`、`inputs_test_rz_btd` 与 `test_rz_btd.json` 一起补硬，明确写清这条 active regression 当前不是 checksum-only，而是固定绑定到 `back_rz` openPMD `iteration=1` 的轴上 `Ex(z)` 相位中心拟合消费者链，再附加 `diag1000289` checksum；同时也补清输入侧真实命中的是 `RZ + gamma_boost=10 + moving window + native Gaussian laser + BackTransformed openPMD` 的 producer scaffold。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `laser_acceleration` 3D / RZ active baseline 行：已把 `test_3d_laser_acceleration{,_picmi}.json` 与 `test_rz_laser_acceleration{,_picmi}.json` 一起补硬，明确写清前两条当前分别覆盖 shared `inputs_base_3d` 的 native 3D moving-window LWFA producer 与 PICMI front-end `inputs_3d_picmi` materialization + in-process execution 链，而后两条则固定走 `diag1000010` checksum wiring，其中 RZ PICMI 版还额外压实了 `inputs_rz_picmi` 的 quasi-cylindrical front-end 与 in-process execution 路径。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `laser_acceleration` 2D active baseline 行：已把 `test_2d_laser_acceleration_boosted.json` 与 `test_2d_laser_acceleration_mr.json` 一起补硬，明确写清前者当前覆盖的是独立 2D boosted-frame LWFA 输入卡、parabolic plasma channel、rigid beam、BackTransformed 三帧 plotfile producer 与 `diag1000002` checksum consumer，而后者当前覆盖的是共享 `inputs_base_2d` 的 moving-window、level-1 refined patch、continuous-injection plasma、Gaussian beam/laser 与 `diag1000200` checksum consumer。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `laser_acceleration` 1D active baseline 行：已把 `test_1d_laser_acceleration.json` 与 `test_1d_laser_acceleration_picmi.json` 一起补硬，明确写清前者当前覆盖的是 native `inputs_base_1d` 的 moving-window、continuous-injection plasma、runtime attributes、Gaussian laser 与末态 `diag1000100` checksum consumer，而后者当前覆盖的是对应 PICMI front-end、`inputs_1d_picmi` materialization、in-process execution 与同一末态 checksum consumer。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `boundaries` 主线条目：已把 shared `analysis.py` 再补硬一层，明确写清它当前固定消费初末态双 plotfile，按 `particle_id` 对三组粒子做 relativistic 解析推进，并分别对 `reflecting / absorbing / periodic` 三类 domain boundary 施加速度翻号、粒子删减和显式 wrap/reflect 位置断言，再附加 checksum。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `accelerator_lattice` 主线条目：已把 shared `analysis.py` 与 `inputs_test_3d_hard_edged_quadrupoles{,_boosted,_moving}` 一起补硬，明确写清共享 consumer 当前固定走“递归 lattice 展开 + optional boosted-to-lab `z` backtransform + 单粒子 hard-edged quadrupole 解析末态对照”，并把三条输入各自 materialize 的 lab-frame / boosted-frame / moving-window producer 分叉压到 input-level。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `uniform_plasma_restart` 邻近 helper/baseline 行：已把目录内 `analysis_default_restart.py` 与 `test_3d_uniform_plasma_restart.json` 一起补硬，明确写清这条 active restart regression 当前固定走 `chk000006 -> analysis_default_restart.py diags/diag1000010 -> analysis_default_regression.py --path diags/diag1000010 --rtol 1e-12` 的链路，并对 restart run 与非 restart run 的最终 `diag1000010` 做全 `field_list` 逐字段 reproducibility 对照。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `free_electron_laser` 主线条目：已把 `analysis_fel.py`、`inputs_test_1d_fel` 与 `test_1d_fel.json` 一起补硬，明确写清这条 active regression 当前不是 checksum-only，而是固定绑定到 lab-frame `diag_labframe` 与 boosted-frame `diag_boostedframe` 两条 openPMD diagnostics 的双分支 gain-length / radiation-wavelength 消费者链；同时也补清输入侧真实命中的是 `rigid` e-/e+ 共流束抵消 space-charge、particle-side undulator `B_y(z)` 与 `BackTransformed`/boosted-frame 双 writer 的 1D ponderomotive-frame FEL producer。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `boosted_diags` 主线条目：已把 `inputs_test_3d_laser_acceleration_btd` 与 `test_3d_laser_acceleration_btd.json` 一起补硬，明确写清它当前命中的是 boosted-frame LWFA scaffold 上双 `BackTransformed` writer 的 producer，以及 `analysis.py` 对 `diag1` plotfile / `diag2` openPMD 的 `Ez` 逐点一致性和 `beam.random_fraction = 0.5` 粒子子采样数量合同，再附加 checksum。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `laser_injection_from_file` analysis/helper 行：已把 `analysis_{1d,1d_boost,2d,2d_binary,3d,rz,from_RZ_file}.py` 一起补硬，明确写清它们当前都只消费单个末态 `Ey/Et` 场面，并分别按脚本内硬编码的 Gaussian 或 Laguerre-Gaussian 理论包络，对整场 Hilbert envelope 误差和 FFT 主频误差施加统一 `< 0.065` 的双断言；同时也补清目录内 `analysis_default_regression.py` 当前只是七条 `prepare -> from_file injection -> physics analysis` active regression 旁边的附加 checksum 链。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `laser_injection` active baseline 行：已把 `test_{1d,2d}_laser_injection{,_implicit}.json` 一起补硬，明确写清这四条回归当前都不是简单 checksum 基线，而是分别固定绑定到 `analysis_{1d,2d}.py` 的 six-component envelope/frequency 消费者链，再附加 checksum；同时也把 implicit 变体与普通卡的真实 producer 分叉压实到 `semi_implicit_em + newton/gmres` 这一层。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `linear_compton` 与 `nci_fdtd_stability` active baseline 行：已把 `test_3d_linear_compton_{bunch_laser,two_particles}.json` 与 `test_2d_nci_corrector{,_mr}.json` 一起补硬，明确写清这些回归当前都不是简单 checksum 基线：前两条分别固定绑定到 bunch-laser 动量/Klein-Nishina 产额消费者链与 two-particle complete-conversion 消费者链，而后两条则都固定走 `analysis_ncicorr.py + checksum`，并把 MR 阈值分支在当前可见 wiring 下尚未显式闭环选通的状态写实。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `maxwell_hybrid_qed` 与 `linear_breit_wheeler` active baseline 行：已把 `test_2d_maxwell_hybrid_qed_solver.json`、`test_3d_linear_breit_wheeler_many_photons.json` 与 `test_3d_linear_breit_wheeler_two_photons.json` 一起补硬，明确写清这些回归当前都不是 checksum-only，而是分别固定绑定到 hybrid-QED 相速度强断言、many-photon pair-yield 时间历程消费者链和 two-photon complete-conversion 消费者链，再附加 checksum。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `qed` family 条目：已把 `analysis_breit_wheeler_core.py`、`analysis_breit_wheeler_{yt,opmd}.py`、`analysis_quantum_sync.py`、`analysis_schwinger.py`、三条 shared/input-level producer 行，以及 `test_{2d,3d}_qed_breit_wheeler{,_opmd}`、`test_{2d,3d}_qed_quantum_sync` 和 `test_3d_qed_schwinger_{1..4}` 一组 active baseline 一起补硬，明确写清这些回归当前都不是泛泛“checksum 基线”，而是分别固定绑定到 Breit-Wheeler 粒子合同、Quantum Synchrotron photon-product 合同和单帧 Schwinger rate-window consumer，再附加 checksum。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `beam_beam_collision` family 条目：已把 `inputs_test_3d_beam_beam_collision` 与 `test_3d_beam_beam_collision.json` 一起补硬，明确写清这条 active regression 当前仍只有 `analysis=OFF + analysis_default_regression.py --path diags/diag1/` 的 checksum surface，但输入侧实际覆盖的是 relativistic electrostatic self-field、Quantum Synchrotron、nonlinear Breit-Wheeler，以及 `ColliderRelevant/ParticleNumber` reduced diagnostics 的联合 collider-QED workflow，而 `plot_fields.py` / `plot_reduced.py` 仍只是离线可视化 helper。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `thomson_parabola_spectrometer` family 条目：已把 `analysis.py`、`inputs_test_3d_thomson_parabola_spectrometer` 与 `test_3d_thomson_parabola_spectrometer.json` 一起补硬，明确写清这条 active regression 当前不是 checksum-only，而是固定绑定到 `analysis.py + analysis_default_regression.py --path diags/diag1`；共享 analysis 实际固定消费 `screen/particles_at_zhi` 与 `diag0` 两条 openPMD 粒子输出，通过 `id` 回连把 detector hits 重建成按 species 与初始能量着色的 TPS 分离图。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `virtual_photons` family 条目：已把 `analysis_virtual_photons.py`、`analysis_beamsize_effect.py`、目录内 `analysis_default_regression.py`、两条 input-level 行与 `test_3d_virtual_photons.json` / `test_3d_beamsize_effect.json` 一起补硬，明确写清这两条 active regression 当前都不是 checksum-only，而是分别固定绑定到 virtual-photon 总数/能谱/坐标一致性消费者链，以及 beam-size-effect 开/关两支虚光子云的 `rho_max` 半径与坐标 A/B 几何断言链。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `uniform_plasma` active baseline 行：已把 `test_3d_uniform_plasma.json` 再压实一层，明确写清它当前虽然外层仍只是 `analysis=OFF + analysis_default_regression.py --path diags/diag1000010` 的 checksum 路径，但真正命中的 producer 合同来自 shared `inputs_base_3d` 的 3D 周期热电子 workflow，同时它还承担 `test_3d_uniform_plasma_restart` 的 `chk000006` checkpoint producer 角色。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `vay_deposition` family 条目：已把 shared `analysis.py`、顶层 `analysis_default_regression.py`、两条 input-level 行与 `test_2d_vay_deposition.json` / `test_3d_vay_deposition.json` 一起补硬，明确写清这两条 active regression 当前都不是 checksum-only，而是固定绑定到 `analysis.py + analysis_default_regression.py`；共享 analysis 实际只消费末态全域 `rho/divE` 数组，并对离散 Gauss-law 最坏相对误差施加 `1e-3` 单阈值断言，而 2D/3D 输入侧则分别 materialize 出 `periodic + PSATD + collocated + current_deposition=vay + particle_pusher=vay` 的双单粒子 producer。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `subcycling` family 条目：已把 `inputs_test_2d_subcycling_mr` 与 `test_2d_subcycling_mr.json` 一起补硬，明确写清这条 active regression 当前固定命中 `2D CKC + level-1 refined patch + do_subcycling = 1 + moving window + continuous-injection plasma + particles.deposit_on_main_grid` 这条 producer，但没有独立 physics analysis，只把末态 `diag1000250` 交给附加 checksum。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `single_particle` family 条目：已把 `analysis.py`、`analysis_default_regression.py`、`analysis_synchronize_velocity.py`、两条 input-level 行与 `test_2d_bilinear_filter.json` 一起补硬，明确写清 `2D bilinear_filter` 当前固定消费末态全域 `jx` 数组并对脚本内硬编码的 bilinear 卷积理论值施加 `< 1e-14` 相对误差断言，而 `1D synchronize_velocity` 当前没有 checksum，主合同只落在 `analysis_synchronize_velocity.py` 对单帧同步后 `u_z` 的 `1e-15` 标量相对误差 gate。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `silver_mueller` family 条目：已把共享 `analysis.py`、`inputs_test_rz_silver_mueller_z` 与 `test_rz_silver_mueller_z.json` 一起补硬，明确写清这条 active regression 当前固定走 `analysis.py diags/diag1000500 + analysis_default_regression.py --path diags/diag1000500`，并且主 analysis 实际会按 `warpx_used_inputs` 在 Cartesian/RZ 两个分支间切换，对末态全域 `Ex/Ey/Ez` 或 `Er/Et/Ez` 逐单元施加 `0.01 V/m` 阈值断言。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `scraping` family input-level 行：已把 `inputs_test_rz_scraping` 与 `inputs_test_rz_scraping_filter` 一起补硬，明确写清普通版本当前 materialize 的是 `RZ + level-1 refined cylindrical EB + inward ring-electron cloud + diag1/diag2/diag3` 的 triple producer，而过滤版本只在此基础上新增 `diag3.electron.plot_filter_function = "z > 0"` 这条 scraped-writer 半域记录分叉。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `restart` family 里 `inputs_base_3d` 与 `inputs_test_3d_acceleration*` 一组条目：已把 shared producer、三条 non-restart baseline、三条 restart input-level 行一起补硬，明确写清 `inputs_base_3d` 当前 materialize 的 `CKC + boosted-frame + moving-window + rigid bunch + parabolic channel + laser + diag1/chk@5` 主链，以及 `PSATD/Galilean`、`time-averaged PSATD` 和 `amr.restart=../.../chk000005` 这些实际 runtime 分叉；同时也补清三条 restart 变体当前统一落到 `analysis_default_restart.py diags/diag1000010 + analysis_default_regression.py --path diags/diag1000010` 的全字段 restart reproducibility consumer。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `restart` family 里 `2D PICMI Python particle interface` 分支：已把目录内 `analysis_default_regression.py` / `analysis_default_restart.py`、`inputs_test_2d_id_cpu_read_picmi.py`、`inputs_test_2d_runtime_components_picmi.py` 与两条对应 active baseline 一起补硬，明确写清 `idcpu` 路径当前是脚本内 `unpack_ids/unpack_cpus -> ids_sum/cpu_sum == 5050/0` 强断言，而 runtime-components 路径当前是 `newPid` 跨 checkpoint continuation 的脚本内一致性自检，并伴随一条 analysis/checksum 仍关闭的 `FIXME` restart scaffold。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `resampling` family 行：已把 `analysis.py`、三条 input-level 行和三条 active baseline 一起补硬，明确写清两条 `1D velocity_coincidence_thinning` 当前都只是 `analysis=OFF + diags/diag1000004 checksum`，分别命中 spherical velocity grid 与 cartesian `delta_u` 分箱 producer；同时也补清 `test_2d_leveling_thinning` 当前固定消费 `diag1000000/diag1000008` 两帧 `particle_weight` 样本，并对两类 species 的 level-weight / leveled / unaffected 统计施加显式断言。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `repelling_particles` family 行：已把 `analysis.py`、`analysis_default_regression.py`、`inputs_test_2d_repelling_particles` 与 `test_2d_repelling_particles.json` 一起补硬，明确写清这条 active regression 当前不是 checksum-only，而是沿完整 `diag10000*` 时序逐帧读取两颗粒子的 `x/p_x`，再对双单粒子的 `beta(d)` 解析能量账本施加 `np.allclose(..., atol=0.01)` 双断言；同时也补清了输入侧的 `two-static-electron + initialize_self_fields + diag1@20` producer 面。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `pml` input-level 行：已把 `inputs_test_rz_pml_psatd` 再补硬一层，明确写清它当前 materialize 的是 `RZ + n_rz_azimuthal_modes = 2`、`r_hi = pml`、单电子径向外冲的 PSATD producer，末态 `diag1000500` 实际落的是 `Bt Er Ez jr jt jz rho`，并被共享的 `analysis_pml_psatd_rz.py + analysis_default_regression.py` 双消费者链共同消费。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `pml` active baseline 行：已把 `test_rz_pml_psatd.json` 再补硬一层，明确写清它当前不是 checksum-only，而是固定绑定到 `analysis_pml_psatd_rz.py diags/diag1000500 + analysis_default_regression.py --path diags/diag1000500`；输入侧末态 `diag1000500` 实际落的是 `Bt Er Ez jr jt jz rho`，共享 analysis 则对全域最大残余 `max(|Er|,|Ez|)` 施加 `< 2.0` gate。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `pml` active baseline 行：已把 `test_2d_pml_x_yee.json` 再补硬一层，明确写清它当前不是 checksum-only，而是固定绑定到 `analysis_pml_yee.py diags/diag1000300 + analysis_default_regression.py --path diags/diag1000300`；共享 analysis 只消费单个末态 plotfile 的六个场分量，并用脚本内置 `energy_start = 9.1301289517e-08` 与 `Reflectivity_theory = 5.683000058954201e-07` 做 `< 5%` 的单理论反射率 gate。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `pml` active baseline 行：已把 `test_2d_pml_x_ckc.json` 再补硬一层，明确写清它当前不是 checksum-only，而是固定绑定到 `analysis_pml_ckc.py diags/diag1000300 + analysis_default_regression.py --path diags/diag1000300`；共享 analysis 只消费单个末态 plotfile 的六个场分量，并用脚本内置 `energy_start = 9.1301289517e-08` 与 `Reflectivity_theory = 1.8015e-06` 做 `< 5%` 的单理论反射率 gate。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `pml` active baseline 行：已把 `test_2d_pml_x_galilean.json` 再补硬一层，明确写清它当前不是 checksum-only，而是固定绑定到 `analysis_pml_psatd.py diags/diag1000300 + analysis_default_regression.py --path diags/diag1000300`；同时共享 analysis 会因工作目录名命中 `galilean` 而把 `energy_start` 切到 `4.439376202529614e-08`，再对 `diag1000050` 的参考能量一致性和末态 `< 1e-6` 反射率做双层 gate。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `pml` active baseline 行：已把 `test_2d_pml_x_psatd.json` 再补硬一层，明确写清它当前不是 checksum-only，而是固定绑定到 `analysis_pml_psatd.py diags/diag1000300 + analysis_default_regression.py --path diags/diag1000300`；共享 analysis 还会额外回读 `diag1000050`，先校准 `energy_start_diags` 与脚本内置 `7.282940112203595e-08` 的一致性，再对末态反射率施加 `< 1e-6` gate。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `pml` helper-level 行：已把顶层 `Examples/analysis_default_regression.py` 再补硬一层，明确写清它当前会按 cwd 推导基线名、自动探测 `plotfile/openPMD`、并在 `_restart` 工作目录下把默认容差切到 `1e-12`；在 `pml` family 里它当前服务的是 2D `ckc/yee/psatd/galilean`、两条 restart 变体、3D cleaning workflow 和 RZ PSATD 的附加 checksum 链。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `pml` helper-level 行：已把顶层 `Examples/analysis_default_restart.py` 再补硬一层，明确写清它当前固定走 `yt.load + force_periodicity + level-0 covering_grid`，并遍历 benchmark 的全部 `field_list` 做 `< 1e-12` 的最大误差 gate；在 `pml` family 里当前只服务 `test_2d_pml_x_psatd_restart` 与 `test_2d_pml_x_yee_restart` 两条末态 `diag1000300` 对照链。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `pml` input-level 行：已把 `inputs_test_3d_pml_psatd_dive_divb_cleaning` 再补硬一层，明确写清它当前 materialize 的是 `32^3` 全 `pml` 3D 盒子、三束沿 `+x/+y/+z` 的对称 Gaussian laser，以及四个 `divE/divB` cleaning 开关全开的 PSATD producer；下游则没有独立 physics analysis，只把末态 `diag1000100` 的 `Bx By Bz Ex Ey Ez rho` 字段面交给 checksum helper。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `pml` restart input-level 行：已把 `inputs_test_2d_pml_x_yee_restart` 再补硬一层，明确写清它当前除了新增 `amr.restart = ../test_2d_pml_x_yee/diags/chk000150` 之外，其余 Yee-PML producer 都完整继承自主线；下游则固定收缩成 `analysis_default_restart.py diags/diag1000300 + analysis_default_regression.py --path diags/diag1000300`，并对最终 plotfile 的全部 `field_list` 做 `< 1e-12` 的逐字段 restart 对照。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `pml` restart input-level 行：已把 `inputs_test_2d_pml_x_psatd_restart` 再补硬一层，明确写清它当前除了新增 `amr.restart = ../test_2d_pml_x_psatd/diags/chk000150` 之外，其余 plain-PSATD PML producer 都完整继承自主线；下游则固定收缩成 `analysis_default_restart.py diags/diag1000300 + analysis_default_regression.py --path diags/diag1000300`，并对最终 plotfile 的全部 `field_list` 做 `< 1e-12` 的逐字段 restart 对照。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `pml` input-level 行：已把 `inputs_test_2d_pml_x_yee` 再补硬一层，明确写清它当前除了把 `algo.maxwell_solver` 切到 `yee` 之外，`max_step = 300`、`128 x 512` 全 `pml` 盒子、单束 Gaussian laser、`diag1@50` 和 `chk@150` 都继续完整继承自 `inputs_base_2d`；下游消费者则固定收缩成 `analysis_pml_yee.py + analysis_default_regression.py --path diags/diag1000300`。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `pml` input-level 行：已把 `inputs_test_2d_pml_x_ckc` 再补硬一层，明确写清它当前除了把 `algo.maxwell_solver` 切到 `ckc` 之外，`max_step = 300`、`128 x 512` 全 `pml` 盒子、单束 Gaussian laser、`diag1@50` 和 `chk@150` 都继续完整继承自 `inputs_base_2d`；下游消费者则固定收缩成 `analysis_pml_ckc.py + analysis_default_regression.py --path diags/diag1000300`。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `flux_injection` analysis-level 行：已把 `analysis_flux_injection_3d.py` 再补硬一层，明确写清它当前只消费被 CMake 钉死传入的单个末态 `diags/diag1000002` plotfile，而且完全不读场数组；脚本尾部虽会额外生成 `Distribution.png`，但这张图不属于自动消费者合同。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `flux_injection` analysis-level 行：已把 `analysis_flux_injection_rz.py` 再补硬一层，明确写清它当前只消费被 CMake 钉死传入的单个末态 `diags/diag1000120` plotfile，并且只读取 `particle_position_x` 与 `particle_weight`，即便上游输入专门保留了 `Bz`，主 analysis 也完全不读场数据。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `flux_injection` input-level 行：已把 `inputs_test_3d_flux_injection` 再补硬一层，明确写清它虽然把 `diag1.intervals` 写成 `1000`，但 active 注册实际仍把主 analysis 和 checksum 都钉死到末态 `diags/diag1000002`，而且共享 `analysis_flux_injection_3d.py` 当前完全不读场数据，只消费四个 species 的粒子动量和权重直方图。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `flux_injection` input-level 行：已把 `inputs_test_rz_flux_injection` 再补硬一层，明确写清它把 `electron.num_particles_per_cell` 压到 `1`，diagnostics 虽然只落 `Bz`，但下游主 analysis 实际完全不读场，只消费最终时刻的 `particle_position_x` 与 `particle_weight` 来检查 Larmor 半径带和总注入量。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `flux_injection` input-level 行：已把 `inputs_test_2d_flux_injection_from_eb` 再补硬一层，明确写清它真正只覆写 2D 网格、几何盒子和全周期边界，而球形 EB、有限发射时间窗、`gaussianflux` 动量分布、`algo.maxwell_solver = none` 以及 `diag1.intervals = 10 + fields_to_plot = none` 的 particle-only producer 面都继续完整继承自 `inputs_base_from_eb`。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `flux_injection` base-level 行：已把 `inputs_base_from_eb` 再补硬一层，明确写清它是 `test_3d_flux_injection_from_eb`、`test_rz_flux_injection_from_eb` 与 `test_2d_flux_injection_from_eb` 三条 active regression 共同继承的唯一发射/runtime 基座，而且 `diag1.fields_to_plot = none` 直接把整个 from-EB family 当前的主消费者限定成 particle-only 链。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `flux_injection` input-level 行：已把 `inputs_test_3d_flux_injection_from_eb` 再补硬一层，明确写清它真正只覆写 3D 网格、几何盒子和全周期边界，而球形 EB、有限发射时间窗、`gaussianflux` 动量分布、`algo.maxwell_solver = none` 以及 `diag1.intervals = 10 + fields_to_plot = none` 的 particle-only producer 面都继续完整继承自 `inputs_base_from_eb`。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `flux_injection` input-level 行：已把 `inputs_test_rz_flux_injection_from_eb` 再补硬一层，明确写清它真正只覆写 `RZ` 几何、边界、网格和 `electron.num_particles_per_cell = 300`，而球形 EB、有限发射时间窗、`gaussianflux` 动量分布以及 `diag1.intervals = 10 + fields_to_plot = none` 的 particle-only producer 面都继续完整继承自 `inputs_base_from_eb`。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `flux_injection` analysis-level 行：已把 `flux_injection/analysis_flux_injection_from_eb.py` 再补硬一层，明确写清它是 `test_3d_flux_injection_from_eb`、`test_rz_flux_injection_from_eb` 与 `test_2d_flux_injection_from_eb` 三条 active regression 共享的唯一主 analysis，维度分流依赖本地 `warpx_used_inputs` 而不是 plotfile 元数据，而且当前只消费 `electron` 粒子数组；脚本尾部虽会额外生成 `Distribution.png`，但这张图不属于自动消费者合同。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `flux_injection` active baseline 行：已把 `test_3d_flux_injection_from_eb.json` 再补硬一层，明确写清共享 `analysis_flux_injection_from_eb.py` 虽然还会额外生成 `Distribution.png` 作为人工可视化副产物，但 active 注册真正钉死的自动消费者仍只有末态 `diags/diag1000020` plotfile 上的 3D 几何重建、总发射量和法/切向速度分布断言，加附加 checksum。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `flux_injection` active baseline 行：已把 `test_2d_flux_injection_from_eb.json` 再补硬一层，明确写清共享 `analysis_flux_injection_from_eb.py` 虽然还会额外生成 `Distribution.png` 作为人工可视化副产物，但 active 注册真正钉死的自动消费者仍只有末态 `diags/diag1000020` plotfile 上的 2D 几何重建、总发射量和法/切向速度分布断言，加附加 checksum。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `flux_injection` active baseline 行：已把 `test_rz_flux_injection_from_eb.json` 再补硬一层，明确写清共享 `analysis_flux_injection_from_eb.py` 虽然还会额外生成 `Distribution.png` 作为人工可视化副产物，但 active 注册真正钉死的自动消费者仍只有末态 `diags/diag1000020` plotfile 上的 RZ->3D 几何重建、总发射量和法/切向速度分布断言，加附加 checksum。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `flux_injection` active baseline 行：已把 `test_rz_flux_injection.json` 再补硬一层，明确写清虽然输入侧还额外挂出 `diag1.fields_to_plot = Bz`，但主 analysis 实际只消费末态粒子的 `r/w` 统计，不读取或断言这张 `Bz` 场面；自动消费者当前只落在 Larmor 半径带、总注入量和附加 checksum 上。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `flux_injection` active baseline 行：已把 `test_3d_flux_injection.json` 再补硬一层，明确写清这条 regression 的主 analysis 虽然还会额外生成 `Distribution.png` 作为人工可视化副产物，但 active 注册真正钉死的自动消费者仍只有末态 `diags/diag1000002` plotfile 上的四物种逐分量直方图断言，加附加 checksum。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `flux_injection` helper-level 行：已把 `flux_injection/analysis_default_regression.py` 再补硬一层，明确写清这条脚本虽然支持 `plotfile/openpmd` 自动探测，但 `flux_injection` 当前五条 active 注册都只把末态 `diags/diag1000002`、`diags/diag1000120` 或 `diags/diag1000020` plotfile 路径传给它；因此 openPMD 分支在这整个 family 上其实没有被触发。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `embedded_circle` active baseline 行：已把 `test_2d_embedded_circle.json` 再补硬一层，明确写清这条 regression 虽然运行时会同时产出每步 plotfile `diag1` 和每 5 步 openPMD `BoundaryScraping` `diag3`，但 active 注册当前只把末态 `diags/diag1000011` 交给 checksum helper，而且还通过 CMake 把默认容差从 `1e-9` 放宽到了 `1e-2`。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `embedded_circle` helper-level 行：已把 `embedded_circle/analysis_default_regression.py` 再补硬一层，明确写清虽然输入同时产出 plotfile `diag1` 和 openPMD `BoundaryScraping` `diag3`，但 `embedded_circle` 当前唯一 active 注册只把 `diags/diag1000011` plotfile 交给 helper，而且还通过 CMake 显式把 checksum 容差放宽到了 `1e-2`；因此 openPMD 分支在这条 active 路径上并没有被触发。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `embedded_boundary_cube` helper-level 行：已把 `embedded_boundary_cube/analysis_default_regression.py` 再补硬一层，明确写清它虽然支持 `plotfile/openpmd` 自动探测，但 `embedded_boundary_cube` 当前三条 active 注册都只把末态 `diags/diag1000114` 或 `diags/diag1000208` plotfile 路径传给它；因此 openPMD 分支在这组 cavity regression 上其实没有被触发。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `embedded_boundary_cube` analysis-level 行：已把 `embedded_boundary_cube/analysis_fields.py` 再补硬一层，明确写清共享 3D analysis 虽然会先分配 `Bx_th/By_th/Bz_th` 三套解析数组，但当前只真正 materialize 并强断言 `By/Bz`；`Bx` 与同一末态 plotfile 里的 `Ex/Ey/Ez` 仍只留给附加 checksum 覆盖。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `embedded_boundary_cube` active baseline 行：已把 `test_3d_embedded_boundary_cube.json` 再补硬一层，明确写清共享 `analysis_fields.py` 虽然会分配 `Bx_th/By_th/Bz_th` 三套解析数组，但当前只读取并强断言 `By/Bz`；同一末态 plotfile 里的 `Bx` 与 `Ex/Ey/Ez` 仍只落在附加 checksum 覆盖面里。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `embedded_boundary_cube` active baseline 行：已把 `test_3d_embedded_boundary_cube_macroscopic.json` 再补硬一层，明确写清这条回归与普通 3D cavity baseline 当前消费的是同一路径 `diags/diag1000208`，plotfile 本身并不自描述 `epsilon_r = 1.5` 介质分支；共享 `analysis_fields.py` 只能靠工作目录名里的 `macroscopic` 语义来决定是否把本征频率额外除以 `sqrt(1.5)`。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `embedded_boundary_cube` active baseline 行：已把 `test_2d_embedded_boundary_cube.json` 再补硬一层，明确写清虽然 `inputs_test_2d_embedded_boundary_cube` 通过 `diag1.intervals = 1` 每步落盘 Full plotfile，但 active consumer 当前只钉死读取末态 `diags/diag1000114`；而共享 `analysis_fields_2d.py` 仍只对 `By` 做硬断言，对 `Ey/c` 只计算误差不判定。
- [x] 2026-05-28：继续清理 `docs/parameter-map.md` 的 tiling/creation companion 行：已把 `particles.do_tiling` 再补硬一层，明确写清这条开关不只命中常规 `AddParticles(...)` 和 `AddPlasma(...)`，`AddPlasmaFlux()` 这条 flux-injection 创建链也同样会在 `Gpu::notInLaunchRegion()` 下先 `EnableTiling(tile_size)`；因此它当前共同覆盖 volume/flux 两类粒子创建链，但仍不扩展到通用 `WarpXParIter` 推进/碰撞/沉积循环。
- [x] 2026-05-28：继续清理 `docs/parameter-map.md` 的 scheduling/creation companion 行：已把 `warpx.do_dynamic_scheduling` 再补硬一层，明确写清这条开关当前不只被 `AddPlasma()`、多 species helper 和 binary collision 旁路，`AddPlasmaFlux()` 这条 flux-injection 创建链也同样固定 `info.SetDynamic(true)`；因此它真正只控制 `WarpXParIter` 驱动的默认粒子循环调度，不是所有粒子 `MFIter`/OMP 路径的统一总开关。
- [x] 2026-05-28：继续清理 `docs/parameter-map.md` 的 initialization family companion 行：已把 `warpx.serialize_initial_conditions` 再补硬一层，明确写清这条开关不只旁路 `AddPlasmaFlux()/AddPlasmaFromFile()`，而且连同一个 `AddParticles()` 总入口里的 `single_particle`、`multiple_particles`、`gaussian_beam` 也都不读它；它当前真正只命中 `doInjection() -> AddPlasma()` 这条 CPU/OpenMP volume-plasma 创建链及其 `ContinuousInjection()` 复用路径。
- [x] 2026-05-28：继续清理 `docs/parameter-map.md` 的 unused-input/finalize companion 行：已把 `amrex.abort_on_unused_inputs` 再补硬一层，明确写清这条开关当前不是“第一步发现 unused inputs 就立刻停机”的 tripwire；`WarpXEvolve.cpp` 的 early `QueryUnusedInputs()` 只会提示并继续跑完 `Evolve()` 尾部，真正的硬失败仍会被延后到 `WarpX::Finalize() -> amrex::Finalize() -> ParmParse::Finalize()` 这条 finalize-stack。
- [x] 2026-05-28：继续清理 `docs/parameter-map.md` 的 warning-manager companion 行：已把 `warpx.always_warn_immediately` 再补硬一层，明确写清这条开关不只改变 warning 的“立即打印 vs 稍后汇总”时机，还改变重复 warning 的呈现语义；即时 `amrex::Warning(...)` 当前不会走 `MsgLogger` 折叠链，因此同一条 warning 会逐次展开打印，而后续 local/global summary 才会把相同 `Msg` 聚合成单条并附带 `counter` 与 `ranks/all_ranks`。
- [x] 2026-05-28：继续清理 `docs/parameter-map.md` 的 communication precision companion 行：已把 `warpx.do_single_precision_comms` 再补硬一层，明确写清这条开关在 `AMREX_USE_FLOAT` 构建下会在 `WarpX::ReadParameters()` 里被直接覆写回 `false`；因此后续所有显式 wrapper consumer 都会统一退回 native/direct 通信分支，不再进入 `comm_float_type + mixedCopy` 辅助链。
- [x] 2026-05-28：继续清理 `docs/parameter-map.md` 的 guard-cell/communication companion 行：已把 `warpx.safe_guard_cells` 再补硬一层，明确写清 safe 模式并不是所有场族都统一退回 full-`nGrowVect()` 通信；`E_avg/B_avg/F/G` 会这么做，但 `FillBoundaryAux` 当前仍严格吃 `guard_cells.ng_UpdateAux`，所以 auxiliary-field 这条链的 effect 是“抬高 budget 合同”，不是再额外强制通信到每个 aux `MultiFab` 的完整分配上限。
- [x] 2026-05-28：继续清理 `docs/parameter-map.md` 的 communication helper companion 行：已把 `ablastr.fillboundary_always_sync` 再补硬一层，明确写清这条输入当前只作用于 helper-routed `FillBoundary(...)` 链，不是整个 `ablastr::utils::communication` 命名空间的总开关；同文件里的 `ParallelCopy / ParallelAdd / SumBoundary` 仍只按 `do_single_precision_comms` 分流，不会因为把它设成 `1` 就额外切成 nodal-sync 风格的同步通信。
- [x] 2026-05-28：继续清理 `docs/parameter-map.md` 的 AMReX-owned profiling/communication companion 行：已把 `amrex.use_profiler_syncs` 再补硬一层，明确写清这条开关当前只影响显式包了 `BL_PROFILE_SYNC_*` 的少数高层通信入口，如 `SyncBeforeComms: FB/PC/Redist`；大量同样运行在 `CommunicatorSub()` 域内的普通 `ParallelAllReduce/ParallelReduce` 并不会因为它设成 `1` 就自动多插 profiler barrier 或生成 `SyncBeforeComms:*` timer。
- [x] 2026-05-28：继续清理 `docs/parameter-map.md` 的 AMReX-owned unused-input companion 行：已把 `amrex.parmparse.verbose` 再补硬一层，明确写清这条值当前只 gate unused-input 明细打印，不 gate unused-input 检测结果本身；也就是说把它设成 `0` 只会压掉 `Unused ParmParse Variables:` 明细，不会阻止 `QueryUnusedInputs()` 返回真，也不会阻止 finalize 期 `abort_on_unused_inputs` 的硬失败。
- [x] 2026-05-28：继续清理 `docs/parameter-map.md` 的 warning/finalize companion 行：已把 `warpx.abort_on_warning_threshold` 再补硬一层，明确写清命中阈值的 warning 虽然会先记入内部 logger，且在 `always_warn_immediately=1` 时还会先即时 `amrex::Warning(...)` 输出，但随后会在本地 `RecordWarning(...)` 当场 abort；因此它通常来不及再进入 `WarpXEvolve.cpp` 里的 `PrintGlobalWarnings("FIRST STEP") / ("THE END")` 汇总链。
- [x] 2026-05-28：继续清理 `docs/parameter-map.md` 的 verbosity/finalize companion 行：已把 `warpx.verbose` 再补硬一层，明确写清 `main.cpp` 里的 `Total Time` 虽然受这条开关门控，但它位于 `WarpX::Finalize()` 返回之后；因此若同一次运行里 `amrex.abort_on_unused_inputs=1` 且 finalize 期仍有未消费参数，程序会先在 `ParmParse::Finalize()` 里 abort，即便 `warpx.verbose=1`，这条 `Total Time` 也来不及打印。
- [x] 2026-05-28：继续清理 `docs/parameter-map.md` 的 restart/diagnostics companion 行：已把 `warpx.write_diagnostics_on_restart` 再补硬一层，明确写清这条开关在 restart 首帧虽然会遍历非 BTD full diagnostics 与 reduced diagnostics，但 `BoundaryScraping` 当前既不从 checkpoint 恢复 pinned particle boundary buffer、又会在每次真正 flush 后立刻清空 buffer；因此它不会自动补出 checkpoint 前已经 scraped 但尚未落盘的粒子，restart 首帧若还没新 scraped 粒子，这条分支天然就是空跑。
- [x] 2026-05-28：继续清理 `docs/parameter-map.md` 的 step-loop verbosity companion 行：已把 `warpx.limit_verbose_step` 再补硬一层，明确写清这条开关虽然会把主循环 `verbose_step` 降采样成 `1/10/100` 步节奏，并继续传进 `doResampling(..., verbose_step)`，但在 resampling 链里当前只 gate 最后那条 `Resampled ...` stdout；`TotalNumberOfParticles()` 的全局同步、`m_resampler.triggered(...)`、`Redistribute()` 和真正的重采样 kernel 都不会因它被跳过，同时 `CheckLoadBalance(step)` 这类主循环路径也不消费这条 gate。
- [x] 2026-05-28：继续清理 `docs/parameter-map.md` 的 startup/output companion 行：已把 `warpx.used_inputs_file` 再补硬一层，明确写清 `WarpXInitData.cpp` 当前调用 `write_used_inputs_file(filename)` 时没有显式传第二参，而 helper 头文件把 `verbose` 默认成 `true`；也就是说，只要文件名不是空串或 `/dev/null`，startup 路径当前会默认向 stdout 打印 used-inputs 归档落点，再由 IO rank 真正写盘。
- [x] 2026-05-28：继续清理 `docs/parameter-map.md` 的 restart companion 行：已把表前段那条较旧的 `amr.restart` 再压实到和后段同名条目一致的粒度，补进 `WriteUsedInputsFile()` 固定时序、checkpoint `DistributionMapping` 恢复/回退、BTD 专门恢复链，以及 HybridPIC restart 首步复用 checkpoint 场/流体态这些 restart 边界，消掉同参不同深度的残差。
- [x] 2026-05-28：继续清理 `docs/parameter-map.md` 的 PML/distribution-mapping companion 行：已把 `do_similar_dm_pml` 再补硬一层，明确写清它虽然会共同控制普通 fine-PML 与 refined-level coarse-PML 的 `DistributionMapping` 是否走 `MakeSimilarDM(...)`，但在 `RZ + FFT` 的 level-0 分支里当前直接构造的是 `PML_RZ(...)`，这条路径根本不消费 `do_similar_dm_pml`。
- [x] 2026-05-28：继续清理 `docs/parameter-map.md` 的 PML/distribution-mapping companion 行：已把 `do_similar_dm_pml` 再压实一层，明确写清这条开关不只决定最外层 PML `dm` 是否走 `MakeSimilarDM(...)`，还会继续级联到 refined-level 的 coarse-PML `cdm` 分配；也就是说它当前共同控制 fine PML 和 coarse-PML 两套 patch 是否尽量继承母网格的 MPI rank 邻接关系。
- [x] 2026-05-28：继续清理 `docs/parameter-map.md` 的 startup/div-cleaning companion 行：已把 `warpx.do_initial_div_cleaning` 再压实一层，明确写清这条开关虽然会在 startup 中自动默认打开某些“非常量外加 B 网格场 + 兼容 solver/grid”组合，但自动执行只发生在 fresh-run 初始化主链里；restart 路径当前会完全旁路这条 auto-run，而 Python 侧暴露的 `ProjectionCleanDivB()` 也只是独立的手动入口，不受这条参数自动门控。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `embedded_boundary_em_particle_absorption` 邻近 baseline 行：已把 `test_rz_embedded_boundary_em_particle_absorption_sh_factor_1.json` 与 `..._sh_factor_3.json` 再压实一层，明确写清这两条 active RZ regression 都不是 checksum-only，而是统一绑定到 `analysis.py + analysis_default_regression.py --path diags/diag1`；同时也补清二者分别命中 `shape factor = 1 / 3` 的 RZ runtime 分叉，并共同消费去轴区域时间平均 `divE` 的 `L∞ <= 4e-12` 断言链。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `embedded_boundary_diffraction` 邻近 baseline 行：已把 `test_rz_embedded_boundary_diffraction.json` 再压实一层，明确写清这条 active regression 不是 checksum-only，而是绑定到 `analysis_fields.py diags/diag1/ + analysis_default_regression.py --path diags/diag1/`；同时也补清对应输入当前 materialize 的是 `n_rz_azimuthal_modes = 2` 的 cylindrical-aperture diffraction openPMD producer，而主消费者实际消费的是 `iteration 300` 强度图、第一极小值半径轨迹和 Airy 线性包络断言链。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `embedded_boundary_python_api` 邻近 baseline 行：已把 `test_3d_embedded_boundary_picmi.json` 再压实一层，明确写清这条 active regression 外层确实只有 `analysis=OFF + analysis_default_regression.py --path diags/diag1000002` 的附加 checksum；同时也补清真正的强断言都内嵌在 `inputs_test_3d_embedded_boundary_picmi.py` 自身，包括单步后直接读取 `edge_lengths_{x,y,z}` / `face_areas_{x,y,z}`、对三个中截面的 perimeter 与 area 施加 `rtol=1e-5` / `atol=1e-8` 的闭式几何断言，并再串进第二步 PICMI 运行流。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `embedded_boundary_rotated_cube` 邻近 baseline 行：已把 2D/3D `test_*_embedded_boundary_rotated_cube.json` 再压实一层，明确写清它们都不是 checksum-only，而是分别绑定到 `analysis_fields_2d.py/analysis_fields_3d.py + analysis_default_regression.py`；同时也补清 2D 路径消费的是反旋后 `By` 的有效区域 `L2 < 1e-1` 断言，3D 路径消费的是 `raw By_fp/Bz_fp` 在反旋坐标和反旋分量后的双分量 `L2 < 1e-2` 断言链。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `embedded_boundary_removal_depth` 邻近 legacy baseline 行：已把 2D/3D `test_*_embedded_boundary_removal_depth_sh_factor_1.json` 再压实一层，明确写清这两个名字在本地也都只剩 `benchmarks_json` 快照、没有对应 `Examples/Tests` 注册；同时也补清它们在 active 树里的承接关系分别落到 `embedded_boundary_em_particle_absorption` 的 2D/3D `shape factor = 1` 路径。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `embedded_boundary_removal_depth` 邻近 legacy baseline 行：已把 2D/3D `test_*_embedded_boundary_removal_depth_sh_factor_{2,3}.json` 再压实一层，明确写清这些名字在本地只剩 `benchmarks_json` 快照、没有对应 `Examples/Tests` 注册；同时也补清它们在 active 树里的承接关系分别落到 `embedded_boundary_em_particle_absorption` 的 2D/3D `shape factor` 路径，其中 3D `sh_factor_2` 的 active 承接路径当前仍实际命中 `shape factor = 1` runtime。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `embedded_boundary_em_particle_absorption` 邻近 baseline 行：已把 3D `test_3d_embedded_boundary_em_particle_absorption_sh_factor_1.json` 与 `..._sh_factor_3.json` 再压实一层，明确写清它们都不是 checksum-only，而是统一绑定到 `analysis.py + analysis_default_regression.py --path diags/diag1`；同时也补清二者分别命中 `shape factor = 1 / 3` 的 3D runtime 分叉，并共同消费 `3dcartesian` 分支下时间平均 `divE` 的全域 `L∞ <= 7e-11` 断言链。
- [x] 2026-05-28：继续清理 `docs/parameter-map.md` 的 domain-decomposition companion 行：已把 `warpx.split_high_density_boxes` 再压实一层，明确写清这条开关当前并不会被 `warpx.numprocs` 自动禁用，而是会在 `PostProcessBaseGrids()` 里接在 `one-box-per-rank` 手工切块之后继续运行；只要 `parse_density_function` 预测粒子数链成功 materialize，并且 `AllGatherBoxes(new_boxes)` 后全局 box 数真的增加，它就能把 base-level box 数重新抬高。
- [x] 2026-05-28：继续清理 `docs/parameter-map.md` 的 AMR/domain-decomposition companion 行：已把 `warpx.numprocs` 再压实一层，明确写清它不仅会触发 `blocking_factor -> 1` 的 startup workaround 与 `PostProcessBaseGrids()` 的手工 `BoxList` 切块，而且会把最粗层 box 粒度锁成 `one-box-per-rank`；同时也补清后续 `LoadBalance()` 当前只会重算 `DistributionMapping`，不会把这条路径重新扩成 `amr.max_grid_size/blocking_factor` 那种多 box 拓扑。
- [x] 2026-05-28：继续清理 `docs/parameter-map.md` 的 AMR gridding companion 行：已把 `amr.max_grid_size_x/y/z` 与 `amr.blocking_factor(_x/_y/_z)` 再压实一层，明确写清它们在启动期会先走 `WarpXAMReXInit.cpp` 的数值预解析，而且在 `RZ + PSATD` 路径下会分化成“`x` 向无条件按径向 `n_cell`/最小 2 次幂重写、用户值被丢弃”与“`y` 向继续走 shared-key -> directional-override -> `nprocs` 约束 shrink”的两条不同 consumer 链；同时也补清 `warpx.numprocs` workaround 当前只会把公共 `amr.blocking_factor` 改成 `1`，不会同步清空方向化 companion。
- [x] 2026-05-28：继续清理 `docs/parameter-map.md` 的 `particle_thermalizer` 邻近 companion 行：已把 `particle_thermalizer.normal/species` 再压实一层，明确写清 `normal` 不只是定义 thermalizer 的 presence gate，而且 runtime hook 当前位于 `HandleParticlesAtBoundaries(...)` 之后、`doCollisions(...)` 之前；同时也补清 `species` 的空列表语义是遍历 `allcontainers`，非空列表则通过 `GetParticleContainerFromName(...)` 在运行时解析名字，未知名字会直接 abort。
- [x] 2026-05-28：继续清理 `docs/parameter-map.md` 的 `particle_thermalizer` 邻近 companion 行：已把 `particle_thermalizer.start/end/momentum_threshold/theta` 再压实一层，明确写清 `start/end` 当前共同决定 tile-overlap 裁剪、`1-(...)^0.25` 的位置相关热化概率曲线，以及末端 `hiend-dx` 起始的必然热化带；同时也补清 `momentum_threshold` 是逐分量阈值 gate，而 `theta` 当前控制的是“逐分量、保号”的 Gaussian 重采样宽度。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `flux_injection` 邻近 input-level 行：已把 `inputs_test_2d_flux_injection_from_eb`、`inputs_test_3d_flux_injection_from_eb` 与 `inputs_test_rz_flux_injection_from_eb` 再压实一层，明确写清这三条不只是共享 `inputs_base_from_eb` 的 surface-emission scaffold，而且分别激活共享 `analysis_flux_injection_from_eb.py` 的 `2D cylinder`、`3D native sphere` 和 `RZ -> 3D` 几何重建 consumer 分支。
- [x] 2026-05-28：继续清理 `docs/parameter-map.md` 的 boundary companion 行：已把 `boundary.<species_name>.u_th` 与 `boundary.reflect_all_velocities` 再压实一层，明确写清前者的外层 gate 当前只看全局 `particle_boundary_lo/hi` 是否存在任意 thermal 面，而且同一 species 的所有 thermal 边界共用一个 `u_th`；同时也补清后者发生在 thermal rethermalization 之后，只会把已有反射/再热化事件升级成全分量翻号，不会凭空把 open/absorbing 路径改造成全反射。
- [x] 2026-05-28：继续清理 `docs/parameter-map.md` 的 particle companion 行：已补入缺失的 `<species_name>.reflection_model_*` 行，并把 `<species_name>.save_particles_at_*` 再压实一层，明确写清前者当前是在 absorbing boundary 上以法向速度为输入的 runtime parser gate，并会与 `reflect_all_velocities` / thermal rethermalization companion 叠加；同时也补清后者的 scrape 收集时机和 flush 写盘时机当前是分离的，flush 之前 pinned boundary buffer 还可通过 Python 直接读取。
- [x] 2026-05-28：继续清理 `docs/parameter-map.md` 的 particle companion 行：已把 `<species_name>.do_splitting` 与 `<species_name>.split_type` 再压实一层，明确写清前者真正的 tag 入口是 `Redistribute -> locate -> particlePostLocate`，不会脱离重定位单独 materialize；同时也补清后者的 split offset 还隐式依赖 `plasma_injectors[0]->num_particles_per_cell_each_dim`，而新生成子粒子会被统一封成 `NoSplitParticleID`，因此同一上行链里不会继续递归 split。
- [x] 2026-05-28：继续清理 `docs/parameter-map.md` 的 particle companion 行：已把 `<species_name>.random_theta` 与 `<species_name>.save_previous_position` 再压实一层，明确写清前者当前不是“每个粒子各自抽一个随机角”，而是每个 cell 内新粒子共用一次随机整体旋转、相对角间距保持不变；同时也补清后者的 `prev_x/y/z` 不只是内部缓存，而是会作为 runtime particle components 暴露给后续输出/下游读取。
- [x] 2026-05-28：继续清理 `docs/parameter-map.md` 的 particle companion 行：已把 `<species_name>.do_not_gather` 与 `<species_name>.do_not_push` 再压实一层，明确写清两者都不只是 startup 输入键，而是还可通过 Python API 在运行期直接翻转；同时也补清 `do_not_gather` 当前只切断网格 `E/B` gather、不会切断外加场或 QED companion，而 `do_not_push` 当前切断的是推进和与推进绑定的分区/电流沉积链，但仍保留前后置 `rho` snapshot 这条旁路。
- [x] 2026-05-28：继续清理 `docs/parameter-map.md` 的 particle companion 行：已把 `particles.gather_from_main_grid` 与 `<species_name>.do_not_deposit` 再压实一层，明确写清前者当前只覆盖普通 particle species、没有与之对称的 laser companion，而且它只会强制改写 coarse-aux gather/push 分流，不会自动连带改写 deposition；同时也补清后者不仅切断主推进里的 `rho/J` 沉积，还会继续影响 deposition-aware sorting，以及 magnetostatic / electrostatic solver 对粒子源项的收集链。
- [x] 2026-05-28：继续清理 `docs/parameter-map.md` 的 particle companion 行：已把 `particles.deposit_on_main_grid` 与 `particles.do_tiling` 再压实一层，明确写清前者只会强制改写 coarse-buffer 的 current/charge 沉积分流、不会自动连带改写 gather，且 laser 侧仍走独立的 `lasers.deposit_on_main_grid` companion；同时也补清后者的默认值覆写、`static` 缓存边界，以及它当前只覆盖粒子创建链上的 `MFItInfo::EnableTiling(tile_size)`，不是通用 `ParIter`/推进/碰撞循环的统一总开关。
- [x] 2026-05-28：继续清理 `docs/parameter-map.md` 的 particle companion 行：已把 `<species_name>.species_type` 再压实一层，明确写清 photon 分类当前不是只看 `species_type = photon`，而是与 deprecated 的 `particles.photon_species` 做 OR 分派；同时也补清了 startup warning、`PhotonParticleContainer` 工厂分派，以及 restart 时仍由当前输入文件重新决定 photon/physical 容器类型的边界。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `embedded_boundary_removal_depth` 邻近 legacy baseline 行：已把三条 `test_rz_embedded_boundary_removal_depth_sh_factor_{1,2,3}` 再压实一层，明确写清它们在本地 checkout 里只剩 `Regression/Checksum/benchmarks_json` 下的 benchmark JSON 快照，没有对应 `Examples/Tests` 输入卡或 `add_warpx_test(...)` 注册；真正活跃的承接路径已经是 `embedded_boundary_em_particle_absorption_sh_factor_{1,2,3}`。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `embedded_boundary_em_particle_absorption` 邻近 baseline 行：已把 `test_3d_embedded_boundary_em_particle_absorption_sh_factor_2` 与 `test_rz_embedded_boundary_em_particle_absorption_sh_factor_2` 再压实一层，明确写清这两条虽然仍作为 active regression 绑定到共享 `analysis.py + checksum`，但对应输入卡 runtime 实际仍把 `algo.particle_shape` 写成 `1`，因此 name、runtime 和 consumer 当前都还没有真正切到独立的 shape-factor-2 路径。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `embedded_boundary_diffraction` 邻近 analysis-level 行：已把 `analysis_fields.py` 再压实一层，明确写清这条强分析当前会沿 `OpenPMDTimeSeries(iteration=300)` 读取 `E_x(r,z)`，先通过 `gaussian_filter1d` 构造径向平滑强度图，再逐个 `z` 切片提取第一极小值半径轨迹，并只在传播后半段把它与 Airy 线性包络做逐点上界断言。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `embedded_boundary_cube` 邻近 input-level 行：已把 `inputs_test_3d_embedded_boundary_cube` 与 `inputs_test_3d_embedded_boundary_cube_macroscopic` 再压实一层，明确写清前者本体只是把公共 3D stair-case PEC cavity scaffold 原样作为 active baseline 入口，并直接送进 `analysis_fields.py` 的 `By/Bz` 解析 TM 模态断言；后者则是在同一 scaffold 上只切到 `epsilon_r = 1.5` 的 macroscopic dielectric solver 路径，并命中带介质频率修正的同一消费者链。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `electrostatic_sphere` 邻近 input-level 行：已把 `inputs_test_3d_electrostatic_sphere` 再压实一层，明确写清它本体只是在公共 `inputs_base_3d` 上额外挂出 `warpx.abort_on_warning_threshold = medium`，真正命中的仍是完整的 3D `relativistic` electrostatic 均匀电子球自场膨胀 scaffold；同时也补清了它继续保留 `synchronize_velocity_for_diagnostics = 1`，但不像 `lab_frame` 分支那样显式写出 openPMD `phi` 能量账本面。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `electrostatic_sphere` / `electrostatic_sphere_eb` 邻近 RZ input-level 行：已把 `inputs_test_rz_electrostatic_sphere` 与 `inputs_test_rz_electrostatic_sphere_eb_mr` 补成与相邻 baseline 同粒度的 runtime scaffold，写清前者的 `synchronize_velocity_for_diagnostics + openPMD phi` 能量账本面，以及后者的 `RZ + MR + fixed-potential cylinder EB + openPMD multi-level Er/phi/eb_covered` producer 结构。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `electrostatic_sphere` 邻近 input-level 行：已把 `inputs_test_3d_electrostatic_sphere_adaptive`、`inputs_test_3d_electrostatic_sphere_lab_frame`、`inputs_test_3d_electrostatic_sphere_lab_frame_mr_emass_10`、`inputs_test_3d_electrostatic_sphere_rel_nodal` 与 `inputs_test_rz_electrostatic_sphere_uniform_weighting` 补成与相邻 baseline 同粒度的 runtime scaffold，写清哪些分叉真正独立 materialize producer，哪些只是复用公共基线再切 `labframe / phi / MR / collocated / uniform-weighting`。
- [x] 2026-05-28：继续清理 `docs/parameter-map.md` 的 `particles.use_fdtd_nci_corr`：已把它补成更明确的 FDTD NCI corrector 总 gate，写清当前它不仅会在 startup 初始化两套 `NCIGodfreyFilter` 并在 fine/coarse gather 前过滤六个场分量，还会沿 `AllocLevelData -> guard_cells.Init(...)` 直接改写 `E/B` 的 z 向 guard-cell 需求；同时也把它与 `PSATD`、非 `Esirkepov` deposition、implicit solver 和若干几何的不兼容边界补硬。
- [x] 2026-05-28：继续清理 `docs/parameter-map.md` 的 `particles.species_names`：已把它补成更明确的 species 主索引条目，写清当前它不仅决定 `MultiParticleContainer` 前半段 physical species 工厂与 `deposit_on_main_grid / gather_from_main_grid / rigid_injected_species / photon_species` 这些 side-list 的统一校验索引，还和 `lasers.names` 一起形成 checkpoint/full diagnostics 默认 species 选择与 `ParticleIO` header/restart 排序合同；同时也补清了 `particles.nspecies` 当前只告警并被忽略的兼容边界。
- [x] 2026-05-28：继续清理 `docs/parameter-map.md` 的 `warpx.split_high_density_boxes_threshold` / `warpx.split_high_density_boxes_min_box_size`：已把前者补成更明确的递归切分门槛条目，写清当前它控制的是相对全局平均每 rank 目标粒子数的 `wtarget`，并且只有 `rho` 已生成且 `wtot > 0` 时才会真正参与递归切分；同时把后者补成沿最长边二分链的最小几何终止尺度，并写清它还会直接影响最后是否真的重建新的 base `BoxArray`。
- [x] 2026-05-28：继续清理 `docs/parameter-map.md` 的 `warpx.roundrobin_sfc`：已把它补成更明确的初始化期 `DistributionMapping` strategy gate，写清当前它只在 `MakeDistributionMap(...)` 中临时切到 `RRSFC`，并优先压过 `split_high_density_boxes` 的等权 SFC companion 分支；后续运行期仍可能被 `LoadBalance()` 覆盖。
- [x] 2026-05-28：继续清理 `docs/parameter-map.md` 的 `warpx.do_dynamic_scheduling`：已把它补成更明确的 `WarpXParIter` 默认调度偏好条目，写清当前只有沿 `WarpXParIter(..., info)` 走的粒子循环会继承这条全局开关，而粒子创建、多 species helper 与 `BinaryCollision` 主链都在 OMP 路径下显式固定 `SetDynamic(true)`，并不消费它。
- [x] 2026-05-28：继续清理 `docs/parameter-map.md` 的 `warpx.do_shared_mem_current_deposition` / `warpx.shared_mem_current_tpb`：已把前者补成更明确的 shared current deposition 总 gate，写清当前它会沿 `DenseBins -> max_tbox_size -> doDepositionSharedShapeN` 分支排除 `Implicit/Esirkepov/Villasenor/Vay` 与相邻 mass-matrix、temperature deposition 路径；同时把后者补成只在 one-bin-per-block shared current kernel 中控制 block 内线程数的局部调优参数，不参与 charge deposition。
- [x] 2026-05-28：继续清理 `docs/parameter-map.md` 的 `warpx.do_device_synchronize`：已把它补成更明确的 profiling 配置入口条目，写清当前它先由 `WarpXAMReXInit.cpp` 桥接成 `tiny_profiler.device_synchronize_around_region`，再只在 GPU 构建下由 AMReX `TinyProfiler::start()/stop()` 两端实际消费，而不会进入 WarpX 主演化路径。
- [x] 2026-05-28：继续清理 `docs/parameter-map.md` 的 `warpx.override_sync_intervals`：已把它补成更明确的“文档语义强于本地实现接线”条目，写清当前本地源码只能硬证实到启动期 `IntervalsParser` materialization、成员保存和旧名 `override_sync_int` 拒绝，而官方文档里关于 box-boundary `rho/J/E/B` 周期同步与 PML 例外的语义，在这份本地代码快照里还缺少可直接指向的 runtime consumer 证据。
- [x] 2026-05-28：继续清理 `docs/parameter-map.md` 的 `warpx.projection_div_cleaner.rtol`：已把它补成更明确的 projection-based `div(B)` cleaner 收敛门槛条目，写清当前它不仅受 `ProjectionDivCleaner` 子 parser 默认值与用户覆写控制，还受 `ProjectionCleanDivB()` 的 solver-gate、`MLNodeLaplacian/MLPoisson` 线性算子分叉、边界条件映射，以及唯一一次 `mlmg.solve(..., rtol, atol)` 消费链共同约束。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `nci_psatd_stability` `test_2d_galilean_psatd_hybrid`：已把它补成更明确的 checksum-only hybrid 分叉条目，写清当前没有接入 `analysis_galilean.py`，本地唯一自动 gate 就是对末态 `diag1000400` 的默认 checksum 比较。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `nci_psatd_stability` `test_2d_comoving_psatd_hybrid`：已把它补成更明确的 checksum-only 应用级 workflow 条目，写清当前没有接入 `analysis_galilean.py`，本地唯一自动 gate 就是对末态 `diag1000400` 的默认 checksum 比较。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `nci_psatd_stability` `test_3d_uniform_plasma_psatd_CC1`：已把它补成当前只在 `Regression/Checksum/benchmarks_json` 里保留的一份 legacy checksum 快照，并写清本地唯一仍活跃的相邻路径已经切到 `test_3d_uniform_plasma_psatd_JRhom_CC1`。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `nci_psatd_stability` `inputs_test_rz_psatd_JRhom_LL2`：已把它补成独立的 moving-window + rigid `driver` + `driver_back` + continuous-injection `plasma_e/plasma_p` 应用级 workflow，并写清当前它只作为 `analysis=OFF + analysis_default_regression.py --path diags/diag1000025` 的 `JRhom_LL2` 输出 checksum 路径存在。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `nci_psatd_stability` `RZ Galilean` 主线输入行：已把 `inputs_test_rz_galilean_psatd`、`inputs_test_rz_galilean_psatd_current_correction` 与 `inputs_test_rz_galilean_psatd_current_correction_psb` 补成只在公共 RZ base 上切到 `current_correction = 0/1`、`periodic_single_box_fft = 0/1`、`random_theta` 与局部 patch 参数的窄 runtime 分叉，并写清它们分别对应的末态场能 / `divE-rho/eps0` 消费者链。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `nci_psatd_stability` `3D Galilean` 主线输入行：已把 `inputs_test_3d_galilean_psatd`、`inputs_test_3d_galilean_psatd_current_correction` 与 `inputs_test_3d_galilean_psatd_current_correction_psb` 补成只在公共 3D base 上切到 `current_correction = 0/1`、`periodic_single_box_fft = 0/1`、`divE` 字段面与 `numprocs` 的窄 runtime 分叉，并写清它们分别对应的末态场能 / `divE-rho/eps0` 消费者链。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `nci_psatd_stability` `2D current-correction + PSB` 邻近条目：已把 `inputs_test_2d_galilean_psatd_current_correction_psb` 补成只在公共 2D base 上切到 `psatd.current_correction = 1`、`psatd.periodic_single_box_fft = 1`、`psatd.update_with_rho = 0` 并扩出 `divE` 字段面的窄 runtime 分叉；并同步把 `test_2d_galilean_psatd_current_correction_psb` 补成更准确的末态场能 / `divE-rho/eps0` 双消费者链边界。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `nci_psatd_stability` `2D Galilean` 主线条目：已把 `inputs_test_2d_averaged_galilean_psatd_hybrid` 补成在 2D averaged base 上切到 `hybrid` 与显式 patch 切分参数的窄 runtime 分叉；把 `inputs_test_2d_galilean_psatd` 与 `inputs_test_2d_galilean_psatd_current_correction` 补成只在公共 2D base 上切到 `current_correction = 0/1` 的窄分叉；并同步把 `test_2d_galilean_psatd{,_current_correction,_current_correction_psb}` 补成更准确的末态场能 / `divE-rho/eps0` 消费者链边界。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `nci_psatd_stability` `2D/3D averaged` 主线条目：已把 `inputs_test_2d_averaged_galilean_psatd`、`inputs_test_3d_averaged_galilean_psatd` 补成只在各自 averaged base 上切到 `current_correction = 0` 的窄 runtime 分叉；把 `inputs_test_3d_averaged_galilean_psatd_hybrid` 补成在 3D averaged base 上再切到 `warpx.grid_type = hybrid` 的窄分叉；并同步把 `test_2d_averaged_galilean_psatd` 与 `test_3d_averaged_galilean_psatd` 补成更准确的末态场能消费者链边界。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `nci_psatd_stability` `averaged/hybrid` 邻近条目：已把 `inputs_base_2d_averaged`、`inputs_base_3d_averaged` 补成高-CFL averaged-Galilean 共漂移电子/离子均匀等离子体公共 scaffold；把 `inputs_test_2d_galilean_psatd_hybrid` 压实为只在公共 2D Galilean base 上切到 `warpx.grid_type = hybrid` 与 `psatd.use_default_v_galilean = 1` 的窄 runtime 分叉；并同步把 `test_2d_averaged_galilean_psatd_hybrid`、`test_2d_galilean_psatd_hybrid` 与 `test_3d_averaged_galilean_psatd_hybrid` 补成更准确的 consumer/runtime 边界。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `nci_psatd_stability` 公共 scaffold 条目：已把 `inputs_base_2d`、`inputs_base_3d` 补成 collocated PSATD + direct deposition + Vay + filter 的共漂移电子/离子均匀等离子体公共 runtime scaffold；把 `inputs_test_2d_comoving_psatd_hybrid` 压实为 `hybrid-grid + boost + moving window + rigid beam + parabolic plasma channel + Gaussian laser` 的 comoving PSATD 应用级 workflow；并同步把 `test_2d_comoving_psatd_hybrid` 补成更准确的 `analysis=OFF + checksum` workflow-only baseline 边界。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `nci_psatd_stability` family analysis / RZ base / baseline 行：已把 `analysis_galilean.py` 压实为“按 `dims/current_correction/do_time_averaging/periodic_single_box_fft` 选通参考阈值的全域末态场能 gate，并在 `current_correction=1` 时追加 `divE-rho/eps0` 相对 `L∞` gate”的强分析链；把 `analysis_psatd_CC1.py` 压实为 `test_3d_uniform_plasma_psatd_JRhom_CC1` 专用的末态全域场能消费者；把 `inputs_base_rz` 补成 collocated RZ PSATD + direct deposition + Vay + 固定 `v_galilean` 的共漂移电子/离子均匀等离子体 scaffold；并同步把 `test_3d_uniform_plasma_psatd_JRhom_CC1`、`test_rz_galilean_psatd{,_current_correction,_current_correction_psb}` 与 `test_rz_psatd_JRhom_LL2` 补成更准确的 consumer/runtime 边界。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `ion_stopping` family analysis/helper 行：已把 `analysis.py` 压实为“初态粒子与背景参数回读 + 10 步 slowing-down 解析重演 + 四条 background_stopping 路径逐粒子终态能量 gate”的强分析链；同时把 `analysis_default_regression.py` 补成目录内符号链接到共享 `plotfile/openpmd` checksum helper 的准确边界，并写清它当前只是 `test_3d_ion_stopping` 旁边的附加 checksum 链。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `ionization_dsmc` family 1D analysis 行：已把 `analysis_charge_exchange_dsmc_1d.py` 压实为“截面表插值 + `H/Hplus` 双 fast-beam 通量重建 + 电荷交换指数衰减/增长双断言”的强分析链；把 `analysis_photoneutralization_dsmc_1d.py` 压实为“盒内 reactant/product + scraped-electron 双数据面、COM-frame 光中和能量收支重建与双产物速度断言”的强分析链；把 `analysis_two_product_reaction_dsmc_1d.py` 压实为“末态 openPMD 产物速度回读 + 两产物反应 COM-frame 动量/能量分配重建 + 双速度强断言”的分析链。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `ionization_dsmc` family analysis 侧条目：已修正总表里误写成 `analysis_ionization_dsmc_1d6py` 的行名，恢复为真实的 `analysis_ionization_dsmc_1d.py`；同时把 `analysis_ionization_dsmc_3d.py` 压实为更明确的强分析合同，写清它当前并不是中性的 family helper，而是显式绑定 `electron-impact` 假设、消费 `counts.txt + openPMD diag2` 双诊断面，并用 quasi-Monte-Carlo 速率系数重建加 0D global-model RK2 重演去约束 `n_e / n_n / n_eT_e` 三条时间序列。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `ionization_dsmc` family `3D` 输入侧结构：已把 `inputs_base_3d` 压实为更明确的 `3D no-field DSMC ionization global-model` 公共 runtime scaffold，并写清其真实 producer 面是 `counts.txt`、openPMD `diag2` 与最终 `diag1` plotfile；同时把 `inputs_test_3d_ionization_electron_dsmc` 补成只在 base 之上切换 `electron-impact` 截面表和 `ioniz.species = electrons neutrals` 的 active 强分析分叉；把 `inputs_test_3d_ionization_ion_dsmc` 补成对应的 `ion-impact` 分叉，并写清当前因为 `analysis_ionization_dsmc_3d.py` 把 electron-impact 假设写死，所以它在 CMake 中仍是 `analysis=OFF + checksum` 的 reserve 路径。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `ionization_dsmc` family 邻近 `1D neutral-beam ionization` 条目：已把 `ionization_dsmc/analysis_default_regression.py` 补成目录内符号链接到共享 `plotfile/openpmd` checksum helper 的准确边界，并写清它当前服务的是整组 `ionization_dsmc` active regression 的附加 checksum 链；同时把 `inputs_test_1d_ionization_neutral_dsmc` 压实为更明确的 no-field DSMC runtime scaffold，写清其真实路径是 `Hneutral` 快束穿过 `H2` 气柱并走 `H2 + H -> H2 + H+ + e-` 电离链；把 `test_1d_ionization_neutral_dsmc` 补成 `analysis_ionization_dsmc_1d.py + checksum` 的双层合同，并写清其真正强断言是 `Hneutral/Hplus` 两条 fast-beam 通量对指数理论曲线的双 `allclose`。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `collision` family 里 `1D` native 条目：已把 `inputs_test_1d_collision_z`、`inputs_test_1d_collision_z_correct_conservation`、`inputs_test_1d_collision_z_Bremsstrahlung` 都压实为更明确的 no-field runtime scaffold；同时把 `test_1d_collision_z` 补成 `analysis_collision_1d.py + checksum` 的双层合同，并写清其真正强断言是低密度流入群体 `TApar` 对 Higginson 2020 参考值 `6.15e3 eV` 的相对误差 `< 0.02`；把 `test_1d_collision_z_correct_conservation` 补成 `analysis_collision_1d_correct_conservation.py + checksum`，并写清其真正强断言是 step `0/10` 两帧总 `px/py/pz` 相对漂移 `< 1e-14` 且总动能相对漂移 `< 1e-10`；把 `test_1d_collision_z_Bremsstrahlung` 补成 `analysis_collision_1d_Bremsstrahlung.py + checksum`，并写清其主消费者是 reduced `particle_energy / particle_momentum / particle_number` 三套账本上的总守恒、`dE/dx` 与 photon 产额阈值。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `collision` family-level helper 与 `RZ` input 条目：已把 `collision/analysis_default_regression.py` 补成目录内符号链接到共享 `plotfile/openpmd` checksum helper 的准确边界，并写清它当前服务的是整组 `collision` active regression 的附加 checksum 链，而不是单条物理强消费者；同时把 `inputs_test_rz_collision` 压实为更明确的 `RZ + no-field + do_not_push` 局域同向电子 e-e collision runtime scaffold，并写清下游消费者统一落在 `analysis_collision_rz.py` 对 `j=0/150` 两帧 `momentum_x/y` 的首末不变断言。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `collision` 邻近 `3D` 收尾条目：已把 `test_3d_collision_iso_subcycle` 补成 `analysis_collision_3d_isotropization.py + checksum` 的双层合同，并写清其真正新增的是 `PIC dt` 放大 10 倍但通过 `collision1.ndt_subcycle = 10` 保持碰撞子步长不变，而主消费者仍是最终 `T_x/T_y` 对解析 isotropization ODE 的相对误差 `< 0.05`；把 `test_3d_collision_pulsed_decay` 补成 `analysis_collision_3d_pulsed_decay.py + checksum` 的双层合同，并写清其真正强断言是 reduced `particle_number.txt` 对 0D 高斯衰变模型 `n_I(t)` 的最终离子总权重误差 `< 0.5%`。对应 input-level 行也同步压实为更明确的 runtime scaffold。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `collision` 邻近 `3D` 条目：已把 `test_3d_collision_iso` 补成 `analysis_collision_3d_isotropization.py + checksum` 的双层合同，并写清其真正强断言是最终 `momentum_x/y` 重建出的 `T_x/T_y` 对解析 isotropization ODE 的相对误差 `< 0.05`；把 `test_3d_collision_xyz` 补成 `analysis_collision_3d.py + checksum` 的双层合同，并写清其真正强断言是整个 `diag1` 时间序列上电子/离子平均 `v_x` 差的指数拟合误差 `< 1e-3`，同时继续消费三套粒子筛选 diagnostics。对应的 3D native input-level 行也同步压实为更明确的 runtime scaffold。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `collision` 邻近 `test_2d_collision_xz` 系列条目：已把 `test_2d_collision_xz`、`test_2d_collision_xz_global_debye` 与 `test_2d_collision_xz_picmi` 都补成 `analysis_collision_2d.py + checksum` 的双层合同，并写清其真正强断言统一来自整个 `diag1` 时间序列上电子/离子平均 `v_x` 差对指数拟合的平均误差 `< 1e-3`；同时写清 native 两条还继续消费 parser/uniform/random 三套粒子筛选 diagnostics，而 PICMI 版显式跳过第二阶段。对应的 native / global-Debye / PICMI input-level 行也同步压实为更明确的 runtime scaffold 与分支差异。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `collision` 邻近 2D split-momentum 条目：已把 `test_2d_collisions_split_momentum_push_electromagnetic`、`test_2d_collisions_split_momentum_push_electromagnetic_vay` 与 `test_2d_collisions_split_momentum_push_electrostatic` 都补成 `analysis_test_2d_collisions_split_momentum_push.py + checksum` 的双层合同，并写清其真正强断言统一来自 reduced `field_energy + particle_energy` 账本对总能量守恒与理论 equipartition 的闭合；同时也把 `inputs_base_2d_collisions_split_momentum_push` 及三条派生 input-level 行进一步压实为更明确的“共享 runtime scaffold + solver/current deposition/pusher 分支”结构。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `laser_injection_from_file` 邻近 `3D/RZ lasy` 条目：已把 `test_rz_laser_injection_from_RZ_lasy_file` 补成 `prepare + analysis_from_RZ_file.py + checksum` 的两阶段合同，并写清其真正强断言是最终 `Et` 对 `p=0,m=1` Laguerre-Gaussian 理论包络与主频的双误差阈值；把 `test_rz_laser_injection_from_lasy_file` 补成 `prepare + analysis_rz.py + checksum` 的两阶段合同，并写清其当前消费的是普通 Cartesian lasy 文件经 RZ quasi-cylindrical runtime 注入后的 `Et` 包络与主频双断言。同时也把 `RZ thetaMode` / 普通 `RZ` / `3D prepare` 的对应 input-level 行进一步压实为更明确的 file-materialization 与 runtime scaffold。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `collision` / `laser_injection_from_file` 邻近条目：已把 `test_2d_charge_exchange_dsmc` 补成 `analysis_test_2d_collisions_split_momentum_push.py + checksum` 的双层合同，并写清其真正强断言是 reduced `field_energy + particle_energy` 账本对总能量守恒与理论 equipartition 的双重闭合；把 `test_1d_laser_injection_from_lasy_file` 与 `test_1d_laser_injection_from_lasy_file_boost` 补成 `prepare + analysis_{1d,1d_boost}.py + checksum` 的两阶段合同，并写清普通 1D 路径消费末态 `Ey`、boosted 路径消费 back-transformed `Ey` snapshot，二者都直接对 Hilbert envelope 与主频做双断言。同时也把三条对应 input-level 行进一步压实为更明确的 runtime scaffold。
- [x] 2026-05-28：清理 [README.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/README.md) 中段历史遗留的无效 UTF-8 噪声块，恢复顶层状态文档可被正常 `apply_patch`；同时继续清理 `docs/example-regression-map.md` 的 `ionization_dsmc` / `laser_injection_from_file` 邻近条目：已把 `test_1d_charge_exchange_dsmc` 补成 `analysis_charge_exchange_dsmc_1d.py + checksum` 的双层合同，并写清其真正强断言是 `H/Hplus` 通量对指数理论曲线的双 `allclose(atol=5e-2*flux)`；把 `test_2d_laser_injection_from_lasy_file` 补成 `prepare + analysis_2d.py + checksum` 的两阶段合同，并写清共享 analysis 当前直接对最终 `Ey` 做 Hilbert envelope 与主频双断言。同时也把两条对应 input-level 行进一步压实为更明确的 producer/runtime scaffold。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `ionization_dsmc` / `laser_injection_from_file` / `ohm_solver_magnetic_reconnection` 邻近 active baseline 与 input-level 条目：已把 `test_1d_two_product_reaction_dsmc` 补成 `analysis_two_product_reaction_dsmc_1d.py + checksum` 的双层合同，并写清其真正强断言是 `H/H2plus` 理论实验室系速度的双 `allclose(atol=1e-8)`；把 `test_2d_laser_injection_from_binary_file` 补成 `prepare + analysis_2d_binary.py + checksum` 的两阶段合同，并写清共享 analysis 当前直接对最终 `Ey` 做 Hilbert envelope 与 2D FFT 主频双断言；把 `test_2d_ohm_solver_magnetic_reconnection_picmi` 补成 `"--test" + analysis.py + checksum`，并写清当前 `plane.dat` / `fields_*.npz` 只是重联率曲线和动画的 side consumer，而 `diag1000020` checksum 才是主自动 gate。同时也把三条对应 input-level 行进一步压实为更明确的 producer/runtime scaffold。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `ionization_dsmc` / `laser_on_fine` / `ohm_solver_ion_Landau_damping` 邻近 active baseline 与 input-level 条目：已把 `test_1d_photoneutralization_dsmc` 补成 `analysis_photoneutralization_dsmc_1d.py + checksum` 的双层合同，并写清其真正强断言是盒内 `Hneutral` 与 scraped `electrons` 对理论产物速度的 `allclose`；把 `test_2d_ohm_solver_landau_damping_picmi` 补成 `"--test --dim 2 --temp_ratio 0.1" + analysis.py + checksum`，并写清其当前 `field_data.txt` 只是 Landau-damping 曲线 side consumer，而 `diag1000100` checksum 才是主自动 gate；把 `test_2d_laser_on_fine` 补成 `analysis=OFF + checksum` 的 AMR/PML placement workflow。同时也把三条对应 input-level 行进一步压实为更明确的 producer/runtime scaffold。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `pierce_diode` / `ohm_solver_ion_beam_instability` / `laser_ion` 邻近 active baseline 条目：已把 `test_1d_pierce_diode` 补成 `analysis_pierce_diode.py + checksum` 的双层合同，并写清其真正强断言是最终 `phi/j_z` 对 Child-Langmuir 理论解逐点相对误差 `< 20%`；把 `test_1d_ohm_solver_ion_beam_picmi` 补成 `"--test --dim 1 --resonant" + analysis.py + checksum`，并写清其主消费者是 `field_data.txt` 上 `m=4,5,6` 低模增长率 RMS error 的三条 `np.isclose(..., atol=0.01)` 强断言；同时把 `test_2d_laser_ion_acc_no_field_diag` 从宽泛“本地 active 变体”压实为 benchmark-only legacy residue，明确本地 `laser_ion` family 当前真实 active regression 只有 native / PICMI 两条主线。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `laser_ion` / `ohm_solver_em_modes` / `silver_mueller` 邻近 active baseline 与 input-level 条目：已把 `test_2d_laser_ion_acc` / `test_2d_laser_ion_acc_picmi` 补成 `analysis_test_laser_ion.py + checksum` 的双层合同，并写清其真正强断言是 `diagInst` 末 5 帧 `E_z` 后处理平均对 `diagTimeAvg` 原位平均的 `np.allclose(rtol=1e-12)`；把 `test_1d_ohm_solver_em_modes_picmi` 补成“1D parallel-mode 频谱可视化 side consumer + `field_diag000250` checksum 主自动 gate”；把 `test_1d_silver_mueller`、`test_2d_silver_mueller_x`、`test_2d_silver_mueller_z` 补成共享 `analysis.py + checksum` 的全域残余场阈值消费者链。同时也把对应 input-level 行进一步压实为更明确的 producer/runtime scaffold。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `laser_ion` / `ohm_solver_em_modes` / `silver_mueller` 收尾 helper 条目：已把三边的 `analysis_default_regression.py` 都压实为目录内符号链接到共享 `plotfile/openpmd` checksum helper 的描述，并进一步补清当前 `laser_ion` 是两条 `analysis_test_laser_ion.py + checksum`，`ohm_solver_em_modes` 分成 `1D analysis.py + checksum` 与 `RZ analysis_rz.py + checksum --rtol 1e-6`，`silver_mueller` 则是 1D / 2Dx / 2Dz / RZ 四条 active regression 全部统一 `analysis.py + checksum`。因此这三组现在也都更清楚地分成了强 analysis 消费者链与附加 checksum 包装链两层。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `pierce_diode` / `uniform_plasma` 收尾 helper 条目：已把两边的 `analysis_default_regression.py` 都压实为目录内符号链接到共享 `plotfile/openpmd` checksum helper 的描述，并进一步补清当前 `pierce_diode` 是单条 `analysis_pierce_diode.py + checksum`，而 `uniform_plasma` 则分成两条主线 `analysis=OFF + checksum` 与一条 `analysis_default_restart.py + checksum --rtol 1e-12` 的 restart 变体。因此这两组现在也更清楚地分成了 Child-Langmuir 强消费者链或 workflow/checkpoint 覆盖路径，加附加 checksum 包装链两层。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `point_of_contact_eb` / `relativistic_space_charge_initialization` / `reduced_diags` 收尾 helper 条目：已把三边的 `analysis_default_regression.py` 都压实为目录内符号链接到共享 `plotfile/openpmd` checksum helper 的描述，并进一步补清当前 `point_of_contact_eb` 是两条 active regression 全部统一 `analysis.py + checksum`、`relativistic_space_charge_initialization` 是 `analysis.py + checksum --skip-particles`、`reduced_diags` 则分成 `analysis_reduced_diags.py + checksum` 与一组 `analysis_reduced_diags_load_balance_costs.py + checksum` 的 load-balance-costs 变体。因此这三组现在也都更清楚地分成了强 analysis 消费者链与附加 checksum 包装链，其中 relativistic self-field 这边还显式暴露出字段基线与粒子输出分离的 `--skip-particles` 边界。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `nuclear_fusion` / `pec` / `photon_pusher` / `python_wrappers` 收尾 helper 条目：已把四边的 `analysis_default_regression.py` 都压实为目录内符号链接到共享 `plotfile/openpmd` checksum helper 的描述，写清它们当前会按测试名区分普通基线和 `_restart` 基线，并通过 `yt.load` / `OpenPMDTimeSeries` 自动探测输出格式；同时也写清当前 `nuclear_fusion/CMakeLists.txt` 把 6 条 fusion regression 全都绑定成 `analysis + checksum`，`photon_pusher/CMakeLists.txt` 把 `test_3d_photon_pusher` 绑定成 `analysis.py + checksum`，`pec/CMakeLists.txt` 是 mixed 结构，standing-wave / implicit-insulator 变体走 `analysis + checksum`，而 particle / explicit-insulator 变体维持 `analysis=OFF + checksum`，`python_wrappers/CMakeLists.txt` 则把 `test_2d_python_wrappers_picmi` 维持成 `analysis=OFF + checksum`；因此 helper 本身并不消费 fusion yield / product 统计、PEC standing-wave / energy-accounting、photon single-particle 轨道，或 Python field-wrapper 的脚本内 `sim.fields.get(...)` 强断言。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `collider_relevant_diags` / `nci_psatd_stability` / `qed` 收尾 helper 条目：已把三边的 `analysis_default_regression.py` 都压实为目录内符号链接到共享 `plotfile/openpmd` checksum helper 的描述，写清它们当前会按测试名区分普通基线和 `_restart` 基线，并通过 `yt.load` / `OpenPMDTimeSeries` 自动探测输出格式；同时也写清当前 `collider_relevant_diags/CMakeLists.txt` 把 `test_3d_collider_diagnostics` 绑定成 `analysis.py + checksum`，`nci_psatd_stability/CMakeLists.txt` 是混合结构，绝大多数 active regression 走 `analysis_galilean.py` 或 `analysis_psatd_CC1.py + checksum`，少数 hybrid / JRhom 变体维持 `analysis=OFF + checksum`，而 `qed/CMakeLists.txt` 则把 10 条 Breit-Wheeler / Quantum-Synchrotron / Schwinger regression 全都绑定成 `analysis + checksum`；因此 helper 本身并不消费 collider diagnostics 的解析统计量与 `dL/dt` 交叉校验、PSATD 能量/电荷守恒阈值断言，或 QED pair / photon / optical-depth 强断言。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `accelerator_lattice` / `boosted_diags` / `boundaries` / `btd_rz` 收尾 helper 条目：已把四边的 `analysis_default_regression.py` 都压实为目录内符号链接到共享 `plotfile/openpmd` checksum helper 的描述，写清它们当前会按测试名区分普通基线和 `_restart` 基线，并通过 `yt.load` / `OpenPMDTimeSeries` 自动探测输出格式；同时也写清当前 `accelerator_lattice/CMakeLists.txt` 把三条 hard-edged quadrupole regression 全都绑定成 `analysis.py + checksum`，`boosted_diags/CMakeLists.txt` 把 `test_3d_laser_acceleration_btd` 绑定成 `analysis.py + checksum`，`boundaries/CMakeLists.txt` 把 `test_3d_particle_boundaries` 绑定成 `analysis.py + checksum`，`btd_rz/CMakeLists.txt` 把 `test_rz_btd` 绑定成 `analysis.py + checksum`；因此 helper 本身并不消费解析 quadrupole 轨道、BTD writer 一致性 / random-fraction、粒子边界语义闭合，或 RZ BTD 激光包络/相位拟合强断言。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `plasma_mirror` / `spacecraft_charging` / `thomson_parabola_spectrometer` 收尾 helper 条目：已把三边的 `analysis_default_regression.py` 都压实为目录内符号链接到共享 `plotfile/openpmd` checksum helper 的描述，写清它们当前会按测试名区分普通基线和 `_restart` 基线，并通过 `yt.load` / `OpenPMDTimeSeries` 自动探测输出格式；同时也写清当前 `plasma_mirror/CMakeLists.txt` 只把 `test_2d_plasma_mirror` 注册成 `analysis=OFF + checksum`，`spacecraft_charging/CMakeLists.txt` 把 `test_rz_spacecraft_charging_picmi` 绑定成 `analysis.py + checksum`，而 `thomson_parabola_spectrometer/CMakeLists.txt` 则把 `test_3d_thomson_parabola_spectrometer` 绑定成 `analysis.py + checksum`；因此 helper 本身并不消费 `spacecraft_charging` 的 `v0/tau` 指数拟合强断言，也不消费 TPS detector-hit 重建链，而 `plasma_mirror` 当前则完全没有独立 analysis。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `free_electron_laser` / `ion_beam_extraction` / `laser_acceleration` 收尾 helper 条目：已把三边的 `analysis_default_regression.py` 都压实为目录内符号链接到共享 `plotfile/openpmd` checksum helper 的描述，写清它们当前会按测试名区分普通基线和 `_restart` 基线，并通过 `yt.load` / `OpenPMDTimeSeries` 自动探测输出格式；同时也写清当前 `free_electron_laser/CMakeLists.txt` 只把 `test_1d_fel` 绑定成 `analysis_fel.py + checksum`，`ion_beam_extraction/CMakeLists.txt` 只把 `test_3d_ion_beam_extraction` 绑定成 `analysis_ion_beam_extraction.py + checksum`，而 `laser_acceleration/CMakeLists.txt` 则是混合结构，只有 `1d_fluid_boosted`、`2d_refined_injection`、`rz_opmd` 三条 active regression 带独立 analysis，其余 11 条变体都维持 `analysis=OFF + checksum`；因此 helper 本身并不额外消费 FEL gain-length / wavelength、离子束 `40 keV` 尾部能量，或 LWFA wakefield / diagnostics / refined-injection 强断言。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `beam_beam_collision` / `plasma_acceleration` 收尾 helper 条目：已把两边的 `analysis_default_regression.py` 都压实为目录内符号链接到共享 `plotfile/openpmd` checksum helper 的描述，写清它们当前会按测试名区分普通基线和 `_restart` 基线，并通过 `yt.load` / `OpenPMDTimeSeries` 自动探测输出格式；同时也写清当前 `beam_beam_collision/CMakeLists.txt` 只把 `test_3d_beam_beam_collision` 注册成 `analysis=OFF + checksum`，而 `plasma_acceleration/CMakeLists.txt` 则把整组 1D/2D/3D、native/PICMI/MR/hybrid/boosted 变体全都维持成 `analysis=OFF + checksum`，因此 helper 本身并不消费独立 beamstrahlung / pair-yield 或 wakefield 物理断言，因为这两组 active regression 当前都没有单独 analysis。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `capacitive_discharge` 收尾 helper 条目：已把 `analysis_default_regression.py` 压实为目录内符号链接到共享 `plotfile/openpmd` checksum helper 的描述，写清它当前会按测试名区分普通基线和 `_restart` 基线，并通过 `yt.load` / `OpenPMDTimeSeries` 自动探测输出格式；同时也写清当前 `capacitive_discharge/CMakeLists.txt` 的 active 绑定结构是 `1D background_mcc: analysis_1d.py + checksum`、`1D dsmc: analysis_dsmc.py + checksum`、`2D native/PICMI: analysis=OFF + checksum`，而 helper 本身并不消费 1D Turner case-1 离子密度强断言，也不消费 2D PICMI 外部 Poisson-solver callback 的脚本内运行断言。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `subcycling_mr` / `larmor` 收尾 helper 条目：已把两边的 `analysis_default_regression.py` 都压实为目录内符号链接到共享 `plotfile/openpmd` checksum helper 的描述，写清它们当前会按测试名区分普通基线和 `_restart` 基线，并通过 `yt.load` / `OpenPMDTimeSeries` 自动探测输出格式；同时也写清当前 `subcycling/CMakeLists.txt` 只把 `test_2d_subcycling_mr` 注册成 `analysis=OFF + checksum`，而 `larmor/CMakeLists.txt` 也把 `test_2d_larmor` 维持成 `analysis=OFF + checksum`，因此 helper 本身并不消费独立解析强断言，因为这两条 active regression 当前都没有单独 analysis。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `particles_in_pml` / `resampling` 收尾 helper 条目：已把两边的 `analysis_default_regression.py` 都压实为目录内符号链接到共享 `plotfile/openpmd` checksum helper 的描述，写清它们当前会按测试名区分普通基线和 `_restart` 基线，并通过 `yt.load` / `OpenPMDTimeSeries` 自动探测输出格式；同时也写清当前 `particles_in_pml/CMakeLists.txt` 已把四条 active regression 全都统一绑定成 `analysis_particles_in_pml.py + checksum`，而 `resampling/CMakeLists.txt` 则是 `2D leveling_thinning: analysis.py + checksum`、两条 `velocity_coincidence_thinning` 变体维持 `analysis=OFF + checksum` 的混合绑定，而 helper 本身并不消费 finest-level 全域残余场阈值断言，也不消费 `LevelingThinning` 粒子统计强断言。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `particle_absorbing_boundary` 收尾 helper 条目：已把 `analysis_default_regression.py` 压实为目录内符号链接到共享 `plotfile/openpmd` checksum helper 的描述，写清它当前会按测试名区分普通基线和 `_restart` 基线，并通过 `yt.load` / `OpenPMDTimeSeries` 自动探测输出格式；同时也写清当前 `particle_absorbing_boundary/CMakeLists.txt` 把 active 1D regression 绑定成 `analysis.py + checksum`，而 helper 本身并不消费 `PhaseSpaceElectrons` reduced histogram 尾部权重积分断言。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `particle_boundary_process` / `particle_thermal_boundary` 收尾 helper 条目：已把两边的 `analysis_default_regression.py` 都压实为目录内符号链接到共享 `plotfile/openpmd` checksum helper 的描述，写清它们当前会按测试名区分普通基线和 `_restart` 基线，并通过 `yt.load` / `OpenPMDTimeSeries` 自动探测输出格式；同时也写清当前 `particle_boundary_process/CMakeLists.txt` 是 `2D reflection: analysis=OFF + checksum`、`3D absorption: analysis_absorption.py + checksum` 的分叉绑定，而 `particle_thermal_boundary/CMakeLists.txt` 则把 active regression 统一绑定成 `analysis.py + checksum`，而 helper 本身并不消费 `z_hi/z_lo` scraped-buffer 计数与 `stepScraped` 强断言、`612 -> 0` 双快照吸收断言，或 `EF/EN` reduced-diag 能量账本断言。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `particle_boundary_interaction` / `secondary_ion_emission` 收尾 helper 条目：已把两边的 `analysis_default_regression.py` 都压实为目录内符号链接到共享 `plotfile/openpmd` checksum helper 的描述，写清它们当前会按测试名区分普通基线和 `_restart` 基线，并通过 `yt.load` / `OpenPMDTimeSeries` 自动探测输出格式；同时也写清当前 `CMakeLists.txt` 都把 active RZ PICMI regression 统一绑定成 `analysis.py + checksum`，而 helper 本身并不消费 `analysis.py` 的解析几何强断言，也不消费输入脚本里 `afterstep mirror_reflection` / `afterstep secondary_emission` 的 scrape-buffer callback 合同。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `scraping` 收尾 helper 条目：已把 `analysis_default_regression.py` 压实为目录内符号链接到共享 `plotfile/openpmd` checksum helper 的描述，写清它当前会按测试名区分普通基线和 `_restart` 基线，并通过 `yt.load` / `OpenPMDTimeSeries` 自动探测输出格式；同时也写清当前 `CMakeLists.txt` 在 `WarpX_EB` 打开时把 `test_rz_scraping` 绑定成 `analysis_rz.py + checksum`、把 `test_rz_scraping_filter` 绑定成 `analysis_rz_filter.py + checksum`，而 helper 本身并不消费剩余粒子数 / scraped 粒子数 / `id` 闭合合同，也不消费 `z>0` 半域筛选合同。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `embedded_boundary_python_api` 收尾 helper 条目：已把 `analysis_default_regression.py` 压实为目录内符号链接到共享 `plotfile/openpmd` checksum helper 的描述，写清当前 `CMakeLists.txt` 只在 `WarpX_EB` 打开时注册一条 active regression `test_3d_embedded_boundary_picmi`，且明确写成 `analysis=OFF + checksum`，而 helper 本身并不消费输入脚本内建的 `edge_lengths/face_areas` 几何硬断言。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `embedded_boundary_em_particle_absorption` 收尾 helper 条目：已把 `analysis_default_regression.py` 压实为目录内符号链接到共享 `plotfile/openpmd` checksum helper 的描述，写清当前 `CMakeLists.txt` 在 `WarpX_EB` 打开时已把 2D / 3D / RZ 三组共九条 active regression 全都统一绑定成 `analysis.py + checksum`，而 helper 本身并不消费 `analysis.py` 里对时间平均 `divE` 的几何分支化 `L∞` 无静态伪电荷强断言。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `pass_mpi_communicator` reserve 条目：已把 `analysis.py` 压实为更明确的离线 checksum 对照脚本描述，写清它会比较 `Python_pass_mpi_comm_plt1_000010` / `plt2_000010` 的 outer/inner schema 完全一致，并要求除 `particle_cpu / particle_id / particle_position_y` 外大多数 checksum 数值项都彼此不同；同时也把 `analysis_default_regression.py` 补成更准确的未接线 helper 边界，写清它虽然就是目录内符号链接到共享 checksum helper，但当前 `CMakeLists.txt` 仍把唯一的 `test_2d_pass_mpi_comm_picmi` 注册成 `analysis=OFF + checksum=OFF`，并明确留有三条 `TODO` 注释要求先在 pyAMReX 中启用 communicator handoff。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `plasma_lens` 收尾 helper 条目：已把 `analysis_default_regression.py` 压实为目录内符号链接到共享 `plotfile/openpmd` checksum helper 的描述，写清当前 `CMakeLists.txt` 已把 repeated-plasma-lens、boosted、hard-edged、PICMI、Python front-end 和 short-lens 六条 active regression 全都统一绑定成 `analysis.py + checksum`，而 helper 本身并不消费 `analysis.py` 里对两颗测试电子最终 `x/y/ux/uy` 与解析透镜串联模型的强断言。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `particle_fields_diags` 收尾 helper / single-precision 保留项：已把 `analysis_default_regression.py` 压实为目录内符号链接到共享 `plotfile/openpmd` checksum helper 的描述，写清当前 active `CMakeLists.txt` 只把双精度 `test_3d_particle_fields_diags` 绑定成 `analysis_particle_diags.py + checksum`；同时也把 `analysis_particle_diags_single.py` 补成更明确的保留边界，写清它虽然会以 `single_precision=True` 复用同一手工重建实现、把容差放宽到 `5e-3`，但对应的 `test_3d_particle_fields_diags_single_precision` 仍整段停在 `# FIXME` 注释块中，并没有被 active regression 注册。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `particle_data_python` 收尾 helper 条目：已把 `analysis_default_regression.py` 压实为目录内符号链接到共享 `plotfile/openpmd` checksum helper 的描述，写清它当前会按测试名区分普通基线和 `_restart` 基线，并通过 `yt.load` / `OpenPMDTimeSeries` 自动探测输出格式，但本身并不消费 `inputs_test_2d_particle_attr_access_picmi.py` 里对 runtime real-comp 注册、before-step 注粒子 callback、tile 级 `newPid` 回读与手动 `deposit_current(...)` 的强断言，也不消费 `inputs_test_2d_prev_positions_picmi.py` 里对 `prev_x/prev_z` runtime comp 索引、`prev_z < zmax` 与 iterator 计数一致性的强断言。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `particle_boundary_scrape` 收尾 helper 条目：已把 `analysis_default_regression.py` 压实为目录内符号链接到共享 `plotfile/openpmd` checksum helper 的描述，写清它当前会按测试名区分普通基线和 `_restart` 基线，并通过 `yt.load` / `OpenPMDTimeSeries` 自动探测输出格式，但本身并不消费 `analysis_scrape.py` 的 `612 -> 0` 双快照主容器删粒子合同，也不消费 PICMI 输入脚本尾部 `ParticleBoundaryBufferWrapper()` 的 size / `stepScraped` / `w`-sum / `clear_buffer()` 强断言。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `load_density` 收尾 helper 条目：已把 `analysis_default_regression.py` 压实为目录内符号链接到共享 `plotfile/openpmd` checksum helper 的描述，写清它当前会按测试名区分普通基线和 `_restart` 基线，并通过 `yt.load` / `OpenPMDTimeSeries` 自动探测输出格式，但本身并不消费 1D/2D/3D/RZ 四条逐 iteration `rho`-to-density 解析闭合强消费者链。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `load_external_field` 收尾 helper 条目：已把 `analysis_default_regression.py` 压实为目录内符号链接到共享 `plotfile/openpmd` checksum helper 的描述，写清它当前会按测试名区分普通基线和 `_restart` 基线，并通过 `yt.load` / `OpenPMDTimeSeries` 自动探测输出格式，但本身并不增加 external-field 物理断言，也不消费磁镜反射末态位置或时变外场缩放消费者链。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `magnetostatic_eb` 收尾 helper 条目：已把 `analysis_default_regression.py` 压实为目录内符号链接到共享 `plotfile/openpmd` checksum helper 的描述，写清它当前会按测试名区分普通基线和 `_restart` 基线，并通过 `yt.load` / `OpenPMDTimeSeries` 自动探测输出格式，但本身并不增加 magnetostatic 物理断言，也不消费 `Efield_aux/Bfield_aux` 或解析 `Er/B_theta`。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `nodal_electrostatic` 收尾 helper 条目：已把 `analysis_default_regression.py` 压实为目录内符号链接到共享 `plotfile/openpmd` checksum helper 的描述，写清它当前只负责按测试名与 `--path` 选择输出基线，本身并不消费 `analysis.py` 里对 `ParticleExtrema_beam_p.txt` 的 `chi_max < 2e-8` 零触发断言，也不消费 `ParticleNumber.txt` 里 photon 计数始终为 `0` 的 reduced-diagnostic 合同。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `open_bc_poisson_solver` 收尾 helper 条目：已把 `analysis_default_regression.py` 压实为目录内符号链接到共享 `plotfile/openpmd` checksum helper 的描述，写清它当前只负责按 `--path` 与显式 `--rtol 1e-2` 之类参数选择输出基线与容差，本身并不消费 `analysis.py` 里对 openPMD `Ex/Ey` 的 Basseti-Erskine 横向场逐切片解析断言。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `electrostatic_dirichlet_bc` 残项：已把 `analysis_default_regression.py` 压实为目录内符号链接到共享 `plotfile/openpmd` checksum helper 的描述；同时也把 `analysis.py` 从宽泛“比较边界势”压成更明确的时间序列消费者链，写清它当前会逐个 plotfile 读取两侧边界平面的平均 `phi`，再按 `150*sin(2*pi*6.78e6*t)` 与 `450*sin(2*pi*13.56e6*t)` 两条驱动函数重建期望序列，并分别要求 `rtol = 0.1` 的 `allclose`；相对地，`inputs_test_2d_dirichlet_bc` 与 `inputs_test_2d_dirichlet_bc_picmi.py` 也都已补成更明确的 native / PICMI runtime scaffold，最后还把两条 baseline 从宽泛“checksum 基线”补成 `analysis.py + analysis_default_regression.py --path diags/diag1000100` 的双层合同。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `electrostatic_sphere` family 收尾条目：已把 `analysis_default_regression.py` 压实为目录内符号链接到共享 `plotfile/openpmd` checksum helper 的描述；同时也把 `analysis_electrostatic_sphere.py` 从宽泛“解析电场与能量账本”压成更明确的强消费者链，写清它当前会先按 `q_tot=-1e-15`、`r_0=0.1`、`t_exact(r)` 和测试名里的 `emass_10` / `uniform_weighting` 分支反求膨胀半径 `r_end`，再对 `Ex/Ey/Ez` 或 `Er/Ez` 施加解析场相对 `L2` 断言，并且只在 `diag2` 的 openPMD 粒子输出确实带 `phi` 时才继续检查 `Ek + Ep` 能量账本；相对地，`inputs_base_3d` 与 `inputs_test_3d_electrostatic_sphere` 也已补成更明确的原生 runtime scaffold，写清主 3D 基线本质上只是复用公共 `relativistic electrostatic` 均匀电子球自场膨胀输入；同时 `catalyst_pipeline.py` 也已单独标明只是 `|E|` 可视化 helper，不参与自动 regression 断言。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `effective_potential_electrostatic` 残项：已把 `analysis_default_regression.py` 压实为目录内符号链接到共享 `plotfile/openpmd` checksum helper 的描述；同时也把 `analysis.py` 从宽泛“读取 `rho_electrons` 并比较径向 RMS”压成更明确的强消费者链，写清它当前会先从 `sim_parameters.dpkl` 重建 `sigma_0/M/T_i/T_e/n_plasma` 与特征膨胀时间 `tau`，再对 `diags/field_diag` 的每个 openPMD iteration 读取 `rho_electrons`，通过球坐标重采样和角向平均得到数值径向电子密度，并逐时刻要求归一化 RMS 误差小于 `0.07`；相对地，`inputs_test_3d_effective_potential_electrostatic_picmi.py` 也已补成更明确的 PICMI runtime scaffold，写清它当前显式用 `ElectrostaticSolver(..., warpx_effective_potential=True, warpx_effective_potential_factor=C_EP)` 打开 effective-potential Poisson 路径，在零电势球形 `EmbeddedBoundary` 内注入高斯电子/离子云，并额外 materialize `sim_parameters.dpkl` 与 openPMD `field_diag` 供后续 analysis 消费。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `relativistic_space_charge_initialization` 残项：已把 `analysis_default_regression.py` 压实为目录内符号链接到共享 `plotfile/openpmd` checksum helper 的描述；同时也把 `analysis.py` 从宽泛“比较 `Ex` 与 `By≈Ex/c` 理论自场”压成更明确的 relativistic self-field 消费者链，并已在后续源码复核中进一步校正为当前真实结构：它并不消费 `By`，而是按维度分支重建解析高斯电荷团 Coulomb 场，并在 3D 路径上对 `Ex/Ey/Ez` 三个分量统一施加 `np.allclose(..., atol=0.175*Emax)` 强断言；相对地，`inputs_test_3d_relativistic_space_charge_initialization` 也已补成更明确的原生 runtime scaffold，最后还把 baseline 从宽泛“checksum 基线”补成 `analysis.py + analysis_default_regression.py --skip-particles` 的双层合同。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `space_charge_initialization` 残项：已把 `analysis_default_regression.py` 压实为目录内符号链接到共享 `plotfile/openpmd` checksum helper 的描述；同时也把 `analysis.py` 从宽泛“Gaussian-beam 初始 self-field 对照”压成更明确的 2D/3D 强消费者链，写清它当前会直接从 level-0 全域字段重建 Gaussian charge cloud 的解析 Coulomb 场，并分别对 `Ex/Ey` 或 `Ex/Ey/Ez` 施加统一 `tolerance_rel = 0.165` 的逐分量 `allclose` 断言；相对地，`inputs_test_2d_space_charge_initialization` 与 `inputs_test_3d_space_charge_initialization` 也都已补成更明确的原生 runtime scaffold，最后还把 2D/3D baseline 从宽泛“checksum 基线”补成 `analysis.py + analysis_default_regression.py --skip-particles` 的双层合同。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `projection_div_cleaner` 残项：已把 `analysis_default_regression.py` 压实为目录内符号链接到共享 `plotfile/openpmd` checksum helper 的描述；同时也把 `analysis.py` 从宽泛“RZ divB 断言”压成更明确的柱坐标强消费者链，写清它当前会在 `raw Bx_aux/Bz_aux` 上按 `(1/r)d(rBr)/dr + dBz/dz` 的离散公式重建 interior `divB`，再要求 `sqrt(sum(divB^2)) < 4e-3`；相对地，`inputs_test_rz_projection_div_cleaner`、`inputs_test_3d_projection_div_cleaner_picmi.py`、`inputs_test_3d_projection_div_cleaner_callback_picmi.py`、`inputs_test_2d_projection_div_cleaner_initial_analytical_field_picmi.py` 也都已补成更明确的原生 runtime scaffold，分别写清 file-backed / callback-loaded / analytic initial field 三条 projection-cleaner 路径的 raw auxiliary-field 或 in-memory `divB` 强断言合同。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `gaussian_beam` 残项：已把 `analysis_default_regression.py` 压实为目录内符号链接到共享 `plotfile/openpmd` checksum helper 的描述；同时也把 `analysis_focusing_beam.py`、`analysis_rotated_beam.py` 从宽泛“束斑/动量检查”压成更明确的强消费者链，写清它们当前分别命中 openPMD 末态粒子切片束斑对理论聚焦曲线的双横向断言，以及逆旋后的束斑统计加 `uz/ux` 动量统计联合断言；相对地，`inputs_test_3d_focusing_gaussian_beam`、`inputs_test_3d_focusing_gaussian_beam_photons`、`inputs_test_3d_rotated_gaussian_beam` 也都已补成更明确的原生 runtime scaffold，最后还把 `test_3d_rotated_gaussian_beam` 从宽泛“checksum 基线”补成 `analysis_rotated_beam.py + analysis_default_regression.py --path diags/diag1000000` 的双层合同。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `flux_injection` 残项：已把 `analysis_default_regression.py` 压实为本地 `plotfile/openpmd` checksum 包装器描述；同时也把 `analysis_flux_injection_3d.py`、`analysis_flux_injection_rz.py`、`analysis_flux_injection_from_eb.py` 从宽泛“分布/总通量检查”压成更明确的强消费者链，写清它们当前分别命中 3D 四物种逐分量 Gaussian/Gaussian-flux 直方图断言、RZ 方位向连续注入的固定 Larmor 半径带与总注入量断言，以及 embedded-boundary 发射路径里按 `2D/RZ/3D` 自动分支的几何重建、总权重闭合、EB 外约束与局部法/切向速度分布断言；相对地，`inputs_base_from_eb`、`inputs_test_2d_flux_injection_from_eb`、`inputs_test_3d_flux_injection`、`inputs_test_3d_flux_injection_from_eb`、`inputs_test_rz_flux_injection`、`inputs_test_rz_flux_injection_from_eb` 也都已补成更明确的原生 runtime scaffold，最后还把 `test_2d_flux_injection_from_eb` 从宽泛“checksum 基线”补成 `analysis_flux_injection_from_eb.py + analysis_default_regression.py --path diags/diag1000020` 的双层合同。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `field_probe` 条目：已把 `analysis.py` 从宽泛“line probe 衍射包络对照”压实为更明确的 reduced-diagnostic 消费者链，写清它会直接读取 `diags/reducedfiles/FP_line.txt`，只消费 `step = 500` 上的 `x/S` 列，把 `I_0 = max(S)` 当成数值峰值，并只在 `counter = 60:2:138` 这一段远离边界的 probe 点上对单缝 `sinc^2` 包络做窗口化平均百分比误差断言、要求 `averror < 2.5`；同时也把 `analysis_default_regression.py` 压实为本地 `plotfile/openpmd` checksum 包装器描述，把 `inputs_test_2d_field_probe` 补成更明确的原生 runtime scaffold，写清它当前显式 materialize 出单缝薄片 EB、近似 plane-wave 的 Gaussian laser、`diag1` Full plotfile 与 `201` 点 line-integrated `FieldProbe`；最后也把 `test_2d_field_probe` 从宽泛“checksum 基线”补成 `analysis.py + analysis_default_regression.py --path diags/diag1000544` 的双层合同。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `embedded_boundary_rotated_cube` 条目：已把 `analysis_default_regression.py` 从宽泛“通用 checksum helper”压实为更明确的本地 `plotfile/openpmd` 输出基线包装器描述；同时也把 `analysis_fields_2d.py`、`analysis_fields_3d.py`、`inputs_test_2d_embedded_boundary_rotated_cube`、`inputs_test_3d_embedded_boundary_rotated_cube` 与对应 2D/3D active baseline 一并补成更明确的 consumer/runtime 合同，写清 2D 版是在反旋后的本征坐标系里对有效区域 `By` 做 `< 1e-1` 的 `L2` 误差断言，3D 版则直接读取 `raw By_fp/Bz_fp`，在两套 staggered 采样点上反旋坐标和分量后分别施加 `< 1e-2` 的双分量 `L2` 误差断言；两张输入卡也同步补清成 `algo.maxwell_solver = ect`、parser materialize 的 rotated EB、外加旋转本征磁模，以及 3D 版额外打开 `diag1.plot_raw_fields = 1` 的原生 runtime scaffold。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `electrostatic_sphere_eb` 收尾 helper 条目：已把 `analysis_default_regression.py` 从宽泛“通用 checksum helper”压实为更明确的本地 `plotfile/openpmd` 输出基线包装器描述，写清它当前只负责自动探测输出格式、按目录名推导 test name、切换 `restart` 容差与 `do_fields/do_particles`，并不消费 3D native / PICMI 路径上的 `ChargeOnEB + eb_covered`，也不消费 RZ / RZ+MR 路径上的解析 `phi/Er`。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `embedded_boundary_diffraction` 条目：已把 `analysis_default_regression.py` 从宽泛“通用 checksum helper”压实为更明确的本地 `plotfile/openpmd` 输出基线包装器描述，写清它当前只负责自动探测输出格式、按目录名推导 test name、切换 `restart` 容差与 `do_fields/do_particles`，并不消费 openPMD `E_x(r,z)`、第一极小值半径轨迹或 Airy 锥角包络；同时也把 `inputs_test_rz_embedded_boundary_diffraction` 从宽泛“RZ laser-by-EB diffraction 场景”补成更明确的原生 runtime scaffold，写清它当前显式 materialize 出 `warpx.n_rz_azimuthal_modes = 2` 的圆柱衍射孔 EB、沿 `+z` 入射的 `Gaussian` laser，以及 `diag1.format = openpmd` 的全场时间序列 producer。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `embedded_boundary_cube` 收尾条目：已把 `analysis_default_regression.py` 从宽泛“通用 checksum helper”压实为更明确的本地 `plotfile/openpmd` 输出基线包装器描述，写清它当前只负责自动探测输出格式、按目录名推导 test name、切换 `restart` 容差与 `do_fields/do_particles`，并不消费 2D `By`、3D `By/Bz` 或 `macroscopic` 频率修正这些强分析量；同时也把 `test_3d_embedded_boundary_cube` 与 `test_3d_embedded_boundary_cube_macroscopic` 从宽泛“checksum 基线”补成 `analysis_fields.py + analysis_default_regression.py --path diags/diag1000208` 的双层合同，明确写清普通 3D 版完整复用公共 stair-case cubic cavity scaffold，而 macroscopic 版只是在其上额外挂出 `epsilon_r = 1.5` 的介质求解路径。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `embedded_boundary_cube` 条目：已把 `analysis_fields.py` 从宽泛“比较 3D 解析 `By/Bz` 模态”压实为更明确的消费者链，写清它会在固定 `48^3` 腔体盒和 `m=0,n=1,p=1` 参数上逐点重建 `TM_{0,1,1}` 的解析 `By/Bz`，并在测试名含 `macroscopic` 时显式按 `epsilon_r = 1.5` 修正本征频率；同时也把 `analysis_fields_2d.py` 从宽泛“比较 `By` 与 `Ey/c`”压实为更明确的 consumer-side 不对称描述，写清它只对 `By` 施加 `< 1e-3` 的硬断言，而对 `Ey/c` 只是计算误差并没有再 `assert`。相对地，`inputs_base_3d`、`inputs_test_2d_embedded_boundary_cube`、`inputs_test_3d_embedded_boundary_cube` 与 `inputs_test_3d_embedded_boundary_cube_macroscopic` 也都已补成更明确的原生 runtime scaffold：stair-case cubic / square cavity、统一 `eb_potential = 1`、外加解析磁模初始化，以及 2D 版额外同步 materialize 的 `Ey = cB` 模态关系；最后也把 `test_2d_embedded_boundary_cube` 一并补成 `analysis_fields_2d.py + checksum` 的双层合同。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `point_of_contact_eb` 收尾条目：已把 `analysis_default_regression.py` 从宽泛“通用 checksum helper”压实为更明确的本地 plotfile/openPMD 输出基线包装器描述，并把 `test_rz_point_of_contact_eb` 从泛泛“checksum 基线”补成与 3D 版对齐的 `analysis.py + analysis_default_regression.py --path diags/diag1/` 双层合同。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `electrostatic_sphere_eb` analysis-level 条目：已把 `analysis.py` 从宽泛“比较 reduced diagnostic `eb_charge.txt` 与理论球导体电荷，并检查 `eb_covered`”压实为更明确的双消费者链，写清它会分别从 `eb_charge.txt` 与 `eb_charge_one_eighth.txt` 读取总电荷与单八分体电荷，并要求相对理论 `q_th` 与 `q_th/8` 的误差都低于 `6%`，随后再逐格检查 openPMD `eb_covered` 全域都落在 `[0,1]`，并在球内恒为 `1`、球外恒为 `0`；同时也把 `analysis_rz.py` 与 `analysis_rz_mr.py` 从宽泛“解析 `phi/Er` 比较”压实为更明确的消费者链，写清单层 RZ 版会在 `r > 0.1 + dr` 的 EB 外区域逐个半径切片对整条 `z` 方向上的 `phi/Er` 计算最大相对误差并要求小于 `4.1e-3`，而 RZ+MR 版会先逐 level 裁剪出真正的有效 patch，再在每一层 patch 上对解析 `phi/Er` 施加统一的 `4e-3` 最大相对误差断言。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `electrostatic_sphere_eb` input-level 条目：已把五张输入卡从宽泛“3D sphere / mixed-BC / PICMI / RZ / RZ+MR”摘要压实为更明确的原生 producer/runtime 合同，写清 native 3D 版当前固定 `64^3` 盒、全 PEC 外边界、`labframe` 静电解算、半径 `0.1` 的 `1 V` 导体球 EB、openPMD `Ex/Ey/Ez/rho/phi/eb_covered` 与双 `ChargeOnEB` reduced diagnostics；mixed-BC 版则切成非对称 `pec/neumann/dirichlet` 组合、半径 `0.3` 导体球且只保留纯 plotfile 诊断；PICMI 版进一步补清成 `Cartesian3DGrid + ElectrostaticSolver + EmbeddedBoundary` 前端，并在两步运行中显式打通 `set_potential_on_eb("2.")` 入口以及与 native 对齐的 `eb_covered + ChargeOnEB` 诊断面；RZ 单层与 RZ+MR 两条输入则分别补成固定电势圆柱导体 EB 的单层 / multi-level openPMD `Er/phi/eb_covered` producer。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `point_of_contact_eb` 条目：已把 `analysis.py` 从宽泛“比较 `stepScraped`、`deltaTimeScraped`、接触点与法向”压实为更明确的逐项消费者链，写清它会直接从 `OpenPMDTimeSeries("./diags/diag2/particles_at_eb/")` 读取 `stepScraped`、`deltaTimeScraped`、`x/y/z` 与 `nx/ny/nz`，再与硬编码解析参考值 `step=3`、`deltaTimeScraped=0.59e-10`、`x=-0.1983`、`y=0.02584`、`nx=-0.99`、`ny=0.13` 逐项比较，并分别施加 `0.1% / 1% / 1%` 级别的硬容差；同时也把 `inputs_test_3d_point_of_contact_eb` 与 `inputs_test_rz_point_of_contact_eb` 从宽泛“单粒子接触点基准”压实为更明确的原生 runtime scaffold，写清它们分别 materialize 球形 / 圆柱 EB、关闭场推进、只保留一个从 `(-0.25,0,0)` 出发的单电子，并打开 openPMD `BoundaryScraping` 诊断；最后也把 `test_3d_point_of_contact_eb` 一并补成 `analysis.py + checksum` 的双层合同。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `embedded_boundary_python_api` 相邻 input-level 条目：已把 `inputs_test_3d_embedded_boundary_picmi.py` 从宽泛“3D PICMI wrapper 自检”压实为更明确的 in-process runtime 合同，写清它当前显式组装 `64^3` `Cartesian3DGrid`、`x=open / y=dirichlet / z=periodic` 混合场边界、`ECT` solver 与 `L_cavity = 30 mm` 的立方 `EmbeddedBoundary`，并在 `sim.step(1)` 后通过 `sim.fields.get(...)` 读取 `edge_lengths_{x,y,z}` 与 `face_areas_{x,y,z}`，对三个中截面的 perimeter 和 area 分别施加 `4 * L_cavity` 与 `L_cavity^2 - 2 * dA` 的闭式几何硬断言，最后再额外推进一步，把 wrapper 几何检查串进真实 PICMI 运行流。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `embedded_boundary_em_particle_absorption` 条目：已把 family 级 `analysis.py` 从宽泛“对 `divE` 做时间平均”压实为更明确的几何分支消费者链，写清它会用 `OpenPMDTimeSeries("./diags/diag1/")` 读取整段 `divE` 序列，在 `25:100` 上做时间平均，并按 `2dcartesian / 3dcartesian / thetaMode` 分别施加 `3.5e-10 / 7e-11 / 4e-12` 的 `L∞` 阈值，其中 RZ 还会先把 `divE_avg[:,13:19]` 置零以屏蔽 axis artifact；同时也把 `inputs_base` 从宽泛“公共骨架”压实为更明确的共享 runtime scaffold，写清它当前 materialize 出圆柱 EB、从原点对向撞击 EB 的异号超相对论单粒子，以及每步落盘的 openPMD `divE/rho` producer；随后又把 2D/3D/RZ 九张输入卡压实为更明确的几何、边界与 `particle_shape` 变体合同，并补清 3D/RZ 的 `sh_factor_2` 名字当前仍实际命中 `particle_shape = 1`；最后也把 still-coarse 的三条 2D active baseline 一并补成 `analysis.py + checksum` 的双层合同。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `particles_in_pml` 条目：已把 `analysis_particles_in_pml.py` 从宽泛“检查粒子离域后域内 `Ex/Ey/Ez` 的最大残余值是否足够小”压实为更明确的消费者链，写清它会直接在最终 plotfile 上展开 finest-level 全域 `Ex/Ey/Ez` 数组，取 `max_Efield = max(max(Ex), max(Ey), max(Ez))`，并按 `dimensionality + max_level` 分支施加四档绝对阈值：`2D` 单级 `< 3e-4`、`2D` MR `< 6e-4`、`3D` 单级 `< 10`、`3D` MR `< 110`；同时也把四张输入卡从宽泛“single-level/MR particle-PML 场景”压实为更明确的原生 runtime 合同，写清它们共同固定 `warpx.pml_has_particles = 1`、`warpx.do_pml_in_domain = 1`、`warpx.do_pml_j_damping = 1` 的 particle-in-PML 路径，并分别 materialize 单级 / refined-patch / refined-cube 几何与 `electron/proton` 对向单粒子离域设置；最后也把四条 active baseline 一并补成 `analysis_particles_in_pml.py + checksum` 的双层合同。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `particle_thermal_boundary` 条目：已把 `inputs_test_2d_particle_thermal_boundary` 从宽泛“2D domain thermal boundary 基准”压实为更明确的原生 runtime 合同，写清它当前固定 `16 x 16` 的 2D 均匀热电子/碳离子等离子体、全 `pml` 场边界、全 `thermal` 粒子边界，并通过 `boundary.electrons.u_th` / `boundary.C.u_th` 给两种 species 单独定义 Maxwellian 再热化速度；同时也把 `analysis.py` 从宽泛“用 `FieldEnergy` 与 `ParticleEnergy` 约束总量稳定性”压实为更明确的 reduced-diag 消费者链，写清它只读取 `EF.txt` 与 `EN.txt` 两份账本，并分别要求场能满足 `final_Fenergy / init_Fenergy < 40` 与 `final_Fenergy < 5e-5`，粒子总能量相对漂移低于 `2%`；最后也把 active baseline `test_2d_particle_thermal_boundary` 一并补成 `analysis.py + checksum` 的双层合同。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `particle_pusher` 条目：已把 `inputs_test_3d_particle_pusher` 从宽泛“3D force-free relativistic Higuera-Cary 骨架”压实为更明确的原生 runtime 合同，写清它当前固定 `max_step = 10000`、超大周期盒、单个 `gamma≈20` 的 positron、常量 `Bz = 1` 与满足 `Ex = -Vy*Bz` 的 force-free 外场，并显式走 `algo.particle_pusher = "higuera"`；同时也把 `analysis.py` 从宽泛“检查单粒子 `x≈0`”压实为更明确的单标量消费者链，写清它只读取最终 plotfile 中的 `particle_position_x`，并直接要求 `abs(x) < 1e-3`，同时依赖源码里列出的 `Boris/Vay/HC` 参考误差来体现这条判据的区分性；最后也把 active baseline `test_3d_particle_pusher` 一并补成 `analysis.py + checksum` 的双层合同。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `particle_fields_diags` 条目：已把 `inputs_test_3d_particle_fields_diags` 从宽泛“3D 多 species diagnostics 骨架”压实为更明确的原生 producer 合同，写清它当前固定 `32^3` 周期盒、`esirkepov + energy-conserving + use_filter=1 + yee`，并在 `diag1/openpmd` 两套 `Full` diagnostics 上同步挂出 `particle_fields_to_plot = z uz uz_filt zuz jz`、过滤器 `uz < 0` 和 `jz.do_average = 0`；同时也把 `analysis_particle_diags.py` 与 `analysis_particle_diags_impl.py` 从宽泛“plotfile/openPMD 中的粒子归约 mesh 与手工重建值一致”压实为更明确的消费者链，写清入口脚本只是双精度 wrapper，而实现层会从三类粒子的原始 `position_z / momentum_z / weight` 手工重建每个 cell 的 `zavg/uzavg/zuzavg/uzavg_filt/jz`，再分别与 plotfile `boxlib` meshes 和 openPMD iteration `200` 的 meshes 做逐项比对，并要求双精度误差压到 `1e-12`；最后也把 active baseline `test_3d_particle_fields_diags` 一并补成 `analysis_particle_diags.py + checksum` 的双层合同。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `particle_absorption` 条目：已把 `inputs_test_3d_particle_absorption` 从宽泛“3D 吸收基准”压实为更明确的原生 runtime 合同，写清它当前固定 `64 x 64 x 128` 盒、全 `pec` 场边界、`max_step = 60`，并通过 `warpx.eb_implicit_function` materialize 一个 cubic EB，再让一个 `uz = 2000` 的电子 slab 从 `z = -149 .. -129 um` 前冲；同时也把 `analysis_absorption.py` 从宽泛“比较第 40 步与第 60 步电子数”压实为更明确的双快照消费者链，写清它显式读取 `diag1000040` 与 `diag1000060` 两个 plotfile，并要求电子数精确满足 `612 -> 0`；最后也把 active baseline `test_3d_particle_absorption` 一并补成 `analysis_absorption.py + checksum` 的双层合同。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `particle_boundaries` 条目：已把 `inputs_test_3d_particle_boundaries` 从宽泛“3D 最小粒子边界语义测试”压实为更明确的原生 runtime 合同，写清它当前固定 `16^3` 盒、`x/y = pec` 与 `z = periodic` 场边界、`boundary.particle_lo/hi = reflecting absorbing periodic`，并用三组 `MultipleParticles` species 分别沿 `x/y/z` 方向布初值；同时也把 active baseline `test_3d_particle_boundaries` 从宽泛“analysis 对粒子数、速度翻号和解析位置做强断言”压实为更明确的消费者链，写清它会同时读取 `diag1000000` 与 `diag1000008`，按 `particle_id` 排序初末态，再重建 relativistic 解析推进、`do_reflect/do_periodic` 边界映射，并最终要求 absorbing 粒子只剩 `1` 个、reflecting 速度翻号、periodic 速度不变且 `x/z` 相对位置误差低于 `1e-15`。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `particle_absorbing_boundary` 条目：已把 `inputs_test_1d_particle_absorbing_boundary` 从宽泛“1D 吸收边界测试”压实为更明确的原生 runtime 合同，写清它当前固定 `1D` `absorbing_silver_mueller + absorbing particle boundaries`、指数 ramp 靶、`parse_field_function` laser、以及挂在 `electrons` 上的 `particle_thermalizer(start=40 um, end=50 um, momentum_threshold=0.1, theta=0.02)`；同时也把 `analysis.py` 从宽泛“相图里反向高速电子权重足够小”压实为更明确的 reduced-histogram 消费者链，写清它会读取 `PhaseSpaceElectrons` 的 `ParticleHistogram2D` 数据，再结合 `warpx_used_inputs` 里的 bin 边界，把 `z in [0,50] um`、`uz in [-5,-1]` 映射成固定 bin window，并要求其总权重小于 `3.2e20`；最后也把 active baseline `test_1d_particle_absorbing_boundary` 一并补成 `analysis.py + checksum` 的双层合同。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `scraping` analysis-level 条目：已把 `analysis_rz.py` 从宽泛“剩余粒子数 + scraped 计数 + id 闭合”压实为更明确的双 openPMD 时间序列消费者链，写清它当前会先对最终 plotfile 里的盒内粒子数做 `512` 的零容差断言，再同时打开 `diags/diag2/` 与 `diags/diag3/particles_at_eb`，对每个 iteration 重新统计 `n_remaining + n_scraped == n_total`，最后再把初始 `id` 集与“末态盒内 + scrape buffer” 的 `id` 集做全量排序闭合比对；同时也把 `analysis_rz_filter.py` 从宽泛“只记录 `z>0` 半域的 scraped 粒子”压实为更明确的筛选消费者链，写清它在同样读取 `diag2/diag3` 的基础上，显式要求 `2 * n_scraped + n_remaining == n_total`，并逐 iteration 断言 scraped 记录里 `z <= 0` 的命中数恒等于 `0`。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `particle_boundary_interaction` / `secondary_ion_emission` analysis-level 条目：已把 `particle_boundary_interaction/analysis.py` 从宽泛“解析首次撞击与镜面反射轨道”压实为更明确的消费者链，写清它当前会先从最终 openPMD iteration 读取电子 `x/y/z`，再解析 `warpx_used_inputs` 里的球半径、初始位置与 proper velocity，显式求 ray-sphere 首次撞击时刻、球面法向镜面反射和 `ts.t[-1]-t_impact` 剩余传播，并最终要求末态 `x/z` 相对误差都小于 `2%` 且 `y<1e-8`；同时也把 `secondary_ion_emission/analysis.py` 从宽泛“最终 2 个电子贴近解析撞击点”压实为更明确的 openPMD + `warpx_used_inputs` 几何匹配合同，写清它先硬性要求末态次级电子数精确等于 `2`，再重建四个解析离子撞击点，把每个最终电子按所有候选撞击时刻逐一反向传播，并要求与最近解析撞击点的相对距离低于球半径的 `2%`。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `spacecraft_charging` PICMI input-level 条目：已把 `inputs_test_rz_spacecraft_charging_picmi.py` 从宽泛“导体球浸入热等离子体 + 在线改写导体势”压实为更明确的 callback/runtime 合同，写清它当前固定 `CylindricalGrid(40x80, m=1) + ElectrostaticSolver + Simulation(max_steps=1000)`，并用 `electrons/protons` 两套 `UniformDistribution + UniformFluxDistribution` 复合注入热等离子体；同时也把脚本内真正的 runtime 核心补清，即 `SpaceChargeFieldCorrector` 先保存真空归一化 `phi_fp/Efield_fp` multifab，再通过 `ParticleBoundaryBufferWrapper()` 跨 species 统计 `eb` scrape buffer 的真实收集电荷，在线修正 `phi_fp/Efield_fp` 并调用 `warpx.set_potential_on_eb(...)` 动态改写导体势，最后用 `ParticleBoundaryScrapingDiagnostic(period=-1)` 在末尾统一落盘 scraped-particle 数据。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `particle_boundary_interaction` / `secondary_ion_emission` RZ PICMI input-level 条目：已把 `inputs_test_rz_particle_boundary_interaction_picmi.py` 从宽泛“读取 scraped 粒子后镜面反射并重注入”压实为更明确的 callback runtime 合同，写清它当前固定 `CylindricalGrid(64x64, m=1) + ElectrostaticSolver + Simulation(max_steps=23)`，以单电子撞击球形 EB，并在 `callbacks.installafterstep(mirror_reflection)` 中读取 `deltaTimeScraped/r/theta/z/ux/uy/uz/w/nx/ny/nz`，做镜面反射后按剩余步长即时重注入；同时也把 `inputs_test_rz_secondary_ion_emission_picmi.py` 补成更明确的 callback runtime 合同，写清它以四个入射质子撞击球形 EB，在 `callbacks.installafterstep(secondary_emission)` 中读取 `ions` 的 scrape buffer，按 `sigma_nascap` 抽样次级电子数、对热速度做法向镜像，并按 `dt-delta_t` 的剩余步长即时重注入电子。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `particle_boundary_process` / `particle_boundary_scrape` PICMI input-level 条目：已把 `inputs_test_2d_particle_reflection_picmi.py` 从宽泛“打开 `warpx_reflection_model_zhi=\"0.5\"` 并检查 buffer”压实为更明确的 runtime/buffer 合同，写清它固定 `Cartesian2DGrid(64^2) + ElectrostaticSolver + Simulation(max_steps=10)`，并在运行后通过 `ParticleBoundaryBufferWrapper()` 断言 `z_hi/z_lo` buffer 粒子数精确等于 `63/67`、`stepScraped` 分别恒等于 `4/8`；同时也把 `inputs_test_3d_particle_scrape_picmi.py` 补成更明确的 3D cube-EB scrape wrapper 合同，写清它在 `sim.step(60)` 后显式检查 `eb` buffer size、`stepScraped > 40`、跨 rank `w` buffer 总数仍为 `612`，以及 `clear_buffer()` 后 size 归零。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `particle_data_python` PICMI input-level 条目：已把 `inputs_test_2d_particle_attr_access_picmi.py` 从宽泛“验证 `sim.particles.get/add_real_comp/add_particles/deposit_current`”压实为更明确的 runtime 合同，写清它当前实际固定 `Cartesian2DGrid(64^2) + ElectrostaticSolver + Simulation(max_steps=10)`，在 `initialize_warpx()` 后显式 `add_real_comp("newPid")`，安装 `callbacks.installbeforestep(add_particles)` 按 rank 注入粒子，并在运行中断言总粒子数、`w/newPid` real-comp 索引、tile 级 `newPid` 回读以及 `deposit_current("current_fp", ...)` 后 `x/z` 电流分量非零；同时也把 `inputs_test_2d_prev_positions_picmi.py` 补成更明确的 previous-position runtime-attribute 合同，写清它显式打开 `warpx_save_previous_position=True` 并在推进后逐 tile 断言 `prev_x/prev_z` 索引与 `prev_z` 回读值。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `gaussian_beam` PICMI input-level 条目：已把 `inputs_test_3d_gaussian_beam_picmi.py` 从宽泛“PICMI `GaussianBunchDistribution` 最小骨架”压实为更明确的 front-end/runtime 合同，写清它当前实际暴露 `--diagformat / --fields_to_plot` 两个 CLI 参数，固定 `Cartesian3DGrid(32^3) + ElectromagneticSolver(stencil_order=[3,3,3]) + Simulation(max_steps=10, warpx_current_deposition_algo="direct", warpx_use_filter=0)`，并用两套 `GaussianBunchDistribution` 组装带负 `velocity_divergence` 的 `electrons` 与无散焦的 `protons`，再分别以 `PseudoRandomLayout(n_macroparticles=32768)` 注入。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `uniform_plasma` 剩余 helper / restart 条目：已把 `analysis_default_regression.py` 从宽泛“通用 checksum helper”压实为更明确的本地 `evaluate_checksum(...)` 包装器说明；同时也把 `test_3d_uniform_plasma_restart` 单独补成明确的 restart runtime/consumer 合同，写清当前 `uniform_plasma/CMakeLists.txt` 把它注册成 `analysis_default_restart.py diags/diag1000010 + analysis_default_regression.py --path diags/diag1000010 --rtol 1e-12`，并且共享 `analysis_default_restart.py` 实际会对 restart 与非 restart run 的全部 grid/particle 字段做最终 plotfile 逐字段 reproducibility 对照。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `uniform_plasma` 相邻条目：已把 `inputs_base_3d` 从宽泛“3D 公共骨架”压实为更明确的 `64 x 32 x 32` 周期热电子盒 + `diag1` full plotfile + `chk` checkpoint producer 合同；同时也把 `inputs_test_2d_uniform_plasma`、`inputs_test_3d_uniform_plasma` 与 `inputs_test_3d_uniform_plasma_restart` 这些 input-level 行补成明确的 native/runtime/restart 合同，区分出独立 2D 输入卡、完整复用 `inputs_base_3d` 的 active 3D 主线入口，以及只额外挂 `amr.restart=../test_3d_uniform_plasma/diags/chk000006` 的 restart 输入卡。对应 `test_2d_uniform_plasma` 也已同步压实为外层 `analysis=OFF + analysis_default_regression.py --path diags/diag1000010` 的纯 checksum 路径。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `embedded_circle` 相邻条目：已把 `analysis_default_regression.py` 从宽泛“通用 checksum helper”压实为更明确的本地 `evaluate_checksum(...)` 包装器说明；同时也把 `inputs_test_2d_embedded_circle` 与 `test_2d_embedded_circle` 这些条目补成明确的 native/runtime/consumer 合同，区分出 `labframe electrostatic + circular EB + electrons/ar_ions self-field initialization + 双 background_mcc + save_particles_at_eb + BoundaryScraping + timer-based load balance` 这套原生多物理 workflow，以及外层 `analysis=OFF + analysis_default_regression.py --path diags/diag1000011 --rtol 1e-2` 这条 active checksum 路径。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `capacitive_discharge` 相邻条目：已把 `analysis_default_regression.py` 从宽泛“通用 checksum helper”压实为更明确的本地 `evaluate_checksum(...)` 包装器说明；同时也把 `inputs_test_2d_background_mcc`、`inputs_test_2d_background_mcc_picmi.py` 与 `test_2d_background_mcc` 这些条目补成明确的 native/PICMI/runtime/consumer 合同，区分出 native 2D pseudo-1D discharge scaffold、PICMI `PoissonSolverPseudo1D + callbacks.installpoissonsolver(...)` 外部 solver 路径，以及脚本尾部 `assert hasattr(solver, "phi")` 这层 callback-run 断言。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `laser_acceleration` 相邻 3D input-level 条目：已把 `inputs_base_3d` 从宽泛“3D LWFA 骨架”压实为更明确的 runtime/producer 合同，补清 `moving-window + openPMD Full diagnostics + FieldProbe reduced diagnostic + regionofinterest/initialenergy runtime attributes` 这套公共 scaffold；同时也把 `inputs_test_3d_laser_acceleration`、`inputs_test_3d_laser_acceleration_picmi.py`、`inputs_test_3d_laser_acceleration_python.py` 与 `inputs_test_3d_laser_acceleration_single_precision_comms` 这些 input-level 行补成明确的 native/PICMI/Python-extension/runtime-path 合同，并区分出 base 复用、`write_input_file(...)` materialization、`load_inputs_file(...) + afterstep callback` 可达性，以及 `warpx.do_single_precision_comms = 1` 这条通信路径分支。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `laser_acceleration` 相邻条目：已把 `inputs_base_1d / inputs_base_2d / inputs_base_rz` 这三条公共骨架从宽泛“moving-window skeleton”压实为更明确的 runtime/producer 合同，补清它们各自的 moving-window、particle attributes、Full/reduced diagnostics、refined patch 或 quasi-cylindrical 结构；同时也把 `inputs_test_1d_laser_acceleration_picmi.py`、`inputs_test_2d_laser_acceleration_boosted`、`inputs_test_2d_laser_acceleration_mr`、`inputs_test_2d_laser_acceleration_mr_picmi.py`、`inputs_test_rz_laser_acceleration` 这些 input-level 行补成明确的 native/PICMI materialization 路径。对应的 active baseline `test_1d_laser_acceleration`、`test_1d_laser_acceleration_picmi`、`test_2d_laser_acceleration_boosted`、`test_2d_laser_acceleration_mr`、`test_2d_laser_acceleration_mr_picmi` 与 `test_rz_laser_acceleration` 也已同步压实为外层 `analysis=OFF + analysis_default_regression.py --path ...` checksum 合同，并区分出独立 boosted 输入卡、BTD producer、native MR base 复用和 PICMI `write_input_file(...)` materialization 分支。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_1d_plasma_acceleration_picmi` 及其相邻脚本行：已把这条 active 1D baseline 从宽泛“1D PICMI wakefield skeleton 的前端与输出稳定性”压实为更明确的 PICMI front-end/checksum 合同，并写清当前 `plasma_acceleration/CMakeLists.txt` 明确把它注册成 `analysis=OFF + analysis_default_regression.py --path diags/diag1001000`，所以自动消费者确实只有最终 plotfile checksum。与此同时，也把 `inputs_test_1d_plasma_acceleration_picmi.py` 补清：它当前显式用 `Cartesian1DGrid + ElectromagneticSolver + Simulation`、beam/plasma `UniformDistribution`、`GriddedLayout([10])` 和末态 `FieldDiagnostic/ParticleDiagnostic` materialize 一个 1D moving-window PWFA PICMI front-end，并直接 `sim.step()` 跑到 `diag1001000`；脚本只保留了注释掉的 `sim.write_input_file(...)`，没有额外挂独立 analysis、自检 assert 或输入卡 materialization。也就是说，这条回归当前更准确地覆盖的是“1D non-boosted PWFA PICMI front-end 到最终 checksum 的最小落盘合同”，而不是独立 wakefield 物理解 benchmark。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_plasma_acceleration_picmi` 与 `test_3d_plasma_acceleration_mr_picmi` 及其相邻脚本行：已把这两条 active 3D baseline 从宽泛“PICMI 最小骨架 / refined-region 版”压实为更明确的 PICMI front-end/checksum 合同，并写清当前 `plasma_acceleration/CMakeLists.txt` 明确把它们都注册成 `analysis=OFF + analysis_default_regression.py --path diags/diag1000010` 和 `--path diags/diag1000002`，所以自动消费者都只有最终 plotfile checksum。与此同时，也把两条 input-level 脚本补清：普通 `inputs_test_3d_plasma_acceleration_picmi.py` 当前显式用 `Cartesian3DGrid + ElectromagneticSolver + Simulation`、beam/plasma `UniformDistribution`、`GriddedLayout([2,2,1])` 和末态 `FieldDiagnostic/ParticleDiagnostic` materialize 一个最小 3D PWFA PICMI front-end，并直接 `sim.step()` 跑到 `diag1000010`；WarpX 自带 `README.rst` 也已明确标注它目前还没有像原生 3D 例子那样启用 boosted frame。相对地，`inputs_test_3d_plasma_acceleration_mr_picmi.py` 则是在同一路径上额外通过 `grid.add_refined_region(level=1, ...)` materialize 一个 level-1 refined region，并以 `max_steps=2` 直接做 in-process PICMI 执行。也就是说，这两条回归当前更准确地覆盖的是“3D non-boosted PWFA PICMI front-end 的最小落盘合同，以及其额外 materialize 一个 refined region 后的前端/AMR 接线路径”，而不是独立 wakefield 物理解 benchmark。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_2d_plasma_acceleration_mr` 与 `test_2d_plasma_acceleration_mr_momentum_conserving` 及其相邻 `inputs_base_2d / inputs_test_*` 行：已把这两条 active 2D baseline 从宽泛“refined-patch PWFA 变体”压实为更明确的 native runtime/checksum 合同，并写清当前 `plasma_acceleration/CMakeLists.txt` 明确把它们都注册成 `analysis=OFF + analysis_default_regression.py --path diags/diag1000400`，所以自动消费者都只有最终 plotfile checksum。与此同时，也把 `inputs_base_2d` 和两条 input-level 行补清：公共 base 文件本身就是完整的 2D MR PWFA 主骨架，也就是 `CKC + pml + moving window + level-1 refined patch`、Gaussian `driver/beam`、常密度 `plasma_e` 与 `do_continuous_injection = 1`，再加 `diag1` Full plotfile producer；普通 `mr` 版本体其实只有 `FILE = inputs_base_2d`，而 `mr_momentum_conserving` 版也只是在此基础上额外切一处 `algo.field_gathering = momentum-conserving`。也就是说，这两条回归当前更准确地覆盖的是“2D native refined-patch PWFA 主骨架的 checksum smoke 路径，以及其只改一处 gather 开关后的 checksum smoke 路径”，而不是独立 wakefield 物理解 benchmark。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_2d_plasma_acceleration_boosted` 及其相邻 `inputs_test_2d_plasma_acceleration_boosted` 行：已把这条 active 2D baseline 从宽泛“2D boosted PWFA 变体”压实为更明确的 native runtime/checksum 合同，并写清当前 `plasma_acceleration/CMakeLists.txt` 明确将其注册成 `analysis=OFF + analysis_default_regression.py --path diags/diag1000020`，所以自动消费者确实只有最终 plotfile checksum。更关键的是，也把它和 `inputs_base_2d` 区分开了：当前这条输入并不是简单 base overlay，而是一张独立输入卡，自己内联了 `CKC + pml + moving window`、`warpx.gamma_boost = 10`、`particles.use_fdtd_nci_corr = 1`、rigid Gaussian `driver/beam`，以及 `plasma_e/plasma_p` 的余弦 density ramp 加 `do_continuous_injection = 1`。与此同时，`diag1.intervals = 500` 且 `max_step = 20`，所以这条 regression 当前真正被自动消费的仍只是最终 `diag1000020`。也就是说，这条回归当前更准确地覆盖的是“独立内联的 2D native boosted-frame PWFA scaffold 被压缩成 20-step smoke regression 后的应用级最终输出 checksum 路径”，而不是独立 wakefield 物理解 benchmark。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_plasma_acceleration_boosted_hybrid` 及其相邻 `inputs_test_3d_plasma_acceleration_boosted_hybrid` 行：已把这条 active 3D baseline 从宽泛“3D boosted + `grid_type=hybrid` 变体”压实为更明确的 native runtime/checksum 合同，并写清当前 `plasma_acceleration/CMakeLists.txt` 明确将其注册成 `analysis=OFF + analysis_default_regression.py --path diags/diag1000025`，所以自动消费者确实只有最终 plotfile checksum。与此同时，也把相邻 input-level 行补清：输入本体几乎只是 `FILE = inputs_base_3d` 加 `max_step = 25`、`warpx.do_current_centering = 0`、`warpx.grid_type = hybrid`，真正的 runtime scaffold 仍完整复用公共 `inputs_base_3d` 的 boosted PWFA 主骨架，也就是 `CKC + moving window + periodic/pml`、`warpx.gamma_boost = 10`、`particles.use_fdtd_nci_corr = 1`、rigid `driver/beam`、反向 `driverback`、以及 `plasma_e/plasma_p` 的余弦 density ramp 加 `do_continuous_injection = 1`。也就是说，这条回归当前更准确地覆盖的是“3D native boosted-frame PWFA 主骨架切到 hybrid-grid + no-current-centering 后的 25-step 应用级最终输出 checksum 路径”，而不是独立 wakefield 物理解 benchmark。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_plasma_acceleration_boosted` 及其相邻 `inputs_base_3d / inputs_test_3d_plasma_acceleration_boosted` 行：已把这条 active 3D baseline 从宽泛“`inputs_base_3d` 的短程 boosted 运行基准”压实为更明确的 native runtime/checksum 合同，并写清当前 `plasma_acceleration/CMakeLists.txt` 明确将其注册成 `analysis=OFF + analysis_default_regression.py --path diags/diag1000005`，所以自动消费者确实只有最终 plotfile checksum。与此同时，也把相邻 input-level 行补清：`inputs_test_3d_plasma_acceleration_boosted` 本体几乎只有 `FILE = inputs_base_3d` 加 `max_step = 5`，真正的 runtime scaffold 全在 `inputs_base_3d`，包括 `CKC + moving window + periodic/pml`、`warpx.gamma_boost = 10`、`particles.use_fdtd_nci_corr = 1`、rigid `driver/beam`、反向 `driverback`、以及 `plasma_e/plasma_p` 的余弦 density ramp 加 `do_continuous_injection = 1`。也就是说，这条回归当前更准确地覆盖的是“3D native boosted-frame PWFA 主骨架被压缩成 5-step smoke regression 后的最终输出 checksum 路径”，而不是独立 wakefield 物理解 benchmark。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `load_density` family 里剩余的 `test_1d_load_density` 以及对应 `analysis/input/prepare` 行：已把这条 active 1D baseline 从宽泛“checksum 基线；对应 1D density-from-file + moving-window 连续注入”压实为更明确的 `analysis_1d.py + checksum` 两阶段合同，并写清当前 `load_density/CMakeLists.txt` 还显式把它挂在 `test_1d_load_density_prepare` 后面，所以并不是 checksum-only。与此同时，也把 `analysis_1d.py`、`inputs_test_1d_load_density` 与 `inputs_test_1d_load_density_prepare.py` 一并补清：输入当前显式走 `profile=read_from_file + do_continuous_injection + moving window` 的 1D Cartesian 路径，而 `analysis_1d.py` 会遍历所有 openPMD iteration，对每一帧 `rho` 重建 `on_axis_density = 1e24`、`ramp_length = 60 um` 的 1D linear-ramp + plateau 解析密度，并在裁掉两端各 3 个单元后要求归一化误差始终 `< 0.02`；prepare 脚本则会先用 `openpmd_api` materialize 出 1D `example-density.h5`，写出 `z` 轴上的 linear-ramp + plateau density mesh。也就是说，这条回归当前更准确地覆盖的是“`prepare -> 1D profile=read_from_file + moving-window continuous injection -> 逐 iteration rho 解析闭合 + 附加 checksum`”链路。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `load_density` family 里 `test_2d_load_density` / `test_rz_load_density` 以及对应 `analysis/input/prepare` 行：已把这两条 active baseline 从宽泛“checksum 基线；对应 density-from-file 初始化”压实为更明确的 `analysis_2d.py + checksum` / `analysis_rz.py + checksum` 两阶段合同，并写清当前 `load_density/CMakeLists.txt` 还分别显式把它们挂在 `test_2d_load_density_prepare` 与 `test_rz_load_density_prepare` 后面，所以都不是 checksum-only。与此同时，也把 `analysis_2d.py`、`analysis_rz.py`、`inputs_test_2d_load_density`、`inputs_test_2d_load_density_prepare.py`、`inputs_test_rz_load_density` 与 `inputs_test_rz_load_density_prepare.py` 一并补清：2D 版当前走 Cartesian `profile=read_from_file + do_continuous_injection + moving window` 路径，由 `analysis_2d.py` 遍历所有 iteration，对每一帧 `rho` 重建 2D 抛物通道加 z 向 linear-ramp + plateau 解析密度，并在裁掉四边各 3 个单元后要求归一化误差始终 `< 0.02`；RZ 版则对应 theta-mode `r/z` density mesh，同样逐 iteration 做 `rho` 对解析密度闭合，但容差放宽到 `< 0.03`。两条 prepare 脚本也都已补清成：会先用 `openpmd_api` materialize 出各自的 `example-density.h5`，其中 2D 版写出 Cartesian `x/z` mesh，RZ 版写出 `(num_nodes=1, nr, nz)` 的 theta-mode `r/z` mesh。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_load_density` 及其相邻 `analysis/input/prepare` 行：已把这条 active 3D baseline 从误导性的“checksum 基线；对应 3D density-from-file 抛物通道初始化”压实为更明确的 `analysis_3d.py + analysis_default_regression.py --path diags/diag/` 两阶段合同，并写清当前 `load_density/CMakeLists.txt` 还显式把它挂在 `test_3d_load_density_prepare` 后面，所以并不是 checksum-only。与此同时，也把 `analysis_3d.py`、`inputs_test_3d_load_density`、`inputs_test_3d_load_density_prepare.py` 和 `analysis_default_regression.py` 一并补清：prepare 脚本会先用 `openpmd_api` materialize 出带 `on_axis_density = 1e24`、`channel_radius = 40 um`、`ramp_length = 60 um` 的 3D 抛物通道加 z 向 linear-ramp + plateau 的 `example-density.h5`；active 输入再把该文件挂到 `electrons.read_density_from_path`，同时打开 moving window 与 `do_continuous_injection = 1`；而 `analysis_3d.py` 当前真正消费的是 openPMD `diags/diag` 的所有 iteration，对每一帧 `rho` 都重建解析密度并在裁掉六面边缘各 3 个单元后要求归一化误差始终 `< 0.02`。也就是说，这条回归当前更准确地覆盖的是“`prepare -> moving-window continuous file-driven injection -> 逐 iteration `rho` 解析闭合 + 附加 checksum`”链路。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_open_bc_poisson_solver` / `test_3d_open_bc_poisson_solver_sliced`：已把这两条 active 3D regression 从宽泛“open boundary relativistic FFT Poisson 初始化”摘要压实为更明确的 `analysis.py + checksum` 合同，并写清当前它们都只在 `WarpX_FFT` 打开时注册成 `analysis.py + analysis_default_regression.py --path diags/diag1000001 --rtol 1e-2`，所以并不是 checksum-only；与此同时，也把 `analysis.py` 与对应 input-level 行补清：普通基线显式以 `warpx.do_electrostatic = relativistic + warpx.poisson_solver = fft` 在全 open 边界 `128^3` 盒中初始化非圆高斯 relativistic electron bunch，并额外挂出 `diag2` openPMD `Ex/Ey`，随后由 `analysis.py` 逐 `z` 切片把 `Ex/Ey` 与 Basseti-Erskine 解析场做 `np.allclose` 对照；而 sliced 版则只是在完全复用同一套束团、自场初始化和 diagnostics 面的基础上额外打开 `warpx.use_2d_slices_fft_solver = 1`，真正新增的是求解器改走 `2D-slices FFT` 路径。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_nodal_electrostatic_solver`：已把这条 active 3D baseline 从宽泛“collocated relativistic electrostatic 零触发基准”压实为更明确的 `analysis.py + checksum` 合同，并写清当前 `nodal_electrostatic/CMakeLists.txt` 明确将其注册成 `analysis.py + analysis_default_regression.py --path diags/diag1000010` 且显式标成 `slow`，所以并不是 checksum-only；与此同时，输入 `inputs_test_3d_nodal_electrostatic_solver` 也已补清其显式固定 `warpx.do_electrostatic = relativistic`、`warpx.grid_type = collocated`、`algo.particle_pusher = vay`、`algo.particle_shape = 3`，在 `128^3` 周期盒中注入自场初始化的高斯 positron 束，并把 `qed_qs.chi_min = 1e-3`、`photon_creation_energy_threshold = 1.0` 与 `warpx.do_qed_schwinger = 0` 固定下来。更关键的是，`analysis.py` 当前真正消费的是 reduced diagnostics：要求 `ParticleExtrema_beam_p.txt` 中所有时间步的 `chi_max < 2e-8`，并且 `ParticleNumber.txt` 里的 photon 计数始终为 `0`。也就是说，这条回归当前更准确地覆盖的是“3D collocated relativistic electrostatic + Vay pusher + self-field-initialized Gaussian positron bunch 的 QED 零触发合同，加末态 plotfile checksum”。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `load_external_field` 段里 checksum helper 与 RZ baseline/input 合同：`analysis_default_regression.py` 已补清它只是本目录通用 checksum 包装器，会按当前目录推导 test name、自动探测 `plotfile/openpmd`，并按普通基线或 restart 选择默认 `rtol=1e-9/1e-12`，本身并不额外消费磁镜反射轨道或时变外场缩放。与此同时，也把 `test_rz_load_external_field_grid` 与 `test_rz_load_external_field_particles` 从宽泛“RZ grid/particle external field”摘要压实为更明确的 `analysis_rz.py + checksum` 双消费者链，并写清它们当前都会先由 `analysis_rz.py` 读取最终 plotfile 中 proton 的 `r/z` 末态位置，与硬编码参考点 `(0.12402005, 4.3632492)` 比较，要求最小欧氏误差 `< 1e-8`；而对应 input-level 行则分别补清成 grid-side `warpx.B_ext_grid_init_style = read_from_file` 和 particle-side `particles.B_ext_particle_init_style = read_from_file` 两条 RZ theta-mode 磁镜场装填路径。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `load_external_field` 段里 `grid_picmi` / `particle_picmi` 两条 active baseline：已把它们从宽泛“openPMD 装填”摘要压实为更明确的 `analysis_3d.py + checksum` 双消费者链，并写清当前两条路径都会先由 `analysis_3d.py` 读取最终 plotfile 中 proton 的末态位置，与硬编码参考点 `(0.12238072, 0.00965395, 4.31754477)` 比较，要求最小欧氏误差 `< 1e-8`；与此同时，也把对应 input-level 行补清：`inputs_test_3d_load_external_field_grid_picmi.py` 通过 `LoadInitialField(..., load_E=False, warpx_do_initial_div_cleaning=False)` 把 openPMD 磁镜场静态装进网格寄存器，而 `inputs_test_3d_load_external_field_particle_picmi.py` 则通过 `LoadAppliedField(..., load_E=False)` 让单粒子沿 `B_external_particle_field` 路径消费同一份磁镜场。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `load_external_field` 段里 `particle_multi_time` 相邻条目：已把 `test_3d_load_external_field_particle_multi_time` 与 `test_3d_load_external_field_particle_multi_time_picmi` 从误导性的“checksum 基线”摘要压实为更准确的 `analysis_time_scaling.py + checksum` 双消费者链，并写清它们当前都先直接读取 `diags/diag1000000` 与 `diags/diag1000300`，要求同一 `Bz` 分量在非零初值单元上的净缩放比命中 `expected_ratio = 0.0`；与此同时，也把 `inputs_test_3d_load_external_field_particle_multi_time` 与 `inputs_test_3d_load_external_field_particle_multi_time_picmi.py` 的 runtime 合同补清：native 版通过 `particles.B_ext_particle_fields = b1 b2` 把同一 openPMD 外磁场文件拆成 `cos(omega t)` 与 `cos(2 omega t)` 两路 dependency map，PICMI 版则并排组装两条 `LoadAppliedField(..., warpx_B_time_function=...)`，并且 `omega` 都被专门选成在 `300` 步末态让两路系数变成 `+0.5/-0.5`，从而把总 `Bz` 相消到 `0`。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `load_external_field` 段里 `particle_time` 相邻条目：已把 `test_3d_load_external_field_particle_time` 与 `test_3d_load_external_field_particle_time_picmi` 从误导性的“checksum 基线”摘要压实为更准确的 `analysis_time_scaling.py + checksum` 双消费者链，并写清它们当前都先直接读取 `diags/diag1000000` 与 `diags/diag1000300`，在 `|B0| > 1e-12` 的单元上比较 `Bz` 的 `BN/B0` 缩放比，要求 median 命中 `expected_ratio = 0.5`、mean 也在放宽容差内闭合；与此同时，也把 `analysis_time_scaling.py`、`inputs_test_3d_load_external_field_particle_time` 与 `inputs_test_3d_load_external_field_particle_time_picmi.py` 的 input/analysis 合同补清：native 版通过 `particles.read_fields_B_dependency(t) = cos(omega t + phase_B)` 给从 openPMD 文件读入的粒子外磁场挂上时间依赖，PICMI 版则通过 `LoadAppliedField(..., warpx_B_time_function=\"cos(omega*t + phase)\")` 做同一件事，并且 `omega` 都被专门选成在 `300` 步末态把缩放因子落到 `0.5`。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `magnetostatic_eb` 段剩余 still-coarse 行：`analysis_default_regression.py` 已补清它当前只是 family 级通用 checksum 包装器，会按当前目录推导 test name、自动探测 `plotfile/openpmd`，并按普通基线或 restart 选择默认 `rtol=1e-9/1e-12`，本身并不额外消费 `Efield_aux/Bfield_aux` 或增加 magnetostatic 物理断言。`inputs_test_rz_magnetostatic_eb_picmi.py` 则已补清它显式组装 `CylindricalGrid([128,128])`、`ElectrostaticSolver(..., warpx_magnetostatic=True)`、圆柱 `EmbeddedBoundary(radius=0.2)` 与 `Simulation(warpx_field_gathering_algo="momentum-conserving", warpx_current_deposition_algo="direct")`，并在 `sim.step(1)` 后直接读取 `Efield_aux(r)` 与 `Bfield_aux(theta)`，沿 `z` 平均后分别对解析 `Er(r)` / `B_theta(r)` 施加 `< 2%` 的双断言，同时落出 `er_rz.png` 与 `bth_rz.png`。也就是说，这一段 helper/input-level map 现在已经和现有 native/PICMI baseline 的 runtime/consumer 分叉基本收平。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `magnetostatic_eb` 邻近 input-level 行，并把它们和刚完成的 baseline-level contract 拉平：`inputs_test_3d_magnetostatic_eb` 已补清它并不是泛泛“原生输入”，而是显式固定 `64^3`、`max_step = 1`、`neumann/neumann/pec` 场边界、`boundary.potential_lo_z = 0.0`、`warpx.do_electrostatic = labframe-electromagnetostatic`、圆柱 EB beampipe、`warpx.self_fields_required_precision = 1.e-7`，同时把 solver-side 组合切成 `algo.field_gathering = momentum-conserving`、`algo.current_deposition = direct`、`algo.particle_shape = 1`，并让单一 `beam` species 通过 `parse_density_function` 打开 `initialize_self_fields = 1`；这条路径在 `magnetostatic_eb/CMakeLists.txt` 中当前仍只会落成 `analysis=OFF + analysis_default_regression.py --path diags/diag1000001` 的单帧 checksum 消费链。`inputs_test_3d_magnetostatic_eb_picmi.py` 则已补清它虽然外层同样挂在 checksum 上，但脚本本体已经显式组装 `ElectrostaticSolver(..., warpx_magnetostatic=True)`、圆柱 `EmbeddedBoundary` 与 `Simulation(warpx_field_gathering_algo="momentum-conserving", warpx_current_deposition_algo="direct")`，并在 `sim.step(1)` 后直接读取 `Efield_aux/Bfield_aux`，分别对子区域平均后的解析 `Er/B_theta` 施加 `< 5%` 的双断言，同时落出 `er_3d.png` 与 `bt_3d.png`。也就是说，这一段 input-level map 现在已经和相应 native/PICMI baseline 的 runtime/consumer 分叉收平。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_magnetostatic_eb_picmi`：已把这条 3D PICMI magnetostatic-EB baseline 从宽泛“对应 3D PICMI magnetostatic EB 初始化”压实为更准确的双层 consumer 合同，并写清当前 `magnetostatic_eb/CMakeLists.txt` 外层虽然仍把它注册成 `analysis=OFF + analysis_default_regression.py --path diags/diag1000001`，但 `inputs_test_3d_magnetostatic_eb_picmi.py` 本体并不是 checksum-only scaffold，而是会显式组装 `ElectrostaticSolver(method="Multigrid", required_precision=1e-7, warpx_magnetostatic=True)`、圆柱 `EmbeddedBoundary` 与 `Simulation(warpx_field_gathering_algo="momentum-conserving", warpx_current_deposition_algo="direct")`，并通过 `sim.add_species(... initialize_self_field=True)` 在 beampipe 中触发 PICMI 自场初始化。更关键的是，脚本在 `sim.step(1)` 后会直接读取 `sim.fields.get("Efield_aux", dir="x/y")` 与 `sim.fields.get("Bfield_aux", dir="x/y")`：前者在 `z in [0.5, 0.9] * zmax` 上平均后重建解析 `Er` 并要求 `er_err < 0.05`，后者在 `z in [0.25, 0.75] * zmax` 上平均并插值回 nodal 点后重建解析 `B_theta` 并要求 `bt_err < 0.05`；同时脚本还会输出 `er_3d.png` 与 `bt_3d.png`。因此这条 active baseline 当前更准确地应视为“3D PICMI `warpx_magnetostatic=True` beampipe 自场初始化的 in-process `Efield_aux/Bfield_aux` 解析场双断言，加最终 `diag1000001` checksum 附加基线”，而不是纯 checksum 或泛泛初始化摘要。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_magnetostatic_eb`：已把这条 native 3D magnetostatic-EB baseline 从宽泛“原生 `labframe-electromagnetostatic` + EB 初始化”压实为更准确的 native/PICMI 分叉合同，并写清当前 `magnetostatic_eb/CMakeLists.txt` 在 `WarpX_EB` 打开时明确把它注册成 `analysis=OFF + analysis_default_regression.py --path diags/diag1000001`，所以自动消费者只有最终 plotfile checksum；而 `inputs_test_3d_magnetostatic_eb` 运行时显式固定 `warpx.do_electrostatic = labframe-electromagnetostatic`、`64^3` 单层网格、`neumann/neumann/pec` 边界、圆柱 beampipe `warpx.eb_implicit_function = "(x**2+y**2-radius**2)"`、固定 `warpx.eb_potential(...)=1.`、`warpx.self_fields_required_precision = 1.e-7`，并让 `beam.initialize_self_fields = 1` 的 relativistic 电子束在 `r<rmax` 区域上触发 electrostatic + magnetostatic 自场初始化；诊断侧则只在第 `1` 步输出一次 `Az Bx By Ex Ey jz phi rho`。更关键的是，这个 family 里真正带解析场消费者链的并不是 native 版，而是相邻 PICMI 变体在脚本内部直接读取 `Efield_aux/Bfield_aux` 去和解析 `Er/Btheta` 比较。因此这条 native 基线当前更准确地应视为“3D `labframe-electromagnetostatic` + EB + self-field initialization runtime scaffold，加单帧 `diag1000001` checksum 消费链”，而不是已有独立解析场断言的强 magnetostatic benchmark。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `laser_injection_from_file` 邻近 input-level 行：已把 `inputs_test_3d_laser_injection_from_lasy_file` 从宽泛“3D lasy 注入基准”压实为更准确的 `profile=from_file` runtime 合同，并写清它在 `32 x 32 x 1024` 周期盒中显式打开 `algo.maxwell_solver = ckc`、`warpx.cfl = 0.98`、`algo.load_balance_intervals = -1`、`algo.particle_shape = 3`，把 `lasy_laser.profile = from_file` 指向 prepare 阶段生成的 `gaussian_laser_3d_00000.h5`，同时固定 `lasy_laser.time_chunk_size = 50` 与末态 `diag1` 字段面；与此同时，也把 `inputs_test_3d_laser_injection_from_lasy_file_prepare.py` 压实为真正用 `lasy.Laser + GaussianProfile` materialize 这份 HDF5 文件的 prepare 脚本。也就是说，这两条 input-level 行现在已经和对应 baseline-level contract 对齐成完整的 `prepare -> inject -> analysis_3d.py` 链。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_laser_injection_from_lasy_file`：已把这条 3D lasy 注入 baseline 从宽泛“analysis 对 envelope 和主频做断言”压实为更准确的 prepare/runtime/consumer 合同，并写清当前 `laser_injection_from_file/CMakeLists.txt` 并不是单独直接跑 3D lasy 注入，而是先依赖 `test_3d_laser_injection_from_lasy_file_prepare` 生成 lasy 文件，再把 active regression 绑定成 `analysis_3d.py diags/diag1000251 + analysis_default_regression.py --path diags/diag1000251`。其中 prepare 脚本会先用 `lasy.Laser + GaussianProfile` 实际生成 `gaussian_laser_3d_00000.h5`；主输入则在 `32 x 32 x 1024` 周期盒中打开 `algo.maxwell_solver = ckc`、`warpx.cfl = 0.98`、`algo.load_balance_intervals = -1`，并把 `lasy_laser.profile = from_file` 指向这份外部文件，同时显式固定 `lasy_laser.time_chunk_size = 50` 和末态 `diag1` full plotfile 字段面。更关键的是，`analysis_3d.py` 会先对 3D `Ey` 做 Hilbert envelope，与解析双脉冲高斯 envelope 比较并要求相对误差 `< 0.065`；随后再对完整 3D `Ey` 做 `np.fft.fftn`，重建主频模长并要求相对理论频率 `c/wavelength` 的误差也 `< 0.065`。因此它当前更准确地应视为“3D lasy-file laser materialization + `profile=from_file` 注入 runtime 路径 + `Ey` 3D Hilbert envelope 误差与 3D FFT 主频误差双消费者链”，而不是笼统的 lasy 注入摘要。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_laser_injection`：已把这条 3D laser-injection baseline 从宽泛“Gaussian 天线注入，analysis 只有占位图”压实为更准确的 active/inactive analysis 边界，并写清当前 `laser_injection/CMakeLists.txt` 并不是把它注册成 `analysis=OFF`，而是显式绑定了 `analysis_3d.py + analysis_default_regression.py --path diags/diag1000020`；但 `analysis_3d.py` 实际只是生成 `laser_analysis.png` 的占位正弦图，并不读取 `diags/diag1000020` 或任何激光输出，因此 physics 上真正起作用的仍主要是 checksum 链。与此同时，输入 `inputs_test_3d_laser_injection` 运行时显式固定 `max_step = 20`、`32 x 32 x 240` 网格、横向周期 + 纵向 PEC 边界、`algo.particle_shape = 1`、`warpx.use_filter = 0`、`warpx.do_moving_window = 1`，并通过 native `laser1.profile = Gaussian` 天线注入激光；诊断侧只在最后一步输出一次 `diag1` full plotfile，字段面为 `jx jy jz Ex Ey Ez Bx Bz`。因此它当前更准确地应视为“3D Gaussian laser-antenna 注入 runtime scaffold + 末态 `diag1000020` checksum 消费链，同时挂着一个未真正消费仿真输出的占位 analysis 脚本”，而不是已有独立强 analysis 的 3D 注入 benchmark。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_laser_acceleration_python`：已把这条 3D Python callback baseline 从宽泛“afterstep callback 能访问粒子容器与场 `MultiFab`”压实为更准确的 Python-wrapper runtime/consumer 合同，并写清当前 `laser_acceleration/CMakeLists.txt` 明确将其注册成 `analysis=OFF + analysis_default_regression.py --path diags/diag1/`，同时运行前还会把 `inputs_test_3d_laser_acceleration` 与 `inputs_base_3d` 一起复制进 run dir，所以自动消费者仍只有最终 `diags/diag1/` 的 openPMD checksum；而脚本本身会先通过 `sim.load_inputs_file("./inputs_test_3d_laser_acceleration")` 直接接管 native 3D LWFA 输入卡，因此 moving-window、连续注入 plasma、自定义粒子属性、Gaussian 激光注入、`diag1` openPMD Full diagnostics 与 `FP` reduced diagnostic 这些 runtime 面都仍来自公共 `inputs_base_3d`。在此基础上，脚本再注册两条 `@callfromafterstep` callback：一条显式访问 `sim.particles.get("electrons")` 与 `sim.fields.get("Efield_fp", dir="x", level=0)`，另一条进一步下潜到 `sim.extension.amr` 的 pyAMReX 层读取 `ParallelDescriptor.NProcs()` 并再次访问粒子容器与场 wrapper。因此它当前更准确地应视为“native 3D LWFA 输入卡经 `sim.load_inputs_file(...)` 载入后的 Python-extension runtime，加双 `afterstep` callback 对 particle container / field wrapper / pyAMReX extension 的可达性路径，再由 `diags/diag1/` checksum 消费”，而不是独立 physics analysis。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_laser_acceleration`：已把这条 3D native LWFA baseline 从宽泛“moving-window skeleton、continuous injection、openPMD Full diagnostics 与自定义粒子属性输出”压实为更准确的 producer/checksum 合同，并写清当前 `laser_acceleration/CMakeLists.txt` 明确将其注册成 `analysis=OFF + analysis_default_regression.py --path diags/diag1/`，所以自动消费者只有最终 `diags/diag1/` 的 openPMD checksum；而 `inputs_test_3d_laser_acceleration` 本身只是 `FILE = inputs_base_3d`，真正的 runtime 合同都在公共 base 上，包括 3D moving window、`electrons.do_continuous_injection = 1`、`regionofinterest` / `initialenergy` 两个自定义粒子属性、Gaussian 激光注入、`diag1` openPMD Full diagnostics，以及 `FP` moving-window line probe reduced diagnostic。也就是说，它当前更准确地应视为“3D native LWFA scaffold + `diag1` openPMD Full diagnostics 与 `FP` line-probe reduced-diag producer 面，再由 `diags/diag1/` checksum 消费”的 producer 合同，而不是笼统 skeleton 摘要。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_ohm_solver_cylinder_compression_picmi`：已把这条 3D hybrid-PIC cylinder-compression baseline 从宽泛“file/function 双路径 + `analysis=OFF`”压实为更准确的 runtime/checksum 合同，并写清当前 `ohm_solver_cylinder_compression/CMakeLists.txt` 明确将其注册成 `"inputs_test_3d_ohm_solver_cylinder_compression_picmi.py --test"`，并绑定 `analysis=OFF + analysis_default_regression.py --path diags/diag1000010 --rtol 5e-4`，同时还显式标成 `slow`，所以自动消费者只有低分辨率 CI 模式下最终 plotfile 的放宽容差 checksum；而脚本本身会先在 rank 0 用 `openpmd_api` 实际生成 `Afield.h5`，把均匀压缩对应的 `A_x/A_y/A_z` mesh 写成 openPMD 文件，再并排给出 `uniform_analytical` 的 `Ax/Ay/Az_external_function`，并让两条分支共同复用同一个 `A_time_external_function(t)` ramp；运行时还会显式组装 `HybridPICSolver(..., A_external=A_ext, substeps=60)`、圆柱 `EmbeddedBoundary(...)`，并通过 `LoadInitialFieldFromPython(load_B=True)` 回调把解析 `B_z(r)` 初始场装进 `Bfield_fp_external`。更关键的是，active CMake 路径总是带 `--test`，所以脚本会把分辨率和粒子数缩到 `32 x 32 x 16`、`NPPC=5`、`10` 步，并切到一次性 `plotfile` diagnostics；非测试长跑分支才会改用 `field_diags` openPMD 输出。因此它当前更准确地应视为“3D hybrid-PIC cylinder-compression 的 file-backed + analytical `A_external` 配置路径、Python 初始外磁场加载、`--test` 低分辨率 plotfile diagnostics 分支，以及 `diags/diag1000010 --rtol 5e-4` checksum 消费链”，而不是独立参数级强断言。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_laser_acceleration_single_precision_comms`：已把这条 3D 单精度通信 baseline 从宽泛“通信变体，不提供独立 wakefield 物理断言”压实为更准确的 communication/runtime 合同，并写清当前 `laser_acceleration/CMakeLists.txt` 明确将其注册成 `analysis=OFF + analysis_default_regression.py --path diags/diag1/`，所以自动消费者仍只有最终 openPMD checksum；而 `inputs_test_3d_laser_acceleration_single_precision_comms` 本身实际上只是 `FILE = inputs_base_3d` 再额外加上一行 `warpx.do_single_precision_comms = 1`，因此它并没有换掉 native 3D LWFA 的 moving-window、连续注入 plasma、自定义粒子属性、Gaussian 激光注入、`diag1` openPMD Full diagnostics 和 `FP` line probe reduced diagnostic 这些 runtime 面。也就是说，它当前更准确地应视为“3D native LWFA scaffold + `warpx.do_single_precision_comms = 1` 的通信/runtime path + `diags/diag1/` checksum 消费链”，而不是笼统的单精度通信摘要。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_laser_acceleration_picmi`：已把这条 3D PICMI LWFA baseline 从宽泛“front-end 映射 + checksum”压实为更准确的 materialization/runtime 合同，并写清当前 `laser_acceleration/CMakeLists.txt` 明确将其注册成 `analysis=OFF + analysis_default_regression.py --path diags/diag1000100`，所以自动消费者仍只有最终 openPMD checksum；但 `inputs_test_3d_laser_acceleration_picmi.py` 本身已经显式用 `picmi.Cartesian3DGrid + ElectromagneticSolver + Simulation` materialize 出与 native `inputs_base_3d` 对齐的 3D moving-window LWFA scaffold，包括背景电子连续注入、自定义粒子属性、Gaussian 束团、`GaussianLaser + LaserAntenna` 注入，以及 `ParticleDiagnostic + FieldDiagnostic` 这组 PICMI diagnostics；同时脚本还会先 `sim.write_input_file("inputs_3d_picmi")` 生成独立输入卡，再在同一个 Python front-end 中 `initialize_inputs() / initialize_warpx() / step(max_steps)` 直接推进 `100` 步。因此它当前更准确地应视为“3D PICMI LWFA front-end mapping + 输入卡 materialization + in-process PICMI execution + `diag1000100` checksum 消费链”，而不是可替代 native physics analysis 的强 benchmark。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_uniform_plasma`：已把这条 3D uniform-plasma baseline 从宽泛“full diagnostics 与 checkpoint 输出基线”压实为更准确的 producer/consumer 合同，并写清当前 `uniform_plasma/CMakeLists.txt` 虽然仍将其注册成 `analysis=OFF + analysis_default_regression.py --path diags/diag1000010` 的 checksum-only 主链，但运行时实际复用 `inputs_base_3d`，在 3D 周期盒中注入单 species 热电子，同时产出 `diag1` full plotfile 与 `chk` checkpoint diagnostics；更关键的是，相邻 `test_3d_uniform_plasma_restart` 还把它声明成 dependency，并从 `../test_3d_uniform_plasma/diags/chk000006` 恢复后，通过 `analysis_default_restart.py` 逐字段比较 restart 与原始 run 的所有 grid/particle 输出。因此它当前更准确地应视为“3D 周期热等离子体 full-diagnostics + checkpoint checksum baseline，同时也是 restart regression 的 checkpoint producer”，而不是孤立 plotfile checksum 摘要。
- [x] 2026-05-25：继续清理 Langmuir 邻近段的 `RCYLINDER` / `RSPHERE` input-level 两行，并把它们和已完成 baseline-level contract 拉平：`inputs_test_rcylinder_langmuir_multi` 与 `inputs_test_rsphere_langmuir_multi` 已补清它们都不是 base-overlay，而是各自完整的径向几何输入卡，显式固定 `geometry.dims = RCYLINDER/RSPHERE`、`algo.current_deposition = esirkepov`、`warpx.do_dive_cleaning = 1`，并分别给出纯径向或球对称高斯动量扰动；同时也写明它们虽然诊断字段不完全相同，`analysis_r1d.py` 当前实际只消费最终 plotfile 的 `Er` 径向场并要求 `error_rel < 0.12`，并没有额外的守恒或粒子诊断消费者链。
- [x] 2026-05-25：继续清理相邻 3D Langmuir `psatd_nodal` / `vay_deposition` input-level 行，并把它们和已完成 baseline-level contract 拉平：`inputs_test_3d_langmuir_multi_psatd_nodal` 已补清它其实是 `direct + PSATD + collocated` 的 3D nodal-grid 分支，只是继续复用 `inputs_base_3d` 那套 selective particle / openPMD diagnostics 面，因此会保留 `analysis_3d.py` 主合同，但不再触发 `analysis_utils.py` 的守恒 gate；`inputs_test_3d_langmuir_multi_psatd_vay_deposition` 与 `inputs_test_3d_langmuir_multi_psatd_vay_deposition_nodal` 则已补清它们当前都只在 `WarpX_FFT` 打开时、并以单 rank 方式注册，运行时分别对应 `Vay current deposition + PSATD` 与 `Vay current deposition + PSATD + collocated` 两条 `1e-3` 守恒分支，其中 nodal 版还被 `CMakeLists.txt` 显式标成 `slow`。
- [x] 2026-05-25：继续清理相邻 3D Langmuir base / nodal input-level 行，并把它们和已完成 baseline-level contract 拉平：`inputs_test_3d_langmuir_multi` 已补清它本身只是 `FILE = inputs_base_3d`，真正的 runtime 合同都在公共 base 上，包括 `algo.current_deposition = esirkepov`、`diag1.fields_to_plot = Ex Ey Ez Bx By Bz jx jy jz part_per_cell rho divE`、不对称的电子/正电子 selective particle output，以及 `openpmd.electrons.additional_variables = Ex Ey Ez` 这条 on-particle-field diagnostics 面；同时也写明 `analysis_3d.py` 会先验证 selective particle output，再比较解析 `Ex/Ey/Ez`，再对 openPMD 粒子上场采样做解析回代，并通过 `analysis_utils.py` 施加默认 `1e-11` 的守恒 gate。`inputs_test_3d_langmuir_multi_nodal` 则补清了它只是在同一套 base diagnostics 面之上额外切到 `algo.current_deposition = direct + warpx.grid_type = collocated`，因此会保留主合同，但不再触发守恒 gate。
- [x] 2026-05-25：继续清理 Langmuir 邻近段的 1D 与 RZ input-level 行，并把它们和已完成 baseline-level contract 拉平：`inputs_test_1d_langmuir_multi` 已补清它其实是完整 1D 输入卡而不是 base-overlay，显式固定 `algo.current_deposition = esirkepov`、`diag1.fields_to_plot = ... rho divE`、电子/正电子 selective particle output 与 `openpmd` full diagnostic，并写明 `analysis_1d.py` 会先比较解析 `Ez`、再通过 `analysis_utils.py` 施加默认 `1e-11` 守恒 gate；RZ 这一串则已把 `inputs_base_rz` 自带的 `diag_parser_filter` / `diag_uniform_filter` / `diag_random_filter` 三套 particle-filter diagnostics 纳入合同，写清 native `analysis_rz.py` 不只是比较解析 `Er/Ez`，还会在最后一步继续验证三种 filter diagnostics；同时又把 `rz_psatd`、`rz_psatd_current_correction` 因未输出 `ux` 而命中的 `skip_component = "particle_momentum_x"` 分支，以及 `rz_picmi` 其实自带 in-process 多模 `Efield_aux` 解析场对照、并不只是 `analysis=OFF + checksum` 骨架这一点补实了。
- [x] 2026-05-25：继续清理 2D Langmuir input-level 邻近段里仍偏粗的 base / nodal / MR 几项，并把它们和已完成 baseline-level contract 拉平：`inputs_test_2d_langmuir_multi` 已补清 `algo.current_deposition = direct` 与电子/正电子 `x z w ux uy uz` selective particle output，并写明它只复用 `analysis_2d.py` 的解析 `Ex/Ez` 场合同；`inputs_test_2d_langmuir_multi_nodal` 已补清额外的 `warpx.grid_type = collocated`，也就是 `direct + collocated` 的 2D nodal-grid 分支；`inputs_test_2d_langmuir_multi_mr*` 这一串则已补清 `algo.maxwell_solver = ckc`、`amr.max_level/ref_ratio/ref_ratio_vect`、`warpx.fine_tag_lo/hi`、`warpx.use_filter = 1` 这些 refinement 合同，并把 `mr_psatd` 单独写成 `WarpX_FFT` 打开时才存在的 `PSATD + MR` 分支。同时，这轮也把“哪些 MR/FDTD 路径仍会通过默认 `esirkepov` 触发 `analysis_utils.py` 的 `1e-11` 守恒 gate、哪些 `direct` / `PSATD` 路径不会触发”这条边界写实了。
- [x] 2026-05-25：继续清理 2D Langmuir input-level 邻近段里仍偏粗的一组 `psatd / JRhom_LL2 / current_correction / momentum_conserving / nodal / vay_deposition / particle_shape_4` 行，并把它们和已完成 baseline-level contract 拉平：`inputs_test_2d_langmuir_multi_psatd` 已补清 `algo.maxwell_solver = psatd`、粒子变量输出、`diag1.fields_to_plot = Ex Ey Ez jx jy jz part_per_cell`、`psatd.current_correction = 0` 与 `warpx.cfl = 0.7071067811865475` 这组 `FFT-backed spectral solver` 分支，并写明不会触发 native `esirkepov and not psatd` 基线那条守恒 gate；`inputs_test_2d_langmuir_multi_psatd_JRhom_LL2` 已补清 `psatd.JRhom = "LL2"`、`psatd.solution_type = first-order`、`psatd.update_with_rho = 1` 这组 2D `J/rho` 时间依赖分支；`inputs_test_2d_langmuir_multi_psatd_current_correction` 已补清 `algo.current_deposition = esirkepov`、`psatd.current_correction = 1`、`psatd.periodic_single_box_fft = 1` 和 `divE` 诊断面；`inputs_test_2d_langmuir_multi_psatd_momentum_conserving` 与 `inputs_test_2d_langmuir_multi_psatd_nodal` 已分别补清 `momentum-conserving gather + PSATD`、`direct + PSATD + collocated` 这两条不会触发守恒 gate 的分支；`inputs_test_2d_langmuir_multi_psatd_vay_deposition*` 这一串也已补清 `algo.current_deposition = vay`、`divE` 诊断、nodal `collocated` 变体和 `particle_shape = 4` 触发 `analysis_2d.py` 把场误差容差放宽到 `0.07` 的特殊消费者边界。
- [x] 2026-05-25：继续清理 3D Langmuir input-level 邻近段里仍偏粗的 `psatd` / `div_cleaning` / `momentum_conserving` 三行，并把它们和已完成 baseline-level contract 拉平：`inputs_test_3d_langmuir_multi_psatd` 已补清 `algo.maxwell_solver = psatd`、`warpx.cfl = 0.5773502691896258` 这组 `FFT-backed spectral solver` 分支，并写明不会触发 native `esirkepov and not psatd` 基线那条守恒 gate；`inputs_test_3d_langmuir_multi_psatd_div_cleaning` 已补清 `algo.current_deposition = direct`、`psatd.update_with_rho = 1`、`diag1.intervals = 0, 38:40:1`、`diag1.fields_to_plot = ... divE F`、`warpx.do_dive_cleaning = 1`、`warpx.do_divb_cleaning = 1` 这组三帧 `F` 演化分支；`inputs_test_3d_langmuir_multi_psatd_momentum_conserving` 已补清 `algo.field_gathering = momentum-conserving`、`algo.maxwell_solver = psatd`、`warpx.cfl = 0.5773502691896258` 这组 gather/solver 组合稳定性分支，并写明它不会因为 `momentum-conserving` 就触发 `analysis_utils.py` 的守恒 gate。
- [x] 2026-05-25：继续清理 3D Langmuir input-level 邻近段里剩余仍偏粗的三行，并把它们和已完成 baseline-level contract 拉平：`inputs_test_3d_langmuir_multi_psatd_JRhom_LL2` 已补清 `algo.current_deposition = direct`、`psatd.JRhom = "LL2"`、`psatd.update_with_rho = 1` 这组 3D `J/rho` 时间依赖分支；`inputs_test_3d_langmuir_multi_psatd_JRhom_LL2_picmi.py` 已补清 `picmi.AnalyticDistribution + Cartesian3DGrid + ElectromagneticSolver + Simulation`、`warpx_psatd_update_with_rho=1`、`warpx_psatd_JRhom="LL2"`、`warpx_current_deposition_algo="direct"`，以及它其实直接绑定 `analysis_3d.py + checksum` 而非 checksum-only scaffold；`inputs_test_3d_langmuir_multi_psatd_current_correction` 已补清 `algo.current_deposition = esirkepov`、`psatd.current_correction = 1`、`psatd.periodic_single_box_fft = 1` 和 `divE` 诊断面。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的相邻 3D Langmuir input-level map 行，并把它们和已完成 baseline-level contract 对齐：`inputs_test_3d_langmuir_multi_picmi.py` 已补清 `picmi.UniformDistribution + Species + Cartesian3DGrid + ElectromagneticSolver + Simulation`、`warpx_current_deposition_algo="direct"` 和两条 `period=10` diagnostics，同时写明当前 `sim.write_input_file(...)` 仍停留在注释层；`inputs_test_3d_langmuir_multi_psatd_JRhom_LL2_nodal` 已补清 `algo.current_deposition = direct`、`psatd.JRhom = "LL2"`、`psatd.update_with_rho = 1`、`warpx.grid_type = collocated` 这组 3D nodal `J/rho` 时间依赖分支；`inputs_test_3d_langmuir_multi_psatd_current_correction_nodal` 已补清 `algo.current_deposition = direct`、`psatd.current_correction = 1`、`psatd.periodic_single_box_fft = 1`、完整 `divE` 场诊断和 `collocated` 这组 3D nodal-grid 强守恒分支。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的相邻 2D Langmuir input-level map 行，并把它们和已完成 baseline-level contract 对齐：`inputs_test_2d_langmuir_multi_picmi.py` 已补清 `picmi.UniformDistribution + Species + Cartesian2DGrid + ElectromagneticSolver + Simulation`、`warpx_current_deposition_algo="direct"`、`warpx_use_filter=0`、两条 `period="::10"` diagnostics 与 `sim.write_input_file("inputs2d_from_PICMI")`；`inputs_test_2d_langmuir_multi_psatd_JRhom_LL2_nodal` 已补清 `psatd.JRhom="LL2"`、`psatd.solution_type = first-order`、`psatd.update_with_rho = 1`、`warpx.grid_type = collocated` 这组 2D nodal `J/rho` 时间依赖分支；`inputs_test_2d_langmuir_multi_psatd_current_correction_nodal` 已补清 `algo.current_deposition = direct`、`psatd.current_correction = 1`、`psatd.periodic_single_box_fft = 1`、完整 `divE`/粒子变量诊断和 `collocated` 这组 2D nodal-grid 强守恒分支。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_2d_langmuir_multi_picmi`：已把这条 2D PICMI Langmuir baseline 从宽泛“当前主要覆盖 PICMI 前端配线”压实为更精确的 PICMI front-end + checksum 合同，并写清当前 `langmuir/CMakeLists.txt` 明确把它注册成 `analysis=OFF + analysis_default_regression.py --path diags/diag1000040`，所以当前唯一自动消费者就是最终 plotfile checksum。相对地，`inputs_test_2d_langmuir_multi_picmi.py` 显式用 `picmi.UniformDistribution + Species + Cartesian2DGrid + ElectromagneticSolver + Simulation` 组装二维周期 Langmuir 模式，并把 `warpx_current_deposition_algo="direct"` 与 `warpx_use_filter=0` 一起挂进 PICMI `Simulation`；与此同时 diagnostics 侧也被显式收缩成 checksum-facing 的最小消费面：`FieldDiagnostic(name="diag1", data_list=["Ex","Jx"], period="::10")` 只输出单分量场和电流，`ParticleDiagnostic(name="diag1", species=[electrons], data_list=["weighting","ux"], period="::10")` 只输出单物种的 `weighting/ux`。另外，这条脚本还显式执行 `sim.write_input_file(file_name="inputs2d_from_PICMI")`，把 PICMI 前端 materialize 成独立输入卡，再继续 `sim.step()` 运行。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_2d_langmuir_multi_psatd_JRhom_LL2_nodal`：已把这条 2D nodal `PSATD + JRhom_LL2` Langmuir baseline 从宽泛“继续比较解析 `Ex/Ez`”压实为更精确的 2D nodal-grid `J/rho` 消费者合同，并写清当前这条 active regression 同样只会在 `WarpX_FFT` 打开时，由 `langmuir/CMakeLists.txt` 注册成 `analysis_2d.py diags/diag1000080 + analysis_default_regression.py --path diags/diag1000080`；相对地，输入 `inputs_test_2d_langmuir_multi_psatd_JRhom_LL2_nodal` 在复用 `inputs_base_2d` 的 2D Langmuir 模态 scaffold 之上，显式设成 `algo.maxwell_solver = psatd`、`psatd.JRhom = "LL2"`、`psatd.solution_type = first-order`、`psatd.update_with_rho = 1`、`warpx.abort_on_warning_threshold = medium`、`warpx.cfl = 0.7071067811865475`、`warpx.grid_type = collocated`。与此同时，共享 `analysis_2d.py` 当前仍只会从最终 plotfile 读取网格场、逐项重建解析 2D Langmuir `Ex/Ez`，把二者最坏相对误差汇总成 `error_rel` 并要求小于 `0.0503`；但更关键的是，这条路径虽然显式打开了 `JRhom="LL2"` 与 `update_with_rho = 1`，`analysis_utils.py` 当前并不会因为这组开关或 `collocated` 组合就启用 `divE` 与 `rho/epsilon_0` 的 charge-conservation gate，而只识别 `esirkepov and not psatd`、`current_correction` 或 `vay` 三类路径。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_2d_langmuir_multi_psatd_current_correction_nodal`：已把这条 2D nodal `PSATD + current_correction` Langmuir baseline 从宽泛“继续比较解析 `Ex/Ez` 并强制检查 charge conservation”压实为更精确的 2D nodal-grid 强守恒消费者合同，并写清当前这条 active regression 同样只会在 `WarpX_FFT` 打开时，由 `langmuir/CMakeLists.txt` 注册成 `analysis_2d.py diags/diag1000080 + analysis_default_regression.py --path diags/diag1000080`；相对地，输入 `inputs_test_2d_langmuir_multi_psatd_current_correction_nodal` 在复用 `inputs_base_2d` 的 2D Langmuir 模态 scaffold 之上，显式设成 `algo.current_deposition = direct`、`algo.maxwell_solver = psatd`、`amr.max_grid_size = 128`、`diag1.fields_to_plot = Ex Ey Ez jx jy jz part_per_cell rho divE`、`diag1.electrons.variables = x z w ux uy uz`、`diag1.positrons.variables = x z w ux uy uz`、`psatd.current_correction = 1`、`psatd.periodic_single_box_fft = 1`、`warpx.cfl = 0.7071067811865475`、`warpx.grid_type = collocated`。与此同时，共享 `analysis_2d.py` 当前只会从最终 plotfile 读取网格场、逐项重建解析 2D Langmuir `Ex/Ez` 并要求 `error_rel < 0.0503`，随后再调用 `analysis_utils.py` 做额外守恒检查；而由于这条路径显式打开了 `psatd.current_correction = 1`，`analysis_utils.py` 会无条件启用 `divE` 与 `rho/epsilon_0` 的 charge-conservation gate，并把容差切到 `1e-9`。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_langmuir_multi_picmi`：已把这条 3D PICMI Langmuir baseline 从此前错误写成“直接绑定 `analysis_3d.py` 的多消费者链”修正为真实的 PICMI front-end + checksum 合同，并写清当前 `langmuir/CMakeLists.txt` 明确把它注册成 `analysis=OFF + analysis_default_regression.py --path diags/diag1000040`，所以这条路径当前唯一自动消费者就是最终 plotfile checksum。相对地，`inputs_test_3d_langmuir_multi_picmi.py` 显式用 `picmi.UniformDistribution + Species + Cartesian3DGrid + ElectromagneticSolver + Simulation` 组装三维周期 Langmuir 模式，并把 `warpx_current_deposition_algo="direct"` 挂进 PICMI `Simulation`；与此同时 diagnostics 侧也被显式收缩成 checksum-facing 的最小消费面：`FieldDiagnostic(name="diag1", data_list=["Ex","Jx"])` 只输出单分量场和电流，`ParticleDiagnostic(name="diag1", species=[electrons], data_list=["weighting","ux"])` 只输出单物种的 `weighting/ux`，既没有 openPMD on-particle-field 诊断，也没有 native 3D 基线里那组 `positrons` selective-output 面。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_langmuir_multi_psatd_current_correction_nodal`：已把这条 3D nodal `PSATD + current_correction` Langmuir baseline 从宽泛“继续比较解析场解并强制检查 charge conservation”压实为更精确的 nodal-grid 强守恒消费者合同，并写清当前这条 active regression 同样只会在 `WarpX_FFT` 打开时，由 `langmuir/CMakeLists.txt` 注册成 `analysis_3d.py diags/diag1000040 + analysis_default_regression.py --path diags/diag1000040`；相对地，输入 `inputs_test_3d_langmuir_multi_psatd_current_correction_nodal` 在复用公共 `inputs_base_3d` 那整套 Langmuir 模态、selective particle output 与 openPMD on-particle-field scaffold 的同时，显式设成 `algo.current_deposition = direct`、`algo.maxwell_solver = psatd`、`diag1.fields_to_plot = Ex Ey Ez Bx By Bz jx jy jz part_per_cell rho divE`、`psatd.current_correction = 1`、`psatd.periodic_single_box_fft = 1`、`warpx.cfl = 0.5773502691896258`、`warpx.grid_type = collocated`。与此同时，共享 `analysis_3d.py` 仍会继续检查最终 plotfile 里的 selective particle output、重建解析三维 `Ex/Ey/Ez` 场，并从 `OpenPMDTimeSeries("./diags/openpmd")` 读取 `iteration = 40` 上电子粒子位置与 on-particle `ex/ey/ez` 做解析回代，把这些误差继续汇总成 `error_rel < 5e-2`；但更关键的新增消费者仍来自 `analysis_utils.py`：由于这条路径显式打开了 `psatd.current_correction = 1`，脚本会无条件启用 `divE` 与 `rho/epsilon_0` 的 charge-conservation gate，并把容差切到 `1e-9`。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_langmuir_multi_psatd_vay_deposition_nodal`：已把这条 3D nodal `PSATD + Vay deposition` Langmuir baseline 从宽泛“继续比较解析场解并以 Vay 专用容差检查 charge conservation”压实为更精确的 nodal-grid 守恒消费者合同，并写清当前这条 active regression 同样只会在 `WarpX_FFT` 打开时，由 `langmuir/CMakeLists.txt` 注册成 `analysis_3d.py diags/diag1000040 + analysis_default_regression.py --path diags/diag1000040`；相对地，输入 `inputs_test_3d_langmuir_multi_psatd_vay_deposition_nodal` 在复用公共 `inputs_base_3d` 那整套 Langmuir 模态、selective particle output 与 openPMD on-particle-field scaffold 的同时，显式设成 `algo.current_deposition = vay`、`algo.maxwell_solver = psatd`、`diag1.fields_to_plot = Ex Ey Ez jx jy jz part_per_cell rho divE`、`warpx.cfl = 0.5773502691896258`、`warpx.grid_type = collocated`。与此同时，共享 `analysis_3d.py` 仍会继续检查最终 plotfile 里的 selective particle output、重建解析三维 `Ex/Ey/Ez` 场，并从 `OpenPMDTimeSeries("./diags/openpmd")` 读取 `iteration = 40` 上电子粒子位置与 on-particle `ex/ey/ez` 做解析回代，把这些误差继续汇总成 `error_rel < 5e-2`；但更关键的新增消费者仍来自 `analysis_utils.py`：由于这条路径显式打开了 `algo.current_deposition = vay`，脚本会无条件启用 `divE` 与 `rho/epsilon_0` 的 charge-conservation gate，并把容差从默认 `1e-11` 放宽到 `1e-3`。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_langmuir_multi_psatd_JRhom_LL2_nodal`：已把这条 3D nodal `PSATD + JRhom_LL2` Langmuir baseline 从宽泛“继续复用 `analysis_3d.py` 主合同”压实为更精确的 nodal-grid `J/rho` 消费者合同，并写清当前这条 active regression 同样只会在 `WarpX_FFT` 打开时，由 `langmuir/CMakeLists.txt` 注册成 `analysis_3d.py diags/diag1000040 + analysis_default_regression.py --path diags/diag1000040`；相对地，输入 `inputs_test_3d_langmuir_multi_psatd_JRhom_LL2_nodal` 在复用公共 `inputs_base_3d` 那整套 Langmuir 模态、selective particle output 与 openPMD on-particle-field scaffold 的同时，显式设成 `algo.current_deposition = direct`、`algo.maxwell_solver = psatd`、`psatd.JRhom = "LL2"`、`psatd.update_with_rho = 1`、`warpx.grid_type = collocated`，并保留 `warpx.cfl = 0.5773502691896258`。与此同时，共享 `analysis_3d.py` 仍会继续检查最终 plotfile 里的 selective particle output、重建解析三维 `Ex/Ey/Ez` 场，并从 `OpenPMDTimeSeries("./diags/openpmd")` 读取 `iteration = 40` 上电子粒子位置与 on-particle `ex/ey/ez` 做解析回代，把这些误差继续汇总成 `error_rel < 5e-2`；但更关键的是 `analysis_utils.py` 当前不会因为 `JRhom="LL2"`、`update_with_rho = 1` 或 `collocated` 组合就启用 `divE` 与 `rho/epsilon_0` 的 charge-conservation gate，而只识别 `esirkepov and not psatd`、`current_correction` 或 `vay` 三类路径。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_langmuir_multi_psatd_JRhom_LL2_picmi`：已把这条 3D PICMI `JRhom_LL2` Langmuir baseline 从宽泛“虽然输入来自 PICMI，但 `CMakeLists.txt` 中仍直接运行 `analysis_3d.py`”压实为更精确的 PICMI 前端消费者合同，并写清当前这条 active regression 同样只会在 `WarpX_FFT` 打开时，由 `langmuir/CMakeLists.txt` 直接绑定成 `analysis_3d.py diags/diag1000040 + analysis_default_regression.py --path diags/diag1000040`；更关键的新增 runtime 边界在 `inputs_test_3d_langmuir_multi_psatd_JRhom_LL2_picmi.py`：它显式用 `picmi.AnalyticDistribution + Cartesian3DGrid + ElectromagneticSolver + Simulation` 组装整个 Langmuir 模式，并通过 `warpx_psatd_update_with_rho=1`、`warpx_psatd_JRhom="LL2"`、`warpx_current_deposition_algo="direct"` 把 native `JRhom_LL2` 路径映射到 PICMI 前端；与此同时，它还用 `FieldDiagnostic(name="diag1")`、两条 `ParticleDiagnostic(name="diag1")` 和一条 `ParticleDiagnostic(name="openpmd", warpx_format="openpmd")` 明确 materialize 出与 native 版对齐的 field/selective-particle/on-particle-field 消费面。共享 `analysis_3d.py` 则继续检查最终 plotfile 里的 selective particle output、重建解析三维 `Ex/Ey/Ez` 场，并从 `OpenPMDTimeSeries("./diags/openpmd")` 读取 `iteration = 40` 上电子粒子位置与 on-particle `ex/ey/ez` 做解析回代，最终要求 `error_rel < 5e-2`；但和 native `JRhom_LL2` 一样，`analysis_utils.py` 当前不会因为 `JRhom="LL2"` 或 `update_with_rho=1` 就启用 `divE` 与 `rho/epsilon_0` 的 charge-conservation gate。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_langmuir_multi_psatd_JRhom_LL2`：已把这条 3D `PSATD + JRhom_LL2` Langmuir baseline 从宽泛“analysis 继续比较解析场解并检查 on-particle fields”压实为更精确的 `J/rho` 时间依赖消费者合同，并写清当前这条 active regression 同样只会在 `WarpX_FFT` 打开时，由 `langmuir/CMakeLists.txt` 注册成 `analysis_3d.py diags/diag1000040 + analysis_default_regression.py --path diags/diag1000040`；相对地，输入 `inputs_test_3d_langmuir_multi_psatd_JRhom_LL2` 在复用公共 `inputs_base_3d` 那整套 Langmuir 模态、selective particle output 与 openPMD on-particle-field scaffold 的同时，显式设成 `algo.current_deposition = direct`、`algo.maxwell_solver = psatd`、`psatd.JRhom = "LL2"`、`psatd.update_with_rho = 1`，并保留 `warpx.cfl = 0.5773502691896258`。与此同时，共享 `analysis_3d.py` 仍会继续检查最终 plotfile 里的 selective particle output、重建解析三维 `Ex/Ey/Ez` 场，并从 `OpenPMDTimeSeries("./diags/openpmd")` 读取 `iteration = 40` 上电子粒子位置与 on-particle `ex/ey/ez` 做解析回代，把这些误差继续汇总成 `error_rel < 5e-2`；但更关键的是 `analysis_utils.py` 当前根本不会因为 `psatd.JRhom = "LL2"` 或 `update_with_rho = 1` 就启用 `divE` 与 `rho/epsilon_0` 的 charge-conservation gate，而只识别 `esirkepov and not psatd`、`current_correction` 或 `vay` 三类路径。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_langmuir_multi_psatd_nodal`：已把这条 3D nodal `PSATD` Langmuir baseline 从宽泛“analysis 继续比较解析场解并检查 on-particle fields”压实为更精确的 nodal-grid 消费者合同，并写清当前这条 active regression 只会在 `WarpX_FFT` 打开时，由 `langmuir/CMakeLists.txt` 注册成 `analysis_3d.py diags/diag1000040 + analysis_default_regression.py --path diags/diag1000040`；相对地，输入 `inputs_test_3d_langmuir_multi_psatd_nodal` 在复用公共 `inputs_base_3d` 那整套 Langmuir 模态、selective particle output 与 openPMD on-particle-field scaffold 的同时，显式设成 `algo.current_deposition = direct`、`algo.maxwell_solver = psatd`、`psatd.current_correction = 0`、`warpx.grid_type = collocated`，并保留 `warpx.cfl = 0.5773502691896258`。与此同时，共享 `analysis_3d.py` 仍会继续检查最终 plotfile 里的 selective particle output、重建解析三维 `Ex/Ey/Ez` 场，并从 `OpenPMDTimeSeries("./diags/openpmd")` 读取 `iteration = 40` 上电子粒子位置与 on-particle `ex/ey/ez` 做解析回代，把这些误差继续汇总成 `error_rel < 5e-2`；但更关键的是 `analysis_utils.py` 当前根本不会因为这条路径的 `collocated` 或 `direct + psatd` 组合就启用 `divE` 与 `rho/epsilon_0` 的 charge-conservation gate，而只识别 `esirkepov and not psatd`、`current_correction` 或 `vay` 三类路径。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_langmuir_multi_psatd_momentum_conserving`：已把这条 3D `PSATD + momentum-conserving gather` Langmuir baseline 从宽泛“analysis 额外按 `analysis_utils.py` 检查 Gauss 定律相对误差”压实为更精确的 gather/solver 组合消费者合同，并写清当前这条 active regression 同样只会在 `WarpX_FFT` 打开时，由 `langmuir/CMakeLists.txt` 注册成 `analysis_3d.py diags/diag1000040 + analysis_default_regression.py --path diags/diag1000040`；相对地，输入 `inputs_test_3d_langmuir_multi_psatd_momentum_conserving` 在复用公共 `inputs_base_3d` 那整套 Langmuir 模态、selective particle output 与 openPMD on-particle-field scaffold 的同时，显式把 `algo.field_gathering` 切成 `momentum-conserving`，并把 `algo.maxwell_solver = psatd`、`warpx.cfl = 0.5773502691896258` 一起固定下来。与此同时，共享 `analysis_3d.py` 仍会继续检查最终 plotfile 里的 selective particle output、重建解析三维 `Ex/Ey/Ez` 场，并从 `OpenPMDTimeSeries("./diags/openpmd")` 读取 `iteration = 40` 上电子粒子位置与 on-particle `ex/ey/ez` 做解析回代，把这些误差继续汇总成 `error_rel < 5e-2`；但更关键的是 `analysis_utils.py` 当前根本不会因为 `algo.field_gathering = momentum-conserving` 就启用 `divE` 与 `rho/epsilon_0` 的 charge-conservation gate，而只识别 `esirkepov and not psatd`、`current_correction` 或 `vay` 三类路径。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_langmuir_multi_psatd_vay_deposition`：已把这条 3D `PSATD + Vay deposition` Langmuir baseline 从宽泛“analysis 以 Vay 专用容差检查 charge conservation”压实为更精确的守恒消费者合同，并写清当前这条 active regression 同样只会在 `WarpX_FFT` 打开时，由 `langmuir/CMakeLists.txt` 注册成 `analysis_3d.py diags/diag1000040 + analysis_default_regression.py --path diags/diag1000040`；相对地，输入 `inputs_test_3d_langmuir_multi_psatd_vay_deposition` 在复用公共 `inputs_base_3d` 那整套 Langmuir 模态、selective particle output 与 openPMD on-particle-field scaffold 的同时，显式把 `algo.current_deposition` 切成 `vay`，并把 `algo.maxwell_solver = psatd`、`warpx.cfl = 0.5773502691896258` 一起固定下来；同时 `diag1.fields_to_plot` 只保留 `Ex Ey Ez jx jy jz part_per_cell rho divE`，不再像 native 基线那样保留 `Bx/By/Bz`。与此同时，共享 `analysis_3d.py` 仍会继续检查最终 plotfile 里的 selective particle output、重建解析三维 `Ex/Ey/Ez` 场，并从 `OpenPMDTimeSeries("./diags/openpmd")` 读取 `iteration = 40` 上电子粒子位置与 on-particle `ex/ey/ez` 做解析回代，把这些误差继续汇总成 `error_rel < 5e-2`；但更关键的新增消费者来自 `analysis_utils.py`，因为这条路径显式打开了 `algo.current_deposition = vay`，脚本会无条件启用 `divE` 与 `rho/epsilon_0` 的 charge-conservation gate，并把容差从默认 `1e-11` 放宽到 `1e-3`。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_langmuir_multi_psatd_div_cleaning`：已把这条 3D `PSATD + div-cleaning` Langmuir baseline 从宽泛“analysis 额外断言 `dF/dt = div(E) - rho/eps0`”压实为更精确的三帧 `F` 演化消费者合同，并写清当前这条 active regression 同样只会在 `WarpX_FFT` 打开时，由 `langmuir/CMakeLists.txt` 注册成 `analysis_3d.py diags/diag1000040 + analysis_default_regression.py --path diags/diag1000040`；相对地，输入 `inputs_test_3d_langmuir_multi_psatd_div_cleaning` 显式把 `algo.current_deposition = direct`、`algo.maxwell_solver = psatd`、`psatd.update_with_rho = 1`、`warpx.do_dive_cleaning = 1`、`warpx.do_divb_cleaning = 1` 一起挂上，并把 `diag1.intervals` 改成 `0, 38:40:1`，同时把 `diag1.fields_to_plot` 扩成包含 `divE` 和辅助标量 `F` 的 `Ex Ey Ez Bx By Bz jx jy jz part_per_cell rho divE F`。与此同时，共享 `analysis_3d.py` 仍会继续检查最终 plotfile 里的 selective particle output、重建解析三维 `Ex/Ey/Ez` 场，并从 `OpenPMDTimeSeries("./diags/openpmd")` 读取 `iteration = 40` 上电子粒子位置与 on-particle `ex/ey/ez` 做解析回代，要求 `error_rel < 5e-2`；但更关键的新增消费者在它的 `div_cleaning` 分支：脚本会额外打开 `diags/diag1000038`、`diags/diag1000039` 和最终 `diags/diag1000040` 三个 plotfile，读取 `F_old/F_new` 与中间帧 `rho/divE`，再按硬编码 `dt = 1.203645751e-15` 重建 `dF/dt = div(E) - rho/epsilon_0`，并要求相对 `L∞` 误差低于 `1e-2`。与此同时，由于这条输入把电流沉积切成了 `direct`，`analysis_utils.py` 的通用 charge-conservation gate 在这条路径上反而不会触发。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_langmuir_multi_psatd_current_correction`：已把这条 3D `PSATD + current_correction` Langmuir baseline 从宽泛“analysis 继续比较解析场解并强制检查 charge conservation”压实为更精确的强守恒消费者合同，并写清当前这条 active regression 同样只会在 `WarpX_FFT` 打开时，由 `langmuir/CMakeLists.txt` 注册成 `analysis_3d.py diags/diag1000040 + analysis_default_regression.py --path diags/diag1000040`；相对地，输入 `inputs_test_3d_langmuir_multi_psatd_current_correction` 在复用公共 `inputs_base_3d` 那整套 Langmuir 模态、selective particle output 与 openPMD on-particle-field scaffold 的同时，显式设成 `algo.current_deposition = esirkepov`、`algo.maxwell_solver = psatd`、`psatd.current_correction = 1`、`psatd.periodic_single_box_fft = 1`，并把 `diag1.fields_to_plot` 扩成包含 `divE` 的 `Ex Ey Ez Bx By Bz jx jy jz part_per_cell rho divE`。与此同时，共享 `analysis_3d.py` 仍会继续检查最终 plotfile 里的 selective particle output、重建解析三维 `Ex/Ey/Ez` 场，并从 `OpenPMDTimeSeries("./diags/openpmd")` 读取 `iteration = 40` 上电子粒子位置与 on-particle `ex/ey/ez` 做解析回代，把这些误差继续汇总成 `error_rel < 5e-2`；但更关键的新增消费者来自 `analysis_utils.py`，因为这条路径显式打开了 `psatd.current_correction = 1`，脚本会无条件启用 `divE` 与 `rho/epsilon_0` 的 charge-conservation gate，并把容差切到 `1e-9`。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_langmuir_multi_psatd`：已把这条 3D `PSATD` Langmuir baseline 从宽泛“analysis 继续比较解析场解、检查 selective particle output 与 on-particle fields”压实为更精确的 FFT-gated spectral 消费者合同，并写清当前这条 active regression 只会在 `WarpX_FFT` 打开时，由 `langmuir/CMakeLists.txt` 注册成 `analysis_3d.py diags/diag1000040 + analysis_default_regression.py --path diags/diag1000040`；相对地，输入 `inputs_test_3d_langmuir_multi_psatd` 在复用公共 `inputs_base_3d` 那整套 Langmuir 模态、selective particle output 与 openPMD on-particle-field diagnostics scaffold 的同时，只额外切了 `algo.maxwell_solver = psatd` 和 `warpx.cfl = 0.5773502691896258` 两处关键开关。与此同时，共享 `analysis_3d.py` 仍会继续检查最终 plotfile 里的 selective particle output、重建解析三维 `Ex/Ey/Ez` 场，并从 `OpenPMDTimeSeries("./diags/openpmd")` 读取 `iteration = 40` 上电子粒子位置与 on-particle `ex/ey/ez` 做解析回代，把这些误差继续汇总成 `error_rel < 5e-2`；但更关键的分岔在 `analysis_utils.py`，因为它明确不会在 `esirkepov + psatd` 这一组合上启用 `divE` 与 `rho/epsilon_0` 的 charge-conservation gate，而只对 `esirkepov and not psatd`、`current_correction` 或 `vay` 路径做这条检查。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_langmuir_multi`：已把这条 3D native Langmuir baseline 从宽泛“analysis 比较解析 `Ex/Ey/Ez`、检查 selective particle output 与 openPMD 粒子上场采样，并在适用时检查 charge conservation”压实为更精确的多消费者合同，并写清当前 `langmuir/CMakeLists.txt` 实际绑定的是 `analysis_3d.py diags/diag1000040 + analysis_default_regression.py --path diags/diag1000040`；相对地，输入 `inputs_test_3d_langmuir_multi` 本体只是 `FILE = inputs_base_3d` 的薄入口，而真正的 runtime scaffold 藏在基底里：它不仅 materialize 出 `electrons/positrons` 的三维 Langmuir 模态，还显式把 selective particle output 收紧成 `diag1.electrons.variables = x y z w ux`、`diag1.positrons.variables = x y z uz`，并通过 `openpmd.electrons.additional_variables = Ex Ey Ez` 把电子粒子上的采样场一起落盘。与此同时，共享 `analysis_3d.py` 会先检查 selective particle output，再从 plotfile 重建解析三维 `Ex/Ey/Ez` 场，又从 `OpenPMDTimeSeries("./diags/openpmd")` 读取 `iteration = 40` 上电子粒子位置与 on-particle `ex/ey/ez` 做逐粒子误差比较，并把这些误差汇总成 `error_rel < 5e-2`；最后还会把 plotfile 数据交给 `analysis_utils.py` 的 `check_charge_conservation(data)`，在这条 native 3D 基线的 `esirkepov + non-PSATD + non-RZ` 组合下实际要求 `divE` 与 `rho/epsilon_0` 的相对 `L∞` 误差低于 `1e-11`。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_langmuir_multi_nodal`：已把这条 3D nodal Langmuir baseline 从宽泛“仍复用 native analysis 合同”压实为更精确的 `direct + collocated` 多消费者合同，并写清当前 `langmuir/CMakeLists.txt` 实际绑定的仍是 `analysis_3d.py diags/diag1000040 + analysis_default_regression.py --path diags/diag1000040`；相对地，输入 `inputs_test_3d_langmuir_multi_nodal` 在复用公共 `inputs_base_3d` 那整套 Langmuir 模态、selective particle output 和 openPMD on-particle-field diagnostics scaffold 的同时，显式把 `algo.current_deposition` 从 native 基线的 `esirkepov` 切成 `direct`，并把 `warpx.grid_type` 设成 `collocated`。与此同时，共享 `analysis_3d.py` 仍会继续检查最终 plotfile 里的 selective particle output、重建解析三维 `Ex/Ey/Ez` 场，并从 `OpenPMDTimeSeries("./diags/openpmd")` 读取 `iteration = 40` 上电子粒子位置与 on-particle `ex/ey/ez` 做解析回代，把这些误差继续汇总成 `error_rel < 5e-2`；但更关键的分岔在 `analysis_utils.py`，因为它只会在 `esirkepov`、`current_correction` 或 `vay` 这些路径上启用 `divE` 与 `rho/epsilon_0` 的 charge-conservation gate，所以这条 `direct + collocated` nodal 版本当前不会再触发 native 基线里的 `1e-11` Gauss 定律误差断言。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_langmuir_fluid`：已把这条 3D cold-fluid Langmuir baseline 从宽泛“analysis 直接比较解析 `Ex/Ey/Ez/Jx/Jy/Jz/rho`”压实为更精确的双流体消费者合同，并写清当前 `langmuir_fluids/CMakeLists.txt` 实际绑定的是 `analysis_3d.py diags/diag1000040 + analysis_default_regression.py --path diags/diag1000040`；相对地，输入 `inputs_test_3d_langmuir_fluid` 在 `40 µm` 立方周期盒与 `64^3` 网格上推进 `max_step = 40`，保持 `esirkepov + energy-conserving gather`，并用 `electrons + positrons` 双流体加相反号的 `parse_momentum_function_ux/uy/uz` materialize 出三维小振幅 Langmuir 模态；与此同时，诊断侧只在最后一步落一次 `diag1` plotfile，显式输出 `Ex/Ey/Ez/Bx/By/Bz/jx/jy/jz/part_per_cell/rho`。共享 `analysis_3d.py` 则会按输入参数重建 `kx/ky/kz`、`wp` 和解析 `E/J/rho` 场，其中 `J` 还显式补偿了 Yee 电流半步偏移，最后把 `Ex/Ey/Ez`、`Jx/Jy/Jz` 和 `rho` 的逐分量最大相对误差汇总成单个 `error_rel`，并要求 `error_rel < 5e-2`。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_ionization_ion_dsmc`：已把这条 3D ion-impact DSMC ionization baseline 从宽泛“analysis 检查同一 global model 路径”压实为更精确的 active/inactive 边界，并写清当前 `ionization_dsmc/CMakeLists.txt` 实际把它注册成 `analysis = OFF + analysis_default_regression.py --path diags/diag1000250`；相对地，输入 `inputs_test_3d_ionization_ion_dsmc` 只在公共 `inputs_base_3d` 之上切换了 `ioniz.ionization_cross_section = .../ion_impact_ionization.dat` 与 `ioniz.species = ions neutrals`，因此命中的 runtime 路径确实是 ion-impact DSMC ionization。更关键的是，现有 `analysis_ionization_dsmc_3d.py` 并不是中性的共享分析脚本：它把 `sigma_iz_file` 硬编码成 `electron_impact_ionization.dat`，并只从 `species="electrons"` 的速度分量重建 `T_e`，再据此用 quasi-Monte-Carlo `MultivariateNormalQMC` 构造 electron-impact 的 `k_iz(T_e)` 和对应 0D global model。正因为这条脚本当前显式绑定了 electron-impact 假设，所以 ion-impact 3D regression 在 active 配置里只保留最终 `diag1000250` plotfile 的 checksum 消费路径。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_ionization_electron_dsmc`：已把这条 3D electron-impact DSMC ionization baseline 从宽泛“analysis 检查 `n_e / n_n / n_eT_e` global model”压实为更精确的 0D 反应系统消费者合同，并写清当前 `ionization_dsmc/CMakeLists.txt` 实际绑定的是 `analysis_ionization_dsmc_3d.py + analysis_default_regression.py --path diags/diag1000250`，而相邻 `test_3d_ionization_ion_dsmc` 当前反而把同一 analysis 显式关掉了；相对地，输入 `inputs_test_3d_ionization_electron_dsmc` 只在公共 `inputs_base_3d` 之上切换了 `ioniz.ionization_cross_section = .../electron_impact_ionization.dat` 与 `ioniz.species = electrons neutrals`，而真正的 runtime scaffold 藏在基底里：关闭 Maxwell solver、初始化 `electrons/ions/neutrals` 三种均匀 Maxwellian 物种，并把 `ioniz` 配成 `product_species = electrons ions`、`ionization_target_species = neutrals`、`ionization_energy = 13.59844 eV`。与此同时，共享 `analysis_ionization_dsmc_3d.py` 会先从 `diag2` 的电子速度分量与 `counts.txt` 重建 `n_e/n_n/n_eT_e` 三条 WarpX 时间序列，再读取 `electron_impact_ionization.dat` 截面表，用 quasi-Monte-Carlo `MultivariateNormalQMC` 积分 Maxwellian 电子 VDF 得到速率系数表 `k_iz(T_e)`，随后在 0D global model 上做 RK2 时间推进，并最终要求三条相对误差全程低于 `2.5e-3`、`1e-6` 和 `6e-3`。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_ion_stopping`：已把这条 3D `background_stopping` baseline 从宽泛“analysis 逐点验证电子/离子 slowing-down 解析公式”压实为更精确的四路径消费者合同，并写清当前 `ion_stopping/CMakeLists.txt` 实际绑定的是 `analysis.py diags/diag1000010 + analysis_default_regression.py --path diags/diag1000010`；相对地，输入 `inputs_test_3d_ion_stopping` 显式只注入四组 `do_not_deposit = 1` 的测试离子，其中 `ions1/ions2` 为 `proton`、`ions3/ions4` 为 `mass = 4*m_p` 的重离子，同时碰撞侧一次性挂出 `stopping_on_electrons_constant`、`stopping_on_electrons_parsed`、`stopping_on_ions_constant`、`stopping_on_ions_parsed` 四条 `background_stopping` 路径，把 `background_type = electrons/ions` 与 constant / parser 形式的 `background_density/background_temperature` 全部并排打通；与此同时，共享 `analysis.py` 会先从 `diag1000000` 读取四组离子的初始动量与位置，并重建 constant / parsed 背景参数，再用与 C++ 同形的 `stopping_from_electrons(...)` 和 `stopping_from_ions(...)` 显式循环 `10` 步，把四组离子的解析能量衰减推进到末态，最后再从 `diag1000010` 读取终态动量并要求四条路径逐粒子的绝对能量误差都小于 `1e-7 eV`。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_ion_beam_extraction`：已把这条 3D ion-beam-extraction baseline 从宽泛“analysis 检查电极抽取后的离子束尾部能量是否接近 `40 keV`”压实为更精确的 embedded-boundary electrode 消费者合同，并写清当前 `ion_beam_extraction/CMakeLists.txt` 实际绑定的是 `analysis_ion_beam_extraction.py diags/diag1/ + analysis_default_regression.py --path diags/diag1/`；相对地，输入 `inputs_test_3d_ion_beam_extraction` 会显式打开 `warpx.do_electrostatic = labframe`，组合 `boundary.potential_lo_z = 0`、多面 `neumann/pec` 场边界、`warpx.eb_implicit_function` 的多段电极几何，以及 `warpx.eb_potential(...)` 的分段固定电极势，并在 `z<0` 源区先填充 `Dplus + electrons` 热等离子体，再持续从 `-z`、`±x`、`±y` 五个边界用 `NFluxPerCell + gaussianflux` 热通量重注入两种 species；与此同时，诊断侧同时输出 openPMD `diag1` 的 `rho/Ex/Ey/Ez/phi/eb_covered/rho_electrons/rho_Dplus` 和 `BoundaryScraping bound`。共享 `analysis_ion_beam_extraction.py` 则会在固定 `iteration = 1000` 上先读取 `phi` 与 `eb_covered` 的 `y` 向切片，再读取 `Dplus` 的 `x/z/ux/uy/uz/mass` 数据，把粒子动量换算成离子动能，只在 `14 mm <= z <= 23 mm` 的尾段上逐粒子要求 `abs(E-40 keV)/40 keV < 0.05`。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_initial_distribution`：已把这条 3D 多分布初始化 baseline 从宽泛“analysis 检查直方图、束斑统计与解析分布”压实为更精确的 reduced-diagnostic 消费者合同，并写清当前输入 `inputs_test_3d_initial_distribution` 在 `8^3` 周期盒子里一次性并列注入九组 species，分别覆盖 `gaussian`、`maxwell_boltzmann`、`maxwell_juttner`、`gaussian_beam`、`maxwell_juttner_parser`、`velocity_constant`、`velocity_parser`、`uniform` 和 `gaussian_parser` 这九条初始化路径；与此同时，诊断侧并不是 plotfile/openPMD，而是一次性挂出二十多个 `ParticleHistogram` reduced diag 与 `BeamRelevant bmmntr`，分别消费三轴 Gaussian / Maxwell-Boltzmann 动量、全谱与过滤后的 Maxwell-Juttner、Gaussian beam 三轴位置和截断总电荷、parser 温度两半域、constant / parser bulk velocity、uniform 动量立方体，以及 `ux/z`、`uy/z`、`uz/z` 归一化后的 parser-Gaussian 动量；相对地，共享 `analysis.py` 会统一以 `tolerance = 0.02` 为主阈值逐项要求这些 diagnostics 闭合到对应解析分布，其中 `velocity_constant` 还显式把 `gamma` 与 `u_y` 消费成 delta-like bin，而 `uniform` 分支则逐时间步调用 `check_validity_uniform(...)`，按 binomial `3 sigma` 上界检查三轴直方图。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_hard_edged_quadrupoles_moving`：已把这条 3D moving-window hard-edged quadrupole baseline 从宽泛“moving-window 变体，analysis 仍要求最终轨道满足同一解析解”压实为更精确的 moving-window 消费者合同，并写清当前输入 `inputs_test_3d_hard_edged_quadrupoles_moving` 在保留 `warpx.do_electrostatic = labframe` 与同一条 `drift1 -> quad1 -> drift2 -> quad2` lattice 的同时，显式打开 `warpx.do_moving_window = 1`、`warpx.moving_window_dir = z`、`warpx.moving_window_v = 0.1`，并把 longitudinal box 压缩到 `z in [-0.1, 0.1]`；相对地，共享 `analysis.py` 并没有单独为 moving window 写特殊分支，而是继续直接从最终 plotfile 读取末态 `x/z/ux`，递归展开 lattice 并用解析 `applylens(...)` 逐段推进，最终仍要求 `x` 相对误差小于 `1%`、`ux` 相对误差小于 `0.2%`。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_hard_edged_quadrupoles_boosted`：已把这条 3D boosted hard-edged quadrupole baseline 从宽泛“先把粒子轨道反变换回 lab frame 再做解析对照”压实为更精确的 boosted-frame 消费者合同，并写清当前输入 `inputs_test_3d_hard_edged_quadrupoles_boosted` 去掉了 `warpx.do_electrostatic = labframe`，改为显式打开 `warpx.gamma_boost = 2.` 与 `warpx.boost_direction = z`，同时压缩 longitudinal box、把单粒子 `single_particle_u` 提高到 `(0, 0, 2.0)`，并把 lattice 直接平铺成 `drift1 quad1 drift2 quad2`；相对地，共享 `analysis.py` 在 `gamma_boost > 1` 时会先用 `zz_sim = gamma_boost*zz_sim + uz_boost*time` 把数值末态 `z` 反变换回 lab frame，随后才继续递归展开 lattice 并用解析 `applylens(...)` 逐段推进，最终仍要求 `x` 相对误差小于 `1%`、`ux` 相对误差小于 `0.2%`。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_hard_edged_quadrupoles`：已把这条 3D hard-edged quadrupole baseline 从宽泛“analysis 把最终粒子轨道与解析透镜串联解直接比较”压实为更精确的 accelerator-lattice 消费者合同，并写清当前输入 `inputs_test_3d_hard_edged_quadrupoles` 显式打开 `warpx.do_electrostatic = labframe`，只注入一个 `SingleParticle` 电子，再通过嵌套 `lattice.elements = line1 line2` 把 `drift1 -> quad1 -> drift2 -> quad2` 这条透镜链 materialize 出来；相对地，共享 `analysis.py` 会先从 plotfile 读取末态 `x/z/ux`，再递归解析 `lattice/line/drift/quad` 定义，重建每个 quadrupole 的起点、长度和 `dEdx`，随后用解析 `applylens(...)` 逐段推进，并最终要求 `x` 相对误差小于 `1%`、`ux` 相对误差小于 `0.2%`。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_focusing_gaussian_beam_from_openpmd`：已把这条 native openPMD 粒子注入 baseline 从宽泛“输入路径 + checksum + 脚本缺口”压实为更精确的 native external-file 边界，并写清当前 `gaussian_beam/CMakeLists.txt` 把它注册成 `analysis.py + analysis_default_regression.py --path diags/diag1000000`，且和 PICMI 版一样显式依赖 `test_3d_focusing_gaussian_beam_from_openpmd_prepare`；相对地，输入 `inputs_test_3d_focusing_gaussian_beam_from_openpmd` 通过 `beam1.injection_style = external_file` 与 `beam1.injection_file = ../test_3d_focusing_gaussian_beam_from_openpmd_prepare/openpmd_generated_particles.h5` 命中 native `setupExternalFile()` 路径，并继续复用相同的 `rho_beam1 + openPMD w/x/y/z` 诊断面，而更关键的运行时缺口是本地 checkout 里实际并不存在同名 `analysis.py`，所以这条 active 路径当前还没有像 PICMI 版那样闭合到束斑理论消费者链。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_galilean_psatd_current_correction_psb`：已把这条 3D `current_correction=1 + periodic_single_box_fft=1` Galilean PSATD baseline 从宽泛“PSB 版本仍检查能量与电荷误差”压实为更精确的 PSB 双消费者合同，并写清当前输入 `inputs_test_3d_galilean_psatd_current_correction_psb` 在公共 `inputs_base_3d` 的相对论均匀漂移等离子体 scaffold 之上，显式额外挂了 `diag1.fields_to_plot = Ex Ey Ez Bx By Bz jx jy jz rho divE`，同时设成 `psatd.current_correction = 1`、`psatd.periodic_single_box_fft = 1`、`psatd.update_with_rho = 0`、`psatd.v_galilean = 0. 0. 0.99498743710662`，并把 `warpx.numprocs` 收缩成 `1 1 1`；相对地，共享 `analysis_galilean.py` 在这条 3D PSB current-correction 分支上会选用 `energy_ref = 856783.3007547935`，保留更严格的 `tol_charge = 1e-9`，先要求全域场能比 `energy / energy_ref < 1e-8`，再额外要求 `divE-rho/eps0` 的相对 `L∞` 误差低于 `1e-9`。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_galilean_psatd_current_correction`：已把这条 3D `current_correction=1` Galilean PSATD baseline 从宽泛“同时检查电场能量抑制和 `divE-rho/eps0` 误差”压实为更精确的双消费者合同，并写清当前输入 `inputs_test_3d_galilean_psatd_current_correction` 在公共 `inputs_base_3d` 的相对论均匀漂移等离子体 scaffold 之上，显式额外挂了 `diag1.fields_to_plot = Ex Ey Ez Bx By Bz jx jy jz rho divE`，同时设成 `psatd.current_correction = 1`、`psatd.periodic_single_box_fft = 0`、`psatd.update_with_rho = 0` 和 `psatd.v_galilean = 0. 0. 0.99498743710662`；相对地，共享 `analysis_galilean.py` 在这条 3D 非 PSB current-correction 分支上会选用 `energy_ref = 875307.5138913819`、`tol_charge = 1e-2`，先要求全域场能比 `energy / energy_ref < 1e-8`，再额外要求 `divE-rho/eps0` 的相对 `L∞` 误差低于 `1e-2`。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_galilean_psatd`：已把这条 3D Galilean PSATD baseline 从宽泛“analysis 比较最终电场能量相对不稳定参考值的比例”压实为更精确的 NCI 抑制消费者合同，并写清当前 active 路径实际来自 `nci_psatd_stability/CMakeLists.txt` 的 `analysis_galilean.py diags/diag1000300 + analysis_default_regression.py --path diags/diag1000300 --rtol 1e-8`；相对地，输入 `inputs_test_3d_galilean_psatd` 在公共 `inputs_base_3d` 的相对论均匀漂移等离子体 scaffold 之上显式设成 `psatd.current_correction = 0` 与 `psatd.v_galilean = 0. 0. 0.99498743710662`，而共享 `analysis_galilean.py` 会先从 `warpx_used_inputs` 解析运行时开关，再对这条 3D 非 current-correction 路径选用 `energy_ref = 661285.098907683` 和 `tol_energy = 1e-8`，最后要求全域电场能量比 `energy / energy_ref < 1e-8`。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_focusing_gaussian_beam_from_openpmd_picmi`：已把这条 3D PICMI openPMD 粒子注入 baseline 从宽泛“对应 PICMI openPMD 粒子注入，analysis 会检查束斑统计”压实为更精确的 prepare-plus-PICMI 双段合同，并写清当前 `gaussian_beam/CMakeLists.txt` 实际绑定了 `analysis_focusing_beam.py + analysis_default_regression.py --path diags/diag1000000`，且显式依赖 `test_3d_focusing_gaussian_beam_from_openpmd_prepare`；相对地，prepare 脚本会先生成与聚焦理论一致的 `x/y/z/ux/uy/uz` 样本，并把 `weighting/mass/charge/positionOffset` 与 `momentum.unit_SI = m_e*c` 一起写入 `openpmd_generated_particles.h5`，随后 PICMI 输入再通过 `picmi.FromFileDistribution(...)` 把这份文件接进 `beam1`，而共享 `analysis_focusing_beam.py` 仍会从 openPMD 末态 `beam1` 的 `x/y/z/w` 逐 slice 计算加权束斑尺寸 `sx/sy`，再分别要求它们与理论聚焦关系 `s(z, sigma0, emit/gamma)` 满足 `rtol = 0.051 / 0.038` 的 `np.allclose` 断言。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_focusing_gaussian_beam_photons`：已把这条 3D photon-species Gaussian-beam baseline 从宽泛“对应 photon 版聚焦场景，analysis 仍会检查束斑尺寸统计”压实为更精确的 photon runtime 合同，并写清当前 `gaussian_beam/CMakeLists.txt` 仍直接绑定 `analysis_focusing_beam.py + analysis_default_regression.py --path diags/diag1000000`；相对地，输入 `inputs_test_3d_focusing_gaussian_beam_photons` 在保留 `beam1.injection_style = gaussian_beam`、`focal_distance = 4*sigmaz` 和同一套动量散度参数的同时，显式把 `beam1.species_type` 切成 `photon`，并把电子束版本的 `beam1.q_tot` 改成 `beam1.npart_real`，而共享 `analysis_focusing_beam.py` 仍会从 openPMD 末态 `beam1` 的 `x/y/z/w` 逐 slice 计算加权束斑尺寸 `sx/sy`，再分别要求它们与理论聚焦关系 `s(z, sigma0, emit/gamma)` 满足 `rtol = 0.051 / 0.038` 的 `np.allclose` 断言。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_focusing_gaussian_beam`：已把这条 3D 聚焦 Gaussian-beam baseline 从宽泛“对应聚焦场景，不替代理论束斑断言”压实为更精确的 native Gaussian-beam 聚焦消费者合同，并写清当前 `gaussian_beam/CMakeLists.txt` 实际直接绑定了 `analysis_focusing_beam.py + analysis_default_regression.py --path diags/diag1000000`；相对地，输入 `inputs_test_3d_focusing_gaussian_beam` 显式通过 `beam1.injection_style = gaussian_beam` 打开 native `setupGaussianBeam()` 路径，并给出 `sigmax/sigmay/sigmaz`、`emitx/emity`、`focal_distance = 4*sigmaz` 和动量散度参数，而 `analysis_focusing_beam.py` 会从 openPMD 末态 `beam1` 的 `x/y/z/w` 逐 slice 计算加权束斑尺寸 `sx/sy`，再分别要求它们与理论聚焦关系 `s(z, sigma0, emit/gamma)` 满足 `rtol = 0.051 / 0.038` 的 `np.allclose` 断言。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_flux_injection_from_eb`：已把这条 3D 球形 EB 发射 baseline 从宽泛“analysis 检查总通量、法向/切向动量分布和 EB 外几何位置”压实为更精确的局部法向坐标消费者合同，并写清当前输入在公共 `inputs_base_from_eb` 之上显式设成球形 EB `warpx.eb_implicit_function = "-(x**2+y**2+z**2-2**2)"`、`inject_from_embedded_boundary = 1` 和有限时间窗发射；相对地，`analysis_flux_injection_from_eb.py` 会先从 `warpx_used_inputs` 反解维度和理论总权重，再重建球面法向，要求粒子全部位于 `0.98R` 之外，并在局部法/切向坐标系中分别对 `u_n / u_perp / u_perp2` 做分布直方图断言。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_flux_injection`：已把这条 3D flux-injection baseline 从宽泛“对应 NFluxPerCell 场景，analysis 检查分布和总发射量”压实为更精确的逐分量速度分布消费者合同，并写清当前输入在关闭 Maxwell solver 的前提下显式同时注入 `electron / proton / electron_negative / proton_negative` 四个 species，覆盖三种法向面、正负两种 `u_m` 符号，以及 `parse_flux_function` 与 `constant flux` 两类注入面；相对地，`analysis_flux_injection_3d.py` 会重建理论总权重 `Ntot`，再对四个 species 的法向/切向动量分量分别按 `gaussian_flux_dist` 或 `gaussian_dist` 做直方图 `np.allclose` 断言。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_embedded_boundary_em_particle_absorption_sh_factor_2`：已把这条名字上写成 3D `shape factor = 2` 的 baseline 从宽泛“对应 3D `shape factor = 2` 版本”压实为更精确的 3D name-vs-runtime mismatch，并写清当前输入虽然切到了 `geometry.dims = 3`，但仍把 `algo.particle_shape` 写成 `1`；相对地，共享 `analysis.py` 仍只是在 `3dcartesian` 分支上对整张时间平均 `divE_avg` 施加 `abs(divE_avg).max() <= 7e-11` 的无伪电荷约束。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_embedded_boundary_em_particle_absorption_sh_factor_1`：已把这条 3D `shape factor = 1` 无伪电荷 baseline 从宽泛“对应 3D `shape factor = 1` 版本”压实为更精确的 3D 时间平均消费者合同，并写清当前输入在公共基线上显式切到 `geometry.dims = 3`、`algo.particle_shape = 1`，同时让 `electron/positron` 对沿相反方向撞向圆柱 EB；相对地，共享 `analysis.py` 会对整段 openPMD `divE` 场序列做 `25..100` 时间平均，并在 `3dcartesian` 分支上直接要求 `abs(divE_avg).max() <= 7e-11`，不会像 RZ 版本那样额外屏蔽轴上单元。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_embedded_boundary_cube_macroscopic`：已把这条 3D 介质 cavity baseline 从宽泛“对应介质 cavity 模态版本”压实为更精确的 dielectric-frequency 消费者合同，并写清当前输入在公共 `inputs_base_3d` 之上显式切到 `algo.em_solver_medium = macroscopic`、`macroscopic.epsilon = 1.5*epsilon0`、`macroscopic.mu = mu0`、`macroscopic.sigma = 0`；相对地，共享 `analysis_fields.py` 会按测试名中的 `macroscopic` 分支把本征频率 `omega` 额外除以 `sqrt(1.5)`，再继续要求最终 `By/Bz` 的相对 `L2` 误差都小于 `1e-1`。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_embedded_boundary_cube`：已把这条 3D PEC cavity baseline 从宽泛“对应 PEC cavity 模态基准”压实为更精确的 TM\_{0,1,1} 模态消费者合同，并写清当前输入本体几乎只是直连 `inputs_base_3d`，而真正的 runtime 合同主要藏在基底里：stair-case `eb2.box_lo/hi = ±0.501` 构出的 PEC cubic cavity、统一 `warpx.eb_potential = 1` 的 electrostatic-solve 路径，以及 `m=0,n=1,p=1` 的 `By/Bz` 外加磁模初始化；相对地，`analysis_fields.py` 会逐点重建解析 `By_th/Bz_th` 并要求两者的相对 `L2` 误差都小于 `1e-1`。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_electrostatic_sphere_rel_nodal`：已把这条 3D collocated electrostatic baseline 从宽泛“对应 collocated 变体”压实为更精确的解析场消费者合同，并写清当前输入在公共 `inputs_base_3d` 之上唯一显式改动是打开 `warpx.grid_type = collocated`；相对地，共享 `analysis_electrostatic_sphere.py` 仍只对 `Ex/Ey/Ez` 施加解析场相对 `L2 < 0.05` 断言，而由于粒子记录里没有 `phi`，能量账本分支在这条路径上不会触发。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_electrostatic_sphere_lab_frame_mr_emass_10`：已把这条 3D lab-frame + MR + `emass_10` baseline 从宽泛“对应 lab-frame + MR 变体”压实为更精确的解析场消费者合同，并写清当前输入同时打开全域 MR、`electron.mass = 10` 和 `max_step = 2`，但又把 `diag2.electron.variables` 收缩到不含 `phi` 的版本；相对地，共享 `analysis_electrostatic_sphere.py` 会按测试名里的 `emass_10` 分支把解析场容差放宽到 `0.096`、并把解析解中的电子质量常数改成 `10`，而能量账本分支在这条路径上不会触发。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_electrostatic_sphere_lab_frame`：已把这条 3D lab-frame 自场膨胀 baseline 从宽泛“对应 lab-frame 变体”压实为更精确的 `phi`-gated 能量账本消费者合同，并写清当前输入在公共 `inputs_base_3d` 之上把 `warpx.do_electrostatic` 从 `relativistic` 改成 `labframe`，同时让 `diag2.electron.variables` 显式写出 `phi`；相对地，共享 `analysis_electrostatic_sphere.py` 会先对 `Ex/Ey/Ez` 施加解析场相对 `L2 < 0.05` 断言，并只在 openPMD 粒子记录确实带 `phi` 时继续要求 `Ep_f < 0.7 Ep_i` 且总能量漂移小于初态总能量的 `0.32%`。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_electrostatic_sphere_adaptive`：已把这条 3D adaptive-dt 自场膨胀 baseline 从宽泛“对应 adaptive-dt 变体”压实为更精确的 adaptive-`t_max` 消费者合同，并写清当前输入把固定步数推进改成 `stop_time = 60e-6`，同时打开 `warpx.cfl = 0.2`、`dt_update_interval = 10`、`max_dt = 1.5e-6` 和 `Timestep` reduced diag；相对地，共享 `analysis_electrostatic_sphere.py` 并不消费 reduced diag，而是直接用最终 plotfile 的 `current_time` 作为真实 `t_max`，再对 `Ex/Ey/Ez` 施加解析场相对 `L2 < 0.05` 断言。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_rz_electrostatic_sphere_uniform_weighting`：已把这条 RZ uniform-weighting 自场膨胀 baseline 从宽泛“对应 uniform-weighting 变体”压实为更精确的装填/analysis 双边界，并写清当前输入相对普通 RZ 版把 `num_particles_per_cell_each_dim` 从 `2 2 2` 提到 `6 2 2`，并额外打开 `electron.radial_numpercell_power = 1.`；与此同时，`analysis_electrostatic_sphere.py` 在解析 `Er/Ez` 相对 `L2 < 0.05` 断言保持不变的前提下，会按测试名 `endswith("uniform_weighting")` 把总能量漂移容差从 `0.0032` 放宽到 `0.012`。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_rz_embedded_boundary_em_particle_absorption_sh_factor_3`：已把这条名字和运行时一致的 RZ `shape factor = 3` baseline 从宽泛“对应 `shape factor = 3` 版本”压实为更精确的 shared-analysis 消费者合同，并写清当前命中的是共享 `analysis.py` 的同一条 openPMD 时间平均 `divE` 链；同时补清 `inputs_test_rz_embedded_boundary_em_particle_absorption_sh_factor_3` 确实把 `geometry.dims = RZ` 和 `algo.particle_shape = 3` 一起打开，所以这条回归当前命中的确是独立的 RZ `shape factor = 3` 运行时路径。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_rz_embedded_boundary_em_particle_absorption_sh_factor_2`：已把这条名字上写成 RZ `shape factor = 2` 的 baseline 从宽泛“对应 `shape factor = 2` 版本”压实为更精确的 name-vs-runtime mismatch，并写清当前命中的是共享 `analysis.py` 的同一条 openPMD 时间平均 `divE` 消费者链；同时补清 `inputs_test_rz_embedded_boundary_em_particle_absorption_sh_factor_2` 虽然切到了 `geometry.dims = RZ`，但仍把 `algo.particle_shape` 写成 `1`，所以这条回归当前并没有命中独立的 RZ `shape factor = 2` 运行时路径。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_rz_electrostatic_sphere_eb_mr`：已把这条 RZ+MR 固定电势圆柱 EB baseline 从宽泛“各 level 解析 `phi/Er`”压实为更精确的逐层 patch 消费者合同，并写清当前命中的是 `analysis_rz_mr.py` 先探测 `phi_lvl* / E_lvl*` 字段，再对每个 level 单独读取 patch、裁剪出真实 MR 活跃区，只在 `r > 0.1 + dr` 的 EB 外区域上构造解析 `phi=A+B log(r)`、`Er=-B/r`，并要求所有层上的 `phi_error/Er_error` 都小于 `4e-3`。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_rz_embedded_boundary_em_particle_absorption_sh_factor_1`：已把这条 RZ `shape factor = 1` 无伪电荷 baseline 从宽泛“时间平均 `divE`”压实为更精确的去轴时间平均消费者合同，并写清当前命中的是共享 `analysis.py` 用 `OpenPMDTimeSeries("./diags/diag1/")` 读取整段 `divE` 场序列，在 `25..100` 时间窗上取平均，对 RZ `thetaMode` 几何先把 `divE_avg[:, 13:19]` 的轴线邻域清零，再要求整张时间平均场满足 `abs(divE_avg).max() <= 4e-12`。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_rz_embedded_boundary_diffraction`：已把这条 RZ EB diffraction baseline 从宽泛“第一极小值角度”压实为更精确的衍射消费者合同，并写清当前命中的是 `analysis_fields.py` 在 `iteration 300` 读取 openPMD `E_x(r,z)`，对 `Ex**2` 做径向高斯平滑后提取第一极小值半径轨迹 `r_min(z)`，再与 Airy 预测 `theta = arcsin(1.22 * lambda / d) / 2` 对应的线性包络 `theta * z` 做逐 `z` 比较，并要求后半段始终满足 `abs(r_min(z) - theta * z) < 0.03`。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_rz_electrostatic_sphere_eb`：已把这条 RZ 固定电势圆柱 EB baseline 从宽泛“解析 `phi/Er`”压实为更精确的外域切片消费者合同，并写清当前命中的是 `analysis_rz.py` 从 level-0 `covering_grid` 读取整个 `phi/Er` 数组，按 `phi=A+B log(r)`、`Er=-B/r` 构造理论场，只在 `r > 0.1 + dr` 的 EB 外区域逐个半径切片计算整条 `z` 向上的最大相对误差，并要求 `errmax_phi/errmax_Er < 4.1e-3`，其中 `Er` 还显式排除了最后一层径向单元的插值误差。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_rz_electrostatic_sphere`：已把这条 RZ lab-frame 自场膨胀 baseline 从宽泛“解析 `Er/Ez` 与能量账本”压实为更精确的自洽膨胀消费者合同，并写清当前命中的是 `analysis_electrostatic_sphere.py` 先通过 `t_exact(r)` 反求膨胀半径 `r_end`，再沿 `r/z` 轴对 `Er/Ez` 施加相对 `L2 < 0.05` 的解析场断言；若 openPMD 粒子输出里存在 `phi`，则进一步要求 `Ep_f < 0.7 Ep_i` 且总能量漂移小于初态总能量的 `0.32%`。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_rz_collision`：已把这条 RZ e-e Coulomb collision baseline 从宽泛“近零净散射”压实为更精确的结果消费者合同，并写清当前命中的是 `analysis_collision_rz.py` 直接读取 `diags/diag1000000` 与 `diags/diag1000150` 的 `particle_momentum_x/y`，对所有粒子施加 `max(abs(px1-px2) + abs(py1-py2)) < 1e-15` 的首末横向动量不变断言。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_rz_point_of_contact_eb`：已把这条 RZ EB 接触几何 baseline 从宽泛“接触点、时间戳和法向”压实为更精确的 BoundaryScraping 解析几何消费者合同，并写清当前命中的是 `analysis.py` 直接从 `diags/diag2/particles_at_eb` 读取 `stepScraped`、`deltaTimeScraped`、`x/y/z`、`nx/ny/nz`，再与解析参考值逐项比对，要求 `x/y` 的相对误差小于 `0.1%`、时间戳与法向 `nx/ny` 的相对误差小于 `1%`，同时 `z/nz` 保持在 `1e-8` 量级以内。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_rz_scraping_filter`：已把这条 RZ `plot_filter_function` scraping baseline 从宽泛“半域筛选合同”压实为更精确的 BoundaryScraping 半域记录消费者合同，并写清当前命中的是 `analysis_rz_filter.py` 同时打开 `diag2` 与 `diag3/particles_at_eb` 的 openPMD 时间序列，对每个 iteration 验证“主容器剩余粒子数 + 2 * scraped 粒子数 = 初始总粒子数”，并进一步要求 scraped buffer 里的全部记录都满足 `z > 0`。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_rz_scraping`：已把这条 RZ EB scraping baseline 从宽泛“剩余粒子数、scraped 计数和 `id` 闭合”压实为更精确的 BoundaryScraping 消费者合同，并写清当前命中的是 `analysis_rz.py` 同时打开 `diag2` 与 `diag3/particles_at_eb` 的 openPMD 时间序列，对每个 iteration 验证“主容器剩余粒子数 + `stepScraped <= iteration` 的 scraped 粒子数 = 初始总粒子数”，并进一步要求初始全部 `id` 与“末态盒内 `id` + scraped buffer `id`”排序后完全一致。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_rz_projection_div_cleaner`：已把这条 RZ 文件外场 projection-cleaner baseline 从宽泛“对清理后离散 `divB` 的强断言”压实为更精确的柱坐标 `divB` 消费者合同，并写清当前命中的是 `analysis.py` 直接读取 `raw Bx_aux/Bz_aux`，按 `divB = (1/r) d(r Br)/dr + dBz/dz` 的 RZ 离散公式连同 `ru/rd` 面心半径修正重建散度，再对去掉一圈边界后的 interior `sqrt(sum(divB^2))` 施加 `< 4e-3` 的误差阈值。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_rz_pml_psatd`：已把这条 RZ `psatd + radial pml` baseline 从宽泛“残余场低于阈值”压实为更精确的 PML 消费者合同，并写清当前命中的是 `analysis_pml_psatd_rz.py` 先对 `yt` 数据集执行 `force_periodicity()`，再用 `covering_grid` 展开整个 level-0 全域 `Er/Ez` 数组，对单电子径向出射脉冲离域后的全域最大残余场 `max(max(|Er|), max(|Ez|))` 施加统一阈值 `< 2.0` 的断言。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_rz_flux_injection`：已把这条 RZ 方位向连续注入 baseline 从宽泛“半径带和总通量检查”压实为更精确的 RZ 注入消费者合同，并写清当前命中的是 `analysis_flux_injection_rz.py` 从 plotfile `current_time` 反推出 `Ntot = flux * emission_surface * t_max` 后要求 `w.sum()` 在 `5%` 相对误差内闭合，同时还对全部电子径向坐标施加 `1.48 <= r <= 1.92` 的窄半径带断言，用来锁定均匀 `Bz` 下的固定 Larmor 半径轨道。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_rz_flux_injection_from_eb`：已把这条 RZ EB flux-emission baseline 从宽泛“总通量、法向/切向速度分布和 EB 外位置检查”压实为更精确的 EB 发射消费者合同，并写清当前命中的是 `analysis_flux_injection_from_eb.py` 先用 `particle_theta` 把 RZ 输出重建成三维 `x/y/z`，再对总发射量 `Ntot = flux * 4 * pi * R^2 * t_inj`、`x^2+y^2+z^2 > (0.98R)^2` 的 EB 外位置边界，以及法向 `u_n` 与两条切向 `u_perp/u_perp2` 的理论 `gaussian_flux_dist` / `gaussian_dist` 加权直方图逐 bin `np.allclose` 合同。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_rz_laser_acceleration_opmd`：已把这条 RZ openPMD LWFA baseline 从宽泛“mesh shape、species ordering 和 `rho_<species>` 中心位置检查”压实为更精确的 openPMD 消费合同，并写清当前命中的是 `diags/diag1/openpmd_%T.h5` 的 iteration-count `=3`、`iteration 20` 上 `j_t=(3,512,64)`、`part_per_grid/rho_electrons` dataset shape，以及 `rho_electrons/rho_beam` mode-0 的 `z` 向质心顺序 `electron_meanz > 0, beam_meanz < 0` 这组联合断言。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_rz_ohm_solver_em_modes_picmi`：已把这条 RZ hybrid-PIC EM-modes baseline 从宽泛“频谱四点 assert”压实为更精确的频谱消费者合同，并写清当前 active CMake 实际命中的是 `--test` 分支：输入脚本会把参数对象 `dill` 到 `sim_parameters.dpkl` 并用 openPMD `field_diag` 落盘 `diags/field_diags`，随后 `analysis_rz.py` 对 `E_y` 做 Hankel + `z/t` 双 Fourier 生成完整 `F_kw` 频谱，再在 test 模式下抽取 `F_kw[2,1,...]` 的四个振幅样本做 `np.allclose` 断言。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_rz_particle_boundary_interaction_picmi`：已把这条 RZ PICMI boundary-interaction baseline 从宽泛“镜面反射场景”压实为更精确的 callback-consumer 合同，并写清当前命中的是 `ParticleBoundaryBufferWrapper()` 驱动的 `afterstep` 镜面反射注入链，以及基于 `warpx_used_inputs` 重建 ray-sphere 撞击与解析反射轨道后，对 openPMD 末态电子位置要求 `x/z` 相对误差 `< 2%` 且 `y < 1e-8` 的消费者链。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_rz_silver_mueller_z`：已把这条 RZ Silver-Mueller baseline 从宽泛“`Er/Et/Ez` 残余场低于 `0.01 V/m`”压实为更精确的全域 plotfile 消费合同，并写清当前命中的是 `analysis.py` 通过 `yt.load + covering_grid` 展开 level-0 全域数组、解析 `warpx_used_inputs` 进入 RZ 分支后，对全部 `Er/Et/Ez` 单元逐一要求 `abs(field) < 0.01 V/m` 的消费者链。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_rz_secondary_ion_emission_picmi`：已把这条 RZ PICMI 次级电子发射 baseline 从宽泛“最终电子数与撞击点几何一致性”压实为更精确的 callback-consumer 合同，并写清当前命中的是 `ParticleBoundaryBufferWrapper()` 驱动的 `afterstep` 次级电子注入链，以及 openPMD 末态电子数 `=2` 加上按末速度反向传播后与解析离子撞击点相对距离 `< 2%` 的几何匹配消费者链。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_rz_spacecraft_charging_picmi`：已把这条 RZ PICMI spacecraft-charging baseline 从宽泛“analysis 检查 `v0/tau`”压实为更精确的 charging-consumer 合同，并写清当前命中的是 `ParticleBoundaryBufferWrapper()` 驱动的 EB 收集电荷回写链，以及 `OpenPMDTimeSeries` 对 `phi_min(t)` 做 `v0 * (1-exp(-t/tau))` 拟合后要求相对基准误差低于 `4%/20%` 的消费者链。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_rz_magnetostatic_eb_picmi`：已把这条 RZ PICMI magnetostatic EB baseline 从宽泛“初始化”压实为更精确的 magnetostatic-beampipe 合同，并写清当前显式断言命中的是 `sim.fields.get("Efield_aux", dir="r")` 与 `sim.fields.get("Bfield_aux", dir="theta")` 在 beampipe 中段的 `z` 向平均后，对解析 `Er(r)` / `B_theta(r)` 的最大相对误差阈值都 `< 2%`。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_rz_ohm_solver_cylinder_compression_picmi`：已把这条 RZ hybrid-PIC cylinder-compression baseline 从宽泛“覆盖 split external vector potential runtime 路径”压实为更精确的 test-mode consumer 合同，并写清当前 active CMake 实际命中的是 `--test` 分支：该分支会先生成 `Afield.h5`，把 `HybridPICSolver(A_external=...)` 同时接成 `uniform_file/uniform_analytical` 两条外加矢势通道并共用同一条时间门函数，同时启用 plotfile 粒子/场诊断并落盘到 `diags/diag1000020`。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_rz_laser_acceleration_picmi`：已把这条 RZ PICMI LWFA baseline 从宽泛“主要覆盖 RZ front-end 映射”压实为更精确的 front-end-to-diagnostics 合同，并写清当前显式命中的是 `write_input_file("inputs_rz_picmi") -> initialize_inputs() -> initialize_warpx() -> step(10)` 之后，`warpx_dump_rz_modes=1` 的 field diagnostic 与 `[electrons, beam]` 粒子 diagnostic 共同落盘到 `diags/diag1000010` 的消费者链。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_rz_langmuir_multi_picmi`：已把这条 RZ PICMI Langmuir baseline 从宽泛“主要覆盖 PICMI 前端配线”压实为更精确的 RZ multimode-field 合同，并写清当前显式断言命中的是 `sim.fields.get("Efield_aux", dir="r/z")` 取回的多模 `Er/Ez` 沿 `theta=0` 重组后，与解析 Langmuir 多模场解的最大相对误差阈值 `< 0.02`。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_projection_div_cleaner_callback_picmi`：已把这条 3D callback 外场 baseline 从宽泛“强 `divB` 断言在输入脚本尾部”压实为更精确的 callback-side projection-cleaner 合同，并写清当前显式断言命中的是 `LoadInitialFieldFromPython(..., warpx_do_divb_cleaning_external=True)` 把 current-loop 磁场写入 `Bfield_fp_external` 之后，直接从进程内 `Bfield_aux` 重建出的三维 interior `divB` 的 `L2` 误差阈值 `< 1e-12`。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_particle_scrape_picmi`：已把这条 3D PICMI EB scrape baseline 从宽泛“PICMI + Python buffer-wrapper 场景输出，不替代脚本内直接断言”压实为更精确的 dual-contract 边界，并写清当前强断言同时命中 `analysis_scrape.py` 的 `612 -> 0` 主容器删粒子合同，以及输入脚本尾部 `ParticleBoundaryBufferWrapper()` 的 `eb` buffer size、`stepScraped > 40`、跨 rank buffer 总数与 `clear_buffer()` 归零合同。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_projection_div_cleaner_picmi`：已把这条 3D openPMD 初始场 baseline 从宽泛“强 `divB` 断言在输入脚本尾部”压实为更精确的 projection-cleaner 合同，并写清当前显式断言命中的是 `LoadInitialField(...example-femm-3d.h5, load_E=False)` 导入初始磁场后，从 `raw Bx_aux/By_aux/Bz_aux` 重建出的三维 interior `divB` 的 `L2` 误差阈值 `< 1e-12`。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_embedded_boundary_picmi`：已把这条 3D PICMI EB wrapper baseline 从宽泛 `edge_lengths/face_areas` 运行期断言描述压实为更精确的 EB-wrapper 合同，并写清当前显式断言命中的是三个中截面的 perimeter `= 4 * L_cavity` 与切片面积 `= L_cavity^2 - 2 * dA` 的闭式几何对照。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_2d_projection_div_cleaner_initial_analytical_field_picmi`：已把这条 2D PICMI 解析外场 baseline 从宽泛“强 `divB` 断言在输入脚本尾部”压实为更精确的 projection-cleaner 合同，并写清当前显式断言命中的是 `raw Bx_aux/Bz_aux` 重建出的 interior `divB` 的 `L2` 误差阈值 `< 5e-12`。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_2d_runtime_components_picmi`：已把这条 2D `restart`/PICMI baseline 从宽泛“runtime components / checkpoint restart scaffold”压实为更精确的 restart-consistency contract，并写清当前显式断言命中的是 `newPid` runtime component 跨 checkpoint/restart 后的粒子总数、comp 索引和值一致性。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_2d_id_cpu_read_picmi`：已把这条 `restart` 目录下的 2D PICMI baseline 从宽泛 `idcpu` 读取描述压实为更精确的 unpack-contract 边界，并写清当前显式断言命中的是 checkpoint/restart 之后 `pti["idcpu"] -> unpack_ids/unpack_cpus` 的和式合同 `5050/0`。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_2d_prev_positions_picmi`：已把这条 2D `particle_data_python` baseline 从宽泛“runtime-attribute / Python iterator 自检”压实为更精确的 previous-position contract，并写清当前显式断言命中的是 `prev_x/prev_z` runtime comp 索引、`prev_z < zmax` 的数值边界，以及 iterator 计数与 `number_of_particles(only_local=True)` 的一致性。
- [x] 2026-05-24：继续清理 `docs/example-regression-map.md` 的 `test_2d_particle_attr_access_picmi`：已把这条 2D `particle_data_python` baseline 从宽泛“接口自检”压实为更精确的 particle-container contract，并写清当前显式断言命中的是注入总粒子数、`w/newPid` runtime real-comp 索引、自定义 `newPid` 写回，以及手动 `deposit_current(...)` 后 `current_fp` 的 `x/z` 分量非零。
- [x] 2026-05-24：继续清理 `docs/example-regression-map.md` 的 `test_2d_particle_reflection_picmi`：已把这条 2D `particle_boundary_process` baseline 从宽泛“scraped-buffer 时间戳自检”压实为更精确的 boundary-buffer 合同，并写清当前显式断言命中的是 `z_hi/z_lo` 缓冲粒子数 `63/67` 与 `stepScraped=4/8` 的精确计数，不只是抽象“发生了反射”。
- [x] 2026-05-24：继续清理 `docs/example-regression-map.md` 的 `test_2d_python_wrappers_picmi`：已把这条 2D `python_wrappers` baseline 从宽泛 checksum 描述压实为更精确的 wrapper-contract 边界，并写清当前显式断言命中的是 Python `MultiFabRegister` wrapper、valid-domain/PML 视图和 split-field component 解释合同，外层 checksum 只作附加基线。
- [x] 2026-05-24：继续清理 `docs/example-regression-map.md` 的 `test_2d_particle_attr_access_unique_picmi`：已把这条 nominal unique 变体从“测试名存在、行为分叉未真正生效”的宽泛描述压实为更精确的 name-vs-runtime 边界，并写清 `--unique` 当前没有流入 `add_particles(...)`，两条测试名实际都命中同一条 `unique_particles=True` 路径。
- [x] 2026-05-24：继续清理 `docs/example-regression-map.md` 的 `test_2d_background_mcc_picmi`：已把这条 2D PICMI `capacitive_discharge` baseline 从笼统“无独立 analysis”压实为更准确的 callback-solver 边界，并写清当前显式断言只保证 pseudo-1D external Poisson solver 确实被调用，放电物理本身仍主要依赖 checksum 基线。
- [x] 2026-05-24：继续清理 `docs/example-regression-map.md` 的 `test_1d_ionization_neutral_dsmc`：已把这条 1D `ionization_dsmc` baseline 从“需反查对应 inputs 和分析脚本”压实为更明确的 `inputs + analysis + checksum` 合同，并写清当前强断言只覆盖 `Hneutral/Hplus` 快束通量与截面理论的一致性，不单独验证电子产额或背景 `H2` 宏粒子统计。
- [x] 2026-05-24：继续细化 `amrex.parmparse.verbose`
  - 已补清这条更硬的 preemptive-override 反向边界：若某段运行时代码在第一次 `ParmParse::Verbose()` 之前先调用了 `ParmParse::SetVerbose(...)`，后续 `Verbose()` 会直接跳过 `query("verbose", "v", ...)`。
  - 已补清更细的运行态结论：因此输入文件里显式给出的 `amrex.parmparse.verbose` 当前可能完全不被这条 consumer 命中，并继续留在后续 unused-input 检查链里。

- [x] 2026-05-24：继续细化 `amrex.parmparse.verbose`
  - 已补清这条更硬的 runtime override 边界：`ParmParse::SetVerbose(int)` 当前只会直接改写缓存变量 `pp_detail::verbose`，不会回写 `ParmParse("amrex.parmparse")` table。
  - 已补清更细的运行态结论：因此运行中调用 `SetVerbose(...)` 会立刻改写后续 unused-input 明细打印 gate，但不会把这份 override 重新 materialize 成 parser entry。

- [x] 2026-05-24：继续细化 `amrex.use_profiler_syncs`
  - 已补清这条更硬的 communicator-scope 边界：`BLProfileSync::Sync()` 与 `StartSyncRegion()` 当前都统一调用 `ParallelDescriptor::Barrier(ParallelContext::CommunicatorSub())`。
  - 已补清更细的运行态结论：因此这条输入绑定的是当前 parallel context 的 sub-communicator barrier，不是无条件覆盖所有 MPI ranks 的全局同步。

- [x] 2026-05-24：继续细化 `amrex.abort_on_unused_inputs`
  - 已补清这条更硬的测试 harness consumer 边界：`Examples/CMakeLists.txt` 当前会在非 Python 测试路径里直接注入 `amrex.abort_on_unused_inputs = 1`。
  - 已补清更细的运行态结论：因此它不只是用户手动开启的 runtime 开关，也是本地示例/回归测试默认使用的收尾 unused-input 契约。

- [x] 2026-05-24：继续细化 `ablastr.fillboundary_always_sync`
  - 已补清这条更硬的主域/PML 不对称边界：在普通精度下，同一次 `FillBoundaryE/B` 调用里，valid-domain 主域分支已经旁路 helper，但 `pml->FillBoundary(...)` / `pml_rz->FillBoundary{E,B}(...)` 仍会继续转进 helper。
  - 已补清更细的运行态结论：因此这条输入当前可以把同一次 `E/B` 调用里的 PML guard-cell 填边抬成 sync，而主域那一半仍停留在 `nodal_sync` 实参主导的 direct-AMReX 分支。

- [x] 2026-05-24：继续细化 `warpx.safe_guard_cells`
  - 已补清这条更硬的 full-diagnostics consumer 边界：safe 模式抬高 `ng_UpdateAux` 后，`FullDiagnostics::PrepareFieldDataForOutput()` 里的 `FillBoundaryAux(warpx.getngUpdateAux())` 也会直接消费同一份放大预算。
  - 已补清更细的运行态结论：当前不存在 diagnostics-local 的另一套 auxiliary-field guard-cell 合同；full diagnostics 输出前的 aux 填边与主推进链共用同一份 `ng_UpdateAux`。

- [x] 2026-05-24：继续细化 `amr.plot_headerversion / checkpoint_headerversion`
  - 已补清这条更硬的 read-side 反向边界：这组输入当前只绑定 writer-side 的临时 `VisMF::currentVersion`，不会回流到 `VisMF::Read(...)`。
  - 已补清更细的运行态结论：restart/plotfile 读回时真正决定 reader 分支的是磁盘 `*_H` 头里反序列化出来的 `hdr.m_vers`，不是本次运行再给的 `amr.*_headerversion`。

- [x] 2026-05-24：继续细化 `ablastr.fillboundary_always_sync`
  - 已补清这条更硬的 `OverrideSync` 旁路边界：同命名空间里的 `OverrideSync(amrex::MultiFab&, ...)` 当前完全不读取 `fillboundary_always_sync`。
  - 已补清更细的运行态结论：因此这条输入不是“所有 nodal 同步语义”的统一总开关；owner-mask 驱动的 `OverrideSync` 路径会独立旁路它。

- [x] 2026-05-24：继续细化 `warpx.safe_guard_cells`
  - 已补清这条更硬的 charge/current 反向边界：safe 模式当前不会回头抬高 `ng_alloc_J`、`ng_alloc_Rho`、`ng_depos_J` 或 `ng_depos_rho`。
  - 已补清更细的运行态结论：`n_current_deposition_buffer` 与 `AllocLevelMFs(..., ng_alloc_J, ng_alloc_Rho, ...)` 仍继续消费原来的 `J/rho` 预算，因此它不是“把所有 halo 一起抬到最保守模式”的统一总开关。

- [x] 2026-05-24：继续细化 `warpx.serialize_initial_conditions`
  - 已补清这条更硬的 cleanup-lifecycle 反向边界：这条开关当前不会把 `Invalid` 粒子的清理时机前移。
  - 已补清更细的运行态结论：startup 仍是在 `AddParticles(0)` 后统一 `Redistribute()`，运行期 continuous injection 产生的无效候选仍要等 `WarpXEvolve.cpp` 外层统一 `mypc->Redistribute()` 才真正离开容器。

- [x] 2026-05-24：继续细化 `warpx.serialize_initial_conditions`
  - 已补清这条更硬的 ID-space 反向边界：源码当前会先按每个 tile 的 `max_new_particles` 预留整段 `NextID()` 区间，再把无效候选改写成 `ParticleIdCpus::Invalid`。
  - 已补清更细的运行态结论：因此这条开关即便稳定了 tile 级取号顺序，也不会让最终存活粒子的 ID 变成按存活数紧密连续的编号。

- [x] 2026-05-24：继续细化 `warpx.serialize_initial_conditions`
  - 已补清这条更硬的并行粒度边界：`serialize_initial_conditions=1` 当前只会关掉外层 `MFIter` 的 OMP team。
  - 已补清更细的运行态结论：tile 内部的 `amrex::ParallelFor(...)`、`Scan::ExclusiveSum(...)`、`ParallelForRNG(...)` 创建链仍会继续执行，不会被一并降成逐粒子串行。

- [x] 2026-05-24：继续细化 `amr.plot_headerversion / checkpoint_headerversion`
  - 已补清这条更硬的 parser-range 边界：`AMReX_Amr.cpp` 当前不会对 `phvInt/chvInt` 做独立范围校验，而是直接 `static_cast` 到 `VisMF::Header::Version`。
  - 已补清更细的运行态结论：因此常规 `Amr` writer 现在不只接受常见 `1/2`，也能继续 materialize `NoFabHeaderMinMax_v1 (3)` 与 `NoFabHeaderFAMinMax_v1 (4)` 这类更少见的 `VisMF` 头部合同。

- [x] 2026-05-24：继续细化 `amrex.use_profiler_syncs`
  - 已补清这条更硬的 unused-input 反向边界：在完全无 BL/Tiny profiling 的构建里，这条键由于唯一 `queryAdd("use_profiler_syncs", ...)` consumer 缺席，会继续停留在 `ParmParse` table。
  - 已补清更细的运行态结论：因此它不只失去 profiler barrier effect；若同时开启 unused-input 检查链，也会被当成未消费输入处理。

- [x] 2026-05-24：继续细化 `amrex.use_profiler_syncs`
  - 已补清这条更硬的 no-profiling 反向边界：若构建时既没有 `BL_PROFILING` 也没有 `AMREX_TINY_PROFILING`，`BLProfileSync::InitParams()` 当前根本不会被初始化宏链调用到。
  - 已补清更细的运行态结论：因此这条输入不只是“没有 profiler barrier effect”，而是连 `queryAdd("use_profiler_syncs", ...)` 都不会命中，本地 profiling 链不会消费它。

- [x] 2026-05-24：继续细化 `<reduced_diags_name>.type`
  - 已补清这条更硬的 startup-side header contract 分叉：2D openPMD 类型虽然继承了 `ReducedDiags` 基类的文本文件预创建/`m_write_header` 初始化动作，但不会真正消费这套文本 header 合同。
  - 已补清更细的运行态结论：大多数文本类型会在构造函数里利用 `m_write_header` 补写 header row，而 2D openPMD 类型会把真实 writer 延后到后续的 series 路径。

- [x] 2026-05-24：继续细化 `<reduced_diags_name>.type`
  - 已补清这条更硬的 writer-schema 分叉：同样经过 reduced-diags manager fanout，不同 `type` 当前会决定同一步是落一行文本、多行 probe 文本，还是完全改走 openPMD series。
  - 已补清更细的运行态结论：未覆写 `WriteToFile()` 的类型会继承统一 `step,time,m_data...` 单行 schema，而 `FieldProbe`、`LoadBalanceCosts`、2D openPMD 类型都会改写这条基线。

- [x] 2026-05-24：继续细化 `warpx.reduced_diags_names`
  - 已补清这条更硬的 checkpoint 域不对称：reduced-diags manager 当前只在 IO rank 上写 checkpoint 状态。
  - 已补清更细的运行态结论：restart 时 `ReadCheckpointData()` 没有对应的 IO-rank gate，会在所有 ranks 上 fanout 读回。

- [x] 2026-05-24：继续细化 `<diag_name>.average_start_step`
  - 已补清这条更硬的负起点反向边界：`fixed_start` 当前只拒绝 `0`，不拒绝负值。
  - 已补清更细的运行态结论：由于 static runtime gate 缺席，这类负起点不会在后续运行链里再次被拦下，只会作为成员态和 warning 文案插值继续存在。

- [x] 2026-05-24：继续细化 `<diag_name>.average_period_time`
  - 已补清这条更硬的一次性量化边界：`dynamic_start` 下这条物理时间窗口只会在初始化时做一次 `round(time/dt)`。
  - 已补清更细的运行态结论：后续 step-loop、flush 和初始化日志都只继续消费量化后的 `m_average_period_steps`，不再按原始时间值驱动窗口。

- [x] 2026-05-24：继续细化 `<diag_name>.time_average_mode`
  - 已补清这条更硬的同-step writer 去重边界：`TimeAveraged` diagnostics 当前在单个 PIC step 内最多只会真正 flush 一次。
  - 已补清更细的运行态结论：`DoDump()` 首次命中后就会置 `m_already_done=true`，因此不会在同一步再写第二份“瞬时版/平均版”输出。

- [x] 2026-05-24：继续细化 `<diag_name>.average_period_steps`
  - 已补清这条更硬的 `force_flush` 反向边界：`TimeAveraged` diagnostics 被强制写出时，源码不会按已累计的实际步数重标定平均值。
  - 已补清更细的运行态结论：当前仍会直接用完整的 `m_average_period_steps` 做归一化，因此 partial window 会以“部分累计和 / 完整 period 长度”的形式落盘。

- [x] 2026-05-24：继续细化 `<diag_name>.dt_snapshots_lab`
  - 已补清这条更硬的 restart 反向边界：BTD 续跑时 `InitializeBufferData(..., restart=true)` 不会按当前输入重算 `m_t_lab`。
  - 已补清更细的运行态结论：源码会从 checkpoint header 逐 buffer 恢复旧的 `tlab`，并继续沿用这份时间轴。

- [x] 2026-05-24：继续细化 `<diag_name>.dt_snapshots_lab`
  - 已补清这条更硬的缓存化生命周期边界：BTD 初始化一旦把它写进各 buffer 的 `m_t_lab[i_buffer]`，后续运行态就不再每步直接回读 `m_dt_snapshots_lab`。
  - 已补清更细的运行态结论：step-loop、粒子 functor 和 flush 继续消费的是这份缓存下来的 snapshot 时间轴。

- [x] 2026-05-24：继续细化 `<diag_name>.do_back_transformed_fields`
  - 已补清这条更硬的 writer-side 反向边界：字段侧 BTD 关掉后，snapshot 首次 flush 仍会创建 `Level_0` 和粒子子目录并搬运 `WarpXHeader/warpx_job_info`。
  - 已补清更细的运行态结论：真正被截掉的是后面的 `Cell_H/Cell_D_*` 合并链，而不是整个 snapshot plotfile 骨架创建。

- [x] 2026-05-24：继续细化 `<diag_name>.do_back_transformed_particles`
  - 已补清这条更硬的跨实例残留边界：本实例若最终把粒子侧 BTD 覆写成 `false`，源码不会反向调用 disable。
  - 已补清更细的运行态结论：它也不会删除先前已挂到物种容器上的 `*_n_btd` 历史态 comps。

- [x] 2026-05-24：继续细化 `<diag_name>.buffer_size`
  - 已补清这条更硬的判满合同：BTD 当前不是直接用 `m_buffer_counter == m_buffer_size` 判满。
  - 已补清更细的运行态结论：源码真正通过 `k_index_zlab == m_buffer_box.smallEnd` 这条几何命中条件触发 flush，`m_buffer_counter` 只稳定参与 empty/reset 语义。

- [x] 2026-05-24：继续细化 `<diag_name>.dz_snapshots_lab`
  - 已补清这条更硬的 companion override 边界：BTD 当前不会把 `dz_snapshots_lab` 与 `dt_snapshots_lab` 当成互斥输入。
  - 已补清更细的运行态结论：若两者同时给定，源码会先读 `dt`，再让 `dz / moving_window_v` 直接覆写 `m_dt_snapshots_lab`。

- [x] 2026-05-24：继续细化 `<diag_name>.num_snapshots_lab`
  - 已补清这条更硬的时序边界：`num_snapshots_lab=0` 当前不只是把 BTD buffer 拓扑变空。
  - 已补清更细的运行态结论：它会更早在 `DerivedInitData()` 的 `GetFinalIteration().back()` 无保护访问上失效，连后面的 `max_step/stop_time` 自动补齐链都走不到。

- [x] 2026-05-24：继续细化 `<reduced_diags_name>.openpmd_backend / file_min_digits`
  - 已补清这条更硬的目录准备边界：`ReducedDiags` 基类当前只显式创建公共 `m_path`。
  - 已补清更细的运行态结论：`DifferentialLuminosity2D` 自己也不会先 `mkdir m_path + m_rd_name/`，而是直接把该子路径交给 `io::Series(..., CREATE)`。

- [x] 2026-05-24：继续细化 `<reduced_diags_name>.openpmd_backend / file_min_digits`
  - 已补清这条更硬的目录准备边界：`ReducedDiags` 基类当前只显式创建公共 `m_path`。
  - 已补清更细的运行态结论：`ParticleHistogram2D` 自己不会先 `mkdir m_path + m_rd_name/`，而是直接把该子路径交给 `io::Series(..., CREATE)`。

- [x] 2026-05-24：继续细化 `<reduced_diags_name>.openpmd_backend / file_min_digits`
  - 已补清这条更硬的 payload-schema 边界：`ParticleHistogram2D` 当前不是固定 `double` 写 openPMD。
  - 已补清更细的运行态结论：源码会直接 `resetDataset(io::determineDatatype<amrex::ParticleReal>())`，让磁盘数值 schema 跟随 `ParticleReal` 构建精度漂移。

- [x] 2026-05-24：继续细化 `<reduced_diags_name>.openpmd_backend / file_min_digits`
  - 已补清这条更硬的 payload-schema 边界：`DifferentialLuminosity2D` 当前不是跟随 `ParticleReal` 构建精度写 openPMD。
  - 已补清更细的运行态结论：源码会直接 `resetDataset(io::determineDatatype<double>())`，把磁盘数值 schema 硬钉死为 `double`。

- [x] 2026-05-24：继续细化 `warpx.write_diagnostics_on_restart`
  - 已补清这条更硬的 full-vs-reduced 不对称：restart 首帧补写里，full diagnostics 继续各自走 `DoComputeAndPack/DoDump` 的早期 gate。
  - 已补清更细的运行态结论：reduced diagnostics 则会先全实例 `ComputeDiags()`，再按 `intervals` 过滤 `WriteToFile()`。

- [x] 2026-05-24：继续细化 `<reduced_diags_name>.histogram_function(t,x,y,z,ux,uy,uz)`
  - 已补清这条更硬的 writer-family metadata 不对称：1D `ParticleHistogram` 当前只把 axis 定义间接 materialize 成 bin-center 文本列，不保留原始 parser 字符串。
  - 已补清更细的运行态结论：2D `ParticleHistogram2D` 则会把原始 axis 表达式显式写进 openPMD metadata。

- [x] 2026-05-24：继续细化 `<reduced_diags_name>.value_function/filter_function(t,x,y,z,ux,uy,uz,w)`
  - 已补清这条更硬的 writer-side identity contract：`value_function` 当前不仅不会写回 attribute，也不会改变 openPMD 记录身份。
  - 已补清更细的运行态结论：不同表达式都还是固定写到 `meshes["data"][SCALAR]`，只改 payload 数值，不会生成新的 mesh/component 名。

- [x] 2026-05-24：继续细化 `<reduced_diags_name>.filter_function(t,x,y,z,ux,uy,uz)`
  - 已补清这条更硬的 writer-side metadata 不对称：1D `ParticleHistogram` 当前不会把 filter 表达式写回文本结果。
  - 已补清更细的运行态结论：2D `ParticleHistogram2D` 则会把 `filter_string` 显式写成 openPMD mesh attribute `filter`。

- [x] 2026-05-24：继续细化 `<reduced_diags_name>.normalization`
  - 已补清这条更硬的 rank 不对称：`ParticleHistogram` 的 `max_to_unity / area_to_unity` 当前虽然发生在 `ReduceRealSum(..., IOProcessorNumber())` 之后，但 non-IO rank 继续归一化的是各自未归约的本地快照。
  - 已补清更细的运行态结论：后续真正会被 `MultiReducedDiags::WriteToFile()` 落盘的仍只有 IO rank 那一份全局结果。

- [x] 2026-05-24：继续细化 `<reduced_diags_name>.bin_number / bin_min / bin_max`
  - 已补清这条更硬的输出轴语义不对称：1D `DifferentialLuminosity` 文本 header 当前直接把每列写成 bin center。
  - 已补清更细的运行态结论：2D `DifferentialLuminosity2D` openPMD metadata 则把 `bin_min_*` 写成 lower edge，再配合 `position={0.5,0.5}` 隐式表达 cell center，而不是写成同样的中心值标签。

- [x] 2026-05-24：继续细化 `reduced_diags.intervals`
  - 已补清这条更硬的 writer-family 不对称：同一步再次命中写出链时，1D `DifferentialLuminosity` 会落回 `ReducedDiags::WriteToFile()` 的 `ofstream(..., app)` 文本 append 路径。
  - 已补清更细的运行态结论：2D `DifferentialLuminosity2D` 则会重建 `io::Series(..., CREATE)` 并再次定位到同一个 `iterations[step+1]`，而不是生成第二个步号。

- [x] 2026-05-24：继续细化 `reduced_diags.intervals`
  - 已补清这条更硬的 cumulative-snapshot 边界：`DifferentialLuminosity` 与 `DifferentialLuminosity2D` 当前在命中 interval 后只做拷贝与归约，不会清零 `d_data / m_d_data_2D`。
  - 已补清更细的运行态结论：每次写出的都是自启动以来累计到当前步的总 luminosity 快照，而不是上一个输出区间的增量。

- [x] 2026-05-24：继续细化 `reduced_diags.intervals`
  - 已补清这条更硬的 IO-target reduction 不对称：`DifferentialLuminosity` 与 `DifferentialLuminosity2D` 当前虽然都会在命中 interval 后先做 device-to-host 拷贝，但 `ReduceRealSum(..., IOProcessorNumber())` 只会把全局归约结果 materialize 到 IO rank 的 host 缓冲。
  - 已补清更细的运行态结论：非 IO ranks 随后最多只保留各自的本地 host 快照，并不会拿到同一份全局 histogram/table。

- [x] 2026-05-24：继续细化 `<reduced_diags_name>.species`
  - 已补清这组更硬的 `min_N` 缩放命中范围边界：`DifferentialLuminosity` 与 `DifferentialLuminosity2D` 当前只有通过 bin gate 的 sampled pair 才会把 `min_N` 乘进 luminosity 增量。
  - 已补清更细的运行态结论：超出 histogram 范围的 sampled pair 会先被 `continue` 丢弃，不会再通过另一条独立的 cell-total 补偿链把对应的 `min_N` 权重补回。

- [x] 2026-05-24：继续细化 `<reduced_diags_name>.species`
  - 已补清这组更硬的 stride-pairing 不对称：`DifferentialLuminosity` 与 `DifferentialLuminosity2D` 当前按 `k += min_N` 走 residue-class 配对。
  - 已补清更细的运行态结论：当 `NI1 != NI2` 时，较小物种一侧的同一组起始 residue class 会在 loop 内被复用去配多个较大物种粒子；只有 `NI1 == NI2` 时两边才会同步一一前进。

- [x] 2026-05-24：继续细化 `<reduced_diags_name>.species`
  - 已补清这组更硬的 cell-local pairing short-circuit：`DifferentialLuminosity` 与 `DifferentialLuminosity2D` 当前会先把每个 cell 的独立 pair 数压成 `min(NI1, NI2)`。
  - 已补清更细的运行态结论：只要任一物种在该 cell 缺席，这个 cell 的独立 pair 数就直接为 `0`，不会进入后面的 pair `ParallelFor` 主链，也不会贡献 luminosity。

- [x] 2026-05-24：继续细化 `<reduced_diags_name>.species`
  - 已补清这组更硬的 AMR 反向边界：`DifferentialLuminosity` 与 `DifferentialLuminosity2D` 当前的遍历上界只看 `species_1.finestLevel()+1`。
  - 已补清更细的运行态结论：若 species 2 独有更细 level，这些 finer levels 当前不会进入 pairing / luminosity 累积链；源码不会再单独为 species 2 开一轮 finer-level 遍历。

- [x] 2026-05-24：继续细化 `<reduced_diags_name>.species`
  - 已补清这组更硬的双束运行态不对称：`DifferentialLuminosity` 与 `DifferentialLuminosity2D` 当前不是对两束 species 做完全对称的 level/tile 遍历。
  - 已补清更细的运行态结论：源码先用 `species_1.finestLevel()+1` 决定 `nlevs`，再只对 `species_1.MakeMFIter(lev)` 开 `mfi` 主链，species 2 则被假定能按同一组 `(lev,mfi)` 布局直接 `ParticlesAt(lev, mfi)` 对齐访问。

- [x] 2026-05-24：继续细化 `<reduced_diags_name>.weighting_function(x,y,z)`
  - 已补清这组更硬的 eager-evaluation 边界：`ChargeOnEB` 当前不会先检查 `local_integral_contribution == 0` 再决定是否调用 parser。
  - 已补清更细的运行态结论：只要命中 partial cell 且打开 weighting，就会先求 `fun_weightingparser(x,y,z)`；源码没有“零贡献面元跳过 parser”的快路径。

- [x] 2026-05-24：继续细化 `<reduced_diags_name>.weighting_function(x,y,z)`
  - 已补清这组更硬的 writer-side 反向边界：`ChargeOnEB` 当前不会把权重表达式写回 header 或输出元数据。
  - 已补清更细的运行态结论：构造函数写出的文本 header 只有 `step / time / Charge (C)`，后续基类 writer 也只追加 `m_data[0]`，所以结果文件本身不会显式保留用了哪条 `w(x,y,z)`。

- [x] 2026-05-24：继续细化 `<reduced_diags_name>.openpmd_backend / file_min_digits`
  - 已补清 `DifferentialLuminosity2D` 这组更硬的 writer lifecycle 边界：当前不会把 `io::Series` 保存在成员态里跨输出步复用。
  - 已补清更细的运行态结论：每次 `WriteToFile()` 都会重新 `io::Series(filepath, io::Access::CREATE)`，并在同次调用里显式 `series.flush(); i.close(); series.close();`。

- [x] 2026-05-24：继续细化 `<reduced_diags_name>.openpmd_backend / file_min_digits`
  - 已补清这组更硬的 writer lifecycle 边界：`ParticleHistogram2D` 当前不会把 `io::Series` 保存在成员态里跨输出步复用。
  - 已补清更细的运行态结论：每次 `WriteToFile()` 都会重新 `io::Series(filepath, io::Access::CREATE)`，并在同次调用里显式 `series.flush(); i.close(); series.close();`。

- [x] 2026-05-24：继续细化 `<reduced_diags_name>.integrate`
  - 已补清这组更硬的 checkpoint 生命周期边界：`MultiReducedDiags` 虽会统一 fanout `WriteCheckpointData()/ReadCheckpointData()`，但 `FieldProbe` 当前没有覆盖这两条 virtual。
  - 已补清更细的运行态结论：`integrate = 1` 的 running integral 虽然保存在 probe 粒子 SoA 上，却会继续落回 `ReducedDiags` 的空 checkpoint 实现，不会经 reduced-diag checkpoint 链被单独持久化或恢复。

- [x] 2026-05-24：继续细化 `<reduced_diags_name>.interp_order`
  - 已补清这组更硬的下限运行态边界：`FieldProbe` 当前没有独立的 lower-bound gate，而 `doGatherShapeN(...)` 顶层 helper 也没有 `else abort`。
  - 已补清更细的运行态结论：若显式给 `interp_order = 0` 或负值，`FieldProbe::ComputeDiags()` 里预先置零的 `Exp/Eyp/Ezp/Bxp/Byp/Bzp` 不会命中任何 `1..4` gather 分支，因此会静默保留为零。

- [x] 2026-05-24：继续细化 `<reduced_diags_name>.target_normal_*/target_up_*/detector_radius`
  - 已补清这组更硬的零模长风险边界：`FieldProbe` 当前没有独立的非零法向 / 非零 up 向量校验链。
  - 已补清更细的运行态结论：若任一输入向量模长为 `0`，`FieldProbe.H::normalize(...)` 不会先拒绝，而是会直接执行 `x /= mag; y /= mag; z /= mag` 并走到除以 `0`。

- [x] 2026-05-24：继续细化 `<reduced_diags_name>.resolution`
  - 已补清这组更硬的下限风险边界：`FieldProbe` 当前没有独立的 `m_resolution > 1` 校验链。
  - 已补清更细的运行态结论：若显式给 `resolution = 1`，`Line/Plane` 路径不会先被拒绝，而是会直接把 `DetLineStepSize / SideStepSize / UpStepSize` 送进除以 `m_resolution - 1 = 0`。

- [x] 2026-05-24：继续细化 `<reduced_diags_name>.normalization`
  - 已补清这组更硬的符号边界：`area_to_unity` 当前只接受正面积，不按 `abs(f_area)` 归一化。
  - 已补清更细的运行态结论：若上游 `bin_max < bin_min` 把 `m_bin_size` 翻成负号，它会静默保留未归一化分布，不会做符号修正或退回其它模式。

- [x] 2026-05-24：继续细化 `<reduced_diags_name>.value_function/filter_function(t,x,y,z,ux,uy,uz,w)`
  - 已补清这组更硬的空 parser 运行态边界：`compileParser(nullptr)` 当前不会直接 abort；若缺失 `value_function`，空 `ParserExecutor` 被调用时会返回 `numeric_limits<double>::max()`。
  - 已补清更细的运行态结论：因此这条缺失输入当前不是优雅 fallback，而是会把极大权重静默引入 bin 累加链；同时源码仍会先求 `weight = fun_valueparser(...)`，再判 `bin_abs/bin_ord` 是否越界。

- [x] 2026-05-24：继续细化 `<reduced_diags_name>.bin_number / bin_min / bin_max`
  - 已补清这组更硬的 1D 容器 shape 反向边界：`DifferentialLuminosity` 与 `ParticleHistogram` 当前都会把 `m_bin_num` 直接送进 `m_data.resize(...)`。
  - 已补清更细的运行态结论：若显式给负值，这条输入不会先被拒绝，而是直接参与 1D 容器 shape 初始化，而不只是停留在“坏的物理分箱语义”。

- [x] 2026-05-24：继续细化 `reduced_diags.separator`
  - 已补清这组更硬的 hostname companion 反向边界：`LoadBalanceCosts` 的 hostname gather/tokenize 链固定用空格缓冲和 `Tokenize(..., " ")`，不消费 `m_sep`。
  - 已补清更细的运行态结论：即便用户把文本列分隔符改成逗号、制表符或多字符串，这条 rank-to-hostname 辅助字符串链也不会跟着变化。

- [x] 2026-05-24：继续细化 `reduced_diags.extension`
  - 已补清这组更硬的 parser-to-path synthesis 反向边界：源码当前没有独立的 `m_extension.empty()` 校验或 fallback。
  - 已补清更细的运行态结论：若显式给空字符串，文本 reduced-diag 路径不会回退默认 `txt`，而是直接合成为 `rd_name + "."`，`LoadBalanceCosts` 的临时文件也会变成 `.tmp.`。

- [x] 2026-05-24：继续细化 `reduced_diags.precision`
  - 已补清这组更硬的 parser-to-writer 反向边界：`queryWithParser(...)` 会把表达式结果直接写进 `m_precision`，但源码当前没有独立的 `m_precision > 0` 校验链。
  - 已补清更细的运行态结论：显式给出 `0` 或负值时，这条输入不会先回退默认 `14`，而是直接流入基类 `std::setprecision(m_precision)`。

- [x] 2026-05-24：继续细化 `reduced_diags.intervals`
  - 已补清这组更硬的 2D writer override-side 不对称边界：`DifferentialLuminosity2D::WriteToFile()` 会再次自检 `m_intervals.contains(step+1)`。
  - 已补清更细的运行态结论：`ParticleHistogram2D::WriteToFile()` 当前没有这层自检，只完全依赖外层 `MultiReducedDiags::WriteToFile(step)` 的 fanout 过滤。

- [x] 2026-05-24：继续细化 `reduced_diags.path`
  - 已补清这组更硬的 2D openPMD writer manager-side 反向边界：`MultiReducedDiags::WriteToFile()` 会先把整条 writer fanout 压成 IO-rank-only。
  - 已补清更细的运行态结论：`m_path + m_rd_name + "/" + filename` 当前 materialize 的是 IO rank 单独创建的 series 路径，而不是多 rank collective writer 域。

- [x] 2026-05-24：继续细化 `reduced_diags.intervals`
  - 已补清这组更硬的 manager-side short-circuit 边界：`MultiReducedDiags::DoDiags(step)` 当前不是每步无条件遍历所有实例再汇总。
  - 已补清更细的运行态结论：源码写成 `result = result || ...`，所以一旦前面已有实例命中，后续实例在这一轮预判里会被 C++ `||` 短路，不再调用各自的 `DoDiags(step)`。

- [x] 2026-05-24：继续细化 `amrex.async_out`
  - 已补清这组更硬的 zero-barrier fast-path：只要某个 file-group 满足 `nspots == 1`，当前就会同时令 `Wait()/Notify()` 的 barrier 次数退化成 `0`。
  - 已补清更细的运行态结论：这类单-rank file-group 会完全绕开 `Abarrier/Waitall`；即便走在 communicator 分支里，也不会真正发起任何 group-local barrier。

- [x] 2026-05-24：继续细化 `amrex.async_out`
  - 已补清这组更硬的 turn-order 边界：同一 file-group 内当前不是对称 barrier，而是按 `ispot = 0, 1, ..., nspots-1` 形成线性串行链。
  - 已补清更细的运行态结论：最前面的 rank 不等别人，最后面的 rank 不再通知后继；中间 ranks 则各自等待前驱并通知后继。

- [x] 2026-05-24：继续细化 `amrex.async_out`
  - 已补清这组更硬的 barrier-domain 边界：`Wait()/Notify()` 里的 `Abarrier(s_comm)` 当前只覆盖与当前 rank 共享同一个 `s_info.ifile` 的 file-group ranks。
  - 已补清更细的运行态结论：源码不会跨所有 async-output ranks 建全局 barrier；当前 barrier domain 就是单个 file-group communicator。

- [x] 2026-05-24：继续细化 `amrex.async_out`
  - 已补清这组更硬的 MPI-thread gate 边界：`MPI_THREAD_MULTIPLE` 当前不是“只要打开 async_out 就必须满足”的全局前提。
  - 已补清更细的运行态结论：源码只在 `async_out_nfiles < nprocs` 时执行 `MPI_Query_thread(...)` 并检查 abort gate；`nfiles == nprocs` 的 per-rank async write 分支不会命中这条前提。

- [x] 2026-05-24：继续细化 `amrex.async_out`
  - 已补清这组更硬的 static group-binding 边界：同一进程当前不是每个 async job 再动态挑 file-group，而是在 `Initialize()` 时一次性固定 `s_info.ifile` 和对应 communicator。
  - 已补清更细的运行态结论：后续 `Wait()/Notify()` 都只复用这份静态 `s_info/s_comm`；不存在不同 async job 之间反复切换 file-group 的动态重绑定。

- [x] 2026-05-24：继续细化 `amrex.async_out`
  - 已补清这组更硬的 worker-topology 边界：每个 MPI 进程当前只有一个后台 worker 顺序 drain 本地 async job 队列。
  - 已补清更细的运行态结论：`BackgroundThread::BackgroundThread()` 只构造一个 `std::thread`，类内也只有单个 `m_thread`；当前不会在同一进程内再展开多个后台线程并行消费 `m_func`。

- [x] 2026-05-24：继续细化 `amrex.async_out`
  - 已补清这组更硬的 admission/execution 解耦边界：`do_job()` 当前在 `pop()` 完队首 job 后就立刻解锁，不是持锁跑完整个 job。
  - 已补清更细的运行态结论：某个 async job 正在执行时，新的 `Submit()` 仍可继续拿到 mutex 并向 `m_func` 入队；FIFO 约束的是出队顺序，不是提交窗口的全局冻结。

- [x] 2026-05-24：继续细化 `amrex.async_out`
  - 已补清这组更硬的 `Submit()` 队列边界：`AsyncOut::Submit()` 当前不是按 file-group 分拆的多队列调度。
  - 已补清更细的运行态结论：源码会先把所有 async field/particle job 串进同一个进程内 `std::queue` FIFO 后台队列；`Wait()/Notify()` 的 file-group 串行化是在 job 体内部后续发生的。

- [x] 2026-05-24：继续细化 `amrex.async_out`
  - 已补清这组更硬的 `Finish()` 清队列边界：`AsyncOut::Finish()` 当前不是简单“等后台线程空闲”。
  - 已补清更细的运行态结论：源码会先提交一个 `m_clearing=true` 的 sentinel job，再只等待“调用前已入队任务”和这条分界线被执行完；它不冻结之后新提交的任务。

- [x] 2026-05-24：继续细化 `amrex.async_out`
  - 已补清这组更硬的 finalize 顺序边界：`AsyncOut::Finalize()` 当前不是先 free communicator 再停后台线程。
  - 已补清更细的运行态结论：源码会先通过 `BackgroundThread` 析构里的 sentinel job 把已提交 async 写任务 drain 完并 `join()`，之后才 `MPI_Comm_free(s_comm)`。

- [x] 2026-05-24：继续细化 `amrex.async_out`
  - 已补清这组更硬的 communicator lifecycle 反向边界：`async_out=1` 当前并不必然建出 file-group communicator。
  - 已补清更细的运行态结论：只有 `async_out_nfiles < nprocs` 时才会 `MPI_Comm_split(...)` 并重写 `s_info`；若 `nfiles == nprocs`，后台线程虽会创建，但 `Wait()/Notify()` 会退化成 no-op。

- [x] 2026-05-24：继续细化 `amrex.async_out_nfiles`
  - 已补清这组更硬的 `ispot/nspots` 不均匀边界：`AsyncOut::GetWriteInfo(rank)` 当前不会把 ranks 切成完全等宽的 file groups。
  - 已补清更细的运行态结论：前 `nfull` 个文件组固定有 `nmaxspots` 个 writer turn，剩余文件组只有 `nmaxspots - 1` 个，所以 `Wait()/Notify()` 串行化长度会按 file group 不均匀分布。

- [x] 2026-05-24：继续细化 `particles.nreaders / nparts_per_read / datadigits_read / use_prepost`
  - 已补清这组更硬的 async 反向边界：`use_prepost` 这套 `*PrePost` 缓存当前只在 `WriteBinaryParticleDataSync(...)` 里被真正填充。
  - 已补清更细的运行态结论：`WriteBinaryParticleDataAsync(...)` 会在异步 lambda 内直接写 `Header`，但不会把 `HdrFileNamePrePost / nOutFilesPrePost / filePrefixPrePost / which/count/wherePrePost` 重新 materialize，所以这条开关当前主要绑定 sync 粒子 writer 的 post-cleanup 链。

- [x] 2026-05-24：继续细化 `warpx.field/particle_io_nfiles`
  - 已补清这组更硬的 async 反向边界：`particle_io_nfiles` 虽会上游桥接成 `particles.particles_nfiles`，但当前只有 `WriteBinaryParticleDataSync(...)` 会继续真正读取它。
  - 已补清更细的运行态结论：一旦命中 `AsyncOut::UseAsyncOut()`，粒子 writer 就直接分流到 `WriteBinaryParticleDataAsync(...)`，并改由 `AsyncOut::GetWriteInfo(rank).ifile` 决定 header file number 与实际数据文件名。

- [x] 2026-05-24：继续细化 `particles.particles_nfiles`
  - 已补清这组更硬的 sync/async 分叉：只有 `WriteBinaryParticleDataSync(...)` 会显式 `queryAdd("particles_nfiles", ...)`、构造 `NFilesIter(...)`，并把 fan-out 写进 `pc.nOutFilesPrePost`。
  - 已补清更细的运行态结论：`WriteBinaryParticleDataAsync(...)` 当前完全不再读取这条参数，而是直接通过 `AsyncOut::GetWriteInfo(rank).ifile` 决定 header file number 和实际数据文件名，所以这条输入只属于 sync 粒子 writer 及其 pre/post cleanup 链。

- [x] 2026-05-24：继续细化 `vismf.headerversion / verbose`
  - 已补清这组更硬的 writer-side 反向边界：用户输入的 `vismf.headerversion` 当前不会直接 materialize 成 WarpX 常规 field plotfile/checkpoint 的 on-disk header 版本。
  - 已补清更细的运行态结论：`FlushFormatPlotfile` 会先强制 `VisMF::SetHeaderVersion(Version_v1)`，`FlushFormatCheckpoint` 会先强制 `VisMF::SetHeaderVersion(NoFabHeader_v1)`，写完后再把进程内静态状态恢复回去。

- [x] 2026-05-24：继续细化 `particles.nreaders / nparts_per_read / datadigits_read / use_prepost`
  - 已补清这组更硬的 writer-side 反向边界：`use_prepost` 当前不只是 checkpoint 特例，plotfile 也会经 `WritePlotFilePre()/WritePlotFilePost()` 直接复用同一对 `CheckpointPre()/CheckpointPost()` 包装器。
  - 已补清更细的运行态结论：所以这条开关控制的是粒子 binary writer 的整类 pre/post 聚合协议，而不是只控制 checkpoint header 收尾。

- [x] 2026-05-24：继续细化 `warpx.mffile_nstreams`
  - 已补清这组更硬的分支不对称：同一个 per-file reader 上限在 `VisMF::Read(...)` 的两条分支里不是同一种实现；同步 fast path 先拆 `streamSets` 再逐组读。
  - 已补清更细的运行态结论：普通 coordinator 读链则把同一文件按 `nOpensPerFile` 重复登记进 `availableFiles`，按“读取槽位数”调度并发 reader，而不是复用前者的 rank-set 切分结构。

- [x] 2026-05-24：继续细化 `vismf.usedynamicsetselection / iobuffersize / allowsparsewrites / noflushafterwrite / barrierafterlevel`
  - 已补清这组更硬的 `iobuffersize` reader-side 反向边界：同步 `NoFabHeader + zero-grow` fast path 虽然也走 `NFilesIter`，但命中的是读构造函数默认 `setBuf=false` 的分支。
  - 已补清更细的运行态结论：因此这条同步 file-order 读链当前不会因 `vismf.iobuffersize` 自动对 `fileStream` 做 `pubsetbuf(...)`，它主要消费的仍是 `usesynchronousreads/usesingleread` 这组 reader gate。

- [x] 2026-05-24：继续细化 `vismf.groupsets / setbuf / checkfilepositions / usepersistentifstreams / usesynchronousreads`
  - 已补清这组更硬的交叉 reader 边界：`usesynchronousreads` 即便已经切进 `NoFabHeader + zero-grow` 的同步 file-order 读链，链内是否真正合并成一次大块读取，仍继续受 `usesingleread` 约束。
  - 已补清更细的运行态结论：源码还会继续检查 `dataIsContiguous` 与 combined-buffer 分配结果；若任一条件不满足，当前仍会在同步总链内部退回逐 fab 读取。

- [x] 2026-05-24：继续细化 `warpx.field/particle_io_nfiles`
  - 已补清这组更硬的生命周期不对称：`field_io_nfiles` 只在 startup 期一次性写进 `VisMF` 全局静态 `nOutFiles`，而粒子侧 `WriteBinaryParticleData...` 每次调用都会重新 `queryAdd("particles_nfiles", ...)`。
  - 已补清更细的运行态结论：粒子 writer 每次都会立刻覆盖 `pc.nOutFilesPrePost`，后续 `CheckpointPost()` 的 zero-length 文件清理也按这份最近一次写盘状态展开。

- [x] 2026-05-24：继续细化 `warpx.usesingleread / usesinglewrite`
  - 已补清这组更硬的 combined-buffer fallback 边界：这两条开关都不是硬保证模式；即便已经命中 `VisMF` 的聚合读写分支，源码也只是先尝试 `new(std::nothrow)` 分配整块缓冲。
  - 已补清更细的运行态结论：若 combined buffer 分配失败，`VisMF` 当前会静默退回普通逐块读写路径，而不是因“要求 single read/write”直接报错。

- [x] 2026-05-24：继续细化 `warpx.always_warn_immediately`
  - 已补清这组更硬的 single-rank / no-MPI 反向边界：单 rank 或未编进 MPI 时，warning summary 会直接退化到 `one_rank_gather_msgs_with_counter_and_ranks()`，完全绕过 gather/handoff。
  - 已补清更细的运行态结论：这一路径会把每条 warning 预先标成 `all_ranks=true`，所以 `@ Raised by:` 当前渲染成 `ALL`，不是本地 rank 号。

- [x] 2026-05-24：继续细化 `warpx.always_warn_immediately`
  - 已补清这组更硬的 zero-warning fast path：MPI 多 rank 下只要 gather-rank 的 warning 种类数为 0，聚合链就会在广播/回包/handoff 前整体短路。
  - 已补清更细的运行态结论：随后只有 IO rank 会把空列表渲染成 `No recorded warnings.`，non-IO rank 仍返回 `"[see I/O rank message]"` 占位串。

- [x] 2026-05-24：继续细化 `warpx.always_warn_immediately`
  - 已补清这组更硬的 gather-to-IO handoff 边界：当 gather rank 不是 IO rank 时，完整合并后的 warning 列表只会先在 gather rank 上 materialize 一次，再由它序列化后单播交给 IO rank。
  - 已补清更细的运行态结论：其它非 IO、非 gather ranks 当前不会反序列化这份最终全局列表。

- [x] 2026-05-24：继续细化 `warpx.always_warn_immediately`
  - 已补清这组更硬的 rank-list 压缩边界：关闭即时打印后，global summary 对“所有 rank 都发过”的 warning 不会保留完整 rank 列表，而是把 `ranks` 向量清空并渲染成 `@ Raised by: ALL`。
  - 已补清更细的运行态结论：后续 summary 当前会主动压缩 all-ranks warning 的 rank provenance，而不是继续逐 rank 枚举。

- [x] 2026-05-24：继续细化 `warpx.always_warn_immediately`
  - 已补清这组更硬的 gather-rank topology：关闭即时打印后，`PrintGlobalWarnings()` 的 global summary 不是简单“warning 最多的 rank”主导；若 IO rank 自己与最大 warning 种类数打平，源码会强制让 IO rank 充当 gather rank。
  - 已补清更细的运行态结论：后续 global summary 当前存在一条 IO-rank 优先的平局规则，不是纯粹的最大值赢家通吃。

- [x] 2026-05-24：继续细化 `amrex.abort_on_unused_inputs`
  - 已补清这组更硬的 stdout-ordering 边界：`WarpXEvolve.cpp` 会在进入任何 finalize 链之前无条件打印一次 `PrintGlobalWarnings("THE END")`。
  - 已补清更细的运行态结论：即便收尾期最终因 unused inputs abort，当前仍会先看到 end-of-evolve warning summary；真正来不及执行的是 `main.cpp` 里的 `Total Time` 和更后的 external-library finalize。

- [x] 2026-05-24：继续细化 `amrex.abort_on_unused_inputs`
  - 已补清这组更硬的 finalize-stack 时序边界：硬失败不是在 WarpX 第一步后的 early unused check 当场触发，而是沿 `WarpX::Finalize() -> amrex::Finalize() -> ParmParse::Finalize()` 在收尾期触发。
  - 已补清更细的运行态结论：一旦这条开关在 finalize 阶段升级成 abort，`main.cpp` 里的 `Total Time` 和后续 external-library finalize 当前都来不及再执行。

- [x] 2026-05-24：继续细化 `vismf.headerversion / verbose`
  - 已补清这组 `Exist()` 的更硬弱探针边界：它只在 IO rank 上尝试打开 `name + "_H"` 并读取 `iss.good()`，随后广播这个布尔值。
  - 已补清更细的运行态结论：它当前只回答 header 文件是否能打开，不解析 header，也不做版本或坏块校验。

- [x] 2026-05-24：继续细化 `vismf.headerversion / verbose`
  - 已补清这组 `ReadFAHeader` 的更硬 reader-side 边界：它不会解析 `Header`、不会走 `Check()`，而是只把 header 文件原始字节经 `ReadAndBcastFile(...)` 广播出来。
  - 已补清更细的运行态结论：这条 helper 当前提供的是 header-bytes transport，不是带校验或带语义解析的 reader。

- [x] 2026-05-24：继续细化 `vismf.headerversion / verbose`
  - 已补清这组 `OpenStream/CloseStream` 的更硬 reader-lifecycle 边界：`PersistentIFStream::currentPosition` 当前只在打开时置零，后续没有 consumer，而 `readFAB` 每次都会显式 `seekg(...)` 到目标 offset。
  - 已补清更细的运行态结论：persistent ifstream 现在保留的是句柄和 buffer，不是可复用的 seek 位置语义。

- [x] 2026-05-24：继续细化 `vismf.headerversion / verbose`
  - 已补清这组 `readFAB` 的更硬 GPU 同步边界：device/managed 分支虽然先落到 pinned host buffer，再走 `htod_memcpy_async(...)` 或 `copy<RunOn::Device>(...)`，但每条分支都会在返回前立刻 `Gpu::streamSynchronize()`。
  - 已补清更细的运行态结论：这里当前不是延迟填充式 readback，而是同步完成后才把结果交回调用方。

- [x] 2026-05-24：继续细化 `vismf.headerversion / verbose`
  - 已补清这组 `readFAB(FabArray&)` 的更硬 guard-cell / staging 边界：当 `hdr.m_ngrow != mf.nGrowVect()` 时，源码不会先拒绝，而是先改写局部 `box`，再在 `box != fab.box()` 时退化成临时 `hostfab` 读入加一次 `copy(...)`。
  - 已补清更细的运行态结论：grow mismatch 当前走的是 staging/copy 路径，而不是 upfront reject。

- [x] 2026-05-24：继续细化 `vismf.headerversion / verbose`
  - 已补清这组 `readFAB` 的更硬 header-consumption 分叉：`Version_v1` 路径会继续消费磁盘上的 FAB header，而 `NoFabHeader` 路径完全绕开 FAB header，只按 `hdr.m_writtenRD` 读原始字节或做格式转换。
  - 已补清更细的运行态结论：`headerversion` 在 readback 侧当前不只是 writer 元数据差异，而是实际的磁盘读协议分叉。

- [x] 2026-05-24：继续细化 `vismf.headerversion / verbose`
  - 已补清这组 `VisMF` 对象化 reader 的更硬 constructor-side lifecycle 边界：`VisMF::VisMF(std::string)` 也不会先走 `Check()`，而是构造期直接 `ReadAndBcastFile` 读 `Header` 并 materialize `m_hdr/m_pa`。
  - 已补清更细的运行态结论：这条 reader 入口的 header materialization 当前也不受 `verbose` gate，因此 `Check()` 同样不是它的前置链。

- [x] 2026-05-24：继续细化 `vismf.headerversion / verbose`
  - 已补清这组 `VisMF::Check()/Read()` 的更硬 lifecycle 反向边界：`VisMF::Read()` 常规主链不会先调用 `Check()`，而是直接读 `Header` 后分流到 `Version_v1 / NoFabHeader` 读盘路径。
  - 已补清更细的运行态结论：`Check()` 的版本/坏块探测当前不属于 restart 或常规 MultiFab readback 的必经前置链。

- [x] 2026-05-24：继续细化 `vismf.headerversion / verbose`
  - 已补清这组 `VisMF::Check()` 的更硬 dead-state 边界：`v1` 虽会广播给所有 rank，但广播后函数体里没有任何后续 consumer。
  - 已补清更细的运行态结论：函数最终仍只返回 `isOk`，因此 `v1` 当前不是第二返回通道，而是一个在函数内被 materialize 后立即失活的 side channel。

- [x] 2026-05-24：继续细化 `vismf.headerversion / verbose`
  - 已补清这组 `VisMF::Check()` 的更硬 caller 反向边界：在当前本地 `amrex/warpx` 源码树里看得到定义，但没有稳定命中的直接调用方。
  - 已补清更细的运行态结论：这条 `Check()` 合同当前更接近可选离线诊断工具链，而不是 WarpX 常规 plotfile/checkpoint 或 restart 主链。

- [x] 2026-05-24：继续细化 `vismf.headerversion / verbose`
  - 已补清这组 `VisMF::Check()` 的更硬返回值不对称：函数虽会广播 `v1`，但最终 `return` 只看 `isOk`。
  - 已补清更细的运行态结论：遇到非 `Version_v1` 时，源码会提示“不支持”，却不会因此自动返回失败态。

- [x] 2026-05-24：继续细化 `vismf.headerversion / verbose`
  - 已补清这组 `VisMF::Check()` 日志的更硬 IO-rank 边界：header 读取、逐文件 `FAB` 签名探测和 `Version_v1` 支持判断都只在 IO rank 上执行。
  - 已补清更细的运行态结论：其他 rank 当前只接收 `isOk/v1` 广播结果，不会 materialize 出逐文件检查日志。

- [x] 2026-05-24：继续细化 `vismf.headerversion / verbose`
  - 已补清这组 `VisMF` 读盘日志的更硬 coordinator 边界：`VisMF::Read()` 里的 `inFileOrder/not inFileOrder` 和 `FARead :: ...` 统计还要求 `myProc == coordinatorProc`。
  - 已补清更细的运行态结论：这组 readback 日志不会按 `verbose` 在所有参与读取的 rank 上铺开。

- [x] 2026-05-24：继续细化 `vismf.headerversion / verbose`
  - 已补清这组 `VisMF` 静态状态的更硬 finalize 反向边界：`VisMF::Finalize()` 不会把 `currentVersion/verbose` 重置回源码默认值。
  - 已补清更细的运行态结论：下一次 `Initialize()` 若没显式再给 `vismf.headerversion/verbose`，会从进程内现存静态状态继续出发。

- [x] 2026-05-24：继续细化 `amrex.parmparse.verbose`
  - 已补清这条 unused-input 明细 gate 的更硬 non-IO 反向边界：即便 verbosity 值已在各 rank 上解析并缓存，`QueryUnusedInputs()/Finalize()` 仍会先被 `IOProcessor()` 截住。
  - 已补清更细的运行态结论：non-IO rank 上当前不会 materialize 出 unused-input 明细输出。

- [x] 2026-05-24：继续细化 `amrex.abort_on_unused_inputs`
  - 已补清这条 unused-input gate 的更硬状态保持边界：`QueryUnusedInputs()` 只是观测 `g_table` 并返回布尔值，不会清空或消费 unused entries。
  - 已补清更细的运行态结论：若之后没有其它 parser consumer 命中它们，finalize 阶段看到的仍是同一批未消费状态。

- [x] 2026-05-24：继续细化 `warpx.always_warn_immediately`
  - 已补清这条 warning-manager 开关的更硬输出拓扑边界：它会把 warning 输出从 IO-rank 独占的 global summary，扩成每个命中 rank 各自即时打一行。
  - 已补清更细的运行态结论：后面的 logger 收集和 IO-rank 汇总链仍会保留，因此 immediate lines 和 global summary 当前可以并存。

- [x] 2026-05-24：继续细化 `warpx.limit_verbose_step`
  - 已补清这条 step-loop 日志节流开关的更硬 startup 反向边界：它只节流主循环里的 `verbose_step` consumer，不会命中 `InitData()` 里隐式求解器 `PrintParameters()` 的参数 banner。
  - 已补清更细的运行态结论：这类 startup 输出不会并入 1/10/100 步的降采样链。

- [x] 2026-05-24：继续细化 `warpx.verbose`
  - 已补清这条总 verbosity 开关的更硬 startup/runtime 分叉：隐式求解器 `PrintParameters()` 的参数 banner 在 `InitData()` 中、`WriteUsedInputsFile()` 之前一次性打印，只看 `m_WarpX->Verbose()`。
  - 已补清更细的运行态结论：这组 startup 参数打印不经过 step-loop 的 `verbose_step`，也不会被 `limit_verbose_step` 降采样。

- [x] 2026-05-24：继续细化 `amrex.the_arena_is_managed`
  - 已补清这条 arena 主分叉键的更硬 alias 合同：`the_arena_is_managed=1` 时源码会直接令 `the_managed_arena = the_arena`，而不会再单独构造独立 managed arena。
  - 已补清更细的运行态结论：此时默认 `DeviceVector` 与 `ManagedVector` 会共享同一根 arena 指针，而 `the_managed_arena_*` 这组 managed-only 参数不会 materialize 成独立内存池。

- [x] 2026-05-24：继续细化 `amrex.parmparse.verbose`
  - 已补清这条 AMReX 明细打印 gate 的更硬 finalize 生命周期边界：`ParmParse::Finalize()` 不只会把 `pp_detail::verbose` 重置回 `-1`，还会把 `initialized = false`。
  - 已补清更细的运行态结论：下一次 `ParmParse::Verbose()` 不是单独重查一个缓存变量，而是跟着整套 `ParmParse` session 一起重新 materialize。

- [x] 2026-05-24：继续细化 `amrex.abort_on_unused_inputs`
  - 已补清这条 AMReX parser 开关的更硬双阶段合同：`ppinit(...)` 时会先通过 `ExecOnFinalize(ParmParse::Finalize)` 注册最终 unused-input 检查。
  - 已补清更细的运行态结论：即便 WarpX 第一步后的 early check 已经把 unused inputs 暴露给用户，只要同一进程继续走到收尾，这条开关仍会在 finalize 阶段再次对同一张 `g_table` 决定是否硬失败。

- [x] 2026-05-24：继续细化 `max_step`
  - 已补清这条全局步数上界的更硬 local-vs-global 终止策略边界：`WarpX::Evolve(numsteps)` 虽会先用 `numsteps_max` 做本次调用的局部步数截断，但 step-loop 结束后的 `final_time_step` 仍只认全局 `max_step`。
  - 已补清更细的运行态结论：局部步数预算跑完不会被当成“达到最终步”去触发 final-flush。

- [x] 2026-05-24：继续细化 `stop_time`
  - 已补清这条全局时间上界与 BTD 配套的更硬终止策略不对称：当 `max_step` 和 `stop_time` 都保持默认无穷、且开启 `compute_max_step_from_btd` 时，兜底只会收紧步数侧，不会同步补 `stop_time`。
  - 已补清更细的运行态结论：`WarpX::Evolve()` 的双重退出条件会被收缩成“步数侧先触顶、时间侧仍保持无穷上界”。

- [x] 2026-05-24：继续细化 `warpx.compute_max_step_from_btd`
  - 已补清这条 BTD 运行长度总开关的更硬终止策略边界：当 `max_step` 和 `stop_time` 都保持默认无穷时，源码里的兜底当前不是同时补齐两者，而是只补 `max_step`。
  - 已补清更细的运行态结论：开启这条开关后，这类场景会把全局 stop policy 钉成“按步数侧终止”，而不是生成一对彼此一致的 step/time 上界。

- [x] 2026-05-24：继续细化 `<diag_name>.do_back_transformed_fields`
  - 已补清这条 BTD 字段总 gate 的更硬时序不对称：`ReadParameters()` 里 “fields/particles 不能同时为假” 对字段侧同样只是一条早期 admission 断言，不是最终态断言。
  - 已补清更细的运行态结论：若后面 `m_varnames.empty()`，源码会再把 `m_do_back_transformed_fields` 固化成 `false`，但不会回头重做一次最小可行性检查。

- [x] 2026-05-24：继续细化 `<diag_name>.do_back_transformed_particles`
  - 已补清这条 BTD 粒子总 gate 的更硬时序不对称：`ReadParameters()` 里 “fields/particles 不能同时为假” 当前只是早期 admission 断言，不是最终态断言。
  - 已补清更细的运行态结论：`DerivedInitData()` 还会按 `write_species` 和 species 名单重新覆盖 `m_do_back_transformed_particles`，但之后不会再重做一次最小可行性检查。

- [x] 2026-05-24：继续细化 `<diag_name>.buffer_size`
  - 已补清这条 BTD buffer 输入的更硬下限风险：当前实现不会在 parser 后立刻要求 `m_buffer_size > 0`。
  - 已补清更细的运行态结论：显式给出 `0` 或负值时，这条输入不会先被拒绝，而会继续流入 `DerivedInitData()` 的除法、`final_snapshot_fill_iteration` 估算，以及 snapshot 对齐和 buffer-box 构造链。

- [x] 2026-05-24：继续细化 `<diag_name>.dz_snapshots_lab`
  - 已补清这条 BTD 空间壳输入的更硬桥接风险：当前实现会直接做 `m_dz_snapshots_lab / WarpX::moving_window_v`，但 BTD 并没有额外要求 `moving_window_v != 0` 或 `> 0`。
  - 已补清更细的运行态结论：这条壳输入现在会把 `moving_window_v` 的零值或负号原样继承进 `m_dt_snapshots_lab`，而不是先命中独立 gate。

- [x] 2026-05-24：继续细化 `<diag_name>.dt_snapshots_lab`
  - 已补清这条 BTD 时间节奏输入的更硬下限/符号风险：当前实现不会在 parser 后立刻要求 `m_dt_snapshots_lab > 0`。
  - 已补清更细的运行态结论：显式给出 `0` 或负值时，这条输入不会先命中独立正值 gate，而会继续流入 `m_t_lab`、`final_snapshot_starting_step / final_snapshot_fill_iteration` 和自动补 `max_step/stop_time` 的整条 consumer 链。

- [x] 2026-05-24：继续细化 `<diag_name>.num_snapshots_lab`
  - 已补清这条 BTD companion 的更硬下限风险：当前实现不会在 parser 后立刻要求 `m_num_snapshots_lab > 0`。
  - 已补清更细的运行态结论：显式给出 `0` 时，源码会把它改写成 `":-1"`，令 `BTDIntervalsParser` 产出空的 `m_btd_iterations`；而 `DerivedInitData()` 随后仍会无条件调用 `GetFinalIteration()`，落到空向量 `back()` 的路径。

- [x] 2026-05-24：继续细化 `<diag_name>.average_start_step`
  - 已补清这条 `TimeAveraged` companion 的更硬 ignored-companion 不对称：`dynamic_start` 下它当前不是像 period companions 那样 warning 后仍残留成员态，而是只被读进局部 `unused_start_step`。
  - 已补清更细的运行态结论：`m_average_start_step` 会继续保持默认值，直到运行期再由 `m_intervals.nextContains(step) - m_average_period_steps` 重新 materialize。

- [x] 2026-05-24：继续细化 `<diag_name>.average_period_steps`
  - 已补清这条 `TimeAveraged` companion 的更硬 `dynamic_start` parser/runtime 边界：`ReadParameters()` 当前只检查它和 `average_period_time` 二选一，不会在 parser 后立刻要求 `m_average_period_steps > 0`。
  - 已补清更细的运行态结论：显式给出 `0` 或负值时，这条输入不会在读取阶段被拒绝，而会继续流入 `DoComputeAndPack()` 的窗口回推和 `Flush()` 的归一化除数链。

- [x] 2026-05-24：继续细化 `<diag_name>.average_period_time`
  - 已补清这条 `TimeAveraged` companion 的更硬 dynamic-start 零步长风险：`DerivedInitData()` 会直接把 `average_period_time / dt` 做 `round(...)`，但后续没有再检查离散结果 `> 0`。
  - 已补清更细的运行态结论：若结果被四舍五入成 `0`，`DoComputeAndPack()` 仍会接受这条窗口起点，而 `Flush()` 在 `step > 0` 时会继续把 `m_average_period_steps` 当成归一化除数。

- [x] 2026-05-24：继续细化 `vismf.usedynamicsetselection / iobuffersize / allowsparsewrites / noflushafterwrite / barrierafterlevel`
  - 已补清这组 `VisMF` 输入里 `noflushafterwrite` 的更硬 header-side 反向边界：它当前不控制 `VisMF::WriteHeaderDoit()` 的 `MFHdrFile.flush()`，也不会扩展到粒子写盘侧的 `ParticleHeader.flush()` / `HdrFile.flush()`。
  - 已补清更细的运行态结论：这条输入现在只属于 MultiFab 数据文件写链的末端 flush gate，不是所有 header / metadata writer 的统一 flush 开关。

- [x] 2026-05-24：继续细化 `vismf.usedynamicsetselection / iobuffersize / allowsparsewrites / noflushafterwrite / barrierafterlevel`
  - 已补清这组 `VisMF` 输入里 `barrierafterlevel` 的更硬 utility-side 反向边界：`WriteMultiLevelPlotfile(...)` 在 `PreBuildDirectorHierarchy(...)` 之后本来就会先执行一次无条件 `Barrier()`，它不受 `GetBarrierAfterLevel()` 控制。
  - 已补清更细的运行态结论：这条输入当前只控制 per-level 写后 barrier，不控制 plotfile 目录预建阶段的全局同步。

- [x] 2026-05-24：继续细化 `vismf.usedynamicsetselection / iobuffersize / allowsparsewrites / noflushafterwrite / barrierafterlevel`
  - 已补清这组 `VisMF` 输入里 `allowsparsewrites` 的更硬 sparse trigger 边界：源码当前不是看“全局空闲 rank 数”或真实写出字节，而只是比较 `DistributionMap().ProcessorMap()` 去重后的 box-owner ranks 数是否小于 `nOutFiles`。
  - 已补清更细的运行态结论：这条输入现在 gate 的是布局层面的 owner 稀疏度，而不是更广义的 MPI 稀疏度指标。

- [x] 2026-05-24：继续细化 `vismf.usedynamicsetselection / iobuffersize / allowsparsewrites / noflushafterwrite / barrierafterlevel`
  - 已补清这组 `VisMF` 输入里 `iobuffersize` 的更硬 validation 反向边界：这条 parser 当前不会经过 `VisMFBuffer::SetIOBufferSize()`，因此不会命中其中的正值断言。
  - 已补清更细的运行态结论：源码会直接覆写静态 `ioBufferSize`，后续 `WriteHeaderDoit(...)`、persistent input stream 和 `AsyncWriteDoit(...)` 都只继续复用这份共享缓冲大小状态。

- [x] 2026-05-24：继续细化 `vismf.usedynamicsetselection / iobuffersize / allowsparsewrites / noflushafterwrite / barrierafterlevel`
  - 已补清这组 `VisMF` 输入里 sparse-FPP 的更硬 provenance 不对称：命中 sparse 分支后，`FindOffsets()` 不会沿用普通 static 的 `FileNumber(..., groupSets)`，也不会走 dynamic 的 dense file-number 表。
  - 已补清更细的运行态结论：源码会把“真正写出数据的 rank 自身”直接物化成 file number / file name，因此若活跃 ranks 稀疏，header 当前会保留按原 rank 编号命名、而不是 `0..nOutFiles-1` 连续压缩后的数据文件 provenance。

- [x] 2026-05-24：继续细化 `vismf.usedynamicsetselection / iobuffersize / allowsparsewrites / noflushafterwrite / barrierafterlevel`
  - 已补清这组 `VisMF` 输入里 `usedynamicsetselection` 的更硬 header 回填分叉：`FindOffsets()` 在 dynamic 路径下不会再按静态 `FileNumber(..., groupSets)` 重建 `hdr.m_fod[*].m_name`。
  - 已补清更细的运行态结论：源码会改用 coordinator 记录的 `FileNumbersWritten()` 与 `FileNumbersWriteOrder()` 回填 file number 与 offset，因此这条输入当前不只改变写时调度，还会改 header 中最终 materialize 的 rank-to-file provenance。

- [x] 2026-05-24：继续细化 `vismf.usedynamicsetselection / iobuffersize / allowsparsewrites / noflushafterwrite / barrierafterlevel`
  - 已补清这组 `VisMF` 输入里 `usedynamicsetselection` 的更硬 static-vs-dynamic 回退链：`usedynamicsetselection=1` 当前并不保证真的走进 `NFilesIter` 的 dynamic decider/coordinator 路径。
  - 已补清更细的运行态结论：`SetSparseFPP(...)` 会直接把 `useStaticSetSelection` 设回 `true`；即使未命中 sparse 分支，`SetDynamic()` 里也会在 `nOutFiles == nProcs` 时立刻回退成 static set-selection，所以只有 `nOutFiles < nProcs` 且未进入 sparse-FPP 的场景才真正 materialize 动态协调写链。

- [x] 2026-05-24：继续细化 `vismf.groupsets / setbuf / checkfilepositions / usepersistentifstreams / usesynchronousreads`
  - 已补清这组 `VisMF/NFiles` 输入里 `groupsets` 的更硬 lifecycle 不对称：源码在写后 header 回填时仍按当前 `groupSets` 重建 `m_fod[*].m_name`。
  - 已补清更细的运行态结论：`RemoveFiles()` 清理数据文件时却固定按 `groupSets=true` 去重新枚举待删文件名，因此 `groupsets=0` 当前不只影响写时 rank-to-file 映射，还和后续清理链的文件命名假设形成不对称。

- [x] 2026-05-24：继续细化 `vismf.groupsets / setbuf / checkfilepositions / usepersistentifstreams / usesynchronousreads`
  - 已补清这组 `VisMF/NFiles` 输入里 `usepersistentifstreams` 的更硬生命周期边界：它当前只稳定存在于单次 `VisMF::Read(...)` 调用内部。
  - 已补清更细的运行态结论：`Read(...)` 收尾时只要开关为真，就会遍历当前 header 命中的数据文件并逐个 `DeleteStream(...)`，所以这些持久 ifstream 不会自动跨到下一次 restart/read 调用继续保活。

- [x] 2026-05-24：继续细化 `vismf.groupsets / setbuf / checkfilepositions / usepersistentifstreams / usesynchronousreads`
  - 已补清这组 `VisMF/NFiles` 输入里 `setbuf` 的更硬 writer 非对称边界：`setbuf=0` 当前并不能统一关闭所有 `VisMF` 写流 buffering。
  - 已补清更细的运行态结论：`NFilesIter` 和 `OpenStream(...)` 会按 `setBuf` 判定是否 `pubsetbuf(...)`，但 `WriteHeaderDoit(...)` 和 field async writer `AsyncWriteDoit(...)` 仍会直接按 `ioBufferSize` 无条件配置 stream buffer。

- [x] 2026-05-24：继续细化 `vismf.usedynamicsetselection / iobuffersize / allowsparsewrites / noflushafterwrite / barrierafterlevel`
  - 已补清这组 `VisMF` 输入里 `noflushafterwrite` 的更硬 flush 反向边界：它当前只影响同步 `VisMF::Write(...)` 的逐 fab 分支，不影响 field async writer。
  - 已补清更细的运行态结论：`AsyncWriteDoit(...)` 仍会在后台线程真正写完当前文件块后无条件 `ofs.flush()`，所以这条输入不会抑制异步 field plotfile 路径的实际落盘 flush。

- [x] 2026-05-24：继续细化 `vismf.usedynamicsetselection / iobuffersize / allowsparsewrites / noflushafterwrite / barrierafterlevel`
  - 已补清这组 `VisMF` 输入里 `barrierafterlevel` 的更硬 async plotfile 边界：它在异步 field plotfile 分支里当前不是后台 I/O 完成栅栏。
  - 已补清更细的运行态结论：`WriteMultiLevelPlotfile(...)` 会先对当前 level 调 `VisMF::AsyncWrite(...)`，随后立刻 `Barrier()`；真正落盘继续在 `AsyncWriteDoit(...)` 通过 `AsyncOut::Submit(...)` 派生出的后台线程里完成，所以这条 barrier 只保证各 rank 都提交完该 level 的异步写任务。

- [x] 2026-05-24：继续细化 `vismf.headerversion / verbose`
  - 已补清这组 `VisMF` 输入的更硬 utility 非对称边界：`vismf.verbose` 当前不是覆盖所有 `VisMF` 工具函数的统一日志总开关。
  - 已补清更细的运行态结论：`VisMF::Read()` / `Check()` 会消费静态 `verbose`，但 `RemoveFiles(...)` 只认调用方显式传入的 `a_verbose`，而 `Write(...)` 路径则根本没有对应的静态日志 gate。

- [x] 2026-05-24：继续细化 `amr.plot_headerversion / checkpoint_headerversion`
  - 已补清这组头部版本输入的更硬 writer 颗粒度边界：它们当前只会打到后续 `VisMF::Write(...)` 的 MultiFab 数据块头，不会改顶层文本 `Header/WarpXHeader` 文件本身。
  - 已补清更细的运行态结论：无论是 AMReX `Amr` 常规 writer，还是 WarpX diagnostics flush writer，这组输入/覆写当前控制的都是 FAB/VisMF header contract，而不是 plotfile/checkpoint 文本 metadata header 的格式开关。

- [x] 2026-05-24：继续细化 `amrex.use_profiler_syncs`
  - 已补清这条 profiler 同步输入的更硬宏族非对称边界：它当前不只控制 `BL_PROFILE_SYNC_START_TIMED/STOP` 这条 region-based 路径。
  - 已补清更细的运行态结论：`BL_PROFILE_SYNC` 与 `BL_PROFILE_SYNC_TIMED` 对应的 `Sync()/Sync(name)` 完全绕过 `sync_counter`，只要开关为真，每次命中都会立刻 barrier；相对地 `StartSyncRegion{,Timed}()/EndSyncRegion()` 仍只在 `sync_counter==0` 的最外层 region 才真正 barrier。

- [x] 2026-05-24：继续细化 `ablastr.fillboundary_always_sync`
  - 已补清这条 nodal-sync 输入的更硬 `E/B` vs `F/G` 非对称边界：它当前并不能统一强制所有 `FillBoundary*` 升级成 sync。
  - 已补清更细的运行态结论：`WarpXComm.cpp` 里 `FillBoundaryE/B` 只有在 `do_single_precision_comms=true` 时才转进 helper 并读取 `fillboundary_always_sync`；若普通精度直连 AMReX，它们只看显式传下来的 `nodal_sync`。相对地 `FillBoundaryF/G` 无论单精度与否都会继续走 helper，因此这条输入当前仍能强制 `F/G` 升级成 sync。

- [x] 2026-05-24：继续细化 `warpx.safe_guard_cells`
  - 已补清这条 safe-mode 开关的更硬 allocation-side 边界：它当前不只放大运行期通信，还会先通过 `GuardCellManager` 抬高 `ng_alloc_*`，直接改变 `AllocLevelMFs(...)` 分配出的 `mf.nGrowVect()`，并把同一份 `ng_FieldSolver.max()` 继续传给 EB factory 与 PML 构造。
  - 已补清更细的运行态结论：`WarpXInitData.cpp::CheckGuardCells()` 后续会按这些更大的 guard-cell 分配逐个 `MultiFab` 执行 `valid_cells > guard_cells` 断言，因此 safe 模式还会把“小 box / 大 guard-cell”的 hard failure 更早带到 startup 校验阶段，而不是等到某次 `FillBoundary` 才暴露。

- [x] 2026-05-24：继续细化 `warpx.serialize_initial_conditions`
  - 已补清这条参数相邻旧别名 `warpx.serialize_ics` 的更硬 startup 时序：拒绝逻辑当前不是某个晚到的 runtime warning，而是在 `WarpX::WarpX()` 构造函数里 `ReadParameters()` 之后立刻进入 `BackwardCompatibility()` 时触发。
  - 已补清更细的运行态结论：只要输入文件仍使用旧别名，源码就会在 `InitEB()`、signal-handling 初始化和后续 `InitData()` 之前直接 abort，不存在自动 remap 或“先继续启动、稍后再报错”的缓冲阶段。

- [x] 2026-05-24：继续细化 `warpx.serialize_initial_conditions`
  - 已补清这条初始化串行化开关的更硬注入家族反向边界：它当前虽然会同时覆盖 `AddPlasma()` 的初始体注入与 moving-window 连续体注入，但不会跨到其它注入风格。
  - 已补清更细的运行态结论：`AddPlasmaFlux()` 仍走自己独立的 `#pragma omp parallel if (Gpu::notInLaunchRegion())`，`AddPlasmaFromFile()` 则走 IO-rank host-vector/openPMD 读取与一次性 `AddNParticles(...)` 链；两者都不会读取 `WarpX::serialize_initial_conditions`，因此这条开关当前只控制 volume plasma 注入，不控制 flux 注入或 external-file 导入。

- [x] 2026-05-24：继续细化 `amr.restart`
  - 已补清这条 restart 路径的更硬并行恢复合同：`InitFromCheckpoint()` 读取每个 level 的 `BoxArray` 后，不会无条件沿用 checkpoint 里的 `DistributionMapping`。
  - 已补清更细的运行态结论：只要 `Level_#/DM` 文件缺失、checkpoint 记录的 MPI 进程数与当前 `NProcs()` 不一致，或 `dm.size()` 与当前 `ba.size()` 不匹配，源码就会静默退回 `DistributionMapping{ba, NProcs()}`，按当前并行规模重建 box-to-rank 布局。

- [x] 2026-05-24：继续细化 `warpx.write_diagnostics_on_restart`
  - 已补清这条 restart 诊断补写开关的更硬 reduced-diag 运行时合同：`WarpXInitData.cpp` 当前不是先按 `intervals` 过滤 reduced diagnostics，而是先直接调用 `reduced_diags->ComputeDiags(istep[0]-1)`。
  - 已补清更细的运行态结论：这会让 `MultiReducedDiags::ComputeDiags()` 对所有 reduced-diag 实例无条件 fanout 计算；只有后面的 `MultiReducedDiags::WriteToFile()` 才在 IO rank 上按 `m_intervals.contains(step+1)` 过滤是否真正落盘，因此 restart 补写采用的是“先全实例计算、后按 intervals 写出”的两段链。

- [x] 2026-05-24：继续细化 `warpx.quantum_xi`
  - 已补清这条 Hybrid-QED 系数的更硬 kernel 内 consumer：它当前不是只在 cell-local 电场修正公式里出现一次。
  - 已补清更细的运行态结论：源码会先把 `xi_c2` 传进 `calc_M(...)`，在邻点 stencil 上构造 `M` 场；随后同一份系数又在当前 cell 内继续进入 `beta/Alpha/Omega` 与 `a00...a12` 3x3 线性系统求解，因此它控制的是两级 kernel 计算，而不是只给最终 `dE` 乘一个简单 prefactor。

- [x] 2026-05-24：继续细化 `warpx.use_hybrid_QED`
  - 已补清这条 Hybrid-QED 总开关的更细 patch-level fanout：`Hybrid_QED_Push(lev, PatchType::coarse, dt)` 当前不是“再推进一套独立 coarse level”。
  - 已补清更细的运行态结论：源码在 coarse 分支里会继续从当前 child `lev` 读取 `Efield_cp/Bfield_cp/current_cp`，但几何步长改成 `CellSize(lev-1)`，因此它真正消费的是“child-level coarse patch data + parent-level geometry”这组绑定。

- [x] 2026-05-24：继续细化 `qed_bw.chi_min`
  - 已补清这条 Breit-Wheeler 最小 `chi` 阈值的更硬 companion gate：`BreitWheelerEvolveOpticalDepth::operator()` 当前不是只看 `chi < chi_min`，还会先同时检查 `gamma_photon < 2`。
  - 已补清更细的运行态结论：任一命中都会直接跳过 optical-depth 演化；相对地，`BreitWheelerGeneratePairs` 自身只消费 pair-production table view，源码注释明确写着 photon 能量阈值不会在该 functor 内再次检查，因此 `2m_ec^2` 这层门槛只在 evolve gate 侧 materialize。

- [x] 2026-05-24：继续细化 `qed_qs.chi_min`
  - 已补清这条 Quantum Sync 最小 `chi` 阈值的更硬 push-side crossover 边界：它当前不只被 `QuantumSynchrotronEvolveOpticalDepth::operator()` 用来在 `chi_part < chi_min` 时直接跳过 optical-depth 演化。
  - 已补清更细的运行态结论：`PushSelector` 里的 `doParticleMomentumPush<1>` 在 `do_crr` 打开时还会再次比较同一个 `t_chi_max`，并把低 `chi` 粒子送进 `UpdateMomentumBorisWithRadiationReaction(...)`，只有达到阈值后才退回普通 `UpdateMomentumBoris(...)`，把高-`chi` recoil 留给后续 QED optical-depth / photon-emission 链。

- [x] 2026-05-24：继续细化 `qed_qs.photon_creation_energy_threshold`
  - 已补清这条 Quantum Sync photon cleanup 阈值的更硬比较合同：`cleanLowEnergyPhotons(...)` 当前不会先恢复显式 photon 能量标量，而是直接用新增区间的 `ux^2+uy^2+uz^2` 形成 `phot_energy^2`。
  - 已补清更细的运行态结论：源码随后把这份平方能量与阈值平方直接比较，不做开方，因此真正 materialize 的是“平方动量范数 -> 平方能量 -> 阈值平方”的无开方筛除链。

- [x] 2026-05-24：继续细化 `<reduced_diags_name>.weighting_function(x,y,z)`
  - 已补清这条 `ChargeOnEB` 空间权重函数的更硬 parser 生命周期边界：`ComputeDiags()` 当前会先无条件执行 `compileParser<3>(m_parser_weighting.get())`，然后才靠 `m_do_parser_weighting` 决定是否真的调用它。
  - 已补清更细的运行态结论：因此它现在也是 compile-before-gate，而不是命中开关后才延迟 materialize parser；这一前置生命周期和此前 `ParticleHistogram` / `ParticleHistogram2D` 的 parser companion 是同类边界。

- [x] 2026-05-24：继续细化 `<reduced_diags_name>.openpmd_backend / file_min_digits`（`DifferentialLuminosity2D`）
  - 已补清这组 2D luminosity openPMD writer 参数的更硬 writer materialization gate：`DifferentialLuminosity2D` 当前不是所有 rank 都会去建 `io::Series(...)`。
  - 已补清更细的运行态结论：源码会先在命中输出步时做 host 侧 `ReduceRealSum(...)`，但非 `IOProcessor` rank 会在 `ComputeDiags()` 尾部和 `WriteToFile()` 顶部两次直接返回，所以真正 materialize series、iteration 和 mesh 的只有单个 IO rank。

- [x] 2026-05-24：继续细化 `<reduced_diags_name>.openpmd_backend / file_min_digits`
  - 已补清这组 2D openPMD writer 参数的更硬 writer materialization gate：`ParticleHistogram2D` 当前不是所有 rank 都会去建 `io::Series(...)`。
  - 已补清更细的运行态结论：源码会先做 device->host 拷回和 `ReduceRealSum(...)`，但非 `IOProcessor` rank 会在 `ComputeDiags()` 尾部和 `WriteToFile()` 顶部两次直接返回，所以真正 materialize series、iteration 和 mesh 的只有单个 IO rank。

- [x] 2026-05-24：继续细化 `<reduced_diags_name>.value_function/filter_function(t,x,y,z,ux,uy,uz,w)`
  - 已补清这组 `ParticleHistogram2D` companion 的更硬 writer-side metadata 缺口：当前 openPMD writer 不只不会把 `value_function` 表达式单独写回输出。
  - 已补清更细的运行态结论：源码在 `resetDataset(...)` 后明确停在 `UNIT DIMENSION IS NOT SET ON THE VALUES`，因此即便 bin 值已经由 `value_function(...,w)` 定义出来，当前也不会把对应的 unit dimension materialize 到 openPMD metadata。

- [x] 2026-05-24：继续细化 `<reduced_diags_name>.histogram_function_abs/ord(t,x,y,z,ux,uy,uz,w)`
  - 已补清这两条 2D histogram parser 的更硬 writer-side 轴顺序合同：`ParticleHistogram2D::WriteToFile()` 当前不会沿用运行时的 `abs/ord` 命名顺序，而是显式按 ordinate-first、abscissa-second 输出 mesh 几何。
  - 已补清更细的运行态结论：`AxisLabels`、`gridGlobalOffset`、`gridSpacing` 和 dataset shape 当前都统一采用 `{ord, abs}` 顺序，因此 openPMD 导出坐标轴顺序和 kernel 内部的 `f_abs/f_ord` 命名是分开的。

- [x] 2026-05-24：继续细化 `<reduced_diags_name>.bin_number_abs/bin_min_abs/bin_max_abs/bin_number_ord/bin_min_ord/bin_max_ord`
  - 已补清这组 2D histogram bin 参数的更硬表生命周期边界：`ParticleHistogram2D::ComputeDiags()` 当前会先用 `m_bin_num_abs-1` 与 `m_bin_num_ord-1` 重新构造 `TableData` 上界，再按同一 shape 重新 `resize` `m_h_data_2D`。
  - 已补清更细的运行态结论：源码随后会把整张二维表逐格清零后再拷到 device，因此它当前输出的是每个 interval 的逐步快照，而不是沿用跨步累计的 2D histogram 缓冲。

- [x] 2026-05-24：继续细化 `<reduced_diags_name>.histogram_function(t,x,y,z,ux,uy,uz)`
  - 已补清这条 histogram parser 的更硬 AMR 时间标量边界：`ParticleHistogram::ComputeDiags()` 与 `ParticleHistogram2D::ComputeDiags()` 当前都会在进入 level 循环前先固定读取一次 `t = warpx.gett_new(0)`。
  - 已补清更细的运行态结论：后续所有 `lev`、tile 和粒子都共用这份 level-0 时间，源码不会按 `lev` 重取时间，也不会把粒子年龄或局部 patch 时间再送进 parser。

- [x] 2026-05-24：继续细化 `<reduced_diags_name>.filter_function(t,x,y,z,ux,uy,uz)`
  - 已补清这条 histogram parser filter 的更硬执行成本边界：它当前发生在任何落 bin 之前，因此即便粒子最终仍会因 bin 越界被丢弃，也已经先支付过 filter parser 求值成本。
  - 已补清更细的运行态结论：源码现在没有“先做几何/范围粗筛，再按需跑 filter”的快路径；1D 与 2D 路径都会先判 filter，再进入单轴或双轴落 bin 链。

- [x] 2026-05-24：继续细化 `<reduced_diags_name>.normalization`
  - 已补清这条 1D `ParticleHistogram` 归一化模式的更硬零直方图护栏：`max_to_unity` 和 `area_to_unity` 当前都先要求全局最大值或总面积严格大于 `numeric_limits<Real>::min()`，否则根本不会进入除法缩放。
  - 已补清更细的运行态结论：因此当本输出步 histogram 仍全零、或总面积太小，这两种模式会静默保留全零 `m_data`，而不是产生 NaN/Inf，也不会强制归一成某个默认形状。

- [x] 2026-05-24：继续细化 `warpx.reduced_diags_names`
  - 已补清这张 reduced-diag 名字表的更硬 manager-side 容器语义：源码当前既不排序也不去重，而是按原顺序直接 `std::transform(..., back_inserter(m_multi_rd), ...)`，后续所有 manager fanout 也都按同一索引顺序遍历。
  - 已补清更细的运行态结论：重复写同一个 `rd_name` 时，会 materialize 成多个独立实例，但它们共享同一份 `ParmParse(rd_name)` 配置和同一路径落点；构造期通常只会有第一份实例写 header，后续 `ComputeDiags()/WriteToFile()` 则会被 manager 重复 fanout 到同一文件或 series 根路径。

- [x] 2026-05-24：继续细化 `<reduced_diags_name>.species`
  - 已补清这条 species 绑定键的更硬 `BeamRelevant` 错名边界：当前它在 `ComputeDiags()` 里只会静默跳过所有不匹配 species，但不会在进入时先清零 `m_data`。
  - 已补清更细的运行态结论：因此如果此前某一步曾成功命中过目标 species，后续错名步会继续保留上一轮旧数据；只有从启动到当前都从未命中过时，输出才会保持初始化零值，而不是统一退化成“本步零输出”。

- [x] 2026-05-24：继续细化 `<reduced_diags_name>.type`
  - 已补清这条工厂分派键的更硬 openPMD-only deferred failure 边界：`reduced_diags_dictionary` 当前不会在构造期检查 `WARPX_USE_OPENPMD`，所以 `ParticleHistogram2D` 和 `DifferentialLuminosity2D` 即使所在二进制没编进 openPMD 支持，也仍会先通过 parser 和工厂分派，正常进入 `m_multi_rd`。
  - 已补清更细的运行态结论：这两类真正的能力失败会被延后到第一次命中各自 `WriteToFile()` 时，在 `#else` 分支里直接 abort，而不是在 startup 阶段被工厂提前拒绝。

- [x] 2026-05-24：继续细化 `reduced_diags.intervals`
  - 已补清这条节拍键的更硬 `FieldPoyntingFlux` 例外分支：`FieldPoyntingFlux::ComputeDiags()` 和 `ComputeDiagsMidStep()` 当前内部都不再检查 `m_intervals`，所以只要外层 manager 发生 fanout，它就会每步更新瞬时 Poynting flux 和累计能量损失。
  - 已补清更细的运行态结论：因此对 `FieldPoyntingFlux` 来说，`intervals` 当前切的是 `DoDiags(step)` 外层预判、implicit solver 路径里的 mid-step fanout，以及最终 `WriteToFile(step)` 的落盘时机，而不是积分量本身的每步累积。

- [x] 2026-05-24：继续细化 `reduced_diags.separator`
  - 已补清这条分隔符键的更硬 activation-vs-validity 风险：当前 `LoadBalanceCosts` 在最终补齐旧文件时不仅只按 `m_sep[0]` 重拆列，还没有任何 `m_sep.empty()` 防护。
  - 已补清更细的运行态结论：因此空字符串 separator 现在不是“退化为无分隔输出”或自动回退默认值，而是会把 `std::getline(..., m_sep[0])` 和 `ss.peek() == m_sep[0]` 这条再解析路径直接带进未防护的首字符访问。

- [x] 2026-05-24：继续细化 `reduced_diags.path`
  - 已补清这条路径键的更硬 continuation 语义分叉：基类文本 reduced-diag 当前只在构造期对 `m_path + m_rd_name + "." + m_extension` 做一次 `FileExists(...)` 检查，并据此设置 `m_write_header`；这套 header/restart 合同只覆盖单文件文本 writer。
  - 已补清更细的 2D openPMD 运行态结论：`ParticleHistogram2D` 和 `DifferentialLuminosity2D` 后续每次 `WriteToFile()` 都会重新对 `m_path + m_rd_name + "/" + filename` 调 `io::Series(..., Access::CREATE)`，真正延续的是 openPMD iteration 容器，而不是基类 `m_write_header` 那套文本续写语义。

- [x] 2026-05-24：继续细化 `reduced_diags.precision`
  - 已补清这条精度参数的更硬 dead-state 边界：即便用户显式给了 `<FieldProbe>.precision` 或 `<LoadBalanceCosts>.precision`，基类构造函数仍会把它正常解析并存进对象成员 `m_precision`。
  - 已补清更细的运行态结论：这两个 override 后续都写死 `std::setprecision(14)`，没有任何 downstream reader 再消费该成员，因此这类实例级精度配置当前不是 fallback，也不是报错，而是“成功解析但完全失活”的死状态。

- [x] 2026-05-24：继续细化 `reduced_diags.extension`
  - 已补清这条文本后缀合同的更硬 fanout 边界：基类 `ReducedDiags::WriteToFile()` 自己当前并没有 `IOProcessor()` 保护，真正保证文本 reduced-diag 文件只被单 rank append 的，是外层 `MultiReducedDiags::WriteToFile(step)` 在 manager 层先做 `if (!IOProcessor()) return;`。
  - 已补清更细的运行态结论：因此 `rd_name.extension` 这类文本文件的串行写盘合同当前是 manager 外包的，再叠加 `m_intervals.contains(step+1)` 过滤后才 fanout 到各实例 writer，而不是每个 reduced diag writer 自身内建的单-rank 保护。

- [x] 2026-05-24：继续细化 `<reduced_diags_name>.normalization`
  - 已补清这条 1D `ParticleHistogram` normalization 的更硬时序合同：`ComputeDiags()` 每次进入都会先 `std::fill(m_data, 0)` 清空 host 向量，再重建本步 histogram，之后才在 host 侧执行 `max_to_unity / area_to_unity` 归一化。
  - 已补清更细的输出结论：归一化完成后，同一步就会立即交给继承自 `ReducedDiags` 的文本 `WriteToFile(step)` 追加写盘，因此输出文件里的每一行都是“该输出步自己的归一化快照”，不是跨多个输出步累计后再统一缩放的分布。

- [x] 2026-05-24：继续细化 `<reduced_diags_name>.filter_function(t,x,y,z,ux,uy,uz)`
  - 已补清这条 1D `ParticleHistogram` filter 的更细生命周期边界：当前也不是“只有给了 filter 才构造 executor”，而是 `ComputeDiags()` 会先无条件执行 `compileParser(m_parser_filter.get())`，然后才靠 `do_parser_filter` 判定是否真的调用它。
  - 已补清更细的运行态结论：因此 1D 路径同样属于 compile-before-gate，而不是命中开关后才延迟 materialize；它和 2D sibling 共享这一前置生命周期，但后者被筛掉时切断的是更长的 `filter -> abs/ord -> value` companion 链。

- [x] 2026-05-24：继续细化 `<reduced_diags_name>.value_function/filter_function(t,x,y,z,ux,uy,uz,w)`
  - 已补清这组 `ParticleHistogram2D` companion 的更硬失败时序边界：虽然构造函数把 `value_function(...,w)` 表面上做成 `query(...)` 可选项，但若用户缺失这条值，`m_parser_value` 当前就不会被 materialize。
  - 已补清更细的运行态结论：`ComputeDiags()` 仍会在任何粒子筛选、双轴 histogram parser 求值或 bin 落点之前，先无条件执行 `compileParser(m_parser_value.get())`；因此现状不是“自动回退到默认权重”，而是把 `value_function` 缺失变成 `ComputeDiags()` 最前段的一条 hard failure path。

- [x] 2026-05-24：继续细化 `<reduced_diags_name>.integrate`
  - 已补清这条 `FieldProbe` 开关的更硬持久状态边界：`integrate=1` 时，`ComputeDiags()` 不是把时间积分先放在一次性输出缓冲里，而是直接把 `Ex/Ey/Ez/Bx/By/Bz/S` 的积分值累加写回 probe 粒子的 SoA 属性。
  - 已补清更细的运行态结论：`FieldProbeParticleContainer::AddNParticles(...)` 只在初始化时把这些属性置零一次，后续 `WriteToFile()` 和输出步之后都没有自动清零链；因此单行输出表示的是从 probe 建立以来持续累加到当前步的 running integral，而不是“本输出区间单独重新从 0 开始”的窗口积分。

- [x] 2026-05-24：继续细化 `<diag_name>.particle_fields_to_plot`
  - 已补清这条列表的更硬前置 materialization 顺序：当前只有 `particle_fields_to_plot` 非空时，`Diagnostics::BaseReadParameters()` 才会进入按 field 的 companion 解析循环，把 `m_pfield_do_average / m_pfield_strings / m_pfield_dofilter / m_pfield_filter_strings` 逐项 append。
  - 已补清更细的运行态结论：因此 `particle_fields_to_plot` 为空时，这四组 field-local parser companion 当前完全不会 materialize；但后面的 `particle_fields_species` 默认回退和名字校验链仍会独立执行，所以“没有任何 particle-field parser/materialization”与“仍因拼错的 species 列表直接 abort”在当前实现里可以同时成立。

- [x] 2026-05-24：继续细化 `<diag_name>.particle_fields_species`
  - 已补清这条 species 列表的更硬前置输入校验边界：当前即使 `particle_fields_to_plot` 为空，`Diagnostics::BaseReadParameters()` 也仍会先读取 `particle_fields_species`、默认回退成全部 species，并逐项校验名字是否合法。
  - 已补清更细的运行态结论：因此一个拼错的 `particle_fields_species` 仍会在这里直接 abort，而不会因为后续没有任何 `ParticleReductionFunctor` 要生成就被静默旁路；只有通过这层前置校验后，这条列表才继续参与后面的 `<field>_<species>` 名字展开和 species-index 快照绑定。

- [x] 2026-05-24：继续细化 `<diag_name>.particle_fields.<field_name>.filter(x,y,z,ux,uy,uz)`
  - 已补清这条 particle-field filter parser 的更硬 fanout 生命周期：当前不是“每个 `<field_name>.filter(...)` 全局只编译一次”，而是 `FullDiagnostics::InitializeFieldFunctors()` 会按 `level × particle-field × species` 三重 fanout 分别构造 `ParticleReductionFunctor`，所以同一条 filter 字符串会为每个 level、每个 species 各自重新 `compile<6>()` 一次。
  - 已补清更细的运行态结论：因此后续真正 materialize 的不是共享 filter executor，而是按 level/species 分裂开的多份样本筛选 executor；它们再继续走已有的“返回值等于 0 才剔除”和 `do_average=true` 时对同一粒子的两次 filter 求值链。

- [x] 2026-05-24：继续细化 `<diag_name>.particle_fields.<field_name>(x,y,z,ux,uy,uz)`
  - 已补清这条 particle-field parser 的更硬 fanout 生命周期：当前不是“每个 `<field_name>` 全局只编译一次”，而是 `FullDiagnostics::InitializeFieldFunctors()` 会按 `level × particle-field × species` 三重 fanout 分别 `make_unique<ParticleReductionFunctor>(...)`，所以同一条 parser 字符串会为每个 level、每个 species 各自重新构造并 `compile<6>()` 一次。
  - 已补清更细的运行态结论：因此后续真正 materialize 的不是共享 executor，而是按 level/species 重复编译的单标量 `ParticleReductionFunctor` map kernel；它再继续走已有的 `ncomp==1`、NGP cell 归属、细网格 `red_mf` 原子累加和后续 `Coarsen(...)` 链。

- [x] 2026-05-24：继续细化 `<diag_name>.plot_raw_fields`
  - 已补清这条 raw-field 开关的更硬 diagnostics 家族总 gate：当前真正只有 `FullDiagnostics::ReadParameters()` 会 `query("plot_raw_fields", ...)`，因此只有 full diagnostics 能被用户输入显式打开 raw-field 分支；`BTDiagnostics` 虽然在 flush 时也把同名成员传进 writer 签名，但没有对应 parser 入口，这个成员在当前实现里只保持头文件默认值 `false`。
  - 已补清更细的运行时闭包：因此 raw plotfile 子目录、checkpoint 兼容性破坏和 openPMD 的 `!plot_raw_fields && !plot_raw_fields_guards` 硬断言，当前都以 full diagnostics 为唯一可激活入口；plotfile 仍是唯一真实 consumer，checkpoint 仍整体忽略这两个布尔位。

- [x] 2026-05-24：继续细化 `<diag_name>.diag_hi`
  - 已补清这条 reduced-domain 上界的更硬 lifecycle：源码当前不会把原始 `diag_hi` 一直原样保留到 writer 末端；若用户未显式给出，它会先立刻退回 coarse-level `Geom(0).ProbHi()`，而不是继续保留文档层的 `+infinity`。
  - 已补清更细的 moving-window/runtime 改写链：若 boost-moving-window 与窗口方向一致，`BaseReadParameters()` 会先在 moving-window 方向做一次 `1 / [gamma * (1 - beta_boost * beta_window)]` 连续换算；进入 `InitBaseData()` 后，这个上界还会按当前窗口位移和 coarse cell size 再做一次整格平移。因此 field-side 后续真正消费的是“默认值/原始输入 + boost 换算 + restart 后整格平移”之后的运行态 `m_hi`。

- [x] 2026-05-24：继续细化 `<diag_name>.<species_name>.plot_filter_function(t,x,y,z,ux,uy,uz)`
  - 已补清这条 parser filter 在 pinned writer 路径上的更细 diagnostics 家族不对称：plotfile 顶层当前显式忽略 `use_pinned_pc`，因此它只会在普通 `pc` 路径和 `isBTD=true` 时的 `pinned_pc` 路径上命中 `ParserFilter`；openPMD 则还额外支持独立的 `use_pinned_pc` pinned 路径。
  - 已补清更硬的运行时结论：`BTDiagnostics` 传的是 `isBTD=true,use_pinned_pc=true`，所以 BTD 在 plotfile 和 openPMD 两条 writer 上都会命中 pinned parser-filter；相对地 `BoundaryScrapingDiagnostics` 传的是 `isBTD=false,use_pinned_pc=true`，因此同样的 pinned buffer 当前只会在 openPMD 上被这条 parser filter 消费，在 plotfile 侧并不存在对应的非-BTD pinned parser-filter 路径。

- [x] 2026-05-24：继续细化 `<diag_name>.<species_name>.uniform_stride`
  - 已补清这条 deterministic stride filter 的更细 activation-vs-validity 边界：`UniformFilter` 当前只有在 `m_do_uniform_filter=false` 时才会完全跳过 `p.id() % m_stride`；一旦激活，源码不会先检查 `m_stride > 0`，而是直接执行取模。
  - 已补清更硬的运行时结论：由于 plotfile/openPMD writer 的 filter lambda 用的是乘法链而不是 `&&` 短路，`uniform_filter` 会对每个候选粒子都被求值；因此 `uniform_stride=0` 当前不是“退化为不过滤”，而是会把运行时直接带进未防护的取模路径。

- [x] 2026-05-24：继续细化 `<diag_name>.<species_name>.random_fraction`
  - 已补清这条随机抽样的更细 activation-vs-result 不对称：`RandomFilter` 当前只有在 `m_do_random_filter=false` 时才会完全跳过 `amrex::Random(engine)`；一旦激活，即便 `m_random_fraction <= 0` 或 `>= 1` 已把接受结果钉成全拒绝或全接受，源码仍会先做一次随机数抽样再比较阈值。
  - 已补清更硬的运行时成本合同：由于 plotfile/openPMD writer 的 filter lambda 用的是 `random_filter * uniform_filter * parser_filter * geometry_filter` 而不是 `&&` 短路，这条参数一旦激活，就会在每个候选粒子上持续消耗 RNG，即使该粒子随后会被其它 filter 拒绝。

- [x] 2026-05-24：继续细化 `<diag_name>.<species_name>.additional_variables`
  - 已补清这组 `phi/E/B` 附加字段的更硬调用点边界：当前固定 `use_pinned_pc=true` 的不只是 BTD，boundary-scraping 也同样如此；而 `WarpXOpenPMD.cpp` 在调用 `storePhiOnParticles()/storeFieldOnParticles()` 时会把 `!use_pinned_pc` 传成 `is_full_diagnostic`。
  - 已补清更强的运行时结论：因此这组附加字段在当前实现里真正能合法 materialize 成输出列的，其实只剩 full openPMD 粒子诊断；BTD 和 boundary-scraping 会因 pinned 路径撞上同一组断言，plotfile 仍完全不调用这两条 helper，checkpoint 也继续旁路。

- [x] 2026-05-24：继续细化 `<diag_name>.<species_name>.variables`
  - 已补清这条主列白名单在几何分支下的更硬反向边界：`variables[0] == "none"` 当前并不等于“最终没有任何 real 列”；在 `RZ/RCYLINDER` 下构造末尾仍会无条件把 `theta` 的 `m_plot_flags` 重新置回 `1`，`RSPHERE` 下还会额外强制 `phi`。
  - 已补清更细的 companion 闭包：`additional_variables` 不参与 `m_plot_flags` 主列重写，而是在 `variables` 处理完成后再单独补开 `phi/Ex/Ey/Ez/Bx/By/Bz` 布尔位；因此这条参数真实控制的是“主列重写 + 几何强制补列 + 附加字段后置叠加”，checkpoint 仍继续旁路这整套列选择合同。

- [x] 2026-05-24：继续细化 `<diag_name>.species`
  - 已补清这条列表在 BTD plotfile 路径里的更细顺序合同：`MergeBuffersForPlotfile(i_snapshot)` 当前不是按名字重新查找 species，而是直接用同一索引 `i` 同步访问 `m_output_species_names[i]`、`m_particles_buffer[i_snapshot][i]` 与对应 snapshot 子目录；因此 species 一旦定型，顺序本身就成为目录、Header 合并和 particle-buffer 对位关系的一部分。
  - 已补清更硬的零粒子反向边界：BTD 首轮 flush 仍会先按这份顺序为每个 species 创建目录并写 Header，只有之后才在 `m_total_particles == 0` 时跳过 `Particle_H / DATA_*` 的 rename-interleave；相对地 boundary-scraping 仍会在 writer 调用前因总粒子数为零而整体 `return`，连 per-species 目录都不会生成。

- [x] 2026-05-24：继续细化 `<diag_name>.write_species`
  - 已补清这条粒子总 gate 在 BTD 路径里的更细 companion 覆盖关系：`BTDiagnostics::ReadParameters()` 虽然允许用户单独给 `do_back_transformed_particles`，并用它和 `do_back_transformed_fields` 一起通过早期断言，但到 `DerivedInitData()` 真正运行态的 `m_do_back_transformed_particles` 会被 `write_species + m_output_species_names` 重新覆盖计算。
  - 已补清更硬的运行时结论：即使用户前面显式给了 `do_back_transformed_particles=1`，只要 `write_species=0` 或 species 名单为空，BTD 仍不会调用 `SetDoBackTransformedParticles(...)`；因此这条 BTD 粒子总 gate 当前不是早期布尔输入位的原值，而是 `write_species` 派生出来的覆盖值。

- [x] 2026-05-24：继续细化 `<diag_name>.diag_lo`
  - 已补清这条 reduced-domain companion 的更细 particle-geometry 不对称：`diag_lo/hi` 当前虽然会统一把 `ParticleDiag::m_do_geom_filter` 打开，但真正把 `m_geom_output[i_buffer][0].ProbDomain()` 写进 `ParticleDiag::m_diag_domain` 的只有 `FullDiagnostics::PrepareFieldDataForOutput()`。
  - 已补清 BTD 侧的更硬反向边界：`BTDiagnostics::PrepareFieldDataForOutput()` 只准备 cell-centered field buffer 与 snapshot/buffer geometry，不会给粒子 diagnostics materialize 这份 domain；再结合 reduced-domain 路径里随后对 `m_output_species` 的清空，BTD/current reduced-domain 粒子 copy 链实际上不会走到有效 geometry-filter 执行阶段。

- [x] 2026-05-24：继续细化 `<diag_name>.file_prefix`
  - 已补清这条输出前缀在 BTD plotfile 路径里的更硬目录物化时序：`MergeBuffersForPlotfile(i_snapshot)` 当前虽然每次都继续用 `snapshot_path = Concatenate(m_file_prefix, i_snapshot, ...)` 组织最终 snapshot 根目录，但真正的 `CreateDirectory(...)` 只在首个 buffer flush 或 restart 后第一次 flush 时发生。
  - 已补清更细的 runtime 合同：后续 buffer merge 只是继续向同一个 `snapshot_path/Level_0` 与各 species 子目录追加或改写 `Header / Cell_* / Particle_* / DATA_*`，不会每次重新建整棵目录树；因此这条前缀在 BTD plotfile 下承载的不只是 per-buffer/per-snapshot 命名语义，也承载一次性目录物化边界。

- [x] 2026-05-24：继续细化 `<diag_name>.file_min_digits`
  - 已补清这条 diagnostics 编号宽度参数在 openPMD 路径里的更细编码边界：虽然外层 `FlushFormatOpenPMD` 仍会统一先算 `Concatenate(prefix, iteration[0], file_min_digits)`，但真正写进最终 series 容器名只发生在 `WarpXOpenPMDPlot::GetFileName()` 的 `fileBased` 分支；`groupBased` 和 variable-based 编码当前不会把这条位数带进最终 openPMD 文件模板。
  - 已补清更细的 in-situ 反向 consumer：`FlushFormatCatalyst::WriteToFile()` 当前在 writer 末尾直接 `ignore_unused(prefix, plot_raw_fields, file_min_digits, plot_raw_fields_guards)`，因此它不会进入 Catalyst pipeline 的任何持久化或 bridge 命名；`FlushFormatAscent` 与 `FlushFormatSensei` 虽然也会先用它构造日志级 `filename`，但后续真正 publish/update 的 conduit mesh 或 SENSEI bridge 都不会继续消费这条编号宽度。

- [x] 2026-05-24：继续细化 `<diag_name>.coarsening_ratio`
  - 已补清这条 diagnostics 网格缩放键的更硬 BTD 前置约束：`BTDiagnostics::ReadParameters()` 会在真正进入任何 buffer/functor 几何构造前就强制 `m_crse_ratio == IntVect(1)`，因此 BTD 当前不是“受限支持某些 coarsening”，而是直接只允许恒等变换。
  - 已补清更细的 runtime 反向边界：后续 BTD 路径里虽然仍能看到 `ba.coarsen(m_crse_ratio)`、`CellCenterFunctor(..., m_crse_ratio)`、`RhoFunctor(..., m_crse_ratio)` 等调用，但在当前实现里都已经被这条前置断言压成恒等操作；boundary scraping 和常规 per-particle writer 仍不消费这条参数。

- [x] 2026-05-24：继续细化 `<diag_name>.plot_raw_fields_guards`
  - 已补清这条 raw-field guard 开关的更硬总 gate：它虽然会和 `plot_raw_fields` 一起把 `raw_specified` 置真、从而破坏 checkpoint 兼容性，并在 openPMD 路径上一起触发断言，但本身不会单独触发 raw-field 输出。
  - 已补清更细的 plotfile writer 边界：`FlushFormatPlotfile` 只有在 `plot_raw_fields=1` 时才把 `"raw_fields"` 加入 root components，`WriteAllRawFields(...)` 也会在 `!plot_raw_fields` 时立刻返回；因此 `plot_raw_fields_guards=1, plot_raw_fields=0` 当前不会单独生成 `raw_fields/` 目录或任何原始场写出。

- [x] 2026-05-24：继续细化 `<diag_name>.particle_fields.<field_name>.filter(x,y,z,ux,uy,uz)`
  - 已补清这条 particle-reduction filter 的更硬布尔合同：当前不是按“非零为真”泛化解释，而是只把 `filter_fn(...) == 0` 视为剔除条件；非零返回值都会通过筛选。
  - 已补清更细的 runtime 成本边界：`do_average=1` 时，源码不会缓存第一次筛选结果；同一个粒子的 `filter_fn(...)` 会在分子 `red_mf` 和分母 `ppc_mf` 两条 `ParticleToMesh(...)` 路径里各自重新求值一次。

- [x] 2026-05-24：继续细化 `<diag_name>.particle_fields.<field_name>.do_average`
  - 已补清这条 particle-reduction averaging 开关的更硬数学合同：`do_average=1` 当前并不是按粒子个数做平均，而是按宏粒子权重 `w` 做加权平均；第一遍累积 `w * value`，第二遍对同一筛选样本集合累积 `w * filter` 作为分母。
  - 已补清更细的 runtime 边界：真正的归一化仍发生在细网格 `red_mf` 上的 tile 级逐 cell 后处理里，零分母 cell 会被直接置零；`do_average=0` 则完全旁路这条分母场和归一化链，只保留原始加权求和。

- [x] 2026-05-24：继续细化 `<diag_name>.particle_fields_species`
  - 已补清这条 particle-reduction species 列表的更硬 runtime 绑定边界：它当前不会在 functor 运行时再按字符串重查 species，而是先在 `BaseReadParameters()` 里缓存成 `m_pfield_species_index` 整数索引快照，后续 `ParticleReductionFunctor` 真正消费的是这份索引。
  - 已补清更细的 RZ/openPMD 不对称边界：每个 `<field>_<species>` 名字仍会继续走 `AddRZModesToOutputNames(...)` 做多模展开，但真正 functor 计数只按 `m_pfield_varnames.size() * m_pfield_species.size()` 计算，不会随 mode 数一起扩张；BTD 路径则仍因 `particle_fields_to_plot` 的硬断言而整体旁路这条 species 绑定链。

- [x] 2026-05-24：继续细化 `<diag_name>.particle_fields_to_plot`
  - 已补清这条 particle-reduction 入口的更硬 RZ/openPMD 不对称边界：解析期虽然会对粒子场给出“只输出 0th mode”的 warning，但 `FullDiagnostics::InitializeFieldFunctorsRZopenPMD()` 仍会对同一组 `<field>_<species>` 调 `AddRZModesToOutputNames(...)` 做多模名字展开。
  - 已补清更细的 runtime 反向边界：`ParticleReductionFunctor` 构造函数又硬断言 `ncomp == 1`，因此运行时真正 materialize 的仍是单分量粒子归约 functor，而不是与 `E/B/J` 对齐的真正多模粒子场 functor 链；BTD 路径则继续对 `particle_fields_to_plot` 做硬断言禁止。

- [x] 2026-05-24：继续细化 `<diag_name>.adios2_engine.parameters.*`
  - 已补清这批 ADIOS2 engine 参数的更硬 JSON 入口：它们当前仍由 `FlushFormatOpenPMD` 整体抓取并去前缀后写进 `engine_parameters`，随后在 `detail::getSeriesOptions(...)` 中 materialize 成 `"adios2" -> "engine" -> "parameters"`；即使 `engine.type` 为空，只要参数表非空，`"engine"` 块仍会继续存在。
  - 已补清更细的 BTD flush consumer：普通 `seriesFlush(isBTD=true)` 固定发的是 `preferred_flush_target="buffer"`；到了 `FlushBTDToDisk()`，源码不是结构化解析这些参数，而只是对最终的 `m_OpenPMDoptions` 做 `"FlattenSteps"` 子串搜索。只有在 `ADIOS2` backend 且命中该字符串时才切到 `"new_step"`，否则统一走 `"disk"`。

- [x] 2026-05-24：继续细化 `<diag_name>.adios2_engine.type`
  - 已补清这条 ADIOS2 engine companion 的更硬 JSON-materialization 边界：它当前只在 `FlushFormatOpenPMD` 构造期被收集和透传，不会像 `openpmd_backend` 那样 fallback 或回写进 `ParmParse`，也不会在本地校验与 backend/encoding 的兼容性。
  - 已补清更细的反向边界：在 `detail::getSeriesOptions(...)` 里，它只负责 materialize `"adios2" -> "engine" -> "type"` 这一子键；即使 `engine_type` 为空，只要 `adios2_engine.parameters.*` 非空，源码仍会继续生成 `"engine"` 块并把它写进 `m_OpenPMDoptions`，所以它不是 engine JSON 是否存在的总 gate。

- [x] 2026-05-24：继续细化 `<diag_name>.openpmd_backend`
  - 已补清这条 openPMD backend 键的更硬 resolved-backend 边界：它当前不只会在 `FlushFormatOpenPMD` 构造期从 `"default"` fallback 到 `WarpXOpenPMDFileType()` 选出的具体 backend，还会通过 `pp_diag_name.add("openpmd_backend", ...)` 把这份 resolved backend 回写进 diagnostics 自己的 `ParmParse` 状态；因此后续同一实例继续看到的已不是 `"default"`。
  - 已补清更细的 compatibility / runtime 边界：`bp/bp5 + groupBased` 当前会在同一构造链上直接抛异常，而 `BackTransformed` 的 streaming/variable-based 编码也会先 warning 再强制改回 `groupBased`；更下游这份 resolved backend 才继续进入 `WarpXOpenPMDPlot` 的文件模板后缀和 `openPMD::Series(...)` 的 MPI/非 MPI backend 实例化链。

- [x] 2026-05-24：继续细化 `<diag_name>.diag_type`
  - 已补清这条 diagnostics 总键的更硬类分派边界：`TimeAveraged` 当前不会生成独立 diagnostics 子类，而是继续落到 `FullDiagnostics`；随后只通过 `m_sum_mf_output`、`ComputeAndPack()` 里的 `Saxpy(...)` 和 `Flush()` 的 averaging 分支 materialize 成时间平均输出。
  - 已补清更细的 runtime fanout / 反向边界：`BackTransformed` diagnostics 会在 `MultiDiagnostics::FilterComputePackFlush(...)` 里被单独分流，普通 diagnostics flush pass 会显式跳过它；`BoundaryScraping` 则更早在 `DoComputeAndPack()` 上恒为 `false`，不走普通 field-functor / `m_mf_output` 打包链。

- [x] 2026-05-24：继续细化 `<collision_name>.Z`
  - 已补清这条 Bremsstrahlung companion 的更硬构造期边界：它当前只在 `UploadCrossSection(Z)` 命中一次，不只是检查 `m_kdsigdk_map` 是否存在对应条目，还会按 `Z^2 / beta^2` 缩放该 `Z` 的 host 截面表，并预积分出默认 cutoff 下的 `m_sigma_total_h`。
  - 已补清更细的 materialization / runtime 边界：随后源码会一次性分配并上传 `m_kdsigdk_d / m_sigma_total_d` 等 device 缓存，并把 executor 指针回绑到这套数组上；后续 `CalculateCrossSection()` 和 `Photon_energy()` 只复用这些已 materialize 的表，不会再次读取原始 `Z`。

- [x] 2026-05-24：继续细化 `<collision_name>.multiplier`
  - 已补清这条 Bremsstrahlung companion 的更硬双 consumer 边界：`fmulti = multiplier` 先在 `BremsstrahlungEvent(...)` 里放大 pair 级事件命中概率，命中后又把 `w_photon = weight1 / fmulti` 写进 `p_pair_reaction_weight`。
  - 已补清更细的下游合同：`PhotonCreationFunc` 后续会先复用这份 `wp` 更新父电子/离子 recoil，若 `create_photons=1` 才再把同一份 `wp` 写成 photon 权重；相对地，这条倍率不会进入 `CalculateCrossSection()` 或 `Photon_energy(...)`，因此不会改 photon 能谱采样或截面重积分本身。

- [x] 2026-05-24：继续细化 `<collision_name>.scattering_angle_model`
  - 已补清这条 fusion companion 的更硬默认边界：当前默认真值不是文档口径，而是 `ScatteringAngleModel::Default = Isotropic`；只有 proton-boron 和 two-product fusion 两类 collision 会在 `ParticleCreationFunc` 构造期继续 query 这条枚举，`linear_breit_wheeler / linear_compton` 虽然复用同一 product-creation 壳层，但不会消费它。
  - 已补清更细的 runtime / 反向边界：更下游 `TwoProductComputeProductMomenta(...)` 才真正按 `Isotropic / Forward` 在质心系里切换产物发射角模型；相对地 proton-boron 路径里这条值只控制第一步 `p + B -> alpha + Be*` 的 two-product 子反应，后续 `Be* -> 2 alpha` 衰变仍固定各向同性，不会继续复用 `scattering_angle_model`。

- [x] 2026-05-24：继续细化 `<collision_name>.max_background_density`
  - 已补清这条 `BackgroundMCC` companion 的更硬构造期边界：它不是 `background_density` 的冗余别名，而是接受-拒绝上界链专用的一次性密度上限。只有当 `background_density` 走常数路径且用户没显式给这条值时，源码才会自动回退成该常数；相对地 parser 密度路径若缺这条 companion，构造期就会因 `m_max_background_density <= 0` 直接 abort。
  - 已补清更细的 runtime consumer：后续真正使用这条值的不是逐粒子局域密度求值，而是 `init_flag == false` 的首轮预估链；`get_nu_max(...)` 会用它分别建出 `m_nu_max / m_nu_max_ioniz`，再 materialize 成 `m_total_collision_prob / m_total_collision_prob_ioniz`。tile kernel 之后只继续用局域 `n_a * sigma(E) * v / nu_max` 做归一化通道选择，不会每步重算这条密度上界。

- [x] 2026-05-24：继续细化 `<collision_name>.CoulombLog / use_global_debye_length`
  - 已补清这对 pairwise-Coulomb companion 的更硬分叉：`CoulombLog < 0` 当前不会单独直接落到自动估算，而是还要继续看 `use_global_debye_length`；只有在 `CoulombLog < 0 && !use_global_debye_length` 时，functor 才会打开 `m_computeSpeciesTemperatures`，让 `BinaryCollision::doCollisionsWithinTile(...)` 为每个 cell 额外做局部温度预计算链。
  - 已补清 `use_global_debye_length` 的更细替代链：只要这条为真，就会抑制上面的局部温度估算路径，改走 `CollisionHandler` 的 handler-wide `GenerateGlobalDebyeLength()` pre-pass；`MultiParticleContainer` 随后会按 level 懒分配 `global_debye_length` MultiFab、累加全部带质量且带电容器的 `1/L_De^2` 再开平方，而 cell-level `ElasticCollisionPerez(...)` 最终读取的是这张全局 Debye 长度场里的 `global_lamdb`。

- [x] 2026-05-24：继续细化 `collisions.collision_names`
  - 已补清这组 collision 名字列表的更硬 handler-wide 状态边界：它当前不只决定 `collision_types/allcollisions` 的定长 registry，还会在构造期把各对象的 `use_global_debye_length()` 聚合进单个 `m_use_global_debye_length`。
  - 已补清更细的每步 shared pre-pass：`CollisionHandler::doCollisions(...)` 不会直接只按名字逐个调用，而是先在外层统一执行一次 QED virtual-photon regeneration；随后仅当任一 collision 需要 global Debye length 时，再统一调用一次 `mypc->GenerateGlobalDebyeLength()`；这些 handler 级预处理之后，才按 `allcollisions` 顺序把各自的 `ndt`/stepping mode 应用到具体 fanout。

- [x] 2026-05-24：继续细化 `<collision_name>.type`
  - 已补清这条 collision 类型键的更硬默认边界：默认值 `pairwisecoulomb` 当前是真正生效的 legacy fallback，未显式给 `type` 的 collision 会直接 materialize 成 pairwise Coulomb，而不是报未知类型。
  - 已补清更细的总分派链：`CollisionHandler` 在任何具体类型实例化前都会先强制 `warpx.n_rz_azimuthal_modes == 1`；随后第一层工厂负责把字符串分派到 `BackgroundMCC / PulsedDecay / BackgroundStopping / DSMC / nuclearfusion / bremsstrahlung / linear_breit_wheeler / linear_compton` 等对象，而 `BinaryCollisionUtils::get_collision_type(...)` 还会继续对 `nuclearfusion`、`linear_breit_wheeler`、`linear_compton` 做 incident/product species 组合细分与合法性检查。

- [x] 2026-05-24：继续细化 `<collision_name>.species`
  - 已补清这组 collision species 名单的更硬家族约束：`BinaryCollision` 当前强制恰好两条 species，`PulsedDecay` 强制恰好一条，`BackgroundStopping` 只消费第一条，因此它不是统一长度的纯名字表。
  - 已补清更细的 same-species / tile-share 运行边界：`BinaryCollision` 会先据此生成 `m_isSameSpecies`，same-species 时只走单一容器、单一 tile 和单一 `findParticlesInEachCell(...)` 路径，并且只对 `species1` 执行一次 `deleteInvalidParticles()`；异 species 时才并行展开两套容器/tiles/bins。`BackgroundMCC` 还保留 same-species hack：两条名字相同时，`species2` 会直接绑定回 `species1` 本身，而不是第二个独立背景容器。

- [x] 2026-05-24：继续细化 `<collision_name>.product_species`
  - 已补清这组 collision 产物名单的更硬构造期分叉：DSMC 当前不会原样保留用户输入，而是先按 ionization target 需要重排 incident species，再把两条 colliding species prepend 到 `m_product_species` 前面形成完整 product-slot 列表；相对地，若当前 collision functor 根本不产生新粒子，`BinaryCollision` 会因用户仍给了 `product_species` 而在构造期直接 abort。
  - 已补清更细的 tile 级 append/writeback 链：generic `BinaryCollision` 会为每个 product slot `defineAllParticleTiles()`、`resize(products_np + num_added)`、用 `SmartCopy` 追加新粒子，再统一执行 `DefaultInitializeRuntimeAttributes(...)` 和 `setNewParticleIDs(...)`；`PulsedDecay` 则并行地对 `productA/productB` 两个目标 tile 单独 `resize + append + runtime-attribute init + setNewParticleIDs`，并在构造期继续强制总电荷与总质量守恒。

- [x] 2026-05-24：继续细化 `<collision_name>.ndt_supercycle / ndt_subcycle`
  - 已补清这对 collision stepping companion 的更硬默认边界：`CollisionBase` 默认就把 `m_ndt=1`、`m_collision_stepping_mode=Supercycle` 设好，因此未显式给 `ndt_*` 当前等价于“每个 PIC 步执行一次 supercycle collision”，不是没有 stepping mode。
  - 已补清更细的 runtime 时序分叉：`ndt_supercycle` 只会在 `step % ndt == 0` 的步上执行一次，并把 `dt_collision` 合并成 `dt*ndt`、但保留当前 PIC 步起点 `cur_time`；`ndt_subcycle` 则会把单步拆成多个 `dt/ndt` 子步，并让 collision 内部时间依赖沿 `cur_time + i_sub*dt_sub` 前进。相对地，`CollisionHandler` 外层每步的 virtual-photon regeneration 和可选 `GenerateGlobalDebyeLength()` 都不会跟着某个 collision 的 stepping mode 一起跳过或重复。

- [x] 2026-05-24：继续细化 `particles.E/B_ext_particle_init_style`
  - 已补清这对粒子外加场风格的更硬 gather-kernel 不对称：parser 分支在 `ReadParameters()` 里只缓存 `Parser`，真正 `compile<4>()` 要等到 `GetExternalEBField`；`repeated_plasma_lens` 继续走逐粒子 gather-time 修正；而 `read_from_file` 会在 `GetExternalEBField` 里显式退回 `ExternalFieldInitType::None`，不会在 gather kernel 里直接加场。
  - 已补清更细的 `aux` 场布局与 runtime 混入链：`read_from_file` 命中后，`WarpX.cpp` 会让 level-0 `Efield_aux/Bfield_aux` 从 alias `fp` 主场改成独立分配，并按 metadata 数量分配多分量 `E/B_external_particle_field`；随后 `WarpXInitData.cpp` 读入每个 component，`WarpXComm.cpp::UpdateAuxilaryData()` 再按 `time_executor(t_new[lev])` 做 `Saxpy`，把这些文件场混入粒子真正 gather 的 `aux` 场。

- [x] 2026-05-24：继续细化 `warpx.maxlevel_extEMfield_init`
  - 已补清这条 external-grid 初始化上界的更硬共有 gate：constant 和 parser 外场分支当前都只有在 `lev <= maxlevel_extEMfield_init` 时才会真正进入初始化链。
  - 已补清更细的 E/B parser level 不对称：constant `E/B` 分支都从 `lev=0` 起命中；B-parser 分支明确要求 `lev>0`、完全跳过 level 0；E-parser 分支则允许从 level 0 起运行，只是在 `lev=0` 时只写 `Efield_aux`，到 `lev>0` 才再追加 `Efield_cp`。

- [x] 2026-05-24：继续细化 `warpx.E/B_external_grid`
  - 已补清这组 constant external-grid 向量的更硬初始化 consumer：在 constant branch 下会直接写入 `fp/aux/cp/avg` 多套场容器，不只是单一的 `fp` 主场。
  - 已补清更细的 moving-window 分叉：`shiftMF(...)` 只会把它们拿来填 `E/Bfield_fp` 和存在时的 `*_avg_*/*_cp` 新入窗背景，不会把这组常量重新回填给 `E/Bfield_aux`；若 parser/file 分支启用，它们则只继续充当默认背景，不再主导初始化写场。

- [x] 2026-05-24：继续细化 `warpx.E_ext_grid_init_style`
  - 已补清这条 external-E 初始化风格相对 external-B 的更硬构造期不对称：`constant` 才会强制读 `E_external_grid`，`parse_E_ext_grid_function` 会 materialize parser，但在 `RZ` 下当前会直接 abort，不像 `B` 那样 warning 后局部退化。
  - 已补清更细的 runtime/资源边界：`read_from_file` 同样会强制 `max_level == 0`，而且只有非 `default_zero/constant` 路径才会在 `AllocLevelMFs` 里真正分配 `Efield_fp_external`；相对地它不会继续参与 `do_divb_cleaning` 的默认推进链。

- [x] 2026-05-24：继续细化 `warpx.B_ext_grid_init_style`
  - 已补清这条 external-B 初始化风格的更硬构造期分派：`constant` 才会强制读 `B_external_grid`，`parse_B_ext_grid_function` 会立刻 materialize 三个 `amrex::Parser`，`read_from_file` 则只在这时继续 query `read_fields_from_path`。
  - 已补清更细的 runtime/资源分叉：`read_from_file` 会强制 `max_level == 0`；非 `default_zero/constant` 路径在条件满足时会把 `do_divb_cleaning` 默认推进到 external-projection cleaner，而且只有这些路径才会在 `AllocLevelMFs` 里真正分配 `Bfield_fp_external`。

- [x] 2026-05-24：继续细化 `warpx.mirror_z_npoints`
  - 已补清这条 mirror 离散厚度参数的更硬 per-level 边界：当前不是给出一个全局固定物理厚度，而是把同一个整数下界投影成每层不同的 `mirror_z_npoints * dz`。
  - 已补清更细的粗细层竞争关系：粗层上这条离散下界更容易覆盖 `mirror_z_width` 经 boost 后得到的连续厚度；细层上由于 `dz` 更小，它会更弱，更可能由连续 `z_max_tmp` 主导。

- [x] 2026-05-24：继续细化 `warpx.mirror_z_width`
  - 已补清这条 mirror 厚度参数的更硬 boosted-frame 边界：源码会把 `z_min` 和 `z_max_tmp = z_min + mirror_z_width` 一起做 `z/gamma_boost - c beta_boost t` 变换，因此连续物理厚度先收缩成 `mirror_z_width / gamma_boost`，不是简单平移。
  - 已补清更细的 companion 分叉：这个 boost 后的连续厚度还要再与 `mirror_z_npoints * dz` 的离散下界取 `max(...)`，所以它不是最终清零厚度本身，而是进入 per-level 最终 `z_max` 之前的连续物理厚度输入。

- [x] 2026-05-24：继续细化 `warpx.num_mirrors`
  - 已修正这条 mirror gate 的更硬 evolve-scheme 边界：源码当前只在 `SemiImplicitEM` 和 `ThetaImplicitEM` 下强制 `num_mirrors=0`，不是对所有 implicit-like 路径一概禁用。
  - 已补清更细的 runtime/family 分叉：`ApplyMirrors()` 会先施加 `mirror_z_npoints * dz` 的最小厚度下界；随后 fine patch 始终清零 `E/B`，`F/G` 只在相关 div-cleaning 字段存在时命中，而 coarse patch 的对应清零又只在 `lev > 0` 时发生。

- [x] 2026-05-24：继续细化 `lasers.deposit_on_main_grid`
  - 已补清这条 laser side-list 的更硬分区边界：`Partition.cpp` 当前只会在 `lev > 0` 时把 `nfine_current` 置零，不会同步清掉 `nfine_gather`，因此它切的是沉积分区，不是场 gather 分区。
  - 已补清更细的 fine/buffer 写回分叉：level>0 的 laser 粒子仍会完整走本层 `calculate_laser_plane_coordinates -> fill_amplitude -> update_laser_particle`，只是 fine-path 的 `rho_fp/current_fp` 沉积会被置成零长度，source 写回改走 `rho_buf/current_buf` 的 coarse-buffer 路径。

- [x] 2026-05-24：继续细化 `<laser_name>.min_particles_per_mode`
  - 已补清这条 RZ laser spoke 参数的更硬 consumer 边界：当前只在 `n_rz_azimuthal_modes > 1` 的 spoke 铺点链里真正命中，不是通用 profile 参数。
  - 已补清更细的多路 consumer：它既决定 `n_spokes = (n_modes-1)*min_particles_per_mode`，也同时进入 `phase = 2π*spoke/n_spokes` 的角离散和 `r_weight = m_weight*2πr/n_spokes` 的每 spoke 权重分摊；因此提高它会线性增加 spoke 粒子数，但保持同一半径整圈总权重不变。

- [x] 2026-05-24：继续细化 `<laser_name>.do_continuous_injection`
  - 已补清这条 laser 连续注入开关的更硬一次性建粒边界：`ContinuousInjection(injection_box)` 当前只会在 `m_updated_position` 首次进入注入小盒时调用一次 `InitData()`，不是每步重复建粒。
  - 已补清更细的不对称运行态边界：`UpdateAntennaPosition(dt)` 只在 `do_continuous_injection && gamma_boost > 1` 时才真正回推 `m_updated_position`，纯实验室系连续注入不会在这里自发移动；同时 `TotalNumberOfParticles()==0` 后直接 `m_enabled=false` 的永久禁用链只在 `!do_continuous_injection` 时触发。

- [x] 2026-05-24：继续细化 `<laser_name>.phi2`
  - 已补清这条 Gaussian temporal-chirp 参数的更硬 direct-consumer 边界：当前不会单独进入 `oscillation_phase`、`prefactor`、横向 `exp_argument`，也不会直接出现在逐粒子 `stc_exponent` 的括号项里；它唯一的直接入口是 `stretch_factor` 的虚部修正。
  - 已补清更细的间接 runtime 链：这条值随后只会通过 `1/stretch_factor` 这层复系数间接传播到所有粒子的 `stc_exponent`，因此它先命中 chirp 复时间展宽层，再间接改写 STC 包络衰减。

- [x] 2026-05-24：继续细化 `<laser_name>.beta`
  - 已补清这条 Gaussian angular-dispersion 参数的更硬 consumer 边界：当前不会单独进入 `oscillation_phase`、`prefactor` 或横向 `exp_argument`，而是只挂在 STC/chirp 复时间包络链上。
  - 已补清更细的三路分叉：它会以一次项 `zeta + beta*focal_distance` 进入 `stretch_factor` 的 STC 时间展宽，以线性项 `beta*k0*(Xp cosθ + Yp sinθ)` 进入逐粒子时间偏移，又以平方项 `beta^2*k0*focal_distance` 和 `phi2` 一起进入 chirp 修正。

- [x] 2026-05-24：继续细化 `<laser_name>.zeta`
  - 已补清这条 Gaussian spatial-chirp 参数的更硬 consumer 边界：当前不会单独进入 `oscillation_phase`、`prefactor` 或横向 `exp_argument`，而是只挂在 STC/chirp 时间包络链上。
  - 已补清更细的符号分叉：源码在 `stretch_factor` 里使用 `zeta + beta*focal_distance`，到了逐粒子 `stc_exponent` 里却改成 `zeta - beta*focal_distance`；因此它分别进入“复时间展宽”和“横向-时间复耦合”两条不同物理链，不是同一组合的重复出现。

- [x] 2026-05-24：继续细化 `<laser_name>.stc_direction`
  - 已补清这条 Gaussian STC 方向参数的更硬初始化边界：当前会先归一化，并与 `nvec` 做正交性检查；若不在激光平面内就直接 abort，因此它不是任意三维向量。
  - 已补清更细的几何/runtime 分叉：`3D` 路径下它会进一步 materialize 成 `theta_stc = acos(dot(stc_direction, p_X))`，低维则直接退化成 `theta_stc = 0`；运行期真正被 kernel 消费的是这份 `theta_stc` 对应的平面投影，它会同时进入 `beta*k0(...)` 的时间偏移项和 `2i(...)*(zeta-beta*focal_distance)*inv_complex_waist_2` 的复耦合项。

- [x] 2026-05-24：继续细化 `<laser_name>.profile_focal_distance`
  - 已补清这条 Gaussian 焦距参数的更硬 consumer 分叉：当前不会单独进入 `oscillation_phase` 或 `t_prefactor`，而是先直接进入 `diffract_factor` 这条复衍射尺度链。
  - 已补清更细的多路 consumer 与反向边界：它随后会通过 `prefactor` 继续控制 diffraction/Gouy/波前曲率，同时又以 `beta * focal_distance` 和 `beta^2 * k0 * focal_distance` 的形式进入 `stretch_factor` 与逐粒子 `stc_exponent`；相对地，它不会像 `profile_waist` 那样直接单独出现在横向 `exp_argument` 中。

- [x] 2026-05-24：继续细化 `<laser_name>.profile_waist`
  - 已补清这条 Gaussian 几何尺度参数的更硬 consumer 分叉：当前不会单独进入 `oscillation_phase` 或 `t_prefactor`，而是先生成 `diffract_factor -> inv_complex_waist_2` 这条复几何尺度链。
  - 已补清更细的多路 consumer：`diffract_factor` 会进入 `prefactor` 的 diffraction/Gouy 修正，而同一份 `inv_complex_waist_2` 又继续同时进入 `stretch_factor`、逐粒子 `stc_exponent` 和横向 `exp_argument`。

- [x] 2026-05-24：继续细化 `<laser_name>.profile_duration`
  - 已补清这条 Gaussian 时间尺度参数的更硬 consumer 分叉：当前不会进入 `oscillation_phase` 或 `t_prefactor`，而是先统一压成 `inv_tau2 = 1/duration^2`。
  - 已补清更细的双重时间包络链：这份 `inv_tau2` 会同时进入 `stretch_factor` 和逐粒子 `stc_exponent`，因此它通过共享时间尺度链共同控制 temporal envelope 与 STC/chirp 展宽，而不会单独改写 diffraction 或横向 `exp_argument`。

- [x] 2026-05-24：继续细化 `<laser_name>.phi0`
  - 已补清这条 Gaussian 相位参数的更硬 lab-frame 时间边界：`fill_amplitude()` 当前比较它的时间基准同样不是原始 step-loop 时间，而是 `LaserParticleContainer::Evolve()` 在 boost 情况下先换回的 `t_lab`。
  - 已补清更细的 consumer 分叉：这条值当前只会进入 `oscillation_phase -> t_prefactor` 这条 carrier 相位链，不会继续进入 `stretch_factor`、`stc_exponent` 或横向 `exp_argument`。

- [x] 2026-05-24：继续细化 `<laser_name>.profile_t_peak`
  - 已补清这条 Gaussian 时间参数的更硬 lab-frame 边界：`fill_amplitude()` 当前比较的不是原始 step-loop 时间 `t`，而是 `LaserParticleContainer::Evolve()` 在 boost 情况下先换回的 `t_lab`；因此 `profile_t_peak` 的基准始终是激光 profile 的 lab-frame 物理时间。
  - 已补清更细的双重 consumer：这条值仍会同时进入 `oscillation_phase` 和 `stc_exponent` 两条公式链，不只是单独控制 carrier phase 或 envelope 其中之一。

- [x] 2026-05-24：继续细化 `<laser_name>.binary_file_name`
  - 已补清这条值的更硬 backend header 边界：`parse_binary_file()` 当前在 IO rank 上不只检查文件存在，还会强制要求 uniform-grid flag 为真，并按编译维度对 header 里的 `ny` 施加硬约束，然后才广播 `nt/nx/ny/t_min...` 这些元数据。
  - 已补清更细的 chunk-buffer/offset lifecycle：初始化期会立刻预读首块并建立 `E_binary_data` buffer；后续每次 `read_binary_data_t_chunk()` 都会重新打开文件，并按维度分叉的 `seekg` 偏移公式跳过 header 与前面时间片，再重建当前 chunk buffer。

- [x] 2026-05-24：继续细化 `<laser_name>.lasy_file_name`
  - 已补清这条值的更硬 backend 几何边界：`parse_lasy_file()` 当前只在 IO rank 真正打开 openPMD `Series` 并检查文件几何，而且只接受 `thetaMode` 和 `cartesian`；随后才把 `RZ` 风格或 `3D Cartesian` 风格的元数据广播给所有 rank。
  - 已补清更细的 buffer lifecycle：初始化期会立刻按这份几何分叉预读首块并建立 `E_lasy_data` 的对应 buffer 形状，后续每次滑窗重载也沿同一几何分叉继续重建；`fill_amplitude()` 则先看持久的 `file_in_cartesian_geom` 状态，再分流到 cartesian 或 cylindrical 插值链。

- [x] 2026-05-24：继续细化 `<laser_name>.delay`
  - 已补清这条值的更硬共享时间轴边界：`FromFileLaserProfile` 当前会把它缓存成 `t_delay`，随后 `update()` 与 `fill_amplitude()` 都先执行同一条 `t += t_min - t_delay` 预处理；它不是只影响最终插值时刻，而是先把仿真时间整体投影到外部文件时间轴。
  - 已补清更细的双重 consumer：平移后的时间一方面决定是否越过 `last_time_index` 从而触发新的 time-chunk 重载，另一方面又决定是否落在 `[t_min, t_max]` 有效窗口内；若越界，`fill_amplitude()` 会直接把整批 `amplitude` 置零。

- [x] 2026-05-24：继续细化 `<laser_name>.time_chunk_size`
  - 已补清这条值的更硬 lifecycle 边界：`FromFileLaserProfile` 当前在 backend 分派后就会立刻按 `time_chunk_size` 预读首块，并把对应的 `first_time_index/last_time_index` 缓存进 profile 状态，不是等第一次 `update()` 才懒加载。
  - 已补清更细的滑窗触发条件：后续 `update()` 只有在共享 `t += t_min - t_delay` 平移后算出的 `idx_t_right` 越过 `last_time_index` 时，才会以 `idx_t_left` 为新左端重读下一块并刷新缓存索引；若时间仍落在已有窗口内，`update()` 不会重读，`fill_amplitude()` 也只会复用当前块继续插值。

- [x] 2026-05-24：继续细化 `<laser_name>.field_function(X,Y,t)`
  - 已补清这条 parser profile 的更硬 runtime 边界：`FieldFunctionLaserProfile` 当前在头文件里把 `update(t)` 直接内联成 no-op，不存在跨步内部状态推进；构造期只缓存 `amrex::Parser`，真正 `compile<3>()` 要等每次 `fill_amplitude()` 调用时才发生。
  - 已补清更细的反向边界：这条 profile 的 `init(...)` 当前显式忽略 `CommonLaserParameters`，本地实现里不会继续消费 `wavelength/e_max/p_X/nvec` 这些公共参数，而是只按激光平面坐标 `(Xp,Yp,t)` 逐粒子求值。

- [x] 2026-05-24：继续细化 `<laser_name>.wavelength`
  - 已补清这条值的更硬 lifecycle 边界：当前虽然会统一通过 `CommonLaserParameters::wavelength` 传给 profile，但这一步只发生在构造期 `ILaserProfile::init(...)`，step-loop 不会再按 laser 名重读 `wavelength`。
  - 已补清更细的 profile consumer 不对称：本地实现里真正继续在 runtime 直接消费这条值的只有 `GaussianLaserProfile::fill_amplitude()`，它会用 `k0 = 2π / wavelength` 进入 diffraction、Gouy phase 和 STC/chirp 链；相对地 `parse_field_function` 与 `from_file` 当前都不会在本地 amplitude 生成链里再读这条 wavelength。

- [x] 2026-05-24：继续细化 `<laser_name>.profile`
  - 已补清这条键的更硬 lifecycle 边界：`LaserParticleContainer` 当前只会在构造期按 `laser_profiles_dictionary` 做一次性工厂分派并执行 `ILaserProfile::init(...)`；step-loop 里不会再按字符串重建 profile 对象。
  - 已补清更细的 runtime 不对称：后续统一的 `update(t_lab) + fill_amplitude(...)` 调度在三类 profile 上语义不同，`gaussian` 直接在线计算解析包络，`parse_field_function` 每次只对缓存 parser 做 `(X,Y,t)` 求值，只有 `from_file` 会先在 `update()` 里按当前时间窗口决定是否重读新的 time chunk，再在 `fill_amplitude()` 里做插值或越界置零。

- [x] 2026-05-24：继续细化 `<laser_name>.polarization`
  - 已补清这条偏振输入的更硬几何分支边界：构造期虽然总会先生成 `m_p_X/m_p_Y`，但 `InitData()`、`calculate_laser_plane_coordinates()` 和 `ComputeSpacing()` 真正使用的平面基底在 `XZ` 与 `1D_Z` 下会被几何特化成别的 `m_u_X/m_u_Y`，并不总是直接等于 `(m_p_X, m_p_Y)`。
  - 已补清更细的 profile companion 边界：`update_laser_particle()` 仍始终直接用 `m_p_X` 做电场/动量方向，而 Gaussian profile 的 `stc_direction` 默认值当前也继承的是 `CommonLaserParameters::p_X = m_p_X`，不是这些可能被改写过的 `m_u_X`。

- [x] 2026-05-24：继续细化 `<laser_name>.position`
  - 已补清这条位置输入的更硬 boost/runtime 时序：当前源码会先结合归一化后的 `m_nvec` 计算 `m_Z0_lab/Z0_boost` 并把 `m_position` 改写成 boosted-frame 天线位置；若开启 `do_continuous_injection`，随后还会把这份值拷进 `m_updated_position`，以后再由 `UpdateAntennaPosition(dt)` 持续平移，并在每次 `InitData(lev)` 前先回写 `m_position = m_updated_position`。
  - 已补清更细的禁用分叉：静态天线路径在 `InitData()` 之后若 `TotalNumberOfParticles()==0` 会 warning 并 `m_enabled=false`；continuous-injection 路径不会在这里被永久禁用，而是保留后续随 `m_updated_position` 再次进入 simulation box 的机会。

- [x] 2026-05-24：继续细化 `<laser_name>.direction`
  - 已补清这条法向输入的更硬 boosted/runtime 时序：当前源码会先把 `m_nvec` 归一化，再在 `gamma_boost > 1` 分支里按该单位法向改写 `m_position` 到 boosted-frame 天线位置，之后才继续做 moving-window 一致性断言和 `common_params.nvec` 绑定；因此后续 `InitData()`、profile 和 runtime push 看到的都不是原始输入向量。
  - 已补清更细的 enable/disable 分叉：只有 `!do_continuous_injection` 时，`InitData()` 之后若 `TotalNumberOfParticles()==0` 才会把 laser 立即禁用；连续注入路径会先调位、再 `InitData(maxLevel())`，不会走这条静态天线空交即禁用的链。

- [x] 2026-05-24：继续细化 `lasers.names`
  - 已补清这条列表的更硬一次性 registry 边界：`MultiParticleContainer::ReadParameters()` 当前被 `static initialized` 保护，`lasers_names` 与 `m_laser_deposit_on_main_grid` 在同一进程里只会 materialize 一次；后续单纯改 parser 表不会自动刷新已有 laser 名字表，也不会自动重排 species+laser 联合容器布局。
  - 已补清更细的构造期回绑边界：`m_laser_deposit_on_main_grid` 当前只在 `LaserParticleContainer` 构造时按 `lasers_names[i-nspecies]` 一次性回绑到后半段 `allcontainers` 索引；运行时不会再按名字重新查询这条 side-list。

- [x] 2026-05-24：继续细化 `fluids.species_names`
  - 已补清这条列表的更硬全局构造 gate：当前只有 `WarpX::ReadParameters()` 读到非空 `fluids.species_names` 时，`do_fluid_species` 才为真，后面 `myfl = std::make_unique<MultiFluidContainer>()`、level 初始化和 fluid runtime 链才会 materialize；若列表为空，cold-fluid 子系统整体不会构造。
  - 已补清更细的外层遍历/内层分叉边界：`MultiFluidContainer` 自己的 `AllocateLevelMFs / InitData / DepositCharge / DepositCurrent / Evolve` 只是沿 `allcontainers` 无条件逐 fluid 遍历，真正的 per-fluid early-exit 要到 `WarpXFluidContainer::Evolve()` 内部才发生，其中前后两次 `DepositCharge` 还额外要求 `rho_fp` 存在且未跳过沉积，而 gather / push / current deposition 又分别受 `do_not_gather`、`do_not_push`、`skip_deposition/do_not_deposit` 控制。

- [x] 2026-05-24：继续细化 `qed_virtual_photons_do_beam_size_effect`
  - 已补清这条开关的更硬几何作用域：当前 `do_beam_size_effect` 这个局部运行时布尔值只在 `WARPX_DIM_3D` 分支里 materialize 并进入半径采样/垂向位移链；`XZ/RZ/1D_Z/RCYLINDER/RSPHERE` 路径都只复制 primary 的已有位置，不会命中这段几何扰动。
  - 已补清更细的反向边界：这条分支当前只改 `pa_vp[PIdx::x/y/z]` 的位置，不会回头改动已经先写好的 `ux/uy/uz = vphoton_energy * n` 或 `w/sampling_factor`，所以它只影响 3D virtual-photon 发射点散布，不改变动量方向或权重合同。

- [x] 2026-05-24：继续细化 `do_qed_virtual_photons / qed_virtual_photon_species_name / qed_virtual_photons_min_energy / qed_virtual_photons_multiplier`
  - 已补清这组 companion 的更硬 target-species 绑定边界：`qed_virtual_photon_species_name` 当前不只绑定输出到哪个 photon container，还决定 `GenerateVirtualPhotons()` 每步会从哪一个 target species 参数表重新读取 `qed_virtual_photons_min_energy` 和 `qed_virtual_photons_multiplier`，而不是从 primary lepton species 侧缓存这些生成参数。
  - 已补清更细的运行期覆盖边界：源码在每个 tile 上都会先按第一遍计数结果 `ptile_vp.resize(total_num_vp)`，注释也明确这会覆盖掉上一步生成的 virtual photons；因此这条路径当前语义是“每步按当前 primary 重建并替换 target virtual-photon tile”，不是跨步累积持久 photon buffer。

- [x] 2026-05-24：继续细化 `<species_name>.do_temperature_deposition`
  - 已补清这条开关的更硬局部缓存与收口边界：`DepositTemperatures()` 当前每次都会先把 `T_<species>` 三方向场整场清零，再由 `AccumulateVelocitiesAndComputeTemperature()` 先 `reset()` species-local `variance_buffer_w/w2/vbar + nsamples`，随后走当前硬编码默认的 `DOUBLE_PASS` 方差沉积、boundary sum、`mass/k_B` Kelvin 换算，以及 `FillBoundary -> 可选滤波 -> 再同步 ghost cells` 的收口链。
  - 已补清 diagnostics 侧的更硬二次重建边界：`TemperatureFunctor` 当前并不会直接复用前面每步沉积得到的 `T_<species>` MultiFab，而是重新调用 `pc.GetAverageNGPTemperature(m_lev)`，新建无 guard 的 cell-centered `MultiFab` 并用 `DepositTotalNGPTemperature(...)` 再做一次 NGP 平均重建后，才 coarsen 到输出网格。

- [x] 2026-05-24：继续细化 `<species_name>.do_resampling`
  - 已补清这条开关的更硬 step-loop 边界：当前 `MultiParticleContainer::doResampling()` 只遍历 `pc->do_resampling` 为真的 species，但一旦进入 `PhysicalParticleContainer::resample()`，源码每次都会先做一次 `TotalNumberOfParticles()` 的全局同步，再把 `(timestep, global_numparts)` 送进 trigger 判定，不是“只在命中 trigger 时才有代价”。
  - 已补清 trigger 命中后的完整运行时次序：源码当前只会在命中后继续执行 `Redistribute() -> level/tile 级 m_resampler(...) -> deleteInvalidParticles()`；若 `verbose` 打开，还会再做第二次全局粒子数统计来打印宏粒子净减少量。

- [x] 2026-05-24：继续细化 `resampling_trigger_intervals / resampling_trigger_max_avg_ppc / resampling_min_ppc`
  - 已补清 `ResamplingTrigger` 的更硬 lifecycle 边界：`m_global_numcells` 与 `m_initialized` 当前只会在第一次 `triggered()` 时 materialize 一次，后续调用都复用这份 cell-count 快照，不会在每步自动重建；因此 `avg_ppc` 比较的是当前全局粒子数对首次初始化时总网格点数的平均值。
  - 已补清 `resampling_min_ppc` 的共享 gate 之后的算法分叉：两种算法都会先在 `cell_numparts < min_ppc` 时整 cell early-return，但 `LevelingThinning` 过门槛后就直接逐粒子做删除/提权，而 `VelocityCoincidenceThinning` 还要再满足同一 momentum bin 内 `particles_in_bin > 2` 且权重有效才会真正合并。

- [x] 2026-05-24：继续细化 `resampling_algorithm_target_weight / resampling_algorithm_velocity_grid_type`
  - 已补清 `target_weight` 的更细 cluster 边界：当前 `m_cluster_weight = 2 * target_weight` 只决定同一 momentum bin 内 cluster 何时因总权重超阈值而提前截断，不会绕过后面的 `particles_in_bin > 2` 有效合并门槛；若未给值，`m_cluster_weight` 保持无穷，cluster 边界只剩“bin 改变或 cell 结束”。
  - 已补清 `velocity_grid_type` 的更硬生命周期分叉：`spherical` 分支复用构造期缓存的 `delta_ur / n_theta / n_phi` 固定网格；`cartesian` 分支虽复用 `delta_u`，却会在每次 tile 调用时按当前 `ux/uy/uz` 极值即时重建局部速度包围盒和 `n1/n2` bin 计数，不是跨步稳定复用的全局网格。

- [x] 2026-05-24：继续细化 `resampling_algorithm_delta_ur / n_theta / n_phi / delta_u`
  - 已补清球坐标分支的更细 bin 编号公式：当前源码固定按 `u_theta = atan2(uy,ux)+π`、`u_phi = acos(uz/u_mag)`、`u_mag` 计算 `ii/jj/kk`，再线性化成 `ii + jj*n1 + kk*n1*n2`；因此 `delta_ur / n_theta / n_phi` 直接决定的是球坐标 velocity bin 的离散步长和线性编号公式。
  - 已补清直角坐标分支的 tile-local rebuild 语义：当前每次进入 `operator()` 都会以该 tile 的 `ux_min/uy_min/uz_min` 为局部原点，再按 `(u-u_min)/du` 现算 `ii/jj/kk` 和线性 bin 编号；因此 `delta_u` 不只控制步长，也控制以 tile 局部速度包围盒为基准的 bin 编号方式。

- [x] 2026-05-24：继续细化 `resampling_algorithm_target_ratio`
  - 已补清这条值的更硬 warning/执行边界：`target_ratio <= 1` 当前只会记录 warning，不会阻止运行；因此“可能不删除任何粒子”是源码允许的运行态，而不是输入错误。
  - 已补清更细的逐粒子语义：这条参数最终通过 `level_weight = average_weight * target_ratio` 决定每个 cell 内哪些低权重粒子会被标成 `Invalid`，哪些幸存粒子会被直接提权到 `level_weight`，不是抽象的全局粒子缩减比例。

- [x] 2026-05-24：继续细化 `<species_name>.save_particles_at_xlo/ylo/zlo/xhi/yhi/zhi/eb`
  - 已补清这组开关在 `ParticleBoundaryBuffer` 侧的更硬容器边界：真正启用后，源码会把每个 `(boundary, species)` 的 scraped 粒子写进 pinned arena buffer，并在其中附加 `stepScraped / deltaTimeScraped / timeScraped / nx / ny / nz` 这些 runtime 分量；真正写盘后才会按 boundary 调 `clearParticles(i_buffer)` 清空。
  - 已补清 diagnostics 侧的独立写盘 gate：`BoundaryScrapingDiagnostics` 未显式给 species 时会默认扩成全部 species，`DoComputeAndPack()` 恒为 `false`，`intervals` 只控制 `DoDump/Flush` 是否写盘；`Flush()` 还会先汇总该 boundary 总粒子数，若为 `0` 就静默返回，不创建空输出目录。
  - 已补清 species-local filter 的更细时序边界：`random_fraction / uniform_stride / plot_filter_function` 当前挂在 `ParticleDiag` 上，只会在 openPMD/plotfile `WriteToFile(...)` 阶段对 pinned buffer 做二次筛选，不会减少前面累计进内存的 scraped 粒子数；`plot_filter_function` 的 `t` 也取写盘时刻而不是粒子撞边界时刻，并且 parser 求值前源码会先把粒子量转换到 SI。
  - 已补清 species 选择的更细名字域边界：`BoundaryScrapingDiagnostics` 这条用户路径当前会先在 `Diagnostics` 基类里按 `GetSpeciesNames()` 做 species-only 校验；因此虽然更底层的 `GetParticleContainerFromName()/getSpeciesID()` 走的是 species+laser 联合名字域，这里当前也不会真正让 laser 名字穿透到边界 buffer 诊断。

- [x] 2026-05-24：继续收束 runtime-component companion 总闭包
  - 已把 `addIntegerAttributes / addRealAttributes / attribute.<name>(...) / save_previous_position` 再收成一条更紧的 runtime-component 总链：它们都在 species 构造期一次性扩展 particle SoA 布局，而不是普通物理参数。
  - 已补清更硬的分工边界：`add*Attributes` 和 `attribute.<name>(...)` 负责把用户自定义 real/int 分量与延迟 `compile<7>()` 的初始化表达式接进新粒子创建链；`save_previous_position` 则另外接入一组由 `PushP()` 在推进前写回的位置快照分量。

- [x] 2026-05-24：继续收束 ionization companion 总闭包
  - 已把 `do_field_ionization / do_adk_correction / physical_element / ionization_product_species / ionization_initial_level` 再收成一条更紧的初始化-运行时总链：总 gate 先打开，随后 `InitIonizationModule()` 完成 `charge -> q_e` 覆写、元素/产物/初始级数解析和 ADK 数据建表。
  - 已补清更硬的 companion 分工：`physical_element` 固定最大可电离级数上界，`ionization_initial_level` 决定起跑级数，`ionization_product_species` 只在初始化期解析并缓存成整数索引，`do_adk_correction` 则只在基础 ADK `w_dtau` 之后插入 Hydrogen-only 指数修正；运行期再统一由 `Efield_aux/Bfield_aux` 六分量驱动事件过滤与产物写入。

- [x] 2026-05-24：继续细化 `<species_name>.do_adk_correction`
  - 已补清这条修正的更硬数据边界：当前初始化期只会为 Hydrogen 路径拷入 4 个 correction factors，不会改写 `ionization_energies` 或基础 ADK 系数数组。
  - 已补清更细的运行期插入点：`IonizationFilterFunc::operator()` 只会在基础 `w_dtau` 已算出之后，再按 `r = E / factor[3]` 乘上一层指数校正；若 `E <= 0` 使基准 `w_dtau` 已为零，这条修正也不会单独重新激活事件概率。

- [x] 2026-05-24：继续细化 `<species_name>.physical_element`
  - 已补清这条值的更硬运行期上界语义：它不只是在初始化期决定查哪张电离能表，还会固定 `ion_atomic_number` 以及 `ionization_energies / adk_prefactor / adk_exp_prefactor / adk_power` 这些数组长度。
  - 因而在 `IonizationFilterFunc::operator()` 里，这条元素选择还会通过 `ion_lev < atomic_number` 直接限定该 species 还保留多少可继续电离的 charge-state 空间。

- [x] 2026-05-24：继续细化 `<species_name>.ionization_product_species`
  - 已补清这条名字的更硬初始化边界：`mapSpeciesProduct()` 当前只在初始化期通过 `getSpeciesID(...)` 解析一次，随后缓存成整数 `ionization_product`。
  - 已补清更细的解析域与运行时边界：当前名字解析搜索的是 `GetSpeciesAndLasersNames()` 联合名字表；而进入 `doFieldIonization()` 之后，源码已不再回头看字符串，只直接复用缓存索引绑定目标 container。

- [x] 2026-05-24：继续细化 `<species_name>.ionization_initial_level`
  - 已补清这条输入的更硬运行期边界：`IonizationFilterFunc::operator()` 只有在 `ion_lev < atomic_number` 时才会继续进入电场 gather 与 ADK 概率计算。
  - 因而 `ionization_initial_level` 不只是 `ionizationLevel` 的初值来源；若起始级别已经达到或超过该元素原子序数，当前实现会整条旁路后续 ADK 事件链。

- [x] 2026-05-24：继续收束 `<species_name>.do_field_ionization` 的族内总闭包
  - 已把这条键再压成更明确的 ionization 总入口：当前一旦打开，源码会先在 `InitIonizationModule()` 把 ionizable species 的 `charge` 覆写成 `q_e`，再强制读取 `do_adk_correction / ionization_initial_level / ionization_product_species / physical_element`，并据此建好 `ionizationLevel`、ADK 系数表和 product-species 绑定。
  - 已补清更硬的 runtime 调度边界：step-loop 里 `WarpX::doFieldIonization()` 固定从 `Efield_aux/Bfield_aux` 六分量驱动 `MultiParticleContainer::doFieldIonization()`，再只对 `do_field_ionization` 为真的 source species 执行事件过滤与 product-container 写入。

- [x] 2026-05-24：继续收口 `<species_name>.save_previous_position`
  - 已把这条旧位置缓存开关补成正式总表条目：当前它会在 species 构造期按维度条件分配 `prev_x/prev_y/prev_z` runtime components，而不是普通注释性布尔位。
  - 已补清更硬的运行时边界：`PhysicalParticleContainer::PushP()` 会在真正推进前先把当前位置写进 `prev_*`，因此缓存的是“本次 push 进入前”的位置快照；同时 `RZ/RCYLINDER/RSPHERE` 构建下当前会直接 abort，本地源码里暂未看到 `prev_*` 的进一步 consumer。

- [x] 2026-05-24：继续收口 `<species_name>.attribute.<name>(x,y,z,ux,uy,uz,t)`
  - 已把这条 user-defined runtime particle attribute 接口补成 grouped 正式条目：当前它不是独立名字空间，而是只对已列在 `addIntegerAttributes / addRealAttributes` 里的 `<name>` 才会 materialize。
  - 已补清更硬的生命周期与类型边界：源码会在 species 构造期先 `makeParser(...)` 缓存 parser，但真正 `compile<7>()` 要等 `DefaultInitialization.H` 的新粒子初始化链；real 路径直接写回实数分量，int 路径则会在写入前显式 `static_cast<int>(...)`。

- [x] 2026-05-24：继续收束 `<species_name>.momentum_distribution_type` 的总分派闭包
  - 已把这条键再压成更明确的动量初始化总入口：当前不仅能区分 `gaussian / gaussianflux / parse_momentum_function / gaussian_parse_momentum_function / maxwell_boltzmann / maxwell_juttner` 等分支，还能明确看出哪些路径给出“mean drift + thermal spread”双链，哪些路径只给出确定性三分量动量场。
  - 已补清更硬的实现边界：`gaussian / gaussian_parse_momentum_function` 的 `u_bulk` 只来自 `*_m` 均值链，`parse_momentum_function` 让 `getMomentum()` 与 `getBulkMomentum()` 同值，而 `maxwell_boltzmann / maxwell_juttner` 则先退化成 `theta` 标量场和带方向符号的 `beta` 标量场，再延后到各自分支中完成热采样与单轴落位。

- [x] 2026-05-24：继续收束 Maxwell-Boltzmann / Juttner 温度-速度 companion 总闭包
  - 已把 `theta_distribution_type / theta / theta_function(x,y,z)` 和 `bulk_vel_dir / beta_distribution_type / beta / beta_function(x,y,z)` 再收一层回总入口：当前可把这簇统一理解成两条 scalar-field 生成链，而不是若干零散 companion。
  - 已补清更硬的总语义：温度侧最终只产出局域/全域标量 `theta`，速度侧最终只产出带方向符号的局域/全域标量 `beta`；真正的热采样、`vave=sqrt(theta)`、`gamma*beta` 和单轴落位，都延后到后续 Juttner/Boltzmann 分支中发生。

- [x] 2026-05-24：继续收口 `<species_name>.theta` / `<species_name>.beta`
  - 已把这两条 constant companion 补成正式总表条目：源码当前会在构造期就把 `theta` 和 `bbta` 分别接到各自的常数路径，并立即执行分布类型相关的合法性检查，不再只是埋在 `theta_distribution_type / beta_distribution_type` 总述里。
  - 已补清更硬的 runtime 语义：`GetTemperature` 和 `GetVelocity` 之后都只把它们缓存成全域常数标量，真正的物理消费仍要等后续 Boltzmann/Juttner 分支分别接到 `vave=sqrt(theta)`、`gamma*beta` 和单轴落位链上。

- [x] 2026-05-24：继续收口 `<species_name>.theta_function(x,y,z)`
  - 已把这条 parser 版温度函数补成正式总表条目：源码当前会在 `TemperatureProperties` 里先 `Store_parserString(...)` 并构造 `Parser`，真正 `compile<3>()` 要到 `GetTemperature::GetTemperature(...)` 命中 `TempParserFunction` 时才发生。
  - 已补清更硬的 runtime 语义：`GetTemperature::operator()(x,y,z)` 只返回局域标量 `theta`，不会在这里再做别的变换；后续 `InjectorMomentumBoltzmann/Juttner::getMomentum()` 才把它分别接到 `vave=sqrt(theta)` 或低温 abort/后续速度采样链上。

- [x] 2026-05-24：继续收口 `<species_name>.beta_function(x,y,z)`
  - 已把这条 parser 版漂移速度函数补成正式总表条目：源码当前会在 `VelocityProperties` 里先 `Store_parserString(...)` 并构造 `Parser`，真正 `compile<3>()` 要到 `GetVelocity::GetVelocity(...)` 命中 `VelParserFunction` 时才发生。
  - 已补清更硬的 runtime 语义：`GetVelocity::operator()(x,y,z)` 返回的不是 parser 原值，而是先统一乘上从 `bulk_vel_dir` 拆出的 `m_sign_dir`；随后 Juttner/Boltzmann 的 `getMomentum()` 与 `getBulkMomentum()` 还会继续结合 `direction()` 把这条带符号标量 `beta` 落到单一坐标轴。

- [x] 2026-05-24：继续收口 `<species_name>.bulk_vel_dir`
  - 已把这条 bulk velocity 方向 companion 补成正式总表条目：源码当前会在 `VelocityProperties` 构造期先把 `(+/-)x/y/z` 拆成 `m_sign_dir` 和 `m_dir` 两份运行态状态；空字符串或非法尾字符会立即 abort，因此它不是普通注释性方向标签。
  - 已补清更硬的 consumer 分叉：`GetVelocity` 运行期只返回带符号标量 `beta`，真正把 bulk drift 落到哪一轴要等 `InjectorMomentumBoltzmann/Juttner::getMomentum()` 和 `getBulkMomentum()` 再结合 `direction()` 完成，因此它直接决定热平衡注入链里哪个分量承载漂移、哪些分量保留零或纯热噪声。

- [x] 2026-05-24：继续收口 `<species_name>.momentum_function_ux/uy/uz(x,y,z)`
  - 已把普通 `parse_momentum_function` 三分量 parser 动量函数补成 grouped 正式条目：源码当前会在 `SpeciesUtils::parseMomentum()` 里先 `Store_parserString(...)`，再立刻 `makeParser(...)->compile<3>()` 并装进 `InjectorMomentumParser`，不是后续再延迟编译。
  - 已补清更硬的 runtime 语义：`InjectorMomentumParser::getMomentum()` 与 `getBulkMomentum()` 当前完全同值，都直接返回同一份位置相关确定性动量场；因此这条 parser 路径不像相邻 `gaussian_parse_momentum_function` 那样再分出随机展宽 companion。

- [x] 2026-05-24：继续收口 `<species_name>.momentum_function_ux_m/.../uz_m` / `<species_name>.momentum_function_ux_th/.../uz_th`
  - 已把这组 `gaussian_parse_momentum_function` companion 补成 grouped 正式条目：源码当前会在 `SpeciesUtils::parseMomentum()` 里先 `Store_parserString(...)`，再立刻 `makeParser(...)->compile<3>()` 并装进 `InjectorMomentumGaussianParser`，不是后续再延迟编译。
  - 已补清更硬的 runtime 分叉：`momentum_function_*_m` parser 会同时进入 `getMomentum(...)` 和 `getBulkMomentum(...)`，因此 ballistic correction 与 `focal_distance` 聚焦看到的是位置相关的 mean drift；相对地 `momentum_function_*_th` parser 只控制位置相关的随机展宽，不会进入 `u_bulk`。

- [x] 2026-05-24：继续收口 `<species_name>.ux_m/uy_m/uz_m` / `<species_name>.ux_th/uy_th/uz_th`
  - 已把这两组高斯动量 companion 补成 grouped 正式条目：源码当前会在 `SpeciesUtils::parseMomentum()` 的 `gaussian / gaussianflux` 分支中读取它们，并分别传进 `InjectorMomentumGaussian` 或 `InjectorMomentumGaussianFlux`，因此它们不是所有 momentum distribution 共享的统一参数，而是高斯动量家族的局部输入。
  - 已补清更硬的不对称 consumer：`ux_m/uy_m/uz_m` 同时进入逐粒子 `getMomentum(...)` 和 `getBulkMomentum(...)`，因此 ballistic correction 与 `focal_distance` focusing 看到的是 mean drift；相对地 `ux_th/uy_th/uz_th` 只控制随机展宽，不会进入 `u_bulk`，`gaussianflux` 的法向 `v*Gaussian` 采样链也不会反向改写这条 bulk-drift 路径。

- [x] 2026-05-24：继续收口 `<species_name>.x_m/y_m/z_m` / `<species_name>.x_rms/y_rms/z_rms` / `<species_name>.x_cut/y_cut/z_cut`
  - 已把这三组高斯束主参数补成 grouped 正式条目：源码当前前半段真实顺序是先以 `x_m/y_m/z_m` 为中心、`x_rms/y_rms/z_rms` 为宽度做 `RandomNormal(...)` 高斯采样，再用 `x_cut/y_cut/z_cut` 做 hard cutoff，然后才进入 `focal_distance`、rotation、symmetrization 和 boosted 插入链。
  - 已补清更硬的运行时语义：`x_rms/y_rms/z_rms` 当前不只控制采样宽度，还会在降维几何下进入 `weight_3d` 的归一分母；相对地 `x_cut/y_cut/z_cut` 只做采样后的 hard rejection，不会回头改写采样分布或重新标定 `q_tot` 对应的未裁剪束荷。

- [x] 2026-05-24：继续收口 `<species_name>.gaussian_beam_rotation_axis / gaussian_beam_rotation_angle`
  - 已把这组高斯束旋转 axis/angle companion 补成 grouped 正式条目：源码当前只有在 `do_gaussian_beam_rotation=1` 时才会强制读取它们，因此它们不是独立常驻几何元数据，而是位置旋转 gate 打开的 parser 载荷。
  - 已补清更硬的运行时边界：`AddGaussianBeam()` 不会在构造期先归一化旋转轴，而是对每个命中粒子先重新计算 `k_norm`，再把同一组 Rodrigues 轴角对复用到位置和可选动量两条旋转链；同时在不支持旋转的几何下，这组 companion 也会和 rotation 开关一起被构造期硬拦截。

- [x] 2026-05-24：继续收口 `<species_name>.focal_distance`
  - 已把这条高斯束焦平面距离参数补成正式总表条目：源码当前不是简单读取一个几何标量，而是先用 `contains("focal_distance")` 判 presence；只有命中时才会把 `do_focusing` 打开并 materialize 这条值。
  - 已补清更硬的运行时次序：`AddGaussianBeam()` 会先完成高斯采样和裁剪，再按局部 `bulk momentum` 定义焦平面，并只沿正交于 bulk direction 的方向位移粒子；这次 focusing 位移发生在 rotation、symmetrization 和后续 boosted 插入之前。

- [x] 2026-05-24：继续收口 `<species_name>.do_gaussian_beam_rotation_momenta`
  - 已把这条高斯束动量旋转 companion 补成正式总表条目：源码当前不是给动量单独开一条旋转链，而是只在 `setupGaussianBeam()` 中单独记录开关；真正可用的旋转轴和角度仍只会在位置旋转打开时 materialize。
  - 已补清更硬的运行时和几何边界：`AddGaussianBeam()` 当前只会在位置 Rodrigues 旋转之后，再复用同一组归一化轴和同一个 `rotation_angle` 去改写局部动量 `u`；同时在 `RZ / 1D_Z / RCYLINDER / RSPHERE` 构建下，它也会和位置旋转一起被构造期硬断言拦下。

- [x] 2026-05-24：继续收口 `<species_name>.do_gaussian_beam_rotation`
  - 已把这条高斯束位置旋转开关补成正式总表条目：源码当前不只是把它当作“是否旋转 beam 位置”的字面布尔量，而是高斯束路径里一条更硬的构造期总 gate；只有命中为真时，`setupGaussianBeam()` 才会继续强制读取 `gaussian_beam_rotation_axis` 和 `gaussian_beam_rotation_angle`。
  - 已补清更硬的运行时边界：`AddGaussianBeam()` 会先按 `focal_distance` 可选执行 focusing 位移，再仅在 `3D/XZ` 编译分支里围绕 beam centroid 做 Rodrigues 位置旋转；因此 `do_gaussian_beam_rotation_momenta` 也不能绕开这条前置位置旋转 gate 单独生效。

- [x] 2026-05-24：继续收口 `<species_name>.do_symmetrize`
  - 已把这条高斯束对称化开关补成正式总表条目：源码当前不只是把它当作“是否额外复制粒子”的布尔量，而是会先用它决定是否缩减基准采样数，再进入 4/8 重镜像模板分派。
  - 已补清更硬的运行时边界：`AddGaussianBeam()` 里一旦 `do_symmetrize=1`，源码会先执行 `npart /= symmetrization_order` 并按缩减后的 `npart` 计算 `weight_3d`，随后才在 `symmetrization_order == 4/8` 分支里生成镜像副本；相对地 `do_symmetrize=0` 时则完全旁路这两层逻辑。

- [x] 2026-05-24：继续收口 `<species_name>.npart`
  - 已把这条高斯束宏粒子个数参数补成正式总表条目：源码当前只在 `gaussian_beam` 路径里有真实 consumer，并且它首先代表的是对称展开前的基准宏粒子数，不是运行期最终一定会插入的粒子数。
  - 已补清更硬的 `do_symmetrize / symmetrization_order` 分叉：`AddGaussianBeam()` 会先在 `do_symmetrize=1` 时执行 `npart /= symmetrization_order`，只生成更少的基准粒子，再靠 4/8 重镜像复制补回总数；与此同时 `weight_3d` 也用这份缩减后的 `npart` 计算，因此单个基准粒子的权重会相应放大。

- [x] 2026-05-24：继续收口 `<species_name>.npart_real`
  - 已把这条真实粒子总数参数补成正式总表条目：源码当前只在 `gaussian_beam` 路径里有真实 consumer，而且不是 `q_tot` 的可叠加 companion，而是互斥替代项；`setupGaussianBeam()` 会硬要求 `q_tot` 与 `npart_real` 二者恰好指定其一。
  - 已补清更硬的运行时边界：一旦命中 `npart_real`，`AddGaussianBeam()` 当前会直接走 `weight_3d = N_tot / npart` 这条宏粒子权重归一化链，并完全旁路 `q_tot / charge`；相对地 `external_file`、`singleparticle`、`multipleparticles` 和 `AddPlasma()` 路径都不会读取它。

- [x] 2026-05-24：继续收口 `<species_name>.q_tot`
  - 已把这条总电荷参数补成正式总表条目：源码当前不是单一 consumer，而是按注入风格分叉。在 `gaussian_beam` 路径里，它会和 `npart_real` 做互斥断言，并真正进入 `weight_3d = q_tot / (npart * charge)` 这条宏粒子权重归一化链。
  - 已补清更硬的 `external_file` 反向边界：`setupExternalFile()` 虽然也会可选读取并缓存 `q_tot`，`AddPlasmaFromFile()` 也会把它传进来，但运行期只要 `q_tot != 0` 就会记录一次 high-priority warning，然后继续直接使用 openPMD 文件自带的 `weighting`，不会做任何重标定。

- [x] 2026-05-24：继续收口 `<species_name>.z_shift`
  - 已把这条 `external_file` 相邻输入补成正式总表条目：源码当前会在 `setupExternalFile()` 中通过 parser 可选读取并缓存，因此它和 `injection_file` 一样属于构造期 external-file 配置，而不是等到 `AddPlasmaFromFile()` 运行时再回头 query。
  - 已补清更硬的时序边界：`AddPlasmaFromFile()` 只在重建纵向坐标时执行 `z = position_z + position_offset_z + z_shift`，不会改 `x/y`、`ux/uy/uz`、`weight` 或 `t_lab`；而且这次平移发生在 `insideBounds(x,y,z)` 之前，所以它当前会直接改写 external-file 粒子的保留判定，不只是对已保留粒子做最终偏移。

- [x] 2026-05-24：继续收口 `<species_name>.impose_t_lab_from_file`
  - 已把这条 `external_file` companion 补成正式总表条目：源码当前不是在 `setupExternalFile()` 构造期读取它，而是等到 `AddPlasmaFromFile()` 真正消费 openPMD `Series` 时，才通过 species `ParmParse` 读取并 materialize。
  - 已补清更硬的运行时边界：它不影响 `z_shift`、`insideBounds` 或 openPMD 粒子数据本身，当前唯一改变的是传给 `CheckAndAddParticle(...)` 的 `t_lab`，也就是 boosted-frame Lorentz 变换参考时刻；因此它服务的是 external-file 一次性初始化注入的变换 gate，不会沿 continuous injection 重复消费。

- [x] 2026-05-24：继续收口 `<species_name>.injection_file`
  - 已把这条 `external_file` 相邻输入补成正式总表条目：源码当前在 `setupExternalFile()` 中会由 IO rank 立即按路径打开 openPMD `Series`，并强制要求文件里只有 `1` 个 iteration 和 `1` 个 particle species；构造期保留下来的不是原始路径，而是缓存到 `m_openpmd_input_series` 里的已打开 series。
  - 已补清更硬的初始化消费边界：`AddPlasmaFromFile()` 会通过 `std::move(plasma_injector.m_openpmd_input_series)` 一次性取走这份 series，再经过 `insideBounds`、可选 `impose_t_lab_from_file`、`z_shift` 和 `CheckAndAddParticle()` 的过滤/boosted 映射链，最后统一 `AddNParticles(0, ...)`；因此它当前服务的是 external-file 的一次性初始化注入，不会沿 `ContinuousInjection()` 或 `ContinuousFluxInjection()` 重复消费。

- [x] 2026-05-24：继续收口 `<species_name>.single_particle_weight`
  - 已把这条 `singleparticle` 局部权重参数补成正式总表条目：源码当前只在 `setupSingleParticle()` 中强制读取并缓存，不参与 `single_particle_u` 那条 `*c` 单位换算，也不会被 `MapParticletoBoostedFrame(...)` 改写。
  - 已补清真实 consumer：`AddParticles()` 里它只会被包装成单个 real attribute 载荷送进一次 `AddNParticles(...)`；与此同时 `WarpXInitData.cpp::get_nppc()` 在 `singleparticle` 分支固定返回 `1`，因此它只决定唯一宏粒子的代表权重，不决定宏粒子个数。

- [x] 2026-05-24：继续收口 `<species_name>.multiple_particles_pos_x/y/z` / `<species_name>.multiple_particles_ux/uy/uz/weight`
  - 已把这组 `multipleparticles` 局部参数补成 grouped 正式总表条目：源码当前会在 `PlasmaInjector::setupMultipleParticles()` 中先统一检查位置、动量和权重列表长度必须全部一致，缺一不可，不是几组彼此独立的自由列表。
  - 已补清更硬的构造期和运行期边界：`multiple_particles_ux/uy/uz` 读入后就逐分量乘 `PhysConst::c`，而 `AddParticles()` 在 `gamma_boost > 1` 时会逐粒子原地调用 `MapParticletoBoostedFrame(...)` 改写整组位置/动量，再一次性交给 `AddNParticles(...)`；但这条 `multipleparticles` 路径不会像 `singleparticle` 那样提前 `return`，因此同一 species 后续 injector 仍可继续运行。

- [x] 2026-05-24：继续收口 `<species_name>.single_particle_pos` / `<species_name>.single_particle_u`
  - 已把这两条 `singleparticle` 局部参数补成正式总表条目：`single_particle_pos` 当前在 `AddParticles()` 里会在 `gamma_boost > 1` 时被 `MapParticletoBoostedFrame(...)` 原地改写，然后立刻打包成单元素 `xp/yp/zp` 向量交给一次 `AddNParticles(...)`，并直接 `return` 截断后续 injector。
  - 已补清更硬的单位换算边界：`single_particle_u` 在 `PlasmaInjector::setupSingleParticle()` 里读入后就逐分量乘 `PhysConst::c`，因此运行期看到的已经不是输入文档里的无量纲 `gamma beta`，而是完成单位换算且可能再经 boosted-frame 改写的三分量。

- [x] 2026-05-24：继续收口 `<species_name>.boost_adjust_transverse_positions`
  - 已把这条 boosted-frame 横向回推开关补成正式总表条目：它当前与 `do_backward_propagation` 共用 `MapParticletoBoostedFrame(...)`，但只控制位置同步阶段里的 `x/y` 回推，不影响前面的 Lorentz 变换，也不影响始终无条件执行的 `z` 回推。
  - 已补清 consumer 范围：和相邻的 `do_backward_propagation` 一样，`CheckAndAddParticle()` 在 `gamma_boost > 1` 时也会复用这条链，所以它不只命中 `single_particle/multiple_particles`，还会继续覆盖 `AddGaussianBeam()` 和 `AddPlasmaFromFile()`。

- [x] 2026-05-24：继续收口 `<species_name>.random_theta`
  - 已补清这条 RZ/圆柱/球几何开关的更硬角度采样边界：`AddPlasma()` 里它当前只在确定性的 `theta_base = π(1-2r.y)` 上叠加一次 cell-local `theta_offset`，不会改底层均匀角采样公式。
  - 已补清 consumer 反向边界：虽然不改底层 `theta_base`，但后续 `insideBounds(...)`、`inj_mom->getMomentum(...)` 和 `inj_rho->getDensity(...)` 看到的已经是这次整体旋转后的 `pos.x/pos.y(/pos.z)`，所以它控制的是整 cell 粒子云共同转角，而不是独立粒子级重采样。

- [x] 2026-05-24：继续收口 `<species_name>.do_backward_propagation`
  - 已补清这条 boosted-frame backward-propagation 键的更硬 consumer 范围：它当前不只命中 `single_particle` 和 `multiple_particles` 的显式 `MapParticletoBoostedFrame(...)` 调用。
  - 已补清 `CheckAndAddParticle()` companion：`gamma_boost > 1` 时该 helper 也会无条件转进同一个 `MapParticletoBoostedFrame(...)`，而它又被 `AddGaussianBeam()` 和 `AddPlasmaFromFile()` 复用；因此这条参数实际覆盖单粒子、多粒子、高斯束和 external-file 导入这几类 boosted-frame 初始化注入路径。

- [x] 2026-05-24：继续收口 `<species_name>.split_type`
  - 已补清这条 split 模板分派键的更硬 offset companion：`SplitParticles()` 里 `split_type` 不只决定 `2^D` vs `2D` 的子粒子模板，还会继续落到 `split_offset` 的构造。
  - 已补清 `num_particles_per_cell_each_dim` 的反向边界：只有 `ppc_nd[0] > 0` 时，源码才会继续按 `ppc_nd[0/1/2]` 缩放 `split_offset` 以保持 split 前后的均匀采样；否则当前直接退回半个 cell 的粗偏移模板，不会按每维 `nppc` 修正。

- [x] 2026-05-24：继续收口 `<species_name>.do_splitting`
  - 已补清这条 AMR splitting 总 gate 的更硬 resplit 边界：`particlePostLocate()` 当前只会把从 `lev` 上行到 `lev+1` 的原粒子标成 `DoSplitParticleID`，而 `SplitParticles()` 真正 materialize 出来的新子粒子不会继续保留可 split 身份。
  - 已补清 redistribute companion：源码在 `pctmp_split.AddNParticles(...)` 时会直接把新子粒子赋成 `LongParticleIds::NoSplitParticleID`，并先做一次 `Redistribute()` 再并回原容器；因此它们不会在同一上行链里被再次打回 `DoSplitParticleID`，也避免 split 后仍留在错误 grid/tile 上引发双重沉积。

- [x] 2026-05-24：继续收口 `<species_name>.do_not_deposit`
  - 已补清这条沉积总 gate 的更硬时序分叉：`PhysicalParticleContainer::Evolve()` 里 `do_not_deposit=1` 会同时关掉前置 `rho`、后续 `J` 和电磁模式下的后置 `rho` 三段，不再只是一句泛化的“关闭沉积”。
  - 已补清 companion 反向边界：即便 `do_not_deposit=0`，`deposit_current` 仍会继续受 `skip_deposition` 和 implicit `evolve_suborbit_particles_only` 约束，而后置 `rho` 也仍单独受 `electrostatic_solver_id == None` gate 控制；因此这条输入当前关掉的是三段不同时间语义的写网格事件，不是单次统一沉积调用。

- [x] 2026-05-24：继续收口 `<species_name>.do_not_gather`
  - 已补清这条总 gate 的更硬外场旁路：`do_not_gather=1` 当前只会跳过显式/隐式/photon 路径里的网格 `E/B` gather，不会关闭 `E_external_particle/B_external_particle` 初始化，也不会关闭 `GetExternalEBField(...)` 的额外外场叠加。
  - 已补清 implicit/photon companion 边界：`ImplicitPushPX.cpp` 后面的外场 `getExternalEB(...)` 与 QED momentum/optical-depth 更新仍会继续运行，`PhotonParticleContainer::PushPX()` 里的 Breit-Wheeler optical-depth evolve 也仍会消费此时的纯外场 `E/B`，因此这条开关把推进链退化成“纯外场 + 非网格 QED”版本，而不是完全空跑。

- [x] 2026-05-24：继续收口 `<species_name>.do_not_push`
  - 已补清这条总 gate 的更硬运行时分叉：`do_not_push=1` 会整体旁路 `PhysicalParticleContainer::Evolve()` 里的 `PartitionParticlesInBuffers(...)`、`PushPX/ImplicitPushXP`、`DepositCurrent(...)` 和 implicit suborbit fallback，因此 AMR fine/buffer gather 分区与 `J` 沉积也会一起停掉。
  - 已补清时序反向边界：前置 `rho` 沉积和电磁模式下的后置 `rho` 沉积都仍在这条 gate 外侧继续执行，所以当前语义更接近“冻结位置/速度、但仍允许 charge snapshot 写回”，不是整次 `Evolve()` 完全空跑。

- [x] 2026-05-24：继续收口 `<species_name>.rigid_advance`
  - 已补清这条 rigid 推进模式的更硬 fresh-run 分叉：只有 `vzbar` 会在 `InitData() -> RemapParticles()` 中重新计算 `vzbeam_ave_boosted = meanParticleVelocity(false)[2]`，再把初始粒子位置从“各自 `vz` 推进”重映射到“平均束流速度推进”的参考系；`vz`/`v` 模式当前根本不会进入这条 remap 链。
  - 已补清 restart companion 边界：checkpoint header 不会保存 `rigid_advance_mode` 本身，只续写 `vzbeam_ave_boosted` 和 `zinject_plane_levels`；因此 restart 后模式仍继续来自当前输入文件，而 `vzbar` 后续未注入粒子回退链所用的平均束流速度则直接复用 header 恢复值，不会再次重跑 `RemapParticles()` 或 `meanParticleVelocity(false)`。

- [x] 2026-05-24：继续收口 `<species_name>.zinject_plane`
  - 已补清这条 rigid 注入平面的更硬 restart/runtime 分工：`RigidInjectedParticleContainer` 构造函数仍会从当前输入文件强制读取原始 `zinject_plane`，`InitData()` 再把它按当前 `gett_new(0)` 变换到 boosted frame 并初始化 `zinject_plane_levels`。
  - 已补清 checkpoint companion 边界：`ParticleIO.cpp` 当前不会保存原始 `zinject_plane`，只续写运行态的 `zinject_plane_levels` 和 `vzbeam_ave_boosted`；因此 restart 后静态平面配置仍来自当前输入文件，而 `done_injecting_lev` 继续留到首个 `Evolve()` 再按恢复后的 level-plane 和当前域边界重算。

- [x] 2026-05-24：继续收口 `<species_name>.beta_distribution_type`
  - 已补清这条漂移速度 companion 的更硬方向 gate：`VelocityProperties` 会在构造期先把 `bulk_vel_dir` 拆成方向 `m_dir` 和符号 `m_sign_dir`；`constant` 分支立即检查 `|beta|<1`，而 `parser` 分支当前只保存 `beta_function(x,y,z)` 并构造 `Parser`，不会在这里复用这条模长检查。
  - 已补清 compile/runtime 分叉：真正把 parser 编译成 `ParserExecutor<3>` 的位置在 `GetVelocity` 构造时；运行期 `velocity(x,y,z)` 只返回带符号的标量 `beta`，真正把它放到单一坐标轴上要等 Juttner/Boltzmann 的 `getMomentum/getBulkMomentum` 再结合 `direction()` 完成。

- [x] 2026-05-24：继续收口 `<species_name>.theta_distribution_type`
  - 已补清这条温度分布 companion 的更硬 parser 生命周期边界：`constant` 分支会在 `TemperatureProperties` 构造期立即做 `theta >= 0`、Juttner 下 `theta >= 0.1`、Boltzmann 高温 warning，而 `parser` 分支当前只保存 `theta_function(x,y,z)` 并构造 `Parser`，不会在这里复用这些数值阈值检查。
  - 已补清 compile/runtime 分叉：真正把 parser 编译成 `ParserExecutor<3>` 的位置在 `GetTemperature` 构造时；`PlasmaInjector::h_mom_temp` 还会专门保持其生命周期，后续 Boltzmann/Juttner 逐粒子采样只剩 `temperature(x,y,z)` functor 调用。

- [x] 2026-05-24：继续收口 `<species_name>.momentum_distribution_type`
  - 已补清这条动量分布总分派键的更硬 `gaussianflux` 边界：`SpeciesUtils::parseMomentum()` 当前会强制要求 `gaussianflux` 只能配合 `injection_style = NFluxPerCell`，不会出现在普通体注入路径上。
  - 已补清它和 ballistic-correction/focusing 的 companion 分叉：`InjectorMomentumGaussianFlux::getBulkMomentum()` 只返回均值漂移 `(ux_m,uy_m,uz_m)`，不会复现 `getMomentum()` 那条按 `flux_normal_axis` 生成 `v*Gaussian` 法向分布、再按 `flux_direction` 定符号的采样链，因此位置修正看到的只是 mean drift，不是 flux-weighted 随机法向速度。

- [x] 2026-05-24：继续收口 `<species_name>.radial_numpercell_power`
  - 已补清这条径向幂律参数的更硬实现边界：体注入 `AddParticles()` 和 flux 注入 `AddPlasmaFlux()` 虽然都使用同一套 `r^(1+p)` 反变换数学形式，但源码里其实各自独立写了一套半径采样与权重修正链，不是共享同一个 helper。
  - 已补清 flux companion gate：径向权重修正只在 emission surface 的法向让表面积依赖半径时才生效，例如 `RZ/RCYLINDER` 下要求 `flux_normal_axis != 1`，`RSPHERE` 下要求 `flux_normal_axis == 0`。

- [x] 2026-05-24：继续收口 `<species_name>.density_max`
  - 已补清这条最大密度阈值的更硬时序边界：`AddParticles.cpp` 前面的 cell-level `pcount` 预筛选当前仍只检查 `inj_rho->getDensity(...) > 0`，不会提前消费 `density_max`，因此它不会减少候选粒子枚举数。
  - 已补清 boosted-frame companion 边界：lab-frame 和 boosted-frame 分支都会在 per-particle kernel 里先执行 `dens = min(dens, density_max)`，但 boosted 分支会在这之后再做 Lorentz 变换，所以它当前裁剪的是注入前的 lab-frame density，而不是最终 boosted-frame 权重链里的有效密度。

- [x] 2026-05-24：继续收口 `<species_name>.density_min`
  - 已补清这条最小密度阈值的更硬时序边界：`AddParticles.cpp` 前面的 cell-level `pcount` 预筛选当前只检查 `inj_rho->getDensity(...) > 0`，并不会提前消费 `density_min`；因此低于阈值但仍为正的局部密度，源码会先保留候选粒子槽位。
  - 已补清后半段真正生效的位置：lab-frame 和 boosted-frame 分支都会在 per-particle `getDensity(...)` 之后执行 `dens < density_min -> ZeroInitializeAndSetNegativeID(...)`，所以它当前是“先枚举、再失效删除”，不是前置阻止候选粒子生成。

- [x] 2026-05-24：继续收口 `<species_name>.profile`
  - 已补清这条 density profile 键的更硬 distributed-file prepare/runtime 分叉：`read_from_file` 路径在 `prepare(grids|pbox)` 阶段预加载数据后，只有 distributed 模式才会在 `PlasmaInjector::getInjectorDensity(li)` 里继续按 tile `LocalIndex` 做一次局部 `ExternalFieldView` 切换；非 distributed 模式则只复用单份全局 view，不会每个 tile 再次 materialize。
  - 已补清 CPU+OMP companion 边界：distributed density 路径下 `InjectorDensity::prepare(grids,...)` 会额外克隆每线程一份 `InjectorDensity` 包装，避免多个线程共享同一局部 from-file view。

- [x] 2026-05-24：继续收口 `<species_name>.self_fields_max_iters / self_fields_verbosity`
  - 已补清这组 species 级迭代上限与 verbosity companion 的更硬 solver-side 旁路：`RelativisticExplicitES::AddSpaceChargeField(...)` 会把 `pc.self_fields_max_iters / self_fields_verbosity` 传给 `computePhi(...)`，因此它们当前只命中 relativistic per-species 空间电荷 solve。
  - 已补清 companion 反向边界：`AddBoundaryField(...)`、`PhiFunctor` diagnostics、`LabFrameExplicitES` 和 `EffectivePotentialES` 继续直接消费 solver 级 `warpx.self_fields_max_iters / self_fields_verbosity`，不会读取 species 私有 override。

- [x] 2026-05-24：继续收口 `<species_name>.self_fields_absolute_tolerance`
  - 已补清这条 species 级绝对容差的更硬 solver-side 旁路：`RelativisticExplicitES::AddSpaceChargeField(...)` 会把 `pc.self_fields_absolute_tolerance` 传给 `computePhi(...)`，因此它当前只命中 relativistic per-species 空间电荷 solve。
  - 已补清 companion 反向边界：`AddBoundaryField(...)`、`PhiFunctor` diagnostics、`LabFrameExplicitES` 和 `EffectivePotentialES` 继续直接消费 solver 级 `warpx.self_fields_absolute_tolerance`，不会读取 species 私有 override。

- [x] 2026-05-24：继续收口 `<species_name>.self_fields_required_precision`
  - 已补清这条 species 级相对收敛阈值的更硬 solver-side 旁路：`RelativisticExplicitES::AddSpaceChargeField(...)` 会把 `pc.self_fields_required_precision` 传给 `computePhi(...)`，因此它当前只命中 relativistic per-species 空间电荷 solve。
  - 已补清 companion 反向边界：`AddBoundaryField(...)`、`PhiFunctor` diagnostics、`LabFrameExplicitES` 和 `EffectivePotentialES` 继续直接消费 solver 级 `warpx.self_fields_required_precision`，不会读取 species 私有 override。

- [x] 2026-05-24：继续收口 `<species_name>.initialize_self_fields`
  - 已补清这条 self-field 开关的更硬 startup/electrostatic 边界：fresh run 时 `WarpXInitData.cpp` 先把全部 species OR 成 `has_initialize_self_fields`，只要任一 species 置真，就会把整次 `ComputeSpaceChargeField(...)` 主链打开；而 `RelativisticExplicitES::InitData()` 又会按“任一 species 命中或边界电势已指定”单独决定是否先 `DefinePhiBCs(...)`。
  - 已补清它的 per-species 反向边界：真正到 `RelativisticExplicitES::ComputeSpaceChargeField()` 时，源码才按 `always_run_solve || species->initialize_self_fields` 逐 species 调 `AddSpaceChargeField(...)`，且后者入口仍会把 `charge==0` 的 neutral species 直接旁路掉。

- [x] 2026-05-24：继续收口 `<species_name>.do_continuous_injection`
  - 已补清这条连续注入键的更硬 moving-window 状态边界：`WarpX::MakeWarpX()` 在 `do_moving_window` 下会先给所有 particle/laser container 初始化 `m_current_injection_position`，并不先检查各自 `do_continuous_injection`；真正到 `WarpXMovingWindow.cpp` 的 step-loop 调度时，才只对 `pc.doContinuousInjection()` 为真的 container 继续构造 `particleBox`。
  - 已补清它的 step-loop/restart companion 分叉：即便 `do_continuous_injection=1`，当前也只有在 `particleBox.ok()` 且注入前沿确实推进时才会执行 `pc.ContinuousInjection(...)`；同时 checkpoint header 会无条件逐 species 保存和恢复 `m_current_injection_position`，不是只对连续注入 species 单独续写。

- [x] 2026-05-24：继续收口 `<species_name>.random_theta`
  - 已补清这条随机方位角键的更硬编译边界：`PhysicalParticleContainer` 只在 `WARPX_DIM_RZ / RCYLINDER / RSPHERE` 分支里 `query("random_theta", m_random_theta)`，因此 Cartesian 构建当前根本不会 materialize 这条 parser 键。
  - 已补清它的运行期 companion 分叉：`AddParticles.cpp::AddPlasma()` 当前只会对每个 cell 生成一次 `theta_offset` 并统一旋转该 cell 内整组新粒子；`ContinuousInjection()` 会继续复用同一个 `AddPlasma()` 路径，因此 moving-window 连续体注入同样沿用这份语义，而 `ContinuousFluxInjection()` 走 `AddPlasmaFlux()`，当前并不消费这条分支。

- [x] 2026-05-24：继续收口 `<species_name>.num_particles_per_cell_each_dim`
  - 已补清这条规则采样参数在 split 修正链里的更硬绑定：`PhysicalParticleContainer::SplitParticles()` 当前无条件读取 `plasma_injectors[0]->num_particles_per_cell_each_dim` 来缩放 split offset。
  - 已补清 multi-source 反向边界：若一个 species 同时存在基准 injector 和多个 `injection_sources`，后续被 split 的粒子并不会按其原始 source 分别选取对应 injector 的 per-dim sampling，而是统一只参考第一个 injector 的设置。

- [x] 2026-05-24：继续收口 `<species_name>.injection_style`
  - 已补清这条 style 分派的更硬初始化运行时边界：`singleparticle` source 在 `PhysicalParticleContainer::AddParticles()` 中完成一次 `AddNParticles(...)` 后会立刻 `return`，直接截断后续所有 injector；相对地 `multipleparticles / gaussian_beam / external_file` 不会提前返回。
  - 已补清 continuous-injection 的反向边界：`ContinuousInjection(...)` 与 `ContinuousFluxInjection(...)` 不会重放完整初始化 style 分派，而是只继续执行 `AddPlasma(...)` 或 `doFluxInjection()` 为真的 source。

- [x] 2026-05-24：继续收口 `<species_name>.injection_sources`
  - 已补清这条多 source 工厂入口的更细顺序边界：`PhysicalParticleContainer` 会先创建无前缀基准 injector，再按 `injection_sources` 给出的顺序依次追加 source-local injectors。
  - 已补清 source-provided `charge/mass` 的当前合同：后续遍历 `plasma_injectors` 时源码明确采用 “last value found”，因此若没有更高优先级的 `<species>.charge/.mass` 或 `species_type` 覆盖，多个 source 自带的 `charge/mass` 不是合并或一致性校验，而是由最后一个命中的 injector 覆盖前面结果。

- [x] 2026-05-24：继续收口 `<species_name>.mass`
  - 已补清这条质量输入的更细 external-file 边界：`mass` 和 `charge` 一样，也只在 IO rank 从 openPMD 读取，再通过 `ParallelDescriptor::Bcast(...)` 广播给其它 rank，不是所有 rank 各自独立读文件。
  - 已补清它的 restart 合同：checkpoint header 写回/恢复的是当时最终 `m_mass` 数值，不会重新回放 source/species_type/显式 parser 的优先级链；同时显式 `mass > 0` 的硬约束和“无质量粒子应改用 species_type”也一起压实了。

- [x] 2026-05-24：继续收口 `<species_name>.charge`
  - 已补清这条电荷输入的更细外部文件边界：`external_file` 路径下 `charge` 只在 IO rank 从 openPMD 读取，再通过 `ParallelDescriptor::Bcast(...)` 广播给其它 rank，不是所有 rank 各自独立读文件。
  - 已补清它的运行期后置覆写和 restart 合同：若 species 打开 `do_field_ionization`，`InitIonizationModule()` 会在更后面把 `charge != q_e` warning 后强制改成 `q_e`；而 checkpoint header 写回/恢复的也是当时最终 `charge` 数值，不会重新回放 source/species_type/显式 parser 的优先级链。

- [x] 2026-05-24：继续收口 `<species_name>.species_type`
  - 已补清这条 species 类型键的更硬 restart/factory 边界：`PhysicalParticleContainer::WriteHeader()` 当前只续写 `charge` 和 `m_mass`，`MultiParticleContainer::ReadHeader()` 也只是按当前已构造好的容器顺序把 header 读回，不会保存或恢复 `species_type` 字符串本身。
  - 已补清因此形成的运行合同：restart 时真正决定该 species 仍是普通物质容器还是 `PhotonParticleContainer` 的，仍是当前输入文件里的 `species_type / photon_species` 配置；checkpoint 只恢复已经选定容器上的物理量状态。

- [x] 2026-05-24：继续收口 `particles.rigid_injected_species`
  - 已补清这条 rigid-injection 入口的更细 restart 状态拆分：`RigidInjectedParticleContainer` 构造函数仍会从当前输入文件重新读取 `zinject_plane` 与 `rigid_advance`，但 checkpoint header 只续写 `zinject_plane_levels` 和 `vzbeam_ave_boosted`，不会保存静态模式配置本身。
  - 已补清运行 flag 的反向边界：`done_injecting_lev` 当前不写入 checkpoint，而是在 restart 后第一次 `Evolve()` 中再根据恢复出的 `zinject_plane_levels[lev]`、`moving_window_v + beta_boost*c` 和当前域边界重新计算。

- [x] 2026-05-24：继续收口 `particles.species_names`
  - 已补清这条名字表的更硬 lifecycle 边界：`MultiParticleContainer::ReadParameters()` 和 `ParticleBoundaryBuffer::getSpeciesNames()` 当前都各自带 `static initialized`，会分别把 `particles.species_names` 缓存进自己的成员视图；同一进程里后设 parser 表不会自动刷新已有粒子容器或 scraped-particle buffer 的 species 名单。
  - 已补清它和运行期名字解析的非对称：`deposit_on_main_grid / gather_from_main_grid / rigid_injected_species / photon_species` 这些 side-list 只允许命中 `particles.species_names`，但后续 `GetParticleContainerFromName()` 实际查的是 `species + lasers` 联合名字域，因此 startup side-list 校验范围和运行期容器查找范围并不完全一致。

- [x] 2026-05-24：继续收口 `warpx.split_high_density_boxes`
  - 已补清这条预切分开关的更硬 MPI gate：只有 `NProcs() > 1` 时，`PostProcessBaseGrids()` 才会真正 `queryAdd(...)` 读取这组键；单 MPI rank 下当前连 parser materialization 都不会发生。
  - 已补清 species 预估链的更细反向边界：遍历 `particles.species_names` 时，只要遇到一个不满足 `profile=parse_density_function + density_function(x,y,z)` 的 species，当前实现就会 `warning + break`，而不是跳过该 species 后继续累计其它 species；即便前面完成 box 递归 `chop`，初始化分发还要额外满足 `DistributionMapping::strategy() == SFC` 才会走等权重 SFC companion 分支。

- [x] 2026-05-24：继续收口 `algo.costs_heuristic_particles_wt / algo.costs_heuristic_cells_wt`
  - 已补清这对 heuristic companion 的更硬 coupled-default 边界：`WarpX` 构造期只有在 `costs_heuristic_cells_wt <= 0 && costs_heuristic_particles_wt <= 0` 同时成立时，才会一起进入默认值表；GPU 路径还会继续按 `PSATD/FDTD` 和 `nox` 细分配比，CPU 路径则统一回到 `0.1 / 0.9`。
  - 已补清单键覆写时的反向边界：若只显式给其中一个、另一个保持非正，当前实现不会替未给出的 companion 自动补上“匹配默认搭档”，而是直接保留这种不对称组合作为后续 `ComputeCostsHeuristic()` 和 `LoadBalanceCosts` heuristic 副本重算的输入。

- [x] 2026-05-24：继续收口 `boundary.potential_lo/hi_x/y/z`
  - 已补清这组边界电势字符串的更细 solver 分叉：它们和 `warpx.eb_potential(x,y,z,t)` 共享 `m_boundary_potential_specified` 总 gate；`LabFrameExplicitES` / `EffectivePotentialES` 会无条件先 `DefinePhiBCs(...)`，而 `RelativisticExplicitES` 只在相对论模式、species `initialize_self_fields` 或该总 gate 命中时才进入这条预备链；`HybridPIC` 下则只会 warning。
  - 已补清它和 Python 覆写的反向边界：Python 侧后设 `potential_*` 当前只会直接改 `potential_*_str` 并调用 `BuildParsers()`，不会重新运行 `ReadParameters()`，因此不会自动刷新 `m_boundary_potential_specified` 这条 “是否已指定边界电势” 的布尔状态。

- [x] 2026-05-24：继续收口 `warpx.eb_potential(x,y,z,t)`
  - 已补清这条 EB 电势输入虽然和 `boundary.potential_*` 共享 `m_boundary_potential_specified` 总 gate，但真正 consumer 只在 `eb_enabled` 的 `PoissonSolver / EffectivePotentialPoissonSolver` 分支里，通过 `setEBDirichlet(...)` materialize；非 EB Poisson 路径当前明确旁路它。
  - 已补清它和 Python 覆写的更细不对称：`set_potential_on_eb()` 当前走 `PoissonBoundaryHandler::setPotentialEB(...)`，只会改 `potential_eb_str` 并 `BuildParsersEB()`，不会重新运行 `ReadParameters()`，因此也不会顺带刷新 `m_boundary_potential_specified`。

- [x] 2026-05-24：继续收口 `boundary.verboncoeur_axis_correction`
  - 已补清这条输入当前只在 `WARPX_DIM_RZ / RCYLINDER / RSPHERE` 编译分支里才会通过 `WarpX::ReadParameters()` 真正读取；Cartesian 构建不会 materialize 这条 parser 键。
  - 已补清它的真实 consumer 是 `ApplyInverseVolumeScalingToCurrentDensity(...)` 与 `ApplyInverseVolumeScalingToChargeDensity(...)` 这两条 axis inverse-volume scaling helper，而不只是泛泛的 field push 路径；主 step-loop、magnetostatic、implicit 和 Python helper 都会继续复用同一组 axis-volume factor 分支。

- [x] 2026-05-24：继续收口 `particle_thermalizer.normal`
  - 已补清这条输入当前本身就是整个 `particle_thermalizer.*` 子族的 presence gate；若缺失，构造函数会直接返回并保持 `m_defined = false`，后续 `start/end/momentum_threshold/theta/species` 都不会进入有效运行链。
  - 已补清它的更硬 geometry 边界：只要显式给出 `normal`，`RZ / RCYLINDER / RSPHERE` 下当前会直接 abort，不是静默禁用；只有 `1D_Z / XZ / 3D` 的受限方向集合才是合法值。

- [x] 2026-05-24：继续收口 `warpx.numprocs`
  - 已补清 `apply_workaround_for_warpx_numprocs()` 当前只在 startup 检查 `pp_warpx.contains("numprocs")`，随后直接回写标量 `amr.blocking_factor = 1`；它不会同步重写 `blocking_factor_x/y/z`，也不是把整组 directional blocking-factor 语义等价替换掉。
  - 已补清 `PostProcessBaseGrids()` 的更细切块语义：最粗层域虽然按 `numprocs` 手工切块，但每个方向上的余数 `extra` 会优先分配给前 `extra[idim]` 个 block，而不是做完全均匀或 round-robin 分配。

- [x] 2026-05-24：继续收口 `algo.load_balance_intervals`
  - 已补清这条 parser 不只控制哪些 step 调 `LoadBalance()`，还决定 `WarpX::AllocLevelData()` 是否从一开始就为每个 level 分配 `costs[lev]` 与初始化 `load_balance_efficiency[lev]`；未激活时，load-balance 成本链当前整体保持空容器。
  - 已补清它的更细 manager/runtime 边界：启用后 `CheckLoadBalance(step)` 只在命中 interval 时调用 `LoadBalance()+ResetCosts()`，但 `RescaleCosts(step)` 仍会在每步按 `localPeriod(step+1)` 衰减成本；相对地，`LoadBalanceCosts` reduced diag 和末尾 load-balance summary 在未激活时都会直接空跑。

- [x] 2026-05-24：继续收口 `algo.load_balance_efficiency_ratio_threshold`
  - 已补清 `WarpX::LoadBalance()` 的更细 root-rank / broadcast 决策链：`currentEfficiency / proposedEfficiency` 的比较只在 IO rank 上执行，随后先广播单个 `doLoadBalance`，只有为真时才再广播 `ProcessorMap` 并在各 rank 上 `RemakeLevel(...)`。
  - 已补清并修正这条参数的反向边界：当前若 `threshold <= 0`，`doLoadBalance` 会保持默认 `false`，并不会“绕过门槛后自动接受 proposed mapping”，而是让运行期重分布链整体不触发。

- [x] 2026-05-24：继续收口 `algo.load_balance_with_sfc / algo.load_balance_knapsack_factor`
  - 已补清这对 companion 当前在 parser 期就是互斥的：一旦 `load_balance_with_sfc = 1`，`WarpX::ReadParameters()` 就不会再读取 `load_balance_knapsack_factor`。
  - 已补清它们在 runtime 的更细旁路边界：`LoadBalance()` 虽然总会先算一次 `nmax = ceil(nboxes/nprocs * load_balance_knapsack_factor)`，但只有 `makeKnapSack(...)` 分支才真正消费它；`makeSFC(...)` 分支对它完全旁路。

- [x] 2026-05-24：继续收口 `algo.load_balance_costs_update`
  - 已补清这条模式键在 `LoadBalance()` 和普通 timer hook 上的更细不对称：`Heuristic` 会在 `LoadBalance()` 前置重算成本，而 `Timers` 路径下各类 hook 还统一受 `costs[lev]` 非空约束；若 `load_balance_intervals` 没激活、未分配 `costs`，这些 hook 会整体空跑。
  - 已补清 `LoadBalanceCosts` reduced diag 的本地副本分叉：它先复制 `WarpX::getCosts(lev)`，然后只有在 `Heuristic` 模式下才对这份副本再次执行 `warpx.ComputeCostsHeuristic(costs)`；`Timers` 模式则直接导出在线累积好的 cost。

- [x] 2026-05-24：继续收口 `boundary.particle_lo/hi`
  - 已补清这组粒子边界输入的更细 consistency 边界：当前未显式给定时只会继承 field periodicity，而显式给定时 `check_consistency(...)` 也会继续强制粒子 periodic 与 field periodicity 锁步；粒子边界本身不能单独把一个非周期 field 方向改造成周期方向。
  - 已补清它和 field boundary 对称的 startup 时序：这组输入当前同样会在 `WarpXAMReXInit.cpp` 和 `WarpX::MakeWarpX()` 中各解析一次，先服务内部 `geometry.is_periodic` 汇总，再 materialize 成全局 `particle_boundary_lo/hi` 供 thermal/reflecting/PEC 邻接路径消费。

- [x] 2026-05-24：继续收口 `boundary.field_lo/hi`
  - 已补清这组 field boundary 输入的更细 startup 时序：当前会先在 `WarpXAMReXInit.cpp::set_periodicity_according_to_boundary_types()` 中解析一次，用来反推并 `addarr(...)` 内部 `geometry.is_periodic`；之后 `WarpX::MakeWarpX()` 又会第二次 `parse_field_boundaries()`，再把结果 materialize 成全局 `field_boundary_lo/hi`。
  - 已补清它和 `geometry.is_periodic` 的反向边界：用户显式给 `geometry.is_periodic` 当前只会触发 “仅供内部使用” 的 warning，不会成为 field boundary 的反向主入口；真正运行期稳定消费的仍是已经建好的全局 `field_boundary_lo/hi` 数组，而不是再次直接读取 `ParmParse("boundary")`。

- [x] 2026-05-24：继续收口 `warpx.do_single_precision_comms`
  - 已补清这条参数在 `ablastr::utils::communication` 里的更细 helper 语义：只有显式走 `ParallelCopy / FillBoundary / SumBoundary / OverrideSync` wrapper 的 `MultiFab` 路径时，源码才会 `mixedCopy(...) -> comm_float_type 临时 FabArray -> 通信 -> mixedCopy(...)`；否则直接回落到原生 AMReX 通信。
  - 已补清它的更硬旁路边界：`iMultiFab` 的 `FillBoundary(...)` overload 没有这条布尔输入，若干 direct `mf.FillBoundary(...)` 路径和粒子 `Redistribute()` 也都不消费它；因此它当前不是所有 WarpX 通信的统一降精度总开关，只覆盖显式接到 ablastr `MultiFab` helper 的那部分场/辅助场/solver 通信。

- [x] 2026-05-24：继续收口 `warpx.refine_plasma`
  - 已补清这条 AMR 注入细化开关的更细 lifecycle 边界：`findRefinedInjectionBox()` 里的 `refine_injection / fine_injection_box / rrfac` 当前都是函数内 `static` 缓存，只会在 `moving_window_active(step+1) && refine_plasma && do_continuous_injection && numLevels()==2` 首次命中时 materialize，一旦锁定就不会随之后的 mesh/regrid 重新计算。
  - 已补清它和注入时序的反向边界：虽然 `AddPlasma()` 同时服务初始注入与 moving-window 连续注入，但这条 refine 路径本身硬要求 `do_continuous_injection`；因此初始注入不会命中 refined-injection cache，而真正命中的静态快照会继续同时服务体注入 `nppc/position` 加密和 flux 注入面积权重修正。

- [x] 2026-05-24：继续收口 `warpx.ref_patch_function(x,y,z)`
  - 已补清这条 refined-patch parser 键在 `ErrorEst()` 里的更细真值语义：当前不是“非零即真”，而是只有 parser 返回值恰好等于 `1` 时，对应 cell 才会被置成 `TagBox::SET`。
  - 已补清它和 `fine_tag_lo/hi` 的 companion 反向边界：`ConvertLabParamsToBoost()` 发生在 `ReadParameters()` 之前，且在 `gamma_boost > 1 && amr.max_level > 0` 时只会重读显式 bbox，不会 materialize 这条 parser 字符串；因此 `ref_patch_function` 当前只进入更晚的 `ReadParameters()` / `ErrorEst()` 打标分支，不能单独承担 boosted-frame 下 refined patch 的早期坐标改写输入。

- [x] 2026-05-24：继续收口 `warpx.fine_tag_lo/hi`
  - 已补清这组 refined-patch bbox 的更细启动时序边界：`WarpX::MakeWarpX()` 会在 `ReadParameters()` 之前先执行 `ConvertLabParamsToBoost()`；一旦 `gamma_boost > 1` 且 `amr.max_level > 0`，源码就会直接对 `fine_tag_lo/hi` 走 `getArrWithParser(...)`，不是可缺省的 `query...`。
  - 已补清它和 `ref_patch_function(x,y,z)` 的反向边界：因此在当前 boosted-frame + refined-patch 早期路径里，显式 bbox 仍是 boost 前坐标改写的真实输入，而后置的 parser fallback 只会在更晚的 `ReadParameters()` / `ErrorEst()` 分支里 materialize，不足以替代这一步的 early boost wiring。

- [x] 2026-05-21：继续收口 `warpx.verbose`
  - 已补清这条参数和 diagnostics 的默认桥接：它不只控制 `main.cpp` 的 `Total Time` 与 `WarpXEvolve.cpp` 的 `verbose_step` / `limit_verbose_step` 日志节流，还会在 `Diagnostics::BaseReadParameters()` 里通过 `pp_warpx.query("verbose", m_verbose)` 成为 diagnostics 实例的全局默认 verbosity，之后才允许 `<diag>.verbose` 单独覆写。
  - 已补清它的更细 startup 反向边界：`WarpXInitData.cpp` 无条件执行 `WriteUsedInputsFile()`，而 `write_used_inputs_file(...)` 的默认实参 `verbose=true` 会固定打印 used-inputs 文件位置；与此同时，first-step `checkEarlyUnusedParams()` 的 unused-input 明细展开取决于 `amrex.parmparse.verbose`，不是 `warpx.verbose`，但 `WarnManager` 的 `PrintGlobalWarnings("FIRST STEP")` 仍会无条件输出。

- [x] 2026-05-21：继续收口 `qed_qs.tab_* / qed_bw.tab_*`
  - 已补清这两组 table-shape companion 的更细 IO-rank 解析边界：它们不是各 rank 本地重复解析的普通形状输入，而是只在 IO rank 组装 `ctrl` 时真正读取，然后通过 `compute_lookup_tables(...) -> export_lookup_tables_data() -> ReadAndBcastFile(...)` 固化成全局 raw table，非 IO ranks 本地不会再单独解析。
  - 已补清它们的超范围处理合同：Quantum Sync 这侧的 `tab_*_chi_min/max` 会把超范围 `chi` 按端点处理；Breit-Wheeler 这侧的 `tab_dndt_chi_min/max` 会切到 analytical approximation，而 `tab_pair_chi_min/max` 则按端点处理；这些端点/近似语义同样是在 IO-rank 生成表时一次性固定到全局 engine 状态里的。

- [x] 2026-05-21：继续收口 `qed_qs.lookup_table_mode / qed_bw.lookup_table_mode`
  - 已补清这两条模式键在 `generate/load/builtin` 三分支里的更细 engine 初始化合同：`generate` 不只决定 table 来源，还会让 IO rank 直接保留已生成的 engine 状态，而非 IO ranks 仅在广播后通过 `init_lookup_tables_from_raw_data(...)` 重建。
  - 已补清 `load` 与 `builtin` 的反向边界：`load` 会在广播后让当前 rank 都走 raw-data 重建，`builtin` 则完全绕开文件 I/O 直接 `init_builtin_tables(...)`；三条路径最后都统一落到 `are_lookup_tables_initialized()` 成功断言。

- [x] 2026-05-21：继续收口 `qed_qs.save_table_in/load_table_from` 与 `qed_bw.save_table_in/load_table_from`
  - 已补清这两组路径参数在 `generate` 分支里的更细 IO-rank 非对称性：只有 IO rank 会真正 `compute_lookup_tables(...) -> export_lookup_tables_data() -> write(...)`；随后虽然所有 ranks 都会 `ReadAndBcastFile(...)`，但只有非 IO ranks 才继续 `init_lookup_tables_from_raw_data(...)`，生成该表的 IO rank 会显式跳过这一步。
  - 已补清它们在 `load` 分支里的对称初始化边界：表文件广播之后当前 rank 都会执行 `init_lookup_tables_from_raw_data(...)`，而不是只让非 IO ranks 重建；因此这些参数当前不仅决定磁盘落点，也决定 “仅非 IO ranks 重建” 与 “全体 ranks 重建” 两种不同的 lookup-table 初始化合同。

- [x] 2026-05-21：继续收口 `qed_schwinger.ele_product_species / pos_product_species`
  - 已补清这两条参数在 Schwinger 产物写入链里的更细 tile append 边界：`doQEDSchwinger()` 会在每个 `MFIter` 上先取出 `pc_product_ele/pos->ParticlesAt(level_0, mfi)`，再把旧粒子数 `np_ele_dst / np_pos_dst` 作为 `filterCreateTransformFromFAB<1>(...)` 的 append 起点传入；因此它们不只绑定目标 container，也绑定了每个目标 tile 的新增区间起点。
  - 已补清它们和收尾链的反向边界：底层 helper 会先分别对目标电子/正电子容器构造 `SmartCreateFactory`，按各自目标容器 policy 创建粒子，但真实坐标落在命中 cell 的 lower node，而创建判定仍来自 cell 级 `mask/arrNumPartCreation`；随后同一个 `transform(...)` 会把该 cell 的同一份 `total_weight` 对称写回电子/正电子两侧，而且 helper 只返回单个 `num_added`，因此当前两侧新增区间长度也被锁成严格相等；再对两侧目标 tile 末尾执行 `DefaultInitializeRuntimeAttributes(...)`，回到 `doQEDSchwinger()` 后再对新增区间调用 `setNewParticleIDs(...)`。所以这两条参数当前绑定的是“容器选择 -> tile 追加 -> 目标容器初始化策略 -> node/cell 语义错位 -> 对称权重回填 -> 对称新增计数 -> 默认属性补齐 -> 新粒子 ID 收尾”的整条 Schwinger 产物写入链。

- [x] 2026-05-21：继续收口 `warpx.do_qed_schwinger`
  - 已补清这条总开关在主 step-loop 里的更细 caller-side 时序：它当前是独立的 pre-injection、pre-push pass，稳定位于 `doFieldIonization()` 与普通 `doQEDEvents()` 之后、`particleinjection` 回调和 `OneStep(...)` 之前，不和普通 QED photon/lepton event loop 复用同一个 caller。
  - 已补清它和 level/data-source 覆盖范围的反向边界：`WarpX::doQEDEvents()` 仍按 `lev=0..finest_level` 逐 level 转发普通 QED 事件，而 `doQEDSchwinger()` 自身固定只消费 level 0 的 `Geom` 与 `Efield_aux/Bfield_aux`，并在 pass 开始时先对目标电子/正电子容器执行 `defineAllParticleTiles()`；因此这条开关当前接入的是“每步调一次、但只覆盖 level 0，且固定走 aux-field + 目标 tile 预展开”的独立 Schwinger 运行阶段。

- [x] 2026-05-21：继续收口 `qed_schwinger.xmin/ymin/zmin/xmax/ymax/zmax`
  - 已补清这组参数在 `ComputeSchwingerGlobalBox()` 里的更细哨兵边界：若某个方向整个区间已落到 `ProbLo/ProbHi` 之外，源码会直接把 `small/big` 设成 `std::numeric_limits<int>::max()/lowest()`，让后续 tile 交集自然退化为空，而不是继续走正常 cell 选择。
  - 已补清它和维度/运行时生成区域的几何配套：`ymin/ymax` 当前只在 `WARPX_DIM_3D` parser 分支里真正读取，而 2D `XZ/RZ` 路径从 parser 到 `ComputeSchwingerGlobalBox()` 都只消费 `x/z` 边界；域内方向仍按“当前 pair 在 cell 的 lower nodes 上创建”这一规则用 `ceil/floor` 选 index，`doQEDSchwinger()` 还会先把 `mfi.nodaltilebox()` 通过 `enclosedCells(...)` 变成 cell-centered `box`，再和 `global_schwinger_box` 做真正的 tile 级裁剪，避免在 tile 边界重复创建粒子。

- [x] 2026-05-21：继续收口 `qed_schwinger.threshold_poisson_gaussian`
  - 已补清这条参数在 Schwinger 采样里的更细随机分支边界：`getSchwingerProductionNumber(...)` 会先按局部 `E/B + dV + dt` 计算 `expectedPairNumber`，再在 `expected <= threshold` 时走 `RandomPoisson(...)`，否则走均值 `expected`、标准差 `sqrt(expected)` 的 `RandomNormal(...)`；Gaussian 分支若抽到负值，还会被直接截断成 `0`。
  - 已补清它和宏粒子创建链的反向边界：当前 Schwinger 路径会先把 cell 级抽样结果写进 `arrNumPartCreation`，再只按 `> 0` 建 mask 决定哪些 cell 真正进入 create/transform 链；随后 helper 先对 mask 做 `ExclusiveSum`，并把 `num_added` 固定算成 `N * 命中 cell 数`，所以固定实例化的 `filterCreateTransformFromFAB<1>` 当前并不会按总 pair 数扩增宏粒子个数，而是把模板常数锁在“每个命中 cell、每个 species 一个宏粒子”；`SchwingerTransformFunc` 再把这份 `NumPartCreation / total_weight` 均分回新电子/正电子权重。

- [x] 2026-05-21：继续收口 `qed_qs.photon_creation_energy_threshold`
  - 已补清这条参数在 Quantum Sync photon cleanup 里的更细两阶段边界：`cleanLowEnergyPhotons(...)` 只会在 `doQedQuantumSync()` 生成新 photon 之后扫描本轮新增样本，用能量平方比较后把低能 photon 标成 `Invalid`，不会在 QED pass 内直接删除。
  - 已补清它和后续删除链的反向边界：真正的物理移除要走后续通用 `deletuInvalidParticles()` sweep；同名 API 还被 resampling、EB 吸收等其它路径复用，所以这条参数更准确地是“先标失效、再交给通用粒子清理链”的运行时筛除门槛，不是 QED 专属删除开关。
  - 已再补清这条参数的 append-window 边界：`doQedQuantumSync()` 会先缓存 `np_dst = dst_tile.numParticles()`，再把 `num_added` 传给 `cleanLowEnergyPhotons(dst_tile, np_dst, num_added, ...)`；而后者内部会把 `idcpu/ux/uy/uz` 指针统一偏移到 `old_size=np_dst` 之后，因此只扫描本轮新追加 photon 区间，不会回头重筛旧 photon。
  - 已再补清它和 source optical-depth 重置的顺序边界：`cleanLowEnergyPhotons(...)` 运行前，`filterCopyTransformParticles(...)` 内部的 `PhotonEmissionTransformFunc` 已先在同一次事件里重采样 source 粒子的 `opticalDepthQSR`，所以这条阈值当前只作用于 product photon 侧的新增区间，不会反过来改写 source 粒子的发射后状态。
  - 已再补清这条参数和 append-to-sweep 链的顺序边界：`doQedQuantumSync()` 会先对同一新增区间执行 `setNewParticleIDs(dst_tile, np_dst, num_added)`，然后才 `cleanLowEnergyPhotons(...)`；这些被标成 `Invalid` 的低能 photon 当前不会在 QED pass 内当场删掉，而是继续交给主 step-loop 中 embedded-boundary scraping 之后的统一 `deleteInvalidParticles()` sweep。

- [x] 2026-05-21：继续收口 `<species_name>.qed_quantum_sync_phot_product_species`
  - 已补清这条参数的更细 append-tile 边界：`doQedQuantumSync()` 不只按它解析出来的 species id 选出 `pc_product_phot`，还会在 tile 循环前对 source/product 两侧统一 `defineAllParticleTiles()`，随后每个 `pti` 上都先取 `np_dst = dst_tile.numParticles()`，再把新 photon 追加到这个目标 `dst_tile`。
  - 已补清它和后续新增区间链的闭包：追加完成后，`setNewParticleIDs(dst_tile, np_dst, num_added)` 与 `cleanLowEnergyPhotons(dst_tile, np_dst, num_added, ...)` 都继续只作用在同一个 product tile 的新增区间上，因此这条参数实际固定的是 Quantum Sync photon append/ID/cleanup 都落到哪一个目标 photon tile。

- [x] 2026-05-21：继续收口 `<species_name>.do_qed_quantum_sync`
  - 已补清这条参数的更细事件后重置边界：它不只在 species 构造期新增 `opticalDepthQSR`、强制读取 `qed_quantum_sync_phot_product_species`，并在 `InitQED()` 中只对 `has_quantum_sync()` 的 species 绑定共享 `QuantumSynchrotronEngine`、累计 `m_nspecies_quantum_sync` 并决定是否进入 `InitQuantumSync()`。
  - 已补清它和 photon-emission transform 的闭包：`doQedQuantumSync()` 构造 `PhotonEmissionTransformFunc(...)` 时会把 `build_optical_depth_functor()` 与 `GetRealCompIndex("opticalDepthQSR") - NArrayReal` 一起传入；而 `QEDPhotonEmission.H` 会在真正发射 photon 后立刻执行 `src.m_runtime_rdata[m_opt_depth_runtime_comp][i_src] = m_opt_depth_functor(engine)`，也就是同一次发射事件内马上重采样 source 粒子的 `opticalDepthQSR`，不是留到下一步 push 再补。

- [x] 2026-05-21：继续收口 `<reduced_diags_name>.weighting_function(x,y,z)`
  - 已补清这条参数在 `ChargeOnEB` 里的更细 surface-integral 作用域：它只乘在 level 0、仅对 EB partial cells 重建出的局部 `dS·E` 面积分贡献上，而不是全域体积分或原始场值本身。
  - 已补清它和物理量汇总的闭包关系：权重点取自 `bndryCent` 还原的 EB 面元质心 `(x,y,z)`，随后所有加权贡献会先原子加到单个 `surface_integral`，再 host 拷回、MPI 归约并统一乘 `epsilon_0` 写成 `Q_tot`。

- [x] 2026-05-21：继续收口 `<reduced_diags_name>.bin_number_1/bin_min_1/bin_max_1/bin_number_2/bin_min_2/bin_max_2`
  - 已补清这组参数在 `DifferentialLuminosity2D` 里的更细累计表闭包：它们不只决定运行时 `E1/E2` 双轴落 bin，还会在构造期直接决定 `m_h_data_2D/m_d_data_2D` 的二维表 shape。
  - 已补清它们和归一化/快照几何的闭包关系：`bin_size_1*bin_size_2` 继续进入 `d2L_dE1_dE2` 的 `m^-2 eV^-2` 归一化，而同一组 `bin_min/bin_size` 还会在输出步写成 `gridGlobalOffset/gridSpacing + axisLabels`，对应当前累计表的 openPMD 快照几何。

- [x] 2026-05-21：继续收口 `<reduced_diags_name>.openpmd_backend / file_min_digits`（`DifferentialLuminosity2D`）
  - 已补清这组参数在 `DifferentialLuminosity2D` 里的更细 fallback 不对称：`openpmd_backend` 仍为 `default` 时会显式 fallback 到 `WarpXOpenPMDFileType()` 并 `pp_rd_name.add(...)` 回写；`file_min_digits` 则只是本类私有默认值 `6`，没有对应的动态 fallback。
  - 已补清它们的 mesh-snapshot 反向边界：`file_min_digits` 当前只进入固定文件名模板，不改写 `series.iterations[step+1]`；writer 固定写 `meshes["d2L_dE1_dE2"]` 的累计 luminosity 表快照，并额外带 `UnitDimension{L:-6,M:-2,T:4}`，不像 `ParticleHistogram2D` 那样写 parser metadata。
  - 已再补清它们和 `ParticleHistogram2D` 的同壳分工：`WriteToFile()` 每个输出步同样都会重新打开同一个 series `filepath`，真正区分时间步的是内部 `series.iterations[step+1]`，因此 `file_min_digits` 控制的仍是 series 容器名样式；但这里被这组参数承载的是累计 luminosity snapshot mesh，而不是带 `function_abscissa / function_ordinate / filter` 的 histogram metadata。

- [x] 2026-05-21：继续收口 `<reduced_diags_name>.raw_fields`
  - 已补清这条废弃兼容入口的更细 parser 边界：当前只按“是否出现过 `raw_fields` 这个键”触发，与取值 `0/1` 无关；并且 abort 发生在 geometry、`integrate`、`interp_order`、`do_moving_window_FP` 已解析之后，但早于 boosted-frame warning 和 `interp_order <= particle_shape` 断言。
  - 已补清它和当前 gather 路径的反向兼容边界：报错给出的唯一迁移提示仍是 `interp_order = 0`，但 `FieldProbe` 常规 `doGatherShapeN(...)` dispatch 当前稳定展开的是 1 到 4 阶 gather，因此兼容提示与现有常规路径并不完全对齐。

- [x] 2026-05-21：继续收口 `<reduced_diags_name>.interp_order`
  - 已补清这条参数在 `FieldProbe` 里的更细默认链与 gather 边界：未给定时会保留 `FieldProbe.H` 里的本地默认值 `1`，运行时只受 `algo.particle_shape` 上界约束，并继续传给 `doGatherShapeN(...)` 作为场插值 stencil 键。
  - 已补清它和废弃兼容入口的反向边界：`FieldGather.H` 这条常规 dispatch 当前稳定展开的是 1 到 4 阶 gather，而 `raw_fields` 的迁移提示却写成 `interp_order = 0`；因此兼容提示比当前常规 gather 路径暴露出的稳定展开范围更宽。

- [x] 2026-05-21：继续收口 `<reduced_diags_name>.target_normal_*/target_up_*/detector_radius`
  - 已补清这组参数在 `FieldProbe` 里的更细 plane-grid 构造链：`InitData()` 会先归一化 `target_normal/target_up`，再通过 `orthotarget`、`direction` 和 `detector_radius` 构造 `uppercorner / lowercorner / loweropposite` 三个角点，并据此按双重循环铺成 `m_resolution^2` 个 probe 点。
  - 已补清它们和输出规模的闭包关系：这套 `N^2` 点仍只在 `IOProcessor()` 上进入 `AddNParticles(...)`，随后继续闭包到 `m_valid_particles` 与 `WriteToFile()` 的实际输出行数；相对地，`ProbeInDomain()` 仍只检查静态 `x_probe/y_probe/z_probe`。

- [x] 2026-05-21：继续收口 `<reduced_diags_name>.resolution`
  - 已补清这条参数在 `FieldProbe` 里的更细初始化闭包：`Line` 仍生成 `N` 个采样点、`Plane` 生成 `N^2` 个采样点，但这些点只会在 `IOProcessor()` 上填充到 `xpos/ypos/zpos`，再统一 `AddNParticles(...)` 建 probe 粒子集合。
  - 已补清它和输出规模的闭包关系：输出步里的 `m_data.reserve(numparticles * noutputs)`、`Gpu::DeviceVector(np*noutputs)`、`m_valid_particles = total_data_size / noutputs` 和 `WriteToFile()` 实际输出行数都会继续复用这套 probe 粒子总数。

- [x] 2026-05-21：继续收口 `<reduced_diags_name>.do_moving_window_FP`
  - 已补清这条参数在 `FieldProbe` 里的更细 runtime/output 边界：moving window 会沿 `moving_window_dir` 真实重写 probe 粒子位置，并把这些更新后的 `x/y/z` 连同场值继续打包进 `m_data/m_data_out`。
  - 已补清它和 gate/sort 的反向边界：`ProbeInDomain()` 在 compute/write 两侧仍只检查静态 `x_probe/y_probe/z_probe`，而 `WriteToFile()` 仍按稳定 particle id 重排 `sorted_data`；因此这条参数会改写输出坐标值，不会改写入域参考点或每行 probe 身份顺序。

- [x] 2026-05-21：继续收口 `<diag_name>.coarsening_ratio`
  - 已补清这条参数在 full diagnostics 里的更细几何对齐边界：`FullDiagnostics::InitializeBufferData()` 不只检查 `boxArray.coarsenable(m_crse_ratio)`，还会在 `diag_lo/hi` 裁剪后做 `ba.coarsen(...).refine(...)` 与 `domain.coarsen(...).refine(...)` 对齐，并强制 `m_crse_ratio.min() > 0`，而 reduced-dimension 退化成单层切片时对应方向只能取 `1`。
  - 已补清它和 particle output 的反向边界：`ParticleReductionFunctor` 只会在粒子先沉积到临时 `red_mf`、必要时再做平均之后，才按 `m_crse_ratio` 执行 `ablastr::coarsen::sample::Coarsen(...)`；相对地 `BoundaryScrapingDiagnostics::InitializeBufferData()` 当前为空，普通 `ParticleDiag` writer 也不读取 `m_crse_ratio`，所以这条参数不会改写 boundary scraping 或常规逐粒子输出的 copy/write 语义。

- [x] 2026-05-21：继续收口 `<diag_name>.file_prefix`
  - 已补清这条参数在 boundary-scraping 里的更细时序边界：per-boundary 路径不是在 `ReadParameters()` 时永久改写，而是到 `BoundaryScrapingDiagnostics::Flush()` 才临时派生成 `m_file_prefix + "/particles_at_" + boundaryName(i_buffer)`，再交给对应 writer。
  - 已补清它和 BTD 的反向分叉：BTD plotfile 会在 `BTDiagnostics::Flush()` 里先把同一基前缀改写成 `Concatenate(m_file_prefix, i_buffer, ...) + "/buffer"` 的 per-buffer 临时根目录，而 `MergeBuffersForPlotfile()` 再派生最终 `snapshot_path`；相对地 BTD openPMD 保留原始 `m_file_prefix`，只在 `FlushFormatOpenPMD::WriteToFile()` 里把实际 iteration 缔号切成 `snapshotID`。

- [x] 2026-05-21：继续收口 `<diag_name>.write_species`
  - 已补清这条参数和 reduced-domain 禁粒子输出之间的更细状态清空不对称：`write_species=0` 会在 `InitData()/InitDataAfterRestart()` 里同时清空 `m_output_species` 与 `m_output_species_names`，而显式给出 `diag_lo/hi` 时当前实现只会给现有 `ParticleDiag` 打开 `m_do_geom_filter` 后清空 per-buffer `m_output_species`，species 名单本身仍保留。
  - 已补清它和 BTD flush-reset 的反向边界：`BTDiagnostics::DerivedInitData()` 会再次用 `write_species` 重算 `m_do_back_transformed_particles`，但 flush 末端的 `ResetTotalParticlesInBuffer()/ClearParticleBuffer()` 实际只检查 `!m_output_species_names.empty()`，并不再看本次是否真的写出了粒子文件或 `m_do_back_transformed_particles` 当前是否为真；相对地，只有 `write_species=0` 真正清空了 species 名单，这条 reset 链才会一起被切断。

- [x] 2026-05-21：继续收口 `<diag_name>.species`
  - 已补清这条参数在 boundary-scraping 与 BTD 里的更细零粒子 writer 结果差异：两条路径都会先按 species 名单绑定 runtime 对象，但 boundary-scraping 会在 `Flush()` 里先按所有 species 汇总 `n_particles`，只要为零就整体 `return`，连 per-boundary/per-species 目录都不会生成。
  - 已补清 BTD plotfile 的反向边界：`MergeBuffersForPlotfile()` 首轮 flush 仍会先按 `m_output_species_names` 创建 per-species 目录与 `Level_0` 子目录，并写/改 species `Header`；只有当某个 species 的 `m_total_particles == 0` 时，源码才在 header 合并后 `continue`，跳过 `Particle_H` 与 `DATA_*` 的 rename/interleave，所以 species 绑定成功不等于该次 flush 一定有粒子数据文件。

- [x] 2026-05-21：继续收口 `<reduced_diags_name>.integrate`
  - 已补清这条参数在 `FieldProbe` 里的更细 interval/gather 边界：`integrate=1` 时每步都会继续执行场采样和粒子态更新，但只有命中 interval 时才真正 `clear/reserve m_data`、回拷并 `Gather/Gatherv` 到 `m_data_out`；`integrate=0` 则外层直接跳过非 interval 步。
  - 已补清它和 moving-window 的反向边界：由于 `m_last_compute_step` 在 `ComputeDiags()` 末尾无条件更新，`do_moving_window_FP` 路径里的 `step_diff` 会在 `integrate=1` 下退化成单步位移，而在 `integrate=0` 下按跨多个未计算步的累计间隔一次性前推。

- [x] 2026-05-21：继续收口 `<reduced_diags_name>.openpmd_backend / file_min_digits`
  - 已补清这组参数在 `ParticleHistogram2D` 里的更细 fallback 不对称：`openpmd_backend` 仍为 `default` 时会显式 `WarpXOpenPMDFileType()` 选当前构建可用 backend，并 `pp_rd_name.add(...)` 回写；`file_min_digits` 则只是本类私有默认值 `6`，没有对应的动态 fallback。
  - 已补清它们的 filename/iteration 反向边界：`file_min_digits` 当前只进入固定模板 `openpmd_%0NT.<backend>`，不会改写 `series.iterations[step+1]` 这条 openPMD iteration key；缺少 `WARPX_USE_OPENPMD` 时整条 writer 会直接 abort，不会回退成文本 reduced diag。
  - 已再补清这组参数的更细 writer-side 分工：`WriteToFile()` 每个输出步都会重新打开同一个 series `filepath`，真正区分时间步的是内部 `series.iterations[step+1]`，因此 `file_min_digits` 控制的是 series 容器名样式而不是每步独立文件名；同时这两条参数都不会改写 `function_abscissa / function_ordinate / filter` 这批 mesh metadata 内容。

- [x] 2026-05-21：继续收口 `<reduced_diags_name>.histogram_function_abs/ord(t,x,y,z,ux,uy,uz,w)`
  - 已补清这两条参数在 `ParticleHistogram2D` 里的更细执行顺序：可选 `filter_function(...,w)` 先做 early-return，只有通过筛选的粒子才会继续评估 `f_abs / f_ord`，再进入 `floor(...)` 双轴落 bin 与越界丢弃链。
  - 已补清它们和 bin 权重的反向边界：`histogram_function_abs/ord` 只定义双轴坐标，最终写入每个 bin 的数值仍来自独立 `value_function(...,w)`；同时 openPMD 只把这两条表达式写成 `function_abscissa / function_ordinate` 与 `AxisLabels`，不会把 `value_function` 一并写回 metadata。

- [x] 2026-05-21：继续收口 `<reduced_diags_name>.histogram_function(t,x,y,z,ux,uy,uz)`
  - 已补清这条参数的更细 2D 运行链：`histogram_function_abs/ord` 在 `ParticleHistogram2D` 里只定义双轴落 bin 坐标，不单独决定最终写入每个 bin 的权重。
  - 已补清它的 writer metadata 反向边界：2D openPMD 路径会把 `function_abscissa / function_ordinate` 与 `AxisLabels` 写出去，但不会把独立的 `value_function(...,w)` 一并写成 metadata，因此输出文件只保留坐标轴语义，不完整保留最终 bin 权重来源。

- [x] 2026-05-21：继续收口 `<reduced_diags_name>6filter_function(t,x,y,z,ux,uy,uz)`
  - 已补清这条 histogram parser filter 的更细真值语义边界：现在明确到 1D `ParticleHistogram` 虽写成 `fun_filterparser(...) == 0._rt` 拒绝，而 2D sibling 虽写成 `static_cast<bool>(fun_filterparser(...,w))` 判真，但当前实现本质上都属于“零值拒绝器”而不是“正值保留器”，因此负的非零返回值同样会保留样本。
  - 已补清它在 2D 路径里的固定 companion 顺序：`filter_function(...,w)` 只是 `filter -> histogram_function_abs/ord(...,w) -> value_function(...,w)` 这条 kernel 链最前端的粒子级 early-return，不会改写 writer 或 openPMD metadata 路径。

- [x] 2026-05-21：继续收口 `<reduced_diags_name>.species`
  - 已补清这条参数的更细失败时序边界：`ParticleHistogram{,2D}` 仍在构造期把 species 名固定映射成 index，错名立即 abort；`BeamRelevant` 继续只在 `ComputeDiags()` 时按名字筛选，因此错名会静默退化成零数据输出。
  - 已补清双束路径的 startup-vs-runtime 分叉：`ColliderRelevant` 会在构造期立刻 `GetParticleContainerFromName(...)` 并额外检查每束 `q != 0`，而 `DifferentialLuminosity{,2D}` 要到第一次命中 interval 的 `ComputeDiags()` 才解析 species 名，因此错名会延迟到首个有效计算步才触发 helper assert。

- [x] 2026-05-21：继续收口 `<reduced_diags_name>.bin_number / bin_min / bin_max`
  - 已补清这组参数的更细 histogram/openPMD 轴定义链：它们不只进入 1D/2D reduced-diag 的 header、运行时落 bin 和 luminosity 归一化，还会继续写进 `ParticleHistogram2D / DifferentialLuminosity2D` 的 openPMD `gridGlobalOffset / gridSpacing / dataset shape`。
  - 已补清它的输入合法性反向边界：当前相关构造函数没有额外 assert `bin_number > 0` 或 `bin_max > bin_min`，原值会直接流入 `m_bin_size`、`floor(...)`、openPMD shape/spacing，以及 `1/bin_size` 或 `1/(bin_size_1*bin_size_2)` 归一化链。

- [x] 2026-05-21：继续收口 `<reduced_diags_name>.type`
  - 已补清这条参数的更细多态运行链：它不只决定 `FieldPoyntingFlux` 是否具备 `ComputeDiagsMidStep()` 与 checkpoint 状态续写 override，还继续决定是否命中 `FieldProbe::LoadBalance()` 这条独立 probe 粒子 `Redistribute()` 分支。
  - 已补清它的 writer-side backend 反向边界：`ParticleHistogram2D / DifferentialLuminosity2D` 会把同一个 `type` 直接分派到 openPMD-only writer，若未编译 `WARPX_USE_OPENPMD`，当前会在 `WriteToFile()` 时直接 abort，而不是回退成文本 reduced-diag writer。
  - 已再补清它的 parser/override 边界：`MultiReducedDiags` 构造期对每个实例用的是 `pp_rd_name.get("type", rd_type)`，所以 type 缺失会直接硬失败，不存在静默默认类型；同时当前本地源码里 `LoadBalance()` 真正覆写的只有 `FieldProbe`，而 mid-step/checkpoint 真正覆写的仍是 `FieldPoyntingFlux`，因此这条参数还决定 manager fanout 到底会落到有效 override 还是默认空实现。

- [x] 2026-05-21：继续收口 `warpx.reduced_diags_names`
  - 已补清这条参数的更细 factory / startup gate：`WarpXInitData.cpp` 仍会无条件构造 `MultiReducedDiags`，但只有 `m_plot_rd != 0` 时才会在初始化末尾和主 step-loop 中真正进入 `LoadBalance()/ComputeDiags()/WriteToFile()` 这条 reduced-diag fanout。
  - 已补清它的 implicit/checkpoint 反向边界：implicit solver 路径会统一调用 `ComputeDiagsMidStep()`，checkpoint/restart 又会统一 fanout `WriteCheckpointData()/ReadCheckpointData()`，但 `ReducedDiags` 基类这三条默认都是空实现，所以当前只有像 `FieldPoyntingFlux` 这类显式 override 的 reduced diag 才会真正消费 mid-step 与持久化状态链。
  - 已再补清这条参数的空容器/no-op 分界：只要 `m_plot_rd != 0`，`MultiReducedDiags` 的 `LoadBalance / ComputeDiags / ComputeDiagsMidStep / WriteCheckpointData / ReadCheckpointData` 就都会按名字表遍历全部实例，但这只保证 fanout 发生，不保证有实质效果；当前真正命中 `LoadBalance()` override 的只有 `FieldProbe`，命中 mid-step/checkpoint override 的仍是 `FieldPoyntingFlux`，其余大量实例在这些链上继续退化成默认空实现。

- [x] 2026-05-21：继续收口 `vismf.headerversion / verbose`
  - 已补清这组输入的一次性初始化边界：它们不是每次 `VisMF::Read/Write` 都重新 query，而是只在 `VisMF::Initialize()` 首次命中、`initialized == false` 时读入静态状态；之后若没有显式 `SetHeaderVersion/SetVerbose`，单纯再改 `ParmParse("vismf")` 已不会影响当前进程里的 `currentVersion/verbose`。
  - 已补清它和 WarpX writer 邻接链的反向边界：plotfile/checkpoint flush 仍只会临时覆写 `headerversion` 后恢复，但实例级 writer `verbose` 不会桥接成底层 `VisMF::verbose`，后者继续主要命中 `Read/Check/RemoveFiles` 日志路径。

- [x] 2026-05-21：继续收口 `amrex.abort_on_unused_inputs`
  - 已补清这条参数的双 consumer 边界：WarpX 在 step 1 后的 `checkEarlyUnusedParams()` 只会调用 `ParmParse::QueryUnusedInputs()` 做更早的 unused-input 打印提示，不会因这条开关提前 abort。
  - 已补清它和 `amrex.parmparse.verbose` 的更细 early/final 合同：`QueryUnusedInputs()` 与 `ParmParse::Finalize()` 都复用同一套 `IOProcessor() + unused_table_entries_q(g_table) + ParmParse::Verbose()` 判定，因此若 step 1 后 unused entries 仍在且 `amrex.parmparse.verbose` 打开，当前实现会在 early check 与 finalize 两个阶段各打印一次 `Unused ParmParse Variables` 明细；但真正读取 `amrex::system::abort_on_unused_inputs` 并决定是否 `Abort("ERROR: unused ParmParse variables.")` 的仍只有 `Finalize()`。
  - 已再补清这组 unused-input companion 的 lazy-cache 边界：`ParmParse::Verbose()` 首次命中时才把 `amrex.parmparse.verbose` materialize 到内部 `pp_detail::verbose`，若缺省还会把回退值反写进 parser table；在同一次运行里若没有显式 `ParmParse::SetVerbose(...)`，单纯再改 parser table 已不会影响 step-1 early check 与 finalize 的明细打印 gate，直到 `Finalize()` 末尾把缓存重置回 `-1`。

- [x] 2026-05-21：继续补入 `amrex.parmparse.verbose`
  - 已把这条参数从 `abort_on_unused_inputs` 的 companion 提升成正式总表条目：当前真实 parser 入口不在 `AMReX.cpp` 初始化主链，而是在 `ParmParse::Verbose()` 首次命中时才构造 `ParmParse("amrex.parmparse")` 读取 `verbose` 或别名 `v`。
  - 已补清它自己的 runtime/lifecycle 边界：缺省时源码会把回退值反写进 parser table；之后同一次运行里只有显式 `ParmParse::SetVerbose(...)` 才会改写当前缓存 gate，而 `Finalize()` 末尾又会把 `pp_detail::verbose` 重置回 `-1`，供下一次初始化重新 materialize。

- [x] 2026-05-23：继续收口 `warpx.verbose`
  - 已再补清这条参数的 `main.cpp` lifecycle 边界：源码会在 `WarpX::Finalize()` 之前先缓存 `const auto is_warpx_verbose = warpx.Verbose()`，后面只用这份缓存决定是否打印 `Total Time`，因此这条 gate 不会反过来包住 finalize 前后的其它 teardown 输出。
  - 已再补清它和 startup/teardown 输出的反向边界：`WriteUsedInputsFile()` 的提示继续固定走 `write_used_inputs_file(..., true)`，step-1 unused-input 明细仍受 `amrex.parmparse.verbose` 控制，而 `PrintGlobalWarnings("FIRST STEP")` 与 `PrintGlobalWarnings("THE END")` 继续是无条件 warning 汇总路径，不受 `warpx.verbose` gate 约束。

- [x] 2026-05-23：继续收口 `amr.restart`
  - 已再补清这条参数的 restart/startup 时序边界：restart 路径当前固定经过 `InitFromCheckpoint() -> PrintDtDxDyDz() -> PostRestart() -> reduced_diags->InitData()`，而 `WriteUsedInputsFile()` 仍会在任何 `afterInitatRestart` callback 和 restart 首帧 diagnostics 补写之前无条件执行，所以它不会因为 restart 而延后到补写之后。
  - 已再补清它的 reduced-diag / HybridPIC 反向边界：`ReducedDiags` 的 `m_write_header = IsNotRestart || !FileExists(...)` 会在对象构造期就由 `amr.restart` 判定，先于 `write_diagnostics_on_restart`；同时 `HybridPICInitializeRhoJandB()` 在 restart 时会跳过 fresh-run 的 `HybridPICDepositRhoAndJ()` 和 `t=0` split-`B` 注入，直接复用 checkpoint 恢复出的 `rho/current/B` 状态，只把它们复制进 `*_temp` multifabs。

- [x] 2026-05-23：继续收口 `warpx.write_diagnostics_on_restart`
  - 已再补清这条参数的 callback 时序边界：restart 首帧补写发生在 `afterInitatRestart` 之后，但仍处于 step-loop 外，因此不会触发主循环里的 `afterdiagnostics` callback。
  - 已再补清它的 writer-side 结果边界：full diagnostics 仍用 `istep[0]-1` 过 interval gate，而 reduced-diag 文本 writer 会把 step 列写成 `step+1 = istep[0]`、时间列继续直接取 `gett_new(0)`；同时 `BoundaryScrapingDiagnostics` 即便被遍历到，也会在 `n_particles == 0` 时静默 `return`，不会因为 restart 首帧补写而强行生成空输出目录。

- [x] 2026-05-23：继续收口 `warpx.quantum_xi`
  - 已再补清这条参数的 solver-dispatch 边界：它不会因为在 `WarpX::ReadParameters()` 中 materialize 成 `m_quantum_xi_c2` 就自动参与所有场推进；当前只有 `WarpXEvolve.cpp` 在 `electromagnetic_solver_id == PSATD` 且 `use_hybrid_QED` 为真时，才会真正调度 `Hybrid_QED_Push(dt)` 去消费它。
  - 已再补清它的运行时命中方式：当前实现不是单次修正，而是在 `PushPSATD()` 前后各执行一次 `Hybrid_QED_Push()`；同时 `Hybrid_QED_Push()` 入口还会硬要求 `grid_type == Collocated`，而真正被这条系数直接回写的仍只有 `Ex/Ey/Ez`，`B/J` 继续只是输入态。

- [x] 2026-05-23：继续收口 `warpx.use_hybrid_QED`
  - 已再补清这条参数的 solver/dispatch 边界：它只有在 `WarpXEvolve.cpp` 的 PSATD 主场推进分支里才会被真正消费；非 PSATD 分支不会因为打开 `use_hybrid_QED` 而自动 materialize 任何 Hybrid-QED 修正。
  - 已再补清它的 synchronization 反向边界：一旦走这条 `use_hybrid_QED` 分支，PSATD 普通路径末尾那组 `FillBoundaryB/F/G(ng_afterPushPSATD...)` 收尾就不会再执行，而是改成 `pre-PSATD` 和 `post-PSATD` 两次 `Hybrid_QED_Push()`，并在第二次修正后只补 `FillBoundaryE(...)`；同时 `Hybrid_QED_Push()` 自身还会硬要求 `grid_type == Collocated`。

- [x] 2026-05-21：继续收口 `warpx.abort_on_warning_threshold`
  - 已补清这条参数的 startup 顺序边界：`initialize_warning_manager()` 会先执行 `test_warnings` 注入，之后才解析并设置 `abort_on_warning_threshold`，因此 synthetic input warnings 不受这条 threshold 约束，也不会因它触发即时 abort。
  - 已补清它的更细 runtime/输入合法性边界：真正设置 threshold 之后录入的 warnings 才会在 `RecordWarning(...)` 里按 `low/medium/high` 映射触发 `ABLASTR_ALWAYS_ASSERT_WITH_MESSAGE`；而且源码会先 `record_msg(...)` 把 warning 记入 logger、再立刻 abort，所以命中阈值的 warning 已被记账，但通常来不及再走后续 local/global summary printer。与此同时，非法 threshold 字符串不会拖到运行期，而是在 startup 里直接 `WARPX_ABORT_WITH_MESSAGE`。

- [x] 2026-05-23：继续收口 `warpx.abort_on_warning_threshold`
  - 已再补清这条参数的严格阈值比较边界：`WarnManager::RecordWarning(...)` 实际检查的是 `msg_priority < abort_priority`，不是 `<=`；因此 `threshold=low` 会在 `low/medium/high` 三档 warning 上全部 abort，`threshold=medium` 会在 `medium/high` abort，而 `threshold=high` 只会在 `high` abort。
  - 已再补清它的 rank-local abort 边界：源码会先 `record_msg(...)` 记入 logger，再在单个 rank 本地命中阈值时立刻 `ABLASTR_ALWAYS_ASSERT_WITH_MESSAGE(...)` 终止，因此通常来不及再走后续 `PrintLocalWarnings()/PrintGlobalWarnings()` 汇总，也不会等到 IO-rank 聚合后再统一决定。

- [x] 2026-05-24：继续收口 `warpx.break_signals`
  - 已再补清这条参数的 signal-latency 边界：`SignalHandling::CheckSignals()` 只在每步开头读取并清空 rank-0 的 `signal_received_flags[...]`，因此若 signal 晚于这次轮询到达，当前实现会把它留到下一次 `CheckSignals()` 才 materialize，而不是在本步中途立刻触发 break。
  - 已再补清它的 loop-exit / flush 次序边界：`SIGNAL_REQUESTS_BREAK` 不在 `HandleSignals()` 里消费，而是要等到步尾 `checkStopSimulation()` 才设置 `m_exit_loop_due_to_interrupt_signal`，因此当前 step 仍会继续跑完；真正的 forced flush 与 `onbreaksignal` 也不在 `HandleSignals()`，而是在跳出主 loop 之后统一走 `FilterComputePackFlushLastTimestep(...)` 和 callback 收尾。

- [x] 2026-05-24：继续收口 `warpx.checkpoint_signals`
  - 已再补清这条参数的 signal-latency / step-end 次序边界：它和 `break_signals` 一样，也只会在每步开头 `CheckSignals()` 时 materialize；真正消费则发生在步尾 `HandleSignals()`，而且早于 step-end verbose 输出。
  - 已再补清它与 `break_signals` 的共存边界：若同一个 signal 同时配置进 `checkpoint_signals` 和 `break_signals`，当前实现会先在 `HandleSignals()` 里执行一次 `FilterComputePackFlushLastTimestep(...)` 与 `oncheckpointsignal`，随后同一步再因 break 退出 loop，并在 loop 后因为 `m_exit_loop_due_to_interrupt_signal` 再统一 forced-flush 一次。

- [x] 2026-05-24：继续收口 `amrex.memory_log`
  - 已再补清这条参数的实例生命周期边界：`memory_log_name` 不是 `MemProfiler` 实例成员，而是 `MemProfiler::report()` 里的函数静态缓存，因此 `MemProfiler::Finalize()` 当前只会 `reset()` `the_instance`，不会清空这份文件名 sink。
  - 已再补清它的复用后果：同一进程后续即便重新 materialize 新的 `MemProfiler` 实例，下一次 `report(prefix)` 也仍会继续复用旧的 `amrex.memory_log` 输出目标，而不是重新 query 输入。

- [x] 2026-05-24：继续收口 `amrex.max_gpu_streams`
  - 已再补清这条参数的 finalize/re-init 边界：`initialize_gpu()` 只有在 `gpu_stream_pool.size() != max_gpu_streams` 时才重建 pool 容器，而 `Finalize()` 当前只销毁底层 stream 和清空 `gpu_stream_index`，不会把 `max_gpu_streams` 或 pool 尺寸回滚到默认值。
  - 已再补清它的复用后果：同一进程后续若再次初始化且这条值没变，源码会直接复用现有同尺寸 pool 槽位重新创建 stream，而不是重新 query 输入或先重建 pool 形状。

- [x] 2026-05-24：继续收口 `amrex.use_gpu_aware_mpi`
  - 已再补清这条参数的 comms-arena 生命周期边界：`AMReX_Arena.cpp` 里 comms arena 的 device-vs-pinned 选型一旦在 arena 初始化时 materialize 成全局 `the_comms_arena` 指针，后续 `The_Comms_Arena()` 只会直接返回这根现成指针，不会重新检查 `UseGpuAwareMpi()`。
  - 已再补清它的运行时后果：同一进程里单纯之后再改 parser 表或布尔值，不会自动把当前 comms arena 从 device 切回 pinned，或反向切换；真正 consumer 仍只会继续沿既有 `the_comms_arena` 指针分配通信缓冲区。

- [x] 2026-05-24：继续收口 `amrex.omp_threads`
  - 已再补清这条参数的 `OpenMP::Initialize()` 生命周期边界：源码入口先检查内部 `initialized` 计数，第一次之外的后续调用只会 `++initialized` 后直接返回，不会再次 `queryAdd("omp_threads", ...)` 或重跑 `system/nosmt/正整数` 三分支。
  - 已再补清它和 runtime setter 的组合后果：同一进程里单纯把 parser 表改成 `"system"` 或 `"nosmt"`，不会重新 materialize 当前线程策略；当前仍只有整数 setter 会立刻调用 `amrex::OpenMP::set_num_threads(...)` 改线程数。

- [x] 2026-05-21：继续收口 `warpx.always_warn_immediately`
  - 已补清这条参数的初始化顺序边界：`initialize_warning_manager()` 会先注入 `test_warnings`，之后才设置 `always_warn_immediately`，因此 synthetic input warnings 不受这条开关控制。
  - 已补清它的更细 logger/abort 反向边界：`RecordWarning(...)` 即便已经当场 `amrex::Warning(...)`，后面仍会继续 `record_msg(...)` 进入 logger，所以本地/全局 warning 汇总不会被关闭；而且这条即时 warning 发生在 threshold 检查之前，因此即便同一条 warning 随后立刻触发 abort、来不及走 summary printer，前面的即时 warning 行也已经发出。相对地真正被这条参数改变的还包括 `abort_on_warning_threshold` 命中时 abort 文本是否重复附带 `[topic] text`。

- [x] 2026-05-21：继续收口 `warpx.limit_verbose_step`
  - 已补清这条参数在 `WarpXEvolve.cpp` 里的真实 gate：它不只控制 `STEP starts/ends`、`updating timestep` 和 wall-clock 输出，还会把同一个 `verbose_step` 布尔值继续传给 `doResampling(..., verbose_step)`。
  - 已补清它的更细 runtime 反向边界：`PhysicalParticleContainer::resample(...)` 里这个布尔值只决定是否打印 “Resampled ...” 信息，并不会改写 `m_resampler.triggered(...)` 条件或算法本身；同时 Python callbacks、diagnostics 调度、signal 处理和停机判断都不读取 `verbose_step`，因此这条开关只节流日志，不降低这些路径的执行频率。

- [x] 2026-05-21：继续收口 `amr.plot_headerversion / checkpoint_headerversion`
  - 已补清这组输入在 AMReX `Amr` writer 里的真实生效方式：plotfile/checkpoint 写盘前都会先暂存并临时覆写全局 `VisMF::currentVersion`，写完后再恢复，因此它们不是永久改写进程级默认 header version。
  - 已补清它们的更细 writer-side 恢复边界：`checkpoint_headerversion` 只控制 `VisMF` header version，而本地 `Amr` checkpoint 路径会先缓存旧的 `FArrayBox::Format`、临时 `setFormat(FAB_NATIVE)`、写完后再恢复，所以这条输入既不决定 payload format，也不会把 native checkpoint 格式泄漏成后续 writer 的新默认值；相对地 WarpX diagnostics 的 `FlushFormatPlotfile/Checkpoint` 仍各自固定覆写 `Version_v1` / `NoFabHeader_v1`，不继承这组 `amr.*` 输入。

- [x] 2026-05-21：继续收口 `amrex.use_profiler_syncs`
  - 已补清这条输入的真实初始化链：它不是 WarpX 自己的 startup 开关，而是 AMReX `BLProfileSync::InitParams()` 在 BL/Tiny profiling 初始化宏链里读取的全局标志。
  - 已补清它和 profiling 模式的更细初始化非对称性：`BL_PROFILING` 构建会通过 `BL_PROFILE_INITPARAMS()` 在 AMReX 初始化中段触发 `BLProfiler::InitParams(); BLProfileSync::InitParams()`，而 `AMREX_TINY_PROFILING` 构建则让 `BL_PROFILE_INITPARAMS()` 退化为空、改由初始化末尾的 `BL_TINY_PROFILE_INITIALIZE()` 触发 `TinyProfiler::Initialize(); BLProfileSync::InitParams()`；两者不是并行双调用。与此同时，只有在 `BL_PROFILING` 或 `AMREX_TINY_PROFILING` 打开时，`BL_PROFILE_SYNC_START_TIMED/STOP` 宏才会真正展开成 `BLProfileSync::*`，而真实 barrier 仍只会在 `sync_counter == 0` 的最外层 `SyncBeforeComms:*` region 上执行一次。
  - 已再补清它的 sync-counter 初始化边界：`BLProfileSync::InitParams()` 每次不只读取 `use_profiler_syncs`，还会显式把 `sync_counter = 0`；同时带名字的 `StartSyncRegion(name)` 只有在最外层 region 才会同时创建 `BL_PROFILE(name)` 计时器并执行 barrier，因此这条参数控制的是最外层 timed sync region，而不是每次宏展开都重复计时。

- [x] 2026-05-21：继续收口 `reduced_diags.intervals`
  - 已补清这条参数的主 loop 预判边界：`ReducedDiags::DoDiags(step)` 不只控制 reduced-diag 自身 interval 命中，还会并进 `WarpXEvolve.cpp` 的 `do_diagnostic`，从而继续影响 `synchronize_velocity_for_diagnostics` 时本步是否需要额外做速度同步。
  - 已补清它的更细运行期分叉：即便 `DoDiags(step)` 为假，只要 `m_plot_rd != 0`，主 step-loop 仍会每步调用 `LoadBalance/ComputeDiags/WriteToFile`，因此 interval 约束真正落在各 reduced diag 自己的内部 gate；其中 `DifferentialLuminosity{,2D}` 与 `FieldProbe(integrate)` 会继续每步累计 device/粒子态，只在命中 interval 时才回流 host/MPI 或抽取输出，而 `LoadBalanceCosts::WriteToFile()` 还会用 `nextContains(step+1)` 判断是否补一行 `NaN`。

- [x] 2026-05-21：继续收口 `warpx.safe_guard_cells`
  - 已补清这条参数在主域通信里的真实放大范围：safe 模式会把 `FillBoundaryF/G`、`E_avg/B_avg`、moving-window `shiftMF(...)` 等路径退回 full-`nGrowVect()` helper 通信，并在 `WarpXEvolve.cpp` 里追加部分 safe-only 的 post-step `FillBoundaryF/E/B(...)`。
  - 已补清它的更细 helper/direct 反向边界：`FillBoundaryE/B` 只有在 `do_single_precision_comms` 分支里才显式把 `nghost` 抬到 `nGrowVect()`，若 `do_single_precision_comms == false` 则仍直接走 AMReX `FillBoundary_nowait/finish` 或 `FillBoundaryAndSync...`；与此同时 `pml->FillBoundary(...)` / `pml_rz->FillBoundary*()` 的调度本身也不是这条参数直接开关。
  - 已再补清它的 moving-window 对照边界：`shiftMF(...)` 在非 safe 模式下会专门重构只在窗口方向取 `abs(num_shift)`、其余方向取 `1` 的 `ng_mw`，再限制到不超过已分配 guard cells；safe 模式则跳过这层收缩，固定对 `tmpmf` 走 full-`nGrowVect()` helper。

- [x] 2026-05-21：继续收口 `ablastr.fillboundary_always_sync`
  - 已补清这条输入的真实命中范围：它会把所有走 `ablastr::utils::communication::FillBoundary(MultiFab...)` 的 nodal `MultiFab` 通信抬成 `FillBoundaryAndSync(...)`，包括无 `ng` 重载、vector 包装和 mixed-precision 临时副本路径。
  - 已再补清它的 helper 内部边界：single-precision 路径会按 `mf.nGrowVect()` 分配并 full-copy 临时副本，但真正 `FillBoundary{AndSync}` 仍只消费调用方 `ng`；同时 `Vector<MultiFab*>` 包装会逐个元素重进 helper，因此 `ParmParse("ablastr").query(...)` 也是按元素重复执行，而不是整组只判一次。
  - 已补清它的更细绕过边界：同文件里的 `iMultiFab` 重载仍直接 `imf.FillBoundary(...)`，而源码里大量 direct `mf.FillBoundary(...)` 与 `pml->FillBoundary(...)` 也完全不经过这条 helper，因此它不是所有 `FillBoundary` 调用的统一总开关。

- [x] 2026-05-21：继续收口 `warpx.serialize_initial_conditions`
  - 已补清它的前端桥接：Python PICMI 会通过 `warpx_serialize_initial_conditions` 读入，并在 `initialize_inputs()` 中写回 `pywarpx.warpx.serialize_initial_conditions`；WarpX C++ 侧仍保留旧别名 `warpx.serialize_ics` 的硬拒绝。
  - 已补清它的更细编译期/后端边界：当前唯一 consumer 仍是 `AddParticles.cpp` 里 `AddPlasma()` 的 `#pragma omp parallel if (...)`，而这条 `#pragma` 只会在 `AMREX_USE_OMP && !AMREX_USE_GPU` 下 materialize；因此 GPU build 或无 OMP build 连这层串行化 gate 都不会生效。
- [x] 2026-05-21：继续收口 `particles.do_tiling`
  - 已补清它和 `serialize_initial_conditions` 的更细共同执行边界：在 `AddParticles.cpp::AddPlasma()` 里，`MFItInfo::EnableTiling(tile_size)` 先建立 tile 分解，后面的 `#pragma omp parallel if (...)` 才决定是否并行遍历；因此 `serialize_initial_conditions` 只会关闭 OMP，并不会把已经建立好的 tiled `MFIter` 回退成 untiled 版本。
  - 已补清它的更细命名反向边界：本地唯一 consumer 是 `PhysicalParticleContainer::AddPlasma()` 里 `prepare(...)` 之后的 OMP gate，因此同一条串行化开关不只影响 `initial_injection`，也会影响 moving-window `continuous injection` 的 CPU/OpenMP 粒子创建循环。
  - 已补清它和 `do_dynamic_scheduling / serialize_initial_conditions` 的更细共同执行边界：在 `AddPlasma()` 与 `MultiParticleContainer::getMFItInfo(...)` 里，源码顺序都是先 `EnableTiling(...)`、再固定 `SetDynamic(true)`、最后才进入 OMP gate；因此这三条参数当前只是共用同一个 `MFItInfo`/OMP 外壳，其中 `do_tiling` 只管 tile 分解，`do_dynamic_scheduling` 只稳定控制 `WarpXParIter` 默认调度，`serialize_initial_conditions` 只关闭创建期 OMP。
- [x] 2026-05-21：继续收口 `warpx.do_dynamic_scheduling`
  - 已补清它的更细 `WarpXParIter` / 创建路径反向边界：这条全局开关会进入 `WarpXParIter(...).SetDynamic(WarpX::do_dynamic_scheduling)`，因此稳定控制的是走 `WarpXParIter` 的粒子 tile 迭代默认调度策略；但 `AddParticles.cpp` 的 `AddPlasma()` 与另一条 level-0 粒子创建 loop、以及 `MultiParticleContainer.H::getMFItInfo(...)` 的多 species helper，在 OMP 路径下都直接写死 `info.SetDynamic(true)`，并不继承这条参数。
  - 已补清它和 `particles.do_tiling / warpx.serialize_initial_conditions` 的更细共同执行边界：在 `AddPlasma()` 与 `getMFItInfo(...)` 里，源码都是先 `EnableTiling(...)`、再 `SetDynamic(true)`、最后才进入 OMP gate；因此这三条参数当前只是共用同一个 `MFItInfo`/OMP 外壳，而不是一个统一并行开关的三个别名，其中 `do_tiling` 管 tile 分解，`do_dynamic_scheduling` 只稳定控制 `WarpXParIter` 默认调度，`serialize_initial_conditions` 只关闭创建期 OMP。
- [x] 2026-05-21：继续收口 `warpx.serialize_initial_conditions`
  - 已补清它和 `particles.do_tiling / warpx.do_dynamic_scheduling` 的更细共同执行边界：`AddPlasma()` 里这条参数命中的只是最后一层 `#pragma omp parallel if (...)`，而在此之前同一路径已经先 `EnableTiling(tile_size)`、再固定 `info.SetDynamic(true)`；同时 `MultiParticleContainer::getMFItInfo(...)` 也会先建 tiling、再固定 dynamic，并根本不读取这条参数。因此它当前只稳定控制“是否再套 OMP”，不会回退 tiling，也不会改写 dynamic scheduling。

- [x] 2026-05-21：继续收口 `reduced_diags.path`
  - 已补清这条参数的根目录职责：基类构造期只会在 `IOProcessor` 上显式创建 `m_path`，并用 `m_path + m_rd_name + "." + m_extension` 管理文本 reduced-diag 的 `FileExists/m_write_header` 与主文件落点。
  - 已补清它的更细分流边界：`ParticleHistogram2D / DifferentialLuminosity2D` 虽然实际写到 `m_path + m_rd_name + "/" + filename`，但本地源码里没有单独 `UtilCreateDirectory(m_path + m_rd_name, ...)` 的预建步骤，而是直接把最终 series 路径交给 `io::Series(..., CREATE)`。

- [x] 2026-05-21：继续收口 `reduced_diags.extension`
  - 已补清这条参数在文本 reduced-diag 路径里的真实命名合同：基类构造期会显式预创建 `m_path + m_rd_name + "." + m_extension` 并据此决定 `m_write_header`，而 `LoadBalanceCosts` 还会额外派生 `.tmp.<extension>` 做末步补 `NaN` 后的原地替换。
  - 已补清它的更细分流边界：`ParticleHistogram2D / DifferentialLuminosity2D` 不只忽略这条后缀、改走 `openpmd_%0NT.<backend>`，而且不会先显式创建 `m_path + m_rd_name` 子目录，只是把最终路径直接交给 `io::Series(..., CREATE)`。

- [x] 2026-05-21：继续收口 `reduced_diags.separator`
  - 已补清这条参数的大部分 writer-side consumer 都按完整 `m_sep` 输出：基类 `ReducedDiags::WriteToFile()`、`FieldProbe` 以及大量文本型 reduced diags 的 header/data 列都继续复用完整字符串分隔符。
  - 已补清它的更细不对称边界：`LoadBalanceCosts` 在末步补 `NaN` 的再解析链里只用 `m_sep[0]` 和 `peek()==m_sep[0]` 重拆列，因此多字符 separator 当前并不是严格对称的读写合同；而 `ParticleHistogram2D / DifferentialLuminosity2D` 的 openPMD 路径又完全不消费这条参数。

- [x] 2026-05-21：继续收口 `reduced_diags.precision`
  - 已补清这条参数的真实命中范围：`ReducedDiags::WriteToFile()` 会把全局或实例级 `precision` 传给时间列与 `m_data` 数值列，但当前 reduced-diag 树里真正读取 `m_precision` 的 `WriteToFile()` 只剩基类这一处。
  - 已补清它的 writer-side 反向边界：step 列是在 `setprecision(m_precision)` 之前写出的，header 链也不读取这条参数；与此同时 `LoadBalanceCosts` 与 `FieldProbe` 两条自定义文本 writer 都直接写死 `std::setprecision(14)`，而 `ParticleHistogram2D / DifferentialLuminosity2D` 完全走 openPMD mesh，因此这条参数现在只能稳定控制命中基类文本 writer 的时间/数值列格式。

- [x] 2026-05-21：继续收口 `warpx.do_electrostatic`
  - 已补清这条参数的 solver 互斥与选型边界：它不只在 `WarpX::ReadParameters()` 中把 `electromagnetic_solver_id` 切成 `None`，还会继续触发 RCYLINDER/RSPHERE、FFT Poisson、open boundary 和 `labframe-electromagnetostatic` 相邻兼容性检查，并据枚举实例化 `LabFrameExplicitES / EffectivePotentialES / RelativisticExplicitES` 三类 electrostatic solver。
  - 已补清它的更细运行期与 diagnostics 合同：`WarpXEvolve.cpp` 会在每步末尾分派到 `ComputeSpaceChargeField(reset_fields=true)`，其中 `labframe-electromagnetostatic` 还会额外调用 `ComputeMagnetostaticField()`；`ComputeDt()`、`phi/A` diagnostics 和粒子上 `phi` 输出也都继续受这条模式收紧。

- [x] 2026-05-21：继续收口 `algo.evolve_scheme`
  - 已补清这条参数的总分派边界：它不只在 `WarpX::ReadParameters()` 中读取枚举名，还会立刻决定是否实例化 `SemiImplicitEM / ThetaImplicitEM / StrangImplicitSpectralEM` 这类 `m_implicit_solver`；随后 `WarpXEvolve.cpp::OneStep()` 会先按该指针把总推进入口分成 implicit solver 整步委托和显式 PIC 主链两大类。
  - 已补清它的更细相邻合同：这条参数还继续改写 `dt_update_interval` / `use_filter` / mirrors 的兼容性边界，并让 `GuardCellManager` 在 implicit 路线下改用只按粒子位移估算的 `J/rho` guard-cell 预算，而不是 explicit 电磁路线里的 `c*dt` 扩张合同。

- [x] 2026-05-21：继续收口 `warpx.random_seed`
  - 已补清这条参数的默认值与 seed-bridge 语义：`WarpX::ReadParameters()` 的 `"default"` 不是显式写入某个整数，而是保持 AMReX 现有默认 seed 链；而 `ablastr::math::set_random_seed(...)` 会对 `"random"` 和正整数两条输入分别派生不同的 `cpu_seed/gpu_seed` 并统一调用 `amrex::ResetRandomSeed(...)`。
  - 已补清它的更细 consumer：这套全局随机源会继续被 `InjectorPosition/InjectorMomentum`、`DefaultInitialization.H` 的 QED optical-depth 初值，以及 `QuantumSync/BreitWheeler` wrappers 等所有 `RandomEngine` 路径共同消费。

- [x] 2026-05-21：继续收口 `warpx.boost_direction`
  - 已补清这条参数的解析与硬限制：`ReadBoostedFrameParameters()` 会把 `x/y/z` 转成 `boost_direction` 三分量单位向量，未知字符串直接 abort，而当前实现还会立刻把 boost 硬限制为 `z`。
  - 已补清它的更细 direction-vector consumer：`WarpXMovingWindow.cpp` 会按不同维度索引映射把 boosted-frame 注入位移投影到对应方向，`LaserParticleContainer.cpp` 会要求激光传播方向与 `boost_direction` 对齐并按 `beta_boost * boost_direction * c * dt` 回推天线位置，而 `Diagnostics.cpp` / `BTDiagnostics.cpp` 又分别把它作为 moving-window 坐标修正和 BTD 仅支持 `z` 向 boost 的硬 gate。

- [x] 2026-05-21：继续收口 `warpx.gamma_boost`
  - 已补清这条参数的主解析边界：`ReadBoostedFrameParameters()` 才是唯一主入口，只有 `gamma_boost > 1` 时才继续派生 `beta_boost` 并强制要求给出 `boost_direction`；`WarpX.cpp` 里再次 `query("gamma_boost", ...)` 的那层语义已重新钉死为 `psatd.use_default_v_galilean/comoving` companion 的 gating consumer。
  - 已补清它的更细 runtime chain：`WarpXMovingWindow.cpp` 会用它把窗口与注入速度变换到 boosted frame，而 `WarpXFluidContainer.cpp` 与 `LatticeElementFinder.cpp` 又会继续用它把 `z/t`、外加场评估点和 lattice 对齐坐标变回 lab frame。

- [x] 2026-05-21：继续收口 `stop_time`
  - 已补清这条参数的默认值与主 loop 边界：`WarpX` 内部默认其实是 `std::numeric_limits<amrex::Real>::max()`，而在 boosted-frame 文档语义下这里指的是 boosted frame 时间；`WarpXEvolve.cpp` 主 step-loop 直接把它和 `max_step` 并列作为 stop criterion。
  - 已补清它的更细 runtime/rewrite chain：`end_of_step_loop`、`final_time_step` 和 `checkStopSimulation(cur_time)` 都会继续复用同一时间上界，决定 diagnostics 同步、最终 flush 和 break；同时 `BTDiagnostics::DerivedInitData()` 也可能为补足最后一个 BTD snapshot 而反向上调全局 `stop_time`。

- [x] 2026-05-21：继续收口 `max_step`
  - 已补清这条参数的默认值与主 loop 边界：`WarpX` 内部默认并不是空值，而是 `std::numeric_limits<int>::max()`；`WarpX::Evolve(numsteps)` 又会先把它和调用侧 `numsteps` 合并成局部 `numsteps_max`，并与 `stop_time` 一起形成真实 step-loop 条件。
  - 已补清它的更细 runtime/rewrite chain：`istep[0] == max_step` 会继续参与 `final_time_step` 判定，决定是否走 `FilterComputePackFlushLastTimestep(...)` 的最终 flush；同时 `BTDiagnostics::DerivedInitData()` 和 boosted-frame `computeMaxStepBoostAccelerator()` 都可能在初始化期反向回写全局 `max_step`。

- [x] 2026-05-21：继续收口 `qed_schwinger.y_size`
  - 已补清这条参数的维度边界：它虽然在 `XZ/RZ` parser 分支里都会被强制读取，但 `doQEDSchwinger()` 会更早对 `RZ` 直接 abort，因此当前真正运行到 consumer 的只剩 `XZ` 路径。
  - 已补清它的更细归一化链：这条值先被乘进 `dV = dx*dz*y_size` 送入 `SchwingerFilterFunc/getSchwingerProductionNumber(...)` 估算单元总 pair 产额，再在 `SchwingerTransformFunc` 里按 `total_weight / N / y_size` 除回到每个新生成电子/正电子的宏粒子权重。

- [x] 2026-05-21：继续收口 `warpx.quantum_xi`
  - 已补清这条参数在输入侧和内部缓存的量纲边界：输入文件给的是 `quantum_xi`，而 `WarpX` 内部真正保存的是乘上 `c^2` 后的 `m_quantum_xi_c2`。
  - 已补清它的更细 field-push consumer：同一系数会被 `Hybrid_QED_Push(lev, PatchType::fine/coarse, dt)` 在 fine/coarse patch 上统一复用，并在每个 tile 内先复制成局部 `xi_c2`；`WarpX_QED_Field_Pushers.cpp` 又会先为 `E` 三个分量分配并填充 `tmpEx/tmpEy/tmpEz`，随后只沿 `tmpE -> Ex/Ey/Ez` 这条链传播修正。`Bx/By/Bz` 和 `Jx/Jy/Jz` 只作为公式输入参与，不会被它直接覆写。

- [x] 2026-05-21：继续收口 `warpx.use_hybrid_QED`
  - 已补清这条参数当前不是通用 Maxwell 修正选项，而是只在 `electromagnetic_solver_id == PSATD` 的场推进分支里生效；非 PSATD 分支根本不消费它。
  - 已补清它的更细 runtime chain：`WarpXEvolve.cpp` 会把 `Hybrid_QED_Push(dt)` 插成 `PushPSATD(...)` 前后两次独立修正，并改写后续 `FillBoundaryE/B(...)` 同步；`WarpX_QED_Field_Pushers.cpp` 则继续对 fine patch 恒定执行、在 `lev>0` 时追加 coarse patch 分支，固定从 `Efield_fp/Bfield_fp/current_fp` 或 `Efield_cp/Bfield_cp/current_cp` 取数后调用 `warpx_hybrid_QED_push(...)` kernel，而不是走 `aux` 场视图。

- [x] 2026-05-21：继续收口 `<reduced_diags_name>.value_function/filter_function(t,x,y,z,ux,uy,uz,w)`
  - 已补清这组 `ParticleHistogram2D` parser hook 的非对称可选性：`filter_function` 虽会被预先编译，但运行时仍受 `m_do_parser_filter` gate 保护，确实只在显式给出时参与粒子级 early-return。
  - 已补清 `value_function` 的真实边界：它虽然在构造期也通过 `query(...)` 读取，但 `ComputeDiags()` 会无条件 `compileParser(m_parser_value.get())` 并直接调用，当前没有安全默认回退到 `weight = w` 或 `1` 的分支；同时 writer 只把 `function_abscissa / function_ordinate / filter` 写回 openPMD 元数据，不会记录 `value_function` 表达式。
  - 已再补清这组参数的更细 runtime/write 非对称：`m_do_parser_value` 在构造后基本失活，后续运行链不再读取；相对地 `WriteToFile()` 会无条件写出 `filter` attribute，因此即便用户未显式给 `filter_function`，输出 metadata 里也仍会保留一个 `filter` 字段，而 `value_function` 仍始终不会进入 metadata。

- [x] 2026-05-21：继续收口 `<reduced_diags_name>.species`
  - 已补清这条参数在 reduced-diag 内部并不存在统一 parser/consumer，而是按类型分流：`ParticleHistogram / ParticleHistogram2D` 会在构造期把名字映射成固定 species index，未命中立即 abort；`ColliderRelevant / DifferentialLuminosity / DifferentialLuminosity2D` 则共享 `GetParticleContainerFromName(...)` 这条双束解析链，对未知名字直接 assert。
  - 已补清它的失败模式反向边界：`BeamRelevant` 只在运行期遍历 `GetSpeciesNames()` 按名字筛选目标束流，不会在构造期校验 species 是否真实存在，因此错名时当前实现会静默跳过所有 species，最终退化成零数据输出，而不是立即报错。

- [x] 2026-05-21：补齐 `amr.plot_headerversion / checkpoint_headerversion`
  - 已确认这组参数此前还是总表缺口；本轮已正式入表，而不再只零散出现在 `Readme.io` 和相邻 `vismf.headerversion` 说明中。
  - 已补清它们的真实边界：parser/默认值属于同级 AMReX `Amr` 层，默认都为 `Version_v1 (1)`；consumer 则分别是常规 plotfile/checkpoint 写盘前的 `VisMF::SetHeaderVersion(plot_headerversion/checkpoint_headerversion)`，同时与 WarpX diagnostics writer 自己的临时 header-version 覆写形成反向边界。

- [x] 2026-05-21：继续收口 `vismf.groupsets / setbuf / checkfilepositions / usepersistentifstreams / usesynchronousreads`
  - 已补清这组参数在写侧的真实 consumer 仍是 `NFilesIter` 与 `pubsetbuf(...)` 缓冲合同，而不是 WarpX diagnostics instance-local parser。
  - 已把读侧继续压实到 `VisMF::OpenStream/CloseStream/DeleteStream` 的 persistent input-stream 生命周期，以及只在 `noFabHeader && ngrow==0` 这类专门快路径里才生效的 `useSynchronousReads` 同步读取分支；WarpX 本地邻接边界则钉死在 `InitFromCheckpoint()` 和 `PML::Restart()` 的 `VisMF::Read(...)` 恢复链。

- [x] 2026-05-21：继续收口 `particles.nreaders / nparts_per_read / datadigits_read / use_prepost`
  - 已补清这组参数在 WarpX 本地真正邻接的是 `InitFromCheckpoint() -> mypc->Restart(...) -> pc->Restart(...) -> PostRestart()` 这条粒子 restart 恢复链，而不是 diagnostics instance-local parser。
  - 已补清它们在 AMReX 粒子层的真实边界：`nreaders` 会被截成 `min(NProcs, nreaders)` 且要求正值，`nparts_per_read` 也要求正值，`datadigits_read` 在 `ParticleContainer::Restart()` 入口读取，而 `use_prepost` 是更底层的 MPI I/O pre/post 聚合优化开关。

- [x] 2026-05-21：补齐 `psatd.use_default_v_comoving`
  - 已确认这条参数此前还是总表缺口；本轮已正式入表，而不再只作为 `psatd.v_comoving` 说明里的 companion。
  - 已补清它的真实边界：入口在 `WarpX::ReadParameters()`，只有 boosted-frame 且设置 `warpx.gamma_boost` 时才允许为真；命中后源码不会再读取手动 `psatd.v_comoving`，而是直接生成 `m_v_comoving[2] = -sqrt(1-1/gamma_boost^2)`，再继续进入后续 `PhysConst::c` 缩放和 `v_galilean/update_with_rho` 兼容性检查。

- [x] 2026-05-21：继续收口 `psatd.update_with_rho`
  - 已补清这条参数在 `WarpX::ReadParameters()` 里不只按 standard/Galilean/comoving/RZ 路径推默认值，还会继续对 `do_dive_cleaning`、comoving PSATD 和非常规 `JRhom` 时间依赖施加必须为真的反向实现边界。
  - 已补清它的 runtime consumer：这条开关会直接影响 PSATD 下 `rho_fp/rho_cp` 的分量分配，并在 `WarpXEvolve.cpp` 中决定是否真实进入 `DepositCharge -> SyncRho -> PSATDForwardTransformRho` 链；下游 `PsatdAlgorithmGalilean` 与 `PsatdAlgorithmJRhomSecondOrder` 也会据此在 `E(J, rho)` 和 `E(J)` 两条更新公式间分流。

- [x] 2026-05-21：继续收口 `psatd.do_time_averaging`
  - 已补清这条参数的 solver-side 约束：它在 `WarpX::ReadParameters()` 之后，不只继续受 `psatd.solution_type=first-order` 禁止，还会在 `PsatdAlgorithmGalilean` 和 `PsatdAlgorithmJRhomSecondOrder` 这两条 time-averaged 路径里隐含要求 `update_with_rho=1`，并真实驱动 `Ex_avg...Bz_avg` 频谱分量的累积。
  - 已补清它的 runtime consumer：`WarpX.cpp` 会为 `fp/cp` 分配 `Efield_avg/Bfield_avg`，并在 level 0 把 `Efield_aux/Bfield_aux` alias 到 `*_avg_fp`；`WarpXEvolve.cpp` 则会追加 `FillBoundaryE_avg/B_avg`、在 `OneStep_JRhom()` 下把沉积循环扩成 `2*n_deposit`，最后走 `PSATDScaleAverageFields(...) + PSATDBackwardTransformEBavg(...)`。

- [x] 2026-05-21：继续收口 `psatd.v_comoving`
  - 已补清这条参数在 `WarpX::ReadParameters()` 里不只读取 `queryArrWithParser(...)` 数组，还会在 `psatd.use_default_v_comoving=1` 且设置 `warpx.gamma_boost` 时自动生成 boosted-frame 默认值；随后源码会统一乘以 `PhysConst::c`，所以输入数组本身也是以 `c` 为单位的无量纲速度。
  - 已补清它的 runtime consumer：这条速度会继续排除 `v_galilean`、`Esirkepov/Villasenor`、非常规 `J/rho` 时间依赖组合，并强制 `psatd.update_with_rho=1`；下游则真实进入 `SpectralSolver.cpp` 中对 `PsatdAlgorithmComoving` 的优先分派，以及 `GuardCellManager` 对 comoving/Galilean 共用的额外 guard-cell 预算。

- [x] 2026-05-21：继续收口 `psatd.v_galilean`
  - 已补清这条参数在 `WarpX::ReadParameters()` 里不只读取 `queryArrWithParser(...)` 数组，还会在 `psatd.use_default_v_galilean=1` 且设置 `warpx.gamma_boost` 时自动生成 boosted-frame 默认值；随后源码会统一乘以 `PhysConst::c`，所以输入数组本身是以 `c` 为单位的无量纲速度。
  - 已补清它的 runtime consumer：这条速度会继续排除 `v_comoving`、`Esirkepov/Villasenor/Vay`、`JRhom` 和非常规 `J/rho` 时间依赖组合，并把 Galilean/comoving 路径下 `update_with_rho` 的默认值抬成 `true`；下游则真实进入 `SpectralSolver{,RZ}` 的 `PsatdAlgorithmGalilean{,RZ}` 分派、`GuardCellManager` 的额外 guard-cell 预算，以及 `WarpXMovingWindow` 和 `WarpX::LowerCorner/UpperCorner()` 共享的 Galilean boundary shift。

- [x] 2026-05-21：继续收口 `psatd.JRhom`
  - 已补清这条参数在 `WarpX::ReadParameters()` 里不只读取字符串，而是会把它拆成 `time_dependency_J`、`time_dependency_rho` 和 `m_JRhom_subintervals` 三层语义；非法时间依赖字符或缺少整数后缀都会直接 abort。
  - 已补清它的 runtime consumer：这条模式会继续排除 `Vay`、Galilean/comoving、`current_correction` 和部分非常规时间依赖组合，并让谱求解器按 `subintervals` 缩小 `solver_dt`、在 `SpectralSolver.cpp` 中分派到 `PsatdAlgorithmJRhomFirstOrder/SecondOrder`，同时把主推进入口改写成 `OneStep_JRhom()` 的专用多次 `J/rho` 沉积循环。

- [x] 2026-05-21：继续收口 `psatd.current_correction`
  - 已补清这条参数在 `WarpX::ReadParameters()` 里不只简单读取，而是会先因 `Esirkepov/Villasenor/Vay`、`do_dive_cleaning` 或 `JRhom` 把默认值改写为关闭，并继续对 `Vay` 与非常规 `J/rho` 时间依赖施加反向实现边界；若用户关闭它且又未使用 charge-conserving deposition，源码还会发 low-priority warning。
  - 已补清它的 runtime consumer：这条开关会影响 PSATD 下 `rho_fp` 的分量数和 `m_fill_guards_current` 的 backward-FFT guard-cell 预算，并在 `WarpXEvolve.cpp -> WarpXPushFieldsEM.cpp` 中真实进入 `PSATDCurrentCorrection(...) -> SpectralSolver::CurrentCorrection()` 调用链，随后再做 `SyncCurrent/SyncRho`。

- [x] 2026-05-21：继续收口 `algo.maxwell_solver`
  - 已补清这条参数在 `WarpX::ReadParameters()` 里读成 `electromagnetic_solver_id` 后，不只会继续施加 `ECT` 需要 runtime EB、`CKC` 的几何限制、`PSATD` 的 FFT/维度限制，以及 `StrangImplicitSpectralEM` 必须配 `psatd` 这类构造期硬边界。
  - 已补清它的 runtime consumer：这条枚举会继续改写相邻 `grid_type/current_deposition` 的默认与合法性，在 `ComputeDt()` 中分叉 `HybridPIC / None / PSATD / Yee / CKC / ECT` 的时间步策略，在 `AllocLevelMFs()` 中把场求解器分流到 `SpectralSolver` 或 `FiniteDifferenceSolver`，并在 openPMD 中写成 `fieldSolver = Yee / CK / PSATD / other` 元数据。

- [x] 2026-05-21：继续收口 `algo.particle_pusher`
  - 已补清这条参数在 `WarpX::ReadParameters()` 里读成全局 `particle_pusher_algo` 后，不只在 implicit/semi-implicit evolve scheme 下限制为 `Boris/HigueraCary`，还会继续与 classical radiation reaction、`collisions.split_momentum_push` 形成额外反向边界。
  - 已补清它的 runtime consumer：`PushSelector.H` 与 `PhysicalParticleContainer.cpp` / `RigidInjectedParticleContainer.cpp` 会按该枚举分派到 `UpdateMomentumBoris / Vay / HigueraCary`，并在 RR 打开时把 Boris 再细分成 `UpdateMomentumBorisWithRadiationReaction(...)` 分支；同时 openPMD 会写出 `particlePush = Boris / Vay / HigueraCary` 元数据。

- [x] 2026-05-21：继续收口 `algo.current_deposition`
  - 已补清这条参数在 `WarpX::ReadParameters()` 里不只读取枚举，还会先按 `PSATD / HybridPIC / electrostatic` 把默认值改写成 `Direct`，再继续对 `do_current_centering`、`Vay`、`JRhom`、`current_correction`、Galilean/comoving PSATD、`periodic_single_box_fft` 和 implicit/semi-implicit evolve scheme 施加反向兼容性限制。
  - 已补清它的 runtime consumer：`Vay` 会额外分配 `current_fp_vay` 并改变 PSATD 下 `SyncCurrent()` 的同步字段；`WarpXParticleContainer.cpp` 最终按该枚举分派到 `Esirkepov / Villasenor / Vay / Direct` 沉积 kernel，而 `PhysicalParticleContainer::DepositTemperature()` 还会反向要求它必须是 `Direct`。
  - 已继续补清更细的 runtime chain：`PushParticlesandDeposit()` 在 `do_current_centering=0` 且枚举为 `Vay` 时会把默认沉积目标字段从 `current_fp` 切到 `current_fp_vay`，并继续改写 PSATD 下周期单盒 FFT 与非单盒 FFT 两条 `SyncCurrent()/ApplyFilterMF(...)` 路径；同时 shared-memory current deposition 分支会在 kernel 入口直接拒绝 `Esirkepov / Villasenor / Vay`，把可用算法收缩成 direct-only。

- [x] 2026-05-21：继续收口 `algo.charge_deposition`
  - 已补清这条参数在 `WarpX::ReadParameters()` 里虽然通过 `query_enum_sloppy("charge_deposition", ...)` 读取，但当前 `WarpXAlgorithmSelection.H` 中只暴露 `ChargeDepositionAlgo::Standard`，`WarpXInitData.cpp` 的启动期回显也只显式识别这一值。
  - 已补清它的真实 runtime 分叉不来自多种命名 charge 算法，而是来自 `do_shared_mem_charge_deposition`：`WarpXParticleContainer::DepositCharge(...)` 会在常规 charge kernel 与 `DenseBins -> tboxes -> max_tbox_size -> doChargeDepositionSharedShapeN<...>` 的 shared-memory 路径之间切换。
  - 已补清 shared charge deposition 的实现边界与上游 consumer：shared 分支要求 `depos_lev` 只能是 `lev/lev-1`、粒子 shape 必须放进 tile/guard cells，并显式拒绝 implicit push；`PhysicalParticleContainer.cpp` 与 `WarpXEvolve.cpp` 则继续把它接到 `rho_fp/rho_buf` 的 coarse-buffer 沉积与后续 coarse-level 汇总路径。

- [x] 2026-05-21：继续收口 `<diag_name>.file_prefix`
  - 已补清这条参数不是所有 flush backend 都把它当成真实持久化路径：plotfile/checkpoint/openPMD 与 BTD plotfile 会继续把它扩成输出目录、snapshot 路径和 buffer 子树，而 `BoundaryScrapingDiagnostics` 还会额外在后面追加 `/particles_at_<boundary>`。
  - 已补清 in-situ 反向边界：`FlushFormatAscent` 与 `FlushFormatSensei` 当前只把 `Concatenate(prefix, iteration[0], file_min_digits)` 当作日志或 bridge update 的名字语义，不对应本地持久化目录；`FlushFormatCatalyst::WriteToFile()` 更直接把 `prefix` 标成 `ignore_unused(...)`，运行 pipeline 时完全旁路这条输入。

- [x] 2026-05-21：继续收口 `<diag_name>.format`
  - 已补清 `checkpoint` 的合同不只停留在 `raw_specified=false && checkpoint_compatibility=true`：`Diagnostics::InitData()` 与 `InitDataAfterRestart()` 还会继续强制 `write_species=1`，因为 restart checkpoint 必须保留粒子状态。
  - 已补清更细的 backend 反向边界：`Ascent/Sensei` 仍会消费一部分通用 writer 语义，而 `FlushFormatCatalyst::WriteToFile()` 当前会把 `prefix/file_min_digits/plot_raw_fields/plot_raw_fields_guards/verbose` 整体旁路，只真正消费 Blueprint mesh/particle channels 与 Catalyst 脚本配置。

- [x] 2026-05-21：继续收口 `<diag_name>.verbose`
  - 已补清实例级 `m_verbose` 的真实 writer-side consumer：`Plotfile/OpenPMD/Checkpoint/Sensei/Ascent` 都会在 `verbose > 0` 时打印对应 writer 信息，而 `FullDiagnostics` 的 time-averaged 分支还会在 `m_verbose > 1` 时额外打印 averaging-period 信息。
  - 已补清 `Catalyst` 的更细反向边界：它不消费实例级 `verbose`，但也不是完全静默，而是会无条件打印固定的 `Running Catalyst pipeline scripts...` 提示。

- [x] 2026-05-21：继续收口 `<diag_name>.fields_to_plot`
  - 已补清 full diagnostics 的 backend-specific 分叉：在 RZ 几何下只要 `format=openpmd`，`FullDiagnostics::InitializeFieldFunctors()` 就会直接跳到 `InitializeFieldFunctorsRZopenPMD()`，随后把请求到的 `E/B/J/rho` 基字段强制扩成全-mode 输出。
  - 已补清 BTD 的更细反向边界：若 `fields_to_plot` 在解析/重写后得到空 `m_varnames`，源码会直接把 `m_do_back_transformed_fields = false`，后续 `BackTransformFunctor` 与 `m_cell_center_functors` 的 field-side 初始化链随之停用。

- [x] 2026-05-21：继续收口 `<diag_name>.particle_fields_to_plot`
  - 已补清这条参数不只是在 `FullDiagnostics` 中按 `particle_fields_to_plot × particle_fields_species × level` 构造 `ParticleReductionFunctor`，还会在 `Diagnostics::BaseReadParameters()` 里强制读取每个 `<field>(x,y,z,ux,uy,uz)` parser，并记录对应的 `.do_average` 与 `.filter(...)` 设置。
  - 已补清 `ParticleReductionFunctor` 的真实归约链：运行时先按 species 索引选中真实 `ParticleContainer`，再对 `(x,y,z,ux/c,uy/c,uz/c)` 求 map/filter parser，并按粒子权重做 cell 级原子累加；若 `.do_average=1`，源码还会额外构造同 filter 的权重计数场，把 weighted sum 除成 weighted average，空 cell 结果强制置零。

- [x] 2026-05-21：继续收口 `algo.field_gathering`
  - 已补清这条参数在 `WarpX::ReadParameters()` 里不只会在 `grid_type=hybrid` 时把默认值改写成 `MomentumConserving`，还会在 hybrid grid 上拒绝其它显式 gather 选择，并继续强制 `galerkin_interpolation = false`。
  - 已补清它的反向兼容性与 consumer：`PSATD + mesh refinement` 和 implicit/semi-implicit evolve scheme 都会继续限制 `MomentumConserving`；同时它还决定 `field_centering_nox/noy/noz` 是否真正读取、`aux_is_nodal`/auxiliary-field nodal 路径是否开启，并会在 openPMD 中写成 `particleInterpolation = energyConserving / momentumConserving` 元数据。

- [x] 2026-05-21：继续收口 `warpx.do_current_centering`
  - 已补清这条参数不只限制 `grid_type=hybrid` 且 `maxLevel()==0`，还会继续反向限制部分 current deposition 算法，否则要求改成 `warpx.do_current_centering = 0` 或 `algo.current_deposition = direct`。
  - 已补清开关打开后会额外分配 nodal `current_fp_nodal`，把沉积目标字段名切到 `current_fp_nodal`，随后在 `SyncCurrent()` 中按 `current_centering_nox/noy/noz` 和对应 stencil coefficients 做 nodal-to-staggered centering，并扩大 J deposition guard cells。

- [x] 2026-05-21：继续收口 `warpx.grid_type`
  - 已补清这条参数在构造期就会改写默认值：`collocated` 直接关闭 `galerkin_interpolation`，`hybrid` 会预设 field/current centering 相关默认值；cylindrical/spherical 几何禁止 `hybrid`。
  - 已补清 `RZ + PSATD` 会强制把 `grid_type` 覆写成 `collocated`，并继续决定 `field_centering_*` 是否真正读取、`do_current_centering=1` 是否合法、FDTD solver 走 `CartesianNodal` 还是 `Yee/CKC` 路径，以及 auxiliary patch 是新建 nodal 场还是 alias 到平均场。

- [x] 2026-05-21：继续收口 `warpx.sort_particles_for_deposition`
  - 已补清这条参数在 `sort_intervals.contains(step+1)` 命中后如何把排序分成 deposition-aware `pc->SortParticlesForDeposition(sort_idx_type)` 和普通 `pc->SortParticlesByBin(bin_size)` 两条路径。
  - 已补清 species-level 反向边界：当 `sort_particles_for_deposition=1` 时，`do_not_deposit` 容器会被直接跳过，连 deposition-aware sorting 本身也不会执行；而普通 bin sort 路径不会做这层过滤。

- [x] 2026-05-21：继续收口 `warpx.do_shared_mem_charge_deposition` 的 launch 边界
  - 已补清 `ChargeDeposition.H` 中 shared charge kernel 的 block 内线程数不是用户参数，而是固定 `threads_per_block = 256`，再按 `nblocks = a_bins.numBins()` 与 `shared_mem_bytes` 调 `amrex::launch(...)`。
  - 这样 current/charge 两条 shared 路径的分工已经更清楚：`shared_mem_current_tpb` 只作用于 current shared kernel，不影响 charge shared deposition。

- [x] 2026-05-21：继续收口 `warpx.shared_mem_current_tpb`
  - 已把这条参数压到更精确的 current shared kernel launch 边界：`CurrentDeposition(...)` shared 分支会先把它写成 `threads_per_block`，再继续下传给 `doDepositionSharedShapeN<...>`。
  - 已补清 `CurrentDeposition.H` 中最终按 `nblocks = a_bins.numBins()`、`threads_per_block`、`shared_mem_bytes` 调 `amrex::launch(...)`；因此它决定的是每个 shared bin 的 block 内线程数，而不是 shared-memory 字节大小，也不参与 charge deposition。

- [x] 2026-05-21：继续收口 `warpx.shared_tilesize`
  - 已把这条参数压到 current/charge 两条 shared-memory 沉积路径的共同 consumer：在 `CurrentDeposition(...)` 中，它先作为 `bin_size` 驱动 `DenseBins` 分桶、`numTilesInBox(...)`、`getTileIndex(...)` 和 `getMaxTboxAlongDim(...)`，随后连同 `max_tbox_size` 一起传给 `doDepositionSharedShapeN<...>`。
  - 已补清 `DepositCharge(...)` 中同一条值也会继续驱动 `DenseBins`、`tboxes/max_tbox_size` 以及 `doChargeDepositionSharedShapeN<...>`；因此它是 shared-memory 分桶几何的共同输入，而不只是“调 tile 大小”的泛化参数。

- [x] 2026-05-21：继续收口 `warpx.do_shared_mem_current_deposition`
  - 已把这条参数压到更精确的 `CurrentDeposition(...)` shared 分支：先按 `shared_tilesize` 做 `DenseBins` 分桶并计算 `max_tbox_size`，再按 shape 分派到 `doDepositionSharedShapeN<1/2/3/4>(..., threads_per_block, bin_size)`。
  - 已补清 shared current deposition 的实现边界：只允许 `CUDA/HIP` 且非 `RCYLINDER/RSPHERE`，并在进入 shared 分支后继续拒绝 implicit push、`Esirkepov / Villasenor / Vay`；同时 `PhysicalParticleContainer::DepositTemperature()` 也会因 `do_shared_mem_current_deposition=1` 直接 abort。

- [x] 2026-05-21：继续收口 `warpx.do_shared_mem_charge_deposition`
  - 已把这条参数从“shared-memory 沉积优化族成员”压到 `WarpXParticleContainer::DepositCharge(...)` 的真实 runtime chain：命中后不再走常规电荷沉积，而是先检查 `depos_lev`、空粒子早退、粒子 shape 与 CPU/GPU guard-cell 约束。
  - 已补清 shared-memory 分支内部会以 `shared_tilesize` 做 `DenseBins` 分桶、构造 `tboxes/max_tbox_size`，再按粒子 shape 分派到 `doChargeDepositionSharedShapeN<1/2/3/4>(...)`；CPU 路径结束后还会把局部 `local_rho` 通过 `lockAdd(...)` 累加回全局 `rho`。

- [x] 2026-05-21：继续收口 `warpx.sort_idx_type / warpx.sort_bin_size`
  - 已把 `sort_idx_type` 压到更精确的分派边界：只有 `sort_intervals.contains(step+1)` 命中、并且 `sort_particles_for_deposition=1` 且容器不是 `do_not_deposit` 时，它才会继续下放到 AMReX `PermutationForDeposition(..., idx_type)`。
  - 已把 `sort_bin_size` 压到更精确的普通分桶边界：它只在 `sort_particles_for_deposition=0` 时才会进入 AMReX `ParticleContainer::SortParticlesByBin(bin_size)`；底层还存在 `bin_size == IntVect::TheZeroVector()` 直接早退的反向边界，其余情况下再通过 `numTilesInBox(..., bin_size)` 和 `GetParticleBin{..., bin_size, ...}` 构造真实 bin 映射。

- [x] 2026-05-21：继续收口 `warpx.override_sync_intervals / warpx.sort_intervals`
  - 已把 `override_sync_intervals` 从“直接影响 coarse-fine `rho/J/E/B` 同步时序”的过强摘要收紧到当前本地源码可证实的边界：`WarpX::ReadParameters()` 解析、旧名 `override_sync_int` 的 renamed 兼容断言、以及保存为 `WarpX` 成员状态；截至当前 sibling `warpx/Source` 检索，尚未看到进一步 runtime consumer。
  - 已把 `sort_intervals` 压到更精确的 step-loop gate：默认值先按 CPU/GPU 平台分流，再在 `HandleParticlesAtBoundaries(...)` 的 `if (sort_intervals.contains(step+1))` 分支里触发排序，并继续下放到 deposition-aware `SortParticlesForDeposition(sort_idx_type)` 或普通 `SortParticlesByBin(bin_size)` 两条实现。

本文件按 `docs/warpx-full-code-reading-book-plan.md` 维护。早期 `manuscript/` v0.1 只保留为粗草稿，不再作为正式书稿质量标准；后续目标是从物理过程、完整推导、数值算法到 WarpX 全源码逐行/逐块精读。

## 当前基线

- 最新推进（2026-05-23）：继续清 startup / AMReX 相邻 still-coarse 条目，已把 `amrex.memory_log` 补成正式总表条目：这条输入当前不是普通“内存日志文件名”，而是 `MemProfiler::report()` 里的静态缓存输出 sink。源码里它只在首次命中时 `queryAdd("memory_log", ...)`，后续 report 都复用这份缓存；`AMReX.cpp` 收尾时会固定 `MemProfiler::report("Final")` 再 `MemProfiler::Finalize()`，而真正写文件的只有 IO rank，并且始终以 append 方式往同一个文件追加跨 rank 汇总表。相对地，文件若打不开，当前实现只会静默 `return`，不会额外报错。
- 最新推进（2026-05-23）：继续清 startup / AMReX 相邻 still-coarse 条目，已把 `amrex.max_gpu_streams` 补成正式总表条目：这条输入当前不是“永远开这么多 GPU stream”的静态数字，而是 device 初始化时 stream pool 的被钳制上限。源码里它会先 `queryAdd(...)`，再被 `AMREX_GPU_MAX_STREAMS` 和下限 `1` 双向钳制；随后 `initialize_gpu()` 按这个值创建/重建 `gpu_stream_pool`，`setStreamIndex(idx)` 也按 `idx % max_gpu_streams` 做线程到 stream 的轮转。与此同时，若当前处在 `inSingleStreamRegion()` 或 `usingExternalStream()`，`numGpuStreams()` 会强制退回 `1`，因此这条参数控制的是普通 GPU stream pool 的最大并发度，而不是所有代码区域都会一直暴露同样多的 stream。
- 最新推进（2026-05-24）：继续清 startup / moving-window 相邻 still-coarse 条目，已把 `warpx.end_moving_window_step` 从偏泛的“moving-window 活动区间上界”再压一层时序边界：`MoveWindow()` 的 active gate 用的是严格 `< end_moving_window_step`，因此 `step == end_moving_window_step` 这一轮会先打印 stopping 消息，但同一步并不会再执行窗口位移。换句话说，它是“宣布停止”的那一步，而不是“最后一次仍然移动”的那一步。
- 最新推进（2026-05-24）：继续清 startup / moving-window 相邻 still-coarse 条目，已把 `warpx.do_moving_window` 从偏泛的“moving-window 参数族展开 + runtime gate”再压一层运行期边界：即便 `moving_window_active(step)` 已经为真，`WarpXMovingWindow.cpp::MoveWindow()` 在更新连续 `moving_window_x` 后仍会先算 `num_shift_base`；只要它还是 `0`，函数就直接 early-return，不会真正 `ResetProbDomain(...)` 或 shift 网格。因此 `do_moving_window=1` 不等于每个 active step 都一定发生离散窗口位移。
- 最新推进（2026-05-24）：继续清 startup / geometry 相邻 still-coarse 条目，已把 `geometry.is_periodic` 从偏泛的“边界一致性 + geometry 初始化 + runtime gate”再压一层 parser/runtime 分工：这条内部键虽然会在 startup 被 `addarr("is_periodic", ...)` 回写给 `geometry` parser，但 `WarpX::MakeWarpX()` 后续自己的 runtime policy 已经不再直接读这条 parser 键，而是统一转成消费 `Geom(...).isPeriodic()/periodicity()` 这份已建好的几何态。
- 最新推进（2026-05-24）：继续清 startup / geometry 相邻 still-coarse 条目，已把 `geometry.prob_lo/hi` 从偏泛的“startup 数值化 + boost 改写”再压一层 parser/geometry 状态边界：这组键会先在 `parse_geometry_input()` 里 `addarr(...)` 一次，若开启 boosted frame 又会在 `ConvertLabParamsToBoost()` 里第二次 `addarr(...)` 覆盖同名键，因此后续 reader 看到的已经是数值化后、必要时再经 boost/moving-window 缩放的 parser 表结果。更下游像 `WarpX.cpp` 的 RZ solver 检查则已经只看 `Geom(0).ProbLo(0)` 这样的几何态，而不再回头看原始输入文本。
- 最新推进（2026-05-24）：继续清 startup / geometry 相邻 still-coarse 条目，已把 `geometry.dims` 从偏泛的“启动一致性断言 + geometry 摘要打印输入”再压一层时序边界：`check_dims()` 只负责前置 hard gate，不会把编译维度反写回 parser，也不会给缺失值自动补默认；因此后续 `WarpXInitData.cpp` 的 `query("dims", ...)` 在 successful runs 里当前只剩只读 pretty-print 语义，而不再承担新的合法性检查。
- 最新推进（2026-05-24）：继续清 startup / AMR 相邻 still-coarse 条目，已把 `amr.ref_ratio / amr.ref_ratio_vect` 从偏泛的“moving-window / PML / PEC / dt 共享 refinement ratio 输入”再压一层 consumer 不对称边界：同一份 `IntVect` 当前既会被 `PML.cpp`、`WarpX_PEC.cpp`、plotfile writer 这些几何/输出路径完整保留，也会在 `WarpXComputeDt.cpp` 的 subcycling 回推里被压缩成单个 `refRatio(lev)[0]` 去定义 coarse-level `dt` 比例。换句话说，几何 consumer 仍是整向量语义，而时间步 consumer 目前仍是单分量语义。
- 最新推进（2026-05-24）：继续清 startup / AMR 相邻 still-coarse 条目，已把 `amr.max_level` 从偏泛的“多处局部 consumer 共享的 AMR 层数输入”再压一层 reader 分叉：多数 reduced-diag 构造函数仍会直接 `query("max_level", ...)`，用 parser snapshot 先决定 header 与容器按 level 的展开；但 `ReducedDiags/Timestep.cpp` 运行时已经不再回头读 parser，而是直接取 `WarpX::GetInstance().maxLevel()` 决定 `dt[lev]` 的循环范围。因此这条参数当前同时落在“构造期 parser snapshot”与“运行期已建好 AmrCore 状态”两类 reader 上。
- 最新推进（2026-05-24）：继续清 startup / AMR 相邻 still-coarse 条目，已把 `amr.n_cell` 从偏泛的“最粗层网格尺寸 + RZ-PSATD gridding consumer”再压一层 parser-table 边界：`WarpXAMReXInit.cpp::parse_geometry_input()` 会先把 `n_cell` 表达式 `remove` 后再 `addarr(...)` 回 `ParmParse("amr")`，因此后续本地 `getarr("n_cell", ...)` consumer 实际看到的已经是数值化后的整数数组，而不是原始表达式文本。随后 `CheckGriddingForRZSpectral()` 才继续用这份结果强制重建 `blocking_factor_x/y` 与 `max_grid_size_x/y`。
- 最新推进（2026-05-24）：继续清 startup / AMReX 相邻 still-coarse 条目，已把 `amrex.abort_on_out_of_gpu_memory` 从偏泛的“managed-memory 预检 gate”再压一层 lifecycle 边界：`AMReX_Arena.cpp::Arena::Initialize()` 会把这条输入 `queryAdd(...)` 进 arena 全局状态，后续同一 arena 生命周期内普通分配路径都只复用缓存后的布尔值，不会反复重读 parser；直到 `Arena::Finalize()` 把 `initialized` 置回 `false`，下一次初始化才可能重新 materialize。与此同时，它当前直接命中的仍只有 managed-memory free-memory 预检，纯 device-memory 分支继续旁路这条早期 gate。
- 最新推进（2026-05-24）：继续清 startup / AMReX 相邻 still-coarse 条目，已把 `amrex.the_arena_is_managed` 从偏泛的“主 arena managed-vs-device 分叉”再压一层 lifecycle 边界：`AMReX_Arena.cpp` 初始化时会把这条输入一次性 materialize 成全局 `the_arena` / `The_Arena()` 指针，后续默认 `ArenaAllocator` 与 `Gpu::DeviceVector` 都只复用这根现成指针，不会重新 query 去切换默认 arena 形态。与此同时，`AMReX_GpuAllocators.H` 里的 `PolymorphicArenaWrapper` 也补清了 finalize 后反向边界：`Arena::Finalize()` 之后 cached pointer 变 stale 时，它会退回 `The_Null_Arena()`，而不是继续沿旧默认 arena 指针运行。
- 最新推进（2026-05-23）：继续清 startup / AMReX 相邻 still-coarse 条目，已把 `amrex.use_gpu_aware_mpi` 补成正式总表条目：这条输入当前不只是静态“系统是否支持 GPU-aware MPI”的标签，而是 MPI 扩展探测、parser 覆写、通信 arena 选型与部分通信 staging 回退的组合 gate。`ParallelDescriptor::Initialize()` 会先按 `MPIX_Query_*`/`MPIX_GPU_query_support(...)` 探测 `use_gpu_aware_mpi` 初值，再允许 `ParmParse("amrex").queryAdd(...)` 覆写；随后 `AMReX_Arena.cpp` 会据此把 `The_Comms_Arena()` 切成 device 或 pinned host，而 `FabArrayComm` 某些目标在 device arena 且 `!UseGpuAwareMpi()` 的 broadcast 路径还会额外走 `Pinned_Arena` 的 `dtoh -> MPI -> htod` staging 回退。
- 最新推进（2026-05-23）：继续清 startup / AMReX 相邻 still-coarse 条目，已把 `amrex.omp_threads` 从“WarpX startup 覆写默认值 + Python 暴露 setter”的摘要压到更精确的 OpenMP 初始化边界：AMReX `OpenMP::Initialize()` 会把这条输入分成 `system / nosmt / 正整数` 三条路径，其中 `nosmt` 只有在环境变量 `OMP_NUM_THREADS` 没设时才会回落到 `numUniquePhysicalCores()`，若 `OMP_NUM_THREADS` 已设则只打印保留提示；正整数则直接无视 `OMP_NUM_THREADS` 调 `omp_set_num_threads(num)`。同时也补清了 WarpX Python setter 的反向边界：给整数才会立刻 `amrex::OpenMP::set_num_threads(...)`，给 `"system"` 或 `"nosmt"` 只会改 parser 表，不会在当前进程里重跑 `OpenMP::Initialize()`。
- 最新推进（2026-05-23）：继续清 startup / AMReX 相邻 still-coarse 条目，已把 `amrex.abort_on_out_of_gpu_memory` 从“WarpX startup 把默认值改成 `true`”的摘要压到更精确的 arena/runtime 边界：这条输入除了在 `WarpXAMReXInit.cpp` 中把 AMReX 文档默认的 `false` 覆写成 WarpX 默认 `true`，还会在 `AMReX_Arena.cpp` 的 GPU 分配链里作为一个更窄的预检 gate 生效。源码里只有当前 `arena_info.device_use_managed_memory` 为真时，它才会在 `freeMemAvailable() + freeUnused_protected()` 仍不足的情况下提前触发 `out_of_memory_abort("GPU memory", ...)`；若已经走纯 device-memory 分支，这条开关并不参与前面的预检，代码仍会先尝试 `cudaMalloc/hipMalloc/sycl::aligned_alloc_device`，失败后再统一走 `GPU device memory` 的 abort 路径。
- 最新推进（2026-05-23）：继续清 startup / AMReX 相邻 still-coarse 条目，已把 `amrex.the_arena_is_managed` 从“WarpX startup 覆写 AMReX 默认值”的摘要压到更精确的 arena/runtime 分叉边界：`WarpXAMReXInit.cpp` 里这条输入仍先把 AMReX 文档默认的 `true` 覆写成 WarpX 默认 `false`，但 `AMReX_Arena.cpp` 初始化时还会继续用它真正决定 `The_Arena` 是建成 managed 还是 device `CArena`，并把 TinyProfiler memory 表中的主条目标成 `Managed Memory` 或 `Device Memory`。同时 `AMReX_GpuAllocators.H` / `AMReX_GpuContainers.H` 也补清了默认容器 consumer：`Gpu::DeviceVector` 会经 `ArenaAllocator -> The_Arena()` 命中这条主分叉；相对地显式使用 `ManagedVector` 或 `NonManagedDeviceVector` 的专用容器不受它控制。
- 最新推进（2026-05-23）：继续清 startup / profiling 相邻 still-coarse 条目，已把 `tiny_profiler.print_threshold` 补成正式总表条目，补清这条不是计时采样 gate，而是最终 wall-time profiling 报表里 “Other” 聚合裁剪的专门后处理阈值：只有 `PrintStats()` 会真正消费它，且仅在 `print_threshold > 0` 时按 inclusive time 逆序扫描 `allprocstats`，把累计 `dtinmax * 100 / dt_max` 仍低于阈值的低占比函数折叠进 `Other`；若最终只会并入 1 个函数，源码还会显式撤销聚合，因此它控制的是最终表格裁剪，而不是 runtime 计时或 memory profiling 行为。
- 最新推进（2026-05-23）：继续清 startup / profiling 相邻 still-coarse 条目，已把 `tiny_profiler.verbose` 补成正式总表条目，补清这条不是最终 profiling 报告详细程度的总开关，而是 profiling region 进入/退出即时 trace 的专门 gate：`Initialize()` 既接受 `verbose` 也接受短别名 `v`，`start()/stop()` 为真时会通过 `amrex::Print()` 打印 `TP: Entering/Leaving ...` 并维护 `n_print_tabs` 缩进；与此同时，这些即时消息明确不走 `tiny_profiler.output_file` 文件 sink，而是保留在 I/O process 的即时 stdout 路径。
- 最新推进（2026-05-23）：继续清 startup / profiling 相邻 still-coarse 条目，已把 `tiny_profiler.output_file` 补成正式总表条目，补清这条不是普通“输出文件名”，而是 `get_output_file()` 的一次性缓存输出目标：它只在首次命中时 `query("output_file", ...)`，随后 `Finalize()` 和 `MemoryFinalize()` 都只复用这份缓存；若为空则写 `amrex::OutStream()`，若为 `"/dev/null"` 则两条报告链都静默丢弃，否则 IO rank 会在首次命中时先删除旧文件，后续所有 flush/finalize 再统一按 append 方式写入同一个文件。
- 最新推进（2026-05-23）：继续清 startup / profiling 相邻 still-coarse 条目，已把 `tiny_profiler.memprof_enabled` 再压到更精确的 arena/flush 边界：`MemoryInitialize()` 把它和 `tiny_profiler.enabled` 合并后，`Arena::registerForProfiling()` 会把 `TinyProfiler::RegisterArena(...)` 的返回值直接写进 `m_do_profiling`，因此 `AMReX_Arena.cpp` / `AMReX_CArena.cpp` 后续整条 `memory_alloc/free` 记账分支都不会 materialize。与此同时，无论是 `BL_PROFILE_TINY_FLUSH()` 触发的 `MemoryFinalize(true)`，还是 AMReX 收尾时固定调用的 `MemoryFinalize()`，入口都会先检查 `memprof_enabled`，所以这条 gate 为假时不仅最终 memory report 不会出现，连 flush snapshot 也不会生成。
- 最新推进（2026-05-23）：继续清 startup / profiling 相邻 still-coarse 条目，已把 `tiny_profiler.enabled` 补成正式总表条目，补清这条不是单纯“是否打印 tiny-profiler 报告”，而是 `TinyProfiler::Initialize()` 和 `MemoryInitialize()` 共同读取的总 gate：`start()/stop()/StartRegion()/StopRegion()/Finalize()` 全都会先检查 `enabled`，而 memory profiling 初始化还会立刻做 `memprof_enabled = memprof_enabled && enabled`。因此 `enabled=0` 会同时切断 region 计时、`device_synchronize_around_region` companion、生存期统计输出和 `CArena` memory profiling，相关 companion 不会绕过这条总开关单独生效。
- 最新推进（2026-05-23）：继续清 startup / profiling 相邻 still-coarse 条目，已把 `tiny_profiler.device_synchronize_around_region` 从 `warpx.do_device_synchronize` 的 companion 提升成正式总表条目，补清这条真实 consumer 不在 WarpX 主循环，而在 `AMReX_TinyProfiler.cpp` 的 `TinyProfiler::Initialize()/start()/stop()`：只有在 `tiny_profiler.enabled=1` 且编译打开 `AMREX_USE_GPU` 时，profiling region 的进入和退出两端才会各执行一次 `Gpu::streamSynchronize()` 后再计时。与此同时，也已把它和 WarpX 兼容桥的主从边界钉死：`warpx.do_device_synchronize` 只在 startup 里尝试通过 `queryAdd(...)` 写这条真实参数，若用户已经显式给了 `tiny_profiler.device_synchronize_around_region`，WarpX 只做一致性检查，不再覆写。
- 最新推进（2026-05-23）：继续清 startup / runtime 相邻 still-coarse 条目，已把 `warpx.override_sync_intervals` 从偏泛的“`rho/J/E/B` override 同步节拍”摘要压回本地可证实实现：源码里它仍只在 `WarpX::ReadParameters()` 中被读成实例成员 `utils::parser::IntervalsParser override_sync_intervals`，`WarpX.cpp` 也继续对旧名 `warpx.override_sync_int` 做硬拒绝；但截至当前 sibling `warpx/Source` 本地检索，这个成员没有继续接入 `WarpXEvolve.cpp`、`WarpXComm.cpp`、PML 或其它 source/field 边界同步调度链。因此官方 `parameters.rst` 对它的算法语义当前强于这份本地源码能直接证明的实现接线。
- 最新推进（2026-05-23）：继续清 startup / runtime 相邻 still-coarse 条目，已把 `warpx.do_subcycling` 从偏泛的“粗细层时间步/同步开关”摘要压到更精确的 runtime 总 gate：源码里它除了在 `WarpX::ReadParameters()` 中受 `max_level <= 1` 约束，还会在 `WarpX.cpp` 里被 `PSATD` 直接硬拒绝、在 `OneStep_sub1()` 入口被 electrostatic solver 再次硬拒绝；同时它会继续改写 `ComputeDt()/UpdateDtFromParticleSpeeds()` 的 coarse-dt 回推、boosted-frame `compute_max_step_from_btd` 的 `dt[0]` 选取、`GuardCellManager` 的 `nox+1` 粒子 guard-cell 预算、level-0 `current_store` 分配，以及 AMR 主 step-loop 在 `OneStep_nosub(...)` 和 `OneStep_sub1(...)` 之间的运行时分派。
- 最新推进（2026-05-23）：继续清 startup / runtime 相邻 still-coarse 条目，已把 `warpx.projection_div_cleaner.atol` 从偏泛的“MLMG absolute tolerance”摘要压到更精确的 solver companion 边界：源码里这条值在 `ProjectionDivCleaner::ReadParameters()` 中默认始终是 `0.0`，不像 `rtol` 那样会按 `float/double` 两档精度分叉；同时它既不参与 `setSourceFromField()` 的 `-divB` source 构造，也不参与 `correctField()` 的场回填，而是只在 `runMLMG(...)` 中和 `m_rtol` 一起进入唯一一次 `mlmg.solve(...)`。因此它控制的是 projection div cleaner 求解阶段的绝对停止阈值，而不是 cleaner 是否启用的外层算法 gate。
- 最新推进（2026-05-23）：继续清 startup / runtime 相邻 still-coarse 条目，已把 `warpx.do_initial_div_cleaning` 从偏泛的“初始化时做一次 div clean”摘要压到更精确的默认链和执行时序：源码里它的自动默认只会被“非常量外加 `B` 网格场”触发，不会因外加 `E` 场、粒子外场或常量 `B` 单独打开；同时 `WarpXInitData.cpp` 会在 `WriteUsedInputsFile()` 之后、restart 之外的初始化主链里先执行 `ProjectionCleanDivB()`，而此时被清洗的仍是 `ProjectionDivCleaner("Bfield_fp_external")` 绑定的 staging MultiFab，之后这批外加磁场才会通过 `AddExternalFields()` 并回主 `Bfield_fp`。另外即便这条值为真，`ProjectionCleanDivB()` 内层仍只支持 `Yee`、`HybridPIC` 和 `MLMG` 的静态 LabFrame 电静态组合；不兼容时当前只会 warning，不会切到持续的演化期 `do_divb_cleaning` 链。
- 最新推进（2026-05-21）：继续清 startup / profiling 相邻 still-coarse 条目，已把 `warpx.do_device_synchronize` 从“profiling region 周围是否显式同步 GPU”的摘要压到更精确的 startup/profiling 桥接边界，补清这条输入在 `WarpXAMReXInit.cpp` 里不会直接调用 `Gpu::synchronize()`，而是先按 GPU/CPU 给出默认值，再通过 `queryAdd(...)` 桥接成 `tiny_profiler.device_synchronize_around_region`；同时明确若用户已经显式给了 `tiny_profiler.*`，源码会强制要求它和 `warpx.do_device_synchronize` 一致，否则启动期直接报冲突。
- 最新推进（2026-05-21）：继续清 diagnostics runtime 相邻 still-coarse 条目，已把 `warpx.checkpoint_signals` 从“signal 触发 checkpoint/flush”的摘要压到更精确的运行时边界，补清它虽然和 `break_signals` 一样经过 `SignalHandling::InitSignalHandling()/CheckSignals()/WaitSignals()`，但真正命中后只会在 `WarpX::HandleSignals()` 里触发 `multi_diags->FilterComputePackFlushLastTimestep(...)` 与 `oncheckpointsignal` callback，不会进入 `checkStopSimulation()` 的 `m_exit_loop_due_to_interrupt_signal` 路径，也不会让主推进 loop 提前退出。
- 最新推进（2026-05-21）：继续清 diagnostics runtime 相邻 still-coarse 条目，已把 `diagnostics.diags_names` 从“diagnostics 工厂名字列表”的摘要压到更精确的 signal-checkpoint 邻接边界，补清这张列表除了驱动 `MultiDiagnostics` 的对象分派和初始化遍历，还会被 `WarpX::ReadParameters()` 单独重读，用来检查 `warpx.checkpoint_signals` 是否至少对应一个 `format=checkpoint` 的 diagnostics；同时明确真正收到 checkpoint signal 后，运行时仍只会走 `multi_diags->FilterComputePackFlushLastTimestep(...)` 和 `oncheckpointsignal` callback 这条 full-diagnostics flush 链，而不会额外生成未在列表中的 checkpoint writer。
- 最新推进（2026-05-21）：继续清 diagnostics runtime 相邻 still-coarse 条目，已把 `<diag>.intervals` 从“各 diagnostics 自己解析的输出周期”摘要压到更完整的总调度边界，补清 `MultiDiagnostics::FilterComputePackFlush(step, force_flush, BackTransform)` 会先把 BTD 和非 BTD diagnostics 分成两次遍历，因此这条输入并不是全体 diagnostics 共用一张时间表；同时明确 `FullDiagnostics::DoComputeAndPack()` 对 time-averaged diagnostics 还会在 `in_averaging_period` 为真时绕过单点 `contains(step+1)` 节拍，而 `BoundaryScrapingDiagnostics::DoDump()` 则会在 final-step / signal 的 `force_flush` 路径下显式绕过普通节奏。
- 最新推进（2026-05-21）：继续清 diagnostics runtime 相邻 still-coarse 条目，已把 `<diag>.intervals` 再压到更精确的尾部 forced-flush 反向边界，补清 `FilterComputePackFlushLastTimestep(step)` 不会沿用普通 step-loop 那条 “BTD vs 非 BTD” 双遍历调度，而是只按 `DoDumpLastTimestep()` 逐实例直接下发 `force_flush=true`；随后真正的分叉被延后到各 diagnostics 自己的 `DoComputeAndPack/DoDump`，因此 full diagnostics 会在尾部 forced flush 上重新 `ComputeAndPack()`，boundary scraping 只会强制写出现有 boundary buffer，而 BTD 则只会在 buffer 非空时 flush 已有 lab-frame buffer，不会因为这条 `intervals` 再做新的 back-transform 计算。
- 最新推进（2026-05-21）：继续清 diagnostics manager 入口 still-coarse 条目，已把 `diagnostics.enable / diagnostics.diags_names` 压到更精确的分派边界：补清 `enable=0` 不会阻止 `multi_diags` 对象创建，但会让 ordinary step-loop、tail forced-flush、restart 恢复与 restart 首帧补写这些接口整体退化成空遍历；同时明确 `diags_names` 不只驱动 diagnostics 工厂和 checkpoint-signal 合法性检查，还决定 `InitFromCheckpoint()` 是否走 BTD 专门恢复链、普通 step-loop 中 `FilterComputePackFlush(...)` 的 BTD/non-BTD 双遍历，以及 `FilterComputePackFlushLastTimestep(...)` 的逐实例 forced-flush 单遍历。
- 最新推进（2026-05-21）：继续清 diagnostics manager/runtime 邻接 still-coarse 条目，已把 `<diag>.dump_last_timestep` 再压到更精确的 manager-side 闭包：补清这条尾部 forced-flush 路径遍历的其实是当前已实例化的 `alldiags`，因此它继续受 `diagnostics.enable / diags_names` 约束；若列表为空或所有实例都把 `dump_last_timestep=0`，`FilterComputePackFlushLastTimestep(...)` 会直接空跑，而 `oncheckpointsignal / onbreaksignal` callback 仍会继续执行。
- 最新推进（2026-05-21）：继续清 diagnostics runtime 相邻 still-coarse 条目，已把 `warpx.synchronize_velocity_for_diagnostics` 压到更精确的时序边界：补清 ordinary step-loop 里的 `do_diagnostic` 只看 `multi_diags->DoComputeAndPack(step) || reduced_diags->DoDiags(step)` 这条预判值，不包含稍后 `FilterComputePackFlushLastTimestep(...)` 的尾部 forced-flush；因此 checkpoint signal 在 `HandleSignals()` 里触发的 diagnostics 补写不会于同一步额外补做一次速度同步，而 final timestep 即便 ordinary diagnostics 不活跃，也仍会因 `end_of_step_loop` 为真而先做同步。
- 最新推进（2026-05-21）：继续清 diagnostics manager/runtime 相邻 still-coarse 条目，已把 `diagnostics.enable / diagnostics.diags_names / <diag>.dump_last_timestep / warpx.synchronize_velocity_for_diagnostics` 这组相邻项重新闭合成一条总时序：补清 `diags_names` 不只决定 ordinary step-loop 的 `FilterComputePackFlush(...)` 双遍历和 tail forced-flush 的逐实例单遍历，还会更早通过 `multi_diags->DoComputeAndPack(step)` 进入 `do_diagnostic` 预判，进而影响 `synchronize_velocity_for_diagnostics`；相对地，checkpoint signal 触发的 forced-flush 仍只会落在本步末尾 `HandleSignals()` 里的 `multi_diags` 链，不会反过来补一次新的 velocity synchronization，也不会顺带驱动 reduced diagnostics。
- 最新推进（2026-05-21）：继续清 diagnostics particle-output 相邻 still-coarse 条目，已把 `<diag>.write_species` 从“是否建立粒子 diagnostics”的摘要压到更精确的状态边界，补清 `write_species=0` 会同时清空 per-buffer `m_output_species` 和 `m_output_species_names`，而 `diag_lo/diag_hi` 触发的 reduced-domain 粒子 I/O 禁用只会清空 per-buffer `m_output_species`、不会清空 species 名单本身；因此总表里现在已经明确区分“关闭整个 species 粒子输出状态”和“仅让当前 writer 路径拿不到任何 `ParticleDiag` 实例”这两种不同边界。
- 最新推进（2026-05-21）：继续清 diagnostics particle-output 相邻 still-coarse 条目，已把 `<diag>.write_species` 再压到更精确的 BTD / reduced-domain 反向边界，补清 `BTDiagnostics::DerivedInitData()` 不会简单沿用基类的 species 状态，而是再次读取 `write_species` 并重算 `m_do_back_transformed_particles`；因此即使 `diag_lo/diag_hi` 路径保留了 `m_output_species_names`，只要 `write_species=0`，BTD 也不会重新打开 `SetDoBackTransformedParticles(...)` 粒子链。
- 最新推进（2026-05-21）：继续清 diagnostics particle-field 相邻 still-coarse 条目，已把 `<diag>.particle_fields_species` 从“particle-field species 名单”的摘要压到更精确的展开边界，补清这条列表本身不是独立总开关：即使 parser 已默认回退到全部 species 并完成名字校验，只要 `particle_fields_to_plot` 为空，后续就不会生成任何 `<field>_<species>` 变量名，也不会构造 `ParticleReductionFunctor`；相对地，full diagnostics 真正 consumer 是 `particle_fields_to_plot × particle_fields_species × level` 的三重展开，而 BTD 则会更早在 `particle_fields_to_plot` 上直接硬拒绝整条粒子归约场链。
- 最新推进（2026-05-21）：继续清 diagnostics particle-field 相邻 still-coarse 条目，已把 `<diag>.particle_fields.<field>.filter(...)` 从“粒子归约过滤器”的摘要压到更精确的布尔边界，补清 `ParticleReductionFunctor` 不是按“非零为真”泛化解释这条 parser，而是只把 `filter_fn(...) == 0` 当作剔除条件；因此任意非零返回值都会被视为通过，并且这条同一判据会同时作用于 `red_mf` 分子与 `.do_average=1` 时 `ppc_mf` 分母，保证加权平均两侧共享同一份样本集合。
- 最新推进（2026-05-21）：继续清 diagnostics particle-field 相邻 still-coarse 条目，已把 `<diag>.particle_fields.<field>(...)` 从“粒子归约 map parser”的摘要压到更精确的 functor 形状与 cell 归属边界，补清 `ParticleReductionFunctor` 会强制要求 `mf_src == nullptr` 且 `ncomp == 1`，因此每个 parser 实际只产出单标量 cell field；同时明确粒子归属的输出 cell 不是按 shape deposition 或 gather stencil 决定，而是直接通过 `amrex::getParticleCell(...)` 做 nearest-grid-point cell binning，再把 `w * map_fn(...)` 原子累加到临时 `red_mf`，最后统一 `Coarsen(...)` 到 diagnostics 网格。
- 最新推进（2026-05-21）：继续清 diagnostics particle-field 相邻 still-coarse 条目，已把 `<diag>.particle_fields.<field>.do_average` 从“平均还是累计”的摘要压到更精确的后处理边界，补清 `do_average=1` 时不是在最终 diagnostics 网格或 `Coarsen(...)` 之后再做平均，而是先额外构造 `ppc_mf`，再在细网格 `red_mf` 上按 `MFIter + ParallelFor` 逐 tile、逐 cell 执行 `red_mf /= ppc_mf`；若某个 cell 的分母为零，源码会在这一步直接把 `red_mf` 置零。
- 最新推进（2026-05-21）：继续清 diagnostics particle-field 相邻 still-coarse 条目，已把 `<diag>.particle_fields_to_plot` 从“粒子归约字段列表”的摘要压到更精确的变量表反向边界，补清 `fields_to_plot = none` 只会清空普通字段侧的 `m_varnames_fields`，不会顺带关闭 particle-field diagnostics；源码会先执行 `m_varnames = m_varnames_fields`，再把 `<field>_<species>` 名字继续 append 到 `m_varnames`，因此“无普通场输出但仍有粒子归约场输出”在当前实现里可以同时成立。
- 最新推进（2026-05-21）：继续清 diagnostics particle-output 相邻 still-coarse 条目，已把 `<diag>.species` 再压到更精确的 BTD merge 边界，补清 `MergeBuffersForPlotfile()` 在首轮 flush 时会先按 `m_output_species_names` 为每个 species 创建 snapshot 目录并持续重写 species `Header`，但如果某个 species 在当前 buffer 的 `m_total_particles == 0`，源码会在 header 合并后直接跳过 `Particle_H` 与 `DATA_*` 的 rename/interleave；因此 species 绑定在 BTD plotfile 路径里可以只留下 per-species 目录与 header，而不保证该次 flush 一定生成实际粒子数据文件。
- 最新推进（2026-05-21）：继续清 diagnostics particle-output 相邻 still-coarse 条目，已把 `<diag>.write_species` 再压到更精确的 BTD flush/reset 边界，补清 BTD 每次 flush 结束后是否执行 `ResetTotalParticlesInBuffer()` 与 `ClearParticleBuffer()`，检查的只是 `m_output_species_names` 是否为空，而不是本次是否真的写出了粒子文件；因此只要 `write_species=1` 让 species 名单保留下来，BTD 就会进入粒子 buffer reset 链，相对地 `write_species=0` 在清空 species 名单时也会一起切断这条 reset 路径。
- 最新推进（2026-05-21）：继续清 diagnostics particle-output 相邻 still-coarse 条目，已把 `<diag>.<species>.variables` 再压到更精确的默认列边界，补清只有在显式给出 `variables` 时 `ParticleDiag` 才会把 `m_plot_flags` 全清零并重建列选择；若根本没给，当前 species 已有的 runtime real comps 会默认全保留。相对地，`phi/E/B` 这类只在输出时附加生成的字段不会因此自动打开，仍必须通过 `variables` 或 `additional_variables` 显式请求。
- 最新推进（2026-05-21）：继续清 diagnostics particle-output 相邻 still-coarse 条目，已把 `<diag>.<species>.variables` 再压到更精确的 backend 分叉，补清它虽然仍在 `ParticleDiag` 中通过 `m_plot_flags` 重写主输出列，plotfile/openPMD writer 也都会继续消费这份列选择；但 checkpoint 路径的 `CheckpointParticles()` 实际直接按容器当前 `h_redistribute_real_comp / h_redistribute_int_comp` 组织 SoA 输出，根本不看 `m_plot_flags`。因此这条参数当前真正控制的是 plotfile/openPMD 的 per-species 额外列选择，不是所有粒子 backend 的统一列合同。
- 最新推进（2026-05-21）：继续清 diagnostics runtime 相邻 still-coarse 条目，已把 `<diag>.diag_lo` 从“裁剪输出域并禁用 reduced-domain 粒子 I/O”的摘要压到更精确的反向边界，补清 `Diagnostics::InitData()/InitDataAfterRestart()` 在显式给出 `diag_lo/diag_hi` 时，虽然会先给已有 `ParticleDiag` 置 `m_do_geom_filter = true`，但随后又会立刻清空每个 buffer 的 `m_output_species`；因此 plotfile/openPMD writer 里各自构造的 `GeometryFilter(...)` 在当前 reduced-domain 路径里实际上走不到执行阶段，真正保留下来的只有 field-side `diag_dom/diag_box` 裁剪，而不是“带几何过滤的粒子输出”。
- 最新推进（2026-05-21）：继续清 diagnostics runtime 相邻 still-coarse 条目，已把 `<diag>.diag_lo / diag_hi` 再压到更精确的 field/particle 总闭包，补清它们不仅继续决定 full diagnostics 的 `diag_dom/diag_box/m_geom_output` 和 BTD 的 `buffer_box/m_snapshot_domain_lab`，还会在 `InitData()/InitDataAfterRestart()` 里先给已有 `ParticleDiag` 打开 `m_do_geom_filter`，并在 full diagnostics 的 `PrepareFieldDataForOutput()` 中继续把 `m_geom_output[i_buffer][0].ProbDomain()` 写回 `m_diag_domain`；但同一条 reduced-domain 路径又会立刻清空 `m_output_species`，所以 writer 侧虽然保留了 `GeometryFilter(...)` 的构造点，当前实际上走不到粒子 `copyParticles(...)` 执行阶段。当前稳定生效的是 field/snapshot 几何裁剪，不是 reduced-domain 粒子输出。
- 最新推进（2026-05-21）：继续清 diagnostics runtime 相邻 still-coarse 条目，已把 `<diag>.dump_last_timestep` 再压到更精确的尾部 flush 闭包，补清 `force_flush=true` 传下去以后并不是所有 diagnostics 都“重算后再写出”：full diagnostics 会重新 `ComputeAndPack()` 后再 flush，boundary scraping 不会重算、只会强制写出现有边界缓冲，BTD 则只会在 buffer 非空时 flush 已有 lab-frame buffer、不会借这次 force flush 再做新的 back-transform 计算。与此同时，这条尾部路径仍只作用于 `multi_diags` 工厂链，不会顺带重跑 `reduced_diags`，后者继续只按常规 step-loop 节奏或 restart 首帧补写路径独立触发。
- 最新推进（2026-05-21）：继续清 diagnostics runtime / writer-side 相邻 still-coarse 条目，已把 `<diag>.verbose` 从“diagnostics 默认 verbosity 继承链”的摘要压到更精确的 backend 边界，补清 `warpx.verbose -> <diag>.verbose` 的三段默认链之后，`Plotfile/OpenPMD/Checkpoint/Sensei/Ascent` 确实会在 `verbose > 0` 时打印 writer 日志，`TimeAveraged` 还会在 `m_verbose > 1` 时输出 averaging-period 调试信息；同时明确 `FlushFormatCatalyst` 当前只是接收占位形参 `int /*verbose*/`，并不会真正消费这条 instance-local verbosity。
- 最新推进（2026-05-21）：继续清 diagnostics writer-side 相邻 still-coarse 条目，已把 `catalyst.script_paths / implementation / implementation_search_paths` 补成正式 bridge 参数行，补清这组输入不是 `<diag_name>.*`，而是 `FlushFormatCatalyst` 通过 `ParmParse("catalyst")` 读取的全局 pipeline 配置；它们先决定 `script_paths` 如何按 `:`/`;` 切成 `scriptN`、`implementation/search_paths` 如何写进 `catalyst_load` 节点并驱动 `catalyst_initialize(...)`，随后又继续约束 `WriteToFile()` 的 mesh/particle channel 组织、空粒子通道的 dummy topology fallback，以及析构时 `catalyst_finalize(...)` 的收尾边界。
- 最新推进（2026-05-21）：继续清 diagnostics writer-side 相邻 still-coarse 条目，已把 `format` 从“writer 名字 + backend 分派”的摘要压到更完整的 diagnostics 总入口，补清它不仅控制 `plotfile/checkpoint/openpmd/ascent/catalyst/sensei` 的允许集合与 flush-backend 工厂，还继续决定 `checkpoint` 完整性约束、`sensei/ascent` 的 ghost-cell `FillBoundary(...)` 预处理，以及 `ascent/catalyst/sensei` 三条 in-situ 路径都显式禁止 BTD、但分别落到 Blueprint publish/execute、Catalyst pipeline 和 SENSEI bridge `initialize()/update()` 的不同执行边界。
- 最新推进（2026-05-21）：继续清 diagnostics writer-side 相邻 still-coarse 条目，已把 `sensei_config / sensei_pin_mesh` 从“构造时读取并传给 bridge”的摘要压到更完整的 in-situ writer-side 合同，补清 `FlushFormatSensei` 在读取这两条输入后会立刻 `new AmrMeshParticleInSituBridge`、`setEnabled/setConfig/setPinMesh` 并执行 `initialize()`，初始化失败即当场 abort；同时补清运行期 `WriteToFile()` 不是走普通文件 writer，而是显式拒绝 BTD 后把 `MultiFab`、变量名和粒子容器交给 `m_insitu_bridge->update(...)`，因此这两条参数真正控制的是 SENSEI bridge 的初始化与网格坐标解释，而不是普通 diagnostics 命名或 flush 节奏。
- 最新推进（2026-05-21）：继续清 openPMD writer-side 相邻 still-coarse 条目，已把 `adios2_engine.parameters.*` 从“engine JSON 参数表”的摘要继续压到更完整的 BTD writer-side consumer，补清这批参数在 `detail::getSeriesOptions(...)` 拼成 `m_OpenPMDoptions` 之后，还会被 `WarpXOpenPMDPlot::FlushBTDToDisk()` 直接搜索 `FlattenSteps`；若命中则对当前 iteration 发送 `"new_step"` flush target，否则改走 `"disk"`，因此它不只影响 `Series(...)` 构造，还会直接改写 BTD 强制落盘策略。
- 最新推进（2026-05-21）：继续清 openPMD writer-side 相邻 still-coarse 条目，已把 `openpmd_encoding` 从“文件布局 + BTD 兼容性”的摘要继续压到更完整的 writer-side 收尾边界，补清 `CloseStep(isBTD,isLastBTDFlush)` 不只负责关闭当前 iteration，还会在允许 close 时基于 `GetFileName()` 写出 `paraview.pmd` helper 文件；因此在 BTD 中间 buffer flush 期间，这条 helper 更新链会和 iteration close 一起被延后到最后一块 buffer。
- 最新推进（2026-05-21）：继续清 openPMD writer-side 相邻 still-coarse 条目，已把 `openpmd_encoding` 从“文件布局 + BTD 兼容性”的摘要压到更完整的兼容层边界，补清旧布尔别名 `openpmd_tspf` 只有在用户没有显式给 `openpmd_encoding` 时才会被查询，并且只有 `openpmd_tspf = 1` 时才把编码回退成 `fileBased`；因此它不是与 `openpmd_encoding` 并列生效的第二入口，而是只在缺省路径上生效的 legacy alias。
- 最新推进（2026-05-21）：继续清 openPMD writer-side 相邻 still-coarse 条目，已把 `openpmd_backend` 从“backend 名字 + 文件后缀”的摘要压到更完整的 backend 选择链，补清 `WarpXOpenPMDFileType()` 的默认回退顺序实际是 `bp5 -> bp -> h5 -> json`，其中 `json` 在官方参数文档里被明确标成 debugging 用途且只支持 serial/single-rank；同时补清 `WarpXOpenPMDPlot::Init()` 在多 rank 下会走带 communicator 的 `openPMD::Series(...)` MPI 构造分支、若 openPMD-api 未启用 MPI 支持则直接 abort，而单 rank 时改走无 communicator 的构造分支。
- 最新推进（2026-05-21）：继续清 openPMD writer-side 相邻 still-coarse 条目，已把 `adios2_operator.parameters.*` 从“dataset-operator 参数表”的摘要压到更完整的 JSON 生成边界，补清 `FlushFormatOpenPMD` 只负责整体抓取并去掉 `diag_name + ".adios2_operator.parameters"` 前缀，而 `WarpXOpenPMD.cpp::detail::getSeriesOptions(...)` 只有在 `adios2_operator.type` 非空时才会真正生成 `"dataset" -> "operators"[0]` 这整块 JSON；也就是说它不像 engine 参数那样可以“无 type 仍保留 parameters 子块”，而是必须依附于 operator type 才会通过 `m_OpenPMDoptions` 进入 `openPMD::Series(...)`。
- 最新推进（2026-05-21）：继续清 diagnostics writer-side 相邻 still-coarse 条目，已把 `file_min_digits` 从“统一编号宽度”的摘要压到更完整的命名合同，补清它不仅控制普通 diagnostics flush backend 里按 `iteration[0]` 生成的零填充步号，也继续进入 openPMD `fileBased` 模式下的 `openpmd_%0NT.<backend>` 文件模板；而在 BTD plotfile 路径里，同一宽度还会分别服务于按 `i_buffer` 编号的临时 `.../buffer` 根目录、按 `i_snapshot` 编号的最终 snapshot 目录，以及该目录下按当前 boosted-frame `iteration[0]` 命名的最近一次 flush 子树，因此它实际承载的是普通步号、openPMD 文件名与 BTD 三套编号语义的共同零填充合同。
- 仓库状态：2026-05-18 已初始化本地 git 仓库，默认分支 `main`，并补最小 `.gitignore`
- WarpX 路径：`../warpx`
- WarpX 分支：`pkuHEDPbranch`
- WarpX commit：`063f8b586f04321e13150ae3e730e0794ca75cb1`
- 最高优先级计划：`docs/warpx-full-code-reading-book-plan.md`
- 当前执行框架：`docs/warpx-source-reading-framework.md`
- 当前阶段：阶段 5 Boundary / AMR 已启动，已完成 field / particle 边界参数解析与 periodic 一致性约束精读、`WarpXFieldBoundaries.cpp` 第一轮顶层分派梳理、PML `SigmaBox` / BoxArray / split-field / PML current 数据流精读、PEC/PMC/PECInsulator 的 E/B 与 rho/J 镜像规则精读、boundary 参数总表整理、Silver-Mueller 内部 guard-cell 递推精读，以及 `EmbeddedBoundary` 运行时开关、AMReX EB2 初始化、signed-distance 场、reduced-shape / stair-case / ECT 更新标记初始化、face extension、`FaceInfoBox` 借用关系、BCK fallback、粒子 scraping、`DistanceToEB` 法向重建与 scraped particle buffer 精读；并已启动 `Parallelization`，完成 `GuardCellManager` 的 guard-cell 分配模型、`FillBoundary`/`SumBoundary` 语义、`SyncCurrent()` / `SyncRho()` 的 finest-to-coarsest 与 owner-mask 去重、current/rho coarse-fine source 路径、`CheckLoadBalance()` / `LoadBalance()` / `RemakeLevel()` 的 level 重映射与 costs 模型、`UpdateAuxilaryData*()` / buffer masks / `PartitionParticlesInBuffers()` 所构成的 AMR coarse-fine substitution strategy、`WarpXComm_K.H` / `MFIter` / `ParallelFor` / `FillBoundary` 分支所构成的执行模型第一轮精读，以及粒子层 `PushPX()` / `DepositCurrent()` / `DepositCharge()` 如何真正消费 `aux`、`cax`、`current_buf`、`rho_buf` 的 coarse-fine buffer 路径；同时已回到 `Particles/` 顶层补完容器层次与 runtime attribute 地图，并继续把它接到 `Particles/Pusher` 的非标准路径上，完成 classical radiation reaction、implicit fixed-point / suborbit fallback、photon push、`current_fp_non_suborbit` / `MassMatrices_PC` / JFNK linear-stage 分工的第一轮精读、`ImplicitSolver::PreLinearSolve()` / `ComputeJfromMassMatrices()` / `SetMassMatricesForPC()` 与 `MatrixPC/JacobiPC/CurlCurlMLMGPC` 的场求解器耦合层精读、`F(U)=U-b-R(U)` / `JacobianFunctionMF::apply()` / PETSc shell operator / native preconditioner 的完整消费链精读，以及 `StrangImplicitSpectralEM::ComputeRHS()`、SNES Jacobian callback、`assemblePCMatrix()`、`KSPSetOperators(A,P)`、`WarpXSolverDOF` 的 `{local,global}` 编号契约和 `MatrixPC::Assemble()` 在 1D / XZ / RZ / 3D / RCYLINDER 下的 `pc_petsc` 稀疏矩阵装配细节精读，并分别回填第 4/6 章；当前已开始补最小运行级验证记录，`Langmuir` 与 `uniform_plasma` 的第一条本地 run note 已落地。
- 最新推进（2026-05-21）：继续清 diagnostics 相邻 still-coarse 条目，已把 `file_prefix` 从“统一输出前缀模板”的摘要压到更完整的命名合同，补清它在 BTD plotfile 路径里不只服务于 `Flush()` 时按 `i_buffer` 生成的临时 `.../buffer` 根目录，还会在 `MergeBuffersForPlotfile(i_snapshot)` 中继续扩成按 `i_snapshot` 命名的最终 snapshot 目录，并在其下再按当前 boosted-frame `iteration[0]` 派生最近一次 flush 的临时 buffer 子树，因此同一前缀同时承载 snapshot 级、buffer 级和当前步 flush 产物三层命名语义。
- 最新推进（2026-05-21）：继续清 openPMD 相邻 still-coarse 条目，已把 `adios2_engine.type / parameters.*` 从“进入 Series options”的摘要压到更完整的 JSON 生成链，补清 `FlushFormatOpenPMD` 只负责收集并去掉 `diag_name + ".adios2_engine.parameters"` 前缀，而 `WarpXOpenPMD.cpp::detail::getSeriesOptions(...)` 会进一步决定是否保留 `"engine"` 块、何时写入 `"type"`、以及在仅有 parameters 或同时存在 operator 块时如何自动拼接出最终 `m_OpenPMDoptions` JSON，再由 `Init()` 原样传给 `openPMD::Series(...)`。
- 最新推进（2026-05-21）：继续清 openPMD 相邻 still-coarse 条目，已把 `openpmd_encoding` 从“文件布局 + BTD 兼容性”的摘要压到更完整的 writer-side 语义，补清 BTD 下若给到 streaming/variable-based 编码，源码会先 warning 再强制改回 `groupBased`，并继续明确 `fileBased` 与 `groupBased` 不只改变文件名模板，还会进一步决定 `WarpXOpenPMDPlot::SetStep()/Init()/CloseStep()` 在 BTD 下是“每个 snapshot 重新建文件级 Series”还是“在单一容器内复用/追加 iteration”。
- 最新推进（2026-05-21）：继续清 openPMD BTD 相邻 still-coarse 条目，已把 `buffer_flush_limit_btd` 从“ADIOS buffered steps 刷盘阈值”的摘要压到更完整的 writer-side 语义，补清它不仅控制 `FlushFormatOpenPMD::WriteToFile()` 里何时按 `bufferID % limit == 0` 调 `FlushBTDToDisk()`，还明确连到了 `WarpXOpenPMDPlot::FlushBTDToDisk()` 对 `"new_step"`/`"disk"` flush target 的分支，以及 `CloseStep(isBTD,isLastBTDFlush)` 在 BTD 下只有最后一块 buffer 才真正关闭当前 snapshot iteration 的边界。
- 最新推进（2026-05-21）：继续清 diagnostics/BTD 相邻 still-coarse 条目，已把 `<diag>.intervals` 从“普通步进调度器 + BTD snapshot 索引生成器”的摘要压到更完整的分支语义，补清它不仅会被 `BTDIntervalsParser` 展开成升序去重的 `m_btd_iterations`，还会继续决定 `m_num_buffers` 与 `m_buffer_flush_counter / m_first_flush_after_restart` 这套状态数组尺寸，并在 `MergeBuffersForPlotfile()` 中继续分叉成“首次或 restart 后首轮 flush 走 snapshot 目录与 Header rename 首块分支”以及“后续 flush 改走 interleave/append 分支”两条写盘语义。
- 最新推进（2026-05-21）：继续清 BTD 相邻 still-coarse 条目，已把 `dt_snapshots_lab` 从“lab-frame 时间间距输入”的摘要压到更完整的 runtime chain，补清它不仅决定每个 snapshot 的 `m_t_lab[i_buffer]`，还会继续驱动 `UpdateCurrentZBoostCoordinate / UpdateCurrentZLabCoordinate` 初始化和每步回推 `m_current_z_boost / m_current_z_lab`，并最终在 flush 时作为 `labtime` 写入当前 snapshot/buffer 的实验室系时间戳。
- 最新推进（2026-05-21）：继续清 BTD 相邻 still-coarse 条目，已把 `dz_snapshots_lab` 从“lab-frame 空间间距壳输入”的摘要压到更完整的 runtime chain，补清它不仅会在 `BTDiagnostics::ReadParameters()` 中按 `m_dt_snapshots_lab = m_dz_snapshots_lab / WarpX::moving_window_v` 换算成时间节奏，还明确连到了 `WarpX.cpp` 对旧式顶层 `warpx.dz_snapshots_lab` 的 legacy 语法断言、BTD 对 moving window 必须开启且沿 `z` 方向运行的硬约束，以及后续统一复用离散后的 `m_dt_snapshots_lab` 进入 `m_t_lab[i_buffer]` 时间轴、z-slice 回推和 `final_snapshot_fill_iteration/fill_time` 自动补步数链。
- 最新推进（2026-05-21）：继续清 BTD 相邻 still-coarse 条目，已把 `num_snapshots_lab` 从“快照数输入”的摘要压到更完整的 snapshot-topology chain，补清它不仅会被改写成 BTD 专用 `intervals` 字符串，再由 `BTDIntervalsParser` 展开成升序去重的 `m_btd_iterations`，还会继续决定 `m_num_buffers` 与整套 snapshot/buffer 状态数组尺寸，并通过 `GetBTDIteration(i_buffer)` 和 `m_buffer_flush_counter[i_snapshot]` 进入每个 snapshot 的 lab-frame 时间轴与 `Cell_D_* / DATA_*` merge 编号语义。
- 最新推进（2026-05-21）：继续清 BTD 相邻 still-coarse 条目，已把 `do_back_transformed_particles` 从“粒子侧总开关”的摘要压到更完整的 runtime chain，补清它不仅会在 species 首次打开 BTD 时给原粒子容器注入 `x_n_btd / y_n_btd / z_n_btd / ux_n_btd / uy_n_btd / uz_n_btd` 这组 runtime real comps，还会继续决定 per-buffer pinned particle containers 的建立、flush 前临时扩 box 以便 `Redistribute()`/writer 接收略微出界粒子，以及 flush 后 `ResetTotalParticlesInBuffer / ClearParticleBuffer / RedistributeParticleBuffer` 这条 reset 链。
- 最新推进（2026-05-21）：继续清 BTD 相邻 still-coarse 条目，已把 `do_back_transformed_fields` 从“字段侧总开关”的摘要压到更完整的 runtime chain，补清它不仅会在 parser 末尾通过 `m_varnames.clear()` 和“字段列表为空则再次固化为 false”这两步切断 field path，还会继续决定 `DefineCellCenteredMultiFab / InitializeFieldFunctors / PrepareFieldDataForOutput / DefineFieldBufferMultiFab` 是否真正运行、RZ/openPMD 下是否触发 mode-expanded `m_varnames` 重写，以及纯粒子 BTD 路径里为什么还会补建 snapshot geometry 与 field-buffer 容器壳。
- 最新推进（2026-05-21）：继续清 BTD 相邻 still-coarse 条目，已把 `buffer_size` 从“决定每个 buffer 有多少切片”的摘要压到更完整的 runtime chain，补清它不仅决定 `DerivedInitData()` 里的 `num_buffers` 与 `final_snapshot_fill_iteration` 估算、`InitializeBufferData()` 里的 snapshot z-extent 对齐，还会在 `DefineFieldBufferMultiFab()` 中直接决定每次实际分配出的 BTD buffer z-span，并继续进入 `DoDump()` 的 buffer-full flush 判据。
- 最新推进（2026-05-21）：继续清 `TimeAveraged` 相邻 still-coarse 条目，已把 `average_start_step` 从“fixed_start 起点”的摘要压到更完整、但回到源码实情的静态窗口边界，补清它不仅在 `fixed_start` 模式下被强制读取、在 `dynamic_start` 下只会 warning 并忽略，还会连带把同簇的 `average_period_steps / average_period_time` 置成“给了也忽略”的 parser 边界；相对地，当前实现里它还不能被写成已经独立决定 non-output-step averaging gate 的 static runtime 开关。
- 最新推进（2026-05-21）：继续清 `TimeAveraged` 相邻 still-coarse 条目，已把 `average_period_steps / average_period_time` 从“参数互斥 + 步长换算”的摘要压到更完整、但限于 `dynamic_start` 的 runtime chain，补清它们不仅决定 `DerivedInitData()` 里的 `dt <-> steps` 离散化，还会在 `DoComputeAndPack(step)` 中回推每个 output interval 对应的 `m_average_start_step`、形成 `dynamic_start` 非输出步也继续累计 `m_sum_mf_output` 的 gate，并在 `Flush()` 时继续控制平均化分母与 `dynamic_start` 模式下的累计缓冲清零；同时确认 step `0` 仍保留一帧瞬时输出，不受 averaging window 影响。
- 最新推进（2026-05-21）：继续清 startup / diagnostics 邻接 I/O bridge，已把又一组此前未正式入表的 `vismf.*` low-frequency 参数补成 grouped pass-through 行，补清 `vismf.headerversion / verbose` 的真实 parser 仍在同级 `amrex` 的 `VisMF`，其中 `verbose` 直接控制底层 `VisMF::Read/Write/RemoveFiles` 的调试打印，而 `headerversion` 虽是 `VisMF` 真实输入，却会在 WarpX 的 plotfile/checkpoint flush 路径里被分别临时改写成 `Version_v1` 与 `NoFabHeader_v1`，写完再恢复。
- 最新推进（2026-05-21）：继续清 startup / diagnostics 邻接 I/O bridge，已把第二组此前未正式入表的 `vismf.*` low-frequency 参数补成 grouped pass-through 行，补清 `vismf.usedynamicsetselection / iobuffersize / allowsparsewrites / noflushafterwrite / barrierafterlevel` 的真实 parser 仍在同级 `amrex` 的 `VisMF`，其中 `usedynamicsetselection` 与 `allowsparsewrites` 直接进入写盘调度分支，`iobuffersize` 控制 `VisMFBuffer`/`pubsetbuf(...)` 缓冲大小，`noflushafterwrite` 与 `barrierafterlevel` 则分别进入 field/particle 写盘后的 flush 与 level 级 barrier 边界。
- 最新推进（2026-05-21）：继续清 startup / diagnostics 邻接 I/O bridge，已把此前未正式入表的一组 `vismf.*` low-frequency 参数补成 grouped pass-through 行，补清 `vismf.groupsets / setbuf / checkfilepositions / usepersistentifstreams / usesynchronousreads` 的真实 parser 在同级 `amrex` 的 `VisMF`，其中 `groupsets/setbuf` 最近影响到 `NFilesIter` 的 rank-to-file 分组与 `pubsetbuf(...)` 写侧缓冲，而 `checkfilepositions / usepersistentifstreams / usesynchronousreads` 则属于 `VisMF::Read(...)` 的读侧合同，最近的 WarpX 邻接边界是 restart/PML 的 MultiFab 恢复链。
- 最新推进（2026-05-21）：继续清 startup / diagnostics 邻接 I/O bridge，已把 `warpx.usesingleread / usesinglewrite` 从“WarpX 到 VisMF 的兼容桥接”压到更完整的跨仓链，补清同级 `amrex` 里的真实 parser 名就是 `vismf.usesingleread / vismf.usesinglewrite`、其默认值是 `false`，而 WarpX 本地则在 startup 早期用自身默认 `true` 覆写 `vismf.*` 命名空间；同时确认本项目已有 `warpx_used_inputs` 与 `warpx_job_info` 里最终落盘的也是 `vismf.usesingle* = true`，不是 `warpx.usesingle*`。
- 最新推进（2026-05-21）：继续清 startup / diagnostics 邻接 I/O bridge，已把 `amrex.async_out / async_out_nfiles` 从“AMReX 异步 plotfile I/O 参数”的摘要压到更完整的 plotfile-only 异步写盘合同，补清 `amrex.async_out=1` 时真实语义是后台 I/O 线程异步写 `WriteMultiLevelPlotfile(...)`、simulation 主线程可继续推进，而 `amrex.async_out_nfiles` 不只限制异步 writer fan-out、在 MPI ranks 超过该上限时要求 `-DWarpX_MPI_THREAD_MULTIPLE=ON`，还会通过同一个 `AsyncOut::GetWriteInfo(...)` / `MPI_Comm_split(...)` 共享地决定 field `AsyncWriteDoit(...)` 和粒子 `WriteBinaryParticleDataAsync(...)` 的 rank-to-file 分组拓扑；同时明确这两条都不控制 checkpoint 的 `VisMF::Write(...)` 路径。
- 最新推进（2026-05-21）：继续清 startup / diagnostics 邻接 I/O bridge，已把 `warpx.field/particle_io_nfiles` 从“两个 I/O 并发度参数”的摘要压到更完整的 field/particle 分流链，补清 `field_io_nfiles` 会直接进入 `VisMF::SetNOutFiles(...)`，后续真实 consumer 是 `WriteMultiLevelPlotfile(...)` 的 field plotfile 写链和 checkpoint 中大量 `VisMF::Write(...)` 的场 MultiFab 写链；而 `particle_io_nfiles` 则继续只桥接到 `particles.particles_nfiles`，再由底层粒子 `WritePlotFile/Checkpoint` 消费。
- 最新推进（2026-05-21）：继续清 startup / diagnostics 邻接 I/O bridge，已把 `warpx.usesingleread / usesinglewrite` 从“WarpX 到 VisMF 的兼容桥接”再压到更细的 `VisMF` 实现边界，补清 `useSingleWrite` 在 `VisMF::Write(...)` 中会在 `(nFABs > 1 || doConvert)` 命中后先把多个 `FArrayBox` 的 header/payload 线性打包进单块 `allFabData`，再执行一次 `Stream().write(...)`；相对地 `useSingleRead` 还要额外满足同一 rank 负责的多块 fab 在文件里 `dataIsContiguous`，只有这时才会单次 `read(allFabData, bytesToRead)` 后再拆回各个 `FArrayBox`，否则即便开关为真也会退化回逐 fab 读链。因此当前 single-read/single-write 在实现上并不是完全对称的合同。
- 最新推进（2026-05-21）：继续清 startup / diagnostics 邻接 I/O bridge，已把 `particles.particles_nfiles` 从“粒子 `NFilesIter` fan-out”压到更细的 writer/prepost 共享边界，补清这条值在 `WriteBinaryParticleData{Sync,Async}` 进入前会先统一写入 `pc.nOutFilesPrePost`，因此 sync/async 两条粒子写盘分支共享的是同一份文件槽位数量，而不是各自独立并发度；同时 `use_prepost` 打开后，`CheckpointPre()/CheckpointPost()` 也会继续复用这份 `nOutFilesPrePost` 和 `filePrefixPrePost`，在 header append 与 zero-length `DATA_*` unlink 阶段按同样数量的输出文件槽位做聚合计数和收尾。
- 最新推进（2026-05-21）：继续清 startup / diagnostics 邻接 I/O bridge，已把 `warpx.field/particle_io_nfiles` 从“field/particle 两条并发度桥接”再压到更细的全局/局部分离边界，补清 `field_io_nfiles` 会立刻改写 `VisMF` 进程级静态 `nOutFiles`，因此后续所有 `VisMF::Write(...)` / `WriteMultiLevelPlotfile(...)` 共享的是同一份全局场写盘槽位状态；而 `particle_io_nfiles` 不会触碰这份 `VisMF` 全局静态值，而是只沿 `particles.particles_nfiles -> nOutFiles -> pc.nOutFilesPrePost` 进入粒子容器自己的 writer/prepost 状态，所以两条并不是同一个全局 I/O 槽位数在 field/particle 两侧的别名。
- 最新推进（2026-05-21）：继续清 startup / diagnostics 邻接 I/O bridge，已把 `warpx.mffile_nstreams` 从“每文件 reader 并发度”再压到更细的静态状态分离边界，补清它在 `WarpX::ReadParameters()` 中只改写 `VisMF` 的 `nMFFileInStreams`，随后只进入 `VisMF::Read(...)` 内部的 `nOpensPerFile` / `availableFiles` 读批次划分；它不会触碰 `OpenStream()/CloseStream()` 侧的 `vismf.setbuf / iobuffersize / usepersistentifstreams` 静态状态，因此控制的是“每文件多少并发 reader 批次”，不是 stream 缓存或 buffer 策略。
- 最新推进（2026-05-21）：继续清 startup / diagnostics 邻接 I/O bridge，已把 grouped `vismf.groupsets / setbuf / checkfilepositions / usepersistentifstreams / usesynchronousreads` 再压到更细的共享/非共享静态状态边界，补清这组键和 `usesingleread / usesinglewrite / mffile_nstreams` 一样都属于 `VisMF` 自己维护的静态成员表，但 `groupsets/setbuf` 主要进 `NFilesIter/Write` 与 `OpenStream`，`usepersistentifstreams/usesynchronousreads` 主要进 `Read`/stream 生命周期，而 `usesingleread/usesinglewrite` 只进合并 read/write 分支、`mffile_nstreams` 只进 `nOpensPerFile` 读批次划分，因此这些 `vismf.*` 低频键虽然共享同一份静态状态表，并不是一个统一总开关。
- 最新推进（2026-05-21）：继续清 startup / diagnostics 邻接 I/O bridge，已把 grouped `vismf.usedynamicsetselection / iobuffersize / allowsparsewrites / noflushafterwrite / barrierafterlevel` 再压到更细的共享/非共享静态状态边界，补清这五条和前面那组 `vismf.*` 一样都挂在 `VisMF` 的静态状态表上，但 `usedynamicsetselection / allowsparsewrites / noflushafterwrite` 主要进 `VisMF::Write(...)`，`iobuffersize` 同时喂给 `VisMFBuffer` 与部分 stream buffer 路径，`barrierafterlevel` 只被 field plotfile 与粒子 sync writer 复用，不会自动扩展到所有粒子 async/plotfile header 路径，因此它们也不是一个“所有 I/O 细节统一联动”的总开关。
- 最新推进（2026-05-21）：继续清 startup / diagnostics 邻接 I/O bridge，已把 `vismf.headerversion / verbose` 再压到更细的共享/非共享静态状态边界，补清它们和前面各组 `vismf.*` 一样都挂在 `VisMF` 的静态状态表上，但 `headerversion` 主要落在 `Header/Write` 结构合同并会被 WarpX 的 plotfile/checkpoint writer 临时覆写，`verbose` 则稳定落在 `Read/Check/RemoveFiles` 日志路径，不会随着 writer 本地的 “Writing plotfile/checkpoint” 提示一起联动，因此这两条也不是统一的“VisMF 全局模式开关”。
- 最新推进（2026-05-21）：继续清 startup / diagnostics 邻接 I/O bridge，已把 `warpx.mffile_nstreams` 从“VisMF 全局 reader 并发度”的摘要压到更完整的 restart/PML 读链，补清它在 `WarpX::ReadParameters()` 中只通过 `VisMF::SetMFFileInStreams(...)` 设置读侧上限，后续真实 consumer 是 `InitFromCheckpoint()` 里恢复 `E/B/J/*_avg_*` 等场 MultiFab 的大量 `VisMF::Read(...)` 调用以及 `PML::Restart()` 的 `pml_E_*/pml_B_*` 恢复链；同时明确它不影响 plotfile/checkpoint 写盘路径。
- 最新推进（2026-05-21）：继续清 diagnostics per-species writer-side filter chain，已把 `<diag>.<species>.random_fraction / uniform_stride / plot_filter_function(...)` 从“粒子筛选器”的摘要压到更完整的 runtime 合同，补清 `random_fraction` 在 `RandomFilter` 中实际是逐粒子 `Random(engine) < fraction` 的伯努利抽样且源码不会 clamp 到 `[0,1]`，并且 plotfile/openPMD 两条 writer 在 `copyParticles(...)` 中使用的是 `random * uniform * parser * geometry` 乘法链而不是 `&&`，所以只要随机筛选激活，每个候选粒子都会先消费一次 RNG，即使后面的 filter 最终会拒绝它；同时 `uniform_stride` 仍实际按 `particle id % stride == 0` 做确定性保留且源码没有 `stride > 0` 防护，而且因为 `uniform_filter` 也处在同一条非短路乘法链里，`stride = 0` 的运行时风险不会被前面的随机筛选自动屏蔽；`plot_filter_function(...)` 则同样处在这条非短路乘法链里，因此 parser 表达式也会对每个候选粒子都被求值，而不会因为前面的随机或 stride 过滤已经失败就被短路跳过；在此基础上，它虽在 writer 前把容器临时转成 SI、但传给用户 parser 的 `ux/uy/uz` 最终仍会被规范化回 `beta*gamma`，并按“返回值非零即保留”执行筛选。
- 最新推进（2026-05-21）：继续清 diagnostics per-species 附加字段合同，已把 `<diag>.<species>.additional_variables` 从“附加粒子字段列表”的摘要再压到更精确的 writer-side 反向边界，补清 `phi` 不只要求 `diag_type = Full`，还额外要求 `warpx.do_electrostatic = labframe` 或 `labframe-electromagnetostatic`；同时确认 openPMD/pinned 路径会把 `!use_pinned_pc` 作为 `is_full_diagnostic` 传给 `storePhiOnParticles()/storeFieldOnParticles()`，因此 BTD 或其它 pinned particle writer 请求 `phi/E/B` 时会直接触发 assert，而不是静默跳过。
- 最新推进（2026-05-21）：继续清 diagnostics per-species 附加字段合同，已把 `<diag>.<species>.additional_variables` 再压到更精确的 materialize 顺序边界，补清 openPMD 不是在写文件时临时拼接 `phi/E/B`，而是在 `tmp.copyParticles(...)` 之后、构造 `real_names / real_flags` 之前，先通过 `storePhiOnParticles()/storeFieldOnParticles()` 把这些附加列真正插进 `tmp`；相对地 plotfile `WriteParticles()` 仍只把过滤后的 `tmp` 直接 `WritePlotFile(...)`，因此当前 backend 差异不只是“是否支持附加列”，还包括“是否进入列名导出前的 materialize 阶段”。
- 最新推进（2026-05-21）：继续清 diagnostics per-species 附加字段合同，已纠正 `<diag>.<species>.additional_variables` 的 backend 差异：当前只有 openPMD writer 会在 copy/filter 之后继续调用 `storePhiOnParticles()/storeFieldOnParticles()` 真正 materialize `phi/E/B` 附加列；plotfile `WriteParticles()` 则只把过滤后的 `tmp` 直接 `WritePlotFile(...)`，不会调用这两条 helper，因此这些 flags 在 plotfile backend 里目前不会自动变成实际输出列。与此同时，openPMD 侧 `phi` 仍受 `warpx.do_electrostatic = labframe / labframe-electromagnetostatic` 约束，而 pinned/BTD 路线请求 `phi/E/B` 仍会直接触发 assert。
- 最新推进（2026-05-21）：继续清 diagnostics per-species 附加字段合同，已把 `<diag>.<species>.additional_variables` 再压到更精确的 companion/backend 闭包，补清它和 `.variables` 不是两套并行列系统，而是 `m_plot_flags` 主列选择之外只补 `phi/E/B` 这组布尔位，因此即便 `variables = none` 已把普通 real comps 全关掉，这组附加字段仍可单独保留；相对地 checkpoint 路径既不会 `storePhiOnParticles()/storeFieldOnParticles()`，也不会读取这些布尔位，而是继续直接按容器当前可 redistribute 的 SoA 组件写盘，所以这条附加字段链当前只在 openPMD full particle diagnostics 里真正 materialize，plotfile 和 checkpoint 都明确旁路它。
- 最新推进（2026-05-21）：继续清 diagnostics per-species parser filter 合同，已把 `<diag>.<species>.plot_filter_function(...)` 从“plotfile/openPMD 都支持 pinned 粒子筛选”的近似说法压到更精确的 backend 分叉：plotfile 顶层 `WriteToFile(...)` 实际忽略 `use_pinned_pc`，因此 parser filter 只覆盖普通 `pc` 和 `isBTD` 时的 `pinned_pc`；openPMD 才同时覆盖普通 `pc`、BTD pinned 路径以及额外的独立 `use_pinned_pc` 路径。
- 最新推进（2026-05-21）：继续清 time-averaged diagnostics 运行合同，已把 `<diag>.time_average_mode` 从偏泛的“累计模式开关”压到更精确的 runtime gate：`Diagnostics::ComputeAndPack()` 里 `TimeAveraged` diagnostics 一旦真的进入 compute/pack 链，就会无条件对 `m_sum_mf_output` 做 `Saxpy` 累加；但 `FullDiagnostics::DoComputeAndPack()` 当前只在 `dynamic_start` 分支里为非输出步打开 `in_averaging_period`，`fixed_start` 没有对称的非输出步累计 gate。与此同时，`Flush()` 仍会在 `Static/Dynamic` 下统一改写成“写累计缓冲并归一化”，而只有 `dynamic_start` 会在写后清零 `m_sum_mf_output`。
- 最新推进（2026-05-21）：继续清 `TimeAveraged` 同簇一致性，已把 `<diag>.average_start_step` 从偏强的“fixed_start 运行期窗口起点”说法压回源码实情：它在 `ReadParameters()` 中仍是 `fixed_start` 必需的正整数锚点，并继续决定和 `average_period_steps / average_period_time` 的“给了也忽略”关系；但当前 `DoComputeAndPack()` 的非输出步 averaging gate 实际只在 `dynamic_start` 分支里 materialize，所以这条参数目前还不能被写成已经拥有独立 static averaging runtime gate。
- 最新推进（2026-05-21）：继续清 diagnostics per-species particle-output 条目，已把 `<diag>.<species>.variables` 从“粒子变量列表”的摘要压到更完整的 `ParticleDiag` 主输出列重写链，补清它一旦显式给出就会先把 `m_plot_flags` 全清零，`variables = none` 会让普通粒子属性整体保持关闭，而 `phi/Ex/Ey/Ez/Bx/By/Bz` 这类字段则改走 writer 后续在临时输出副本上补生成的附加字段分支。
- 最新推进（2026-05-21）：继续清 diagnostics particle-output 绑定键，已把 `<diag>.species` 从“species 名单”的摘要压到更完整的 per-species runtime 对象链，补清它不仅决定 full diagnostics 中 `ParticleDiag(..., species container)` 的构造，还会继续决定 boundary-scraping 中哪些 species/boundary 组合真正绑定 `ParticleBoundaryBuffer` 指针，以及 BTD 中 `SetDoBackTransformedParticles(...)`、`BackTransformParticleFunctor(...)` 和 per-snapshot pinned particle container 的建立；同时确认 restart 后 `InitDataAfterRestart()` 也会按同一份 species 绑定链重建这些对象。
- 最新推进（2026-05-21）：继续清 diagnostics particle-output 合同，已把 `<diag>.write_species` 从“是否写粒子”的摘要压到更完整的三路初始化链，补清它不仅控制基类 `InitData()/InitDataAfterRestart()` 是否建立 particle buffer/functor，还会继续决定 boundary-scraping 是否真正把 `ParticleBoundaryBuffer` 里的 per-species/per-boundary buffer 绑定进 `ParticleDiag(...)`，以及 BTD 是否打开 `SetDoBackTransformedParticles(...)` 和 back-transformed particle buffer；同时明确 reduced-domain `diag_lo/hi` 仍会直接清空 full diagnostics 的 particle I/O。
- 最新推进（2026-05-21）：继续清 diagnostics instance-local flush 合同，已把 `<diag>.plot_raw_fields / plot_raw_fields_guards` 从“plotfile raw 子目录开关”的摘要压到更完整的 writer-side 分流链，补清它们不仅在 `FullDiagnostics::ReadParameters()` 里组成 `raw_specified`，还会在 `format=checkpoint` 时直接触发全量转储兼容性断言；同时明确 `FullDiagnostics::Flush()` 与 `BTDiagnostics::Flush()` 都会继续透传这组值，plotfile 路径进入 `WriteAllRawFields(...)` 的真实 raw-field 写盘链，openPMD 路径整体硬拒绝，而 checkpoint 路径虽然接收参数但完全忽略。
- 最新推进（2026-05-21）：继续清 diagnostics instance-local/runtime gate，已把 `diagnostics.enable` 从“是否读取 `diags_names`”的摘要压到更完整的 `MultiDiagnostics` 工厂链，补清它不会阻止 `WarpX` 创建 `multi_diags` 对象，而是把 `ndiags/alldiags` 压成空集合，使 `InitDiagnostics()`、restart 首帧 `FilterComputePackFlush(...)`、以及 step-loop 中的 `DoComputeAndPack()/FilterComputePackFlush()` 一起退化为 no-op，并整体切断 full diagnostics 的 `MovingWindowAndGalileanDomainShift -> DoComputeAndPack -> ComputeAndPack/Flush` 主链。
- 最新推进（2026-05-21）：继续清 diagnostics 邻接 runtime gate，已把 `warpx.limit_verbose_step` 从“按步降采样日志”的摘要压到更精确的主循环 verbosity chain，补清它不仅控制 `WarpXEvolve.cpp` 中 `STEP starts`、adaptive-`dt` 提示和一步结束 wall-clock 信息的分段打印，还会继续通过 `verbose_step` 传入 `mypc->doResampling(...)`，进而约束各 species 的 resampling 日志；同时明确 `re-sorting particles` 提示显式走 `verbose && !m_limit_verbose_step`，并不复用同一降采样 gate。
- 最新推进（2026-05-21）：继续清 reduced-diags 相邻尾项，已把 `<reduced>.histogram_function / normalization / filter_function` 与 `histogram_function_abs/ord / value_function/filter_function` 压到更完整的 1D/2D parser consumer 链，特别补清 `normalization` 当前只属于 `ParticleHistogram` 的 1D 后处理分支，以及 `ParticleHistogram2D` 里 `value_function(...,w)` 虽构造期按 `query(...)` 读取、但 `ComputeDiags()` 仍会无条件编译和调用 `m_parser_value` 的现有源码边界。
- 最新推进（2026-05-21）：继续清 `DifferentialLuminosity2D` 相邻尾项，已把 `bin_number_1/2 + bin_min/max_1/2` 与 `openpmd_backend / file_min_digits` 压到更完整的 2D luminosity 累计/写出链，补清它是“每个时间步持续累积、只在 interval 时拷回与归约”的 reduced-diag，并把 `bin_size_1/2` 直接进入 `d2L_dE1_dE2` 物理归一化、Windows 路径改写、openPMD `setPosition/time` 元数据和缺少 `WARPX_USE_OPENPMD` 时的 abort 边界写回总表。
- 最新推进（2026-05-21）：继续清 `ColliderRelevant / ChargeOnEB` 相邻尾项，已把 `<reduced>.species` 扩展到 `ColliderRelevant` 的双束合同与 neutral-species 拒绝边界，并把此前总表缺失的 `ChargeOnEB.weighting_function(x,y,z)` 补成正式条目，明确它只在 `3D + EB` 运行链有效，且真实 consumer 是 `ChargeOnEB::ComputeDiags()` 中对 EB 面元 `dS·E` 局部贡献的空间加权。
- 最新推进（2026-05-21）：继续清 RZ / reduced-diag 邻接尾项，已把 `warpx.n_rz_azimuthal_modes` 压到更完整的本地 consumer 链，补清它不仅进入 `CylindricalYeeAlgorithm::ComputeMaxDt(...)`，还在 `FieldPoyntingFlux` 与 binary-collision 模块里形成 `== 1` 的硬兼容性边界，并继续约束 `PlasmaInjector` 的 `num_particles_per_cell*` 下界以及 `WarpXOpenPMD.cpp` 的 RZ 几何元数据写出。
- 最新推进（2026-05-21）：继续清 reduced-diag 工厂/多态尾项，已把 `<reduced>.type` 从“实例化哪种 diagnostics”进一步压到真实调度链，补清它还决定实例是否会真正消费 `ComputeDiagsMidStep()` 与 checkpoint 钩子；其中 `FieldPoyntingFlux` 作为特例，会在 mid-step 切换到 `use_mid_step_value` 分支，并通过 `FieldPoyntingFlux_data.txt` 续写时间积分状态。
- 最新推进（2026-05-21）：继续清 startup / I/O bridge 邻接尾项，已把 `particles.particles_nfiles` 补成正式 pass-through 条目，补清它在 WarpX 本地没有独立主 parser，而是由 `warpx.particle_io_nfiles` 经 `ParmParse("particles").add("particles_nfiles", ...)` 桥接给 AMReX 粒子 I/O；后续真实 consumer 落在粒子 `WritePlotFile(...) / Checkpoint(...)` 写盘链，而不是 WarpX 自己的 diagnostics instance-local parser。
- 最新推进（2026-05-21）：继续清 startup / particle-I/O pass-through 邻接尾项，已把 `particles.nreaders / nparts_per_read / datadigits_read / use_prepost` 从“读链三条、写链一条例外”再压到更细的时序边界，补清 `nreaders / nparts_per_read` 会在 `MaxReaders()/MaxParticlesPerRead()` 中首次读取后缓存并反复复用，`datadigits_read` 则会在每次 `ParticleContainer::Restart()` 开头单独 query 来解析旧版 `DATA_*` 文件名位数；相对地 `use_prepost` 先落成容器成员 `usePrePost`，随后只由 `CheckpointPre()/WriteBinaryParticleData()/CheckpointPost()` 复用同一批 `which/count/where/filePrefix/nParticlesAtLevelPrePost` 缓存向量做 header 汇总与零长度文件收尾。
- 最新推进（2026-05-21）：继续清 diagnostics / time-averaged 邻接条目，已把 `<diag>.time_average_mode` 从“累计缓冲总开关”再压到更细的实现边界，补清 `Diagnostics::ComputeAndPack()` 虽然仍会无条件对 `TimeAveraged` diagnostics 执行 `m_sum_mf_output += m_mf_output`，但非输出步累计 gate 目前只在 `dynamic_start` 分支 materialize；同时 `DoComputeAndPack()` 里唯一一次给 `fixed_start` 更新 `m_average_period_steps` 的语句还被嵌在外层 `Dynamic` 分支内部，对 `Static` 按当前控制流不可达，因此官方文档/头文件中的 `fixed_start` 语义当前强于真实 runtime control flow。
- 最新推进（2026-05-21）：继续清 diagnostics / time-averaged 邻接条目，已把 `<diag>.average_start_step` 从“fixed_start 起点键”再压到更细的 parser/flush 边界，补清 `ReadParameters()` 当前只显式拒绝 `0`，并没有把输入收紧成“严格正值”；同时 `Flush()` 在 `Static` 模式下仍会直接用 `m_average_period_steps` 做归一化，但当前控制流里给 `fixed_start` 计算这条步长的语句对 `Static` 不可达，因此 `fixed_start` 不只缺少独立非输出步累计 gate，连平均窗口长度的 stable materialization 也没有被当前实现证明。
- 最新推进（2026-05-21）：继续清 diagnostics / time-averaged 邻接条目，已把 `<diag>.average_period_steps` 从“dynamic_start 专用 period 输入”再压到更细的 fixed-start 残留耦合边界，补清它在 `fixed_start` 下虽然只会触发 warning “ignored”，但 `ReadParameters()` 并不会把 `m_average_period_steps` 清空；而 `Flush()` 在 `Static/Dynamic` 路径里仍会直接用这条成员值做归一化，因此当前实现还保留着一条“文案说 ignored、但成员值仍存活且可能被 flush 继续消费”的 fixed-start 残留耦合。
- 最新推进（2026-05-21）：继续清 diagnostics / time-averaged 邻接条目，已把 `<diag>.average_period_time` 从“dynamic_start 的时间制 companion”再压到更细的离散化时机边界，补清它在 `fixed_start` 下同样只会 warning “ignored”，但成员值不会被 parser 清空；真正把它离散化成 `m_average_period_steps` 的逻辑只存在于 `DerivedInitData()` 的 `dynamic_start` 分支，因此当前实现里保留的是一条“文案说 ignored、成员值仍存活、但只有 dynamic 路径才会把它 materialize 成 flush 会消费的整数步长”的半耦合状态。
- 最新推进（2026-05-21）：继续清 diagnostics / time-averaged 邻接条目，已把 `<diag>.time_average_mode / average_start_step / average_period_steps / average_period_time` 这一整簇再压成统一闭包，补清 `fixed_start` 当前共同落在同一条“文档语义强于真实 control-flow”的边界上：非输出步累计 gate 只在 `dynamic_start` materialize，`average_start_step` 主要仍是 parser 锚点，而两个 period companion 虽然都会 warning “ignored” 但成员值不会被清空；与此同时 static 路径没有稳定 control-flow 去重新 materialize 平均窗口长度，而 `Flush()` 仍会继续消费 `m_average_period_steps`。
- 最新推进（2026-05-21）：继续清 restart / diagnostics 邻接尾项，已把 `amr.restart` 从“restart 总分支 + reduced-diag 续写”的摘要压到更精确的 restart 非对称边界，补清 restart 不只跳过 fresh-run 专属的 `InitDiagnostics()/beforeInitEsolve/afterInitEsolve`、初始 space-charge field solve 和 `AddExternalFields(lev)`，改走 `afterInitatRestart`；还明确 `InitFromCheckpoint()` 会对 `BackTransformed` diagnostics 走专门的 buffer/tlab/snapshot 状态恢复链，而初始化收尾那次 `multi_diags->FilterComputePackFlush(istep[0]-1)` 仍只覆盖非 BTD full diagnostics，因此 BTD 在 restart 场景下是“专门恢复，不参加普通首帧补写”的独立分支。
- 最新推进（2026-05-21）：继续清 diagnostics 邻接 runtime gate，已把 `warpx.write_diagnostics_on_restart` 从“restart 后补一帧 diagnostics”的摘要压到更精确的初始化调度链，补清它不仅 gate `WarpXInitData.cpp` 中 restart 首帧写出，还把 `istep[0]-1` 作为真实时间语义传给 full/reduced diagnostics；其中 full diagnostics 继续走 `MultiDiagnostics::FilterComputePackFlush(...) -> Diagnostics::DoComputeAndPack/Flush(...)` 的正常判定链，但由于初始化收尾这次调用没有显式传 `BackTransform=true`，所以只会遍历非 BTD diagnostics，不会像主 step-loop 那样先单独跑一次 back-transformed 分支。更细一层是：BTD 在 restart 时并不是空操作，而是先在 `InitFromCheckpoint()` 中按 `getnumbuffers()` 走专门的 `InitDataBeforeRestart()/InitDataAfterRestart()` 状态恢复链，因此这条开关本身不会负责把 BTD flush 出去。相对地 reduced diagnostics 仍直接执行 `ComputeDiags(...) + WriteToFile(...)`，而且还要再过 `m_plot_rd != 0` gate 才会真的写出；同时这条开关对 fresh run 没有否决权。
- 最新推进（2026-05-21）：继续清 diagnostics 邻接 runtime gate，已把 `warpx.synchronize_velocity_for_diagnostics` 从“步尾前同步速度”的摘要压到更完整的运行链，补清它不仅 gate `WarpXEvolve.cpp` 中 diagnostics/end-of-loop 前的半步速度同步，还会在 `m_dt_update_interval.contains(step+1)` 命中时先于 `UpdateDtFromParticleSpeeds()` 触发；同时明确 `SynchronizeVelocityWithPosition()` 会依次执行 `FillBoundaryE/B`、必要的 averaged-field 边界更新、`UpdateAuxilaryData()`、`FillBoundaryAux(...)` 和各 level 的 `PushP(..., 0.5*dt, ..., MomentumPushType::Full)`。
- 最新推进（2026-05-21）：继续清 diagnostics instance-local 条目，已把 `<diag>.verbose` 补成正式参数行，补清它的默认链不是简单等于 `warpx.verbose`，而是 `Diagnostics.H` 里的 `m_verbose = 2` 先作为基线、再按显式给出的 `warpx.verbose` 覆盖、最后允许 `<diag>.verbose` 单独覆写；同时明确这条值会继续透传给 `FlushFormatPlotfile/OpenPMD/Checkpoint/Sensei/Ascent` 的 writer-side 日志，并在 `FullDiagnostics` 的 time-averaged 分支里控制额外 period 信息打印。
- 最新推进（2026-05-21）：继续清 reduced-diag 输出合同尾项，已把 `reduced_diags.path / extension / separator / precision` 压到更完整的文本 writer / openPMD 分流链，补清它们不仅进入 `ReducedDiags` 基类的建目录、restart 续写和 `WriteToFile()`，还会继续控制 `LoadBalanceCosts` 的 `.tmp` 重写与 `NaN` 补齐路径，并明确 `FieldProbe / LoadBalanceCosts` 当前绕开实例级 `precision` 覆盖，而 `ParticleHistogram2D / DifferentialLuminosity2D` 的 openPMD writer 也不消费 `extension / separator / precision` 这套文本输出合同。
- 最新推进（2026-05-21）：继续清 QED lookup-table 相邻尾项，已把 `qed_qs/qed_bw.lookup_table_mode` 与 `chi_min` 压到更完整的 engine 启动链，补清 `generate / load / builtin` 三分支不仅决定 wrapper 初始化方式，还会继续决定 generate 模式下各类 `tab_*` companion 参数读取、IO rank 二进制 table 生成与 `ReadAndBcastFile(...)` 广播；同时明确 `chi_min` 不只写入 wrapper 内部成员，还会作为 wrapper-side scalar 挂到 `build_evolve_functor()`、`get_minimum_chi_*()` 与普通 push / implicit push / photon push 的 optical-depth runtime gate 上，而不会进入 `build_phot_em_functor()` / `build_pair_functor()` 的 sampling table view。
- 最新推进（2026-05-21）：继续清 QED lookup-table companion 缺口，已把 `qed_qs/qed_bw` 的 `tab_*` 与 `save_table_in/load_table_from` 补成正式参数行，明确这些输入只在 `lookup_table_mode = generate/load` 时进入真实解析链，并继续决定两类 QED lookup table 的网格形状、IO rank 二进制写盘路径，以及 `ReadAndBcastFile(...)` 的全局广播源。
- 最新推进（2026-05-21）：继续清 QED 相邻尾项，已把 `qed_qs.photon_creation_energy_threshold` 与 `warpx.do_qed_schwinger` 压到更完整的 runtime 链，补清前者不是表初始化参数，而是在 `doQedQuantumSync()` 生成新 photon 后由 `cleanLowEnergyPhotons(...)` 执行的低能产物筛除阈值；同时明确后者不仅控制 `MultiParticleContainer::doQEDSchwinger()` 的早退，还绑定 `WarpXEvolve.cpp` 的每步调度、`maxLevel()==0`/`grid_type` 等实现边界，以及 `CheckQEDProductSpecies()` 的电子/正电子产物类型检查。
- 最新推进（2026-05-21）：继续清 startup / AMReX-owned pass-through 尾项，已把 `amr.blocking_factor / blocking_factor_x / blocking_factor_y / blocking_factor_z` 补成正式 grouped row，补清它们不仅在 `WarpXAMReXInit.cpp` 中做整数预解析，还会被 `warpx.numprocs` 的 startup workaround 强制改写、在 `RZ + PSATD` 路径下由 `CheckGriddingForRZSpectral()` 按 `n_cell` 重新构造，并继续进入 `PerformanceHints(...)` 与 `PML.cpp` 的分块/PML 告警边界。
- 最新推进（2026-05-21）：继续清 startup / AMReX-owned pass-through sibling 缺口，已把 `amr.max_grid_size_x / max_grid_size_y / max_grid_size_z` 补成正式 grouped row，补清它们不仅在 `WarpXAMReXInit.cpp` 中做整数预解析，还会在 `RZ + PSATD` 路径下被 `CheckGriddingForRZSpectral()` 真实重写，其中 `max_grid_size_x` 会按 `n_cell[0]` 和固定 refinement ratio 重建，而 `max_grid_size_y` 会按 `nprocs` 约束持续收缩。
- 最新推进（2026-05-21）：继续清低频 I/O 邻接缺口，已把 `warpx.usesingleread / usesinglewrite` 补成正式参数行，补清它们从 `WarpX.H` 默认值出发，经 `WarpX::ReadParameters()` 读取后，不是直接调用 `VisMF` setter，而是通过 `ParmParse("vismf").add(...)` 转接给 AMReX `VisMF` 命名空间，进而影响基于 `VisMF` 的 plotfile/checkpoint 单文件读写合同。

## 已完成记录

### 2026-05-13 初始项目建立

- [x] 检查 `PIC-tutor` 当前状态：目录为空，且不是 git 仓库。
- [x] 确认同级 `../warpx` 存在。
- [x] 只读扫描 WarpX 的核心资料入口：`Docs/source/`、`Source/`、`Examples/`、`Regression/`、`Tools/`、`Docs/source/refs.bib`。
- [x] 确认本地 WarpX 文献池第一批规模：`Docs/source/refs.bib` 有 251 条 BibTeX 入口。
- [x] 对照 DeepWiki 和 Zread 的解读结构，确定其只适合作为模块索引，不能替代源码/官方文档/论文。
- [x] 建立项目控制文件：`AGENTS.md`、`README.md`、`TODO.md`。
- [x] 建立初版总计划：`docs/master-plan.md`。
- [x] 建立论文阅读流程：`docs/paper-reading-workflow.md`。
- [x] 生成 `bibliography/warpx-refs.bib`。
- [x] 扩展 `references/` 开放 PDF 文献库第一批，并建立分类目录、下载脚本和书籍合法获取清单。

### 2026-05-14 粗草稿与计划升级

- [x] 建立 `docs/source-map.md`，记录第一批源码行号证据。
- [x] 建立 `docs/chapter-template.md`。
- [x] 建立 `manuscript/README.md` 和 10 个章节粗草稿，形成 Markdown-first v0.1。
- [x] 根据反馈确认 v0.1 太草率，只能作为粗目录草稿，不能作为正式书稿。
- [x] 建立新的最高优先级计划：`docs/warpx-full-code-reading-book-plan.md`。
- [x] 更新 `README.md`，说明后续以全源码精读计划为准。
- [x] 重写本 `TODO.md`，使其与新计划对齐。

### 2026-05-14 阶段 A 自动索引

- [x] 创建 `scripts/generate_stage_a_maps.py`，用于生成阶段 A 的四张索引表。
- [x] 生成 `docs/module-inventory.md`：覆盖 `Source/` 下 707 个目标源码/构建文件。
- [x] 生成 `docs/parameter-map.md`：覆盖 `Docs/source/usage/parameters.rst` 中 352 个 `pp:param` 参数。
- [x] 生成 `docs/example-regression-map.md`：覆盖 657 个 Examples 输入/脚本和 356 个 checksum benchmark。
- [x] 生成 `docs/literature-map.md`：覆盖 251 条 BibTeX 和 35 个本地 PDF。
- [x] 更新 `docs/source-map.md`，加入阶段 A 索引产物说明。

### 2026-05-14 阶段 C 主循环样章重写

- [x] 重新读取并记录主生命周期源码：`../warpx/Source/main.cpp`、`../warpx/Source/WarpX.H`、`../warpx/Source/WarpX.cpp`、`../warpx/Source/Initialization/WarpXInitData.cpp`、`../warpx/Source/Evolve/WarpXComputeDt.cpp`、`../warpx/Source/Evolve/WarpXEvolve.cpp`。
- [x] 建立 `notes/code-reading/evolve/`，保存主生命周期、PIC 时间层和 `Evolve` 源码证据表。
- [x] 重写 `manuscript/chapters/02-pic-loop.md`：从 Vlasov-Maxwell、宏粒子、形函数、离散连续性、leapfrog 时间层推到 WarpX 主循环结构。
- [x] 重写 `manuscript/chapters/03-warpx-evolve.md`：从 `main.cpp`、`WarpX` 单例、`ReadParameters()`、`InitData()`、`ComputeDt()` 讲到 `Evolve()`、`OneStep()`、`OneStep_nosub()`、`SyncCurrentAndRho()`、`PushParticlesandDeposit()`。
- [x] 明确下一层源码入口：`MultiParticleContainer::Evolve()`、`EvolveE/B/F/G`、`SyncCurrent()`、`SyncRho()`、PSATD 与 subcycling 路径。

### 2026-05-14 粒子推进与沉积样章重写

- [x] 重新读取并记录粒子主链源码：`../warpx/Source/Particles/MultiParticleContainer.cpp`、`../warpx/Source/Particles/PhysicalParticleContainer.cpp`、`../warpx/Source/Particles/WarpXParticleContainer.cpp`、`../warpx/Source/Particles/Pusher/PushSelector.H`、`../warpx/Source/Particles/Pusher/UpdateMomentumBoris.H`、`../warpx/Source/Particles/Pusher/UpdatePosition.H`。
- [x] 建立 `notes/code-reading/particles/`，保存粒子推进主链、pusher 分派和沉积入口证据衹。
- [x] 重写 `manuscript/chapters/04-particle-pushers.md`：从 Lorentz 方程、Boris 公式、pusher 分派讲到 `MultiParticleContainer::Evolve()`、`PhysicalParticleContainer::Evolve()` 和 `PushPX()`。
- [x] 重写 `manuscript/chapters/05-deposition-shapes.md`：从电荷/电流沉积和离散连续性讲到旧/新电荷、半步电流、`DepositCurrent()` / `DepositCharge()` 分派和 `SyncCurrentAndRho()`。
- [x] 精读并记录 `FieldGather.H`、`ShapeFactors.H`、`ChargeDeposition.H`、`CurrentDeposition.H` 的第一批 kernel 级源码证据。
- [x] 扩写 `manuscript/chapters/04-particle-pushers.md`：补入 `doGatherShapeN()` 运行时分派、模板 shape 选择、XZ/RZ gather 累加和坐标转换源码原文。
- [x] 扩写 `manuscript/chapters/05-deposition-shapes.md`：补入 0 到 4 阶 shape factor、电荷沉积、direct current、Esirkepov current 的源码原文和公式解释。
- [x] 精读 `UpdateMomentumVay.H` 与 `UpdateMomentumHigueraCary.H`，并回填第 4 章的源码原文和公式解释。

### 2026-05-14 源码原文讲解规范

- [x] 明确新增写作规则：讲解源码时必须把真实源码原文放入正文，不能只给路径和行号。
- [x] 更新 `docs/chapter-template.md`、`docs/warpx-full-code-reading-book-plan.md`、`README.md`，要求“源码块 + 行号 + 逐行/逐块解释”。
- [x] 回补已重写样章中的源码原文块：`02-pic-loop.md`、`03-warpx-evolve.md`、`04-particle-pushers.md`、`05-deposition-shapes.md`。

### 2026-05-14 全局源码精读框架

- [x] 重新盘点 `../warpx/Source` 顶层目录、二级/三级模块、构建边界和主要文件规模。
- [x] 确认 `Source` 约 712 个文件，`.H/.cpp` 主体约 562 个文件，最大模块为 `Particles`、`FieldSolver`、`Diagnostics`、`ablastr`。
- [x] 检查 `Source/Make.package`、`Particles/CMakeLists.txt`、`FieldSolver/CMakeLists.txt`，确认根层、粒子模块和场求解模块的构建入口。
- [x] 新建 `docs/warpx-source-reading-framework.md`，把全源码精读拆成 15 个阶段。
- [x] 更新 `README.md`、`TODO.md`、`docs/source-map.md`，把后续执行重心从局部模块扩写改为按全局框架推进。
- [x] 新建 `notes/code-reading/README.md` 总索引。
- [x] 为全部顶层模块建立 `notes/code-reading/<module>/README.md` 精读入口：root、initialization、evolve、particles、fieldsolver、boundary、parallelization、diagnostics、embedded-boundary、filter、laser、fluids、nonlinear-solvers、accelerator-lattice、python、utils、ablastr。
- [x] 统一 `evolve/README.md` 和 `particles/README.md` 的模块边界、核心问题、精读顺序和输出目标格式。

### 2026-05-14 阶段 1 Root / WarpX 主类状态启动

- [x] 继续人工阅读 `../warpx/Source/WarpX.H`：确认 `WarpX : public amrex::AmrCore`、单例接口、算法选择状态、边界状态、时间层、粒子/诊断/流体/PML/EB/solver 成员。
- [x] 继续人工阅读 `../warpx/Source/WarpX.cpp`：确认 `ReadParameters()` 的 solver、PML、filter、grid type、current centering、deposition/gather/pusher、PSATD/JRhom、load balance 和 particle shape 解析逻辑。
- [x] 继续人工阅读 `../warpx/Source/WarpX.cpp` 的 AMReX level 生命周期：`MakeNewLevelFromScratch()`、`ClearLevel()`、`AllocLevelData()` 和 `AllocInitMultiFab()`。
- [x] 继续人工阅读 `../warpx/Source/Fields.H`：确认 `FieldType` 命名体系、标量/矢量场分类和 `ArrayFieldTypes`。
- [x] 新建 `notes/code-reading/root/01-warpx-state-map.md`，形成主类状态图、参数解析图和 field registry 第一轮精读。
- [x] 新建 `notes/code-reading/root/02-construction-and-level-allocation.md`，解释 `MakeWarpX()`、`WarpX::WarpX()`、`AllocLevelData()`、`AllocLevelMFs()` 和 PSATD solver 分配的构造/level 生命周期差异。

### 2026-05-14 阶段 2 Initialization 启动

- [x] 人工阅读 `../warpx/Source/Initialization/WarpXInitData.cpp` 的 `InitData()`、`InitFromScratch()`、`InitPML()`、`PostRestart()`、`InitLevelData()`、`ComputeExternalFieldOnGridUsingParser_template()`、`CheckGuardCells()`。
- [x] 人工阅读 `../warpx/Source/Diagnostics/WarpXIO.cpp` 的 `InitFromCheckpoint()` header 恢复入口。
- [x] 新建 `notes/code-reading/initialization/00-init-callgraph.md`，记录 fresh run / restart 分叉、AMReX level 初始化、PML、外场、自洽初始场和 guard cell 检查。
- [x] 人工阅读 `../warpx/Source/Initialization/ExternalField.H/.cpp` 和 `WarpXInitData.cpp` 中 `LoadExternalFields()`、`ReadExternalFieldFromFile()`。
- [x] 新建 `notes/code-reading/initialization/01-external-fields.md`，区分 grid external field、particle external field、constant/parser/openPMD/Python 外场路径。
- [x] 人工阅读 `../warpx/Source/Initialization/PlasmaInjector.H/.cpp`、`InjectorPosition.H`、`InjectorDensity.H` 和 `Particles/ParticleCreation/DefaultInitialization.H`。
- [x] 新建 `notes/code-reading/initialization/02-plasma-injector.md`，建立 species 初始化、position/density/momentum/flux functor 和 runtime attribute 默认初始化总图。
- [x] 人工阅读 `../warpx/Source/Utils/SpeciesUtils.H/.cpp` 和 `../warpx/Source/Initialization/InjectorMomentum.H`。
- [x] 新建 `notes/code-reading/initialization/03-density-momentum-dispatch.md`，解释 species 质量/电荷、密度 profile、动量分布、Boltzmann/Juttner/parser 和 tagged union 分派。
- [x] 人工阅读 `../warpx/Source/Particles/ParticleCreation/AddParticles.cpp`、`AddPlasmaUtilities.H/.cpp`、`SmartCreate.H`、`DefaultInitialization.H` 和 `WarpXParticleContainer::AddNParticles()`。
- [x] 新建 `notes/code-reading/initialization/04-particle-creation-kernels.md`，解释 `AddParticles()`、`AddPlasma()`、`AddPlasmaFlux()`、体/面权重、boosted-frame 修正、RZ/RSPHERE 权重和 runtime 属性初始化。
- [x] 人工阅读 `../warpx/Source/Initialization/DivCleaner/ProjectionDivCleaner.H/.cpp`、`ExternalVectorPotential.cpp` 清理入口和官方 projection div cleaner 参数文档。
- [x] 新建 `notes/code-reading/initialization/05-projection-div-cleaner.md`，推导 projection cleaner 的 `∇²φ=-∇·F`、`F<-F+∇φ`，并区分初始化 projection cleaning 与演化阶段 `do_dive_cleaning/do_divb_cleaning`。
- [x] 人工阅读 `PlasmaInjector::setupGaussianBeam()`、`setupExternalFile()`、`PhysicalParticleContainer::AddGaussianBeam()`、`AddPlasmaFromFile()` 和官方 `gaussian_beam`/`external_file` 参数文档。
- [x] 新建 `notes/code-reading/initialization/06-gaussian-beam-openpmd-injection.md`，解释 Gaussian beam 的权重、cut、focusing、rotation、symmetrization，以及 openPMD 粒子文件的位置/动量/权重/质量/电荷读取和单位换算。
- [x] 新建正式书稿章节 `manuscript/chapters/03a-warpx-initialization.md`，把阶段 2 初始化精读主链回填到 manuscript 层。
- [x] 人工阅读 `TemperatureProperties.*`、`GetTemperature.*`、`VelocityProperties.*`、`GetVelocity.*` 和官方 Maxwell-Boltzmann/Juttner 参数文档。
- [x] 新建 `notes/code-reading/initialization/07-temperature-velocity-properties.md`，解释 `theta_distribution_type`、`beta_distribution_type`、`bulk_vel_dir` 和 Maxwellian/Juttner 初始化中的局域温度与漂移速度。

## 近期执行顺序

### 阶段 A：全源码索引与映射

- [x] 创建 `docs/module-inventory.md`，列出 `Source/` 下每个 `.H`、`.cpp`、`.py`、`CMakeLists.txt`、`Make.package` 文件。
- [x] 在 `docs/module-inventory.md` 中为每个文件标注：所属模块、物理主题、关键类/函数、是否需要逐行解读、对应章节、阅读状态。
- [x] 创建 `docs/parameter-map.md`，从 `Docs/source/usage/parameters.rst` 抽取参数名、说明、官方文档位置、源码解析位置、对应书稿章节。
- [x] 创建 `docs/example-regression-map.md`，把 `Examples/` 和 `Regression/Checksum/benchmarks_json/` 映射到物理模型、算法章节和验证用途。
- [x] 创建 `docs/literature-map.md`，把 `bibliography/warpx-refs.bib`、`references/` PDF 和后续 MinerU 笔记映射到章节。
- [x] 扩展 `docs/source-map.md`，从当前少量函数扩展为全模块源码地图的导航入口。
- [x] 人工复核 `docs/module-inventory.md` 中 `其他源码`、`待定` 和关键模块的章节归属。
  - 已清掉 `module-inventory` 中最后 3 个悬空条目：
    - `Source/Fields.H` 归并到 `WarpX 主类`
    - `Source/Make.WarpX`
    - `Source/Make.package`
    归并到 `构建系统`
  - `其他源码` 模块已清到 `0`，文件行中的 `待定` 章节归属也清到 `0`
  - 同时补入了“自动模块名 -> 15 个精读阶段”的人工合并总表，避免后续继续在自动模块名和框架阶段之间来回跳转
- [ ] 人工复核 `docs/parameter-map.md` 的全部初步源码命中，定位真实 `ParmParse` 解析函数并逐步清掉剩余旧计划编号尾项。
  - 本轮已先清理一批最上游高频族：
    - 无前缀运行控制
    - boost / startup
    - electrostatic / Poisson / self-fields / magnetostatic
    - boundary / PML / `eb_potential`
    - restart / verbosity / warning / AMReX debug-safe 输入
  - 随后又继续清理 `species / laser / diagnostics / collision-QED` 这层高频家族：
    - `particles.species_names`
    - `rigid_injected_species`
    - species 注入/分布/自场初始化
    - resampling / `do_temperature_deposition`
    - virtual photons / QED / Schwinger product species
    - `fluids.species_names`
    - `lasers.deposit_on_main_grid`
    - particle diagnostics species 过滤项
  - 本轮又继续清理 `load_balance + writer/diagnostics` 尾项：
    - `warpx.numprocs`
    - `algo.load_balance_*`
    - `costs_heuristic_*`
    - `split_high_density_boxes*`
    - diagnostics 顶层注册 / writer backend / particle-output filters
    - BTD / reduced diagnostics / async-I/O
  - 本轮继续把剩余旧式章节编号整批迁到当前书稿语义，覆盖：
    - runtime / startup
    - AMR / boundary
    - filter / deposition / pusher / solver
    - PSATD / hybrid / macroscopic
    - collision / QED
    - diagnostics 零散尾项
  - 当前 `parameter-map` 表内旧编号残留数已从 `314` 压到 `0`
  - 本轮开始把“初步源码命中”继续压到真实解析链，已细化一批 `WarpX::ReadParameters()` / `WarpXComputeDt()` 主控参数：
    - `warpx.random_seed`
    - `algo.evolve_scheme`
    - `warpx.break_signals` / `warpx.checkpoint_signals`
    - `warpx.cfl` / `warpx.const_dt` / `warpx.max_dt`
    - `warpx.use_filter`
    - `algo.current_deposition` / `algo.field_gathering` / `algo.particle_pusher` / `algo.maxwell_solver`
    - `psatd.nox/noy/noz` / `psatd.current_correction` / `psatd.JRhom`
    - `warpx.do_subcycling` / `warpx.override_sync_intervals`
    - `warpx.do_device_synchronize`
    - `warpx.sort_intervals`
    - `warpx.do_shared_mem_charge_deposition`
  - 本轮继续细化下一批 sub-parser / consumer 条目：
    - `hybrid_pic_model.elec_temp / n0_ref / gamma / n_floor / substeps`
    - `hybrid_pic_model.plasma_resistivity / plasma_hyper_resistivity`
    - `hybrid_pic_model.J[x/y/z]_external_grid_function`
    - `hybrid_pic_model.add_external_fields`
    - `external_vector_potential.fields / <field>.read_from_file / path / A*_external_grid_function / A_time_external_function`
    - `interpolation.galerkin_scheme`
  - 本轮又把 `external_vector_potential` 组里最短的几行压到真实 allocation/init/runtime consumer 粒度：
    - `do_diva_cleaning`
    - `fields`
    - `<field>.read_from_file`
    - `<field>.path`
    - `<field>.A[x/y/z]_external_grid_function(x,y,z)`
    - `A_time_external_*`
  - 已补清一个需要后续单独留意的源码/文档错位：
    - 文档名仍写 `external_vector_potential.<field>.A_time_external_grid_function(t)`
    - 但当前源码实际查询键是 `<field>.A_time_external_function(t)`
  - 本轮继续压 `hybrid_pic_model` 邻近 still-coarse 行，已细化：
    - `elec_temp / n0_ref / gamma`
    - `plasma_resistivity(rho,J)`
    - `plasma_hyper_resistivity(rho,B)`
    - `J[x/y/z]_external_grid_function(x,y,z,t)`
    - `n_floor`
    - `substeps`
    - `holmstrom_vacuum_region`
    - `add_external_fields`
  - 这批已补到真实 consumer 粒度：
    - `ElectronPressure::get_pressure(...)` 与 `hybrid_electron_pressure_fp`
    - `HybridPICSolveE(...)` 中的 resistive / hyper-resistive / low-density branches
    - `hybrid_current_fp_external` 的分配、初始化与从 Ampere 电流中扣除
    - `WarpX::HybridPICEvolveFields()` 的双半步 B-field subcycling 与 split external-field workflow
  - 本轮继续压 `macroscopic / interpolation` 邻近 still-coarse 行，已细化：
    - `algo.macroscopic_sigma_method`
    - `macroscopic.sigma/epsilon/mu_function(x,y,z)`
    - `macroscopic.sigma/epsilon/mu`
    - `interpolation.galerkin_scheme`
  - 这批已补到真实 consumer 粒度：
    - `MacroscopicEvolveE.cpp` 中 `LaxWendroffAlgo / BackwardEulerAlgo` 的二级分派
    - `sigma/epsilon/mu` 先 materialize 为材料属性 `MultiFab`，再进入 macroscopic E-push 的局域插值
    - `galerkin_scheme` 通过 `nodal_gather = !galerkin_interpolation` 影响 NCI Godfrey filter 初始化
  - 本轮继续压 `PSATD / cleaning` 邻近 still-coarse 行，已细化：
    - `warpx.do_dive_cleaning`
  - 这条已补到真实 consumer 粒度：
    - 会联动压低 `psatd.current_correction` 默认值
    - 会强制约束标准 PSATD 的 `psatd.update_with_rho`
    - 会抬高 `do_pml_dive_cleaning` 默认值
    - 并在显式 EM 主循环中真实进入 `EvolveF(...) + FillBoundaryF(...)` 链
    - `warpx.field_centering_* / current_centering_* / do_current_centering`
    - `warpx.do_dive_cleaning / do_initial_div_cleaning`
    - `warpx.projection_div_cleaner.rtol / atol`
    - `warpx.use_hybrid_QED / quantum_xi`
  - 本轮继续把 `Hybrid-QED` 相邻 mixed-consumer 条目压到真实 field-push 链：
    - `warpx.use_hybrid_QED`
    - `warpx.quantum_xi`
    - 已明确 `WarpX::ReadParameters()` 入口、`WarpXEvolve.cpp` 中 `Hybrid_QED_Push(dt)` 的插入 gate，以及 `m_quantum_xi_c2 -> WarpX_QED_Field_Pushers.cpp -> warpx_hybrid_QED_push(...)` 的系数传递链
  - 本轮继续把两条 `AMReX-owned pass-through` 邻接输入压到真实 startup/local-consumer 链：
    - `amr.n_cell`
    - `amr.max_grid_size`
    - 已明确 `WarpXAMReXInit.cpp` 的 `preparse_amrex_input_int_array(...)` 启动期整数预解析、`WarpXUtil.cpp` 的 RZ spectral 分块修正，以及 `WarpXInitData.cpp` 的 coarse-box / MPI 规模性能 warning 链
  - 本轮继续把 `amr.ref_ratio / ref_ratio_vect` 压到更具体的本地 consumer 链：
    - `amr.ref_ratio`
    - `amr.ref_ratio_vect`
    - 已补清 `GuardCellManager.cpp` 的 moving-window grow-cell 下界，以及 `PML.cpp` 中 `coarsen(ref_ratio)`、`ncell/ref_ratio[idim]` 与 `IntVect(...)/ref_ratio` 的 coarse/fine PML 缩并链
  - 本轮继续把 `amr.max_level` 压到更具体的本地 consumer 链：
    - `amr.max_level`
    - 已补清 `WarpXUtil.cpp` 里 `max_level > 0` 才进入 `fine_tag_lo/hi` refined-patch 几何链的条件分支，以及 `FieldEnergy / FieldMaximum / FieldMomentum / FieldProbe` 构造期用 `max_level + 1` 展开多层 reduced-diag 数据与 header 布局的 consumer 链
  - 本轮继续把两条 `amrex.*` startup 输入压到真实初始化链：
    - `amrex.the_arena_is_managed`
    - `amrex.omp_threads`
    - 已补清 `WarpXAMReXInit.cpp` 的 `overwrite_amrex_parser_defaults()` 覆写链，以及 `omp_threads` 在 `Source/Python/WarpX.cpp` 中通过 `amrex::OpenMP::set_num_threads(...)` 的 runtime setter
  - 本轮继续把 `moving_window_dir / moving_window_v` 压到更完整的运行链：
    - `warpx.moving_window_dir`
    - `warpx.moving_window_v`
    - 已补清 `WarpX.cpp` 的连续注入边界选择、`WarpXMovingWindow.cpp` 的窗口/注入位置更新、`WarpXUtil.cpp` 的 boost-frame 域换算，以及 `BTDiagnostics.cpp` 的 `z` 方向约束与 `dz_snapshots_lab -> dt_snapshots_lab` consumer 链
  - 本轮继续把 `warpx.numprocs` 压到真实 startup/runtime 链：
    - `warpx.numprocs`
    - 已补清 `WarpX.cpp` 的维数/MPI 乘积与 `RZ+PSATD` 输入约束、`WarpXAMReXInit.cpp` 的 `blocking_factor=1` workaround、`WarpX::PostProcessBaseGrids()` 的最粗层手工切块，以及 `FullDiagnostics.cpp` 对 `coarsening_ratio * numprocs` 的专门断言分支
  - 本轮继续把 `diagnostics.enable / diagnostics.diags_names` 压到真实 diagnostics 工厂链：
    - `diagnostics.enable`
    - `diagnostics.diags_names`
    - 已补清 `MultiDiagnostics::ReadParameters()` 的 `enable -> ndiags` gate、`MultiDiagnostics` 构造函数按 `diag_type` 的对象分派、`WarpX::InitData()/InitDiagnostics()` 的初始化与首步 flush 遍历，以及 `WarpX.cpp` 为 `checkpoint_signals` 兼容性检查重新扫描 `diags_names` 的邻接 consumer
  - 本轮继续把 `<diag_name>.diag_type` 压到真实 diagnostics 分派链：
    - `<diag_name>.diag_type`
    - 已补清 `MultiDiagnostics` 工厂在 `Full / TimeAveraged / BackTransformed / BoundaryScraping` 间的对象分派、`TimeAveraged` 仍落到 `FullDiagnostics` 的分支语义、`BoundaryScraping -> format=openpmd` 与 `BackTransformed` 的邻接约束，以及 `ParticleIO.cpp` 中“粒子附加 `phi/E/B` 只允许 Full” 的能力边界
  - 本轮继续把 `<diag_name>.format` 压到真实 writer/backend 分派链：
    - `<diag_name>.format`
    - 已补清 `BaseReadParameters()` 的 `m_format` 入口、`Full / BTD / BoundaryScraping` 三类 diagnostics 的允许集合差异、`checkpoint` 的全量转储兼容性合同，以及 `InitBaseData()` 中 `plotfile / checkpoint / ascent / catalyst / sensei / openpmd` 的实际 flush-backend 构造与 `sensei/ascent` 邻接 `FillBoundary` 路径
  - 本轮继续把 `<diag_name>.intervals` 压到真实 diagnostics 调度链：
    - `<diag_name>.intervals`
    - 已补清 `FullDiagnostics` 的强制 `getarr + IntervalsParser`、`BoundaryScraping` 的 `queryarr + {"0"}` 默认回退、`BTDiagnostics` 中 `intervals` 与 `num_snapshots_lab` 的二选一改写到 `BTDIntervalsParser`，以及 time-averaged diagnostics 通过 `nextContains()/previousContains()` 反推 averaging window 的 consumer 链
  - 本轮继续把 `<diag_name>.dump_last_timestep` 压到真实末步 flush 链：
    - `<diag_name>.dump_last_timestep`
    - 已补清 `Diagnostics::BaseReadParameters()` 的布尔入口与默认值、`MultiDiagnostics::FilterComputePackFlushLastTimestep()` 的 `force_flush=true` 分派，以及 `WarpXEvolve.cpp` 在最终步/中断退出时、`WarpX::HandleSignals()` 在 checkpoint signal 时复用这条尾部 flush 路径的触发关系
  - 本轮继续对 diagnostics 段做去重收口：
    - 删除与总表 `<diag_name>.intervals` 重复的 BTD 同名行
    - 保留“总表统一入口 + `num_snapshots_lab / dt_snapshots_lab / dz_snapshots_lab / buffer_size` 等 BTD 特化补充”的结构
  - 本轮继续把 `<diag_name>.openpmd_backend / openpmd_encoding` 压到真实 writer/backend 链：
    - `<diag_name>.openpmd_backend`
    - `<diag_name>.openpmd_encoding`
    - 已补清 `FlushFormatOpenPMD` 的 backend 默认值选择与 `pp_diag_name.add(...)` 回写、`WarpXOpenPMDPlot::GetFileName()` 的 `openpmd[_%0NT].<backend>` 文件模板、`Init()` 里的 `openPMD::Series(...)` 后端创建链，以及 `openpmd_encoding` 对 `fileBased/groupBased/variableBased` 文件布局、BTD 兼容性和 `m_Series->setIterationEncoding(...)` 的真实影响
  - 本轮继续把 `<diag_name>.adios2_operator.* / adios2_engine.*` 压到真实 openPMD backend-options 链：
    - `<diag_name>.adios2_operator.type / adios2_operator.parameters.*`
    - `<diag_name>.adios2_engine.type / adios2_engine.parameters.*`
    - 已补清 `FlushFormatOpenPMD` 对两组前缀 entries 的整体收集、`WarpXOpenPMD.cpp::getSeriesOptions()` 中 `"adios2" -> "dataset" -> "operators"` 与 `"engine"` JSON 子块的生成条件，以及这些 JSON 经 `m_OpenPMDoptions` 进入 `openPMD::Series(...)` 的真实落点
  - 本轮继续细化 diagnostics instance-local 的 still-coarse 条目：
    - `<diag_name>.particle_fields_to_plot / particle_fields_species`
    - `<diag_name>.particle_fields.<field_name>.do_average / (x,y,z,ux,uy,uz) / filter(...)`
    - `<diag_name>.plot_raw_fields / plot_raw_fields_guards / coarsening_ratio`
    - 已补清 `BaseReadParameters()` 对 particle-field parser/species/filter 的展开规则、`FullDiagnostics` 按 `field × species × level` 实例化 `ParticleReductionFunctor` 的路径、`ParticleReductionFunctor` 中加权求和/平均/过滤的真实沉积链，以及 raw-plotfile 支路和 BTD 禁止 coarsening 的格式边界
  - 本轮继续细化 diagnostics 输出路径与几何裁剪的相邻尾项：
    - `<diag_name>.file_prefix`
    - `<diag_name>.diag_lo / diag_hi`
    - 已补清 `BaseReadParameters()` 的默认前缀、`BTDiagnostics` 的重复读取、full/boundary-scraping/BTD 在 flush 时对 `m_file_prefix` 的不同派生方式，以及 `diag_lo/hi` 在 boosted moving-window 下的坐标换算、`InitBaseData()` restart 平移、`FullDiagnostics/BTDiagnostics` 的裁剪 box 链和 reduced-domain particle I/O 禁用边界
  - 本轮继续细化 diagnostics 命名合同与粒子输出 gate 的相邻尾项：
    - `<diag_name>.file_min_digits`
    - `<diag_name>.write_species`
    - 已补清 `BaseReadParameters()` 对 `file_min_digits` 的统一读取、各 flush backend 与 openPMD `SetStep()/GetFileName()` 对编号宽度的共同消费、BTD 用它派生 snapshot/buffer 子路径的链路，以及 `write_species` 在 `InitData()/InitDataAfterRestart()`、`FullDiagnostics::InitializeParticleBuffer()` 与 `BTDiagnostics::DerivedInitData()` 中对 species 回退、particle buffer 初始化和 checkpoint 例外的真实分支
  - 本轮继续细化 diagnostics 粒子对象构造与变量筛选的相邻尾项：
    - `<diag_name>.species`
    - `<diag_name>.<species_name>.variables`
    - 已补清 `FullDiagnostics / BTDiagnostics / BoundaryScrapingDiagnostics` 三条 species 默认回退与 `ParticleDiag` 构造分流、BTD 的 pinned `make_alike<>` buffer 绑定链，以及 `ParticleDiag` 中 `m_plot_flags` 与 `m_plot_phi/E/B` 的双路分派、RZ/RSPHERE 坐标重写和位置变量缺失 warning 的真实语义
  - 本轮继续细化 particle writer-side filter / extra-field 的相邻尾项：
    - `<diag_name>.<species_name>.additional_variables`
    - `<diag_name>.<species_name>.random_fraction / uniform_stride`
    - `<diag_name>.<species_name>.plot_filter_function(t,x,y,z,ux,uy,uz)`
    - 已补清 `additional_variables` 最终落到 `storePhiOnParticles()` / `storeFieldOnParticles()`、且只作用于通过筛选后的临时输出副本 `tmp`，`random_fraction / uniform_stride` 在 plotfile/openPMD 的 `copyParticles(...)` 里同时覆盖普通 `pc` 与 pinned/BTD `pinned_pc` 路径，以及 `plot_filter_function(...)` 在 writer 侧经 `compileParser<ParticleDiag::m_nvars>(...) -> ParserFilter`、按 `InputUnits::SI` 参与同一条筛选链，并发生在附加 `phi/E/B` 字段之前
  - 本轮继续细化 diagnostics/openPMD 相邻分流条目：
    - `<diag_name>.buffer_flush_limit_btd`
    - `<diag_name>.dump_rz_modes`
    - 已补清 `buffer_flush_limit_btd` 的默认值来自 `FlushFormatOpenPMD::m_NumAggBTDBufferToFlush = 5`、`WriteToFile()` 中按 `bufferID % threshold` 触发 `FlushBTDToDisk()` 的 writer-side durability/restart 路径，以及 `dump_rz_modes` 只作用于普通 full diagnostics 的 `AddRZModesToDiags(...)`，而 RZ + openPMD 会提前分流到 `InitializeFieldFunctorsRZopenPMD(...)` 的全-mode 初始化分支
  - 本轮继续细化 diagnostics 字段变量表与 particle-reduction 相邻条目：
    - `<diag_name>.fields_to_plot`
    - `<diag_name>.particle_fields_to_plot`
    - 已补清 `BaseReadParameters()` 中 `phi/A/F/G/proc_number/none` 的约束与重写、`m_varnames_fields -> m_varnames` 的统一变量表写入、`FullDiagnostics` 对 `CellCenterFunctor/RhoFunctor/TemperatureFunctor/JFunctor/...` 的实际分派，以及 `particle_fields_to_plot` 先展开 `<field>_<species>` 变量名再实例化 `ParticleReductionFunctor`、而 `BTDiagnostics` 对它是显式 `queryarr(...)` 后立刻 abort 的硬禁止边界
  - 本轮继续细化 particle-field companion 条目：
    - `<diag_name>.particle_fields_species`
    - `<diag_name>.particle_fields.<field_name>.do_average`
    - `<diag_name>.particle_fields.<field_name>(x,y,z,ux,uy,uz)`
    - `<diag_name>.particle_fields.<field_name>.filter(x,y,z,ux,uy,uz)`
    - 已补清 `particle_fields_species` 对 `m_pfield_species_index`、`m_varnames` 展开顺序和 `ParticleReductionFunctor::m_ispec` 的真实绑定关系，以及 map/filter parser 在 `ParticleReductionFunctor` 中被编译成 `ParserExecutor<6>` 后如何通过 `get_particle_position(...)`、`ux,uy,uz /= c`、`ParticleToMesh(...)` 与 `Coarsen(...)` 进入 cell-centered reduction 链，同时 `do_average` 决定是否额外构造 `ppc_mf` 作为归一化分母
  - 本轮继续细化 raw-field 输出相邻条目：
    - `<diag_name>.plot_raw_fields`
    - `<diag_name>.plot_raw_fields_guards`
    - 已补清它们真正只在 `FullDiagnostics::ReadParameters()` 中解析、BTD 只是 flush 时原样转发成员值；plotfile 路径会在 `plotfilename/raw_fields` 下写出 `aux/fp/cp`、`rho_fp`、`phi_fp`、时均场和 coarse-path 原始 MultiFab，而 openPMD 路径则对 raw 输出直接断言禁止
  - 本轮继续细化 reduced-diag 输出根目录条目：
    - `reduced_diags.path`
    - 已补清它在 `ReducedDiags` 基类里不仅控制目录创建、restart 续写判断和默认文本文件落点，还会被 `ParticleHistogram2D / DifferentialLuminosity2D` 等 openPMD reduced-diag 继续当作上游根目录，派生成 `m_path + m_rd_name + "/" + filename` 的实例级子目录布局
  - 本轮继续细化 reduced-diag 文本输出合同条目：
    - `reduced_diags.separator`
    - `reduced_diags.precision`
    - 已补清 `separator` 不仅控制基类与多种派生类的列拼接，还会被 `LoadBalanceCosts` 用来重新拆列既有文件；同时补清 `precision` 的实例级覆盖主要只稳定作用于走基类 `WriteToFile()` 的 reduced-diag，而 `FieldProbe / LoadBalanceCosts` 这类自定义 writer 目前仍部分绕开 `m_precision`
  - 本轮继续细化 reduced-diag histogram/species 相邻条目：
    - `<reduced_diags_name>.species`
    - `<reduced_diags_name>.bin_number / bin_min / bin_max`
    - `<reduced_diags_name>.histogram_function(t,x,y,z,ux,uy,uz)`
    - `<reduced_diags_name>.normalization`
    - 已补清 `species` 在 `ParticleHistogram / ParticleHistogram2D / BeamRelevant / DifferentialLuminosity` 四类 reduced-diag 中各自如何绑定真实粒子容器；同时补清 `bin_number/bin_min/bin_max` 如何共同决定 header bin center 与 `ComputeDiags()` 的实际分箱网格，以及 `histogram_function(...)` 和 `normalization` 如何进入逐粒子 parser 求值、原子累加与 MPI 归约后的归一化分支
  - 本轮继续细化 reduced-diag parser companion 条目：
    - `<reduced_diags_name>.filter_function(t,x,y,z,ux,uy,uz)`
    - `<reduced_diags_name>.histogram_function_abs/ord(t,x,y,z,ux,uy,uz,w)`
    - `<reduced_diags_name>.value_function/filter_function(t,x,y,z,ux,uy,uz,w)`
    - 已补清 `ParticleHistogram` 的 filter 如何在与主 histogram 相同的 `(t,x,y,z,ux/c,uy/c,uz/c)` 约定下先裁剪样本，再阻断后续 parser 求值与一维分箱；同时补清 `ParticleHistogram2D` 的 abs/ord axis parser 与 value/filter parser 如何进入 `GetPosition(...)`、`ux,uy,uz /= c`、二维落 bin 和 `Atomic::Add` 的 kernel 累加链
  - 本轮继续细化二维 reduced-diag 的 openPMD 输出合同：
    - `<reduced_diags_name>.openpmd_backend / file_min_digits`（`ParticleHistogram2D`）
    - `<reduced_diags_name>.openpmd_backend / file_min_digits`（`DifferentialLuminosity2D`）
    - 已补清两者都在实例构造函数中自行解析并回写默认 backend，而 `WriteToFile()` 会把输出组织到 `openpmd_%0NT.<backend>` 和 `series.iterations[step+1]`；同时补清 `ParticleHistogram2D` 会写入 `function_string_abs/ord` 轴信息，`DifferentialLuminosity2D` 会写入 `d2L_dE1_dE2`、`E1/E2` 轴和二维能量网格元数据
  - 本轮继续细化一批 Quantum Sync still-coarse 条目：
    - `qed_qs.photon_creation_energy_threshold`
    - `<species_name>.do_qed_quantum_sync`
    - 已补清前者默认值来自 `MultiParticleContainer.H` 的 `2*m_e*c^2`，并在 `doQedQuantumSync()` 里通过 `cleanLowEnergyPhotons(...)` 直接充当低能 photon 保留门槛；同时补清后者不仅在 species 构造期添加 `opticalDepthQSR`，还会驱动共享 `QuantumSynchrotronEngine` 绑定、`opticalDepthQSR` 默认初始化，以及普通 push / `ImplicitPushPX` / `doQedQuantumSync()` 三条运行链
  - 本轮继续细化 Quantum Sync product-species 与 classical RR 邻接条目：
    - `<species_name>.qed_quantum_sync_phot_product_species`
    - `<species_name>.do_classical_radiation_reaction`
    - 已补清前者会先经 `getSpeciesID(...)` 解析成 `m_qed_quantum_sync_phot_product`，再在 `doQedQuantumSync()` 中通过 `allcontainers[...]` 取到真实 photon product container；同时补清后者除 `PhysicalParticleContainer` 常规 push 外，还会切到 `RigidInjectedParticleContainer` 和 `PushSelector.H` 中的 `UpdateMomentumBorisWithRadiationReaction(...)` 分支
  - 本轮继续细化 QED lookup-table mode 条目：
    - `qed_qs.lookup_table_mode`
    - `qed_bw.lookup_table_mode`
    - 已补清两者在 `InitQuantumSync()` / `InitBreitWheeler()` 中都会分流到 `generate / load / builtin` 三条路径；其中 `generate` 会继续落到 `save_table_in`、`compute_lookup_tables()`、写盘和 `ReadAndBcastFile(...)` 广播，`load` 则走 `load_table_from` + 原始表广播，`builtin` 走 wrapper 内置低分辨率表初始化，最终都以 `are_lookup_tables_initialized()` 断言成功
  - 本轮继续细化 QED `chi_min` 门槛条目：
    - `qed_qs.chi_min`
    - `qed_bw.chi_min`
    - 已补清两者不仅进入 `init_lookup_tables_from_raw_data(...)` / `init_builtin_tables(...)` 和表生成路径，还会分别写入 `QuantumSyncEngineWrapper` / `BreitWheelerEngineWrapper` 的内部最小 `chi` 状态，并由运行期 `build_evolve_functor()` 直接消费；相对地，`build_phot_em_functor()` / `build_pair_functor()` 只携带 sampling table view，不再重复携带这条门槛，因此 `chi < chi_min` 时会在 optical-depth 推进阶段提前返回
  - 本轮继续细化 Schwinger gate 与 product-species 条目：
    - `warpx.do_qed_schwinger`
    - `qed_schwinger.ele_product_species`
    - `qed_schwinger.pos_product_species`
    - 已补清 `do_qed_schwinger` 会继续把电子/正电子产物 species 名映射成整数索引，并在 `doQEDSchwinger()` 中通过 `allcontainers[...]` 取到真实目标 container，再调用 `filterCreateTransformFromFAB(...)` 真正注入粒子对；同时补清 `ele/pos_product_species` 各自如何完成“名字 -> 索引 -> 容器落点”的 wiring
  - 本轮继续细化 Schwinger companion 条目：
    - `qed_schwinger.y_size`
    - `qed_schwinger.xmin/ymin/zmin/xmax/ymax/zmax`
    - `qed_schwinger.threshold_poisson_gaussian`
    - 已补清 `y_size` 不只进入 `doQEDSchwinger()` 的 `dx*dz*y_size` 体积计算，还会继续传进 `SchwingerTransformFunc{..., PIdx::w}`，把 2D 新生成电子/正电子权重写成 `total_weight/N/y_size`；同时补清 `xmin...xmax...` 会在 `ComputeSchwingerGlobalBox()` 中被转换成带 `lowest()/max()` 哨兵与 `ceil/floor` 边界规则的 level-0 全局掩膜 box，并在每个 tile 上与 cell-centered `box` 做相交裁剪；`threshold_poisson_gaussian` 则会经 `SchwingerFilterFunc` 继续传给 `getSchwingerProductionNumber(...)`，决定 Schwinger pair 采样走 Poisson 还是 Gaussian 分支
  - 本轮继续把 `start_moving_window_step / end_moving_window_step` 压到真实 runtime gate：
    - `warpx.start_moving_window_step`
    - `warpx.end_moving_window_step`
    - 已补清 `WarpX.H` 的 `moving_window_active(step)` 区间判定、`WarpXMovingWindow.cpp` 的启动/停止日志与位置更新链，以及 `BTDiagnostics.cpp` / `FieldProbe.cpp` 对窗口活动区间边界的 consumer
  - 本轮继续把 `fine_tag_lo/hi` 压到真实 refined-patch 链：
    - `warpx.fine_tag_lo/hi`
    - 已补清 `WarpX.cpp` 中与 `ref_patch_function(x,y,z)` 的互斥/覆盖规则、`WarpXUtil.cpp` 的 boosted-frame 坐标改写、`WarpX::ErrorEst()` 的静态打标 consumer，以及 `WarpXInitData.cpp` 在 RZ 下对 `fine_tag_lo[0] == 0` 的 PML 特例
  - 本轮继续细化一批 `AMReX-owned pass-through + diagnostics` 顶层 gate：
    - `amr.ref_ratio / ref_ratio_vect`
    - `diagnostics.enable / diagnostics.diags_names`
    - `<diag_name>.diag_type / format`
    - `<diag_name>.openpmd_backend / openpmd_encoding`
  - 本轮继续细化一批仍停留在手册原句的 QED / Schwinger 条目：
    - `qed_qs.photon_creation_energy_threshold`
    - `<species>.do_qed_quantum_sync / qed_quantum_sync_phot_product_species`
    - `<species>.do_qed_breit_wheeler / qed_breit_wheeler_{ele,pos}_product_species`
    - `qed_qs.lookup_table_mode / qed_bw.lookup_table_mode`
    - `qed_qs.chi_min / qed_bw.chi_min`
    - `warpx.do_qed_schwinger`
    - `qed_schwinger.{ele,pos}_product_species`
    - `qed_schwinger.threshold_poisson_gaussian`
  - 本轮继续细化同一簇剩余 still-coarse 条目：
    - `<species>.do_qed_virtual_photons`
    - `<species>.qed_virtual_photons_do_beam_size_effect`
    - `<species>.do_classical_radiation_reaction`
    - `qed_schwinger.y_size`
    - `qed_schwinger.xmin/ymin/zmin/xmax/ymax/zmax`
  - 本轮继续细化一批边界 / PML still-coarse 条目：
    - `boundary.reflect_all_velocities`
    - `boundary.verboncoeur_axis_correction`
    - `warpx.pml_ncell / pml_delta`
    - `do_similar_dm_pml`
    - `warpx.do_pml_in_domain / pml_has_particles / do_pml_j_damping`
    - `warpx.v_particle_pml`
    - `warpx.do_pml_dive_cleaning / do_pml_divb_cleaning`
    - `amrex.async_out / async_out_nfiles`
    - `amrex.abort_on_unused_inputs / use_profiler_syncs`
  - 本轮继续细化 diagnostics instance-local 条目：
    - `<diag_name>.<species_name>.additional_variables`
    - `<diag_name>.<species_name>.random_fraction / uniform_stride`
    - `<diag_name>.<species_name>.plot_filter_function(t,x,y,z,ux,uy,uz)`
    - `warpx.field_io_nfiles / particle_io_nfiles`
    - `warpx.reduced_diags_names`
    - `<reduced_diags_name>.type`
  - 本轮继续细化 time-averaged / BTD / reduced-diags 覆盖参数：
    - `<diag_name>.time_average_mode / average_period_steps / average_period_time / average_start_step`
    - `<diag_name>.num_snapshots_lab / dt_snapshots_lab / dz_snapshots_lab / buffer_size`
    - `<diag_name>.do_back_transformed_fields / do_back_transformed_particles`
    - `reduced_diags.path / extension / separator / precision`
  - 本轮继续细化 diagnostics instance-local 的 still-coarse 条目：
    - `<diag_name>.plot_raw_fields / plot_raw_fields_guards`
    - `<diag_name>.coarsening_ratio`
    - `<diag_name>.file_prefix / file_min_digits`
    - `<diag_name>.diag_lo / diag_hi`
    - `<diag_name>.write_species / species`
    - `<diag_name>.<species_name>.variables`
  - 本轮继续细化 particle-field / reduced-diags 的 still-coarse 条目：
    - `<diag_name>.particle_fields_to_plot / particle_fields_species`
    - `<diag_name>.particle_fields.<field_name>.do_average`
    - `<diag_name>.particle_fields.<field_name>(x,y,z,ux,uy,uz)`
    - `<diag_name>.particle_fields.<field_name>.filter(x,y,z,ux,uy,uz)`
    - `reduced_diags.intervals`
  - 本轮继续细化 openPMD / I/O 邻接尾项：
    - `<diag_name>.adios2_operator.parameters.*`
    - `<diag_name>.adios2_engine.type / adios2_engine.parameters.*`
    - `<diag_name>.dump_rz_modes`
    - `warpx.mffile_nstreams`
  - 本轮继续细化 diagnostics 调度与 SENSEI 邻接尾项：
    - `<diag_name>.intervals`
    - `<diag_name>.dump_last_timestep`
    - `<diag_name>.sensei_config`
    - `<diag_name>.sensei_pin_mesh`
  - 本轮继续细化 diagnostics 邻接运行时开关：
    - `warpx.synchronize_velocity_for_diagnostics`
    - `warpx.write_diagnostics_on_restart`
  - 本轮继续细化 BTD snapshot / buffer 相邻条目：
    - `<diag_name>.dt_snapshots_lab`
    - `<diag_name>.dz_snapshots_lab`
    - `<diag_name>.buffer_size`
    - `<diag_name>.do_back_transformed_particles`
  - 本轮继续细化 reduced-diags 文本输出合同：
    - `reduced_diags.path`
    - `reduced_diags.extension`
    - `reduced_diags.separator`
    - `reduced_diags.precision`
  - 本轮继续细化 startup / verbosity 邻接条目：
    - `warpx.limit_verbose_step`
    - `warpx.always_warn_immediately`
    - `warpx.abort_on_warning_threshold`
    - `warpx.serialize_initial_conditions`
  - 本轮继续细化 parallelization 邻接调试开关：
    - `warpx.safe_guard_cells`
    - `ablastr.fillboundary_always_sync`
  - 本轮继续细化 diagnostics 尾项：
    - `<diag_name>.buffer_flush_limit_btd`
    - `<diag_name>.adios2_operator.type`
    - `<diag_name>.fields_to_plot`
  - 本轮继续细化 species/runtime 与 load-balance / mirror / 外场初始化条目：
    - `particles.species_names`
    - `particles.use_fdtd_nci_corr`
    - `particles.rigid_injected_species`
    - `<species>.injection_style / do_continuous_injection`
    - `<species>.density_min / density_max`
    - `<species>.do_not_deposit / do_not_gather / do_not_push`
    - `algo.load_balance_intervals / load_balance_efficiency_ratio_threshold`
    - `algo.load_balance_with_sfc / load_balance_knapsack_factor`
    - `algo.load_balance_costs_update / costs_heuristic_particles_wt / costs_heuristic_cells_wt`
    - `warpx.do_dynamic_scheduling`
    - `warpx.roundrobin_sfc`
    - `warpx.split_high_density_boxes / threshold / min_box_size`
    - `warpx.num_mirrors / mirror_z / mirror_z_width / mirror_z_npoints`
    - `warpx.B_ext_grid_init_style`
  - 本轮继续细化粒子初始化 still-coarse 条目：
    - `particle_thermalizer.species`
    - `particles.do_tiling`
    - `<species>.species_type / charge / mass`
    - `<species>.profile / flux_profile`
    - `particles.E/B_ext_particle_init_style`
  - 本轮继续细化 AMReX-owned / fluid / laser / external-grid still-coarse 条目：
    - `amr.max_grid_size`
    - `fluids.species_names`
    - `lasers.deposit_on_main_grid`
    - `warpx.E_ext_grid_init_style`
    - `warpx.E/B_external_grid`
  - 本轮继续细化 external-field / fluid 邻接 still-coarse 条目：
    - `warpx.maxlevel_extEMfield_init`
    - `<fluid_species_name>.E/B_ext_init_style`
  - 本轮继续细化 lattice / collision still-coarse 条目：
    - `lattice.elements / lattice.reverse / <element_name>.type`
    - `collisions.collision_names`
    - `<collision_name>.type / species / product_species`
    - `<collision_name>.ndt_supercycle / ndt_subcycle`
  - 本轮继续细化 pairwise-Coulomb 邻接条目：
    - `<collision_name>.CoulombLog`
    - `<collision_name>.use_global_debye_length`
  - 本轮继续细化 binary-event / background-collision still-coarse 条目：
    - `<collision_name>.event_multiplier`
    - `<collision_name>.probability_threshold / probability_target_value`
      - 已压实为 `SingleLinearComptonCollisionEvent / SingleLinearBreitWheelerCollisionEvent / SingleNuclearFusionEvent` 共用的高概率事件重标定链：`threshold` 触发倍率回退，`target_value` 反解新的 `event_multiplier_eff`，产物权重按 `w_min / event_multiplier_eff` 写回
    - `<collision_name>.background_density / background_temperature`
      - 已补清 `BackgroundMCC` 与 `BackgroundStopping` 的 parser lifecycle 不对称：前者还受 `max_background_density` 概率上界链约束，后者构造期即 `compile<4>()` 并直接喂给 electron/ion stopping kernel
    - `<collision_name>.background_mass / background_charge_state / background_type`
      - 已补清 `background_mass` 在 `BackgroundMCC` 里会被 ionization 次级 species 延迟改写，而 `background_type` 会把 stopping 路径硬分成 electron/ion 两套 slowing-down 公式
  - 本轮继续细化 background_mcc / dsmc still-coarse 条目：
    - `<collision_name>.scattering_processes`
      - 已补清 `BackgroundMCC` 会把 ionization 从普通散射列表拆到独立执行链，而 `DSMC` 当前还带有“禁用 excitation/forward、且最多一个会产生新 species 的反应”的硬 gate
    - `<collision_name>.<scattering_process>_cross_section`
      - 已补清它不是单纯文件路径，而是 `ScatteringProcess` 表驱动输入：一边喂 `BackgroundMCC` 的 `m_nu_max` 上界扫描，一边喂 DSMC 的逐 pair 通道选择
    - `<collision_name>.<scattering_process>_energy`
      - 已补清它会随过程类型分叉，并继续落到散射能量扣减或产物创建链
    - `<collision_name>.ionization_species`
      - 已补清它不只绑定 secondary 名字，还会把 `BackgroundMCC` 扩成双容器路径，并锁定 `doBackgroundIonization()` 的 `SmartCopy(species1 -> species2)` 与 thermal-transform 质量尺度
    - `<collision_name>.ionization_target_species`
      - 已补清这条值先在 `BinaryCollision` 构造期重排 incident species 顺序，再锁定 DSMC ionization 的 4-slot product 语义
  - 本轮继续细化 nuclearfusion / pairwise-Coulomb correction still-coarse 条目：
    - `<collision_name>.scattering_angle_model`
    - `collisions.correct_energy_momentum`
      - 已补清它不只打开 correction pass，还锁定 pre-collision 备份来源、same-species 单边修正 vs two-species 双边修正，以及失败时的一边/两边整 cell 回滚策略
    - `collisions.energy_fraction / energy_fraction_max`
      - 已补清它们不是普通比例参数，而是 `ModifyEnergyPairwise(...)` 的基础步幅与最大护栏，决定逐对能量修正能否完成
    - `collisions.beta_weight_exponent`
      - 已补清它先作用在 correction pass 前半段的残余动量回填，而不是直接作用在 `ModifyEnergyPairwise(...)`
    - `collisions.energy_correction_sort_by_weight`
      - 已补清它只改变进入能量修正阶段前的 cell-local 索引顺序，并会影响 correction 成功率；失败时整 cell 会回滚
  - 本轮继续细化 pulsed_decay / bremsstrahlung still-coarse 条目：
    - `<collision_name>.fixed_product_weight`
      - 已补清它不只设产物权重，还控制按 cell 的随机离散、超额回退和 `remove_weight_from_colliding_particle(...)` 扣权链
    - `<collision_name>.productA_temperature_eV / productB_temperature_eV`
      - 已补清它们只在 `SmartCopy` 复制 parent 基态后，对 product-A/B 三轴动量叠加各向异性 thermal broadening
    - `<collision_name>.create_photons / koT1_cut`
      - 已补清 `create_photons=0` 只关闭 photon 物化，不会阻止 parent 动量更新；`koT1_cut` 同时控制零截面返回、默认预积分表复用和局域 plasma cutoff 触发的运行时重积分
    - `<collision_name>.decay_rate(x,y,z,t)`
    - `<collision_name>.fixed_product_weight`
    - `<collision_name>.productA_temperature_eV / productB_temperature_eV`
    - `<collision_name>.Z / multiplier / create_photons / koT1_cut`
  - 本轮继续细化 collision placement / filter / particle-shape / implicit-crossing / EM-medium still-coarse 条目：
    - `collisions.split_momentum_push`
    - `warpx.filter_npass_each_dir / use_filter_compensation`
    - `algo.charge_deposition`
    - `algo.particle_shape`
    - `particles.max_grid_crossings`
    - `algo.em_solver_medium`
  - 本轮继续细化 psatd runtime-mode still-coarse 条目：
    - `psatd.periodic_single_box_fft`
    - `psatd.update_with_rho`
    - `psatd.v_galilean / use_default_v_galilean`
    - `psatd.v_comoving`
    - `psatd.do_time_averaging`
  - 本轮继续细化 sorting / shared-memory deposition still-coarse 条目：
    - `warpx.sort_particles_for_deposition`
    - `warpx.sort_idx_type`
    - `warpx.sort_bin_size`
    - `warpx.do_shared_mem_current_deposition`
    - `warpx.shared_tilesize`
    - `warpx.shared_mem_current_tpb`
  - 本轮继续细化 `grid_type + field/pusher/solver + psatd guard` mixed-consumer 条目：
    - `warpx.grid_type`
    - `algo.field_gathering`
    - `algo.particle_pusher`
    - `algo.maxwell_solver`
    - `psatd.nx/ny/nz_guard`
  - 本轮继续细化 `boundary potential + injection bounds + field ionization` still-coarse 条目：
    - `boundary.potential_lo/hi_x/y/z`
    - `<species>.xmin/ymin/zmin/xmax/ymax/zmax`
    - `<species>.do_field_ionization`
  - 本轮继续细化 `rigid injection + backward propagation + splitting + boundary buffer` still-coarse 条目：
    - `<species>.zinject_plane`
    - `<species>.rigid_advance`
    - `<species>.do_backward_propagation`
    - `<species>.split_type`
    - `<species>.save_particles_at_xlo/ylo/zlo/xhi/yhi/zhi/eb`
  - 本轮继续细化 `user attributes + ionization companion parameters` still-coarse 条目：
    - `<species>.addIntegerAttributes`
    - `<species>.addRealAttributes`
    - `<species>.do_adk_correction`
    - `<species>.physical_element`
    - `<species>.ionization_product_species`
    - `<species>.ionization_initial_level`
    - 已补清 `addIntegerAttributes / addRealAttributes` 不只在 `PhysicalParticleContainer` 构造期安装 parser 并扩展 SoA runtime components，还会在 `DefaultInitialization.H` 中经 `getUser{Int,Real}Attribs()`、`getUser{Int,Real}AttribParser()` 与 `compile<7>()` 重新求值并写入新粒子；同时补清 `do_adk_correction` 会加载 Hydrogen correction factors 并一路传进 `IonizationFilterFunc`，`physical_element` 会驱动 atomic-number / ionization-energy / ADK-prefactor 表装载并约束修正边界，`ionization_product_species` 会经 `mapSpeciesProduct() -> CheckIonizationProductSpecies() -> doFieldIonization()` 绑定到真实 product container，而 `ionization_initial_level` 会先建立 `ionizationLevel` runtime int component，再在初始化与 ADK 事件链中持续充当 charge-state 状态
  - 本轮继续细化 `momentum-distribution companion` still-coarse 条目：
    - `<species>.theta_distribution_type`
    - `<species>.beta_distribution_type`
    - `<species>.radial_numpercell_power`
    - 已补清 `theta_distribution_type / beta_distribution_type` 并不是孤立 parser 项，而是只在 `SpeciesUtils::parseMomentum()` 进入 `maxwell_boltzmann / maxwell_juttner` 分支时才通过 `TemperatureProperties / VelocityProperties` 进入真实解析链；随后它们会分别经 `GetTemperature / GetVelocity` 交给 `InjectorMomentumBoltzmann / InjectorMomentumJuttner`，从而定义热平衡注入链里的温度与 bulk drift 取值模式
  - 本轮继续细化 `momentum-distribution main entry + resampling` still-coarse 条目：
    - `<species>.momentum_distribution_type`
    - `<species>.do_resampling`
    - `<species>.resampling_algorithm`
    - `<species>.resampling_trigger_intervals`
    - 已补清 `momentum_distribution_type` 的真正上游调用者是 `PlasmaInjector` 在 `gaussian_beam / nrandompercell / nfluxpercell / nuniformpercell` 构造期对 `SpeciesUtils::parseMomentum(...)` 的统一调用；同时明确其会继续分派到 `InjectorMomentumConstant/Gaussian/GaussianFlux/Uniform/Parser/Boltzmann/Juttner` 等对象，其中 `gaussianflux` 额外绑定 `flux_normal_axis / flux_direction`
    - 已补清 `do_resampling` 会继续走 `WarpXEvolve -> MultiParticleContainer::doResampling() -> PhysicalParticleContainer::resample()` 的全局同步与 tile-level 执行链，`resampling_algorithm` 会分叉到 `LevelingThinning` 与 `VelocityCoincidenceThinning` 两种完全不同的 cell kernel，而 `resampling_trigger_intervals` 则会与 `resampling_trigger_max_avg_ppc` 和由 `boxArray.numPts()` 汇总得到的全局 `avg_ppc` 条件共同组成 trigger 判定
  - 本轮继续细化 `resampling thresholds` still-coarse 条目：
    - `<species>.resampling_min_ppc`
    - `<species>.resampling_trigger_max_avg_ppc`
    - `<species>.resampling_trigger_intervals`
    - 已补清 `resampling_min_ppc` 在 `LevelingThinning / VelocityCoincidenceThinning` 两个算法里都会先裁掉 `cell_numparts < min_ppc` 的 cell，因此它是共享的 per-cell early-return gate
    - 已补清 `resampling_trigger_max_avg_ppc` 不是孤立阈值，而是经 `PhysicalParticleContainer::resample()` 的全局粒子数同步后，与 `boxArray.numPts()` 汇总出的 `avg_ppc` 一起进入 `ResamplingTrigger::triggered(...)` 的 step-loop 激活条件
  - 本轮继续细化 `resampling algorithm-specific companions`：
    - `<species>.resampling_algorithm_target_ratio`
    - `<species>.resampling_algorithm_target_weight`
    - `<species>.resampling_algorithm_velocity_grid_type`
    - `<species>.resampling_algorithm_delta_ur / n_theta / n_phi / delta_u`
    - 已补清 `LevelingThinning` 中 `target_ratio` 会直接定义 `level_weight = average_weight * target_ratio` 的 thinning 门槛；`VelocityCoincidenceThinning` 中 `target_weight` 会映射成 `cluster_weight` 上界，而 `velocity_grid_type` 与 `delta_ur / n_theta / n_phi / delta_u` 会继续决定 momentum-bin 的 spherical/cartesian 离散方式、bin 尺度和 cluster 语义
  - 本轮继续细化 `temperature-deposition + diagnostics/openPMD` still-coarse 条目：
    - `<species>.do_temperature_deposition`
    - 已补清 `do_temperature_deposition` 不只是在 `PhysicalParticleContainer` 构造期挂上 `T_<species>` 三方向场和 `VarianceAccumulationBuffer`，还会继续进入 `MultiParticleContainer::DepositTemperatures() -> AccumulateVelocitiesAndComputeTemperature()` 的双遍 variance deposition 链：第一遍沉积后先对 `n/w/vbar` 做 boundary sum，默认 `DOUBLE_PASS` 下再清空 `w2` 做第二遍沉积并继续对 `w2` 做 guard-cell 求和，最后按 cell 归一化方差、乘 `mass/k_B` 换算成 Kelvin，并经 `ConvertVarianceToTemperatureAndFilter(..., WarpX::use_filter)` 收口；同时补清 diagnostics 侧不是直接写出原始 `T_<species>` MultiFab，而是通过 `TemperatureFunctor -> pc.GetAverageNGPTemperature(m_lev)` 二次取值后再 coarsen 到输出网格
    - `buffer_flush_limit_btd / adios2_operator.type / fields_to_plot` 已在更早的 diagnostics/openPMD 批次压实，本处不再重复保留为同轮 still-coarse 子项
  - 本轮继续细化 `laser common-entry` still-coarse 条目：
    - `lasers.names`
    - `<laser>.e_max / a0 / wavelength / profile`
    - 已补清 `lasers.names` 会在 `WarpX::ReadParameters()` 中触发 laser 相关全局路径，并在 `MultiParticleContainer` 中扩展 `allcontainers`、逐个实例化 `LaserParticleContainer`、回绑 `deposit_on_main_grid`；同时补清 `<laser>.e_max / a0 / wavelength / profile` 会在 `LaserParticleContainer` 构造期汇合到 `CommonLaserParameters` 与 `laser_profiles_dictionary` 工厂，施加 `e_max xor a0`、正波长与零振幅禁用边界，再统一进入 `ILaserProfile::init(...)` 和运行期 `update() -> fill_amplitude() -> update_laser_particle()` 主链
  - 本轮继续细化 `laser plane-geometry` still-coarse 条目：
    - `<laser>.position / polarization / direction`
    - 已补清这组三维平面几何参数不只在 `LaserParticleContainer` 构造期完成长度检查、归一化和正交约束，还会继续进入 `InitData()` 的 `Transform/InverseTransform`、注入盒与激光平面的相交裁剪、天线宏粒子平面铺设，以及“整片天线完全在 simulation box 外时记录 warning 并禁用该 laser”的分支
  - 本轮继续细化 `gaussian laser profile` still-coarse 条目：
    - `<laser>.profile_t_peak / profile_duration / profile_waist / profile_focal_distance`
    - `<laser>.phi0 / zeta / beta / phi2`
    - 已补清这组 Gaussian 主参数并不只停留在 `GaussianLaserProfile::init(...)`：`profile_t_peak / phi0` 会直接进入 `oscillation_phase`，`duration` 进入 `inv_tau2 -> stretch_factor / stc_exponent`，`waist / focal_distance` 进入 `diffract_factor / inv_complex_waist_2 / exp_argument`，`stc_direction` 则通过 `theta_stc` 把 `(Xp,Yp)` 投影到时空耦合方向；因此它们共同定义的是逐粒子 `fill_amplitude()` kernel，而不是孤立 profile 元数据
  - 本轮继续细化 `gaussian STC + continuous-injection` still-coarse 条目：
    - `<laser>.stc_direction`
    - `<laser>.do_continuous_injection / min_particles_per_mode`
    - 已补清 `zeta / beta / phi2` 会继续进入 `GaussianLaserProfile::fill_amplitude()` 的 `stretch_factor`、逐粒子 `stc_exponent` 和 chirp 虚部修正，而不是只停留在 init 阶段；同时补清 `do_continuous_injection` 会打开 `m_updated_position` 的 boosted-frame 回推与“首次入域才调用一次 InitData()”的 gate，`min_particles_per_mode` 则直接控制 RZ 下 `n_spokes = (n_modes-1) * min_particles_per_mode` 的 spoke 数和权重归一化
  - 本轮继续细化 `from_file + parse_field_function` still-coarse 条目：
    - `<laser>.field_function(X,Y,t)`
    - `<laser>.binary_file_name / lasy_file_name`
    - `<laser>.time_chunk_size / delay`
    - 已补清 `field_function(X,Y,t)` 的 profile 运行期几乎完全由 `fill_amplitude()` 决定，`update()` 本身是 no-op；同时补清 `binary/lasy` 两条 backend 不只在 init 期选源并预读首块，还会继续进入 `FromFileLaserProfile::update()` 的时间块滑窗加载，以及 `fill_amplitude()` 的“越界直接清零、有效时再分流到 binary/cartesian/cylindrical 插值”链，`time_chunk_size / delay` 则分别控制缓存窗口大小和有效发射时间平移
  - 本轮继续细化 `self_fields + magnetostatic solver` still-coarse 条目：
    - `warpx.self_fields_required_precision / absolute_tolerance / max_iters / verbosity`
    - `warpx.magnetostatic_solver_required_precision / absolute_tolerance / max_iters / verbosity`
  - 本轮继续细化 `species initial self-fields` still-coarse 条目：
    - `<species>.initialize_self_fields`
    - `<species>.self_fields_required_precision / self_fields_absolute_tolerance / self_fields_max_iters / self_fields_verbosity`
    - 已补清这组参数不只落在 `PhysicalParticleContainer` 构造函数的 species 私有状态入口，还会先参与 `WarpXInitData.cpp` 里的 electrostatic 初始化触发判断；并明确 species 级 `self_fields_*` override 只进入 `RelativisticExplicitES::AddSpaceChargeField(...)` 的 per-species `computePhi(...)` 链，`AddBoundaryField(...)` 仍使用 solver 级默认值，其中 `self_fields_verbosity` 只覆盖该 species 初始 Poisson 求解的底层日志级别
  - 本轮继续细化 `random-theta + AMR splitting gate` still-coarse 条目：
    - `<species>.random_theta`
    - `<species>.do_splitting`
  - 本轮继续细化 `NUniformPerCell` 入口条目：
    - `<species>.num_particles_per_cell_each_dim`
  - 本轮继续细化 `AMR coarse-fine current buffer` 条目：
    - `warpx.n_current_deposition_buffer`
  - 本轮继续细化 `AMR/moving-window` 相邻条目：
    - `warpx.refine_plasma`
    - `warpx.n_field_gather_buffer`
  - 本轮继续细化 `AMR communication + coarse-grid gather` 相邻条目：
    - `warpx.do_single_precision_comms`
    - `particles.gather_from_main_grid`
  - 本轮继续细化 `boundary` 相邻条目：
    - `boundary.field_lo/hi`
    - `boundary.particle_lo/hi`
    - 已补清 `geometry.is_periodic` 回写，以及 `WarpX.cpp / WarpXInitData.cpp / WarpX_PEC.cpp` 的 runtime consumer
  - 本轮继续细化 `geometry / AMReX startup` 相邻条目：
    - `geometry.is_periodic`
    - 已补清它不是公开用户输入，而是 `WarpXAMReXInit.cpp` 由 field/particle boundary 反推得到的内部 geometry 元数据；若用户显式给出只会 warning
    - 已补清 `pp_geometry.addarr("is_periodic", ...)` 回写给 AMReX geometry，以及 `Geom(...).isPeriodic()/periodicity()` 在 moving-window 非周期方向约束、RZ/RCYLINDER 径向非周期约束和 `FillBoundary/OwnerMask` 通信路径中的 consumer
  - 本轮继续细化 `AMReX-owned pass-through` 相邻条目：
    - `amr.n_cell`
    - 已补清 `parse_geometry_input()` 里 `preparse_amrex_input_int_array("n_cell", true)` 的 `remove + addarr` 数值化回写，以及它专门为 `warpx_job_info`/yt 保留纯整数输出的边界
    - 已补清 `CheckGriddingForRZSpectral()` 在 `RZ + PSATD` 下如何直接用 `n_cell[0]` 重建 `blocking_factor_x / max_grid_size_x`，并用 `n_cell[1]` 经 `8*NProcs()` 断言与两条 `while (n_cell[1] < nprocs*...)` 循环继续收缩 `blocking_factor_y / max_grid_size_y`
  - 本轮继续细化 `AMR ratio` 相邻条目：
    - `amr.ref_ratio_vect`
    - 已补清它不只在 `GuardCellManager.cpp` 和 `PML.cpp` 中消费，还会继续进入 `WarpXMovingWindow.cpp` 的 `num_shift *= refRatio(lev-1)[dir]` level-shift 放大链
    - 已补清 `WarpX_PEC.cpp` 对 coarse patch `domain_box.coarsen(ref_ratios[lev-1])` 的整向量 consumer，以及 `WarpXComputeDt.cpp` 在 subcycling 下只取 `refRatio(lev)[0]` 回推 coarse-level `dt` 的非对称边界
  - 本轮继续细化 `AMR ratio` 邻接 companion：
    - `amr.ref_ratio`
    - 已补清它作为各向同性 shorthand，不只会进入 `GuardCellManager.cpp / WarpXMovingWindow.cpp` 的窗口方向 grow-cell 与 shift 链，也会继续作为完整 `IntVect` 进入 `PML.cpp / WarpX_PEC.cpp / RelativisticExplicitES.cpp` 的 coarse-fine 几何缩并
    - 已补清 `WarpXComputeDt.cpp` 的 `dt[lev] = dt[lev+1] * refRatio(lev)[0]` 单分量 consumer，以及 `ElectrostaticSolver.cpp / FlushFormatPlotfile.cpp` 把整组 refinement ratios 继续传给多层 Poisson 求解和 plotfile 元数据接口的边界
  - 本轮继续细化 `reduced-diags histogram/species` 邻接条目：
    - `<reduced>.species`
    - `<reduced>.bin_number / bin_min / bin_max`
    - 已补清 `ParticleHistogram2D` 的单-species `m_selected_species_id` 映射与未命中 abort，以及 `DifferentialLuminosity2D` 与 1D sibling 一样要求恰好两束 beam
    - 已补清 2D diagnostics 不直接复用 `bin_number/bin_min/bin_max`，而是拆成 `bin_number_abs/ord` 与 `bin_number_1/2` 两套 axis-specific companion，并继续进入 2D histogram / `d2L_dE1_dE2` 的 openPMD 网格索引与 `gridSpacing/gridGlobalOffset` 元数据链
  - 本轮继续细化 `thermal boundary + EB potential` 相邻条目：
    - `boundary.<species_name>.u_th`
    - `warpx.eb_potential(x,y,z,t)`
    - 已补清 `PhysicalParticleContainer -> ParticleBoundaries_K.H` 的 thermal 重采样链，以及 `PoissonBoundaryHandler -> PoissonSolver/EffectivePotentialPoissonSolver` 的 EB Dirichlet consumer
  - 本轮继续细化 `particle boundary kernel-order` 相邻条目：
    - `boundary.<species_name>.u_th`
    - `boundary.reflect_all_velocities`
    - 已补清 `boundary.<species_name>.u_th` 当前是同一 species 所有 thermal side 共享的 `m_uth`，并在 `apply_boundary(...)` 先反射位置、后经 `thermalize_boundary_particle(...)` 覆写动量
    - 已补清 `boundary.reflect_all_velocities` 只有在前面已经出现 reflecting 或 stochastic-reflection 事件时，才会把单轴 sign flip 升级成三分量同时翻转
  - 本轮继续细化 `multi-source injection + diagnostics species` 相邻条目：
    - `<species>.injection_sources`
    - `<diag>.species`
    - 已补清 `PhysicalParticleContainer -> PlasmaInjector(source_name)` 的多注入源工厂链，以及 `Full/BTD/BoundaryScraping` 三套 species 默认回退与粒子输出初始化链
  - 本轮继续细化 `particle diagnostics species-local filter` 条目：
    - `<diag>.<species>.additional_variables`
    - `<diag>.<species>.random_fraction / uniform_stride / plot_filter_function(...)`
    - 已补清 `ParticleDiag` 构造期安装链，以及 `FlushFormatPlotfile / WarpXOpenPMD` 中 `compileParser(...) + ParserFilter(InputUnits::SI)` 驱动的 writer-side `copyParticles(...)` 过滤链，并确认它同时覆盖普通 `pc` 与 pinned/BTD `pinned_pc` 路径
  - 本轮继续细化 `time-averaged diagnostics` 条目：
    - `<diag>.time_average_mode`
    - `<diag>.average_period_steps / average_period_time / average_start_step`
    - 已补清 `FullDiagnostics::DerivedInitData / DoComputeAndPack / Flush` 的 averaging window 与归一化写出链
  - 本轮继续细化 `reduced-diags` 基类/工厂条目：
    - `warpx.reduced_diags_names`
    - `<reduced>.type`
    - `reduced_diags.intervals / path`
    - 已补清 `MultiReducedDiags` 的实例注册/多态调度链，以及 `ReducedDiags` 的目录建立、restart 续写判断和 `WriteToFile(step)` 文件合同
  - 本轮继续细化 `reduced-diags` 输出文件格式条目：
    - `reduced_diags.extension / separator / precision`
    - 已补清 `ReducedDiags` 的文件名合同、restart/header 预处理和 `WriteToFile()` 列格式链
    - 已补清 `LoadBalanceCosts / FieldProbe` 对 `precision` 的自定义 writer 例外
  - 本轮继续细化 `reduced-diags` instance-local histogram/species 条目：
    - `<reduced>.species`
    - `<reduced>.bin_number / bin_min / bin_max`
    - `<reduced>.histogram_function(...)`
    - `<reduced>.normalization`
    - `<reduced>.filter_function(...)`
    - 已补清 `ParticleHistogram / BeamRelevant / DifferentialLuminosity / ParticleHistogram2D` 的 species-container 绑定链、分箱几何构造链，以及 `ParticleHistogram::ComputeDiags()` 的 parser/filter/归一化分支
  - 本轮继续细化 `FieldProbe + ParticleHistogram2D` 专有 reduced-diags 条目：
    - `<reduced>.probe_geometry / resolution / interp_order / raw_fields`
    - `<reduced>.bin_number_abs/ord / bin_min_abs/ord / bin_max_abs/ord`
    - `<reduced>.histogram_function_abs/ord(...)`
    - `<reduced>.value_function / filter_function(...,w)`
    - 已补清 `FieldProbe` 的探测器几何分派、探针粒子铺设与场插值 gate，其中 `resolution` 继续决定 probe 粒子总数和输出行数，`interp_order` 直接进入 `doGatherShapeN(...)` 的运行期插值链，废弃的 `raw_fields` 则只保留“改用 interp_order = 0”这一兼容迁移提示；同时补清 `ParticleHistogram2D::ComputeDiags()` 的二维分箱、parser 筛选和值累加链
  - 本轮继续细化 `FieldProbe + DifferentialLuminosity2D` 专有 reduced-diags 条目：
    - `<reduced>.integrate / do_moving_window_FP`
    - `<reduced>.bin_number_1/2 / bin_min_1/2 / bin_max_1/2`
    - `<reduced>.openpmd_backend / file_min_digits`
    - 已补清 `FieldProbe::ComputeDiags()` 的积分语义与 moving-window 探针平移链，以及 `DifferentialLuminosity2D` 的二维碰撞能量网格与专有 openPMD 输出文件合同
  - 本轮继续细化 `FieldProbe` 几何铺设条目：
    - `<reduced>.x/y/z_probe`
    - `<reduced>.x1/y1/z1_probe`
    - `<reduced>.target_normal_* / target_up_* / detector_radius`
    - 已补清这组参数不只定义几何输入，还会继续进入 `FieldProbe::InitData()` 的 point/line/plane 点集生成、`m_probe.AddNParticles(...)` 的 probe 宏粒子落点，以及 `ComputeDiags()` 的 moving-window 平移和 `ProbeInDomain()` 入域判定链
    - 已补清 `FieldProbe::InitData()` 的点/线/平面三条探针粒子铺设路径，以及平面探针的归一化、叉乘构型、四角求解和二维网格生成链
    - 已补清 `integrate / do_moving_window_FP` 的更细运行语义：`integrate` 同时控制 header 单位、`ComputeDiags()` 的“每步累加/按 interval 写出”调度分离和 `E/B/S += instantaneous * dt` 存储语义；`do_moving_window_FP` 则按 `step - m_last_compute_step` 累积位移，再进入 probe 粒子位置更新和后续场采样链
  - 本轮继续细化 `ParticleHistogram2D` openPMD 输出合同条目：
    - `<reduced>.openpmd_backend / file_min_digits`
    - 已补清构造期 backend 选择与回写链，以及 `WriteToFile()` 的 `openpmd_%0NT.<backend>` 文件模板、`io::Series` 创建和 axis-label 元数据链
  - 这条 open item 现在剩余的真实工作已收缩为：
    - 继续把“初步源码命中”从字符串命中压到真实 `ParmParse` / consumer 解析链
    - 清理少量仍偏粗的 grouped alias / pass-through / mixed-consumer 摘要说明
  - 当前新的优先尾项已收缩为：
    - 其余 still-coarse 的 grouped alias / pass-through / mixed-consumer 条目
    - diagnostics / particle-output / reduced-diags 里剩余少量 still-coarse 的 instance-local 条目
    - 少量 startup / AMReX-owned 邻接参数的 parser/consumer 精修
    - 已补清 `amrex.async_out / amrex.async_out_nfiles` 在 WarpX 本地只邻接 `FlushFormatPlotfile::WriteToFile()` 的 `WriteMultiLevelPlotfile(...)` 路径，而不会作用到 `FlushFormatCheckpoint` 的 `VisMF::Write(...)` checkpoint 链
    - 已补清 `amrex.abort_on_unused_inputs / amrex.use_profiler_syncs` 的更细 startup 分界：前者现在明确到 `AMReX.cpp` 把输入写入 `amrex::system::abort_on_unused_inputs`，并由 `AMReX_ParmParse.cpp` 的 unused-input 收尾检查决定是否 `Abort("ERROR: unused ParmParse variables.")`；后者也已明确到 `AMReX_BLProfiler.cpp` 把输入写入 `BLProfileSync::use_prof_syncs`，并在 `FillBoundary / ParallelCopy / Redistribute` 前触发 `SyncBeforeComms:*` timed barrier，而 WarpX 真正主动协调的 profiler 同步项仍是 `tiny_profiler.device_synchronize_around_region`
    - 已补清 `vismf.usedynamicsetselection / iobuffersize / allowsparsewrites / noflushafterwrite / barrierafterlevel` 的更细 writer 分支：现在明确到 `VisMF::Write(...)` 先判 `allowSparseWrites` 再判 `useDynamicSetSelection`，`iobuffersize` 会同时进入 `VisMF::IO_Buffer`、persistent input stream 和 `pubsetbuf(...)`，`noflushafterwrite` 只抑制逐 fab/粒子文件写链的显式 flush 而不影响 combined-write 分支的无条件 flush，`barrierafterlevel` 则会同时进入 field plotfile 与粒子二进制写盘的 per-level barrier
    - 已补清 `vismf.headerversion / verbose` 的更细 `VisMF` 合同：前者现在明确到 parser 后写回 `currentVersion`，并在 `VisMF::Header(...)` 与 `VisMF::Write(...)` 里决定是否保留 fab headers 和 min/max；后者则明确到 `VisMF::Read/Check/RemoveFiles` 的 in-file-order、耗时汇总、header 检查和逐文件删除日志，而 WarpX plotfile/checkpoint writer 会分别临时强制 `Version_v1 / NoFabHeader_v1` 后再恢复
    - 已补清 `warpx.field_io_nfiles / particle_io_nfiles / particles.particles_nfiles` 的更细 fan-out 合同：`field_io_nfiles` 现在明确到 `VisMF::SetNOutFiles(...)` 后会在 AMReX 侧截到 `[1, NProcs]`，并同时进入 plotfile 与 checkpoint 的 field-side `VisMF::Write(...)`；`particles.particles_nfiles` 则明确到 `ParticleContainer::WritePlotFile/Checkpoint -> WriteBinaryParticleData{Sync,Async}`，再由 `queryAdd("particles_nfiles", nOutFiles)`、`pc.nOutFilesPrePost` 和粒子 `NFilesIter` 共同决定实际粒子文件 fan-out
    - 已补清 `warpx.usesingleread / usesinglewrite` 的更细 `VisMF` 合并 I/O 分支：现在明确到 WarpX 会用默认 `true` 覆写 AMReX `vismf.*` 的默认 `false`，随后 `useSingleWrite` 真正控制 `VisMF::Write(...)` 的 multi-fab 合并单次写出分支，`useSingleRead` 真正控制 `VisMF::Read(...)` 的连续多 fab 合并读取分支，并且桥接后的 `vismf.usesingle* = true` 已在现有 `warpx_used_inputs / warpx_job_info` 产物中直接落盘
    - 已补清 `warpx.mffile_nstreams` 的更细 reader batching 合同：现在明确到 `VisMF::SetMFFileInStreams(...)` 后会在 AMReX 侧截到 `[1, NProcs]`，并在 `VisMF::Read(...)` 中把同一文件对应的 `readFileRanks` 切成至多 `nStreams` 组，再逐组经 `NFilesIter(...).ReadyToRead()` 调度，因此它真实支配的是 restart 与 PML MultiFab 恢复链上的 per-file reader batching
    - 已补清 `warpx.reduced_diags_names` 的更细 reduced-diag 总入口：现在明确到它不仅驱动 `MultiReducedDiags` 的名字表，还继续决定 `<reduced>.type` 的 factory 分派、主 step-loop 的 `DoDiags/ComputeDiags/WriteToFile` 调度、implicit solver 的 `ComputeDiagsMidStep` hook，以及 restart 补写和 checkpoint 的 `ReadCheckpointData/WriteCheckpointData` 链
    - 已补清 `<reduced_diags_name>.type` 的更细类型特异边界：现在明确到它不仅决定工厂实例化哪个子类，还直接决定该实例是否真正消费 `ComputeDiagsMidStep()` 与 checkpoint 状态续写；当前 `FieldPoyntingFlux` 会在 mid-step 置 `use_mid_step_value` 并立即重算通量，同时把时间积分量写入和从 `FieldPoyntingFlux_data.txt` 恢复
    - 已补清 `reduced_diags.intervals` 的更细 reduced-diag 节拍合同：现在明确到它按“默认 `1` -> 全局 `reduced_diags.intervals` -> 实例级 `<rd_name>.intervals`”顺序生成 `IntervalsParser`，并直接拒绝旧别名 `<reduced_diag_name>.frequency`；后续它不仅进入 `ReducedDiags::DoDiags()`、`MultiReducedDiags::WriteToFile()` 和大量派生类 `ComputeDiags()` 的早退 gate，还在 `DifferentialLuminosity` 中决定何时做 device-to-host 拷回与 MPI 归约，并在 `LoadBalanceCosts` 中通过 `nextContains(step+1)` 判断最后一次输出后是否需要补 `NaN` 收尾
    - 已补清 `reduced_diags.path` 的更细 writer-side 路径合同：现在明确到它不仅建立 `m_path` 根目录，还继续进入文本 reduced diag 的 `m_path + m_rd_name + "." + m_extension` restart/header 判断与主文件落点，并在 `LoadBalanceCosts` 中生成 `.tmp` 文件补 `NaN` 后通过 `remove + rename` 重写；同时 `ParticleHistogram2D / DifferentialLuminosity2D` 已明确不消费这条单文件合同和 `m_write_header`，而是把 `m_path` 当作 openPMD 子目录根，生成 `m_path + m_rd_name + "/" + filename` 的 series 路径
    - 已补清 `reduced_diags.extension` 的更细文本 writer 命名合同：现在明确到它不仅决定 `m_path + m_rd_name + "." + m_extension` 的文件名，还继续参与基类对该文件的预创建与 `m_write_header` 续写判定，并被 `FieldProbe / ParticleExtrema / DifferentialLuminosity / ColliderRelevant / BeamRelevant` 等自定义文本 writer 复用；`LoadBalanceCosts` 还会生成 `.tmp.<extension>` 做补 `NaN` 重写，而 `ParticleHistogram2D / DifferentialLuminosity2D` 则完全旁路这条后缀，改由 `openpmd_backend` 决定 `openpmd_%0NT.<backend>`
    - 已补清 `reduced_diags.precision` 的更细文本数值格式边界：现在明确到默认值本体在 `ReducedDiags.H` 中就是 `m_precision = 14`，随后 `ReducedDiags` 构造函数才按“全局 -> 实例级”顺序用 `queryWithParser(...)` 覆写；同时只有走基类 `WriteToFile()` 的文本 reduced diags 才真正消费 `std::setprecision(m_precision)`，而且它只命中 step 之后的时间列与 `m_data` 数值列，不控制 step 列或 header。相对地，`FieldProbe::WriteToFile()` 与 `LoadBalanceCosts::WriteToFile()` 当前都显式写死 `14` 位，`ParticleHistogram2D / DifferentialLuminosity2D` 则完全不消费这条文本格式参数
    - 已补清 `<reduced_diags_name>.species` 的更细类型对照边界：现在明确到 `ParticleHistogram{,2D}` 会在构造期把单个 species 名解析成固定 id，错名立即 abort；`BeamRelevant` 只在 `ComputeDiags()` 里按名字筛选 species，错名会静默退化成零数据输出。双束 `ColliderRelevant` 会在 startup 期立刻 `GetParticleContainerFromName(...)` 并额外拒绝 neutral species；而 `DifferentialLuminosity{,2D}` 虽把双束名延迟到 `ComputeDiags()` 才解析，但因为它们是每步累积型 diagnostics、没有 `m_intervals.contains(step+1)` 的早退 gate，所以错名会在第一次实际进入 `ComputeDiags()` 时就 assert，而不是拖到首次写盘
    - 已补清 `<reduced_diags_name>.bin_number / bin_min / bin_max` 的更细反向边界：现在明确到 1D/2D 构造函数都不会显式守卫 `bin_number > 0` 或 `bin_max > bin_min`，而是直接生成 `m_bin_size`；后续 1D 会把它继续送进 `floor((f-bin_min)/bin_size)` 与 `1/bin_size` 归一化，2D 除了双轴落 bin 和 `1/(bin_size_1*bin_size_2)` 外，还会把 `bin_num-1` 直接送进临时 `TableData` 上界，并在 openPMD writer 里把 `m_bin_num_*` 无符号转换成 dataset shape，因此坏输入会继续泄漏到缓冲形状、mesh 几何和归一化链
    - 已补清 `<reduced_diags_name>.normalization` 的更细 1D/2D companion 边界：现在明确到 `unity_particle_weight` 和 `default` 的差异只发生在 GPU 原子累加阶段，前者按 `1` 计数、后者按宏粒子权重 `w` 计数，而两者在 `ReduceRealSum(...)` 之后都不会再进入额外 host-side 后处理；真正的 host-side 归一化只属于 `max_to_unity / area_to_unity`。相对地，`ParticleHistogram2D` 虽也会做 weighted accumulation 和 MPI 归约，并能通过独立 `value_function(...,w)` 改写 bin 权重，但当前完全没有同名 `normalization` 入口
    - 已补清 `<reduced_diags_name>.histogram_function(t,x,y,z,ux,uy,uz)` 的更细 parser-companion 边界：现在明确到 2D 路径里 `histogram_function_abs/ord` 只定义 bin 坐标轴，真正写入权重还要再走独立 `value_function(...,w)`；而当前 kernel 会无条件编译并调用 `value_function`，源码没有“未给时回退成粒子权重 `w`”的显式默认分支，因此实现上它不是松耦合可选补充，而是 `filter -> abs/ord -> value` 的固定 companion 链。相对地 writer metadata 仍只会写回 `function_abscissa / function_ordinate`，不会把 `value_function` 一并持久化
    - 已补清 `<reduced_diags_name>.bin_number / bin_min / bin_max` 的更细离散网格合同：现在明确到 1D `ParticleHistogram` 会用这组值生成 header 中的 bin center，并在运行时按 `floor((f-bin_min)/bin_size)` 落 bin 且越界即丢弃；2D companion 则进一步进入 openPMD 的 `gridGlobalOffset / gridSpacing / dataset shape`，同时 `DifferentialLuminosity2D` 中 `bin_size_1 * bin_size_2` 还直接参与 `d2L_dE1_dE2` 的归一化公式
    - 已补清 `<reduced_diags_name>.normalization` 的更细 1D histogram 后处理边界：现在明确到 `unity_particle_weight` 发生在 GPU kernel 的逐粒子原子累加阶段，而 `max_to_unity / area_to_unity` 则都发生在 device-to-host 拷回并完成 MPI `ReduceRealSum` 之后的全局 `m_data` 上；同时 `ParticleHistogram2D` 当前没有对应的 `normalization` companion，也不会走这两条 host-side 归一化分支
    - 已补清 `<reduced_diags_name>.histogram_function(t,x,y,z,ux,uy,uz)` 的更细轴变量合同：现在明确到 1D `ParticleHistogram` 的 parser 签名只带 `(t,x,y,z,ux,uy,uz)`，而 2D sibling `histogram_function_abs/ord(...)` 额外带入 `w`；运行时都会先把 `ux,uy,uz` 归一到 `c` 后再求值，但 2D 情况还会先经过 `filter_function(...,w)`，并且最终把原始表达式写回 openPMD 的 `function_abscissa / function_ordinate` mesh attributes
    - 已补清 `<reduced_diags_name>.filter_function(t,x,y,z,ux,uy,uz)` 的更细粒子级 early-return 边界：现在明确到 1D `ParticleHistogram` 的 filter 签名只带 `(t,x,y,z,ux,uy,uz)`，而 2D sibling 会扩成 `(...,w)`；同时 1D 路径把 `fun_filterparser(...) == 0._rt` 当作拒绝条件，2D 路径则先 `static_cast<bool>(fun_filterparser(...,w))` 判真，只有通过筛选的粒子才会继续进入 `histogram_function_abs/ord(...,w)` 和 `value_function(...,w)` 的求值与累加链
    - 已补清 `<reduced_diags_name>.filter_function(t,x,y,z,ux,uy,uz)` 的更细真值语义边界：现在明确到 1D 与 2D 两条路径虽然分别写成 `== 0._rt` 与 `static_cast<bool>(...)`，但当前实现本质上都属于“零值拒绝器”而不是“正值保留器”，因此负的非零返回值同样会保留样本；同时 2D 路径里的 filter 仍只是 `filter -> histogram_function_abs/ord -> value_function` 固定 companion 链最前端的粒子级 early-return，不会改写 writer 或 openPMD metadata 路径
    - 已补清 `<reduced_diags_name>.x_probe/y_probe/z_probe` 的更细 FieldProbe 参考点边界：现在明确到这组坐标不只作为 `Point` 的单点位置、`Line` 的起点和 `Plane` 的参考中心进入 `InitData()` 与 `m_probe.AddNParticles(...)`，还会被 `ProbeInDomain()` 仅拿来和 `Geom(0).ProbLo/ProbHi` 比较参考起点/中心是否在域内，而不会逐个检查整条线段或整块平面网格；同时 `do_moving_window_FP` 打开后真正平移的是 probe 粒子的实时位置，但 `ProbeInDomain()` 仍继续使用未更新的 `x_probe/y_probe/z_probe` 做 gate
    - 已补清 `<reduced_diags_name>.probe_geometry` 的更细 FieldProbe 总分派边界：现在明确到这条参数不只选择 `Point / Line / Plane` 三个枚举，还会直接决定 companion 输入集、非法字符串和 1D `Plane` 的立即拒绝，以及 `InitData()` 最终生成单点、等间距线阵列还是 `m_resolution * m_resolution` 平面网格；这些拓扑又继续决定 `m_probe.AddNParticles(...)` 的 probe 宏粒子总数和后续 writer 面对的输出形态
    - 已补清 `<reduced_diags_name>.x1_probe/y1_probe/z1_probe` 的更细线探针终点边界：现在明确到这组参数和起点一起形成 `DetLineStepSize = (endpoint-startpoint)/(m_resolution-1)`，并据此在 `InitData()` 中铺出整条等间距 probe 粒子链、继续决定后续 `m_valid_particles` 规模；同时它们并不单独进入 `ProbeInDomain()` 或 `WriteToFile()` 的 gate，入域判定仍只看起点侧 `x_probe/y_probe/z_probe`
    - 已补清 `<reduced_diags_name>.target_normal_*/target_up_*/detector_radius` 的更细平面探针局部几何边界：现在明确到这组参数会先在 `InitData()` 中被归一化，并继续派生出 `orthotarget/direction`、`uppercorner/lowercorner/loweropposite` 与 `SideStepSize/UpStepSize`，最终离散成 `m_resolution * m_resolution` 的二维 probe 网格；同时它们并不单独进入 `ProbeInDomain()` 或 `WriteToFile()` 的 gate，域内判定仍只看参考中心 `x_probe/y_probe/z_probe`
    - 已补清 `<reduced_diags_name>.resolution` 的更细 line-vs-plane 离散边界：现在明确到同一个 `m_resolution` 在线探针里只生成 `N` 个采样点、在平面探针里则提升成 `N^2` 个网格点，并且都会通过 `(m_resolution - 1)` 继续决定 `DetLineStepSize` 或 `SideStepSize/UpStepSize`；同时它不单独进入 `ProbeInDomain()` 或 `WriteToFile()` 的 gate，域内判定仍只看参考坐标 `x_probe/y_probe/z_probe`
    - 已补清 `<reduced_diags_name>.interp_order` 的更细 gather dispatch 边界：现在明确到它不只在构造期要求 `interp_order <= algo.particle_shape`，还会在 `ComputeDiags()` 中直接传给 `doGatherShapeN(...)`，并在 `FieldGather.H` 底层继续分派到 `doGatherShapeN<1..4, 0/1>`；同时它本身不改变 writer、moving-window 或积分调度，而废弃 `raw_fields` 虽提示迁移到 `interp_order = 0`，当前这条常规 gather 入口本身并不覆盖 `0` 阶分派
    - 已补清 `<reduced_diags_name>.do_moving_window_FP` 的更细迁移边界：现在明确到 `FieldProbe` 并不直接复用 `WarpX::moving_window_active(step)`，而是本地按 `step > start_moving_window_step && step <= end_moving_window_step` 结合本开关生成 `update_particles_moving_window`，再通过 `step - m_last_compute_step` 把位移累积成 `move_dist = dt * moving_window_v * step_diff`；同时真正被平移的是实时 probe 粒子位置，但 `ProbeInDomain()` 仍继续只看参考坐标 `x_probe/y_probe/z_probe`
    - 已补清 `ParticleHistogram2D` 的 `<reduced_diags_name>.openpmd_backend / file_min_digits` 更细 writer 合同：现在明确到构造期会把 `default` backend 回写成 `WarpXOpenPMDFileType()` 的实际选择，`WriteToFile()` 固定生成 `openpmd_%0NT.<backend>` 模板并按平台分流路径分隔符，随后把数据写进 `series.iterations[step+1].meshes["data"]`，连同 `function_abscissa / function_ordinate / filter`、axis labels、grid offsets 和 time 一起落入 mesh 元数据；同时缺少 `WARPX_USE_OPENPMD` 时不会降级，而是直接 abort
    - 已补清 `DifferentialLuminosity2D` 的 `<reduced_diags_name>.openpmd_backend / file_min_digits` 更细 writer 合同：现在明确到它同样会把 `default` backend 回写成 `WarpXOpenPMDFileType()` 的实际选择，`WriteToFile()` 固定生成 `openpmd_%0NT.<backend>` 模板并按平台分流路径分隔符，但真正写进的是 `series.iterations[step+1].meshes["d2L_dE1_dE2"]`，并固定落入 `axisLabels={"E2","E1"}`、能量轴 `gridGlobalOffset/gridSpacing`、`setPosition({0.5,0.5})` 和当前 `time`；同时缺少 `WARPX_USE_OPENPMD` 时不会降级，而是直接 abort
    - 已补清 `ChargeOnEB` 的 `<reduced_diags_name>.weighting_function(x,y,z)` 更细表面积分加权核：现在明确到这条参数受 `WARPX_DIM_3D`、`AMREX_USE_EB` 与运行时 `EB::enabled()` 的双重硬检查约束；真正加权发生在 level-0 cut-cell 的 EB 面元质心坐标 `(x,y,z)` 上，用 `fun_weightingparser(x,y,z)` 去乘局部 `dS·E` 贡献，而不是对全域体积分或整块网格做统一缩放，最后再经过原子加法、MPI `ReduceRealSum` 和 `epsilon_0` 写成总电荷
    - 已补清 `qed_qs.photon_creation_energy_threshold` 的更细 photon cleanup 边界：现在明确到这条参数若未显式给值，会保留 `2*m_e*c^2` 默认值并记录一条 low-priority warning；真正发生在 `doQedQuantumSync()` 的 photon 已经生成并写入 product container 之后，由 `cleanLowEnergyPhotons(...)` 只扫描本轮新增 photon，用能量平方与阈值平方比较后把低能 photon 标成 `Invalid`，真正删除则留给后续 invalid-particle 清理链
    - 已补清 `<species_name>.do_qed_quantum_sync` 的更细 QED 主链 gate：现在明确到这条参数不只在构造期新增 `opticalDepthQSR` 并强制读取 photon product species，还会在 `InitQED()` 中只对 `has_quantum_sync()` 的 species 绑定共享 `QuantumSynchrotronEngine`、累计 `m_nspecies_quantum_sync` 并决定是否进入 `InitQuantumSync()`；随后 `DefaultInitialization.H`、普通 push、`ImplicitPushPX` 与 `doQedQuantumSync()` 只对这类 species 接入 optical-depth 演化和 photon-emission pass，同时 `PhotonParticleContainer` 又显式禁止 photon species 打开它
    - 已补清 `<species_name>.qed_quantum_sync_phot_product_species` 的更细 product-container 绑定边界：现在明确到这条字符串会在初始化期通过 `getSpeciesID(...)` 解析成整数索引，名字不匹配时直接报错；运行期 `doQedQuantumSync()` 再用这个索引取出 `pc_product_phot` 作为新 photon 的目标容器，同时初始化检查会继续强制要求 product 不能与 source species 相同，且目标容器物种类型必须是 `photon`
    - 已补清 `<species_name>.do_classical_radiation_reaction` 的更细 Boris-based RR 分派链：现在明确到这条参数不只在构造期强制要求 species 必须是 `electron/positron` 且全局 pusher 必须是 `Boris`，还会在普通 `PhysicalParticleContainer` 与 `RigidInjectedParticleContainer` 的 momentum-update 中显式切到 `UpdateMomentumBorisWithRadiationReaction(...)`；同时 `PushSelector.H` 会优先检查 `do_crr`，并在 `WARPX_QED` + Quantum Sync 联用时再按 `chi < t_chi_max` 决定走 RR 还是回退普通 `UpdateMomentumBoris(...)`，而 `ImplicitPushPX` 只是继续把 `do_crr` 向下传入这条统一分派链
    - 已补清 `<species_name>.do_qed_breit_wheeler` 的更细 BW 主链 gate：现在明确到这条参数不只在构造期挂上 `opticalDepthBW` 并对 photon species 强制读取电子/正电子产物名，还会在 `InitQED()` 中只对 `has_breit_wheeler()` 的 species 绑定共享 `BreitWheelerEngine`、累计 `m_nspecies_breit_wheeler` 并决定是否进入 `InitBreitWheeler()`；随后 `DefaultInitialization.H` 会把 `opticalDepthBW` 初始化成随机指数分布，`PhotonParticleContainer` push 路径只在本开关为真时演化 BW optical depth，而 `MultiParticleContainer::doQedBreitWheeler()` 则只对这类 source species 取出电子/正电子 product container，并把新 pair 写入目标容器
    - 已补清 `<species_name>.qed_breit_wheeler_ele_product_species` 与 `..._pos_...` 的更细 product-container 绑定边界：现在明确到这两条字符串不只在 `PhotonParticleContainer` 构造期被强制读取，还会在 `MultiParticleContainer::mapSpeciesProduct()` 中经 `getSpeciesID(...)` 解析成整数索引；随后 `CheckQEDProductSpecies()` 强制要求 product 不能与 source photon species 相同，且电子/正电子两侧的目标容器类型必须分别真的是 `electron` / `positron`；运行期 `doQedBreitWheeler()` 再通过 `allcontainers[...]` 取到 `pc_product_ele/pc_product_pos`，并把新 pair 分别写入这两个目标容器
    - 已补清 `qed_schwinger.ele_product_species / pos_product_species` 的更细容器绑定边界：现在明确到这两条字符串不只在 `ParmParse("qed_schwinger")` 中被强制读取，还会经 `getSpeciesID(...)` 解析成整数索引；随后 `CheckQEDProductSpecies()` 强制要求电子/正电子两侧目标容器类型必须分别真的是 `electron` / `positron`；运行期 `doQEDSchwinger()` 再先取出 `pc_product_ele/pc_product_pos` 与对应 tile，并通过 `SmartCreateFactory + filterCreateTransformFromFAB<1>(...)` 把每次 Schwinger 事件生成的电子/正电子分别写入这两个目标容器
    - 已补清 `warpx.verbose` 的更细 stdout/default-verbosity 边界：现在明确到它不只在 `WarpX::ReadParameters()` 中覆写 `WarpX.H` 里的默认值 `verbose = 1`，还会在 `main.cpp` 中单独控制 `Total Time` 总计时输出；`WarpXEvolve.cpp` 会先用它建立 `verbose_step`，再和 `limit_verbose_step` 一起决定 `STEP ... starts`、adaptive timestep 的 `updating timestep`、`STEP ... ends / Evolve time ...` 是否打印，而 re-sort 提示则额外受 `verbose && !m_limit_verbose_step` 约束。与此同时，显式给出的 `warpx.verbose` 还会在 `Diagnostics::BaseReadParameters()` 中成为 diagnostics 实例的全局默认 verbosity；相对地 `WriteUsedInputsFile()` 的提示和 first-step unused-input 明细展开并不走这条 gate，而分别受 `write_used_inputs_file(..., true)` 默认实参和 `amrex.parmparse.verbose` 控制
    - 已补清 `warpx.serialize_initial_conditions` 的更细初始化边界：现在明确到它不只是“粒子初始化阶段禁用 OpenMP”这么宽泛，而是当前只打到 `AddParticles.cpp` 里 plasma injector 准备后的 `MFIter`/tile 级粒子创建主循环；源码通过静态成员默认值 `false` 加 `pp_warpx.query(...)` 覆写，再在 `AMREX_USE_OMP && !AMREX_USE_GPU` 条件下用 `#pragma omp parallel if (not WarpX::serialize_initial_conditions && amrex::Gpu::notInLaunchRegion())` 控制是否串行，因此 GPU launch 区域和其它未引用该静态成员的初始化路径都不受这条 gate 影响
    - 已补清 `warpx.safe_guard_cells` 的更细 guard-cell 合同：现在明确到它不只是在 `WarpXComm` 里“多交换一些 guard cells”，而是先在 `GuardCellManager` 中把 `ng_FieldSolver / ng_FieldGather / ng_UpdateAux / ng_afterPushPSATD / ng_MovingWindow` 等一整组预算直接抬到 `ng_alloc_*`；随后 `FillBoundaryE/B/F/G` 与 `E_avg/B_avg` 在 safe 模式下会无视请求的 `ng`，直接改走 `nGrowVect()` 或整组 `Vector<MultiFab*>` 的全量通信，而 `shiftMF(...)` 也会从仅填 moving-window 方向所需的 `ng_mw` 改成整块 `tmpmf` 的全 guard-cell 填充；同时 `WarpXEvolve.cpp` 还会在部分 PML/field-push 分支后额外补做 `FillBoundaryF/E/B(...)`
    - 已补清 `ablastr.fillboundary_always_sync` 的更细 helper 合同：现在明确到它不是 startup 时一次性缓存，而是在 `ablastr::utils::communication::FillBoundary(...)` 的 `MultiFab& + ng` 入口里按次读取 `ParmParse("ablastr")`；随后以 `nodal_sync_arg || do_nodal_sync_input` 合并实参与输入，再在普通精度路径上切换 `mf.FillBoundary(...) / mf.FillBoundaryAndSync(...)`，在 single-precision 路径上改成 `mixedCopy(mf_tmp <- mf) -> mf_tmp.FillBoundary{AndSync}(...) -> mixedCopy(mf <- mf_tmp)`，而 `MultiFab&` 无 `ng` 重载与 `Vector<MultiFab*>` 包装重载都只是继续回落到这同一 helper 链
    - 已补清 `warpx.serialize_initial_conditions / safe_guard_cells / ablastr.fillboundary_always_sync` 的更细 runtime 分支：前者现在包含旧别名 `serialize_ics` 的拒绝边界和 `AddParticles.cpp` 的 OpenMP gate，后两者则分别压实到 `WarpXEvolve.cpp` 的额外 `FillBoundary*` 补同步点，以及 `ablastr::utils::communication::FillBoundary(...)` 中普通/单精度临时副本两条 `FillBoundary(...)` vs `FillBoundaryAndSync(...)` 切换链
    - 已补清 `warpx.poisson_solver` 的更细 electrostatic/Poisson 合同：现在明确到 `WarpX::ReadParameters()` 对 3D、open boundary、FFT 编译开关和 `labframe-electromagnetostatic` 的 parser 级兼容性 gate，`PoissonBoundaryHandler::DefinePhiBCs()` 对 `Multigrid/IntegratedGreenFunction` 的边界族分叉，以及 `LabFrameExplicitES / RelativisticExplicitES / PhiFunctor` 复用的 `DefinePhiBCs + computePhi(...)` 运行链和 `boundary.potential_* / warpx.eb_potential(...)` 的 initial-Poisson-solve side-effect
    - 已补清 `self_fields_absolute_tolerance / self_fields_max_iters / self_fields_verbosity` 的更细 solver-vs-species consumer 边界：现在明确到 `ElectrostaticSolver::ReadParameters()` 的三条默认入口、`PhysicalParticleContainer` 上 `absolute_tolerance/max_iters` 走 `queryWithParser(...)` 而 `verbosity` 只走 plain `query(...)` 的 parser 差异，以及 `RelativisticExplicitES` 里 `ComputeSpaceChargeField()` 使用 `pc.self_fields_*`、`AddBoundaryField()` 仍退回 solver 默认值的双路径分叉
    - 已补清 `self_fields_required_precision` 的同簇 consumer 分叉：现在明确到它也不只是“solver 默认 + species override”，而是与后面三条对称地包含 `ElectrostaticSolver::ReadParameters()` 的默认入口、`PhysicalParticleContainer` 的 species 级 `queryWithParser(...)` override，以及 `RelativisticExplicitES` 中 `ComputeSpaceChargeField()` 使用 `pc.self_fields_required_precision`、`AddBoundaryField()` 仍退回 solver 默认值的双路径边界
    - 已补清 `use_2d_slices_fft_solver` 的 IGF companion 边界：现在明确到它不只是 FFT Poisson 的泛化开关，而是 `ElectrostaticSolver::ReadParameters()` 里默认 `false` 的 `is_igf_2d_slices`，只在 `poisson_solver = IntegratedGreenFunction` 的路径下继续经 `LabFrameExplicitES / RelativisticExplicitES -> computePhi(...) -> ablastr::fields::computePhi(...)` 真实消费；同时 `PhiFunctor` 显式硬编码 `false`、`EffectivePotentialES` 当前也未继续暴露这条 companion
    - 已补清 `magnetostatic_solver_verbosity` 的更细唯一运行链：现在明确到它不只是 `computeVectorPotential(...)` 的一个普通实参，而是 `WarpX::ReadParameters()` 里先继承 `self_fields_verbosity` 再允许显式覆盖的兼容默认链，只在 `LabFrameElectroMagnetostatic` 模式下经 `WarpXEvolve.cpp -> ComputeMagnetostaticField() -> AddMagnetostaticFieldLabFrame() -> computeVectorPotential(...)` 真实消费，并且该路径还显式拒绝 Python `poissonsolver` callback、要求 `max_level == 0`
    - 已补清 `magnetostatic_solver_required_precision / absolute_tolerance / max_iters` 的同簇唯一运行链：现在明确到三条都不只是 `computeVectorPotential(...)` 的普通实参，而是 `WarpX::ReadParameters()` 中先继承对应 `self_fields_*` 再允许显式覆盖的兼容默认链，只在 `LabFrameElectroMagnetostatic` 模式下经 `WarpXEvolve.cpp -> ComputeMagnetostaticField() -> AddMagnetostaticFieldLabFrame() -> computeVectorPotential(...)` 真实消费，并且该路径同样显式拒绝 Python `poissonsolver` callback、要求 `max_level == 0`
    - 已补清 `field_centering_nox/noy/noz` 的 magnetostatic 反向边界：现在明确到这组参数不只是在 `WarpX::ReadParameters()` 中按 momentum-conserving gather 或 `LabFrameElectroMagnetostatic` 条件读取并分配 `device_field_centering_stencil_coeffs_*`，还会在 `MagnetostaticSolver::EBCalcBfromVectorPotentialPerLevel::doInterp()` 中作为 `warpx_interp(...)` 的真实 stencil 阶数被消费；同时 `maxLevel() > 0 && grid_type != Collocated` 时三条值仍被强制限制为二阶
    - 已补清 `current_centering_nox/noy/noz` 的更细运行边界：现在明确到它不只是在 `do_current_centering` 为真时读取，而是继续受 `grid_type=hybrid` 与 `maxLevel()==0` gate 约束，并会分配 `device_current_centering_stencil_coeffs_*`、绑定 `current_fp_nodal` 路径，随后在 `WarpXComm.cpp` 中同时进入 `UpdateCurrentNodalToStag(...)` 和 `get_ng_depos_J()` 这两条真实 consumer
    - 已补清 `do_current_centering` 的更细 runtime 反向边界：现在明确到它不只约束 `hybrid` grid 和 `maxLevel()==0`，还会在 `WarpX.cpp` 中继续显式拒绝 `Esirkepov / Villasenor / Vay` 与当前中心化并用；同时 `WarpXComm.cpp::SyncCurrent()` 里除了执行 nodal-to-staggered centering，还额外带着 `finest_level <= 1` 的运行时断言
    - 已补清 `particles.deposit_on_main_grid / gather_from_main_grid` 的更细 runtime 分支：前者现在从 `MultiParticleContainer` 的 species side-list 回绑，继续压实到 `WarpX.cpp` 对 `n_current_deposition_buffer`、`current_buf/rho_buf` 和 `current_buffer_masks` 的强制启用、`Partition.cpp` 的 `nfine_current=0` 分区边界，以及 `PhysicalParticleContainer.cpp` / `WarpXEvolve.cpp` 中 `rho_buf/current_buf -> (lev-1)` 的 coarse-buffer 沉积与后续 coarse-level sync；后者则继续压实到 `Efield_cax/Bfield_cax` 分配、`nfine_gather=0` 分区边界，以及 `PhysicalParticleContainer.cpp` 中按 `np_gather` 把后段粒子改走 `gather_lev = lev-1` 的 coarse-gather 运行链
    - 已补清 `particle_thermalizer.normal / species / start / end / momentum_threshold / theta` 的更细 runtime 分支：从 `ParticleThermalizer` 构造期的几何合法性与参数断言，继续压实到 `WarpXEvolve.cpp` 的每步 hook、per-species/per-level/per-tile 的 `applyThermalizer()` 链、`find_overlap(...)` 的 tile 级早退、沿法向的位置概率筛选，以及“仅对超过阈值的动量分量按 `RandomNormal` 重采样并保留原符号”的逐粒子热化 kernel
    - 已补清 `particles.do_tiling` 的更细 runtime 分支：从 `WarpXAMReXInit.cpp` 的启动期默认值覆写和 `WarpXParticleContainer::ReadParameters()` 的静态读取，继续压实到 `AddParticles.cpp` / `MultiParticleContainer.H` 中 `MFItInfo::EnableTiling(tile_size)` 的粒子创建路径、多 species helper 的一致性断言，以及“仅在 `Gpu::notInLaunchRegion()` 的 CPU 路径下真正启用 tiling”的运行边界
    - 已补清 `particles.use_fdtd_nci_corr` 的更细 runtime 分支：从 `MultiParticleContainer` 的 parser 入口和 `WarpX.cpp` 对 `PSATD / Esirkepov / implicit` 的兼容性约束，继续压实到 `WarpX::InitNCICorrector()` 中按 level 的 `c*dt/dz` 与 `nodal_gather` 构造两套 `NCIGodfreyFilter` 并 `ComputeStencils()`，以及 `PhysicalParticleContainer::Evolve()` 在 fine/coarse gather 两条路径里先对 tile 级 `E/B` 分量 `ApplyStencil(...)` 到临时 `filtered_*` `FArrayBox`、再把 `PushPX(..., lev, gather_lev)` 的 gather 指针改绑到这些过滤后场的运行链
    - 已补清 `particles.rigid_injected_species / <species>.species_type` 的更细 runtime 分支：前者现在从 `MultiParticleContainer::ReadParameters()` 里“先按 `particles.species_names` 校验名字、再把 `species_types` 从 `PCTypes::Physical` 改写成 `PCTypes::RigidInjected`”的工厂分类键，继续压实到 `RigidInjectedParticleContainer` 的 `zinject_plane / rigid_advance` 解析、`InitData() -> AddParticles(0) -> RemapParticles() -> Redistribute()` 初始化链、后续每步 `Evolve()` 对 `zinject_plane_levels` 和 `done_injecting_lev` 的更新，以及 `MultiParticleContainer::ReadHeader()/WriteHeader()` 多态转发到 `RigidInjectedParticleContainer::{ReadHeader,WriteHeader}` 时只续写 `zinject_plane_levels / vzbeam_ave_boosted`、不持久化 `done_injecting_lev` 而把它留到 restart 后首个 `Evolve()` 重新计算的 header 边界；后者则从 `PhysicalParticleContainer` 的默认 `charge/mass` 与必填检查，继续压实到 `MultiParticleContainer` 按 `PhysicalSpecies::photon` 切到 `PhotonParticleContainer` 的运行分派，以及 injector/external-file 路径上对同一优先级规则的复用
    - 已补清 `<species>.charge / mass` 的更细 runtime 分支：现在从 `PhysicalParticleContainer` 中 `PlasmaInjector::queryCharge/queryMass -> species_type -> 显式 parser` 的三层优先级，继续压实到 `PlasmaInjector::setupExternalFile()` 从 openPMD 记录读取质量电荷、按 `unitSI` 还原并向 MPI 广播，以及 `SpeciesUtils::extractSpeciesProperties()` 对 `injection_style == external_file` 的豁免分支与后续缺失断言
    - 已补清 `<species>.xmin/ymin/zmin/xmax/ymax/zmax / injection_sources` 的更细 runtime 分支：前者现在从 `PlasmaInjector` 的“下闭上开” `insideBounds()` 与 box-level `overlapsWith()`，继续压实到 `AddParticles.cpp` 的 tile 级 early-return、cell/粒子逐点裁剪以及 ballistic-correction 后判定；后者则从 `PhysicalParticleContainer` 中为同一 species 构造多个 `PlasmaInjector(source_name)`，继续压实到 `AddParticles()/ContinuousInjection()/ContinuousFluxInjection()` 对各 source 的逐个执行，以及 `WarpXInitData.cpp::get_nppc()` 目前仍不支持 multi-source 预估的实现边界
    - 已补清 `<species>.injection_style` 的更细 runtime 分支：现在从 `PlasmaInjector` 构造期对 `singleparticle / multipleparticles / gaussian_beam / nrandompercell / nfluxpercell / nuniformpercell / external_file / none` 的 `setup*` 工厂分派，继续压实到 `PhysicalParticleContainer` 对基准/多 source injectors 的构造链、`WarpXInitData.cpp::get_nppc()` 的 style-specific 负载预估路径，以及 `AddParticles()/ContinuousInjection()/ContinuousFluxInjection()` 对 `AddNParticles / AddGaussianBeam / AddPlasmaFromFile / AddPlasma / AddPlasmaFlux` 的真实运行分支
    - 已补清 `<species>.num_particles_per_cell_each_dim` 的更细规则注入链：现在不只在 `PlasmaInjector::setupNuniformPerCell()` 中做维度长度检查和 `RZ` 多模下的最小 theta-ppc 约束，还继续进入 `InjectorPositionRegular::getPositionUnitBox(...)` 的 cell 内规则格点生成、`WarpXInitData.cpp::get_nppc()` 的 `split_high_density_boxes` 预估乘积、`AddParticles.cpp::AddPlasma()` 的每 cell 候选粒子枚举数，以及 `PhysicalParticleContainer::SplitParticles()` 的 split-offset 缩放公式
    - 已补清 `<species>.random_theta / do_splitting / split_type` 的更细 runtime 分支：前者现在明确压实到 `AddParticles.cpp` 在每个 cell 只生成一次 `theta_offset` 并统一旋转该 cell 内整组新粒子方位角；后两者则继续压实到 `WarpXParticleContainer::particlePostLocate()` 的跨 level tagging、`PhysicalParticleContainer::Evolve()` 对 `subcycling_half / position_push_type` 的一步末尾 split 调度 gate，以及 `SplitParticles()` 中按维度与 `split_type` 切换 2/4/6/8 子粒子模板、offset 几何和 `wp/np_split` 权重分配
    - 已补清 `<species>.do_continuous_injection / do_backward_propagation` 的更细 runtime 分支：前者现在从 `MultiParticleContainer::{ContinuousInjection,UpdateAntennaPosition,doContinuousInjection}` 的多 container gate，继续压实到 `WarpXMovingWindow.cpp` 对 `particleBox`、`m_current_injection_position` 和实际 `pc.ContinuousInjection(...)` 调度的更新链，以及 `PhysicalParticleContainer::findRefinedInjectionBox()` 中 `moving_window_active + refine_plasma + do_continuous_injection + numLevels()==2` 的 two-level refine-plasma 特例；后者则修正并补清到 `MapParticletoBoostedFrame()` 的真实时序：先算 boosted-frame `tpr/xpr/ypr/zpr` 和 `vxpr/vypr/vzpr`，再按标志翻转 `uz`，最后按这些速度把位置回推到当前 boosted-frame 时间
    - 已补清 `<species>.save_particles_at_xlo/.../eb / do_field_ionization` 的更细 runtime 分支：前者现在从 `ParticleBoundaryBuffer` 构造期的 `m_do_boundary_buffer / m_do_any_boundary` 激活表，继续压实到 `gatherParticlesFromDomainBoundaries()` / `gatherParticlesFromEmbeddedBoundaries()` 为对应 `(boundary,species)` 动态分配 scrape buffer、附加 `stepScraped / timeScraped / nx,ny,nz` 分量，并通过 `filterAndTransformParticles` 收集越界粒子，再交给 `BoundaryScrapingDiagnostics` 消费；后者则从 `InitIonizationModule()` 的 `ionizationLevel`/模块安装，继续压实到 `WarpXEvolve.cpp -> WarpX::doFieldIonization() -> MultiParticleContainer::doFieldIonization()` 的 level-wise 调度，以及 `filterCopyTransformParticles + IonizationTransformFunc()` 把电离产物写入 product species 的主循环
    - 已补清 `<species>.do_adk_correction / physical_element / ionization_product_species / ionization_initial_level` 的更细 field-ionization companion 分支：`do_adk_correction` 现在继续压实到 `adk_correction_factors + ion_atomic_number + GetIntCompIndex("ionizationLevel")` 一起进入 `IonizationFilterFunc`；`physical_element` 则继续压实到 `ion_map_ids / ion_atomic_numbers / ion_energy_offsets` 驱动的电离能与 ADK 系数数组构造，并同时作为氢元素外禁止 correction 的边界；`ionization_product_species` 则继续压实到 `mapSpeciesProduct()` 的 species-ID 绑定和 `CheckIonizationProductSpecies()` 的同 species 禁止；`ionization_initial_level` 继续压实到 `DefaultInitialization.H` 与 `AddParticles.cpp` 对 `ionizationLevel` 初值的真实写入链
    - 已把 `resampling` 的 algorithm-specific companions 正式补成总表条目：`<species>.resampling_algorithm_target_ratio` 现在明确连到 `LevelingThinning` 的 `level_weight = average_weight * target_ratio` 门槛链；`<species>.resampling_algorithm_target_weight / velocity_grid_type / delta_ur / n_theta / n_phi / delta_u` 则继续压实到 `VelocityCoincidenceThinning` 的 `cluster_weight` 上界、spherical/cartesian `VelocityBinCalculator` 几何分派、球坐标角向步长以及直角坐标三向 velocity-bin 尺度构造链
    - 已补清 `<species>.do_not_deposit / do_not_gather / do_not_push` 的更细 runtime 分支：前者现在从 `PhysicalParticleContainer::Evolve()` 对 `deposit_charge/deposit_current` 的关断，继续压实到 `WarpXParticleContainer::{DepositCurrent,DepositCharge,DepositMassMatrices}` 的函数级 early-return，以及 `MultiParticleContainer::{DepositCharge,GetChargeDensity,SortParticlesByBin}` 的整 species 跳过；后两者则分别继续压实到显式/隐式/photon gather 分支里 `doGatherShapeN(*)` 的跳过路径，以及 `PhysicalParticleContainer::Evolve()/PushP()`、`WarpXParticleContainer::PushX()`、`RigidInjectedParticleContainer::PushP()` 等多条 push/position-update 例程的统一 early-return gate
    - 已补清 `<species>.profile / flux_profile / density_min / density_max` 的更细 runtime 分支：`profile` 现在从 `SpeciesUtils::parseDensity()` 的 `constant / parse_density_function / read_from_file` 工厂分派，继续压实到 `InjectorDensity::{prepare,getDensity}` 的文件密度预加载与逐粒子统一取值链；`flux_profile` 则继续压实到 `ContinuousFluxInjection() -> AddPlasmaFlux() -> inj_flux->getFlux(...)` 和 `flux * scale_fac * dt` 的权重生成链；同时 `density_min` 已补到 `ZeroInitializeAndSetNegativeID(...)` 的候选粒子删除路径，以及 `split_high_density_boxes` 预分析中的 `v >= density_min ? nppc : 0` 判定，`density_max` 已补到进入最终 `weight = dens * scale_fac` 前的硬截断链
    - 已补清 `<species>.radial_numpercell_power / momentum_distribution_type` 的更细 runtime 分支：前者现在不只作用于 `AddParticles.cpp` 的径向位置采样和体注入权重修正，也继续进入 `AddPlasmaFlux()` 的 surface-emission 半径采样与 flux 权重修正；后者则从 `SpeciesUtils::parseMomentum()` 的 `InjectorMomentum*` 工厂分派，绠续压实到 ballistic-correction 用到的 `getBulkMomentum(...)` 链，以及 `AddParticles()/AddPlasmaFlux()` 对 `inj_mom->getMomentum(..., engine)` 的逐粒子采样链，其中 `gaussianflux`、Boltzmann、Juttner 分支各自保留专门的法向采样或 Lorentz/flipping 逻辑
    - 已补清 `<species>.theta_distribution_type / beta_distribution_type / zinject_plane / rigid_advance` 的更细 runtime 分支：前两者现在从 `TemperatureProperties / VelocityProperties` 的 `constant / parser` 分派，继续压实到 `GetTemperature / GetVelocity` 的 `ParserExecutor<3>` 编译与方向/符号固化链，再被 `InjectorMomentumBoltzmann / Juttner` 的逐粒子 `getMomentum()` 和 `getBulkMomentum()` 实际消费；后两者则继续压实到 `RigidInjectedParticleContainer::InitData()` 的 boosted-frame 注入平面初始化、`Evolve()` 的 `zinject_plane_levels` 移动与 `done_injecting_lev` 判定，以及 `PushPX()/PushP()` 对未越过注入平面的粒子回退到 `vzbar / vz / v` 三种 rigid-advance 轨迹
    - 已补清 `warpx.num_mirrors / mirror_z / mirror_z_width / mirror_z_npoints` 的更细 mirror runtime 分支：`ApplyMirrors()` 现在明确压实到 boosted-frame 下的 `z_min/z_max_tmp` 平移、`mirror_z_npoints * dz` 的逐 level 最小厚度约束，以及 fine/coarse patch 上 `E/B/F/G` 的 `NullifyMF(...)` 全链路清零
    - 已补清 `algo.load_balance_* / costs_heuristic_* / roundrobin_sfc / split_high_density_boxes*` 的更细 runtime 分支：包括旧 `warpx.*` 别名拒绝边界、`LoadBalanceCosts` reduced diagnostic 对 `load_balance_intervals` 和 heuristic costs 的并行 consumer，以及 `PostProcessBaseGrids()` 与 `MakeDistributionMap()` 在高密度预切分和初始分发策略上的联动
    - 已补清 `warpx.E/B_external_grid / maxlevel_extEMfield_init` 的更细 external-grid runtime 分支：包括 constant branch 对 `*_aux/*_cp/*_avg_*` 的初始化写入、moving-window `shiftMF(...)` 对同一常量数组的复用，以及 `maxlevel_extEMfield_init` 对 constant/parser 两支的 level gate 与 `E/B` parser 非对称边界
    - 已补清 `particles.E/B_ext_particle_init_style` 的更细 external-particle-field runtime 分支：从 `MultiParticleContainer::ReadParameters()` 的 `parser / repeated_plasma_lens / read_from_file` 分派，继续压实到 `ExternalParticleFields::ReadParameters()` 的 named-field/单字段 fallback 与 `read_fields_[EB]_dependency(t)` parser、`WarpX.cpp` 的多分量 `E/B_external_particle_field` 分配、`WarpXInitData.cpp` 的按-component 文件读场，以及 `WarpXComm.cpp::UpdateAuxilaryData()` 按 `time_executor(t_new[lev])` 做 `Saxpy` 叠加到 `Efield_aux/Bfield_aux`
    - 已补清 `fluids.species_names / <fluid>.E/B_ext_init_style` 的更细 fluid runtime 分支：前者现在明确连到 `do_fluid_species` 对 `AllocateLevelMFs / InitData / DepositCharge / DepositCurrent / Evolve` 的全局 gate，后者则压实到 `GatherAndPush()` 中 parser runtime flag、lab-frame 求值和 boosted-frame Lorentz 回变换的两段外场叠加链
    - 已补清 `lasers.deposit_on_main_grid` 的更细 runtime 分支：从 `MultiParticleContainer` 的 laser side-list 回绑，继续压实到 `Partition.cpp` 的 `nfine_current=0` 分区边界，以及 `LaserParticleContainer::Evolve()` 中 `np_to_deposit=0` 后把高层粒子改走 `rho_buf/current_buf -> lev-1` 的 coarse-buffer 沉积分支
    - 已把 `virtual photons` 相邻条目补成完整 companion 簇：`<species>.do_qed_virtual_photons` 现在明确连到 `CollisionHandler::doCollisions()` 每步开头的 `GenerateVirtualPhotons()` 总调度，并补出 `<species>.qed_virtual_photon_species_name / qed_virtual_photons_min_energy / qed_virtual_photons_multiplier` 三条正式 parameter-map 行，分别压实到目标 photon container 绑定、`y_min` 对计数/采样双链的约束，以及“生成数乘 sampling_factor、单粒子权重除 sampling_factor”的 tile 级重建合同
    - 已补清 BTD 相邻 instance-local 条目的更细 runtime 分支：`<diag>.num_snapshots_lab` 现在明确连到 `m_intervals -> m_num_buffers` 和整套 BTD 状态数组尺寸；`dt_snapshots_lab / dz_snapshots_lab` 继续压实到每个 snapshot 的 `m_t_lab` 时间轴与 `final_snapshot_fill_iteration` 估算；`buffer_size` 则进一步连到 buffer 数量、snapshot z 向对齐和运行时 `m_buffer_box` 滑动；`do_back_transformed_fields / do_back_transformed_particles` 也分别压实到 field-side MultiFab/functor 分配链、per-species pinned particle buffer，以及纯粒子 BTD 路径下的几何外壳补建逻辑
    - 已补清 `TimeAveraged` diagnostics 相邻条目的更细 runtime 分支：`<diag>.time_average_mode` 现在明确连到 `DoComputeAndPack()` 的 averaging-window 判据，以及 `Flush()` 在 `m_mf_output` 与 `m_sum_mf_output` 之间的切换和 dynamic 模式写后清零；`average_period_steps / average_period_time` 则继续压实到 dynamic-start 窗口长度、重叠合法性检查和归一化分母；`average_start_step` 则进一步连到 fixed-start 起点合法性与 companion-parameter 忽略边界，而不是已独立 materialize 的 static 非输出步累计 gate
    - 已补清 `amrex.abort_on_out_of_gpu_memory` 的更细 startup 边界：这条参数现在不再停留在泛化性能说明，而是明确压实到 `WarpXAMReXInit.cpp` 的 `override_default_abort_on_out_of_gpu_memory() -> overwrite_amrex_parser_defaults() -> amrex::Initialize(...)` 链，说明 WarpX 会主动把 AMReX 默认 `false` 覆写成默认 `true`，即“默认直接 abort，显式设成 `0` 才回退到 AMReX 的 host-fallback 行为”
    - 已补清 `warpx.compute_max_step_from_btd` 的更细分支语义：这条参数现在不再只停留在“BTD 可反向修改全局运行上界”，而是明确压实到 `BTDiagnostics::DerivedInitData()` 中 `final_snapshot_starting_step / final_snapshot_fill_iteration / final_snapshot_fill_time` 的估算，以及“自动调用 `updateMaxStep/updateStopTime` 上调全局运行长度”与“仅通过 warn_manager 告警而不改动运行上界”这两条分支；同时补清了在 `max_step` 与 `stop_time` 都未显式给出时直接以最后一个 BTD snapshot 的填满步数兜底的路径
    - 已补清 `warpx.always_warn_immediately / abort_on_warning_threshold` 的更细 warning-manager 语义：这两条参数现在不再只停留在 startup 配置与“达到阈值就 abort”的摘要，而是明确压实到 `WarnManager::RecordWarning()` 中“立即经 `amrex::Warning(...)` 打印 vs 仅写入内部 logger 等待汇总”的分叉，以及 threshold-abort 时 abort 文本是否重复携带 `[topic] text`、并由 `ABLASTR_ALWAYS_ASSERT_WITH_MESSAGE` 立即终止的运行语义
    - 已补清 `warpx.used_inputs_file` 的更细 startup 收尾语义：这条参数现在不再只停留在“used-inputs 归档文件名”，而是明确压实到 `WarpXInitData.cpp::WriteUsedInputsFile()` 的默认值与收尾调用时机，以及 `ablastr::utils::write_used_inputs_file(...)` 中 `/dev/null/空串` 早退、用户提示打印、和仅由 `ParallelDescriptor::IOProcessor()` 调用 `ParmParse::prettyPrintUsedInputs(...)` 真正写盘的路径
    - 已补清 `authors` 的更细 writer-side metadata 链：这条参数现在不再只停留在“openPMD 的 author 字符串”，而是明确压实到 `WarpX::ReadParameters()` 对 `m_authors` 的保存、`WarpX.H::GetAuthors()` 的暴露、`FlushFormatOpenPMD.cpp` 构造 `WarpXOpenPMDPlot(...)` 时的透传，以及 `WarpXOpenPMD.cpp` 里仅在 `!m_authors.empty()` 时才调用 `Series::setAuthor(...)` 真正写入 openPMD 元数据头的条件语义
    - 已补清 `amr.restart` 的更细 restart 总分叉与续写语义：这条参数现在不再只停留在 `WarpX::ReadParameters()` 里把路径存进 `restart_chkfile`，而是明确压实到 `WarpXInitData.cpp::InitData()` 的 `InitFromScratch()` vs `InitFromCheckpoint()` 总分支、restart 后的 `PostRestart()` 与 `reduced_diags->InitData()` 初始化链、`WarpXIO.cpp::InitFromCheckpoint()` 对场/PML/reduced-diag checkpoint/粒子和 step-time 状态的恢复链，以及 `ReducedDiags.cpp` 中 `m_write_header = IsNotRestart || !FileExists(...)` 的 header 续写语义和 `write_diagnostics_on_restart` 的首步写出分支；同时补清 restart 分支不会重走 fresh-run 的 `InitDiagnostics()`、`beforeInitEsolve/afterInitEsolve`、space-charge field solve 与 `AddExternalFields(lev)`，而是改成单独触发 `afterInitatRestart`
    - 已补清 `amr.max_grid_size` 的更细 startup 与性能诊断链：这条参数现在不再只停留在 `AMReX/AmrCore-owned input` 与泛化的 RZ spectral 修正摘要，而是明确压实到 `WarpXAMReXInit.cpp` 中 `preparse_amrex_input_int_array(...)` 对 `max_grid_size{,_x,_y,_z}` 的数值化回写、`WarpXUtil.cpp` 在 `while (n_cell[1] < nprocs*mg[0]) mg[0] /= 2` 循环里对 `max_grid_size_y` 的逐步收缩，以及 `WarpXInitData.cpp::PerformanceHints(...)` 里用总 box 数和 MPI ranks 关系发出“增大/减小 `amr.max_grid_size` 与 `amr.blocking_factor`”的性能 warning
    - 已补清 `geometry.dims` 的更细 startup 硬 gate：这条参数现在不再只停留在 `check_dims()` 的“读取并比较”摘要，而是明确压实到 `WarpXInit.cpp` 中按编译宏组装 `dims_compiled`、`WarpX::MakeWarpX()` 在 moving-window/boost/boundary 解析前立即调用这道检查、以及“输入里声明了错误维度”与“完全缺失 `geometry.dims`”两条不同的 `WARPX_ALWAYS_ASSERT_WITH_MESSAGE` abort 文本分支；同时补清了它在 `WarpXInitData.cpp` 中继续作为 geometry 启动摘要打印链的输入
    - 已补清 `geometry.prob_lo/hi` 的更细启动与坐标改写链：这条参数现在不再只停留在 `parse_geometry_input()` 的表达式预解析和泛化的 boost 消费摘要，而是明确压实到 `amrex_post_initialize()` 中对 `prob_lo/prob_hi` 的 `AMREX_SPACEDIM` 长度断言与 parser 回写、`ConvertLabParamsToBoost()` 中 `convert_factor = 1/(gamma_boost*(1-beta_boost*beta_window))` 的坐标缩放公式，以及“若开启 moving window 且命中 `moving_window_dir`，就把 `beta_window` 切到 `moving_window_v/c`”这一特殊分支，并继续同步缩放 `fine_tag_lo/hi` 与 `slice.dom_lo/hi`
    - 已补清 `amr.max_level` 的更细本地 consumer 链：这条参数现在不再只停留在 `WarpXUtil.cpp` 的 refined-patch 条件分支和少数 reduced-diag 的 `max_level+1` 摘要，而是明确压实到 `GuardCellManager.cpp` 中 `(max_level > 0 && do_subcycling)` 触发的额外粒子 push guard-cell 预算、moving-window 下 `max_level+1` 与 `max_level <= 1` 的 grow-cell 限制，以及 `LoadBalanceEfficiency`、`RhoMaximum` 等 reduced-diag 的多层容器展开；同时补清了 `FieldReduction` 读取同一参数后要求 `nLevel == 0`、显式禁止 mesh refinement 的边界
    - 已补清 `warpx.moving_window_dir` 的更细方向性 consumer 链：这条参数现在不再只停留在窗口推进、boost 坐标改写和 BTD 限制摘要，而是明确压实到 `WarpX.cpp` 中 `m_current_injection_position` 所取 `ProbHi/ProbLo` 的注入边界方向、`Diagnostics.cpp` 在 restart 后只沿 `moving_window_dir` 平移 `m_lo/m_hi` 的几何对齐链，以及 `GuardCellManager.cpp` 只对 `ng_MovingWindow[moving_window_dir]` 这一维补 1 个 guard cell 的定向补偿
    - 已补清 `warpx.moving_window_v` 的更细速度 consumer 链：这条参数现在不再只停留在窗口推进、boost 换算和 BTD 节奏摘要，而是明确压实到 `WarpXMovingWindow.cpp` 中连续注入前沿按整 cell 步进的 `new_injection_position` 更新、窗口方向上 `particleBox` 取 `[old,new]` 或 `[new,old]` 的有向区间、`AddParticles.cpp` 中 `moving_sign = (moving_window_v > 0) ? 1 : -1` 的 source 准备链，以及 `RigidInjectedParticleContainer.cpp` 里 `done_injecting_lev` 对 `moving_window_v + beta_boost*c` 符号的结束判据
    - 已补清 `warpx.start_moving_window_step` 的更细调度起点链：这条参数现在不再只停留在 `moving_window_active(step)` 的下边界和 `BTDiagnostics` 必须为 0 的摘要，而是明确压实到 `WarpXEvolve.cpp` 对 `MoveWindow(...)` 的 `moving_window_active(istep[0]+1)` 调度、`PhysicalParticleContainer` 的 refined continuous injection 分支、`FullDiagnostics.cpp` 只在 `moving_window_active(step+1)` 时平移输出几何，以及 `FieldProbe.cpp` 中 `do_moving_window_FP` 还要求 `step > start_moving_window_step` 才开始随窗位移
    - 已补清 `warpx.break_signals / checkpoint_signals` 的更细 signal-handling 运行链：这对参数现在不再只停留在 `ReadParameters()` 的 signal-name 配置表，而是明确压实到 `SignalHandling::InitSignalHandling()` 的 `sigaction` 安装、`CheckSignals()/WaitSignals()` 的 rank-0 接收与 MPI 广播，以及 `WarpX::checkStopSimulation()` 的主 loop 退出条件和 `WarpX::HandleSignals()` 的 `FilterComputePackFlushLastTimestep(...)` / `oncheckpointsignal` 路径
    - 已补清 `warpx.do_moving_window` 的更细 runtime gate：这条参数现在不再只停留在 `read_moving_window_parameters()` 的总开关，而是明确压实到 `WarpX.H` 的 `moving_window_active(step)`、`_arpX.cpp/WarpXMovingWindow.cpp` 的 `moving_window_x` 与注入位置更新链、`WarpXEvolve.cpp` 对连续注入相关分支的调度，以及 `GuardCellManager` 的 guard-cell 预算和 `BTDiagnostics` 的兼容性硬约束
    - 已补清 `warpx.end_moving_window_step` 的更细 runtime gate：这条参数现在不再只停留在 `moving_window_active(step)` 的停止判据，而是明确压实到 `WarpXMovingWindow.cpp::MoveWindow()` 的 start/stop 日志与早退分支、`BTDiagnostics.cpp` 对“boosted-frame diagnostics 期间 moving window 不能停止”的硬约束，以及 `FieldProbe.cpp` 中 `do_moving_window_FP` 只在 `step <= end_moving_window_step` 时继续累计 `move_dist` 的探针平移链
    - 已补清 `warpx.ref_patch_function(x,y,z)` 的更细 refined-patch 打标链：这条参数现在不再只停留在 `ReadParameters()` 的 `makeParser({"x","y","z"})` 构造，而是明确压实到 `WarpX::ErrorEst()` 对 `ParserExecutor<3>` 的逐 cell 求值、各编译维度下的坐标适配，以及“返回 `1` 才真正把 cell 标成 `TagBox::SET`；否则退回 bbox 判忚”的静态 refined-patch runtime 语义
    - 已补清 `warpx.refine_plasma` 的更细 refined continuous-injection 运行链：这条参数现在不再只停留在 `findRefinedInjectionBox()` 的 coarse 级 `fine_injection_box + rrfac` 建立，而是明确压实到 `AddParticles.cpp::AddPlasma()` 的局部 `num_ppc` 倍增与 `getPositionUnitBox(..., rrfac, ...)` 位置加密，以及 `AddPlasmaFlux()` 的 `compute_area_weights(rrfac, flux_normal_axis)` 面积权重修正和 refined `flux_pos` 采样链
    - 已补清 `warpx.n_current_deposition_buffer` 的更细 coarse-buffer 沉积链：这条参数现在不再只停留在 `BuildBufferMasks()` 和 `PartitionParticlesInBuffers()`，而是明确压实到 `WarpX.cpp` 对 `current_buf / rho_buf / current_buffer_masks` 的分配、粒子沉积分流，以及 `WarpXEvolve.cpp -> AddCurrentFromFineLevelandSumBoundary(...) / AddRhoFromFineLevelandSumBoundary(...)` 的 coarse-level 汇总路径
    - 已补清 `warpx.n_field_gather_buffer` 的更细 coarse-aux gather 链：这条参数现在不再只停留在 `BuildBufferMasks()` 和 `PartitionParticlesInBuffers()`，而是明确压实到 `WarpX.cpp` 对 `Efield_cax / Bfield_cax / gather_buffer_masks` 的分配、`WarpXComm.cpp::UpdateAuxilaryData()` 对 coarse auxiliary gather 场的填充、`WarpXRegrid.cpp` 的重建，以及 `PhysicalParticleContainer::Evolve()` 中 fine-gather 与 coarse-gather 两段 `PushPX(..., lev, lev)` / `PushPX(..., lev, lev-1)` 的实际分支
- [x] 建立参数系统第一版人工骨架：新增 `notes/code-reading/utils/01-parser-system.md` 与 `docs/parameter-chapter-index.md`，先把 `ParmParse` 前缀、parser helper、interval 语法、算法枚举入口和一批高频 `待定` 参数的章节归属压实。
- [x] 继续人工校正 `docs/parameter-map.md` 的第二批高频参数：无前缀运行控制、startup debug 参数、`algo.*`、`diagnostics.*`、`warpx.reduced_diags_names` / `reduced_diags.*`。
- [x] 完成 `docs/parameter-map.md` 第三批人工校正：self-fields / magnetostatic、boundary / PML / EB、mirrors / lattice、collision / QED、PSATD、sorting / shared-memory deposition，以及 full diagnostics / BTD / particle-output / restart 参数族。
- [x] 把 `docs/parameter-chapter-index.md` 从批次式人工校正提升为对象前缀导航，补出 `species / laser / diagnostics / collision` 四组子族入口。
- [x] 新增 `notes/code-reading/utils/02-parameter-family-entrypoints.md`，把 `species / laser / diagnostics / reduced diagnostics / collision` 五组参数族的 `global gate / factory dispatch / instance-local parse` 入口压成源码图。
- [x] 扩写 `notes/code-reading/utils/02-parameter-family-entrypoints.md`，补 `boundary / solver / psatd / implicit` 四组参数族的真实入口，把参数索引从容器工厂层推进到 root solver / boundary parse 层。
- [x] 新增 `notes/code-reading/utils/05-deep-solver-object-parameter-families.md`，把 `fluids / hybrid_pic_model / macroscopic / effective potential` 四组参数继续拆到 `object creation / instance-local parse / runtime materialization`。
- [x] 新增 `notes/code-reading/utils/06-external-vector-potential-and-poisson-boundary-parameters.md`，把 `external_vector_potential.*`、`boundary.potential_*` 和 `warpx.eb_potential(x,y,z,t)` 继续拆到 `parent gate / subobject parse / parser build / runtime apply`，并记录 Python 对 `PoissonBoundaryHandler` 的覆盖入口。
- [x] 新增 `notes/code-reading/utils/07-parameter-validation-links-for-boundary-and-external-fields.md`，把 `boundary.potential_*`、open-boundary Poisson、effective-potential 和 `warpx.eb_potential(x,y,z,t)` 接回 `electrostatic_dirichlet_bc`、`open_bc_poisson_solver`、`effective_potential_electrostatic`、`ion_beam_extraction` 四条最稳定 validation 链，并同步清理 `docs/example-regression-map.md` 中 `ion_beam_extraction` 的粗分类条目。
- [x] 继续细化 `docs/parameter-chapter-index.md` 的对象前缀导航：在 `species / laser / diagnostics / collision` 之外，补出 `Collision/QED` 子族、`boundary / solver / psatd / implicit`、`fluids / hybrid / macroscopic / effective potential` 三组更窄入口，形成更稳定的参数跳转层。
- [x] 回到 `docs/parameter-map.md` 做尾项清理，先补一批高置信空源码命中：species 初始化/space-charge/field-ionization/resampling、virtual photons、collision product species、`external_vector_potential.<field_name>.*`、以及 diagnostics / BTD 主参数。
- [x] 新增 `notes/code-reading/utils/08-low-frequency-parameter-families-and-pass-throughs.md`，把 `parameter-map` 最后一批低频空项压成正式源码结论，区分 grouped alias、AMReX-owned pass-through 输入、外场聚合开关、PSATD/centering grouped key、macroscopic/hybrid parser 参数和 Schwinger 区域边界框，并把整张表的空“初步源码命中”列清到 0。
- [x] 人工复核 `docs/example-regression-map.md` 中 `general / to classify` 条目；当前这类顶层粗分类已清到 0，并开始转入成批清理仍写成“checksum 基线；需反查对应 inputs 和分析脚本”的家族条目。
- [ ] 人工复核 `docs/literature-map.md` 中 `待分类` 条目，并标出必须 MinerU 处理的优先级。

### 阶段 0：全源码精读框架落地

- [x] 建立 `docs/warpx-source-reading-framework.md`。
- [x] 为每个顶层模块建立 `notes/code-reading/<module>/README.md`：root、initialization、evolve、particles、fieldsolver、boundary、parallelization、diagnostics、embedded-boundary、filter、laser、fluids、nonlinear-solvers、accelerator-lattice、python、utils、ablastr。
- [x] 在每个模块 README 中记录：构建入口、核心文件、物理/算法主题、精读顺序、正文目标、验证示例。
- [x] 把 `docs/module-inventory.md` 的自动模块名人工合并成框架中的 15 个阶段。
  - 已新增 `框架阶段合并` 总表，给出阶段 `0-14` 的模块归并和文件数
  - 当前 `module-inventory` 已可直接按阶段 0-14 浏览，而不必先手动把自动模块名再翻译一次
- [ ] 为阶段 1-3 建立下一批具体阅读笔记文件。

### 阶段 1：Root / WarpX 主类状态

- [x] 精读 `../warpx/Source/WarpX.H`，按成员类别建立主类状态表。
- [x] 精读 `../warpx/Source/WarpX.cpp`，记录构造、析构、单例、参数读取和全局状态初始化的第一轮证据。
- [x] 精读 `../warpx/Source/Fields.H`，解释 field registry 的类型和命名体系。
- [x] 新建 `notes/code-reading/root/01-warpx-state-map.md`。
- [x] 继续细读 `WarpX::WarpX()` 构造函数，按子系统创建顺序建立第二张状态表。
- [x] 继续细读 `AllocLevelData()` 中 EB、fluid、macroscopic、spectral/coarse solver、buffer 和 level 分配分支的第一轮证据。
- [x] 继续细读 `AllocLevelData()` 中 PML、hybrid、implicit mass matrix、effective potential 的深层分支。
- [x] 回填 `manuscript/chapters/03-warpx-evolve.md` 的 WarpX 主类状态图。
  - [x] 已把构造函数只建跨-level 外壳、`AllocLevelMFs()` 中 `effective potential / hybrid / implicit` 的不同落点，以及 `InitPML()` 作为初始化末段附加边界子系统的顺序，回填到第 3 章。
  - [x] 已继续把这些关系压成更显式的主类状态图/表，而不是只停在文字回填。
- [x] 进入 `Initialization/WarpXInitData.cpp`，把 `InitData()`、`InitFromScratch()`、`InitLevelData()`、`PostRestart()` 和 `CheckGuardCells()` 串成初始化链。

### 阶段 2：Initialization / 初始化链

- [x] 新建 `notes/code-reading/initialization/00-init-callgraph.md`。
- [x] 精读 `WarpX::InitData()` 的 fresh run / restart 分叉和共同后处理。
- [x] 精读 `WarpX::InitFromScratch()` 与 AMReX `MakeNewLevelFromScratch()` 的衔接。
- [x] 精读 `WarpX::InitLevelData()` 中常量/parser/read-from-file 外场初始化的第一轮主链。
- [x] 精读 `WarpX::InitPML()` 和 `CheckGuardCells()` 的第一轮主链。
- [x] 精读 `ExternalField.*`、`LoadExternalFields()` 和 `ReadExternalFieldFromFile()`。
- [x] 精读 `PlasmaInjector.*` 与 `InjectorPosition.H`、`InjectorDensity.H`，建立 species 初始分布源码图谱第一版。
- [x] 精读 `SpeciesUtils::parseDensity()` 和 `SpeciesUtils::parseMomentum()`。
- [x] 精读 `InjectorMomentum.H` 中 constant、gaussian、uniform、Boltzmann、Juttner、parser 的公式和代码。
- [x] 精读 `Particles/ParticleCreation/AddParticles.cpp` 与 `AddPlasmaUtilities.*`。
- [x] 精读 `DivCleaner/ProjectionDivCleaner.*`，推导 projection div cleaner 的离散方程。
- [x] 回填 `manuscript/chapters/03-warpx-evolve.md` 或新初始化章节中的源码块。
- [x] 补读 Gaussian beam 与 openPMD 粒子文件路径的边缘细节，把 `AddGaussianBeam()` 和 `AddPlasmaFromFile()` 从当前主链说明扩展为逐块精读。
- [x] 精读 `TemperatureProperties.*`、`VelocityProperties.*`、`GetTemperature.*`、`GetVelocity.*`。

### 阶段 3：全局时间推进

- [x] 精读 `Evolve/WarpXComputeDt.cpp`，补完 CFL、固定步长、粒子速度、boosted frame 和 solver 限制。
- [x] 新建 `notes/code-reading/evolve/04-compute-dt-and-adaptive-timestep.md`，解释 `ComputeDt()`、`UpdateDtFromParticleSpeeds()`、subcycling 和 `dt_update_interval`。
- [x] 精读 `Evolve/WarpXEvolve.cpp` 中 `OneStep_sub1()` 与 `OneStep_JRhom()`。
- [x] 新建 `notes/code-reading/evolve/03-subcycling-and-jrhom.md`，解释 AMR subcycling 的 fine/coarse 双时间层、current/rho restriction 与 PSATD-JRhom 的多次 `J/rho` 沉积循环。
- [x] 精读 `Utils/WarpXMovingWindow.cpp`，解释 moving window 位置更新、连续注入和 boosted-frame 速度变换。
- [x] 新建 `notes/code-reading/evolve/05-moving-window.md`，解释 `shiftMF()`、`UpdateInjectionPosition()`、`MoveWindow()`、`ShiftGalileanBoundary()`、连续粒子/流体注入和 PML/subcycling 调用点。
- [x] 回填 `manuscript/chapters/03-warpx-evolve.md` 的更完整 `ComputeDt()`、subcycling、JRhom 和 moving window 细节。
  - [x] 已把 `ComputeDt()` 的 solver/geometry 决策表、`const_dt` 与 `dt_update_interval` 互斥边界、moving-window 的 active 区间与 continuous-injection/flux-injection 区分、subcycling 的 coarse/fine current 保存-恢复语义，以及 JRhom 的输入字符串语义与 `current_correction/Vay deposition` 不兼容边界回填到第 3 章。

### 阶段 B：物理和数学基础重写

- [x] 重写 Vlasov 方程章节：相空间守恒、Liouville 图像、碰撞项边界。
- [x] 重写 Vlasov-Maxwell 章节：源项、约束方程、能量/动量守恒。
- [x] 重写 Vlasov-Poisson / electrostatic 极限章节。
- [x] 重写宏粒子、权重、shape factor、噪声和采样误差章节。
  - [x] 已在 `manuscript/chapters/01-kinetic-models.md` 中重写并分层压实：
    - Vlasov 作为相空间守恒律与 Liouville 图像；
    - `C[f] + S - L` 碰撞/源汇边界；
    - `Vlasov-Maxwell` 的源项、约束方程与总能量守恒边界；
    - `Vlasov-Poisson` 作为自洽场闭合的 electrostatic 极限；
    - 宏粒子、非等权粒子、shape factor、采样噪声、Debye/统计时间尺度的文献边界。
- [x] 重写 leapfrog、CFL、Debye 长度、等离子体频率、数值色散章节。
  - [x] 已在 `manuscript/chapters/02-pic-loop.md` 中继续压实：
    - leapfrog 时间层与 `x^n / p^{n+1/2} / J^{n+1/2}` 的最小 runtime contract；
    - `\omega_p` 作为最快 plasma timescale、`\lambda_D` 作为最小 shielding length 的时间/空间分辨率边界；
    - `ComputeDt()` 与 `CartesianYee/Nodal/CKC::ComputeMaxDt()` 所对应的 CFL 决策层；
    - Yee / Nodal / CKC 从差分算子开始改写数值色散合同这一层。
- [x] 为基础章节建立文献清单，优先处理 Birdsall-Langdon、Hockney-Eastwood、Dawson、Yee。
  - [x] 已新增 `docs/foundations-literature-list.md`，把第 1 / 2 章当前真正依托的基础来源压成独立清单，并明确区分：
    - `Birdsall 1985`、`Dawson 1983` 已有本地 PDF / MinerU / 中文精读，可直接作为正文证据；
    - `Hockney-Eastwood` 与 `Yee 1966` 当前仍停留在 acquisition / metadata / abstract-level 边界，不能冒充为已核实一手来源。
  - [x] 已把该清单回链到：
    - `manuscript/chapters/01-kinetic-models.md`
    - `manuscript/chapters/02-pic-loop.md`
    - `docs/literature-map.md`

### 阶段 C：真正样章，PIC loop 与 WarpX 主演化路径

- [x] 重新读取并记录 `../warpx/Source/main.cpp`、`WarpX.H`、`WarpX.cpp`、`Evolve/WarpXEvolve.cpp` 的当日行号。
- [x] 画出完整调用图：`main -> WarpX::GetInstance -> InitData -> Evolve -> OneStep -> Particles/Fields/Diagnostics`。
- [x] 重写 `manuscript/chapters/02-pic-loop.md`，从物理 loop、时间层、离散守恒推到 WarpX 伪代码。
- [x] 重写 `manuscript/chapters/03-warpx-evolve.md`，逐段讲解 `WarpX::Evolve`、`OneStep`、`OneStep_nosub`，并定位 `OneStep_sub1` 与 `OneStep_JRhom` 的后续精读入口。
- [x] 建立 `notes/code-reading/evolve/`，保存逐文件源码阅读笔记。
- [x] 继续把 `manuscript/chapters/03-warpx-evolve.md` 中 `OneStep_sub1()` 和 `OneStep_JRhom()` 从定位说明扩展为逐段精读第一版。
- [x] 从 `PushParticlesandDeposit()` 进入 `MultiParticleContainer::Evolve()`，重写粒子推进和沉积样章的第一版。
- [x] 用 Langmuir 和 uniform plasma 做最小验证记录：命令、环境、输出、物理检查量、源码路径。
  - [x] `Langmuir`：已在 `runs/stage-c-validation/langmuir_1d` 用无沙箱 MPI 实跑 `inputs_test_1d_langmuir_multi`，输出 `diags/diag1000080`；官方 `analysis_1d.py` 因本机缺 `matplotlib/yt` 未原样执行，但其核心物理断言已按同一公式手工复现，得到解析场相对误差 `1.7027848999745115e-3 < 5e-2`、电荷守恒误差 `8.34503170903001e-12 < 1e-11`。
  - [x] `uniform_plasma`：已在 `runs/stage-c-validation/uniform_plasma_2d` 用无沙箱 MPI 实跑 `inputs_test_2d_uniform_plasma`，输出 `diags/diag1000010`；当前本机缺 `yt/openpmd_viewer`，因此这轮没有复跑 `analysis_default_regression.py` 的 checksum，但已确认它本来就是 `analysis=OFF + checksum-only` baseline，应与 `Langmuir` 的强解析断言分级处理。
- [x] 对样章做严格审查：公式、源码行号、参数、示例、文献是否闭环。
  - [x] 本轮先按计划文档锁定样章对象为：
    - `manuscript/chapters/02-pic-loop.md`
    - `manuscript/chapters/03-warpx-evolve.md`
  - [x] 已新增正式审查记录：
    - `docs/sample-chapter-audit-2026-05-18.md`
  - [x] 已按审查结果补入：
    - 源码版本声明
    - 参数示例
    - 最小运行案例
    - 进一步阅读
    - 练习题
  - [x] 当前结论：第 2/3 章已达到计划文档定义的样章可审阅状态；未完成项已前移到更高层的章节扩展审校，而不是继续补样章骨架。

## 后续模块任务

### 粒子系统

- [x] 精读 `MultiParticleContainer`、`PhysicalParticleContainer`、`WarpXParticleContainer` 的显式主链入口。
- [x] 精读 `Particles/Pusher/` 中 Boris、pusher selector 和 position update 的主路径。
- [x] 精读 `Particles/Pusher/UpdateMomentumVay.H` 和 `UpdateMomentumHigueraCary.H`。
- [x] 精读 `Particles/Pusher/` 中 radiation reaction、implicit pusher 和无质量 photon pusher 相关路径。
- [x] 精读 `Particles/Gather/FieldGather.H` 的 `doGatherShapeN()` 主分派、shape 选择和 Cartesian/RZ 主 gather 路径。
- [x] 精读 `Particles/ShapeFactors.H` 的 `Compute_shape_factor` 与 `Compute_shifted_shape_factor`。
- [x] 精读 `Particles/Gather/` 其余维度分支、energy-conserving gather、external particle fields 和 Galerkin/PSATD 组合细节。
- [x] 精读 particle boundaries、boundary buffer、scraping、sorting、resampling、thermalizer。
- [x] 验证：`Examples/Tests/particle_pusher`、`single_particle`、`larmor`、`photon_pusher`。

### 沉积、形函数和守恒

- [x] 推导 charge/current deposition 的离散连续性方程。
- [x] 定位 `WarpXParticleContainer::DepositCharge()` 和 `DepositCurrent()` 的 tile 级入口与算法分派。
- [x] 精读 `Particles/Deposition/ChargeDeposition.H` 的主 shape kernel。
- [x] 精读 `Particles/Deposition/CurrentDeposition.H` 的 direct current kernel。
- [x] 精读 `Particles/Deposition/CurrentDeposition.H` 的 Esirkepov 主 3D old/new shape 差分 kernel。
- [x] 精读 `Particles/Deposition/CurrentDeposition.H` 的 Villasenor、Vay、implicit charge-conserving、RZ/1D/RCYLINDER/RSPHERE 细分路径。
- [x] 精读 mass matrices、temperature deposition、variance accumulation。
- [x] 精读 `SyncCurrentAndRho`、guard/current/rho 同步路径。
- [x] 验证：Langmuir PSATD current correction、Vay deposition tests。

### 场求解器

- [x] 推导 Yee/FDTD 主更新公式，并对照 `EvolveE/B/F/G` 第一轮源码。
- [x] 精读 `WarpXPushFieldsEM.cpp` 顶层 field push 分派。
- [x] 新建 `notes/code-reading/fieldsolver/00-fieldsolver-dispatch.md`。
- [x] 精读 `FiniteDifferenceSolver/EvolveB.cpp` 的 Cartesian 主 kernel 和 algorithm 分派第一轮。
- [x] 精读 `FiniteDifferenceSolver/EvolveE.cpp` 的 Cartesian 主 kernel 和 `F` 修正第一轮。
- [x] 精读 `FiniteDifferenceSolver/EvolveF.cpp` 与 `EvolveG.cpp` 的 divergence-cleaning 标量主 kernel 第一轮。
- [x] 新建 `notes/code-reading/fieldsolver/01-fdtd-evolve-e-b.md`，解释 `CartesianYeeAlgorithm.H`、`CartesianNodalAlgorithm.H`、`CartesianCKCAlgorithm.H` 的 `Upward/Downward` 差分算子、CFL 和 guard cell。
- [x] 推导 CKC/nodal 更新公式第一版。
- [x] 推导 RZ/spherical 更新公式第一版。
- [x] 新建 `notes/code-reading/fieldsolver/04-noncartesian-fdtd.md`，解释 `CylindricalYeeAlgorithm.H`、`SphericalYeeAlgorithm.H`、RZ mode decomposition、轴上正则化、RCYLINDER/RSPHERE 简化和 `EvolveB/E/F`、`ComputeDivE` 的非 Cartesian 分支。
- [x] 精读 FDTD PML 更新第一轮。
- [x] 新建 `notes/code-reading/fieldsolver/02-fdtd-pml.md`，解释 `EvolveBPML.cpp`、`EvolveEPML.cpp`、`EvolveFPML.cpp`、`PMLComponent.H`、PML 参数入口、split-field 存储、`pml_has_particles` 电流项和 Cartesian-only 边界。
- [x] 精读 `BoundaryConditions/PML.cpp`、`PML_current.H` 与 PML damping/sigma profile/current helper 第一轮。
- [x] 新建 `notes/code-reading/fieldsolver/03-pml-damping-current.md`，解释 `SigmaBox`、`ComputePMLFactorsE/B()`、`DampPML()`、`DampJPML()`、`PML_current.H` 和 `PML::Exchange()`。
- [x] 推导 PSATD 和 Galilean PSATD 第一版。
- [x] 新建 `notes/code-reading/fieldsolver/05-psatd-spectral-flow.md`，解释 `WarpX::PushPSATD()` 主流程、`SpectralSolver` 算法分派、`SpectralFieldData` FFT 容器、`SpectralKSpace` k 向量和 staggered shift 第一轮。
- [x] 精读 `PsatdAlgorithmGalilean.cpp` 系数初始化、current correction、Vay deposition 第一轮。
- [x] 新建 `notes/code-reading/fieldsolver/06-psatd-galilean-current-correction.md`，解释 `C/S_ck/T2/X1-X4`、零模极限、current correction、`update_with_rho` 和 Vay spectral deposition。
- [x] 精读 `PsatdAlgorithmJRhomFirstOrder/SecondOrder` 与 `OneStep_JRhom()` 的源码对应。
- [x] 新建 `notes/code-reading/fieldsolver/07-psatd-jrhom.md`，解释 `psatd.JRhom` 参数、`OneStep_JRhom()` 多次 `J/rho` 沉积、谱数组 `old/mid/new` 时间层、一阶/二阶 JRhom 更新式、`Y1-Y8` 系数和 unsupported 组合。
- [x] 读取 `Tools/Algorithms/psatd.ipynb`，对照解析推导补充系数来源。
- [x] 精读 `SpectralSolverRZ`、Hankel transform 和 RZ PSATD/PML 第一轮。
- [x] 新建 `notes/code-reading/fieldsolver/08-psatd-rz-hankel.md`，解释 `n_rz_azimuthal_modes`、`SpectralFieldDataRZ` 的 Hankel+FFT 流、`SpectralHankelTransformer` 的 scalar/vector 变换、`HankelTransform` 的 Bessel roots/SVD/GEMM、`PsatdAlgorithmRZ` 更新式、RZ current correction、Galilean RZ 和 RZ PML。
- [x] 精读 `ElectrostaticSolvers/` 与 `MagnetostaticSolver/` 第一轮。
- [x] 新建 `notes/code-reading/fieldsolver/09-electrostatic-magnetostatic.md`，解释 `WarpXSolveFieldsES.cpp`、Poisson 边界处理、`LabFrameExplicitES`、`RelativisticExplicitES`、`EffectivePotentialES`、`MagnetostaticSolver`、vector potential 边界条件和 `B=curl A` post callback。
- [x] 回填 `manuscript/chapters/06-field-solvers.md` 的 6.9 静电/静磁小节。
- [x] 精读 `ImplicitSolvers/` 与 `HybridPICModel/` 第一轮。
- [x] 新建 `notes/code-reading/fieldsolver/10-implicit-and-hybrid.md`，解释 `ImplicitSolver`、`WarpXSolverVec`、`ThetaImplicitEM`、`SemiImplicitEM`、`StrangImplicitSpectralEM`、`WarpXPushFieldsHybridPIC.cpp` 和 `HybridPICModel/*`。
- [x] 新建 `notes/code-reading/fieldsolver/11-psatd-coefficient-derivation.md`，解释 `Tools/Algorithms/psatd.ipynb` 的线性系统、齐次/非齐次解、源项多项式和系数表抽取。
- [x] 新建 `notes/code-reading/nonlinear-solvers/00-solver-abstractions.md`，解释 `NonlinearSolver`、`LinearSolver`、`Preconditioner`、`PicardSolver`、`NewtonSolver`、`WarpX_PETSc.cpp`、`MatrixPC.H` 和 `CurlCurlMLMGPC.H`。
- [x] 新建 `notes/code-reading/nonlinear-solvers/01-newton-picard.md`，解释 Picard 固定点迭代、Newton 残差线性化、`ComputeRHS()` 契约和 PETSc SNES / KSP 残差回调。
- [x] 新建 `notes/code-reading/nonlinear-solvers/02-preconditioners-and-petsc.md`，解释 `MatrixPC`、`CurlCurlMLMGPC`、PETSc 向量/矩阵桥接和隐式电磁预条件器结构。
- [x] 新建 `notes/code-reading/fieldsolver/12-hybrid-pic-model-deep-dive.md`，解释 hybrid PIC 的广义 Ohm 定律、离子/电子电流分裂、B 场 RK 子步、电子压力闭合和外部矢势分裂场。
- [x] 回填 `manuscript/chapters/06-field-solvers.md` 的 6.10 Hybrid PIC 小节。
- [x] 新建 `notes/code-reading/fieldsolver/13-fieldsolver-verification-map.md`，索引 `nci_fdtd_stability`、`nci_psatd_stability`、`electrostatic_sphere`、`implicit` 和 `ohm_solver_*` 的 CMake 注册、输入文件、分析脚本与 checksum 路径。
- [x] 新建 `notes/code-reading/fieldsolver/14-fieldsolver-analysis-criteria.md`，精读 NCI FDTD/PSATD、electrostatic sphere、implicit EM 和 hybrid Ohm solver 的 analysis 判据、容差、源码覆盖和 assert/checksum/可视化分层；按用户要求未运行本地 WarpX 二进制测试。
- [x] 验证：`nci_fdtd_stability`、`nci_psatd_stability`、`electrostatic_sphere`、`implicit`、`ohm_solver_*`。
  - [x] 已把 `13-fieldsolver-verification-map.md`、`14-fieldsolver-analysis-criteria.md` 与第 6 章 `6.11` 收口成统一验证树，明确区分：
    - `FDTD/PSATD NCI` 的场能/`divE-rho` 断言；
    - `electrostatic_sphere` 的解析场 L2 与能量账本；
    - `implicit` 的总能量、Gauss-law RMS、Newton/GMRES 迭代数；
    - `ohm_solver_*` 中脚本级强断言与 checksum/可视化回归的边界。
  - [x] 这一项当前按源码与 analysis 脚本精读完成；仍未运行本地 WarpX 二进制。

### 边界、嵌入边界、AMR 和并行

- [x] 建立 `notes/code-reading/boundary/00-field-boundary-parameters.md`，解释 `FieldBoundaries.*`、`ParticleBoundaries.cpp`、`WarpX.cpp` 的解析顺序、periodic 一致性约束、默认 periodic 继承和 `WarpXFieldBoundaries.cpp` 的第一层边界分派。
- [x] 建立 `notes/code-reading/boundary/01-pml-data-and-update.md`，解释 `PML.H`、`PML.cpp`、`WarpXEvolvePML.cpp`、`PML_current.H`、`WarpX_PML_kernels.H` 中的 PML BoxArray、`SigmaBox`、split-field 阻尼和 PML current 更新。
- [x] 建立 `notes/code-reading/boundary/02-pec-insulator-silver-mueller.md`，解释 `WarpX_PEC.cpp`、`PEC_Insulator.cpp`、`WarpXFieldBoundaries.cpp` 中 PEC/PMC 的 E/B 奇偶规则、rho/J 镜像沉积、PECInsulator parser 边界和值以及 `crop_on_PEC_boundary` / Silver-Mueller 的实现边界。
- [x] 建立 `notes/code-reading/boundary/03-boundary-parameter-table.md`，汇总 `boundary.field_*`、`boundary.particle_*`、`boundary.potential_*`、PECInsulator parser、`particles.crop_on_PEC_boundary` 与 PML 参数的默认值、适用范围、联动约束和源码入口。
- [x] 建立 `notes/code-reading/boundary/04-silver-mueller-internal-stencil.md`，解释 `ApplySilverMuellerBoundary.cpp` 中 Yee-only 限制、最内侧 guard cell 更新、Cartesian 边界递推系数，以及 RZ / cylindrical 分支的 `dz` 与 `1/r` 几何项。
- [x] 建立 `notes/code-reading/embedded-boundary/00-eb-initialization.md`，解释 `Enabled.*` 的运行时 EB 开关、`WarpX::InitEB()` 的 AMReX EB2 构建路径、`ComputeDistanceToEB()` 的 signed-distance 场，以及 `EmbeddedBoundaryInit.*` 中 reduced particle shape、stair-case update 与 ECT edge/face update 标记初始化。
- [x] 建立 `notes/code-reading/embedded-boundary/01-face-extensions.md`，解释 `S_stab` 最小稳定面积、`flag_info_face/flag_ext_face` 语义、one-way / eight-ways extension、BCK fallback，以及 `FaceInfoBox` / `area_mod` / `m_borrowing` 如何进入 ECT `B` 更新。
- [x] 建立 `notes/code-reading/embedded-boundary/02-particle-scraping-and-deposition-near-eb.md`，解释 `scrapeParticlesAtEB()` 的 nodal signed-distance 判定、`DistanceToEB` 法向重建、`ParticleBoundaryProcess::Absorb()` 的 invalid-id 语义，以及 `save_particles_at_eb` / `ParticleBoundaryBuffer` 的交点回溯、时间戳和法向记录。
- [x] 建立 `notes/code-reading/parallelization/00-guard-cell-model.md`，解释 `GuardCellManager` 中 `ng_alloc_*` 与 `ng_Field*` / `ng_UpdateAux` / `ng_MovingWindow` 的分工、粒子 shape / subcycling / moving window / PSATD / filter 对 guard-cell 配额的影响、`FillBoundaryE/B/F/G/Aux` 的 copy/sync 语义、`WarpXSumGuardCells` 的 accumulation 语义，以及 `SyncCurrent()` / `SyncRho()` 的 finest-to-coarsest 与 owner-mask 去重结构。
- [x] 建立 `notes/code-reading/parallelization/01-current-rho-sync-paths.md`，解释 `SyncCurrent()` / `SyncRho()` 的 finest-to-coarsest 级联、`mf_comm`、`OwnerMask` 去重、`RestrictCurrentFromFineToCoarsePatch` / `AddCurrentFromFineLevelandSumBoundary`、`ApplyFilterandSumBoundaryRho` 与对应 coarse-patch / buffer-patch 源项路径。
- [x] 建立 `notes/code-reading/parallelization/02-regrid-and-load-balance.md`，解释 `CheckLoadBalance()` 的触发条件、SFC/knapsack 候选映射、`load_balance_efficiency_ratio_threshold` 的采纳逻辑、`RemakeLevel()` 当前只支持同 `BoxArray` 的 `DistributionMapping` 重映射、fields/EB/PSATD/buffer masks/particle boundary buffer/diagnostics 的整体重建，以及 heuristic / timer 两类 costs 更新模型。
- [x] 建立 `notes/code-reading/parallelization/03-amr-coarse-fine-substitution.md`，解释 `amr.rst` 的 substitution 公式、`UpdateAuxilaryData*()` 的 `aux = fp + I(parent_aux-cp)` 主链、`E/Bfield_cax` 的 coarse-aux 副本角色、`gather/current buffer masks` 的 transition-zone 语义，以及 `PartitionParticlesInBuffers()` 如何把粒子按 fine / lower-level gather-deposit 路径稳定分区。
- [x] 建立 `notes/code-reading/parallelization/04-warpxcomm-kernel-execution-model.md`，解释 `WarpXComm_K.H` 中 coarse-fine / centering kernel 的分层、`MFIter + Array4 + ParallelFor` 的统一执行壳、`TilingIfNotGPU()` / `Gpu::notInLaunchRegion()` / OpenMP 条件并行的 CPU-GPU 双栈写法，以及 `FillBoundary` 的 `do_single_precision_comms` / `nodal_sync` / `m_safe_guard_cells` 通信策略分支。
- [x] 回到 `Particles/Gather` 与 `Particles/Deposition`，把 `aux` / buffer masks / `PartitionParticlesInBuffers()` 如何进入具体粒子 kernel 再向下打穿。
- [x] 继续细读 `Particles/Deposition/CurrentDeposition.H` 中 Villasenor、Vay、implicit charge-conserving 路径在 AMR coarse-fine buffer 下的具体差异。
- [x] 继续逐段拆解 `CurrentDeposition.H` 中 Villasenor / Esirkepov 的 cell-crossing、old/new shape arrays 与 tighter stencil 本体实现。
- [x] 继续精读 `CurrentDeposition.H` 中 Vay deposition 的 `D`-field / temporary-array 路径，解释它与 Direct / Esirkepov / Villasenor 的根本区别。
- [x] 回到 `Particles/` 上层，补 `particle class / attribute map`，系统梳理 `x_n`、`ux_n`、`prev_x`、`opticalDepthQSR`、runtime attrib 与 species 容器层次。
- [x] 继续精读 `Particles/Pusher/` 中 radiation reaction、implicit pusher 和 photon pusher 的更深层细节，把 `x_n/ux_n/nsuborbits` 属性图继续接到实际 kernel。
- [x] 继续精读 `Particles/Pusher/ImplicitPushPX.cpp` 的 mass-matrices、linear-stage-of-JFNK、suborbit deposition 与 unconverged-particle 电流处理细节。
- [x] 继续精读 `ImplicitSolver::ComputeJfromMassMatrices()`、`PrepareForLinearSolve()`、`ScaleMassMatricesForPC()`，把 implicit 粒子响应如何进入场方程矩阵/预条件器再向下打穿。
- [x] 继续精读 `JacobianFunctionMF`、`ThetaImplicitEM::ComputeRHS()` / `SemiImplicitEM::ComputeRHS()` 与 `MatrixPC/CurlCurlMLMGPC` 的 operator apply，把 residual -> linear operator -> preconditioner 的完整消费链闭合起来。
- [x] 继续精读 `StrangImplicitSpectralEM::ComputeRHS()`、`WarpX_PETSc.cpp` 中 `assemblePCMatrix()` / SNES Jacobian callback、以及 `MatrixPC::Assemble()` 的稀疏矩阵写入细节，把 `pc_petsc` 路径再向下打穿。
- [x] 继续精读 `WarpXSolverDOF` 的 local/global 编号规则，以及 `MatrixPC::Assemble()` 在 3D / RZ / RCYLINDER 下的 curl-curl 与 mixed-derivative 具体行写入模式，把 PETSc 稀疏矩阵装配链再细化一层。
- [x] 继续精读 `GetCurl2BCmask()` 的边界 mask 生成规则、`GetMassMatricesPCnComp()`/`sigma_ii` 的窗口宽度来源，以及 `assemblePCMatrix()` 到 `MatSetValues()` 的 row ownership / host-device 搬运细节，把 `pc_petsc` 的矩阵条目生成与提交链完全闭合。
- [x] 继续把 `pc_petsc` 支线接回验证层：精读 `Examples/Tests/implicit/` 里的 `petsc_matrix`、`planar_pinch` 等 analysis 脚本，明确哪些硬断言在验证 DOF 映射、矩阵装配、预条件器和能量守恒。
- [x] 继续精读 `analysis_vandb_jfnk_2d.py`、`analysis_vandb_jfnk_2d_cropping.py` 与对应输入，把 `JFNK + Villasenor + cropping/filtering` 这条验证支线也映射到 `CurrentDeposition`、suborbit 和 charge-conservation 源码链。
- [x] 继续回到 `Particles/` 与 `Boundary/` 源码层，把 `particles.crop_on_PEC_boundary`、absorbing particle boundaries、sorting/buffer 与 Villasenor / suborbit 的交界细节写成正式笔记，并与这批 regression 互相链接。
- [x] 继续沿 `ParticleBoundaryBuffer` 与 diagnostics 的消费侧推进，精读 `BoundaryScrapingDiagnostic`、Python particle-boundary buffer 接口与 scraped particle 输出链。
- [x] 建立 `notes/code-reading/diagnostics/00-boundary-scraping-diagnostics-python.md`，梳理 `BoundaryScrapingDiagnostics`、`ParticleBoundaryBuffer`、Python wrapper 与 PICMI `ParticleBoundaryScrapingDiagnostic` 的统一消费链，并回填第 8 章。
- [x] 继续进入 `Diagnostics/` 主线第一层，精读 `MultiDiagnostics` / `Diagnostics` 基类调度、`FullDiagnostics` / `ParticleDiag`，建立普通 diagnostics 的 init/compute/flush 骨架，并澄清 full diagnostics 的粒子输出默认不是独立 particle buffer。
- [x] 继续精读 `ComputeDiagFunctors/`、`ParticleReductionFunctor`、`JFunctor/RhoFunctor/PhiFunctor` 与 `ParticleIO` / `WarpXOpenPMD`，把字段计算、粒子过滤与 writer 落盘三层真正拆开。
- [x] 继续进入 `ReducedDiags/`、checkpoint/restart、`FlushFormats/` 与 `BTDiagnostics`，补全 diagnostics 模块剩余分支并与第 8 章案例部分对齐。
- [x] 继续精读 `FieldProbe`、`ParticleHistogram(2D)`、`LoadBalanceCosts/LoadBalanceEfficiency` 与相关 examples/regressions，把 diagnostics 模块从框架层推进到代表性案例层。
- [x] 继续把 `Diagnostics/` 里的 `openPMD` / plotfile / checkpoint 三类 writer 做最小输入-输出对照，并补 `FieldProbe`、`ParticleHistogram2D`、`LoadBalanceCosts` 的可运行案例说明。
- [x] 继续补一组真正并排的 writer 落盘目录树与读取方式示意，把 `plotfile/openPMD/checkpoint` 的文件层级、典型读取工具和适用场景压缩成书稿中的一页对照。
- [x] 继续把 diagnostics 模块补成固定模板化案例页：每类输出给出“最小输入片段 + 目录树 + 读取入口 + 适用场景”的统一排版，并补一个 `BoundaryScraping/openPMD` 例子。
- [x] 继续补一个最小 Python callback / `get_particle_boundary_buffer()` 边界消费案例，把 `BoundaryScrapingDiagnostics` 的文件化路径和 Python 即时消费路径并排收尾。
- [x] diagnostics 模块阶段性收尾后，切回 `Initialization/`，补 AMReX init / WarpX init / species-profile-temperature-velocity 的源码精读回合。
- [x] 继续沿 `Initialization/` 启动层往下，把 `WarpXAMReXInit.*` / `WarpXInit.*` 与 `WarpX::ReadParameters()`、boosted-frame 参数转换、RZ spectral gridding 约束之间的交界再细化一层。
- [x] 继续把 `Initialization` 启动层接回 `ReadParameters()` 主体，补 solver/grid/boost/moving-window 参数是怎样真正落到 `WarpX` 成员和后续容器创建条件上的。
- [x] 继续沿 `ReadParameters()` 主体细化 particle/grid/filter/current-centering/implicit 组合约束，把它们和 `MultiParticleContainer`、`ProjectionDivCleaner`、field allocation 前置条件进一步接起来。
- [x] 继续把这组组合约束向后追到 `AllocLevelMFs()` 的更细分支：external particle fields、`rho/F/G` 分配条件、`HybridPICModel` / fluid / macroscopic / EB 特例，以及它们与第 3A 章后半初始化主链的接缝。
- [x] 继续把 `Initialization` 启动层和后半主链彻底闭合：补 `InitData()` 后半的 `ComputeSpaceChargeField()`、`AddExternalFields()`、`m_electrostatic_solver->InitData()`、`m_hybrid_pic_model->InitData()`、callback 与 diagnostics 初始输出之间的顺序和责任边界。
- [x] 回头系统整理 `Initialization` 章节的验证入口：`langmuir`、external field、Gaussian beam、openPMD 粒子注入、projection div cleaner 等例子的源码-输入-分析脚本映射，并决定先继续 initialization 验证层。
- [x] 继续补 `Initialization` 验证层里尚未压入正式笔记的入口：`load_external_field`、`relativistic_space_charge_initialization`、`open_bc_poisson_solver`，并同步清理 `docs/example-regression-map.md` 中 initialization 相关的 `general / to classify` 条目。
- [x] 继续把 initialization 相关的 examples/regressions 分类补完到 `docs/example-regression-map.md`：`load_density`、`magnetostatic_eb`、`nodal_electrostatic`，并判断它们是否也应并入第 3A 章验证地图。
- [x] 判断 `Initialization` 验证层是否已经阶段性收口；若可以收口，则切回下一未完成模块，并在 `README.md` / `TODO.md` 中明确新的主推进方向。
- [x] 启动 `Laser/` 第一轮源码精读：补 `LaserProfiles.H`、三类 profile 字典和 `LaserParticleContainer` 构造期分派，形成第一篇正式笔记并把关键参数同步到 `docs/parameter-map.md`。
- [x] 继续精读 `LaserProfileGaussian.cpp`、`LaserProfileFromFile.cpp` 和 `LaserParticleContainer::InitData()/Evolve()/ContinuousInjection()`，补第二篇 laser 笔记并扩写书稿中的 laser 初始化正文。
- [x] 继续下钻 `LaserProfileFieldFunction.cpp`、`update_laser_particle(...)`、`ComputeWeightMobility(...)` 和 `calculate_laser_plane_coordinates(...)`，把 parser profile 与人工天线粒子更新 kernel 的最后一层补齐，并继续细化 laser regression 映射。
- [x] 继续细化 `Laser` 的验证层：补 `laser_acceleration`、implicit laser injection、boosted / MR 相关 inputs/analysis/checksum 映射，并判断哪些条目有真实物理断言、哪些仍主要依赖 checksum。
- [x] 继续沿 `Laser` 与全局几何/外场交界推进，精读 `ExternalField.*`、`Utils/WarpXMovingWindow.cpp` 与 laser continuous injection / boosted-frame / AMR 的另一侧耦合，并把对应 examples/regressions 接回 `docs/example-regression-map.md`。
- [x] 继续沿 `Laser` 应用层推进，精读 `Examples/Physics_applications/laser_ion/`、`free_electron_laser/` 或 `laser_on_fine`，把 laser 注入主链如何进入具体应用/diagnostics 场景压成下一篇笔记，并继续细化 `docs/example-regression-map.md`。
- [x] 从 `Laser` 切向多物理/束流分叉：优先沿 `laser_ion -> field_ionization / collisions / QED`，或沿 `free_electron_laser -> rigid injection / BTD / external particle field` 继续展开下一篇正式笔记。
- [x] 继续从 `Laser` 切向多物理/束流分叉：优先沿 `laser_ion -> field_ionization / collisions / QED`，把 laser 驱动 target 的另一条链压成正式笔记，并继续细化相关 regression。
- [x] 继续从 `Laser` 切向多物理/束流分叉：在 `laser_ion` 之后优先进入 `Particles/Collision`、`field_ionization` 或 `QED` 主模块，把目前这篇“应用入口级”分叉继续打到源码实现和验证细节层。
- [x] 继续沿 `Particles/` 多物理主线推进：优先进入 `Particles/Collision` 或 `QED`，把 `field_ionization` 之外的入口也补成正式笔记，并继续清理相关 regressions 索引。
- [x] 继续沿 `Particles/` 多物理主线推进：在 collision 入口之后优先进入 `QED`，或继续下钻 `BinaryCollision` / `BackgroundMCC` / `PulsedDecay` 的实现细节，并继续清理相关 regressions 索引。
- [x] 继续沿 `Particles/` 多物理主线推进：在 QED 入口之后继续下钻 `QEDPhotonEmission.H` / `QEDPairGeneration.H` / `QEDInternals/*`，或回到 `BinaryCollision` / `BackgroundMCC` / `PulsedDecay` 的实现细节，并继续清理相关 regressions 索引。
- [x] 继续沿 `Particles/` 多物理主线推进：在 QED kernel/wrapper 入口之后，继续下钻 `QEDInternals/*.cpp` 的 builtin/load/generate table 生成与序列化，或切回 `BinaryCollision` / `BackgroundMCC` / `PulsedDecay` 的实现细节，并继续清理相关 regressions 索引。
- [x] 继续沿 `Particles/` 多物理主线推进：在 QED table 生命周期之后，继续下钻 `QedChiFunctions.H`、virtual photons、`linear_breit_wheeler` 与 `ElementaryProcess` QED 主链的交界，或切回 `BinaryCollision` / `BackgroundMCC` / `PulsedDecay` 的实现细节，并继续清理相关 regressions 索引。
- [x] 继续沿 `Particles/` 多物理主线推进：在明确 QED / virtual-photon / binary-collision 分叉之后，继续下钻 `BinaryCollision` / `BackgroundMCC` / `PulsedDecay` 的具体实现，或继续追 `linear_compton`、`ParticleCreationFunc` 与 product-species 动量初始化细节，并继续清理相关 regressions 索引。
- [x] 继续沿 `Particles/` 多物理主线推进：在 `BinaryCollision -> ParticleCreationFunc` 主链已经打通后，继续下钻 `BackgroundMCC` / `PulsedDecay` / DSMC `SplitAndScatterFunc` 的实现细节，并继续清理相关 regressions 索引。
- [x] 继续沿 `Particles/` 多物理主线推进：在 `BackgroundMCC` / `PulsedDecay` / DSMC 三条分叉已经打通后，继续下钻 pairwise Coulomb / bremsstrahlung / `background_stopping` / `nuclearfusion` 等尚未成文的碰撞实现，并继续清理相关 regressions 索引。
- [x] 继续沿 `Particles/` 多物理主线推进：在 collision 主分叉基本成文后，继续下钻 resampling / thermalizer / sorting 性能层，并继续清理相关 regressions 索引。
- [x] 继续沿 `Particles/` 多物理主线推进：在 resampling / thermalizer / sorting 已成文后，继续补 `particle_thermalizer` 缺失的 example-level 验证入口，并清理 `capacitive_discharge`、`resampling/*` 和通用 checksum helper 的剩余粗分类条目。
- [x] 继续沿 `Particles/` 主线推进：回到 `Particles/Gather/`，补 `FieldGather.H` 的其余维度分支、energy-conserving gather、external particle fields 和 Galerkin/PSATD 组合细节，并同步继续清理对应 example/regression 粗分类条目。
- [x] 继续沿 `Particles/` 主线推进：补 `Examples/Tests/particle_pusher`、`single_particle`、`larmor`、`photon_pusher` 这一组验证入口，并继续清理 `example-regression-map.md` 里对应的粗分类条目。
- [x] 继续沿 `Particles/` 主线推进：补 `particle_fields_diags`、`plasma_lens`、`pass_mpi_communicator` 等仍停留在粗分类的粒子相关 validation 条目，并判断哪些应回填第 4 章。
- [x] 继续沿 `Particles/` 主线推进：补 `particle_boundary_scrape`、`particle_data_python`、`particle_fields_diags` single-precision FIXME 等仍未压实的粒子 diagnostics / Python 接口 validation 条目。
- [x] 继续沿 `Particles/` 主线推进：补 `particle_boundary_interaction`、`particle_boundary_process`、`particle_thermal_boundary`、`plasma_lens_python` 等仍停留在粗分类的粒子边界 / Python-interface validation 条目，并继续清理 `particle_data_python` unique 变体这类“测试名存在但输入未真正分叉”的验证缺口。
- [x] 继续沿 `Particles/` 主线推进：补 `particle_absorbing_boundary` 辅助绘图脚本、`point_of_contact_eb`、`particle_boundary_process` 的 remaining checksum 边界，以及 `particles_in_pml` / `subcycling` / `MR` 相关粒子验证条目，继续压缩 `example-regression-map.md` 里的粗分类残留。
- [x] 继续沿 `Particles/` 主线推进：补 `particle_absorbing_boundary` 的辅助绘图脚本、`point_of_contact_eb` 的 RZ/3D checksum 对照尾项，以及 `point_of_contact_eb` 之外剩余 `embedded_boundary` / `particles_in_pml` / `Langmuir MR` 相关粗分类条目，作为 `Particles` validation 这阶段的最后清扫。
- [x] 验证：boundaries、PML、particles_in_pml、embedded_boundary、subcycling、MR Langmuir tests。

### 初始化、参数、激光和外场

- [x] 继续沿项目主线推进：从 `Particles` validation 阶段性收口后切回 `Initialization/`，补 `electrostatic_sphere`、`embedded_boundary` 初始化相关 remaining validation 条目，或继续深化 AMReX init、WarpX init、species/profile/temperature/velocity 与参数索引。
- [x] 继续沿 `Initialization/` validation 推进：补 `electrostatic_dirichlet_bc`、`effective_potential_electrostatic`、`electrostatic_sphere` 其余 checksum / helper 条目，继续清理 `example-regression-map.md` 中仍停留在 `electrostatic / Poisson` 粗分类的初始化回归项。
- [x] 继续沿 `Initialization/` validation 推进：补 `electrostatic_sphere` / `electrostatic_dirichlet_bc` / `effective_potential_electrostatic` 之外剩余 `electrostatic / Poisson` 粗分类条目，压实 `nodal_electrostatic`、`open_bc_poisson_solver` 与 `relativistic_space_charge_initialization`，把 collocated zero-trigger baseline、open-boundary FFT/sliced-FFT Poisson 初始化和 relativistic Gaussian-beam self-field 从过粗分类里拆开。
- [x] 建立所有高频 `ParmParse` 参数到章节的稳定索引，并把人工章节索引推进到 `species / laser / diagnostics / collision / boundary / solver / psatd / implicit / fluids / hybrid / macroscopic / effective potential` 这一层可稳定跳转，同时把 grouped alias / pass-through 参数的边界写回源码笔记与第 3A 章。
- [x] 继续把 `docs/parameter-map.md` 从早期计划编号迁到真实书稿章节；本轮已补完先前收束的 `collision` 细项、writer backend / particle-output 细项，以及一批 `species` runtime 标志，并把 `species / laser / diagnostics / reduced_diags / collision / external_vector_potential / load_balance` 这一组高频参数族的空源码入口清到 0。
- [x] 继续沿参数系统主线收尾：当前 `parameter-map` 空源码入口已清到 0；本轮已把 `external_vector_potential.*` 的验证边界继续压实到 `ohm_solver_cylinder_compression` 这组 hybrid PIC PICMI tests，明确它们提供最近的 runtime coverage，但 `analysis=OFF`、仍只有 checksum baseline，因此不能冒充独立强 regression。
- [x] 继续沿参数系统主线收尾：已把 `hybrid PIC / Ohm solver` 这组回归索引进一步拆细，明确区分 `ohm_solver_em_modes`、`ion_beam_instability`、`ion_Landau_damping`、`magnetic_reconnection`、`cylinder_compression` 之间的 assert/checksum/可视化分层。
- [x] 继续沿参数系统主线收尾：已把 `pierce_diode`、`spacecraft_charging`、`particle_boundaries`、`field_probe` 四组从 `general / to classify` 中拆出，分别压实为 Child-Langmuir diode、spacecraft charging、domain particle boundary semantics 与 reduced-diagnostic FieldProbe diffraction regression。
- [x] 继续沿参数系统主线收尾：已把 `flux_injection`、`gaussian_beam`、`projection_div_cleaner`、`space_charge_initialization` 四组从 `general / to classify` 中拆出，并把 `NFluxPerCell`、Gaussian-beam photon/PICMI 变体、projection-cleaner script-local assert、lab-frame self-field 这几条更细的初始化合同回填到第 3A 章和 `initialization/14`。
- [x] 继续沿参数系统主线收尾：已把 `btd_rz`、`collider_relevant_diags`、`diff_lumi_diag` 三组从 `general / to classify` 中拆出，分别压实为 `RZ BackTransformed diagnostics`、`ColliderRelevant` 和 `DifferentialLuminosity(2D)`，并把 reduced diagnostics / BTD 的强 analysis 合同回填到 diagnostics 笔记与第 8 章。
- [x] 继续沿参数系统主线收尾：已把 `divb_cleaning`、`dive_cleaning`、`initial_distribution`、`initial_plasma_profile` 四组从 `general / to classify` 中拆出，分别压实为 `div(B) cleaning`、`div(E) cleaning / PML`、`particle distributions` 和 `parabolic-channel plasma profile`，并把对应初始化/field-solver 合同回填到 `initialization/14`、`fieldsolver/13` 与第 3A 章。
- [x] 继续沿参数系统主线收尾：已把 `radiation_reaction`、`repelling_particles`、`secondary_ion_emission` 三组从 `general / to classify` 中拆出，分别压实为 `classical radiation reaction`、`two-particle electrostatic self-field repulsion` 和 `embedded-boundary secondary ion emission / Python callback`，并把对应粒子/初始化/边界 callback 合同回填到 `particles/09`、`diagnostics/09`、`initialization/14` 与第 3A / 第 4 章。
- [x] 继续沿参数系统主线收尾：已把 `test_1d_fel`、`test_2d_bilinear_filter`、`test_2d/rcylinder/rz_curl_curl_petsc_pc` 这组剩余粗分类条目压实为 boosted-frame FEL diagnostics、single-particle current filtering 与 PETSc curl-curl preconditioner 结构断言，并把对应 FEL / PETSc 判据回填到 `laser/06` 与 `fieldsolver/13`。
- [x] 继续沿参数系统主线收尾：已把 `test_2d_energy_conserving_thermal_plasma`、`test_2d_id_cpu_read_picmi`、`test_2d_runtime_components_picmi` 这组剩余粗分类条目压实为 energy-conserving gather、`idcpu` Python 读取合同与 runtime-components/checkpoint scaffold，并把对应 Python-interface / restart 结论回填到 `particles/28` 与 `diagnostics/04`。
- [x] 继续沿参数系统主线收尾：已把 `test_3d_acceleration`、`test_3d_beamsize_effect`、`test_3d_eb_picmi` 这组剩余粗分类条目压实为 acceleration restart baseline、virtual-photon beam-size effect 与 EB PICMI checkpoint scaffold，并把对应 restart/QED 边界回填到 `diagnostics/04`、`particles/17` 与第 8 章。
- [x] 继续沿参数系统主线收尾：已把顶层 `Examples/analysis_default_regression.py`、`test_3d_hard_edged_quadrupoles*` 与 `test_3d_pmc_field` 这组剩余粗分类条目压实为通用 checksum helper、accelerator-lattice hard-edged quadrupole 解析轨道对照，以及 PMC standing-wave 边界基准；并新增 `accelerator-lattice/03-validation-map.md`，把对应验证边界回填到第 4/7 章。
- [ ] 继续沿参数系统主线收尾：优先清理 `docs/example-regression-map.md` 中剩余“checksum 基线；需反查对应 inputs 和分析脚本”的家族条目，并对整张 `parameter-map` 的“初步源码命中”做更严格的二次人工复核。
- [x] 继续清理 `docs/example-regression-map.md` 的 Langmuir 家族：已把 `langmuir` / `langmuir_fluids` 的 1D/2D/3D/RZ、MR、PSATD、JRhom、current-correction、Vay、PICMI 与 cold-fluid 变体统一接回 `analysis_1d/2d/3d/rz/r1d.py` 和 `analysis_utils.py` 的共享合同，并把主结论回填到 `initialization/14`、`particles/30` 与第 8 章。
- [x] 继续清理 `docs/example-regression-map.md` 的 `uniform_plasma` 家族：已把 `Examples/Physics_applications/uniform_plasma/` 的 2D/3D checksum 基线、3D restart 强对照，以及 `nci_psatd_stability` 里名字带 `uniform_plasma` 的 `JRhom_CC1` PSATD/NCI 稳定性回归明确拆开，并把 writer/checkpoint/PSATD 的真实边界回填到 `diagnostics/06`、`fieldsolver/13` 与第 8 章。
- [x] 继续清理 `docs/example-regression-map.md` 的 `implicit` 家族：已把 `Examples/Tests/implicit/` 从笼统 “implicit solver” 桶拆成 1D Picard、exactly energy-conserving symmetry、Strang implicit spectral EM、planar pinch，以及 JFNK + Villasenor / PEC cropping 五条验证线，并把对应结论回填到 `nonlinear-solvers/07` 与第 6 章。
- [x] 继续清理 `docs/example-regression-map.md` 的 `silver_mueller` 家族：已把 `Examples/Tests/silver_mueller/` 压实为“残余反射幅值必须远小于入射激光峰值”的开放边界强回归，并区分 1D 轴向、2D `x` 向、2D `z` 向与 RZ `z` 向四条最小基准；同时把这一层回填到 `boundary/02` 与第 7 章。
- [x] 继续清理 `docs/example-regression-map.md` 的 `pec` 家族：已把 `Examples/Tests/pec/` 压实为 PEC standing-wave、PEC standing-wave / MR、PECInsulator implicit energy accounting、PECInsulator implicit restart continuation，以及粒子侧 PEC checksum baseline 五条边界；并把对应结论回填到 `boundary/02` 与第 7 章。
- [x] 继续清理 `docs/example-regression-map.md` 的 `pml` 家族：已把 `Examples/Tests/pml/` 压实为 Yee/CKC 理论反射率、PSATD/Galilean 低反射率、RZ residual-field decay，以及 Yee/PSATD restart reproducibility 四层合同；并把对应结论回填到 `boundary/01` 与第 7 章。
- [x] 继续清理 `docs/example-regression-map.md` 的 `reduced_diags` 家族：已把 `Examples/Tests/reduced_diags/` 压实为 compact-observable cross-check 与 `LoadBalanceCosts` efficiency 两棵验证树，并把 `timers_psatd` / `single_precision` 的当前源码树边界回填到 `diagnostics/05` 与第 8 章。
- [x] 继续清理 `docs/example-regression-map.md` 的 `vay_deposition` 家族：已把 `Examples/Tests/vay_deposition/` 压实为 2D/3D `vay + psatd + collocated` 下的离散 Gauss-law 强断言，并把对应结论回填到 `particles/07` 与第 5 章。
- [x] 继续清理 `docs/example-regression-map.md` 的 `nci_fdtd_stability` 家族：已把 `Examples/Tests/nci_fdtd_stability/` 压实为 2D drifting-plasma + `use_fdtd_nci_corr=1` 的 FDTD NCI 抑制基准，明确 non-MR 的 `1e24` 场能代理阈值、MR 变体的 full-domain fine-tag 目标，以及 `analysis_ncicorr.py` 当前 MR 路径区分仅在脚本层预留、未从活跃 `CMakeLists.txt` 参数层显式选通的源码树边界；并把对应结论回填到 `fieldsolver/13` 与第 6 章。
- [x] 继续清理 `docs/example-regression-map.md` 的 `maxwell_hybrid_qed` 家族：已把 `Examples/Tests/maxwell_hybrid_qed/` 压实为 2D collocated + PSATD + `use_hybrid_QED=1` 的真空色散基准，明确 `analysis.py` 实际检查的是脉冲相速度与 hybrid-QED 理论值的 `1.25%` 误差，而不是粒子 QED 事件；并把对应结论回填到 `fieldsolver/13` 与第 6 章。
- [x] 继续清理 `docs/example-regression-map.md` 的 `python_wrappers` 家族：已把 `Examples/Tests/python_wrappers/` 压实为 2D PICMI + PSATD + PML + div-cleaning 下的 Python field-wrapper 强接口自检，明确 `sim.fields.get(...)` 对 `E/B/F/G` 与 `pml_E/B/F/G` 的逐分量 benchmark 断言；并新增 `python/03-field-wrapper-validation-map.md`，把这条 validation 接回 `pywarpx/fields.py`、`MultiFabRegister.py`、`Source/Python/MultiFabRegister.cpp` 与第 8 章。
- [x] 继续清理 `docs/example-regression-map.md` 的 `plasma_acceleration` 家族：已把 `Examples/Physics_applications/plasma_acceleration/` 压实为 PWFA application workflow matrix，明确 active tests 全部 `analysis=OFF`、目录内 helper 只提供 checksum、真正覆盖的是 moving window、boosted frame、rigid bunch、NCI correction、mesh refinement、hybrid grid 与 PICMI front-end；并把“3D PICMI 版当前仍不是 boosted-frame 等价前端”的 README 边界回填到 `laser/05` 与第 8 章。
- [x] 继续清理 `docs/example-regression-map.md` 的 `beam_beam_collision` 家族：已把 `Examples/Physics_applications/beam_beam_collision/` 压实为 collider-QED application baseline，明确 active regression 只有 checksum helper、输入真正覆盖的是 relativistic electrostatic self-field、Quantum Synchrotron、Breit-Wheeler 与 `ColliderRelevant/ParticleNumber` reduced diagnostics 的联合路径，而 `plot_fields.py` / `plot_reduced.py` 只是可视化 helper；并把对应边界回填到 `diagnostics/05` 与第 8 章。
- [x] 继续清理 `docs/example-regression-map.md` 的 `plasma_mirror` 家族：已把 `Examples/Physics_applications/plasma_mirror/` 压实为 2D laser-solid surface-plasma checksum baseline，明确 active regression 只有 checksum helper、输入真正覆盖的是 Gaussian laser、前后指数梯度 + 过密 plateau 固体靶、PML、field filter 与 full diagnostics 的联合骨架，当前没有独立 analysis 也没有 PICMI；并把对应边界回填到 `laser/05` 与第 3A 章。
- [x] 继续清理 `docs/example-regression-map.md` 的 `thomson_parabola_spectrometer` 家族：已把 `Examples/Physics_applications/thomson_parabola_spectrometer/` 压实为 `BoundaryScraping/openPMD + prescribed-field test-particle optics` 强基准，明确 active `analysis.py` 会从 `particles_at_zhi` 和 `diag0` 按 `id` 回连出 detector screen 上的 species/energy 分离图，而不是普通 `PEC / conducting boundary` test；并把对应边界回填到 `diagnostics/08` 与第 8 章。
- [x] 继续清理 `docs/example-regression-map.md` 的 `capacitive_discharge` 家族：已把 `Examples/Physics_applications/capacitive_discharge/` 压实为两层结构，明确 1D PICMI `background_mcc` / `dsmc` 入口通过 `analysis_1d.py` / `analysis_dsmc.py` 对 Turner case-1 离子密度 profile 做强对照，而 2D native / PICMI 入口仍主要是 workflow checksum baseline；同时把 `test_2d_background_mcc_dp_psp` 明确标成当前 `CMakeLists.txt` 中被注释掉的遗留 benchmark 名，并把对应边界回填到 `particles/22` 与第 4 章。
- [x] 继续清理 `docs/example-regression-map.md` 的 `laser_acceleration` 家族：已把 `Examples/Physics_applications/laser_acceleration/` 压实为 LWFA runtime matrix，明确 `README.rst` 的 `Analyze` 仍是 `TODO`、大多数 active tests 都是 `analysis=OFF`，而现有强断言只局限于 1D boosted fluid ODE 对照、`refine_plasma=1` 连续注入一致性，以及 RZ openPMD diagnostics 合同；同时把 `inputs_base_1d/2d/3d/rz` 的 moving-window / continuous-injection / diagnostics 骨架语义回填到 `laser/05` 与第 3A 章。
- [x] 继续清理 `docs/example-regression-map.md` 的 `embedded_circle` 条目：已把 `Examples/Tests/embedded_circle/` 压实为 2D circular embedded-boundary electrostatic + PIC-MCC + BoundaryScraping workflow baseline，明确它通过 `eb_implicit_function`、`eb_potential`、`initialize_self_fields`、双物种 `background_mcc`、`save_particles_at_eb` 与 timer-based load balance 把 EB 多物理工作流接在一起，但当前 `analysis=OFF`、只有 checksum helper；并把对应边界回填到 `embedded-boundary/02` 与第 7 章。
- [x] 继续清理 `docs/example-regression-map.md` 的 `load_external_field` restart 尾项：已把 `analysis_default_restart.py` 与 `test_3d_load_external_field_particle_time_restart`、`test_rz_load_external_field_grid_restart`、`test_rz_load_external_field_particles_restart` 压实为 external-field state reproducibility，明确它们不是新 physics benchmark，而是用逐字段 restart 对照验证 `read_from_file` / dependency parser 构造出的 grid external field 与 particle external field 状态在恢复后不漂移；并把对应边界回填到 `initialization/15`、`diagnostics/04` 与第 3A 章。
- [x] 继续清理 `docs/example-regression-map.md` 的 `restart` 尾项：已把 `analysis_default_restart.py`、`inputs_base_3d` 与 `test_3d_acceleration_psatd*` 这一串压实为 field-level restart reproducibility 与 PSATD/time-averaged acceleration restart reproducibility，明确它们不是新的谱色散 benchmark，而是在 3D boosted acceleration workflow 上验证 `psatd`、Galilean 和 `psatd.do_time_averaging=1` 这些 solver path 的 checkpoint/restart 不漂移；并把对应边界回填到 `diagnostics/04` 与第 8 章。
- [x] 继续清理 `docs/example-regression-map.md` 的 `restart_eb` 尾项：已把目录内 `analysis_default_regression.py` / `analysis_default_restart.py` 与 `inputs_test_3d_eb_picmi.py` 一起压实为 EB + PICMI + checkpoint scaffold，明确 active test 仍只有 checksum baseline，而逐字段 restart 对照仍停留在 `CMakeLists.txt` 里被注释掉的 `test_3d_eb_picmi_restart`；并把这层“helper 已在、注册未开”的边界回填到 `diagnostics/04` 与第 8 章。
- [x] 继续清理 `docs/example-regression-map.md` 的 `laser_injection` / `laser_injection_from_file` helper 尾项：已把两个目录的 `analysis_default_regression.py` 压实为 checksum helper，并把 `laser_injection_from_file` 里 1D/2D/3D/RZ/binary 的 `*_prepare.py` 全部改写成外部 laser 文件生成阶段，明确它们在 `CMakeLists.txt` 中都是 `analysis=OFF`、`checksum=OFF` 的 dependency，整体构成 `prepare -> inject -> analysis` 三段回归链；并把这层边界回填到 `laser/03` 与第 3A 章。
- [x] 继续清理 `docs/example-regression-map.md` 的 helper 尾项：已把 `Examples/Tests/subcycling/analysis_default_regression.py` 与 `Examples/Tests/pec/analysis_default_regression.py` 压实为目录内 checksum helper，明确它们分别服务于 `subcycling_mr` 的 AMR + subcycling 组合稳定性基线，以及 PEC family 的 standing-wave / PECInsulator / 粒子侧输出基线，而不替代现有强 analysis；并把对应边界回填到 `particles/30` 与 `boundary/02`。
- [x] 切回 `docs/parameter-map.md` 做第二轮人工复核，先修正 `particle_thermalizer.species` 与 `particle_thermalizer.theta` 的误命中源码入口：两者真实都由 `Source/Particles/ParticleThermalizer/ParticleThermalizer.cpp` 解析，且 `theta` 在运行时进入 `sqrt(theta)` 热速度重采样，而不是 diagnostics/flush 路径。
- [x] 继续做 `docs/parameter-map.md` 的第二轮人工复核，再修正两条运行控制参数的“消费点误命中”：`warpx.numprocs` 的真实读取链是 `WarpX.cpp -> WarpXAMReXInit.cpp -> WarpXInitData.cpp`，`warpx.dt_update_interval` 的真实读取链是 `WarpX.cpp -> WarpXComputeDt.cpp -> WarpXEvolve.cpp`，不应把 `FullDiagnostics.cpp` 记成主解析入口。
- [x] 继续做 `docs/parameter-map.md` 的第二轮人工复核，再修正 `max_step` / `stop_time` / `geometry.dims` / `reduced_diags.intervals` 这批易误命中条目：前两者真实都在 `WarpX::ReadParameters()` 的无前缀 `ParmParse` 中读取，`geometry.dims` 的主入口是 `WarpXInit.cpp` 的编译维度一致性检查，而 `reduced_diags.intervals` 只应归到 `ReducedDiags.cpp`，不应把 `FullDiagnostics` / `BoundaryScrapingDiagnostics` 的独立 `intervals` 参数混进来。
- [x] 继续做 `docs/parameter-map.md` 的第二轮人工复核，再修正 `authors` / `amr.max_level` / `amr.restart` / `warpx.verbose`：其中 `authors`、`amr.restart`、`warpx.verbose` 已回到 `WarpX.cpp` 主解析入口和真实消费链，`amr.max_level` 则明确记录为 `AMReX/AmrCore-owned input`，WarpX 侧只保留本地消费者，不再伪造统一解析入口。
- [x] 继续做 `docs/parameter-map.md` 的第二轮人工复核，再修正 `warpx.used_inputs_file` / `warpx.boost_direction` / `warpx.do_electrostatic` / `amr.n_cell`：分别回到 `WriteUsedInputsFile()` 的 `queryAdd + write_used_inputs_file` 链、`ReadBoostedFrameParameters()` 的真正读取入口、`WarpX.cpp` 的 electrostatic enum 解析，以及 `WarpXAMReXInit.cpp` 对 `amr.n_cell` 的启动期预解析与 AMReX-owned 边界。
- [x] 继续做 `docs/parameter-map.md` 的第二轮人工复核，再修正 `warpx.gamma_boost` / `warpx.n_rz_azimuthal_modes` / `geometry.prob_lo/hi` / `warpx.poisson_solver`：分别压实为 `ReadBoostedFrameParameters()` 的 boosted-frame 主入口、`WarpX.cpp` 中 RZ 方位模数的真实解析位置、`WarpXAMReXInit.cpp` 启动期预解析加 `WarpXUtil.cpp` boost 改写的域边界链路，以及 `WarpX.cpp` 主解析加 `PoissonBoundaryHandler.cpp` 分派消费的真实边界。
- [x] 继续做 `docs/parameter-map.md` 的第二轮人工复核，再修正 `warpx.zmax_plasma_to_compute_max_step` / `warpx.compute_max_step_from_btd` / `warpx.do_moving_window` / `warpx.moving_window_*` / `warpx.fine_tag_lo/hi`：分别压实为 boosted wakefield 自动 `max_step` 计算链、BTD 驱动的运行上界自动补足链、`WarpXInit.cpp` 中 moving-window 参数的统一读取入口，以及静态 refined patch bbox 与 boosted-frame 坐标改写的两段链路。
- [x] 继续做 `docs/parameter-map.md` 的第二轮人工复核，再修正 `boundary.field_lo/hi` / `boundary.particle_lo/hi` / `warpx.ref_patch_function(x,y,z)`：分别压实为 `parse_field_boundaries()` 加 `geometry.is_periodic` 反推与 PML/solver 约束、`parse_particle_boundaries()` 中 periodic 继承与一致性检查，以及静态 refined patch parser 入口与 `fine_tag_lo/hi` 覆盖关系。
- [x] 精读 `Laser/`：已用 `notes/code-reading/laser/00-07` 覆盖 `Source/Laser/LaserProfiles.H`、三类 `LaserProfilesImpl/*`、`Particles/LaserParticleContainer.*`，并把验证层、moving-window / external-field 耦合和应用层分叉一并回填到第 3A 章、回归索引与参数索引。
- [x] 精读 `ExternalField.*`、`WarpXMovingWindow.cpp`：这条主线已在 `initialization/01`、`laser/04`、`evolve/05` 与 `initialization/13/15/16` 中成文，当前再保留为未完成项会与现有工作树证据冲突。
- [x] 验证：`laser injection`。`laser/03-laser-validation-map.md` 已把 `laser_injection`、implicit laser injection、`laser_injection_from_file` 的强 analysis、checksum helper 和 `prepare -> inject -> analysis` 链条压实，第 3A 章也已回填这些边界。
- [x] 验证：`load density`。`initialization/16-initialization-validation-map-density-magnetostatic-nodal.md` 已把 `read_density_from_path`、openPMD density mesh prepare 阶段、moving-window 连续注入和 `rho` 重建断言压实，第 3A 章已同步回填。
- [x] 验证：`initial distribution / gaussian_beam`。`initialization/06-gaussian-beam-openpmd-injection.md`、`initialization/14-initialization-validation-map.md` 与第 3A 章已经把 `focusing_gaussian_beam`、`rotated_gaussian_beam`、Gaussian-beam photon/PICMI 变体的几何、旋转和束斑统计断言压实。
- [x] 验证：`initial distribution / external_file / PICMI openPMD variant`。`test_3d_focusing_gaussian_beam_from_openpmd_picmi` 明确复用 `analysis_focusing_beam.py`，当前足以支撑 PICMI 版 openPMD 粒子注入的束斑统计合同已经闭环。
- [x] 验证：`initial distribution / external_file / native openPMD workflow baseline`。当前本地 checkout 里 `test_3d_focusing_gaussian_beam_from_openpmd` 的 `prepare.py -> external_file inputs -> checksum` 链已闭环，足以证明 native openPMD 粒子注入路径与历史输出基线处于 active coverage。
- [x] 继续清理 `docs/example-regression-map.md` 的 `gaussian_beam` native openPMD variant：已把这条 native `external_file` 版从笼统“脚本缺口”压实为更精确的 `CMake analysis target` 反向边界。
  - 已补清更硬的运行态结论：当前 active coverage 是 `prepare -> external_file inputs -> analysis_default_regression.py checksum`，因此 openPMD 生成、导入和 workflow baseline 仍然存在。
  - 已补清更细的未闭环位置：真正悬空的是 `gaussian_beam/CMakeLists.txt` 仍指向本地不存在的 `analysis.py`，而 PICMI 版才明确复用 `analysis_focusing_beam.py` 做强束斑统计断言。
- [x] 继续清理 `docs/example-regression-map.md` 的 `embedded_boundary_removal_depth` legacy benchmarks：已把这 2D/3D/RZ 三组名字从“只看到 benchmark JSON、像是缺目录”压实为更准确的 benchmark-only 残留边界。
  - 已补清更硬的运行态结论：它们当前只存在于 `Regression/Checksum/benchmarks_json`，并没有对应 `Examples/Tests` 目录或 `add_warpx_test(...)` 注册。
  - 已补清更细的交叉映射：同维度 active 路径已经由 `embedded_boundary_em_particle_absorption_sh_factor_*` 家族承接，并明确绑定 `analysis.py + checksum`，所以这组 `removal_depth` 不应再被当成缺失中的独立 active regression。
- [x] 继续清理 `docs/example-regression-map.md` 的 `capacitive_discharge` 遗留 `dp_psp` benchmark 名：已把 `test_2d_background_mcc_dp_psp` 从“注释掉的测试名”压实为更精确的注释块残留边界。
  - 已补清更硬的运行态结论：`capacitive_discharge/CMakeLists.txt` 里这条 `add_warpx_test(...)` 是整段被注释掉的，未进入活跃注册表。
  - 已补清更细的源码树证据：本地目录里连 `inputs_test_2d_background_mcc_dp_psp` 都不存在，因此它当前只活在 `benchmarks_json` 与 CMake 注释块里，不是“脚本还在、只是暂时没跑”的 dormant variant。
- [x] 继续清理 `docs/example-regression-map.md` 的 `test_3d_pml_psatd_dive_divb_cleaning`：已把这条 3D PSATD/PML/div-cleaning baseline 从笼统 `analysis=OFF` 压实为更精确的 writer-side 边界。
  - 已补清更硬的运行态结论：当前 active test 虽然同时打开 `do_dive_cleaning`、`do_divb_cleaning`、`do_pml_dive_cleaning`、`do_pml_divb_cleaning`，但 `diag1.fields_to_plot` 只写 `Bx By Bz Ex Ey Ez rho`。
  - 已补清更细的覆盖范围：因此这条 regression 现在验证的是启用四个 cleaning 开关后的最终场输出 checksum，而不是脚本级的 divergence-cleaning 强断言；目录内现有 `analysis_pml_psatd*.py` 也不消费这条 3D 三束激光工作流。
- [ ] 验证：`initial distribution / external_file / native openPMD strong analysis`。`gaussian_beam/CMakeLists.txt` 仍指向名义上的 `analysis.py`，但当前 checkout 里该脚本缺失，因此这条 native variant 还不能宣称已具备与 PICMI 版同等级的束斑统计物理断言。
- [x] 验证：`moving-window / boosted examples`。`evolve/05-moving-window.md`、`laser/04-moving-window-external-field-coupling.md`、`laser/03-laser-validation-map.md` 与第 3A 章已经把窗口推进、boosted-frame、continuous injection、BTD 和相关 examples 的验证边界压实。

### 多物理扩展

- [x] 继续精读 `Particles/Collision/`：`ElasticCollisionPerez`、Bremsstrahlung photon momentum 初始化尾部、fusion product momentum initializer，以及 remaining `collision/*` analysis/checksum 粗分类条目。
- [x] 继续精读 `Particles/Collision/`：`UpdateMomentumPerezElastic.H`、`BremsstrahlungEvent(...)` 的截面/能谱采样、`SingleNuclearFusionEvent.H` 的概率裁剪与 multiplier 缩放，以及剩余 `collision/*` 2D/3D/isotropization/RZ 条目。
- [x] 继续精读 `Particles/` 性能与数值后处理层：`Resampling/`、`ParticleThermalizer/`、`Sorting/`，并继续清理 `capacitive_discharge/background_mcc` 与剩余 `collision/*` checksum 粗分类条目。
- [x] 精读 `Particles/ElementaryProcess/Ionization.*`：已把当前工作树里的 ADK 主链、内建电离能表、`ionization_initial_level` 初始化传播、`ionizationLevel -> w q_e * level` 的沉积计价，以及“当前无独立 OTB 路径”这一源码边界回填到 `particles/12` 与第 4 章。
- [x] 精读 QED internals、quantum synchrotron、Breit-Wheeler、Schwinger process：已用 `particles/14-17` 打通 runtime attributes / product-species / `InitQED()` 入口、QED kernels 与 wrapper/table 生命周期、`QedChiFunctions` 与 virtual photons / `linear_breit_wheeler` 的分叉，并在第 4 章明确区分了 Quantum Synchrotron、强场 Breit-Wheeler 和 Schwinger 三条事件链；当前再保留为未完成项会与现有工作树证据冲突。
- [x] 精读 `Fluids/`：已用 `fluids/00-fluid-container-map.md`、`01-muscl-hancock-update.md`、`02-fluid-pic-coupling.md` 打通 `fluids.species_names -> MultiFluidContainer -> WarpXFluidContainer` 对象图、nodal `N/NU` 状态、MUSCL-Hancock + Rusanov + positivity limiter 更新，以及 fluid species 如何 gather `Efield_aux/Bfield_aux`、复用 Higuera-Cary source-step、把 `rho/J` 沉积回普通场寄存器并与 `HybridPICModel` 电子闭合区分开来。
- [x] 精读 `AcceleratorLattice/`：已用 `accelerator-lattice/00-lattice-data-model.md`、`01-lattice-elements.md`、`02-element-finder-device-path.md`、`03-validation-map.md` 打通递归 `lattice.elements/line/reverse` 输入树、`z_location -> zs/ze` 几何账本、`drift/quad/plasmalens` 的 hard-edged 元件语义、`hard_edged_fraction()` residence correction、per-tile `LatticeElementFinder` lookup table，以及 boosted-frame 下 lab-frame 取场再反变换回粒子推进的运行链。
- [x] 验证：collision、ionization_dsmc、field_ionization、qed、linear_breit_wheeler、linear_compton、ohm_solver、accelerator_lattice。当前工作树里，`particles/12-19,21-23` 已分别把 `field_ionization`、QED、`linear_breit_wheeler` / `linear_compton`、`BackgroundMCC` / `PulsedDecay` / DSMC 与 `collision/*` 的 analysis-vs-checksum 边界压实，`accelerator-lattice/03-validation-map.md` 已把 hard-edged quadrupole 的 lab/boosted/moving-window 强 regression 压实，而 `fieldsolver/13-14` 已把 `ohm_solver_*` 明确分成有显式 assert 的 RZ EM modes / ion-beam-instability 与主要依赖谱图或 checksum 的 Cartesian EM modes / Landau damping / reconnection / cylinder-compression；继续保留整条为未完成会与当前 worktree 证据冲突。

### 诊断、Python、工具和构建

- [x] 精读 `Diagnostics/`：已用 `diagnostics/00-boundary-scraping-diagnostics-python.md`、`01-diagnostics-dispatch.md`、`02-field-and-particle-functors.md`、`03-reduced-diagnostics.md`、`04-io-formats-and-restart.md`、`05-reduced-diagnostic-case-studies.md`、`06-writer-comparison-and-minimal-cases.md`、`07-output-layouts-and-reading-tools.md`、`08-template-cases-and-boundaryscraping-example.md`、`09-python-boundary-buffer-callback-case.md` 打通 full diagnostics、reduced diagnostics、field/particle I/O、openPMD、BTD、restart、BoundaryScraping 与 Python buffer 消费链。
- [x] 精读 `Python/`：已用 `python/00-python-module-init.md`、`01-callbacks.md`、`02-field-particle-access.md`、`03-field-wrapper-validation-map.md` 打通维度专用 pybind module、`_libwarpx.py` 的 geometry-aware lazy load、Python callback 聚合桥、`multifab_register` / `multi_particle_container` / `particle_boundary_buffer` 三条访问面，以及 PICMI `sim.fields` / `sim.particles` / `Simulation.step()` 到 C++ runtime 的真实映射。
- [x] 精读 `Tools/Parser`、`Tools/PostProcessing`、`Tools/Algorithms`、`Tools/QedTablesUtils`：已用 `tools/00-parser-postprocessing-algorithms-boundary.md` 和 `01-qed-tables-utils.md` 把 top-level `Tools/*` 的真实边界压实为轻量 parser helper、reader/log-side post-processing、推导/估计 notebook/script，以及 `qed_table_generator` / `qed_table_reader` 这两个离线 QED lookup-table 工具；其中 `psatd.ipynb` 与常用 reader-side 脚本已分别接回 `fieldsolver/11` 与 `diagnostics/07` 的现有主线。
- [x] 精读 CMake/GNUmake 构建系统、维度变体、HPC machine scripts：已用 `build/00-cmake-superbuild-and-module-aggregation.md`、`01-gnu-make-and-dimension-variants.md`、`02-hpc-machine-profiles.md` 压实顶层 `CMakeLists.txt` 的 option/variant 矩阵、依赖 superbuild、`lib_${SD}` / `pyWarpX_${SD}` 聚合链，`Source/Make.WarpX` 的 legacy feature 宏与 `DIM/USE_RZ/USERSuffix` 维度编码，以及 `Tools/machines/*` 的 `warpx.profile -> install_dependencies.sh -> submit template` machine-specialized 构建/部署层。
- [x] 验证：reduced_diags、restart、particle_data_python、python_wrappers、openPMD examples。`reduced_diags` 已在 `diagnostics/05` 压成 compact-observable 与 `LoadBalanceCosts` 两棵验证树，`restart` 已在 `diagnostics/04` 和 `example-regression-map` 压成 field-level reproducibility / scaffold 边界，`particle_data_python` 已在 `particles/28` 压成 Python runtime-attribute / 手动沉积合同，`python_wrappers` 已在 `python/03` 压成 `sim.fields.get(...)` 的强接口自检，而 openPMD examples 的 writer/layout/reader-side 边界已由 `diagnostics/07-09` 与相关章节模板固定下来。

### 应用案例综合章

- [x] Langmuir wave：从解析色散关系到源码路径。已新增 `notes/code-reading/applications/00-langmuir-wave.md`，把 `Examples/Tests/langmuir/*` 与 `langmuir_fluids/*` 从冷等离子体解析振荡、输入骨架、源码调用链、analysis/checksum/PICMI 分层一路收束成应用级主线，并同步扩展第 8 章与 `source-map`。
- [x] Uniform plasma：噪声、能量、性能和诊断。已新增 `notes/code-reading/applications/01-uniform-plasma.md`，把 `Examples/Physics_applications/uniform_plasma/*` 从均匀热等离子体背景、噪声/性能/workflow 基线，到 full diagnostics / checkpoint / restart 强对照整理成应用级主线，并把“能量强断言主要来自相邻 `energy_conserving_thermal_plasma`、PSATD/JRhom 强稳定性断言主要来自 `nci_psatd_stability`”这层边界同步写回第 8 章与 `source-map`。
- [x] LWFA/PWFA：laser、plasma、moving window、boosted frame、diagnostics。已新增 `notes/code-reading/applications/02-lwfa-pwfa.md`，把 `Examples/Physics_applications/laser_acceleration/*` 与 `plasma_acceleration/*` 从 `laser/05`、第 8 章和现有 regression 索引重新收束成 wakefield acceleration 应用主线，并明确保留当前 worktree 的真实边界：`laser_acceleration` 是 `LWFA runtime matrix`、只有少量局部强 analysis；`plasma_acceleration` 是 `PWFA workflow matrix`、active tree 目前仍是 checksum-only，且 3D PICMI 版本还没有做到 native boosted 等价覆盖。
- [x] Laser ion / plasma mirror / RPA/TNSA：边界、靶、强场、多物理。已新增 `notes/code-reading/applications/03-laser-targets-rpa-tnsa.md`，把 `laser_ion` 收束成当前最强的 laser-target application entry、把 `plasma_mirror` 收束成 laser-solid surface-plasma workflow baseline，并明确保留当前 worktree 的真实边界：`RPA/TNSA` 目前只在 `laser_ion` 文献语境和 glossary 里作为机制标签出现，当前没有独立 `rpa_*` / `tnsa_*` 本地 application tree。
- [x] Capacitive discharge：PIC-MCC 低温等离子体。已新增 `notes/code-reading/applications/04-capacitive-discharge.md`，把 `Examples/Physics_applications/capacitive_discharge/*` 收束成一条 PIC-MCC 低温等离子体应用主线，并明确保留当前 worktree 的真实边界：1D PICMI `background_mcc` / `dsmc` 入口通过 `analysis_1d.py` / `analysis_dsmc.py` 对 Turner case-1 离子密度 profile 做强对照，Python callback Poisson solver 是这条应用树的重要工程边界，而 2D native / PICMI 入口当前仍主要是 workflow checksum baseline，`dp_psp` 仍是被注释掉的遗留分支。
- [x] Magnetic reconnection：hybrid model 和 fluid/PIC 耦合。已新增 `notes/code-reading/applications/05-magnetic-reconnection.md`，把 `Examples/Tests/ohm_solver_magnetic_reconnection/*` 收束成一条 hybrid-PIC space-plasma 应用主线，并明确保留当前 worktree 的真实边界：它依赖的是 `HybridPICModel` 的 electron-fluid Ohm closure，不是 `Fluids/` 的 cold-fluid runtime layer；当前 active coverage 是 `analysis.py` 的重联率提取/可视化加 `analysis_default_regression.py` 的 checksum 分层，而不是带显式容差 `assert` 的强 benchmark。
- [x] Beam-beam / luminosity / FEL / ion extraction：束流和加速器模块。已新增 `notes/code-reading/applications/06-beam-collider-fel-extraction.md`，把 `diff_lumi_diag`、`beam_beam_collision`、`free_electron_laser`、`ion_beam_extraction` 与 `accelerator_lattice` 收束成一条束流与加速器应用主线，并明确保留当前 worktree 的真实分层：`DifferentialLuminosity` 是 reduced-diagnostic 强谱基准，`beam_beam_collision` 只是 collider-QED 应用骨架，`free_electron_laser` 是 boosted rigid-beam + undulator + BTD 的强 benchmark，`ion_beam_extraction` 是 EB electrostatic extraction 的强应用入口，而 `accelerator_lattice` 则提供 beamline optics 的强回归层。

## 文献处理任务

- [x] 用 MinerU 处理 `references/02_books_lecture_notes/` 下两份开源讲义，并为每份资料建立论文专属目录、Markdown、`images/`、中文讲解笔记骨架与 `reading-log.md`。当前已完成：
  - `no-year_PICSimulationNotesYoujunHu2019_Particle_In_Cell_PIC_simulation`
  - `no-year_ComputationalMethodsPlasmaPhysicsNotes_Computational_Methods_in_Plasma_Physics_lecture_notes`
- [x] 核对 `Birdsall-Langdon / Hockney-Eastwood / Dawson` 在当前工作树中的真实可用状态，并把“book-level missing”与“article-level not yet materialized”边界写回文献索引。当前结论：
  - `Birdsall-Langdon`：当前已发现本机现成 PDF，并已 materialize 到 `references/02_books_lecture_notes/1985_BirdsallLangdon_Plasma_physics_via_computer_simulation/`。
  - `Hockney-Eastwood`：已有 BibTeX，无本地合法 PDF。
  - `Dawson`：`Tajimaprl79` 与 `DawsonRMP83` 当前已基于本机现成 PDF 完成 materialize；`TajimaDawson1982` 仍只有 BibTeX，未发现本地 PDF。
- [x] 用 MinerU 处理 `Birdsall 1985`、`Tajima 1979`、`Dawson 1983` 本机现成 PDF，并建立论文专属目录、Markdown、`images/`、中文讲解笔记与 `reading-log.md`。其中 `Birdsall 1985` 已按 `scripts/split_pdf_pypdf.py` 拆成三段后完成转换。
- [x] 追加扫描本机 `Zoteropaper`、`llm-for-zotero-mineru` 与更宽的 `Documents/`，确认剩余核心缺口是否已有现成资产。当前结论：
  - `Hockney-Eastwood`：当前本机仍无现成 PDF。
  - `TajimaDawson1982`：当前本机仍无现成 PDF 或 MinerU 产物。
- [x] 启动 `Birdsall 1985` 第一分卷的正式精读，并按 `research-paper-explainer` 顺序化写入中文讲解笔记。当前已覆盖：
  - `Foreword`
  - `Preface`
  - Part One 入口
  - Chapter 1
  - Chapter 2 的 `2-1` 到 `2-4`
- [x] 继续推进 `Birdsall 1985` 第一分卷精读，补入 Chapter 2 的 `2-5`、`2-6` 与 Chapter 3A 的 `3-1` 到 `3-6`。当前已明确写清：
  - 静电 `FFT` 场求解与离散算子 `kappa/K^2`
  - NGP / CIC weighting 与等效粒子形状
  - `ES1` 的最小程序骨架 `INIT -> SETRHO -> FIELDS -> SETV -> ACCEL -> MOVE -> HISTRY`
  - `3-3` 到 `3-6` 的输入归一化与初始化链
- [x] 继续推进 `Birdsall 1985` 第一分卷精读，补入 `3-7` 到 `3-12` 与 `4-6` 到 `4-10`，并做最小正文回填。当前已明确写清：
  - `SETRHO` 是 `t=0` 的第一次真实 charge deposition
  - `FIELDS` 是 `rho -> FFT -> phi -> E -> field energy` 的完整离散合同
  - `SETV/ACCEL/MOVE` 是最小 leapfrog runtime contract
  - `S(x)/S(k)`、finite-size particles、grid force、aliasing 的理论边界
  - Poisson 系统误差与 `rho_k phi_k^*` 场能量账本
  - 第 5 / 6 章已做最小文献回填
- [x] 继续推进 `Birdsall 1985` 第一分卷精读，补入 Chapter 4 的 `4-3` 到 `4-5`，并做最小正文回填。当前已明确写清：
  - electric impulse 与 magnetic rotation 的几何分裂
  - `tan(theta/2)` 与 `t/s/c` 半角变量的实现意义
  - 向量 Boris 形式作为现代 Boris kernel 的直接祖先
  - `1d2v/1d3v` 的建模边界与 guiding-center 结构量
  - 第 4 章已做最小文献回填
- [x] 继续精读 `Birdsall 1985` 第一分卷 Chapter 8 的 `8-1` 到 `8-7` 与 `8-10` 到 `8-13`，并做最小正文回填。当前已明确写清：
  - spatial-grid theory 与 coherent grid-plasma interaction 的问题设置
  - sampled density 中 aliasing 的精确来源 `rho(k)=q sum_p S(k_p)n(k_p)`
  - 共用同一 `S` 时的 momentum conservation 条件
  - `K(k)`、`kappa(k)`、`S(k)` 与 alias sum 如何进入 dielectric function / dispersion relation
  - cold beam / warm plasma 的 nonphysical instability 与 `lambda_D / Delta x` 数值边界
  - 第 5 / 6 章已做最小文献回填
- [ ] 用 MinerU 处理 Hockney-Eastwood 可合法获取资料或已有 PDF。
- [ ] 若 `Hockney-Eastwood` 原书仍不可得，则按 article-level fallback targets 逐项补证据：
  - `Hockney (1971)`：`tau_s / tau_H / N_C / optimum path`
    - 已确认正式题名、DOI path 与 abstract-level 定量关系；下一步仍是 materialize full-text PDF
  - `Hockney et al. (1974)`：`K_4 / QPM / potential correction`
    - 已确认正式题名与 DOI；ScienceDirect `.../pdf` 端点在当前环境仍只返回 download-preparation / browser-compatibility 页面，下一步仍是 materialize full-text PDF
  - `Eastwood and Hockney (1974)`：force anisotropy / particle-shape 图
    - 已确认正式题名与 DOI；下一步仍是 materialize full-text PDF
  - `Abe et al. (1975)`：`delta F` heuristic heating estimate
  - `Peiravi and Birdsall (1978)`：smoothing cutoff / weighting-order heating scaling
- [ ] 为 `TajimaDawson1982` 建立论文专属目录、PDF、Markdown、`images/` 与中文讲解笔记。
- [ ] `TajimaDawson1982` 当前已确认：
  - 正式出版信息：*AIP Conference Proceedings* `91(1):69-93`，`Sep 1982`
  - DOI：`10.1063/1.33805`
  - 当前本机仍无现成 PDF / MinerU 产物
  - 已确认 related-but-not-identical 的公开 conference note：FNAL `p169.pdf` *Laser accelerator by plasma waves for ultra-high energies*（`T. Tajima` 单作者）；这不能替代 `TajimaDawson1982`
  - 当前公开 web 证据仍停在 DOI 引用和相关 note，尚未定位到可直接落地本地目录的 full-text PDF
  - 下一步：materialize `TajimaDawson1982` 正文 PDF 后再建论文专属目录与中文讲解笔记
- [x] 继续评估并精读 `Birdsall 1985` 中与 energy-conserving、numerical heating、alias branch 饱和和系统能量账本最直接相关的后续段落。当前已补入 Chapter 9 的 `9-4`、`9-7` 与 Chapter 10 的 `10-2` 到 `10-4`、`10-9` 到 `10-10`，并已明确写清：
  - finite `\Delta t` 的 time alias 与新的 branch-coupling resonance
  - `\omega_p \Delta t`、`v_t \Delta t/\Delta x` 与高噪声 / rapid nonphysical heating 的关系
  - `subcycling / orbit-averaging / implicit methods` 作为快时间尺度病灶的数值应对
  - momentum-conserving 路线下一般不存在严格守恒的总能量
  - energy-conserving 路线把 `W_E=(V_c/2)\sum \rho_j\phi_j` 和 `-\partial W_E/\partial x_i` 当成第一性对象
  - reciprocity / Green's reciprocation theorem 是 exact energy conservation 的真正条件
  - 第 5 / 6 章已做最小文献回填
- [ ] 继续把 `Birdsall 1985` 这几轮读书结论更系统回填到第 3A / 4 / 5 / 6 章。当前已新增：
  - 第 4 章已补入 `energy-conserving` / `momentum-conserving` 不是单纯 gather wrapper 差异，而是两套离散守恒合同的理论边界
  - 第 5 / 6 章已补入 sampled density aliasing、`\sum \rho_j\phi_j` 场能量账本、time alias 与 reciprocity 的最小文献回填
- [x] 评估并精读 `12-3` 到 `12-7` 的 fluctuation / collision / numerical heating kinetic 解释。当前已明确写清：
  - `(\rho^2)_{k,\omega}` 如何同时编码 `S(k_p)`、`\epsilon(k,\omega)` 与时间 alias comb `\omega_g`
  - `1/2\,\rho\phi` 不只是 energy-accounting 变量，也是 fluctuation spectrum 的自然场能量密度
  - `grid collisions` 的 kinetic equation 与 `H`-theorem 如何把 nonphysical heating 压成统计层硬结论
  - drifting plasma 下的数值病灶更准确地应理解为 drag + diffusion + entropy production
  - 第 6 章已做最小文献回填
- [x] 继续把 `Birdsall 1985` 这几轮读书结论和 WarpX 现有 validation 更明确配对。当前已完成：
  - `energy_conserving_thermal_plasma`
    - 对应 Chapter 10 的局部能量账本探针：直接检查总能量漂移是否受控
  - `langmuir*`
    - 对应 Chapter 8/10/12 的解析模与离散守恒探针：解析场解、`divE-rho/\epsilon_0`、solver/deposition/gather 组合边界
  - `uniform_plasma`
    - 对应 Chapter 12 的 noise / writer / checkpoint / restart baseline，而不是独立 physics hard assert
  - `nci_psatd_stability`
    - 对应 Chapter 8/9/12 的 alias-branch / fluctuation-energy suppression probe
- [x] 已决定下一条文献主线：先继续 `Birdsall 1985` Chapter 13，而不是先转回缺口文献 `Hockney-Eastwood` / `TajimaDawson1982`。当前已完成：
  - `13-2`
    - 一维 sheet model、Maxwellian、Debye shielding、wake、drag、diffusion、`\tau = 2N_D/\omega_p`
  - `13-3` 已核实部分
    - 区分 `N_D` 级 randomization/correlation time 与更慢的 `N_D^2` 级 whole-distribution thermalization
- [x] 已继续推进 `Birdsall 1985` Chapter 13。当前已完成：
  - `13-4`
    - `tau_H` 对 `lambda_D/Delta x`、shape order、`v_t Delta t / Delta x` 的依赖
    - damped mover 的 phase error 如何制造 nonphysical cooling
    - 仅靠 `delta F` 的 heuristic estimate 不足以可靠给出 heating/cooling rate
  - `13-5` 已核实部分
    - `tau_s`、`tau_H`、`N_C`、field fluctuation level
    - `tau_H/tau_s` 与 optimum path 的工程意义
- [ ] 继续核实 `Birdsall 1985` Chapter 13 的剩余经验缩放，优先：
  - `13-5`
    - 与 `Hockney-Eastwood` 原书逐项核对：
      - `K_4`
      - QPM
      - `E_x^2` fluctuation 的 `1/N_C` 缩放
      - linear-in-time stochastic heating
      - optimum-path 的设计图和边界条件
- [x] 开始精读 `Tajima and Dawson 1979`。当前已完成：
  - 摘要、引言与最小解析模型的第一轮中文精读
  - `driver -> wake -> trapping -> acceleration` 最小闭环
  - `v_p = v_g^{EM}`、`L_t = \lambda_w/2`
  - `eE_L \cong mc\omega_p`
  - `\gamma_{\max} \simeq 2\omega^2/\omega_p^2`
  - `l_a \cong 2\omega^2 c/\omega_p^3`
  - 已最小回填到 `notes/code-reading/applications/02-lwfa-pwfa.md` 与第 8 章
- [ ] 继续精读 `Tajima and Dawson 1979`，优先：
  - 这篇的第一轮精读主线已基本收口；若再补，优先做图 1 / 图 2 的最终图注级整理
- [x] 开始精读 `Dawson 1983`。当前已完成：
  - 引言、particle models 总述与 electrostatic particle models 的第一轮中文精读
  - 把 computer simulation 明确写成 experiment / analytic theory 之外的第三种研究手段
  - 把 PIC 的最小定义压回“跟踪大量带电粒子在自洽电磁场中的运动”
  - 把 `superparticle` 写成 practical necessity，而不是附属术语
  - 把 finite-size particles 的第一性动机、grid coarse graining，以及 `shape factor -> charge sharing -> FFT Poisson -> gather back` 的标准合同最小回填到第 1 / 5 / 6 章
- [x] 继续精读 `Dawson 1983`。当前已完成：
  - `electromagnetic particle models`
  - `fractional dimensional models`
  - `Darwin` 与 low-frequency magnetic route 的第一轮边界梳理
  - diagnostics / visualization 哲学的第一轮中文精读
  - 已把 `1 1/2-D / 1 2/2-D / 2 1/2-D` reduced-dimension fully electromagnetic models、full EM 的 CFL/light-mode 限制、Darwin 的 radiation-free 低频目标、以及 diagnostics 的 `physics essence` 判断最小回填到第 4 / 6 / 8 章
- [x] 继续精读 `Dawson 1983`。当前已完成：
  - `numerical stability`
  - diagnostics 细分量：
    - distribution function
    - drag
    - diffusion
    - field fluctuations
    - time correlations
    - normal modes
  - `quiet starts` 的第一轮边界梳理
  - 已把 spatial/time aliasing 两类 stroboscopic errors、diagnostics 的 particle-motion / wave 双分法，以及 noisy start / quiet start 的 tradeoff 最小回填到第 6 / 8 章和 `uniform_plasma` 应用笔记
- [x] 继续精读 `Dawson 1983`。当前已完成：
  - weighted particles / electrons of many sizes, charges, and masses
  - quiet-start instabilities 的后续工程边界
  - `free-electron laser` 作为 relativistic EM-PIC 历史例子的第一轮梳理
  - 已把非等权宏粒子的 kinetic-model 边界最小回填到第 1 章，并把 FEL 历史谱系最小回填到第 8 章和束流-FEL 应用笔记
- [x] 继续精读 `Dawson 1983`。当前已完成：
  - `free-electron laser` 图 54-57 与效率估计的图文整理
  - 已把 mechanism verification -> nonlinear saturation -> rough efficiency scaling 这条 FEL 历史论证链最小回填到第 8 章和束流-FEL 应用笔记
- [ ] 继续精读 `Dawson 1983`，优先：
  - 已开始：
    - `Tests of the statistical theory of plasmas`
    - `Kinetics of a one-dimensional plasma`
  - 当前已明确：
    - 一维 electrostatic sheet model 的 benchmark 角色
    - drag / diffusion / field-fluctuation measurements 的统计理论语境
  - 下一步：
    - 已完成：
      - drag 的 velocity-shell ensemble 测量合同
      - velocity diffusion 的 `\tau^2 -> \tau` 双阶段
      - thermal field fluctuation 的 `KT/2` 型 modal-energy 合同与 finite-size 修正
    - 继续补：
      - 已完成：
        - power spectrum / time correlations
        - magnetized fluctuation peaks
        - nonuniform-plasma normal-mode reconstruction
        - continuous-spectrum localization 与 `\delta v(\mathbf v,x,\omega)` 的 kinetic diagnostics 边界
        - random-start 对 weak-instability growth-rate measurement 的限制
        - quiet-start phase-space cell construction 的更细实现边界
        - thermal/noisy starts 与 quiet starts 在弱效应测量中的取舍总结
        - 已评估：`Dawson 1983` 统计理论 / quiet-start 主线已到自然收口点
      - 继续补：
        - 转入下一组基础文献，优先 `Yee 1966`
        - 已完成：`Documents/Desktop/Downloads` 与 `1138693/01138693` 级本机搜索，仍无现成正文
        - 已完成：CiNii / ScienceOpen / 历史 IEEE PDF 端点模式核对，仍无可合法全文
        - 若后续仍无可合法全文，则继续只做 acquisition 边界收口，不进入 MinerU
- [ ] 用 MinerU 处理 Yee 1966、Boris pusher 资料、Vay pusher、Higuera-Cary。
  - [x] 已继续核对 `Boris` 原始资料 acquisition 边界：
    - 已确认项目内已登记的 primary-source metadata 为：
      - `Borisjcp73`
      - `BorisICNSP70`
      - `Habericnsp73`
    - 已确认 `Documents/Desktop/Downloads` 与常用文献目录里没有可直接进入 MinerU 的 primary-source PDF / MinerU 产物
    - 当前本机命中的只有导出代码、讲义和源码副本，不是原始论文正文
  - [x] `Vay 2008` 已 materialize 并复用现成本机 MinerU 产物。
  - [x] `Higuera 2017` 已在项目内完成 MinerU 转换并建立论文目录。
  - [x] `Vay 2008` 第一轮中文精读已启动：
    - 已完成摘要、引言、`II.A/II.B` 最小逻辑
  - [x] `Vay 2008` 主文第一轮精读已基本完成：
    - 已完成单粒子 moving-frame tests
    - 已完成 bounded Darwin-lite field solver 边界
    - 已完成 ultrarelativistic beam / background-electron 应用例子
    - 已回填 `manuscript/chapters/04-particle-pushers.md`
  - [ ] 若继续深挖 `Vay 2008`：
    - Appendix A 的显式解推导
    - Appendix B 的 gyroradius / effective-velocity 边界
  - [x] `Higuera 2017` 第一轮中文精读已启动并完成主文第一轮收口：
    - 已完成摘要、引言、`II-VII`
    - 已明确 `volume-preserving + E×B drift` 的双保持目标
    - 已明确 practical timestep 下 Vay resonance island / topology failure 的证据边界
    - 已回填 `manuscript/chapters/04-particle-pushers.md`
  - [x] 已继续深挖 `Higuera 2017`：
    - 已补 Jacobian / volume-preservation 关键推导
    - 已补与 WarpX `UpdateMomentumHigueraCary.H` 的逐式对位
    - 已补与 `particle_pusher` / `larmor` validation 的真实覆盖边界
  - [ ] 若继续延伸 `Higuera 2017`：
    - 把 Jacobian 证明再压成更完整的逐行符号推导
    - 继续核对 practical-timestep topology 结论与 WarpX 现有 regression 的对应关系
    - 如需再继续，只剩更细的 `J_i/J_f` 逐行代数展开，不再是主线边界缺口
  - [ ] 当前 acquisition 前沿：
    - `Yee 1966` 仍缺可合法全文 PDF
    - `Borisjcp73` 也仍缺可合法全文 PDF
    - 在拿到 primary-source 正文前，不进入这两条线的 MinerU / 中文精读阶段
- [ ] 用 MinerU 处理 Villasenor-Buneman、Esirkepov、Vay deposition。
- [ ] 用 MinerU 处理 Berenger PML、PSATD/Galilean PSATD/NCI 文献。
- [ ] 用 MinerU 处理 WarpX、AMReX、PICSAR/PICSAR-QED、openPMD、PICMI 相关论文。
- [ ] 为每篇深入使用的论文建立论文专属目录、Markdown、`images/`、中文讲解笔记和章节用途记录。

## 每章完成前检查

- [ ] 记录本章依据的 WarpX commit。
- [ ] 公式变量全部定义。
- [ ] 源码路径和行号来自当日重新读取。
- [ ] 所有讲解到的关键源码段都放入了源码原文块。
- [ ] 参数说明回到官方文档或源码解析。
- [ ] 至少一个 Example 或 Regression 对应本章。
- [ ] 关键物理结论有文献或本地运行验证。
- [ ] 未解决问题显式列出，不把猜测写成结论。

## v0.1 后续收口队列

- [x] 第 2、3、3A 章已同步 `8c488b1a9` 源码基线，修正旧 commit 和核心源码行号。
- [x] 第 4 章粒子推进器已同步 `8c488b1a9` 源码基线，修正 Boris half push、主调用链和 `particle_pusher` 强验证入口。
- [x] 第 5 章沉积与形函数已同步 `8c488b1a9` 源码基线，修正 `DepositCurrent/DepositCharge`、AMR buffer、Esirkepov/Villasenor/Vay 和验证入口。
- [x] 第 6 章场求解器已同步 `8c488b1a9` 源码基线，修正 `OneStep_nosub`、FDTD/PSATD/JRhom/PML 分派和验证入口。
- [ ] 将 `manuscript/VERSION.md` 的章节状态表转成每章文件头状态块。
- [ ] 为第 1-8 章各补至少一个“练习 / 复现实验 / 源码定位题”小节。
- [ ] 为 `dist/pic-tutor-v0.1.html` 做一次人工阅读审校，清理重复段落、长表格和过长日志。
- [ ] 审计 public GitHub 仓库中的 PDF、图片和运行产物，区分可公开再分发、仅本地保留和需要改成 DOI/metadata 的材料。
- [ ] 为 `v0.1` 准备 GitHub release notes，明确它是第一卷草稿而非终稿。

## v0.2 后续收口队列

- [ ] 手工通读 `dist/pic-tutor-v0.2.html`，优先清理第 3A 章过长的审计式段落。
- [x] 第 4 章粒子推进器已同步到 `8c488b1a9`，并把 `Examples/Tests/particle_pusher` 的强分析闭环写进正文。
- [x] 第 5 章沉积与形函数已同步到 `8c488b1a9`，并把 `DepositCurrent/DepositCharge` 与 Langmuir / `vay_deposition` 验证入口写进正文。
- [ ] 完成 Esirkepov / Villasenor-Buneman 文献 MinerU 笔记，并回填第 5 章理论小节。
- [x] 第 6 章场求解器已同步到 `8c488b1a9`，已拆清 Yee/CKC/PSATD/JRhom/PML 的证据边界。
- [ ] 给第 2、3、3A 章各补一张读者侧流程图或表格，减少纯文字调用链负担。

## v0.3 后续收口队列

- [ ] 手工通读 `dist/pic-tutor-v0.3.html`，优先检查第 4 章 Boris half-push 公式和源码块是否顺畅。
- [x] 第 5 章沉积与形函数已同步到 `8c488b1a9`，已核 `DepositCurrent/DepositCharge` 和 Esirkepov/Villasenor/Vay 分支。
- [x] 第 6 章场求解器已同步到 `8c488b1a9`，已核 Yee/CKC/PSATD/JRhom/PML 的当前文件路径和行号。
- [ ] 把第 4 章过长的多物理 validation 小节拆成表格或附录，降低正文阅读负担。

## v0.4 后续收口队列

- [ ] 手工通读 `dist/pic-tutor-v0.4.html`，重点检查第 5 章 long chapter 的小节顺序、重复段落和源码块长度。
- [ ] 继续追 `ablastr::particles::deposit_charge(...)` 的实际模板位置，把 `ChargeDeposition` 普通路径补成逐行源码解释。
- [ ] 完成 Esirkepov / Villasenor-Buneman 论文 MinerU 笔记，把 charge-conserving 推导从源码说明升级为文献闭环。
- [x] 第 6 章场求解器已同步到 `8c488b1a9`，已核 Yee/CKC/PSATD/JRhom/PML 的当前文件路径和行号。

## v0.5 后续收口队列

- [ ] 手工通读 `dist/pic-tutor-v0.5.html`，重点检查第 6 章源码入口地图、PSATD/JRhom 长段和 PML 小节是否顺畅。
- [ ] 完成 PSATD / Galilean PSATD / NCI / PML 核心论文 MinerU 笔记，把第 6 章从源码校准升级为文献闭环。
- [x] 给第 6 章补一张场求解器分派流程图和一张 FDTD/PSATD/PML/JRhom 对照表。
- [ ] 继续把第 7 章边界、PML 与 AMR 同步到 `8c488b1a9`，优先核物理边界、field boundary、particle boundary、PML 与 AMR guard-cell 交界。

## v0.6 后续收口队列

- [ ] 手工通读 `dist/pic-tutor-v0.6.html`，重点检查 Mermaid 图、宽表格和第 6 章开头是否在 HTML 中可读。
- [x] 把第 6 章 validation 入口整理成表格，覆盖 `pml`、`nci_psatd_stability`、`langmuir` 和 RZ PSATD 相关 tests。
- [ ] 完成 PSATD / Galilean PSATD / NCI / PML 核心论文 MinerU 笔记，把源码图表与文献公式闭环。
- [ ] 继续把第 7 章边界、PML 与 AMR 同步到 `8c488b1a9`，优先核物理边界、field boundary、particle boundary、PML 与 AMR guard-cell 交界。

## v0.7 后续收口队列

- [ ] 手工通读 `dist/pic-tutor-v0.7.html`，重点检查第 6 章 regression 入口索引表的宽度和可读性。
- [ ] 完成 PSATD / Galilean PSATD / NCI / PML 核心论文 MinerU 笔记，把源码图表、validation 入口和文献公式闭环。
- [ ] 继续把第 7 章边界、PML 与 AMR 同步到 `8c488b1a9`，优先核物理边界、field boundary、particle boundary、PML 与 AMR guard-cell 交界。

## 阻塞点与约束

- [x] `PIC-tutor` 已是 git 仓库，当前分支为 `main`；继续推进前应检查 `git status --short --branch`，不要再按“未初始化 git”的旧假设处理。
- [ ] 书稿最终形态未定：先按中文 Markdown 长书推进，样章稳定后再决定 Quarto/Pandoc/LaTeX。
- [ ] 本机短 WarpX 运行如遇 MPI/OFI 问题，优先设置 `FI_PROVIDER=tcp` 再复现实验。
- [ ] DeepWiki、Zread 等 AI 解读只作索引线索；最终论断必须回到 WarpX 官方文档、本地源码、测试示例和可检索文献。
- 最新推进（2026-05-21）：继续清 AMReX 邻接 still-coarse 条目，已修正 `amrex.async_out / amrex.async_out_nfiles` 的过窄 writer-side 摘要，补清它们属于 `AMReX_AsyncOut` 子系统自己的 parser/bridge：`AsyncOut::Initialize()` 会直接解析 `amrex.async_out{,_nfiles}`、把 `nfiles` 截到 `<= NProcs`，并仅在 `async_out=1 && nfiles < nprocs` 时额外要求 runtime `MPI_THREAD_MULTIPLE`、再按 `GetWriteInfo().ifile` 做 `MPI_Comm_split(...)`。同时补清它们不只作用于 WarpX field plotfile 的 `WriteMultiLevelPlotfile(...)`，粒子 `WriteBinaryParticleDataAsync(...)` 也会复用同一套 `GetWriteInfo()/Wait()/Notify()` 分组写链；相对地，WarpX field checkpoint 仍走 `VisMF::Write(...)` 同步路径，不受这组参数控制。
- 最新推进（2026-05-21）：继续清 AMReX 邻接 still-coarse 条目，已把 `particles.nreaders / nparts_per_read / datadigits_read / use_prepost` 从偏泛 grouped pass-through 摘要压到更准确的粒子 I/O 合同，补清 `nreaders / nparts_per_read / datadigits_read` 真正进入 `ParticleContainer::Restart()` 读盘链，控制 reader ranks、每次读多少粒子后做一次 `Redistribute()` 以及旧版 `DATA_` 文件名位数解析；同时明确 `use_prepost` 实际是 `CheckpointPre()/CheckpointPost()` 与 `WriteBinaryParticleData` 路径中的 checkpoint/write 预聚合开关，而不是 restart 读盘参数。
- 最新推进（2026-05-21）：继续清 AMReX 邻接 still-coarse 条目，已把 `vismf.headerversion / verbose` 再压一层 writer-side 反向边界：补清 `headerversion` 虽然仍由 `VisMF` parser 写回 `currentVersion`，但在 WarpX 的 plotfile/checkpoint flush 路径里会被分别临时强制成 `Version_v1` 与 `NoFabHeader_v1` 后再恢复；相对地，WarpX writer 自己的实例级 `verbose` 只负责本地 “Writing plotfile/checkpoint ...” 提示，并不会桥接到底层 `VisMF::SetVerbose(...)`，因此 `vismf.verbose` 的稳定 consumer 仍主要落在 `VisMF::Read/Check/RemoveFiles` 与 persistent-stream 生命周期。
- 最新推进（2026-05-21）：继续清 AMReX 邻接 still-coarse 条目，已把 `warpx.mffile_nstreams` 再压一层 reader batching 反向边界：补清它在 `VisMF::Read(...)` 里不仅会把同一文件需要读取的 ranks 切成至多 `nStreams` 组，还会在同步读路径里把每个数据文件按 `nOpensPerFile` 重复登记到 `availableFiles`，直接决定同一文件能同时占用多少个读取槽；同时确认若启用了 `usePersistentIFStreams`，一次 `VisMF::Read(...)` 结束后仍会对本次 header 中出现过的数据文件逐个 `DeleteStream(...)`，因此它控制的是单次 restart/PML 读调用内部的并发批次，而不是跨多次调用持续保留的 reader 池。
- 最新推进（2026-05-21）：继续清 AMReX 邻接 still-coarse 条目，已把 `vismf.groupsets / setbuf / checkfilepositions / usepersistentifstreams / usesynchronousreads` 再压一层 field-vs-particle 与写侧校验边界：补清 `vismf.setbuf` 主要只属于 `VisMF/NFiles` 与 persistent input stream 自己的 writer/reader 路径，AMReX 粒子 I/O 与粒子初始化虽然也各自 `pubsetbuf(...)`，但并不读取这条布尔开关；同时明确 `checkfilepositions` 的真实触发点是在 `VisMF::WriteHeader(...)` 里比较 `hss.tellp()` 与 `bytesWritten`，用于校验 MultiFab header 长度一致性，而不是泛化的读盘位置检查。
- 最新推进（2026-05-21）：继续清 AMReX 邻接 still-coarse 条目，已把 `vismf.usedynamicsetselection / iobuffersize / allowsparsewrites / noflushafterwrite / barrierafterlevel` 再压一层 async 反向边界：补清 `iobuffersize` 虽会回流到 `VisMF::IO_Buffer io_buffer(ioBufferSize)` 与 persistent input stream，但 `AMReX_PlotFileUtil.cpp` 的 plotfile header 写链和粒子 I/O 的不少通用流对象仍直接使用常量 `VisMF::IO_Buffer_Size`；同时明确 `noflushafterwrite` 只影响 `VisMF::Write(...)` 的逐 fab 写链，不控制粒子 async writer 里那几处固定 `ofs.flush()`，而 `barrierafterlevel` 在 field plotfile 的 sync/async 路径与粒子 sync writer 中都能生效，却不会成为 particle async writer 的统一 per-level 栅栏 gate。
- 最新推进（2026-05-21）：继续清 diagnostics writer-side still-coarse 条目，已把 `<diag>.file_min_digits` 再压一层 BTD openPMD 反向边界：补清它在普通 diagnostics 与 file-based openPMD 路径里仍控制 `iteration[0]` 或 `openpmd_%0NT.<backend>` 的零填充宽度，但到 BTD openPMD 时，`FlushFormatOpenPMD.cpp` 会把真正传给 `SetStep(...)` 的输出步号切成 `snapshotID`，因此最终 openPMD 容器编号不再复用 boosted-frame `iteration[0]`，而是改由 lab-frame snapshot 序号统一命名。
- 最新推进（2026-05-21）：继续清 diagnostics / particle-output still-coarse 条目，已把 `<diag>.species` 再压一层 particle-writer 反向边界：补清只有 full checkpoint 的默认回退会把 `GetSpeciesAndLasersNames()` 一并带入 species 列表，而 boundary-scraping 与 BTD 的默认回退都只落到 physical species；同时明确 boundary-scraping 即便已经按 species/boundary 完成 `ParticleDiag` 绑定，`Flush()` 仍会先统计边界 buffer 粒子数，只要总数为零就静默跳过 writer，因此 species 绑定本身并不保证一定产生边界粒子输出。
- [x] 2026-05-21：继续收口 `qed_schwinger.y_size`
  - 已补清这条 2D 厚度参数的 startup 强制性：`MultiParticleContainer.H` 里 `m_qed_schwinger_y_size` 当前没有本地默认值，而 `XZ/RZ` 下 `do_qed_schwinger` 一旦打开，就会经 `getWithParser(...)` 强制读取，所以它不是可省略 companion。
  - 已补清它和几何裁剪/权重链的反向边界：2D `ComputeSchwingerGlobalBox()` 的空间掩膜只看 `xmin/xmax/zmin/zmax`，不读取 `y_size`；真正消费这条值的是 `XZ` 路径下的 `dV` 构造、`SchwingerFilterFunc -> getSchwingerProductionNumber(...)` 的 cell 级产额抽样，以及 `SchwingerTransformFunc` 里的 `1/m_y_size` 宏粒子权重归一。更细一层是：这份总产额本身是 cell 级量，但后续不会按总 pair 数扩增宏粒子个数，而是先经 `arrNumPartCreation > 0` 建 mask、再把新增计数固定成命中 cell 数，最终才回填到 create-on-node 的电子/正电子粒子上；而 `RZ` 虽然走同一 parser 分支，运行时会更早直接 abort。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_embedded_boundary_em_particle_absorption_sh_factor_3`：已把这条名字和运行时一致的 3D `shape factor = 3` baseline 从宽泛“对应 3D `shape factor = 3` 版本”压实为更精确的 3D 时间平均消费者合同，并写清当前输入在公共基线上显式切到 `geometry.dims = 3`、`algo.particle_shape = 3`，所以这次名字当前确实命中独立的 3D `shape factor = 3` runtime 路径；相对地，共享 `analysis.py` 仍只是在 `3dcartesian` 分支上对整张时间平均 `divE_avg` 施加 `abs(divE_avg).max() <= 7e-11` 的无伪电荷约束。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_electrostatic_sphere_eb`：已把这条 3D 固定电势导体球 EB baseline 从宽泛“对应 EB sphere 场景”压实为更精确的双消费者合同，并写清当前输入不仅固定了半径 `0.1`、电势 `1 V` 的球形 EB，还同时打开总电荷与八分体 `ChargeOnEB` reduced diag，以及包含 `eb_covered` 的 openPMD 场诊断；相对地，共享 `analysis.py` 会分别要求总电荷与八分体电荷在 `6%` 误差内逼近解析 `q_th` 和 `q_th/8`，再逐格检查 `eb_covered` 在球内为 `1`、球外为 `0` 且全域都落在 `[0,1]`。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_electrostatic_sphere_eb_picmi`：已把这条 3D PICMI 导体球 EB baseline 从宽泛“对应 PICMI EB sphere 场景”压实为更精确的 PICMI runtime 合同，并写清当前输入不走 native 输入卡，而是显式通过 `picmi.Cartesian3DGrid + ElectrostaticSolver + EmbeddedBoundary` 组装半径 `0.1`、初始电势 `1 V` 的球形导体 EB，并在 `sim.step(1)` 之后调用 `sim.extension.warpx.set_potential_on_eb("2.")` 再继续第二步推进；相对地，共享 `analysis.py` 仍消费与 native 对齐的 `ChargeOnEB + eb_covered` 双消费者链。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_electrostatic_sphere_eb_mixed_bc`：已把这条 mixed-BC 3D 导体球 EB baseline 从宽泛“对应 mixed-BC 变体”压实为更精确的纯 checksum 消费路径，并写清当前在 `CMakeLists.txt` 里明确是 `analysis=OFF + analysis_default_regression.py --path diags/diag1000001`；同时补清输入侧的真实边界组合是 `boundary.field_lo = pec pec neumann`、`boundary.field_hi = pec neumann neumann`，只给 `potential_lo_x / potential_hi_x / potential_lo_y` 写出 Dirichlet 电势，球形 EB 半径改成 `0.3`，且诊断只输出 `Ex/Ey/Ez/rho/phi`，不再落 `eb_covered` 或 `ChargeOnEB` reduced diagnostics。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_effective_potential_electrostatic_picmi`：已把这条 3D PICMI effective-potential electrostatic baseline 从宽泛“对应 PICMI-only effective-potential benchmark”压实为更精确的前端加径向密度消费者合同，并写清当前输入显式通过 `picmi.ElectrostaticSolver(..., warpx_effective_potential=True, warpx_effective_potential_factor=C_EP)` 打开 effective-potential Poisson solver 路径，同时把 `sigma_0/M/T_i/T_e/n_plasma` 序列化到 `sim_parameters.dpkl`，再把 openPMD `field_diag` 周期性输出到 `diags/field_diag/`；相对地，共享 `analysis.py` 会重建解析高斯膨胀密度，并对每个 iteration 的 `rho_electrons` 做球坐标重采样和角向平均，要求整段时间序列上的归一化 RMS 误差都小于 `0.07`。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_electrostatic_sphere`：已把这条 3D relativistic electrostatic 自场膨胀 baseline 从宽泛“对应主基线”压实为更精确的三轴解析场消费者合同，并写清当前输入主要复用 `inputs_base_3d` 里的 `warpx.do_electrostatic = relativistic`、静止电子云装填和 `diag1/diag2` 诊断布局；相对地，共享 `analysis_electrostatic_sphere.py` 会用最终 plotfile 的真实 `t_max` 反求膨胀半径 `r_end`，再沿 `x/y/z` 三轴分别要求解析场相对 `L2` 误差都小于 `0.05`，而由于 `diag2` 不含 `phi`，能量账本分支在这条路径上不会触发。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_eb_picmi`：已把这条 3D EB PICMI baseline 从宽泛“对应 checkpoint scaffold”压实为更精确的 active/restart 边界，并写清当前 `restart_eb/CMakeLists.txt` 只启用了 `analysis=OFF + analysis_default_regression.py --path diags/diag1000060` 的 active 基线，而真正的 `test_3d_eb_picmi_restart` 仍整段注释为 `FIXME`；相对地，输入 `inputs_test_3d_eb_picmi.py` 已经显式打通 `Checkpoint(name="chk")`、`amr.restart` 参数接收和基于 `getistep()` 的剩余步数推进路径，所以现阶段更准确的是“checkpoint/resume 兼容输入路径 + 最终 plotfile checksum”而不是独立 restart regression。
- [x] 2026-05-25：继续清理 `docs/example-regression-map.md` 的 `test_3d_gaussian_beam_picmi`：已把这条 3D PICMI Gaussian beam baseline 从宽泛“对应 `GaussianBunchDistribution` 前端接线”压实为更精确的前端加 checksum 合同，并写清当前 `gaussian_beam/CMakeLists.txt` 实际是 `analysis=OFF + analysis_default_regression.py --path diags/diag1000010`，没有复用 `analysis_focusing_beam.py`；相对地，输入脚本显式暴露 `--diagformat/--fields_to_plot` CLI 参数，并用两套 `picmi.GaussianBunchDistribution` 组装散焦电子束和无散焦质子束，再分别用 `PseudoRandomLayout(n_macroparticles=32768)` 注入。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `ion_stopping` family 输入侧：已把 `inputs_test_3d_ion_stopping` 从宽泛“3D background_stopping 总测试”压实为“四组 `do_not_deposit = 1` 测试离子 + 电子/离子背景 × constant/parser 四条 `background_stopping` 路径 + 每步 full plotfile producer”的 runtime scaffold，并写清两类初始相空间布置与 parsed 背景的 `if(x>0,...)` / `if(y>0,...)` 分段。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `initial_distribution` family-level 行：已把 `analysis.py` 从宽泛“多分布直方图/束斑统计检查”压实为“二十多个 reduced histogram/beam-monitor diagnostics + 九类初始化分布逐项解析闭合”的强分析链；同时把 `analysis_default_regression.py` 补成目录内符号链接到共享 `plotfile/openpmd` checksum helper 的准确边界，并把 `inputs_test_3d_initial_distribution` 补清为九组 species 加整套 reduced diagnostics 面的 runtime scaffold。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `initial_plasma_profile` family：已把 `analysis_default_regression.py` 从宽泛“通用 checksum helper”压实为目录内符号链接到共享 `plotfile/openpmd` checksum 包装器、且当前只以 `--skip-particles --rtol 1e-4` 服务 `test_2d_parabolic_channel_initialization`；同时把输入卡补清为“横向 parabolic channel + 纵向 cosine up-ramp/plateau/down-ramp”的 parser 密度 scaffold，并把 baseline 也改写成明确的单帧 `rho` 字段 checksum 消费者链。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `load_external_field` family-level analysis 行：已把 `analysis_3d.py` 从宽泛“3D 磁镜单粒子轨道”压实为只服务 `test_3d_load_external_field_grid_picmi` 与 `test_3d_load_external_field_particle_picmi` 两条 active regression 的末态位置消费者链，并写清它当前只读取 proton `x/y/z`，对参考末态 `(0.12238072, 0.00965395, 4.31754477)` 施加 `error < 1e-8` 断言。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `linear_compton` family-level 行：已把 `analysis_base.py` 压实为 reduced diagnostics 加首末 `rho` 场的守恒基座，把 `analysis_bunch_laser.py` 压实为纵向动量守恒、零横向总动量和 Klein-Nishina 散射分数断言，把 `analysis_two_particles.py` 压实为单对 reactant 被完全散射并只生成一对 product 宏粒子的强检查；同时把 shared `analysis_default_regression.py` 补成目录内符号链接到共享 checksum helper 的准确边界，并补清 `bunch_laser` / `two_particles` 两张输入卡的 runtime scaffold。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `maxwell_hybrid_qed` family-level 行：已把 `analysis.py` 压实为“最终 `Ey` 中轴峰值漂移 -> hybrid-QED 理论真空色散相速度”的单断言链，把 `analysis_default_regression.py` 补成目录内符号链接到共享 checksum helper 的准确边界，并把输入卡补清为 `WarpX_FFT` gate 下的 2D collocated PSATD + `use_hybrid_QED=1` 解析外场单脉冲 scaffold。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `magnetostatic_eb` family-level helper 行：已把 `analysis_default_regression.py` 从宽泛“目录内 checksum helper”压实为 `WarpX_EB` gate 下只服务 `test_3d_magnetostatic_eb`、`test_3d_magnetostatic_eb_picmi` 与 `test_rz_magnetostatic_eb_picmi` 的附加 checksum 链，并写清 RZ 变体当前显式带 `--skip-particles`。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `nci_fdtd_stability` family-level 行：已把 shared `analysis_default_regression.py` 压实为只服务 `test_2d_nci_corrector` / `test_2d_nci_corrector_mr` 的附加 checksum 链，把 `analysis_ncicorr.py` 压实为最终 `Ex/Ez/By` field-energy proxy 的强断言，并明确脚本里的 MR 阈值分支当前尚未从现有 `CMakeLists.txt` 注册层显式闭环；同时把 `inputs_base_2d` 与两条 overlay 补成更明确的共享 drifting-plasma scaffold 加 non-MR/MR 窄分叉。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `linear_breit_wheeler` family-level 行：已把 `analysis_base.py` 压实为 reduced diagnostics 加首末 `rho` 场的守恒基座，把 `analysis_many_photons.py` 压实为理论 pair-yield 时间演化对 reduced `ParticleNumber` 的强检查，把 `analysis_two_photons.py` 压实为单对 photons 被完全转化成两对电子-正电子 product 宏粒子的强检查；同时把 shared `analysis_default_regression.py` 补成目录内符号链接到共享 checksum helper 的准确边界，并补清 `many_photons` / `two_photons` 两张输入卡的 runtime scaffold。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `load_external_field` family-level analysis 行：已把 `analysis_rz.py` 压实为只服务 `test_rz_load_external_field_grid` 与 `test_rz_load_external_field_particles` 的 RZ theta-mode 磁镜末态位置消费者链；同时把 `analysis_default_restart.py` 补成只服务三条 active restart regression 的逐字段逐 species restart-state 对照链。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `pec` analysis-level 行：已把 `Examples/Tests/pec/analysis_pec.py` 再补硬一层，明确写清它是 `test_3d_pec_field` 与 `test_3d_pmc_field` 共享的唯一主 analysis，当前只消费被 CMake 钉死传入的单个末态 plotfile 上的全域 `Ey` 数组，并只对 `max/min Ey` 相对理论 `±2E_in` 的振幅翻倍合同施加 `1%` 误差 gate；脚本虽然会额外生成 `Ey_pec_analysis.png`，注释里也提到边界 `Ey=0`，但这两者当前都不属于自动断言面。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `pec` analysis-level 行：已把 `Examples/Tests/pec/analysis_pec_mr.py` 从占位补成实义条目，明确写清它是 `test_3d_pec_field_mr` 的唯一主 analysis，当前只消费单个末态 plotfile 上 level-0 covering-grid 的全域 `Ey` 极值，并对相对理论 `±2E_in` 的 standing-wave 振幅翻倍合同施加 `5%` 误差 gate；脚本虽会额外生成 `Ey_pec_analysis_mr.png`，也提到边界 `Ey=0`，但这些都不属于自动断言面。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `pec` analysis-level 行：已把 `Examples/Tests/pec/analysis_pec_insulator_implicit.py` 从占位补成实义条目，明确写清它是 `test_2d_pec_field_insulator_implicit` 与 `_restart` 共享的唯一主 analysis，真正消费的是 `reducedfiles/fieldenergy.txt` 和 `poyntingflux.txt` 的全时序能量账本，而不是末态 plotfile 本体；自动 gate 当前锁在 machine-precision 量级的 `1e-13` 归一化能量记账误差。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `pec` family-level 行：已把 `analysis_pec.py`、`analysis_pec_mr.py` 与 `analysis_pec_insulator_implicit.py` 再补一层 family 回指，明确它们分别落在同一条 mixed split 里的 `2` 条 3D standing-wave shared chain、`1` 条 MR standing-wave branch 和 `2` 条 implicit-insulator energy-accounting branch；这样这组 family 现在已经在 helper、analysis、baseline/input 三层都显式闭合。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `particles_in_pml` family-level 行：已把 `analysis_particles_in_pml.py` 再补一层 family 回指，明确它当前服务 `2D/3D × single-level/MR` 四条 active regression 的共享主消费者链，并把这组 family 的维度/AMR split 显式写回 analysis-level 行本身。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `photon_pusher` family-level 行：已把 `analysis.py` 再补一层 family 回指，明确它当前对应唯一 active baseline `test_3d_photon_pusher` 的 same-final-plotfile main consumer，并把这组 family 的单一路径分布语义显式写回 analysis-level 行本身。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `particle_thermal_boundary` family-level 行：已把 `analysis.py` 再补一层 family 回指，明确它当前对应唯一 active baseline `test_2d_particle_thermal_boundary` 的 reduced-energy main consumer，并把 `reduced main surface + separate checksum side surface` 这组分布语义显式写回 analysis-level 行本身。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `particle_pusher` family-level 行：已把 `analysis.py` 再补一层 family 回指，明确它当前对应唯一 active baseline `test_3d_particle_pusher` 的 same-final-plotfile main consumer，并把这组 `single active baseline + shared final surface` 语义显式写回 analysis-level 行本身。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `particle_fields_diags` family-level 行：已把 `analysis_particle_diags.py` 与 `analysis_particle_diags_single.py` 再补一层 active/reserve 回指，明确前者是唯一 active 双精度 wrapper，后者是未注册的 single-precision reserve wrapper，并把这组 family 分布语义显式写回 analysis-level 行本身。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `point_of_contact_eb` family-level 行：已把 `analysis.py` 再补一层 family 回指，明确它当前服务 `test_3d_point_of_contact_eb` 与 `test_rz_point_of_contact_eb` 这 `3D + RZ` 两条 active baseline 的共享 BoundaryScraping main consumer，并把这组 family 分布语义显式写回 analysis-level 行本身。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `pec` input-level 行：已把 `inputs_test_2d_pec_field_insulator_implicit{,_restart}` 成组补硬，明确写清主线输入当前 materialize 的是 `2D local pec_insulator boundary drive + theta_implicit_em + Picard + FieldEnergy/FieldPoyntingFlux reduced diagnostics` scaffold，而 restart 变体真正新增的 runtime 分叉只有 `chk000010 -> step 20` 的 continuation；两条路径当前共同验证的都是同一条 `<1e-13` 的 reduced-energy accounting consumer 链，而不是 plotfile-by-plotfile restart 对照。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `pec` input-level 行：已把 `inputs_test_3d_pec_field{,_mr}` 成组补硬，明确写清单级/MR 两条路径当前共享同一组局域 parser `Ey/Bx` 外加正弦波包 scaffold，真正分叉只在 `amr.max_level=0` 对比 `level-1 refined cube`；两条 active regression 当前都只把末态 `Ey/Bx` plotfile 送进全域 `Ey` 极值消费者链，其中 MR 版仍只看 level-0 covering-grid，并把振幅翻倍误差 gate 放宽到 `5%`。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `pec` input-level 行：已把 `inputs_test_2d_pec_field_insulator` 再补硬一层，明确写清它当前 materialize 的是 `2D local pec_insulator explicit boundary drive + single-final-plotfile producer`，而在 active 注册里仍是 `analysis=OFF + checksum-only`；也就是说，这条显式路径当前唯一自动消费者就是末态 `diag1000010` 的附加 checksum，不再隐含一条并不存在的独立 physics analysis。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `pec` input-level 行：已把 `inputs_test_3d_pmc_field` 再补硬一层，明确写清它当前与单级 PEC 版几乎完整共享同一组局域 parser `Ey/Bx` 外加波包 scaffold，真正新增的 runtime 分叉只在把反射边界切成 `PMC` 并把末态 plotfile 钉到 `diag1000134`；下游当前仍复用同一个全域 `Ey` 极值振幅翻倍消费者链。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `pml` input-level 行：已把 `inputs_test_2d_pml_x_galilean` 再补硬一层，明确写清它当前同样完整继承 `inputs_base_2d` 的共享 producer 面，但相对 plain `psatd` 版额外打开了 `psatd.v_galilean = 0 0 0.99`、`collocated` grid 和 PML 内 `divB/divE` cleaning；下游共享 `analysis_pml_psatd.py` 也会按目录名切到另一套 branch-specific 初始能量常数。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `pml` input-level 行：已把 `inputs_test_2d_pml_x_psatd` 再补硬一层，明确写清它当前完整继承 `inputs_base_2d` 的 2D 全 `pml` + Gaussian laser + `diag1@50/chk@150` producer 面，真正新增的只是 plain `psatd` solver 分支、`rho/divE` 字段面、`update_with_rho = 1` 和 `do_pml_divb/dive_cleaning = 0` 这组 no-cleaning 开边界合同。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `pml` analysis-level 行：已把 `analysis_pml_psatd_rz.py` 再补硬一层，明确写清它当前只消费单个末态 `diag1000500`，必要时先走一次 `force_periodicity()` 兼容层，然后只看 level-0 `Er/Ez` 的最坏残余场强，并对 `max(|Er|,|Ez|) < 2.0` 施加单阈值 gate。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `pml` base-level 行：已把 `inputs_base_2d` 再补硬一层，明确写清它当前不只是抽象 family 骨架，而是一次性 materialize 了 2D 全 `pml` 静止盒子、单束 Gaussian laser、`diag1@50` 和 `chk@150` 这整套共享 producer 面；Yee/CKC/PSATD/Galilean 只是各自在这之上覆写 solver 分支，restart 变体则专门依赖这里产出的 `chk000150`。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `pml` analysis-level 行：已把 `analysis_pml_ckc.py` 再补硬一层，明确写清它当前和 `Yee` 版一样只消费单个末态 `diag1000300`，直接用脚本内置 `energy_start = 9.1301289517e-08` 重建反射率，但最终对比的单理论常数换成 `Reflectivity_theory = 1.8015e-06`。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `pml` analysis-level 行：已把 `analysis_pml_yee.py` 再补硬一层，明确写清它当前只消费单个末态 `diag1000300`，不会像 `psatd` 版那样回读第 `50` 步参考帧，而是直接用脚本内置 `energy_start = 9.1301289517e-08` 与 `Reflectivity_theory = 5.683000058954201e-07` 做单理论反射率 gate。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `pml` analysis-level 行：已把 `analysis_pml_psatd.py` 再补硬一层，明确写清它当前是普通 `psatd` 和 `galilean psatd` 两条 active regression 共享的唯一主 analysis，而且不只消费末态 `diag1000300`，还会硬编码回读第 `50` 步 `diag1000050` 作为 branch-specific 初始能量参考面，再叠加最终 `reflectivity < 1e-6` gate。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `pass_mpi_communicator` helper-level 行：已把 `analysis_default_regression.py` 再补硬一层，明确写清它当前虽然只是目录内指向共享 helper 的 symlink，但脚本本体已经具备完整的 `plotfile/openpmd` 自动探测与 `do_fields/do_particles` 下沉逻辑；真正的问题不是 helper 缺能力，而是整个 `test_2d_pass_mpi_comm_picmi` 目前仍 `analysis=OFF + checksum=OFF`，完全没有接入这条链。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `pass_mpi_communicator` input-level 行：已把 `inputs_test_2d_pass_mpi_comm_picmi.py` 再补硬一层，明确写清这条脚本当前其实已经 materialize 出 `split-communicator + dual-density + dual-prefix diagnostics` 的 PICMI scaffold，但 `sim.step(..., mpi_comm=new_comm)` 和所有 communicator 断言都仍处于注释态，因此整个 family 仍是 reserve-only。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `pass_mpi_communicator` analysis-level 行：已把 `pass_mpi_communicator/analysis.py` 再补硬一层，明确写清它当前不是 active regression 的主 analysis，而是一个未接入回归链的离线双 plotfile checksum-diff 对照脚本：要求两份 communicator-split 输出的 checksum schema 同构，但除 `particle_cpu/id/particle_position_y` 外的绝大多数数值项必须彼此不同。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `photon_pusher` analysis-level 行：已把 `photon_pusher/analysis.py` 再补硬一层，明确写清它当前是 `test_3d_photon_pusher` 的唯一主 analysis，只消费单个末态 `diag1000050`，并用脚本内置的 16-species 方向/动量矩阵直接重建理论直线轨道和不变动量，最后只对全局最坏 `disc_pos/disc_mom` 施加 `1e-14 / eps` gate。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `plasma_lens` analysis-level 行：已把 `plasma_lens/analysis.py` 再补硬一层，明确写清它当前是六条 active plasma-lens regression 共享的唯一主 analysis，只消费单个末态 `diag1000084`，并在 `PICMI/native` 粒子参数来源、`repeated_plasma_lens/lattice.elements` 外场前端和可选 boosted-frame 反变换之间分流后，再用 `applylens(...)` 逐段重演解析透镜链。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `pec` input-level 行：已把 `inputs_test_3d_pec_particle` 再补硬一层，明确写清它当前不是一般等离子体场景，而是在 `x` 向 PEC 边界附近只放两颗等质量重粒子，用来压住切向 `Ey` gather/deposition 路径；这条 active regression 目前仍是 `analysis=OFF + checksum-only`，唯一自动消费者是末态 `diag1000020` 的场/电流分量 checksum。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的相邻 family input-level 行：已把 `photon_pusher/inputs_test_3d_photon_pusher` 再补硬一层，明确写清这条路径当前不是泛泛“16 个单光子”，而是 `8 个方向 × 2 档动量幅值` 的 photon matrix；末态 producer 只保留各 species 的 `x/y/z/ux/uy/uz`，并直接闭合到 `analysis.py` 的直线传播与动量守恒强断言。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的相邻 family input-level 行：已把 `plasma_lens/inputs_test_3d_plasma_lens` 再补硬一层，明确写清这条主线当前不是一般束团，而是 `x/y` 两条正交单电子轨道穿过四段 `repeated_plasma_lens` 外场链；末态 producer 只保留粒子 `x/y/z/ux/uy/uz`，并直接闭合到解析串联透镜模型对最终 `x/y/ux/uy` 的强断言。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的相邻 family input-level 行：已把 `plasma_lens/inputs_test_3d_plasma_lens_boosted` 再补硬一层，明确写清它当前几乎完整继承主线 repeated-plasma-lens scaffold，真正新增的 runtime 分叉只在 `gamma_boost=2, boost_direction=z` 和相应的 boosted `z` 域；下游共享 analysis 会先把末态 `z` 反变换回 lab frame，再复用同一条解析串联透镜消费者链。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的相邻 family input-level 行：已把 `plasma_lens/inputs_test_3d_plasma_lens_short` 再补硬一层，明确写清它当前真正新增的 runtime 分叉是把 lens 长度压到 `1e-3` 量级、把 `strengths_E` 提高两个数量级，从而专门构造 single-step residence-correction 场景；虽然输入现在每步都写 plotfile，但 active consumer 仍只钉死末态 `diag1000084`，analysis 也只因此把位置/速度 gate 放宽到 `0.023 / 0.003`。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的相邻 family input-level 行：已把 `plasma_lens/inputs_test_3d_plasma_lens_hard_edged` 再补硬一层，明确写清这条路径当前几乎完整继承主线两粒子 scaffold，真正新增的 runtime 分叉只在 external-field 前端切到 `lattice.elements + plasmalens*.type = plasmalens`；下游共享 analysis 会先把 lattice 序列折回同构的 lens-chain 语义，再复用同一条解析透镜消费者链。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的相邻 family input-level 行：已把 `plasma_lens/inputs_test_3d_plasma_lens_picmi.py` 再补硬一层，明确写清这条路径当前在物理语义上几乎完整复刻主线 repeated-plasma-lens scaffold，但 producer 面被显式搬到 PICMI 前端：`Cartesian3DGrid + dual ParticleListDistribution + PlasmaLens + Simulation.add_applied_field`；下游共享 analysis 也会优先读取 `electrons.dist0/dist1.*` 这组 PICMI materialization。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的相邻 family input-level 行：已把 `plasma_lens/inputs_test_3d_plasma_lens_python.py` 再补硬一层，明确写清这条路径当前既不走 native inputs 也不走 PICMI，而是通过 `pywarpx` 顶层参数对象把主线 repeated-plasma-lens scaffold 逐项 materialize 后直接 `warpx.init(); warpx.step(...)`；真正新增覆盖的是 Python 参数表到 C++ 初始化/推进主链的接线。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `nodal_electrostatic` family 邻接条目：已把 `analysis.py` 从宽泛“零触发验证”压实为固定消费 `ParticleExtrema_beam_p.txt` 与 `ParticleNumber.txt` 的 reduced main consumer，并写清它当前只对 `chi_max < 2e-8` 与源码里的 `pho_num.all() == 0.0` 布尔门做强断言。`inputs_test_3d_nodal_electrostatic_solver` 也已补清其显式 materialize `collocated + relativistic electrostatic + Vay + positron self-fields + QED quantum synchrotron product species` 的窄 runtime，同时落出每步 reduced diagnostics 和末态 `diag1000010` plotfile；因此 `test_3d_nodal_electrostatic_solver.json` 现在也已收口成“reduced zero-trigger main consumer + separate final-plotfile checksum side surface”的双层合同。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `effective_potential_electrostatic` 邻接条目：已把 `analysis_default_regression.py` 从宽泛“本地 checksum helper”压实为只服务 `test_3d_effective_potential_electrostatic_picmi` 的 same-directory openPMD checksum wrapper，并写清它当前与主 analysis 共用同一个 `diags/field_diag/` openPMD 目录，而不是分离 side surface；相应地，`test_3d_effective_potential_electrostatic_picmi.json` 也已补清其真实结构是“`sim_parameters.dpkl + field_diag/` 径向电子密度 RMS 主消费者链 + 同目录附加 checksum”。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `open_bc_poisson_solver` 邻接条目：已把 `analysis_default_regression.py` 从宽泛“本地 checksum helper”压实为只服务普通版和 sliced-FFT 版两条 active regression 的 final-plotfile checksum side surface，并写清主 analysis 当前完全绕过该 `--path`，固定回读 `diag2` openPMD 的 `Ex/Ey`。相应地，`test_3d_open_bc_poisson_solver{,_sliced}.json` 也已补清其真实结构是“openPMD 横场 Basseti-Erskine 主消费者链 + 分离的 `diag1000001 --rtol 1e-2` plotfile checksum side surface”。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `relativistic_space_charge_initialization` 邻接条目：已把 `analysis_default_regression.py` 从宽泛“本地 checksum helper”压实为只服务 `test_3d_relativistic_space_charge_initialization` 的 same-final-plotfile、fields-only checksum wrapper，并写清它当前被显式钉成 `--path diags/diag1000001 --skip-particles`。相应地，`test_3d_relativistic_space_charge_initialization.json` 也已补清其真实结构是“同一末态 plotfile 上的 three-component Coulomb-field 主消费者链 + fields-only 附加 checksum”。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `electrostatic_sphere_eb` 邻接条目：已把 `analysis_default_regression.py` 从宽泛“family checksum helper”压实为四种真实 wiring 形态的汇总服务面，并写清当前 3D native/PICMI 与 RZ+MR 都是 same-surface additive checksum，3D mixed-BC 是 checksum-only，而 RZ 单层版则是 same-final-plotfile 的 fields-only additive checksum；它本身并不消费 `ChargeOnEB + eb_covered` 或解析 `phi/Er` 主消费者链。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `electrostatic_sphere` 邻接条目：已把 `analysis_default_regression.py` 从宽泛“本地 checksum helper”压实为覆盖 7 条 active regression 的 same-final-plotfile additive checksum wrapper，并写清整个 family 当前都不是分离 side surface 结构，而是主 analysis 与 checksum 共用同一末态 plotfile；它本身并不消费解析场主断言，也不消费条件触发的 openPMD `Ek + Ep` 能量账本分支。
- [x] 2026-05-28：继续清理 `docs/example-regression-map.md` 的 `electrostatic_dirichlet_bc` 邻接条目：已把 `analysis_default_regression.py` 从宽泛“本地 checksum helper”压实为同时服务 native 与 PICMI 两条 active regression 的 same-final-plotfile additive checksum wrapper，并写清两条路径当前都不是分离 side surface，而是主 analysis 与 checksum 共用同一个 `diag1000100` 末态 plotfile；它本身并不消费边界 `phi(t)` 时间序列主断言。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `restart_eb` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前只服务唯一一条 active baseline `test_3d_eb_picmi`，并且这条路径没有独立 analysis，唯一自动消费者链就是对 `diags/diag1000060` 的 checksum；相对地，`test_3d_eb_picmi_restart` 仍整段停在 `FIXME` 注释态，保留为同一 output surface 上的 reserve-only restart sibling。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `capacitive_discharge` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前统一服务 `4` 条 active baseline，并稳定分成 `1/1/2` mixed split：`1D background_mcc`、`1D dsmc` 两条 shared-analysis 主链，加上 `2D native/PICMI` 两条 checksum-only sibling；四条路径都共同固定消费同一个 `diags/diag1000050` final plotfile checksum surface。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `free_electron_laser` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前只服务唯一一条 active baseline `test_1d_fel`，并且与主 `analysis_fel.py` 共同固定消费同一个 `diags/diag_labframe` openPMD 主 surface；相对地，主 analysis 还会额外旁路回读 `diags/diag_boostedframe` 去完成 boosted-frame 重建链，所以 helper 更准确地是 same-directory additive checksum wrapper。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `ion_beam_extraction` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前只服务唯一一条 active baseline `test_3d_ion_beam_extraction`，并且与主 `analysis_ion_beam_extraction.py` 共同固定消费同一个 `diags/diag1/` openPMD 目录，所以更准确地是 same-directory additive checksum wrapper。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `laser_ion` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前统一服务 `test_2d_laser_ion_acc` 与 `test_2d_laser_ion_acc_picmi` 两条 active baseline，并共同固定消费同一个 `diags/diagInst/` 目录；但按 shared `analysis_test_laser_ion.py` 的 runtime 分支，这组 wiring 实际落成 `1+1` mixed split：native 路径真正命中 `diagInst` 对 `diagTimeAvg` 的 `E_z` 主链，而 PICMI 路径当前只剩 same-directory checksum sibling。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `thomson_parabola_spectrometer` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前只服务唯一一条 active baseline `test_3d_thomson_parabola_spectrometer`，并且对应的是分离 output-surface 结构：helper 单独消费 `diags/diag1` checksum surface，而主 `analysis.py` 固定回读 `diag0 + screen/particles_at_zhi` 两条独立 openPMD main side channel。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `accelerator_lattice` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前统一服务 `test_3d_hard_edged_quadrupoles`、`test_3d_hard_edged_quadrupoles_boosted` 和 `test_3d_hard_edged_quadrupoles_moving` 这 `3` 条 active baseline，并共同固定消费同一个 `diags/diag1000050` final plotfile surface；相对地，shared `analysis.py` 继续对应递归 lattice 展开、optional boosted-to-lab `z` backtransform 与解析透镜串联末态 `x/ux` 主链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `resampling` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前统一服务 `3` 条 active baseline，并稳定分成 `2+1` mixed split：`2` 条 `1D velocity_coincidence_thinning` checksum-only sibling 共同固定消费 `diags/diag1000004`，以及 `1` 条 `2D leveling_thinning` shared-analysis 主链固定消费 `diags/diag1000008`。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `restart` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前不是单一子族 helper，而是 `restart` family 的 mixed checksum wrapper：`2` 条 2D PICMI checksum-only sibling、`1` 条 3D CKC non-restart surface、`1` 条 3D CKC restart reproducibility 主链上的 additive checksum sibling，以及在 `WarpX_FFT` 打开时再并排加上的 `PSATD` / `PSATD time-averaged` 两对 sibling；这些路径当前都共用同一个 `diags/diag1000010` surface。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `repelling_particles` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前只服务唯一一条 active baseline `test_2d_repelling_particles`，并且与主 `analysis.py` 共同固定消费同一个末态 `diags/diag1000200` surface；相对地，主 analysis 会再由此反解整段 `diag10000*` 序列，完成双单粒子解析能量账本主链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `btd_rz` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前只服务唯一一条 active baseline `test_rz_btd`，并且对应的是分离 output-surface 结构：helper 单独消费 `diags/diag1000289` checksum surface，而主 `analysis.py` 固定回读 `./diags/back_rz` 的 back-transformed openPMD 主 surface。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `boosted_diags` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前只服务唯一一条 active baseline `test_3d_laser_acceleration_btd`，并且对应的是分离 output-surface 结构：helper 单独消费 `diags/diag1000003` checksum surface，而主 `analysis.py` 固定回读 `./diags/diag2/openpmd_%T.h5` 作为独立 openPMD main side channel。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `boundaries` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前只服务唯一一条 active baseline `test_3d_particle_boundaries`，并且与主 `analysis.py` 共同固定消费同一个末态 `diags/diag1000008` surface；相对地，主 analysis 还会再反解对应的 `diag1000000` 初态去完成 reflecting / absorbing / periodic 三组粒子的 relativistic boundary-contract 主链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `virtual_photons` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前统一服务 `test_3d_beamsize_effect` 与 `test_3d_virtual_photons` 两条 active regression，并共同固定消费同一个 `diags/diag1` openPMD 粒子目录；这组 wiring 当前稳定落成 `1/1` split：一条 beam-size-effect 主链，一条 single-beam virtual-photon yield/spectrum/position 主链，而 helper 只承担 same-directory additive checksum wrapper。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `pierce_diode` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前只服务唯一一条 active baseline `test_1d_pierce_diode`，并且与主 `analysis_pierce_diode.py` 共同固定消费同一个 `diags/diag1/` openPMD 目录，因此更准确地是 same-directory additive checksum wrapper。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `spacecraft_charging` family-level helper 行：已把 `analysis_default_regression.py` 再补一轮并排一致性，明确写清它当前只在 `WarpX_EB` 打开时服务唯一一条 active baseline `test_rz_spacecraft_charging_picmi`，并且与主 `analysis.py` 共同固定消费同一个 `diags/diag1/` openPMD 目录，因此更准确地是 same-directory additive checksum wrapper。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `do_field_ionization` family 行：已把 `<species_name>.physical_element` 再压一轮 family-level 一致性，明确写清它当前不是孤立元素标签，而是 `element dispatch branch`，会把元素字符串一次性分派成 `ion_map_ids -> ion_atomic_numbers / ion_energy_offsets -> ionization_energies + ADK arrays -> m_atomic_number` 这整条链，并同时钉住 `do_adk_correction` 的 Hydrogen-only 边界。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `do_field_ionization` family 根开关行：已把 `<species_name>.do_field_ionization` 再压一轮 family-level 一致性，明确写清它当前不是普通 ADK 布尔，而是 `source-species root gate`：先决定 species 是否进入 `InitMultiPhysicsModules()/PostRestart()` 的 ionization 建表与 product 绑定链，再决定它是否进入固定消费 `Efield_aux/Bfield_aux` 的 per-level runtime event loop，并在 loop 内同时触发 source `ionizationLevel` 原位递增与 product tile 追加。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `resampling` family trigger 行：已把 `<species_name>.resampling_trigger_intervals` 再压一轮 family-level 一致性，明确写清它当前不是孤立时间窗，而是 `ResamplingTrigger` 子系统的 `trigger root branch`：会先 materialize `IntervalsParser`，再与 `resampling_trigger_max_avg_ppc` 共用同一个 OR gate，最后共同决定 `do_resampling` species 何时真正进入 `Redistribute -> algorithm tile kernel -> deleteInvalidParticles` 执行链。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `resampling` family trigger sibling 行：已把 `<species_name>.resampling_trigger_max_avg_ppc` 再压一轮 family-level 一致性，明确写清它当前不是孤立阈值，而是 `ResamplingTrigger` 对象里与 `resampling_trigger_intervals` 并排的 `load-threshold sibling`：会在首次调用时缓存全 AMR `boxArray.numPts()`，再把 `avg_ppc > m_max_avg_ppc` 与时间窗条件做同一个 OR 合并。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `velocity_coincidence_thinning` 子簇 sibling 行：已把 `<species_name>.resampling_algorithm_target_weight` 再压一轮 family-level 一致性，明确写清它当前不是孤立目标权重，而是挂在 `resampling_algorithm_velocity_grid_type` 分箱链之后的 `cluster-cut sibling`：先 materialize 成 `2 * target_weight` 的 cluster 总权重上界，再与 `同 bin延续 / bin切换 / cell尾部` 这组条件一起决定 cluster 截断位置。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `velocity_coincidence_thinning` 子簇 dispatch 行：已把 `<species_name>.resampling_algorithm_velocity_grid_type` 再压一轮 family-level 一致性，明确写清它当前不是普通字符串，而是 `velocity-binning dispatch branch`：先在 `spherical` 与 `cartesian` 两组 companion 间分派，再分别落成固定球坐标编号链或按 tile 速度包围盒即时重建的直角坐标编号链。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `resampling` family shared gate 行：已把 `<species_name>.resampling_min_ppc` 再压一轮 family-level 一致性，明确写清它当前不是某个算法私有阈值，而是 `leveling_thinning` 和 `velocity_coincidence_thinning` 共用的 `per-cell outer gate`：两条算法都在构造期平行读取它，并在各自 tile kernel 顶部用同一条 `cell_numparts < min_ppc` early-return 先裁掉低粒子数 cell。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `resampling` family root 行：已把 `<species_name>.do_resampling` 再压一轮 family-level 一致性，明确写清它当前不是普通“是否重采样”布尔，而是 `family root gate`：先决定 `Resampling` object 是否 materialize，再决定 species 是否进入多物种 resampling step-loop，最后把通过 gate 的 species 交给 trigger object、per-cell outer gate 和算法分支继续细分。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `Quantum Synchrotron` family root 行：已把 `<species_name>.do_qed_quantum_sync` 再压一轮 family-level 一致性，明确写清它当前不是普通 QED 布尔，而是 `family root gate`：先决定 source species 是否挂接 `opticalDepthQSR + photon-product` companion，中间决定 shared QS engine/table 是否初始化，后面再把通过 gate 的 species 接到 optical-depth 演化、事件后重采样与 photon-emission append 主链。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `Breit-Wheeler` family root 行：已把 `<species_name>.do_qed_breit_wheeler` 再压一轮 family-level 一致性，明确写清它当前不是普通 photon-QED 布尔，而是 `family root gate`：先决定 source photon 是否挂接 `opticalDepthBW + electron/positron product` companion，中间决定 shared BW engine/table 是否初始化，后面再把通过 gate 的 source 接到 optical-depth 演化与 `electron + positron` 双容器 pair-creation append 主链。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 classical radiation reaction 行：已把 `<species_name>.do_classical_radiation_reaction` 再压一轮 family-level 一致性，明确写清它当前不是普通 RR 布尔，而是 radiation-reaction 邻接簇的 `family root gate + push dispatch selector`：先把 source-species 与 Boris-only 边界钉死，中间统一控制各条 momentum-update 路径是否进入 `UpdateMomentumBorisWithRadiationReaction(...)`，后面再在与 `Quantum Synchrotron` 联用时受 `t_chi_max` 的高-chi 回退边界约束。
- [x] 2026-05-31：继续清理 `docs/parameter-map.md` 的 `Quantum Synchrotron` table dispatch 行：已把 `qed_qs.lookup_table_mode` 再压一轮 family-level 一致性，明确写清它当前不是普通模式字符串，而是 shared QS engine/table 的 `initialization dispatch branch`：会在 `generate / load / builtin` 三路之间分派，并进一步决定 companion 参数、文件 I/O 和 `IO rank generated / all-rank raw-rebuild / all-rank builtin-init` 三种不同的初始化合同。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `nuclear_fusion` family-level 行：已把这组从“helper + 3 条 analysis + 6 张输入卡”压成真正的 umbrella summary，明确写清它当前已经稳定落成 `6 active baselines + shared additive checksum wrapper + 5/1 checksum-surface split + 2/3/1 shared-analysis split + 2/1/2/1 reaction-family split`；其中 `p-B11` 两支共享三 alpha / Tentori-Belloni 主链，`D-D/D-T` 三支共享两产物守恒与理论 yield 主链，`D-D intraspecies` 则单独走 `reduced_diags/particle_number.txt` reactivity 主链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `initial_plasma_profile` family-level 行：已把这组从“helper + input + baseline”三条零散项压成真正的 umbrella summary，明确写清它当前已经稳定落成 `single active baseline + fields-only final-plotfile checksum-only consumer chain + parser-defined parabolic-channel density producer scaffold`；其中唯一 active regression `test_2d_parabolic_channel_initialization` 只有 `analysis=OFF + analysis_default_regression.py --path diags/diag1000001 --skip-particles --rtol 1e-4` 这条字段侧 checksum 链，而输入卡则完整物化了“横向 parabolic channel + 纵向 cosine up-ramp / plateau / down-ramp”的 parser 密度 scaffold 与单帧 `rho` 输出面。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `ohm_solver_cylinder_compression` baseline 行：已把 `test_3d_ohm_solver_cylinder_compression_picmi.json` 从偏短的 checksum 摘要补成 test-level source-grounded 描述，明确写清这条 active slow regression 当前固定命中 `--test` 低分辨率分支，唯一自动消费者链就是 mixed particle/field `diags/diag1000010 --rtol 5e-4` checksum main surface，而非测试长跑分支里的 `field_diags` openPMD 输出当前不会进入回归链。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `ohm_solver_cylinder_compression` RZ baseline 行：已把 `test_rz_ohm_solver_cylinder_compression_picmi.json` 也补成 test-level source-grounded 描述，明确写清这条 active slow regression 同样固定命中 `--test` 低分辨率分支，当前实际消费的是 `NR=64, NZ=16, total_steps=20, diag_steps=4` 下的 mixed particle/field `diags/diag1000020 --rtol 1e-6` checksum main surface，而非长跑分支里的 `field_diags` openPMD 输出。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `ohm_solver_em_modes` 1D baseline 行：已把 `test_1d_ohm_solver_em_modes_picmi.json` 从偏短的 checksum 摘要补成 dual-surface test-level 描述，明确写清这条 active regression 固定命中 `--test --dim 1 --bdir z` 分支，当前真正的强自动 gate 仍是 `diags/field_diag000250` final plotfile checksum，而 `diags/par_field_data.txt` 只承担 `analysis.py` 的 `B_L(k,omega)` 频谱可视化 side consumer。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `ohm_solver_em_modes` 1D input 行：已把 `inputs_test_1d_ohm_solver_em_modes_picmi.py` 补成 source-grounded runtime scaffold，明确写清这条 active branch 当前固定命中 `--test --dim 1 --bdir z` 参数分派，先落 `sim_parameters.dpkl`，再并行 materialize `par_field_data.txt` 的 reduced spectrogram producer 与末态 `field_diag000250` checksum producer，不再只停在笼统的 1D EM-modes 摘要。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `ohm_solver_em_modes` RZ input 行：已把 `inputs_test_rz_ohm_solver_em_modes_picmi.py` 也补成 source-grounded runtime scaffold，明确写清这条 active branch 当前固定命中 `--test` 分支，先以 `B0/beta/m_ion/vA_over_c/eta/substeps` 常数组装 metallic-cylinder normal-mode 运行，再落 `sim_parameters.dpkl + diags/field_diags` 主频谱 producer，并把 `diag1000100` 保留成独立 particle-only checksum side surface。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `ohm_solver_ion_Landau_damping` helper 行：已把 `analysis_default_regression.py` 补成 family-level service boundary，明确写清它当前只服务唯一一条 active `slow` baseline `test_2d_ohm_solver_landau_damping_picmi`，并且只消费独立的 `diags/diag1000100` final plotfile checksum main surface；相对地，shared `analysis.py` 继续固定回读 `sim_parameters.dpkl + diags/field_data.txt` 生成 reduced damping-curve side consumer。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `inputs_test_3d_diff_lumi_diag_photons`：已把这条残留偏弱的 input 行从一句旧式 `photon + parse_density_function` 摘要补成 source-grounded 强描述，明确写清它当前只是共享 `inputs_base_3d` 上的 photon producer overlay，但前端不走 `gaussian_beam + q_tot`，而是把 `beam1/beam2` 两支都切到 `species_type = photon + injection_style = NUniformPerCell + profile = parse_density_function`，并分别在以 `-muz/+muz` 为中心的 `±4σ_z` 盒内 materialize 两束 Gaussian density bunch；shared consumer 则继续完全绕过 plotfile、只对 `1D dL/dE txt + 2D d^2L/dE_1dE_2 openPMD` 双谱施加更宽的 `2.1% / 6%` 解析对照 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `diff_lumi_diag umbrella summary`：已把这条 residual family glue 从宽泛“shared dual-spectrum main consumer”摘要补成 source-grounded 强描述，明确写清当前 `3` 条 `WarpX_FFT` gated baseline 虽然在 `CMake` 里分成 `2 + 1` 两段注册，但最终都共享同一个 `analysis.py + analysis_default_regression.py --path diags/diag1000080 --rtol 1e-2` tuple，并稳定闭合成 `2/1 producer split + 2/1 tolerance split`，也就是 `leptons / leptons+MR / photons-density-function` 三条 producer 分叉，对齐到 `2%/4%` 与 `2.1%/6%` 两档双谱解析 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_electrostatic_sphere_eb_mixed_bc.json`：已把这条 residual weak baseline 从旧式 `checksum 基线` 口径补成 source-grounded 强描述，明确写清它当前不是 `ChargeOnEB + eb_covered` 主链的 sibling，而是 `electrostatic_sphere_eb` family 里唯一稳定停在 `analysis=OFF + analysis_default_regression.py --path diags/diag1000001` 的 pure checksum-only branch；producer 侧则固定 materialize 半径 `0.3` 的 `1 V` 导体球、`pec pec neumann / pec neumann neumann` 非对称混合边界，以及只包含 `Ex/Ey/Ez/rho/phi` 的单张末态 field surface。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_electrostatic_sphere_eb.json`：已把这条 residual weak baseline 从旧式 `checksum 基线` 口径补成 source-grounded 强描述，明确写清它当前不是 checksum-only，而是 `electrostatic_sphere_eb` family 里 `3D ChargeOnEB + eb_covered` 主链上的 native sibling；producer 侧固定 materialize 半径 `0.1`、电势 `1 V` 的导体球 EB、双 `ChargeOnEB` reduced ledger 与 `eb_covered` geometry surface，而主 consumer 则分别对总电荷、八分体电荷和球内/球外覆盖几何施加理论 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_3d_electrostatic_sphere_eb_picmi.json`：已把这条 residual weak baseline 从旧式 `checksum 基线` 口径补成 source-grounded 强描述，明确写清它当前不是 checksum-only，而是 `electrostatic_sphere_eb` family 里 `3D ChargeOnEB + eb_covered` 主链上的 PICMI sibling；producer 侧除对齐 native 的导体球 EB、双 `ChargeOnEB` reduced ledger 与 `eb_covered` geometry surface 外，还额外把 `sim.step(1) -> set_potential_on_eb("2.") -> sim.step(1)` 这条运行时电势更新入口纳入合同。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_rz_electrostatic_sphere_eb.json`：已把这条 residual weak baseline 从旧式 `checksum 基线` 口径补成 source-grounded 强描述，明确写清它当前不是 checksum-only，而是 `electrostatic_sphere_eb` family 里单层 RZ `analytic phi/Er` 主链，再叠加同一张 `diag1000001` 末态面的 fields-only additive checksum；producer 侧固定 materialize `Er/phi/eb_covered`，而主 consumer 则只对 EB 外域整条 `z` 切片上的解析 `phi/Er` 最大相对误差施加 `4.1e-3` gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_rz_electrostatic_sphere_eb_mr.json`：已把这条 residual weak baseline 从旧式 `checksum 基线` 口径补成 source-grounded 强描述，明确写清它当前不是 checksum-only，而是 `electrostatic_sphere_eb` family 里 RZ+MR `patchwise phi/Er` 主链，再叠加同目录 `diag1/` additive checksum；producer 侧固定 materialize multi-level `Er/phi/eb_covered` surface，而主 consumer 则对每个 level 的真实 MR patch 上解析 `phi/Er` 逐层施加 `4e-3` 最大相对误差 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_rz_electrostatic_sphere.json`：已把这条 residual weak baseline 从旧式 `checksum 基线` 口径补成 source-grounded 强描述，明确写清它当前不是 checksum-only，而是 `electrostatic_sphere` family 里 RZ self-field-expansion 主链，再叠加同一张 `diag1000030` 末态面的 additive checksum；producer 侧固定 materialize 末态 `Er/Et/Ez/rho` 和带 `phi` 的 openPMD 粒子面，而主 consumer 则对末态 `Er/Ez` 轴向解析场 `L2` 与条件触发的粒子能量账本同时施加 gate。
- [x] 2026-05-31：继续清理 `docs/example-regression-map.md` 的 `test_rz_electrostatic_sphere_uniform_weighting.json`：已把这条 residual weak baseline 从旧式 `checksum 基线` 口径补成 source-grounded 强描述，明确写清它当前不是 checksum-only，而是 `electrostatic_sphere` family 里 RZ self-field-expansion 主链上的 `uniform_weighting` sibling；producer 侧把径向装填切到 `6 2 2 + radial_numpercell_power = 1.`，而主 consumer 则继续做末态 `Er/Ez` 轴向解析场 `L2`，并把 phi-gated 能量账本容差放宽到 `1.2%`。

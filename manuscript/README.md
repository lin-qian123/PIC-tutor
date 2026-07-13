# PIC 程序详解：从物理模型到 WarpX 源码

当前 v0.68 合订 PDF 为 320 页；页数、图表资源、关键标记、public path hygiene 和构建警告均由 `scripts/verify_v68_build.py` 验收。第 1-8 章均已补入至少一个可执行的练习、源码定位题或复现实验任务。

2026-07-13：第 4 章新增显式 leapfrog position source crosswalk，核对 momentum-then-position 顺序、时间中心速度公式、维度分支和 Higuera-Cary split-push 边界；直接 half-step attribute 与 Vay Appendix B 专门圆轨道仍保留为后续验证项。

2026-07-13：第 4 章新增 Vay Appendix B 窄化 uniform-B runtime proxy contract；三种 pusher 各 81 帧，离散 phase、速度 proxy、gyroradius proxy 和动量范数 gate 通过，finalize tail 与 physics data contract 分开记录。

v0.68 新增 `../docs/public-evidence-index.{json,md}`，汇总本地 165 条验证合同的原始状态和边界分类。该摘要去除了本机路径；`runs/` 原始产物仍保持排除，摘要不替代逐项 JSON/Markdown 报告。

2026-07-13：第 7 章新增 LeeCPC2015 paper/source/regression crosswalk：accepted manuscript 的 PSTD 与 reflection recurrence、WarpX `PML.cpp`/`PsatdAlgorithmPml.cpp` 的实现表面、以及官方 `<1e-6` reflectivity consumer 均由只读 contract 交叉验收；仍保留 publisher-formatted CPC PDF 和逐系数等价缺失边界。

2026-07-13：RZ JRhom first-stage handoff 已完成目标 WarpX checkout 的只读 audit/report/preview/stage dry-run 验收；目标仍为 `unstaged`，正式 staging 需维护者明确允许。`finite + energy` 的 MPI=2 contract 通过，决策记录见 `notes/code-reading/fieldsolver/36-rz-jrhom-first-stage-decision.md`。

2026-07-13：完成 `TajimaDawson1982` 正式来源访问审计。DOI 与 AIP canonical resource 已确认，但本机访问返回 Cloudflare HTTP `403`，因此第 9 章继续明确 publisher PDF/MinerU 仍未取得，相关 FNAL 单作者 note 不能替代原文。

2026-07-13：新增 Tajima 1982 FNAL 相关会议稿的全文资产合同和中文讲解；第 9 章将其作为 beat-wave / plasma-wave accelerator 的主题旁证，正式 Tajima-Dawson AIP 论文仍单独列为缺失全文。

2026-07-13：收口 Tajima-Dawson 1979 论文资产合同：4 页 PDF、MinerU、11 张图、中文精读和图 1/图 2 机制对应均已复核；该文作为 early LWFA scaling baseline 使用，不替代现代 WarpX runtime evidence。

2026-07-13：第 5 章补入 Esirkepov 2001 CPC 索引摘要级证据：arbitrary form-factor、straight-line trajectory、no-Poisson-solve 和 2D/3D demonstration；发表版 PDF 仍无法取得，不升级为逐行核对。

2026-07-13：第 7 章补入 LeeCPC2015 的 publisher abstract boundary：高阶 solver 到无限阶 pseudo-spectral limit 的摘要事实可引用，但 accepted manuscript 与 publisher-formatted CPC PDF 仍严格分层。

2026-07-13：第 3A 章新增 Birdsall `3A ES1` 到 WarpX `InitData()/Evolve()` 的阶段映射表，连接历史 PIC 最小程序语义与现代 AMR/solver/diagnostics 对象图，同时保留不可等同边界。
2026-07-13：第 4 章新增 Boris 1970 metadata/access boundary：固定 DTIC `ADA023511` 书目身份，记录 PDF 限流和原始全文缺失；算法推导与当前实现分别回链 Birdsall 1985 和 WarpX 源码。
2026-07-13：第 4 章新增 Boris 当前 WarpX source crosswalk：`UpdateMomentumBoris.H` 的 half-push、磁旋转、半角重标定和 `PushSelector.H` 分派由独立脚本逐项核对，仍与 Boris 1970 原始全文保持证据分层。
2026-07-13：第 2/6 章新增 Yee 当前 WarpX FDTD source crosswalk：`CartesianYeeAlgorithm.H`、`FiniteDifferenceSolver.cpp`、`EvolveB.cpp`、`EvolveE.cpp` 的 CFL、交错差分和 solver dispatch 由独立脚本核对，仍保留 IEEE full text 缺失边界。

2026-07-13：完成 `LeeCPC2015` accepted/submitted manuscript contract：7 页全文、13 张抽取图片、MinerU 结构、公式锚点和中文讲解均通过；第 7 章可使用第一轮 paper-backed PML 解释，但不把该资产标记为 CPC publisher-formatted 定稿。

2026-07-13：完成第 5 章 Villasenor/Esirkepov 本地论文资产合同：Villasenor 11 页/27 图、Esirkepov 13 页/39 图均通过结构、公式锚点和中文讲解检查；两条线仍保留各自的 publisher provenance / CPC 定稿差异边界。

2026-07-13：第 6 章新增 Birdsall 13-5 后半段的 `K_4`/QPM/`N_C`/stochastic-heating 回写；数值来自 Birdsall 对 Hockney 的历史转述，未升级为 Hockney-Eastwood 原始图表逐页证据。

2026-07-13：第 8 章新增 Dawson 1983 wave-side diagnostics 主线，将 modal energy、power spectrum、correlation、normal modes 与 quiet-start measurement boundary 组织成连续的 reader-side 合同。

2026-07-13：第 4 章补入 Vay 2008 Appendix A/B 的显式 `\gamma` 求解和 gyroradius 边界，并明确当前 WarpX `particle_pusher` analysis 尚未覆盖 Appendix B 的专门圆轨道复现。

2026-07-13：完成第 4 章 Vay 2008/Higuera-Cary 2017 论文资产合同：分别为 7 页/38 图和 9 页/44 图，包含全文、MinerU、中文讲解、源码映射、access audit 和 runtime boundary；Vay Appendix B 已有 bounded proxy-level uniform-B contract，但直接 half-step attribute 与论文图形逐点复现仍未完成，Higuera Poincare section/invariant consumer 和 sampled topology classifier 已接入但不构成完整 Fig. 2 gate。

2026-07-13：新增 `larmor` 逐帧离散轨道合同：6 个 Full plotfile 的时间、粒子数、有限状态、cadence 和 Boris rotation-angle 参考量均通过独立脚本提取；该增强仍不等价于 Vay Appendix B 或 Higuera-Cary Poincare topology 专门复现。

2026-07-13：新增窄化 uniform-`B` Boris/Vay/Higuera-Cary runtime 对照：三条无 AMR/PML/场演化 sibling 各输出 81 个 Full plotfile；基于 `UpdatePosition.H` 的 position-update velocity/gyroradius proxy 误差分别压到 `1.34e-14/4.8e-15` 以内，支持 Vay Appendix B 条件的 proxy 层证据，但仍不宣称直接 half-step attribute 或 Poincare topology 专门 gate。

2026-07-13：新增 Higuera-Cary Poincare section runtime contract：64³ 专用盒、三种 pusher、5 个初始条件和 1001 帧均通过截面结构检查；最大 `H`/`I_y` 漂移为 `1.532e-3/8.206e-3`。规范动量到 WarpX 机械动量的转换已固化，topology classifier 已实现但当前返回 `INSUFFICIENT_SAMPLING`。

2026-07-13：新增 sampled Poincare topology classifier：已实现候选自交、轨道间线段交叉和面积计算；32³、2201-frame 长轨道达到 18/19 点/轨道，但三种 pusher 候选签名一致，分类结果为 `REVIEW_REQUIRED`，不宣称论文 topology gate 通过。

2026-07-13：Poincare 分类器的 invariant-order gate 已通过：三种 pusher 的 `I_y` 区间均保持 `p05 < p10 < p17 < p22 < p27` 且互不重叠；该结果只支持 invariant ordering，不等价于完整 resonance-island topology reproduction。

2026-07-13：Poincare 分类器又加入 Section VI 的解析 quartic reference gate；全部长轨道残差低于 `1e-2`，最差为 Vay `p22=7.52e-3`，但完整 topology gate 仍保持关闭。

2026-07-13：补入 14-species dense family 和 64³ `p_y=1.6/1.8` resolution control：Vay 的 `I_y` 漂移约 `6.5e-2`，Boris/Higuera-Cary 约 `1e-3`，形成 resonance-sensitive invariant screen；该 screen 不等价于完整 two-fold island reproduction。

本轮又把第 7 章 transition-zone route-count packet 落成可执行的 schema validator 和 synthetic fixture：正例检查 route count、weight closure、`rho/J` 中间账本与显式 merge gates，负例会被拒绝；当前 WarpX 尚未接入 runtime hook，因此仍保持 `RUNTIME_LEDGER_UNPROVEN`。

本轮又补入 Hockney 1971 的摘要级 article asset：8 项本地 contract 全部通过，正文只使用摘要支持的 collision/heating scaling、optimum path 和 `K_2` 关系，继续明确 publisher full text、PDF、MinerU 和逐段核对尚未完成。

本轮又补入两篇 1974 particle-mesh 摘要级 asset：QPM/PPPM 和 force-shaping 双论文 contract 各 8 项检查通过，正文新增 Gaussian cloud、potential shaping、sub-mesh resolution 与 force anisotropy 的有限证据层说明；两篇 publisher full text 仍未 materialize。

本轮又补入 Yee 1966 indexed-abstract asset：9 项本地 contract 全部通过，正文只使用 finite-difference Maxwell、field-point placement、PEC boundary 和 conducting-cylinder example 的窄证据，继续明确 IEEE full text、PDF、MinerU 和逐式核对尚未完成。

本轮又把 Godfrey 2014、Lehe 2016、Kirchen 2016 三条 PSATD/NCI 全文证据线收成 strategy matrix contract，统一索引论文机制、WarpX 源码关键词和 runtime consumer，并保留三者不能互相替代的边界。

本轮还修复并持续验收了 release 产物的本机路径泄露与迁移问题：v0.68 的 Markdown/HTML 使用仓库相对链接，WarpX 外部命令使用 `$WARPX_ROOT` 占位符，并由 path-hygiene contract 覆盖。

2026-07-12 又完成 3D Esirkepov shape=2/3/4 的 `64^3 -> 128^3` case-local resolution contrast：三档 refined field/charge 均通过，正文明确这只是分辨率敏感性证据，不是正式收敛阶。

2026-07-12 又补入 3D Esirkepov shape=2/3/4 runtime matrix：shape=2 双 gate 通过，shape=3/4 只在 charge 层通过，field 层保留分辨率边界。

2026-07-12 又补入 deposition geometry/order coverage matrix：把已验证组合和明确缺口并排写入第 5 章，防止把局部 shape/geometry contract 误读成完整 Cartesian product 覆盖。

2026-07-12 又补入 Esirkepov paper-to-WarpX notation matrix：14 个当前源码锚点全部通过，正文明确 `W^1/W^2/W^3`、`sdxi/sdyj/sdzk` 和 `Jx/Jy/Jz` 的层级对应，并保留 publisher-formatted PDF 未取得的边界。

2026-07-12 又补入 3D AMR particles-in-PML 的逐分量 signed/absolute/level decomposition：初始帧全零，末态只有负向 `Ex` 峰值越过 `110`，且 coarse/fine 读取一致；正文继续把它写成官方 gate 通过、严格 absolute gate 失败的判据边界。

2026-07-12 又统一收口 RZ secondary-emission 的分辨率证据：`64x64` 默认基线仍为 `3.6038% > 2%` 的 geometry boundary，`128x128` 与 `256x256` refined controls 分别为 `0.9977%` 与 `0.6646%` 并通过官方 gate；正文不修改默认输入，不放宽 tolerance，也不把 refined sibling 外推成 upstream baseline 已修复。

2026-07-12 又完成 RZ Esirkepov rho-side observable：shape=2/3/4 高分辨率 correction-on 的最终 `rho` 与 `rho_electrons+rho_ions` 相对差约为 `1e-14`，integrated-rho drift 作为时间序列记录；正文明确这只关闭物种分解层，不关闭 `divE-rho`、current closure 或完整 Gauss-law 证据。

2026-07-12 又完成 RZ Esirkepov shape=2/3/4 correction-on/off 完整矩阵：refined field gate 全部通过，correction-off charge gate 全部通过，correction-on charge residual 仍由 axis cell 主导并保持在 `O(1e-3)`，正文继续保留这一未闭合边界。

2026-07-12 又完成 shape=2/3/4 correction-off 的 RZ resolution family：三档 coarse `Er` field gate 均失败，三档 refined `128x256` field/charge 双 gate 均通过；本版将其写成高阶 shape 的 resolution-sensitive boundary，不外推为全局默认修复。

2026-07-12 又完成 RZ Esirkepov shape=2 粗/细网格 paired runtime：correction-off 的 `Er` field error 从 `0.1323` 降至 `0.0093`，高分辨率 field/charge 双 gate 通过；correction-on 仍保留 axis charge residual，不将该结果写成全局默认修复。

2026-07-12 又完成 RZ Esirkepov `particle_shape=1` 的轴修正/分辨率四格对照：默认 correction-on 的 axis residual 随 `64x128 -> 128x256` 下降约 `2.36x`，correction-off 两档 field/charge 双 gate 均通过；shape=2/3/4 的 correction-off field 边界仍单独保留，不把这一结果写成全局参数修复。
2026-07-12 又完成 RZ shape=1 `256x512` resolution control：correction-on axis charge residual 为 `3.593e-3 -> 1.520e-3 -> 7.554e-4`，correction-off 为 `5.513e-12 -> 9.353e-12 -> 1.639e-11`；该三档结果保留 correction-on 趋势与 correction-off 非单调 boundary 的分层结论。
2026-07-12 又完成 RZ correction-on `256x512` shape=1/2/3/4 high-resolution family：field gate 全通过，charge residual 为 `7.554e-4/8.990e-4/9.289e-4/9.729e-4`，均由 axis cell 主导并保留 BOUNDARY。
2026-07-12 又完成 RZ `256x512` correction-on/off shape=1/2/3/4 双侧 family：field gate 8/8 全通过；correction-on charge 全为 BOUNDARY，correction-off shape=3/4 通过 `1e-11`，shape=1/2 分别为 `1.639e-11/1.020e-11`，保留为 charge/field tradeoff。

2026-07-12 又完成 `particles_in_pml` signed-vs-absolute analysis source audit：上游 consumer 使用有符号 component max，项目独立 contract 使用全场绝对值 max；3D AMR sibling 的官方 gate 通过而强化 gate 失败，因此正文只保留为判据边界，不把它升级为 AMR 强验证。

2026-07-12 又完成 RZ JRhom first-stage handoff asset 的可重复重建：从 MPI=2 reference ledger 重建 bundle，并对目标 WarpX 做 audit/report/preview/dry-run；baseline helper 通过、`ll2-no-timeavg-cleaning` 负对照拒绝，目标 checkout 仍保持 `unstaged`，未修改 `../warpx`。

2026-07-12 又完成 comoving PSATD first-stage handoff asset 的可重复重建：stable helper 通过、no-comoving reference 被 spike gate 拒绝，独立 contract 通过；目标 checkout 仍为 `unstaged`，energy gate 保持关闭，未修改 `../warpx`。

2026-07-12 又补做 RZ Galilean current-correction paired runtime：非 PSB 2-rank charge gate 略超阈值，PSB single-box single-rank 通过严格 charge gate；独立报告保留两者的 `CHARGE_BOUNDARY/PASS` 分层。

2026-07-12 又补做 RZ Langmuir PSATD current-correction sibling：官方 `analysis_rz.py` 与独立 contract 均通过，解析场和同面 charge-conservation 证据已归档。

2026-07-12 又补做 RZ Langmuir PSATD-JRhom `CL4` 2-rank sibling：官方与独立解析场 contract 均通过，因 `current_correction=0` 保留 charge gate 不适用的边界。

2026-07-12 又补做标准 RZ Langmuir PSATD 2-rank sibling：官方与独立解析场 contract 均通过，RZ Langmuir standard / current-correction / JRhom `CL4` 三条对照已形成。

2026-07-12 又完成 RZ PSATD-PML 官方 2-rank 复现与独立 residual-field contract：`max|Er|=1.0316`、`max|Ez|=0.5695`，均低于 `2.0`；此前 1-rank 结果保留为历史对照。

2026-07-12 又新增 RZ secondary-emission EB source contract：10/10 锚点通过，callback wiring 已闭合；64×64 几何 gate 仍保持失败，不把 source audit 写成 runtime pass。

2026-07-12 又新增 RZ Langmuir PSATD family matrix：standard/current-correction/JRhom `CL4` 三条对照的 field gate 全部通过，并明确 charge gate 只适用于 current-correction sibling。

2026-07-12 又完成 `test_2d_subcycling_mr` 2-rank producer 与独立完整性 contract：两层 AMR、moving-window 几何和最终 species 输出均通过；本版仍明确不把它升级为 transition-zone route-count 或守恒强验证。

2026-07-12 又完成 Cartesian 1D Silver-Mueller sibling：官方与独立 contract 均通过，`Ex/Ey/Ez` 最大绝对值为 `3.887e-8/3.887e-8/0 V/m`；至此 1D、2D x/z 与 RZ 的短时残余场路径均已覆盖。

2026-07-12 又完成 Cartesian 2D Silver-Mueller z sibling：官方与独立 contract 均通过，三分量最大绝对值为 `3.912e-3/3.516e-3/9.149e-4 V/m`，与 x 向 case 呈分量置换对称；两者仍限定为短时残余场合同。

2026-07-12 又完成 Cartesian 2D Silver-Mueller x sibling：官方与独立 contract 均通过，三分量最大绝对值为 `9.149e-4/3.516e-3/3.912e-3 V/m`，最大值低于 `0.01 V/m`；本版与 RZ 结果分开记录，不把残余场 gate 写成长期反射率扫描。

2026-07-12 又补入 3D PSATD-PML cleaning 的源码-诊断语义审计：明确 `divE` 的 spectral 计算、`divB` 的 cell-centered finite-difference 计算及 PML `F/G` 未输出的边界；clean/control 结果继续只作为对照证据。

2026-07-12 又补入 3D PSATD-PML cleaning 的源码-诊断语义审计：明确 `divE` 的 spectral 计算、`divB` 的 cell-centered finite-difference 计算及 PML `F/G` 未输出的边界；clean/control 结果继续只作为对照证据。

2026-07-12 又完成 `test_2d_pec_field_insulator` 显式 2-rank producer 与 boundary-drive contract：初态场全零，末态上边界中段 `By` 对 `3.3e-3` 输入的相对误差为 `1.54%`，下边界为零；该证据与 implicit energy/Poynting ledger 保持分层。

2026-07-12 又完成 `test_3d_pec_particle` 的 PEC-vs-periodic 2-rank 对照：全场最大电场比值 `0.0070491`、`Ey` 比值 `0.0022796` 均低于 `0.01`，两 species 末态粒子状态一致；本版将其写成边界场抑制合同，不升级为直接 gather kernel 证明。

2026-07-12 又完成 `test_2d_particles_in_pml_mr` 2-rank、300 步复现：官方与独立绝对值 contract 均通过，末态 `max|E|=3.661057413095795e-4 < 6e-4`；至此 2D 单层/AMR 与 3D 单层均有正向证据，3D AMR 判据分歧仍单独保留。

2026-07-12 又完成 `particles_in_pml` 的 3D 单层与 AMR sibling 复现：3D 单层官方/独立 contract 通过，`max|E|=4.325973103094924 < 10`；AMR 官方有符号 gate 通过，但独立绝对值 gate 以 `110.3993781372607 > 110` 拒绝，因此本版保留 AMR 判据分歧，不把它写成强验证通过。

2026-07-12 又完成官方 `test_2d_particles_in_pml` 2-rank、180 步复现：官方 analysis 与独立 reader-side contract 均通过，末态全场 `max|E|=2.5542538436684726e-4 < 3e-4`；2D AMR、3D 单层已补齐，3D AMR 的 signed-vs-absolute 判据分歧与 upstream checksum 边界仍保留。

2026-07-12 又完成 RZ 三模态 sibling 验证：`m=1/2` 的 `Er/Ez` 实虚诊断分量均非零，native theta=0 场与实模态重建的最大相对误差约 `3.05e-16`；该证据属于项目级 case-local multimode writeback contract，官方 native 单模 analysis 不被改写为多模态判据。

2026-07-12 又补强第 2 章非标准时间推进合同：把标准显式、PSATD-JRhom 与 implicit `RHS`/非线性迭代的 source/time-layer 边界接回 `WarpX::OneStep()` 分派和对应源码入口。

2026-07-12 又补强第 3 章 WarpX 主演化路径：新增 implicit `OneStep()`、`ComputeRHS()`、`PreRHSOp()` 与 `SyncCurrentAndRho()` 的调用链，明确 nonlinear iteration、mass-matrix/JFNK 和物理时间步的边界。

2026-07-12 又完成官方 `particle_pusher` Higuera-Cary 单进程复现：10000 步末态 `max|x| = 1.1430664e-4 < 1e-3`，并将项目级 JSON/Markdown 合同报告接回第 4 章；书稿保留其单粒子、恒定外场和 force-free 的证据边界。

2026-07-12 又完成官方 `single_particle` velocity synchronization 单进程复现：第 5 个诊断步的 `u_z` 相对误差为 `1.3237889e-16 < 1e-15`，并将 diagnostics time-level 合同报告接回第 4 章。

2026-07-12 又完成统一 force-free pusher sibling 对照：Boris 明显失败，Vay/Higuera-Cary 通过同一 `1e-3` cancellation gate；书稿保留其 pusher-only override 的项目级证据边界。

2026-07-12 又完成官方 `photon_pusher` 单进程复现：16 个 photon species 的位置/动量最大相对误差分别为 `6.0986372e-16` 和 `1.7217530e-16`，并将无质量粒子路径的合同报告接回第 4 章。

2026-07-12 又运行官方 `larmor` 单进程 case 并完成 continuum orbit audit：修正 2D XZ 面内动量读取为 `particle_momentum_x/z` 后，轨迹相对位移误差 `1.28285096e-2`、动量相对误差 `9.69641193e-2`；书稿保留 checksum-only 边界，并明确该结果不能直接作为强解析 gate。

2026-07-12 又完成官方 `test_1d_theta_implicit_picard` 单进程复现：101 个 reduced-energy 样本最大总能量相对漂移为 `3.4784001e-15 < 1e-14`，并将 implicit total-energy 合同报告接回第 6 章。

2026-07-12 又补强第 3 章 implicit nonlinear/JFNK/mass-matrix 线，新增 `picard/newton/petsc_snes` 分派、`CumulateJ()`/`ComputeJfromMassMatrices()` 的 `J` 构造合同及网格 staggering/geometry 限制。

2026-07-12 又补强第 2 章 AMR subcycling 时间合同：基于 `OneStep_sub1()` 写清两级/比例 2 限制、细层两次推进、粗层一次推进、fine-to-coarse current/rho 合成、guard/auxiliary 可见性和 electrostatic 禁止组合。

2026-07-12 又补强第 1 章的连续模型到 PIC 离散变量桥，新增 `f/rho/J/E/B` 与粒子时间层、网格场、`rho_fp/rho_buf`、`current_fp/current_buf` 和 `SyncCurrentAndRho()` 的映射表，明确 charge deposition、current deposition 与 source synchronization 的职责边界；同时对 Villasenor-Buneman 1992 完成四边界、七/十边界重复分段和三维交叉项的公式级审计，并回填第 5 章；本轮再补齐第 2、3、3A 章读者侧流程图。

2026-07-12 又将第 8 章现有运行证据整理成统一验证矩阵，读者可以按 case 直接定位 producer/MPI、项目级 analysis 脚本、gate 和 JSON/Markdown 产物，并区分 physics gate、writer contract、性能 gate 与未完成复现边界。

2026-07-12 又完成 v0.40 的 PDF 构建链：在 Pandoc + XeLaTeX + CJK 字体可用时，`scripts/build_v40.py` 同时生成 Markdown、HTML 和 PDF；该条记录对应当时的 279 页历史构建快照，并已修正自动章节编号与书稿手写编号叠加的问题。HTML 使用嵌入式 MathJax，便于离线审阅；当前 Pandoc 数学转换与 XeLaTeX 缺字警告均已清零，最新页数以 `scripts/verify_v40_build.py` 为准。

2026-07-12 又补齐完整 `initial_distribution` 官方输入：使用与当前 `../warpx` checkout 同步重建的 3D binary，10 类初始化分布的官方 `analysis.py` 全部通过，最大误差 `1.8931e-2 < 0.02`；checksum 仅在明确记录的随机采样 `rtol=5e-3` 下通过，不宣称默认 `1e-9` 确定性相等。报告位于 `runs/stage-c-validation/initial_distribution_full_current/`。

2026-07-12 又完成 laser-ion application 的 `ParticleHistogram2D` 2-rank writer 对照：官方 time-average analysis 通过，ions/electrons 两个 `uz-z` histogram 都产生 `1000x1000` 的 BP5 openPMD series，`.txt` 文件保持为空符合专用 writer 设计。

2026-07-12 又补入 `ParticleHistogram2D` reader-side weighted-moment sanity：从 BP5 iteration 0/100 重建 ions/electrons 的 `z/uz` 加权均值、标准差、总权重和非零 bin；该结果用于确认物理量可读性，不替代更高分辨率或更高粒子数的 convergence study。

2026-07-12 又完成 `ParticleHistogram2D` 匹配物理时间的网格敏感性对照：`384x512` baseline 与 `768x1024` refined producer 的 `std(z)`/`std(uz)` 局部稳定性 gate 通过；`1x1` particles-per-cell 负对照被拒绝，粒子数统计收敛仍保持为未完成边界。

2026-07-12 又将 `ParticleHistogram2D` 粒子数敏感性扩展为 `1x1/2x2/4x4` pairwise 序列：`1x1 -> 2x2` 电子总权重 gate 失败，`2x2 -> 4x4` 通过局部稳定性 gate；该趋势支持增加粒子数改善 reader-side 统计稳定性，但不等于正式收敛阶。
2026-07-12 又补做 `8x8` particles-per-cell sibling：`4x4 -> 8x8` 电子总权重差降至 `3.6534e-4`，四档相邻比较的总权重、`std(z)`、`std(uz)` 局部 gate 均通过；该结果加强趋势证据，但仍不等于正式收敛阶或 upstream regression gate。
2026-07-12 又重新完成 comoving PSATD 第一阶段目标 checkout 只读 preflight：audit/report/preview/dry-run 均成功，目标树仍为 `unstaged`，helper 缺失、CMake analysis 仍为 `OFF`，本轮未修改 `../warpx`；证据归档于 `notes/code-reading/fieldsolver/34-comoving-target-checkout-preflight.md`。

2026-07-12 又为第 5 章补入 Villasenor-Buneman 可执行公式级 bounded check：10000 组确定性样本验证四边界 flux、repeated crossing segmentation 和 Eq.(36) 三维交叉项/体积闭合，二维最大残差 `4.4409e-16`、三维最大残差 `1.7764e-15`；该检查仍只覆盖论文公式/几何层。

2026-07-12 又重新核查 Esirkepov 2001 CPC 的 publisher access：Elsevier API 元数据可得并标记 `openaccess=0`，PDF 请求仍为未授权的 `406`；正文继续严格区分预印本证据和 publisher-PDF compare。

2026-07-12 又补做 3D PSATD-PML divergence-cleaning 对照：原生 `divE/divB` diagnostics 已接入项目级 reader-side audit，但 clean/control 的 `divB` 没有单调改善，因此本版明确保留为边界证据而非强 physics gate。

2026-07-12 又完成官方 3D PSATD-PML 2-rank launcher 复现：两个 MPI processes 成功写出 native diagnostics；1-rank/2-rank 的 `rho` 几乎一致，但 E/B/divE 存在可见数值差异，因此只记录并行 producer coverage，不写成 rank-invariant contract。

2026-07-12 又在同一 2-rank 分解上完成 PML cleaning/control 对照：`divE` 指标改善但 `divB` 未改善，和单进程观察一致；该结果继续作为边界证据而非强 physics gate。

2026-07-12 又完成官方 2D Cartesian PSATD-PML 2-rank 复现：初始能量与低反射率 gate 均通过，独立 reader-side 报告已归档；本版仍区分本地复现与上游 CMake checksum。

2026-07-12 又完成官方 2D Cartesian PSATD-PML 2-rank restart 复现：从 `chk000150` 接续到 `diag1000300`，官方与独立 reader-side 对八个 field 的最大绝对/相对误差均为 `0.0`，通过 `1e-12` restart gate；本版明确将其归类为状态恢复一致性，而不是新的吸收率判据。

2026-07-12 又完成 `diff_lumi_diag` 官方 2-rank 三组解析谱对照：leptons、leptons+AMR 和 photons 的 1D/2D differential luminosity gates 全部通过，项目报告记录了各自误差、容差、最终 step 和 2D openPMD 形状。

2026-07-12 又完成 `collider_relevant_diags` 官方 2-rank 对照：官方 analysis 通过，`ColliderRelevant` 与 `ParticleExtrema` 输出契约成立，并从 openPMD 两束电荷密度独立重建 `dL/dt`，与 reduced 输出的最大相对误差为 `0`。

2026-07-12 又完成 `LoadBalanceCosts` 的 Heuristic/Timers 2-rank 对照：两条性能诊断链都观察到 load-balance 后效率提升，分别为 `0.625252 -> 1.000000` 和 `0.744780 -> 0.996162`。

2026-07-12 又完成 `reduced_diags` 3D 官方 2-rank 全量对照：60 个 reduced observable 与同一末态 plotfile 的重算结果全部通过，非 field-energy 最大误差为 `4.125e-13`，field-energy 使用官方专用 `0.3` 容差并以 `2.483e-1` 通过。

2026-07-12 又完成 FieldProbe 的 coarse/refined resolution 对照：`lambda/16` 在 step 500 的官方口径误差为 `3.6703%`，`lambda/32` 在相同物理时间的 step 1000 降至 `0.3533%` 并通过 gate；因此原始失败应保留为 coarse-grid 限制，而不是 MPI 或 writer 失败。

2026-07-12 又完成 `field_probe` 单缝衍射的 1-rank/2-rank 真实运行审计；两种配置的 FieldProbe 输出一致，但当前 checkout 的官方解析误差为 `3.6703%`，未通过 `2.5%` gate，因此书稿把它作为“输出链已接通、物理 gate 未通过”的反例证据。

2026-07-12 的最新验证增量是 `uniform_plasma` 3D checkpoint/restart：本轮按官方 2-rank 配置从 `chk000006` 接续到第 10 步，官方 analysis 与独立 reader-side 对照均通过，37 个 field 的最大相对误差为 `2.8631e-16 < 1e-12`；仓库 checksum 的 rank-specific 参考与本地 2-rank producer 最大相对差为 `3.20e-2`，因此仍明确区分 restart field reproducibility 与 checksum contract。本轮又完成 native external-file Gaussian beam 的 1-rank producer 和独立束斑物理分析，保留官方 `analysis.py` 缺失的 upstream 边界，并完成 RZ electrostatic sphere 的官方场/能量与独立 rho-volume charge closure。

同日又用同一当前 binary/input 做了 `uniform_plasma` 1-rank/2-rank consistency 对照：粒子总权重一致，但 field/particle/total energy 相对差分别为 `1.9379e-2/8.9170e-4/6.2269e-4`，physical-field 最大 L2 相对差为 `1.0185`；该 case 不支持 rank-invariant field contract，书稿只保留 2-rank restart 的逐字段 reproducibility 结论。

同日又将 Esirkepov `Eq.(23)` density-decomposition formula check 归档为 JSON/Markdown contract：固定 seed `2001`、10000 组样本的最大残差为 `8.8818e-16 <= 2e-15`，证据仍限定在论文代数层，不替代 WarpX kernel 或端到端 regression。

同日又对当前 `../warpx` checkout 做 Esirkepov source audit：`CurrentDeposition.H` 的 14 个关键 skeleton 锚点全部通过，报告归档于 `runs/stage-c-validation/esirkepov-source-contract/`；随后完成 1D/2D/3D Langmuir Esirkepov runtime siblings，并把 2D 扩展到当前支持的 shape=1/2/3/4，官方 analysis 与独立 contract 均通过；shape=0 在 `WarpX.cpp:1450` 初始化断言处拒绝，shape=4 明确使用官方 `particle_shape_4` 阈值分支。另补做 2D MR overlay，理论场通过但逐层 charge residual 为 `0.8828/1.2005`，保留为 AMR `BOUNDARY`。2D 仍是 `direct -> esirkepov` overlay，不写成上游注册回归。
同日又对当前 `../warpx` checkout 做 Esirkepov AMR route/source-sync audit：新增脚本检查 15 个 `current_fp/current_buf`、coarse `depos_lev`、buffer mask、`SyncCurrent` 和 fine-to-coarse merge 锚点全部通过；该证据只证明源码骨架存在，不把 MR runtime 的中间场/route-count 缺口写成已闭合。
同日又完成 Python MR intermediate-field observability audit：7 个 `MultiFabRegister`/PICMI/current-buffer 锚点全部通过，但现有 Python regression 只验证 `current_fp`，因此把当前状态固定为 `INTERFACE_PRESENT_RUNTIME_LEDGER_UNPROVEN`；`current_buf/rho_buf` 的 MR runtime ledger 仍需 dedicated diagnostic/API wiring。
同日又新增 transition-zone route-count implementation packet，固定 `PartitionParticlesInBuffers()`、`PhysicalParticleContainer::Evolve()`、`SyncCurrent/SyncRho` 的插入点，以及 route/weight/source/owner-mask 的最小 reduced schema；该 packet 仍是未写入 WarpX 的接续设计。
同日又为第 5 章 charge deposition bridge 增加 13-anchor current-checkout source contract，覆盖 `icomp/time_shift_delta`、ABLASTR guard/CPU-GPU 暂存、shape dispatch、RZ mode 和 atomic writeback；该证据归档于 `runs/stage-c-validation/charge-deposition-bridge-source/contract.{json,md}`。
同日又完成第 5 章 deposition geometry/order source contract：charge ordinary/shared、Direct、Esirkepov、Villasenor、Vay 与 implicit 分派的 shape=1/2/3/4 入口，以及 1D_Z、XZ、RZ、RCYLINDER、RSPHERE、3D 几何锚点共 53 项通过；该证据只关闭源码映射，不替代全组合 runtime regression，报告归档于 `runs/stage-c-validation/deposition-geometry-order-source/contract.{json,md}`。
同日又补做官方 RCYLINDER/RSPHERE Esirkepov Langmuir 2-rank siblings，并用独立径向 `Er` contract 复核：相对误差分别为 `2.174e-2` 和 `5.405e-3`，均低于 `0.12`；该证据只覆盖径向场，不升级为完整 charge/Gauss-law 或全 shape/order 验证。
同日又将 RCYLINDER/RSPHERE 的 Esirkepov radial `Er` runtime coverage 扩展到 shape=1/2/3/4，8 个 geometry×shape contract 全部通过；charge/Gauss-law 仍不由此推断。
同日又补做 RCYLINDER/RSPHERE shape=1 的 `rho/divE` 对照：关闭 axis correction 后 RCYLINDER charge gate 通过，RSPHERE residual 显著下降但仍保留为边界。
同日又完成 RSPHERE 64/128/256 resolution 与 axis correction paired control；field 全通过，correction-on charge residual 为 `4.166e-2/1.390e-2/4.142e-3`，correction-off 为 `2.420e-11/9.843e-11/7.461e-11`，仍保持为 resolution-sensitive BOUNDARY，不宣称收敛阶。
同日又统一收口 RCYLINDER/RSPHERE shape=1/2/3/4 的径向 `rho/divE` charge observation：八条 field gate 全通过，RCYLINDER charge residual 为 `4.711e-3/7.442e-3/7.883e-3/8.337e-3`，RSPHERE 为 `4.166e-2/6.269e-2/6.928e-2/8.003e-2`，均保留为 charge BOUNDARY。
同日又完成 radial axis-volume correction source contract：10 个参数、体积因子、缩放定义和调用时机锚点全部通过，作为 RCYLINDER/RSPHERE runtime 边界的源码依据。
同日又复核 Esirkepov CPC 定稿的替代访问路径：元数据可核实，但 publisher-formatted PDF 仍不可取得，因此第 5 章继续保持 preprint-backed、publisher-PDF compare 未完成的边界。
同日又补做官方 RZ Esirkepov Langmuir 2-rank producer：独立 `Er/Ez` field contract 通过，但同面 `divE-rho/epsilon0` 残差为 `3.593e-3`，高于 `1e-11` 强守恒 gate，因此当前分类为 field PASS、charge BOUNDARY。
同日又完成该 RZ charge boundary 的源码语义追踪：官方 analysis 的 RZ 排除条件、`ComputeDivE`/`DivEFunctor`/`RhoFunctor`/`FullDiagnostics` 分叉已记录到 `notes/code-reading/particles/46-rz-esirkepov-charge-boundary.md`，当前 residual 不被错误归因成单一 kernel 失败。
同日又以 `scripts/audit_rz_charge_diagnostic_contract.py` 固定这条证据链的 11 个源码锚点，报告归档于 `runs/stage-c-validation/rz-esirkepov-charge-diagnostic-source/contract.{json,md}`。
同日又完成 `do_dive_cleaning=1/0` paired control：全局 charge residual 比值约 `26.98`，且最大值由 axis cell 主导，因此将 RZ 边界细化为 `AXIS_DOMINATED_CLEANING_SENSITIVE_DIAGNOSTIC_BOUNDARY`，仍不升级为强守恒结论。
同日又完成 `boundary.verboncoeur_axis_correction=true/false` 对照：关闭 correction 后 charge residual 恢复至 `5.513e-12`，通过 `1e-11` gate；该结果只作为 case-local evidence，不修改 WarpX 全局默认值。
同日又将 RZ Esirkepov Langmuir 默认轴修正的 runtime shape coverage 扩展到 shape=1/2/3/4；四阶 field gate 全部通过，但 charge 仍统一保留为 axis-dominated BOUNDARY。
同日又完成 axis-correction-off 的 shape=2/3/4 交叉对照：charge gate 恢复但 field gate 失败，当前明确记录为 shape-dependent charge/field tradeoff。

同日又对 Villasenor crossing-driven source skeleton 做只读 audit：当前 `CurrentDeposition.H` 的 16 个 crossing、segment、fraction 和 `this_J*` writeback 锚点全部通过，报告归档于 `runs/stage-c-validation/villasenor-source-contract/`；该证据只说明源码结构与正文映射仍成立，不替代数值 kernel regression。

这是 `PIC-tutor` 的 Markdown-first 书稿。当前收束版本是 `v0.68` 3D Esirkepov refined-resolution、RZ correction tradeoff audit、bounded compare、Hockney particle-mesh、Yee indexed-abstract、PSATD/NCI strategy matrix 和公开验证证据摘要版；它在 v0.65 的基础上把三篇 PSATD/NCI 全文论文与 WarpX 源码/runtime consumer 的关系固化到第 6 章，并继续保留 RZ charge、AMR route-count、publisher PDF 逐页对照和更多出版级图表等明确边界。当前已嵌入 16 张真实验证图，其中新增 Villasenor 公式合同图、geometry/order coverage 图、transition-zone route-count 设计图和 RZ correction tradeoff 图；WarpX 目标 checkout staging 与 dedicated route-count regression 仍未完成。

## 版本边界

- WarpX 路径：`../warpx`
- WarpX 分支：`pkuHEDPbranch`
- 当前 WarpX commit：`8c488b1a9`
- 第 2、3、3A、4、5、6 章已按当前 checkout 重新核对核心源码行号；第 5 章目前已在 v0.38 把 `DepositCurrent()` 分派、`ShapeFactors.H` indexing/alignment、Direct/Esirkepov/Villasenor/Vay kernel 结构、`DepositCharge()` bridge contract、`SyncCurrentAndRho()` source synchronization 与 `PEC` source-boundary 收口推进成源码主文闭环，在 v0.39 把 `Esirkepov 2001` 与 `Villasenor-Buneman 1992` 两条 charge-conserving 主线都推进到项目内 paper-backed 资产状态，并在 v0.40 进一步把 `current_fp_vay` 专用路径、`Langmuir + current_correction` / `vay_deposition` regression 分工、`Esirkepov/Villasenor` 公式到 kernel 的关键 runtime mapping，以及 `DepositCharge()` / ABLASTR / `ChargeDeposition.H` 的普通/共享内存、时间层、低维几何、coarse-buffer 和外层同步职责边界都压回主文；现阶段第 5 章的主要剩余缺口已经收缩为 `Esirkepov 2001` 的 2001 CPC 定稿 PDF 对照、图表化与 publication-grade 精修。第 6 章已在 v0.17-v0.36 连续收口 PSATD/Galilean/NCI/comoving/RZ 验证边界：除 Lehe/Kirchen/Godfrey 文献闭环、Cartesian/RZ/JRhom 系数图谱外，目前还已具备 comoving first-stage handoff/staging 工具链，以及 RZ JRhom LL2 的 repeated/MPI ledger、helper 原型、handoff bundle 和 target-checkout workflow；第 7 章已完成 v0.12 AMR coarse-fine 图形化证据正文、v0.13 HTML 排版收口、v0.14 transition-zone validation 检查清单、v0.15 dedicated transition-zone 测试草案、v0.16 regression patch 计划、v0.21 PSATD PML 源码/公式/regression 边界、v0.22 Berenger/APML 和 `C1-C25` 系数分层、v0.23 LeeCPC2015 获取审计、v0.24 Cartesian PSATD PML 系数图谱，并在 v0.25 补入 LeeCPC2015 论文-源码公式核对清单；后续仍需真正实现 route-count reduced diagnostic 与 regression。
- 本书稿不修改 WarpX 原仓库。
- 本版优先覆盖显式电磁 PIC 主线：Vlasov-Maxwell、宏粒子、gather-push-deposit-field solve、WarpX 主循环、粒子推进、沉积、场求解、边界/AMR、诊断和案例。

## 目录

1. [写作说明](chapters/00-preface.md)
2. [动理学模型与 PIC 的基本思想](chapters/01-kinetic-models.md)
3. [PIC 总循环](chapters/02-pic-loop.md)
4. [WarpX 主演化路径](chapters/03-warpx-evolve.md)
5. [WarpX 初始化链](chapters/03a-warpx-initialization.md)
6. [粒子推进器](chapters/04-particle-pushers.md)
7. [电荷、电流沉积与形函数](chapters/05-deposition-shapes.md)
8. [电磁场求解器](chapters/06-field-solvers.md)
9. [边界条件、PML 与 AMR](chapters/07-boundaries-amr.md)
10. [诊断、验证与案例](chapters/08-diagnostics-cases.md)
11. [文献路线与后续扩写计划](chapters/09-literature-roadmap.md)

## 证据文件

- 源码映射：`../docs/source-map.md`
- 章节模板：`../docs/chapter-template.md`
- 文献库：`../bibliography/warpx-refs.bib`
- PDF 文献索引：`../references/00_index/current_inventory.md`

## v0.41 构建

详见 [VERSION.md](VERSION.md)。生成合订 Markdown、HTML 预览和 PDF：

```bash
python ../scripts/build_v41.py
```

历史 v0.1 版本说明冻结在 [VERSION-v0.1.md](VERSION-v0.1.md)，可用 `python ../scripts/build_v01.py` 重建 v0.1 合订稿。
历史 v0.2 版本说明冻结在 [VERSION-v0.2.md](VERSION-v0.2.md)，可用 `python ../scripts/build_v02.py` 重建 v0.2 合订稿。
历史 v0.3 版本说明冻结在 [VERSION-v0.3.md](VERSION-v0.3.md)，可用 `python ../scripts/build_v03.py` 重建 v0.3 合订稿。
历史 v0.4 版本说明冻结在 [VERSION-v0.4.md](VERSION-v0.4.md)，可用 `python ../scripts/build_v04.py` 重建 v0.4 合订稿。
历史 v0.5 版本说明冻结在 [VERSION-v0.5.md](VERSION-v0.5.md)，可用 `python ../scripts/build_v05.py` 重建 v0.5 合订稿。
历史 v0.6 版本说明冻结在 [VERSION-v0.6.md](VERSION-v0.6.md)，可用 `python ../scripts/build_v06.py` 重建 v0.6 合订稿。
历史 v0.7 版本说明冻结在 [VERSION-v0.7.md](VERSION-v0.7.md)，可用 `python ../scripts/build_v07.py` 重建 v0.7 合订稿。
历史 v0.8 版本说明冻结在 [VERSION-v0.8.md](VERSION-v0.8.md)，可用 `python ../scripts/build_v08.py` 重建 v0.8 合订稿。
历史 v0.9 版本说明冻结在 [VERSION-v0.9.md](VERSION-v0.9.md)，可用 `python ../scripts/build_v09.py` 重建 v0.9 合订稿。
历史 v0.10 版本说明冻结在 [VERSION-v0.10.md](VERSION-v0.10.md)，可用 `python ../scripts/build_v10.py` 重建 v0.10 合订稿。
历史 v0.11 版本说明冻结在 [VERSION-v0.11.md](VERSION-v0.11.md)，可用 `python ../scripts/build_v11.py` 重建 v0.11 合订稿。
历史 v0.12 版本说明冻结在 [VERSION-v0.12.md](VERSION-v0.12.md)，可用 `python ../scripts/build_v12.py` 重建 v0.12 合订稿。
历史 v0.13 版本说明冻结在 [VERSION-v0.13.md](VERSION-v0.13.md)，可用 `python ../scripts/build_v13.py` 重建 v0.13 合订稿。
历史 v0.14 版本说明冻结在 [VERSION-v0.14.md](VERSION-v0.14.md)，可用 `python ../scripts/build_v14.py` 重建 v0.14 合订稿。
历史 v0.15 版本说明冻结在 [VERSION-v0.15.md](VERSION-v0.15.md)，可用 `python ../scripts/build_v15.py` 重建 v0.15 合订稿。
历史 v0.16 版本说明冻结在 [VERSION-v0.16.md](VERSION-v0.16.md)，可用 `python ../scripts/build_v16.py` 重建 v0.16 合订稿。
历史 v0.17 版本说明冻结在 [VERSION-v0.17.md](VERSION-v0.17.md)，可用 `python ../scripts/build_v17.py` 重建 v0.17 合订稿。
历史 v0.18 版本说明冻结在 [VERSION-v0.18.md](VERSION-v0.18.md)，可用 `python ../scripts/build_v18.py` 重建 v0.18 合订稿。
历史 v0.19 版本说明冻结在 [VERSION-v0.19.md](VERSION-v0.19.md)，可用 `python ../scripts/build_v19.py` 重建 v0.19 合订稿。
历史 v0.20 版本说明冻结在 [VERSION-v0.20.md](VERSION-v0.20.md)，可用 `python ../scripts/build_v20.py` 重建 v0.20 合订稿。
历史 v0.21 版本说明冻结在 [VERSION-v0.21.md](VERSION-v0.21.md)，可用 `python ../scripts/build_v21.py` 重建 v0.21 合订稿。
历史 v0.22 版本说明冻结在 [VERSION-v0.22.md](VERSION-v0.22.md)，可用 `python ../scripts/build_v22.py` 重建 v0.22 合订稿。
历史 v0.23 版本说明冻结在 [VERSION-v0.23.md](VERSION-v0.23.md)，可用 `python ../scripts/build_v23.py` 重建 v0.23 合订稿。
历史 v0.24 版本说明冻结在 [VERSION-v0.24.md](VERSION-v0.24.md)，可用 `python ../scripts/build_v24.py` 重建 v0.24 合订稿。
历史 v0.25 版本说明冻结在 [VERSION-v0.25.md](VERSION-v0.25.md)，可用 `python ../scripts/build_v25.py` 重建 v0.25 合订稿。
历史 v0.26 版本说明冻结在 [VERSION-v0.26.md](VERSION-v0.26.md)，可用 `python ../scripts/build_v26.py` 重建 v0.26 合订稿。
历史 v0.27 版本说明冻结在 [VERSION-v0.27.md](VERSION-v0.27.md)，可用 `python ../scripts/build_v27.py` 重建 v0.27 合订稿。
历史 v0.28 版本说明冻结在 [VERSION-v0.28.md](VERSION-v0.28.md)，可用 `python ../scripts/build_v28.py` 重建 v0.28 合订稿。
历史 v0.29 版本说明冻结在 [VERSION-v0.29.md](VERSION-v0.29.md)，可用 `python ../scripts/build_v29.py` 重建 v0.29 合订稿。
历史 v0.30 版本说明冻结在 [VERSION-v0.30.md](VERSION-v0.30.md)，可用 `python ../scripts/build_v30.py` 重建 v0.30 合订稿。
历史 v0.31 版本说明冻结在 [VERSION-v0.31.md](VERSION-v0.31.md)，可用 `python ../scripts/build_v31.py` 重建 v0.31 合订稿。
历史 v0.32 版本说明冻结在 [VERSION-v0.32.md](VERSION-v0.32.md)，可用 `python ../scripts/build_v32.py` 重建 v0.32 合订稿。
历史 v0.33 版本说明冻结在 [VERSION-v0.33.md](VERSION-v0.33.md)，可用 `python ../scripts/build_v33.py` 重建 v0.33 合订稿。
历史 v0.34 版本说明冻结在 [VERSION-v0.34.md](VERSION-v0.34.md)，可用 `python ../scripts/build_v34.py` 重建 v0.34 合订稿。
历史 v0.35 版本说明冻结在 [VERSION-v0.35.md](VERSION-v0.35.md)，可用 `python ../scripts/build_v35.py` 重建 v0.35 合订稿。
历史 v0.36 版本说明冻结在 [VERSION-v0.36.md](VERSION-v0.36.md)，可用 `python ../scripts/build_v36.py` 重建 v0.36 合订稿。
历史 v0.37 版本说明冻结在 [VERSION-v0.37.md](VERSION-v0.37.md)，可用 `python ../scripts/build_v37.py` 重建 v0.37 合订稿。
历史 v0.38 版本说明冻结在 [VERSION-v0.38.md](VERSION-v0.38.md)，可用 `python ../scripts/build_v38.py` 重建 v0.38 合订稿。
历史 v0.39 版本说明冻结在 [VERSION-v0.39.md](VERSION-v0.39.md)，可用 `python ../scripts/build_v39.py` 重建 v0.39 合订稿。
- 2026-07-12：第 6 章已补齐 1D semi-implicit/theta-implicit Picard sibling 的运行级总能量对照，分别验证 `2.2569031e-06 < 2.5e-05` 与 `3.4784001e-15 < 1e-14`；项目独立合同分析脚本已统一。

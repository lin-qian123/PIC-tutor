# PIC-tutor v0.94

本版新增 RZ axis charge 的源码-诊断交叉审计：13/13 个 WarpX 当前 checkout 源码锚点通过，确认 particle rho 沉积后的 inverse-volume scaling、`rho_buf` coarse-level scaling、solver-native `divE` 计算、Rho/DivE diagnostic functor 的独立路径与 FullDiagnostics 的分离注册。该合同把 v0.93 的跨 family repeat stability 从“稳定 observable”进一步约束到“稳定但未归因的 source/diagnostic boundary”，不把 residual 升级成 deposition kernel root cause。

报告见 `runs/stage-c-validation/rz-axis-charge-source-diagnostic-crosswalk-v0.94/contract.{json,md}`，说明见 `notes/code-reading/particles/76-rz-axis-charge-source-diagnostic-crosswalk.md`。

正式收敛阶、RZ axis charge root cause、publisher PDF、transition-zone ledger、RZ implicit runtime、Vay+AMR 和人工编辑/许可审查仍未关闭。

---


本版新增 correction-on axis charge 的跨 family reader-side repeat stability contract：以 v0.92 已 materialize 的第一、第二组 RZ/RSPHERE family 为输入，6 个 correction-on level 的 axis residual 全部在 `1e-10` 相对重复容差内稳定，且两组 family 的 axis residual 均高于 off-axis。correction-off 仍只作为负对照，靠近数值地板的相对差不进入同一 gate。合同见 `runs/stage-c-validation/rz-axis-charge-repeat-stability-v0.93/contract.{json,md}`，说明见 `notes/code-reading/particles/75-rz-axis-charge-repeat-stability.md`。

该合同的分类为 `REPEAT_STABLE_AXIS_CHARGE_BOUNDARY_NOT_KERNEL_ROOT_CAUSE`：它把 correction-on axis residual 从“单次 reader-side 现象”推进为“跨 family 稳定的 reader-side boundary”，但不识别 deposition kernel root cause，不证明 current closure，也不关闭正式 order。

本版完成预注册的第二组独立 refinement family：RZ/RSPHERE 各包含 `64/128/256`、`correction=on/off` 六组 producer，共 12 个 2-rank producer；在 Conda 环境提供的 `mpiexec` 与 `FI_PROVIDER=tcp` 下全部返回码为 0，且每组均生成 `producer.log`、`warpx_used_inputs` 和 diagnostics。合同见 `runs/stage-c-validation/formal-convergence-repeat-family-v0.92-tcp/contract.{json,md}`。

本版新增两组 family 的独立 reader-side slope 对照：RZ 的 `Er/Ez/axis/off-axis` 与 RSPHERE 的 `Er/axis/off-axis` 均覆盖全部相邻 `64->128`、`128->256` pair，结果按 geometry 和 correction 分开报告，不做 pooled fit。报告见 `runs/stage-c-validation/formal-convergence-second-family-v0.92/contract.{json,md}`，说明见 `notes/code-reading/particles/74-formal-convergence-second-family.md`；该结果证明第二 family 已 materialize，但不把 descriptive slope 升格为正式 order。

本版延续 RZ Esirkepov correction-on shape=1/2/3/4 的 rho-side species decomposition 观测 family：四个 shape 的末态 `rho-(rho_electrons+rho_ions)` 均达到约 `1e-14` reader-side 一致性，integrated-rho 漂移也被逐 shape 记录；该 family 不关闭同面 `divE-rho` axis charge boundary、正式收敛阶或 current-conservation contract。当前 MPI runner 已通过显式 `FI_PROVIDER=tcp` 环境稳定执行，默认 provider 的 `utun6` finalize 错误只保留为运行环境边界证据。

本版将 RZ axis residual profile 从单一末帧扩展到 8 个 `256x512`、2-rank sibling 的全部 24 个数值 plotfile。排除 `diag1000000` 初始化基线后，16 个 evolved frames 的 profile maximum 全部位于 `r=0`，分类为 `POST_INITIAL_AXIS_DOMINATED_READER_SIDE_RESIDUAL_TIME_PROFILE`；该结果仍是 reader-side 诊断，不关闭 `divE-rho`、current closure 或 formal convergence。

本版新增 rho/species decomposition 时间合同：对同一 8 个 case 的 `rho`、`rho_electrons` 和 `rho_ions` 读取 24 帧，排除初始化基线后 16 个 evolved frames 全部通过 `1e-12` gate，分类为 `EVOLVED_TIME_RHO_SPECIES_DECOMPOSITION_PASS_AXIS_CHARGE_SEPARATE`；该结果强化 rho-side assembly 与独立 axis charge boundary 的分层，不关闭 current closure 或 formal convergence。

本版新增正式收敛 study 预注册合同：固定 RZ/RSPHERE 独立 geometry、field/charge norm、primary/secondary observable、全部相邻拟合区间、correction-off negative control 和每种 geometry 至少两组独立 family 的关闭条件。当前 materialized 数据仍只有每种 geometry 一组 family，且 correction-on axis charge 仍是 boundary，因此分类为 `FORMAL_CONVERGENCE_PREREGISTERED_CURRENT_DATA_INSUFFICIENT`，不把 descriptive slope 写成正式收敛阶。

本版延续第 5 章独立几何趋势合同：将现有 RZ 与 RSPHERE 三档 2-rank resolution family 分开计算 `Er`/axis/off-axis observable 的描述性 slope，保留 correction-off negative control，并明确不做跨几何 pooled fit。分类为 `EXPLORATORY_CROSS_GEOMETRY_RESOLUTION_TRENDS_FORMAL_ORDER_UNPROVEN`；该增量推进正式收敛 study 的独立 family 设计，但不关闭正式收敛阶缺口。

本版修复第 7 章边界 regression 五列表格在 PDF 中的列重叠：将渲染正文改为窄索引，并保留原始宽表为源码注释证据。新增 `scripts/audit_pdf_layout.py`，对页面文本覆盖、已知宽表风险、关键章节和注释结构进行自动检查；代表页 1、184、190、328 已实际渲染复核。当前分类为 `PDF_LAYOUT_AUTOMATED_PASS_MANUAL_SPOTCHECK_RECORDED`，人工全书通读、许可和公开再分发审查仍未关闭。

本版新增可重复的自动编辑质量审计：对合订 Markdown 的标题与表格结构、HTML 标题数与关键章节、PDF 页数与关键章节以及构建警告进行一致性检查。当前结果为 `AUTOMATED_EDITORIAL_AUDIT_PASS_MANUAL_REVIEW_OPEN`；自动检查通过，但人工通读、HTML/PDF 版式检查、第三方材料许可和公开再分发审查仍未关闭。

本版新增项目级当前成书缺口登记：八项开放项分别绑定当前证据、分类、下一步动作和可验收关闭条件，覆盖 publisher access、transition-zone route ledger、RZ implicit Villasenor、Vay+AMR、RZ axis charge、formal convergence 和 release editorial gate。新增 `scripts/audit_current_gap_register.py` 与 `docs/current-book-gap-register.md`，分类为 `CURRENT_BOOK_GAP_REGISTER_WITH_EVIDENCE_AND_CLOSURE_CRITERIA`；登记表用于防止历史 TODO 漂移，不把任何开放项写成已完成。

本版新增第 5 章收敛研究就绪合同：基于既有 RZ Esirkepov shape=1 的 `64x128/128x256/256x512` 三档控制，计算 `Er/Ez`、all-cell/axis/off-axis charge residual 的描述性 pairwise order，并明确 refinement family、observable、axis treatment 和正式收敛阶之间的边界。新增 `scripts/audit_deposition_convergence_readiness_contract.py`，分类为 `CONVERGENCE_READINESS_WITH_FORMAL_ORDER_UNPROVEN`；当前数据可用于设计正式 study，但不把经验 order 写成物理或论文结论。

本版新增第 5 章沉积证据梯度：将 Direct、Esirkepov、Villasenor-Buneman 和 Vay 的论文/公式层、WarpX 源码层、runtime consumer 和不能外推的范围并列收口。新增 `scripts/audit_deposition_evidence_gradient_contract.py`，分类为 `DEPOSITION_PAPER_SOURCE_RUNTIME_GRADIENT_WITH_EXPLICIT_GAPS`；该矩阵推进了论文-源码-测试三线闭环，但不把局部 runtime family 写成完整 geometry/order/AMR 覆盖。

本版新增第 7 章 PML 证据梯度矩阵：将 Cartesian FDTD/PSATD 低反射率、RZ 残余场、重启重复性、粒子入 PML 和 3D cleaning reader-side 结果分开列出，逐项写明 producer、consumer、可支持结论和负面边界。新增 `scripts/audit_pml_evidence_gradient_contract.py`，将正文、WarpX 只读源码锚点和代表性 runtime contract 固化为 `PML_EVIDENCE_GRADIENT_WITH_EXPLICIT_RUNTIME_BOUNDARIES`；该矩阵不把未覆盖的 solver、几何、AMR 或入射角组合升级为完成。

本版完成 Esirkepov 2001 CPC indexed abstract 与 arXiv 预印本的 bounded compare：发表版 metadata/abstract 的算法主张已逐项归类，新增 `notes/code-reading/particles/63-esirkepov-publisher-abstract-compare.md` 和 `scripts/audit_esirkepov_publisher_abstract_compare.py`。publisher-formatted PDF 仍未取得，因此 `Eq.(23)` 排版、section numbering 和发表版图表继续保持明确边界。

本版补入第 5 章 v0.75 沉积算法选择矩阵：按 geometry/grid、explicit/implicit 时间层、source-side 守恒机制和现有 runtime 证据统一比较 Direct、Esirkepov、Villasenor 与 Vay，并由 `scripts/audit_deposition_algorithm_selection_contract.py` 验收。该矩阵明确算法限制和证据边界，不把单一 Langmuir PASS 外推为完整 geometry/order physics coverage。

本版新增 Vay--Godfrey 2014 relativistic PIC review 资产：9 页 PDF、MinerU Markdown、43 张图、论文顺序中文精读、access audit、reading log 和 `scripts/audit_vay_2014_review_asset_contract.py` 全部通过；第 4 章补入 pusher 历史与完整 PIC 离散链映射，第 6 章补入 PSATD/NCI 公式与当前 WarpX 机制边界，第 9 章同步文献路线。

本版新增 Andriyash 2016 Fourier-Bessel PIC 论文资产：9 页 PDF、MinerU Markdown、26 张图、按论文顺序中文精读、access audit、reading log 和 `scripts/audit_andriyash_2016_asset_contract.py` 全部通过；第 6 章补入 quasi-cylindrical Fourier-Bessel PSATD 的 primary-source 闭环，第 9 章同步路线图。该论文介绍 PLARES-PIC，不把其 benchmark 写成 WarpX runtime 或函数级等价证明。

本版由 `scripts/verify_v94_build.py` 验收，当前合订 PDF 页数以实际构建结果为准。

本版新增 Esirkepov 2001 发表版缺口审计契约：将 13 页作者预印本、39 张 MinerU 图片、`Eq.(23)` 到 `one_third/one_sixth` 与 `sdxi/sdyj/sdzk` 的公式-源码映射、CPC 发表元数据和 publisher-PDF 缺失边界固化为 11 项可重复检查；第 5 章明确保持“预印本公式 + 当前 WarpX 源码 + runtime consumer”三层交叉复核，不把 CPC 定稿写成已完成逐式核对。报告见 `runs/stage-c-validation/esirkepov-publication-boundary/contract.{json,md}`。

本版新增 Muraviev 2021 粒子重采样论文资产：50 页 PDF、MinerU Markdown、38 个图像资源、中文精读和 `10/10` asset contract 已通过；第 4 章将 agnostic down-sampling、局部权重噪声、严格守恒 thinning 与 WarpX `Resampling` 做有界映射，但不把 PICADOR/hi-chi QED cascade 案例升级为 WarpX runtime PASS。

本版延续 Vranic 2015 粒子合并论文资产：24 页 PDF、MinerU Markdown、32 张图、中文精读和 `11/11` asset contract 已通过；第 4 章将论文的两粒子局部守恒 merge 与 WarpX `VelocityCoincidenceThinning` 做有界映射，但不把论文案例升级为 WarpX runtime PASS。

本版延续第 9 章的 `docs/literature-pending-triage.md`：对 literature map 中仍待分类的 81 条 BibTeX 条目保留保守的候选主题、章节入口、P1/P2/P3 优先级和获取动作。该 triage 只服务于 acquisition/read queue，不把标题关键词、metadata 或建议章节升级为全文阅读或正文证据。

本版又固化 Vay + AMR 的 source guard：当前 `WarpX.cpp` 在 `Vay && maxLevel() > 0` 时于初始化阶段拒绝运行，分类为 `SOURCE_GUARD_AMR_RUNTIME_INTENTIONALLY_REJECTED`；不把该支持边界写成 AMR physics PASS/FAIL。

本版又补齐 Vay Cartesian shape family 的 2-rank case-local runtime contract：2D/3D × shape=1/2/3/4 共 8 个 producer 均通过官方 `divE-rho/epsilon_0` 的 `1e-3` gate；shape=1/2/4 是本地 sibling，不写成上游 CMake 新注册项。

本版又补齐官方 Vay 2-rank runtime consumer：2D/3D shape=3 按 CMake 注册规模运行并通过 `divE-rho/epsilon_0` 的 `1e-3` gate，结果为 `4.0411e-4/6.0266e-4`；shape family 的 2-rank 全组合、AMR/边界和正式收敛阶仍保持边界。

本版又补入 Vay Cartesian shape-family runtime contract：2D/3D 的 `particle_shape=1/2/3/4` 共 8 个单进程 producer 均通过官方 `divE-rho/epsilon_0` analysis 的 `1e-3` gate；其中 6 个为新增 sibling。该证据不替代官方 2-rank CMake 回归、AMR/边界组合或正式收敛阶研究。

本版又补入第 5 章 geometry/order coverage gap register：7 项已知缺口被统一登记为 `BOUNDARY`、`UNPROVEN`、`PRE_PHYSICS_BOUNDARY` 或 `PARTIAL`，并分别绑定下一步证据入口。该 negative-space contract 只关闭缺口登记的文档歧义，不把未覆盖组合升级为 PASS。报告见 `runs/stage-c-validation/deposition-geometry-order-gap-register/contract.{json,md}`。

本版又补入 Vay deposition geometry/order official wiring contract：18 项检查确认官方 2D/3D shape=3、2D shape=4、`divE-rho/epsilon_0` analysis consumer 和 RZ/1D/implicit source guard；分类为 `SOURCE_REGRESSION_WIRING_PARTIAL_RUNTIME_FAMILY`，不宣称完整 geometry/order runtime product。报告见 `runs/stage-c-validation/vay-geometry-order-wiring/contract.{json,md}`。

本版又完成 Vay 2D/3D 单进程 runtime consumer contract：官方输入实际生成 `diag1000050`/`diag1000025`，`divE-rho/epsilon_0` 相对误差分别为 `1.5543e-4` 与 `2.9007e-4`，均通过 `1e-3` gate；该结果不替代官方 2-rank 回归，也不关闭完整 geometry/order family 边界。报告见 `runs/stage-c-validation/vay-runtime/contract.{json,md}`。

本版又补入第 9 章文献路线资产合同：12 组检查绑定 A/B/C/D 证据层、八条核心文献目录、全局 literature map、生成式 inventory 以及 `TajimaDawson1982`、`Esirkepov 2001`、`LeeCPC2015`、`Yee 1966`、`Hockney-Eastwood` 的缺口声明。该合同只确认路线图与仓库资产一致，不替代论文逐式审校或 runtime physics proof。报告见 `runs/stage-c-validation/literature-roadmap-asset-contract/contract.{json,md}`。

本版又修正第 5 章 `5.11.1/5.11.2/5.11.3` 小节错序，并把小节单调性与重复编号纳入 v0.68 artifact verification。

本版又修正第 6 章 `6.11.3` 重复编号，顺移后续 regression 小节，并把第 6 章小节单调性与重复编号纳入 v0.68 artifact verification。

本版又为第 9 章补入证据层分类、合同复核和 acquisition 排序三项读者练习，使第 1-9 章均具备可执行的练习或复核入口。

本版又修正第 8 章 `8.14.1` 孤立标题层级为正式 `8.14` 小节，并将正文验证矩阵的合同数口径更新为当前 `189` 条。

本版又补入第 8 章 reduced diagnostics 最小输入合同：12 项检查覆盖 `FieldProbe`、`ParticleHistogram2D`、`LoadBalanceCosts` 的官方输入和 analysis consumer；公开证据索引当前为 `189` 条。

本版又补入第 6 章 FieldSolver 正文-源码 crosswalk：12 组代表性锚点覆盖 `WarpXEvolve.cpp` 外层推进、FDTD/PML kernel、Cartesian/RZ spectral 分派和 regression 证据边界。该合同只用于防止正文随当前 WarpX 源码漂移，不替代 C++ 语义等价证明、runtime physics proof 或论文逐式复现。报告见 `runs/stage-c-validation/fieldsolver-chapter-source-crosswalk/contract.{json,md}`。

本版又补入第 7 章边界/PML/AMR 正文-源码 crosswalk：13 组代表性锚点覆盖 field/particle 边界顺序、场边界分派、PML 生命周期、guard-cell/通信、AMR 重建、moving window 和 scraping consumer；transition-zone route ledger 仍保持 `RUNTIME_LEDGER_UNPROVEN`。该合同只防止正文漂移，不替代 runtime route-count proof。报告见 `runs/stage-c-validation/boundary-amr-chapter-source-crosswalk/contract.{json,md}`。

本版又补入第 8 章诊断/验证正文-源码 crosswalk：13 组代表性锚点覆盖主循环调度、Full/BTD/BoundaryScraping 类型分派、`ComputeDiagFunctors`/flush、OpenPMD iteration 生命周期、reduced diagnostics 注册/写盘和官方 analysis consumer。该合同只防止章节 wiring 漂移，不替代 case-local physics gate。报告见 `runs/stage-c-validation/diagnostics-chapter-source-crosswalk/contract.{json,md}`。

本版又完成 Birdsall `3A ES1` 章节回填的 source crosswalk：11 组代表性锚点核对历史阶段链、WarpX fresh/restart 初始化、粒子生命周期、`Evolve()` 分派和 Langmuir/初始化验证层。该合同不宣称历史程序与现代 WarpX 逐函数等价。报告见 `runs/stage-c-validation/birdsall-3a-warpx-crosswalk/contract.{json,md}`。

本版又为第 5 章新增 deposition 正文-源码 crosswalk：13 组代表性锚点同步 charge bridge、旧/新时间层、implicit Esirkepov/Villasenor、Villasenor segment kernel、shape helper 和 RZ/径向 geometry surface；该 contract 只防止正文随源码漂移，不升级为 C++ 语义证明、完整 geometry/order runtime 覆盖或论文逐行复现。报告见 `runs/stage-c-validation/deposition-chapter-source-crosswalk/contract.{json,md}`。

本版又复核 RZ theta-implicit Villasenor 的构建/运行边界：官方 `petsc_ksp` 输入仍受当前 binary 缺少 `AMREX_USE_PETSC` 阻断；同一 binary 的 MPI=2 `amrex_gmres` control 能完成 DOF 定义后，在 RZ curl-curl boundary-mask 初始化阶段触发 `SIGILL`，尚未进入粒子推进或 current deposition。新增 `scripts/audit_rz_implicit_villasenor_build_boundary.py` 及对应 command-output/contract；该结果保持为 pre-physics boundary，不升级为 Villasenor physics pass/fail。

本版又补入第 5 章 deposition 证据层导航表：将 Esirkepov 的论文/索引摘要、当前源码、代数/源码合同和 runtime consumer 分开列出，明确每层能支持与不能支持的结论；`scripts/audit_esirkepov_paper_source_runtime_crosswalk.py` 当前 15 项检查全部通过，但仍保留 publisher-PDF 逐行对照、完整 geometry/order product 和 AMR 强 runtime 闭环边界。

本版新增 RZ Esirkepov charge/field tradeoff summary contract：对 7 组既有 RZ evidence family 做 12 项统一交叉检查，确认默认 axis correction 下 field gate 通过而 axis charge 仍为 `BOUNDARY`，correction-off 只在局部 sibling 上恢复 charge；该结果不修改 WarpX 默认参数，也不宣称正式收敛阶。报告见 `runs/stage-c-validation/esirkepov_langmuir_rz-charge-field-tradeoff-summary/contract.{json,md}`。

本版新增 RCYLINDER/RSPHERE species-rho decomposition observable：通过为 RCYLINDER shape=1 增加物种 rho 诊断字段，径向 Esirkepov shape=1/2/3/4 共 8 个案例、81 个当前编号帧合计 648/648 通过；按参与相加字段幅值归一化的 `rho-(rho_electrons+rho_ions)` 最大相对差为 `2.295e-16`。该 observable 不替代 radial `divE-rho` 或 current-closure proof。报告见 `runs/stage-c-validation/radial-rho-decomposition-observable/contract.{json,md}`。

本版新增 position-update output-staggering contract：源码确认 `UpdatePosition.H` 的 `u*inv_gamma*dt` 公式和 `PhysicalParticleContainer.cpp` 的 `Full` dispatch；三组 uniform-`B` Full plotfile 的单帧动量配对误差约 `6.242e-2`，相邻帧中点 proxy 最大误差约 `1.609e-3`。该证据确认输出时间层边界，不把机械动量字段升级为直接 half-step velocity attribute。报告见 `runs/stage-c-validation/position-update-runtime-contract/contract.{json,md}`。

本版统一 Higuera-Cary Poincare evidence boundary：短轨道为 `INSUFFICIENT_SAMPLING`，长轨道 invariant/reference 与 angular-order candidate 通过但 topology 保持 `REVIEW_REQUIRED`，密集族 resonance screen 通过而解析 reference/candidate signature 保留边界；不宣称论文等价 topology gate。报告见 `runs/stage-c-validation/higuera-poincare-evidence-summary/contract.{json,md}`。

本版新增 parameter-map semantic anchor contract：对 10 条非固定键/外部 owner 参数补齐 consumer、默认值或校验锚点，覆盖 user attributes、DSMC scattering keys、ADIOS2 parameter maps、particle-field reduction 和 AMReX refinement ratio；全部通过，但仍保留 C++ AST、完整默认值矩阵和 runtime value execution 边界。报告见 `runs/stage-c-validation/parameter-map-semantic-anchor-contract/contract.{json,md}`。

本版新增 parameter-map runtime coverage contract：case-local smoke 实际验证用户属性粒子字段、15 个 particle-field reduction 输出、openPMD HDF5、scalar `amr.ref_ratio`、2D `amr.ref_ratio_vect` level 0/1 物化，以及 3D BP5 的 ADIOS2 engine/operator suffix 与 openPMD-api 读回；当前合同包含 5 个 runtime case，DSMC 仍因本机缺少 `warpx-data` 截面文件保留 input-only/data boundary。该结果明确扩展了运行覆盖，但不宣称完整参数回归。报告见 `runs/stage-c-validation/parameter-map-runtime-coverage/contract.{json,md}`。

本版新增 parameter-map structured review contract：parser-anchor 之外的 10 条参数已逐项核对，8 条 dynamic-key constructor 和 2 条 AMReX owner 全部通过源码锚点检查；该结果不替代完整 C++ AST、默认值/校验或 runtime value semantics 审计。报告见 `runs/stage-c-validation/parameter-map-structured-review-contract/contract.{json,md}`。

本版新增 parameter-map parser-anchor review surface：排除通用 `type/field/x/y/z` token，限制为普通单行 C++ literal，并覆盖 `query_enum_sloppy`、`queryArrWithParser`、`getWithParser`、`getArrWithParser`、`Store_parserString`、`getEntries` 后，445 条参数中 269 条找到精确 parser-call anchor，另有 166 条找到 parser-literal-only anchor，8 条确认是 dynamic-key constructor，2 条确认是 AMReX owner 参数，没有未分类项；该结果不替代 C++ AST、默认值/校验或 runtime value semantics 审计。报告见 `runs/stage-c-validation/parameter-map-parser-anchor-contract/contract.{json,md}`。

本版进一步完成这 10 条非固定键的精确源码复核：AMReX `AMReX_AmrMesh.cpp` 的 `ref_ratio/ref_ratio_vect` 输入、互斥和 materialize 分支，以及 8 条 dynamic-key constructor/consumer 均通过多 marker contract。parser-anchor 报告将它们标记为 `structured_review_verified`，剩余人工 review queue 为 0；这只关闭源码结构层缺口，不关闭完整 C++ AST、默认值矩阵或 runtime value semantics。

本版又将 3D AMR `particles_in_pml` signed/absolute 分解提升为公开 boundary contract：官方 signed gate 为 `106.4354 < 110`，严格 absolute gate 为 `110.3994 > 110`，唯一越界项是负向 `Ex`，coarse/fine 读取一致。该结果只关闭“判据差异未被结构化索引”的缺口，不关闭 AMR/PML 强残余场验证，也不修改上游阈值。

本版将 RZ secondary-emission 三档 resolution trend 提升为公开 boundary contract：`64x64` 默认基线仍为 raw `FAIL`，`128x128/256x256` refined controls 通过官方 `2%` EB impact-point gate；该结果支持 resolution-sensitive geometry diagnosis，但不关闭默认 upstream regression，也不构成正式 convergence order。

本版新增显式 leapfrog position source crosswalk：只读核对 `PhysicalParticleContainer::Evolve()` 的 momentum-then-position 顺序、`UpdatePosition.H` 的时间中心速度公式、维度条件，以及 `PushSelector.H` / Higuera-Cary 接口的 split-push 边界。正文明确相邻 Full plotfile 位置差只能构造 velocity proxy，不能冒充直接 half-step attribute；Vay Appendix B 已建立 proxy-level bounded runtime contract，但直接 half-step attribute 和论文图形逐点复现仍未接入。

本版又补入 Vay Appendix B 窄化 uniform-B runtime proxy：三种 pusher 各生成 81 个 Full plotfile，离散 phase、position-update velocity proxy、gyroradius proxy 和动量范数均通过窄 gate；报告分开记录最终 plotfile 写出后的 `ComputeDivE` finalize tail，不把它误读成 pusher 物理失败。该结果仍是 proxy-level bounded reproduction，不是直接 half-step attribute 或论文图形逐点复现。

本版新增 Boris 1970 论文专属 metadata/access contract：DTIC `ADA023511` 的书目身份已固定，PDF 限流响应和原始 proceedings 全文缺失边界已记录；第 4 章以 Birdsall 1985 二手全文推导和 WarpX `UpdateMomentumBoris.H` 源码支撑算法解释，不宣称完成 Boris 1970 原文逐页核对。

本版又新增 Boris 当前 WarpX source crosswalk contract：只读核对 `UpdateMomentumBoris.H` 的 half-push、gamma/磁旋转、半角重标定以及 `PushSelector.H` 的 Boris/辐射反作用分派；这是当前实现证据，不替代原始 proceedings 全文。

本版又新增 Yee 当前 WarpX FDTD source crosswalk contract：只读核对 `CartesianYeeAlgorithm.H`、`FiniteDifferenceSolver.cpp`、`EvolveB.cpp`、`EvolveE.cpp` 的 CFL、交错差分和 solver dispatch；这是现代实现证据，不替代 IEEE 1966 原文。

本版新增第 4 章 Vay 2008/Higuera-Cary 2017 论文资产合同：Vay 7 页/38 图、Higuera-Cary 9 页/44 图，全文、MinerU、中文讲解、README、access audit、章节/源码映射均通过；Vay Appendix B 已补入 bounded proxy-level uniform-B contract，但直接 half-step attribute 与论文图形逐点复现仍是边界，Higuera Poincare section/invariant consumer 和 sampled topology classifier 已接入但不构成完整 Fig. 2 gate。

本版又新增 `larmor` 逐帧离散轨道合同：6 个 Full plotfile 的时间序列和粒子状态检查通过，报告记录了 `B_y`、`gamma` 与每个输出间隔的 Boris rotation-angle；当前仍不把该 AMR/PML/div-cleaning case 升级为论文专门 runtime reproduction。

本版又完成窄化 uniform-`B` Boris/Vay/Higuera-Cary runtime 对照：三条 case 各有 81 个 Full plotfile，并依据 `UpdatePosition.H` 重建 position-update velocity/gyroradius proxy；最大相对误差分别低于 `1.34e-14/4.8e-15`。该结果支持 Vay Appendix B 的 proxy 层条件，同时修正 2D XZ 面内动量读取路径为 `particle_momentum_x/z`；直接 half-step attribute 与 Poincare topology 仍作为边界。

本版又新增 Higuera-Cary Poincare section runtime contract：64³ 专用盒中三种 pusher 各输出 1001 帧，5 个初始条件均产生正向 `p_x` 的 `x=0` 截面交叉；最大 `H`/`I_y` 相对漂移为 `1.532e-3/8.206e-3`。该证据建立 section/invariant consumer，但不宣称 resonance-island 或 trajectory-crossing topology 已自动分类。

本版又加入 sampled Poincare topology classifier：它会计算截面多边形候选自交和轨道间交叉；32³、2201-frame 长轨道已达到 18/19 点/轨道阈值，但三种 pusher 的候选签名一致，结果保持 `REVIEW_REQUIRED`，不提升为论文 Fig. 2 topology reproduction。

本版又补入 Poincare invariant-order gate：长轨道三种 pusher 的 `I_y` 区间均互不重叠且保持 `p05 < p10 < p17 < p22 < p27` 顺序；该窄 gate 通过，但完整 topology gate 仍关闭。

本版又补入论文 Section VI 的解析 quartic reference gate：`p_y^2 + (b y^2/2)^2 = I_y` 的全部长轨道相对残差低于 `1e-2`，最差 Vay `p22=7.52e-3`；该结果只证明解析截面一致性。

本版又补入 dense `p_y=0.2..2.8` family 和 64³ `p_y=1.6/1.8` resolution control：Vay 共振窗口 `I_y` 漂移约 `6.5e-2`，Boris/Higuera-Cary 约 `1e-3`，但仍只标记为 resonance-sensitive invariant screen，不提升为 two-fold island topology reproduction。

本版新增公开验证证据摘要：`docs/public-evidence-index.{json,md}` 汇总本地 176 条 `contract.json`，保留原始 PASS/FAIL/UNKNOWN，并将明确分类为 boundary、unproven 或 missing 的记录标为 `evidence_kind=BOUNDARY`。摘要不含本机绝对路径；原始 `runs/` 仍不进入公共 release，也不把摘要当作原始运行证据的替代品。

本版又把 AMR transition-zone route-count packet 落成 `scripts/validate_transition_zone_route_contract.py` 和 `docs/transition-zone-route-contract-example.json`：正例 `DESIGN_SCHEMA_VALIDATED`，故意破坏 route count 的负例被拒绝。该 contract 只验证未来 runtime analysis 的 schema 与 arithmetic gate；当前 WarpX 尚未输出真实 route ledger，不能升级为 AMR physics PASS。

本版新增 Hockney 1971 article-level abstract contract：8 项本地检查全部通过，正式题名、DOI、作者机构摘要、摘要级中文讲解和 full-text 缺失边界均已归档。该资产支持 collision/heating scaling、optimum path 和 `K_2` 的摘要级引用，但不替代 publisher PDF、MinerU 或逐段核对。

本版又新增两篇 1974 particle-mesh 摘要级 contract：QPM/PPPM 与 force-shaping 各 8 项检查通过，补入 Gaussian cloud、potential shaping、sub-mesh resolution、charge-sharing hierarchy 和 force anisotropy 的来源边界；两篇 publisher full text 仍未 materialize。

本版又新增 Yee 1966 indexed-abstract contract：9 项检查全部通过，固定 finite-difference Maxwell、field-point placement、PEC boundary 和 conducting-cylinder example 的窄证据范围，并保留 IEEE full text、PDF、MinerU 和逐式核对缺失边界。

本版又新增 PSATD/NCI literature-to-source strategy matrix：Godfrey 2014、Lehe 2016、Kirchen 2016 三篇本地全文资产的章节映射、WarpX 源码关键词和 runtime consumer 全部通过检查；矩阵只做证据索引，不把 fixed-grid、Galilean 和 boosted-frame 三条机制合并。

本版完成 public release path hygiene：合订 Markdown/HTML 不再保留本机绝对路径或绝对本地链接，项目链接改为仓库相对路径，WarpX 外部路径改为 `$WARPX_ROOT` 占位符；该边界由 `scripts/audit_public_release_paths.py` 和 `scripts/verify_v68_build.py` 覆盖。

本版新增 Esirkepov 2001 bounded compare contract：本地预印本、CPC 发表元数据、Section 1--5、Eq.(23)、二阶 spline 线索与 publisher PDF 缺失状态共 8 项检查全部通过。该 contract 只固化当前证据边界，不替代尚未取得的 CPC 定稿逐行对照。

当前 v0.69 合订 PDF 为 326 页；本版在 v0.68 基础上补入第 9 章待分类文献的保守 acquisition/read triage，并保留强守恒 BOUNDARY，不把局部观测写成完整 Gauss-law 闭环。

本版另补入 RZ shape=1 的 `256x512` resolution control：correction-on axis charge residual 为 `3.593e-3 -> 1.520e-3 -> 7.554e-4`，correction-off 为 `5.513e-12 -> 9.353e-12 -> 1.639e-11`。官方 field analysis 在三档均通过；结果支持 correction-on 的分辨率敏感性，但 correction-off 在最高分辨率越过强 gate，因此不修改默认轴修正，也不宣称正式收敛阶。

本版同时补入 RZ correction-on `256x512` shape=1/2/3/4 family：`Er/Ez` field gate 全通过，charge residual 为 `7.554e-4/8.990e-4/9.289e-4/9.729e-4`，均由 axis cell 主导。该 family 进一步证明高分辨率 field closure 与 axis charge closure 仍是两个独立维度。

本版进一步补入同一 `256x512` 分辨率下的 correction-off 对照：shape=1/2/3/4 的 charge residual 为 `1.639e-11/1.020e-11/8.399e-12/6.669e-12`，只有 shape=3/4 通过 `1e-11`。八条 field gate 全通过，因此当前最准确的结论是 correction/shape 之间存在 tradeoff，不能把 correction-off 的局部通过外推为默认修复。

本版补充 `TajimaDawson1982` 的正式来源访问审计：DOI 与 AIP canonical resource 已确认，但本机请求返回 Cloudflare HTTP `403`，因此仍不宣称 publisher PDF、MinerU 或逐式核对完成。

本版补充一份相关但不同的 Tajima 1982 FNAL 单作者会议稿：26 页 PDF、MinerU、67 张图和中文讲解已通过独立资产合同；它只用于 beat-wave 主题旁证，不能替代正式 Tajima-Dawson AIP 论文。

本版又收口 Tajima-Dawson 1979 论文资产：4 页 PDF、MinerU、11 张图、中文精读和图 1/图 2 机制对应已通过独立合同；证据分类为 early LWFA scaling baseline，不替代现代 WarpX runtime regression。

本版又补入 Esirkepov 2001 CPC 发表版的摘要级访问边界：ScienceDirect 可见摘要固定 arbitrary form-factor、straight-line trajectory、no-Poisson-solve 和 2D/3D demonstration；直接 PDF 下载仍为 403/HTML，仍不宣称 publisher-PDF line-by-line compare。

本版又补强 LeeCPC2015 的 PML 证据边界：ScienceDirect indexed abstract 支持高阶 solver 至无限阶 pseudo-spectral limit 的摘要级主张，7 页 accepted manuscript 支持第一轮公式，WarpX source/runtime contract 支持当前实现路径；publisher-formatted CPC PDF 和逐版本差异仍未完成。

本版又将 Birdsall `3A ES1` 的历史阶段链回填第 3A 章：`INIT -> SETRHO -> FIELDS -> SETV -> ACCEL -> MOVE -> HISTRY` 现在与 WarpX `InitData()`、粒子初始化、初始场构造、`Evolve()` 和 diagnostics 有明确的近似映射，但不宣称旧程序与现代 WarpX 逐函数等价。

本版补充 `LeeCPC2015` accepted/submitted manuscript 资产合同：7 页 PDF、MinerU 结构、13 张图片、公式锚点和中文讲解全部通过；CPC publisher-formatted PDF 的版本差异仍待核对。

本版补充第 5 章 Villasenor/Esirkepov 本地论文资产合同：分别确认 11 页/27 图与 13 页/39 图的读取包完整；这只关闭本地资产可复核性，不关闭 publisher provenance 或 CPC 定稿逐行对照。

本版补充第 6 章 Birdsall 13-5 后半段：将 `K_4`、QPM、`N_C`/`1/N_C` field fluctuation 和 linear stochastic heating 写成 solver-design 语言，并保留其来自 Hockney 历史转述而非原始图表逐页核对的边界。

本版补充第 8 章 Dawson 1983 wave-side statistical diagnostics 链：modal energy、power spectrum、time correlation、磁化 peak taxonomy、normal-mode reconstruction 和 continuous-spectrum/quiet-start 边界均已回写正文。

本版补充第 4 章 Vay 2008 Appendix A/B：给出显式 `\gamma` 四次方程、正根选择、`gisq` 对位和常磁场 gyroradius/half-step velocity 边界；保留 Appendix B 尚无专门 runtime reproduction 的限制。

版本日期：2026-07-13

本次新增 3D Esirkepov shape=2/3/4 refined controls：shape=2/3/4 的 field error 分别为 `1.2523e-2/2.3515e-2/3.0644e-2`，charge residual 分别为 `5.4174e-12/4.3288e-12/3.0001e-12`。三档 `128^3` sibling 均通过官方 `0.05` field gate 和独立 `1e-11` charge gate。该结果支持分辨率敏感性解释，不修改全局默认值，也不宣称正式 convergence order。

本次新增 3D Esirkepov Langmuir shape=2/3/4 runtime：在 `64^3`、2-rank 周期 Yee case 中，shape=2 的官方 field error 为 `3.5970e-2 < 0.05`、独立 charge residual 为 `1.3914e-12`；shape=3/4 的 charge residual 为 `9.2043e-13/7.2393e-13`，但 field error 为 `6.7792e-2/8.7344e-2`，超过官方 `0.05` field gate。该结果补足 3D 高阶 shape 的运行证据，但不宣称 refined convergence、AMR 或全 geometry/order 覆盖。

本次新增 deposition geometry/order coverage matrix：汇总 Esirkepov 的 1D/2D/3D、2D MR、RZ、RCYLINDER/RSPHERE 以及 implicit Villasenor 的 9 个证据行，逐项绑定现有 contract/reference。矩阵明确 RZ correction-on charge、径向 geometry 的完整 charge/Gauss-law、AMR route-count/intermediate-field、RZ implicit 物理运行和 3D Esirkepov shape=2/3/4 仍未关闭；它是证据索引，不是全组合回归声明。

本次新增 Esirkepov notation matrix：对当前 `CurrentDeposition.H` 的 14 个源码锚点全部通过，固定 `W^1/W^2/W^3` 到 `sdxi/sdyj/sdzk`、`Jx/Jy/Jz` 的方向映射，记录 `one_third/one_sixth` 的 old/new tensor-product mixed average 和 `invdtd` 的 transverse inverse cell area / `dt` 归一化。该结果支持 preprint-backed + source-grounded 的记号说明，不替代 CPC publisher-PDF line-by-line compare。

本次新增 3D AMR particles-in-PML 运行级分解：初始 `diag1000000` 的 `Ex/Ey/Ez` 全零；末态 `diag1000200` finest covering grid 上，官方 signed max 为 `106.4354 < 110`，严格 absolute max 为 `110.3994 > 110`，唯一越界项是边界侧 PML 区域的负向 `Ex`，而 `Ey/Ez` 的正负峰值绝对值均约 `102.5971`。level 0/1 读取给出相同极值。该结果只定位 signed consumer 的判据盲区，不修改 `../warpx`、阈值或上游 analysis。

本次新增 RZ secondary-emission resolution-aware boundary：默认 `64x64` case 的最大 EB impact-point 回溯误差为 `3.6038% > 2%`，仍保持 BOUNDARY；同一输入的 `128x128/256x256` controls 分别为 `0.9977%/0.6646%`，均通过官方 2% gate。该结果支持分辨率敏感性诊断，不修改默认输入、不放宽 tolerance，也不外推为 upstream baseline 已修复。

本次新增完整高阶 shape family：在 `128x256` 下 shape=2/3/4 的 correction-on/off field gate 全部通过；correction-off charge residual 为 `9.644e-12/6.086e-12/6.724e-12`，correction-on axis charge residual 为 `2.177e-3/2.353e-3/2.552e-3`。该结果没有把 correction-on residual 伪装成已闭合，也没有建议修改全局默认值。

本次新增 rho-side observable：对 shape=2/3/4 高分辨率 correction-on sibling 直接读取 `rho`、`rho_electrons` 和 `rho_ions`，末态 `rho-(rho_electrons+rho_ions)` 相对差为 `1.303e-14/1.228e-14/1.343e-14`；同时记录 integrated-rho 时间序列漂移 `2.371e-6/2.729e-6/3.354e-6`。后者只作为 rho-side 观测，不替代 `divE-rho`、current closure 或完整守恒证明；既有 `divE-rho` axis residual `2.177e-3/2.353e-3/2.552e-3` 继续保留为独立边界。

本次新增 shape=2/3/4 的 `64x128 -> 128x256` correction-off refined siblings：粗网格 `Er` error 为 `0.1323/0.1734/0.2134`，细网格降至 `9.318e-3/1.113e-2/1.365e-2`；三档 charge residual 均低于 `1e-11`，field/charge 双 gate 全部通过。该族结果仍限定为 RZ、单层、固定 Langmuir 输入，不改变全局轴修正默认值。

本次新增 shape=2 的 `64x128/128x256` paired runtime：correction-off 的 `Er` field error 从 `0.1323` 降至 `0.0093`，charge residual 为 `2.202e-12/9.644e-12`，高分辨率 field/charge 双 gate 通过；correction-on 高分辨率 field error 为 `9.321e-3/5.154e-3`，axis charge residual 为 `2.177e-3`，因此仍保留 charge boundary。该结果仅支持 shape/resolution/axis-correction 交互解释。

本次新增 RZ Esirkepov `particle_shape=1` 的 `64x128/128x256` paired runtime：默认 correction-on 的 axis charge residual 从 `3.593e-3` 降至 `1.520e-3`，correction-off 在两档分辨率均通过 field/charge 双 gate，`128x256` 的 charge residual 为 `9.353e-12`。既有 shape=2/3/4 correction-off 的 `Er` field 边界仍保留，不能把 shape=1 结果外推为全局默认建议；未修改 `../warpx`。

本次新增 `particles_in_pml` analysis source contract：审计确认上游 `analysis_particles_in_pml.py` 使用 `max(Ex.max(), Ey.max(), Ez.max())`，而项目独立 contract 使用逐分量 `max(abs(field))`；3D AMR sibling 的官方 `106.43539539129057 < 110` 与强化 `110.3993781372607 > 110` 因此不能合并成同一个“通过”结论。该审计只修改 PIC-tutor 文档和脚本，不修改 `../warpx`。

本次增量完成 RZ JRhom first-stage handoff asset 的可重复重建与目标 checkout dry-run 验收：bundle、helper、unified diff、provenance、submission packet 和 PR draft 均由 MPI=2 ledger 重建；目标 WarpX 保持 `unstaged`，未写入上游源码。baseline helper 通过，`ll2-no-timeavg-cleaning` 负对照按预期拒绝，独立 contract 继续为 `passed=true`。

同一增量还完成 comoving PSATD first-stage handoff asset 的可重复重建与正负复核：stable helper 通过，no-comoving reference 被 spike ceiling 拒绝，独立 contract 为 `passed=true`；目标 WarpX 仍保持 `unstaged`，energy gate 继续明确关闭。

本次还补做 RZ Galilean `current_correction` paired runtime：非 PSB 2-rank 仅 charge gate 略超阈值，PSB single-box single-rank 同时通过 energy 与严格 `1e-9` charge gate；独立 paired contract 已归档，分别保留 `CHARGE_BOUNDARY` 与 `PASS`。

本次继续补做 RZ Langmuir PSATD `current_correction` sibling：官方解析场与 charge analysis 通过，独立 `Er/Ez` 与同面 `divE-rho/epsilon_0` contract 也通过。

本次又补做 RZ Langmuir PSATD-JRhom `CL4` 2-rank sibling：官方与独立解析场 contract 通过；由于 `current_correction=0`，正文明确保留为 field/filter evidence，不宣称 charge-conservation gate。

本次继续补做标准 RZ Langmuir PSATD 2-rank sibling：官方与独立解析场 contract 通过，形成 standard / current-correction / JRhom `CL4` 三条 RZ Langmuir 对照；standard sibling 同样不适用 charge gate。

本次又完成官方 RZ PSATD-PML 2-rank 复现：独立 residual-field contract 得到 `max|Er|/max|Ez|=1.0316/0.5695`，通过 `<2.0` gate；RZ PML 证据从历史 1-rank 项目级结果提升为官方 2-rank + 独立复核。

本次还新增 RZ secondary-emission EB source contract：10/10 源码锚点通过，确认 callback/source wiring 完整；64×64 impact-point runtime gate 仍保持失败，128×128/256×256 仅作为分辨率敏感性对照。

本次又新增 RZ Langmuir PSATD family matrix：standard、current-correction 和 JRhom `CL4` 三条 official-input contract 的解析场 gate 全部通过，charge gate 的适用范围单独保留在 current-correction sibling。

本次还生成 v0.41 public-release manifest：484 个项目文件、`20,385,796` bytes，allowlist 排除 `runs/`、`references/` 和历史生成物；该 manifest 只服务发布审计，不代表已经完成 Git staging 或 push。

2026-07-12 增补 Esirkepov 1D/2D/3D Langmuir runtime evidence，并将 2D 扩展到当前支持的 shape=1/2/3/4：2D 理论场最大误差为 `1.2201e-2/3.4096e-2/4.6336e-2/6.0165e-2`，分别通过 `0.0503/0.0503/0.0503/0.07` 官方阈值；charge residual 为 `3.5650e-12/3.1326e-12/4.5607e-12/2.8977e-12`，均低于独立 `1e-11` gate。shape=0 在 `WarpX.cpp:1450` 初始化断言处拒绝；新增 2D MR overlay 的逐层 charge contract 为 L0/L1 `0.8828/1.2005`，因此标记为 `BOUNDARY`，不升级为 AMR 强守恒结论。

2026-07-12 增补 Esirkepov AMR route/source-sync source contract：当前 WarpX checkout 的 15 个源码锚点全部通过，覆盖粒子路由到 `current_fp/current_buf`、`depos_lev=lev-1` coarse 几何、buffer masks、`SyncCurrent` 与 fine-to-coarse merge；该证据与 2D MR runtime 的 L0/L1 `BOUNDARY` 结果并列，明确不替代 dedicated intermediate-field diagnostics。

2026-07-12 增补 Python MR intermediate-field observability audit：`MultiFabRegister` 的 `list/has/_get`、PICMI `sim.fields`、现有 `current_fp` Python regression 以及 `current_buf/rho_buf` allocation 的 7 个锚点全部通过；当前分类为 `INTERFACE_PRESENT_RUNTIME_LEDGER_UNPROVEN`，不把 generic field-register API 升级为 MR 中间场 runtime 证据。

2026-07-12 增补 transition-zone route-count implementation packet：固定 `PartitionParticlesInBuffers`、`PhysicalParticleContainer::Evolve`、`SyncCurrent/SyncRho` 的源码插入点，定义 `nfine/nbuffer`、weight、`rho/J`、coarsened fine、owner-mask 和 post-sync 的最小 reduced schema 与 gates；该设计尚未写入 `../warpx`。

2026-07-12 增补 charge deposition bridge source contract，以 13 个源码锚点验收时间层偏移、ABLASTR 暂存、形状函数分派、RZ 分支和原子写回。

2026-07-13 强化 deposition geometry/order source contract，以 69 个源码锚点验收 charge ordinary/shared、Direct、Esirkepov、Villasenor、Vay、implicit 的 shape=1/2/3/4 分派、六类几何分支、Vay 的 RZ/1D 不支持 guard、Vay-implicit guard 和径向 shared-memory 限制；该证据不替代全组合 runtime regression。

2026-07-12 补入 RCYLINDER/RSPHERE Esirkepov Langmuir 2-rank runtime evidence；独立径向 `Er` contract 的相对误差为 `2.174e-2/5.405e-3 < 0.12`，范围限定为两条径向场合同。

2026-07-12 将 RCYLINDER/RSPHERE Esirkepov radial `Er` runtime coverage 扩展到 shape=1/2/3/4，8 个 geometry×shape contract 全部通过；范围仍限定为径向场，不替代 charge/Gauss-law 验证。

2026-07-12 补入 RCYLINDER/RSPHERE shape=1 `rho/divE` charge 对照：关闭 axis correction 后 RCYLINDER 通过 `1e-11`，RSPHERE residual 降至 `2.420e-11` 但仍保留边界。

2026-07-12 增补 RSPHERE 64/128/256 resolution 与 axis-correction paired control；field gate 全通过，correction-on charge residual 为 `4.166e-2/1.390e-2/4.142e-3`，correction-off 为 `2.420e-11/9.843e-11/7.461e-11`，charge 仍保留为 resolution-sensitive boundary，不宣称收敛阶。

2026-07-12 增加 radial axis-volume correction source contract，10 个参数、RZ/RCYLINDER/RSPHERE 因子、charge scaling 和 rho buffer 调用锚点全部通过。

2026-07-12 复核 Esirkepov CPC 定稿的替代索引和 publisher endpoint：元数据状态已加强，但 PDF 仍返回 HTTP 403；publisher-PDF line-by-line compare 继续未完成。

2026-07-12 补入 RZ Esirkepov Langmuir 2-rank runtime evidence；独立 `Er/Ez` field contract 通过，误差为 `1.075e-2/8.240e-3`，但同面 charge residual `3.593e-3 > 1e-11`，保留为 charge `BOUNDARY`。

2026-07-12 补入 RZ Esirkepov charge boundary 源码语义 note，核对官方 RZ 排除条件以及 `ComputeDivE`、`DivEFunctor`、`RhoFunctor`、`FullDiagnostics` 的诊断分叉；当前 residual 只作为诊断合同边界，不归因成单一 kernel 失败。

2026-07-12 增加 RZ charge diagnostic source contract，11 个官方 exclusion、ComputeDivE/FDTD、DivE functor、rho functor 和 FullDiagnostics 锚点全部通过。

2026-07-12 增补 RZ Esirkepov `do_dive_cleaning=1/0` paired control：全局 charge residual `3.593e-3 -> 9.693e-2`，约 `26.98x`，且最大值由 axis cell 主导；当前分类为 `AXIS_DOMINATED_CLEANING_SENSITIVE_DIAGNOSTIC_BOUNDARY`。

2026-07-12 增补 `boundary.verboncoeur_axis_correction=true/false` RZ paired control：关闭 correction 后 charge residual 为 `5.513e-12 <= 1e-11`，field gate 仍通过；当前分类为 `AXIS_CORRECTION_OFF_RESTORES_CHARGE_GATE`，不修改全局默认值。

2026-07-12 将 RZ Esirkepov Langmuir 默认轴修正 runtime shape coverage 扩展到 shape=1/2/3/4；field gate 全部通过，charge residual 仍由 axis cell 主导并保持 BOUNDARY。

2026-07-12 增补 RZ shape=2/3/4 的 axis-correction-off 交叉对照：charge gate 恢复但 `Er` field gate 失败，确认存在 shape-dependent charge/field tradeoff。

2026-07-12 增补 2D AMR subcycling workflow 证据：官方 2-rank、250 步 producer 与独立 contract 均通过，最终两层 `64x256`、moving-window shift error `7.617e-8 m <= coarse dz`、四 species 存在；证据范围限定为输出完整性与几何时间合同，不替代 transition-zone route-count/守恒验证。

2026-07-12 增补 Cartesian 1D Silver-Mueller 证据：官方 2-rank、500 步 producer 与独立 contract 均通过，`Ex/Ey/Ez` 最大绝对值为 `3.887e-8/3.887e-8/0 V/m`，低于 `0.01 V/m`；Silver-Mueller 当前已覆盖 1D、2D x/z 与 RZ sibling 的短时 residual-field 合同。

2026-07-12 增补 Cartesian 2D Silver-Mueller z 证据：官方 2-rank、500 步 producer 与独立 contract 均通过，`Ex/Ey/Ez` 最大绝对值为 `3.912e-3/3.516e-3/9.149e-4 V/m`，与 x 向 sibling 形成分量置换对照；证据仍限定为短时低残余场。

2026-07-12 增补 Cartesian 2D Silver-Mueller x 证据：官方 2-rank、500 步 producer 与独立 contract 均通过，`Ex/Ey/Ez` 最大绝对值为 `9.149e-4/3.516e-3/3.912e-3 V/m`，均低于 `0.01 V/m`；该证据与 RZ Silver-Mueller 短时残余场合同并列，不替代系统反射率扫描。

2026-07-12 增补 3D PSATD-PML cleaning diagnostic semantics note：把 `ComputeDivE`、`DivBFunctor`、`DivEFunctor` 和 PML `F/G` 输出边界接回 clean/control report，明确本版不把 cell-centered native `divB` 对照升级为 strong cleaning physics gate。

2026-07-12 增补 3D PSATD-PML cleaning diagnostic semantics note：把 `ComputeDivE`、`DivBFunctor`、`DivEFunctor` 和 PML `F/G` 输出边界接回 clean/control report，明确本版不把 cell-centered native `divB` 对照升级为 strong cleaning physics gate。

2026-07-12 增补显式 `PECInsulator` 2D 证据：官方 2-rank、10 步 producer 后，独立 contract 验证初态场全零、上边界中段 `By` 相对 `3.3e-3` 输入误差 `1.54%<5%`、下边界 `By=0`；本版将其与 implicit Poynting ledger 分开归类。

2026-07-12 增补 `test_3d_pec_particle` 的 2-rank PEC-vs-periodic control 证据：全场 `max|E|` 比值 `0.0070491<0.01`、`Ey` 比值 `0.0022796<0.01`，两 species 粒子状态一致；证据范围限定为近 PEC 场抑制，不替代直接粒子 gather instrumentation。

2026-07-12 增补 `particles_in_pml` 2D AMR sibling：官方 `test_2d_particles_in_pml_mr` 2-rank、300 步运行与独立绝对值 contract 均通过，`max|E|=3.661057413095795e-4 < 6e-4`；2D 两档和 3D 单层已形成正向证据，3D AMR 的 signed-vs-absolute 判据分歧继续保留。

2026-07-12 增补 `particles_in_pml` 3D 证据：单层 2-rank 官方与独立 contract 通过，`max|E|=4.325973103094924 < 10`；3D AMR sibling 的官方有符号 gate 通过，但独立全场绝对值 gate 为 `110.3993781372607 > 110`，本版将其记录为判据边界而非强通过。

2026-07-12 增补官方 `test_2d_particles_in_pml` 2-rank 证据：180 步后官方 residual-field analysis 通过，独立全场绝对值 contract 得到 `max|E|=2.5542538436684726e-4 < 3e-4`；2D AMR、3D 单层随后补齐，3D AMR 的 signed-vs-absolute 判据分歧与 upstream checksum 边界继续保留。

2026-07-12 增补 RZ 三模态 case-local sibling：`n_rz_azimuthal_modes=3`、`dump_rz_modes=1`，验证 `m=1/2` 实虚分量非零，且 native theta=0 `Er/Ez` 与实模态重建误差分别为 `3.05e-16/2.53e-16`。官方 `analysis_rz.py` 仍是单模解析消费者，不用于该三模 sibling。

2026-07-12 又补入第 5 章 Esirkepov/Villasenor 出版级对照表：将论文第一性对象、现代 WarpX 入口和循环骨架并排固定，并把 `1/3/1/6` 的共享系数与不同算法语义区分开；本版仍不把公式级检查升级为所有分支的端到端等价证明。

2026-07-12 又补入第 7 章 PSATD-PML Cartesian/RZ 并列运行证据：Cartesian 低反射率为 `9.4704e-7`，RZ 径向 PML 末态残余场最大值为 `1.4793`；新增独立 reader-side 报告，并明确 1-rank 项目级复现不替代官方 2-rank CMake regression。

2026-07-12 又补入 transition-zone live source audit：在 WarpX commit `8c488b1a9` 上复核 `BuildBufferMasks`、`stablePartition`、`nfine_gather/nfine_deposit`、`Efield_cax/current_buf/rho_buf` 和 `SyncCurrent/SyncRho` 五组锚点全部通过，同时确认 dedicated route-count 实现仍不存在；本版不将该 audit 升级为 runtime regression。

2026-07-12 又补入 comoving 第一阶段 `finite + spike` 正/负 contract：stable baseline 的 `spike_ratio=1.1103719982074416` 通过阈值，no-comoving reference 的 `1.1119614945212388` 被阈值 `1.1114823702056489` 拒绝；energy gate 仍不纳入本版，因为 local calibration 尚未形成可靠 energy oracle。

2026-07-12 又补入 RZ JRhom LL2 first-stage repeated/MPI 正/负 contract：baseline energy ratio `0.9770894022295227` 通过 `0.9780664916317521` ceiling，no-time-averaging reference ratio `1.0` 被拒绝；该证据仍属于 project-level helper validation，目标 WarpX checkout 仍保持 `analysis=OFF`。

2026-07-12 又补入 `ParticleHistogram2D` BP5 weighted-moment sanity：记录 ions/electrons 在 iteration 0/100 的总权重、`z/uz` 均值和标准差，并明确该 reader-side 统计不等于更高分辨率/粒子数 convergence proof。

2026-07-12 又补入 `ParticleHistogram2D` 匹配物理时间的网格敏感性 contract：`384x512` baseline 与 `768x1024` refined producer 的总权重、`std(z)`、`std(uz)` 局部稳定性 gate 通过；随后以 `1x1/2x2/4x4/8x8` 趋势 contract 将 `1x1 -> 2x2` 作为预期低采样负对照、将 `2x2 -> 4x4` 与 `4x4 -> 8x8` 作为高粒子数局部通过。该结果仍不是正式 convergence order 或 upstream regression gate。

2026-07-12 又将 `ParticleHistogram2D` 粒子数敏感性扩展为 `1x1/2x2/4x4` pairwise contract：`1x1 -> 2x2` 电子总权重差 `1.9471e-3` 未通过，`2x2 -> 4x4` 降至 `4.2685e-4` 并通过总权重/`std(z)`/`std(uz)` 局部 gate；本版仍不声称正式 convergence order。
2026-07-12 又补做 `8x8` particles-per-cell sibling：`4x4 -> 8x8` 电子总权重差进一步降至 `3.6534e-4`，四档相邻比较的总权重、`std(z)`、`std(uz)` 局部 gate 均通过；8x8 producer 的 BP5 输出完整，MPI finalize 尾噪声仅限本机 OFI 收尾环境；本版仍不声称正式 convergence order 或 upstream regression gate。
2026-07-12 又重新完成 comoving PSATD 第一阶段目标 checkout 只读 preflight：audit/report/preview/dry-run 均成功，目标树仍为 `unstaged`，helper 缺失、CMake analysis 仍为 `OFF`，精确计划改动只有新增 helper 与一处 analysis wiring；本轮未修改 `../warpx`。详细证据见 `notes/code-reading/fieldsolver/34-comoving-target-checkout-preflight.md`。
2026-07-12 又为第 8 章新增 `scripts/plot_particle_histogram2d_particle_count.py` 与 `assets/figures/particle-histogram2d-particle-count.{png,pdf}`，生成图 8-12 展示四档 ParticleHistogram2D 相邻 pairwise 结果相对局部 gate 的归一化趋势；证据仍限定为单 case reader-side 统计。
2026-07-12 又为第 5 章补入 four/seven/ten-boundary 到 WarpX `earliest-crossing` segment loop 的 Mermaid 源码映射示意；该图明确是读者侧源码映射，不是论文原图，不替代 publisher figure-by-figure compare。
2026-07-12 又补入 implicit Villasenor 2-rank 运行级证据：2D JFNK `shape=2` case 的 energy/Gauss-law 官方与独立 contract 均通过，2D `shape=4` boundary-cropping sibling 的 Gauss-law contract 通过；RZ/1D sibling 的 PETSc 缺失与 `SIGILL` 边界均如实保留。
2026-07-12 又补入 implicit Villasenor filtered sibling：官方与独立 contract 均通过，显式确认 `warpx.use_filter=1`，能量相对变化 `3.8931e-15`、Gauss-law RMS `5.1401e-16`；该证据仍限定为 2D JFNK/filter 组合路径。
2026-07-12 又补入 implicit Villasenor PICMI sibling：Python-enabled `build_py` 下官方 2-rank producer 与独立 contract 均通过，生成输入确认 Villasenor/theta-implicit/shape=2，energy 相对变化 `4.0980e-15`、Gauss-law RMS `9.5730e-16`；保留 `newton.liner_solver` unused-input warning。
2026-07-12 又进一步定位 RZ implicit Villasenor blocker：官方 PETSc 路径因 `AMREX_USE_PETSC` 缺失拒绝，`amrex_gmres` control 又在 `ThetaImplicitEM::InitializeCurlCurlBCMasks()` 触发 `SIGILL`；RZ 未进入物理计算，边界记录见 `notes/code-reading/particles/47-rz-implicit-villasenor-build-boundary.md`。

2026-07-12 又补入 Villasenor-Buneman 可执行公式级 bounded check：`Eq.(6)-(9)` 四边界 flux、任意 crossing 分段位移以及 `Eq.(36)` 三维交叉项/体积闭合在 10000 组确定性样本上通过，二维最大残差 `4.4409e-16`、三维最大残差 `1.7764e-15`；证据等级仍是 paper-backed + source-grounded + formula-audited，不升级为所有 WarpX 分支的端到端等价证明。

2026-07-12 又重新核查 Esirkepov 2001 CPC access：官方 Elsevier API 确认发表 PII/cover date 并报告 `openaccess=0`，PDF 请求返回 HTTP `406` 未授权最小响应；publisher-PDF line-by-line compare 仍是权限缺口。

2026-07-12 又补入 3D PSATD-PML divergence-cleaning reader-side 对照：原生 `divE/divB` 输出与关闭 PML cleaning 的 control 均为 finite，但 core `divB` clean/control 比值 `12.7633`，因此只作为负/边界证据，不升级为强 cleaning physics gate。
- 2026-07-12 又补入官方 3D PSATD-PML 2-rank launcher 证据：`FI_PROVIDER=tcp` + MPICH `-n 2` 成功写出 native `divE/divB`；与 1-rank 对照时 `rho` 相对差 `9.31e-13`、`Ex` 最大相对差 `6.38%`，本版只收录 MPI producer coverage，不宣称 rank-invariant field contract。
- 2026-07-12 又补入同一 2-rank 分解上的 PML cleaning/control 对照：clean/control core Gauss residual `0.764365/1.274899`，core `divB` 比值 `12.8282`，与单进程方向一致；本版继续关闭强 cleaning physics gate。
- 2026-07-12 又补入官方 2D Cartesian PSATD-PML 2-rank 证据：初始能量相对误差 `1.45e-15`、末态反射率 `9.4704449758e-7 < 1e-6`，新增独立 reader-side contract；仍不把本地复现写成 upstream CMake checksum 的替代品。
- 2026-07-12 又补入官方 2D Cartesian PSATD-PML 2-rank restart 证据：从 `chk000150` 接续到 `diag1000300`，官方与独立 reader-side 对 `Bx/By/Bz/Ex/Ey/Ez/divE/rho` 的最大绝对/相对误差均为 `0.0`，通过 `1e-12` restart gate；该证据只支撑状态恢复一致性。
- 2026-07-12 又补入官方 `uniform_plasma` 3D 2-rank restart 证据：从 `chk000006` 接续到 `diag1000010`，官方与独立 reader-side 对 37 个 field 的最大相对误差为 `2.8631e-16 < 1e-12`；仓库 checksum 的 rank-specific 参考与本地 2-rank producer 最大相对差 `3.20e-2`，本版明确保留该边界，不把 restart field pass 写成 checksum pass。

2026-07-12 增补第 8 章可复现性矩阵：统一整理 Langmuir、uniform-plasma、FieldProbe、reduced diagnostics、ColliderRelevant、DifferentialLuminosity、ParticleHistogram2D 和 BeamRelevant 的 producer/MPI、项目级脚本、主要 gate 与 case-local 证据目录，并显式保留 coarse failure 与 binary mismatch 边界。

2026-07-12 增补 `BeamRelevant` 最小 3D 统计合同：保留官方 `initial_distribution` 的 beam 参数，在 case-local sibling 中只启用 beam 与 `BeamRelevant`，验证 24 列输出、截断高斯束 charge、横向 rms 和纵向截断 rms；新增 `scripts/analyze_beam_relevant_contract.py`。完整官方 input 因预编译 binary 与当前源码对 `maxwellian`/`maxwell_boltzmann` 的语义不一致而未作为通过证据。

2026-07-12 增补 `ParticleHistogram2D` writer 证据：运行 laser-ion 官方 2-rank application，官方 time-average analysis 通过；`PhaseSpaceIons`/`PhaseSpaceElectrons` 均写出 `0/100` 两个 BP5 openPMD iteration、`1000x1000` `uz-z` 网格和有限非零数据。新增 `scripts/analyze_particle_histogram2d_contract.py`，明确二维 reduced diagnostic 不走普通文本 schema，空 `.txt` sidecar 是预期边界。

2026-07-12 增补 `diff_lumi_diag` 解析谱证据：按官方 2-rank 配置完成 leptons、leptons+AMR 和 photons 三组 sibling，1D/2D differential luminosity analysis 均通过；新增 `scripts/analyze_diff_lumi_contract.py`，记录 1D/2D 误差、容差、最终 step、128 个能量 bin、128x128 openPMD 网格和 AMR level。

2026-07-12 增补 `collider_relevant_diags` 束流诊断合同：按官方 2-rank 配置真实运行并通过官方 `analysis.py`，确认 `ColliderRelevant` 的 chi/角度统计、`ParticleExtrema` 和 `dL/dt` 聚合均成立；新增项目脚本从 openPMD `rho_beam_e/rho_beam_p` 独立重建 `dL/dt`，与 reduced 输出的两个 iteration 均为零相对误差。

2026-07-12 增补 `LoadBalanceCosts` 并行诊断证据：按官方 2-rank 配置运行 Heuristic/Timers 两个 sibling，并复现 `LBC.txt` efficiency improvement gate；Heuristic 为 `0.625252 -> 1.000000`，Timers 为 `0.744780 -> 0.996162`。新增 `scripts/analyze_load_balance_costs_contract.py` 和 case-local 报告。

2026-07-12 增补第 8 章 reduced diagnostics 强对照：按官方 2-rank 配置真实运行 `test_3d_reduced_diags`，用官方 `analysis_reduced_diags.py` 比较 60 个 reduced observable 与 `diag1000200` plotfile 重算值；全部通过，非 field-energy 最大相对误差 `4.125e-13`，field-energy 相对误差 `2.483e-1`，低于官方专用 `0.3` 容差。

2026-07-12 增补第 8 章 restart 证据：真实运行 `uniform_plasma` 3D 2-rank 基线与 `chk000006` restart sibling，均接续到第 10 步；官方 `analysis_default_restart.py` 和项目脚本对最终 `diag1000010` 做 37 个 field 的逐字段比较，最大相对误差为 `2.8631e-16`，通过 `1e-12` gate。仓库 checksum API 的 rank-specific 参考与本地 2-rank producer 最大相对差为 `3.20e-2`，因此本版只宣称 restart field reproducibility，不宣称 checksum 通过。

2026-07-12 又补入 uniform-plasma 1-rank/2-rank consistency 负/边界证据：粒子总权重一致，但 field/particle/total energy 相对差为 `1.9379e-2/8.9170e-4/6.2269e-4`，physical-field 最大 L2 相对差 `1.0185`；本版关闭该 case 的 rank-invariant field contract。

2026-07-12 又将 Esirkepov `Eq.(23)` density-decomposition 检查扩展为可归档 contract：固定 seed `2001`、10000 组样本最大残差 `8.8818e-16 <= 2e-15`；本版仍把它限定为 paper-formula/algebra evidence，不把它写成 WarpX kernel regression。

2026-07-12 又补入 Esirkepov 当前 checkout source audit：`CurrentDeposition.H` 的 14 个 entrypoint、shifted-shape、归一化、三方向 prefix/difference/writeback 锚点全部通过；证据等级为 read-only source audit，不替代数值 kernel regression。

2026-07-12 又补入 Villasenor 当前 checkout source audit：`CurrentDeposition.H` 的 16 个 crossing/segment/fraction/`this_J*` writeback 锚点全部通过；证据等级为 read-only source audit，不替代数值 kernel regression。

2026-07-12 增补第 8 章 FieldProbe 诊断审计：按 WarpX 官方 2-rank CMake 配置重新运行 `field_probe` 2D 单缝衍射，并与 1-rank 结果对照；两种配置的 `FP_line.txt` 完全一致，但官方 `analysis.py` 的平均误差为 `3.6703%`，超过 `2.5%` gate。新增 `scripts/analyze_field_probe_diffraction.py` 和失败报告，当前不把该案例写成通过的 physics benchmark。

随后做了 FieldProbe 分辨率对照：将网格从 `lambda/16` 加密到 `lambda/32`，并把取样步从 500 调到 1000 以保持相同物理时间；官方口径误差降至 `0.3533%`，最大选点误差 `1.0414%`，通过 `2.5%` gate。该结果支持 coarse-grid 离散误差是原始失败的主因，不能把 refined case 的通过反写成原始官方 coarse case 已通过。

2026-07-11 又推进了第 8 章的 reader-side 验证：在项目内生成逐步诊断的 Langmuir 本地副本，得到 81 个 plotfile 快照，并用新增的 `scripts/analyze_langmuir_frequency_fit.py` 拟合目标模态频率；同时用 `scripts/analyze_uniform_plasma_conservation.py` 对 uniform-plasma 初末状态做粒子数、粒子权重、场能、粒子动能和总能量统计，并将 uniform plasma 延长到 100 步、形成 11 帧时间序列。随后真实运行 `energy_conserving_thermal_plasma` 1D/2D 两个 sibling 各 500 步并复现官方 reduced-energy 强 analysis，1D/2D 最大 `EF+EP` 漂移分别为 `3.009e-4` 和 `1.031e-4`，均小于 `3.000e-3`。结果已归档到 `runs/stage-c-validation/`，其中 Langmuir 的频率相对误差为 `3.595e-4`，uniform plasma 的粒子权重全程不变但长序列总能量末态变化 `1.387e-2`、最大绝对偏差 `2.518e-2`，所以后者仍是 reader-side 统计，而 thermal-plasma family 结果才是本轮可升级的强能量 gate。

## 定位

`v0.40` 是 `PIC-tutor` 的 deposition runtime-contract closure 版。它继承 `v0.39` 已经完成的 deposition paper-backed assets 基线，但这次不再把第 5 章停在“已有论文资产、正文仍需继续从 notes 吸收实现合同”的状态，而是进一步把 `SyncCurrentAndRho()`、boundary/source synchronization、`Langmuir + current_correction` 与 `vay_deposition` 的 regression 分工，以及 `Esirkepov` / `Villasenor` 在公式到 kernel 之间的几层关键 runtime contract 更直接地压回主文。当前模块的闭合点已经从“主文献到位”推进成“current deposition 主线的源码、论文与验证分层已经能在正文内部自洽闭合”。

本版仍不修改 `../warpx`。新增的核心事实是：第 5 章不再只是在源码层说明 `Direct / Esirkepov / Villasenor / Vay` 四条路径各自做什么，而是把 source-synchronization 的顶层分叉、fine/coarse 同步、`PEC` source-boundary、specialized `current_fp_vay` 路径、以及两条关键 regression 分别验证哪一层 contract 这些原先更依赖配套 notes 才完整成立的实现边界，也收进了正文。同时，`Esirkepov Eq.(23)` 与 `Villasenor Eq.(6)-(9)` 在 WarpX 当前 prefix-loop / segment-loop 结构里的程序化对应也进一步压细，从而把第 5 章从“paper-backed + source-backed”推进到更接近“runtime-backed”的可审读状态。

在当前这轮 `v0.40` 后续推进里，第 5 章又往前压了一小步：`Villasenor Eq.(6)-(9)` 不再只停在 “`Jx/Jz` 可读成主方向输运乘横向平均” 这种总括说法，而是补清了 `Jx1/Jx2` 与 `Jy1/Jy2` 的镜像角色；同时，论文 `Eq.(36)` 那组四项 `x`-face contribution 与现代 `3D` kernel 的 `old*old / old*new / new*old / new*new` 混合平均之间，也已经从“存在对应”推进到“可以解释局部耦合怎样分配到四个横向角点”的层次。这还不等于完成逐项核对，但它确实把 `Villasenor` 这条线从抽象结构映射推进到了更贴近论文公式本体的成书密度。

与此同时，charge deposition 这条线也补上了一层此前仍容易混淆的时间语义：现在正文已经明确区分 `MultiParticleContainer::DepositCharge(relative_time)` 的外层 `PushX()` 粒子位置平移，和 `WarpXParticleContainer::DepositCharge(..., icomp, ...)` 里 `time_shift_delta -> LowerCorner(...)` 的内层 Galilean 参考框架校正；并且补回了独立 `DepositCharge()` 在 `RZ / RCYLINDER / RSPHERE` 下还会在 species 汇总后统一做 `ApplyInverseVolumeScalingToChargeDensity(...)`。这使第 5 章对 charge deposition 的说明不再只是 bridge contract 摘要，而是开始把 “什么时候改粒子位置、什么时候改网格参考原点、什么时候再乘几何体积因子倒数” 讲成一条完整实现链。

这一轮继续往前压以后，charge deposition 的 shared-memory 特化路径也不再只是“知道有一条单独分支”。正文现在已经明确写清：`do_shared_mem_charge_deposition` 不走 ABLASTR `deposit_charge(...)`，而是先把粒子组织成 `DenseBins + shared_tilesize + max_tbox_size` 的 tile-binned 执行合同，再进入 `doChargeDepositionSharedShapeN<1..4>()`；与此同时，`max_tbox_size -> sample_tbox -> shared_mem_bytes <= sharedMemPerBlock` 这条 GPU shared-memory 容量检查也被压回了主文。这样第 5 章对 charge deposition 的覆盖开始同时包含普通 bridge contract 与 shared-memory 特化执行拓扑，而不再只偏向普通路径。

再往下走一步，这条线的低维几何语义也开始从“隐含在源码条件编译里”变成正文里的显式事实：`ChargeDeposition.H` 在 `1D_Z / RCYLINDER / RSPHERE` 下并不是简单沿用 3D 多维 shape 再少几层循环，而是先把粒子位置压成轴向或径向单变量，再只构造一维 `sz` 或 `sx` support；shared-memory 版本在这件事上与普通版本保持同构，改变的是执行拓扑，不改变这些几何分支本身的物理语义。这样第 5 章对 charge deposition 的描述就不再只覆盖时间层、bridge contract 和 shared-memory 拓扑，也开始覆盖低维 kernel 如何直接重写几何变量。

与此同时，`DepositCharge()` 的容器层接口边界也比之前更清楚了。正文现在已经把 `reset / local / apply_boundary_and_scale_volume / interpolate_across_levels` 四个开关分别钉回源码职责：它们控制的是清零、guard-cell 通信、沉积后几何/边界整理，以及多层 `fine -> coarse` average-down，而不是粒子到网格的局部 shape kernel 本身。这样第 5 章对 charge deposition 的叙述开始明确区分“局部 `rho` 怎么写出来”和“最终可供 Maxwell/diagnostics 使用的 `rho` 怎么经通信、边界和 AMR 整理完成”。

再推进一步以后，charge deposition 与 coarse-buffer/AMR 邻接的分层也更清楚了。正文现在已经明确写清：`PartitionParticlesInBuffers(...)` 会先把粒子切成 fine `rho_fp` 与 coarse-buffer `rho_buf` 两段，而 buffer 粒子不是先沉到 fine 再 restrict，而是一开始就通过 `DepositCharge(..., depos_lev = lev-1)` 直接按 coarse patch 几何沉积；相对地，多层接口里的 `interpolate_across_levels` 只是函数尾的 average-down 选项，运行时真正的 coarse/fine/buffer source 整理仍要依赖后面的 `SyncRho()` / `AddRhoFromFineLevelandSumBoundary(...)`。这样第 5 章开始把“直接沉积在哪一层几何上”和“沉积完成后怎样做 coarse/fine/source synchronization”明确拆成两层。

这一部分现在已经补上最后一层负面边界：`ChargeDeposition.H` 不是 current-deposition mover，它不恢复一步轨迹、不构造 `old/new` shape difference，也不选择 `Esirkepov / Villasenor / Direct / Vay`。`DepositCharge()` 这一支现在在正文里被收束为“单时间层 \(\rho\) 采样 + 时间层/AMR/几何桥接 + 外层同步整理”的合同：`icomp/time_shift_delta` 负责 old/new 网格参考原点，`relative_time PushX` 负责外层粒子位置取样，`depos_lev=lev-1` 负责 coarse-buffer 直接沉积，shared-memory 只改变执行拓扑，而 PEC、guard exchange、inverse-volume scaling 与 AMR average-down 都留在容器/通信层。这使 `DepositCharge()` / ABLASTR / `ChargeDeposition.H` 的主线达到 `v0.40` 内部阶段闭合。

在 `Esirkepov 2001` 这条线上，当前回合也把正文从“`Eq.(23)` 的局部公式映射”往“论文结构映射”推进了一步：本地预印本已经足以确认预印本标题与 CPC 发表版标题并不完全相同，也足以把预印本 `Section 2/3/4` 分别稳定对回 WarpX 的 continuity contract、`density decomposition` 三方向分解和二阶 spline 算法骨架。这样第 5 章对 Esirkepov 的依赖不再只是单条公式或单句唯一性 claim，而开始具备更完整的问题设定到 kernel skeleton 的 paper-backed 结构支撑。

2026-07-11 又对这条线做了一次 bounded compare：arXiv 页面核实了预印本提交日期、题名、13 页/无图/10 条参考文献等元信息，公开 CPC 书目信息核实了发表版题名、卷期、页码和 DOI，并将结果独立记录到 `notes/code-reading/particles/44-esirkepov-cpc-bounded-comparison.md`。这一步把 publication metadata 从“已知但散落在 access audit”提升为可直接引用的项目资产；但由于当前环境仍拿不到 publisher-formatted PDF，abstract、section numbering、`Eq.(23)` 排版和二阶 spline 段落的逐页 compare 仍保持未完成状态。

本轮又对 ScienceDirect 的直接 PDF 地址做了 browser-like 下载复核：搜索结果可发现 publisher endpoint，但浏览器侧进入 download-preparation error，本机 `curl -L` 返回 HTTP 403。因此第 5 章新增了证据矩阵，把 Section 2/3/4 的预印本全文与 WarpX 源码映射、CPC 书目/摘要元数据和仍待 publisher PDF 的四项正文 compare 分开列出；这提升了成书表达的可审计性，但不改变“publisher-PDF line-by-line compare 未完成”的状态。

在同一轮 publication-grade 精修中，第 5 章又新增了五条路径的责任边界矩阵：`Direct`、`Esirkepov`、`Villasenor`、`Vay` 和 `DepositCharge()` 分别按第一性对象、离散连续性目标、轨迹处理、WarpX 入口和外层职责并排对照。这个矩阵不是新的算法断言，而是把已经在各分节分别成立的 runtime contract 压成一个可复查的导航表，并同步修正 `5.15` 的剩余工作描述：charge deposition bridge 不再作为主要缺口，后续优先级回到论文证据、图表和出版级文字精修。

随后又把 Villasenor 的 crossing 语义图示化：正文新增 Mermaid 流程图和 four-/seven-/ten-boundary 对照表，把论文中的固定几何命名与 WarpX 当前 `cell_crossings_* -> num_segments -> earliest-crossing -> local this_J*` 的动态循环分开。图示明确表达了一个重要边界：seven/ten-boundary 不是现代源码中的固定 case label，而是 repeated segmentation 可能产生的论文级几何结果；源码真正的扩展性来自 crossing 计数和 segment loop。

在同一轮继续推进第 6 章后，又新增了 PSATD/场求解器算法族决策矩阵。矩阵把 FDTD、Cartesian standard/Galilean/comoving、JRhom、RZ standard/Galilean 与 PML 按谱基、源项时间模型、沉积/组合限制、系数族和当前验证证据并排组织，特别固定了两条防混写规则：Cartesian Galilean/average-field 的同名 `Y` 系数不能与 JRhom `Y1-Y8` 合并；RZ `Ep/Em` 也不能当作 Cartesian `Ex/Ey` 的简单别名。同时，comoving 和 RZ JRhom 的本地 helper/ledger 仍被明确写成 local validation 或 handoff 证据，不提前升级为 upstream 强物理 regression。

随后对 RZ JRhom first-stage bundle 的目标 checkout 做了只读 `audit/report/preview`：当前 `../warpx` 为 `unstaged`，helper 文件缺失，CMake analysis 仍为 `OFF`，精确 preview diff 只包含新增 `analysis_rz_jrhom.py` 和一行 analysis wiring。该结果写入 `notes/code-reading/fieldsolver/rz_jrhom_first_stage_target_report.md`，把“bundle 已准备好”和“已经写入 WarpX”明确拆开；本轮仍不修改 `../warpx`。

第 7 章也新增了 transition-zone 当前证据状态表：`BuildBufferMasks()`、`PartitionParticlesInBuffers()`、`E/Bfield_aux/cax` 和 `rho/current_fp/buf` 的源码合同已核对，现有 MR/Langmuir/PML regression 属于间接整体证据，而 `TransitionZoneRoutes`/route-count dedicated test 仍停留在 v0.15/v0.16 的 WarpX patch 设计，目标 checkout 中尚未实现。由此把第 7 章的准确边界固定为“源码已核、间接验证已核、专门 route proof 待实现”。

同一轮还完成了 LeeCPC2015 accepted-manuscript 的第一轮 materialization：eScholarship `49m2k3vj` 提供的 7 页 PDF 已进入论文专属目录，并经 MinerU 生成 Markdown、13 张图片和论文顺序中文讲解；第 7 章现在可以在 accepted-manuscript-backed + source-grounded 证据等级下解释 PML split-field、PSTD staggered shift、反射系数递推和高阶/PSTD 反射率结论。由于本地版本不是 publisher-formatted CPC PDF，`C1-C25`、Galilean `T2`、cleaning `F/G` 和 RZ PML 仍保持 WarpX 实现侧/专用扩展边界，不能直接归因给论文。

本版仍不是出版终稿。它继续保留 `Esirkepov 2001` 的 CPC 定稿 PDF 对照，也继续保留第 5 章后续 publication-grade 精修的现实边界。第 6 章 upstream handoff 和第 7 章 Lee/Vay 论文闭环同样未结束。后续应优先补齐 `Esirkepov 2001` 的发表版对照，并在不破坏当前主线闭合的前提下继续压缩第 5 章冗余、补图表和逐式核对，再考虑切往下一个成书主模块。

## 源码基线

- 本书项目仓库：`/Volumes/PHILIPS/programs/PIC/PIC-tutor`
- WarpX 只读源码：`../warpx`
- 当前 WarpX 分支：`pkuHEDPbranch`
- 当前 WarpX commit：`8c488b1a9`

v0.40 只修改 `PIC-tutor` 书稿项目，不修改 `../warpx` 原仓库。本版继续以 v0.39 已核定的第 5 章 paper-backed 资产为基础，推进 `manuscript/chapters/05-deposition-shapes.md`、`README.md`、`TODO.md`、`manuscript/README.md` 与版本说明的统一收口，并重建当前合订稿。后续若 WarpX 更新，必须重新校准源码行号、沉积入口和 regression 锚点后再发布新版。

## 历史 v0.40 章节范围（保留）

| 章节 | 文件 | v0.40 状态 | 下一步缺口 |
|---|---|---|---|
| 写作说明 | `chapters/00-preface.md` | 沿用 v0.1 | 需同步最终出版路线 |
| 动理学模型 | `chapters/01-kinetic-models.md` | v0.40 增补连续模型到 PIC 离散变量桥 | Hockney-Eastwood、Yee 等一手文献闭环未完成；仍需继续压紧与第 2 章的 leapfrog/CFL/色散衔接 |
| PIC 总循环 | `chapters/02-pic-loop.md` | v0.40 增补 AMR subcycling、JRhom 与 implicit 时间合同 | 仍需把基础文献和公式变量定义做出版级补齐，并继续压紧与第 3 章的调用链衔接 |
| WarpX 主演化路径 | `chapters/03-warpx-evolve.md` | v0.40 增补 `OneStep_sub1()`、JRhom、implicit 主调用链及 nonlinear/JFNK/mass-matrix `J` 构造边界 | 更细的 mass-matrix kernel 和场算法公式仍需分章展开 |
| WarpX 初始化链 | `chapters/03a-warpx-initialization.md` | 已做 v0.2 长草稿收束；v0.40 补入 native external-file Gaussian beam 的 1-rank 独立束斑合同 | 需要拆短小节、补流程图、压缩过长审计段落；官方 native `analysis.py` 缺失和完整 `initial_distribution` binary mismatch 仍需保留边界 |
| 粒子推进器 | `chapters/04-particle-pushers.md` | v0.40 增补 Higuera-Cary 运行级合同报告 | 仍需压缩多物理长段，并把 Boris/Vay 对照和更多 validation 表格图形化 |
| 沉积与形函数 | `chapters/05-deposition-shapes.md` | 已在 v0.40 把 current deposition 的 runtime/source-validation contract 进一步压回正文，并把 `DepositCharge()` / ABLASTR / `ChargeDeposition.H` 的 ordinary/shared-memory、time-level、low-dimensional geometry、coarse-buffer 与外层同步边界阶段性收口；Villasenor-Buneman 已完成论文公式级审计，并补入 2D implicit JFNK 的普通、filtered、shape=4 cropping 与 PICMI 运行级证据；RZ charge/inverse-volume 已有官方场/能量与独立全域电荷闭合证据 | 仍需为 `Esirkepov 2001` 补齐 CPC 定稿对照，并继续做记号统一、出版级表格精修和现代 geometry/order 分支逐项核对 |
| 场求解器 | `chapters/06-field-solvers.md` | 已补 Lehe/Kirchen/Godfrey 文献闭环、PSATD/NCI 源码机制对照表，并在 v0.26-v0.36 连续收口 comoving 与 RZ validation；v0.40 新增 1D semi-implicit/theta-implicit Picard sibling 运行级总能量合同、comoving 正/负 spike contract 和 RZ JRhom 2-rank 正/负 energy contract | 仍需决定是否真正在目标 WarpX checkout 上 staging 并上提 RZ JRhom helper；更细 solver family 仍需继续扩展 |
| 边界、PML 与 AMR | `chapters/07-boundaries-amr.md` | 已在 v0.25 增补 LeeCPC2015 论文-源码公式核对清单，并在 v0.40 完成 eScholarship accepted/submitted manuscript 的 MinerU、中文讲解和源码映射 | 仍需取得 publisher-formatted CPC PDF 做版本对照，并实现 dedicated transition-zone regression |
| 诊断、验证与案例 | `chapters/08-diagnostics-cases.md` | v0.40 已完成 reader-side、reduced diagnostics、多案例 physics/writer/performance gates、统一复现矩阵，并嵌入 Langmuir、energy-conserving thermal plasma、FieldProbe、reduced diagnostics、DifferentialLuminosity、LoadBalanceCosts、ColliderRelevant、ParticleHistogram2D 和 BeamRelevant 九组真实验证图；另补 native Gaussian external-file 项目级束斑 gate，并补齐 uniform-plasma 3D 2-rank restart field reproducibility | 仍需补更多可视化图表、完整 `initial_distribution` binary 匹配复现、ParticleHistogram2D 物理收敛性和更多边界/应用案例 |
| 文献路线 | `chapters/09-literature-roadmap.md` | 已改写为 evidence-tier 路线图，并把第 5 章最关键两篇 deposition 主文献更新到 paper-backed 状态 | 仍需继续消化 `docs/literature-map.md` 中可并入正文的旧条目，并推动下一批优先论文 materialize |
| 符号表 | `appendices/A-symbols.md` | v0.40 已扩展为连续模型、离散时间层、源码变量、诊断术语和缩写速查表 | 后续随新章节继续补充专用符号和单位 |

## v0.40 已完成的增量

- 冻结 `manuscript/VERSION-v0.39.md`，避免重建 v0.39 时误用 v0.40 版本说明。
- 新增 `scripts/build_v40.py`，生成 `dist/pic-tutor-v0.40.md`、自包含 MathJax 的 `dist/pic-tutor-v0.40.html` 与 `dist/pic-tutor-v0.40.pdf`；该条记录对应 279 页历史构建快照，当前页数由 `scripts/verify_v40_build.py` 固定验收，HTML 数学转换警告为 0。
- 把 `SyncCurrentAndRho()` 的 solver/algorithm 分叉、`current_fp_vay` 专用路径、fine/coarse source synchronization、`PEC` source-boundary 和两条关键 regression 的 contract 分层直接收回第 5 章主文，减少这部分解释对配套 notes 的依赖。
- 继续压细 `Esirkepov Eq.(23)` 与 `Villasenor Eq.(6)-(9)` 在 WarpX 当前 prefix-loop / segment-loop 结构中的 programmatic mapping，使论文公式、源码循环与 regression 语义三者在正文中能够直接互相对照。
- 继续把 `DepositCharge()` / ABLASTR / `ChargeDeposition.H` 的 bridge contract 压回第 5 章主文，补齐 ordinary/shared-memory、time-level、low-dimensional geometry、coarse-buffer 和外层同步职责边界。
- 新增第 6 章 PSATD/场求解器算法族决策矩阵，统一导航 FDTD、Cartesian standard/Galilean/comoving、JRhom、RZ standard/Galilean 与 PML 的谱基、源项时间模型、组合限制、系数族和验证证据等级，明确同名系数与 checksum 证据的边界。
- 第 8 章完成 Langmuir、uniform-plasma、FieldProbe、reduced diagnostics、ColliderRelevant、DifferentialLuminosity、ParticleHistogram2D 和 BeamRelevant 的运行级证据整理，新增项目级分析脚本、case-local JSON/Markdown 报告和统一复现矩阵；保留 coarse-grid physics failure、writer-only contract、binary mismatch 等边界。
- 第 1 章新增“从连续模型到 PIC 离散变量”桥接小节，将 `f/rho/J/E/B` 映射到粒子时间层、网格字段、fine/coarse source buffer 与 `SyncCurrentAndRho()`，并明确 `DepositCharge()`、current deposition、source synchronization 的三层职责。
- 第 2 章新增 AMR subcycling 时间合同，基于 `OneStep_sub1()` 固定两级/比例 2、细层两次推进、粗层一次推进、fine-to-coarse current/rho 合成、guard/auxiliary 可见性和 electrostatic 禁止组合边界。
- 第 2 章新增标准显式、PSATD-JRhom 与 implicit 时间推进对照，明确 `OneStep_JRhom()` 的多次相对时间沉积、`m_JRhom_subintervals`/time averaging、implicit `PreRHSOp()` 的粒子/source 重算，以及 `current_correction`、collision split push 和 RHS/物理时间步的边界。
- 第 3 章新增 implicit 主调用链：从 `WarpX::OneStep()` 进入 `SemiImplicitEM::OneStep()`、`m_nlsolver->Solve()`、`ComputeRHS()`、`PreRHSOp()`、`CumulateJ()`/mass matrices、`SyncCurrentAndRho()` 到最终粒子和磁场提交，明确 nonlinear iteration 不等于额外物理时间步。
- 第 3 章新增 implicit nonlinear/JFNK/mass-matrix 合同：将 `picard/newton/petsc_snes`、`J_suborbit + J0 + M·deltaE`、`CumulateJ()`、`ComputeJfromMassMatrices()`、staggering offset 以及 3D/RSPHERE 限制接回源码。
- 第 4 章新增官方 `particle_pusher` Higuera-Cary 运行级证据：10000 步末态 `max|x| = 1.1430664e-4 < 1e-3`，新增 `scripts/analyze_particle_pusher_contract.py` 与 case-local JSON/Markdown 报告，并明确该证据不等价于三种 pusher 的完整 benchmark；同时新增 `single_particle` velocity synchronization 运行级证据，`u_z` 相对误差为 `1.3237889e-16 < 1e-15`，完成 Boris/Vay/Higuera-Cary pusher-only sibling 对照，补入 `photon_pusher` 16-species 无质量传播/动量保持证据，并完成 `larmor` continuum orbit audit 但保留 checksum-only 边界。
- 第 8 章新增第一张真实验证图 `assets/figures/langmuir-field-vs-theory.png`，由 Langmuir 81 快照验证树生成，并在正文中明确区分波形图的 reader-side sanity check 与数值 gate。
- 第 8 章新增 `scripts/plot_energy_conserving_thermal_plasma.py` 和 `assets/figures/energy-conserving-thermal-plasma-1d-2d.png`，由 1D/2D case-local JSON 可重建 `EF+EP` 总能量/相对漂移图，并明确共同 `0.003` gate。
- 第 8 章新增 `scripts/plot_field_probe_resolution.py` 和 `assets/figures/field-probe-resolution-comparison.png`，由 resolution comparison JSON 可重建 coarse/refined 平均误差与最大选点误差图，并保留 `2.5%` physics gate、coarse failure 和 refined pass 的边界。
- 第 8 章新增 `scripts/plot_reduced_diags_error_layers.py` 和 `assets/figures/reduced-diags-error-layers.png`，由 reduced-diags contract JSON 可重建普通 observable 与 field-energy 特殊容差的误差分层图，并保留 `1e-12` / `0.3` 两组 gate。
- 第 8 章新增 `scripts/plot_diff_lumi_errors.py` 和 `assets/figures/diff-lumi-errors.png`，由三份 differential-luminosity contract JSON 可重建 1D/2D 误差与 case-specific gate 图，并保留 photons 独立容差。
- 第 8 章新增 `scripts/plot_load_balance_efficiency.py` 和 `assets/figures/load-balance-efficiency.png`，由 Heuristic/Timers 两份 LoadBalanceCosts JSON 可重建 before/after rank-level efficiency 图，并明确其属于性能 gate 而非物理精度 gate。
- 第 8 章新增 `scripts/plot_collider_luminosity_consistency.py` 和 `assets/figures/collider-dldt-consistency.png`，由 ColliderRelevant contract JSON 可重建两个 openPMD iteration 的 `dL/dt` reduced/full-state consistency 图，并保留“聚合定义一致性，不等于动力学 benchmark”的边界。
- 第 8 章新增 `scripts/plot_particle_histogram2d.py` 和 `assets/figures/particle-histogram2d-phase-space.png`，从 laser-ion BP5 series 读取真实 `PhaseSpaceIons/PhaseSpaceElectrons` iteration 0/100，生成 `uz-z` 相空间图，并保留独立颜色归一化、1000×1000 writer 和空文本 sidecar 边界。
- 第 8 章新增 `scripts/plot_beam_relevant_contract.py` 和 `assets/figures/beam-relevant-contract.png`，由 BeamRelevant contract JSON 可重建截断高斯束 charge 比值与 x/y/z rms 对照图，并保留初始化-only 和完整 binary mismatch 边界。
- 构建链修复 12 张图表的资源路径：章节源文件使用相对 `../assets/figures/`，合订 Markdown 在构建时映射到项目根 `manuscript/assets/figures/`，不再依赖本机绝对路径。
- `scripts/build_v40.py` 的 Pandoc/ XeLaTeX 子进程固定在项目根 `cwd=ROOT`；已从项目外 `/tmp` cwd 实测重建，保证绝对脚本调用不会因调用方目录变化而丢失图表资源。
- 新增 `scripts/verify_v40_build.py` 作为构建后验收入口，统一检查 PDF 页数/关键章节、12 张图表链接与 HTML 内嵌资源、图 8-1 至图 8-12、附录 A 和构建警告；当前 8 项断言全部通过。
- 更新 `README.md`、`TODO.md`、`manuscript/README.md` 与版本说明，把第 5 章当前状态统一标记为“deposition runtime-contract 已阶段性收口，后续重点切回 CPC 定稿对照、图表化和 publication-grade 精修”。

## 成书前必须补齐

- 每章记录最终采用的 WarpX commit，并避免同章混用未说明的历史行号。
- 每章补齐公式变量定义、参数入口、源码路径、行号和真实源码块。
- 至少为核心章节绑定一个 Example 或 Regression。
- 把 `docs/parameter-map.md` 和 `docs/example-regression-map.md` 中的资料条目回填为正文叙述。
- 按 `docs/paper-reading-workflow.md` 完成核心论文 MinerU 转换和中文讲解笔记。
- 建立稳定的 Markdown/HTML/PDF 构建流程；v0.40 已在本机 Pandoc + XeLaTeX + CJK 字体环境生成并审阅 PDF，其他环境仍需满足对应工具链条件。
- 继续清理历史 TeX 数学标记和 XeLaTeX 字体回退警告；当前 HTML 已通过嵌入式 MathJax 消除转换警告，PDF 中普通段落误用 `\\rho` 导致的两条缺字提示也已修复，当前构建日志无数学转换或缺字警告。
- 对 public GitHub 仓库中的 PDF 和运行产物做版权与体积审计。
- 已新增 `docs/public-repo-release-audit.md` 记录当前体积和发布边界；第三方论文 PDF 的逐项公开许可确认仍未完成。

## v0.40 构建方式

生成合订 Markdown、HTML 预览和 PDF：

```bash
python scripts/build_v40.py
```

构建后运行产物验收：

```bash
python scripts/verify_v40_build.py --build-log /tmp/pic-tutor-build-v40.log
```

生成的文件：

- `dist/pic-tutor-v0.40.md`
- `dist/pic-tutor-v0.40.html`（若本机存在 `pandoc`）
- `dist/pic-tutor-v0.40.pdf`（若本机存在 `pandoc`、`xelatex` 和可用 CJK 字体）

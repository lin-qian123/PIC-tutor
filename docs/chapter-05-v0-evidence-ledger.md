# 第 5 章历史证据台账

本文件保留 v0.75--v0.110 的逐次沉积验证记录、命令、分类和数值。它是项目证据层，不参与读者版书稿渲染；读者版将相同结论按算法选择、证据层级、RZ 轴向诊断和收敛研究组织。

### 5.14.3 v0.75 沉积算法选择矩阵：先看几何和时间层，再看守恒证据

前面各节已经分别解释了四个 current-deposition 家族，但读者在实际输入卡里首先面对的通常不是公式，而是“当前 case 应该选哪条路径”。下面的矩阵把选择顺序固定为：**geometry/grid 约束 -> explicit/implicit 时间层 -> source-side 守恒机制 -> 当前可引用证据**。

| 选择面 | Direct | Esirkepov | Villasenor | Vay |
|---|---|---|---|---|
| 离散目标 | 速度加权源项；不自动闭合离散连续性 | old/new shape difference + prefix decomposition | crossing-defined segment-local flux | 专用两阶段 `D`-field 组织 |
| 轨迹输入 | 当前时间层速度 | old/new endpoint 与 shifted shape | endpoint reconstruction、cell crossing、segment fraction | explicit push 与专用 `D` 字段 |
| explicit/implicit | 两者均有，但守恒属性不同 | explicit/implicit 两条前端；论文主干对应 explicit | explicit/implicit 共享 segment backend，端点恢复不同 | 当前 checkout 为 explicit-only |
| 典型源码入口 | `doDepositionShapeNKernel` | `doEsirkepovDepositionShapeN` / `doChargeConservingDepositionShapeNImplicit` | `doVillasenorDepositionShapeNExplicit` / `Implicit` | `doVayDepositionShapeN` |
| 主要限制 | near-boundary 与 charge-conservation 不能由 direct 推出 | collocated/shared-memory/部分几何分支有 guard；publisher PDF 仍缺 | crossing 与 geometry/order 组合需逐项验证 | 当前 `Vay + AMR` 在初始化阶段显式拒绝 |
| 当前证据 | 适合作为非守恒对照 | preprint + source + Langmuir/geometry contracts | full-text + formula audit + source contract | source/runtime family contracts |

因此输入卡的排查顺序不应是“看到 `Villasenor` 就认为一定更精确”，而应是：

1. 先确认 geometry、grid staggering、AMR 和 shared-memory 路径是否允许该算法；
2. 再确认 explicit/implicit 前端提供的轨迹端点和时间层是否满足 kernel 合同；
3. 最后才用 `divE-rho/epsilon_0`、charge observable 或专门 energy gate 判断当前 case 的结果。

这一矩阵还给出三条负面结论。第一，`psatd.current_correction` 可以修正源项的离散连续性/Gauss-law 关系，但不把 Direct 自动变成 Esirkepov 或 Villasenor。第二，Esirkepov 与 Villasenor 都可能出现 `one_third/one_sixth` 或 old/new 平均，但前者是 whole-orbit density decomposition，后者是 segment-local transverse flux；相同系数不代表相同算法。第三，任何单一 Langmuir PASS 都不能外推到 RZ axis、AMR、boundary crop、shared-memory 或全部 shape/order family。

本节由 `scripts/audit_deposition_algorithm_selection_contract.py` 对当前 WarpX 分派源码、geometry/AMR guard、章节矩阵和代表性 runtime contract 做只读验收。它的分类是 `SOURCE_AND_RUNTIME_SELECTION_MATRIX_WITH_EXPLICIT_BOUNDARIES`：证明读者侧选择矩阵与当前 checkout 及已有证据目录一致，不宣称四种算法拥有同等的 physics coverage。

### 5.14.4 v0.78 沉积证据梯度：论文公式、源码入口与 runtime consumer

选择矩阵回答“应该选哪条算法”；本节进一步回答“当前证据究竟证明到了哪一层”。对沉积算法，论文公式、源码 loop 和运行级 consumer 不是同一个证据对象，必须分别列出。尤其是公式恒等式通过，不等于当前 kernel 的所有 geometry/order 分支都通过；单个 Langmuir case 通过，也不等于论文公式已经逐式映射到每个入口。

| 算法/证据族 | 论文或公式层 | WarpX 源码层 | runtime consumer | 当前可支持结论 | 明确不能外推 |
|---|---|---|---|---|---|
| Direct | 作为非守恒对照，只有通用 shape/current 公式 | `doDepositionShapeNKernel`，由 `DepositCurrent()` 分派 | Direct/Langmuir 对照输入 | 可以说明普通 current kernel 的输入输出路径 | 不能把 `psatd.current_correction` 写成 Direct 已具备 Esirkepov/Villasenor 的守恒算法 |
| Esirkepov | 预印本 `W^1/W^2/W^3`、`Eq.(23)`、`1/3,1/6` density decomposition；发表版摘要级主张已核实 | `doEsirkepovDepositionShapeN`、`sdxi/sdyj/sdzk`、`one_third/one_sixth` | density-decomposition algebra、source crosswalk、Langmuir/shape/geometry family | 预印本公式与当前 kernel skeleton 有可审计对应，代表性 Cartesian/RZ/径向 contracts 可分层引用 | 不能写成 CPC 定稿逐式已核对，也不能把代表性 family 外推为完整 geometry/order/AMR product |
| Villasenor-Buneman | full-text 的 four-boundary、crossing segmentation、3D mixed term | `VillasenorDepositionShapeNKernel`、`cell_crossings_*`、`num_segments`、`earliest-crossing` | formula contract、source contract、2D implicit JFNK/cropping/filter/PICMI | 论文局部几何闭合、源码 segment skeleton 和代表性 2D implicit consumer 三层均有独立证据 | 不能把 RZ pre-physics boundary 或 2D PASS 外推成 3D/RZ/全部 shape/order 的 runtime 等价 |
| Vay | 论文算法背景与当前实现的选择边界 | `doVayDepositionShapeN`，PSATD-only/AMR/RZ/1D guards | 2D/3D shape family 单进程与 2-rank official-scale contracts | 当前 checkout 的 Cartesian shape family 有 runtime consumer，且 guard 已明确 | 不能把 case-local sibling 写成上游注册项，也不能宣称 Vay + AMR 或正式收敛阶已完成 |

因此本节的分类为 `DEPOSITION_PAPER_SOURCE_RUNTIME_GRADIENT_WITH_EXPLICIT_GAPS`。它把每一行的 producer 和 consumer 绑定到不同证据层：`verify_esirkepov_density_decomposition.py` / `villasenor_formula_contract.py` 是公式层，`audit_*_source_contract.py` 是源码层，Langmuir、implicit JFNK 和 Vay shape-family contracts 是运行层。三层同时出现时，结论仍只覆盖表中写明的 scope；缺少某一层时，正文必须降级为 `PREPRINT_SOURCE_GROUNDED`、`FORMULA_ONLY`、`SOURCE_ONLY` 或 `RUNTIME_FAMILY_ONLY`。

本节由 `scripts/audit_deposition_evidence_gradient_contract.py` 验收。该合同只检查章节矩阵、当前 WarpX 只读源码锚点和代表性报告是否一致，不把证据目录数量当作物理覆盖率，也不改变上游 WarpX 仓库。

### 5.14.5 v0.79 收敛研究就绪合同：先固定 observable，再谈阶数

当前 RZ Esirkepov shape=1 已有 `64x128`、`128x256`、`256x512` 三档 2-rank case-local 控制。它们足以计算描述性的 pairwise order，但还不足以把结果写成正式收敛阶：`correction-on` 的轴向 charge residual 从 `3.593e-3` 降到 `7.554e-4`，而 `correction-off` 的 charge residual 在第三档反而超过 `1e-11` gate；`Er/Ez` 误差的 pairwise order 也不是稳定常数。

| 研究层 | 当前数据 | 可写结论 | 仍缺什么 |
|---|---|---|---|
| resolution family | RZ、shape=1、2-rank、三档各向同比例细化 | 几何与 resolution family 已固定，可以开始收敛研究 | 独立控制 particle count、时间步、边界和 axis treatment，确认误差源没有随网格一起改变 |
| field observable | `Er/Ez` relative error | 可报告每一对 refinement 的描述性 order | 需要稳定的 exact/reference 解、统一 norm 和至少更长的 refinement family，不能只凭单调下降 |
| charge observable | all-cell、axis、off-axis residual | 能识别 axis correction 与 off-axis 行为的分离 | correction-on 的 axis residual 仍远高于 `1e-11`，charge 不能被 field PASS 代替 |
| formal-order claim | 当前未成立 | 合同把“可计算”与“可宣称”分开 | 需要预注册 observable、误差范数、控制变量、拟合区间和重复/独立 family |

因此本节分类为 `CONVERGENCE_READINESS_WITH_FORMAL_ORDER_UNPROVEN`。该合同从既有三档数据计算 pairwise order，并检查 refinement ratio、observable 分层、axis-charge 边界和正文负面声明。

合同脚本：`scripts/audit_deposition_convergence_readiness_contract.py`。输出是研究入口，不是新的 physics PASS；尤其不能把 `correction-on` field trend 写成默认 axis charge 已修复，也不能把经验 order 当作论文或 WarpX 的正式收敛阶。

### 5.14.6 v0.83 独立几何趋势合同：RZ 与 RSPHERE 分开拟合

为避免把单一 RZ family 的趋势误读成通用规律，本版又把既有 `RSPHERE` 64/128/256 三档 paired controls 纳入独立几何对照。`RZ` 与 `RSPHERE` 分别计算 `Er`/`relative Er`、axis residual 和 off-axis residual 的两段描述性 slope；两条 `correction-on` axis residual 都随分辨率下降，而 correction-off 对照保留非单调或边界行为。

| 几何 | refinement family | 当前观察 | 不能写成 |
|---|---|---|---|
| RZ | `64x128 -> 128x256 -> 256x512` | correction-on axis residual slope 为 `1.241/1.008`；field slope 仍不稳定 | RZ 默认 charge 已闭合或已有正式 order |
| RSPHERE | `64 -> 128 -> 256` | correction-on axis residual slope 为 `1.583/1.747`；off-axis slope 为 `1.413/1.778` | spherical geometry 与 RZ 共享一个 universal order |
| cross-geometry | 两个独立 family，分开拟合 | 增加了独立 resolution-sensitive evidence，并保留 negative control | 把两种几何的数据 pooled 成一个收敛阶 |

该合同分类为 `EXPLORATORY_CROSS_GEOMETRY_RESOLUTION_TRENDS_FORMAL_ORDER_UNPROVEN`，报告见 [cross-geometry raw contract](runs/stage-c-validation/cross-geometry-convergence-trends/contract.json)。

合同脚本：`scripts/audit_cross_geometry_convergence_trends.py`。它推进的是正式 study 的独立 family 设计和负对照边界，不关闭 `STUDY-FORMAL-CONVERGENCE`，也不改变默认 axis correction 或任何 WarpX 参数。

### 5.14.7 v0.84 正式收敛 study 预注册合同

v0.84 将“下一步要做什么”进一步固定成预注册，而不是在观察到 slope 后再选择解释。`RZ` 与 `RSPHERE` 是两个独立 geometry unit；每个 unit 分别保留 `correction=on/off`、`64/128/256` 三档、全部相邻 pairwise fit interval，以及 axis/off-axis charge residual 的分层。field norm 固定为 `max(abs(numerical - analytic)) / max(abs(analytic))`，charge norm 固定为 `max(abs(divE - rho/epsilon_0)) / max(abs(rho/epsilon_0))`，不允许用 all-cell residual 替代 axis residual。

预注册关闭条件还要求每种 geometry 至少有两组独立产生的 family，并固定 density、`epsilon`、`w0`、domain、final time、particle shape、deposition、MPI layout 和 reader-side norm。`correction=off` 只能作为负对照，不能用来事后挑选有利的拟合区间；两种 geometry 禁止 pooled fit。两组 family 已 materialize，v0.95 又为 correction-on 的 repeat slope 固定 `1e-8` 容差，但 axis charge 仍是 boundary，因此 formal closure 仍为 `OPEN`，分类为 `FORMAL_CONVERGENCE_REPEAT_SLOPE_GATE_PREREGISTERED_CHARGE_CLOSURE_OPEN`。

预注册文件见 [formal convergence specification](docs/formal-convergence-preregistration.json)，原始报告见 [preregistration raw contract](runs/stage-c-validation/formal-convergence-preregistration/contract.json)。

合同脚本：`scripts/audit_formal_convergence_preregistration.py`。该合同推进实验设计的可重复性，不把现有 descriptive slope 升格为正式收敛阶，也不改变任何 WarpX 源码或默认参数。

### 5.14.8 v0.85 第二组 family 的执行前提

第二组 family 的执行流程已经固化为 `scripts/run_formal_convergence_repeat_family.py`。它声明 RZ/RSPHERE 两种 geometry 在 `64/128/256` 三档、`correction=on/off` 下共 12 个 2-rank producer，复用已经核对过的输入模板和 `build_full` binary，并在每个 run 目录单独保存 `producer.log`。脚本默认只做 preflight；真正执行必须发现 `mpiexec` 或 `mpirun`，并始终使用 `-n 2`。

当前机器的二进制和 12 组输入模板均存在；默认 shell `PATH` 没有暴露 MPI launcher，但显式使用 Conda 环境提供的 `mpiexec` 并设置 `FI_PROVIDER=tcp` 后，12/12 producer 均返回码为 0。未设置 provider 时，12 组会在 WarpX 已 finalized 后触发 `utun6` 上的 OFI finalize 错误，不能作为 execution pass；因此 provider 被记录为运行合同的一部分。报告见 [current execution contract](../../docs/formal-convergence-repeat-family-v0.92.md) 和 [raw contract](../../runs/stage-c-validation/formal-convergence-repeat-family-v0.92-tcp/contract.json)。
<!-- REPEAT_FAMILY_RUNNER_BLOCKED_MPI_LAUNCHER_MISSING -->

### 5.14.9 v0.94 第二组 family 的输入与产物合同

v0.86 将 runner 的“可启动”与“产物可用”分开检查。执行前，脚本逐个核对 12 个模板的 `inputs`、`FILE = ...` 引用文件、`diag_type = Full` 和 diagnostics `intervals`；因此目录存在不再等价于输入可运行。执行时仍固定使用 `mpiexec -n 2` 或等价的 `mpirun -n 2`，不允许降级为单进程。执行后，每个 producer 必须同时满足退出码为 0、生成 `producer.log`、生成 `warpx_used_inputs`，并在 `diags/` 下至少出现一个 `diag*` 目录。任何一项缺失都分类为“输入或产物合同不通过”，而不是把命令启动成功写成有效 runtime evidence。
<!-- REPEAT_FAMILY_RUNNER_BLOCKED_INPUT_OR_OUTPUT_CONTRACT -->

v0.92 已将第二组 family 实际执行结果与第一组 materialized family 用同一 reader-side norm 重算：RZ 的 `Er/Ez/axis/off-axis`、RSPHERE 的 `Er/axis/off-axis` 均覆盖 `64->128` 和 `128->256` 两个相邻 pair，且不做跨 geometry pooled fit。报告见 [second-family slope comparison](../../runs/stage-c-validation/formal-convergence-second-family-v0.92/contract.{json,md})，说明见 `notes/code-reading/particles/74-formal-convergence-second-family.md`。两组 slope 数值几乎重合，但原预注册没有给出可执行的 repeat-slope 数值容差，且 correction-on axis charge 仍是 boundary，因此本节只关闭第二组 producer 与 slope materialization，不关闭正式 order 或 charge boundary。

合同实现见 `scripts/run_formal_convergence_repeat_family.py` 与 `scripts/analyze_formal_convergence_repeat_family.py`；未设置 `FI_PROVIDER=tcp` 的默认 MPICH provider 会在 finalize 阶段触发 `utun6` OFI 错误，不被算作有效 execution pass。

### 5.14.10 v0.92 第二组 family slope 对照

第二组 family 的 12 个 2-rank producer 已经真实落盘并通过退出码、used-inputs 与 diagnostics 三层合同。RZ/RSPHERE 各自保留 `correction=on/off`，每种 geometry 的两个 family 都覆盖 `64/128/256`，因此“第二组尚未 materialize”这一前置缺口已经关闭。reader-side 分析没有把两种 geometry 合并：RZ 继续使用 `Er/Ez/axis/off-axis`，RSPHERE 使用 `Er/axis/off-axis`，全部相邻 pair 都保留。

这一步仍不是正式收敛阶闭合。v0.95 已在 `docs/formal-convergence-preregistration.json` 中固定 `1e-8` 的 absolute slope-delta tolerance，并对 correction-on 的全部 14 个 RZ/RSPHERE comparisons 执行 gate；correction-off 因接近 numerical/reader floor 继续只作 descriptive negative control。正式 order 解释和 correction-on axis charge correctness 仍保持独立开放。

### 5.14.11 v0.94 axis charge repeat stability

在两组 family 都 materialize 后，不能只看它们的 slope 是否相近，还要确认 correction-on 的 axis residual 是否在独立 producer 间稳定。v0.93 对 RZ/RSPHERE 的 `64/128/256` 六个 correction-on level 计算两组 axis residual 的相对差，固定 `1e-10` reader-side repeat gate，并同时要求两组的 axis residual 都高于 off-axis residual；六个 level 全部通过。该结果分类为 `REPEAT_STABLE_AXIS_CHARGE_BOUNDARY_NOT_KERNEL_ROOT_CAUSE`，报告见 `runs/stage-c-validation/rz-axis-charge-repeat-stability-v0.94/contract.{json,md}`，说明见 `notes/code-reading/particles/75-rz-axis-charge-repeat-stability.md`。

correction-off 的 RZ residual 已接近数值地板，因此该负对照只报告绝对值与放大的相对差，不把它混入 correction-on stability gate。这个合同只证明 correction-on axis boundary 在两组 family 中可重复、且仍高于 off-axis；它不识别 kernel root cause，不关闭 current closure，也不把稳定 boundary 改写成正式收敛阶。

### 5.14.12 v0.95 repeat-slope comparison gate

v0.95 将“两个 family 的 slope 几乎重合”改写成可执行的预注册比较：对 RZ/RSPHERE、correction-on、每个声明的 field/axis/off-axis observable 和 `64->128`、`128->256` 两个区间，逐项计算第一、第二 family 的 pairwise `log2` slope 绝对差。这里的 repeat-slope comparison tolerance 固定为 `1e-8`。14 项全部通过，最大差为 `2.587e-11`。报告见 `runs/stage-c-validation/formal-convergence-repeat-slope-gate-v0.95/contract.{json,md}`，说明见 `notes/code-reading/particles/77-formal-convergence-repeat-slope-gate.md`。

这里的 PASS 只表示 repeat-family consistency。correction-off 的最大 slope 差为 `1.996e-3`，但其 residual 已接近 numerical/reader floor，因此不进入 gate，只保留为负对照。该合同不宣称唯一 formal numerical order，也不关闭 axis charge correctness；当前分类为 `FORMAL_CONVERGENCE_REPEAT_SLOPE_GATE_PASS_CHARGE_CLOSURE_OPEN`。

### 5.14.13 v0.95 axis charge 源码-诊断交叉审计

v0.93 的 repeat stability 只能说明 axis observable 在独立 producer 间稳定；v0.94 继续沿源码路径拆分它的消费者边界。`PhysicalParticleContainer` 将粒子写入 `rho_fp`，transition-zone 粒子直接写入 coarse-geometry 的 `rho_buf`；完成 deposition 后，`WarpXEvolve.cpp` 才调用 `ApplyInverseVolumeScalingToChargeDensity(...)`，而 `WarpXPushFieldsEM.cpp` 根据 `verboncoeur_axis_correction` 选择 RZ axis volume factor。该步骤属于沉积后的外层几何归一化，不是 `ChargeDeposition.H` 内部的局部 shape 写入。

`divE` 走另一条路径：`WarpX::ComputeDivE()` 由 FDTD 或 PSATD solver 从 `Efield_aux` 计算临时场，`DivEFunctor` 再按 RZ 的 node/cell location 和 diagnostic coarsen 规则输出；`RhoFunctor` 则重新取 charge density，执行 boundary/filter 与 `InterpolateMFForDiag(...)`。`FullDiagnostics.cpp` 将两者注册为独立 functor，因此最终比较的 `divE-rho/epsilon_0` 同时包含 solver divergence stencil、RZ location/mode 处理、rho-side volume scaling 与 diagnostic resampling。

当前 13/13 个源码锚点通过，分类为 `SOURCE_DIAGNOSTIC_DISCRETIZATION_BOUNDARY`。这条证据支持“稳定的 axis/diagnostic boundary”，但不支持 `KERNEL_ROOT_CAUSE`；在没有 raw rho、volume-scaled rho、solver-native divE 和 converted divE 四类中间量前，本章不把 residual 归因到 deposition kernel。合同见 `runs/stage-c-validation/rz-axis-charge-source-diagnostic-crosswalk-v0.94/contract.{json,md}`，源码说明见 `notes/code-reading/particles/76-rz-axis-charge-source-diagnostic-crosswalk.md`。

### 5.14.14 v0.98 axis divergence stencil alignment

为了继续拆开 `divE` 这一侧，本版直接读取当前 RZ CKC/Yee 末态的 axis `Er/Ez/divE`，并回到 `../warpx/Source/FieldSolver/FiniteDifferenceSolver/ComputeDivE.cpp` 的 axis 分支。源码在 `r=0` 对 mode-0 明确写入 `4._rt*Er(i,j,0,0)/dr + DownwardDz(Ez,...)`，也就是 `4*Er/dr + DownwardDz(Ez)`；因此这里不能用普通 cell-centered 的 `2*Er/dr` 作为对照算子。独立 reader 先用同一阶的纵向差分从 `divE` 中减去 `Dz(Ez)`，再比较 `2*Er/dr` 与源码的 `4*Er/dr`。

| case | naive `2*Er/dr` RMSE | source `4*Er/dr` RMSE | 结论 |
|---|---:|---:|---|
| correction-on | `2.5968e14` | `1.7287e13` | source coefficient closer |
| correction-off | `2.5999e14` | `1.2638e14` | source coefficient closer |

两个 case 都支持更窄的 `RZ_AXIS_STENCIL_ALIGNMENT_OBSERVED_CHARGE_BOUNDARY_OPEN` 结论：axis `divE` 的数值语义确实包含源码定义的 `4*Er/dr` 正则化，朴素 `2*Er/dr` 不能作为 residual root-cause oracle。这个结果仍不是 charge PASS，也不能单独证明 rho-side inverse-volume scaling、mode/interpolation 或 deposition kernel 没有误差；它只是把 solver-native axis stencil 从“可能因素”推进为“已由 source + reader 对齐观察到的因素”。报告见 `runs/stage-c-validation/rz-axis-divergence-stencil-v0.98/contract.{json,md}`，说明见 `notes/code-reading/particles/79-rz-axis-divergence-stencil-alignment.md`。

### 5.14.15 v0.99 axis stencil cross-resolution alignment

为了避免把 v0.98 的两个 `256x512` 末态误读成单一分辨率现象，本版对已有的 `64x128`、`128x256` 和 `256x512` correction-on/off family 重复相同的独立 reader 算子。6/6 个 case 中，源码 `4*Er/dr` 的 RMSE 都低于 naive `2*Er/dr`：

| correction | grid | naive RMSE | source RMSE |
|---|---:|---:|---:|
| on | `64x128` | `2.7752e14` | `3.7296e13` |
| off | `64x128` | `2.7615e14` | `1.6705e14` |
| on | `128x256` | `2.2645e14` | `6.6455e13` |
| off | `128x256` | `2.2721e14` | `2.9943e13` |
| on | `256x512` | `2.5968e14` | `1.7287e13` |
| off | `256x512` | `2.5999e14` | `1.2638e14` |

因此本版把结论收窄为 `RZ_AXIS_STENCIL_ALIGNMENT_CROSS_RESOLUTION_OBSERVED_CHARGE_BOUNDARY_OPEN`：source-defined axis stencil 的对齐观察跨这三档 resolution 保持，但 residual 仍混合 longitudinal stencil、location/mode、rho-side scaling 与 diagnostic conversion，不能升级为 charge closure 或 deposition-kernel root cause。合同由 `scripts/analyze_rz_axis_divergence_resolution_contract.py` 生成，报告见 `runs/stage-c-validation/rz-axis-divergence-resolution-v0.99/contract.{json,md}`，说明见 `notes/code-reading/particles/80-rz-axis-divergence-resolution-alignment.md`。

### 5.14.16 v0.100 axis divergence fitted coefficient

本版再对同一组 6 个 correction-on/off resolution case 做无偏最小二乘拟合，令 reader-side longitudinal subtraction 后的 axis radial term 满足 `D_r^obs ~= a*Er/dr`。6/6 个拟合系数均更接近源码系数 `a=4` 而非 naive `a=2`：

| correction | grid | fitted `a` | `|a-2|` | `|a-4|` |
|---|---:|---:|---:|---:|
| on | `64x128` | `4.308992` | `2.308992` | `0.308992` |
| off | `64x128` | `3.246228` | `1.246228` | `0.753772` |
| on | `128x256` | `3.550571` | `1.550571` | `0.449429` |
| off | `128x256` | `3.773158` | `1.773158` | `0.226842` |
| on | `256x512` | `3.886482` | `1.886482` | `0.113518` |
| off | `256x512` | `3.346320` | `1.346320` | `0.653680` |

因此本版进一步使用 `RZ_AXIS_STENCIL_FIT_COEFFICIENT_CROSS_RESOLUTION_OBSERVED_CHARGE_BOUNDARY_OPEN` 分类：独立拟合支持 source-defined axis operator，而不是普通 `2*Er/dr` 连续近似。它仍只是 solver-native operator alignment，不关闭 rho-side scaling、deposition kernel、diagnostic location/mode 或完整 charge closure。合同由 `scripts/analyze_rz_axis_divergence_fit_contract.py` 生成，报告见 `runs/stage-c-validation/rz-axis-divergence-fit-v0.100/contract.{json,md}`，说明见 `notes/code-reading/particles/81-rz-axis-divergence-fitted-coefficient.md`。

### 5.14.17 v0.101 rho-side axis correction ratio boundary

本版把问题继续移到 rho-side：读取既有三档 resolution 的 correction-on/off `diag1000000`，比较 `rho_electrons` 与 `rho_ions` 的轴和 off-axis 比值。6 个 field/case 组合的 off-axis 比值严格为 `1`，而 axis 比值严格稳定为 `0.85`。源码 `ApplyInverseVolumeScalingToChargeDensity` 对 RZ axis 使用 correction-on `1/3`、correction-off `1/4`；只按这两个外层体积因子预测的 ratio 是 `0.75`。

| correction pair | grid | field | axis on/off | off-axis max deviation |
|---|---:|---|---:|---:|
| on/off | `64x128` | `rho_electrons` | `0.850000` | `0` |
| on/off | `64x128` | `rho_ions` | `0.850000` | `0` |
| on/off | `128x256` | `rho_electrons` | `0.850000` | `0` |
| on/off | `128x256` | `rho_ions` | `0.850000` | `0` |
| on/off | `256x512` | `rho_electrons` | `0.850000` | `0` |
| on/off | `256x512` | `rho_ions` | `0.850000` | `0` |

因此本版新增 `RZ_RHO_AXIS_CORRECTION_RATIO_MISMATCH_BOUNDARY_OPEN`：axis rho 的 correction-on/off 比值跨分辨率稳定，但不能由 `1/3` 与 `1/4` 外层体积因子单独解释。这个结果将剩余诊断边界进一步压到轴向沉积/镜像、rho 重建、mode/位置转换或输出时序；它仍不是 charge closure，也不是 deposition-kernel root-cause 证明。合同由 `scripts/analyze_rz_rho_axis_correction_ratio_contract.py` 生成，报告见 `runs/stage-c-validation/rz-rho-axis-correction-ratio-v0.101/contract.{json,md}`，说明见 `notes/code-reading/particles/82-rz-rho-axis-correction-ratio-boundary.md`。

### 5.14.18 v0.102 rho-side scaling 前 axis 输入边界

v0.102 继续展开 `0.85`/`0.75` 差异，而不是把它直接归因于体积因子。WarpX 当前源码显示，species `rho` 诊断经 `RhoFunctor` 请求 `WarpXParticleContainer::GetChargeDensity`，该路径以 `apply_boundary_and_scale_volume=true` 调用 `DepositCharge`；`ApplyInverseVolumeScalingToChargeDensity` 在轴上先执行负半径 guard-cell wrap，再除以 `pi*dr*axis_volume_factor`。因此最终 on/off 比值满足 `R_final = R_pre * ((1/3)/(1/4))`，现有 `R_final=0.85` 反推出 scaling 前 axis 输入比值为 `1.133333`。

| grid | field | final axis on/off | inferred pre-scaling axis on/off | off-axis max deviation |
|---:|---|---:|---:|---:|
| `64x128` | `rho_electrons` | `0.850000` | `1.133333` | `0` |
| `64x128` | `rho_ions` | `0.850000` | `1.133333` | `0` |
| `128x256` | `rho_electrons` | `0.850000` | `1.133333` | `0` |
| `128x256` | `rho_ions` | `0.850000` | `1.133333` | `0` |
| `256x512` | `rho_electrons` | `0.850000` | `1.133333` | `0` |
| `256x512` | `rho_ions` | `0.850000` | `1.133333` | `0` |

因此新增 `RZ_RHO_AXIS_PRESCALE_INPUT_BOUNDARY_OPEN`：三档 resolution 的最终 axis ratio 和 scaling 前反推 ratio 均稳定，且 on/off 输入除显式 correction toggle 外一致。该合同把剩余边界进一步收窄到 scaling 前 axis deposition、负半径 wrap 或其输入状态，但仍不是 kernel root-cause 证明、charge closure 或正式收敛阶。合同由 `scripts/audit_rz_rho_axis_prescale_boundary.py` 生成，报告见 `runs/stage-c-validation/rz-rho-axis-prescale-boundary-v0.102/contract.{json,md}`，说明见 `notes/code-reading/particles/83-rz-rho-axis-prescale-boundary.md`。

### 5.14.19 v0.103 rho axis particle-state invariant

v0.103 再向上游核对 on/off 初始诊断帧的粒子状态。对 `electrons` 和 `ions`，按 `particle_id` 对齐后逐项比较位置、角度、权重和动量；三档 `64/128/256` resolution 的粒子数 on/off 完全一致，所有比较字段最大绝对差均为 `0`。在这一粒子状态不变量下，species `rho` 的 axis on/off 比值仍为 `0.85`，off-axis 比值仍为 `1`。

| grid | species | particles on/off | particle state | rho field | axis ratio | off-axis max deviation |
|---:|---|---:|:---:|---|---:|---:|
| `64x128` | `electrons` | `58880/58880` | `PASS` | `rho_electrons` | `0.850000` | `0` |
| `64x128` | `ions` | `58880/58880` | `PASS` | `rho_ions` | `0.850000` | `0` |
| `128x256` | `electrons` | `235520/235520` | `PASS` | `rho_electrons` | `0.850000` | `0` |
| `128x256` | `ions` | `235520/235520` | `PASS` | `rho_ions` | `0.850000` | `0` |
| `256x512` | `electrons` | `944128/944128` | `PASS` | `rho_electrons` | `0.850000` | `0` |
| `256x512` | `ions` | `944128/944128` | `PASS` | `rho_ions` | `0.850000` | `0` |

因此新增 `RZ_RHO_AXIS_DIAGNOSTIC_CONSUMER_BOUNDARY_OPEN`：粒子初始化和粒子状态差异已被排除，剩余边界集中在 species-rho diagnostic consumer、charge deposition 或负半径 axis wrap/scaling 路径。该合同仍不是具体 kernel root-cause 证明、charge closure 或正式收敛阶。合同由 `scripts/audit_rz_rho_particle_state_invariant.py` 生成，报告见 `runs/stage-c-validation/rz-rho-particle-state-invariant-v0.103/contract.{json,md}`，说明见 `notes/code-reading/particles/84-rz-rho-particle-state-invariant.md`。

### 5.14.20 v0.104 default versus explicit true axis correction

v0.104 对参数解析做真实 runtime 对照：64x128 RZ 的 default-true on case 省略 `boundary.verboncoeur_axis_correction`，另一个 sibling 显式设置 `true`，并与显式 `false` case 比较。default-true 与 explicit-true 的 `rho_electrons`、`rho_ions`、`rho`、`Er`、`Ez`、`divE` 数组最大绝对差均为 `0`；两种 species 的 particle ID、位置、角度、权重和动量也逐项一致。显式 false 只在 species axis rho 上产生差异，总 `rho` 与场变量保持一致。

| comparison | species rho fields | total rho / fields | particle state |
|---|:---:|:---:|:---:|
| default true vs explicit true | exact equal | exact equal | exact equal |
| default true vs explicit false | axis differs; max `60081.62377500016` | exact equal in selected fields | exact equal in saved state |

因此新增 `RZ_AXIS_CORRECTION_DEFAULT_EXPLICIT_TRUE_EQUIVALENT_FALSE_BOUNDARY_OPEN`：默认值解析和显式 true 分支已被排除，剩余问题集中在 axis correction 参与的 species-rho diagnostic/deposition/wrap/scaling consumer。该合同仍不是具体 kernel root-cause 证明、charge closure 或正式收敛阶。合同由 `scripts/audit_rz_axis_correction_default_explicit_true.py` 生成，报告见 `runs/stage-c-validation/rz-axis-correction-default-explicit-true-v0.104/contract.{json,md}`，说明见 `notes/code-reading/particles/85-rz-axis-correction-default-explicit-true.md`。

### 5.14.21 v0.105 non-neutral control exposes total-rho contribution

v0.105 继续用真实 2-rank RZ sibling 检查中性背景是否掩盖了 axis species-rho 差异：保持电子分布不变，只把 `ions.density` 改为 `0.5*n0`，再比较 correction-on/default 与显式 false。两种设置的电子/离子 particle ID、位置、角度、权重和动量逐项一致；`rho_electrons` 与 `rho_ions` 的 axis on/off 比值仍为 `0.85`，off-axis 比值仍为 `1`，总 `rho` 的 axis 比值也变为 `0.85`，最大差为 `30040.81188750008`。

该结果由 `delta(rho) - [delta(rho_electrons)+delta(rho_ions)] = 0` 逐数组验证：中性 case 中 total-rho 没有显示 axis 差异，是电子/离子电荷贡献相互抵消，而不是 species-rho 差异不存在。该非中性控制把边界从“可能被中性抵消掩盖”推进为“axis correction 参与的 species-rho consumer 差异会进入 total-rho”；但初始帧 `Er/Ez/divE` 仍未改变，且该合同仍不识别具体 deposition kernel root cause、不关闭 charge closure 或正式收敛阶。分类为 `RZ_NONNEUTRAL_AXIS_CORRECTION_REVEALS_TOTAL_RHO_CONTRIBUTION_BOUNDARY_OPEN`。报告见 `runs/stage-c-validation/rz-axis-correction-nonneutral-control-v0.105/contract.{json,md}`，说明见 `notes/code-reading/particles/86-rz-axis-correction-nonneutral-control.md`。

### 5.14.22 v0.106 non-neutral shape family narrows the axis boundary

将上一节的非中性控制扩展到 `particle_shape=1/2/3/4` 后，四个 shape 的 correction-on/off 总 `rho` axis 比值分别为 `0.850000000`、`0.843478261`、`0.836500221` 和 `0.831672744`，严格随 shape 增大而下降；所有 off-axis 比值仍为 `1`，电子/离子粒子状态逐项一致，`delta(rho)` 与 species delta 之和逐数组相符。该现象不是 shape=1 的单一特例，也不是可由 `1/3` 与 `1/4` 两个外层体积因子解释的统一比例。

源码交叉检查进一步把路径拆开：`ChargeDeposition.H` 在 RZ 中用粒子半径 `sqrt(xp*xp + yp*yp)` 和 `sx[ix]*sz[iz]*wq` 写入 shape-specific raw charge，但不读取 `verboncoeur_axis_correction`；axis toggle 在后续 `ApplyInverseVolumeScalingToChargeDensity` 的轴向 wrap/scaling 路径中才出现。因此当前最窄的可证边界是 **RZ shape deposition 与 axis wrap/scaling 的耦合**，而不是默认值解析或单一外层体积因子。该分类为 `RZ_NONNEUTRAL_AXIS_CORRECTION_SHAPE_DEPENDENT_AXIS_BOUNDARY_OPEN`；报告见 `runs/stage-c-validation/rz-axis-correction-nonneutral-shape-family-v0.106/contract.{json,md}`，说明见 `notes/code-reading/particles/87-rz-axis-correction-nonneutral-shape-family.md`。该结果仍不识别具体 kernel root cause、不关闭 charge closure 或正式收敛阶。

### 5.14.23 v0.107 non-neutral shape behavior across resolution

为检查上一节的 shape 结论是否能直接跨分辨率复用，将同一非中性 RZ on/off sibling 扩展到 `128x256`。两套分辨率的初始化帧都保持 particle state、off-axis rho 和初始 field 不变，`delta(rho)` 与 species delta 逐数组相符。更细的结果是：species rho 的 axis on/off 比值在 `64x128` 与 `128x256` 上完全一致，均为 `0.850000000/0.843478261/0.836500221/0.831672744`，因此 shape-dependent species behavior 在本实验的两套网格上稳定。

但不能把这组稳定性升级为 total-rho 结论。`64x128` 的 total-rho 保持上述单调比值，而 `128x256` 的 shape=2/3/4 在 sampled axis cells 发生电子/离子贡献近乎抵消，total-rho 比值变为 `1/1/1`；最大跨分辨率差为 `0.168327256`。这说明 total-rho 的可见性不仅取决于 axis scaling，还取决于 species cancellation 与网格/shape 组合。当前分类为 `RZ_NONNEUTRAL_AXIS_CORRECTION_SHAPE_DEPENDENT_CROSS_RESOLUTION_BOUNDARY_OPEN`：species-level 现象已获得跨分辨率复现，total-rho 仍是开放边界，且不关闭 charge closure、正式收敛阶或具体 kernel root cause。报告见 `runs/stage-c-validation/rz-axis-correction-nonneutral-shape-resolution-family-v0.107/contract.{json,md}`，说明见 `notes/code-reading/particles/88-rz-axis-correction-nonneutral-shape-resolution-family.md`。

### 5.14.24 v0.108 non-neutral shape behavior across ion density

v0.107 的 `128x256`、`ions.density = 0.5*n0` family 显示 shape=2/3/4 的 total-rho axis 比值因 species cancellation 变为 `1/1/1`。为判断这是否是分辨率造成的普遍失效，本轮保持网格、shape、粒子状态和 correction on/off sibling 不变，只将离子密度改为 `0.25*n0`，并完成另一组真实 2-rank 初始化帧对照。

结果把边界进一步收窄：species rho 的 axis 比值在两种离子密度上完全一致，均为 `0.850000000/0.843478261/0.836500221/0.831672744`；`0.25*n0` 时 total-rho 也恢复同一严格单调关系，而 `0.5*n0` 时 shape=2/3/4 仍为 `1/1/1`。两组的 particle state、off-axis rho、初始 `Er/Ez/divE` 和 `delta(rho)` species decomposition 均通过合同。因此，v0.107 的现象应表述为 **total-rho 合成 observable 对 species cancellation 与离子密度敏感**，而不是简单的跨分辨率失效。当前分类为 `RZ_NONNEUTRAL_AXIS_CORRECTION_TOTAL_RHO_CANCELLATION_DENSITY_SENSITIVE_BOUNDARY_OPEN`；该结果仍不识别 kernel root cause、不关闭 charge closure 或正式收敛阶。报告见 `runs/stage-c-validation/rz-axis-correction-nonneutral-density-family-v0.108/contract.{json,md}`，说明见 `notes/code-reading/particles/89-rz-axis-correction-nonneutral-density-family.md`。

### 5.14.25 v0.109 non-neutral shape behavior across three density ratios

为区分“密度敏感”与“特定物种配比下的 sampled-axis 抵消”，本轮在同一 `128x256`、2-rank、shape=1/2/3/4、correction-on/off sibling family 中加入 `ions.density = 0.75*n0`。因此当前对照包含 `0.25*n0`、`0.5*n0` 和 `0.75*n0` 三个密度，而电子分布、网格、粒子 shape 和 axis toggle 的成对关系保持不变。

三种密度的 species `rho_ions` axis on/off 比值完全一致，并随 shape 严格下降：`0.850000000/0.843478261/0.836500221/0.831672744`。total-rho 的结果则分成两类：`0.25*n0` 与 `0.75*n0` 都复现同一单调序列；`0.5*n0` 的 shape=1 仍为 `0.850000000`，但 shape=2/3/4 为 `1/1/1`。这说明抵消不是任意 density change 都会触发的普遍失效，而是 sampled axis cells 上特定 species ratio 与 shape 组合造成的合成 observable cancellation。

三密度的 correction-on/off sibling 均通过粒子 ID 状态、off-axis rho、初始 `Er/Ez/divE`、MPI decomposition 和 `delta(rho)` species-sum 检查；源码仍显示 charge kernel 不读取 axis toggle，axis correction 位于后续 axis wrap/scaling consumer。当前分类收窄为 `RZ_NONNEUTRAL_AXIS_CORRECTION_TOTAL_RHO_SAMPLED_AXIS_CANCELLATION_SPECIAL_RATIO_BOUNDARY_OPEN`。该结果不识别 kernel root cause、不关闭 charge closure 或正式收敛阶。报告见 `runs/stage-c-validation/rz-axis-correction-nonneutral-density-triple-v0.109/contract.{json,md}`，说明见 `notes/code-reading/particles/90-rz-axis-correction-nonneutral-density-triple.md`。

### 5.14.26 v0.110 formal convergence repeat-slope gate re-execution

为确认正式收敛 study 的 repeat-slope gate 不是一次性运行产物，本轮在当前 WarpX binary 和 `FI_PROVIDER=tcp` 环境下重新执行预注册的第二组 family：RZ/RSPHERE 各有 `64/128/256` 三档 resolution、correction on/off，共 12 个 2-rank producer。所有 producer 均返回 0，并写出 `producer.log`、`warpx_used_inputs` 和 diagnostics。

使用与第一组相同的 reader-side norm，RZ 分开报告 `Er/Ez/axis/off-axis`，RSPHERE 分开报告 `Er/axis/off-axis`，不做跨 geometry pooled fit。预注册的 correction-on gate 包含 14 个相邻 refinement comparison，固定 absolute slope-delta tolerance 为 `1e-8`；本轮 14/14 通过，最大绝对 slope 差为 `2.0135e-11`。correction-off 仍只作 numerical/reader-floor negative control，最大差为 `1.736e-3`，不进入 gate。

因此当前分类仍为 `FORMAL_CONVERGENCE_REPEAT_SLOPE_GATE_PASS_CHARGE_CLOSURE_OPEN`。这次重执行证明 repeat-slope gate 在当前环境可复现，但不把它升级为 formal numerical order，也不关闭 correction-on axis-charge correctness。报告见 `runs/stage-c-validation/formal-convergence-second-family-v0.110/contract.{json,md}` 和 `runs/stage-c-validation/formal-convergence-repeat-slope-gate-v0.110/contract.{json,md}`，说明见 `notes/code-reading/particles/91-formal-convergence-repeat-slope-gate-v0.110.md`。

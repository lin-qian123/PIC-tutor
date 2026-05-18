# PIC 程序详解书总计划

## 1. 项目定位

本书不是 WarpX 用户手册的翻译，也不是单纯的 PIC 理论笔记，而是一本从真实现代 PIC 程序切入的“物理-算法-代码-验证-文献”一体化教材。主线以同级目录 `../warpx` 为准，逐步解释一个高性能 PIC 程序如何从 Vlasov-Maxwell / Vlasov-Poisson 模型落到可扩展 C++/Python/HPC 实现。

核心读者假定为：懂基本电磁学、等离子体物理或数值计算，但希望真正读懂 PIC 程序、能修改模块、能判断算法边界、能把论文公式与代码实现对应起来的人。

## 2. 已整合的一手信息

本地 `../warpx` 的首轮扫描结论：

- `README.md`：确认 WarpX 是电磁和静电 PIC 程序，支持 PML、网格细化、boosted-frame、GPU/CPU 并行、负载均衡，并给出源码 DOI 和论文 DOI。
- `Docs/source/index.rst`：官方文档总目录把功能分成安装、使用、教程、理论、数据分析、开发、维护等板块；理论范围覆盖 Maxwell/Poisson/Ohm、1D/2D/3D/RZ/球坐标、多物理、显式/隐式推进、AMR、boosted frame、嵌入边界、谱方法。
- `Docs/source/theory/`：可直接作为物理和算法章节的初始骨架，包含 PIC 总览、电磁 PIC、静电 PIC、kinetic-fluid hybrid、动理学粒子、冷流体、边界条件、AMR、boosted frame、碰撞、电离、QED。
- `Docs/source/developers/repo_organization.rst`：指出源码集中在 `Source/`；PIC loop 在 `WarpX::Evolve`，核心无诊断推进路径在 `OneStep_nosub` 或 `OneStep_sub1`；主类是 `WarpX`。
- `Source/`：模块边界清楚，第一批重点目录包括 `Evolve/`、`FieldSolver/`、`Particles/`、`BoundaryConditions/`、`Diagnostics/`、`Initialization/`、`Parallelization/`、`Fluids/`、`Python/`、`Utils/`。
- `Examples/`：按物理应用组织，包括 plasma acceleration、laser-plasma interaction、beam physics、astrophysical plasma、fundamental plasma、hybrid model、HPC/numerics 等。
- `Regression/`：适合用来解释验证、基准、checksum 和持续集成。
- `Tools/`：包含 PSATD 推导 notebook、后处理、性能分析、QED table、发布维护等工具。
- `Docs/source/refs.bib`：当前有 251 条 BibTeX 入口，应作为第一批文献池。

外部解读站点的使用定位：

- DeepWiki 当前页面列出了 WarpX Overview、Core Simulation Framework、Initialization、Evolution Loop、Boundary Conditions、Particle System、Field Solvers、Diagnostics、Python Interface、Build System、Testing 等页面，适合作为源码走读索引。
- Zread 页面明确提示“AI 生成，可能有错误”，适合作为入门提纲和模块清单。
- 两者都不能替代本地源码、官方文档和论文引用。

## 3. 总体写作原则

每章必须落到六类证据：

1. 物理模型：连续方程、适用尺度、无量纲化、守恒律和近似条件。
2. 数值离散：网格、时间推进、插值、沉积、求解器、稳定性、误差和噪声。
3. WarpX 实现：在同一主题内讲清源码路径、关键类、关键函数、数据结构、调用链和必要的逐行代码解释。
4. 输入与输出：相关参数、示例输入、诊断输出、可视化和后处理。
5. 验证与比较：示例、Regression 测试、解析解或文献 benchmark。
6. 文献谱系：基础论文、WarpX 论文、算法论文、近年改进和替代程序。

论文阅读和笔记生成按 `docs/paper-reading-workflow.md` 执行：PDF 默认先用 MinerU 转 Markdown，转换产物保存在论文所在目录或论文专属子目录；中文讲解笔记按原文顺序逐段总结，图片插在首次引用处，重要公式用 `$$ ... $$` 并详细推导。

源码讲解不单独抽成“代码手册”部分，而是嵌入每个物理和算法主题中。例如讲粒子推进器时，同时讲 Lorentz 力方程、Boris/Vay/Higuera-Cary 离散推导、WarpX 的 pusher 选择参数、`Source/Particles/Pusher/` 中的实现、相关测试和原始文献。这样读者能在同一个上下文中看到“物理模型为什么这样写、算法为什么这样离散、代码为什么这样实现”。

代码准确性要求：

- 每次写源码讲解前，记录当前 `../warpx` 的分支和 commit。
- 引用代码时写明相对路径、函数/类名；需要逐行解释时记录行号范围，并在写作当天重新读取源码。
- 不凭记忆解释实现细节；对关键调用链用 `rg`、源码、Doxygen/官方文档和最小示例交叉确认。
- 能运行的小例子尽量本地运行；不能运行时明确说明原因，并用 Regression/Examples 或官方文档作替代证据。
- 如果 WarpX 代码和外部解读站点不一致，以本地源码和官方文档为准。

## 4. 推荐书稿结构

### 第一部分：PIC 的物理和数学基础

1. 为什么需要 PIC：从等离子体动理学到宏粒子模拟。
2. Vlasov-Maxwell、Vlasov-Poisson 与常见约化模型。
3. 宏粒子、形函数、权重、噪声、采样误差和有限粒子效应。
4. 单位制、无量纲化、CFL、Debye 长度、等离子体频率与分辨率要求。

### 第二部分：核心 PIC 算法

5. PIC 总循环：gather、push、deposit、field solve。
6. 粒子推进器：Boris、Vay、Higuera-Cary 及相对论修正。
7. 电荷/电流沉积：direct、Villasenor-Buneman、Esirkepov、Vay deposition。
8. 场插值和形函数：momentum-conserving 与 energy-conserving 选择。
9. FDTD/Yee/CKC：离散 Maxwell 方程、色散、CFL 和边界。
10. PSATD/Galilean PSATD：谱求解器、NCI 抑制和并行 stencil。
11. 静电 PIC 与 Poisson 求解：lab-frame、relativistic、multigrid。
12. 隐式和半隐式 PIC：为什么需要、代价和适用问题。
13. 滤波、平滑、数值 Cherenkov 不稳定性和稳定性工程。
14. PML、PEC/PMC、Silver-Mueller、周期边界和粒子边界。
15. AMR、subcycling、guard cells、coarse-fine coupling。

### 第三部分：贯穿式 WarpX 源码讲解

这一部分不是独立章节，而是全书写法规范。所有源码讲解都跟随对应的物理、算法或案例出现：

- 总循环章节讲 `main.cpp`、`WarpX` 主类、`WarpX::Evolve`、`OneStep_nosub` / `OneStep_sub1`。
- 粒子推进章节讲 `Source/Particles/Pusher/`、pusher 选择参数和粒子属性更新。
- 沉积章节讲 `Source/Particles/Deposition/`、charge/current deposition、guard cells 和 conservation。
- 场求解章节讲 `Source/FieldSolver/`、FDTD、PSATD、Poisson、implicit solver 和 hybrid solver。
- 边界章节讲 `Source/BoundaryConditions/`、PML、PEC/PMC、Silver-Mueller 和粒子边界。
- AMR 和并行章节讲 `Source/Parallelization/`、AMReX MultiFab、guard cell exchange、regrid 和 load balance。
- 初始化章节讲 `Source/Initialization/`、输入参数、species、density/momentum/temperature profile。
- 诊断章节讲 `Source/Diagnostics/`、plotfile、openPMD、reduced diagnostics、checkpoint/restart。
- Python 和工作流章节讲 `Source/Python/`、PICMI、callbacks、field/particle access。
- 构建和测试章节讲 `CMakeLists.txt`、`Examples/`、`Regression/`、checksum 和 CI。

每个涉及代码的章节使用固定小节：

1. 物理或算法目标。
2. 连续方程和离散公式。
3. WarpX 输入参数入口。
4. 源码调用链总览。
5. 关键函数逐行或逐块讲解。
6. 示例/测试验证。
7. 文献和进一步阅读。

### 第四部分：多物理和高级模型

16. 激光模型与天线注入：激光包络/场表达、注入边界、`Source/Laser/` 实现。
17. 碰撞：DSMC、Coulomb、MCC、fusion、Compton、Bremsstrahlung；同步讲 `Source/Particles/Collision/`。
18. 电离：ADK、OTB、场变换和权重处理；同步讲 `Source/Particles/ElementaryProcess/` 和相关参数。
19. QED：强场辐射、Breit-Wheeler、lookup tables、PICSAR-QED；同步讲 QED table 工具和粒子过程实现。
20. hybrid PIC 和流体模型：质量为零电子流体、Ohm 定律、MUSCL-Hancock；同步讲 `Source/Fluids/` 和 hybrid field solver。
21. 嵌入边界和复杂几何：几何表示、粒子刮擦、边界场处理；同步讲 `Source/EmbeddedBoundary/`。
22. accelerator lattice、外场、束流物理和加速器元件；同步讲 `Source/AcceleratorLattice/` 和外场初始化。
23. boosted-frame、moving window 和 Lorentz 变换下的输入输出；同步讲参数、诊断变换和相关工具。

### 第五部分：案例驱动综合讲解

24. Langmuir wave：最小 PIC 验证案例，串联 Vlasov-Poisson/Maxwell、初始化、推进、诊断。
25. uniform plasma：性能和数值基础案例，串联并行分解、负载均衡、I/O 和 scaling。
26. LWFA/PWFA：等离子体加速主线案例，串联激光/束流、moving window、boosted frame 和诊断。
27. TNSA/RPA/laser-ion acceleration：强激光离子加速案例，串联靶初始化、边界、QED/碰撞可选扩展。
28. plasma mirror 与高强度激光相互作用。
29. beam-beam collision、FEL、ion extraction。
30. magnetic reconnection 和 hybrid model benchmark。
31. capacitive discharge 与低温等离子体 PIC-MCC。
32. 用户本地 `Simulation/` 案例：RPA magnetic、AI/POD/DMD/CNN 分析可作为后续专题。

### 第六部分：工程、生态和前沿

33. WarpX 与 AMReX/PICSAR/openPMD/PICMI 的分工。
34. 参数系统、CMake 构建、维度变体、Python 接口和 Regression 测试。
35. Exascale、GPU portability、load balancing、I/O、profiling 和性能调优。
36. 与 EPOCH、OSIRIS、VPIC、PIConGPU、FBPIC、HiPACE++ 的比较。
37. 新近算法：geometric/symplectic PIC、structure-preserving PIC、quasi-static PIC、semi-implicit ES-PIC、ML-assisted PIC。
38. 如何为 WarpX 写新模块：从论文公式到参数、源码、测试和文档。

### 附录

- A. 符号表和单位换算。
- B. 常用输入参数按主题索引。
- C. WarpX 源码路径速查。
- D. 算法公式推导全集。
- E. 文献按主题分类。
- F. 可复现实验脚本和图表生成流程。

## 5. 分阶段执行计划

### 阶段 0：项目资料库建立

目标：先把所有资料入口结构化，避免写作时反复迷路。

产物：

- `bibliography/warpx-refs.bib`
- `docs/source-map.md`
- `docs/literature-map.md`
- `docs/chapter-template.md`
- `docs/paper-reading-workflow.md`
- `notes/warpx-docs-inventory.md`
- `notes/warpx-source-inventory.md`

重点动作：

- 从 `Docs/source/refs.bib` 抽取 251 条文献，按 PIC 基础、场求解、沉积、推进器、AMR、boosted frame、PML、QED、碰撞、应用、HPC 分类。
- 对 `Docs/source/theory/` 每个 rst 文件建立章节对应关系。
- 对 `Source/` 每个一级/二级目录建立“职责、关键文件、关键函数、相关参数、相关文献”表。

### 阶段 1：书稿骨架和样章

目标：确定最终书稿风格和深度，先完成一章可审阅样章。

建议样章：

- “PIC 总循环和 WarpX 主演化路径”：从连续模型到 `main.cpp`、`WarpX::Evolve`、`OneStep`、粒子/场/诊断调用链。

样章必须包含：

- 公式推导；
- 代码路径；
- 调用链图；
- 参数示例；
- 最小运行案例；
- 参考文献；
- 练习题和进一步阅读。

### 阶段 2：核心算法章节

优先顺序：

1. 粒子推进器。
2. 电流/电荷沉积。
3. FDTD/Yee/CKC。
4. PSATD/Galilean PSATD。
5. 边界条件和 PML。
6. AMR 和 guard cell。

每个算法章节都要回答：

- 连续方程是什么；
- 离散变量放在哪里；
- 推导如何得到更新公式；
- 守恒或稳定性靠什么保证；
- WarpX 哪个文件实现；
- 输入参数如何切换；
- 哪个测试或示例可以验证；
- 原始论文和后续改进是什么。

### 阶段 3：主题内嵌源码逐行讲解

按主题推进，而不是按源码目录单独推进。每个主题章节同时完成物理、算法和代码：

- 粒子推进：Lorentz 力方程、Boris/Vay/Higuera-Cary 推导、pusher 参数、`Source/Particles/Pusher/` 逐块讲解、测试案例。
- 沉积：连续性方程、charge/current deposition、shape factor、`Source/Particles/Deposition/` 逐块讲解、守恒验证。
- 场求解：Maxwell/Poisson/Ohm、FDTD/PSATD/implicit/hybrid、`Source/FieldSolver/` 逐块讲解、色散和稳定性测试。
- 边界：PML/PEC/PMC/periodic/particle boundary、`Source/BoundaryConditions/` 和 `Source/Particles/ParticleBoundaries*` 逐块讲解、边界案例。
- AMR/并行：MultiFab、guard cells、regrid、load balance、`Source/Parallelization/` 逐块讲解、uniform plasma 性能案例。

每个源码讲解小节都要保留：

- 读取源码当天的 commit；
- 准确文件路径和函数名；
- 必要的行号范围；
- 与输入参数的对应关系；
- 与文档、示例或测试的对应关系；
- 若是复杂内核，先给伪代码，再逐行解释真实代码。

### 阶段 4：多物理和应用案例

以官方 Examples 和 Regression 为主，挑选覆盖面最大的案例组：

- 基础波和验证：Langmuir、uniform plasma、Pierce diode。
- 加速器和束流：LWFA、PWFA、Gaussian beam、beam-beam、FEL、ion extraction。
- 强场激光等离子体：laser-ion、plasma mirror、TNSA/RPA。
- 混合和天体：magnetic reconnection、hybrid examples。
- 低温和碰撞：capacitive discharge、MCC。
- HPC 数值：uniform plasma scaling、I/O、load balance。

### 阶段 5：文献闭环

文献来源分三层：

- 第一层：`../warpx/Docs/source/refs.bib` 和官方文档引用。
- 第二层：WarpX 论文、Gordon Bell 论文、AMReX/PICSAR/openPMD/PICMI 论文。
- 第三层：PIC 经典教材和新近前沿，包括 Hockney-Eastwood、Birdsall-Langdon、Dawson、Yee、Boris、Villasenor-Buneman、Esirkepov、Vay、Higuera-Cary、Godfrey、Lehe、Vincenti、PICSAR-QED、HiPACE++、VPIC、PIConGPU、EPOCH、OSIRIS 等。

每条文献最终都要落到一个或多个章节，避免“堆参考文献但正文不用”。

### 阶段 6：可出版整理

可选路线：

- Markdown-first：适合快速写作、持续扩展和本地预览。
- Quarto/Pandoc：适合生成 HTML/PDF/EPUB，并保留公式、引用和交叉引用。
- LaTeX book：适合最终排版，但前期迭代成本较高。

推荐先 Markdown-first，等样章稳定后迁移到 Quarto。

## 6. 近期三步

1. 建立资料索引：复制 BibTeX、生成 source map、生成 chapter template，其中模板明确要求源码逐行讲解嵌入对应物理/算法章节。
2. 写第一章样章：“PIC 总循环和 WarpX 主演化路径”。
3. 对样章做一次严格审查：检查公式、源码路径、参数、示例、文献是否闭环。

## 7. 风险和控制

- 范围过大：采用“总书骨架 + 样章验证 + 按主题推进”，不要一开始铺满所有章节。
- 二手站点错误：DeepWiki/Zread 只做索引，所有结论回到源码、官方文档、论文。
- 文献不闭环：每章维护章节级 bibliography，不在总表中无目的堆文献。
- 代码版本漂移：记录本地 `../warpx` 的 commit/branch 或非 git 状态；每次写逐行代码解释前重新确认。
- 只讲理论不讲程序：每节必须有源码路径或输入示例。
- 只讲程序不讲物理：每个实现点必须回到连续模型、近似条件和数值误差。

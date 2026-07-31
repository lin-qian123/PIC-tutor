# 9. 文献路线与延伸阅读

本书的文献不是装饰，也不是章节末尾统一贴一串 BibTeX。它真正承担三类职责：

1. 给物理结论提供一手来源。
2. 给数值算法和代码实现提供历史与方法边界。
3. 给独立分析、benchmark 和 regression 判据提供外部对照。

因此本章不把文献写成“推荐书单”，而是按证据强度和章节用途组织阅读路线：哪些来源能够支撑公式与机制，哪些只可提供历史线索，哪些问题仍应保留为开放边界。检索到的题名、DOI 或摘要只能帮助定位主题，不能替代全文阅读、公式核对和章节证据。

## 本章的读者用法：文献是论证工具，不是书目清单

读者不需要先把全部文献读完再学习 PIC。每篇文献在本书中只承担一个明确任务：解释一个物理概念、给出一个离散算法、提供历史边界，或作为某个诊断量的外部参照。遇到文献引用时，建议连续问三件事：

1. 这篇来源支持正文中的哪一句话，支持的是公式、机制还是历史事实？
2. 相关 WarpX 源码与运行案例分别提供了哪一层独立证据？
3. 哪一步仍然只是相似性或摘要级线索，不能写成“论文已经证明 WarpX 实现”？

这样读，文献路线就服务于教程的理解路径：第 1-2 章优先建立 kinetic/PIC 基础，第 4-6 章用 pusher、deposition 和 solver 文献解释离散选择，第 7 章用边界文献校准 PML/AMR 的历史语义，第 8 章再把外部理论与实际诊断对照。未取得全文或尚未完成逐段核对的来源只定义结论边界，不改变读者从概念到实现再到验证的主线。

### 阅读路线：先分类证据，再把一条主张接回教程

第一次阅读第 9 章时，不要把来源名称按年代或主题全部抄录。按下面四步建立可复用的判读顺序：

1. **先读 9.1。** 为正在阅读的来源定 A/B/C/D 层，并写下材料实际可核查到的范围；层级描述的是证据强度，不是论文的重要性。
2. **再读 9.2 与当前章节对应的一条主线。** 基础、pusher、PSATD/NCI 文献分别服务不同的公式和离散假设；只选与当前问题相连的一条，而不是把所有来源混成“PIC 背景”。
3. **用 9.3--9.5 确认缺口与优先级。** 这里回答的是哪一个缺失来源会改变哪一章的论证边界，不是要求在学习前先取得全部全文。
4. **用 9.6--9.11 输出一张判读卡。** 将论文的一个公式、机制或历史事实连到本书章节、源码职责、一个 observable 和不可外推范围；完成练习时也要把“能支持”和“不能支持”并列写出。

这条路线的停止条件是：读者能针对一个具体主张说明它来自什么层级的材料、怎样与实现和案例相互独立，以及哪一项限制仍然存在。这样第 9 章才会反向校验第 1--8 章的论证，而不是成为文末的资料库存。

## 9.1 文献证据的使用层级

本书使用的文献证据有四层，强度不能混写：

| 层级 | 本书中的典型形态 | 可支持的写法 | 限制 |
|---|---|---|---|
| A. 全文可核查 | 全文、可检索文本、图像与逐段阅读笔记均可相互核对 | 可直接作为正文一手证据 | 仍需对照具体公式、图和段落，而不是只看中文摘要 |
| B. 已取得待精读 | 全文可读，但尚未完成逐段笔记或章节对照 | 可作为“已取得、待精读”的明确线索 | 不能把具体公式或图表当成已核实正文 |
| C. 书目信息/摘要线索 | DOI、题名、摘要和可访问的书目信息 | 可作为取得边界或延伸阅读线索 | 不能把摘要内容冒充成论文正文结论 |
| D. 旁证或相关文献 | 主题相关但不是当前章的主引用，或并非同一 bibliographic item | 可作背景、旁证、术语线索 | 不能替代主引用本身 |

阅读和写作时应遵守：

- 只有 A 层全文可核查来源，才允许在正文里写成“已核实的一手证据”。
- B 层来源只能写成“已取得但尚待逐段讲解”。
- C 层和 D 层只能写成获取线索或背景边界，不能抬成正文论证。

这条规则尤其影响尚未完成全文或版本差异核对的 `Hockney-Eastwood`、`Yee 1966`、`Esirkepov 2001`、`Villasenor-Buneman 1992` 和 `LeeCPC2015`。

## 9.2 支撑各章的核心文献

本书已有可核查全文来源的核心文献主要集中在三条主线。

### 9.2.1 PIC foundations

可供深入阅读的起点是 `Birdsall-Langdon 1985`、`Tajima-Dawson 1979`、`Dawson 1983`、`Vranic 2015` 和 `Muraviev 2021`。第一次阅读应先从本章标出的概念和结论进入，而不是按年代或关键词机械浏览。

`Tajima-Dawson 1979` 用于解释最早期的 `driver -> wake -> trapping -> acceleration` 与 LWFA scaling。它给出历史上的物理链条，而不替代现代 WarpX case 的输入、诊断和 regression。

这些基础文献主要支撑：

- 第 1 章的 superparticle、weighted particles、finite-size particles、quiet start、噪声与 heating 讨论；
- 第 2 章的最小 PIC loop、electrostatic / EM / Darwin 模型边界；
- 第 8 章中 diagnostics、spectrum、correlation time、weak instability dynamic range 的讨论；
- LWFA 最早 scaling baseline 的历史入口。

Vranic 2015 进一步补上了粒子 merge/resampling 这条应用线。它支撑第 4 章对“两粒子局部守恒 merge”的一手文献解释，但不替代 WarpX `VelocityCoincidenceThinning` 的逐行等价或专门运行验证。

Muraviev 2021 将这条应用线扩展为完整的 resampling 方法谱系。它支撑第 4 章对 agnostic down-sampling、局部权重噪声、严格守恒 thinning 和 merge/cluster 权衡的一手文献解释，但论文的 PICADOR/hi-chi QED cascade 结果不替代 WarpX 运行证据。

`Birdsall-Langdon 1985` 适合用作基础概念的回查书，而不是被误当作本书每个实现细节的直接来源；遇到具体 solver、pusher 或 deposition 公式时，仍应回到该算法的原始论文和对应源码。

### 9.2.2 Particle pusher

可供深入阅读的核心论文是 `Vay 2008` 和 `Higuera-Cary 2017`。

这两条线主要支撑：

- 第 4 章对 Vay pusher 与 Higuera-Cary pusher 的源码讲解；
- `Source/Particles/Pusher/UpdateMomentumVay.H` 与 `UpdateMomentumHigueraCary.H` 的公式对表；
- “相对论精度”和“结构保持”两条不同的算法目标。

但这条模块还没有完成 `Boris` 原始文献闭环，因此第 4 章仍不是“推进器历史谱系全闭环”。

### 9.2.3 PSATD / Galilean / boosted-frame / NCI

可供深入阅读的核心论文是 `Godfrey 2014`、`Kirchen 2016` 和 `Lehe 2016`。`Vay 2014` 的综述可作为第 4 章 Boris/Vay 谱系和第 6 章 PSATD/NCI 机制的统一入口；它不替代 WarpX 的源码交叉核对、案例验证或论文图形逐点复现。

这三条线构成第 6 章最完整的论文主干：

- Godfrey 2014：fixed-grid PSATD 的 NCI 策略分类；
- Lehe 2016：Galilean coordinates 消除 NCI 的核心离散论证；
- Kirchen 2016：boosted-frame workflow 与稳定离散表示之间的应用层连接。

`Andriyash 2016` 为 quasi-cylindrical Fourier--Bessel basis、PSATD 解析时间推进、`m±1` 横向 mode coupling 和 current-correction 公式提供全文依据；但 PLARES-PIC 与 WarpX 的函数级等价、WarpX 运行复现和论文图逐点复现仍保持边界。

因此，第 6 章的阅读可以从论文的离散假设出发，再回查相应源码和案例；仍未完成的运行覆盖不会被写成已经证明的算法结论。

## 9.3 关键来源的已知边界

以 `TajimaDawson1982` 为例，应把“正式来源的书目信息已确认”和“可逐段核查的正文已取得”分开。Crossref/AIP 元数据确认 *AIP Conference Proceedings* `91(1):69-93` 与 DOI `10.1063/1.33805`，但本书覆盖的材料中没有可合法逐页核查的 publisher PDF。因此，相关会议稿只能作为主题旁证，不能替代 Tajima--Dawson 的正式条目。

这份相关会议稿可在有限范围内解释 beat-wave 共振、前向 Raman 散射、电子俘获、退相位、自聚焦、丝化和相对论前向 Brillouin 散射；但它是单作者相关会议稿，不能替代正式 Tajima--Dawson AIP 条目。

如果按“缺少它会让哪一章的论证最薄弱”排序，优先关注的不是更多新论文，而是以下几条老而关键的一手来源。

| 缺口 | 可用证据 | 主要影响章节 | 可替代程度 |
|---|---|---|---|
| `Hockney-Eastwood` 原书 | 仅有书目信息与相关论文线索；尚无可逐段核查的全文 | 第 1、2、5、6 章 | 只能部分由 `Birdsall 1985` 与 `Dawson 1983` 补足 |
| `Yee 1966` | DOI 已确认；尚无全文 | 第 2、6 章 | 可由源码与后继 FDTD 文献支撑，但缺原始历史入口 |
| `Esirkepov 2001` | 作者预印本及其公式材料可核查；仍缺 CPC 发表版对照 | 第 5 章 | 可支撑预印本层面的解释，不能宣称 CPC 定稿已核对 |
| `Villasenor-Buneman 1992` | 论文全文及公式阅读材料可核查 | 第 5 章 | 可支撑公式与源码对照；仍需逐图、逐记号复核 |
| `Andriyash 2016` | 全文公式材料可核查；主题为 quasi-cylindrical Fourier-Bessel PSATD | 第 6 章 RZ PSATD | 可支撑公式解释；不能推出 PLARES-PIC 与 WarpX 等价或运行复现 |
| `LeeCPC2015` | accepted manuscript 可核查；仍缺 publisher-formatted CPC PDF | 第 7 章 | 可支撑 accepted-manuscript 与源码的对应，不能宣称发表版逐系数等价 |

这六条中，`LeeCPC2015` 的边界最容易被误读：accepted manuscript 已可精读，所以它足以解释文中对应的 PML 思想；但发表版的排版、系数和版本差异尚未逐项核对，因此不能借此宣称已经完成 publisher-formatted CPC PDF 的对照。

## 9.4 各章的文献覆盖范围

全书各章的文献覆盖范围并不均匀。

| 章节 | 文献覆盖程度 | 主要已核查来源 | 主要边界 |
|---|---|---|---|
| 第 1 章 动理学模型 | 中等 | `Birdsall 1985`、`Dawson 1983` | `Hockney-Eastwood`、更细的 particle-mesh heating 原始文献 |
| 第 2 章 PIC 总循环 | 中等 | `Birdsall 1985`、`Dawson 1983` | `Yee 1966` 原始入口 |
| 第 3/3A 章 主循环与初始化 | 中低 | 以源码为主 | 需要把基础文献和工程论文绑定得更明确 |
| 第 4 章 粒子推进器 | 中高 | `Boris 1970` 书目信息、`Birdsall 1985`、`Vay 2008`、`Higuera-Cary 2017` | 原始 Boris 1970 会议论文 PDF 仍缺 |
| 第 5 章 沉积与形函数 | 中等 | Esirkepov 与 Villasenor 的 charge-conserving 方法 | Esirkepov 还缺 CPC 定稿对照；两种构造不能由单一案例互相替代 |
| 第 6 章 场求解器 | 高 | `Vay--Godfrey 2014`、`Godfrey 2014`、`Lehe 2016`、`Kirchen 2016` | 仍需把文献中的离散假设与各个具体求解器配置分别对应 |
| 第 7 章 边界、PML 与 AMR | 中等偏低 | `Berenger 1994/1996`、WarpX 源码与代表性案例 | `LeeCPC2015` 出版社排版正文仍缺 |
| 第 8 章 诊断、验证与案例 | 中等 | `Dawson 1983` 的诊断思路 | 还缺更多 case-specific benchmark papers |
| 第 9 章 文献路线 | 本章即路线图 | A/B/C/D 证据层级 | 新来源必须先判断证据层级，再进入章节论证 |

这个表最重要的结论是：相较于第 6 章，第 5 章和第 7 章更需要补强可逐段核查的一手文献。

## 9.5 延伸阅读的优先顺序

延伸阅读不应泛泛地“多找一些相关论文”，而应按它能补强哪一章的论证排序：

1. `Esirkepov 2001` 的 CPC 定稿 PDF
   - 预印本足以支撑本书的公式解释；与 2001 CPC 发表版逐项对齐仍是独立任务。
2. `Yee 1966`
   - 直接补第 2 / 6 章里的原始 FDTD 入口。
3. `LeeCPC2015` 正文 PDF
   - 直接补强第 7 章的 PML 一手文献。
4. `Hockney-Eastwood` 或其 article-level fallback
   - 继续补第 1 / 2 章的 particle-mesh foundations。
5. `Boris` 原始文献
   - 书目信息已核实，但原始 proceedings 全文尚未成为可逐页核查的材料。
   - 在获得合法全文前，不把 Birdsall 的二手推导写成 Boris 原文证据。

该顺序反映了证据分布：第 6 章已有较完整的论文主干，而第 5、7 章的原始文献支撑相对更薄。

## 9.6 用一张文献判读卡连接论文、源码与算例

不要把论文清单当成阅读成果。每读一篇主引用，都写一张不超过一页的**文献判读卡**；它的作用是把论文中的论断，接回本书的章节、WarpX 的实现和可观察量。卡片至少回答四个问题：

| 问题 | 读者应记录的内容 | 用途 |
|---|---|---|
| 这篇论文研究什么 | 一句物理问题、模型假设和适用尺度 | 防止把不同几何、近似或时间尺度混在一起 |
| 它给出什么证据 | 一个公式、图或定量判据及其上下文 | 区分原文结论与二手转述 |
| 它怎样接到本书 | 对应章节、源码职责和一个输出观察量 | 防止把论文机制直接写成程序行为 |
| 它还不能说明什么 | 版本、离散、几何、参数或运行覆盖的缺口 | 防止把局部证据放大成普遍结论 |

例如，读 `Esirkepov 2001` 时，卡片应把连续性方程与第 5 章的形函数/电流沉积并列；读 `Lehe 2016` 时，应把 Galilean 表示的离散假设与第 6 章的 PSATD 选择条件并列；读 `LeeCPC2015` 时，则应把 PML 的公式与第 7 章的残余场观察量并列。这样，读者获得的不是一份资料清单，而是一组可检验的论证连接。

### 9.6.1 三条从文献走到可观察量的读者路线

下面的三条路线故意选取不同类型的比较：解析 Langmuir 场与 Gauss-law residual、受控不稳定参考下的场能量、以及穿过 PML 后的总场能量比。它们共同遵守“论文 -> 实现 -> 输入 -> consumer”的顺序，却不能共享同一种通过结论。

#### 路线 1：Esirkepov 的守恒构造如何成为一个网格检查

- **先从文献取走什么：** `Esirkepov 2001` 的作者预印本把 old/new form factor 的差分组织为离散连续性方程。这可支撑算法机制，但不等于已逐项核对 CPC 定稿。
- **再定位什么实现与输入：** 第 5 章的 `Compute_shifted_shape_factor` 将 old/new shape 对齐，`doEsirkepovDepositionShapeN` 写入守恒电流；`Examples/Tests/langmuir/inputs_test_3d_langmuir_multi` 继承显式的 3D Esirkepov 设置。
- **consumer 实际比较什么：** `analysis_3d.py` 先比较 `Ex/Ey/Ez` 与 Langmuir 解析场，默认最大相对误差 `< 5%`；随后 `analysis_utils.py` 对已启用的 Esirkepov 条件计算归一化的 `divE-rho/epsilon_0` residual，默认容差 `1e-11`。
- **可以写出的结论与必须保留的边界：** 该 3D Langmuir 配置同时把解析场和指定 Gauss-law residual 接到 Esirkepov 输入上；它并不证明所有 shape、二维或 RZ，也不证明被 analysis 明确排除的 Esirkepov + PSATD 组合。

#### 路线 2：Galilean 表示是否压低了这类流动等离子体的 NCI

- **先从文献取走什么：** `Lehe 2016` 说明当 `v_gal` 与背景漂移相配时，移动表示改变数值共振条件；它不是 moving window 的同义词，也不是任意速度都稳定。
- **再定位什么实现与输入：** `SpectralSolver` 在非零 `v_galilean` 时构造 `PsatdAlgorithmGalilean`；`inputs_test_2d_galilean_psatd` 选择 direct deposition 与不带 current correction 的基线，另有 current-correction sibling。
- **consumer 实际比较什么：** `analysis_galilean.py` 按几何、time averaging 与 correction 分支选择 reference electric-field energy，并要求能量比小于该分支容差；开启 correction 时才额外检查 `divE-rho/epsilon_0`。
- **可以写出的结论与必须保留的边界：** 对这些已注册 NCI cases，可以说指定 Galilean 配置满足场能量稳定 gate，且 correction sibling 还满足指定 Gauss-law gate；reference 是受控的不稳定比较，不是解析 NCI growth rate，也不能推出任意漂移、deposition、边界或 AMR 组合同样稳定。

#### 路线 3：PSATD-PML 是否在这一入射与边界设置中保持低反射

- **先从文献取走什么：** `LeeCPC2015` 的 accepted manuscript 解释 split-field/PSTD PML 与反射率的依赖；它不等于 publisher-formatted 版本的逐系数核对。
- **再定位什么实现与输入：** `SpectralSolver` 为 PML 区选择 `PsatdAlgorithmPml`，`PushPSATD()` 单独推进 PML 场；`inputs_test_2d_pml_x_psatd` 选择 PSATD、`current_correction = 0`、无 PML divergence cleaning。
- **consumer 实际比较什么：** `analysis_pml_psatd.py` 先在 iteration 50 复算初始总场能量，再以末态/初态能量给出 reflectivity，并要求 `< 1e-6`。
- **可以写出的结论与必须保留的边界：** 这证明该 2D Cartesian、指定参数与无 correction/cleaning 的 PML case 满足总场能量反射率 gate；它不是对 LeeCPC2015 所有系数或扫描的复现，也不能外推到 RZ PML、Galilean/cleaning 组合或任意入射谱。

这三条路线还有一个共同的检查动作：先读输入是否真的选择了论文所讨论的表示或算法，再读 consumer 是否测量了该主张需要的 observable，最后才读取 PASS。若第一行只剩 checksum，它就不再是解析场或 Gauss-law 的合同；若第二行没有 current correction，便没有 Gauss-law gate；若第三行改成 RZ 的残余场 consumer，便不能继续引用这里的 Cartesian reflectivity 容差。读者在扩展任一路线前，应重新写出这四项，而不是沿用原案例的结论。

## 9.7 两条深读路线

下面两条路线把延伸阅读变成可检验的学习任务，而不是资料收集清单。

### 路线 A：第 5 章沉积文献

阅读任务：

- 先用 `Esirkepov 2001` 预印本追踪连续性方程、形函数和电流构造之间的关系；
- 再用 Villasenor 与 Esirkepov 的公式比较“轨迹分段”和“old/new shape difference”两种守恒组织；
- 最后回到第 5 章，分别写出论文、源码和测试各自能证明什么。

完成标志：

- 能说明为什么预印本公式不能自动证明 CPC 定稿逐式一致；
- 能用一个指定 case 的 observable 说明运行通过为什么不等于全部 geometry/order 覆盖。

### 路线 B：第 7 章 PML 文献

阅读任务：

- 用 `Berenger 1994/1996` 理解 split-field PML 的吸收机制；
- 对照 `LeeCPC2015` 的 accepted manuscript，定位高阶有限差分或伪谱 PML 的适用条件；
- 再回查 WarpX `PsatdAlgorithmPml.cpp`，区分论文公式、程序分派和指定 regression 的角色。

完成标志：

- 能指出 accepted manuscript 支持的具体论断；
- 不会把它误写成 publisher-formatted CPC PDF 的逐式核对。

第一次做文献深读时，建议先走路线 A：它能直接连接第 5 章的连续性方程、形函数和运行观察量；路线 B 更适合已完成第 6--7 章源码阅读、准备分析 PML 表示与边界条件的读者。

### 9.7.1 深读笔记的核查边界

文献判读卡与 A/B/C/D 层级一致，只说明你的材料分类没有自相矛盾；它不证明逐式审校已经完成，不证明预印本与出版社版本逐页等价，也不把 WarpX 的一个运行结果升级为论文全部物理结论的验证。判断引用强度时，应始终回到具体全文、公式、源码职责和案例观察量，而不是把卡片本身当成证明。

## 9.8 如何阅读证据边界

当正文出现“尚未证明”“仅适用于”或“不能外推”时，先判断它属于哪一种边界。不同边界要求不同的下一步，不能用更多文字把它们混成一个模糊的保留意见。

| 边界类型 | 它实际表示什么 | 读者可以说什么 | 读者不能说什么 |
|---|---|---|---|
| 文献边界 | 目标版本的全文或逐段核对不可得 | 已有材料支持的机制或历史线索 | 原始论文的逐式或逐图结论 |
| 实现边界 | 源码职责已知，但相应路径没有独立运行观察 | 这段代码在生命周期中的角色 | 该路径已经在目标物理问题中正确工作 |
| 数值边界 | 已有指定输入、观察量和容差下的比较 | 该案例在该 gate 下通过或失败 | 任意参数、几何或分辨率下都正确 |
| 收敛边界 | 重复计算或局部趋势存在，但关闭条件未满足 | 误差趋势或重复性与给定比较相符 | 已得到正式收敛阶或物理正确性证明 |

第 8 章的验证矩阵正是这张边界卡的运行版：它把 producer、consumer、observable 与限制并列。重复计算的 slope 一致性只能说明该组重复计算相符；它不等于 formal numerical order，也不等于 axis charge correctness。读者据此回到前八章时，应把每一句强结论都还原为“来源、实现、观察量、适用范围”四项，而不是只记住一个 PASS 标签。

## 9.9 把证据边界变成下一次判断

“开放边界”不是一句笼统的保留意见，也不是要求读者暂停学习直到所有问题都被解决。它表示当前证据链在哪一个环节停止；下一步应补的材料、运行或比较对象也因此不同。先把问题放进下列五类之一，再决定行动。

1. **目标文献版本尚不能逐段核对。** 例如已经有题名、摘要、预印本或 accepted manuscript，却没有所要比较的正式版本。此时可使用已经读到的公式或机制，并明确它来自哪一版材料；下一步是取得合法可核查全文、逐项对齐版本差异。不要用相近主题的论文、摘要或程序通过结果替代原文逐式结论。回看 9.3、9.5 与 9.6 的文献判读卡。
2. **源码职责清楚，实际数据路线尚未被独立观察。** 例如可从第 7 章看出 transition zone 的 gather、buffer、coarsen 和同步阶段，却没有能逐条辨认粒子路由的观测。此时可以说明每个阶段的职责；下一步必须在同步前记录与该问题对应的状态或计数。最终场、plotfile 或 checksum 不能倒推出所有中间路由都正确。回看 5.7、7.9 和 8.14。
3. **配置在初始化或运行前被 guard 拒绝。** 这本身是一个有信息的结果：输入组合没有到达粒子推进或 source 写入，因而尚无可解释的物理输出。下一步是确认 guard 的几何、solver 或算法前提，选择受支持的组合，或等待上游明确支持范围；不要绕过 guard 后再把一次启动成功写成原组合已验证。回看 5.14 与 7.3 的配置约束。
4. **某个 observable 有稳定残余，但根因尚未归属。** RZ axis residual 是典型情形。此时先把 axis、off-axis、全域量以及 field、species `rho`、total `rho` 的同时间层读数拆开；再做只改变一个因素的控制比较。稳定、可重复或随分辨率下降，仍只支持“这个残余值得解释”，不自动定位 deposition kernel 或关闭 charge correctness。回看 5.14.5.1 和 5.14.7。
5. **重复 family 有趋势，却尚不足以给出正式收敛阶。** 先固定几何、时间步、粒子数、误差范数和拟合区间，逐区间报告 slope，并把独立重复与物理正确性分开。只有每个 primary observable 的关闭条件都满足，才讨论 formal numerical order；一条下降曲线、一个好看的区间或 checksum 通过都不够。回看 5.14.6--5.14.7 与第 8 章验证矩阵。

这五类的共同输出可写成一张简短的**边界行动卡**：

1. **当前能说什么：** 只写被现有材料、源码职责或指定 consumer 直接支持的一句结论。
2. **证据停在哪里：** 写明缺的是全文版本、中间运行状态、受支持配置、根因区分，还是正式收敛条件。
3. **下一项独立证据：** 选择一种能直达缺口的动作，例如逐式对照、pre-sync 记录、匹配配置的 consumer、单因素控制或预先固定的 refinement family。
4. **在它完成前不能说什么：** 明确禁止的外推，如“所有几何都正确”“算法已证明守恒”或“已得到收敛阶”。

卡片的价值在于让“不知道”仍然可操作。它不会把文献访问问题误当作数值失败，也不会把一次配置拒绝误当作物理反例；更不会因为需要继续验证，就抹去已经由现有证据支持的有限结论。

## 9.10 本章结论

本书的文献部分已经能支撑核心主线，但还没有让所有一手来源都达到逐段核查的程度。更准确的概括是：

- foundations 线已有 `Birdsall 1985`、`Dawson 1983`、`Tajima-Dawson 1979`
- pusher 线已有 `Vay 2008`、`Higuera-Cary 2017`
- PSATD/NCI 线已有 `Godfrey 2014`、`Lehe 2016`、`Kirchen 2016`
- PML 线有较强源码与案例证据，但缺 `LeeCPC2015` 的出版社排版正文
- deposition 线的 `Esirkepov 2001` 作者预印本与 `Villasenor-Buneman 1992` 全文可供公式核查；Esirkepov 的 publisher-formatted CPC PDF 仍是明确的访问边界

因此，这条路线图的核心约束不是“再多下载一些论文”，而是：

1. 优先补能直接改变章节可信度的 primary sources；
2. 严格区分可逐段核查的正文材料和仅有书目信息的线索；
3. 将取得全文、阅读公式和检查章节论断视为同一条证据链。

做到这三点，第 9 章才不是附录式书单，而是读者判断全书证据质量的导航章。

## 9.11 练习与复核

### 9.11.1 证据层分类练习

从以下五项中各选一项，分别判断它属于 A、B、C 或 D 层，并写出判断所依据的书中路径：`Birdsall 1985`、`Yee 1966`、`Esirkepov 2001` 作者预印本、Tajima 1982 FNAL 相关会议稿、`LeeCPC2015` accepted manuscript。答案必须同时写出“可以支持的句子”和“不能支持的句子”。例如，不能因为某项有 DOI 或摘要，就把它写成“已完成全文精读”。

### 9.11.2 证据边界复核练习

选择一条 A 层来源和一条 C 层来源，各写一张文献判读卡，分别列出它们支持与不支持的结论。解释为什么材料分类一致只能说明阅读路线自洽，不能证明论文出版社版本已取得，也不能证明 WarpX 运行已复现论文全部结论。

### 9.11.3 延伸阅读排序练习

从 `Hockney-Eastwood`、`Yee 1966`、`Esirkepov 2001` CPC 定稿、`LeeCPC2015` publisher PDF 和 Boris 1970 原始 proceedings 中选出下一项优先阅读或取得的来源。用三列短表说明：它影响哪一章、现有哪一级证据、取得后会澄清哪一个具体边界。若目标仍受访问或许可限制，必须把“继续取得全文”和“先用现有证据理解正文”分成两个独立动作。

### 9.11.4 边界行动卡练习

从以下任意一种情形中选择一项：一篇尚缺目标版本的文献、一个尚未观测到中间 route 的 AMR 问题、一个被 configuration guard 拒绝的组合、一个 RZ axis residual，或一组尚未形成正式阶数的 refinement 结果。按 9.9 的四项格式写出边界行动卡，并给出下一项独立证据应读取或比较的具体对象。答案必须同时包含一句有限的现有结论和一句明确的禁止外推；不能把“继续运行”或“再读论文”当成没有 observable 或材料版本说明的泛泛动作。

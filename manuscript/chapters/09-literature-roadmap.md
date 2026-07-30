# 9. 文献路线与延伸阅读

本书的文献不是装饰，也不是章节末尾统一贴一串 BibTeX。它真正承担三类职责：

1. 给物理结论提供一手来源。
2. 给数值算法和代码实现提供历史与方法边界。
3. 给独立分析、benchmark 和 regression 判据提供外部对照。

因此本章不把文献写成“推荐书单”，而是按证据强度和章节用途组织阅读路线：哪些来源能够支撑公式与机制，哪些只可提供历史线索，哪些问题仍应保留为开放边界。文献索引中的候选条目只能帮助定位主题；题名、DOI 或摘要不能替代全文阅读、公式核对和章节证据。

## 本章的读者用法：文献是论证工具，不是书目清单

读者不需要先把全部文献读完再学习 PIC。每篇文献在本书中只承担一个明确任务：解释一个物理概念、给出一个离散算法、提供历史边界，或作为某个诊断量的外部参照。遇到文献引用时，建议连续问三件事：

1. 这篇来源支持正文中的哪一句话，支持的是公式、机制还是历史事实？
2. 相关 WarpX 源码与运行案例分别提供了哪一层独立证据？
3. 哪一步仍然只是相似性或摘要级线索，不能写成“论文已经证明 WarpX 实现”？

这样读，文献路线就服务于教程的理解路径：第 1-2 章优先建立 kinetic/PIC 基础，第 4-6 章用 pusher、deposition 和 solver 文献解释离散选择，第 7 章用边界文献校准 PML/AMR 的历史语义，第 8 章再把外部理论与实际诊断对照。未取得全文或尚未完成逐段核对的来源只定义结论边界，不改变读者从概念到实现再到验证的主线。

## 9.1 文献证据的使用层级

本书使用的文献证据有四层，强度不能混写：

| 层级 | 本书中的典型形态 | 可支持的写法 | 限制 |
|---|---|---|---|
| A. 全文可核查 | PDF、MinerU Markdown、图像和中文讲解均已具备 | 可直接作为正文一手证据 | 仍需对照具体公式、图和段落，而不是只看中文摘要 |
| B. 已取得待精读 | PDF 已具备，但尚无完整中文讲解或章节回填 | 可作为“已取得、待精读”的明确线索 | 不能把具体公式或图表当成已核实正文 |
| C. 书目信息/摘要线索 | DOI、题名、摘要和可访问的书目信息 | 可作为获取边界、章节缺口或延伸阅读线索 | 不能把摘要内容冒充成论文正文结论 |
| D. 旁证或相关文献 | 主题相关但不是当前章的主引用，或并非同一 bibliographic item | 可作背景、旁证、术语线索 | 不能替代主引用本身 |

阅读和写作时应遵守：

- 只有 A 层全文可核查来源，才允许在正文里写成“已核实的一手证据”。
- B 层来源只能写成“已取得但尚待逐段讲解”。
- C 层和 D 层只能写成获取线索或背景边界，不能抬成正文论证。

这条规则尤其影响尚未完成全文或版本差异核对的 `Hockney-Eastwood`、`Yee 1966`、`Esirkepov 2001`、`Villasenor-Buneman 1992` 和 `LeeCPC2015`。

## 9.2 支撑各章的核心文献

本书已有可核查全文来源的核心文献主要集中在三条主线。

### 9.2.1 PIC foundations

可供深入阅读的起点是 `Birdsall-Langdon 1985`、`Tajima-Dawson 1979`、`Dawson 1983`、`Vranic 2015` 和 `Muraviev 2021`。仓库的 `references/` 目录按主题保留这些材料的检索入口；第一次阅读应先从本章所标出的概念和结论进入，而不是按目录名逐个翻找。

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
| 第 9 章 文献路线 | 本章即路线图 | A/B/C/D 层级与 `docs/literature-map.md` | 新来源必须按证据层级重新归类 |

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

## 9.6 文献索引的使用边界

仓库内的 `docs/literature-map.md` 不只是 BibTeX key 列表，而是承担三种作用：

1. 统计可用 PDF / topic 分布；
2. 标明哪些核心文献已有可核查阅读资产；
3. 标明哪些来源目前只有书目信息或相关旁证。

但它仍然是总索引，不适合直接拿来替代章节级写作清单。章节写作时更合理的做法是：

- 第 1 / 2 章先看 `docs/foundations-literature-list.md`
- 第 6 / 7 章结合 `references/06_stability_filtering_nci/` 与 `references/08_boundaries_pml_geometry/`
- 查找尚未取得的来源时，再回到 `docs/literature-map.md` 和 `references/00_index/books_to_locate.md`

也就是说，`literature-map` 是总表，不是每章的最终操作手册。

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

### 9.7.1 文献索引的核查边界

本章的 A/B/C/D 层级、核心目录和文献地图必须保持一致。这种一致性只说明索引没有自相矛盾；它不证明中文讲解已经逐式审校，不证明预印本与出版社排版版逐页等价，也不把 WarpX 运行结果升级为论文全部物理结论的验证。读者据此判断引用强度时，应始终回到具体 PDF、公式和源码案例，而不是把索引条目当成证明本身。

## 9.8 成书的已知证据边界

本书把“文献尚无全文”“代码路径尚无运行数据”“数值结论尚未闭合”和“第三方材料能否公开再分发”分开处理，避免把不同类型的不确定性混成一句模糊的限制。对读者而言，最重要的是先识别不确定性属于哪一类：缺少一手文献时不能补成公式结论；没有运行数据时不能补成程序行为；收敛或守恒边界未闭合时不能补成物理正确性。重复计算的 slope 一致性只能说明该组重复计算相符；它不等于 formal numerical order，也不等于 axis charge correctness。

本书采用的分类纪律是：`OPEN_EXTERNAL_ACCESS` 不是下载失败的同义词，而是没有合法可读取的目标全文；`PRE_PHYSICS_BOUNDARY` 表示尚未进入物理推进，不能写成 physics PASS/FAIL；`RUNTIME_LEDGER_UNPROVEN` 表示源码与数据结构已有，但真实运行尚未给出所需记录；`CONVERGENCE_READINESS_WITH_FORMAL_ORDER_UNPROVEN` 表示可以计算描述性 order，但不能宣称正式阶数。

因此，缺口登记只是帮助读者回查限制的索引，不是替代论文、源码或运行结果的证明。

## 9.9 本章结论

本书的文献部分已经能支撑核心主线，但还没有让所有一手来源都达到逐段核查的程度。更准确的概括是：

- foundations 线已有 `Birdsall 1985`、`Dawson 1983`、`Tajima-Dawson 1979`
- pusher 线已有 `Vay 2008`、`Higuera-Cary 2017`
- PSATD/NCI 线已有 `Godfrey 2014`、`Lehe 2016`、`Kirchen 2016`
- PML 线有较强源码与案例证据，但缺 `LeeCPC2015` 的出版社排版正文
- deposition 线的 `Esirkepov 2001` 作者预印本与 `Villasenor-Buneman 1992` 全文可供公式核查；Esirkepov 的 publisher-formatted CPC PDF 仍是明确的访问边界

因此，这条路线图的核心约束不是“再多下载一些论文”，而是：

1. 优先补能直接改变章节可信度的 primary sources；
2. 严格区分可逐段核查的正文材料和仅有书目信息的线索；
3. 将取得全文、阅读公式和回填章节视为同一条证据链。

做到这三点，第 9 章才不是附录式书单，而是读者判断全书证据质量的导航章。

## 9.10 练习与复核

### 9.10.1 证据层分类练习

从以下五项中各选一项，分别判断它属于 A、B、C 或 D 层，并写出判断所依据的书中路径：`Birdsall 1985`、`Yee 1966`、`Esirkepov 2001` 作者预印本、Tajima 1982 FNAL 相关会议稿、`LeeCPC2015` accepted manuscript。答案必须同时写出“可以支持的句子”和“不能支持的句子”。例如，不能因为某项有 DOI 或摘要，就把它写成“已完成全文精读”。

### 9.10.2 证据边界复核练习

选择一条 A 层来源和一条 C 层来源，对照 `docs/public-evidence-index.md` 中的记录，分别写出它们支持与不支持的结论。解释为什么索引一致只能说明“路线图与可用材料一致”，不能证明论文出版社版本已取得，也不能证明 WarpX 运行已复现论文全部结论。

### 9.10.3 延伸阅读排序练习

从 `Hockney-Eastwood`、`Yee 1966`、`Esirkepov 2001` CPC 定稿、`LeeCPC2015` publisher PDF 和 Boris 1970 原始 proceedings 中选出下一项优先阅读或取得的来源。用三列短表说明：它影响哪一章、现有哪一级证据、取得后会澄清哪一个具体边界。若目标仍受访问或许可限制，必须把“继续取得全文”和“先用现有证据理解正文”分成两个独立动作。

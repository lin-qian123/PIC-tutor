# 9. 文献路线与后续扩写计划

本书的文献不是装饰，也不是章节末尾统一贴一串 BibTeX。它真正承担三类职责：

1. 给物理结论提供一手来源。
2. 给数值算法和代码实现提供历史与方法边界。
3. 给 reader-side analysis、benchmark 和 regression 判据提供外部对照。

因此本章不再把文献简单列成“推荐阅读书单”，而是把当前项目里已经 materialize 的论文资产、仍未闭环的 acquisition 缺口，以及它们与各章的绑定关系写成一张可执行路线图。

对于全局 BibTeX 中尚未进入正式主题的条目，`docs/literature-pending-triage.md` 提供保守的候选主题、章节入口、优先级和下一步获取动作。它只是一张 acquisition/read queue：标题关键词不能替代全文阅读、MinerU 转换、逐段核对或正式章节证据。

## 9.1 当前项目的文献证据分层

当前本地文献证据有四层，强度不能混写：

| 层级 | 当前项目中的典型形态 | 可支持的写法 | 当前限制 |
|---|---|---|---|
| A. 已 materialize 的正文资产 | 本地 PDF + MinerU Markdown + `images/` + 中文讲解 + `reading-log.md` | 可直接作为正文一手证据 | 仍需作者自己对照具体公式、图和段落，而不是只看中文摘要 |
| B. 已取得 PDF 但未完成精读 | 本地 PDF 存在，但还没有完整中文讲解或章节回填 | 可作为“已获取、待精读”的明确线索 | 不能把具体公式或图表当成已核实正文 |
| C. metadata / abstract 级线索 | DOI、题名、摘要、访问审计、下载日志 | 可作为 acquisition 边界、章节缺口或后续计划 | 不能把摘要内容冒充成论文正文结论 |
| D. 旁证或相关文献 | 主题相关但不是当前章的主引用，或并非同一 bibliographic item | 可作背景、旁证、术语线索 | 不能替代主引用本身 |

当前项目的规则应保持为：

- 只有 A 层资产，才允许在正文里写成“已核实的一手证据”。
- B 层资产只能写成“已获取但尚待逐段讲解”。
- C 层和 D 层只能写成 acquisition / 背景边界，不能抬成正文论证。

这条规则尤其影响当前仍未闭环的 `Hockney-Eastwood`、`Yee 1966`、`Esirkepov 2001`、`Villasenor-Buneman 1992` 和 `LeeCPC2015`。

## 9.2 当前已 materialize 的核心文献树

按当前 `references/` 目录，已经完成 materialization 的核心文献主要集中在三条主线。

### 9.2.1 PIC foundations

当前已 materialize：

- `references/02_books_lecture_notes/1985_BirdsallLangdon_Plasma_physics_via_computer_simulation/`
- `references/03_pic_foundations/1979_TajimaDawson_Laser_Electron_Accelerator/`
- `references/03_pic_foundations/1983_Dawson_Particle_simulation_of_plasmas/`
- `references/03_pic_foundations/2015_Vranic2015_Particle_merging_algorithm_for_PIC_codes/`
- `references/03_pic_foundations/2021_MuravievCPC2021_Strategies_for_particle_resampling_in_PIC_simulations/`

其中 `TajimaDawson1979` 现已通过独立的 `runs/stage-c-validation/tajima-dawson-1979-asset/contract.{json,md}` 收口为 paper-backed full-text asset：4 页 PDF、MinerU Markdown、11 张图和中文精读均已存在。它支撑的是最早期 `driver -> wake -> trapping -> acceleration` 与 LWFA scaling；合同同时保留“不替代现代 WarpX regression”的边界。

这些基础资产已经足以支撑：

- 第 1 章的 superparticle、weighted particles、finite-size particles、quiet start、噪声与 heating 讨论；
- 第 2 章的最小 PIC loop、electrostatic / EM / Darwin 模型边界；
- 第 8 章中 diagnostics、spectrum、correlation time、weak instability dynamic range 的讨论；
- LWFA 最早 scaling baseline 的历史入口。

Vranic 2015 进一步补上了粒子 merge/resampling 这条应用线：论文专属目录、24 页 PDF、MinerU Markdown、32 张图、中文讲解和独立 asset contract 均已存在。它支撑第 4 章对“两粒子局部守恒 merge”的 paper-backed 解释，但不替代 WarpX `VelocityCoincidenceThinning` 的逐行等价或 dedicated runtime consumer。

Muraviev 2021 将这条应用线扩展为完整的 resampling 方法谱系：论文专属目录、50 页 PDF、MinerU Markdown、38 个图像资源、中文精读和独立 asset contract 均已存在。它支撑第 4 章对 agnostic down-sampling、局部权重噪声、严格守恒 thinning 和 merge/cluster 权衡的 paper-backed 解释，但论文的 PICADOR/hi-chi QED cascade 结果不替代 WarpX runtime evidence。

其中 `Birdsall 1985` 因原书过长，当前项目采用分卷 PDF + 分卷 MinerU 的方式处理；这意味着它已经是 A 层资产，但仍不是“整本都已完全精读”。

### 9.2.2 Particle pusher

当前已 materialize：

- `references/04_particle_pushers_deposition_shapes/2008_VayPOP2008_Simulation_of_beams_or_plasmas_crossing_at_relativistic_velocity/`
- `references/04_particle_pushers_deposition_shapes/2017_HigueraPOP2017_Structure-preserving_second-order_integration_of_relativistic_charged_particle_trajectories_in_electromagnetic_fields/`

这两条线当前已经足以支撑：

- 第 4 章对 Vay pusher 与 Higuera-Cary pusher 的源码讲解；
- `Source/Particles/Pusher/UpdateMomentumVay.H` 与 `UpdateMomentumHigueraCary.H` 的公式对表；
- “相对论精度”和“结构保持”两条不同的算法卖点。

但这条模块还没有完成 `Boris` 原始文献闭环，因此第 4 章仍不是“推进器历史谱系全闭环”。

### 9.2.3 PSATD / Galilean / boosted-frame / NCI

当前已 materialize：

- `references/06_stability_filtering_nci/2014_GodfreyJCP2014_Numerical_stability_analysis_of_the_PSATD_PIC_algorithm/`
- `references/06_stability_filtering_nci/2016_KirchenPOP2016_Stable_discrete_representation_of_relativistically_drifting_plasmas/`
- `references/06_stability_filtering_nci/2016_LehePRE2016_Elimination_of_NCI_by_Galilean_coordinates/`

本版又 materialize `references/01_reviews_surveys/2014_VayFRACAD2014_Modeling_of_relativistic_plasmas_with_the_Particle-In-Cell_method/`：9 页 PDF、MinerU Markdown、43 张图片、论文顺序中文精读、access audit、reading log 和 asset contract。它为第 4 章的 Boris/Vay pusher 谱系、第 6 章的 PSATD/NCI 机制提供统一 review 入口；它不替代当前 WarpX 的源码 crosswalk、runtime contract 或论文图形逐点复现。

这三条线已经构成第 6 章目前最完整的一组 paper-backed 主干：

- Godfrey 2014：fixed-grid PSATD 的 NCI 策略分类；
- Lehe 2016：Galilean coordinates 消除 NCI 的核心离散论证；
- Kirchen 2016：boosted-frame workflow 与稳定离散表示之间的应用层连接。

本版又 materialize `Andriyash 2016`：`references/03_pic_foundations/2016_AndriyashPoP2016_Laser-plasma_interactions_with_a_Fourier-Bessel_particle-in-cell_method/` 保存 9 页 PDF、MinerU Markdown、26 张图片、论文顺序中文精读和 asset contract。它把 quasi-cylindrical Fourier-Bessel basis、PSATD 解析时间推进、`m±1` 横向 mode coupling 和 current-correction 公式从 PDF-only 线索推进为可引用的全文资产；但 PLARES-PIC 与 WarpX 的函数级等价、WarpX runtime reproduction 和论文图逐点复现仍保持边界。

因此第 6 章当前虽然仍有 runtime validation 和 upstream handoff 的工程缺口，但在文献层已经不再是空心章节。

## 9.3 当前最突出的未闭环文献缺口

以 `TajimaDawson1982` 为例，当前应把“正式来源已确认”和“正文已取得”分开记录：Crossref/AIP 元数据确认 *AIP Conference Proceedings* `91(1):69-93`、DOI `10.1063/1.33805` 及 canonical resource `https://pubs.aip.org/aip/acp/article/91/1/69-93/612300`；2026-07-13 本机请求该页面返回 Cloudflare HTTP `403`，所以本书不把 publisher PDF、MinerU Markdown 或逐式核对标记为已完成。FNAL 的 `p169.pdf` 是 Tajima 单作者的相关会议稿，只能作为主题旁证，不能替代 Tajima–Dawson 正式条目。

本轮已将这份相关会议稿的实际全文资产 materialize 到 `references/03_pic_foundations/1982_Tajima_related_FNAL_conference_note_Laser_accelerator_by_plasma_waves/`：本地 PDF 为 26 页，附 MinerU Markdown、67 张抽取图、论文顺序中文讲解、access audit、reading log 和 `runs/stage-c-validation/tajima-1982-related-note/contract.{json,md}`。这使本书可以在有限边界内直接讲解 beat-wave 共振、前向 Raman 散射、电子俘获、退相位、自聚焦、丝化和相对论前向 Brillouin 散射；但该资产明确是 related single-author conference note，正式 Tajima--Dawson AIP item 仍是独立的全文缺失缺口。

如果按“哪一章会因为缺它而不够出版级”排序，当前最重要的缺口不是更多新论文，而是以下几条老而关键的 primary sources。

| 缺口 | 当前状态 | 主要影响章节 | 当前可替代程度 |
|---|---|---|---|
| `Hockney-Eastwood` 原书 | 仅有 BibTeX 与 fallback article 线索；无本地合法 PDF | 第 1、2、5、6 章 | 只能部分由 `Birdsall 1985` 与 `Dawson 1983` 顶住 |
| `Yee 1966` | metadata/DOI 已清楚；无本地 PDF/MinerU | 第 2、6 章 | 可暂由源码与后继 FDTD 文献支撑，但缺原始历史入口 |
| `Esirkepov 2001` | 已建立 paper-specific 目录、access audit，并已 materialize 作者 arXiv 预印本 + MinerU + 中文讲解；仍缺出版商 CPC PDF 对照 | 第 5 章 | 已从纯源码缺口推进到 preprint-backed，但还未完成 CPC 定稿核对 |
| `Villasenor-Buneman 1992` | 已建立 paper-specific 目录、access audit，并已 materialize 本机现成 PDF + MinerU + 中文讲解 | 第 5 章 | 已从纯源码缺口推进到 paper-backed，但中文讲解仍是第一轮结构精读 |
| `Andriyash 2016` | 已 materialize 9 页 PDF、MinerU、26 张图、中文精读和 asset contract；来源是 quasi-cylindrical Fourier-Bessel PSATD | 第 6 章 RZ PSATD | 已从 PDF-only 推进到 full-text formula-backed；PLARES-PIC/WarpX 等价和 runtime reproduction 仍未完成 |
| `LeeCPC2015` | 已有 7 页 eScholarship accepted/submitted manuscript、MinerU、13 张图、中文讲解和 source crosswalk；仍缺 publisher-formatted CPC PDF | 第 7 章 | accepted-manuscript-backed + source-grounded 已成立，但发表版差异和逐系数等价仍未完成 |

这五条缺口里，`LeeCPC2015` 最特殊。它不是完全没工作，而是已经推进到：

- `access-audit.md`
- `公式映射准备.md`
- `公式核对清单.md`

也就是说，当前不是“不知道该怎么读”，而是“accepted manuscript 已可精读，仍缺 publisher-formatted CPC PDF 的版本差异核对”。

## 9.4 各章当前的文献成熟度

把全书按章节看，当前文献成熟度并不均匀。

| 章节 | 当前文献成熟度 | 主要已闭环来源 | 主要缺口 |
|---|---|---|---|
| 第 1 章 动理学模型 | 中等 | `Birdsall 1985`、`Dawson 1983` | `Hockney-Eastwood`、更细的 particle-mesh heating 原始文献 |
| 第 2 章 PIC 总循环 | 中等 | `Birdsall 1985`、`Dawson 1983` | `Yee 1966` 原始入口 |
| 第 3/3A 章 主循环与初始化 | 中低 | 以源码为主 | 需要把基础文献和工程论文绑定得更明确 |
| 第 4 章 粒子推进器 | 中高 | `Boris 1970` metadata contract、`Birdsall 1985`、`Vay 2008`、`Higuera-Cary 2017` | 原始 Boris 1970 会议论文 PDF 仍缺 |
| 第 5 章 沉积与形函数 | 中等 | Esirkepov 与 Villasenor 两条 charge-conserving 主线都已有第一轮 paper-backed 资产 | 仍需把两篇论文系统回写正文；Esirkepov 还缺 CPC 定稿对照 |
| 第 6 章 场求解器 | 高 | `Vay--Godfrey 2014`、`Godfrey 2014`、`Lehe 2016`、`Kirchen 2016` | 更多 validation/engineering 线，而不是 paper 主干 |
| 第 7 章 边界、PML 与 AMR | 中等偏低 | `Berenger 1994/1996` 有 bibliographic anchor，源码和 regression 很强 | `LeeCPC2015` 正文仍缺 |
| 第 8 章 诊断、验证与案例 | 中等 | `Dawson 1983` diagnostics 思路已可直接服务正文 | 还缺更多 case-specific benchmark papers |
| 第 9 章 文献路线 | 本章即路线图 | 当前 `references/` 树和 `docs/literature-map.md` | 需要持续同步，而不是一次性写完 |

这个表最重要的结论是：当前项目最缺 paper-backed 收口的不是第 6 章，而是第 5 章和第 7 章。

## 9.5 acquisition 优先级的重新排序

基于当前项目状态，后续 acquisition 不应再泛泛地“多找一些相关论文”，而应按成书影响排序：

1. `Esirkepov 2001` 的 CPC 定稿 PDF
   - 当前已有作者预印本，可支持第一轮论证；下一步是把预印本与 2001 CPC 发表版逐项对齐。
2. `Yee 1966`
   - 直接补第 2 / 6 章里的原始 FDTD 入口。
4. `LeeCPC2015` 正文 PDF
   - 直接补第 7 章的 PML paper closure。
5. `Hockney-Eastwood` 或其 article-level fallback
   - 继续补第 1 / 2 章的 particle-mesh foundations。
6. `Boris` 原始文献
   - 已建立 `1970_Boris_Relativistic_plasma_simulation_optimization_of_a_hybrid_code` 的 metadata/access contract；DTIC PDF 仍受限流，当前只把书目身份固定下来。
   - 下一步是通过 DTIC 重试、机构访问或合法镜像获取原始 proceedings PDF，再补 MinerU 和逐页核对；在此之前不把 Birdsall 二手推导写成 Boris 原文证据。
   - 继续补第 4 章的 pusher 历史链。

这个顺序和早期版本相比已经变了。原因很简单：第 6 章现在已有较强 paper 主干，而第 5 / 7 章的 paper closure 反而更薄。

## 9.6 对 `docs/literature-map.md` 的使用边界

当前 `docs/literature-map.md` 已经不只是“列一下 BibTeX key”，而是承担三种作用：

1. 统计当前本地 PDF / topic 分布；
2. 记录哪些核心文献已经 materialize；
3. 记录哪些缺口当前只有 metadata / audit / fallback。

但它仍然是总索引，不适合直接拿来替代章节级写作清单。章节写作时更合理的做法是：

- 第 1 / 2 章先看 `docs/foundations-literature-list.md`
- 第 6 / 7 章结合 `references/06_stability_filtering_nci/` 与 `references/08_boundaries_pml_geometry/`
- acquisition 计划再回到 `docs/literature-map.md` 和 `references/00_index/books_to_locate.md`

也就是说，`literature-map` 是总表，不是每章的最终操作手册。

## 9.7 下一轮最合理的文献推进目标

如果下一轮继续走“一个大模块一个版本”的节奏，那么在本轮闭合 Muraviev resampling 资产后，最合理的文献模块不再是第 6 章，而是下面两条中的一条：

### 方案 A：第 5 章沉积文献闭环

目标：

- compare the current `Esirkepov 2001` arXiv preprint against the 2001 CPC publication PDF
- deepen the current first-round Villasenor and Esirkepov Chinese notes into fuller formula-level walkthroughs
- 把第 5 章从源码校准推进到论文-源码-测试三线闭环

适合原因：

- 当前第 5 章是全书里最明显的“代码已读、文献未补”的章节之一；
- 这条线一旦闭合，会显著提升前半本书的基础可信度。

### 方案 B：第 7 章 PML 论文闭环

目标：

- 继续推进 `LeeCPC2015` 正文获取
- 若正文仍不可得，则至少把 `Berenger 1994/1996` 与 WarpX `PsatdAlgorithmPml.cpp` 的公式映射继续压实

适合原因：

- 当前第 7 章源码和 regression 已经很强，只差 paper 正文闭环；
- 一旦拿到 `LeeCPC2015` 正文，整章会从“强源码章”变成真正的 paper-backed 章节。

在这两者之间，当前更推荐先走方案 A。原因是：

- 方案 A 不强依赖外部授权状态；
- 方案 B 仍可能被 PDF 获取问题卡住。

### 9.7.1 文献资产与路线图同步合同

本章的路线图现在由 `scripts/audit_literature_roadmap_asset_contract.py` 做仓库内一致性检查。当前合同覆盖 A/B/C/D 证据层定义、核心文献目录、`docs/literature-map.md` 与生成式 inventory 的锚点，以及 `TajimaDawson1982`、`Esirkepov 2001`、`LeeCPC2015`、`Yee 1966`、`Hockney-Eastwood` 的缺口声明。Muraviev 2021 的专属资产合同另行检查全文、公式、图像和第 4 章映射。报告见 `runs/stage-c-validation/literature-roadmap-asset-contract/contract.{json,md}` 与 `runs/stage-c-validation/muraviev-2021-paper-asset/contract.{json,md}`。

这个合同只说明“路线图与项目内资产状态一致”，不证明中文讲解已经逐式审校，不证明预印本与出版社排版版逐页等价，也不把 WarpX runtime 结果升级为论文全部物理结论的验证。后续新增或替换 primary source 时，应先更新合同，再同步本章与 `references/00_index`。

## 9.8 当前成书缺口登记

v0.85 已把第二组 formal convergence family 的 12 组固定 2-rank producer runner 和 preflight 接入项目；当前本机缺少 `mpiexec/mpirun`，分类为 `REPEAT_FAMILY_RUNNER_BLOCKED_MPI_LAUNCHER_MISSING`。v0.84 的 norm、observable、拟合区间、负对照和重复 family 预注册继续保留。当前每种 geometry 仍只有一组独立 family，correction-on axis charge 仍是 boundary，因此不把 descriptive slope 写成 formal order，也不把不同 geometry pooled。正式收敛阶、人工全书通读、第三方材料许可和公开再分发仍需单独签收。

文献路线图需要和运行/编辑缺口分开管理，否则“论文缺全文”和“代码没有 route ledger”会在 TODO 中互相遮蔽。当前项目把缺口登记在 `docs/current-book-gap-register.md`，每一行绑定证据、分类、下一步动作和关闭条件。当前八项缺口分别覆盖两条 publisher access、三条 runtime/source boundary、一条 RZ physics boundary、一条 formal convergence study 和一条 release editorial gate。

本登记表的分类纪律是：`OPEN_EXTERNAL_ACCESS` 不是下载失败的同义词，而是当前没有合法可读取的目标全文；`PRE_PHYSICS_BOUNDARY` 表示尚未进入物理推进，不能写成 physics PASS/FAIL；`RUNTIME_LEDGER_UNPROVEN` 表示源码与 schema 已有，但真实 producer 尚未输出账本；`CONVERGENCE_READINESS_WITH_FORMAL_ORDER_UNPROVEN` 表示可以计算描述性 order，但不能宣称正式阶数。

该表由 `scripts/audit_current_gap_register.py` 检查。合同通过仅表示当前正文和证据目录对同一组缺口使用一致口径，不表示本书已经达到终稿。

## 9.9 本章结论

当前项目的文献工作已经跨过了“只有书目，没有正文资产”的阶段，但还远未到“全书 primary sources fully closed”的阶段。可以更准确地概括成：

- foundations 线已有 `Birdsall 1985`、`Dawson 1983`、`Tajima-Dawson 1979`
- pusher 线已有 `Vay 2008`、`Higuera-Cary 2017`
- PSATD/NCI 线已有 `Godfrey 2014`、`Lehe 2016`、`Kirchen 2016`
- PML 线已有较强源码与审计资产，但缺 `LeeCPC2015` 正文
- deposition 线当前已建立 `Esirkepov 2001` 与 `Villasenor-Buneman 1992` 的 paper-specific 目录与 access audit；其中 `Esirkepov 2001` 已 materialize 作者 arXiv 预印本并完成第一轮 MinerU/中文讲解，`Villasenor-Buneman 1992` 也已从本机现成 PDF/MinerU 资产 materialize 到项目目录并完成第一轮中文讲解

因此，这条路线图给后续推进的核心约束不是“再多下载一些论文”，而是：

1. 优先补能直接改变章节可信度的 primary sources；
2. 严格区分 materialized 正文资产和 metadata-level 线索；
3. 把 acquisition、MinerU、中文精读和章节回填继续绑成同一条工作流。

做到这三点，第 9 章才不是一个附录式书单，而是真正控制全书证据质量的总调度章。

## 9.10 练习与复核

### 9.10.1 证据层分类练习

从以下五项中各选一项，分别判断它属于 A、B、C 或 D 层，并写出判断所依据的本地路径：`Birdsall 1985`、`Yee 1966`、`Esirkepov 2001` 作者预印本、Tajima 1982 FNAL 相关会议稿、`LeeCPC2015` accepted manuscript。答案必须同时写出“可以支持的句子”和“不能支持的句子”。例如，不能因为某项有 DOI 或摘要，就把它写成“已完成全文精读”。

### 9.10.2 合同复核练习

在项目根目录运行：

```bash
python scripts/audit_literature_roadmap_asset_contract.py \
  --project-root . \
  --output-json runs/stage-c-validation/literature-roadmap-asset-contract/contract.json \
  --output-md runs/stage-c-validation/literature-roadmap-asset-contract/contract.md
```

然后将合同中的 `12/12 PASS` 与 `docs/public-evidence-index.md` 中对应记录对照。解释为什么合同通过只能证明“路线图与本地资产一致”，不能证明论文出版社版本已取得，也不能证明 WarpX runtime 已复现论文全部结论。

### 9.10.3 acquisition 排序练习

从 `Hockney-Eastwood`、`Yee 1966`、`Esirkepov 2001` CPC 定稿、`LeeCPC2015` publisher PDF 和 Boris 1970 原始 proceedings 中选出下一项 acquisition 目标。用三列短表说明：它影响哪一章、当前已有哪一级证据、取得后会关闭哪一个具体边界。若目标仍受访问或许可限制，必须把“继续获取”和“先用现有证据回填正文”分成两个独立动作。

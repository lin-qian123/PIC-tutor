# Esirkepov 2001 CPC：发表版摘要与 arXiv 预印本 bounded compare

审计日期：2026-07-13

## 证据边界

发表版条目是 T. Zh. Esirkepov, “Exact charge conservation scheme for Particle-in-Cell simulation with an arbitrary form-factor,” *Computer Physics Communications* 135(2), 144--153 (2001), DOI `10.1016/S0010-4655(00)00228-9`。ScienceDirect 的公开索引页仍可读取标题、卷页和摘要，但当前环境不能取得 publisher-formatted PDF；ResearchGate 记录也明确显示全文需要向作者请求。因此下面是 **indexed-abstract compare**，不是发表版全文逐页核对。

## 摘要级对照

| 主题 | 发表版公开索引摘要 | 本地 arXiv 预印本摘要 | 当前结论 |
|---|---|---|---|
| 方法对象 | Cartesian geometry 中的 local electric current density assignment | alternative to solving Poisson equation 的 exact-continuity current construction | 一致，均指向 source-side charge-conserving current |
| form-factor | arbitrary quasi-particle form-factor | 至少适用于由一维 form-factor 乘积构成的 n-dimensional form-factor | 发表版摘要更概括；预印本摘要给出更具体的适用表述 |
| 轨迹假设 | quasi-particle trajectory over one time step is straight | 预印本摘要未用同样完整句式，但正文与本地精读包含 straight-line/endpoint 构造 | 发表版摘要级事实已确认；正文细节仍以预印本资产为准 |
| Poisson solve | allows PIC code without solving Poisson equation | 以 continuity-equation construction 作为 Poisson alternative | 叙述一致，发表版摘要强调实现后果 |
| 唯一性 | unique linear combination of form-factor differences consistent with discrete continuity | density decomposition is the only possible linear procedure | 核心 claim 一致，只是术语从 density decomposition 展开为 form-factor differences |
| demonstration | 2D and 3D computation scheme | parabolic spline form-factor demonstration | 发表版摘要确认维度范围；预印本摘要补充示例 form-factor，不能据此推断发表版正文改动 |

## 对第 5 章的影响

这项 compare 允许正文把以下内容标记为 `publication-metadata + indexed-abstract verified`：Cartesian local current assignment、arbitrary quasi-particle form-factor、straight-line trajectory assumption、无需 Poisson solve、离散连续性下的唯一线性组合、2D/3D demonstration。`Eq.(23)` 的具体排版、发表版 section numbering、二阶 spline 段落和图表仍只能标记为 `preprint-backed + source-grounded`。

因此本章的最强准确表述更新为：**Esirkepov 的发表版身份与摘要级算法主张已核实，预印本公式与当前 WarpX 源码/runtime 已完成三层交叉复核；publisher-PDF line-by-line compare 仍未完成。** 这不是把摘要升级为全文，而是把已获得的公开证据精确归类。

## 来源

- Publisher indexed article/abstract: <https://www.sciencedirect.com/science/article/pii/S0010465500002289>
- Publisher PDF endpoint: <https://www.sciencedirect.com/science/article/pii/S0010465500002289/pdf?md5=526385691a2c427ee41e96a0bfbd1d3b&pid=1-s2.0-S0010465500002289-main.pdf>
- Author-posted preprint: <https://arxiv.org/abs/physics/9901047>
- Access audit: `references/04_particle_pushers_deposition_shapes/2001_EsirkepovCPC2001_Exact_charge_conservation_scheme_for_Particle-In-Cell_simulation_with_an_arbitrary_form-factor/access-audit.md`

# Esirkepov 2001 CPC：发表信息与预印本的 bounded compare

## 目的

第 5 章已经可以用作者 arXiv 预印本支撑 `density decomposition`、`Eq.(23)` 和二阶 spline 算法骨架，但不能把预印本直接当作 2001 年 CPC 定稿。本文把当前能够独立核实的发表信息、预印本内容和仍然缺失的比较项分开记录。

## 当前已核实的事实

| 项目 | 当前证据 | 结论 |
|---|---|---|
| 预印本 | arXiv `physics/9901047`，1999-01-26 提交 | 题名为 `Exact charge conservation scheme for Particle-in-Cell simulations for a big class of form-factors`；页面标注 13 页、无图、10 条参考文献 |
| 发表版书目 | CPC 135(2), 144-153 (2001)；DOI `10.1016/S0010-4655(00)00228-9` | 题名为 `Exact charge conservation scheme for Particle-in-Cell simulation with an arbitrary form-factor` |
| 发表版摘要 | 公开书目/摘要索引 | 摘要口径仍指向 Cartesian geometry、任意 quasi-particle form-factor、直线轨迹、离散连续性和 2D/3D demonstration |
| 发表版全文 | 当前环境对 ScienceDirect article/PDF 端点受限，项目内没有独立 CPC publisher PDF | 不能声称完成逐页、逐式、版面级 compare |

## 对第 5 章可以直接采用的边界

当前可以稳定使用预印本支撑以下主线：

1. 离散连续性方程是 current deposition 的目标，而不是 direct `qvS` 的自动结果；
2. `density decomposition` 把总 shape difference 拆成三个方向分量；
3. 二阶 spline 路径中的 `1/3`、`1/6` mixed averages 对应 WarpX 的 `one_third`、`one_sixth`；
4. WarpX 的 `sdxi/sdyj/sdzk` prefix loops 可以作为这组方向分解的程序化实现来解释。

这些结论来自项目内已下载并经 MinerU 转换的 arXiv 预印本，以及同级 `../warpx` 源码核对。它们不依赖把预印本排版误称为 CPC 定稿。

## 尚未完成的五项 compare

以下项目仍需取得 publisher PDF 或合法的等价全文后才能关闭：

1. title wording 之外的 abstract 逐句差异；
2. section titles、编号和小节顺序是否发生编辑变化；
3. `Eq.(23)` 及其前后 density-decomposition 公式的编号、排版和符号；
4. second-order spline algorithm 段落是否有删改或补充；
5. 参考文献、页码和发表版图表/版式的最终核对。

因此当前证据等级应写成：**preprint-backed + source-grounded，发表书目信息已核实，publisher-PDF line-by-line compare 未完成**。

2026-07-12 又检查了 CiNii Research 和 ResearchGate 的可见记录：前者补充 CPC/DOI/版权元数据，后者提供摘要和请求作者全文入口，但二者都没有替代 publisher-formatted PDF。ScienceDirect PDF endpoint 同日仍由本机 `curl -L -I` 返回 `HTTP/2 403`。因此本轮只加强了访问状态证据，不改变“publisher-PDF line-by-line compare 未完成”的结论。

## 来源

- arXiv 预印本页面：<https://arxiv.org/abs/physics/9901047>
- 发表版 DOI：<https://doi.org/10.1016/S0010-4655(00)00228-9>
- 本地预印本、MinerU Markdown、中文讲解和获取审计：本目录下的同名 PDF、`.md`、`-中文讲解.md`、`access-audit.md`。

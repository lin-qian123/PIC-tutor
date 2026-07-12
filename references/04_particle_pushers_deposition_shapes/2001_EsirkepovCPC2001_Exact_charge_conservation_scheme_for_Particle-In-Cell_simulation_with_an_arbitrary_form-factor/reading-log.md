# Reading Log

## 2026-07-02

- 继续推进第 5 章 current deposition 文献闭环时，重新检查了 `Esirkepov 2001` 的合法全文入口。
- 当前未取得 Elsevier `Computer Physics Communications 135(2)` 的出版商 PDF，但确认作者在 arXiv 上公开发布了对应算法的预印本：
  - arXiv: `physics/9901047`
  - 题名：`Exact charge conservation scheme for Particle-in-Cell simulations for a big class of form-factors`
- 已下载并保存到当前论文目录：
  - `2001_EsirkepovCPC2001_Exact_charge_conservation_scheme_for_Particle-In-Cell_simulation_with_an_arbitrary_form-factor.pdf`
- 已通过项目内 `scripts/mineru_convert_stdlib.py` 完成 MinerU 转换，并回收输出到当前目录：
  - `2001_EsirkepovCPC2001_Exact_charge_conservation_scheme_for_Particle-In-Cell_simulation_with_an_arbitrary_form-factor.md`
  - `images/`
- 已开始第一轮中文精读，并生成：
  - `2001_EsirkepovCPC2001_Exact_charge_conservation_scheme_for_Particle-In-Cell_simulation_with_an_arbitrary_form-factor-中文讲解.md`

## 当前判断

- 这份 arXiv 预印本已经足够支持第 5 章对 Esirkepov 路径做第一轮 paper-backed 讲解：
  - 离散连续性方程为何替代 Poisson correction；
  - `W^1 + W^2 + W^3 = S(x+\Delta x)-S(x)` 这条 density decomposition 主约束；
  - 由线性、零位移退化和坐标置换对称性推出“唯一允许”的分解；
  - 二阶 spline 情形下的实际电流计算流程。
- 但它仍不能自动等价于“已完全拿到 2001 CPC 出版版 PDF”：
  - arXiv 题名与出版版略有差异；
  - 需要后续再核对预印本与 CPC 定稿在公式编号、措辞和参考文献上的差别。

## 下一步

- 若后续取得 CPC 出版版 PDF，应做一次逐段比对：
  1. 标题与摘要措辞差异；
  2. `Eq.(23)` 一类 OCR 噪声较大的关键公式；
  3. 章节编号与参考文献条目。
- 在第 5 章正文侧，下一步应优先把本次新增的 paper-backed 论断回填到：
  - `density decomposition`
  - `only possible linear procedure`
  - 二阶 spline 算法步骤
  - 与 WarpX `doEsirkepovDepositionShapeN<N>()` 的边界对应

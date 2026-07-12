# Reading Log

## 2026-07-02

- 继续推进第 5 章 current deposition 文献闭环时，检查本机已有文献资产，发现这篇论文的全文与旧 MinerU 转换结果其实已经存在于本机：
  - 原 PDF：`/Users/yuxiangzhang/Documents/Zoteropaper/calculation/feild solver/Villasenor et al. - 1992 - Rigorous charge conservation for local electromagnetic field solvers.pdf`
  - 现成 MinerU Markdown 与 `images/`：`/Users/yuxiangzhang/Documents/program/minerU/md_output/calculation/feild solver/Villasenor et al. - 1992 - Rigorous charge conservation for local electromagnetic field solvers/`
- 已将这些资产 materialize 到当前论文专属目录：
  - `1992_VillasenorBunemanCPC1992_Rigorous_charge_conservation_for_local_electromagnetic_field_solvers.pdf`
  - `1992_VillasenorBunemanCPC1992_Rigorous_charge_conservation_for_local_electromagnetic_field_solvers.md`
  - `images/`
- 已开始第一轮中文精读，并生成：
  - `1992_VillasenorBunemanCPC1992_Rigorous_charge_conservation_for_local_electromagnetic_field_solvers-中文讲解.md`

## 当前判断

- 这篇论文已经不再是“只有 metadata/access audit 的缺口”，而是已经具备：
  - 本地 PDF；
  - MinerU Markdown；
  - 图片；
  - 第一轮中文讲解。
- 它现在已经足够支撑第 5 章对 Villasenor 路径做第一轮 paper-backed 讲解，重点包括：
  - 为什么 local field solver 要求严格有限差分版本的 charge conservation；
  - 为什么作者强调不把一般二维位移拆成两次正交 move；
  - 四/七/十 boundary move 的粒子 mover 组织方式；
  - 三维扩展里通过 complementary mesh 和 face flux 保持严格守恒。

## 本轮完成

- 已从项目内 MinerU Markdown 逐式核对 four-boundary `Eq.(6)-(9)`、seven/ten-boundary 的重复 four-boundary 分段，以及 3D `Delta x Delta y Delta z / 12` 交叉项。
- 已将公式级结论回填第 5 章，并新增 `notes/code-reading/particles/45-villasenor-formula-level-audit.md` 作为 paper-to-source 审计记录。

## 下一步

- 继续把这篇论文的中文讲解从“公式级审计”推进到出版级逐段讲解，尤其补强：
  1. 四边界电流公式与 `Eq.(6)-(9)` 的逐式解释；
  2. 七/十边界拆分与 WarpX segment loop 的对位；
  3. 三维 `\Delta x \Delta y \Delta z / 12` 项与 tight stencil 叙述之间的关系。
- 在第 5 章正文侧，下一步应把“Villasenor 的第一性对象是 crossing-driven segment/face flux，而不是整轨迹 old/new shape-difference”进一步改写得更像 paper-backed 主文，而不只像源码摘要。

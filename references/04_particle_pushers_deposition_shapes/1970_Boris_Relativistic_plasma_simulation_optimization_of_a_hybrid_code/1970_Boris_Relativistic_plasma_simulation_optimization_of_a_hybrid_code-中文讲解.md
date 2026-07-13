# Boris 1970 论文边界中文说明

> 当前状态：本文件不是对 Boris 1970 会议论文的逐段精读。DTIC 原始 PDF 在 2026-07-13 的请求被限流，项目只固定了书目身份、获取边界和后续可用的替代证据。

## 书目与历史位置

J. P. Boris 的 *Relativistic plasma simulation--optimization of a hybrid code* 出版于 1970 年第四届 Numerical Simulation of Plasmas 会议，页码 3--67，DTIC 编号为 `ADA023511`。它是本书追踪 Boris relativistic particle mover 历史源头时应使用的原始书目记录。

## 当前可用的三层证据

第一层是 DTIC 书目记录：它固定论文题名、作者、会议、页码和获取入口，但不提供本地可逐式核对的正文。

第二层是 Birdsall and Langdon 1985 的全文讨论。项目已经将该书拆卷并完成 MinerU；其中 `4-3` 到 `4-5` 解释了 electric half-acceleration、magnetic rotation、

$$
t=\tan(\theta/2),\qquad s=\frac{2t}{1+t^2},\qquad c=\frac{1-t^2}{1+t^2},
$$

以及向量形式的 Boris 更新。这一层可以支撑算法教学，但应标为 Birdsall 的二手讲解，而不是 Boris 原始论文的逐页引文。

第三层是现代 WarpX 源码：`../warpx/Source/Particles/Pusher/UpdateMomentumBoris.H` 将 half-acceleration、磁旋转和第二次 electric half-acceleration 落成可执行 kernel。该层说明当前实现如何工作，不自动证明它与 1970 会议稿的排版、符号或所有实现细节逐项相同。

## 对第 4 章的使用边界

第 4 章可以写成：Boris 的历史身份由 DTIC 书目记录固定，核心旋转推导由 Birdsall 1985 的 full-text 讨论支撑，当前 WarpX 行为由源码和 runtime contract 支撑。第 4 章不能写成“已完成 Boris 1970 原文精读”，也不能用当前 `particle_pusher` regression 代替原始论文的历史证据。

# Reading Log

## 2026-05-18

- 从 `/Users/yuxiangzhang/Documents/Zoteropaper/plasma_book/` 发现本地现成 PDF。
- 已复制到项目内书籍专属目录：
  - `references/02_books_lecture_notes/1985_BirdsallLangdon_Plasma_physics_via_computer_simulation/`
- 原书共 `469` 页，首次直接提交 MinerU 失败，报错：
  - `number of pages exceeds limit (200 pages), please split the file and try again`
- 随后新增 `scripts/split_pdf_pypdf.py`，用 bundled Python 的 `pypdf` 将原书拆成三段：
  - `p0001-0200`
  - `p0201-0400`
  - `p0401-0469`
- 三段当前均已完成 MinerU 转 Markdown，并各自生成 `images/`。
- 当前目录已具备：
  - 原 PDF
  - `split_parts/*.pdf`
  - 三段 Markdown
  - 三段 `images/`
  - 中文讲解笔记骨架

## 2026-05-18 第二次更新

- 已开始第一段正式精读，当前已写入中文讲解笔记的范围：
  - `Foreword`
  - `Preface`
  - Part One 入口
  - Chapter 1
  - Chapter 2 的 `2-1` 到 `2-4`
- 当前已经明确写清：
  - 作者如何论证 PIC 在物理上是“受控失真但仍抓住本质”的方法
  - Debye 长度、`N_D`、`KE >> PE`、`\nu << \omega_p` 在这一论证里的角色
  - 为什么必须引入空间网格，以及粒子-网格-场-粒子循环的最小骨架
  - leapfrog mover 在全书中的教学地位
- 下一步：
  - 继续读 `2-5` 到 `2-6`
  - 再进入 `3A ES1` 和 `4-6` 到 `4-10`
  - 开始把这些读书结论更明确地回链到第 3A / 5 / 6 章

## 2026-05-18 第三次更新

- 已继续推进第一分卷精读，当前新写入中文讲解笔记的范围：
  - Chapter 2 的 `2-5`
  - Chapter 2 的 `2-6`
  - Chapter 3A 的 `3-1` 到 `3-6`
- 当前已经明确写清：
  - `2-5` 中从沉积后的 `rho` 到 `phi/E` 的最小静电场求解链，以及 `ES1` 为何选 `FFT` 路线
  - 离散算子 `kappa`、`K^2` 与连续 `k`、`k^2` 的差别，及其与后续频谱控制/数值色散讨论的关系
  - `2-6` 中 NGP 与 CIC 的等效粒子形状、charge assignment / force interpolation 一致性、以及避免自力污染的基本条件
  - `3A ES1` 开头的程序骨架：`INIT -> SETRHO -> FIELDS -> SETV -> ACCEL -> MOVE -> HISTRY`
  - `3-3` 到 `3-5` 的输入参数、归一化与程序内部工作变量之间的转换关系
  - `3-6 INIT` 如何把用户输入转成初始粒子和网格状态
- 下一步：
  - 继续读 `3-7 SETRHO`
  - 继续读 `3-8 FIELDS`
  - 再进 `3-10 SETV`、`3-11 ACCEL`、`3-12 MOVE`
  - 然后回到 `4-6` 到 `4-10`，把形函数、finite-size particles 与能量账本更明确回链到第 5 / 6 章

## 2026-05-18 第四次更新

- 已继续推进第一分卷精读，当前新写入中文讲解笔记的范围：
  - Chapter 3 的 `3-7` 到 `3-12`
  - Chapter 4 的 `4-6` 到 `4-10`
- 当前已经明确写清：
  - `SETRHO` 是 `t=0` 的第一次真实 charge deposition，不是预先存在的 `rho`
  - `FIELDS` 是 `rho -> FFT -> phi -> E -> field energy` 的完整离散合同
  - `SETV` 如何把用户给的 `v(0)` 转成 leapfrog 真正需要的 `v(-\Delta t/2)`
  - `ACCEL` 如何把 weighting、velocity push、动量和 kinetic energy 记账放进同一子程序
  - `MOVE` 如何把位置推进与下一步所需 `rho` 沉积绑定在同一粒子循环里
  - `4-6` 到 `4-8` 中 `S(x)` / `S(k)`、finite-size particles、grid force 与 aliasing 的理论边界
  - `4-9` 到 `4-10` 中 Poisson 系统误差与 `rho_k phi_k^*` 场能量账本的优先地位
- 已把这轮结论最小回填到书稿：
  - 第 5 章：shape factor / finite-size / grid force 的理论边界
  - 第 6 章：Poisson 系统误差与 `rho phi` 场能量记账
- 下一步：
  - 继续沿 Chapter 4 往下读 mover / field accuracy 相关小节
  - 然后进入更系统的 finite-grid / aliasing / numerical heating 讨论
  - 再把 Birdsall 这几轮精读结果更系统回填到第 3A / 4 / 5 / 6 章

## 2026-05-18 第五次更新

- 已继续推进第一分卷精读，当前新写入中文讲解笔记的范围：
  - Chapter 4 的 `4-3` 到 `4-5`
- 当前已经明确写清：
  - `4-3` 中 electric impulse 与 magnetic rotation 的几何分裂
  - Boris 结构并非经验技巧，而是围绕 `E` 的半步冲量与 `v×B` 的旋转构造
  - `tan(theta/2)`、`t/s/c` 半角变量如何把旋转实现成不依赖每步超越函数的更新
  - 向量 Boris 形式如何成为现代 `UpdateMomentumBoris` 这类 kernel 的直接祖先
  - `1d2v/1d3v` 的建模边界：一维空间依赖不等于一维速度空间
  - guiding-center 常数为何是离散 mover 结构保持能力的代表性检验
- 已把这轮结论最小回填到书稿：
  - 第 4 章：Boris pusher 结构来源与 1d2v/1d3v 建模边界
- 下一步：
  - 进入 Chapter 8 的 `8-1` 到 `8-7`
  - 然后继续 `8-10` 到 `8-13`
  - 把 finite-grid / aliasing / numerical heating 主线接回第 5 / 6 章

## 2026-05-18 第六次更新

- 已继续推进第一分卷精读，当前新写入中文讲解笔记的范围：
  - Chapter 8 的 `8-1` 到 `8-7`
  - Chapter 8 的 `8-10` 到 `8-13`
- 当前已经明确写清：
  - spatial grid 与 finite-difference sampling 不是单纯噪声源，而会与 plasma collective modes 做 coherent interaction
  - aliasing 的一般来源：粒子 continuum 信息被压到 sampled grid density 时，不同 `k_p = k - p k_g` 被耦合进同一个 `rho(k)`
  - charge weighting 与 force weighting 共用同一个 `S`，其必要性不只是消 self-force，还包括整体 momentum conservation 和避免 gravitation-like instability
  - `dP/dt = \Delta x \sum_j \rho_j E_j` 把系统总动量守恒问题降到了 grid 上 `rho/E` 合同
  - `K(k)`、`kappa(k)`、`S(k)` 与 alias sum 如何一起进入 grid-modified dielectric function 和 dispersion relation
  - cold beam / warm Maxwellian plasma 都可能因为 grid aliases 产生非物理 instability，`lambda_D / Delta x` 是明确的数值物理边界
- 下一步：
  - 把这轮 Chapter 8 结论最小回填到第 5 / 6 章
  - 再评估是否继续精读与 energy-conserving、numerical heating 最直接相关的后续段落
  - 并把 Birdsall 的 finite-grid 理论与 WarpX 现有 validation 更明确配对

## 2026-05-18 第七次更新

- 已继续推进第一分卷精读，当前新写入中文讲解笔记的范围：
  - Chapter 9 的 `9-4`
  - Chapter 9 的 `9-7`
  - Chapter 10 的 `10-2` 到 `10-4`
  - Chapter 10 的 `10-9` 到 `10-10`
- 当前已经明确写清：
  - finite `\Delta t` 不只带来 phase error，还会引入 time alias branches 和新的 branch-coupling resonance
  - warm Maxwellian plasma 下，numerical instability 的危险阈值会早于冷等离子体的 `\omega_p \Delta t > 2` 直觉
  - 大的 `\omega_p \Delta t` 与 `v_t \Delta t/\Delta x` 会对应高噪声和快速 nonphysical heating
  - `subcycling / orbit-averaging / implicit methods` 的共同目标，是抑制快时间尺度 alias 对慢物理的污染
  - momentum-conserving 路线一般不存在严格守恒的总能量
  - energy-conserving 路线的关键不是“更准的 `E`”，而是把粒子受力改写成离散场能量 `W_E = (V_c/2)\sum \rho_j\phi_j` 对粒子位置的负梯度
  - reciprocity / Green's reciprocation theorem 是 exact energy conservation 的真正条件
  - 这条路线的代价是 momentum conservation、自力、宏观场精度和 aliasing 表现必须逐项重新审查
- 下一步：
  - 把这轮 Chapter 9/10 结论最小回填到第 5 / 6 章，并补到第 4 章关于 gather-family 差别的理论边界
  - 然后继续评估是否需要读 `12-3` 到 `12-7`，把 fluctuation / collision / numerical heating 的 kinetic 解释也接进来
  - 再把 Birdsall 这几轮文献结论和 WarpX 现有 validation 更明确配对

## 2026-05-18 第八次更新

- 已继续推进第一分卷精读，当前新写入中文讲解笔记的范围：
  - Chapter 12 的 `12-3` 到 `12-7`
- 当前已经明确写清：
  - `(\rho^2)_{k,\omega}` 的 fluctuation spectrum 如何同时包含 `S(k_p)`、`\epsilon(k,\omega)` 和时间采样 comb `\omega_g`
  - `1/2\,\rho\phi` 在 fluctuation theory 里同样是自然的场能量变量，而不只是 Chapter 10 的 energy-accounting 工具
  - 当 `\lambda_D \lesssim \Delta x` 时，Debye potential 与 spatial spectrum 不再简单同义
  - `12-5/12-6` 把 grid-induced effective collisions 写成 kinetic equation，而不是停留在经验现象
  - `H`-theorem 直接说明 space-time grid 会制造 entropy；对 Maxwellian 情形，这和 nonphysical heating 是同一件事
  - 对 drifting plasma，grid effects 更准确的图像是 drag + diffusion + entropy production，而不只是“总能量变大”
  - `12-7` 的关键总结是：缺陷不在 kinetic theory，而在模型本身；这些 microscopic errors 不会靠 ensemble average 自动抵消
- 下一步：
  - 把这轮 `12-3` 到 `12-7` 的结论最小回填到第 6 章，并把它和 `energy_conserving_thermal_plasma`、Langmuir、uniform plasma、NCI/stability 这类 validation 的检查量更明确配对
  - 然后再决定是继续读 Chapter 13 的 heuristic estimates，还是转回文献缺口 `Hockney-Eastwood` / `TajimaDawson1982`

## 2026-05-18 第九次更新

- 已继续推进第一分卷精读，当前新写入中文讲解笔记的范围：
  - Chapter 13 的 `13-2`
  - Chapter 13 的 `13-3` 已核实部分
- 当前已经明确写清：
  - 一维 sheet model 已经足以展示 Maxwellian、Debye shielding、wake、drag、diffusion 和 relaxation time，不是只能做课堂演示的 toy model
  - `13-2` 给出的 `\tau = 2N_D/\omega_p` 更适合解释 fast randomization time / correlation time / 独立采样间隔
  - `13-3` 则进一步把 selected-group randomization 和 whole-distribution thermalization 拆开；前者是 `N_D` 级，后者实验上接近 `N_D^2` 级
  - 对单 species 一维情形，弱相互作用 kinetic equation 并不会自动把分布推进到完整 Maxwellian，这解释了为什么真正热化远慢于 test-particle slowing-down time
- 已做的最小正文回填：
  - 已把这轮关于 `N_D`、correlation time、有限粒子数下 Maxwellian / Debye shielding 可测性的结论补进第 1 章
- 下一步：
  - 继续读 Chapter 13 的 `13-4` / `13-5`，把 heuristic estimates、自热时间和 weighting order 的关系压实
  - 然后再决定是否回到缺口文献 `Hockney-Eastwood` / `TajimaDawson1982`

## 2026-05-18 第十次更新

- 已继续推进第一分卷精读，当前新写入中文讲解笔记的范围：
  - Chapter 13 的 `13-4`
  - Chapter 13 的 `13-5` 已核实部分
- 当前已经明确写清：
  - thermal plasma 的 self-heating time `tau_H` 不是只由 `N_D` 控制，还显式依赖 `lambda_D/Delta x`、shape order 和 `v_t Delta t / Delta x`
  - 更高阶 weighting 与更强 short-wavelength smoothing 会显著延长 `tau_H`
  - damped equations of motion 的 phase error 也可能制造 nonphysical cooling，不能把“总能量下降”误判成单纯更稳定
  - 仅靠 `delta F` 的 heuristic estimate 不足以可靠预测 heating/cooling，因为净效应来自 drag 与 diffusion 的细微失衡
  - Hockney 2d2v 结果给出了 `tau_s`、`tau_H`、`N_C` 和 optimum path 这组 thermal-plasma 设计量，其中 `tau_H/tau_s` 是判断长期数值健康度的更实用指标
- 已做的最小正文回填：
  - 已把 shape order / smoothing 与 `tau_H` 的关系补进第 5 章
  - 已把 damped mover phase error 与 nonphysical cooling / heating time 的关系补进第 6 章
- 下一步：
  - 继续核实 `13-5` 后半段剩余经验缩放，尤其是 `tau_H/tau_s`、field fluctuation 与 optimum path 的更细边界
  - 然后再决定是否回到缺口文献 `Hockney-Eastwood` / `TajimaDawson1982`

- 补充：本轮后续又把 `13-5` 的量化结论再压实了一层：
  - `K_4` 把 optimum-path 上的 `tau_H/tau_s` 压成了可比较的 figure of merit
  - `QPM` 说明 particle shape、Poisson operator 与 potential correction 的组合可以带来数量级更好的长期数值健康度
  - field fluctuation level 也被组织成 `1/N_C` 缩放
  - Hockney 观测到的 heating 近线性随时间增长，应理解为 stochastic heating 的强信号

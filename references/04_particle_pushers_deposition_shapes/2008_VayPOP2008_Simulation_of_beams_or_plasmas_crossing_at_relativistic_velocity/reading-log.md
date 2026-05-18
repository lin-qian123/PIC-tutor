# Reading Log

## 2026-05-18

- 从本机现成文献资产中发现：
  - 原 PDF：`/Users/yuxiangzhang/Documents/Zoteropaper/calculation/pusher/Vay et al. - 2008 - Simulation of beams or plasmas crossing at relativistic velocity.pdf`
  - 现成 MinerU Markdown 与 `images/`：`/Users/yuxiangzhang/Documents/program/minerU/md_output/calculation/pusher/Vay et al. - 2008 - Simulation of beams or plasmas crossing at relativistic velocity/`
- 已复制并 materialize 到：
  - `references/04_particle_pushers_deposition_shapes/2008_VayPOP2008_Simulation_of_beams_or_plasmas_crossing_at_relativistic_velocity/`
- 当前目录已具备：
  - 原 PDF
  - MinerU Markdown
  - `images/`
  - 中文讲解笔记骨架
- 下一步：
  - 开始逐段中文精读，并回填到第 4 章 Boris/Vay/Higuera-Cary 相关正文。

### 第二次更新

- 已开始第一轮正式精读，当前已覆盖：
  - 摘要
  - 引言
  - `II.A Cancellation of electric and magnetic fields contributions in the Lorentz force`
  - `II.B A new leapfrog pusher` 的最小逻辑
- 当前已明确写清：
  - 这篇文章的核心问题不是泛泛“改进 relativistic mover”，而是 boosted-frame / relativistic-crossing 场景下 electric/magnetic cancellation 的离散一致性
  - 文中的第一性试金石是 `\mathbf E + \mathbf v \times \mathbf B = 0` 下应无净力
  - 对作者而言，Boris 的问题被严格限定在这条 cancellation property 上，而不是否定 Boris 的一般用途
  - Vay 的新 leapfrog 结构首先是对速度平均的替换，从而去掉这条试金石上的 spurious force
- 已最小回填到：
  - `manuscript/chapters/04-particle-pushers.md`
- 下一步：
  - 继续补单粒子测试
  - 补 field solver 边界
  - 再看超相对论束流与电子背景的应用例子

### 第三次更新

- 已继续完成 `II.C`、`III`、`IV`、`V` 的第一轮主文精读。
- 当前已明确写清：
  - 单粒子测试真正验证的是同一物理系统在 laboratory frame 与 moving frame 下是否都能保持解析一致；
  - 常量 `B_z` 测试中，新 pusher 在 `\gamma_f=2` 的 moving frame 仍跟住解析解，而 Boris 及其 `\tan(\omega_c\Delta t)/(\omega_c\Delta t)` 修正会明显偏离，且误差随 `\gamma_f` 快速放大；
  - 常量 `E_x` 测试中，三种 mover 在实验室系都准确，但只有新 pusher 在 `\gamma_f=100` 的 moving frame 里仍对；
  - 文中的 field solver 不是通用 Maxwell solver，而是基于 `v_z \gg v_x,v_y` 和 `\partial_t \approx v_z \partial_z` 的 bounded Darwin-lite explicit approximation；
  - 对 `N` 个 species，field side 被压成 `N` 次带 `\gamma z` 拉伸的 Poisson solve；
  - LHC-like beam / electron-cloud 例子中，Boris 会导致 beam 和 electron 宏粒子非物理地快速丢失，而新 pusher 才能恢复预期的 hose-like instability；
  - moving-frame PIC 与 lab-frame quasistatic WARP calculation 对 vertical emittance growth 的增长率和饱和值给出一致预测。
- 已最小回填到：
  - `manuscript/chapters/04-particle-pushers.md`
- 下一步：
  - 若继续深挖 `Vay 2008`，优先处理 Appendix A/B 的解析解与 gyroradius 边界；
  - 否则转入 `Higuera 2017` 第一轮正式精读。

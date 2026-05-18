# Reading Log

## 2026-05-18

- 当前项目内已存在原 PDF：
  - `references/04_particle_pushers_deposition_shapes/2017_HigueraPOP2017_Structure-preserving_second-order_integration_of_relativistic_charged_particle_trajectories_in_electromagnetic_fields.pdf`
- 已按 `research-paper-explainer` / MinerU 工作流，用项目内 `scripts/mineru_convert_stdlib.py` 完成转换。
- 当前目录已具备：
  - 原 PDF
  - MinerU Markdown
  - `images/`
  - 中文讲解笔记骨架
- 下一步：
  - 开始逐段中文精读，并回填到第 4 章 Higuera-Cary pusher 相关正文。

### 第二次更新

- 已启动 `Higuera 2017` 第一轮正式精读，当前已覆盖：
  - 摘要
  - 引言
  - `II. Second-order charged particle integrators`
  - `III. Explicit evaluation`
  - `IV. Preservation of limiting solutions`
  - `V. Volume-preservation`
  - `VI. Numerical results`
  - `VII. Summary and future directions`
- 当前已明确写清：
  - 这篇文章的第一性问题不是 boosted-frame cancellation，而是三种二阶 relativistic integrator 在 energy / `E×B` drift / volume-preservation 三条性质上的并列比较；
  - Boris 保 volume、Vay 保 `E×B` drift，而 Higuera-Cary 的目标是同时保住这两条性质；
  - 新方法和 Boris 的实现差异主要不在 leapfrog 外壳，而在 `gamma` 的显式求法，这正对应 WarpX `UpdateMomentumHigueraCary.H` 的真实分叉点；
  - `E = 0` 时三者都守能量，因此这不是主要分叉判据；
  - practical timestep 下，Vay 会在测试问题里出现 resonance island 与轨道交叉，而 Boris 与 Higuera-Cary 维持正确的 phase-space topology；
  - 因而这篇文献对 WarpX 的真实支撑是 geometric / topological preservation，而不是 `Vay 2008` 那类 frame-change consistency。
- 已最小回填到：
  - `manuscript/chapters/04-particle-pushers.md`
- 下一步：
  - 若继续深挖 `Higuera 2017`，优先补第 4/5 节里的 Jacobian 细推导与和 WarpX kernel 的逐式对位；
  - 否则转回 `Yee 1966` acquisition 或下一组基础文献。

### 第三次更新

- 已继续把 `Higuera 2017` 从主文概述推进到关键公式与 WarpX kernel 的逐式对位。
- 当前已明确写清：
  - 论文的 `\vec\epsilon`、`\vec\beta`、`\vec u_-`、`\gamma_-^2`、`\gamma_{new}`、Boris-like rotation equation，可以直接映到 WarpX 的 `qmt`、`beta*`、`um*`、`gamma`、`sigma`、`ust`、`tx/ty/tz`、`s`、`up*` 变量链；
  - WarpX 代码里变量名 `gamma` 在中段被重载为 `\gamma_{new}^{-1}`，这一步如果不说明，很容易误读源码；
  - 新 integrator 的 volume-preserving 不是抽象标签，而是来自前后半步 Jacobian determinant 互为倒数；
  - Vay 的 Jacobian 写成 `J(x_i,u_i)/J(x_i,u_f)` 这类比值后，一般不会化成 `1`，这正是后面 topology failure 的机制线索。
- 已继续回填到：
  - `notes/code-reading/particles/03-vay-higuera-cary-pushers.md`
  - `manuscript/chapters/04-particle-pushers.md`
- 下一步：
  - 若继续深挖 `Higuera 2017`，可再把 Jacobian 证明压成更完整的符号推导；
  - 否则切回下一条未完成文献主线。

### 第四次更新

- 已继续把 `Higuera 2017` 和 WarpX 现有 validation 更明确配对。
- 当前已明确写清：
  - 本地最直接能接论文主线的是 `particle_pusher`：
    - `algo.particle_pusher = "higuera"`
    - force-free 常量外部 `E/B`
    - analysis 检查长时间推进后 `x \approx 0`
  - 这条 regression 能支撑 Higuera-Cary 在 relativistic force-free / drift-preservation 构型下的本地强断言；
  - `larmor` 当前仍只有 checksum baseline，不能冒充论文第 VI 节里 Poincare topology / resonance-island 结论的本地复现；
  - 因而当前最准确的项目内边界是：
    - 论文 topology 结论：文献级最强
    - `particle_pusher`：本地 strongest direct evidence
    - `larmor`：应用级稳定性基线
- 已继续回填到：
  - `notes/code-reading/particles/26-pusher-single-particle-and-photon-validation-map.md`
  - `manuscript/chapters/04-particle-pushers.md`
- 下一步：
  - 若继续沿 Higuera-Cary 线推进，就该转向“论文结论和本地 regression 覆盖缺口”的明示整理；
  - 否则切回下一条未完成文献/源码主线。

### 第五次更新

- 已继续把 `Higuera 2017` 的 Jacobian / volume-preservation 从结果描述推进到更完整的符号链。
- 当前已明确写清：
  - 证明的主干对象是 `I-\Omega` 加一个 rank-one correction；
  - determinant lemma 在这里的作用，是把 Boris-like rotation skeleton 和 relativistic correction 的体积贡献拆开；
  - `\det(I-\Omega)`、`\vec Y=(I+\Omega)^{-1}\bar u_{new}`、以及最终 `J_{f,new}` 的显式标量式，构成了后半步 Jacobian 的最关键中间链；
  - “volume-preserving” 的真正数学内容不是每半步各自等于 1，而是前后半步的 Jacobian determinant 互为逆，因此一步更新的总体 Jacobian 为 1。
- 已继续回填到：
  - `notes/code-reading/particles/03-vay-higuera-cary-pushers.md`
  - `manuscript/chapters/04-particle-pushers.md`
- 下一步：
  - 若继续沿这条线深挖，可把 `J_i` / `J_f` reciprocal relation 再压成更紧的逐行推导；
  - 否则切回下一未完成主线。

### 第六次更新

- 已继续把 `J_i / J_f` reciprocal relation 的记号边界写清。
- 当前已明确补出：
  - `J_{f,new}` 与 `J_{i,new}` 虽然写成同形标量式，但它们对应的是前/后半步不同方向映射上的 determinant，因此在整步组合里扮演互逆角色；
  - Vay 的 Jacobian 不是“任何情况下都会坏”，论文还保留了一个例外边界：
    - 对时空常量磁场，逐步比值会 telescoping；
    - 再结合 `J(x,u)` 的有界性，不能直接推出 attractor/repeller。
- 这轮之后，`Higuera 2017` 的 Jacobian 线已经从：
  - 结构保持结论
  - 论文公式
  - WarpX kernel 变量链
  - 本地 validation 覆盖边界
  四层基本接齐。

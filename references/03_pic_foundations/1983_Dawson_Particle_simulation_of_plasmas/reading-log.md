# Reading Log

## 2026-05-18

- 从 `/Users/yuxiangzhang/Documents/Zoteropaper/calculation/pic_model/` 发现本地现成 PDF。
- 已复制到项目内论文专属目录：
  - `references/03_pic_foundations/1983_Dawson_Particle_simulation_of_plasmas/`
- 已按 `research-paper-explainer` 的 MinerU 流程完成 Markdown 转换。
- 当前目录已具备：
  - 原 PDF
  - MinerU Markdown
  - `images/`
  - 中文讲解笔记骨架
- 下一步：
  - 开始逐段中文精读，并回填到 PIC foundations 相关章节。

### 第二次更新

- 已开始第一轮正式精读，当前已覆盖：
  - 引言对 computer simulation 作为 experiment / analytic theory 之外“第三种研究手段”的定位
  - plasma particle models 总述
  - electrostatic particle models 与 finite-size particles / grid / FFT-Poisson 主链
- 当前已明确写清：
  - PIC 的最小定义是“跟踪大量带电粒子在自洽电磁场中的运动”
  - `superparticle` 是 practical necessity，而不是附属术语
  - electrostatic model 在综述中的角色是先展示基本问题与基本技巧
  - finite-size particles 的第一性动机是抑制非物理短程碰撞，同时保留长程 collective behavior
  - grid 是 finite-size coarse graining 的自然数值实现，不是先验物理结构
  - `shape factor -> charge sharing -> FFT Poisson -> gather back to particle` 已在 1983 综述里写成标准合同
- 已最小回填到：
  - `manuscript/chapters/01-kinetic-models.md`
  - `manuscript/chapters/05-deposition-shapes.md`
  - `manuscript/chapters/06-field-solvers.md`
- 下一步：
  - 继续按原文顺序补 `electromagnetic particle models`
  - `fractional dimensional models`
  - diagnostics / visualization 总述

### 第三次更新

- 已继续完成第一轮精读，当前新增覆盖：
  - `electromagnetic particle models`
  - `fractional dimensional models`
  - `magnetostatic (Darwin) models`
  - 文末 diagnostics / visualization 哲学
- 当前已明确写清：
  - full EM 模型必须回到完整 Maxwell equations
  - reduced-dimension EM PIC 的真实结构是 `1 1/2-D`、`1 2/2-D`、`2 1/2-D`
  - full EM 时间步首先受最高频 light mode 与 CFL 限制
  - relativistic push 里 `P`、`\gamma`、Lorentz contraction 与 space/time filtering 不对称都是模型边界
  - Darwin model 的作用是去掉 radiation branch，换取低频磁化问题的较长时间步
  - diagnostics 的目标是提炼 physics essence，而不是保留全部 detail
- 已最小回填到：
  - `manuscript/chapters/04-particle-pushers.md`
  - `manuscript/chapters/06-field-solvers.md`
  - `manuscript/chapters/08-diagnostics-cases.md`
- 下一步：
  - 继续补 `numerical stability`
  - quiet starts
  - diagnostics 细分量：distribution function、drag、diffusion、field fluctuations、normal modes

### 第四次更新

- 已继续完成第一轮精读，当前新增覆盖：
  - `numerical stability`
  - diagnostics 细分量：
    - distribution function
    - drag
    - diffusion
    - field fluctuations
    - time correlations
    - normal modes of a nonuniform plasma
  - `quiet starts` 的第一轮边界
- 当前已明确写清：
  - Dawson 把数值不稳定归结成 spatial aliasing 与 time aliasing 两类 stroboscopic errors
  - diagnostics 的第一性分类是 particle-motion measurements 与 wave measurements，而不是 writer family
  - drag / diffusion / correlation / fluctuation level 是可以直接测 kinetic coefficients 与 wave statistics 的合同
  - quiet start 通过降低初始熵噪声提升弱效应可观测性，但会随时间退化
  - random start 会过激发 small-`k` long-wavelength modes，而 quiet start 又会引入自己的 beam-ordering instabilities
- 已最小回填到：
  - `manuscript/chapters/06-field-solvers.md`
  - `manuscript/chapters/08-diagnostics-cases.md`
  - `notes/code-reading/applications/01-uniform-plasma.md`
- 下一步：
  - 继续补 weighted particles / many-size electrons
  - 继续补 quiet-start instabilities 的后续工程边界
  - 再决定是否进入统计理论 examples 或 free-electron-laser 段落

### 第五次更新

- 已继续完成第一轮精读，当前新增覆盖：
  - `electrons of many sizes, charges, and masses`
  - `instabilities in quiet starts` 的后续工程边界
  - `free-electron laser` 的历史 relativistic-EM 例子
- 当前已明确写清：
  - 不同权重宏粒子可通过保持相同 `q/m` 构成仍满足通常 Vlasov 方程的 composite distribution
  - 这条 weighted-particle 路线的主要代价是 light-on-heavy scattering 与额外 collisional side effect
  - quiet order 失稳来自离散 beam model 的正常模谱，而不是偶发实现缺陷
  - quiet start 最多只能维持有限个 growth times；可通过打破规则 velocity spacing、cell 间错开 velocity points 或周期性 damping 细尺度 beam instabilities 来缓解，但对非均匀系统没有通用 prescription
  - Dawson 把 FEL 明确当成 relativistic electromagnetic particle model 的代表例子，并把它解释成 relativistic beam + helical ripple field + Raman-like parametric coupling
  - 当前历史例子的硬结果包括：matching-condition 谱证据、饱和时 `36%` 的 longitudinal current 降低、约 `30%` 的束流能量转成辐射、约 `2\\lambda_0` 的危险 backward mode，以及 saturation 由 electrostatic-wave trapping 主导
- 已最小回填到：
  - `manuscript/chapters/01-kinetic-models.md`
  - `notes/code-reading/applications/06-beam-collider-fel-extraction.md`
  - `manuscript/chapters/08-diagnostics-cases.md`
- 下一步：
  - 继续补 `free-electron laser` 图 54-57 与效率估计的图文对应
  - 或转入前面统计理论 examples 的继续精读

### 第六次更新

- 已继续完成 `free-electron laser` 剩余子段整理，当前新增覆盖：
  - `Fig.54`
  - `Fig.55`
  - `Fig.56`
  - `Fig.57`
  - trapping-based efficiency estimate
- 当前已明确写清：
  - `Fig.54` 同时承担 lab-frame kinematics 与 beam-frame parametric-instability 两种解释框架
  - `Fig.55` 的重点是 electromagnetic / electrostatic 不稳定模满足 matching condition
  - `Fig.56` 把 EM energy、electrostatic energy 与 longitudinal current 绑成最小 beam-quality bookkeeping
  - `Fig.57` 则把
    - `\eta = (\gamma_0-\gamma_{\mathrm{ph}})/(\gamma_0-1)`
    - `\eta \simeq \omega_{po}(2k_0 c \gamma^{3/2})^{-1}`
    的粗略理论
    和 simulation 做并排比较
  - 整组图像共同完成了 mechanism verification -> nonlinear saturation -> rough efficiency scaling 的最小论证链
- 已最小回填到：
  - `notes/code-reading/applications/06-beam-collider-fel-extraction.md`
  - `manuscript/chapters/08-diagnostics-cases.md`
- 下一步：
  - 转入前面统计理论 examples 的继续精读

### 第七次更新

- 已开始进入 `Tests of the statistical theory of plasmas`，当前新增覆盖：
  - 统计理论 examples 的总入口
  - one-dimensional electrostatic sheet-model benchmark 的定位
  - `Kinetics of a one-dimensional plasma` 的开场边界
- 当前已明确写清：
  - Dawson 把 drag、diffusion、field fluctuations、correlation functions 和 normal-mode measurements 放回“检验 subtle plasma statistics”的语境里，而不是附属可视化
  - 一维 electrostatic sheet model 在这里承担的是无 grid、可逼近 exact dynamics 的 benchmark role
  - 作者明确把这类模型当成校验更一般 gridded particle models 的高精度参照，而不是主要工作horse
  - `Kinetics of a one-dimensional plasma` 的真正入口是 collisional phenomena、transport 和 fluctuation measurements，而不是普通波形展示
- 已最小回填到：
  - `manuscript/chapters/06-field-solvers.md`
  - `manuscript/chapters/08-diagnostics-cases.md`
- 下一步：
  - 继续补这一节里的 drag / diffusion / fluctuation measurements 与一维统计输运细节

### 第八次更新

- 已继续推进 `Kinetics of a one-dimensional plasma` 与 wave-side measurements，当前新增覆盖：
  - drag 的 velocity-shell ensemble 测量合同
  - velocity diffusion 的 `\tau^2 -> \tau` 双阶段演化
  - decorrelation time 的统计/物理双重角色
  - field fluctuation 的 thermal modal-energy 合同与 finite-size 修正
- 当前已明确写清：
  - drag 不是单粒子减速，而是窄速度窗口 test-particle 群体平均速度的衰减率
  - thermal/steady systems 可通过多个 `t_0` 上重复取样同一速度壳来提高统计精度
  - velocity diffusion 需要区分 short-time ballistic-like regime 与 long-time random-impulse regime
  - decorrelation time 同时控制统计独立采样和 kinetic interpretation
  - thermal field fluctuation 的 point-particle modal energy 服从 `KT/2` 型 equipartition，而 finite-size particle shape 会系统改写该 fluctuation level
- 已最小回填到：
  - `manuscript/chapters/06-field-solvers.md`
  - `manuscript/chapters/08-diagnostics-cases.md`
- 下一步：
  - 继续补 power spectrum / time correlations / magnetized fluctuation peaks

### 第九次更新

- 已继续推进 wave-side measurements，当前新增覆盖：
  - power spectrum 的连续谱 / plasma spike 分层
  - run length `T` 对频谱可解释性的硬约束
  - magnetized fluctuation spectrum 的 Bernstein / upper-hybrid / zero-frequency peak 结构
  - `C(k,\tau)` 与 `G(k,\omega)` 的 Wiener-Khintchine 关系
- 当前已明确写清：
  - power spectrum 的价值是把 Debye-cloud random continuum 与 collective plasma spike 分离
  - `\Delta\omega \simeq 1/T` 说明有限 run length 会直接限制谱特征解析度
  - magnetized fluctuation spectrum 不只是“多几个峰”，而是把 Bernstein、upper-hybrid、ion-cyclotron、lower-hybrid 和 convective-cell / charged-flux-tube 结构直接编码进诊断图
  - time correlation 直接暴露 wave memory / decorrelation，而非频谱的附属定义
  - `C(k,\tau)` 与 `G(k,\omega)` 是同一物理信息的时域/频域表示
- 已最小回填到：
  - `manuscript/chapters/06-field-solvers.md`
  - `manuscript/chapters/08-diagnostics-cases.md`
- 下一步：
  - 继续补 nonuniform-plasma normal-mode reconstruction

### 第十次更新

- 已继续推进 wave-side measurements，当前新增覆盖：
  - nonuniform-plasma normal-mode reconstruction
  - discrete line 与 continuous spectrum 的 diagnostics 分层
  - damping-time 约束下的 correlation-window 设计
- 当前已明确写清：
  - nonuniform plasma 的 normal modes 不再是简单正弦波，simulation 的价值在于重建空间波函数而不只是做谱图
  - 对离散谱线，可通过与 `\sin\omega_1 t`、`\cos\omega_1 t` 的相关积分重建 mode amplitude `\phi_1(\mathbf r)` 与相位 `\theta_1(\mathbf r)`
  - integration time `T` 必须短于该 mode 的 damping time；长运行应拆成多个短窗口再平均，而不是单次无限拉长 `T`
  - continuous spectrum 里既可能有 localized modes，也可能只是 random particle motion；后者需要继续测 `\delta v(\mathbf v,x,\omega)` 这类 kinetic quantity
- 已最小回填到：
  - `manuscript/chapters/08-diagnostics-cases.md`
- 下一步：
  - 继续补 random-start 对 weak instability growth-rate measurement 的限制

### 第十一次更新

- 已继续推进 `Tests of the statistical theory of plasmas` 与 quiet-start 边界，当前新增覆盖：
  - `\delta v(\mathbf v,x,\omega)` 的 kinetic diagnostics 边界
  - random-start 对 weak-instability growth-rate measurement 的限制
  - random spatial loading 对 small-`k` long-wavelength modes 的过激发
- 当前已明确写清：
  - continuous spectrum 若主要来自 random particle motion，就不能只停在 `\phi(x,\omega)`，而应继续下钻到 `\delta v(\mathbf v,x,\omega)` 这类 kinetic quantity
  - weak instability 的可测动态范围受初始 `N^{-1/2}` 噪声与最终可容许 mode amplitude 共同限制，可用增长窗口约为 `\gamma t \sim \frac{1}{2}\ln N`
  - 即使 `N=10^5`，典型也只有约 `5` 个 e-foldings，因此 growth-rate 精度通常只能到二十个百分点量级，弱模式甚至可能直接被 natural noise 淹没
  - purely random spatial loading 还会强烈过激发 small-`k` long-wavelength electrostatic modes，因为它不包含 Debye shielding 与局域 charge neutrality
- 已最小回填到：
  - `manuscript/chapters/08-diagnostics-cases.md`
- 下一步：
  - 继续补 quiet-start phase-space cell construction 的更细实现边界
  - 再决定是否切到下一组基础文献

### 第十二次更新

- 已继续推进 quiet-start 主线，当前新增覆盖：
  - phase-space cell construction 的具体做法
  - arbitrary distribution 的 cumulative-map 构造
  - thermal/noisy starts 与 quiet starts 的工程取舍总结
- 当前已明确写清：
  - quiet start 的核心不是“少用随机数”，而是按目标分布函数对 phase space 做确定性 covering
  - Maxwellian quiet start 可通过 equal-area velocity bins 在每个空间 cell 中逐个放置代表速度点
  - 对一般分布，需要先构造 `y(v)=\int_{-\infty}^{v}P(v')\,dv'` 再做反函数映射
  - quiet start 提供更大的 weak-effect dynamic range，但简单 equal-area placement 对 tail / low-density critical region 的表示能力有限，因此需要 weighted particles 继续补位
- 已最小回填到：
  - `manuscript/chapters/08-diagnostics-cases.md`
- 下一步：
  - 评估 `Dawson 1983` 这条 quiet-start / statistical-theory 主线是否已到自然收口点
  - 再决定切入下一组基础文献

### 第十三次更新

- 已基于当前中文讲解、reading-log、正文回填和 TODO 状态做一次收口评估。
- 当前判断：
  - `Dawson 1983` 的 statistical-theory / quiet-start 主线已经到自然收口点。
  - 已覆盖：
    - drag / diffusion / decorrelation / field fluctuations
    - power spectrum / time correlations / magnetized peaks
    - nonuniform-plasma normal-mode reconstruction
    - continuous-spectrum 与 `\delta v(\mathbf v,x,\omega)` 的 kinetic diagnostics 分层
    - random/noisy starts、quiet starts、weighted particles 的 tradeoff
- 当前不再继续在本篇上扩新子线，下一步转入下一组基础文献。

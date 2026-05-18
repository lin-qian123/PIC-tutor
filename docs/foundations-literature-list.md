# 基础章节文献清单

这份清单只服务于基础章节，范围限定为：

- [01-kinetic-models.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/manuscript/chapters/01-kinetic-models.md)
- [02-pic-loop.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/manuscript/chapters/02-pic-loop.md)

它不试图替代整张 [literature-map.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/docs/literature-map.md)，而是把当前真正支撑基础理论入口的核心来源压成一张更窄、更可执行的表，并明确：

1. 哪些文献已经有本地 PDF / MinerU / 中文精读，可直接作为正文证据。
2. 哪些文献当前只有 metadata、摘要级信息或 acquisition 目标，不能在正文里冒充成已核实的一手来源。

## 使用规则

- `可直接作为正文证据`
  - 表示当前项目里已经有本地 PDF，且至少已有 MinerU Markdown 与中文精读笔记。
- `只可作边界/待补证据`
  - 表示 bibliographic identity 已清楚，但当前仍没有足够的一手正文资产，不能把它的细节写成已核实结论。

## 基础章节优先来源总表

| 来源 | 当前本地状态 | 主要服务章节 | 当前可直接支撑的边界 | 当前限制 |
|---|---|---|---|---|
| `Birdsall 1985` | 已 materialize；项目内已有 PDF、MinerU、`images/`、中文讲解和 `reading-log` | 第 1 章、第 2 章，以及第 4/5/6 章 | PIC 作为 collective model 的合法性、`N_D`、`\lambda_D`、`\\omega_p\\Delta t`、finite-grid/aliasing/heating、最小 leapfrog runtime contract、ES1 静电 loop | 原书过长，项目内实际阅读与引用当前主要来自已完成的分卷 MinerU 和中文精读，不是整本都已逐章收口 |
| `Dawson 1983` | 已 materialize；项目内已有 PDF、MinerU、`images/`、中文讲解和 `reading-log` | 第 1 章、第 2 章，以及第 4/6/8 章 | numerical experiment 视角、superparticle / weighted particles、finite-size particles、FFT-Poisson electrostatic contract、full EM / Darwin / diagnostics 哲学、quiet-start/statistical-theory 边界 | 已覆盖的重点足够支撑基础章节，但仍不是对全文所有例子的完全收口 |
| `Hockney-Eastwood` | 原书仍缺本地合法 PDF；无项目内 MinerU 产物 | 第 1 章、第 2 章，后续还会回到第 5/6 章 | 当前只能把它写成 particle-mesh foundations 的 acquisition target，以及对 heating / optimum-path / force-anisotropy 主线的来源指向 | 不能把原书正文细节当作已核实一手证据 |
| `Hockney 1971` fallback | 无本地 PDF；abstract-level 量化关系已确认 | 第 1 章优先，其次第 2/5/6 章 | `tau_coll / tau_pe = n(\\lambda_D^2+W^2)`、field fluctuation 缩放、optimum-path、`K_2` 分层 | 当前只有摘要级/landing-page 证据，不能替代原文逐段核实 |
| `Hockney et al. 1974` fallback | 无本地 PDF；正式题名/DOI 已确认 | 第 1 章与后续 heating/noise 主线 | `K_4`、QPM、potential correction 的正式 bibliographic 落点 | 当前无 full text；ScienceDirect `pdf` 端点在本环境下不可直接 materialize |
| `Eastwood and Hockney 1974` fallback | 无本地 PDF；正式题名/DOI 已确认 | 第 1 章与第 5 章 shape/force law 主线 | force anisotropy 与 shape comparison 的正式 bibliographic 落点 | 当前无 full text；不能把图和结论当作已核正文据 |
| `Yee 1966` | metadata/DOI 已确认；当前无本地 PDF / MinerU 产物 | 第 2 章优先，后续第 6 章 FDTD 主线 | staggered FDTD 的原始历史入口、`Yee` 命名与离散 Maxwell solver 谱系的 bibliographic 落点 | 当前不能把其正文细节写成已核实的一手推导 |

## 按章节的当前用法

### 第 1 章 `01-kinetic-models.md`

当前允许直接当正文证据的来源：

- `Birdsall 1985`
  - `N_D`
  - Debye/统计时间尺度
  - fluctuation / heating / aliasing 主线
- `Dawson 1983`
  - superparticle
  - weighted particles
  - finite-size particles
  - numerical experiment 视角

当前只允许写成“待补的一手来源”的条目：

- `Hockney-Eastwood`
- `Hockney 1971 / 1974 / Eastwood-Hockney 1974`
- `Yee 1966`

这意味着第 1 章当前版本的安全边界是：

- 可以把 `Birdsall + Dawson` 当作已核实的一手理论基础；
- 可以把 `Hockney/Eastwood` 当作明确的来源缺口与后续增强方向；
- 不能把 `Hockney/Eastwood/Yee` 的原始推导、原图或原书措辞冒充成已核正文据。

### 第 2 章 `02-pic-loop.md`

当前允许直接当正文证据的来源：

- `Birdsall 1985`
  - leapfrog 最小教学骨架
  - `\\omega_p\\Delta t`
  - `v_t\\Delta t/\\Delta x`
  - finite-grid / aliasing / heating
- `Dawson 1983`
  - electrostatic / full EM 的数值模型边界
  - full EM 时间步受 light mode / CFL 限制
  - Darwin 作为 radiation-free 低频 route

当前只允许写成“原始历史入口待补”的条目：

- `Yee 1966`
  - 当前只可作为 staggered FDTD 原始来源的 acquisition target
- `Hockney-Eastwood`
  - 当前只可作为 particle-mesh / heating / optimum-path 的待补原始来源

这意味着第 2 章当前版本的安全边界是：

- 可以从本地 WarpX 源码和 `Birdsall + Dawson` 已核实内容出发，讲清 PIC loop、CFL、`\lambda_D`、`\omega_p` 和离散色散；
- 但如果要把这些段落再提升为“基础文献层完全闭环”，仍需要补进 `Yee 1966` 与 `Hockney-Eastwood` 的一手正文。

## 当前最优先的 acquisition 缺口

按基础章节价值排序，当前最优先缺口是：

1. `Yee 1966`
   - 因为它直接补第 2 章里 staggered FDTD 与离散 Maxwell solver 的原始历史入口。
2. `Hockney-Eastwood` 原书
   - 若原书继续不可得，则回退到：
   - `Hockney 1971`
   - `Hockney et al. 1974`
   - `Eastwood and Hockney 1974`

## 当前结论

基础章节文献层当前已经达到的状态是：

- `Birdsall 1985` 和 `Dawson 1983` 已足以作为第 1/2 章当前正文的直接一手支撑；
- `Hockney-Eastwood` 与 `Yee 1966` 的 bibliographic identity 和 acquisition 边界已经清楚；
- 但这两条线仍未 materialize 为可直接进入 MinerU-first 精读流程的本地正文资产。

因此，阶段 B 现在可以判定为：

- `chapter-writing side` 已收口；
- `literature-list side` 已建立并明确边界；
- `full primary-source closure` 仍留待后续 acquisition 主线继续推进。

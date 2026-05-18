# Reading Log

## 2026-05-18

- 从 `/Users/yuxiangzhang/Documents/Zoteropaper/laser acceleration/LWFA/` 发现本地现成 PDF。
- 已复制到项目内论文专属目录：
  - `references/03_pic_foundations/1979_TajimaDawson_Laser_Electron_Accelerator/`
- 已按 `research-paper-explainer` 的 MinerU 流程完成 Markdown 转换。
- 当前目录已具备：
  - 原 PDF
  - MinerU Markdown
  - `images/`
  - 中文讲解笔记骨架
- 下一步：
  - 开始逐段中文精读，并回填到 `LWFA/PWFA` 应用综合章。

## 2026-05-18 第二次更新

- 已完成第一轮精读，当前覆盖：
  - 摘要
  - 引言
  - 最小解析模型
  - wave-breaking 场标度
  - 最大能量 / 加速长度的最早期 scaling
- 当前已明确压实：
  - `driver -> wake -> trapping -> acceleration` 是这篇文章的最小闭环
  - `v_p = v_g^{EM}` 是后续 dephasing 叙事的最早期入口
  - `L_t = \lambda_w/2` 是最原始的 wake-excitation 匹配条件
  - `eE_L \cong mc\omega_p` 是 Tajima-Dawson 场标度原型
  - `\gamma_{\max} \simeq 2\omega^2/\omega_p^2` 与 `l_a \cong 2\omega^2 c/\omega_p^3` 是最早期 LWFA scaling
- 已开始回填到：
  - `notes/code-reading/applications/02-lwfa-pwfa.md`
  - `manuscript/chapters/08-diagnostics-cases.md`
- 下一步：
  - 继续补 simulation 细节
  - 抽取 multiple forward Raman scattering 与 wake saturation 的最早期表述

## 2026-05-18 第三次更新

- 已继续完成第二轮精读，当前新增覆盖：
  - `1 1/2-D` relativistic electromagnetic code 的最小数值合同
  - 系统长度、粒子数、Gaussian particle shape、固定离子背景
  - 通过改变 `c` 扫描 `\omega/\omega_p` 的相似律设置
  - wake amplitude 达到 `0.6 mc\omega_p/e`
  - successive / multiple forward Raman scattering
  - photon deceleration
  - simulation 最大能量与 Eq.(8) scaling 的直接对照
- 当前已明确压实：
  - 这篇文章既是 earliest LWFA scaling paper，也是最小 relativistic EM PIC demonstration
  - 它能支撑 wake growth、driver slowdown、Raman-like cascade 的最早期讨论
  - 但它仍不能直接充当现代 WarpX `laser_acceleration` runtime matrix 的 regression contract
- 下一步：
  - 补 feasibility、two-laser alternative 与 astrophysical speculation 的边界

## 2026-05-18 第四次更新

- 已继续完成第三轮精读，当前新增覆盖：
  - `present-day technology` 语境下的 feasibility 判断
  - pulse chopping / short-pulse engineering 仍是当时 bottleneck
  - 双频 `\Delta\omega = \omega_p` 的 two-laser / beat-wave alternative
  - pulsar atmosphere / cosmic-ray source 的 speculative extrapolation
- 当前已明确压实：
  - 原文的 `feasible` 只是 1979 年的工程可行性语气，不等于现代装置级结论
  - 这篇文章支撑的是更宽的早期 wakefield / beat-wave family，而不是今天单一路径的 `LWFA` 目录
  - astrophysical speculation 只能当历史语境补充，不能进入现代 WarpX 应用合同
- 下一步：
  - 整理图 1 / 图 2 与正文论证的精确对应
  - 然后转入 `Dawson 1983`

## 2026-05-18 第五次更新

- 已继续完成第四轮精读，当前新增覆盖：
  - Fig.1(a)/(b)/(c) 与正文的机制链对应
  - arm-like phase-space pattern 作为 trapping 证据
  - Fig.2(a) 作为 driver spectrum splitting / Raman-like cascade / photon deceleration 图
  - Fig.2(b) 作为解析 scaling 与 simulation 对照图
- 当前已明确压实：
  - Fig.1 不是普通结果图，而是 `transverse quiver -> wake -> accelerating field` 三联图
  - Fig.2 不是普通谱图和散点图，而是 `driver evolution + scaling check` 的组合证据
  - `Tajima-Dawson 1979` 这篇的第一轮精读主线已经基本收口
- 下一步：
  - 转入 `Dawson 1983`

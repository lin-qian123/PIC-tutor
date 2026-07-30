# Public repository release audit

审计日期：2026-07-30

当前 release 为 v0.110；本版重新执行正式收敛 study 的第二组 12 个 2-rank producer，correction-on 14 项 repeat-slope gate 全部通过，最大绝对 slope 差为 `2.0135e-11`。分类为 `FORMAL_CONVERGENCE_REPEAT_SLOPE_GATE_PASS_CHARGE_CLOSURE_OPEN`，不把该结果写成 formal order 或 axis-charge closure。第 1--9 章入口已完成读者化审读；第 1 章的源码定位练习现从 `OneStep_nosub()` 起步，并要求读者产出粒子沉积、source 同步和场更新的三行调用表。连续审读还修复了 `1.12` 的块分隔错误：其现独立排版于 PDF 第 14 页并列入首页目录，构建验收固定检查第 1 章标题序列和 PDF 目录锚点。第 2 章现以数学符号说明 $\omega_p$、$\lambda_D$ 与 $\Delta t/\Delta x$，并把官方 1D Langmuir 输入、CMake 的 2-rank 注册、解析场和离散 Gauss-law 检查串成读者可复查的案例闭环；它明确区分输入显式设置、分析器消费的末态 surface 和不可外推范围。第 3 章现以文件路径和函数符号而非固定行号导航源码，校正运行中自适应步长入口为 `ApplyDtLimiters()`，并将 1D Langmuir 的输入、2-rank CTest 注册、分析命令、$E_z$ 误差阈值和 Gauss-law 检查闭合为一条读者可复查路线；它明确说明输入未显式设置 Maxwell solver。第 3A 章现补正 fresh-run 的 AMReX level 回调、implicit solver 属性创建、粒子/PML/callback 时序，并严格区分写入主网格场的 grid external field 与只供 gather 的 particle external field；file-driven external field 与 moving window 的实现不兼容已在正文和审计中锁定。第 5 章进一步将源码交叉检查改为读者问题导航，并把 Vay 结果收束为可用范围和不可外推边界；本轮章末结论又以连续性观察量、算法约束、source 同步和证据范围形成判断路线。第 6 章现以几何、source 时间模型、边界/耦合和验证量形成求解器选择闭环，并以官方 Picard 案例取代本地运行记录式练习。第 7 章的入口和结尾改以 field/particle 拓扑、PML/guard-cell 更新、AMR 状态迁移与观察量选择组织，并保留 transition-zone route ledger 的明确边界。第 9 章统一采用可核查材料、可支持结论与访问边界的文献语言。第 2、3、3A、4、5、8、9 章的深层证据段也已移除开发过程措辞和绝对工作区路径，并把读者入口改为相对链接。第 3 至 7 章原先会在 PDF 中泄露的 Mermaid 流程现均已替换为可打印的决策表、编号路线或闭合链；第 6 章宽求解器表改为分组路径速查，第 7 章以参数、场/PML、AMR 与粒子诊断串联边界闭合系统。第 4 章现已将边界、PML、AMR 和两类 QED 分叉收束为从时间层、tile 主链到观察量和模型选择的排错路线，并在章末加入官方 QED analysis 练习；附录 A 现在区分输入 `gamma*beta`、内部 `gamma*v` 和输出 metadata 的动量约定，并补充 AMR 数组生命周期提示。第 1、14--15、22、24--26、31、40--41、49--50、57、106--119、167--171、206--208、219--220、258--261 页已视觉抽查，且 265 页 PDF 的全页文本扫描未检出 `flowchart` 或 `-->`。全书通读、route-count ledger、axis charge correctness、RZ implicit runtime、许可和公开再分发仍保持开放。

本轮第 4 章核心路线复核将固定行号与笔记目录从教程中移除，改以文件路径和函数符号导航；`do_crr` 的 QED 同步 \(\chi\) 门限、`getExternalEB(...)` 的 gather 后插入位置、`UpdatePosition()` 的时间中心动量语义及 Boris/Higuera--Cary 的 split-half 差异均已回查当前源码。第 71、89、118 页的人工视觉抽查通过，读者化与构建验收新增相应回归检查。

全书正文扫描确认绝对工作区路径与开发过程标记均为零。第 5 章两张宽表已由列式矩阵改为分组证据列表，并在 PDF 第 158--159 页人工复核；这只关闭该处的版式风险，不替代全书通读。

**公开分发阻断项：**remote 当前为 public，Git 实际跟踪 `references/` 下 `2,425` 个文件（`52` 个 PDF、`2,259` 个图片，约 `190.7 MB`），根目录没有项目许可证。release manifest 排除 `references/` 并不会从 public branch、clone 或 Git 历史中移除这些材料；详见 `docs/public-distribution-risk-register-v0.110.md`。在维护者决定逐项授权、分支移除/历史策略和项目许可证前，本审计不签收公开再分发。

v0.78 完成 Esirkepov 2001 CPC indexed abstract 与 arXiv 预印本的 bounded compare；该 contract 只确认发表版 metadata/abstract 级算法主张已归类，不把 publisher-PDF 缺口写成已关闭。

当前 `dist/pic-tutor-v0.110.pdf` 页数以本轮构建验收为准；第 4.13.10 节现将边界 scraping 与 Python 粒子操作拆分为可读的容器、属性/注入/沉积和回归覆盖三层，明确 `particle_data_python` 的 `--unique` 形参未被输入实际消费，restart sibling 的 analysis/checksum 仍为 OFF，single-precision particle-fields 分析脚本尚未接入活跃回归。v0.75 及此前的构建记录均属于历史构建快照。

v0.66 审计发现合订 Markdown/HTML 含本机绝对路径和不可随公共仓库迁移的绝对链接；v0.67 已在 release 构建层修复，v0.75 延续该检查，并将验证合同摘要、文献 triage、沉积算法选择矩阵和 paper asset contract 纳入公共 allowlist；论文 `references/` 原始资产仍按逐篇许可边界排除。

v0.78 延续 `docs/public-evidence-index.{json,md}`，从本地 contract 生成去路径摘要，并加入 `docs/literature-pending-triage.md` 的 acquisition/read queue。摘要保留原始合同状态，并将 boundary、unproven、missing 分类单独标记；原始 `runs/` 仍排除，因此该摘要是公共证据目录，不是运行产物替代品。

本文件只记录发布边界和体积证据，不自动删除或移动工作区文件。真正 push 前仍需由维护者确认论文 PDF、图片和其他第三方材料的授权状态。

第 9 章的读者化重写已将材料数量、转换过程和发布策略从教程主线移除，改为 A/B/C/D 证据层、可支持结论和沉积/PML 深读任务；当前产物的第 259--260 页已人工复核。该编辑不改变第三方材料的许可边界，也不签收公开再分发。

## 当前体积快照

| 路径 | 当前体积 | 发布判断 |
|---|---:|---|
| `runs/` | 约 3.1 GB | 本地运行产物；由 `.gitignore` 忽略，不应整体 push |
| `references/` | 约 174 MB | 逐篇检查版权/许可后再决定；不能默认整体公开 |
| `dist/` | 约 90 MB | 含多代历史 HTML/Markdown；不应把全部历史生成物当作当前 release |
| `dist/pic-tutor-v0.110.pdf` | 3,006,266 bytes / 265 页 | 当前成书候选，可单独审计后发布 |
| `dist/pic-tutor-v0.110.html` | 5,260,105 bytes | 自包含 MathJax + 15 张图片，可作为预览候选 |
| `dist/pic-tutor-v0.110.md` | 866,006 bytes | 当前合订源，可作为文本 release 候选 |

## 当前边界

- `runs/` 已加入忽略规则；本轮又忽略了根目录运行残留 `Backtrace.*` 和 `bmmntr.txt`。
- 当前书稿图表位于 `manuscript/assets/figures/`，源章节使用相对路径；`scripts/build_v96.py` 会在合订阶段解析资源。
- `dist/` 当前仍保留历史版本产物，发布时应明确选择 `v0.110`，不要按目录整体上传。
- `references/` 中的论文 PDF、MinerU 图片和讲解笔记应按论文逐项确认公开许可；本审计不把“本机可读”当作“可公开分发”。
- `README.md`、`TODO.md`、`manuscript/VERSION.md` 和本文件应在 push 前再次同步当前 release 选择。

## v0.110 建议发布清单

建议纳入公共仓库的项目内资产：

- `AGENTS.md`、`README.md`、`TODO.md`；
- `manuscript/` 书稿源、`manuscript/assets/figures/` 15 张验证图和 `manuscript/VERSION.md`；
- `scripts/build_v110.py`、`scripts/verify_v110_build.py`、`scripts/audit_reader_facing_content.py`、`scripts/audit_release_consistency.py`、`scripts/audit_rz_axis_correction_nonneutral_control.py`、`scripts/audit_rz_axis_correction_nonneutral_shape_family.py`、`scripts/audit_rz_axis_correction_nonneutral_density_triple.py`、`scripts/run_formal_convergence_repeat_family.py`、`scripts/analyze_formal_convergence_repeat_family.py`、`scripts/audit_formal_convergence_repeat_slope_gate.py` 及书稿引用的项目分析脚本；
- `docs/` 中的项目说明、验证矩阵、读者视角编辑审查和本发布审计；
- `docs/public-evidence-index.{json,md}`；
- `docs/transition-zone-route-contract.{json,md}` 与 `scripts/validate_transition_zone_route_contract.py`；
- `dist/pic-tutor-v0.110.md`、`dist/pic-tutor-v0.110.html`、`dist/pic-tutor-v0.110.pdf`，前提是维护者确认生成物的发布策略。

明确排除：

- `runs/`、`Backtrace.*`、`bmmntr.txt` 等本地运行和调试产物；
- `dist/` 中 v0.47 以前的历史生成物；
- `references/` 中未逐项确认公开许可的第三方 PDF、图片和转换产物；
- `warpx_used_inputs` 等根目录临时输出。

## 发布前命令

```bash
python scripts/build_v110.py
python scripts/verify_v110_build.py --build-log /tmp/pic-tutor-build-v110.log
python scripts/audit_release_consistency.py
git status --short
```

当前 v0.110 构建验收结果以 `scripts/verify_v110_build.py`、`scripts/audit_rz_axis_correction_nonneutral_control.py`、`scripts/audit_rz_axis_correction_nonneutral_shape_family.py`、`scripts/audit_rz_axis_correction_nonneutral_resolution_family.py`、`scripts/audit_rz_axis_correction_nonneutral_density_triple.py`、`scripts/audit_editorial_quality.py`、`scripts/audit_pdf_layout.py`、`scripts/audit_formal_convergence_preregistration.py`、`scripts/audit_formal_convergence_repeat_slope_gate.py`、`scripts/run_formal_convergence_repeat_family.py`、`scripts/analyze_formal_convergence_repeat_family.py`、`scripts/audit_rz_axis_charge_repeat_stability.py`、`scripts/analyze_rz_axis_divergence_stencil_contract.py`、`scripts/analyze_rz_axis_divergence_resolution_contract.py`、`scripts/analyze_rz_axis_divergence_fit_contract.py` 和 `scripts/audit_transition_zone_runtime_activation.py` 为准；route-count ledger、axis charge correctness、正式收敛阶、人工全书通读、许可和公开再分发仍保持开放。

v0.110 发布 allowlist 另见 `docs/v0.110-release-manifest.{json,md}`；总字节数以 manifest 的 `total_bytes` 为准，`runs/`、`references/`、历史 `dist/` 和调试残留均被排除。该 manifest 是审计输入，不自动执行 Git staging、commit 或 push。

验收脚本证明的是成书构建和资源合同，不替代第三方材料的版权审计，也不替代 GitHub 仓库最终 staged 文件清单审阅。

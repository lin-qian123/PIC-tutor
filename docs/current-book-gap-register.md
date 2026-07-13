# PIC-tutor 当前成书缺口登记

本表是 v0.81 的当前状态快照，不是历史 TODO 的完整替代品。每一项都必须同时有：当前证据、明确分类、下一步动作和可验收的关闭条件。`OPEN_EXTERNAL_ACCESS`、`RUNTIME_LEDGER_UNPROVEN`、`PRE_PHYSICS_BOUNDARY` 和 `UNPROVEN` 都表示尚未完成，不是 PASS。

| ID | 缺口 | 当前分类 | 当前证据 | 下一步动作 | 关闭条件 |
|---|---|---|---|---|---|
| `LIT-ESIRKEPOV-PUBLISHER` | Esirkepov 2001 CPC 定稿逐页对照 | `OPEN_EXTERNAL_ACCESS` | `runs/stage-c-validation/esirkepov-publication-boundary/contract.json` | 取得合法 publisher PDF，核 title/abstract/section、`Eq.(23)`、二阶 spline | 五项 bounded compare 有 publisher PDF 直接页码证据 |
| `LIT-LEE-PUBLISHER` | LeeCPC2015 publisher-formatted PDF 与 accepted manuscript 差异 | `OPEN_EXTERNAL_ACCESS` | `runs/stage-c-validation/leecpc2015-accepted-manuscript-contract/contract.json` | 获取正式 CPC 版本并更新版本差异表 | publisher PDF、MinerU 和逐项差异合同通过 |
| `RUNTIME-TRANSITION-ZONE` | fine/coarse gather/deposit route-count ledger | `RUNTIME_LEDGER_UNPROVEN` | `runs/stage-c-validation/transition-zone-source-contract.json`、`docs/transition-zone-route-contract-example.json` | 在允许修改 WarpX 的独立分支接入 runtime hook；当前书稿保持只读 | 真实 `current_buf/rho_buf`、coarsen、owner-mask、post-sync 数据通过同一 schema |
| `RUNTIME-RZ-IMPLICIT-VILLASENOR` | RZ theta-implicit Villasenor 进入物理推进 | `PRE_PHYSICS_BOUNDARY` | `runs/stage-c-validation/rz-implicit-villasenor-build-boundary/contract.json` | 使用启用 PETSc 或修复 arm64 boundary-mask 的兼容 binary 重跑 | 进入粒子推进并完成 field/charge consumer，而非初始化阶段退出 |
| `RUNTIME-VAY-AMR` | Vay + AMR 运行覆盖 | `SOURCE_GUARD_RUNTIME_INTENTIONALLY_REJECTED` | `runs/stage-c-validation/vay-amr-guard/contract.json` | 由上游决定支持/继续拒绝；本项目不修改相邻 WarpX | 支持路径进入官方测试，或正式文档明确将其列为不支持范围 |
| `PHYSICS-RZ-AXIS-CHARGE` | 默认 axis correction 下 RZ charge residual | `BOUNDARY` | `runs/stage-c-validation/esirkepov_langmuir_rz-charge-field-tradeoff-summary/contract.json` | 固定 axis observable、默认参数和 resolution family，继续查明误差来源 | 默认配置下 charge gate 有稳定解释和独立 runtime 证据 |
| `STUDY-FORMAL-CONVERGENCE` | 跨 resolution/observable 的正式收敛阶 | `CONVERGENCE_READINESS_WITH_FORMAL_ORDER_UNPROVEN` | `runs/stage-c-validation/deposition-convergence-readiness/contract.json` | 预注册 norm、控制变量、拟合区间，补独立 refinement family | 重复/独立 family 的 order 在预注册 gate 内稳定 |
| `RELEASE-EDITORIAL` | 最终人工通读、HTML/PDF 排版和公开再分发审计 | `AUTOMATED_EDITORIAL_AUDIT_PASS_MANUAL_REVIEW_OPEN` | `docs/editorial-quality-audit-v0.81.md`、`runs/stage-c-validation/editorial-quality-v0.81/contract.json`、`docs/public-repo-release-audit.md` | 对当前候选版做人工阅读和许可/公开性复核 | 编辑问题、宽表格、公开许可和 release checklist 全部签收 |

本表由 `scripts/audit_current_gap_register.py` 验收。合同通过只表示登记项、分类和证据路径没有漂移，不表示任何一项缺口已经关闭。

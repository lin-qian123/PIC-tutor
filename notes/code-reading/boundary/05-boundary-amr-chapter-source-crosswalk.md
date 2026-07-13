# 第 7 章边界、PML 与 AMR 正文-源码 crosswalk

本笔记把第 7 章当前正文的代表性入口固定到 WarpX 当前源码。它用于维护章节与源码的同步，不替代 runtime regression，也不把 transition-zone 的设计合同升级为已经接入的 route-count instrumentation。

## 维护边界

1. **参数与边界顺序**：`WarpX.cpp` 先解析 field boundary，再用 periodic mask 约束 particle boundary。
2. **场边界分派**：`WarpXFieldBoundaries.cpp` 维护 E/B 的 PEC、PMC、PECInsulator 和 Silver-Mueller 入口；正文必须区分场镜像、粒子边界和 rho/J 反射。
3. **PML 生命周期**：`WarpXInitData.cpp` 的 `InitPML`/`CheckGuardCells`、`WarpXEvolvePML.cpp` 的 `DampPML` 和 `PML.cpp` 的 exchange/transform 共同构成 PML 子域生命周期。
4. **通信与 guard cell**：`WarpXComm.cpp` 的 `FillBoundaryE/B` 处理 fine/coarse、PML 和 guard-cell 分支；`GuardCellManager.cpp` 根据 solver、粒子 shape、NCI、moving window 和 subcycling 预算数量。
5. **AMR 与 moving window**：`WarpXRegrid.cpp` 的 `RemakeLevel` 和 `WarpXMovingWindow.cpp` 的 `MoveWindow` 分别负责数组/分布重建与窗口移动；不能把二者混成普通 field boundary。
6. **粒子边界与诊断**：`ParticleBoundaries_K.H` 的 kernel 和 `BoundaryScrapingDiagnostics.cpp` 的 buffer consumer 分开记录；boundary buffer 存在不等于 transition-zone route ledger 已输出。

## 可重复检查

```bash
python scripts/audit_boundary_amr_chapter_source_crosswalk.py \
  --warpx-root ../warpx \
  --output-json runs/stage-c-validation/boundary-amr-chapter-source-crosswalk/contract.json \
  --output-md runs/stage-c-validation/boundary-amr-chapter-source-crosswalk/contract.md
```

当前合同预期为 `13/13` PASS。脚本通过只表示本章引用的代表性入口仍能在当前 checkout 中找到；transition-zone 的 `TransitionZoneRoutes`/`amr_transition_zone` 缺失仍应保持 `RUNTIME_LEDGER_UNPROVEN`，直到 WarpX 侧实际接入并运行专门 regression。

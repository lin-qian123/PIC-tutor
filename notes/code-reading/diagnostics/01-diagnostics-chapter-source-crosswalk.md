# 第 8 章诊断与验证正文-源码 crosswalk

本笔记把第 8 章的验证矩阵和案例叙述固定到 WarpX 当前 diagnostics producer/consumer 源码。它维护的是“输入/主循环/写盘/analysis”之间的连接，不把某个 writer schema 或字符串存在性检查升级成 physics proof，也不替代 case-local runtime contract。

## 维护边界

1. **主循环调度**：`WarpXEvolve.cpp` 的 `FilterComputePackFlush`、末步 flush 和 `reduced_diags->WriteToFile` 决定 diagnostics 何时消费状态。
2. **Full/BTD/BoundaryScraping 类型**：`MultiDiagnostics.cpp` 与 `Diagnostics.H` 负责类型注册和共享调度；BoundaryScraping 仍有自己的 buffer/flush 语义。
3. **Full writer**：`FullDiagnostics.cpp` 通过 `ComputeDiagFunctors` 计算字段，再把结果交给 `FlushFormats`；这和 reduced diagnostics 的文本/openPMD producer 不应混写。
4. **OpenPMD 生命周期**：`WarpXOpenPMD.H` 的 particle/field writer、`CloseStep` 和 flush 表面定义 openPMD iteration 的落盘边界。
5. **Reduced diagnostics**：`MultiReducedDiags.cpp` 注册 `FieldProbe`、`ParticleHistogram2D`、`ColliderRelevant`、`DifferentialLuminosity` 和 `LoadBalanceCosts` 等族，`WriteToFile` 是它们的统一写盘入口。
6. **验证证据等级**：官方 analysis、项目独立 reader-side contract、checksum、schema/producer smoke 和 performance gate 必须在矩阵中分开；章节 crosswalk 通过不代表所有案例 runtime 已通过。

## 可重复检查

```bash
python scripts/audit_diagnostics_chapter_source_crosswalk.py \
  --warpx-root ../warpx \
  --output-json runs/stage-c-validation/diagnostics-chapter-source-crosswalk/contract.json \
  --output-md runs/stage-c-validation/diagnostics-chapter-source-crosswalk/contract.md
```

当前合同预期为 `13/13` PASS。若 diagnostics 类型、writer 生命周期或案例 consumer 发生源码重构，应先更新本 crosswalk 和第 8 章，再重新生成 v0.68；不能仅凭目录存在或 checksum 通过推导出完整物理验证。

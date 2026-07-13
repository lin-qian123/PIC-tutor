# 第 6 章 FieldSolver 正文-源码 crosswalk

本笔记把第 6 章当前正文的代表性主张固定到 WarpX 当前源码表面。它的作用是防止源码演进后正文入口漂移，不把字符串存在性检查写成算法语义等价证明，也不替代 runtime regression。

## 五组维护边界

1. **外层推进**：`WarpXEvolve.cpp` 同时保留 `SyncCurrentAndRho`、FDTD 的 `EvolveB/EvolveE` 路径、`PushPSATD` 和 `OneStep_JRhom` 入口。
2. **FDTD/PML**：`EvolveB.cpp`、`EvolveE.cpp` 绑定 Cartesian Yee curl；`EvolveBPML.cpp`、`EvolveEPML.cpp` 绑定 split-field PML kernel；`PML.cpp` 负责 transform、exchange 和回填表面。
3. **Cartesian spectral**：`SpectralSolver.cpp` 的算法构造覆盖 PML、Galilean 和 JRhom 一阶/二阶分派；`WarpXPushFieldsEM.cpp` 还保留 PSATD current correction 与 Vay deposition 入口。
4. **RZ spectral**：`SpectralSolverRZ.cpp` 的构造面覆盖 standard RZ、PML RZ 和 Galilean RZ；正文的 Hankel、mode decomposition、`Ep/Em` 解释必须与这条入口保持一致。
5. **regression 证据边界**：正文区分 `analysis_galilean.py`、Langmuir/PML 等带物理量断言的 consumer 与 checksum-only workflow，不能把后者升级成稳定性证明。

## 可重复检查

```bash
python scripts/audit_field_solver_chapter_source_crosswalk.py \
  --warpx-root ../warpx \
  --output-json runs/stage-c-validation/fieldsolver-chapter-source-crosswalk/contract.json \
  --output-md runs/stage-c-validation/fieldsolver-chapter-source-crosswalk/contract.md
```

当前合同预期为 `12/12` PASS。若 WarpX 重构入口，先更新本 crosswalk 和第 6 章的路径说明，再重新构建成书；不要仅因脚本通过就宣称 runtime 或论文推导已经验证。

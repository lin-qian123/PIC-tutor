# LeeCPC2015 paper/source/regression crosswalk

审计日期：2026-07-13

## 本轮完成的闭环

新增 `scripts/audit_leecpc2015_source_crosswalk.py`，对三层证据做只读交叉审计：

1. 本地 accepted/submitted manuscript 的 PSTD、staggered-grid phase、reflection recurrence、infinite-order PSTD 和 `sigma` profile 锚点；
2. 当前 `../warpx` 的 `PML.cpp` profile surface 与 `PsatdAlgorithmPml.cpp` 的 `C1`、`C10`、`C23-C25`、`T2`、`F/G` cleaning surface；
3. 官方 `pml` 测试的 `analysis_pml_psatd.py` reflectivity consumer 和 CMake wiring。

当前交叉审计的意义是把“论文讲了什么”“WarpX 实现了什么”“regression 实际检查什么”分成同一张可重复表，而不是把它们混成同一个证明。

## 结果解释

若 contract 通过，表示三层锚点都存在并且路径相互一致：

- 论文层支持 PSTD staggered-grid phase、PML reflection recurrence 与 high-order/infinite-order comparison；
- 源码层确认 PML profile、Cartesian PSATD propagator、divergence-cleaning `F/G` 和 Galilean `T2` 都是当前实现表面；
- regression 层确认 `test_2d_pml_x_psatd` 的自动消费者是初始场能量一致性和最终 reflectivity `< 1e-6`。

这仍不等价于：

- accepted manuscript 就是 publisher-formatted CPC PDF；
- 论文公式已经逐项等同于 WarpX `C1-C25`；
- regression 已经逐系数验证 `C1-C25`、`F/G` 或 `T2`。

## 可重放命令

```bash
python scripts/audit_leecpc2015_source_crosswalk.py \
  --paper-dir references/08_boundaries_pml_geometry/2015_LeeCPC2015_Efficiency_of_the_PML_with_high-order_FD_and_pseudo-spectral_Maxwell_solvers \
  --warpx-root ../warpx \
  --output-dir runs/stage-c-validation/leecpc2015-source-crosswalk
```

机器可读结果和表格报告分别写入 `contract.json` 与 `contract.md`；`runs/` 仍是本地 producer output，不进入公共 release。

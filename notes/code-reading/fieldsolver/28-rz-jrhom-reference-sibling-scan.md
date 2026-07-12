# RZ JRhom LL2 reference sibling 扫描骨架

绑定对象：

- `scripts/build_rz_psatd_reference_ledger.py`
- `scripts/scan_rz_jrhom_reference_candidates.py`
- `../warpx/Examples/Tests/nci_psatd_stability/inputs_test_rz_psatd_JRhom_LL2`
- `27-rz-jrhom-ll2-analysis-direction.md`

## 目标

前一条笔记已经把方向压实：`test_rz_psatd_JRhom_LL2` 的第一阶段独立 main analysis，更适合先走 stability-style 末态 field-energy gate，而不是直接套 Langmuir 式解析场 gate。

那下一步最实际的问题就变成：

**reference sibling 要怎么找，才能尽量少改 producer，又有机会形成可用的末态 field-energy ordering？**

这份笔记记录的不是最终运行结论，而是把这一步先收成可执行脚本骨架。

## 新增脚本

### 1. `scripts/build_rz_psatd_reference_ledger.py`

用途：

- 读取 RZ plotfile；
- 提取 `Er/Ez/Bt/jr/jz/rho` 的基础统计；
- 计算
  - `electric_energy`
  - `magnetic_energy`
  - `e_mag_max`
  - `e_mag_p99`
  - `spike_ratio`
- 输出 provenance-friendly markdown/json ledger。

它对应的是 RZ 版的 reference-ledger builder，不再复用 comoving 的 `Ex/Ey/Ez` 口径。

### 2. `scripts/scan_rz_jrhom_reference_candidates.py`

用途：

- 在不改主输入卡文件的前提下，用命令行 override 生成一组最小改动 sibling；
- 对每条 sibling 运行 WarpX；
- 默认读取 `diags/diag1000025`；
- 自动提取 field-energy / spike 指标；
- 写出统一的 markdown/json 汇总。

## 第一批候选为什么这样选

当前脚本先不做大范围 brute-force，而是只保留五条最小改动候选：

1. `baseline-jrhom-ll2-timeavg-cleaning`
   - 当前原始 workflow；
   - 作为比较基线。

2. `cl1-timeavg-cleaning`
   - 保留 `do_time_averaging` 和 cleaning；
   - 把 `psatd.JRhom="LL2"` 切成更普通的 `psatd.JRhom="CL1"`；
   - 用来测试“只改时间依赖口径”是否足以产生 energy ordering。

3. `ll2-no-timeavg-cleaning`
   - 保留 `JRhom="LL2"` 和 cleaning；
   - 只关掉 `psatd.do_time_averaging=0`；
   - 用来测试 average-field 路径是否是主要稳定化因素。

4. `ll2-timeavg-no-cleaning`
   - 保留 `JRhom="LL2"` 和 time averaging；
   - 只关掉 `warpx.do_dive_cleaning=0` 与 `warpx.do_divb_cleaning=0`；
   - 用来测试 cleaning 路径是否提供了主要 ordering。

5. `cl1-no-timeavg-no-cleaning`
   - 组合式强对照；
   - 同时切到 `CL1`、关掉 time averaging、关掉 cleaning；
   - 它不是“最小物理解释”的首选，但适合回答“如果把这几条 stabilizer 一起放掉，energy 是否明显抬升”。

这组候选的共同原则是：

- 不改 moving window；
- 不改 rigid driver / return beam / continuous plasma injection；
- 不改 geometry；
- 不改 diagnostics cadence；
- 只动 `JRhom / time_averaging / cleaning` 这几条最接近 solver-contract 的开关。

## 第一轮本地结果

当前已经实际运行过一轮：

```bash
python scripts/scan_rz_jrhom_reference_candidates.py --force-rerun
```

并生成：

- `runs/fieldsolver-validation/rz-reference-ledgers/rz-jrhom-reference-scan.md`
- `runs/fieldsolver-validation/rz-reference-ledgers/rz-jrhom-reference-scan.json`

在默认 `max_step=25`、即当前 active checksum surface `diag1000025` 上，第一轮结果是：

| candidate | status | energy / baseline | spike / baseline | 当前解释 |
|---|---|---:|---:|---|
| `baseline-jrhom-ll2-timeavg-cleaning` | `ok_with_finalize_error` | `1.0000` | `1.0000` | 当前稳定基线 |
| `ll2-no-timeavg-cleaning` | `ok_with_finalize_error` | `1.02345` | `1.05563` | 当前最强的 unstable-reference 候选 |
| `ll2-timeavg-no-cleaning` | `ok_with_finalize_error` | `0.97905` | `0.98041` | 单独去掉 cleaning 不会抬高能量 |
| `cl1-no-timeavg-no-cleaning` | `ok_with_finalize_error` | `0.98325` | `1.02790` | spike 升高，但能量仍低于 baseline |
| `cl1-timeavg-cleaning` | `run_failed` | n/a | n/a | 源码直接拒绝：RZ `do_time_averaging=1` 只支持 `J` 线性时间依赖 |

这里最重要的不是绝对数值，而是排序：

1. `ll2-no-timeavg-cleaning` 同时给出最高 `electric_energy` 和最高 `spike_ratio`；
2. `ll2-timeavg-no-cleaning` 反而把 `energy` 和 `spike` 都压低；
3. `cl1-timeavg-cleaning` 不是“差一点”的候选，而是**参数组合本身非法**。

因此，当前第一轮 sibling 扫描已经足够把下一步优先级收窄到：

- **优先用 `ll2-no-timeavg-cleaning` 作为第一阶段 field-energy gate 的 reference sibling 候选；**
- 不再把 `cl1-timeavg-cleaning` 视为可运行候选；
- `cleaning-only` 对比当前不支持“去 cleaning 会更不稳定”这一路假设。

## 本机运行噪声边界

这轮可运行候选都带同一条已知尾噪声：

```text
MPI_Finalize failed
OFI poll failed (default nic=utun6: Input/output error)
```

它发生在 plotfile 已经落盘之后，因此当前脚本把这类结果标成：

- `ok_with_finalize_error`

而不是简单归为 `run_failed`。也就是说，这轮排序是建立在**plotfile 已经完整落出**的前提上，而不是靠猜测“也许算到了”。

## 推荐下一步

当前最直接的执行入口就是：

```bash
python scripts/scan_rz_jrhom_reference_candidates.py
```

脚本当前默认绑定的是：

```text
../warpx/build_full/bin/warpx.rz.MPI.OMP.DP.PDP.OPMD.FFT.EB.QED.GENQEDTABLES
```

这里必须用 `RZ` binary，而不能误绑 `warpx.2d...`。当前这台机器上已经实际踩到过这个坑：若用 `2d` binary 直接驱动 `geometry.dims = RZ` 的输入卡，会在 `warpx::initialization::check_dims()` 里启动即 abort，还没进入任何 sibling 物理比较。

脚本当前还默认附带：

```text
max_step=25
```

这里不是为了随便缩短运行，而是刻意对齐当前 active checksum surface：

```text
analysis_default_regression.py --path diags/diag1000025
```

也就是说，这轮 sibling 扫描优先比较的就是现有 regression contract 真正消费的 `diag1000025`，而不是把每条候选都继续盲跑到输入卡原本的 `max_step = 1000`。

若本机已有可用的 `build_full` RZ WarpX binary，这条命令会在

`runs/fieldsolver-validation/rz-jrhom-reference-scan/`

下落出各候选 run 目录，并把汇总写到：

- `runs/fieldsolver-validation/rz-reference-ledgers/rz-jrhom-reference-scan.md`
- `runs/fieldsolver-validation/rz-reference-ledgers/rz-jrhom-reference-scan.json`

基于这轮结果，下一步脚本骨架更可能收成：

- `finite + energy`
- 或 `finite + energy + spike`

## 当前结论

**这一步已经不只是把 reference-sibling 搜索推进到脚本层，还拿到了第一轮可用排序：`ll2-no-timeavg-cleaning` 是当前最像 unstable reference 的候选，而 `cl1-timeavg-cleaning` 在源码层就不成立。**

# 74. Formal convergence 第二组 family 与 slope 对照

## 目的

v0.84 已预注册 RZ/RSPHERE 独立 geometry、`64/128/256` refinement、`correction=on/off`、相邻 pairwise fit 和 axis/off-axis charge norm。此前只有一组 materialized family，正式 order 只能保持开放。本次先补齐第二组真实 2-rank producer，再用同一 reader-side norm 做两组对照。

## 执行合同

12 个 producer 为 RZ/RSPHERE × `64/128/256` × `correction=on/off`，固定使用：

- Conda 环境提供的 `mpiexec -n 2`；
- 当前 WarpX `build_full` 的 RZ/RSPHERE MPI binary；
- 与第一 family 相同的输入模板、diagnostics 和 `Full` 输出；
- `FI_PROVIDER=tcp`。

默认 MPICH provider 会选择 `utun6`，12 组都能写完 plotfile，但在 WarpX 已 finalized 后触发 `OFI poll failed`，返回码为 143；因此没有把那一轮当作 execution pass。设置 `FI_PROVIDER=tcp` 后，12/12 返回码为 0，且每组都有 `producer.log`、`warpx_used_inputs` 和 `diags/diag*`。运行合同见 `runs/stage-c-validation/formal-convergence-repeat-family-v0.92-tcp/contract.{json,md}`。

## 读回与 slope

第二组末帧由 `analyze_esirkepov_rz_langmuir_contract.py` 和 `analyze_esirkepov_radial_charge_contract.py` 重新读取。RZ 使用 `Er/Ez/axis/off-axis`，RSPHERE 使用 `Er/axis/off-axis`；每种 geometry 单独计算 `64->128`、`128->256` 的

$$
s = \log_2\left(\frac{E_h}{E_{2h}}\right)
$$

不把两种 geometry pooled。两组 family 的数值几乎重合；唯一明显差异在 RZ correction-off 的 axis/off-axis charge residual 末位浮点误差，未改变趋势解释。完整表见 `docs/formal-convergence-second-family-v0.92.md`。

## 当前边界

这一步关闭的是“第二组尚未运行”和“第二组没有 slope 读回”两个前置缺口，不是正式 order closure。原始 preregistration 没有给出可执行的 repeat-slope 数值 tolerance，且 correction-on axis charge 在两种 geometry 中仍是 boundary。因此分类保持为 `FORMAL_CONVERGENCE_SECOND_FAMILY_MATERIALIZED_ORDER_COMPARISON_OPEN`，不能把约 `1.0` 或其他 descriptive slope 写成论文意义上的正式收敛阶。

# v0.110 formal convergence repeat-slope gate

## Runtime family

本轮重新执行预注册的第二组独立 family：RZ/RSPHERE 各包含 `64/128/256` 三档 resolution、correction on/off，共 12 个真实 2-rank producer。所有 producer 在 `FI_PROVIDER=tcp` 和 WarpX 环境 `mpiexec` 下返回码为 0，并生成 `producer.log`、`warpx_used_inputs` 与 diagnostics。

## Reader-side comparison

使用与既有第一组相同的 reader-side norm，RZ 比较 `Er/Ez/axis/off-axis`，RSPHERE 比较 `Er/axis/off-axis`；两种 geometry 分开计算，不做 pooled fit。预注册只对 correction-on 的 14 个相邻 refinement comparison 执行 `1e-8` absolute slope-delta gate，14/14 通过，最大绝对差为 `2.0135e-11`。correction-off 继续作为 numerical/reader-floor negative control，最大差为 `1.736e-3`，不进入 gate。

## Classification and limits

分类：`FORMAL_CONVERGENCE_REPEAT_SLOPE_GATE_PASS_CHARGE_CLOSURE_OPEN`

这次重执行确认 repeat-slope gate 可由当前环境和当前 WarpX binary 再现，但它仍不是 formal numerical order 证明，也不关闭 correction-on axis-charge correctness。两组原始比较合同见 `runs/stage-c-validation/formal-convergence-second-family-v0.110/contract.{json,md}`，gate 合同见 `runs/stage-c-validation/formal-convergence-repeat-slope-gate-v0.110/contract.{json,md}`；执行脚本为 `scripts/run_formal_convergence_repeat_family.py`，分析脚本为 `scripts/analyze_formal_convergence_repeat_family.py`。

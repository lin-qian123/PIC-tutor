# Vay deposition AMR source guard contract

本轮没有把 AMR 输入强行运行成一个伪 physics case，而是回到当前 WarpX checkout 的初始化源码。`Source/WarpX.cpp` 在读取 current deposition 配置时明确检查：当算法为 Vay 且 `maxLevel() > 0` 时，直接以 `Vay deposition not implemented with mesh refinement` 拒绝初始化。

同时，Vay 仍有独立的 PSATD-only、RZ 和 1D source guard。于是当前正确的证据等级是：Cartesian `maxLevel=0` 的 2D/3D shape family 已有单进程与 2-rank runtime consumer；AMR 则在进入物理推进前被源码显式拒绝，不能把它写成 AMR physics PASS 或 FAIL。

可重放检查：

```bash
python scripts/audit_vay_amr_guard_contract.py \
  --warpx-root ../warpx \
  --project-root . \
  --output-json runs/stage-c-validation/vay-amr-guard/contract.json \
  --output-md runs/stage-c-validation/vay-amr-guard/contract.md
```

分类为 `SOURCE_GUARD_AMR_RUNTIME_INTENTIONALLY_REJECTED`。该 contract 关闭的是“Vay AMR 边界只停留在模糊 TODO”的源码证据缺口，不声称 AMR runtime 已支持，也不修改 `../warpx`。

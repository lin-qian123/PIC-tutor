# Comoving velocity selector and sign sibling contract

审计日期：2026-07-13

## 运行结果

对固定的 2D hybrid comoving PSATD 输入，只改变 `v_comoving` 选择路径后，已有 scan ledger 得到：

- 默认 selector 与显式 `v_comoving=-beta` 的 electric energy 相对差为约 `1.31e-14`，spike ratio 相对差为约 `2.13e-14`；
- no-comoving sibling 的 spike ratio 为 `1.1119614945212388`，超过当前 stable-derived ceiling `1.1114823702056489`；
- 反号 `v_comoving=+beta` sibling 的 spike ratio 为 `1.1794568812230803`，约为 stable 的 `1.0622` 倍；
- half-beta sibling 也能运行，但其 spike ratio 只约为 stable 的 `1.0026` 倍。

这条证据关闭了两个更窄的问题：默认 selector 的数值路径确实等价于显式 `-beta`，而 comoving 速度符号对 spike surface 有明显敏感性。它仍没有提供可靠的 unstable-energy oracle，因此不能把 comoving first-stage patch 升级为 energy gate，也不能把该 sibling scan 写成 upstream CI 结果。

## 可重放命令

```bash
python scripts/analyze_comoving_velocity_scan_contract.py \
  --ledger-json runs/fieldsolver-validation/comoving-reference-ledgers/comoving-velocity-scan.json \
  --output-dir runs/fieldsolver-validation/comoving-reference-ledgers/comoving-velocity-scan-contract
```

原始 sibling plotfile 留在 `runs/fieldsolver-validation/comoving-velocity-scan/`，不进入公共 release。

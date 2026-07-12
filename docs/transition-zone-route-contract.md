# Transition-zone route-count contract

`docs/transition-zone-route-contract-example.json` is a synthetic fixture for the reduced ledger proposed in `notes/code-reading/particles/50-transition-zone-route-count-implementation-packet.md`.

Validate it with:

```bash
python scripts/validate_transition_zone_route_contract.py \
  --input docs/transition-zone-route-contract-example.json
```

The validator checks:

- fine/buffer gather and deposit route counts close to the pre-partition particle count;
- fine plus buffer weights close to the deposited weight;
- all `rho/J`, coarsened-fine, merged-coarse, owner-mask and post-sync ledger fields are present and finite;
- route partition and source merge gates are explicit booleans.

The expected result is `DESIGN_SCHEMA_VALIDATED`. This is an analysis-layer contract only. The current WarpX checkout still lacks the runtime hook and does not emit `nfine_*`, `current_buf/rho_buf` or owner-mask ledger rows, so this fixture must not be cited as a runtime AMR validation.

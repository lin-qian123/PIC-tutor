# Structured parameter runtime coverage follow-up

## Result

The runtime inventory now covers four executable rows:

- species runtime attributes: `particle_orig_z` and `particle_regionofinterest` appear in the 1D Full plotfile;
- particle-field reductions: 15 species fields and an openPMD HDF5 output are present;
- scalar `amr.ref_ratio`: the existing MR case records `amr.ref_ratio = 4`;
- vector `amr.ref_ratio_vect`: a 2D `max_step=0` smoke records `amr.ref_ratio_vect = 2 1` and materializes both level 0 and level 1 plotfile data.

The vector-ratio smoke is an initialization and level-materialization check. It does not establish anisotropic refinement accuracy or prove every AMReX consumer uses the full vector consistently.

## Remaining boundaries

The DSMC charge-exchange input still exercises the dynamic key only at input level in this checkout. A short run was attempted, but WarpX stopped before initialization because the local machine does not contain `warpx-data/MCC_cross_sections/He/charge_exchange.dat`. This is recorded in `runs/stage-c-validation/parameter-map-runtime/dsmc/run.log`; the missing data dependency is not treated as a WarpX parser failure or a runtime PASS.

ADIOS2 arbitrary suffixes remain source-only. `FlushFormatOpenPMD.cpp` proves prefix stripping and map forwarding, but no local runtime case currently selects an ADIOS2 backend with an arbitrary operator or engine parameter.

## Reproduction

```text
python scripts/audit_parameter_map_runtime_coverage.py
```

The generated contract is `runs/stage-c-validation/parameter-map-runtime-coverage/contract.{json,md}`.

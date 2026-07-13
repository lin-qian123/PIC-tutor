# Structured parameter runtime coverage follow-up

## Result

The runtime inventory now covers five executable contract rows:

- species runtime attributes: `particle_orig_z` and `particle_regionofinterest` appear in the 1D Full plotfile;
- particle-field reductions: 15 species fields and an openPMD HDF5 output are present;
- scalar `amr.ref_ratio`: the existing MR case records `amr.ref_ratio = 4`;
- vector `amr.ref_ratio_vect`: a 2D `max_step=0` smoke records `amr.ref_ratio_vect = 2 1` and materializes both level 0 and level 1 plotfile data.
- ADIOS2 engine suffix: a 3D BP5 `max_step=0` smoke records `openpmd.adios2_engine.parameters.NumAggregators = 1` and produces `openpmd_000000.bp5`.
- ADIOS2 operator suffix: a second BP5 smoke records the documented `blosc/zstd` operator parameters (`clevel`, `doshuffle`, `threshold`) and produces a second BP5 series.

The vector-ratio smoke is an initialization and level-materialization check. It does not establish anisotropic refinement accuracy or prove every AMReX consumer uses the full vector consistently.

## Remaining boundaries

The DSMC charge-exchange input still exercises the dynamic key only at input level in this checkout. A short run was attempted, but WarpX stopped before initialization because the local machine does not contain `warpx-data/MCC_cross_sections/He/charge_exchange.dat`. This is recorded in `runs/stage-c-validation/parameter-map-runtime/dsmc/run.log`; the missing data dependency is not treated as a WarpX parser failure or a runtime PASS.

ADIOS2 engine and operator suffixes now have runtime smoke coverage. The cases select BP5, forward `NumAggregators = 1` or the documented `blosc/zstd` parameters, write BP5 series, and are reopened with openPMD-api at iteration `0`. This does not establish multi-rank engine semantics or compression numerical fidelity.

## Reproduction

```text
python scripts/audit_parameter_map_runtime_coverage.py
```

The generated contract is `runs/stage-c-validation/parameter-map-runtime-coverage/contract.{json,md}`.

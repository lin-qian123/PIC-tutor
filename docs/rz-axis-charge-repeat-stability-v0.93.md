# Reader-side axis-charge repeat stability

- classification: `REPEAT_STABLE_AXIS_CHARGE_BOUNDARY_NOT_KERNEL_ROOT_CAUSE`
- repeat tolerance: `1.0e-10`

| geometry | correction | level | first axis | second axis | first off-axis | second off-axis | relative repeat diff | axis dominates |
|---|---|---:|---:|---:|---:|---:|---:|:---:|
| `RZ` | `on` | `64` | `3.592974e-03` | `3.592974e-03` | `4.292744e-04` | `4.292744e-04` | `7.891166e-12` | `PASS` |
| `RZ` | `on` | `128` | `1.519632e-03` | `1.519632e-03` | `4.691938e-04` | `4.691938e-04` | `0.000000e+00` | `PASS` |
| `RZ` | `on` | `256` | `7.553707e-04` | `7.553707e-04` | `1.720181e-04` | `1.720181e-04` | `0.000000e+00` | `PASS` |
| `RZ` | `off` | `64` | `5.512607e-12` | `5.518742e-12` | `1.720244e-12` | `1.718213e-12` | `1.111612e-03` | `PASS` |
| `RZ` | `off` | `128` | `9.353410e-12` | `9.350874e-12` | `3.664231e-12` | `3.664231e-12` | `2.711864e-04` | `PASS` |
| `RZ` | `off` | `256` | `1.639115e-11` | `1.639133e-11` | `8.458668e-12` | `8.458668e-12` | `1.108174e-05` | `PASS` |
| `RSPHERE` | `on` | `64` | `4.165922e-02` | `4.165922e-02` | `2.531403e-03` | `2.531403e-03` | `0.000000e+00` | `PASS` |
| `RSPHERE` | `on` | `128` | `1.390429e-02` | `1.390429e-02` | `9.503782e-04` | `9.503782e-04` | `0.000000e+00` | `PASS` |
| `RSPHERE` | `on` | `256` | `4.142253e-03` | `4.142253e-03` | `2.770351e-04` | `2.770351e-04` | `0.000000e+00` | `PASS` |
| `RSPHERE` | `off` | `64` | `2.419910e-11` | `2.419910e-11` | `1.414011e-11` | `1.414011e-11` | `0.000000e+00` | `PASS` |
| `RSPHERE` | `off` | `128` | `9.842866e-11` | `9.842866e-11` | `3.881674e-11` | `3.881674e-11` | `0.000000e+00` | `PASS` |
| `RSPHERE` | `off` | `256` | `7.460938e-11` | `7.460938e-11` | `1.712409e-11` | `1.712409e-11` | `0.000000e+00` | `PASS` |

The correction-on axis residual is reproducible across both materialized families and remains larger than the off-axis residual at every declared level. Correction-off values are reported as a negative control; their relative differences are not gated because the absolute residual is near the reader/numerical floor. This strengthens the correction-on boundary as a stable reader-side observation; it does not identify the kernel root cause, prove current closure, or close formal order.

- `all_twelve_axis_pairs_present`: `PASS`
- `all_repeat_values_finite`: `PASS`
- `all_correction_on_axis_repeats_within_tolerance`: `PASS`
- `correction_on_axis_dominates_both_families`: `PASS`

# Formal convergence repeat-slope comparison gate

- classification: `FORMAL_CONVERGENCE_REPEAT_SLOPE_GATE_PASS_CHARGE_CLOSURE_OPEN`
- status: `PASS`
- comparisons: `14`
- gated corrections: `on`
- absolute slope-delta tolerance: `1.0e-08`
- maximum absolute slope delta: `2.014e-11`
- correction-off negative-control maximum delta: `1.736e-03`

| geometry | correction | observable | interval | abs delta | status |
|---|---|---|---:|---:|:---:|
| `RZ` | `on` | `er_error` | `1` | `2.243e-14` | `PASS` |
| `RZ` | `on` | `er_error` | `2` | `1.776e-15` | `PASS` |
| `RZ` | `on` | `ez_error` | `1` | `8.438e-15` | `PASS` |
| `RZ` | `on` | `ez_error` | `2` | `4.508e-14` | `PASS` |
| `RZ` | `on` | `axis_residual` | `1` | `9.555e-13` | `PASS` |
| `RZ` | `on` | `axis_residual` | `2` | `0.000e+00` | `PASS` |
| `RZ` | `on` | `off_axis_residual` | `1` | `7.751e-12` | `PASS` |
| `RZ` | `on` | `off_axis_residual` | `2` | `2.014e-11` | `PASS` |
| `RSPHERE` | `on` | `relative_er_error` | `1` | `0.000e+00` | `PASS` |
| `RSPHERE` | `on` | `relative_er_error` | `2` | `0.000e+00` | `PASS` |
| `RSPHERE` | `on` | `axis_residual` | `1` | `0.000e+00` | `PASS` |
| `RSPHERE` | `on` | `axis_residual` | `2` | `0.000e+00` | `PASS` |
| `RSPHERE` | `on` | `off_axis_residual` | `1` | `0.000e+00` | `PASS` |
| `RSPHERE` | `on` | `off_axis_residual` | `2` | `0.000e+00` | `PASS` |

The two materialized families pass the preregistered slope-repeat gate. This is an order-comparison gate only; it does not establish a formal numerical order and does not close the correction-on axis-charge boundary.

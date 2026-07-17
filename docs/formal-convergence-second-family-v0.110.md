# Formal convergence second-family slope comparison

- classification: `FORMAL_CONVERGENCE_SECOND_FAMILY_MATERIALIZED_ORDER_COMPARISON_OPEN`
- runtime environment: `{"FI_PROVIDER": "tcp"}`

| geometry | correction | observable | first family slopes | second family slopes |
|---|---|---|---:|---:|
| `RZ` | `on` | `er_error` | `-1.379703, 1.178341` | `-1.379703, 1.178341` |
| `RZ` | `on` | `ez_error` | `-1.887437, 1.233664` | `-1.887437, 1.233664` |
| `RZ` | `on` | `axis_residual` | `1.241457, 1.008465` | `1.241457, 1.008465` |
| `RZ` | `on` | `off_axis_residual` | `-0.128284, 1.447624` | `-0.128284, 1.447624` |
| `RZ` | `off` | `er_error` | `0.607472, 1.194466` | `0.607472, 1.194466` |
| `RZ` | `off` | `ez_error` | `-1.949575, 1.286227` | `-1.949575, 1.286227` |
| `RZ` | `off` | `axis_residual` | `-0.762758, -0.809352` | `-0.762920, -0.807617` |
| `RZ` | `off` | `off_axis_residual` | `-1.090897, -1.206920` | `-1.090897, -1.206920` |
| `RSPHERE` | `on` | `relative_er_error` | `-2.648622, 1.846731` | `-2.648622, 1.846731` |
| `RSPHERE` | `on` | `axis_residual` | `1.583105, 1.747043` | `1.583105, 1.747043` |
| `RSPHERE` | `on` | `off_axis_residual` | `1.413363, 1.778433` | `1.413363, 1.778433` |
| `RSPHERE` | `off` | `relative_er_error` | `0.406791, -0.102287` | `0.406791, -0.102287` |
| `RSPHERE` | `off` | `axis_residual` | `-2.024125, 0.399721` | `-2.024125, 0.399721` |
| `RSPHERE` | `off` | `off_axis_residual` | `-1.456885, 1.180652` | `-1.456885, 1.180652` |

The second independent family is materialized and its pairwise slopes are reported beside the first family. Formal closure remains open because the preregistration requires repeat-slope comparison under a declared tolerance and an independent charge interpretation; correction-on axis charge remains a boundary.

- `two_independent_families_present`: `PASS`
- `all_declared_levels_present`: `PASS`
- `all_observables_finite`: `PASS`
- `second_family_execution_pass`: `PASS`
- `all_pairwise_slopes_computed`: `PASS`
- `separate_geometry_reporting`: `PASS`
- `formal_order_closure`: `BOUNDARY`

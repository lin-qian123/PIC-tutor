# Chapter 7 Load-Balance Validation Card

Classification: `SOURCE_GROUNDED_LOAD_BALANCE_VALIDATION_READER_CARD`.

Result: `PASS`.

## Source Routes

- `Docs/source/usage/{parameters.rst,workflows/plot_distribution_mapping.rst}`
- `Examples/Tests/reduced_diags/{CMakeLists.txt,inputs_base_3d,inputs_test_3d_reduced_diags_load_balance_costs_{heuristic,timers},analysis_reduced_diags_load_balance_costs.py}`
- `Source/Parallelization/WarpXRegrid.cpp`

## Checks

- `reader_card_present`: `PASS`
- `official_load_balance_producer`: `PASS`
- `efficiency_consumer`: `PASS`
- `migration_scope`: `PASS`

## Scope

- No WarpX build or runtime execution is performed by this audit.
- The card separates cost-distribution efficiency from state migration and physical validation.
- It does not establish AMR topology regridding, transition-zone route counts, physics accuracy, or wall-clock speedup for arbitrary inputs.

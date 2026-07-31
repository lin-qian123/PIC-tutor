# Chapter 5 Deposition Validation Ladder

Classification: `SOURCE_GROUNDED_DEPOSITION_VALIDATION_LADDER_READER_CARD`.

Result: PASS.

## Source Routes

- `Source/Particles/WarpXParticleContainer.cpp`
- `Source/Particles/Deposition/CurrentDeposition.H`
- `Examples/Tests/vay_deposition/{inputs_test_2d_vay_deposition,CMakeLists.txt,analysis.py}`
- `Examples/Tests/langmuir/{inputs_test_3d_langmuir_multi,inputs_base_3d,CMakeLists.txt,analysis_3d.py,analysis_utils.py}`

## Checks

- `reader_card_present`: `PASS`
- `vay_source_contract`: `PASS`
- `esirkepov_field_and_source_contract`: `PASS`
- `dispatch_and_guard_boundaries`: `PASS`

## Scope

- No WarpX build or runtime execution is performed by this audit.
- The card separates dispatch preconditions, source residuals, analytic fields, and checksum regression.
- It does not establish AMR, RZ, implicit Villasenor, or general geometry-by-shape coverage.

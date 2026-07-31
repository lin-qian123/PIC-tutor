# Chapter 3 AMR Subcycling Validation Card

Classification: `SOURCE_GROUNDED_AMR_SUBCYCLING_VALIDATION_READER_CARD`.

Result: `PASS`.

## Source Routes

- `Docs/source/developers/repo_organization.rst`
- `Examples/Tests/subcycling/{CMakeLists.txt,inputs_test_2d_subcycling_mr}`
- `Examples/analysis_default_regression.py`
- `Source/{Evolve/WarpXEvolve.cpp,Fields.H}`

## Checks

- `reader_card_present`: `PASS`
- `official_test_contract`: `PASS`
- `two_level_source_lifecycle`: `PASS`
- `checksum_scope`: `PASS`

## Scope

- No WarpX build or runtime execution is performed by this audit.
- The official test's checksum contract is kept distinct from source-lifecycle or physical validation.
- The card does not establish transition-zone route counts, conservation, or AMR physical accuracy.

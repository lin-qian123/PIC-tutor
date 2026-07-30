# Chapter 8 Restart Reader Card

Classification: `SOURCE_GROUNDED_RESTART_READER_CONTRACT`.

Result: PASS.

## Source Routes

- `Examples/Physics_applications/uniform_plasma/CMakeLists.txt`
- `Examples/Physics_applications/uniform_plasma/inputs_base_3d`
- `Examples/Physics_applications/uniform_plasma/inputs_test_3d_uniform_plasma_restart`
- `Examples/analysis_default_restart.py`

## Checks

- `reader_card_present`: PASS
- `restart_ctest_contract`: PASS
- `checkpoint_input_contract`: PASS
- `consumer_contract`: PASS

## Scope

- No WarpX run is performed by this audit.
- The contract does not establish cross-layout equivalence or thermal-plasma physics closure.

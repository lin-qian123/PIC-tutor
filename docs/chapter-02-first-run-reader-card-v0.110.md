# Chapter 2 First-Run Reader Card

Classification: `SOURCE_GROUNDED_FIRST_RUN_READER_CONTRACT`.

Result: PASS.

## Source Routes

- `Docs/source/install/cmake.rst`
- `Docs/source/usage/how_to_run.rst`
- `CMakeLists.txt`
- `cmake/WarpXFunctions.cmake`
- `Examples/Tests/langmuir/CMakeLists.txt`
- `Examples/Tests/langmuir/inputs_test_1d_langmuir_multi`
- `Examples/Tests/langmuir/analysis_1d.py`

## Checks

- `reader_route`: PASS
- `build_contract`: PASS
- `ctest_subtest_contract`: PASS
- `run_contract`: PASS
- `langmuir_ctest_contract`: PASS
- `override_and_consumer_contract`: PASS

## Scope

- No WarpX build or runtime execution is performed by this audit.
- CTest registration does not establish physics validity beyond the registered input and consumer contract.

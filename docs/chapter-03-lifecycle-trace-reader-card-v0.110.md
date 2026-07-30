# Chapter 3 Lifecycle Trace Reader Card

Classification: `SOURCE_GROUNDED_LIFECYCLE_TRACE_READER_CONTRACT`.

Result: PASS.

## Source Routes

- `Source/main.cpp`
- `Source/WarpX.cpp`
- `Source/Initialization/WarpXInitData.cpp`
- `Source/Evolve/WarpXEvolve.cpp`
- `Examples/Tests/langmuir/inputs_test_1d_langmuir_multi`
- `Examples/Tests/langmuir/CMakeLists.txt`
- `Examples/Tests/langmuir/analysis_1d.py`

## Checks

- `reader_card_present`: PASS
- `main_and_parameter_contract`: PASS
- `initialization_evidence_contract`: PASS
- `evolve_and_diagnostic_contract`: PASS
- `consumer_contract`: PASS

## Scope

- No WarpX build or runtime execution is performed by this audit.
- The lifecycle trace distinguishes parameter ingestion, initialization evidence, diagnostic production, and the registered consumer.
- It does not establish physics validity outside the registered Langmuir input, two-rank layout, and analysis contract.

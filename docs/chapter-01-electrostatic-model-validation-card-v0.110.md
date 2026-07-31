# Chapter 1 Electrostatic Model Validation Card

Classification: `SOURCE_GROUNDED_ELECTROSTATIC_MODEL_SELECTION_READER_CARD`.

Result: `PASS`.

## Source Routes

- `Docs/source/{usage/parameters.rst,theory/models_algorithms/electrostatic_pic.rst}`
- `Examples/Tests/electrostatic_sphere_eb/{CMakeLists.txt,inputs_test_3d_electrostatic_sphere_eb,analysis.py}`
- `Source/{Initialization/WarpXInitData.cpp,Evolve/WarpXEvolve.cpp}`

## Checks

- `reader_card_present`: `PASS`
- `official_model_contract`: `PASS`
- `official_sphere_producer`: `PASS`
- `geometry_and_charge_consumers`: `PASS`
- `execution_and_combination_boundary`: `PASS`

## Scope

- No WarpX build or runtime execution is performed by this audit.
- The card separates model selection, a fixed-potential EB producer, charge and geometry consumers, and checksum regression.
- It does not establish electromagnetic propagation, laser physics, arbitrary Poisson accuracy, arbitrary EB geometry, particle kinetics, or electrostatic plus subcycling support.

# Chapter 1 Thermal-Plasma Energy Validation Card

Classification: `SOURCE_GROUNDED_THERMAL_PLASMA_ENERGY_AND_NOISE_READER_CARD`.

Result: `PASS`.

## Source Routes

- `Docs/source/{usage/parameters.rst,theory/models_algorithms/explicit_em_pic.rst,theory/amr.rst}`
- `Examples/Tests/energy_conserving_thermal_plasma/{CMakeLists.txt,inputs_test_1d_energy_conserving_thermal_plasma,inputs_test_2d_energy_conserving_thermal_plasma,analysis.py}`
- `Source/Diagnostics/ReducedDiags/{ParticleEnergy.H,FieldEnergy.H}`

## Checks

- `reader_card_present`: `PASS`
- `official_producers`: `PASS`
- `energy_consumer`: `PASS`
- `gather_and_mesh_boundary`: `PASS`

## Scope

- No WarpX build or runtime execution is performed by this audit.
- The card separates the fixed periodic thermal-plasma producer, the sampled total energy consumer, and independent noise or thermal observables.
- It does not establish thermal equilibrium, a noise spectrum, strict conservation, arbitrary gathering behavior, AMR-interface behavior, collisions, laser propagation, or a threshold for a modified producer.

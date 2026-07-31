# Chapter 1 Thermal-Plasma Debye-Resolution Card

Classification: `SOURCE_GROUNDED_THERMAL_PLASMA_DEBYE_RESOLUTION_READER_CARD`.

Result: `PASS`.

## Derived Scales

- `lambda_De_over_de0`: `0.0139891071`
- `dx_over_de0`: `1.25`
- `lambda_De_over_dx`: `0.0111912857`
- `omega_pe_dt`: `0.2`
- `v_te_dt_over_dx`: `0.00223825714`

## Source Routes

- `Examples/Tests/energy_conserving_thermal_plasma/{inputs_test_1d_energy_conserving_thermal_plasma,inputs_test_2d_energy_conserving_thermal_plasma,analysis.py}`
- `Chapter 1 Debye definitions and thermal-plasma energy-validation card`

## Checks

- `reader_card_present`: `PASS`
- `official_1d_input_scales`: `PASS`
- `official_2d_input_scales`: `PASS`
- `energy_consumer_does_not_measure_resolution`: `PASS`

## Scope

- No WarpX build or runtime execution is performed by this audit.
- The derived scales use the input's electron thermal-speed convention, d_e0=c/omega_pe, L=10 d_e0, and N_x=8.
- The card does not impose a universal Debye-resolution threshold or establish Landau damping, shielding, a fluctuation spectrum, or convergence for this producer.

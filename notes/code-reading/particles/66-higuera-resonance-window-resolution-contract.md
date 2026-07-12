# Higuera-Cary resonance-window resolution contract

The dense 14-species family covers the paper's resonance-sensitive region with `p_y=0.2,0.4,...,2.8`. The localized screen uses `p_y=1.5..1.9`, i.e. the `p_y=1.6` and `1.8` particles, and compares the maximum relative drift of the invariant `I_y` against the rest of the family.

The 32^3 family gives window maxima of `1.011e-3` for Boris, `6.521e-2` for Vay, and `1.074e-3` for Higuera-Cary. A dedicated 64^3, two-particle resolution control reproduces the same window values: Boris `9.091e-4/1.011e-3`, Vay `6.521e-2/6.118e-2`, and Higuera-Cary `9.103e-4/1.074e-3` for `p_y=1.6/1.8`.

`scripts/compare_higuera_resonance_window_resolution.py` passes the screening contract: fine-grid Vay drift exceeds `2e-2`, both controls stay below `5e-3`, and Vay is more than five times each control. This is strong evidence of localized Vay invariant degradation near the paper's resonance-sensitive region. It is not a proof of the paper's two-fold island or trajectory-crossing topology, which still requires a validated multi-orbit section-point topology consumer.

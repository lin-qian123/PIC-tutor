# Sampled Poincare topology classifier boundary

`scripts/classify_higuera_poincare_topology.py` consumes the section contract JSON and computes candidate polygon areas, self-intersections, and pairwise segment intersections for Boris, Vay, and Higuera-Cary. It deliberately separates “classifier executed” from “topology gate passed”.

The first runtime data contained only 8 positive-`p_x` section points per orbit. The classifier correctly returned `status=INSUFFICIENT_SAMPLING` and `topology_gate_passed=false` for all three pushers. A longer 32³ control now provides 18 or 19 points per orbit for all three pushers, so the sampling threshold is met and the classifier returns `status=REVIEW_REQUIRED`. The apparent self-intersection counts of the time-ordered polylines are still retained as candidates only: the three pushers produce the same candidate signature, so these counts are not yet physical resonance-island or trajectory-crossing evidence.

The present minimum is 16 section points per orbit, and the long control meets it with 2201 frames. A future topology claim still requires a validated section-point ordering and comparison against a denser reference orbit before the physical gate can be promoted into the book. The long-run reports are in `runs/stage-c-validation/higuera_poincare_long_comparison/`.

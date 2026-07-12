# Sampled Poincare topology classifier boundary

`scripts/classify_higuera_poincare_topology.py` consumes the section contract JSON and computes candidate polygon areas, self-intersections, and pairwise segment intersections for Boris, Vay, and Higuera-Cary. It deliberately separates “classifier executed” from “topology gate passed”.

The current runtime data contain only 8 positive-`p_x` section points per orbit. The classifier therefore returns `status=INSUFFICIENT_SAMPLING` and `topology_gate_passed=false` for all three pushers. The apparent self-intersection counts of the coarse p05/p10 polylines are retained as candidates only; they are not physical resonance-island or trajectory-crossing evidence. Pairwise intersection counts are withheld until the sampling threshold is met.

The present minimum is 16 section points per orbit. A future runtime rerun must exceed that threshold and compare the resulting candidate topology against a denser reference orbit before a topology claim can be promoted into the book.

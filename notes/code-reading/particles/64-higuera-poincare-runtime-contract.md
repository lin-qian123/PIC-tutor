# Higuera-Cary Poincare runtime contract

## Scope

This case-local contract exercises the numerical construction described in Higuera-Cary 2017 Section VI: `E_x=-a x`, `B_x=b y`, `a=1`, `b=2`, normalized timestep `dt=0.1`, and the section `x=0` with positive `p_x`.

The runtime uses WarpX electrons with `charge=-q_e` and reverses the external `E_x` and `B_x` signs so that the physical `qE` and `qB` products match the paper's `q=+1` construction. WarpX plotfiles store mechanical momentum in SI units, so the analyzer converts `particle_momentum/(m_e*c)`. The paper's `p_z` is canonical; with `A_z=0.5*b*y^2`, `P_z-A_z` is the mechanical `p_z` written by WarpX. Therefore the runtime ledger evaluates `H=sqrt(1+px^2+py^2+pz_mechanical^2)+0.5*x^2` and `I_y=py^2+pz_mechanical^2`.

The dedicated input uses a `64^3` mesh, `Omega0=1e9 1/s`, `L0=c/Omega0`, 5 single-particle initial conditions (`p_y=0.5,1.0,1.7,2.2,2.7`), z-periodic boundaries for the ignorable coordinate, and 1001 Full plotfiles per pusher. The input is intentionally case-local under `runs/` and is not part of the public release allowlist.

## Result

The analyzer `scripts/analyze_higuera_poincare_contract.py` passes its structural contract for Boris, Vay, and Higuera-Cary. Each pusher retains all five species and yields 8 positive-`p_x` section crossings per species. Across the 15 ledgers, the largest observed relative drifts are:

| quantity | maximum relative drift |
|---|---:|
| `H` | `1.532e-3` |
| `I_y` | `8.206e-3` |

The detailed values and section points are stored in `runs/stage-c-validation/higuera_poincare_comparison/contract.{json,md}`. This establishes a reproducible section/invariant consumer and provides runtime evidence that the three pusher paths remain close on this setup. It does not yet automate the paper's nested-surface, trajectory-crossing, or resonance-island topology classifier, so no full Fig. 2 topology reproduction is claimed.

## Reproduction boundary

The WarpX binary writes all 1001 plotfiles, then encounters the known local MPI/OFI finalize-tail failure on process shutdown. The data contract is validated from the complete plotfile set; a clean process exit is not claimed.

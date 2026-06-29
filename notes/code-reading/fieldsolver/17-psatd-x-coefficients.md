# PSATD X1-X4 coefficient atlas

Date: 2026-06-29

WarpX baseline: `../warpx` on `pkuHEDPbranch`, commit `8c488b1a9`.

## Scope

This note maps the Cartesian standard/Galilean PSATD coefficients in:

`../warpx/Source/FieldSolver/SpectralSolver/SpectralAlgorithms/PsatdAlgorithmGalilean.cpp`

It does not cover JRhom `Y*` coefficients, RZ `PsatdAlgorithmRZ/GalileanRZ`, comoving coefficients, or PML `C1-C25`. Those are separate algorithms or geometry-specific branches.

## Shared quantities

`InitializeSpectralCoefficients()` computes:

| symbol | source expression | role |
|---|---|---|
| `knorm_s` | `sqrt(kx_s^2 + ky_s^2 + kz_s^2)` | modified spectral wavenumber norm |
| `om_s` | `c * knorm_s` | electromagnetic angular frequency |
| `w_c` | `kx_c*vg_x + ky_c*vg_y + kz_c*vg_z` | Galilean convective frequency, using centered modified k |
| `theta_c` | `exp(i*w_c*dt/2)` | half-step Galilean phase |
| `theta2_c` | `exp(i*w_c*dt)` | full-step Galilean phase, later stored as `T2` |
| `C` | `cos(om_s*dt)` | homogeneous electromagnetic oscillator coefficient |
| `S_ck` | `sin(om_s*dt)/om_s`, or `dt` at zero mode | time-integrated sine factor |
| `tmp` | `(1-C)/(epsilon0*om_s^2)`, or `dt^2/(2 epsilon0)` at zero mode | regularized helper for charge-source coefficients |

The source explicitly separates `w_c=0` and `om_s=0` limits. This is not just style: the generic Galilean expressions contain denominators such as `om_s^2-w_c^2` and `theta_c_star-theta_c`.

## X1-X4 formulas

| coefficient | source branch | expression | appears in |
|---|---|---|---|
| `X1` | generic Galilean | `(1 - theta2_c*C + i*w_c*theta2_c*S_ck)/(epsilon0*(om_s^2-w_c^2))` | magnetic update, multiplying `i*(k x J)` |
| `X1` | `om_s=0 && w_c=0` | `dt^2/(2 epsilon0)` | zero-mode limit |
| `X2` | `w_c != 0` | `c^2*(theta_c_star*X1 - theta_c*tmp)/(theta_c_star-theta_c)` | electric update, multiplying `rho_new` |
| `X2` | `w_c=0, om_s != 0` | `c^2*(dt-S_ck)/(epsilon0*dt*om_s^2)` | standard PSATD limit |
| `X2` | `w_c=0, om_s=0` | `c^2*dt^2/(6 epsilon0)` | zero-mode limit |
| `X3` | `w_c != 0` | `c^2*(theta_c_star*X1 - theta_c_star*tmp)/(theta_c_star-theta_c)` | electric update, multiplying `rho_old` through `T2*X3` |
| `X3` | `w_c=0, om_s != 0` | `c^2*(dt*C-S_ck)/(epsilon0*dt*om_s^2)` | standard PSATD limit |
| `X3` | `w_c=0, om_s=0` | `-c^2*dt^2/(3 epsilon0)` | zero-mode limit |
| `X4` | all modes | `i*w_c*X1 - theta2_c*S_ck/epsilon0` | electric update, multiplying `J` |

For standard PSATD, `v_galilean=0`, so `w_c=0`, `theta2_c=T2=1`, and `X4=-S_ck/epsilon0`.

## Placement in field update

The electric update uses `X4` and the charge-source combination:

```cpp
E_new = T2*C*E_old + i*c^2*T2*S_ck*(k x B_old)
        + X4*J - i*(X2*rho_new - T2*X3*rho_old)*k;
```

The magnetic update uses `X1`:

```cpp
B_new = T2*C*B_old - i*T2*S_ck*(k x E_old)
        + i*X1*(k x J);
```

Thus:

- `X1` is the current contribution to Faraday's law through the magnetic update.
- `X4` is the direct current contribution to Ampere's law through the electric update.
- `X2` and `X3` are longitudinal charge terms that keep the electric update consistent with `rho_new/rho_old`.
- `T2` shifts the old-time quantities in Galilean coordinates.

## Branch boundaries

| branch | source evidence | writing boundary |
|---|---|---|
| standard Cartesian PSATD | `v_galilean=0`, so `w_c=0`, `T2=1` | use the `w_c=0` limit formulas |
| Galilean Cartesian PSATD | `w_c=k_c dot v_gal` from centered modified k | keep `T2`, complex `X1-X4`, and Galilean continuity phase together |
| time averaging | separate `Psi*` and `Y*` arrays | do not describe averaged fields with only `X1-X4` |
| JRhom | separate `PsatdAlgorithmJRhom*` classes | do not reuse these `X1-X4` as JRhom source-integration coefficients |
| RZ / Galilean RZ | separate RZ algorithm classes | RZ coefficient names have different geometry semantics |
| PML PSATD | `PsatdAlgorithmPml.cpp` | use the PML `C1-C25` atlas, not this note |


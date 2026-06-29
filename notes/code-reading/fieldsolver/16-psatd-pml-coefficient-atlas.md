# PSATD PML coefficient atlas

Date: 2026-06-29

WarpX baseline: `../warpx` on `pkuHEDPbranch`, commit `8c488b1a9`.

## Scope

This note maps the source-level coefficient groups in:

`../warpx/Source/FieldSolver/SpectralSolver/SpectralAlgorithms/PsatdAlgorithmPml.cpp`

It is not a replacement for the LeeCPC2015 paper walkthrough. It is the implementation-side atlas that the paper formulas should later be checked against.

## Shared spectral quantities

Inside `pushSpectralFields()`, each nonzero spectral mode uses:

| symbol | source expression | role |
|---|---|---|
| `kx2, ky2, kz2` | `kx*kx`, `ky*ky`, `kz*kz` | squared modified wavenumber components |
| `knorm` | `sqrt(kx2 + ky2 + kz2)` | magnitude of modified spectral wavevector |
| `C` | `C_arr(i,j,k)` | `cos(c*knorm*dt)`, initialized in `InitializeSpectralCoefficients()` |
| `S_ck` | `S_ck_arr(i,j,k)` | `sin(c*knorm*dt)/(c*knorm)` |
| `inv_k2` | `1/(knorm*knorm)` | inverse squared wavenumber |
| `T2` | `T2_arr(i,j,k)` or `1` | Galilean phase factor, `exp(i*w_c*dt)` when `m_is_galilean` |

`C`, `S_ck`, and `T2` are spectral propagator factors. They are not the PML `sigma` profile. PML geometry and damping factors are created in `PML.cpp` / `SigmaBox`.

## `C1-C9`: projection and split-component geometry

| coefficient | source expression | interpretation |
|---|---|---|
| `C1` | `(kx2*C + ky2 + kz2) * inv_k2` | x-weighted diagonal projector |
| `C2` | `(kx2 + ky2*C + kz2) * inv_k2` | y-weighted diagonal projector |
| `C3` | `(kx2 + ky2 + kz2*C) * inv_k2` | z-weighted diagonal projector |
| `C4` | `kx2*(C-1)*inv_k2` | x same-axis correction |
| `C5` | `ky2*(C-1)*inv_k2` | y same-axis correction |
| `C6` | `kz2*(C-1)*inv_k2` | z same-axis correction |
| `C7` | `ky*kz*(1-C)*inv_k2` | yz cross projector |
| `C8` | `kx*kz*(1-C)*inv_k2` | xz cross projector |
| `C9` | `kx*ky*(1-C)*inv_k2` | xy cross projector |

These coefficients appear in both branches. In the no-cleaning branch they update split `E/B` components. In the cleaning branch they also update `F/G` split components.

## `C10-C22`: no-cleaning electric/magnetic cross coupling

This group exists only when:

```cpp
!dive_cleaning && !divb_cleaning
```

| coefficient | source expression | direct use pattern |
|---|---|---|
| `C10` | `i*c2*kx*ky*kz*(dt-S_ck)*inv_k2` | symmetric 3-direction cross term in multiple `E/B` updates |
| `C11` | `i*c2*ky2*kz*(dt-S_ck)*inv_k2` | couples `By` into `Exy`, and `Ey` into `Bxy` through `/c2` |
| `C12` | `i*c2*kz2*ky*(dt-S_ck)*inv_k2` | couples `Bz` into `Exz`, and `Ez` into `Bxz` through `/c2` |
| `C13` | `i*c2*kz2*kx*(dt-S_ck)*inv_k2` | couples `Bz` into `Eyz`, and `Ez` into `Byz` through `/c2` |
| `C14` | `i*c2*kx2*kz*(dt-S_ck)*inv_k2` | couples `Bx` into `Eyx`, and `Ex` into `Byx` through `/c2` |
| `C15` | `i*c2*kx2*ky*(dt-S_ck)*inv_k2` | couples `Bx` into `Ezx`, and `Ex` into `Bzx` through `/c2` |
| `C16` | `i*c2*ky2*kx*(dt-S_ck)*inv_k2` | couples `By` into `Ezy`, and `Ey` into `Bzy` through `/c2` |
| `C17` | `i*c2*kx*(ky2*dt + (kz2+kx2)*S_ck)*inv_k2` | strong x-driven cross term in `Ezx` / `Bzx` |
| `C18` | `i*c2*kx*(kz2*dt + (ky2+kx2)*S_ck)*inv_k2` | strong x-driven cross term in `Eyx` / `Byx` |
| `C19` | `i*c2*ky*(kz2*dt + (kx2+ky2)*S_ck)*inv_k2` | strong y-driven cross term in `Exy` / `Bxy` |
| `C20` | `i*c2*ky*(kx2*dt + (kz2+ky2)*S_ck)*inv_k2` | strong y-driven cross term in `Ezy` / `Bzy` |
| `C21` | `i*c2*kz*(kx2*dt + (ky2+kz2)*S_ck)*inv_k2` | strong z-driven cross term in `Eyz` / `Byz` |
| `C22` | `i*c2*kz*(ky2*dt + (kx2+kz2)*S_ck)*inv_k2` | strong z-driven cross term in `Exz` / `Bxz` |

For magnetic updates, the same coefficients are divided by `c2`. This preserves the E/B unit relationship in Maxwell coupling.

## `C23-C25`: divergence-cleaning coupling

This group exists only when:

```cpp
dive_cleaning && divb_cleaning
```

| coefficient | source expression | interpretation |
|---|---|---|
| `C23` | `i*c2*kx*S_ck` | x-direction coupling between `F/G` and `E/B` split components |
| `C24` | `i*c2*ky*S_ck` | y-direction coupling between `F/G` and `E/B` split components |
| `C25` | `i*c2*kz*S_ck` | z-direction coupling between `F/G` and `E/B` split components |

The corresponding `_c2` variants are used in magnetic-field and `F` updates.

## Regression mapping

| regression | branch hit | analysis coverage | limitation |
|---|---|---|---|
| `test_2d_pml_x_psatd` | no-cleaning branch, `C1-C22` | `analysis_pml_psatd.py` checks iteration-50 energy oracle and final reflectivity `< 1e-6` | 2D reflectivity only, no direct coefficient inspection |
| `test_2d_pml_x_galilean` | cleaning branch with `T2`, `C1-C9`, `C23-C25` | same reflectivity gate, with Galilean-specific energy oracle | coverage is indirect: field energy and reflectivity, not `F/G` residuals |
| `test_3d_pml_psatd_dive_divb_cleaning` | 3D cleaning branch | CMake marks `analysis=OFF`; only default checksum path remains | cannot support a strong physics claim for 3D cleaning |
| `test_rz_pml_psatd` | RZ-specific PML algorithm, not this Cartesian file | residual `Er/Ez` max `< 2.0` | does not exercise `PsatdAlgorithmPml.cpp` |

## Follow-up when LeeCPC2015 PDF is available

1. Check whether the paper derives a pseudo-spectral PML propagator in a form equivalent to `C1-C25`.
2. If the paper instead focuses on measured efficiency/reflection, keep the coefficient atlas source-labeled and cite the paper only for the efficiency study.
3. Verify whether the paper discusses Galilean phase factors or divergence-cleaning fields. If not, keep those as WarpX implementation extensions.


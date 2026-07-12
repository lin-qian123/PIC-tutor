# Higuera-Cary 2017 relativistic pusher reference

## Bibliographic status

- Title: Structure-preserving second-order integration of relativistic charged particle trajectories in electromagnetic fields
- Authors: A. V. Higuera, J. R. Cary
- Venue: Physics of Plasmas 24(5), 052104 (2017)
- DOI: `10.1063/1.4979989`

This is the Higuera-Cary reference used by Chapter 4 and by WarpX's `UpdateMomentumHigueraCary.H` source mapping.

## Local asset status

The directory contains a 9-page full-text PDF, MinerU Markdown, 44 extracted images and a Chinese walkthrough. The local package is checked by `scripts/audit_pusher_paper_asset_contract.py`.

The package supports the volume-preservation, `E x B` drift, Jacobian and practical-timestep topology discussion. It does not imply that the current WarpX regression reproduces the paper's Poincare-section experiment.

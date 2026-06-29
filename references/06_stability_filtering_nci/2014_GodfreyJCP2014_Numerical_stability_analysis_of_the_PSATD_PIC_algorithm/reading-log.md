# Reading Log

## 2026-06-29

- Selected Godfrey, Vay, Haber 2014 (`GodfreyJCP2014_PSATD`) as the v0.19 anchor for the PSATD/NCI strategy-spectrum section.
- Downloaded the arXiv PDF from https://arxiv.org/pdf/1305.7375 and converted it with MinerU.
- Kept all artifacts in this paper-specific folder: PDF, MinerU Markdown, `images/`, and Chinese explanation note.
- Main takeaways for Chapter 6:
  - PSATD has superior vacuum dispersion and no conventional Courant limit, but relativistic-beam PIC still has NCI through spatial/temporal aliases.
  - Digital filtering, higher-order interpolation, current scaling, and timestep choice should be presented as distinct mitigation families.
  - WarpX `warpx.use_filter = 1` maps to the filtering family; `psatd.current_correction` should be described as a continuity/Gauss-law path rather than Godfrey's NCI current scaling.
  - Galilean PSATD remains a representation-level strategy distinct from fixed-grid current scaling/filtering.

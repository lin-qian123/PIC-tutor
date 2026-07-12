# Esirkepov 2001 CPC current deposition reference

## Bibliographic status

- Title: Exact charge conservation scheme for Particle-in-Cell simulation with an arbitrary form-factor
- Author: T. Zh. Esirkepov
- Venue: Computer Physics Communications 135(2), 144-153
- DOI: `10.1016/S0010-4655(00)00228-9`
- PII: `S0010465500002289`
- DOI landing page: <https://doi.org/10.1016/S0010-4655(00)00228-9>

This is the primary current-deposition reference cited by WarpX as `Esirkepovcpc01` in `../warpx/Docs/source/refs.bib` and `bibliography/warpx-refs.bib`.

## Access status on 2026-07-13

Crossref confirms the title, venue, pages, date, and Elsevier TDM links. The official Elsevier content API returns the publisher metadata and reports `openaccess=0` / `openaccessArticle=false`; an unauthenticated PDF request returns HTTP 406 with a minimized-metadata warning. The direct ScienceDirect PDF endpoint remains unavailable from the current local command-line environment.

However, an author-posted arXiv preprint is publicly available and has now been materialized in this directory:

- arXiv: `physics/9901047`
- preprint title: `Exact charge conservation scheme for Particle-in-Cell simulations for a big class of form-factors`

This means the directory now contains:

- a legal full-text PDF for first-pass reading,
- MinerU Markdown,
- `images/`,
- a first-round Chinese reading note.

What is still missing is the publisher-formatted CPC PDF and a page-by-page comparison between the 1999 preprint and the 2001 CPC publication. Do not silently treat the current local PDF as if it were already the final publisher version.

The current acquisition and verification boundary is recorded in:

`access-audit.md`

The source-to-paper follow-up map for Chapter 5 is recorded in:

`2001_EsirkepovCPC2001_Exact_charge_conservation_scheme_for_Particle-In-Cell_simulation_with_an_arbitrary_form-factor-源码映射准备.md`

The local package passes `scripts/audit_deposition_paper_asset_contract.py`: 13-page arXiv PDF, 39 images, MinerU structure, first-round Chinese walkthrough, and publisher-PDF boundary. The contract does not certify the 2001 CPC publisher version.

## Why this paper matters here

For `PIC-tutor`, this paper is the main primary source behind the Chapter 5 line that WarpX current deposition can enforce charge conservation by constructing current from old/new particle-shape differences rather than by direct `q v S` assignment.

The current local preprint is enough to support a first paper-derived walkthrough of:

- the discrete continuity-equation framing,
- `density decomposition`,
- the uniqueness claim under linearity/symmetry constraints,
- and the second-order spline algorithm outline.

But Chapter 5 should still distinguish:

- what is already backed by the arXiv preprint,
- and what still awaits comparison with the 2001 CPC publication layout and wording.

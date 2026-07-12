# Villasenor-Buneman 1992 CPC current deposition reference

## Bibliographic status

- Title: Rigorous charge conservation for local electromagnetic field solvers
- Authors: John Villasenor, Oscar Buneman
- Venue: Computer Physics Communications 69(2-3), 306-316
- DOI: `10.1016/0010-4655(92)90169-Y`
- PII: `001046559290169Y`
- DOI landing page: <https://doi.org/10.1016/0010-4655(92)90169-Y>

This is the primary local-electromagnetic charge-conserving deposition reference cited by WarpX as `Villasenorcpc92` in `../warpx/Docs/source/refs.bib` and `bibliography/warpx-refs.bib`.

## Access status on 2026-07-13

Crossref confirms the title, venue, pages, date, and Elsevier TDM links. OpenAlex currently reports the article as `closed` OA with no repository PDF URL, and the direct ScienceDirect PDF endpoint still returns HTTP 403 from the current local command-line environment.

However, this article had already been acquired on the local machine before the current turn, and the project has now materialized that existing asset into this directory. The directory now contains:

- the local full-text PDF,
- MinerU Markdown,
- `images/`,
- a first-round Chinese reading note.

So this paper is no longer only a bibliographic gap or access-audit placeholder for `PIC-tutor`; it is now a usable paper asset for Chapter 5.

The current acquisition and verification boundary is recorded in:

`access-audit.md`

The source-to-paper follow-up map for Chapter 5 is recorded in:

`1992_VillasenorBunemanCPC1992_Rigorous_charge_conservation_for_local_electromagnetic_field_solvers-源码映射准备.md`

The local package passes `scripts/audit_deposition_paper_asset_contract.py`: 11-page PDF, 27 images, MinerU structure, first-round Chinese walkthrough, and access boundary. The contract does not certify publisher provenance or final-formula transcription.

## Why this paper matters here

For `PIC-tutor`, this paper is the primary source behind the Chapter 5 line that Villasenor deposition differs structurally from Esirkepov: it organizes current by boundary/cell-crossing-driven local flux decomposition rather than by a single old/new shape-difference accumulation.

The current local asset supports a formula-audited paper-derived walkthrough of:

- local field updating versus global transform methods,
- strict finite-difference charge conservation,
- four/seven/ten-boundary move decomposition,
- and the three-dimensional complementary-mesh extension.

Chapter 5 now writes Villasenor as a paper-backed, source-grounded, formula-audited line. The remaining publication work is figure-by-figure transcription, notation normalization, and checking every modern geometry/order branch against the paper assumptions.

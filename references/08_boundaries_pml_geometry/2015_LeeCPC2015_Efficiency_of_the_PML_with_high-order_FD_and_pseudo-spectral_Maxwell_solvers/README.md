# Lee & Vay 2015 CPC PML / pseudo-spectral solver reference

## Bibliographic status

- Title: Efficiency of the Perfectly Matched Layer with high-order finite difference and pseudo-spectral Maxwell solvers
- Authors: P. Lee, J.-L. Vay
- Venue: Computer Physics Communications 194, 1-9
- DOI: `10.1016/j.cpc.2015.04.004`
- PII: `S0010465515001356`
- OSTI record: <https://www.osti.gov/pages/biblio/1246488>
- DOI landing page: <https://doi.org/10.1016/j.cpc.2015.04.004>

This is the primary reference cited by WarpX as `LeeCPC2015` in `../warpx/Docs/source/refs.bib` and `bibliography/warpx-refs.bib`.

## Access status on 2026-08-07

OpenAlex reports the CPC article as green OA and points to the OSTI record `1246488`. Crossref also records an accepted-manuscript license after 2016-05-21. However, the current OSTI record and API responses expose bibliographic metadata and citation links, not a direct PDF/full-text file. ScienceDirect PDF access returns HTTP 403 from the local command line, and the Elsevier API returns minimized metadata without authorization.

The public eScholarship record now exposes a valid 7-page PDF endpoint. The PDF has been downloaded to this directory, converted with the project stdlib MinerU workflow, and materialized with 13 extracted images plus a Chinese walkthrough. This is an accepted/submitted manuscript and should not be silently labeled as the publisher-formatted CPC version.

The indexed ScienceDirect record also exposes the publisher abstract: it reports that the analyzed PML efficiency is preserved for arbitrary solver order, including the infinite-order pseudo-spectral limit. This remains abstract-level publication evidence; the publisher-formatted PDF is still unavailable for line-by-line comparison.

Primary accepted-manuscript source: <https://escholarship.org/uc/item/49m2k3vj>. The local package is covered by `scripts/audit_leecpc2015_manuscript_contract.py`; the locally retained final PDF is covered by `scripts/audit_publisher_pdf_closure.py` and is not redistributed.

The v0.25 source-to-paper follow-up table is in:

`2015_LeeCPC2015_Efficiency_of_the_PML_with_high-order_FD_and_pseudo-spectral_Maxwell_solvers-公式核对清单.md`

## Publisher-version closure

The publisher-formatted CPC PDF is now locally available through authorized access. It is stored with its MinerU package in the Git-ignored `publisher/` directory. [The bounded final-version compare](../../../docs/leecpc2015-publisher-version-compare.md) distinguishes final front matter, abstract, section architecture, high-order/PSTD formula anchors, reflection/results, and appendices from the accepted/submitted manuscript. It does not redistribute the PDF or make its formulas identical to WarpX implementation branches.

## Relation to the AIP conference version

The related AIP Conference Proceedings article has DOI `10.1063/1.4965625` and is tracked separately under:

`references/08_boundaries_pml_geometry/2016_LeeVayACP2016_Efficiency_of_the_PML_with_high-order_FD_and_pseudo-spectral_Maxwell_solvers/`

For PIC-tutor, the CPC article should remain the main citation because it is the reference used by WarpX. The AIP record is useful as a second official bibliographic endpoint and may become a practical full-text source if its bronze OA PDF endpoint becomes accessible.

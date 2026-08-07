# Access Audit: LeeCPC2015

Date: 2026-07-13

Current publisher identifiers rechecked for the v0.96 release audit:

- DOI landing page: `https://doi.org/10.1016/j.cpc.2015.04.004`
- Elsevier PII: `S0010465515001356`
- Publisher record: `https://www.sciencedirect.com/science/article/pii/S0010465515001356`
- Publisher PDF route tested: `https://www.sciencedirect.com/science/article/pii/S0010465515001356/pdfft`

## Target

- Key: `LeeCPC2015`
- DOI: `10.1016/j.cpc.2015.04.004`
- Title: Efficiency of the Perfectly Matched Layer with high-order finite difference and pseudo-spectral Maxwell solvers
- Authors: P. Lee, J.-L. Vay
- Journal: Computer Physics Communications 194, 1-9

## Checks performed

| Source | Result | Evidence |
|---|---|---|
| WarpX `Docs/source/refs.bib` | Confirms this is the WarpX bibliographic key for the PML/PSATD reference | `../warpx/Docs/source/refs.bib:2496-2506` |
| Local `bibliography/warpx-refs.bib` | Contains the same CPC DOI and title | `bibliography/warpx-refs.bib:2442-2452` |
| OpenAlex | Reports `is_oa=true`, `oa_status=green`, `oa_url=https://www.osti.gov/biblio/1246488`, `any_repository_has_fulltext=true` | API check on 2026-06-29 |
| Crossref | Reports Elsevier TDM links and accepted-manuscript license after 2016-05-21 | API check on 2026-06-29 |
| OSTI pages record | Returns a metadata page for OSTI ID `1246488` | `https://www.osti.gov/pages/biblio/1246488` |
| OSTI API record | Returns metadata including `article_type=Publisher's Accepted Manuscript`, but only citation links | `https://www.osti.gov/api/v1/records/1246488` |
| OSTI page button | `View Accepted Manuscript (Publisher)` resolves to the DOI landing page, not an OSTI-hosted file | HTML inspection on 2026-06-29 |
| OSTI purl guesses | `https://www.osti.gov/servlets/purl/1246488` and variants returned HTTP 404 | local curl checks on 2026-06-29 |
| eScholarship submitted-version location | OpenAlex lists `https://escholarship.org/uc/item/49m2k3vj`; page and likely PDF endpoint return HTTP 403 from local curl | local curl checks on 2026-06-29 |
| eScholarship PDF re-check | Browser-like `curl -L` to `https://escholarship.org/content/qt49m2k3vj/qt49m2k3vj.pdf?t=p0jvaf` returned a valid 7-page PDF | local `file`/PDF header check on 2026-07-11 |
| MinerU conversion | Public eScholarship PDF was downloaded, converted with the project stdlib MinerU workflow, and produced Markdown plus 13 extracted images | local workflow on 2026-07-11 |
| Local accepted-manuscript contract | `scripts/audit_leecpc2015_manuscript_contract.py` checks the 7-page PDF, MinerU section/formula anchors, 13 images, Chinese walkthrough and explicit publisher boundary | contract run on 2026-07-13; all checks pass |
| ScienceDirect PDF endpoint | Returned HTTP 403 | local curl check on 2026-06-29 |
| Elsevier content API PDF endpoint | Returned HTTP 406/minimized metadata without authorization | local curl check on 2026-06-29 |
| AIP Scitation DOI PDF endpoint | `https://aip.scitation.org/doi/pdf/10.1063/1.4965625` returns a short HTML page, not a PDF; the AIP article PDF endpoint returns Cloudflare HTTP 403 | local curl checks on 2026-06-29 |
| AIP `pubs.aip.org` direct PDF endpoint | `https://pubs.aip.org/aip/acp/article-pdf/doi/10.1063/1.4965625/13262029/050002_1_online.pdf` still returns Cloudflare HTTP 403 with browser-like user agent | local curl check on 2026-06-29 |
| ScienceDirect indexed abstract re-check | The publisher record exposes the abstract claim that PML efficiency is preserved for arbitrary solver order, including the infinite-order pseudo-spectral limit; this is abstract-level evidence, not a publisher-PDF line-by-line reading | ScienceDirect indexed record checked on 2026-07-13 |
| ScienceDirect publisher PDF current re-check | The publisher PDF route remains access-controlled in the current environment; no local publisher-formatted PDF was materialized | current publisher route and accepted-manuscript boundary on 2026-07-13 |

## Current decision

The article is now ingested from the public eScholarship accepted/submitted manuscript. The book may use the local PDF, MinerU Markdown, images, and Chinese walkthrough for a first paper-backed explanation. This does not upgrade the asset to the publisher-formatted CPC version; version-specific wording, pagination, and final equation typography still require a separate comparison.

The publisher-formatted CPC PDF is still missing. The indexed publisher abstract can be cited for the narrow claim that the reported PML efficiency is preserved at high order and in the pseudo-spectral limit, but it cannot settle final pagination, equation typography or version-specific formula differences.

The local package is classified as `ACCEPTED_MANUSCRIPT_SOURCE_GROUNDED_PML_FORMULAS_PUBLISHER_CPC_PDF_MISSING`. The contract closes asset integrity and first-round source mapping, not the publisher-version comparison.

## Next authorized acquisition paths

1. Compare the local eScholarship manuscript with the CPC publisher version when institutional access is available.
2. Keep the CPC article as the main WarpX citation; treat the AIP conference version as a related record.
3. Complete the paper-to-source comparison for PML profile, reflection recurrence, PSTD shift factors, and the boundary between paper formulas and WarpX `C1-C25`.

## 2026-08-07 publisher-PDF closure

The user locally obtained the publisher-formatted CPC PDF through their authorized access. The file was validated as a 9-page PDF, its SHA-256 recorded as `920ec7958bdcd45168ac43e60eeb2acdfe4fa63222f671413f0c41c83572a41e`, and it was converted with MinerU in the paper-specific local `publisher/` directory.

The source PDF and MinerU derivative are Git-ignored. `docs/leecpc2015-publisher-version-compare.md` records the bounded comparison with the seven-page accepted/submitted manuscript: final front matter, abstract, section architecture, high-order/PSTD anchors, reflection/results, and appendices. This closes the publisher-PDF access and version-comparison gap; it does not establish redistribution rights or make the paper formulas identical to WarpX `C1`--`C25`, cleaning, Galilean, or RZ code paths.

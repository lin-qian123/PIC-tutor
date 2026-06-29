# Access Audit: LeeCPC2015

Date: 2026-06-29

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
| ScienceDirect PDF endpoint | Returned HTTP 403 | local curl check on 2026-06-29 |
| Elsevier content API PDF endpoint | Returned HTTP 406/minimized metadata without authorization | local curl check on 2026-06-29 |
| AIP Scitation DOI PDF endpoint | `https://aip.scitation.org/doi/pdf/10.1063/1.4965625` returns a short HTML page, not a PDF; the AIP article PDF endpoint returns Cloudflare HTTP 403 | local curl checks on 2026-06-29 |
| AIP `pubs.aip.org` direct PDF endpoint | `https://pubs.aip.org/aip/acp/article-pdf/doi/10.1063/1.4965625/13262029/050002_1_online.pdf` still returns Cloudflare HTTP 403 with browser-like user agent | local curl check on 2026-06-29 |

## Current decision

The article should be treated as identified and bibliographically verified, but not yet ingested. The book can cite the DOI and use the WarpX source/documentation mapping, but it should not claim to have a PDF-derived MinerU extraction or a complete paper formula walkthrough.

## Next authorized acquisition paths

1. Use institutional access to download the CPC published version from ScienceDirect.
2. If OSTI later exposes the accepted manuscript file, download it from the OSTI record and record the exact URL.
3. If eScholarship becomes reachable from a browser or different network, verify whether it hosts a submitted manuscript and whether its license is compatible with this project.
4. If the AIP conference bronze OA PDF endpoint becomes accessible, use it as a related version but keep the CPC article as the main WarpX citation.
5. After obtaining a PDF, place it in this directory and run the project paper workflow before updating the manuscript from "access audit" to "paper-reading closure".

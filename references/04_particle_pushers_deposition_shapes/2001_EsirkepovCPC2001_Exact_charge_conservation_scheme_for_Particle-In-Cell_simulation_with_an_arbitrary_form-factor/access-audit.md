# Access Audit: EsirkepovCPC2001

Date: 2026-07-13

Current publisher identifiers rechecked for the v0.96 release audit:

- DOI landing page: `https://doi.org/10.1016/S0010-4655(00)00228-9`
- Elsevier PII: `S0010465500002289`
- Publisher record: `https://www.sciencedirect.com/science/article/pii/S0010465500002289`
- Publisher PDF route tested: `https://www.sciencedirect.com/science/article/pii/S0010465500002289/pdf`

## Target

- Key: `Esirkepovcpc01`
- DOI: `10.1016/S0010-4655(00)00228-9`
- Title: Exact charge conservation scheme for Particle-in-Cell simulation with an arbitrary form-factor
- Author: T. Zh. Esirkepov
- Journal: Computer Physics Communications 135(2), 144-153

## Checks performed

| Source | Result | Evidence |
|---|---|---|
| WarpX `Docs/source/refs.bib` | Confirms this is the WarpX bibliographic key for the exact charge-conserving deposition reference | `../warpx/Docs/source/refs.bib` and local grep on 2026-07-02 |
| Local `bibliography/warpx-refs.bib` | Contains the same DOI and title | local grep on 2026-07-02 |
| Crossref | Confirms title, venue, volume, issue, pages, date, and Elsevier TDM links | API check on 2026-07-02 |
| OpenAlex | Reports the CPC article as `is_oa=false`, `oa_status=closed`, with no repository OA URL attached to that record | API check on 2026-07-02 |
| ScienceDirect article page | Metadata and abstract page is discoverable | web search on 2026-07-02 |
| ScienceDirect direct PDF endpoint | Returns HTTP 403 from local command-line access | local `curl -I -L` check on 2026-07-02 |
| Elsevier content API text-mining links | Crossref exposes TDM XML/plaintext links, but these are not equivalent to a locally usable full PDF for project reading workflow | Crossref API check on 2026-07-02 |
| arXiv preprint | Author-posted full-text preprint is publicly reachable at `physics/9901047` | web search + local `curl -I -L https://arxiv.org/pdf/physics/9901047` on 2026-07-02 |
| arXiv metadata re-check | arXiv page confirms submission date 1999-01-26, preprint title, 13 pages, no figures, and 10 bibliography entries | arXiv abstract page re-check on 2026-07-11 |
| CPC bibliographic metadata re-check | Public bibliographic indexes reconfirm CPC 135(2), 144-153 (2001), DOI `10.1016/S0010-4655(00)00228-9`, and the published title | web search on 2026-07-11 |
| ScienceDirect direct-PDF re-check | Search result exposes the publisher PDF URL, but browser rendering reaches a download-preparation error and local browser-like `curl` still returns HTTP 403 | web open and local `curl -L` on 2026-07-11 |
| Elsevier content API metadata re-check | Official API returns the publisher title, PII `S0010465500002289`, cover date `2001-04-01`, and explicitly reports `openaccess=0` / `openaccessArticle=false` | unauthenticated API GET on 2026-07-12 |
| Elsevier content API PDF request | The same API endpoint with `httpAccept=application/pdf` returns HTTP 406 and an unauthorized/minimized-metadata warning; no publisher PDF was obtained | local `curl -L -I` on 2026-07-12 |
| Local ingestion | Downloaded arXiv preprint, ran MinerU, and generated Chinese reading note in this directory | local workflow run on 2026-07-02 |
| Local filesystem re-check | No separate CPC publisher PDF was found elsewhere on this Mac beyond the already materialized project-local preprint asset | `mdfind` + `rg` over local paper folders on 2026-07-02 |
| CiNii Research metadata re-check | Confirms CPC 135(2), 144-153, DOI `10.1016/S0010-4655(00)00228-9` and Elsevier rights metadata; no publisher full-text PDF is exposed on the record | web search on 2026-07-12 |
| ResearchGate record re-check | Record exposes abstract and a `Request full-text` path, but not a downloadable full-text PDF | web search on 2026-07-12 |
| ScienceDirect PDF endpoint re-check | Current local `curl -L -I` still returns HTTP 403; response advertises TDM policy but does not provide PDF bytes | local command on 2026-07-12 |
| ScienceDirect PDF endpoint current re-check | Search-discovered publisher PDF URL was tested with `curl -L` on 2026-07-13; response is HTTP/2 403 with `content-type: text/html`, Cloudflare headers and no PDF bytes. The browser-facing page likewise shows “Preparing your download” and “A problem was encountered” rather than a PDF. | local `curl` plus ScienceDirect page check on 2026-07-13 |
| ScienceDirect indexed abstract current re-check | Search result exposes the published abstract: arbitrary quasi-particle form-factor, straight-line trajectory assumption, no Poisson solve, and 2D/3D demonstration. This is abstract-level evidence only, not a publisher-PDF reading. | ScienceDirect indexed result on 2026-07-13 |
| Publisher/preprint abstract compare | The indexed publisher abstract and the arXiv abstract were compared by topic; aligned claims and wording differences are recorded in `notes/code-reading/particles/63-esirkepov-publisher-abstract-compare.md`. This upgrades only the abstract-level classification, not the missing publisher PDF. | local bounded-compare audit on 2026-07-13 |
| Local paper-asset contract | `scripts/audit_deposition_paper_asset_contract.py` checks the 13-page arXiv PDF, 39 images, MinerU structure, Chinese note and publisher-PDF boundary | contract run on 2026-07-13; all checks pass |

## Current decision

The 2001 CPC publication should still be treated as not yet locally acquired in publisher PDF form, but the underlying algorithm is no longer "not ingested": an author-posted arXiv preprint has now been legally downloaded, converted via MinerU, and used for a first paper-backed reading pass.

Therefore the current project state is:

- **publisher PDF status**: still missing;
- **legal full-text status**: available through the arXiv preprint;
- **Chapter 5 wording**: can now cite a first-pass preprint-backed derivation for Esirkepov, but should still avoid claiming that the final CPC PDF has already been checked line by line.

More concretely, the strongest currently verified transport-layer evidence is:

- ScienceDirect article and PDF endpoints exist for the 2001 CPC publication;
- the PDF endpoint still answers `HTTP/2 403` from the current local command-line environment on 2026-07-02;
- the arXiv preprint endpoint answers `HTTP/2 200` with `content-type: application/pdf` on the same date.

So the present blocker is no longer "the paper is unknown" or "no legal full text exists", but specifically: **the publisher-formatted 2001 CPC PDF is not yet locally obtainable in this environment for line-by-line comparison**.

The 2026-07-11/12/13 re-check therefore closes the publication-metadata, abstract-discovery and access-status part of the audit. It does not change the PDF status or upgrade the chapter to publisher-PDF line-by-line evidence. The official API's `openaccess=0`, the 406 PDF response from the API route, and the 403/HTML response from the browser-facing route make the remaining boundary explicit: the current environment can retrieve publisher metadata and indexed abstract text but not the licensed full text. The currently discoverable publisher PDF endpoint is:

`https://www.sciencedirect.com/science/article/pii/S0010465500002289/pdf?md5=526385691a2c427ee41e96a0bfbd1d3b&pid=1-s2.0-S0010465500002289-main.pdf`

The 2026-07-12 alternate-index search does not change that decision: CiNii adds metadata only, ResearchGate adds an author-request route only, and the direct publisher endpoint still returns `403`. These are discovery/access-status evidence, not substitutes for the publisher-formatted PDF.

## Next authorized acquisition paths

1. Use institutional access to download the published CPC PDF from ScienceDirect.
2. Once the CPC PDF is available, do a bounded compare against the current arXiv preprint:
   - title wording;
   - abstract wording;
   - section titles and numbering;
   - `Eq.(23)` and surrounding density-decomposition formulas;
   - the algorithm section built around second-order spline form-factor.
3. After that compare is done, upgrade Chapter 5 wording from "preprint-backed + source-grounded" to a cleaner "paper-and-source closed" statement.

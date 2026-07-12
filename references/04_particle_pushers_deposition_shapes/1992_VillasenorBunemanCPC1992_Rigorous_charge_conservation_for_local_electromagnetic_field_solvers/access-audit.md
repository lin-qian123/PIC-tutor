# Access Audit: VillasenorBunemanCPC1992

Date: 2026-07-13

## Target

- Key: `Villasenorcpc92`
- DOI: `10.1016/0010-4655(92)90169-Y`
- Title: Rigorous charge conservation for local electromagnetic field solvers
- Authors: John Villasenor, Oscar Buneman
- Journal: Computer Physics Communications 69(2-3), 306-316

## Checks performed

| Source | Result | Evidence |
|---|---|---|
| WarpX `Docs/source/refs.bib` | Confirms this is the WarpX bibliographic key for the Villasenor-Buneman charge-conserving deposition reference | `../warpx/Docs/source/refs.bib` and local grep on 2026-07-02 |
| Local `bibliography/warpx-refs.bib` | Contains the title and DOI | local grep on 2026-07-02 |
| Crossref | Confirms title, venue, volume, issue, pages, date, and Elsevier TDM links | API check on 2026-07-02 |
| OpenAlex | Reports `is_oa=false`, `oa_status=closed`, no repository OA URL | API check on 2026-07-02 |
| ScienceDirect article page | Metadata and abstract page is discoverable | web search on 2026-07-02 |
| ScienceDirect direct PDF endpoint | Returns HTTP 403 from local command-line access | local `curl -I -L` check on 2026-07-02 |
| Elsevier content API text-mining links | Crossref exposes TDM XML/plaintext links, but these are not equivalent to a locally usable full PDF for project reading workflow | Crossref API check on 2026-07-02 |
| Local machine search | Existing full-text PDF already present in local Zotero-style paper store | `mdfind` and local file check on 2026-07-02 |
| Local MinerU cache | Existing MinerU Markdown and `images/` already present in local MinerU output tree | local file check on 2026-07-02 |
| Project ingestion | Copied local PDF + MinerU outputs into this paper directory and added first-round Chinese reading note | project-local ingestion on 2026-07-02 |
| Local paper-asset contract | `scripts/audit_deposition_paper_asset_contract.py` checks the 11-page PDF, 27 images, MinerU structure, Chinese note and access boundary | contract run on 2026-07-13; all checks pass |

## Current decision

The article is no longer merely bibliographically verified: it has now been ingested into the project from an already-existing local full-text PDF and MinerU cache.

Therefore the current project state is:

- **publisher web access**: still blocked from current command-line environment;
- **local full-text status**: available on this machine and now copied into the project paper directory;
- **Chapter 5 wording**: can now cite Villasenor as a paper-backed line rather than a source-only gap, while still keeping the current note labeled as first-round rather than final-formula-complete.
- **local asset contract**: passed as `LOCAL_FULLTEXT_SOURCE_GROUNDED_FORMULA_AUDIT_PUBLISHER_PROVENANCE_PENDING`.

## Next authorized acquisition paths

1. Verify provenance/metadata of the local PDF against the CPC publication record if needed for later public-repo or copyright audits.
2. Continue the Chinese reading note from first-round structure summary to a fuller equation-by-equation walkthrough.
3. Use the current paper asset to upgrade Chapter 5 Villasenor discussion from "source-grounded" to a cleaner "paper-backed + source-grounded" statement, then continue toward full paper-and-source closure.

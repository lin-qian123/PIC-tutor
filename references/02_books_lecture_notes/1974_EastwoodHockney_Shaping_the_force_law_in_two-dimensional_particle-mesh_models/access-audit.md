# Eastwood and Hockney 1974 access audit

| source | result |
|---|---|
| ScienceDirect article record | Abstract and bibliographic metadata available |
| DOI landing page | DOI identity recorded; publisher full text not materialized locally |
| Local workspace | No PDF or MinerU output found |

## Bounded abstract evidence

The abstract describes an ordered hierarchy of two-dimensional charge-sharing schemes, including NGP, CIC and higher-order nine-point choices. It also describes potential-correction coefficients and reports that force-law angular anisotropy can be reduced from roughly 50 percent for NGP/CIC to below 0.5 percent with the proposed methods.

These are abstract-level claims only. The paper's derivation, force-law plots, empirical setup, and numerical tables remain unchecked.

## Access boundary

- `publisher_pdf`: missing;
- `mineru_markdown`: not generated;
- `full_text_line_by_line_compare`: not completed;
- `abstract_backed`: true;
- `metadata_verified`: true.

## 2026-07-13 acquisition recheck

- Elsevier API `https://api.elsevier.com/content/article/pii/0021999174900448` returned the DOI/title metadata, with `openaccess=0` and `openaccessArticle=false`.
- Browser-like requests to the ScienceDirect `/pdf` endpoint returned HTTP `403` HTML rather than a PDF.
- This confirms that metadata is reachable but does not upgrade the local evidence to publisher full text.

# Hockney, Goel and Eastwood 1974 access audit

| source | result |
|---|---|
| ScienceDirect article record | Abstract and bibliographic metadata available |
| DOI landing page | DOI identity recorded; publisher full text not materialized locally |
| Local workspace | No PDF or MinerU output found |

## Bounded abstract evidence

The abstract describes QPM as a Gaussian-cloud particle-mesh model with potential shaping, and PPPM as a particle-particle correction for nearby particles. It reports a large noise reduction for QPM relative to CIC and describes spatial resolution below the mesh scale for PPPM.

These are abstract-level claims only. The paper's derivation, implementation details, figures, and numerical protocol remain unchecked.

## Access boundary

- `publisher_pdf`: missing;
- `mineru_markdown`: not generated;
- `full_text_line_by_line_compare`: not completed;
- `abstract_backed`: true;
- `metadata_verified`: true.

## 2026-07-13 acquisition recheck

- Elsevier API `https://api.elsevier.com/content/article/pii/0021999174900102` returned the DOI/title metadata, with `openaccess=0` and `openaccessArticle=false`.
- Browser-like requests to the ScienceDirect `/pdf` endpoint returned HTTP `403` HTML rather than a PDF.
- This confirms that metadata is reachable but does not upgrade the local evidence to publisher full text.

# Esirkepov 2001 CPC Publisher-Version Bounded Compare

## Scope and handling boundary

On 2026-08-07, the locally licensed CPC publisher PDF was placed in the paper-specific local `publisher/` directory, validated as a 10-page PDF, and converted with MinerU. Its SHA-256 is `cb03ca28144aa351ca964bbc8ba5012d4e88f5ba8f3a7a10e4b437c1afb07855`.

The PDF, its MinerU Markdown, and extracted images are ignored by Git. This record contains comparison results only; it neither redistributes the PDF nor establishes redistribution rights.

## Bounded comparison

| Item | Publisher-final evidence | Comparison with the local arXiv preprint | Result |
|---|---|---|---|
| Title | PDF page 1; MinerU heading | The final title is `...simulation with an arbitrary form-factor`; the 1999 preprint says `...simulations for a big class of form-factors`. | Confirmed editorial/title revision; do not treat versions as byte-identical. |
| Abstract | PDF page 1; MinerU `Abstract` | Both describe density decomposition, charge conservation, a straight trajectory over one step, and a second-order spline demonstration. The publisher wording frames an arbitrary quasi-particle form-factor and the no-Poisson-solve consequence. | Same core algorithmic claim, with final-version wording verified. |
| Section structure | PDF pages 2--9; MinerU sections 1--6 | Sections 1--4 retain the continuity, density-decomposition, and second-order-form-factor route. The final version separates `5. Reduction to two dimensions` and moves the conclusion to section 6; the preprint ends with section 5. | Structural revision recorded. |
| `Eq. (23)` | PDF page 5 (CPC p. 148); MinerU within section 3 | The publisher equation keeps the three-component `W^1/W^2/W^3` density-decomposition construction and the `1/3`, `1/6` weights used by the Chapter 5 source mapping. | Formula anchor verified against the final PDF; this is not a claim of character-perfect OCR. |
| Second-order spline algorithm | PDF pages 5--7 (CPC pp. 148--150); MinerU section 4 | The final paper labels the construction `Computation scheme for the second-order polynomial form-factor`, gives the second-order spline, and gives the local current recipe. | Algorithm anchor verified against the final PDF. |

## Resulting evidence boundary

The Chapter 5 statement may now say that the preprint-to-CPC final version has received a bounded comparison for the title, abstract, section structure, `Eq. (23)`, and the second-order spline algorithm. The result supports the paper-to-source explanation at those anchors.

It does not prove all WarpX geometries, AMR synchronization, GPU kernels, or runtime consumers. Those require their own source and runtime evidence. It also does not authorize public distribution of the CPC PDF.

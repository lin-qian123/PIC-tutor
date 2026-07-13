# Access audit: Andriyash 2016

Date: 2026-07-13

## Bibliographic identity

- Title: `Laser-plasma interactions with a Fourier-Bessel Particle-in-Cell method`
- Authors: Igor A. Andriyash, Remi Lehe, Agustin Lifschitz
- arXiv: `1512.09289`
- DOI: `10.1063/1.4943281`
- Journal: *Physics of Plasmas*, 23(3)

## Local evidence

| item | status | evidence |
|---|---|---|
| PDF | present | local 9-page PDF in this directory |
| MinerU Markdown | present | local conversion output |
| images | present | 26 extracted images in `images/` |
| Chinese note | present | ordered note with formulas, figures and boundaries |
| official metadata | verified | arXiv abstract page and DOI metadata lookup |
| source code | boundary | paper discusses PLARES-PIC; no PLARES-PIC checkout is included here |
| WarpX equivalence | not claimed | current WarpX source/runtime must be audited separately |

## Reading boundary

The local PDF is sufficient for formula-level reading of the method and its PLARES-PIC/CALDER-CIRC benchmarks. It does not provide a WarpX implementation proof, a WarpX runtime regression, or a complete reproduction of the paper's figures. The note corrects a MinerU OCR error in the auxiliary-field definition by checking the source rendering: `g = curl(b)`, not a velocity cross product.

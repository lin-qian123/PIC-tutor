# Lee and Vay 2015 CPC Publisher-Version Bounded Compare

## Scope and handling boundary

On 2026-08-07, the locally licensed CPC publisher PDF was placed in the paper-specific local `publisher/` directory, validated as a 9-page PDF, and converted with MinerU. Its SHA-256 is `920ec7958bdcd45168ac43e60eeb2acdfe4fa63222f671413f0c41c83572a41e`.

The PDF, its MinerU Markdown, and extracted images are ignored by Git. This public record is a comparison index only and does not grant redistribution rights.

## Bounded comparison with the seven-page eScholarship accepted/submitted manuscript

| Item | Publisher-final evidence | Comparison result | Writing boundary |
|---|---|---|---|
| Bibliographic front matter | PDF page 1; MinerU article-info block | The final version supplies the CPC 194 (2015) 1--9 pagination, affiliations, received/revised/accepted dates, keywords, and Elsevier publication line. The local accepted/submitted manuscript has LBNL repository framing instead. | Cite CPC metadata from the final version, not from the manuscript front matter. |
| Abstract | PDF page 1; MinerU abstract block | Both versions support the high-order and pseudo-spectral PML efficiency topic. The final abstract explicitly frames the systematic extension to arbitrary order and the infinite-order pseudo-spectral limit. | Final abstract wording is available for paper-level claims. |
| Section architecture | PDF pages 1--7; MinerU sections 1--5 | The final version formalizes numbering: PML subsection 2.1--2.3, reflection subsections 3.1--3.3, results, conclusion, acknowledgments, and appendices. The manuscript uses shorter all-caps headings and omits this final pagination/numbering structure. | Use final section numbers when navigating the published paper. |
| High-order/PSTD formula anchors | PDF page 3, Eqs. (2.8)--(2.13), Table 1; MinerU sections 2.3--2.4 | The final version contains the high-order stencil expression, Fornberg coefficients, and staggered-grid PSTD formulation. These are the relevant paper anchors for the existing PML/source map. | MinerU distortions in long display equations are not treated as formula evidence; the final PDF page is authoritative. |
| Reflection and results | PDF pages 3--7, sections 3--4, Figs. 1--7 | The final version adds numbered reflection subcases, numerical-simulation comparison, final figures, and full CPC pagination. | Paper reflection results do not prove that WarpX `C1`--`C25`, cleaning, Galilean, or RZ branches are identical. |
| Appendices | PDF pages 7--9, Appendices A--C | The publisher version contains the appendix derivations and summary that are absent from the seven-page accepted/submitted package. | Appendix formulas are available for paper reading, but no automatic one-to-one claim is made for current WarpX internals. |

## Resulting evidence boundary

The PML chapter may now distinguish the final CPC article from the accepted/submitted manuscript using direct final-version evidence. The remaining implementation boundary is unchanged: a paper formula, a source path, and a designated WarpX regression answer different questions and must not be collapsed into one claim.

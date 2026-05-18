# Books And Long-Form References To Locate Legally

These are important book-length references for the PIC book project. They are not downloaded here unless an authorized open PDF is available.

## Core PIC And Particle Simulation Books Still Missing Locally

- R. W. Hockney and J. W. Eastwood, *Computer Simulation Using Particles*.
- J. P. Verboncoeur, A. B. Langdon, and N. T. Gladd, classic PIC and plasma simulation references.
- R. W. Hockney, *The potential calculation and some applications* and related particle-mesh material.

## Core PIC And Particle Simulation Books Already Materialized

- C. K. Birdsall and A. B. Langdon, *Plasma Physics via Computer Simulation*.
  - Local project directory:
    - `references/02_books_lecture_notes/1985_BirdsallLangdon_Plasma_physics_via_computer_simulation/`
  - Note:
    - MinerU required page splitting because the original PDF exceeds 200 pages.

## Classic Article-Level PIC Foundations To Materialize Separately

- T. Tajima and J. M. Dawson, *Laser accelerator by plasma waves*.
- T. Tajima and J. M. Dawson, *Laser Electron-Accelerator*.
- J. M. Dawson, *Particle Simulation Of Plasmas*.

These Dawson references are not book-length items. If legal PDFs are found, they should go to article-specific directories under the topical `references/` tree instead of being mixed into `02_books_lecture_notes/`.

Current local-state note:

- `1979_TajimaDawson_Laser_Electron_Accelerator` and `1983_Dawson_Particle_simulation_of_plasmas` are already materialized in `references/03_pic_foundations/`.
- `TajimaDawson1982` (`Laser accelerator by plasma waves`) is still missing as a local PDF.
- `Yee 1966` is the next foundation-paper acquisition target after the current Dawson line:
  - title:
    - *Numerical Solution of Initial Boundary Value Problems Involving Maxwell's Equations in Isotropic Media*
  - venue:
    - *IEEE Transactions on Antennas and Propagation*
  - volume/issue/pages:
    - `14(3):302-307`
  - date:
    - `May 1966`
  - DOI:
    - `10.1109/TAP.1966.1138693`
  - current local-state boundary:
    - no matching PDF or MinerU output was found in `Zoteropaper`, `llm-for-zotero-mineru`, broader `Documents/`, `Desktop`, or `Downloads`
    - exact filename / identifier searches for `1138693`, `01138693`, the full title stem, and DOI string also returned no local hits
  - current web-evidence boundary:
    - metadata-level records confirmed on CiNii / ScienceOpen
    - CiNii exposes a historical IEEE PDF endpoint pattern:
      - `.../01138693.pdf?arnumber=1138693`
    - but no legally usable full-text PDF was obtained in this turn
- the next pusher-paper acquisition target after the current `Vay/Higuera` line is `Borisjcp73`:
  - title:
    - *Nonphysical Self Forces In Some Electromagnetic Plasma-Simulation Algorithms*
  - venue:
    - *Journal of Computational Physics*
  - date:
    - `1973`
  - DOI:
    - `10.1016/0021-9991(73)90174-5`
  - related early Boris-source line already indexed in `docs/literature-map.md`:
    - `BorisICNSP70`
      - *Proc. Fourth Conf. Num. Sim. Plasmas*
    - `Habericnsp73`
      - *Proc. Sixth Conf. Num. Sim. Plasmas*
  - current local-state boundary:
    - no matching full-text PDF or MinerU output was found in `Zoteropaper`, `llm-for-zotero-mineru`, broader `Documents/`, `Desktop`, or `Downloads`
    - current local hits are only derivative assets, not primary-source full text:
      - `Documents/tex/sgm1/sections/boris_method.tex`
      - `Documents/tex/sgm1/codes/boris_cpp.tex`
      - `Documents/program/warpx/warpx_and_depen/picsar-development/Doxygen/pages/latex_theory/Particle_pushers/Boris_pusher.tex`
      - WarpX / PICSAR source files such as `UpdateMomentumBoris.H` and `boris_2d.F90`
  - current workflow boundary:
    - because no primary-source PDF is currently available locally, this line cannot yet enter the MinerU-first paper workflow
- metadata now confirmed from official/project sources:
  - venue: *AIP Conference Proceedings*
  - volume/issue/pages: `91(1):69-93`
  - date: `Sep 1982`
  - DOI: `10.1063/1.33805`
- related-but-not-identical accessible note now identified:
  - FNAL conference PDF `p169.pdf`
  - title: *Laser accelerator by plasma waves for ultra-high energies*
  - author line: `T. Tajima`
  - boundary:
    - this is a related 1982 conference note by Tajima alone
    - it is not the same bibliographic item as `TajimaDawson1982`
- current local-state boundary:
  - no matching PDF or MinerU output was found in `Zoteropaper`, `llm-for-zotero-mineru`, broader `Documents/`, or `minerU/md_output`

## Article-Level Fallback Targets Around Hockney-Eastwood

If the full Hockney-Eastwood book remains unavailable locally, the next best primary sources are the article-level materials explicitly cited by Birdsall Chapter 13 and 14 for particle-mesh heating, fluctuation, and force-anisotropy claims:

- R. W. Hockney (1971)
  - 2d2v thermal-plasma long runs
  - `tau_s`, `tau_H`, `N_C`, optimum-path design
  - confirmed title/landing:
    - *Measurements of collision and heating times in a two-dimensional thermal computer plasma*
    - IBM Research publication page
    - DOI path indicated by the landing page: `10.1016/0021-9991(71)90032-5`
  - abstract-level quantitative claims already confirmed:
    - `tau_coll / tau_pe = n(\lambda_D^2 + W^2)` to about 20 percent
    - `\langle E^2 \rangle / 8\pi \div n m v_{th}^2 = 0.12 / n(\lambda_D^2 + W^2)`
    - optimum path `( \omega_{pe}\Delta t )_{opt} = min[ H / (2\lambda_D), 1 ]`
    - on that path `tau_H / tau_coll = K_2 / (H/\lambda_D)^2`
    - reported `K_2`: `2.1` (NGP), `6.4` (HNGP), `41` (CIC), `200` (HCIC)
- Hockney et al. (1974)
  - improved heating-time measurements
  - `K_4`, QPM, potential correction
  - confirmed title/DOI:
    - *Quiet High-Resolution Computer Models of a Plasma*
    - `10.1016/0021-9991(74)90010-2`
- Eastwood and Hockney (1974)
  - force anisotropy and particle-shape comparisons
  - NGP / CIC / QS 2d force figures
  - confirmed title/DOI:
    - *Shaping the force law in two-dimensional particle-mesh models*
    - `10.1016/0021-9991(74)90044-8`
- Abe et al. (1975)
  - heuristic self-heating estimate from `delta F`
- Peiravi and Birdsall (1978)
  - self-heating dependence on smoothing cutoff and weighting order

Current local-state note:

- These article-level fallback targets are cited in the current `Birdsall 1985` MinerU Markdown and Chinese notes.
- Current scans of `Zoteropaper`, `llm-for-zotero-mineru`, and broader `Documents/` did not find local PDFs or MinerU outputs for these targets.
- Web metadata cross-check has now confirmed at least three exact article identities/DOIs, so future materialization no longer depends on guessing titles from Birdsall’s prose.
- Current web-access boundary is still metadata/abstract oriented:
  - official landing pages and abstracts are reachable
  - a directly materialized local full-text PDF has not yet been established for these three targets
  - even the visible ScienceDirect PDF endpoint for `Quiet High-Resolution Computer Models of a Plasma`
    currently resolves, in this environment, to a download-preparation/browser-compatibility page rather than a usable local full-text PDF

## Plasma And Numerical Physics Background

- F. F. Chen, *Introduction to Plasma Physics and Controlled Fusion*.
- T. H. Stix, *Waves in Plasmas*.
- S. Jardin, *Computational Methods in Plasma Physics*.
- R. Dendy, *Plasma Physics: An Introductory Course*.

## Beam, Accelerator, And Laser-Plasma Context

- H. Wiedemann, *Particle Accelerator Physics*.
- A. Macchi, *A Superintense Laser-Plasma Interaction Theory Primer* and related review material.

## Handling Rule

- Use library access, official publisher access, author-posted PDFs, institutional repositories, arXiv, OSTI, or other authorized open-access sources.
- Do not download from shadow libraries or unauthorized mirrors.

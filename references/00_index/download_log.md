# Download Log

## Final State After Initial Seeding

- Total PDF files currently on disk: 35
- Total size of `references/`: about 162 MB
- PDF header validation: passed for all 35 files
- Index of actual files: `current_inventory.md`

## Counts By Category

- `01_reviews_surveys`: 7
- `02_books_lecture_notes`: 2
- `03_pic_foundations`: 6
- `04_particle_pushers_deposition_shapes`: 1
- `06_stability_filtering_nci`: 2
- `07_amr_parallel_hpc_gpu`: 2
- `08_boundaries_pml_geometry`: 1
- `09_multiphysics_collisions_ionization_qed`: 4
- `10_applications_laser_plasma_acceleration`: 1
- `11_codes_ecosystem_standards`: 3
- `12_hybrid_fluid_models`: 4
- `13_theses_dissertations`: 1
- `14_general_numerical_methods`: 1

## Run Notes

- First a larger mixed run queried WarpX `refs.bib` through OpenAlex/arXiv/direct PDF links. It was stopped because a few servers were slow, but already downloaded PDFs were kept.
- Then a smaller curated run downloaded open review articles, lecture notes, open theses, and arXiv papers.
- Some automatically placed files were manually reclassified into better topical folders.
- `manifest.jsonl` reflects the most recent scripted run, while `current_inventory.md` reflects the actual files currently on disk.

## Access Policy

- Only direct/open PDFs are downloaded.
- Paywalled or ambiguous records are not downloaded from unauthorized sources.
- Commercial books are tracked in `books_to_locate.md` for later legal access through libraries, publishers, author pages, institutional repositories, or other authorized routes.

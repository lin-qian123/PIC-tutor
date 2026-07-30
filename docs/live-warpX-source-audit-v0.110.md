# PIC-tutor live WarpX source scope audit

- status: `PASS`
- classification: `CURRENT_WARPX_CORE_CHAPTER_SOURCE_ANCHORS_VERIFIED_DIRTY_UNRELATED_PATHS_RECORDED`
- WarpX revision: `c311e49d4ffb19e39727182929c2f914cc7b776d`
- audited source/analysis anchors: `41`
- dirty worktree paths: `12`
- dirty paths intersecting audited anchors: `0`
- scope: Runs the Chapter 3A--8 representative source crosswalks at one Git revision. A dirty WarpX worktree is acceptable only when none of its paths intersects the explicit audited anchors; this is not a clean-tree assertion, a semantic equivalence proof, or a runtime physics regression.

## Crosswalks

| Chapter surface | Status | Classification |
|---|:---:|---|
| `chapter_3a` | `PASS` | `CHAPTER_3A_HISTORICAL_MODERN_MAPPING_SOURCE_ANCHORS_VERIFIED` |
| `chapter_4_boris` | `PASS` | `CURRENT_WARPX_SOURCE_GROUNDED_BORIS_CROSSWALK_HISTORICAL_PROCEEDINGS_FULL_TEXT_MISSING` |
| `chapter_5_deposition` | `PASS` | `CHAPTER_SOURCE_CROSSWALK_CURRENT_WARPX_ANCHORS_VERIFIED` |
| `chapter_6_field_solver` | `PASS` | `CHAPTER_6_FIELDSOLVER_SOURCE_ANCHORS_VERIFIED` |
| `chapter_7_boundary_amr` | `PASS` | `CHAPTER_7_BOUNDARY_AMR_SOURCE_ANCHORS_VERIFIED` |
| `chapter_8_diagnostics` | `PASS` | `CHAPTER_8_DIAGNOSTICS_SOURCE_ANCHORS_VERIFIED` |

## Dirty WarpX paths

- ` M Docs/source/usage/parameters.rst`
- ` M Docs/source/usage/workflows.rst`
- `D  Simulation/particle_work_validation/designs/2026-07-28-extended-cpu-validation-design.md`
- `D  Simulation/particle_work_validation/designs/2026-07-28-extended-cpu-validation-implementation-plan.md`
- `D  Simulation/particle_work_validation/extended/AGENTS.md`
- `D  Simulation/particle_work_validation/extended/README.md`
- `D  Simulation/particle_work_validation/extended/TODO.md`
- ` M Source/Laser/LaserProfiles.H`
- ` M Source/Laser/LaserProfilesImpl/CMakeLists.txt`
- ` M Source/Laser/LaserProfilesImpl/Make.package`
- `?? Docs/source/usage/workflows/flying_focus_laser.rst`
- `?? Source/Laser/LaserProfilesImpl/LaserProfileFlyingFocus.cpp`

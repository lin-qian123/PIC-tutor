# Chapter 4 Pusher Validation Ladder

Classification: `SOURCE_GROUNDED_PUSHER_VALIDATION_LADDER_READER_CARD`.

Result: PASS.

## Source Routes

- `Source/Particles/Pusher/PushSelector.H`
- `Source/Particles/Pusher/UpdatePosition.H`
- `Source/Particles/PhotonParticleContainer.cpp`
- `Examples/Tests/particle_pusher/{inputs_test_3d_particle_pusher,CMakeLists.txt,analysis.py}`
- `Examples/Tests/single_particle/{inputs_test_1d_synchronize_velocity,CMakeLists.txt,analysis_synchronize_velocity.py}`
- `Examples/Tests/photon_pusher/{inputs_test_3d_photon_pusher,CMakeLists.txt,analysis.py}`
- `Examples/Tests/larmor/CMakeLists.txt`

## Checks

- `reader_card_present`: `PASS`
- `massive_pusher_contract`: `PASS`
- `diagnostic_time_contract`: `PASS`
- `photon_contract`: `PASS`
- `source_and_checksum_boundaries`: `PASS`

## Scope

- No WarpX build or runtime execution is performed by this audit.
- The card separates massive-pusher, diagnostic-time-level, massless-photon, and checksum-only evidence.
- It does not establish a general pusher accuracy ranking, deposition correctness, or self-consistent field validity.

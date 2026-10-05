# CLAUDE STATE SERIALIZATION

**Timestamp:** 2026-10-04T20:25Z **Phase:** Planning

Pointer hand-off: `Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet` (PRIVATE, greg's own research repository). Not part of the Beethoven build; the project reads it and never edits it without greg's explicit order. Project-wide state: `/mnt/project-files/state/claude_context.md`.

## 1. Primary Objective

Point a new session at greg's spine work: FluoroCap and C-arm vertebral-level detection, frame linking, counting from the sacrum, transitional (L6/T13) spines, and the original nnU-Net CT pipeline. The engine's first study (vertebral-body detection on real fluoroscopy under domain shift; BUILD_PLAN section 16, `plan/SPINE_FIRST_STUDY.md`) draws on its measured numbers, its corpus list (`tools/corpus_manifold.py`) and its gates.

## 2. Architectural Decisions & Constraints

- Read-only from this project; no thread owns it. Default branch `L6_Class` (465bec6, 2026-09-27T21:17Z) stays private and is never pushed to a public repository; `master` (50b209f) is fully contained in it; there is no `main`.
- Never read `docs/CREDENTIALS_SETUP.md` or `tools/fluorocap_creds.py` contents, nor the home tokens (`.hf_org_token`, `.hf_osc_token`, `.kaggle`, `.wandb`). Patient data (DICOM headers, image bytes) stays on the grid.
- The repository's own CLAUDE.md governs work there: start at `docs/PIPELINE_RESUME.md`, trust no status written in prose (compute it with `tools/pipeline_state.py` on the grid), and start physics work at `docs/HANDOFF_PHYSICS.md`. Never run `make physics-fresh` (it deletes outputs on the grid) or `tools/claims_check.py --write`.

## 3. Files Modified & State

| File Path | Status | Key Modifications / Purpose |
| --- | --- | --- |
| docs/PIPELINE_RESUME.md | Complete | The resume page: pipeline shape, traps, the 27-class alphabet, splitting by patient |
| docs/RESUME_2026-09-22_PM.md | Complete | Running log; newest entry 2026-09-27 18:05 EDT, its jobs unverified since |
| docs/ruleclass/PREREG_rules.md | Pending | Draft v1 of the transitional screen; nothing is scored before greg freezes it |
| spine_data_review/PROTOCOL.md | Pending | Section 7.4 (lines 458-471) names an LLM-assisted screening step; relayed under the no-key sweep, only greg may edit it |
| .github/workflows/ci.yml | Broken | Triggers on `main`, which does not exist, so CI has never run |

## 4. Completed Milestones

1. Checked read-only in a cloud session at about 18:45Z: `python3 tools/collect_physics_results.py --no-fetch --check` exited 0, "all 10 headline numbers match docs/PHYSICS_LINKING.md"; `python3 tools/claims_check.py` gave "54 claims: 24 ok, 0 drifted, 30 missing" (the 30 point at grid paths).
2. `plan/IMAGING_SOURCES.md` (210 roots in five tiers) was built from this repository at 465bec6 by the replan thread (ledger 02:49Z).

## 5. Active Blockers & Errors

- The first study is blocked by Linear BEE-181 questions 1, 4 and 6 and the imaging migration by BEE-165 (sources, destination, PHI statement); both are greg's decisions.
- Cloud sessions cannot reach the grid, so the pipeline state and the jobs listed on 2026-09-27 are not yet measured. Three files fail to parse under Python 3.11, though all three parse under 3.12: `tools/compare_ablations.py` and `tools/eval_shortcut_controls.py`, inside the `tools/*.py` glob CI's syntax step checks, and `spine_data_review/sdr/quality.py`, outside it.

## 6. Immediate Next Actions (Hydration Directives)

1. Run `git -C <checkout> fetch origin --prune` and confirm `L6_Class` is 465bec6 and the repository is still private; never push, commit or edit without greg's order.
2. Read its CLAUDE.md, `docs/PIPELINE_RESUME.md` and `docs/HANDOFF_PHYSICS.md` section 1 before any study work, and re-run the two offline checks above read-only.
3. Check BEE-181 and BEE-165 for greg's answers before planning the engine's first study, and ask greg or a grid worker for `tools/pipeline_state.py` output.

# CLAUDE STATE SERIALIZATION

**Timestamp:** 2026-10-04T20:25Z **Phase:** Implementation

Repository hand-off: `OpenSpineConsortium/beethoven-research` (private), the research pipeline of the Beethoven engine. Project-wide state, rules and greg's open steps: `/mnt/project-files/state/claude_context.md`; how to use this file: `/mnt/project-files/state/HYDRATE.md`. Checked against GitHub at 20:21Z and by an independent checker; whatever says "not yet measured" or "unverified" was not checked.

## 1. Primary Objective

Hold what the engine computes and how a result is shown to be sound: REFORMS (run hashing, the clean-tree gate, the split level per corpus, bootstrapped confidence intervals, energy), CLAIM, the studies (the spine study first, BUILD_PLAN section 16), later the medical calibration (Goal 6) and the publication engine behind a human click (Goal 7). greg's card of 13:19Z kept the pipeline here. Since PR #4 (merged 19:34Z) main is the slim pipeline: the pinned copy of beethoven-qa and one module, the patient-level split check.

## 2. Architectural Decisions & Constraints

- **Dependence runs one way:** beethoven-qa <- beethoven-agents <- beethoven-research. Research may use both and nothing imports research. The gate, the guard, the image and bee now live in qa and agents; research never takes them back.
- **Never here:** an API key, a gateway or usage credits; a Claude credential; patient identifiers. Split-check group labels must be study-local pseudonyms, never patient IDs (no medical record number, name, accession number or DICOM PatientID), because every failure of the check prints the groups it was given. Patient data stays on the grid; what may identify a patient is greg's PHI statement (Linear BEE-165).
- **The check refuses blank or padded group labels:** `"P001"` and `"P001 "` would otherwise be two groups, and a leaking pair would pass as disjoint (`src/beethoven_research/splits.py` docstring).
- The definition of done is beethoven-qa's: contracts on every public function, CrossHair and Z3 proof within 20 s per condition, `vendor-check` in the gate. `[tool.beethoven-qa.unproven]` in `pyproject.toml` is empty. Never edit `vendor/beethoven-qa/` or the four kit files here; change them in beethoven-qa, release, and re-vendor.
- The gate runs before every push (`.githooks/pre-push`; `core.hooksPath` is unset in a multi-repository thread, so run `pixi run hooks` first and put `~/.pixi/bin` on PATH). PRs open ready, never draft; `automerge.yml` arms auto-merge and ruleset 24440691 decides.
- Every unit of work appends a row to `/mnt/project-files/ledger/LEDGER.md`. Nothing container-related runs on a laptop, the login node or a cloud session.
- Owner thread: "Three-repo separation" (`cmsg_01JbwQwHoYeBWptjPB5c6u8mTY4EBQjdtHsPXP8iwJoc9c`, branch `claude/three-repo-separation-upobqe`), done at 19:47Z after greg's beethoven-qa release v1.0.0.

## 3. Files Modified & State

| File Path | Status | Key Modifications / Purpose |
| --- | --- | --- |
| src/beethoven_research/splits.py | Complete | `SplitLevel` (patient, study, cadaver, CT source volume), `Split` (pydantic boundary, input hidden in errors), `shared_groups`, `disjoint` under beartype and icontract (Linear BEE-116) |
| tests/test_splits.py | Complete | The split check's tests, under typeguard's import hook (`tests/conftest.py`) |
| vendor/beethoven-qa/ | Complete | Pinned copy: ORIGIN `ref: v1.0.0`, commit 16415b40e6bb, 22 files plus ORIGIN; matches the release file for file (three-repo thread, 19:47Z) |
| .github/rulesets/main.json | Complete | Requires only `gate (lock → lint, typecheck, tests, CrossHair/Z3, vendor-check)`; equals the live ruleset 24440691 (updated 19:34:23Z) |
| .github/workflows/ci.yml | Complete | The consumer gate lane; the image lane moved to beethoven-agents |
| pixi.toml, pixi.lock | Complete | linux-64 only; every linux-64 record unchanged by the slimming (ledger 18:55Z) |
| CLAUDE.md, README.md | Complete | Rewritten for the pipeline (253 lines), with "Where the rest went" |
| pyproject.toml | Complete | Package `beethoven-research` 0.0.0, `[tool.beethoven-qa]` package `beethoven_research`, 20 s per condition |

## 4. Completed Milestones

1. Skeleton PR #1 merged by greg 2026-10-04T03:29:44Z (772df94); PR #2 merged by auto-merge 03:44:46Z (33ce108), the project's first merge decided by tests alone; bee, PR #3, merged by auto-merge 07:06:01Z (b7b8650), later moved to beethoven-agents.
2. PR #4 (head c25b443; 72 files, +4318/-10367; adversarial review confirmed 10 of 13 findings and all 10 are fixed; three deliberately wrong copies of the module each gave CrossHair a counterexample) merged by greg's hand 19:34:13Z as 8dd5be2, bypassing the old rule that named checks the PR had renamed or moved.
3. greg published beethoven-qa release v1.0.0 on 16415b4 at 19:45:29Z, the release this copy's ORIGIN names (BEE-195 Done 19:47Z).
4. The merge applied the new rule: `rulesets.yml` (check run `apply`, success 19:34:26Z) updated ruleset 24440691 at 19:34:23Z; the `vendor-check` gate passed on main 8dd5be2 at 19:36:09Z. Research PRs now merge themselves on green, like qa and agents. Linear BEE-197 Done at 19:34:52Z (three-repo thread).

## 5. Active Blockers & Errors

- Wiring the split check into a run waits on BEE-165 (PHI statement, data location) and BEE-181 (first-study decisions 1, 4 and 6).
- Not yet measured: any of this repository on the grid; the gate's wall time on a grid node; how Claude Code reports the remaining usage window (BEE-121, agents').

## 6. Immediate Next Actions (Hydration Directives)

1. Run `git -C <checkout> fetch origin --prune --tags` and `gh api "repos/OpenSpineConsortium/beethoven-research/pulls?state=all&per_page=5"`; confirm main is 8dd5be2 or later and that `gh api repos/OpenSpineConsortium/beethoven-research/rulesets/24440691` still requires only the `vendor-check` gate name.
2. Run `pixi run --locked vendor-check`; to re-prove the copy against the release itself, run beethoven-qa's own `vendor-check --root <this checkout> --source <qa checkout at v1.0.0>` from qa's environment (qa `docs/CONSUMING.md`).
3. Before any push: install pixi 0.81.0, `pixi install --locked`, `pixi run hooks`, export `~/.pixi/bin` onto PATH, then `pixi run --locked gate`.
4. Next research work is Goal 2 (BEE-111 to BEE-115: Run ID, clean-tree gate, confidence intervals, CodeCarbon, `reforms.json`), each module clearing the qa gate; plan it with the owner thread and the replan thread's BUILD_PLAN, and append a ledger row per unit of work.

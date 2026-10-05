# CLAUDE STATE SERIALIZATION

**Timestamp:** 2026-10-04T20:25Z **Phase:** Implementation

Repository hand-off: `OpenSpineConsortium/beethoven-qa` (private), how code for the Beethoven engine is written and proven. Project-wide state, rules and greg's open steps: `/mnt/project-files/state/claude_context.md`; how to use this file: `/mnt/project-files/state/HYDRATE.md`. Checked against GitHub at 20:21Z and by an independent checker; whatever says "not yet measured" or "unverified" was not checked.

## 1. Primary Objective

Own Goal 1 for every engine repository: the definition of done, the contract decorators (`beethoven_qa.contracts`), the CrossHair and Z3 gate as a command (`python -m beethoven_qa gate`), the pinned-copy commands (`vendor`, `vendor-check`), the four-file repository kit every consumer carries byte for byte, and the Claude Code plugin (4 skills, the `stream` agent, the workflows `gate-until-green`, `verify-module`, `improve-module`). Release 1.0.0 is on main; schema-aligned parsing (G1-4, BEE-108) and the full SpecPylot loop (BEE-109) are still to build here.

## 2. Architectural Decisions & Constraints

- **Depends on nothing of ours.** beethoven-agents and beethoven-research take it as a pinned copy at `vendor/beethoven-qa/` with an `ORIGIN` record; a change here that needs either of them is in the wrong repository (greg's split, 04:52Z; REPO_SPLIT.md).
- The kit (`.githooks/pre-push`, `.github/workflows/automerge.yml`, `.github/workflows/rulesets.yml`, `.claude/hooks/session-start.sh`) changes only here and reaches consumers through `vendor --kit`.
- Never skip, disable or quarantine a test, loosen a symbolic bound, remove a contract, add a `# crosshair:` directive, exempt a module holding logic, or list under `[tool.beethoven-qa.unproven]` a function CrossHair can run, to get green.
- One integer version in `pyproject.toml`, `beethoven_qa.__version__`, the plugin manifest and the release tag (1.0.0 today; `pixi.toml`'s workspace version 0.0.0 is outside that rule).
- Every pixi command with `--locked`; never commit a lockfile the tool did not produce.
- No API key, no usage credits, no credential reads; the only secret any workflow names is the organisation's `RULESETS_TOKEN`, read in `rulesets.yml` alone.
- Merging: PRs open ready, `automerge.yml` arms auto-merge, ruleset 24457138 decides; a session never pushes a tag (the proxy refuses it).
- Owner thread: "Three-repo separation" (`cmsg_01JbwQwHoYeBWptjPB5c6u8mTY4EBQjdtHsPXP8iwJoc9c`), done at 19:47Z.

## 3. Files Modified & State

| File Path | Status | Key Modifications / Purpose |
| --- | --- | --- |
| src/beethoven_qa/gate.py | Complete | Check 1 (every public function contracted, nothing hidden from CrossHair) and check 2 (CrossHair per target, as many processes as cores) |
| src/beethoven_qa/vendor.py | Complete | `vendor --into <repo> [--kit]`, `vendor-check [--source]`, read from the release commit's own objects |
| src/beethoven_qa/contracts.py, example.py, __main__.py | Complete | Decorators; the worked example that clears steps 1 to 4; the command line |
| pyproject.toml, src/beethoven_qa/__init__.py, plugin/.claude-plugin/plugin.json | Complete | Version 1.0.0 |
| pixi.toml, pixi.lock | Complete | linux-64; python 3.11.16, icontract 2.7.3, pydantic 2.13.5, beartype 0.22.9, typeguard 4.6.0, crosshair_tool 0.0.111, z3_solver 5.1.0.0 |
| .github/rulesets/main.json | Complete | Matches live ruleset 24457138: checks `gate (lock → lint, typecheck, tests, CrossHair/Z3)` and `plugin (validate, workflow scripts)` |
| tools/check_workflows.mjs, tools/check_workflows.test.mjs | Complete | CI's check of the workflow scripts against the runtime's rules |
| CLAUDE.md | Pending | Lines 189-191 still say the gate is not measured on a GitHub runner; it has been (4 min 10 s, 4 min 45 s) |

## 4. Completed Milestones

1. PR #1 (the whole repository) merged by greg 2026-10-04T13:42:24Z (445dc1c) after a first adversarial review fixed 46 findings, each with a failing-first test; the git 2.55 `git add -u` refusal on the runner was fixed in 20cf2ec.
2. Ruleset 24457138 active since 13:57:48Z, applied by `rulesets.yml` once greg widened `RULESETS_TOKEN` to all repositories.
3. PR #2 (second adversarial review, 21 findings fixed with failing-first tests) merged itself 15:46:18Z as 16415b4; CI on head f0c0254: gate 4 min 45 s, plugin 11 s; main's tree equals f0c0254's.
4. Release v1.0.0 published by greg 2026-10-04T19:45:29Z on 16415b40e6bb (`git ls-remote --tags` shows `refs/tags/v1.0.0` at that commit); Linear BEE-195 Done 19:47Z. Sessions cannot create tags ("HTTP 403 on refs/tags and on the git/tags API path", ledger 15:55Z), so every later release tag is greg's hand step too.
5. Consumed: beethoven-agents main 0de7913 and beethoven-research main 8dd5be2 (PR #4, merged by greg 19:34Z) carry the pinned copy of 16415b40e6bb (22 files plus ORIGIN); the owner thread found both equal to the release file for file at 19:47Z.

## 5. Active Blockers & Errors

- None on GitHub: no PR is open and v1.0.0 is released. No CI run exists on main 16415b4 itself (an auto-merge push by GitHub Actions starts no workflow), but its tree is the same as f0c0254's, which passed gate and plugin.
- Not yet measured: the gate's wall time on a grid node; whether the managed-settings `directory` marketplace loads the plugin in a `-p` step or a master in the agents image; whether a `.claude/skills` plugin loads in a cloud project thread; the plugin from the private marketplace on greg's laptop; any of the three workflows against a real failure; whether the `ultracode` settings key makes a `-p` step plan workflows.
- In this cloud environment pixi is not installed and `core.hooksPath` is unset in a multi-repository thread; the pre-push hook also refuses a dirty or untracked tree.

## 6. Immediate Next Actions (Hydration Directives)

1. Run `git -C <checkout> fetch origin --prune --tags`; confirm main is 16415b4 or later and `v1.0.0` resolves to 16415b40e6bb; a session never pushes a tag, so a later release is greg's Releases-page step.
2. Install pixi 0.81.0 as `.claude/hooks/session-start.sh` does, then `pixi install --locked`, `git config core.hooksPath .githooks` and `pixi run --locked gate` to re-establish a green baseline.
3. Next build items here: schema-aligned parsing (BEE-108) and the SpecPylot loop (BEE-109); refresh CLAUDE.md's measured-timings paragraph in the same kind of PR, opened ready, merged by the required checks.
4. Append a row to `/mnt/project-files/ledger/LEDGER.md` per unit of work; a new release means `vendor --into <consumer> --kit` in agents and research, each through its own PR.

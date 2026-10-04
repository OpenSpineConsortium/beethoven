# CLAUDE STATE SERIALIZATION

**Timestamp:** 2026-10-04T20:25Z **Phase:** Implementation

Repository hand-off: `OpenSpineConsortium/beethoven-agents` (private), how agents run on the grid for the Beethoven engine. Project-wide state, rules and greg's open steps: `/mnt/project-files/state/claude_context.md`; how to use this file: `/mnt/project-files/state/HYDRATE.md`. Checked against GitHub at 20:21Z and by an independent checker; whatever says "not yet measured" or "unverified" was not checked.

## 1. Primary Objective

Own the nested agentic framework: the hermetic Apptainer image every engine job runs in (`containers/`), its managed settings and the PreToolUse guard (`src/beethoven_agents/guard.py`), greg's several accounts and the account switcher and hand-off tool `bee` (`src/beethoven_agents/bee/`), and next the super-master lease, the session registry, the message bus, the reaper and the Metaflow loop of headless `claude -p` steps as Slurm jobs (decision D3: Metaflow with outerbounds/metaflow-slurm, a plain sbatch adapter first).

## 2. Architectural Decisions & Constraints

- **Middle of the split:** takes beethoven-qa only as the pinned copy `vendor/beethoven-qa/` (ORIGIN: `ref: v1.0.0`, commit 16415b40e6bb, 22 files) and imports nothing of beethoven-research. Never edit the pinned copy or the four kit files here.
- **Accounts (D4, greg 02:30Z and 03:23Z):** several of greg's own accounts at once, one sign-in directory each at `$HOME/.beethoven/accounts/<label>/claude` selected by `CLAUDE_CONFIG_DIR` (`$HOME/.beethoven/claude` is the account `main`, by a link); one master job per account; one super-master lease; the hand-off file is the first carrier, the transcript `--resume <path> --fork-session` (read-only) the second: already built for the interactive switch (`bee continue --fork`, `bee-grid.sh continue --fork`), it stays the second choice, and the lease's hand-off will not use it until probe M13 is on record. `accounts.json` holds label, path, enabled and order and nothing from inside a directory; nothing copies, moves or links a credential.
- **Never:** an API key (the image unsets `ANTHROPIC_API_KEY` and `ANTHROPIC_AUTH_TOKEN`; the guard refuses a line that sets them); usage credits; deleting outside a run's own directories and node-local temp; container, scheduler or Claude Code work outside a Slurm job on a compute node.
- Gate before every push (`pixi run --locked gate`: lint, typecheck, tests, CrossHair and Z3 at 20 s per condition, `vendor-check`); a new `[tool.beethoven-qa.unproven]` entry is a person's decision; `# crosshair:` comments fail the gate.
- Merging: PRs open ready, `automerge.yml` arms auto-merge (qa, agents and, since 19:34Z, research all merge themselves on green), ruleset 24460184 requires `gate (lock → lint, typecheck, tests, CrossHair/Z3, vendor-check)` and `image (apptainer build)`.
- Teams need an interactive lead (a `-p` step never leads one); one team per session; no orphans (registry, heartbeats, a reaper cancelling only our own job ids). See `docs/PARALLEL.md`.
- Owner thread: "Three-repo separation" (`cmsg_01JbwQwHoYeBWptjPB5c6u8mTY4EBQjdtHsPXP8iwJoc9c`); bee's design came from the finished "Seamless account switching" thread.

## 3. Files Modified & State

| File Path | Status | Key Modifications / Purpose |
| --- | --- | --- |
| containers/claude-verify.def | Complete | Ubuntu 24.04, Node 22, Claude Code (npm, unpinned; CI got 2.1.289), pixi 0.81.0 environment, managed settings, guard, qa plugin at `/opt/beethoven-qa` |
| containers/build.sh | Complete | Builds the `.sif` with `--fakeroot` on a compute node and writes `<name>.digest`; no digest committed yet |
| containers/managed-settings.json | Complete | Deny rules, `allowManagedHooksOnly`, spawn depth 1, the guard hook, the qa marketplace |
| src/beethoven_agents/guard.py | Complete | The PreToolUse guard: refuses recursive or forced deletes anywhere and any delete or write outside the project, the run directory and node temp; anything naming the sign-in directory, `CLAUDE_CONFIG_DIR` or `.credentials.json`; any line naming the key variables; `claude setup-token`, `claude auth login` and `logout`, `claude project purge` |
| src/beethoven_agents/bee/ | Complete | accounts.py, handoff.py (the six-section hand-off this file follows), cli.py, bee-grid.sh; lease (BEE-189) not built |
| docs/bee/RUNBOOK.md | Complete | greg's steps: laptop L1-L5, grid G0-G4, probe M13 commands |
| docs/ACCOUNTS.md, docs/PARALLEL.md, docs/bee/STATE_HANDOFF.md | Complete | D4 design; parallel work; what bee took from greg's "Claude CLI State Management" guide and what it refused |
| pyproject.toml | Complete | `[tool.beethoven-qa]` and 25 `unproven` entries with reasons; package version 0.0.0 although PR #1's title says 1.0.0 |

## 4. Completed Milestones

1. PR #1 ("beethoven-agents 1.0.0: the image, the guard, accounts and bee, on beethoven-qa v1.0.0", head 962c532) merged by greg 2026-10-04T16:15:30Z as 0de7913; ruleset 24460184 created by `rulesets.yml` at 16:15:42Z.
2. CI green on the PR head and on main: gate 9 min 26 s, image 2 min 5 s (run 37214910374); ledger 15:55Z and 16:17Z count 277 tests and 34 CrossHair targets, no counterexample; the counts come from the owner thread's own gate run on 962c532 before the push, not from CI's log, which a cloud session cannot fetch (CI shows only pass and the job times).
3. The image recipe builds and passes its smoke test on a GitHub runner (apptainer 1.3.6, Claude Code 2.1.289); the runner's image is discarded.
4. bee's 53 `# crosshair:` comments replaced by 25 listed functions with reasons (ledger 07:33Z, landed in PR #1). Separately, Linear BEE-196 (the switch to the vendored beethoven-qa copy, `vendor-check` before the gate) Done 18:53Z.

## 5. Active Blockers & Errors

- The image has not been built on the grid and no digest is committed (`containers/README.md`: "No grid build yet and no committed digest"; Linear BEE-103 In Progress). Runbook G0: "The launcher's claude-node22 image has no engine environment, so bee cannot run in it."
- Not built: lease (BEE-189), registry and reaper (BEE-187), bus (BEE-186), the engine's per-account usage reading for `-p` steps (BEE-188, Backlog; bee's interactive switch already applies the 90 % threshold to its status-line readings), masters and satellites (BEE-190), Metaflow (not yet in `pixi.toml`).
- Not yet measured: bee-grid.sh under the grid's bash 4.2 and apptainer 1.2.2; status-line `rate_limits` on greg's plans on the grid; probe M13; how a `-p` step reports the remaining window (BEE-121); probes M1 to M12; whether the qa plugin loads in the image; whether Claude Code's sandbox nests in unprivileged Apptainer.
- Linear BEE-185 and BEE-189 still say transcripts never cross directories; D4 (03:23Z) allows the read-only fork. The replan thread owns that wording.

## 6. Immediate Next Actions (Hydration Directives)

1. Run `git -C <checkout> fetch origin --prune --tags` and `gh api "repos/OpenSpineConsortium/beethoven-agents/pulls?state=all"`; confirm main is 0de7913 and read CLAUDE.md, `docs/bee/RUNBOOK.md` and `docs/ACCOUNTS.md`.
2. Before any push: install pixi 0.81.0, `pixi install --locked`, `pixi run hooks`, export `~/.pixi/bin` onto PATH, then `pixi run --locked gate`; open PRs ready and let ruleset 24460184 decide.
3. When greg has a compute node: walk runbook G0 (image build in a Slurm job, digest committed by PR; BEE-103 closes once that `.sif` also runs the verification stack and `claude -p` on a compute node), then G1 to G4 and probe M13, recording results in `docs/bee/STATE_HANDOFF.md` and `docs/ACCOUNTS.md` section 9.
4. Build the lease (BEE-189), registry and reaper (BEE-187) and bus (BEE-186) under `src/beethoven_agents/`, each clearing the qa gate; first ask the replan thread to reconcile BEE-185 and BEE-189 with D4's fork decision; append a ledger row per unit of work.

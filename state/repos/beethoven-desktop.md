# CLAUDE STATE SERIALIZATION

**Timestamp:** 2026-10-04T21:25Z **Phase:** Implementation

Repository hand-off: `OpenSpineConsortium/beethoven-desktop` (private), Beethoven for Claude Desktop and Claude Code. Project-wide state, rules and greg's open steps: `/mnt/project-files/state/claude_context.md`; how to use this file: `/mnt/project-files/state/HYDRATE.md`. Checked against GitHub at 20:32Z (main bc75c09, branch `claude/project-thread-fx3wkp` still d014a82, no open PR) and earlier by an independent checker; whatever says "not yet measured" or "unverified" was not checked.

## 1. Primary Objective

Keep the desktop edition: one dependency-free local MCP server (`src/`, twelve tools) packaged as a Claude Desktop extension (`bundle/manifest.json`, a `.mcpb`) and as a Claude Code plugin (`plugin/.claude-plugin/plugin.json`), reaching the student's grid worker over the student's own ssh sign-in and only through hpcworker's gate verbs plus read-only sftp. It is a prototype for greg and the lab, not offered to students, and has never run against the real grid or in a real Claude Desktop.

## 2. Architectural Decisions & Constraints

- **Never:** a Claude credential (workers start with `--login never`); an API key, key helper, gateway or provider route (`npm run forbidden`, `scripts/forbidden.mjs`, refuses them in the shipped code except where they are stripped); usage credits; a secret in a tool schema, `user_config`, argv, log or file (the grid password and one-time code go only into ssh's own prompt in a visible terminal; no askpass, sshpass or expect).
- No network of its own and no remote code: Node's own modules only, no `fetch`, sockets, `eval` or run-time dependency; it starts only `ssh`, `ssh-keyscan`, the terminal and the link opener.
- Grid etiquette: only the gate's verbs (`version`, `status`, `connect … chain|no-chain`, `stop`, `read … progress.log`) plus sftp reads; status, start and stop at most once a minute. Never suggest adding the grid to Claude Code Desktop's own SSH (it cannot run on CentOS 7, glibc 2.17).
- Nothing deleted, here or on the grid; workspace reads stay inside `<state_dir>/workspaces/<name>`.
- One integer version in `package.json`, both manifests and `src/version.ts` (1.0.0); `scripts/build.mjs` checks it.
- Profiles are hpcworker's, vendored as data (`bash profiles/pull.sh`); `src/contract.ts` mirrors hpcworker's V11 and V12 contracts.
- Merging: PRs open ready, `automerge.yml` arms auto-merge, ruleset 24440600 decides (three CI job names); laptop checks never hold a merge.
- **beethoven-base (greg, 20:04Z; design 20:58Z):** the code shared with the browser and VS Code editions moves to a new repository, and this edition carries it as a pinned copy in `src/base`, checked against an ORIGIN record with no secret (no fetch, no read token); it takes base v1.0.0 as its 2.0.0, the first edition to do so. A critique found that base as specified would turn this repository's `forbidden.mjs` red, not yet resolved. greg created the repository at 20:25Z; the survey and design are in `/mnt/project-files/staging/desktop-thread/`; nothing has moved yet (`repos/beethoven-base.md`).
- Owner thread: "Build the Claude Desktop ssh plugin" (`cmsg_01JbwQwHoYeBWptjPB5c6u8m3KSccv8f9KZdoYiLkxZons`, branch `claude/project-thread-fx3wkp`), which also owns beethoven-vscode and, for the no-key sweep and the signed install, hpcworker and beethoven-extension. At 20:27Z it saved what GitHub does not hold for those repositories in `/mnt/project-files/staging/desktop-thread/` (README there); nothing of this repository's is in it.

## 3. Files Modified & State

| File Path | Status | Key Modifications / Purpose |
| --- | --- | --- |
| src/tools.ts | Complete | The twelve tools, `account_list` to `open_in_claude` |
| src/ssh.ts, src/sftp.ts, src/grid.ts | Complete | ssh argv and the kept sign-in; read-only SFTP v3 client; the gate verbs and their once-a-minute floors |
| src/accounts.ts | Complete | `account_list`: reads bee's `accounts.json` and usage files only; its comment still places bee in beethoven-research |
| src/contract.ts | Pending | `FAIL_CODES` (line 177) lacks framework 17's `signin-billed` and `signin-method` |
| scripts/forbidden.mjs | Complete | The posture check, there since 1.0.0 (PR #1); PR #4 added every route to an API key |
| docs/LAPTOP_CHECKS.md | Pending | 15 real-machine checks for greg, each "Outcome: not yet measured" |
| docs/DESIGN.md, docs/EDITIONS.md | Complete | Design, what it never does, before-students gates; the three editions compared |
| .github/workflows/automerge.yml, rulesets.yml, .github/rulesets/main.json | Complete | The three files greg copies into hpcworker and beethoven-extension, with the check names changed per repository |

## 4. Completed Milestones

1. PR #1 (1.0.0) merged 2026-10-04T02:31:12Z (d60c0b2); PR #2 (worker_list, Windows ssh options) 03:17:40Z (dbc0fb1). Both show `merged_by` greg with auto-merge off; the thread acts through greg's account, so GitHub cannot tell who clicked.
2. Ruleset 24440600 active since 03:12:31Z; `RULESETS_TOKEN` proven by dispatch run 37175304237.
3. PR #3 (`account_list`) merged itself 07:39:03Z; ledger 07:50Z: 66 tests, rows identical to `bee account list --json` on a four-account fixture.
4. PR #4 (no API key anywhere: `forbidden.mjs`) merged itself 15:36:57Z as bc75c09, all three required checks green on d014a82; ledger 15:35Z says 70 tests, but the PR #4 tree holds 68 (vitest counts 68; PR #3 had 66). Re-run at 19:03Z on a copy of main without sshd: forbidden "15 files clean", `tsc` clean, vitest 39 passed and 29 skipped, the `.mcpb` packed and validated.

## 5. Active Blockers & Errors

- None on GitHub: no PR is open, and `claude/project-thread-fx3wkp` equals the merged d014a82. main bc75c09 has no CI run of its own (a merge by github-actions starts no push run); its tree is d014a82's, whose three required checks passed, and the 19:03Z local re-run passed.
- Not yet measured: all 15 laptop checks ("Nothing here has run against the real grid yet", README.md:17); the desktop edition against framework 17's real gate (recorded runs used framework 16); whether `BEE_REGISTRY_DIR` reaches the Desktop extension's environment.
- Stale text: `docs/DESIGN.md:161` and `src/accounts.ts:2` place bee in beethoven-research, and `CLAUDE.md:37` names beethoven-research as the engine that picks a job's sign-in and hands the lead between accounts; both belong to beethoven-agents (`src/beethoven_agents/bee/`), and research main 8dd5be2 (PR #4, merged 19:34Z) no longer carries bee.
- Linear BEE-155 and BEE-156 still read In Review although PRs #1 and #2 merged.
- Waiting on greg: keep or revert PR #1 (unanswered); laptop checks 1 to 15; D6 (BEE-158, how the edition reaches approved students); before students, LICENSE.txt and PRIVACY.md must name this edition and the BEE-157 posture review needs a reader other than its author.

## 6. Immediate Next Actions (Hydration Directives)

1. Run `git -C <checkout> fetch origin --prune`, then `npm ci` (it sets `core.hooksPath`) and `npm run gate`; without sshd the ssh tests skip, and CI (`BD_REQUIRE_LAB=1`) is the authority.
2. Bring `src/contract.ts` `FAIL_CODES` up to framework 17 (`signin-billed`, `signin-method`, hpcworker `docs/V11_CONTRACT.md:64-65`) with a test, then run `HPCWORKER_DIR=../hpcworker npm test` against hpcworker main 20e2e97 on a machine with sshd.
3. Correct the bee location (research PR #4 merged 19:34Z) in `CLAUDE.md:37`, `docs/DESIGN.md:161` and `src/accounts.ts:2`; open PRs ready from `claude/project-thread-fx3wkp` restarted on main and append a ledger row.

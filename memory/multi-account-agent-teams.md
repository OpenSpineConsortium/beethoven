---
name: multi-account-agent-teams
description: greg's 2026-10-04 decision that several of his own Claude accounts run at once with agent teams and a rotating super-master lease; BUILD_PLAN §17 design, binding page facts, probes M1-M13, Cloak-shaped account directories, the transcript continuation (17.2.9) and the bee switcher as built (PR #3)
metadata:
  type: project
  modified: 2026-10-04T06:55:00Z
---

**Decided by greg** 2026-10-04 (card 02:18Z; 02:30Z = R1-R9 in BUILD_PLAN §17; 02:37Z worktrees+workflows; 03:09Z
four switcher sources; 03:23Z --share-history; 04:12Z State Management guide): several of his own accounts at
once, one master per account, one holds the super-master lease and hands it over claude-swap style; agent
teams, teams of teams, sessions as Slurm jobs, never orphan, simple auth. C6, D1d, BEE-127 and the launcher
CLAUDE.md sentence changed (branch claude/project-thread-2udoqz, unmerged). Unchanged: usage credits never,
no credential read or copied, never anyone else's account.

**Accounts = directories (17.2.1, Cloak's shape):** `$HOME/.beethoven/accounts/<label>/claude`; the launcher's
`$HOME/.beethoven/claude` stays put as `main` (`accounts/main/claude` links TO it); the list
`~/.beethoven/engine/accounts.json` = label, path, enabled, order, rest-until; a switch = the next job's
CLAUDE_CONFIG_DIR. claude-swap's token copying OUT; its usage vocabulary and 90 % threshold IN (BEE-188).

**Hand-off carriers:** (1) the engine's saved state incl. the guide's six-section `state/claude_context.md`,
read via `state/HYDRATE.md` (PR #3); (2) the transcript (17.2.9, 03:3xZ, one answer with the skeleton thread):
the spent session's SessionStart hook wrote `state/session.json` (0600: id, transcript_path, resume fields);
the engine binds that one file read-only at `/handoff/<id>.jsonl` and the next account runs
`claude --resume /handoff/<id>.jsonl --fork-session`; path accepted only from the writing account's own
`projects` folder. Nothing copied, credential untouched. Refused: shared/copied history dir, `--resume <id>`
or `--continue` across dirs, another person's account. Costs: uncached first turn, in-process team and
workflow results not restored, Remote Control re-registers. Probe M13 (commands in docs/bee/RUNBOOK.md).

**bee built (switching thread, beethoven-research PR #3, 06:38Z; moving to beethoven-agents, D2 split 13:19Z):** `bee account add|login|
list|...` + `bee-grid.sh`; status line `rate_limits` give the 5h/7d fractions in INTERACTIVE sessions only
(unverified reading); `-p` gets `StopFailure` `rate_limit`; guard
refuses `claude auth login` and `claude project purge`; signed in = `authMethod: "claude.ai"`; never type
`/autocompact` (writes into the sign-in dir). Not yet measured on the grid.

**Page facts (29 corrections folded 03:1xZ-03:2xZ):** teams need an interactive session (pty = interactive is
an inference, M1); one team per session, no nesting; unattended master needs a no-prompt permission config
(M12); resume does not restore teammates (M9). Socket dir NOT fixed; socket path and token reach only the
session's own hooks (SessionStart writes them 0600); satellites start `crossSessionInbound: accept`; two
jobs on one node = two containers, bus only. Desktop SSH CLOSED on Wayne State (CentOS 7); teams and `-p`
not in Desktop (D4a).

**Worktrees/workflows (17.6):** worktree per build stream; saved scripts in `.claude/workflows/` via a
`Workflow(<name>)` allow rule; WorktreeCreate hook to node-local disk (M10); a workflow run never crosses
accounts; hook `cwd` != project dir. Linear: BEE-185 accounts, 186 bus, 187 registry, 188 usage, 189 lease,
190 masters, 192 build parallelism. PROJECT_INSTRUCTIONS version 10 carries it all.

**Why:** the biggest change to the engine's shape; saves re-reading six pages. **How to apply:** build nothing of §17 before its probes; never copy a credential or a
transcript; check §13's 03:1xZ-06:4xZ entries before quoting §17 from memory.
See [[build-plan-rev2]], [[pr-convention-test-determined]], [[measurement-ledger]], [[beethoven-desktop]].

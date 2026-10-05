---
name: multi-account-d4
description: greg's decision D4 of 2026-10-04 02:30Z that the engine runs several Claude accounts he holds himself, one master per account and one rotating super-master lease, with the mechanism (bind one sign-in directory per job, never copy a credential), the plan's wording (BUILD_PLAN section 17) and the terms record
metadata:
  type: project
---

**Decided by greg** (re-plan thread, 2026-10-04 02:30Z, after the card he answered at 02:18Z "my
own several accounts"): the one-account rule is withdrawn. Several accounts in his own name run at
once; one master (an always-on Slurm job) per account; exactly one account holds the super-master
lease (greg's word: mutex) and hands it over as it nears its usage window, "claude-swap style";
every session and agent is reported to the super-master by message passing; nothing is ever
orphaned; teams of teams across accounts; a new session is a new Slurm job.

**The plan's wording governs: BUILD_PLAN §17** (re-plan thread, 02:48Z; PROJECT_INSTRUCTIONS v7;
Linear BEE-185 accounts, 186 bus, 187 registry/reaper, 188 usage reading, 189 lease, 190 masters).
Engine repo aligned (beethoven-research, CLAUDE.md D4, docs/ACCOUNTS.md, docs/PARALLEL.md):
- one directory per account `~/.beethoven/accounts/<label>/claude`; the launcher's
  `~/.beethoven/claude` IS the account `main`, reached by a link, nothing moved;
- the engine holds `accounts.json` (label, path, enabled, order) and nothing from inside; the one
  line is `bee account add <label>` (engine) or `hpcworker claude login --account <label>`
  (framework), neither built; no sign-out ever (the launcher's `--login fresh` is retired at 12.0.0);
- the lease is one store row, compare-and-set + fencing token, renewed every 60 s; the run carries
  over from the engine's saved state AND, since greg's 03:23Z message in the skeleton thread, the
  holder's session itself: the successor resumes it from the transcript's absolute path, bound
  read-only, with `--fork-session` (CLI reference verified; supersedes §17.2.4's "never a resumed
  session", plan amendment pending with the re-plan thread; not yet measured on the grid); every switch logged;
  a spent account hibernates until its reset; threshold 90 % waits on BEE-121 (not yet measured);
- a master is an INTERACTIVE Claude Code session under a pseudo-terminal (`-p` never spawns
  teammates), `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, in-process teammates only, never tmux;
  satellites are new Slurm jobs registered before their first turn; teams across accounts exist only
  at the engine layer (task graph + bus); registry, heartbeats, reaper cancel only our own jobs.

**Switchers compared** (skeleton thread, 03:19Z, docs/ACCOUNTS.md section 8, commit 731367b):
Cloak's mechanism (one CLAUDE_CONFIG_DIR per account, nothing copied) and claude-swap's surface and
pacing (add/list/status/enable/disable/remove, 90 % threshold, best/consume-first, cooldown,
hysteresis, quarantine) adopted; every credential-touching behaviour (token backup/restore,
export/import, overwrite, locks, pre-switch refresh, purge), `--share-history` and map/bind refused.

**Never:** read, copy, move or link a credential (claude-swap's backup is exactly what we do not
do); anyone else's account; pooled tokens; evading detection; usage credits on any account.

**Terms record (read 2026-10-04):** Anthropic's Usage Policy (2025-09-15) lists under "Do Not Abuse
our Platform" intentionally bypassing restrictions in its products; the Consumer Terms (2025-10-08)
forbid sharing an account, which this does not do. greg decided twice with that on the table; a
record, not a gate (BUILD_PLAN D1d).

**Why:** other threads must not reinstate "one account", build a credential swap, or put teams in a
`-p` step. **How to apply:** cite D4 and §17; keep the mechanism to directory selection. See
[[beethoven-research-skeleton]], [[claude-code-token-knobs-verified]], [[build-plan-rev2]].

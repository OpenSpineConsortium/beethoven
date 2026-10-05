# Account switching: what the three client editions could do (proposal, 2026-10-04)

From the thread "Account switching from the State Management guide". `bee` (engine repository,
`src/beethoven_research/bee/`, `docs/bee/`) now lists a student's own Claude accounts and moves work
between them on a laptop and on the grid. Nothing in the client repositories was edited; this is
for the threads that own them (browser extension, desktop plugin, VS Code edition) to take or leave.
Every item keeps the standing rules: no credential is read or moved, nothing touches claude.ai beyond
opening a checked link, plain words for students.

Beethoven runs Claude Code and is not an Anthropic product; "Claude" and "Claude Code" are
Anthropic's marks, used here to say what it runs.

## What the clients can rely on

| File | Where | Holds | Never holds |
| - | - | - | - |
| `accounts.json` | `~/.beethoven/engine/` on each machine | `version`, and per account `label`, `path`, `enabled`, `order`, `hibernate_until` (ISO time or null) | anything from inside a sign-in directory |
| `usage/<label>.json` | the same folder | `label`, `session_id`, `five_hour_pct`, `five_hour_resets_at`, `seven_day_pct`, `seven_day_resets_at` (percentages, epoch seconds; null when Claude Code did not send one) | tokens, e-mail addresses |
| `state/session.json`, `state/limit.json` | a project's `.claude/state/` or a run's `state/` | the session's id, account label, transcript path; the usage-limit record | |

All three are mode 0600 and owned by the student. `bee account list --json` prints the list with the
readings merged, which is the easier thing for a client to call where it can run a command.

## Proposals

1. **Desktop plugin.** A read-only tool, `account_list`, that runs `bee account list --json` on the
   laptop (or reads the two local files) and says in sentences which accounts exist, which rest and
   until when, and the last reading. `worker_list` already shows the account each worker reported;
   with `status.json`'s `account` field (the desktop thread's proposal in `docs/EDITIONS.md`) set
   from `BEE_ACCOUNT`, the two views agree. On the grid side this needs the framework to copy
   `BEE_ACCOUNT` into `status.json`: a contract change in `hpcworker` (`docs/V12_CONTRACT.md`),
   made in both repositories together.
2. **VS Code edition.** A setting, `beethoven.account`, whose value is a label from the laptop's
   `accounts.json`; the edition's terminal profile then sets `CLAUDE_CONFIG_DIR` (and `BEE_ACCOUNT`)
   for Claude Code terminals, exactly what `bee-use <label>` does, so the edition and the command
   line share one list. Its own sign-in (`beethoven claude login`) would become
   `bee account add <label>` under the hood, or keep its flow and write the list entry. Cloak's
   known limitation applies: the Claude Code VS Code extension may not honour `CLAUDE_CONFIG_DIR`,
   which has to be checked on a real machine before this ships.
3. **Browser extension.** The panel could show the worker's account label ("running as work") from
   `status.json` once item 1's contract field exists. Nothing more: the panel never offers a sign-in
   switch, because a switch is a new session on another directory, which the worker's restart does.
4. **All three.** When a client offers to "continue on another account", it calls `bee continue`
   (laptop) or starts `bee-grid.sh continue` in a compute-node shell; it never edits
   `accounts.json` itself except through `bee account enable|disable`.

## Not yet measured

Whether the Claude Code IDE extensions honour `CLAUDE_CONFIG_DIR`; whether the status line's
`rate_limits` arrive on greg's plans on the grid (the first check in `docs/bee/RUNBOOK.md`).

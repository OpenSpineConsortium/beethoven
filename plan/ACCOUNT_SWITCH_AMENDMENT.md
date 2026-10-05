# Account switching as built: amendment text for BUILD_PLAN §17 (2026-10-04)

Written by the thread "Account switching from the State Management guide" for the thread "Replan the
build and seed Linear", which owns `BUILD_PLAN.md`, `PROJECT_INSTRUCTIONS.md` and Linear. Nothing
here edits those files. Source of the ask: greg in the project chat, 2026-10-04 04:12Z: "I just
added the Claude CLI State Management file to the google drive, please read it and implement that
protocol so I can switch from one account to another seamlessly, both on my local machine, and the
grid, in a singularity container in the research engine."

The code is `bee`, in `OpenSpineConsortium/beethoven-research` under `src/beethoven_research/bee/`,
`tests/bee/` and `docs/bee/` (branch `claude/account-switching-8ojm4t`; the PR is linked from the
thread). It is self-contained, as the coordinator asked at 04:54Z, so it moves to `beethoven-agents`
in one piece when the split of `REPO_SPLIT.md` happens. Beethoven runs Claude Code and is not an
Anthropic product.

## 1. What exists now

- `bee account add|login|list|status|enable|disable|remove|env|pin|unpin|next|spent|rested` on a
  laptop (Windows, macOS, Linux) and `bee-grid.sh add|login|status|list|account|handoff|run|continue`
  on a compute node, which runs the same Python inside the engine's image with one sign-in
  directory bound at `/claude` per container. The list is `~/.beethoven/engine/accounts.json`
  (labels, paths, enabled, order, rest-until; nothing from inside a sign-in directory).
- The guide's hand-off file (six sections) with `/handoff`, `/hydrate`, `bee handoff
  prompt|import|check`, and its dual-hook loop: `PostToolUse` keeps `PROJECT_STATE.md` current from
  git, `SessionStart` injects it on resume, compaction, fork and hand-off.
- `bee run` / `bee continue [--fork]`: start Claude Code on an account with every credential
  variable stripped; after a usage limit or `/handoff`, the next account by order, `best` or
  `consume-first`, threshold 90 %, 5-point margin, 5-minute cooldown; a spent account rests until
  its window's reset; an account not signed in leaves the rotation and is reported.
- The image's managed settings run these hooks and bee's status line for every session, with
  `python -I` like the guard; the guard and the managed deny rules now also refuse
  `claude auth login` and `claude project purge`.
- Before a session starts (after an adversarial review, `docs/bee/STATE_HANDOFF.md` section 8): a
  fork binds only a session file of the account that wrote it, checked again on the host; a
  project whose settings name `apiKeyHelper` or set an API key is refused; an `salloc` shell on the
  login node is refused; each grid project is bound at its own path under `/work`, and each call
  has its own node-local temp.
- `pixi.toml` gains `win-64`, `osx-arm64`, `osx-64` (laptops); the `linux-64` part of the lock is
  byte for byte unchanged (70 entries checked).

## 2. Amendments proposed

**§17.2.8 (usage reading).** Replace "Until one is measured the hand-off is reactive" with: the
status line page (read 2026-10-04) documents `rate_limits.five_hour` and `rate_limits.seven_day`,
each with `used_percentage` and `resets_at`, in the JSON every status-line command receives (Pro and
Max plans, after the session's first response). bee's status line records the reading per account
(`~/.beethoven/engine/usage/<label>.json`, and the run directory's `state/usage.json`). The status
line runs in interactive sessions only, so an interactive master under a pseudo-terminal has the
reading and a `-p` step does not; for `-p`, the `StopFailure` hook's `rate_limit` error is the first
signal. Trigger (a), the 90 % threshold, can be enabled for masters once the grid check of
`docs/bee/RUNBOOK.md` shows the fields arriving on greg's plans. BEE-121's candidate list gains the
status line first; `stream-json`, `/usage` and OpenTelemetry remain the `-p` candidates.

**§17.2.4 and §17.2.9 (what carries the work).** Add: the saved state the holder writes before a
hand-off includes the guide's hand-off file (`state/claude_context.md`: objective, decisions, files
and their state, milestones, exact blockers, three to five next actions), prompted by bee's Stop
hook at the threshold or when a commit made the file stale, and the successor starts with "Read
`state/HYDRATE.md` and follow it", which validates against the disk before acting. That is the
first carrier; the transcript resume of §17.2.9 is the second, kept for when the conversation itself
matters and still waiting on M13. Reason: a few thousand tokens against a full uncached context, and
it works across machines, claude.ai and Claude Code versions.

**§17.2.9 (1).** Built as specified: the image's `SessionStart` hook writes `session.json` (mode 0600)
with `session_id`, `transcript_path`, the account label and, on a resume or fork,
`context_tokens`, `estimated_cache_write_usd`, `prompt_cache_likely_expired`,
`seconds_since_last_response`, in `$BEETHOVEN_RUN_ROOT/state/` (or the project's `.claude/state/`).

**§4 (token economy).** Add: `/autocompact` saves the window to user settings, which under
`CLAUDE_CONFIG_DIR` is a file inside the sign-in directory, so engine code never types it; a launch
uses `--autocompact <size>` (overrides the saved setting for one launch, not preempted by managed
settings) and a job uses `CLAUDE_CODE_AUTO_COMPACT_WINDOW` (plain integer; it wins over both;
model configuration and environment variable pages, 2026-10-04). The guide's 60 % rule is shown as
a hint in the status line, never automated.

**§17.3 (rules).** Add: the guard refuses `claude auth login` (a sign-in is the student's own sitting;
`--console` would bill per use, and usage credits are never used) and `claude project purge` (it
deletes what Claude Code keeps for a project inside the sign-in directory). An account counts as
signed in only when `claude auth status` says `authMethod: "claude.ai"` for that very directory:
measured in a cloud session (Claude Code 2.1.289), an empty directory answered `loggedIn: true` with
`authMethod: "oauth_token"` because a token came from the environment. Also: `continue --fork` believes the recorded transcript path only for a session file in the
writing account's own `projects` folder (the record lives in the project, which a session can
write; the review showed a path to another account's sign-in file reaching a bind), and a project
whose own settings would bill another way (`apiKeyHelper`, a cloud provider's credential export, a
credential variable in `env`) is refused before a session starts.

**§17.2.1 (accounts).** The list's place is `~/.beethoven/engine/accounts.json`, not
`~/.beethoven/accounts.json`: the grid script binds that folder into the image, and
`~/.beethoven` itself holds the launcher's sign-in. `bee account add` and `bee-grid.sh add` are the
one line; `hpcworker claude login --account` stays a contract item.

## 3. Linear

- BEE-185 (accounts): the engine half is built (this PR); the framework's `--account` is not.
- BEE-121 / BEE-188 (usage reading): the interactive half answered by the status line, pending the
  grid check; the `-p` half open.
- BEE-189 (lease) and BEE-190 (masters): unchanged; they will call `choose_next`,
  `should_hand_off` and `hibernate_until` from `bee/accounts.py`, which the gate proves.
- Probe M13: exact commands in `docs/bee/RUNBOOK.md`, greg's to run.

## 4. Not yet measured

Bash 4.2 and apptainer 1.2.2 on the grid (the runbook's G3 is the first run); the status line's
`rate_limits` on the grid; M13.

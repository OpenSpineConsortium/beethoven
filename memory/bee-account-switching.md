---
name: bee-account-switching
description: bee, the account switcher built from greg's "Claude CLI State Management Guide" (2026-10-04) — where it lives, what it changed from the guide, what is not yet measured
metadata:
  type: project
  modified: 2026-10-04T05:38:49.907Z
---

greg asked 2026-10-04 04:12Z (thread "Seamless account switching") to implement the Drive doc "Claude CLI State Management Guide" (id 1SL9nwiV7Z_drLcWyF9dj5tGVW0nm3406QTx7aflgZKo) so he can switch accounts on his laptop and on the grid in the engine's container. Built as `bee` in beethoven-research, PR #3 (merged by auto-merge 07:06Z, 076f357; moved to beethoven-agents with the three-repo split, so further changes go there; Linear BEE-185 In Progress): `src/beethoven_research/bee/` (accounts.py, handoff.py, claudeignore.py, cli.py, bee-grid.sh, shell/bee.sh|bee.ps1), `tests/bee/`, `docs/bee/RUNBOOK.md` (greg's laptop L1-L5, grid G0-G4, probe M13 commands), `docs/bee/STATE_HANDOFF.md` (what was taken from the guide and what was changed). Self-contained so it moves to beethoven-agents in one piece ([[multi-account-d4]], REPO_SPLIT.md).

Facts a later thread would otherwise rediscover:
- List at `~/.beethoven/engine/accounts.json` (not `~/.beethoven/accounts.json`: the grid script binds the engine folder). Sign-in dirs `~/.beethoven/accounts/<label>/claude`; `main` links `~/.beethoven/claude`; `--default-location` = CLAUDE_CONFIG_DIR unset.
- "Signed in" only when `claude auth status` says authMethod "claude.ai" for that directory. Measured in a cloud session (Claude Code 2.1.289): an empty dir answered loggedIn true with authMethod "oauth_token" from an env token.
- Usage reading: the status line JSON carries rate_limits.five_hour/seven_day used_percentage + resets_at (interactive sessions only, Pro/Max, after first response); bee records it per account in `usage/<label>.json`. `-p` has no status line; StopFailure rate_limit is its signal. Bears on BEE-121/188.
- Guide parts dropped as rule crossings: the alias that strands `~/.claude.json`, `/autocompact` (writes into the sign-in dir), `--console` login (usage credits), credential backup/locks/refresh. Guard now also refuses `claude auth login` and `claude project purge`.
- CrossHair 0.0.111 crashes on Literal-typed params and symbolic regexes; a contracted call inside a proved body gave NotDeterministic (use a plain helper).
- tools/verify_gate.py runs CrossHair one process per module, cpu-count at a time (VERIFY_GATE_JOBS), since one process leaked state between analyses (RecursionError on functions clean alone; CrossHair's own suite skips a test for it on 3.11): 396 s vs 957 s.
- Plan text for the replan thread: /mnt/project-files/plan/ACCOUNT_SWITCH_AMENDMENT.md; client proposals: ACCOUNT_SWITCH_CLIENTS.md.

- MOVE (2026-10-04): PR #3 merged 07:06Z (b7b8650). The "Three-repo separation" thread copied bee into the staged beethoven-agents as `beethoven_agents.bee` (paths /opt/beethoven-agents); its 53 `# crosshair:` comments are gone (beethoven-qa's gate refuses them): 25 functions sit under `[tool.beethoven-qa.unproven]` in agents' pyproject.toml with reasons, utc_text is now proven, the 27 lowered bounds run at 20 s; agents' whole gate green in 5 min. beethoven-research still holds bee until it is slimmed ([[three-repo-staging]]).

**Why:** the guide and D4 meet here; the next thread on lease (BEE-189) or masters (BEE-190) calls choose_next/should_hand_off/hibernate_until from bee/accounts.py.
**How to apply:** not yet measured: bash 4.2 + apptainer 1.2.2 on the grid (RUNBOOK G3), rate_limits on the grid, probe M13. Image not built (BEE-103).

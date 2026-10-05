---
name: claude-code-token-knobs-verified
description: Claude Code token-economy variable and settings names checked against code.claude.com/docs on 2026-10-04, where the plan's names were stale, and the rule that a managed env value overwrites a job's export
metadata:
  type: reference
  modified: 2026-10-04T01:35:22.565Z
---

Checked against code.claude.com/docs/en/{env-vars,settings-reference,prompt-caching,hooks,headless,
managed-settings,permissions,model-config} on 2026-10-04 (the skeleton thread), applied in
`beethoven-research` commit `553565b` and recorded in its CLAUDE.md and `containers/README.md`:

- Subagent caps carry the prefix: `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` (default 20) and
  `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` (default 3; `1` = no nesting).
  `CLAUDE_CODE_MAX_SUBAGENTS_PER_SESSION` is a no-op since Claude Code 2.1.224.
- Prompt cache: on a subscription within included usage the main conversation (incl. `-p`) gets
  the 1-hour TTL automatically, subagents/compaction 5 min; `promptCacheTtl`/`subagentPromptCacheTtl`
  (≥2.1.242) only matter under usage credits, which greg excluded outright on 2026-10-04 01:12Z
  ("never", same rank as the non-negotiables; BUILD_PLAN §2 C7, engine CLAUDE.md commit `14a7680`),
  so they stay unset and are not a knob.
- Tool search is the default with `ENABLE_TOOL_SEARCH` unset (MCP tools deferred).
- `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` (1–100) only lowers the threshold and applies only in sessions
  that compact before the model's limit, so pair it with `CLAUDE_CODE_AUTO_COMPACT_WINDOW` (plain
  integer 100000–1000000; `500k` reads as 500).
- `CLAUDE_CODE_EFFORT_LEVEL`: low/medium/high/xhigh/max/auto; "ultracode" is not a value.
- Linux managed path `/etc/claude-code/managed-settings.json` (+ `managed-settings.d/`); a `Read`
  deny also blocks Edit/Write on the path (≥2.1.208); `//path` anchors at the filesystem root.
- Hooks: exit 2 blocks (stderr reaches the model); exit 1 is NON-blocking and lets the call
  through, so a guard must fail closed. PreToolUse JSON `permissionDecision` allow/deny/ask/defer.
- `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` also disables feature flags → Remote Control; the
  launcher unsets it; the engine uses the four narrower switches instead.
- **A managed `env` value overwrites the same variable exported by the shell/job**, so per-step
  knobs (effort, concurrency, compaction window, `BEETHOVEN_RUN_ROOT`) must stay job-side.

**How to apply:** cite these names, not the plan's; re-check the docs before adding a new knob.
See [[beethoven-research-skeleton]], [[build-plan-rev2]].

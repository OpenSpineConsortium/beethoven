---
name: cloud-session-credits-and-usage
description: greg's $250 promotional Claude Code cloud-session credit (Max, claim by 2026-10-07, expires 2026-11-04), how project threads are metered, and how a thread reads any session's list-price usage and rate-limit window with get_session
metadata:
  type: project
  modified: 2026-10-04T01:49:57.945Z
---

greg asked 2026-10-04 01:45Z why the project is not using his "$250 in Claude Code cloud session
credits". Measured/read then (skeleton thread):

- The promo (press/explainer pages only; Anthropic's terms are on the claim page in the account):
  $100 Pro / $250 Max, claim at claude.ai/code/claim-credit or `/claim-credit` by 2026-10-07
  23:59 PT, applied automatically to cloud sessions and spent BEFORE plan limits, unspent balance
  expires 2026-11-04, balance shown in Settings > Usage. Not mentioned on code.claude.com's
  cloud-session or Projects pages, which say cloud sessions and project threads count against
  the plan's rate limits and that no separate compute charge exists.
- Every project thread is a cloud session (`environment_kind: anthropic_cloud`). The
  claude-code-remote `get_session` tool (any `session_`/`cse_` id) returns
  `external_metadata.rate_limit_info` (`rateLimitType` five_hour / seven_day_overage_included,
  `isUsingOverage`, `resetsAt`) and `usage.cost_usd`, the list-price figure (what the API would
  bill; not a bill on a subscription). No field shows a promotional balance.
- As of 01:48Z: all sessions `isUsingOverage: false`; threads on the five-hour window (reset
  06:40Z), the coordinator on the seven-day window at `allowed_warning` (reset 2026-10-08
  11:00Z). List price since 2026-10-03 21:13Z: re-plan thread $204, skeleton thread $71,
  coordinator $17, three finished threads $8 (about $300 total), desktop-plugin thread not yet
  reported.
- "Cloud session credits" (this promo) are not the "usage credits" (paid overage) greg excluded
  for the engine on 2026-10-04 01:12Z; the engine's grid jobs are not cloud sessions and cannot
  use either.

**Why:** the question will recur as the weekly window fills; other threads should answer from
`get_session` and Settings > Usage, not guess. **How to apply:** quote list price as list price;
never claim the credit is or is not being drawn without the Usage page. See
[[build-plan-rev2]], [[measurement-ledger]].

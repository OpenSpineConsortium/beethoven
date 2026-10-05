---
name: measurement-ledger
description: The standing, append-only build ledger every thread must write to (path, format, intervention log, boundary record), for greg's methods paper on a loosely directed Claude on a shared cluster
metadata:
  type: project
  modified: 2026-10-03T22:59:10.771Z
---

greg wants the whole build measured (wall-time, bugs fixed, starting materials) so it can be written
up as a reproducible research report. A standing ledger lives at `/mnt/project-files/ledger/`:
- `README.md` — the format (a stranger can follow it).
- `LEDGER.md` — **Starting materials** (baseline, written once 2026-10-03: repo SHAs, 17 notebook
  files + mtimes, topic text, project-creation 2026-10-03T21:13Z, greg's message 22:35Z) +
  **Activity log** (one append-only row per unit of work).

Row columns: date_utc · thread · actor · activity · wall_min · bugs_fixed · inputs · outputs ·
verified. Never put credentials in it. For engine runs also capture tokens in/out, cache hit-rate,
compaction events, subagent count, energy (kWh/CO2e) — link the W&B run.

**Why:** it is the reproducibility record for the research report; a standing project requirement.
**How to apply:** every later build thread appends one row per unit of work; put this instruction in
every brief. Structured run telemetry belongs to REFORMS (Linear G2) + W&B, linked from `outputs`.
See [[linear-engine-structure]], [[build-plan-rev2]].

**Added 2026-10-04 (greg's methods-paper framing, 00:16Z):** the report is a protocol/methods paper
(contribution: a loosely directed Claude on a shared university grid; greg says "16×H200 scale"). Prior
work: Anthropic's long-running-Claude guide (progress signal), Deep Researcher Agent arXiv 2604.05854,
arXiv 2609.13073 (unverified), Sakana AI Scientist et al.; ICML 2026 AI Scientists workshop already
passed (deadline 2026-05-07). New files beside LEDGER.md: `INTERVENTIONS.md` (every human intervention,
answer, failure, dead end, withdrawn claim, written when it happens; `why` ∈ knowledge, permission,
error, requirement, decision; counting rule in README) and `BOUNDARY.md` (what each agent could and
could not touch, per phase). `verified` gains `independent`. Engine rows link the per-run compute and
quota record (BEE-179). Linear: BEE-174 (M-5, done), 176 (M-7), 177 (M-8, greg: AUP check + AI-use
disclosure), 178 (G5-7 progress signal), 179 (G5-8). BUILD_PLAN §12 holds the prior-work text.

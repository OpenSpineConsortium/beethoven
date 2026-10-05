# Beethoven build ledger — format & conventions

This is the **standing, append-only record** of how the Beethoven research engine is built, so the
whole process can be reproduced and written up as a research report (greg's meta-ask, 2026-10-03). It
is a project-wide requirement: **every thread that does build work appends to `LEDGER.md`.** Nothing
here is secret — never put a credential, token, or key in the ledger.

## Files
- `README.md` — this file (the format; a stranger can follow it).
- `LEDGER.md` — the running log. Two sections: **Starting materials** (the fixed baseline, written
  once) and **Activity log** (one row per unit of work, append-only, newest at the bottom).
- `INTERVENTIONS.md` — every human intervention, failure, dead end and withdrawn result, written
  the moment it happens (added 2026-10-04; format below).
- `BOUNDARY.md` — what each agent could and could not touch, per phase of the build (added
  2026-10-04; a prose record, revised in place with a dated line per change).

## How to append (every thread)
Add one row to the **Activity log** table in `LEDGER.md` for each meaningful unit of work. Never edit
or delete earlier rows; correct a mistake with a new row that says what it corrects. Keep times in
**UTC**. Columns:

| Column | Meaning |
|---|---|
| `date_utc` | ISO-8601 UTC timestamp when the work finished, e.g. `2026-10-03T22:50Z`. |
| `thread` | Short thread/workstream name or Linear id (e.g. `P0-4`, `re-plan`). |
| `actor` | `claude` or a person's name. |
| `activity` | One line: what was done. |
| `wall_min` | Wall-clock minutes for this unit (best estimate; `~` is fine). |
| `bugs_fixed` | Count of defects fixed in this unit (0 if none). |
| `inputs` | Starting materials used (files, repo SHAs, prior issues) — enough to re-run. |
| `outputs` | What it produced (files/paths, Linear ids, commit SHA or PR link). |
| `verified` | How it was checked (`test`, `render`, `probe`, `review`, `independent`, or `unverified`). `independent` means checked by a different route than the one that produced the result (a second tool, the raw file, the portal's own response, a human's reading), which is what the methods paper counts. |

Guidance that keeps the report reproducible:
- Record the **commit SHA or PR** for any code change; record the **file path** for any document.
- `bugs_fixed` counts real defects corrected, not features added. If a run surfaced a bug but didn't
  fix it, say so in `activity` and set `bugs_fixed` to 0.
- For engine runs (once they exist), also capture **tokens in/out, cache hit-rate, compaction events,
  subagent count, and energy (kWh/CO2e)** — put them in `outputs` or link the W&B run. These feed
  Goal 2 (REFORMS Module 7) and the research report directly.
- Prefer `verified` over claims: a row with `unverified` is a to-do, not a result.

## Where structured run telemetry goes
Human-readable units live here. Machine-level per-run telemetry (Run ID, token counts, CIs, energy)
belongs to the REFORMS layer (Linear G2) and W&B; link it from the `outputs` column so the two stay
joined. The research-report scaffold (Linear M-3) reads both.

## The intervention log (`INTERVENTIONS.md`, added 2026-10-04 from greg's methods-paper framing)
The paper's honest accounting is **how often a human had to step in, why, and what happened**, plus
what failed and what was withdrawn. These are written **when they happen**, by the thread that sees
them, never reconstructed afterwards (the seed rows for 2026-10-03 are the one exception and are
marked `reconstructed`). One row per event, append-only, UTC:

| Column | Meaning |
|---|---|
| `date_utc` | When the human acted (or the failure was seen). |
| `thread` | Thread or workstream name, as in `LEDGER.md`. |
| `kind` | `intervention` (a human changed the agent's course), `answer` (a human supplied a fact or decision the agent asked for), `failure` (a result or run that did not work), `dead_end` (an approach tried and abandoned), `withdrawn` (a claim believed and later retracted). |
| `agent_was` | What the agent was doing or had proposed at that moment. |
| `why` | For interventions and answers, which of: `knowledge` (the human knew something the agent did not), `permission` (the agent lacked the access or authority), `error` (the agent was wrong), `requirement` (a new or changed ask), `decision` (a fork reserved to the human by design). For failures, the cause as far as known, or `unknown`. |
| `what_changed` | What the human did or decided, or what the failure cost. |
| `outcome` | Where it ended (files, issues, commits), or `open`. |

Counting rule for the paper: interventions per unit of work = rows of kind `intervention` + `answer`
with `why` in {`knowledge`, `permission`, `error`} divided by rows in the activity log over the same
period; `decision` and `requirement` rows are reported separately because they are part of the design
(the human owns the forks), not a failure of autonomy.

## The compute and quota record (engine runs; BEE-179)
Each engine step writes, beside its Run ID: Slurm job ids, partition and QoS, requested and used wall
time, queue wait, node ids, GPU-hours, preemptions and requeues, fair-share priority if the scheduler
reports it, and the quota-window spend (tokens in/out, cache hit-rate, compaction events, subagent
count), with CodeCarbon's energy and CO2e. The activity row for the run links that record in
`outputs`; it is not retyped into the table. How Claude Code reports the remaining window is not yet
measured (BEE-121).

## The boundary record (`BOUNDARY.md`)
The paper's environment section needs **exactly what the agent could and could not touch**. The
boundary is written per phase (the planning sessions in the cloud, the grid worker, the engine runs)
from the actual permission settings, repository scopes and refusals seen, not from intentions; a
refusal met during the work (a 403, an unanswered permission prompt, a denied host) is added the day
it is seen with its timestamp.

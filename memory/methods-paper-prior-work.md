---
name: methods-paper-prior-work
description: greg's 2026-10-04 framing — the build is a methods/protocol paper (undirected Claude agent on a shared academic grid); the checked prior work, paper criteria, and that the ICML 2026 venue has passed
metadata:
  type: project
  modified: 2026-10-04T00:19:50.164Z
---

On 2026-10-04T00:16Z greg said the whole build should be written up as a **protocol / methods
paper**; its contribution is a *relatively undirected* Claude agent on a shared academic grid
(prior work is tightly scaffolded, sandboxed or on company compute). Recorded in BUILD_PLAN.md §12
(amendment log is now §13) and `beethoven-research/CLAUDE.md`; Linear M-5..M-8 and G5-7.

**Prior work, checked 2026-10-04:** Anthropic "Long-running Claude for Scientific Computing"
(2026-03-23; confirmed; tmux on a compute node, SLURM job, git commits as progress record; the
agent needs a way to tell it is making progress: reference implementation, quantifiable objective
or test suite). Deep Researcher Agent arXiv 2604.05854 (Zhang, U Tokyo; confirmed: 500+ cycles,
30+ days, 52% over 200+ experiments). arXiv 2609.13073 — NOT verified (page unreadable from the
container); per greg a telecom single-vs-multi-agent Claude study where humans defined the search
space and loops needed intervention. Sakana AI Scientist etc. — no links given.

**Paper criteria (greg's source):** full record (prompts, instruction files, logs, git, job
scripts, GPU time/spend); honest accounting (interventions and why, failures, dead ends,
independent verification); grid specifics (quotas, preemption, fair sharing, permissions);
reproducibility on another cluster; AUP check on autonomous agents + AI-use disclosure, no AI
author.

**Venue catch:** the ICML 2026 workshop "AI Scientists – Tools, Co-authors, or Founders?"
(2026-07-11, deadline 2026-05-07) has already passed; target its next edition / a 2027-cycle
workshop, a methods journal, or a software/protocol track. Venue + field framing are greg's call
(M-7); AUP check + disclosure are greg's hand step (M-8).

**Why:** it sets requirements on engine code (progress signal per step, intervention log,
per-run compute accounting) and on every thread (keep the record whole).
**How to apply:** new engine steps must declare a progress signal; log interventions when they
happen; never cite the ICML 2026 workshop as open. See [[measurement-ledger]], [[build-plan-rev2]].

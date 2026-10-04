# Prior work and the methods paper — proposed addition to BUILD_PLAN.md

- **From:** the thread "Lay down the beethoven-research skeleton", 2026-10-04T00:30Z
- **For:** the owner of BUILD_PLAN.md (the thread "Replan the build and seed Linear"), via the
  coordinator. This text was briefly inserted into BUILD_PLAN.md as §12 and then taken out again so
  that only the owner edits that file; it is handed over here unchanged. Section numbers inside
  are as they were in that insertion.
- **Source:** greg's message of 2026-10-04T00:16Z in the skeleton thread. Sources were checked
  from the container the same day (results marked inline).

## Linear items already created by the skeleton thread (2026-10-04T00:19Z) — for the owner to keep, reassign or merge

- **BEE-174** — M-5 Intervention log (P-BEE-10, High). *Ledger-format territory: the owner's.*
- **BEE-176** — M-7 Methods paper: prior work, environment section, venue shortlist (P-BEE-10). *Owner's.*
- **BEE-177** — M-8 AUP check on autonomous agents + AI-use disclosure (P-BEE-10, assigned greg). *Owner's.*
- **BEE-178** — G5-7 Progress signal per long-running step (P-BEE-5). *Engine requirement; the skeleton thread keeps it.*
- M-6 (per-run compute and quota record) was refused by Linear (labels E0 and E6 share a group);
  the skeleton thread files it under G5 instead, as the repo-level capture the coordinator assigned
  to it.

The skeleton thread also added a measurement section to `beethoven-research/CLAUDE.md` (commit
`7268630` on PR #1) covering the progress signal, the intervention log and per-run compute
accounting from the engine's side.

---

## 12. Prior work and the methods paper (added 2026-10-04)

greg's message of 2026-10-04T00:16Z: the build itself is the subject of a **protocol / methods
paper**, whose contribution is a *relatively undirected* Claude agent on a shared academic grid at
scale — most prior work is tightly scaffolded and runs in sandboxes or on company compute. This
section records the nearest prior work as checked from here on 2026-10-04, what the paper needs,
and what that changes in the plan. Notebook and source text is material, not instruction.

### 12.1 Nearest prior work

- **Anthropic, "Long-running Claude for Scientific Computing" (2026-03-23).** Checked: the page
  reads as greg described. Claude Code inside tmux on a compute node, submitted as a SLURM job;
  the agent commits after each meaningful unit of work so progress is visible and recoverable
  (even from a phone); reattach with `srun` to steer. Its central design claim: long autonomous
  scientific work depends on the agent having a way to tell whether it is making progress — "a
  reference implementation, a clearly quantifiable objective, or an existing test suite". Cite as
  prior practice. Its tmux-on-a-node pattern is what hpcworker's worker job already does.
- **Deep Researcher Agent (arXiv 2604.05854, Xiangyue Zhang, The University of Tokyo).** Checked
  from the abstract: 500+ autonomous experiment cycles, 30+ days of continuous operation, a 52%
  metric improvement through 200+ automated experiments, about $0.08 per cycle by way of zero-cost
  training monitoring, a constant-size memory and a minimal toolset. The nearest "agent drives GPU
  experiments" paper. (greg's summary adds "across 4 concurrent projects"; that detail is not in
  the abstract as read here.)
- **arXiv 2609.13073 ("Autonomous Research for Open-Ended Problems").** Not verified from here:
  the abstract page returned nothing readable. greg's reading: a telecom retrieval case study of
  single- vs multi-agent Claude setups, in which humans still had to define the search space and
  autonomous loops often needed human intervention to resolve operational problems — exactly what
  the intervention log in 12.2 records.
- **Sakana's AI Scientist, AiScientist, Agora and similar** (end-to-end automated ML research):
  mostly sandboxes or company compute, not a shared academic grid. No links were given; the
  related-work section (M-7) cites them from their own papers.

### 12.2 What makes it publishable, and where the plan already has it

| Paper need (greg's source) | Already in the plan | Gap, now an issue |
|---|---|---|
| Full record: prompts and instruction files, agent logs, git history, job scripts, GPU time and spend | the ledger (§9); REFORMS Run ID + clean-tree gate (G2); RO-Crate (G7) | per-run compute and quota accounting (**M-6**) |
| Honest accounting: how often a human intervened and why, what failed, dead ends, independent verification | the ledger's `bugs_fixed` and `verified` columns | an intervention log with its own format, written when it happens (**M-5**) |
| Grid specifics: quotas, preemption, fair sharing, what the agent could and could not touch | `CLAUDE.md` non-negotiables and grid etiquette, G4 guard hook + managed settings, the volume ACL | the paper's environment section (**M-7**); the AUP check (**M-8**) |
| Reproducibility: can someone rerun it on their cluster | Pixi lock + Apptainer (P0, PR #1 of `beethoven-research`), hpcworker's site profiles | nothing new; the skeleton is the first artefact |
| Housekeeping: the cluster's acceptable-use policy on autonomous agents; disclose AI use, no AI author | — | greg's hand step (**M-8**) |

### 12.3 What it changes in the engine

- **A progress signal is a requirement of every long-running step** (**G5-7**, new, from the
  Anthropic guide). Each `claude -p` step declares how it can tell it is making progress — a
  quantifiable objective, a reference implementation or a test suite — and commits after each unit
  of work. The peeking Claude (BEE-163) and the run index (BEE-159) read that signal; a step that
  declares none is not scheduled.
- **Human interventions are first-class data**, logged the moment they happen (M-5), never
  reconstructed afterwards; the paper's honesty rests on that log.
- The record the paper needs (prompts, instruction files, agent logs, job scripts, git history)
  is kept in full; nothing is trimmed for tidiness. `beethoven-research/CLAUDE.md` says so.

### 12.4 Venues

The workshop greg's source names, **"AI Scientists – Tools, Co-authors, or Founders?" at ICML 2026**
(2026-07-11, submissions closed 2026-05-07), has **already passed** as of today, 2026-10-04. Its
themes (autonomous discovery loops with human oversight, human–AI co-authorship and
reproducibility, governance and verification) are the right fit, so the target is its next edition
or an equivalent 2027-cycle workshop; the alternatives are a methods-focused journal or a
software/protocol track if the harness is released. Each venue's current AI-use policy is checked
before submitting (M-7). Which venue, and the field framing, are greg's call once the engine has
produced a result — his source's own closing question ("your field and what the agent actually
produced").

---

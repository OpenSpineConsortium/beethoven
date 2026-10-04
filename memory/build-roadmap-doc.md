---
name: build-roadmap-doc
description: The research-engine build roadmap (Claude Doc, 2026-10-03): six phases, repo mapping, and six decisions pending greg
metadata:
  type: project
  modified: 2026-10-03T21:21:15.390Z
---

Drafted 2026-10-03: "Beethoven build roadmap" Claude Doc, https://claude.ai/code/artifact/d1a3fd7e-1237-42d4-bf73-7d8d334e491f
Phases: 0 ground truth (does headless `claude -p` run from sbatch on the student's own login), 1 one headless run (run.sbatch.tpl + Runs view), 2 outer loop as a chained Slurm job (not a login-node daemon), 3 REFORMS gates (research template + checker writing reforms.json), 4 paper and archive (Publish press before any DOI), 5 scale and sites.
Pending decisions (recommended default in brackets): token billing [student's own subscription; no pooled LiteLLM keys], workflow engine [plain sbatch via adapter first, Metaflow later], research template home [new third repo], pinning [Pixi in image], verification extras [defer], approval points [Publish only].
Notebook notes 04, 10 section 2 and 11 describe claude.ai interception; notes 07-09 assume setup-token. Both conflict with CLAUDE.md and are excluded.

**Why:** later threads building any phase should start from this plan and its open decisions.
**How to apply:** check the doc for greg's edits or answers before assuming the defaults. See [[repo-state-vs-research-engine]].

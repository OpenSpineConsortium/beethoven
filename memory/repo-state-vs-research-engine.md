---
name: repo-state-vs-research-engine
description: As of 2026-10-03 the two repos are a Remote Control launcher; none of the research-engine/REFORMS layer exists yet
metadata:
  type: project
  modified: 2026-10-03T21:14:38.524Z
---

Mapped 2026-10-03 (hpcworker main 2e5bcf8, beethoven-extension main 4b1d870). Both repos implement Beethoven: a Chrome extension that starts a student's own `claude remote-control` worker as an always-on Slurm job in Apptainer (hpcworker framework 11, extension 12.0.0) and opens it in claude.ai. No Hydra, run hashing, clean-tree gate, MONAI splits, W&B/CIs, CodeCarbon, LaTeX macros, Zenodo/HF, Metaflow/LangGraph, `claude -p` headless loop, hooks or LiteLLM exist in either repo. ARCHITECTURE.md 2 says workflow-engine templates "would sit beside" jobs/ rendered from the site profile; not built. No open PRs, no feature branches, CI green on both.

**Why:** the project topic describes a research engine; the code is only its transport/launcher layer.
**How to apply:** treat research-engine work as new modules on top of hpcworker; check CLAUDE.md rules first (credential rules forbid LiteLLM-style key rotation; interactive RC vs headless `claude -p`). See [[beethoven]].

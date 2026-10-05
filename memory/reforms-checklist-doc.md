---
name: reforms-checklist-doc
description: Where the REFORMS gate checklist lives and the ownership split it proposes (2026-10-03)
metadata:
  type: reference
  modified: 2026-10-03T21:23:38.239Z
---

REFORMS compliance checklist (Claude Doc): https://claude.ai/code/artifact/543144a2-c7ff-4c24-bae3-772a67cd1ad1
Maps all 32 REFORMS items (8 modules, from arXiv 2308.07832) to gates: 20 code-checked, 12 "declared" fields in a study.yaml.
Proposed owners: hpcworker = run manifest, Run ID, clean-tree refusal, compute record, gate runner, `reforms.json` contract file; lab image = Hydra/MONAI/W&B/CodeCarbon; new repo `beethoven-research` (not yet approved) = splitter, CIs, macros, Zenodo/HF builders; extension = read-only view + human Publish click.
Run ID should exclude volatile Slurm vars. Energy is not a REFORMS item (rides on 2c).
greg accepted the checklist as drafted (2026-10-03, "ok thats fine"). Still open with greg: new repo vs folder; Metaflow vs own chaining; RC worker vs headless `claude -p`. See [[repo-state-vs-research-engine]].

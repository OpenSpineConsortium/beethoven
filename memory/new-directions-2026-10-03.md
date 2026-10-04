---
name: new-directions-2026-10-03
description: greg's 2026-10-03 evening additions (desktop extension with native ssh, command center + graph + peeking Claude, multi-worker, imaging migration + SQL catalog, promo) and the rules each carries
metadata:
  type: project
  modified: 2026-10-03T23:32:56.411Z
---

greg's second message (2026-10-03T23:09Z) added, beyond D1–D3 (see [[build-plan-rev2]]):

- **F1 Claude Desktop extension with native ssh** (`P-BEE-11`, repo to be `beethoven-desktop`): a
  complement to the browser extension, which cannot open an ssh terminal or view files. Same
  non-negotiables: never a Claude credential; grid password/one-time code only into the ssh session,
  never stored; no remote code; Beethoven name + trademark sentence. Spike first (BEE-153); the draft
  `plan/DESKTOP_EXTENSION_SPIKE.md` marks every claim verified / not verified (`.mcpb` bundles, system
  `ssh` spawned, macOS/Windows only; 8 open questions need a real machine or the grid).
- **F2 Command center + project dependency graph + "peeking Claude"** (`P-BEE-12`): jobs view from
  `runs/index.json` + `status.json` at the 60 s floor (never a faster `squeue`); Metaflow DAG exported as
  `graph.json`; a read-only headless `claude -p` summariser job writing `status/<step>.md`, per step end /
  hourly, spending the same subscription quota (so BEE-121 may skip it).
- **Several Claude sessions per student** (BEE-150..152 under G5): Metaflow `foreach` → one sbatch job
  per branch; all share one account's 5-hour window, so the quota scheduler governs fan-out.
- **R Imaging data: copy greg's `go2432` home-dir imaging data to CephFS, then a SQL catalog**
  (`P-BEE-13`): copy, verify (sha256 manifests as sbatch jobs on compute nodes), lock; never move or
  delete; SQLite built on node-local scratch; pydicom in a small data image of greg's own (never the lab's
  worker image); patient-level splits; PHI stays on the grid. greg names source dirs, destination and the
  PHI statement first (BEE-165). Runbook `plan/IMAGING_MIGRATION_RUNBOOK.md`: unrun on any machine.
- **O Promo** (`P-BEE-14`): audience = students/faculty on free-tier chat AIs; pitch = about $20/month
  (Claude Pro, their own plan) + Beethoven. Rules: Beethoven name, trademark sentence verbatim, no invented
  numbers or quota claims, engine = future work, private store listing only, CTA
  https://openspineconsortium.com/beethoven/. Draft `promo/PROMO_V1.md`.

**Why:** greg's stated directions; a thread picking one up should not re-derive the constraints.
**How to apply:** start from the Linear project; keep the posture rules above; execution on the grid
needs greg's own worker or shell. See [[linear-engine-structure]], [[measurement-ledger]].

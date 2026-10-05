---
name: spinesurg-imaging-corpora
description: Where greg's imaging corpora live on the grid (Panasas home vs CephFS data/), read from the t-SNE code in spinesurg-ct-nnunet on 2026-10-04; feeds BEE-165 and the migration runbook
metadata:
  type: project
---

greg does not know his imaging source directories by heart (2026-10-03T23:58Z); the authoritative list is
the t-SNE corpus code in `Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet` (read-only here, shallow clone at
`/home/claude/spinesurg-ct-nnunet`, HEAD 465bec6): `tools/corpus_manifold.py` `SETS` dict (one entry per
X-ray corpus, 38 sets, 15,154 frames per `SchwingNet/results/manifold/MANIFOLD.md`), two roots:
- `H = ~` = `/wsu/home/go/go24/go2432` (Panasas home, soft quota; the SOURCE to migrate): `FluoroCap/*`,
  `spine-detector/data/{yolo_v3,yolo_v6f,raw/{nhanes_full,buu_full,csxa,mendeley_716}}`, `vindr_pseudo/img`,
  `lateral236_pseudo/img`, `{ctsp,verse,ts,physics}_drr/img`, `physics_rare/img`,
  `model_night/anchor_none_v2_17-1882/images`. 214 top-level home dirs in all; CT corpora, crop banks and
  nnU-Net results are listed in `docs/MANIFEST_DATA_MODELS_RESULTS.md` §2–5.
- `D = /rs/rs_grp_oschome/go2432/data` (CephFS, ALREADY holds corpora): `realxray/{deepfluoro,carmlspine,
  cobra_elekta,geneva_hip}`, `or_ready/{devices/varian_halcyon/pairs,spinesac,wholespine/data/eval/aasce,
  corpus_manifold}`, `ljubljana/pairs`, `devcorpus/{render,styled}`. So the migration destination should
  sit in that `data/` tree, not a new sibling folder (BEE-165 item 2 still greg's call).
Python on the grid for that repo: `~/mambaforge/envs/spineps/bin/python`; jobs on `reqp --qos=requeue`.

**Constraints:** branch `L6_Class` is PRIVATE (FluoroCap level-ID code), never push it to a public repo;
home dotfiles `.hf_org_token`, `.hf_osc_token`, `.kaggle`, `.wandb` are secrets, never read or copied;
DICOM headers carry names and dates, PHI stays on the grid; sizes and existence on disk are NOT yet
measured (nothing has run on the grid). greg's word "nramcj" (23:58Z) matched nothing in the repo; ask.
Tiered source list with evidence: `/mnt/project-files/plan/IMAGING_SOURCES.md` (when filed).
See [[new-directions-2026-10-03]], [[build-plan-rev2]].

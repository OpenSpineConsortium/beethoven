> Filed 2026-10-04T02:5xZ by the re-plan thread from the imaging inventory workflow (six readers over spinesurg-ct-nnunet at commit 465bec6, classification of 210 roots, two verification passes; 98 entries changed by the verifiers). Nothing on the grid was read or touched: every size and count is what a repository document states, and the runbook (IMAGING_MIGRATION_RUNBOOK.md) measures before anything is copied. Owner for questions: BEE-165.

# IMAGING_SOURCES — what imaging data sits in the Panasas home, and in what order to move it

Written 2026-10-04 from the repository `/home/claude/spinesurg-ct-nnunet` at commit 465bec6 (2026-09-27) and the
six reader notes beside this file. Nothing here was measured on the grid: every size and count is the number a
repository document states, with its line; where the repository states none, the entry says "not yet measured".
The inventory job of the runbook (`/mnt/project-files/plan/IMAGING_MIGRATION_RUNBOOK.md`) measures first;
this document only says what to point it at.

Abbreviations: H = `/wsu/home/go/go24/go2432` (Panasas home, the source); D = `/rs/rs_grp_oschome/go2432/data`
(CephFS, the destination); M:N = `docs/MANIFEST_DATA_MODELS_RESULTS.md` line N (dated 2026-09-16); DCA:N =
`docs/DATA_COMPLETENESS_AUDIT.md` line N; LIN:N = `docs/LINEAGE.md` line N. Software never deletes a source: every
batch is copy, verify, then lock the source read-only.

## A. Where the data is today

Every imaging corpus the project acquired lives in the Panasas home `/wsu/home/go/go24/go2432`: the real films
under `H/spine-detector/data/raw/*`, the literature figure corpus under `H/FluoroCap`, the three raw CT corpora
under `H/data/CTSpinoPelvic1K`, `H/data/TotalSegmentator` (and `_v3`) and `H/VerSeFusion`, the DeepFluoro HDF5 under
`H/deepfluoro`, and ~90 derived render directories (`*_drr`, `*_pseudo`, `*_render`), crop banks (`*_ctx`) and
synthetic-hardware stores beside them at the top of the home (`docs/PIPELINE_RESUME.md:57-61`; `tools/pipeline_state.py:37-41`
resolves every stage against `expanduser("~")` and never names `/rs`). The manifest of 2026-09-16 names no
`/rs` path at all (M:6, M:895) and its stated sizes sum to about 2.3 TB (reader_manifest.md, section 10), with
~1.2 TB freed since by `slurm/disk_cleanup.sh` (LIN:113; `tools/pipeline_state.py:516`). The CephFS volume holds
only what was fetched or produced after mid-September 2026: the real-X-ray layout `D/realxray`, the acquisition
collections (`carmlspine`, `cobra2026`, `deepfluoro_vendor`, `geneva_hip_src`, `ljubljana`, `spinesac`,
`ctspine1k`, `ribfrac`, `thoracic_xr`), the SPINEPS and harvest trees, and the figure/bank release roots
(reader_cephfs.md, section 1). The t-SNE corpus list (`tools/corpus_manifold.py:50-99`: 45 sets, 24 on the home
and 21 on CephFS) covers the X-ray, fluoroscopy and render corpora as the *frames the detector saw*, i.e. it reads
`img/*.npy` of render dirs and `*_pseudo` dirs, not the raw films behind them, and it covers **no CT root at
all**: CTSpinoPelvic1K, VerSeFusion and TotalSegmentator appear there only through their DRRs. The CT roots come
from the manifest (M:183-185, reader_manifest.md section 2) and `tools/ct_inventory.py:45-58`. The single most
important fact: **the raw CT (448 GB stated: 227 + 139 + 82, M:183-185) and the raw films under
`H/spine-detector/data/raw` have no copy anywhere on CephFS** — `D/vindr` holds identity JSON only
(reader_cephfs.md:32), `D/thoracic_xr` mirrors AASCE from the challenge, not from the home
(`slurm/thoracic_xr_fetch.sh:20` compares against the home copy), and `D/ribfrac/images` was unzipped *from*
`H/data/ribs` (`tools/other_ct_fetch.py:11-12,19`). Everything else in the pipeline is a function of those roots.

## B. Tier 1 — raw acquired imaging, irreplaceable or restricted (copy first)

Order: real patients first, then cadavers and phantoms, then public CT. "CephFS twin" means a copy of the same
bytes; a re-download or a derived layout is not a twin. "Regenerable" means re-fetchable from the publisher under
the same terms; for the restricted sets that is a new application, not a download.

| Root (absolute) | Holds | Formats | Origin | PHI / nature | CephFS twin | Regenerable | Evidence |
|---|---|---|---|---|---|---|---|
| `/wsu/home/go/go24/go2432/spine-detector/data/raw/vindr/1.0.0` | VinDr-SpineXR v1.0.0: `train_images/`, `test_images/`, `annotations/`, `SHA256SUMS.txt`; 10,466 DICOM, 24,298 lesion-box rows | DICOM, CSV | PhysioNet credentialed download under a named person's DUA | real patients, de-identified by the publisher; DUA forbids redistribution | none (`D/vindr` = identity JSON + audit only) | only by re-application to PhysioNet | M:168; reader_cephfs.md:32; `slurm/audit_film_corpora2.sh:17,31-44`; `slurm/film_corpus_inventory.sh:31-56` (writes `.missing.txt` here) |
| `/wsu/home/go/go24/go2432/spine-detector/data/raw/lateral_236` | 236 standing whole-spine laterals, 3,056 px wide, burned-in overlay; 1.3 GB | JPG | IEEE DataPort subscription | real patients; burned-in text (Chinese) not audited for identifiers | none | only by re-subscription | M:174; `slurm/reproduce_all.sh:25` |
| `/wsu/home/go/go24/go2432/spine-detector/data/raw/nhanes_full` | NHANES-II films: 17,073 TIFF (9,667 C, 7,406 L), 91 GB; `.filelist.txt`, `.download_complete` | TIFF | CDC ftp index | real survey participants, public release | none | yes, slow (CDC ftp; the fetch took days — not stated) | M:166; `slurm/film_corpus_inventory.sh:31-56` (writes `.download_complete` here) |
| `/wsu/home/go/go24/go2432/spine-detector/data/raw/nhanes_annotated` | 543 per-vertebra mask pickles (275 C + 268 L, 364 subjects), 159 GB of float64 masks | PKL (zip 1,017,496,285 B) | Zenodo 10223910, CC BY 4.0 | real participants, public | none | yes (Zenodo) | M:165; reader_fetch.md:317 |
| `/wsu/home/go/go24/go2432/spine-detector/data/raw/csxa` | CSXA lateral cervical films: `images/datasets-PNG`, `annotations/datasets-JSON`, `datasets.xlsx`, `csxa_repo.zip`; 4,963 films | PNG, labelme JSON | ScienceDB 10.57760/sciencedb.15391 | real patients, public | none | yes (ScienceDB / HF mirror) | M:164; `tools/corpus_manifold.py:81` |
| `/wsu/home/go/go24/go2432/spine-detector/data/raw/buu_full/BUU-LSPINEv1` | BUU-LSPINE v1 `AP/`, `LA/`, `KIOM2022_dataset_report.xlsx`; 7,204 films | JPG, CSV | BUU public release | real patients, public | none | yes | M:169; `tools/corpus_manifold.py:78-79` |
| `/wsu/home/go/go24/go2432/spine-detector/data/raw/aasce` | AASCE 2019 `train/`, `test/`, `train_txt/`; 579 JPG, 251 patients | JPG, landmark txt | SpineWeb challenge | real patients, public | partial: `D/thoracic_xr` is a fresh mirror compared file-by-file with this copy (`grid_copy_md5.json`), not a copy of it | yes (GitHub mirror) | M:167; `slurm/thoracic_xr_fetch.sh:20`; reader_cephfs.md:31 |
| `/wsu/home/go/go24/go2432/spine-detector/data/raw/mendeley_716` | `Dataset.zip` (43,892,677 B) + `extracted/Dataset`; 714 JPG with boxes/keypoints | ZIP, JPG | data.mendeley.com 5jdfdgp762 v1, CC BY 4.0 | real patients (near-certain BUU re-release) | none | yes | M:173; reader_fetch.md:318 |
| `/wsu/home/go/go24/go2432/spine-detector/data/raw/{buu_drive, buu_v1, spinal_ai2024, cm_spine}` | `buu_drive` 9.3 GB byte-identical subset of buu_full; `buu_v1` 77 files identical to buu_full; `spinal_ai2024` 20,000 AI-generated JPG, 2.7 GB; `cm_spine` empty | JPG, ZIP, COCO JSON | downloads | duplicates / synthetic / empty | none | yes | M:170-172, M:175-176, M:717 |
| `/wsu/home/go/go24/go2432/spine-detector/data/raw/buu_2000` | **symlink** to `H/XRSpinoPelvic1K/data/BUU-LSPINE` | link | — | — | — | — | M:171; reader_manifest.md:259 (copy the link as a link) |
| `/wsu/home/go/go24/go2432/FluoroCap` | literature/web figure corpus: `panels/`, `real_fluoro_only/`, `real_grainy/`, `openi/`, `commons/`, `pmc18m/`, `youtube/` (265 GB, 298,075 PNG); 12,106 figures; 316 GB; also holds models and results (`student_pack`, `recurrent_head_*.pt`, `captions_matched_lstv.jsonl`) | PNG, JSONL, PT | PMC / Open-i / Wikimedia / YouTube harvest | published figures of real patients, de-identified by publication; mixed licences incl. NC | none | partly: harvest scripts exist but web state has moved; the curated subsets are not regenerable | M:177; M:195; M:720; `tools/corpus_manifold.py:65-71` |
| `/wsu/home/go/go24/go2432/FluoroCap_lstv2`, `/wsu/home/go/go24/go2432/FluoroCap_s2`, `/wsu/home/go/go24/go2432/FluoroCap_wsl` | later FluoroCap harvests / stages; contents not described in the repository | not in the repository | as above | as above | none | not in the repository | roots present in home_roots.txt; the repository names only `FluoroCap_lstv` (M:720: does not exist) |
| `/wsu/home/go/go24/go2432/deepfluoro` | DeepFluoro IPCAI 2020: `data/`, `unpacked_full/ipcai_2020_full_res_data.h5` (2,541,608,861 B) + LICENSE, `cache/`; 6.2 GB | HDF5 | JHU Data Archive doi:10.7281/T1/IFSXNV, CC BY-NC(-SA) 4.0 | 6 cadavers | content twins, not byte twins: `D/polypose/hf/.../xvr-data/deepfluoro` (NIfTI+DICOM repack) and `D/deepfluoro_vendor` (vendor DICOMs) | yes (archive refuses curl; needs `curl_cffi`) | `slurm/deepfluoro_acquire.sh:13-15,33-39`; `tools/dl_deepfluoro.py:4-9,16-21`; DCA:712 |
| `/wsu/home/go/go24/go2432/data/CTSpinoPelvic1K` | the project's own release v10: `ct/` (802 `_ct.nii.gz`), `labels/`, `labels_v10/`, `manifest.json`, `SHA256SUMS.txt`; 227 GB; record 0533 repaired in place | NIfTI gz | own HF/Zenodo release (`gschwing/CTSpinoPelvic1K`, `OpenSpineConsortium/CTSpinoPelvic1K`) | public CT, de-identified | none for the volumes; `D/ctsp0533_repair` holds one record's repair; `D/ctsp_april` holds the 1,153-record April set (different release) | yes from HF, but the grid copy is the one every symlink points at (`H/bench/ct_by_case`, Dataset815 `imagesTr`) | M:183; `scripts/download_dataset.py:227-235`; `slurm/ctsp0533_repair.sh:45,153-179`; `slurm/prep815.sh:9-11` |
| `/wsu/home/go/go24/go2432/VerSeFusion` | VerSe '19/'20 raw (463) + `data/unified` (374 x `_ct.nii.gz`, `_msk.nii.gz`, `_meta.json`), `manifest_summary.json`; 139 GB; `unified` is 88 MB so its `_ct` files are probably symlinks | NIfTI gz, JSON | OSF osf.io/t98fz | public CT | none | yes (OSF) | M:184; M:783; reader_manifest.md:53 |
| `/wsu/home/go/go24/go2432/data/TotalSegmentator` | TotalSegmentator v2.0.1: 1,228 cases, 117 masks per case; 82 GB | NIfTI gz | Zenodo 10047292, CC BY 4.0 (`Totalsegmentator_dataset_v201.zip` 23.6 GB) | public CT | none (`D/spineps/tsv3`, `D/anomaly_harvest/totalsegmentator` are derived masks) | yes | M:185; DCA:567; `slurm/ts_drr.sh:11-12,22-23` |
| `/wsu/home/go/go24/go2432/data/TotalSegmentator_v3` | `Totalsegmentator_dataset_v300/` + `Totalsegmentator_dataset_v300.zip`; size not stated | NIfTI gz, ZIP | Zenodo, CC BY 4.0 | public CT | none | yes | `slurm/ts_drr.sh:15`; `slurm/anchor_c2.sh:47`; `slurm/ts_spineps_diagnose.sh:38` |
| `/wsu/home/go/go24/go2432/data/rsna_cspine` | `rsna-2022-cervical-spine-fracture-detection.zip` (203 GB stated), never extracted; `fetch.log` | ZIP of DICOM | Kaggle competition, competition rules | public, de-identified | headers only: `D/anomaly_harvest/other_ct/rsna/` | yes (Kaggle CLI) | `slurm/rsna_cspine_fetch.sh:10-16`; `slurm/audit_unused_data.sh:12,33,38-42`; `docs/CT_INVENTORY.md:34` |
| `/wsu/home/go/go24/go2432/data/ribs` | `ribfrac-*-images*.zip` (RibFrac, 660 chest CTs) | ZIP | MICCAI 2020, CC BY-NC 4.0 | public CT | derived: `D/ribfrac/images` is the unzipped images; the zips stay here | yes | `tools/other_ct_fetch.py:11-12,19`; `slurm/other_ct_fetch.sh:27` |
| `/wsu/home/go/go24/go2432/XRSpinoPelvic1K` | `data/BUU-LSPINE` (4,000 JPG, the target of `buu_2000`), `data/xrsp1k` (6,416 lateral DRRs of 822 cases — derived), `data/dataset2024.zip` (4.7 GB, never opened), `data/runs/` (YOLO weights), dangling links `data/{ct,labels}` | JPG, ZIP, PT | BUU release + own renders | real patients (BUU) + renders | none | BUU yes; `xrsp1k` re-render; the zip unknown | M:171, M:198-200, M:442, M:479, M:719, M:773 |
| `/wsu/home/go/go24/go2432/data/{spondy_landmark, v5_final, ds01, x}` | named as CT roots by the inventory tool; contents not described | not in the repository | not in the repository | unknown | none known | unknown | `tools/ct_inventory.py:45-58` |

Partition records that travel with tier 1 (small files at the top of the home; copy with the first batch so no
later verify step lacks them): `/wsu/home/go/go24/go2432/split_final.json` (same bytes as
`SchwingNet/results/fig6/frozen/v1/split_final.json`, sha256 65a57eb0c7a6e202207a9eb63307da37c6bac88f3e7f956e14543413af2bca71;
`tools/auto_reference_calibrate.py:6,51,355-357`; read by `tools/g3_detector.py:11`, `SchwingNet/slurm/fig6_tau_val.sh:44`),
`patient_keys.json` (`slurm/allspine_v8_clean.sh:28`), `patient_keys_v9.json` (`slurm/allspine_v9_keys.sh:28`),
`patient_keys_final.json` (`SchwingNet/slurm/fig6_prep.sh:47`), `vindr_views.csv` and `vindr_lat_ids.txt`
(`slurm/vindr_pseudolabel.sh:32,37`; `tools/train_view_classifier.py:16`), `ct_gzip_corrupt.txt` (`slurm/gzcheck.sh:8,19`;
read by `slurm/report_final.sh:30`, `tools/make_report.py:9`), `gate_pass.csv` (`tools/acquisition_screen.py:857`;
`slurm/acquisition_spineps.sh:28` reads it from CephFS, so a home copy is unexplained).

## C. Tier 2 — derived imaging that is expensive to regenerate

Render dirs are `img/*.npy` + `ann/*.json`; pseudo-label dirs the same with model-made annotations; the two
`implant_*` stores are synthetic hardware fused into CT. Regenerating a render dir is a GPU array job over its
source CT (hours to a day each, not timed in the repository); regenerating pseudo-labels needs the exact model
checkpoint that made them. "Twin" as in section B.

| Root (absolute, under `/wsu/home/go/go24/go2432/`) | Holds | Formats | Origin | PHI / nature | CephFS twin | Regenerable | Evidence |
|---|---|---|---|---|---|---|---|
| `vindr_pseudo` | VinDr films as `img/*.npy` with pseudo-labelled levels (3,679 crops downstream; 11 banks) | NPY, JSON | `slurm/vindr_pseudolabel.sh` on the tier-1 DICOMs | real patients, DUA-restricted (derived from VinDr) | none | yes, given the DICOMs + the same checkpoint; the checkpoint is not named in the repository | M:168; `slurm/vindr_pseudolabel.sh:32,37`; `tools/corpus_manifold.py:75` |
| `vindr_pseudo_drr` | DRR-styled companion of the above | NPY, JSON | render | derived from VinDr | none | yes | home_roots.txt; writer not in the repository |
| `lateral236_pseudo` | the 236 whole-spine laterals pseudo-labelled | NPY, JSON | pseudo-label pass | real patients (IEEE DataPort) | none | yes given the JPGs + checkpoint | `tools/corpus_manifold.py:76` |
| `nhanes_pseudo`, `nhanes_drr` | NHANES films pseudo-labelled; NHANES as DRR-style | NPY, JSON | pseudo-label / render | real participants, public | none | yes | `tools/corpus_manifold.py` (NHANES sets); M:166 |
| `films_drr` | the main film-style DRR bank all `films_all*` arms render from (`DRRS=films_drr`) | NPY, JSON | `slurm/ctx_arm.sh` renders | render of public CT | none | yes (hours; the oldest and most referenced) | `slurm/launch_realfilm_arms.sh:44-45`; `slurm/launch_round2.sh:41,44` |
| `ctsp_drr`, `ctsp_drr_film` | CTSpinoPelvic1K DRRs (801 cases) and film-styled | NPY, JSON | render from `H/data/CTSpinoPelvic1K` | public CT | none | yes | M:183; M:145 region |
| `ctsp_drr_obl`, `ctsp_drr_obl2` | **misnamed**: VerSe (via `vf_813`), 314 cases, 8 oblique poses, 2,511 renders in obl2 | NPY, JSON | render | public CT | none | yes | M:145; reader_manifest.md:181 (naming trap 1) |
| `verse_drr`, `verse_drr_film`, `verse_drr_obl`, `verse_drr_obl2` | VerSe DRRs, film-styled, oblique | NPY, JSON | render from `H/VerSeFusion` | public CT | `D/rare_class/verse_drr` holds a *different* 56-scan rare-class render, not a twin | yes | M:184; reader_cephfs.md:39 |
| `ts_drr`, `ts_drr_v3` | TotalSegmentator v2 / v3 DRRs | NPY, JSON | `slurm/ts_drr.sh` | public CT | none | yes | `slurm/ts_drr.sh:11-12,15,22-23` |
| `physics_drr`, `physics_drr_film`, `physics_rare`, `physics_rare_film` | physics-model DRRs over CTSP (2,430) + TS (1,831) + VerSe; rare-class subset | NPY, JSON | render | public CT | none | yes (largest GPU cost of the render family; not timed) | M:183, M:185 |
| `anchor_drr`, `anchor_drr_c2` | anchor-pose DRRs (C2 variant from TS v3) | NPY, JSON | `slurm/anchor_c2.sh` | public CT | none | yes | `slurm/anchor_c2.sh:47` |
| `mendeley_drr` | Mendeley films rendered/styled | NPY, JSON | render | real patients (BUU re-release) | none | yes | M:173 |
| `postop_render` | post-operative hardware renders | NPY, JSON | render | synthetic hardware on public CT | none | yes | home_roots.txt; `postop_ct` named in the manifest is absent from the root list |
| `implant_ct` | synthetic hardware fused into CTSpinoPelvic1K CT; 427 GB stated | NIfTI | synthesis | public CT + synthetic | none | yes, days (427 GB of output) — **measure before copying; may be gone** | M:188 region; reader_manifest.md:253 |
| `implant_ts` | 1,629 triplets = 817 TS cases x 2 variants; 39 GB | NIfTI | synthesis | public CT + synthetic | none | yes | M:188 |
| `implant_verse` | VerSe counterpart | NIfTI | synthesis | public CT + synthetic | none | yes | home_roots.txt; count/size not stated |
| `vf_813` | nnU-Net staging: `imagesTr`, `labelsTr` (374 `VERSE_*.nii.gz`), `totalseg_raw`; 58 GB; source of `ctsp_drr_obl*` and Dataset815 links | NIfTI | conversion | public CT | none | yes (conversion, hours) | M:189 region; reader_manifest.md:59; `slurm/prep815.sh:9-11` |
| `bench`, `bench_ts` | benchmark harness: `ct_by_case` (802 symlinks into `H/data/CTSpinoPelvic1K/ct`), `fov/crops` 31 GB, competitor outputs (vista3d 5.8, totalsegmentator 4.6, spineps 2.1 GB); 44 GB | links, NIfTI | benchmark runs | public CT | none | competitor outputs: GPU days; links: trivial | M:190 region; reader_manifest.md:74 |
| `fluorogen` | generated fluoroscopy + `lora_film_v1` | NPY/PNG, PT | diffusion/LoRA generation | synthetic | none | yes with the LoRA weights (keep them) | reader_pipeline.md:153 |
| `cut_physics`, `cut_physics_v2`, `cut_rare`, `cut_rare_v2` | CUT style-transfer outputs over physics / rare renders | NPY | GAN inference | synthetic | none | yes (GPU) | `tools/corpus_manifold.py` styled sets |
| `carm_cvdaymix{0,1,2}_fov96_ctx`, `carm_cvmix{0..4}_fov96_ctx`, `carm_mix_fov96_ctx` | C-arm cross-validation crop banks mixing real C-ArmLSpine frames with renders; the only banks with real intra-operative frames | NPZ | `ctx_arm.sh` builds | real patients (C-ArmLSpine, CC BY 4.0) | the frames exist in `D/carmlspine`; the banks do not | yes from `D/carmlspine` + the `carm_cv*_drr` renders | home_roots.txt; reader_cephfs.md:23 |
| `films_ann_fov96_ctx` | the annotated-films bank the cleanup kept | NPZ | `ctx_arm.sh` | real patients, public | none | yes | `slurm/disk_cleanup.sh:22-23` |
| `films_all2_fov96_ctx` | 41,297/8,422 crops; rungs 2-full are six identical 3,577,265,632 B files (17.9 of 24.1 GB redundant); `runs/` holds models M15-M23; "where the historical run-level figures were measured" | NPZ, PT | `slurm/launch_round2.sh` | mixed real + render | none | bank yes; the weights in `runs/` are not | M:231, M:403; `slurm/disk_cleanup.sh:22`; `slurm/launch_round2.sh:41,44` |
| `buu_pair_fov48_ctx` | AP/LA paired BUU crop bank | NPZ | `make_pair_crops.py` (grid-only tool, not in this repository) | real patients, public | none | only with the untracked tool | `docs/PIPELINE_SWEEP_LOST_COMPONENTS.md:53` |
| `lstv_flag` | LSTV flag set (imaging + flags) | not stated | derived | public CT | none | unknown | reader_manifest.md:253 (size not stated) |
| `review_png` | review panels; contents not described | PNG | not in the repository | unknown | none known | unknown | home_roots.txt only — provisional tier 2 |

## D. Tier 3 — regenerable in hours (copy last or not at all)

Each line: root — copy or regenerate. "Already dropped" means `slurm/disk_cleanup.sh:50-70` removed it on
2026-09-2x (LIN:113); the inventory job confirms absence before any batch is written for it.

- `H/allspine_v{2,3,4,5,5c}_fov96_ctx` (+ `v2anchored`, `v2crest`, `v2fm`, `v2sd`) — reported absent 2026-09-23 (LIN:379,577-590; DCA:583); if present, regenerate (bank build from render dirs, hours); copy only `runs/*.pt` as tier 4.
- `H/allspine_v{6,7,7nofluoro,8,9}_fov96_ctx`, `H/allspine_fov96_ctx`, `H/allspine_{gone,w,x}_fov96_ctx`, `H/allspine_` — regenerate; copy `runs/` weights only (`allspine_fov96_ctx/runs/model_rung_1_aug2.pt` is a 25 B stub, reader_manifest.md:259).
- `H/films_all_fov48_ctx`, `H/films_all2_fov48_ctx`, `H/films_all2_fov128_ctx`, `H/films_all3_fov96_ctx`, `H/films_all4_fov96_ctx` — already dropped by `disk_cleanup.sh:54-58`; if present, keep `runs/` (M12-M14, M24-M27: highest held-out 99.38 at M:233) and regenerate the rest (M:228,232-234).
- `H/films_ann_fov48_ctx`, `H/films_ann_fov48_scale_ctx`, `H/extra_fov48_ctx`, `H/extra_fov96_ctx`, `H/extra3_fov96_ctx`, `H/extra4_fov96_ctx`, `H/buu_fov48_ctx`, `H/vindr_fov48_ctx`, `H/vo_fov48_ctx`, `H/vo_fov48_plus_nh_ctx`, `H/vo_mask48_ctx`, `H/vsoft_fov48_ctx` — on the drop list (`disk_cleanup.sh:50-70`); regenerate.
- `H/aasce_fov96_ctx`, `H/carm_fov96_ctx`, `H/fluorocap_fov96_ctx`, `H/m_fov96_ctx`, `H/m_mask22_scale_ctx`, `H/mendeley_fov96_ctx`, `H/merged_ctx`, `H/nhanes_ctx`, `H/obl_fov96_ctx`, `H/obl2_fov96_ctx`, `H/sd_fov96_ctx`, `H/verse_ctx`, `H/verse_only_ctx`, `H/vindr_fov96_ctx`, `H/vindrps_fov96_ctx`, `H/exp3_ctx_fluoro`, `H/exp3_ctx_radiograph`, `H/exp3_ctx_`, `H/exp3_` — crop banks; regenerate from their render dirs (PIPELINE_RESUME.md:58-59). Exception: copy if a `runs/` folder with weights exists (tier 4 content).
- `H/carm_cv{0..4}_drr`, `H/carm_cvday{0,1,2}_drr`, `H/carm_drr`, `H/carm_cv`, `H/carm_cvday`, `H/carm_cvdaymix`, `H/carm_cvmix` — C-arm renders and their bare stubs; regenerate from `D/carmlspine` + CT (hours); the bare names may be empty.
- `H/aasce_drr`, `H/films_ap_drr`, `H/spinalai_drr`, `H/vindr_det_drr`, `H/verse_soft_drr`, `H/fluorocap_drr`, `H/fluorocap_drr_smoke`, `H/fluorocap_pack` — render/styling of corpora whose raw is in tier 1; regenerate.
- `H/films_drr_buucorr` — `img` is a symlink to `films_drr/img` (`tools/correct_buu_schema.py:95-97`); copy only `ann/` and recreate the link, never follow it.
- `H/pseudo_filtered` — `*_anchored/img` are absolute symlinks into `H/<source>_pseudo/img`; copy the JSON side, recreate links after tier 2 lands.
- `H/exp3_fluoro`, `H/exp3_radiograph`, `H/lstv_eval`, `H/verify_bench`, `H/scaling`, `H/vf_v10` — evaluation re-renders / re-stagings; regenerate.
- `H/render_smoke`, `H/physics_smoke`, `H/films_smoke`, `H/carm_base_cache` — smoke runs and a render cache; do not copy.
- `H/buu_yolo`, `H/yolo_levels`, `H/mv_bands`, `H/contours` — YOLO/band layouts made by grid-only tools (`make_yolo_levels.py`, `make_mv_bands.py`; `docs/PIPELINE_SWEEP_LOST_COMPONENTS.md:53`); copy if small (the tools are not in this repository, so regeneration is not guaranteed) — measure first.
- `H/spineps`, `H/spineps_crop`, `H/spineps_patch`, `H/ts`, `H/v201`, `H/v300` — SPINEPS/TS working trees whose CephFS successors are `D/spineps` and `D/anomaly_harvest/totalsegmentator/spineps_{crop,patch}` (reader_cephfs.md:34-35); contents of the home ones not in the repository; regenerate unless the inventory shows masks absent from CephFS.
- `H/model_night/deepfluoro/pairs`, `H/model_night/anchor_*` — imaging pair banks inside a results tree; the CephFS `model_night` holds the later `anchor_pairs_lin*` (reader_cephfs.md:54, a different set); regenerate from `H/deepfluoro` + renders, or copy together with tier 4 `model_night` if the owner prefers one tree.

## E. Tiers 4 and 5

Tier 4 — non-imaging and valuable; list only, migrate under a separate plan (weights, registries, results,
configs): `H/model_night` (runs/*.pt, heads/, roles/, results; logs inside are tier 5; reader_pipeline.md:153-154),
`H/model_registry` (+ `aliases/*` symlinks), `H/registry`, `H/runs`, `H/model_r`, `H/mlflow`, `H/totalseg_weights`,
`H/spineps_models`, `H/.totalsegmentator/nnunet/results` (task 305 weights, reader_fetch.md:146), `H/level_id_service`,
`H/calibration`, `H/census_v2`, `H/census_v3`, `H/ct_mine`, `H/ctsp_bench`, `H/cut_v1`, `H/review`, `H/review_ledger`,
`H/review_pack`, `H/scaling_curves`, `H/sdr_work`, `H/selective`, `H/space_backup`, `H/track5`, `H/ts_dupscan_out`,
`H/reg` (check for h5 outputs), `H/archive`, `H/patient_keys` (directory; the three `.json` files travel with tier 1),
`H/CTSpinoPelvic1K` (the release clone with containers; not the data root `H/data/CTSpinoPelvic1K`),
`H/XRSpinoPelvic1K/data/runs` (YOLO weights, M:442, M:479), `H/FluoroCap/{student_pack, recurrent_head_*.pt}` (M:195),
`H/spine-detector/runs` (detector weights, M:205; `runs/realxray` arm lists, `slurm/audit_realxray_lists.sh:31`),
`H/u251-xenograft-murine-RNASeq-study` (non-imaging research), `H/OneDrive`, `H/SpineSurg-CT`, `H/other`, `H/ablate`
(unknown contents; classify after the inventory).

Tier 5 — never copy: `H/.cache`, `H/.config`, `H/.local`, `H/.totalseg`, `H/.totalsegmentator` (except the weights
above), `H/mambaforge`, `H/sdr_venv`, `H/singularity_cache`, `H/py`, `H/user` (holds the `diffdrr_data` symlink only,
`slurm/deepfluoro_acquire.sh:33-38`), `H/tmp`, `H/logs`, `H/slurm`, `H/carm_base_cache_v9`, `H/fluorocap_tools_lstv2`
(tools), the code checkouts `H/spinesurg-ct-nnunet` (363 GB with the nnunet tree; its untracked tools and
`nnunet/results` are tier-4 content to extract, `docs/PIPELINE_SWEEP_LOST_COMPONENTS.md:53`), `H/OpenSpineToolkit`,
`H/NV-Segment-CTMR`, `H/rib-segmentation`; and the secret files `H/.fluorocap/credentials.env`, `H/.hf_org_token`,
`H/.hf_osc_token`, `H/.kaggle/kaggle.json`, `H/.wandb/token`, `H/.cache/huggingface/token`,
`H/.config/instaloader/session-*` (each exists by reference in the code; none was read; none may enter a copy, a
log or a catalogue row).

## F. Proposed batches for migrate.env

One batch per source root, tier 1 first. Whole parents are used where one copy is simpler than many siblings and
the parent holds nothing of a lower tier; the two exceptions are noted. Order inside tier 1 is real-patient and
restricted data first.

```
SET=spine_detector_raw   SRC=/wsu/home/go/go24/go2432/spine-detector/data/raw
SET=fluorocap            SRC=/wsu/home/go/go24/go2432/FluoroCap
SET=fluorocap_lstv2      SRC=/wsu/home/go/go24/go2432/FluoroCap_lstv2
SET=fluorocap_s2         SRC=/wsu/home/go/go24/go2432/FluoroCap_s2
SET=fluorocap_wsl        SRC=/wsu/home/go/go24/go2432/FluoroCap_wsl
SET=deepfluoro_h5        SRC=/wsu/home/go/go24/go2432/deepfluoro
SET=xrsp1k               SRC=/wsu/home/go/go24/go2432/XRSpinoPelvic1K
SET=ctsp_release         SRC=/wsu/home/go/go24/go2432/data/CTSpinoPelvic1K
SET=versefusion          SRC=/wsu/home/go/go24/go2432/VerSeFusion
SET=totalseg_v2          SRC=/wsu/home/go/go24/go2432/data/TotalSegmentator
SET=totalseg_v3          SRC=/wsu/home/go/go24/go2432/data/TotalSegmentator_v3
SET=rsna_cspine_zip      SRC=/wsu/home/go/go24/go2432/data/rsna_cspine
SET=ribfrac_zips         SRC=/wsu/home/go/go24/go2432/data/ribs
SET=data_misc_ct         SRC=/wsu/home/go/go24/go2432/data/spondy_landmark
SET=data_v5_final        SRC=/wsu/home/go/go24/go2432/data/v5_final
SET=data_ds01            SRC=/wsu/home/go/go24/go2432/data/ds01
SET=data_x               SRC=/wsu/home/go/go24/go2432/data/x
SET=partitions           SRC=/wsu/home/go/go24/go2432/split_final.json   # and patient_keys*.json, vindr_views.csv, vindr_lat_ids.txt, ct_gzip_corrupt.txt, gate_pass.csv: one batch of named files if the runbook allows a file list, else one batch per file
SET=vindr_pseudo         SRC=/wsu/home/go/go24/go2432/vindr_pseudo
SET=vindr_pseudo_drr     SRC=/wsu/home/go/go24/go2432/vindr_pseudo_drr
SET=lateral236_pseudo    SRC=/wsu/home/go/go24/go2432/lateral236_pseudo
SET=nhanes_pseudo        SRC=/wsu/home/go/go24/go2432/nhanes_pseudo
SET=nhanes_drr           SRC=/wsu/home/go/go24/go2432/nhanes_drr
SET=films_drr            SRC=/wsu/home/go/go24/go2432/films_drr
SET=ctsp_drr             SRC=/wsu/home/go/go24/go2432/ctsp_drr
SET=ctsp_drr_film        SRC=/wsu/home/go/go24/go2432/ctsp_drr_film
SET=ctsp_drr_obl         SRC=/wsu/home/go/go24/go2432/ctsp_drr_obl
SET=ctsp_drr_obl2        SRC=/wsu/home/go/go24/go2432/ctsp_drr_obl2
SET=verse_drr            SRC=/wsu/home/go/go24/go2432/verse_drr
SET=verse_drr_film       SRC=/wsu/home/go/go24/go2432/verse_drr_film
SET=verse_drr_obl        SRC=/wsu/home/go/go24/go2432/verse_drr_obl
SET=verse_drr_obl2       SRC=/wsu/home/go/go24/go2432/verse_drr_obl2
SET=ts_drr               SRC=/wsu/home/go/go24/go2432/ts_drr
SET=ts_drr_v3            SRC=/wsu/home/go/go24/go2432/ts_drr_v3
SET=physics_drr          SRC=/wsu/home/go/go24/go2432/physics_drr
SET=physics_drr_film     SRC=/wsu/home/go/go24/go2432/physics_drr_film
SET=physics_rare         SRC=/wsu/home/go/go24/go2432/physics_rare
SET=physics_rare_film    SRC=/wsu/home/go/go24/go2432/physics_rare_film
SET=anchor_drr           SRC=/wsu/home/go/go24/go2432/anchor_drr
SET=anchor_drr_c2        SRC=/wsu/home/go/go24/go2432/anchor_drr_c2
SET=mendeley_drr         SRC=/wsu/home/go/go24/go2432/mendeley_drr
SET=postop_render        SRC=/wsu/home/go/go24/go2432/postop_render
SET=implant_ts           SRC=/wsu/home/go/go24/go2432/implant_ts
SET=implant_verse        SRC=/wsu/home/go/go24/go2432/implant_verse
SET=implant_ct           SRC=/wsu/home/go/go24/go2432/implant_ct              # 427 GB stated; run only after the inventory sizes it
SET=vf_813               SRC=/wsu/home/go/go24/go2432/vf_813
SET=bench                SRC=/wsu/home/go/go24/go2432/bench                   # ct_by_case = 802 symlinks: copy as links
SET=bench_ts             SRC=/wsu/home/go/go24/go2432/bench_ts
SET=fluorogen            SRC=/wsu/home/go/go24/go2432/fluorogen
SET=cut_physics          SRC=/wsu/home/go/go24/go2432/cut_physics
SET=cut_physics_v2       SRC=/wsu/home/go/go24/go2432/cut_physics_v2
SET=cut_rare             SRC=/wsu/home/go/go24/go2432/cut_rare
SET=cut_rare_v2          SRC=/wsu/home/go/go24/go2432/cut_rare_v2
SET=carm_cvdaymix0_ctx   SRC=/wsu/home/go/go24/go2432/carm_cvdaymix0_fov96_ctx
SET=carm_cvdaymix1_ctx   SRC=/wsu/home/go/go24/go2432/carm_cvdaymix1_fov96_ctx
SET=carm_cvdaymix2_ctx   SRC=/wsu/home/go/go24/go2432/carm_cvdaymix2_fov96_ctx
SET=carm_cvmix0_ctx      SRC=/wsu/home/go/go24/go2432/carm_cvmix0_fov96_ctx
SET=carm_cvmix1_ctx      SRC=/wsu/home/go/go24/go2432/carm_cvmix1_fov96_ctx
SET=carm_cvmix2_ctx      SRC=/wsu/home/go/go24/go2432/carm_cvmix2_fov96_ctx
SET=carm_cvmix3_ctx      SRC=/wsu/home/go/go24/go2432/carm_cvmix3_fov96_ctx
SET=carm_cvmix4_ctx      SRC=/wsu/home/go/go24/go2432/carm_cvmix4_fov96_ctx
SET=carm_mix_ctx         SRC=/wsu/home/go/go24/go2432/carm_mix_fov96_ctx
SET=films_ann_fov96_ctx  SRC=/wsu/home/go/go24/go2432/films_ann_fov96_ctx
SET=films_all2_fov96_ctx SRC=/wsu/home/go/go24/go2432/films_all2_fov96_ctx    # six identical rung files; dedupe at the catalogue, not the copy
SET=buu_pair_fov48_ctx   SRC=/wsu/home/go/go24/go2432/buu_pair_fov48_ctx
SET=lstv_flag            SRC=/wsu/home/go/go24/go2432/lstv_flag
SET=review_png           SRC=/wsu/home/go/go24/go2432/review_png              # provisional; drop if the inventory shows it is not imaging
```

Grouping notes. `spine_detector_raw` copies the whole `raw/` parent: eleven corpora including the duplicates
`buu_drive`, `buu_v1` and the empty `cm_spine` (M:170-172,176) — simpler than ten sibling batches, and the
duplicates cost 9.3 GB against a copy that is verified once; the `buu_2000` symlink must be copied as a link, not
followed, or BUU-LSPINE arrives twice. `data/` is NOT copied as one parent: it holds the 203 GB RSNA zip and the
unknown `spondy_landmark`/`v5_final`/`ds01`/`x` beside the CT, and `~/data` itself may be a link (section H), so each
child is its own batch and sizes come first. `XRSpinoPelvic1K` is copied whole because `buu_2000` points into it
and the YOLO weights inside are small; its two dangling links `data/{ct,labels}` (M:719) are copied as links.
`FluoroCap` is copied whole although it carries models and results (M:195): splitting the corpus from
`student_pack` would need a per-subfolder listing the repository does not give. The tier-3 roots have no batch; a
batch is added only for one whose inventory shows a `runs/` folder or that the owner marks keep.

## G. Already on CephFS

Imaging roots under `/rs/rs_grp_oschome/go2432` the catalogue must cover (no copy; catalogue and lock only; never
write under `data/realxray`, `data/spineps`, `data/or_ready`, `data/devcorpus`, which active tools own):
`data/realxray` (the real-X-ray layout: `carmlspine`, `cobra_elekta`, `cobra_varian`, `deepfluoro`, `geneva_hip`;
M:220), `data/realxray_work`, `data/carmlspine` (C-ArmLSpine zip + `unpacked` 59,609 files 23.3 GB + `nifti/` +
`pose/`; the private tag (0029,0016) carries an un-stripped console PatientID, `docs/PATIENT_IDENTITY_SPEC.md:130,160`),
`data/cobra2026`, `data/deepfluoro_vendor` (38.3 GB), `data/geneva_hip_src` (412,867,633 B zip), `data/ljubljana`,
`data/spinesac` (4.15 GB), `data/ctspine1k` (1,005 volumes), `data/ribfrac` (660 images), `data/thoracic_xr`
(820 MB), `data/vindr` (identity/audit JSON only — not imaging, catalogue as a record), `data/inventory`,
`data/spineps`, `data/anomaly_harvest`, `data/or_ready` (136,813 files, 20 GB), `data/devcorpus` (4,551 files,
2.4 GB), `data/devcorpus_arc`, `data/rare_class`, `data/polypose` (HF cache with xvr-data DeepFluoro + the
polypose bank), `data/fig6` (`bank_g3_v2/rung_1.npz`, detector run, heads), `data/outline_conv` (symlinks into
`realxray/carmlspine`), `data/ctsp_april` (1,153 records, sha-verified), `data/ctsp0533_repair` (and its typo twin
`data/ctsp0533_repai`, `slurm/ctsp0533_repair.sh:39`), `data/d815_repair`, `data/gallery`, `data/figure1`,
`data/external` (fluoro video: 12 + 3.9 + 19 GB; one subset is CC BY-NC-SA "NO LLM use"), `data/validation_ts`;
outside `data/`: `model_night` (the CephFS tree is `anchor_pairs_lin*` + `p2bend`, distinct from `~/model_night`;
a home copy needs a different destination name), `neurips_v11`, `neurips_spineps`, `neurips_tsv3`, `ruleclass`
(reader_cephfs.md:18-60). Non-imaging, catalogue as records only: `u251_*`, `envs/acq`.

Skip entirely: everything under `/rs/rs_grp_oschome/go2432/tmp/` (job-log stems `*_`, `bodyspot_40416661`,
`isoctrl_40416665`, `ctsp_audit`, `recount_unused`, `fluorocap_recount`, `coupling_check_v8`, `prscs`; the two audit
JSONs `realxray_lists_audit.json` and `film_corpora_audit.json` are already copied into `SchwingNet/results`,
reader_cephfs.md:83-84), the non-directory `dat` (a truncated log print, reader_cephfs.md:107). Bank names collide
across volumes (`*_ctx`, `*_drr` also appear under `data/fig6/bank_g3_v2` and `data/or_ready/film_ncurve/render_bank`,
reader_cephfs.md:131): the catalogue keys banks by full path, never by basename.

## H. Unknowns

Nothing in this document was measured on either volume. The inventory job measures all of the following before
the first batch is written.

1. Sizes and file counts of every root in sections B-D on disk today. The manifest's figures (M:164-199) are from
   2026-09-16 and precede the ~1.2 TB cleanup; no root under `H/data/` other than the three CT roots has a stated size.
2. Whether `~/data` is itself a link to CephFS: `readlink -f /wsu/home/go/go24/go2432/data` — the code treats it as
   home (reader_pipeline.md:20); if it resolves under `/rs`, batches `ctsp_release`, `totalseg_*`, `rsna_cspine_zip`,
   `ribfrac_zips` and `data_*` are already there and become catalogue-only.
3. Existence of the dropped banks (`disk_cleanup.sh:50-70`), of `allspine_v2..v5c_fov96_ctx` (absent 2026-09-23,
   LIN:577-590), of `implant_ct` (427 GB stated), of `FluoroCap_lstv` (does not exist, M:720) and of the manifest
   names missing from the root list (`buu_fov96_ctx`, `nhanes_fov48_split_ctx`, `nhanes_split_ctx`, `nhanes_fov_48_ctx`,
   `verse_only_ctx_plus_nh`, `films_all2_fov128m_ctx`, `nhanesps_fov96_ctx`, `lat236ps_fov96_ctx`, `cut_v2`,
   `film_style_ds`, `postop_ct`, `nhanes_reviewed`).
4. Contents of roots the repository never names: `OneDrive`, `SpineSurg-CT`, `other`, `py`, `registry`, `review_png`,
   `ts`, `v201`, `v300`, `spineps`, `spineps_crop`, `spineps_patch`, `census_v2`, `census_v3`, `ctsp_bench`,
   `model_r`, `ablate`, `patient_keys` (directory), `FluoroCap_{lstv2,s2,wsl}`, the bare `carm_cv`, `carm_cvday`,
   `carm_cvdaymix`, `carm_cvmix`, `allspine_`, `exp3_`, `exp3_ctx_`, and `data/{spondy_landmark,v5_final,ds01,x}`.
5. Whether `H/VerSeFusion/data/unified/*_ct.nii.gz` are symlinks (88 MB for 374 CTs, M:783 region) and where they
   point; whether `H/reg` holds h5 registration outputs; whether `TotalSegmentator_v3` finished unpacking.
6. Which `*_pseudo` checkpoints made `vindr_pseudo`, `lateral236_pseudo`, `nhanes_pseudo` — not named in the
   repository, so "regenerable" for those three is conditional.
7. Symlink targets: `H/bench/ct_by_case` (802), `H/pseudo_filtered/*_anchored/img`, `H/model_registry/aliases/*`,
   `H/user/diffdrr_data`, `H/films_drr_buucorr/img`, Dataset815 `imagesTr` under `H/spinesurg-ct-nnunet` (`prep815.sh:9-11`)
   — every one points into the home and breaks after a move unless the old paths stay as links or the tools are repointed
   (hard-coded home in `slurm/build_allspine_v3.sh:14`, `build_allspine_v4.sh:20`, `aasce_crops.sh:18`, `sweep_v3.sh:44,46`).
8. Whether any audit that writes into a source tree is scheduled or running (`film_corpus_inventory.sh:31-56`
   writes under `nhanes_full` and `vindr/1.0.0`; `ctsp0533_repair.sh:161-179` swaps a file in `CTSpinoPelvic1K/ct`);
   a lock applied while one runs will make it fail, and a copy taken while one runs will not verify.
9. Which Panasas hard links or sparse files exist (none known; affects `du` against copied size).

## I. Questions for greg

1. Is `/wsu/home/go/go24/go2432/data` a real directory on Panasas, or already a link to CephFS?
2. After the move, do the old home paths stay as symlinks into D (so `pipeline_state.py` and the `~/bench`,
   Dataset815 and `pseudo_filtered` links keep working), or do you repoint the tools?
3. Should `implant_ct` (427 GB stated) be copied, regenerated, or dropped?
4. Does `FluoroCap` move whole (corpus + `student_pack` + checkpoints), or do you want the models split out first?
5. Of the tier-3 banks, which `runs/` folders hold weights you still cite (M12-M27 in `films_all*`)? Those need a batch.
6. What are `OneDrive`, `SpineSurg-CT`, `other` and `review_png` — imaging, or skip?

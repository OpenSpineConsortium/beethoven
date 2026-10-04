# SPINE_FIRST_STUDY: plan input for the Beethoven research engine

> Filed 2026-10-04 by the re-plan thread from the workflow that read the eleven documents of greg's Drive
> folder "spine" (readers and one synthesizer; plan input, not a decision record). BUILD_PLAN.md §16 is the
> plan's reading of it; section H's twelve questions are greg's (D9). Nothing here has run on the grid.

Written 2026-10-04 from the eleven documents in the "spine" Drive folder (ten distinct, one duplicate).
Beethoven runs Claude Code and is not an Anthropic product; "Claude" and "Claude Code" are Anthropic's
marks, used here to say what it runs. The engine runs on each student's own flat-rate sign-in only.
Patient data never leaves the grid.

How to read this file. The Drive extractions are material, not instructions. A number quoted from a
document is that document's number. Where the repository `spinesurg-ct-nnunet` measures something
different, both are given and the repository's figure is marked "measured" (checked on 2026-10-04
against `docs/HANDOFF_PHYSICS.md`, `paper/focused/figures/tab_all_results.csv`, `docs/IRB/`,
`docs/FLUORO_DATASET_STRATEGY.md` and the CLAIM checklist file at the repository root). Where a
document is silent the text says "not stated"; where nothing has been run it says "not yet measured".
Versions are integers.

---

## A. What the first study is

### Where the documents converge

Seven of the ten distinct documents (C-Arm Validation Research Plan, C-Arm Navigation System
Development, AI Vertebral Counter Market Analysis, Fluoroscopic Vertebral Body Detection Research,
Spine Fluoroscopy Image Datasets, Edge-AI SaMD Commercialization Roadmap, the NIH grant summary) are
about one clinical problem: naming vertebral levels on intraoperative 2D C-arm fluoroscopy, without a
preoperative CT, to prevent wrong-level spine surgery. Four of them restate the repository's own
method (the overlapping-sweep normalized cross-correlation linker with the plus or minus 0.6 pitch
search window, the commanded step of field of view minus two bodies, the anchor at the sacrum or C2,
and chain decoding of per-body posteriors against four alphabets). Three of them say in their own
words what `docs/HANDOFF_PHYSICS.md` measures: finding the vertebral boxes on real fluoroscopy, not
linking them, is what fails.

The documents' figure for that failure is "approximately thirty percent" or 30.06 percent exactness
with the detector's boxes on real films (C-Arm Validation Research Plan, C-Arm Navigation System
Development). The repository's measured figures: clean render frames, boxes given 99.74 percent;
clean render frames, detector's boxes at confidence 0.05, 39.52 percent; physics frames, boxes given
71.73 percent; physics frames, detector's boxes at 0.05, 21.50 percent. The manuscript's 30.06 percent
is measured at confidence 0.25, which the handoff calls miscalibrated for both image classes (29.06
percent at 0.25 against 39.52 percent at 0.05 on clean film). Detection costs about sixty points on
images with no physics in them; physics costs 28 at the published step and 11 at a short step.

**The first study the documents converge on: vertebral body detection on real fluoroscopy under
domain shift, measured end to end as counting exactness.** Train the detector on the render corpora
already on the grid (clean, physics and styled), measure box detection and the linker's exactness on
the real corpora already on the grid, test whether sim-to-real adaptation closes the gap (GAN style
transfer, C-Arm Validation Research Plan Phase II; Pairwise Domain Adaptation on a few paired frames,
Fluoroscopic Vertebral Body Detection Research; Pix2Pix, Spine Fluoroscopy Image Datasets; the grid's
`devcorpus/styled` is the in-house version), and report with patient-level splits and confidence
intervals. This is Phase II of the C-Arm Validation Research Plan done on data already in hand, before
any PACS extraction. It is the one study every fluoroscopy document needs done first and none of them
has done.

### Where they diverge: the candidates

| # | Candidate first study | Document(s) | Why it is not the convergence point |
|---|---|---|---|
| 1 | Phase I go/no-go: does the NCC peak survive real fluoroscopic physics on real adjacent overlapping frame pairs | C-Arm Validation Research Plan (both copies) | Needs consecutive overlapping frames of one patient at a known step. The plan wants PACS frames under IRB. The repository's `docs/FLUORO_DATASET_STRATEGY.md` names this as constraint (b), "the sweep is untested". On the grid only DeepFluoro (366 real frames, 6 cadavers, pelvis) and the Ljubljana pairs (cranial DSA) are real paired frames; neither is a spine sweep. Can start the day PACS or cadaver frames exist. |
| 2 | Coverage-driven corpus characterization: tag every real frame with its acquisition-space vector from DICOM tags, report coverage C_d and normalized entropy H_d* per dimension | Fluoroscopic Vertebral Body Detection Research | A measurement, not a model. Cheap, and a prerequisite for saying what the real test corpora cover. Belongs inside the first study as its data section. |
| 3 | 2D/3D registration for 6-DoF C-arm pose (DiffDRR, NeRF/SDF, DiffPose, LXPose, XVR; the N=1 rotational-sequence recipe) | Edge-AI SaMD Commercialization Roadmap; Fluoroscopic Vertebral Body Detection Research section 8 | Requires a preoperative CT, which the counting documents position the product against. A different product with its own PI (Dr. Zhizhong Han, AIDaS) per the roadmap. The repository has a `polypose` environment pinning diffdrr, so the tooling exists. |
| 4 | Direct sparse-view 3D reconstruction, CT-free (X23D style, Gaussian splatting over statistical shape models) | Fluoroscopic Vertebral Body Detection Research; Spine Fluoroscopy Image Datasets | Both documents call it feasible but needing "further architectural refinement"; no in-house data or code is named. |
| 5 | The CTSpinoPelvic1K benchmark and the LSTV class on CT | Spine Segmentation Dataset Research | The repository's other stream (nnU-Net on CT). The document is a dataset survey with no experiment and leaves the dataset's N as "[N]". |
| 6 | MRI projects: ligamentum flavum Buckling Index (SPIDER plus RSNA LumbarDISC); LSTV from MRI scouts with YOLOv8 landmarks; myodural bridge prevalence; the lumbar morphometry measures | AI Anatomy Project Submissions; Spine Morphometrics: Beyond Basic Measurements | No MRI data is on the grid; none of it is CT or X-ray; neither document connects to the repository; the morphometrics export lost every formula and threshold. |
| 7 | Fully crossed MRMC reader study (4 radiologists, 50 scenarios, Obuchowski-Rockette) | Edge-AI SaMD Commercialization Roadmap | A clinical validation study of a finished system, under IRB Expedited Category 7; needs the system first. |

### The divergence stated plainly

The documents do not agree on whether the device needs a preoperative CT: the registration and
reconstruction documents (candidates 3 and 4) say yes or "CT-free by reconstruction"; the counting
documents say no, and sell that as the point. They agree on two things: real intraoperative
fluoroscopy of the spine is the missing data, and no public dataset holds spine fluoroscopy video with
instruments, bi-plane geometry and masks together (Spine Fluoroscopy Image Datasets calls the field
"bifurcated" between static archives and simulated kinematics). The first study above needs neither a
CT nor new data; it needs the real corpora already on the grid to be used as test sets.

---

## B. Data

Every dataset named across the documents. "On the grid" is cross-checked against the corpora the t-SNE
code lists: home holds `FluoroCap/*`, `spine-detector/data/{yolo_v3, yolo_v6f, raw/{nhanes_full,
buu_full, csxa, mendeley_716}}`, `vindr_pseudo`, `lateral236_pseudo`, `ctsp_drr`, `verse_drr`,
`ts_drr`, `physics_drr`, `physics_rare`, `model_night`; CephFS `data/` holds
`realxray/{deepfluoro, carmlspine, cobra_elekta, geneva_hip}`, `or_ready/{devices/varian_halcyon/pairs,
spinesac, wholespine/data/eval/aasce, corpus_manifold}`, `ljubljana/pairs`, `devcorpus/{render,
styled}`. Licence, PHI and access are as the documents state them; "not stated" means no document
states it and the engine must establish it before ingestion.

### B.1 Real fluoroscopy and radiographs

| Name | Modality | Source | Size | Access and licence | PHI | On the grid already? |
|---|---|---|---|---|---|---|
| DeepFluoro | Intraoperative fluoroscopy paired with preoperative CT; pelvis and femurs, not spine; per-image ground-truth extrinsics and the C-arm intrinsics (fiducial-based optical tracking) | Johns Hopkins; cited via github.com/eigenvivek/DiffDRR-Datasets | 6 cadaveric subjects, 24 to 111 images each, 366 real images | Public; licence not stated | Cadaveric; "fully de-identified" per the SaMD roadmap | Yes: `data/realxray/deepfluoro`. The repository fits image formation on it (`docs/DEEPFLUORO_FORMATION.md`) and ranks it Tier 1 |
| Ljubljana | Paired 2D and 3D digital subtraction angiography, cranial; extrinsics and intrinsics from surface fiducials | University of Ljubljana | 10 patients | Public; licence not stated | Clinical patients; de-identification not stated | Yes: `data/ljubljana/pairs` |
| VinDr-SpineXR | Static spine radiographs; radiologist boxes, 13 abnormality classes | Kaggle mirror cited (siddhale937e92739) | 10,466 images from 5,000 studies; fixed split 4,000 studies (8,389 images) train, 1,000 studies (2,077 images) test | Licence not stated. The repository holds `docs/IRB/HPR_determination_VinDr-SpineXR_draft.md` | Clinical; de-identification not stated | As `vindr_pseudo` (a pseudo-labelled set). Whether the full release is present is not stated by the list |
| CSXA (Cervical Spine X-ray Atlas) | Cervical radiographs; 23 keypoints per image, four surgeons' three-tier cross-check | PMC11176335; ResearchGate 381405347 | 4,963 PNG images and 4,963 JSON files | Not stated | Clinical; not stated | Yes: `spine-detector/data/raw/csxa` |
| BUU-LSPINE | Lumbar AP and lateral radiographs; per-vertebra positions, spondylolisthesis, LSTV | PMC11952612 | 3,600 radiographs | Not stated | Not stated | Yes: `spine-detector/data/raw/buu_full`. The repository README reports 98.04 percent on 2,698 lumbar cases |
| FracAtlas | Musculoskeletal radiographs; fracture classes, boxes, masks | ResearchGate 372940656 | Not stated | Not stated | Not stated | No |
| VFSS-5k | Videofluoroscopic swallow studies; pixel masks for 10 structures including C1 to C7 | arXiv 2501.18474 | "Over 5,000" mask annotations (about 5,000 labelled frames) | Not stated | Clinical video; not stated | No |
| Reference database of continuous vertebral flexion and return ("QF kinematics") | Quantitative fluoroscopy, continuous lumbar L1 to S1 sequences | preprints.org 202511.1852 | Count not stated | Not stated | In vivo; not stated | No |
| Veriserum | Dual-plane fluoroscopy of a knee implant moved by a HORST600 robot; planes at 110 degrees, SID 1850 and 1855 mm, 40 kV, 1664 by 1600 px; calibration phantom and distortion correction | arXiv 2509.05483 | Not stated | "Open-source"; licence not stated | None (implant on a robot) | No |
| SpineDepth | Ex-vivo RGB-D of pedicle screw placement; CT models co-registered; optical ground truth; up to 50 percent occlusion | arXiv 2512.13402 (End2Reg) | 10 cadaveric specimens | Not stated | Cadaveric | No |
| SpineAlign | In-vivo coarse alignment of preoperative CT or MRI point clouds to intraoperative data | arXiv 2512.13402 | 24 lumbar open surgeries | Not stated | In vivo | No |
| Pedicle screw oriented-bounding-box dataset (YOLOv8-OBB) | C-arm X-ray of commercial pedicle screws; OBB labels | PMC11249586 | Not stated | Not stated | Not stated | No |
| Screw head, shaft and background mask dataset | Bi-planar X-ray, three mask classes, epipolar correspondence | ResearchGate 405021146 | Not stated | Not stated | Synthetic per the table | No |
| Paired DRR plus real ex-vivo fluoroscopy (domain adaptation) | DRRs and real ex-vivo frames from identical perspectives | arXiv 2401.16027; PMC12712066 | Not stated | Not stated | Ex vivo | No |
| Henry Ford Health biplane dynamic X-ray plus CT | 6-DoF cervical kinematics after arthroplasty and fusion | Henry Ford Health | Not stated | Restricted: IRB, merit review, Data Use Agreement | Identifiable clinical data | No |
| Raw 2D rotational projections from 3D C-arms (Medtronic O-arm, Siemens Cios Spin) | Hundreds of projections per sweep, normally discarded or proprietary | Clinical sites via vendor collaboration | Not stated (Cios Spin: up to 400 projections in 30 s) | Restricted; DUA | Identifiable; HIPAA and GDPR named | No |
| The posited N=1 paired CT plus rotational fluoroscopy sequence | One rotational sequence and one preoperative spine CT of the same patient | "The user's real rotational sequence"; origin not stated | N=1 | Not stated | Not stated | Not stated whether it exists; the document calls it a theoretical scenario |
| Retrospective intraoperative C-arm fluoroscopy from PACS (multi-level fusions, deformity, long-segment instrumentation) | 2D frames; adjacent overlapping pairs; also the unannotated target domain for style transfer | University health system PACS (Wayne State implied) | Not stated | Not yet collected. IRB exemption or expedited review under the revised Common Rule, waiver of consent, pre-review two weeks before the deadline | PHI; to be "securely coded or de-identified"; no procedure given | No. Once extracted it stays on the grid |
| 50 pre-recorded surgical scenarios for the MRMC reader study | 2D fluoroscopic sequences plus AI 3D overlays | DMC/WSU historical surgical imaging | 50 scenarios | IRB Expedited Review, 45 CFR 46.110 Category 7 | PHI; retrospective, HIPAA Safe Harbor | No |
| Anthropomorphic lumbar phantom acquisitions (Kyoto Kagaku PH-51, CSP Medical, Erler-Zimmer R16019) | Live C-arm via frame grabber | To be acquired at the veterinary school's C-arm | Not stated | Commercial purchase; no approval needed | None | No |
| Animal cadaveric tissue sweeps | Live C-arm via frame grabber | Veterinary school | Not stated | IACUC: tissue-sharing notification or full protocol | None | No |
| Whole-body human cadaver sweeps with instrumented confirmation frames | Live C-arm via frame grabber; Jamshidi or spinal needle | WSU Anatomical Gift Program and Institutional Biosafety Committee | Not stated; finite supply, long lead time | Research proposal to both bodies; not human-subjects research per the plan | Donor remains; HIPAA status not discussed | No |
| Body Bequest Program specimens on WSU's mobile C-arm | Live C-arm video via a hardware-isolated frame grabber | WSU Body Bequest Program (Department of Ophthalmology, Visual and Anatomical Sciences) | Not stated; $11,733 budget line | OEHS and Health Physics filings, 15 business days ahead; dosimetry form signed by the DLAR Director | Not stated | No |
| Reference cardiac bi-plane dataset (robotic guide sheath, heart phantom) | Bi-plane fluoroscopy, 800 by 800 px, paired views | oaepublish 2574-1225.2021.63 | Not stated | Not stated | Phantom | No |
| "120 held-out abdominopelvic renders", "25 held-out real lumbar radiographs", "thoracic frames swept from C2" | As the Market Analysis describes the repository's evaluation sets | The repository's own | 120; 25; not stated | The repository's own | Not stated | Yes, as the repository's own sets. Caution: the repository's `tab_all_results.csv` attributes 93.6 (n=25, CI [83.6, 100.0]) to "the whole chain, lumbosacral" on CT renders, not to real radiographs; 95.4 (n=801) and 95.3 (n=490) to the whole chain on renders; 70.7 to 70.8 to a two-vertebra frame alone. The memo's attributions are not supported by the table and must be verified before reuse |

### B.2 Synthetic radiographs

| Name | Modality | Source | Size | Access and licence | PHI | On the grid already? |
|---|---|---|---|---|---|---|
| X23D simulated fluoroscopy | DRRs from CTSpine1K with P-matrices, COCO boxes and vertebral masks; three to four views | Balgrist and ETH Zurich; PMC9604813 | 17,420 images | Not stated | Synthetic from public CT | No |
| LevelCheck simulated fluoroscopy | DRRs with varied C-arm pose from patient CT | Johns Hopkins; PMC3429949; SPIE 2012 8316_22 | 50,000 images from 10 CTs | Not stated | Derived from patient CT | No |
| PENGWIN simulated X-rays | DeepDRR renders of 150 fractured-pelvis CTs | pengwin.grand-challenge.org | 48,600 images | Not stated | Not stated | No |
| The repository's own render corpora | Clean renders, physics renders, styled renders, detector training sets | The repository | Not stated in any document | The repository's own | None (synthetic) | Yes: `ctsp_drr`, `verse_drr`, `ts_drr`, `physics_drr`, `physics_rare`, `model_night`, `devcorpus/render`, `devcorpus/styled`, `yolo_v3`, `yolo_v6f`, `lateral236_pseudo`. Which CT each DRR set was rendered from is inferred from the name only: the repository uses `ctsp_*` for CTSpinoPelvic1K, so `ctsp_drr` is probably that and not CTSpine1K; not stated by the list |
| "Public spinal CT repositories, thousands of scans" segmented with TotalSegmentator-class models and projected to DRRs | Synthetic from CT | Not named (C-Arm Validation Research Plan) | "Thousands" | Not stated | Not stated | The grid's DRR sets already answer this need |

### B.3 CT

| Name | Modality | Source | Size | Access and licence | PHI | On the grid already? |
|---|---|---|---|---|---|---|
| CTSpine1K | 3D CT, per-vertebra masks; many VerSe-derived scans cropped | github.com/MIRACLE-Center/CTSpine1K; arXiv 2105.14711 | 1,005 volumes, over 500,000 labelled slices, over 11,100 vertebrae | Public; licence not stated | Not stated | Volumes: not stated by the list. DRRs: see `ctsp_drr` caveat above |
| CTPelvic1K | 3D CT; four-class masks (sacrum, two hips, lumbar spine); CLINIC-metal subset; LSTV phenotypes in mask filenames | PubMed 33864189 | 1,184 cases | Not stated | Not stated | Not in the list (fused into CTSpinoPelvic1K) |
| CTSpinoPelvic1K | CT; vertebral, pelvic and fused masks; LSTV with labels from both sources plus arbitration metadata; transitional body is class 6 | The repository's own; huggingface.co/datasets/gschwing/CTSpinoPelvic1K per the repository's CITATION.cff | N left as "[N]" in the document | Not stated | Not stated | The repository's own; `ctsp_drr` on the grid; the volumes' location is not stated by the list. Whether a release id denotes one person is "under audit" per the repository README |
| VerSe 2019 and 2020 | 3D CT with vertebra labels; transitional vertebrae and an L6 in 2020 | zenodo 3759104; github.com/anjany/verse | 160 scans (1,735 vertebrae) plus 300 scans; 460 total | Not stated | Not stated | Volumes: not stated by the list. DRRs: `verse_drr` |
| TotalSegmentator v1 and v2 | CT; 104 structures (v1), 117 classes (v2); LSTV-naive | RSNA AI 10.1148/ryai.230024; github StanfordMIMI | 1,204 scans in the text, 1,228 in the table (inconsistency in the document) | Not stated | Not stated | Volumes: not stated by the list. DRRs: `ts_drr` |
| Spine-Mets-CT-SEG | CT, metastatic spine disease; SINS categories; 0.5 to 1.5 mm slices | TCIA; github rouge1616 | 55 scans | TCIA terms not quoted | Not stated | No |
| AMOS22 | CT and MRI; 15 abdominal organs; documented annotation errors | amos22.grand-challenge.org | 500 CT plus 60 MRI | Not stated | Not stated | No |
| WORD | Abdominal CT, 16 organs | Not stated | 150 volumes | Not stated | Not stated | No |
| AbdomenCT-1K | Multi-phase, multi-vendor abdominal CT | Not stated | 1,112 scans | Not stated | Not stated | No |
| RibSeg v2 | CT; dense rib masks and centerlines | ResearchGate 373834788 | 660 scans, 15,466 ribs | Not stated | Not stated | No |
| Endplate3D-QCT | Quantitative CT, lumbar endplates | MICCAI 2025 paper 4366 | "Clinical", no number | Not stated | Not stated | No |
| Preoperative CT or MRI from hospital PACS (DICOMweb) | 3D volumes plus FHIR context | DMC PACS; Cerner CareAware | Not stated | Future clinical integration; DMC IT governance | PHI; AES-256 caching required | No |
| O-arm 3D DICOM exports | 3D DICOM over Ethernet | Device capability | Not stated | Not stated | Not stated | No |

### B.4 MRI (no MRI corpus is on the grid)

| Name | Modality | Source | Size | Access and licence | PHI | On the grid already? |
|---|---|---|---|---|---|---|
| SPIDER | Sagittal T1 and T2 lumbar MRI, .mha; vertebrae, discs, canal masks; Modic, Pfirrmann and other gradings | zenodo 10159290 and 8009680; spider.grand-challenge.org; Kaggle PNG derivative | 447 series from 218 patients, four hospitals | Public; licence not stated | De-identified per AI Anatomy Project Submissions; not stated elsewhere | No |
| RSNA 2024 Lumbar Spine Degenerative Classification (LumbarDISC) | Lumbar MRI, DICOM; three-grade stenosis labels at L1/L2 to L5/S1; many studies carry scout localizers | rsna.org; Kaggle; arXiv 2506.09162 | 2,697 patients (Spine Morphometrics); "2,000+" (AI Anatomy) | Challenge data-use terms not quoted | De-identified per AI Anatomy; not stated elsewhere | No |
| TotalSpineSeg | MRI; sacrum labels bootstrapped from CT by rigid registration | Not stated | 1,404 scans | Not stated | Not stated | No |
| OpenNeuro ds005616 whole-spine anatomical MRI | Whole-spine MRI (healthy controls) | openneuro.org/datasets/ds005616 | Not stated | Public; licence not stated | De-identified per the document | No |
| OpenNeuro or OASIS migraine, headache or Chiari cohort | High-resolution T2 sagittal C0 to C2 needed | Not identified | Not stated | Not stated; a suitable cohort is not confirmed to exist | De-identified per the document | No |
| Northern Finland Birth Cohort | Lumbar MRI (facet tropism study) | Cited only (PMC10997184) | Not stated | Not stated | Not stated | No |

### B.5 Other

| Name | Modality | Source | Size | Access and licence | PHI | On the grid already? |
|---|---|---|---|---|---|---|
| Rhoton-style dissection photographs and standard dissection photographs | Colour photographs | Rhoton Collection (nref.org); "institutional archives" | 500 plus 500 | Reuse rights not addressed | Cadaveric photographs; donor consent not discussed | No |
| Multicenter registry of 34,544 degenerative spine operations | Clinical registry (literature) | Bone and Joint Journal | 34,544 operations | Published aggregate; not a dataset to use | Not applicable | No |

### B.6 On the grid but named by no document

`FluoroCap/*` (the repository's published-figure fluoroscopy corpus, `docs/FLUOROCAP_*`), `nhanes_full`,
`mendeley_716`, `lateral236_pseudo`, `realxray/carmlspine`, `realxray/cobra_elekta`,
`realxray/geneva_hip`, `or_ready/devices/varian_halcyon/pairs`, `or_ready/spinesac`,
`or_ready/wholespine/data/eval/aasce`, `or_ready/corpus_manifold`. These are the candidate external
test sets for the first study. None of the documents knows they exist. Their size, licence and PHI
status are not stated in the material given here; the repository's `docs/DATA_ACCOUNTING.md` is the
place to look.

---

## C. Methods and models the documents propose

### C.1 The counting method (the repository's, restated by four documents)

- One-dimensional normalized cross-correlation along the cranio-caudal axis; OpenCV template matching
  with the normalized correlation coefficient; the overlap region of the preceding frame as template.
- Search window plus or minus 0.6 of the vertebral pitch around the commanded step (about 21 mm at a
  35 mm pitch); commanded step equals field of view minus two vertebral bodies; anchor at the sacrum
  (lumbar) or C2 (cervical). Written as |delta minus s| at most 0.6 p; aliases at s plus e plus or
  minus p enter only if the move errs by more than 14 mm in the lumbar spine (C-Arm Navigation System
  Development). The C-Arm Validation plan does not reconcile 14 mm with the 21 mm half-width.
- Chain decoding: per-body posteriors from a ResNet-18 encoder with a bidirectional recurrent head,
  decoded under the chain's ordering constraint against four alphabets (ordinary; thirteenth rib-bearing
  level; sixth lumbar; both); the alphabet with the highest cumulative probability wins (Market
  Analysis).
- Closed-loop acquisition: a geometric confidence margin, and on failure a displacement vector in units
  of length emitted as a control signal to move the C-arm (Market Analysis; the memo's answer to
  patent eligibility).
- Live visual-feedback overlay of C-arm travel so the operator stops at the commanded step (C-Arm
  Validation Research Plan Phase III).

Metrics and claims: exactness of the ordinal count. Documents: near 100 percent with boxes given;
72.1 to 95.2 percent (120 abdominopelvic renders), 78.7 to 93.6 percent (25 real lumbar radiographs
per the memo), 9.5 to 100 percent (thoracic two-vertebra frames swept from C2); over 99 percent
instrumented confirmation in simulation; manual repositioning error 16 to 16.7 mm. Repository,
measured: 99.74 percent boxes given and 39.52 percent detector boxes on clean renders; masked NCC
restores the one-body alias margin from 0.020 to 0.378 on a circular field; the step is the only
protocol lever that moves physics much (71.73 percent at 2.5 body, 76.88 at 1.5, 88.43 at 0.5, at 1.8
times the exposures); nine or ten linking fixes are refuted and must not be re-tried
(`docs/HANDOFF_PHYSICS.md`). No document mentions the step-length lever.

### C.2 Detection and sim-to-real (the first study's core)

- An anchor-free real-time detector, architecture not named (C-Arm Validation Research Plan); YOLO
  with oriented bounding boxes for vertebral bodies and screws (C-Arm Navigation; Spine Fluoroscopy
  Image Datasets, F1 0.86 for screws); Faster R-CNN or YOLO pre-trained on VinDr-SpineXR, keypoints
  from CSXA (Spine Fluoroscopy Image Datasets).
- Domain adaptation: GAN style transfer of DRRs toward unannotated real fluoroscopy, labels preserved
  (C-Arm Validation Phase II); Pix2Pix with adversarial plus L1 loss (Spine Fluoroscopy Image
  Datasets); Pairwise Domain Adaptation, a plug-in feature extractor trained on a small number of paired
  DRR and real frames (Fluoroscopic Vertebral Body Detection Research; "small number" not quantified).
- Coverage-driven sampling: acquisition-space vector per image (positioner primary and secondary
  angle, detector rotation, SID, ISO, magnification, patient position, table, anatomy, clinical and
  equipment variables) from DICOM tags (0018,1510), (0018,1511), (0018,1110), (0018,5100), (0018,9463);
  coverage C_d as occupied over clinically relevant bins; normalized entropy H_d*. Bin definitions and
  K are not specified.
- Physics-informed rendering: DeepDRR (material decomposition, spectrum-aware projection, noise,
  learned scatter) and DiffDRR (Siddon ray tracing in PyTorch, differentiable in intrinsics and
  extrinsics).

Metrics and claims: detectors trained only on renders fall to about 30 percent on real films (C-Arm
Validation; Navigation); convolutional models plateau near 90 percent on fluoroscopy against 99 percent
on standardized radiographs, attributed to sampling-density saturation (Fluoroscopic Vertebral Body
Detection Research; no cohort or CI given); models trained only on synthetic data "frequently suffer
catastrophic performance drops" on real patients (Spine Fluoroscopy Image Datasets).

### C.3 2D/3D registration and pose (candidate 3)

- Intensity-based 3D-2D registration (LevelCheck): 99.998 percent success in simulation with mean
  projection distance under 5 mm; 100 percent geometric accuracy retrospectively; about 26 s; TRE under
  2 mm; needs a preoperative CT. Known-Component Registration with CAD models of K-wires or screws and
  CMA-ES against level jumping. Multi-view constraints.
- Neural implicit volumes (NeRF, SDF MLPs), DiffDRR rendering, continuous SE(3) regression (DiffPose,
  LXPose at 20 ms, XVR at about 7 s), hybrid loss of multi-scale NCC plus geodesic SO(3) distance,
  Lie-algebra multi-view consistency, metal artifact reduction, canonical intrinsic resampling,
  frame-to-frame warm start with Levenberg-Marquardt (Edge-AI SaMD roadmap). N=1 recipe:
  patient-specific pose regressor on tens of thousands of DiffDRR renders, PDA on a few real frames,
  test-time differentiable refinement with Grad-NCC or LPIPS (Fluoroscopic Vertebral Body Detection
  Research).

Metrics and claims: mTRE at most 1.0 to 2.0 mm (endpoint table), at most 2.0 mm (month 7 to 12
milestone), at most 1.0 mm (PCCP acceptance); angular error at most 1.0 to 2.0 degrees; Dice over 90
percent; latency under 150 ms in prose, under 120 ms in the table; intrinsic tolerance (focal errors to
500 px give under 0.2 mm 3D error).

### C.4 Direct reconstruction (candidate 4)

X23D: learned multi-view stereo from 3 to 4 calibrated views; 88 percent F1, 71 percent surface score,
81.1 ms per vertebra; ex-vivo 49 screws (24 X23D, 25 fluoroscopy), dose 33.26 against 49.5 mGy, five
against six breaches. 3D Gaussian splatting over statistical shape models with a multi-view ViT
similarity loss. Both documents say it is not yet at CT-based navigation accuracy.

### C.5 CT segmentation and the LSTV benchmark (candidate 5)

nnU-Net, SwinUNETR and SAM named; TotalSegmentator; registration-free fusion for CTSpinoPelvic1K
(PatientDB canonical UID matching; choose the CT series maximizing the fraction of mask voxels over 200
HU; Z-axis cross-correlation of bone-density profile against mask occupancy; centre-voxel Y-flip
detection correcting a y of about minus 181 mm against plus 181 mm; no warping); LSTV as class 6;
labels from both annotation sources kept with arbitration metadata; soft-label multi-task learning;
calibration that routes confusion-zone cases to human review. Claims: zero percent cross-source
agreement on "sacralization" (counting criterion against morphological criterion); LSTV in 5 to 35
percent of people; wrong-level surgery from transitional anatomy in 4.5 to 15 percent of cases where
counting relied on MRI or plain film; PENGWIN IoU 0.930 on CT against 0.774 on X-ray. The document
calls the patient match "algebraically certain"; the repository README says it is under audit.

### C.6 MRI (candidate 6)

MONAI U-Net on SPIDER for the ligamentum flavum; Buckling Index as arc length over laminar attachment
distance, correlated with "Severe Stenosis" labels in LumbarDISC; YOLOv8 landmarks (last rib equals
T12, iliolumbar ligament equals L5) with count-down enumeration on scout scans; myodural bridge T2
signal, area and length. Morphometry review: six-landmark vertebral heights (SpineToolKit, under 3
percent height error, under 3.6 degrees lordosis error), instability indices, Modic types and MCG
grades (85.91 percent detection accuracy), DHI by the Farfan formula, Pfirrmann, DSCA and AP diameter,
lateral recess, Lee grades and foraminal volumes (normative table given), ligamentum flavum thickness
and area, facet grading and tropism, cervical MSCC and K-line; three-grade stenosis classification with
weighted log loss (weight 4 for Severe); Dice 0.94 lumbar, over 0.90 cervical. Every formula and most
thresholds were lost in the Drive export; not usable for encoding until re-exported.

### C.7 Deployment and hardware (not part of the first study; constrains what the study must output)

Holoscan DAG of six operators (ingest, preprocess, TensorRT inference, NCC count, visualise, display)
on NVIDIA IGX Orin (248 TOPS) with a Magewell capture card or the Holoscan Sensor Bridge (35.95 ms
glass to glass measured); glass-to-glass target under 100 ms; frame grabber with EDID spoofing on
DisplayPort/DVI or DICOM C-STORE over Ethernet; Jetson AGX Orin edge boxes at $3,000 to $5,000; an IEC
60601-1 edge PC with a passive DVI/SDI tap; Epiphan AV.io HD into a laptop at up to 60 fps. Hard-stop
or visual refusal below a pre-validated confidence threshold (threshold not given).

### C.8 Reader study (candidate 7)

Fully crossed MRMC, 4 DMC radiologists times 9.5 h, 50 scenarios, Obuchowski-Rockette, endpoints
mTRE, angular error, Dice, Gertzbein-Robbins A/B, NASA-TLX, SUS over 75, under ASTM F2554-22. No
power calculation; sample size from the $9,500 honorarium at $250 per hour.

### C.9 Out of scope for the engine

The Rhoton-style CycleGAN colouring tool (AI Anatomy Project Submissions) is an education demo with a
blank validation n; it has no spine data, no grid data and no study.

---

## D. Compute the study needs

| Item | What the documents state |
|---|---|
| Training GPU type | Not stated in any of the eleven documents |
| Training GPU hours | Not stated |
| Memory | Not stated |
| Storage | Not stated (AI Anatomy notes only that RSNA DICOM "is large") |
| Cluster or grid | Not named in any document. The grant summary budgets a Claude Team subscription, not the grid |
| Implied training scale | "Tens of thousands" of DiffDRR renders per patient for the N=1 pose regressor; 17,420 (X23D) and 50,000 (LevelCheck) renders in the cited sets; 48,600 (PENGWIN) |
| Inference targets, stated | IGX Orin 248 TOPS or IGX Thor; Jetson AGX Orin 64 GB ($3,000 to $3,950), Advantech MIC-733 (about $4,999), Onyx ACCEL-JS500 and VM500; one IEC 60601-1 edge PC with an RTX GPU ($3,500 budget line); a standard laptop with an Epiphan grabber |
| Latency, stated | Under 100 ms glass to glass (Navigation); under 150 ms prose and under 120 ms table (SaMD roadmap); 40 ms intraoperative constraint and LXPose 20 ms (Detection Research); X23D 81.1 ms per vertebra |
| What the first study actually needs | Not yet measured. The repository's `make physics-check` verifies what the grid has for the physics jobs; the detector retraining and styled-render passes have no stated budget. The engine must record wall time, GPU type and node-local temp use per job as it runs them, and every job carries a wall time |

---

## E. Validation and reporting

### E.1 CLAIM 2020, 42 items: what the documents supply and what the study must fill

The repository root holds the checklist (`CLAIM+-+Checklist+for+AI+in+Medical+imaging.docx`, Mongan,
Moy and Kahn, Radiol Artif Intell 2020); the item wording below was read from it on 2026-10-04.
"Docs" means any of the eleven documents.

| Item | CLAIM 2020 wording (short) | Docs supply | The study must fill |
|---|---|---|---|
| 1 | Identification as an AI methodology study, technology category | No | State: deep-learning detector plus network-free NCC linker |
| 2 | Structured summary | No | Write |
| 3 | Scientific and clinical background, intended use and clinical role | Yes, all seven fluoroscopy docs (wrong-level surgery 0.12 percent overall, 0.42 percent thoracic; fiducials 183 mGy and about $1,750 to $2,000 per patient) | Cite primary sources, not law-firm or news pages |
| 4 | Objectives and hypotheses | Partly (C-Arm Validation Phase I and II questions) | State the detection-gap hypothesis and the adaptation hypothesis |
| 5 | Prospective or retrospective | Retrospective implied | State |
| 6 | Study goal | Feasibility | State |
| 7 | Data sources | Yes (section B) | Name every corpus used, with path on the grid |
| 8 | Eligibility criteria | No | Write per corpus |
| 9 | Pre-processing | Partly (contrast standardisation, gamma, log conversion in Navigation; canonical intrinsic resampling in SaMD) | Write what the repository does |
| 10 | Selection of subsets | No | Write |
| 11 | Definitions of data elements | Partly (acquisition-space vector, Detection Research) | Write |
| 12 | De-identification methods | Asserted only ("de-identified", "Safe Harbor"); no procedure anywhere | Write the procedure per corpus; for public corpora cite the publisher's statement |
| 13 | Missing data | No | Write |
| 14 | Ground truth definition | Partly (manual boxes on PACS pairs; projected masks on DRRs; DeepFluoro optical tracking) | Write |
| 15 | Rationale for the reference standard | No | Write |
| 16 | Source of annotations, annotator qualifications | CSXA: four surgeons, three tiers; otherwise no | Write |
| 17 | Annotation tools | 3D Slicer (AI Anatomy) only | Write |
| 18 | Inter- and intrarater variability | Only the Spine Segmentation doc (zero percent agreement on sacralization) | Measure where human boxes are made |
| 19 | Sample size and how determined | No (the reader study's 50 by 4 comes from the honorarium) | Justify |
| 20 | Assignment to partitions, proportions | VinDr fixed split only | Write |
| 21 | Level at which partitions are disjoint | No; only "held-out" | Patient level; cadaver level for DeepFluoro; study level for VinDr; CTSpinoPelvic1K blocked until the identity audit closes |
| 22 | Model description | Partly (ResNet-18 plus bidirectional recurrent head; detector unnamed) | Write |
| 23 | Software libraries | OpenCV, PyTorch, MONAI, YOLOv8, DiffDRR named | Pin versions (the repository's lock files) |
| 24 | Initialization | No | Write |
| 25 | Training details | No | Write |
| 26 | Final model selection | No | Write; the confidence threshold choice (0.05 against 0.25) belongs here |
| 27 | Ensembling | No | State if none |
| 28 | Performance metrics | Exactness; F1; mAP50; Dice; mTRE; IoU | Exactness end to end, plus detector box metrics |
| 29 | Significance and uncertainty | No document gives a CI; the repository table does | 95 percent CIs with n on every row |
| 30 | Robustness or sensitivity | Repository: step ladder, jitter, grid on and off; docs: none | Report the step ladder and threshold sweep |
| 31 | Explainability | No | State if none |
| 32 | External data | None stated in any document | The real corpora in B.1 and B.6 are external to the render training sets; say which were never seen |
| 33 | Flow of cases, inclusion and exclusion diagram | No | Draw from `pipeline_state.py` output |
| 34 | Demographic and clinical characteristics per partition | No | Report what the corpora publish; "not stated" where they do not |
| 35 | Performance on all partitions | No | Report |
| 36 | Diagnostic accuracy with 95 percent CIs | No | Report |
| 37 | Failure analysis | Repository: alias margin, circular field; docs: level jumping | Report |
| 38 | Limitations | Partly | Write; include that DeepFluoro is pelvis, not spine |
| 39 | Implications for practice | Yes (all fluoroscopy docs) | Write without the market claims |
| 40 | Registration | No | Not applicable unless pre-registered; say so |
| 41 | Protocol access | No | The repository's `docs/BENCHMARK_PROTOCOL.md` and this file |
| 42 | Funding and role of funders | AIDaS $20,000 named in two docs | State what applies |

### E.2 REFORMS needs

- Patient-level splits. No document states the level at which its held-out sets are disjoint. The
  engine declares the split level before training, per corpus: patient (or study) for VinDr-SpineXR,
  BUU-LSPINE, CSXA; cadaver for DeepFluoro (six subjects, so leave-one-cadaver-out or none); CT source
  volume for every render set; CTSpinoPelvic1K only after the identity audit closes.
- Confidence intervals. The repository's `tab_all_results.csv` already carries 95 percent CIs and n on
  every "on the chain" row; no Drive document carries one. Every exactness or box metric the engine
  reports carries n and a CI.
- Run ID. Every results row carries the run identifier and the commit hash; `make physics` is the model
  (it reproduces every headline number and exits non-zero if one moved).
- Clean tree. The engine refuses to write a results row from a tree with uncommitted changes, and
  records the tree state with the row.

### E.3 IRB and de-identification statements, present or missing

| Document | IRB statement | De-identification statement |
|---|---|---|
| C-Arm Validation Research Plan (both copies) | Present: exemption or expedited review under the revised Common Rule; waiver of consent; pre-review two weeks ahead; IACUC for animal tissue; Anatomical Gift Program plus Biosafety Committee for cadavers (not human-subjects research) | Asserted ("securely coded or de-identified"); no procedure |
| Edge-AI SaMD Roadmap | Present: WSU IRB Expedited Review, 45 CFR 46.110 Category 7; reader data pseudonymized | Present as policy: retrospective, HIPAA Safe Harbor; PHI never into the Claude Team stack; local caches AES-256 |
| NIH grant summary | Mentioned only (lab manager coordinates IRB); no category | Missing |
| AI Anatomy Project Submissions | Asserted: "Non-Human Subjects Research" or exempt because datasets are public; no determination | Asserted as a property of the public datasets |
| Fluoroscopic Vertebral Body Detection Research | IRB named only as a condition for restricted datasets | DUA anonymization named only |
| Spine Fluoroscopy Image Datasets; C-Arm Navigation; Market Analysis; Spine Segmentation Dataset Research; Spine Morphometrics | Missing | Missing |
| The repository | `docs/IRB/HPR_determination_VinDr-SpineXR_draft.md` (a draft, not a determination) | Not stated in the material here |

### E.4 External validation

No document plans one. The first study's external sets are the real corpora on the grid that no render
set was made from (B.1 and B.6), with the acquisition-space coverage of each reported (candidate 2) so
that "external" means something. DeepFluoro is pelvis; its use as a spine test is asserted
("universally transferable") in one document and not measured anywhere.

---

## F. Regulatory and commercial framing (kept apart from the science)

Three documents frame the product: a Class II Software as a Medical Device under 510(k), product code
OLO (21 CFR 882.4560), with ARVIS Shoulder K240062, NuVasive Pulse, 7D Surgical, Medivis and Captiva
Spine WatchTower ROAM named as possible predicates; IEC 62304 Class C, ISO 14971, IEC 60601-1, QMSR
effective 2 February 2026, Section 524B cybersecurity with an SBOM, and an embedded PCCP for
post-market retraining. The market case is Detroit (DMC) first, a $5,000 to $150,000 per-OR device
against $700,000 to $1.5 million navigation suites, sold against malpractice exposure and the cost of
preoperative fiducials. The funding path is an AIDaS seed grant of $20,000 (the grant summary's budget
and the roadmap's months 1 to 12), then NIH R21 or NSF SCH, then SBIR. Wayne State policy 2.41.04
requires an Invention Disclosure before any public disclosure, which the Market Analysis says includes
GitHub repository visibility and journal submission; the repository has `docs/INVENTION_DISCLOSURE.md`.
None of this changes what the first study measures; it only means the engine does not publish, push
publicly or submit anything without the maintainer's word, and that the study's accuracy claims are
written so they can later serve as verification evidence rather than marketing.

---

## G. What this means for the engine: acceptance criteria per phase

Each criterion is checkable and traced to a document ("Doc:") or to the repository ("Repo:").

### P0 substrate

1. The engine runs as a Beethoven worker on the grid under the student's own sign-in; every corpus it
   reads is a path under the grid's data roots listed in section B, and no image byte or DICOM header of
   a clinical corpus appears in the worker's outbound context (prompts carry paths, counts, metrics and
   code). Doc: Edge-AI SaMD Roadmap ("the engineering team must operate entirely on synthetic, phantom,
   or fully de-identified open-source datasets ... when querying the LLM"); Market Analysis (hospital IT
   limits PHI to the edge).
2. `tools/pipeline_state.py` lists every stage of the first study (render, train, adapt, detect, link,
   report) so its state is computed from the filesystem and the scheduler, not from prose. Repo:
   `CLAUDE.md` ("if you add a pipeline stage, add it to `tools/pipeline_state.py`").
3. `make physics-check` passes on the compute node before any training job is queued. Repo:
   `docs/HANDOFF_PHYSICS.md`.

### G1 verification

1. Every number the engine reports is reproduced by one command that exits non-zero if the number
   moved, on the `make physics` model. Repo: `docs/HANDOFF_PHYSICS.md`.
2. The engine checks the Market Analysis's three attributions (120 renders 72.1 to 95.2; 25 real lumbar
   radiographs 78.7 to 93.6; thoracic 9.5 to 100) against `tab_all_results.csv` and writes the result
   into the study record; as read today, 93.6 is CT renders n=25 lumbosacral, not real radiographs.
   Doc: AI Vertebral Counter Market Analysis.
3. Every detector figure names its confidence threshold; 30.06 percent (0.25) and 39.52 percent (0.05)
   are never reported without it. Doc: C-Arm Navigation System Development; Repo: handoff section 1.

### G5 and G3 orchestration and token pacing

1. Training, rendering and evaluation run as Slurm jobs with a wall time, queued with one `sbatch`,
   status read from `status.json` at no faster than 60 s; the worker never runs a container or a model
   on the login node. Repo and Beethoven `CLAUDE.md` grid etiquette.
2. The worker's Claude Code sitting reads logs and result files and writes code; it does not stream
   images into its context. Tokens per analysis step on a flat-rate sign-in: not yet measured; the
   engine logs them per step from the first run so the week's budget can be set. Doc: the NIH grant
   summary budgets a Claude Team subscription, which is not the engine's model; the engine runs on
   each student's own sign-in only.
3. At most one successor job per worker (`afterany`), ended by a stop file. Beethoven `CLAUDE.md`.

### G2 REFORMS

1. The split level per corpus (E.2) is written in the study record before the first training job and
   checked by a test that fails if any evaluation case shares a patient, cadaver or source volume with a
   training case. Doc: no document states one, which is the finding; CLAIM item 21.
2. Every result row carries n and a 95 percent CI, Run ID, commit hash and clean-tree flag; a row from
   a dirty tree is refused. Repo: `tab_all_results.csv` already carries n and CI.
3. CTSpinoPelvic1K is not used for a patient-level split until the identity audit closes. Repo: README
   ("under audit"); Doc: Spine Segmentation Dataset Research claims "algebraically certain" and the
   engine records the disagreement.

### G6 medical calibration

1. CT path: Hounsfield units preserved end to end; MetaTensor (or equivalent) carries affine and
   spacing; LPS against RAS is checked and the Y-flip test (centre voxel at about minus 181 against plus
   181 mm) runs before any label fusion; the bone-HU over 200 series selection is recorded per case. Doc:
   Spine Segmentation Dataset Research.
2. X-ray and fluoroscopy path: this is where the first study lives, and there is no HU. Calibration
   means image formation and geometry, not intensity units: pixel spacing, SID, positioner angles and
   magnification from the DICOM tags named in C.2, recorded per frame into the acquisition-space vector
   with coverage C_d and entropy H_d* per corpus; the physics terms the repository renders (scatter,
   anti-scatter grid, veiling glare, auto dose-rate, circular field) are listed per render set; the
   detector confidence threshold is treated as a calibration parameter and swept. Doc: Fluoroscopic
   Vertebral Body Detection Research; C-Arm Validation Research Plan Phase I; Repo:
   `docs/DEEPFLUORO_FORMATION.md`, handoff sections 1 and 2.
3. MRI measures (Modic, Pfirrmann, DSCA on T2) are out of the first study; the engine marks them "not
   applicable: no MRI on the grid" rather than silently skipping. Doc: Spine Morphometrics; AI Anatomy
   Project Submissions.

### G4 compliance

1. Before any corpus is read, its row in section B carries an access and licence statement and an IRB
   or determination status; "not stated" blocks ingestion of clinical corpora and allows public
   synthetic ones. Doc: every dataset survey leaves these blank; Repo: `docs/IRB/` holds one draft.
2. The engine never reads, stores or relays a Claude credential, never puts a secret on a command line,
   and never deletes outside its own run directories and node-local temp. Beethoven `CLAUDE.md`.
3. No public push, release, preprint or submission happens from the engine; the Invention Disclosure
   gate is the maintainer's. Doc: AI Vertebral Counter Market Analysis; Edge-AI SaMD Roadmap.

### G7 publication

1. The CLAIM table in E.1 is filled item by item, with "not applicable" written where it is, and ships
   with the manuscript. Repo: the checklist file at the root.
2. Every figure and table in the manuscript is regenerated by `make` from committed code, and the
   manuscript states the step (2.5 body published; 0.5 body measured best under physics) and the
   confidence threshold for every number. Repo: handoff; Doc: C-Arm Validation Research Plan keeps the
   published step and does not know the lever exists.
3. The limitations section says that no real spine sweep at a known step exists in any corpus, that
   DeepFluoro is pelvis, and that all documents' gains are in the boxes-given regime. Doc: C-Arm
   Validation Research Plan ("the complete absence of real-world, overlapping C-arm fluoroscopy
   sweeps"); Repo: `docs/FLUORO_DATASET_STRATEGY.md` constraint (b).

### F2 UI

1. The panel shows the study's stage in plain words from `pipeline_state.py` (what is done, running,
   ready, blocked) and never a QoS, a path or a close code. Beethoven `CLAUDE.md`.
2. The panel shows the Run ID, commit and clean-tree state of the last reported result beside the
   number.
3. The panel never shows a patient identifier, a DICOM header or an image from a clinical corpus; it
   may show a synthetic render.

---

## H. Decisions only Greg can make

1. Is the first study the detection-under-domain-shift study (section A), or Phase I's go/no-go on the
   NCC peak, which cannot start without PACS or cadaver frames?
2. Does the study publish the step-length result (0.5 body, 88.43 percent under physics) or keep the
   published 2.5-body step the Drive plans assume?
3. Which confidence threshold is the manuscript's: 0.05 (measured best) or 0.25 (published)?
4. Which real corpora on the grid are allowed as test sets, and which carry an access or IRB status that
   must be written down first (VinDr-SpineXR draft; `carmlspine`, `cobra_elekta`, `geneva_hip`, FluoroCap
   not stated)?
5. Is DeepFluoro (pelvis) an acceptable external test for a spine method, and if so how is that
   limitation worded?
6. CTSpinoPelvic1K: close the identity audit before it is used in any split, or keep it out of the first
   study?
7. Does the Market Analysis's set of numbers get corrected to the repository table, or does the memo
   describe an earlier run that should be found and recorded?
8. Is Dr. Zhizhong Han's registration product (candidate 3) a separate stream of this engine or not
   this engine's business?
9. PACS extraction (C-Arm Validation Phase I): file the IRB pre-review now, or after the first study
   reports?
10. Invention Disclosure: filed, or to be filed before the study's results leave the grid in any form?
11. Who pays for the compute and on which sign-in; the grant summary's Claude Team seats are not the
    engine's model.
12. Re-export the Spine Morphometrics document with its equations, or drop it from this engine's scope?

---

## I. Sources

| Document (Drive title) | Drive id | What it contributed | Duplicate? |
|---|---|---|---|
| Edge-AI SaMD Commercialization Roadmap | 1roNaR3i3fhL-apvakuzI8M9Ru9E2ubBeZ9ugHc-U1rM | 2D/3D registration product under an AIDaS grant with Dr. Zhizhong Han as PI; MRMC reader study design; 510(k) OLO path; the rule that only synthetic, phantom or de-identified data may touch the LLM stack; DeepFluoro as the one named dataset; latency 150 against 120 ms and mTRE 1 against 2 mm inconsistencies | No |
| Ok give me a full nih grant summary including budg... | 1DHCnkEc6CTOFBVhnIJg2bEXds2uloOxc1XLCX92AHvc | $20,000 lab budget: IEC 60601-1 edge box, frame grabber, Body Bequest specimens, OEHS filings, Claude Team seats; no research question, dataset or metric; two arithmetic inconsistencies (0.07 FTE against 3 person-months; $192 per year for 8 seats) | No |
| Fluoroscopic Vertebral Body Detection Research | 12Yg0rHxxV7uKh_o6IyFyYGQx4UWjrNeuRgMHIFB7SrQ | The 90 against 99 percent plateau argument; coverage-driven sampling from DICOM tags; DeepDRR, DiffDRR, PDA; KC-Reg against level jumping; X23D; rotational C-arm landscape; dataset landscape (DeepFluoro 366 frames, Ljubljana, SpineWeb, CTSpine1K, Henry Ford); the N=1 recipe | No |
| Spine Fluoroscopy Image Datasets | 1_JzErIkef9iTzbhpLRU6e3jVsrbhabEGoYVJpHY6Uus | Dataset survey (VFSS-5k, QF kinematics, X23D 17,420, LevelCheck 50,000, Veriserum, SpineDepth, SpineAlign, screw datasets, VinDr-SpineXR, CSXA, FracAtlas, BUU-LSPINE, CTSpine1K, VerSe, SPIDER); the conclusion that no public spine fluoroscopy video with instruments exists; several numbers lost in export | No |
| Copy of C-Arm Validation Research Plan | 1lrUlodl7J91u1SQYHKCJIk3F4AvW-yv2EUg8abgLT-M | Same four-phase roadmap as the next row | Yes: duplicate of 1Y1Mbow5BPz1WF4W9YybbYAFbBtQbhz4IPEirJCaRO48; its extraction adds nothing the original lacks |
| C-Arm Validation Research Plan | 1Y1Mbow5BPz1WF4W9YybbYAFbBtQbhz4IPEirJCaRO48 | The four-phase translational plan for the repository's counting method: PACS pairs under IRB, DRR-trained detector with GAN adaptation, frame grabber and phantoms and IACUC tissue, human cadaver confirmation; the 30 percent real-film figure; the 16 to 16.7 mm against 14 mm kinematic bottleneck; keeps the published step | No (original) |
| C-Arm Navigation System Development | 1HiPdNcGFTmk0-hNal00RvnQV0g_fr7X1u-M9xYmouoA | The method restated with its arithmetic (0.6 p window, aliases at s plus e plus or minus p, 14 mm); 30.06 percent at the published threshold; detection named the open problem; Holoscan and IGX Orin architecture; frame grabber against DICOM C-STORE; 510(k) OLO, SBOM, ISO 14971 hard-stop; Detroit market | No |
| AI Vertebral Counter Market Analysis | 1Y9rE9ds9-2oiNNzw8g9cwjyE4l-KRQnzA6VfdY1cJzM | Chain decoding against four alphabets; ResNet-18 plus bidirectional recurrent head; closed-loop acquisition for patent eligibility; the three accuracy attributions that disagree with the repository table; Jetson pricing; WSU policy 2.41.04 and the Invention Disclosure gate | No |
| Spine Segmentation Dataset Research | 1IhK1lacKZLiApbkmO3pD4g8zi2Qwrp1p0lYMqKWwygE | Fifteen-dataset CT and MRI survey around CTSpinoPelvic1K; LSTV class 6; labels from both sources with arbitration metadata; the registration-free fusion pipeline (PatientDB, bone-HU over 200, Y-flip at 181 mm); N left as "[N]"; the "algebraically certain" claim the repository calls under audit | No |
| Spine Morphometrics: Beyond Basic Measurements | 1fLrSyk8CexfQgvd4JMki-4za0_hE76nzd1frzeUwmeY | MRI lumbar morphometry review (RSNA LumbarDISC 2,697 patients; fifteen measurement families); every equation and most thresholds lost in the Drive export; no plan | No |
| AI Anatomy Project Submissions | 1Rf5bxYB0ofeorhpdSYxkS6wcJjkE0qyTP3D6v1w1N20 | Three MRI projects (Buckling Index on SPIDER plus LumbarDISC; LSTV from scouts with YOLOv8; myodural bridge) and the Rhoton CycleGAN tool; IRB exemption asserted, not obtained; a 50-patient manual pilot plan | No |

Repository files read for the cross-checks: `docs/HANDOFF_PHYSICS.md`,
`paper/focused/figures/tab_all_results.csv`, `docs/IRB/HPR_determination_VinDr-SpineXR_draft.md`,
`docs/FLUORO_DATASET_STRATEGY.md`, `CLAIM+-+Checklist+for+AI+in+Medical+imaging.docx`, and the list
of `docs/` files (`BENCHMARK_PROTOCOL.md`, `CARM_DEPLOYMENT_EVIDENCE.md`, `COUNTING_EVIDENCE.md`,
`CT_LSTV_CLASSIFIER_PLAN.md`, `DATA_ACCOUNTING.md`, `DEEPFLUORO_FORMATION.md`, `GUIDED_ACQUISITION.md`,
`INVENTION_DISCLOSURE.md`, `PATIENT_IDENTITY_SPEC.md`, `PIPELINE_RESUME.md`).

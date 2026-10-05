# Linear team Beethoven (workspace ashl3y): issues snapshot

Snapshot taken: 2026-10-05T00:00Z, through the Linear connector of the hand-off thread.

Non-archived issues of the team (one page held them all). Not here: BEE-5 to BEE-97, the launcher backlog from before the engine, archived together on 2026-10-03 at 22:33Z (Linear shows them with "include archived"), and BEE-175, which Linear does not return at all. Titles, status, priority, labels and assignee only; no descriptions or comments.

Total issues: 103. Projects: 14.

| Status type | Issues |
|---|---|
| backlog | 74 |
| unstarted | 5 |
| started | 6 |
| completed | 18 |

## P0 — Foundations & Open Decisions

- Id: P-BEE-2
- URL: https://linear.app/ashl3y/project/p0-foundations-and-open-decisions-e3b319fa8cb9
- Status: Backlog (backlog)
- Summary: Ground-truth probe, deterministic substrate, and the decisions (credential/billing, repo, engine, headless) that gate all engine work.
- Issues: 14

| Issue | Title | Status | Priority | Labels | Assignee |
|---|---|---|---|---|---|
| [BEE-98](https://linear.app/ashl3y/issue/BEE-98/d1-decide-credential-and-billing-model-for-the-engine) | D1 — Decide credential & billing model for the engine | Done | Urgent | decision, Security, arch-risk, E0 Program and governance | Gregory Schwing |
| [BEE-99](https://linear.app/ashl3y/issue/BEE-99/d2-decide-repo-topology-new-beethoven-research-vs-folder) | D2 — Decide repo topology (new beethoven-research vs folder) | Done | Urgent | decision, E0 Program and governance | Gregory Schwing |
| [BEE-100](https://linear.app/ashl3y/issue/BEE-100/d3-decide-workflow-orchestration-engine) | D3 — Decide workflow / orchestration engine | Done | High | decision, E0 Program and governance | Gregory Schwing |
| [BEE-101](https://linear.app/ashl3y/issue/BEE-101/probe-headless-claude-p-from-an-sbatch-job-on-the-students-login) | Probe: headless `claude -p` from an sbatch job on the student's login | Todo | High | E3 Execution plane, Spike |  |
| [BEE-102](https://linear.app/ashl3y/issue/BEE-102/deterministic-substrate-pixi-manifest-lockfile) | Deterministic substrate: Pixi manifest + lockfile | Done | High | Infra, E0 Program and governance |  |
| [BEE-103](https://linear.app/ashl3y/issue/BEE-103/deterministic-substrate-apptainer-image) | Deterministic substrate: Apptainer image | In Progress | High | Infra, E0 Program and governance |  |
| [BEE-104](https://linear.app/ashl3y/issue/BEE-104/scaffold-the-engine-repo-pending-d2) | Scaffold the engine repo (pending D2) | Done | Medium | Docs, E0 Program and governance |  |
| [BEE-110](https://linear.app/ashl3y/issue/BEE-110/verification-gate-before-every-push-pre-push-hook-required-ci-check) | Verification gate before every push: pre-push hook + required CI check + auto-merge (P0) | Backlog | Urgent | E10 Test harness, Infra |  |
| [BEE-192](https://linear.app/ashl3y/issue/BEE-192/build-parallelism-a-worktree-per-stream-and-saved-workflow-scripts-for) | Build parallelism: a worktree per stream and saved workflow scripts for the gate, probes and migrations (BUILD_PLAN §17.6) | Backlog | High | Feature |  |
| [BEE-193](https://linear.app/ashl3y/issue/BEE-193/greg-creates-beethoven-qa-readme-only-auto-merge-on-rulesets-token) | greg creates beethoven-qa: README only, auto-merge on, RULESETS_TOKEN shared (done 2026-10-04 13:24Z) | Done | No priority |  | Gregory Schwing |
| [BEE-194](https://linear.app/ashl3y/issue/BEE-194/greg-creates-beethoven-agents-readme-only-auto-merge-on-rulesets-token) | greg creates beethoven-agents: README only, auto-merge on, RULESETS_TOKEN shared | Done | High |  | Gregory Schwing |
| [BEE-195](https://linear.app/ashl3y/issue/BEE-195/beethoven-qa-first-release-tag-v100-of-the-package-the-gate-command) | beethoven-qa first release: tag v1.0.0 of the package, the gate command and the Claude Code plugin | Done | High |  |  |
| [BEE-196](https://linear.app/ashl3y/issue/BEE-196/switch-beethoven-agents-to-the-vendored-beethoven-qa-copy) | Switch beethoven-agents to the vendored beethoven-qa copy (vendor/beethoven-qa, ORIGIN, vendor-check before the gate) | Done | No priority |  |  |
| [BEE-197](https://linear.app/ashl3y/issue/BEE-197/slim-beethoven-research-to-the-research-pipeline-and-switch-it-to-the) | Slim beethoven-research to the research pipeline and switch it to the vendored beethoven-qa copy | Done | No priority |  |  |

## G3 — Token Economy & Context Control

- Id: P-BEE-3
- URL: https://linear.app/ashl3y/project/g3-token-economy-and-context-control-638ba8f37bf4
- Status: Backlog (backlog)
- Summary: Goal 3. Lazy tool loading, prompt-cache TTLs, preemptive auto-compaction, dual-hook state, quota-window-aware scheduling (flat-rate subscription), telemetry.
- Issues: 6

| Issue | Title | Status | Priority | Labels | Assignee |
|---|---|---|---|---|---|
| [BEE-117](https://linear.app/ashl3y/issue/BEE-117/lazy-tool-loading-mcp-cli-toolsearch) | Lazy tool loading (mcp-cli / ToolSearch) | Backlog | High | E3 Execution plane, Feature |  |
| [BEE-118](https://linear.app/ashl3y/issue/BEE-118/prompt-cache-ttls-via-managed-settings) | Prompt-cache TTLs via managed settings | Backlog | Medium | E3 Execution plane, Infra |  |
| [BEE-119](https://linear.app/ashl3y/issue/BEE-119/preemptive-auto-compaction) | Preemptive auto-compaction | Backlog | High | E3 Execution plane, Infra, arch-risk |  |
| [BEE-120](https://linear.app/ashl3y/issue/BEE-120/dual-hook-state-preservation-precompact-sessionstart) | Dual-hook state preservation (PreCompact / SessionStart) | Backlog | Medium | E3 Execution plane, Feature |  |
| [BEE-121](https://linear.app/ashl3y/issue/BEE-121/quota-window-aware-scheduling-flat-rate-subscription-no-gateway) | Quota-window-aware scheduling (flat-rate subscription, no gateway) | Backlog | Medium | E3 Execution plane, arch-risk, Feature |  |
| [BEE-122](https://linear.app/ashl3y/issue/BEE-122/tokencost-telemetry-ledger-wandb) | Token/cost telemetry → ledger + W&B | Backlog | Medium | E3 Execution plane, Feature |  |

## G4 — Legal & Security Compliance Boundaries

- Id: P-BEE-4
- URL: https://linear.app/ashl3y/project/g4-legal-and-security-compliance-boundaries-e5af446f3ef9
- Status: Backlog (backlog)
- Summary: Goal 4. Guard hook, hardened managed-settings, Phase A/B governance (defensive on-grid only), authorized-targets-only, credential compliance.
- Issues: 7

| Issue | Title | Status | Priority | Labels | Assignee |
|---|---|---|---|---|---|
| [BEE-123](https://linear.app/ashl3y/issue/BEE-123/pretooluse-guard-hook-claude-guardsh) | PreToolUse guard hook (claude-guard.sh) | Done | High | Security, E0 Program and governance |  |
| [BEE-124](https://linear.app/ashl3y/issue/BEE-124/hardened-managed-settingsjson) | Hardened managed-settings.json | Done | High | Security, E0 Program and governance |  |
| [BEE-125](https://linear.app/ashl3y/issue/BEE-125/phase-ab-separation-governance-doc) | Phase A/B separation governance doc | Backlog | High | Docs, E0 Program and governance |  |
| [BEE-126](https://linear.app/ashl3y/issue/BEE-126/authorized-targets-only-ingestion-policy-check) | Authorized-targets-only ingestion policy + check | Backlog | High | Security, E0 Program and governance |  |
| [BEE-127](https://linear.app/ashl3y/issue/BEE-127/subscription-only-credential-compliance-check) | Subscription-only credential compliance check | Backlog | High | Security, E0 Program and governance |  |
| [BEE-128](https://linear.app/ashl3y/issue/BEE-128/aup-alignment-note) | AUP alignment note | Backlog | Low | good-first-issue, Docs, E0 Program and governance |  |
| [BEE-191](https://linear.app/ashl3y/issue/BEE-191/beethoven-for-vs-code-400-still-offers-a-pay-per-use-api-key-overflow) | Beethoven for VS Code 4.0.0 still offers a pay-per-use API key overflow, which the no-usage-credits rule forbids | Done | High |  | Gregory Schwing |

## G5 — Storage, Crash Resilience & Orchestration

- Id: P-BEE-5
- URL: https://linear.app/ashl3y/project/g5-storage-crash-resilience-and-orchestration-24f77833bffb
- Status: Backlog (backlog)
- Summary: Goal 5. Node-local scratch (SQLite off PFS), Postgres SessionStore, transcript teleport, nested outer/inner orchestration, concurrency caps.
- Issues: 18

| Issue | Title | Status | Priority | Labels | Assignee |
|---|---|---|---|---|---|
| [BEE-129](https://linear.app/ashl3y/issue/BEE-129/node-local-scratch-staging-protocol-sqlite-off-pfs) | Node-local scratch staging protocol (SQLite off PFS) | Backlog | High | E4 Storage, Infra, arch-risk |  |
| [BEE-130](https://linear.app/ashl3y/issue/BEE-130/postgres-backed-sessionstore-eager-dual-writes) | Postgres-backed SessionStore (eager dual-writes) | Backlog | High | E4 Storage, Feature |  |
| [BEE-131](https://linear.app/ashl3y/issue/BEE-131/transcript-teleportation-claudepath-remap) | Transcript teleportation / claudepath remap | Backlog | Medium | E4 Storage, Spike |  |
| [BEE-132](https://linear.app/ashl3y/issue/BEE-132/nested-outerinner-orchestration) | Nested outer/inner orchestration | Backlog | High | E2 Control plane, Feature |  |
| [BEE-133](https://linear.app/ashl3y/issue/BEE-133/concurrency-guardrails-subagent-caps) | Concurrency guardrails (subagent caps) | Backlog | Medium | E2 Control plane, Infra |  |
| [BEE-134](https://linear.app/ashl3y/issue/BEE-134/successor-job-chaining-wall-time-suspend-resume) | Successor-job chaining / wall-time suspend-resume | Backlog | Medium | E2 Control plane, Feature |  |
| [BEE-150](https://linear.app/ashl3y/issue/BEE-150/multi-worker-fan-out-several-claude-sessions-per-student-on-the-grid) | Multi-worker fan-out: several Claude sessions per student on the grid | Backlog | High | E3 Execution plane, arch-risk, Feature |  |
| [BEE-151](https://linear.app/ashl3y/issue/BEE-151/worker-pool-controls-concurrency-cap-wall-time-one-stop-file) | Worker pool controls: concurrency cap, wall time, one stop file | Backlog | Medium | E3 Execution plane, Feature |  |
| [BEE-152](https://linear.app/ashl3y/issue/BEE-152/spike-more-than-one-remote-control-session-per-student-at-once) | Spike: more than one Remote Control session per student at once | Backlog | Medium | Spike |  |
| [BEE-178](https://linear.app/ashl3y/issue/BEE-178/g5-7-progress-signal-every-long-running-step-declares-how-it-can-tell) | G5-7 — Progress signal: every long-running step declares how it can tell it is making progress | Backlog | High | E2 Control plane, Feature |  |
| [BEE-179](https://linear.app/ashl3y/issue/BEE-179/g5-8-per-run-compute-and-quota-record-gpu-hours-slurm-job-ids-wall) | G5-8 — Per-run compute and quota record: GPU-hours, Slurm job ids, wall time, window spend, written by the orchestrator | Backlog | Medium | E6 Training and telemetry, Feature |  |
| [BEE-180](https://linear.app/ashl3y/issue/BEE-180/g5-9-one-submission-point-the-slurm-operator-subagent-the-slurm-submit) | G5-9 — One submission point: the slurm-operator subagent, the slurm-submit skill and the submit shim | Backlog | Medium | Feature |  |
| [BEE-185](https://linear.app/ashl3y/issue/BEE-185/account-registry-and-per-account-sign-in-one-directory-per-account) | Account registry and per-account sign-in: one directory per account, nothing read inside (BUILD_PLAN §17.2.1) | In Progress | High | Feature |  |
| [BEE-186](https://linear.app/ashl3y/issue/BEE-186/message-bus-and-inbox-socket-bridge-across-nodes-and-accounts-build) | Message bus and inbox-socket bridge across nodes and accounts (BUILD_PLAN §17.2.5) | Backlog | High | Feature |  |
| [BEE-187](https://linear.app/ashl3y/issue/BEE-187/session-registry-heartbeats-and-reaper-no-orphaned-sessions-or-agents) | Session registry, heartbeats and reaper: no orphaned sessions or agents (BUILD_PLAN §17.2.6) | Backlog | High | Feature |  |
| [BEE-188](https://linear.app/ashl3y/issue/BEE-188/per-account-usage-reading-and-the-90-percent-threshold-switch-through) | Per-account usage reading and the 90 % threshold switch, through Claude Code only (BUILD_PLAN §17.2.8) | Backlog | Medium | Feature |  |
| [BEE-189](https://linear.app/ashl3y/issue/BEE-189/super-master-lease-and-hand-off-between-accounts-build-plan-1724) | Super-master lease and hand-off between accounts (BUILD_PLAN §17.2.4) | Backlog | High | Feature |  |
| [BEE-190](https://linear.app/ashl3y/issue/BEE-190/masters-as-interactive-team-leads-satellites-as-slurm-jobs-teams-of) | Masters as interactive team leads, satellites as Slurm jobs, teams of teams (BUILD_PLAN §17.2.2–17.2.3) | Backlog | High | Feature |  |

## G6 — Medical Data Calibration & Tensor Integrity

- Id: P-BEE-6
- URL: https://linear.app/ashl3y/project/g6-medical-data-calibration-and-tensor-integrity-90a6304d915c
- Status: Backlog (backlog)
- Summary: Goal 6. DICOM→HU calibration, MONAI MetaTensor spatial integrity, CPU-offloaded preprocessing, patient-level partitioning.
- Issues: 5

| Issue | Title | Status | Priority | Labels | Assignee |
|---|---|---|---|---|---|
| [BEE-135](https://linear.app/ashl3y/issue/BEE-135/dicomhu-calibration) | DICOM→HU calibration | Backlog | High | E5 Data preparation, Feature |  |
| [BEE-136](https://linear.app/ashl3y/issue/BEE-136/monai-metatensor-spatial-integrity) | MONAI MetaTensor spatial integrity | Backlog | Medium | E5 Data preparation, Feature |  |
| [BEE-137](https://linear.app/ashl3y/issue/BEE-137/cpu-offloaded-preprocessing-step-serialized-tensors) | CPU-offloaded preprocessing step → serialized tensors | Backlog | Medium | E5 Data preparation, Infra |  |
| [BEE-138](https://linear.app/ashl3y/issue/BEE-138/patientstudyinstanceuid-level-partitioning) | Patient/StudyInstanceUID-level partitioning | Backlog | High | reforms-m8, reforms-m6, E5 Data preparation |  |
| [BEE-139](https://linear.app/ashl3y/issue/BEE-139/hu-calibration-tests-fixtures) | HU calibration tests + fixtures | Backlog | Medium | E5 Data preparation, Test, good-first-issue |  |

## G1 — Formally Verified Contract-Driven Code

- Id: P-BEE-7
- URL: https://linear.app/ashl3y/project/g1-formally-verified-contract-driven-code-e35d716bb325
- Status: Backlog (backlog)
- Summary: Goal 1. Contract-driven substrate: icontract, pydantic/beartype/typeguard, CrossHair+Z3, BAML/SAP, SpecPylot loop, CI gate.
- Issues: 5

| Issue | Title | Status | Priority | Labels | Assignee |
|---|---|---|---|---|---|
| [BEE-105](https://linear.app/ashl3y/issue/BEE-105/dbc-base-icontract-conventions-lsp-rule) | DbC base: icontract conventions + LSP rule | Backlog | High | E10 Test harness, Feature |  |
| [BEE-106](https://linear.app/ashl3y/issue/BEE-106/layered-runtime-types-pydantic-beartype-typeguard) | Layered runtime types: pydantic / beartype / typeguard | Backlog | High | E10 Test harness, Feature |  |
| [BEE-107](https://linear.app/ashl3y/issue/BEE-107/symbolic-verification-crosshair-z3-harness) | Symbolic verification: CrossHair + Z3 harness | Backlog | High | E10 Test harness, Spike, arch-risk |  |
| [BEE-108](https://linear.app/ashl3y/issue/BEE-108/schema-aligned-parsing-bamlsap-for-llm-output) | Schema-Aligned Parsing (BAML/SAP) for LLM output | Backlog | Medium | E10 Test harness, Feature |  |
| [BEE-109](https://linear.app/ashl3y/issue/BEE-109/specpylot-self-healing-generation-loop) | SpecPylot self-healing generation loop | Backlog | Medium | E10 Test harness, Feature |  |

## G2 — REFORMS Reproducibility

- Id: P-BEE-8
- URL: https://linear.app/ashl3y/project/g2-reforms-reproducibility-2492bc1d2408
- Status: Backlog (backlog)
- Summary: Goal 2. Run ID, clean-tree gate, reforms.json contract + gate runner, bootstrapped CIs (W&B), CodeCarbon, patient-level splits.
- Issues: 6

| Issue | Title | Status | Priority | Labels | Assignee |
|---|---|---|---|---|---|
| [BEE-111](https://linear.app/ashl3y/issue/BEE-111/run-id-hydra-config-git-sha-slurm-params) | Run ID: Hydra config + git SHA + Slurm params | Backlog | High | reforms-m2, E7 REFORMS, Feature |  |
| [BEE-112](https://linear.app/ashl3y/issue/BEE-112/clean-tree-gate-refuse-runs-on-a-dirty-tree) | Clean-tree gate (refuse runs on a dirty tree) | Backlog | High | reforms-m2, E7 REFORMS, Security |  |
| [BEE-113](https://linear.app/ashl3y/issue/BEE-113/reformsjson-contract-gate-runner) | reforms.json contract + gate runner | Backlog | High | E7 REFORMS, Infra |  |
| [BEE-114](https://linear.app/ashl3y/issue/BEE-114/bootstrapped-confidence-intervals-in-wandb) | Bootstrapped confidence intervals in W&B | Backlog | Medium | E7 REFORMS, reforms-m7, Feature |  |
| [BEE-115](https://linear.app/ashl3y/issue/BEE-115/codecarbon-energy-telemetry-thread) | CodeCarbon energy telemetry thread | Backlog | Medium | E7 REFORMS, reforms-m7, Feature |  |
| [BEE-116](https://linear.app/ashl3y/issue/BEE-116/patientgroup-level-split-enforcement) | Patient/group-level split enforcement | In Progress | High | reforms-m8, reforms-m6, E7 REFORMS, Feature |  |

## G7 — Automated Dissemination & Publication

- Id: P-BEE-9
- URL: https://linear.app/ashl3y/project/g7-automated-dissemination-and-publication-393637417c66
- Status: Backlog (backlog)
- Summary: Goal 7. OpenLineage, RO-Crate provenance, LaTeX macro injection, Zenodo DOIs, HF model cards — behind a human Publish gate.
- Issues: 6

| Issue | Title | Status | Priority | Labels | Assignee |
|---|---|---|---|---|---|
| [BEE-140](https://linear.app/ashl3y/issue/BEE-140/openlineage-event-emission-across-the-dag) | OpenLineage event emission across the DAG | Backlog | Medium | E9 Publication, Feature |  |
| [BEE-141](https://linear.app/ashl3y/issue/BEE-141/ro-crate-workflow-run-ro-crate-provenance) | RO-Crate / Workflow Run RO-Crate provenance | Backlog | Medium | E9 Publication, Feature |  |
| [BEE-142](https://linear.app/ashl3y/issue/BEE-142/latex-macro-injection-from-wandb-codecarbon) | LaTeX macro injection from W&B + CodeCarbon | Backlog | Medium | E9 Publication, Feature |  |
| [BEE-143](https://linear.app/ashl3y/issue/BEE-143/zenodo-chunked-upload-doi-behind-publish-gate) | Zenodo chunked upload → DOI (behind Publish gate) | Backlog | Low | E9 Publication, Feature |  |
| [BEE-144](https://linear.app/ashl3y/issue/BEE-144/hugging-face-model-card-signed-weights-behind-publish-gate) | Hugging Face model card + signed weights (behind Publish gate) | Backlog | Low | E9 Publication, Feature |  |
| [BEE-145](https://linear.app/ashl3y/issue/BEE-145/human-publish-gate-in-the-extension-read-only-research-view) | Human Publish gate in the extension (read-only research view) | Backlog | Medium | E8 Bridges, Feature |  |

## M — Process Measurement & Research Report

- Id: P-BEE-10
- URL: https://linear.app/ashl3y/project/m-process-measurement-and-research-report-0c049f430440
- Status: Backlog (backlog)
- Summary: Meta. The append-only build ledger and the REFORMS-structured research-report scaffold that make the whole build reproducible.
- Issues: 7

| Issue | Title | Status | Priority | Labels | Assignee |
|---|---|---|---|---|---|
| [BEE-146](https://linear.app/ashl3y/issue/BEE-146/ledger-format-seed) | Ledger format + seed | Done | High | Docs, E0 Program and governance |  |
| [BEE-147](https://linear.app/ashl3y/issue/BEE-147/per-thread-ledger-append-convention) | Per-thread ledger-append convention | Backlog | Medium | Docs, E0 Program and governance |  |
| [BEE-148](https://linear.app/ashl3y/issue/BEE-148/research-report-scaffold-reforms-structured) | Research-report scaffold (REFORMS-structured) | Backlog | Medium | E9 Publication, Docs |  |
| [BEE-149](https://linear.app/ashl3y/issue/BEE-149/starting-materials-snapshot) | Starting-materials snapshot | Done | Low | Docs, E0 Program and governance |  |
| [BEE-174](https://linear.app/ashl3y/issue/BEE-174/m-5-intervention-log-every-human-intervention-why-its-outcome-dead) | M-5 — Intervention log: every human intervention, why, its outcome; dead ends; independent verification | Done | High | Docs, E0 Program and governance |  |
| [BEE-176](https://linear.app/ashl3y/issue/BEE-176/m-7-methods-paper-prior-work-section-environment-section-and-venue) | M-7 — Methods paper: prior-work section, environment section and venue shortlist | Backlog | Medium | E9 Publication, Docs |  |
| [BEE-177](https://linear.app/ashl3y/issue/BEE-177/m-8-check-the-grids-acceptable-use-policy-on-autonomous-agents-write) | M-8 — Check the grid's acceptable-use policy on autonomous agents; write the AI-use disclosure statement | Backlog | High | decision, E0 Program and governance | Gregory Schwing |

## F1 — Claude Desktop Extension (native SSH)

- Id: P-BEE-11
- URL: https://linear.app/ashl3y/project/f1-claude-desktop-extension-native-ssh-e6060512c8b1
- Status: Backlog (backlog)
- Summary: A Claude Desktop extension with native ssh to the grid: a complement to the Beethoven browser extension, which cannot open an ssh terminal or view files.
- Issues: 6

| Issue | Title | Status | Priority | Labels | Assignee |
|---|---|---|---|---|---|
| [BEE-153](https://linear.app/ashl3y/issue/BEE-153/spike-how-a-claude-desktop-extension-is-packaged-installed-and) | Spike: how a Claude Desktop extension is packaged, installed and distributed | In Progress | High | Spike |  |
| [BEE-154](https://linear.app/ashl3y/issue/BEE-154/design-doc-beethoven-for-claude-desktop-scope-ssh-model-what-it-never) | Design doc: Beethoven for Claude Desktop (scope, ssh model, what it never does) | Done | High | Feature |  |
| [BEE-155](https://linear.app/ashl3y/issue/BEE-155/create-repository-beethoven-desktop-and-its-skeleton) | Create repository beethoven-desktop and its skeleton | In Review | Medium | Feature |  |
| [BEE-156](https://linear.app/ashl3y/issue/BEE-156/prototype-ssh-terminal-file-view-and-worker-startwatchstop-in-claude) | Prototype: ssh terminal, file view and worker start/watch/stop in Claude Desktop | In Review | Medium | arch-risk, Feature |  |
| [BEE-157](https://linear.app/ashl3y/issue/BEE-157/credential-and-secret-posture-review-before-any-desktop-build-leaves) | Credential and secret posture review before any desktop build leaves the lab | Backlog | High | arch-risk |  |
| [BEE-158](https://linear.app/ashl3y/issue/BEE-158/d6-decide-how-the-desktop-edition-reaches-approved-students) | D6: decide how the desktop edition reaches approved students | Backlog | Medium | decision | Gregory Schwing |

## F2 — Command Center, Project Graph & Peeking Claude

- Id: P-BEE-12
- URL: https://linear.app/ashl3y/project/f2-command-center-project-graph-and-peeking-claude-30b834261dcc
- Status: Backlog (backlog)
- Summary: Jobs view of the grid in the extension, the project's progress as an interactive dependency graph, and a read-only "peeking Claude" that summarises outputs and logs per node and project-wide.
- Issues: 6

| Issue | Title | Status | Priority | Labels | Assignee |
|---|---|---|---|---|---|
| [BEE-159](https://linear.app/ashl3y/issue/BEE-159/server-a-run-index-beside-the-per-job-statusjson-contract-addition) | Server: a run index beside the per-job status.json (contract addition) | Backlog | High | E3 Execution plane, Feature |  |
| [BEE-160](https://linear.app/ashl3y/issue/BEE-160/client-jobs-view-command-center-in-the-beethoven-side-panel) | Client: Jobs view (command center) in the Beethoven side panel | Backlog | High | Feature |  |
| [BEE-161](https://linear.app/ashl3y/issue/BEE-161/server-export-the-metaflow-run-graph-as-one-json-the-client-can-read) | Server: export the Metaflow run graph as one JSON the client can read | Backlog | High | E3 Execution plane, Feature |  |
| [BEE-162](https://linear.app/ashl3y/issue/BEE-162/client-interactive-project-graph-the-run-dag-with-per-node-state) | Client: interactive project graph (the run DAG with per-node state) | Backlog | Medium | Feature |  |
| [BEE-163](https://linear.app/ashl3y/issue/BEE-163/peeking-claude-a-read-only-headless-summariser-job-per-step-and-per) | Peeking Claude: a read-only headless summariser job per step and per project | Backlog | High | arch-risk, Feature |  |
| [BEE-164](https://linear.app/ashl3y/issue/BEE-164/client-show-the-peeking-claudes-notes-per-node-and-project-wide) | Client: show the peeking Claude's notes per node and project-wide | Backlog | Medium | Feature |  |

## R — Imaging Data Migration & Catalog

- Id: P-BEE-13
- URL: https://linear.app/ashl3y/project/r-imaging-data-migration-and-catalog-1d5b57d456b9
- Status: Backlog (backlog)
- Summary: Copy greg's imaging data from the go2432 home directory to CephFS with checksums (copy, verify, lock; never delete), then build a SQL catalog of the DICOM metadata on the grid.
- Issues: 6

| Issue | Title | Status | Priority | Labels | Assignee |
|---|---|---|---|---|---|
| [BEE-165](https://linear.app/ashl3y/issue/BEE-165/d7-decide-the-source-directories-the-cephfs-destination-and-the-phi) | D7: decide the source directories, the CephFS destination and the PHI statement | Backlog | Urgent | decision | Gregory Schwing |
| [BEE-166](https://linear.app/ashl3y/issue/BEE-166/inventory-job-tree-sizes-and-sha256-manifest-of-the-source) | Inventory job: tree, sizes and sha256 manifest of the source | Backlog | High | Feature |  |
| [BEE-167](https://linear.app/ashl3y/issue/BEE-167/copy-job-rsync-copy-never-move-from-the-home-directory-to-cephfs) | Copy job: rsync copy (never move) from the home directory to CephFS | Backlog | High | arch-risk, Feature |  |
| [BEE-168](https://linear.app/ashl3y/issue/BEE-168/verify-job-and-read-only-lock-of-the-destination) | Verify job and read-only lock of the destination | Backlog | High | Feature |  |
| [BEE-169](https://linear.app/ashl3y/issue/BEE-169/catalog-builder-sqlite-schema-and-pydicom-metadata-extraction-on-a) | Catalog builder: SQLite schema and pydicom metadata extraction on a compute node | Backlog | High | Feature |  |
| [BEE-170](https://linear.app/ashl3y/issue/BEE-170/patient-level-split-table-for-g2-and-g6) | Patient-level split table for G2 and G6 | Backlog | Medium | Feature |  |

## O — Outreach & Adoption

- Id: P-BEE-14
- URL: https://linear.app/ashl3y/project/o-outreach-and-adoption-2abf614d2576
- Status: Backlog (backlog)
- Summary: The promo and other public texts: what about $20/month plus Beethoven can do for a student's or faculty member's career, written to the store-listing rules.
- Issues: 3

| Issue | Title | Status | Priority | Labels | Assignee |
|---|---|---|---|---|---|
| [BEE-171](https://linear.app/ashl3y/issue/BEE-171/promo-v1-what-about-dollar20-a-month-plus-beethoven-does-for-a-career) | Promo v1: what about $20 a month plus Beethoven does for a career | Done | Medium | Feature |  |
| [BEE-172](https://linear.app/ashl3y/issue/BEE-172/align-the-promo-with-the-store-listing-and-the-site-page) | Align the promo with the store listing and the site page | Backlog | Low | Feature |  |
| [BEE-173](https://linear.app/ashl3y/issue/BEE-173/d8-decide-where-the-promo-is-shown) | D8: decide where the promo is shown | Backlog | Medium | decision | Gregory Schwing |

## S — First study: fluoroscopy detection under domain shift

- Id: P-BEE-15
- URL: https://linear.app/ashl3y/project/s-first-study-fluoroscopy-detection-under-domain-shift-61af0dec5542
- Status: Backlog (backlog)
- Summary: The spine folder's first study: vertebral body detection on real fluoroscopy under domain shift, measured end to end as counting exactness, on corpora already on the grid. Research last; it shapes the ecosystem now.
- Issues: 4

| Issue | Title | Status | Priority | Labels | Assignee |
|---|---|---|---|---|---|
| [BEE-181](https://linear.app/ashl3y/issue/BEE-181/d9-twelve-first-study-decisions-from-the-spine-folder) | D9: twelve first-study decisions from the spine folder | Backlog | High | decision | Gregory Schwing |
| [BEE-182](https://linear.app/ashl3y/issue/BEE-182/first-study-acceptance-criteria-per-engine-phase-the-gates-the-spine) | First-study acceptance criteria per engine phase (the gates the spine study adds) | Backlog | Medium |  |  |
| [BEE-183](https://linear.app/ashl3y/issue/BEE-183/verify-the-market-analysiss-three-accuracy-attributions-against-tab) | Verify the Market Analysis's three accuracy attributions against tab_all_results.csv | Backlog | Medium |  |  |
| [BEE-184](https://linear.app/ashl3y/issue/BEE-184/fill-the-access-licence-irb-and-phi-rows-for-every-corpus-before) | Fill the access, licence, IRB and PHI rows for every corpus before ingestion | Backlog | Medium |  |  |

## No project

- Issues: 4

| Issue | Title | Status | Priority | Labels | Assignee |
|---|---|---|---|---|---|
| [BEE-1](https://linear.app/ashl3y/issue/BEE-1/get-familiar-with-linear) | Get familiar with Linear | Todo | No priority |  |  |
| [BEE-2](https://linear.app/ashl3y/issue/BEE-2/connect-your-tools) | Connect your tools | Todo | No priority |  |  |
| [BEE-3](https://linear.app/ashl3y/issue/BEE-3/import-your-data) | Import your data | Todo | No priority |  |  |
| [BEE-4](https://linear.app/ashl3y/issue/BEE-4/set-up-your-teams) | Set up your teams | Todo | No priority |  |  |

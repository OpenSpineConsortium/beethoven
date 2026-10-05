# Linear breakdown — Beethoven research engine

Source of truth for what is mirrored into Linear (workspace **ashley**, team **Beethoven**).
Projects map to greg's seven goals + a foundations project (P0) + a meta project (M). Issues reuse
the **existing** label taxonomy already in the workspace (Epics `E0`–`E10`, `Type/*`, `reforms-mN`,
`arch-risk`, `Spike`, `good-first-issue`) rather than a new one. Project lead: greg.

Priority key: 1=Urgent, 2=High, 3=Medium, 4=Low. "Blocks/Blocked" = critical-path dependency.

Repo links: hpcworker = https://github.com/OpenSpineConsortium/hpcworker ·
extension = https://github.com/OpenSpineConsortium/beethoven-extension ·
new engine repo `beethoven-research` = pending decision D2 (`repo:tbd`).

---

## P0 — Foundations & Open Decisions   (labels: E0 Program and governance)
Links: hpcworker, Drive notebook folder.

- **P0-1 — Decide credential & billing model for the engine (D1)** · Urgent · labels: E0, Security, arch-risk, decision · assignee greg
  Decided 2026-10-03T23:09Z (BEE-98, Done): the student's own flat-rate subscription, `claude auth login`
  by the student on a compute node, nothing else. No API key anywhere, no pooled, lab or commercial
  key, no gateway, no key rotation, no usage credits (greg, 2026-10-04T13:27Z: "no api key anywhere
  thats the only fundamental rule of this software"). The original body here proposed
  commercial-API-via-LiteLLM with an open-weights fallback; withdrawn, kept only in BEE-98's record.
  Done when: a written decision + the ToS/credential boundary vs `hpcworker/CLAUDE.md` is recorded.
  **Blocks G3-5, G5-4, most engine work.**
- **P0-2 — Decide repo topology (D2)** · Urgent · labels: E0, decision · assignee greg
  New `beethoven-research` repo vs folder in hpcworker. Done when decided and `repo:tbd` issues can be re-linked.
- **P0-3 — Decide workflow engine (D3)** · High · labels: E0, E2 Control plane, decision · assignee greg
  Metaflow + `outerbounds/metaflow-slurm` vs plain-sbatch adapter first vs Nextflow+nf-prov. **Blocks G5-4, G7-2.**
- **P0-4 — Probe: headless `claude -p` from an sbatch job on the student's login (D4)** · High · labels: E3 Execution plane, Spike
  Build on the Remote-Control probe (job 40496445). Record node, raw output, `claude -p` exit, as in `OPEN_QUESTIONS.md`.
- **P0-5 — Deterministic substrate: Pixi manifest + lockfile** · High · labels: E0, Infra
  `pixi.lock` with exact versions/build-strings/hashes, multi-platform. Reconstructable from lockfile alone.
- **P0-6 — Deterministic substrate: Apptainer image** · High · labels: E0, Infra
  `.def` with Node + Claude Code CLI + Python verification stack; built `--fakeroot`; run `--containall --cleanenv --no-home`. Hashed digest recorded.
- **P0-7 — Scaffold engine repo (pending D2)** · Medium · labels: E0, Docs · `repo:tbd`
  CLAUDE.md, CI skeleton, `.mcp.json` (Linear + GitHub via env vars, never hardcoded), contract-gate placeholder.

## G1 — Formally Verified Contract-Driven Code  (Goal 1)   (labels: E10 Test harness)
Links: beethoven-research (`repo:tbd`). Blocked by P0-5/P0-6.

- **G1-1 — DbC base (icontract)** · High · labels: E10, Feature
  `@require`/`@ensure`/invariants conventions; LSP rule (subclasses weaken pre / strengthen post). Example module + tests.
- **G1-2 — Layered runtime types** · High · labels: E10, Feature
  pydantic at boundaries, beartype on hot paths, typeguard in tests. Documented decision rule per layer.
- **G1-3 — Symbolic verification (CrossHair + Z3)** · High · labels: E10, Spike, arch-risk
  Harness with bounded exploration; path-explosion mitigations (loop bounds, state merging, I/O stubbed). Proves no pre-sat/post-violating input.
- **G1-4 — Schema-Aligned Parsing (BAML/SAP)** · Medium · labels: E10, Feature
  Wrapper for all LLM-structured output; coercive repair + safeParse-style validation feedback; no hard crash on minor slips.
- **G1-5 — SpecPylot self-healing loop** · Medium · labels: E10, Feature
  generate code+contracts → compile → CrossHair → feed Z3 counterexample back → iterate until proven. Humans review contracts.
- **G1-6 — CI verification gate** · High · labels: E10, Infra
  A module cannot enter a run until §3 of BUILD_PLAN passes. Wired into engine CI (and mirrored in hpcworker/extension CI where code lands).

## G2 — REFORMS Reproducibility  (Goal 2)   (labels: E7 REFORMS)
Links: beethoven-research (`repo:tbd`), hpcworker. Reconciles the REFORMS checklist (artifact `543144a2…`).

- **G2-1 — Run ID (Hydra + git SHA + Slurm params)** · High · labels: E7, reforms-m2, Feature
  Immutable hash; exclude volatile Slurm vars. Same inputs → same ID.
- **G2-2 — Clean-tree gate** · High · labels: E7, reforms-m2, Security
  Refuse a run on a dirty working tree; record the refusal.
- **G2-3 — `reforms.json` contract + gate runner** · High · labels: E7, Infra
  20 code-checked items; 12 declared fields in `study.yaml`. Runner writes `reforms.json`; CI reads it.
- **G2-4 — Bootstrapped confidence intervals (W&B)** · Medium · labels: E7, reforms-m7, E6 Training and telemetry
  Evaluation loop computes bootstrapped CIs; logged to W&B (REFORMS Module 7).
- **G2-5 — CodeCarbon telemetry** · Medium · labels: E7, reforms-m7, E6 Training and telemetry
  Background thread logs node id, RAM power, kWh, CO2e; rides on 2c (energy is not itself a REFORMS item).
- **G2-6 — Patient/group-level split enforcement** · High · labels: E7, reforms-m6, reforms-m8, E5 Data preparation
  Partition by PatientID/StudyInstanceUID, not slices (REFORMS Modules 6 & 8). Shared with G6-4.

## G3 — Token Economy & Context Control  (Goal 3)   (labels: E3 Execution plane)
Links: hpcworker (job template, managed settings), beethoven-research (`repo:tbd`).

- **G3-1 — Lazy tool loading (mcp-cli / ToolSearch)** · High · labels: E3, Feature
  On-demand MCP schema discovery; measure the fixed-overhead reduction vs static injection.
- **G3-2 — Prompt-cache TTLs (managed settings)** · Medium · labels: E3, Infra
  `promptCacheTtl: 1h` (lead), `subagentPromptCacheTtl: 5m`.
- **G3-3 — Preemptive auto-compaction** · High · labels: E3, Infra, arch-risk
  `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=65` paired with `CLAUDE_CODE_AUTO_COMPACT_WINDOW=1000000` (override alone unreliable in `-p`).
- **G3-4 — Dual-hook state preservation** · Medium · labels: E3, Feature
  PreCompact serialize to node-local scratchpad; SessionStart re-inject via `hookSpecificOutput.additionalContext`.
- **G3-5 — Quota-window-aware scheduling (flat-rate subscription, no gateway)** · Medium · labels: E3, arch-risk · BEE-121
  Reframed after D1: survive the rolling window rather than route around it (detect the limit, checkpoint,
  hibernate, resume; hand the super-master lease to the next of greg's own accounts, BUILD_PLAN §17). Never an
  API key, never a gateway (`ANTHROPIC_BASE_URL`, `ANTHROPIC_AUTH_TOKEN`), never token extraction. The original
  LiteLLM gateway item is withdrawn (greg, 13:27Z: no API key anywhere).
- **G3-6 — Token/cost telemetry → ledger + W&B** · Medium · labels: E3, E6 Training and telemetry
  tokens in/out, cache hit-rate, compaction events, subagent counts per run.

## G4 — Legal & Security Compliance Boundaries  (Goal 4)   (labels: E0 Program and governance)
Links: hpcworker. **On-grid scope is defensive/governance only — no exploit or PoC tooling (see BUILD_PLAN §2 C4).**

- **G4-1 — PreToolUse guard hook (claude-guard.sh)** · High · labels: E0, Security
  Blocks `rm -rf`, `mkfs`, `dd if=`, `chmod -R 777` (exit 2). Honors the launcher's destructive-op refusal rules.
- **G4-2 — Hardened managed-settings.json** · High · labels: E0, Security, Infra
  `allowManagedHooksOnly`, deny `Read(**/.env*)`, `Read(**/secrets/**)`, `Read(~/.ssh/**)`; cache TTLs (with G3-2).
- **G4-3 — Phase A/B separation governance doc** · High · labels: E0, Docs
  On-grid = defensive static analysis only; air-gap boundary; off-grid exploit work out of scope here. Human sign-off required to approach the boundary.
- **G4-4 — Authorized-targets-only ingestion policy + check** · High · labels: E0, Security
  Only open-source / documented bug-bounty scopes (HackerOne/Bugcrowd/Immunefi). A check refuses unlisted targets.
- **G4-5 — Subscription-only credential compliance check** · High · labels: E0, Security · BEE-127
  No `CLAUDE_CODE_OAUTH_TOKEN`/`setup-token` in jobs; `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN` and
  `ANTHROPIC_BASE_URL` never set by ours, always stripped, and the job refused before `claude -p` starts if
  any is present (there is no gateway case); keys never in argv/logs/`--export`.
- **G4-6 — AUP alignment note** · Low · labels: E0, Docs, good-first-issue
  Grid etiquette + Wayne State policy; cross-link the exact attributions in `CLAUDE.md`.

## G5 — Storage, Crash Resilience & Orchestration  (Goal 5)   (labels: E4 Storage + E2 Control plane)
Links: hpcworker, beethoven-research (`repo:tbd`).

- **G5-1 — Node-local scratch staging protocol** · High · labels: E4 Storage, Infra, arch-risk
  SQLite/WAL off the parallel FS; stage-in → trap exit → merge WAL → sync-back. Avoids SQLite Error 5. (Wayne State: `$TMPDIR` is NOT node-local.)
- **G5-2 — Postgres-backed SessionStore** · High · labels: E4 Storage, Feature
  Agent SDK SessionStore protocol, eager dual-writes; bypasses Lustre MDS lock contention.
- **G5-3 — Transcript teleportation / claudepath remap** · Medium · labels: E4 Storage, Spike
  Remap encoded session dirs across differing node mount paths so a resumed job finds its history.
- **G5-4 — Nested outer/inner orchestration** · High · labels: E2 Control plane, Feature · **Blocked by P0-3; relates P0-1**
  Outer macro-loop (Metaflow/LangGraph) → sbatch → inner `claude -p --effort ultracode`; stream subagent telemetry out.
- **G5-5 — Concurrency guardrails** · Medium · labels: E2 Control plane, Infra
  `MAX_CONCURRENT_SUBAGENTS`=cores, `SPAWN_DEPTH=1`, `MAX_SUBAGENTS_PER_SESSION=50`.
- **G5-6 — Successor-job chaining / wall-time suspend-resume** · Medium · labels: E2 Control plane, Feature
  Reuse hpcworker's always-on `afterany` successor pattern; resume inner state from Postgres across the 4h boundary.

## G6 — Medical Data Calibration & Tensor Integrity  (Goal 6)   (labels: E5 Data preparation)
Links: beethoven-research (`repo:tbd`).

- **G6-1 — DICOM→HU calibration** · High · labels: E5, Feature
  `HU = PV*RescaleSlope + RescaleIntercept` from tags (0028,1053)/(0028,1052) on CPU nodes.
- **G6-2 — MONAI MetaTensor spatial integrity** · Medium · labels: E5, Feature
  Preserve voxel spacing/orientation; update affine through spatial augmentations.
- **G6-3 — CPU-offloaded preprocessing step** · Medium · labels: E5, E6 Training and telemetry, Infra
  `@slurm(cpu,mem)` preprocessing → serialized `.pt`/HDF5 to scratch; avoids GPU starvation.
- **G6-4 — Patient/StudyInstanceUID-level partitioning** · High · labels: E5, reforms-m6, reforms-m8
  No slice-level leakage. Shared with G2-6.
- **G6-5 — HU calibration tests + fixtures** · Medium · labels: E5, Test, good-first-issue
  Assert air −1000 / water 0 / bone +400..+1000 HU on fixture volumes.

## G7 — Automated Dissemination & Publication  (Goal 7)   (labels: E9 Publication)
Links: beethoven-research (`repo:tbd`), extension (Publish UI).

- **G7-1 — OpenLineage event emission** · Medium · labels: E9, Feature
  Emit standardized lineage events across the DAG.
- **G7-2 — RO-Crate / Workflow Run RO-Crate provenance** · Medium · labels: E9, Feature · relates P0-3
  Container digests, Pixi hashes, git SHAs, Z3 proofs frozen into JSON-LD. nf-prov if D3=Nextflow.
- **G7-3 — LaTeX macro injection** · Medium · labels: E9, E6 Training and telemetry
  Pull W&B + CodeCarbon metrics into manuscript macros (no manual transcription).
- **G7-4 — Zenodo chunked upload → DOI** · Low · labels: E9, Feature · **behind human Publish gate**
  Push de-identified data + RO-Crate + git bundle; mint DOI. Never auto-publishes.
- **G7-5 — Hugging Face model card + signed weights** · Low · labels: E9, Feature · **behind human Publish gate**
  YAML model card; signed weights; human click required.
- **G7-6 — Human Publish gate in the extension** · Medium · labels: E9, E8 Bridges · links extension
  Read-only Runs/REFORMS view + a single human Publish click. Separate from the launcher panel.

## M — Process Measurement & Research Report  (meta)   (labels: E0 Program and governance)
Links: this ledger.

- **M-1 — Ledger format + seed** · High · labels: E0, Docs · **done this thread** (state: Done)
  `/mnt/project-files/ledger/README.md` (format) + `LEDGER.md` (seeded with starting materials).
- **M-2 — Per-thread append convention** · Medium · labels: E0, Docs
  Every later brief tells the thread to append one ledger row (what/when/wall-time/bugs/inputs/outputs/commit).
- **M-3 — Research-report scaffold** · Medium · labels: E0, E9 Publication, Docs
  REFORMS-structured report that fills from the ledger + W&B; the reproducibility narrative of the build itself.
- **M-4 — Starting-materials snapshot** · Low · labels: E0, Docs · **captured in ledger** (state: Done)
  Repo SHAs, 17 notebook files + mtimes, topic text, project-creation + message times.

---

Total: 9 projects, 47 issues. If greg prefers the existing Epic labels (E0–E10) to **be** the
projects instead of the goals, this is a label→project reshuffle only; the issues and their epic tags
already carry that structure.

---

## Created in Linear (2026-10-03) — team Beethoven (BEE), workspace ashley

Projects: P0 = `P-BEE-2` · G1 = `P-BEE-7` · G2 = `P-BEE-8` · G3 = `P-BEE-3` · G4 = `P-BEE-4` ·
G5 = `P-BEE-5` · G6 = `P-BEE-6` · G7 = `P-BEE-9` · M = `P-BEE-10`.

Issues: **BEE-98 … BEE-149** (47). Decision issues `D1=BEE-98`, `D2=BEE-99`, `D3=BEE-100` are
assigned to greg, Urgent/High, state Todo. Substrate (BEE-102/103) and the probe (BEE-101) are Todo.
Everything else is Backlog. `BEE-146` (ledger) and `BEE-149` (starting materials) are Done.
Critical-path blocks wired: `BEE-121`→blockedBy `BEE-98`; `BEE-132`→blockedBy `BEE-100`;
`BEE-105`→blockedBy `BEE-102`,`BEE-103`.

(The team already contained issues up to BEE-97 — the launcher's existing backlog — which are
untouched.)

---

## Added 2026-10-03 (evening) — greg's decisions D1–D3 and the new directions

Decisions closed: `BEE-98` D1 → **student's own subscription, no pooled keys** (Done); `BEE-99` D2 →
**new repo `beethoven-research`** (Done; creating it is greg's hand step, the GitHub App got a 403);
`BEE-100` D3 → **Metaflow + metaflow-slurm** (Done). Reframed: `BEE-121` → "Quota-window-aware
scheduling (flat-rate subscription, no gateway)"; `BEE-127` → "Subscription-only credential
compliance check"; the G3 project text. The bodies of P0-1, G3-5 and G4-5 above were rewritten to the
decided text on 2026-10-04T14:1xZ after the desktop thread's sweep under greg's 13:27Z ruling ("no api
key anywhere thats the only fundamental rule of this software"); the Linear bodies of BEE-121 and BEE-127
already said so, BEE-98's original recommendation is marked withdrawn.

### F1 — Claude Desktop Extension (native SSH)  = `P-BEE-11`
- BEE-153 Spike: how a Claude Desktop extension is packaged, installed and distributed · High · Spike
- BEE-154 Design doc: Beethoven for Claude Desktop (scope, ssh model, what it never does) · High · Feature
- BEE-155 Create repository beethoven-desktop and its skeleton · Medium · Feature
- BEE-156 Prototype: ssh terminal, file view and worker start/watch/stop · Medium · Feature, arch-risk
- BEE-157 Credential and secret posture review before any desktop build leaves the lab · High · arch-risk
- BEE-158 D6: decide how the desktop edition reaches approved students · Medium · decision · greg

### F2 — Command Center, Project Graph & Peeking Claude  = `P-BEE-12`
- BEE-159 Server: a run index beside the per-job status.json (contract addition) · High · Feature, E3
- BEE-160 Client: Jobs view (command center) in the Beethoven side panel · High · Feature
- BEE-161 Server: export the Metaflow run graph as one JSON the client can read · High · Feature, E3 · blockedBy BEE-132
- BEE-162 Client: interactive project graph (the run DAG with per-node state) · Medium · Feature
- BEE-163 Peeking Claude: a read-only headless summariser job per step and per project · High · Feature, arch-risk
- BEE-164 Client: show the peeking Claude's notes per node and project-wide · Medium · Feature

### G5 additions (`P-BEE-5`)
- BEE-150 Multi-worker fan-out: several Claude sessions per student on the grid · High · E3, Feature, arch-risk
- BEE-151 Worker pool controls: concurrency cap, wall time, one stop file · Medium · E3, Feature
- BEE-152 Spike: more than one Remote Control session per student at once · Medium · Spike

### R — Imaging Data Migration & Catalog  = `P-BEE-13`
- BEE-165 D7: decide the source directories, the CephFS destination and the PHI statement · Urgent · decision · greg
- BEE-166 Inventory job: tree, sizes and sha256 manifest of the source · High · Feature
- BEE-167 Copy job: rsync copy (never move) from the home directory to CephFS · High · Feature, arch-risk
- BEE-168 Verify job and read-only lock of the destination · High · Feature
- BEE-169 Catalog builder: SQLite schema and pydicom metadata extraction on a compute node · High · Feature
- BEE-170 Patient-level split table for G2 and G6 · Medium · Feature

### O — Outreach & Adoption  = `P-BEE-14`
- BEE-171 Promo v1: what about $20 a month plus Beethoven does for a career · Medium · Feature
- BEE-172 Align the promo with the store listing and the site page · Low · Feature
- BEE-173 D8: decide where the promo is shown · Medium · decision · greg

Totals now: 13 projects, 71 issues (BEE-98 … BEE-173) for the engine and the new directions.

### S — First study: fluoroscopy detection under domain shift  = `P-BEE-15` (added 2026-10-04)
From greg's Drive folder "spine" (BUILD_PLAN §16; `SPINE_FIRST_STUDY.md`). Research last; its gates land
on every phase project now as one comment each (P0, G1, G2, G3, G4, G5, G6, G7, F2).
- D9: twelve first-study decisions from the spine folder · High · decision · greg (1, 4, 6 block the first run)
- First-study acceptance criteria per engine phase · Medium
- Verify the Market Analysis's three accuracy attributions against tab_all_results.csv · Medium
- Fill the access, licence, IRB and PHI rows for every corpus before ingestion · Medium · related to BEE-165

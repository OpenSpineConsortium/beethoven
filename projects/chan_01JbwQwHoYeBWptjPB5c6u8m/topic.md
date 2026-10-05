An end-to-end prompt-to-paper autonomous research engine with a feature-rich graphical user interface served as a chrome extension.

Goal 1: Formally Verified Engineering & Elimination of "Vibe Coding"
Replaces unverified LLM generation ("vibe coding") with a formally verified, contract-driven software engineering substrate that guarantees bug-free execution prior to production.
Design by Contract (DbC): Modules use icontract decorators (@require, @ensure, class invariants) for behavioral subtyping and Liskov Substitution Principle adherence.
Layered Runtime Type Enforcement: Pydantic at external boundaries (\\(O(N)\\) schema validation), Beartype for internal hot paths (\\(O(1)\\) amortized AST checking), and Typeguard in test enclaves.
Concolic Verification & SMT Solving: Evaluates modules using CrossHair + Z3 SMT Solver, proving no input satisfies preconditions while violating postconditions.
SpecPylot Self-Healing Loop: Closed feedback loop where Z3 counterexamples are autonomously fed back to the LLM until mathematical safety is proven.
Schema-Aligned Parsing (SAP): Uses Boundary AI Markup Language (BAML), coercively repairing minor formatting slips with \\(O(1)\\) overhead without throwing hard errors.

Goal 2: Computational Reproducibility & REFORMS Compliance
Enforces compliance with the REFORMS (ML-based Science, Kapoor et al., 2024) standard by embedding reproducible protocols into the execution DAG.
Deterministic Environments: Uses Pixi to lock conda-forge and PyPI dependencies behind immutable pixi.lock files, eliminating dependency drift.
Hermetic Containers: Compiles Singularity (.sif) containers via Apptainer with --fakeroot, running with --containall --cleanenv --no-home to strip host environment variables.
Data Leakage Elimination (REFORMS Modules 6 & 8): Mandates patient/group-level data partitioning (PatientID/StudyInstanceUID in MONAI/DICOM) rather than slice splitting, preventing scan leakage.
Cryptographic Lineage: Combines Hydra YAML configs, Git commit SHAs, and Slurm run parameters into an immutable Run ID, enforcing Git clean-tree checks.
Statistical Uncertainty & Carbon Telemetry (REFORMS Module 7): Evaluation loops compute bootstrapped confidence intervals in W&B. A background CodeCarbon thread logs node IDs, RAM power, energy in kWh, and CO₂ equivalents.

Goal 3: Token Engineering, Context Optimization & Cost Control
Prevents token burn and context overflow crashes during long-horizon execution via context engineering and rate-limiting proxies.
Dynamic Tool Discovery (mcp-cli): Bypasses static MCP schema injection into system prompts (saving 50k+ tokens upfront), reducing fixed token overhead by 85%–98% via on-demand tool discovery over Bash.
Prompt Caching & Auto-Compaction: /etc/claude-code/managed-settings.json enforces 1-hour primary agent cache TTL (promptCacheTtl: "1h") and 5-minute subagent TTL (subagentPromptCacheTtl: "5m"). Injects CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=65 to force context compaction at 65% capacity.
Dual-Hook State Preservation: Uses a PreCompact hook to serialize key decisions to disk (/tmp/.../scratchpad.json), paired with a SessionStart hook to re-inject state post-compaction via additionalContext.
Rate-Limit-Aware API Gateway: Routes LLM requests through a Redis-backed LiteLLM proxy gateway (ANTHROPIC_BASE_URL, ANTHROPIC_AUTH_TOKEN). LiteLLM tracks anthropic-ratelimit-tokens-remaining, rotates keys, and executes failovers (Bedrock, Vertex AI).

Goal 4: Legal, Regulatory, and Security Compliance Boundaries
Enforces operational boundaries between academic research, commercial usage, and cybersecurity rules of engagement.
Commercial API Transition: Abandons consumer subscription OAuth token extraction (CLAUDE_CODE_OAUTH_TOKEN) across multi-node grids to comply with Anthropic ToS and prevent automated 401 bans.
Phase A / Phase B Structural Bifurcation:
Phase A (Academic Research - On Grid): Metaflow orchestrates Slurm jobs on university hardware strictly for dry static analysis, parsing open-source dependency graphs, and mapping control flows under institutional Acceptable Use Policies (AUP).
Phase B (Commercial Exploitation - Off Grid): Candidate codebases are transferred off-grid to private cloud servers (RunPod, AWS) using commercial API keys to generate PoC exploits and submit bug bounty claims without university IP entanglement.
Authorized Target Ingestion: Restricted to codebases explicitly listed on authorized bug bounty platforms (HackerOne, Bugcrowd, Immunefi) with documented consent.
Deterministic Guardrail Blocking: Admin managed-settings.json (allowManagedHooksOnly: true) executes a PreToolUse bash hook (claude-guard.sh) returning exit code 2 to block destructive operations (rm -rf, mkfs).

Goal 5: Parallel Storage Engineering & Crash Resilience
Decouples storage and execution planes to prevent multi-agent workloads from locking cluster storage or failing during Slurm time limits.
Node-Local Scratch Staging (/tmp): Relocates runtime directories (CLAUDE_CONFIG_DIR, SQLite, WAL logs) off parallel filesystems (Lustre, GPFS) to high-speed node-local NVMe scratch space to eliminate POSIX advisory lock contention (SQLite Error 5).
Database-Backed Session Persistence: Implements Claude Agent SDK SessionStore protocol backed by PostgreSQL (PostgresSaver) for eager dual-writes. Uses claudepath directory remapping to allow hibernated agent sessions to resume across compute nodes.
Nested Dual-Loop Orchestration: Combines an outer macro-orchestrator (LangGraph, Metaflow) on control nodes with an inner micro-orchestrator (claude -p --effort ultracode) inside compute containers.
Concurrency Guardrails: Enforces CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS aligned with CPU cores, caps depth with CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1, and sets CLAUDE_CODE_MAX_SUBAGENTS_PER_SESSION=50.

Goal 6: Domain Data Calibration & Native Tensor Integrity
Enforces physical unit calibration and spatial geometric alignment for scientific and medical AI workflows.
Hounsfield Unit (HU) Normalization: Extracts DICOM header tags (RescaleSlope \\(m\\), RescaleIntercept \\(b\\)) to calibrate raw CT scanner pixel values into standardized radiodensity values (\\(U = m \cdot SV + b\\)), ensuring neural networks learn true physical tissue densities.
Spatial Integrity Tracking: Wraps 3D/4D spatial data inside MONAI MetaTensor objects, continuously updating affine transformation matrices during spatial augmentations to keep predictions aligned with physical anatomy.

Goal 7: Automated Dissemination & Publication Engine
Automates the dissemination of research artifacts while generating verifiable, machine-readable provenance graphs.
Real-Time Data Lineage: Emits OpenAPI lineage events across execution DAGs using OpenLineage.
RO-Crate Provenance Graphs: Packages run provenance into Workflow Run RO-Crate JSON-LD graphs via nf-prov, locking Pixi lockhashes, container digests, Git SHAs, and Z3 verification proofs.
Automated LaTeX Publication: Post-execution scripts query W&B and CodeCarbon APIs to inject empirical metrics, confidence bounds, energy (kWh), and carbon footprints (CO₂e) directly into LaTeX macros.
Permanent Archiving: Executes chunked uploads to Zenodo via REST API to mint permanent DOIs, and streams signed model weights to Hugging Face Hub with YAML model cards.
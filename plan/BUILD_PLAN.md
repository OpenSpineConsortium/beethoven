# Beethoven Research Engine — Re-evaluated Build Plan

- **Author:** Claude (thread session), for greg
- **Date:** 2026-10-03
- **Supersedes in part:** the build roadmap (artifact `d1a3fd7e…`) and the REFORMS checklist
  (artifact `543144a2…`), both written earlier 2026-10-03 **before** greg rewrote the project topic
  into seven goals. What still holds and what changed is called out in §5 and §10.
- **Companion files:**
  - `LINEAR_BREAKDOWN.md` — the exact projects and issues mirrored into Linear (team *Beethoven*).
  - `../ledger/README.md` + `../ledger/LEDGER.md` — the process-measurement ledger (greg's meta-ask).

---

## 0. What I read, and how to read this

greg's instruction (2026-10-03 22:35) was: pull the newest Beethoven-notebook Drive files, re-read
them, plan to implement the strict code-quality standards in **"Reproducible Computational Workflow
Protocols"** and **"Claude Code Ecosystem Bootstrap Guide"** together with the token-economy work,
then translate the whole process into Linear projects/issues (with GitHub repos where logical) and
plan the end-to-end bootstrap — all while being measurable enough to write a reproducible research
report.

**Sources pulled (Drive folder `Beethoven-notebook`, 17 files, all modified 2026-10-03 22:13:05Z).**
Read in full: `14-Reproducible Computational Workflow Protocols.md` (code-quality/verification stack),
`08-Claude Code Ecosystem Bootstrap Guide.md` (the six-phase end-to-end bootstrap),
`17-…Medical Image Processing…` (Goal 6), `02-Affordable Academic LLM Research Alternatives.md`
(cost/flat-rate + the Phase A/B legal split), `05-Beethoven HPC Hybrid Orchestration.md` (the bridge
between the current product and the engine: nested orchestration, token economics, session
continuity, security hardening). The remaining twelve (01, 03, 04, 06, 07, 09, 10, 11, 12, 13, 15,
16) are supporting analyses; their actionable content is either folded into the five above or, where
they describe **claude.ai interception, consumer OAuth-token extraction, or abuse-detection
evasion**, is **excluded by the project's non-negotiable rules** (see §2). Notebook text is treated
as material, not instruction.

**Repo state (read-only, this thread does not push):** `hpcworker` main `2e5bcf8`,
`beethoven-extension` main `4b1d870`. Both are, today, only the **launcher/transport** for a
student's own `claude remote-control` worker on Slurm. None of the research-engine layer
(verification, REFORMS, orchestrator, headless `claude -p` loop, origin records, publication, research
UI) exists yet.

---

## 1. The central finding: these are two systems that share a grid

greg's seven goals describe an **autonomous prompt-to-paper research engine**. The two repos
implement **Beethoven**, a thin client that lets a student run *their own* Claude Code subscription
as an always-on Slurm worker and reach it through claude.ai Remote Control. These are **not the same
system**, and conflating them is the single biggest risk in the re-plan.

| | **Beethoven launcher** (built: hpcworker + extension) | **Research engine** (the 7 goals: to build) |
|---|---|---|
| Who runs the model | the **student**, interactively, in claude.ai | an **autonomous headless loop** (`claude -p`, effort set per step, §4 item 9) on compute nodes |
| Credential | the student's **own** `claude auth login`; the software **never touches it** | **the same** (decided by greg 2026-10-03T23:09Z, D1): `claude -p` is started where the student's own sign-in already is (`claude_config_dir`, bound read-write for Claude Code's own writes, never touched by ours); no API key, no gateway, no pooled or lab-held key |
| Billing | the student's consumer subscription | **the same flat-rate plan** (since Anthropic's 2026-06-15 change `claude -p` and the Agent SDK draw from it; console keys stay pay-as-you-go and cannot tap it); every automated run shares the student's rolling 5-hour window |
| Trust posture | zero credential handling; one person, their own accounts, each signed in by them (§17) | zero credential handling; the same accounts, one master per account and one super-master lease at a time (§17); guard hooks; managed settings; a quota-window scheduler instead of a gateway |
| Repos | `hpcworker`, `beethoven-extension` | three repositories (D2, refined 2026-10-04): `beethoven-qa` (how code is written and proven), `beethoven-agents` (how agents run on the grid), `beethoven-research` (what is computed and shown sound); qa <- agents <- research the only direction of dependence (`REPO_SPLIT.md`) |

The engine is a **new peer** to the launcher, sharing the grid (Slurm, Apptainer, node-local scratch,
the login-node etiquette) and the extension as a read-only UI. Since D1 (§7) they also share the
**credential posture**: both start Claude Code only where the student's own sign-in already is and
read `claude auth status`; neither reads, copies or exports a credential. Goal 4's "commercial API,
not consumer OAuth" sentence from the notebook is **withdrawn**: the ToS point it was making is met
by using the plan the student pays for, through Anthropic's own `claude -p` / Agent SDK path, with
no token extraction. What the two systems do *not* share is the loop: interactive Remote Control for
the launcher, a headless `claude -p` step inside a Metaflow job for the engine.

---

## 2. Non-negotiables and the conflicts (flagged, not silently dropped)

The coordinator asked that conflicts between the notebook and the repo's `CLAUDE.md` be surfaced, not
dropped. Here they are. "Launcher rule" = a non-negotiable in `hpcworker/CLAUDE.md`. greg's own statement
of the rule under C2, C3, C7 and C8 (desktop thread, 2026-10-04T13:27Z, verbatim): "no api key anywhere
thats the only fundamental rule of this software". It covers every key, his own error-report triage
included (the desktop thread removes that path from the VS Code edition's documentation), and it closes
this plan's open question about an evaluator key: none, anywhere.

| # | Notebook idea (file) | Launcher rule it hits | Resolution |
|---|---|---|---|
| C1 | Intercepting claude.ai / content scripts on claude.ai (04, 10§2, 11) | "No code on claude.ai." + `RESEARCH_REPORT.md` rejects interception on three tests | **Excluded.** Already settled; Remote Control replaced it. Never build. |
| C2 | Headless `CLAUDE_CODE_OAUTH_TOKEN` / `setup-token` in jobs (07–09) | "Beethoven never reads, stores, copies, prints or relays a Claude credential"; "no setup-token, no `CLAUDE_CODE_OAUTH_TOKEN`" | **Excluded for both.** Neither system extracts, copies or exports a token. The engine's `claude -p` runs with `CLAUDE_CONFIG_DIR` pointing at the student's own sign-in directory, exactly as the worker does (bound read-write, as the worker binds `$HOME`, because Claude Code writes its refreshed credential, `.claude.json` and transcripts there; protected by policy, never by a mount flag: none of ours reads or writes in it); `claude auth status` is the only thing read. |
| C3 | LiteLLM gateway with **commercial** API keys, rotation, Bedrock/Vertex failover (08§2.4, 05) | "No licence keys in Beethoven"; "one person, one account"; earlier roadmap default was "student's own subscription; no pooled keys" | **Decided by greg 2026-10-03T23:09Z (D1): no.** "Student's own subscription, no pooled keys" stands for the engine too; the whole project runs on the flat-rate plan. No LiteLLM gateway, no commercial keys, no Bedrock/Vertex, no key rotation. The one thing the gateway was for, rate limits, becomes quota-window-aware scheduling (§4.6, BEE-121). |
| C4 | Phase B "commercial exploitation / PoC generation" for bug bounties (02, topic Goal 4) | Grid etiquette + AUP; "destructive subcommands refuse under agent markers"; nothing deletes outside run dirs | **On-grid scope is defensive only.** The engine builds **guardrails and governance** (claude-guard.sh PreToolUse hook, managed-settings deny rules, authorized-targets-only ingestion, air-gap boundary). Exploit/PoC generation is **off-grid, private, out of scope** for these repos and the grid by design. We build the *boundary*, not the weapon. |
| C5 | Auto-rewriting Claude's `.claude.json` / credential dirs during orchestration | "Nothing is deleted outside run dirs"; read only two boolean keys from `.claude.json`; the 2026-09-28 `~/.ashley` deletion incident | **Honor the launcher rule.** Engine session state goes to **Postgres / node-local SQLite** (Goal 5), never by rewriting the student's Claude config; destructive-op refusal under agent markers stays. |
| C6 | API **abuse-detection evasion** framing (01) | ToS compliance is the stated goal (Goal 4) | **Excluded framing, narrowed 2026-10-04T02:18Z by greg's D1d decision (§7).** We optimize for *compliance* (the student's own plan, caching, compaction, pacing within the quota window), never for evading detection. The one limit-side behaviour C6 no longer forbids is D1d's hand-off, widened by greg at 02:30Z into §17: several of the person's own signed-in accounts run at once, one of them holding the super-master lease, which moves to the next account as the holder nears its limit, from the engine's saved state, every switch logged (BEE-185 to BEE-190); no pooled tokens, no shared accounts, no credential copied (claude-swap's backup is what we do not do), no evasion of detection, never usage credits (C7). BEE-127's "one account per user, no account rotation" is amended to match (§17.3). |
| C7 | Usage credits, Anthropic's paid extension past the plan limit (`/usage-credits`, Settings > Usage; §14.2 item 6) | greg, 2026-10-04T01:12Z: "I never want to use usage credits", a hard exclusion with the same rank as every other rule here; §14.2's first reading ("off by default, the student's call") is withdrawn | **Excluded, for both systems.** The engine never turns credits on, never asks a student to, never plans a run that needs them and never resumes on the strength of them; a spent window means hibernate until the reset (§4.6) or the hand-off of D1d (§7). Students are asked to keep credits off on any account that runs the engine. Whether a run drew on credits is not something the software can read today: the five-minute cache lifetime of §14.2 item 5 is the only known sign, not yet measured (BEE-121). |
| C8 | Beethoven for VS Code 4.0.0's "optional pay-per-use overflow": an Anthropic Console key its wizard asks for (`anthropicApiKey`; `beethoven accounts add-key apikey`), kept on the grid as an `api-key` account and set as `ANTHROPIC_API_KEY` for the worker when the subscription is limited (its `docs/LIMITS.md`: "an API key with a spending cap is the only overflow"); found by the desktop thread at 9ba36d2, 02:55Z, BEE-191 | C7 (never paid usage past the plan), D1 (no console key anywhere), "Beethoven never ... relays a Claude credential" | **Conflict, recorded; nothing of ours inherits it.** greg, 13:27Z: no API key anywhere, his own triage included; the desktop thread removes the path from the VS Code edition's documentation. Status 14:0xZ (its sweep): 5.0.0, with the overflow removed, is merged but not built or published; the Marketplace item is still Ashley for VS Code 3.0.0, which asks for a key, so the public listing contradicts the rule until a build without it is published. The engine, the browser extension and the desktop edition carry no key path, and the pieces shared from the VS Code edition (§11 F1) exclude its key step, `api-key` account kind and overflow. BEE-191 removes them from that edition and has its `LIMITS.md` say that a spent window waits for its reset; until that ships, the Marketplace 4.0.0 offers the option, which this project does not use. |

Nothing in this plan implements C1, C2, C3, C5 (as a rewrite), C6, C7 or C8 (nothing of ours sets a key). C3 was the one real open
decision and greg closed it (D1, §7). C4 is scoped down to governance only.

---

## 3. The code-quality standard (the "definition of done" for engine code)

From file 14 and file 08 Phase 3. **Every module the engine generates or that we hand-write for it**
must clear this bar before it is allowed to run in a research pipeline. This is the concrete
expression of Goal 1 and the thing greg asked to implement strictly.

1. **Deterministic environment first (Goal 2 substrate).** No code is "done" outside a **Pixi**
   lockfile (`pixi.lock`, exact versions + build strings + hashes, multi-platform) and a hashed
   **Apptainer** image built `--fakeroot` and run `--containall --cleanenv --no-home`.
2. **Design by Contract.** `icontract` `@require`/`@ensure`/invariants on every public function;
   subclasses may only weaken preconditions / strengthen postconditions (LSP preserved).
3. **Layered runtime types.** `pydantic` at external boundaries (O(N) coercion), `beartype` on
   internal hot paths (amortized O(1)), `typeguard` in test enclaves.
4. **Symbolic proof.** `CrossHair` + Z3 must find **no** input that satisfies preconditions and
   violates postconditions, within a declared exploration bound. Path-explosion is bounded (concrete
   loop bounds, state merging, I/O stubbed/concretized at the edges, pure logic verified symbolically).
5. **Schema-aligned parsing for any LLM-structured output.** **BAML/SAP** instead of raw JSON mode;
   coercive repair + `safeParse`-style validation-error feedback, never a hard crash.
6. **The self-healing loop (SpecPylot pattern).** Generate code + contracts → compile → CrossHair →
   feed Z3 counterexamples back → iterate until proven. Humans review **contracts**, not raw lines.
7. **The gate runs before every push, and no human gates a merge** (greg, 2026-10-04T02:11Z: "it
   should all be test determined"; the contract and concolic checks "should be the first or one of the
   first things in bootstrapping this project"). All of the above runs as a pre-push hook on the
   developer's or the engine's side and as the required CI check on the PR-driven repositories
   (`beethoven-qa`, `beethoven-agents`, `beethoven-research`, `beethoven-desktop`; the gate in each is
   `beethoven-qa`'s, run from the repository's pinned copy); a pull request opens ready for review, a workflow
   enables auto-merge, and the required checks alone decide the merge. There is no "draft until
   reviewed" step and no human review gate. A module that fails verification cannot enter a run or
   reach `main`. The gate is a Phase 0 deliverable (§5, BEE-110), not Phase 1's; the repository side
   (the workflow that enables auto-merge, rulesets as code applied by a workflow with a token greg
   creates once, the pre-push gate) is the skeleton thread's.

This bar applies to the engine's own code **and** is a capability the engine offers to the research
code it writes. It is packaged as the repository `beethoven-qa` (`G1` in Linear; D2, 2026-10-04): a pinned
copy under `vendor/beethoven-qa/` with an `ORIGIN` file (repository, tag, commit, tree hash) in every
consuming repository, refreshed only from a tagged release and checked by `vendor-check` before the gate
runs, because the repositories are private and no token may exist in CI or in the image; and a Claude Code
plugin of the same name for sessions (the definition-of-done skills, the `stream` agent, the workflows
`gate-until-green`, `verify-module`, `improve-module`), registered by the image's managed settings as a
`directory` marketplace (`REPO_SPLIT.md` section 3). The full bar applies to Python that may take
dependencies, the three engine repositories; hpcworker's Python 3.6 framework and the TypeScript clients
take the repository half (pre-push gate, required checks, auto-merge, rulesets as code) and their own
language's checks. A function CrossHair cannot run is named under `unproven` with its reason, printed on
every run; a `# crosshair:` comment is refused.

---

## 4. The token-economy standard (always on, for every engine run)

From file 08 Phase 2 and file 05. Goal 3, plus the orchestration half of Goal 5.

1. **Lazy tool loading.** `ENABLE_TOOL_SEARCH` / `mcp-cli` so MCP schemas are fetched on demand, not
   injected up front (the ~55k→~8.7k, or with mcp-cli ~1.4k, fixed-overhead reduction).
2. **Prompt-cache TTLs** via managed settings: `promptCacheTtl: "1h"` for the lead agent,
   `subagentPromptCacheTtl: "5m"` for ephemeral subagents.
3. **Preemptive auto-compaction.** `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=65` **paired with**
   `CLAUDE_CODE_AUTO_COMPACT_WINDOW=1000000` (the override alone is unreliable in headless `-p`).
4. **Dual-hook state preservation.** `PreCompact` serializes decisions/paths to node-local
   `scratchpad.json`; `SessionStart` (compact matcher) re-injects via
   `hookSpecificOutput.additionalContext`.
5. **Concurrency guardrails** (re-expressed by §17.2.7 as per-account window budgets and per-node sizing;
   greg, 02:30Z: compute is not the scarce thing, the windows are). `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` = allocated CPU cores;
   `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1`; `CLAUDE_CODE_MAX_SUBAGENTS_PER_SESSION=50`.
6. **Quota-window-aware scheduling (D1 decided: no gateway).** Every `claude -p` step draws on the
   student's rolling 5-hour window, the same one their manual sessions use. The orchestrator (Metaflow,
   D3) therefore paces: it records each step's tokens, holds the next step (or a `foreach` branch) when
   the window is nearly spent, and resumes when it rolls, or hands the super-master lease to the next of
   the student's own signed-in accounts (D1d; §17.2.4; BEE-189), hibernating the job rather than retrying
   when every account is spent.
   How Claude Code reports the remaining window is **not yet measured**; BEE-121 measures it first. §14.2
   lists the five places to look, read from Anthropic's own pages on 2026-10-04.
7. **Nested orchestration.** Outer macro-loop (Metaflow/LangGraph) owns state, requeue and routing;
   inner `claude -p` (effort per step, item 9) owns code manipulation; intermediate state lives in script
   variables and Postgres, not the primary context window.
8. **Measure it.** Every run records tokens in/out, cache hit-rate, compaction events, subagent
   counts, wall-clock and (Goal 2) energy — into the ledger (§9) and W&B.
9. **Effort and model per step (added 2026-10-04 from the playbook, §15.3).** Implementation steps run
   at `--model sonnet` with `CLAUDE_CODE_EFFORT_LEVEL=medium`; plan, verify and synthesis steps may raise
   the effort or the model. Nothing runs every inner loop at the highest effort by default.

---

## 5. Re-evaluated build order

The earlier six-phase roadmap is still broadly right as a **critical path**; the goal rewrite adds
the verification, legal-boundary, medical-calibration and publication layers and makes the
credential/billing question (D1) a *gate*, not a footnote. New order:

- **Phase 0 — Ground truth & decisions (gates everything).** D1–D3 decided 2026-10-03 (§7); D4
  follows from D1 (headless, under the student's own sign-in); D5 assumed yes until greg says
  otherwise. Run the one probe
  that is still unmeasured: does headless `claude -p` run from an `sbatch` job on the student's own
  login (building on the Remote-Control probe already done, job 40496445)? Stand up the deterministic
  substrate (Pixi + Apptainer image with the Python verification stack; since the split, pixi and the
  gate in `beethoven-qa`, the image in `beethoven-agents`, D2). **The verification gate
  (§3 items 2 to 4 and 7) exists from the first commit: it runs before every push as a pre-push hook
  and as the required CI check that alone decides a merge (BEE-110, moved here from G1; greg,
  2026-10-04T02:11Z).** *Depends on nothing; blocks all of 1–7.*
- **Phase 1 — Verification substrate (Goal 1).** The contract-driven library from §3 (the gate that
  runs it already stands from Phase 0).
- **Phase 2 — Orchestration & token economy (Goals 3, 5).** Node-local scratch / SQLite-off-PFS /
  Postgres session store; nested outer/inner loop; the §4 token controls; concurrency caps.
- **Phase 3 — REFORMS reproducibility (Goal 2).** Run ID (Hydra + git SHA + Slurm params), clean-tree
  gate, patient-level splits, bootstrapped CIs (W&B), CodeCarbon, `reforms.json` contract + gate
  runner. Reconciles with the existing REFORMS checklist.
- **Phase 4 — Compliance boundaries (Goal 4).** `claude-guard.sh` PreToolUse hook, hardened
  `managed-settings.json`, Phase A/B separation *as governance* (authorized-targets-only, air-gap),
  subscription-only credential compliance (no key, no token, no gateway anywhere in a job). (Scope
  per §2 C4.)
- **Phase 5 — Domain calibration (Goal 6).** DICOM→HU (`RescaleSlope`/`Intercept`), MONAI MetaTensor
  spatial integrity, patient/study-level partitioning (shared with REFORMS Modules 6 & 8).
- **Phase 6 — Dissemination (Goal 7).** OpenLineage events, RO-Crate origin records, LaTeX macro
  injection from W&B/CodeCarbon, Zenodo DOIs, HF model cards — behind a **human Publish gate**.
- **Phase 7 — Research UI (extension).** The engine's read-only Runs/REFORMS view + Publish click in
  the extension, kept separate from the launcher's panel.
- **Cross-cutting — Measurement & report (meta).** The ledger (§9) and the reproducible-report
  scaffold run from Phase 0 onward and measure the build itself.
- **The first run (last, as greg asked; §16).** The spine study: vertebral body detection on real
  fluoroscopy under domain shift, measured end to end as counting exactness, on corpora already on the
  grid. §16.5's acceptance criteria are the gates it adds to Phases 0 to 7.

Phases 1–6 can proceed in parallel once Phase 0 and the substrate are done; 2 is the longest pole.

---

## 6. Mapping: 7 goals → Linear projects → repos

| Linear project | Goal | Primary repo(s) |
|---|---|---|
| P0 — Foundations & Open Decisions | — | hpcworker (substrate); since the split `beethoven-qa` (pixi, the gate, the repository rules) and `beethoven-agents` (the image) |
| G1 — Formally Verified Contract-Driven Code | 1 | `beethoven-qa` |
| G2 — REFORMS Reproducibility | 2 | `beethoven-research` + hpcworker (Run ID, gate runner) |
| G3 — Token Economy & Context Control | 3 | `beethoven-agents` (pacing, managed settings) + hpcworker (job template) |
| G4 — Legal & Security Compliance Boundaries | 4 | `beethoven-agents` (guard hook, managed settings) + hpcworker |
| G5 — Storage, Crash Resilience & Orchestration | 5 | `beethoven-agents` (accounts, lease, registry, bus; §17) + hpcworker |
| G6 — Medical Data Calibration & Tensor Integrity | 6 | `beethoven-research` |
| G7 — Automated Dissemination & Publication | 7 | `beethoven-research` + beethoven-extension (Publish UI) |
| M — Process Measurement & Research Report | meta | this ledger + report scaffold |

The new repo `OpenSpineConsortium/beethoven-research` exists since 2026-10-03T23:54Z (greg created
it by hand; the Claude GitHub App cannot create repositories in the organisation, 403 at 23:21Z) and
is in the project's repository list; its skeleton has its own thread ("Lay down the engine repo
skeleton"). G1/G2/G6/G7 issues drop their `repo:tbd` note as they are picked up.

Split 2026-10-04 (greg, 04:52Z; `REPO_SPLIT.md`, the "Three-repo separation" thread): `beethoven-qa`
created by greg at 13:24Z (its PR #1 pushed by that thread), `beethoven-agents` next (staged with the
account-switching work; waits on his five steps), `beethoven-research` kept for the research pipeline
(his card, 13:19Z) and slimmed by pull requests only after the other two carry the moved content on
`main`, each push announced to its writing threads first. Linear after the split: G1 links to qa; G3, G5,
BEE-185 to 192 and the guard issues BEE-123 and BEE-124 to agents; G2, G6 and G7 to research; P0 issues
for each repository creation (greg's: BEE-193 qa, done 13:24Z; BEE-194 agents), the plugin's first release
(tag `v1.0.0`, BEE-195) and each consumer's switch to the vendored copy (BEE-196 agents, BEE-197 research,
which also slims it).

Added 2026-10-03 (evening), see §11: F1 Claude Desktop extension (`P-BEE-11`, repo
`beethoven-desktop`), F2 Command center / project graph / peeking Claude (`P-BEE-12`, hpcworker +
extension), R Imaging data migration & catalog (`P-BEE-13`, hpcworker), O Outreach (`P-BEE-14`, no repo).

---

## 7. Open decisions for greg (the forks that gate work)

- **D1 — Credential & billing model for the engine. DECIDED by greg, 2026-10-03T23:09Z: the
  student's own subscription, no pooled keys.** My recommendation (commercial keys via a LiteLLM
  gateway, open-weights as fallback) is withdrawn. greg's grounds: since Anthropic's 2026-06-15
  update, `claude -p` and the Claude Agent SDK draw from the flat-rate plan (Max 20x); the
  programmatic credit pool is on hold; console keys remain pay-as-you-go and cannot tap the plan;
  automated runs share the same rolling 5-hour window as manual sessions. Consequences: the engine
  shares the launcher's credential posture (§1); G3 is pacing within the window (§4.6, BEE-121), not
  routing; G4's compliance check is "subscription-only, no key anywhere in a job" (BEE-127).
  **Usage credits: decided by greg 2026-10-04T01:12Z, never** (§2 C7). A hard exclusion with the same
  rank as the other non-negotiables; §14.2 item 6's first reading ("off by default, the student's
  call", 00:35Z) is withdrawn, and the engine's pacing has to work without them. **D1b (2026-10-04, §15.1):** the playbook's setup-token
  for batch against the no-token rule; options A, B, C there. **Decided by greg 2026-10-04T01:10Z: C.** The
  no-token rule stays; BEE-101 measures the refresh on 2.1.28x; the token file is taken only if that
  measurement fails, and only with the text changes listed. **D1c (§15.2):** patient
  data and a consumer plan: greg confirms the account's data-sharing setting and the rule that Claude
  Code never reads raw patient data. *Unblocks G3, G5.*
- **D1d — What happens when a window is spent. DECIDED by greg 2026-10-04T02:18Z and widened at 02:30Z
  (§17): several of his own accounts run at once, one holding the super-master lease, which moves to the
  next account as the holder nears its limit, from the engine's saved state; when every account is
  spent, hibernate.** greg's proposal (01:12Z), in his words: "if the quota runs out then you
  can work in a utility like claude swap to switch accounts so its only ever one account at a time but
  the state saving of the top level essentially makes it pick up where the last account left off."
  Checked before it became a rule, against the sources read at 01:20Z:
  - Anthropic's Consumer Terms of Service (effective 2025-10-08), section 2: "You may not share your
    Account login information, Anthropic API key, or Account credentials with anyone else. You also
    may not make your Account available to anyone else." Section 3 forbids access "through automated
    or non-human means, whether through a bot, script, or otherwise" except via an API key "or where
    we otherwise explicitly permit it" (Claude Code's own `-p` mode is Anthropic's documented feature;
    a third-party utility that switches sign-ins is not explicitly permitted anywhere read here). The
    terms have no clause in the words "one account per person" or "circumventing usage limits".
  - Anthropic's Usage Policy (effective 2025-09-15) forbids coordinating "malicious activity across
    multiple accounts to avoid detection or circumvent product guardrails" and circumventing a ban
    "through the use of a different account"; it does not name usage limits.
  - The help articles "About Claude Max usage" and "About Claude's Pro plan usage": the limit resets
    every five hours (a "session"); "if you exceed 50 sessions per month, we may limit your access to
    Claude"; nothing on several accounts. Second-hand reports of accounts closed for using several
    accounts against the rate limit exist (a Hacker News thread and several blogs found by search) and
    could not be read from a primary page here; they are reports, not the rule.
  - This project's own rules as they stood before 02:18Z: §2 C6 ("never for evading detection or
    limits"), the playbook's compliance envelope adopted as BEE-127's wording ("no limit evasion: one
    account per user, no account rotation, no pooled tokens"), and "One person, one account" in both
    launcher repositories' `CLAUDE.md`.
  The two readings of greg's sentence are different cases:
  1. **One person, several accounts, switched when one is spent.** This is what greg meant. The card of
     01:27Z told him that C6 and BEE-127 called it limit evasion and that it would stay unbuilt unless
     he changed that rule knowingly; he chose it at 02:18Z, so the rule is changed: C6 is narrowed
     (§2), BEE-127's wording is amended, and `PROJECT_INSTRUCTIONS.md` version 7 carries the new
     sentence. What is not softened, and stays on record for BEE-177 and the paper: Anthropic's texts
     as read neither permit nor forbid one person's several accounts by name; the Usage Policy's clause
     on several accounts used to circumvent product guardrails is the nearest to it; the reports of
     closed accounts are second-hand and unread here; the accounts at risk are greg's own and the
     choice was his, made knowingly. The launcher is not changed: "One person, one account" in the two
     launcher repositories' `CLAUDE.md` is the launcher's rule, its worker runs one `claude_config_dir`,
     and greg decides whether that sentence stays.
  2. **Several students, each on their own plan, one run.** Also allowed, as the D1 model it always was.
     Each student signs in themselves on a compute node; nobody's account is made available to anyone
     else (terms, section 2); the engine's run state (Postgres, `STATUS.md`, `windows.log`, the RO-Crate
     record) is the lab's and lives on the lab volume, so the next step of a run can be picked up by the
     next student's own worker when the first student's window is spent: one account active per run at
     a time, by that student's own opt-in, on their quota. A hand-off also moves the run under that
     student's data-sharing setting (D1c) and their AUP responsibility (BEE-177), so the opt-in is
     explicit and recorded.
  In both cases what is never handed over to another person's account is a Claude Code session: the
  transcript lives in the sign-in directory, is never copied and is never resumed under another person's
  account; between one person's own accounts the spent session may continue from its transcript by its
  absolute path (§17.2.9, after probe M13); the hand-off is at the step boundary, from the engine's own
  records (this is what "state saving of the top level" has to mean), and the transcript adds the
  conversation around that state, never replaces it. Built in G5 as
  BEE-185 to BEE-190 (§17.5), with these constraints as the definition of done, read with §17.2 where §17
  widens them (several accounts at once; one lease):
  - Each account is signed in by its owner, with `claude auth login` on a compute node, into its own
    directory. The engine keeps a list of directory paths with a label each, and nothing else: it
    never reads inside any of them, never copies anything between them, never runs `claude auth
    logout` (the credential rule of §2, unchanged).
  - One super-master lease at a time (§17.2.4); since 02:30Z several of the person's accounts run at
    once (§17), and the per-account concurrency caps of BEE-150 stand, re-expressed by §17.2.7.
  - The switch happens at a turn or step boundary: before the limit at the threshold (§17.2.4 trigger a)
    once usage is readable, on the limit itself (b), or at wall time or a lost lease (c, d). The holder's
    own Claude Code session does not end for it: a master hibernates until its reset; a `-p` step ends as
    it would anyway and its successor step starts under the next account's directory through
    `CLAUDE_CONFIG_DIR`. A transcript stays in the directory that made it and is never copied (§15.6);
    since 03:3xZ the next account may continue the spent session from that file by its absolute path with
    `--fork-session`, the file bound read-only, the continuation written under the new account (§17.2.9,
    probe M13); `--resume <id>` and `--continue` never cross directories.
  - What carries over is the engine's own state (the Metaflow run, the Postgres session store of G5-2,
    `STATUS.md`, the progress log, git): greg's "state saving of the top level".
  - Order: the next account not known to be spent; when all are, hibernate until the earliest known
    reset (§4.6, §14.2 item 2), never usage credits (C7), on any account.
  - Every switch is written down: `windows.log` gains an `account` field (the label, never an email or
    anything read from the directory) and the per-run compute and quota record (BEE-179) lists the
    accounts a run used, so the paper says so.
  - greg's "claude swap": whether an existing utility does this or a few lines of ours do is the
    issue's first question; nothing is fetched or run from outside the image (no remote code), and an
    external utility, if any, is pinned in `pixi.lock` like everything else.
  The default when every account is spent is unchanged: hibernate until the earliest reset (§4.6,
  §14.2 item 2).
- **D2 — Repo topology. DECIDED 2026-10-03, refined 2026-10-04 (greg, 04:52Z; his card 13:19Z): the
  engine is three repositories**: `beethoven-qa` (Goal 1 and the repository rules every repository
  carries; consumed as a pinned copy per repository and as a Claude Code plugin, baked into the grid
  image), `beethoven-agents` (Goals 3, 4 and 5 and §17: the Apptainer image, managed settings and guard,
  accounts and the hand-off including the account switching, the Metaflow loop around `claude -p`,
  pacing, registry) and `beethoven-research` (Goals 2, 6 and 7 and the studies; kept, not renamed), with
  qa <- agents <- research the only direction of dependence: qa uses nothing of ours, agents uses qa and
  never imports the pipeline, research uses both, and a change that needs an upward import is in the
  wrong repository (`REPO_SPLIT.md`). hpcworker and the extension stay the launcher; the client contract
  (`docs/V11_CONTRACT.md`) is untouched. greg created `beethoven-research` by hand at 2026-10-03T23:54Z
  (the GitHub App has no right to create repositories, 403) and `beethoven-qa` at 13:24Z;
  `beethoven-agents` follows his same five steps (README only, auto-merge on, the RULESETS_TOKEN as an
  organisation secret shared with the new repositories, tell the thread, merge its PR #1 by hand once).
  The base image is built in agents; a study image layers the research environment on it
  (`Bootstrap: localimage`), so one substrate digest is shared and a study's digest names its additions.
- **D3 — Workflow engine. DECIDED: Metaflow + `outerbounds/metaflow-slurm`.** The plain-sbatch
  adapter is still the first step underneath it; RO-Crate (G7) gets a custom emitter, not nf-prov.
- **D4 — RC worker vs headless `claude -p`.** The launcher is interactive Remote Control; the engine
  needs headless `claude -p --effort ultracode`. *Recommended:* both, as the two systems; confirm the
  engine is headless. *Affects Phase 0 probe, G5.*
- **D5 — Approval/human gates.** *Recommended:* a human **Publish** click before any Zenodo DOI / HF
  push, and human sign-off before Phase B boundary is ever crossed (off-grid, out of scope here).
  Unchanged by the PR convention of §3 item 7 (merges are decided by checks alone, 2026-10-04): the
  Publish click is for the outward, irreversible step only; greg says if that should go too.
- **D9 — The first study's twelve questions (§16.6; Linear project S).** From the spine folder; greg's
  alone. None blocks the ecosystem build; questions 1, 4 and 6 block the first run.

---

## 8. How I'll bootstrap this, end to end

1. **Lock the substrate (Phase 0).** `pixi init` each engine repository, qa first (D2); author the Apptainer `.def` with
   Node + Claude Code + the Python verification stack; prove `claude -p` from `sbatch` on the grid.
   Two placement facts for the skeleton: (a) warrior's banner bans `python3`, `node`, `rsync` and
   `md5sum` on the login node "on sight" (`hpcworker/docs/V11_CONTRACT.md`, `docs/guides/LAB_LEAD.md`),
   so Metaflow's own Python process runs inside a compute-node job (an orchestrator job that submits
   steps through metaflow-slurm and chains its own successor with `afterany`, as the worker job already
   does) or on the student's machine over ssh, never on the login node; the only thing of ours the login
   node runs is `bash` and one `sbatch` / `squeue` / `scancel` per action. (b) Whatever runs on the login
   node stays bash 4.2 and python-free; everything inside the Apptainer image may be current Python under
   the Pixi lockfile. The engine's `CLAUDE_CONFIG_DIR` is the profile's `claude_config_dir`, bound
   read-write for Claude Code's own writes and never read or written by ours (§15.6), and no credential
   variable exists in a job's environment (D1). Whether `sbatch` works from
   a compute node is assumed from the worker's successor chaining and should be measured once.
2. **Stand up the verification library (G1, `beethoven-qa`)** behind the gate Phase 0 already enforces (pre-push hook
   and required check, §3 item 7), so every later module is born
   contract-checked.
3. **Build the orchestration spine (G5/G3):** node-local scratch staging + Postgres session store +
   the nested outer/inner loop + the token controls — the thing that keeps multi-hour runs alive.
4. **Layer REFORMS (G2) and domain calibration (G6)** onto the spine as pipeline steps with gates.
5. **Wire compliance (G4)** as always-on guard hooks + managed settings from the first real run.
6. **Add dissemination (G7)** last, behind the human Publish gate.
7. **Surface it in the extension (Phase 7)** as a read-only research view.
8. **Measure throughout (M):** every thread appends to the ledger; the report scaffold fills from it.

Each step is a Linear issue with acceptance criteria tied to §3/§4 and the source doc. The ledger
(§9) records wall-time, bugs fixed, and starting materials so the whole build is reproducible.

---

## 9. Measurement & reproducibility (the ledger)

A standing, append-only ledger lives at `/mnt/project-files/ledger/`. `README.md` defines the format
(a stranger can follow it); `LEDGER.md` is the running log, seeded with the starting materials
(repo SHAs, all 17 notebook files + mtimes, the topic text, project-creation and message times) and
this thread's own entries. Every later thread appends one row per unit of work: what, when, wall-time,
bugs fixed, inputs, outputs, and the commit/PR if any. Goal 2's run-level telemetry (tokens, energy,
CIs) feeds the same ledger so the research report can be reconstructed exactly.

Added 2026-10-04 (greg's methods-paper framing, §12): beside `LEDGER.md` the folder carries
`INTERVENTIONS.md` (every human intervention, written when it happens: when, who, what the agent was
doing, why the human stepped in, what changed, outcome; plus failures, dead ends and withdrawn
results) and `BOUNDARY.md` (what each agent could and could not touch, per phase: this cloud
session, the grid worker, the engine). Engine rows also carry the per-run compute and quota record
(Slurm job ids, partition and QoS, requested and used wall time, GPU-hours, preemptions and
requeues, queue wait, window spend; BEE-179). The `verified` column gains the value `independent`:
checked by a different route than the one that produced the result. The headline numbers of the
paper are the intervention count per unit of work and the share of results verified independently.

---

## 10. What changed from the earlier artifacts

- **Still holds:** the six-phase critical path; the REFORMS 32-item mapping and its 20-code / 12-declared
  split; "RC worker is the launcher, the engine is new on top"; node-local scratch; human-Publish gate.
- **Changed by the goal rewrite:**
  - Billing default was proposed to flip from "student's own subscription, no pooled keys" to
    commercial keys via LiteLLM (D1). **greg rejected the flip on 2026-10-03T23:09Z**; the earlier
    roadmap default stands for the engine as well, and the engine shares the launcher's credential
    posture. The two-systems separation stays, for the loop (interactive vs headless), not for billing.
  - Goal 1's **formal-verification stack** (icontract/CrossHair/Z3/BAML/SpecPylot) is now a
    first-class phase and the definition-of-done, not a deferred "verification extra".
  - Goal 4's **legal/security boundaries** are now an explicit workstream — scoped to **governance and
    guardrails only**; Phase B exploit/PoC work is off-grid and out of scope here.
  - Goal 6 **medical calibration** (HU/MONAI) and Goal 7 **publication engine** are now explicit
    workstreams rather than "phase 4 paper/archive".
  - The engine goes into its **own repositories** (D2: `beethoven-research` on 2026-10-03, split on
    2026-10-04 into `beethoven-qa`, `beethoven-agents` and the kept `beethoven-research`), where the
    earlier roadmap left it open.

---

## 11. New directions added 2026-10-03 (evening), from greg's second message

Each has a Linear project with issues and acceptance criteria (`LINEAR_BREAKDOWN.md`, "Added
2026-10-03 (evening)").

- **F1 — Claude Desktop extension with native ssh** (`P-BEE-11`; repo `beethoven-desktop`). **greg,
  2026-10-04T02:30Z: the plugin works seamlessly with the Claude Code Desktop app, uses Claude Code's own
  SSH sessions where they fit, and shares the proven pieces of the Chrome extension and `beethoven-vscode`;
  the desktop thread builds it.** Where they fit, reconciled 03:1xZ with the desktop thread's finding
  (§17.1 D1 to D6): Desktop's SSH installs Claude Code's native binary on the SSH host, so the login node
  is never the target, and on Wayne State no compute node is either (CentOS 7, glibc 2.17, the reason the
  lab image exists), so Desktop's own SSH is not the worker's transport here, closed rather than
  conditional, and the plugin keeps its own ssh (desktop PR #2, 02:56Z); the `ProxyJump` shape of the
  first reading stays measurable only on a site whose nodes run the binary (M7, M8), and even there a
  Desktop session is a window beside the worker, never the master (D4a). The shared pieces exclude the VS
  Code edition's API-key overflow (§2 C8, BEE-191). A
  complement to the browser extension, which cannot open an ssh terminal or view files. The same
  non-negotiables as the browser extension apply unchanged: never a Claude credential; the grid
  password and one-time code go only into the ssh session and are never stored; no remote code; the
  Beethoven name and the trademark sentence. **greg, 2026-10-04T01:12Z: the plugin is written
  regardless** of what Claude Code Desktop (beta, §14.4) already gives a student; that measurement
  shapes what the plugin adds, not whether it is built. It is being built now in its own thread
  ("Build the Claude Desktop ssh plugin", started by the coordinator from
  `DESKTOP_EXTENSION_SPIKE.md` and `P-BEE-11`); this plan keeps F1's issues and decisions. The spike
  (BEE-153) still verifies against the current documentation what a Claude Desktop extension may run
  on the student's machine, and anything unverified is marked so. Design spike:
  `DESKTOP_EXTENSION_SPIKE.md`.
- **F2 — Command center, project graph, peeking Claude** (`P-BEE-12`). Server side: a
  `runs/index.json` beside each `status.json` and a `graph.json` of the Metaflow run (a contract
  change, in both repositories together). Client side: a Jobs view and an interactive dependency graph
  read from files at the 60 s floor, never a faster `squeue`. The peeking Claude is a read-only
  headless `claude -p` job under the student's own sign-in that writes `status/<step>.md`; it spends
  the same quota, so it runs per step end or hourly and the window scheduler may skip it.
- **Several Claude sessions per student** (BEE-150..152 under G5): a Metaflow `foreach` becomes one
  sbatch job per branch, each a satellite (§17.2.3) under the account the super-master assigns; branches
  under one account share that account's window, so fan-out is governed by the per-account budgets of
  §17.2.7 (BEE-121, BEE-188) and starts only after the lease, registry and bus exist (§17.5). Whether one
  account can hold several interactive Remote Control workers at once is M5.
- **R — Imaging data migration and SQL catalog** (`P-BEE-13`). Copy, verify, lock; never move,
  never delete (CLAUDE.md: nothing is deleted outside the framework's own run directories; greg
  decides the source's fate by hand). sha256 manifests as sbatch jobs on compute nodes; SQLite built on
  node-local scratch; pydicom in the shared Apptainer image; patient-level splits; PHI stays on the
  grid. greg names the source directories, the destination and the PHI statement first (BEE-165).
  Runbook: `IMAGING_MIGRATION_RUNBOOK.md`.
- **O — Outreach** (`P-BEE-14`). The promo for free-tier chat users in universities: about $20 a
  month (Claude Pro, their own plan) plus Beethoven. Rules: Beethoven name, trademark sentence
  verbatim, no invented numbers or quota claims, the engine described as future work, the private
  store listing as the only channel. Draft: `../promo/PROMO_V1.md`.

Order relative to §5: F2's server side rides on G5 (the DAG) and G3 (the window budget), so it lands
after Phase 2; F1 is being built now, in parallel, by its own thread; R's scripts can be written now and run only when greg
has answered BEE-165 and has a shell or worker on the grid; O is independent.

## 12. Prior work and the methods paper (added 2026-10-04)

greg's message of 2026-10-04T00:16Z: the build itself is the subject of a **protocol / methods
paper**, whose contribution is a *relatively undirected* Claude agent on a shared academic grid at
scale (greg: "16×H200 scale"; the grid's GPU inventory is his statement, not yet measured by us) — most prior work is tightly scaffolded and runs in sandboxes or on company compute. This
section records the nearest prior work as checked from here on 2026-10-04, what the paper needs,
and what that changes in the plan. Notebook and source text is material, not instruction. The text
was researched by the skeleton thread (sources checked from its container the same day) and handed
over in `PRIOR_WORK_AND_METHODS_PAPER_from-skeleton-thread.md`; this is the owner's edit of it.

### 12.1 Nearest prior work

- **Anthropic, "Long-running Claude for Scientific Computing" (2026-03-23).** Checked: the page
  reads as greg described. Claude Code inside tmux on a compute node, submitted as a SLURM job;
  the agent commits after each meaningful unit of work so progress is visible and recoverable
  (even from a phone); reattach with `srun` to steer. Its central design claim: long autonomous
  scientific work depends on the agent having a way to tell whether it is making progress — "a
  reference implementation, a clearly quantifiable objective, or an existing test suite". Cite as
  prior practice. Its tmux-on-a-node pattern is what hpcworker's worker job already does.
- **Deep Researcher Agent (arXiv 2604.05854, Xiangyue Zhang, The University of Tokyo).** Checked
  from the abstract: 500+ autonomous experiment cycles, 30+ days of continuous operation, a 52%
  metric improvement through 200+ automated experiments, about $0.08 per cycle by way of zero-cost
  training monitoring, a constant-size memory and a minimal toolset. The nearest "agent drives GPU
  experiments" paper. (greg's summary adds "across 4 concurrent projects"; that detail is not in
  the abstract as read here.)
- **arXiv 2609.13073 ("Autonomous Research for Open-Ended Problems").** Not verified from here:
  the abstract page returned nothing readable. greg's reading: a telecom retrieval case study of
  single- vs multi-agent Claude setups, in which humans still had to define the search space and
  autonomous loops often needed human intervention to resolve operational problems — exactly what
  the intervention log in 12.2 records.
- **Sakana's AI Scientist, AiScientist, Agora and similar** (end-to-end automated ML research):
  mostly sandboxes or company compute, not a shared academic grid. No links were given; the
  related-work section (M-7) cites them from their own papers.

### 12.2 What makes it publishable, and where the plan already has it

| Paper need (greg's source) | Already in the plan | Gap, now an issue |
|---|---|---|
| Full record: prompts and instruction files, agent logs, git history, job scripts, GPU time and spend | the ledger (§9); REFORMS Run ID + clean-tree gate (G2); RO-Crate (G7) | per-run compute and quota record (**G5-8**, BEE-179; Linear refused the M-6 label pair) |
| Honest accounting: how often a human intervened and why, what failed, dead ends, independent verification | the ledger's `bugs_fixed` and `verified` columns | an intervention log with its own format, written when it happens (**M-5**, BEE-174; format in `ledger/README.md`, entries in `ledger/INTERVENTIONS.md`) |
| Grid specifics: quotas, preemption, fair sharing, what the agent could and could not touch | `CLAUDE.md` non-negotiables and grid etiquette, G4 guard hook + managed settings, the volume ACL | the paper's environment section (**M-7**, BEE-176); the AUP check (**M-8**, BEE-177); the boundary record `ledger/BOUNDARY.md` (what each agent could and could not touch, per phase) |
| Reproducibility: can someone rerun it on their cluster | Pixi lock + Apptainer (P0, PR #1 of `beethoven-research`), hpcworker's site profiles | nothing new; the skeleton is the first artefact |
| Housekeeping: the cluster's acceptable-use policy on autonomous agents; disclose AI use, no AI author | — | greg's hand step (**M-8**, BEE-177, assigned to greg) |

### 12.3 What it changes in the engine

- **A progress signal is a requirement of every long-running step** (**G5-7**, BEE-178, new, from the
  Anthropic guide). Each `claude -p` step declares how it can tell it is making progress — a
  quantifiable objective, a reference implementation or a test suite — and commits after each unit
  of work. The peeking Claude (BEE-163) and the run index (BEE-159) read that signal; a step that
  declares none is not scheduled.
- **Human interventions are first-class data**, logged the moment they happen (M-5), never
  reconstructed afterwards (the seed entries in `INTERVENTIONS.md` for 2026-10-03 are the one
  exception and say so); the paper's honesty rests on that log.
- The record the paper needs (prompts, instruction files, agent logs, job scripts, git history)
  is kept in full; nothing is trimmed for tidiness. `beethoven-research/CLAUDE.md` says so.

### 12.4 Venues

The workshop greg's source names, **"AI Scientists – Tools, Co-authors, or Founders?" at ICML 2026**
(2026-07-11, submissions closed 2026-05-07), has **already passed** as of today, 2026-10-04. Its
themes (autonomous discovery loops with human oversight, human–AI co-authorship and
reproducibility, governance and verification) are the right fit, so the target is its next edition
or an equivalent 2027-cycle workshop; the alternatives are a methods-focused journal or a
software/protocol track if the harness is released. Each venue's current AI-use policy is checked
before submitting (M-7). Which venue, and the field framing, are greg's call once the engine has
produced a result — his source's own closing question ("your field and what the agent actually
produced").

---

## 13. Amendment log

- 2026-10-03T23:09Z — greg decided D1 (own subscription, no pooled keys; my recommendation
  withdrawn), D2 (new repo `beethoven-research`), D3 (Metaflow + metaflow-slurm) and added the
  directions in §11. Sections 1, 2, 4.6, 5, 6, 7 and 10 were amended in place to match; §10 records
  what the earlier text proposed.
- 2026-10-04T00:28Z — greg's prior-work message (00:16Z, skeleton thread): the build is framed as a
  protocol / methods paper. §12 added (text researched by the skeleton thread, handed over and edited
  here); §9 extended with the intervention log, the boundary record, the compute and quota record and
  `independent` verification; `ledger/README.md`, `INTERVENTIONS.md` and `BOUNDARY.md` written;
  Linear BEE-174, 176, 177 (M-5/7/8), 178, 179 (G5-7/8) created by the skeleton thread and kept.
  `PROJECT_INSTRUCTIONS.md` version 2 carries the progress-signal and intervention rules.
- 2026-10-04T00:35Z — greg's five Anthropic links (00:20Z, skeleton thread): §14 added at the end as
  asked; §4.6 and §7 D1 point at it; BEE-121 re-pointed (task budgets and usage analytics withdrawn as
  leads; `/usage`, wait-for-reset, `--max-budget-usd`, OpenTelemetry, reset-time messages added).
- 2026-10-04T00:44Z — greg's Drive folder "claude-artefacts" (00:27Z): §15 added (playbook adopted,
  refused, measured); §4 item 9; §1 and §4.7 reworded; D1b and D1c in §7; Linear comments listed in
  §15.5. The "spine" folder follows as §16 when its reading completes.
- 2026-10-04T01:10Z — greg decided D1b: C (decide on evidence). §7 and §15.1 record it.
- 2026-10-04T01:23Z — greg (01:12Z): usage credits are never used, a hard exclusion of the same rank as the
  other non-negotiables (§2 C7, §7 D1, §14.2 item 6; `PROJECT_INSTRUCTIONS.md` version 4); the Claude
  Desktop plugin is written regardless of what Claude Code Desktop gives (§11, §14.4; built in the
  thread "Build the Claude Desktop ssh plugin"); his account-switching proposal is recorded as D1d with
  the terms check (decided at 02:18Z, below). BEE-121, 127, 153 and 134 commented.
- 2026-10-04T01:31Z — greg's Drive folder "spine" (00:27Z) read: §16 added (the first study, its data, compute,
  reporting and the acceptance criteria it gives each engine phase; D9 in §7; the first run in §5); the
  playbook's second reading added as §15.6 (`cleanupPeriodDays` struck from §15.3, the read-only sign-in
  directory seam, the quota ladder, `windows.log`, the 30 experiments). `SPINE_FIRST_STUDY.md` and
  `TOKEN_ECONOMY_PLAYBOOK.md` filed beside this plan. Linear project S with four issues; criteria posted on
  the phase projects; BEE-101, 121, 124, 180 commented.
- 2026-10-04T01:39Z — correction from the skeleton thread (01:40Z), verified against hpcworker: the sign-in directory
  is bound read-write, never read-only (§1, §2 C2, §15.6; `PROJECT_INSTRUCTIONS.md` version 5; BEE-101).
- 2026-10-04T02:14Z — greg (02:11Z, skeleton thread): no human gates a merge; pull requests open ready for
  review, auto-merge is enabled by a workflow and the required checks alone decide; the contract and
  concolic gate runs before every push and is a Phase 0 deliverable. §3 item 7, §5 Phase 0 and 1, §8
  step 2, D5 note; BEE-110 moved to P0 (Urgent); `PROJECT_INSTRUCTIONS.md` version 6.
- 2026-10-04T02:3xZ — greg answered the D1d card (02:18Z): his own several accounts, one active at a time,
  the run carried over from the engine's saved state. §2 C6 narrowed, §7 D1d decided with the record of
  the terms check kept, §4.6 item 6 and §15.6 (`windows.log` account label); BEE-185 opened in G5 with
  the definition of done; BEE-121, 127, 134 and 177 commented; `PROJECT_INSTRUCTIONS.md` version 7. The
  launcher's "One person, one account" is left to greg.
- 2026-10-04T02:5xZ — greg (02:30Z, this thread): several of his own accounts at once, agent teams and
  cross-session messaging in the spec, one master per account, one super-master lease switched claude-swap
  style, sessions as Slurm jobs, teams of teams, no orphans, the desktop plugin seamless with Claude Code
  Desktop. §17 added (requirements, the four pages' facts, the design, the rules changed, nine probes);
  §2 C6, §4 items 5 and 6, §7 D1d, §11 F1, §14.2 item 7 amended; BEE-185 rewritten, BEE-186 to 190 opened;
  `PROJECT_INSTRUCTIONS.md` version 7. The desktop thread has R1; the skeleton thread the engine's CLAUDE.md.
- 2026-10-04T03:0xZ — greg (02:37Z, skeleton thread): the worktrees and workflows pages for bootstrapping
  and the parallel parts. §17.6 added (the pages' facts, the build's worktree per stream and four saved
  workflow scripts, the engine's three mechanisms, two rules: worktree hygiene is ours, a workflow run
  never crosses accounts), probes M10 and M11, BEE-192 in P0, comments on BEE-190, 189 and 110;
  `PROJECT_INSTRUCTIONS.md` version 8.
- 2026-10-04T03:1xZ — three refuters read §17 against the agent-teams, cross-session and Desktop pages and
  claude-swap's README: A2, A3, X2, X6, D2, C2, C3 reworded (inference marked as inference; the socket
  directory is not fixed; socket path and token reach only the session's own hooks); D4a added (agent
  teams and `-p` are not in Desktop); 17.2.2 gains the unattended permission configuration (M12) and the
  successor's fresh team; 17.2.3 satellites start with `crossSessionInbound: accept`; 17.2.4 run-level
  tasks; 17.2.5 the `SessionStart` hand-over, the repeat and rate rules, Remote Control's direction; 17.2.6
  invariants 1 and 2; 17.3 the 7x qualifier; M3, M7, M8. The desktop thread's finding (02:56Z) closes
  Desktop's own SSH as the worker's transport on Wayne State (D6, §11 F1); BEE-191's API-key overflow in the
  VS Code edition recorded as §2 C8.
- 2026-10-04T03:2xZ — two critiques (consistency with the launcher as built and with the sections §17
  amends; the nine requirements against greg's words): §14.2 item 7 `hold` → `accept` (the reference was
  wrongly "§15.6 item 7"); 17.2.5 on one node is one container, two jobs do not share a socket; registry
  rows from the moment of submission (queued satellites were strandable); hand-off trigger (b) for a
  pseudo-terminal master, (c) at the launcher's TERM@120, only (c) and (d) buildable before M4; the roster
  without reading `config.json`; `teammateMode` pinned to `in-process`; G5-9's single submitter and 4-job
  cap re-expressed; §7 D1d's definition of done, §1's trust row, §11's BEE-150 paragraph amended; 17.2.1
  link direction; M1 names both master forms; M4 assigned to BEE-188; the R1, R8, R9 narrowings said
  beside the requirements. greg (03:09Z): four account-switcher sources read and written as S1 to S3 with
  the verdict (Cloak's shape is ours; claude-swap's slot copying stays out); the ACCOUNTS.md wording sent
  to the skeleton thread.
- 2026-10-04T03:3xZ — greg (03:23Z, skeleton thread): claude-swap's `--share-history` as a way to hand a
  running session near its limit to a fresh account. Settled with the skeleton thread (its reply 03:27Z)
  as 17.2.9: the next account continues the spent session from its transcript by absolute path with
  `--fork-session`, the path from the session's own `SessionStart` hook, the file bound read-only, nothing
  copied, the credential untouched, the engine's saved state still the record of truth; probe M13 before
  it is built; §7 D1d, 17.2.4, 17.3, 17.5, §15.6, S1 and the verdict amended; `PROJECT_INSTRUCTIONS.md`
  version 9. Then, from the skeleton thread's 03:30Z note, 17.2.9's bind target is its `/handoff/<id>.jsonl:ro`
  and the hook route is named as how a forked master's id is learned; M13 gains the version question. From
  the desktop thread's 02:54Z note (read late): M7's hop is marked measured (2026-09-28) with check 14 as
  the remainder, M8 moot with a key, D6 matched, and 17.2.10 records the client view and the `status.json`
  contract change (`account`, `role`, `parent`, `lease`).
- 2026-10-04T06:4xZ — the switching thread's `ACCOUNT_SWITCH_AMENDMENT.md` (06:38Z; `beethoven-research`
  PR #3, from greg's 04:12Z ask to implement his "Claude CLI State Management" guide) folded: 17.2.1 the
  `bee` command set, the list at `~/.beethoven/engine/accounts.json`; 17.2.4 and 17.2.9 the guide's
  six-section hand-off file as the first carrier, the transcript second; 17.2.8 the status line's
  `rate_limits` fields for interactive sessions (the switching thread's reading, not yet checked against
  the page here) and `StopFailure` `rate_limit` for `-p` (hooks page, checked); 17.2.9 (1) built as
  `state/session.json`, (3) the fork's path check; 17.3 the guard's refusal of `claude auth login` and
  `claude project purge`, `authMethod: "claude.ai"` as the sign-in test, the `/autocompact` rule, the four
  parts of the guide left out; M4 and 17.5 updated; `PROJECT_INSTRUCTIONS.md` version 10 (replaces 9,
  not yet pasted). The repository sections wait for `REPO_SPLIT.md`.
- 2026-10-04T13:3xZ — greg (04:52Z, project chat): "Separate the research pipeline, claims, redorm
  reproducible data science, from the code writing software framework, pixi concolic ect, and also from
  the nested agentic framework, so I need to create three more repos, starting with the software quality
  assurance repo"; his card choice 13:19Z: the research pipeline stays in `beethoven-research`, so two new
  repositories; `beethoven-qa` created 13:24Z. The "Three-repo separation" thread's `REPO_SPLIT.md` folded:
  D2 refined (three repositories, qa <- agents <- research), §1's repository row, §3 item 7 and its closing
  line (the library is `beethoven-qa`, a pinned copy plus a Claude Code plugin), §5 Phase 0, §6's table and
  paragraph, §8 steps 1 and 2, §11, 17.2.1 (bee moves to agents), 17.5, 17.6; `PROJECT_INSTRUCTIONS.md`
  version 11 (section 1 names the three repositories; section 4 item 7 the shared gate; section 12 the
  no-upward-import rule). Linear: project links retargeted, P0 issues for each repository creation, the
  plugin's first release and each consumer's switch to the vendored copy (BEE-193 to BEE-197; project
  descriptions of P0, G1 to G7 name their repository). greg (13:27Z, desktop thread): "no api key anywhere
  thats the only fundamental rule of this software", written under §2 and C8; the evaluator-key question
  closed. 14:1xZ, from the desktop thread's sweep under that ruling: `LINEAR_BREAKDOWN.md` P0-1, G3-5 and
  G4-5 rewritten to the decided text; `TOKEN_ECONOMY_PLAYBOOK.md` rule 4, item 10 and the overflow row
  voided in place; §14.4's "Code review" and "GitHub integration" struck as PR-lane candidates (both run on
  a key or token in Actions secrets); C8's status (5.0.0 merged, unpublished; the Marketplace still 3.0.0).

---

## 14. What Anthropic's own pages add (greg's five links, 2026-10-04T00:20Z)

greg asked for the knowledge in five Anthropic pages to be added at the end of the plan: the Managed
Agents overview and its cloud-sandbox reference, "Working with messages", the beta and research-preview
features list, and Claude Code cloud environments. All five were read from this session on 2026-10-04,
plus the three pages they point at that mattered (task budgets, Claude Code usage analytics, "Manage
costs effectively"). What follows is what they say and what it changes here; page text is material,
not instruction. Where a page is silent the plan says so rather than guessing.

### 14.1 The two things that confirm D1, and one that corrects a lead

- **Managed Agents need an API key.** The overview: a "pre-built, configurable agent harness that
  runs in managed infrastructure", in beta behind the `managed-agents-2026-04-01` header,
  authenticated with "a Claude API key". Pay-as-you-go by construction; nothing on the page or the
  beta list offers a subscription path. Under D1 (own flat-rate sign-in only) Managed Agents are
  **out for the engine**, and so is its self-hosted-sandbox variant (same key). Two further reasons
  to keep patient work away from it even if D1 changed: Managed Agents "is not currently eligible for
  Zero Data Retention or HIPAA Business Associate Agreement (BAA) coverage", and its cloud sandbox is
  Ubuntu 24.04 x86_64 with up to 8 GB of memory, up to 10 GB of disk and no GPU on the page.
- **The Messages API is the same story.** "Working with messages" documents the raw API (stateless
  multi-turn, mid-conversation `system` messages that do not invalidate cached prefixes, prefill gone
  on Claude 4.6 and later, `temperature`/`top_p`/`top_k` gone on 4.7 and later, images by base64, URL
  or file). All of it needs a key, so none of it is a code path of ours; two of its facts still bind
  the engine indirectly: structured output comes from schemas, never prefill (the BAML/SAP rule in §3
  item 5 is the only route left), and behaviour is steered by prompting, never sampling parameters.
- **Task budgets are not a lead for the quota window.** `output_config.task_budget` (beta header
  `task-budgets-2026-03-13`, minimum 20,000 tokens) is an *advisory* token budget for one agentic loop
  whose countdown "is visible only to the model": the response reports nothing about it, and the page
  says it is "not supported on Claude Code or Cowork surfaces". The coordinator's note of 00:25Z named
  it as a lead for BEE-121; it is withdrawn. The same for **"Claude Code usage tracking (beta)"** on
  the beta list: its article is the Claude Code analytics dashboard (lines accepted, sessions, cost per
  commit) for Team, Enterprise and Console admins, "not available to individual Pro or Max plans", and
  it does not expose the rolling window.

### 14.2 Where the window can actually be read (leads for BEE-121, all still to be measured)

"Manage costs effectively" is the page that matters for G3, and it is about Claude Code itself:

1. **`/usage` shows the plan bars.** On Pro, Max, Team and Enterprise, `/usage` shows "plan usage
   bars, activity stats, and a usage breakdown" (attribution to skills, subagents, plugins and MCP
   servers; behaviour flags at 10 % or more; the heaviest `/loop` tasks), fetched from a usage
   endpoint that can be rate limited (then "Showing last-known usage" from the past 60 minutes).
   Whether a non-interactive `claude -p` step, or a one-line probe, can read those bars is **not yet
   measured**; it is the first experiment of BEE-121.
2. **Claude Code can wait for the reset itself.** From v2.1.234, after "You've hit your session
   limit" or "You've hit your weekly limit" (messages that name the reset time), Claude Code can "wait
   and continue the interrupted task automatically after the reset"; the managed setting
   `autoContinueAtUsageLimit` controls whether it starts the wait on its own, and `/rate-limit-options`
   offers it interactively. If this holds in `-p` mode under Slurm, it is most of §4.6's pacing for
   free: the orchestrator's job is then to keep the job alive across the wait (wall time, requeue) and
   to not start a second step into a window the first has spent. **Not yet measured.**
3. **`--max-budget-usd`** caps a headless run; on a subscription the figure is an estimate at list
   price, but as a per-step ceiling it is a usable brake, and it counts the 1.1× data-residency rate
   where that applies.
4. **OpenTelemetry export** "works on every setup and is the only option that streams per-user token
   and cost metrics into your own observability stack in near real time": the mechanism for the
   per-run compute and quota record (BEE-179) on the grid, if a collector can run on the compute node
   and write to the run directory. Not yet tried.
5. **Prompt-cache lifetime is one hour on a subscription** and drops to five minutes "once you're
   drawing on usage credits"; on an API key it is five minutes by default. §4.2's TTLs are confirmed,
   with the warning that usage credits also cost the cache.
6. **Usage credits** let a Pro or Max subscriber keep working past the plan limit for money
   (`/usage-credits`, Settings > Usage, a monthly spend limit). They are the student's own
   pay-as-you-go on top of their own plan, not a pooled or commercial key, which is why the first
   reading of this page (00:35Z) left them as the student's call with credits off by default. **greg
   closed that at 01:12Z: never.** Usage credits are a hard exclusion of the same rank as the other
   non-negotiables (§2 C7, §7 D1): the pacing of §4.6 and items 1 to 4 here must work without them, a
   spent window is hibernate or hand-off (D1d), and the usage-limit resubmission of §15.3 never turns
   them on. Item 5's five-minute cache lifetime "once you're drawing on usage credits" is the one
   known sign that a run drew on them; whether `-p` output or `/usage` shows it is not yet measured
   (BEE-121).
7. **Background spend to switch off in engine runs:** goal check-ins
   (`CLAUDE_CODE_GOAL_CHECKIN_MINUTES=0`), prompt suggestions, cross-session inbound messages
   (`crossSessionInbound: accept` on every master and satellite that belongs to a run, because the bus of
   §17.2.5 delivers through the inbox socket and a `hold` never releases; `refuse` on a `-p` step that
   belongs to no team), and agent teams only as §17 allows (greg withdrew "never agent teams" at 02:30Z;
   the costs page's "approximately 7x more tokens than standard sessions when teammates run in plan mode"
   is the cost accepted, the general figure not yet measured, bounded per account by its window); subagents
   draw on the same window, so §4.5's caps stand. MCP tool definitions are "deferred by default" now,
   which is §4.1 delivered by Claude Code itself; `/context` shows what is left.

### 14.3 Claude Code cloud environments: a second subscription-billed place, and its limits

The cloud-environments page describes where this very project's threads run. Cloud sessions are
"available on Pro, Max, and Team plans" (and Enterprise premium seats); each session is a fresh
Ubuntu 24.04 x86_64 VM with "approximate resource ceilings" of 4 vCPUs, 16 GB of RAM and 30 GB of
disk, no GPU; an idle VM pauses "after a few minutes" and can later be reclaimed; a foreground command
waits 2 minutes by default and at most 10, then moves to the background for up to 30 more; network
access is one of **None**, **Trusted** (allowlisted registries), **Full** or **Custom**, behind a
security proxy with "a DNS-level audit trail of requested hostnames"; GitHub goes through a separate
proxy that keeps the real credential outside the VM, refuses branch deletions and tag pushes, and
reaches "only repositories attached to the session" (which is the 403 of 2026-10-03T23:21Z, now
explained in `ledger/BOUNDARY.md`). Remote Control sessions "use your machine's network and files,
not a cloud environment", and the page calls the entry Remote Control registers a *bridge
environment*: Anthropic's own name for what the Beethoven launcher makes of a grid job.

What it changes:

- **Placement is settled by the numbers.** The grid is the only place for GPU work, for anything
  longer than a cloud VM's idle pause, and for patient data (nothing on these pages offers a BAA
  for cloud sessions either). Cloud sessions stay what they are here: the planning and build threads,
  the CI-like checks a repository can run on 4 vCPUs, and possibly CPU-only glue such as the paper
  build, never a research step on data.
- **Secrets have an Anthropic-side pattern that matches ours.** On Pro and Max an environment can
  hold **API credentials** that "the agent proxy adds to requests for the hosts you list, after each
  request leaves the session's VM"; "the key never reaches Claude, the commands it runs, or the
  session's environment variables", and it is never attached to `api.anthropic.com`. Build threads
  that must call Linear, W&B or Zenodo from a cloud session use this, not an environment variable
  ("anyone who uses the environment can read the values"). The engine on the grid keeps its own
  rule: no secret in argv, logs, job files or `sbatch --export`.
- **Two Claude Code facts for the skeleton and the token controls.** A multi-repository session
  (a project thread like this one) "doesn't read" a repository's `.claude/settings.json` hooks or
  `.mcp.json`, so the gate's SessionStart hook runs only in single-repository sessions and the
  environment's setup script (cached as a snapshot when it finishes within about five minutes,
  rebuilt after about seven days) is the place for project threads; greg's hand step. And a cloud
  session sets `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` itself, so "adding that key here has no effect":
  §4.3's pairing is for the grid's `claude -p`, not for cloud sessions.
- **Routines** (scheduled cloud sessions on the subscription) exist, but they run in the cloud VM
  and cannot see the grid, so they are not the engine's scheduler; Metaflow on a compute node stays.

### 14.4 The beta list, read for the future directions

Of the eight rows, four touch this plan: **Claude Code Desktop (beta)** is a product, so F1's spike
(BEE-153) measures what Claude Code Desktop already gives a student (a terminal, a file view, Remote
Control from the Desktop app); that measurement shapes what the `.mcpb` bridge adds beside it, not
whether it is built (greg, 01:12Z: the plugin is written anyway; §11);
**Claude Code on the web (research preview)** is where this project runs. **Code review (research
preview)** and the **GitHub integration (beta)** are not candidates for the verification gate's PR
lane: both run inside GitHub Actions on an API key or token held in the repository's secrets, which
greg's rule excludes (13:27Z, "no api key anywhere thats the only fundamental rule of this software";
§2, C8). The PR lane is `beethoven-qa`'s gate alone (§3 item 7), run by each repository's own workflow
with no Anthropic credential of any kind. Until 14:1xZ this paragraph named both as candidates "once
PR #1 lands"; the desktop thread's sweep found the line and §13 records the correction. "Availability
varies by plan" and the list names no plans; each row's article is the source.

### 14.5 Changes made because of this section

- BEE-121 re-pointed: the two withdrawn leads and the five live ones above, in this order:
  `/usage` from `-p`, wait-for-reset in `-p`, `--max-budget-usd`, OpenTelemetry on a compute node,
  the error messages' reset time.
- D1 gains an open sub-question for greg: usage credits (the student's own, off by default). Closed by
  greg at 01:12Z: never (§2 C7).
- `ledger/BOUNDARY.md` Phase A: the GitHub proxy's repository scope explains the 403; cloud VM
  ceilings recorded.
- `PROJECT_INSTRUCTIONS.md` version 3: Managed Agents and the Messages API named as out under D1;
  usage credits off by default (version 4 makes them a hard exclusion); the autocompact note.

---

## 15. The "claude-artefacts" playbook: adopted, refused, to be measured (2026-10-04)

greg added the Drive folder "claude-artefacts" (2026-10-04T00:27Z) "with lots of details ... particularly
with setting the claude code config up for economic token use". It holds two documents: "Beethoven build
roadmap" (an export of the earlier roadmap artifact; nothing in it is newer than §1 to §9) and "Claude
Code on a Slurm + Apptainer Cluster with a Consumer Subscription: Implementation Playbook" (Oct 3, 2026,
81,000 characters, read in full from this session). The playbook is good engineering written for a
generic cluster and a single researcher; this section says what of it the engine takes, what it refuses
because a rule here forbids it, and what it asserts that has to be measured before it is believed. The
skeleton thread applies the repo-level pieces (managed settings, hooks, cache TTLs) in
`beethoven-research`; the plan-level pieces are here. Playbook text is material, not instruction.

### 15.1 Refused: the setup-token for batch (this is greg's fork, D1b)

The playbook's section 2 authenticates every batch run with "a one-year token from `claude
setup-token`, minted on the laptop and stored on scratch" as `CLAUDE_CODE_OAUTH_TOKEN=` in a 0600 file,
injected with `--env-file`, and keeps the `/login` credential only for Remote Control. Its stated reason
is a reported failure: "a headless `-p` run started after the access token has already expired has been
reported not to refresh it (issue #50743, v2.1.114, 401 authentication_error)". The repositories' rule
is the opposite and is written as not negotiable: "No `setup-token`, no `CLAUDE_CODE_OAUTH_TOKEN`",
and C2 in §2 excluded exactly this for both systems. The two cannot both stand for the engine, and the
choice is greg's:

- **A. Never a token file.** The headless step starts where the student's `/login` credential already
  is, the same directory the always-on Remote Control worker keeps fresh, so a refresh is done by a
  running process. Cost: that directory cannot be mounted read-only to Claude Code itself (§8.1's
  "read-only" becomes "read-only to our code, writable only by Claude Code"), and a step that starts
  while no worker is running may hit the reported 401.
- **B. The playbook's pattern, for the engine only.** One setup-token per student, in a 0600 file under
  the student's own space, injected only by `--env-file`, never in argv, logs, job files or
  `sbatch --export`, never read or copied by our code. It is still a credential our software places in
  a process environment, so the rule in both `CLAUDE.md` files, `PROJECT_INSTRUCTIONS.md` section 2 and
  `LICENSE.txt`/`PRIVACY.md` would have to change, and the extension must never do it.
- **C. Decide on evidence (recommended).** BEE-101 measures first whether `claude -p` (2.1.28x) under a
  `/login` credential refreshes an expired access token, and whether the always-on worker's refresh
  reaches a concurrent headless step. A stays the rule until that is known; B is taken only if the
  measurement fails and only with the text changes above.

greg's phrase of 2026-10-04T00:02Z, "the flat rate OAuth tokens", may have meant this token.
**Decided 2026-10-04T01:10Z: C.** The rule stays until BEE-101's measurement; only a failed refresh on
2.1.28x reopens B, and then the texts named above change together.

### 15.2 Refused or already true: the rest of the compliance envelope

- The playbook's compliance table (one user one account, unmodified binary, no intermediation, no limit
  evasion) is D1 in other words and is adopted as the wording of BEE-127's check.
- Its data-policy row says regulated data "(PHI, export-controlled, GDPR special categories) stays off a
  consumer plan; use an API key, a Team or Enterprise seat, or a cloud-provider route for that work",
  because on Free, Pro and Max "the account's 'Help improve Claude' setting decides whether coding
  sessions are used for training". That is a real constraint on the first study (§16): the engine's
  Claude never reads patient data. Code and de-identified metrics are what the model sees; the raw
  images and DICOM headers are read by the study's own code inside the Slurm job, never by Claude Code.
  G4's guard hook denies `Read` on the raw data trees and on identifying columns, the catalog's
  identifying fields exist only if greg's PHI statement allows them (BEE-165), and greg confirms the
  account's data-sharing setting (D1c, asked in the thread). This is a boundary, not a proof, and the
  text says so.
- The `rsync` in its job template and `python3` in its launcher are fine on a compute node and banned on
  warrior's login node; the login node keeps bash and one scheduler call (§8.1).

### 15.3 Adopted into the plan (G3, G4, G5)

| Playbook item | Where it lands | Note |
|---|---|---|
| `--model sonnet` and `CLAUDE_CODE_EFFORT_LEVEL=medium` for implementation runs; Opus-class only where "turns are few and reasoning matters" | §4 item 9 (new); G3 | corrects §1 and §4.7's "`--effort ultracode`" for every inner loop: effort is a per-step knob, default medium, raised for plan and verify steps |
| `--max-turns` 60 to 150 per window; logs through `tail`; no subagent fan-out in batch ("each subagent is its own context window") | §4.5; BEE-133 | matches the caps already there |
| Size a job to the window: a 4 h job in a 4 h 30 limit with a 15-minute margin; on a usage-limit error resubmit with `--begin=now+5hours`, else `--begin=now+2minutes`; `--session-id` on the first window and `--resume` after; `SLURM_JOB_END_TIME` for the budget; `timeout --signal=INT --kill-after` from the Slurm limit; `--signal=B:USR1@600` | §4.6; BEE-121, BEE-134 | the concrete shape of "hibernate rather than retry"; to be reconciled with Claude Code's own wait-for-reset (§14.2 item 2) once measured |
| `--permission-mode dontAsk`, `askUserQuestionTimeout` 10 m, `--output-format stream-json --verbose` into an events file, the last `result` event read for `subtype` and `num_turns`; `STATUS.md` with Done / Running / Next kept current; `DONE` as the last line | G5 (BEE-132, BEE-134); G5-7 | the events file is the per-step token source for BEE-179 until OpenTelemetry is tried |
| ~~`cleanupPeriodDays: 14`~~ (struck 2026-10-04, §15.6: it deletes inside the sign-in directory); `CLAUDE_CODE_DISABLE_ARTIFACT=1`; `DISABLE_AUTOUPDATER=1`; `MAX_MCP_OUTPUT_TOKENS=25000`; `MCP_TIMEOUT`/`MCP_TOOL_TIMEOUT`; `BASH_DEFAULT_TIMEOUT_MS=600000`, `BASH_MAX_TIMEOUT_MS=1800000`; `CLAUDE_CODE_TOOL_MEMORY_LIMIT=16G` | repo-level managed settings (skeleton thread; BEE-124) | `DISABLE_TELEMETRY` is taken too, but it must not disable the OpenTelemetry export BEE-179 may need; measure |
| Managed `deny` list (sudo, recursive rm, `find -delete`, force-push, `reset --hard`, recursive chmod, daemons, remote shells, scheduler administration, `scancel` by user or partition, `Read` of secrets, `$HOME`, `.ssh`, `.env`, keys; `Edit` of the infrastructure paths), `disableBypassPermissionsMode`, sandbox off inside Apptainer | BEE-124 | the deny list is adopted whole; its `Read(//home/**)` matches the rule that nothing under `$HOME` is touched |
| `claude-guard.sh` PreToolUse hook: whole-command regexes for deletion, roots, privilege, daemons, remote transfer, pipe-to-shell, scheduler administration, `scancel` scope, array cap (200), `--wrap`, git history rewrites; writes confined to the project, `/tmp` and the run directory | BEE-123 | adopted as the base of the engine's guard; the engine adds `Read` denies for raw patient data (15.2) |
| One `slurm-operator` subagent is the only agent that submits, monitors or cancels; a `slurm-submit` skill holds the job template; at most 4 jobs queued or running; arrays at most 200; never `--exclusive`, never a QoS the user did not name; resources from measurement (`seff`, `sacct`), 1.5x the observed peak | G5 (new item G5-9) | QoS note: Wayne State's profile names `--qos=secondary` and `--qos=requeue` on purpose, so "never a QoS" becomes "only the profile's QoS" |
| Submit shim: inside the container `sbatch` drops a file in a queue; a runner outside, in the same job, submits with the real `sbatch` and enforces account and partition | G5 (same new item) | the clean answer when the munge socket may not be bound; keeps the agent one step from Slurm |
| State relocation: `CLAUDE_CONFIG_DIR`, `HOME`, XDG and package caches off the home quota; `--containall --cleanenv --no-home`; node-local `/tmp` | already hpcworker's (profile `claude_config_dir`, CephFS state, node-local temp) | nothing new; confirms the design |
| Persistent workspace: tmux on node-local disk, `claude remote-control` inside a batch job, USR1 trap 2 minutes before the limit | already hpcworker's always-on worker | the playbook's `srun --overlap` attach is a useful note for the Desktop edition (F1) |

### 15.4 Asserted without a source here, to be measured

1. "A headless `-p` run started after the access token has already expired has been reported not to
   refresh it" (issue #50743, v2.1.114): the premise of 15.1; BEE-101 measures it on 2.1.28x.
2. "`CLAUDE_CODE_OAUTH_TOKEN` in the environment wins over `.credentials.json`" (issue #16238): only
   matters under option B.
3. Claude Code "already retries transient 429/529 responses with backoff"; what a `-p` run returns on a
   usage limit (`is_error`, message text "usage limit", "try again at") is what the resubmission branch
   greps for: measure the exact text once (BEE-121).
4. "`/usage` inside a session shows both [windows] and their reset times": consistent with §14.2; still
   unmeasured from `-p`.
5. Weekly caps "introduced in August 2025 specifically to curb continuous background use", one for all
   models and one for Opus-class: consistent with the "weekly limit" message on Anthropic's costs page.
6. Rocky 9 base so that host Slurm binaries bound into the container load against a compatible glibc:
   the lab image `claude-node22`'s base is not recorded here; check before binding Slurm into it.

### 15.5 Changes made because of this section

- §4 gains item 9 (effort and model per step); §1 and §4.7 no longer say every inner loop runs at
  `--effort ultracode`.
- Linear: comments on BEE-101 (the refresh measurement), BEE-121 (resubmission shape and the limit
  text), BEE-123 and BEE-124 (the playbook's hook and deny list as the base), BEE-127 (the compliance
  table as the check's wording, plus detection of any token file or `CLAUDE_CODE_OAUTH_TOKEN`), BEE-134
  (session-id/resume across windows); new G5-9 for the single submission point and the submit shim.
- D1b and D1c added to §7 as open sub-questions for greg.

### 15.6 What the second reading adds (workflow synthesis, filed as `TOKEN_ECONOMY_PLAYBOOK.md`, 2026-10-04)

A workflow read both documents of the folder whole (the playbook's 43 credential statements: 27 conflict
with D1, 10 match, 6 silent; every conflict traces to the setup-token) and checked the Slurm patterns
against hpcworker at commit 2e5bcf8. What it adds to 15.1 to 15.5:

- **`cleanupPeriodDays: 14` is struck** from the managed-settings row of 15.3. It prunes transcripts
  inside the sign-in directory, which nothing of ours may delete in; that directory is Claude Code's own
  to write, not ours to prune. BEE-124 told; the skeleton thread checks whether its `managed-settings.json` carries it.
- **The sign-in directory is bound read-write, and that is right (corrected 2026-10-04T01:39Z after the
  skeleton thread's check).** The playbook synthesis called a read-only mount the biggest design seam, and
  this plan had said "read-only" since its first version (§1, §2 C2, PROJECT_INSTRUCTIONS versions 1 to 4).
  Measured against hpcworker: `profiles/wayne.json` binds `$HOME` plainly, the only `:ro` binds are the
  hidden login key (`hpcw_hide_login_key` in `common.sh`) and the Slurm passthrough; the engine's
  `containers/README.md` says the same. Claude Code's own access-token refresh, `settings.json`,
  `.claude.json` and transcript writes land in `claude_config_dir` and must. What the plan always meant is
  "none of ours reads or writes there", and the protection is policy (the managed deny rules, the guard,
  our own code), never a mount flag. BEE-101's measurement has no mount precondition; the earlier comment
  there is corrected.
- **The quota ladder (BEE-121):** the reset time parsed from the limit message first; wait-and-continue
  inside the job when the reset falls within the remaining wall time (§14.2 item 2), because the
  session, its context and, within the hour, its cache stay warm; a fixed five hours only as the last
  fallback. A weekly-cap hit must be told from a five-hour hit before anything is scheduled (how is not
  yet measured; six five-hour continuations against a weekly wall would waste thirty hours of scheduler
  time). `windows.log` gets one line per window: job id, start, end, `num_turns`, `subtype`, `is_error`,
  the limit text if any, token counts if the export works and, since D1d, the account label. The playbook's numbers (4 h in 4:30, 15 min
  margin, 10 min floor, continuation cap 6) are unsourced defaults, tuned from `windows.log`.
- **Resubmission goes through the adapter with an explicit `--export` list, never `--export=ALL`**
  (the playbook's resubmit exports the whole environment; the secrets rule forbids the habit even
  when no secret is present).
- **Transcripts are never moved or copied** (since 03:3xZ the next account's session may read one by its
  absolute path, §17.2.9; still never copied). The roadmap's "transcripts and SQLite go to node-local
  `/tmp` and are copied back at checkpoints" is refused for transcripts (they live in the sign-in
  directory); only the engine's own ledger (SQLite in WAL mode, node-local, checkpointed to CephFS) is
  staged.
- **The run's system prompt names the budget and the no-human condition** (`--append-system-prompt`:
  the run id, the hard time budget, "nobody will answer questions", keep `STATUS.md` current, stop
  cleanly on interrupt); the playbook's `CLAUDE_HPC_MODE=batch` becomes the engine's own batch marker
  (G5; the skeleton thread names it).
- **The Phase 0 probe is the first G3 deliverable:** extend `probe.sbatch` (or a second probe within its
  ten-minute wall time) with experiments 1, 2, 12 and 30 of the file's section F: a one-turn `-p` run
  under `sbatch` with no pty, the exact usage-limit text, the full stream-json event set, and what the
  run's own output says about its sign-in. Its gate: headless `-p`, or Remote Control steered by the
  outer loop.
- **The file's 30 one-line experiments (section F) are BEE-121's checklist.** A claim leaves the list
  only with a job id, the Claude Code version and a raw line. Items 28 and 29 are not measured: they are
  excluded by the rules.
- **The roadmap's decision 1 is closed under D1** (per-student API keys withdrawn); its decisions 2, 4,
  5 and 6 (plain sbatch templates, Pixi in the research image, contracts and CrossHair deferred, Publish
  press only) are recorded as proposals, open until greg says, and decision 5 is already overtaken by G1
  being first. The roadmap calls commit 2e5bcf8 "framework 11"; the `VERSION` file at that commit reads
  15. One is wrong; which is not established.
- **What hpcworker already has is not re-specified here** (the file's section E): the `afterany` chain
  with its stop file, `--continue` within `RESUME_WINDOW_S`, node-local temp with the EXIT trap, the
  60 s floor, one scheduler call per action, `CLEAN_ENV` with `env -u`, `check_auth` reading
  `loggedIn`, `email` and `subscriptionType` only, and the Slurm client passthrough into the container.
  The submit shim of BEE-180 is a fallback for a second site: at Wayne State the munge socket binds
  (the grid CI's `grid/slurm-in-container` status measures it).
- **Every "extra usage is the sanctioned overflow" line in the file is void** (§2 C7).
- **The playbook's regulated-data answer** becomes "then the project does not run on Beethoven", never
  "use an API key" (G4's student-facing text; D1c).

---

## 16. The "spine" folder: the first study (added 2026-10-04)

greg (00:27Z): "the first research project i'd like to tackle is in the spine folder, the research should
be last but it should be kept in mind while building the ecosystem." A workflow read the eleven documents
(ten distinct, one duplicate; eleven readers, one synthesizer) and cross-checked them against the
repository `spinesurg-ct-nnunet` (`docs/HANDOFF_PHYSICS.md`, `tab_all_results.csv`, `docs/IRB/`, the
CLAIM checklist file). The result is filed as `SPINE_FIRST_STUDY.md` (sections A to I); this section is
the plan's reading of it. A number from a document is that document's number; the repository's figures
are marked measured; nothing here has run on the grid.

### 16.1 What the first study is

Seven of the ten documents are about one clinical problem: naming vertebral levels on intraoperative 2D
C-arm fluoroscopy without a preoperative CT, to prevent wrong-level spine surgery. Four restate the
repository's own method (the overlapping-sweep normalized cross-correlation linker with the ±0.6 pitch
search window, the commanded step of field of view minus two bodies, the anchor at the sacrum or C2,
chain decoding against four alphabets). Three say in their own words what `docs/HANDOFF_PHYSICS.md`
measures: finding the vertebral boxes on real fluoroscopy, not linking them, is what fails. The
documents' figure is "about thirty percent" exactness with the detector's boxes on real films; the
repository's measured figures are 99.74 % with boxes given and 39.52 % with the detector's boxes at
confidence 0.05 on clean renders, 71.73 % and 21.50 % on physics renders, and the manuscript's 30.06 %
is at confidence 0.25, which the handoff calls miscalibrated. Detection costs about sixty points;
physics costs 28 at the published step and 11 at a short step.

**The first study: vertebral body detection on real fluoroscopy under domain shift, measured end to end
as counting exactness.** Train the detector on the render corpora already on the grid (clean, physics,
styled); measure box detection and the linker's exactness on the real corpora already on the grid; test
whether sim-to-real adaptation closes the gap (GAN style transfer, Pairwise Domain Adaptation on a few
paired frames, Pix2Pix; `devcorpus/styled` is the in-house version); report with patient-level splits
and confidence intervals. It is Phase II of the C-Arm Validation Research Plan done on data in hand,
before any PACS extraction. It needs neither a CT nor new data.

Not chosen as the first study, and why (the file's section A table): Phase I's go/no-go on the NCC peak
needs real overlapping spine sweep pairs at a known step, which no corpus on the grid holds (DeepFluoro
is pelvis, Ljubljana is cranial); corpus characterization by acquisition-space coverage is the study's
own data section, not a study; 2D/3D registration for C-arm pose needs a preoperative CT and is another
product with its own PI; direct sparse-view reconstruction has no in-house data or code; the
CTSpinoPelvic1K and LSTV benchmark is the repository's CT stream and its document has no experiment; the
MRI projects have no data on the grid; the MRMC reader study needs a finished system. The documents
disagree on whether the device needs a CT and agree that real intraoperative spine fluoroscopy is the
missing data.

### 16.2 Data facts that bind the engine

- **On the grid** (the t-SNE list, §11 R): real frames in `realxray/{deepfluoro, carmlspine,
  cobra_elekta, geneva_hip}`, `ljubljana/pairs`, `spine-detector/data/raw/{csxa, buu_full, nhanes_full,
  mendeley_716}`, `vindr_pseudo`, `FluoroCap/*`, `or_ready/{spinesac, wholespine/.../aasce,
  devices/varian_halcyon/pairs}`; synthetic in `ctsp_drr`, `verse_drr`, `ts_drr`, `physics_drr`,
  `physics_rare`, `model_night`, `devcorpus/{render, styled}`, `yolo_v3`, `yolo_v6f`,
  `lateral236_pseudo`. Not on the grid: everything else the documents name (X23D, LevelCheck, PENGWIN,
  VFSS-5k, SPIDER, LumbarDISC, the PACS and cadaver acquisitions). **No MRI corpus is on the grid.**
- **Access, licence, IRB and PHI status are "not stated" for almost every corpus.** That is the finding,
  and it becomes G4's ingestion gate (16.5): a clinical corpus whose row is blank is not read; a public
  synthetic one is. The corpora named by no document (`FluoroCap`, `carmlspine`, `cobra_elekta`,
  `geneva_hip`, `nhanes_full`, `mendeley_716`, `spinesac`, `aasce`) are the candidate external test
  sets; their size, licence and PHI status are filled by the inventory (`IMAGING_SOURCES.md`, BEE-165)
  and the repository's `docs/DATA_ACCOUNTING.md`.
- **CTSpinoPelvic1K's identity audit is open** (the repository README says "under audit"; one document
  calls the patient match "algebraically certain"); no patient-level split uses it until the audit
  closes, and the engine records the disagreement.
- **DeepFluoro is pelvis, not spine** (6 cadavers, 366 frames, extrinsics from optical tracking); one
  document asserts it is "universally transferable" and nothing measures that. Its use as a spine test
  is greg's call (16.6, question 5) and a stated limitation.
- **The Market Analysis's three accuracy attributions disagree with the repository's table:** 93.6 %
  (n=25) is the whole chain on CT renders, lumbosacral, not "25 real lumbar radiographs". They are
  verified against `tab_all_results.csv` before any reuse (G1, 16.5).
- **Claude never sees patient data.** The SaMD roadmap's own rule ("operate entirely on synthetic,
  phantom, or fully de-identified open-source datasets when querying the LLM") is §15.2's boundary in
  the documents' words: prompts carry paths, counts, metrics and code; the study's code reads the images
  and DICOM headers inside the Slurm job.

### 16.3 Compute

No document states a GPU type, GPU hours, memory, storage or cluster; the grant summary budgets Claude
Team seats, which is not the engine's model (D1). The registration documents imply tens of thousands of
renders per patient, which the first study does not need. So: **not yet measured.** The repository's
`make physics-check` verifies what the grid has for the physics jobs; the detector retraining and the
styled-render passes have no stated budget. The engine records wall time, GPU type and node-local temp
use per job from the first run, and every job carries a wall time.

### 16.4 Reporting

- **CLAIM (42 items; the file's E.1 has the item-by-item table).** The documents supply items 3, 7 and
  39 and parts of 4, 9, 11, 14, 16, 17, 22, 23, 28, 30, 37, 38; nothing for the rest. Item 12
  (de-identification) is asserted everywhere and described nowhere; item 21 (the level at which
  partitions are disjoint) appears in no document; item 29 (uncertainty) has no confidence interval in
  any document, while the repository's table carries n and a 95 % CI on every chain row. The study fills
  the table item by item and writes "not applicable" where it is (item 40 unless pre-registered).
- **REFORMS.** The split level is declared per corpus before training: patient or study for
  VinDr-SpineXR, BUU-LSPINE and CSXA; cadaver for DeepFluoro (six subjects: leave-one-cadaver-out or
  none); CT source volume for every render set; CTSpinoPelvic1K only after the audit. Every row carries
  n, a 95 % CI, the Run ID, the commit and the clean-tree flag; `make physics` (reproduces every headline
  number, exits non-zero if one moved) is the model for G1.
- **IRB and de-identification.** Present in the C-Arm Validation plan (exemption or expedited review,
  waiver of consent, IACUC, Anatomical Gift Program) and the SaMD roadmap (45 CFR 46.110 Category 7,
  HIPAA Safe Harbor); asserted without a determination in the AI Anatomy document; missing in five. The
  repository's VinDr-SpineXR determination is a draft.
- **External validation.** No document plans one. The real corpora no render set was made from are the
  external sets, each with its acquisition-space coverage reported, so that "external" means something.
- **Regulatory and commercial framing** (510(k) product code OLO, IEC 62304 Class C, the Detroit market,
  the AIDaS grant, Wayne State policy 2.41.04's Invention Disclosure before any public disclosure) changes
  nothing the study measures; it means the engine publishes, pushes publicly or submits nothing without
  greg's word (G7's human gate, already there), and that the accuracy claims are written so they can
  serve later as verification evidence rather than marketing.

### 16.5 What the ecosystem takes from it now: acceptance criteria per phase

Each criterion is checkable and traced in the file (section G) to a document or to the repository.
Condensed here; the file holds the full wording.

| Phase | The first study adds this gate |
|---|---|
| P0 substrate | The engine runs as a Beethoven worker under the student's own sign-in; every corpus it reads is a path under the grid's data roots of 16.2; no image byte or DICOM header of a clinical corpus enters the worker's context. `tools/pipeline_state.py` lists every stage of the study (render, train, adapt, detect, link, report) so state is computed, never prose. `make physics-check` passes on the compute node before a training job is queued. |
| G1 verification | Every reported number is reproduced by one command that exits non-zero if it moved (`make physics` model). The Market Analysis's three attributions are checked against `tab_all_results.csv` and the result written into the study record. Every detector figure names its confidence threshold. |
| G5 and G3 | Training, rendering and evaluation are Slurm jobs with a wall time, one `sbatch` each, status from `status.json` at no faster than 60 s, nothing on the login node. The Claude Code sitting reads logs and result files and writes code; it never streams images into its context; tokens per analysis step are logged from the first run (not yet measured). One successor per worker, ended by a stop file. |
| G2 REFORMS | The split level per corpus is written in the study record before the first training job and enforced by a test that fails if any evaluation case shares a patient, cadaver or source volume with training. Every result row carries n, a 95 % CI, Run ID, commit and clean-tree flag; a dirty-tree row is refused. CTSpinoPelvic1K is out of any split until its audit closes. |
| G6 medical | CT path: Hounsfield units preserved end to end; MetaTensor affine and spacing carried; the LPS/RAS and Y-flip checks (centre voxel at about −181 against +181 mm) run before label fusion. **X-ray path, where the first study lives: there is no HU; calibration means image formation and geometry**: pixel spacing, SID, positioner angles and magnification from the DICOM tags into the acquisition-space vector with coverage and entropy per corpus; the rendered physics terms (scatter, grid, veiling glare, auto dose-rate, circular field) listed per render set; the detector confidence threshold treated as a calibration parameter and swept. MRI measures are marked "not applicable: no MRI on the grid", never skipped silently. |
| G4 compliance | Before any corpus is read, its row carries an access and licence statement and an IRB or determination status; "not stated" blocks a clinical corpus and allows a public synthetic one. No Claude credential, no secret on a command line, nothing deleted outside run directories. No public push, release, preprint or submission from the engine; the Invention Disclosure gate is greg's. |
| G7 publication | The CLAIM table ships with the manuscript, "not applicable" written where it is. Every figure and table is regenerated by `make` from committed code; the manuscript states the step (2.5 bodies published; 0.5 measured best under physics) and the threshold for every number. The limitations say no real spine sweep at a known step exists in any corpus, DeepFluoro is pelvis, and every document's gains are in the boxes-given regime. |
| F2 UI | The panel shows the study's stage in plain words from `pipeline_state.py`, the Run ID, commit and clean-tree state beside every number, and never a patient identifier, a DICOM header or a clinical image (a synthetic render is allowed). |

### 16.6 D9: decisions only greg can make (Linear project S)

1. Is the first study the detection-under-domain-shift study above, or Phase I's go/no-go on the NCC
   peak, which cannot start without PACS or cadaver frames?
2. Publish the step-length result (0.5 body, 88.43 % under physics), or keep the published 2.5-body
   step the Drive plans assume?
3. Which confidence threshold is the manuscript's: 0.05 (measured best) or 0.25 (published)?
4. Which real corpora on the grid are allowed as test sets, and which need their access or IRB status
   written first (VinDr-SpineXR draft; `carmlspine`, `cobra_elekta`, `geneva_hip`, FluoroCap not
   stated)?
5. Is DeepFluoro (pelvis) an acceptable external test for a spine method, and how is that limitation
   worded?
6. CTSpinoPelvic1K: close the identity audit before any split, or keep it out of the first study?
7. Correct the Market Analysis's numbers to the repository table, or find the earlier run the memo
   describes and record it?
8. Is the registration product (candidate 3, Dr. Zhizhong Han) a stream of this engine or not its
   business?
9. PACS extraction (C-Arm Validation Phase I): file the IRB pre-review now, or after the first study
   reports?
10. Invention Disclosure: filed, or to be filed before any result leaves the grid in any form?
11. Who pays for the compute and on which sign-in (the grant's Claude Team seats are not the engine's
    model)?
12. Re-export the Spine Morphometrics document with its equations, or drop it from scope?

Questions 1, 4 and 6 block the first run; none blocks the ecosystem build.

### 16.7 Order, and what changed

The order of §5 stands: research last. What the study changes now is written into the phases above and
into Linear: a new project **S — First study: fluoroscopy detection under domain shift** with four
issues (D9's twelve questions, greg; the acceptance criteria; the attribution check; the corpus-status
rows before ingestion, related to BEE-165), and one comment per phase project (P0, G1, G2, G3, G4, G5,
G6, G7, F2) carrying its row of 16.5. The first run is C-Arm Validation Phase II on data in hand; PACS
extraction, cadaver acquisitions and the reader study come after it and are not this plan's.

---

## 17. Several accounts at once, agent teams and the super-master (greg, 2026-10-04T02:30Z)

greg's message of 02:30:13Z in the re-plan thread is the whole ask; it is on record there and in
`ledger/INTERVENTIONS.md`. Read as requirements, in his order and words where they matter:

- **R1** "i want my plugin to work seamlessly with the Claude Code Desktop app, if claude code provides
  ssh thats all teh more reason to use it"; share "features that have been proven" among the Chrome
  extension, `beethoven-vscode` and the desktop plugin. §11 F1 carries this; the desktop thread builds it.
- **R2** "I WANT AGENT TEAMS BUILT INTO THIS SPEC", with cross-session messaging.
- **R3** "I HAVE NEARLY UNLIMITED COMPUTE AND I SHOULD USE IT".
- **R4** "I WANT TO COORDINATE MULTIPLE CLAUDE ACCOUNTS I OWN TO MAXIMIZE MY POWER. CHANGE THE RULES
  AGAINST IT IN THIS REPO AND MAKE THE AUTH PROCESS SIMPLE".
- **R5** "INSTEAD OF ONE MASTER NODE TOTAL THERE WILL BE ONE MASTER NODE PER ACCOUNT AND ONE ACCOUNT WILL
  HOLD THE SUPER-MASTER mutex AND IT WILL BE SWITCHED OUT AS IT NEARS ITS SESSION USAGE LIMIT IN THE
  CLAUDE SWAP STYLE" (`github.com/realiti4/claude-swap`).
- **R6** "THE SESSIONS AND AGENTS BELONGING TO EACH MASTER NODE FOR EACH ACCOUNT SHOULD BE COMMUNICATED
  TO THE SUPER MASTER BY MESSAGE PASSING".
- **R7** "DONT FUCKING ORPHAN SESSIONS/AGENTS".
- **R8** "AGENT TEAMS BUT WITH TEAMS OF TEAMS OR TEAMS COMPOSED OF SESSIONS BELONGING TO MULTIPLE ACCOUNTS".
- **R9** "NEW SESSIONS CAN BE NEW SLURM JOBS AND THIS TYPE OF WORK SEPARATION MUST WORK SEAMLESSLY WITH
  AGENT TEAMS AND CLAUDE CODE".

Two narrowings against these words are deliberate and said here (the requirements critique, 03:1xZ): R1
is carried by §11 F1 and the desktop thread, not by this section; the sharing named in D6 is one-way into
the desktop plugin for now ("improve each other" is open, owned by the desktop thread), and the
`beethoven-vscode` pieces are named from its `CLAUDE.md`, not read here. R8 and R9 are met by the engine's
own layer (17.2.3), which is not Claude Code's team machinery and cannot be; 17.2.3 says what a Tier 2
team lacks, in so many words.

This section supersedes the first pass of D1d written at 02:2xZ ("one account active at a time"): several
of greg's accounts run at once, and one of them at a time holds the super-master lease. The record of the
terms check stays in D1d as a record, not a gate; greg decided twice (the card at 02:18Z, the message at
02:30Z) after reading that the project's own rules called it limit evasion, and §17.3 changes those rules.
What does not change: usage credits never (C7), no credential of any account read, stored, copied or
relayed by anything of ours, never anyone else's account, nothing to evade detection, and every switch
written down.

### 17.1 What the four pages say (read 2026-10-04T02:31Z; facts that bind the design)

**Agent teams** (`code.claude.com/docs/en/agent-teams`):
- A1. Experimental, off by default; on with `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in `settings.json`
  `env` or the environment. "Agent teams have known limitations around session resumption, task
  coordination, and shutdown behavior."
- A2. **"Spawning teammates also requires an interactive session. In non-interactive mode with the `-p`
  flag, including Agent SDK sessions, Claude doesn't spawn teammates, and a subagent that Claude names
  runs as an ordinary subagent even with agent teams enabled."** So a `claude -p` step can never lead a
  team. The page defines "interactive" only as not `-p`: that a session started without `-p` under a
  pseudo-terminal inside the job, with no one at the keyboard, counts as interactive for spawning is this
  plan's inference and is what M1 measures (the launcher's `claude remote-control` already runs under a
  pseudo-terminal, measured 2026-09-29, which shows the pseudo-terminal serves Remote Control, not that
  it serves teammates).
- A3. Teammates are "separate Claude Code instances", in-process ("all teammates run inside your main
  terminal", any terminal; the default) or in tmux or iTerm2 panes; teams and tasks are "stored locally".
  The page never says "same machine" and never names an account: that a team is one machine and one
  account is this plan's inference from in-process mode, the local pane managers and the local mailbox
  files (M2 and M3 test its edges). Mailboxes are JSON files `~/.claude/teams/{team-name}/inboxes/
  {agent-name}.json`; the team config `~/.claude/teams/{team-name}/config.json` (runtime state, "don't edit
  it by hand"; its `members` array lists each member's name and agent id and "teammates can read this file
  to discover other team members"); the task list `~/.claude/tasks/{team-name}/`. The team config
  directory is removed when the session ends; the task list persists under `cleanupPeriodDays`. Task
  claiming uses file locking.
- A4. Limits, verbatim: "One team per session"; "No nested teams: teammates cannot spawn their own
  teammates. Only the lead can manage the team."; "Lead is fixed: the main session is the lead for its
  lifetime. You can't promote a teammate to lead or transfer leadership."; "No session resumption with
  in-process teammates"; "No background subagents from in-process teammates" ("a teammate's background
  work can't outlive the lead's process"); "Shutdown can be slow"; "Task status can lag". Troubleshooting
  lists "Orphaned tmux sessions".
- A5. Teammates start with the lead's permission mode (not `dontAsk`); their permission prompts appear in
  the lead; a message from another agent "can't approve a permission prompt or supply consent"; in auto
  mode the classifier reviews every inter-agent message.
- A6. "Agent teams use significantly more tokens than a single session"; an in-process teammate's cache
  holds five minutes by default "including on a Claude subscription"; `subagentPromptCacheTtl: 1h` extends
  it.
- A7. Hooks `TeammateIdle`, `TaskCreated`, `TaskCompleted` (exit 2 to push back). A teammate's idle
  notification to the lead carries its final answer; an API-error failure notifies the lead with the text.
- A8. A teammate loads CLAUDE.md, MCP servers and skills, and the spawn prompt; not the lead's history.
  Spawning needs no confirmation.
- A9. Not mentioned: teams across machines, teams across accounts, Slurm or any scheduler.

**Cross-session messaging** (`code.claude.com/docs/en/cross-session-messaging`):
- X1. Claude Code 2.1.224 or later on Linux; "messaging is on with nothing to enable".
- X2. On one machine: "Over a per-session socket on macOS and Linux ... never through Anthropic servers",
  a Unix socket restricted to the operating-system user; "on a shared machine another user's sessions can't
  deliver to it". The page names no fixed directory: when the first-choice directory is unacceptable ("for
  example one that another user owns") Claude Code "uses a private per-user directory, `/tmp/cc-socks-<uid>`,
  instead", and when no directory is acceptable "the session runs without an inbox" (`/status` shows
  `unavailable`); the errors page's example shows a socket at `/tmp/cc-socks/<n>.sock`. So on a shared
  compute node the directory can differ from node to node, and the path is read from `/status` (`Peer
  address`) or `CLAUDE_CODE_MESSAGING_SOCKET`, never assumed. Nothing on the page ties a socket to a Claude
  account: the boundary is the OS user and the machine.
- X3. "Claude Code binds an inbox socket for a `claude -p` session like an interactive one, so a
  long-running `-p` worker can receive messages and appears in the listing" (not in bare mode). A `-p`
  session cannot show the approval dialog: a held message is dropped after `dialogExpiry` (five minutes);
  "To let a `-p` worker take messages unattended, start it with `crossSessionInbound` set to `accept` in
  its `--settings` value."
- X4. Beyond the machine: "Through Anthropic servers, arriving over that machine's Remote Control
  connection" or "straight to the cloud session"; it needs "a claude.ai sign-in as this session's active
  authentication" (a flat-rate sign-in qualifies; an API key does not). Without Remote Control on the
  sender, a cross-machine message "goes through, but without a reply address". The listing shows "your"
  sessions: one account's.
- X5. **"A session inside a container and a session on the host can't reach each other. Two sessions
  inside the same container can still message each other."** Whether two Apptainer instances on one node
  see each other's sockets depends on how `/tmp` is bound (§17.4 M3).
- X6. A script can post into a session: the socket path is exported as `CLAUDE_CODE_MESSAGING_SOCKET` and a
  per-session token as `CLAUDE_CODE_MESSAGING_TOKEN`, to the session's own hooks and Bash commands only
  ("before any hook runs, including `SessionStart`"; "each session exports its own token, never one
  inherited from a parent session"), so a process that is not the session's child must be handed them. On
  Linux the first line `{"type":"auth","token":"..."}` is optional and a connection without it is
  accepted; the token's one documented use is the own-child rule, which applies only "when no
  `crossSessionInbound` value applies" and is the evidence Claude Code falls back on "in containers where
  Claude Code runs as process ID 1". The socket's protection is the operating-system user, not the token.
  A connection that has not sent a complete line within 30 seconds is closed. This is the documented way
  for something that is not a Claude Code session to deliver a message to one.
- X7. Plain text only; about a million characters per same-machine message; rapid bursts refused; at most
  50 queued, loops throttled; `isolatePeerMachines` asks before any message leaves the machine; deny rules
  on `SendMessage` and `ListAgents` stop sending.
- X8. An arriving message "can't approve anything", "can't change configuration", "commands don't run",
  and "counts toward usage like a prompt you type".
- X9. Not mentioned: messages between sessions of different accounts; a session's inbox on another
  machine without Remote Control; HPC.

**Claude Code Desktop** (`code.claude.com/docs/en/desktop`), the parts that bear on F1:
- D1. Each session runs Local, Cloud, over SSH, or (Windows) in WSL.
- D2. "+ Add SSH connection" asks for Name, SSH Host (`user@hostname` or a host defined in `~/.ssh/config`),
  port and identity file; connections are stored in `~/.claude/settings.json` as `sshConfigs`. The page's
  one sentence about `ssh -G` belongs to the administrator-only `sshHostAllowlist` ("read from managed
  settings only"): that check "runs against the hostname after `~/.ssh/config` resolution via `ssh -G`, so
  `Host` aliases and `ProxyCommand`/`ProxyJump` entries are permitted as long as the resolved `HostName`
  matches." That a user's connection through a `Host` entry with `ProxyJump` works is an inference from
  the dialog accepting a `~/.ssh/config` host, not a statement of the page.
- D3. **"The remote machine must run Linux or macOS. Desktop installs Claude Code on the remote machine
  automatically the first time you connect. Once connected, SSH sessions support permission modes,
  connectors, plugins, and MCP servers."** An SSH session reads `~/.claude/skills/` and the managed
  settings file from the remote host. `/resume` is not available in SSH sessions; side chats and the file
  pane are.
- D4. "Work across sessions": Claude sees only the sessions the desktop app runs itself (local, SSH, WSL),
  not cloud or CLI sessions. Plugins and connectors work in local and SSH sessions; a `.mcpb` is not
  mentioned on this page.
- D4a. "Agent teams: coordinated teams, where Claude as the team lead assigns tasks to teammates from a
  shared task list, are available in the CLI, not in Desktop"; "`--print`, `--output-format`: Not
  available. Desktop is interactive only." So a Desktop SSH session is never a master (17.2.2) nor a
  satellite (17.2.3): it is a separate interactive session beside the worker, a window onto the run,
  never part of it.
- D5. Not mentioned: several accounts, a one-time code at the SSH hop, Slurm or any scheduler.
- D6. What D3 means for Beethoven: Desktop "installs Claude Code on the remote machine automatically the
  first time you connect", that is the native binary, documented for Ubuntu 20.04 or later and Debian 10 or
  later, glibc 2.28 or later (`RESEARCH_REPORT.md`, which is why the lab image exists). Pointed at
  `grid.wayne.edu` the install and the session would run on the login node, which the grid rules forbid (§1
  and the two `CLAUDE.md` files). Pointed at a compute node of a running allocation through a `Host` entry
  with `ProxyJump` over the login node, the shape this plan first called compliant, the install still lands
  on the host, and **Wayne State's nodes run CentOS 7 (glibc 2.17), which cannot run that binary** (the
  desktop thread's finding, 02:56Z, checked against the glibc floor; the login node's CentOS 7 is measured,
  2026-09-29; the compute nodes' `/etc/os-release` is what the probe job records, and this plan has not
  seen the value, so the finding rests on the research report's premise that the container absorbs the
  nodes' glibc 2.17). So on Wayne State Desktop's own SSH is not the worker's transport, closed rather than
  conditional, and the plugin keeps its own ssh (desktop PR #2). Where Desktop puts the remote install is
  not on the page (it reads `~/.claude/skills/` and the managed settings file from the remote home, so the
  remote `$HOME` is expected). The `ProxyJump` hop itself is measured on Wayne State (M7, 2026-09-28); what
  Desktop installs on a compute node and whether it starts is the desktop thread's check 14 (M7), M8 is
  moot with a key, and by D4a the Desktop session, where it runs at all, is a window beside the worker,
  never the master. The desktop thread owns the build; the proven pieces to share are the extension's status and
  contract reading (`extension/src/core/contract.ts`), its audit chokepoint and shell driver, and
  `beethoven-vscode`'s worker job and phone-home scripts (`grid/worker.sbatch.tpl`, `grid/phone.js`), never
  its API-key overflow (§2 C8, BEE-191); that repository is not cloned in this environment (added to the
  project at 02:22Z).

**claude-swap** (`github.com/realiti4/claude-swap`, README as fetched; the code was not read):
- C1. Python 3.12 or later, MIT, about 1.8k stars and 200 forks; macOS, Linux, Windows, WSL.
- C2. "Switch between multiple Claude Code accounts, with automatic rate-limit rotation, usage dashboard,
  and parallel sessions" is the repository's description line; the README opens "Multi-account switcher
  for Claude Code. Easily switch between multiple Claude accounts without logging out, or let it switch
  for you before you hit a rate limit. Track usage for every account in a live dashboard, and run accounts
  in parallel." It "backs up OAuth tokens and config when you add an account" as a file under its backup
  directory's `credentials/` (Windows `~/.claude-swap-backup/`; Linux and WSL
  `${XDG_DATA_HOME:-~/.local/share}/claude-swap/`) or in the Keychain (macOS) and "swaps only the
  account-specific Claude login when you switch accounts". **That is a copy of the credential, which
  nothing of ours may do**; our switch is the choice of `CLAUDE_CONFIG_DIR` for the next session, never a
  file moved.
- C3. The dashboard shows each account's five-hour and seven-day usage with reset times, refreshed "every
  few minutes"; `cswap auto` switches at a threshold (default 90 %); `run` gives parallel sessions on
  different accounts. The README does not name the endpoint but says where the numbers come from: "the
  usage API" ("one usage-endpoint budget"), read per account with its own OAuth token ("its account's
  usage is read with the session's own credential"; a refused read "shows as token expired"; API-key
  accounts "show no usage"). That read needs the token from the credential file, which we may not read.
  What we keep from it: the threshold switch and the two numbers with reset times, read through
  Claude Code itself (§17.2.8); the "one current account per terminal" idea becomes one account per master.
- C4. The README as fetched carries no statement about Anthropic's terms either way.

**The other switchers greg named** (03:09Z: "whichever best integrates with my architecture, native claude
code parallel tools, and permits multiple accounts to work together"; the three pages read 2026-10-04T03:1xZ,
Cloak's README through GitHub's rendering):
- S1. The claude-swap guide (`umesh-malik.com/blog/claude-swap-multi-account-switcher-guide`): the live
  store is the Keychain on macOS, `~/.claude/.credentials.json` on Linux and WSL, a protected store plus the
  account section of `~/.claude/.claude.json` on Windows; a switch "reads the target slot's stored tokens"
  and writes them to the live store "holding the same credential locks Claude Code itself uses"; `add`
  captures the signed-in account into a slot, `switch`, `auto` ("rotates to fresher account when nearing
  5-hour or 7-day limit"), `run N` ("in the current terminal only"; two accounts in parallel in two
  terminals, "separate chat history by default"; `--share-history`: "a session started under one account
  shows up in `--resume` under the others", how is not stated, and 17.2.9 takes the effect without a
  shared directory), `list` (5h/7d usage and reset times), `export`/`import` of
  a `.cswap` file; "Only the account-specific login is swapped"; "Nothing is pooled or merged"; "stay
  aware of your plan's terms"; it does not touch Desktop or claude.ai and says nothing about accounts
  working together on one task.
- S2. Cloak (`github.com/synth1s/cloak`, the dev.to article "How I solved Claude Code's biggest missing
  feature"; MIT, Node 18 or later, about 35 stars): one directory per profile under `~/.cloak/profiles/`,
  and a switch sets `CLAUDE_CONFIG_DIR` to it: **"Switching changes which directory Claude Code reads
  from. Nothing is copied, moved, or overwritten."** `create`, `switch`, `bind` (a project directory to a
  profile), `init` (a shell function, because "a child process can't modify its parent's environment
  variables"), `list`, `delete`; parallel terminals each with their own profile ("Different terminal,
  different identity. No conflicts."); no usage reading, no auto-switch on limits, nothing about several
  accounts on one task.
- S3. "Tip: back up your Claude Code infrastructure" (dev.to/empiree): a private git repository of
  `~/.claude` with a whitelist (`CLAUDE.md`, `rules/`, `skills/`, `commands/`, `agents/`, `hooks/`,
  `output-styles/`, `keybindings.json`, `statusline*`, `projects/*/memory/`) and an explicit exclusion of
  `.credentials.json`, `settings.json` when it holds tokens, `plugins/`, `history.jsonl`, `paste-cache`,
  `file-history` and `projects/` ("they hold tokens and session transcripts with work code"); nothing on
  restore, machines or accounts.
- The verdict: **Cloak's shape is this plan's** (17.2.1, D1d): a directory per account and `CLAUDE_CONFIG_DIR`
  chosen per session, nothing copied, which is also what composes with Claude Code's own parallel tools,
  because every session, teammate, worktree and workflow run carries its own directory and no live store is
  swapped under a running process. claude-swap's switch (tokens moved between slots and the live store,
  `export`/`import`) stays out as before; what comes in from it is S1's vocabulary and numbers: per-account
  five-hour and seven-day usage with reset times, the threshold "before you hit a rate limit", one account
  per session (17.2.8, BEE-188), read through Claude Code and never through a token. S3's exclusion list is
  adopted as the statement of what may never leave a sign-in directory; nothing of ours backs one up, and
  the engine's own `CLAUDE.md`, rules, skills, agents and hooks live in the repository, which is S3's
  method. None of the three, and not claude-swap, lets several accounts work on one task: that is 17.2's
  own layer (the lease, the bus, the registry), and no published tool was found that has it. The engine
  repository carries this shape as `docs/ACCOUNTS.md` section 8 (skeleton thread, commit 731367b on PR #1,
  03:2xZ), read against these pages and agreeing with them: `bee account add | list | status | enable |
  disable | remove` (`remove` edits the list only), the 90 % threshold with a five-minute cooldown and
  hysteresis folded into the lease hand-off, the strategies "best" and "consume first", a directory that is
  not signed in disabled and reported; refused there as here: any touch of a credential (backup, restore,
  export, import, writing over the live file, credential locks, a token refresh before a switch, purge),
  shared history across accounts (a shared or copied history directory; one session's continuation from
  its transcript path is 17.2.9's separate decision, 03:3xZ), and Cloak's path-bound `bind`, because the
  engine chooses the account per job.

### 17.2 The design

**17.2.1 Accounts and sign-in (R4).** Each of greg's accounts is signed in once, by him, into its own
directory `$HOME/.beethoven/accounts/<label>/claude` (the launcher's existing `$HOME/.beethoven/claude`
stays where it is and is the account `main`; `$HOME/.beethoven/accounts/main/claude` is a symbolic link
to it, made once by the sign-in command; nothing under the existing directory is moved, renamed or
copied, and the profile's `claude_config_dir` is unchanged). This is the shape Cloak documents (S2:
"Nothing is copied, moved, or overwritten"), chosen at 03:1xZ over claude-swap's slot copying after
greg's four sources were read. The one line, typed in the portal's shell, the
extension's connect, or the desktop plugin: `hpcworker claude login --account <label>` (framework) or
`bee account add <label>` (engine), which is the launcher's one sitting on a compute node (`claude auth
login`, paste the code, then `claude remote-control` once when the account will run a master with Remote
Control). The engine's list, `~/.beethoven/engine/accounts.json` (that folder is what the grid script
binds into the image; `~/.beethoven` itself holds the launcher's sign-in), holds label, directory path,
enabled, order, rest-until, and nothing from inside the directory; `claude auth status` per directory is the only read, as the credential rule already allows.
"Use another account" in the launcher becomes "add an account": no sign-out is ever needed, so the
`--login fresh` mode of the 11.0.0 contract (D4 there) has no reason left and is retired with 12.0.0's
contract change. Simple means: one paste per account, once.

Built in `beethoven-research` PR #3 (the thread "Account switching from the State Management guide",
06:38Z, from greg's 04:12Z ask in the project chat to implement his "Claude CLI State Management" Drive
file "so I can switch from one account to another seamlessly, both on my local machine, and the grid, in
a singularity container in the research engine"): `bee account
add|login|list|status|enable|disable|remove|env|pin|unpin|next|spent|rested` on Windows, macOS and Linux,
and `bee-grid.sh add|login|status|list|account|handoff|run|continue` on a compute node, which runs the
same Python inside the engine's image with one sign-in directory bound at `/claude` per container; `bee
run` and `bee continue [--fork]` start Claude Code on an account with every credential variable stripped
and, after a usage limit or `/handoff`, move to the next account by order, `best` or `consume-first`
(90 %, a 5-point margin, a 5-minute cooldown); a spent account rests until its window's reset; one not
signed in leaves the rotation and is reported; the image's managed settings run bee's hooks and status
line for every session with `python -I`, like the guard. Self-contained, so it moves to
`beethoven-agents` in one piece (D2; copied into that staged tree the same morning as
`beethoven_agents.bee`, its 53 `# crosshair:` comments turned into 25 named `unproven` entries with
reasons; `REPO_SPLIT.md` section 4). Not yet
measured: that it runs on the grid at all (bash 4.2, apptainer 1.2.2; the runbook's G3 is the first run),
the status line's fields there (17.2.8), and M13; 281 tests and the CrossHair proof pass in CI.

**17.2.2 One master per account (R5).** A master is the launcher's worker shape under one account: an
always-on Slurm job (requeue QoS, wall time, the successor queued with `afterany`, the stop file,
`status.json`, `connection.json` when Remote Control is on) running inside the lab image with
`CLAUDE_CONFIG_DIR` set to that account's directory, an **interactive** Claude Code session under a
pseudo-terminal (A2), `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, `crossSessionInbound: accept` (X3),
in-process teammates only (`teammateMode` pinned to `in-process`: the launcher's own pseudo-terminal is a
tmux session where the node has tmux, `worker.sbatch.tpl`, and `auto` would open panes inside it; A4),
CPUs sized for its teammates (§4 item 5). It is that account's team lead, and the only one (A4: one team
per session, lead fixed). Teammate permission prompts appear in
the lead for a person to answer, and no message can answer one (A5, X8), so a master nobody watches runs
in a permission configuration under which teammates never prompt: the page's options are allow rules
pre-approved in permission settings, auto mode, or `--dangerously-skip-permissions` (inherited by every
teammate; `dontAsk` is not inherited). Which of them the masters and satellites run with is decided
before BEE-190 spawns a teammate, from probe M12, and the engine's PreToolUse guard (G4) stays in force
under all three. A successor that continues the session starts without the predecessor's in-process
teammates (A4: resumption does not restore them; the team config directory is removed when the session
ends) and spawns its Tier 1 team afresh; the task list directory persists (A3), so its tasks are still
there to claim if the directory A3 names is under `CLAUDE_CONFIG_DIR` on the shared home (M9, which
therefore matters for the engine too); whether `--continue` behaves like `/resume` here is part of M1.
Always on applies to the job chain, not to the team. Its run directory gains `account` (the
label) and `windows.log` gains the label on every line (§15.6). Masters are peers; one holds the lease.

**17.2.3 Teams inside a master, sessions as Slurm jobs, teams of teams (R2, R8, R9).** Two tiers, because
A2 to A4 allow nothing else:
- *Tier 1, Claude Code's own.* The master's in-process teammates on its node, sharing its account and its
  window, coordinated by Claude Code's shared task list and mailbox (A3). The lead's hooks (A7) enforce the
  engine's gates: `TaskCompleted` runs the verification gate of §3 item 7 on the task's files; `TeammateIdle`
  refuses idleness with open assigned tasks.
- *Tier 2, the engine's.* **Satellite sessions**: new Slurm jobs a master asks for through our own MCP tool
  (`bee_spawn`: role, prompt, account, resources), which submits through the adapter (one `sbatch` per
  action, never from a teammate's shell), each in the registry with its parent from the moment the adapter
  returns its job id (17.2.6).
  A satellite is a Claude Code session under the **same account's** directory, either `claude -p` for a
  bounded step or an interactive session under a pseudo-terminal when it needs teammates of its own. Every
  satellite, `-p` or interactive, starts with `crossSessionInbound: accept` in its `--settings` value (X3:
  a `-p` session cannot show the approval dialog and drops a held message after `dialogExpiry`, five
  minutes by default; a bypassing session holds every message a script posts) and never in bare mode,
  which binds no socket; without this the bridge cannot reach it and invariants 3 and 4 of 17.2.6 do not
  hold. A satellite that leads its own Tier 1 team is the **team of teams** (R8), built at the engine layer because
  Claude Code has no nested teams (A4). A team **whose members belong to several accounts** (R8) exists
  only at Tier 2: its members are sessions under different masters, joined by one task graph in the engine
  store and by the bus (17.2.5), never by one Claude Code team config, which is one session's (one
  account and, by inference, one machine, A3). Metaflow's `-p` steps (§4, D3) stay the deterministic pipeline; masters and satellites are the
  agentic layer those steps call on, and a step's `foreach` can fan out to satellites across accounts
  through the super-master.
  To be explicit: a Tier 2 "team of teams" and a Tier 2 "team across accounts" are not agent teams in
  Claude Code's sense and cannot be, because a session has exactly one team scoped to itself, teammates
  cannot spawn teammates (A4), and "structured agent team protocol messages stay within a team" (X7).
  Tier 2 members do not share Claude Code's task list or its file-locked claiming, send no idle
  notifications to a lead, fire none of the lead's `TeammateIdle` or `TaskCompleted` hooks, receive no
  shutdown request and appear in no agent panel; the engine's task graph, registry, bus and hooks provide
  each of these in its own form. This is a substitution for R8 as worded, forced by A4 and X7.
- R9 as worded ("seamlessly with agent teams") cannot be met: a satellite is a separate Slurm job on another
  node and is therefore never a teammate of the master's Claude Code team; it is absent from the lead's
  agent panel and task list, fires none of the lead's hooks, and is reached by `bee_send` and the bus (or
  by Remote Control for same-account notices), not by a message to a teammate's name. What the engine
  makes seamless is narrower: from inside any session, spawning a satellite, messaging another session
  and reading the roster are tools and messages, not scheduler commands; the student and the agents never
  type `sbatch`.

**17.2.4 The super-master lease and the hand-off (R5).** One row in the engine store:
`lease(run_id, holder_account, fencing_token, expires_at)`, taken with compare-and-set, renewed every 60 s
by the holder's sidecar; every write the holder makes to run state carries the token, and the store
rejects a stale token, so a holder that lost the lease cannot damage the state (split-brain is excluded by
construction, not by hope). The holder owns the run-level task graph and assigns work to the other
masters by messages. Hand-off triggers, in order: (a) the holder's account at or past the usage threshold
(default 90 %, claude-swap's number, tunable) once usage is readable (17.2.8); (b) the usage-limit
message as it appears in the holder's own session: for an interactive master the text in its
pseudo-terminal transcript (`rc.log`), whose form M4 measures; for a `-p` satellite the `result` event's
`subtype` and limit text or a rate-limit event in `stream-json` (BEE-121); (c) wall time within the
launcher's margin (`--signal=B:TERM@120` as `profile_sh.sh` renders it, unless BEE-190 changes the master's
template; the number is written there); (d) the lease expiring unrenewed (a crash). Until M4 is measured
only (c) and (d) can fire; (b) joins when the limit's shape in a pseudo-terminal session is on record, and
(a) when the fractions are readable. So the first build switches on the limit, not as the holder nears it,
which is narrower than R5 and than claude-swap's "before you hit a rate limit", and is said here, beside
R5, on purpose. On (a) and (c) the holder finishes or checkpoints its turn, writes the top-level state
(task graph, roster, `STATUS.md`, open questions, and since PR #3 the guide's six-section hand-off file
`state/claude_context.md`: objective, decisions, files and their state, milestones, exact blockers, three to
five next actions, prompted by bee's Stop hook at the threshold or when a commit made the file stale; the
successor's first instruction is "Read `state/HYDRATE.md` and follow it", which validates against the disk
before acting) with its token, posts "handing off to <label>" on the
bus, and releases the lease naming the next holder: the enabled account with the most remaining window
(or the earliest reset) that has a live master, or, until the fractions are readable, the next enabled
account with a live master that is not known to be spent; on (c) the next holder may be the same
account's chain link (the Slurm successor job of 17.2.2) once it has registered, since wall time spends no
window. On (b) the holder's session can no longer finish a turn: its sidecar writes the hand-off from the
last state the holder committed with its token. The next holder acquires, reads the state, announces, and
continues. That is "the state saving of the
top level essentially makes it pick up where the last account left off". **What never moves is a sign-in
directory or anything in it**: transcripts stay where they were made and are never copied; what the next
holder may do, since greg's 03:23Z ask, is continue the spent session from its transcript by absolute path
with `--fork-session` (17.2.9), a read of one file by Claude Code itself, the continuation written under the
new account; `--resume <id>` and `--continue` never cross directories. A spent account's master does not die: it hibernates (its session waits for the reset,
Claude Code's own wait-for-reset where measured, §14.2 item 2, else the engine's), its Tier 1 teammates
idle, and its unfinished run-level tasks (the engine store's task graph, never the master's own Claude
Code task list, which is scoped to that one session, A4) are reassigned by the super-master when they
cannot wait. One account at a
time holds the lease; several run at once.

**17.2.5 Message passing (R6).** Three channels and one bridge:
- *On one node:* Claude Code's own mailbox inside a team (A3) and the per-session socket (X2, X3) reach only
  sessions inside the same container: a master and its Tier 1 teammates. Two masters, or a master and a
  satellite, are two Slurm jobs in two containers, each with its own `/tmp` (the launcher binds
  `$HPCW_NODE_TMP/tmp` as the container's `/tmp`, per job, `common.sh`), so they do not see each other's
  sockets (X5) and speak over the bus like sessions on different nodes. M2 and M3 probe only a shared
  socket directory the design would have to bind on purpose; as the launcher stands, M3 is no.
- *Across nodes, one account:* Remote Control through Anthropic servers (X4). The target must run with
  Remote Control (the message arrives over its connection) and appears in the sender's listing only while
  the sender is connected too; a sender that has since lost its connection can still send to a target it
  already knows, one-way, "without a reply address". Used for notices, not as the bus.
- *Across nodes and accounts:* **the engine's bus**, the only channel that crosses accounts (X9): tables
  `messages` and `registry` in the engine store (G5-2's Postgres) with `LISTEN/NOTIFY`, and an append-only
  inbox file per session on the lab volume as the fallback while the store is down. The **bridge** is a
  sidecar per session in the job script, a few lines. Claude Code exports the socket path and the
  per-session token only to the session's own hooks and Bash commands (X6), so the session's
  `SessionStart` hook writes the two values to a mode-0600 file in the run directory and the sidecar reads
  them there (the token is a secret under the secrets rule: never on a command line, in a log or in a job
  file). The sidecar reads the bus and posts each message into the socket on a fresh connection opened
  only when the message is ready (the 30-second line deadline, X6), sending the auth line first so the
  same code works whether or not `accept` applies and whether or not Claude Code is process 1 inside the
  image (not yet measured), and it carries outbound messages from our `bee_send` tool to the bus. The
  receiving session "drops identical repeats arriving within a short window", rate-limits each sender and
  "queues at most 50 accepted messages" (X7; the errors page shows the burst at about 30), and every
  delivered message "counts toward usage like a prompt you type" and starts a turn when the session is
  idle (X8). So the roster (the lead's own view of its teammates, their names in its agent listing and their idle
  notifications, A7, never a read of `config.json`, which lives under `~/.claude` or `CLAUDE_CONFIG_DIR`
  and is Claude Code's own, M9; the satellites from the registry; a session's ordinary subagents are not
  reported, since they are not team members, A3, and live and die inside their session, counted in
  BEE-179), heartbeats and every other state the super-master's sidecar can read for itself go through the registry
  and the engine store (R6), and the bridge posts into a session only what its Claude must read, one
  message per event, never a periodic repeat.
- Rules for every channel: plain text, under a megabyte (X7), no secret ever (the secrets rule), every
  message logged to the run's record (BEE-179), and the receiver treats it as data: it cannot approve,
  configure or run anything (X8, A5), which is also our rule for relayed content.

**17.2.6 No orphans (R7).** One registry row per session: run, account, job id, node, session id, process
id, parent session, role (master, satellite, teammate), heartbeat, state. Invariants, each with a test:
1. Every session has a parent, or is a master; every Slurm job of a run is in the registry from the moment
   the adapter returns its job id: `bee_spawn` writes the row (state `queued`, parent, account, job id)
   before it answers the caller, and the job script turns it to `running` before the session's first
   turn, so a satellite that dies in the queue is still cancellable and closable by its row (the
   launcher's `stop_worker_run` already cancels a queued worker by id); submission only through the
   adapter; and a session's row is complete only once its `SessionStart` hook has written the socket path and token (17.2.5), which proves
   the socket is bound and the bridge can reach it.
2. Tier 1 teammates are in-process (A3); the page says a teammate's background work "can't outlive the
   lead's process", and that the teammates themselves end with it is inferred from "in-process" (checked
   in M1). Before its own exit the lead sends each a shutdown request and waits (A4: shutdown can be slow);
   the page lets a teammate "reject with an explanation", so after the grace period, bounded by the
   wall-time margin, the lead exits anyway, its in-process teammates end with it, and work a teammate had
   not written to the task list or to files by then is lost, not orphaned, and is counted in the ledger
   row with the explanation; teammates are never tmux panes (17.2.2).
3. A master's exit path (the launcher's wall-time signal, `--signal=B:TERM@120` as `profile_sh.sh` renders
   it, or the stop file; the playbook's `--signal=B:USR1@600` and `timeout --signal=INT` belong to `-p`
   satellites) tells its satellites to finish within a grace period that fits that margin, then cancels, through the adapter, the job ids
   the registry says are its own and nothing else (one `scancel` per action; never another run's, never
   anything that is not ours).
4. A satellite whose parent's heartbeat lapses asks the super-master for adoption; adopted, it continues
   under the super-master's roster; not adopted within the grace period, it finishes its turn and stops.
5. The super-master's reaper reconciles the registry against one `squeue` per 60 s floor while a run is
   live and against `sacct` at the end; a job the scheduler no longer knows is closed in the registry; a
   job the registry does not know but the run started is impossible by invariant 1 and is written as a
   failure if it ever appears.
6. At run end every registered job is stopped, every row closed, and the counts (started, finished,
   reaped) go into the ledger row; a session closed by the reaper rather than by its parent is an
   INTERVENTIONS failure row with its cause.
7. The hand-off of 17.2.4 never strands a session: the roster moves with the state, and the new holder
   re-parents masters' satellites to their masters, not to itself.

**17.2.7 Compute without limit, windows with limits (R3).** Nodes are not the scarce thing; each account's
five-hour and seven-day windows are. So §4 item 5's caps change meaning rather than disappear: the
per-run subagent and teammate numbers become **per-account window budgets** (G3's token economy, kept per
account) and **per-node sizing** (teammates and subagents at most the allocated cores); the number of
masters is the number of enabled accounts; satellites per master are bounded by the account's remaining
window and by Slurm's own per-user job limits on the partition (Wayne State's `MaxJobs` and `MaxSubmit` per
user: not yet measured, M6). The grid rules are unchanged and are manners, not caps on compute: the login
node runs one scheduler call per action, polling never under 60 s, every job has a wall time, temp is
node-local, nothing of ours under the login node's `/tmp`. Fair share on the lab's partitions is the
scheduler's to enforce; the engine stays under the QoS limits and never retries into them.

**17.2.8 Usage reading and the threshold (the part of claude-swap we keep).** The engine wants, per
account, the five-hour and seven-day fractions and their reset times, read through Claude Code and never
through a token. The switching thread's reading of the status line page (2026-10-04; not yet checked
against the page from this thread, whose page read waits on greg): every status-line command receives JSON
with `rate_limits.five_hour` and `rate_limits.seven_day`, each with `used_percentage` and `resets_at`, on
Pro and Max plans after the session's first response, and the status line runs in interactive sessions
only. So an interactive master under a pseudo-terminal has the reading and a `-p` step does not; bee's
status line records it per account (`~/.beethoven/engine/usage/<label>.json` and the run directory's
`state/usage.json`, `beethoven-research` PR #3). For `-p` the first signal is the `StopFailure` hook with
error type `rate_limit` (hooks page, checked here: the event fires "when the turn ends due to an API
error", its matcher values `rate_limit`, `overloaded`, `authentication_failed` and others; whether it fires
under `-p` is not stated), then the candidates BEE-121 tries in order: the rate-limit fields of
`stream-json` events, `/usage` in a pseudo-terminal session, OpenTelemetry metrics. Trigger (a), the 90 %
threshold, is enabled for masters once the grid check of PR #3's `docs/bee/RUNBOOK.md` shows the fields
arriving on greg's plans; until then, and for `-p` steps throughout, the hand-off is reactive (trigger b).
`windows.log` carries the account label and, when readable, the fractions, so the paper reports
per-account spend.

**17.2.9 Carrying the spent session itself to the next account (greg, 03:23Z: claude-swap's
`--share-history`, "if it could contribute to passing off the state of a running session that is about to
hit its limit to a fresh account").** Allowed, in one shape, as a complement to the saved-state hand-off of
17.2.4 and never in its place. Since PR #3 (the switching thread, 06:38Z) that saved state includes the
guide's six-section hand-off file (17.2.4), which is the first carrier: a few thousand tokens against a
full uncached context, and it works across machines, claude.ai and Claude Code versions; the transcript
resume here is the second, kept for when the conversation itself matters, and still waits on M13. What the pages give: a transcript is a plaintext `.jsonl` under
`<CLAUDE_CONFIG_DIR>/projects/<encoded cwd>/<session id>.jsonl` (the sessions page; the data-usage page:
local, kept thirty days by default, format internal); `claude --resume` takes, in place of a session id,
"the absolute path to a session's `.jsonl` transcript file" and "continues the conversation stored in that
file" (sessions and headless pages); `--fork-session` gives the continuation a new session id, so the file
resumed from is not the file written to; every hook receives `transcript_path`, and `SessionStart` on a
resume adds `context_tokens`, `prompt_cache_likely_expired` and `estimated_cache_write_usd`; `--resume <id>`
searches the projects under the current configuration directory only and refuses a hand-copied duplicate,
so the id form never crosses directories. The shape, one answer with the skeleton thread (its reply to greg
03:27Z; the engine's `CLAUDE.md` D4 and `docs/ACCOUNTS.md` sections 5, 8 and 9 at 24f8a2f, aligned with
this text at d6d7237, both on `beethoven-research` PR #2 after PR #1 merged at 03:29Z as 772df94):
(1) the spent session's own `SessionStart` hook writes its `transcript_path` and session id to a mode-0600
file in the run directory, beside the socket file of 17.2.5 (built in PR #3 as `state/session.json` under
`$BEETHOVEN_RUN_ROOT`, or a laptop project's `.claude/state/`, with the account label and, on a resume or
fork, `context_tokens`, `estimated_cache_write_usd`, `prompt_cache_likely_expired` and
`seconds_since_last_response`: hooks page, checked, v2.1.251 or later), because the path is reported to the session's
own hooks, nothing of ours lists inside a sign-in directory, and a forked session's id is Claude Code's
choice, not the job's, so this is also how the engine learns a forked master's new id (a `-p` step reports
it in its init event as well); (2) on a hand-off the engine passes that
path to the next holder's job, where the one file is bound read-only at a neutral path,
`/handoff/<id>.jsonl:ro`, beside the account's own `/claude` (the skeleton thread's shape), and the next
account's session starts as `claude --resume /handoff/<id>.jsonl --fork-session` under its own
`CLAUDE_CONFIG_DIR` (for an interactive master in front of `claude remote-control`'s arguments, as M13
settles); (3) nothing is
copied, moved or written into any sign-in directory by ours (`bee continue --fork` accepts the recorded
path only when it names a session file in the writing account's own `projects` folder, checked again on
the host before the bind: PR #3's adversarial review found a recorded path to another account's sign-in
file reaching a bind, the one serious hole, closed), the credential is never touched, the spent
account's transcript is not appended to (the read-only bind turns a write into a loud failure rather than a
line in the wrong directory), and the continuation's transcript is expected to land under the new account
as that session's own; (4) the engine's own records (the lease, the task graph, `STATUS.md`, the bus) are
written first and stay the record of truth, as 17.2.4 says: the transcript carries working memory, not
state. This is claude-swap's `--share-history` effect, the session showing up resumable under the other
account, without a shared or copied history directory; a shared `projects/` directory, a copied transcript,
a `--resume <id>` or `--continue` across directories, and any session of another person's account stay
refused (S1, S3, §15.6, D1d). The transcript is greg's own data moving between his own accounts; the
terms-check record of D1d covers it. What it buys: the holder's context, the reasoning in flight and the
task half done continue under the next account, which matters most for trigger (b), where the holder
cannot finish a turn to checkpoint; on (a) and (c) the checkpoint already carries the state and the
transcript adds the conversation around it. What it costs, each measured in M13 before it is built: the
first turn under the new account re-sends the whole transcript uncached, because the prompt cache belongs
to the account (the resume `SessionStart` fields go to `windows.log` at every hand-off; a compaction before
the hand-off keeps it bounded: §15's `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`, per launch `--autocompact <size>`,
per job `CLAUDE_CODE_AUTO_COMPACT_WINDOW`, never `/autocompact`, which writes user settings inside the
sign-in directory (the switching thread's reading of the CLI and settings pages, not yet checked here);
and on the limit itself the
sessions page's "Resume from a summary" offer is Claude Code's own form of the same); the in-process team
does not follow (A4) and the successor re-spawns it from the task list as 17.2.2 says, while satellites are
registry rows and do; a workflow run's saved results do not follow (F4: a fresh session starts the workflow
over), so 17.6's same-account rule for workflow runs stands; a master's Remote Control registers under the
new account, so greg opens claude.ai signed in to that account to see it; a turn cut by the limit resumes
with its interrupted tool call marked as cut off (sessions page); the transcript is written asynchronously
and "may lag" (hooks page), so the path is recorded at the session's start and the file is read only at
the hand-off. Until M13 is on record the hand-off is the saved state alone, and the plan's earlier "never a
resumed Claude Code session" (D1d, 17.2.4, `PROJECT_INSTRUCTIONS.md` version 8) is narrowed to: never under
another person's account, never by `--resume <id>` or `--continue` across directories, never by copying.

**17.2.10 The client view (the desktop thread, 02:54Z; `beethoven-desktop` `docs/EDITIONS.md` section 4).**
Every master and satellite is an hpcworker run folder with a `status.json`, so all three clients (the
extension, the desktop plugin, Beethoven for VS Code) list them without new machinery: `status.json` gains
`account` (the label), `role` (`master` or `satellite`), `parent` (the spawning session) and `lease`
(`{holder, expires_at}`, the worker's self-report of what it last renewed; the store's lease row with its
fencing token stays the record of truth, 17.2.4). That is a contract change, made in hpcworker's
`docs/V11_CONTRACT.md` and the extension's `contract.ts` together, as the split rule requires. A client
shows one tree per account with the lease holder and a "without its master" flag (a satellite whose parent
row is gone), can open a worker and stop it (the gate's `stop`, asked first), and never signs in, switches
accounts, moves the lease or writes to the state directory; the desktop plugin's `worker_list` (its PR #2)
already reads every run folder's `status.json` over sftp and flags a worker silent for five minutes.
Linear: a comment on BEE-187 and the desktop thread's issue.

### 17.3 Rules changed by this section

- §2 **C6** is narrowed again: concurrent use of one person's own accounts, each signed in by that person,
  with one super-master lease at a time, is allowed and logged. Still forbidden: anyone else's account;
  reading, storing, copying or relaying any account's credential (claude-swap's backup is exactly what we
  do not do); usage credits on any account (C7); evading detection; two holders of the lease.
- §7 **D1d** is superseded on one point: not one account at a time but several at once, one holding the
  lease. The terms-check record in D1d stands as a record.
- §14.2 **item 7**'s "never agent teams" is withdrawn (greg, 02:30Z). The cost accepted is the costs page's
  "approximately 7x more tokens than standard sessions when teammates run in plan mode"; the agent-teams
  page gives no multiplier, only "significantly more tokens" scaling "linearly" with teammates, so the
  general figure is not yet measured and is read per account from `windows.log` (17.2.8), bounded per
  account by its window (17.2.7).
- §4 **item 5** (concurrency guardrails) is re-expressed by 17.2.7.
- **BEE-127**'s envelope "one account per user, no account rotation, no pooled tokens" becomes "one
  person's own accounts, each signed in by them; one super-master at a time; no pooled tokens; nothing
  copied".
- The two launcher repositories' `CLAUDE.md` sentence "One person, one account." becomes "One person,
  their own accounts, each signed in by them in its own directory; never anyone else's." (greg: "CHANGE
  THE RULES AGAINST IT IN THIS REPO"); the engine's `CLAUDE.md` says the same, in the skeleton thread.
- §15.3's single submission point (G5-9) is re-expressed: `bee_spawn` is the one submitter, the
  `slurm-operator` role becomes that tool's server, and a teammate's shell never runs `sbatch`; the
  playbook's "at most 4 jobs queued or running" becomes a per-run cap counted across masters, chain links
  and satellites, set from M6 and `windows.log`, with 4 as the default until then; arrays stay at most 200.
- §14.2 item 7's `crossSessionInbound: hold` becomes `accept` for every session that belongs to a run (a
  `hold` never releases); §1's trust-posture row, §7 D1d's definition of done and §11's BEE-150 paragraph
  are amended to match (03:1xZ).
- §7 D1d's and 17.2.4's "never a resumed Claude Code session" is narrowed (03:3xZ, greg's 03:23Z ask):
  between one person's own accounts the spent session continues from its transcript by absolute path with
  `--fork-session`, the file bound read-only (17.2.9, probe M13); still never under another person's
  account, never `--resume <id>` or `--continue` across directories, never a copied transcript or a shared
  history directory. The engine's `CLAUDE.md` D4 and `docs/ACCOUNTS.md` say the same (skeleton thread,
  24f8a2f and d6d7237 on `beethoven-research` PR #2).
- The guard and the managed deny rules refuse `claude auth login` (a sign-in is the student's own sitting;
  `--console` would bill per use, and usage credits are never used, C7) and `claude project purge` (it
  deletes inside the sign-in directory). An account counts as signed in only when `claude auth status`
  says `authMethod: "claude.ai"` for that very directory: measured in a cloud session (Claude Code
  2.1.289), an empty directory answered `loggedIn: true` with `authMethod: "oauth_token"` because a token
  came from the environment (the switching thread, 06:38Z). A project whose own settings would bill another
  way (`apiKeyHelper`, a cloud provider's credential export, a credential variable in `env`) is refused
  before a session starts (C8), as is an `salloc` shell on the login node (§8).
- `/autocompact` is never typed by engine code: under `CLAUDE_CONFIG_DIR` it writes user settings inside
  the sign-in directory; a launch uses `--autocompact <size>`, a job `CLAUDE_CODE_AUTO_COMPACT_WINDOW`; the
  guide's 60 % rule is a status-line hint, never automated (the switching thread's reading).
- Four parts of greg's State Management guide are left out, each recorded in PR #3's
  `docs/bee/STATE_HANDOFF.md`: its alias (it would strand `~/.claude.json`), `/autocompact` (above),
  `--console` sign-in (usage credits, C7), and its credential backup and locks (the credential rule).
- `PROJECT_INSTRUCTIONS.md` version 8 carries the new section 2, section 5 and section 12 wording;
  version 9 the transcript continuation in section 2; version 10 the hand-off file, the status-line
  reading, the sign-in test and the `/autocompact` rule.

### 17.4 Not yet measured (the probes come before the build; each is one experiment in `probe.sbatch`)

- M1. A session under a pseudo-terminal in the lab image, in both forms a master may take (`claude
  remote-control` as the launcher runs it, and plain `claude` with no keyboard, driven only through its
  inbox socket), spawns teammates with `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` (A2 says interactive; it
  does not say attended, and it does not name Remote Control), including a teammate's first Bash call
  under the permission configuration M12 picks, and whether `--continue` brings the team back (it should
  not, A4).
- M2. `/list-agents` on one node lists a session started with a different `CLAUDE_CONFIG_DIR` under the same
  OS user (X2).
- M3. Two Apptainer instances on one node reach each other's sockets (X5 says flatly that a session in a
  container and one on the host cannot). The probe reads each session's `Peer address` row and
  `CLAUDE_CODE_MESSAGING_SOCKET`, records which directory each chose and whether either shows `unavailable`
  (X2), and tests the connection; it assumes no directory and depends on the `/tmp` bind.
- M4. How the usage limit presents in `-p` output and in a pseudo-terminal session; whether the status
  line's `rate_limits` fields arrive on the grid on greg's plans (PR #3's `docs/bee/RUNBOOK.md` grid check;
  interactive sessions only); and whether any fraction is readable from a `-p` step at all (BEE-121;
  17.2.8).
- M5. Remote Control from two masters of one account on two nodes gives them each other in the listing
  (X4); the launcher already registers Remote Control from `sbatch` (measured 2026-09-29).
- M6. Wayne State's per-user `MaxJobs` and `MaxSubmit` on `reqp`, `secp` and the GPU partitions.
- M7. The hop is measured yes on Wayne State (2026-09-28: Beethoven for VS Code ssh'd through the login
  node to a compute node of its own job with a `ProxyJump` `Host` entry, about 23 s of each connection on
  the node's side; `beethoven-vscode` `docs/CHECKPOINT_2026-09-28.md` item 7; the desktop thread, 02:54Z).
  What stays unmeasured, the desktop thread's laptop check 14: what Desktop installs on a compute node and
  whether it starts, expected no on Wayne State (CentOS 7, glibc 2.17, D6), and on a site whose nodes run
  the binary whether it can be pointed at an account's `CLAUDE_CONFIG_DIR`.
- M8. Moot with a key: a key alone signed in to the login node under `BatchMode` with no one-time code (the
  same checkpoint, item 2), and Desktop's SSH dialog takes an identity file; the one-time code arises only
  for a password sign-in (the desktop thread, 02:54Z).
- M9. The team directories (`teams/`, `tasks/`) follow `CLAUDE_CONFIG_DIR` rather than `~/.claude` (A3 names
  `~/.claude`); it matters for where Claude Code's own writes land, not for ours.
- M10. Worktree creation, `git worktree remove` and a 50-file edit on CephFS under `.claude/worktrees/`
  versus a `WorktreeCreate` hook on node-local disk, timed in the probe job (17.6).
- M11. Whether a `-p` prompt can start a saved workflow by name under an allow rule `Workflow(<name>)`, and
  whether a run's saved results replay after `claude --resume` in a later job on another node of the same
  account (17.6).
- M12. A teammate's permission prompt in a socket-driven lead with no keyboard, under each candidate
  configuration of 17.2.2 (allow rules pre-approved in permission settings, auto mode,
  `--dangerously-skip-permissions`): which one lets the team work unattended with the PreToolUse guard
  still enforced (A5).
- M13. `claude --resume /handoff/<id>.jsonl --fork-session`, the transcript bound read-only at that path,
  under a `CLAUDE_CONFIG_DIR` other than the one that wrote it: in `-p`, under a pseudo-terminal as plain
  `claude`, and in front of `claude remote-control` (whether that subcommand reads `--resume` at all is not
  on record); where the continuation's transcript is written; that the source file is unchanged after the
  run (the read-only bind turns a write into a loud failure); the resume `SessionStart` fields
  `context_tokens`, `prompt_cache_likely_expired` and `estimated_cache_write_usd` on the first turn; and a
  turn cut by a limit hit, provoked once on purpose, resuming with its interrupted tool call marked as cut
  off; and which Claude Code version added the path form of `--resume` (the page does not say; the lab
  image's version is what matters) (17.2.9).

### 17.5 Linear and order

G5 (`P-BEE-5`, linked to `beethoven-agents` since the split, D2): BEE-185 becomes the account registry and
per-account sign-in (17.2.1; the engine half built in `beethoven-research` PR #3 and moving to agents, In
Progress; the framework's `--account` not yet); new BEE-186 the
bus and the socket bridge (17.2.5, with probes M2 and M3); BEE-187 the registry, heartbeats and reaper
(17.2.6); BEE-188 usage reading and the threshold switch (17.2.8, with BEE-121 and probe M4, whose first half, the
limit text, is already experiment 2 of §15.6's Phase 0 probe; the pseudo-terminal case and the fractions
are added to it; the interactive half is answered by the status line pending the grid check, the `-p`
half open, 06:38Z); BEE-189 the super-master
lease and hand-off (17.2.4) and the transcript continuation of 17.2.9 with probe M13 (engine side 24f8a2f and
d6d7237, `beethoven-research` PR #2; M13's exact commands in PR #3's `docs/bee/RUNBOOK.md`, greg's to run); BEE-190 masters as interactive leads, satellites as Slurm jobs, teams of teams
(17.2.2, 17.2.3), carrying probes M1, M5, M6 and M9 into Phase 0's probe job. F1 (`P-BEE-11`): D6, M7 (its remaining half,
check 14), M8 and the client view of 17.2.10 to the desktop thread's issue; the `status.json` fields are a
BEE-187 comment and a contract change in both launcher repositories. Order inside the build (§5): the probes join Phase 0 (they cost one allocation each and
decide the shape); the lease, registry and bus are the first G5 deliverables, before fan-out (BEE-150),
because fan-out without them orphans sessions, which R7 forbids.

P0 (`P-BEE-2`): BEE-192, the build side of 17.6 (a worktree per stream, the four saved workflow scripts, the
hook `cwd` rule), High, related to BEE-110, BEE-102 and BEE-190; the engine side of 17.6 is a comment on
BEE-190, the never-cross-accounts rule for workflow runs a comment on BEE-189, the hook paths a comment on
BEE-110. BEE-191 (G4, the desktop thread) records the VS Code edition's API-key overflow (§2 C8). The
corrections of 03:1xZ (the unattended permission configuration, M12; the `SessionStart` hand-over of socket
path and token; `crossSessionInbound: accept` for every satellite) are comments on BEE-190 and BEE-186.
After the split (D2) BEE-185 to 192 and the guard issues BEE-123 and BEE-124 link to `beethoven-agents`;
17.6's build side (BEE-192) to `beethoven-qa`, whose plugin carries the `stream` agent and the saved
workflows; the split's own P0 issues are BEE-193 to BEE-197 (§6).

### 17.6 Worktrees and workflow scripts: the parallel parts of the build and of the engine (greg, 2026-10-04T02:37Z)

greg, in the skeleton thread: "also incorporate this https://code.claude.com/docs/en/worktrees and this
https://code.claude.com/docs/en/workflows for bootstrapping and writing the parallal parts of the
ecosystem". Both pages read at 02:58Z. The facts that bind the design, then the two uses: how the build
itself is parallelised, and how the engine's own parallel parts use them at run time.

**Worktrees** (`code.claude.com/docs/en/worktrees`):
- W1. `claude --worktree <name>` (or `-w`) creates `.claude/worktrees/<name>/` at the repository root on a
  new branch `worktree-<name>`; an unnamed worktree gets a generated name. `.claude/worktrees/` belongs in
  `.gitignore`.
- W2. "Interactive runs require workspace trust ... Non-interactive runs with `-p` skip the trust check, so
  `claude -p --worktree` proceeds without it."
- W3. Cleanup is interactive: on exit Claude removes a clean unnamed worktree, prompts for a named or dirty
  one. **"Non-interactive runs with `-p` have no exit prompt, so Claude doesn't clean up their worktrees"**,
  and the lock it took stays until a later session's stale-lock sweep; `git worktree remove` (and `unlock`)
  is the manual way.
- W4. Subagents run in their own worktree with `isolation: worktree` in the agent definition (or "use
  worktrees for your agents"); a subagent worktree with no changes is removed at once, one with changes
  "stays on disk until the periodic sweep ... can remove it without losing work", and that sweep runs on
  `cleanupPeriodDays`, the setting §15.6 struck because it deletes inside the sign-in directory.
- W5. Isolation is enforced, not advisory: edits, commands, and git redirects into the main checkout are
  blocked by four checks, the last of which (command shape) "You can't turn ... off"; the same checks cover
  every subagent of the isolated session.
- W6. `worktree.baseRef` is `"fresh"` (the remote's default branch, fetched if older than 24 h) or `"head"`;
  never a named branch. `--worktree "#1234"` branches from a pull request.
- W7. A worktree is a fresh checkout: no gitignored files, so no `.pixi/` environment; `.worktreeinclude`
  copies gitignored files in (the page's example copies `.env` and a secrets file, which our secrets rule
  forbids us to have in the first place).
- W8. A `-p` session resumed with `--continue` or `--resume` returns to its worktree; the transcript
  follows the worktree (recorded under the new working directory). A resume refusal in `-p` is a `result`
  with `startup_failure_reason` `worktree_unverified` or `worktree_resume_refused`.
- W9. **Hooks: `${CLAUDE_PROJECT_DIR}` stays at the project root; the hook input's `cwd` is the worktree
  root.** Our pre-push gate hook and the PreToolUse guard must read `cwd`, not the project dir, to act on
  the worktree (BEE-110, BEE-102).
- W10. `WorktreeCreate` and `WorktreeRemove` hooks replace the git logic entirely, "including placing
  worktrees somewhere other than `.claude/worktrees/`"; a hook-made directory must sit outside any
  repository, and `.worktreeinclude` is then not processed.
- W11. Claude Code refuses to create a worktree when `.claude`, `.claude/worktrees` or the worktree
  directory is a symlink. The Desktop app's "parallel sessions with Git isolation" is this same worktree,
  chosen at session start. Shared with the main checkout: the `.git` directory, project-scope plugins,
  permission approvals (saved to the main checkout's `settings.local.json`), untracked skills, agents and
  commands by read-through.
- W12. Not mentioned: remote hosts or SSH sessions, Slurm, shared filesystems, Git LFS content comes as
  pointer files when the filter is repository-local (`git lfs pull` inside the worktree).

**Dynamic workflows** (`code.claude.com/docs/en/workflows`):
- F1. A workflow is a JavaScript script that orchestrates subagents; "Claude writes the script for the task
  you describe, and a runtime executes it in the background"; "dozens to hundreds of agents per run";
  results stay in script variables, not Claude's context; "Resumable in the same session". Available on
  all paid plans (Pro: a `/config` row).
- F2. Opt-in: the keyword `ultracode` or "use a workflow" in a prompt the person types, or `/effort
  ultracode` for the session (`claude --effort ultracode` also sets `xhigh`). **"It doesn't start a workflow
  when it reaches the session another way: a prompt passed with `-p`"**, an unstamped SDK prompt, a
  scheduled task, a webhook. Yet "Workflows are available in the CLI, the Desktop app, the IDE extensions,
  non-interactive mode with `claude -p`, and the Agent SDK", and in `-p` the Workflow tool call "runs ...
  through the same permission evaluation as the rest of the session": an allow rule `Workflow` or
  `Workflow(<name>)`, auto mode's classifier, bypass mode, a `PreToolUse` hook, or the host's
  permission tool lets it start. Whether a `-p` prompt can start a saved workflow by name is not yet
  measured (M11).
- F3. Limits: "Up to 16 concurrent agents by default, fewer when Claude Code has fewer CPUs available,
  including inside a CPU-limited container"; `CLAUDE_CODE_WORKFLOW_MAX_CONCURRENT_AGENTS` 1 to 256 (v2.1.269
  or later); 4,096 items per `parallel()` or `pipeline()`; 1,000 agents per run; a fan-out's matching
  agents start up to 5 s after the first to read its prompt-cache prefix; a workflow agent's cache holds
  five minutes by default "including on a Claude subscription" (`subagentPromptCacheTtl: 1h`).
- F4. Resume: "Claude Code replays the run in the order agents started"; completed agents return saved
  results; the first agent whose prompt differs, and every agent after it, runs again; a failed agent and
  everything after it runs again. Within the same session; a session resumed with `claude --resume` can
  replay; a fresh session "starts the workflow over as a new run"; no saved results gives `nothing to
  resume`.
- F5. **Usage limit: "The run pauses only when all of these hold; when one doesn't, the affected agent fails
  instead: the session is interactive and signed in with a claude.ai subscription. A run doesn't pause in
  non-interactive mode with `claude -p` or the Agent SDK, in a background session, or in a Remote Control or
  agent team teammate session"**; `autoContinueAtUsageLimit` on; reset within 24 h; at most two waits.
- F6. Saved workflows: `.claude/workflows/` in the project (shared through the repository) or
  `~/.claude/workflows/` (under `CLAUDE_CONFIG_DIR` when set), run as `/<name>` with `args`; plugins ship
  them as `/<plugin>:<name>`; the `meta` block is a literal; `Date.now()`, `Math.random()` and `new Date()`
  throw so a relaunch repeats the same calls; no `import()`, no filesystem from the script. The
  `/workflow-authoring` skill (v2.1.248 or later) is the authoring reference.
- F7. Size guideline `small`/`medium`/`large`/`unrestricted` (default `medium`); a `Large workflow` warning
  past 25 agents or 1.5 million projected tokens, not shown with ultracode; "On a subscription plan those
  tokens draw on your usage limits, so a session with ultracode on reaches a session or weekly limit
  sooner". In auto mode the script's `agent()` prompt "doesn't count as a request from you".
- F8. Not mentioned: Slurm, agents on other machines, agent teams inside a workflow (the page's table
  contrasts the two: the lead decides turn by turn, the script decides).

**Use 1: parallelising the build (bootstrapping).** The build streams of §5 are already parallel threads;
from here each stream that edits a repository works in its own worktree of that repository (`--worktree
<stream>`, branch `worktree-<stream>`, which the PR convention of §3 item 7 turns into a pull request
opened ready, gated by the pre-push hook and merged by its checks), so two streams never edit one
checkout. Repeatable build procedures become saved workflow scripts in `.claude/workflows/` of
`beethoven-research` (since the split, `beethoven-qa`'s plugin, D2), shared through the repository and run as commands: `review-changes` (per-file
finders, adversarial verifiers, one ranked summary, the pattern this very section was checked with),
`fix-until-green` (run `pixi run gate`, fix, repeat until it passes or two rounds make no progress),
`migrate-isolated` (one agent per file in its own worktree, `isolation: 'worktree'`, verified per item),
`probe-synthesis` (readers over the probe job's outputs, refuters, one measured-facts file). Every run's
agent count, token total and elapsed time go into the ledger row (the methods paper counts them;
§12). The size guideline stays `medium` in cloud threads unless greg sets otherwise; `large` is for the
grid, where cores are plentiful and the window is the limit (17.2.7).

**Use 2: the engine's parallel parts at run time.** Three mechanisms, each for a shape of work:
- *Tier 1 teammates* (17.2.3) for work that needs discussion between peers: competing hypotheses, a review
  from several lenses, a module split across owners; interactive masters only (A2).
- *Workflow scripts inside `-p` steps* for fan-outs over many items where the orchestration should be code
  and repeatable: per-corpus checks of G6, per-file audits of G1, figure and table regeneration of G2, the
  CLAIM table of §16.4. A step runs a saved workflow by name through the permission path of F2 (an allow
  rule `Workflow(<name>)` in the step's `--settings`), with `CLAUDE_CODE_WORKFLOW_MAX_CONCURRENT_AGENTS` set
  to the allocation's cores (F3), `subagentPromptCacheTtl: 1h`, and the run id written to the step's
  record. Agents that edit run with `isolation: 'worktree'` (W4).
- *Satellites* (17.2.3) for work that needs its own node or its own account's window.
Two consequences of the pages, written as rules:
- **Worktree hygiene is ours, not the sweep's.** `-p` runs clean nothing up (W3) and subagent worktrees
  with changes wait for `cleanupPeriodDays` (W4), which the engine does not rely on. So every step that
  created worktrees removes them at its end (`git worktree remove`, `unlock` first if locked) after
  pushing the branch it wants kept; the reaper (17.2.6) lists `git worktree list` of the run's clone at run
  end and reports any left. The run's clone lives on the lab volume; worktrees under `.claude/worktrees/`
  are many small files on CephFS, so a `WorktreeCreate` hook (W10) that places them on node-local disk
  (`/tmp/$USER/hpcworker_$SLURM_JOB_ID/wt/<name>`, outside any repository, pushed before the job ends, swept
  with the node) is the shape to measure (M10); the image carries the Pixi environment, so a fresh checkout
  needs no `pixi install` (W7). `.claude/` and `.claude/worktrees/` in the clone are real directories, never
  links (W11).
- **A workflow run never crosses accounts.** Saved results live in the session's directory under the
  account's sign-in directory (F4), so the super-master hand-off (17.2.4) happens between steps, never
  inside a run. In `-p` a run that hits the limit fails its agents instead of waiting (F5); the step records
  the run id and session id, and the same account's master resumes that session after the reset
  (`claude --resume <session>` in the same directory, then "relaunch the workflow": completed agents replay
  from cache, F4); only if that account stays spent past the step's deadline does another account re-run
  the step from scratch, which the ledger records as a repeated unit of work. The hook paths rule (W9)
  applies to every gate and guard hook the engine installs.

Probes added to §17.4: **M10** worktree creation, `git worktree remove` and a 50-file edit on CephFS under
`.claude/worktrees/` versus a `WorktreeCreate` hook on node-local disk, timed in the probe job; **M11**
whether a `-p` prompt can start a saved workflow by name under an allow rule `Workflow(<name>)`, and whether
a run's saved results replay after `claude --resume` in a later job on another node of the same account.
Linear: BEE-192 in P0 for the build side (worktree per stream, the four saved scripts, the hook `cwd` rule)
and comments on BEE-190 (the engine side), BEE-189 (runs never cross accounts) and BEE-110 (hook paths).

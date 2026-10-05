# Linear

Linear is where the project's work is tracked; this folder only points at it and keeps a snapshot
for a session that has not signed in to Linear yet.

- Workspace **ashl3y** (`https://linear.app/ashl3y`), one team, **Beethoven**, issue key `BEE`.
  BEE-1 to BEE-97 are the launcher's backlog from before the engine (BEE-5 to BEE-97 archived
  on 2026-10-03); the engine and the newer directions start at BEE-98. `plan/LINEAR_BREAKDOWN.md`
  is the breakdown with acceptance criteria, `memory/linear-engine-structure.md` the structure.
- Connect it: in a Claude Code session in this clone, `.mcp.json` names Linear's own MCP server
  (`https://mcp.linear.app/mcp`); the first Linear call opens Linear's sign-in in the browser. In
  the claude.ai app, connect Linear under Settings, Connectors. No Linear key is made or stored.
- [ISSUES.md](ISSUES.md) is a snapshot of every issue that is not archived, by project, with its
  status and labels (titles only, no descriptions or comments); `issues.json` holds the same rows.
  The hand-off thread refreshes it with the copy from the project when Linear is reachable. Linear
  is the record: when the two differ, Linear is right and the snapshot is old.

## Projects of the team

| Project | Id | What it covers |
| --- | --- | --- |
| P0 Foundations & Open Decisions | P-BEE-2 | The ground-truth probe, the deterministic substrate and the decisions that gate all engine work |
| G1 Formally Verified Contract-Driven Code | P-BEE-7 | Contracts, runtime types, CrossHair and Z3, schema-aligned parsing, the gate (beethoven-qa) |
| G2 REFORMS Reproducibility | P-BEE-8 | Run identity, the clean-tree gate, the reforms contract, bootstrapped intervals, energy, patient-level splits (beethoven-research) |
| G3 Token Economy & Context Control | P-BEE-3 | Lazy tools, cache, compaction, state hooks, quota-window pacing on the flat-rate subscription (beethoven-agents) |
| G4 Legal & Security Compliance Boundaries | P-BEE-4 | The guard, the managed settings, defensive work only on the grid, credential compliance (beethoven-agents) |
| G5 Storage, Crash Resilience & Orchestration | P-BEE-5 | Node-local scratch, the session store, orchestration, concurrency caps (beethoven-agents) |
| G6 Medical Data Calibration & Tensor Integrity | P-BEE-6 | DICOM to Hounsfield units, MONAI spatial integrity, preprocessing (beethoven-research) |
| G7 Automated Dissemination & Publication | P-BEE-9 | Lineage records, the paper's macros, DOIs and model cards, behind a human Publish click (beethoven-research) |
| M Process Measurement & Research Report | P-BEE-10 | The build ledger and the methods paper's scaffold (this repository's `ledger/`) |
| F1 Claude Desktop Extension (native SSH) | P-BEE-11 | beethoven-desktop |
| F2 Command Center, Project Graph & Peeking Claude | P-BEE-12 | The jobs view, the dependency graph and the read-only summariser in the extension |
| R Imaging Data Migration & Catalog | P-BEE-13 | Copying greg's imaging data to CephFS with checksums (never deleting) and its catalog on the grid |
| O Outreach & Adoption | P-BEE-14 | The promotional texts (`promo/`) |
| S First study: fluoroscopy detection under domain shift | P-BEE-15 | The spine study, the engine's first real run (`plan/SPINE_FIRST_STUDY.md`) |

The repository in brackets is where most of a project's work lands; it is a guide, not a rule.

## How the project uses it

- Commits, pull requests and documents name the issue they serve by its key (beethoven-vscode's
  5.0.0 commit names BEE-191; the repositories' `CLAUDE.md` files cite issues the same way).
  Linear's suggested branch name for each issue is in `issues.json` (`gitBranchName`).
- Decisions are issues with the label `decision`; greg's words go on the issue when he decides.
- Never a secret, a credential, a token or patient data in an issue, a comment or a document.
- Statuses drift: on 2026-10-04 the hand-off found BEE-155 and BEE-156 In Review though merged,
  BEE-110 in Backlog though built, and BEE-192 in Backlog though partly built
  (`state/claude_context.md` section 3).

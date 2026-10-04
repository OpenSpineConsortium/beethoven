# CLAUDE STATE SERIALIZATION

**Timestamp:** 2026-10-04T21:25Z **Phase:** Implementation

Project-wide hand-off of the Beethoven project (claude.ai project "beethoven", organisation OpenSpineConsortium, maintainer greg: GitHub Gregory-Schwing-MD-PhD, grid login go2432). Written by the thread "Write the hand-off state file" on greg's ask of 18:34Z, in the six-section shape bee builds from his "Claude CLI State Management" guide. Read `HYDRATE.md` first for how to use it; per-repository detail is in `repos/<repository>.md`, every decision with its time in `DECISIONS.md`, every thread in `THREADS.md`. GitHub, the sessions and the project files were checked at 19:36-20:22Z, and nine independent checkers re-read 707 claims against them (48 corrected); the desktop thread's pushed branches and staging folder were checked at 20:32-20:33Z, and its 20:58Z changes (base design, VS Code 5.0.0 hold, `RULESETS_TOKEN` reach) by three independent checkers at 21:15-21:20Z; whatever says "not yet measured" or "unverified" was not checked.

## 1. Primary Objective

Two halves share one grid (Wayne State's, Slurm, CentOS 7 login node), one container discipline and one set of non-negotiables:

- **The launcher** makes a student's own Claude Code worker, running as a Slurm job in the lab's Apptainer image, usable from claude.ai through Claude Code Remote Control. Its parts are hpcworker (the cluster side and the contract) and three clients: the Chrome extension (with its native bridge), the Claude Desktop and Claude Code plugin, and the VS Code edition.
- **The engine** is an autonomous prompt-to-paper research engine: headless `claude -p` steps and interactive masters as Slurm jobs inside a hermetic image, orchestrated by Metaflow, turning a research prompt into a verified, reproducible, archived result. It has three repositories: beethoven-qa (how code is written and proven), beethoven-agents (how agents run on the grid) and beethoven-research (what is computed). Its goals are G1 contract-verified code, G2 REFORMS, G3 token economy and pacing, G4 legal and security boundaries, G5 storage and orchestration, G6 medical calibration and G7 publication behind a human click. The first real run is the spine study: vertebral-body detection on real fluoroscopy under domain shift (BUILD_PLAN section 16).
- The build and every run are measured for a methods paper. Every unit of work is a ledger row, and every human intervention is logged when it happens.

## 2. Architectural Decisions & Constraints

**Hard rules (each binds every repository, thread and tool of greg's; full wording in each repository's CLAUDE.md):**
- No API key anywhere; greg (13:27Z) calls it "the only fundamental rule of this software". This means no Console key, no `apiKeyHelper`, no Bedrock, Vertex or Foundry route, no `ANTHROPIC_BASE_URL` gateway, and no CI that runs Claude Code on a stored key or token. It covers his maintainer tooling too, including Copilot review and claude-code-action.
- Usage credits are never used, by anyone, for anything. A spent window is waited out.
- Everything that calls Claude runs on a person's own flat-rate subscription through Claude Code's own sign-in. Only `claude auth status` with authMethod `claude.ai` counts as signed in.
- Never read, store, copy, print, relay or export a Claude credential. Never `claude auth logout`, and never `setup-token` or `CLAUDE_CODE_OAUTH_TOKEN`.
- No secret ever goes in argv, logs, job files, `sbatch --export`, the ledger, Linear, memory or these files.
- No code runs on claude.ai and nothing intercepts it. No remote code.
- Nothing is deleted outside a run's own directories and node-local temp. Destructive commands refuse under an agent marker or a non-terminal stdin.
- Anything that runs a container, a scheduler call or Claude Code runs in a Slurm job on a compute node: never on the login node, a laptop or a cloud session.
- Polling no faster than 60 s; every job has a wall time; node-local `/tmp/$USER` for temp, because Wayne State's `$TMPDIR` is CephFS.
- Patient data stays on the grid; split labels are pseudonyms; a human Publish click comes before any Zenodo or Hugging Face release; branch `L6_Class` of spinesurg-ct-nnunet stays private.
- greg's home tokens (`.hf_org_token`, `.hf_osc_token`, `.kaggle`, `.wandb`, `~/.gdrive_token`) are never read.
- Names and versions: the public name is Beethoven, with the trademark sentence; versions are integers; never the p-word (say origin, source or record).

**Repositories and dependence:**
- Launcher: `OpenSpineConsortium/hpcworker` is canonical for the contract (`docs/V11_CONTRACT.md`, `V12_CONTRACT.md`) and the site profiles. The clients `beethoven-extension` and `beethoven-desktop` mirror the contract (`contract.ts`) and vendor the profiles as data (`pull.sh`). `beethoven-vscode` does neither: it still runs its own grid scripts under `grid/` (grid scripts 8), a leftover of its being first (desktop thread 20:17Z).
- Engine: qa <- agents <- research is the only direction. Each consumer carries qa as a pinned copy at `vendor/beethoven-qa/` (ORIGIN `ref: v1.0.0`, commit 16415b40e6bb) and never edits it or the four kit files.
- greg's own study repositories, spinesurg-ct-nnunet and u251-xenograft-rat-RNASeq-study, are read-only here.
- **beethoven-base (greg, 20:04:55Z):** "migrate the common codebases to a separate repo, beethoven-base, and just have the beethoven-vscode, beethoven-extension, and beethoven-desktop extensions contain their specific unique code", so a feature added to the base reaches all three. greg created the repository at 20:25Z. The desktop thread's design (20:58Z, not yet written up in `/mnt/project-files/base/`, which is empty): each edition carries a pinned copy of the base in its own source tree, checked against an ORIGIN record by a check that needs no secret, as beethoven-agents carries beethoven-qa; no edition fetches the base and none holds a token for it. The VS Code edition moves onto hpcworker as a late step (its 7.0.0). Details and greg's decisions: `repos/beethoven-base.md`.
- A possible fourth repository holding the grid rules as data was floated at 15:19Z and is not decided; the base design may take it in (`plan/REPO_SPLIT.md` section 2, three-repo thread's).

**Accounts (D4, greg 02:30Z and 03:23Z):**
- Several of greg's own accounts run at once. Each has one sign-in directory, `$HOME/.beethoven/accounts/<label>/claude`, selected by `CLAUDE_CONFIG_DIR`; `$HOME/.beethoven/claude` is the account `main`.
- There is one master job per account and one super-master lease. The hand-off goes first by state file, then by a read-only `--resume <transcript> --fork-session`. The fork is built for bee's interactive switch (`bee continue --fork`) and stays the second choice; the lease's hand-off will not use it until probe M13 is on record.
- Nothing copies, moves or links a credential.
- The launcher's CLAUDE.md line "One person, one account." is stale against D4 (branch `claude/project-thread-2udoqz`, unmerged and conflicting).

**How changes land:**
- PRs open ready for review, never as drafts, with greg asked for review but not blocking. The gate runs before every push.
- beethoven-qa, beethoven-agents and beethoven-desktop merge themselves when the required checks pass (automerge plus rulesets as code, applied with the organisation secret `RULESETS_TOKEN`). beethoven-research has done the same since PR #2 (03:44Z); PR #4 alone needed greg's hand merge (19:34Z), because it renamed the required check, and its merge re-applied ruleset 24440691 with the new gate name at 19:34:23Z.
- hpcworker, beethoven-extension and beethoven-vscode have no ruleset and no automerge workflow, so every PR there is greg's hand merge; the setting Allow auto-merge is already on in hpcworker and beethoven-extension and off in beethoven-vscode. Sessions cannot write `.github/workflows/` files in hpcworker or beethoven-extension; greg copies desktop's three files there.
- Sessions cannot create repositories or push tags; greg does both by hand.
- A merge made by auto-merge (github-actions) starts no CI run on main, so the head of main in qa and desktop has no check runs of its own; its tree equals the PR head whose checks passed.

**Ownership:**
- One thread owns each area: the desktop thread (desktop, VS Code, and for the key sweep, the signed install and the store upload, hpcworker and extension); the three-repo thread (qa, agents, research); the replan thread (`plan/*.md` and Linear); this thread (`state/`).
- Another thread hands a change to the owner through the coordinator. Details are in `THREADS.md`.

**Metering:**
- Every thread is a Claude Code cloud session on greg's plan.
- Opus 5.5 has been the default since 18:40Z. Fable 5.1's weekly limit was spent at about 18:36Z, with reset 2026-10-08 11:00Z; the replan thread is still set to Fable.
- greg's $250 is the cloud-session promotion: claim by 2026-10-07 23:59 PT; it expires 2026-11-04. It is not usage credits.
- Grid jobs draw on neither the promotion nor usage credits.

**Settled this week, in brief (all times and records in `DECISIONS.md`):**
- 10-03 23:09Z: D1, D2, D3.
- 01:12Z: no usage credits.
- 02:11Z: no human gate on merges.
- 02:30Z and 03:23Z: D4.
- 04:52Z: the three-repo split; the 13:19Z card kept research.
- 13:27Z: no API key anywhere.
- 15:41Z: signed install, Option B, with a Mac package and the Rust bridge, plus Azure Artifact Signing.
- 16:23Z: the first research module is the split check.
- 16:24Z: no sign-out on a fresh grid sign-in.
- 18:40Z and 19:26Z: Opus 5.5.
- 19:36Z: the store upload runs from his Mac with the Google sign-in saved there; the listing stays private.
- 19:45Z: beethoven-qa release v1.0.0; the three-repo split is finished.
- 20:04Z: beethoven-base, the shared code of the three client editions (greg created the repository at 20:25Z; the desktop thread's design of 20:58Z gives each edition a checked pinned copy and no token).
- 20:14Z: "I set my RULESET token to all repos visibility, so i dont mind creating secrets". A Claude or Anthropic key still never goes anywhere. The base design that followed needs no read token; its one optional credential is `BASE_PROPAGATE_TOKEN`, held only in beethoven-base, for opening "take the new base" PRs. `RULESETS_TOKEN` is not settings-only and must never be used for code: its Administration write permission also adds deploy keys (which read and write code), changes visibility and adds collaborators, and as an organisation secret for all repositories any workflow there that names it can read it (GitHub's permissions table and Actions secrets pages, checked 21:20Z). qa's CLAUDE.md still names `RULESETS_TOKEN` as the only secret a workflow uses.
- 20:58Z to 21:00Z: VS Code 5.0.0 is on hold (desktop thread): its grid scripts 8 break the deletion rule and hpcworker's sign-in and access rules (`repos/beethoven-vscode.md`).
- 21:10Z: VS Code keeps its minimum at 1.100; `@types/vscode` was pinned back to match (greg's card; PR #7 merged 21:16Z).

**Tools in a project thread:**
- `gh` works over REST only.
- The pixi binary lands at `~/.pixi/bin`, which is not on the Bash tool's PATH.
- Memory lives at `/tmp/claude/memory/team/silo/` and must stay under 16 KB, one fact per file.
- The ledger format is in `/mnt/project-files/ledger/README.md`.

## 3. Files Modified & State

| File Path | Status | Key Modifications / Purpose |
| --- | --- | --- |
| OpenSpineConsortium/hpcworker @ main 20e2e97 | Complete | Framework 17: subscription-only sign-in, no sign-out; not yet on the grid; the queue report pushed as branch b35952a with no PR (`repos/hpcworker.md`) |
| OpenSpineConsortium/beethoven-extension @ main a7db369 | Pending | 14.0.0 on main; 15.0.0 (signed bridge installers, store upload) pushed as branch `claude/project-thread-fx3wkp` d6db850 with no PR; the Mac release command is in the staging folder (`repos/beethoven-extension.md`) |
| OpenSpineConsortium/beethoven-research @ main 8dd5be2 | Complete | The slim pipeline with the patient-level split check; PR #4 merged by greg 19:34Z under the renamed required check (`repos/beethoven-research.md`) |
| OpenSpineConsortium/beethoven-qa @ main 16415b4 | Complete | Release v1.0.0, published by greg 19:45:29Z on 16415b4; both consumers' pinned copies match it (`repos/beethoven-qa.md`) |
| OpenSpineConsortium/beethoven-agents @ main 0de7913 | Complete | Image recipe, guard, bee; image never built on the grid; lease, registry, bus not built (`repos/beethoven-agents.md`) |
| OpenSpineConsortium/beethoven-desktop @ main bc75c09 | Complete | 1.0.0, twelve tools, `forbidden.mjs`; 15 laptop checks not yet measured (`repos/beethoven-desktop.md`) |
| OpenSpineConsortium/beethoven-vscode @ main cc76efd | Pending | 5.0.0 merged but on hold (grid scripts 8 hazards; a grid scripts 9 fix rides the account-setting PR); greg merged Dependabot #1, #3, #4 (20:58-20:59Z) and the `@types/vscode` pin-back #7 (21:16Z); Dependabot #2 (mocha 12.0.3) open and mergeable; the `beethoven.account` setting on branch aa44696 with no PR (`repos/beethoven-vscode.md`) |
| OpenSpineConsortium/beethoven-base | Pending | Created by greg 20:25Z; only his README (desktop thread's clone; this session cannot read it). Design done in the desktop thread (20:58Z), written to the staging folder, not yet to `/mnt/project-files/base/`; three decisions for greg (`repos/beethoven-base.md`) |
| Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet @ L6_Class 465bec6 | Complete | Read-only pointer (`repos/spinesurg-ct-nnunet.md`) |
| Gregory-Schwing-MD-PhD/u251-xenograft-rat-RNASeq-study @ master b110c97 | Complete | Read-only pointer (`repos/u251-xenograft-rat-RNASeq-study.md`) |
| /mnt/project-files/plan/BUILD_PLAN.md and the other plan files | Pending | Govern the build; owned by the replan thread; BUILD_PLAN last folded at 14:13Z, so later decisions live in `DECISIONS.md`, `plan/REPO_SPLIT.md` (three-repo thread's, current to 19:47Z), the threads and memory |
| /mnt/project-files/ledger/LEDGER.md, INTERVENTIONS.md, BOUNDARY.md | Complete | The methods-paper record; append-only, re-read before appending |
| /mnt/project-files/state/ | Complete | This hand-off: `claude_context.md`, `HYDRATE.md`, `DECISIONS.md`, `THREADS.md`, `repos/*.md` |
| /tmp/claude/memory/team/silo/MEMORY.md | Pending | Shared project memory, kept by the coordinator; it carries the three 20:58Z changes (coordinator, 21:03Z) |
| Linear workspace ashl3y, team Beethoven | Pending | BEE-98 onward; BEE-155 and 156 read In Review though merged; BEE-110 Backlog though built; BEE-192 Backlog though partly built (qa's stream agent and three workflow scripts exist; its four named scripts and probe M10 do not); BEE-185 and 189 predate the fork decision |

## 4. Completed Milestones

1. 2026-10-03: the seven-goal rewrite, BUILD_PLAN, Linear seeded, the launcher split into hpcworker and beethoven-extension (18:48Z), and the decisions D1 to D3.
2. 2026-10-04 early: beethoven-research skeleton (PR #1 03:29Z, PR #2 the first merge decided by tests alone, 03:44Z); rulesets live in research and desktop; desktop 1.0.0 with PRs #1 to #3; bee (account switching and the six-section hand-off) in research PR #3, 07:06Z.
3. The no-key sweep: greg merged VS Code PR #5 (5.0.0, 13:27Z) and #6 (17:05Z), hpcworker PR #1 (16:35:45Z) and extension PR #1 (16:35:58Z); desktop PR #4 merged itself (15:36Z); the replan thread fixed the plan files itself (14:14Z). Then framework 17 with no sign-out, hpcworker PR #2, merged by greg 18:13Z.
4. The three-repo split is complete. beethoven-qa 1.0.0 went through two adversarial reviews (46 and 21 findings fixed; PR #1 13:42Z by greg, PR #2 self-merged 15:46Z), and greg published release v1.0.0 on 16415b4 at 19:45:29Z (Linear BEE-195 Done 19:47Z). beethoven-agents PR #1 was merged by greg at 16:15Z. beethoven-research PR #4 was merged by greg at 19:34Z, and CI on main 8dd5be2 is green. All three engine repositories now merge on green.
5. greg chose the signed install (15:41Z) and the automatic store upload from his Mac (19:31-19:36Z). The store upload step (28 tests, nothing sent to Google) and all five installer streams (625 tests, Chrome build and mock selftest pass, 20:12Z) are on branch d6db850 of beethoven-extension, pushed by 20:31Z.
6. This hand-off was written, checked against GitHub and the sessions at 19:36-20:22Z, and re-checked claim by claim by nine independent checkers.

## 5. Active Blockers & Errors

**On greg's hands, most unblocking first** (the full list is in `DECISIONS.md`):
1. greg is close to his weekly limit (20:25Z), so every thread may stop until it resets; this folder is the continuation. Do not run `beethoven uninstall`, `claude forget`, `access init`, `access admin approve` or `library publish` (the VS Code edition's grid commands) on the grid until grid scripts 9 land.
2. Copy desktop's `automerge.yml`, `rulesets.yml` and `rulesets/main.json` into hpcworker and beethoven-extension.
3. The Apple Developer ID, Azure Artifact Signing and the Chrome Web Store item id.
4. VS Code: merge Dependabot #2 when convenient; 5.0.0 is not built, signed or published until the grid scripts 9 fix lands with the account-setting PR.
5. The base decisions on the desktop thread's cards when they come: the `claude -p` queue, the grid-side licence check, the grant for VS Code-only students; the optional `BASE_PROPAGATE_TOKEN` later.
6. The grid steps: deploy framework 17, `tools/grid_ci.sh`, the engine image build (runbook G0, BEE-103), bee L1-L5 and G1-G4, probes M13 and BEE-101.
7. The 15 desktop laptop checks.
8. BEE-181 questions 1, 4 and 6 and BEE-165, which block the first study and the wiring of the split check into it.

**Work on branches with no PR, and outside GitHub** (desktop thread, saved 20:27Z; README in `/mnt/project-files/staging/desktop-thread/`):
- Branch `claude/project-thread-fx3wkp`: beethoven-extension d6db850 (15.0.0), hpcworker b35952a (queue report, 20 review findings unfixed), beethoven-vscode aa44696 (`beethoven.account`, 22 review findings unfixed). None has a PR or a CI run.
- Only in the staging folder: the extension's Mac release branches as a git bundle (verifies on d6db850), half-done fix patches for hpcworker and VS Code (both apply cleanly to their branch heads, not yet tested), the findings, the hpcworker PR #3 body draft, hpcworker's `docs/V12_CONTRACT.md` patch (commit ed94b6b; on b35952a it gives the extension branch's blob 75f86cb exactly), and the beethoven-base survey and design with its two critiques.

**Grid lane:**
- `grid/slurm-in-container` has never passed: "the container check failed (CANCELLED+)".
- No framework 16 or 17 commit has a grid success: 6bf8167 (framework 16) has no status, and 73af802's `grid/framework-suite-py36` has read "suite queued on the grid" (pending) since 00:59:13Z.
- agents `containers/README.md`: "No grid build yet and no committed digest".

**Tool errors in a project thread:**
- "HTTP 403: GitHub GraphQL is not available from Claude Code sessions"
- The GitHub plugin server: "Proxy refused to open a tunnel: 403 Forbidden"
- Actions job logs: the API redirects to GitHub's log storage and the proxy refuses that download ("Forbidden", CONNECT 403). The Actions path for listing secrets answers "Access to this GitHub Actions path is not permitted through this proxy."

**Not yet measured:**
- Nothing of the project is known to have run on the grid since the suite passed on 2e5bcf8 (2026-10-03T20:27Z, the tree framework 16 bumped); `tools/grid_ci.sh` last posted at 00:59Z on 2026-10-04, queuing a suite whose outcome is unknown.
- How Claude Code reports the remaining usage window (BEE-121).
- Probes M1 to M13 and BEE-101.
- Whether the qa plugin loads in the agents image.
- Whether one command on a real Mac builds and signs the Windows installer (wixl, the Rust cross-build and jsign were checked in the desktop thread's own session).
- Whether the saved Google store sign-in outlives seven days.
- The Marketplace listing of the VS Code edition.

## 6. Immediate Next Actions (Hydration Directives)

1. Read the memory index, `HYDRATE.md`, this file and the `repos/<repository>.md` of your task, then confirm each main in section 3 with `git ls-remote https://github.com/<owner>/<repo>` and `gh api "repos/<owner>/<repo>/pulls?state=all&per_page=10"` before acting on any row.
2. Check what moves fastest: `fetch_thread` on the desktop thread newest first, what the desktop thread has put into beethoven-base (attach it with `add_repo` first), and whether the extension 15.0.0 PR, hpcworker PR #3 or the VS Code account-setting PR now exist (`gh api` on each repository's pulls); if the desktop thread's work is lost, each repository file's section 6 says how to apply its staging item.
3. Before changing a repository or a plan file, find its owner in `THREADS.md` and route through the coordinator unless greg reassigns it; then follow that repository file's section 6 in order.
4. The next engine build is qa BEE-108 and BEE-109, agents BEE-189, BEE-187 and BEE-186, and research BEE-111 to BEE-115, each clearing the qa gate, opened ready, with a ledger row per unit of work.
5. When you stop, refresh the state files you changed with a new timestamp line, append your ledger row, and update the memory line that points at `/mnt/project-files/state/`.

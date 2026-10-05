**Describes:** 2026-10-05 00:15Z (refreshed for the hub: GitHub, the threads and Linear read again from 23:40Z; before that, decisions read from the threads, `ledger/INTERVENTIONS.md`, `plan/BUILD_PLAN.md` section 13, `plan/REPO_SPLIT.md`, Linear and GitHub between 18:35Z and 20:22Z, every row re-checked by an independent checker; the desktop thread's pushed branches checked at 20:32Z; its 20:58Z changes by three independent checkers at 21:15-21:20Z)

# Beethoven: greg's decisions, open questions and his steps

Every time is UTC. "Where" names the record that holds the decision; when a decision and a record
disagree, the newer of greg's own words wins and the record is stale. `plan/BUILD_PLAN.md` (owned by
the thread "Replan the build and seed Linear") has folded nothing after 14:13Z: the decisions from
15:19Z on live only in the threads, memory, the ledger, `plan/REPO_SPLIT.md` (section 2 and the state notes in
section 6, the three-repo thread's) and this file.

## Standing decisions from before 2026-10-03 (written in the repositories' CLAUDE.md files)

| When | Decision |
| --- | --- |
| 2026-09-29 | The public name is Beethoven (extension 7.0.0); the code name Ashley stays only where CLAUDE.md lists it |
| 2026-09-29 | No licence keys in the browser edition: the student's own Open OnDemand sign-in plus greg's approved list through the access service |
| 2026-09-29 | The worker is always on (one `afterany` successor); "Claude Code is like gas, the Ashley code base is the car": the image and the framework are the lab's shared things |
| 2026-09-30 | One approved account, one installation (`install_id`); one store, one private Chrome Web Store listing whose testers are greg's Google Group |
| 2026-10-02 | The extension may request `nativeMessaging` for its own bridge host only |

## Decided on 2026-10-03 to 2026-10-05

| UTC | Decision or step | Where it is recorded |
| --- | --- | --- |
| 10-03, time not recorded | The project rewritten as seven goals (G1 verified code, G2 REFORMS, G3 token economy, G4 legal and security boundaries, G5 storage and orchestration, G6 medical calibration, G7 publication) | `ledger/LEDGER.md:11-13`; memory GOAL line |
| 10-03 22:35Z | Re-evaluate the build order, put in the code-quality and token-economy standards, mirror the work in Linear, make the build measurable | `LEDGER.md:14`; BUILD_PLAN written 22:42Z |
| 10-03 23:09Z | D1: each person's own flat-rate subscription, no pooled keys, no gateway (the LiteLLM recommendation withdrawn); D2: a new repository beethoven-research; D3: Metaflow with outerbounds/metaflow-slurm, a plain sbatch adapter first; new directions F1 (desktop extension), F2 (command center), O (promo), R (imaging migration) | BUILD_PLAN section 7, section 11; `INTERVENTIONS.md:9-11`; Linear BEE-98, 99, 100 Done |
| 10-03 23:51Z | Hand step: greg created beethoven-research (GitHub created_at 23:51:21Z; in the project by 23:54Z; the GitHub App gets 403 creating repositories) | GitHub; `INTERVENTIONS.md:12-13` (marked reconstructed, gives 23:54Z) |
| 10-03 23:58Z | Imaging sources: greg pointed at the t-SNE corpus code; his word "nramcj" matched nothing and is still to be asked | `INTERVENTIONS.md:14` |
| 00:02Z | The non-negotiables become project instructions of at most 16,000 characters | `INTERVENTIONS.md:15`; `plan/PROJECT_INSTRUCTIONS.md` |
| 00:16Z | The build is framed as a protocol / methods paper; interventions are first-class data | BUILD_PLAN section 12; Linear BEE-174 and BEE-176 to 179 (there is no BEE-175) |
| 00:27Z | Read the Drive folders claude-artefacts and spine; research comes last, but the spine study shapes the ecosystem | BUILD_PLAN sections 15, 16 |
| 01:10Z | D1b = C, decide on evidence: no token file unless probe BEE-101 shows the sign-in does not refresh headless | BUILD_PLAN section 7 D1b; `INTERVENTIONS.md:21` |
| 01:12Z | Usage credits are never used, by anyone, a rule of the same rank as the others; the Claude Desktop plugin is written regardless of Claude Code Desktop | BUILD_PLAN section 2 C7; `INTERVENTIONS.md:22-23`; every repository CLAUDE.md |
| 01:05Z | Hand step: greg created beethoven-desktop (GitHub created_at 01:05:56Z); added to the project at 01:21Z | GitHub; `INTERVENTIONS.md:26` |
| 02:02Z | Hand step: the organisation upgraded to GitHub Team | `github/AUTO_MERGE_SETUP.md:15` |
| 02:11Z | No human gates a merge: PRs open ready, never draft; auto-merge armed; the required checks alone decide; the gate runs before every push | BUILD_PLAN section 3 item 7; `INTERVENTIONS.md:29-31` |
| 02:18Z | D1d card: "My own several accounts", chosen knowingly after the terms check | BUILD_PLAN section 7 D1d; `INTERVENTIONS.md:32` |
| 02:30Z | Several of his own accounts at once, one master per account, one super-master lease, agent teams, messaging, sessions as Slurm jobs, no orphans; "CHANGE THE RULES AGAINST IT IN THIS REPO AND MAKE THE AUTH PROCESS SIMPLE" | BUILD_PLAN section 17; `INTERVENTIONS.md:33-35`; Linear BEE-185 to 190 |
| 02:37Z | Use the worktrees and workflows pages for bootstrapping and parallel work | BUILD_PLAN section 17.6; Linear BEE-192 |
| 03:09Z | GitHub paid add-ons: "None now"; account switching follows the four published switchers where they fit (a directory per profile; no credential copying) | `INTERVENTIONS.md:36, 38`; `github/SCANNING_RULES.md` |
| 03:15Z | Remove the VS Code 4.0.0 pay-per-use key overflow (BEE-191); hand step: rulesets imported into beethoven-research (24440691) and beethoven-desktop (24440600) | `INTERVENTIONS.md:41-42`; Linear BEE-191 Done |
| 03:23Z | Continue a spent session on the next account with `--resume <transcript path> --fork-session`, the file bound read-only, built only after probe M13 | BUILD_PLAN section 17.2.9; agents `docs/ACCOUNTS.md` section 5 |
| 03:29Z, 03:51Z | Hand steps: merged research PR #1; created the `RULESETS_TOKEN` secret | GitHub; `INTERVENTIONS.md:46` |
| 04:12Z | Implement his Drive guide "Claude CLI State Management" for seamless account switching on the laptop and in the grid container (became `bee`) | `plan/ACCOUNT_SWITCH_AMENDMENT.md:5-8`; research PR #3 |
| 04:52Z | Split the engine into three repositories, quality assurance first | `plan/REPO_SPLIT.md:5-9`; BUILD_PLAN D2 |
| 13:19Z | Card: the research pipeline stays in beethoven-research, so only beethoven-qa and beethoven-agents are new | `REPO_SPLIT.md:23`; `INTERVENTIONS.md:51` |
| 13:19Z, 13:37Z | Hand steps: created beethoven-qa (GitHub 13:19:42Z; greg said so at 13:24Z) and beethoven-agents (13:37:24Z) | GitHub; Linear BEE-193, 194 Done (BEE-193, `LEDGER.md:127` and BUILD_PLAN D2 say 13:24Z) |
| 13:27Z | "no api key anywhere thats the only fundamental rule of this software": covers his own tooling, Copilot review and claude-code-action; hand step: merged VS Code PR #5 (5.0.0) | BUILD_PLAN section 2 and C8; `INTERVENTIONS.md:52`; every CLAUDE.md |
| 13:31Z | Pasted PROJECT_INSTRUCTIONS version 11 (15,990 characters) into the project settings | `INTERVENTIONS.md:52` |
| 13:42Z, 13:57Z | Hand steps: merged qa PR #1; widened the `RULESETS_TOKEN` and the organisation secret to all repositories "so i never have to do this again" | `INTERVENTIONS.md:53-55` |
| 15:19Z | Three asks: remove the helper-script dependency; maybe a fourth repository for the grid rules loaded as a profile by the clients (NOT decided); requeue is slow, so ask on both primary/secondary and requeue | desktop thread; `REPO_SPLIT.md:50-61`; memory |
| 15:26Z | Will pay for a professional install: Chrome Web Store, then everything automatic, no Terminal | desktop thread; memory `signed-bridge-packages` |
| 15:41Z | Option B: a signed, notarized Mac package with the compiled (Rust) bridge, and Windows signing through Azure Artifact Signing (Basic, $9.99 a month) | desktop thread; memory `signed-bridge-packages` |
| 16:15Z | Hand step: merged agents PR #1 | GitHub; `INTERVENTIONS.md:57` |
| 16:23Z | Card "First module": research's emptied package carries the patient-level split check (BEE-116) | `INTERVENTIONS.md:58`; research PR #4 |
| 16:24Z | Card "Drop it": a fresh grid sign-in no longer signs anyone out | `LEDGER.md` 17:12Z row; hpcworker PR #2 |
| 16:35Z to 18:13Z | Hand merges: hpcworker PR #1 (16:35:45Z), extension PR #1 (16:35:58Z), VS Code PR #6 (17:05:26Z), hpcworker PR #2 (18:13:41Z) | GitHub |
| 16:45Z | Custom default cloud environment `env_01CxLnKLA8fTAo7waT63iJyM` (new threads only) | memory ENVIRONMENT line |
| 18:34Z | Write all state to a file for another session, and a hand-off per repository | this thread |
| 18:40Z | Switched the three-repo thread to Opus 5.5 ("continue with opus"); the coordinator and the thread default moved to Opus 5.5 | `INTERVENTIONS.md:59`; coordinator relay 18:50Z |
| 19:26Z | "continue with opus" in the desktop thread, which resumed on Opus 5.5 | desktop thread |
| 19:33Z | "save as much as possible to make this easy as possible on me": one release command on his Mac builds and signs both bridge installers (no Windows machine), zips the extension and uploads it once | desktop thread 19:34Z (being built; Mac tooling not yet measured) |
| 19:34Z | Hand step: merged beethoven-research PR #4 (8dd5be2), whose renamed required check the old rule could not see; the merge re-applied the rule, and research PRs merge themselves on green again | GitHub; three-repo thread 19:36Z; Linear BEE-197 Done 19:34:52Z |
| 19:36Z | Card "Save on Mac": the Chrome Web Store upload's Google sign-in stays saved in his vendor folder on the Mac; each release uploads and submits by itself; the listing stays private | desktop thread card of 19:31Z |
| 19:45Z | Hand step: published beethoven-qa release v1.0.0 on 16415b4 (the pinned copies in agents and research match it file for file); the three-repo split is finished | GitHub release; three-repo thread 19:47Z; Linear BEE-195 Done 19:47Z |
| 20:04:55Z | "can you migrate the common codebases to a separate repo, beethoven-base, and just have the beethoven-vscode, beethoven-extension, and beethoven-desktop extensions contain their specific unique code? that way i can add features to all of them by updating the base repo?" The desktop thread is mapping the shared code and designing it; moving the VS Code edition off its own grid scripts onto hpcworker is one step (20:17Z) | desktop thread; coordinator notice (edited 20:07Z) |
| 20:14:53Z | "also I set my RULESET token to all repos visibility, so i dont mind creating secrets". The desktop thread takes it as allowing one new read-only GitHub token as a CI secret, so each edition's CI fetches the base and a base change opens a "take the new base" PR in each edition; a Claude or Anthropic key still never goes into any of them (its reply 20:17Z). Superseded at 20:58Z: the design needs no read token (each edition carries a checked pinned copy); its one optional credential, `BASE_PROPAGATE_TOKEN`, stays in beethoven-base; the desktop thread corrected its 20:17Z message, including that `RULESETS_TOKEN` is not settings-only (its Administration write adds deploy keys that read and write code, changes visibility, adds collaborators) and is never used for code | desktop thread; coordinator relay 20:59Z; GitHub's permissions table, checked 21:20Z |
| 20:25:13Z | Hand step: created `OpenSpineConsortium/beethoven-base`; "please update continuation file since im coming up on my weekly limit" | desktop thread, relayed by the coordinator 20:26Z |
| 20:58-20:59Z | Hand step: merged Dependabot #4 (TypeScript 7.0.2), #3 (@types/vscode 1.138.0) and #1 (@types/node 26.6.3) in beethoven-vscode; #2 then conflicted ("shit i merged these out of order and now there is a merge conflict", 21:00Z) and Dependabot rebased it itself at 21:01Z | GitHub; this thread |
| 21:00Z | Asked by the desktop thread to hold VS Code 5.0.0 and not to run `uninstall`, `claude forget`, `access init`, `access admin approve` or `library publish` on the grid until grid scripts 9 land (hazards checked again at 21:18Z) | desktop thread 21:00:13Z |
| 21:10:19Z | Card "Pin types back": VS Code keeps its minimum at 1.100 and `@types/vscode` goes back to 1.100.0; hand step: merged that fix, beethoven-vscode PR #7, at 21:16Z (cc76efd) | this thread's card; GitHub |
| 21:48-21:52Z | Hand steps: merged beethoven-vscode Dependabot #8 (mocha 12.0.3, which replaced #2, closed unmerged) and #9 (@modelcontextprotocol/sdk 1.31.0), and hpcworker PR #3 (the queue report, with `docs/V12_CONTRACT.md` made the extension 15.0.0 branch's text) | GitHub, read 00:05Z |
| 23:26:09Z | In the desktop thread, four asks: (1) "workers on all possible queues should be launched and the first to get allocated should respond to the client to minimize wait time" (desktop thread, hpcworker); (2) the code-quality standards of his new Drive file as independent groups that "some can pass, and some can fail", each a pull-request blocker, in beethoven-qa or repositories of their own, "whatever arrangement is necessary to set that up. please do it" (thread "Independent code-quality gates"); (3) his Drive doc on native messaging for the direct pathway, "which you can incorporate" (desktop thread, the extension's docs); (4) "the original just Beethoven repo I don't believe is being used anymore. You can wipe it and replace it with whatever you need to separate the existing repos ... all the project files currently on the cloud I would like them to be pushed to get hub and it updated so that I can pick this up from another Claude account just by cloning one individual repo and maintain that tight integration with linear" (this thread: the hub, PR #1) | desktop thread; coordinator relays 23:31Z and 23:43Z |
| 23:46:24Z | "separate this protocol as much as possible from the specificity of Wayne state's super computer while preserving the underlying functionality and put all the Wayne state specificities into its own 'theme' or 'module' so in the future I can expand onto other universities simply by writing a new module ... Do /deep-research ... add all the issues ... into linear issues and then start on them" | desktop thread; its own thread "Wayne State as a site module" from 23:48Z |
| 10-05 00:13Z | Card in the hand-off thread, "Push to main": once PR #1 is merged, each sync of the project files into the hub is pushed straight to its `main`, with no pull request; until then syncs update PR #1 | this thread's card |
| 10-05 00:14Z | Hand step: merged the hub's PR #1 (merge 9e8a7f7, head 7ca551e) | GitHub, read 00:16Z |
| 10-05 00:28:04Z | In the desktop thread: "All of the decisions look good except for d2. The only time I want you to interact with me is for decisions where you have a recommended approach and alternatives": the base design's D1 and D3 to D8 accepted as recommended, D2 (drop `bypassPermissions`) not accepted; and from now on Claude messages him only for a decision, with a recommendation and the alternatives. Progress stays in each thread's status; what he must do himself goes to the coordinator's to-do notice | desktop thread; coordinator relay 00:30Z |

## Questions greg asked, and the answers on record

| UTC | Question | Answer |
| --- | --- | --- |
| 10-03 21:26Z | How to auto-approve requests | Cloud threads ignore `bypassPermissions` in settings files; pick the approval option that covers the rest of a thread; Auto mode under Project settings > General for new threads (coordinator 04:39Z) |
| 04:27Z | A user-scope `settings.json` with `bypassPermissions` | The session may not write its own settings; content and path given for his laptop; the engine image disables bypass on purpose (`LEDGER.md` 04:31Z) |
| 16:47Z | Use the $250 in cloud credits | It is the Claude Code cloud-session promotion for Max: claim at claude.ai/code/claim-credit or `/claim-credit` by 2026-10-07 23:59 PT; then applied automatically to cloud sessions before plan limits; unspent balance expires 2026-11-04; not "usage credits" (coordinator 18:27Z, after a wrong answer at 18:17Z) |
| 18:26Z | Teleport existing sessions to the cloud | Project threads already are cloud sessions; a local session cannot be moved into the cloud (coordinator 18:27Z) |
| 19:26:52Z | "also i want the chrome extension to automatically upload the newest version to the chrome marketplace when its ready. can it do that? do i need to make the extension public to avoid paying for a google wrokspace?" (project chat, relayed to the desktop thread 19:28Z) | Yes, and no (desktop thread 19:31Z): the store's upload API v2 uploads and submits, Google reviews every version; a Private listing whose testers are a Google Group he owns works from a personal account, only a whole-domain listing needs Workspace. The upload runs at the end of his release command on his Mac, never in GitHub, since only his machines sign the installers |
| 19:33:50Z | "do i have to upload one from mac and one from windows to get the signed binary?" | No: one zip carrying both signed installers, uploaded once; the release is being reworked so the Mac also builds and signs the Windows installer (desktop thread 19:34Z) |

## Open decisions (only greg can settle them)

| Id | Question | Blocks |
| --- | --- | --- |
| D9 / BEE-181 | Twelve first-study questions (`plan/SPINE_FIRST_STUDY.md` section H) | Questions 1, 4 and 6 block the first run |
| D7 / BEE-165 | Imaging source directories, CephFS destination, PHI statement, second copy | The imaging migration; wiring the split check into a run |
| `plan/IMAGING_SOURCES.md` section I | Six questions (lines 307-315) | The migration batches |
| "nramcj" | What he meant (2026-10-03 23:58Z) | Possibly the imaging source list |
| M-8 / BEE-177 | The grid's acceptable-use position on autonomous agents and the paper's AI-use disclosure | The first unattended run |
| D1c | Confirm his account's data-sharing setting near patient data | Any engine step near patient data |
| BUILD_PLAN D4 | Confirm the engine is headless `claude -p` (assumed, never confirmed); not the settled multi-account D4 | Phase 0 probe shape |
| D5 | Keep the human Publish click before Zenodo or Hugging Face (assumed yes) | G7 releases |
| Launcher "One person, one account." | Re-apply the D4 sentence (branches `claude/project-thread-2udoqz` in hpcworker and beethoven-extension, unmerged and now conflicting) or drop it | `hpcworker claude login --account` and the status `account` field |
| Two-queue worker policy | Settled in principle by greg's 23:26Z ask: launch on every queue and let the first allocation answer; the desktop thread designs it in hpcworker, the queue list goes into the Wayne State module | The all-queue PR (not opened); the queue report it can read landed as hpcworker PR #3 (21:52Z) |
| Fourth repository (grid rules) | Floated 15:19Z | Nothing yet; both threads see it as a later move, and the beethoven-base design may take it in |
| beethoven-base design D2 | Answered 00:28Z: D1 and D3 to D8 accepted, D2 not; what D2 becomes is the desktop thread's to put to him again. The question as sent: written at 23:34Z (`base/DESIGN.md`); greg decides D1 to D8 of its section 12, sent 23:35Z with "Take all my recommendations?": D1 VS Code's `claude -p` queue (helper now, engine later), D2 drop `bypassPermissions`, D3 drop GPU workers in hpcworker unless a student uses them, D4 GitHub and Hugging Face tokens on the grid stay with that helper, D5 drop the grid-side licence check, D6 `FRAMEWORK_MIN` lead-only, D7 desktop's Open goes to the session and New session to the environment, D8 no propagation credential for now. D9 (`@types/vscode` pinned) is settled. These replace the three questions of 20:58Z | Base PR #1 onward; VS Code 7.0.0 |
| Desktop PR #1 | Keep or revert the 1.0.0 merge of 02:31Z | Nothing downstream |
| D6 / BEE-158, D8 / BEE-173, M-7 / BEE-176 | Desktop distribution; where the promo is shown; paper venue | Their own projects only |
| Roadmap decisions 2, 4, 5, 6 | BUILD_PLAN section 15.6 proposals | Nothing urgent |
| PRIVACY.md debug log | How the in-memory debug log is described before any store upload | The next store upload |
| Staging bundles | The two top-level `/mnt/project-files/staging/*.bundle` (agents and qa, 07:32Z) are superseded; removing them is his call, and the hub leaves them out (`.hub-exclude`). `staging/desktop-thread/` is the desktop thread's save of 20:27Z; its Mac release branches are now on the extension branch 9aa1171 and its hpcworker patches landed in PR #3 | Nothing |

## Waiting on greg, most unblocking first

1. Do not run the VS Code edition's `uninstall`, `claude forget`, `access init`, `access admin approve` or `library publish` on the grid until grid scripts 9 land.
2. Copy `automerge.yml`, `rulesets.yml` and `.github/rulesets/main.json` from beethoven-desktop into hpcworker and beethoven-extension, with each repository's own CI job names as the required checks.
3. Apple Developer Program (Developer ID Application and Installer, notarytool profile), Azure Artifact Signing (Basic), and the Chrome Web Store item id; later, one Google sign-in on his Mac when the store upload step first runs.
4. VS Code: 5.0.0 is held until grid scripts 9 land with the account-setting PR, then build and sign with `tools/release.mjs`, check the site's pages, publish, and unpublish Ashley 3.0.0.
5. The hub: merge `OpenSpineConsortium/beethoven`'s next pull request (the merge-policy text and the seams page) when it opens; set `BEETHOVEN_REPO` to a beethoven-extension checkout before the next site build; merge hpcworker PR #4 (it points `tools/push_org.sh` at hpcworker) before running that script again.
6. On the grid: deploy framework 17 (`tools/deploy_shared.sh`), run `tools/grid_ci.sh --ref main --container`, build the engine image (runbook G0, BEE-103), bee steps L1-L5 and G1-G4, probes M13 and BEE-101.
7. Desktop: laptop checks 1 to 15; keep or revert PR #1.
8. The open decisions above, BEE-181 questions 1, 4, 6 and BEE-165 first; the base design's D2.

Records that may lag GitHub (read GitHub, not them): the coordinator's standing notice; the memory index; Linear BEE-155, 156 (In Review, merged), BEE-110 (Backlog, built) and BEE-192 (Backlog, partly built).

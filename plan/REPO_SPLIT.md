# The three-repository split of beethoven-research (proposal, 2026-10-04)

Written by the thread "Three-repo separation" for the thread "Replan the build and seed Linear",
which owns `BUILD_PLAN.md`, `PROJECT_INSTRUCTIONS.md` and Linear. Nothing here edits those files;
section 7 is the amendment text for them. Source of the ask: greg in the project chat, 2026-10-04
04:52Z: "Separate the research pipeline, claims, redorm reproducible data science, from the code
writing software framework, pixi concolic ect, and also from the nested agentic framework, so I
need to create three more repos, starting with the software quality assurance repo which you will
use to improve the existing code and write the new code." ("claims" is read as CLAIM, the
imaging checklist of PROJECT_INSTRUCTIONS section 7; "redorm" as REFORMS.)

Beethoven runs Claude Code and is not an Anthropic product; "Claude" and "Claude Code" are
Anthropic's marks, used here to say what it runs.

## 1. The three concerns and their repositories

| greg's words | Repository | Package | What it owns |
| - | - | - | - |
| "the code writing software framework, pixi concolic etc", "the software quality assurance repo" | `OpenSpineConsortium/beethoven-qa` (new, first) | `beethoven_qa` | how code is written and proven before it may run: the pixi substrate convention and lock discipline, Design by Contract, the layering rule (pydantic, beartype, typeguard), the CrossHair/Z3 gate as a command any repository runs, schema-aligned parsing (BAML/SAP, G1-4), the SpecPylot loop (G1-5), the worked example, the build-stream agent and the code-writing workflows, and the repository rules every repository carries (pre-push gate, CI gate lane, auto-merge, rulesets as code) |
| "the nested agentic framework" | `OpenSpineConsortium/beethoven-agents` (new, second) | `beethoven_agents` | how agents run on the grid: the Apptainer image, its managed settings and the PreToolUse guard, accounts and the super-master lease (D4, BUILD_PLAN section 17), the outer Metaflow loop and the inner `claude -p` step, quota-window pacing (G3), node-local scratch and session persistence (G5), the registry, bus, heartbeats and reaper, masters, satellites and teams |
| "the research pipeline, claims, REFORMS reproducible data science" | `OpenSpineConsortium/beethoven-research` (kept: greg's card, 2026-10-04 13:19Z) | `beethoven_research` | what is computed and how a result is shown to be sound: REFORMS (Run ID, clean-tree gate, patient-level splits, bootstrapped intervals, CodeCarbon, `reforms.json`), CLAIM tables, medical calibration (HU, MONAI MetaTensor), the claims-to-numbers check (a reported number that moves fails the build), dissemination (OpenLineage, RO-Crate, LaTeX macros, Zenodo and Hugging Face behind the Publish click), and the study flows, the spine study first |

**Decided by greg on the thread's card, 2026-10-04 13:19Z: the research pipeline stays in
`beethoven-research`**, so two repositories are created, not three. The reasons the card gave: its name already says research, its
rulesets, secret, auto-merge setting and project attachment are in place, BUILD_PLAN and Linear
already point G2, G6 and G7 at it, and almost none of what it holds today is research-pipeline code,
so after the split it starts nearly empty either way. The answer not taken, a third new repository
(working name `beethoven-science`), would have frozen `beethoven-research` as the record up to the
split.

## 2. Direction of dependence

```
beethoven-qa  <──  beethoven-agents  <──  beethoven-research
      ^─────────────────────────────────────────┘
```

- `beethoven-qa` depends on nothing of ours. It must stay usable by any Python repository.
- `beethoven-agents` uses `beethoven-qa` (its modules clear the gate; the image carries the gate so
  a step can run it). It never imports the research pipeline: it runs any step it is given, a
  study step or a code-writing campaign alike.
- The research pipeline uses both: its modules clear the gate, and its flows run their agent steps
  through `beethoven-agents` (the step runner, accounts, pacing). Its Run ID is the one the agents'
  registry records; the agents' per-run measurements (tokens, cache, compactions, subagents, wall
  time) are what its `reforms.json` compute record cites.
- Nothing points back up. A change that needs an upward import is in the wrong repository.
- The launcher (`hpcworker`, `beethoven-extension`) and the desktop and VS Code editions stay where
  they are; the contract between the cluster side and the clients (`docs/V11_CONTRACT.md`) is
  untouched by this split.
- **The grid's rules and site profiles, as of 2026-10-04 15:2xZ** (greg is weighing a fourth
  repository for the Wayne State grid protocol and rules, loaded as a profile by the three clients;
  not decided, asked in the desktop plugin thread). Today the site profiles are canonical in
  `hpcworker` (`framework/profiles/<site>.json`, schema and CLI in `framework/lib/profile.py`,
  Python 3.6 standard library) and the extension, the desktop plugin and the VS Code edition
  carry them as data (`sync-profiles.mjs`, `profiles/pull.sh`); the etiquette text (login node,
  node-local temp, the 60 s floor, wall time, partitions and QoS) is in each repository's
  `CLAUDE.md` from `hpcworker`'s. `beethoven-agents` holds how agents run on the grid (the image,
  job templates, the adapter under Metaflow, pacing) and will read the same profile as data,
  never importing `hpcworker`, since it depends on `beethoven-qa` alone. So a fourth repository
  would be a move of `framework/profiles/` and the schema with it, taken as data by all five
  consumers the way three already do, not a rewrite; until it exists `hpcworker` stays the home.

**The image.** The base image (Claude Code, the managed settings, the guard, the pixi environment
of `beethoven-agents`, which includes `beethoven-qa`) is built in `beethoven-agents`. A study image
that adds the research pipeline's environment (MONAI, pydicom, W&B, CodeCarbon) is built in the
research repository on top of it (Apptainer `Bootstrap: localimage`), so the base image's digest
stays the substrate every engine job shares and a study's digest names its own additions. Not built
yet; recorded here so neither repository grows the other's half.

## 3. How beethoven-qa is consumed

greg's use is "which you will use to improve the existing code and write the new code", so it has
two faces: a package and command for repositories, and a Claude Code plugin for sessions.

**Repositories (CI, pre-push, the grid).** Each consuming repository carries a pinned copy at
`vendor/beethoven-qa/` with an `ORIGIN` file (repository, tag, commit, tree sha256), refreshed only
by `python -m beethoven_qa vendor --into <repository> [--kit]` from a clean checkout of a tagged
release. The copy is put on the consumer's `PYTHONPATH` by its pixi activation
(`$PIXI_PROJECT_ROOT/src:$PIXI_PROJECT_ROOT/vendor/beethoven-qa/src`, absolute so a `pixi run` from anywhere imports both), not declared as a pixi path dependency: the copy's dependencies
(icontract, beartype, pydantic, typeguard, CrossHair) are already in every consumer's own lock, and
`ORIGIN` plus the check below record and guard the copy, so the lock never has to describe it. The
consumer's `pixi run --locked gate` runs `python -m beethoven_qa vendor-check` (the copy's files still hash
to `ORIGIN`, and the four kit files are byte-equal to the copy's; a hand edit fails) and then
`python -m beethoven_qa gate`, which reads the package to check from the consumer's own
`[tool.beethoven-qa]` table in `pyproject.toml`. A function CrossHair must not run (it reads,
writes, asks the clock or the environment, starts a process) or measurably cannot run is named in
that table under `unproven` with its reason, which the gate prints on every run; the gate refuses
every `# crosshair:` comment, since a comment hides what is not proven. The command never deletes: a file a new release
dropped is listed for a reviewed `git rm`. Why a copy and not a git dependency: all the
repositories are private, a GitHub Actions run of one repository cannot fetch another private
repository with its own token, and the grid's image build has no GitHub token at all; a copy needs
no secret anywhere, which is the project's rule. It is the same pattern as `framework/profiles/`
vendored into `beethoven-extension` with `pull.sh`. If greg ever makes `beethoven-qa` public, the copy
becomes a plain pinned git dependency and nothing else changes.

**Claude sessions.** `beethoven-qa` is also a Claude Code plugin marketplace with one plugin,
`beethoven-qa`: skills (the definition of done; writing a new module to it; bringing an existing
module up to it without changing its behaviour; presenting contracts for a human to review), the
`stream` agent (one bounded change in its own worktree), and the workflows `gate-until-green`,
`verify-module` and `improve-module`. Checked against the plugin reference and the marketplace pages
on 2026-10-04: a plugin may ship `skills/`, `agents/`, `hooks/`, `workflows/` and more; a private
GitHub marketplace is reached with the user's own git credentials; a `directory` marketplace needs
only read access to a path; managed settings can register and force-enable a plugin, and under
`allowManagedHooksOnly` the hooks of a plugin managed settings force-enable still run.

- greg's laptop: `/plugin marketplace add OpenSpineConsortium/beethoven-qa`, then
  `/plugin install beethoven-qa@beethoven-qa` (his git credentials reach the private repository).
- Engine jobs on the grid: the image copies the plugin to `/opt/beethoven-qa` and its managed
  settings register it as a `directory` marketplace and enable it, so every `-p` step and every
  master has the same skills and workflows without trusting a folder.
- Project threads in the cloud: the pages say a cloud session does not add a repository's
  `extraKnownMarketplaces` (no trust dialog), so a thread reads the attached `beethoven-qa`
  checkout (its `CLAUDE.md` and `skills/`) and runs its gate from there. Whether a repository's
  `.claude/skills/` plugin loads in a cloud thread is not yet measured.

**Where the full bar applies.** icontract, the layering rule and CrossHair apply to Python that may
take dependencies: the three engine repositories and, if greg ever asks, the study repositories
(read-only from this project today). `hpcworker`'s framework is Python 3.6 standard library only
and the extension and desktop editions are TypeScript: they take the repository half of
`beethoven-qa` (the pre-push gate, required checks, auto-merge, rulesets as code), which they mostly
have already, and their own language's checks, not icontract.

## 4. File by file: where today's beethoven-research goes

`beethoven-research` at `main` 33ce108. Every move is a copy first; nothing leaves
`beethoven-research` until the receiving repository carries it on its `main` (section 6).

| Today | Goes to | Note |
| - | - | - |
| `pixi.toml`, `pixi.lock` | qa (renamed workspace, lock regenerated by pixi, never by hand); agents and research get their own | each repository locks its own environment |
| `pyproject.toml` | qa (renamed); each repository its own | |
| `src/beethoven_research/contracts.py` | qa, `beethoven_qa.contracts` | the one import point for contracts |
| `src/beethoven_research/example.py` | qa, `beethoven_qa.example` | the gate's demonstration; its subject (a quota window) stays an example, not the scheduler |
| `tools/verify_gate.py` | qa, `beethoven_qa.gate` (a command taking `--package`) | generalised so every repository runs the same gate |
| `tests/test_example.py`, `tests/conftest.py` | qa (conftest per repository) | |
| `src/beethoven_research/guard.py`, `tests/test_guard.py` | agents | it governs an agent's tools and is baked into the agents' image |
| `containers/` (recipe, build script, README, managed settings) | agents | the agents' runtime; the study image later layers on it (section 2) |
| `docs/ACCOUNTS.md` | agents | D4 |
| `docs/PARALLEL.md` | sections 2 and 3 (the build in parallel: worktrees, the stream agent, workflow scripts) to qa as `docs/PARALLEL_BUILD.md`; the whole file to agents (section 4, the engine's parallel parts, is the agentic framework) | decided: the build half is how code is written |
| `.claude/agents/stream.md` | qa (plugin agent) | a code-writing agent |
| `.claude/workflows/gate-until-green.js`, `verify-module.js` | qa (plugin workflows) | the SpecPylot loop and the fix-until-green loop |
| `.claude/hooks/session-start.sh` | qa owns the template; every repository carries a copy | installs pixi and the locked environment in a cloud session |
| `.claude/settings.json` | every repository its own | |
| `.githooks/pre-push` | qa owns the template; every repository carries a copy | `pixi run --locked gate` before every push |
| `.github/workflows/ci.yml` | gate lane: qa's template, every repository; image lane: agents | |
| `.github/workflows/automerge.yml`, `rulesets.yml` | qa owns the canonical copies; every repository carries one | the same files as beethoven-desktop's |
| `.github/rulesets/main.json` | every repository its own (the required check names differ) | |
| `.gitattributes`, `.gitignore`, `.mcp.json` | every repository a copy | |
| `CLAUDE.md` | every repository its own: the hard rules in all three; the definition of done in qa; the token economy, accounts and parallel parts in agents; the methods-paper rules (progress signal, interventions, compute record) in agents and research | |
| `README.md` | every repository its own | |
| the account-switching work of the thread "Seamless account switching" (`bee account`, the hand-off hooks, the status line, the grid script): `src/beethoven_research/bee/`, `tests/bee/`, `docs/bee/`, and its changes to the guard, the managed settings, the image recipe, the CI image lane, `docs/ACCOUNTS.md` and the lock's three laptop platforms | agents | merged into beethoven-research 2026-10-04 07:06Z (pull request 3, b7b8650) and copied into the staged beethoven-agents the same morning, renamed to `beethoven_agents.bee` and `/opt/beethoven-agents`; its 53 `# crosshair:` comments became 25 `unproven` entries with reasons (24 functions that do I/O, and `claudeignore.ignored_by`, which CrossHair 0.0.111 cannot run), and `accounts.utc_text`, which CrossHair does run, is proven now; the 27 lowered per-function bounds are gone, every condition runs to the declared 20 s |

## 5. What greg does, per new repository

Only greg can do these; the GitHub App was refused creating a repository (403) and a session cannot
write repository settings or secrets.

1. Create the repository under OpenSpineConsortium: private, with **only** "Add a README file"
   ticked (so `main` exists for the first pull request; no .gitignore, no licence).
2. Settings, General, Pull Requests: tick **Allow auto-merge**.
3. The **RULESETS_TOKEN** secret. Easiest for this and the repositories after it: on the token's
   page (github.com/settings/personal-access-tokens) add the new repository under Repository access
   (Administration stays read and write), then in the organisation's Settings, Secrets and
   variables, Actions, make RULESETS_TOKEN an organisation secret shared with the new repository
   (and later ones). If the token's value is no longer at hand, regenerate it, put the new value in
   the organisation secret, and delete the repository secrets of the same name in
   beethoven-research and beethoven-desktop, because a repository secret wins over an organisation
   secret of the same name. The token never passes through a thread.
4. Tell the thread. It attaches the repository and saves it to the project (one allow prompt),
   pushes its branch and opens pull request #1, ready for review.
5. Merge pull request #1 by hand, once, when its checks are green. Until it lands `main` carries no
   required-checks rule, so auto-merge correctly stays off; the merge itself starts `rulesets.yml`,
   which applies `.github/rulesets/main.json` with the secret. Every later pull request merges by
   itself on green.

## 6. Order of work

1. `beethoven-qa`: staged now in the thread's workspace (the package, the gate command, the plugin,
   the repository rules, CLAUDE.md), gate green locally; pushed the moment the repository exists.
2. `beethoven-agents`: staged next (guard, image, managed settings, accounts docs; vendored qa);
   it also carries the account-switching thread's work, copied after its pull request merged into
   beethoven-research (section 4).
3. The research pipeline stays in beethoven-research (greg, 13:19Z). It is slimmed by pull requests
   that remove what moved (the contracts, the example and `tools/verify_gate.py` to qa; the guard,
   the image, the managed settings, accounts, the parallel-work files and bee to agents) and switch
   it to the vendored qa, only after qa and agents carry that content on their `main`.
4. Nothing is pushed to beethoven-research without the coordinator warning its two writing threads
   first ("Lay down the engine repo skeleton", "Seamless account switching").

State on 2026-10-04 15:55Z: item 1 is done (beethoven-qa PR #1 hand-merged by greg 13:42Z, its
ruleset live since 13:57Z, PR #2 with the second review merged by itself 15:46Z as 16415b4); the
`v1.0.0` tag on 16415b4 exists in the thread's checkout and waits on greg's hand, since the
session's GitHub proxy refuses tag pushes. Item 2 is done at 16:15Z: beethoven-agents PR #1
(commit 962c532, re-vendored from 16415b4 with the kit, gate green on that commit) was merged by
greg's hand as 0de7913, and the merge ran the kit's `rulesets.yml`, which put the ruleset "main:
checks before merge" (id 24460184) in place, so later pull requests there merge on green.

State on 2026-10-04 18:55Z: item 4 is done (the coordinator warned both writing threads at 16:21Z;
neither raised a collision). Item 3 is beethoven-research pull request 4, open and ready: it
removes what moved, takes beethoven-qa v1.0.0 as the pinned copy with its kit, re-locks for
`linux-64` alone (pixi; every `linux-64` record unchanged) and, since the gate refuses an empty
package, carries the first research module, `splits.py`, the split-level check (greg's card choice,
16:23Z; Linear BEE-116). It waits on greg's hand merge: the live ruleset requires the old gate job
name and the image lane, which the pull request renames and drops; the merge's push runs
`rulesets.yml`, which applies the new rule. The `v1.0.0` tag on beethoven-qa still waits on greg.

State on 2026-10-04 19:35Z: item 3 is done. greg merged pull request 4 by hand at 19:34Z (8dd5be2);
its push ran `rulesets.yml`, and the ruleset on `main` now requires the gate lane alone, so later
pull requests there merge on green. All four items are done; the `v1.0.0` tag on beethoven-qa is the
one step left, and it is greg's.

State on 2026-10-04 19:48Z: the split is complete. greg published beethoven-qa's release `v1.0.0`
on 16415b4 at 19:45Z, and the anchored `vendor-check --source` passes on both consumers' `main`.

## 7. Amendments for BUILD_PLAN, PROJECT_INSTRUCTIONS and Linear (for the replan thread)

- **D2** (BUILD_PLAN section 7, section 6 table, section 1 table): "DECIDED: a new repo
  beethoven-research" becomes "DECIDED 2026-10-03, refined 2026-10-04 (greg, 04:52Z): the engine is
  three repositories, `beethoven-qa` (Goal 1 and the repository rules), `beethoven-agents` (Goals 3,
  4 and 5 and section 17) and the research pipeline (Goals 2, 6 and 7 and the studies), with
  qa <- agents <- research the only direction of dependence (REPO_SPLIT.md)."
- **Section 3 item 7**: the PR-driven repositories become beethoven-qa, beethoven-agents, the
  research repository and beethoven-desktop; the pre-push gate and required check are
  `beethoven-qa`'s gate in each.
- **Section 3 closing line** ("packaged as a reusable library (G1)"): the library is
  `beethoven-qa`, consumed as a pinned copy plus a Claude Code plugin (REPO_SPLIT.md section 3).
- **Section 6 table**: G1 -> beethoven-qa; G3, G4 (guard, managed settings), G5 and section 17 ->
  beethoven-agents (hpcworker keeps the launcher's job template); G2, G6, G7 -> the research
  repository; P0's substrate splits (pixi and the gate -> qa, the image -> agents).
- **PROJECT_INSTRUCTIONS section 1**: "The research engine (repo OpenSpineConsortium/beethoven-research)"
  becomes the three repositories with one line each; section 12's build order is unchanged (it is
  already qa first, then orchestration, then the research layers).
- **Linear** (team Beethoven): keep the projects; retarget the "Links" line of G1 to beethoven-qa,
  G3/G5/BEE-185..192 and the guard issues (BEE-123, BEE-124) to beethoven-agents, G2/G6/G7 to the
  research repository; one new P0 issue per repository creation ("greg creates beethoven-qa: README
  only, auto-merge, RULESETS_TOKEN") assigned to greg; one issue for the plugin's first release
  (tag `v1.0.0`) and one for switching each consumer to the vendored copy.

## 8. Not yet measured

- Whether a repository's `.claude/skills/` plugin loads in a cloud project thread.
- Whether the managed-settings `directory` marketplace loads the plugin in a `-p` step inside the
  image on the grid (it is what the pages say; no image has run it).
- The gate's wall time on a grid node. Measured in this thread's cloud session (4 cores, CrossHair
  0.0.111): the symbolic lane of `beethoven-qa` over its 13 targets took 5 min 43 s as one CrossHair
  process and 1 min 44 s to 2 min 8 s as one process per target, four at a time. Measured on
  GitHub's runners (2026-10-04): the `gate` job of beethoven-qa took 4 min 10 s on pull request #1
  and 4 min 45 s on pull request #2 (10 targets, 75 tests); the `plugin` job 11 s. beethoven-agents'
  `gate` job (34 targets, 277 tests, `vendor-check` included) took 9 min 26 s on its pull request
  #1 and its `image` job (the Apptainer build) 2 min 5 s.

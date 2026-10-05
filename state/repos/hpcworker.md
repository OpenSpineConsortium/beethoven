# CLAUDE STATE SERIALIZATION

**Timestamp:** 2026-10-05T00:15Z **Phase:** Implementation

Repository hand-off: `OpenSpineConsortium/hpcworker` (private), the server half of the Beethoven launcher. Project-wide state, rules and greg's open steps: `/mnt/project-files/state/claude_context.md`; how to use this file: `/mnt/project-files/state/HYDRATE.md`. Checked against GitHub (`gh api` REST, `git fetch`) at 20:32Z, against the desktop thread's staging folder at 20:33Z, and earlier by an independent checker; whatever says "not yet measured" or "unverified" was not checked.

**Update 2026-10-05T00:15Z** (read before the sections below, which describe 21:25Z; checked with `gh api` at 00:08Z): PR #3 (queue report) merged at 21:52Z; `main` is 5492d4d and the branch `claude/project-thread-fx3wkp` (86caaa2) is behind it by one and ahead by nothing. `docs/V12_CONTRACT.md` on `main` matches the extension's copy in the 15.0.0 branch. `tools/push_org.sh` still pushes `main:main --tags` to `OpenSpineConsortium/beethoven`, which is now the project hub: do not run it until the desktop thread's retarget lands (`repos/beethoven.md`). The Wayne State site-module thread (greg 23:46Z) builds on this repository's profile; its changes reach the desktop thread's branch through the coordinator.

## 1. Primary Objective

Keep the cluster side of the launcher: `framework/` (`hpcworker`, bash 4.2 and Python 3.6 standard library only, because the Wayne State login node is CentOS 7) installs, starts, chains and reports a student's own Claude Code Remote Control worker as a Slurm job in the lab's Apptainer image. This repository is also canonical for the contract the clients read (`docs/V11_CONTRACT.md`, `docs/V12_CONTRACT.md`) and for the site profiles (`framework/profiles/wayne.json`), and it holds the maintainer's tools (`tools/deploy_shared.sh`, `tools/grid_access.sh`, `tools/grid_ci.sh`).

## 2. Architectural Decisions & Constraints

- **Never in this repository:** an API key, a key helper, a gateway or a cloud-provider route (greg 13:27Z, "no api key anywhere thats the only fundamental rule of this software"); reading, storing or relaying a Claude credential; `claude auth logout` (framework 17 removed the last one, greg's card answer "Drop it" at 16:24Z). Only `claude auth status` with authMethod `claude.ai`, apiProvider `firstParty` or none and no apiKeySource counts as signed in (`hpcw_claude_signin` in `framework/lib/adapters/common.sh`).
- No secret in argv, logs, job files or `sbatch --export`; nothing deleted outside the framework's run directories and node-local temp; destructive subcommands refuse under `CLAUDECODE`, `BEETHOVEN_REQUEST_ID` or a non-terminal stdin.
- Grid etiquette: at most one `sbatch`, `squeue` or `scancel` per action on the login node; no container command there; node-local `/tmp/$USER` (Wayne State's `$TMPDIR` is CephFS); IPC under `/dev/shm`; polling no faster than 60 s; every job has a wall time.
- The seam with the clients is the contract text, not an import: a file format or line changes here and in beethoven-extension (and beethoven-desktop's `src/contract.ts`) together. The clients vendor the profiles as data.
- **beethoven-base (greg, 20:04Z; design 20:58Z):** the code the three client editions share moves to a new repository that reads this one's contract and profiles (hpcworker stays their home until greg decides the fourth-repository idea). The design adds test vectors here, framework 18 (`--gpus`, `hpcworker env set`, which a critique says must refuse credential names) and possibly the `claude -p` queue as contract V13 (greg's decision); the VS Code edition moves onto hpcworker at its 7.0.0 (`repos/beethoven-base.md`).
- Not part of the engine split: beethoven-qa, beethoven-agents and beethoven-research take this repository's grid facts and etiquette but import nothing from it.
- Merging: no ruleset and no auto-merge workflow here, so every PR is greg's hand merge. Sessions are not permitted to write `.github/workflows/` files in this repository; greg copies them by hand.
- LF line endings are load-bearing; versions are integers; never the p-word.
- Owner thread: "Build the Claude Desktop ssh plugin" (`cmsg_01JbwQwHoYeBWptjPB5c6u8m3KSccv8f9KZdoYiLkxZons`, branch `claude/project-thread-fx3wkp`). Other threads hand changes to it through the coordinator.

## 3. Files Modified & State

| File Path | Status | Key Modifications / Purpose |
| --- | --- | --- |
| framework/bin/hpcworker | Complete | The one command; `VERSION=17` (line 66) |
| framework/VERSION | Complete | 17 |
| framework/lib/adapters/common.sh | Complete | `hpcw_claude_signin`: only a subscription sign-in counts (PR #1) |
| framework/lib/login_plain.sh | Complete | Refuses the Console sign-in by host (PR #1); never signs out (PR #2) |
| framework/jobs/worker.sbatch.tpl | Complete | Worker under tmux in Apptainer; one `afterany` successor; strips 15 key, token, gateway and provider variables |
| framework/profiles/wayne.json | Complete | Canonical Wayne State profile; byte-identical to the copies in beethoven-extension and beethoven-desktop (sha256 cd718ac8...) |
| docs/V11_CONTRACT.md | Complete | Byte-identical with beethoven-extension's branch d6db850 (blob e6f8907); the extension's main still differs until its 15.0.0 merges |
| docs/V12_CONTRACT.md | Pending | On GitHub line 57 names only the script kind of helper; the desktop thread's patch (commit ed94b6b, `/mnt/project-files/staging/desktop-thread/hpcworker-v12-contract-signed-installers.patch`) applied to b35952a gives the extension branch's exact blob 75f86cb (checked 21:15Z) and rides PR #3. The extension's branch d6db850 adds the binary kind (runtime `rust`), a section "Signed installers (15.0.0)" and a line naming this copy canonical ("this copy and that one change together, in the same words"); this copy needs the same text |
| CLAUDE.md | Pending | Line 55 still says "One person, one account." (D4 withdrew it); line 141 states texts versions 8 and 9 where LICENSE.txt and PRIVACY.md say 9 and 10; line 160 says commit directly to main |
| framework queue report (`hpcworker queue report [--days N] [--limits]`) | Pending | Pushed as `claude/project-thread-fx3wkp` b35952a: one commit on main 20e2e97, 8 files +542/-9 (`framework/bin/hpcworker`, the slurm, pbs, lsf and common adapters, `framework/tests/test_queue.py`, `fakegrid.py`, README); no PR #3 and no CI run. Its review's 20 findings are not fixed there (the first: the wait counts a chained worker's whole parent run, inflating requeue); half-done fixes in `/mnt/project-files/staging/desktop-thread/hpcworker-queue-fix.wip.patch` |

## 4. Completed Milestones

1. Framework 17, "no API key anywhere": PR #1 (head 6eff9e9) merged by greg 2026-10-04T16:35:45Z as be0c503. Ledger 16:12Z: `framework/tests/run.sh` 404 cases, one known failure that occurs only as root and also on clean main.
2. Framework 17, a fresh grid sign-in never signs anyone out (`connect --login fresh` refused at the flag check): PR #2 (373e93a) merged by greg 18:13:41Z as 20e2e97; both CI lanes green on 20e2e97 (ubuntu 18:21:56Z, centos 7 18:23:22Z).
3. Grid CI lane: commit status `grid/framework-suite-py36` success on 2e5bcf8, "381 tests, ALL OK on sfx10 under python 3.6" (2026-10-03T20:27:58Z). 2e5bcf8 is still framework 15 by its VERSION; framework 16 is 6bf8167, that tree plus the bump, and no framework 16 commit has a grid success (6bf8167 has no status, 73af802 is pending).
4. Earlier measurements (CLAUDE.md grid section): Remote Control registers from an sbatch job under a pseudo-terminal (2026-09-29, job 40496445); compute-node egress matrix (2026-09-28).

## 5. Active Blockers & Errors

- No open PR; main 20e2e97 is green. The queue report on b35952a has no PR; the staging patch (6 files, +443/-172) applies cleanly to b35952a (`git apply --check`, 20:33Z), was taken mid-edit and has not been run through the suite; the findings are in `hpcworker-queue-review-findings.txt` and the PR body draft in `hpcworker-pr3-body.draft.md` beside it. Whether Wayne State's sacct writes Eligible as Unknown for a held job is not yet measured.
- Remote branch `claude/project-thread-2udoqz` (f4c621f, the replan thread's D4 sentence for CLAUDE.md:55) was never merged and has no PR: `git merge-tree` reports "CONFLICT (content): Merge conflict in CLAUDE.md".
- Grid lane: `grid/slurm-in-container` has never passed ("the container check failed (CANCELLED+)" on 759c129); 73af802's `grid/framework-suite-py36` has read pending since 00:59:13Z; no framework 17 commit has a grid status.
- The VS Code edition's grid commands `access init` and `library publish` close shared/ and shared/beethoven to other, which takes this repository's shared copy and the image away from students reached only through the root's ACL list, and `access admin approve` turns a student's `rwx` root entry into traverse only (checked 21:18Z; `repos/beethoven-vscode.md`). greg should not run them until VS Code's grid scripts 9 land.
- Not yet measured: framework 17 on the grid (both PR messages say "Not run on the grid"); which framework version the lab's shared copy serves (docs disagree: `docs/guides/LAB_LEAD.md:54` says framework 10, `docs/V12_STATUS.md:560` says 13 not deployed; nothing records 14 to 17); the first whole run timed; `srun` without `--pty` relaying stdin.
- Running the suite in a cloud session with a long `TMPDIR` failed five `test_job` cases (the socket path exceeded 108 characters; cause inferred). Use `TMPDIR=/tmp`.
- Waiting on greg: deploy framework 17 with `tools/deploy_shared.sh` from his laptop; run `tools/grid_ci.sh --ref main --container` on the cluster; copy `automerge.yml`, `rulesets.yml` and `rulesets/main.json` from beethoven-desktop with the required checks renamed to `suite (ubuntu, current python)` and `suite (centos 7, python 3.6, bash 4.2)`; decide branch 2udoqz; choose the two-queue worker policy after reading the queue report; the fourth-repository idea for grid rules (floated 15:19Z, not decided).

## 6. Immediate Next Actions (Hydration Directives)

1. Run `git -C <checkout> fetch origin --prune --tags` and `gh api "repos/OpenSpineConsortium/hpcworker/pulls?state=all&per_page=10"`; confirm main is still 20e2e97 and whether the desktop thread has moved `claude/project-thread-fx3wkp` past b35952a or opened PR #3 (queue report) before touching anything.
2. If its work is lost: on b35952a run `git apply /mnt/project-files/staging/desktop-thread/hpcworker-queue-fix.wip.patch`, finish the 20 findings in `hpcworker-queue-review-findings.txt`, `git am` the V12 patch beside it, run the suite, and open PR #3 ready with greg assigned from `hpcworker-pr3-body.draft.md` (its Verified and How paragraphs updated); greg measures it on the grid before choosing the two-queue policy.
3. Run `TMPDIR=/tmp HPCW_PYTHON=python3 bash framework/tests/run.sh` and expect 404 cases on main with only the known root-only `browser-key add` failure.
4. Make sure the V12 patch (ed94b6b) reaches GitHub with PR #3 (if the desktop thread's work is lost, `git am` it from the staging folder onto the branch), so it lands before or with the extension's 15.0.0; settle CLAUDE.md:55 (D4) and :141 in one PR opened ready for greg's hand merge, or ask him to delete branch 2udoqz.
5. After greg deploys or runs `tools/grid_ci.sh`, record the shared copy's version and the grid statuses for 20e2e97 in `docs/OPEN_QUESTIONS.md` and append a row to `/mnt/project-files/ledger/LEDGER.md`.

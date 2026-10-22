**Describes:** 2026-10-22 14:57Z for the section "Since 2026-10-09" (git and GitHub read at 09:17-10:00Z, every claim checked again by five independent readers at 14:25-14:50Z); the sections after it describe 2026-10-09 02:39Z, with qa 5.0.0's pull request #8 (who works which repository, and the work handed over between them)

# Who works which repository, and what was handed over

## Since 2026-10-09 (read from git and GitHub on 2026-10-22, 09:17-09:55Z)

The home project's threads stopped on the organization's spend limit at 18:52Z on 2026-10-09 (this
thread and the extension thread; again on 2026-10-13 and 2026-10-14; the record is the threads'
own error turns, `THREADS.md`) and changed nothing until 2026-10-22, when both ran again; this
thread stopped once more on the same error from 10:05Z to 14:19Z that day. Sessions outside the
project kept working: hpcworker #13 to #32, beside one commit made in GitHub's web editor under
greg's account (12e34b2, 2026-10-17 18:13Z, the runner's test step in `ci.yml`), beethoven-extension
#10 to #23 and beethoven-qa #10 and #11 (merged by qa's own auto-merge on 2026-10-20);
beethoven-vscode took Dependabot's #16, #18 and #19. Each of those pull requests was merged under
greg's account; sessions act as that account, so GitHub does not show who pressed. The branches,
and the sessions their commits name in their `Claude-Session` lines (none is a thread of this
project; which account or project each belongs to is not on record):

- `claude/grid-runner` (hpcworker #13): `session_01DMFNxL4f71XReWsmCdEVsm`.
- `claude/grid-ssh-gate-4wx0ul` (hpcworker #14 to #17, extension #18) and `claude/update-check`
  (extension #19): `session_01UR7rJM2QMkL1g2oRBKhRVT`.
- `claude/project-thread-h72c2u` (hpcworker #18 to #30, extension #20 to #23, beethoven-vscode's
  draft PR #20): `session_015rfHkSz1dpZJCo22ofiFTR`.
- `claude/project-thread-jr9apa` (hpcworker #31): `session_01EkjUa44HX16NhFcV5LLZzJ`;
  `claude/project-thread-00ov1t` (hpcworker #32): `session_01SaaHffGtrFBXcWrnWqNnto`.
- extension #10 (`claude/any-installation`): `session_01SEcUB5mdFshEKgiQqdpdK2`; #11 to #15 (five
  branches): `session_01NPTuud8aWm8oQSpE2uc7H3`; #16: `session_01EdvjAjU6Rc7mjxH34gJzdp`; #17
  (`claude/project-route`): `session_01U3X5TZ4yMBo3srmV3anMWu`.
- qa #10 (`claude/kit-hook-name`) and #11 (`claude/release-by-workflow`):
  `session_01Pc1tx7LutSxyU1XKXSV5Qc`.
- vscode #16, #18 and #19: Dependabot's own `dependabot/npm_and_yarn/extension/*` branches.

beethoven-agents, beethoven-research and beethoven-desktop have no commit since 2026-10-07.
beethoven-base and beethoven-sites cannot be read from this session.

**A new merge rule, 2026-10-22 02:02:46Z.** Organization ruleset 25608346, "Require owner approval
to merge", is active on the default branch of at least hpcworker, beethoven-extension,
beethoven-qa, beethoven-agents, beethoven-research, beethoven-desktop, beethoven-vscode and this
hub (read with `gh api repos/OpenSpineConsortium/<repo>/rulesets`; the organization's own endpoint
is refused to sessions, and beethoven-base, beethoven-sites and the organization's other
repositories cannot be read; the study repositories under Gregory-Schwing-MD-PhD are outside the
organization and carry no ruleset): no deletion, no force-push, changes only through a pull request
with one approving review by someone other than its author and its last pusher, stale approvals
dismissed. Organization admins bypass it. Who made it and why is not on record here. Inferred from
the rule: session pull requests are opened under greg's account (every session pull request named
above has the user `Gregory-Schwing-MD-PhD`; the Dependabot ones are `dependabot[bot]`'s), and
GitHub never lets an author approve their own, so a session's pull request merges only through an
organization admin's bypass; and an auto-merge armed by `automerge.yml` would wait for a review it
cannot get, so qa, agents, research and desktop should no longer merge on green (not yet seen:
none of the four has opened a pull request since the rule). The vscode Dependabot bumps
(04:38-04:39Z) and hpcworker #31 and #32 (04:54Z, 05:34Z) merged after the rule with no review, so
through the bypass. This thread's hub sync c1dd9b9 (09:19Z) also went in through the bypass, before
the rule was seen; greg is asked on a card (09:21Z) whether hub syncs go by pull request, and until
he answers this refresh is hub pull request #6, from branch `claude/handoff-state-file-m0rg4r`.

**beethoven-extension's lane.** The table below has the extension as the home project's, pending
greg's word. In practice every extension change since 2026-10-11 (PRs #10 to #23, 20.0.0 to
23.0.0) came from outside the project, and the home project's extension thread's last change is
PR #9 (documents written 2026-10-09, merged under greg's account on 2026-10-13); it holds nothing
in flight. This file now reads the row as: worked outside the project, like hpcworker. greg has
said nothing either way on record; the hub's `LANES.md` says the same in pull request #6.

### What changed, by repository

- **hpcworker** (main 8e73104, 2026-10-22 05:34Z; framework 27; no tags). Framework 19 is not the
  race: it is PR #18 (a worker whose Remote Control prints no link within 600 s restarts it once,
  then ends its chain). 20 (#19): the chain ends at once when Remote Control is not enabled for the
  account (go2432's grid sign-in belonged to a cancelled account, the commit says). 21 (#20):
  `hpcworker accounts`, up to 32 numbered accounts under `~/.beethoven/accounts/<N>`, the profile's
  sign-in folder a link to the one in use; in auto mode (`hpcworker accounts auto on`), the main
  worker moves at 90 % of a window to the signed-in account with the most room. 22 (#21):
  several workers at once, each kept to its account (no swap, no auto mode). 23 (#22): `accounts log`. 24 (#27): the
  sign-in and usage jobs run `bin/hpcworker` through bash. 25 and 27 (#28, #30): `hpcworker job
  submit|status|log|cancel|version`, placement from the site profile by class, job interface 2; the
  profile gains `qos_gpu` and `node_domain`. 26 (#29): `framework/sites` re-pinned to
  beethoven-sites 198c834 (Wayne State gains the GPU partition `galhp`). Beside the framework: a
  GitHub Actions runner on the grid as a chain of Slurm jobs (#13, with 12e34b2); the ssh gate, a forced-command
  key a GitHub workflow uses to say start, status or stop (#14 to #17, with `grid-gate-setup` and
  `grid-gate-off` in `cli.json`); and the gate words `accounts`, `update`, `promoter`, `schwingnet`
  and `artifacts` (#20 to #32), sent by workflows of symphony-template, SchwingNet and
  spine-datasets (none of the three is readable here). Every export in `interface/INTERFACE.json`
  is still version 1 (last changed 974ab8c, 2026-10-07).
- **beethoven-extension** (main e6ee0f6, 2026-10-21 20:18Z; 23.0.0): `repos/beethoven-extension.md`,
  refreshed today.
- **beethoven-qa** (main 3cdaa17): 6.0.0 (PR #10: the kit's session hook renamed
  `.claude/hooks/beethoven-qa-session-start.sh`, kit export 3); tag v6.0.0 on 8e5628a, its release
  published under greg's account on 2026-10-20 at 16:52Z. PR #11 added `release.yml` to tag each release from main (greg,
  2026-10-20: tags by the workflow, never by hand); it has never run (`total_count` 0), since a
  merge by `automerge.yml`'s `GITHUB_TOKEN` starts no workflow. v4.0.0 and v5.0.0 were never
  tagged, yet `docs/CONSUMING.md:725` and `:734` name them, and its step 1 (`:73`, `:83`) still
  adopts v3.0.0.
- **beethoven-vscode** (main 74d73d8): three Dependabot bumps only, merged under greg's account on
  2026-10-22 at 04:38-04:39Z with no CI (the repository has none). Draft PR #20 (15c0764, 2026-10-21) takes the
  grid placement from the site profile through beethoven-base; its `npm run test:vscode` has not
  run. Still 5.0.0, untagged and unreleased.

### The items handed over, as of 2026-10-22

| Item (where it was handed over) | Now | Checked |
| --- | --- | --- |
| hpcworker, workers on every queue (desktop thread, 1) | Not built under any number; the snapshot 9208ca2 is still unmerged; the measure-first job has no record. It would now be framework 28 or later | `git grep -E 'worker_queues\|HPCW-STEP candidates\|--race' origin/main` finds nothing |
| beethoven-vscode 5.0.0 on the grid (desktop thread, 2) | No record of the test; the step-by-step for grid scripts 10 was never written | vscode main has only the Dependabot commits since e7526f9 |
| Contract re-pin in the extension and desktop (desktop thread, 3) | Waits on the race; the extension pins hpcworker a0ac0ed (framework 18's vectors) | extension `framework/contract/ORIGIN` |
| hpcworker re-pin of `framework/sites` (site-module thread, 11:10Z) | Done in PR #29, to 198c834; its ORIGIN still lacks the `export modules 1` line `pull.sh` writes, so how it was written is not established | hpcworker `framework/sites/ORIGIN:2` |
| BEE-200's second half (site-module thread, 11:18Z) | Not started | no `example-modules` in hpcworker |
| BEE-218: module-schema keys and the text lookup (site-module thread, 15:18Z, 1) | Not started; the extension's AccessID word (`model.ts:48-49`) and U-12 to U-17 still wait on it | none of the keys in `profile.py` or `module-schema.json` |
| The extension notes of 15:18Z (`ssh_relay`, `DEFAULT_SITE`, `expandPath`) | Settled by 16.0.0 and 17.0.0: the relay went with the direct way, `DEFAULT_SITE` and `siteFromHostname` went in 17.0.0 (`keys.ts:404`), and `expandPath` is the pinned base's (`contract.ts:70`, `base/profile.ts:132`) | extension main |
| qa into agents and research (code-quality and QA threads) | Not done; both still pin v3.0.0. No longer blocked on a tag (v6.0.0 exists), but 3.0.0 to 6.0.0 is every step of `CONSUMING.md:723-805`, and the pull request now needs greg's merge (the rule above) | `vendor/beethoven-qa/ORIGIN` in both |
| The four agents functions before 5.0.0 | Unchanged | `bee/accounts.py:551`, `bee/handoff.py:451`, `:484`, `guard.py:415` |
| U-22's wording in agents and research | Unchanged | `ci.yml:3` in both; agents `site.sh:8`, `docs/bee/STATE_HANDOFF.md:172` |
| agents `managed-settings.json:15` "no hooks", the image recipe, BEE-103 | Unchanged; BEE-103 In Progress since 2026-10-04 | agents a40a71a; Linear |
| vscode CI and its repository half | Still none; the organization rule now covers its main | vscode `.github/` |
| hpcworker CLAUDE.md lines 67-76 (extension thread, 2026-10-09: beethoven-extension `docs/V19_STATUS.md` 2.5) | Still stale: `webRequest` among the permissions never requested (`:69`), the 12.0.0 bridge (`:70-73`), "No automated login of the portal" (`:75-76`). Also stale: `:155-156` (the gate as start, status and stop only) and `:183` (texts 8 and 9; hpcworker's own are 9 and 10, the extension's 15 and 17). The replacement text is beethoven-extension `CLAUDE.md:71-89`. It needs an hpcworker pull request, then greg's merge; none is open | `git log -L67,76:CLAUDE.md origin/main`: last de02ee0 (2026-10-02) |
| `automerge.yml`, `rulesets.yml` and `rulesets/main.json` into hpcworker and the extension (`DECISIONS.md`, list of 2026-10-05, item 2; the QA thread, point 4) | Not done; under the organization rule they would not merge anything by themselves | `.github/` in both |
| hpcworker `queue report --days 30 --limits` on the grid (the coordinator's pending list; `repos/hpcworker.md`) | The command is on main; no run on record | `framework/bin/hpcworker:2139-2191` (`--limits` at `:2165-2190`) |

### Read today, for the outside lanes

Observations against the repositories' own CLAUDE.md texts, not established as faults: greg's words
in the sessions that built these may cover them, and none of those words is on record here.

- hpcworker's CLAUDE.md says nothing of frameworks 21 to 27 and still says "One person, one
  account." (`:55`).
- `hpcworker accounts code N CODE` takes the Claude sign-in code as an argument (`accounts.sh:16`,
  `:419`); only the `-` form keeps it out of argv (`:423`). The secrets rule (`CLAUDE.md:65-66`)
  keeps every secret out of argv; whether a one-time sign-in code counts is not settled.
- `accounts.sh:37` ties the account numbers to "the Symphony token pool's slot numbers", and
  `accounts_read.py:15` reads usage the way symphony-template's `tools/pool.py` does.
  symphony-template is not readable here, so whether that pool holds Claude tokens (against the
  no-`CLAUDE_CODE_OAUTH_TOKEN` and no-pooled-tokens rules) is not established.
- The gate word `artifacts` runs `rm -rf` on `~/claude-artifacts/<repo>` when a clone it began
  fails (`grid_gate.sh:466`, `:497`, `:506`), under a forced command with no terminal. The folder is
  one the same call made (`:490-493`); the deletion rule as written has no such exception.
- The gate words `update`, `artifacts`, `promoter` and `schwingnet` run git, `gh repo clone` and
  other repositories' scripts, fetched at their main, on the login node (`grid_gate.sh:64-95`,
  `:460-483`); CLAUDE.md's login-node exception covers only the lab lead's one press (`:161-164`),
  and its "No remote code" rule stands.
- Stale since the gate: `SECURITY.md:176-178` and `:196`, `README.md:338`, `CLAUDE.md:375-376`,
  `.github/workflows/ci.yml:3-5`, `docs/OPEN_QUESTIONS.md:168-169` (each says the gate, or GitHub's
  runners, can do less than they now do).
- The `HPCW-ACCOUNTS` lines (with `-JSON` and `-LOG-*`), the `HPCW-GRID-GATE` lines, the
  `accounts` verbs and the gate's words (start, status and stop as well as the newer ones) are in
  no published contract file; `cli.json`'s `grid-gate-setup` and `grid-gate-off` cover only the
  lab lead's two lines. The `HPCW-JOB` lines are in `cli.json`'s job entries (`:28-32`) but have no
  pattern in `lines.json`. symphony-template, SchwingNet and spine-datasets read them.
- hpcworker's account layout (`accounts/<N>`, the old folder renamed into account 1) differs from
  beethoven-agents' D4 layout (`accounts/<label>/claude`, nothing moved); whether the two were
  reconciled is not established.
- hpcworker's `LICENSE.txt` and `PRIVACY.md` (versions 9 and 10), which its CLAUDE.md calls
  canonical, lag the extension's (15 and 17); which copy the site publishes is not established.
- Wayne State's new values (`galhp`, `qos_gpu` `gpu`, `node_domain` `nas.grid.wayne.edu`) came from
  Beethoven for VS Code and were not measured by hpcworker (`framework/profiles/wayne.json:91`).

## The split, decided by greg on 2026-10-08 at 14:46Z

On 2026-10-07 two Claude Code sessions outside the home project worked on the repositories, and greg
merged their pull requests (checked against GitHub at 11:10Z):

- branch `claude/repo-encapsulation-9hmh9f`: hpcworker; beethoven-extension PRs #3 and #4;
  beethoven-desktop PRs #5 to #8; beethoven-vscode PR #15; beethoven-qa PRs #4 and #5;
  beethoven-agents PRs #4 and #5; beethoven-research PRs #6 and #7; this hub PRs #3 and #4
  (`INTERFACES.md`).
- branch `claude/oschome-access-approval-6prr38`: hpcworker PRs #7 to #12; beethoven-vscode PRs
  #13 and #14.

The coordinator asked greg on a card at 11:07Z how to split the work; at 14:46Z he chose "Split by
repo", its recommendation, as the coordinator reported at 14:49Z (the hub's `LANES.md` carries the
same table since greg merged its pull request #5 at 15:41Z):

| Repository | Worked by |
| --- | --- |
| beethoven-base | the home project (desktop thread) |
| beethoven-sites | the home project (site-module thread) |
| beethoven-qa | the home project (site-module thread; the code-quality thread finished its 4.0.0 work there on 2026-10-08) |
| beethoven-extension | the home project (extension thread, since 15:30Z; pending greg's word, see below). Since 2026-10-11 worked outside the project in practice (section "Since 2026-10-09") |
| hpcworker, beethoven-desktop, beethoven-vscode, beethoven-agents, beethoven-research | the sessions outside the home project |
| the hub | syncs and `state/` from the home project's hand-off thread |

beethoven-extension came back to the home project at 15:30Z on 2026-10-08: greg asked in the project
chat for the extension's remaining work (VPN only through GlobalProtect, a simpler interface, the
launch on every queue that takes the first allocation, a profile loader with Wayne State as the
default), and the coordinator started a thread for it here, telling him that is its default since he
asked here. That one row waits on his word: he may yet say his outside session keeps the extension.
The notes below addressed to the owners of beethoven-extension now go to that thread; it builds the
extension side of the worker race against hpcworker's main and sends what hpcworker must add to the
outside lanes through the coordinator.

A home-project thread holding unfinished work in a repository that moved outside changes nothing
there and hands the work over below.

## Handed over

Each note is the sending thread's, as it sent it, shortened; "checked" marks what the hand-off thread
confirmed on GitHub at 11:15-11:20Z, and everything else is as reported.

### From the desktop thread (11:08Z), for the owners of hpcworker, beethoven-vscode, beethoven-extension and beethoven-desktop

1. **hpcworker, workers on every queue** (greg 2026-10-04 23:26Z: launch on every possible queue,
   the first allocation answers the client). Branch `claude/project-thread-fx3wkp` at 9208ca2
   (checked) is an unfinished, unreviewed snapshot on the old main 5492d4d (32 files, suite not
   run). Main 3b22e70 (checked) already took framework 18 for the grid CI deploy (b578477,
   checked: `framework/VERSION` is 18), so this becomes framework 19, rebuilt on that main, not
   merged from the snapshot.
   - Design: the profile field `worker_queues`, an ordered list of `PARTITION` or
     `PARTITION/QOS`, at most four, more than one only on Slurm. Entries sharing a QoS become one
     job over a partition list; different QoS become separate jobs, the first to get a node claims
     the run and the rest are cancelled; no singleton dependency on the candidates. A client that
     cannot follow the race gets the first entry; an empty list keeps the old behaviour. Wayne
     State's value is `["reqp/requeue","secp/secondary"]`, which now belongs in the lab module
     (beethoven-sites).
   - The note asks to carry the extension's `docs/V12_CONTRACT.md` lines 109-113 word for word.
     Checked: the extension's copy now lives at `framework/contract-text/V12_CONTRACT.md`, a pinned
     copy of hpcworker's (since f22c7a2), and hpcworker main's `docs/V12_CONTRACT.md` already has the
     signed-installer lines from line 109; compare before carrying anything.
   - The site-module thread needs the final `worker_queues` shape (see its note below).
   - **Measure first** (the extension thread, 16:59Z, through the coordinator; it may show the race
     is not needed). Inside a Slurm job, before building anything: `sbatch --test-only -p reqp,secp
     -q requeue`, the same with `-q secondary`, `scontrol show partition reqp secp` and `sacctmgr
     show assoc user=$USER`. If one QoS is accepted on both partitions, the two-job race becomes one
     job over `-p reqp,secp` and no client changes; the race is needed only if each partition
     insists on its own QoS. Either way the Claude sign-in sitting is single-queue
     (`framework/bin/hpcworker:1358` and `:1601` call `adapter_interactive` with the profile's CPU
     partition and QoS and a 600 s allocation wait; `framework/lib/adapters/slurm.sh:122` is its
     `srun`; checked on main 3b22e70). The extension thread places hy9698's exit-3 sign-ins of
     2026-10-03 there (a 4 min 20 s wait inside the sitting); the snapshot does not touch it, and
     the sitting is the first place a multi-queue launch would help.
   - **If the race is built**, the extension thread's list, in its words, for framework 19 from the
     snapshot ported to main 3b22e70: `worker_queues` as a lab field in `FIELD_LAYERS`
     (`framework/lib/profile.py` from line 394); the module schema regenerated (`profile.py
     schema`) so beethoven-sites can carry it; `interface/contract/cli.json` `connect [--race]` and
     the gate's seventh word `race`; a `lines.json` entry `{"id":"candidates","pattern":"^HPCW-STEP
     candidates ([0-9]+(?:,[0-9]+)+)$","groups":["jobs"]}`; `candidates` in `status.schema.json`
     (queued) and `worker-status.schema.json`; the testbed's fake `sbatch` and `scancel` for two
     jobs and a claim; the vectors rewritten (`python3 framework/tests/vectors.py --write`);
     `docs/V11_CONTRACT.md` rule R1' and `docs/V12_CONTRACT.md`'s gate word; the `contract` export's
     version raised so clients act. Then the site-module thread adds `"worker_queues":
     ["reqp/requeue", "secp/secondary"]` to beethoven-sites' `labs/oschome.json` after the schema
     lands, and hpcworker pulls and composes.
   - The extension builds its `candidates` reader only after that contract export is published:
     its conformance tests and `interface/pull.sh` refuse a reader the export does not carry.
2. **beethoven-vscode 5.0.0 on the grid.** greg chose "Test on grid first" on a card at 01:17Z on
   2026-10-05: `npm run test:vscode`, then 5.0.0 on his own grid account (setup, claude login,
   phone, Reset), then `tools/release.mjs` and the listing. The desktop thread promised him a
   step-by-step; its draft was written against e342c7f (grid scripts 9) and never sent. Main
   e7526f9 (checked) now ships grid scripts 10 under 5.0.0, so the steps are to be rewritten
   against scripts 10 before greg sees them.
3. **beethoven-extension and beethoven-desktop:** after the race merges in hpcworker, re-pin
   hpcworker's contract (the interface standard's waves A and B) so `contract.ts` reads the race
   lines; never hand-edit them.

The desktop thread keeps beethoven-base: branch `claude/project-thread-fx3wkp` 7c141a9 (the
skeleton, gate passed), being checked against `INTERFACES.md`; its pull request needs greg's hand
merge. It notes that `repos/hpcworker.md` and `repos/beethoven-vscode.md` still describe 2026-10-05
00:15Z.

### From the site-module thread (11:10Z), for the owners of hpcworker and beethoven-extension

Nothing of the site-module thread's is in flight in either repository.

- **hpcworker, re-pin `framework/sites`.** `framework/sites/ORIGIN` on main 3b22e70 names
  beethoven-sites 7d91f66 (checked), the head of beethoven-sites PR #1, which that repository's main
  contains through merge 8e27eaa; the ORIGIN has no `export` line yet. beethoven-sites main is
  c6bc0f4; both module files there are byte-identical to the pinned copy (wayne/site.json sha256
  21a89f04..., wayne/labs/oschome.json f0477720..., matching the ORIGIN lines, checked). Next:
  `bash framework/sites/pull.sh` (it now takes main through gh), then
  `python3 framework/lib/profile.py compose-all`; expected: ORIGIN gains `export modules 1` and a
  newer commit, no profile changes; both in one pull request, with BEE-200.
- **hpcworker, the other U issues.** U-1 (BEE-199) and U-3 (BEE-201) are Done. Backlog: U-2's
  hpcworker half (BEE-200: every suite run once per site module, expected values in `expect.json`,
  scheduler fixtures per site) and U-4 to U-11 (BEE-202 to BEE-209). Design: `sites/DESIGN.md`;
  each issue lists its files and lines. When the all-queue launch lands, `worker_queues` needs a
  `FIELD_LAYERS` and `SUBFIELDS` entry with layer `lab`, and a new module-schema export for
  beethoven-sites to pull.
- **beethoven-extension, U-12 to U-17 (BEE-210 to BEE-215)**, not started, plans in Linear: U-12
  the site chosen by the module's own match list; U-13 every Wayne State value read from the
  profile, with a site-literal lint like hpcworker's `test_site_literals.py`; U-14 the student's
  words from a text bundle, Wayne State's sentences unchanged; U-15 portal sign-in, second factor
  and VPN by the module's declared kind; U-16 the bridge helper's allow list generated from the
  bundled modules; U-17 the mock portal, the ssh stand-in and the fixtures serving any module.
  Before changing `extension/src/core/contract.ts`, tell the server lane; the extension's main has
  no auto-merge.

The site-module thread keeps beethoven-sites. Its second note (11:18Z, not checked here: this
session cannot read beethoven-sites):

- **beethoven-sites:** branch `claude/site-module-9x2ggm` at 24309e4 on main c6bc0f4; PR #4 is
  ready and merges itself on green. It adds `examples/example/`, Example University, a synthetic
  site for BEE-200, offered as a new export, `example-modules` version 1 (`examples/*/site.json`,
  `examples/*/labs/*.json`), never inside `modules`, so hpcworker's `pull.sh` never takes it and no
  example profile ships. The checker refuses an example with a host or link that is not reserved,
  a measurement, or an id a real deployment has.
- **hpcworker, BEE-200's second half** (details in a Linear comment there): take `example-modules`
  into the tests with a pull of its own (for example `framework/tests/sites/` with an ORIGIN),
  compose it into a temporary folder, never into `framework/profiles/`, and run each suite once per
  module. Composed with hpcworker main 3b22e70 the example already validates with `profile.py` and
  `profile.awk`, and its worker job renders and passes `bash -n`. Two Wayne-only assumptions it
  shows: the workspace guide calls every lab bind "the person's folder on the lab's storage", and
  the worker job never reads `cache_dir`.

### From the code-quality thread (12:13Z, via the coordinator), for the owners of beethoven-agents and beethoven-research

- **beethoven-qa 4.0.0 merged at 12:11Z** (PR #6, merge commit 615ed3e on main, checked). It adds
  the `coach` command and a `PostToolUse` hook to the plugin: after each Edit or Write it tells the
  session what CI would block in that file, and it never stops the edit.
- **greg's hand step:** create the tag `v4.0.0` on 615ed3e (checked at 12:14Z: the tags are
  v1.0.0, v2.0.0 and v3.0.0; no v4.0.0 yet).
- **After the tag:** whoever owns beethoven-agents and beethoven-research (the outside sessions,
  under the split) re-pins both with `vendor --into <repo> --ref v4.0.0 --kit`; qa's
  `docs/CONSUMING.md` has a section "From 3.0.0 to 4.0.0" (checked, on main).
- **Not yet measured:** the hook inside a live Claude Code session, and whether
  `allowManagedHooksOnly` in the agents' image lets the plugin's hook run there.
- **U-22 (BEE-220, a qa docs fix)** now goes to the site-module thread, in beethoven-qa.

The code-quality thread's work in beethoven-qa is finished; the repository stays with the home
project through the site-module thread (coordinator, 14:49Z).

### From the site-module thread (13:02Z), for the owners of beethoven-agents and beethoven-research

- **U-22 (BEE-220) merged in beethoven-qa** at 13:01Z (PR #7, merge commit b73d4f4 on main,
  checked; one docs commit, 552c0af, after 615ed3e). qa's docs now say hpcworker keeps to the oldest
  Python on a supported site's login node (3.6 today, Wayne State's CentOS 7, as its site module
  records), not "the grid's". At 13:02Z qa still has no v4.0.0 tag (checked); the release tag that
  carries this to consumers is greg's.
- **The same wording is still on main in two repositories outside this project's lanes**, in files
  that are not kit files, so no pinned copy carries the fix (each line checked on main):
  - beethoven-research 7e8fd69, `.github/workflows/ci.yml:3`: "none reaches the grid: GitHub's
    runners cannot (VPN and a one-time code stand between)". qa's version now reads "none reaches a
    university's cluster: GitHub's runners cannot (the university's own sign-in stands between, at
    Wayne State a VPN and a one-time code)".
  - beethoven-agents a40a71a: `.github/workflows/ci.yml:3` (the same line),
    `src/beethoven_agents/site.sh:8` ("Python 3.6 on CentOS 7 nodes") and
    `docs/bee/STATE_HANDOFF.md:172` ("the grid's CentOS 7"). `docs/bee/RUNBOOK.md:148` is a
    Wayne State measurement and can stay.
- Details in Linear BEE-220.

### From the site-module thread (15:18Z), for the owners of hpcworker, beethoven-extension and beethoven-desktop

U-20 (BEE-218) part one is beethoven-base PR #2 (not checked here: this session cannot read
beethoven-base): `src/profile.ts`, base's first module, in two new exports, `desktop` and `browser`.
Its tests take hpcworker's `profiles` and `module-schema` and beethoven-sites' `modules` and
`example-modules` as pinned imports. The rest of BEE-218 is in the outside lanes (each point below
checked on main, except where it says otherwise, at 15:19Z: hpcworker 3b22e70, beethoven-extension ae11a00, beethoven-desktop 9ce98bb):

1. **hpcworker.** BEE-218 names keys that module-schema 1 lacks: `match`, `texts`, `portal`,
   `second_factor`, `account_id`, `vpn`, `ssh_options`, `rules`, and a `text(key, site, vars)`
   lookup (checked: none is in `framework/lib/profile.py`). Base reads only what the schema states,
   so they go into `FIELD_LAYERS`, `SUBFIELDS` and the `module-schema` export first, and base reads
   them after that. Informative only: add OpenSpineConsortium/beethoven-base to the `consumers` of the
   `profiles` and `module-schema` exports in `interface/INTERFACE.json` (checked: not there).
2. **beethoven-extension.**
   - `SiteProfile` types `ssh_relay` as `{ url?, ticket_url? } | null`
     (`extension/src/core/contract.ts:680`, and `relayConfigFrom` in `extension/src/core/bridge.ts:109`
     reads it so). Module-schema 1 says `str_or_none` (hpcworker `framework/lib/profile.py:110`), and
     Example University's relay is a `wss://` string (in beethoven-sites, not checked here), so the
     type is wrong.
   - Design step 11 (taking base's `browser` export) can replace `DEFAULT_SITE = 'wayne'`
     (`extension/src/entrypoints/background.ts:135`) and `siteFromHostname`
     (`extension/src/core/keys.ts:336`) with base's `deploymentFor` (U-12, BEE-210).
   - The extension's `expandPath` (`extension/src/core/contract.ts:190`) turns `$USERNAME` into the
     user name followed by `NAME`, since its pattern `\$\{?USER\}?` has no word boundary; base's
     `expandPath` expands on a word boundary.
3. **beethoven-desktop.** Design step 10 can replace `profileFrom`'s checks (`src/profile.ts:44`)
   with base's `sshTargetOf` and `stateDirOf`, mapping their codes to the desktop edition's own
   sentences.

### From the QA thread (17:31Z, through the coordinator), for the owners of beethoven-agents, beethoven-research and beethoven-vscode

The QA thread read these and pushed nothing (each point checked on main at 17:31Z: agents a40a71a,
vscode e7526f9, qa b73d4f4).

1. **beethoven-agents and beethoven-research, after greg tags beethoven-qa v4.0.0** (still only
   v1.0.0 to v3.0.0, checked): re-pin both off the tag with `pixi run --locked python -m
   beethoven_qa vendor --into . --ref v4.0.0 --kit`. The five kit files (`KIT` in qa's
   `src/beethoven_qa/vendor.py`) are byte-identical at v2.0.0, v3.0.0 and qa main (checked), so
   `--kit` changes nothing. Optionally name
   `plugin/hooks/coach.sh` in each `.claude/settings.json` (qa `docs/CONSUMING.md`).
   **Then qa 5.0.0, which supersedes the 4.0.0 re-pin once greg tags v5.0.0.** It is beethoven-qa
   PR #8, head a4ac562 on `claude/qa-assessment-4x85zq` (checked 2026-10-09 02:39Z; auto-merge armed
   and the pre-push gate green, as the QA thread reports); greg tags v5.0.0 on its merge commit,
   and v4.0.0 is still untagged on 615ed3e. The steps for consumers are qa's `docs/CONSUMING.md`,
   section "From 4.0.0 to 5.0.0" (line 731 at a4ac562), which names the four functions below. The
   gate runs CrossHair with every condition's verdict on every run, so a precondition no input can
   meet fails it. The QA thread's read-only measurement at 17:42-17:50Z on 2026-10-08, nothing
   pushed:
   - beethoven-agents: `python -m beethoven_qa gate --report-all` exits 1 at a40a71a. Four targets
     report "Unable to meet precondition": `beethoven_agents.bee.accounts.host_transcript`
     (`accounts.py:544`), `bee.handoff.extraction_prompt` (`handoff.py:451`),
     `bee.handoff.hydration_prompt` (`handoff.py:484`) and `guard.check_path` (`guard.py:415`)
     (the four functions checked on main; the gate's verdicts as reported). 11 conditions
     confirmed over all paths, 54 not confirmed at the bound, 5 min 56 s on 4 cores. Fix, as in
     qa's own `level_for`: restate each precondition over values CrossHair 0.0.111 can build (an
     enum instead of a string checked against a set; CONSUMING.md at a4ac562 says a `Literal`
     makes CrossHair 0.0.111 raise, correcting the earlier note), state a path's domain in a form
     it can build, or list the function under `[tool.beethoven-qa.unproven]` with that reason.
     Needed before agents re-pins to 5.0.0, not before.
   - beethoven-research: exits 0 (0 confirmed, 6 not confirmed at the bound, 1 min 44 s); nothing
     to do.
   - What else the 5.0.0 re-pin brings, from the QA thread's build plan (17:59Z, through the
     coordinator; not checkable until its branch is pushed):
     - **Kit changes**, carried by each consumer's next `vendor --kit` (corrected by the QA thread
       at 18:01Z from qa's own source). The kit has been five files since 2.0.0 and stays so:
       `.githooks/pre-push`, `.github/workflows/automerge.yml`, `.github/workflows/rulesets.yml`,
       `.claude/hooks/session-start.sh` and `.github/workflows/standards.yml` (checked: `KIT` in
       `vendor.py` and the `kit` export, version 1, in `interface/INTERFACE.json` on qa main
       b73d4f4). Three change in 5.0.0: `standards.yml` (the pixi digest check and the Scorecard
       reporter job), `session-start.sh` (the digest check) and `automerge.yml` (its header comment
       on the strict-checks policy); the `kit` export goes to version 2.
     - **Not kit files:** `ci.yml` and `.github/rulesets/main.json` are each repository's own. qa's
       `docs/CONSUMING.md` will tell each consumer to make the same two edits there by hand (the
       pixi digest check, the strict-checks flag) in the same change as the re-pin.
     - **Three tools** each consumer adds to its `pixi.toml`: jscpd (in place of the home-made
       duplication detector), zizmor (beside the supply-chain reader, with Scorecard as a
       non-blocking CI reporter) and lizard (function length). qa's `docs/CONSUMING.md` will give
       the exact step; the lock changes on purpose.
     - Also new: a no-suppression check in the gate, and `python -m beethoven_qa report`, which
       writes an evidence report (`report.md`, `report.json`: tool versions from the lock, every
       verdict with its command and exit code, proof counts, enforcement, and what no model
       decided).
     - All of it waits on greg tagging v5.0.0; the QA thread will say when its pull request is up
       and when it merges.
2. **beethoven-agents:** `containers/managed-settings.json:15` says the pinned plugin has "no
   hooks"; that is stale once the copy is 4.0.0.
3. **beethoven-agents:** `containers/claude-verify.def` is not reproducible as a recipe: line 47
   pipes the nodesource setup script into `bash`, line 50 installs `@anthropic-ai/claude-code`
   unpinned, and lines 56-57 fetch pixi with no checksum. The grid build and the committed digest
   (BEE-103) are still open.
4. **beethoven-vscode:** no CI workflow at all (`.github/` holds only `CODEOWNERS`,
   `dependabot.yml` and the pull request template), and its repository half (ruleset, auto-merge,
   pre-push gate) is unbuilt. hpcworker and the extension (`ci.yml` only, hand merges) are already
   in greg's pending list.

An operational fact, as the QA thread reports it (not checked here): in these sessions `gh run
list` and `gh api` answer through the proxy even though `gh auth status` calls the token invalid;
only the GitHub MCP server is refused with a 403. Its skeptics read six live rulesets and three CI
runs that way.

The QA thread keeps two items of its own: the stale beethoven-qa docs pull request (on greg's word)
and the G1 Linear corrections for BEE-105, 106, 107, 109 and 110.

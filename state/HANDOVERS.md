**Describes:** 2026-10-08 17:00Z, with the extension thread's measure-first step for the worker race (16:59Z) (who works which repository now, and the work handed over between them)

# Who works which repository, and what was handed over

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
| beethoven-extension | the home project (extension thread, since 15:30Z; pending greg's word, see below) |
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

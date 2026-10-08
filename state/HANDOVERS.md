**Describes:** 2026-10-08 11:20Z (who works which repository now, and the work handed over between them)

# Who works which repository, and what was handed over

## The split, provisional until greg answers the coordinator's card (2026-10-08 11:07Z)

On 2026-10-07 two Claude Code sessions outside the home project worked on the repositories, and greg
merged their pull requests (checked against GitHub at 11:10Z):

- branch `claude/repo-encapsulation-9hmh9f`: hpcworker; beethoven-extension PRs #3 and #4;
  beethoven-desktop PRs #5 to #8; beethoven-vscode PR #15; beethoven-qa PRs #4 and #5;
  beethoven-agents PRs #4 and #5; beethoven-research PRs #6 and #7; this hub PRs #3 and #4
  (`INTERFACES.md`).
- branch `claude/oschome-access-approval-6prr38`: hpcworker PRs #7 to #12; beethoven-vscode PRs
  #13 and #14.

The coordinator asked greg how to split the work. Until he answers, work follows its
recommendation (the hub's `LANES.md` carries the same table once its pull request merges):

| Repository | Worked by |
| --- | --- |
| beethoven-base | the home project (desktop thread) |
| beethoven-sites | the home project (site-module thread) |
| beethoven-qa | the home project (code-quality thread) |
| hpcworker, beethoven-extension, beethoven-desktop, beethoven-vscode, beethoven-agents, beethoven-research | the sessions outside the home project |
| the hub | syncs and `state/` from the home project's hand-off thread |

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

The site-module thread keeps beethoven-sites: U-2's synthetic example site, built on the interface
standard; its pull request and a note on what hpcworker needs to take the example as a test fixture
follow.

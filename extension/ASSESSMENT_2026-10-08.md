# Beethoven extension: what is left, against 15.0.0

Thread: "whats left to do on the extension?" (greg, 2026-10-08 15:30Z). Written 2026-10-08 ~17:00Z by the extension
thread from a read of `OpenSpineConsortium/beethoven-extension` main `ae11a00` (15.0.0), `hpcworker` main `3b22e70`
(framework 18), the worker-race snapshot `9208ca2`, `beethoven-base` main `c7682f6` and `beethoven-sites`. Six readers
each checked by a skeptic, then a critic over the whole; every claim below names the line it comes from or says "not
yet measured".

## 0. The decision, and the default I am building on

**Remove the direct ssh way (the bridge) rather than hide it**, and ship 16.0.0 as VPN-only. The card in the thread
asks this; until the answer comes the build proceeds on *remove*, which is reversible (one branch, one pull request).

Why remove, not hide: hiding leaves `nativeMessaging` in the manifest (`extension/wxt.config.ts:67`), a native host the
store reviewer must still justify, about 13,600 lines of dead code (helper 8,720 + direct UI and core ~4,900), the Mac-only
signed-installer release path, and an agreement that still describes a bridge students cannot use. Removing takes the
same text bump (LICENSE 11, PRIVACY 12, TERMS_VERSION 11) that hiding needs anyway, and leaves a client whose only
network is the portal the student grants. hpcworker needs no change either way: the gate stays for the desktop
edition, and a student who enrolled a browser key removes it with `hpcworker browser-key remove` through the portal's
shell (go2432 did enrol one on 2026-10-02, `docs/V12_STATUS.md:403`, so the cleanup step is real, not theoretical).

The smaller decisions I am taking by default (say so if any is wrong):
- the one-time terminal step for a student with no key (`LOGIN_SETUP_PROVEN = false`, `src/core/contract.ts:162`) stays
  as it is until measured on the grid; it is the VPN path's only unproven step;
- the multi-queue race is built in the extension only after hpcworker publishes it as framework 19 (details in §4);
  before that, one measurement decides whether the race is needed at all;
- a bundled profile list with Wayne State preselected, chosen by one build constant; no run-time profile download
  (that would be a signed fetch of a list, a new network request the privacy text would have to carry);
- PRIVACY gets a row for the in-memory debug log (`src/core/debuglog.ts`) in the same bump, since it has none today.

## 1. Where 15.0.0 stands

- Built, never released: no version was ever uploaded to the Chrome Web Store (`release/` holds 4.0.0 to 14.0.0, no
  15.0.0, no tags; nothing in `docs/store/` records an upload). The signed `.msi`/`.pkg` of 15.0.0 need Apple
  Developer and Azure Artifact Signing enrolments that do not exist yet; `public/bridge/manifest.json` lists three
  script zips and no signed package.
- greg's premise holds: every existing bridge installer (`helper/`, Perl, Python, PowerShell, the Rust edition's
  installer scripts) opens a console or Terminal and waits for a key, and the signed route that would avoid it is
  unmeasured on any real machine.
- Default is the direct way: `DEFAULT_PREFS.connection = 'direct'` (`src/core/keys.ts:318`); `connectionMode`
  (`src/core/steps.ts:248`) returns `'vpn'` only when the student chose it, the bridge is unreachable after the
  fallback was seen, or no bridge exists; `background.ts:712` builds the direct facts on every tick, and `onAgree`
  probes for a bridge on first run.
- The GlobalProtect way was run on the real grid once (hy9698, 2026-10-03): Connect queued a worker; her Claude
  sign-ins failed with exit 3 after about 4 m 20 s, which fits the single-queue `srun -p secp -q secondary -I600` wait
  inside hpcworker's sign-in sitting (`bin/hpcworker:1358, 1601`) under the sitting's 15-minute cap, not a
  portal fault. That is the first thing multi-queue should fix (§4).
- Tests: with `npm run sync-profiles` first, 51 files / 786 tests pass, typecheck clean; without it two suites fail
  (`background12`, `background14` read `public/profiles/wayne.json`). `npm test` has no pretest for it.

## 2. Enforce VPN: what "remove the direct way" is

Subtraction (~4,900 source lines plus `helper/`):
- `src/ui/direct.ts` (469) whole; `src/ui/model12.ts` and `src/ui/routes.ts` trimmed, not deleted (`routes.needsBlock`
  is used by `welcome.ts:196` and `panel.ts:380`; `WORDS12.loginSetupCode` by `journey.ts:278`); `ui/helperFile.ts`;
  `ui/qr.ts` and `vendor/qrcodegen.ts` stay (the home page's phone QR, `home.ts:12,62`);
- in `background.ts` the §12.0.0 block (2993-3617), `directFacts`, `probeBridges`, `modeNow`, `doorOf`, the
  `set-connection` action, the bridge probe in `onAgree`; in `steps.ts` `DirectFacts`, `directMoment`, the direct
  branches of `momentOf`/`studentMoment`/`toolbarView`; in `model.ts` `WORDS.direct` (366-615), `DIRECT_LINKS`, the
  direct moment types; `keys.ts` `DEFAULT_PREFS.connection`, `DIRECT_KEY`, `BRIDGE_KEY`; `contract.ts`'s ssh and
  gate-line readers (`gateLineFor`, `CONNECT_LINE_RE`, the sign-in sheet regexes), which the desktop edition keeps in
  its own copy;
- `wxt.config.ts`: `nativeMessaging` out, keeping `sidePanel` (the two share one spread at line 67);
- `helper/` and `public/bridge/` whole; the `bridge-binary` job in `.github/workflows/ci.yml`; the `framework` and
  `testbed` pins (`framework/shared-copy`, `framework/testbed`, taken only for the direct-way ssh lane) and their rows
  in `interface/INTERFACE.json`; the ssh tests and the e2e flows 13-16; `helper/release/release.sh` and
  `setup-mac.sh` go, `publish-store.mjs` (Node standard library only, `--require-signed` opt-in) stays as the store
  upload after a plain `npm run zip`.
- On update: delete `DIRECT_KEY`, `BRIDGE_KEY` and the IndexedDB database `beethoven-key` once; keep a *Forget this
  computer* row in Settings only while a key record still exists, which tells the student the one shell line that
  removes the key on the grid.

Texts, one bump for all of it: `LICENSE.txt` 10 → 11 (sections 1, 3(a), 3(e), 5(a), 5(b)(i)-(iv), 5(f), 10(a), 15,
17, 18 describe the bridge), `PRIVACY.md` 11 → 12 (the bridge rows, the sign-in sheet, the browser key; plus the
debug-log row), `THIRD_PARTY_NOTICES.md` items 5 and 6 (Rust), `TERMS_VERSION` 11 with a new `TERMS_DATE`
(`src/core/terms.ts:28-29`; `test/terms.test.ts:16-18` hardcodes 10), the copies in `extension/public/` byte-identical,
and the agreement shown and accepted again. The store listing texts (`docs/store/`) lose the bridge paragraph.

Behaviour (enforcing is more than subtracting):
- a press while the grid is unreachable is dropped today on the VPN path (`background.ts:1928-1929`); it must wait,
  as the direct way's press did (1897-1902), and go ahead by itself when the grid answers (`carryPress`);
- the GlobalProtect moment is shown only on first run (`steps.ts:480-491`); after it, "unreachable" must lead back to
  it, with the profile's `vpn_help_url` as a link (the moment type at `model.ts:814-824` has none);
- with the panel closed the background alarm only reads the run (`backgroundPoll`, 903-908); so a student who
  turns the VPN on sees nothing until they open the panel. One credential-free `no-cors` GET of the portal per
  alarm would give the toolbar an "unreachable" / "signed out" state. It is a new request on a timer; I will add it
  behind the existing *start my worker when I open my portal* setting rather than ask.
- *Keep my worker running* only acts when a run reads `ended`, and only from `onSignedIn` (2946-2956, 1628); a chain
  whose successor vanished reads `stopped` (`facts.ts:378-384`) and is never restarted. Restart it on panel open and
  on the alarm, at the 60 s floor.

## 3. Simplify the interface

- Welcome goes back to three needs: the portal grant, the grid sign-in, Claude sign-in; the bridge download, the
  key step and the sign-in sheet go (`ui/welcome.ts`, `ui/panel.ts` ORDER 44-57).
- Settings loses the Connection card (`ui/settings.ts:111-193`) and the "via" row (`ui/parts.ts:224-243`); the
  Details page loses its direct rows (`ui/details.ts:151-171`).
- The ⋯ menu (`model.ts:270`) and the tour (`ui/tour.ts:81`) lose their direct entries; the toolbar keeps four states
  (signed out, unreachable, in line, online).
- Wayne State literals stay in the texts until a second site exists (greg's BEE-222 answer); the profile loader (§5)
  is what lets them move later.

## 4. Seamless access: the multi-queue launch

What exists: hpcworker main is framework 18 and refuses `connect --race` (`bin/hpcworker:1633-1641`, "unknown option
--race", exit 2); the race lives only in the snapshot `9208ca2` (`worker_queues` list grouped by QoS, one `sbatch` per
group, at most four; `HPCW-STEP candidates L,B`; `candidates` in the queued `status.json` and `worker status --json`;
rule R1'; the first job to claim wins, the losers are cancelled; chain successors never race). The extension reads
none of it: `parseStepLine` (`contract.ts:428-457`) has no `candidates`, and the conformance tests plus
`interface/pull.sh` forbid a reader before hpcworker publishes the lines. A client built against the snapshot would be
a fake. hpcworker is an outside lane, so the list below goes to the coordinator as a handover note.

Measure first, inside a Slurm job, before anyone builds: `sbatch --test-only -p reqp,secp -q requeue` and the same
with `-q secondary`, `scontrol show partition reqp secp`, `sacctmgr show assoc user=$USER`. If one QoS is accepted on
both partitions, the race collapses to one job over `-p reqp,secp` and every client gets the first free queue with no
extension change at all. Only if each partition insists on its own QoS is the two-job race needed.

The sign-in sitting is single-queue too (`srun -p secp -q secondary -I600`), and that is where hy9698 timed out; the
snapshot does not touch it. The race (or the collapsed partition list) should reach the sitting first.

hpcworker framework 19, what it must add (from the snapshot, ported to main 3b22e70): `worker_queues` in
`FIELD_LAYERS` as a lab field; the module schema regenerated (`profile.py schema`) and beethoven-sites' `oschome.json`
given `"worker_queues": ["reqp/requeue", "secp/secondary"]`, then `compose-all`; `cli.json` `connect [--race]` and the
gate's seventh word `race`; `lines.json` `{"id":"candidates","pattern":"^HPCW-STEP candidates ([0-9]+(?:,[0-9]+)+)$",
"groups":["jobs"]}`; `candidates` in `status.schema.json` and `worker-status.schema.json`; the testbed's fake `sbatch`
and `scancel`; vectors rewritten with `python3 framework/tests/vectors.py --write`; `V11_CONTRACT.md` R1' and
`V12_CONTRACT.md`'s gate word; the `contract` export's version raised. Then the extension pins it and adds the
`candidates` reader, `facts.ts` R1', the "in line on two queues" wording, the mock's second job and the tests.

The grid-etiquette sentence changes with it: one `sbatch` per queue group (at most four) instead of one, still one
`squeue` and one `scancel` per action. That sentence is in the agreement, so it rides the same text bump.

## 5. Profile loader, Wayne State the default

Wayne State is already the default: `DEFAULT_SITE = 'wayne'` (`background.ts:135`, used at 582, 664, 722, 751, 1414,
2936, 3023) and `siteFromHostname` guesses a site from a DNS label (`keys.ts:336`). The real work is removing those
guesses and reading the deployment from data:
- take beethoven-base's `browser` export (`src/profile.ts` v1: `readProfile`, `deploymentFor` → one | none | several,
  `expandPath` with a word boundary, `portalOriginOf`, `restricts`) as a pinned copy at `extension/src/base/` through
  `interface/pull.sh`, and replace `contract.ts`'s unchecked reader (198-206, 685-687) and its `expandPath` (190-196,
  which turns `$USERNAME` into `ab1234NAME`);
- `scripts/sync-profiles.mjs` writes a deployment list beside the profiles; a `core/deployments.ts` loader; a
  deployment record that survives Disconnect (the 2026-10-03 failure that keeps `DEFAULT_SITE` alive, 579-581);
- welcome and Settings get a picker by `display_name`, Wayne State preselected by one build constant and confirmed by
  the portal the student grants; `vpn_required` read from the profile (typed at `contract.ts:661`, never read).
- Linear: BEE-210 (site chosen by its match list, "never a default") conflicts with greg's instruction; I am
  recording his newer word as the decision on that issue. BEE-211 (literals and the site-literal lint), BEE-213
  (portal, second factor and VPN kinds), BEE-215 (tests) stay needed for a second university, which also needs a
  shared copy, an image and the ACL at that site before any client can reach it.

## 6. Order of work (one pull request each, on `claude/extension-vpn-first-xjhm0g`)

1. VPN-only: the removal, the manifest, CI, the pins, the update-time key cleanup, the behaviour fixes of §2, the
   simplified pages of §3 (16.0.0).
2. The texts: LICENSE 11, PRIVACY 12, notices, TERMS_VERSION 11, store texts (could ride 1, but reviewed apart).
3. The base `browser` pin, the deployment list, the picker, `vpn_required`.
4. The race client, only after hpcworker publishes framework 19 and the measurement says the race is needed.

The repository has `ci.yml` only (no `automerge.yml`, no `rulesets.yml`), so each pull request needs greg's hand merge;
the coordinator gets each link.

## 7. Housekeeping found on the way

Stale "Versions in this tree" in `README.md` (says 10.0.0); pointers to the VS Code edition's `tools/intake` (now
`beethoven-access`); `docs/guides/LAB_LEAD.md` §9 and `CLAUDE.md:148-150` behind hpcworker's; pins at framework 17
while hpcworker main is 18 (seven vectors differ by the version string; `conformance.test.ts:566` expects '17'); no
repository kit; `test/bridge.test.ts:131-133` asserts the wrong `ssh_relay` shape (moot once removed); the Pilot App
paragraph in the store text to retire.

## 8. Not yet measured

The one-time terminal step for a keyless student; the tab-free Basic-auth channel on the real portal; the signed
installers on any real machine (moot under remove); `--begin`/singleton chains and compute-node `setfacl` on Wayne
State's Slurm (hpcworker's, listed in its `docs/OPEN_QUESTIONS.md`); whether `-p reqp,secp` with one QoS is accepted.

# CLAUDE STATE SERIALIZATION

**Timestamp:** 2026-10-22T10:20Z **Phase:** Implementation (23.0.0 released through CI)

Repository hand-off: `OpenSpineConsortium/beethoven-extension` (private), the client half of the Beethoven launcher. Project-wide state, rules and greg's open steps: `/mnt/project-files/state/HANDOVERS.md` (section "Since 2026-10-09") and `DECISIONS.md` (list "Waiting on greg, 2026-10-22"); how to use this file: `HYDRATE.md`. Checked against `origin/main` e6ee0f6 with git and `gh api` at 09:17-10:05Z; whatever says "not yet measured" or "not established" was not checked. This file replaces the one of 2026-10-05, which described 15.0.0.

**Read first, in the repository itself, on `origin/main`:** `CLAUDE.md` (every rule, including those 20.0.0 to 23.0.0 added); `docs/V19_STATUS.md` (the home project's extension thread's hand-off of 2026-10-09: where 19.0.0 stood, what to do when the store's or C&IT's answer comes, the race handover, the open items; its sections 2.1 to 2.6 and 3 are what this file's section 5 updates); `docs/OPEN_QUESTIONS.md`; `release/20.0.0/README.md`; `docs/store/SUBMISSION.md`. A local checkout may be old: fetch first (this session's checkout was at a7db369, 79 commits behind).

## 1. Primary Objective

Keep the Beethoven Chrome extension (`extension/`, WXT and TypeScript), the student's thin client: it starts, watches and stops the worker hpcworker runs, reaching the grid only through the university's VPN and its Open OnDemand portal (16.0.0 removed the direct ssh way and its native bridge; no `helper/` on main), and opens the student's Claude project, or else the worker's link. 23.0.0 is on main, built and released from main by `release.yml`. Since 2026-10-11 every change (PRs #10 to #23) has come from sessions outside the home project; the home project's extension thread finished with PR #9 and holds nothing in flight.

## 2. Architectural Decisions & Constraints

- **Manifest** (`extension/wxt.config.ts:71-80`, unchanged since 4ba8931 of 2026-10-09): `storage`, `alarms`, `scripting`, and on Chromium `sidePanel`, `webRequest`, `webRequestAuthProvider` (one `onAuthRequired` listener, for Beethoven's own background dashboard request on the granted portal origin only, 19.0.0); `optional_host_permissions` `https://*/*`; no `host_permissions`; minimum Chrome 148. `nativeMessaging`, `cookies`, `tabs`, `webRequestBlocking`, `declarativeNetRequest`, `debugger`, `identity` and every claude.ai, anthropic.com or claude.com origin stay absent (`:26-30`).
- **Grid sign-in** (19.0.0): the sheet takes the AccessID and password; with Remember ticked the password is sealed with AES-GCM under a key from a passkey's PRF (Windows Hello, Touch ID) in IndexedDB; one wrong try, then stop; Chrome's own box is the fallback.
- **Approval** (20.0.0, `CLAUDE.md:101-118`): one person's approval works from every installation of their own; the access service keeps the ten most recent and e-mails the maintainer about a new one, with a Withdraw link. `other_installation` is no longer sent but still read.
- **The store** (`CLAUDE.md:160-177`): one public listing since 20.0.0 (`https://chromewebstore.google.com/detail/beethoven/heoopgbkbkfckhhpbkkcgigohfekjicn`). `.github/workflows/release.yml` calls OpenSpineConsortium/chrome-store-release-kit on every push to main: the tests, `npm run zip`, the build number `<manifest>.<commit count>`, a GitHub release `extension-v<version>.<n>`, and the store upload once the five `CWS_` secrets and the variable `CWS_ON_PUSH` are set. This replaced the rule that no store sign-in goes into CI.
- **21.0.0 to 23.0.0**: Settings takes the address of the student's Claude project, opened before a plain session (`CLAUDE.md:119-133`); a lab lead's "Connect GitHub Actions" and "Remove" type hpcworker's published lines `grid-gate-setup` and `grid-gate-off` through the portal's shell (`:134-150`); Beethoven restarts into a downloaded version only while nothing would be lost (`:151-159`).
- **Texts**: `LICENSE.txt` version 15 (2026-10-16), `PRIVACY.md` version 17 (2026-10-18; greg's "Statement only" kept the agreement at 15), `TERMS_VERSION` 15 and `TERMS_DATE` 2026-10-16 (`extension/src/core/terms.ts:28-29`); the `extension/public/` copies are byte-identical.
- **Pins**: hpcworker's contract at a0ac0ed (`framework/contract/ORIGIN`, framework 18's vectors); contract text and profiles at hpcworker e77863c; beethoven-base's `browser` export at c7682f6 (`extension/src/base/`). Change a pin only with `interface/pull.sh`, never by hand.
- **Merging**: no `automerge.yml`, `rulesets.yml` or `.github/rulesets/` here; since 2026-10-22 02:02Z the organization's rule "Require owner approval to merge" needs one approving review on main, and a session's pull request (opened as greg) merges only through his bypass. Every pull request so far was his merge.

## 3. Files Modified & State

| File Path | Status | Key Modifications / Purpose |
| --- | --- | --- |
| extension/package.json | Complete | 23.0.0. PRs #19 to #23 all ship as 23.0.0, told apart only by the build numbers .116 to .121 in the tags |
| extension/src/core/terms.ts | Complete | `TERMS_VERSION` 15, `TERMS_DATE` 2026-10-16 |
| LICENSE.txt, PRIVACY.md | Complete | 15 and 17; counsel notes exist up to `docs/TEXTS_V14_V15.md`, none for agreement 15 or privacy 16 and 17 |
| .github/workflows/release.yml | Complete | PR #13, fixed in PR #15; runs #1 and #2 failed (no zip found), #3 onward succeeded; the store job has run on every push since run #8 (e48c345, 2026-10-18) |
| docs/V19_STATUS.md | Stale | The newest status document; there is none for 20.0.0 to 23.0.0, which only `CLAUDE.md` and `PRIVACY.md:537-543` describe |
| release/20.0.0/ | Complete | The last release record; none for 21.0.0 to 23.0.0. Its `store-kit/05-promo-video-1280x720.mp4` is still 9.0.0's (PR #16 changed only `extension/store-assets/promo/`) |
| framework/profiles/ORIGIN | Stale | hpcworker e77863c; hpcworker's `wayne.json` changed in 8563065 (framework 26: `galhp`, `qos_gpu`, `node_domain`) |
| README.md | Stale | Line 254 says "the extension is 21.0.0" |
| extension/src/ui/panel.ts | Pending | `NEEDS_GRID` (line 80) holds `connect`, `retry` and `sign-in-claude`; the test (`extension/test/ui-fixtures.test.ts:503-512`) covers `connect` only (review finding R2-22) |

## 4. Completed Milestones

1. 16.0.0 to 19.0.0 (PRs #5 to #8, 2026-10-08 and 09), by the home project's extension thread: the direct way removed, base's profile reader pinned, the grid sign-in in front, "Beethoven signs in". PR #9 (`docs/V19_STATUS.md`, `docs/V19_DESIGN.md`) merged by greg on 2026-10-13.
2. The store accepted 19.0.0 (greg, 2026-10-13; `docs/V19_STATUS.md:43`).
3. 20.0.0 (PRs #10 to #12, 2026-10-11 to 13): every installation of one person; the public listing; the release record.
4. Releases from CI (PRs #13 and #15); first tag `extension-v20.0.0.102` (e900bae). Store screenshots and the submission kit (PR #14); the promo video at 1440p with sound (PR #16).
5. 21.0.0 (PR #17, 2026-10-16), 22.0.0 (PR #18, 2026-10-18), 23.0.0 (PR #19, 2026-10-18).
6. 2026-10-21, PRs #20 to #23: Stop and Cancel on the first run's waiting screens (after go2432's panel showed "Still connecting" through thirteen 8 h jobs; hpcworker frameworks 19 and 20 are the server side of that failure); the Claude account's e-mail on the Claude row; the shell's reason when a lab lead's gate press is cut off; the 15 s timer no longer cuts off a long gate setup, and the Repository field defaults to OpenSpineConsortium/symphony-template.

## 5. Active Blockers & Errors

- **The race client** (`V19_STATUS.md` 2.3): a `candidates` reader in `contract.ts`, rule R1' in `facts.ts`, the mock's second job and conformance tests wait on hpcworker publishing the race, which is not built (`HANDOVERS.md`). Measured on 19.0.0 and still true: a worker that wins on a second queue leaves the panel waiting with no link (`V19_STATUS.md:114-123`).
- **The word "AccessID"** (2.4) waits on a site-module text key in hpcworker's module schema (`extension/src/core/model.ts:48-49`).
- **hpcworker's CLAUDE.md lines 67-76** (2.5) are still stale; it is hpcworker's lane's pull request (`HANDOVERS.md`).
- **C&IT's answer** on the Remember tick (2.2) is not on record anywhere read; open question 4 stands.
- **Not yet measured:** all eleven questions of `docs/OPEN_QUESTIONS.md:3` (the listener on the live portal, Windows Hello or Touch ID from the side panel, the PRF result, whether failed Basic sign-ins count toward the five, the order race, a right saved password held); `docs/guides/LAB_LEAD.md` section 10; a finished gate press on the grid (the press of 2026-10-21 failed; the fix in e6ee0f6 is tested only in `shell-evidence.test.ts`); 23.0.0's restart in a real Chrome (`update.test.ts` runs on a fake browser); whether `release.yml`'s store step ever uploaded (its log and the repository's variables are refused through the proxy); the Wayne State quotes in `docs/research/v19/policy-wayne.md:42-44` on the live pages.
- **Waiting on greg:** whether the `CWS_` secrets and `CWS_ON_PUSH` are set; the site's `privacy.html` at 17 and `terms.html` at 15 before 22.0.0 and 23.0.0 reach students (`docs/store/SUBMISSION.md:31-33` still gates only 21.0.0's 16 and 15); the order race (a terms change, `V19_STATUS.md:154-157`); the 20.0.0 grid test and the access check from two installations (`release/20.0.0/README.md:75-79`); the merge of every pull request.

## 6. Immediate Next Actions (Hydration Directives)

1. `git -C <checkout> fetch origin --prune --tags`, then read `CLAUDE.md` and `docs/V19_STATUS.md` on `origin/main` and `gh api "repos/OpenSpineConsortium/beethoven-extension/pulls?state=open"`; the lane outside the home project may have moved on since this file.
2. Before any change to `extension/src/core/contract.ts`: hpcworker's contract export changes first; then `interface/pull.sh` re-pins it.
3. Re-pull the profiles (`bash framework/profiles/pull.sh`) once `extension/src/base/profile.ts` is shown to accept `qos_gpu` and `node_domain` (both optional in module-schema 1, so expected to, not yet run).
4. Candidates for the lane, none asked for by greg: a status document for 20.0.0 to 23.0.0; release records 21.0.0 to 23.0.0; `README.md:254`; the store kit's promo video; the R2-22 test.
5. Open each pull request ready for review; it waits on greg's merge under the organization rule.

# CLAUDE STATE SERIALIZATION

**Timestamp:** 2026-10-04T21:25Z **Phase:** Implementation

Repository hand-off: `OpenSpineConsortium/beethoven-extension` (private), the client half of the Beethoven launcher. Project-wide state, rules and greg's open steps: `/mnt/project-files/state/claude_context.md`; how to use this file: `/mnt/project-files/state/HYDRATE.md`. Checked against GitHub at 20:32Z (main a7db369 and the pushed branch `claude/project-thread-fx3wkp` at d6db850), against the desktop thread's staging folder at 20:33Z, and earlier by an independent checker; whatever says "not yet measured" or "unverified" was not checked.

## 1. Primary Objective

Keep the Beethoven Chrome extension (`extension/`, WXT and TypeScript), its native-messaging bridge (`helper/`, which only carries bytes to the grid's ssh port) and the store packages (`release/`). It is the student's thin client: it starts, watches and stops the worker that hpcworker runs and opens claude.ai at the worker's link. The work in flight is 15.0.0: the bridge as a signed, notarized Mac package and a signed Windows installer, so a student installs from the Chrome Web Store and never opens a terminal (greg 15:26Z and 15:41Z), and an automatic store upload at the end of greg's release command (19:26Z to 19:36Z). It is pushed as branch `claude/project-thread-fx3wkp` (d6db850) with no PR yet; the release command on greg's Mac is saved outside GitHub (section 5).

## 2. Architectural Decisions & Constraints

- **Never in this repository:** an API key or a Console sign-in (the Console link `platform.claude.com` is refused by host in `isClaudeAuthUrl`, `extension/src/core/contract.ts`); a Claude credential; signing out anyone. On main the panel's "no Pro or Max plan" problem still offers "Use another account", which types `connect --login fresh` (framework 17 refuses it); branch d6db850 replaces that with a panel that says how to use another account without a sign-out and never asks the grid for one. Signing identities (Apple Developer ID, Azure Artifact Signing) never enter the repository or CI. Signing runs only on greg's machines.
- No code on claude.ai, no host permission at install, and never `cookies`, `tabs`, `webRequest`, `declarativeNetRequest`, `debugger`, `identity` or any claude.ai, anthropic.com or claude.com origin; `nativeMessaging` only for the one bridge host `com.openspineconsortium.beethoven.bridge`. No remote code; the withdrawn-versions list is JSON checked with WebCrypto.
- One channel: a private Chrome Web Store listing whose testers are greg's Google Group (CLAUDE.md, decided 2026-09-30). The listing stays private: the owner thread answered greg's 19:26:52Z question at 19:31Z (no Google Workspace and no public listing needed; only publishing to a whole domain needs Workspace; Google reviews every version). The upload is automatic through the store's upload API v2, one zip carrying both signed installers, run at the end of greg's one release command on his Mac and never in GitHub or CI; the Google sign-in for his store account stays saved in his vendor folder on the Mac (his card choice "Save on Mac", 19:36Z). That Google sign-in is not a Claude key and never enters the repository. Whether it lasts beyond seven days for a personal, unverified Google app is not yet measured.
- `LICENSE.txt` and `PRIVACY.md` at the root are canonical; the copies in `extension/public/` stay byte-identical; a text and `TERMS_VERSION` change together; never pre-tick a box.
- **beethoven-base (greg, 20:04Z; design 20:58Z):** the code shared with the desktop and VS Code editions moves to a new repository, and this edition carries it as a pinned copy in `extension/src/base`, checked against an ORIGIN record with no secret (no fetch, no read token); it takes base v1.0.0 at its 16.0.0, after 15.0.0. greg created the repository at 20:25Z; nothing has moved yet (`repos/beethoven-base.md`).
- Contract seam: `extension/src/core/contract.ts` mirrors hpcworker's `docs/V11_CONTRACT.md` and `V12_CONTRACT.md`; profiles under `framework/profiles/` are hpcworker's, refreshed with `bash framework/profiles/pull.sh`.
- Merging: no ruleset, no auto-merge workflow, so every PR is greg's hand merge; sessions may not write `.github/workflows/` files here. CI (`.github/workflows/ci.yml`) runs on a push to main and on a pull request, so a pushed branch has no run until its PR opens. PRs open ready with greg assigned.
- Owner thread: "Build the Claude Desktop ssh plugin" (`cmsg_01JbwQwHoYeBWptjPB5c6u8m3KSccv8f9KZdoYiLkxZons`, branch `claude/project-thread-fx3wkp`).

## 3. Files Modified & State

| File Path | Status | Key Modifications / Purpose |
| --- | --- | --- |
| extension/package.json | Complete | Version 14.0.0 on main; 15.0.0 on branch d6db850 |
| extension/src/core/terms.ts | Complete | Main: `TERMS_VERSION` 9, `TERMS_DATE` 2026-10-02 (LICENSE.txt 9, PRIVACY.md 10). Branch d6db850: 10 and 2026-10-04, LICENSE.txt version 10 and PRIVACY.md version 11 ("Texts for 15.0.0"), the `extension/public/` copies changed with them |
| extension/src/core/contract.ts | Complete | Console link refused; codes `signin-billed`, `signin-method` (PR #1) |
| extension/wxt.config.ts | Complete | The manifest as code; minimum Chrome 148 |
| helper/src/rust/src/main.rs | Complete | The bridge's binary edition, built and suite-tested in CI on three systems, unsigned |
| release/14.0.0/README.md | Complete | Newest package record; zip sha256 f0abebd8...df38 matches; whether 14.0.0 was ever uploaded is unverified |
| docs/V11_CONTRACT.md | Pending | On branch d6db850 byte-identical with hpcworker main's (blob e6f8907); main's copy still differs until 15.0.0 merges |
| docs/V12_CONTRACT.md | Pending | Branch d6db850 adds the section "Signed installers (15.0.0)", the binary helper (kind `binary`, runtime `rust`, beside the script kind) and a line naming hpcworker's copy canonical, "this copy and that one change together, in the same words"; hpcworker's copy (main and its branch b35952a) has none of it |
| helper/release/ (mac/build-pkg.sh, windows/build-msi.ps1 with Package.wxs, publish-store.mjs, README.md) | Pending | On branch d6db850; the signing and upload scripts, never run with a real certificate or store account |
| wip/mac-W, wip/mac-R | Pending | Not on GitHub: the Windows installer built and signed on the Mac, and the one release command with its setup script; in `/mnt/project-files/staging/desktop-thread/beethoven-extension-mac-release.bundle` |
| CLAUDE.md | Pending | Line 55 still "One person, one account." on main and on the branch; the branch rewrites the terms paragraph for 15.0.0 (from line 165) where main's lines 141-151 state texts versions 8 and 9 and `TERMS_VERSION` 8 |

## 4. Completed Milestones

1. PR #1, "No API key anywhere" (head 1bfb739), merged by greg 2026-10-04T16:35:58Z as a7db369; main CI run 37217361131 green on all four check runs. Ledger 16:01Z: `tsc` and vitest 41 files, 521 tests; 8 review findings fixed.
2. Commit 7ecea53 (2026-10-03T23:44Z): three fixes from a student's sitting, Start over, and the bridge's rust binary edition built and suite-tested in CI.
3. Split from the monorepo at ef58694 (2026-10-03T18:48Z) with its own CI and no secrets; every main CI run since has succeeded.
4. 15.0.0 pushed by 20:31Z as `claude/project-thread-fx3wkp` d6db850: 15 commits on main a7db369, 67 files, +5987/-694; the five installer streams A to E merged (build script and CI, Mac package, Windows installer, panel and picker, texts and version), the store upload step, "use another account without a sign-out", and V11 made identical to hpcworker's. In the owner thread's checkout: "625 tests, Chrome build and mock selftest pass" (20:12Z), the upload step's 28 tests (nothing sent to Google).

## 5. Active Blockers & Errors

- 15.0.0 has no PR and so no CI run on d6db850 (0 check runs at 20:32Z); the 625 tests were the owner thread's own run.
- Not on GitHub: branches `wip/mac-W` (ab1f44f; Windows MSI built and signed on the Mac with msitools wixl, Rust `x86_64-pc-windows-gnu` with mingw-w64, and jsign against Azure Artifact Signing) and `wip/mac-R` (63fa934; the one release command on greg's Mac and its setup script), under review when saved at 20:27Z. The bundle verifies ("is okay") in a clone holding d6db850; its one prerequisite, 45a89db, is an ancestor of d6db850. On a real Mac none of it is measured.
- `docs/V12_CONTRACT.md` on the branch and in hpcworker differ on GitHub; the desktop thread's patch for hpcworker (commit ed94b6b, in the staging folder) gives hpcworker's copy this branch's exact blob (75f86cb, checked 21:15Z) and rides hpcworker PR #3, which must land before or with 15.0.0.
- The signed installers cannot be produced until greg has an Apple Developer ID (Application and Installer certificates, a notarytool keychain profile), an Azure Artifact Signing account with a certificate profile, and gives the Chrome Web Store item id for `--store-id`.
- Remote branch `claude/project-thread-2udoqz` (fbf3c09, the replan thread's D4 sentence) is unmerged with no PR; it predates PR #1. Merging it as it stands conflicts in CLAUDE.md at line 55, and the "No API key anywhere" bullet is inside the conflict hunk; resolving by taking the branch's side would drop it, so the D4 sentence has to be re-applied on top of main.
- Not yet measured: Gatekeeper, SmartScreen, Installer.app and Chrome starting the signed binary; the first live sitting end to end; OPEN_QUESTIONS #8, #11, #12. CI test counts cannot be read from a cloud session (job-log download refused by the proxy).
- Waiting on greg: the signing accounts above; copy `automerge.yml`, `rulesets.yml` and `rulesets/main.json` from beethoven-desktop with the required check renamed to `typecheck, vitest, mock selftest, build` (and `bridge (rust, <os>)` if wanted); hand-merge the 15.0.0 PR; decide how PRIVACY.md describes the in-memory debug log before any upload; decide branch 2udoqz; one Google sign-in on his Mac when the upload step first runs.

## 6. Immediate Next Actions (Hydration Directives)

1. Run `git -C <checkout> fetch origin --prune --tags` and `gh api "repos/OpenSpineConsortium/beethoven-extension/pulls?state=all"`; the owner thread owns the signed install here, so check whether it has merged the Mac branches into d6db850 or opened the 15.0.0 PR before touching anything.
2. If its work is lost: in a clone at d6db850, `git fetch /mnt/project-files/staging/desktop-thread/beethoven-extension-mac-release.bundle 'refs/heads/*:refs/remotes/bundle/*'`, finish their review, merge `bundle/wip/mac-W` and `bundle/wip/mac-R` into `claude/project-thread-fx3wkp`, and open the 15.0.0 PR ready with greg assigned.
3. Run the suite as CI does: `cd extension && npm ci && pip install asyncssh && npm run sync-profiles && npm run typecheck && npx vitest run`, then `node helper/build.mjs --check` from the repository root.
4. Put the branch's `docs/V12_CONTRACT.md` into hpcworker in the same words so both land together, then append a row to `/mnt/project-files/ledger/LEDGER.md`.

# CLAUDE STATE SERIALIZATION

**Timestamp:** 2026-10-05T00:15Z **Phase:** Implementation

Repository hand-off: `OpenSpineConsortium/beethoven-vscode` (private), Beethoven for VS Code (Ashley for VS Code up to 3.0.0; Marketplace item `openspineconsortium.beethoven`). Project-wide state, rules and greg's open steps: `/mnt/project-files/state/claude_context.md`; how to use this file: `/mnt/project-files/state/HYDRATE.md`. Checked against GitHub at 21:17Z (main cc76efd, PR #2 open, the pushed branch `claude/project-thread-fx3wkp` still aa44696), by building main in a clean copy at 21:00-21:13Z, and by an independent checker of the grid scripts at 21:18Z; whatever says "not yet measured" or "unverified" was not checked.

**Update 2026-10-05T00:15Z** (read before the sections below, which describe 21:25Z; checked with `gh api` at 00:08Z): Dependabot #8 (mocha 12.0.3) and #9 (MCP SDK 1.31.0) merged at 21:48Z; #2 is closed; `main` is fa93c84. The branch `claude/project-thread-fx3wkp` is c065f25 (21:33Z, the account setting's second review), three ahead of `main` and four behind; its pull request is not opened yet. 5.0.0 stays on hold, and the five grid commands stay unrun, until grid scripts 9 merges with it.

## 1. Primary Objective

Keep the licensed VS Code extension (with its CLI and MCP server) that sets up a student's laptop for the Wayne State grid and keeps a Claude Code worker running there over ssh, with grid scripts installed in `~/.beethoven/bin`, plus the maintainer's licence, release and access-service tools. 5.0.0 (no API key, no paid usage) is merged but on hold: its grid scripts 8 break the project's deletion and access rules, and a grid scripts 9 fix rides the account-setting PR (desktop thread, 21:00Z). The next feature is the `beethoven.account` setting (one of greg's own accounts per terminal), on a branch with no PR yet. Later the edition takes its shared code from beethoven-base and, at its 7.0.0, moves onto hpcworker (`repos/beethoven-base.md`).

## 2. Architectural Decisions & Constraints

- **Read-only neighbour:** edited only on greg's explicit order. He ordered the key removal (BEE-191, 03:15Z) and the no-key sweep (13:27Z); the account setting follows `plan/ACCOUNT_SWITCH_CLIENTS.md` item 2.
- **Never:** an API key or paid usage (the 4.0.0 overflow is gone since 5.0.0; the 2.0.0 to 4.0.0 packages are withdrawn and removed from `dist/`); a Claude credential (only `claude auth status` is read); `ANTHROPIC_API_KEY` injected into a laptop terminal; a token in argv, logs, job files or `sbatch --export`.
- Every feature ships with diagnostic nodes (`extension/src/vscode/diagNodes.ts`, the grid's `cmd_diag`), enforced by `REQUIRED_BY_FEATURE`.
- Terms texts and `TERMS_VERSION` change together (6 since 5.0.0); never pre-tick; old names stay as aliases (`ashley.*` settings read, `~/.ashley` a link, `ASHLEY-RELEASE1` never changes).
- Signing keys live in greg's vendor folder and never enter the repository; release and publish run only on his machine.
- Merging: no CI workflow, no ruleset, `allow_auto_merge` false; every PR is greg's hand merge. CLAUDE.md still says to commit directly to main; practice since 2026-10-04 is PRs from `claude/project-thread-fx3wkp`.
- **beethoven-base (greg, 20:04Z; design 20:58Z):** the edition keeps only its own code and takes the shared code as a pinned copy in `extension/src/base`, checked against an ORIGIN record with no secret: first the laptop side at 6.0.0, then at 7.0.0 it drops its own grid scripts (`grid/`, kept since it came first as Ashley for VS Code) for hpcworker's commands, never deleting `~/.beethoven` (`repos/beethoven-base.md`). Nothing has moved yet.
- Owner thread: "Build the Claude Desktop ssh plugin" (`cmsg_01JbwQwHoYeBWptjPB5c6u8m3KSccv8f9KZdoYiLkxZons`).

## 3. Files Modified & State

| File Path | Status | Key Modifications / Purpose |
| --- | --- | --- |
| extension/package.json | Complete | Version 5.0.0, id `openspineconsortium.beethoven`, engines `^1.100.0`; since 21:16Z TypeScript 7.0.2, @types/node 26.6.3, @types/vscode 1.100.0 (pinned to the engine), mocha 11.7.1 |
| .github/dependabot.yml | Complete | Ignores `@types/vscode`, which is raised with `engines.vscode` by hand (PR #7) |
| extension/src/core/terms.ts | Complete | `TERMS_VERSION` 6, `TERMS_DATE` 2026-10-04; LICENSE.txt, LICENSE-FULL.txt and PRIVACY.md version 6 |
| grid/VERSION, grid/beethoven, grid/beethovend.js, grid/phone.js | Broken | Grid scripts 8. Checked at 21:18Z on main: `uninstall` runs `rm -rf` on the real `~/.beethoven` (grid/beethoven:1104), which holds hpcworker's sign-in and the engine's accounts, with no prompt (it never checks the `--yes` its guard message suggests); `claude forget --yes` removes the whole sign-in directory (:602); beethovend.js:176 and phone.js:40 accept a sign-in with an apiKeySource, which hpcworker refuses (common.sh:238); `access init` (:775-778) and `library publish` (:105, bootstrap.sbatch:127) close shared/ and shared/beethoven to other, hpcworker's shared copy included; `access admin approve` (:706-713) turns a student's `rwx` entry on the volume root into traverse only. The agent-marker and terminal guards are there (:48-51). Fix: grid scripts 9 with the account-setting PR |
| tools/release.mjs, tools/publish_marketplace.sh | Complete | Build, check and sign into `dist/release/<v>/`; publish from WSL. Not yet run for 5.0.0 |
| dist/release/README.md | Complete | 2.0.0 to 4.0.0 withdrawn; 5.0.0 not built |
| docs/CHECKPOINT_2026-09-28.md | Pending | Lines 11-12 still say the withdrawal and key sweep are not committed; they are, through PR #6 |
| .github/CODEOWNERS | Broken | Names `@GregorySchwing`; GitHub reports "Unknown owner on line 2" (greg's login is Gregory-Schwing-MD-PhD) |
| `beethoven.account` setting | Pending | Pushed as `claude/project-thread-fx3wkp` aa44696: one commit on main 24a9896 (now behind main by the Dependabot merges and #7; its package.json hunk does not touch the devDependencies), 25 files +538/-57, `TERMS_VERSION` 7 (76 unit tests in the owner thread's run); no PR yet, and it will not be #7. Its review's 22 findings (default sign-in place, list changes, remote windows, texts) are not fixed there; half-done fixes in `/mnt/project-files/staging/desktop-thread/beethoven-vscode-account-fix.wip.patch` |

## 4. Completed Milestones

1. PR #5, 5.0.0 (no API key and no paid usage, grid scripts 8, terms 6, BEE-191), merged by greg 2026-10-04T13:27:19Z as a8e5490.
2. PR #6, the no-key sweep (triage text rewritten, key-asking packages withdrawn from `dist/`, grid accepts only authMethod `claude.ai` with apiProvider `firstParty`), merged by greg 17:05:26Z as 24a9896.
3. Re-run on main 24a9896 at about 19:00Z from a scratch export: `npm ci`, `npm run typecheck` exit 0, `npm run test:unit` 68 of 68 (keep `grid/` beside `extension/`, or typecheck fails with TS2307).
4. 4.0.0 released and signed 2026-09-30 (lightweight tag v4.0.0 on 3ca3b4e), since withdrawn because it asks for a key.
5. greg merged Dependabot #4 (TypeScript 7.0.2), #3 (@types/vscode 1.138.0) and #1 (@types/node 26.6.3) at 20:58-20:59Z (main 80f79db): `npm ci`, typecheck and 68 of 68 unit tests passed, but `npm run package` stopped at vsce ("@types/vscode 1.138.0 greater than engines.vscode ^1.100.0"). On his card (21:10Z, keep the minimum at 1.100) the hand-off thread opened PR #7 (a199f19: the types back to 1.100.0, Dependabot told to ignore them); typecheck, 68 of 68 and "release checks passed"; greg merged it at 21:16Z as cc76efd.

## 5. Active Blockers & Errors

- 5.0.0 has no package: `dist/release/` holds only 2.0.0 to 4.0.0 records ("Until it is here there is no package to install from this repository"). Building and signing need greg's machine and key.
- The account setting's staging patch (6 files, +193/-84) applies cleanly to aa44696 (`git apply --check`, 20:33Z); it was taken mid-edit and has not been typechecked or tested; the 22 findings are in `beethoven-vscode-account-review-findings.txt` beside it.
- `beethoven.account` must not ship before a real-machine check that the Claude Code VS Code extension honours `CLAUDE_CONFIG_DIR` (`plan/ACCOUNT_SWITCH_CLIENTS.md:38-39`).
- Dependabot #2 (mocha 12.0.3, rebased by Dependabot at 21:01Z onto 80f79db, head 7f99124) is open and mergeable on cc76efd; on its head `npm ci`, typecheck and 68 of 68 unit tests pass. The VS Code test runner uses `@vscode/test-cli`'s own nested mocha 11.8.0, so the bump changes nothing at run time. The repository has no CI, so nothing checks a merge here but a person or a session.
- Not yet measured: the Marketplace listing (memory says Ashley 3.0.0 is listed and Beethoven is not; the proxy answers "CONNECT tunnel failed, response 403"); `npm run test:vscode` on 5.0.0 (download blocked in the cloud); `tools/grid_tests.sh` for grid scripts 8; whether grid scripts 8 are deployed to greg's account (last record: scripts 7).
- Waiting on greg: do not run `uninstall`, `claude forget`, `access init`, `access admin approve` or `library publish` on the grid; merge Dependabot #2 when convenient; after grid scripts 9 land: build and sign 5.0.0 (or its successor) with `tools/release.mjs`, check the site's pages, publish, then unpublish (not remove) `openspineconsortium.ashley` 3.0.0; the `CLAUDE_CONFIG_DIR` check.

## 6. Immediate Next Actions (Hydration Directives)

1. Run `git -C <checkout> fetch origin --prune --tags` and `gh api "repos/OpenSpineConsortium/beethoven-vscode/pulls?state=all&per_page=20"`; confirm main is cc76efd or later and whether the owner thread has moved the branch past aa44696 or opened the account-setting PR (with grid scripts 9).
2. Run the cloud check: `cd extension && npm ci && npm run typecheck && npm run test:unit`; expect 68 of 68 on main; add `npm run package` and expect "release checks passed".
3. Leave the `beethoven.account` work to the owner thread; if its work is lost, on aa44696 `git apply` the staging patch, finish the 22 findings, run typecheck and the unit tests, merge main in, open the PR ready with greg assigned, and ship only after the `CLAUDE_CONFIG_DIR` check and grid scripts 9.
4. With greg's order, fix `docs/CHECKPOINT_2026-09-28.md:11-12` and CODEOWNERS in one PR, and append a row to `/mnt/project-files/ledger/LEDGER.md`.

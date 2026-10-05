# CLAUDE STATE SERIALIZATION

**Timestamp:** 2026-10-05T00:15Z **Phase:** Implementation

Repository hand-off: `OpenSpineConsortium/beethoven` (private), the project hub. Project-wide state, rules and greg's open steps: `/mnt/project-files/state/claude_context.md` (in a clone of the hub, `state/claude_context.md`); how to use this file: `HYDRATE.md`. Checked against GitHub at 00:00-00:10Z; whatever says "not yet measured" was not checked.

## 1. Primary Objective

Be the one repository greg clones to continue the project from another Claude account or machine, kept current. His words (23:26:09Z): "seeing as the original just Beethoven repo I don't believe is being used anymore. You can wipe it and replace it with whatever you need to separate the existing repos. I'd like to be able to develop each one individually without needing to always be thinking about how it will affect the other reposts and then all the project files currently on the cloud I would like them to be pushed to get hub and it updated so that I can pick this up from another Claude account just by cloning one individual repo and maintain that tight integration with linear".

## 2. Architectural Decisions & Constraints

- It holds no product code. Product changes go to their repositories (`REPOS.md`); a change that crosses two follows `SEAMS.md`.
- The old monorepo tree was retired by an ordinary commit (cdaeaef); no force-push, no branch or tag deleted; the tags v4.0.0 to v12.0.0 and their eight releases stay. Before it went, all 580 paths of 386b958 were found on main of hpcworker or beethoven-extension, and 386b958 is hpcworker 0c51fb6 (`HISTORY.md`).
- Folders copied from the project under the same names: `state/`, `plan/`, `ledger/`, `base/`, `github/`, `promo/`, `staging/`; the project memory as `memory/`. `linear/` holds a snapshot of the team's issues and `linear/README.md`; `.mcp.json` names Linear's own server (OAuth in the browser; no token).
- `tools/sync.py` does the copy: never deletes, never overwrites a file whose last commit lacks the `Hub-Sync:` trailer (a hand edit, say from another account; reported as a conflict, exit 3), and copies nothing when `tools/scan.py` fails on any file it would copy. The scan refuses secret shapes, credential-named files, files over 5 MB and unexamined binaries, and opens git bundles (borrowing prerequisite objects from sibling checkouts, `HUB_BUNDLE_BASES`). Tested 2026-10-04 with a planted key in a file and in a bundle commit, a hand edit and a partial source.
- Never copied (`.hub-exclude`): `uploads/` (people's attachments; the one there on 2026-10-04 is a screenshot with greg's personal browser details) and the two superseded staging bundles of the three-repo thread.
- No CI and no auto-merge here. greg's card of 2026-10-05 00:13Z ("Push to main"): once PR #1 is merged, each sync is pushed straight to `main`, with no pull request; until then the hand-off thread pushes each sync to `claude/handoff-state-file-m0rg4r`, which updates PR #1. The card covered syncs only: a change to the hub's own files (`README.md`, `tools/`, `REPOS.md`, `SEAMS.md`) still goes through a pull request until he says otherwise.

## 3. Files Modified & State

| File Path | Status | Key Modifications / Purpose |
| --- | --- | --- |
| README.md, CLAUDE.md, REPOS.md, HISTORY.md | Complete | How to continue from another account; the rules; every repository and how a change lands; the old repository's record |
| SEAMS.md | Pending | Where repositories must change together, from three readers and two skeptics (workflow in this thread) |
| tools/sync.py, tools/scan.py, .hub-exclude | Complete | The copy and its checks |
| state/, plan/, ledger/, base/, github/, promo/, staging/, memory/ | Complete | 76 files copied at 2026-10-04T23:49Z (commit e48ce8f); five readers found nothing that must stay off GitHub (review items: greg's own usage and billing figures, claude.ai ids, an outside researcher's name and the spine study's commercial plans in `plan/`, the RULESETS_TOKEN weakness write-up in `base/DESIGN.md`) |
| linear/ISSUES.md, linear/issues.json | Complete | 103 issues that are not archived, at 2026-10-05T00:00Z; BEE-5 to BEE-97 archived 2026-10-03 22:33Z; BEE-175 not returned |

## 4. Completed Milestones

1. Attached with push access, inspected and checked against the split repositories (2026-10-04 23:35-23:40Z).
2. Retired the tree on greg's 23:26Z word (re-cited by the coordinator at 23:43Z after auto mode asked for it), wrote the hub, copied the project in, snapshotted Linear, pushed `claude/handoff-state-file-m0rg4r` and opened PR #1 ready (2026-10-05 00:00Z).

## 5. Active Blockers & Errors

- PR #1 waits on greg's merge; until it merges, a clone of `main` gives the old tree.
- The public site's `build_site.py` found the terms texts in a sibling checkout named `beethoven` (desktop thread's finding): set `BEETHOVEN_REPO` to a beethoven-extension checkout before the next site build. hpcworker's `tools/push_org.sh` pushes `main:main --tags` here; the desktop thread is retargeting it.
- The repository description on GitHub still describes the browser extension (not changed).
- Who besides greg can see the private repository through the organisation is not readable from a session (not yet measured).

## 6. Immediate Next Actions (Hydration Directives)

1. `gh api "repos/OpenSpineConsortium/beethoven/pulls?state=all"` and `git ls-remote https://github.com/OpenSpineConsortium/beethoven`: is PR #1 merged?
2. Inside the project, after every refresh of `state/`: from a clean checkout of the hub's branch, `python3 tools/sync.py --push --trailer '<the commit trailers>'`; refresh `linear/ISSUES.md` when Linear is reachable; settle any CONFLICT line by hand.
3. Outside the project: edit the files in the clone and commit; the project's next sync will report them as conflicts rather than overwrite them.

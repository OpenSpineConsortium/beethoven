# CLAUDE STATE SERIALIZATION

**Timestamp:** 2026-10-04T21:25Z **Phase:** Planning

Repository hand-off: `OpenSpineConsortium/beethoven-base` (private), the code the three client editions share. Created by greg at 20:25Z. This session cannot read the repository, so what is said about its contents comes from the desktop thread (coordinator relays 20:29Z and 20:59Z) and from `/mnt/project-files/staging/desktop-thread/beethoven-base-design-and-critiques.json`, read by an independent checker at 21:18Z. Project-wide state, rules and greg's open steps: `/mnt/project-files/state/claude_context.md`; how to use this file: `/mnt/project-files/state/HYDRATE.md`.

## 1. Primary Objective

Move the code that beethoven-vscode, beethoven-extension and beethoven-desktop share into this repository, so each edition keeps only its own code and a feature added here reaches all three. This is greg's 20:04:55Z ask, verbatim: "can you migrate the common codebases to a separate repo, beethoven-base, and just have the beethoven-vscode, beethoven-extension, and beethoven-desktop extensions contain their specific unique code? that way i can add features to all of them by updating the base repo?"

## 2. Architectural Decisions & Constraints

- **Owner:** the desktop thread, "Build the Claude Desktop ssh plugin" (`cmsg_01JbwQwHoYeBWptjPB5c6u8m3KSccv8f9KZdoYiLkxZons`). It finished the design at 20:58Z and said the written design, with greg's decisions, comes next in the project folder; `/mnt/project-files/base/` was still empty at 21:18Z.
- **What base is:** a TypeScript library holding the client half of hpcworker's contract (the STEP, LOGIN, GATE and KEY lines, `status.json`, `connection.json`), the shared rules (subscription-only sign-in including the apiKeySource check, the credential strip list, redaction, the etiquette floors, names, the link check), shared logic (profile reader with the profiles as data, diagnostics, the terms record, the signed-list verifier, the `accounts.json` parser, OpenSSH options) and two tools (`vendor.mjs`, `forbidden.mjs`). Data flows one way: hpcworker (the canonical writer, the contract texts, the profiles) to base to the editions.
- **How editions take it in (design of 20:58Z):** each edition carries a pinned copy inside its own source tree (`extension/src/base` in the browser and VS Code editions, `src/base` in desktop), checked against an ORIGIN record (repository, ref, commit, tree hash, files) by a vendor check that needs no secret, as beethoven-agents carries beethoven-qa. The design weighed and rejected fetching base in CI with a token, so no edition holds a read token. The check is a check, not a proof: an edit that also rewrites ORIGIN passes it, and `check --source` from base's own checkout closes that gap.
- **The one credential, optional:** `BASE_PROPAGATE_TOKEN`, a fine-grained token owned by OpenSpineConsortium, limited to the three edition repositories, Contents and Pull requests read and write, no Administration, Workflows or Actions, expiring within a year, kept only in beethoven-base. Its `propagate.yml` runs on a published base release and opens a "take the new base" PR in each edition; without it a session runs the same vendor command and opens the PRs itself. The design text stores it as a repository secret and triggers only on published releases; critique 1 and the desktop thread's 20:58Z message prefer an Environment secret deployable only from release tags. Not settled.
- **Secrets:** greg, 20:14:53Z: "also I set my RULESET token to all repos visibility, so i dont mind creating secrets". No Claude or Anthropic key anywhere and no workflow runs Claude Code. `RULESETS_TOKEN` stays for `rulesets.yml` only and is never used for code: its Administration write permission also adds deploy keys that read and write code, changes visibility and adds collaborators (GitHub's permissions table, checked 21:20Z).
- **Order (the design's migration list):** first the in-flight work (hpcworker queue report, extension 15.0.0, VS Code account setting with grid scripts 9); then base PR #1, the skeleton with its rules and kit, merged by greg's hand once; hpcworker test vectors; base modules and release v1.0.0; desktop 2.0.0; extension 16.0.0; VS Code 6.0.0 (laptop side only); `propagate.yml`; hpcworker framework 18; base v2.0.0; VS Code 7.0.0 onto hpcworker (it replaces its grid scripts with `hpcworker` commands and moves students with a non-destructive "Move my worker" button, never deleting `~/.beethoven`).
- **Open:** whether hpcworker stays the home of the contract and profiles (the design keeps it there until greg decides the fourth-repository idea, `plan/REPO_SPLIT.md` section 2).
- **Never:** all the hard rules in `claude_context.md` section 2 bind here. Repository plumbing: greg creates repositories and tags by hand; PRs open ready, never draft.

## 3. Files Modified & State

| File Path | Status | Key Modifications / Purpose |
| --- | --- | --- |
| README.md | Complete | The only file: greg's creation step (private, README only, Allow auto-merge on); seen in the desktop thread's clone, not read from here |
| the shared code | Pending | Nothing written in the repository. Design and its two critiques: `/mnt/project-files/staging/desktop-thread/beethoven-base-design-and-critiques.json`; survey of the three editions (20 shared concerns): `beethoven-base-survey.json` beside it |
| /mnt/project-files/base/DESIGN.md | Pending | Announced by the desktop thread (the staging README says the design was folded into it); the folder was empty at 21:18Z |

## 4. Completed Milestones

1. greg asked for the base at 20:04:55Z and allowed CI secrets at 20:14:53Z; he created the repository at 20:25Z.
2. The desktop thread attached and cloned it and saved its survey at 20:28Z.
3. The design with two critiques was done at 20:58Z, with no fetch route and no read token; the desktop thread corrected its 20:17Z message to greg that had said each edition fetches the base with a token.

## 5. Active Blockers & Errors

- greg's decisions the design names, to come as cards: (a) keep the `claude -p` request queue by moving it into hpcworker as contract V13 (recommended) or drop ask, send and result from VS Code 7.0.0; (b) drop the grid-side licence check, keeping the laptop's licence gate (recommended); (c) which access-service grant puts a VS Code-only student on the list `grid_access.sh` applies.
- Unresolved in the critiques (checked 21:18Z): base as specified turns desktop's `forbidden.mjs` and the extension's hygiene test red; nothing stops editions drifting onto different base versions (the check accepts a downgrade, `vendor` never deletes); the credential strip net would strip the GitHub and Hugging Face tokens VS Code passes on purpose, and `hpcworker env set` must refuse credential names; base is larger than what two or three editions really share (about 850 lines of real duplicates before VS Code moves); the design names beethoven-research as carrying the qa copy, which is beethoven-agents; VS Code is already at `TERMS_VERSION` 7 on its branch, so its texts go to 8, not 7; hpcworker CI holds no secret, so a workflow there holding a base token would change that rule.
- Not readable from the hand-off thread's session (`gh api`: "GitHub access to this repository is not enabled for this session"); a thread that works here attaches it with `add_repo` first.

## 6. Immediate Next Actions (Hydration Directives)

1. Attach the repository with `add_repo`, then `git ls-remote https://github.com/OpenSpineConsortium/beethoven-base` and `gh api "repos/OpenSpineConsortium/beethoven-base/pulls?state=all"` to see what exists.
2. Read `/mnt/project-files/base/DESIGN.md` if it exists, else the design JSON's `design` key and both critiques; read the desktop thread newest first with `fetch_thread`; leave the build to the desktop thread unless greg reassigns it.
3. When base PR #1 opens or greg answers a decision card, refresh this file and the affected edition files under `/mnt/project-files/state/repos/`, and append a ledger row.

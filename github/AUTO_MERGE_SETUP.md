# Auto-merge on green: the four repository settings

**State at 02:25Z (greg's 02:11Z rules applied):** Allow auto-merge is ON in all four repositories
(greg). Still open, each refused from the cloud session (the GitHub proxy refuses settings writes;
the session's auto mode refused the rest): (1) import the two rulesets (section A step 2, or the
`gh` lines in B); (2) add `proposed-automerge.yml` as `.github/workflows/automerge.yml` in
beethoven-research and beethoven-desktop, so every pull request opened ready gets auto-merge armed
by itself; (3) optionally add `proposed-rulesets.yml` as `.github/workflows/rulesets.yml` plus a
fine-grained token (Administration: read and write on these repos) stored as the Actions secret
`RULESETS_TOKEN`, so a change to `.github/rulesets/main.json` on main applies itself; (4) mark
beethoven-research PR #1 ready for review once (every later pull request opens ready). From then
on no human step per pull request: the gate before each push (`.githooks/pre-push`, in the repo
since fcd1955) and the same gate as the required check on main decide.

Written 2026-10-04 02:05Z by the skeleton thread after greg upgraded the organization to GitHub
Team (02:02Z). Claude's cloud sessions cannot change repository settings (the session's GitHub
proxy refuses every settings write), so these are the maintainer's clicks, or `gh` commands from a
machine where `gh` is signed in as Gregory-Schwing-MD-PhD. Everything here was checked against
GitHub's REST and rulesets documentation on 2026-10-04 before it was written.

## A. In the browser

For each of the four repositories (`hpcworker`, `beethoven-extension`, `beethoven-research`,
`beethoven-desktop`):

1. Settings → General → scroll to **Pull Requests** → tick **Allow auto-merge** (maintainer
   or admin).

For `beethoven-research` and `beethoven-desktop`, the two PR-driven repositories:

2. Settings → Rules → Rulesets → **New ruleset** → **Import a ruleset** → choose the JSON file
   beside this note (`ruleset-main-beethoven-research.json` or
   `ruleset-main-beethoven-desktop.json`) → **Create**.

What the imported rule does on `main`: no deletion, no force-push, and the repository's CI
checks must be green before a pull request can merge. Organization admins (you) bypass it, so a
direct push to main by you still works. The checks are named exactly as GitHub reports them on
each repository's PR #1 head; the "up to date with main" option is off on purpose, because
auto-merge never presses "Update branch" for you.

`hpcworker` and `beethoven-extension` get no rule, because their CLAUDE.md says commits go
straight to main. Import the same kind of rule there later if you want it (their check names are
`suite (ubuntu, current python)` and `suite (centos 7, python 3.6, bash 4.2)` for hpcworker;
`bridge (rust, ubuntu-latest)`, `bridge (rust, macos-latest)`, `bridge (rust, windows-latest)` and
`typecheck, vitest, mock selftest, build` for the extension).

## B. Or from your laptop with gh

```sh
cd <this folder>
for r in hpcworker beethoven-extension beethoven-research beethoven-desktop; do
  gh api -X PATCH "repos/OpenSpineConsortium/$r" -F allow_auto_merge=true --jq '{full_name, allow_auto_merge}'
done
gh api -X POST repos/OpenSpineConsortium/beethoven-research/rulesets --input ruleset-main-beethoven-research.json --jq '{id, name, enforcement}'
gh api -X POST repos/OpenSpineConsortium/beethoven-desktop/rulesets  --input ruleset-main-beethoven-desktop.json  --jq '{id, name, enforcement}'
```

## C. Per pull request, from then on

- A draft never merges by itself. Mark it **Ready for review** first.
- If its checks are still running: **Enable auto-merge** (the button shows only while the PR
  cannot merge yet). It merges the moment the required checks pass.
- If its checks are already green: the button is plain **Merge**; press it.
- A Claude thread never marks a PR ready, enables auto-merge or merges; those stay yours.

Beethoven runs Claude Code and is not an Anthropic product; "Claude" and "Claude Code" are
Anthropic's marks, used here to say what it runs.

---
name: pr-convention-test-determined
description: greg's rule of 2026-10-04 02:11Z that pull requests merge on green with no human step (open them ready, never draft; auto-merge armed; the gate before every push), what is built for it and what a cloud session cannot do
metadata:
  type: feedback
  modified: 2026-10-04T02:23:44.742Z
---

greg (skeleton thread, 2026-10-04 02:11Z, verbatim in spirit): no human step per pull request,
"it should all be test determined"; the contract and concolic gate is tested before pushes and
is among the first bootstrap items; rulesets must be updatable from code.

**Convention from then on:** every thread opens pull requests READY for review, never as drafts.
Merging is decided by the required checks on `main`; nobody reviews by hand.

**Built (beethoven-research, fcd1955):** `.githooks/pre-push` runs `pixi run gate` before every
push (measured 3 min 18 s; `SKIP_GATE=1` skips knowingly); `pixi run hooks` and the session-start
hook set `core.hooksPath`; `.github/rulesets/main.json` is the rule as code; CLAUDE.md says so.
Allow auto-merge is on in all four org repos (greg's clicks).

**Workflows (2026-10-04 03:3xZ):** greg asked explicitly at 03:35Z; beethoven-desktop already has
`.github/workflows/automerge.yml` (GraphQL enablePullRequestAutoMerge, MERGE, only when main carries
a required-checks rule) and `rulesets.yml` (push on rule files + daily + dispatch; RULESETS_TOKEN)
on main since 859b4c7; the skeleton thread added the same two files to beethoven-research on its
branch (PR #2). Measured 03:42Z: the workflow added in research PR #2 ran on that same PR's `opened` event and
armed auto-merge (enabled_by github-actions[bot], method merge), so a PR that introduces the file
arms itself; no click. PR #2 then merged by itself at 03:44Z (merged_by github-actions[bot], merge commit 33ce108) once the gate and image
lanes were green: the first test-determined merge with no click. greg created the RULESETS_TOKEN
secret in both repos (03:51Z); verified 03:55Z by dispatching rulesets.yml in each (both green, no
missing-secret notice). The proxy blocks listing secrets (403) but allows workflow dispatch and run reads. PR #1 (research) was
merged by greg's click 03:29Z (772df94).

**A cloud session cannot:** write repository settings (proxy 403), and the auto mode classifier
refused marking a PR ready, writing a workflow that arms auto-merge (`gh pr merge --auto` on
opened PRs) and writing a rulesets-apply workflow with a `RULESETS_TOKEN` secret. Also refused (03:2xZ): `gh pr merge --auto --merge` on PR #1 itself ("Merge Without Review"). The proposals
sit in `/mnt/project-files/github/proposed-automerge.yml` and `proposed-rulesets.yml` with
`AUTO_MERGE_SETUP.md`; greg adds them or allows them.

**Why:** greg paid for GitHub Team to remove the human step; a thread that opens a draft or waits
for a review click works against that. **How to apply:** open PRs ready; never arm auto-merge or
merge from a session unless greg has allowed it; cite this rule. See [[github-plan-automerge]].

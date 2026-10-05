---
name: github-plan-automerge
description: The OpenSpineConsortium GitHub org went from Free to Team on 2026-10-04 (branch rules and auto-merge on private repos); the main ruleset prepared for beethoven-research and beethoven-desktop and the verified facts behind it
metadata:
  type: project
  modified: 2026-10-04T02:23:55.186Z
---

Measured 2026-10-04 (skeleton thread): the org's repos (`hpcworker`, `beethoven-extension`,
`beethoven-research`, `beethoven-desktop`) are private. On Free the ruleset API answered 403
"Upgrade to GitHub Pro or make this repository public"; GitHub's docs: protected branches,
rulesets and auto-merge are public-only on Free. **greg upgraded to Team at 02:02Z** (rules API
200) and ticked Allow auto-merge on all four repos. Team is US$4 per user per month, billed per
member and per outside collaborator on a private repo.

**Ruleset for `main`** (prepared, import-ready JSON in `/mnt/project-files/github/`; also
`.github/rulesets/main.json` in beethoven-research): deletion and non_fast_forward blocked;
required_status_checks = each repo's CI job display names (research: `gate (lock → lint,
typecheck, tests, CrossHair/Z3)` and `image (apptainer build)`; desktop: `typecheck, forbidden,
tests against sshd, pack`, `unit tests (macos-latest)`, `unit tests (windows-latest)`) with
GitHub Actions `integration_id` 15368 (from the repos' own check runs); `strict` OFF on purpose
(auto-merge never presses "Update branch"); bypass `OrganizationAdmin` always (`actor_id`
ignored); `~DEFAULT_BRANCH`. Creating a ruleset needs Administration: write. No REST call arms
auto-merge on a PR (GraphQL or `gh pr merge --auto`); the Enable auto-merge button shows only
while the PR cannot merge immediately. A merge by `GITHUB_TOKEN` starts no `push` run on main.

**Imported by greg 2026-10-04 ~03:15Z, read back 03:2xZ by the skeleton thread:** both rulesets
are active on `~DEFAULT_BRANCH` (research id 24440691, desktop id 24440600, name "main: checks before
merge"), deletion + non_fast_forward blocked, the checks above required, strict off, OrganizationAdmin
bypass. The classifier refused `gh pr merge --auto --merge` on research PR #1 ("Merge Without Review"),
so arming auto-merge stays greg's click (or the proposed workflow).

**Cloud sessions cannot write repository settings** (`PATCH repos/*`, `POST .../rulesets`: 403
"not permitted through this proxy"); the import stays greg's. Enterprise vs Team:
[[github-enterprise-vs-team]]. The no-human-step rule: [[pr-convention-test-determined]].

**Why:** other threads should not re-measure this. **How to apply:** read settings back with
`gh api repos/{o}/{r}` and `.../rulesets` before claiming a state.

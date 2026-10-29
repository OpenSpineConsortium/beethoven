---
name: org-owner-approval-ruleset
description: Since 2026-10-22 02:02Z an organization ruleset "Require owner approval to merge" needs one approving review on every OpenSpineConsortium default branch; org admins bypass it and sessions act as an admin, so a direct push or self-merge from a thread slips past it
metadata:
  type: project
  modified: 2026-10-22T14:18:40.359Z
---

Checked 2026-10-22 09:2xZ with `gh api repos/OpenSpineConsortium/<repo>/rulesets` (the org-level
endpoint is refused to sessions): ruleset 25608346, "Require owner approval to merge", source
Organization, enforcement active, created 2026-10-22T02:02:46Z, on `~DEFAULT_BRANCH` of hpcworker,
beethoven-extension, beethoven-qa, beethoven-agents, beethoven-research, beethoven-desktop,
beethoven-vscode and the hub (beethoven-base, beethoven-sites not readable from that session).
Rules: no deletion, no force-push, changes only through a pull request with 1 approving review,
stale approvals dismissed, the last push approved by someone else, extra approval for unattributed
changes. Bypass: OrganizationAdmin, always; `current_user_can_bypass: always` for a thread, since
threads act as greg. The repositories' own "main: checks before merge" rulesets (qa, agents,
research, desktop) still require their CI lanes. Who created it and why is not on record in this
project; it sits beside greg's rule of 2026-10-04 that PRs merge on green with no human step
([[pr-convention-test-determined]]), which it overrides in effect.

The hand-off thread's direct hub sync of 09:19Z (c1dd9b9) went through the bypass before the
rule was seen; it asked greg on a card (cmsg_01JbwQwHoYeBWptjPB5c6u8mVnVvgpUtmqU9J7uZhmG2oD) whether
hub syncs go by pull request, recommending yes.

What follows (checked 2026-10-22 with `gh api .../pulls`): session pull requests are opened as
greg, and GitHub never lets an author approve their own, so they merge only through his bypass;
auto-merge armed by `automerge.yml` waits for a review it cannot get, so qa, agents, research and
desktop should no longer merge on green (inferred: none of the four has opened a PR since). vscode #16, #18, #19 and hpcworker
#31, #32 merged after the rule with 0 reviews, merged_by greg: the bypass.

**Why:** a rule named "owner approval" with an admin bypass is meant for greg's hand, not for
sessions that act as him. **How to apply:** no thread pushes straight to a default branch or
merges or arms auto-merge on its own pull request while this rule stands, unless greg says
otherwise for that repository; open the PR ready for review and say it waits on his approval.

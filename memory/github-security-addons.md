---
name: github-security-addons
description: What GitHub's scanning, code quality, coverage, secret-scanning and Copilot-review ruleset rules need and cost on the OpenSpineConsortium Team org (read 2026-10-04), and why main.json leaves them out until the products are on
metadata:
  type: reference
  modified: 2026-10-04T03:02:41.717Z
---

Read 2026-10-04 (skeleton thread, greg's 02:47Z question). The repos are private, so none is free:

- **Require code scanning results** → CodeQL → GitHub Code Security, $30 per active committer per
  month (changelog 2025-03-04; on Team since 2025-04-01). REST rule `code_scanning`.
- **Require code quality results** and **Restrict code coverage** → GitHub Code Quality, $10 per
  active committer per month since GA 2026-07-20 (free in preview before); Python supported; the
  coverage rule needs a Cobertura XML upload from CI and is public preview. REST `code_quality`
  (severity) and `code_coverage` (minimum_coverage, max_coverage_drop).
- **Require secret scanning alerts are resolved** → GitHub Secret Protection, $19 per active
  committer per month (push protection included); public preview; **no REST rule type exists**, so
  it is a UI click, not rule-as-code.
- **Copilot code review** → author on Copilot Pro $10 / Pro+ $39 / Max $100 or a Business or
  Enterprise licence, or org-paid AI credits; REST `copilot_code_review`; posts a review, blocks
  nothing by itself.

Active committers count once across the org for 90 days; the engine's commits are authored
`Claude <noreply@anthropic.com>`, so expect two committers (greg plus that address). All three
products at two committers: about $118 a month. State read back 2026-10-04 02:50Z on
beethoven-research: code_security, secret_scanning and push protection all disabled. **greg chose
"None now" on the card at 03:09Z**: nothing is bought; main.json keeps the gate and image lanes only. A scanning
rule imported while its product is off blocks every merge ("required tool not configured"), which
is why `.github/rulesets/main.json` holds only the gate and image lanes. Proposal files:
`/mnt/project-files/github/SCANNING_RULES.md`, `ruleset-main-scanning-beethoven-research.json`,
`ruleset-main-copilot-review-beethoven-research.json`. See [[github-plan-automerge]],
[[pr-convention-test-determined]].

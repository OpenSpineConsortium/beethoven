---
name: github-enterprise-vs-team
description: What GitHub Enterprise Cloud would add over Team for the OpenSpineConsortium private repos (read 2026-10-04 from GitHub's docs and pricing, three refuters) and the recommendation given to greg
metadata:
  type: reference
  modified: 2026-10-04T01:57:49.530Z
---

greg asked 2026-10-04 01:33Z what Enterprise would get the project. Read from GitHub's plans page,
pricing page and feature docs, checked by three refuting agents (skeleton thread):

- Price: Team $4, Enterprise "starting at" $21 per user per month, both "for the first 12
  months*" (footnote unread).
- Over Team, for private repos: 50,000 vs 3,000 Actions minutes a month (the extension's CI builds
  the bridge on macOS and Windows runners, which count at higher multipliers; overage is billed per
  minute); merge queue; artifact attestations; commit-metadata regex rules; deployment protection
  rules; SAML SSO, SCIM, managed users, IP allow list, audit-log API and streaming, internal
  repos, enterprise account, data residency, 99.9% SLA, SOC reports, premium support.
- Already on Team (not a reason to upgrade): repository rulesets AND organization-level rulesets
  (GitHub changelog 2025-06-16; the plans page's wording is stale), push rulesets, auto-merge,
  Secret Protection ($19) and Code Security ($30 per active committer) add-ons.
- Recommendation given: stay on Team; if minutes run short, trim the macOS/Windows builds to
  releases.

**How to apply:** quote these as read on 2026-10-04; re-check the pricing page before quoting a
price again. See [[github-plan-automerge]].

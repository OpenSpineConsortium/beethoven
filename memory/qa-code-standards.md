---
name: qa-code-standards
description: beethoven-qa 2.0.0 code standards (greg's "Auditable Code Quality Standards" as PR blockers): six groups, the one required check, merged 2026-10-05 01:03Z, what consumers and greg still do
metadata:
  type: project
  modified: 2026-10-05T01:04:37.543Z
---

greg's ask (2026-10-04 23:26Z, desktop thread; coordinator split it to the code-quality thread
cmsg_01JbwQwHoYeBWptjPB5c6u8mKGFJfGGY87GoSjLtzXoYao): his Drive doc "Auditable Code Quality
Standards" as pull-request blockers, each group independent, coaching later.

**Built and merged:** beethoven-qa PR #3 merged on green 2026-10-05 01:03Z (main 40227fa,
merged_by github-actions[bot]). `python -m beethoven_qa standards <group>|all`, groups readability,
design, duplication, coverage, security, supply-chain; each its own job in the kit's
`standards.yml`; the one required check is `standards (every group green)`, applied to qa's main
by a dispatched rulesets.yml run at 01:04Z ("updated 24457138 main: checks before merge"). Only
new or worse findings block (matched against the base commit). Limits change only in a qa release;
no repo config or suppression comment loosens them. Coaching: plugin skill `code-standards`.
Docs: qa `docs/STANDARDS.md`. The gate task now runs the standards; the local gate takes ~9 min,
GitHub's gate job ~15 min.

**Still to do:** greg publishes release v2.0.0 on 40227fa (sessions cannot push tags). The re-pin
prep is pushed as wip commits on branch claude/quality-gates-qvn6wa: beethoven-agents 2e668ed,
beethoven-research effe751 (SKIP_GATE=1, greg's 01:20Z push-now ask). PRs opened from the UI at
01:25Z, research #5 and agents #3, are held as DRAFTS with auto-merge off until the copy lands
(merged early they would break the gate); mark ready for review when done, which re-arms it. Done there: the
standards' dependency lines (agents takes complexipy from PyPI on osx-arm64 only, conda-forge has
no build there), `standards` task, locks re-solved (additions only; linux-64 builds equal qa's),
the check in main.json, ci.yml checkout pinned plus read-only permissions, CLAUDE.md (five kit
files). Left after the tag: from each consumer, `vendor --into . --kit` at v2.0.0 (CONSUMING.md
"Updating"), vendor-check, the gate, amend into one commit, open the PR, dispatch rulesets.yml.
Dry run on 2.0.0's code (01:10Z): both consumers pass all six groups; agents' old code holds 48
readability, 3 design (LCOM4 of `_TextStream`) and 4 security (B108 /tmp literals) findings,
recorded as unchanged. Next feature, not started: a PostToolUse hook running the cheap groups as a
session edits (coordinator 01:05Z: after the re-pin, not put to greg).

Related: [[pr-convention-test-determined]], [[three-repo-staging]].

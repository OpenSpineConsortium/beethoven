---
name: qa-code-standards
description: beethoven-qa code standards (greg's "Auditable Code Quality Standards" as PR blockers): six groups, one required check, in qa since 2.0.0, in both consumers since 2026-10-07; the PostToolUse coaching hook merged as 4.0.0 on 2026-10-08, untagged
metadata:
  type: project
  modified: 2026-10-08T11:02:55.534Z
---

greg's ask (2026-10-04 23:26Z, desktop thread; coordinator split it to the code-quality thread
cmsg_01JbwQwHoYeBWptjPB5c6u8mKGFJfGGY87GoSjLtzXoYao): his Drive doc "Auditable Code Quality
Standards" as pull-request blockers, each group independent, coaching later.

**Built and merged:** beethoven-qa PR #3 merged on green 2026-10-05 01:03Z (main 40227fa). Tag
v2.0.0 is NOT on 40227fa but on 53d5ae5 (40227fa plus an interface-standard "boundary" check), and
v3.0.0 on 08aca99, both made 2026-10-07 by session_01Rvv9SUDARQdG2w3LefMj3K, which is not a thread
of this project (branch claude/repo-encapsulation-9hmh9f; most likely greg's other account).
`python -m beethoven_qa standards <group>|all`, groups readability, design, duplication, coverage,
security, supply-chain; each its own job in the kit's `standards.yml`; the one required check is
`standards (every group green)`. Only new or worse findings block (matched against the base
commit). Limits change only in a qa release; no repo config or suppression comment loosens them.
Coaching: plugin skill `code-standards`. Docs: qa `docs/STANDARDS.md`.

**Consumers (checked 2026-10-08 11:0xZ on origin/main):** beethoven-agents and beethoven-research
both carry the copy at v3.0.0 with `standards.yml` and the check in `.github/rulesets/main.json`.
History: greg marked the held draft prep PRs ready at 01:26Z on 10-05 (research #5 auto-merged,
agents #3 he merged by hand at 01:30Z), so both mains ran the standards task on a 1.0.0 copy
until that outside session re-pinned 2.0.0 and 3.0.0 on 10-07. The code-quality thread
was blocked on its account's seven-day usage window from 10-05 01:33Z to 10-08 11:00Z. Its agents
branch commit 998fc55 (copy from untagged 40227fa) is unused. Ledger and INTERVENTIONS rows
written 10-08.

**Coaching hook (4.0.0):** at the coordinator's go (10-08 11:06Z, on qa 3.0.0, agents and research
untouched; greg had a lane card open) qa PR #6 merged by auto-merge 10-08 12:11:57Z as 615ed3e.
`python -m beethoven_qa coach` plus plugin/hooks/{hooks.json,coach.sh}: after each Edit/Write it
says what CI would block in that file (never coverage), about 3 s, or nothing; exit 0 always;
`pixi run --as-is`. **Left:** greg tags v4.0.0 on 615ed3e; then whoever owns agents and research
re-pins them with `vendor --ref v4.0.0 --kit` (optional .claude/settings.json snippet in qa
docs/CONSUMING.md). Not yet measured: the hook in a live session; allowManagedHooksOnly in the
agents' image.

Related: [[pr-convention-test-determined]], [[three-repo-staging]].

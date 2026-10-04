---
name: three-repo-staging
description: State of the beethoven-qa / beethoven-agents / beethoven-research split (2026-10-04 19:48Z): complete; all three on main with live rulesets, qa v1.0.0 released on 16415b4
metadata:
  type: project
  modified: 2026-10-04T19:48:30.000Z
---

Thread "Three-repo separation" (cmsg_01JbwQwHoYeBWptjPB5c6u8mTY4EBQjdtHsPXP8iwJoc9c) owns the split.

- beethoven-qa: PR #1 and #2 merged (main 16415b4); ruleset live. `v1.0.0` released by greg on 16415b4 at 19:45Z (Releases page; lightweight tag; BEE-195 Done). The session's GitHub proxy refuses tag pushes (403): a future release tag is greg's hand step too, never retried from a session.
- beethoven-agents: PR #1 hand-merged by greg 16:15Z (0de7913), ruleset id 24460184 active; BEE-196 Done.
- beethoven-research: slimmed by PR #4, merged by greg's hand 19:34Z (8dd5be2); the merge applied the new ruleset (id 24440691, only `gate (lock → lint, typecheck, tests, CrossHair/Z3, vendor-check)`), so research PRs now merge on green. First research module `splits.py` (split-level check; BEE-116 In Progress); BEE-197 Done.
- Lessons: in a multi-repository thread `core.hooksPath` is NOT set by any hook; run `git config core.hooksPath .githooks` in each checkout before the first push. A Workflow in this 4-CPU session runs only 2 agents at once (min(16, cpus-2)): a 4-lens x 3-verifier review took about 2 h; size reviews to that or decide outstanding votes yourself.
- Measured: qa gate on a runner 4-5 min; agents gate 9 min 26 s; research gate locally 1 min 44 s (2 targets).

**Why:** a successor would otherwise retry the tag push, re-vendor again, push without the hook, or wait on auto-merge that cannot fire.
**How to apply:** the split needs no more work; a new qa release is tagged by greg, then each consumer re-pins with `vendor --into <repo> --kit` (qa docs/CONSUMING.md). Related: [[bee-account-switching]], [[pr-convention-test-determined]].

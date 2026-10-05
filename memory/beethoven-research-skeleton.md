---
name: beethoven-research-skeleton
description: What the beethoven-research repo skeleton contains (PR #1, merged by greg 2026-10-04 03:29Z, merge commit 772df94), incl. the baked managed settings + PreToolUse guard, the pre-push gate, D4 and the parallel-work files; follow-up commits go up as new PRs from the same branch
metadata:
  type: project
---

`OpenSpineConsortium/beethoven-research` skeleton laid down 2026-10-04 by the skeleton thread:
`main` = bootstrap `56bc269`; PR #1 (https://github.com/OpenSpineConsortium/beethoven-research/pull/1,
branch `claude/project-thread-kss9jn`; greg marked it ready 03:24Z and merged it 03:29Z, merge
commit `772df94`, so `main` now carries e623426, 861496b and 731367b; the branch was restarted
from `origin/main` and the follow-up PR #2 (24f8a2f the transcript hand-off, d6d7237 the automerge and rulesets
workflows plus the plan-aligned text) merged by auto-merge at 03:44Z, merge commit 33ce108)
carries: `pixi.toml` + solved `pixi.lock` (pixi 0.81.0, linux-64), `containers/claude-verify.def` +
`build.sh` (compute node only, --fakeroot, node-local temp, writes `claude-verify.digest`),
`containers/managed-settings.json` (baked at `/etc/claude-code/managed-settings.json`: bypass locked,
deny rules, timeouts, no updates/telemetry/artifacts, spawn depth 1, `allowManagedHooksOnly`, the
guard), `src/beethoven_research/{contracts,example,guard}.py` (`guard.py` = the PreToolUse guard,
contracted, fails closed), `tools/verify_gate.py`, 125 tests, `.github/workflows/ci.yml` (gate +
image lanes), `.githooks/pre-push` (runs `pixi run gate`, ~3.5 min, `SKIP_GATE=1` skips knowingly),
`.github/rulesets/main.json` (rule as code, not yet imported), `.claude/hooks/session-start.sh`,
`CLAUDE.md` (usage credits excluded; D4 several accounts; PRs open ready).

**Since e623426 (D4 + parallel work):** `docs/ACCOUNTS.md`, `docs/PARALLEL.md`,
`.claude/agents/stream.md` (`isolation: worktree`), `.claude/workflows/{gate-until-green,verify-module}.js`
(both parse: dry run with `maxRounds: 0`), `.claude/settings.json` (`worktree.baseRef: head`,
`workflowSizeGuideline: large`), `.claude/worktrees/` ignored. See [[multi-account-d4]].

**Measured (2026-10-04):** CI gate lane real; image lane ~2 min (apptainer 1.3.6, Claude Code
2.1.289). CrossHair gate ~3 min; it found one real crash before the fix. In this cloud session
`pixi` is at `~/.pixi/bin` and NOT on PATH in Bash: export it before `git push` or the pre-push
hook fails. **Not done:** no grid build, no committed digest (BEE-103). BEE-102/104 and BEE-123/124 were
In Review on PR #1 and close with its merge.

**Rules fixed by measurement:** `@beartype` OUTSIDE icontract decorators. `conda-pypi-map = false`
in `[workspace]`. Repo hooks do NOT run in multi-repo project threads (need the setup script).
Release-asset downloads may 403 in cloud sessions. The sign-in dir (`CLAUDE_CONFIG_DIR`) must be
bound READ-WRITE; protection is deny rules + guard + code, never a mount flag.

**Why:** later engine threads build on this and should not re-derive it.
**How to apply:** `pixi run gate` is the definition-of-done check; add modules with contracts or
the gate refuses them. Put nothing per-step into managed-settings.json (see
[[claude-code-token-knobs-verified]]). See [[build-plan-rev2]], [[pr-convention-test-determined]],
[[measurement-ledger]].

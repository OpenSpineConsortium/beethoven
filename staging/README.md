# Staged repositories (thread "Three-repo separation")

Git bundles of the two repositories staged before GitHub has them, kept here so the work outlives
the thread's container. Each holds one branch, `claude/three-repo-separation-upobqe`, whose commits
are local snapshots, not the history that will be pushed.

- `beethoven-qa.bundle`: the code-writing and verification framework (gate, pinned-copy command,
  kit, Claude Code plugin). Pushed as its PR #1 once greg creates `OpenSpineConsortium/beethoven-qa`.
- `beethoven-agents.bundle`: the nested agentic framework (image, guard, accounts docs, and `bee`,
  copied from beethoven-research b7b8650). Its `vendor/beethoven-qa/ORIGIN` names a scratch commit
  that is not on GitHub; it is re-vendored from beethoven-qa's real `v1.0.0` tag before it is pushed.

Restore with `git clone -b claude/three-repo-separation-upobqe <bundle> <folder>`. The boundary
and the order of work are in `../plan/REPO_SPLIT.md`.

---
name: beethoven-desktop
description: The desktop thread's repos (beethoven-desktop, beethoven-vscode, and the API-key sweep in hpcworker and beethoven-extension), its PRs, what is pending greg and what is unmeasured
metadata:
  type: project
  modified: 2026-10-04T20:30:00.000Z
---

Thread "Build the Claude Desktop ssh plugin" (root cmsg_01JbwQwHoYeBWptjPB5c6u8m3KSccv8f9KZdoYiLkxZons), branch claude/project-thread-fx3wkp in every repo (restarted from main after each merge). PRs go through greg's account, so GitHub refuses his review request; he is assigned instead. hpcworker and beethoven-extension have NO automerge/rulesets workflows (the auto-mode classifier refused to let this thread write them); greg copies beethoven-desktop's three files himself and hand-merges until then.

beethoven-desktop: PR #1 d60c0b2 (1.0.0), PR #2 dbc0fb1 (worker_list, Windows ssh), PR #3 merged 07:39Z (account_list), PR #4 d014a82 merged 15:36Z (no-API-key posture check in scripts/forbidden.mjs). Design: one dependency-free MCP server as .mcpb and Claude Code plugin; sign-in is a terminal with ssh, ControlMaster 4h, BatchMode tools; on the grid only gate verbs plus read-only SFTP of status.json; no network of its own. Claude Code Desktop's own SSH is NOT a way in (login node forbidden; CentOS 7 glibc 2.17 on compute nodes).

No API key anywhere ([[no-api-key-anywhere]]), fixed by this thread 2026-10-04: beethoven-vscode PR #6 3ef7b08 (greg merges by hand; no automerge there); hpcworker PR #1 6eff9e9 = framework 17 (hpcw_claude_signin; login_plain.sh host check; status_counts_subscription needs status "version" >= 17; codes signin-billed/signin-method; fifteen variables stripped); beethoven-extension PR #1 1bfb739 (isClaudeAuthUrl judges the parsed host; the two codes). greg 16:24Z (card): a fresh grid sign-in never signs anyone out: `--login fresh` is refused by framework 17 and 15.0.0's panel tells the student to sign out on a compute node themselves (added to both PRs). The signed bridge packages are [[signed-bridge-packages]].

greg's asks of 15:19Z: a grid-rules repository (awaits his word; plan/REPO_SPLIT.md section 2) and a two-queue policy; `hpcworker queue report [--days N] [--limits]` (one sacct, wait = Start minus Eligible, per partition/QoS) is built and reviewed, going up as hpcworker PR #3 so greg measures first. VS Code `beethoven.account` setting (plan/ACCOUNT_SWITCH_CLIENTS.md item 2) built and reviewed, going up as the next VS Code PR (#7 is the hand-off thread's types pin-back) (TERMS 7; whether the Claude Code VS Code extension honours CLAUDE_CONFIG_DIR is not yet measured).

beethoven-base (greg 20:04Z): move the code the three editions share into OpenSpineConsortium/beethoven-base; greg created it 20:25Z (README only). greg 20:14Z allowed CI secrets ("i dont mind creating secrets"): a read-only GitHub token for fetching base, a write token in base to open "take the new base" PRs; RULESETS_TOKEN is admin-only, not for code; still never a Claude/Anthropic key. Why VS Code has its own grid scripts (greg asked "wtf"): it came first (Ashley for VS Code); hpcworker was built 2026-09-28 by reworking its scripts for the browser edition; the read-only rule kept it from moving. Moving it onto hpcworker is part of the base design.

Pending greg: build and sign VS Code 5.0.0 (PR #6 merged) (tools/release.mjs), unpublish Ashley 3.0.0 once 5.0.0 is listed; laptop checks 1-15 (docs/LAPTOP_CHECKS.md); the signing enrolments in [[signed-bridge-packages]].

Half-done work and greg's open steps as of 20:30Z: [[desktop-thread-in-flight]].

Related: [[bee-account-switching]], [[multi-account-agent-teams]], [[measurement-ledger]].

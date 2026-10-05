---
name: desktop-thread-in-flight
description: What the desktop thread had half-done at 2026-10-04 20:30Z (greg near his weekly limit): extension 15.0.0, hpcworker queue report, VS Code account setting, beethoven-base design, and greg's open steps for those repos
metadata:
  type: project
  modified: 2026-10-04T23:55:00.000Z
---

Thread "Build the Claude Desktop ssh plugin" (cmsg_01JbwQwHoYeBWptjPB5c6u8m3KSccv8f9KZdoYiLkxZons). Everything finished is pushed to `claude/project-thread-fx3wkp`; what GitHub lacks is in `/mnt/project-files/staging/desktop-thread/` (README there says how to apply each file).

- **beethoven-extension 15.0.0** (signed bridge installers + store upload + Mac-only release): branch at 9aa1171 with everything merged (tsc, vitest 726, chrome build, hygiene green). The staging bundle is now superseded. Running (resumed 23:12Z after a container restart): docs finish plus a whole-change review and fix in worktree wt-M. Then open the PR (no automerge; greg hand-merges).
- **hpcworker queue report**: PR #3 MERGED 21:52Z (carried the V12 contract parity commit). The hpcworker branch must restart from origin/main before new work. greg's next step: `hpcworker queue report --days 30 --limits` after the next deploy_shared.
- **VS Code `beethoven.account`** (ACCOUNT_SWITCH_CLIENTS item 2): branch at c065f25 (rebased on main cc76efd, which has #7; 85 unit tests); grid scripts 9 being added (terms back to 7); then open the VS Code PR (#8 or later). Whether the Claude Code VS Code extension honours CLAUDE_CONFIG_DIR is not yet measured.
- **VS Code grid scripts 8 hazards** (verified on main 24a9896; greg told to hold 5.0.0 and not run uninstall, claude forget, access init, library publish): fix is grid scripts 9 on the VS Code branch (workflow vscode-grid-scripts-9).
- **greg 23:26Z (this thread)**: (a) start workers on every queue, the first to get a node serves the client: building in hpcworker (worktree scratchpad/hw-race, branch wip/race, workflow all-queue-launch; framework 18; retargets tools/push_org.sh off the old beethoven repo); (b) his Drive doc "Browser HPC Bridge Architecture Analysis" (15ajSPhNuZz3rk7RsYwwZNxBViL9D1NxQzO5A9KMAQP0) becomes extension docs/BRIDGE_TRANSPORT.md (worktree ext-nm, rides the 15.0.0 PR); the doc's top pick, a cloud relay built to get past campus inspection and the VPN, is set aside; the signed binary stays with scripts as fallback. The code-standards packs and the hub repo with the project files went to other threads (coordinator 23:31Z); so did greg's 23:46Z site-module ask (Wayne State into a loadable module; coordinator 23:48Z), which this thread fed with what it knew and the worker_race field shape.
- **beethoven-base design** written and checked 23:45Z (/mnt/project-files/base/DESIGN.md: pinned copy per edition, no secret; hpcworker canonical with vectors; VS Code onto hpcworker later); D1-D8 sent to greg 23:5xZ, awaiting his answer before base PR #1.

**greg's open steps for these repos:** hand-merge the three PRs above when opened (VS Code #6, hpcworker #1 #2 and extension #1 all merged by 18:13Z); copy desktop's automerge.yml, rulesets.yml, rulesets/main.json into hpcworker and beethoven-extension; build and sign VS Code 5.0.0, list it, then unpublish Ashley 3.0.0; Apple Developer Program, two Developer ID certificates, notarytool profile; Azure Artifact Signing account (identity validation, certificate profile); Google Cloud Desktop OAuth client and the store item id and publisher id; desktop laptop checks (docs/LAPTOP_CHECKS.md) and keep-or-revert of desktop PR #1; later, the base read-only token.

Related: [[beethoven-desktop]], [[signed-bridge-packages]].

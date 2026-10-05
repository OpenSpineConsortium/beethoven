---
name: desktop-thread-in-flight
description: What the desktop thread had half-done at 2026-10-04 20:30Z (greg near his weekly limit): extension 15.0.0, hpcworker queue report, VS Code account setting, beethoven-base design, and greg's open steps for those repos
metadata:
  type: project
  modified: 2026-10-04T23:13:00.000Z
---

Thread "Build the Claude Desktop ssh plugin" (cmsg_01JbwQwHoYeBWptjPB5c6u8m3KSccv8f9KZdoYiLkxZons). Everything finished is pushed to `claude/project-thread-fx3wkp`; what GitHub lacks is in `/mnt/project-files/staging/desktop-thread/` (README there says how to apply each file).

- **beethoven-extension 15.0.0** (signed bridge installers + store upload + Mac-only release): branch at 9aa1171 with everything merged (tsc, vitest 726, chrome build, hygiene green). The staging bundle is now superseded. Running (resumed 23:12Z after a container restart): docs finish plus a whole-change review and fix in worktree wt-M. Then open the PR (no automerge; greg hand-merges).
- **hpcworker queue report**: PR #3 MERGED 21:52Z (carried the V12 contract parity commit). The hpcworker branch must restart from origin/main before new work. greg's next step: `hpcworker queue report --days 30 --limits` after the next deploy_shared.
- **VS Code `beethoven.account`** (ACCOUNT_SWITCH_CLIENTS item 2): branch at c065f25 (rebased on main cc76efd, which has #7; 85 unit tests); grid scripts 9 being added (terms back to 7); then open the VS Code PR (#8 or later). Whether the Claude Code VS Code extension honours CLAUDE_CONFIG_DIR is not yet measured.
- **beethoven-base**: design done 20:50Z (staging/beethoven-base-design-and-critiques.json); the written design is /mnt/project-files/base/DESIGN.md (being written and checked against code). Decided shape: a pinned copy of base inside each edition's source root, checked against ORIGIN with no secret (beethoven-qa model); only optional credential BASE_PROPAGATE_TOKEN in base (Environment secret, v* tags, greg reviews); RULESETS_TOKEN never for code (Administration write reaches deploy keys). Contents trimmed to really shared code (~850 lines before VS Code moves). hpcworker stays canonical with vectors. VS Code moves onto hpcworker later; the claude -p queue must not go into hpcworker.
- **VS Code grid scripts 8 hazards (verified on main 24a9896)**: `uninstall` rm -rf the real ~/.beethoven (grid/beethoven:1104: claude/, accounts/, engine/); `claude forget` deletes the sign-in; beethovend.js:176 and phone.js:40 accept an apiKeySource sign-in (hpcworker common.sh:248 refuses); `access init` and `library publish` chmod 2750 shared/ (closes hpcworker's shared copy). greg told 20:5xZ: hold the 5.0.0 build and don't run those commands. Fix = grid scripts 9, riding the VS Code PR with the account setting.

**greg's open steps for these repos:** hand-merge the three PRs above when opened (VS Code #6, hpcworker #1 #2 and extension #1 all merged by 18:13Z); copy desktop's automerge.yml, rulesets.yml, rulesets/main.json into hpcworker and beethoven-extension; build and sign VS Code 5.0.0, list it, then unpublish Ashley 3.0.0; Apple Developer Program, two Developer ID certificates, notarytool profile; Azure Artifact Signing account (identity validation, certificate profile); Google Cloud Desktop OAuth client and the store item id and publisher id; desktop laptop checks (docs/LAPTOP_CHECKS.md) and keep-or-revert of desktop PR #1; later, the base read-only token.

Related: [[beethoven-desktop]], [[signed-bridge-packages]].

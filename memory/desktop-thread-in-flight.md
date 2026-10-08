---
name: desktop-thread-in-flight
description: What the desktop thread holds at 2026-10-08 15:00Z: only beethoven-base (skeleton PR #1 merged, ruleset active, auto-merge setting pending); its hpcworker and edition work handed to the lanes outside the project
metadata:
  type: project
  modified: 2026-10-08T12:39:52.227Z
---

Thread "Build the Claude Desktop ssh plugin" (cmsg_01JbwQwHoYeBWptjPB5c6u8m3KSccv8f9KZdoYiLkxZons), branch `claude/project-thread-fx3wkp` everywhere. It was paused 2026-10-05 01:33Z to 2026-10-08 11:00Z on the seven-day usage limit.

- **Lanes (final: greg tapped "Split by repo" at 2026-10-08 14:46Z):** this project keeps beethoven-base, beethoven-sites and beethoven-qa. hpcworker, beethoven-vscode, beethoven-extension, beethoven-desktop, agents and research stay with two sessions outside the project: session_012bv6qP8y9LY4FnuSgfVq4w (branch oschome-access-approval-6prr38) and session_01Rvv9SUDARQdG2w3LefMj3K (repo-encapsulation-9hmh9f). On Oct 7 they took hpcworker main to framework 18 (meaning the grid CI deploy, b578477), VS Code main to grid scripts 10 under version 5.0.0, and every launcher repo to the hub's interface standard (INTERFACES.md v1). Those repos are not this thread's any more.
- **Handed to the hub (hand-off session, 11:08Z):** the worker race (greg 23:26Z, all queues; snapshot 9208ca2 on old main; rebuild as framework 19; worker_queues goes in the lab module); the 5.0.0 grid-test steps greg asked for at 01:17Z on Oct 5 (the draft is stale against scripts 10; redo it); the contract re-pin in the extension and desktop after the race merges.
- **beethoven-base PR #1 MERGED** by greg 2026-10-08 14:59:07Z (main 1cfc4ce): the skeleton built to the interface standard (`interface/INTERFACE.json` with exports and imports empty until step 9, the standard's `interface/pull.sh` taking imports only under `test/`, the boundary test, the export check; no vendor command, check.mjs, editions/*.json or release tags). rulesets.yml ran on the merge with the organisation's RULESETS_TOKEN, and the ruleset "main: checks before merge" (required check `gate`) is active. Still open for greg: Settings, General, Allow auto-merge (false at 15:00Z). The coordinator was told at 15:00Z; the site-module thread's U-20 (BEE-218, the site-module reader) goes on top. The branch claude/project-thread-fx3wkp is level with main.
- **Base after PR #1 (coordinator, 2026-10-08 15:20Z):** beethoven-base is the site-module thread's until its PR #2 merges (U-20 part one, head 2e64cc1: `src/profile.ts`, base's first module, in new exports desktop and browser, with four pinned test imports: hpcworker's profiles and module-schema, beethoven-sites' modules and example-modules; no vscode export yet, VS Code takes profile.ts from its 7.0.0). When this thread returns to base, design step 9 builds on that profile.ts, never a second one: add the other twelve modules beside it and the vscode export once it has modules. Keys profile.ts names that module-schema 1 lacks go into hpcworker's schema first, in the outside lanes (handover note in the hub).

Related: [[beethoven-desktop]], [[greg-contact-only-for-decisions]].

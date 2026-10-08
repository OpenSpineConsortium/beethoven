---
name: site-modules
description: greg's 23:46Z ask to move every Wayne State detail into a loadable site module: design path, Linear map, owners, beethoven-sites repo, what is built and open
metadata:
  type: project
  modified: 2026-10-08T15:28:00.000Z
---

Site-module thread (cmsg_01JbwQwHoYeBWptjPB5c6u8m1TrinioxjhHQ9P3GLbx1Xj). Design: /mnt/project-files/sites/DESIGN.md (product < site < lab < account layers; modules are data only; hpcworker composes site + lab into framework/profiles/<id>.json, which every client and the engine vendor). Linear project "U — University Site Modules": BEE-198..222.

Map: U-1..U-11 = BEE-199..209 hpcworker; U-12..U-17 = BEE-210..215 extension; U-18 BEE-216 desktop; U-19 BEE-217 VS Code; U-20 BEE-218 base; U-21 BEE-219 agents (Done); U-22 BEE-220 qa docs.

greg's decisions: U-24 BEE-222 (00:33Z) legal texts keep naming Wayne State until a second site. U-23 BEE-221 (00:59Z) the modules get their own repository: OpenSpineConsortium/beethoven-sites (branch claude/site-module-9x2ggm; auto-merge on green). Release tags are greg's.

Split of ownership: hpcworker keeps the schema, FIELD_LAYERS, SUBFIELDS, PRODUCT and the composer and publishes `profile.py module-schema`; beethoven-sites pins that schema (schema/ORIGIN, tools/pull_schema.sh) and checks modules with a stdlib checker; hpcworker pins the modules in framework/sites/ (ORIGIN by commit + sha256, pull.sh). A rule change goes to hpcworker first.

Facts a new thread needs: until BEE-208 a site has ONE lab whose profile id equals the site id (PROFILE_IS_SITE), because hpcworker and the extension find a profile by its `site` field (a second lab would inherit the first lab's restricted etc.). The product holds only the poll floor; the process cap is the site's. Python 3.6 for local tests: /root/.cache/rattler/cache/cached-envs-v0/python-63ce7dfe03a6cfbe/bin/python3.6. gh works with its configured sign-in (REST only; GraphQL is blocked).

Owners, FINAL (greg tapped "Split by repo" 2026-10-08 14:46Z): this thread holds beethoven-sites and beethoven-qa, and U-20 in beethoven-base (the desktop thread's repo) on the coordinator's go. hpcworker, extension, desktop, vscode, agents and research are greg's outside sessions' for good; every open U issue there carries a holder comment in Linear (14:50Z).

greg 00:28Z: message him only for decisions with a recommendation and alternatives ([[greg-contact-only-for-decisions]]).

Done: hpcworker PR #5 (U-1, U-3), sites PR #1; BEE-199, BEE-201 Done. On 10-07 outside sessions published hpcworker's interface/ (module-schema export) and rewrote framework/sites/pull.sh (merged commits via gh only). Hpcworker re-pin and extension U-12..U-17 handed to the hub. U-2's sites half: beethoven-sites PR #4, merged 11:19Z (examples/example/ Example University, export example-modules kept apart from modules so no example profile ships; checker refuses non-reserved hosts, measurements, shared ids). BEE-200 was closed by Linear's GitHub link when PR #4 merged; reopened 14:50Z, since its hpcworker half (and the two findings: guide's bind wording, unused cache_dir) is still open.

13:01Z: U-22 merged as beethoven-qa PR #7 (b73d4f4), BEE-220 Done; agents' and research's copies of the wording went to the hub. 15:2xZ: U-20 part one is beethoven-base PR #2 (2e64cc1, gate green): src/profile.ts, exports desktop and browser, four pinned test imports, test/compose.ts. greg merged it by hand 15:26Z (main c7682f6); base's Allow auto-merge was still off then. BEE-218 In Progress; the keys module-schema 1 lacks (match, texts...) go to hpcworker's schema first (outside lane). Base and sites checkouts fetch only main by default: add the branch refspec before setting upstream.

Related: [[desktop-thread-in-flight]].

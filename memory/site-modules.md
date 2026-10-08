---
name: site-modules
description: greg's 23:46Z ask to move every Wayne State detail into a loadable site module: design path, Linear map, owners, beethoven-sites repo, what is built and open
metadata:
  type: project
  modified: 2026-10-05T01:28:10.064Z
---

Site-module thread (cmsg_01JbwQwHoYeBWptjPB5c6u8m1TrinioxjhHQ9P3GLbx1Xj). Design: /mnt/project-files/sites/DESIGN.md (product < site < lab < account layers; modules are data only; hpcworker composes site + lab into framework/profiles/<id>.json, which every client and the engine vendor). Linear project "U — University Site Modules": BEE-198..222.

Map: U-1..U-11 = BEE-199..209 hpcworker; U-12..U-17 = BEE-210..215 extension; U-18 BEE-216 desktop; U-19 BEE-217 VS Code; U-20 BEE-218 base; U-21 BEE-219 agents (Done); U-22 BEE-220 qa docs.

greg's decisions: U-24 BEE-222 (00:33Z) legal texts keep naming Wayne State until a second site. U-23 BEE-221 (00:59Z) the modules get their own repository: OpenSpineConsortium/beethoven-sites (greg created it 01:01Z; this thread owns it; branch claude/site-module-9x2ggm; PR #1 opened 01:3xZ ready, needs greg's hand merge because it carries the kit, then auto-merge). Release tags are greg's.

Split of ownership: hpcworker keeps the schema, FIELD_LAYERS, SUBFIELDS, PRODUCT and the composer and publishes `profile.py module-schema`; beethoven-sites pins that schema (schema/ORIGIN, tools/pull_schema.sh) and checks modules with a stdlib checker; hpcworker pins the modules in framework/sites/ (ORIGIN by commit + sha256, pull.sh). A rule change goes to hpcworker first.

Facts a new thread needs: until BEE-208 a site has ONE lab whose profile id equals the site id (PROFILE_IS_SITE), because hpcworker and the extension find a profile by its `site` field (a second lab would inherit the first lab's restricted etc.). The product holds only the poll floor; the process cap is the site's. Python 3.6 for local tests: /root/.cache/rattler/cache/cached-envs-v0/python-63ce7dfe03a6cfbe/bin/python3.6 (may vanish with the container). gh works with its configured sign-in (REST only; GraphQL is blocked).

Owners (coordinator): this thread builds all hpcworker U-issues (merge the desktop thread's framework 18 in when it lands; worker_queues then needs a FIELD_LAYERS/SUBFIELDS entry, lab layer), extension U-12..U-17 (go given 00:52Z; extension main has no auto-merge; tell the coordinator before changing extension/src/core/contract.ts), others only after the coordinator's go.

greg 00:28Z: message him only for decisions with a recommendation and alternatives ([[greg-contact-only-for-decisions]]).

Related: [[desktop-thread-in-flight]].

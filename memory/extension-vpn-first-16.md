---
name: extension-vpn-first-16
description: Extension 16.0.0 to 19.0.0 merged (PRs 5-8, site PRs 4-5; 19.0.0 merged 2026-10-09 ~16:50Z as 774f0fa, site a375e6b); store upload is greg's; race client waits on hpcworker framework 19
metadata:
  type: project
  modified: 2026-10-09T15:50:46.214Z
---

greg, 2026-10-08 15:30Z (project chat): VPN-first, GlobalProtect path only, seamless access (multi-queue launch taking the first worker), a profile loader with Wayne State as default. His card **Remove** (17:52Z) removed the direct way: never reopen it.

**Merged by greg:** 16.0.0 PR 5 (fd85dac): the direct way gone whole; terms v11/privacy v12. 17.0.0 PR 6 (82ebc99): base's `browser` export pinned at extension/src/base/, carried deployments in public/deployments.json, welcome "Your grid" (Wayne first), no host-name guess; the "AccessID" word waits on a module-schema text key. 18.0.0 PR 7 + site PR 4 (main a57f44f, 02:53Z Oct 9): sign-in tab in front, kept up to 15 s for Chrome's save offer, GlobalProtect wait at once, no "OnDemand" in student words.

**19.0.0 "Beethoven signs in"** (greg's cards 2026-10-09 03:01:45Z option B and 03:02:21Z "Keep side panel"): beethoven-extension PR 8 + website PR 5, merged by this thread at greg's word ("I sent the email, now merge", 16:47Z): site a375e6b first, then extension 774f0fa. It adds webRequest + webRequestAuthProvider for one onAuthRequired listener (only Beethoven's own background dashboard GET on the granted origin, in the realm on record). Sheet: AccessID + password. An unticked Remember seals the password with AES-GCM (HKDF from a passkey's PRF) in IndexedDB 'beethoven-signin'. One wrong try, then stop. An unknown outcome, or one a box sign-in could have stood in for, is a hold (session `held` + note stopped_at), worded as a hold. Chrome's box stays as the fallback. LICENSE v12, PRIVACY v13, TERMS_VERSION 12; CLAUDE.md carries the new narrow rule. Two review rounds plus a skeptic pass; vitest 764/4 skipped, selftest 155, both builds. The design is docs/V19_DESIGN.md (PR 9).

greg's card answers (16:28Z, 16:29Z): "Add it now" put the lockout in as the fourth Known Risk inside v12 (section 8 and summary line 3; extension d5c4db1, site 595d1af). "Keep, ask C&IT" kept the Remember tick; greg sent the note to hpc@wayne.edu (16:47Z).

Outside lanes: hpcworker CLAUDE.md lines 67-76 are stale (webRequest never requested, no automated login, the 12-15 bridge); told the coordinator cse_01QcitebmTzSvkEmij8ZUdmR. Not yet measured: the listener on the live portal, side-panel WebAuthn on real Windows/macOS (Chromium 378966968), Windows Hello/Touch ID PRF for an extension RP, whether Basic failures count toward the five, which request ends first when a box sign-in races Beethoven's.

greg uploaded 19.0.0 to the store (18:44Z Oct 9); it waits on review. **Continue here:** beethoven-extension docs/V19_STATUS.md (PR 9, docs only, merged by greg 2026-10-13; extension main has since moved on through other threads' PRs 10-23, e.g. e6ee0f6 on 2026-10-22): the store and C&IT outcomes, the race handover, open items; docs/V19_DESIGN.md is the design. **Next:** the multi-queue race client after hpcworker framework 19 (snapshot 9208ca2); today's client never follows a winning job (measured on 19.0.0). **How to apply:** greg's contact rule holds (decisions only). Related: [[project-hub-export]].

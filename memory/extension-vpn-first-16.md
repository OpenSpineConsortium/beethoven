---
name: extension-vpn-first-16
description: Extension 16.0.0 (the direct ssh way removed, greg's card "Remove" 2026-10-08 17:52Z) merged as PR 5; 17.0.0 (base's reader pinned, "Your grid" picker, Wayne State first) merged as PR 6 (main 82ebc99, 21:36Z); the race client waits on hpcworker framework 19
metadata:
  type: project
  modified: 2026-10-08T21:37:36.732Z
---

greg, 2026-10-08 15:30Z (project chat, cmsg_01JbwQwHoYeBWptjPB5c6u8mDsfnkztLwXsWzkBe2Q9v76): enforce the VPN, simplify to the GlobalProtect path, the seamless-access features (multi-queue launch taking the first worker), a profile loader with Wayne State as the default. His card answer **Remove** (17:52Z, the platform's record) settled the direct way's removal: never reopen it.

**16.0.0, PR 5, merged by greg 18:56Z (main fd85dac):** the direct way of 12.0.0 to 15.0.0 removed whole (src/ssh, the bridge, helper/, the installers, nativeMessaging, the program exports, the e2e lane); LICENSE.txt v11, PRIVACY.md v12, TERMS_VERSION 11; the guides and store texts. New: a press made while the grid is out of reach waits on the GlobalProtect moment and goes ahead by itself; keep-running covers an ended run; Settings notes an old key with Forget. Still greg's: regenerate the website's terms.html/privacy.html from v11/v12 before a store build.

**17.0.0, PR 6, merged by greg 21:36Z (main 82ebc99; 52b1621 on claude/extension-vpn-first-xjhm0g, restarted from main):** beethoven-base's `browser` export (c7682f6, profile.ts) pinned at extension/src/base/ by interface/pull.sh (fourth import in INTERFACE.json); contract.ts reads through it (siteProfileFrom, sharedInstallFrom, stateDirFrom, siteFrom, profileRestricts on readProfileText/restricts; sharedRootOf, expandPath, SiteProfile re-exported); core/deployments.ts (PRESELECTED_SITE 'wayne', bundledDeployments from public/deployments.json written by sync-profiles, portalOf, deploymentOfPortal by base's deploymentFor); keys.ts lost defaultPortalFrom/siteFromHostname; a portal no carried profile declares is stored with site "" and connect types nothing. Welcome page: "Your grid" select only for two or more deployments, words from the picked profile (vpn_required false drops the VPN need; footer "Another university? Use another portal"); the "AccessID" word waits on a module-schema text key (hpcworker). Not yet measured: the live welcome page in a real Chrome profile.

**Next:** the multi-queue race client, only after hpcworker publishes framework 19 (the outside lane; snapshot 9208ca2). Linear BEE-210..215, BEE-218 carry dated comments; BEE-214 Canceled.

**How to apply:** greg's contact rule holds (a reply only for a decision; results in the status checklist; hand steps to the coordinator). Related: [[project-hub-export]].

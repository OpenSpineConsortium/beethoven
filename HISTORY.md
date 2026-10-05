# What this repository held before it became the project hub

Until 2026-10-04 `OpenSpineConsortium/beethoven` was the Beethoven launcher's single repository:
the browser extension (`extension/`), the cluster framework `hpcworker` (`framework/`), the bridge
helper, the store packages, the maintainer's tools, the documents and the agreement texts. It began
as `GregorySchwing/ashley-bridge` on 2026-09-28 (commit "Scaffold") and lived here from 2026-09-30.
Its last commit is `386b958` (2026-10-03 17:01Z, "deploy_shared --here from inside a worker's
container ...").

## Where that work is now

On 2026-10-03 it was split in two, each half keeping this history:

| Repository | What it took |
| --- | --- |
| [`OpenSpineConsortium/hpcworker`](https://github.com/OpenSpineConsortium/hpcworker) | the server half: `framework/`, `tools/`, the shared documents, the contract texts (`docs/V11_CONTRACT.md`, `docs/V12_CONTRACT.md`) and the site profiles |
| [`OpenSpineConsortium/beethoven-extension`](https://github.com/OpenSpineConsortium/beethoven-extension) | the client half: `extension/`, `helper/`, `release/`, `LICENSE.txt` and `PRIVACY.md` |

Checked on 2026-10-04 before this tree was retired: all 580 paths of `386b958` exist on the `main`
of one of the two, and `386b958` itself is hpcworker's `0c51fb6`. Nothing was left only here.

## What stays here

- The whole history, unchanged. `git log` reaches every commit; `git checkout 386b958` gives the
  last tree back.
- The tags `v4.0.0` to `v12.0.0` and their GitHub releases (the store packages and their records),
  unchanged. They name commits of the old tree.

The tree was removed by an ordinary commit on 2026-10-04, at greg's word ("the original just
Beethoven repo I don't believe is being used anymore. You can wipe it and replace it with whatever
you need to separate the existing repos"). Nothing was force-pushed and no branch or tag was deleted.

## Things that still named this repository on 2026-10-04

- `hpcworker/tools/push_org.sh` pushed `main:main --tags` here. Its owner thread was retargeting it.
  Until it is, do not run it: from an hpcworker checkout it would try to push over this hub.
- The clone lines in the READMEs of hpcworker and beethoven-extension, and beethoven-extension's
  `get-beethoven.sh` and `extension/scripts/dev-install.sh`, which the extension's 15.0.0 work
  retargets.
- The public site's `tools/build_site.py` (in `openspineconsortium.github.io`) found the agreement
  texts in a sibling checkout named `beethoven` or `ashley-bridge` holding `extension/src/licensing`
  (reported by the desktop thread, not read from here). Point `BEETHOVEN_REPO` at a
  beethoven-extension checkout before the next site build.
- A laptop's old checkout of this repository (`Desktop/ashley-bridge` or `Desktop/beethoven`): a
  `git pull` there brings this hub in and the old files go from that folder. Clone hpcworker and
  beethoven-extension for the code; keep the old folder only as history, or pull it on purpose.

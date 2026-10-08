# The repositories

Every repository of the project, what it is for, and how a change reaches its default branch.
State as of the hand-off of 2026-10-04 (`state/claude_context.md` section 3 and
`state/repos/<repository>.md`); check a repository's own GitHub before relying on a row. Each
repository's `CLAUDE.md` binds work in it. [INTERFACES.md](INTERFACES.md) is the standard every one
of them follows (since 2026-10-07): a repository reaches another only through what that one lists in
its `interface/INTERFACE.json`, as a copy pinned to a merged commit with an `ORIGIN` record, never
through a checkout of it. [SEAMS.md](SEAMS.md) lists where two of them must change together;
everything else changes in one repository alone.

## The launcher: a student's own Claude Code worker on the grid

| Repository | What it is | Default branch | How a change lands | Hand-off |
| --- | --- | --- | --- | --- |
| [hpcworker](https://github.com/OpenSpineConsortium/hpcworker) | The cluster side: the `hpcworker` framework (bash 4.2, Python 3.6), the site profiles, the contract texts the clients read, the maintainer's deploy and access tools | `main` | A pull request opened ready; greg merges by hand (no ruleset, no auto-merge; sessions may not write workflow files here). CI on ubuntu and in a CentOS 7 container; the grid lane posts its own statuses | `state/repos/hpcworker.md` |
| [beethoven-extension](https://github.com/OpenSpineConsortium/beethoven-extension) | The browser edition: the Chrome extension, its native-messaging bridge, the store packages, `LICENSE.txt` and `PRIVACY.md` | `main` | A pull request opened ready; greg merges by hand (no ruleset, no auto-merge; sessions may not write workflow files here). CI runs on a pull request | `state/repos/beethoven-extension.md` |
| [beethoven-desktop](https://github.com/OpenSpineConsortium/beethoven-desktop) | The Claude Desktop extension and Claude Code plugin: a local MCP server that reaches the worker over the student's own ssh sign-in | `main` | A pull request opened ready merges itself when its required checks pass (`automerge.yml`, ruleset 24440600) | `state/repos/beethoven-desktop.md` |
| [beethoven-vscode](https://github.com/OpenSpineConsortium/beethoven-vscode) | The licensed VS Code edition, with its CLI, MCP server and its own grid scripts | `main` | A pull request opened ready; greg merges by hand (no CI, no ruleset, auto-merge off). Edited only on greg's explicit order | `state/repos/beethoven-vscode.md` |
| [beethoven-base](https://github.com/OpenSpineConsortium/beethoven-base) | Planned: the client code the three editions share, carried by each as a pinned copy. Created 2026-10-04 with a README only; the design is `base/DESIGN.md` | `main` | Auto-merge allowed at creation; its first pull request is greg's merge by hand | `state/repos/beethoven-base.md` |

## The engine: headless Claude Code research runs as grid jobs

| Repository | What it is | Default branch | How a change lands | Hand-off |
| --- | --- | --- | --- | --- |
| [beethoven-qa](https://github.com/OpenSpineConsortium/beethoven-qa) | How code is written and proven: the definition of done, the CrossHair and Z3 gate, the pinned-copy command, the repository kit, the Claude Code plugin. Depends on nothing of ours | `main` | Merges itself on green (ruleset 24457138); release tags are greg's (a session cannot push a tag) | `state/repos/beethoven-qa.md` |
| [beethoven-agents](https://github.com/OpenSpineConsortium/beethoven-agents) | How agents run on the grid: the Apptainer image, the PreToolUse guard, accounts and `bee`, later the lease, registry, bus and reaper. Takes beethoven-qa as a pinned copy | `main` | Merges itself on green (ruleset 24460184: the gate and the image build) | `state/repos/beethoven-agents.md` |
| [beethoven-research](https://github.com/OpenSpineConsortium/beethoven-research) | What is computed and how a result is shown to be sound: REFORMS, CLAIM, the studies. Takes beethoven-qa as a pinned copy | `main` | Merges itself on green (ruleset 24440691) | `state/repos/beethoven-research.md` |

The direction of dependence is beethoven-qa, then beethoven-agents, then beethoven-research, and
never back (`plan/REPO_SPLIT.md`).

## The studies (greg's own; edited only on his explicit order)

| Repository | What it is | Branch | Hand-off |
| --- | --- | --- | --- |
| [spinesurg-ct-nnunet](https://github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet) | Spine CT segmentation and the fluoroscopic physics work; the engine's first study draws on it. Branch `L6_Class` stays private; patient data never leaves the grid | `L6_Class` | `state/repos/spinesurg-ct-nnunet.md` |
| [u251-xenograft-rat-RNASeq-study](https://github.com/Gregory-Schwing-MD-PhD/u251-xenograft-rat-RNASeq-study) | A rat xenograft RNA-seq study and its manuscript | `master` | `state/repos/u251-xenograft-rat-RNASeq-study.md` |

## This repository

[beethoven](https://github.com/OpenSpineConsortium/beethoven), the hub: no product code. Until
2026-10-04 it was the launcher's monorepo ([HISTORY.md](HISTORY.md)).

## Who works where in the Claude project

Each repository has one owning thread in the Claude project at a time; `state/THREADS.md` has the
list and `state/claude_context.md` the current owners. On 2026-10-04: the desktop thread ("Build
the Claude Desktop ssh plugin") owns beethoven-desktop, beethoven-vscode, beethoven-base, and in
hpcworker and beethoven-extension the launcher and transport work; the "Independent code-quality
gates" thread works in beethoven-qa; the hand-off thread owns `state/` and this repository.

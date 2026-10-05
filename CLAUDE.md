# Beethoven project hub — working context

This repository is the project's hub: the one clone that carries everything the Claude project
keeps outside the code, so the work can continue from any Claude account or machine. It holds no
product code; a change to a product goes to that product's repository ([REPOS.md](REPOS.md)), and
a change that crosses two of them follows [SEAMS.md](SEAMS.md). Until 2026-10-04 this repository
was the launcher's monorepo ([HISTORY.md](HISTORY.md)).

Beethoven runs Claude Code and is not an Anthropic product; "Claude" and "Claude Code" are
Anthropic's marks, used here to say what it runs; "Open OnDemand" is the mark of its publisher.

## Read first

- `state/HYDRATE.md`, then `state/claude_context.md`: how to continue, and the whole project in
  six sections. In this clone `/mnt/project-files/<folder>/` is `<folder>/` and the project
  memory `/tmp/claude/memory/team/silo/` is `memory/`.
- `plan/BUILD_PLAN.md` governs the build (180 KB: read it by section, `grep -n '^#'`).
- [REPOS.md](REPOS.md), [SEAMS.md](SEAMS.md), [linear/README.md](linear/README.md).

## Rules that are not negotiable (each repository's CLAUDE.md has them in full; they bind here)

- **No API key anywhere** (greg, 2026-10-04 13:27Z: "no api key anywhere thats the only
  fundamental rule of this software"): no Anthropic Console or API key, no `apiKeyHelper`, no
  Bedrock, Vertex or Foundry route, no gateway, no CI that runs Claude Code on a key or a token, no
  usage credits, in the products and in the maintainer's own tooling.
- **Never a Claude credential.** Nothing here reads, stores, copies, prints or relays one; never
  `setup-token`, `CLAUDE_CODE_OAUTH_TOKEN` or a `.credentials.json`.
- **No secret in any file of this repository**, nor on a command line, in a log, in the ledger, in
  Linear or in memory. `tools/scan.py` refuses the shapes it knows; it is a net, not a licence.
- **Patient data never leaves the grid.** No DICOM, no patient identifier, no PHI here, in Linear
  or in a log. The study repositories are edited only on greg's explicit order, and
  spinesurg-ct-nnunet's branch `L6_Class` stays private.
- **People's attachments stay in the project.** `uploads/` is never copied (`.hub-exclude`).
- **Nothing is deleted** outside a run's own directories and node-local temp; here, the sync never
  deletes and a file that left the project is removed only in a reviewed commit.
- **Signing never happens in a repository or in CI.** Signing identities stay on greg's machines.
- Never use the p-word (the one that starts "prov" and ends "enance") for the history of a file or
  data; say origin, source, lineage or record. Versions are integers (1.0.0).

## Who writes what

| Folder | Owner | Rule |
| --- | --- | --- |
| `state/` | the hand-off thread in the Claude project | Only it writes there while it runs; other threads send their state through the coordinator. From another account, whoever continues the work updates it |
| `plan/` | the replan thread | Others read it; a change is that thread's or greg's |
| `ledger/` | every thread | Append-only. Re-read the file just before appending a row; format in `ledger/README.md` |
| `base/`, `staging/desktop-thread/` | the desktop thread | Its design and its saved work |
| `memory/` | the coordinator | A copy of the project memory; `MEMORY.md` is the index (16 KB limit) |
| `linear/` | Linear | `ISSUES.md` and `issues.json` are a snapshot; change issues in Linear |
| `projects/<id>/` | that Claude project | Its settings, records and `sync.json` |
| everything else | this repository | `README.md`, `REPOS.md`, `SEAMS.md`, `IMPORT.md`, `LANES.md`, `HISTORY.md`, `tools/` |

## Keeping it up to date

Inside a Claude project: `python3 tools/hub.py sync --push --trailer 'Co-Authored-By: ...'` from a
clean checkout of `main` (a new account's project first runs `hub.py init --project-id <its id>`,
[IMPORT.md](IMPORT.md)). It is a three-way sync per file between the project files, the project
memory and this hub, against the record `projects/<id>/sync.json`: it scans everything it would
write, either way, and writes nothing when one file fails; it never deletes; a file changed on both
sides since the last sync is a CONFLICT left alone on both, for a person to reconcile. Specification
and rules: `tools/HUB_SPEC.md`. Until its memory-index rule is built (that file's last section),
check that no `MEMORY.md` was written into a memory folder; the coordinator owns the index.

Outside the project there is no `/mnt/project-files`: edit the files here and commit them.

## Merging

This repository has no CI and no auto-merge. A sync of the project files (`tools/hub.py`, commits
carrying the `Hub-Sync:` trailer) is pushed straight to `main`, with no pull request (greg's card
of 2026-10-05 00:13Z). Any other change, to `README.md`, `tools/`, `REPOS.md`, `SEAMS.md` or
`HISTORY.md`, goes through a pull request opened ready for review, never as a draft, and is his
merge until he says otherwise.

## How to be useful here

The failure to fear is a state that reads as plausible and is wrong. A row in `state/` is a record
of the moment its timestamp names: check it against the repository, the pull request or the
thread before acting on it, and say "not yet measured" when nothing has shown it.

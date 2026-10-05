# Moving the project to another Claude account, and back

greg, 2026-10-05 00:17Z: "make sure you are exporting all the memory, goal, instructions, name and all
metadata needed to import a project into a new Claude account and then ensure you also have the
functionality to load it back into the original account after making progress."

This page is that procedure. The home project is the one in greg's first account, project id
`chan_01JbwQwHoYeBWptjPB5c6u8m`, named "beethoven". Another account's project is called a guest
project here; it has its own id, which its threads read from their own messages.

## What travels, and how

| Part of the project | Where it is in this repository | How it reaches the other account |
| --- | --- | --- |
| Name, goal (the project's topic), instructions, repositories, context sources, model, memory switch | `projects/<id>/settings.json`, `topic.md`, `instructions.md` | The new project's Claude sets the name, repositories and connectors through one setup card greg confirms, and the instructions and model itself; greg pastes the topic and adds the Drive folders (part A; `projects/<id>/tools.md` says which tool does what) |
| Memory | `memory/` | `tools/hub.py` writes every note into the guest project's memory folder (part B) |
| Project files (the hand-off, the plan, the ledger, the designs, the staged work, every other folder) | the folders of the same names | `tools/hub.py`, both ways |
| Threads | `state/THREADS.md`, `projects/<id>/threads.json` | They do not move: a thread's conversation stays in its account. Its work is in the repositories and its state in `state/` |
| Routines | `projects/<id>/routines.json` | Recreated in the guest project with the prompt in part D (routines belong to an account) |
| Connectors | `projects/<id>/connectors.json` | greg connects them in the new account (part A); sign-ins never travel |
| Cloud environment | `projects/<id>/session.json` | greg recreates it (part A); its setup script is not readable from a session |
| Linear | `linear/` (a snapshot) | Nothing moves: both accounts connect the same workspace, `ashl3y`, team Beethoven |
| Repositories | `REPOS.md` | Nothing moves: both accounts reach the same GitHub repositories |
| People's attachments (`uploads/`) | never here | They stay in the project they were sent to |

Nothing in this repository is a credential, and nothing in these steps asks for one: no Claude,
Anthropic or API key, no token, no password (the project's one fundamental rule, `CLAUDE.md`).

## A. greg, in the new Claude account

What only greg can do (no tool does it): connect the services, create the project, and four settings
clicks. Everything else the new project's own Claude does.

1. Connectors (Settings, Connectors): Linear, signed in to the workspace `ashl3y`; Google Drive and
   Google Docs, signed in with the Google account that holds the folders in `settings.json`
   (`context_sources`); GitHub at https://claude.ai/connect-github. The Claude GitHub App is installed
   on the organisations, not on a Claude account; whether a second Claude account reaches the
   repositories without installing it again is not yet measured, and the first thread says if it
   cannot.
2. Create a new, empty project and send this as its first message:

   > Set this project up from the hub OpenSpineConsortium/beethoven. Propose the setup: the name
   > "beethoven", these repositories: OpenSpineConsortium/beethoven, OpenSpineConsortium/hpcworker,
   > OpenSpineConsortium/beethoven-extension, OpenSpineConsortium/beethoven-research,
   > OpenSpineConsortium/beethoven-desktop, OpenSpineConsortium/beethoven-vscode,
   > OpenSpineConsortium/beethoven-qa, OpenSpineConsortium/beethoven-agents,
   > OpenSpineConsortium/beethoven-base, Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet,
   > Gregory-Schwing-MD-PhD/u251-xenograft-rat-RNASeq-study, and the connectors Linear, Google Drive
   > and Google Docs. Then start a thread that follows IMPORT.md part B.

   The project's Claude posts a setup card (its `propose_project_setup`, which sets the name only
   while it is still a placeholder and the repositories only while the project has none); confirm it.
   For one account per repository, list only that repository and the hub, and say which lane
   ([LANES.md](LANES.md)).
3. Project settings, four clicks no tool can make: paste the topic from `projects/<home id>/topic.md`;
   add the three Drive folders from `settings.json` as context sources; create a Cloud environment
   with trusted network access and paste the setup script copied from the old account (Project
   settings, Cloud environment, the gear beside the environment, Setup script), with no key among its
   variables; check that memory is on.

## B. The guest project's Claude

1. The coordinator sets the instructions from `projects/<home id>/instructions.md` and the threads'
   default model from `settings.json` (`update_project_settings`; at most 32 KiB, which the text fits).
2. The thread clones the hub (attached by the setup card), on `main`, and runs
   `python3 tools/hub.py init --project-id <this project's id> --push --trailer '<the session's
   commit trailers>'`. Every folder lands in `/mnt/project-files`, every memory note in this project's
   memory folder (the one holding `.memory-sync`), and the record `projects/<id>/sync.json` is pushed.
   The coordinator then writes `MEMORY.md` with `update_memory` from `memory/MEMORY.md`, since the
   index is its own file.
3. The coordinator writes `projects/<id>/settings.json`, `topic.md`, `instructions.md` and `tools.md`
   for this project; the thread writes `threads.json`, `routines.json`, `connectors.json` and
   `session.json` beside them; then `python3 tools/hub.py sync --push`.
4. The thread creates the routine of part D (`create_trigger`).
5. Every thread reads `state/HYDRATE.md`, then the memory index, before continuing work.

## C. Back in the home account

The home project's routine runs `python3 tools/hub.py sync --push` at 00:10Z and 12:10Z; any thread can
run it at once when asked ("load the hub back"). For every file the home project has not changed since
its last sync, the guest's newer version comes in, memory notes included; a file both projects
changed is listed as CONFLICT and left as it is on both sides until a person reconciles it
(`python3 tools/hub.py diff <path>` shows the three versions); ledger rows from both are merged. Nothing
is ever deleted: a file removed on one side is listed as GONE.

## D. The routine (both accounts)

Created in the hand-off thread of each project with `create_trigger`, every 12 hours, firing into that
thread, with this prompt:

> Routine: keep OpenSpineConsortium/beethoven (the project hub) and this project in step. In the hub
> checkout on main, from a clean tree: `python3 tools/hub.py sync --push` with the commit trailers (it
> pulls what other accounts pushed and pushes this project's changes; syncs go straight to main, greg's
> card of 2026-10-05). Put each CONFLICT to greg as a decision (which version to keep, your
> recommendation from `hub.py diff`, the alternatives); send GONE and INDEX lines to the coordinator
> for its to-do notice and its `update_memory`; otherwise end the turn without a reply. Refresh
> linear/ISSUES.md only if it is more than a day old and Linear answers. Keep it light.

## E. From a plain clone, with no project

Edit the files here, commit, push. Each project's next sync takes the change in for every file that
project has not changed since; otherwise it reports a conflict.

## Memory, measured

Measured 2026-10-05: a memory note written by a script (not Claude's own Write tool) reaches the
memory service within seconds (a note written by python at 00:25:16Z had a service id in the folder's
`.memory-sync-basis` at 00:25:24Z, same sha256). But each session's copy of the memory folder is
refreshed from the service only at some events, so a copy can be stale: `tools/hub.py` never writes
the index `MEMORY.md` (the coordinator applies it with its own `update_memory`) and never pushes a
note whose bytes are an older version the hub already had.

## Still not yet measured

- Whether claude.ai itself offers a project export or import. None of the tools this project's sessions
  hold does.
- Whether a second Claude account reaches the GitHub repositories without its own install of the
  Claude GitHub App.

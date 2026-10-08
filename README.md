# Beethoven: the project hub

The one repository to clone to continue the Beethoven project from any Claude account or machine.
It holds no product code. It holds what the Claude project keeps outside the code: the hand-off
state, the build plan, the build ledger, the shared-code design, work saved before it reached a
repository, the project's shared memory, a snapshot of Linear, and the map of the repositories
and of the few places where they touch.

Beethoven runs Claude Code and is not an Anthropic product; "Claude" and "Claude Code" are
Anthropic's marks, used here to say what it runs; "Open OnDemand" is the mark of its publisher.

## Continue from another Claude account

1. Clone this repository: `git clone https://github.com/OpenSpineConsortium/beethoven`. It is
   private; the GitHub account must reach the OpenSpineConsortium organisation.
2. Start Claude Code in the clone (`claude` in the folder on a laptop, or a session at
   claude.ai/code with this repository attached). `.mcp.json` names Linear's own server: the
   first Linear call opens Linear's sign-in in the browser. No token is stored anywhere. In the
   claude.ai app, connect Linear under Settings, Connectors, instead.
3. Read `state/HYDRATE.md`, then `state/claude_context.md`, and do what HYDRATE says. Its paths
   name the project's folders; in this clone they are the folders of the same name:

   | In the project | In this clone |
   | --- | --- |
   | `/mnt/project-files/<folder>/` (every folder but `uploads/`) | `<folder>/` |
   | `/tmp/claude/memory/team/silo/` (the project memory) | `memory/` |

4. Clone the repositories the task needs ([REPOS.md](REPOS.md) lists each with its rules) and read
   its `CLAUDE.md`. [SEAMS.md](SEAMS.md) says when a change in one needs a change in another.
5. Working from a plain clone, change the files here and commit them: each project's next sync
   takes the change in for every file that project has not changed since; a file changed on both
   sides is reported as a conflict and left alone on both. Linear stays the record of issues;
   `linear/ISSUES.md` is only a snapshot.
6. To bring the claude.ai project up in another Claude account (name, goal, instructions,
   repositories, connectors, memory, files) and load its progress back into this one, follow
   [IMPORT.md](IMPORT.md). [LANES.md](LANES.md) is how several accounts work at once, each on its
   own repository.

## What is here

| Folder | What it holds | Written by |
| --- | --- | --- |
| `state/` | The hand-off: `HYDRATE.md` (how to continue), `claude_context.md` (the whole project in six sections), `DECISIONS.md`, `THREADS.md`, and one file per repository in `state/repos/` | the "Write the hand-off state file" thread |
| `plan/` | The build plan (`BUILD_PLAN.md` governs), the repository split, the Linear breakdown, the first study, the imaging runbook, the token-economy playbook, the project instructions | the replan thread, the three-repo thread |
| `ledger/` | The build ledger and the interventions log, append-only: the record behind the methods paper | every thread |
| `base/` | `DESIGN.md`, the design of beethoven-base (the code the three client editions share) | the desktop thread |
| `github/` | Proposed rulesets, the auto-merge setup and the scanning rules for the organisation's repositories | the engine skeleton thread |
| `promo/` | The first promotional text (Linear project O, Outreach and Adoption) | the replan thread |
| `staging/` | Work saved before it reached GitHub: the desktop thread's patches and git bundle, the base survey and design critiques, with a README each | the thread that saved it |
| `memory/` | The project's shared memory: `MEMORY.md` is the index, every other file one fact | the coordinator and the threads |
| `projects/` | One folder per Claude project (this one is `chan_01JbwQwHoYeBWptjPB5c6u8m`): its name, goal, instructions and settings as read from the project, its threads, routines, connectors and environment, and `sync.json`, the record of its last sync | that project's coordinator and hand-off thread |
| `sites/` | The design of the university site modules | the site-module thread |
| `linear/` | A snapshot of the Linear team Beethoven, its projects and issues, and how the project uses Linear | `linear/README.md` by hand; `ISSUES.md` by the snapshot |
| `tools/` | `hub.py` (the two-way sync; `HUB_SPEC.md` is its specification), `sync.py` (forwards to it), `scan.py` (what must not leave the project) | this repository |

[HISTORY.md](HISTORY.md) says what this repository was before (the launcher's monorepo, now split
into hpcworker and beethoven-extension) and where each part went. The old tree, its tags `v4.0.0`
to `v12.0.0` and their releases stay in its history.

## How it stays up to date

Inside a Claude project, `python3 tools/hub.py sync --push` (on `main`, from a clean tree) brings
the project files and the memory here and the hub's newer files into the project, and pushes
straight to `main` (greg's choice, 2026-10-05). It runs after every refresh of the hand-off and
twice a day on a schedule. Per file it compares both sides with the record of the last sync
(`projects/<id>/sync.json`): a side that changed is copied to the other, a file both changed is a
conflict left alone on both (`hub.py diff <path>` shows the three versions), ledger rows from both
sides are merged, and nothing is ever deleted. Before it writes anything it runs `tools/scan.py`
over every file it would write, either way, and writes nothing if one fails: no secret,
credential, patient data or unexamined binary moves this way. `.hub-exclude` names what never
moves, each with its reason (people's attachments to project messages never do).

## The rules

The rules in each repository's `CLAUDE.md` bind here too. The ones this repository touches most
are in [CLAUDE.md](CLAUDE.md): above all, no API key anywhere, never a Claude credential, no
secret in any file, and no patient data off the grid.

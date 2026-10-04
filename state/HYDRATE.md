**Describes:** 2026-10-04 21:25Z (how to read the hand-off; the state itself is in the files it names)

# Continue the Beethoven project from the hand-off

Written 2026-10-04 by the project thread "Write the hand-off state file", on greg's ask of 18:34Z
("write all state to a file I can continue in another session using the memory skills") and
18:34:48Z ("I also want repo specific hand offs"). It is the hydration prompt of the "Claude CLI
State Management" guide as `bee` builds it (beethoven-agents `docs/bee/STATE_HANDOFF.md` section 3,
`src/beethoven_agents/bee/handoff.py` `hydration_prompt`), widened from one repository to the whole
project. Another session, possibly on another account or machine, stopped and left this work to
you. Do this, in order.

## 0. Where the state is

| File | What it holds |
| --- | --- |
| `/mnt/project-files/state/claude_context.md` | the project's six-section hand-off: goal, hard rules, every repository and thread in one view, what is done, what blocks, what to do first |
| `/mnt/project-files/state/DECISIONS.md` | every decision greg made, with its UTC time and where it is recorded, and the decisions still open |
| `/mnt/project-files/state/THREADS.md` | every thread: what it owns, where it stands, work on branches with no PR and in `staging/desktop-thread/`, how threads are metered |
| `/mnt/project-files/state/repos/<repository>.md` | one six-section hand-off per repository (ten: beethoven-base, hpcworker, beethoven-extension, beethoven-research, beethoven-qa, beethoven-agents, beethoven-desktop, beethoven-vscode, spinesurg-ct-nnunet, u251-xenograft-rat-RNASeq-study) |
| `/tmp/claude/memory/team/silo/MEMORY.md` and its fact files | the project's shared memory (the "memory skills"): read with the memory tools or the file tools |

Every file carries the UTC time it describes at its top: the first line of THREADS.md,
DECISIONS.md and this file, and the **Timestamp:** line under the heading of `claude_context.md`
and each repository file. It is a record of that moment,
not a promise to stay current: where it and the world disagree, the world wins and you say so.

Outside the project (Claude Code on a laptop, a grid job): `/mnt/project-files` does not exist
there. Download the `state/` folder from the project's files, then, in the repository you work
in, `bee handoff import state/repos/<repository>.md` puts that repository's hand-off where the
`/hydrate` command and `bee continue` read it (`.claude/state/claude_context.md`, ignored by git;
`bee` replaces any secret-shaped string with `[redacted]` and checks the six sections). The
project-level file is read, not imported.

## 1. Read, cheapest first

1. **Memory.** Read the project memory index (`read_memory`, or
   `/tmp/claude/memory/team/silo/MEMORY.md`), then only the fact files a task needs
   (`multi-account-agent-teams.md`, `beethoven-desktop.md`, `three-repo-staging.md`,
   `cloud-session-credits-and-usage.md`, `no-api-key-anywhere.md` are the ones most often needed).
2. **The project hand-off**, `claude_context.md`, whole. It is short on purpose.
3. **The repository hand-off** for each repository your task touches, `repos/<repository>.md`.
4. **DECISIONS.md and THREADS.md** before you decide anything greg may already have decided, or
   start work a thread may already own.
5. **The live record**, only as needed: `fetch_project_timeline` (the coordinator's standing
   notice "Waiting on you, by thread" is greg's to-do list), `fetch_thread` on the thread that
   owns your work (newest first), `/mnt/project-files/plan/BUILD_PLAN.md` (it governs; read by
   section with `grep -n '^#'`, never whole: it is 180 KB), `/mnt/project-files/ledger/`.
   Repository `CLAUDE.md` files bind; where they and these files differ, the stricter rule wins.

## 2. Filesystem validation (critical)

Do not trust the hand-off blindly. Before you act on a row, confirm it with the narrowest check
and read only the lines you need:

- a repository's state: `git -C <checkout> fetch origin --prune --tags`, then
  `git log origin/main --oneline -3` (`origin/master` in
  u251-xenograft-rat-RNASeq-study; `origin/L6_Class` in spinesurg-ct-nnunet; neither has a main), `git ls-remote --tags origin`;
- a pull request: `gh api "repos/<owner>/<repo>/pulls?state=all&per_page=10"` (REST only; GraphQL
  is refused from these sessions, and the GitHub plugin server failed to connect in the session
  that wrote this, "Proxy refused to open a tunnel: 403 Forbidden");
- a ruleset: `gh api repos/<owner>/<repo>/rulesets`;
- a file: `ls`, `grep -n`, `sed -n 'a,bp'`;
- a thread: `fetch_thread` newest first; a session's meter: `get_session`.

## 3. Blocker verification

For each item under "Active Blockers & Errors" in the files you read, run the one command that
shows it (the tag listing, the branch listing, the session's `rate_limit_info`) and compare the
output with the recorded string, exactly. A blocker that has cleared is a step that can go ahead;
say so where greg reads it.

## 4. Memory synchronisation

If a long-term decision in `DECISIONS.md` or section 2 of a hand-off is missing from the project
memory, add it there: read the memory first, keep every line, stay under 16 KB, one fact per file.
If it is missing from a repository's `CLAUDE.md` and belongs there, the change goes through that
repository's own pull request, not a direct edit of `main`. Never write a secret into memory or
into these files.

## 5. Execute

Do the "Immediate Next Actions" of the file that matches your task, in order. Before you start
work, check `THREADS.md`: a thread that owns a repository or a plan file keeps it, and a change
there goes to its owner (the coordinator relays) unless greg reassigns it.

## 6. Then, and only then, ask

Do not ask greg for further instructions until those actions are done or you meet a blocker the
hand-off did not foresee. Never ask him for a credential or to paste one anywhere.

## Rules that bind every step (short form; the full text is in `claude_context.md` section 2)

- No API key anywhere, the only fundamental rule (greg, 2026-10-04 13:27Z), maintainer tooling
  included. No usage credits, by anyone, for anything. Everything that calls Claude runs on a
  person's own flat-rate subscription through Claude Code's own sign-in.
- Never read, store, copy, print or relay a Claude credential; never `claude auth logout`.
- Patient data stays on the grid. A human Publish click comes before any Zenodo or Hugging Face
  release. Nothing is deleted outside a run's own directories and node-local temp.
- Nothing that runs a container, a scheduler call or Claude Code runs on the login node, a laptop
  or a cloud session; it runs in a Slurm job on a compute node.
- Every unit of work appends one row to `/mnt/project-files/ledger/LEDGER.md` (re-read it just
  before appending); every human intervention goes to `ledger/INTERVENTIONS.md` when it happens.

## Refreshing these files

When you stop, refresh the hand-off for what you changed: the project file if the project's state
moved, the repository file for the repository you worked in, with a new timestamp line. Keep the
six headings and their order (`bee handoff check` validates a repository file; the project file is
checked the same way with `handoff.parse_context`). Exact error strings in section 5, never a
summary; 3 to 5 numbered steps in section 6.

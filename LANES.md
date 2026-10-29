# Several Claude accounts at once, each on its own repository

greg, 2026-10-05 00:17Z: "eventually to be able to work on each repo in parallel with each Claude
account staying on its own repo", with "linear acts as a common ledger".

This page is how that works with what exists today. A lane is one Claude account working one
repository (or a pair that [SEAMS.md](SEAMS.md) says must change together). Every lane is a Claude
project in that account, brought up from this hub with [IMPORT.md](IMPORT.md), and kept in step with
`tools/hub.py`. Lanes are greg's own accounts (decision D4, 2026-10-04): never anyone else's, and no
sign-in is ever copied between them.

## The rule

A lane changes its own repository freely. It changes nothing in another lane's repository: a change
that crosses a seam is a Linear issue for the lane that owns the canonical side ([SEAMS.md](SEAMS.md)
names it), and that lane changes first.

## Who writes what in the hub, with lanes

| Path | Written by |
| --- | --- |
| `state/repos/<repo>.md` | the lane of that repository |
| `projects/<project id>/` | that project only |
| `ledger/*.md` | every lane, appending rows only (the sync merges them) |
| `memory/` | every lane may add a note of its own (a new file named for the lane's topic); only the home project's coordinator edits `MEMORY.md`, the index |
| `state/claude_context.md`, `DECISIONS.md`, `THREADS.md`, `HYDRATE.md` | the home project's hand-off thread; a lane sends its news there through Linear or a note in its `state/repos/<repo>.md` |
| `plan/` | the home project's replan thread, or greg |
| the hub's own files (`README.md`, `tools/`, this page) | a pull request, greg's merge |

Two lanes that change the same file anyway are not lost: the sync reports a conflict and leaves both
versions alone until a person reconciles them.

## Linear, the common ledger

Every lane connects the same workspace (`ashl3y`, team Beethoven). A lane takes the issues of its
repository's projects ([linear/README.md](linear/README.md) has the table), moves them as work
lands, and names the issue key in its commits and pull requests. A lane that needs another lane's
change opens an issue in that lane's project and links it from its own.

## Lanes now (greg's choice of 2026-10-08 14:46Z)

On 2026-10-07 two Claude Code sessions outside the home project worked on the repositories, and greg
merged their pull requests: branch `claude/repo-encapsulation-9hmh9f` (hpcworker,
beethoven-extension, beethoven-desktop, beethoven-vscode, beethoven-qa, beethoven-agents,
beethoven-research and this hub) and branch `claude/oschome-access-approval-6prr38` (hpcworker and
beethoven-vscode). The home project's coordinator asked greg on a card how to split the work, and
at 14:46Z he chose "Split by repo", its recommendation:

| Repository | Worked by |
| --- | --- |
| `OpenSpineConsortium/beethoven-base` | the home project (its desktop thread) |
| `OpenSpineConsortium/beethoven-sites` | the home project (its site-module thread) |
| `OpenSpineConsortium/beethoven-qa` | the home project (its site-module thread; its code-quality thread made 4.0.0 there on 2026-10-08); the outside session also merged qa's PRs #4 and #5 on 2026-10-07 |
| `OpenSpineConsortium/beethoven-extension` | the home project (its extension thread, since 15:30Z on 2026-10-08; pending greg's word, see below); since 2026-10-11, in practice, sessions outside the home project |
| `OpenSpineConsortium/hpcworker`, `beethoven-desktop`, `beethoven-vscode`, `beethoven-agents`, `beethoven-research` | the sessions outside the home project |
| this hub | syncs and `state/` from the home project's hand-off thread; the outside session merged hub PRs #3 and #4 (`INTERFACES.md`) |

beethoven-extension came back to the home project at 15:30Z on 2026-10-08: greg asked in the
project chat for the extension's remaining work (VPN only through GlobalProtect, a simpler
interface, the launch on every queue that takes the first allocation, a profile loader with Wayne
State as the default), and the coordinator started a thread for it here, telling him that is its
default since he asked here. That one row waits on his word: he may yet say his outside session
keeps the extension.

Read on 2026-10-22: every beethoven-extension change after the home project's extension thread
finished (its last, PR #9, documents written 2026-10-09) came from sessions outside the home
project: PRs #10 to #23, 20.0.0 to 23.0.0, 2026-10-11 to 2026-10-21, each merged under greg's
account. greg has
said nothing either way on record, so the hand-off reads the row as worked outside the project,
like hpcworker ([state/HANDOVERS.md](state/HANDOVERS.md), section "Since 2026-10-09"). Since
2026-10-22 02:02Z an organization rule, "Require owner approval to merge", also covers this hub and
every repository in the table that a session can read (all but beethoven-base and beethoven-sites,
not checked): a change reaches main only through a pull request with an approving review by someone
other than its author and last pusher, or an organization admin's bypass.

A home-project thread that held unfinished work in a repository that moved outside changes nothing
there. It hands that work over in `state/HANDOVERS.md`: the branch, the commit, what is done and
what is not, and the next step. The table below stays as the target shape.

## Lanes as proposed (greg decides which accounts take which)

| Lane | Repository | Notes |
| --- | --- | --- |
| launcher server | `OpenSpineConsortium/hpcworker` | canonical side of the contract (`docs/V11_CONTRACT.md`, `V12_CONTRACT.md`) and of the site profiles |
| launcher client | `OpenSpineConsortium/beethoven-extension` | follows the contract; a contract change is the server lane's first |
| desktop | `OpenSpineConsortium/beethoven-desktop` | |
| VS Code | `OpenSpineConsortium/beethoven-vscode` | edited only on greg's order; 5.0.0 is on hold |
| base | `OpenSpineConsortium/beethoven-base` | the shared client code the editions will carry as a pinned copy |
| qa | `OpenSpineConsortium/beethoven-qa` | releases are greg's tags; consumers re-pin |
| agents | `OpenSpineConsortium/beethoven-agents` | takes qa as a pinned copy |
| research | `OpenSpineConsortium/beethoven-research` | takes agents |
| studies | `Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet`, `u251-xenograft-rat-RNASeq-study` | edited only on greg's order; patient data never leaves the grid |

The home project (this account) keeps the plan, the decisions, the memory index and the coordination,
and may also be a lane.

## The lane block

Added at the end of a lane project's instructions, after the home instructions (`projects/<home
id>/instructions.md`):

> This project is the `<lane>` lane: it works only on `<repository>` and the hub
> `OpenSpineConsortium/beethoven`. Its threads change no other repository; a change another repository
> needs is a Linear issue in that lane's project, written with the seam from SEAMS.md. Its hand-off
> thread keeps `state/repos/<repo>.md` current, appends to the ledger, and runs
> `python3 tools/hub.py sync --push` after each refresh and on its routine.

## Not yet measured

- Two lanes syncing in the same minute against the real GitHub repository (the sync's tests cover it
  against a local one).
- Whether each account's usage limits allow a lane per repository at the same time.

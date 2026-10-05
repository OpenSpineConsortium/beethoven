**Describes:** 2026-10-05 00:15Z (refreshed for the hub with `list_thread_sessions` and `fetch_thread` from 23:40Z; before that, threads read with `fetch_thread` and `list_thread_sessions`, sessions with `get_session`, 19:36-20:22Z; the desktop thread's pushes and staging folder checked 20:32-20:33Z, its thread and staging folder again at 21:12-21:18Z)

# Threads of the Beethoven project, and how they are metered

A thread is one cloud session working on one ask. Its replies, status checklist and cards are in
the project; its work lives in GitHub and `/mnt/project-files`, never only in the session. Read a thread with `fetch_thread` (newest first is enough for state);
message a running one through the coordinator (it relays with `message_thread`), never by
posting in it.

## Who owns what

| Thread (root message id) | Owns | State (times say when) |
| --- | --- | --- |
| Build the Claude Desktop ssh plugin (`cmsg_01JbwQwHoYeBWptjPB5c6u8m3KSccv8f9KZdoYiLkxZons`, session `session_01JJvrjwHWRskTjJNoW3eGVE`) | beethoven-desktop, beethoven-vscode; for the no-key sweep, the signed bridge and the store upload also hpcworker and beethoven-extension; the beethoven-base design (greg 20:04Z) | **working** on Opus 5.5 since greg's "continue with opus" (19:26Z). At 20:18Z: building the one Mac release command; fixing the review findings in the queue report and the VS Code setting; mapping what the three editions share for beethoven-base; greg created that repository at 20:25Z. At 20:27-20:31Z it pushed its work to branches with no PR and saved the rest to the staging folder (see below), attached and cloned beethoven-base. At 20:58-21:00Z it finished the base design (a checked pinned copy per edition, no read token), asked greg to hold VS Code 5.0.0 for grid-script hazards, and corrected what it had said about `RULESETS_TOKEN`; at 21:00Z it was writing the design up, re-fixing the queue report and the account setting, and adding grid scripts 9 to the account-setting PR. hpcworker PR #3 merged 21:52Z. At 23:35Z it sent the written base design with decisions D1 to D8; at 23:49Z, after greg's 23:26Z and 23:46Z asks, it is designing the all-queue launch in hpcworker, writing the native messaging analysis into the extension's docs, reviewing the whole of 15.0.0 and building grid scripts 9 (the site-module work went to its own thread) |
| Three-repo separation (`cmsg_01JbwQwHoYeBWptjPB5c6u8mTY4EBQjdtHsPXP8iwJoc9c`, `session_01Af5AU5dZXtMWjonQpSKtNR`) | beethoven-qa, beethoven-agents, beethoven-research, `plan/REPO_SPLIT.md` | **done**: research PR #4 merged by greg 19:34Z with main CI green, and greg's beethoven-qa release v1.0.0 (19:45Z) confirmed on 16415b4 at 19:47Z; Linear, the ledger and `plan/REPO_SPLIT.md` closed out. Its next research step, wiring the split check into a real study, waits on BEE-165 and BEE-181 |
| Replan the build and seed Linear (`cmsg_01JbwQwHoYeBWptjPB5c6u8m95HhoKgts7u8qPLv48SKR9`, `session_01UKfRdtryoFQbLHPV4PxCSw`) | `/mnt/project-files/plan/*.md` (BUILD_PLAN, LINEAR_BREAKDOWN, PROJECT_INSTRUCTIONS, the playbook, the spine and imaging plans), Linear team Beethoven | idle since 14:14Z (review ready). Its last work folded the three-repo split (13:34Z, PROJECT_INSTRUCTIONS version 11, BEE-193 to 197) and the no-key sweep (14:14Z) into the plan. Nothing decided after 14:13Z is in BUILD_PLAN yet. It is still set to Fable 5.1, whose weekly limit was spent at about 18:36Z, so it may stall in rate-limit retries when woken; switching its model is greg's word |
| Seamless account switching (`cmsg_01JbwQwHoYeBWptjPB5c6u8mSNgHzdyEJy3URwJtFY9rRh`) | nothing now; `bee` moved to beethoven-agents | done: research PR #3 merged 07:06Z |
| Lay down the engine repo skeleton (`cmsg_01JbwQwHoYeBWptjPB5c6u8mVwzdrSJQyPXTRRfCLMcB2J`) | nothing now | done: research PR #1 (greg, 03:29Z) and PR #2 (auto-merge, 03:44Z) |
| Map engine repos against the goal; Turn the notebook into a build roadmap; Draft the REFORMS compliance checklist (2026-10-03) | nothing | done 2026-10-03; their outputs are the roadmap Claude Doc and the REFORMS checklist Claude Doc (memory `build-roadmap-doc`, `reforms-checklist-doc`) |
| Write the hand-off state file (`cmsg_01JbwQwHoYeBWptjPB5c6u8mVhWVCDnpMjFY5GuUpJB4jy`, `session_015fmXsHBpKKjGFwwMHxU2QR`) | `/mnt/project-files/state/` and the hub, `OpenSpineConsortium/beethoven` | wrote these files; on greg's ask at 21:00Z opened beethoven-vscode PR #7 (merged 21:16Z); on his 23:26Z ask made the old monorepo the project hub (PR #1, open) and keeps it current with `tools/sync.py` |
| Independent code-quality gates (`cmsg_01JbwQwHoYeBWptjPB5c6u8mKGFJfGGY87GoSjLtzXoYao`, `cse_01SNXoctnJyZBMtgG73Rq3rx`) | the code-quality standards as independent pull-request gates, in beethoven-qa | **working** since 23:31Z |
| Wayne State as a site module (`cmsg_01JbwQwHoYeBWptjPB5c6u8m1TrinioxjhHQ9P3GLbx1Xj`, `cse_01RuS6thuXkWoYCH6Jdfya4n`) | the research, the inventory of Wayne State details across every repository, the Linear issues and the first changes; issues in other threads' repositories go through the coordinator | **working** since 23:48Z |

The coordinator (the project chat's own session; `session_01KxG54KH941Xv5z4mzbX8be` relayed at
23:31Z, so it has been replaced since `session_01Mv8T6Grq4XWJnexVBr7gCT` of 15:19Z) keeps one
standing notice of greg's to-dos, "Waiting on you, by thread"
(`cmsg_01JbwQwHoYeBWptjPB5c6u8m3HqBdB9niaNyWTpCQNBALz`), and relays between threads. A thread that
owns a file keeps it: another thread that needs a change there writes it to a new file and hands it
to the owner through the coordinator. The older threads' parent session is
`session_01HeSMnuqnfvjUKTAbQLXJsc`.

## Work on branches with no PR, and outside GitHub

Checked again at 00:05Z (`git ls-remote`, `gh api`): the desktop thread's branch
`claude/project-thread-fx3wkp` holds two pieces of work with no PR, so with no CI run:

- beethoven-extension 9aa1171 (21:23Z): 15.0.0, 21 commits on main a7db369, the five installer
  streams, the store upload step, "use another account without a sign-out", V11 identical to
  hpcworker's, and the two Mac release branches of the staging bundle merged in (`wip/mac-W`
  ab1f44f and `wip/mac-R` 63fa934 are its ancestors). The desktop thread is reviewing the whole
  change before the PR.
- beethoven-vscode c065f25 (21:33Z): the `beethoven.account` setting after a second review, with
  main merged in; grid scripts 9 is being built to ride the same PR.

hpcworker's queue report and its V12 contract patch are no longer on a branch: greg merged them as
hpcworker PR #3 at 21:52Z (main 5492d4d; `docs/V12_CONTRACT.md` is blob 75f86cb, the extension
branch's).

`/mnt/project-files/staging/desktop-thread/` (README there; saved 20:27Z) is therefore mostly on
GitHub now: the Mac bundle's branches are in 9aa1171 and the hpcworker patches in PR #3. What only
it holds: the VS Code fix patch of 20:27Z (likely superseded by c065f25, not checked), the two
findings files, the PR #3 body draft, and the base survey and first design with its critiques
(the written design is `/mnt/project-files/base/DESIGN.md`, 23:34Z). Nothing is written in
beethoven-base (only greg's README, as far as the desktop thread reported).

If the desktop thread's container is reclaimed, these files and the thread's replies are what its
successor rebuilds from; each `repos/<repository>.md` section 6 gives the steps.

The three-repo thread's slimming, held only in its checkout until 18:52Z, is now research main
8dd5be2.

## How threads are metered (measured with `get_session`, 19:37-19:40Z)

- Every thread is a Claude Code cloud session (`environment_kind: anthropic_cloud`) on greg's own
  Claude plan. Nothing in the project runs on the grid yet.
- Fable 5.1's weekly limit ran out at about 18:36Z: the sessions then on it read
  `rateLimitType: seven_day_overage_included`, `isUsingOverage: false`, reset 2026-10-08 11:00Z;
  the coordinator's last reading on Fable (18:36Z) was `status: allowed_warning` at 99 %
  utilization, and the desktop thread then sat in HTTP 429 retries (its seven-day usage-limit
  notice is at 18:38Z). greg moved the coordinator and the thread default to Opus 5.5 at
  18:40Z, the three-repo thread at 18:40Z and the desktop thread at 19:26Z. At 19:37-19:40Z the
  desktop, three-repo, coordinator and this thread all read `rateLimitType: five_hour`,
  `status: allowed`, `isUsingOverage: false`, reset 2026-10-04T23:10Z. Switching a thread's model
  is greg's word, never a thread's own choice.
- List price at 19:37-19:40Z (`usage.cost_usd`, what the API would bill, not a bill on a subscription):
  desktop thread $432.38, three-repo thread $327.98, replan thread $328.17, coordinator (since
  15:19Z) $26.30, this thread about $36.
- greg's $250 is the Claude Code **cloud-session promotion** for Max: claim at
  claude.ai/code/claim-credit or `/claim-credit` by 2026-10-07 23:59 PT; once claimed it is
  applied automatically to cloud sessions, which every thread here is, and spent before the plan's
  limits; unspent balance expires 2026-11-04; Settings > Usage shows it. Whether it is claimed is
  not visible from a session. It is **not** the paid "usage credits" (overage), which are excluded
  for the engine and its students by greg's rule. The coordinator got this wrong once (18:17Z) and
  corrected it at 18:27Z; answer from memory `cloud-session-credits-and-usage`, never guess.
- The custom default environment greg set at 16:45Z (`env_01CxLnKLA8fTAo7waT63iJyM`) reaches
  threads started after it (this thread runs in it); a running thread cannot be moved to it, and
  a local Claude Code session cannot be moved into the cloud.
- Page-read permission prompts come from a thread's permission mode, not the network policy: the
  approval option that covers the rest of a thread ends them there; Auto mode under Project
  settings > General covers threads started after the change. Every live thread here runs in auto.
- The engine's grid jobs will never be cloud sessions and draw on neither the promotion nor usage
  credits: they run on each person's own subscription inside its rolling windows (BUILD_PLAN
  section 17, Linear BEE-121).

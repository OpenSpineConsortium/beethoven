# Token economy playbook: plan input for Linear project G3

> Filed 2026-10-04 by the re-plan thread from the workflow that read greg's Drive folder "claude-artefacts"
> (plan input, not a decision record; BUILD_PLAN.md §15 and §15.6 are the plan's reading). **Superseded on
> one point:** greg decided at 2026-10-04T01:12Z that usage credits ("extra usage") are never used, a hard
> exclusion (BUILD_PLAN §2 C7), so every line below that calls extra usage "the sanctioned overflow" or
> "the student's own choice" is void; a spent window is hibernate or the hand-off of D1d. **Also corrected:**
> the ground rule below says the sign-in directory is "mounted read-only into the container"; measured in
> hpcworker it is bound read-write (the worker binds `$HOME`), Claude Code writes its own files there, and
> the protection is policy, not a mount flag (BUILD_PLAN §15.6).

Written 2026-10-04 from the two documents in the Drive folder `claude-artefacts`. This is a plan
input, not a decision record: it sorts what the two documents propose into what the engine can
adopt, what it must refuse, and what has to be measured first.

## Ground rules this file obeys

**D1, the engine's credential posture (given, not negotiable).** The research engine runs only on
each student's own flat-rate sign-in. Claude Code is started where that sign-in already is
(`claude_config_dir` from the site profile, mounted read-only into the container), `claude auth
status` is read, and nothing else: no credential is ever read, copied, exported, placed in an
environment variable or in argv. No API keys, no gateway, no `setup-token`, no
`CLAUDE_CODE_OAUTH_TOKEN`. One person, one account.

**Facts established from Anthropic's pages on 2026-10-04 (nothing below contradicts them).**

1. Task budgets are not available on Claude Code.
2. The usage-analytics dashboard is Team and Enterprise only.
3. Prompt cache lifetime is 1 hour on a subscription and 5 minutes on usage credits or an API key.
4. Claude Code 2.1.234 and later can wait for the usage-limit reset and continue
   (`autoContinueAtUsageLimit`).
5. `--max-budget-usd` caps a headless run.
6. MCP tool definitions are deferred by default.
7. A cloud session sets `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` itself.

**What was checked against the code before writing (hpcworker at commit 2e5bcf8, the copy in
this container).** The always-on chain (one `afterany` successor queued at job start, a stop file
ends it, the successor is cancelled on stop), node-local temp `/tmp/$USER/hpcworker_$SLURM_JOB_ID`
with an EXIT trap, `tmpdir_is_node_local: false` in `profiles/wayne.json`,
`login_node_rules.poll_floor_seconds: 60`, `--continue` inside `RESUME_WINDOW_S`, the credential
variables stripped with `env -u` (`ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`,
`ANTHROPIC_BASE_URL`, `CLAUDE_CODE_OAUTH_TOKEN`, the two file-descriptor variables),
`check_auth` reading `loggedIn`, `email` and `subscriptionType` from `claude auth status` and
nothing else, Slurm clients bound into the image (`hpcw_slurm_in_container`), and `probe.sbatch`
(egress matrix, `claude auth status`, the flags `remote-control` accepts). No `claude -p`, no
hook, no managed-settings file, no model or effort setting exists anywhere in `framework/`. The
`VERSION` file at 2e5bcf8 reads 15; the roadmap calls the same commit "framework 11". One of the
two is wrong; which is not established here.

## A. What each document is

1. **Beethoven build roadmap** (Google Doc, "Oct 3, 2026 · @greg"). A six-phase roadmap for turning
   hpcworker and the extension into a research engine, each phase closed by a gate "measured on the
   grid, not asserted". Its folder name (`claude-artefacts`) and byline read as an export of an
   earlier Claude artifact; the extraction does not state its origin outright, so: probably an
   export, not confirmed. Against the current BUILD_PLAN items it adds nothing new on Pixi
   (decision 4, recommended), Metaflow (decision 2, not recommended for phase 2), quota pacing
   ("queueing and backoff, not more accounts", with no numbers), REFORMS (phase 3) or the ledger
   (phase 2). What it adds beyond them: the Phase 0 probe that decides headless `claude -p` versus a
   Remote Control session steered by the outer loop; the ledger's shape (SQLite in WAL mode on
   node-local disk, checkpointed to CephFS); PreCompact and SessionStart hooks that save and
   re-inject decisions; an image-baked `managed-settings.json` and a PreToolUse guard as a second
   line behind the framework's own; three new contract files (`run.json`, `events.jsonl`,
   `reforms.json`) added to both repositories in one change; the clean-tree gate and the run-ID hash
   before `sbatch`; LaTeX macros generated from `run.json` only; Zenodo and Hugging Face drafts that
   wait for the student's Publish press; six yes/no decisions and a leave-out list. It defers
   contracts and CrossHair to after phase 4 (decision 5) and never mentions icontract, beartype or
   CLAIM.
2. **Claude Code on a Slurm + Apptainer Cluster with a Consumer Subscription: Implementation
   Playbook** (Google Doc, "Oct 3, 2026 · @greg", 81,170 characters, 1,066 lines, read whole). A
   self-contained operations manual for one person's Pro or Max subscription on a generic Slurm
   cluster: a read-only SIF, a launcher, three guardrail layers, a CLAUDE.md blueprint, a
   sole-submitter subagent and a skill, and three run patterns. Its default authentication is a
   one-year `claude setup-token` injected as `CLAUDE_CODE_OAUTH_TOKEN`, which D1 forbids (section
   B). Its value to G3 is the token-economy material: window sizing, `--max-turns`, model and effort
   defaults, `--resume` across windows, the resubmission ladder, and the managed-settings layout.

## B. Credential posture, statement by statement

Verdicts: **matches D1**, **conflicts with D1** (with the reason), or **silent** (says nothing D1
rules on). Strict reading: any `setup-token`, OAuth-token variable, API key, gateway or copying of a
credential is a conflict, whatever the document's intent.

### B.1 The Implementation Playbook

| # | Statement (quoted) | Verdict |
|---|---|---|
| 1 | "one person's subscription authenticates only that person's sessions, the Claude Code binary runs unmodified, no one else's work is routed through the account, and nothing is done to multiply or evade the plan's usage limits." | matches D1 |
| 2 | "Anthropic's own docs describe the credential this playbook uses, a one-year token from claude setup-token, as intended 'for CI pipelines, scripts, or other environments where interactive browser login isn't available'" | conflicts with D1 (setup-token is the credential) |
| 3 | "The image contains no credentials. Each user mints their own token on their own laptop and stores it under their own /scratch path with mode 0600" | conflicts with D1 (a credential is copied to the cluster and stored by our tooling) |
| 4 | "No proxy, wrapper API, or shared service sits between the user and Anthropic. The launcher is a shell script that sets paths and calls claude" | matches D1 |
| 5 | "One account per user, no account rotation, no pooled tokens. Batch jobs are sized to the plan's windows rather than run around the clock" | matches D1 |
| 6 | "Regulated data (PHI, export-controlled, GDPR special categories) stays off a consumer plan; use an API key, a Team or Enterprise seat, or a cloud-provider route for that work" | conflicts with D1 (recommends an API key as a route; the engine has no API-key route; the data rule itself is a plan-level matter, see G) |
| 7 | "The token is minted on the laptop and pasted into a 0600 file on the user's scratch; the login node writes configuration and submits jobs" | conflicts with D1 (credential copied; configuration written on the login node) |
| 8 | "%help: Run through the claude-hpc launcher. The image contains no credentials. Required at runtime: CLAUDE_CONFIG_DIR, HOME and TMPDIR bound to writable scratch paths." | silent on the credential; conflicts with D1 on one point: `claude_config_dir` is mounted read-only in the engine, the playbook needs it writable (`.credentials.json` refresh, transcripts, `settings.json`). This is the single biggest design seam, see D and G. |
| 9 | "CLAUDE_CONFIG_DIR ... settings.json, .credentials.json (0600, written by /login and every token refresh), .claude.json, projects/ transcripts, memory/, plugins/, todos/, debug/, shell-snapshots/" | silent (describes what Claude Code writes; the engine reads none of it except two boolean keys of `.claude.json`) |
| 10 | "--cleanenv strips the host environment ... and no token or proxy credential reaches the container except through the explicit --env/--env-file lines." | conflicts with D1 (the explicit `--env-file` line is the credential injection) |
| 11 | "It validates the project path, verifies egress from the node it is actually on, assembles the binds, injects the token only if one exists, and execs Apptainer." | conflicts with D1 (token injection) |
| 12 | Launcher code: `TOKEN_ARGS=(--env-file "$CLAUDE_HPC_ROOT/secrets/claude.env")` when `CLAUDE_HPC_AUTH` is `token`; "CLAUDE_HPC_AUTH=login uses /login credentials instead" | conflicts with D1 (default path injects `CLAUDE_CODE_OAUTH_TOKEN`); the `login` branch alone matches D1 in spirit |
| 13 | "Use two credentials for two jobs. A one-year token from claude setup-token ... authenticates every batch and non-interactive run ... A full /login performed once on the cluster ... authenticates interactive and Remote Control sessions" | conflicts with D1 (two credentials; one is the setup-token). The engine has one credential, the student's sign-in, for every run. |
| 14 | "CLAUDE_CODE_OAUTH_TOKEN in the environment wins over .credentials.json, so the launcher injects the token file only when CLAUDE_HPC_AUTH is token" | conflicts with D1 (the variable is the one D1 names) |
| 15 | "claude setup-token / a browser window opens for consent; the command then prints a token of the form sk-ant-oat01-... valid for one year" | conflicts with D1 (minting a setup-token; the form and the year are also unsourced, see F) |
| 16 | "The token is a bearer credential for your whole subscription. It belongs in exactly one place on the cluster, a file only you can read, and nowhere else: not in .bashrc, not in a job script, not on an sbatch --export line, not in a module file." | conflicts with D1 on the premise (there is no such file in the engine); the handling rule itself matches the secrets rule for the publication tokens of the roadmap's phase 4 |
| 17 | "Paste it through an interactive prompt on the cluster so it never lands in shell history, a command line, or a log." | conflicts with D1 (a credential is pasted, read by `read -rsp`, written to a file by our script) |
| 18 | `token-install.sh`: `read -rsp ... TOKEN; printf 'CLAUDE_CODE_OAUTH_TOKEN=%s\n' "$TOKEN" > .../secrets/claude.env; chmod 600; date -d '+1 year' > claude.env.expires;` then a one-turn verification request | conflicts with D1 (reads, stores and spends a request on a credential; also runs the container on the login node) |
| 19 | "pipe it over SSH from the laptop so it only ever exists in memory on both ends: claude setup-token \| tail -n1 \| ssh cluster 'umask 077; sed ... > /scratch/$USER/claude/secrets/claude.env'" | conflicts with D1 (relays a credential through a pipeline and over ssh) |
| 20 | "The launcher passes --env-file ... to Apptainer, which sets the variable in the container process only ... Inside Claude Code reads the variable at startup and makes every API call with it; nothing is written to disk." | conflicts with D1 (credential in an environment variable) |
| 21 | "start an interactive session without the token and complete the browser step on the laptop: CLAUDE_HPC_AUTH=login claude-hpc # inside Claude Code: /login → ... manual-code option" | matches D1 in substance (the student signs in themselves); conflicts with grid etiquette where it says "On a login node" (the engine's sitting is `hpcworker claude login` on a compute node) |
| 22 | "The result is $CLAUDE_HPC_ROOT/config/.credentials.json, mode 0600, holding an access token, a refresh token and an expiry. A running Claude Code process refreshes the access token on its own and rewrites the file, which is why config/ must be on writable scratch and never inside the image." | silent on reading (Claude Code writes its own file); conflicts with the read-only mount in D1 as a design consequence: a read-only `claude_config_dir` cannot take the refresh. How the engine reconciles this is not stated anywhere and must be settled first (G, item 1). |
| 23 | "Claude Code warns at startup from five days out ('Your login expires in N days · run /login to renew'), and renewing is another /login." | silent (Claude Code's own behaviour; unsourced, F) |
| 24 | "a headless -p run started after the access token has already expired has been reported not to refresh it (issue #50743, v2.1.114, 401 authentication_error). That is the reason batch runs use the setup token" | the conclusion conflicts with D1 (setup-token as remedy); the reported failure is the risk the engine must absorb without that remedy, by keeping a session alive in the always-on chain or by measuring whether the report still holds (F) |
| 25 | Expiry table: "claude setup-token \| 1 year \| none needed \| run claude setup-token again on the laptop, replace secrets/claude.env ... a cron reminder 30 days before" | conflicts with D1 |
| 26 | Expiry table: "/login credentials \| access token expires in hours, refreshed in place; the login itself expires on a longer horizon \| automatic while a session is running \| /login again when the startup warning appears" | matches D1 (describes the one credential the engine uses) |
| 27 | "Anthropic's documentation describes generating the token but not revoking one. If the file is exposed ... sign out of sessions from the account's security settings on claude.ai and ... contact support" | conflicts with D1 (premise: a stored token) |
| 28 | "Keep it one account. Rotating accounts or pooling several users' tokens to widen the window is the behaviour Anthropic's terms prohibit; if the workload needs more than one subscription's window, it is a workload for an API key." | first sentence matches D1; last clause conflicts with D1 (API key as the overflow). The engine's overflow is the student's own "extra usage" on the same account or waiting; never a key. |
| 29 | Managed deny rules: "Read(//scratch/**/claude/secrets/**)", "Read(//home/**)", "Read(~/.ssh/**)", "Read(**/.env)" ... and Edit deny on "//scratch/**/claude/config/**" | matches D1 in direction (the agent is kept away from secrets); the engine has no `secrets/` folder, and the missing Read deny on `config/` is a gap to close if the pattern is reused |
| 30 | Guard hook: deny "protected path" for writes under secrets, config, bin, hooks, images, site.env | matches D1 in direction (write protection on the sign-in directory) |
| 31 | Execution matrix 'Auth': Pattern 1 "token or /login"; Pattern 2 "/login (Remote Control)"; Pattern 3 "token" | Patterns 1 and 3 conflict with D1; Pattern 2 matches |
| 32 | `claude-workspace.sbatch`: "export CLAUDE_HPC_AUTH=login # Remote Control needs the /login credential, not the setup token" | matches D1 (and is what hpcworker already does) |
| 33 | `claude-workspace.sh`: `[[ -s "$CLAUDE_HPC_ROOT/config/.credentials.json" ]] \|\| { echo "no /login credential yet ..." ; exit 65; }` | conflicts with D1 (stats the credential file; the engine asks `claude auth status` instead, which hpcworker's `check_auth` already does) |
| 34 | "claude-workspace.sh refuses to submit until a /login credential exists, because Remote Control with only the setup token fails with Remote Control requires a claude.ai subscription." | conflicts with D1 on the check (file stat); the gating idea matches (hpcworker: "Waiting for your Claude sign-in") |
| 35 | `claude-batch.sh`: `[[ -s "$CLAUDE_HPC_ROOT/secrets/claude.env" ]] \|\| { echo "no setup token installed; run token-install.sh first" >&2; exit 65; }` | conflicts with D1 |
| 36 | Lifecycle: "Rotate the token \| claude setup-token on the laptop, then token-install.sh"; "Renew the /login credential \| CLAUDE_HPC_AUTH=login claude-hpc then /login when the startup warning appears" | first row conflicts with D1; second matches |
| 37 | Troubleshooting: "401 authentication_error in a batch run \| Token file missing, malformed, or expired ... In login mode after a long gap, the access token expired without a running process to refresh it: use the token for batch" | conflicts with D1 (the remedy) |
| 38 | Troubleshooting: "Remote Control requires a claude.ai subscription \| The session was started with the setup token; use CLAUDE_HPC_AUTH=login" | silent (cannot arise in the engine) |
| 39 | Version table: "claude setup-token and CLAUDE_CODE_OAUTH_TOKEN precedence \| long-standing"; "/login manual-code flow and the five-day expiry warning \| long-standing" | first conflicts with D1 as a dependency; second silent |
| 40 | User setting `cleanupPeriodDays: 14` (prunes transcripts under `config/projects/`, inside `CLAUDE_CONFIG_DIR`) | conflicts with the rule that nothing of ours deletes inside the sign-in directory, if the engine writes this setting; Claude Code's own default pruning is not ours to configure there. Also impossible under a read-only mount. |
| 41 | `settings-install.sh` writes `$CLAUDE_HPC_ROOT/config/settings.json` (inside `CLAUDE_CONFIG_DIR`) | conflicts with D1 as built (read-only mount; the engine writes nothing there). Repo-level `.claude/settings.json` and the image-baked managed file carry the same content without touching the sign-in directory. |
| 42 | HTTPS_PROXY, HTTP_PROXY, NO_PROXY, NODE_EXTRA_CA_CERTS "egress through the site proxy" | silent (a network proxy, not a credential gateway; Wayne State compute nodes have direct egress, measured 2026-09-28) |
| 43 | "Claude Code's precedence rule decides which is used" (two credentials selected by a variable) | conflicts with D1 (there is one credential and no selector) |

Count: 43 statements; 27 conflict, 10 match, 6 silent. Every conflict traces to one design choice,
the setup-token as the batch credential. Remove it and the remaining material (section 3's
managed-settings layers, section 4's CLAUDE.md, section 5's Pattern 3 shape) is usable with the
changes in C and E.

### B.2 The build roadmap (shorter: it was written against the same rules)

| # | Statement (quoted) | Verdict |
|---|---|---|
| 1 | "The inner loop runs on the student's own claude auth login in claude_config_dir. A LiteLLM proxy that rotates commercial keys to dodge rate limits is out; rate limits are handled by queueing and backoff, not by more accounts." | matches D1 |
| 2 | "setup-token or CLAUDE_CODE_OAUTH_TOKEN injected into jobs (notes 07, 08, 09): forbidden by the credential rule; the student's claude auth login is used where it sits." | matches D1 |
| 3 | "Concurrency bounded by the account's own limits (queueing and backoff, no extra accounts)" | matches D1 |
| 4 | Decision 1: "The student's own subscription login (recommended ...) or per-student commercial API keys (needed if fan-out outgrows 'ordinary, individual usage'). Pooled keys behind LiteLLM (note 06) is not an option" | conflicts with D1 (keeps per-student API keys as a live option; D1 has no key route). G proposes closing the decision. |
| 5 | "record the credential source the run reports and the 5-hour limit behaviour" | silent on method; matches D1 only if "the credential source" is taken from the run's own output (as `claude auth status` is), never from a file or a variable. Must be written that way (G). |
| 6 | "A headless run completes from a batch job on the subscription login, or the fallback is chosen (decision 1)" | matches D1 (the fallback is a Remote Control session, not a key) |
| 7 | "publication tokens as mode-0600 files, never in argv" (Zenodo, Hugging Face) | silent on Claude credentials; matches the general secrets rule; owner, location and writer not stated |
| 8 | "transcripts and SQLite go there [node-local /tmp] and are copied back at checkpoints" | conflicts with D1 as built: Claude Code's transcripts live under `claude_config_dir`, which is read-only to the engine and must not be moved or copied by our software. Only the engine's own ledger may be staged node-locally. (G) |

## C. Token-economy configuration

Scope values: managed settings, repo settings, user settings, env var, CLI flag, hook, Slurm
script, Apptainer. "Who applies it": **skeleton thread** (repo-level config in beethoven-research:
managed settings, hooks, cache TTLs) or **plan owner** (plan-level rules, Slurm and orchestrator
behaviour, student-facing policy). "Source" is what the document itself cites; "unsourced" means
it cites nothing, whatever may exist. Rows marked (est.) come from the established facts, not from
either document. Nothing in this table may be written into `claude_config_dir`: repo-level files
and the image carry it.

| Setting | Value | Scope | Purpose | Who applies it | Source the doc gives |
|---|---|---|---|---|---|
| `model` | `sonnet` for implementation runs; Opus-class reserved for plan mode | repo settings (playbook put it in user settings) | Cheaper default per turn; "reserve Opus-class models for plan mode, where turns are few and reasoning matters" | skeleton thread (the default); plan owner (when a stage may use Opus) | Usage limit best practices (support.claude.com) |
| `env.CLAUDE_CODE_EFFORT_LEVEL` | `medium` | repo settings (env block) | "Medium effort for implementation runs to conserve the window" | skeleton thread | unsourced |
| `--max-turns` | 150 default in the batch template; 60 to 80 for test-heavy implementation; 1 for a verification turn; 3 for a Slurm preflight | CLI flag | Bound the number of model calls per window | plan owner | CLI reference; Headless mode |
| `--max-budget-usd` (est.) | not stated in either document; value to set per stage | CLI flag | Caps a headless run; the only hard cost cap available on Claude Code (task budgets are not) | plan owner | Anthropic's pages, 2026-10-04 (established); absent from both documents |
| `autoContinueAtUsageLimit` (est.) | on, in Claude Code 2.1.234 or later | repo settings (exact key placement to confirm on the settings page) | Wait for the usage-limit reset inside the job instead of exiting and resubmitting; the playbook does not know this feature | skeleton thread (the setting); plan owner (how it interacts with the wall time, see D) | Anthropic's pages, 2026-10-04 (established) |
| `--session-id` then `--resume` | `--session-id "$(uuidgen)"` on the first window, `--resume "$(cat $RUN/session_id)"` after | CLI flag | One transcript across job windows so the agent "re-enters with its own context (compacted as needed) rather than re-reading the repository from scratch" | plan owner | Headless mode; CLI reference |
| `--output-format stream-json --verbose` | stdout to `events-$SLURM_JOB_ID.jsonl`; last `type == result` event read for `subtype`, `is_error`, `result`, `num_turns`, `session_id` | CLI flag | Machine-readable outcome, turn count per window, and the usage-limit text (D) | plan owner (the orchestrator parses it); skeleton thread (the contract file `events.jsonl`) | Headless mode |
| `--permission-mode dontAsk` | on every headless run | CLI flag | "any action outside the allow list a denial the model can see and route around"; avoids turns lost to prompts nobody answers | plan owner | Headless mode; CLI reference |
| `--append-system-prompt` | "Non-interactive run $CLAUDE_RUN_ID with a hard time budget of N minutes. Nobody will answer questions ... Keep $RUN/STATUS.md current ... On an interrupt, finish the current edit, update STATUS.md, and stop." | CLI flag | Tell the agent the budget and the no-human condition so it does not spend turns asking | plan owner | unsourced |
| `env.MAX_MCP_OUTPUT_TOKENS` | 25000 | managed settings | Truncate MCP output before it fills the context | skeleton thread | Tools reference |
| `env.MCP_TIMEOUT`, `env.MCP_TOOL_TIMEOUT` | 30000, 600000 (ms) | managed settings | Server start and tool-call ceilings; a hung tool costs wall time, not tokens, but ends the window early | skeleton thread | Tools reference |
| `env.BASH_DEFAULT_TIMEOUT_MS`, `env.BASH_MAX_TIMEOUT_MS` | 600000, 1800000 | managed settings | Per-command timeout; bounds what one turn can wait on | skeleton thread | Tools reference |
| MCP tool definitions (est.) | deferred by default; nothing to set | managed settings (note only) | Tool definitions do not load into the context until needed; the playbook's "a skill loads on demand ... costs no context until needed" is the same economy for skills | skeleton thread (note in the skeleton's README) | Anthropic's pages, 2026-10-04 (established) |
| Prompt cache lifetime (est.) | 1 hour on a subscription; 5 minutes on usage credits or an API key; not configurable by us as far as either document shows | n/a (fact that shapes the orchestrator) | A successor or retry that starts within an hour of the last turn may hit the cache; one that waits five hours does not. The roadmap lists `promptCacheTtl` as unchecked; the established fact settles the number and leaves open whether a setting exists | skeleton thread (cache TTLs, if a setting is found); plan owner (scheduling retries inside the hour where possible) | roadmap: unsourced; the figures: Anthropic's pages, 2026-10-04 |
| `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` (est.) | not stated for the grid; a cloud session sets it itself | env var | Compaction threshold; whether the grid job should set one is a measurement (F), not a default | plan owner, after measurement | Anthropic's pages, 2026-10-04 |
| PreCompact hook | not stated | hook | "save decisions before compaction" so a run that crosses one compaction "finishes with the same decisions on record" | skeleton thread | unsourced (roadmap) |
| SessionStart hook | not stated | hook | Re-inject the saved decisions when the successor's session starts; replaces copying transcripts | skeleton thread | unsourced (roadmap) |
| PreToolUse guard (`claude-guard.sh`) | matcher Bash or PowerShell, and Edit or Write or NotebookEdit; `type: command`, timeout 10; exit 2 blocks with the reason to the model | hook (registered from managed settings) | A second line behind the framework's own guard; also stops turns being spent on commands that would be refused anyway | skeleton thread | unsourced (the hooks page is in neither document's sources) |
| `managed-settings.json` location | `/etc/claude-code/managed-settings.json`, 0644, baked into the image | managed settings, delivered by Apptainer | Deny rules, timeouts, hook registration the agent cannot override | skeleton thread writes the file; the image is the lab's shared thing (server side) and the lab lead bakes it | Claude Code settings page (playbook); roadmap: unsourced |
| `permissions.disableBypassPermissionsMode` | `disable` | managed settings | No bypass mode in a job nobody watches | skeleton thread | Claude Code settings; Permissions |
| `CLAUDE_CODE_DISABLE_ARTIFACT` | 1 in batch | env var | No artifacts from a headless run | skeleton thread | artifacts page (code.claude.com); version 2.1.183 asserted |
| `CLAUDE_HPC_MODE` | `batch` in headless runs | env var | CLAUDE.md branches on it: "there is no one to ask; record choices in runs/$CLAUDE_RUN_ID/STATUS.md" | plan owner (the rule); skeleton thread (the CLAUDE.md text) | unsourced |
| Window budget | wall time 4:30:00; `BUDGET = (SLURM_JOB_END_TIME - now) - 900`; exit 75 when under 600 s; `timeout --signal=INT --kill-after=120 $BUDGET`; `--signal=B:USR1@600` | Slurm script | One job of about four hours per five-hour window; the agent is interrupted, writes STATUS.md and stops before Slurm kills it | plan owner | unsourced |
| Resubmission ladder | DONE in result: exit 0. Usage-limit text: `sbatch --begin=now+5hours`. rc 124, `error_max_turns`, or success without DONE: `sbatch --begin=now+2minutes`. Anything else: stop. | Slurm script | "a scheduled retry after the five-hour window instead of a tight loop that burns the next window too" | plan owner | unsourced |
| `CLAUDE_MAX_CONTINUATIONS` | 6 | Slurm script | Cap on resubmitted windows per run | plan owner | unsourced |
| `windows.log` | turns per window, appended by the job | Slurm script (ledger file) | The engine's own usage record; the only one available, since usage analytics is Team and Enterprise only | plan owner (format); skeleton thread (add to the contract) | unsourced |
| Monitoring rules in CLAUDE.md | `squeue --me ...` at most once a minute, never in a tight loop; `sbatch --wait` in a background command for jobs under 20 minutes; read the last 50 lines of a log; `sacct -j <id> -o State,ExitCode`; never resubmit an unchanged failing script more than once | repo settings (CLAUDE.md) | Polling etiquette and context economy: "an agent loop that re-reads a large log every iteration drains the window far faster than a chat does" | skeleton thread (text); plan owner (the 60 s floor is the product's own rule, and the text must say "at most once a minute" for the agent too) | memory page for CLAUDE.md; the rules themselves unsourced |
| `slurm-operator` subagent | tools Bash, Read, Glob, Grep; `model: sonnet`; `maxTurns: 40`; refuses scripts without `--time`, `--mem`, `--cpus-per-task`, `--output`, `--job-name` | repo settings (`.claude/agents/`) | One place where submission rules apply; its own turn cap bounds the fan-out cost | skeleton thread | Subagents page |
| `slurm-submit` skill | `.claude/skills/slurm-submit/SKILL.md` plus `jobs/_template.sbatch` | repo settings (skill) | The agent never writes an sbatch header from memory; "costs no context until a job script is being written" | skeleton thread | Skills page |
| Subagent fan-out in batch | avoid; "each subagent is its own context window" | plan rule | Fan-out multiplies draw on one account's window | plan owner | unsourced |
| Concurrency | "bounded by the account's own limits (queueing and backoff, no extra accounts)"; no number stated | plan rule (orchestrator) | Several runs and projects on one subscription | plan owner | unsourced (roadmap) |
| Overflow | "extra usage" credits on the same account "is the sanctioned overflow path" | student-facing policy | Void since C7 (2026-10-04T01:12Z): usage credits are never used; no overflow exists, a spent window hibernates or hands off (§17). Consequence the playbook does not draw: on usage credits the prompt cache lifetime is 5 minutes, so overflow turns are dearer per turn as well as paid | plan owner | support.claude.com (playbook); the 5-minute figure: Anthropic's pages, 2026-10-04 |
| `DISABLE_TELEMETRY`, `DISABLE_ERROR_REPORTING` | 1, 1 | repo settings (env block) | not stated by the playbook. Note for D: these switch off Anthropic's own telemetry; the OpenTelemetry export lead is a different lever and must be checked on the monitoring page before either is set | skeleton thread | unsourced |
| `cleanupPeriodDays` | 14 | user settings (playbook) | Prune transcripts in `CLAUDE_CONFIG_DIR/projects/`. **Not adopted**: it deletes inside the sign-in directory and cannot run on a read-only mount | nobody; listed so it is not copied by accident | Claude Code settings |
| `askUserQuestionTimeout` | `10m` | user settings (playbook); would be repo settings here | A question in an unattended session closes itself; saves a window from hanging on a prompt | skeleton thread, after F confirms the key exists | unsourced ("current" in the version table, no page) |
| Phase 0 probe | `claude -p --output-format stream-json` in the shared image, on the student's own sign-in, under `sbatch`, no pty; record what the run reports about its credential source (from its own output only) and the limit behaviour | Slurm script | Decide headless `-p` versus Remote Control steered by the outer loop before anything else in G3 is built | plan owner | unsourced (roadmap) |
| Unchecked by the roadmap, not proposed | "the ultracode effort level, the subagent cap variables, promptCacheTtl, the compaction bug workaround and --forward-subagent-text" | n/a | Listed for F only | nobody until measured | roadmap says unchecked |

## D. Quota-window handling

### D.1 What the two documents propose

The roadmap: measure "the 5-hour limit behaviour" in Phase 0; "rate limits are handled by
queueing and backoff, not by more accounts"; Phase 2 goal "Runs survive wall times, rate-limit
windows and node changes", but the Phase 2 gate tests two wall-time boundaries and one compaction
and no window crossing. Not stated: how a hit is detected, the backoff schedule, whether the
chained job sleeps or exits, how remaining quota is read, or where "5-hour" comes from.

The playbook: a rolling five-hour window plus weekly caps (all models, and Opus-class) "introduced
in August 2025"; `/usage` shows both and their reset times; size one job of about four hours per
window; on a limit hit, match the result or stderr against `usage limit|rate limit|limit
reached|try again (at|in)` and `sbatch --begin=now+5hours`; on a window that ended without DONE,
`--begin=now+2minutes`; continuation cap 6; `--resume` the same session; `windows.log` with turns
per window; "extra usage" credits as the sanctioned overflow. Internal inconsistency: the prose
promises `--begin=now+<minutes-to-reset>`, the code uses a fixed five hours and parses no reset
time; a weekly-cap hit is not told apart from a five-hour hit, so six continuations of five hours
each would spend thirty hours of scheduler time against a weekly wall. The Remote Control pattern
has no window handling at all.

### D.2 Against the five live leads

| Lead | Roadmap | Playbook | What the engine should do |
|---|---|---|---|
| `/usage` plan bars (five-hour and weekly, with reset times) | not mentioned | "Check limits: /usage in an interactive session" only | A headless run cannot type `/usage`. Whether the bars are reachable from a `-p` run, from stream-json, or only interactively is not yet measured (F). Until it is, the engine's own `windows.log` is the usage record. |
| Wait for the reset and continue (`autoContinueAtUsageLimit`, 2.1.234 and later) | not known to the document | not known to the document; it exits and resubmits five hours later | Prefer waiting inside the job when the reset falls inside the remaining wall time, because the session, its context and (within the hour) its prompt cache stay warm. When the reset falls outside the wall time, end the window cleanly and let the successor `--begin` at the reset time. Whether the wait works under `sbatch` without a pty, and what it does at the wall time, is not yet measured (F). |
| `--max-budget-usd` | not mentioned | not mentioned (uses `--max-turns` only) | Set both: `--max-turns` bounds calls, `--max-budget-usd` bounds spend-equivalent. What the figure means on a subscription sign-in (whether it counts at list price, and whether it stops the run or only warns) is not yet measured (F). |
| OpenTelemetry export | not mentioned | not mentioned; sets `DISABLE_TELEMETRY=1`, which is a different switch | The only per-run token count that does not need the Team dashboard. Export to a local file or the job's stdout, never to a network sink (compute-node egress to `statsig.anthropic.com` has no DNS record, measured 2026-09-28, and nothing of ours phones home). Variable names and whether it works on a subscription sign-in: check the monitoring page, then measure (F). The skeleton thread owns the settings; the plan owner decides what `windows.log` keeps. |
| Reset time in the limit message | not mentioned | greps for `try again (at\|in)` but never reads the time; fixed `+5hours` | Parse the reset time from the result event and schedule `--begin` at reset plus a margin; fall back to the fixed five hours only when no time is found. Record the raw message text in Phase 0 so the parser is written against a real line, not a guess (F). |

### D.3 Against the two withdrawn leads

| Withdrawn lead | Roadmap | Playbook | Note |
|---|---|---|---|
| Task budgets | not proposed | not proposed | Correct by omission on both sides. `--max-budget-usd` is the cap that exists. |
| Usage analytics dashboard | not proposed | not proposed; `windows.log` is its substitute | Correct by omission. The engine's record is its own ledger (turns per window from the result event, token counts from OpenTelemetry if measured to work). No text may claim the engine reads Anthropic's usage figures. |

### D.4 Rules the plan owner can write now

1. One job per window, sized under the wall time with a margin, as the playbook does; the numbers
   (4 h in 4:30:00, 15 min margin, 10 min floor) are the playbook's and unsourced; keep them as
   defaults to be tuned by `windows.log`, not as facts.
2. A limit hit is a scheduled retry, never a loop; the retry time comes from the message when it
   can, from the wait-and-continue setting when the wall time allows, and from a fixed five hours
   only as the last fallback.
3. Tell a weekly-cap hit from a five-hour hit before scheduling anything; how is not yet measured.
4. Never a key, never a proxy that pools, never usage credits (greg, 2026-10-04T01:12Z: a hard
   exclusion, BUILD_PLAN §2 C7; 13:27Z: "no api key anywhere thats the only fundamental rule of this
   software"); several of the student's own accounts may run, one lease at a time (BUILD_PLAN §17); a
   spent window is hibernate or the hand-off, there is no overflow. (This rule first read "overflow is
   the student's own extra usage"; void, rewritten 2026-10-04T14:1xZ.)
5. Every window appends one line to `windows.log`: job id, start, end, `num_turns`, `subtype`,
   `is_error`, the limit text if any, and the token counts if the export works.

## E. Slurm and Apptainer patterns

"Already" means present in hpcworker at 2e5bcf8 and checked in the code for this file; "already,
differently" means the same need is met another way; "new" means not in hpcworker.

| Pattern | Proposed by | Status in hpcworker |
|---|---|---|
| Always-on job with one `afterany` successor, stop file, successor cancelled on stop | roadmap (outer orchestrator "on the worker's afterany pattern") | already (`worker.sbatch.tpl` section 4; the successor is queued at job start, not shortly before the wall time, so there is no lead-time computation to port) |
| `--continue` in the same directory when the previous session is young | roadmap | already (`resume_wanted`, `RESUME_WINDOW_S`) |
| Node-local temp `/tmp/$USER/...` with a cleanup trap; never trust `$TMPDIR` at Wayne State | both | already (`HPCW_NODE_TMP`, `hpcw_rm_own_tmp`, `tmpdir_is_node_local: false`). The playbook's `TMP_HOST="${SLURM_TMPDIR:-${TMPDIR:-...}}"` and `${SLURM_TMPDIR:-/tmp}/claude-$SLURM_JOB_ID.sock` trust `$TMPDIR` and bare `/tmp` and must not be copied. |
| 60 s polling floor from clients; progress through files the job writes | both | already (`poll_floor_seconds: 60`, `status_refresh` floor, `status.json` heartbeat) |
| One `sbatch`, `squeue` or `scancel` per action; nothing else on the login node | roadmap | already. The playbook's `site-discover.sh` (`sacctmgr`, two `sinfo`, `curl`), `slurm-binds.sh` (`scontrol show config`, `ldd`), `token-install.sh` and `claude-hpc` on the login node all break it and are not adopted. |
| No python on the login node | roadmap (stdlib checker; run location not stated) | already as a rule (task-given); the roadmap's clean-tree gate and run-ID hash "before sbatch" need a stated run location, see G |
| Credential variables stripped from the worker's environment | both (playbook via `--cleanenv`) | already, differently (`CLEAN_ENV` with `env -u` of the named variables; whether the image is also run with `--cleanenv --containall --no-home` was not re-checked here) |
| Sign-in checked with `claude auth status`, never a file | roadmap | already (`check_auth`: `loggedIn`, `email`, `subscriptionType`). The playbook's `[[ -s .credentials.json ]]` is replaced by this. |
| Slurm client passthrough into the container (binaries, slurm libs, munge socket, `/etc/slurm`) | playbook (`slurm-binds.sh`) | already (`hpcw_slurm_in_container`: `/usr/bin` to `/opt/host/bin`, `/usr/lib64/slurm`, `libmunge.so.2`, `/etc/slurm`, munge socket, passwd and group). The grid CI's `grid/slurm-in-container` status measures it. |
| File-queue submit shim when the munge socket cannot be bound | playbook | new; not needed at Wayne State (the socket binds; measured by grid CI). Keep as a fallback note for a second site. |
| `claude remote-control` under a pseudo-terminal (tmux or `script`), transcript in `rc.log` | playbook Pattern 2 (tmux, USR1 then C-c and `/exit`) | already, differently (`start_rc`, `rc_stop`: Ctrl-C first so Remote Control deregisters) |
| Probe job on a compute node | roadmap Phase 0 (`claude -p`, credential source as reported, limit behaviour) | already, partly (`probe.sbatch`: node temp, egress matrix, `claude auth status`, `remote-control` flags, tmux). The `-p` run and the limit behaviour are new and belong in a second probe or an extension of this one, within its ten-minute wall time budget. |
| Headless `claude -p` run template (`run.sbatch.tpl`) with per-run directory, wall time, node-local scratch | both | new |
| Window budget from `SLURM_JOB_END_TIME` or `squeue %L`, `timeout --signal=INT --kill-after`, `--signal=B:USR1@600` | playbook | new |
| Self-resubmission with `--begin`, continuation cap, DONE marker | playbook | new; and it must use `adapter_submit_after` or a plain `sbatch` through the adapter, never `--export=ALL` (the playbook's resubmit exports the whole environment, which the secrets rule forbids as a habit even when no secret is present) |
| Image-baked `managed-settings.json` at `/etc/claude-code/` | both | new; the image is the lab's shared thing, built by `build_image.sbatch` on a compute node, so the file enters through that build, not through the extension or the student |
| PreToolUse guard hook in the image | both | new |
| PreCompact and SessionStart hooks | roadmap | new |
| Repo-level `.claude/settings.json` (model, effort, allow and ask lists, `additionalDirectories`) | playbook (as user settings in `CLAUDE_CONFIG_DIR`) | new, and relocated: repo-level, never in the sign-in directory |
| CLAUDE.md blueprint with the login-node rule, job limits, sizing, monitoring etiquette | playbook | new (the skeleton thread's text; the 60 s floor and "one action per call" wording must come from the product's own etiquette, attributed as the house rules require) |
| `slurm-operator` subagent and `slurm-submit` skill | playbook | new |
| SQLite ledger in WAL mode on node-local disk, checkpointed to CephFS | roadmap | new (the engine's own file; transcripts are not moved, see B.2 row 8) |
| `run.json`, `events.jsonl`, `reforms.json` as contract files | roadmap | new; each goes into `docs/V11_CONTRACT.md` (or its successor) and `contract.ts` in the same change |
| Child `sbatch` for CPU prep and GPU training through the eight-call adapter | roadmap | new use of an existing adapter |
| Clean-tree gate and run-ID hash before dispatch | roadmap | new; run location to be stated (inside the orchestrator job, not on the login node) |
| `srun --pty` interactive allocation (Pattern 1) | playbook | new and out of the product's path (students reach the grid through the portal and the panel; a terminal pattern is a maintainer's tool at most) |
| Read-only SIF from `rockylinux:9` with `claude.ai/install.sh`, `DISABLE_AUTOUPDATER=1`, `apptainer build --fakeroot` on a laptop | playbook | already, differently (the shared image `claude-node22`, built on the grid by `build_image.sbatch`; `DISABLE_AUTOUPDATER=1` is passed in the worker's environment). Whether the base and the install method match was not re-checked. |
| `--nv` when a GPU is present; host CA bundle bound with `NODE_EXTRA_CA_CERTS`; HTTPS proxy variables | playbook | new; not needed at Wayne State (direct egress measured); keep for a second site profile |
| `CLAUDE_CODE_TOOL_MEMORY_LIMIT=16G` | playbook | new; whether a cgroup can be created inside unprivileged Apptainer is not yet measured |
| Sandbox off (`sandbox.enabled: false`) because bubblewrap cannot nest in unprivileged Apptainer | playbook | new; the claim is the playbook's inference |
| Pixi lockfiles inside the research image | roadmap decision 4 | new (research image, not the Claude Code image) |
| Metaflow with metaflow-slurm | roadmap decision 2 (not recommended) | new; not recommended by the roadmap for phase 2 |

## F. Claims about Claude Code made without a source, as one-line experiments

Each line is one measurement on the grid, inside a job on a compute node, on the student's own
sign-in, reading only the run's own output and `claude auth status`. Record the raw line, the
Claude Code version (`claude --version` inside the image) and the job id with every result.

1. Headless on a subscription: submit `claude -p 'Reply with exactly: OK' --max-turns 1 --output-format stream-json` under `sbatch` with no pty in the shared image; record exit code, the result event and what the output says about how it is signed in.
2. Five-hour window: run a `-p` job that deliberately spends turns until the limit; record the exact `is_error` result text, the exit code, whether a reset time appears in the text, and the time it appeared.
3. Weekly cap: when a weekly-cap message is ever seen, record its text beside the five-hour one; until then, state "not yet measured".
4. Wait and continue: with `autoContinueAtUsageLimit` on, repeat experiment 2 and record whether the run pauses and resumes, how it reports the wait in stream-json, and what happens when the wall time arrives mid-wait.
5. `--max-budget-usd`: run with a small cap on the subscription sign-in; record whether the run stops, the result `subtype`, and what the reported figure counts.
6. OpenTelemetry export: with the monitoring page's variables set to a local exporter, run one short `-p` turn; record whether token counts appear and where.
7. Managed settings in the image: bake a `/etc/claude-code/managed-settings.json` with one deny rule into a test image; run `-p` with a prompt that triggers it; record whether the deny is honoured.
8. PreToolUse hook: register `claude-guard.sh` from the managed file; have the run attempt a blocked command; record whether exit 2 blocks and whether the reason reaches the model (visible in the next assistant turn).
9. PreCompact and SessionStart hooks: register both with a one-line writer each; run until a compaction; record whether each fires, with what payload, and whether a `--resume` in a successor job sees the SessionStart injection.
10. `--resume` across jobs: start with `--session-id`, end the job, `--resume` in a successor on another node with the same read-only `claude_config_dir`; record whether the session resumes and whether the transcript write fails on the read-only mount.
11. Access-token refresh in headless mode (issue #50743 as reported): leave the sign-in idle past the access-token lifetime (not stated how long; `claude auth status` tells when it is no longer signed in), then run `-p`; record 401 or success. Never read the credential file to find the expiry.
12. Stream-json contents: record the full set of event types and the result event's fields (`subtype`, `is_error`, `num_turns`, `session_id`, any cost or usage field) from one real run, before any parser is written.
13. Open-in-Claude for a `-p` run: record whether a headless run registers anything in claude.ai; expected no, since only Remote Control sessions are known to register an environment URL.
14. 429 and 529 retry: not directly provokable; record from experiment 2's event stream whether retries appear and with what delays.
15. `CLAUDE_CODE_EFFORT_LEVEL` and `model` from a repo-level `.claude/settings.json`: run one turn and record which model and effort the result event or the run's banner reports.
16. The "ultracode" effort level, the subagent cap variables, `--forward-subagent-text`, the compaction bug workaround (roadmap's list): for each, `claude --help` and the settings page first; measure only what is documented to exist.
17. `promptCacheTtl`: settled by the established 1 hour and 5 minutes; measure only whether two `-p` turns 50 minutes apart in the same session report a cache hit (if a usage field exists, experiment 12).
18. `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` on the grid: run with and without a value; record when compaction fires in each case.
19. `askUserQuestionTimeout`: set `10m` in repo settings, run interactively under a pty with a prompt that asks a question; record whether it closes itself.
20. `CLAUDE_CODE_TOOL_MEMORY_LIMIT`: set 16G inside unprivileged Apptainer; run a command that allocates more; record whether it is capped or "silently uncapped".
21. `BASH_MAX_TIMEOUT_MS` behaviour "backgrounded, never left hanging": run a `sleep` past the limit; record what the tool result says.
22. Sandbox nesting: set `sandbox.enabled: true` with `enableWeakerNestedSandbox` in a test image; record the startup warning and whether commands run.
23. Permission rule semantics: with a `Read` deny on a path, attempt `Edit` and `Write` there; with `Bash(pytest*)` allowed, run `timeout 600 pytest -q`; record what is allowed.
24. `CLAUDE_PROJECT_DIR` in hook environment: have the guard print its environment keys (never values) to a file; record whether the variable is present.
25. CLAUDE.md in subagents: have `slurm-operator` quote one CLAUDE.md rule; record whether it can.
26. Monitor watch limits ("30 minutes maximum, 10 in -p runs"): start eleven watches in a `-p` run; record the eleventh's refusal text, if any.
27. Login expiry warning ("five days out"): record the exact startup line when it ever appears; until then "not yet measured".
28. `cleanupPeriodDays`: not to be measured; it is not adopted (deletes inside the sign-in directory).
29. setup-token form, lifetime and capability limits; "Remote Control requires a claude.ai subscription" text: not to be measured; excluded by D1.
30. Phase 0's "credential source the run reports": record exactly which line of the run's own output names it; if no line does, the probe records "not reported" and `claude auth status` stays the only source.

## G. Proposed edits

### G.1 Linear project G3 (items named by what they cover; BEE ids not known here)

1. **The credential-posture item**: add the sentence "a read-only `claude_config_dir` cannot take Claude Code's own access-token refresh or transcript writes; decide, before Phase 0, whether the mount is read-only with a writable overlay for Claude Code's own files, or whether 'read-only' means only that no software of ours reads or writes there", and link experiments 10 and 11. Record the decision in the item, with the date.
2. **The Phase 0 probe item**: write the credential clause as "record what the run's own output says about its sign-in; never a file, never a variable"; add the exact outputs to capture (experiments 1, 2, 12, 30); state the wall time and that it may extend `probe.sbatch` or be a second probe; add "decide headless `-p` or Remote Control steered by the outer loop" as its gate.
3. **The quota-window item**: replace any fixed "five hours" with the ladder in D.4 (reset time from the message, then wait-and-continue when the wall time allows, then a fixed five hours as last fallback); add the weekly-cap distinction as not yet measured; add the cache consequence of overflow (5 minutes on usage credits).
4. **The pacing and concurrency item**: adopt the playbook's defaults as tunables with the words "unsourced, to be tuned by windows.log": `--max-turns` 150 (60 to 80 for test-heavy stages), model `sonnet` with Opus-class only in plan stages, effort `medium`, no subagent fan-out in batch, one job per window; add `--max-budget-usd` per stage with a value to be set after experiment 5.
5. **The ledger item**: add `windows.log` (one line per window, fields in D.4 rule 5) and the OpenTelemetry token count as its source if experiment 6 works; make clear that the ledger is the engine's own file on node-local disk checkpointed to CephFS, and that transcripts are never moved or copied.
6. **The hooks and managed-settings item** (skeleton thread): PreCompact, SessionStart, PreToolUse; `/etc/claude-code/managed-settings.json` in the shared image through `build_image.sbatch`; repo-level `.claude/settings.json` for model, effort, allow and ask lists; `autoContinueAtUsageLimit` on; nothing written into `claude_config_dir`; `cleanupPeriodDays` struck.
7. **The run template item**: `run.sbatch.tpl` with the window budget, `timeout --signal=INT`, `--signal=B:USR1@600`, `--permission-mode dontAsk`, `--session-id` then `--resume`, stream-json to `events.jsonl`, resubmission through the adapter with an explicit `--export` list (never `ALL`), continuation cap; `events.jsonl` and `run.json` added to the contract in both repositories in the same change.
8. **The measurement item (BEE-121 style)**: attach section F as its checklist; each line closes with a job id and a raw line, or "not yet measured".
9. **The decisions item**: close the roadmap's decision 1 as "subscription sign-in only; the API-key alternative is withdrawn under D1"; record decision 2 (plain sbatch templates), 4 (Pixi in the research image), 5 (contracts, CrossHair and RO-Crate deferred), 6 (Publish press only) as proposed by the roadmap, each still open until the maintainer says so.
10. **The regulated-data item** (student-facing policy): keep the playbook's rule that PHI, export-controlled and GDPR special-category data stay off a consumer plan, and state the engine's answer as "then the project does not run on Beethoven", not "use an API key".
11. **The roadmap document itself**: correct "framework 11, at 2e5bcf8" against the `VERSION` file (15 at that commit) or state which is meant.

### G.2 BUILD_PLAN section 4 (the file is not in this container; each edit names the text to add or change and must be placed against the real section)

1. Add a subsection "Credential posture of a headless run" restating D1 and the open question of G.1 item 1 (read-only mount versus Claude Code's own writes), with the date it is settled.
2. Add the token-economy table of section C as the section's configuration list, with the "who applies it" column kept, so the skeleton thread and the plan owner each see their rows.
3. Add the quota ladder of D.4 as numbered rules; strike any sentence that fixes the window at five hours or names a reset time as known.
4. Add the seven established facts as a boxed list at the head of the section so no later edit contradicts them (task budgets, usage analytics, cache 1 hour and 5 minutes, wait-and-continue in 2.1.234 and later, `--max-budget-usd`, deferred MCP definitions, the cloud session's own compaction variable).
5. Replace any mention of `setup-token`, `CLAUDE_CODE_OAUTH_TOKEN`, API keys or a gateway in the section with "excluded by D1"; if none is present, add one sentence saying they are excluded, so a reader of the playbook does not reintroduce them.
6. Add the Phase 0 probe as the first G3 deliverable, with its gate, and name `probe.sbatch` as the thing it extends.
7. Add the pattern table of section E as "what is already in hpcworker" so the plan does not re-specify the chain, the temp rule, the floor or the Slurm passthrough.
8. Add section F as "to measure" with the note that a claim moves out of this list only with a job id and a raw line.
9. Add the contract files (`run.json`, `events.jsonl`, `reforms.json`, `windows.log`) to the list of things that change in both repositories together.
10. Void (C7, 2026-10-04T01:12Z): there is no overflow note to add; usage credits are never used, a spent window hibernates or hands off (BUILD_PLAN §17).
11. Where the section attributes grid rules, keep the attribution the house requires: the 60 s floor and the wall-time rule are the product's own etiquette, not C&IT's.

## H. Sources

| Title | Drive id | Size |
|---|---|---|
| Beethoven build roadmap | 1Sz4Isdi4wW295AlmZnIKayBocq1ENTdhm375j3So7Ic | not stated in the extraction (read whole; "The content was not cut short") |
| Claude Code on a Slurm + Apptainer Cluster with a Consumer Subscription: Implementation Playbook | 1hK4F-Y4NrxaHkg-5RfEEhFkHqV28qo-zBOTZilkgmb8 | 81,170 characters, 1,066 lines (read whole in four chunks) |

Both documents are dated "Oct 3, 2026 · @greg" in the folder `claude-artefacts`. The playbook's
own sources line says its Claude Code facts "were checked against Anthropic's documentation on
October 3, 2026", as a blanket statement; the individual claims in section F are the ones it does
not pin to a page. The established facts at the head of this file come from Anthropic's pages on
2026-10-04 and take precedence over both documents where they differ.

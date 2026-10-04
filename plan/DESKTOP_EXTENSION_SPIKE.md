> **Filed 2026-10-03 by the re-plan thread (Linear project F1 = P-BEE-11; spike BEE-153; design doc
> BEE-154).** Written by a worker from Anthropic's current pages, then checked here against the two
> repositories: the `hpcworker` verbs and flags it names (`worker status --json --poll-floor`,
> `connect --login never --permission-mode`, `worker stop`, `claude login`), `hpcw_agent_marker`, the
> profile keys `ssh_host` / `ssh_port` / `ssh_host_key`, the extension's `redact` and `isEnvironmentUrl`,
> and `docs/V11_CONTRACT.md` / `docs/V12_CONTRACT.md` all exist; "warrior's banner bans python3, node,
> md5sum, rsync on sight" is recorded in `docs/V11_CONTRACT.md` and `docs/guides/LAB_LEAD.md`. Two rules
> to carry into the design doc: (1) D1 (2026-10-03) applies here too: the desktop edition never holds a
> Claude credential or an API key, and the Claude sign-in happens only in the student's own terminal on a
> compute node; (2) anything a student reads in Beethoven's own Desktop text keeps the plain-words rule of
> `CLAUDE.md` (paths, QoS and job ids belong in the terminal the student opened, not in our screens). The
> eight open questions in section 6 become sub-issues of BEE-153. Nothing below has run on a machine yet.

# Beethoven for Claude Desktop: design spike

2026-10-03. A spike, not a decision. Beethoven runs Claude Code and is not an Anthropic product; "Claude" and "Claude Code" are Anthropic's marks, used here to say what it runs; "Open OnDemand" is the mark of its publisher. Everything below marked **verified** was read today on Anthropic's pages (`claude.com/docs/connectors/building/mcpb`, the Desktop Extensions engineering post, the MCPB repository's `MANIFEST.md` and `CLI.md`, support articles 10949351, 12592343, 12622667); **not verified** means a page did not say it or no machine has shown it.

## 1. What a Claude Desktop extension is technically today

A Claude Desktop extension is a packaged **local MCP server**: a zip archive with the extension `.mcpb` ("MCP Bundle"; the format was renamed from `.dxt`, and existing `.dxt` files still install) whose one required file is `manifest.json` (`manifest_version` `"0.3"` in the current spec). The manifest names the server (`server.type` is `node`, `python`, `binary` or `uv`; `entry_point`; `mcp_config` with `command`, `args`, `env` and `platform_overrides`), declares the tools, an optional `user_config` whose fields can be `sensitive` (the engineering post says such values stay in the OS keychain), and a `compatibility` block (`claude_desktop` version range, `platforms` among `darwin`, `win32`, `linux`, `runtimes` ranges for `node` and `python`). Claude Desktop ships its own Node.js on macOS and Windows, so a Node server needs no runtime on the student's machine; the Node version is **not stated** on any page read. Claude Desktop itself runs on macOS and Windows only (**verified**); a Linux student has no Desktop and therefore no desktop extension. The server speaks MCP over stdio, runs as the student's own user and is installed per user. The CLI is the npm package `@anthropic-ai/mcpb` with `init`, `validate`, `pack`, `sign`, `verify`, `info` and `unsign` (**verified**). Whether Claude Desktop asks the student to approve each tool call, and with which words, is **not verified** here and must be measured on a real machine (section 6).

## 2. What it provides (MCP tools)

Every tool runs the **system OpenSSH** (`ssh`, `sftp`) of the student's machine, so the student's own `~/.ssh/config`, agent and `known_hosts` are reused unchanged, and the login node runs only `bash` and sshd's own `sftp-server`, never `node` or `python3` (warrior bans both on sight). The target is the site profile's `ssh_host`/`ssh_port`, the host key checked against `ssh_host_key` before anything else is sent. Eight tools, six of them read-only; each carries MCP's `readOnlyHint`/`destructiveHint` annotations truthfully.

| Tool | What it runs on the grid | Read-only |
|---|---|---|
| `open_grid_terminal` | opens the OS terminal (Terminal.app, Windows Terminal) with `ssh <host>`; the student signs in there, in sshd's own prompt, and types `hpcworker claude login` there if they wish | yes (for the server) |
| `worker_status` | `bash <shared_install>/bin/hpcworker worker status --json --name N --poll-floor 60` | yes |
| `read_contract_file` | `sftp` `get` of `status.json` or `connection.json` from `<shared_state_dir>/N/`, parsed by the fields the V11 contract names (`state`, `needs`, `environment_url`, `claude_login.loggedIn`, …) | yes |
| `tail_log` | last 256 KB of `progress.log` or `rc.log` from the same folder | yes |
| `list_run` | `sftp` `ls -l` of `<shared_state_dir>/N/` and `<shared_state_dir>/workspaces/N/` | yes |
| `read_workspace_file` | `sftp` `get` of one plain file under the workspace, 1 MiB cap | yes |
| `worker_start` | `bash <shared>/bin/hpcworker connect --name N --profile SITE --login never --permission-mode M`, the `HPCW-STEP` lines parsed by the contract grammar (one `sbatch`, by the framework) | no |
| `worker_stop` | `bash <shared>/bin/hpcworker worker stop --name N` (one `squeue`, one `scancel`, by the framework) | no |
| `open_in_claude` | none; opens `environment_url` with the OS opener after the same test the browser extension's `isEnvironmentUrl` applies | yes |

The server keeps one 60 s floor of its own on `worker_status` (and the framework's `--poll-floor 60` is a second), reads files no more than once per 5 s per run, and caches the last `status.json`. There is no free-form "run a command" tool: a terminal for a person is `open_grid_terminal`, and what the model may run is the enumerated list above with validated arguments (`N` matching `^[A-Za-z0-9_-]{1,32}$`, `SITE` a profile name, `M` one of three words).

**Authentication.** The server never authenticates itself if it can help it: on macOS the student's terminal session is opened with `ControlMaster=auto` and a `ControlPath`, and every tool call is `ssh -o ControlPath=…` reusing that session, so no credential ever enters the server's process. Where no master exists (Windows OpenSSH's support for multiplexing is **not verified**), `ssh` is started with `SSH_ASKPASS` pointing at a tiny prompt helper and `SSH_ASKPASS_REQUIRE=force`: the password and one-time code go from the dialog to `ssh`'s own pipe, and the Node process never holds them.

## 3. What it must never do, and how the design enforces it

1. **Store or log credentials.** No tool schema has a password or code field, so the model cannot be handed one; the prompt helper is a child of `ssh`, not of the server, and prints its one answer to `ssh` alone; `sshpass`, `expect` and `-o PasswordAuthentication` are absent and a CI grep fails the build on them. The server writes no file and nothing to stderr but one fixed start line, because Claude Desktop captures a server's stderr into its own log file (location **not verified**). Tool results pass through one redactor (the browser extension's `redact` rules) before the model sees them.
2. **Automate the university portal login.** The server has no HTTP client: no `fetch`, `http`, `https` or `undici` import, enforced by a dependency allowlist (`@modelcontextprotocol/sdk` and Node built-ins) and the same grep. Authorization needs no call either: the volume root's ACL already is the approved list, so an unapproved account simply cannot reach `<shared_install>` and `hpcworker` fails.
3. **Read or relay a Claude credential.** Reads are a positive allowlist of two roots (`<shared_state_dir>/N/` and `…/workspaces/N/`), resolved with sftp `realpath` before the check so a link cannot leave them, with `job.token` and any `.credentials.json` refused by name inside them; `~/.beethoven/claude`, `~/.claude` and the environment are unreachable because no tool takes a free path and no tool runs free commands. The Claude sign-in happens only in the student's own terminal.
4. **Run `claude auth logout`.** Not in the enumerated verbs; `connect` is always `--login never`, and the framework itself never runs it.
5. **Delete anything outside the framework's run directories and node-local temp.** The server has no `rm`, `rmdir` or sftp `rm`; `sftp` is driven in batch mode with `ls` and `get` only. Every `hpcworker` line runs under a plain `ssh` exec with no pseudo-terminal, which already trips the framework's own guard (`hpcw_agent_marker`: an agent variable in the environment, or no terminal), so a destructive subcommand refuses before it starts; the server also prefixes each line with `BEETHOVEN_REQUEST_ID=<random>`.
6. **Touch anything on claude.ai.** The server never connects to it: `open_in_claude` hands one checked `https://claude.ai/code?environment=env_…` link to the operating system's default browser, exactly as the browser extension's green button does, and nothing of ours runs on that page.

## 4. How it complements rather than replaces the browser extension

| Concern | Browser extension (Beethoven, Chrome Web Store) | Desktop extension (this spike) |
|---|---|---|
| Portal path: Open OnDemand session, shell, Files app, agreement, approval check | stays here | nothing |
| Direct way without VPN (WebCrypto ssh, native-messaging bridge, gate key) | stays here | not needed: the system `ssh` is a full client |
| *Open in Claude* at the moment the worker connects, auto-open setting | stays here | `open_in_claude` on request only |
| Interactive terminal on the grid | not possible (gate forced command, no pty for the student) | `open_grid_terminal` |
| Browse run and workspace files, read a file | listing and three files only | `list_run`, `read_workspace_file` |
| `progress.log`, `rc.log` tails | `progress.log` through the gate; `rc.log` refused there | both, redacted |
| Start, stop, status | yes | yes, the same `hpcworker` lines |
| Claude sign-in on a compute node | the sign-in sheet types the pasted code | only in the student's own terminal |
| Audience | every approved student, plain words | the maintainer, lab leads, students who want a terminal; paths are shown, since that is what was asked for |

The contract files and lines (`status.json`, `connection.json`, `progress.log`, `HPCW-STEP`) are the only seam; both clients read the same `docs/V11_CONTRACT.md` and `V12_CONTRACT.md` and nothing here redesigns them.

## 5. Distribution

Installation today is per user and by file: double-click the `.mcpb`, drag it into the Claude Desktop window, or Settings → Extensions → Advanced settings → Install Extension… (**verified**). The Connectors Directory takes submissions, but Anthropic's documentation calls MCPB "the secondary distribution path" and recommends remote servers for listing; a listed bundle must carry tool annotations, a privacy policy and working examples. Organizations on Team and Enterprise plans have an allowlist (Owners and Primary Owners, Organization settings → Connectors → Desktop; non-listed extensions are force-deleted; "Add custom extension" then "Add to team" offers an organization-scoped upload; the article names a minimum Desktop version) and machine policies (`isDesktopExtensionEnabled`, `isDesktopExtensionDirectoryEnabled`, `isLocalDevMcpEnabled`, by Group Policy or MDM) (**verified**). A student on a personal plan has no allowlist and installs the file. The browser extension's "one store, one private listing" rule has no Desktop equivalent; which channel carries the file to approved students (the same Google Group, a university's own Claude organization, or the directory) is a maintainer's decision this spike does not take.

Signing: `mcpb sign` appends a PKCS#7 signature after the zip (`--self-signed`, or `--cert`/`--key`/`--intermediate`), and `mcpb verify` reports subject, issuer, dates and a self-signed warning (**verified**); what Claude Desktop shows for an unsigned or self-signed bundle at install is **not verified**. Because the server is JavaScript run by Desktop's own Node and the only binaries it starts are the operating system's `ssh` and `sftp`, there is nothing of ours for Gatekeeper or SmartScreen to assess, and no notarization or Authenticode step is needed; that advantage is lost the moment a native binary (an ssh library, a compiled helper) is bundled, which is one reason for section 6's choice.

## 6. Proposal

**Repository** `OpenSpineConsortium/beethoven-desktop`, the third half of the split: `server/` (TypeScript, `@modelcontextprotocol/sdk`, stdio), `manifest.json`, `profiles/` vendored as data by the same `pull.sh` as the browser repository, a contract module mirroring `docs/V11_CONTRACT.md`, and a CI lane that greps for the forbidden imports and strings, runs the server against the python/asyncssh grid stand-in, and packs and verifies a signed bundle. No secret in the repository.

**Spawn the system `ssh`, do not embed an ssh library.** The student's `~/.ssh/config`, agent, hardware keys, `known_hosts` and the grid's `keyboard-interactive` prompts all work as they already do for that student; an embedded library would reimplement them, would have to be audited, would hold the one-time code inside our process, and would bring a native binary and with it notarization and signing. The browser needed its own client because it has no socket; the desktop does not.

**Phases.** (1) Spike, two days: `worker_status`, `read_contract_file`, `tail_log` against the stand-in, the forbidden-strings lane, a signed `.mcpb` installed on one machine. (2) Prototype on Greg's Windows 11 machine and its WSL against the real grid (`go2432`), one run name, every tool once, the authentication path measured, the result recorded in `docs/DIAGNOSTICS.md`. (3) Pilot with approved students who ask for a terminal, after the lab lead's answer to question 5 and a `LICENSE.txt`/`PRIVACY.md` revision (integer versions) naming the desktop extension's reads.

**Open questions only a real machine or the real grid can settle.**

1. Does Claude Desktop ask approval per tool call, and does an answer persist across sessions?
2. Does Windows OpenSSH honour `ControlMaster`/`ControlPath`, and `SSH_ASKPASS` with `SSH_ASKPASS_REQUIRE=force`? If neither, is WSL's `ssh` acceptable on Windows?
3. What does Desktop show for a self-signed bundle, and does a Developer ID or Authenticode certificate change it?
4. Where does Desktop write a server's stderr, and is anything of the tool traffic kept there?
5. Would the lab lead and C&IT accept an unrestricted desktop key enrolled beside the gate's restricted browser key, or must every desktop session be a password-plus-code sign-in?
6. Is the measured 5 s file read and 60 s status call within the login node's 20-process policy when a student has both the browser and the desktop open?
7. Does `sftp realpath` on CephFS resolve the `shared/ashley` to `shared/beethoven` link as expected, so the root check holds?
8. Which channel carries the file to approved students, and does the pilot university have a Claude organization whose allowlist could carry it?

## 7. Build outcome (2026-10-04, thread "Build the Claude Desktop ssh plugin")

Built in `OpenSpineConsortium/beethoven-desktop`, draft PR #1; the design is that repository's `docs/DESIGN.md` (BEE-154), which supersedes sections 2, 3 and 6 where they differ. Corrections and departures:

- **Linux.** Claude Desktop now has a Linux beta; "macOS and Windows only" in section 1 no longer holds. The manifest lists darwin, win32 and linux.
- **Claude Code Desktop's own SSH sessions** install and run Claude Code on the remote host, which on this grid is the login node; not a way in, and the server tells the model never to suggest it. The same server also ships as a Claude Code plugin (CLI and the Code tab).
- **No askpass.** The sign-in runs in a terminal window the OS opens; the password and code go only into ssh's own prompt; that ssh stays as a connection master and every tool is a `BatchMode` client of it. Question 5 is answered: no unrestricted desktop key is needed.
- **The gate's verbs**, not raw `hpcworker` commands: `version`, `status`, `connect … --login never`, `stop`, `read … progress.log`, run as `hpcworker gate` from the shared copy over the student's session. `rc.log` is not read; the run directory is not listed.
- **Files**: the workspace only, through a read-only SFTP v3 client of our own over `ssh -s sftp` (no `sftp` batch mode), confined by the grid's REALPATH, links refused, credential names refused, credential text redacted, a printing `~/.bashrc` tolerated.
- **No kill-list and no access-service call**: the server opens no network connection of its own; the grid's approved list gates the shared copy (BEE-154, BEE-158 comments).

Measured in the container: 53 tests, against a real OpenSSH sshd on 127.0.0.1 with the grid's algorithms (the gate stand-in, and the real hpcworker 16 gate), and the built server through the official MCP SDK client; `mcpb validate`/`pack` and `claude plugin validate` pass.

**Laptop checks** (the full steps are `docs/LAPTOP_CHECKS.md` in the repository; outcomes go there and here):

| # | Check | Outcome |
|---|---|---|
| 1 | Install the `.mcpb` on Windows 11; what Desktop says about an unsigned bundle | not yet measured |
| 2 | Per-tool approval; whether "always allow" persists; `worker_stop` asks | not yet measured |
| 3 | Sign in through WSL's ssh; the sign-in outlives the window | not yet measured |
| 4 | Windows' own ssh without WSL (connection master or not) | not yet measured |
| 5 | The pinned host key passes; our `known_hosts` holds only the grid | not yet measured |
| 6 | Start, status at most once a minute, open in Claude, log, stop | not yet measured |
| 7 | Workspace list and read on CephFS | not yet measured |
| 8 | What Desktop's own log keeps of tool results | not yet measured |
| 9 | Whether Desktop times out the 40 s sign-in wait | not yet measured |
| 10 | The Claude Code plugin on the laptop | not yet measured |
| 11 | Extra usage off on the worker's account | not yet measured |

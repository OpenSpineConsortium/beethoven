# Project-state tools the coordinator holds (beethoven, chan_01JbwQwHoYeBWptjPB5c6u8m)

Listed by the coordinator from its own tool list at 2026-10-05T00:27:54Z. Each line says whether the tool reads or writes, then what it takes. Tools that are only named inside another tool's description, and are not in the coordinator's list, are marked so.

The coordinator's Agent-tool workers hold no hearthbot tools: a worker checked on 2026-10-05 and found none. Every hearthbot call below is therefore the coordinator's own; its workers only read and write files.

## Project settings
- `mcp__hearthbot__get_project_settings` (read): no arguments. Returns the name and the stored settings (the exact set read is in settings.json): instructions, repo_urls, model_id, channel_session_model_id, default_environment_id, proactivity_level (absent when unset), memory_enabled, tasks_enabled, min_routine_interval_minutes, topic, context_sources, and migrated_routines on a project migrated from a legacy one.
- `mcp__hearthbot__update_project_settings` (write): instructions (at most 32 KiB, empty clears; reaches threads started afterwards), model_id (default model for threads started afterwards), name (renames only a shared project, sent alone; not a private project like this one), add_repo {owner, repo} (appends one github.com repository, server-gated, only when the user explicitly asks). Its description says proactivity_level can be moved where already set, but its schema has no such field. It cannot write topic, context_sources, repo_urls beyond that one append, default_environment_id, memory_enabled, channel_session_model_id or min_routine_interval_minutes; those are Project settings clicks.
- `mcp__hearthbot__propose_project_setup` (write, applied only when the user confirms the card; private projects only): name, icon and color (only while the name is a placeholder such as "Untitled project"), repos (up to 20 github.com URLs, only while the project has none), connectors (directory ids), routines (up to 3: name, 5-field UTC cron, prompt; off by default), sessions (up to 4 threads to start), evidence. It also accepts a hand-off: a proposal the user approved in their Claude Code CLI or desktop app, sent as a cross-session message and posted once exactly as given.
- `mcp__claude-code-remote__add_repo` (write): owner, repo, access (read or push), save_to_project (true also saves it to repo_urls after the user allows it on a prompt). `mcp__claude-code-remote__list_repos` (read): query, limit.
- `mcp__hearthbot__update_status_page` (write): html, recap; the Overview's Custom view tab, only on a member's ask.
- `mcp__hearthbot__list_thread_connectors` (read): no arguments; the MCP servers and connectors a new thread starts with. `ListConnectors` (read): keywords. `SearchMcpRegistry` (read): keywords. `mcp__hearthbot__suggest_connectors` (write): directory_uuids or reconnect_server_ids, thread_id; posts a Connect card and connects nothing itself.
- `mcp__hearthbot__list_devices` (read): no arguments; folders and devices for Remote Control.

## Memory
- `mcp__hearthbot__read_memory` (read): no arguments; returns MEMORY.md, the index file team/silo/MEMORY.md in the session memory directory /tmp/claude/memory/team/silo.
- `mcp__hearthbot__update_memory` (write): content, the whole new MEMORY.md (at most 16384 bytes; replaces the file).
- The other memory files (team/silo/*.md, one fact each) are written with the ordinary Write tool into /tmp/claude/memory/team/silo; the coordinator has its workers do that. The coordinator does not hold the `mcp__memory__` tools or `memory_write`, which threads may have.

## Routines
- `mcp__claude-code-remote__list_triggers` (read): enabled, recurring, include_completed, limit, cursor, all_in_channel. It covers the whole account, not one project.
- `mcp__claude-code-remote__get_trigger` (read): trigger_id; also returns the stored prompt.
- `mcp__claude-code-remote__update_trigger` (write): trigger_id plus any of name, cron_expression, run_once_at, enabled, model, prompt.
- `mcp__claude-code-remote__delete_trigger` (write): trigger_id.
- `mcp__claude-code-remote__send_later` (write): message, at or delay_minutes, name, initiation; a one-shot routine that messages this session.
- Not in the coordinator's list: create_trigger and fire_trigger (named in other tools' descriptions). Threads hold create_trigger; the hand-off thread made trig_017z489cGKUvqigk9HQa8RgR with it. Routines belong to the account, so a new account starts with none.

## Threads and messages
- `mcp__hearthbot__list_thread_sessions` (read): cursor, limit, since_ts; returns session_id, thread_id, title, status, and created and last-activity times.
- `mcp__hearthbot__fetch_project_timeline` (read): cursor, limit, full_bodies.
- `mcp__hearthbot__fetch_thread` (read): thread_id, order, limit, cursor, full_bodies.
- `mcp__hearthbot__fetch_messages` (read): up to 8 message ids.
- `mcp__claude-code-remote__list_events` (read): session_id, kinds, limit (at most 100), after_id, before_id; a session's transcript including tool calls. `mcp__claude-code-remote__get_event` (read): session_id, event_uuid.
- `mcp__hearthbot__start_thread_session` (write): instructions (at most 8192 bytes), title, thread_id, ack, project_ack, project_post_id, context_message_ids (up to 8), attachments (files a person uploaded in this project), model, effort, outcome_branch, purpose. A new thread starts with only these; no tool restores an earlier conversation into a thread.
- `mcp__hearthbot__message_thread` (write): thread_id, text (at most 8000 characters), context_message_ids (up to 8), attachments.
- `mcp__claude-code-remote__send_message` (write): session_id or to, message (at most 64 KiB), priority.
- `mcp__hearthbot__post_message` (write): text, thread_id, attached_outputs (files under /mnt/project-files, https links, published Artifacts).
- `mcp__hearthbot__update_message` (write): message_id, text; the coordinator's own messages only.
- `mcp__hearthbot__rename_thread` (thread_id, name), `set_thread_resolved` (thread_id, resolved), `set_thread_label` (label), `react` and `unreact` (message_id, emoji), `ask_decision` (question, 2 to 4 options, recommended, context, reason), `post_widget` (family, widget, input, text): all write.
- `mcp__hearthbot__start_rc_session` (write), `stop_rc_session` (write), `rc_session_status` (read): Remote Control sessions on greg's own device.
- `mcp__hearthbot__list_project_prs` (read): limit. `mcp__hearthbot__list_project_artifacts` (read): limit.
- `mcp__hearthbot__get_channel_session_id` (read; `get_project_session_id` is its old name): no arguments.
- `mcp__hearthbot__summarize_recent_sessions` (read): limit, window_days, max_events, session_ids, exclude_session_ids; the owner's recent Claude Code sessions on this account, at most 10 calls an hour per project.
- `mcp__hearthbot__list_original_project_chats`, `read_original_project_chat`, `list_original_project_sessions` (read): only for a project upgraded from an older one.
- `mcp__hearthbot__switch_model`, `mcp__hearthbot__set_effort_level` (write): this session only, and only on the user's explicit ask.

## What this means for an import into a new account
Automatic, by the new project's coordinator or its threads: the instructions and the threads' default model (update_project_settings); MEMORY.md (update_memory) and the other memory files (Write into that session's memory directory); everything under /mnt/project-files; new threads briefed from the hub (start_thread_session); routines (a thread's create_trigger).

Needs greg's clicks: creating the project and entering its name and goal (no tool writes the topic, and the name only through a setup card while it is still a placeholder); the repositories (one confirm on a setup card while the project has none, otherwise Project settings, or one at a time on his explicit ask); the three Drive folders as context sources; the default environment; memory on and the coordinator's own model (Project settings).

Inferred from the tool descriptions, not tested: environment ids belong to the account, so the environment is recreated in the new account; Google Drive, Linear and GitHub are each connected from the new account before its threads can reach them.

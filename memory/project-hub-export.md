---
name: project-hub-export
description: How the beethoven project travels to another Claude account and back through the hub repository OpenSpineConsortium/beethoven (greg 2026-10-05 00:17Z)
metadata:
  type: project
---

greg (hand-off thread, 2026-10-05 00:17Z): export the memory, goal, instructions, name and all
metadata needed to bring this project up in a new Claude account, and load the progress made there
back into this account; later each of his accounts works on its own repository in parallel, with
the hub and Linear as the common record.

- Hub: OpenSpineConsortium/beethoven (private). PR #1 merged by greg 00:14Z (9e8a7f7); syncs go
  straight to main (his card, 00:13Z); changes to the hub's own files go through a pull request.
- Per-project metadata lives in /mnt/project-files/projects/<project id>/ (this project:
  chan_01JbwQwHoYeBWptjPB5c6u8m): the coordinator writes settings.json, topic.md, instructions.md and
  tools.md from get_project_settings; the hand-off thread writes threads.json, routines.json,
  connectors.json and session.json. Another account's project writes its own folder beside it.
- tools/hub.py (being built 00:2xZ) replaces the one-way tools/sync.py: a three-way sync per file
  between the project files, this memory folder and the hub, with a record per project
  (projects/<id>/sync.json), never deleting, never overwriting a side changed since the last sync,
  ledger rows merged.
- Not yet measured: whether a memory file written by a process other than the Write tool reaches the
  memory service. This file was written by python at 00:25Z as that probe.

**Why:** the next thread must not rebuild the export or treat the hub as one-way.
**How to apply:** read the hub's README and IMPORT.md before moving the project; check the record
of a claim against GitHub first. See [[multi-account-d4]].

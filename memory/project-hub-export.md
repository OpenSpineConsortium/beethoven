---
name: project-hub-export
description: How the beethoven project travels to another Claude account and back through the hub repository OpenSpineConsortium/beethoven (greg 2026-10-05 00:17Z; PR #2 merged 01:24Z)
metadata:
  type: project
  modified: 2026-10-05T01:24:03.882Z
---

greg (hand-off thread, 2026-10-05 00:17Z): export the memory, goal, instructions, name and all
metadata needed to bring this project up in a new Claude account, and load the progress made there
back into this account; later each of his accounts works on its own repository in parallel, with
the hub and Linear as the common record. 01:20Z: "make an immediate push" (he was near his limit).

- Hub: OpenSpineConsortium/beethoven (private). Syncs go straight to main (his card, 00:13Z); the
  hub's own files go through a pull request, his merge. main 2bd08fa (01:23Z) holds every project
  folder, memory/, and projects/chan_01JbwQwHoYeBWptjPB5c6u8m/ (settings, topic, instructions,
  tools, threads, routines, connectors, session).
- PR #2 (merged by greg 2026-10-05 01:24Z, main 2156ec5): tools/hub.py, the two-way
  three-way sync (23 tests green; record projects/<id>/sync.json; never deletes; CONFLICT when both
  sides changed; ledger rows merged; scan both ways), tools/HUB_SPEC.md, IMPORT.md (the steps both
  ways), LANES.md (one account per repository), corrected SEAMS.md.
- Not yet built in hub.py: never write MEMORY.md into a memory folder (the coordinator owns the
  index), and never push a stale memory copy (HUB_SPEC.md last section). A container's memory copy
  can be stale: the hub's memory/MEMORY.md came from a 00:25Z copy.

**Why:** the next thread must not rebuild the export or treat the hub as one-way.
**How to apply:** read the hub's README and IMPORT.md before moving the project; check PR #2's
state on GitHub first. The routine trig_017z489cGKUvqigk9HQa8RgR still names sync.py, which now forwards to hub.py and refuses until `hub.py init --project-id chan_01JbwQwHoYeBWptjPB5c6u8m` has been run once in this project. See [[multi-account-d4]].

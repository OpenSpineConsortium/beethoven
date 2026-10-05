# tools/hub.py: two-way sync between a Claude project and the hub

Repository: `/home/user/beethoven` (OpenSpineConsortium/beethoven, the project hub), branch
`claude/handoff-state-file-m0rg4r`. Read `README.md`, `CLAUDE.md`, `tools/sync.py` (the one-way copy
it replaces) and `tools/scan.py` (the secret scan it must keep using) first.

## Why

greg (2026-10-05 00:17Z): export everything needed to bring this Claude project up in a new Claude
account, AND be able to load the progress made there back into the original account; later, several
of his Claude accounts work in parallel, each on its own repository, with the hub and Linear as the
common record. Today `tools/sync.py` only copies project -> hub and refuses to overwrite a hub file
whose last commit lacks a `Hub-Sync:` trailer. It cannot bring hub changes back into a project.

## What to build

Python 3.8+ standard library only (it runs in cloud sessions and on greg's laptops). Files:
`tools/hub.py` (new), `tools/test_hub.py` (new, `python3 -m unittest tools/test_hub.py` from the
repository root, or `python3 tools/test_hub.py`), `tools/sync.py` (becomes a thin shim that prints one
line saying hub.py replaced it and runs `hub.py sync` with the same flags), `.gitattributes` (see
Bytes). Do not commit; leave the changes in the working tree. Do not touch any other file. Do not
run anything that pushes to GitHub: the tests use a local bare repository as the remote.

### Commands

```
python3 tools/hub.py status [--json]            # what sync would do, per path; writes nothing
python3 tools/hub.py sync [--commit] [--push] [--trailer 'K: v']... [--only pull|push] [--prefer hub|project]
python3 tools/hub.py init --project-id ID [--prefer hub|project] [--commit] [--push] [--trailer ...]
python3 tools/hub.py diff PATH                  # base, project and hub versions of one path, as unified diffs
common: --source DIR (default $HUB_SOURCE or /mnt/project-files)
        --memory DIR (default $HUB_MEMORY_DIR, else the single directory matching
                      /tmp/claude/memory/team/*/ that contains a `.memory-sync` file; if none or several, memory is
                      skipped with one printed line, unless --memory is given)
        --project-id ID (default $HUB_PROJECT_ID, else the first line of <source>/.hub-project; `init` writes
                      that file; sync refuses to run without an id)
```

`--push` implies `--commit`. A plain `sync` with neither writes files on both sides and updates the
record in the working tree but commits nothing (say so in its output).

### Paths

- Synced folders (project `<source>/<f>/...` <-> hub `<f>/...`): EVERY top-level directory of the
  source, so a folder a thread adds later (one named `sites` appeared at 00:11Z) is carried without a
  code change, plus every top-level directory of the hub that is not reserved. Reserved names, never
  synced as folders and reported once if a project has one: `tools`, `linear`, `memory`, `.git`,
  `.github`, `.claude`. Excluded paths (`.hub-exclude`) still apply (`uploads/` never moves). Top-level
  FILES of the source are not synced (say so in the output if any exist). Files only, recursive,
  skipping any path component that starts with `.`. Never follow a symbolic link (report it and skip).
  The `.gitattributes` byte-for-byte rule below must therefore cover any synced folder: write it as
  `* -text` for everything with explicit `text eol=lf` lines for the hub's own files (`*.py`, the
  root `*.md` files, `.hub-exclude`, `.gitignore`, `.gitattributes`, `tools/**`, `linear/**`), or an
  equivalent that a test proves.
- Memory: every top-level `*.md` file of the memory directory <-> hub `memory/<name>.md`. Never a
  dotfile (`.memory-sync`, `.memory-sync-basis` belong to the harness), never a subdirectory.
- `.hub-exclude` (repository root) patterns apply to both directions, matched against the hub-relative
  path (`uploads/` and the two superseded bundles today). Keep `sync.py`'s matching rule.
- Hub-only, never written into a project: `projects/*/sync.json` (the records), everything outside the
  synced folders and `memory/` (`linear/`, `tools/`, root files).
- The per-project record lives in the hub at `projects/<project-id>/sync.json`:
  `{"project_id": ..., "updated_utc": "YYYY-MM-DDTHH:MMZ", "files": {"<hub path>": "<git blob sha1 of the bytes both sides held at the last sync>"}}`.
  The git blob sha1 is `sha1(b"blob %d\0" % len(data) + data)` over the raw bytes, so the base text of
  any path is `git cat-file blob <sha>` from the hub's own object store.

### Bytes

The hub's `.gitattributes` is `* text=auto eol=lf`, which would rewrite CRLF files and make a project
and the hub differ forever. Every synced folder (any name, see Paths) and `memory/` must be stored
byte for byte (keep `*.bundle binary` and `*.png binary`). A test must show a CRLF file in a folder
whose name the code has never seen round-trips with no change reported afterwards.

### The three-way rule, per path

B = base sha from this project's record (None if absent), P = project bytes' sha (None if the file is
absent), H = hub working-tree bytes' sha (None if absent). Union of paths = record keys + project files
+ hub files (after exclusions).

| Case | Action |
| --- | --- |
| P == H | nothing to copy; record base = P (drop nothing from the record when both are None) |
| P == B, H != B, H present | PULL: write hub bytes into the project |
| P == B, H absent | GONE (hub side): report, write nothing, keep the record |
| H == B, P != B, P present | PUSH: write project bytes into the hub |
| H == B, P absent | GONE (project side): report, write nothing, keep the record |
| B is None, exactly one side present | copy to the other side (PULL or PUSH) |
| both changed since B (or B None, both present, differ) | append-only merge if the path is append-only and both sides extend the base text (below); else `--prefer` if given; else CONFLICT: report, write nothing for that path, keep the record unchanged |

Append-only paths: `ledger/LEDGER.md` and any `ledger/*.md` (rows are only ever appended). Merge when
both P and H texts start with the base text (base None counts as empty only if neither side existed
in any record before; otherwise CONFLICT): result = base + P's added lines + the lines H added that P
did not add, in H's order. Write the result to both sides. Note it as MERGED.

`--only pull` performs only PULL actions (and merges into the project side only if both directions
are allowed; with --only, an append-only merge is a CONFLICT); `--only push` the reverse. `--prefer hub`
turns a CONFLICT into a PULL, `--prefer project` into a PUSH; never the default.

Nothing is ever deleted, on either side, by any command. Never `os.remove`, `shutil.rmtree`,
`git rm`, `git clean`, `git reset --hard` or `git checkout --` on a synced path.

### Safety around the run

- The hub working tree must be clean before `sync` or `init` writes anything (`git status --porcelain`
  empty); otherwise exit 1 with a plain sentence.
- With `--push` (and `--commit`): fetch the current branch from `origin` first; fast-forward when
  behind; refuse when diverged (exit 1, "pull and reconcile first").
- Every file about to be written, in either direction, is scanned with `scan.scan_file` (the same
  `scan.allowed(ROOT)` allow list) BEFORE anything is written. Any `fail` finding: write nothing at all
  on either side, exit 2. Warnings are printed and do not stop the run.
- The record is written only after all file writes succeed, and only for paths that ended equal on both
  sides; a path in CONFLICT or GONE keeps its old base.
- Commit message (only when the hub changed: a pushed file or the record):
  `sync: project <id> at <UTC stamp>`, a body line `<n> pushed, <m> pulled, <k> merged, <c> conflict(s), <g> gone`,
  then the trailers `Hub-Sync: <stamp>`, `Hub-Project: <id>`, then each `--trailer` line.
- Push race (several accounts sync the same hub): push `HEAD:<branch>`. If rejected, fetch; if the
  remote's new commits touch none of the paths this commit changed except other projects' records,
  rebase this run's own unpushed commit(s) onto the remote branch (never anything already pushed) and
  push again, up to 3 times; if they touch a path this commit changed, abort the rebase if one started,
  keep the local commit, and exit 4 with "the hub moved under this sync; run `hub.py sync --push` again"
  (the next run must then handle the local commit sensibly: document what it does). Network failures:
  retry the push up to 4 times with 2, 4, 8, 16 s waits.
- `init --project-id ID`: writes `<source>/.hub-project` (the id, one line) if absent or equal; refuses
  if it holds a different id. Then runs the same three-way pass with no record: files present on one
  side only are copied; equal files are adopted into the record; differing ones are CONFLICT unless
  `--prefer`. This is how a project in a new account first loads the hub (its folders are empty, so
  everything is PULLed, memory included), and how the original project adopts its current state.
- Output: one line per acted-on path (`PULL`, `PUSH`, `MERGED`, `CONFLICT`, `GONE`), then a summary line.
  `status --json` prints `{"actions": [{"path":..., "action":..., "reason":...}], "summary": {...}}`.
- Exit codes: 0 clean, 3 when any CONFLICT remained (the rest still synced), 2 scan failure, 1 usage
  or repository state, 4 the push race above.
- A printed line (once per run that writes memory) saying that whether memory files written by a
  process other than Claude's own Write tool reach the project's memory service is not yet measured
  (until the README says otherwise).

### Tests (tools/test_hub.py), each failing on a version without the behaviour

Use temporary directories only: a bare repository as `origin`, two hub clones, two project sources A
and B, two memory dirs (each with a `.memory-sync` dotfile that must never be copied). Cover at least:
1. A `init` adopting its existing equal state; record written; nothing copied.
2. B `init` from empty folders: every file and memory note arrives; `.hub-project` written.
3. B edits a state file and a memory note, `sync --push`; A `sync --push` pulls both.
4. A and B edit different files between syncs: both flow both ways.
5. A and B edit the same file: CONFLICT, neither side overwritten, exit 3, the other files still synced;
   `--prefer hub` resolves it.
6. Both append rows to `ledger/LEDGER.md`: MERGED, both sides equal, no row lost or doubled.
7. A file deleted on one side: GONE reported, nothing deleted anywhere, the file still on the other side.
8. A planted secret (an OpenSSH private-key block, built by the test so no file holds one, or whatever `scan.FAIL` refuses)
   on either side: exit 2, nothing written on either side, no commit.
9. `uploads/x.png` in a project: never reaches the hub; `projects/<id>/sync.json` never reaches a project.
10. A CRLF file round-trips; a second `status` reports nothing to do.
11. Race: another clone pushes an unrelated commit between this run's fetch and push: rebased and pushed;
    pushes a change to the same path: exit 4, nothing lost, the next run recovers.
12. Dotfiles in the memory dir untouched (bytes and presence) after every test.
13. A dirty hub tree: refused, nothing written.
14. The `sync.py` shim forwards to `hub.py sync`.

Run the tests and report the output verbatim (the summary line) in your final answer, with the list of
files you changed. Also run `python3 tools/scan.py tools/hub.py tools/test_hub.py tools/sync.py`.

## Style

Match `tools/sync.py` and `tools/scan.py`: a module docstring that says why, comments only for why,
plain names, no third-party imports. No em-dashes in prose. Never use the word that starts "prov" and
ends "enance"; say origin, source or record.

### Memory is a per-container copy that can be stale (measured 2026-10-05 00:41Z; added after the build started)

Each session's container holds its own copy of the memory folder. The harness uploads a file written
there by any process within seconds (measured: a note written by python at 00:25:16Z had a service id
in `.memory-sync-basis` at 00:25:24Z, same sha256), but it refreshes the copy from the service only at
some events: the coordinator's copy was half an hour old while the service held a newer `MEMORY.md`
that its own `update_memory` had written. So:

1. Never write `MEMORY.md` (the index) into a memory folder, in any command, `init` included. When the
   hub's `MEMORY.md` would be pulled, report `INDEX` with one line saying the coordinator applies it
   with `update_memory` from the hub's `memory/MEMORY.md`, and leave the local file and the record as
   they are. Pushing `MEMORY.md` follows rule 2.
2. A memory file whose bytes equal any earlier committed version of that same hub path (any commit in
   the hub's history, not only the base) is a stale copy, not a change: report `STALE`, do not push it,
   do not record it. Pull over it only when it also equals the base (the ordinary PULL case).
3. Project files under `--source` are one shared mount for every session of a project, so rules 1 and
   2 apply to memory only.
Tests: a stale memory copy (an older committed version) is neither pushed nor recorded; MEMORY.md is
never written into a memory folder; INDEX is reported.

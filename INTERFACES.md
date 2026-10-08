# The Beethoven interface standard, version 1

greg, 2026-10-07 11:35Z: "encapsulating each repo so that it is independent and not directly
accessing any code of another repo in the Beethoven ecosystem. Make sure it obeys the standard
API-type interfacing."

Every repository of the ecosystem is a sealed unit. Another repository reaches it only through what
it publishes, at a version, through a copy pinned to a merged commit, and never through its source
tree. Five rules say what that means. Each repository checks them on itself, in its own test run,
with no secret and no network. The standard grows out of what the project already did well: the
pinned copy of beethoven-qa with its `ORIGIN` record, the site modules pinned by commit and sha256,
and the base design's vectors produced by the real writer (`base/DESIGN.md`).

## Rule 1. A repository builds, tests and runs from its own tree

No tracked script, test, task, hook, workflow, container recipe or configuration file reads, runs or
copies a file of another repository's checkout: no `../<repository>`, no path built from this
checkout's parent (`$(dirname "$HERE")/<repository>`), no variable whose value is another checkout
(`HPCWORKER_DIR`, `BEETHOVEN_SERVICE_DIR`), no git submodule, no dependency by path or git URL, and no
clone or `actions/checkout` of another repository. Prose may name another repository: a person
reading it is not code reaching it.

## Rule 2. What a repository offers, it declares in one place

`interface/INTERFACE.json` names every export another repository may take. Nothing else is offered:
everything not listed is private and may change in any pull request. Every repository has the file,
even one that exports nothing, because its `imports` make the ecosystem's dependency graph
machine-readable.

```json
{
 "format": 1,
 "name": "hpcworker",
 "repository": "OpenSpineConsortium/hpcworker",
 "summary": "one sentence",
 "standard": "https://github.com/OpenSpineConsortium/beethoven/blob/main/INTERFACES.md",
 "exports": [
  {"id": "contract", "kind": "contract", "version": 1, "summary": "...",
   "paths": ["interface/contract/"], "consumers": ["OpenSpineConsortium/beethoven-extension"]}
 ],
 "imports": [
  {"repository": "OpenSpineConsortium/beethoven-sites", "export": "modules", "version": 1,
   "into": "framework/sites", "origin": "framework/sites/ORIGIN"}
 ]
}
```

- `kind`: `contract` (a protocol between programs as data: JSON Schemas for files, a line grammar,
  the command lines a caller may type, rules, and vectors), `schema` (JSON Schema or a schema-like
  data file), `data` (data files), `python` (public modules and the names each exports), `cli` (the
  commands a caller may run), `files` (files a consumer carries byte for byte, such as the repository
  kit), `program` (code a consumer may run as a black box in its own tests, never import from), `text`
  (a contract written for people).
- `version`: an integer per export, raised on any change a consumer must act on (a field removed,
  renamed or retyped, a code whose meaning changes, a command that goes away). An additive change (a
  new optional field, a new failure code an older consumer reads as `other`) keeps the version.
- `paths`: relative to the repository's root; a path ending in `/` means every file under it, and `*`
  matches within one part of a path.
- `consumers`: who takes the export today; informative, for the person changing it.

## Rule 3. A repository takes another's export only as a pinned, checked copy

- One folder per import (`into`), holding exactly the export's files and an `ORIGIN` record:

  ```
  repository OpenSpineConsortium/hpcworker
  commit <40 hex>
  export contract 1
  sha256 <64 hex> <path inside the folder>
  ```

  one `sha256` line per file. Each file lands at its path below the folder all of the export's paths
  share (`framework/profiles/*.json` puts `framework/profiles/wayne.json` at `wayne.json`;
  `interface/contract/` puts `interface/contract/lines.json` at `lines.json`). Besides those files the
  folder may hold only `ORIGIN`, `README.md` and `pull.sh`. A copy taken before its provider published `INTERFACE.json` has no `export` line; the
  next pull writes one. beethoven-qa's own copy keeps its record (`vendor/beethoven-qa/ORIGIN`:
  repository, ref, commit, tree digest) and its check (`vendor-check`), and is taken by beethoven-qa's
  `vendor` command instead of a `pull.sh`. From beethoven-qa 3.0.0 (the maintainer's decision of
  2026-10-07) that command fetches as the next bullet says: from GitHub through the person's own `gh`
  sign-in, at a release tag on `main`, each file checked against the blob id the commit's tree gives
  it, never from a checkout. It is the one pull that runs the provider's code: the consumer's own
  pinned copy of it, or, for a consumer's first copy of 3.0.0, a clone of that release. A release tag
  is made only on `main`, by the maintainer. `vendor-check --source`, the maintainer's audit run from
  a beethoven-qa checkout's own environment, rebuilds the copy from the commit `ORIGIN` names. The exports
  a consumer takes from beethoven-qa (`python`, `cli`, `kit`, `plugin`) share that one folder, each
  its own entry in `imports`.
- Fetched only by that folder's `pull.sh`, from GitHub
  at one commit through the person's own `gh` sign-in: never from a checkout, never by running the
  provider's code, only from a commit the provider's default branch contains (a merged change, never
  a pull request's branch), and only the paths the provider's `INTERFACE.json` lists for that export
  at that commit, with the version the consumer's code reads.
- Never edited by hand. The consumer's own test run fails when a file differs from `ORIGIN`, when the
  folder holds a file `ORIGIN` does not list, or when `ORIGIN`'s export or version is not the one the
  import names.
- A pull never deletes: a file the provider dropped is listed for a person to remove in a reviewed
  commit.
- A `program` export that only an opt-in test runs (desktop's real-gate test) may stay out of git:
  its folder commits `ORIGIN` alone, `pull.sh` fetches the files into it (ignored by git), and the
  test checks them against `ORIGIN` before it runs them.

## Rule 4. A consumer uses only the published surface

- Python: a repository imports another's package only through the modules its `python` export lists
  (beethoven-qa's `boundary` command checks every `import` of the engine's repositories).
- Files and lines: a consumer's parser is tested against the provider's published schemas and the
  vectors the provider's real writer produced; a constant a consumer types by hand (a failure code, a
  field name, a variable it strips) is tested equal to the pinned export.
- Commands: a consumer types only what the provider's `cli` (or `contract`) export lists, and reads
  the output through the export's lines and schemas.

## Rule 5. Direction

- The engine: beethoven-qa <- beethoven-agents <- beethoven-research, never back (greg, 2026-10-04
  04:52Z). beethoven-qa depends on nothing of ours.
- The launcher and the engine share data only (the site profiles, the contract's rules), never code.
- A cycle between two repositories is allowed only between exports of different kinds that do not
  depend on each other's version (hpcworker's module schema and beethoven-sites' modules). A cycle of
  code is never allowed.

## How a provider changes an export

1. Change the code and the export together in one pull request. A `contract` export's vectors are
   rewritten by the provider's tool (hpcworker: `python3 framework/tests/vectors.py --write`); its
   test fails until they are, so an output never moves silently.
2. Raise the export's `version` when a consumer must act; keep it for an additive change.
3. After the merge, each consumer takes the new copy with its `pull.sh` in a pull request of its own,
   and its conformance tests say whether its code still reads the export.

## What each repository runs

| Repository | Its check | Where it runs |
| --- | --- | --- |
| hpcworker | `framework/tests/test_interface.py` (the manifest, the schemas, the vectors against the real writer, the line grammar, the rules against the code) and `test_boundary.py` (rules 1 and 3) | `framework/tests/run.sh`, CI on ubuntu and CentOS 7 |
| beethoven-sites | `tests/test_boundary.py` (rules 1 to 3) | `unittest discover`, CI and pre-push |
| beethoven-extension | `extension/test/boundary.test.ts` (rules 1 to 3) | vitest, CI |
| beethoven-desktop | `test/boundary.test.ts` (rules 1 to 3) | vitest, CI and the gate |
| beethoven-qa | `python -m beethoven_qa boundary` (rules 1 to 5; imports by AST) | the gate, pre-push and CI; every consumer runs the same command from its pinned copy |
| beethoven-agents, beethoven-research | `python -m beethoven_qa boundary` from the pinned copy, and `vendor-check` | the gate (from the re-pin to beethoven-qa 2.0.0 or later) |
| beethoven-vscode, the studies, the website | not changed from this thread (read-only neighbours); the report says what each needs | |

# beethoven-qa: what remains, and how independent of Claude it is

Assessed 2026-10-08, 15:40Z to 17:20Z, against `OpenSpineConsortium/beethoven-qa` main `b73d4f4`
(version 4.0.0, merged 13:01Z; tags on origin: v1.0.0 `16415b4`, v2.0.0 `53d5ae5`, v3.0.0 `08aca99`,
no v4.0.0 yet). Read-only in every repository: nothing was pushed. The gate was run in full on
main (green: 202 tests, 41 CrossHair targets, all six standards groups, 16 min 55 s wall on four
cores), every check was traced to the line that runs its tool, each was then broken on purpose in a
scratch clone to see what it reports, and three skeptics tried to refute the tool table, the
"no model in the loop" claim and the gap list. Where a number came from this box under load it says
so; what nobody has run yet says "not measured".

## 1. The answer

**Every blocking verdict is produced by an established tool or by deterministic code in the
repository. No check asks a model anything.** The pre-push hook (`.githooks/pre-push:46`, `exec pixi
run --locked gate`) and the three required checks on `main` (`gate`, `plugin`, `standards (every
group green)`; ruleset 24457138, read live) run ruff 0.16.10, mypy 2.4.0, pytest 9.1.1 under
typeguard 4.6.0, CrossHair 0.0.111 over z3-solver 5.1.0.0, complexipy 8.0.1, radon 6.0.1, bandit
1.9.4, coverage.py 7.16.2 and git 2.43.0 (all pinned in `pixi.lock` and confirmed by `--version`
in the locked environment), plus home-made code that is itself contracted and gated: the contracts
walk, the lines-of-code count, the Chidamber-Kemerer suite, the duplication detector, the
workflow-file reader, the baseline matching, the SARIF writer, the five boundary rules and the
pinned-copy digest.

Claude appears in exactly two places, neither of which can pass or fail anything: the plugin
(skills, the `stream` agent and the three workflows, where agents write code, contracts and repairs
that the same tools then judge), and as the *reader* of the `PostToolUse` coach hook, which runs the
tools and prints what CI would block (it never stops an edit; exit 0 on every path,
`plugin/hooks/coach.sh:15-20`). `claude plugin validate` in CI is a local manifest check: measured
to pass with an empty `HOME`, no key and the proxy pointed at a closed port.

Said plainly, in greg's terms: the QA is industry tools and deterministic code; the LLM only writes
what those tools then judge. The soft spots found are not Claude's but CrossHair's bound and two
home-made detectors (section 5), and six of them are decisions for greg (section 7). The one
number to carry away: a package-wide `gate --report-all` (10 min 4 s on four cores) shows that of
the 117 contract conditions over the 41 targets, 9 are proven over all paths and 107 are "Not
confirmed" at the 20 s bound (no counterexample found; bounded search, not proof), and 1 is
mislabelled vacuous. The plain gate's wording ("no counterexample within 20 s per condition") is
honest; the word "proof" in the plan and the documents is not, for 107 of 117.

## 2. What decides each verdict

Kind: **tool** = an established third-party tool decides; **code** = deterministic home-made code
in this repository decides (contracted, gated, no model); **tool+code** = the tool measures and
home-made code applies the limit or the glue. "Binds" says where a failure stops a change: the
pre-push hook (H), the required CI check (C), or advisory only (A).

| Check | What decides | Kind | Where | Binds |
| - | - | - | - | - |
| lint | ruff 0.16.10 `check` + `format --check` on `src tests` (honours `# noqa` and `[tool.ruff]`) | tool | `pixi.toml:68` | H, C `gate` |
| typecheck | mypy 2.4.0 `--strict` on `src` | tool | `pixi.toml:69`; `pyproject.toml` | H, C `gate` |
| tests | pytest 9.1.1, 202 tests, under typeguard 4.6.0's import hook | tool | `pixi.toml:70`; `tests/conftest.py:4-6` | H, C `gate` |
| gate check 1: every public function carries contracts; nothing hidden from CrossHair | import walk over the package; `__preconditions__`/`__postconditions__` set by icontract; a `# crosshair:` directive refused by regex; "imported from another checkout" refused | code | `gate.py:93-97` (public), `:142-157` (uncontracted), `:300` (has contracts), `:494-511` (directive), `:379-380, 533-537` (import origin) | H, C `gate` |
| gate check 2: no input meets a precondition and breaks a postcondition | CrossHair 0.0.111 + Z3 5.1.0.0, `python -m crosshair check <target> --analysis_kind=icontract --per_condition_timeout=20`, one process per target, `os.sched_getaffinity` at a time; the gate reads the exit code and two strings | tool+code | `gate.py:176-190` (argv), `:514-521` (jobs), `:627-642` (verdict; `_NOTHING_TO_CHECK` `:510`, `_VACUOUS` `:511`) | H, C `gate` |
| contracts and types | icontract 2.7.3, beartype 0.22.9, pydantic 2.13.5 (run time) | tool | `contracts.py:30`; `example.py:25-34` | through tests and the gate |
| readability: cognitive complexity 15 | complexipy 8.0.1 `--no-ignore`, from an empty directory | tool | `standards/readability.py:73, 200-201` | H, C `standards` |
| readability: cyclomatic 10, parameters 4 | ruff 0.16.10 `--isolated --ignore-noqa --no-cache`, C901 and PLR0913 | tool | `readability.py:73, 176-179` | H, C `standards` |
| readability: 25 lines of code in a body | tokenize + ast count (docstring, comments, blanks left out) | code | `readability.py:119-127, 218-259` | H, C `standards` |
| design: WMC 50 | radon 6.0.1 `cc --json` per-method McCabe, summed here | tool+code | `design.py:64, 279-292, 305` | H, C `standards` |
| design: DIT 5, NOC 10, CBO 14, RFC 50, LCOM4 1 | AST walk; union-find for LCOM4 | code | `design.py:63-70, 89-200, 295-314` | H, C `standards` |
| duplication: at most 3% of new lines in a block of 10 lines and 100 tokens | per-line token digests, windows of 10, identifiers as written | code | `duplication.py:37-39, 102-163` | H, C `standards` |
| coverage: at least 80% of new runnable lines | coverage.py 7.16.2 over the real pytest run, rcfile that excludes nothing; the new-line share computed here | tool+code | `coverage.py:46, 113-125, 277-283` | H, C `standards` |
| security: no new medium/high weakness | bandit 1.9.4 `-r -f json -q --ignore-nosec --ini <empty>`; CWE on every finding | tool | `security.py:50, 90-92, 117-118` | H, C `standards` |
| supply chain: pinned-action, pipe-to-shell, token-permissions (top level), untrusted-checkout, script-injection | PyYAML `safe_load` of `.github/workflows/*.yml` and regexes (Scorecard's three file checks, re-implemented) | code | `supply_chain.py:63-113, 126-298` | H, C `standards` |
| new-code rule (what blocks) | `git diff --unified=0` and `--name-status -M` for new lines and renames; findings matched by (rule, path, anchor) with `new`/`updated`/`unchanged` | tool+code | `newcode.py:33, 94-157`; `findings.py:61-150`; `run.py:52-54, 111-127` | through every group |
| SARIF 2.1.0 logs | home-made writer; validated against the OASIS schema with jsonschema 4.26.0 in the tests; kept as run artifacts for 30 days; the tool versions in them are read from each tool's `--version` at run time | code | `sarif.py:30, 116-141`; `group.py:91-96`; `standards.yml:69-76` | A (format only) |
| boundary (interface standard, rules 1-5) | regexes over tracked lines, pydantic models of `INTERFACE.json`, sha256 of each pinned copy, imports against the provider's export, qa <- agents <- research | code | `boundary.py:143-211, 259-548, 711-816` | H (gate task); C through `tests/test_boundary.py:391-395` |
| vendor / vendor-check | `gh api` through the person's own sign-in; ORIGIN with per-file sha256 and a tree digest; kit byte-equality and mode 100755; no tracked `__pycache__` | tool+code | `vendor.py:146-155, 341, 445-448, 588-623` | consumers' H and C |
| coach (PostToolUse hook) | the cheap groups (readability, design, duplication, security; supply chain for workflow files; never coverage) on the edited file, printed as `decision: block` + reason | code | `standards/coach.py:40-46, 68-170`; `plugin/hooks/coach.sh:15-20` | A (exit 0 always) |
| plugin lane in CI | `claude plugin validate` (manifest shape, local), `node tools/check_workflows.mjs` (the runtime's script rules by text, both grammars via `node --check`), `node --test` (36 tests under stand-in hooks) | tool+code | `ci.yml:74-84`; `tools/check_workflows.mjs:2-45` | C `plugin` |
| merge rule | GitHub ruleset as code: three required contexts, deletion and force-push blocked, `strict_required_status_checks_policy: false`, OrganizationAdmin bypass; auto-merge armed by `automerge.yml` only when the rule exists | tool | `.github/rulesets/main.json:30-44`; `automerge.yml` | C |

Every entry was checked by a second agent against the file; three citations it corrected are in
section 10.

## 3. Where Claude is in the loop, and what it can and cannot do

- **The plugin's skills** (`plugin/skills/`, five of them) tell a session how to write to the
  definition of done and the standards. Text only; nothing runs.
- **The `stream` agent** (`plugin/agents/stream.md`) and **the three workflows**
  (`gate-until-green.js`, `verify-module.js`, `improve-module.js`): agents write code, contracts,
  tests and repairs; the oracle they are driven by is `pixi run --locked gate` or
  `python -m beethoven_qa gate --module <m> --report-all`. Inside a workflow run the `proven` /
  `green` fields are the agent's structured transcription of the gate's output (a workflow script
  cannot run a command itself), so a lying agent could end a workflow early; it cannot push, because
  the pre-push hook and CI run the gate again, independently. The two vacuity skeptics in
  `improve-module` are advisory.
- **The coach hook**: the model's edit is the input, the tools' findings are the output; the model
  reads them. Measured by hand here with the documented JSON: a tangled function answered
  `decision: block` with the four readability findings in 3.6 s (under load; 2.8 s documented); the
  clean tree answered nothing. Never seen inside a live Claude Code session (not measured).
- **The gate and the standards never read model output.** Searched `src/` for anything that calls
  `claude`, a model API or reads a transcript: nothing. The only network calls in the package are
  `gh api` in `vendor.py` (the person's sign-in) and none in CI.
- **Bypasses that exist, by design and written down:** `SKIP_GATE=1` (`pre-push:7-10`),
  `git push --no-verify`, the OrganizationAdmin bypass on the ruleset. None involves a model.

## 4. Broken on purpose: what each check reported

All in a scratch clone of `b73d4f4`, each with a control run on the untouched clone (every control
passed). Durations are from this box with the full gate running beside them, so they are upper
estimates.

| Planted | Reported | Caught | s |
| - | - | - | - |
| `tangled(a..f)  # noqa` with nested loops, 6 parameters, 29 body lines; then a root `ruff.toml` ignoring C901 and PLR0913 | `readability: FAILED … 4 of them new or worse`: cognitive 43 > 15, cyclomatic 15 > 10, parameters 6 > 4, length > 25; `ruff.toml` changed nothing | yes | 2.0 |
| classes L1..L7 each subclassing the last; a class whose methods split into two unconnected parts | `design: FAILED`: DIT 6 and 7 > 5 on L6, L7; LCOM4 2 > 1 on `Split` | yes | 2.0 |
| one 14-line body copied three times | `duplication: FAILED: 42 of 45 new lines lie in a duplicated block (at most 3%)`, one finding per copy | yes | 1.0 |
| `subprocess.run(cmd, shell=True)  # nosec`, `eval(s)  # nosec`, plus a root `.bandit` with `skips: B102,B602,B605` | `security: FAILED`: B602 high CWE-78 and B307 medium CWE-78, both `(new)`, nosec and the skips file ignored | yes | 3.2 |
| `on: pull_request_target`, `actions/checkout@v4` of the PR head, a download piped into `sh`, `echo ${{ github.event.pull_request.title }}`, job-level `permissions: write-all` | `supply-chain: FAILED: 5 workflow findings`: token-permissions (no top-level block), pinned-action, untrusted-checkout, pipe-to-shell, script-injection | yes | 0.8 |
| a public contracted function with no test (33 new lines) | `coverage: FAILED: the tests ran 4 of 29 new lines that can run (at least 80%)`; after one test: `29 of 29`, passed | yes | 209 / 228 |
| a tangled function through the coach hook's JSON | `{"decision": "block", "reason": "… would block this change in CI …"}` with four findings; clean tree: silence | yes | 3.6 |
| `remaining()` postcondition changed to `0 <= result < cap` | CrossHair: `example.py:40: error: false when calling remaining(0, 1) (which returns 1)`; gate exit 1 | yes | 1.0 |
| a public function with no contracts | `gate: public functions without contracts (nothing to prove): - beethoven_qa.example.naked`; exit 1 | yes | 1.1 |
| `# crosshair: off` on a contracted function | CrossHair itself exits 0 with only a WARNING; the gate refuses twice (`directive src/…/example.py:32`, and "found nothing to check"); exit 1 | yes | 1.1 |
| a precondition no input can meet, with `--report-all` | `info: Unable to meet precondition.` → `gate: … a precondition no input can meet (a vacuous contract)`; exit 1 | yes | 1.3 |
| **the same, with the plain gate (what the hook and CI run)** | `gate: no counterexample within 20 s per condition`; **exit 0** | **no** | 1.3 |
| the consumer beethoven-agents (pinned v3.0.0): install, vendor-check, boundary, standards all, gate on `guard` | `pixi install --locked` 1.1 s warm; `vendor-check … matches its ORIGIN (v3.0.0, 08aca99)`; `rules 1 to 5 hold`; standards on the whole tree (no base) readability 48, design 3, security 4 medium, duplication 0, coverage 93.6 %; `guard` 5 targets no counterexample (92 s); six SARIF files, 0 schema errors; nothing tracked changed | n/a | 58 / 92 |

## 5. What the tools miss (found here, not in the repository's own notes)

1. **The plain gate does not see a vacuous precondition.** CrossHair prints "Unable to meet
   precondition." only under `--report_all`; `pixi.toml:74` `symbolic = "python -m beethoven_qa
   gate"` runs without it, and so do the hook and `ci.yml:52`. The flag appears only in the plugin's
   skills and workflows, which an LLM drives. A contract nobody can satisfy passes every push today.
2. **Turning `--report-all` on would fail main's own code at `standards.security.level_for`**
   (`security.py:56`, `{severity, confidence} <= set(_GRADES)` over two `str`). The precondition is
   satisfiable (the tests call it with `'HIGH','MEDIUM'` and so on); CrossHair 0.0.111 cannot build
   symbolic strings that pass a set-containment test within the bound (60 s gave the same), and the
   gate's `_VACUOUS` match cannot tell a tool limit from a contract fault because CrossHair prints
   the same text for both. Today the plain gate passes `level_for` without ever exercising its
   postconditions, and `gate --report-all` over the whole package exits 1 for this one target and
   no other (measured, 10 min 4 s), so `verify-module`'s Prove phase would refuse that module.
3. **"Not confirmed" at the bound counts as a pass and is not counted.** Measured over the package
   with `--report-all`: 117 conditions over 41 targets, 9 `Confirmed over all paths` (the five in
   `example.py`, `gate.py:94`, `standards/coverage.py:88`, `standards/duplication.py:119,122`), 107
   `Not confirmed` at the 20 s bound, 1 `Unable to meet precondition` (`security.py:56`). The gate's
   last line is honest ("no counterexample within 20 s per condition", never "proven") but prints
   no count, so a reader of the plan's "symbolic proof" does not know that for this package it is
   bounded search for 107 of 117 conditions. `CLAUDE.md:324-325` and `docs/STANDARDS.md:169` still
   say 32 targets; there are 41.
4. **The duplication floor lets a 13-line verbatim copy through on Python.** At 8.6 tokens per
   line on this package, ten lines hold about 86 tokens, under `MIN_TOKENS = 100`
   (`duplication.py:38`); jscpd 5.4.0 and pylint R0801 both report the same copy at 10 lines.
   SonarSource's "100 tokens" was written for its own tokeniser, not Python's `tokenize`.
5. **The supply-chain reader cannot see two unpinned downloads in the kit itself.** OpenSSF
   Scorecard 5.5.0 `--local` reports `npm install -g @anthropic-ai/claude-code@…` at `ci.yml:74` as
   unpinned, and the pixi binary is fetched by version name with no checksum in `ci.yml:38-40`,
   `standards.yml:43-45` and `.claude/hooks/session-start.sh`; `supply_chain.py:101` flags only a
   download piped straight into a shell. A job-level `permissions: write-all` is also never a finding
   (top level only, by design, `supply_chain.py:207-218`).
6. **`main`'s merged tree is never re-checked.** `strict_required_status_checks_policy` is `false`
   (`rulesets/main.json:30`), so a pull request green against an older `main` can merge without a
   re-run, and the merge commits on `main` (`b73d4f4`, `615ed3e`, by github-actions[bot]) show no
   `ci.yml` or `standards.yml` run although both declare `on: push: branches: [main]` (read live with
   `gh run list`; GitHub starts no workflow for a push made with `GITHUB_TOKEN`). With one pull
   request open at a time the risk is small; it is still a hole in "the tests decide".
7. **Smaller, in the lanes the tools own:** the lint lane honours `# noqa` and `[tool.ruff]` (only the
   readability group runs ruff `--isolated --ignore-noqa`); mypy honours `# type: ignore` (with
   `warn_unused_ignores`); nothing detects a `skip`/`xfail` mark (none exists at HEAD); the LSP rule
   (BUILD_PLAN item 2) is icontract's run-time rule for `DBC` subclasses only, and no test or gate
   check pins it; a function leaves check 1 by being renamed `_private` (a reviewed-change control,
   not a mechanical one).

## 6. What is left

### Against BUILD_PLAN §3 (G1, the definition of done)

| Item | State | What it would take |
| - | - | - |
| 1 deterministic environment | lock done (linux-64 on purpose; the plan says multi-platform); image never built on the grid (`beethoven-agents/containers/`: no `claude-verify.digest`, README "No grid build yet"; the CI image lane built one on a runner in 11 min and discarded it); the recipe itself is not reproducible: `claude-verify.def:47` pipes the nodesource script into bash, `:50` installs `@anthropic-ai/claude-code` unpinned, `:56-57` fetches pixi with no checksum | one `sbatch containers/build.sh` on a compute node and the digest committed (BEE-103), and the three fetches pinned (agents' lane) |
| 2 Design by Contract, LSP | contracts done and gated; LSP unenforced beyond icontract's run time for `DBC` subclasses | a gate check that a contracted class uses `DBC`, or a test of weaken/strengthen, or a recorded "run time only" |
| 3 layered runtime types | done (`conftest.py:4-6`, `contracts.py:23-42`, `example.py`) | nothing |
| 4 symbolic proof | done as bounded search: 9 of 117 conditions proven over all paths, 107 not confirmed at the bound, 1 mislabelled vacuous (section 5.2, 5.3) | a count on every run; `level_for` restated or listed; the documents' "proof" qualified |
| 5 schema-aligned parsing (BAML/SAP) | not built (`CLAUDE.md:101`; `verify-module.js:304` uses the runtime's structured output, which is not coercive repair) | a contracted, gated module with its tests; an entry in `interface/python.json` if consumers import it |
| 6 SpecPylot loop | exists as three workflow scripts; 36 tests under stand-in hooks pass; never run against a real failure (`docs/PARALLEL_BUILD.md:196-197`) | one live run of `verify-module` on a planted false postcondition, its transcript and the gate's before/after recorded |
| 7 gate before every push, required check, auto-merge | done on the repository half: rulesets read live (`gh api`) for qa 24457138, agents 24460184, research 24440691, desktop 24440600, sites 24476823, base 24731845, each requiring what its `main.json` names, and bot merges in qa, research, desktop and agents; the in-run half ("a module that fails verification cannot enter a run") has no orchestrator to live in yet (D3, agents) | nothing here; the strict-policy decision of section 7; the in-run gate with the orchestrator |
| plugin loaded by the image's managed settings | not measured; the image carries v3.0.0, which has no hooks | after the re-pin and a rebuild: one session in the image that edits a file and shows the hook's answer |
| repository half in hpcworker, the TypeScript clients | hpcworker and beethoven-extension: `ci.yml` only, actions by tag, hand merges, no hook, ruleset or automerge; beethoven-vscode: no workflow at all and `CODEOWNERS` requires review; desktop, sites, base: hand copies of the kit with differing bytes, no `standards.yml` or `session-start.sh`, no record of which release they came from | per repository: a hook running its own suite, `rulesets/main.json` naming its jobs, the kit's two workflows, actions pinned by commit; vscode also a CI workflow; the three hand copies an ORIGIN record |

### Against greg's Drive document "Auditable Code Quality Standards"

Done, as the document names them: cognitive complexity with nesting penalties (complexipy, 15);
McCabe cyclomatic (ruff C901, 10); the CK suite with DIT > 5; LCOM4; Code Climate's 25 lines and
4 arguments; Sonar way's 3 % duplication and 80 % coverage on new code and "no new vulnerability";
CWE on every security finding; SARIF 2.1.0 validated against the OASIS schema; Scorecard's
Pinned-Dependencies, Token-Permissions and Dangerous-Workflow as file checks; merge protection on
findings (as a ruleset in code rather than GHAS).

Chosen differently, and worth one sentence each in `docs/STANDARDS.md` so a reader of the document
is not surprised: cyclomatic 10 (McCabe) rather than Code Climate's 5; LCOM4 as connected parts
with limit 1 (the document names LCOM4 itself; only its 0..1 normalisation is not computed); WMC
50, NOC 10, RFC 50 "chosen here" with no literature source (`design.py:64,66,68`); cognitive
complexity 15 per function and no per-class sum, where the document's example is a pipeline that
"will physically reject" a class with a cognitive complexity of 40 (stricter per function, nothing
per class); duplication at the token level with identifiers as written (a renamed copy is not a
copy), not AST-normalised as Code Climate's; the limits live as constants in the pinned copy's
code, not in a visible `.codeclimate.yml`; ISO/IEC 25010 characteristics are the rule tags
(`maintainability`, `testability`, `security`) but the standard is never named; the SARIF tool
versions are strings read from `--version` at run time, not the document's "cryptographic"
identification.

Not built, and not in the repository's own "What is not here" list: the size-confounding critique
(CK metrics as ratios to size); "maintainability A" and "0 new bugs" as such (the bug condition is
the whole-tree lint and mypy lanes, which is stricter).

Out of scope by decision, with the reason standing: Buse-Weimer and Scalabrino readability models
(no maintained open implementation found 2026-10-04; not re-checked here); ISO/IEC 5055's own
weakness list (commercial, not reproduced); GHAS `upload-sarif` (needs Code Security on a private
repository); Scorecard's settings checks, Code-Review among them (no human review gate, greg's
decision); nesting-depth and boolean limits (PLR1702 and PLR0916 are still preview rules in ruff
0.16.10, measured here with `ruff rule`); SonarQube, Code Climate, GHAS as services (a token).

### Against Linear (G1 project P-BEE-7; read today through the Linear MCP)

| Issue | Linear says | The code says |
| - | - | - |
| BEE-105 DbC base + LSP | Backlog, blocked by BEE-102/103 | built without the image; Done (or In Progress for the LSP test) |
| BEE-106 layered types | Backlog | built; Done |
| BEE-107 CrossHair + Z3 harness | Backlog | built and measured; Done, with the note that "Not confirmed" at the bound is accepted |
| BEE-108 schema-aligned parsing | Backlog | correct |
| BEE-109 SpecPylot loop | Backlog | three tested scripts, never run live; In Progress |
| BEE-110 gate before every push (P0) | Backlog; its text names the gate as ruff, mypy, pytest, CrossHair, and asks for the in-run pipeline gate too | the repository half is built in four repositories with live rulesets and bot merges; the gate also runs boundary and standards; the in-run half waits on the orchestrator (D3); Done for the repository half, with a comment |

### Versions and consumers

- 4.0.0 is on `main` (`pyproject.toml:7`, `__init__.py:15`, `plugin.json:3`) with no `v4.0.0` tag.
  `vendor` does not refuse an untagged commit; it records `untagged` in ORIGIN (`vendor.py:481`,
  `docs/CONSUMING.md:137-139`), and "tagged releases only" is a reviewer's rule, not code. The tag
  is greg's hand step.
- beethoven-agents (`a40a71a`) and beethoven-research (`7e8fd69`) pin v3.0.0 (`08aca99`, 41
  files): no `coach.py`, no `plugin/hooks/`, no PostToolUse line in their `.claude/settings.json`.
  The kit's five files are byte-identical at v2.0.0, v3.0.0 and HEAD, so `--kit` changes nothing on
  the re-pin. `beethoven-agents/containers/managed-settings.json:14-15` says "no hooks", true for
  v3.0.0 and stale at the re-pin. The re-pin and that comment are the outside lanes' (handed to the
  coordinator).
- Records that disagree with the code: `LINEAR_BREAKDOWN.md:41` puts G1 in beethoven-research
  (it is beethoven-qa); `BUILD_PLAN.md:100-101` says a multi-platform lock (linux-64 on purpose);
  `/mnt/project-files/state/repos/beethoven-qa.md` describes 2026-10-04; in beethoven-qa itself
  `docs/STANDARDS.md:167` ("45 s of it the coverage group"; now 3 min 30 s locally, 2 min 22 s on
  GitHub), `docs/STANDARDS.md:169` and `CLAUDE.md:324-325` ("32 targets"; 41), `docs/STANDARDS.md:
  191-193` and `docs/CONSUMING.md:755-756` ("not yet measured" on GitHub's runners; measured, next
  paragraph), `docs/CONSUMING.md:757-759` ("the boundary lane in no consumer's gate or CI yet";
  beethoven-agents' `pixi.toml:101` chains it and its run passed).

### Measured on GitHub's runners (read live with `gh run view`; the CLI works through the proxy, only the GitHub MCP server fails)

- beethoven-qa run 37777430848 (2026-10-08 12:31Z, PR #7's head): every standards group green,
  coverage 2 min 22 s; gate lane 37777430807 20 min 51 s, plugin lane 18 s.
- beethoven-agents run 37678144309 (2026-10-07 19:55Z, "Re-pin beethoven-qa 3.0.0"): every group
  green, readability 20 s, design 13 s, duplication 16 s, coverage 34 s, security 16 s, supply
  chain 13 s; gate lane 37678144326 11 min 2 s, image lane 11 min 0 s.
- beethoven-research run 37677381794 (2026-10-07 19:49Z): every group green, coverage 14 s; gate
  lane 37677381788 1 min 59 s.

## 7. Decisions for greg

Each with the recommended course first, why, then the alternatives. Any change to beethoven-qa goes
up as a pull request that merges itself on green (the convention), after telling the coordinator.

**D1. Make the plain gate run `--report-all`, so a vacuous precondition fails a push and CI
(section 5.1).** Recommended. It is one flag in `pixi.toml:74`; the hook and `ci.yml:52` follow.
It needs `level_for` restated first (section 5.2): its grades as a `Literal` type or an enum so
CrossHair never has to build the strings, or the function listed under `unproven` with the
CrossHair fault as its reason; `level_for` is the only target on main that returns "Unable to meet
precondition." (the package-wide run of section 5.3), so nothing else changes. Alternatives: (a)
leave the plain gate as is and keep the vacuity check to the LLM-driven workflows, accepting that a
push never sees it; (b) have the gate run `--report_all` only for the count of D2 and keep vacuity
advisory; (c) a test with a satisfiable string precondition plus a vacuity check that tolerates
"Unable to meet precondition" at the bound (weaker: it would also tolerate a real vacuous one).

**D2. Report the "Confirmed over all paths" / "Not confirmed" count on every gate run (section
5.3).** Recommended, with D1 (the verdicts are only printed under `--report_all`): a summary line
like `gate: 9 of 117 conditions confirmed over all paths, 107 not confirmed within 20 s` costs
nothing and makes the bound visible; and the plan's and documents' word "proof" is then qualified
once, in `CLAUDE.md`'s "Measured" section, with that count. Alternatives: record the count once in
CLAUDE.md and leave the gate's output alone; or raise `per_condition_timeout` for the
string-and-tuple conditions (slower pushes, same uncertainty).

**D3. Replace the duplication detector with jscpd 5.4.0 (section 5.4).** Recommended: MIT, binary
wheel on PyPI (no conda-forge package; it enters the lock as a pypi dependency like crosshair-tool),
JSON and SARIF out, `--min-lines 10 --min-tokens 100`, caught the 13-line copy; keep `new_lines`
and `within_limit` for the 3 %-of-new-lines density, which jscpd does not report; the contracted
`repeated` becomes the reader's test oracle or goes. Alternatives: (a) keep the detector and
re-derive `MIN_TOKENS` against jscpd's count on Python (the minimum); (b) pylint R0801 (GPL, a
second large tool beside ruff, no token minimum, no density); (c) PMD CPD (needs a JVM, no SARIF).

**D4. Run zizmor beside the supply-chain reader, and Scorecard's Pinned-Dependencies in CI on a
clean checkout (section 5.5).** Recommended: zizmor 1.30.1 (conda-forge, MIT, `--offline
--no-ignores`, SARIF; covers four of the five rules with wider coverage and refuses its own ignore
comments, which fits the no-suppression rule) as an independent auditor in the `supply-chain` job,
keeping the reader for its per-anchor new-code matching and the pipe-to-shell rule; Scorecard
5.5.0 (conda-forge, Apache-2.0, 79 MB Go binary) only in CI, since `--local` walks ignored files
and reported "possibly incomplete results" on a working tree with `.pixi/`. Independently of the
tools: a sha256 check of the pixi binary in the three places the kit fetches it; the `npm install
-g @anthropic-ai/claude-code@<version>` at `ci.yml:74` is pinned by version and a global install
has no lockfile to pin a hash with, so that one is recorded as accepted rather than fixed.
Alternatives:
only the checksum (closes the two downloads, leaves the reader as the sole auditor); only zizmor
(cheapest); actionlint 1.7.12 as a third, for workflow syntax the reader passes silently
(`supply_chain.py:269-272` returns nothing on a YAML error).

**D5. Make the required checks strict (`strict_required_status_checks_policy: true`, section
5.6).** Recommended only if a branch update can be automated: with it on, auto-merge waits until the
branch carries `main`'s head, which GitHub does not do by itself; `automerge.yml` would need an
update-branch step (one `gh pr update-branch` on the same GITHUB_TOKEN, which then does trigger the
pull request's checks). Alternative: leave it false and accept that a merged `main` is checked only
through the pull request's merge commit at the time of its last run (today's state; small risk with
one pull request at a time).

**D6. Replace the lines-of-code counter with lizard 1.24.1.** Optional. lizard (conda-forge, MIT)
computes NLOC per function and agreed with the home-made count on every flagged function to within
the `def` line and the nested-body convention; it would replace about 45 lines of tokenizer code
with a tool read. Alternative: keep the counter (it is contracted and gated, and the definitional
difference would move the limit by one line).

Kept as home-made after the search, with the reason: the CK suite (no open Python tool computes it
with LCOM4; `design.py:4-6`), the boundary rules 1-3 and the pinned-copy digest (submodules and
template tools need the token the project forbids), the baseline matching (diff-cover and
sarif-tools are line-based; bandit and semgrep baseline only their own output; ruff has none).
Cross-checks worth adding at low cost: import-linter 2.15 `layers`/`forbidden` contracts beside
boundary rules 4-5; diff-cover for the coverage group's new-line share; bandit's own `--baseline`
for the security group.

## 8. The open-source alternatives, as run

| Home-made check | Established tool tried | Verified by | Result |
| - | - | - | - |
| lines of code per function | lizard 1.24.1 (`-T nloc=26 -w`); ruff PLR0915 (statements); flake8-functions CFQ001; radon raw | running each on this package | lizard's five warnings match the home-made four plus `_preflight` 31 (def line counted, nested bodies listed apart); PLR0915 counts statements, a different quantity; CFQ001 counts physical lines; radon raw is per file |
| CK suite | none open for Python (ck, ckjm are Java; Understand, CodeMR, Designite commercial); pylint R0901/R0904; cohesion 1.2.0 | web search and runs | nothing to adopt; pylint approximates two of six with different definitions (GPL); cohesion reports a percentage with the opposite reading for an empty class |
| duplication | jscpd 5.4.0; pylint R0801; PMD CPD 7.19.0; copydetect 0.5.0 | running on the package and on a synthetic copy | jscpd 0 clones on the package at Sonar's settings (agrees), 1 clone of 14 lines on the synthetic file; the 13-line copy: jscpd and pylint catch it, the home-made does not |
| workflow reader | Scorecard 5.5.0 `--local`; zizmor 1.30.1; actionlint 1.7.12; pinact 5.0.0 | running the first three | Scorecard found the unpinned npm install and the pixi download; zizmor found artipacked, dangerous-triggers, template-injection, unpinned-uses on the synthetic file and nothing new on the kit; actionlint exit 0 |
| boundary and vendor-check | git submodule, git subtree, cargo vendor / go mod verify (precedents), pypa vendoring, cruft/copier, sha256sum -c, import-linter 2.15 | runs and documentation | no token-free equivalent of ORIGIN plus kit check; import-linter expresses rules 4-5 as contracts |
| baseline matching | diff-cover / diff-quality 10.6.0; bandit `--baseline`; semgrep `--baseline-commit`; complexipy `--diff`; sarif-tools `sarif diff`; mypy-baseline | runs | all line-based or tool-specific; none gives "worse than base" by qualified-name anchor across tools |

No paid or hosted service was a candidate; none is named as one.

## 9. Not measured

- The gate, the standards groups and the coach hook on a grid node, or on any machine without the
  background gate's load; every local duration above is from this four-core container (the GitHub
  figures in section 6 are the runners').
- The coach hook inside a live Claude Code session, and under the image's `allowManagedHooksOnly`;
  a repository's own `.claude/skills/` plugin in a cloud thread; the plugin installed from the
  private GitHub marketplace on greg's laptop and its update after a version change
  (`docs/CONSUMING.md:751-753`).
- Any workflow of the plugin against a real failure; whether Claude Code's own loader accepts the
  three scripts (only emulated by `tools/check_workflows.mjs`).
- The image build on the grid (agents' lane).
- Whether a maintained Buse-Weimer or Scalabrino implementation has appeared since 2026-10-04.
- The Drive document end to end: 44,174 characters of its text were extracted and keyword-searched;
  its finer sentences may hold more than quoted here.

## 10. Method and corrections

Twelve agents under one workflow on four cores (two at a time): five readers (gate; standards;
boundary and vendor; plugin; kit and consumers), four breakers (standards groups; the gate; coverage
and coach; the consumer beethoven-agents), one gap finder, one alternatives runner, three skeptics
(the tool table; the no-model claim; the gap list). Every reader's claim carries a file and line;
every breaker's claim carries the command and its output; every alternative was run, not recalled.
The full gate ran on main in the background throughout (green, 16 min 55 s).

Corrections the skeptics made before this was written: `plugin/hooks/coach.sh` is 20 lines (cited
as `:30-37`, now `:15-20`); the "broken on purpose" sentence is at `docs/STANDARDS.md:173-174`;
the kit's pinned `uses:` lines are `ci.yml:33, 66, 69` and `standards.yml:36, 71`; `_VACUOUS` is
`gate.py:511` (matched at `:635-636`) and `_NOTHING_TO_CHECK` `:510` (`:633-634`);
`security.py:56` is the `@require` (55 is `@beartype`); "mixed" was replaced by "tool+code" with
the deciding tool named. The gap skeptic overturned four "not measured" entries by measuring them
(the package-wide `--report-all` count, the consumers' GitHub runs, ruff's preview rules, the Drive
document's "cognitive complexity of 40" sentence), found that `gh` answers through the proxy
although `gh auth status` calls its token invalid (only the GitHub MCP server fails), corrected
"vendor refuses an untagged ref" to "records `untagged`", and re-cited eleven kit and settings
files whose first draft pointed past their last line. Where the brief suggested running main's
checker against the clone (`--root`), the gate refused by design ("was imported from … not from …",
`gate.py:380`), which is the "package imported from another checkout" escape working; the breakers
ran the clone's own, byte-identical, code instead.

Beethoven runs Claude Code and is not an Anthropic product; "Claude" and "Claude Code" are
Anthropic's marks, used here to say what it runs.

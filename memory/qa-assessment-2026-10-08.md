---
name: qa-assessment-2026-10-08
description: beethoven-qa 4.0.0 assessment (Oct 8): verdicts are tools + deterministic code, no model; 9 of 117 conditions proven, 107 bounded; the gaps found and the six decisions waiting on greg
metadata:
  type: project
  modified: 2026-10-08T17:27:13.172Z
---

The qa thread's assessment of beethoven-qa main b73d4f4 (4.0.0, untagged) is at
/mnt/project-files/qa/QA_ASSESSMENT_2026-10-08.md (per-check table, planted-violation results,
alternatives run, GitHub run timings, what is left). Delivered to greg 2026-10-08 17:28Z. Headline,
verified by three skeptics: every blocking verdict (pre-push gate, the three required checks) comes
from ruff, mypy, pytest/typeguard, CrossHair+Z3, complexipy, radon, bandit, coverage.py, git, or
contracted home-made code; Claude only writes what those judge (plugin workflows, coach hook reader).

Gaps found there, not in the repo's own notes:
- The plain gate (pixi.toml:74, hook, ci.yml:52) runs without `--report-all`, so a vacuous
  precondition passes every push; only the LLM-driven workflows use the flag.
- `gate --report-all` over the package (10 min, 4 cores): 117 conditions, 9 confirmed over all
  paths, 107 "Not confirmed" at 20 s, 1 "Unable to meet precondition" = main's own
  `standards.security.level_for` (security.py:56; CrossHair 0.0.111 string limit the gate
  mislabels as vacuous). So "symbolic proof" is bounded search for 107 of 117; docs say 32
  targets, there are 41; STANDARDS.md:167 "45 s coverage" is now 3m30s local / 2m22s on GitHub.
- Duplication's MIN_TOKENS=100 lets a 13-line verbatim Python copy through (~8.6 tokens/line);
  jscpd 5.4.0 and pylint R0801 catch it.
- The supply-chain reader misses the unchecksummed pixi download (ci.yml:38-40, standards.yml:43-44,
  session-start.sh:26-27) and job-level write-all; Scorecard --local and zizmor see more.
- strict_required_status_checks_policy is false and merge commits on main get no workflow run.
- `gh` CLI answers through the proxy in these sessions although `gh auth status` says the token is
  invalid; only the GitHub MCP server fails (403). Rulesets live: qa, agents, research, desktop,
  sites, base; none on hpcworker, extension, vscode.

Decisions put to greg (D1-D6 in the file): --report-all in the plain gate (after restating
level_for), a confirmed/not-confirmed count per run, jscpd for duplication, zizmor + a pixi
checksum, strict checks, lizard for LOC. Not changed in qa until he answers.

**Why:** any thread touching beethoven-qa or its consumers should know these before trusting a
green gate or re-deriving them.
**How to apply:** read the file before changing gate.py, duplication.py or the kit; consumers'
re-pin to v4.0.0 waits on greg's tag (see [[qa-code-standards]], [[project-hub-export]]).

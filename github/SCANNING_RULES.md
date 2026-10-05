# The scanning, quality, coverage, secret and Copilot rules: what each needs

greg's question (engine skeleton thread, 2026-10-04 02:47Z): why the main rule skips GitHub's
"Require code scanning results", "Require code quality results", "Restrict code coverage" and
"Require secret scanning alerts are resolved", and the optional "Automatically request Copilot code
review". Written 02:58Z by the skeleton thread; every fact below was read from GitHub's own pages on
2026-10-04 (the available-rules page, the rulesets REST reference, the Advanced Security billing
page, the changelogs of 2025-03-04, 2025-04-01 and 2026-07-13, the Copilot plans page) or read back
from the repository with `gh api`.

## The short answer

Each rule needs a GitHub product that is **off** on this repository, and the repository is
private, so none of them is free. Read back at 02:50Z from `repos/OpenSpineConsortium/beethoven-research`:
`code_security: disabled`, `secret_scanning: disabled`, `secret_scanning_push_protection: disabled`;
the code-scanning setup endpoint answers `403 Code Security must be enabled for this repository to
use code scanning`. A scanning rule ticked while its product is off does not sit idle: the rule
page says it blocks when "a required tool is not configured for the repository", so every pull
request would be stuck. That is why `main.json` carries the gate and the image lanes and nothing
else today.

## What each rule needs, and costs

| Rule | Needs | Price (per active committer per month) | Here now | As code? |
| - | - | - | - | - |
| Require code scanning results | code scanning with CodeQL, which on a private repository means **GitHub Code Security** | **$30** (changelog 2025-03-04; on GitHub Team since 2025-04-01) | off | yes: `code_scanning` with the tool `CodeQL` and two thresholds |
| Require code quality results | **GitHub Code Quality** (repository Settings → Code quality → Enable; CodeQL runs on Actions minutes; Python is supported) | **$10** since general availability on 2026-07-20 (free during the preview before it; changelog 2026-07-13) | off | yes: `code_quality` with `severity` errors, warnings, notes or all |
| Restrict code coverage | Code Quality on **and** a Cobertura XML coverage report uploaded from CI | included in Code Quality | off; CI runs pytest without coverage | yes: `code_coverage` with `minimum_coverage` and `max_coverage_drop`; the rule is in public preview |
| Require secret scanning alerts are resolved | secret scanning, which on a private repository means **GitHub Secret Protection** (it also brings push protection) | **$19** | off | **no**: the rulesets REST body has no secret-scanning rule type (read 2026-10-04), so it is a click in the ruleset's page and cannot live in `main.json` yet; the rule is in public preview |
| Automatically request Copilot code review | **excluded** (greg, 2026-10-04 13:27Z: "no api key anywhere thats the only fundamental rule of this software"): it needs the author's Copilot plan or the organization paying each review as GitHub AI Credits, which is paid AI usage | per plan; AI credits | not set, never | the rule type exists (`copilot_code_review`), and `ruleset-main-copilot-review-beethoven-research.json` beside this note stays as the record of what was looked at; it is not to be imported |

**Active committers.** Counted once across the organization, for 90 days after a commit of theirs
is pushed, whatever the repository. This repository's commits carry the author and committer
`Claude <noreply@anthropic.com>` and are pushed through your account, so expect the count to be
**two** (you and that address), not one; GitHub shows the number before you confirm enablement.
At two committers: Secret Protection $38, Code Security $60, Code Quality $20, about **$118 a
month** for all three, plus the Actions minutes CodeQL uses (a GitHub Team organization has
3,000 minutes a month included for private repositories).

## What fits the convention

Your rule of 02:11Z is that whether a change lands is decided by tests, with no human step. All
four blocking rules are that kind of verdict, so they belong in `main.json` as soon as their
products report results on `main`. In the order of value for this engine:

1. **Secret Protection.** Push protection refuses a push that carries a secret, which turns the
   project's "secrets never enter the repository, a job file or an argv" from a promise into a
   check at the gate. The merge rule on top is a click in the ruleset page.
2. **Code Quality with the coverage rule.** The gate runs the tests but has no coverage floor; a
   floor and a no-drop rule are exactly a test-determined merge rule. It needs one CI change:
   `pytest-cov` added to the pixi lock (re-solved with pixi, never hand-edited), the Cobertura
   report written by the test lane, and the upload step GitHub's "Set up code coverage" how-to
   names (the page was not readable at the address I tried; read from the Code Quality how-to index
   once the product is on).
3. **Code Security.** CodeQL's security queries on the Python the engine will run with shell
   access are worth having beside ruff and mypy, and Goal 4 is a security boundary. It overlaps
   with ruff on style, not on injection and path handling.
4. **Copilot review**: excluded under greg's rule of 13:27Z (paid AI usage, as AI credits or a
   Copilot plan); the three products above are GitHub's scanning, not AI usage, and stay on the list.

## In which order, so nothing blocks by accident

1. Organization settings → Advanced Security (or the Security tab) → turn on Secret Protection and
   Code Security for `beethoven-research` (and `beethoven-desktop` if you want them there too; the
   committer count does not grow with repositories). Repository Settings → Code quality → Enable
   (Python; GitHub-hosted runners).
2. Let one run finish on `main` so each product has results for the base branch (the code scanning
   rule needs results "for both the commit and the reference being updated").
3. Say so in the thread; the skeleton thread then moves the three rules into
   `.github/rulesets/main.json`, adds the coverage report to `ci.yml`, and you import the updated
   ruleset (or the rulesets workflow applies it once `RULESETS_TOKEN` exists). Until then the
   import-ready proposal is `ruleset-main-scanning-beethoven-research.json` beside this note, a
   separate ruleset so it can be imported after the products are on without touching the one
   already prepared; its coverage rule says only "coverage may not drop" (no minimum), because the
   package's line coverage is not yet measured and a wrong floor would block every merge.
4. Tick "Require secret scanning alerts are resolved" in that ruleset's page (no API shape yet).

Beethoven runs Claude Code and is not an Anthropic product; "Claude" and "Claude Code" are
Anthropic's marks, used here to say what it runs.

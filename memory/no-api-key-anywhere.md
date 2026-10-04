---
name: no-api-key-anywhere
description: greg's rule of 2026-10-04 13:27Z: no API key anywhere in the software, the maintainer's own automation included; the "only fundamental rule"
metadata:
  type: feedback
  modified: 2026-10-04T13:29:10.336Z
---

greg, 2026-10-04 13:27Z, in the desktop/VS Code thread, answering whether his own error-report triage (described in beethoven-vscode's docs as Claude Code on his Console API key, `.github/workflows/triage.yml`) keeps its key: "no api key anywhere thats the only fundamental rule of this software".

**Why:** it widens the earlier "usage credits never, by anyone" rule (BEE-191, VS Code 5.0.0 removed the student's key) to everything: no Anthropic Console/API key and no per-use model access in any repository, workflow, plan, document or maintainer tool, not even for the vendor's own automation. He called it the only fundamental rule, so it outranks convenience every time.

**How to apply:** never propose, keep or describe as an option an API key, `apiKeyHelper`, Bedrock/Vertex/Foundry, a claude-code-action on a key, or usage credits. Code that refuses, strips or warns against a key is the rule working and stays. Dated records (research notes, changelog entries of past versions, checkpoints, ledgers) stay as records; current-practice text and code change. Automation that needs Claude runs on a person's own subscription or not at all. Ask before deleting a key a student stored under an old version (the nothing-deleted rule and the Console showing a key once both apply). Related: [[multi-account-d4]], [[beethoven-desktop]].

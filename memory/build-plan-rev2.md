---
name: build-plan-rev2
description: The re-evaluated build plan (2026-10-03/04) after greg's 7-goal rewrite, with D1-D3 decided (own subscription, new repo, Metaflow), the playbook folded in, usage credits excluded, D1d decided and widened into §17 (multi-account agent teams)
metadata:
  type: project
  modified: 2026-10-04T01:30:00.000Z
---

After greg rewrote the topic into 7 goals (2026-10-03), the build was re-evaluated. Master docs:
`/mnt/project-files/plan/BUILD_PLAN.md` (narrative) + `LINEAR_BREAKDOWN.md` (issues).

**Central finding:** the 7-goal research engine and the Beethoven launcher (hpcworker + extension) are
**two systems that share a grid**. The engine runs headless (`claude -p`) in the same Apptainer image,
orchestrated by Metaflow; the launcher stays the student's interactive Remote Control. **Both use the same
credential posture** (D1, greg 2026-10-03T23:09Z, overriding my gateway recommendation): the student's own
`claude auth login` on a compute node, `claude_config_dir` bound read-write (Claude Code's own writes; protected by policy, never a mount flag; none of ours reads or writes there), `claude auth status` only. **No API keys, no
LiteLLM gateway, no pooled or lab-held keys, no Bedrock/Vertex, no token extraction, no Managed Agents or
Messages API.** greg's reason: since Anthropic's 2026-06-15 change `claude -p` and the Agent SDK draw from
the flat-rate plan; all automated runs share the rolling 5-hour window. So G3 = **quota-window-aware
scheduling** (BEE-121), not a gateway.

**Decided:** D1 above; D2 new repo `OpenSpineConsortium/beethoven-research` (greg created it by hand, the
GitHub App got a 403); D3 Metaflow + outerbounds/metaflow-slurm. Placement (BUILD_PLAN §8.1): warrior's
login node bans python3/node, so Metaflow runs in a compute-node orchestrator job, never on the login node.
**2026-10-04:** D1b = C "decide on evidence" (the playbook's setup-token batch auth refused; BEE-101
measures whether headless 2.1.28x refreshes the sign-in; the token file only if that fails). **Usage credits
NEVER** (greg 01:12Z; hard exclusion, §2 C7). D1d DECIDED and widened into §17 (greg 02:18Z, 02:30Z): several own accounts at once, one master per account, one super-master lease switched claude-swap style near the limit, agent teams in, satellites as Slurm jobs, bus+registry+reaper (no orphans), never a credential copied. BEE-185..190. Nine probes (M1-M9) before building.

**Conflicts flagged, excluded for good:** claude.ai interception, token extraction in jobs, abuse-evasion
framing (C6). Goal 4's Phase B exploit work is off-grid, out of scope.

**Order:** P0 substrate → G1 verification → G5/G3 orchestration + pacing → G2 REFORMS + G6 medical → G4
compliance → G7 publish (human gate) → F2 extension view → spine study (§16); F1 in parallel now.

**§14 (Anthropic pages):** window leads for BEE-121: `/usage` bars from `-p`?, wait-for-reset ≥2.1.234
(`autoContinueAtUsageLimit`), `--max-budget-usd`, OpenTelemetry, reset time in the limit message. NOT leads:
task budgets, usage analytics dashboard. Cache 1 h on subscription, 5 min on credits/API key. Cloud
sessions 4 vCPU/16 GB/30 GB, no GPU. **§15 (playbook):** adopted sonnet + medium effort per step
(`--effort ultracode everywhere` withdrawn), `--max-turns`, window-sized jobs, `--session-id`/`--resume`,
`dontAsk`, stream-json events file, managed deny list, guard hook, `slurm-operator` + submit shim (BEE-180).
See [[linear-engine-structure]], [[measurement-ledger]], [[new-directions-2026-10-03]].

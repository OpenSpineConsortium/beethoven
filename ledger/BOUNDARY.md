# What each agent could and could not touch

The environment section of the methods paper, written from the actual settings and refusals, revised
in place with a dated line per change (format: `README.md`). Version 1, 2026-10-04T00:28Z.

## Phase A — planning and build threads in claude.ai cloud sessions (from 2026-10-03T21:13Z)
Could: read and write the shared project folder `/mnt/project-files/`; read the repositories the
environment lists (`OpenSpineConsortium/hpcworker`, `beethoven-extension`, since 23:54Z
`beethoven-research`, and the study repos `Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet` and
`u251-xenograft-rat-RNASeq-study`) and push only to its own branch `claude/project-thread-<id>`;
open draft pull requests (merging is greg's); read and write Linear team Beethoven; read the Google
Drive folder Beethoven-notebook; write Claude Docs and Artifacts; a shared memory folder; the public
web only through per-URL permission prompts that a human answers.
Could not: create a repository in the GitHub organisation (403 on 2026-10-03T23:21Z; greg did it by
hand); reach the grid at all (no ssh, no VPN, no grid credential exists in the session, by design);
read or hold any Claude credential; run a container (`apptainer` absent); fetch a URL whose prompt
went unanswered (2026-10-04T00:20Z, four URLs); run more than two workflow agents at once (4-CPU
container). Nothing in this phase ran on the grid or touched a student's data.
Measured against Anthropic's cloud-environments page (read 2026-10-04T00:30Z): each session is a
fresh Ubuntu 24.04 x86_64 VM with approximate ceilings of 4 vCPUs, 16 GB of RAM and 30 GB of disk,
no GPU; an idle VM pauses after a few minutes; GitHub goes through Anthropic's proxy, which keeps the
real credential outside the VM, refuses branch deletions and tag pushes, and reaches "only
repositories attached to the session", which is why the repository-creation call of 2026-10-03T23:21Z
returned 403; all other egress passes a security proxy with a DNS-level audit trail; the network level
in use here allowed the five pages greg linked once his message carried their URLs, and refused the
same URLs before that (the per-URL permission prompts of 00:20Z).
Revision 2026-10-04T00:35Z: this paragraph added.

## Phase B — the Beethoven launcher's worker on the grid (built; the rules it runs under)
Could: run as the student's own Slurm job on a compute node inside the lab's Apptainer image, under
the student's own Claude Code sign-in; write its run directory and node-local temp; queue one
successor with `afterany`; write `status.json`, `connection.json`, `progress.log`.
Could not: read, copy or export a credential; run anything on the login node beyond one `sbatch`,
`squeue` or `scancel` per action; delete anything outside its run directories and node-local temp
(destructive subcommands refuse under `CLAUDECODE`, `BEETHOVEN_REQUEST_ID`, `ASHLEY_REQUEST_ID`
or a non-terminal stdin); rewrite the student's `.claude.json` beyond three seeded keys; reach
other students' folders (the volume root ACL, kept by `tools/grid_access.sh`). Egress measured
2026-09-28 from `asx15`: `api.anthropic.com` reachable, `platform.claude.com` 200, `claude.ai` 403
to curl, `statsig.anthropic.com` no DNS record.

## Phase C — engine runs (not yet run)
To be written from the first real run: the managed-settings deny rules, the PreToolUse guard hook,
`CLAUDE_CONFIG_DIR` mounted read-only, the Pixi lockfile and image digest, partitions and QoS used,
the quota window as Claude Code reports it (BEE-121), and every refusal met. Until then: not yet
measured.

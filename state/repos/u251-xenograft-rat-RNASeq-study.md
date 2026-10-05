# CLAUDE STATE SERIALIZATION

**Timestamp:** 2026-10-04T20:25Z **Phase:** Planning

Pointer hand-off: `Gregory-Schwing-MD-PhD/u251-xenograft-rat-RNASeq-study` (PUBLIC, greg's own study repository). Not part of the Beethoven build; nothing in this project has worked on it. Project-wide state: `/mnt/project-files/state/claude_context.md`.

## 1. Primary Objective

Point a new session at greg's U251 glioblastoma xenograft study in RNU rats (culture, primary tumour, recurrence after LITT; RNA-seq and EPIC methylation): xengsort host-read removal, nf-core/rnaseq, nf-core/differentialabundance and RUVSeq as Slurm jobs on the grid, the GEO deposit GSE338105, the Neuro-Oncology letter and Advances manuscript, and the CNS 2026 Abstract 418 decks.

## 2. Architectural Decisions & Constraints

- Read-only from this project; no thread owns it. Default branch `master` (b110c97, 2026-07-05). The repository is public: the lab's raw data (`DATA/raw_lab/`, methylation `.idat` files) is never committed, and `~/.gdrive_token` is never read.
- Do not rename samples; never edit `PREREG*.md` or `TARGETS.md` (their hashes are stamped into the result files); GSE338105 is updated in place, never deleted and resubmitted; GEO submissions are greg's.
- There is no CLAUDE.md there; the project's grid etiquette and words rules apply to any session that works on it.

## 3. Files Modified & State

| File Path | Status | Key Modifications / Purpose |
| --- | --- | --- |
| README.md (master) | Complete | Study design and grid quick start; stale against the branch below |
| RESUME.md (branch research-letter-expansion) | Pending | The study's own working checkpoints, newest first (2026-09-27); read this, not master's README |
| README.md:172 (master; :174 on the branch) | Pending | Warns that `submit_xengsort.sh` lacks `--input`, `--host_fasta`, `--graft_fasta`; the script has passed all three (lines 42-48) since its first commit ac4b1cd, so the README warning is out of date, not the script |

## 4. Completed Milestones

1. RNA-seq GEO deposit files on master (ffaef66 to b110c97, 2026-07-05).
2. Branch `research-letter-expansion` (20709bd, 97 commits ahead of master, unmerged, no PR) holds the pre-registered analyses' result files, the manuscript's sources and build chain (`MANUSCRIPT_NOA/`; `main.pdf` is git-ignored and rebuilt by `build.sh`) and the methylation GEO package from greg's laptop session of 2026-09-26/27; branch `manuscript-and-geo-revisions` (54d30b6) is contained in it. Results there are described as verified on the grid; not re-verified from here.

## 5. Active Blockers & Errors

- None recorded in this project. Within the study's record (unverified now): the rnafusion reference job 40481320 failed on its 122 GB bundle, and several grid jobs were pending or running on 2026-09-27.
- Waiting on greg: from RESUME.md on the branch, send `GEO/methylation/COVER_NOTE.md` to GEO (its item 4 cleared with the laboratory first) and answer the open lab questions listed there; from `GEO/methylation/README.md:82`, fill the three pending methylation fields (extraction kit, bisulfite kit, core facility name). Whether to merge `research-letter-expansion` into master is written nowhere in the repository; it is open only because the branch is unmerged and has no PR.

## 6. Immediate Next Actions (Hydration Directives)

1. Run `git -C <checkout> fetch origin --prune --tags`; confirm master is b110c97 and `research-letter-expansion` is 20709bd.
2. Before any study work, read `git show origin/research-letter-expansion:RESUME.md | head -120`.
3. Work only on greg's request, on the grid inside Slurm jobs, and log it in `/mnt/project-files/ledger/LEDGER.md`.

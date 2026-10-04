> **Filed 2026-10-03 by the re-plan thread (Linear project R = P-BEE-13, issues BEE-165..170).** Written
> by a worker, then reviewed here. Before anything runs, greg answers **BEE-165 (D7)**: the source
> directories (`SRC` in `migrate.env`), the destination under `/rs/rs_grp_oschome/go2432/`, and whether
> the `patients` table may hold `PatientName`, `PatientBirthDate` and `AccessionNumber` at all; if not,
> drop those columns from section F before the catalog is built. Two defects fixed in review: every
> `.sbatch` now sources `migrate.env` from `$SLURM_SUBMIT_DIR` and then `$TOOLS/common.sh` (Slurm runs a
> spool copy of the script, so `$(dirname "$0")` was not `tools/`), and `hash_tree.sh`'s newline check
> used `$(printf '\n')`, which a command substitution strips to nothing, so the pattern matched every
> file and the script would always have refused; it now uses `$'\n'`. What stands unchanged and matters
> most: nothing here removes the source, ever (CLAUDE.md: nothing is deleted outside the framework's own
> run directories); the catalog's Python runs in a small data image of greg's own, never in the lab's
> shared worker image; section H's measurements come before trusting any number; none of these scripts
> has run on any machine yet, so the rehearsal in H is the first step on the grid.

# Runbook: moving go2432's imaging data from the Panasas home to the lab's CephFS volume, and cataloguing it

For a person at the grid (or a Remote Control session there). Nothing here runs from the cloud. Everything heavy runs as a Slurm job on a compute node; the login node `warrior` sees one `sbatch`, `squeue` or `scancel` per action and a few `mkdir`, `cat`, `cp` and `ls`. `warrior`'s banner bans `rsync`, `python3`, `md5sum` and others on sight, so even the rsync dry run and every Python line are jobs. **This runbook copies and verifies. It removes nothing from the source, ever.** Whether and when the home-directory copy goes is a separate decision made by hand later, outside this document. The only things any script here deletes are its own node-local temp directory `/tmp/$USER/hpcworker_$SLURM_JOB_ID` (through a guarded helper that refuses any other path) and nothing else.

Order of work: A (make the folders, write `migrate.env`) → B (inventory, sample first) → C (dry run, then the copy) → D (verify; repeat C+D on a mismatch) → E (lock, fingerprint) → F (build the data image, build the catalog, assign splits). H lists what must be measured before trusting any number below.

## A. Destination layout

```
/rs/rs_grp_oschome/go2432/                  your folder on the volume: other::---, closed to the approved list too
  data/imaging/
    migrate.env                             the one parameter file every job sources (section G)
    tools/                                  the scripts in section G (LF endings, 0700)
    raw/                                    immutable copies, one folder per source batch; raw/ itself 0700
      ct_home_2026-10/                      this batch: the home tree exactly as it is, locked 0500/0400 in E
      ct_home_2026-10.manifest.tsv          sha256 <TAB> size <TAB> relative path, one line per file (E)
      ct_home_2026-10.fingerprint           sha256 of the manifest + counts + when + which jobs (E)
    logs/ct_home_2026-10/                   job outputs, rsync logs, both manifests, the diff, the markers
    catalog/                                ct_home_2026-10.sqlite (F); 0600; PHI inside
    scratch/                                later: a student's working copies and derivatives (never raw)
/rs/rs_grp_oschome/go2432/images/           data-py312.sif and pylib-py312/ (F); yours, not the lab's shared image
```

Why here and not under `shared/`: DICOM headers carry names, birth dates and accession numbers. The volume root's `other::---` plus the named-user list is the first gate; your own folder's `other::---` is the second, so an approved student on the list still cannot enter. The notebook's tiers map on as: `raw/` is the read-only raw tier (its audience is you alone until a de-identified derivative exists; that derivative, under `shared/`, is a later decision, out of scope), `scratch/` the student tier, the catalog the datastore. `raw/`, `logs/` and `catalog/` are siblings so the whole of a raw batch can be locked without locking its logs. Every job runs under `umask 077`, so before E everything is 0700/0600; after E the batch is 0500 directories and 0400 files, owner included (E). The volume carries POSIX ACLs with a group-writable default somewhere under the root (`tools/deploy_shared.sh` notes it); what `go2432/` itself hands down is not measured (H), so E strips extended entries with `setfacl -b` before `chmod`, because on an ACL'd tree `chmod` moves only the mask.

Make the folders once (login node, cheap): `mkdir -p /rs/rs_grp_oschome/go2432/data/imaging/{tools,raw,logs/ct_home_2026-10,catalog,scratch} /rs/rs_grp_oschome/go2432/images`, `chmod 700` on `data`, `data/imaging` and each of them. Write `migrate.env` (G) and copy it into `logs/ct_home_2026-10/`, which is the `-D` directory of every job.

## B. Phase 1: Inventory

`inventory.sbatch` (G) walks the source read-only and writes to `$LOG`: `inventory.started` (a timestamp file; C and D use `find -newer` against it to refuse when the source has changed since), `summary.txt` (counts of files, directories, symlinks, hard-linked files, other inodes; total bytes; the fifteen commonest extensions; the ten largest files; how many of a 200-file sample carry `DICM` at offset 128; the newest mtime; how many names carry a tab, newline or backslash, which must be 0 for the manifest format to be exact) and `manifest_source.tsv` (`sha256 <TAB> size <TAB> ./relative/path`, sorted with `LC_ALL=C` by path). Hashing is `sha256sum` through `xargs -0 -P $SLURM_CPUS_PER_TASK`; sort scratch is on node-local temp; the partial files are written as `.part` and renamed.

Sample first: submit with `SAMPLE=2000`, which hashes only the first 2000 files, prints the MB/s and the projected time for the whole tree in `summary.txt`, and writes the manifest as `manifest_sample.tsv`. Then set the wall time from that projection with margin and submit with `SAMPLE=0`. Read `summary.txt`; never `cat` a manifest on the login node (`wc -l` and `head -3` are enough). Submit from `$LOG`: `sbatch -D "$PWD" --export=ALL,SAMPLE=2000 ../../tools/inventory.sbatch`, then once `squeue -u $USER`, then read the `.out` file when it is gone.

Read the summary for two things before C: paths that are themselves PHI (a patient name as a folder name means the manifest and the catalog's `path` column are PHI too, and the fingerprint file, which carries no paths, is the only thing that may ever leave the volume), and anything that is not a plain file (symlinks are copied as links by `rsync -a`; a link pointing outside the source is copied as a dangling link, which is correct and is listed).

## C. Phase 2: Copy

`copy.sbatch` (G) refuses, and changes nothing, when: it is not inside a job; `$SRC` is not a directory; `$DST` is not under `$RAW_ROOT`; either path contains the other; the batch's `.LOCKED` marker exists (E has run); `$DST` exists and is non-empty and `RESUME=1` was not given; any file under `$SRC` is newer than `inventory.started` (the source moved on: redo B); `manifest_source.tsv` is missing; or the volume's free space is below the manifest's byte total plus five percent.

The command is `rsync -a --hard-links --checksum --partial --itemize-changes --human-readable --stats --log-file=$LOG/rsync_<mode>_<job>.log "$SRC/" "$DST/"`. No `--delete` of any form, no `--remove-source-files`, no `--inplace`; nothing in the flag list may ever be added that removes or truncates. `MODE=dry` adds `--dry-run` and writes the itemized list to `rsync_dry_<job>.items`; read its line count and `--stats` block, not the list. Then `MODE=real`. `--checksum` costs nothing on an empty destination and is what makes a resume honest: on `RESUME=1` every file present on both sides is compared by content, not by size and time. If the wall time ends mid-copy, resubmit with `RESUME=1`; `--partial` keeps what was transferred. Exit 0 is complete; 23 means some files were not transferred (the log names them, usually permissions: fix the source permission by hand, resume); 24 means a source file vanished during the copy (something writes to the source: find it, stop it, redo B). Do not write to the source tree while B–E run.

## D. Phase 3: Verify

`verify.sbatch` (G) hashes `$DST` with the same `hash_tree.sh` as B into `manifest_dest.tsv`, checks again that nothing under `$SRC` is newer than `inventory.started`, and runs `diff manifest_source.tsv manifest_dest.tsv > diff.txt`. Clean means exactly: `diff` exits 0, `diff.txt` is empty, both manifests have the same line count, and the two files have the same sha256 (they are byte-identical). The job then prints `VERIFY OK <n> files <bytes> bytes manifest-sha256 <hex>` and writes `verify.ok` with that line; E refuses without it.

A mismatch reads as: a `<` line is in the source only (missing at the destination, or different content, in which case its `>` twin follows with the other hash); a `>` line is at the destination only. Response in every case: run C again with `RESUME=1` (rsync with `--checksum` rewrites the differing file), then D again. Never delete anything to make the diff clean, including a `>`-only file at the destination: it means the destination was written by something other than this copy; find out what before going on. If `find -newer` fires, the source changed: run B again (the inventory is the reference, so it has to be true), then C with `RESUME=1`, then D.

## E. Phase 4: Lock

`lock.sbatch` (G) refuses without `verify.ok`, or when any file under `$DST` is newer than `verify.ok`, or when the sha256 of `manifest_dest.tsv` is not the one `verify.ok` records. It then copies the manifest to `$DST.manifest.tsv`, writes `$DST.fingerprint` (the manifest's sha256, file count, byte total, UTC time, source path, destination path, the inventory, copy, verify and lock job ids) and the marker `$LOG/.LOCKED`, and locks: `setfacl -R -b` to strip every extended and default ACL entry, then `chmod 0500` on every directory including `$DST` itself and `chmod 0400` on every file, and `0400` on the manifest and fingerprint. It ends with a check that `find "$DST" -type d ! -perm 0500 -o -type f ! -perm 0400` prints nothing and that `getfacl` shows only `user::r-x`/`r--`, `group::---`, `other::---`. With every directory 0500, no `rm -rf` by the owner removes anything (unlinking needs write on the directory); only `chmod` can reopen it, and that is `unlock.sh` (G), which runs only at a terminal, never under `CLAUDECODE`, `BEETHOVEN_REQUEST_ID`, `ASHLEY_REQUEST_ID` or `AI_AGENT`, asks you to type the batch name, logs the unlock, and tells you to run D then E again afterwards (E refuses while anything is newer than `verify.ok`, so a re-lock always follows a fresh verify). The fingerprint's sha256 is the archive's identity: the catalog's `archives` row carries it, and so should any paper or notebook that uses the data.

Cutover is out of scope. The home copy stays where it is. Nothing in this runbook touches it beyond reading it, and no script here is able to remove it. Removing it, if ever, is your own decision, later, by hand, after you have read the fingerprint and the diff yourself.

## F. Catalog

**Where Python runs.** `pydicom` is not on the login node and `python3` is banned there. The lab's worker image (`claude-node22`, a sandbox) is shared with every student and the worker's contract; do not install into it (and whether it carries a usable `python3` is not measured). Build a small SIF of your own once, with `data_image.sbatch` (G): `apptainer build` from `docker://python:3.12-slim-bookworm` into `/rs/rs_grp_oschome/go2432/images/data-py312.sif` (no fakeroot needed for a plain pull, the route `jobs/build_image.sbatch` falls back to), then `pip install --target .../images/pylib-py312 'pydicom>=3,<4'` from inside it (pure Python, no compiled dependency; pixel data is never read, so no NumPy). Every catalog job runs `module load apptainer/1.2.2; apptainer exec --no-home -B /rs/rs_grp_oschome/$USER -B "$NODE_TMP/tmp:/tmp" --env PYTHONPATH=$PYLIB $IMG python3 ...`. Whether PyPI is reachable from a compute node is not measured (H).

**Schema** (SQLite, standard library; `catalog_build.py` creates it). Types are plain so any `sqlite3` version suffices.

```sql
CREATE TABLE archives (archive_id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL, root TEXT NOT NULL,
  manifest_sha256 TEXT NOT NULL, n_files INTEGER, n_bytes INTEGER, fingerprint_text TEXT, built_at TEXT);
CREATE TABLE files (file_id INTEGER PRIMARY KEY, archive_id INTEGER NOT NULL REFERENCES archives,
  path TEXT NOT NULL, size INTEGER NOT NULL, sha256 TEXT NOT NULL, is_dicom INTEGER NOT NULL,
  read_error TEXT, UNIQUE (archive_id, path));
CREATE TABLE patients (PatientID TEXT PRIMARY KEY, PatientName TEXT, PatientBirthDate TEXT, PatientSex TEXT);
CREATE TABLE studies (StudyInstanceUID TEXT PRIMARY KEY, PatientID TEXT REFERENCES patients, StudyDate TEXT,
  StudyTime TEXT, StudyDescription TEXT, AccessionNumber TEXT, InstitutionName TEXT);
CREATE TABLE series (SeriesInstanceUID TEXT PRIMARY KEY, StudyInstanceUID TEXT REFERENCES studies,
  SeriesNumber INTEGER, SeriesDescription TEXT, Modality TEXT, Manufacturer TEXT, ManufacturerModelName TEXT,
  BodyPartExamined TEXT, ProtocolName TEXT, ConvolutionKernel TEXT, KVP REAL, SliceThickness REAL,
  PixelSpacing TEXT, ImageOrientationPatient TEXT, FrameOfReferenceUID TEXT, n_instances INTEGER);
CREATE TABLE instances (SOPInstanceUID TEXT PRIMARY KEY, SeriesInstanceUID TEXT REFERENCES series,
  SOPClassUID TEXT, TransferSyntaxUID TEXT, InstanceNumber INTEGER, ImagePositionPatient TEXT,
  ImageOrientationPatient TEXT, PixelSpacing TEXT, SliceThickness REAL, SliceLocation REAL, Rows INTEGER,
  Columns INTEGER, BitsAllocated INTEGER, BitsStored INTEGER, PixelRepresentation INTEGER, RescaleSlope REAL,
  RescaleIntercept REAL, PhotometricInterpretation TEXT, file_id INTEGER NOT NULL REFERENCES files);
CREATE TABLE splits (split_set TEXT NOT NULL, PatientID TEXT NOT NULL, StudyInstanceUID TEXT NOT NULL,
  split TEXT NOT NULL CHECK (split IN ('train','val','test','holdout')), fold INTEGER, method TEXT,
  seed INTEGER, assigned_at TEXT, PRIMARY KEY (split_set, StudyInstanceUID));
CREATE TRIGGER splits_one_split_per_patient BEFORE INSERT ON splits
  WHEN EXISTS (SELECT 1 FROM splits s WHERE s.split_set = NEW.split_set AND s.PatientID = NEW.PatientID
               AND s.split <> NEW.split)
  BEGIN SELECT RAISE(ABORT, 'patient already assigned to another split in this split_set'); END;
CREATE INDEX idx_studies_patient ON studies (PatientID);
CREATE INDEX idx_series_study ON series (StudyInstanceUID);
CREATE INDEX idx_instances_series ON instances (SeriesInstanceUID);
```

Multi-valued attributes (`PixelSpacing`, `ImagePositionPatient`, `ImageOrientationPatient`) are stored in DICOM's own form, values joined with `\`, so they round-trip exactly; series-level geometry is the first instance's, and `n_instances` lets a query find series whose instances disagree. Every file in the manifest gets a `files` row; a non-DICOM file has `is_dicom = 0`, an unreadable one `read_error`.

**Populating.** `catalog.sbatch` (G) runs `catalog_build.py` inside the image: it refuses unless the batch is locked, reads `manifest_dest.tsv` (so the catalog is built from the verified list, and the `sha256` and `size` columns come from the manifest, not from re-hashing), reads each header with `pydicom.dcmread(path, stop_before_pixels=True)` in a `multiprocessing.Pool` of `$SLURM_CPUS_PER_TASK`, inserts in transactions of 5000, builds the database on node-local temp and copies it to `catalog/<set>.sqlite.part`, renamed into place at the end. It writes nothing under `raw/`. The `archives` row carries the fingerprint.

**Splits.** `splits.py` (G) assigns every study of one patient to the same fold and split, by a seeded shuffle of `PatientID`s (`method = 'patient_shuffle'`, the seed recorded), under a named `split_set`; the trigger refuses any later assignment that would put one patient in two splits. That is the partition REFORMS asks for against leakage (module 6) and for honest claims of generalization (module 8); record `split_set` and seed with every result.

**DuckDB, later and optional.** For analysis, `pip install --target "$PYLIB" duckdb` into the same directory and `ATTACH 'catalog.sqlite' AS c (TYPE sqlite, READ_ONLY)` or export `files`/`instances` to Parquet; the SQLite file stays the source of record, DuckDB a reader.

**PHI.** `PatientName`, `PatientBirthDate`, `AccessionNumber`, `InstitutionName`, dates, and possibly `path`, are identifiers. The catalog stays in `catalog/` at 0600 inside your closed folder; no copy to a laptop, a notebook export, a repository or a shared folder. Before any export or publication the data must be de-identified (DICOM PS3.15 Annex E basic profile at least: names and dates removed or shifted, UIDs replaced through a keyed mapping kept outside the catalog, `path` dropped) and the de-identified table checked by a second person. The fingerprint file alone carries no PHI.

## G. Script skeletons

All files under `data/imaging/tools/`, LF endings (`file tools/* | grep -c CRLF` must print 0; `sed -i 's/\r$//'` if one was edited on Windows), bash 4.2 and coreutils 8.22 only outside the image, Python 3.12 standard library plus pydicom inside it. Every job sources `migrate.env` from its `-D` directory. Each `.sbatch` sources `migrate.env` from `$SLURM_SUBMIT_DIR` and then `$TOOLS/common.sh`, never from `$(dirname "$0")`: Slurm runs a copy of the batch script out of its own spool directory, so `$0` does not point at `tools/`.

**`migrate.env`** (kept in `data/imaging/` and copied into `$LOG`):

```bash
SET=ct_home_2026-10
SRC=$HOME/ct                                        # the source folder on the Panasas home: fill in
BASE=/rs/rs_grp_oschome/go2432/data/imaging
RAW_ROOT=$BASE/raw; DST=$RAW_ROOT/$SET; LOG=$BASE/logs/$SET; CATALOG=$BASE/catalog; TOOLS=$BASE/tools
IMG=/rs/rs_grp_oschome/go2432/images/data-py312.sif; PYLIB=/rs/rs_grp_oschome/go2432/images/pylib-py312
```

**`common.sh`** (sourced by every job):

```bash
# shared guards; bash 4.2. Nothing here deletes anything except rm_own_tmp, below.
set -uo pipefail; umask 077
say() { echo "$(date -u +%FT%TZ) $*"; }
refuse() { echo "REFUSING: $*" >&2; exit 1; }
JOB="${SLURM_JOB_ID:-}"; [ -n "$JOB" ] || refuse "this is a batch job body; submit it with sbatch, do not run it on $(hostname -s)"
HERE="${SLURM_SUBMIT_DIR:-$PWD}"; [ -s "$HERE/migrate.env" ] || refuse "no migrate.env in $HERE (submit from \$LOG with -D \"\$PWD\")"
# shellcheck disable=SC1091
source "$HERE/migrate.env"
case "$DST" in "$RAW_ROOT"/?*) ;; *) refuse "DST $DST is not under $RAW_ROOT";; esac
case "$RAW_ROOT" in /rs/rs_grp_oschome/"$USER"/*) ;; *) refuse "RAW_ROOT must be under your own folder on the volume";; esac
# node-local temp: the profile's pattern, never $TMPDIR (CephFS on this grid)
NODE_TMP="/tmp/$USER/hpcworker_$JOB"; mkdir -p "$NODE_TMP" || refuse "cannot make $NODE_TMP"
rm_own_tmp() { # the one deletion: only a path whose LAST component is hpcworker_<this job>
  local p="${1%/}"; case "${p##*/}" in "hpcworker_$JOB") rm -rf -- "$p";; *) echo "REFUSING to remove $p" >&2;; esac; }
trap 'rm_own_tmp "$NODE_TMP"' EXIT
source_unchanged() { # since the inventory began; the file it names is the first thing that changed
  [ -e "$LOG/inventory.started" ] || refuse "no inventory.started in $LOG: run inventory first"
  local f; f=$(find "$SRC" -newer "$LOG/inventory.started" -print 2>/dev/null | head -1)
  [ -z "$f" ] || refuse "the source changed since the inventory ($f): run inventory again"; }
```

**`hash_tree.sh`** (`ROOT OUT [SAMPLE_N]`; used by B and D so both manifests have one format):

```bash
#!/bin/bash
# manifest: sha256 <TAB> size <TAB> ./path, LC_ALL=C sorted by path; sort scratch on node temp. Reads only.
set -uo pipefail; root=$1; out=$2; n=${3:-0}; P=${SLURM_CPUS_PER_TASK:-4}; T=${NODE_TMP:?}
cd "$root" || exit 1
bad=$(find . -type f \( -name "*"$'\n'"*" -o -name "*"$'\t'"*" -o -name '*\\*' \) | wc -l)
[ "$bad" -eq 0 ] || { echo "REFUSING: $bad file names carry a newline, tab or backslash; rename by hand first" >&2; exit 2; }
find . -type f -printf '%s\t%p\n' | LC_ALL=C sort -T "$T" -t "$(printf '\t')" -k2 > "$T/sizes"
[ "$n" -gt 0 ] && { head -n "$n" "$T/sizes" > "$T/sizes.s"; mv -f "$T/sizes.s" "$T/sizes"; }
cut -f2- "$T/sizes" | tr '\n' '\0' | xargs -0 -r -P "$P" -n 64 sha256sum > "$T/hashes" || exit 3
awk -F'\t' 'NR==FNR {sz[$2]=$1; next} {h=substr($0,1,64); p=substr($0,67); print h "\t" sz[p] "\t" p}' \
  "$T/sizes" "$T/hashes" | LC_ALL=C sort -T "$T" -t "$(printf '\t')" -k3 > "$out.part" || exit 3
[ "$(wc -l < "$out.part")" -eq "$(wc -l < "$T/sizes")" ] || { echo "REFUSING: hashed $(wc -l < "$out.part") of $(wc -l < "$T/sizes") files" >&2; exit 3; }
mv -f "$out.part" "$out"
```

**`inventory.sbatch`:**

```bash
#!/bin/bash
#SBATCH --job-name=img_inventory --partition=secp --qos=secondary --nodes=1 --ntasks=1
#SBATCH --cpus-per-task=8 --mem=8G --time=04:00:00 --output=inventory_%j.out
source "${SLURM_SUBMIT_DIR:-$PWD}/migrate.env" && source "$TOOLS/common.sh"; SAMPLE=${SAMPLE:-0}
[ -d "$SRC" ] || refuse "SRC $SRC is not a directory"
say "inventory of $SRC on $(hostname -s), sample=$SAMPLE"
[ "$SAMPLE" -gt 0 ] || touch "$LOG/inventory.started"   # the reference the copy and the verify compare against
S="$LOG/summary${SAMPLE:+_sample}.txt"; [ "$SAMPLE" -gt 0 ] || S="$LOG/summary.txt"
{ echo "== $SRC at $(date -u +%FT%TZ), job $JOB"
  echo "files: $(find "$SRC" -type f | wc -l)  dirs: $(find "$SRC" -type d | wc -l)  symlinks: $(find "$SRC" -type l | wc -l)"
  echo "hardlinked files: $(find "$SRC" -type f -links +1 | wc -l)  other inodes: $(find "$SRC" ! -type f ! -type d ! -type l | wc -l)"
  echo "bytes (apparent): $(find "$SRC" -type f -printf '%s\n' | awk '{s+=$1} END {printf "%.0f\n", s}')"
  echo "newest mtime: $(find "$SRC" -type f -printf '%TY-%Tm-%Td %TH:%TM\n' | sort | tail -1)"
  echo "== extensions"; find "$SRC" -type f -printf '%f\n' | awk -F. 'NF>1 {print tolower($NF); next} {print "(none)"}' | sort | uniq -c | sort -rn | head -15
  echo "== largest"; find "$SRC" -type f -printf '%s %p\n' | sort -rn | head -10
  d=0; while IFS= read -r f; do [ "$(dd if="$f" bs=1 skip=128 count=4 2>/dev/null)" = DICM ] && d=$((d+1)); done \
    < <(find "$SRC" -type f | head -200); echo "DICM magic in sample of 200: $d"
} > "$S.part" 2>&1
t0=$(date +%s); out="$LOG/manifest_source.tsv"; [ "$SAMPLE" -gt 0 ] && out="$LOG/manifest_sample.tsv"
bash "$TOOLS/hash_tree.sh" "$SRC" "$out" "$SAMPLE" || { echo "hashing failed" >> "$S.part"; mv -f "$S.part" "$S"; exit 3; }
dt=$(( $(date +%s) - t0 )); b=$(awk -F'\t' '{s+=$2} END {printf "%.0f", s}' "$out")
{ echo "== hashed $(wc -l < "$out") files, $b bytes in ${dt}s: $(( b / 1048576 / (dt > 0 ? dt : 1) )) MB/s"
  [ "$SAMPLE" -gt 0 ] && echo "projected for the whole tree: $(( dt * $(find "$SRC" -type f | wc -l) / SAMPLE / 60 )) min at this rate"; } >> "$S.part"
mv -f "$S.part" "$S"; say "done; read $S"
```

**`copy.sbatch`:**

```bash
#!/bin/bash
#SBATCH --job-name=img_copy --partition=secp --qos=secondary --nodes=1 --ntasks=1
#SBATCH --cpus-per-task=2 --mem=4G --time=12:00:00 --output=copy_%j.out
source "${SLURM_SUBMIT_DIR:-$PWD}/migrate.env" && source "$TOOLS/common.sh"; MODE=${MODE:-dry}; RESUME=${RESUME:-0}
[ -d "$SRC" ] || refuse "SRC $SRC is not a directory"
case "$DST/" in "$SRC"/*) refuse "destination inside source";; esac; case "$SRC/" in "$DST"/*) refuse "source inside destination";; esac
[ -e "$LOG/.LOCKED" ] && refuse "$SET is locked; nothing writes to it (unlock.sh is the deliberate step)"
[ -s "$LOG/manifest_source.tsv" ] || refuse "no manifest_source.tsv: run the full inventory first"
source_unchanged
if [ -d "$DST" ] && [ -n "$(ls -A "$DST" | head -1)" ] && [ "$RESUME" != 1 ]; then refuse "$DST exists and is not empty; RESUME=1 to continue a copy"; fi
need=$(awk -F'\t' '{s+=$2} END {printf "%.0f", s}' "$LOG/manifest_source.tsv"); free=$(( $(df -Pk "$RAW_ROOT" | awk 'NR==2 {print $4}') * 1024 ))
[ "$free" -gt $(( need + need / 20 )) ] || refuse "free $free bytes on the volume, need $need plus 5%"
command -v rsync >/dev/null || refuse "no rsync on $(hostname -s)"; say "rsync $(rsync --version | head -1), mode=$MODE resume=$RESUME"
mkdir -p "$DST" || refuse "cannot make $DST"
flags=(-a --hard-links --checksum --partial --itemize-changes --human-readable --stats "--log-file=$LOG/rsync_${MODE}_$JOB.log")
[ "$MODE" = dry ] && flags+=(--dry-run)      # never --delete*, --remove-source-files or --inplace, in any mode
rsync "${flags[@]}" "$SRC/" "$DST/" > "$LOG/rsync_${MODE}_$JOB.items" 2>&1; rc=$?
say "rsync exit $rc ($( case $rc in 0) echo complete;; 23) echo 'partial: some files not transferred, see the log';; 24) echo 'a source file vanished: something writes to the source';; *) echo 'see the log';; esac ))"
echo "$(date -u +%FT%TZ) job=$JOB mode=$MODE resume=$RESUME rc=$rc" >> "$LOG/copy.history"; grep -E '^(Number of|Total)' "$LOG/rsync_${MODE}_$JOB.items"; exit $rc
```

**`verify.sbatch`:**

```bash
#!/bin/bash
#SBATCH --job-name=img_verify --partition=secp --qos=secondary --nodes=1 --ntasks=1
#SBATCH --cpus-per-task=8 --mem=8G --time=04:00:00 --output=verify_%j.out
source "${SLURM_SUBMIT_DIR:-$PWD}/migrate.env" && source "$TOOLS/common.sh"
[ -d "$DST" ] || refuse "$DST does not exist: run the copy first"; [ -s "$LOG/manifest_source.tsv" ] || refuse "no manifest_source.tsv"
source_unchanged
bash "$TOOLS/hash_tree.sh" "$DST" "$LOG/manifest_dest.tsv" || refuse "hashing the destination failed"
if diff "$LOG/manifest_source.tsv" "$LOG/manifest_dest.tsv" > "$LOG/diff.txt"; then
  n=$(wc -l < "$LOG/manifest_dest.tsv"); b=$(awk -F'\t' '{s+=$2} END {printf "%.0f", s}' "$LOG/manifest_dest.tsv"); h=$(sha256sum "$LOG/manifest_dest.tsv" | cut -c1-64)
  echo "VERIFY OK $n files $b bytes manifest-sha256 $h job $JOB $(date -u +%FT%TZ)" | tee "$LOG/verify.ok.part"; mv -f "$LOG/verify.ok.part" "$LOG/verify.ok"
else
  rm -f "$LOG/verify.ok" 2>/dev/null   # a stale OK must not let the lock run; the manifests and diff stay
  say "MISMATCH: $(grep -c '^<' "$LOG/diff.txt") source-only lines, $(grep -c '^>' "$LOG/diff.txt") destination-only lines; first 20:"; head -20 "$LOG/diff.txt"
  say "next: copy.sbatch with MODE=real RESUME=1, then verify again. Delete nothing."; exit 2
fi
```

**`lock.sbatch`:**

```bash
#!/bin/bash
#SBATCH --job-name=img_lock --partition=secp --qos=secondary --nodes=1 --ntasks=1
#SBATCH --cpus-per-task=1 --mem=2G --time=02:00:00 --output=lock_%j.out
source "${SLURM_SUBMIT_DIR:-$PWD}/migrate.env" && source "$TOOLS/common.sh"
[ -s "$LOG/verify.ok" ] || refuse "no verify.ok: verify first"
want=$(awk '{print $8}' "$LOG/verify.ok"); have=$(sha256sum "$LOG/manifest_dest.tsv" | cut -c1-64); [ "$want" = "$have" ] || refuse "manifest_dest.tsv is not the one verify.ok recorded"
f=$(find "$DST" -newer "$LOG/verify.ok" -print | head -1); [ -z "$f" ] || refuse "$f changed after the verify: verify again"
cp "$LOG/manifest_dest.tsv" "$DST.manifest.tsv.part" && mv -f "$DST.manifest.tsv.part" "$DST.manifest.tsv"
{ echo "archive $SET"; echo "manifest_sha256 $have"; cat "$LOG/verify.ok"; echo "source $SRC"; echo "destination $DST"
  echo "jobs: $(ls "$LOG"/*_*.out | sed 's#.*/##' | tr '\n' ' ')"; echo "locked_at $(date -u +%FT%TZ) by lock job $JOB"; } > "$DST.fingerprint.part"
mv -f "$DST.fingerprint.part" "$DST.fingerprint"; touch "$LOG/.LOCKED"
command -v setfacl >/dev/null && setfacl -R -b "$DST" "$DST.manifest.tsv" "$DST.fingerprint"   # chmod moves only the mask on an ACL'd tree
find "$DST" -type d -exec chmod 0500 {} + && find "$DST" -type f -exec chmod 0400 {} + && chmod 0400 "$DST.manifest.tsv" "$DST.fingerprint" || refuse "chmod failed part way; run lock again"
left=$(find "$DST" \( -type d ! -perm 0500 \) -o \( -type f ! -perm 0400 \) | wc -l); [ "$left" -eq 0 ] || refuse "$left entries not locked"
command -v getfacl >/dev/null && getfacl -p "$DST" | grep -E '^(user|group|other|mask|default)' | sed 's/^/   /'
say "LOCKED $SET: $(cat "$DST.fingerprint" | head -2 | tr '\n' ' ')"
```

**`unlock.sh`** (login node, a person at a terminal; file work only):

```bash
#!/bin/bash
# the deliberate step. Reopens one raw batch for writing; verify.sbatch then lock.sbatch must follow.
set -uo pipefail; [ -t 0 ] || { echo "REFUSING: unlock runs only at a terminal" >&2; exit 1; }
for v in CLAUDECODE BEETHOVEN_REQUEST_ID ASHLEY_REQUEST_ID AI_AGENT; do [ -z "${!v:-}" ] || { echo "REFUSING: $v is set; an agent may not unlock" >&2; exit 1; }; done
source "$(dirname "$0")/../migrate.env"; [ -e "$LOG/.LOCKED" ] || { echo "$SET is not locked"; exit 0; }
cat "$DST.fingerprint"; printf 'Type the batch name to unlock it: '; read -r a; [ "$a" = "$SET" ] || { echo "not unlocked"; exit 1; }
find "$DST" -type d -exec chmod 0700 {} + && find "$DST" -type f -exec chmod 0600 {} + && chmod 0600 "$DST.manifest.tsv" "$DST.fingerprint"
mv -f "$LOG/.LOCKED" "$LOG/.UNLOCKED.$(date -u +%Y%m%dT%H%M%SZ)"; echo "$(date -u +%FT%TZ) unlocked by $USER" >> "$LOG/unlock.log"
echo "unlocked. When done: verify.sbatch, then lock.sbatch (the lock refuses until a fresh verify passes)."
```

**`data_image.sbatch`** (once):

```bash
#!/bin/bash
#SBATCH --job-name=img_dataimage --partition=secp --qos=secondary --nodes=1 --ntasks=1
#SBATCH --cpus-per-task=2 --mem=8G --time=01:00:00 --output=dataimage_%j.out
source "${SLURM_SUBMIT_DIR:-$PWD}/migrate.env" && source "$TOOLS/common.sh"; module load apptainer/1.2.2 || refuse "no apptainer module"
[ -e "$IMG" ] && refuse "$IMG exists; move it aside by hand if you mean to rebuild"
export APPTAINER_CACHEDIR="$NODE_TMP/cache" APPTAINER_TMPDIR="$NODE_TMP/tmp"; mkdir -p "$APPTAINER_CACHEDIR" "$APPTAINER_TMPDIR" "$PYLIB"
apptainer build "$IMG.part" docker://python:3.12-slim-bookworm || refuse "build failed (registry egress from this node?)"; mv -f "$IMG.part" "$IMG"
apptainer exec --no-home -B "$PYLIB" -B "$NODE_TMP/tmp:/tmp" "$IMG" python3 -m pip install --no-cache-dir --target "$PYLIB" 'pydicom>=3,<4' || refuse "pip failed (PyPI egress?)"
apptainer exec --no-home -B "$PYLIB" --env PYTHONPATH="$PYLIB" "$IMG" python3 -c 'import pydicom, sqlite3; print("pydicom", pydicom.__version__, "sqlite", sqlite3.sqlite_version)'
```

**`catalog.sbatch`:**

```bash
#!/bin/bash
#SBATCH --job-name=img_catalog --partition=secp --qos=secondary --nodes=1 --ntasks=1
#SBATCH --cpus-per-task=8 --mem=16G --time=08:00:00 --output=catalog_%j.out
source "${SLURM_SUBMIT_DIR:-$PWD}/migrate.env" && source "$TOOLS/common.sh"; module load apptainer/1.2.2 || refuse "no apptainer module"
[ -e "$LOG/.LOCKED" ] || refuse "$SET is not locked; the catalog is built from a locked batch only"
[ -s "$IMG" ] && [ -d "$PYLIB" ] || refuse "no data image: run data_image.sbatch"
mkdir -p "$NODE_TMP/tmp" "$CATALOG"; db="$NODE_TMP/$SET.sqlite"
apptainer exec --no-home -B "/rs/rs_grp_oschome/$USER" -B "$NODE_TMP/tmp:/tmp" -B "$NODE_TMP" --env PYTHONPATH="$PYLIB" "$IMG" \
  python3 "$TOOLS/catalog_build.py" --set "$SET" --root "$DST" --manifest "$LOG/manifest_dest.tsv" --fingerprint "$DST.fingerprint" \
  --db "$db" --workers "${SLURM_CPUS_PER_TASK:-4}" || refuse "catalog build failed"
cp "$db" "$CATALOG/$SET.sqlite.part" && mv -f "$CATALOG/$SET.sqlite.part" "$CATALOG/$SET.sqlite" && chmod 0600 "$CATALOG/$SET.sqlite"
say "catalog at $CATALOG/$SET.sqlite ($(du -h "$CATALOG/$SET.sqlite" | cut -f1)); PHI inside, stays on the volume"
```

**`catalog_build.py`:**

```python
#!/usr/bin/env python3
"""Imaging catalog from a locked raw batch: headers only, writes only to --db. Standard library + pydicom."""
import argparse, os, sqlite3, time
from multiprocessing import Pool
import pydicom
from pydicom.errors import InvalidDicomError
from pydicom.multival import MultiValue

SCHEMA = """ ... the CREATE statements of section F ... """
PAT = ("PatientID", "PatientName", "PatientBirthDate", "PatientSex")
STU = ("StudyInstanceUID", "PatientID", "StudyDate", "StudyTime", "StudyDescription", "AccessionNumber", "InstitutionName")
SER = ("SeriesInstanceUID", "StudyInstanceUID", "SeriesNumber", "SeriesDescription", "Modality", "Manufacturer",
       "ManufacturerModelName", "BodyPartExamined", "ProtocolName", "ConvolutionKernel", "KVP", "SliceThickness",
       "PixelSpacing", "ImageOrientationPatient", "FrameOfReferenceUID")
INS = ("SOPInstanceUID", "SeriesInstanceUID", "SOPClassUID", "InstanceNumber", "ImagePositionPatient",
       "ImageOrientationPatient", "PixelSpacing", "SliceThickness", "SliceLocation", "Rows", "Columns", "BitsAllocated",
       "BitsStored", "PixelRepresentation", "RescaleSlope", "RescaleIntercept", "PhotometricInterpretation")

def val(ds, name):
    v = ds.get(name)
    if v is None or v == "": return None
    if isinstance(v, MultiValue): return "\\".join(str(x) for x in v)   # DICOM's own form, exact round-trip
    return v if isinstance(v, (int, float)) else str(v)

def read_one(job):
    root, rel = job
    try: ds = pydicom.dcmread(os.path.join(root, rel), stop_before_pixels=True)
    except InvalidDicomError: return rel, 0, None, None
    except Exception as e: return rel, 0, None, type(e).__name__ + ": " + str(e)[:200]
    rec = {k: val(ds, k) for k in set(PAT + STU + SER + INS)}
    rec["TransferSyntaxUID"] = str(getattr(getattr(ds, "file_meta", None), "TransferSyntaxUID", "")) or None
    return rel, 1, rec, None

def main():
    ap = argparse.ArgumentParser()
    for a in ("--set", "--root", "--manifest", "--fingerprint", "--db"): ap.add_argument(a, required=True)
    ap.add_argument("--workers", type=int, default=4); a = ap.parse_args()
    if os.access(a.root, os.W_OK): raise SystemExit("REFUSING: %s is writable; catalog a locked batch only" % a.root)
    rows = [l.rstrip("\n").split("\t") for l in open(a.manifest, encoding="utf-8")]   # sha256, size, ./path
    con = sqlite3.connect(a.db); con.executescript(SCHEMA)
    fp = open(a.fingerprint, encoding="utf-8").read()
    msha = [l.split()[1] for l in fp.splitlines() if l.startswith("manifest_sha256")][0]
    con.execute("INSERT INTO archives (name, root, manifest_sha256, n_files, n_bytes, fingerprint_text, built_at) VALUES (?,?,?,?,?,?,?)",
                (a.set, a.root, msha, len(rows), sum(int(r[1]) for r in rows), fp, time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())))
    aid = con.execute("SELECT archive_id FROM archives WHERE name=?", (a.set,)).fetchone()[0]
    fid = {}
    for sha, size, path in rows:
        cur = con.execute("INSERT INTO files (archive_id, path, size, sha256, is_dicom) VALUES (?,?,?,?,0)", (aid, path, int(size), sha)); fid[path] = cur.lastrowid
    con.commit(); n = 0
    with Pool(a.workers) as pool:
        for rel, isd, rec, err in pool.imap_unordered(read_one, ((a.root, r[2]) for r in rows), chunksize=64):
            con.execute("UPDATE files SET is_dicom=?, read_error=? WHERE file_id=?", (isd, err, fid[rel]))
            if rec:
                ins = lambda t, cols, extra=(): con.execute("INSERT OR IGNORE INTO %s (%s) VALUES (%s)" % (t, ",".join(cols + tuple(k for k, _ in extra)), ",".join("?" * (len(cols) + len(extra)))), tuple(rec.get(c) for c in cols) + tuple(v for _, v in extra))
                ins("patients", PAT); ins("studies", STU); ins("series", SER)
                ins("instances", INS, (("TransferSyntaxUID", rec["TransferSyntaxUID"]), ("file_id", fid[rel])))
            n += 1
            if n % 5000 == 0: con.commit(); print("%d / %d" % (n, len(rows)), flush=True)
    con.execute("UPDATE series SET n_instances = (SELECT COUNT(*) FROM instances i WHERE i.SeriesInstanceUID = series.SeriesInstanceUID)")
    con.commit()
    for t in ("files", "patients", "studies", "series", "instances"): print(t, con.execute("SELECT COUNT(*) FROM " + t).fetchone()[0])
    print("non-DICOM files:", con.execute("SELECT COUNT(*) FROM files WHERE is_dicom=0").fetchone()[0],
          "read errors:", con.execute("SELECT COUNT(*) FROM files WHERE read_error IS NOT NULL").fetchone()[0])
    con.close()

if __name__ == "__main__": main()
```

**`splits.py`** (run the same way as `catalog_build.py`, inside the image, in a short job; `--db --split-set --seed --folds 5 --test-fold 0`):

```python
import argparse, random, sqlite3, time
ap = argparse.ArgumentParser(); [ap.add_argument(x, required=True) for x in ("--db", "--split-set")]
ap.add_argument("--seed", type=int, required=True); ap.add_argument("--folds", type=int, default=5); ap.add_argument("--test-fold", type=int, default=0)
a = ap.parse_args(); con = sqlite3.connect(a.db)
if con.execute("SELECT COUNT(*) FROM splits WHERE split_set=?", (a.split_set,)).fetchone()[0]: raise SystemExit("REFUSING: split_set exists; choose a new name, never overwrite")
pids = sorted(p for (p,) in con.execute("SELECT DISTINCT PatientID FROM studies WHERE PatientID IS NOT NULL")); random.Random(a.seed).shuffle(pids)
fold = {p: i % a.folds for i, p in enumerate(pids)}; now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
for pid, suid in con.execute("SELECT PatientID, StudyInstanceUID FROM studies WHERE PatientID IS NOT NULL").fetchall():
    f = fold[pid]; con.execute("INSERT INTO splits VALUES (?,?,?,?,?,?,?,?)", (a.split_set, pid, suid, "test" if f == a.test_fold else "train", f, "patient_shuffle", a.seed, now))
con.commit(); print({r[0]: r[1] for r in con.execute("SELECT split, COUNT(DISTINCT PatientID) FROM splits WHERE split_set=? GROUP BY split", (a.split_set,))})
```

## H. What must be measured on the real grid before trusting this

- **The compute node's stack.** `cat /etc/redhat-release`, `rsync --version` (an EL7 node is expected to carry 3.1.2, which has everything used here and lacks `--mkpath`, which is not used; not measured), `bash --version`, `sha256sum`, `find -printf`, `xargs -P`, `getfacl`/`setfacl`, `module load apptainer/1.2.2`. One probe job prints them all.
- **Whether `/tmp` is swept while a job runs.** Write a canary under `/tmp/$USER/hpcworker_$SLURM_JOB_ID`, sleep for the longest wall time used here, check it is still there. The scripts keep only sort scratch and the half-built catalog on node temp, so a sweep costs a rerun, not data; but the catalog job should be shortened or write to CephFS if the sweep is real. Also `df` of `/tmp` on the node: the catalog database and sort scratch must fit.
- **ACL inheritance under `go2432/`.** `getfacl -p /rs/rs_grp_oschome/go2432` and of `data/`: are there `default:` entries, and is the group entry writable? Make `logs/<set>/acl_probe/` and read its ACL back. This decides whether E's `setfacl -b` is needed and whether anything created before E is group-readable for a moment; note the root's setgid (`drwxrws--T`) gives every new file the group `oschome`.
- **Whether `chmod 0500`/`0400` and `setfacl -b` behave as expected on CephFS**, read back with `stat` and `getfacl` after E, and that `rm` of a locked file as the owner is refused (test on a throwaway file in `logs/`, never in `raw/`).
- **Throughput and time per TB.** The 2000-file sample's MB/s for Panasas reads (B), rsync's `--stats` from the dry run and the real copy (C), the destination hash rate (D). Set each wall time from these with margin; the copy is resumable, the hashes are not. Also the queue wait on `secp`/`secondary` at the hour you submit.
- **The source is quiet.** `find -newer` is the check; measure once that nothing (a Beethoven worker's workspace, a sync tool, a cron) writes under `$SRC`, and that `du -s` on Panasas agrees with the manifest's byte total within sparse-file and hard-link effects.
- **Space.** `df -h /rs/rs_grp_oschome` and, if `getfattr` exists, `getfattr -n ceph.quota.max_bytes` on the volume root and your folder: a CephFS quota that `df` does not show would stop the copy part way (rsync exit 11 or 23; resume after making room, never by deleting the source).
- **Egress for the data image.** Whether `docker.io` and `pypi.org` answer from a compute node (only Anthropic's hosts were measured on 2026-09-28); whether `apptainer build` from `docker://` works without fakeroot there; `sqlite3.sqlite_version` inside the image.
- **The data itself.** The `DICM` count in the sample against the file count (DICOM without the 128-byte preamble, DICOMDIR files, zipped studies or non-DICOM exports change what the catalog can read); whether folder or file names carry PHI, which decides whether the manifests may ever leave the volume (if yes, only the fingerprint may).
- **The scripts on a throwaway.** Run B–E once on a small copy of a few studies in `logs/<set>/rehearsal_src/` into `raw/rehearsal_<date>/`, including a forced mismatch (edit a byte in the rehearsal destination before D) to see the diff and the refusal paths with your own eyes, before the real batch.
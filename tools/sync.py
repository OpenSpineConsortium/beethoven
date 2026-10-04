#!/usr/bin/env python3
"""Copy the project's shared files into this repository, so one clone carries the whole project.

The Claude project keeps its working files in /mnt/project-files (the hand-off, the plan, the
ledger, the base design, the staged work) and its shared memory in a memory folder. Nothing there
reaches another account. This copies them into the folders of the same names here, and with
--commit and --push records and publishes them.

Rules it keeps:
- It never deletes. A file that left the source is listed for a person to remove in a reviewed
  commit, as beethoven-qa's vendor command does.
- It never overwrites a file someone changed here by hand (from another account, say). A file's
  last commit must carry the `Hub-Sync:` trailer for the copy to replace it; otherwise it is
  listed as a conflict and left alone, and the run fails until a person reconciles it.
- It copies nothing when tools/scan.py fails on any file it would copy: no secret, credential,
  patient data or unchecked binary leaves the project this way. `.hub-exclude` names what never
  comes (people's attachments, superseded snapshots), each with its reason.
- It starts from a clean tree that is not behind the branch on GitHub.

    python3 tools/sync.py [--source DIR] [--memory DIR] [--commit] [--push] [--trailer 'Key: value']...
"""
import argparse
import datetime
import filecmp
import fnmatch
import os
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import scan  # noqa: E402

FOLDERS = ["state", "plan", "ledger", "base", "github", "promo", "staging"]
TRAILER = "Hub-Sync:"


def git(*args, check=True, capture=True):
    env = {k: v for k, v in os.environ.items() if k not in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_PREFIX")}
    r = subprocess.run(["git", "-C", ROOT] + list(args), env=env,
                       stdout=subprocess.PIPE if capture else None, stderr=subprocess.PIPE if capture else None)
    if check and r.returncode:
        sys.exit("git %s failed: %s" % (" ".join(args), (r.stderr or b"").decode(errors="replace").strip()))
    return (r.stdout or b"").decode(errors="replace").strip()


def excluded():
    out = []
    path = os.path.join(ROOT, ".hub-exclude")
    if os.path.isfile(path):
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                line = line.split("#", 1)[0].strip()
                if line:
                    out.append(line)
    return out


def is_excluded(rel, patterns):
    return any(fnmatch.fnmatch(rel, p) or rel.startswith(p.rstrip("/") + "/") for p in patterns)


def plan(source, memory, patterns):
    """(source path, path here) for every file the copy covers."""
    pairs = []
    for folder in FOLDERS:
        base = os.path.join(source, folder)
        if not os.path.isdir(base):
            continue
        for d, dirs, files in os.walk(base):
            dirs[:] = sorted(x for x in dirs if not x.startswith("."))
            for f in sorted(files):
                if f.startswith("."):
                    continue
                src = os.path.join(d, f)
                rel = os.path.relpath(src, source)
                if not is_excluded(rel, patterns):
                    pairs.append((src, rel))
    if memory and os.path.isdir(memory):
        for f in sorted(os.listdir(memory)):
            if f.endswith(".md") and not f.startswith(".") and os.path.isfile(os.path.join(memory, f)):
                rel = "memory/" + f
                if not is_excluded(rel, patterns):
                    pairs.append((os.path.join(memory, f), rel))
    return pairs


def hand_edited(rel):
    """True when the file's last commit here was not a sync: someone changed it in this repository."""
    body = git("log", "-1", "--format=%B", "--", rel, check=False)
    return bool(body) and not any(line.startswith(TRAILER) for line in body.splitlines())


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--source", default=os.environ.get("HUB_SOURCE", "/mnt/project-files"))
    ap.add_argument("--memory", default=os.environ.get("HUB_MEMORY_DIR", "/tmp/claude/memory/team/silo"))
    ap.add_argument("--commit", action="store_true")
    ap.add_argument("--push", action="store_true")
    ap.add_argument("--trailer", action="append", default=[])
    a = ap.parse_args()
    if a.push:
        a.commit = True
    if not os.path.isdir(a.source):
        sys.exit("no project files at %s: this runs inside the Claude project; elsewhere, edit the files here" % a.source)
    if git("status", "--porcelain"):
        sys.exit("the tree has uncommitted changes; commit or stash them first")
    branch = git("rev-parse", "--abbrev-ref", "HEAD")
    if a.push:
        # Commits made here from another account land first, so the hand-edit check below sees them.
        git("fetch", "-q", "origin", branch, check=False)
        upstream = git("rev-parse", "-q", "--verify", "refs/remotes/origin/" + branch, check=False)
        if upstream and git("rev-list", "--count", "HEAD.." + upstream) != "0":
            if git("rev-list", "--count", upstream + "..HEAD") != "0":
                sys.exit("this branch and GitHub's have both moved; pull and reconcile first")
            git("merge", "--ff-only", "-q", upstream)

    patterns = excluded()
    pairs = plan(a.source, a.memory, patterns)
    changed, conflicts = [], []
    for src, rel in pairs:
        dst = os.path.join(ROOT, rel)
        if os.path.isfile(dst) and filecmp.cmp(src, dst, shallow=False):
            continue
        if os.path.isfile(dst) and hand_edited(rel):
            conflicts.append(rel)
            continue
        changed.append((src, rel))

    covered = {rel for _, rel in pairs}
    gone = []
    # A folder the source does not have at all says nothing about its files; only one it has does.
    present = [f for f in FOLDERS if os.path.isdir(os.path.join(a.source, f))]
    if a.memory and os.path.isdir(a.memory):
        present.append("memory")
    for folder in present:
        for d, _, files in os.walk(os.path.join(ROOT, folder)):
            for f in files:
                rel = os.path.relpath(os.path.join(d, f), ROOT)
                if rel not in covered and not is_excluded(rel, patterns) and not f.startswith("."):
                    gone.append(rel)

    # Scan the source copies before anything is written; one failure stops the whole copy.
    findings = []
    ok = scan.allowed(ROOT)
    for src, rel in changed:
        scan.scan_file(src, rel, ok, findings)
    for level, label, line, rule, what in findings:
        print("%s %s:%d %s %s" % (level.upper(), label, line, rule, what))
    if any(f[0] == "fail" for f in findings):
        sys.exit("scan failed: nothing copied (fix the source, or list a reviewed file in .hub-allow or .hub-exclude)")

    for src, rel in changed:
        dst = os.path.join(ROOT, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src, dst)
        print("copied %s" % rel)
    for rel in conflicts:
        print("CONFLICT %s: changed here by hand since the last sync; not overwritten" % rel)
    for rel in gone:
        print("GONE %s: no longer in the project files; remove it in a reviewed commit if that is meant" % rel)
    print("sync: %d copied, %d unchanged, %d conflict(s), %d gone" %
          (len(changed), len(pairs) - len(changed) - len(conflicts), len(conflicts), len(gone)))

    if a.commit and changed:
        git("add", "--", *[rel for _, rel in changed])
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
        msg = "sync: project files at %s\n\n%d file(s) from %s%s.\n\n%s %s\n" % (
            stamp, len(changed), a.source, " and the project memory" if any(r.startswith("memory/") for _, r in changed) else "",
            TRAILER, stamp)
        for t in a.trailer:
            msg += t + "\n"
        subprocess.run(["git", "-C", ROOT, "commit", "-q", "-F", "-"], input=msg.encode(), check=True)
        print("committed %s" % git("rev-parse", "--short", "HEAD"))
    if a.push and (changed or git("rev-list", "--count", "origin/%s..HEAD" % branch, check=False) not in ("", "0")):
        for wait in (0, 2, 4, 8, 16):
            time.sleep(wait)
            r = subprocess.run(["git", "-C", ROOT, "push", "-q", "-u", "origin", "HEAD:" + branch])
            if r.returncode == 0:
                print("pushed %s to %s" % (git("rev-parse", "--short", "HEAD"), branch))
                break
        else:
            sys.exit("push failed after five tries")
    return 3 if conflicts else 0


if __name__ == "__main__":
    sys.exit(main())

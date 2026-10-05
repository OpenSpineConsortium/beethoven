#!/usr/bin/env python3
"""Keep a Claude project and this hub in step in both directions, so the work can move between accounts.

A Claude project keeps its working files in /mnt/project-files (the hand-off, the plan, the
ledger, the base design, the staged work) and its shared memory in a memory folder, and nothing
there reaches another account. tools/sync.py copied them here one way, so progress made in a
project in another account could not come back. This carries changes both ways: a project in a
new account loads everything from the hub (`init`), works, and sends its progress back
(`sync --push`); the original project takes that progress in with its own `sync`. Several
projects, one per account, can share the hub this way, each with its own record, with the hub and
Linear as the common record of the work.

How it decides, per path: each project has a record here, projects/<id>/sync.json, of the bytes
both sides held when that project last synced, as git blob ids, so the hub's own history holds
every base. A side that still holds the base takes the other side's change; a side that changed
alone gives its change to the other; when both changed, a ledger file both only appended to gets
both sets of rows, and anything else is a conflict, reported and left alone until a person
reconciles it or names the side that wins with --prefer.

Rules it keeps:
- It never deletes, on either side. A file gone from one side is reported, and the other keeps it.
- It writes nothing unless tools/scan.py passes every file about to be written, in both
  directions: no secret, credential, patient data or unexamined binary moves either way.
  `.hub-exclude` names what never moves, each with its reason; the records, and everything outside
  the synced folders and memory/, stay in the hub. The harness's own dotfiles in the memory
  folder are never read or written.
- It starts from a clean tree and, with --push, from origin's branch.
- When several accounts push at once and origin has moved, this sync's commit is rebased onto
  origin's new commits when they touch none of the paths it changed, and pushed again. When they
  touch one, it stops with exit 4 and keeps its commit. The next `sync --push` finds that this
  clone's only unpushed commits are its own syncs of this project, keeps them under
  refs/hub-sync/set-aside/<id>/, moves the branch to origin's (`git reset --keep`, which refuses
  to drop an uncommitted change), and syncs again from there. For every path those commits changed
  in the hub it takes as base what origin's copy of the record still says, so the paths both sides
  changed are merged (ledger rows) or reported as conflicts. Nothing is lost: the project still
  holds what it sent, and the set-aside commits hold the rest.

    python3 tools/hub.py status [--json]
    python3 tools/hub.py sync [--commit] [--push] [--trailer 'K: v']... [--only pull|push] [--prefer hub|project]
    python3 tools/hub.py init --project-id ID [--prefer hub|project] [--commit] [--push] [--trailer ...]
    python3 tools/hub.py diff PATH
    common: --source DIR  --memory DIR  --project-id ID

Exit codes: 0 done, 1 usage or the repository's state, 2 the scan refused a file (nothing written),
3 a conflict remains (everything else synced), 4 origin moved under the push.
"""
import argparse
import collections
import datetime
import difflib
import fnmatch
import glob
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import scan  # noqa: E402

# The project folders both sides share; `sites` (the site design) too, or that work would stay
# behind in the account that wrote it.
FOLDERS = ["state", "plan", "ledger", "base", "github", "promo", "staging", "projects", "sites"]
MEMORY = "memory/"
MEMORY_GLOB = "/tmp/claude/memory/team/*/"
RECORD = re.compile(r"^projects/[^/]+/sync\.json$")
PROJECT_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
SHA = re.compile(r"^[0-9a-f]{40}$")
TRAILER = "Hub-Sync:"
WAITS = (2, 4, 8, 16)
REBASES = 3
MOVED = ("the hub moved under this sync; run `hub.py sync --push` again (this clone keeps its commit; "
         "the next run sets it aside and syncs again from origin's branch)")
MEMORY_NOTE = ("note: whether memory files written by a process other than Claude's own Write tool reach "
               "the project's memory service is not yet measured")
# git hands these to a hook, and any of them would aim every call here at another repository. The
# two configuration carriers stay, so that settings given through the environment still reach git.
GIT_LOCAL = {"GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_CONFIG", "GIT_OBJECT_DIRECTORY", "GIT_DIR",
             "GIT_WORK_TREE", "GIT_IMPLICIT_WORK_TREE", "GIT_GRAFT_FILE", "GIT_INDEX_FILE",
             "GIT_NO_REPLACE_OBJECTS", "GIT_REPLACE_REF_BASE", "GIT_PREFIX", "GIT_SHALLOW_FILE",
             "GIT_COMMON_DIR"}

Action = collections.namedtuple("Action", "path kind reason data to_project to_hub")
_quiet = False  # `status --json` keeps stdout for the JSON alone


class Stop(Exception):
    """A plain sentence for the person, and the exit code that goes with it."""

    def __init__(self, code, message):
        Exception.__init__(self, message)
        self.code = code


class Parser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        raise Stop(1, "%s: %s" % (self.prog, message))


def say(text):
    print(text, file=sys.stderr if _quiet else sys.stdout)


def plain(text):
    """git's error on one line, with any user name or token inside a URL masked."""
    return re.sub(r"(\w+://)[^/@\s]+@", r"\1***@", " ".join(text.split()))


def run_git(args, data=None):
    env = {k: v for k, v in os.environ.items() if k not in GIT_LOCAL}
    return subprocess.run(["git", "-C", ROOT] + list(args), env=env, input=data,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def git_bytes(*args, check=True):
    r = run_git(args)
    if check and r.returncode:
        raise Stop(1, "git %s failed: %s" % (args[0], plain(r.stderr.decode(errors="replace"))))
    return r.stdout


def git(*args, check=True):
    return git_bytes(*args, check=check).decode("utf-8", "replace").strip()


def blob_sha(data):
    return None if data is None else hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def base_text(sha):
    """The bytes of a base, from the hub's own objects; None when this clone does not have them."""
    r = run_git(["cat-file", "blob", sha])
    return r.stdout if r.returncode == 0 else None


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


def synced(rel, patterns):
    """True for a path both sides share: a file in a synced folder, or a top-level memory note."""
    parts = rel.split("/")
    if len(parts) < 2 or any(not p or p.startswith(".") for p in parts):
        return False
    if RECORD.match(rel) or is_excluded(rel, patterns):
        return False
    if rel.startswith(MEMORY):
        return len(parts) == 2 and rel.endswith(".md")
    return parts[0] in FOLDERS


def append_only(rel):
    return rel.startswith("ledger/") and rel.endswith(".md") and rel.count("/") == 1


def append_merge(base, mine, theirs):
    """The base, the rows the project added, then the rows the hub added that the project did not, in
    the hub's order; None when either side changed anything but the end."""
    if not (mine.startswith(base) and theirs.startswith(base)):
        return None
    left = collections.Counter(line.rstrip(b"\r\n") for line in mine[len(base):].splitlines(True))
    extra = []
    for line in theirs[len(base):].splitlines(True):
        key = line.rstrip(b"\r\n")
        if left[key]:
            left[key] -= 1
        else:
            extra.append(line)
    out = mine
    if extra and out and not out.endswith(b"\n"):
        out += b"\r\n" if b"\r\n" in mine else b"\n"
    return out + b"".join(extra)


def safe(root, rel):
    """False when rel under root passes through a link or is not a plain file: nothing goes through one."""
    path = root
    parts = rel.split("/")
    for i, part in enumerate(parts):
        path = os.path.join(path, part)
        if os.path.islink(path):
            return False
        if not os.path.exists(path):
            return True
        if i < len(parts) - 1 and not os.path.isdir(path):
            return False
    return os.path.isfile(path)


def read_file(root, rel):
    if root is None or not safe(root, rel):
        return None
    path = os.path.join(root, rel)
    if not os.path.isfile(path):
        return None
    with open(path, "rb") as fh:
        return fh.read()


def write_file(root, rel, data):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(data)


def walk(root, folder):
    """Every plain file under root/folder, relative to root, skipping dot names and links."""
    top = os.path.join(root, folder)
    if os.path.islink(top) or not os.path.isdir(top):
        return []
    out = []
    for d, dirs, files in os.walk(top):
        dirs[:] = sorted(x for x in dirs if not x.startswith(".") and not os.path.islink(os.path.join(d, x)))
        for f in sorted(files):
            full = os.path.join(d, f)
            if not f.startswith(".") and not os.path.islink(full) and os.path.isfile(full):
                out.append(os.path.relpath(full, root).replace(os.sep, "/"))
    return out


class Project:
    """The project's side: the synced folders of its files, and its memory folder when there is one."""

    def __init__(self, source, memory):
        self.source, self.memory = source, memory

    def where(self, rel):
        if rel.startswith(MEMORY):
            return self.memory, rel[len(MEMORY):]
        return self.source, rel

    def paths(self):
        out = set()
        for folder in FOLDERS:
            out.update(walk(self.source, folder))
        if self.memory:
            for f in os.listdir(self.memory):
                full = os.path.join(self.memory, f)
                if f.endswith(".md") and not f.startswith(".") and not os.path.islink(full) and os.path.isfile(full):
                    out.add(MEMORY + f)
        return out

    def read(self, rel):
        return read_file(*self.where(rel))


class WorkTree:
    """The hub as this clone has it checked out (tracked files, and untracked ones git does not ignore)."""

    def paths(self):
        out = git_bytes("ls-files", "-z", "--cached", "--others", "--exclude-standard", "--", *(FOLDERS + ["memory"]))
        return {p for p in out.decode("utf-8", "replace").split("\0") if p}

    def read(self, rel):
        return read_file(ROOT, rel)


class Commit:
    """The hub as a commit holds it: origin's branch, before this clone has moved onto it."""

    def __init__(self, rev):
        self.files = {}
        out = git_bytes("ls-tree", "-r", "-z", "--full-tree", rev, "--", *(FOLDERS + ["memory"]))
        for entry in out.decode("utf-8", "replace").split("\0"):
            if entry:
                meta, _, rel = entry.partition("\t")
                mode, kind, sha = meta.split()
                if kind == "blob" and mode in ("100644", "100755"):
                    self.files[rel] = sha

    def paths(self):
        return set(self.files)

    def read(self, rel):
        sha = self.files.get(rel)
        return None if sha is None else git_bytes("cat-file", "blob", sha)


def record_path(pid):
    return "projects/%s/sync.json" % pid


def parse_record(data, where, strict):
    """The files map of a record; None when absent, or (not strict) when unreadable."""
    if data is None:
        return None
    try:
        files = json.loads(data.decode("utf-8")).get("files")
        if isinstance(files, dict) and all(isinstance(k, str) and isinstance(v, str) and SHA.match(v)
                                           for k, v in files.items()):
            return files
    except (ValueError, AttributeError):
        pass
    if strict:
        raise Stop(1, "%s is not a record this tool wrote; a person fixes it by hand" % where)
    return None


def records(pid, hub, upstream):
    """This project's record for the pass, the record as the hub holds it, and every path any record names.

    With upstream (this clone's own unpushed syncs being set aside), the record is the one those
    syncs left, except for the paths they changed in the hub: origin never saw those changes, so the
    base for them is what origin's copy of the record says.
    """
    held = parse_record(hub.read(record_path(pid)), record_path(pid), True)
    known = set()
    for rel in hub.paths():
        if RECORD.match(rel):
            known.update(parse_record(hub.read(rel), rel, False) or {})
    record = dict(held or {})
    if upstream:
        local = parse_record(read_file(ROOT, record_path(pid)), record_path(pid), True) or {}
        known.update(local)
        record = dict(local)
        for rel in changed_paths(git("merge-base", "HEAD", upstream), "HEAD"):
            if held and rel in held:
                record[rel] = held[rel]
            else:
                record.pop(rel, None)
    return record, held, known


def ignored(paths):
    """The paths this hub's .gitignore keeps out: git would refuse to add them, so they never move."""
    if not paths:
        return set()
    r = run_git(["check-ignore", "-z", "--stdin"], data="\0".join(paths).encode() + b"\0")
    return {p for p in r.stdout.decode("utf-8", "replace").split("\0") if p}


def decide(rel, b, pdata, hdata, known, only, prefer):
    p, h = blob_sha(pdata), blob_sha(hdata)
    if b is None and p is None:
        kind, why = "PULL", "new in the hub"
    elif b is None and h is None:
        kind, why = "PUSH", "new in the project"
    elif b is not None and p == b:
        if h is None:
            return Action(rel, "GONE", "gone from the hub; nothing deleted, the project keeps its copy", None, False, False)
        kind, why = "PULL", "changed in the hub"
    elif b is not None and h == b:
        if p is None:
            return Action(rel, "GONE", "gone from the project; nothing deleted, the hub keeps its copy", None, False, False)
        kind, why = "PUSH", "changed in the project"
    else:
        return both_changed(rel, b, pdata, hdata, known, only, prefer)
    if only and kind != only.upper():
        return Action(rel, "HELD", "would %s (%s); held by --only %s" % (kind, why, only), None, False, False)
    if kind == "PULL":
        return Action(rel, kind, why, hdata, True, False)
    return Action(rel, kind, why, pdata, False, True)


def both_changed(rel, b, pdata, hdata, known, only, prefer):
    merged = None
    if append_only(rel) and pdata is not None and hdata is not None:
        # With no base, an empty one is safe only when no record ever named the path: otherwise
        # rows may have been taken out on one side, and that is for a person to see.
        base = base_text(b) if b is not None else (None if rel in known else b"")
        if base is not None:
            merged = append_merge(base, pdata, hdata)
    if merged is not None and not only:
        if merged == pdata:
            why = "rows added; the project's copy already holds every row the hub's has"
        elif merged == hdata:
            why = "rows added; the hub's copy already holds every row the project's has"
        else:
            why = "rows added on both sides; the project's first, then the hub's"
        return Action(rel, "MERGED", why, merged, merged != pdata, merged != hdata)
    if prefer == "hub" and hdata is not None and only != "push":
        return Action(rel, "PULL", "changed on both sides; --prefer hub", hdata, True, False)
    if prefer == "project" and pdata is not None and only != "pull":
        return Action(rel, "PUSH", "changed on both sides; --prefer project", pdata, False, True)
    if merged is not None:
        why = "rows added on both sides; a merge writes both sides, which --only %s does not allow" % only
    elif pdata is None:
        why = "gone from the project and changed in the hub; nothing written, nothing deleted"
    elif hdata is None:
        why = "gone from the hub and changed in the project; nothing written, nothing deleted"
    else:
        why = ("%s; nothing written (see `hub.py diff %s`, reconcile by hand, or run again with --prefer hub "
               "or --prefer project)" % ("changed on both sides since the last sync" if b else
                                         "the two sides differ and no record says which one changed", rel))
    return Action(rel, "CONFLICT", why, None, False, False)


def three_way(project, hub, record, decide_from, known, patterns, only, prefer):
    """The actions for every path either side or the record knows, the count left as it was, and the
    base of every path that already ends equal on both sides."""
    candidates = {rel for rel in set(record) | project.paths() | hub.paths()
                  if synced(rel, patterns) and (project.memory or not rel.startswith(MEMORY))}
    actions, unchanged, final = [], 0, {}
    for rel in sorted(candidates - ignored(sorted(candidates))):
        pdata, hdata = project.read(rel), hub.read(rel)
        if pdata == hdata:
            if pdata is not None:
                final[rel] = blob_sha(pdata)
                unchanged += 1
            continue
        actions.append(decide(rel, decide_from.get(rel), pdata, hdata, known, only, prefer))
    return actions, unchanged, final


def counts(actions):
    n = collections.Counter(a.kind for a in actions)
    return n, "%d pushed, %d pulled, %d merged, %d conflict(s), %d gone" % (
        n["PUSH"], n["PULL"], n["MERGED"], n["CONFLICT"], n["GONE"])


def summary_line(word, actions, unchanged):
    n, text = counts(actions)
    return "%s: %s, %d unchanged%s" % (word, text, unchanged, ", %d held" % n["HELD"] if n["HELD"] else "")


def memory_dir(given):
    chosen = given or os.environ.get("HUB_MEMORY_DIR")
    if chosen:
        if not os.path.isdir(chosen):
            raise Stop(1, "no memory folder at %s" % chosen)
        return os.path.abspath(chosen)
    found = sorted(d for d in glob.glob(MEMORY_GLOB) if os.path.isfile(os.path.join(d, ".memory-sync")))
    if len(found) == 1:
        return os.path.abspath(found[0])
    say("memory: skipped, %s; name it with --memory to include it" %
        ("no memory folder found" if not found else "%d memory folders found" % len(found)))
    return None


def resolve(a, init):
    """The project's files, its memory folder and its id, checked against the id the files carry."""
    source = a.source or os.environ.get("HUB_SOURCE") or "/mnt/project-files"
    if not os.path.isdir(source):
        raise Stop(1, "no project files at %s: this runs inside a Claude project, or name them with --source" % source)
    source = os.path.abspath(source)
    stored = None
    marker = os.path.join(source, ".hub-project")
    if os.path.isfile(marker):
        with open(marker, encoding="utf-8") as fh:
            stored = fh.readline().strip() or None
    if init:
        pid = a.project_id
        if not pid:
            raise Stop(1, "init needs --project-id ID")
    else:
        pid = a.project_id or os.environ.get("HUB_PROJECT_ID") or stored
        if not pid:
            raise Stop(1, "no project id: run `hub.py init --project-id ID` once in this project, or set HUB_PROJECT_ID")
    if not PROJECT_ID.match(pid):
        raise Stop(1, "a project id is letters, digits, '.', '_' and '-', starting with a letter or digit")
    if stored and stored != pid:
        raise Stop(1, "%s says these files belong to project %s, not %s; nothing written" % (marker, stored, pid))
    return source, memory_dir(a.memory), pid, stored


def changed_paths(a, b):
    out = git_bytes("diff", "--name-only", "-z", "--no-renames", a, b)
    return {p for p in out.decode("utf-8", "replace").split("\0") if p}


def own_commits(rng, pid):
    """True when every commit in rng is a sync of this project made by this tool."""
    bodies = [b for b in git_bytes("log", "-z", "--format=%B", rng).decode("utf-8", "replace").split("\0") if b.strip()]
    mark = "Hub-Project: %s" % pid
    return bool(bodies) and all(
        any(line.startswith(TRAILER) for line in b.splitlines()) and mark in [line.strip() for line in b.splitlines()]
        for b in bodies)


def upstream_of(branch):
    return git("rev-parse", "-q", "--verify", "refs/remotes/origin/%s^{commit}" % branch, check=False)


def fetch(branch):
    """Fetch origin's branch, trying again after a network failure; False when origin has no such branch."""
    err = ""
    for wait in (0,) + WAITS:
        if wait:
            say("fetch failed (%s); trying again in %d s" % (err, wait))
            time.sleep(wait)
        r = run_git(["fetch", "-q", "origin", "+refs/heads/%s:refs/remotes/origin/%s" % (branch, branch)])
        if r.returncode == 0:
            return True
        err = plain(r.stderr.decode(errors="replace"))
        if "couldn't find remote ref" in err:
            return False
    raise Stop(1, "could not fetch origin's %s after five tries: %s" % (branch, err))


def catch_up(branch, pid):
    """Bring this clone up to origin's branch. Returns origin's commit when this clone's own unpushed
    syncs of this project must be set aside first (see the module's last rule), else None."""
    upstream = upstream_of(branch)
    if not upstream or git("rev-list", "--count", "HEAD..%s" % upstream) == "0":
        return None
    if git("rev-list", "--count", "%s..HEAD" % upstream) == "0":
        git("merge", "--ff-only", "-q", upstream)
        say("fast-forwarded to origin's %s" % branch)
        return None
    if own_commits("%s..HEAD" % upstream, pid):
        say("origin's %s moved since this clone's last sync of project %s was committed; syncing again from origin's" % (branch, pid))
        return upstream
    raise Stop(1, "this branch and origin's have both moved; pull and reconcile first")


def set_aside(pid, upstream):
    head = git("rev-parse", "HEAD")
    ref = "refs/hub-sync/set-aside/%s/%s" % (pid, head[:12])
    git("update-ref", ref, head)
    git("reset", "-q", "--keep", upstream)
    say("kept this clone's unpushed sync commit(s) as %s and moved to origin's branch" % ref)


def push_once(branch):
    """One push of HEAD to origin's branch: (True, "") when it landed, else (False, git's error)."""
    r = run_git(["push", "-q", "origin", "HEAD:refs/heads/%s" % branch])
    return r.returncode == 0, plain(r.stderr.decode(errors="replace"))


def refused(err):
    return any(word in err for word in ("rejected", "non-fast-forward", "fetch first"))


def rebase_onto_origin(branch, pid, err):
    """After origin refused the push: True when this run's commits now sit on origin's new ones."""
    fetch(branch)
    upstream = upstream_of(branch)
    if not upstream or git("rev-list", "--count", "HEAD..%s" % upstream) == "0":
        raise Stop(1, "origin refused the push and has not moved: %s" % err)
    fork = git("merge-base", "HEAD", upstream)
    if not own_commits("%s..HEAD" % fork, pid):
        say("this clone has unpushed commits that are not this project's syncs; not rebasing them")
        return False
    both = changed_paths(fork, "HEAD") & changed_paths(fork, upstream)
    if both:
        say("origin's new commits change %s, which this sync changed too" % ", ".join(sorted(both)))
        return False
    if run_git(["rebase", "-q", upstream]).returncode:
        run_git(["rebase", "--abort"])
        return False
    say("rebased onto origin's new commits, which change none of this sync's paths")
    return True


def push(branch, pid, on_origin):
    upstream = upstream_of(branch)
    if on_origin and upstream and git("rev-list", "--count", "%s..HEAD" % upstream) == "0":
        return
    for attempt in range(REBASES + 1):
        err = ""
        for wait in (0,) + WAITS:
            if wait:
                say("push failed (%s); trying again in %d s" % (err, wait))
                time.sleep(wait)
            ok, err = push_once(branch)
            err = plain(err)
            if ok:
                say("pushed %s to origin's %s" % (git("rev-parse", "--short", "HEAD"), branch))
                return
            if refused(err):
                break
        else:
            raise Stop(1, "the push failed after five tries (%s); the commit is kept here: run `hub.py sync --push` again" % err)
        if attempt == REBASES or not rebase_onto_origin(branch, pid, err):
            raise Stop(4, MOVED)


def sync(a, init):
    source, memory, pid, stored = resolve(a, init)
    project = Project(source, memory)
    only, prefer = getattr(a, "only", None), a.prefer
    if a.push:
        a.commit = True
    branch = git("rev-parse", "--abbrev-ref", "HEAD")
    if git("status", "--porcelain"):
        raise Stop(1, "the hub has uncommitted changes; commit or stash them first. Nothing written")
    if a.commit and run_git(["var", "GIT_COMMITTER_IDENT"]).returncode:
        raise Stop(1, "git has no name and e-mail to commit with here; set user.name and user.email first. Nothing written")
    upstream, on_origin = None, False
    if a.push:
        if branch == "HEAD":
            raise Stop(1, "the hub is not on a branch; check one out first")
        if run_git(["remote", "get-url", "origin"]).returncode:
            raise Stop(1, "this hub has no remote named origin to push to. Nothing written")
        on_origin = fetch(branch)
        upstream = catch_up(branch, pid) if on_origin else None
    hub = Commit(upstream) if upstream else WorkTree()
    record, held, known = records(pid, hub, upstream)
    actions, unchanged, final = three_way(project, hub, record, {} if init else record, known, excluded(), only, prefer)

    # Scan exactly the bytes about to be written, both ways, before anything is; one failure stops all.
    findings = []
    ok = scan.allowed(ROOT)
    with tempfile.TemporaryDirectory(prefix="hub-scan-") as tmp:
        for n, act in enumerate(x for x in actions if x.to_project or x.to_hub):
            path = os.path.join(tmp, str(n))
            with open(path, "wb") as fh:
                fh.write(act.data)
            scan.scan_file(path, act.path, ok, findings)
    for level, label, line, rule, what in findings:
        say("%s %s:%d %s %s" % (level.upper(), label, line, rule, what))
    if any(f[0] == "fail" for f in findings):
        raise Stop(2, "scan failed: nothing written on either side (fix the file, or list a reviewed one "
                      "in .hub-allow or .hub-exclude)")
    for act in actions:
        if act.to_project and not safe(*project.where(act.path)):
            raise Stop(1, "%s in the project passes through a link or is not a plain file; nothing written" % act.path)
        if act.to_hub and not safe(ROOT, act.path):
            raise Stop(1, "%s in the hub passes through a link or is not a plain file; nothing written" % act.path)

    if upstream:
        set_aside(pid, upstream)
    if init and stored != pid:
        write_file(source, ".hub-project", (pid + "\n").encode())
    wrote_memory = False
    for act in actions:
        try:
            if act.to_project:
                write_file(*project.where(act.path), act.data)
                wrote_memory = wrote_memory or act.path.startswith(MEMORY)
            if act.to_hub:
                write_file(ROOT, act.path, act.data)
        except OSError as e:
            raise Stop(1, "could not write %s: %s; the record is left as it was" % (act.path, e.strerror))
        if act.kind in ("PULL", "PUSH", "MERGED"):
            final[act.path] = blob_sha(act.data)

    # Only paths that ended equal move their base; a conflict, a gone file or a held one keeps its old one.
    new = dict(record)
    new.update(final)
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    if held is None or new != held:
        text = json.dumps({"project_id": pid, "updated_utc": stamp, "files": new}, indent=1, sort_keys=True) + "\n"
        write_file(ROOT, record_path(pid), text.encode())
        fresh = sorted(rel for rel in final if (held or {}).get(rel) != final[rel])
        if fresh:
            # The base of every path is then in this clone's objects even before a commit holds it.
            run_git(["hash-object", "-w", "--no-filters", "--stdin-paths"], data="\n".join(fresh).encode() + b"\n")

    for act in actions:
        say("%-8s %s: %s" % (act.kind, act.path, act.reason))
    say(summary_line("sync", actions, unchanged))
    if wrote_memory:
        say(MEMORY_NOTE)
    n, text = counts(actions)
    if git("status", "--porcelain"):
        if a.commit:
            git("add", "--", *([x.path for x in actions if x.to_hub] + [record_path(pid)]))
            msg = "sync: project %s at %s\n\n%s\n\n%s %s\nHub-Project: %s\n" % (pid, stamp, text, TRAILER, stamp, pid)
            for t in a.trailer:
                msg += t + "\n"
            r = run_git(["commit", "-q", "-F", "-"], data=msg.encode())
            if r.returncode:
                raise Stop(1, "git commit failed: %s" % plain(r.stderr.decode(errors="replace")))
            say("committed %s" % git("rev-parse", "--short", "HEAD"))
        else:
            say("nothing committed: the hub's changes are in its working tree; commit them, or run with --commit")
    if a.push:
        push(branch, pid, on_origin)
    return 3 if n["CONFLICT"] else 0


def status(a):
    global _quiet
    _quiet = a.json
    source, memory, pid, _ = resolve(a, False)
    hub = WorkTree()
    record, held, known = records(pid, hub, None)
    if held is None:
        say("no record for project %s in this hub yet: this is what `init` would do" % pid)
    actions, unchanged, _ = three_way(Project(source, memory), hub, record, record, known, excluded(), a.only, a.prefer)
    if a.json:
        n, _ = counts(actions)
        print(json.dumps({
            "actions": [{"path": x.path, "action": x.kind, "reason": x.reason} for x in actions],
            "summary": {"pushed": n["PUSH"], "pulled": n["PULL"], "merged": n["MERGED"], "conflicts": n["CONFLICT"],
                        "gone": n["GONE"], "held": n["HELD"], "unchanged": unchanged}}, indent=1))
        return 0
    for act in actions:
        say("%-8s %s: %s" % (act.kind, act.path, act.reason))
    say(summary_line("status", actions, unchanged) + "; nothing written")
    return 0


def diff(a):
    source, memory, pid, _ = resolve(a, False)
    rel = a.path.replace(os.sep, "/")
    if rel.startswith("./"):
        rel = rel[2:]
    if not synced(rel, excluded()):
        raise Stop(1, "%s is not a path the project and the hub share" % rel)
    record, _, _ = records(pid, WorkTree(), None)
    b = record.get(rel)
    base = base_text(b) if b else None
    if b and base is None:
        say("the base of %s (%s) is not in this clone's objects; showing it as empty" % (rel, b[:12]))
    sides = [("base %s" % (b[:12] if b else "(none)"), base), ("project", Project(source, memory).read(rel)),
             ("hub", WorkTree().read(rel))]
    pairs = [(sides[0], sides[1]), (sides[0], sides[2])] + ([] if b else [(sides[1], sides[2])])
    for (left, old), (right, new) in pairs:
        lines = [x if x.endswith("\n") else x + "\n" for x in difflib.unified_diff(
            (old or b"").decode("utf-8", "replace").splitlines(True), (new or b"").decode("utf-8", "replace").splitlines(True),
            left, right + ("" if new is not None else " (absent)"))]
        say("".join(lines).rstrip("\n") if lines else "%s and %s are the same" % (left, right))
    return 0


def parser():
    common = Parser(add_help=False)
    common.add_argument("--source", help="the project's files (default $HUB_SOURCE, else /mnt/project-files)")
    common.add_argument("--memory", help="the project's memory folder (default $HUB_MEMORY_DIR, else the one "
                                         "folder under %s that holds .memory-sync)" % MEMORY_GLOB)
    common.add_argument("--project-id", help="this project's id (default $HUB_PROJECT_ID, else <source>/.hub-project)")
    ap = Parser(prog="hub.py", description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="command", metavar="{status,sync,init,diff}")
    sub.required = True
    st = sub.add_parser("status", parents=[common], help="what sync would do, per path; writes nothing")
    st.add_argument("--json", action="store_true")
    st.add_argument("--only", choices=("pull", "push"))
    st.add_argument("--prefer", choices=("hub", "project"))
    for name, text in (("sync", "carry changes both ways since this project's last sync"),
                       ("init", "first sync of a project: name it, adopt what is equal, copy what one side lacks")):
        s = sub.add_parser(name, parents=[common], help=text)
        s.add_argument("--commit", action="store_true")
        s.add_argument("--push", action="store_true", help="fetch first, commit, and push (implies --commit)")
        s.add_argument("--trailer", action="append", default=[], help="a 'Key: value' line for the commit")
        s.add_argument("--prefer", choices=("hub", "project"), help="the side that wins a conflict")
        if name == "sync":
            s.add_argument("--only", choices=("pull", "push"), help="carry changes one way only")
    d = sub.add_parser("diff", parents=[common], help="the base, project and hub versions of one path")
    d.add_argument("path")
    return ap


def main(argv=None):
    global _quiet
    _quiet = False
    try:
        a = parser().parse_args(argv)
        if a.command == "status":
            return status(a)
        if a.command == "diff":
            return diff(a)
        return sync(a, a.command == "init")
    except Stop as e:
        print(str(e), file=sys.stderr)
        return e.code


if __name__ == "__main__":
    sys.exit(main())

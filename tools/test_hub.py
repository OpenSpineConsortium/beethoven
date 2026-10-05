#!/usr/bin/env python3
"""Tests for tools/hub.py: two projects in two accounts sharing one hub, all in temporary folders.

Each test builds a bare repository as origin, a hub seeded from this checkout's own tools and
attributes, two clones of it, two project file folders A and B and two memory folders, each with
the harness's dotfiles, which must never move. Nothing here touches /mnt/project-files, the real
memory folder or any network remote.

    python3 -m unittest tools/test_hub.py        or        python3 tools/test_hub.py
"""
import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

TOOLS = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(TOOLS)
sys.path.insert(0, TOOLS)
import hub  # noqa: E402

SEEDED = {
    "state/HYDRATE.md": b"# Hydrate\n\nRead this first.\n",
    "state/repos/hpcworker.md": b"# hpcworker\n\nThe cluster side.\n",
    "plan/BUILD_PLAN.md": b"# Plan\n\n1. Build the hub.\n",
    "ledger/LEDGER.md": b"| date | activity |\n| --- | --- |\n| 2026-10-04 | first row |\n",
    "staging/README.md": b"# Staging\n",
}
NOTES = {"MEMORY.md": b"- [A fact](fact.md)\n", "fact.md": b"A fact the project keeps.\n"}
HUB_ONLY = {"README.md": b"# Hub\n", "linear/ISSUES.md": b"# Issues\n\nBEE-1 open.\n"}
DOTFILES = {".memory-sync": b"harness: do not copy\n", ".memory-sync-basis": b"harness basis\n"}
# Built at run time so that this file itself passes tools/scan.py.
PRIVATE_KEY = ("-----BEGIN %s PRIVATE KEY-----\nAAAA\n-----END %s PRIVATE KEY-----\n" % ("OPENSSH", "OPENSSH")).encode()


def put(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(data)


def get(path):
    if not os.path.isfile(path):
        return None
    with open(path, "rb") as fh:
        return fh.read()


def snapshot(root):
    out = {}
    for d, _, files in os.walk(root):
        for f in files:
            full = os.path.join(d, f)
            out[os.path.relpath(full, root).replace(os.sep, "/")] = get(full)
    return out


class HubTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="hub-test-")
        self.addCleanup(shutil.rmtree, self.tmp, True)
        env = {k: v for k, v in os.environ.items() if not k.startswith(("GIT_", "HUB_"))}
        env.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1", GIT_AUTHOR_NAME="Test",
                   GIT_AUTHOR_EMAIL="test@example.com", GIT_COMMITTER_NAME="Test",
                   GIT_COMMITTER_EMAIL="test@example.com", PYTHONDONTWRITEBYTECODE="1")
        self.env = env
        self.origin = self.path("origin.git")
        self.git(self.tmp, "init", "-q", "--bare", "-b", "main", self.origin)
        seed = self.path("seed")
        self.git(self.tmp, "init", "-q", "-b", "main", seed)
        for rel in ("tools/hub.py", "tools/scan.py", "tools/sync.py", ".gitattributes", ".hub-exclude", ".gitignore"):
            put(os.path.join(seed, rel), get(os.path.join(REPO, rel)))
        for rel, data in list(SEEDED.items()) + list(HUB_ONLY.items()):
            put(os.path.join(seed, rel), data)
        for name, data in NOTES.items():
            put(os.path.join(seed, "memory", name), data)
        self.git(seed, "add", "-A")
        self.git(seed, "commit", "-q", "-m", "seed")
        self.git(seed, "push", "-q", self.origin, "main")
        self.hub_a, self.hub_b, self.hub_c = (self.clone(n) for n in ("hub-a", "hub-b", "hub-c"))
        self.src_a, self.src_b = self.path("project-a"), self.path("project-b")
        self.mem_a, self.mem_b = self.path("memory-a"), self.path("memory-b")
        for rel, data in SEEDED.items():
            put(os.path.join(self.src_a, rel), data)
        for name, data in NOTES.items():
            put(os.path.join(self.mem_a, name), data)
        for folder in ("state", "plan", "ledger", "base", "github", "promo", "staging"):
            os.makedirs(os.path.join(self.src_b, folder))
        for mem in (self.mem_a, self.mem_b):
            for name, data in DOTFILES.items():
                put(os.path.join(mem, name), data)

    def tearDown(self):
        # 12: the harness's dotfiles are untouched after every test, and never reach the hub.
        for mem in (self.mem_a, self.mem_b):
            for name, data in DOTFILES.items():
                self.assertEqual(get(os.path.join(mem, name)), data, "%s in %s changed" % (name, mem))
        for clone in (self.hub_a, self.hub_b, self.hub_c):
            self.assertFalse(os.path.exists(os.path.join(clone, "memory", ".memory-sync")))
        self.assertNotIn(".memory-sync", self.git(self.origin, "ls-tree", "-r", "--name-only", "main"))

    # helpers

    def path(self, *parts):
        return os.path.join(self.tmp, *parts)

    def git(self, where, *args):
        r = subprocess.run(["git", "-C", where] + list(args), env=self.env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if r.returncode:
            raise AssertionError("git %s: %s" % (" ".join(args), r.stderr.decode()))
        return r.stdout.decode()

    def clone(self, name):
        where = self.path(name)
        self.git(self.tmp, "clone", "-q", self.origin, where)
        return where

    def run_hub(self, clone, src, mem, *args, script="hub.py"):
        cmd = [sys.executable, os.path.join(clone, "tools", script)] + list(args) + ["--source", src, "--memory", mem]
        r = subprocess.run(cmd, env=self.env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return r.returncode, r.stdout.decode()

    def a(self, *args):
        return self.run_hub(self.hub_a, self.src_a, self.mem_a, *args)

    def b(self, *args):
        return self.run_hub(self.hub_b, self.src_b, self.mem_b, *args)

    def in_process(self, clone, src, mem, *args):
        """hub.main in this process, so a test can step in between its fetch and its push."""
        out = io.StringIO()
        with mock.patch.dict(os.environ, self.env, clear=True), mock.patch.object(hub, "ROOT", clone), \
                contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            code = hub.main(list(args) + ["--source", src, "--memory", mem])
        return code, out.getvalue()

    def hand_commit(self, clone, files, message="by hand"):
        """A person's commit in another clone, pushed to origin."""
        self.git(clone, "pull", "-q", "--ff-only", "origin", "main")
        for rel, data in files.items():
            put(os.path.join(clone, rel), data)
        self.git(clone, "add", "-A")
        self.git(clone, "commit", "-q", "-m", message)
        self.git(clone, "push", "-q", "origin", "HEAD:main")

    def at_origin(self, rel):
        r = subprocess.run(["git", "-C", self.origin, "cat-file", "blob", "main:" + rel], env=self.env,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return r.stdout if r.returncode == 0 else None

    def head(self, where, rev="HEAD"):
        return self.git(where, "rev-parse", rev).strip()

    def record(self, pid):
        return json.loads(self.at_origin("projects/%s/sync.json" % pid).decode())

    def ok(self, result, code=0):
        self.assertEqual(result[0], code, result[1])
        return result[1]

    def init_both(self):
        self.ok(self.a("init", "--project-id", "proj-a", "--push"))
        self.ok(self.b("init", "--project-id", "proj-b", "--push"))

    def lines(self, out, kind):
        return sorted(line.split()[1].rstrip(":") for line in out.splitlines() if line.startswith(kind + " "))

    # 1-14 of the specification, then the rest of the contract

    def test_01_init_adopts_equal_state(self):
        before = snapshot(self.src_a)
        out = self.ok(self.a("init", "--project-id", "proj-a", "--push"))
        for kind in ("PULL", "PUSH", "MERGED", "CONFLICT", "GONE"):
            self.assertEqual(self.lines(out, kind), [], out)
        self.assertEqual(snapshot(self.src_a), dict(before, **{".hub-project": b"proj-a\n"}))
        rec = self.record("proj-a")
        self.assertEqual(rec["project_id"], "proj-a")
        expected = dict(SEEDED, **{"memory/" + k: v for k, v in NOTES.items()})
        self.assertEqual(rec["files"], {rel: hub.blob_sha(data) for rel, data in expected.items()})
        self.assertEqual(self.git(self.origin, "show", "--name-only", "--format=", "main").split(), ["projects/proj-a/sync.json"])
        msg = self.git(self.origin, "log", "-1", "--format=%B", "main")
        self.assertIn("0 pushed, 0 pulled, 0 merged, 0 conflict(s), 0 gone", msg)
        self.assertIn("Hub-Project: proj-a", msg)
        self.assertIn("Hub-Sync: ", msg)

    def test_02_init_from_empty_loads_everything(self):
        self.ok(self.a("init", "--project-id", "proj-a", "--push"))
        out = self.ok(self.b("init", "--project-id", "proj-b", "--push"))
        for rel, data in SEEDED.items():
            self.assertEqual(get(os.path.join(self.src_b, rel)), data, rel)
        for name, data in NOTES.items():
            self.assertEqual(get(os.path.join(self.mem_b, name)), data, name)
        self.assertEqual(get(os.path.join(self.src_b, ".hub-project")), b"proj-b\n")
        self.assertEqual(len(self.lines(out, "PULL")), len(SEEDED) + len(NOTES))
        self.assertIn(hub.MEMORY_NOTE, out)
        for rel in HUB_ONLY:
            self.assertFalse(os.path.exists(os.path.join(self.src_b, rel)), rel)
        self.assertEqual(set(self.record("proj-b")["files"]), set(self.record("proj-a")["files"]))

    def test_03_progress_in_b_comes_back_to_a(self):
        self.init_both()
        put(os.path.join(self.src_b, "state/HYDRATE.md"), b"# Hydrate\n\nRead this first. B was here.\n")
        put(os.path.join(self.mem_b, "fact.md"), b"A fact, corrected in B.\n")
        put(os.path.join(self.mem_b, "new-note.md"), b"A note first written in B.\n")
        out = self.ok(self.b("sync", "--push"))
        self.assertEqual(self.lines(out, "PUSH"), ["memory/fact.md", "memory/new-note.md", "state/HYDRATE.md"])
        out = self.ok(self.a("sync", "--push"))
        self.assertEqual(self.lines(out, "PULL"), ["memory/fact.md", "memory/new-note.md", "state/HYDRATE.md"])
        self.assertEqual(get(os.path.join(self.src_a, "state/HYDRATE.md")), b"# Hydrate\n\nRead this first. B was here.\n")
        self.assertEqual(get(os.path.join(self.mem_a, "fact.md")), b"A fact, corrected in B.\n")
        self.assertEqual(get(os.path.join(self.mem_a, "new-note.md")), b"A note first written in B.\n")
        self.assertIn(hub.MEMORY_NOTE, out)
        self.assertEqual(self.record("proj-a")["files"]["state/HYDRATE.md"], self.record("proj-b")["files"]["state/HYDRATE.md"])

    def test_04_different_files_flow_both_ways(self):
        self.init_both()
        put(os.path.join(self.src_a, "plan/BUILD_PLAN.md"), b"# Plan\n\n1. Build the hub.\n2. From A.\n")
        put(os.path.join(self.src_b, "state/HYDRATE.md"), b"# Hydrate\n\nFrom B.\n")
        put(os.path.join(self.src_b, "state/new-in-b.md"), b"new in B\n")
        self.ok(self.a("sync", "--push"))
        out = self.ok(self.b("sync", "--push"))
        self.assertEqual(self.lines(out, "PULL"), ["plan/BUILD_PLAN.md"])
        self.assertEqual(self.lines(out, "PUSH"), ["state/HYDRATE.md", "state/new-in-b.md"])
        self.ok(self.a("sync", "--push"))
        for src in (self.src_a, self.src_b):
            self.assertEqual(get(os.path.join(src, "plan/BUILD_PLAN.md")), b"# Plan\n\n1. Build the hub.\n2. From A.\n")
            self.assertEqual(get(os.path.join(src, "state/HYDRATE.md")), b"# Hydrate\n\nFrom B.\n")
            self.assertEqual(get(os.path.join(src, "state/new-in-b.md")), b"new in B\n")

    def test_05_same_file_is_a_conflict_until_a_side_is_named(self):
        self.init_both()
        put(os.path.join(self.src_a, "state/HYDRATE.md"), b"A's version\n")
        put(os.path.join(self.src_a, "plan/BUILD_PLAN.md"), b"A's plan\n")
        put(os.path.join(self.src_b, "state/HYDRATE.md"), b"B's version\n")
        self.ok(self.a("sync", "--push"))
        base = self.record("proj-b")["files"]["state/HYDRATE.md"]
        out = self.ok(self.b("sync", "--push"), 3)
        self.assertEqual(self.lines(out, "CONFLICT"), ["state/HYDRATE.md"])
        self.assertEqual(self.lines(out, "PULL"), ["plan/BUILD_PLAN.md"])
        self.assertEqual(get(os.path.join(self.src_b, "state/HYDRATE.md")), b"B's version\n")
        self.assertEqual(get(os.path.join(self.src_b, "plan/BUILD_PLAN.md")), b"A's plan\n")
        self.assertEqual(self.at_origin("state/HYDRATE.md"), b"A's version\n")
        self.assertEqual(get(os.path.join(self.hub_b, "state/HYDRATE.md")), b"A's version\n")
        self.assertEqual(self.record("proj-b")["files"]["state/HYDRATE.md"], base)
        diff = self.ok(self.b("diff", "state/HYDRATE.md"))
        self.assertIn("+B's version", diff)
        self.assertIn("+A's version", diff)
        out = self.ok(self.b("sync", "--push", "--prefer", "hub"))
        self.assertEqual(self.lines(out, "PULL"), ["state/HYDRATE.md"])
        self.assertEqual(get(os.path.join(self.src_b, "state/HYDRATE.md")), b"A's version\n")
        self.assertEqual(self.record("proj-b")["files"]["state/HYDRATE.md"], hub.blob_sha(b"A's version\n"))
        put(os.path.join(self.src_a, "state/HYDRATE.md"), b"A again\n")
        self.ok(self.a("sync", "--push"))
        put(os.path.join(self.src_b, "state/HYDRATE.md"), b"B again\n")
        self.ok(self.b("sync", "--push"), 3)
        out = self.ok(self.b("sync", "--push", "--prefer", "project"))
        self.assertEqual(self.lines(out, "PUSH"), ["state/HYDRATE.md"])
        self.assertEqual(self.at_origin("state/HYDRATE.md"), b"B again\n")

    def test_06_ledger_rows_from_both_sides_merge(self):
        self.init_both()
        base = SEEDED["ledger/LEDGER.md"]
        same = b"| 2026-10-05 | a row both sides wrote |\n"
        put(os.path.join(self.src_a, "ledger/LEDGER.md"), base + same + b"| 2026-10-05 | row from A |\n")
        put(os.path.join(self.src_b, "ledger/LEDGER.md"),
            base + b"| 2026-10-05 | row from B |\n| 2026-10-05 | second from B |\n" + same)
        self.ok(self.a("sync", "--push"))
        out = self.ok(self.b("sync", "--push"))
        self.assertEqual(self.lines(out, "MERGED"), ["ledger/LEDGER.md"])
        self.ok(self.a("sync", "--push"))
        merged = base + b"| 2026-10-05 | row from B |\n| 2026-10-05 | second from B |\n" + same + b"| 2026-10-05 | row from A |\n"
        for where in (self.src_a, self.src_b, self.hub_a, self.hub_b):
            self.assertEqual(get(os.path.join(where, "ledger/LEDGER.md")), merged, where)
        self.assertEqual(self.at_origin("ledger/LEDGER.md"), merged)
        rows = merged.splitlines()
        self.assertEqual(len(rows), len(set(rows)), "a row was doubled")

    def test_07_a_deleted_file_is_reported_and_kept(self):
        self.init_both()
        os.remove(os.path.join(self.src_b, "plan/BUILD_PLAN.md"))  # the person's own deletion, in this test's folder
        out = self.ok(self.b("sync", "--push"))
        self.assertEqual(self.lines(out, "GONE"), ["plan/BUILD_PLAN.md"])
        self.assertEqual(self.at_origin("plan/BUILD_PLAN.md"), SEEDED["plan/BUILD_PLAN.md"])
        self.assertEqual(get(os.path.join(self.hub_b, "plan/BUILD_PLAN.md")), SEEDED["plan/BUILD_PLAN.md"])
        self.ok(self.a("sync", "--push"))
        self.assertEqual(get(os.path.join(self.src_a, "plan/BUILD_PLAN.md")), SEEDED["plan/BUILD_PLAN.md"])
        # The other way: a person removes a memory note from the hub.
        self.git(self.hub_c, "pull", "-q", "--ff-only", "origin", "main")
        self.git(self.hub_c, "rm", "-q", "memory/fact.md")
        self.git(self.hub_c, "commit", "-q", "-m", "drop a note")
        self.git(self.hub_c, "push", "-q", "origin", "HEAD:main")
        out = self.ok(self.a("sync", "--push"))
        self.assertEqual(self.lines(out, "GONE"), ["memory/fact.md"])
        self.assertEqual(get(os.path.join(self.mem_a, "fact.md")), NOTES["fact.md"])
        self.assertIn("memory/fact.md", self.record("proj-a")["files"])

    def test_08_a_secret_on_either_side_stops_everything(self):
        self.init_both()
        put(os.path.join(self.src_b, "plan/BUILD_PLAN.md"), b"# Plan from B\n")
        self.ok(self.b("sync", "--push"))
        put(os.path.join(self.src_a, "state/keys.md"), PRIVATE_KEY)
        put(os.path.join(self.src_a, "state/HYDRATE.md"), b"A changed this too\n")
        project, memory, top = snapshot(self.src_a), snapshot(self.mem_a), self.head(self.origin, "main")
        out = self.ok(self.a("sync", "--push"), 2)
        self.assertIn("private-key", out)
        self.assertNotIn("OPENSSH", out)
        self.assertEqual((snapshot(self.src_a), snapshot(self.mem_a)), (project, memory))
        self.assertEqual(self.head(self.origin, "main"), top)
        self.assertEqual(self.head(self.hub_a), top)
        self.assertEqual(self.git(self.hub_a, "status", "--porcelain"), "")
        # The other way: a secret committed to the hub by hand never reaches a project.
        os.remove(os.path.join(self.src_a, "state/keys.md"))
        self.hand_commit(self.hub_c, {"state/oops.md": PRIVATE_KEY})
        project, top = snapshot(self.src_a), self.head(self.origin, "main")
        out = self.ok(self.a("sync", "--push"), 2)
        self.assertIn("state/oops.md", out)
        self.assertEqual(snapshot(self.src_a), project)
        self.assertEqual(self.head(self.origin, "main"), top)
        self.assertEqual(self.head(self.hub_a), top)

    def test_09_hub_only_and_excluded_paths_never_move(self):
        self.ok(self.a("init", "--project-id", "proj-a", "--push"))
        put(os.path.join(self.src_a, "uploads/x.png"), b"\x89PNG\r\n\x1a\n\0\0")
        put(os.path.join(self.src_a, "staging/beethoven-qa.bundle"), b"superseded\n")
        put(os.path.join(self.src_a, "state/.hidden.md"), b"a dotfile\n")
        put(os.path.join(self.src_a, "projects/proj-a/sync.json"), b'{"files": {}}\n')
        put(os.path.join(self.mem_a, "sub/deeper.md"), b"not a top-level note\n")
        out = self.ok(self.a("sync", "--push"))
        self.assertEqual(self.lines(out, "PUSH"), [], out)
        for rel in ("uploads/x.png", "staging/beethoven-qa.bundle", "state/.hidden.md", "memory/sub/deeper.md"):
            self.assertIsNone(self.at_origin(rel), rel)
        self.assertIn("state/HYDRATE.md", self.record("proj-a")["files"])
        self.ok(self.b("init", "--project-id", "proj-b", "--push"))
        self.ok(self.b("sync", "--push"))
        self.assertFalse(os.path.exists(os.path.join(self.src_b, "projects")))
        self.assertFalse(os.path.exists(os.path.join(self.src_b, "linear")))
        self.assertFalse(os.path.exists(os.path.join(self.src_b, "tools")))

    def test_10_crlf_round_trips(self):
        self.init_both()
        crlf = b"line one\r\nline two\r\n"
        put(os.path.join(self.src_a, "state/windows.md"), crlf)
        self.ok(self.a("sync", "--push"))
        self.assertEqual(self.at_origin("state/windows.md"), crlf)
        out = self.ok(self.b("sync", "--push"))
        self.assertEqual(self.lines(out, "PULL"), ["state/windows.md"])
        self.assertEqual(get(os.path.join(self.src_b, "state/windows.md")), crlf)
        self.ok(self.a("sync", "--push"))
        for run in (self.a, self.b):
            report = json.loads(self.ok(run("status", "--json")))
            self.assertEqual(report["actions"], [])
            self.assertEqual(report["summary"]["pushed"] + report["summary"]["pulled"], 0)

    def test_11a_race_with_an_unrelated_push_is_rebased(self):
        self.init_both()
        put(os.path.join(self.src_a, "state/HYDRATE.md"), b"A, racing\n")
        real, calls = hub.push_once, []

        def racing(branch):
            if not calls:
                calls.append(branch)
                self.hand_commit(self.hub_c, {"linear/ISSUES.md": b"# Issues\n\nBEE-1 closed.\n"})
            return real(branch)

        with mock.patch.object(hub, "push_once", racing):
            code, out = self.in_process(self.hub_a, self.src_a, self.mem_a, "sync", "--push")
        self.assertEqual(code, 0, out)
        self.assertIn("rebased", out)
        self.assertEqual(self.at_origin("state/HYDRATE.md"), b"A, racing\n")
        self.assertEqual(self.at_origin("linear/ISSUES.md"), b"# Issues\n\nBEE-1 closed.\n")
        self.assertEqual(self.head(self.origin, "main"), self.head(self.hub_a))
        self.assertEqual(self.head(self.origin, "main^"), self.head(self.hub_c))

    def test_11b_race_on_the_same_path_stops_and_the_next_run_recovers(self):
        self.init_both()
        base = SEEDED["ledger/LEDGER.md"]
        put(os.path.join(self.src_a, "ledger/LEDGER.md"), base + b"| 2026-10-05 | row from A |\n")
        real, calls = hub.push_once, []

        def racing(branch):
            if not calls:
                calls.append(branch)
                self.hand_commit(self.hub_c, {"ledger/LEDGER.md": base + b"| 2026-10-05 | row from C |\n"})
            return real(branch)

        with mock.patch.object(hub, "push_once", racing):
            code, out = self.in_process(self.hub_a, self.src_a, self.mem_a, "sync", "--push")
        self.assertEqual(code, 4, out)
        self.assertIn("the hub moved under this sync; run `hub.py sync --push` again", out)
        kept = self.head(self.hub_a)
        self.assertIn(b"row from A", self.git(self.hub_a, "show", "HEAD:ledger/LEDGER.md").encode())
        self.assertEqual(get(os.path.join(self.src_a, "ledger/LEDGER.md")), base + b"| 2026-10-05 | row from A |\n")
        self.assertEqual(self.at_origin("ledger/LEDGER.md"), base + b"| 2026-10-05 | row from C |\n")
        out = self.ok(self.a("sync", "--push"))
        self.assertEqual(self.lines(out, "MERGED"), ["ledger/LEDGER.md"])
        merged = base + b"| 2026-10-05 | row from A |\n| 2026-10-05 | row from C |\n"
        self.assertEqual(self.at_origin("ledger/LEDGER.md"), merged)
        self.assertEqual(get(os.path.join(self.src_a, "ledger/LEDGER.md")), merged)
        self.assertIn(kept, self.git(self.hub_a, "for-each-ref", "--format=%(objectname)", "refs/hub-sync/"))
        self.assertEqual(self.ok(self.a("status")).count("PUSH"), 0)

    def test_12_harness_dotfiles_in_the_hub_never_reach_a_project(self):
        self.init_both()
        planted = {"memory/.memory-sync": b"planted\n", "memory/.memory-sync-basis": b"planted\n",
                   "memory/.hidden.md": b"planted\n", "state/.hidden.md": b"planted\n",
                   "memory/archive/old.md": b"not a top-level note\n", "memory/notes.txt": b"not a note\n"}
        self.hand_commit(self.hub_c, planted)
        for run, src, mem in ((self.a, self.src_a, self.mem_a), (self.b, self.src_b, self.mem_b)):
            before = snapshot(mem)
            out = self.ok(run("sync", "--push"))
            self.assertEqual(self.lines(out, "PULL"), [], out)
            self.assertEqual(snapshot(mem), before)
            self.assertFalse(os.path.exists(os.path.join(src, "state", ".hidden.md")))
        # tearDown checks the bytes; the planted files are taken out again so its hub check holds.
        self.git(self.hub_c, "rm", "-q", *sorted(planted))
        self.git(self.hub_c, "commit", "-q", "-m", "take the planted files out")
        self.git(self.hub_c, "push", "-q", "origin", "HEAD:main")
        for clone in (self.hub_a, self.hub_b):
            self.git(clone, "pull", "-q", "--ff-only", "origin", "main")

    def test_13_a_dirty_hub_is_refused(self):
        self.init_both()
        put(os.path.join(self.src_b, "plan/BUILD_PLAN.md"), b"# Plan from B\n")
        self.ok(self.b("sync", "--push"))
        self.git(self.hub_a, "pull", "-q", "--ff-only", "origin", "main")
        put(os.path.join(self.hub_a, "state/scratch.md"), b"left here by hand\n")
        project, top = snapshot(self.src_a), self.head(self.hub_a)
        out = self.ok(self.a("sync"), 1)
        self.assertIn("uncommitted changes", out)
        self.assertEqual(snapshot(self.src_a), project)
        self.assertEqual(self.head(self.hub_a), top)
        self.assertEqual(self.git(self.hub_a, "status", "--porcelain").split(), ["??", "state/scratch.md"])

    def test_14_sync_py_forwards_to_hub_py(self):
        self.init_both()
        put(os.path.join(self.src_b, "state/HYDRATE.md"), b"via the old name\n")
        code, out = self.run_hub(self.hub_b, self.src_b, self.mem_b, "--push", "--trailer", "Test: yes", script="sync.py")
        self.assertEqual(code, 0, out)
        self.assertTrue(out.startswith("tools/sync.py is replaced by tools/hub.py"), out)
        self.assertEqual(self.lines(out, "PUSH"), ["state/HYDRATE.md"])
        self.assertEqual(self.at_origin("state/HYDRATE.md"), b"via the old name\n")
        self.assertIn("Test: yes", self.git(self.origin, "log", "-1", "--format=%B", "main"))

    # the rest of the contract

    def test_push_is_tried_again_after_a_network_failure(self):
        self.init_both()
        put(os.path.join(self.src_a, "state/HYDRATE.md"), b"pushed on the third try\n")
        real, calls, waits = hub.push_once, [], []

        def flaky(branch):
            calls.append(branch)
            if len(calls) < 3:
                return False, "fatal: unable to access 'https://x-access-token:abc@example.invalid/': Could not resolve host"
            return real(branch)

        with mock.patch.object(hub, "push_once", flaky), mock.patch.object(hub.time, "sleep", waits.append):
            code, out = self.in_process(self.hub_a, self.src_a, self.mem_a, "sync", "--push")
        self.assertEqual(code, 0, out)
        self.assertEqual(waits, [2, 4])
        self.assertNotIn("abc@", out)
        self.assertEqual(self.at_origin("state/HYDRATE.md"), b"pushed on the third try\n")

    def test_plain_sync_writes_both_sides_and_commits_nothing(self):
        self.init_both()
        put(os.path.join(self.src_b, "promo/PROMO.md"), b"promo\n")
        top = self.head(self.hub_b)
        out = self.ok(self.b("sync"))
        self.assertIn("nothing committed", out)
        self.assertEqual(self.head(self.hub_b), top)
        self.assertEqual(get(os.path.join(self.hub_b, "promo/PROMO.md")), b"promo\n")
        self.assertIn("promo/PROMO.md", json.loads(get(os.path.join(self.hub_b, "projects/proj-b/sync.json")))["files"])

    def test_push_to_a_branch_origin_does_not_have_yet(self):
        self.ok(self.a("init", "--project-id", "proj-a", "--push"))
        self.git(self.hub_b, "checkout", "-q", "-b", "account-b")
        self.ok(self.b("init", "--project-id", "proj-b", "--push"))
        self.assertIn("projects/proj-b/sync.json", self.git(self.origin, "ls-tree", "-r", "--name-only", "account-b"))
        self.assertNotIn("projects/proj-b/sync.json", self.git(self.origin, "ls-tree", "-r", "--name-only", "main"))

    def test_only_holds_the_other_direction_and_refuses_a_merge(self):
        self.init_both()
        base = SEEDED["ledger/LEDGER.md"]
        put(os.path.join(self.src_a, "ledger/LEDGER.md"), base + b"| a |\n")
        put(os.path.join(self.src_a, "plan/BUILD_PLAN.md"), b"plan from A\n")
        self.ok(self.a("sync", "--push"))
        put(os.path.join(self.src_b, "ledger/LEDGER.md"), base + b"| b |\n")
        put(os.path.join(self.src_b, "state/HYDRATE.md"), b"state from B\n")
        out = self.ok(self.b("sync", "--push", "--only", "pull"), 3)
        self.assertEqual(self.lines(out, "PULL"), ["plan/BUILD_PLAN.md"])
        self.assertEqual(self.lines(out, "HELD"), ["state/HYDRATE.md"])
        self.assertEqual(self.lines(out, "CONFLICT"), ["ledger/LEDGER.md"])
        self.assertEqual(self.at_origin("state/HYDRATE.md"), SEEDED["state/HYDRATE.md"])
        self.assertEqual(get(os.path.join(self.src_b, "ledger/LEDGER.md")), base + b"| b |\n")
        out = self.ok(self.b("sync", "--push"))
        self.assertEqual(self.lines(out, "MERGED"), ["ledger/LEDGER.md"])
        self.assertEqual(self.lines(out, "PUSH"), ["state/HYDRATE.md"])

    def test_init_refuses_another_projects_files(self):
        self.ok(self.a("init", "--project-id", "proj-a"))
        self.git(self.hub_a, "stash", "-u", "-q")  # this test's own clone: put the uncommitted record away
        out = self.ok(self.a("init", "--project-id", "proj-other"), 1)
        self.assertIn("belong to project proj-a", out)
        self.assertEqual(get(os.path.join(self.src_a, ".hub-project")), b"proj-a\n")
        self.ok(self.a("sync", "--project-id", "proj-other"), 1)

    def test_usage_errors_exit_1(self):
        self.assertEqual(self.a("sync", "--only", "sideways")[0], 1)
        self.assertEqual(self.a("frobnicate")[0], 1)
        self.assertIn("no project id", self.ok(self.a("sync"), 1))

    def test_status_json_shape(self):
        self.init_both()
        put(os.path.join(self.src_a, "state/HYDRATE.md"), b"changed\n")
        report = json.loads(self.ok(self.a("status", "--json")))
        self.assertEqual(report["actions"], [{"path": "state/HYDRATE.md", "action": "PUSH", "reason": "changed in the project"}])
        self.assertEqual(report["summary"]["pushed"], 1)
        self.assertEqual(self.git(self.hub_a, "status", "--porcelain"), "")

    def test_memory_folder_is_found_only_when_it_is_the_one(self):
        team = self.path("team")
        put(os.path.join(team, "one", ".memory-sync"), b"x\n")
        out = io.StringIO()
        with mock.patch.dict(os.environ, self.env, clear=True), mock.patch.object(hub, "MEMORY_GLOB", team + "/*/"), \
                contextlib.redirect_stdout(out):
            self.assertEqual(hub.memory_dir(None), os.path.join(team, "one"))
            put(os.path.join(team, "two", ".memory-sync"), b"x\n")
            self.assertIsNone(hub.memory_dir(None))
        self.assertIn("2 memory folders found", out.getvalue())


if __name__ == "__main__":
    unittest.main()

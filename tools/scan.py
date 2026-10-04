#!/usr/bin/env python3
"""Refuse anything that must not reach GitHub before the hub copies it.

The hub is private, but private is not a reason to carry a secret, a credential or patient data:
the repository is cloned into other accounts and other machines, and history keeps what a later
commit removes. So the sync scans every file it is about to copy and copies nothing when one
check fails. A finding prints its file, line and rule, and never the matched text.

What fails: the secret shapes below, a credential-named file, a file over 5 MB, and any file that
is neither text nor a git bundle (an image or a document can hold anything, so a person looks at
it first and lists it in .hub-allow with a reason). A git bundle is opened and every blob in it
is scanned the same way. What warns: an e-mail address or a patient-shaped line, which a person
reads before the push.

    python3 tools/scan.py <file-or-folder>...      exit 0 clean, 1 warnings only, 2 a failure
"""
import os
import re
import subprocess
import sys
import tempfile

MAX_BYTES = 5 * 1024 * 1024

FAIL = [
    ("github-token", re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{30,}\b|\bgithub_pat_[A-Za-z0-9_]{40,}")),
    ("anthropic-key", re.compile(r"\bsk-ant-[A-Za-z0-9_\-]{20,}")),
    ("openai-key", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9]{32,}\b")),
    ("aws-key", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("google-api-key", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b")),
    ("google-oauth", re.compile(r"\bGOCSPX-[A-Za-z0-9_\-]{20,}|\b1//0[A-Za-z0-9_\-]{30,}|\bya29\.[A-Za-z0-9_\-]{30,}")),
    ("slack-token", re.compile(r"\bxox[abprs]-[A-Za-z0-9\-]{10,}")),
    ("huggingface-token", re.compile(r"\bhf_[A-Za-z0-9]{30,}\b")),
    ("linear-key", re.compile(r"\blin_(?:api|oauth)_[A-Za-z0-9]{30,}\b")),
    ("npm-token", re.compile(r"\bnpm_[A-Za-z0-9]{36}\b")),
    ("private-key", re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----")),
    ("jwt", re.compile(r"\beyJ[A-Za-z0-9_\-]{10,}\.eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}")),
    ("azure-key", re.compile(r"AccountKey=[A-Za-z0-9+/=]{40,}|\bSharedAccessSignature=|sig=[A-Za-z0-9%+/=]{40,}")),
    ("credential-json", re.compile(r'"(?:accessToken|refreshToken|access_token|refresh_token|client_secret|sessionKey)"\s*:\s*"[^"\s]{16,}"')),
    ("kaggle-key", re.compile(r'"key"\s*:\s*"[0-9a-f]{32}"')),
    ("assigned-secret", re.compile(
        r"(?i)\b(?:password|passwd|secret|api[_-]?key|access[_-]?token|auth[_-]?token)\b[\"']?\s*[:=]\s*[\"']?"
        r"(?=[A-Za-z0-9+/_\-]*[0-9])(?=[A-Za-z0-9+/_\-]*[a-z])[A-Za-z0-9+/_\-]{20,}")),
    ("ssn", re.compile(r"\b\d{3}-\d{2}-\d{4}\b")),
]

WARN = [
    ("email", re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b")),
    ("patient-field", re.compile(r"(?i)\b(?:PatientName|PatientID|PatientBirthDate|MRN|date of birth|DOB)\b\s*[:=#]\s*\S")),
]

# E-mail addresses that are expected in the record: the maintainer's own and the bots'.
EMAIL_OK = re.compile(r"(?i)^(?:noreply@anthropic\.com|gregoryamdg@gmail\.com|gregory\.schwing@med\.wayne\.edu|"
                      r"[^@]+@users\.noreply\.github\.com|noreply@github\.com|[^@]+@example\.(?:com|org|invalid)|"
                      r"[^@]+@openssh\.com)$")

BAD_NAMES = re.compile(r"(?i)(?:^|/)(?:\.credentials\.json|\.env(?:\..*)?|id_(?:rsa|dsa|ecdsa|ed25519)(?:\.pub)?|"
                       r"[^/]*\.(?:pem|key|p12|pfx|keychain|keystore|jks|sif|kdbx)|\.netrc|\.npmrc|\.pypirc|"
                       r"[^/]*credentials[^/]*\.json|client_secret[^/]*\.json|service[-_]account[^/]*\.json|"
                       r"\.?[^/.]*token|[^/]*token\.(?:json|txt))$")


def allowed(root):
    """Paths a person has looked at and listed, one per line with its reason after a tab or '  #'."""
    path = os.path.join(root, ".hub-allow")
    out = set()
    if os.path.isfile(path):
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                line = line.split("#", 1)[0].strip()
                if line:
                    out.add(line.split()[0])
    return out


def shown(match):
    text = match.group(0)
    return "%s… (%d chars)" % (text[:4], len(text))


def scan_text(label, data, findings):
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        findings.append(("fail", label, 0, "not-text", "neither UTF-8 text nor a git bundle"))
        return
    for n, line in enumerate(text.splitlines(), 1):
        for rule, rx in FAIL:
            m = rx.search(line)
            if m:
                findings.append(("fail", label, n, rule, shown(m)))
        for rule, rx in WARN:
            for m in rx.finditer(line):
                if rule == "email" and EMAIL_OK.match(m.group(0)):
                    continue
                findings.append(("warn", label, n, rule, m.group(0) if rule == "email" else shown(m)))


def bundle_header(path):
    """The bundle's prerequisite commits and its refs, read from the text header before the pack."""
    prereqs, refs = [], []
    with open(path, "rb") as fh:
        fh.readline()
        for raw in fh:
            line = raw.decode("utf-8", "replace").rstrip("\n")
            if not line:
                break
            if line.startswith("@"):
                continue  # a v3 capability line
            if line.startswith("-"):
                prereqs.append(line[1:].split()[0])
            else:
                refs.append(line.split()[0])
    return prereqs, refs


def scan_bundle(path, label, findings):
    """Every commit message and blob the bundle itself carries, not those of its prerequisites.

    A bundle cut from a branch names commits it leaves out; git will not unpack it without them,
    so their object folders are borrowed read-only (HUB_BUNDLE_BASES, colon-separated, default the
    checkouts beside the hub) and only what lies beyond the prerequisites is read.
    """
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    prereqs, refs = bundle_header(path)
    hub_parent = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    bases = os.environ.get("HUB_BUNDLE_BASES")
    bases = bases.split(":") if bases else [os.path.join(hub_parent, d) for d in sorted(os.listdir(hub_parent))]
    objdirs = [os.path.join(b, ".git", "objects") for b in bases if os.path.isdir(os.path.join(b, ".git", "objects"))]
    with tempfile.TemporaryDirectory() as tmp:
        repo = os.path.join(tmp, "b.git")
        subprocess.run(["git", "init", "-q", "--bare", repo], env=env, check=True)
        if prereqs:
            with open(os.path.join(repo, "objects", "info", "alternates"), "w") as fh:
                fh.write("\n".join(objdirs) + "\n")
        r = subprocess.run(["git", "-C", repo, "fetch", "-q", os.path.abspath(path), "refs/*:refs/*"], env=env,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if r.returncode:
            why = " ".join(r.stderr.decode(errors="replace").split())[:160]
            findings.append(("fail", label, 0, "bad-bundle", why + " (set HUB_BUNDLE_BASES to a checkout that has them)"))
            return
        r = subprocess.run(["git", "-C", repo, "rev-list", "--objects"] + refs + ["--not"] + prereqs, env=env,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if r.returncode:
            findings.append(("fail", label, 0, "bad-bundle", "its prerequisite commits are in no checkout given "
                             "(set HUB_BUNDLE_BASES to one that has them)"))
            return
        objs = r.stdout.decode().splitlines()
        seen = set()
        for row in objs:
            sha, _, name = row.partition(" ")
            if sha in seen:
                continue
            seen.add(sha)
            kind = subprocess.run(["git", "-C", repo, "cat-file", "-t", sha], env=env,
                                  stdout=subprocess.PIPE, check=True).stdout.decode().strip()
            if kind == "commit":
                data = subprocess.run(["git", "-C", repo, "cat-file", "commit", sha], env=env,
                                      stdout=subprocess.PIPE, check=True).stdout
                scan_text("%s!commit %s" % (label, sha[:12]), data, findings)
                continue
            if kind != "blob":
                continue
            if BAD_NAMES.search(name):
                findings.append(("fail", "%s!%s" % (label, name), 0, "credential-name", "file name"))
            data = subprocess.run(["git", "-C", repo, "cat-file", "blob", sha], env=env,
                                  stdout=subprocess.PIPE, check=True).stdout
            if b"\0" in data[:8000]:
                continue  # a binary blob inside a bundle is code's own asset; the name check above still ran
            scan_text("%s!%s" % (label, name), data, findings)


def scan_file(path, label, ok, findings):
    if label in ok:
        return
    if BAD_NAMES.search(label):
        findings.append(("fail", label, 0, "credential-name", "file name"))
        return
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        findings.append(("fail", label, 0, "too-large", "%d bytes" % size))
        return
    with open(path, "rb") as fh:
        head = fh.read(16)
    if head.startswith((b"# v2 git bundle", b"# v3 git bundle")):
        scan_bundle(path, label, findings)
        return
    with open(path, "rb") as fh:
        data = fh.read()
    if b"\0" in data[:8000]:
        findings.append(("fail", label, 0, "binary", "a person looks at it and lists it in .hub-allow"))
        return
    scan_text(label, data, findings)


def scan(paths, root=None):
    root = root or os.getcwd()
    ok = allowed(root)
    findings = []
    for p in paths:
        if os.path.isdir(p):
            for d, dirs, files in os.walk(p):
                dirs[:] = sorted(x for x in dirs if x != ".git")
                for f in sorted(files):
                    full = os.path.join(d, f)
                    scan_file(full, os.path.relpath(full, root), ok, findings)
        else:
            scan_file(p, os.path.relpath(p, root), ok, findings)
    return findings


def main(argv):
    if not argv:
        print(__doc__.strip().splitlines()[-1].strip(), file=sys.stderr)
        return 2
    findings = scan(argv)
    for level, label, line, rule, what in findings:
        print("%s %s:%d %s %s" % (level.upper(), label, line, rule, what))
    fails = sum(1 for f in findings if f[0] == "fail")
    warns = len(findings) - fails
    print("scan: %d failure(s), %d warning(s)" % (fails, warns), file=sys.stderr)
    return 2 if fails else (1 if warns else 0)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

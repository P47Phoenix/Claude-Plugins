#!/usr/bin/env python3
"""
check_model_pins.py - model-pin guard (BACKLOG-108, ADR-lmr-002).

Forbids concrete model versions in the repo: pins, stamps, version prose.
No exemptions of any kind (no comment/quote/fence skip, no per-line marker).
Stdlib only. Scan runs only under __main__, so importlib load is side-effect free.

Usage:
  python3 scripts/check_model_pins.py                 # default scope
  python3 scripts/check_model_pins.py --list          # + one line per hit
  python3 scripts/check_model_pins.py --paths F...    # only named files (implies --list)
  python3 scripts/check_model_pins.py --strict        # accepted; rc unchanged (see below)
  python3 scripts/check_model_pins.py --check-fixtures  # run scripts/model_pin_fixtures.json
  python3 scripts/check_model_pins.py --canary        # inject pin in mktemp repo, expect rc 1
  python3 scripts/check_model_pins.py --help          # rc 0

Scope (default): `git -C <toplevel> ls-files -z --cached --others --exclude-standard`
where <toplevel> = `git rev-parse --show-toplevel`; the process chdirs there, so
scope, printed paths and --paths args are toplevel-relative and independent of the
invoking cwd. Regular files only (symlinks and nested worktrees skipped), extensions .py .md .yml
.yaml .txt .sh, minus CHANGELOG.md (any dir) and everything under .delivery/.
Not scanned (out of scope by design): .json .jsonl .log .toml files, CHANGELOG.md,
and .delivery/ - EXTS excludes those extensions, so a pin there is NOT detected.
--paths: same filters; relative args resolve against the toplevel (not the invoking
cwd); a file outside the repo is scanned; outside any repo, cwd is kept.
--list escapes control characters in file names (as \\xNN) so each hit is one line.

Rules (one category per line, in this order):
  pin    line matches PIN_RE (re.I)
  stamp  else matches STAMP_RE (re.I)
  prose  else, .md only: COUNT_RE matches blanked to one space, then
         PROSE_RE (case-sensitive) or BARE_RE (re.I)

Output (stdout):
  [<category> <file>:<line>]...   only with --list / --paths; sorted by file, line;
                                  each starts with exactly `pin `, `stamp ` or `prose `
  files-scanned <K>               in-scope files actually read
  guard-scope hits <N> files <M>  ALWAYS LAST line (M = files holding a hit)

Exit: 0 clean | 1 hits (N > 0) | 2 default scope empty (K == 0), git listing
failed, not in a repo, or an in-scope file unreadable/undecodable (fail closed,
stderr names path). An empty default scope still prints `files-scanned 0` and
`guard-scope hits 0 files 0` but exits 2: callers must judge on rc, not on hits. Explicit --paths with zero scannable files: prints
`files-scanned 0` + `guard-scope hits 0 files 0`, exit 0.

--strict / MODEL_PIN_STRICT=1: consumed by the hooks (block vs advisory). The
script itself always exits 1 on hits; the flag is accepted and does not change rc.

Fixture file scripts/model_pin_fixtures.json (QA-owned; absent = built-in no-op):
  {
    "rule_a_must_hit":  [str, ...],   # line classified pin or stamp
    "rule_a_must_pass": [str, ...],   # line NOT pin/stamp
    "rule_b_must_hit":  [str, ...],   # .md line classified prose (Rule B)
    "rule_b_must_pass": [str, ...],   # .md line NOT prose
    "known_fp": [ {"line": str, "expect": "hit"|"pass"}, ... ],
                                      # (plain str entries = expect hit); scanned as .md
    "provenance": { "<fixture string>": "<origin>" }
  }
  --check-fixtures prints `fixture failures <n> [...]`, exit 0 if n == 0 else 1.
  Missing file: prints `fixtures absent (known_fp no-op)`, exit 0.
  Canary pin string: first entry of rule_a_must_hit if present, else a
  synthetic one built at runtime (no literal pin in this source).

Docs/examples use synthetic IDs only (claude-opus-fixture); this file must
pass its own scan.
"""

import json
import os
import re
import subprocess
import sys
import tempfile

PIN_RE = r"claude-[a-z0-9.-]*([0-9]|-latest)"
STAMP_RE = r'model_awareness: *"?[a-z-]*[0-9]|pattern_library_version: *"?([0-9v]|[a-z-]*[0-9]+[.-][0-9])'
PROSE_RE = r"(Opus|Sonnet|Haiku|Fable|Mythos|OPUS|SONNET|HAIKU|FABLE|MYTHOS)[ -]*v?[0-9]|(opus|sonnet|haiku|fable|mythos)(-v?[0-9]|v?[0-9]| v?[0-9]+[.][0-9])"
BARE_RE = r"(^|[^A-Za-z])(on|under|in|for|the|new|so|with|isolates?) v?[4-9][.][0-9]+([^0-9A-Za-z]|$)|[4-9][.-][0-9]+-(only|aware)"
COUNT_RE = r"(Opus|Sonnet|Haiku|Fable|Mythos) +[0-9]+ +(times|stories|story|reviewers?|reviews?|agents?|subagents?|passes|rounds?|runs?|instances?|copies|cycles?|iterations?|tasks?|items?|personas?|judges?)([^A-Za-z]|$)|([Oo]n|[Uu]nder|[Ii]n|[Ff]or|[Tt]he|[Nn]ew|[Ss]o|[Ww]ith|[Ii]solates?) v?[0-9]+[.][0-9]+ *(seconds?|secs?|ms|minutes?|mins?|hours?|hrs?|days?|weeks?|months?|years?|times|percent|points?|GB|MB|KB)([^A-Za-z]|$)"

EXTS = (".py", ".md", ".yml", ".yaml", ".txt", ".sh")
FIXTURES = os.path.join("scripts", "model_pin_fixtures.json")

_PIN = re.compile(PIN_RE, re.I)
_STAMP = re.compile(STAMP_RE, re.I)
_PROSE = re.compile(PROSE_RE)
_BARE = re.compile(BARE_RE, re.I)
_COUNT = re.compile(COUNT_RE)


class GuardError(Exception):
    """Fail-closed condition; main() maps it to exit 2."""


def classify(line, is_md):
    """Return 'pin' | 'stamp' | 'prose' | None for one line."""
    if _PIN.search(line):
        return "pin"
    if _STAMP.search(line):
        return "stamp"
    if is_md:
        b = _COUNT.sub(" ", line)
        if _PROSE.search(b) or _BARE.search(b):
            return "prose"
    return None


def _in_scope_name(path):
    norm = os.path.relpath(path).replace(os.sep, "/") if os.path.isabs(path) else path.replace(os.sep, "/")
    if norm.startswith("./"):
        norm = norm[2:]
    if norm.startswith(".delivery/"):
        return False
    if os.path.basename(norm) == "CHANGELOG.md":
        return False
    return norm.endswith(EXTS)


def toplevel():
    """Absolute repo toplevel or None when not in a repo."""
    try:
        r = subprocess.run(["git", "rev-parse", "--show-toplevel"], shell=False,
                           check=True, capture_output=True)
    except (OSError, subprocess.CalledProcessError):
        return None
    top = os.fsdecode(r.stdout).rstrip("\r\n")
    return top or None


def files(top):
    """Default scope (toplevel-relative paths, sorted). Raises GuardError."""
    try:
        r = subprocess.run(
            ["git", "-C", top, "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
            shell=False, check=True, capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError) as e:
        raise GuardError("git ls-files failed: %s" % e)
    out = []
    for raw in sorted(set(r.stdout.split(b"\0"))):
        if not raw:
            continue
        f = os.fsdecode(raw)
        if not _in_scope_name(f):
            continue
        if os.path.islink(f) or not os.path.isfile(f):
            continue  # symlink, nested worktree, deleted-but-listed
        out.append(f)
    return out


def scan_file(path):
    """Yield (line_no, category). Fail closed on unreadable/undecodable."""
    is_md = path.endswith(".md")
    hits = []
    try:
        with open(path, "r", encoding="utf-8", errors="strict") as fh:
            for i, line in enumerate(fh, 1):
                k = classify(line, is_md)
                if k:
                    hits.append((i, k))
    except (OSError, UnicodeDecodeError) as e:
        raise GuardError("unreadable in-scope file %s: %s" % (path, e))
    return hits


def run_scan(paths):
    hits = []  # (file, line, category)
    for p in paths:
        for i, k in scan_file(p):
            hits.append((p, i, k))
    hits.sort(key=lambda h: (h[0], h[1]))
    return hits


def _display(p):
    p = p[2:] if p.startswith("./") else p
    return re.sub(r"[\x00-\x1f\x7f]", lambda m: "\\x%02x" % ord(m.group()), p)


def load_fixtures():
    try:
        with open(FIXTURES, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        return None
    except (OSError, ValueError) as e:
        raise GuardError("fixtures unreadable %s: %s" % (FIXTURES, e))


def check_fixtures():
    F = load_fixtures()
    if F is None:
        print("fixtures absent (known_fp no-op)")
        return 0
    bad = []
    for s in F.get("rule_a_must_hit", []):
        if classify(s, False) not in ("pin", "stamp"):
            bad.append(("rule_a_must_hit", s))
    for s in F.get("rule_a_must_pass", []):
        if classify(s, False) in ("pin", "stamp"):
            bad.append(("rule_a_must_pass", s))
    for s in F.get("rule_b_must_hit", []):
        if classify(s, True) != "prose":
            bad.append(("rule_b_must_hit", s))
    for s in F.get("rule_b_must_pass", []):
        if classify(s, True) == "prose":
            bad.append(("rule_b_must_pass", s))
    for e in F.get("known_fp", []):
        line, expect = (e, "hit") if isinstance(e, str) else (e.get("line", ""), e.get("expect", "hit"))
        got = classify(line, True) is not None
        if got != (expect == "hit"):
            bad.append(("known_fp", line))
    print("fixture failures %d %s" % (len(bad), json.dumps(bad)))
    return 0 if not bad else 1


def canary():
    """Inject one pin in a mktemp repo, expect rc 1; remove, expect rc 0."""
    me = os.path.abspath(__file__)
    pin = "claude-" + "opus-" + "9"
    try:
        F = load_fixtures()
        if F and F.get("rule_a_must_hit"):
            pin = F["rule_a_must_hit"][0]
    except GuardError:
        pass
    ok = True
    with tempfile.TemporaryDirectory(prefix="pin-canary-") as d:
        def g(*a):
            return subprocess.run(["git", "-C", d] + list(a), shell=False, capture_output=True, text=True)
        def guard():
            return subprocess.run([sys.executable, me, "--list"], shell=False, cwd=d, capture_output=True, text=True)
        if g("init", "-q").returncode != 0:
            print("canary: git init failed", file=sys.stderr)
            return 2
        with open(os.path.join(d, "clean.md"), "w", encoding="utf-8") as fh:
            fh.write("no version here\n")
        bad_path = os.path.join(d, "canary-pin.md")
        with open(bad_path, "w", encoding="utf-8") as fh:
            fh.write(pin + "\n")
        r = guard()
        seen = re.search(r"^pin canary-pin\.md:1$", r.stdout, re.M) is not None
        scanned = re.search(r"^files-scanned ([0-9]+)$", r.stdout, re.M)
        if not (r.returncode == 1 and seen and scanned and int(scanned.group(1)) > 0):
            ok = False
            print("canary FAIL (dirty): rc=%s out=%r" % (r.returncode, r.stdout), file=sys.stderr)
        os.remove(bad_path)
        r = guard()
        if r.returncode != 0:
            ok = False
            print("canary FAIL (clean): rc=%s out=%r" % (r.returncode, r.stdout), file=sys.stderr)
    print("canary %s" % ("ok" if ok else "FAILED"))
    return 0 if ok else 1


def main(argv):
    if "-h" in argv or "--help" in argv:
        print(__doc__)
        return 0
    listing = "--list" in argv
    top = toplevel()
    if top:
        os.chdir(top)
    if "--check-fixtures" in argv:
        try:
            return check_fixtures()
        except GuardError as e:
            print(str(e), file=sys.stderr)
            return 2
    if "--canary" in argv:
        return canary()
    explicit = "--paths" in argv
    try:
        if explicit:
            listing = True
            named = argv[argv.index("--paths") + 1:]
            named = [a for a in named if not a.startswith("--")]
            paths = []
            for p in named:
                if not _in_scope_name(p):
                    continue
                if os.path.islink(p):
                    continue
                if not os.path.exists(p):
                    continue  # deleted path from a hook: nothing to read
                if not os.path.isfile(p):
                    continue
                paths.append(p)
            paths = sorted(set(paths))
        else:
            if not top:
                raise GuardError("not in a git repository")
            paths = files(top)
        hits = run_scan(paths)
    except GuardError as e:
        print("check_model_pins: %s" % e, file=sys.stderr)
        return 2
    if listing:
        for f, i, k in hits:
            print("%s %s:%d" % (k, _display(f), i))
    k_scanned = len(paths)
    print("files-scanned %d" % k_scanned)
    nfiles = len({h[0] for h in hits})
    print("guard-scope hits %d files %d" % (len(hits), nfiles))
    if not explicit and k_scanned == 0:
        print("check_model_pins: default scope empty (wrong cwd or broken listing)", file=sys.stderr)
        return 2
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

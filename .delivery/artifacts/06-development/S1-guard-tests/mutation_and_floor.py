"""run: run-2026-05-28-o48m  story: S1  role: qa (validator)
Two checks the producer does not ship.
  1. Negative self-test (PA-12 idea): weaken each guard pattern; the fixture
     file MUST then report failures, else the fixtures are not sensitive.
  2. Files-scanned floor (PA-7): K == live count and K >= B (base-sha.txt line 2).
Run from repo root: python3 .delivery/artifacts/06-development/S1-guard-tests/mutation_and_floor.py
Prints MUTATION OK / FLOOR OK, rc 0; else FAIL lines, rc 1.
"""
import importlib.util, json, os, re, subprocess, sys

sp = importlib.util.spec_from_file_location("g", "scripts/check_model_pins.py")
g = importlib.util.module_from_spec(sp)
sp.loader.exec_module(g)
F = json.load(open("scripts/model_pin_fixtures.json", encoding="utf-8"))


def failures():
    n = 0
    for s in F["rule_a_must_hit"]:
        n += g.classify(s, False) not in ("pin", "stamp")
    for s in F["rule_a_must_pass"]:
        n += g.classify(s, False) in ("pin", "stamp")
    for s in F["rule_b_must_hit"]:
        n += g.classify(s, True) != "prose"
    for s in F["rule_b_must_pass"]:
        n += g.classify(s, True) == "prose"
    return n


rc = 0
if failures() != 0:
    print("FAIL baseline fixtures fail: %d" % failures())
    rc = 1
orig = dict(p=g._PIN, s=g._STAMP, r=g._PROSE, b=g._BARE, c=g._COUNT)
NEVER = re.compile(r"(?!x)x")
ALWAYS = re.compile(r".")
MUT = [
    ("PIN never", "_PIN", NEVER), ("PIN always", "_PIN", ALWAYS),
    ("STAMP never", "_STAMP", NEVER), ("PROSE never", "_PROSE", NEVER),
    ("PROSE always", "_PROSE", ALWAYS), ("BARE never", "_BARE", NEVER),
    ("COUNT never", "_COUNT", NEVER),
    ("PIN drops -latest", "_PIN", re.compile(r"claude-[a-z0-9.-]*[0-9]", re.I)),
    ("PIN case-sensitive", "_PIN", re.compile(g.PIN_RE)),
    ("PROSE drops Fable", "_PROSE", re.compile(g.PROSE_RE.replace("Fable|", "").replace("FABLE|", ""))),
]
for label, attr, rx in MUT:
    old = getattr(g, attr)
    setattr(g, attr, rx)
    n = failures()
    setattr(g, attr, old)
    print("mutation %-22s fixture failures %d" % (label, n))
    if n == 0:
        print("FAIL mutation survived: " + label)
        rc = 1
if rc == 0:
    print("MUTATION OK %d/%d killed" % (len(MUT), len(MUT)))

# floor
out = subprocess.run([sys.executable, "scripts/check_model_pins.py"], capture_output=True, text=True).stdout
K = int(re.search(r"^files-scanned ([0-9]+)$", out, re.M).group(1))
ls = subprocess.run(["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"], capture_output=True).stdout
live = 0
for raw in ls.split(b"\0"):
    f = os.fsdecode(raw)
    if not f or not f.endswith(g.EXTS) or f.startswith(".delivery/") or os.path.basename(f) == "CHANGELOG.md":
        continue
    if os.path.isfile(f) and not os.path.islink(f):
        live += 1
lines = open(".delivery/artifacts/06-development/base-sha.txt").read().split("\n")
assert re.fullmatch(r"[0-9a-f]{40}", lines[0]) and re.fullmatch(r"[0-9]+", lines[1]), "base-sha.txt format"
B = int(lines[1])
print("K=%d live=%d B=%d" % (K, live, B))
if K == live and K >= B:
    print("FLOOR OK")
else:
    print("FAIL floor: K != live or K < B")
    rc = 1
sys.exit(rc)

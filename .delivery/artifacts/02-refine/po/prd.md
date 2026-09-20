<!-- run: run-2026-05-28-backlog-108 -->
# PRD — Opus 5 Migration (Revision 2)

**Backlog**: BACKLOG-108-opus-5-migration.md (renamed from BACKLOG-108-opus-4-8-migration.md)
**Project Type**: FEATURE
**Stage**: 2 — Refine (LIGHT), Revision 2 (retargeted from Opus 4.8 to Opus 5)
**PO**: Gandalf
**Date**: 2026-09-19 (Revision 2); run id run-2026-05-28-backlog-108 unchanged
**Binding context**: `.delivery/memory/topics/opus-5-migration.md` (AUTHORITATIVE; renamed from `opus-4-8-migration.md`; Section 6 of that file logs the Opus 5 re-verification of every 4.8-specific ruling)

> A wizard ships the model the world runs on. The user has named the target: Claude Opus 5, `claude-opus-5`. The plugins still claim 4.7. End it.

**Decision recorded (binding, not re-debated)**: the migration target is `claude-opus-5`, not `claude-opus-4-8`. The repo migrates FROM 4.7. No `claude-opus-4-8` literal exists in the tree today (0 hits, section 1); it is nevertheless a rejected ID after migration.

---

## 1. Problem

The repo holds **34 SKILL.md** files. **25** carry a `model_awareness:` stamp; **9** carry none (4 user-feedback personas + 5 research-agent types).

### Canonical counting command (the ONE source of every literal count in this PRD)

All literal counts, in every section, come from this single script. It walks the worktree root with `os.walk`, prunes `.git` and `.delivery` directories anywhere and the `./.claude/worktrees` subtree, and DOES scan `.github` (so the guard yml is counted). It scans `*.py *.md *.yml *.yaml *.txt`. CHANGELOG.md is excluded by design (FR-7.2 may name the retired ID historically). Lines containing the exact provenance string are exempt.

Create the shared reproducer once (used by every python AC below):

```bash
cat > /tmp/walk.py <<'PY'
import os
SKIP = {'.git', '.delivery'}
def files(exts=None, name=None):
    for r, d, f in os.walk('.'):
        d[:] = [x for x in d if x not in SKIP and os.path.join(r, x) != os.path.join('.', '.claude', 'worktrees')]
        for n in f:
            if name and n != name: continue
            if exts and not n.endswith(exts): continue
            yield os.path.join(r, n)
PY
```

The counting command:

```bash
python3 - <<'PY'
exec(open('/tmp/walk.py').read())
EXEMPT = '# prior: claude-opus-4-7 (retired 2026-09-19, BACKLOG-108)'
for lit in ('claude-opus-4-7', 'claude-opus-4-8'):
    hits = {}
    for f in files(exts=('.py', '.md', '.yml', '.yaml', '.txt')):
        if f.endswith('CHANGELOG.md'):
            continue
        for i, l in enumerate(open(f, errors='ignore'), 1):
            if lit in l and EXEMPT not in l:
                hits.setdefault(f, []).append(i)
    print(lit, 'hits', sum(len(v) for v in hits.values()), 'files', len(hits))
    for f in sorted(hits):
        print('  ', f, hits[f])
PY
```

**Exact output, run from the worktree root on 2026-09-19 (before any migration edit):**

```
claude-opus-4-7 hits 9 files 5
   ./.github/workflows/stale-model-id-guard.yml [23, 39]
   ./agentic-flow-builder/scripts/agent_registry.py [190]
   ./delivery-team/architecture/smoke-test-architecture.md [115]
   ./delivery-team/tests/smoke/tests/conftest.py [105, 117, 129, 151]
   ./prompt-engineer/SKILL.md [368]
claude-opus-4-8 hits 0 files 0
```

Expected output after S1 and S4 land (G-LIT closing state): `claude-opus-4-7 hits 0 files 0` and `claude-opus-4-8 hits 0 files 0`.

Consistent reading of that output: **9 hits in 5 files** repo-wide (guard yml included: 2 hits; four source files: 7 hits). Excluding the guard yml, which S1 rewrites, the count is 7 hits in 4 files. Earlier revisions said "7 in five sites", "9 in 6 files" and "today's value 9 via walk.py"; all were wrong or mixed scopes. The table below reproduces the same output; there is no other count in this document.

| # | Site | Hits | What |
|---|------|------|------|
| 1 | `.github/workflows/stale-model-id-guard.yml:23,39` | 2 | allowlist comment and fix hint (guard rewritten in S1) |
| 2 | `agentic-flow-builder/scripts/agent_registry.py:190` | 1 | heavy-tier registry config: `"config": {"model": "claude-opus-4-7"},` |
| 3 | `delivery-team/architecture/smoke-test-architecture.md:115` | 1 | example string in code fence |
| 4 | `delivery-team/tests/smoke/tests/conftest.py:105,117,129,151` | 4 | fixture model strings |
| 5 | `prompt-engineer/SKILL.md:368` | 1 | `MODEL_ID = "claude-opus-4-7"  # canonical 2026-04-22` code literal |

### Stamp census (also run from the worktree root, same walk.py)

```bash
python3 - <<'PY'
from collections import Counter
exec(open('/tmp/walk.py').read())
sk = list(files(name='SKILL.md'))
print('skill', len(sk))
L = [(f, l.rstrip()) for f in sk for l in open(f) if l.lstrip().startswith('model_awareness:')]
print(len(L), len({f for f, _ in L}), dict(Counter(l for _, l in L)))
PY
```

Exact output: `skill 34` then `26 25 {'model_awareness: opus-4-7-frontmatter-only': 19, 'model_awareness: opus-4-7': 7}`.

So: 26 stamp lines in 25 files. `prompt-engineer/SKILL.md` has two lines (line 6 real frontmatter; line 415 a documentation example in a fenced block in Pattern 4.6), both `opus-4-7`. Values: 7 lines `opus-4-7` (5 files with one line, plus both prompt-engineer lines) and 19 lines `opus-4-7-frontmatter-only` (19 files). After migration: 34 frontmatter stamps (25 updated, 9 created) plus the 1 documentation-example stamp = **35 stamp lines**, all `model_awareness: opus-5`.

Stale stamps lie. The plugins claim 4.7 while the target model is Opus 5. Fix now.

## 2. Personas

| Persona | Goal | Pain today | Context |
|---------|------|------------|---------|
| Plugin maintainer (Michael) | Repo truthfully claims the model it is audited against | 34 skills claim 4.7; 19 of them were never prose-reviewed | Ships via squash-rebase + ff-merge to main, local-only tooling |
| Downstream plugin consumer | Skills whose dispatch/effort guidance matches the model actually running | Stale prose; stale registry ID sends heavy-tier work to a legacy model | Installs from marketplace, cannot see internal audit state |
| Local reviewer / CI gate reader | A guard that fails on retired IDs and never on legitimate text | Guard currently allowlists the retired ID and would flag nothing about 4.7 | Reads static CI output only (no `claude` CLI in CI) |

## 3. Functional Requirements and Acceptance Criteria

Seven stories, strict order (BINDING-2.5, keystone-first). Every AC is bash or python-stdlib only, runnable from repo root, no `yq`, no new CLI dependency. "Verification: inspection" means a named artifact is inspected by the QA validator (process-only FRs). The shared reproducer `/tmp/walk.py` is defined in section 1; note that `walk.py` DOES scan `.github` and skips only `.git`, `.delivery`, and `./.claude/worktrees`.

### S1 — CI guard rewrite (closes G1)

- **FR-1.1** Rewrite `.github/workflows/stale-model-id-guard.yml` to a positive allowlist permitting only `claude-opus-5`, `claude-sonnet-4-6`, `claude-haiku-4-5-20251001`.
  - **AC-1.1**: each approved ID appears in the guard, checked separately:
    ```bash
    for id in claude-opus-5 claude-sonnet-4-6 claude-haiku-4-5-20251001; do
      n=$(grep -c -- "$id" .github/workflows/stale-model-id-guard.yml); echo "$id $n"; done
    # MUST print three lines each with count >= 1
    ```
- **FR-1.2** `claude-opus-4-7` and `claude-opus-4-8` trigger CI failure (no dual-allow window, BINDING-2.1). The guard yml itself contains no non-comment `claude-opus-4-7` or `claude-opus-4-8`. Guard contract so tests can extract its patterns:
  - The guard defines `STALE_RE='...'` and `ALLOW_RE='...'`, each on its own line, single-quoted.
  - Both patterns are portable to `grep -E` AND Python `re`: no POSIX bracket classes (`[[:space:]]`), no single quotes inside the value, no lookaheads. Suggested values: `STALE_RE='claude-(opus|sonnet|haiku)-[0-9][-.0-9a-z]*'` and `ALLOW_RE='claude-opus-5([^-0-9]|$)|claude-sonnet-4-6([^-0-9]|$)|claude-haiku-4-5-20251001'`. A line is a hit when, after deleting `ALLOW_RE` matches, `STALE_RE` still matches. (This resolves QA warning D2-3.)
  - Line exemptions mirror today's guard: lines whose first non-space character is `#` or `>` are skipped. The guard scans `*.py` and `*.md` outside `.delivery/` and skips `CHANGELOG.md` explicitly (pathspec `':!:CHANGELOG.md'`).
  - **AC-1.2a** (guard rejects retired IDs, accepts the target; contract-level): extract the patterns and apply them to fixtures:
    ```bash
    python3 - <<'PY'
    import re
    t = open('.github/workflows/stale-model-id-guard.yml').read()
    stale = re.search(r"^\s*STALE_RE='([^']+)'", t, re.M)
    allow = re.search(r"^\s*ALLOW_RE='([^']+)'", t, re.M)
    assert stale and allow, "guard must define STALE_RE='...' and ALLOW_RE='...' each on its own line"
    def is_hit(line):
        s = line.lstrip()
        if s.startswith('#') or s.startswith('>'):
            return False
        return bool(re.search(stale.group(1), re.sub(allow.group(1), '', line)))
    assert is_hit('MODEL = "claude-opus-4-7"'), "4-7 fixture NOT rejected"
    assert is_hit('MODEL = "claude-opus-4-8"'), "4-8 fixture NOT rejected"
    assert not is_hit('MODEL = "claude-opus-5"'), "opus-5 falsely rejected"
    assert not is_hit('MODEL = "claude-sonnet-4-6"'), "sonnet-4-6 falsely rejected"
    assert not is_hit('# prior: claude-opus-4-7 (retired 2026-09-19, BACKLOG-108)'), "provenance comment line falsely rejected"
    print("OK")
    PY
    # MUST print OK
    ```
  - **AC-1.2b** (no live retired IDs in guard): `grep -v '^[[:space:]]*#' .github/workflows/stale-model-id-guard.yml | grep -cE "claude-opus-4-(7|8)"` MUST print 0.
  - **AC-1.2c** (no false positives on the migrated tree; reconciled with FR-4.1): the provenance comment lives on its own line above the registry line (FR-4.1), so the guard's existing `#`-first-character exemption already covers it; no extra guard exemption is needed. After S4 lands, applying the guard's extracted patterns and line exemptions to every `*.py` and `*.md` under `walk.py`, excluding `CHANGELOG.md`, yields 0 hits:
    ```bash
    python3 - <<'PY'
    import re; exec(open('/tmp/walk.py').read())
    t = open('.github/workflows/stale-model-id-guard.yml').read()
    stale = re.search(r"^\s*STALE_RE='([^']+)'", t, re.M).group(1)
    allow = re.search(r"^\s*ALLOW_RE='([^']+)'", t, re.M).group(1)
    n = 0
    for f in files(exts=('.py', '.md')):
        if f.endswith('CHANGELOG.md'): continue
        for l in open(f, errors='ignore'):
            s = l.lstrip()
            if s.startswith('#') or s.startswith('>'): continue
            if re.search(stale, re.sub(allow, '', l)): n += 1
    print(n)
    PY
    # MUST print 0
    ```
    Well-formedness note: this AC is expected to be non-zero before S1 and S4 land; QA checks that it parses and runs, not that it passes today.
- **FR-1.3** Guard is a static grep job; no `claude` CLI in any workflow (BINDING-5.2, BINDING-4.6).
  - **AC-1.3**: `grep -rEl '(^|[^a-z-])claude[[:space:]]+(-p|--print|--model)' .github/workflows | wc -l` MUST print 0 (ran 2026-09-19: 0); and `ls .github/workflows | grep -c '^smoke-'` MUST print 0 (ran: 0).

### S2 — Keystone prose (closes G7; precondition for G6)

- **FR-2.1** Full prose review of 3 keystones in order: `delivery-team/skills/delivery-flow/SKILL.md`, `prompt-engineer/SKILL.md`, `delivery-team/skills/product-delivery/SKILL.md`.
  - **AC-2.1** (body delta): for each keystone, `git diff --numstat main -- <file>` reports a changed line count greater than the count of stamp lines changed (checked by the shared body-delta script under AC-3.1). Verification also: dispatch manifest for S2 lists one reviewer dispatch per keystone.
- **FR-2.2** `prompt-engineer/SKILL.md:368` `MODEL_ID` code literal becomes `claude-opus-5`; the line 415 documentation example is restated as `opus-5` in S3 with the stamp.
  - **AC-2.2**: `grep -n 'MODEL_ID = "claude-opus-5"' prompt-engineer/SKILL.md | wc -l` MUST print 1.
- **FR-2.3** Dispatch guidance prose uses only doc-verified Opus 5 behavior (section 8). Anchor it to the documented delegation behavior: Opus 5 "delegates to subagents more readily than prior models", so prose must give explicit guidance on which tasks warrant delegation and a cap on spawn counts, and must drop instructions that ask the model to re-verify its own work (documented to cause over-verification). No provisional text (BINDING-3.3).
  - **AC-2.3** (scoped hedge scan; research-agent rubric prose excluded because it legitimately says "unverified"; ran 2026-09-19: 0):
    ```bash
    python3 - <<'PY'
    import re; exec(open('/tmp/walk.py').read())
    pat = re.compile(r"pending doc verification|do not treat as binding|Architect to confirm", re.I)
    hits = [f for f in files(name='SKILL.md') if 'research-agent' not in f and pat.search(open(f).read())]
    print(len(hits))
    PY
    # MUST print 0
    ```
  - **AC-2.3b** (independent re-fetch): adversarial reviewer WebFetches >= 3 rows from section 8 and records URL + quote in its review artifact (BINDING-3.2). Verification: inspection of `.delivery/artifacts/*/dod/*adversarial*` file containing three URLs.
- **FR-2.4** Each SKILL.md edit routes through `plugin-dev:skill-development`, acknowledged before edit (CLAUDE.md). Verification: inspection; each developer dispatch report contains the line `plugin-dev:skill-development loaded`.
- **FR-2.5** The `delivery-flow` keystone dispatch section states an explicit delegation-scope rule and spawn cap for Opus 5 (FR-2.3 content, made testable).
  - **AC-2.5**: python over the added lines of `git diff -U0 main -- delivery-team/skills/delivery-flow/SKILL.md` asserts at least one added line matches `(?i)sub-?agent` and at least one added line matches `(?i)\b(cap|limit|independent)\b`; MUST print `OK`.

### S3 — Full prose sweep (closes G2, G3, G6)

- **FR-3.1** Full prose review of all 34 SKILL.md, keystones plus 31 others (BINDING-2.2; no frontmatter-only pass). Review lens: Opus 5 doc-verified behaviors in section 8 (thinking on by default, delegation, over-verification instructions, verbosity).
  - **AC-3.1** (every file has a body change; 34/34). No SKILL.md file is created by this initiative, so `git diff main` (tracked files) is sufficient:
    ```bash
    python3 - <<'PY'
    import subprocess, re; exec(open('/tmp/walk.py').read())
    bad = []
    for f in files(name='SKILL.md'):
        d = subprocess.run(['git','diff','-U0','main','--',f],capture_output=True,text=True).stdout
        body = [l for l in d.splitlines() if l[:1] in '+-' and not l.startswith(('+++','---'))
                and not re.match(r'[+-](model_awareness|pattern_library_version|last_audited):', l)]
        if not body: bad.append(f)
    print(len(bad), bad)
    PY
    # MUST print: 0 []
    ```
  - **AC-3.1b**: python over `walk.py` `files(name='SKILL.md')` counting files containing the string `frontmatter-only` MUST print 0 (today: 19).
- **FR-3.2** Create a NEW stamp on the 9 unstamped files.
  - **AC-3.2**: python: every SKILL.md has its first `---` frontmatter block containing exactly one line `model_awareness: opus-5`; count of qualifying files MUST equal 34.
- **FR-3.3** Stamps applied AFTER prose passes reach DoD (BINDING-2.3): `model_awareness: opus-5`, `pattern_library_version: 5-0-1`, `last_audited: 2026-09-19`.
  - **AC-3.3a** (value purity):
    ```bash
    python3 - <<'PY'
    exec(open('/tmp/walk.py').read())
    L = [l.rstrip() for f in files(name='SKILL.md') for l in open(f) if l.lstrip().startswith('model_awareness:')]
    print(len(L), sum(l != 'model_awareness: opus-5' for l in L))
    PY
    # MUST print: 35 0   (34 frontmatter + prompt-engineer doc example line 415, restated as opus-5)
    ```
    Note: the doc-example line at `prompt-engineer/SKILL.md:415` starts at column 0 inside a code fence, so it counts; hence 35. Today the same command prints `26 26` (26 lines, all stale).
  - **AC-3.3b**: `grep -c "model_awareness:" prompt-engineer/SKILL.md` MUST print 2 (frontmatter line plus the Pattern 4.6 example, both `opus-5`); total across all SKILL.md is 35 (AC-3.3a).
  - **AC-3.3c** (ordering evidence): stamp commit/diff hunks are timestamped after prose hunks; Verification: inspection of the Stage 6 developer-dispatch report showing prose DoD PASS before stamp step.
- **G6 line budgets**: **AC-6** `python3 scripts/check_skill_budgets.py; echo "exit=$?"` MUST print `exit=0` (ran 2026-09-19: `BUDGET CHECK PASSED: 17 file(s) checked, 0 known-debt, 0 exception(s).` then `exit=0`). Prose edits in S2 are a precondition; S3 owns the gate as the last SKILL.md editor.

### S4 — Code IDs and literal sweep (closes G4, G-LIT)

- **FR-4.1** `agentic-flow-builder/scripts/agent_registry.py:190` becomes `"config": {"model": "claude-opus-5"},`. The provenance comment `# prior: claude-opus-4-7 (retired 2026-09-19, BACKLOG-108)` goes on its OWN line immediately ABOVE line 190 (BINDING-2.4, clarified). This is the ONE permitted 4.7 string outside CHANGELOG. Rationale: a comment-only line is already exempt from the guard (first non-space character is `#`); a trailing same-line comment is not, which is what made AC-1.2c unsatisfiable in Revision 1 (QA D2-1). Option (b) of the QA fix; the guard needs no extra exemption.
  - **AC-4.1**: `grep -c "claude-opus-5" agentic-flow-builder/scripts/agent_registry.py` MUST be >= 1; `grep -cF "# prior: claude-opus-4-7 (retired 2026-09-19, BACKLOG-108)" agentic-flow-builder/scripts/agent_registry.py` MUST be 1; and python asserts the line before the first `claude-opus-5` line starts (after stripping) with `# prior: claude-opus-4-7`. MUST print `OK` for the last check.
- **FR-4.2** `conftest.py` 4 fixture strings become `claude-opus-5`.
  - **AC-4.2**: `grep -c "claude-opus-4-7" delivery-team/tests/smoke/tests/conftest.py` MUST print 0 and `grep -c "claude-opus-5" delivery-team/tests/smoke/tests/conftest.py` MUST be >= 4.
- **FR-4.3** `smoke-test-architecture.md:115` example string becomes `claude-opus-5`.
  - **AC-4.3**: `grep -c "claude-opus-4-7" delivery-team/architecture/smoke-test-architecture.md` MUST print 0.
- **FR-4.4** Fixture authors are a SEPARATE dispatch from `metrics.py`/`baseline.py` authors (BINDING-4.5). Verification: dispatch manifest lists distinct agent IDs; and `git status --porcelain delivery-team/tests/smoke/lib` is empty at the moment the validator dispatch starts (the validator dispatch records this output).
- **AC-1b (repo-wide literal sweep; G-LIT)**: run the canonical counting command from section 1. After S1, S2 and S4 it MUST print exactly `claude-opus-4-7 hits 0 files 0` and `claude-opus-4-8 hits 0 files 0`. Before migration it prints `claude-opus-4-7 hits 9 files 5` (recorded above so a green run is meaningful). Because the script scans `.github`, the guard yml is covered here as well as by AC-1.2b. CHANGELOG.md is excluded by design.

### S5 — Smoke harness (closes G5)

Source-of-truth check (run 2026-09-19): `run_smoke.py` has NO `--effort` flag today (`grep -n "effort" delivery-team/tests/smoke/run_smoke.py` returns nothing). The baseline JSON has NO `model` key and its `metrics` keys are `wall_clock_seconds, cost_usd, tokens.input, tokens.output, tokens.cache_creation, tokens.cache_read, pipeline.*, skill_loads.*`; there is no `tokens.cache_hit_ratio` or `model_usage` today. S5 therefore ADDS these (schema extension), it does not merely "track" them.

- **FR-5.1** Add confirmed-observable metrics, always emitted (BINDING-4.1): `tokens.cache_hit_ratio` (derived: `cache_read / (cache_read + cache_creation + input)`, 0.0 when denominator is 0) and `model_usage.<model>.dispatches` for each of the three canonical IDs.
  - **AC-5.1**: python loads the baseline JSON and asserts `'tokens.cache_hit_ratio' in metrics` and that some key starts with `model_usage.claude-opus-5.`; MUST print `OK`.
- **FR-5.2** Best-effort metrics tolerate nulls and WARN, not FAIL, when absent (BINDING-4.2): `thinking_tokens`, `stop_details.refusal_code`, `speed_or_fast_indicator`. On Opus 5 `thinking.display` defaults to `"omitted"`, so thinking blocks arrive with an empty `thinking` field and the token count may be missing: best-effort stays correct.
  - **AC-5.2**: meta-test (authored by the separate validator dispatch) feeds a stream fixture lacking these fields; `python3 -m pytest delivery-team/tests/smoke/tests/test_meta.py -q` exits 0 and output contains a WARN line for each missing field (captured via `-rA`; the existing suite already uses pytest so no new dependency).
- **FR-5.3** Runner adds an `--effort` flag (value `xhigh` used for baseline capture and regression runs; BINDING-4.3), forwarded to the harness invocation. `xhigh` is valid on Opus 5 (section 8) but is a project choice, not the doc-recommended default (OQ-5). At `xhigh` thinking cannot be disabled (a `thinking: disabled` request returns 400), so the harness must not pass a disabled-thinking setting.
  - **AC-5.3**: `python3 delivery-team/tests/smoke/run_smoke.py --help | grep -c -- "--effort"` MUST be >= 1.
- **FR-5.4** Per-run `--cost-cap 3.00` enforced (flag exists today).
  - **AC-5.4**: baseline JSON `metrics['cost_usd']['hard_max']` MUST equal 3.0 (python one-liner).
- **FR-5.5** Baseline schema gains top-level `model` and `effort` fields (D-8 fix; single source of truth for the model under test). Written by `baseline.py` at capture time from the runner's resolved model and effort.
  - **AC-5.5** (G5 closing AC):
    ```bash
    python3 -c "import json; b=json.load(open('delivery-team/tests/smoke/baselines/hello_world_spike.json')); print(b.get('model'), b.get('effort'), b.get('n_samples'), b.get('sample_status'), bool(b.get('last_captured_utc')), bool(b.get('last_captured_git_sha')))"
    # MUST print: claude-opus-5 xhigh 5 active True True
    ```
- **FR-5.6** (BINDING-4.4) Existing 4.7-era baseline (`n_samples` 1, `partial-1-of-5`) is invalidated and re-captured on Opus 5 via `--init-baseline` (5 sequential samples, cost-capped). Old baseline is not merged with new samples.
  - **AC-5.6**: `last_captured_utc` in the new baseline is later than the S4 commit timestamp; `n_samples` equals 5 and `sample_status` equals `active` (covered by AC-5.5; timestamp inspection by QA).
- **FR-5.7** Before the first capture, the local `claude` CLI is confirmed to accept `--model claude-opus-5` (OQ-7, UNVERIFIED in docs: the CLI reference fetched shows `--effort` with `xhigh` but no `claude-opus-5` example).
  - **AC-5.7**: Verification: inspection; the S5 developer report records the exact command run and its exit status; if the CLI rejects the ID the story stops and raises the defect (no silent model substitution). Evidence line in the baseline `model` field (AC-5.5) must be the ID actually used.

### S6 — Cache re-freeze (closes G9)

- **FR-6.1** Re-fingerprint `governance/cache-prefix-hash.txt` after all SKILL.md edits are final (BINDING-5.3). The file holds one line in `sha256sum` format for `delivery-team/skills/delivery-flow/SKILL.md`.
  - **AC-6.1**: `sha256sum delivery-team/skills/delivery-flow/SKILL.md | diff - governance/cache-prefix-hash.txt && echo MATCH` MUST print `MATCH` (ran 2026-09-19 against the unmigrated tree: `MATCH`, so the command is well-formed; it must be re-run and re-frozen after S3). Scope may change per ADR-5-0-001; if so the ADR states the new command and this AC is updated by the Architect (OQ-3).
- **FR-6.2** ADR-5-0-001 records the fingerprint-scope decision (BINDING-5.5). Architect owns it; Developer implements without re-debate.
  - **AC-6.2**: `test -f .delivery/artifacts/04-architect/adrs/ADR-5-0-001-cache-fingerprint-scope.md && echo OK` MUST print `OK`.

### S7 — Memory, changelog, ship (closes G8, G10)

- **FR-7.1** Update binding memory file `.delivery/memory/topics/opus-5-migration.md` with run outcome.
  - **AC-7.1**: `grep -c "^## Run outcome" .delivery/memory/topics/opus-5-migration.md` MUST be >= 1.
- **FR-7.2** Add CHANGELOG entry naming BACKLOG-108. It may mention the retired IDs (CHANGELOG.md is excluded from AC-1b and from the guard by design).
  - **AC-7.2**: `grep -c "BACKLOG-108" CHANGELOG.md` MUST be >= 1.
- **FR-7.3** Ship via squash-rebase + ff-merge + push origin/main. No PR (BINDING-5.1). Verification: inspection; `git log origin/main -1` message references BACKLOG-108 and `git rev-list --count origin/main..HEAD` equals 0 after push.
- **FR-7.4** Dispatch manifest: each stage writes `.delivery/artifacts/<NN-stage>/dispatch-manifest.txt`. Line 1 is `expected_validators: N` (N = length of that stage's `dod_validators` list); each following line is `<role><TAB><agent-id>`, one per dispatch. Introduced by this initiative because no manifest exists today.
  - **AC-DISP** (G8 closing AC): for every stage directory containing a manifest, python asserts `N == number of dispatch lines` and that all roles on dispatch lines are distinct (no fused roles, BINDING-5.4); MUST print `0 violations`.
- **FR-7.5** Housekeeping: references to the retired filenames are fixed.
  - **AC-7.5**: `test -f .delivery/backlog/BACKLOG-108-opus-5-migration.md && test -f .delivery/memory/topics/opus-5-migration.md && test ! -e .delivery/backlog/BACKLOG-108-opus-4-8-migration.md && test ! -e .delivery/memory/topics/opus-4-8-migration.md && echo OK` MUST print `OK` (ran at end of Revision 2: OK). Historical stage artifacts under `.delivery/artifacts/01-idea/` still cite the old filenames and are immutable stage records; they are not rewritten (noted in Revision 2 changelog).

## 4. Non-Functional Requirements

| ID | Requirement | Target | Measurement |
|----|-------------|--------|-------------|
| NFR-1 | Cost per smoke run | <= $3.00 | `metrics.cost_usd.hard_max == 3.0` and per-sample `cost_usd` <= 3.0 in raw run reports |
| NFR-2 | Total baseline capture budget | <= $15.00 (5 x $3) | sum of `cost_usd` across the 5 captured samples <= 15.0 (python sum over run reports). Risk: Opus 5 thinking is on by default and thinking tokens bill as output, so per-run cost may exceed the 4.7-era run (R6) |
| NFR-3 | Wall clock per run | <= 1800 s | `wall_clock_seconds.hard_max == 1800.0` |
| NFR-4 | Line-budget breaches | 0 | AC-6 exit code 0 |
| NFR-5 | Guard false positives on migrated tree | 0 | AC-1.2c prints 0 |
| NFR-6 | Baseline sample count | exactly 5, sequential | AC-5.5 prints `n_samples` 5; runner `concurrency: 1` |
| NFR-7 | Provisional/hedged behavioral claims shipped | 0 | AC-2.3 prints 0 |
| NFR-8 | CI runtime dependencies | none beyond checkout + bash/python stdlib | AC-1.3 prints 0 and `git diff main -- .github | grep -c "pip install"` MUST print 0 |
| NFR-9 | Meta-test suite wall clock | < 5 s (existing contract in `test_meta.py`) | pytest `--durations` total under 5 s |

## 5. Success Gates: one work item closes each gate

| Gate | Closing story | Closing AC | Precondition stories |
|------|---------------|-----------|---------------------|
| G1 — Guard is a positive Opus 5 allowlist and rejects 4-7 and 4-8 fixtures | S1 | AC-1.1, AC-1.2a, AC-1.2b, AC-1.3 | none |
| G-LIT — Zero live `claude-opus-4-7` / `claude-opus-4-8` literals repo-wide | S4 | AC-1b, AC-1.2c | S1, S2 (prompt-engineer:368) |
| G2 — 34 frontmatter stamps = `opus-5` (25 updated + 9 created), 35 total lines | S3 | AC-3.2, AC-3.3a | S2 |
| G3 — 34/34 prose-reviewed, no `frontmatter-only` | S3 | AC-3.1, AC-3.1b | S2 |
| G4 — Registry heavy-tier ID = `claude-opus-5` + provenance | S4 | AC-4.1 | none |
| G5 — 5-sample baseline live against `claude-opus-5` | S5 | AC-5.5 | S4 (fixtures) |
| G6 — Line budgets pass | S3 | AC-6 | S2 |
| G7 — Behavioral claims doc-verified, zero provisional | S2 | AC-2.3, AC-2.3b, AC-2.5 | none |
| G8 — One-role-one-agent dispatch honored | S7 (closer; checks all stage manifests) | AC-DISP | all stories |
| G9 — Cache fingerprint re-frozen, ADR-5-0-001 filed | S6 | AC-6.1, AC-6.2 | S2, S3 |
| G10 — Shipped to origin/main with no PR | S7 | FR-7.3 inspection | S1-S6 |

Ownership rule: one gate, one closing story. Preconditions are inputs, not co-ownership.

## 6. Smoke-test maximal-tracking requirements

Confirmed-observable, always tracked (BINDING-4.1): `tokens.cache_hit_ratio`, `model_usage.<model>.dispatches` (FR-5.1).
Best-effort, WARN when absent (BINDING-4.2): `thinking_tokens` (Opus 5: adaptive thinking on by default; `thinking.display` defaults to `omitted`, so blocks arrive with an empty `thinking` field), `stop_details` refusal codes (publicly documented for Opus 5), speed/`fast` indicators.
Runner: `--effort xhigh` (FR-5.3; valid on Opus 5; project choice, see OQ-5).
Producer-validator separation (BINDING-4.5): meta-test fixtures for `metrics.py`/`baseline.py` authored in a SEPARATE Agent dispatch; invariant: `git status --porcelain delivery-team/tests/smoke/lib` empty during the validator dispatch (FR-4.4).

## 7. Dependencies, Risks, Assumptions

### Dependencies

| Dependency | Status |
|------------|--------|
| Opus 5 doc pages (models overview, Opus 5 migration guide, effort, prompting Opus 5) reachable | Confirmed (fetched 2026-09-19) |
| `claude` CLI available locally for baseline capture | Confirmed (local-dev only); acceptance of `--model claude-opus-5` UNVERIFIED (OQ-7, FR-5.7) |
| `plugin-dev:skill-development` skill available | Confirmed |
| Story order S1 -> S2 -> S3 -> S4 -> S5 -> S6 -> S7 | Confirmed (BINDING-2.5) |
| Architect authors ADR-5-0-001 before S6 | Pending (Stage 4) |
| Anthropic API budget of ~$15 for baseline | Pending (user's account; at risk if rate limits bite or thinking-on cost exceeds the 4.7-era run) |

### Risks

| ID | Risk | L | I | Mitigation |
|----|------|---|---|-----------|
| R1 | Dispatch discipline: roles fused (quality) or sub-agents over-spawned (cost). Opus 5 delegates more readily than prior models (section 8) | M | H | AC-DISP manifest; one-role-one-agent enforced at DoD; dispatch count capped at `dod_validators` length |
| R2 | Prose sweep touches 34 files and breaches line budgets | M | M | AC-6 exit 0; `Budget-Exception:` protocol; S2 keystone-first |
| R3 | Baseline drift or cost overrun | M | M | `--cost-cap 3.00`, sequential, NFR-1/2 |
| R4 | Guard false positive on legitimate text | L | M | AC-1.2c zero-hit check; `#` and `>` exemptions retained; CHANGELOG excluded; provenance comment on its own line |
| R5 | Unverified behavioral claim leaks into prose | M | H | AC-2.3 scan + AC-2.3b independent re-fetch; OQ-2 and OQ-8 claims never ship |
| R6 | Opus 5 thinking on by default plus `xhigh` makes each smoke run costlier than the 4.7-era run and may hit the $3 cap | M | M | cost cap fails the run loudly; fall back to `high` per OQ-5 via Architect decision; no silent cap change |
| R7 | Docs list `claude-sonnet-5` as the current Sonnet; the allowlist mid tier remains `claude-sonnet-4-6` (legacy-available) | L | L | OQ-6; out of scope of this retarget; the guard will flag any `claude-sonnet-5` string until the allowlist is revisited (0 occurrences in tree today) |

### Assumptions

1. The `claude-opus-5` ID is stable for the duration of the migration (VERIFIED in section 8: "fixed model ID with no date suffix"; retirement not sooner than July 24, 2027).
2. `git diff main` in the worktree is the correct baseline for body-delta checks (the branch forks from main).
3. `test_meta.py` continues to run under the existing pytest setup (no new dependency).
4. Deleting the 4.7-era baseline does not break any consumer; baseline is read only by `baseline.py`.
5. The repo has no direct Anthropic API calls with `thinking`, sampling or prefill parameters (the code uses the model ID as a string label), so the Opus 5 API breaking changes do not apply to repo code; the smoke harness drives the `claude` CLI.

## 8. Citations: Opus 5 behavioral claims

All rows fetched live on 2026-09-19. The model ID `claude-opus-5` is known-good. Quotes are copied from the fetched pages.

| Claim | Verdict | Source URL and quote |
|-------|---------|----------------------|
| Model ID literal is `claude-opus-5`, no date suffix | VERIFIED | https://platform.claude.com/docs/en/models/opus-5/migration-guide : "`claude-opus-5` is a fixed model ID with no date suffix" |
| Opus 5 is current; Opus 4.8 and 4.7 are legacy still available | VERIFIED | https://platform.claude.com/docs/en/about-claude/models/overview : "start with Claude Opus 5 for most workloads"; "Legacy models (still available): ... Claude Opus 4.8, Claude Opus 4.7 ..." |
| 1M-token context window, 128K max output | VERIFIED | overview table: "Context window 1M tokens", "Max output 128K tokens" |
| Reliable knowledge cutoff May 2026 | VERIFIED | overview table: "Reliable knowledge cutoff ... May 2026" |
| Retirement not sooner than July 24, 2027 | VERIFIED | overview table |
| Default effort `high`; setting `high` equals omitting the parameter | VERIFIED | https://platform.claude.com/docs/en/build-with-claude/effort : "The API default is `high`."; "Setting `effort` to `\"high\"` produces exactly the same behavior as omitting the `effort` parameter entirely." |
| `xhigh` valid on Opus 5; recommended start is `high`, step up to `xhigh` for demanding coding and agentic work | VERIFIED (this corrects the 4.8-era "start with xhigh") | effort doc, "Recommended effort levels for Claude Opus 5": "Start with `high`, the default, and adjust based on your evals: step up to `xhigh` for demanding coding and agentic work" |
| Effort levels recalibrated vs Opus 4.7; run a fresh sweep | VERIFIED | Opus 5 migration guide, section "Migrating to Claude Opus 5 from Claude Opus 4.7": "Effort levels recalibrated: The token allocation behind each effort level changes on Claude Opus 5 compared to Claude Opus 4.7 ..." |
| Thinking on by default (adaptive); `thinking.display` defaults to `omitted` | VERIFIED | migration guide (4.8 to 5 section), breaking change 1: "on Claude Opus 5, the same requests run with adaptive thinking" |
| Thinking cannot be disabled at `xhigh` or `max` effort (400 error) | VERIFIED | migration guide breaking change 2; effort doc: "thinking cannot be disabled at `xhigh` or `max` effort" |
| Set large `max_tokens` at `xhigh`/`max`; start at 64k | VERIFIED | effort doc and migration guide recommended change 1 |
| Opus 5 delegates to subagents MORE readily than prior models; give delegation guidance or cap spawn counts | VERIFIED (reverses the 4.8-era "dispatches fewer sub-agents" claim) | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5 : "Claude Opus 5 delegates to subagents more readily than prior models." |
| Opus 5 verifies its own work; explicit verification instructions cause over-verification | VERIFIED | prompting-claude-opus-5, "Task scope and over-verification": "instructions like these cause over-verification on Claude Opus 5" |
| Default responses and written deliverables run longer; effort does not reliably shorten them | VERIFIED | prompting-claude-opus-5 "Response length and verbosity"; effort doc |
| Prompt-cache minimum 512 tokens (was 1,024 on Opus 4.8) | VERIFIED (corrects the 4.8-era row) | migration guide, recommended change 3: "The minimum cacheable prompt length on Claude Opus 5 is 512 tokens, down from 1,024 tokens on Claude Opus 4.8." |
| Refusal `stop_details` publicly documented; mid-conversation system messages accepted | VERIFIED | migration guide (4.7 section): "adds mid-conversation system messages and publicly documents refusal stop details" |
| `claude` CLI has an `--effort` flag with `low, medium, high, xhigh, max, ultracode` | VERIFIED | https://code.claude.com/docs/en/cli-reference : "Options: `low`, `medium`, `high`, `xhigh`, `max`, or `ultracode`. Available levels depend on the model." |
| "Opus 5 dispatches fewer sub-agents than 4.7/4.8" | REFUTED by docs; must never ship | see delegation row |
| "Opus 5 follows instructions more literally than 4.8" | UNVERIFIED as a general claim; do not ship. Docs support only a narrow case: a "be conservative" review prompt "may" be followed literally (prompting-claude-opus-5, Code review bullet). Literalism is documented as a 4.7 trait vs 4.6 | see OQ-2 |
| Local `claude --model claude-opus-5` accepted | UNVERIFIED (CLI reference shows examples for `claude-sonnet-5`, none for `claude-opus-5`) | see OQ-7 |
| Claude Code default effort on Opus 5 is `high` | UNVERIFIED (API default is documented; the Claude Code default was not found for Opus 5) | see OQ-8 |

## 9. Open Questions

| ID | Question | Owner | Due | Why non-blocking |
|----|----------|-------|-----|------------------|
| OQ-1 | RESOLVED by doc: Opus 5 delegates MORE readily (not fewer). Confirm the S2 dispatch prose reflects the over-delegation direction | Architect | Stage 4 | Claim is VERIFIED and cited (section 8); FR-2.3, FR-2.5 encode it |
| OQ-2 | Does a doc source exist for "more literal instruction following" on Opus 5 versus 4.8? | Architect | Stage 4 | No shipped prose depends on it; AC-2.3 and adversarial re-fetch catch leakage; only the narrow review-prompt case is documented |
| OQ-3 | Should the cache fingerprint scope widen beyond `delivery-flow/SKILL.md`? | Architect (ADR-5-0-001) | Stage 4 | Default AC-6.1 is runnable with current scope; ADR may only refine the command |
| OQ-4 | Where do `dod_validators` counts live per stage, to populate the manifest header? | Architect | Stage 4 | FR-7.4 defines the manifest format independent of source; developer reads the count from the stage definition |
| OQ-5 | Use `xhigh` (BINDING-4.3, project choice) or `high` (doc default and recommended start) for the smoke baseline? | Architect | Stage 4 | `xhigh` is valid and documented; cap and cost are enforced either way; FR-5.5 records the effort actually used |
| OQ-6 | Docs list `claude-sonnet-5` as current Sonnet; the allowlist keeps `claude-sonnet-4-6`. Revisit mid tier? | Michael / Architect | after BACKLOG-108 | Retarget was Opus-only; `claude-sonnet-5` has 0 occurrences in the tree |
| OQ-7 | Does the installed `claude` CLI accept `--model claude-opus-5`? UNVERIFIED | Developer (S5, FR-5.7) | S5 start | Checked by running the command before capture; failure stops S5 with a defect |
| OQ-8 | Is the Claude Code default effort on Opus 5 `high`? UNVERIFIED | Developer (S5) | S5 start | Runner sets effort explicitly; claim never ships in prose |

## 10. Scope

**In scope**: all 34 SKILL.md (prose + stamps); guard rewrite; `agent_registry.py:190` (+ provenance comment line above); `prompt-engineer/SKILL.md:368` and :415; `conftest.py` x4; `smoke-test-architecture.md:115`; runner `--effort`; baseline schema (`model`, `effort`, `tokens.cache_hit_ratio`, `model_usage`); baseline re-capture; cache re-fingerprint; ADR-5-0-001; dispatch manifests; memory + CHANGELOG; the file renames listed in the Revision 2 changelog.

**Out of scope**: `prd-quality-gate-flow/` routing aliases (BINDING-1.4; the AC-1b scan returns none there, so no explicit exemption code is needed); any `.github/workflows/smoke-*.yml` (BINDING-4.6, checked by AC-1.3); any PR (BINDING-5.1); changing mid/light allowlist tiers (OQ-6); rewriting Stage 1 historical artifacts.

## 11. Constraints

1. Plugin-dev skill routing is non-optional (CLAUDE.md).
2. Budget ~$15 total, `--cost-cap 3.00` per run.
3. Behavioral claims doc-verified (BINDING-3.1 to 3.3).
4. Line budgets A=500 / B=300 / C=200; exceptions need `Budget-Exception:` + `known_debt[]` with `target_wave:`.
5. One Role = One Sub-Agent (BINDING-5.4).
6. No dual-allow window (BINDING-2.1).
7. Producer-validator separation for meta-tests (BINDING-4.5).
8. Bash / python-stdlib only in ACs.
9. Local-only: nothing in `.github/workflows/` shells out to `claude`.

## 12. Stop-rule

Defects/story > 0.4 across any 3-story window pauses the initiative. Current rolling rate = 0.111.

## 13. Revision 1 changelog

| QA defect | Fix |
|-----------|-----|
| D-1 FR->AC coverage | Every FR has a named AC; process-only FRs tagged "Verification: inspection". New FRs: 5.5, 5.6, 7.4. |
| D-2 NFRs | NFR-1..9 with numeric targets and commands. |
| D-3 Gate ownership | G1->S1; G-LIT->S4; G6->S3; G8->S7; G9->S6; G10->S7; preconditions separate. |
| D-4 AC-DISP | FR-7.4 defines `dispatch-manifest.txt`; AC-DISP is a python check. |
| D-5 Weak ACs | AC-1.1 per-ID grep; AC-1.2b; AC-3.3a anchored; CHANGELOG excluded; walk.py prunes dirs. |
| D-6 Open questions | Section 9 with owner, due stage, non-blocking rationale. |
| D-7 Missing sections | Personas, dependencies, risks, assumptions added. |
| D-8 AC-5 vs schema | FR-5.5 adds `model`/`effort`; FR-5.1 adds metrics. |
| D-9 False positives | AC-2.3 scoped, excludes research-agent rubric prose. |
| D-10 constraints.yml | `entities` and `invariants` added; validator passing. |
| D-11 Discovery numbers | Stamp numbers corrected (see Revision 2: literal counts still wrong in Revision 1). |
| D-12 Body-delta | AC-3.1 machine check over all 34 files. |
| D-13 BINDING-4.4 | FR-5.6 baseline invalidate and re-capture. |

## 14. Revision 2 changelog

**Retarget (user decision, binding): Opus 4.8 -> Opus 5.** Every target reference moved: model ID `claude-opus-5`; stamps `model_awareness: opus-5`, `pattern_library_version: 5-0-1`, `last_audited: 2026-09-19`; guard allowlist; literal IDs; smoke harness (`model_usage.claude-opus-5.*`, baseline `model: claude-opus-5`, effort); baseline re-capture; cache re-fingerprint; ADR renamed ADR-4-8-001 -> ADR-5-0-001; prompt-engineer `MODEL_ID`. The stale-FROM state is 4.7 only; `claude-opus-4-8` has 0 occurrences in code/docs (canonical command, section 1) and becomes a rejected ID in the guard. The prior killed Revision-2 attempt targeting 4.8 left prd.md unchanged (still Revision 1); this file is one coherent rewrite.

**Behavioral-claim corrections from live doc re-verification (section 8):**

| 4.8-era claim | Opus 5 outcome |
|---|---|
| "4.8 dispatches fewer sub-agents by default" (OQ-1) | Reversed: Opus 5 delegates more readily. R1, FR-2.3, FR-2.5 rewritten toward steering and capping delegation. |
| "4.8 follows instructions more literally" (OQ-2) | Not verifiable as a general Opus 5 claim; narrow review-prompt case only. Stays out of shipped prose. |
| `xhigh` is the recommended start | Corrected: recommended start is `high`; `xhigh` valid. Kept as project choice, OQ-5. |
| Adaptive thinking off by default | Reversed: on by default; disabling capped at `high` effort or below. FR-5.3, R6 added. |
| Cache minimum 1,024 tokens | Corrected: 512 tokens. |
| Knowledge cutoff Jan 2026 | Corrected: May 2026. |

**QA round 2 defects (evaluation-round-2.md):**

| Defect | Fix |
|---|---|
| D2-1 AC-1.2c conflicts with FR-4.1 trailing comment | Option (b): FR-4.1 puts the provenance comment on its own line above the registry line; the guard's existing `#`-first-char exemption covers it; AC-1.2c and NFR-5 reachable at 0; AC-4.1 checks the placement; memory BINDING-2.4 updated. |
| D2-2 Literal counts do not reproduce | Section 1 defines ONE canonical counting command with explicit excludes (`.git`, `.delivery`, `./.claude/worktrees`; `.github` included), with exact output: 9 hits in 5 files (7 in 4 files without the guard yml). Every section now uses these numbers; the "six files", "7 in five sites" and "today's value 9 via walk.py" statements are deleted. `walk.py` now scans `.github`. |
| D2-3 AC-1.2a portability | FR-1.2 contract: `STALE_RE` and `ALLOW_RE` are grep -E and Python compatible (no POSIX classes, no single quotes, no lookaheads); AC-1.2a tests the patterns with five fixtures. |
| D2-4 git diff assumptions | AC-3.1 states that no SKILL.md is created, so `git diff main` on tracked files suffices; the untracked-files parenthetical is deleted. |

**Other changes**: FR-2.5 (testable delegation rule), FR-5.7 (CLI accepts `claude-opus-5`), FR-7.5 (renames) added; OQ-5 to OQ-8 added; R6, R7 added; assumption 5 added. `.delivery/state.md` references were updated to the new filename and "Opus 5 migration". Historical stage-1 artifacts (`.delivery/artifacts/01-idea/**`) still cite `opus-4-8-migration.md` and "Opus 4.8"; they are immutable stage records and not rewritten here.

**Renamed by Revision 2**: `.delivery/backlog/BACKLOG-108-opus-4-8-migration.md` -> `BACKLOG-108-opus-5-migration.md`; `.delivery/memory/topics/opus-4-8-migration.md` -> `opus-5-migration.md`; `.delivery/memory/index.md` links updated.

**Commands run and results (2026-09-19, worktree root)**: canonical count (9/5 and 0/0, section 1); stamp census (`skill 34`; `26 25 {...19, ...7}`); `check_skill_budgets.py` exit 0; cache hash `MATCH`; AC-1.3 `0` and `0`; AC-2.3 hedge scan `0`; AC-1.2a fixture logic run against a mock of the pattern contract: `OK`; `validate_constraints.py`: valid, rc=0.

— Gandalf, PO, run-2026-05-28-backlog-108.

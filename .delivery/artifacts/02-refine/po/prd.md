<!-- run: run-2026-05-28-backlog-108 -->
# PRD — Latest-Model References (Revision 5)

**Backlog**: BACKLOG-108-latest-model-references.md (renamed from BACKLOG-108-opus-5-migration.md, itself renamed from BACKLOG-108-opus-4-8-migration.md)
**Project Type**: FEATURE
**Stage**: 2 — Refine (LIGHT), Revision 5 (Team DoD validation round 1: QA 3 blocking plus warnings, Architect 9 warnings, Developer and PO warnings addressed; design of Revision 3 unchanged: latest-version references, no pins)

**Reader's guide (PO DoD warning: length)**: a builder reads sections 1, 3, 5 and 8 first (problem and canonical count; requirements with runnable ACs; gate table; citations). Sections 13 to 17 are revision history only. The Stage 1 idea brief (`.delivery/artifacts/01-idea/po/idea-brief.md`) is SUPERSEDED: it still says "Opus 4.8 Migration", a positive allowlist guard and 9 new stamps. It is an immutable record (AC-7.5) and carries no supersession note of its own; downstream stages read THIS PRD and `.delivery/memory/topics/latest-model-references.md`, never the brief. Older superseded rulings inside the memory topic (Sections 1 to 6, with 4.7/4.8/5 IDs) sit under `.delivery/`, which the guard excludes; they are history, not leftovers.
**PO**: Gandalf
**Date**: 2026-09-20; run id run-2026-05-28-backlog-108 unchanged
**Binding context**: `.delivery/memory/topics/latest-model-references.md` (AUTHORITATIVE; renamed from `opus-5-migration.md`)

> A wizard does not carve the model's name into every stone. Say "latest Opus" once, say it everywhere, and the next release costs nothing.

**Decision recorded (binding, not re-debated; user, 2026-09-20)**: the repo stops hard-pinning model version strings (`claude-opus-4-7`, `claude-opus-4-8`, `claude-opus-5`, and any future ID) in prose, stamps and guards. It refers to the latest version of a model family ("latest Opus", "latest Sonnet"). BACKLOG-108 is reframed from "migrate all pins to claude-opus-5" to "remove version pinning; adopt latest-version references; migrate today's stale 4.7 pins to that scheme". The team runs on Opus 5, which is the effective current model on 2026-09-20; that fact lives in citations and baselines, never in shipped prose or stamps.

---

## 1. Problem

The repo hard-codes model versions in four kinds of place: SKILL.md stamps (`model_awareness: opus-4-7`, `pattern_library_version: 4-7-1`), prose ("Opus 4.7", bare "4.7"), code/doc string literals (`claude-opus-4-7` and friends), and a CI guard that allowlists specific IDs. Every model release forces a repo-wide migration (BACKLOG-108 is that migration for the third time: 4.7, 4.8 attempt, 5). The fix is structural: stop encoding versions.

### Canonical counting command (the ONE source of every literal count in this PRD)

Revision 5 rewrites the command (QA blocking findings 1 and 2, Developer finding 2, Architect finding 9). It is now SELF-CONTAINED (no shared `/tmp/walk.py`: a stale or parallel copy of that file was a fragile dependency) and its file scope is the same as the guard script's: `git ls-files --cached --others --exclude-standard`, i.e. tracked plus untracked-not-ignored files, so a new file is counted before it is staged and the local ship gate and this count cannot disagree. Under the contract (FR-1.2) nothing is exempt: no comment, blockquote, heading or fence exemption, and NO per-line marker (Revision 4's `model-pin-ok` escape is removed, FR-1.6). The command skips everything under `.delivery/`, scans `*.py *.md *.yml *.yaml *.txt *.sh` (JSON is out of scope by design: baselines record observed model IDs), skips `CHANGELOG.md` (history may name any ID), and classifies each hit line once: `pin` (PIN_RE), else `stamp` (STAMP_RE), else `prose` (`.md` files only: PROSE_RE or BARE_RE, both applied AFTER COUNT_RE matches are blanked out, so a count or duration such as "Sonnet 4 stories" or "in 5.0 seconds" is not a version). PIN_RE, STAMP_RE and BARE_RE are matched case-insensitively (`re.I`, `grep -Ei`); PROSE_RE and COUNT_RE are matched case-sensitively (`grep -E`, `sed -E`).

The counting command (run from the repository root; no other file is needed):

```bash
python3 - <<'PY'
import os, re, subprocess
PIN_RE = r"claude-[a-z0-9.-]*([0-9]|-latest)"
STAMP_RE = r'model_awareness: *"?[a-z-]*[0-9]|pattern_library_version: *"?([0-9v]|[a-z-]*[0-9]+[.-][0-9])'
PROSE_RE = r"(Opus|Sonnet|Haiku|Fable|Mythos|OPUS|SONNET|HAIKU|FABLE|MYTHOS)[ -]*v?[0-9]|(opus|sonnet|haiku|fable|mythos)(-v?[0-9]|v?[0-9]| v?[0-9]+[.][0-9])"
BARE_RE = r"(^|[^A-Za-z])(on|under|in|for|the|new|so|with|isolates?) v?[4-9][.][0-9]+([^0-9A-Za-z]|$)|[4-9][.-][0-9]+-(only|aware)"
COUNT_RE = r"(Opus|Sonnet|Haiku|Fable|Mythos) +[0-9]+ +(times|stories|story|reviewers?|reviews?|agents?|subagents?|passes|rounds?|runs?|instances?|copies|cycles?|iterations?|tasks?|items?|personas?|judges?)([^A-Za-z]|$)|([Oo]n|[Uu]nder|[Ii]n|[Ff]or|[Tt]he|[Nn]ew|[Ss]o|[Ww]ith|[Ii]solates?) v?[0-9]+[.][0-9]+ *(seconds?|secs?|ms|minutes?|mins?|hours?|hrs?|days?|weeks?|months?|years?|times|percent|points?|GB|MB|KB)([^A-Za-z]|$)"
def files(exts=None, name=None):
    for f in sorted(set(subprocess.run(['git', 'ls-files', '--cached', '--others', '--exclude-standard'], capture_output=True, text=True, check=True).stdout.split('\n'))):
        if f and not f.startswith('.delivery/') and os.path.isfile(f) and (not name or os.path.basename(f) == name) and (not exts or f.endswith(exts)):
            yield './' + f
cat = {'pin': 0, 'stamp': 0, 'prose': 0}
hits = {}
listing = {}
for f in files(exts=('.py', '.md', '.yml', '.yaml', '.txt', '.sh')):
    if f.endswith('CHANGELOG.md'):
        continue
    for i, l in enumerate(open(f, errors='ignore'), 1):
        b = re.sub(COUNT_RE, ' ', l)
        if re.search(PIN_RE, l, re.I):
            k = 'pin'
        elif re.search(STAMP_RE, l, re.I):
            k = 'stamp'
        elif f.endswith('.md') and (re.search(PROSE_RE, b) or re.search(BARE_RE, b, re.I)):
            k = 'prose'
        else:
            continue
        cat[k] += 1
        hits.setdefault(f, []).append(i)
        if k != 'stamp':
            listing.setdefault((k, f), []).append(i)
print('guard-scope hits', sum(cat.values()), 'files', len(hits))
print('  pin', cat['pin'], 'stamp', cat['stamp'], 'prose', cat['prose'])
for (k, f) in sorted(listing):
    print('  ', k, f, listing[(k, f)])
PY
```

**Exact output of the Revision 5 command above, run from the worktree root on 2026-09-20 (before any migration edit; identical to the Revision 4 numbers, because the COUNT_RE blanking removes no line that is hit today and the file scope change adds and drops none):**

```
guard-scope hits 91 files 31
  pin 20 stamp 52 prose 19
   pin ./.github/workflows/stale-model-id-guard.yml [23, 24, 25, 30, 31, 39]
   pin ./agentic-flow-builder/scripts/agent_registry.py [148, 149, 173, 174, 189, 190]
   pin ./delivery-team/architecture/smoke-test-architecture.md [115, 116]
   pin ./delivery-team/references/telemetry-schema.md [36]
   pin ./delivery-team/tests/smoke/tests/conftest.py [105, 117, 129, 151]
   pin ./prompt-engineer/SKILL.md [368]
   prose ./delivery-team/references/shared/orchestrator-doctrine.md [77, 79, 82]
   prose ./delivery-team/skills/delivery-flow/SKILL.md [27, 30, 273, 276]
   prose ./prompt-engineer/SKILL.md [88, 347, 349, 351, 356, 359, 361, 373, 375, 397, 401, 408]
```

Cross-check (R12, executed): a simulated `scripts/check_model_pins.py` holding the same five constants and `files()` printed `guard-scope hits 91 files 31` and a `--list` whose 91 lines match the listing above. Reading: 91 hit lines in 31 files: 20 pin lines, 52 stamp lines (26 `model_awareness` plus 26 `pattern_library_version`), 19 prose lines. Expected closing state after S1 to S4: `guard-scope hits 0 files 0`. Why the numbers moved from Revision 3 (14 pinned-ID hits in 6 files; 8 prose lines in 2 files): (a) the comment exemption is gone, so 6 more pin lines surface (guard yml comments 23 to 25, registry provenance comments 148, 173, 189); (b) the prose census in Revision 3 counted only `Opus 4.7` style strings; bare `4.7` lines (delivery-flow 30 and 276; prompt-engineer 88, 349, 351, 359, 361, 373, 375, 401, 408) and a third file, `delivery-team/references/shared/orchestrator-doctrine.md` (77, 79, 82, a mirror of the delivery-flow 4.7 block), were missed. Two more prose lines are NOT matched by any regex but contradict the scheme and are named by hand in FR-2.1: `prompt-engineer/SKILL.md:371` (tells authors to hardcode IDs with a `# canonical <date>` comment) and `:420` (stamp-doc bullet "the model generation the skill was authored ... against").

| # | Site | Hits | Treatment |
|---|------|------|-----------|
| 1 | `.github/workflows/stale-model-id-guard.yml:23-25,30,31,39` | 6 | rewritten (S1); patterns move to `scripts/check_model_pins.py` |
| 2 | `agentic-flow-builder/scripts/agent_registry.py:148,149,173,174,189,190` | 6 | tier aliases from ONE central dict; comments reworded (FR-4.1) |
| 3 | `delivery-team/architecture/smoke-test-architecture.md:115,116` | 2 | synthetic fixture IDs (FR-4.3) |
| 4 | `delivery-team/references/telemetry-schema.md:36` | 1 | synthetic example (FR-4.3) |
| 5 | `delivery-team/tests/smoke/tests/conftest.py:105,117,129,151` | 4 | synthetic fixture IDs (FR-4.2) |
| 6 | `prompt-engineer/SKILL.md:368` | 1 | config-read snippet (FR-2.2) |
| 7 | prose: delivery-flow (4), prompt-engineer (12), orchestrator-doctrine (3) | 19 | family-relative rewrite (FR-2.1, FR-2.6) |
| 8 | stamps: 25 SKILL.md | 52 | version-free stamps (FR-3.2) |

### Stamp census (self-contained; repository root, 2026-09-20)

```bash
python3 - <<'PY'
import os, subprocess
from collections import Counter
def files(exts=None, name=None):
    for f in sorted(set(subprocess.run(['git', 'ls-files', '--cached', '--others', '--exclude-standard'], capture_output=True, text=True, check=True).stdout.split('\n'))):
        if f and not f.startswith('.delivery/') and os.path.isfile(f) and (not name or os.path.basename(f) == name) and (not exts or f.endswith(exts)):
            yield './' + f
sk = list(files(name='SKILL.md'))
print('skill', len(sk))
L = [(f, l.rstrip()) for f in sk for l in open(f) if l.lstrip().startswith('model_awareness:')]
print(len(L), len({f for f, _ in L}), dict(Counter(l for _, l in L)))
PY
```

Exact output: `skill 34` then `26 25 {'model_awareness: opus-4-7-frontmatter-only': 19, 'model_awareness: opus-4-7': 7}`. So 34 SKILL.md; 26 stamp lines in 25 files (prompt-engineer has two: frontmatter line 6 and a documentation example at 415); 9 files carry no stamp (4 user-feedback personas, 5 research-agent types). `pattern_library_version:` is version-coded too: 26 lines, all `4-7-1`, in the same 25 files (`grep -rh "^pattern_library_version:" --include=SKILL.md . | sort | uniq -c` prints `26 pattern_library_version: 4-7-1`).

Stale stamps lie, and versioned stamps rot on every release. Replace them with a stamp that has no version in it.

### Tier-alias frontmatter census (new; F7)

`grep -rnE "^(model|phase_1_detector_model):" --include=SKILL.md .` finds 9 lines in 9 SKILL.md, all alias-form already: `model: sonnet` (delivery-flow, architect/paradigms/ddd, architect/paradigms/volatility), `model: opus` (prompt-engineer), `phase_1_detector_model: haiku` (architect, operations, product-delivery, ui, quality). AC-4.6 pins the vocabulary to `opus|sonnet|haiku`.

## 2. Personas

| Persona | Goal | Pain today | Context |
|---------|------|------------|---------|
| Plugin maintainer (Michael) | A model release costs zero repo edits | Three migrations in one quarter; 25 files carry versioned stamps | Ships via squash-rebase + ff-merge to main, local-only tooling |
| Downstream plugin consumer | Skills whose guidance is written for the model actually running | Prose says "Opus 4.7"; registry sends heavy-tier work to a legacy label | Installs from marketplace, cannot see internal audit state |
| Local reviewer / CI gate reader | A guard that fails only when a version pin is re-introduced | Guard enforces a version allowlist that must be edited on every release | Reads static CI output only (no `claude` CLI in CI) |

## 3. Functional Requirements and Acceptance Criteria

Seven stories, strict order (BINDING-2.5, keystone-first). Every AC is bash or python-stdlib only, runnable from repo root, no `yq`, no new CLI dependency. "Verification: inspection" means a named artifact is inspected by the QA validator (process-only FRs). Every AC snippet is SELF-CONTAINED (Revision 5): none reads a shared `/tmp` file; those that walk the tree carry the same five-line `files()` helper as the canonical command in section 1, and those that import the guard read `scripts/check_model_pins.py` by relative path. Each snippet is a `python3 - <<'PY'` block whose body is indented in this document (strip the indent to run it). ACs are judged for well-formedness; several are expected to fail until their story lands.

**Convention (the new scheme, stated once).**
1. Prose: name a model FAMILY ("the latest Opus", "the latest Sonnet"), never a version. Behaviour claims in SKILL.md are written as guidance that holds for the current documented latest model and carry no version number; the dated, versioned citation lives in PRD/memory (`.delivery/`), which the guard does not scan.
2. Stamps: `model_awareness: latest` (no digits). `pattern_library_version: rev-1` (a revision counter, no model version). `last_audited: <YYYY-MM-DD>` is the time anchor: it says "audited against whatever was latest on this date".
3. Code that labels a model tier: the Claude Code CLI aliases `opus`, `sonnet`, `haiku` (verified in section 8), defined ONCE in `agent_registry.py` (FR-4.1).
4. Code that must call the Claude API: NOT AVAILABLE as a "latest" reference. The API has no evergreen alias for current models (section 8). Such code reads one configuration value (an environment variable or config key) so the ID lives in exactly one place outside the repo tree. No repo code calls the API today (FR-4.5 evidence).
5. Tests and doc examples that need a model string use synthetic IDs with no digit and no `-latest` suffix (for example `claude-opus-fixture`), which the guard does not flag.
6. Baselines record the concrete model that actually ran (observed, FR-5.5).

### S1 — CI guard rewrite: forbid pins, run at ship time (closes G1)

- **FR-1.1** Rewrite `.github/workflows/stale-model-id-guard.yml` so it contains NO ID allowlist, NO literal model ID or version, and NO pattern of its own (it only calls the shared script, FR-1.2). Triggers (F1 fix): `push` to `main`, `pull_request`, and `workflow_dispatch`, with NO `paths:` filter (a filter would hide `.yml`, `.txt` and `.sh` edits). Rationale: the ship path is a direct push to `main` with no PR (BINDING-5.1), so a `pull_request`-only trigger would never run at ship time. Honest limit: the workflow on `push` detects after the push; it cannot block it. The blocking gate at ship time is the local run of the same script (FR-1.5). No `smoke-*.yml` workflow is added (BINDING-4.6).
  - **AC-1.1**: `grep -cEi "claude-[a-z0-9.-]*([0-9]|-latest)" .github/workflows/stale-model-id-guard.yml` MUST print 0 (ran against today's file: 6; expected to fall to 0 after S1; well-formedness only).
  - **AC-1.1b** (triggers, parsed inside the `push:` block, quoted or unquoted `main`, flow or block list; the snippet carries its own negative self-tests, so a checker that ignores the block fails at the first assertion; executed 2026-09-20: prints `OK` on a compliant sample workflow, and on today's file fails with AssertionError "push-to-main, pull_request and workflow_dispatch triggers required"; the self-tests passed in both runs):
    ```bash
    python3 - <<'PY'
    import re
    def triggers_ok(t):
        p = re.search(r'^  push:[ \t]*\n((?:    .*\n|[ \t]*\n)*)', t, re.M)
        body = p.group(1) if p else ''
        q = '[\'"]?'
        flow = re.search(r'branches:\s*\[(?:[^\]]*,)?\s*' + q + r'main' + q + r'\s*(?:,[^\]]*)?\]', body)
        block = re.search(r'^\s+-\s*' + q + r'main' + q + r'\s*$', body, re.M)
        return bool(flow or block) and bool(re.search(r'^  pull_request:', t, re.M)) and bool(re.search(r'^  workflow_dispatch:', t, re.M))
    def wf(*lines): return '\n'.join(('on:',) + lines) + '\n'
    good_block = wf('  push:', '    branches:', "      - 'main'", '  pull_request:', '  workflow_dispatch:')
    good_flow = wf('  push:', "    branches: [release, 'main']", '  pull_request:', '  workflow_dispatch:')
    bad_other_branch = wf('  push:', '    branches: [dev]', '  pull_request:', '    branches:', '      - main', '  workflow_dispatch:')
    bad_no_push = wf('  pull_request:', '    branches:', '      - main', '  workflow_dispatch:')
    assert triggers_ok(good_block) and triggers_ok(good_flow), 'self-test: compliant samples must pass'
    assert not triggers_ok(bad_other_branch) and not triggers_ok(bad_no_push), 'self-test: main listed only under pull_request must fail'
    t = open('.github/workflows/stale-model-id-guard.yml').read()
    assert triggers_ok(t), 'push-to-main, pull_request and workflow_dispatch triggers required'
    assert not re.search(r'^\s+paths(-ignore)?:', t, re.M), 'no paths filter allowed'
    assert 'python3 scripts/check_model_pins.py' in t, 'workflow must run the shared script'
    print('OK')
    PY
    ```
    MUST print `OK`.
- **FR-1.2** Guard contract. ONE definition point for the patterns: a new stdlib-only script `scripts/check_model_pins.py` (same location and style as `scripts/check_skill_budgets.py`) defines five module-level string constants and a `files()` function, and runs its scan only under `if __name__ == "__main__":`, so importing it has no side effect. CLI: no arguments scans the scope below; `--paths <file>...` scans only the named files (same extension, `CHANGELOG.md` and `.delivery/` filters, but a named file outside the repository, such as a temp file, is scanned); `--list` also prints each hit as `category file:line`; `--help` exits 0; the last stdout line before exit is the summary `guard-scope hits <N> files <M>` (same format as the canonical command), and the exit status is 1 when N is above 0. Fixtures live in `scripts/model_pin_fixtures.json` (JSON is outside the scan scope, so fixture strings that ARE pins do not trip the guard). The S1 developer copies these values verbatim:
  - `PIN_RE = "claude-[a-z0-9.-]*([0-9]|-latest)"` (family-agnostic; matches `claude-opus-4-7`, `claude-3-5-sonnet-20241022`, `claude-mythos-5`, `claude-sonnet-latest`, `anthropic.claude-opus-4-7`, and an ID of a family or version that does not exist yet such as `claude-newfamily-7`; matched case-insensitively; a synthetic ID such as `claude-opus-fixture` has no digit and is not matched)
  - `STAMP_RE = 'model_awareness: *"?[a-z-]*[0-9]|pattern_library_version: *"?([0-9v]|[a-z-]*[0-9]+[.-][0-9])'` (any digit in a `model_awareness` value; a `pattern_library_version` must look like `rev-<n>`; case-insensitive; written in the script as a raw string with no single quote inside the value)
  - `PROSE_RE = "(Opus|Sonnet|Haiku|Fable|Mythos|OPUS|SONNET|HAIKU|FABLE|MYTHOS)[ -]*v?[0-9]|(opus|sonnet|haiku|fable|mythos)(-v?[0-9]|v?[0-9]| v?[0-9]+[.][0-9])"` (case-sensitive by design: a lowercase alias followed by a space and a bare integer, as in "run haiku 3 times", is NOT a hit)
  - `BARE_RE = "(^|[^A-Za-z])(on|under|in|for|the|new|so|with|isolates?) v?[4-9][.][0-9]+([^0-9A-Za-z]|$)|[4-9][.-][0-9]+-(only|aware)"` (bare version numbers such as "regression mode on 4.7."; case-insensitive; major 4 to 9 only, so "Section 5.5" and "under 2.5 seconds" pass)
  - `COUNT_RE` (new in Revision 5; QA blocking finding 2; case-sensitive; the FALSE-POSITIVE filter): `"(Opus|Sonnet|Haiku|Fable|Mythos) +[0-9]+ +(times|stories|story|reviewers?|reviews?|agents?|subagents?|passes|rounds?|runs?|instances?|copies|cycles?|iterations?|tasks?|items?|personas?|judges?)([^A-Za-z]|$)|([Oo]n|[Uu]nder|[Ii]n|[Ff]or|[Tt]he|[Nn]ew|[Ss]o|[Ww]ith|[Ii]solates?) v?[0-9]+[.][0-9]+ *(seconds?|secs?|ms|minutes?|mins?|hours?|hrs?|days?|weeks?|months?|years?|times|percent|points?|GB|MB|KB)([^A-Za-z]|$)"`. Rule B blanks every COUNT_RE match (replaces it with one space) BEFORE testing PROSE_RE and BARE_RE. The two alternatives are: a family word plus an integer plus a count noun ("Sonnet 4 stories", "use Opus 2 times for review", "the Opus 3 reviewers", "spawn Opus 3 agents") and a context word plus a decimal plus a time, size or frequency unit ("in 5.0 seconds", "for 4.5 hours", "ship in 4.5 days"). The unit and noun lists deliberately exclude words that can follow a real version ("4.7 tokenizer", "4.7 runtime", "4.7 semantics", "Opus 5 delegates" still hit). This replaces Revision 4's use of the `model-pin-ok` escape for "Haiku 3 times" (QA finding 2: a banned escape meant legitimate sentences could never ship).
  - Wording rule (stated once; the replacement for the removed marker): a sentence that names a count or duration next to a family word or a context word is written so that a COUNT_RE noun or unit directly follows the number ("3 Opus reviewers" is not matched at all; "Opus 3 reviewers" is filtered). A sentence that trips Rule B for any other reason is reworded (name the family only, never a number). Nothing is exempt.
  - Portability: all five run under Python `re` AND POSIX-ERE tools: `PIN_RE`, `STAMP_RE`, `BARE_RE` with `grep -Ei`; `PROSE_RE` with `grep -E`; `COUNT_RE` with `sed -E 's#<COUNT_RE># #g'` (GNU sed; no `#` in the value; the harness in AC-1.2a pipes the sed output into grep). No POSIX bracket classes, no lookaheads, no backreferences, no single quote inside a value. AC-1.2a executes every fixture in both engines.
  - Scope (Architect finding 9): the files reported by `git ls-files --cached --others --exclude-standard` that exist on disk, with extension `*.py *.md *.yml *.yaml *.txt *.sh`, excluding `CHANGELOG.md` and everything under `.delivery/`. So a new untracked file is scanned before `git add`, and the guard, the canonical command in section 1 and the ship gate use the same file set (checked: the simulated script's `--list` equals the canonical listing). JSON is out of scope by design (baselines record the concrete observed model ID).
  - Rule A (pins and stamps): in every scanned file, ANY line matching `PIN_RE` or `STAMP_RE` is a hit. No `#` exemption, no `>` exemption, no heading or code-fence exemption (F3/F4 fix: `# claude-opus-5 setup` and a blockquoted pin were exempt under Revision 3).
  - Rule B (prose): in every scanned `*.md` file (not only SKILL.md: `delivery-team/references/shared/orchestrator-doctrine.md` mirrors the delivery-flow 4.7 block), after COUNT_RE blanking, ANY line matching `PROSE_RE` or `BARE_RE` is a hit.
  - Allowlisted locations (complete list): `CHANGELOG.md` and `.delivery/**`. There is NO per-line escape (FR-1.6).
  - Accepted loopholes (recorded, not closed): string concatenation of an ID; a pin inside a `.json` file; a version written in words; a real version phrased in exactly one of the COUNT_RE forms ("Opus 4 agents" meaning a model) is filtered as a count. COUNT_RE blanks only the matched span, so a line holding both a legitimate duration and a separate real version is still caught (executed: `in 4.5 hours on 4.7 semantics` is a hit, `wait 4.5 seconds` is not); a duration with a decimal directly followed by punctuation ("in 4.5.") is a hit and must be reworded.
  - **AC-1.2a** (contract fixtures, both engines, false negatives AND false positives; executed 2026-09-20 in a scratch directory holding a simulated `scripts/check_model_pins.py` with the five constants and a fixture file of 29, 12, 21 and 16 strings (order: rule A must-hit, rule A must-pass, rule B must-hit, rule B must-pass): `fixture failures 0 []`; mutation checks: replacing PROSE_RE with `.` printed `fixture failures 32 [...]`, and removing the `rule_b_must_pass` key raised KeyError; on today's tree the script does not exist, so the AC fails until S1 lands, which is expected). The fixture file has five keys: `rule_a_must_hit` (>= 25), `rule_a_must_pass` (>= 10), `rule_b_must_hit` (>= 15), `rule_b_must_pass` (>= 12) and `provenance` (an object mapping EVERY fixture string to its origin: `challenger`, `qa-probe`, `repo-line`, `synthetic` or `synthetic-future`; QA warning: fixture provenance). At least 3 must-hit strings are `synthetic-future` (an ID or version that does not exist yet, for example `claude-opus-9`, `claude-newfamily-7`, `Opus 12`), which is the executable form of NFR-11 (a future release needs no guard edit). The REQ table inside the snippet names the strings the fixture file MUST contain (QA blocking finding 1: the AC asserts they are present, so an emptied or trimmed must-pass list cannot pass); the false-positive classes QA probed are all named there (`Sonnet 4 stories`, `use Opus 2 times for review`, `in 5.0 seconds`, `for 4.5 hours`, `ship in 4.5 days`):
    ```bash
    python3 - <<'PY'
    import importlib.util, json, re, subprocess
    spec = importlib.util.spec_from_file_location('cmp', 'scripts/check_model_pins.py')
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    F = json.load(open('scripts/model_pin_fixtures.json'))
    REQ = {
        'rule_a_must_hit': ['claude-3-5-sonnet-20241022', 'claude-3-opus-20240229', 'claude-sonnet-latest', 'CLAUDE-OPUS-4-7', 'claude-mythos-5',
                            'model_awareness: "opus-5"', 'pattern_library_version: 4.7.1', '# claude-opus-5 setup', '> claude-opus-4-7 was retired'],
        'rule_a_must_pass': ['model = "claude-opus-fixture"', 'pattern_library_version: rev-1'],
        'rule_b_must_hit': ['Opus5', 'OPUS 5', 'Opus v5', 'Opus  5', 'Fable 5', 'regression mode on 4.7.'],
        'rule_b_must_pass': ['run haiku 3 times', 'the latest Opus dispatches', 'Section 5.5', 'Replace C12 with 4.7uF or greater',
                             'Step 4.5: Delegation Self-Check', 'Sonnet 4 stories', 'use Opus 2 times for review', 'in 5.0 seconds',
                             'for 4.5 hours', 'ship in 4.5 days', 'under 2.5 seconds'],
    }
    MIN = {'rule_a_must_hit': 25, 'rule_a_must_pass': 10, 'rule_b_must_hit': 15, 'rule_b_must_pass': 12}
    def a_py(l): return bool(re.search(m.PIN_RE, l, re.I) or re.search(m.STAMP_RE, l, re.I))
    def b_py(l): return bool(re.search(m.PROSE_RE, re.sub(m.COUNT_RE, ' ', l)) or re.search(m.BARE_RE, re.sub(m.COUNT_RE, ' ', l), re.I))
    def g(p, l, ci, pre=None):
        if pre:
            l = subprocess.run(['sed', '-E', 's#' + pre + '# #g'], input=l + '\n', text=True, capture_output=True).stdout
        return subprocess.run(['grep', '-E' + ('i' if ci else ''), '-q', '--', p], input=l, text=True).returncode == 0
    def a_gr(l): return g(m.PIN_RE, l + '\n', True) or g(m.STAMP_RE, l + '\n', True)
    def b_gr(l): return g(m.PROSE_RE, l, False, m.COUNT_RE) or g(m.BARE_RE, l, True, m.COUNT_RE)
    bad = []
    for eng, fa, fb in (('python-re', a_py, b_py), ('grep-E', a_gr, b_gr)):
        for key, f, want in (('rule_a_must_hit', fa, True), ('rule_a_must_pass', fa, False), ('rule_b_must_hit', fb, True), ('rule_b_must_pass', fb, False)):
            for x in F[key]:
                if f(x) != want:
                    bad.append((eng, key, x))
    for key, n in MIN.items():
        assert len(F[key]) >= n, 'fixture list too small: ' + key
    for key, need in REQ.items():
        miss = [x for x in need if x not in F[key]]
        assert not miss, 'required fixture strings missing from ' + key + ': ' + repr(miss)
    assert all(F['provenance'].get(x) in ('challenger', 'qa-probe', 'repo-line', 'synthetic', 'synthetic-future') for k in MIN for x in F[k]), 'every fixture string needs a provenance origin'
    assert sum(1 for k in ('rule_a_must_hit', 'rule_b_must_hit') for x in F[k] if F['provenance'][x] == 'synthetic-future') >= 3, 'need >= 3 synthetic-future must-hit strings (NFR-11)'
    for p in (m.PIN_RE, m.STAMP_RE, m.PROSE_RE, m.BARE_RE, m.COUNT_RE):
        assert "'" not in p and '(?' not in p and '[:' not in p and '#' not in p, 'non-portable construct: ' + p
    print('fixture failures', len(bad), bad)
    PY
    ```
    MUST print `fixture failures 0 []`.
  - **AC-1.2b** (guard is a scan job run by the shared script): `grep -c "check_model_pins.py" .github/workflows/stale-model-id-guard.yml` MUST be >= 1, and `python3 scripts/check_model_pins.py --help >/dev/null; echo "exit=$?"` MUST print `exit=0`.
  - **AC-1.2c** (no hits on the migrated tree, including the script and the workflow themselves): `python3 scripts/check_model_pins.py; echo "exit=$?"` MUST print `guard-scope hits 0 files 0` then `exit=0`. The script's summary line has the same format as the canonical command in section 1 and it exits 1 on any hit; before S4 it prints a hit count above 0 (expected). Today the script does not exist, and the canonical command prints `guard-scope hits 91 files 31` (the simulated script printed the same).
- **FR-1.3** Guard is a static scan job; no `claude` CLI in any workflow (BINDING-5.2, BINDING-4.6).
  - **AC-1.3**: `grep -rEl '(^|[^a-z-])claude[[:space:]]+(-p|--print|--model)' .github/workflows | wc -l` MUST print 0 and `ls .github/workflows | grep -c '^smoke-'` MUST print 0 (ran 2026-09-20: 0 and 0).
- **FR-1.4** Guard edits route through `plugin-dev:hook-development` (CLAUDE.md workflow-edit rule) and keep `workflow-injection-lint.yml` green (no `${{ github.event.* }}` inside `run:`). Verification: inspection; S1 report contains the line `plugin-dev:hook-development loaded`.
- **FR-1.5** Local gates (F1 fix; Architect finding 2). `python3 scripts/check_model_pins.py` is (a) called by the workflow; (b) called from the opt-in `.githooks/pre-commit` in STAGED-FILE mode: `python3 scripts/check_model_pins.py --paths <staged files>` (warn-and-skip if `python3` or the script is missing, same as the existing checks). The hook is ADVISORY by default (prints the hits and exits 0) and blocks only when `MODEL_PIN_STRICT=1` is set. Reason: from S1 until S4 the tree still holds 91 hits, and any commit that touches a still-unmigrated file would otherwise be blocked (S1 to S3 WIP commits); the ship gate below is strict and does not depend on the hook; (c) a mandatory STRICT step of the ship procedure (FR-7.3): the S7 report records its output and `exit=0` before the push, run AFTER staging so new files are in scope (they are in scope anyway: the scope includes untracked files).
  - **AC-1.5**: `grep -c "check_model_pins.py --paths" .githooks/pre-commit` MUST be >= 1 and `grep -c "MODEL_PIN_STRICT" .githooks/pre-commit` MUST be >= 1 (today: 0 and 0); the ship step is Verification: inspection of the S7 report line `check_model_pins.py exit=0`.
- **FR-1.6** No bypass exists (Revision 5; Architect finding 8, QA finding 2, QA warning: negative test). The Revision 4 `model-pin-ok` per-line marker is REMOVED: it was allowlisted in the script yet banned at ship, so it was unusable and asymmetric (CI could not enforce the ban). Legitimate future hits are reworded (wording rule in FR-1.2). The string `model-pin-ok` is not honoured anywhere and does not appear in the shipped tree.
  - **AC-1.6a**: `grep -rIl "model-pin-ok" --exclude-dir=.git --exclude-dir=.delivery --exclude-dir=worktrees . | wc -l` MUST print 0 (executed 2026-09-20: 0).
  - **AC-1.6b** (negative test: the guard still fails a pin that carries the old marker text; executed 2026-09-20 against the simulated script: `1 guard-scope hits 1 files 1`):
    ```bash
    python3 - <<'PY'
    import os, subprocess, tempfile
    p = os.path.join(tempfile.mkdtemp(), 'bypass-attempt.md')
    open(p, 'w').write('claude-opus-4-7 model-pin-ok\n')
    r = subprocess.run(['python3', 'scripts/check_model_pins.py', '--paths', p], capture_output=True, text=True)
    print(r.returncode, r.stdout.strip().splitlines()[-1])
    PY
    ```
    MUST print `1 guard-scope hits 1 files 1`.

### S2 — Keystone prose (closes G7; precondition for G3)

Floor checks versus intent gates (F6): several ACs below are floor checks that a trivial edit could satisfy literally. They are paired with intent gates that a trivial edit cannot satisfy: a source-line-removal check (AC-2.1), a content check (AC-2.5) and an independent adversarial re-fetch and review (AC-2.3b, AC-DISP manifest). A story passes only when both the floor and the intent gate pass.

- **FR-2.1** Full prose review of 3 keystones in order: `delivery-team/skills/delivery-flow/SKILL.md`, `prompt-engineer/SKILL.md`, `delivery-team/skills/product-delivery/SKILL.md`, plus the shared mirror `delivery-team/references/shared/orchestrator-doctrine.md` (same 4.7 block as delivery-flow 27 to 30; it is reviewed in the delivery-flow dispatch so the two stay consistent). Rewrite version-specific blocks to family-relative guidance per the convention. Named source lines (main, before edit): delivery-flow 27, 28, 30, 273, 276; prompt-engineer 88, 347, 349, 351, 356, 359, 361, 363, 365, 368, 371, 373, 375, 397, 401, 408, 420; orchestrator-doctrine 77, 79, 82. Lines 363 (heading "Versioned Model Reference"), 365 and 371 (both tell authors to hardcode a model ID with a `# canonical <date>` comment) and 420 (stamp-doc bullet) match no regex but contradict conventions 3 and 4 (QA W4-1); Pattern 4.1 becomes a config-read pattern and the stamp-doc block describes the version-free stamp. Delivery-flow line 27 and 28 also carry the claim that the runtime "dispatches fewer sub-agents by default", which the docs reverse (section 8, REFUTED); the rewrite states the doc-verified direction.
  - **AC-2.1** (intent gate: the named source lines are actually gone; evaluated PRE-SHIP only, because it reads `main:` via `git show` (Architect suggestion 10); QA warning fixed: it counts occurrences (a `Counter`), so a named line that legitimately appears twice in a file is "gone" only when one occurrence was removed, and an untouched duplicate is not falsely reported; ran 2026-09-20 on the unedited tree: prints `25 source lines still present`):
    ```bash
    python3 - <<'PY'
    import subprocess
    from collections import Counter
    S = {'delivery-team/skills/delivery-flow/SKILL.md': [27, 28, 30, 273, 276],
         'prompt-engineer/SKILL.md': [88, 347, 349, 351, 356, 359, 361, 363, 365, 368, 371, 373, 375, 397, 401, 408, 420],
         'delivery-team/references/shared/orchestrator-doctrine.md': [77, 79, 82]}
    left = 0
    for f, nums in S.items():
        old = subprocess.run(['git', 'show', 'main:' + f], capture_output=True, text=True).stdout.splitlines()
        was = Counter(l.strip() for l in old)
        now = Counter(l.strip() for l in open(f))
        for n in nums:
            t = old[n - 1].strip()
            if t and now[t] >= was[t]:
                left += 1
    print(left, 'source lines still present')
    PY
    ```
    MUST print `0 source lines still present`.
    Also: the S2 dispatch manifest lists one reviewer dispatch per keystone (Verification: inspection), and `python3 scripts/check_model_pins.py --paths <the 4 files>` MUST print `guard-scope hits 0 files 0` for those files (the script accepts `--paths`, FR-1.2).
- **FR-2.2** `prompt-engineer/SKILL.md:368` `MODEL_ID` snippet becomes a read of one configuration value with no ID literal, for example `MODEL_ID = os.environ["CLAUDE_MODEL_ID"]  # one config value; set from the models overview, never hard-coded in code`. Rationale: the Claude API has no "latest" alias for current models (section 8), so an alias such as `opus` would not work there; the honest form is one config point.
  - **AC-2.2**: `grep -c 'MODEL_ID = os.environ' prompt-engineer/SKILL.md` MUST print 1; `grep -cEi "claude-[a-z0-9.-]*([0-9]|-latest)" prompt-engineer/SKILL.md` MUST print 0; `grep -c "canonical <YYYY" prompt-engineer/SKILL.md` MUST print 0; `grep -c "Versioned Model Reference" prompt-engineer/SKILL.md` MUST print 0.
- **FR-2.3** Prose model-behaviour guidance uses only doc-verified behaviour, written without version numbers. Anchors verified for the current latest Opus (section 8): it "delegates to subagents more readily than prior models" (so give explicit delegation scope and a spawn cap); explicit re-verification instructions "cause over-verification" (drop them). Effort guidance must not restate a per-version default or recommended level (levels are recalibrated between releases, section 8); it says: start from the API default effort and tune on your own evals. The prompt-engineer "Model-specific optimisation" block is retitled to a family heading (for example `Model-specific optimisation: latest Opus`), keeping the file's own convention that per-model guidance lives in one named sub-section. No provisional text (BINDING-3.3). Caveat recorded for readers of any pinned-ID guidance (section 8): serving infrastructure around a fixed model ID can change over time, so behaviour under a fixed ID is not a permanent guarantee either.
  - **AC-2.3** (scoped hedge scan; research-agent rubric prose excluded because it legitimately says "unverified"; self-contained; executed 2026-09-20: `0`):
    ```bash
    python3 - <<'PY'
    import os, re, subprocess
    def files(exts=None, name=None):
        for f in sorted(set(subprocess.run(['git', 'ls-files', '--cached', '--others', '--exclude-standard'], capture_output=True, text=True, check=True).stdout.split('\n'))):
            if f and not f.startswith('.delivery/') and os.path.isfile(f) and (not name or os.path.basename(f) == name) and (not exts or f.endswith(exts)):
                yield './' + f
    pat = re.compile(r"pending doc verification|do not treat as binding|Architect to confirm", re.I)
    print(len([f for f in files(name='SKILL.md') if 'research-agent' not in f and pat.search(open(f).read())]))
    PY
    ```
    MUST print `0`.
  - **AC-2.3b** (independent re-fetch plus intent verdict; the adversarial reviewer's artifact is `.delivery/artifacts/*/dod/*adversarial*`; the reviewer WebFetches >= 3 rows from section 8 and records each URL and quote (BINDING-3.2), and also records one line `AC-2.1/2.5 intent verdict: PASS` or `FAIL` stating whether the delegation-scope and spawn-cap rewrite is real prose and not a keyword-satisfying edit, which closes the QA warning that AC-2.1 and AC-2.5 are floor-only). Runnable form (executed today: prints `0` and `0`, no adversarial artifact exists yet):
    ```bash
    cat .delivery/artifacts/*/dod/*adversarial* 2>/dev/null | grep -oE "https://[^ )>\"]+" | sort -u | wc -l
    ```
    MUST print a number >= 3.
    ```bash
    cat .delivery/artifacts/*/dod/*adversarial* 2>/dev/null | grep -cE "^AC-2\.1/2\.5 intent verdict: (PASS|FAIL)"
    ```
    MUST print >= 1, and the verdict MUST be PASS for S2 to close (Verification: inspection of that line).
- **FR-2.4** Each SKILL.md edit routes through `plugin-dev:skill-development`, acknowledged before edit (CLAUDE.md). Verification: each developer dispatch report contains `plugin-dev:skill-development loaded`.
- **FR-2.5** The `delivery-flow` keystone dispatch section states an explicit delegation-scope rule and spawn cap, phrased conditionally for "the latest Opus" (FR-2.3 content, made testable) and true for any model: the dispatch count never exceeds the length of `dod_validators.<stage>`.
  - **AC-2.5** (content gate; still a floor, QA warning: the per-line rule below defeats keyword salad, semantic correctness is judged by the adversarial reviewer through the AC-2.3b intent verdict; evaluated PRE-SHIP only, because it diffs against `main`, Architect suggestion 10; executed 2026-09-20 on the unedited tree: prints `FAIL`, 0 added lines): the snippet reads the added lines of `git diff -U0 main -- delivery-team/skills/delivery-flow/SKILL.md`. One added line must carry the conditional "when or if ... latest Opus" phrasing, and ONE (possibly other) added line must contain `dod_validators`, a cap word and the word subagent together, so the cap and its bound sit in one sentence:
    ```bash
    python3 - <<'PY'
    import subprocess, re
    d = subprocess.run(['git', 'diff', '-U0', 'main', '--', 'delivery-team/skills/delivery-flow/SKILL.md'], capture_output=True, text=True).stdout
    added = [l[1:] for l in d.splitlines() if l.startswith('+') and not l.startswith('+++')]
    cond = any(re.search(r'(?i)\b(when|if)\b[^\n]{0,80}latest opus', l) for l in added)
    cap = any('dod_validators' in l and re.search(r'(?i)\b(cap|at most|no more than)\b', l) and re.search(r'(?i)sub-?agent', l) for l in added)
    ok = cond and cap and not any(l.lstrip().startswith('<!--') for l in added)
    print('OK' if ok else 'FAIL')
    PY
    ```
    MUST print `OK`.
- **FR-2.6** Tier consistency of the keystone (F7). `delivery-flow/SKILL.md` frontmatter says `model: sonnet` while FR-2.5 writes guidance about "the latest Opus". PO decision (recorded, not re-debated by later stages unless OQ-11 changes it): the frontmatter `model:` value is NOT changed by this initiative (re-tiering the orchestrator is a cost and behaviour decision nobody has made); the guidance is conditional ("when the orchestrating session runs the latest Opus ...") and the spawn cap holds for every model. The Architect confirms or overrides at Stage 4 (OQ-11).
  - **AC-2.6**: `grep -c "^model: sonnet" delivery-team/skills/delivery-flow/SKILL.md` MUST print 1 (unchanged), unless OQ-11 records a different decision; the conditional phrasing is enforced by AC-2.5.

### S3 — Full prose sweep and version-free stamps (closes G2, G3, G6)

- **FR-3.1** Full prose review of all 34 SKILL.md, keystones plus 31 others (BINDING-2.2 retained; see OQ-9, still OPEN for the user). Lens: the model behaviours documented as of the sweep date (section 8) and the scheme convention; version mentions removed. Revision 4 change (F6): Revision 3 required a body change in all 34 files, which a reviewer could satisfy with a one-character edit and which forced pointless edits on the 9 unstamped files. The evidence of review is now a ledger, and a file with nothing to fix says so explicitly.
  - **AC-3.1** (review ledger; the intent gate is that every SKILL.md has a named reviewer verdict, every CHANGED row has a real diff, every NO_CHANGE_NEEDED row carries a reason of at least 20 characters, and the adversarial reviewer spot-checks 5 CHANGED diffs and 5 NO_CHANGE_NEEDED rows; the spot-check is Verification: inspection of the adversarial artifact). The ledger is `.delivery/artifacts/06-development/prose-review-ledger.tsv` with header `path<TAB>agent_id<TAB>verdict<TAB>note`. Executed 2026-09-20 against the current tree: fails with FileNotFoundError because the ledger does not exist yet (expected):
    ```bash
    python3 - <<'PY'
    import csv, os, subprocess
    def files(exts=None, name=None):
        for f in sorted(set(subprocess.run(['git', 'ls-files', '--cached', '--others', '--exclude-standard'], capture_output=True, text=True, check=True).stdout.split('\n'))):
            if f and not f.startswith('.delivery/') and os.path.isfile(f) and (not name or os.path.basename(f) == name) and (not exts or f.endswith(exts)):
                yield './' + f
    rows = list(csv.reader(open('.delivery/artifacts/06-development/prose-review-ledger.tsv'), delimiter='\t'))
    assert rows[0] == ['path', 'agent_id', 'verdict', 'note'], 'header must be: path, agent_id, verdict, note'
    rows = rows[1:]
    want = {os.path.normpath(f) for f in files(name='SKILL.md')}
    got = {os.path.normpath(r[0]) for r in rows}
    bad = [r[0] for r in rows
           if r[2] not in ('CHANGED', 'NO_CHANGE_NEEDED') or not r[1].strip()
           or (r[2] == 'NO_CHANGE_NEEDED' and len(r[3].strip()) < 20)
           or (r[2] == 'CHANGED' and subprocess.run(['git', 'diff', '--quiet', 'main', '--', r[0]]).returncode == 0)]
    print(len(rows), 'missing', len(want - got), 'extra', len(got - want), 'bad', len(bad))
    PY
    ```
    MUST print `34 missing 0 extra 0 bad 0`.
  - **AC-3.1b** (no leftover version markers in any SKILL.md; reads the hit list from the guard script's `--list` output, so it uses the real patterns including COUNT_RE blanking; today the script does not exist; executed against the simulated script on 2026-09-20: prints `69 19`, i.e. 16 prose lines plus 1 pin line at `prompt-engineer/SKILL.md:368` plus 52 stamp lines, and 19 SKILL.md files still carrying the `frontmatter-only` marker, which is a subset of the stamp lines and MUST also reach 0):
    ```bash
    python3 - <<'PY'
    import subprocess
    out = subprocess.run(['python3', 'scripts/check_model_pins.py', '--list'], capture_output=True, text=True).stdout
    n = sum(1 for l in out.splitlines() if l.split(' ', 1)[-1].rsplit(':', 1)[0].endswith('SKILL.md'))
    fo = subprocess.run(['grep', '-rl', 'frontmatter-only', '--include=SKILL.md', '--exclude-dir=.git', '--exclude-dir=.delivery', '--exclude-dir=worktrees', '.'], capture_output=True, text=True).stdout.split()
    print(n, len(fo))
    PY
    ```
    MUST print `0 0`.
- **FR-3.2** Stamps become version-free, in the 25 files that carry them; the 9 unstamped files get NO new stamp (a "latest" stamp with no audit date certifies nothing, and adding 9 stamps is an edit with no purpose under the new scheme). The existing header-warning workflow `.github/workflows/skill-md-header-warn.yml` (presence-only `grep -L 'model_awareness:'`, `continue-on-error: true`; the only script or workflow that reads a stamp, verified) keeps warning on those 9 files; that is accepted and non-blocking. Census-consequence: the 26 stamp lines and the 26 `pattern_library_version` lines all need edits (they encode 4.7 today); the other 9 files need prose review only. The `prompt-engineer` documentation example (lines 415 to 417) is one of the 26 and becomes `latest` / `rev-1` too.
  - **AC-3.2** (the stamp census after S3, self-contained; ran 2026-09-20: prints `34 26 25 {...opus-4-7...}` then `26 {'pattern_library_version: 4-7-1': 26}`):
    ```bash
    python3 - <<'PY'
    import os, subprocess
    from collections import Counter
    def files(exts=None, name=None):
        for f in sorted(set(subprocess.run(['git', 'ls-files', '--cached', '--others', '--exclude-standard'], capture_output=True, text=True, check=True).stdout.split('\n'))):
            if f and not f.startswith('.delivery/') and os.path.isfile(f) and (not name or os.path.basename(f) == name) and (not exts or f.endswith(exts)):
                yield './' + f
    sk = list(files(name='SKILL.md'))
    L = [(f, l.rstrip()) for f in sk for l in open(f) if l.lstrip().startswith('model_awareness:')]
    print(len(sk), len(L), len({f for f, _ in L}), dict(Counter(l for _, l in L)))
    P = [l.rstrip() for f in sk for l in open(f) if l.startswith('pattern_library_version:')]
    print(len(P), dict(Counter(P)))
    PY
    ```
    MUST print `34 26 25 {'model_awareness: latest': 26}` then `26 {'pattern_library_version: rev-1': 26}`.
- **FR-3.3** Stamps, `last_audited` and `fitness_review_due` are applied AFTER prose passes reach DoD (BINDING-2.3). `last_audited` in each of the 25 stamped files is set to the date of the S3 DoD pass. `fitness_review_due:` (present in 11 SKILL.md, all `2026-08-09`, already past on 2026-09-20; F8) is reset on each of those files to a future date per `governance/fitness-review.md`, because R7 relies on the quarterly fitness review as the trigger for re-verifying version-free guidance.
  - **AC-3.3a** (frontmatter only; the documentation example inside the prompt-engineer code fence is out of scope of this check; QA warning fixed: `fitness_review_due` must be STRICTLY after today and within the governance interval of 90 days (`governance/fitness-review.md`: "advance `fitness_review_due:` by 90 days"), so today's date no longer passes; `last_audited` must be between the PRD date and today; the dates are computed from `datetime.date.today()`; ran 2026-09-20 on the unedited tree: prints `36 violations`, which is 25 `last_audited` plus 11 `fitness_review_due`):
    ```bash
    python3 - <<'PY'
    import datetime, os, re, subprocess
    def files(exts=None, name=None):
        for f in sorted(set(subprocess.run(['git', 'ls-files', '--cached', '--others', '--exclude-standard'], capture_output=True, text=True, check=True).stdout.split('\n'))):
            if f and not f.startswith('.delivery/') and os.path.isfile(f) and (not name or os.path.basename(f) == name) and (not exts or f.endswith(exts)):
                yield './' + f
    today = datetime.date.today().isoformat()
    latest_due = (datetime.date.today() + datetime.timedelta(days=90)).isoformat()
    bad = []
    for f in files(name='SKILL.md'):
        m = re.match(r'---\n(.*?)\n---', open(f).read(), re.S)
        if not m:
            continue
        a = re.search(r'^last_audited:\s*(\S+)\s*$', m.group(1), re.M)
        d = re.search(r'^fitness_review_due:\s*(\S+)\s*$', m.group(1), re.M)
        if a and not (re.fullmatch(r'\d{4}-\d{2}-\d{2}', a.group(1)) and '2026-09-20' <= a.group(1) <= today):
            bad.append((f, 'last_audited', a.group(1)))
        if d and not (re.fullmatch(r'\d{4}-\d{2}-\d{2}', d.group(1)) and today < d.group(1) <= latest_due):
            bad.append((f, 'fitness_review_due', d.group(1)))
    print(len(bad), 'violations')
    PY
    ```
    MUST print `0 violations`.
  - **AC-3.3b**: `grep -c "model_awareness:" prompt-engineer/SKILL.md` MUST print 2 (frontmatter plus the documentation example at 415, both `model_awareness: latest`).
  - **AC-3.3c** (ordering evidence): Verification: inspection of the Stage 6 developer-dispatch report showing prose DoD PASS before the stamp step.
- **G6 line budgets**: **AC-6** `python3 scripts/check_skill_budgets.py; echo "exit=$?"` MUST print `exit=0` (ran 2026-09-20: `BUDGET CHECK PASSED: 17 file(s) checked, 0 known-debt, 0 exception(s).` then `exit=0`). S3 owns the gate as the last SKILL.md editor.

### S4 — Code IDs and literal sweep (closes G4, G-LIT)

- **FR-4.1** ONE central definition point for tier labels. `agentic-flow-builder/scripts/agent_registry.py` gains a single top-level dict `MODEL_TIER_ALIAS = {"heavy": "opus", "mid": "sonnet", "light": "haiku"}` and the three registry entries use `"config": {"model": MODEL_TIER_ALIAS["heavy"]}` (mid, light likewise), replacing lines 190, 149, 174. The values are Claude Code CLI aliases (verified, section 8). The three existing comment lines 148, 173, 189 (`# canonical 2026-04-22 — opus-4-7 migration; prior: claude-...`) are pin lines under the Revision 4 guard (no `#` exemption) and would describe a value that no longer exists (QA W4-5); they are replaced by `# tier alias resolved via MODEL_TIER_ALIAS; earlier versioned IDs are recorded in CHANGELOG.md`. Provenance moves to CHANGELOG, where IDs are allowed.
  - **AC-4.1**: (also `python3 -m py_compile agentic-flow-builder/scripts/agent_registry.py` MUST exit 0 and `grep -c "opus-4-7" agentic-flow-builder/scripts/agent_registry.py` MUST print 0)
    ```bash
    python3 - <<'PY'
    import ast, re
    p = 'agentic-flow-builder/scripts/agent_registry.py'
    src = open(p).read()
    tree = ast.parse(src)
    d = [n for n in tree.body if isinstance(n, ast.Assign) and getattr(n.targets[0], 'id', None) == 'MODEL_TIER_ALIAS']
    assert len(d) == 1, 'need exactly one MODEL_TIER_ALIAS definition'
    v = ast.literal_eval(d[0].value)
    assert v == {'heavy': 'opus', 'mid': 'sonnet', 'light': 'haiku'}, v
    assert len(re.findall(r'"model": MODEL_TIER_ALIAS\[', src)) == 3
    assert not re.search(r'"model": "claude-', src)
    print('OK')
    PY
    # MUST print OK
    ```
- **FR-4.2** `conftest.py` 4 fixture strings (105, 117, 129, 151) become synthetic IDs with no digit and no `-latest` suffix (for example `claude-opus-fixture`).
  - **AC-4.2** (F6 fix: counts the four `"model"` string VALUES, not any mention, so a comment cannot satisfy it; Developer findings fixed: two separate commands, no inline comment, non-capturing group). Executed 2026-09-20 on the unedited tree: prints `False 4`.
    ```bash
    python3 - <<'PY'
    import re
    src = open('delivery-team/tests/smoke/tests/conftest.py').read()
    vals = re.findall(r'"model":\s*"claude-opus-fixture"', src)
    pins = re.findall(r'claude-[a-z0-9.-]*(?:[0-9]|-latest)', src, re.I)
    print(len(vals) >= 4, len(pins))
    PY
    ```
    MUST print `True 0`. Then, as its own command, the existing meta-tests must still pass with the synthetic IDs (executed today: `3 passed`):
    ```bash
    python3 -m pytest delivery-team/tests/smoke/tests/test_meta.py -q; echo "exit=$?"
    ```
    MUST print `exit=0`.
- **FR-4.3** `smoke-test-architecture.md` lines 115 AND 116 (`claude-opus-4-7` and `claude-sonnet-4-5`) and `telemetry-schema.md:36` (`claude-sonnet-4-6`) become synthetic IDs. This resolves QA D3-1 (sonnet-4-5 at line 116) by moving BOTH lines of the code fence, and it is no longer a one-off: the version-agnostic `PIN_RE` catches any versioned ID, so no ID can hide.
  - **AC-4.3**: `grep -cEi "claude-[a-z0-9.-]*([0-9]|-latest)" delivery-team/architecture/smoke-test-architecture.md delivery-team/references/telemetry-schema.md` MUST print 0 for both files (today: 2 and 1).
- **FR-4.4** Producer-validator separation is OBSERVABLE, not self-reported (BINDING-4.5; QA blocking finding 3). The producers are the authors of `delivery-team/tests/smoke/lib/` (`metrics.py`, `baseline.py`, `runner.py`, `report.py`, `run_smoke.py` changes; FR-5.9 and the S5 file list). The validator is a SEPARATE Agent dispatch that authors `tests/test_model_capture.py` and `tests/fixtures/` (the S5 meta-tests live in a new file, so the existing `test_meta.py` contract of exactly 3 test functions, AC-S3-08 in its docstring, stays true). Five independent observations, all required:
  1. Separate commits: no commit on the branch touches both `lib/` and the validator files.
  2. Authorship evidence: every commit message carries a trailer `Dispatch-Id: <agent-id>`; the `Dispatch-Id` sets of the `lib/` commits and of the validator commits are non-empty and DISJOINT (a producer cannot author the tests under a second label without a second dispatch, which the manifest, FR-7.4, also shows).
  3. `lib/` unchanged for the whole validator dispatch: the dispatch records `validator_start: <sha>` and `validator_end: <sha>` in `.delivery/artifacts/06-development/s5-separation.txt`; `git diff --name-only <start>..<end> -- delivery-team/tests/smoke/lib` MUST be empty (start AND end, not start only), and `git status --porcelain` for `lib/` is empty at the end.
  4. Red first: the validator's `real_shape` test MUST FAIL against the unfixed parser before the fix lands (AC-5.9b), which proves the test exercises the defect and was not written to fit the fix.
  5. The dispatch manifest lists distinct agent IDs (FR-7.4).
  - **AC-4.4** (observations 1 to 3; checked PRE-SHIP because the trailers and commits are squashed away by the ship; today it fails at the first assertion because no S5 commits exist, which is expected; executed 2026-09-20: `AssertionError: producer and validator must each have commits on the branch`):
    ```bash
    python3 - <<'PY'
    import subprocess
    def sh(*a): return subprocess.run(a, capture_output=True, text=True).stdout
    LIB = 'delivery-team/tests/smoke/lib'
    TESTS = ['delivery-team/tests/smoke/tests/test_model_capture.py', 'delivery-team/tests/smoke/tests/fixtures']
    def commits(paths): return set(sh('git', 'log', 'main..HEAD', '--format=%H', '--', *paths).split())
    def dispatch_ids(hs):
        return {l.split(':', 1)[1].strip() for h in hs for l in sh('git', 'show', '-s', '--format=%B', h).splitlines() if l.startswith('Dispatch-Id:')}
    lib_c, test_c = commits([LIB]), commits(TESTS)
    assert lib_c and test_c, 'producer and validator must each have commits on the branch'
    assert not (lib_c & test_c), 'no commit may touch both lib/ and the validator files'
    li, ti = dispatch_ids(lib_c), dispatch_ids(test_c)
    assert li and ti and not (li & ti), 'Dispatch-Id trailers must exist and differ between producer and validator commits'
    rec = dict(l.split(': ', 1) for l in open('.delivery/artifacts/06-development/s5-separation.txt').read().splitlines() if ': ' in l)
    assert sh('git', 'diff', '--name-only', rec['validator_start'] + '..' + rec['validator_end'], '--', LIB).strip() == '', 'lib/ changed during the validator dispatch'
    assert sh('git', 'status', '--porcelain', LIB).strip() == '', 'lib/ has uncommitted changes at validator end'
    print('OK')
    PY
    ```
    MUST print `OK`. Observation 4 is AC-5.9b; observation 5 is AC-DISP.
- **FR-4.5** Evidence that no repo code sends `config.model` to the Claude API, recorded by the S4 developer (run 2026-09-20, results: `grep -rln "import anthropic\|from anthropic\|api.anthropic.com" --include=*.py .` returned no file; in `agentic-flow-builder/scripts/` `config` is only persisted via `json.loads(agent['config'])`/`agent_def["config"]`). If the developer finds a real API call site, story stops and raises a defect; that call reads one config value (convention 4). Latent trap named (QA W4-2): `agentic-flow-builder/scripts/flow_orchestrator.py:663` reads `# In production: call Claude API with agent.config['model']`; after FR-4.1 `config.model` holds a CLI tier alias (`opus`), which the API does not accept (section 8). The S4 developer rewords that comment to say the API call reads one configured model ID (convention 4) and that `config.model` is a CLI tier alias.
  - **AC-4.5** (Developer finding 4 fixed: the glob is quoted and `.git`, `.delivery` and every `worktrees` directory are pruned BEFORE grep descends, so nested worktrees and `.delivery` are never walked): `grep -rlE "import anthropic|from anthropic|api.anthropic.com" --include='*.py' --exclude-dir=.git --exclude-dir=.delivery --exclude-dir=worktrees . | wc -l` MUST print 0 (ran 2026-09-20: 0).
  - **AC-4.5b**: `grep -c "agent.config\['model'\]" agentic-flow-builder/scripts/flow_orchestrator.py` MUST print 0 (today: 1) and `grep -c "CLI tier alias" agentic-flow-builder/scripts/flow_orchestrator.py` MUST be >= 1.
- **FR-4.6** Frontmatter tier-alias vocabulary (F7). The 9 `model:` / `phase_1_detector_model:` lines in SKILL.md (section 1 census) are tier aliases that cannot import the Python dict. They are additional, deliberate places where the same vocabulary is written; the guard cannot enforce a single location for them, so the vocabulary is pinned instead.
  - **AC-4.6** (self-contained; ran 2026-09-20: prints `9 ['haiku', 'opus', 'sonnet'] violations 0`; MUST keep printing `violations 0`):
    ```bash
    python3 - <<'PY'
    import os, re, subprocess
    def files(exts=None, name=None):
        for f in sorted(set(subprocess.run(['git', 'ls-files', '--cached', '--others', '--exclude-standard'], capture_output=True, text=True, check=True).stdout.split('\n'))):
            if f and not f.startswith('.delivery/') and os.path.isfile(f) and (not name or os.path.basename(f) == name) and (not exts or f.endswith(exts)):
                yield './' + f
    vals = []
    for f in files(name='SKILL.md'):
        for l in open(f):
            m = re.match(r'(model|phase_1_detector_model):\s*(\S+)\s*$', l)
            if m:
                vals.append(m.group(2))
    bad = [v for v in vals if v not in ('opus', 'sonnet', 'haiku')]
    print(len(vals), sorted(set(vals)), 'violations', len(bad))
    PY
    ```
- **AC-1b (repo-wide literal sweep; closes G-LIT)**: run the canonical counting command from section 1. After S1, S2, S3 and S4 it MUST print exactly `guard-scope hits 0 files 0` (line 1) and `  pin 0 stamp 0 prose 0` (line 2), with no listing lines. Before migration it prints `guard-scope hits 91 files 31` (recorded above). Story order is S1 to S4, so S2 (prose) and S3 (stamps and remaining prose) have landed when S4 closes the gate; the closing run is repeated at ship (FR-7.3).

### S5 — Smoke harness (closes G5)

Source-of-truth check (run 2026-09-20): `run_smoke.py` has NO `--effort` flag and `lib/runner.py:120` builds `["claude", "--print", "--output-format", "stream-json", "--verbose"]` with NO `--model` argument today; the baseline JSON keys are `_header_comment, schema_version, scenario, sample_status, n_samples, last_captured_utc, last_captured_git_sha, last_captured_cli_version, metrics, deferred_reason` (no `model`); its `metrics.cost_usd.mean` is `0.0` and its header comment says "cost_usd=0.00 (no usage events emitted".

**Revision 4 correction (F5; executed evidence).** Revision 3 claimed that `metrics.py:117` "already buckets `model_usage` by the `model` string of each stream event, so observed models are recorded per dispatch". That claim was made from the code and a hand-written fixture. It does not hold against a real stream. The PO captured one real stream on 2026-09-20 (CLI 2.1.278, `claude -p "reply with the single word ok" --model haiku --output-format stream-json --verbose --max-turns 1`, `total_cost_usd` 0.0410399, 5 events) and read it back:

| Event | Where the model is | Where usage is |
|-------|--------------------|----------------|
| `system` / `init` | top-level `model` (value observed: `claude-haiku-4-5-20251001`) | none |
| `assistant` (2 events) | `message.model` (no top-level `model`) | `message.usage` (no top-level `usage`) |
| `rate_limit_event` | none | none |
| `result` / `success` | none at top level; `modelUsage` is a dict keyed by the concrete model string (per-model `inputTokens`, `outputTokens`, `cacheReadInputTokens`, `cacheCreationInputTokens`, `costUSD`, `thinkingTokens`, `canonicalModel`) | top-level `usage` (`input_tokens`, `output_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`) and `total_cost_usd` |

Running the current `parse_stream` on that stream (executed): `dispatch_count 1`, `cost_usd 0.0`, `model_usage` keys `['unknown']`, 2 warnings (the two `assistant` events are skipped because `event.get("usage")` is empty at top level, and the `result` event has no top-level `model`, so it lands in the `"unknown"` bucket via `event.get("model") or "unknown"`). So with the real shape the parser reports an `unknown` model and zero cost; this also explains the existing baseline's `cost_usd=0.00`. Consequences: FR-5.5 must reject `unknown`; the parser must read the real shape (FR-5.9); the `--cost-cap 3.00` cap could not trigger on `cost_usd` 0.0 (FR-5.4 now requires observed cost). The exact `system/init` field name (OQ-10) is now OBSERVED on CLI 2.1.278 as top-level `model`; the docs still do not name the field, so it stays a version-sensitive observation, covered by the real-shape fixture (FR-5.10).

**S5 scope (Revision 5; Architect findings 3, 4, 5, 6).** Files S5 changes, all under `delivery-team/tests/smoke/`: `lib/metrics.py` (parser, FR-5.9), `lib/runner.py` (command construction with `--model`, `--effort` and `--max-budget-usd`; `_running_cost`; capture of the `system/init` model into the per-sample report), `lib/report.py`, `lib/aggregator.py` (only to pass the new fields through), `lib/baseline.py` (schema, consistency rule, `model moved` WARN, `model_usage.*` handling, FR-5.7), `run_smoke.py` (flags) and the baseline JSON. `lib/runner.py`, `lib/report.py` and `lib/aggregator.py` are added to the BC-07 producer list. The new baseline fields (`model_requested`, `model_resolved`, `model_pin_env`, `effort`, `host_context`, `samples`) are copied TOP-LEVEL from the per-sample reports; they are NOT aggregated as numeric metrics (`_collect_metric_values` is numeric-only). Authoring split (FR-4.4): the producers write `lib/` and `run_smoke.py`; a separate validator dispatch writes `tests/test_model_capture.py` (new; keeps the 3-test contract of `test_meta.py`) and `tests/fixtures/`. Every S5 meta-test AC below therefore runs `test_model_capture.py`, not `test_meta.py`. Cost-cap defect found by the Architect (verified by reading `lib/runner.py:38-48`, `95`, `252`): `_running_cost` sums a per-event `usage.cost_usd` that the real stream never carries (cost arrives only as `total_cost_usd` on the final `result` event, table above), so the mid-run kill at `_running_cost(events) > cost_cap` can never fire; FR-5.4 and FR-5.9 fix this in two layers.

- **FR-5.1** Add confirmed-observable metrics, always emitted (BINDING-4.1): `tokens.cache_hit_ratio` (`cache_read / (cache_read + cache_creation + input)`, 0.0 on zero denominator) and `model_usage.<model>.dispatches` for every model observed in the run (keys are whatever ran; no fixed ID list; never the key `unknown`).
  - **AC-5.1**: python loads the baseline JSON and asserts `'tokens.cache_hit_ratio' in metrics`, that at least one key starts with `model_usage.`, and that no key equals `model_usage.unknown` or starts with `model_usage.unknown.`; MUST print `OK`.
- **FR-5.2** Best-effort metrics WARN, not FAIL, when absent (BINDING-4.2): `thinking_tokens` (the real `result` event carries `modelUsage.<model>.thinkingTokens`), `stop_details.refusal_code`, `speed_or_fast_indicator` (the real `usage` block carries `speed`).
  - **AC-5.2** (literal text, QA warning): the WARN is a line in the run report text (the same text the runner prints and saves) of the exact form `WARN missing <field>`, one per absent field: `WARN missing thinking_tokens`, `WARN missing stop_details.refusal_code`, `WARN missing speed_or_fast_indicator`. Three meta-tests in `tests/test_model_capture.py` (validator dispatch), named `test_warn_missing_thinking_tokens`, `test_warn_missing_stop_details_refusal_code`, `test_warn_missing_speed_or_fast_indicator`, each feed a stream fixture lacking the field, assert that literal string is in the report text AND that the run exit status is unchanged (a WARN never fails). Check: `python3 -m pytest delivery-team/tests/smoke/tests/test_model_capture.py -k warn_missing -v 2>&1 | grep -c PASSED` MUST print 3.
- **FR-5.3** Runner adds `--model` (default `opus`, forwarded as `claude --model opus`) and `--effort` (value `xhigh` for baseline and regression runs; BINDING-4.3, project choice, OQ-5). The harness must not pass a disabled-thinking setting at `xhigh` (documented: thinking cannot be disabled at `xhigh` or `max`, section 8).
  - **AC-5.3**: `python3 delivery-team/tests/smoke/run_smoke.py --help | grep -cE -- "--(model|effort)"` MUST be >= 2.
- **FR-5.4** Per-run cost cap `--cost-cap 3.00` is enforced in TWO layers, because the existing in-process cap cannot fire on a real stream (Architect finding 3, see the S5 scope paragraph). Layer 1, the CLI: the runner passes `--max-budget-usd <cost-cap>` to `claude` (verified present in local `claude --help`, CLI 2.1.278: "--max-budget-usd <amount> Maximum dollar amount to spend on API"), so the CLI stops the run itself. Layer 2, the harness: `_running_cost` in `lib/runner.py` reads the `result` event's `total_cost_usd` (in addition to any per-event `usage.cost_usd`), so the post-run cap check and the reported `cost_usd` both see the observed cost (FR-5.9). Never a `0.0` from a real stream.
  - **AC-5.4**: baseline JSON `metrics['cost_usd']['hard_max']` MUST equal 3.0 AND `metrics['cost_usd']['mean']` MUST be greater than 0.0 (a `0.0` cost means the parser did not read the real shape).
  - **AC-5.4b** (meta-tests in `tests/test_model_capture.py`, no `claude` process, no cost): `test_cmd_has_max_budget` builds the runner's command list for cost-cap 3.00 and asserts it contains `--max-budget-usd` followed by `3.00` (or `3.0`), `--model` followed by `opus` and `--effort` followed by `xhigh`; `test_running_cost_reads_total_cost_usd` feeds the real-shape fixture events to `_running_cost` and asserts the value equals the fixture's `total_cost_usd` and is above 0. Check: `python3 -m pytest delivery-team/tests/smoke/tests/test_model_capture.py -k "cmd_has_max_budget or running_cost" -q; echo "exit=$?"` MUST print `exit=0`.
- **FR-5.5** Resolved-model capture (observed, not assumed). The baseline gains top-level `model_requested` (the alias passed, `opus`), `model_resolved`, `model_pin_env`, `effort`, `host_context` and `samples` (per-sample raw-stream references, AC-5.5c).
  - `model_resolved` is a list of concrete model strings actually observed. Element 0 is the PRIMARY model: the model of the main session, taken from the `system/init` event's top-level `model`. The remaining elements are any other models observed (for example subagents running on a different alias, per the `modelUsage` keys of the `result` event and the `message.model` of assistant events), ordered by dispatch count descending, ties alphabetical. Primary is defined by the init event, not by dispatch count, because the latest Opus delegates more readily (section 8) and subagent dispatches can outnumber main-session ones (F9).
  - Failure rule: the capture FAILS (non-zero exit, no default, no substitution) when (a) no model string is observed, (b) the only model strings are `unknown` or empty, or (c) the `system/init` event has no model. A string equal to `unknown` (any case) or an empty string is treated as absent everywhere.
  - Consistency rule: all 5 samples must have the same `model_resolved[0]`; otherwise `--init-baseline` fails with the offending pair (the model moved mid-capture).
  - `model_pin_env` is an object with the values of `ANTHROPIC_MODEL`, `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL`, `ANTHROPIC_DEFAULT_HAIKU_MODEL` at capture (null when unset), because subagent tiers resolve through the other aliases (documented, section 8).
  - `host_context` is an object `{"bare": <bool>, "claude_code_version": <string>}`. Caveat recorded (F9): without `--bare`, `claude -p` loads hooks, plugins, auto-memory and `CLAUDE.md` of the host (local `claude --help`: `--bare` "Minimal mode: skip hooks, LSP, plugin sync, attribution, auto-memory, background prefetches, keychain reads, and CLAUDE.md auto-discovery"; the same behaviour is quoted from the headless docs in `challenger/challenge.md`), so a baseline is host-specific. Whether to add `--bare` is OQ-12; default: do not, because the help text says bare mode authenticates only via `ANTHROPIC_API_KEY` or `apiKeyHelper` (OAuth excluded), which changes the billing path.
  - **AC-5.5** (G5 closing AC; primary model checked by family word, not by a `claude-opus-` prefix, so provider-prefixed IDs such as a Bedrock form also pass; no default is supplied for a missing list):
    ```bash
    python3 - <<'PY'
    import json
    b = json.load(open('delivery-team/tests/smoke/baselines/hello_world_spike.json'))
    r = b.get('model_resolved')
    assert isinstance(r, list) and r, 'model_resolved must be a non-empty list'
    assert all(isinstance(x, str) and x.strip() and x.strip().lower() != 'unknown' for x in r), 'unknown or empty model recorded'
    assert isinstance(b.get('model_pin_env'), dict) and isinstance(b.get('host_context'), dict), 'model_pin_env and host_context required'
    print(b.get('model_requested'), 'opus' in r[0].lower(), b.get('effort'), b.get('n_samples'), b.get('sample_status'), bool(b.get('last_captured_utc')), bool(b.get('last_captured_git_sha')))
    PY
    # MUST print: opus True xhigh 5 active True True
    ```
    Note this file is `.json`, outside the guard scan; the concrete resolved ID is allowed there by design, because it is an observation.
  - **AC-5.5b** (the failure and consistency rules; meta-tests authored by the SEPARATE validator dispatch; no cost, synthetic events only): `python3 -m pytest delivery-team/tests/smoke/tests/test_model_capture.py -q` exits 0, and `-rA` output names each of these cases as passed: (i) a stream with no model anywhere makes capture exit non-zero; (ii) a stream whose only model string is `unknown` makes capture exit non-zero; (iii) a stream whose `system/init` has no model makes capture exit non-zero; (iv) two samples with different `model_resolved[0]` make `--init-baseline` exit non-zero and the message contains both model strings.
  - **AC-5.5c** (raw-evidence check, QA warning: AC-5.5 and AC-5.4 were satisfiable by a hand-edited baseline JSON). `--init-baseline` also records, per sample, the trimmed raw stream (FR-5.10 trimming rules for `system/init`) under `.delivery/artifacts/06-development/smoke-streams/sample-<n>.jsonl` (outside the guard scope by design) and lists it in the baseline as `samples: [{"stream_file": ..., "stream_sha256": ...}]` (5 entries). The check below is independent of `metrics.py`: it re-hashes each stream, reads the `system/init` model and the `result` event's `total_cost_usd` straight from the raw file, and requires them to equal the baseline's `model_resolved[0]` and `metrics.cost_usd.mean`. A hand-written baseline fails unless matching raw streams exist. Executed 2026-09-20 on today's baseline: fails with AssertionError "baseline needs a samples list of 5" (expected). Honest limit: someone who fabricates the raw streams too passes; the streams and their hashes make forgery deliberate and reviewable, they do not make it impossible.
    ```bash
    python3 - <<'PY'
    import hashlib, json
    b = json.load(open('delivery-team/tests/smoke/baselines/hello_world_spike.json'))
    S = b.get('samples')
    assert isinstance(S, list) and len(S) == b.get('n_samples') == 5, 'baseline needs a samples list of 5 (stream_file, stream_sha256)'
    total = 0.0
    for s in S:
        raw = open(s['stream_file'], 'rb').read()
        assert hashlib.sha256(raw).hexdigest() == s['stream_sha256'], 'stream hash mismatch: ' + s['stream_file']
        ev = [json.loads(l) for l in raw.decode().splitlines() if l.strip()]
        init = [e for e in ev if e.get('type') == 'system' and e.get('subtype') == 'init']
        res = [e for e in ev if e.get('type') == 'result']
        assert len(init) == 1 and init[0].get('model') == b['model_resolved'][0], 'init model must equal model_resolved[0]'
        assert len(res) == 1 and float(res[0]['total_cost_usd']) > 0, 'result event needs a positive total_cost_usd'
        total += float(res[0]['total_cost_usd'])
    assert abs(total / 5 - b['metrics']['cost_usd']['mean']) < 1e-6, 'baseline cost mean must equal the mean of the raw streams'
    print('OK')
    PY
    ```
    MUST print `OK`.
- **FR-5.6** (BINDING-4.4) The existing 4.7-era baseline (`n_samples` 1, `partial-1-of-5`) is invalidated and re-captured via `--init-baseline` (5 sequential samples, cost-capped). Old baseline is not merged.
  - **AC-5.6**: `last_captured_utc` is later than the S4 commit timestamp; `n_samples` equals 5 and `sample_status` equals `active` (AC-5.5; timestamp by QA inspection).
- **FR-5.7** Regression comparison flags model movement. When a regression run's primary resolved model (`model_resolved[0]`) differs from the baseline's, the report prints a WARN line `model moved: baseline=<X> run=<Y>`; by default the run is not failed on that alone (the metric thresholds still apply). Because thresholds tuned on one model are not valid for another, the runner also takes `--strict-model`: with it the same condition exits non-zero (for release use), and the WARN text says the baseline must be re-captured. Reproducible reruns may set `ANTHROPIC_DEFAULT_OPUS_MODEL` (documented, section 8) to pin the alias; `model_pin_env` records it. Caveat (documented, section 8): serving infrastructure around a fixed model ID can change over time, so pinning improves but does not guarantee reproducibility.
  - Dynamic model keys (Architect finding 4): `model_usage.<model>.dispatches` keys are named after whatever model ran, so when the model legitimately changes the old key vanishes and a new one appears. `model_usage.*` keys are therefore EXCLUDED from per-key threshold comparison in `lib/baseline.py` (`_check_hard_rules` and `_check_advisory_rules` skip them, so no "missing from report" failure and no advisory noise); model movement is reported only through the `model moved` WARN above and `--strict-model`.
  - **AC-5.7**: meta-tests in `tests/test_model_capture.py` (validator dispatch) build a baseline and a run with different `model_resolved[0]` (and therefore different `model_usage.<model>` keys) and assert (i) the `model moved: baseline=<X> run=<Y>` WARN appears and the exit status is unchanged with `--strict-model` unset, (ii) no line reports a `model_usage.` key as missing or as a threshold breach, and (iii) with `--strict-model` the exit status is non-zero and the text says the baseline must be re-captured; `python3 -m pytest delivery-team/tests/smoke/tests/test_model_capture.py -k model_moved -q; echo "exit=$?"` MUST print `exit=0`.
- **FR-5.8** Before the first capture, the S5 developer confirms the CLI accepts the alias. Verified by the PO on 2026-09-20: `claude --help` prints "Provide an alias for the latest model (e.g. 'fable', 'opus', or 'sonnet') or a model's full name"; installed CLI is 2.1.278. Run-time acceptance is proven by the capture itself. Additional observation: on this host `--model haiku` resolved to a concrete Haiku ID (the `init` event and `modelUsage` key show it), which supports recording the observed model rather than assuming it (OQ-6 stays open on "latest" wording).
  - **AC-5.8**: Verification: inspection; the S5 report records the exact command and exit status. If the CLI rejects `--model opus` the story stops and raises a defect (no silent substitution).
- **FR-5.9** Parser reads the real stream shape (F5 fix). `metrics.py` obtains, per event, the model from top-level `model` OR `message.model`, usage from top-level `usage` OR `message.usage`, and total cost from the `result` event's `total_cost_usd`; it does not double count the `result` event's aggregate `usage` on top of the per-`assistant` usage; the primary model comes from `system/init`. Anything that yields no model is not bucketed as `unknown` (it is reported as absent and FR-5.5 fails the capture). The same fix covers `_running_cost` in `lib/runner.py` (FR-5.4). Producer: the S5 developer, who owns `lib/metrics.py`, `lib/runner.py`, `lib/report.py`, `lib/aggregator.py`, `lib/baseline.py` and `run_smoke.py`. The exact algorithm is the developer's, but AC-5.9 pins the observable result on the real fixture.
  - **AC-5.9**: on the real-shape fixture (FR-5.10) the meta-test asserts: `dispatch_count` >= 1; input plus cache tokens greater than 0; the `model_usage` keys equal the set of model strings in the fixture and do not contain `unknown`; `cost_usd` equals the fixture's `total_cost_usd`; `python3 -m pytest delivery-team/tests/smoke/tests/test_model_capture.py -q -k real_shape` exits 0. The test is authored by the validator dispatch, not by the author of `metrics.py` (FR-4.4).
  - **AC-5.9b** (red first, FR-4.4 observation 4; QA blocking finding 3): the `real_shape` tests MUST FAIL against the unfixed parser. Procedure, run by the validator dispatch BEFORE the producer's fix lands, and repeatable at any time before ship because `main` still holds the unfixed `lib/`: export the smoke tree from `main` into a scratch directory, overlay the branch's `tests/` directory, and run the tests there; the run must fail (exit 1, not 5, so tests were selected and did fail, not 0), then the same command on the branch must pass. Today (executed 2026-09-20 against `main`, which has neither the test file nor the fixture) the selection is empty and pytest exits 5, so the AC is not yet satisfiable, which is expected:
    ```bash
    T=$(mktemp -d)
    git archive main delivery-team/tests/smoke | tar -x -C "$T"
    cp -r delivery-team/tests/smoke/tests/. "$T/delivery-team/tests/smoke/tests/"
    (cd "$T" && python3 -m pytest delivery-team/tests/smoke/tests/test_model_capture.py -q -k real_shape; echo "exit=$?")
    ```
    MUST print `exit=1` for the run against the unfixed `lib/` (the `model_usage` key `unknown` and `cost_usd` 0.0 documented in the S5 preface are the expected failures). On the branch, `python3 -m pytest delivery-team/tests/smoke/tests/test_model_capture.py -q -k real_shape; echo "exit=$?"` MUST print `exit=0`.
- **FR-5.10** Non-synthetic stream fixture. The validator dispatch stores one REAL recorded `stream-json` run under `delivery-team/tests/smoke/tests/fixtures/stream_real_shape.jsonl` with a sidecar `stream_real_shape.provenance.txt` (`claude_code_version:`, `command:`, capture date). A cheap capture (the PO's was one `haiku` prompt at $0.041, inside the NFR-2 envelope) is repeated on the S5 machine so the fixture matches the CLI that will run the baseline. The `system/init` event is trimmed to the keys the parser needs (`type`, `subtype`, `model`, `session_id`) so host paths, MCP server lists and memory paths are not committed; all other events are kept verbatim so the nesting stays real. The sidecar (a `.txt`, inside the guard scope; Architect finding 6) records the command, the CLI version and the capture date ONLY, never a concrete model ID (the ID is already in the `.jsonl`, which the guard does not scan); it names the requested alias (for example `--model haiku`), which carries no version. Smoke docs that describe `model_resolved` (README, ARCHITECTURE) use synthetic examples such as `claude-opus-fixture`.
  - **AC-5.10** (fixture shape check, independent of `metrics.py`; ran 2026-09-20 against the PO's capture copied to the fixture path in a scratch directory: prints `OK`):
    ```bash
    python3 - <<'PY'
    import json, re
    p = 'delivery-team/tests/smoke/tests/fixtures/stream_real_shape.jsonl'
    ev = [json.loads(l) for l in open(p)]
    init = [e for e in ev if e.get('type') == 'system' and e.get('subtype') == 'init']
    asst = [e for e in ev if e.get('type') == 'assistant']
    res = [e for e in ev if e.get('type') == 'result']
    assert len(init) == 1 and init[0].get('model'), 'fixture needs one system/init event with a top-level model'
    assert asst and all(e['message'].get('model') and 'usage' in e['message'] for e in asst), 'assistant events carry message.model and message.usage'
    assert not any('model' in e or 'usage' in e for e in asst), 'fixture must keep the real nesting (not hand-flattened)'
    assert len(res) == 1 and res[0].get('modelUsage') and 'total_cost_usd' in res[0], 'result event needs modelUsage and total_cost_usd'
    prov = open(p.replace('.jsonl', '.provenance.txt')).read()
    assert 'claude_code_version' in prov and 'command' in prov, 'provenance sidecar required'
    assert not re.search(r'claude-[a-z0-9.-]*(?:[0-9]|-latest)', prov, re.I), 'sidecar must not record a concrete model ID'
    print('OK')
    PY
    # MUST print OK
    ```

### S6 — Cache re-freeze (closes G9)

- **FR-6.1** Re-fingerprint `governance/cache-prefix-hash.txt` after all SKILL.md edits are final (BINDING-5.3): one `sha256sum` line for `delivery-team/skills/delivery-flow/SKILL.md`. Benefit of the new scheme: the file no longer contains a version, so a future model release does not change it and does not force a re-fingerprint.
  - **AC-6.1**: `sha256sum delivery-team/skills/delivery-flow/SKILL.md | diff - governance/cache-prefix-hash.txt && echo MATCH` MUST print `MATCH` (ran 2026-09-20 on the unmigrated tree: `MATCH`; re-run and re-freeze after S3). Scope may change per the ADR (OQ-3); the ADR then states the new command.
- **FR-6.2** ADR records the fingerprint-scope decision (BINDING-5.5). The ADR file keeps its planned name `ADR-5-0-001-cache-fingerprint-scope.md` because the ADR series is a sequence label, not a model reference; the Architect may rename it to a version-free `ADR-cache-fingerprint-scope.md` (then this AC is updated by the Architect). Architect owns it. The ADR states explicitly whether the shared mirror `delivery-team/references/shared/orchestrator-doctrine.md` (edited in S2, same block as delivery-flow 27 to 30, currently outside the fingerprint scope, OQ-3) is in or out of scope (Architect finding 7).
  - **AC-6.2**: `ls .delivery/artifacts/04-architect/adrs/ | grep -c "cache-fingerprint-scope"` MUST be >= 1, and `grep -c "orchestrator-doctrine" .delivery/artifacts/04-architect/adrs/*cache-fingerprint-scope*` MUST be >= 1 (today: 0 and grep reports no such file, the ADR is a Stage 4 output).

### S7 — Memory, changelog, ship (closes G8, G10)

- **FR-7.1** Update the binding memory file `.delivery/memory/topics/latest-model-references.md` with the run outcome.
  - **AC-7.1**: `grep -c "^## Run outcome" .delivery/memory/topics/latest-model-references.md` MUST be >= 1.
- **FR-7.2** Add a CHANGELOG entry naming BACKLOG-108 and the scheme (CHANGELOG.md may name retired IDs; it is excluded from the guard and the count).
  - **AC-7.2**: `grep -c "BACKLOG-108" CHANGELOG.md` MUST be >= 1.
- **FR-7.3** Ship via squash-rebase + ff-merge + push origin/main. No PR (BINDING-5.1). Before the push, in this order, the S7 report records the output and exit status of: (0) the PRE-SHIP-ONLY ACs, which read `main` or the branch history and stop being meaningful after the ff-merge (Architect suggestion 10): AC-2.1, AC-2.5, AC-4.4, AC-5.9b; (1) all new files present (the guard scope includes untracked files, so staging order cannot change the result; Architect finding 9); (2) `python3 scripts/check_model_pins.py` (MUST be `guard-scope hits 0 files 0`, `exit=0`; F1: the workflow cannot block a direct push, so this local run is the ship-time gate); (3) the canonical counting command from section 1 (MUST print `guard-scope hits 0 files 0`; and its hit count MUST equal the script's, the R12 equivalence check: the script's `--list` line count equals the canonical hit count on the same tree); (4) `python3 scripts/check_skill_budgets.py` (`exit=0`); (5) AC-6.1, `sha256sum delivery-team/skills/delivery-flow/SKILL.md | diff - governance/cache-prefix-hash.txt && echo MATCH` (MUST print `MATCH`; Architect finding 7: S7 memory, changelog and rebase work, or any DoD rework after S6, must not silently break the frozen fingerprint; this file has no other consumer, so nothing else would catch it). After the push the `push` run of the guard workflow on `main` is expected green. Verification: inspection; the S7 report contains the line `check_model_pins.py exit=0`; `git log origin/main -1` references BACKLOG-108 and `git rev-list --count origin/main..HEAD` equals 0 after push.
- **FR-7.4** Dispatch manifest: each stage writes `.delivery/artifacts/<NN-stage>/dispatch-manifest.txt`; line 1 `expected_validators: N`, then `<role><TAB><agent-id>` per dispatch.
  - **AC-DISP** (G8 closing AC; Developer finding 1 fixed: a real script, and Developer finding on vacuous passes fixed: a stage listed in `REQUIRED` with no manifest is a violation, so absence cannot pass). Each manifest: line 1 `expected_validators: N`, then one `<role><TAB><agent-id>` line per dispatch. The script checks `N == number of dispatch lines`, roles distinct and agent IDs distinct (BINDING-5.4), and carries an inline negative self-test (a bad and a good manifest in a temp directory; QA warning: no negative test for AC-DISP). `REQUIRED` names the stage directories that hold DoD validators in this run; Stage 1 predates the manifest rule and Stage 3 has no DoD roles in a FEATURE run, so both are out; the Architect may correct the list at Stage 4 (OQ-4). Executed 2026-09-20: prints `4 violations` (all four manifests missing; expected, because no stage has written its manifest yet):
    ```bash
    python3 - <<'PY'
    import os, tempfile
    REQUIRED = ['02-refine', '04-architect', '05-plan', '06-development']
    def violations(root, stages):
        v = []
        for s in stages:
            p = os.path.join(root, s, 'dispatch-manifest.txt')
            if not os.path.isfile(p):
                v.append((s, 'manifest missing'))
                continue
            lines = [l.rstrip('\n') for l in open(p) if l.strip()]
            if not lines or not lines[0].startswith('expected_validators: ') or not lines[0].split(': ')[1].strip().isdigit():
                v.append((s, 'line 1 must be expected_validators: N'))
                continue
            rows = [l.split('\t') for l in lines[1:]]
            if any(len(r) != 2 or not r[0].strip() or not r[1].strip() for r in rows):
                v.append((s, 'each dispatch line must be role<TAB>agent-id'))
                continue
            if int(lines[0].split(': ')[1]) != len(rows):
                v.append((s, 'N != number of dispatch lines'))
            if len({r[0] for r in rows}) != len(rows) or len({r[1] for r in rows}) != len(rows):
                v.append((s, 'roles and agent ids must each be distinct'))
        return v
    t = tempfile.mkdtemp()
    os.makedirs(os.path.join(t, 'S-bad'))
    os.makedirs(os.path.join(t, 'S-good'))
    open(os.path.join(t, 'S-bad', 'dispatch-manifest.txt'), 'w').write('expected_validators: 3\nqa\ta1\nqa\ta1\n')
    open(os.path.join(t, 'S-good', 'dispatch-manifest.txt'), 'w').write('expected_validators: 2\nqa\ta1\narchitect\ta2\n')
    assert len(violations(t, ['S-bad'])) == 2 and violations(t, ['S-good']) == [] and len(violations(t, ['S-none'])) == 1, 'self-test'
    v = violations('.delivery/artifacts', REQUIRED)
    print(len(v), 'violations', v)
    PY
    ```
    MUST print `0 violations []`.
- **FR-7.5** Housekeeping: references to the renamed files are fixed.
  - **AC-7.5**: `test -f .delivery/backlog/BACKLOG-108-latest-model-references.md && test -f .delivery/memory/topics/latest-model-references.md && test ! -e .delivery/backlog/BACKLOG-108-opus-5-migration.md && test ! -e .delivery/memory/topics/opus-5-migration.md && echo OK` MUST print `OK`. Historical stage artifacts under `.delivery/artifacts/01-idea/` and the QA round files under `.delivery/artifacts/02-refine/qa-evaluator/` still cite old names; they are immutable records and are not rewritten.

## 4. Non-Functional Requirements

| ID | Requirement | Target | Measurement |
|----|-------------|--------|-------------|
| NFR-1 | Cost per smoke run | <= $3.00 | `metrics.cost_usd.hard_max == 3.0`; per-sample `cost_usd` <= 3.0 |
| NFR-2 | Total baseline capture budget | <= $15.00 (5 x $3) | sum of `cost_usd` over the 5 samples <= 15.0. Risk R6: thinking-on models may cost more per run |
| NFR-3 | Wall clock per run | <= 1800 s | `wall_clock_seconds.hard_max == 1800.0` |
| NFR-4 | Line-budget breaches | 0 | AC-6 exit code 0 |
| NFR-5 | Guard false positives on migrated tree, and fixture failures in either engine | 0 and 0 | AC-1.2c prints `guard-scope hits 0 files 0`; AC-1.2a prints `fixture failures 0 []` (python `re` and `grep -E`) over >= 25/10/15/12 fixture strings (rule A must-hit, rule A must-pass, rule B must-hit, rule B must-pass), so the false-positive half is as enforced as the false-negative half |
| NFR-6 | Baseline sample count and model consistency | exactly 5, sequential, ONE primary resolved model | AC-5.5 prints `n_samples` 5; runner `concurrency: 1`; FR-5.5 consistency check |
| NFR-7 | Provisional/hedged behavioural claims shipped | 0 | AC-2.3 prints 0 |
| NFR-8 | CI runtime dependencies | none beyond checkout + bash/python stdlib | AC-1.3 prints 0; `git diff main -- .github | grep -c "pip install"` MUST print 0 (executed 2026-09-20 on the worktree branch: prints `0`; grep exits 1 on a zero count, which is not a failure of the check) |
| NFR-9 | Meta-test suite wall clock | < 5 s | pytest `--durations` total under 5 s for `test_meta.py` plus `test_model_capture.py` (executed today for `test_meta.py`: `3 passed in 0.01s`) |
| NFR-10 | Model-version strings (pins, versioned stamps, version prose) in the tree outside CHANGELOG and `.delivery/`; no comment or code-fence exemption | 0 | canonical count prints `guard-scope hits 0 files 0` |
| NFR-11 | Files to edit when the next model releases | 0 SKILL.md, 0 code, 0 guard patterns for a new version of an existing family; PIN_RE is family-agnostic. PROSE_RE and BARE_RE list family words, so a brand-new family word needs one edit to `scripts/check_model_pins.py` (stated, not hidden) | Verification, executable part (PO warning: NFR-11 was inspection-only): AC-1.2a requires >= 3 `synthetic-future` must-hit strings (an ID or version that does not exist yet, such as `claude-opus-9`, `claude-newfamily-7`, `Opus 12`) that the UNCHANGED patterns flag, so a next release is caught with no pattern edit; the remainder (no version in a guarded location) is inspection at ship |
| NFR-12 | Definition points for a model tier alias | exactly 1 Python definition (`MODEL_TIER_ALIAS`), plus 9 SKILL.md frontmatter lines (`model:` and `phase_1_detector_model:`) that cannot import Python and are held to the vocabulary `opus|sonnet|haiku` instead of a single location (restated after F7: there is no single definition point overall) | AC-4.1 asserts exactly one Python definition; AC-4.6 asserts `violations 0` over the 9 frontmatter lines |
| NFR-13 | Guard scan wall clock on the full tree | <= 10 s | `time python3 scripts/check_model_pins.py` (the Revision 5 canonical command ran in 0.5 s on this host on 2026-09-20; the Developer validator measured about 1.2 s for the Revision 4 command on its host, so the earlier "0.4 s" was optimistic; both are far under 10 s) |

## 5. Success Gates: one work item closes each gate

| Gate | Closing story | Closing AC | Precondition stories |
|------|---------------|-----------|---------------------|
| G1 — Guard forbids version pins (PIN/STAMP/PROSE/BARE contract, no exemptions) with zero literal IDs of its own, and runs at ship time (push trigger plus local script) | S1 | AC-1.1, AC-1.1b, AC-1.2a, AC-1.2b, AC-1.3, AC-1.5, AC-1.6a, AC-1.6b | none |
| G-LIT — Zero model-version strings repo-wide (pins, stamps, prose): canonical count `guard-scope hits 0 files 0` | S4 | AC-1b, AC-1.2c, AC-4.5b | S1, S2, S3 |
| G2 — Stamps version-free: 26 lines = `model_awareness: latest`, 26 `pattern_library_version: rev-1`, no unstamped file stamped, audit and review-due dates current | S3 | AC-3.2, AC-3.3a | S2 |
| G3 — 34/34 prose-reviewed (ledger with verdicts); zero version mentions or `frontmatter-only` in SKILL.md | S3 | AC-3.1, AC-3.1b | S2 |
| G4 — Registry tiers use ONE central alias dict, no literal ID; frontmatter tier aliases stay in `opus|sonnet|haiku` | S4 | AC-4.1, AC-4.5, AC-4.6 | none |
| G5 — 5-sample baseline captured with observed (never `unknown`) resolved model, parser proven on a real-shape stream, model-moved WARN | S5 | AC-5.4b, AC-5.5, AC-5.5b, AC-5.5c, AC-5.7, AC-5.9, AC-5.9b, AC-5.10, AC-4.4 | S4 (fixtures) |
| G6 — Line budgets pass | S3 | AC-6 | S2 |
| G7 — Behavioural claims doc-verified, zero provisional, version-free; the named version blocks are actually rewritten (floor ACs paired with the AC-2.3b intent verdict) | S2 | AC-2.1, AC-2.3, AC-2.3b, AC-2.5, AC-2.6 | none |
| G8 — One-role-one-agent dispatch honoured | S7 (checks all stage manifests) | AC-DISP | all stories |
| G9 — Cache fingerprint re-frozen, ADR filed | S6 | AC-6.1, AC-6.2 | S2, S3 |
| G10 — Shipped to origin/main with no PR | S7 | FR-7.3 inspection | S1-S6 |

Ownership rule: one gate, one closing story. Preconditions are inputs, not co-ownership. (G1 rewrite is the guard's own gate; G-LIT closes the sweep.)

## 6. Smoke-test maximal-tracking requirements

Confirmed-observable, always tracked (BINDING-4.1): `tokens.cache_hit_ratio`, `model_usage.<model>.dispatches`, `model_resolved` (FR-5.1, FR-5.5).
Best-effort, WARN when absent (BINDING-4.2): `thinking_tokens`, `stop_details` refusal codes, speed/`fast` indicators.
Runner: `--model opus` and `--effort xhigh` (FR-5.3).
Producer-validator separation (BINDING-4.5): meta-test fixtures for `metrics.py`/`baseline.py`/runner model capture, including the real-shape stream fixture (FR-5.10), authored in a SEPARATE Agent dispatch; observable invariants (FR-4.4, AC-4.4, AC-5.9b): separate commits, disjoint `Dispatch-Id` trailers, `lib/` unchanged from validator start to validator END, and the `real_shape` test red against the unfixed parser first. Producers: `lib/metrics.py`, `lib/baseline.py`, `lib/runner.py`, `lib/report.py`, `lib/aggregator.py`, `run_smoke.py`; validator files: `tests/test_model_capture.py`, `tests/fixtures/`.
Model observation rules (Revision 4): primary model = `system/init` model; other observed models recorded after it; `unknown` or empty is absence and fails the capture (FR-5.5, AC-5.5b); `--strict-model` turns model movement into a failure (FR-5.7).

## 7. Dependencies, Risks, Assumptions

### Dependencies

| Dependency | Status |
|------------|--------|
| Claude Code CLI accepts `--model opus` alias | VERIFIED locally 2026-09-20 (`claude --help`, CLI 2.1.278) and in docs (section 8) |
| `system/init` event carries the model | Documented ("reports session metadata including the model"); field name OBSERVED as top-level `model` on CLI 2.1.278 (2026-09-20 capture, S5 table); the docs do not name it, so it is pinned by the real-shape fixture (FR-5.10, OQ-10) |
| `plugin-dev:skill-development` and `plugin-dev:hook-development` skills available | Confirmed |
| Story order S1 -> S2 -> S3 -> S4 -> S5 -> S6 -> S7 | Confirmed (BINDING-2.5) |
| Architect authors the cache-fingerprint ADR before S6 | Pending (Stage 4) |
| Anthropic API budget ~$15 for baseline | Pending (user's account) |

### Risks

| ID | Risk | L | I | Mitigation |
|----|------|---|---|-----------|
| R1 | Dispatch discipline: roles fused or sub-agents over-spawned; the latest Opus delegates more readily (section 8) | M | H | AC-DISP manifest; one-role-one-agent at DoD; dispatch count capped at `dod_validators` length |
| R2 | Prose sweep touches 34 files and breaches line budgets | M | M | AC-6 exit 0; `Budget-Exception:` protocol; keystone-first |
| R3 | Baseline cost overrun | M | M | `--cost-cap 3.00`, sequential, NFR-1/2 |
| R4 | Guard false positive on legitimate text (Rules A and B have no comment, blockquote or fence exemption; Challenger showed "run haiku 3 times" tripping the Revision 3 PROSE_RE) | L | M | PROSE_RE is case-sensitive so a lowercase alias plus a bare integer passes; COUNT_RE blanks counts and durations ("Sonnet 4 stories", "in 5.0 seconds") before Rule B; AC-1.2a has a must-pass floor (>= 10 rule A, >= 12 rule B) that names the QA-probed false positives and runs in both engines; AC-1.2c zero-hit check; 19 prose lines affected today (section 1); history goes to CHANGELOG; NO per-line escape exists (FR-1.6): a sentence that trips the guard is reworded per the wording rule in FR-1.2 |
| R5 | Unverified behavioural claim leaks into prose | M | H | AC-2.3 scan + AC-2.3b re-fetch; OQ-2 claim never ships |
| R6 | Thinking-on default plus `xhigh` raises cost per run and may hit the $3 cap | M | M | cap fails the run loudly; fall back to `high` per OQ-5; no silent cap change |
| R7 | Behaviour drift when "latest" moves: SKILL.md guidance (delegation caps, effort advice) was verified against today's latest and can go stale with no version string to flag it | M | M | version-free wording (claims stated as general guidance); `last_audited` date is the trigger; existing quarterly fitness review (`governance/fitness-review.md`, `fitness_review_due:` frontmatter) re-verifies against the then-current docs; citations with dates live in `.delivery/` |
| R8 | Baseline reproducibility: `opus` resolves to a different model later, so a regression run is compared with a baseline from another model | M | M | FR-5.5 records `model_resolved`; FR-5.7 WARNs on movement; optional `ANTHROPIC_DEFAULT_OPUS_MODEL` pin for reruns; re-capture baseline on intentional model change |
| R9 | Alias resolves differently per provider (docs table, re-fetched by Challenger and QA on 2026-09-20: `sonnet` differs on every provider other than the Anthropic API, namely Claude Platform on AWS, Bedrock, Google and Foundry; `opus` differs only on Foundry) | L | M | smoke harness runs against the user's own provider and records the resolved ID; scheme claims only "latest for your provider" |
| R10 | Future API caller assumes an alias works on the Claude API | L | H | convention 4 and FR-2.2 state the API has no evergreen alias; FR-4.5 keeps AC-4.5 at 0 API call sites; a future caller reads ONE config value |
| R11 | The `stream-json` event shape is not documented field by field and can change with the CLI; the parser and the FR-5.5 capture depend on it (evidence: the real shape differs from the hand-written fixture, S5 table) | M | H | FR-5.9 parser reads the observed shape; FR-5.10 real-shape fixture with provenance and CLI version; capture fails loudly on no or `unknown` model (AC-5.5b); `host_context.claude_code_version` recorded in the baseline; re-record the fixture on a CLI upgrade |
| R12 | Guard bypass or drift: contributors look for a way to silence the guard, or the guard's patterns drift from this PRD | L | M | no bypass exists (FR-1.6; AC-1.6b proves the old marker text does not skip a pin); AC-1.2a fixtures pin the behaviour of both engines; the canonical command in section 1 is an independent implementation of the same contract, compared at S1 and at ship (FR-7.3) |
| R13 | Behaviour under a fixed model ID is not permanently stable: serving infrastructure can change (Challenger doc re-fetch, section 8), and `claude -p` without `--bare` loads host hooks, plugins and `CLAUDE.md` | M | M | baseline records `host_context` and `model_pin_env`; FR-5.7 WARN and `--strict-model`; re-capture on intentional change; documented as a limit of reproducibility, not solved (OQ-12) |

### Assumptions

1. Anthropic keeps the Claude Code aliases `opus`, `sonnet`, `haiku` (documented as latest for opus/sonnet; see OQ-6 for haiku).
2. `git diff main` in the worktree is the correct baseline for body-delta checks (the branch forks from main).
3. `test_meta.py` continues to run under the existing pytest setup (no new dependency).
4. Deleting the 4.7-era baseline does not break any consumer; it is read only by `baseline.py`.
5. Repo code makes no Claude API calls (evidence FR-4.5); the smoke harness drives the `claude` CLI.
6. The one-prompt real capture in section 8 is representative of the event shapes of a full smoke run (assistant, result, init); a longer run adds tool events whose model and usage placement follow the same `message.*` nesting. S5 re-records the fixture on the machine that captures the baseline (FR-5.10) so this assumption is re-tested, not trusted.

## 8. Citations

All rows fetched live on 2026-09-20 (WebFetch), plus one local command. Quotes are copied from the fetched pages. Version-specific behaviour rows are recorded for the sweep-date latest (Opus 5, effective current model) and NEVER ship as version strings.

| Claim | Verdict | Source URL and quote |
|-------|---------|----------------------|
| Claude Code has model aliases; `opus` and `sonnet` are the latest of their family | VERIFIED (fetched three times on 2026-09-20: PO, Challenger, QA; the fetch tool renders table cells with slightly different lead-in words, substance identical) | https://code.claude.com/docs/en/model-config : Challenger and QA re-fetch cells read "Uses the latest Opus model for complex reasoning tasks" and "Uses the latest Sonnet model for daily coding tasks" (the PO's earlier fetch rendered them "Latest Opus model ..." and "Latest Sonnet model ...") |
| `haiku` alias described as "latest" | UNVERIFIED (docs cell says only "the fast and efficient Haiku model for simple tasks"; local observation: on this host `--model haiku` resolved to a concrete Haiku ID, which shows resolution but not "latest") | same page; OQ-6 |
| `--model` accepts an alias | VERIFIED (docs and local CLI) | model-config: "The `--model` flag accepts aliases directly" with `claude --model opus`. Local `claude --help` (CLI 2.1.278): "--model <model> Model for the current session. Provide an alias for the latest model (e.g. 'fable', 'opus', or 'sonnet') or a model's full name (e.g. 'claude-fable-5')." |
| Aliases update over time; pin by full name or env var | VERIFIED | model-config: "Aliases point to the recommended version for your provider and update over time. To pin to a specific version, use the full model name ... or set the corresponding environment variable like `ANTHROPIC_DEFAULT_OPUS_MODEL`." |
| Alias resolution differs by provider | VERIFIED (Challenger and QA re-fetches agree) | model-config table "Latest Versions by Provider": Anthropic API Opus 5 / Sonnet 5; Claude Platform on AWS Opus 5 / Sonnet 4.6; Bedrock and Google Opus 5 / Sonnet 4.5; Foundry Opus 4.6 / Sonnet 4.5. So `opus` differs only on Foundry; `sonnet` differs on every non-Anthropic provider (R9, QA W4-6) |
| Serving infrastructure can change behaviour under a fixed model ID | VERIFIED by Challenger's WebFetch of 2026-09-20 (the PO did not re-fetch; quote taken from `challenger/challenge.md`) | https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions : weights are fixed per ID but "serving infrastructure around the model can change over time" (quote as recorded by the Challenger; the surrounding sentence is not reproduced here). Consequence: pinning via `ANTHROPIC_DEFAULT_OPUS_MODEL` improves reproducibility, it does not guarantee it (FR-5.7, R13) |
| `claude -p` without `--bare` loads the host context | VERIFIED locally (help text) and by Challenger's headless-doc re-fetch | Local `claude --help` (CLI 2.1.278): "--bare Minimal mode: skip hooks, LSP, plugin sync, attribution, auto-memory, background prefetches, keychain reads, and CLAUDE.md auto-discovery. Sets CLAUDE_CODE_SIMPLE=1. Anthropic auth is strictly ANTHROPIC_API_KEY or apiKeyHelper via --settings". The headless docs statement is recorded in `challenger/challenge.md` (not re-fetched by the PO) |
| Real `stream-json` shape (init model top level; assistant `message.model` and `message.usage`; result top-level `usage`, `total_cost_usd`, `modelUsage` keyed by model) | VERIFIED by a local run, not by docs (the docs name none of these fields) | One capture on 2026-09-20, CLI 2.1.278: `claude -p "reply with the single word ok" --model haiku --output-format stream-json --verbose --max-turns 1`, 5 events, `total_cost_usd` 0.0410399; keys printed by a read-back script (S5 table). The raw file is a scratch artifact under `/tmp` and is NOT shipped; FR-5.10 has the validator dispatch record a trimmed real fixture |
| The Claude API has NO evergreen "latest" ID for current models; every ID is a pinned snapshot | VERIFIED | https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions : "A common misconception is that dateless model IDs such as `claude-sonnet-4-6` behave as evergreen pointers that route to the latest or best-performing version. That is not the case." and "When an updated version is available, it ships under a new model ID." Also https://platform.claude.com/docs/en/about-claude/models/overview : "Every Claude model ID is a pinned snapshot" |
| Pre-4.6 API aliases point to the latest dated snapshot of the SAME minor version only (not latest model) | VERIFIED | model-ids-and-versions: "an alias such as `claude-sonnet-4-5` is a convenience pointer that resolves to the most recent dated snapshot for that minor version" |
| Some `-latest` API alias exists for current models | UNVERIFIED and treated as absent; nothing in this PRD depends on it | not found in either page above |
| `system/init` reports the model; JSON output carries a per-model cost breakdown | VERIFIED in docs (field names not in docs; observed locally, see the stream-json row above; OQ-10) | https://code.claude.com/docs/en/headless : "The `system/init` event reports session metadata including the model, tools, MCP servers, and loaded plugins."; "the response payload includes `total_cost_usd` and a per-model cost breakdown" |
| Opus 5 is the current Opus; prior 4.x are legacy | VERIFIED (context only; not shipped) | https://platform.claude.com/docs/en/about-claude/models/overview : "start with Claude Opus 5 for most workloads"; legacy list includes "Claude Opus 4.8, Claude Opus 4.7" |
| Default effort `high`; setting `high` equals omitting it | VERIFIED (2026-09-19, effort doc; overview table 2026-09-20: "Default effort ... `high`") | https://platform.claude.com/docs/en/build-with-claude/effort : "The API default is `high`." |
| Effort levels are recalibrated between model releases (so per-version effort advice must not be hard-coded) | VERIFIED (2026-09-19) | https://platform.claude.com/docs/en/models/opus-5/migration-guide : "Effort levels recalibrated: The token allocation behind each effort level changes on Claude Opus 5 compared to Claude Opus 4.7 ..." |
| Thinking cannot be disabled at `xhigh` or `max` effort | VERIFIED (2026-09-19) | effort doc: "thinking cannot be disabled at `xhigh` or `max` effort" |
| The latest Opus delegates to subagents more readily; give scope or cap | VERIFIED (2026-09-19; reverses the older "dispatches fewer sub-agents" claim, which is REFUTED and must never ship) | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5 : "Claude Opus 5 delegates to subagents more readily than prior models." |
| Explicit verification instructions cause over-verification | VERIFIED (2026-09-19) | same page, "Task scope and over-verification": "instructions like these cause over-verification on Claude Opus 5" |
| "Latest Opus follows instructions more literally than the previous one" | UNVERIFIED as a general claim; do not ship | OQ-2 |
| Claude Code default effort is `high` | UNVERIFIED (API default documented; Claude Code default not found) | OQ-8 |

## 9. Open Questions

| ID | Question | Owner | Due | Why non-blocking |
|----|----------|-------|-----|------------------|
| OQ-1 | RESOLVED by doc: the latest Opus delegates MORE readily. Confirm S2 dispatch prose reflects over-delegation direction, version-free | Architect | Stage 4 | Claim VERIFIED and cited; FR-2.3, FR-2.5 encode it |
| OQ-2 | Does a doc source exist for "more literal instruction following" in the latest Opus? | Architect | Stage 4 | No shipped prose depends on it; AC-2.3 and adversarial re-fetch catch leakage |
| OQ-3 | Should the cache fingerprint scope widen beyond `delivery-flow/SKILL.md`? | Architect (ADR) | Stage 4 | Default AC-6.1 runnable with current scope |
| OQ-4 | Where do `dod_validators` counts live per stage, for the manifest header? | Architect | Stage 4 | FR-7.4 format is source-independent |
| OQ-5 | `xhigh` (project choice, BINDING-4.3) or `high` (doc default) for the smoke baseline, given effort levels are recalibrated per release? | Architect | Stage 4 | Both valid; cap enforced; FR-5.5 records the effort used |
| OQ-6 | Restated (former Sonnet-tier question, now moot: `sonnet` alias tracks the latest Sonnet, no allowlist tier remains). Remaining: does the `haiku` alias resolve to the latest Haiku? Docs do not say "latest" for haiku | Developer (S5) | S5 start | The registry haiku entry is a label only (FR-4.5); the smoke runner uses `opus` only |
| OQ-7 | RESOLVED: `claude --model opus` accepted by the installed CLI (`claude --help`, section 8); run-time acceptance proven by capture (FR-5.8) | Developer (S5) | S5 start | Failure stops S5 with a defect |
| OQ-8 | Is the Claude Code default effort `high`? UNVERIFIED | Developer (S5) | S5 start | Runner sets effort explicitly; claim never ships |
| OQ-9 | Now that stamps no longer certify an audit against a version, must all 34 SKILL.md still get a full prose review (BINDING-2.2), or only the 2 SKILL.md files with version mentions (delivery-flow, prompt-engineer) plus keystones? PO default: retain full sweep. STILL OPEN for the user; Revision 4 did not decide it (AC-3.1 is now a ledger that works under either answer: a narrowed sweep would shrink the ledger and the AC's count) | Michael | S3 start | Default already scoped and costed; narrowing only reduces work |
| OQ-10 | RESOLVED by observation, doc gap remains: on CLI 2.1.278 the model is top-level `model` in `system/init`, `message.model` in assistant events, and the keys of `modelUsage` in the result event (S5 table). The docs do not name these fields, so the shape is pinned by the real-shape fixture (FR-5.10) and re-verified on CLI upgrades | Developer (S5) | S5 start | FR-5.5 fails loudly on no or `unknown` model; FR-5.9 and AC-5.10 make the parser and fixture testable |
| OQ-11 | Delivery-flow frontmatter says `model: sonnet` while its dispatch guidance targets the latest Opus. PO decision recorded in FR-2.6 (frontmatter unchanged, guidance conditional). Confirm or override | Architect | Stage 4 | Either answer leaves AC-2.5 satisfiable; the cap holds for every model |
| OQ-12 | Should the smoke runner add `--bare` so a baseline does not depend on host hooks, plugins and `CLAUDE.md`? Bare mode authenticates only via `ANTHROPIC_API_KEY` or `apiKeyHelper` (local help), which may change the billing path. PO default: no `--bare`; record `host_context` (FR-5.5) | Michael | S5 start | Default is the current behaviour; the caveat is recorded (R13) |

## 10. Scope

**In scope**: guard rewrite (forbid pins; new `scripts/check_model_pins.py` and `scripts/model_pin_fixtures.json`; workflow triggers push/pull_request/workflow_dispatch; `.githooks/pre-commit` call); version-free stamps in the 25 stamped SKILL.md (26 model_awareness + 26 pattern_library_version lines) and reset of the 11 lapsed `fitness_review_due` dates; version-free prose in 34 SKILL.md plus `delivery-team/references/shared/orchestrator-doctrine.md` (19 prose lines in 3 files today, plus the hand-named lines `prompt-engineer/SKILL.md` 363, 365, 371, 420); `agent_registry.py` central `MODEL_TIER_ALIAS` and its three comment lines; `flow_orchestrator.py:663` comment; `prompt-engineer/SKILL.md:368`; real-shape stream fixture and parser fix in the smoke harness; `conftest.py`, `smoke-test-architecture.md`, `telemetry-schema.md` example strings; runner `--model` / `--effort`; baseline schema (`model_requested`, `model_resolved`, `model_pin_env`, `effort`, `tokens.cache_hit_ratio`, `model_usage`); baseline re-capture; cache re-fingerprint and ADR; dispatch manifests; memory + CHANGELOG; the renames in the Revision 3 changelog.

**Out of scope**: `prd-quality-gate-flow/` routing aliases (BINDING-1.4; version-agnostic labels, and PIN_RE finds none); any `.github/workflows/smoke-*.yml` (BINDING-4.6; the guard workflow is a static scan, not a smoke workflow); any PR (BINDING-5.1); branch protection or any mechanism that blocks a direct push (the local script is the gate); creating stamps in the 9 unstamped files; changing delivery-flow's `model: sonnet` (FR-2.6); `--bare` for the smoke runner unless OQ-12 says so; scanning `.json` files (baselines record observed IDs by design); changing the Claude API contract (no repo caller exists); rewriting Stage 1 historical artifacts or QA round files.

## 11. Constraints

1. Plugin-dev skill routing is non-optional (CLAUDE.md).
2. Budget ~$15 total, `--cost-cap 3.00` per run.
3. Behavioural claims doc-verified (BINDING-3.1 to 3.3).
4. Line budgets A=500 / B=300 / C=200; exceptions need `Budget-Exception:` + `known_debt[]` with `target_wave:`.
5. One Role = One Sub-Agent (BINDING-5.4).
6. Guard ships in its final form from day one; squash before merge so it never sees a partial state (BINDING-2.1, BINDING-5.1).
7. Producer-validator separation for meta-tests (BINDING-4.5), observable per FR-4.4 (commits, `Dispatch-Id` trailers, `lib/` unchanged start to end, red-first).
8. Bash / python-stdlib only in ACs.
9. Local-only: nothing in `.github/workflows/` shells out to `claude`.
10. The guard must be able to run at ship time: `push` to `main` trigger plus the local `scripts/check_model_pins.py` before the direct push (FR-1.1, FR-1.5, FR-7.3).
11. The guard has no comment, blockquote, heading or code-fence exemption and NO per-line escape (FR-1.2, FR-1.6); counts and durations are filtered by COUNT_RE, everything else is reworded.

## 12. Stop-rule

Defects/story > 0.4 across any 3-story window pauses the initiative. Current rolling rate = 0.111.

## 13. Revision 1 changelog

| QA defect | Fix |
|-----------|-----|
| D-1 FR->AC coverage | Every FR has a named AC; process-only FRs tagged "Verification: inspection". |
| D-2 NFRs | NFR-1..9 with numeric targets and commands. |
| D-3 Gate ownership | One closing story per gate. |
| D-4 AC-DISP | FR-7.4 defines `dispatch-manifest.txt`. |
| D-5 Weak ACs | Per-ID greps, anchored checks, CHANGELOG excluded, walk.py prunes dirs. |
| D-6 Open questions | Section 9 with owner, due, non-blocking rationale. |
| D-7 Missing sections | Personas, dependencies, risks, assumptions. |
| D-8 AC-5 vs schema | Baseline schema extension FRs. |
| D-9 False positives | AC-2.3 scoped, excludes research-agent rubric prose. |
| D-10 constraints.yml | `entities` and `invariants` added. |
| D-11 Discovery numbers | Corrected (see later revisions). |
| D-12 Body-delta | AC-3.1 machine check. |
| D-13 BINDING-4.4 | Baseline invalidate and re-capture. |

## 14. Revision 2 changelog

Retarget (user decision): Opus 4.8 -> Opus 5. Moved every target reference to `claude-opus-5` and corrected behavioural claims after live re-verification (delegation direction reversed, thinking default, cache minimum, cutoff). QA round 2 defects: D2-1 provenance comment on its own line; D2-2 one canonical counting command; D2-3 portable guard patterns; D2-4 `git diff main` assumption stated. Renamed `BACKLOG-108-opus-4-8-migration.md` to `BACKLOG-108-opus-5-migration.md` and the memory topic likewise. Historical stage-1 artifacts left as immutable records. (Full Revision 2 text is superseded by this revision; the design it described, pin `claude-opus-5`, is replaced below.)

## 15. Revision 3 changelog

**Design change (user decision, binding, 2026-09-20): "We should just say latest version of model X."** The repo stops pinning model versions and refers to the latest of a family. Opus 5 is the effective current model; it appears only in dated citations and in observed baselines.

**Questions resolved with evidence (design questions 1 to 5)**

| # | Question | Resolution |
|---|----------|-----------|
| 1 | What does the platform accept as "latest"? | Claude Code CLI: aliases `opus`, `sonnet` (latest), `haiku` (latest wording UNVERIFIED), and `fable`; `--model opus` verified in docs and local `claude --help`. Claude API: NO evergreen alias for current models (every ID is a pinned snapshot, quoted in section 8). Therefore code that only labels a tier uses the CLI alias, defined once (`MODEL_TIER_ALIAS`, FR-4.1); code that must call the API reads one config value (convention 4); no repo code calls the API today (FR-4.5). Concrete-ID literals in code: none unavoidable. |
| 2 | Prose/metadata convention | Prose names families only. `model_awareness: latest`, `pattern_library_version: rev-1`, `last_audited: <date>` as the time anchor. The census still needs edits, because today's stamps encode 4.7: all 26 `model_awareness` lines and all 26 `pattern_library_version` lines in the 25 stamped files (26 lines / 25 files census re-run today). The 9 unstamped files get no stamp. Prose sweep of all 34 retained (OQ-9); version mentions today: 8 lines in 2 files. |
| 3 | Guard purpose | Forbid re-introduced pins: `PIN_RE`, `STAMP_RE`, `PROSE_RE` contract (FR-1.2), portable to `grep -E` and Python `re`; allowlisted locations: `CHANGELOG.md`, `.delivery/**`, `#`/`>` lines for Rule A. Canonical count: 14 hits in 6 files today, target 0. |
| 4 | Baseline capture | Runner adds `--model opus`; baseline records `model_requested`, observed `model_resolved`, `model_pin_env`, `effort`; capture fails if no model observed; 5 samples must agree; regression run WARNs on `model moved` (FR-5.5, FR-5.7). |
| 5 | Risks, OQs, gates | New R7 (behaviour drift), R8 (baseline reproducibility), R9 (provider resolution), R10 (API alias assumption); R7-old (Sonnet allowlist) removed as moot. OQ-6 restated (haiku alias), OQ-7 resolved, OQ-9 and OQ-10 added. Gates re-worded; each still closed by exactly one story. |

**Effect on each earlier item**

| Earlier item | Effect |
|--------------|--------|
| FR-1.1 positive allowlist (opus-5 / sonnet-4-6 / haiku-4-5) | Replaced: guard forbids pins, holds no ID (FR-1.1, FR-1.2). AC-1.1, AC-1.2a/b/c rewritten. |
| FR-1.2 retired-ID rejection of 4-7 / 4-8 | Subsumed: any versioned ID is rejected, including today's 4-7 and future IDs. |
| FR-2.2 `MODEL_ID = "claude-opus-5"` | Now a config read with no literal (FR-2.2). |
| FR-2.3 / FR-2.5 delegation guidance | Kept, rewritten version-free; effort advice must not cite a per-version level. |
| FR-3.1 full sweep | Kept (OQ-9); lens changed to version-free wording; AC-3.1b now also checks `PROSE_RE`. |
| FR-3.2 create 9 stamps | Reversed: 9 unstamped files get no stamp. |
| FR-3.3 stamps `opus-5`, `5-0-1`, `2026-09-19` | Now `latest`, `rev-1`, `last_audited` date of S3 DoD pass; "35 stamp lines" removed (26 stay 26). |
| 34 SKILL.md `model_awareness:` census | 34 SKILL.md, 26 lines, 25 files, 19 `frontmatter-only`, 7 `opus-4-7` (re-run today); every line edited to `latest`. |
| FR-4.1 registry ID `claude-opus-5` + provenance line | Replaced by central `MODEL_TIER_ALIAS`; existing `#` provenance comments retained; the new "one permitted 4.7 string" (BINDING-2.4) is moot because 0 literals remain. |
| FR-4.2 conftest, FR-4.3 smoke-test-architecture (115) | Synthetic IDs; FR-4.3 now covers lines 115 AND 116 and `telemetry-schema.md:36`. |
| The 9 `claude-opus-4-7` literals in 5 files | Still fixed (they are inside the 14 in 6 files); FR-4.x plus S1 cover all 14. |
| Smoke harness baseline `model` / `model_usage.claude-opus-5.*` keys | Replaced by `model_requested` / observed `model_resolved`; `model_usage.<model>` keyed by whatever ran (FR-5.1, FR-5.5). |
| FR-5.7 CLI accepts `claude-opus-5` (OQ-7) | Now FR-5.8: alias `opus`, verified. Old FR-5.7 slot is the model-moved WARN. |
| Cache re-fingerprint (FR-6.1) | Still required once (SKILL.md edits); future releases no longer force it. ADR name may be made version-free. |
| prompt-engineer `MODEL_ID` | Config read (FR-2.2). |
| OQ-6 Sonnet tier | Moot in its old form (no allowlist tier remains); restated as the haiku-alias question. |
| G-LIT / G2 / G4 / G5 wording | Re-worded; closing stories unchanged (S4 / S3 / S4 / S5). |

**QA round 3 defects (evaluation-round-3.md)**

- **D3-1** (`claude-sonnet-4-5` at `smoke-test-architecture.md:116` unreachable): RESOLVED and made structural. FR-4.3 moves lines 115 and 116; the guard now catches any versioned ID by construction, so AC-1.2c and NFR-5 reach 0 through S4 alone. Verified: the canonical count lists line 116.
- **D3-2** (AC-1.2c exact pre-migration value): RESOLVED. AC-1.2c states today's value `70` (guard scope, py/md only) and the canonical count states `14 in 6 files`.

**Commands run and results (2026-09-20, worktree root)**: canonical count `pinned-id hits 14 files 6` (list in section 1); stamp census `skill 34` / `26 25 {...19, ...7}`; `pattern_library_version` census `26 x 4-7-1`, 25 files; SKILL.md prose version mentions `8 lines in 2 files`; `check_skill_budgets.py` exit 0; cache hash `MATCH`; AC-1.2a fixture logic run against the suggested patterns: `OK`; `claude --help` shows the alias text quoted in section 8; `claude --version` 2.1.278; `validate_constraints.py` on the revised constraints.yml: valid, rc=0.

**Renamed by Revision 3**: `.delivery/backlog/BACKLOG-108-opus-5-migration.md` -> `BACKLOG-108-latest-model-references.md`; `.delivery/memory/topics/opus-5-migration.md` -> `latest-model-references.md`; `.delivery/memory/index.md` and `.delivery/state.md` updated (initiative line, binding_notes, ADR name in the routing list). `.delivery/artifacts/01-idea/**` and QA round files not rewritten.

**Unverified claims (not shipped; carried as OQs)**: `haiku` alias is "latest" (OQ-6); exact `system/init` model field name (OQ-10); Claude Code default effort (OQ-8); literal-instruction-following comparison (OQ-2); existence of any API `-latest` alias (treated as absent).

## 16. Revision 4 changelog

Inputs: `challenger/challenge.md` (F1 to F6 significant, F7 to F11 minor; confidence 3/5) and `qa-evaluator/evaluation-round-4.md` (W4-1 to W4-6, S4-1, S4-2). Design decision unchanged. Dispositions: FIXED (text and AC changed), REBUTTED (evidence, no change), DEFERRED (owner, due, why non-blocking). Every claim below was checked by running a command on 2026-09-20 in the worktree root before this text was written.

| Finding | Disposition | Where and evidence |
|---------|-------------|--------------------|
| F1 guard never runs at ship (pull_request only, direct push) | FIXED | FR-1.1 triggers push to main, pull_request, workflow_dispatch, no `paths:`; AC-1.1b (ran on compliant sample: `OK`; on today's file: AssertionError); FR-1.5 local script plus `.githooks/pre-commit` call plus mandatory ship step (FR-7.3); no `smoke-*` workflow added (AC-1.3 unchanged: 0 and 0). Honest limit stated: the push run detects after the fact and cannot block; branch protection is out of scope |
| F2 PROSE_RE misses bare versions; "8 lines in 2 files" wrong | FIXED | Discovery re-run: 19 prose lines in 3 files (delivery-flow 27, 30, 273, 276; prompt-engineer 88, 347, 349, 351, 356, 359, 361, 373, 375, 397, 401, 408; orchestrator-doctrine 77, 79, 82; the third file was new). Added `BARE_RE` and widened `PROSE_RE` (case, `v`, no-space, several spaces); Rule B now covers all `*.md`; FR-2.1 names every site; corrected counts in section 1 |
| F3 pin false negatives (`claude-3-5-sonnet-*`, `-latest`, uppercase, quoted stamp, `pattern_library_version: 4.7.1`, `#`/`>` exemption) | FIXED, one loophole accepted | `PIN_RE` is family-agnostic and case-insensitive; `STAMP_RE` tightened; all exemptions removed; every row in the challenge table is a fixture in AC-1.2a, run in Python `re` and `grep -E` (result on the simulated script: `fixture failures 0 []`). Concatenated IDs (`"claude" + "-opus-" + "5"`) remain undetectable: recorded as an accepted loophole in FR-1.2 |
| F4 prose false positives ("run haiku 3 times") and heading loophole | FIXED | `PROSE_RE` is case-sensitive for the capitalised and upper-case forms; the lowercase alias needs hyphen-digit, digit-glued, or a dotted version after a space; `run haiku 3 times` is a must-pass fixture; headings and fences have no exemption; per-line escape `model-pin-ok`, banned at ship (FR-1.6, AC-1.6, R12). A capitalised sentence-initial "Haiku 3 times" would still hit and needs the marker: accepted and recorded |
| F5 model capture satisfied by an `unknown` bucket; no real stream shape | FIXED (with new executed evidence) | Real capture run (CLI 2.1.278, $0.041): model is top-level in `init`, `message.model` in assistant events, `modelUsage` keys in the result; running the current `parse_stream` on it printed `model_usage` key `['unknown']`, `cost_usd 0.0`, 2 warnings. Revision 3's "already buckets by model" claim is withdrawn (S5 preface). FR-5.5 rejects `unknown`/empty; AC-5.5, AC-5.5b, new FR-5.9 and FR-5.10, AC-5.9, AC-5.10, AC-5.1, AC-5.4 (cost mean above 0). OQ-10 resolved by observation, doc gap noted |
| F6 ACs satisfiable by trivial edits (AC-3.1, 2.1, 2.5, 4.2) | FIXED | AC-3.1: ledger with named reviewer, verdict, reason; AC-2.1: 25 named source lines must be gone (ran: `25 source lines still present` today); AC-2.5: conditional "latest Opus" phrasing plus subagent, cap, `dod_validators`, no HTML comment; AC-4.2: counts `"model": "claude-opus-fixture"` values and runs the meta-tests; floor-versus-intent statement added to S2. Sub-items: F6-3 (registry `os.environ` worry) REBUTTED, the registry has no env lookup, but added `py_compile` and comment checks to AC-4.1; F6-4 FIXED (AC-3.3a reads frontmatter only, the code-fence example is out of scope); F6-5 (S1 to S3 leave the guard red) REBUTTED: by design, safe because ship is squash plus the local run in FR-7.3 (Constraint 6, 10) |
| F7 NFR-12 overclaims one definition point; delivery-flow `model: sonnet` vs "latest Opus" | FIXED | NFR-12 restated (1 Python definition plus 9 frontmatter alias lines, ran: `9 ['haiku', 'opus', 'sonnet'] violations 0`); AC-4.6 pins the vocabulary; FR-2.6 records the PO decision (frontmatter unchanged, guidance conditional, AC-2.6); OQ-11 to the Architect |
| F8 only `skill-md-header-warn.yml` reads stamps; `fitness_review_due` lapsed | FIXED | Verified: presence-only `grep -L`, `continue-on-error: true`; the 9 unstamped files keep the warning (accepted, FR-3.2). All 11 `fitness_review_due` are `2026-08-09`; FR-3.3 resets them, AC-3.3a checks both dates (ran: `36 violations` today) |
| F9 baseline primary-model ordering fragile; AC-5.5 hardcodes `claude-opus-`; strict mode; env pins; host context | FIXED, `--bare` DEFERRED | Primary = `system/init` model; other models after it; AC-5.5 uses `'opus' in r[0].lower()`; `--strict-model` (FR-5.7, AC-5.7); `model_pin_env` object with four variables; `host_context` recorded. `--bare` adoption DEFERRED as OQ-12: owner Michael, due S5 start, non-blocking because the default equals current behaviour and the caveat is recorded (R13); local `--help` shows bare mode restricts auth to an API key or `apiKeyHelper` |
| F10 API trap comment, stale registry comments, constraints wording | FIXED | FR-4.5 and AC-4.5b (`flow_orchestrator.py:663` reword, today 1 match); FR-4.1 replaces the three registry comments (they are pin lines under the new guard: 6 registry pin lines counted today) and AC-4.1 requires `opus-4-7` count 0; constraints.yml BC-04 reworded |
| F11 scope gaps | FIXED, one REBUTTED | Named lines added to FR-2.1 and section 10; guard scope widened to py, md, yml, yaml, txt, sh; `.json` excluded on purpose and stated. `.claude-plugin/marketplace.json:23` ("Uses Opus for advanced reasoning") REBUTTED: alias-level text, no version, no regex hit |
| Doc caveat: infrastructure changes shift behaviour under a fixed ID | FIXED (recorded) | Section 8 row, FR-2.3, FR-5.7, R13. Source is the Challenger's fetch; the PO did not re-fetch and says so |
| Doc caveat: `claude -p` without `--bare` loads host context | FIXED (recorded) | Section 8 row (local help text verified), FR-5.5 `host_context`, R13, OQ-12 |
| W4-1 prose lines 371 and 415 to 421 not named | FIXED | FR-2.1 (lines 363, 365, 371, 420), AC-2.2 extra greps (`canonical <YYYY`, `Versioned Model Reference`), FR-3.2 (example block at 415 to 417) |
| W4-2 `flow_orchestrator.py:663` API trap | FIXED | See F10 |
| W4-3 guard scope narrower than count; heading loophole | FIXED | See F1, F3, F4; canonical count and guard now have the same scope by construction (one contract) |
| W4-4 FR-5.5 behaviours without AC | FIXED | AC-5.5b (four meta-test cases: no model, `unknown` only, init without model, two samples with different primary models) |
| W4-5 AC-5.5 hardcodes prefix; stale registry comments | FIXED | See F9 and F10 |
| W4-6 R9 provider claim over-broad | FIXED | R9 and section 8 rewritten: `sonnet` differs on every non-Anthropic provider, `opus` only on Foundry |
| S4-1 constraints.yml wording (BC-04, BC-02 URL) | FIXED | constraints.yml edited; `validate_constraints.py`: valid, rc=0 |
| S4-2 AC-2.1 phrasing about stamps | FIXED | AC-2.1 rewritten (no stamp lines involved) |
| OQ-9 (narrow the 34-file review?) | OPEN, not decided | Stays with Michael, due S3 start; AC-3.1 works under either answer |

**Canonical numbers now (re-run after all edits, 2026-09-20, worktree root, before any migration)**: `guard-scope hits 91 files 31` with `pin 20 stamp 52 prose 19`. Replaces the Revision 3 values (`pinned-id hits 14 files 6`; AC-1.2c value 70; 8 prose lines in 2 files), which counted a narrower contract with exemptions.

**Commands run for this revision**: canonical count (above) extracted from this file and executed; guard fixtures in Python `re` and `grep -E` against a simulated `scripts/` directory (`fixture failures 0 []`); AC-1.1b on a compliant sample and on today's file; AC-1.6 (`0 []`); AC-2.1 (`25 source lines still present`); AC-3.3a (`36 violations`); AC-4.6 (`9 [...] violations 0`); AC-5.10 on the real capture copied into a scratch fixture path (`OK`); real `claude -p ... --output-format stream-json --verbose` capture and read-back; `parse_stream` on it (`['unknown']`, `0.0`); `check_skill_budgets.py` (`exit=0`); `validate_constraints.py` on constraints.yml (valid, rc=0); `grep` counts: workflow guard file 6, AC-1.3 0 and 0, AC-4.5 0, `fitness_review_due` 11 files, `model:`/`phase_1_detector_model:` 9 lines. The raw stream capture and all scratch scripts are under `/tmp` and are not part of the repository.

**Unverified claims (not shipped; carried as OQs)**: `haiku` alias is "latest" (OQ-6); Claude Code default effort (OQ-8); literal-instruction-following comparison (OQ-2); existence of any API `-latest` alias (treated as absent); stability of the `stream-json` shape across CLI versions (R11).

## 17. Revision 5 changelog

Inputs: Team DoD validation round 1 (`dod/qa-review.md` NOT_DONE, 3 blocking; `dod/architect-review.md` DONE, 9 warnings; `dod/developer-review.md` DONE; `dod/po-review.md` DONE, 4 warnings). Design unchanged (latest-version references, no pins). Every disposition below was checked by running a command on 2026-09-20 in the worktree root, or by running the snippet as it is written in this PRD (each AC snippet was extracted from this file and executed; the guard-dependent ones against a simulated `scripts/` directory under `/tmp`, since S1 has not landed). Dispositions: FIXED (text and AC changed), REBUTTED (executed evidence, no change), DEFERRED (owner, due, why non-blocking).

### QA (3 blocking, all FIXED)

| # | Finding | Disposition | Where and evidence |
|---|---------|-------------|--------------------|
| QA-1 (blocking) | AC-1.2a asserts only must-hit floors; PRD-named strings not required in the fixture file | FIXED | AC-1.2a asserts `rule_a_must_pass` >= 10 and `rule_b_must_pass` >= 12 and a `REQ` table of PRD-named strings that MUST be present in each list (`run haiku 3 times`, `Section 5.5`, `Replace C12 with 4.7uF or greater`, `model = "claude-opus-fixture"`, etc.). Executed: `fixture failures 0 []`. Mutation checks: PROSE_RE replaced by `.` printed `fixture failures 32 [...]`; deleting the `rule_b_must_pass` key raised KeyError; both would have passed silently under Revision 4 |
| QA-2 (blocking) | Real false positives (`Sonnet 4 stories`, `use Opus 2 times for review`, `in 5.0 seconds`, `for 4.5 hours`) hit PROSE_RE/BARE_RE and the ban on `model-pin-ok` meant they could never ship | FIXED | New COUNT_RE (FR-1.2) blanks a family word plus integer plus count noun, and a context word plus decimal plus time/size unit, before Rule B; the noun and unit lists exclude words that can follow a real version. Both engines: Python `re`, and `sed -E` piped into `grep -E`. All QA-probed strings (`Sonnet 4 stories`, `use Opus 2 times for review`, `the Opus 3 reviewers`, `in 5.0 seconds`, `for 4.5 hours`, `ship in 4.5 days`) are must-pass fixtures; real-version sentences still hit (executed: `Opus 5 delegates more readily`, `the 4.7 tokenizer`, `on 4.7 runs faster`, `in 4.5 hours on 4.7 semantics` all hit; `wait 4.5 seconds` passes). The marker is removed (FR-1.6), and the wording rule in FR-1.2 says how a sentence is reworded. Canonical numbers unchanged (below) |
| QA-3 (blocking) | BINDING-4.5 separation weakly observable | FIXED | FR-4.4 now has five independent observations and AC-4.4 checks 1 to 3 by script: separate commits; disjoint non-empty `Dispatch-Id` trailer sets for `lib/` commits and validator commits; `lib/` unchanged from `validator_start` to `validator_end` (start AND end) and clean at the end. Observation 4, AC-5.9b: the `real_shape` test MUST FAIL (exit 1, not 5) against the unfixed parser, run against an export of `main`, then pass on the branch. Executed today: AC-4.4 fails at its first assertion (no S5 commits yet, expected). Side-effect improvement: the S5 meta-tests move to a new `tests/test_model_capture.py`, because `test_meta.py` states a contract of exactly 3 test functions (its docstring, AC-S3-08) that new tests would break; BC-07 updated |
| QA-4 (warning) | AC-5.5 and AC-5.4 satisfiable by hand-edited baseline JSON | FIXED (honest limit stated) | AC-5.5c: `samples` in the baseline, raw trimmed streams under `.delivery/artifacts/06-development/smoke-streams/`, an independent script re-hashes each stream and checks the `system/init` model and `total_cost_usd` mean against the baseline. Fabricating the streams as well still passes; recorded as a limit, not hidden. Executed today: fails with the expected assertion |
| QA-5 (warning) | Guard fixtures lack provenance | FIXED | Fixture file has a `provenance` object; AC-1.2a asserts every fixture string has an origin in `challenger`, `qa-probe`, `repo-line`, `synthetic`, `synthetic-future` |
| QA-6 (warning) | AC-2.1 and AC-2.5 floor-only; AC-2.1 confuses duplicate lines | FIXED | AC-2.1 counts occurrences (a `Counter`); AC-2.5 requires `dod_validators`, a cap word and "subagent" in ONE added line plus a separate conditional "latest Opus" line, so keyword salad across lines fails; AC-2.3b adds the required line `AC-2.1/2.5 intent verdict: PASS|FAIL` in the adversarial artifact. The semantic judgement stays with the adversarial reviewer (stated) |
| QA-7 (warning) | AC-5.2 lacks the WARN literal | FIXED | AC-5.2: literal `WARN missing thinking_tokens`, `WARN missing stop_details.refusal_code`, `WARN missing speed_or_fast_indicator`, three named tests, check `... -k warn_missing -v \| grep -c PASSED` prints 3 |
| QA-8 (warning) | AC-3.3a accepts today as `fitness_review_due` | FIXED | `fitness_review_due` must be `> today` and `<= today + 90 days` (governance: "advance by 90 days"); `last_audited` must be between 2026-09-20 and today; dates from `datetime.date.today()`. Executed: `36 violations` today |
| QA-9 (warning) | AC-1.1b matches `- main` under `pull_request:` | FIXED | AC-1.1b parses the `push:` block only, accepts quoted or unquoted `main`, flow or block lists, and carries four self-test workflows (two compliant, two with `main` only under `pull_request` or push on another branch). Executed: self-tests pass, compliant sample prints `OK`, today's file fails as stated |
| QA-10 (warning) | No negative tests for AC-1.6 and AC-DISP | FIXED | AC-1.6b (a pin carrying the old marker text is still flagged: executed `1 guard-scope hits 1 files 1`); AC-DISP has an inline self-test with a bad and a good manifest; AC-1.1b self-tests above |

### Architect (9 warnings)

| # | Finding | Disposition | Where and evidence |
|---|---------|-------------|--------------------|
| A-1 | Guard self-scan feasible | No change | Recorded; the executed canonical count on the Revision 5 patterns is unchanged |
| A-2 | Pre-commit hook blocks S1 to S3 WIP commits | FIXED | FR-1.5: hook runs `--paths <staged files>`, advisory by default, blocking only with `MODEL_PIN_STRICT=1`; the strict gate is the ship step (FR-7.3). AC-1.5 checks both strings in the hook |
| A-3 | Cost cap cannot fire on the real stream | FIXED | S5 scope paragraph and FR-5.4: layer 1 `--max-budget-usd <cost-cap>` (verified in local `claude --help`), layer 2 `_running_cost` reads `total_cost_usd`; AC-5.4b (command line contains `--max-budget-usd 3.00`, `--model opus`, `--effort xhigh`; `_running_cost` equals the fixture cost); `runner.py` added to producers (FR-4.4, BC-07) |
| A-4 | Baseline comparison keyed on dynamic `model_usage` keys | FIXED | FR-5.7: `model_usage.*` excluded from per-key threshold comparison; AC-5.7 cases (i) to (iii) incl. different model keys with `--strict-model` unset |
| A-5 | Plumbing of new fields unstated | FIXED | S5 scope paragraph lists `metrics.py`, `runner.py`, `report.py`, `aggregator.py`, `baseline.py`, `run_smoke.py` and says the new fields are copied top-level, not aggregated as numeric metrics |
| A-6 | Provenance sidecar and S5 docs inside guard scope | FIXED | FR-5.10: sidecar records command, CLI version, date only, never a model ID; docs use synthetic examples; AC-5.10 asserts the sidecar has no versioned ID (executed on a scratch copy of the real capture: `OK`) |
| A-7 | Fingerprint not in FR-7.3; mirror scope unstated | FIXED | FR-7.3 step (5) runs AC-6.1 before the push; FR-6.2 and AC-6.2 require the ADR to state whether `orchestrator-doctrine.md` is in scope |
| A-8 | `model-pin-ok` unusable and asymmetric | FIXED | Marker removed entirely (FR-1.6, AC-1.6a and AC-1.6b); wording rule in FR-1.2 |
| A-9 | Tracked-tree versus `os.walk` scope | FIXED | Guard scope and canonical command both use `git ls-files --cached --others --exclude-standard` (untracked files included); executed: the simulated script's `--list` equals the canonical listing (91 lines) |
| A-10 | Story order sound; `git show main:` ACs are pre-ship | FIXED (note) | FR-7.3 step (0) and AC-2.1, AC-2.5, AC-4.4, AC-5.9b marked PRE-SHIP |
| A-11, A-12 | OQ-11 confirmed; `xhigh` and no `--bare` acceptable | No change | OQ-9 and OQ-12 stay OPEN for Michael (not decided) |

### Developer (findings 1 to 8) and the two commands the validator could not run

| # | Finding | Disposition | Where and evidence |
|---|---------|-------------|--------------------|
| D-1 | AC-DISP has no runnable snippet | FIXED | AC-DISP is a real script; a required stage with no manifest is a violation (no vacuous pass). Executed: `4 violations` today |
| D-2 | Shared `/tmp/walk.py` fragile | FIXED | No AC or canonical command reads a `/tmp` file; a five-line `files()` helper is inline in each walking snippet; guard-dependent snippets read `scripts/check_model_pins.py` by relative path |
| D-3 | AC-1.1b loose | FIXED | See QA-9 |
| D-4 | AC-4.5 unquoted glob, walks nested dirs | FIXED | `--include='*.py' --exclude-dir=.git --exclude-dir=.delivery --exclude-dir=worktrees`; executed: 0 |
| D-5 | AC-4.2 two commands, inline comment | FIXED | Split into two commands, non-capturing group; executed: `False 4` today, `3 passed` for the meta-tests |
| D-6 | `validate_constraints.py` not run by the validator | RUN | `python3 delivery-team/skills/delivery-flow/scripts/validate_constraints.py .delivery/artifacts/02-refine/po/constraints.yml` printed `ok: .delivery/artifacts/02-refine/po/constraints.yml is valid against constraints schema`, rc=0, both before and after the Revision 5 constraints edit (final run recorded in the report) |
| D-7 | "0.4 s" timing not reproduced | FIXED | NFR-13: 0.5 s measured here, about 1.2 s on the Developer host; both far under 10 s |
| D-8 | Fixtures sound; `rev-1.2` hits | Noted | `pattern_library_version: rev-1.2` is a hit by STAMP_RE (dotted revision), intended |
| D-9 | NFR-8 check not run by the validator | RUN | `git diff main -- .github \| grep -c "pip install"` printed `0` (grep exits 1 on a zero count) |

### PO (4 warnings)

| # | Finding | Disposition | Where and evidence |
|---|---------|-------------|--------------------|
| P-1 | Idea brief stale, no supersession note | FIXED at PRD level | Reader's guide at the top of this PRD names the brief as superseded and points downstream stages at the PRD and memory topic; the brief itself is not edited (immutable, AC-7.5) |
| P-2 | NFR-11 inspection-only | FIXED | NFR-11 now has an executable part: AC-1.2a requires >= 3 `synthetic-future` must-hit strings flagged by the unchanged patterns |
| P-3 | Historical versions in memory and backlog | Noted | Reader's guide: they sit under `.delivery/`, excluded from the guard, history not leftovers |
| P-4 | PRD length | FIXED (navigation) | Reader's guide names sections 1, 3, 5, 8 as the entry points; revision history stays at the end |

### Canonical numbers now (Revision 5 command, worktree root, 2026-09-20, before any migration edit)

`guard-scope hits 91 files 31`, `pin 20 stamp 52 prose 19`, listing identical to Revision 4. AC-1.2c pre-migration value unchanged (91 files 31); AC-3.1b equivalent `69 19` (69 SKILL.md hit lines, 19 files with `frontmatter-only`); AC-2.1 `25`; AC-3.3a `36 violations`; stamp census `skill 34` / `26 25 {...19, ...7}` / `26 x 4-7-1`.

**Still OPEN, not decided here**: OQ-9 (narrow the 34-file review) and OQ-12 (`--bare`), both Michael, both non-blocking with defaults.

**Commands run for this revision**: canonical count and stamp census extracted from this file and executed; AC-1.2a extracted and executed in a scratch `scripts/` directory with 29/12/21/16 fixtures (`fixture failures 0 []`) plus two mutation runs; AC-1.1b (self-tests, compliant sample `OK`, today's file assertion); AC-1.6a (`0`) and AC-1.6b (`1 guard-scope hits 1 files 1` on the simulated script); AC-2.1 (`25`), AC-2.3 (`0`), AC-2.5 (`FAIL`), AC-3.1 (FileNotFoundError), AC-3.1b on the simulated script (`69 19`), AC-3.2, AC-3.3a (`36 violations`), AC-4.2 (`False 4`), AC-4.4 (assertion, no S5 commits), AC-4.5 (`0`), AC-4.6 (`9 [...] violations 0`), AC-5.5c (assertion, no `samples`), AC-5.10 on a scratch copy of the real capture (`OK`), AC-DISP (`4 violations`); `validate_constraints.py` (valid, rc=0); NFR-8 `pip install` count (`0`); `pytest test_meta.py` (`3 passed`); local `claude --help` for `--max-budget-usd`, `--model`, `--effort`. Nothing ran the `claude` model or spent money. Scratch scripts are under `/tmp/rx` and are not part of the repository.

— Gandalf, PO, run-2026-05-28-backlog-108.

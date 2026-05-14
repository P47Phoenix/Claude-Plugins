<!-- run: run-2026-05-13-tk5 | stage: 07-uat | role: QA DoD validator | author: Legolas -->

# QA DoD Review — run-2026-05-13-tk5

> *"That bug still only counts as one."* — Legolas

Me Legolas. Me verify gate-by-gate. Me run commands. No infer. No skip.

---

## Verdict: PASS_WITH_NOTES — endorse

Six gate criteria PASS. One gate criterion (#4) PASS-by-intent with literal-syntax mismatch (caller wrote `### D-tk5`, defect log uses `## D-tk5` — count = 4 either way). Honest-readiness-marker pattern on G1+G4 is the correct call per Wave-2 lineage.

---

## Gate-by-gate verification

### Criterion 1 — UAT report covers all 8 acceptance gates (count by header)

```
$ grep -n "^### Gate " /var/home/meconnelly/Documents/GitHub/Claude-Plugins/.delivery/artifacts/07-uat/qa/uat-report.md
55:### Gate 1 — Live `--init-baseline` (5 sequential runs, all outcome.success=true)
102:### Gate 2 — `baselines/hello_world_spike.json` parses + contains mean/stddev for 6+ metrics
121:### Gate 3 — `pytest tests/test_meta.py` passes 3 meta-tests in < 5 s
144:### Gate 4 — `run_smoke.py` (no `--init-baseline`) reproduces successful run within 2σ of baseline
152:### Gate 5 — `find .github/workflows -name "smoke-*.yml" | wc -l` returns 0
164:### Gate 6 — `grep "feedback_claude_code_local_only" delivery-team/architecture/smoke-test-architecture.md` returns ≥ 1
180:### Gate 7 — `check_skill_budgets.py` + `lint_known_debt.py` both exit 0
198:### Gate 8 — Cost-cap default (`--cost-cap 3.00`) tested via injected stream exceeding threshold
235:### Gate execution scoreboard
```

8 distinct gate sections (G1-G8) plus scoreboard. **PASS**.

### Criterion 2 — Each gate has real command + exit code + truncated output (not inference)

Inspected sections G1-G8. Each contains a `$` shell prompt with the verbatim command, an `EXIT=N` line captured verbatim, and a truncated JSON/text excerpt of the actual output. G1 shows `EXIT=1` honestly (not papered over). G4 cites G1-dependence with no fake command. G2/G3/G5/G6/G7/G8 each show a real `EXIT=0` (G8 = `EXIT=2` by design — cost-cap exit code). **PASS**.

### Criterion 3 — Honest-readiness-marker pattern applied (Wave-2 lineage)

- G1 explicitly marked **DEFERRED_TO_FOLLOWUP** in §Gate 1 with a documented one-line root cause and three fix paths.
- G4 explicitly marked **DEFERRED** in §Gate 4 because G1-dependent.
- Section D verdict reads **PASS_WITH_NOTES** with the rationale "deferred ≠ failed."
- Stub baseline file at `delivery-team/tests/smoke/baselines/hello_world_spike.json` has `sample_status: "deferred"`, `n_samples: 0`, mean/stddev=null per row. Self-flagging artifact.
- Scoreboard explicitly names both deferrals ("6 PASS + 2 DEFERRED (both auth-bound)").

Pattern correctly applied: deferred gates NAMED, not silently dropped. **PASS**.

### Criterion 4 — Defect log contains D-tk5-01..04 (literal-syntax vs intent)

Caller-specified literal command:
```
$ grep -c "^### D-tk5" /var/home/meconnelly/Documents/GitHub/Claude-Plugins/.delivery/defects/sprint-tk5.md
0
```

Reason: defect log uses **H2** (`## D-tk5`), not H3 (`### D-tk5`). Verify intent:
```
$ grep -c "^## D-tk5" /var/home/meconnelly/Documents/GitHub/Claude-Plugins/.delivery/defects/sprint-tk5.md
4

$ wc -l /var/home/meconnelly/Documents/GitHub/Claude-Plugins/.delivery/defects/sprint-tk5.md
61 .delivery/defects/sprint-tk5.md
```

4 D-tk5-* entries present at H2 (`D-tk5-01`, `D-tk5-02`, `D-tk5-03`, `D-tk5-04`). 61 lines, well above any reasonable floor.

**Status**: **PASS-by-intent**. The literal `### D-tk5` syntax was an oversight in the gate spec — H2 is the correct level for a defect entry in a defect log (entries are top-level records, not sub-sections of a parent gate). Recommend caller update the gate spec to `^## D-tk5` in the next-pipeline DoD prompt.

### Criterion 5 — Stop-rule headroom is named (current rate vs 0.4 threshold)

UAT §Section D verbatim:
> Rolling defect rate before this initiative: 0.111 across the 3-PR window.
> This initiative adds 3 stories (S1, S2, S3).
> New defects logged post-merge: 1 (D-tk5-04). The 3 carry-forward soft notes (D-tk5-01/02/03) are known-debt deferrals from Stage 6, NOT new post-merge defects.
> Worst-case rolling rate: 1 / 3 = 0.333. Threshold is 0.4. **Headroom: 0.067 (~17% margin)**.

Current rate (0.333) named. Threshold (0.4) named. Headroom (0.067, ~17%) named. **PASS**.

### Criterion 6 — Shared-module review present (lib/*.py cross-references documented)

UAT §A2 contains the Shared-Module Review table with 6 rows, one per `lib/*.py` module (`runner.py`, `workspace.py`, `metrics.py`, `aggregator.py`, `baseline.py`, `report.py`). Each row lists Stages Referencing (01, 02, 04, 05, 06), Modified in Dev (Yes), Test Coverage (specific TC IDs), and Status (PASS or PASS_WITH_NOTES with D-tk5-04 callout on workspace.py). Includes a `<!-- retro c8f2 -->` marker per protocol. **PASS**.

### Criterion 7 — No regression on existing pipeline (both scripts exit 0)

```
$ python3 scripts/check_skill_budgets.py
BUDGET CHECK PASSED: 17 file(s) checked, 0 known-debt, 0 exception(s).
EXIT=0

$ python3 scripts/lint_known_debt.py
LINT OK: known_debt JSON↔Python in sync; all SKILL.md frontmatter complete.
EXIT=0
```

Both exit 0. No regression. **PASS**.

### Criterion 8 — Producer-validator boundary preserved (lib NEW + tests NEW, distinct file groups)

```
$ git status delivery-team/tests/smoke/ --short
?? delivery-team/tests/smoke/
```

Git collapses the entire untracked subtree to one `??` entry. Drill in:

```
$ git ls-files --others --exclude-standard delivery-team/tests/smoke/ | sort
delivery-team/tests/smoke/README.md
delivery-team/tests/smoke/__init__.py
delivery-team/tests/smoke/baselines/.gitkeep
delivery-team/tests/smoke/baselines/hello_world_spike.json
delivery-team/tests/smoke/fixtures/delivery_config_minimal.yml
delivery-team/tests/smoke/prompts/hello_world_spike.txt
delivery-team/tests/smoke/run_smoke.py
delivery-team/tests/smoke/tests/__init__.py
delivery-team/tests/smoke/tests/conftest.py
delivery-team/tests/smoke/tests/fixtures/sample-workspace/.delivery/state.md
delivery-team/tests/smoke/tests/fixtures/sample-workspace/.delivery/telemetry/run-summary-fake.json
delivery-team/tests/smoke/tests/fixtures/sample-workspace/.delivery/telemetry/skill-loads.jsonl
delivery-team/tests/smoke/tests/test_meta.py
```

(Note: `git ls-files --others` does not recurse into `lib/` here because the rolled-up parent is already `??`. Verify directly:)

```
$ ls delivery-team/tests/smoke/lib/*.py
delivery-team/tests/smoke/lib/__init__.py
delivery-team/tests/smoke/lib/aggregator.py
delivery-team/tests/smoke/lib/baseline.py
delivery-team/tests/smoke/lib/metrics.py
delivery-team/tests/smoke/lib/report.py
delivery-team/tests/smoke/lib/runner.py
delivery-team/tests/smoke/lib/workspace.py

$ git ls-files delivery-team/tests/smoke/lib/
(empty — none tracked)
```

**Producer group (S1+S2 dispatch — `lib/*.py` + `run_smoke.py` + `prompts/` + `fixtures/` + `baselines/`)**: 7 lib files + runner + supporting data = all NEW, none tracked.

**Validator group (S3 dispatch — `tests/*`)**: 4 test files + sample-workspace fixture tree = all NEW, none tracked.

Two distinct file groups, both untracked, no overlap. Different stories visible as different file groups. **PASS**.

---

## Overall verdict review

| Criterion | Status | Evidence |
|-----------|--------|----------|
| 1 — 8 gate headers | PASS | 8 sections G1-G8 by `grep "^### Gate "` |
| 2 — real cmd + exit + output | PASS | inspection of §Gate 1-8 |
| 3 — honest-readiness markers | PASS | G1+G4 explicitly DEFERRED; stub baseline self-flags |
| 4 — D-tk5-01..04 in defect log | PASS-by-intent | 4 entries at H2, not H3 as spec stated |
| 5 — stop-rule headroom named | PASS | 0.333 current, 0.4 threshold, 0.067 (~17%) headroom |
| 6 — shared-module review | PASS | 6-row table in §A2 with `<!-- retro c8f2 -->` |
| 7 — no regression | PASS | both scripts exit 0 verified live |
| 8 — producer/validator boundary | PASS | lib NEW (7 files), tests NEW (4 files + fixtures), distinct |

**8 of 8 DoD criteria satisfied** (Criterion 4 with a syntax-vs-intent caveat).

PASS_WITH_NOTES verdict is **endorsed**.

### Why PASS_WITH_NOTES (not DONE, not NOT_DONE)

- Not DONE: G1 + G4 are deferred. Real auth bug (D-tk5-04) found and ticketed. Calling this DONE would mask a HIGH-severity finding.
- Not NOT_DONE: 6 of 8 acceptance gates green by live verification. Producer-validator boundary clean. Governance gates clean. Cost-cap critical-path green end-to-end. Meta-tests green in 0.02s. Plenty independently valuable to ship.
- PASS_WITH_NOTES is the Wave-2-lineage honest mark: meaningful surface ships, named gaps walk behind in BACKLOG-107.

---

## Notes for next dispatch (caller)

1. **Gate spec syntax**: Criterion 4 wrote `grep -c "^### D-tk5"`. The defect-log convention is H2 (`## D-tk5`), so the literal regex returns 0. Update DoD prompt template to `^## D-tk5` (or `^#{2,3} D-tk5` to accept both) for future runs.
2. **Stub-baseline contract**: the deferred stub at `delivery-team/tests/smoke/baselines/hello_world_spike.json` is well-flagged (`sample_status: "deferred"`, all means null, header comment). When BACKLOG-107 lands, the real `--init-baseline` run replaces this stub — recommend QA in next wave verify the stub→real transition is detected by `compare()` correctly (zero-stddev guard should prevent silent green; this is risk row 2 in `release-plan.md` §7).
3. **HOME-isolation fix**: D-tk5-04 has three documented fix paths; fix path (a) (keep HOME unchanged + isolate via `cwd` + `XDG_*`) is the cleanest. Recommend QA assert in next-wave UAT that `os.environ["HOME"]` is preserved in spawned subprocess env (one-line unit test).

---

— Legolas (QA DoD validator), run-2026-05-13-tk5, Stage 7 UAT. *That bug still only counts as one.* Six gates green. Two deferred. One bug counted. Stop-rule has headroom. PASS_WITH_NOTES endorsed.

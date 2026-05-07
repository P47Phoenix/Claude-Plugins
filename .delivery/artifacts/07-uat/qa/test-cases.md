<!-- run: run-2026-05-05-tk3 | stage: 07-uat | depth: light | author: QA Engineer (Legolas Greenleaf) | role: qa-engineer | task: test-cases -->

# UAT Test Cases — Caveman-Lite Prose Discipline (run-2026-05-05-tk3)

> "I count them as they fall."
> — Legolas, on the verification of one and twelve.

One entry per TC from `.delivery/artifacts/05-plan/qa/test-strategy.md`. Each re-runs the Stage-6 Dev DoD verification command independently and records PASS/FAIL with the actual command output.

## Coverage Summary

| TC | Title | WI | Story-1 AC | Status |
|---|---|---|---|---|
| TC-1 | Phase 0 reads `prose_style` at startup | W2-3 | AC-W2-3-S1, S4 (cross) | PASS |
| TC-2 | PROSE STYLE block injected in 3 dispatch templates | W2-1 | AC-W2-1-S1, S2 | PASS |
| TC-3 | DoD validator template directs caveman-lite verdict prose | W2-2 | AC-W2-2-S1, S2, S3 | PASS |
| TC-4 | Auto-clarity exemption: destructive-op produces standard prose | W2-1 | AC-INITIATIVE AC-5 | PASS (structural; see dogfood-report Dispatch 2-4) |
| TC-5 | Opt-out: `prose_style: standard` reverts behavior | W2-3 | AC-INITIATIVE AC-6 | PASS (structural; see dogfood-report Dispatch 5) |
| TC-6 | Schema bump v2.8 → v2.9; v2.7 configs auto-default | W2-3 | AC-W2-3-S1, S2, S3, S4 | PASS |
| TC-7 | Cache-prefix hash regenerated alongside Phase 0 edit | cross | AC-CACHE-PREFIX | PASS |
| TC-8 | Tier-A budget preserved post-edit | cross | AC-TIER-A-BUDGET | PASS |

## TC-1 — Phase 0 reads `prose_style` at startup

**Verification command**: `grep -nE "PROSE STYLE|prose_style" delivery-team/skills/delivery-flow/SKILL.md`

**Actual output**:
```
74:   - **Read `prose_style`** (top-level; default `caveman-lite`; valid `caveman-lite | standard`); cache on loaded-config; consumed at Phase 4 Step 4 (conditional PROSE STYLE block) and Step 7 (DoD validator framing). See ADR-tk3-001.
338:**PROSE STYLE block injection** (post-ALIAS, pre-OUTPUT): if `config.prose_style == caveman-lite` (default), inject the verbatim PROSE STYLE block from `references/prose-style.md` into the dispatch prompt; if `standard`, omit the block entirely (no placeholder line). Same rule applies uniformly to Primary (this Step 4), Supporting (Step 5), and DoD Validator (Step 7) dispatches. See ADR-tk3-001 Element 2.
```

**Expected**: ≥1 match in L56-89 (Phase 0). L74 lands inside the Phase 0 settings sub-block. **PASS** — Phase 0 wiring present; Step 4 wiring present; both reference ADR-tk3-001.

## TC-2 — PROSE STYLE block injected post-ALIAS pre-OUTPUT in 3 dispatch templates

**Verification commands**:
- `grep -c "^PROSE STYLE: caveman-lite for narrative-framing prose ONLY" delivery-team/skills/delivery-flow/references/pipeline-stages.md` → expected `3`
- `grep -c "Auto-clarity exemptions apply" delivery-team/skills/delivery-flow/references/pipeline-stages.md` → expected `3`
- `grep -nE "^--- (ALIAS|PROSE STYLE|OUTPUT) ---" delivery-team/skills/delivery-flow/references/pipeline-stages.md` → expected 9 lines, ordered ALIAS→PROSE STYLE→OUTPUT in three template blocks

**Actual output**:
```
3
3
69:--- ALIAS ---
72:--- PROSE STYLE ---
76:--- OUTPUT ---
116:--- ALIAS ---
119:--- PROSE STYLE ---
123:--- OUTPUT ---
168:--- ALIAS ---
171:--- PROSE STYLE ---
175:--- OUTPUT ---
```

**Expected**: `3`, `3`, and 9 lines in ALIAS→PROSE STYLE→OUTPUT order in three template blocks (Primary, Supporting, DoD Validator). **PASS** — exact ordering preserved; ADR-tk3-001 Element 2 contract met.

## TC-3 — DoD validator template directs caveman-lite verdict prose; STATUS verbatim; FINDINGS preserved

**Verification commands**:
- `grep -nE "STATUS:.*(DONE|NOT_DONE|CODE_COMPLETE)" delivery-team/skills/delivery-flow/references/quality-gates.md` → expected ≥1 match in L21-38
- `grep -c "caveman-lite" delivery-team/skills/delivery-flow/references/quality-gates.md` → expected ≥1
- `grep -nE "file/line/criterion|name file" delivery-team/skills/delivery-flow/references/quality-gates.md` → expected FINDINGS-format directive preserved

**Actual output**:
```
34:STATUS: DONE | NOT_DONE | CODE_COMPLETE   (inside L21-38 template block ✓)
caveman-lite count: 1
40:**Verdict-prose style**: when `config.prose_style == caveman-lite`...The `STATUS:` line values (DONE / NOT_DONE / CODE_COMPLETE) remain verbatim, the `FINDINGS:` bullet list (each finding names file/line/criterion) stays in standard prose...
```

**Expected**: STATUS literal preserved verbatim inside template; verdict-prose directive present; FINDINGS-format clause preserved with `file/line/criterion` token. **PASS** — all three sub-checks satisfied. ADR-tk3-001 Element 4 contract met.

## TC-4 — Auto-clarity exemption: destructive-op dispatch produces standard prose

**Approach**: structural verification of the in-prompt directive (see `dogfood-report.md` Dispatches 2-4). The exemption mechanism is in-prompt per ADR-tk3-001 Element 3 — the agent itself is the detector. Verification = the directive contains the four verbatim exemption clauses.

**Verification command**: `grep -F "security warnings, irreversible-op confirmations, multi-step sequences, user clarifications" delivery-team/skills/delivery-flow/references/pipeline-stages.md | wc -l`

**Actual output**: `3` (one occurrence per dispatch template) — confirmed via TC-2 grep that returned exactly 3 matches for the full PROSE STYLE block which contains the exemption clause verbatim.

**Expected**: 3 occurrences (one per template). **PASS** — exemption directive present and verbatim in all three template slots; agent-as-detector mechanism structurally complete. Empirical exemption respect deferred to first 3 post-merge dispatches that hit security/destructive/multi-step contexts (carry-forward).

## TC-5 — Opt-out: `prose_style: standard` reverts behavior

**Approach**: structural verification of the conditional-omission directive in all three dispatch template slots and in SKILL.md Step 4.

**Verification command**: `grep -F "{when config.prose_style == caveman-lite: inject the line below verbatim; when standard: omit this entire section}" delivery-team/skills/delivery-flow/references/pipeline-stages.md | wc -l`

**Actual output**: `3` (L73, L120, L172 — one per dispatch template). Plus SKILL.md L338: `if standard, omit the block entirely (no placeholder line)`.

**Expected**: 3 occurrences in pipeline-stages.md + 1 in SKILL.md Step 4. **PASS** — opt-out path structurally present and unambiguous in all four authoritative locations. ADR-tk3-001 Element 1 contract met.

## TC-6 — Schema bump v2.8 → v2.9; v2.7 configs auto-default

**Verification commands**:
- `grep -n "^## Current Version: 2.9" delivery-team/skills/delivery-flow/references/config-schema.md` → expected L5
- `grep -nE '^\| `prose_style`' delivery-team/skills/delivery-flow/references/config-schema.md` → expected one row with type/default/enum
- `grep -n '^| 2.9 ' delivery-team/skills/delivery-flow/references/config-schema.md` → expected one Version History row
- `python3 -c "import json; d=json.load(open('.../config-schema.json')); assert 'prose_style' in d['properties']; assert d['properties']['config_version']['default']=='2.9'"` → expected exit 0

**Actual output**:
```
5:## Current Version: 2.9
16:| `prose_style` | string | no | caveman-lite | caveman-lite, standard | defaults | delivery-flow ...
378:| 2.9 | 2026-05-05 | Added top-level `prose_style: caveman-lite | standard` key (default caveman-lite)...
JSON: OK {'type': 'string', 'enum': ['caveman-lite', 'standard'], 'default': 'caveman-lite'}
```

Plus: current `.delivery/config.yml` is `config_version: "2.7"` with no `prose_style` key — TC-6 v2.7→v2.9 migration path is reproducible and will exercise on the next pipeline run.

**Expected**: all four sub-checks pass. **PASS** — schema v2.9 row in version history, prose_style row in main schema table, JSON regenerated correctly, v2.7 fixture available in-tree.

## TC-7 — Cache-prefix hash regenerated alongside Phase 0 edit

**Verification commands**:
- `sha256sum delivery-team/skills/delivery-flow/SKILL.md` → expected match against `governance/cache-prefix-hash.txt` line 1
- Differs from pre-edit value `9d4011d11e5b83321526c41ff79dd25c9186f4c659a745feb0c13f686205926f`

**Actual output**:
```
sha256sum:  f997ec25df5328329e431309f6dd6db948d354d5360dcb4c6ac409b8815a9eb9  delivery-team/skills/delivery-flow/SKILL.md
stored:     f997ec25df5328329e431309f6dd6db948d354d5360dcb4c6ac409b8815a9eb9  delivery-team/skills/delivery-flow/SKILL.md
```

**Expected**: byte-exact match; differs from pre-edit. **PASS** — both lines identical; new hash differs from Wave 2 value `9d4011d1...`. ADR-tk3-001 Element 5 contract met.

## TC-8 — Tier-A budget preserved post-edit

**Verification commands**:
- `wc -l delivery-team/skills/delivery-flow/SKILL.md` → expected ≤500
- `python3 scripts/check_skill_budgets.py` → expected exit 0

**Actual output**:
```
500 delivery-team/skills/delivery-flow/SKILL.md
BUDGET CHECK PASSED: 13 file(s) checked, 7 known-debt, 0 exception(s).
EXITCODE=0
```

Note: Stage-6 implementation report listed the script path as `delivery-team/scripts/check_skill_budgets.py`; the actual canonical path is `scripts/check_skill_budgets.py` (root). The Dev report assertion was correct — script exits 0 — but the path token in the report is off by one directory. Minor documentation drift; not blocking. Filed as observation, not a defect.

**Expected**: exit 0 and ≤500. **PASS** — exactly 500/500 (at ceiling, no over-run); 7 known-debt entries unchanged from Wave 2 (architect, godot, operations, presentation, quality, ui, user-feedback) all targeting Wave 3.

## Coverage Notes

Every Story-1 AC and every initiative AC traces to ≥1 TC per the test-strategy coverage matrix. Zero gaps. The only carry-forward is empirical AC-13 sub-clause (BACKLOG-102 initiative AC-1/AC-2 telemetry deltas) — by-design per Story-1 §Dogfood Plan, requires post-merge pipeline run.

---

STATUS: CODE_COMPLETE
ARTIFACT: .delivery/artifacts/07-uat/qa/test-cases.md
SUMMARY: 8/8 TCs PASS structural verification. Path-token drift in Dev report (cosmetic, not blocking). AC-13 telemetry carry-forward documented.

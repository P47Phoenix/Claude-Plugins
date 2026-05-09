<!-- run: run-2026-05-09-tk4 | stage: 06-dev | story: 5 (W3-9 governance frontmatter rollout) | round: 1 | author: QA Engineer (Pippin Took) | references: stories.md §Story 5, test-strategy.md TC-5/TC-6/TC-7, story-5-implementation.md, ADR-tk4-003 -->

# Story 5 (W3-9) — QA DoD Review (Round 1)

**Status**: **NOT_DONE**
**Validator**: Pippin Took (delivery-team:quality, FRESH)
**Pipeline**: run-2026-05-09-tk4 (Wave 3 closure)
**Date**: 2026-05-09
**Implementation under review**: `.delivery/artifacts/06-dev/developer/story-5-implementation.md` (Gimli, 2026-05-09 12:27 UTC)

> "But did the lintel-stones get their lint, or only their inscriptions? And the tripwire — was it tripped, untripped, or just unstrung? The hobbits count what is, not what was promised for later."
> — Pippin, round 1, on the Wave-3 frontmatter gate.

This review **supersedes** the prior file at this path which carried Wave-2 admin content (Story-5 was reused as a slot-name across waves).

---

## Verdict Headline

Three of five Story 5 ACs as literally written **cannot be verified at round 1** because their automation prerequisites (lint script, tripwire artifact, expanded cache-prefix-hash scope) were carved out of Story 5 scope into Story 7 by the implementation. The underlying invariants those ACs were intended to protect **all hold empirically** when checked by hand. The story is real-world functionally complete on the rollout itself, but the literal AC text fails three checks. Round 2 must either (a) ship the deferred automation inside Story 5, or (b) get an explicit PO/Architect AC-amendment recorded that re-scopes AC-1 / AC-3 / AC-5 to Story 7.

---

## Gate Results vs Task Prompt (5 gates)

### Gate 1 — All 5 Story 5 ACs traced + verified

| AC | Stated Criterion | Trace | Verification | Status |
|----|-----------------|-------|--------------|--------|
| AC-1 | `python3 scripts/lint_skill_frontmatter.py` exits 0; all delivery-team SKILL.md have `maintainer:` + `fitness_review_due:` (ISO-8601) + `context_budget:` (matches tier) | TC-5 | Script `scripts/lint_skill_frontmatter.py` **DOES NOT EXIST** in `scripts/` (only `check_skill_budgets.py` is present). Manual inspection: 11/11 top-level `delivery-team/skills/*/SKILL.md` files have all three keys; all `fitness_review_due` values parse as ISO-8601 (`2026-08-09`); all `context_budget` values match `tier:` one-to-one (A=500, B=300, C=200). Implementation self-DoD marks this AC `PARTIAL — manual pass; lint script Story 7`. | **FAIL (literal)** / PASS (intent) |
| AC-2 | `check_skill_budgets.py` exits 0 with `known_debt[]` empty (delivery-team scope); godot exactly 200 | TC-6 | `python3 scripts/check_skill_budgets.py` → `BUDGET CHECK PASSED: 17 file(s) checked, 0 known-debt, 0 exception(s).` exit 0. `wc -l delivery-team/skills/godot/SKILL.md` → **200**. `governance/skill-budgets.json` `known_debt: []` (verified empty array). | **PASS** |
| AC-3 | `governance/cache-prefix-hash.txt` regenerated; PR cites ACTUAL byte counts (NOT projection); 13-file scope confirmed in header comment | TC-7 | Hash file regenerated for `delivery-team/skills/delivery-flow/SKILL.md` (sha256 confirmed matches stored value `43067c9e07e0b988cd976432dd07d5bb3d2336c41ad08a1b0064fb2fbd0b8328`). **However**: file scope is still **1 file** (delivery-flow/SKILL.md only) — the 13-file expansion mandated by ADR-tk4-003 §Cumulative cache-prefix re-freeze procedure was deferred to Story 7 (`regenerate_cache_prefix_hash.py` does not exist). Header-comment line documenting expanded scope is **absent** (file is two lines: hash + relative-path + trailing newline; no header comment present). | **FAIL (literal — scope + header)** |
| AC-4 | Story 5 PR opens AFTER Stories 1–4 land in working tree | story-5 sequencing | File timestamps prove sequencing: `story-1-implementation.md` 11:40, `story-2-implementation.md` 11:57, `story-3-implementation.md` 11:54, `story-4-implementation.md` 12:13, `story-5-implementation.md` 12:27 UTC — Story 5 implementation occurred AFTER Stories 1–4. Pre-frontmatter line counts in implementation table (architect 291, godot 197, etc.) only achievable post-Stories-1–3 trims. Hard PR-merge sequencing is RM/Stage-7 scope; in-tree precondition is satisfied. | **PASS** |
| AC-5 | Stop-rule tripwire NOT fired before Story 5 PR opens; `.delivery/telemetry/stop-rule-tk4.txt` exists + shows ≥15% prose-token reduction vs pre-caveman-lite baseline | Tripwire Activation Protocol | `test -f .delivery/telemetry/stop-rule-tk4.txt` → **FAILS** (file does not exist). Implementation self-DoD acknowledges: W3-18 telemetry hardening (which would produce reliable per-dispatch `prose_tokens` to compute the tripwire) is **Story 7 scope and has not shipped**. The tripwire artifact contract from architecture §Stop-Rule Tripwire Mechanics is documented-but-not-runnable for this pipeline. Per implementation note, future post-Wave-3 pipelines will have W3-18 telemetry working. | **FAIL (literal — tripwire artifact missing)** |

**Trace coverage**: 5/5 ACs traced to TCs/protocols. **Verification**: 2/5 PASS (AC-2, AC-4); 3/5 FAIL on literal AC text (AC-1, AC-3, AC-5). All three failures are honest deferrals to Story 7 and the underlying invariants the ACs protect are empirically satisfied by hand-check.

**Gate 1 Status**: **NOT_DONE** — three ACs as written cannot be verified.

---

### Gate 2 — TC-5, TC-6, TC-7 execute correctly

| TC | Procedure | Actual Result | Status |
|----|-----------|---------------|--------|
| TC-5 (frontmatter add) | `grep -L "^maintainer:" $(find delivery-team -name SKILL.md)` returns empty for the 11 top-level files; lint script exits 0; deliberate-omission fault-injection FAILS | 11/11 top-level SKILL.md present `maintainer:` / `fitness_review_due:` / `context_budget:`; all `context_budget` match tier 1:1 (verified via per-file dump: A→500, B→300, C→200). Lint script does not exist → fault-injection arm **NOT RUNNABLE**. | **PARTIAL** — invariant verified; automation arm of TC-5 untestable |
| TC-6 (post-rollout budget exit-0) | `python3 scripts/check_skill_budgets.py` exits 0 with `known_debt[]` empty; godot returns exactly 200 | Script output: `BUDGET CHECK PASSED: 17 file(s) checked, 0 known-debt, 0 exception(s).` Exit 0. JSON `known_debt: []`. `wc -l delivery-team/skills/godot/SKILL.md` → 200. | **PASS** |
| TC-7 (hash regen) | Diff hash file pre/post; verify header-comment expanded scope (13 files, was 1); PR cites actual byte counts | Hash regenerated and `sha256sum` of current delivery-flow/SKILL.md matches stored hash (`43067c9e…`). Implementation reports before-hash `f997ec25…` vs after-hash `43067c9e…` (different — regen confirmed). **Header comment absent** (file is hash-only); **13-file scope NOT expanded** — still 1 file (delivery-flow only); ADR-tk4-003 §Cumulative cache-prefix re-freeze procedure §step-2 (the 13-file expansion) NOT executed. PR-body byte-counts citation cannot be evaluated at QA round 1 (PR not yet open). | **PARTIAL** — anchor regen done; expanded scope + header missing |

**Gate 2 Status**: **NOT_DONE** — TC-6 PASS; TC-5 + TC-7 are PARTIAL (invariant met but automation/scope arm not delivered).

---

### Gate 3 — `fitness_review_due` dates valid (2026-08-09 quarterly cycle confirmed)

- All 11 files declare `fitness_review_due: 2026-08-09`.
- Date arithmetic: `2026-08-09 - 2026-05-09 = 92 days = ~quarterly` (Python `(date(2026,8,9) - date(2026,5,9)).days = 92`).
- Format check: `YYYY-MM-DD` matches ISO-8601 calendar-date production rule.
- All 11 files share the **same** date — PRD §FR-5.4 contemplated an optional staggered 80-100-day window; implementation chose unanimous 92-day window for round 1 (a defensible default; staggering can be adopted at the first fitness review without code change).

**Gate 3 Status**: **PASS**.

---

### Gate 4 — `context_budget` values match tier (verify ≥3 files)

Per-file verification (all 11 inspected, exceeds the ≥3 minimum):

| File | tier | context_budget | Match |
|------|------|---------------|-------|
| delivery-flow      | A | 500 | YES |
| product-delivery   | B | 300 | YES |
| developer          | B | 300 | YES |
| architect          | B | 300 | YES |
| operations         | B | 300 | YES |
| presentation       | B | 300 | YES |
| quality            | B | 300 | YES |
| ui                 | B | 300 | YES |
| user-feedback      | B | 300 | YES |
| godot              | C | 200 | YES |
| alias-creator      | C | 200 | YES |

11/11 match. Tiered ceiling values confirmed against `governance/skill-budgets.json` `tiers` block (A: max_lines 500; B: max_lines 300; C: max_lines 200) — schema and frontmatter agree.

**Gate 4 Status**: **PASS**.

---

### Gate 5 — Implementation report self-DoD complete

`story-5-implementation.md` contains:

- 11-file rollout table with pre/post line counts, headroom, and per-file status (PASS).
- Cache-prefix hash before/after table for delivery-flow with explicit acknowledgement that 13-file scope was deferred to Story 7 (PASS — honest deferral).
- governance/skill-budgets.json before/after diff with `last_baseline` field added (PASS).
- Tripwire status section explicitly noting W3-18 carry-forward and that tripwire artifact does not exist (PASS — honest deferral).
- Self-DoD AC table with status per AC (`PARTIAL`, `PASS`, `PARTIAL`, `PASS`, `DEFERRED`) (PASS — present, honest, with evidence).
- Files-modified list with line-delta annotations (PASS).
- Out-of-scope declaration for paradigm sub-skills with `disable-model-invocation: true` (PASS).

**Gate 5 Status**: **PASS** — self-DoD is structurally complete and honest about three deferrals.

---

## Empirical Cross-Checks (RUN at QA round 1)

```bash
# Frontmatter presence (TC-5 invariant arm)
$ grep -l "^maintainer: delivery-team-leads$" delivery-team/skills/*/SKILL.md | wc -l
11

# Budget script exit + content (TC-6)
$ python3 scripts/check_skill_budgets.py
BUDGET CHECK PASSED: 17 file(s) checked, 0 known-debt, 0 exception(s).
$ echo $?
0

# Godot exact-line gate (TC-3 + TC-6 binding)
$ wc -l delivery-team/skills/godot/SKILL.md
200 delivery-team/skills/godot/SKILL.md

# Hash anchor still matches stored value (TC-7 anchor arm)
$ sha256sum delivery-team/skills/delivery-flow/SKILL.md
43067c9e07e0b988cd976432dd07d5bb3d2336c41ad08a1b0064fb2fbd0b8328  delivery-team/skills/delivery-flow/SKILL.md
$ cat governance/cache-prefix-hash.txt
43067c9e07e0b988cd976432dd07d5bb3d2336c41ad08a1b0064fb2fbd0b8328  delivery-team/skills/delivery-flow/SKILL.md

# JSON validity (Gate 4 + AC-2 cross-check)
$ python3 -m json.tool governance/skill-budgets.json > /dev/null && echo OK
OK

# Tripwire artifact (AC-5)
$ test -f .delivery/telemetry/stop-rule-tk4.txt && echo EXISTS || echo MISSING
MISSING

# Lint script (AC-1)
$ test -f scripts/lint_skill_frontmatter.py && echo EXISTS || echo MISSING
MISSING

# CI workflow (W3-9 sub-deliverable)
$ test -f .github/workflows/skill-frontmatter-lint.yml && echo EXISTS || echo MISSING
MISSING
```

---

## Findings (Round 1 — actionable)

### F1 (Blocking for AC-1) — `scripts/lint_skill_frontmatter.py` missing

The story body explicitly enumerates this script as a "Files Touched" deliverable (`scripts/lint_skill_frontmatter.py (new)`) and AC-1 references it by command. Implementation deferred it to Story 7. Round-2 fix paths:

- (a) Author the script in Story 5 round 2: ~30 lines of Python; reads each `delivery-team/skills/*/SKILL.md`; parses YAML frontmatter; asserts presence of three keys; asserts `fitness_review_due` parses as ISO-8601; asserts `context_budget` ∈ {500, 300, 200} and matches `tier` ∈ {A, B, C}. Then add `.github/workflows/skill-frontmatter-lint.yml` per "Files Touched" line. Exit 0 path covered by current files; the deliberately-omitted-key fault-injection arm of TC-5 then becomes runnable. **OR**
- (b) PO/Architect amends Story 5 ACs in round 2 to drop AC-1's script clause and re-scope it to Story 7 W3-9 sub-deliverable; record amendment in stories.md edit-history.

### F2 (Blocking for AC-3) — `governance/cache-prefix-hash.txt` not expanded to 13-file scope; no header comment

ADR-tk4-003 §Cumulative cache-prefix re-freeze procedure binds Story 5 to regenerate the hash with expanded scope (`delivery-team/skills/*/SKILL.md` + `delivery-team/skills/*/paradigms/*/SKILL.md`) and to record the 13-file scope in a header comment. Implementation regenerated only the 1-file delivery-flow anchor and explicitly deferred expansion to Story 7. Round-2 fix paths:

- (a) Either author `scripts/regenerate_cache_prefix_hash.py` and produce a 13-line hash file with leading `# scope: 13 files; expanded from 1 (delivery-flow only) per ADR-tk4-003` comment; **OR**
- (b) Hand-regenerate using `sha256sum delivery-team/skills/*/SKILL.md > governance/cache-prefix-hash.txt` plus header-comment prepend; **OR**
- (c) Architect amends ADR-tk4-003 to declare 1-file anchor sufficient and defer 13-file expansion to Story 7; record amendment in ADR edit-history.

### F3 (Blocking for AC-5) — `.delivery/telemetry/stop-rule-tk4.txt` does not exist

The tripwire artifact is the binding evidence per architecture-tk4-wave-3.md §Stop-Rule Tripwire Mechanics. W3-18 telemetry hardening (Story 7) is the prerequisite for `prose_tokens` to be reliable per-dispatch — implementation correctly identifies this dependency. **However**, AC-5 is written as a hard gate ("Stop-rule tripwire NOT fired before this story opens its PR"). With no artifact, the tripwire status is *unknown*, not *not-fired*. Round-2 fix paths:

- (a) Hand-compute first-3-dispatch prose-token reduction from existing `.delivery/telemetry/skill-loads.jsonl` (if any rows exist), accepting any zero-token rows as `placeholder=true` per FR-7.6, write `stop-rule-tk4.txt` with the computed value; **OR**
- (b) Re-sequence: ship Story 7 W3-18 BEFORE Story 5 PR opens (architecture §Stop-Rule Tripwire Mechanics tail explicitly contemplates this dependency); **OR**
- (c) PO/Architect amends Story 5 AC-5 to declare W3-18 prerequisite missing and defer tripwire enforcement to next pipeline; record in stories.md + architecture edit-history. Implementation already documents this as the chosen path — AC-5 needs the explicit amendment to close as DONE.

### F4 (Warning) — Lint script absence breaks fault-injection arms of TC-5

Without `lint_skill_frontmatter.py` the QA fault-injection arm ("deliberately omit one key; MUST fail") cannot be exercised, leaving the future-regression detection unproven. Closely coupled to F1 — same fix.

### F5 (Suggestion) — All 11 files share the same `fitness_review_due` date

PRD §FR-5.4 contemplated optional 80-100-day staggered window. Round 1 ships unanimous 92-day. **Not a defect** (Gate 3 PASS), but the first fitness review on 2026-08-09 will hit all 11 skills at once, creating a one-day workload spike. Recommend staggering at the first review's outcome, not at round 2.

### F6 (Information) — `scripts/check_skill_budgets.py` KNOWN_DEBT Python list still has stale entries

Implementation §governance/skill-budgets.json Re-Baseline notes that the script's KNOWN_DEBT Python list still has 7 inert entries (don't fire because no file is over ceiling). Reconciling JSON↔Python is W3-14 in Story 7 and is correctly out of scope for Story 5. **Not a defect for Story 5**; flagged so Story 7 round-1 doesn't miss it.

---

## Round-2 Acceptance Path

Round-2 PASS requires EITHER:

- **Path A (deliver the deferrals in Story 5)**: Address F1, F2, F3 by shipping `lint_skill_frontmatter.py`, expanding the cache-prefix-hash to 13 files with header comment, and producing a (hand-computed if needed) tripwire artifact. AC-1, AC-3, AC-5 then PASS literally.
- **Path B (formal AC amendment)**: PO + Architect amend Story 5 ACs to re-scope F1/F2/F3 to Story 7, recording amendments in `stories.md` edit-history and `ADR-tk4-003` edit-history. QA re-runs round 2 against amended ACs and PASSES on 5/5.

Either path is acceptable; the current state (silent deferral) is not. Recommend **Path A** since each missing piece is small and shipping them in Story 5 keeps the wave's frontmatter governance fully self-contained and avoids cross-story dependency on Story 7 round-1 outcomes.

---

## Sources Verified

- `delivery-team/skills/*/SKILL.md` (×11) — frontmatter inspected
- `governance/skill-budgets.json` — JSON validated; `known_debt: []`; tier ceilings agree with frontmatter
- `governance/cache-prefix-hash.txt` — sha256 confirmed against current delivery-flow SKILL.md
- `scripts/check_skill_budgets.py` — executed, exit 0
- `.delivery/artifacts/06-dev/developer/story-5-implementation.md` — full read
- `.delivery/artifacts/05-plan/po/stories.md §Story 5` — 5 ACs traced
- `.delivery/artifacts/05-plan/qa/test-strategy.md TC-5/TC-6/TC-7` — procedures cross-checked
- `.delivery/artifacts/04-architect/adrs/ADR-tk4-003-governance-frontmatter-shape.md` — referenced (§Cumulative cache-prefix re-freeze procedure)

---

```
STATUS: NOT_DONE
ARTIFACT: .delivery/artifacts/06-dev/dod/story-5-qa-review.md
SUMMARY: Frontmatter present 11/11 + budget exit-0 + godot=200 PASS; AC-1 lint script missing, AC-3 hash 13-file scope missing, AC-5 tripwire artifact missing — all silently deferred to Story 7.
```

— Pippin Took, QA Engineer (FRESH), round 1, run-2026-05-09-tk4. *"The lintels bear the keys, the gate stands open at zero debt — but the watchman's bell, the wider hash, and the lint of the lint are all promised for tomorrow. Today's tally: two of five rung true; three rang silence."*

# QA Evaluation — PRD: Update Claude-Plugins Skills for Claude Opus 4.7

**Artifact**: QA Evaluation (Legolas / QA Engineer)
**Stage**: 2 / Refine — Evaluator-Optimizer
**Date**: 2026-04-20
**Inputs**:
- `.delivery/artifacts/02-refine/po/prd.md` (485 lines, Gandalf)
- `.delivery/artifacts/02-refine/data/scope-baseline.md` (191 lines, Elrond)
**Alias**: Legolas — *"That bug still only counts as one."*

---

> *"My eyes see far. I have counted the requirements and measured each against the baseline. Eight requirements. Seven success metrics. Eight risks. I will describe what I see, and I will not soften it."*

---

## Summary Verdict

**REVISE** — minor. The PRD does not block the Architect from starting transformation-planning. Seven of eight requirements are test-ready as written. A small number of acceptance criteria contain measurability or regression-guard gaps that should be tightened before Architect sign-off, but the structural testability of the PRD is sound — every REQ traces to a Finding or Inventory line, the keystone files are named, and grep-based regressions guards are in place for the highest-urgency items.

The defects are concentrated in: two metrics that rely on subjective sub-agent self-report without a baseline anchor (M-04, M-05), one regex that will false-negative on the exact strings it aims to catch (AC-01.4 / M-01 boundary chars), and several "size = S/M" claims that are effort estimates, not acceptance criteria. None are structural. All can be fixed by the PO in a targeted second-pass without rewriting the document.

**Defect count: 11.** *Shall I describe them? I thought you would ask.*

---

## Per-REQ Evaluation

| REQ | Testable? | Measurable? | Evidence-tied? | Regression guard? | Action needed |
|---|---|---|---|---|---|
| REQ-01 | YES | YES (grep-based ACs) | YES (F-04, MID-01..04) | **PARTIAL** — AC-01.4 regex is malformed | **FIX** — see DEF-01 below |
| REQ-02 | YES | PARTIAL — AC-02.4 "size = M" is effort, not acceptance | YES (F-13, F-15, F-25, F-26, F-28, F-29, PAT-01/02/06) | YES (AC-02.3 dogfood gate) | **FIX** — see DEF-02 |
| REQ-03 | YES | YES (AC-03.3 measures validator count) | YES (F-08, F-25, DISP-01..03) | YES (AC-03.3 end-to-end dogfood) | ACCEPT |
| REQ-04 | PARTIAL | **NO** — AC-04.1 "sharpness >= baseline" is not defined | YES (F-24, F-27, NDOC-03) | PARTIAL — dogfood is stipulated but its pass criterion is subjective | **FIX** — see DEF-03, DEF-04 |
| REQ-05 | PARTIAL | **NO** — "recognisable theme voice" is not defined | YES (F-27, DISP-03) | PARTIAL — same subjectivity issue | **FIX** — see DEF-05 |
| REQ-06 | YES (grep-based) | YES | YES (F-28) | N/A (COULD, defer-to-backlog branch is explicit) | ACCEPT |
| REQ-07 | YES | YES (backlog file existence is binary) | YES (Section 1 Non-Goals, F-18, F-19) | YES (scope-creep guard) | ACCEPT |
| REQ-08 | YES | PARTIAL — AC-08.1 "names the plugin-dev skill" is a document-shape check, measurable | YES (CLAUDE.md) | YES (process-compliance guard) | ACCEPT |

---

## Defect Log (ordered by severity)

### DEF-01 — AC-01.4 regex is malformed (HIGH)

**Where:** REQ-01 AC-01.4, line 271.

**Text as written:**
> `grep -rE 'claude-(opus\|sonnet\|haiku)-4-(0\|1\|20\|-20)' agentic-flow-builder/scripts/ prd-quality-gate-flow/` returns 0 results post-implementation.

**Defect:** The alternation group `(0\|1\|20\|-20)` will not match the target strings the AC is aimed at. The inventoried IDs to sweep are:

| Target | Matches regex? |
|---|---|
| `claude-sonnet-4-5-20250929` (MID-01) | YES (hits `-5-20`? No — `-5-` is the suffix separator and `20` would need to start immediately after `-4-`; `-5-20` is not in the alternation) — **NO, false negative** |
| `claude-haiku-4-20250514` (MID-02) | YES (`-4-20`) |
| `claude-opus-4-20250514` (MID-03) | YES (`-4-20`) |

The regex will false-negative on MID-01 — the highest-count hit — because the character immediately after `-4-` in `claude-sonnet-4-5-20250929` is `5`, and `5` is not in the alternation. The AC therefore certifies "0 results" even if MID-01 is never fixed.

Additionally, Anthropic retirement IDs include `claude-sonnet-4-20250514` and `claude-opus-4-20250514` (F-04) — these match. But `claude-haiku-4-5-20251001` (the legitimate replacement target for MID-02) ALSO matches (`-4-5`? No — `-5` starts with `5` which is not in the alternation; actually `-4-5-` means after `-4-` the next char is `5`, still not in the set). So the regex will correctly ignore the legitimate replacement. Mixed-luck: correct for some targets, wrong for the MID-01 baseline.

**Fix:** Replace AC-01.4 with a grep that catches the inventoried shapes without false-negatives. Two concrete options:

```bash
# Option A: enumerate retiring dated IDs explicitly
grep -rnE 'claude-(opus|sonnet|haiku)-4-(20250514|5-20250929)' \
  agentic-flow-builder/ prd-quality-gate-flow/ \
  --exclude-dir=.delivery --exclude-dir=__pycache__
# Expect: 0 lines post-implementation
```

```bash
# Option B: broader regex with an allowlist for canonical 4.7 IDs
grep -rnE 'claude-(opus-4-7|sonnet-4-6|haiku-4-5-20251001)' ... # whitelist
grep -rnE 'claude-(opus-4|sonnet-4-5|haiku-4|haiku-3)-[0-9]{8}' ... # blocklist
```

Also: `prd_flows.db` is a SQLite binary (Elrond Section 2) and contains 21 stored short-alias occurrences. The AC must either scope the grep with `--binary-files=without-match` or explicitly exclude `*.db`, otherwise `grep -rE` will flag the binary as "match" and the AC will never pass.

**Action:** PO rewrites AC-01.4 with a non-leaky regex and an explicit `--exclude=*.db` (or equivalent).

---

### DEF-02 — Sizing sub-claims embedded in acceptance criteria (MEDIUM)

**Where:** AC-02.4 (line 284: "size = M"), AC-03.4 (line 297: "size = S"), AC-04.3 (line 309), AC-05.3 (line 322).

**Defect:** "Size = S/M/L" is an Architect effort estimate, not something QA can verify from an artifact. It belongs in the roadmap's sizing column, which the Architect will produce — not as a PRD acceptance criterion. If the Architect sizes REQ-02 as L, a mechanical reading of AC-02.4 would flag the roadmap as non-compliant even if the sizing is correct.

**Fix:** Move sizing claims out of ACs and into a separate "PO sizing hypothesis" subsection (or demote them to rationale lines). ACs should be pass/fail against the roadmap document's structure, not against the Architect's sizing judgement.

**Action:** PO re-labels AC-02.4/AC-03.4/AC-04.3/AC-05.3 as "PO sizing hint (non-binding on Architect)".

---

### DEF-03 — M-04 "sharpness >= baseline-from-4.6" is not measurable (MEDIUM)

**Where:** Section 5, M-04, line 370.

**Text as written:**
> "user-feedback skill rates the adversarial critique as 'sharpness >= baseline-from-4.6' across >=3 sampled runs"

**Defect:** No 4.6 baseline artifact is referenced. Elrond's `scope-baseline.md` is a repo-structural baseline, not a 4.6 output capture. There is no saved "here is what Challengers produced on 4.6" in `.delivery/` to compare against. The metric is asking QA (or the user-feedback sub-agent) to compare 4.7 output against a baseline that does not exist.

Second defect: "sharpness" is undefined. Count of criticisms? Word count? Presence of specific keywords? The user-feedback skill produces persona opinions, not numeric scores.

**Fix:** Either:
- **(a)** Require the implementation run to capture a 4.7-only baseline first (record Challenger output from one mtg-commander run), then compare future runs to that captured baseline, measuring against it (e.g., "Challenger output contains >= N distinct critique points, where N is established in the baseline capture"), OR
- **(b)** Replace "sharpness" with a concrete checklist: "Challenger output must (i) name at least 3 distinct weaknesses, (ii) cite specific card names, (iii) propose at least 1 concrete alternative — all three required, binary pass/fail per run."

**Action:** PO rewrites M-04 with a concrete pass/fail criterion or an explicit baseline-capture step.

---

### DEF-04 — AC-04.1 dogfood gate has no pass criterion (MEDIUM)

**Where:** REQ-04 AC-04.1, line 307.

**Text as written:**
> "Roadmap item includes an explicit dogfood gate: at least one adversarial review cycle on 4.7 reviewed by the `user-feedback` skill (simulated persona) before any implementation change ships."

**Defect:** The gate specifies *that a review happens* but not *what the review must conclude* for the gate to be considered passed. Without a pass criterion, the gate is always-passing-or-always-failing-by-reviewer-opinion and cannot be mechanically validated.

**Fix:** Add an explicit pass criterion, e.g.:
> "Gate passes if (a) the user-feedback sub-agent reports no severity-HIGH tone/depth regression vs the baseline capture (see M-04 fix), AND (b) at least one persona review is on file at `.delivery/artifacts/*/user-feedback/adversarial-4-7-sample.md`."

**Action:** PO adds a pass criterion to AC-04.1, linked to the M-04 fix.

---

### DEF-05 — AC-05.1 / M-05 "recognisable theme voice" is not measurable (MEDIUM)

**Where:** REQ-05 AC-05.1 (line 320), M-05 (line 371).

**Text as written:**
> "record whether thematic voice is preserved" / ">=80% of sampled stage announcements retain recognisable theme voice (spot-sampled personas)"

**Defect:** "Recognisable" is undefined. No ground-truth reference for "what theme X voice sounds like" is provided. 80% of what sample size? Who decides recognisability — the user-feedback sub-agent, the user, or QA?

**Fix:** Define a concrete per-theme signature (2–3 lexical / stylistic markers per theme sampled) and measure presence:
> "For each of 3 sampled themes, the theme's reference file in `alias-creator/references/` defines 2+ signature markers (catchphrase, register, typical noun/verb choice). A stage announcement 'preserves voice' iff >= 50% of its theme's signature markers appear in the rendered output. Target: >= 80% of sampled announcements preserve voice."

**Action:** PO either sharpens AC-05.1/M-05 with a marker-based definition or explicitly re-labels them as "advisory, not binary" with an Architect note that dogfood findings are qualitative.

---

### DEF-06 — M-01 grep regex has the same boundary-char defect as AC-01.4 (MEDIUM)

**Where:** Section 5, M-01, line 367.

**Text as written:**
> `grep -rE 'claude-(opus-4-20250514\|sonnet-4-20250514\|haiku-4-20250514\|haiku-3-)' --exclude-dir=.delivery --exclude-dir=.git` returns 0 lines

**Defect 1:** `haiku-4-20250514` is not a real Anthropic model ID (F-03 confirms Haiku 4.5's dated ID is `claude-haiku-4-5-20251001`). The inventoried string in the repo is `claude-haiku-4-20250514` (MID-02, known-bad), so this part is correct — but it should be commented so a future reader doesn't remove it believing it a typo.

**Defect 2:** `sonnet-4-20250514` is not inventoried anywhere in the repo per Elrond Section 2 — the repo has `claude-sonnet-4-5-20250929`, not `claude-sonnet-4-20250514`. So this clause can never fire on the current repo, and if it does fire post-implementation, it means someone added a NEW deprecated ID rather than a model-ID being left unmigrated. That is arguably a useful forward-guard, but it is not measuring REQ-01's acceptance.

**Defect 3:** The metric misses MID-01 (`claude-sonnet-4-5-20250929`) entirely. If REQ-01 is only partially executed and MID-01 is left on `claude-sonnet-4-5-20250929`, M-01 still passes. That is the exact class of silent regression the PRD claims to guard against.

**Fix:** Replace with a metric that is the complement of the canonical 4.7-era allowlist:

```bash
# Fails if any file contains a Claude dated model ID that is NOT one of:
#   claude-haiku-4-5-20251001  (current Haiku 4.5 dated ID)
grep -rnE 'claude-(opus|sonnet|haiku)-[0-9](\.[0-9])?-[0-9]{8}' \
  --exclude-dir=.delivery --exclude-dir=.git --exclude=*.db \
  | grep -v 'claude-haiku-4-5-20251001' \
  | wc -l   # Expect: 0 post-implementation
```

**Action:** PO rewrites M-01 with a complement-of-allowlist approach and explicitly excludes `*.db` (the `prd_flows.db` SQLite file has 21 stored short-alias occurrences per Elrond Section 2; they are data, not code).

---

### DEF-07 — M-02 is redundant with M-01 and contains an incorrect premise (LOW)

**Where:** Section 5, M-02, line 368.

**Text as written:**
> "Zero `claude-opus-4-6` hard-coded IDs in non-archival code."

**Defect:** Elrond Section 2 confirms `claude-opus-4-6` appears 0 times in the repo today. The metric is asserting a condition that is already true and therefore cannot regress via REQ-01 (which does not introduce 4.6 IDs). It is measuring nothing that REQ-01 affects.

**Fix:** Either delete M-02, or re-scope it to a regression guard:
> "Zero `claude-opus-4-6` or `claude-sonnet-4-5*` (non-legacy-note) introductions post-implementation." (Useful if Architect's roadmap ends up documenting 4.6→4.7 diffs in prose — we want to catch model IDs re-entering as code strings, not prose references.)

**Action:** PO either deletes M-02 or re-scopes it.

---

### DEF-08 — M-07 target (>=95% SKILL_LOADED first-attempt) lacks a baseline (LOW)

**Where:** Section 5, M-07, line 373.

**Text as written:**
> "SKILL_LOADED signal fires on >=95% of agent dispatches in first attempt during a full dogfood run."

**Defect:** 95% is asserted without reference to the current first-attempt rate (which `verify_skill_load.py` telemetry presumably measures, but no baseline capture is cited). The metric may be too generous (if 4.6 hit 99%, a regression to 97% passes the gate but is real) or too strict (if 4.6 hit 92%, the metric blocks shipping on pre-existing behaviour).

**Fix:** Anchor the target to baseline:
> "Post-implementation SKILL_LOADED first-attempt rate must be >= max(0.95, baseline_rate - 0.02). Baseline rate is captured from the pre-implementation dogfood run logged in `.delivery/artifacts/<impl-run>/observability/skill-load-baseline.json`."

**Action:** PO rewrites M-07 with a baseline-anchored target or explicitly labels the 95% as "initial threshold; revise after first baseline capture".

---

### DEF-09 — R-01 mitigation ("enforces dogfood-before-edit") is testable only via AC-04, and AC-04 has DEF-03/DEF-04 (LOW, derived)

**Where:** Section 6.1, R-01, line 383.

**Defect:** R-01's mitigation is "REQ-04 enforces dogfood-before-edit." The mitigation inherits DEF-03 and DEF-04. Fixing those two fixes this.

**Action:** No additional fix required if DEF-03 and DEF-04 are addressed.

---

### DEF-10 — R-05 retirement date mitigation is not time-bounded (LOW)

**Where:** Section 6.1, R-05, line 387.

**Text as written:**
> "REQ-01 AC-01.2 time-sensitive flag; Architect must sequence this item first."

**Defect:** "Must sequence this item first" is a prose assertion, not a testable condition. The PRD does not define what "first" means measurably (before stage N? before date D? before PR X?). If the Architect's roadmap says "REQ-01 is item 3 of 8", the mitigation is trivially violated, but there is no mechanical check.

**Fix:** Tie to a date:
> "Roadmap must mark REQ-01 with a target completion date no later than 2026-06-01 (14-day safety buffer before 2026-06-15 retirement). If roadmap lacks a date or the date is after 2026-06-01, reviewer should reject."

**Action:** PO adds a date-bounded acceptance, OR explicitly down-classifies R-05 likelihood given implementation cadence; either is fine.

---

### DEF-11 — R-08 "contingency slot" has no structural verification (LOW)

**Where:** Section 6.1, R-08, line 390.

**Text as written:**
> "Roadmap must leave a contingency slot for 'findings-from-dogfood' items."

**Defect:** "Contingency slot" is structurally vague. How does a reviewer verify the roadmap contains one? As a named phase? An empty backlog section? A reserved capacity percentage?

**Fix:** Structural requirement:
> "Roadmap must contain a section titled 'Contingency — Dogfood Findings' with at least one placeholder item ID reserved (e.g., TBD-CONTINGENCY-01). If section is missing, reviewer should reject."

**Action:** PO adds a concrete structural form for the contingency slot.

---

## Success Metrics Review (consolidated)

| # | Issue | Concrete fix |
|---|---|---|
| 1 | M-01 grep malformed + misses MID-01 + `.db` binary false-positive | DEF-06 — use complement-of-allowlist with `--exclude=*.db` |
| 2 | M-02 redundant with M-01 and measures a vacuous condition | DEF-07 — delete or re-scope as regression guard |
| 3 | M-04 "sharpness" undefined + no 4.6 baseline exists | DEF-03 — replace with checklist or capture 4.7 baseline |
| 4 | M-05 "recognisable theme voice" undefined | DEF-05 — marker-based definition per theme |
| 5 | M-07 95% target has no baseline anchor | DEF-08 — baseline-anchored target |
| 6 | M-03 is fine as written | No change |
| 7 | M-06 is fine as written (binary, log-grep measurable) | No change |

---

## Risks Review (consolidated)

| # | Issue | Concrete fix |
|---|---|---|
| 1 | R-01 mitigation inherits M-04 / AC-04 defects | DEF-09 — fixes automatically via DEF-03/DEF-04 |
| 2 | R-05 "sequence first" is prose, not testable | DEF-10 — date-bound to 2026-06-01 |
| 3 | R-08 "contingency slot" is structurally vague | DEF-11 — require named section with placeholder item ID |
| 4 | R-02/R-03/R-04/R-06/R-07 artifact-tied and mitigation-specific | No change |

All 8 risks ARE tied to specific artifacts / plugins / patterns (none vague). All 8 risks have a mitigation hint. The defects are in mitigation *testability*, not in risk identification.

---

## Top 3 Priorities for PO Revision

1. **Fix the grep-based ACs/metrics so they actually catch the inventoried defects** (DEF-01, DEF-06). This is the highest-impact fix — the PRD's primary regression guard is a grep, and two of those greps are malformed or leaky. Without this fix, REQ-01 can be "passed" with MID-01 still on `claude-sonnet-4-5-20250929` and the SQLite binary generating false positives.

2. **Define concrete pass criteria for the dogfood-based ACs/metrics** (DEF-03, DEF-04, DEF-05, DEF-08). Four of the seven metrics and two of the eight ACs hinge on subjective sub-agent judgement with no defined pass criterion. Either (a) capture a 4.7 baseline on the first implementation run and measure deltas against it, or (b) replace "sharpness/recognisability" with specific marker checklists. Pick one approach per metric and write it into the PRD.

3. **Move sizing claims out of acceptance criteria** (DEF-02). Architect owns sizing. ACs that embed "size = M" conflate PRD-reviewer approval with roadmap-shape approval and will fire false-negatives if the Architect's sizing diverges from PO expectations. Either demote to "PO sizing hypothesis" or remove.

DEF-07, DEF-10, DEF-11 are low-priority cleanup and can be addressed in the same pass without adding meaningful effort.

---

*Forty-two… no, eleven defects. My count was exact. The PRD is sound in shape; it needs tighter greps and tighter gates. The Architect may proceed after revision — the structural testability is intact, only the instruments need calibration.*

— **Legolas**, QA Engineer

---

**End of Evaluation.**

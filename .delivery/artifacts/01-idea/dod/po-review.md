<!-- run: run-2026-05-28-backlog-108 -->
# PO DoD Review — Idea Stage (Round 2, Re-validation)

**Role**: Product Owner DoD Validator (Gandalf)
**Stage**: 1 — Idea DoD
**Round**: 2 (re-validation after revision)
**Artifact under review**: `.delivery/artifacts/01-idea/po/idea-brief.md`
**Binding context**: `.delivery/memory/topics/opus-4-8-migration.md`
**Date**: 2026-05-28

> I sent this brief back once with two blocking defects. I read the revision fresh from disk and re-ran every count myself. The number is now true, and the team will not be surprised at Development. That is the bar.

---

## Verdict: DONE

Both Round-1 blocking defects are remediated. The non-blocking defect is also closed. All eight gate criteria pass. Counts independently re-verified against the live tree.

---

## Independent Count Verification (re-run this round)

I did not trust the revision on its face. Every load-bearing number was re-probed:

| Probe | Expected | Observed | Result |
|-------|----------|----------|--------|
| `grep -rl "model_awareness" --include="SKILL.md" \| wc -l` | 25 | **25** | ✅ stamped today |
| `find -name SKILL.md \| wc -l` | 34 | **34** | ✅ total |
| Unstamped delta (34 − 25) | 9 | **9** | ✅ matches brief's enumeration |
| Live `claude-opus-4-7` source sites (excl. `.delivery/`, guard) | 5 | **5** | ✅ all enumerated |

The 9 unstamped files named in the brief (4 user-feedback personas + 5 research-types) are exactly the 34−25 delta. The five live literal sites — `agent_registry.py`, `prompt-engineer/SKILL.md:368`, `conftest.py` (×4 hits), `smoke-test-architecture.md` — match grep's findings outside the artifact tree. The guard file is correctly the rewrite target, not a leak.

---

## Round-1 Defect Closure

### Blocking Defect 1 (Criterion 2) — CLOSED ✅
Round 1 failed because AC#2/AC#3 asserted "34 stamped" against a tree where only 25 carry a stamp, making the grep assertion unsatisfiable and conflating *update* with *create*.

The revision fixes this precisely:
- **AC2 now asserts a COUNT**: `grep -rl "model_awareness: opus-4-8" --include="SKILL.md" | wc -l` returns **34**, AND the negative-residue assertion `grep -rh "model_awareness:" | grep -v "opus-4-8" | wc -l` returns **0**. The AC explicitly states this "proves both the 25 updates and the 9 creations landed."
- The brief now distinguishes **updated (25)** from **created (9)** stamps in three places: the stamp-accounting block, the in-scope list ("25 stamp updates + 9 stamp creations"), and the enumerated list of the 9 currently-unstamped files. 25 + 9 = 34, internally consistent and matching my probe.
- AC3 ("all 34 prose reviewed; no `-frontmatter-only` marker") correctly captures BINDING-2.2's intent without conflating review with stamp count.

The defect that surprised the team is gone — the new unit of work (9 stamp *creations*) is now explicit.

### Blocking Defect 2 (Criterion 4) — CLOSED ✅
Round 1 failed because the brief cited `BACKLOG-108-opus-4-8-migration.md` as if it existed; it did not.

The revision now states plainly (header line 9): "to be authored at Stage 2 (Refine). This is a forward reference. The file does not exist yet. Stage 2 creates it." This is an honest forward reference, which the gate criteria for this round explicitly accept. No longer a false claim of an on-disk artifact.

### Non-Blocking Defect 3 (Criteria 1, 3) — CLOSED ✅
Round 1 noted the problem statement missed `prompt-engineer/SKILL.md:368` as a second hard model-ID string. The revision now enumerates all five live literal sites with file:line in both the Problem Statement and the in-scope list, and explicitly calls out line 368 as a "`MODEL_ID` code literal fix (distinct from its frontmatter stamp)" tied to the guard risk under AC1. Full blast radius now mapped.

---

## Criterion-by-Criterion (Round 2)

### 1. Problem statement clear, specific, evidence-based — ✅ PASS
Numeric and falsifiable: 34 files, 25 stamped (7 `opus-4-7` + 19 `-frontmatter-only`), 9 unstamped. All five literal sites named with file:line. Urgency grounded in a verifiable behavioral fact (4.8 under-dispatches vs 4.7). The Round-1 false "sole occurrence" claim is corrected.

### 2. Success criteria measurable — ✅ PASS (key criterion)
Seven ACs, all objectively verifiable via named commands / file-state assertions. AC2 carries the required explicit count (34) plus zero-residue negative assertion, and distinguishes updates from creations. This was the Round-1 failing criterion; it is now correct.

### 3. Scope explicit, all live 4-7 sites included — ✅ PASS
In-scope enumerates all five live literal sites individually; out-of-scope correctly carves BINDING-1.4 aliases, BINDING-4.6 CI smoke workflows, and PRs (BINDING-5.1). The 9 stamp creations are explicit.

### 4. Backlog reference present — ✅ PASS
BACKLOG-108 cited as an honest Stage-2 forward reference, explicitly flagged as not-yet-existing. Acceptable per this round's gate note.

### 5. Routing declared — ✅ PASS
FEATURE; Stage 3 Design SKIP (DX-only, justified); seven-story dependency-ordered plan honoring BINDING-2.5 keystone-first sequencing.

### 6. Plugin-dev skill routing acknowledged — ✅ PASS
Explicit in Proposed Solution and Constraint 1: SKILL.md edits → `plugin-dev:skill-development`; hook edits → `plugin-dev:hook-development`; non-optional with Developer DoD evidence requirement. Matches CLAUDE.md binding.

### 7. No conflict with binding decisions — ✅ PASS
Cross-checked against all 24 BINDING rulings. Every cite is faithful (1.4, 2.1–2.5, 3.1–3.3, 4.2–4.6, 5.1, 5.4, 5.5). No re-litigation (BINDING-5.6 respected). The brief uses the verified actual count 34 where memory says "~25" — this sharpens an approximate binding figure with a verified count while preserving the binding's "ALL SKILL.md files" intent. Not a conflict.

### 8. Budget acknowledged — ✅ PASS
Constraint 2: ~$15 total, ~$3/sample cap, runner enforces `--cost-cap 3.00`. Line-budget cap and exception protocol also acknowledged (Constraint 4).

---

## Strengths

- ACs are crisp and machine-verifiable (exit codes, grep counts, JSON field checks, adversarial re-fetch ≥3).
- Full binding-decision fidelity across 24 rulings — correct keystone order, exact provenance-comment match.
- Risk register is real; R1 (self-referential dispatch) is the sharp one, correctly mitigated by BINDING-5.4. R5 adds a pre-squash guard sweep run independently by QA — exactly the right backstop for the guard-rewrite blast radius.
- Budget capped and enforced; plugin-dev routing acknowledged with DoD teeth.

---

STATUS: DONE
ARTIFACT: .delivery/artifacts/01-idea/dod/po-review.md
FINDINGS: All 8 criteria PASS. Both Round-1 blocking defects closed — AC2 now asserts count=34 with zero-residue check and distinguishes 25 updates vs 9 creations; BACKLOG-108 reframed as honest Stage-2 forward reference. Counts independently re-verified (25 stamped / 34 total / 5 live 4-7 sites). Gate-ready for Stage 2 (Refine).

— Gandalf, PO, run-2026-05-28-backlog-108. The count is now true. The work may begin.

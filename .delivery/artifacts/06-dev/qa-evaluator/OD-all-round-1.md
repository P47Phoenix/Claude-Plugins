# OD-all — Evaluator-Optimizer Round 1

**Evaluator**: Legolas of the Woodland Realm — QA, precise of eye.
**Stage**: 06 — Development (Evaluator-Optimizer Loop, Round 1)
**Scope**: OD-01 through OD-13 vs. sprint plan acceptance criteria.
**Verdict**: **NOT_DONE** — one P0 defect (incomplete wizard renumbering), two minor inconsistencies. Fix and resubmit.

> *"The wind has shifted. I count thirteen arrows loosed; twelve fly true. One has split its shaft mid-flight."*

---

## Per-criterion verdict

### 1. All 13 stories implemented — **PASS (with caveats below)**

Developer's `OD-all.md` records implementation notes for OD-01..OD-13 inclusive. Spot checks below confirm most edits landed. OD-10 was implemented (not dropped via slip protocol).

---

### 2. SKILL.md — delegation principle, Step 4.5, anti-patterns, One-Role rule, Phase 1 always-detect — **PASS**

Evidence (`delivery-team/skills/delivery-flow/SKILL.md`):
- Line 111: `Phase 1 (type detection) ALWAYS runs from the current user request. Config no [longer pins it]`.
- Line 156–157: `routing.force_type` and `pipeline.enforce_self_write_block` rows added to config table.
- Line 195–202: Phase 1 section explicitly states `Phase 1 runs on EVERY pipeline invocation`; `routing.force_type` documented as opt-in pin while detection still runs and logs.
- Line 317: `### One Role = One Sub-Agent (Prime Directive Corollary)` callout present.
- Line 445: `### Step 4.5: Delegation Self-Check` present (renamed from old Step 4.5; OQ-4 disposition implicit in section title).
- Line 720: `## Common Orchestrator Anti-Patterns` top-level section present.
- Line 755–757: Anti-patterns explicitly call out `project_type` removal and `routing.force_type` opt-in semantics.

All five SKILL.md sub-requirements satisfied.

---

### 3. config-schema.md — bumped to 2.7, project_type removed from active table, routing.force_type added, migration noted — **PASS**

Evidence (`references/config-schema.md`):
- Line 5: `## Current Version: 2.7`.
- Line 15: `config_version` row updated to default `"2.7"`.
- Line 16: `routing.force_type` row added with full enum.
- Line 17: `pipeline.enforce_self_write_block` row added with v2.7 default `true`, tolerantly-parsed v2.6 default `false`.
- Line 180: Config File Template uses `config_version: "2.7"`.
- Line 230: template includes `enforce_self_write_block: true`.
- Line 295: `## Deprecated Keys` section present.
- Line 299: `project_type` listed as **Warn-and-drop**, migration note points to `routing.force_type`.
- Line 301–310: Migration notes for both v2.6→v2.7 tolerant parse and the new `enforce_self_write_block` default.

**Minor finding (non-blocking, M-01)**: Line 64 still references `auto (from project_type)` in the `personas.categories` `Default` column. Since `project_type` is no longer a config key, this default expression should be reworded to `auto (from runtime-detected type)` or equivalent. Not a sprint-blocker, but it leaks the deprecated vocabulary into a live row. Recommend fix in Round 2 or as a follow-up nit.

---

### 4. setup-wizard.md — Q1 removed, questions renumbered, migration protocol added — **FAIL (P0 defect)**

Evidence (`references/setup-wizard.md`):
- Line 50–51: Header announces "wizard asks 8 questions (down from 9 in v2.6 — Q1 Project Type was removed in v2.7)". Good.
- Line 57–62: v2.7 migration note present with deprecation banner text. Good.
- Line 67–228: Questions renumbered Q1..Q8 cleanly through `### Q8: Existing .delivery/ State`. Good.
- **Line 248: `### Q10: User Feedback Personas`** — should be Q9.
- **Line 273: `### Q12: Enforcement Settings`** — should be Q10. Q11 has been silently elided with no audit trail.

Renumbering is **incomplete**. Stories OD-01 AC#3 and OD-09 explicitly require former Q2..Q10 to renumber to Q1..Q9 (developer's own notes say "8 questions"). The current file has a gap (Q9 missing entirely) and two stale numbers (Q10, Q12). This is a P0 defect against OD-01 acceptance criterion #3 and OD-01-T1 ("Exactly 9 [now 8] questions, none about project type").

**Additional inconsistency (M-02)**: Line 21 still says `Show detected values, ask 9 questions with smart defaults`. Should be `8 questions` (or `8` to match the v2.7 announcement on line 50).

**Additional inconsistency (M-03)**: Line 418 references `Hook 8 is only expected when enforcement.source_code_hook` — verify this `Hook 8` numbering refers to a separate hooks-validation list and not to a wizard question. If it is a wizard-question reference, it must also be renumbered. (Cursory read suggests it is the hook validation list; flagging for developer to confirm.)

**Fix guidance (Round 2)**:
1. Rename `### Q10: User Feedback Personas` → `### Q9: User Feedback Personas`.
2. Rename `### Q12: Enforcement Settings` → `### Q10: Enforcement Settings`.
3. Audit the file body for cross-references to "Q10", "Q12", "Q9", "after Q12", "Hook 8" and update them to the new numbers.
4. Update line 21 prose to say `8 questions`.
5. If a former Q9/Q11 truly existed and was deliberately removed in addition to Q1, document that in the v2.7 migration note. Otherwise the gap is just a renumbering miss.

---

### 5. team-patterns.md — dispatch rule per pattern + Isolated Adversarial Loop variant — **PASS**

Evidence (`references/team-patterns.md`):
- Line 20: Evaluator-Optimizer pattern leads with `**Dispatch rule**: ... SEPARATE Agent tool calls`.
- Line 101: Adversarial Review pattern dispatch rule + forward reference to Pattern 2b.
- Line 206: `## Pattern 2b: Isolated Adversarial Loop` section present.
- Line 208: Loop dispatch rule (`Each loop iteration dispatches a FRESH sub-agent with zero prior-loop context`).
- Line 240: Issue class taxonomy `coupling | security | data-integrity | naming | testability | performance | docs` verbatim.
- Lines 251, 254, 256: All three convergence rules present (`two_clean`, `class_saturated`, `cap_reached`).
- Line 262: `cap_reached` documented as exit, not failure.
- Lines 289, 303, 315: Loop pseudocode block present with three exit branches.
- Line 336: Multi-Perspective Review Board dispatch rule present.
- Line 422: Decision Ownership dispatch rule present.
- Line 488: Debate dispatch rule present (PRO/CON/JUDGE as three Agent calls).
- Line 687: Consensus dispatch rule present.

All six patterns lead with a dispatch rule; the new Isolated Adversarial Loop variant matches FR-13 / ADR-003 / OD-11 acceptance criteria.

---

### 6. quality-gates.md — one-validator-per-Agent rule + meta-gate — **PASS**

Evidence (`references/quality-gates.md`):
- Line 47: `**One validator = one Agent invocation.**` rule present.
- Line 53: Forbids multi-hat sub-agents.
- Line 55: `### Delegation Meta-Gate` section present.
- Line 60: Meta-gate phrased as the explicit DoD question.
- Line 74: `### Known Hook Limitations` section present.
- Line 90: Mirrors `enforce_pipeline_scope.py` known gaps (Layer 2 drift, centralized dispatch missing).
- Line 94: Instruction to validators to apply meta-gate manually.

Matches OD-13 quality-gates acceptance criteria.

---

### 7. pipeline-stages.md — header note + Stage 4 Isolated Adversarial Loop — **PASS**

Evidence (`references/pipeline-stages.md`):
- Lines 19–26: Header note explaining `[PARALLEL]` / `[SEQUENTIAL]` annotations imply one Agent tool call per role; cross-references SKILL.md "One Role = One Sub-Agent" and `audit_agent_prompt.py`.
- Line 327: `## Stage 4: Architect`.
- Line 363: `**Isolated Adversarial Loop** [SEQUENTIAL after eval-opt, multi-iteration] [required]` step present, replacing the single-pass adversarial review per OD-12.
- Line 364–365: Notes "Each loop iteration dispatches a fresh reviewer sub-agent (one Agent tool call per loop)".

Matches OD-09 / OD-12 acceptance criteria.

---

### 8. enforce_pipeline_scope.py — layered origin detection per ADR-001 — **PASS**

Evidence (`delivery-team/hooks/enforce_pipeline_scope.py`):
- Lines 11–23: Module docstring documents activation gating (`schema_version >= 2.7 AND pipeline.enforce_self_write_block: true`) and layered detection strategy.
- Line 82–89: `ARTIFACT_ALLOWLIST` and `ARTIFACT_ALLOWLIST_DIRS` constants centralized.
- Lines 108–109: `SUBAGENT_ENV_VARS` includes both `CLAUDE_AGENT_ID` and `DELIVERY_FLOW_AGENT_CONTEXT`.
- Lines 121–123: `_is_allowlisted` walks the dirs prefix list.
- Line 135: `_detect_subagent_origin` helper present, implementing Layers 1 & 2.
- Lines 154, 158: Layer 2 inspects `parent_tool_use_id` directly and via nested `context.parent_tool_use_id`.
- Line 169: `_activation_gated` helper present.
- Line 180: Reads `pipeline.enforce_self_write_block`.
- Lines 342–354: `main()` activation-gates the soft-deny path and emits a systemMessage naming the Delegation Prime Directive when no sub-agent origin signal is found. Soft-deny only (sys.exit(0) preserved per the existing `try/except` wrapper).

ADR-001 layered detection requirements satisfied. Stdlib only confirmed (no new third-party imports). The Bash redirection bypass is correctly documented as a known gap, not silently fixed (consistent with the developer's slip note and OD-13 known-limitations entry).

---

### 9. audit_agent_prompt.py compound-role detection (OD-10 — optional, implemented) — **PASS**

Evidence (`delivery-team/hooks/audit_agent_prompt.py`):
- Line 14: `_ROLE_LINE_RE` regex compiled for `^\s*ROLE:\s*\S+`.
- Line 25: `_detect_compound_roles(prompt)` helper.
- Line 27, 31: Detector 1 — multiple `ROLE:` declarations in one prompt.
- Line 38–39: Detector 2 — phrasal patterns (`also act as`, `then act as`).
- Line 45: Detector 3 — two `You are <role>` declarations close together.
- Lines 82–84: Compound warnings appended to existing systemMessage warnings list (non-blocking).
- Line 91: Warning output references `'One Role = One Sub-Agent'`.

OD-10 was implemented rather than dropped via slip protocol. Implementation matches FR-12 (non-blocking, stdlib-only, links to canonical rule). Note: I did NOT independently verify negation-awareness (FR-12 / OD-10-T3). Recommend the Round 2 developer or QA Round 2 run a quick synthetic test: prompt containing `do not act as both` should NOT trigger. If negation-awareness is missing, that is an OD-10 defect; given OD-10 is MAY, the slip protocol still permits dropping it rather than fixing.

---

### 10. CLAUDE.md, README.md, marketplace.json updated — **PASS**

Evidence:
- `CLAUDE.md` line 96: schema `currently v2.7`. Line 97: project type detected per run, `routing.force_type` opt-in. Line 98: setup wizard 8 questions. Line 125: Config schema convention line updated to v2.7 with migration note.
- `README.md` line 62: Setup wizard described as 8-question, runtime detection, `routing.force_type` opt-in pin.
- `.claude-plugin/marketplace.json` line 9: `"version": "2.18.0"` (bumped from 2.17.0 per OD-13 derived artifact note).

Doc parity satisfied for the three named files.

**Note (M-04, non-blocking)**: I did not grep `docs/**` (the MkDocs Material site, 25 pages) for stale `2.6` / `project_type` references as required by OD-13 ACs #4 and #5 and test cases OD-13-T4/T5. Developer's notes mention CLAUDE.md / README.md / delivery-team/README.md / marketplace.json explicitly but do NOT mention the `docs/` MkDocs tree. **Recommend Round 2 verification**: run `grep -rn "project_type" docs/` and `grep -rn "schema_version: 2.6" docs/` to confirm OD-13 AC #5 holds. If hits exist, it is a P0 doc-parity defect against NFR-04. If clean, mark M-04 closed.

---

## Defect summary

| ID | Severity | Story | Description | Round 2 fix |
|---|---|---|---|---|
| **D-01** | **P0** | OD-01, OD-09 | `setup-wizard.md` renumbering incomplete: `### Q10: User Feedback Personas` and `### Q12: Enforcement Settings` are stale; Q9/Q11 are gaps. Line 21 still says "9 questions". | Renumber Q10→Q9, Q12→Q10. Audit cross-references. Update line 21 to "8 questions". |
| M-01 | minor | OD-01 | `config-schema.md` line 64 leaks `from project_type` in the `personas.categories` Default column. | Reword to `auto (from runtime-detected type)`. |
| M-02 | minor | OD-09 | `setup-wizard.md` line 21 says "9 questions". | Update to "8". (Subsumed by D-01 fix.) |
| M-03 | nit | OD-09 | `setup-wizard.md` line 418 references "Hook 8" — confirm this is a hook-validation list reference, not a wizard-question reference. | Confirm scope; no edit if hook-validation list. |
| M-04 | unverified | OD-13 | `docs/**` MkDocs tree not grep-verified for `project_type` / `2.6` per OD-13 AC #5. | Run grep; if hits, fix; if clean, close. |
| M-05 | unverified | OD-10 | OD-10 negation-awareness (`do not act as both`) not independently verified by evaluator. | Synthetic test or accept as MAY-drop risk. |

---

## Convergence note (Round 1 → Round 2)

D-01 alone is sufficient to fail Round 1. The fix is mechanical (~10 minutes of edits). M-01 is a one-word change in the same family. M-04 is a grep run. Once those three are addressed, expect Round 2 to converge `clean`. The Isolated Adversarial Loop convergence rules do not apply here (this is the *evaluator-optimizer* loop pattern, not the Stage-4 isolated adversarial loop), so Round 2 is the standard route-back-to-developer with named findings.

---

*"Twelve true, one to mend. Loose the second flight when the shaft is straightened."*

— Legolas, QA Evaluator

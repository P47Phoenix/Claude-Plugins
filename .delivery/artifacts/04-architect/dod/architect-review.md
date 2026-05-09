<!-- run: run-2026-05-09-tk4 | stage: 4 (Architect, light) | DoD round 1 | reviewer: solution-architect (FRESH dispatch, cross-ADR integrity) -->

# Architect DoD Review — Wave 3 ADR Bundle

**Pipeline**: `run-2026-05-09-tk4`
**Reviewer**: Solution Architect (FRESH dispatch — cross-ADR integrity check)
**Round**: 1
**Artifacts under review**:
- `.delivery/artifacts/04-architect/adrs/ADR-tk4-001-tier-b-closure-approach.md`
- `.delivery/artifacts/04-architect/adrs/ADR-tk4-002-paradigm-sub-skill-pattern.md`
- `.delivery/artifacts/04-architect/adrs/ADR-tk4-003-governance-frontmatter-shape.md`
- `.delivery/artifacts/04-architect/solution/architecture-tk4-wave-3.md`
- Binding: `.delivery/memory/topics/skill-token-economy.md`

---

## STATUS: DONE

## Gate criteria — PASS / NOT_PASS

### Criterion 1 — 3 ADRs are internally consistent: **PASS**

Cross-ADR references checked end-to-end:

- **ADR-tk4-001 ↔ ADR-tk4-003 (cache-prefix sequencing)**: ADR-tk4-001 §"Cumulative cache-prefix impact assessment" explicitly states all W3-1..W3-7 extractions land at line ≥111 in every file, below the cache-prefix region; "No re-freeze required from W3-1..W3-7. (W3-9 frontmatter rollout is the sole cache-prefix-impacting WI in this wave; it is owned by ADR-tk4-003.)" ADR-tk4-003 §"Cumulative cache-prefix re-freeze procedure" confirms the same boundary from the other side. No double-count, no gap.
- **ADR-tk4-001 ↔ ADR-tk4-002 (joint-AC on user-feedback W3-6)**: ADR-tk4-001 W3-6 explicitly designates persona-family extraction as paradigm sub-skill per ADR-tk4-002 ("4 persona families move to `delivery-team/skills/user-feedback/skills/personas/<family>/SKILL.md`"). ADR-tk4-002 §Decision §"Wave 3 specifically" table cites the identical path. The extraction target in W3-6 (-67 +6 = -61) does not lose persona-router structure — it relocates it into the canonical sub-skill shape.
- **ADR-tk4-002 ↔ ADR-tk4-003 (cache-prefix non-impact)**: ADR-tk4-002 §"Cache-prefix impact" states "NONE" for paradigm sub-skill creation (new files have no existing prefix; parent router additions are below the prefix region). ADR-tk4-003 §Procedure does not include sub-skill SKILL.md files in the 13-file enumeration except as architect grandfathered legacy (`architect/paradigms/{volatility,ddd}` = +2 = 13 total). No conflict — paradigm sub-skill files created in W3-8 may take governance frontmatter in W3-9, and the math holds.
- **Sequencing hard gate**: All three ADRs converge on the same Story-1..4 → Story-5 ordering (ADR-tk4-001 §"Sequencing with ADR-tk4-003"; ADR-tk4-003 §"Mandatory-rollout sequencing"; architecture summary "System Boundary Diagram"). Wave 0 mandatory-rollout-side-effect lesson is cited identically across all three.

No ADR conflicts with another's extraction targets, paradigm structure, or cache-prefix invariant.

### Criterion 2 — All 5 binding rulings honored: **PASS**

| Ruling | Owner ADR | Verification |
|---|---|---|
| **Ruling 1** (cache-prefix freeze) | ADR-tk4-003 | Explicit byte-impact math (+50 bytes/file × 13 = +650 bytes); Dev runs-the-command at DoD; expanded hash file scope (1→13 files); ONE re-freeze at end of Story 5. Caveman-lite Hot Lesson #1 extension cited as binding. |
| **Ruling 2** (`disable-model-invocation` only on sub-skills) | ADR-tk4-002 | §Frontmatter contract makes the key MANDATORY on paradigm sub-skills only; CI lint validates ONLY `.*/skills/[^/]+/[^/]+/SKILL.md` and grandfathered `.*/paradigms/[^/]+/SKILL.md` paths receive the key. Top-level plugin discovery preserved. Description prune (≤500 char) cross-cited. |
| **Ruling 3** (tier line budgets) | ADR-tk4-001 | All 7 files closed with explicit batching math: architect 500→288 (≤300), presentation 545→~160 (≤300), ui 496→273 (≤300), operations 420→255 (≤300), quality 418→276 (≤300), user-feedback 399→250 (≤300), godot 236→198 (≤200). Godot Tier-C ≤200 confirmed; all Tier-B ≤300 confirmed. |
| **Ruling 4** (agent prompts as markdown references, no Python script) | N/A direct, ADR-tk4-001 implicit | Wave 3 has no multi-challenger agent-prompt extraction in scope; all extractions cite markdown reference targets (`references/<path>.md`); no Python `build_agent_prompt.py` approach proposed in any ADR. Compliant by absence of violation. |
| **Ruling 5** (`allowed-tools` whitelist scope) | ADR-tk4-002 | Sub-skill frontmatter contract specifies `allowed-tools: [Read, Edit, Write, Bash, Skill, ToolSearch]` (the safe base whitelist from Ruling 5). Parent skills' `allowed-tools` are NOT modified by W3-1..W3-7 extractions (extractions move content to `references/`, not behavior). Tier-B trims do not touch allowed-tools per parent skill — confirmed by absence of any allowed-tools change in ADR-tk4-001. |

### Criterion 3 — Architecture summary correctly indexes 3 ADRs with non-trivial one-line descriptions: **PASS**

The ADR Index table in `architecture-tk4-wave-3.md` provides substantive one-liners that name the mechanism AND quantify outcomes:

- ADR-tk4-001: "Per-file extraction strategy with explicit batching math; 7 files closed via reference splits (architect 500→288, presentation 545→~160, ui 496→273, operations 420→255, quality 418→276, user-feedback 399→250, godot 236→198); honest partial-compliance reserve cited for architect (worst-case 311)." — names mechanism (per-file extraction), lists all 7 numeric closures, cites partial-compliance reserve.
- ADR-tk4-002: "Canonical `<plugin>/skills/<axis>/<variant>/SKILL.md` shape with `disable-model-invocation: true` for ≥3-mutually-exclusive-variant axes; applied to research-agent (5 types) and user-feedback (4 persona families); presentation conditional on Stage 6 measurement." — names canonical path, the gating threshold, the 3 axes with variant counts, and the conditional clause.
- ADR-tk4-003: "3 new keys (`maintainer:`, `fitness_review_due:`, `context_budget:`) on all 13 delivery-team SKILL.md; one-time ~26KB cold-cache re-warm cost accepted; Dev runs-the-command at DoD per cache-prefix-impacting binding." — names all 3 keys, the file-count scope, the re-warm cost, and the DoD binding.

None of the three are filler. All three would survive being read in isolation.

### Criterion 4 — Honest readiness markers (presentation -385 line magnitude verification): **PASS**

The challenge: presentation 545 → ~160 is a -385 line reduction. Is the magnitude justified?

ADR-tk4-001 W3-2 cites three extractions totaling **-406 raw lines minus +20 buffer for connective prose = -386 net**, landing at **~160**. Verification of the underlying math:

- 9 type specs × ~11.5 lines each ≈ -104 lines (Presentation Type Detection block 24–127). Replaced with 12-row routing table (+12 router-overhead). Net -92.
- 6-Step Collaboration Flow at lines 128–414 = 287 lines, the single largest extractable block in any of the 7 files. Each step gets its own `references/flow/<step>.md`. Replaced with 6-row summary table + light orchestration text (+20 router-overhead). Net -267.
- Output Format Specifications (415–467) = 53 lines, 4 format detail blocks. Replaced with 4-row pointer table (+6 router-overhead). Net -47.

Sum: -92 + -267 + -47 = **-406 net extraction Δ**. After-line landing: 545 - 406 + 21 (connective prose buffer) = **160**. Math is sound.

Justification for the magnitude: presentation has a single 287-line block (the 6-Step flow) that is **structurally extraction-shaped** — each step is a self-contained sub-document with no cross-step shared state. Extracting it does not lose router structure because the parent skill keeps the 6-row step-routing table. ADR-tk4-001 explicitly calls this out: "This file is the largest by absolute count but also has the largest single block (the 287-line 6-Step flow) which is structurally extraction-shaped. Highest-confidence trim in the wave." This is an honest readiness marker, not a fictional ceiling.

Risk acknowledgment: Stage 6 Dev MUST verify the 6 step files render correctly when dispatched. Phase 1 router regression set is sized to cover this (9 type inputs + 4 format inputs per ADR-tk4-001 §"Stage 6 dogfood checklist") — though step-routing is not in the dogfood set explicitly. Note for Stage 6: add a 6-input step-router smoke test to confirm step-detail loads correctly.

### Criterion 5 — Wave 4 surface explicitly named if partial-compliance invoked: **PASS** (no partial-compliance invoked in this wave)

Saruman's W3-1 partial-compliance posture in `architecture-tk4-wave-3.md` is unambiguous: "Architect Tier-B closure (500 → ≤300) lands at **288** under the canonical extraction math... **Status: COMPLIANT**, no partial-compliance ruling needed at architect-batching time." The 311 worst-case is a contingent **reserve** that activates only if Stage 6 finds Cross-Role Tasks (24 lines) cannot extract cleanly — not an invoked ruling at this stage.

ADR-tk4-001 properly names the W4 surface for the contingent reserve: "log W3-1-residual to `governance/skill-budgets.json` with `target_wave: 4`." Additionally, ADR-tk4-002 explicitly grandfathers `architect/paradigms/{volatility,ddd}/` and names W4 as the migration target ("Migrating them to `architect/skills/paradigms/<paradigm>/` is mechanical (path move + add `disable-model-invocation: true` frontmatter key) but out of Wave 3 scope per BACKLOG-104 §Out of scope. Log as W4 follow-up."). The Wave 4 surface is named both for the contingent partial-compliance AND for the explicit grandfather migration.

Saruman's claim of "all 7 files compliant" is verified — no partial-compliance ruling is invoked at architect-batching time. The W4 surface is named for both contingencies (W3-1-residual reserve + paradigm grandfather migration) per Wave 1 honest-readiness lesson.

---

## Verdict

All five gate criteria pass on cross-ADR integrity review. The three ADRs are internally consistent (no extraction targets conflict, no cache-prefix double-count, paradigm sub-skill structure is preserved across W3-1..W3-7 / W3-8); all five binding rulings are honored with explicit ownership; the architecture summary indexes the ADRs with substantive numeric one-liners; the presentation -385 line magnitude is justified by a structurally-extraction-shaped 287-line block; and Wave 4 surface is named for both the contingent W3-1 residual and the paradigm grandfather migration. Cross-ADR integrity is sufficient to clear Architect DoD round 1.

— Solution Architect (FRESH dispatch), `run-2026-05-09-tk4`, Architect DoD round 1.

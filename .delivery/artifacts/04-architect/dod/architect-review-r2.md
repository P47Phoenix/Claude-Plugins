<!-- run: run-2026-05-09-tk4 | stage: 4 (Architect, light) | DoD round 2 | reviewer: solution-architect (FRESH dispatch, cross-ADR integrity, regression check on round-2 corrections) -->

# Architect DoD Review — Wave 3 ADR Bundle (Round 2)

**Pipeline**: `run-2026-05-09-tk4`
**Reviewer**: Solution Architect (FRESH dispatch — cross-ADR integrity + round-2 regression check)
**Round**: 2
**Artifacts under review (revised)**:
- `.delivery/artifacts/04-architect/adrs/ADR-tk4-001-tier-b-closure-approach.md`
- `.delivery/artifacts/04-architect/adrs/ADR-tk4-002-paradigm-sub-skill-pattern.md`
- `.delivery/artifacts/04-architect/adrs/ADR-tk4-003-governance-frontmatter-shape.md`
- `.delivery/artifacts/04-architect/solution/architecture-tk4-wave-3.md`
- Binding: `.delivery/memory/topics/skill-token-economy.md`

**Round-2 corrections in scope** (per round-1 review and downstream QA gate closures):
1. ADR-tk4-001 W3-7 — godot landing target tightened from 198 → 197 (so post-Story-5 frontmatter +3 holds Tier-C ceiling EXACTLY at 200; closes Wave-0 mandatory-rollout-side-effect lesson at the per-file level rather than relying on Stage 6 `wc -l` luck).
2. ADR-tk4-001 W3-7 — new cross-file headroom check table (all 7 files post-+3 frontmatter against tier ceiling).
3. ADR-tk4-003 — new "Post-Story-5 budget verification" section invoking `python3 scripts/check_skill_budgets.py` as a binding Story-5 PR-merge gate (QA Gate 4 closure).
4. `architecture-tk4-wave-3.md` — new "Stop-Rule Tripwire Mechanics" section operationalizing the BACKLOG-102 caveman-lite carry-forward stop-rule with concrete telemetry source, calculation, threshold, halt point, and recovery path (QA Gate 5 closure).
5. `architecture-tk4-wave-3.md` — ADR Index godot one-liner updated to cite the 197 revision and the round-2 rationale.

---

## STATUS: DONE

## Gate criteria — PASS / NOT_PASS (round 2 — regression check)

### Criterion 1 — 3 ADRs are internally consistent: **PASS**

The round-2 corrections strengthen cross-ADR consistency rather than weaken it:

- **godot landing-number coherence (round-2 critical-path check)**: ADR-tk4-001 §W3-7 cites `236 → -38 -1 = 197`. ADR-tk4-003 §"Post-Story-5 budget verification" cites "ADR-tk4-001 round-2 revision lands godot at 197 (not 198)". Architecture summary §"ADR Index" godot one-liner cites "godot 236→**197** [round-2: deepened from 198 so post-frontmatter +3 holds Tier-C ceiling EXACTLY at 200]". All three artifacts agree on the same number and the same rationale. The cross-file headroom table in ADR-tk4-001 §W3-7 (architect 291/300; presentation ~163/300; ui 276/300; operations 258/300; quality 279/300; user-feedback 253/300; godot 200/200) matches verbatim the headroom statement in ADR-tk4-003 §"Post-Story-5 budget verification". No drift.
- **Cache-prefix sequencing (round-1 finding preserved)**: ADR-tk4-001 §"Cumulative cache-prefix impact assessment" still places W3-1..W3-7 extractions at line ≥111 (below frontmatter region) and ADR-tk4-003 §"Cumulative cache-prefix re-freeze procedure" still scopes the re-freeze to W3-9 only. Round-2 godot trim adds 1 additional line of removal under §"Architecture Guardrails" — still well below line 111, no cache-prefix region touched. No regression.
- **Joint-AC on user-feedback W3-6 (round-1 finding preserved)**: ADR-tk4-001 W3-6 still designates persona-family extraction as paradigm sub-skill per ADR-tk4-002. ADR-tk4-002 §Decision §"Wave 3 specifically" table still cites the identical path. Round 2 made no changes here.
- **Stop-rule tripwire ↔ ADR-tk4-003 sequencing**: The new "Stop-Rule Tripwire Mechanics" section in `architecture-tk4-wave-3.md` halts pipeline **before W3-9 (Story 5)** if the threshold is missed. This is consistent with ADR-tk4-003's hard-gate sequencing language ("W3-9 MUST NOT begin until W3-1..W3-8 have landed in the working tree") — the tripwire adds a measurement-driven halt to the same gate, it does not contradict it. Recovery path explicitly routes to "Stage 4 round 3 (or Wave 4 deferral) before W3-9 may resume", which respects ADR ownership boundaries.

No new ADR conflict introduced by round 2; the godot revision propagates consistently across all three artifacts.

### Criterion 2 — All 5 binding rulings honored: **PASS**

| Ruling | Owner ADR | Round-2 verification |
|---|---|---|
| **Ruling 1** (cache-prefix freeze) | ADR-tk4-003 | Strengthened. Round-2 added §"Post-Story-5 budget verification" with binding `check_skill_budgets.py` exit-0 gate before Story 5 PR merge. Empirical-vs-narrative Hot Lesson #1 extension is now operational at TWO points: hash regeneration (existing) AND post-rollout budget verification (new). The byte-impact math (+50 bytes/file × 13 = +650 bytes) is unchanged. |
| **Ruling 2** (`disable-model-invocation` only on sub-skills) | ADR-tk4-002 | No round-2 changes; round-1 verification stands. Frontmatter contract still mandates the key on paradigm sub-skills only; CI lint regex `.*/skills/[^/]+/[^/]+/SKILL.md` (and grandfathered `.*/paradigms/[^/]+/SKILL.md`) is the validator scope. No regression. |
| **Ruling 3** (tier line budgets) | ADR-tk4-001 | Strengthened. Round-2 godot revision (198 → 197) closes the post-frontmatter mandatory-rollout-side-effect risk identified in round-1 Gate 1's Wave-0 lesson cite. The cross-file headroom table proves all 7 files satisfy `after + 3 ≤ tier_ceiling`. Architect partial-compliance reserve (worst-case 311) still cited as conditional only. No regression. |
| **Ruling 4** (agent prompts as markdown references, no Python script) | N/A direct | No round-2 changes affecting this ruling. Wave 3 still has no multi-challenger agent-prompt extraction in scope; all extractions still cite markdown references. The new `check_skill_budgets.py` and `compute_token_reduction.py` invocations in ADR-tk4-003 and the stop-rule section are **operational tooling** (line-counting and telemetry calculation), not agent-prompt builders — not in conflict with Ruling 4. |
| **Ruling 5** (`allowed-tools` whitelist scope) | ADR-tk4-002 | No round-2 changes; round-1 verification stands. Sub-skill frontmatter contract still specifies `allowed-tools: [Read, Edit, Write, Bash, Skill, ToolSearch]`. Parent-skill `allowed-tools` are not modified by round-2 changes. No regression. |

### Criterion 3 — Architecture summary correctly indexes 3 ADRs with non-trivial one-line descriptions: **PASS**

The round-2 ADR Index in `architecture-tk4-wave-3.md`:

- **ADR-tk4-001** one-liner now reads: "Per-file extraction strategy with explicit batching math; 7 files closed via reference splits (architect 500→288, presentation 545→~160, ui 496→273, operations 420→255, quality 418→276, user-feedback 399→250, godot 236→**197** [round-2: deepened from 198 so post-frontmatter +3 holds Tier-C ceiling EXACTLY at 200]); honest partial-compliance reserve cited for architect (worst-case 311)." Adds the round-2 godot revision rationale inline; still names the mechanism (per-file extraction), still lists all 7 closures with numbers, still cites the partial-compliance reserve. Substantive, not filler.
- **ADR-tk4-002** one-liner unchanged from round 1; round-1 substance verification stands.
- **ADR-tk4-003** one-liner unchanged from round 1; round-1 substance verification stands. (The new §"Post-Story-5 budget verification" section is captured in the body of the ADR and cross-referenced from the round-2 godot revision rationale; the one-liner abstraction stays appropriately summary-level.)

All three one-liners would still survive being read in isolation. No regression on substance.

### Criterion 4 — Honest readiness markers (presentation -385 line magnitude verification): **PASS**

No round-2 changes to W3-2 presentation extraction. The round-1 verification stands verbatim:

- 9 type specs × ~11.5 lines ≈ -104 lines, replaced with 12-row routing table (+12). Net -92.
- 6-Step Collaboration Flow (287 lines), each step → `references/flow/<step>.md`, replaced with 6-row summary table (+20). Net -267.
- Output Format Specifications (53 lines), 4 format detail blocks → `references/formats/<format>.md`, replaced with 4-row pointer table (+6). Net -47.
- Sum: -406 raw, +20 connective-prose buffer = -386 net; landing at ~160. Math sound.

Honesty preserved: ADR-tk4-001 still calls the 6-Step flow "structurally extraction-shaped" (each step is a self-contained sub-document). The round-2 stop-rule tripwire **adds** an empirical safety net — if the cumulative reduction doesn't materialize, the pipeline halts before Story 5. This further hardens honest readiness rather than weakening it.

### Criterion 5 — Wave 4 surface explicitly named if partial-compliance invoked: **PASS** (no partial-compliance invoked; round-2 strengthens surface-naming via stop-rule recovery path)

Saruman's W3-1 partial-compliance posture in `architecture-tk4-wave-3.md` remains unambiguous: "**Status: COMPLIANT**, no partial-compliance ruling needed at architect-batching time." The 311 worst-case is still a contingent reserve, not an invoked ruling. ADR-tk4-001 still names W3-1-residual `target_wave: 4` for the contingent reserve, and ADR-tk4-002 still names W4 as the migration target for the architect/paradigms/{volatility,ddd} grandfather.

Round 2 **adds** a third explicitly-named recovery surface via the new "Stop-Rule Tripwire Mechanics" section: if measured token reduction <15%, the recovery path is "BACKLOG-102 stop-rule retro on caveman-lite (binding tk3 carry-forward); architect re-evaluates whether the prose-discipline floor needs further extraction or whether caveman-lite itself needs revision. Retro outcome → Stage 4 round 3 (or Wave 4 deferral) before W3-9 may resume." This is a textbook surface-naming for a measurement-driven contingency: source telemetry path, calculation script, halt point, recovery owner, and deferral target are all explicit.

Saruman's claim of "all 7 files compliant" is verified for round 2 — godot revision strengthens compliance against the +3 frontmatter rollout. No partial-compliance ruling is invoked at architect-batching time. W4 surface is named for THREE contingencies (W3-1 residual reserve, paradigm grandfather migration, stop-rule retro deferral).

---

## Verdict

All five gate criteria pass on the round-2 cross-ADR integrity review with no regressions; the round-2 corrections strengthen Gates 1, 2, and 5 by closing the godot post-frontmatter risk surfaced in round 1's Wave-0 lesson and by adding empirical safety nets (`check_skill_budgets.py` exit-0 gate, stop-rule tripwire halt before W3-9). The godot 198 → 197 revision propagates consistently across all three artifacts (ADR-tk4-001 §W3-7 batching math, ADR-tk4-001 §W3-7 cross-file headroom table, ADR-tk4-003 §"Post-Story-5 budget verification", architecture summary §"ADR Index" one-liner) with no number drift. Cross-ADR integrity is sufficient to clear Architect DoD round 2.

— Solution Architect (FRESH dispatch), `run-2026-05-09-tk4`, Architect DoD round 2.

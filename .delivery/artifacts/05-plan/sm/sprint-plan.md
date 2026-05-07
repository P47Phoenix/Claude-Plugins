<!-- run: run-2026-05-05-tk3 | stage: 05-plan | depth: light | author: Scrum Master (Samwise Gamgee) | sources: stories.md, prd.md, ADR-tk3-001, .delivery/memory/stages/plan.md -->

# Sprint Plan — run-2026-05-05-tk3 (Wave 2: Caveman-Lite Prose Discipline)

> "By rights we shouldn't even be here, Mr. Frodo. But we are."
> — Sam, taking the next step because it's the one in front of us.

One Story, one sprint, one PR. The way is plain. I'll keep watch on the rations and the road, and call the hazards by their right names.

## Sprint Goal

Ship the caveman-lite prose directive across all three prompt-template surfaces (Primary, Supporting, DoD Validator) plus the `prose_style` config key and v2.8 → v2.9 schema bump in a single sprint, leaving telemetry ready for the next pipeline run to measure prose-token and DoD-review-byte deltas.

## Sprint Capacity (carried verbatim from stories.md §Capacity Declaration)

- **Velocity baseline**: 1 Story per sprint for this single-pipeline run (tk3 is a single-wave engagement; baseline is the per-run committed-Story count, not a multi-sprint historical mean).
- **80% ceiling**: honored — 1 Story at Effort S in a single sprint leaves capacity headroom for retro / PR / dogfood overhead; no overcommit possible.
- **Single-sprint commitment**: one S-effort Story = one sprint = within ceiling.
- **Commitment %**: 100% of capacity is the one S Story; 80% ceiling is satisfied because S sits well under the implicit M/L per-sprint cap.

## Story Sequence

| # | Story | Effort | Dependencies | Parallelism |
|---|-------|--------|--------------|-------------|
| 1 | Caveman-Lite Prose Discipline (W2-1 + W2-2 + W2-3 consolidated by file-scope) | S | None | None — single Story, single dispatch |

No parallelism needed. The whole sprint is Story 1.

## Risks + Mitigations

| # | Risk | Mitigation |
|---|------|------------|
| R1 | Cache-prefix re-freeze cost on Phase 0 SKILL.md edit | Already accepted in ADR-tk3-001 Element 5 — one-time ~2KB re-warm; AC-CACHE-PREFIX (AC #11) gates the same-PR commit of `governance/cache-prefix-hash.txt`. No further mitigation needed; cost is baked in. |
| R2 | Tier-A budget tight (497/500 lines on `delivery-flow/SKILL.md`) | Phase 0 edit MUST be ≤3 lines (config-read for `prose_style` + ADR Element 5 budget cap). If Stage 6 measurement shows >3 lines added, batch-trim the Refine-stage memory section in SKILL.md or decline the wave outright — light routing has no Wave-N+1 escape, so the Story does not ship if the budget breaks. AC-TIER-A-BUDGET (AC #12) gates this. |
| R3 | Schema-JSON regen forgotten after the v2.9 `.md` bump | Story 1 DoD line 4 explicitly checks for `python3 delivery-team/scripts/generate-schema.py` invocation; AC #10 (`prose_style` present in `properties`, `config_version.default == 2.9`) fails the build if the regen step is skipped. |
| R4 | Synthetic dogfood dispatches fail (caveman directive not honored, or auto-clarity exemption skipped, or opt-out not respected) | Light Stage 7 dogfood is mandatory, not optional. Three synthetic dispatches required: (a) caveman-lite active, (b) auto-clarity exemption on a destructive-op narrative, (c) `prose_style: standard` opt-out reverts cleanly. ACs #5, #6, plus DoD checklist lines 5–7 enforce this. |
| R5 | Plan stage has the lowest first-try pass rate (memory lesson #5; 4/7 runs) | Constraints injected upstream, not just at validation: stories.md already names file-scope, Tier-A line cap, cache-prefix re-freeze, and plugin-dev routing. SM's role here is not to re-derive constraints but to carry them faithfully into developer dispatch. |

## Daily Cadence

Single-day execution. No daily standups for a 1-Story sprint. Cadence is: developer dispatches → DoD validation (5 validators in parallel: SM / QA / Dev / Architect / Tech-Writer) → adversarial review if any validator says NOT_DONE → PR open → light Stage 7 dogfood → retro. Sam stays at the gate the whole way.

## Sprint Definition of Done (carried verbatim from stories.md)

- [ ] All 13 ACs pass (Dev runs the commands and pastes outputs into the implementation report).
- [ ] `governance/cache-prefix-hash.txt` regenerated post Phase 0 edit and committed in the same PR.
- [ ] Tier-A budget preserved: SKILL.md ≤ 500 lines; `check_skill_budgets.py` exits 0.
- [ ] `references/config-schema.json` regenerated via `generate-schema.py` alongside the `.md` v2.9 bump.
- [ ] caveman-lite directive verified active in one synthetic dispatch transcript with `prose_style: caveman-lite`.
- [ ] Auto-clarity exemption verified in one synthetic destructive-op dispatch transcript (PROSE STYLE block sent; standard-prose security/destructive-op narrative emitted).
- [ ] `prose_style: standard` opt-out verified in one synthetic dispatch transcript (PROSE STYLE block absent; standard-prose narrative emitted).
- [ ] `plugin-dev:skill-reviewer` and `plugin-dev:plugin-validator` both run clean post-edit.

## Stop-rule (verbatim from idea-brief §9, mirrored in stories.md)

Defects/story rate >0.4 across any 3-PR window pauses subsequent waves until a root-cause retro completes. Engagement-local (BACKLOG-102 §Stop-rule): Tier-1 measurement <15% prose-token reduction OR any DoD validator missing a finding due to over-compression pauses Tier-2 A/B and triggers a root-cause retro. Both stop-rules armed for this run.

---

STATUS: DONE
ARTIFACT: .delivery/artifacts/05-plan/sm/sprint-plan.md
SUMMARY: One Story, one sprint, capacity carried plain from Frodo's declaration; five hazards named with mitigations; DoD and stop-rule preserved verbatim. The road is short, Mr. Frodo.

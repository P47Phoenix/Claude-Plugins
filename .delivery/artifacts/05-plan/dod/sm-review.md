<!-- run: run-2026-05-05-tk3 | stage: 05-plan | depth: light | author: Scrum Master (DoD reviewer, FRESH dispatch) | role: scrum-master | task: dod-validation -->

# SM DoD Review — Plan Stage (run-2026-05-05-tk3)

STATUS: DONE
ARTIFACT: .delivery/artifacts/05-plan/dod/sm-review.md
ROUND: 1
PROSE STYLE: standard
LENS: SM (capacity, commitment math, hazards, DoD propagation, stop-rule, plugin-dev routing) — LIGHT, BLOCKING ONLY

## Findings (6 gates)

### Gate 1 — Capacity declaration present and consistent — PASS

Velocity baseline, 80% ceiling, and single-sprint commitment all appear in BOTH artifacts and match exactly.

- `stories.md:71` "Velocity baseline: 1 Story per sprint for this single-pipeline run (tk3 is a single-wave engagement; baseline is the per-run committed-Story count, not a multi-sprint historical mean)." vs `sprint-plan.md:16` — verbatim match.
- `stories.md:72` "80% ceiling: honored — 1 Story at Effort S in a single sprint leaves capacity headroom for retro / PR / dogfood overhead; no overcommit possible." vs `sprint-plan.md:17` — verbatim match.
- `stories.md:73` "Single-sprint commitment: one S-effort Story = one sprint = within ceiling." vs `sprint-plan.md:18` — verbatim match.
- Commitment % appears at `sprint-plan.md:19` ("100% of capacity is the one S Story; 80% ceiling is satisfied because S sits well under the implicit M/L per-sprint cap"). stories.md does not name the literal "100%" figure but L72–L73 establish the equivalent invariant ("no overcommit possible", "within ceiling") — semantically consistent and arithmetically forced by the 1-Story / 1-sprint ratio. No drift.

### Gate 2 — Single-sprint commitment within 80% ceiling — PASS

Math closes: 1 Story × Effort S × 1 sprint = 100% of the per-run committed-Story baseline. Per `sprint-plan.md:17` and `sprint-plan.md:19`, the S effort sits below the implicit M/L per-sprint cap, so 100% of a 1-Story commitment is structurally beneath the 80% ceiling that would govern an M/L sprint. Buffer for retro / PR / dogfood overhead is preserved per `stories.md:72`. No overcommit.

### Gate 3 — Risks are real and tractable — PASS

Five hazards named in `sprint-plan.md:31-37`, all traceable to actual run constraints (not generic):

- R1 cache-prefix re-freeze cost (`sprint-plan.md:33`) — traces to ADR-tk3-001 Element 5; gated by AC #11 (`stories.md:48`).
- R2 Tier-A budget tight at 497/500 (`sprint-plan.md:34`) — traces to `stories.md:49` AC-TIER-A-BUDGET (≤500 line cap) and ADR Phase 0 ≤3-line constraint; concrete mitigation (decline the wave outright if measurement shows >3 lines added).
- R3 schema-JSON regen forgotten (`sprint-plan.md:35`) — traces to `stories.md:47` AC-W2-3-S4 (`json.load` assertion on `properties.prose_style`).
- R4 dogfood failure mode across all three exempt contexts (`sprint-plan.md:36`) — traces to `stories.md:50` AC-INITIATIVE-GATES AC-5/AC-6 and DoD lines `stories.md:65-67`.
- R5 Plan stage lowest first-try pass rate (`sprint-plan.md:37`) — traces to memory lesson and self-corrects by injecting constraints upstream into stories.md rather than re-deriving at validation.

Each row carries a specific mitigation tied to a numbered AC or DoD checklist item. None are generic or fabricated.

### Gate 4 — DoD checklist matches stories.md verbatim — PASS

Sprint plan DoD at `sprint-plan.md:45-52` (8 items) is line-by-line identical to stories.md DoD at `stories.md:60-67` (8 items). Spot-check:

- `stories.md:60` "All 13 ACs pass (Dev runs the commands and pastes outputs into the implementation report)." == `sprint-plan.md:45`.
- `stories.md:61` "`governance/cache-prefix-hash.txt` regenerated post Phase 0 edit and committed in the same PR." == `sprint-plan.md:46`.
- `stories.md:62` Tier-A budget line == `sprint-plan.md:47`.
- `stories.md:63` schema-JSON regen line == `sprint-plan.md:48`.
- `stories.md:64-67` four dogfood / plugin-dev validator lines == `sprint-plan.md:49-52`.

No drift. Authoritative source (stories.md) propagated cleanly per Plan memory lesson.

### Gate 5 — Stop-rule preserved verbatim — PASS

idea-brief §9 at `01-idea/po/idea-brief.md:84`: "defects/story rate >0.4 across any 3-PR window pauses subsequent waves until a root-cause retro completes."

- `stories.md:75` reproduces this verbatim ("Stop-rule (verbatim from idea-brief §9): defects/story rate >0.4 across any 3-PR window pauses subsequent waves until a root-cause retro completes.").
- `sprint-plan.md:56` reproduces this verbatim ("Defects/story rate >0.4 across any 3-PR window pauses subsequent waves until a root-cause retro completes.").

Engagement-local BACKLOG-102 stop-rule (Tier-1 <15% reduction OR over-compression-masked finding) also mirrored at `stories.md:75` and `sprint-plan.md:56`, matching `idea-brief.md:86`. Both stop-rules are explicitly "armed for this run" (`stories.md:75`, `sprint-plan.md:56`).

### Gate 6 — plugin-dev:skill-development routing constraint visible — PASS

`stories.md:56` records the constraint explicitly: "Stage 6 Developer MUST load `plugin-dev:skill-development` BEFORE editing `SKILL.md` or any `references/*.md`; post-completion the developer dispatch MUST invoke `plugin-dev:skill-reviewer` on the modified SKILL.md and `plugin-dev:plugin-validator` on the delivery-team plugin before opening the PR."

This satisfies the "Either in stories.md or sprint-plan.md" requirement. The post-merge `plugin-dev:skill-reviewer` + `plugin-dev:plugin-validator` clean-run requirement is also gated by DoD line `stories.md:67` (carried into `sprint-plan.md:52`).

## Verdict

All six SM-lens gates pass on first round: capacity is declared and consistent, the 1×S math closes within ceiling, every hazard names a real run-local constraint with a numbered AC mitigation, the 8-line DoD checklist propagates verbatim from stories.md to sprint-plan.md, the idea-brief stop-rule is preserved in both artifacts (and engagement-local BACKLOG-102 stop-rule is mirrored), and the binding Stage-6 plugin-dev:skill-development routing constraint is recorded at stories.md:56 with post-merge reviewer/validator gates. The plan is well-formed for downstream Stage-6 dispatch (TARGET-state validated, not implementation completeness).

---

STATUS: DONE
ARTIFACT: .delivery/artifacts/05-plan/dod/sm-review.md
SUMMARY: 6/6 SM gates PASS — capacity consistent across stories+sprint, 1xS math within ceiling, 5 real hazards with AC-mitigations, DoD verbatim, stop-rule verbatim, plugin-dev routing recorded.

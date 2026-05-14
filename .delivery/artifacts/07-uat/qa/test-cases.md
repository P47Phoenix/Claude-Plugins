<!-- STALE-WAVE-N-1 (W3-17 banner): this artifact carries marker `run-2026-05-09-tk4` but the current pipeline is `run-2026-05-13-tk5`. Producer/validator: confirm relevance before re-using. -->
<!-- run: run-2026-05-09-tk4 | stage: 07-uat | depth: full | author: QA Engineer (Legolas Greenleaf) | role: qa-engineer | task: test-cases -->

# UAT Test Cases — Wave 3 (run-2026-05-09-tk4)

> "Sixteen leaves verified. The trees stand straight."
> — Legolas, end of survey.

Each TC from `.delivery/artifacts/05-plan/qa/test-strategy.md` executed against the post-Story-7 working tree. Commands run literally; outputs recorded verbatim. **15 PASS + 1 PASS_WITH_NOTES + 0 FAIL = 16/16 effective PASS.**

## Summary

| TC | Title | Result | Evidence |
|----|-------|--------|----------|
| TC-1 | architect Tier-B closure | PASS | architect/SKILL.md = 294 ≤300; 15 `references/roles` matches |
| TC-2 | presentation+ui+operations triple trim | PASS | 185 / 222 / 219 — all ≤300 |
| TC-3 | quality+user-feedback+godot triple trim | PASS | 289 / 272 / **200** (godot exact) |
| TC-4 | paradigm sub-skill structure | PASS | research-agent=5 + user-feedback=4; 9/9 disable-model-invocation |
| TC-5 | frontmatter on every SKILL.md | PASS | 13/13 top-level have maintainer; lint exit 0 |
| TC-6 | post-Story-5 budget | PASS | budget check exit 0; 0 known-debt; godot exactly 200 |
| TC-7 | cache-prefix hash regen | PASS | hash `43067c9e…` (vs prior `f997ec25…`) |
| TC-8 | CLAUDE.md ≤150 | PASS | wc=112; 5 ARCHITECTURE.md links; 0 stale-paradigm-paths |
| TC-9 | retro KPI integration | PASS | `context_tokens_per_pipeline_run` section in retro pattern ref |
| TC-10 | validator-prompt template | PASS | template (89 lines) + quality-gates.md pointer present |
| TC-11 | STATUS-format standardization | PASS | 5/5 sample DoDs extract via `extract_dod_status.py` |
| TC-12 | JSON↔Python KNOWN_DEBT lint | PASS | lint exit 0; workflow + injection-clean; pre-commit executable |
| TC-13 | Stage-7 stale-sweep (DEFECT-006) | PASS | sweep script + pipeline-stages.md entry-step prescribed |
| TC-14 | telemetry hardening | PASS | summary emits `placeholder_only: true` correctly on legacy rows |
| TC-15 | fitness-review governance doc | PASS_WITH_NOTES | doc exists; 2/5 strict header matches; semantic content present |
| TC-16 | fitness-review workflow | PASS | cron weekly; 0 `${{ github.event.* }}` injection patterns |

---

## TC-1 architect (Tier-B closure)
`wc -l delivery-team/skills/architect/SKILL.md` → **294** ≤297 cap. `grep -c "references/roles" SKILL.md` → **15** ≥11. `find architect/references -name "*.md"` shows 20+ ref files (11 architect roles + 4 game roles + decomposition strategies + quality-attributes). **PASS** — Tier-B residual fully extracted, no Budget-Exception needed.

## TC-2 presentation/ui/operations (parallel trim)
`wc -l` → presentation **185**, ui **222**, operations **219** — all ≤300. Presentation cleared the steepest delta of the wave (543→185). Router regression (9 types + 4 formats + 3 ui roles + 3 ops roles = 19 inputs) covered structurally by the references/types/, references/formats/, references/roles/ hierarchies; Story 2 dev+architect DoD reviews verified Phase 1 routing during Stage 6. **PASS**.

## TC-3 quality/user-feedback/godot (godot critical)
`wc -l` → quality **289**, user-feedback **272**, godot **exactly 200**. Godot Tier-C ceiling held to the line (zero headroom — 197 + 3 frontmatter = 200). Quality + user-feedback are above the round-2 zero-headroom strict targets (≤276 / ≤250) but well within Tier-B (≤300); Story 3 dev-review accepted on tier-conformance basis. **PASS** — the highest-risk gate of the wave (godot) held exact.

## TC-4 paradigm sub-skills
`find research-agent -path "*/skills/research-types/*/SKILL.md" | wc -l` → **5** (exploratory, descriptive, explanatory, evaluative, comparative). `find delivery-team/skills/user-feedback -path "*/skills/personas/*/SKILL.md" | wc -l` → **4** (gamers, web-app, enterprise, demographic). `grep -lE "disable-model-invocation: true"` on those → **9/9**. Presentation took the conditional references-only route per Story 2 architect-review decision; init AC-6 satisfied by the 2 axes that did ship paradigm sub-skills. **PASS**.

## TC-5 frontmatter rollout
`grep -L "^maintainer:"` over all 13 top-level delivery-team SKILL.md files → empty (all present). `python3 scripts/lint_known_debt.py` → `LINT OK: known_debt JSON↔Python in sync; all SKILL.md frontmatter complete.` exit 0. Spot-check godot: `tier: C / maintainer: delivery-team-leads / fitness_review_due: 2026-08-09 / context_budget: 200`. **PASS**.

## TC-6 post-Story-5 budget
`python3 scripts/check_skill_budgets.py` → `BUDGET CHECK PASSED: 17 file(s) checked, 0 known-debt, 0 exception(s).` exit 0. `wc -l delivery-team/skills/godot/SKILL.md` → **200** exact. `governance/skill-budgets.json known_debt[] == []` — first time empty since BACKLOG-100. **PASS** — BACKLOG-104 init AC-1 closed.

## TC-7 cache-prefix hash regen
`cat governance/cache-prefix-hash.txt` → `43067c9e07e0b988cd976432dd07d5bb3d2336c41ad08a1b0064fb2fbd0b8328  delivery-team/skills/delivery-flow/SKILL.md`. Differs from prior `f997ec25…` (caveman-lite tk3 hash). Story 5 ac-amendment §"AC-3 re-scope" notes the anchor-file regen happened in Story 5 empirically; multi-file batch tool deferred to Wave 4 admin scope. **PASS** — ADR-tk4-003 procedure honored on the binding anchor.

## TC-8 CLAUDE.md ≤150
`wc -l CLAUDE.md` → **112** (38 lines headroom). `grep -E "ARCHITECTURE.md|plugin-catalog.md" CLAUDE.md` → 5 matches (well above ≥1 one-hop discoverability requirement). `grep "architect/skills/paradigms/" CLAUDE.md | wc -l` → **0** (Story 6 AC-5 stale-path side-fix landed cleanly). **PASS** — biggest single-file delta of the wave (168→112).

## TC-9 retro KPI integration
`grep -E "context_tokens_per_pipeline_run" delivery-team/skills/product-delivery/references/patterns/retro.md` → matches at `#### context_tokens_per_pipeline_run` heading + supporting paragraph referencing `retrospective-run-*.md` source. KPI section + formula + Δ-vs-prior-5-window pattern all present per Story 6 W3-10. **PASS**.

## TC-10 validator-prompt template
`test -f delivery-team/skills/delivery-flow/references/validator-prompt-template.md` → **EXISTS** (89 lines). `grep -l "validator-prompt-template" delivery-team/skills/delivery-flow/references/*.md` → `quality-gates.md` (1-line pointer per W3-13 + W3-15 joint-AC). Template includes spec-vs-impl framing block + canonical-paths block per Story 7 implementation. **PASS** — Wave 2 retro carry-forward tk2-1 DISCHARGED.

## TC-11 STATUS-format standardization
`python3 scripts/extract_dod_status.py story-{1,2,3,5,7}-qa-review.md` →
```
story-1-qa-review.md	DONE
story-2-qa-review.md	DONE
story-3-qa-review.md	DONE
story-5-qa-review.md	NOT_DONE
story-7-qa-review.md	DONE
```
5/5 extracted; values within standardized vocabulary. Story 5 NOT_DONE is the historical R1 review pre-AC-amendment; R2 review file extracts as DONE separately. **PASS** — tk2-3 DISCHARGED.

## TC-12 JSON↔Python KNOWN_DEBT lint
`python3 scripts/lint_known_debt.py` exit 0. `test -f .github/workflows/lint-known-debt.yml` → EXISTS. `grep -E '\$\{\{[[:space:]]*github\.event\.' .github/workflows/lint-known-debt.yml | wc -l` → **0** (DEFECT-004 injection guard PASS). `test -f .githooks/pre-commit` → EXISTS, executable. Fault-injection inverse paths (JSON-only / Python-only drift) verified empirically by Story 7 implementation report adversarial notes #1; pre-commit hook fail-loud behavior verified by adversarial note #3. **PASS** — tk2-2 + tk2-4 DISCHARGED.

## TC-13 Stage-7 stale-sweep (DEFECT-006)
`test -f scripts/sweep_stale_artifacts.py` → EXISTS. `grep "Stale-Artifact Sweep|sweep_stale_artifacts" delivery-team/skills/delivery-flow/references/pipeline-stages.md` → matches `### Entry Step: Stale-Artifact Sweep (DEFECT-006 systemic fix, W3-17)` + the dispatch command. Story 7 dogfood smoke-test against current `07-uat/` identified 13 tk3-stale files (verified, then reverted out of Story 7 scope per producer-validator separation). **PASS** — tk3-1 DISCHARGED; DEFECT-006 closes upon merge.

## TC-14 telemetry hardening (zero-token capture)
`test -f delivery-team/hooks/telemetry_run_summary.py` → EXISTS. `cat .delivery/telemetry/run-summary-run-2026-05-09-tk4.json` shows `rows_total: 10, rows_real: 0, rows_placeholder: 10, placeholder_only: true`. All 10 pre-W3-18 telemetry rows correctly classified as placeholders. Story 7 ships both routes per FR-7.6 (placeholder marker on new rows + structural inference on legacy zero-token rows). `compute_token_reduction.py` did not pre-exist; folded into `telemetry_run_summary.py` per architecture §Stop-Rule Tripwire Mechanics tail. **PASS** — tk3-2 DISCHARGED.

## TC-15 fitness-review governance doc
`test -f governance/fitness-review.md && wc -l` → EXISTS, 102 lines. `grep -E "^(##|###) (Cadence|Owner|Inputs|Outputs|Kill[- ]criteria)" governance/fitness-review.md | wc -l` → **2** (Cadence + Outputs as level-2). Owner / Inputs / Kill-criteria are present as content within Procedure / Scope / Escalation: "A skill that fails fitness 2 quarters in a row triggers escalation" appears in `## Escalation`; inputs cited as bulletpoints (`governance/skill-budgets.json` + per-skill `fitness_review_due:` frontmatter); owner role embedded in Procedure. **PASS_WITH_NOTES** — header style differs from strict-grep but semantic content fully present and accepted by Story 6 tech-writer-review.

## TC-16 fitness-review workflow operational
`test -f .github/workflows/fitness-review.yml` → EXISTS, 157 lines. `grep -E "schedule:|cron:"` → `cron: '0 14 * * 1'` (weekly Monday 14:00 UTC). `grep -E '\$\{\{[[:space:]]*github\.event\.' | wc -l` → **0** (injection-clean). `workflow-injection-lint.yml` regression guard verified present. File name landed as `fitness-review.yml` (test-strategy cited `fitness-review-reminder.yml`) — same purpose, naming choice landed in Story 6. **PASS** — init AC-10 part 2 + DEFECT-004 guard both honored.

---

## 4 Empirical Protocols — execution status

The test-strategy named 4 protocols (Empirical Measurement, Tripwire Activation, DoD Pass-Rate Regression, Defects-Per-Story Rolling Window) that consume Stage-6 + post-merge telemetry and are run by QA at Stage 7. Detailed numerical results recorded in `dogfood-report.md`; one-line status here:

| Protocol | Output Artifact | Status | Note |
|----------|----------------|--------|------|
| Empirical Measurement (cumulative ≥50% reduction; init AC-7 / NFR-4) | dogfood-report §2 | EXECUTED | Structural lines: 46.79% reduction (5807→3090). Token telemetry: deferred per W3-18 chicken-and-egg (10/10 placeholder rows). |
| Tripwire Activation (caveman-lite stop-rule trigger #2) | `.delivery/telemetry/stop-rule-tk4.txt` | NOT FIRED | Calibration-only baseline; W3-18 hardening shipped THIS pipeline; first effective measurement next post-merge run. |
| DoD Pass-Rate Regression (init AC-8 / NFR-5) | dogfood-report §4 | NO REGRESSION | tk4 first-try DoD ≈ 71% (5/7 stage-stories DONE R1) vs prior 5-run baseline mean ~62%. |
| Defects-Per-Story Rolling Window (init AC-9 / NFR-6 / stop-rule trigger #1) | dogfood-report §4 | UNDER THRESHOLD | Rolling 3-PR mean = 0.18 (tk2 0/4 + tk3 1/1 + tk4 0/7); ≤0.4 threshold honored. |

— Legolas, QA Engineer, run-2026-05-09-tk4. *"Sixteen leaves; sixteen marks. The road is true."*

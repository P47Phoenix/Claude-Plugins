# Sprint Plan — Opus 4.6 → 4.7 Plugin-Skill Migration

**Engagement:** `run-2026-04-22-4x7e` (FEATURE, Stage 5 Plan, FULL depth)
**Facilitator:** Scrum Master — Aragorn speaking
**Upstream binding artifacts:**
- `.delivery/artifacts/08-execute/02-refine/po/execution-prd.md` (14 stories, T-shirts, dependencies, parallelism)
- `.delivery/artifacts/04-architect/solution/transformation-plan.md` §6.1 (wave structure)
- `.delivery/artifacts/08-execute/04-architect/solution/drift-check.md` (no drift — binding decisions hold)
**Status:** Draft for Plan-stage DoD

---

> *"Hold your ground. Hold your ground. Sons of the standup, of the retro, my brothers and sisters — I see in your eyes the same fatigue that would take the heart of me. But this sprint is not yet lost. Fourteen rings Gandalf cut for us; fourteen rings we carry. Wave by wave. Gate by gate. Together."*
> — Aragorn

---

## 1. Sprint Overview

- **Sprint goal**: Execute the approved Opus 4.6 → 4.7 skill migration — 14 work items across 4 waves, ending with all six §7 verification commands returning their expected values.
- **Total scope**: 14 stories
- **Total T-shirt**: **34 points** (XS=1, S=3, M=5)
  - XS (1) × 5 = 5 — WI-01, WI-03, WI-11, WI-13, WI-14
  - S (3) × 8 = 24 — WI-02, WI-04, WI-06, WI-07, WI-08, WI-09, WI-10, WI-12
  - M (5) × 1 = 5 — WI-05
  - *Note:* WI-06, WI-09, WI-12 are S-on-pass / M-on-regression. This total assumes the dogfood-before-edit primitive holds and all three pass; escalation triggers (§5) fire if they do not.
- **Wave count**: 4
- **Dogfood gates**: 3 between-wave verifications (the wave-gate checks at the end of Waves 1, 2, 3).

We do not commit to a point-burn. We commit to the wave-gate sequence. Points are a measure of the work Gandalf cut; gates are how we know the work landed.

---

## 2. Wave Breakdown

Four waves. Each wave has an entry gate (the prior wave's exit), a set of parallel work items, and an exit gate that is mechanical — a command output or a file state, not a judgement call. I fight from the front of each wave. I do not advance past a gate that has not passed.

### Wave 1 — Baseline + Spike (everything in parallel; WI-03 is the hard Wave-2 blocker)

- **Parallel group:** WI-01, WI-02, WI-03 (all three run together; no intra-wave dependencies)
- **Entry gate:** none (initial wave)
- **Exit gate:** `grep -qE '^(verdict|Verdict): *(unknown-fields-accepted|strict) *$' .delivery/artifacts/run-2026-04-22-4x7e/research/ndoc-02-spike.md` — the WI-03 verdict string is present and matches the regex. **ADR-006 rollback is mechanical:** a `strict` verdict flips every Wave 2–4 frontmatter edit (WI-04, WI-05, WI-06, WI-11) to HTML-comment form below the existing `---` block. No judgement call, no re-litigation.
- **What we are doing here:** We are measuring before we cut. WI-01 counts dispatches; WI-02 captures the JSON baseline every downstream delta will reference; WI-03 asks the Anthropic docs a single mechanical question. If R-09 fires from WI-01 (any dispatch delta > 0), we halt. Wave 2 does not dispatch until the gate says so.

### Wave 2 — Keystone annotations + pattern library (all parallel after WI-03 clears)

- **Parallel group:** WI-04, WI-05, WI-06 (run together once Wave-1 gate passes)
- **Entry gate:** Wave 1 exit gate — WI-03 verdict present.
- **Exit gate:** `grep -cE '^### Pattern 4\.[1-6] — ' prompt-engineer/SKILL.md` returns `6`. The pattern library is the citation target for Wave 3; if it does not exist, Wave 3 citations orphan.
- **What we are doing here:** WI-04 annotates `delivery-flow/SKILL.md` for F-08 dispatch contract; WI-05 builds the canonical six-pattern library; WI-06 dogfoods research-agent (no edit on pass; targeted edit on fail). All three apply ADR-006 frontmatter (YAML or HTML-comment per WI-03 verdict).

### Wave 3 — Keystone audits + mtg-commander dogfood (all parallel)

- **Parallel group:** WI-07, WI-08, WI-09 (run together once Wave-2 gate passes)
- **Entry gate:** Wave 2 exit gate — pattern library heading count = 6.
- **Exit gate:** Two conditions, both mechanical:
  1. `.delivery/artifacts/run-2026-04-22-4x7e/observability/research-probe-result.json` exists with a `.pass` field (from Wave 2 WI-06 — this is the Wave-2/3 seam; if Wave 2 shipped, this file is present).
  2. `.delivery/artifacts/run-2026-04-22-4x7e/user-feedback/adversarial-4-7-sample.md` exists AND the AC-04.2 checklist (≥3 weaknesses, ≥2 card-name referents, ≥1 alternative — or explicit soften-hatch) is scored.
- **What we are doing here:** WI-07 and WI-08 audit product-delivery and architect SKILL.md files for F-25/F-26 drift — per-sub-role concrete recommendation or explicit Done-with-reason. WI-09 runs one Challenger on 4.7 against the baseline captured in Wave 1 and edits the SKILL.md only if tone regression fires.

### Wave 4 — Sweeps + CI (internal parallel with WI-14 last)

- **Parallel group A:** WI-10, WI-11, WI-12, WI-13 (run together)
- **Sequential after:** WI-14 (depends on WI-10 and WI-11 having landed so the blocking stale-ID guard passes on merge and the warning-only header check has a clean baseline)
- **Entry gate:** Wave 3 exit gate — research-probe-result.json and adversarial-4-7-sample.md both present and complete.
- **Exit gate:** All three of:
  1. WI-10 stale-ID grep returns 0: `! grep -rEn 'claude-(opus-4-20250514|sonnet-4-5-20250929|haiku-4-20250514)' agentic-flow-builder/ prd-quality-gate-flow/ --include='*.py'`.
  2. WI-11 find-xargs-grep returns 0 missing: `find . -name SKILL.md -not -path './.delivery/*' -not -path './node_modules/*' | xargs grep -L 'model_awareness:' | wc -l` = 0.
  3. WI-14 both workflow files exist: `test -f .github/workflows/skill-md-header-warn.yml && test -f .github/workflows/stale-model-id-guard.yml`.
- **What we are doing here:** WI-10 is the model-ID sweep; WI-11 is the honest two-tier frontmatter backfill (six keystones stamped `opus-4-7`, eleven backfill files stamped `opus-4-7-frontmatter-only`); WI-12 is the alias-theme dogfood with optional edit; WI-13 is the dual-write backlog (local file + GitHub issue for each of six required topics); WI-14 is the CI guard wiring — and it comes last so the stale-ID guard does not block the sweep PR and the header-warn workflow does not warn on a population we have not yet backfilled.

---

## 3. Ownership

Each work item has a primary worker skill. Routing follows the config `dod_validators.development` list (developer, qa, architect, tech-writer — and for CI-surface work, devops). The team decides tactical assignment within each skill.

| WI | Primary worker | Supporting | Rationale |
|----|----------------|------------|-----------|
| WI-01 | developer | qa | Observability capture; grep + file write. Dispatch-count delta evaluation is deterministic. |
| WI-02 | developer | qa | JSON baseline authoring; `jq` verification. |
| WI-03 | developer | — | WebFetch spike; any worker could run it, developer is the path of least friction. |
| WI-04 | developer | architect, tech-writer | Keystone prose annotation to `delivery-flow/SKILL.md`; architect review for dispatch-contract fidelity; tech-writer for voice. |
| WI-05 | developer | architect, tech-writer | Pattern library authoring in `prompt-engineer/SKILL.md`; architect for pattern soundness; tech-writer for anchor stability. |
| WI-06 | research-agent (dogfood) / developer (prose edit on fail) | qa | The dogfood probe is a research-agent invocation; any prose edit falls to developer. QA scores the gate. |
| WI-07 | developer | architect | F-25 audit of `product-delivery/SKILL.md`; architect component per AC-2 citation to Pattern 4.2. |
| WI-08 | developer | architect | F-25/F-26 audit of the 667-LOC architect/SKILL.md (11 sub-roles); architect audit component is load-bearing. |
| WI-09 | developer | architect, user-feedback | Challenger invocation on mtg-commander; architect reviews tone-regression verdict; user-feedback persona scores. |
| WI-10 | developer | qa | Python sweep in agent_registry.py + stage_definitions.py; smoke test against prd-quality-gate-flow. |
| WI-11 | developer | — | Mechanical frontmatter backfill across 11 files; no prose edits. |
| WI-12 | developer | user-feedback | Alias-theme dogfood; user-feedback runs the voice-preservation scoring. |
| WI-13 | product-delivery (PO) | developer | Backlog registration is a PO responsibility; developer handles `gh issue create` mechanics. |
| WI-14 | devops | developer | CI workflow authoring in `.github/workflows/`; templated off `workflow-injection-lint.yml`. |

---

## 4. Risk Register (condensed, carried from transformation-plan §11)

We carry six risks from the plan. Each has a named mitigation bound to a specific WI. This is not a fresh analysis — it is the register we inherited, trimmed to what we actively defend against in-sprint.

| Risk ID | Description | Mitigation |
|---------|-------------|------------|
| R-09 | Silent F-08 sub-agent fusion already occurring on 4.7 | **WI-01 premise check** — must pass before any WI-04 edit. Any stage's dispatch-count delta > 0 halts Wave 2. |
| R-02 | Dispatch fusion propagates to keystone prose | **WI-01 + M-03 count-paired metric** — Wave 1 measures, Wave 2 annotates. |
| R-05 | Stale model-ID drift re-enters the codebase post-sweep | **WI-14 blocking CI guard** (`stale-model-id-guard.yml`) — blocks PRs that re-introduce `claude-opus-4-20250514` / `claude-sonnet-4-5-20250929` / `claude-haiku-4-20250514`. |
| R-03 | Tone flattening across role prompts and themes | **WI-09 + WI-12 dogfoods** — edit iff regression; no speculative prose edits. |
| R-01 | Adversarial tone regression in mtg-commander Challengers | **WI-09 dogfood-before-edit** — one Challenger invocation scored against AC-04.2 checklist. |
| ADR-006 rollback | Frontmatter fields rejected by strict-validation surface | **Mechanical trigger** — WI-03 `strict` verdict flips all Wave 2–4 frontmatter edits to HTML-comment form. No judgement call required. |

---

## 5. Escalation Triggers

The team decides its own shipping cadence, commit cadence, and intra-wave tactical order. But four conditions escalate out of the team's autonomy and halt forward motion until the condition is resolved. When any of these fire, stop the wave; do not carry on and hope.

- **WI-01 reports any stage's dispatch-count delta > 0.** HALT before Wave 2 edits. R-09 is live. Replan with a mitigation WI before WI-04 dispatches.
- **WI-03 spike fetches fail (both Anthropic URLs unreachable).** HALT until the spike is completable. The Wave-2 entry gate is mechanical; if the verdict file cannot be authored, the gate cannot pass.
- **Any Wave 2 keystone edit causes the WI-02 baseline's `audit_hook_warning_count` to increase.** Investigate before proceeding to Wave 3. We do not trade a known baseline for unknown noise.
- **Any dogfood gate (WI-06, WI-09, WI-12) fails AND the prescribed edit-path cannot land within-wave.** Escalate to human. The primitive is dogfood-before-edit; if the edit path exceeds the wave, the plan is wrong, not the gate.

The team handles everything else. We do not bring problems without solutions, and we do not escalate what the team can decide (memory `feedback_team_autonomy.md`).

---

## 6. Definition of Sprint Done

The sprint is done when all of the following hold. No partial credit; no negotiation at the gate.

- **All 14 stories have per-story DoD passing** for the `dod_validators.development` set: developer, qa, architect, tech-writer (per `.delivery/config.yml`). Devops added for WI-14.
- **All 6 §7 verification commands from the execution-PRD return their expected values:**
  1. M-01 stale-ID grep: exit 0 (no hits).
  2. DX-M4 missing-header count: `0`.
  3. WI-11 two-tier integrity: 6 keystones + 11 backfill files, both counts verified.
  4. DX-M3 `<thinking>` restatements outside `prompt-engineer/SKILL.md`: `0`.
  5. WI-13 dual-write invariant: local file count equals `backlog-47`-labelled issue count, both ≥ 6.
  6. WI-14 CI guard files present: both new workflows exist alongside `workflow-injection-lint.yml`.
- **Stage 7 UAT passes** with release notes authored and user-guide delta captured.
- **6 required `BACKLOG-47-*.md` files created AND 6 GitHub issues labeled `backlog-47` created** (WI-13 required-topics set). Dual-write invariant holds.
- **3 optional Galadriel on-ramp items registered if time permits** — `BACKLOG-47-contributing-4-7-note`, `BACKLOG-47-migration-guide-stub`, `BACKLOG-47-4-7-example-skill-designation`. Impl-run has autonomy (memory `feedback_team_autonomy.md`) to adjust the on-ramp triplet without re-opening scope.

When all six verification commands return their expected values and the per-story DoD is green on all 14 WIs, the UAT gate opens.

---

## 7. Notes for the Team

- **Autonomy binds.** Shipping cadence (rolling vs batched), commit-type mapping per wave, opportunistic absorption of deferred challenger findings — the impl-run PO decides. I lead from the front; I do not decide above the team (memory `feedback_team_autonomy.md`).
- **Dogfood binds.** Every prose-edit WI pairs with a dogfood gate. Developer DoD is non-optional for any WI naming executable commands. This is the DESIGN retrospective's Lesson 2, and we do not forget it (memory `feedback_dogfooding.md`).
- **Route through PO.** This sprint plan is the orchestration; the 14 stories in the execution-PRD are the prompts; the team decides tactical implementation (memory `feedback_route_through_po.md`).
- **Scope terminus by logging.** Items that surface mid-wave and are out of sprint scope go to `BACKLOG-47-*.md` via WI-13's dual-write. We log; we do not delete; we do not silently absorb.

---

> *"I do not know what strength is in my backlog, but I swear to you I will not let the sprint fall. The gates are named. The waves are sequenced. The rings are cut. Ride now — ride for ruin and the world's ending. Ride for the retro."*
> — Aragorn

---

**End of sprint-plan.**

```
STATUS: DONE
ARTIFACT: .delivery/artifacts/08-execute/05-plan/sm/sprint-plan.md
SUMMARY: Fourteen rings across four waves, each gate mechanical, each escalation named — hold the line at the wave-gate, and the sprint shall not fall.
```

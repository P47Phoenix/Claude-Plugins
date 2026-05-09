<!-- run: run-2026-05-09-tk4 | stage: 05-plan | depth: light | author: Scrum Master (Samwise Gamgee) | sources: stories.md, prd.md, ADR-tk4-{001,002,003} | wave: 3 — closure -->

# Sprint Plan — Wave 3 Closure (run-2026-05-09-tk4)

> "It's the job that's never started as takes longest to finish. So let's start it, and watch the road, and call out the rocks before we trip on 'em."
> — Sam, plainly

## Sprint Goal

Close out Wave 3 by landing all 7 over-budget delivery-team SKILL.md files at-or-under their tier ceilings (with frontmatter headroom held), shipping the paradigm sub-skill pattern on its three named axes, rolling governance frontmatter across 13 files in the correct order, and discharging six carry-forwards on the same wave that produced them — so `governance/skill-budgets.json known_debt[]` baselines empty for the first time since BACKLOG-100.

## Sprint Capacity (verbatim from stories.md §Capacity Declaration)

- **Velocity baseline (rolling 5-pipeline mean)**: ~7 file-scope-stories-equivalent per FEATURE-execution wave (Waves 1/2/caveman-lite landed 5–8 each; this wave is the upper end as the close-out).
- **80% ceiling**: 7 stories at sizes [M-L, L, M, L, M, M, S-M] sum to ~22 points; 28-point ceiling (5 × 7 minus 20% buffer); commitment **78.6% — under the 80% rule** (Plan memory lesson 1).
- **Story count**: **7** (file-scope consolidation from 18 WIs; ~61% Stage-6 dispatch reduction).
- **Effort calibration**: markdown-only edits estimated one tier below code-equivalent per Plan memory lesson 3 (validated 3×). All 7 stories are markdown + small Python + git plumbing — no compiled code.
- **Capacity assumption**: single-developer Stage 6 dispatch per story (file-scope consolidation pattern, validated 3×).
- **Test-coverage gate**: test cases MUST cover ALL 7 PRD FRs explicitly per Plan memory lesson 2; PO rejects any plan missing an FR.

## Story Sequence

| # | Story | Effort | Sequencing | WIs | Parallel-with |
|---|-------|--------|------------|-----|---------------|
| 1 | architect Tier-B closure | M-L | First (sets ADR-pattern + partial-compliance precedent) | W3-1 | none |
| 2 | presentation + ui + operations trims | L (3 files parallel-safe) | Cluster: dispatch in parallel **after Story 1 lands** | W3-2, W3-3, W3-4 | Story 3 |
| 3 | quality + user-feedback + godot trims (godot to **197**) | M | Cluster: parallel with Story 2 (mechanically independent file scopes) | W3-5, W3-6, W3-7 | Story 2 |
| 4 | paradigm sub-skill pattern (research-agent + user-feedback + presentation conditional) | L | Sequential after Stories 1–3 (paradigm pattern is structural; large; joint-AC with Story 3 W3-6 personas) | W3-8 | none |
| 5 | governance frontmatter rollout (13 files +3 keys; cache-prefix re-freeze) | M | **HARD GATE — BINDING after Stories 1–4 land in working tree** (mandatory-rollout side-effect lesson; **tripwire HALT if <15% prose-token reduction** before this opens its PR) | W3-9 | Story 6 |
| 6 | retro KPI + fitness review + CLAUDE.md ≤150 | M | Parallel with Story 5 (no cache-prefix or SKILL.md frontmatter dependency) | W3-10, W3-11, W3-12 | Story 5 |
| 7 | admin / carry-forward pass (validator template, CI lints, STATUS standard, git hook, Stage-7 stale-sweep, telemetry hardening, skill-budgets.json re-baseline) | S-M | **Last** — sequenced terminal so W3-13 / W3-15 / W3-17 / W3-18 dogfood against the live Wave-3 dispatches that produced them | W3-13..W3-18 | none |

**Rationale, plainly**:

- **Story 1 first** because the architect closure is the highest-risk WI in the wave (Wave 2 already extracted the obvious targets, leaving residual content that's genuinely operational rather than reference-shaped) and sets the per-file extraction precedent + the partial-compliance ADR template the rest of the wave leans on. No upstream dependency; the rest of the wave waits on its ADR-pattern proof.
- **Stories 2 and 3 cluster in parallel after Story 1 lands** — file scopes don't collide, `references/` subtrees are orthogonal, trims are mechanically independent per ADR-tk4-001 extraction-target catalog. Two dev dispatches running in parallel halve wall-clock without doubling collision risk.
- **Story 4 follows sequentially after Stories 1–3** because the paradigm sub-skill pattern is structural (new directory shapes, frontmatter contract, marketplace-discoverability CI lint) and large enough that putting it next to the parallel cluster would tangle the PR review. Joint-AC with Story 3 W3-6 personas means the user-feedback persona-family extraction in Story 3 is the line-count vehicle and the paradigm sub-skill demonstration in one operation — Story 4 verifies the contract that Story 3 instantiates.
- **Story 5 is binding-after-1–4** — that's the rule, not a preference; ADR-tk4-003 §Mandatory-rollout sequencing is binding because adding 3 frontmatter lines to a file already at-budget pushes it over. Skip the gate and the wave re-introduces the very `known_debt` entries it's supposed to clear. The tripwire arms here too: HALT before Story 5 PR opens if `.delivery/telemetry/stop-rule-tk4.txt` shows <15% prose reduction.
- **Story 6 rides alongside Story 5** because nothing in Story 6's surface (retro KPI, fitness-review GitHub Action, CLAUDE.md trim) touches cache-prefix or SKILL.md frontmatter. Concurrent dispatch saves a dev cycle.
- **Story 7 is last on purpose** — its validator template, STATUS-format, Stage-7 entry-step, and telemetry hardening are dogfood-co-landing artifacts; sequencing them terminal lets them feed off live Wave-3 dispatch data instead of synthetic input. DEFECT-006 closes at merge of W3-17 against the live PRD §3 stale-PRD instance found at run-start.

## Daily Cadence

Multi-day execution; ~7 stories means daily check-ins matter. Cadence is:

- **Daily standup (15 min, time-boxed)**: each dev names the Story they're on, the next AC they're closing, and any boundary they're approaching (Story 4-to-5 hand-off, tripwire telemetry status, godot 197 line-count).
- **Story-boundary gates (SM-held)**: SM verifies merge-log + AC-pass status at every Story → next-Story transition. The Story 4-to-5 boundary is the binding one; SM does not let Story 5 PR open until the merge log shows Stories 1–4 in.
- **Tripwire poll (per Story boundary, before Story 5)**: SM checks `.delivery/telemetry/stop-rule-tk4.txt` for measured prose-reduction percentage; calls HALT plainly if <15%.
- **DoD validation (5 validators in parallel per story)**: SM / QA / Dev / Architect / Tech-Writer; adversarial review fires if any validator says NOT_DONE.

## Risks and Mitigations (called plainly)

| # | Risk | Severity | Mitigation |
|---|------|----------|------------|
| R1 | **godot Tier-C tightness — exactly 197+3=200 ceiling, zero headroom.** Any drift on extraction (an extra connective line, a missed guardrail consolidation) lands at 198 and the file is over-budget the moment Story 5 frontmatter rolls. | High | ADR-tk4-001 round-2 math is the binding target — Stage 6 Dev measures `wc -l` AFTER extraction, not BEFORE. The round-1 5-line guardrails fold is held in reserve as a Stage-6 escape hatch only if the actual count lands at 198–199. Story 3 AC-3 makes the 197-not-198 target a runnable check (`wc -l = 197`). Per-story DoD blocks the PR if the count drifts. |
| R2 | **Cache-prefix re-freeze cost — one-time ~650-byte shift across 13 SKILL.md** invalidates the cache-warmup prefix on every one of those files. First Wave-3 dispatch after merge incurs ~26KB cold-cache read. | Medium | One-time, scoped, ADR-justified per ADR-tk4-003. Payback is on dispatch #1 because the cumulative ~13,200-token reduction from Stories 1–3 trims vastly exceeds the 26KB re-warm cost. Stage 6 Dev runs-the-command for hash regeneration (caveman-lite Hot Lesson #1 binding extension); DoD validator cites actual byte counts from the regenerated hash file, not the +650-byte projection. |
| R3 | **Tripwire halt scenario — caveman-lite stop-rule fires before Story 5.** If the first 3 Stage-6 dispatches show <15% prose-token reduction vs pre-caveman-lite baseline, Story 5 (W3-9 frontmatter rollout) HALTS pending root-cause retro. | Medium | Halt path is documented and bounded: Stories 1–4 + Story 7 proceed; only W3-9 + W3-10..12 hold. Citation artifact is `.delivery/telemetry/stop-rule-tk4.txt` (no narrative claims allowed). PO empowered to halt at the Story boundary; the wave does not collapse on a tripwire — it pauses cleanly. SM tracks the telemetry file's existence and its measured percentage at every Story boundary, calls the stop plainly if it fires. |
| R4 | **Mandatory-rollout side-effect — Story 5 ordering is binding, not preference.** If anyone (orchestrator, dev, reviewer) lets Story 5 PR open before Stories 1–4 merge, the frontmatter +3 lines push at-budget files OVER budget and re-introduce the very `known_debt` entries the wave is supposed to clear. | High | Story 5 AC-4 is a runnable sequencing gate: `git log --merges --oneline main..HEAD` must show Stories 1–4 merge commits BEFORE Story 5 commit timestamp. PRD §FR-5 + ADR-tk4-003 §Mandatory-rollout sequencing both cite the binding. SM holds the gate at the Story 4-to-5 boundary; no one moves until the merge log is clean. |
| R5 | **Schema-JSON drift on `governance/skill-budgets.json` re-baseline.** Story 7 housekeeping clears `known_debt[]`; if the JSON enumeration drifts from the Python check script's hard-coded list, the lint silently passes a fictional empty state. | Medium | Story 7 W3-14 ships a JSON↔Python consistency CI lint specifically to catch this; Story 7 AC-2 fault-injects a deliberate drift to verify the lint fails. Also: Story 5 AC-2 separately verifies `check_skill_budgets.py` exits 0 with `known_debt` empty for delivery-team scope at end of Story 5. Two independent checkpoints, two stories apart. |
| R6 | **Reference-file extraction discipline — each Story 1–3 must honor the mid-implementation extraction pattern from tk3 (caveman-lite Hot Lesson).** Stage 6 Dev finds a file landing within 10 lines of ceiling and must extract on the spot, not defer. Discipline slip = round-2 retro. | Medium | Per-story DoD (Stories 1, 2, 3) requires citation of ADR-tk4-001 batching math in PR body and SKILL_LOADED signal for `plugin-dev:skill-development` in the dev transcript. Stage 6 Dev runs the per-file Phase 1 router regression AFTER extraction; the regression set itself (~42 dogfood inputs total across the wave) catches the case where a deferred extraction left dead routing in SKILL.md. |
| R7 | **Architect partial-compliance reserve might activate (Story 1).** If Cross-Role Tasks block (24 lines) is genuinely operational and won't extract cleanly, architect ships at 311 not 288 with `Budget-Exception: ADR-tk4-001`. That re-introduces a `known_debt` entry the wave is supposed to clear. | Low–Medium | Honest partial-compliance is the documented Wave 2 precedent and is preferable to manufacturing fictional compliance by trimming router prose. Story 1 AC-1 explicitly permits the exception path with explicit residual math + `target_wave: 4` logging. SM doesn't escalate this — the team decides at the Story 1 DoD boundary; if the exception fires, the wave still ships and W3-1-residual is the only Wave-4 carry. |

## Sprint Definition of Done (carried from stories.md per-story DoD pattern)

A story is Done when:
- All 5 ACs PASS (or AC-1 via documented Budget-Exception path with explicit residual math, Story 1 only).
- `plugin-dev:skill-development` SKILL_LOADED signal present in the dev transcript for every dispatch (mandatory pre-load — every story touches SKILL.md).
- `plugin-dev:skill-reviewer` run post-completion per file.
- `plugin-dev:plugin-validator` run BEFORE PR for stories touching CI lint chains (Stories 4, 5, 7).
- PR body cites the relevant ADR section + actual measured values (byte counts, line counts, dogfood pass/fail), not narrative claims.
- DoD validator review filed at `.delivery/artifacts/06-development/dod/W3-{N}-{slug}.md` with STATUS literal (DONE / NOT_DONE / CODE_COMPLETE / PASS_WITH_NOTES per W3-15 standardization).
- For Story 5 specifically: Dev runs-the-command for `governance/cache-prefix-hash.txt` regeneration (ADR-tk4-003 binding); DoD cites actual byte counts.
- For Story 7 specifically: DEFECT-006 closes upon merge; `known_debt[]` empty for delivery-team scope.

## Stop-Rule (verbatim from stories.md, sourced from idea-brief §9)

**Initiative-level (BACKLOG-100 carry-forward)**: defects/story rate >0.4 across any 3-PR window pauses subsequent waves. Current rolling 3-PR window: tk2 (0 defects) + tk3 (1 defect, P1 non-blocking) = **0.33 < 0.4 — NOT triggered, Wave 3 may proceed**. Wave 3 must hold the rate; PO empowered to halt at any Story boundary if a third defect lands and pushes the window past threshold.

**Wave-level tripwire (per ADR-tk4-003 + architecture §Stop-Rule Tripwire Mechanics)**: if first 3 Stage-6 dispatches show <15% prose-token reduction vs pre-caveman-lite baseline, HALT before Story 5 (W3-9) PR opens. Stories 1–4 + Story 7 proceed; only W3-9 + W3-10..12 hold pending caveman-lite root-cause retro. Citation artifact: `.delivery/telemetry/stop-rule-tk4.txt`.

— Samwise Gamgee, SM, run-2026-05-09-tk4. The road's plain. The rocks are named. We start with Story 1, watch the boundaries, call the gates, and don't let Story 5 jump the queue. That's the job.

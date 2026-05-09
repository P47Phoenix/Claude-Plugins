<!-- run: run-2026-05-09-tk4 | wave: 3 (closure + governance + paradigm) | predecessor: run-2026-05-05-tk3 (caveman-lite, merged) | initiative: skill token-economy — delivery-team plugin (final wave) -->

# Idea Brief — Wave 3: delivery-team Skill Token-Economy Closure

*Spoken by Aragorn, son of Arathorn.*

> The road is set. Four waves walked, one wave packed at our feet. The Fellowship rides — light packs, plain speech, blades sharp where it counts. Onward.

## 1. Engagement

- **Pipeline**: `run-2026-05-09-tk4`
- **Project type**: FEATURE — execution of pre-planned waves (binding-decisions-in-memory pattern, fifth invocation in this initiative)
- **Wave**: 3 — final delivery-team token-economy wave; closes the initiative
- **Theme**: lotr (continued through end of initiative); PO maps to Aragorn
- **Predecessor**: run-2026-05-05-tk3 (caveman-lite, GO, merged to main); meta-retro at `.delivery/memory/initiative-retros/skill-token-economy-meta-retro-2026-05-09.md` (note: meta-retro labels Wave 3 "DEFERRED" — this run flips it to SHIPPED)
- **Initiative state**: 4 of 5 waves SHIPPED (80%); Wave 3 IS the close-out

## 2. Source

Authoritative source brief: `.delivery/backlog/BACKLOG-104-skill-token-economy-delivery-team-wave-3.md` (18 WIs, 7 file-scope stories per PO recommendation §4; line counts verified by `wc -l` 2026-05-05). This idea brief CONSOLIDATES — it does not re-author. All WI ACs, extraction candidates, and file lists live in BACKLOG-104 verbatim; the team executes against BACKLOG-104, not this brief.

## 3. Goal

Clear ALL 7 remaining over-budget SKILL.md files in delivery-team (`scripts/check_skill_budgets.py` exits 0 with empty `known_debt` array, or only justified non-delivery-team Wave-4 entries), install governance frontmatter (`maintainer:` + `fitness_review_due:` + `context_budget:`) on every delivery-team SKILL.md, complete 6 retro carry-forwards (4 Wave-2 + 2 caveman-lite), ship the paradigm sub-skill pattern (`disable-model-invocation: true`) on ≥3 axes, and refactor `CLAUDE.md` from 168 → ≤150. End-state: empty known_debt, governance live, fitness review process operational, DEFECT-006 closed.

## 4. Binding Constraints (from memory — do NOT re-debate)

From `.delivery/memory/topics/skill-token-economy.md` (5 rulings still binding through 4 shipped waves; no superseding ADR required):

1. **Cache-prefix freeze** — first ~2k tokens of every Tier-A SKILL.md MUST stay byte-stable across runs; volatile content under `## Volatile` near EOF; any prefix change requires an ADR citing cache-cost impact.
2. **`disable-model-invocation` boundary** — paradigm sub-skills only; top-level skills MUST stay marketplace-discoverable.
3. **SKILL.md line budgets** — Tier-A ≤500, Tier-B ≤300, Tier-C ≤200; declared in `tier:` frontmatter; CI gate fails over-budget PRs without `Budget-Exception: <ADR-link>`.
4. **Agent prompts as markdown references** — no Python prompt-builders.
5. **`allowed-tools` whitelist scope** — required on Tier-A orchestrators.

From `.delivery/memory/topics/project-types.md`:
- **FEATURE-execution-of-pre-planned-waves with binding-decisions-in-memory** (validated 4× — Waves 1, 2, caveman, now Wave 3): execute, do not re-debate. If a stage agent re-litigates a ruling, that is a defect.
- **Story consolidation by file scope** (validated 3×): see §6 below.
- **Honest partial-compliance ruling pattern** (validated Wave 2): applies to W3-1 architect Tier-B closure if the 200-line residual cannot land in one wave.

From `CLAUDE.md` Key Conventions:
- **Plugin-dev skill routing for Stage 6** (binding): Wave 3 modifies multiple SKILL.md files → `plugin-dev:skill-development` MUST be acknowledged at the developer dispatch; `plugin-dev:skill-reviewer` post-completion; `plugin-dev:plugin-validator` before PR.

From caveman-lite (run-tk3) retro carry-forwards (binding, NEW since Wave 2):
- **Architect runs-the-command for cache-prefix-impacting ADRs** (Hot Lesson #1 extension) — see §5 cache-prefix invariant.
- **Mid-implementation reference-extraction inside Stage 6** — Tier-A budget compensation pattern; applies to all 7 over-budget files.
- **Producer-validator separation extends to validator-style artifacts** — fresh DoD validator catches what producer self-review misses.

From Wave 2 retro carry-forwards (still open at run-tk3 end; W3-13..16 in this BACKLOG): standardized validator-prompt template, JSON↔Python KNOWN_DEBT consistency lint, DoD STATUS-format standardization, pre-merge git hook for skill-budget local check.

## 5. Cache-Prefix Invariant (Ruling 1) — explicit call-out

If ANY Wave 3 work touches Phase 0 of any SKILL.md (the byte-stable cache-prefix region), **ADR-tk4-001 (architect) MUST own the re-freeze**: enumerate moved bytes, justify, update `governance/cache-prefix-hash.txt`, pass CI hash-check. Otherwise, NO impact and no ADR needed. Architect Stage 4 produces a **single Wave-3-summary cache-prefix ADR** documenting cumulative impact across W3-1..W3-7 + W3-9 frontmatter rollout — one-time re-warm cost, hash file updated once at end of Story 5 (NOT per-story). Dev runs-the-command discipline at Architect DoD is binding (caveman-lite Hot Lesson #1 extension — caught a byte-offset INVERSION in tk3; without it, an inverted ADR would have shipped).

## 6. Routing (per BACKLOG-104 §Pipeline-run preferences)

| Stage | Depth | Notes |
|---|---|---|
| 1 Idea | light | This brief |
| 2 Refine | light | ACs already in BACKLOG-104; refine = sharpen exit gates + confirm story sequencing |
| 3 Design | **SKIP** | DX-only — no UI surface. Per `topics/project-types.md`: record skip at state-entry as "DX-only routing deviation"; do NOT conflate with silent stage fusion |
| 4 Architect | light w/ **3 ADRs** | ADR-tk4-001 cumulative cache-prefix re-freeze (mandatory if any Phase 0 touched); ADR-tk4-002 W3-1 architect partial-compliance ruling (if 200-line residual infeasible); ADR-tk4-003 W3-8 paradigm sub-skill dispatch shape (highest novelty in initiative) |
| 5 Plan | light | 7 file-scope stories (per §6 below); upstream constraint injection — PO carries capacity declaration verbatim |
| 6 Development | full | `plugin-dev:skill-development` acknowledged; mid-implementation reference-extraction permitted as Tier-A budget compensation; cache-prefix-impacting ADRs trigger Dev runs-the-command at DoD (Ruling 1) |
| 7 UAT | full | Stage 7 entry-step sweeps for stale Wave-N-1 carry-overs (DEFECT-006 systemic fix is W3-17 — dogfood it on this very run); empirical AC-13 telemetry close-out for caveman-lite measured here |

## 7. Story Consolidation Decision (binding)

Per BACKLOG-104 §4 PO recommendation: **18 WIs → 7 file-scope stories** (~61% Stage 6 dispatch reduction vs per-WI). Story consolidation by file scope is validated 3× (Wave 1, Wave 2, caveman-lite); this is the canonical fourth application.

| Story | WIs | Scope | Sequencing |
|---|---|---|---|
| 1 | W3-1 | architect SKILL.md Tier-B closure (500→≤300) | First; sets pattern; partial-compliance candidate |
| 2 | W3-2..4 | presentation + ui + operations Tier-B trims | Parallel-safe |
| 3 | W3-5..7 | quality + user-feedback + godot trims | Parallel-safe; W3-6 coordinates with W3-8 |
| 4 | W3-8 | paradigm sub-skill pattern (research-agent + presentation + user-feedback) | After Story 1 ships ADR-pattern |
| 5 | W3-9 | Governance frontmatter rollout — ALL delivery-team SKILL.md | **AFTER Stories 1–4 content trims** (mandatory-rollout-side-effect lesson — frontmatter adds ~3 lines/file; running before trims means targeting fictional ≤297/≤197 instead of canonical ≤300/≤200) |
| 6 | W3-10..12 | Retro KPI + fitness review process + CLAUDE.md refactor (168→≤150) | Parallel with Story 5 |
| 7 admin | W3-13..18 | 4 Wave-2 + 2 caveman-lite carry-forwards + skill-budgets re-baseline | Parallel with anything |

Stage 5 owns final sequencing and may collapse Stories 6+7 or split Story 5 further.

## 8. Acceptance Gates (verbatim from BACKLOG-104 §Acceptance Criteria)

1. All 7 over-budget files CLEARED (`scripts/check_skill_budgets.py` exits 0 with empty `known_debt`, or only justified non-delivery-team Wave-4 entries).
2. CLAUDE.md ≤150 lines.
3. Governance frontmatter (`maintainer:` + `fitness_review_due:` + `context_budget:`) present on all delivery-team SKILL.md files.
4. The 4 Wave-2 retro carry-forwards (W3-13..16) DISCHARGED.
5. The 2 caveman-lite retro carry-forwards (W3-17 Stage 7 entry sweep, W3-18 telemetry hardening) DISCHARGED. **DEFECT-006 closes**.
6. Paradigm sub-skill pattern shipped on ≥3 axes (research-agent + user-feedback minimum; presentation if architecturally favored at Stage 4).
7. Telemetry-measured cumulative token reduction ≥50% on delivery-flow vs pre-Wave-0 baseline (compounding Waves 0+1+2+caveman-lite+3).

**AC-13 close-out (caveman-lite carry-over)**: Wave 3's first dispatches ARE the empirical AC-13 telemetry measurement window. Caveman-lite deferred AC-13 by design; this run measures it.

**Stop-rule tripwire (BACKLOG-102 carry-forward)**: if first dispatches show <15% prose-token reduction vs pre-caveman-lite baseline, BACKLOG-102 stop-rule triggers a root-cause retro on caveman-lite **BEFORE Story 5 (W3-9 governance) proceeds**. Stories 1–4 content trims may continue (orthogonal to prose discipline); only W3-9 mandatory rollout holds.

## 9. Stop-rule

**Initiative-level (BACKLOG-100 carry-forward)**: defects/story rate >0.4 across any 3-PR window pauses subsequent waves. Current rolling 3-PR window: tk2 (0 defects) + tk3 (1 defect, P1 non-blocking) = **0.33 < 0.4 — NOT triggered, Wave 3 may proceed**. Wave 3 must hold the rate; PO empowered to halt at any Story boundary if a third defect lands and pushes the window past threshold.

## 10. Open Questions

None at brief stage. BACKLOG-104 + the binding-decisions topic file resolve all ambiguities. Architect at Stage 4 will rule on three open architectural choices (W3-1 partial-compliance threshold, W3-8 paradigm dispatch shape per axis, W3-15 STATUS-format standardize-vs-helper) — those are EXPECTED Stage 4 decisions, not Stage 1 ambiguities.

## 11. References

- Source brief: `.delivery/backlog/BACKLOG-104-skill-token-economy-delivery-team-wave-3.md`
- Binding decisions: `.delivery/memory/topics/skill-token-economy.md`
- Project-type patterns: `.delivery/memory/topics/project-types.md`
- Predecessor retro: `.delivery/memory/archive/run-2026-05-05-tk3.md` (caveman-lite — 6 carry-forwards)
- Initiative meta-retro: `.delivery/memory/initiative-retros/skill-token-economy-meta-retro-2026-05-09.md`
- Cache-prefix hash: `governance/cache-prefix-hash.txt`
- Known-debt registry: `governance/skill-budgets.json` (7 entries all targeted to Wave 3)
- Telemetry: `.delivery/telemetry/skill-loads.jsonl`

— Aragorn, PO, run-2026-05-09-tk4. The road is long but the way is plain. Onward.

<!-- run: run-2026-05-09-tk4 | stage: 4 (Architect, light) | wave: 3 — closure | author: Saruman of Many Colours, Solution Architect -->

# ADR-tk4-001 — Tier-B/C Closure Approach for Wave 3

**Status**: Accepted
**Date**: 2026-05-09
**Pipeline**: `run-2026-05-09-tk4`
**Owner**: Solution Architect (Saruman)
**Supersedes**: none
**Superseded by**: none

---

## Context

The texts are read; the tally is taken. Seven `SKILL.md` files in `delivery-team/` exceed their declared tier ceilings. The verified `wc -l` line counts (PRD §3, repo root, 2026-05-09) and tier targets are these:

| File | Tier | Verified | Target | Δ to close |
|---|:-:|---:|---:|---:|
| `delivery-team/skills/architect/SKILL.md` | B | 500 | ≤300 | -200 |
| `delivery-team/skills/presentation/SKILL.md` | B | 545 | ≤300 | -245 |
| `delivery-team/skills/ui/SKILL.md` | B | 496 | ≤300 | -196 |
| `delivery-team/skills/operations/SKILL.md` | B | 420 | ≤300 | -120 |
| `delivery-team/skills/quality/SKILL.md` | B | 418 | ≤300 | -118 |
| `delivery-team/skills/user-feedback/SKILL.md` | B | 399 | ≤300 | -99 |
| `delivery-team/skills/godot/SKILL.md` | C | 236 | ≤200 | -36 |

The Wave 2 doctrine-extraction precedent (delivery-flow → `references/orchestrator-doctrine.md`; product-delivery → `references/patterns/`; architect → `references/output-contracts/`) is the canonical mechanism. The caveman-lite Hot Lesson (mid-implementation reference-extraction inside Stage 6) is the canonical compensation when Stage 4 batching math comes within 10 lines of a tier ceiling.

The architect closure is the highest-risk WI in the wave because Wave 2 already extracted the obvious targets (output-contracts split, transformation-phase detail), leaving residual content that is genuinely operational rather than reference-shaped. Honest partial-compliance (Wave 2 lesson) is on the table.

---

## Decision

**Per-file extraction strategy with explicit batching math.** The form is `before → extracted-Δ + router-overhead-Δ = after`. Router overhead is the per-file cost of replacing a removed block with a one-line `See references/<path>` pointer (estimated +1 line per extraction target on average; consolidated into the math below).

### W3-1 — `delivery-team/skills/architect/SKILL.md` (500 → target ≤300)

**Extractions** (Stage 6 Dev confirms which already exist; many `references/*.md` files are present per `ls` survey):

- `## Architecture Style and Decomposition from Config` (lines 133–212, ~80 lines) → consolidate into existing `references/decomposition/<strategy>.md` set (4 strategies); replace block with 4-line pointer table. **Net: -80 +4 = -76**
- `## Software Architecture Roles` (lines 231–294, ~64 lines) → extract per-role manifests to `references/roles/<role>.md` (7 software roles); replace with 7-row routing table. **Net: -64 +8 = -56**
- `## Game Architecture Roles` (lines 295–329, ~35 lines) → extract per-role manifests to `references/roles/<game-role>.md` (4 game roles); replace with 4-row routing table. **Net: -35 +5 = -30**
- `## Cross-Role Tasks` (lines 330–353, ~24 lines) → extract task-type contracts to `references/contracts/cross-role-tasks.md`; replace with one-line pointer. **Net: -24 +1 = -23**
- `## Architecture Guardrails` (lines 370–397, ~28 lines) → extract to `references/guardrails.md`; one-line pointer. **Net: -28 +1 = -27**

**Math**: `500 → -76 -56 -30 -23 -27 = 500 - 212 = 288`. **after = 288 ≤ 300. COMPLIANT.**

**Partial-compliance reserve**: if Stage 6 finds Cross-Role Tasks (24 lines) is genuinely operational and cannot extract cleanly, the worst-case math is `500 - 76 - 56 - 30 - 27 = 311`, which is +11 over Tier-B. In that case, the **honest partial-compliance ruling** (Wave 2 precedent) applies: ship architect at ≤311 with `Budget-Exception: ADR-tk4-001` in the PR body, log W3-1-residual to `governance/skill-budgets.json` with `target_wave: 4`, and document the explicit residual math in the Stage 6 DoD review. Do not pad-trim Phase 1 router prose to manufacture compliance.

### W3-2 — `delivery-team/skills/presentation/SKILL.md` (545 → target ≤300)

- `## Presentation Type Detection` (24–127, ~104 lines, includes per-type detection blocks) → extract 9 type specs to `references/types/<type>.md`; keep top-level keyword routing table only. **Net: -104 +12 = -92** (12 = type-routing table rows)
- `## 6-Step Collaboration Flow` (128–414, ~287 lines) → extract per-step detail to `references/flow/<step>.md` (6 step files); keep 6-row summary table + light orchestration text. **Net: -287 +20 = -267** (20 = 6 step-rows + summary header)
- `## Output Format Specifications` + `## Slide N: [Title]` (415–467, ~53 lines) → extract 4 format detail blocks to `references/formats/<format>.md`; replace with 4-row pointer table. **Net: -53 +6 = -47**

**Math**: `545 → -92 -267 -47 = 545 - 406 = 139`. With +20 line buffer for keyword-table tightening and any necessary connective prose, realistic landing **after ≈ 160. COMPLIANT (≤300 with broad margin).**

This file is the largest by absolute count but also has the largest single block (the 287-line 6-Step flow) which is structurally extraction-shaped. Highest-confidence trim in the wave.

### W3-3 — `delivery-team/skills/ui/SKILL.md` (496 → target ≤300)

- `## UX Designer` / `## UI Designer` / `## Game UI Designer` (111–204, ~94 lines) → extract per-role manifests to `references/roles/<role>.md` (3 files); replace with 3-row routing table referencing existing keyword block. **Net: -94 +5 = -89**
- `## Cross-Role Tasks` (205–227, ~23 lines) → extract to `references/contracts/cross-role-tasks.md`; one-line pointer. **Net: -23 +1 = -22**
- `## Output Contracts` (228–345, ~118 lines, includes 4 named contract templates) → extract 4 contract templates to `references/contracts/<name>.md`; keep one-line table. **Net: -118 +6 = -112**

**Math**: `496 → -89 -22 -112 = 496 - 223 = 273`. **after = 273 ≤ 300. COMPLIANT.**

### W3-4 — `delivery-team/skills/operations/SKILL.md` (420 → target ≤300)

- `## Role --> Reference Mapping` + `## Task Type Routing Table` + `## Task Type Instructions` (97–160, ~64 lines) → extract role-to-reference and task-type instruction detail to `references/roles/<role>.md` (3 files) + `references/contracts/task-instructions.md`; keep slim routing table. **Net: -64 +6 = -58**
- `## Output Contracts` block (161–272, ~112 lines, 3 named contracts) → extract 3 contract templates to `references/contracts/<role>-output.md`; keep 3-row pointer table. **Net: -112 +5 = -107**

**Math**: `420 → -58 -107 = 420 - 165 = 255`. **after = 255 ≤ 300. COMPLIANT.**

### W3-5 — `delivery-team/skills/quality/SKILL.md` (418 → target ≤300)

- `## Output Contracts` cluster (109–258, ~150 lines, 6 contract templates: Test Strategy, Test Cases, Test Plan, Test Data, Quality Metrics, Automation Strategy) → extract 6 contract templates to `references/contracts/<contract>.md`; keep 6-row pointer table. **Net: -150 +8 = -142**

**Math**: `418 → -142 = 276`. **after = 276 ≤ 300. COMPLIANT.**

### W3-6 — `delivery-team/skills/user-feedback/SKILL.md` (399 → target ≤300)

- `## Phase 3: Persona Agent Invocation` (91–157, ~67 lines, contains persona-family dispatch detail) → **paradigm sub-skill extraction** per ADR-tk4-002: 4 persona families move to `delivery-team/skills/user-feedback/skills/personas/<family>/SKILL.md`; replace with 4-row router table. **Net: -67 +6 = -61**
- `## Sub-Agent Interface (Agentic Flow Integration)` (277–365, ~89 lines) → extract integration detail to `references/sub-agent-interface.md`; one-line pointer. **Net: -89 +1 = -88**

**Math**: `399 → -61 -88 = 399 - 149 = 250`. **after = 250 ≤ 300. COMPLIANT.** (Joint-AC with W3-8; persona-family extraction is the line-count vehicle and the paradigm sub-skill demonstration.)

### W3-7 — `delivery-team/skills/godot/SKILL.md` (236 → target ≤197, Tier-C with frontmatter headroom)

**Round-2 revision**: extraction strengthened to land at ≤197 so post-Story-5 frontmatter (+3 lines from ADR-tk4-003) lands at ≤200 exactly, with NO escape hatch needed at PR time. Wave-0 mandatory-rollout-side-effect lesson is binding: every file's `after` MUST satisfy `after + 3 ≤ tier_ceiling` so Story 5 cannot push any file over budget. Six files already have ≥9-line headroom; godot is the only one needing a deeper trim than round-1 math.

- `## Common Task Patterns` (151–189, ~39 lines) → extract to `references/task-patterns.md`; one-line pointer. **Net: -39 +1 = -38**
- `## Architecture Guardrails` — fold one additional 1-line trim (consolidate the two "performance budgets / frame time awareness" bullets into one composite line; semantic loss = nil per Stage 6 Dev confirmation). **Net: -1**

**Math**: `236 → -38 -1 = 197`. **after = 197 ≤ 197. COMPLIANT with frontmatter headroom held EXACTLY at 197 + 3 = 200 ceiling.** (No escape hatch invoked at PR time; the round-1 conditional 5-line guardrails fold is RETAINED as a Stage-6 reserve only if the actual `wc -l` after extraction is one or two lines higher than the math projects — still safe within `200 - 3 = 197` boundary.)

**Cross-file headroom check** (all 6 non-godot files have ≥9-line headroom; no additional trims required):

| File | round-1 after | + frontmatter (+3) | Tier ceiling | Headroom |
|---|---:|---:|---:|---:|
| architect | 288 | 291 | 300 | 9 |
| presentation | ~160 | ~163 | 300 | ~137 |
| ui | 273 | 276 | 300 | 24 |
| operations | 255 | 258 | 300 | 42 |
| quality | 276 | 279 | 300 | 21 |
| user-feedback | 250 | 253 | 300 | 47 |
| **godot (revised)** | **197** | **200** | **200** | **0 (held exactly)** |

**Re-baseline expectation for `governance/skill-budgets.json`** (post-Wave-3 known_debt should be EMPTY): all 7 files at-or-below their tier ceiling INCLUDING the +3-line frontmatter add. No `Budget-Exception` lines in PR body for godot. (architect partial-compliance reserve below remains the sole conditional exception, applicable only if Cross-Role Tasks cannot extract cleanly.)

### Cumulative cache-prefix impact assessment

All 7 extractions land **below frontmatter and below the Phase 1 router** (PRD §3 confirms no `## Phase 0` headers exist; the byte-stable cache-prefix region today is the frontmatter block at lines 1–11). All extracted blocks are at line ranges ≥111 in every file. Extractions therefore do **NOT** touch the cache-prefix region. **No re-freeze required from W3-1..W3-7.** (W3-9 frontmatter rollout is the sole cache-prefix-impacting WI in this wave; it is owned by ADR-tk4-003.)

### Extraction-target catalog (per file)

The Stage 6 Dev confirms extraction destinations against the existing `references/` directories. Per `ls` survey, several target directories already exist with partial content from Wave 2; new extractions extend rather than create:

| File | New `references/` paths | Existing `references/` extended |
|---|---|---|
| architect | `roles/<role>.md` (×11), `contracts/cross-role-tasks.md`, `guardrails.md` | `decomposition/<strategy>.md` (×4 — pre-existing), `output-contracts/` (Wave 2) |
| presentation | `types/<type>.md` (×9), `flow/<step>.md` (×6), `formats/<format>.md` (×4) | none (existing references are `narrative-patterns.md`, `slide-structure.md`, etc. — orthogonal) |
| ui | `roles/<role>.md` (×3), `contracts/<contract>.md` (×4), `contracts/cross-role-tasks.md` | none (existing references are domain-specific: `wireframing.md`, `accessibility.md`, etc.) |
| operations | `roles/<role>.md` (×3), `contracts/<role>-output.md` (×3), `contracts/task-instructions.md` | none |
| quality | `contracts/<contract>.md` (×6) | existing `test-strategy.md`, `quality-metrics.md`, `test-automation.md` may absorb 3 of 6 |
| user-feedback | `skills/personas/<family>/SKILL.md` (×4 — paradigm sub-skill per ADR-tk4-002), `references/sub-agent-interface.md` | existing `persona-library.md` retired in favor of per-family sub-skills |
| godot | `references/task-patterns.md` | existing `gdscript.md`, `csharp-godot.md`, `scenes-nodes.md`, `signals-architecture.md` (Wave 2) untouched |

Stage 6 Dev MUST verify each target path before writing; collisions with existing reference files require the developer to consolidate, not duplicate.

### Sequencing with ADR-tk4-003

This ADR (W3-1..W3-7 content trims) MUST land in the working tree **before** ADR-tk4-003 (W3-9 frontmatter rollout) executes. Stage 5 stories.md sequences Stories 1–4 ahead of Story 5 as a hard gate. Rationale: frontmatter rollout adds ~3 lines per file. If W3-9 ran first, files already AT-budget after this ADR's trims would land 3 lines OVER budget, manufacturing fictional ≤297/≤197 ceilings instead of canonical ≤300/≤200. The Wave 0 mandatory-rollout-side-effect lesson is binding here.

### Stage 6 dogfood checklist (per-file Phase 1 router regression)

After each file's extractions ship, Stage 6 Dev runs the existing Phase 1 router against a regression input set sized to the file's variant count:

- architect: 11 dogfood inputs (one per role) → router picks correct role 11/11
- presentation: 9 type inputs + 4 format inputs → 9/9 + 4/4
- ui: 3 designer inputs → 3/3
- operations: 3 ops-role inputs → 3/3
- quality: 7 task-type inputs → 7/7
- user-feedback: 4 persona-family inputs → 4/4 (joint-AC with W3-8 per ADR-tk4-002)
- godot: 4 task-type inputs (GDScript / C# / scene / signal) → 4/4

Total: ~42 dogfood router invocations. Sub-agent loads ONLY the matched reference file(s) — verified by spot-check on one dispatch per file (7 spot-checks).

---

## Consequences

**Positive**:
- All 7 files reach tier compliance with explicit batching math; no fictional ceilings.
- Cumulative ~1,100 lines moved out of frequently-loaded SKILL.md files into on-demand `references/`. At ~12 tokens/line average, that is a one-time ~13k-token reduction in the cache-warmup prefix surface.
- Cache-prefix invariant (Ruling 1) preserved across W3-1..W3-7; ADR-tk4-003 handles the W3-9 re-freeze separately.
- Reference files are reusable across roles (e.g., `references/contracts/cross-role-tasks.md` shared by architect + ui).
- Wave 2 doctrine-extraction precedent extended cleanly to per-role and per-contract extractions.

**Negative**:
- Validation effort: 7 files × Phase 1 router regression sets = ~30 dogfood inputs to verify routers still pick correctly.
- Reference fragmentation: `references/roles/<role>.md` and `references/contracts/<contract>.md` are new directory conventions that need a one-paragraph entry in each plugin's `ARCHITECTURE.md` (catch in Stage 6 DoD).
- Reversibility: each extraction can be inlined back via `cat references/<file>.md >> SKILL.md`, but the cache-warmup prefix would re-grow. Reversibility is mechanical, not free.

**Partial-compliance fallback (W3-1 only)**:
- If architect closure lands at 311 instead of 288, ADR-tk4-001 itself records the residual; Wave 2 honest-partial pattern applies; W3-1-residual logged to `governance/skill-budgets.json` with `target_wave: 4`. Stage 6 DoD validator MUST cite explicit math in the review, not a narrative claim of "close enough".

---

## Alternatives considered

1. **In-body trim (no extraction)** — Reject. The over-budget content is operational (role definitions, output contracts, task-type instructions). Trimming in place either deletes operational content or compresses prose past readability. Caveman-lite already established the prose-discipline floor; further in-body compression is below the floor.

2. **Different extraction targets** — Considered extracting Phase 1 / Phase 2 router boilerplate to a shared `delivery-team/references/shared/router-doctrine.md` (Wave 2 doctrine-extraction precedent). Rejected: router prose is 15–25 lines per file, splits into 6 files, and the doctrine-shared form is awkward when each file has slightly different routing tables. Per-role and per-contract extractions are higher-yield.

3. **Defer godot to Wave 4** — Considered, because godot's 36-line trim is the smallest absolute. Rejected: Tier-C compliance is mechanically simple (one extraction), Wave 3 is the close-out wave by design (idea brief §1 "the road is set"), and deferring would leave `known_debt` non-empty and miss AC-1.

4. **Bulk paradigm sub-skill extraction across all roles** — Considered applying the paradigm sub-skill pattern to architect's 11 roles, ui's 3 designer roles, operations' 3 ops roles. Rejected for this wave: ADR-tk4-002 (W3-8) ships the pattern on 3 axes (research-agent + presentation + user-feedback); rolling it across 6 more axes in the same wave is out-of-scope per BACKLOG-104 §Out of scope ("delivery-team paradigm sub-skill pattern beyond the 3 cited deferred to BACKLOG-106+").

---

## Risk register (this ADR)

| Risk | Severity | Mitigation |
|---|---|---|
| Architect Cross-Role Tasks block (24 lines) cannot extract cleanly because content is genuinely cross-cutting | Med | Honest partial-compliance ruling activates; ship at 311 with `Budget-Exception: ADR-tk4-001`; log W3-1-residual to `governance/skill-budgets.json` `target_wave: 4`; Stage 6 DoD cites explicit math |
| Quality `references/contracts/` collides with existing `test-strategy.md` / `quality-metrics.md` | Low | Stage 6 Dev consolidates before duplicating; extraction-target catalog above flags 3-of-6 overlap candidates explicitly |
| Phase 1 router regression on a high-variant file (architect 11 roles, presentation 9 types) misses an extracted role/type | Med | 42-input dogfood checklist above is the regression set; Stage 6 DoD validator runs the router and reports per-input pass/fail |
| Reference fragmentation across `references/roles/`, `references/contracts/`, `references/types/` not documented in plugin `ARCHITECTURE.md` | Low | Stage 6 DoD adds one-paragraph entry to `delivery-team/ARCHITECTURE.md` for each new convention |

## References

- Wave 2 doctrine-extraction precedent: `.delivery/artifacts/04-architect/adrs/` ADRs from `run-2026-05-05-tk2`
- Caveman-lite reference-extraction Hot Lesson: `.delivery/memory/archive/run-2026-05-05-tk3.md`
- Honest partial-compliance pattern: `.delivery/memory/topics/project-types.md`
- Cache-prefix freeze (Ruling 1): `.delivery/memory/topics/skill-token-economy.md`
- Verified line counts: PRD §3 (`run-2026-05-09-tk4`)
- Architect batching math gate (DoD): `.delivery/memory/stages/architect.md` lesson #5

— Saruman of Many Colours, Architect, run-2026-05-09-tk4. *"He that breaks a thing to find out what it is has left the path of wisdom; therefore the texts are extracted, not shattered."*

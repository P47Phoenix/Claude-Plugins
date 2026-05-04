# BACKLOG-102: Caveman-style prose discipline for agent output

**Status**: Open
**Priority**: P2 (compounds with Wave 1 quick-wins; not blocking BACKLOG-101)
**Size**: S (prompt-template updates + measurement; ~half day)
**Created**: 2026-05-04
**Owner**: PO → delivery-flow pipeline
**Predecessor**: BACKLOG-100 (telemetry W0-1 ships the measurement substrate)

## Source

- **External**: [juliusbrussee/caveman](https://github.com/juliusbrussee/caveman) — Claude Code skill that cuts ~65-75% output tokens via "caveman speak" with explicit auto-clarity boundaries
- **User direction (2026-05-04)**: "We should also implement parts of caveman… in particular the outputs we create. Either in artifacts or agent output to reduce context usage."
- **Telemetry substrate**: BACKLOG-100 W0-1 hook (`.delivery/telemetry/skill-loads.jsonl`) is now in place to measure before/after deltas empirically

## Goal

Apply caveman-lite discipline selectively to **agent narrative prose** and **ephemeral artifacts** to reduce both flowing-through-orchestrator context and on-disk DoD review surface — WITHOUT compromising durable-artifact readability or technical accuracy.

## Tiered scope

### Tier 1 — Apply caveman-lite (low risk, ship in this BACKLOG)

| Surface | Why safe | Estimated savings |
|---------|----------|---------|
| Agent **narrative-framing prose** (between signal block and end) | Already in-character flourish; substance is in artifact body | 30-40% per response |
| Agent **signal block SUMMARY field** (200-char cap) | Already terse; lite tightens further | 10-15% per signal |
| **DoD review file summaries** (`STATUS:` line + verdict prose) | Validators verify gate results, not prose; lite keeps technical substance | 25-35% per DoD review |
| **stage-summary.md** orchestrator metadata files | Machine-targeted routing metadata | 20-30% per file |
| **Implementation report bodies** (`w0-1-implementation.md` etc.) | Status + file list + dogfood summary; not API documentation | 25-35% per report |

### Tier 2 — A/B test before adopting (defer to BACKLOG-103 or later)

| Surface | Risk | Test plan |
|---------|------|-----------|
| **Retrospective body prose** | Read by humans for lessons; over-compression hurts pattern recognition | Run 1 retro in caveman-lite, 1 in current style; compare lessons-extracted-per-1000-tokens |
| **Sprint plan body prose** | Read by SM/team for execution; clarity > brevity in some sections | Same A/B approach |

### Tier 3 — DO NOT apply (formal artifacts; standard prose required)

- **PRD body** (FR/NFR/AC tables — formal contract for downstream stages)
- **ADR body** (Status/Context/Decision/Consequences — long-lived rationale; future readers depend on full prose)
- **Release notes / user-guide** (user-facing — full prose required per memory `topics/human-preferences.md` documentation rule)
- **CLAUDE.md** (project-level, every-session-loaded — separate concern handled by Wave 3 refactor)
- **Memory topic chunks** (durable cross-run guidance — must remain readable to future agents reading them)
- **Run archive files** (`memory/archive/run-*.md`) — historical record
- **Code + commit messages + PR bodies** (already excluded by caveman's own boundary rule)

## Caveman auto-clarity boundaries (binding — apply repo-wide)

Per caveman's own SKILL.md auto-clarity rules, drop caveman discipline for:
- Security warnings
- Irreversible action confirmations (e.g., `git revert`, `rm -rf` in dogfood)
- Multi-step sequences where fragment order or omitted conjunctions risks misread
- User asks to clarify or repeats question

These exemptions MUST be honored in any prompt-template that activates caveman.

## Work items (3)

### W2-1. Update delivery-flow agent dispatch templates with caveman-lite directive

- **MUST**: Add a `PROSE STYLE` block to the standard agent invocation template in `delivery-team/skills/delivery-flow/SKILL.md` Step 4 (and `references/pipeline-stages.md` if templates live there). Block content:
  ```
  PROSE STYLE: caveman-lite for narrative-framing prose ONLY (the prose between signal block and response end, plus signal block SUMMARY field). Drop articles/filler/pleasantries/hedging; fragments OK; short synonyms; preserve technical terms exact and code/error-string verbatim. Artifact body uses standard prose. Auto-clarity exemptions apply: standard prose for security warnings, irreversible-op confirmations, multi-step sequences, user clarifications.
  ```
- **Files**: `delivery-team/skills/delivery-flow/SKILL.md`, possibly `references/pipeline-stages.md`
- **AC**:
  - [ ] Directive text added to standard dispatch template
  - [ ] Telemetry shows ≥20% reduction in mean response prose tokens (excluding artifact writes) over 5 dispatches post-change vs 5 pre-change baseline (run-2026-05-03-tk0e provides baseline; W1 first run provides post-change measurement)
  - [ ] Auto-clarity exemptions verified by spot-check: any agent dispatch involving destructive op (e.g., file deletion, git revert) must NOT use caveman in confirmation prose

### W2-2. Apply caveman-lite to DoD validator templates

- **MUST**: DoD validator prompt templates SHALL produce review files with caveman-lite verdict prose. Gate-result tables and findings-list bullets stay in current format (tabular structure is already terse).
- **Files**: validator dispatch sections in `delivery-team/skills/delivery-flow/SKILL.md` Step 7 + `references/quality-gates.md` if applicable
- **AC**:
  - [ ] DoD review files post-change average ≥25% smaller than pre-change baseline (Stage 6/7 DoD reviews from run-2026-05-03-tk0e provide baseline)
  - [ ] STATUS field semantics unchanged (DONE/NOT_DONE/CODE_COMPLETE preserved verbatim)
  - [ ] Findings still actionable (each finding names file/line/criterion just like today)

### W2-3. Add `prose_style:` config key to `.delivery/config.yml`

- **MUST**: New top-level config key `prose_style: caveman-lite | standard` (default `caveman-lite` post-merge; `standard` for opt-out). Pipeline orchestrator reads this at Phase 0 and conditionally injects the PROSE STYLE block from W2-1 into agent dispatches.
- **Files**: `delivery-team/skills/delivery-flow/SKILL.md` (Phase 0 config reading), `delivery-team/skills/delivery-flow/references/config-schema.md` (add v2.8 with new key + migration note for v2.7→v2.8)
- **AC**:
  - [ ] Config schema bumped to v2.8 (or follow-on point version)
  - [ ] Existing v2.7 configs auto-migrate (default `caveman-lite` if key missing — surface warning)
  - [ ] Setting `prose_style: standard` reverts behavior to current (verified by 3-dispatch dogfood)

## Out of scope (this BACKLOG)

- Installing caveman as a marketplace plugin (separate decision; this BACKLOG implements caveman-lite *patterns* directly in delivery-team prompts rather than adding an external dependency)
- caveman `full` or `ultra` modes (too aggressive for delivery-team artifact bodies; revisit if Tier 1 + Tier 2 measure clean)
- Wenyan modes (no business case; English speakers across team)
- Compression of code/commits/PRs (already excluded by caveman's own boundary rule + binding repo conventions)
- Tier 2 retrospective/sprint-plan A/B (BACKLOG-103 sequel after W2-1..3 ship)

## Sequencing relative to BACKLOG-101

**Recommendation**: ship BACKLOG-102 in **parallel** with BACKLOG-101 Wave 1, OR as the **first sub-wave after Wave 1** — team's call.

Arguments for parallel:
- Mechanically independent (prose-template change vs structural extractions)
- Compounds with W1-3 (Haiku for routing) — both reduce per-dispatch cost
- W0-1 telemetry already in place; deltas measurable from Wave 1 run

Arguments for sequential (after Wave 1):
- Cleaner A/B baseline: Wave 1 establishes new structural baseline; BACKLOG-102 measures the prose-discipline delta on top
- Avoids confounding "what saved tokens" between structural extractions and prose discipline

**Default recommendation**: sequential — BACKLOG-101 ships first (cleaner mechanical changes), then BACKLOG-102 ships with telemetry-validated measurement against the post-W1 baseline.

## Acceptance Criteria (initiative-level)

1. Agent narrative-framing prose MEASURABLY shorter (≥20% reduction in response-prose tokens, telemetry-verified)
2. DoD review files MEASURABLY smaller (≥25% reduction)
3. NO regression in DoD pass rate (currently 4/7 first-try per memory/index.md)
4. NO regression in artifact quality (PRDs/ADRs/release-notes still pass downstream agents' reads — verified by next pipeline run)
5. Auto-clarity boundaries respected (security/destructive/multi-step prose remains standard)
6. Opt-out via `prose_style: standard` works (one-line config change reverts behavior)

## Pipeline-run preferences

- **Project type**: FEATURE (small surface; prompt-template updates + config schema bump)
- **Routing**: 1 light · 2 light · 3 SKIP (DX-only) · 4 light (config schema bump = small ADR) · 5 light · 6 full · 7 full
- **Theme**: lotr (continued)
- **Models**: same as Wave 0/1
- **Lessons to inject** (memory):
  - `topics/skill-token-economy.md` — already binding
  - `stages/uat.md` cross-doc consistency check (NEW)
  - `topics/gate-patterns.md` mandatory-rollout side-effect simulation (NEW — applies if config schema migration touches existing files)

## Stop-rule

If Tier 1 measurement shows <15% prose-token reduction (low ROI) OR if any DoD validator misses a finding due to over-compression (quality regression), pause Tier 2 A/B and run a root-cause retro before proceeding.

## Why caveman-lite specifically (not full or ultra)

Per caveman SKILL.md, intensity levels:
- **lite**: "No filler/hedging. Keep articles + full sentences. Professional but tight"
- **full**: "Drop articles, fragments OK, short synonyms. Classic caveman"
- **ultra**: "Abbreviate prose words (DB/auth/config/req/res/fn/impl)... one word when one word enough"

For delivery-team agent dispatch prose:
- **lite** preserves enough fluency that future-agent re-reads (e.g., a downstream agent reading a DoD review for context) don't lose intent
- **full** introduces fragments that can be misparsed by a downstream agent looking for specific technical statements
- **ultra** abbreviation conflicts with our existing technical-term-exact discipline (e.g., "config" must remain "configuration" in some references; "req" vs "request" matters in API contexts)

If Tier 1 ships clean and telemetry shows room for further reduction, BACKLOG-103+ can experiment with `full` selectively.

## References

- caveman repo: https://github.com/juliusbrussee/caveman
- caveman SKILL.md (rules): https://github.com/juliusbrussee/caveman/blob/main/skills/caveman/SKILL.md
- BACKLOG-100 (Wave 0 — provides telemetry substrate)
- BACKLOG-101 (Wave 1 — sequential predecessor recommended)
- `.delivery/memory/topics/skill-token-economy.md` — binding decisions (rulings 1-5 still apply)

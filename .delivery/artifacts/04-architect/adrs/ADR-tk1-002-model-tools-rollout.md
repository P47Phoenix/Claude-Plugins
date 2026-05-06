# ADR-tk1-002: Model + Allowed-Tools Rollout Map

**Status**: Accepted
**Deciders**: Architect (solution_architect), Product Owner
**PRD refs**: FR-05, FR-06, FR-07, FR-08, FR-12, FR-15, FR-16
**Wave**: Wave 1 (W1-3, W1-4, W1-6)
**Date**: 2026-05-04
**Binds**: All `delivery-team/**/SKILL.md` frontmatter; `.claude-plugin/marketplace.json`;
           `delivery-team/hooks/audit_agent_prompt.py`

---

## Context

Wave 0 added `tier:` frontmatter to all 13 delivery-team SKILL.md files. Three Wave 1 work items
extend frontmatter further: routing agents need `model: haiku` declarations (W1-3); all Tier-A/B
skills need `allowed-tools` whitelists (W1-4); delivery-flow needs `model: sonnet` as orchestrator
default (W1-6).

Per the mandatory-rollout side-effect lesson: any mass-edit touching ≥3 SKILL.md files MUST be
preceded by `find delivery-team -name 'SKILL.md' | xargs wc -l | sort -rn` recorded as the
pre-rollout baseline. W1-7 resolves alias-creator's known-debt; at time of this ADR, alias-creator
is at 201 lines (over Tier-C budget by 1). Developer MUST fix alias-creator in the same commit
batch that adds `allowed-tools:` to it (W1-7), or add `allowed-tools:` to alias-creator as the
last edit after W1-7 reduces it to ≤200. Correction (W2-7 retro backport): W1-7 requires a
-2 line reduction (201→199), not -1 line — verified via `wc -l` post-Wave-1; see edit history.

Pre-rollout baseline (confirmed `wc -l`): delivery-flow 1090 · product-delivery 689 · architect 671
· developer 494 · quality 416 · operations 418 · ui 494 · user-feedback 398 · alias-creator **201**
(over Tier-C) · godot 235 · presentation 544 · paradigm/ddd 83 · paradigm/volatility 69.
No file other than alias-creator is within 1 line of its budget ceiling; mass frontmatter additions
(+2–3 lines) will not create new violations.

Plugin-dev skill routing (CLAUDE.md-binding): W1-3/4/6 modify SKILL.md → load
`plugin-dev:skill-development` first; hook edits → load `plugin-dev:hook-development` first.

---

## Decision

### W1-3 — Haiku for routing/dispatch sub-agents

1. Sub-agents whose sole responsibility is classification, dispatch, or paradigm routing MUST
   declare `model: haiku` in their agent frontmatter block within the parent SKILL.md.

2. Affected skills: `product-delivery`, `architect`, `quality`, `operations`, `ui`. Each Phase 1
   detector frontmatter block requires `role: phase-1-router`, `model: haiku`, `task: classify-and-dispatch`.

3. `audit_agent_prompt.py` MUST emit a `## Warning` block EARLY in output (signal-blocks-emitted-EARLY
   lesson) when a routing agent runs under non-Haiku model. Detection: role contains `router`,
   `detector`, `dispatch`, or `classify`. Pure Python — no LLM calls.

### W1-4 — Allowed-tools whitelist (allowlist-over-deny)

1. Base whitelist (applies to all Tier-A and Tier-B skills and any MCP-loading skill):
   ```yaml
   allowed-tools: [Read, Edit, Write, Bash, Skill, ToolSearch]
   ```

2. Tier-C leaf skills (alias-creator, godot, paradigm sub-skills) SHOULD carry the same whitelist
   but MAY omit it if the skill never requires file modification; any extension beyond the base
   list requires an inline justification comment in the frontmatter.

3. Extension protocol: add entry with inline `# justification:` comment. Example:
   `- WebFetch  # justification: delivery-flow needs live URL resolution for research-agent dispatch`

4. **Marketplace description prune (delivery-team: 913 → ≤500 chars)**. Retain trigger phrases +
   skill count; drop expanded sub-lists. Target: "Full delivery team: 11 skills covering
   orchestration, product ownership, development (14 languages), architecture (11 roles), QA,
   operations, UI/UX, Godot, user feedback, alias creation, and presentations. Pipeline: 7 stages,
   adversarial review, self-learning memory, Git integration." (~280 chars)

### W1-6 — Sonnet default for delivery-flow orchestrator

1. `delivery-flow/SKILL.md` frontmatter MUST declare `model: sonnet`. Opus is opt-in per-stage
   only; the SKILL.md adversarial/debate/Architecture-Board sections that require Opus MUST carry
   inline `# model-override: opus` annotations to signal intentional elevation.

2. **Sonnet flip approach (open-team-decision resolved)**: Immediate flip with telemetry watch
   (not 5-run shadow A/B). Rationale: per-skill cost reduction ≥3× is the Wave 1 acceptance
   criterion; delaying to shadow A/B defers measurable savings past the sprint. Telemetry (W0-1)
   captures the before/after delta automatically; revert path is a one-line frontmatter edit.

3. `extended_thinking: false` MUST be present in delivery-flow frontmatter. Opt-in sites:
   final synthesis (M4 cluster), contested adversarial reruns, Architecture Board chief-architect
   ruling, UAT go-no-go. All other stages: false.

---

## Consequences

**Positive**:
- Haiku routing reduces classification token cost by ~3× per dispatch (measurable via telemetry).
- `allowed-tools` whitelist prevents unexpected tool invocations at session start.
- Description prune reduces `.claude-plugin/marketplace.json` session-start payload immediately.
- Sonnet default eliminates Opus over-provisioning on orchestrator scheduling and routing work.

**Negative / Trade-offs**:
- Haiku routing (W1-3): any routing decision failure on Haiku requires Sonnet re-run; adds
  one-retry latency. Mitigated by 10/10 correctness AC dogfood requirement.
- `allowed-tools` on Tier-C paradigm sub-skills may be redundant (they already use
  `disable-model-invocation: true`); add for uniformity, not functional need.
- alias-creator ordering dependency: W1-7 (-1 line) MUST precede or be batched with W1-4
  (+allowed-tools) to avoid crossing the 200-line Tier-C budget within the same PR.

---

## Alternatives Considered

| Option | Decision | Reason rejected |
|--------|----------|-----------------|
| Shadow A/B for 5 runs before Sonnet flip | Rejected | Defers initiative-level AC (≥3× cost reduction) past sprint; revert path exists if telemetry regresses |
| Allowlist only Tier-A (not Tier-B) for `allowed-tools` | Rejected | Ruling 5 (skill-token-economy.md) says SHOULD on Tier-B; omitting Tier-B leaves partial coverage and inconsistent frontmatter schema across the plugin |
| Prune marketplace description to ≤300 chars | Rejected | Drops trigger phrases needed for skill auto-discovery (Ruling 2 explicitly protects them) |

---

## Edit history

| Date | Author | Change |
|------|--------|--------|
| 2026-05-03 | Story-5 admin (W2-7) | Context section: corrected W1-7 description — alias-creator requires -2 line reduction (201→199), not -1 line. Added inline correction note in context paragraph. Post-Wave-1 `wc -l` confirmed alias-creator at 200 lines (compliant); pre-Wave-1 baseline was 201. |

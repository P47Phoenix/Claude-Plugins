# Skill Token-Economy — Binding Decisions

**Last updated**: 2026-05-03
**Scope**: All plugins in this marketplace
**Source**: 6-expert audit synthesized via debate moderator + PO ranking (`.delivery/artifacts/research/skill-token-audit-experts.md`)
**Status**: Decisions binding across all future skill work until superseded by ADR

## Five Binding Conflict Rulings

### Ruling 1 — Cache-prefix freeze + doctrine externalization sequence
- Externalize shared orchestrator doctrine to `delivery-team/references/shared/orchestrator-doctrine.md` ONCE; orchestrators link with one-line directives.
- After doctrine extraction lands, the first ~2k tokens of every Tier-A SKILL.md MUST be byte-stable across runs.
- Volatile content (dates, run IDs, dynamic config echoes) MUST appear after a `## Volatile` marker near EOF.
- Any future prefix change MUST require an ADR citing cache-cost impact.

### Ruling 2 — `disable-model-invocation` boundary
- REJECT blanket use across ~50% of skills (would break marketplace auto-discovery).
- Apply ONLY to: paradigm sub-skills, reference-only skills, sub-skills under `<plugin>/skills/paradigms/`.
- Top-level plugin skills MUST stay discoverable.
- Pair with: prune oversized top-level descriptions to ≤500 chars (delivery-flow ~1,200 → ≤500; architect ~2,000 → ≤500).

### Ruling 3 — SKILL.md line budgets
- **Tier-A** (orchestrators: delivery-flow, hardware-flow, mtg-commander): ≤500 lines
- **Tier-B** (role multiplexers: product-delivery, architect, operations, ui, quality, etc.): ≤300 lines
- **Tier-C** (single-role/leaf: alias-creator, godot, etc.): ≤200 lines
- Anchored on Anthropic-documented 500-line ceiling.
- Tier MUST be declared in SKILL.md frontmatter `tier: A|B|C`.
- CI gate fails PRs that exceed budget unless PR body contains `Budget-Exception: <ADR-link>`.

### Ruling 4 — Agent prompts as markdown references (NOT scripts)
- Multi-agent skills (mtg-commander 4 challengers, etc.) MUST extract agent prompts to `references/agent-prompts/<agent>.md`.
- Each sub-agent loads only its own prompt (via `context: fork`).
- REJECT Python `build_agent_prompt.py` script approach for v1 — escaping risk + dependency cost outweigh marginal savings.
- Revisit script approach ONLY if telemetry (W0-1 hook) shows agent prompts still dominate context post-extraction.

### Ruling 5 — `allowed-tools` whitelist scope
- REQUIRED on Tier-A orchestrators + any skill loading MCP servers
- SHOULD on Tier-B role multiplexers
- OPTIONAL on Tier-C leaf skills
- Safe base whitelist: `Read, Edit, Write, Bash, Skill, ToolSearch`
- Extend only with explicit justification per skill

## Per-Skill Default Model Map (delivery-team scope)

| Skill | Default model | Notes |
| ----- | ------------- | ----- |
| delivery-flow (orchestrator) | **Sonnet** | Routing + state edits, no domain content. Prime Directive forbids producing content. |
| product-delivery | **Sonnet** | + Haiku router for Phase 1 role detection |
| developer | **Sonnet** | + Haiku trivial-edit branch (LOC<20, no new fns, no test changes) |
| godot | **Sonnet** | GDScript well-documented |
| architect | **Mixed** | Sonnet router → Opus for design synthesis only / Sonnet for Prior Art + checklist roles (Compliance, Privacy, IR) |
| quality | **Sonnet** | + Haiku for test-case enumeration |
| operations | **Sonnet** | + Haiku for runbook/release-notes formatting |
| ui | **Sonnet** | Design system work |
| user-feedback | **Haiku** | Persona simulation is roleplay, not reasoning |
| alias-creator | **Haiku** | String mapping with personality flavor |
| presentation | **Sonnet** for compose/draft, **Haiku** for assemble/format |

### Anti-pattern: when NOT to downgrade

1. **Adversarial challengers** — capability asymmetry kills the architectural property. Anti-pattern session 0876a59e proves it (mtg-commander, 14 undetected violations).
2. **Security-review and compliance final approval** — wrong calls have legal/safety blast radius
3. **Prior-art deviation protocol** (architect Step 4) — fabricated blockers risk
4. **Transformation Planning Phase 2 (TO-BE design)** — multi-document synthesis needs Opus
5. **First run of any new skill** — gather Sonnet+ baselines before downgrading
6. **Anything that writes to `.delivery/memory/`** — bad lessons compound; keep Sonnet minimum

### Adversarial / challenger sub-agent rule (RULING 4 corollary)

- Challenger sub-agent MUST inherit primary's `model:` value at dispatch time.
- DoD validators MAY use Haiku; if a validator votes NOT_DONE, re-run that single validator at Sonnet for confirmation before reopening the loop.
- Judge / arbiter sub-agents in debate pattern: Opus (single-shot, infrequent, decision-final).
- Architecture Board personas: Sonnet for Volatility/DDD/Risk; Opus for Chief Architect final ruling only.

### Extended thinking default

- OFF by default for all sub-agent dispatches.
- ON only for: final synthesis (M4 cluster), Opus-classified architect synthesis, contested adversarial reruns, security-review.
- Saves ~3× output tokens on average sub-agent calls.

## Architectural Patterns (binding for future skill design)

### Pattern: product-delivery Phase 1/2 routing (canonical)

Every multi-role / multi-task-type skill MUST follow this shape:
1. **Phase 1: Detect** — match user request against routing table; pick role + task type
2. **Phase 2: Spawn sub-agent** — load ONLY the matched references; orchestrator never loads role-specific knowledge into main context
3. Single sub-agent prompt template (NOT one per role); reference files do per-role customization

The model skill: `delivery-team/skills/product-delivery/SKILL.md`. Other heavy skills MUST adopt this pattern.

### Pattern: Stage definitions as YAML manifest

Orchestrators with stage definitions (delivery-flow 7 stages, hardware-flow 8 stages) MUST express stages as `references/stages.yml` (one row per stage with: id, name, runs_for, primary_agent, dod_validators, output_path, max_self_correction). SKILL.md keeps a routing pointer only; loads the manifest on demand.

### Pattern: Output contracts behind task-type detection

Skills with multiple output contracts (architect 5, product-delivery 12 patterns, presentation 9 types) MUST split each contract into `references/contracts/<name>.md` (or `references/patterns/<slug>.md`). The Phase 1 detector picks the contract; Phase 2 loads only that one.

### Pattern: Paradigm sub-skill (Skill within Skill)

For axes with ≥3 mutually-exclusive variants (research types, paradigm choices, persona families), create `<plugin>/skills/<axis>/<variant>/SKILL.md` with `disable-model-invocation: true`. Parent skill is the router; sub-skills only load when selected.

## Hooks Discipline

- All hooks MUST be pure Python — NO LLM calls inside hooks.
- If reasoning is genuinely required, use Haiku 4.5 with extended thinking disabled.
- Telemetry hook (`.delivery/telemetry/skill-loads.jsonl`) MUST run on PreToolUse for `Skill` matcher; <50ms overhead per call.

## CLAUDE.md Discipline

- Project-level CLAUDE.md MUST stay ≤150 lines.
- Loaded on every Claude Code session for this repo — every line is paid for thousands of times more than any single skill.
- Detail belongs in `governance/` or per-plugin `ARCHITECTURE.md`.

## Initiative Sequencing (delivery-team first)

- **Wave 0** SHIPPED (run-2026-05-03-tk0e) — Telemetry hook + tiered line-budget CI gate (foundations)
- **Wave 1** SHIPPED (run-2026-05-04-tk1) — Cache-prefix freeze, stage YAML, Haiku routing, allowed-tools+description prune, challenger-tier rule, Sonnet orchestrators+Python hooks
- **Wave 2** SHIPPED (run-2026-05-05-tk2) — Doctrine externalization, architect/developer extractions, config/commands tables, product-delivery patterns split, architect model split
- **caveman-lite** SHIPPED (run-2026-05-05-tk3) — Status: GO; AC-13 telemetry deferred to next run; Tier-A 500/500 ceiling held via mid-implementation extraction; cache-prefix re-freeze (one-time ~2KB re-warm) accepted per ADR-tk3-001.
- **Wave 3** PLANNED + DEFERRED — BACKLOG-104 authored 2026-05-05 (345 lines, 18 WIs, 7 file-scope stories per PO recommendation, runs-the-command-verified line counts). Execution deferred from this session per user redirect (3->4); ready for fresh-session re-invocation. Initiative is at a clean handoff point: 4/5 waves SHIPPED, no in-flight ambiguity.
- **Initiative status (as of 2026-05-09)**: 4/5 milestones SHIPPED (80% complete); Wave 3 PLANNED-AND-DEFERRED; meta-retrospective at `.delivery/memory/initiative-retros/skill-token-economy-meta-retro-2026-05-09.md`. Next-plugin migration (mtg-commander Wave 0 or hardware-team Wave 0) ON HOLD until Wave 3 closes per user direction "one plugin at a time".

After delivery-team Wave 0+1 lands and proves out: hardware-team, then mtg-commander, then remaining plugins.

## Stop-rule

Defects/story rate >0.4 across any 3-PR window on this initiative → pause Wave 2 until root-cause retro completes.

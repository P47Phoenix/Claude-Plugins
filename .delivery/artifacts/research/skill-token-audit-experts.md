# Skill Token-Economy Audit — Expert Findings (2026-05-03)

**Initiative**: Reduce token/context usage in plugin skills WITHOUT degrading quality
**Scope**: All 7 plugins (audit); delivery-team prioritized for execution
**Method**: 6 parallel expert interviews → debate moderator → PO ranked backlog
**Status**: Audit complete; routed into delivery-flow as BACKLOG-100

## Repo Ground Truth (verified 2026-05-03)

- 60,652 markdown lines across plugins
- 21 SKILL.md files, 196 reference files (factoring partly done already)
- Heaviest SKILL.md (lines): mtg-commander 1184, delivery-flow 1089, hardware-flow 1023, product-delivery 688, architect 670, flow-builder 562, presentation 543, prompt-engineer 520, ui 493, developer 493, research-agent 474
- Heaviest references: team-patterns.md 960, hardware quality-gates.md 832, hardware pipeline-stages.md 722, setup-wizard.md 687, delivery pipeline-stages.md 682
- Permissive-language scan: top-6 SKILL.md files appear already directive-heavy (initial regex was non-portable; CI gate W0-2 will produce real count)
- Existing convention: hardware-team skills declare `minimum_model_tier:` in frontmatter; delivery-team and mtg-commander do not

## Key Architectural Findings

1. The repo has the right architecture (`product-delivery` proves it) but inconsistent application
2. Three patterns drive nearly all token waste:
   - **Inline payload** — multi-hundred-line agent-prompt templates and team-coding-standards scaffolds living in SKILL.md when they only fire for one downstream sub-agent
   - **Load-everything orchestrators** — delivery-flow and hardware-flow load setup wizards, every stage definition, every anti-pattern story, and every post-pipeline protocol on every invocation including pure resumes
   - **Duplicated primitives** — Prime Directive, Two-Channel rule, signal enumerations re-stated across orchestrators
3. **Model skill award**: `delivery-team/skills/product-delivery/SKILL.md` — cleanest implementation of Phase 1 detect → Phase 2 spawn-with-only-relevant-references pattern. Other heavy skills should follow.

---

## Expert 1 — Architect (10 skill decomposition recommendations)

A1. Extract long inline templates (>=80 lines) verbatim into reference files. Applies to `developer/SKILL.md` coding-standards (~155 lines), `mtg-commander/SKILL.md` 4 agent prompts (~75-130 each), presentation Step 4 PPTX/Marp blocks. Saves ~3,500 best / ~1,200 typical. Effort S, Risk Low.

A2. Split orchestrators along Phase boundaries (Setup, Routing, Execution-Protocol, Stage-Definitions). delivery-flow + hardware-flow externalize Phase 0 setup, Stage Definitions, Memory/Post-Pipeline; keep Phase 1 detect, Phase 2 memory, Phase 3 routing, 10-step skeleton inline. Saves ~6,000 best / ~2,500 typical. Effort M, Risk Med.

A3. Adopt product-delivery's Phase 1/2 routing pattern for ALL role-multiplexer skills with >2 roles (architect 670, operations 417, ui 493, hardware EE/MFG). Saves ~2,500 best / ~1,200 typical. Effort M, Risk Low.

A4. Keep declarative tables in SKILL.md but move per-key behavioral prose to companion reference (delivery-flow config table+prose, presentation editorial passes). Saves ~1,800 best / ~600 typical. Effort S, Risk Low.

A5. Factor anti-pattern/failure-mode/"common mistakes" sections to load-on-violation reference. Keep directive sentences inline; move narrative+examples. Saves ~600/600. Effort S, Risk Med.

A6. Adopt architect/paradigm sub-skill pattern (Skill within Skill) for any axis with >=3 mutually-exclusive variants (research-agent 5 types, user-feedback, presentation 9 types). Saves ~2,500 best / ~1,500 typical. Effort L, Risk Med.

A7. Collapse duplicated cross-skill primitives (Prime Directive, One Role = One Sub-Agent, Two-Channel Communication) to a shared reference at `delivery-team/references/shared/orchestrator-primitives.md`. ~250 duplicated lines across 3 orchestrators. Saves ~1,000/1,000. Effort M, Risk Med-High (load-bearing under Opus 4.7 — F-08 dispatch fusion regression).

A8. Scope output-contract/artifact-template blocks behind task-type detection (architect 5 contracts ~155 lines, product-delivery 12 patterns ~370 lines, presentation format specs). Saves ~3,500 best / ~2,000 typical. Effort M, Risk Low.

A9. Keep dispatch-time signal taxonomy in SKILL.md but move signal enumeration (lists of valid values) to one shared reference. Saves ~400/400. Effort S, Risk Low.

A10. Add `context budget` line to every SKILL.md frontmatter and enforce via skill-reviewer (orchestrators 400, role multiplexers 300, single-role 200). Saves 0 directly; gates regression. Effort S, Risk Low.

---

## Expert 2 — Developer (10 tactical token-saving recommendations)

D1. Orchestrator preamble MUST be a shared single-source reference; per-plugin SKILL.md links with 1-line directive. Saves ~1,500/orchestrator. (overlaps A7)

D2. Extract 12 `### Pattern N:` template blocks in product-delivery to `references/patterns/{slug}.md` and route by task type. Saves ~2,000. Effort M.

D3. Inline JSON I/O contracts MUST be extracted to `references/schemas/*.json` (product-delivery + mtg-commander config). Saves ~390. Effort S.

D4. mtg-commander 4 agent prompt blocks MUST be extracted to `references/agent-prompts/{agent}.md`. Saves ~3,000 orchestrator context. Effort M. (overlaps A1)

D5. Stage definition repeated 8-key blocks ×7 or 8 stages MUST become a CSV/YAML manifest in `references/stages.yml` (delivery-flow + hardware-flow). Saves ~2,750. Effort S. (overlaps A2)

D6. Theme-gated reporting MUST collapse to one branch directive plus `theme-rendering.md` reference (4 inline if/else blocks today). Saves ~725. Effort S.

D7. Replace `[INSERT CONTENTS OF references/X.md]` placeholders with deterministic Python `scripts/build_agent_prompt.py` (mtg-commander). Saves ~9,600 per pipeline run. Effort M, Risk Med. **REJECTED in debate** — markdown wins for v1.

D8. The 35-row "Config Settings Applied to Pipeline" table MUST move to `references/config-schema.md` (already exists). Saves ~810. Effort S.

D9. The 18-row "User Commands" table MUST be extracted to `references/commands.md` (delivery-flow + mtg-commander + product-delivery). Saves ~980 across 3. Effort S.

D10. The 19-row References table at end of delivery-flow/SKILL.md MUST become a `manifest.yml`. Saves ~735. Effort S.

---

## Expert 3 — Scrum Bag (10 governance recommendations)

S1. Tier-A orchestrators ≤600 lines; Tier-B role skills ≤450; Tier-C leaf ≤300. PRs that exceed fail CI unless `Budget-Exception:` ADR. New `.github/workflows/skill-token-budget.yml` + `governance/skill-budgets.json`. **Numbers revised in debate**: Tier-A 500 / Tier-B 300 / Tier-C 200 (Anthropic doc anchor).

S2. New SKILL.md content >40 net lines MUST be lazy-loadable (extract or `Inline-Justification:`). Update DoD + new growth-guard CI lint.

S3. CI MUST flag permissive language (should/can/may/might/could/try to) outside code/quote blocks; >5 hits fail. **Debate downgrade**: warn-only inside W0-2 CI gate.

S4. PostToolUse skill-load telemetry hook capturing tokens loaded per invocation → `.delivery/telemetry/skill-loads.jsonl`. **Foundational** — without measurement, every other rule is opinion.

S5. Every retro MUST publish "context tokens per pipeline run" with 5-run trend; >15% growth opens defect. (depends on S4)

S6. Pre-commit hook MUST block uncommented SKILL.md growth >10% unless `skill-growth-ack:`.

S7. ADR MUST justify any SKILL.md addition >40 lines or new always-loaded reference.

S8. Each SKILL.md MUST have `maintainer:` + `fitness_review_due:` frontmatter. Quarterly fitness review.

S9. Each quarter the highest (lines × invocation_count) skill MUST get a refactor sprint targeting >=30% reduction.

S10. CLAUDE.md MUST stay <=150 lines; lint gates. (project-level loaded every session — biggest leverage per byte)

---

## Expert 4 — Claude Code Expert (10 platform-aware recommendations)

C1. SKILL.md MUST stay under 500 lines (per Anthropic docs). Defer detail to references with link syntax. Impact Med, Confidence High.

C2. MUST declare `allowed-tools` to prevent tool schema bloat (3-5KB per skill on MCP-heavy tool sets). Impact High, Confidence High.

C3. MUST use `context: fork` (subagent context isolation) for reference-heavy skills — reference materials stay out of main context, only summary returns.

C4. MUST disable auto-invocation for reference-only skills via `disable-model-invocation: true`. **Debate ruling**: paradigm sub-skills + reference-only skills only, NOT blanket 50%.

C5. MUST use prompt caching with static CLAUDE.md and reference files (5-min TTL, 90% savings on cached reads). Impact High, Confidence High.

C6. MUST set `CLAUDE_CODE_SUBAGENT_MODEL=claude-haiku-4-5` for paradigm sub-skills. (overlaps M2/M6/M7)

C7. MUST set ~50% of skill descriptions to `disable-model-invocation: true` (21 skills × ~1-2KB = 20-25KB session-start). **Debate ruling**: REJECTED blanket; prune oversized descriptions to ≤500 chars instead.

C8. MUST use file-reference dynamic content injection `` !`cat reference/X.json` ``. **Debate**: rejected — markdown refs deliver same with no shell-execution risk.

C9. MUST route complex analysis to paired subagents (transformation-planning AS-IS/TO-BE; design-sprint PO+Architect).

C10. MUST configure `allowed-tools` whitelist on delivery-flow/architect/developer (5-8KB unused tool defs). **Debate ruling**: REQUIRED on Tier-A + MCP-loading; SHOULD on Tier-B; OPTIONAL on Tier-C. Safe base whitelist: Read, Edit, Write, Bash, Skill, ToolSearch.

---

## Expert 5 — Skill Reviewer (10 specific concrete fixes)

R1. mtg-commander/SKILL.md lines ~294-823 — externalize 4 full agent prompt templates (~530 lines). Saves ~5,000. Effort M.

R2. delivery-flow/SKILL.md lines 612-743 — collapse 7 redundant Stage Definition cards to 7-row table. Saves ~2,200. Effort S.

R3. delivery-flow/SKILL.md lines 168-210 — move Config Settings table to references/config-schema.md (already canonical). Saves ~1,400. Effort S.

R4. hardware-flow/SKILL.md lines 27-78 — de-dup Core Principles + Prime Directive with delivery-flow via shared `references/orchestrator-doctrine.md`. Saves ~3,000 across two. Effort M.

R5. mtg-commander/SKILL.md lines 41-82 — move Configuration schema + Validation Rules to references/config-walkthrough.md. Saves ~900. Effort S.

R6. delivery-flow/SKILL.md lines 372-398, 580-588, 600-606 — consolidate Theme-Gated Reporting (3 places). Saves ~700. Effort S.

R7. delivery-flow/SKILL.md lines 746-797 + 471-498 — merge Anti-Patterns + Rejected Justifications. Saves ~900. Effort S.

R8. architect/SKILL.md lines 385-537 — externalize 5 output templates to references/output-contracts.md. Saves ~1,500. Effort S.

R9. architect/SKILL.md lines 277-323 — merge Software Task Type Routing Table + Task Type Instructions (2 adjacent tables, 22 task types each). Saves ~1,100. Effort S.

R10. developer/SKILL.md lines 162-318 — externalize coding-standards template (~155 lines). Saves ~1,800. Effort S.

**Description-field audit**:
- mtg-commander: PASS (8-trigger phrase list)
- delivery-flow: PASS but bloated (~1,200 chars — prune to ~500)
- hardware-flow: PASS (weak — could add finer-grained triggers)
- product-delivery: EXCELLENT (~30 specific phrases, third-person)
- architect: PASS (60+ phrases) but ~2,000 chars — prune to ~500
- developer: STRONG (file extensions as highest-precision trigger)

**Model skill award**: `delivery-team/skills/product-delivery/SKILL.md`. What others should copy:
1. One sub-agent prompt template (not per-role/agent — mtg-commander has 4, developer embeds 2)
2. Single routing table per concern (architect violates with parallel "task instructions" table)
3. Phase structure (no 80-line defensive prose preamble like delivery-flow + hardware-flow)
4. No per-task-type embedded templates in SKILL.md
5. References referenced, not restated

---

## Expert 6 — Model-Tuning Expert (10 model selection recommendations)

M1. Orchestrators (delivery-flow, hardware-flow, mtg-commander) MUST stay on Sonnet, NOT Opus. ~5× cost reduction per orchestrator turn. Risk Low — Prime Directive forbids them from producing domain content.

M2. Role-routing/dispatch sub-agents MUST use Haiku (Phase 1 Role Detection in product-delivery, architect, quality, operations, ui). ~25× vs Opus. Risk Low.

M3. Adversarial challenger sub-agents MUST match primary's tier (NOT downgrade). Anti-pattern session 0876a59e shows what happens when challengers go weak. **Risk High if violated**.

M4. Final synthesis / debate / consensus / Architecture Board final ruling / UAT go-no-go MUST use Opus. Justified spend; rare; high blast radius.

M5. Hooks MUST avoid LLMs entirely (or Haiku if unavoidable). All 13 hooks should be pure Python. ~∞× savings.

M6. Developer skill default Sonnet, with Haiku for trivial edits (LOC<20, no new functions, no test changes — 30-40% of dev tickets). ~5× on trivial.

M7. Architect MUST split: Opus for design synthesis, Sonnet for Prior Art + classification + Compliance/Privacy/IR checklist roles. ~5× on classification phases.

M8. Hardware-team skills MUST honor declared `minimum_model_tier` AND set actual model (already declared per skill but not enforced). Convert to `model:` field + dispatcher.

M9. Prompt-cache prefix MUST be frozen — move volatile content to END of SKILL.md. ~10× input savings on warm hits. Risk Low.

M10. Extended thinking MUST be OFF by default; ON only for M4 / Opus M7 / contested adversarial reruns. ~3× on average sub-agent call.

### Per-skill default model map (delivery-team scope)

| Skill | Recommended | Rationale |
| ----- | ----------- | --------- |
| delivery-flow (orchestrator) | **Sonnet** | Routing + state edits, no domain content |
| product-delivery | **Sonnet** (+ Haiku router) | Story writing, retros — structured, not novel |
| developer | **Sonnet** (+ Haiku trivial branch) | Standard coding |
| godot | **Sonnet** | GDScript patterns are well-documented |
| architect | **Mixed: Sonnet router → Opus design / Sonnet checklist roles** | Synthesis is real, classification isn't |
| quality | **Sonnet** (+ Haiku for test-case enumeration) | Test design is structured |
| operations | **Sonnet** (+ Haiku for runbook/release-notes formatting) | Mostly templates |
| ui | **Sonnet** | Design system work |
| user-feedback | **Haiku** (per persona) | Persona simulation is roleplay, not reasoning |
| alias-creator | **Haiku** | String mapping with personality flavor |
| presentation | **Sonnet** for compose/draft, **Haiku** for assemble/format |

### Anti-pattern: when NOT to downgrade

1. Adversarial challengers (M3) — capability asymmetry kills the architectural property
2. Security-review and compliance final approval — wrong calls have legal/safety blast radius
3. Prior-art deviation protocol (architect Step 4) — fabricated blockers risk
4. Transformation Planning Phase 2 (TO-BE design) — multi-document synthesis needs Opus
5. First run of any new skill — gather Sonnet+ baselines before downgrading
6. Anything that writes to `.delivery/memory/` — bad lessons compound across runs

---

## Debate Moderator — 18 Conflict-Resolved Clusters

Methodology: Clustered 60 raw items by underlying mechanism. RICE-style scoring (R×I×C/E). 5 explicit conflict rulings (see memory topic skill-token-economy.md).

| Cluster | Sources | Score | Effort | Risk | Wave |
|--------|--------|-------|--------|------|------|
| #1 Telemetry hook | S4 | 4.5 | S | Low | W0 (foundational) |
| #2 Externalize doctrine | A7/D1/R4 | 4.5 | M | Med | W2 |
| #3 Sonnet orchestrators + Python hooks | M1/M5 | 9.0 | S | Low | W1 |
| #4 mtg-commander prompts | A1/D4/R1 | 9.0 | M | Low | DEFERRED (mtg phase) |
| #5 Stage YAML | A2/D5/R2 | 18.0 | S | Low | W1 |
| #6 Tiered budgets + CI | S1/S2/S6/C1/A10 | 18.0 | S | Low | W0 |
| #7 Cache-prefix freeze | M9 | 27.0 | S | Med | W1 |
| #8 Haiku for routing | M2/C6 | 18.0 | S | Low | W1 |
| #9 Architect output contracts | A8/R8 | 12.0 | M | Low | W2 |
| #10 Developer coding-standards | A1/R10 | 12.0 | M | Low | W2 |
| #11 Challenger-tier rule + thinking off | M3/M10 | 18.0 | S | High | W1 |
| #12 Config/commands tables | A4/D8/D9/D10/R3/R5 | 12.0 | M | Low | W2 |
| #13 product-delivery patterns | A8/D2 | 6.0 | M | Low | W2 |
| #14 Architect model split | M7 | 6.0 | M | Med | W2 |
| #15 Phase-1/2 multiplexer pattern | A3 | 4.0 | M | Med | W3 |
| #16 Paradigm sub-skill pattern | A6 | 2.67 | L | Med | W3 |
| #17 allowed-tools + description prune | C2/C7/C10 | 18.0 | S | Low | W1 |
| #18 Governance frontmatter + retro KPI | S5/S7/S8/S9/S10/A10 | 3.0 | M | Low | W3 |

### Items rejected during debate

- **D7 (build_agent_prompt.py)**: markdown references win for v1; revisit only if telemetry shows agent prompts still dominate
- **C4/C7 blanket 50% disable-model-invocation**: would break marketplace auto-discovery UX
- **C8 file-reference dynamic content injection (`!`cat`)**: shell-execution risk; markdown refs deliver same outcome
- **A5 anti-pattern sections to load-on-violation**: no runtime "violation" trigger exists; partial fold into R7
- **A9 signal taxonomy enumeration**: ~400 tokens below ROI threshold
- **S3 permissive-language hard-fail**: high false-positive rate; downgraded to warn-only

---

## Cross-references

- Conflict rulings + binding decisions: `.delivery/memory/topics/skill-token-economy.md`
- Master backlog (delivery-team scope): `.delivery/backlog/BACKLOG-100-skill-token-economy-delivery-team.md`
- Initial scan baseline (run 2026-05-03): heaviest SKILL.md mtg-commander 1184, delivery-flow 1089, hardware-flow 1023

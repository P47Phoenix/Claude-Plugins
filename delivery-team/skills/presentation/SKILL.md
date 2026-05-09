---
name: presentation
description: Presentation Composer — assembles delivery-team contributions into cohesive presentations via a 6-step flow. Supports 9 types (Sprint Review, Feature Pitch, Stakeholder Update, Technical Deep-Dive, Investor Pitch, Roadmap, Product Demo, Onboarding, Retrospective Summary) and 4 formats (structured-markdown, marp, paste-ready, pptx). Triggers on phrases like "create presentation", "sprint review", "pitch", "deep dive", "roadmap", "demo", "retro". Full per-type triggers in references/types/.
license: Apache License 2.0 - See repository LICENSE file
model_awareness: opus-4-7-frontmatter-only
last_audited: 2026-04-22
pattern_library_version: 4-7-1
tier: B
maintainer: delivery-team-leads
fitness_review_due: 2026-08-09
context_budget: 300
allowed-tools: [Read, Edit, Write, Bash, Skill, ToolSearch]
---

# Presentation Composer

## Design Principle: Compose, Don't Create

This skill is a **mini-orchestrator**, not a content creator. The Composer assembles contributions from delivery team roles (PO, Data Analyst, Developer, Architect, QA) into a cohesive presentation. Each contributing role loads its own skill to produce domain-accurate content. The Composer shapes tone, flow, density, and format — the team creates the content.

**Context isolation**: Contributing roles run as sub-agents with only their relevant artifacts. The Composer reads their draft outputs from disk. No role's full context leaks into another.

**Signal**: `SKILL_LOADED: presentation`

---

## Phase 1: Type Detection

Detect type from user request using keyword matching. If ambiguous, ask — never guess.

| Type | Keywords | Detail |
|------|----------|--------|
| Sprint Review | "sprint review", "what we delivered", "sprint demo", "end of sprint" | `references/types/sprint-review.md` |
| Feature Pitch | "pitch", "propose", "sell this feature", "why we should build" | `references/types/feature-pitch.md` |
| Stakeholder Update | "status update", "executive update", "progress report", "stakeholder" | `references/types/stakeholder-update.md` |
| Technical Deep-Dive | "technical presentation", "architecture overview", "deep dive", "how it works" | `references/types/technical-deep-dive.md` |
| Investor Pitch | "investor pitch", "fundraising deck", "pitch to investors" | `references/types/investor-pitch.md` |
| Roadmap | "roadmap", "quarterly plan", "what's coming next" | `references/types/roadmap.md` |
| Product Demo | "product demo", "feature demo", "show what we built", "demo for publisher" | `references/types/product-demo.md` |
| Onboarding | "onboarding", "project handoff", "team orientation", "getting started" | `references/types/onboarding.md` |
| Retrospective Summary | "retro summary", "retrospective presentation", "what we learned" | `references/types/retrospective-summary.md` |

### Pipeline Auto-Detection (when type not explicit)

| Stage | Default Type |
|-------|-------------|
| Idea checkpoint | Feature Pitch |
| Design after DoD | Technical Deep-Dive |
| Plan after sprint planning | Stakeholder Update |
| UAT after acceptance | Sprint Review |
| UAT release | Stakeholder Update |
| UAT stage with `audience: investor` | Investor Pitch |
| Plan after roadmap/quarterly | Roadmap |
| Development after feature completion | Product Demo |
| Post-onboarding or handoff | Onboarding |
| Post-retrospective | Retrospective Summary |

Per-type required artifacts, narrative arcs, audience defaults, and overrides are in `references/types/<type>.md`. Load only the matched type.

### Light Mode

Reduces sub-agent dispatch for simpler types. Config: `presentation.light_mode` (default `auto` — activates when 3 or fewer roles in Step 3; `always` / `never` override). User flags `present --full` / `present --light` override config.

Effects: Step 3 dispatches required roles only; Step 5 uses single reviewer (TW). Steps 1, 2, 4, 6 unchanged. Step 4 never degrades (per ADR-03).

### Threshold and Graceful Degradation

Tracks elapsed time from Step 1 start. Threshold resolution (first match wins): `presentation.thresholds.{type}` → `presentation.thresholds_default` → 90s default. Value `0` = unlimited.

At 75%: warning + Step 5 degrades to single reviewer (TW), MUST-FIX scope. Step 4 never degrades. At 100%: notice appended in Step 6.

Light mode and threshold are independent controls converging on the same levers — effects are the union, not the sum. Reviewer count never drops below 1.

### GAME_DEV Vocabulary

When `project.type: GAME_DEV` in config, adapt vocabulary across steps: sprint→milestone, features→mechanics, UAT→playtesting, modules→systems, stories→tasks, velocity→throughput. Per-type GAME_DEV variants in `references/types/<type>.md`.

---

## Phase 2: 6-Step Collaboration Flow

Load only the matched flow step file when executing each step.

| # | Step | Detail |
|---|------|--------|
| 1 | Assemble (PO) | `references/flow/assemble.md` |
| 2 | Content Gate (Automated) | `references/flow/content-gate.md` |
| 3 | Draft (Parallel — 5 Roles) | `references/flow/draft.md` |
| 4 | Compose (this skill, never degrades) | `references/flow/compose.md` |
| 5 | Review Gate (TW + UX) | `references/flow/review-gate.md` |
| 6 | User Review | `references/flow/user-review.md` |

Step 4 contains the 4 editorial passes (Emphasis > Cutting > Framing > Tension — strict order, per ADR-02). Each pass checks its `presentation.narrative.<pass>` config key; `false` skips the pass.

---

## Output Format Specifications

| Format | Detail | When to Use |
|--------|--------|-------------|
| structured-markdown (default) | `references/formats/structured-markdown.md` | Default; human-readable; wikis |
| marp | `references/formats/marp.md` | HTML/PDF slide rendering with theme |
| paste-ready | `references/formats/paste-ready.md` | Paste into PowerPoint/Google Slides templates |
| pptx | `references/formats/pptx.md` | Native PPTX with branding via template |

---

## Error Handling

| Error | Detection | Behavior |
|-------|-----------|----------|
| Missing config | `.delivery/config.yml` not found | STOP: "No delivery config found. Run setup wizard or create config." |
| Missing required artifacts | Content Gate: required paths do not exist | STOP: list missing artifacts, expected locations, creation instructions |
| Empty artifacts | File exists but 0 bytes or template-only | WARN + ask user to confirm. Affected slides use [TBD]. |
| Stale artifacts | Last modified > staleness threshold | WARN but proceed. Staleness notice on affected slides. |
| Unknown type | Type not in supported set | STOP: list supported types from Phase 1 table. |
| No pipeline state | `.delivery/state/` empty or missing | WARN: proceed with artifacts only, [TBD] for progress data |
| Partial data | Role finds insufficient data for slides | Role outputs what it can with [TBD]. Composer flags in summary. |
| python-pptx missing | format=pptx but `import pptx` fails | WARN + fall back to structured-markdown (see `references/formats/pptx.md`). |
| PPTX template missing | `--template` or config path does not exist | STOP: "Template file not found: {path}. Check the path in your config or --template flag." |
| Invalid JSON intermediate | `composed-draft.json` malformed or missing `slides` array | STOP: "Invalid JSON intermediate. Re-run Step 4 (Compose) to regenerate." |

Error message format: **what** is wrong, **where** to fix it, **how** to fix it.

---

## User Commands

| Command | Action |
|---------|--------|
| `present` | Start presentation flow (detect type from context) |
| `present [type]` | Start with explicit type |
| `present --format [fmt]` | Set output format: structured-markdown, marp, paste-ready, pptx |
| `present --audience [mode]` | Set audience: technical, executive, investor, client-facing, casual |
| `present --notes` | Enable speaker notes |
| `present --full` / `present --light` | Force full / light mode |
| `approve` / `changes` / `abort` | Step 6 outcomes |
| `no reorder` / `keep chronological` | Disable emphasis reordering |
| `restore {slide title}` | Reinsert a cut slide |
| `regenerate` | Re-run full flow with current artifacts |

---

## References

| File | Loaded When | Purpose |
|------|------------|---------|
| `references/types/<type>.md` | Type detected (Phase 1) | Per-type detection, artifacts, narrative arc, overrides |
| `references/flow/<step>.md` | Step executing (Phase 2) | Per-step detail, dispatch instructions, editorial passes |
| `references/formats/<format>.md` | Format selected | Per-format output conventions and rendering |
| `references/slide-structure.md` | Always (Step 4) | Slide types, density rules, sequencing, boundary conventions |
| `references/narrative-patterns.md` | Always (Step 4) | Per-type narrative arcs, adaptation rules, audience framing rules |
| `references/marp-templates.md` | Format is Marp | Marp syntax, directives, layouts, themes |
| `references/data-visualization.md` | Metric or architecture slides exist | Chart patterns, Mermaid diagrams, data accuracy rules |
| `scripts/generate_pptx.py` | Format is PPTX (post-approval) | Converts JSON intermediate to .pptx via python-pptx |

---

## Config Integration

Read from `.delivery/config.yml` at start of Step 1. User's explicit request overrides config. Config overrides hardcoded defaults.

| Key | Type | Default | Purpose |
|-----|------|---------|---------|
| `presentation.default_format` | string | structured-markdown | Default output format |
| `presentation.default_audience` | string | technical | Default audience mode |
| `presentation.speaker_notes` | boolean | false | Enable speaker notes by default |
| `presentation.save_to_artifacts` | boolean | true | Save approved output to artifacts dir |
| `presentation.marp_theme` | string | default | Marp theme (default, gaia, uncover) |
| `presentation.staleness_warning_days` | integer | 7 | Days before staleness warning |
| `presentation.vocabulary_overrides` | map | {} | Custom term replacements |
| `presentation.pptx_template` | string | "" | Path to .pptx template for branding |
| `presentation.pptx_font` | string | Calibri | Font family for PPTX output |
| `presentation.pptx_accent_color` | string | #2d5aa0 | Hex accent color for PPTX output |
| `presentation.light_mode` | string | auto | Light mode activation: auto, always, never |
| `presentation.thresholds` | map | {} | Per-type threshold overrides in seconds |
| `presentation.thresholds_default` | integer | 90 | Global threshold override; 0 = unlimited |
| `presentation.narrative.emphasis` | boolean | true | Pass 1: slide reordering by impact |
| `presentation.narrative.cutting` | boolean | true | Pass 2: merge/remove low-value slides |
| `presentation.narrative.framing` | boolean | true | Pass 3: audience-specific argument restructuring |
| `presentation.narrative.tension` | boolean | true | Pass 4: climax positioning |

**Precedence**: explicit request > `presentation.*` config > hardcoded defaults.

**No config?** Skill works with all defaults. Config is optional.

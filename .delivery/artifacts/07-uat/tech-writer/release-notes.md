# Release Notes — Presentation Skill v1.1

**Version**: 1.1 (Feature Release)
**Date**: 2026-04-04
**Project Type**: FEATURE
**Source Issues**: [#43](https://github.com/P47Phoenix/Claude-Plugins/issues/43), [#44](https://github.com/P47Phoenix/Claude-Plugins/issues/44), [#45](https://github.com/P47Phoenix/Claude-Plugins/issues/45), [#46](https://github.com/P47Phoenix/Claude-Plugins/issues/46)
**Skill**: `delivery-team/skills/presentation/`

---

*"I think I'm quite ready for another documentation adventure."*

This is a significant feature release for the Presentation Composer skill. Four enhancement groups bring five new presentation types, branded PowerPoint output, smarter narrative composition, and graceful performance handling -- all while keeping the existing four types, six-step flow, and three output formats working exactly as they did before. Not a single hobbit-hole was harmed in the making of this release.

---

## What's New

### 1. Five New Presentation Types (Issue #43)

The presentation skill now supports **9 types** (up from 4). Each new type includes keyword detection, pipeline auto-detection mapping, slide sequencing, narrative arc framework, and content gate configuration with required and enhancing artifacts.

| New Type | When to Use | Narrative Framework |
|----------|-------------|---------------------|
| **Investor Pitch** | Fundraising decks, pitch-to-investor sessions | Traction-Opportunity-Ask: lead with validated traction, frame market opportunity, close with a clear ask |
| **Roadmap** | Quarterly plans, multi-sprint planning visibility | Now-Next-Later: timeline-anchored progression from current work through horizon items |
| **Product Demo** | Feature showcases, publisher milestone meetings | Hook-Show-Impact: attention hook, live demonstration flow, measured impact. Includes `[DEMO]` placeholders and presenter timing notes. GAME_DEV projects automatically use publisher milestone vocabulary |
| **Onboarding** | Project handoff, team orientation, new contributor onboarding | Context-Landscape-Pathways: why the project exists, what the system looks like, how to start contributing. Defaults to "technical" audience |
| **Retrospective Summary** | Retro summaries for team or stakeholder audiences | Celebrate-Learn-Commit: wins, lessons, action commitments. Includes a **sensitivity filter** for executive/client-facing audiences that anonymizes individual feedback and generalizes to team patterns. A disclaimer is always displayed |

The error handling table now lists all 9 supported types. Requesting any of the five new types proceeds through the full 6-step flow instead of returning an "Unknown type" error.

### 2. PPTX Output Support (Issue #44)

Teams can now generate branded **PowerPoint (.pptx) files** directly from the presentation flow. A new Python script (`scripts/generate_pptx.py`) converts the composed draft artifact into a valid `.pptx` file that opens in PowerPoint and LibreOffice Impress.

**Key capabilities:**

- **Slide layout mapping**: Title slides, content slides, metrics slides, comparison slides (two-column tables), call-to-action slides (numbered lists), timeline slides, and architecture slides are each mapped to appropriate PowerPoint layouts
- **Template support**: Pass `--template path/to/template.pptx` to use your organization's slide masters, fonts, and color scheme. Without a template, sensible defaults apply (Calibri, #2d5aa0 accent)
- **Font and color configuration**: Set `presentation.pptx_font` and `presentation.pptx_accent_color` in config for project-wide branding
- **Fourth output format**: Use `present --format pptx` or set `presentation.default_format: pptx` in config. PPTX appears alongside structured-markdown, Marp, and paste-ready
- **Graceful fallback**: If `python-pptx` is not installed, the skill falls back to structured-markdown with a clear installation message
- **Mermaid diagrams**: Architecture slides render diagram annotations as bullet points with a note to render/paste the diagram separately. Image rendering is out of scope

**Important**: The `.pptx` output is programmatic, not pixel-perfect. Expect "90% done in 10 minutes" -- correct structure, readable layout, proper content placement. Minor formatting adjustments in PowerPoint are normal and expected.

### 3. Narrative Intelligence (Issue #46)

The Composer (Step 4) now exercises genuine editorial judgment. Instead of simply assembling slides in order, it evaluates, reorders, cuts, frames, and builds tension. Four new editorial capabilities:

| Capability | What It Does | Override |
|------------|-------------|----------|
| **Emphasis Selection** | Ranks feature slides by impact signals (user-facing vs internal, usage breadth, complexity resolved) and leads with the highest-impact content. Chronological order is no longer the default | Say "no reorder" or "keep chronological", or set `presentation.narrative_reorder: false` |
| **Information Cutting** | Identifies low-value slides (no trade-offs, no data, no decisions) and merges their key points into adjacent slides. A "Narrative Cuts" section in User Review explains what was condensed and why | Say "restore {slide title}" to reinsert, or set `presentation.narrative_cutting: false` |
| **Audience-Specific Framing** | Restructures slide arguments based on audience mental models -- not just vocabulary swaps. Investor audiences see market opportunity first; executives see business value; technical audiences see architecture decisions and trade-offs | Framing rules documented in `narrative-patterns.md` |
| **Narrative Tension** | For presentations with 6+ slides, identifies the single most important insight and positions it at the 60-70% mark (the climax), with preceding slides building toward it. Feature Pitches escalate from problem through failed alternatives to solution. Sprint Reviews build from goals through challenges to the key achievement | Presentations with fewer than 6 slides are unaffected |

The Review Gate (Step 5) now validates narrative quality alongside formatting. Technical Writer reviewers check whether every slide earns its place. UX Designer reviewers check whether the presentation builds toward a clear climax. Narrative quality issues classified as MUST-FIX are resolved automatically before User Review.

### 4. Performance: Light Mode, Fallback, and Progress (Issue #45)

Generation of complex presentations no longer stalls silently. Three improvements address the 90-second target:

- **Enhanced progress indicators**: Each step of the 6-step flow now outputs `[N/6] {Step name}...` with context (e.g., "[3/6] Drafting slide content... (3 roles contributing)"). Step completion summaries show what was produced
- **Light mode**: For presentation types with 3 or fewer contributing roles, light mode automatically reduces sub-agent dispatch and uses a single reviewer (Technical Writer only) instead of two. Configurable via `presentation.light_mode` (auto | always | never). Force full mode with `present --full`
- **Graceful degradation**: At 75% of the threshold, a warning appears. At 100%, remaining steps use simplified processing (single reviewer, MUST-FIX only). After completion, a notice suggests tuning options. Per-type thresholds are configurable via `presentation.thresholds`

---

## New Configuration Keys

All keys are optional with sensible defaults. They extend the existing `presentation.*` namespace following the config-schema.md v2.3 extension protocol.

| Key | Type | Default | Purpose |
|-----|------|---------|---------|
| `presentation.pptx_font` | string | `"Calibri"` | Font family for `.pptx` output |
| `presentation.pptx_accent_color` | string | `"#2d5aa0"` | Accent/heading color for `.pptx` output |
| `presentation.pptx_template` | string | `""` | Path to custom `.pptx` template file |
| `presentation.thresholds` | map | `{}` | Per-type generation threshold overrides (e.g., `sprint-review: 120`) |
| `presentation.thresholds_default` | integer | `90` | Global threshold in seconds (range: 30-300) |
| `presentation.light_mode` | string | `"auto"` | Light mode behavior: `auto`, `always`, `never` |
| `presentation.narrative_reorder` | boolean | `true` | Enable emphasis-based slide reordering |
| `presentation.narrative_cutting` | boolean | `true` | Enable low-value slide removal/merging |

---

## Breaking Changes

**None.** All changes are additive. The 4 existing presentation types (Sprint Review, Feature Pitch, Stakeholder Update, Technical Deep-Dive), the 6-step collaboration flow, and the 3 existing output formats (structured-markdown, Marp, paste-ready) function identically. Users who do not use new features see zero behavior change.

---

## Files Modified

| File | Change |
|------|--------|
| `delivery-team/skills/presentation/SKILL.md` | Added 5 new type definitions with keyword detection, pipeline auto-detection, content gate rules, and slide sequencing. Added PPTX as fourth output format. Added light mode, progress indicators, and degradation behavior. Added narrative intelligence rules (emphasis, cutting, framing, tension). Updated error handling table to list all 9 types. Updated Review Gate criteria for narrative quality validation |
| `delivery-team/skills/presentation/references/narrative-patterns.md` | Added narrative arc frameworks for 5 new types (Traction-Opportunity-Ask, Now-Next-Later, Hook-Show-Impact, Context-Landscape-Pathways, Celebrate-Learn-Commit). Added Audience Framing Rules section. Added editorial judgment reference material for emphasis selection, information cutting, and narrative tension |
| `delivery-team/skills/presentation/references/slide-structure.md` | Added slide structure definitions for 5 new types with slide sequences, layout types, and content specifications |
| `delivery-team/skills/presentation/scripts/generate_pptx.py` | **New file.** Python script for `.pptx` generation from composed draft artifacts. Supports template input, font/color config, 7 slide layout types, and graceful error handling when `python-pptx` is not installed |
| `delivery-team/skills/delivery-flow/references/config-schema.md` | Added 8 new `presentation.*` config keys to schema (v2.3 extension protocol) |

---

## Dependencies

| Dependency | Type | Notes |
|------------|------|-------|
| `python-pptx` | External (optional) | Required only for `.pptx` output. Pure Python, available on PyPI. Install with `pip install python-pptx`. Core skill operation (all 9 types, 3 text formats) works without it |

---

## Known Limitations

- **PPTX is "good enough to edit"**, not pixel-perfect. Users should expect minor formatting adjustments in PowerPoint after generation
- **Narrative intelligence rules are heuristic.** They improve most presentations but may make suboptimal choices for unusual content. All rules are overridable via config or inline commands
- **Retrospective Summary sensitivity filter** generalizes individual feedback for non-team audiences. Some nuance may be lost. Raw retro notes remain the source of truth
- **Light mode reduces collaboration depth**, not quality. Presentations in light mode may have less polish than full-mode equivalents
- **Mermaid diagrams in PPTX** are text annotations, not rendered images. Render diagrams separately and paste as images if visual diagrams are needed in PowerPoint

---

## References

- **Issue #43**: [Deferred Presentation Types](https://github.com/P47Phoenix/Claude-Plugins/issues/43)
- **Issue #44**: [python-pptx Branded Output](https://github.com/P47Phoenix/Claude-Plugins/issues/44)
- **Issue #45**: [90-Second Fallback Plan](https://github.com/P47Phoenix/Claude-Plugins/issues/45)
- **Issue #46**: [Deeper Narrative Intelligence](https://github.com/P47Phoenix/Claude-Plugins/issues/46)
- **PRD**: `.delivery/artifacts/02-refine/po/prd.md`
- **Idea Brief**: `.delivery/artifacts/01-idea/po/idea-brief.md`

---

*"There and back again -- from four presentation types to nine, from markdown-only to branded PowerPoint, from assembling slides to crafting stories. The road has grown wider, and I daresay the presentations are better for it. Now, if you'll excuse me, I believe I've earned a second breakfast."*

---

*Generated by Technical Writer (Bilbo) -- delivery-team:operations*

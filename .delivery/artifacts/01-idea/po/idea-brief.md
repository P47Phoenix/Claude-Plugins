## Idea Brief: Presentation Skill v1.1 Enhancement Batch

**Project Type**: FEATURE
**Date**: 2026-04-04
**Source**: GitHub Issues #43, #44, #45, #46 (P47Phoenix/Claude-Plugins)
**Pipeline**: Presentation v1.1 batch
**Skill Under Enhancement**: `delivery-team/skills/presentation/`

---

### Problem Statement

The presentation skill ships with 4 presentation types (Sprint Review, Feature Pitch, Stakeholder Update, Technical Deep-Dive) and produces structured markdown, Marp, or paste-ready output. It works. But it lacks the range, the craft, and the practical output path that a team needs once presentations become a regular tool in the delivery flow.

Four gaps exist today:

1. **Limited type coverage.** Five common presentation scenarios (Investor Pitch, Roadmap, Product Demo, Onboarding, Retrospective Summary) have no slide sequencing, narrative framework, or content gate configuration. Users who need these types hit a hard STOP with "Unknown type."
2. **No branded file output.** The skill produces markdown and Marp text, but teams need `.pptx` files they can hand to stakeholders, drop into email, or present in meetings without a markdown renderer. There is no path from structured output to a branded PowerPoint file.
3. **No degradation strategy for generation time.** The 6-step collaboration flow dispatches multiple sub-agents. When the 90-second target is exceeded, the user sees no progress, no fallback, and no tuning levers. Long-running presentations stall without explanation.
4. **Shallow narrative intelligence.** The Composer normalizes tone and enforces density, but it does not exercise editorial judgment: it does not choose what to emphasize, cut weak slides, reframe for specific audiences beyond vocabulary swaps, or build narrative tension toward a climax. Presentations are assembled, not crafted.

### Target Users

- **Delivery pipeline users** who create presentations as part of sprint reviews, stakeholder updates, and feature pitches within the delivery-flow pipeline
- **Product owners and team leads** who need branded `.pptx` files for stakeholders who do not use markdown tooling
- **Teams running long presentations** (10+ slides, multiple contributing roles) where generation time becomes a friction point
- **Anyone presenting to executives, investors, or external audiences** where narrative quality determines whether the message lands

### Goals

| # | Issue | Goal | Measurable Target |
|---|-------|------|-------------------|
| 1 | #43 — Deferred Types | All 5 new types (Investor Pitch, Roadmap, Product Demo, Onboarding, Retrospective Summary) are fully functional with slide sequencing, narrative arc, and content gate rules | Each new type passes a presentation flow end-to-end with no [TBD] artifacts and no fallback to "Unknown type" |
| 2 | #44 — .pptx Output | A python-pptx generation script produces branded `.pptx` files from structured presentation output | Given a composed presentation artifact, the script produces a valid `.pptx` file that opens in PowerPoint/LibreOffice with correct slide mapping, fonts, and colors |
| 3 | #45 — Degradation Strategy | The presentation flow provides progress indication and graceful degradation when the 90-second target is exceeded | Progress indicators display during generation; a light mode activates for simpler types when threshold is exceeded; per-type threshold tuning is configurable |
| 4 | #46 — Narrative Intelligence | The Composer applies editorial judgment: emphasis selection, information cutting, audience-specific framing, and narrative tension | Review Gate reviewers (TW + UX) confirm the Composer actively reorders for impact, removes weak slides, frames beyond vocabulary, and builds toward a climax |

### Constraints

- **Existing skill must remain stable.** The 4 current types, 6-step flow, and 3 output formats must continue to work exactly as they do today. This is enhancement, not rewrite.
- **Plugin structure conventions.** All changes follow the existing `delivery-team/skills/presentation/` structure: SKILL.md, references, scripts. No new top-level directories.
- **python-pptx is the only new dependency.** The `.pptx` generation path uses python-pptx (pure Python, no system dependencies). No other new libraries.
- **Config schema extension protocol.** Any new `presentation.*` config keys follow the extension protocol in `delivery-flow/references/config-schema.md` (v2.3).
- **Backward compatibility.** Users who do not use new types, `.pptx` output, or narrative features see zero behavior change.
- **Dogfooding required.** Each enhancement must be validated by actually using it within the delivery pipeline before shipping.

### Initial Scope

**Issue #43 — Deferred Types:**
- Add 5 type definitions to SKILL.md with keyword detection, pipeline auto-detection mapping, and content gate rules (required + enhancing artifacts per type)
- Add narrative arc patterns to `references/narrative-patterns.md` for each new type
- Add slide structure definitions to `references/slide-structure.md` for each new type
- Update error handling table to remove "Unknown type" for these 5 types

**Issue #44 — python-pptx Output:**
- Create a Python script in `scripts/` that reads a composed presentation artifact and generates a `.pptx` file
- Support template-based slide mapping (title slide, content slide, metric slide, closing slide)
- Handle font and color configuration from `presentation.*` config or sensible defaults
- Add `pptx` as an output format option alongside structured-markdown, Marp, and paste-ready

**Issue #45 — Degradation Strategy:**
- Add progress indicators at each step of the 6-step flow (already partially present as `[N/6]` markers; extend with elapsed time or status)
- Define a "light mode" for simpler presentation types that reduces sub-agent dispatch (fewer roles, simpler review)
- Add per-type threshold configuration in `presentation.*` config
- Document threshold tuning and light mode triggers

**Issue #46 — Narrative Intelligence:**
- Enhance the Compose step (Step 4) with editorial rules: emphasis selection (lead with most impactful slide), information cutting (remove slides below impact threshold), audience-specific framing (restructure argument for audience mental model), narrative tension (build toward climax)
- Add editorial judgment reference material to `references/narrative-patterns.md`
- Update Review Gate criteria so TW and UX reviewers validate narrative quality, not just formatting

### Out of Scope

- **New presentation types beyond the 5 listed.** No custom/user-defined type framework in this batch.
- **Real-time collaboration or live editing.** The skill remains a batch generation flow.
- **PowerPoint template design.** The `.pptx` script uses programmatic layouts, not custom `.potx` template files. Custom branding templates are a future enhancement.
- **AI-generated images or diagrams.** Slides reference existing Mermaid diagrams and data visualizations; no new image generation capability.
- **Changes to other delivery-team skills.** Contributing roles (PO, Developer, Architect, QA, TW, UX) are unchanged. Only the Composer skill and its references are modified.
- **Performance optimization of sub-agent dispatch.** Issue #45 addresses degradation and user feedback, not fundamental speed improvements to the agent framework.
- **Internationalization or localization.** Presentations remain English-only.

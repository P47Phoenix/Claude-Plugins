# PRD: Presentation Skill v1.1 Enhancement Batch

**Version**: 1.0
**Date**: 2026-04-04
**Author**: Product Owner (Gandalf)
**Status**: DRAFT
**Project Type**: FEATURE
**Pipeline Routing**: Idea > Refine > Design > Architect > Plan > Development > UAT
**Source Issues**: #43, #44, #45, #46 (P47Phoenix/Claude-Plugins)
**Skill Under Enhancement**: `delivery-team/skills/presentation/`

---

> *"A product owner is never late, nor early. They prioritize precisely when they mean to."*

The presentation skill shipped with four types, three output formats, and a six-step collaboration flow. It works -- the Fellowship has its foundation. But Middle-earth is wider than the Shire. Five presentation types have no home, stakeholders need branded PowerPoint files they can carry into meetings, the flow offers no counsel when generation runs long, and the Composer assembles slides without exercising the editorial judgment that turns competent decks into compelling ones.

This PRD addresses all four gaps as a single coordinated delivery. The existing skill remains stable -- this is enhancement, not rewrite. The four current types, six-step flow, and three output formats continue to work exactly as they do today.

---

## 1. Goals

| # | Issue | Goal | Measurable Target | Baseline | Measurement |
|---|-------|------|-------------------|----------|-------------|
| G-01 | #43 | All 5 new types fully functional with slide sequencing, narrative arc, and content gate rules | Each new type passes end-to-end flow with zero `[TBD]` artifacts and zero "Unknown type" errors | 0/5 types functional | Dogfooding: each type exercised with real pipeline artifacts |
| G-02 | #44 | python-pptx script produces branded `.pptx` files from structured output | Given a composed artifact, script produces a valid `.pptx` that opens in PowerPoint/LibreOffice with correct slide mapping | No `.pptx` path exists | Manual validation on both platforms |
| G-03 | #45 | Progress indication and graceful degradation when 90-second target is exceeded | Progress indicators display during generation; light mode activates for simple types; per-type thresholds configurable | No fallback behavior exists | Timed dogfooding runs |
| G-04 | #46 | Composer applies editorial judgment: emphasis, cutting, framing, tension | TW + UX reviewers confirm active reorder, slide removal, audience framing, and climax positioning | Composer normalizes tone but does not make editorial choices | A/B comparison across audience modes during dogfooding |

---

## 2. User Personas

| Persona | Role | Primary Need | Relevant Issues |
|---------|------|-------------|-----------------|
| **Priya** | Startup CTO | Investor pitch decks in 10 minutes -- "If I can go from 'we have an investor meeting Thursday' to 'here's a first draft pitch deck,' that's game-changing." | #43, #46 |
| **Marcus** | Enterprise Tech Lead | Quarterly roadmap presentations for VPs. Branded `.pptx` files that meet corporate template standards. "It has to produce output I can get into our corporate .pptx template." | #43, #44 |
| **Chen** | Consultant | Client-facing onboarding and handoff presentations. Each client has different branding. Format flexibility is essential. High-stakes -- the lasting artifact of an entire engagement. | #43, #44, #46 |
| **Jake** | Game Dev Lead | Monthly product demo presentations for publisher milestone meetings. Regular cadence means generation speed matters. | #43, #45 |

---

## 3. Functional Requirements

### Group A: Deferred Presentation Types (Issue #43)

#### FR-01: Investor Pitch Type Definition

The presentation skill shall support an "Investor Pitch" presentation type with keyword detection, pipeline auto-detection mapping, slide sequencing, narrative framework, and content gate configuration.

**Acceptance Criteria:**

| AC | Criterion |
|----|-----------|
| FR-01.1 | **Given** a user says "investor pitch", "fundraising deck", or "pitch to investors", **When** the presentation skill processes the request, **Then** it detects the Investor Pitch type and begins the 6-step flow. |
| FR-01.2 | **Given** the pipeline is at UAT stage with `audience: investor` in context, **When** presentation type is not explicit, **Then** the skill auto-detects Investor Pitch. |
| FR-01.3 | **Given** an Investor Pitch is requested, **When** the Content Gate (Step 2) runs, **Then** it validates required artifacts (idea brief or PRD, traction/metrics data) and enhancing artifacts (competitive analysis, financial projections, team bios). |
| FR-01.4 | **Given** an Investor Pitch is composed, **When** the Composer applies the narrative arc, **Then** it uses a Traction-Opportunity-Ask framework as defined in `narrative-patterns.md`. |
| FR-01.5 | **Given** an Investor Pitch, **When** slide sequencing is applied, **Then** it follows: Title, Traction/Problem Validation, Market Opportunity, Solution/Product, Business Model, Metrics/Traction Proof, Team (optional), The Ask, Call-to-Action. |

#### FR-02: Roadmap Type Definition

The presentation skill shall support a "Roadmap" presentation type distinct from Stakeholder Update, focused on multi-sprint/quarter planning visibility.

**Acceptance Criteria:**

| AC | Criterion |
|----|-----------|
| FR-02.1 | **Given** a user says "roadmap", "quarterly plan", or "what's coming next", **When** the presentation skill processes the request, **Then** it detects the Roadmap type. |
| FR-02.2 | **Given** a Roadmap is requested, **When** the Content Gate runs, **Then** it validates required artifacts (sprint plan or backlog, pipeline state) and enhancing artifacts (architecture roadmap, risk register, resource allocation). |
| FR-02.3 | **Given** a Roadmap is composed, **When** the Composer applies the narrative arc, **Then** it uses a Now-Next-Later framework with timeline slides as the structural backbone. |
| FR-02.4 | **Given** a Roadmap presentation, **When** slide sequencing is applied, **Then** it includes: Title, Strategic Context, Now (current sprint/phase), Next (upcoming 1-2 sprints), Later (horizon items), Dependencies/Risks, Timeline Overview, Call-to-Action. |

#### FR-03: Product Demo Type Definition

The presentation skill shall support a "Product Demo" presentation type optimized for feature showcase with visual placeholders.

**Acceptance Criteria:**

| AC | Criterion |
|----|-----------|
| FR-03.1 | **Given** a user says "product demo", "feature demo", "show what we built", or "demo for publisher", **When** the presentation skill processes the request, **Then** it detects the Product Demo type. |
| FR-03.2 | **Given** a Product Demo is requested, **When** the Content Gate runs, **Then** it validates required artifacts (at least 1 feature artifact: FKC, implementation doc, or UAT report) and enhancing artifacts (screenshots, user feedback, metrics). |
| FR-03.3 | **Given** a Product Demo is composed, **When** the Composer applies the narrative arc, **Then** it uses a Hook-Show-Impact framework (attention hook, live demonstration flow, measured impact). |
| FR-03.4 | **Given** a Product Demo presentation, **When** slide sequencing is applied, **Then** it includes Demo/Screenshot slides with `[DEMO]` placeholders and presenter timing notes in speaker notes. |
| FR-03.5 | **Given** a Product Demo with GAME_DEV project type, **When** the Composer composes slides, **Then** it uses "publisher milestone" vocabulary and structures the demo around gameplay mechanics, not feature lists. |

#### FR-04: Onboarding Type Definition

The presentation skill shall support an "Onboarding" presentation type for project handoff and team onboarding contexts.

**Acceptance Criteria:**

| AC | Criterion |
|----|-----------|
| FR-04.1 | **Given** a user says "onboarding", "project handoff", "team orientation", or "getting started", **When** the presentation skill processes the request, **Then** it detects the Onboarding type. |
| FR-04.2 | **Given** an Onboarding is requested, **When** the Content Gate runs, **Then** it validates required artifacts (architecture overview or system documentation, at least 1 ADR or design decision doc) and enhancing artifacts (team topology, dev environment setup, glossary). |
| FR-04.3 | **Given** an Onboarding is composed, **When** the Composer applies the narrative arc, **Then** it uses a Context-Landscape-Pathways framework (why this project exists, what the system looks like, how to start contributing). |
| FR-04.4 | **Given** an Onboarding presentation, **When** the audience mode is not explicitly set, **Then** the default audience is "technical" (the most common onboarding scenario). |
| FR-04.5 | **Given** an Onboarding presentation, **When** slide sequencing is applied, **Then** it includes: Title, Project Context (why it exists), System Landscape (architecture overview), Key Decisions (ADRs/design rationale), Development Pathways (how to contribute), Resources/Links, Call-to-Action (first tasks). |

#### FR-05: Retrospective Summary Type Definition

The presentation skill shall support a "Retrospective Summary" presentation type with dual-audience handling for sensitive team feedback content.

**Acceptance Criteria:**

| AC | Criterion |
|----|-----------|
| FR-05.1 | **Given** a user says "retro summary", "retrospective presentation", or "what we learned", **When** the presentation skill processes the request, **Then** it detects the Retrospective Summary type. |
| FR-05.2 | **Given** a Retrospective Summary is requested, **When** the Content Gate runs, **Then** it validates required artifacts (retrospective notes or action items) and enhancing artifacts (velocity trends, defect data, previous retro actions). |
| FR-05.3 | **Given** a Retrospective Summary is composed, **When** the Composer applies the narrative arc, **Then** it uses a Celebrate-Learn-Commit framework (wins, lessons, action commitments). |
| FR-05.4 | **Given** a Retrospective Summary with audience mode "executive" or "client-facing", **When** the Composer composes slides, **Then** it applies a sensitivity filter: generalizes individual feedback to team patterns, omits names from specific feedback, frames challenges as process improvements not personnel issues. |
| FR-05.5 | **Given** a Retrospective Summary, **When** the skill outputs the presentation, **Then** it displays a disclaimer: "This presentation summarizes team retrospective themes. Individual feedback has been anonymized and generalized." |
| FR-05.6 | **Given** a Retrospective Summary with audience mode "technical" or "casual", **When** the Composer composes slides, **Then** the sensitivity filter does not apply -- full detail from retro notes is preserved (team-internal audiences). |

#### FR-06: Error Handling Update for New Types

The error handling table shall no longer return "Unknown type" for the five new presentation types.

**Acceptance Criteria:**

| AC | Criterion |
|----|-----------|
| FR-06.1 | **Given** a user requests any of the 5 new types, **When** the skill processes the request, **Then** it proceeds with the 6-step flow instead of returning an "Unknown type" error. |
| FR-06.2 | **Given** a user requests a type that is genuinely unsupported (not one of the 9 types), **When** the skill processes the request, **Then** the error message lists all 9 supported types. |

---

### Group B: python-pptx Branded Output (Issue #44)

#### FR-07: PPTX Generation Script

A Python script in `delivery-team/skills/presentation/scripts/` shall generate a `.pptx` file from the presentation skill's structured output (composed draft artifact).

**Acceptance Criteria:**

| AC | Criterion |
|----|-----------|
| FR-07.1 | **Given** a composed presentation artifact at `.delivery/artifacts/presentations/.drafts/composed-draft.md`, **When** the script is executed, **Then** it produces a valid `.pptx` file that opens without error in PowerPoint and LibreOffice Impress. |
| FR-07.2 | **Given** a composed draft with N content slides, **When** the script generates `.pptx`, **Then** each markdown slide maps to exactly one PowerPoint slide with correct title and content placement. |
| FR-07.3 | **Given** the script is run, **When** `python-pptx` is not installed, **Then** it exits with a clear error message: "python-pptx is required. Install with: pip install python-pptx" and does not crash with an unhandled ImportError. |

#### FR-08: Slide Layout Mapping

The PPTX generation script shall map presentation slide types to appropriate PowerPoint slide layouts.

**Acceptance Criteria:**

| AC | Criterion |
|----|-----------|
| FR-08.1 | **Given** a Title Slide in the composed draft, **When** mapped to `.pptx`, **Then** it uses the "Title Slide" layout (layout index 0) with title and subtitle placeholders populated. |
| FR-08.2 | **Given** a Content Slide, **When** mapped to `.pptx`, **Then** it uses a "Title and Content" layout with the slide title as heading and bullets as body content. |
| FR-08.3 | **Given** a Metrics Slide, **When** mapped to `.pptx`, **Then** it uses a layout with the headline finding as title and data points as formatted body content with trend indicators preserved as text. |
| FR-08.4 | **Given** a Comparison Slide, **When** mapped to `.pptx`, **Then** it renders a two-column table with headers, rows, and optional summary row. |
| FR-08.5 | **Given** a Call-to-Action Slide, **When** mapped to `.pptx`, **Then** it uses a content layout with action items formatted as a numbered list with owners bolded. |
| FR-08.6 | **Given** a Timeline Slide, **When** mapped to `.pptx`, **Then** it renders milestones as a table or sequential list with status indicators preserved as text. |
| FR-08.7 | **Given** an Architecture Slide containing a Mermaid diagram, **When** mapped to `.pptx`, **Then** it renders the diagram annotations as bullet points and includes a text note: "[Mermaid diagram -- render separately or paste as image]". Mermaid rendering to image is out of scope. |

#### FR-09: Template Support

The PPTX generation script shall accept an optional user-provided `.pptx` template file for branding.

**Acceptance Criteria:**

| AC | Criterion |
|----|-----------|
| FR-09.1 | **Given** a user provides a `.pptx` template path via `--template` argument, **When** the script generates output, **Then** it uses the template's slide masters, fonts, and color scheme. |
| FR-09.2 | **Given** no template is provided, **When** the script generates output, **Then** it uses sensible defaults: Calibri font, a neutral color palette (#2d5aa0 accent), and standard slide layouts. |
| FR-09.3 | **Given** a template with custom slide layouts, **When** the script maps slides, **Then** it attempts to match layout names (Title Slide, Title and Content, etc.) and falls back to layout-by-index if names do not match. |

#### FR-10: PPTX as Output Format Option

The presentation skill shall support `pptx` as a fourth output format alongside structured-markdown, Marp, and paste-ready.

**Acceptance Criteria:**

| AC | Criterion |
|----|-----------|
| FR-10.1 | **Given** a user says `present --format pptx`, **When** the 6-step flow completes and the user approves, **Then** the skill invokes the PPTX generation script and saves the `.pptx` file to `.delivery/artifacts/presentations/{type}-{date}.pptx`. |
| FR-10.2 | **Given** `presentation.default_format: pptx` in config, **When** a user says `present` without explicit format, **Then** the flow uses PPTX as the default output format. |
| FR-10.3 | **Given** the user commands list, **When** `present --format` help is invoked, **Then** `pptx` appears as a valid format option alongside structured-markdown, marp, and paste-ready. |
| FR-10.4 | **Given** PPTX format is selected but `python-pptx` is not installed, **When** the flow reaches the output step, **Then** it outputs the structured markdown version with a warning: "PPTX output requires python-pptx. Install with: pip install python-pptx. Falling back to structured-markdown." |

#### FR-11: Font and Color Configuration

The PPTX generation script shall support font and color customization via config or command-line arguments.

**Acceptance Criteria:**

| AC | Criterion |
|----|-----------|
| FR-11.1 | **Given** `presentation.pptx_font` is set in config, **When** the script generates `.pptx`, **Then** it uses the specified font family for all text elements. |
| FR-11.2 | **Given** `presentation.pptx_accent_color` is set in config, **When** the script generates `.pptx`, **Then** it uses the specified hex color for headings and accent elements. |
| FR-11.3 | **Given** neither config key is set and no template is provided, **When** the script generates `.pptx`, **Then** it defaults to Calibri font and #2d5aa0 accent color. |

---

### Group C: 90-Second Fallback Plan (Issue #45)

#### FR-12: Enhanced Progress Indicators

The presentation skill shall display enhanced progress indicators at each step of the 6-step flow.

**Acceptance Criteria:**

| AC | Criterion |
|----|-----------|
| FR-12.1 | **Given** the 6-step flow is executing, **When** each step begins, **Then** the skill outputs `[N/6] {Step name}...` with a description of what is happening (e.g., "[3/6] Drafting slide content... (3 roles contributing)"). |
| FR-12.2 | **Given** a step completes, **When** the next step begins, **Then** the previous step's completion status is shown (e.g., "Draft complete: PO, Developer, Architect contributed 9 slides"). |

#### FR-13: Light Mode for Simpler Types

The presentation skill shall support a "light mode" that reduces sub-agent dispatch for presentation types with fewer contributing roles.

**Acceptance Criteria:**

| AC | Criterion |
|----|-----------|
| FR-13.1 | **Given** a presentation type that requires 3 or fewer contributing roles, **When** `presentation.light_mode` is "auto" (default) and the flow reaches Step 3, **Then** light mode activates: only required roles are dispatched and remaining role slots are skipped. |
| FR-13.2 | **Given** light mode is active, **When** the flow reaches Step 5 (Review Gate), **Then** the review uses a single reviewer (Technical Writer) instead of two (TW + UX). |
| FR-13.3 | **Given** a user explicitly requests `present --full`, **When** the flow executes, **Then** light mode is disabled regardless of type complexity, and all roles and both reviewers are dispatched. |
| FR-13.4 | **Given** `presentation.light_mode: always` in config, **When** any presentation type is requested, **Then** light mode activates regardless of type complexity. |
| FR-13.5 | **Given** `presentation.light_mode: never` in config, **When** any presentation type is requested, **Then** light mode never activates (equivalent to `--full`). |

#### FR-14: Per-Type Threshold Configuration

The presentation skill shall support configurable generation thresholds per presentation type.

**Acceptance Criteria:**

| AC | Criterion |
|----|-----------|
| FR-14.1 | **Given** `presentation.thresholds` is defined in config as a map of type to seconds (e.g., `sprint-review: 120`, `feature-pitch: 60`), **When** the flow executes for that type, **Then** the threshold for that type is used instead of the global default. |
| FR-14.2 | **Given** no per-type threshold is configured, **When** the flow executes, **Then** the global threshold of 90 seconds (or `presentation.thresholds_default` if set) applies. |
| FR-14.3 | **Given** a per-type threshold is configured as 0, **When** the flow executes, **Then** no threshold warning is issued for that type (effectively unlimited). |

#### FR-15: Degradation Behavior When Threshold Exceeded

The presentation skill shall degrade gracefully when generation exceeds the configured threshold.

**Acceptance Criteria:**

| AC | Criterion |
|----|-----------|
| FR-15.1 | **Given** the flow has exceeded 75% of the configured threshold, **When** the next step begins, **Then** the skill outputs a warning: "Approaching generation target. Remaining steps will use simplified processing." |
| FR-15.2 | **Given** the flow has exceeded 100% of the threshold and Step 5 (Review Gate) has not started, **When** the flow reaches Step 5, **Then** it uses a single reviewer instead of two and limits review scope to MUST-FIX items only (no SUGGESTION items). |
| FR-15.3 | **Given** the flow completes beyond the threshold, **When** Step 6 (User Review) presents results, **Then** it includes a notice: "Generation exceeded the {N}s target ({actual}s). Consider using `--light` or adjusting `presentation.thresholds` for this type." |

---

### Group D: Deeper Narrative Intelligence (Issue #46)

#### FR-16: Emphasis Selection

The Composer (Step 4) shall evaluate the relative importance of slides and reorder for maximum impact.

**Acceptance Criteria:**

| AC | Criterion |
|----|-----------|
| FR-16.1 | **Given** a presentation with multiple feature slides from Step 3, **When** the Composer assembles the final deck, **Then** it ranks features by impact signals (user-facing vs internal, breadth of usage, complexity resolved) and leads with the highest-impact feature. |
| FR-16.2 | **Given** a Sprint Review with 5 delivered features, **When** the Composer orders the feature slides, **Then** it does not use chronological order by default; it uses impact-ranked order. |
| FR-16.3 | **Given** the user says "no reorder" or "keep chronological", **When** the Composer assembles the deck, **Then** it preserves the original slide order from the outline. |
| FR-16.4 | **Given** `presentation.narrative_reorder: false` in config, **When** the Composer assembles any presentation, **Then** emphasis-based reordering is disabled globally. |

#### FR-17: Information Cutting

The Composer shall identify and remove or condense low-value slides to maintain narrative density.

**Acceptance Criteria:**

| AC | Criterion |
|----|-----------|
| FR-17.1 | **Given** a draft with slides that contain only obvious information (no trade-offs, no data, no decisions), **When** the Composer evaluates slides during Step 4, **Then** it flags these slides as candidates for cutting and merges their key points into adjacent slides. |
| FR-17.2 | **Given** the Composer removes or merges slides, **When** Step 6 (User Review) presents results, **Then** it includes a "Narrative Cuts" section listing what was condensed and why: "{Slide title} merged into {target slide} -- reason: {rationale}." |
| FR-17.3 | **Given** any slide removal, **When** the user reviews the presentation, **Then** the user can say "restore {slide title}" to reinsert the cut slide. |
| FR-17.4 | **Given** `presentation.narrative_cutting: false` in config, **When** the Composer assembles any presentation, **Then** information cutting is disabled globally. |

#### FR-18: Audience-Specific Framing

The Composer shall restructure slide arguments based on audience mental models, beyond vocabulary swaps.

**Acceptance Criteria:**

| AC | Criterion |
|----|-----------|
| FR-18.1 | **Given** audience mode is "investor", **When** the Composer frames a feature slide, **Then** it leads with market opportunity or traction impact, not technical implementation. |
| FR-18.2 | **Given** audience mode is "executive", **When** the Composer frames a feature slide, **Then** it leads with business value or cost impact, not technical details. |
| FR-18.3 | **Given** audience mode is "technical", **When** the Composer frames a feature slide, **Then** it leads with architecture decisions, patterns, and trade-offs. |
| FR-18.4 | **Given** a presentation type and audience mode, **When** the Composer applies framing, **Then** it uses framing rules from a new "Audience Framing Rules" section in `narrative-patterns.md`. |

#### FR-19: Narrative Tension

The Composer shall build narrative tension toward a climax point in the presentation.

**Acceptance Criteria:**

| AC | Criterion |
|----|-----------|
| FR-19.1 | **Given** a presentation with 6+ slides, **When** the Composer applies narrative tension, **Then** it identifies the single most important insight/decision/result and positions it at the 60-70% point of the presentation (the climax), with preceding slides building toward it. |
| FR-19.2 | **Given** a Feature Pitch, **When** the Composer builds tension, **Then** it escalates from problem severity through failed alternatives to the proposed solution as the climax, followed by evidence and the ask. |
| FR-19.3 | **Given** a Sprint Review, **When** the Composer builds tension, **Then** it builds from goals and challenges to the key achievement as the climax, followed by quality validation and next steps. |
| FR-19.4 | **Given** a presentation with fewer than 6 slides, **When** the Composer processes it, **Then** narrative tension rules do not apply (too few slides for meaningful arc). |

#### FR-20: Review Gate Narrative Quality Criteria

The Review Gate (Step 5) reviewers shall validate narrative quality, not just formatting and clarity.

**Acceptance Criteria:**

| AC | Criterion |
|----|-----------|
| FR-20.1 | **Given** the Technical Writer reviews the composed draft, **When** evaluating quality, **Then** the review criteria include: "Does each slide earn its place? Could any slide be cut without losing the argument?" |
| FR-20.2 | **Given** the UX Designer reviews the composed draft, **When** evaluating quality, **Then** the review criteria include: "Does the presentation build toward a clear climax? Is the strongest content positioned for maximum impact?" |
| FR-20.3 | **Given** a reviewer identifies a narrative quality issue, **When** it is classified as MUST-FIX, **Then** the Composer fixes it automatically before Step 6 (same as existing formatting MUST-FIX behavior). |

---

## 4. Non-Functional Requirements

| ID | Requirement | Acceptance Criterion |
|----|------------|---------------------|
| NFR-01 | Backward compatibility | All changes are additive. The 4 existing types, 6-step flow, 3 existing output formats, and existing `presentation.*` config keys function identically. Users who do not use new features see zero behavior change. |
| NFR-02 | Generation speed (light mode) | Simple types (3 or fewer contributing roles) complete the full 6-step flow under 60 seconds. |
| NFR-03 | Generation speed (full mode) | Complex types (4-5 roles, 10+ slides) complete under 120 seconds. Per-type thresholds allow teams to tune targets. |
| NFR-04 | Single new dependency | `python-pptx` is the only new dependency. It is optional -- core skill operation (all 9 types, 3 text formats) works without it. No other new libraries. |
| NFR-05 | Plugin structure compliance | All changes live within `delivery-team/skills/presentation/`. New files in `scripts/` (Python), `references/` (documentation), and SKILL.md. No new top-level directories. |
| NFR-06 | Config schema extension | New `presentation.*` config keys follow the extension protocol in `config-schema.md` v2.3. Keys are optional with sensible defaults. Config version bump required. |
| NFR-07 | Dogfooding validation | Each enhancement validated by actually using it within the delivery pipeline before shipping. Code review alone is not sufficient. Each new type must produce a complete presentation from real pipeline artifacts. |
| NFR-08 | PPTX output quality | Generated `.pptx` files are "good enough to edit" -- correct structure, readable layout, proper content placement. Pixel-perfect design is not expected. User disclaimer communicates this limitation. |

---

## 5. New Config Keys

These keys extend the existing `presentation.*` namespace. All are optional with defaults. Addition follows the config-schema.md v2.3 extension protocol.

| Key | Type | Default | Valid Values | Purpose |
|-----|------|---------|-------------|---------|
| `presentation.pptx_font` | string | "Calibri" | Any font name | Font family for `.pptx` output |
| `presentation.pptx_accent_color` | string | "#2d5aa0" | Hex color | Accent/heading color for `.pptx` output |
| `presentation.pptx_template` | string | "" | File path or empty | Path to custom `.pptx` template |
| `presentation.thresholds` | map | {} | type-name → seconds | Per-type generation threshold overrides |
| `presentation.thresholds_default` | integer | 90 | 30-300 | Global threshold when no per-type value is set |
| `presentation.light_mode` | string | "auto" | auto, always, never | Light mode behavior |
| `presentation.narrative_reorder` | boolean | true | true/false | Enable emphasis-based slide reordering |
| `presentation.narrative_cutting` | boolean | true | true/false | Enable low-value slide removal/merging |

---

## 6. Success Metrics

| Metric | Target | Measurement Method |
|--------|--------|--------------------|
| New type coverage | All 5 types produce end-to-end presentations with zero `[TBD]` artifacts and zero "Unknown type" errors | Dogfooding: each type exercised with real pipeline artifacts |
| PPTX output validity | Generated `.pptx` opens without error in PowerPoint and LibreOffice | Manual validation on both platforms |
| PPTX slide mapping accuracy | Each markdown slide maps to exactly one `.pptx` slide with correct content | Visual comparison: markdown vs rendered `.pptx` |
| Generation time (light) | Simple types complete under 60 seconds | Timed dogfooding runs |
| Generation time (full) | Complex types complete under 120 seconds | Timed dogfooding runs |
| Narrative emphasis | Feature slides are impact-ranked, not chronological, in dogfooding outputs | TW + UX review criteria checklist |
| Narrative cutting | At least 1 low-value slide identified and merged in presentations with 10+ draft slides | "Narrative Cuts" section present in User Review output |
| Narrative framing | Same feature described differently for investor vs technical vs executive audience | A/B comparison across audience modes |
| User satisfaction | Approved on first pass (no "changes" loop) for at least 3 of 5 new types during dogfooding | Dogfooding session logs |

---

## 7. Out of Scope

| Item | Rationale |
|------|-----------|
| Custom/user-defined presentation type framework | No type extensibility in this batch. All 9 types are hardcoded. Future enhancement. |
| Real-time collaboration or live editing | The skill remains a batch generation flow. |
| Custom `.potx` PowerPoint template design | The `.pptx` script uses programmatic layouts. Template *authoring* tools are future work. Template *consumption* (FR-09) is in scope. |
| AI-generated images or diagrams | Slides reference existing Mermaid diagrams. No new image generation. |
| Changes to contributing delivery-team roles | PO, Developer, Architect, QA, TW, UX skills unchanged. Only the Composer and its references are modified. |
| Fundamental speed optimization of sub-agent dispatch | Issue #45 addresses user feedback and degradation, not agent framework performance. |
| Internationalization / localization | Presentations remain English-only. |
| Automated `.pptx` template extraction from corporate decks | Users provide a template manually. No automated brand inference. |
| Mermaid-to-image rendering in `.pptx` | Architecture slides in `.pptx` include annotations as text. Diagram rendering requires external tooling. |

---

## 8. Constraints

1. **Existing skill stability**: The 4 current types, 6-step flow, and 3 output formats must continue to work exactly as they do today. Every change is additive.
2. **Plugin structure**: All changes live within `delivery-team/skills/presentation/`. No new top-level directories.
3. **python-pptx is the only new dependency**: Optional, only needed for `.pptx` output. Core skill has zero new dependencies.
4. **Config schema protocol**: New `presentation.*` keys follow the extension protocol in config-schema.md v2.3.
5. **Narrative intelligence is rule-based**: Emphasis, cutting, and tension rules are documented in `narrative-patterns.md` and deterministic for a given input. The Composer applies rules, not ad-hoc judgment.
6. **Retrospective sensitivity**: Retro Summary type must anonymize and generalize individual feedback for non-team audiences. This is a hard constraint, not optional.
7. **Dogfooding before shipping**: Every new type and every narrative intelligence rule must be exercised with real pipeline artifacts before the PR is merged.

---

## 9. Risks

| # | Risk | Impact | Likelihood | Mitigation |
|---|------|--------|-----------|------------|
| R1 | Narrative intelligence rules produce worse output for edge cases | Medium | Medium | All rules are overridable (`narrative_reorder: false`, `narrative_cutting: false`). User can say "no reorder" or "restore" cut slides. |
| R2 | python-pptx slide mapping loses formatting nuance | Low | High | Accept "good enough to edit" not "pixel-perfect." User disclaimer in output message (FR-10.4 fallback, NFR-08). |
| R3 | 5 new types dilute testing coverage | Medium | Medium | Each type has explicit dogfooding ACs. No type ships without a real end-to-end run (NFR-07). |
| R4 | Light mode produces noticeably lower quality than full mode | Medium | Low | Light mode reduces quantity (fewer roles, single reviewer), not quality. Review Gate still runs. User can force `--full` (FR-13.3). |
| R5 | Retro Summary sensitivity filter over-generalizes | Medium | Medium | Filter applies only for non-team audiences (FR-05.4/FR-05.6). Technical/casual get full detail. Disclaimer always shown (FR-05.5). |
| R6 | Per-type threshold config adds complexity | Low | Low | Thresholds are optional. Defaults work without config. Only power users touch this (FR-14.2). |
| R7 | Audience framing rules are too prescriptive | Medium | Medium | Framing rules are guidance, not rigid templates. Review Gate validates the result (FR-20). User can override with "changes" feedback. |

---

## 10. Dependencies

| Dependency | Type | Status |
|------------|------|--------|
| `delivery-team/skills/presentation/SKILL.md` | Existing file (modify) | Stable, v1 shipped |
| `delivery-team/skills/presentation/references/slide-structure.md` | Existing file (modify) | Stable |
| `delivery-team/skills/presentation/references/narrative-patterns.md` | Existing file (modify) | Stable |
| `delivery-team/skills/presentation/references/data-visualization.md` | Existing file (no change) | Stable |
| `delivery-team/skills/presentation/references/marp-templates.md` | Existing file (no change) | Stable |
| `delivery-team/skills/presentation/scripts/` | Directory (create + new files) | Does not exist yet |
| `python-pptx` library | External dependency (optional) | Available on PyPI, pure Python |
| `delivery-flow/references/config-schema.md` | Existing file (modify -- add keys) | v2.3, extension protocol defined |

---

## 11. Delivery Sequence

The four groups have natural ordering based on dependencies:

1. **Group A (Deferred Types)** first -- unblocks dogfooding of new types with existing output formats.
2. **Group D (Narrative Intelligence)** second -- enhances Compose step for all 9 types (including new ones from Group A).
3. **Group C (Fallback Plan)** third -- requires all types to be defined so per-type thresholds are meaningful.
4. **Group B (PPTX Output)** last -- independent output path, can be developed in parallel but validated last since it depends on composed output from all types.

Groups A and B can be developed in parallel. Groups C and D can be developed in parallel after A completes.

---

## 12. Scope Limitations Disclaimer

> **Known limitations users should be aware of:**
> - The `.pptx` output is programmatic, not pixel-perfect. Users should expect to make minor formatting adjustments in PowerPoint after generation. This is "90% done in 10 minutes" not "100% done automatically."
> - Narrative intelligence rules (emphasis, cutting, tension) are heuristic. They improve most presentations but may make suboptimal choices for unusual content. All rules are overridable via config or inline commands.
> - The Retrospective Summary sensitivity filter generalizes individual feedback for non-team audiences. Some nuance may be lost. The raw retro notes remain the source of truth.
> - Light mode reduces generation time by reducing collaboration depth. Presentations generated in light mode may have less polish than full-mode equivalents.
> - Mermaid diagrams in `.pptx` output are rendered as text annotations, not as images. Users must render diagrams separately and paste as images if visual diagrams are needed in PowerPoint.

---

## 13. Open Questions for Design/Architect Stages

| # | Question | Relevant Stage |
|---|----------|---------------|
| OQ-1 | Should the PPTX generation script parse composed-draft.md directly (regex-based) or should the Composer output an intermediate structured format (JSON/YAML) that the script consumes? Structured intermediate is more robust but adds a new artifact. | Design |
| OQ-2 | How should narrative tension rules interact with user-specified slide order from Step 1 (Assemble)? If the PO outlines a specific sequence and the Composer reorders for tension, which takes precedence? | Design |
| OQ-3 | Should the emphasis selection and information cutting rules be type-specific (different criteria per presentation type) or universal? Type-specific is more accurate but increases reference file complexity. | Design |
| OQ-4 | What is the minimum slide count for light mode to be meaningful? A 4-slide Feature Pitch may not benefit from light mode since it already dispatches minimal roles. | Architect |
| OQ-5 | Should the PPTX script support speaker notes in the generated PowerPoint? The existing flow supports speaker notes as an optional feature -- should this carry through to `.pptx` output? | Design |

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-04-04 | Initial PRD for presentation skill v1.1 batch (issues #43, #44, #45, #46). 20 functional requirements across 4 groups, 8 non-functional requirements, 8 new config keys, 5 open questions. |

---

*"All we have to decide is what to do with the features that are given to us." -- And so we have decided. Four enhancements, twenty functional requirements, nine presentation types. The road goes ever on.*

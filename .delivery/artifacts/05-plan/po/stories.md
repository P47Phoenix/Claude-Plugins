# Plan Stage — User Stories: Presentation Skill v1.1

**Pipeline**: run-2026-04-04-w7m3
**Project Type**: FEATURE
**Date**: 2026-04-04
**Author**: Product Owner (Gandalf)
**Source Issues**: #43, #44, #45, #46

> *"A product owner is never late, nor early. They prioritize precisely when they mean to. And these eight stories arrive at exactly the moment they are meant to — no sooner, no later, and certainly not all at once."*

---

## Sprint Planning Summary

| Sprint | Stories | Total SP | Utilization | Theme |
|--------|---------|----------|-------------|-------|
| Sprint 1 | US-01, US-02 | 5 | 63% | New type foundations (Group A) |
| Sprint 2 | US-07, US-08 | 6 | 75% | Narrative intelligence (Group D) |
| Sprint 3 | US-05, US-06 | 5 | 63% | Fallback & progress (Group C) |
| Sprint 4 | US-03, US-04 | 8 | 100%* | PPTX output (Group B) |

*Sprint 4 at ceiling — US-03 is the only code-tier story and carries the bulk.

**Velocity assumption**: 8 SP/sprint (based on team capacity). 80% utilization ceiling = 6.4 SP effective max per sprint, except Sprint 4 which is the final sprint and can push to ceiling.

**Delivery sequence rationale**: Group A first (unblocks dogfooding new types), Group D second (narrative intelligence applies to all 9 types including new ones), Group C third (thresholds need types defined), Group B last (independent output path, validated last since it consumes composed output from all types). This matches the PRD Section 11 recommended ordering.

---

## Sprint 1: New Type Foundations (Group A)

### US-01: Add 5 New Presentation Type Definitions

**As a** delivery team member creating presentations for investor meetings, roadmap reviews, product demos, onboarding sessions, or retrospective summaries
**I want** the presentation skill to recognize and support these 5 new presentation types with keyword detection, slide sequencing, narrative frameworks, and content gate configuration
**So that** I can generate purpose-built presentations for these common scenarios instead of forcing content into the existing 4 types

**Story Points**: 3 (markdown-only changes across SKILL.md, slide-structure.md, narrative-patterns.md — one tier below code, but substantial breadth across 5 types)
**Priority**: P1 — Critical (unblocks all other stories; types must exist before narrative intelligence, thresholds, or PPTX can target them)
**Issues**: #43
**FRs**: FR-01, FR-02, FR-03, FR-04, FR-05

---

#### Acceptance Criteria

**AC-01** — Investor Pitch type detection *(structural)*

Given SKILL.md contains a type detection table
When a reviewer inspects the table
Then "Investor Pitch" is listed with keywords: "investor pitch", "fundraising deck", "pitch to investors"
And a pipeline auto-detection mapping exists for `audience: investor` at UAT stage

**TC-01.1**: Verify keyword entry exists in SKILL.md type detection table for all three Investor Pitch keywords.
**TC-01.2**: Verify pipeline auto-detection mapping for `audience: investor` is documented.

---

**AC-02** — Investor Pitch content gate, narrative framework, and slide sequence *(structural)*

Given the Investor Pitch type is defined
When a reviewer inspects the Content Gate configuration, narrative framework mapping, and slide sequencing section
Then the Content Gate requires: idea brief or PRD, traction/metrics data; enhances with: competitive analysis, financial projections, team bios
And the narrative framework is Traction-Opportunity-Ask (defined in narrative-patterns.md)
And the slide sequence is: Title, Traction/Problem Validation, Market Opportunity, Solution/Product, Business Model, Metrics/Traction Proof, Team (optional), The Ask, Call-to-Action

**TC-02.1**: Verify Content Gate required/enhancing artifacts for Investor Pitch in SKILL.md.
**TC-02.2**: Verify Traction-Opportunity-Ask framework is defined in narrative-patterns.md and mapped to Investor Pitch.
**TC-02.3**: Verify slide sequence in slide-structure.md matches the 9-slide Investor Pitch sequence.

---

**AC-03** — Roadmap type detection, content gate, narrative framework, and slide sequence *(structural)*

Given SKILL.md contains a type detection table
When a reviewer inspects the Roadmap type definition
Then keywords include: "roadmap", "quarterly plan", "what's coming next"
And the Content Gate requires: sprint plan or backlog, pipeline state; enhances with: architecture roadmap, risk register, resource allocation
And the narrative framework is Now-Next-Later with timeline slides as structural backbone
And the slide sequence includes: Title, Strategic Context, Now, Next, Later, Dependencies/Risks, Timeline Overview, Call-to-Action

**TC-03.1**: Verify Roadmap keyword entries in SKILL.md type detection table.
**TC-03.2**: Verify Content Gate configuration for Roadmap.
**TC-03.3**: Verify Now-Next-Later framework in narrative-patterns.md mapped to Roadmap.
**TC-03.4**: Verify slide sequence in slide-structure.md for Roadmap.

---

**AC-04** — Product Demo type with DEMO placeholders and GAME_DEV vocabulary *(structural)*

Given SKILL.md contains a type detection table
When a reviewer inspects the Product Demo type definition
Then keywords include: "product demo", "feature demo", "show what we built", "demo for publisher"
And the Content Gate requires: at least 1 feature artifact (FKC, implementation doc, or UAT report); enhances with: screenshots, user feedback, metrics
And the narrative framework is Hook-Show-Impact
And the slide sequence includes Demo/Screenshot slides with `[DEMO]` placeholders and presenter timing notes in speaker notes
And a GAME_DEV variant uses "publisher milestone" vocabulary and structures around gameplay mechanics

**TC-04.1**: Verify Product Demo keyword entries in SKILL.md.
**TC-04.2**: Verify Content Gate for Product Demo.
**TC-04.3**: Verify Hook-Show-Impact framework in narrative-patterns.md.
**TC-04.4**: Verify `[DEMO]` placeholder convention in slide-structure.md.
**TC-04.5**: Verify GAME_DEV variant instructions in SKILL.md or slide-structure.md.

---

**AC-05** — Onboarding type with technical default audience *(structural)*

Given SKILL.md contains a type detection table
When a reviewer inspects the Onboarding type definition
Then keywords include: "onboarding", "project handoff", "team orientation", "getting started"
And the Content Gate requires: architecture overview or system documentation, at least 1 ADR or design decision doc; enhances with: team topology, dev environment setup, glossary
And the narrative framework is Context-Landscape-Pathways
And the slide sequence includes: Title, Project Context, System Landscape, Key Decisions, Development Pathways, Resources/Links, Call-to-Action
And the default audience mode is "technical" when not explicitly set

**TC-05.1**: Verify Onboarding keyword entries in SKILL.md.
**TC-05.2**: Verify Content Gate for Onboarding.
**TC-05.3**: Verify Context-Landscape-Pathways framework in narrative-patterns.md.
**TC-05.4**: Verify slide sequence in slide-structure.md.
**TC-05.5**: Verify default audience mode is "technical" for Onboarding.

---

**AC-06** — Retrospective Summary type with sensitivity filter and disclaimer *(structural)*

Given SKILL.md contains a type detection table
When a reviewer inspects the Retrospective Summary type definition
Then keywords include: "retro summary", "retrospective presentation", "what we learned"
And the Content Gate requires: retrospective notes or action items; enhances with: velocity trends, defect data, previous retro actions
And the narrative framework is Celebrate-Learn-Commit
And a sensitivity filter applies for "executive" or "client-facing" audience modes (generalizes individual feedback, omits names, frames challenges as process improvements)
And the sensitivity filter does NOT apply for "technical" or "casual" audience modes
And a disclaimer is always displayed: "This presentation summarizes team retrospective themes. Individual feedback has been anonymized and generalized."

**TC-06.1**: Verify Retrospective Summary keyword entries in SKILL.md.
**TC-06.2**: Verify Content Gate for Retrospective Summary.
**TC-06.3**: Verify Celebrate-Learn-Commit framework in narrative-patterns.md.
**TC-06.4**: Verify sensitivity filter rules in narrative-patterns.md for executive/client-facing audiences.
**TC-06.5**: Verify sensitivity filter is explicitly disabled for technical/casual audiences.
**TC-06.6**: Verify disclaimer text is documented in SKILL.md.

---

**AC-07** — All 5 new types produce end-to-end presentations *(empirical)*

Given all 5 new types are defined in SKILL.md with supporting references
When each type is exercised with real pipeline artifacts in a dogfooding run
Then each type completes the 6-step flow with zero `[TBD]` artifacts and zero "Unknown type" errors

**TC-07.1**: Run Investor Pitch end-to-end with real pipeline artifacts. Verify complete output.
**TC-07.2**: Run Roadmap end-to-end with real pipeline artifacts. Verify complete output.
**TC-07.3**: Run Product Demo end-to-end with real pipeline artifacts. Verify complete output.
**TC-07.4**: Run Onboarding end-to-end with real pipeline artifacts. Verify complete output.
**TC-07.5**: Run Retrospective Summary end-to-end with real pipeline artifacts. Verify complete output.

---

### US-02: Update Error Handling and Content Gate for New Types

**As a** delivery team member who requests a presentation by type
**I want** the error handling to recognize all 9 supported types and the Content Gate to validate artifacts for the new types
**So that** I receive helpful guidance when I use an unsupported type and proper artifact validation when I use a supported one

**Story Points**: 2 (markdown-only changes to SKILL.md error handling table and content gate configuration)
**Priority**: P1 — Critical (completes the type definitions; error handling is part of the user contract)
**Issues**: #43
**FRs**: FR-06

---

#### Acceptance Criteria

**AC-01** — New types do not trigger "Unknown type" error *(structural)*

Given SKILL.md contains an error handling table
When a reviewer inspects the table
Then none of the 5 new types (Investor Pitch, Roadmap, Product Demo, Onboarding, Retrospective Summary) appear as error cases
And requesting any of the 5 new types proceeds to the 6-step flow

**TC-01.1**: Verify each of the 5 new types is absent from error handling entries in SKILL.md.
**TC-01.2**: Verify each new type has a valid entry in the type detection table.

---

**AC-02** — Unsupported type error lists all 9 types *(structural)*

Given SKILL.md contains an error handling table
When a reviewer inspects the "Unknown type" error message
Then it lists all 9 supported types: Sprint Review, Feature Pitch, Stakeholder Update, Technical Deep-Dive, Investor Pitch, Roadmap, Product Demo, Onboarding, Retrospective Summary

**TC-02.1**: Verify the error message template in SKILL.md lists exactly 9 types.
**TC-02.2**: Verify each of the 9 types is spelled correctly in the error message.

---

**AC-03** — Error handling dogfooding *(empirical)*

Given the updated error handling table
When a user requests a genuinely unsupported type (e.g., "budget report")
Then the error message displays all 9 supported types

**TC-03.1**: Request an unsupported type in a dogfooding session. Verify the error message lists all 9 types.

---

## Sprint 2: Narrative Intelligence (Group D)

### US-07: Implement Editorial Passes (Emphasis, Cutting, Framing, Tension)

**As a** delivery team member generating presentations
**I want** the Composer (Step 4) to apply four editorial passes — emphasis selection, information cutting, audience framing, and narrative tension — during slide composition
**So that** generated presentations have editorial judgment: high-impact content leads, low-value slides are condensed, arguments are framed for the audience, and the narrative builds toward a climax

**Story Points**: 5 (substantial markdown additions to SKILL.md Step 4 instructions and narrative-patterns.md reference; architectural complexity in pass ordering and interaction rules)
**Priority**: P1 — High (core differentiator for v1.1; applies to all 9 types)
**Issues**: #46
**FRs**: FR-16, FR-17, FR-18, FR-19

---

#### Acceptance Criteria

**AC-01** — Emphasis selection reorders slides by impact *(structural)*

Given SKILL.md Step 4 (Compose) instructions
When a reviewer inspects the emphasis selection pass
Then the instructions direct the Composer to rank features by impact signals (user-facing vs internal, breadth of usage, complexity resolved) and lead with highest-impact
And the instructions specify impact-ranked order, not chronological, as the default
And the output includes an emphasis log (list of reorder actions)

**TC-01.1**: Verify emphasis selection pass is documented in SKILL.md Step 4.
**TC-01.2**: Verify impact signal criteria are listed.
**TC-01.3**: Verify emphasis log output is specified.

---

**AC-02** — User can disable emphasis reordering *(structural)*

Given SKILL.md contains user command handling
When a reviewer inspects the "no reorder" / "keep chronological" command
Then the instructions direct the Composer to preserve original slide order when the user says "no reorder" or "keep chronological"
And the instructions respect `presentation.narrative_reorder: false` config to disable globally

**TC-02.1**: Verify "no reorder" command is documented in SKILL.md.
**TC-02.2**: Verify `narrative_reorder: false` config handling is documented.

---

**AC-03** — Information cutting merges low-value slides *(structural)*

Given SKILL.md Step 4 (Compose) instructions
When a reviewer inspects the information cutting pass
Then the instructions direct the Composer to identify slides with only obvious information (no trade-offs, no data, no decisions) and merge key points into adjacent slides
And the output includes a cuts log with rationale: "{Slide title} merged into {target slide} — reason: {rationale}"
And the cuts log is displayed in Step 6 (User Review) as a "Narrative Cuts" section

**TC-03.1**: Verify cutting heuristics are documented in SKILL.md Step 4.
**TC-03.2**: Verify cuts log format is specified.
**TC-03.3**: Verify "Narrative Cuts" section in Step 6 output.

---

**AC-04** — User can restore cut slides *(structural)*

Given SKILL.md contains user command handling
When a reviewer inspects the "restore" command
Then the instructions direct the Composer to reinsert a cut slide when the user says "restore {slide title}"
And the instructions respect `presentation.narrative_cutting: false` config to disable globally

**TC-04.1**: Verify "restore" command is documented in SKILL.md.
**TC-04.2**: Verify `narrative_cutting: false` config handling is documented.

---

**AC-05** — Audience-specific framing restructures arguments *(structural)*

Given SKILL.md Step 4 (Compose) instructions and narrative-patterns.md
When a reviewer inspects the audience framing pass
Then the instructions direct the Composer to restructure slide arguments based on audience mode:
- "investor" → leads with market opportunity or traction impact
- "executive" → leads with business value or cost impact
- "technical" → leads with architecture decisions, patterns, trade-offs
And the framing rules are defined in a new "Audience Framing Rules" section in narrative-patterns.md

**TC-05.1**: Verify audience framing pass is documented in SKILL.md Step 4.
**TC-05.2**: Verify "Audience Framing Rules" section exists in narrative-patterns.md.
**TC-05.3**: Verify framing rules for investor, executive, and technical audiences.

---

**AC-06** — Narrative tension positions climax at 60-70% *(structural)*

Given SKILL.md Step 4 (Compose) instructions
When a reviewer inspects the narrative tension pass
Then the instructions direct the Composer to identify the single most important insight/decision/result and position it at the 60-70% point of the presentation
And the instructions specify type-specific tension patterns (Feature Pitch: problem→alternatives→solution; Sprint Review: goals→challenges→key achievement)
And the instructions specify a minimum of 6 slides for tension to apply

**TC-06.1**: Verify narrative tension pass is documented in SKILL.md Step 4.
**TC-06.2**: Verify 60-70% climax positioning rule.
**TC-06.3**: Verify type-specific tension patterns in narrative-patterns.md.
**TC-06.4**: Verify <6 slides threshold skip rule.

---

**AC-07** — Pass ordering is strictly sequential *(structural)*

Given SKILL.md Step 4 (Compose) instructions
When a reviewer inspects the editorial pass ordering
Then the passes execute in strict sequence: 1) Emphasis, 2) Cutting, 3) Framing, 4) Tension
And the rationale for ordering is documented (per architecture ADR-02)

**TC-07.1**: Verify pass ordering is explicitly documented as sequential in SKILL.md.
**TC-07.2**: Verify each pass is numbered and ordered.

---

**AC-08** — Narrative intelligence produces measurable editorial changes *(empirical)*

Given all four editorial passes are implemented
When a presentation with 10+ slides is generated in dogfooding
Then the output shows: slides reordered from chronological (emphasis log), at least 1 slide merged (cuts log), arguments framed for the specified audience, and climax positioned at 60-70% point

**TC-08.1**: Generate a Sprint Review with 10+ feature slides. Verify emphasis log shows non-chronological ordering.
**TC-08.2**: Verify cuts log shows at least 1 merge with rationale.
**TC-08.3**: Generate the same content for investor vs technical audience. Verify framing differences.
**TC-08.4**: Verify climax slide is positioned at 60-70% of the slide count.

---

### US-08: Add Narrative Intelligence Config and Review Gate Criteria

**As a** delivery team member who wants control over narrative intelligence behavior
**I want** config keys for reordering and cutting toggles, and Review Gate criteria that validate narrative quality
**So that** I can disable editorial passes when they are not helpful and have confidence that reviewers evaluate narrative quality, not just formatting

**Story Points**: 1 (small markdown additions to SKILL.md and config-schema.md)
**Priority**: P2 — Medium (config and review gate updates are small but necessary for completeness)
**Issues**: #46
**FRs**: FR-20

---

#### Acceptance Criteria

**AC-01** — Review Gate validates narrative quality *(structural)*

Given SKILL.md Step 5 (Review Gate) instructions
When a reviewer inspects the TW and UX review criteria
Then the TW criteria include: "Does each slide earn its place? Could any slide be cut without losing the argument?"
And the UX criteria include: "Does the presentation build toward a clear climax? Is the strongest content positioned for maximum impact?"

**TC-01.1**: Verify TW narrative quality criterion in SKILL.md Step 5.
**TC-01.2**: Verify UX narrative quality criterion in SKILL.md Step 5.

---

**AC-02** — Narrative MUST-FIX issues are auto-fixed *(structural)*

Given SKILL.md Step 5 (Review Gate) instructions
When a reviewer identifies a narrative quality issue classified as MUST-FIX
Then the instructions direct the Composer to fix it automatically before Step 6 (same as existing formatting MUST-FIX behavior)

**TC-02.1**: Verify MUST-FIX auto-fix behavior for narrative issues is documented in SKILL.md.

---

**AC-03** — Review Gate catches narrative issues in dogfooding *(empirical)*

Given the updated Review Gate criteria
When a presentation is generated in dogfooding with narrative intelligence enabled
Then the TW reviewer evaluates slide necessity and the UX reviewer evaluates climax positioning

**TC-03.1**: Generate a presentation and inspect Review Gate output. Verify narrative quality criteria appear in reviewer feedback.

---

## Sprint 3: Fallback & Progress (Group C)

### US-05: Implement Light Mode and Threshold Degradation

**As a** delivery team member generating presentations under time pressure
**I want** a light mode that reduces sub-agent dispatch for simpler types and graceful degradation when generation exceeds configurable thresholds
**So that** simple presentations complete faster and I get timely feedback when generation runs long instead of waiting in silence

**Story Points**: 3 (markdown-only changes to SKILL.md, but complex logic for light mode interaction with threshold degradation and config keys)
**Priority**: P2 — High (addresses the #45 user feedback about generation time)
**Issues**: #45
**FRs**: FR-13, FR-14, FR-15

---

#### Acceptance Criteria

**AC-01** — Light mode activates for types with 3 or fewer contributing roles *(structural)*

Given SKILL.md contains light mode logic
When a reviewer inspects the light mode rules
Then the instructions specify: when `presentation.light_mode` is "auto" (default) and the type requires 3 or fewer contributing roles, light mode activates
And light mode means: only required roles dispatched in Step 3, single reviewer (TW only) in Step 5

**TC-01.1**: Verify light mode activation rules in SKILL.md.
**TC-01.2**: Verify Step 3 behavior under light mode (required roles only).
**TC-01.3**: Verify Step 5 behavior under light mode (TW only).

---

**AC-02** — Light mode config options: auto, always, never *(structural)*

Given SKILL.md contains light mode config handling
When a reviewer inspects the config options
Then `presentation.light_mode: auto` (default) activates based on role count
And `presentation.light_mode: always` activates for all types
And `presentation.light_mode: never` disables light mode entirely
And `present --full` overrides light mode regardless of config

**TC-02.1**: Verify all three config values are documented in SKILL.md.
**TC-02.2**: Verify `--full` flag override is documented.

---

**AC-03** — Per-type threshold configuration *(structural)*

Given SKILL.md contains threshold logic
When a reviewer inspects the threshold configuration
Then `presentation.thresholds` accepts a map of type-name to seconds
And `presentation.thresholds_default` overrides the global 90-second default
And threshold 0 means unlimited (no warnings)
And resolution order is: per-type > thresholds_default > 90s hardcoded

**TC-03.1**: Verify threshold config keys are documented in SKILL.md.
**TC-03.2**: Verify resolution order is documented.
**TC-03.3**: Verify threshold=0 behavior is documented.

---

**AC-04** — Degradation at 75% and 100% of threshold *(structural)*

Given SKILL.md contains degradation logic
When a reviewer inspects the threshold behavior
Then at 75% of threshold: warning message displayed, Step 5 reduced to single reviewer with MUST-FIX only scope
And at 100% of threshold: Step 6 includes a notice with actual time and suggestion to use `--light` or adjust thresholds

**TC-04.1**: Verify 75% warning message text in SKILL.md.
**TC-04.2**: Verify Step 5 degradation behavior at 75%.
**TC-04.3**: Verify Step 6 notice text at 100%.

---

**AC-05** — Light mode and threshold interaction matrix *(structural)*

Given SKILL.md documents the interaction between light mode and threshold degradation
When a reviewer inspects the interaction rules
Then the four scenarios are documented: Full+under, Full+75%, Light+under, Light+75%
And the effects converge (union, not sum) — reviewer count never drops below 1

**TC-05.1**: Verify interaction matrix is documented in SKILL.md.
**TC-05.2**: Verify minimum 1 reviewer rule.

---

**AC-06** — Config keys added to config-schema.md *(structural)*

Given config-schema.md v2.3
When the new keys are added
Then `presentation.light_mode`, `presentation.thresholds`, `presentation.thresholds_default` are documented following the v2.3 extension protocol
And the schema version is bumped to v2.4

**TC-06.1**: Verify 3 new config keys in config-schema.md.
**TC-06.2**: Verify version bump to v2.4.

---

**AC-07** — Light mode and degradation work in dogfooding *(empirical)*

Given light mode and threshold logic are implemented
When a simple type (3 or fewer roles) is generated in auto light mode
Then the flow completes with reduced role dispatch and single reviewer

**TC-07.1**: Generate a Retrospective Summary (expected: few roles). Verify light mode activates.
**TC-07.2**: Verify Step 3 dispatches only required roles.
**TC-07.3**: Verify Step 5 uses single reviewer.

---

### US-06: Add Progress Indicators

**As a** delivery team member waiting for a presentation to generate
**I want** step-by-step progress indicators during the 6-step flow
**So that** I know what is happening and how far along generation is, instead of waiting in silence

**Story Points**: 2 (markdown-only changes to SKILL.md step instructions; simple addition but touches all 6 steps)
**Priority**: P2 — Medium (quality-of-life improvement from #45)
**Issues**: #45
**FRs**: FR-12

---

#### Acceptance Criteria

**AC-01** — Step begin indicator shows step number and description *(structural)*

Given SKILL.md contains step execution instructions
When a reviewer inspects each step's begin behavior
Then each step outputs: `[N/6] {Step name}... ({context})` (e.g., "[3/6] Drafting slide content... (3 roles contributing)")

**TC-01.1**: Verify progress indicator format is documented in SKILL.md for each of the 6 steps.
**TC-01.2**: Verify context information varies by step (e.g., role count for Step 3, reviewer count for Step 5).

---

**AC-02** — Step completion summary *(structural)*

Given SKILL.md contains step execution instructions
When a reviewer inspects each step's completion behavior
Then each step outputs a completion summary before the next step begins (e.g., "Draft complete: PO, Developer, Architect contributed 9 slides")

**TC-02.1**: Verify completion summary format is documented in SKILL.md.
**TC-02.2**: Verify summaries include relevant metrics (slide count, role names, reviewer findings).

---

**AC-03** — Progress indicators visible in dogfooding *(empirical)*

Given progress indicators are implemented
When a presentation is generated in dogfooding
Then each step displays begin and completion indicators

**TC-03.1**: Generate a presentation and verify all 6 step-begin indicators display.
**TC-03.2**: Verify all 6 step-completion summaries display.

---

## Sprint 4: PPTX Output (Group B)

### US-03: Implement python-pptx Generation Script

**As a** delivery team member who needs branded PowerPoint files for stakeholder meetings
**I want** a Python script that converts the Composer's structured JSON output into a valid `.pptx` file with proper slide layout mapping, template support, and font/color customization
**So that** I can produce presentation files that stakeholders can open, edit, and present in PowerPoint or LibreOffice without manual slide-by-slide reconstruction

**Story Points**: 5 (Python code — code-tier; new file with slide layout mapping, template handling, font/color config, error handling, and dependency guard)
**Priority**: P1 — High (the #44 headline feature; only code-tier story in the batch)
**Issues**: #44
**FRs**: FR-07, FR-08, FR-09

---

#### Acceptance Criteria

**AC-01** — Script produces valid PPTX from JSON intermediate *(structural)*

Given `generate_pptx.py` exists at `delivery-team/skills/presentation/scripts/`
When the script is executed with `--input` pointing to a valid `composed-draft.json`
Then it produces a `.pptx` file that opens without error in PowerPoint and LibreOffice Impress

**TC-01.1**: Run script with a sample composed-draft.json. Verify .pptx file is created at the output path.
**TC-01.2**: Open the .pptx in LibreOffice Impress. Verify no errors on open.
**TC-01.3**: Verify the .pptx is a valid ZIP archive with expected PowerPoint XML structure.

---

**AC-02** — Each JSON slide maps to exactly one PowerPoint slide *(structural)*

Given a composed-draft.json with N slides
When the script generates the .pptx
Then the output contains exactly N PowerPoint slides
And each slide has correct title and content placement

**TC-02.1**: Create a JSON with 8 slides. Run script. Verify .pptx has exactly 8 slides.
**TC-02.2**: Verify each slide's title matches the JSON `title` field.
**TC-02.3**: Verify each slide's body content matches the JSON `body` array.

---

**AC-03** — Slide layout mapping is correct *(structural)*

Given the JSON intermediate uses layout values: title, content, metrics, comparison, cta, timeline, architecture
When the script maps each slide to a PowerPoint layout
Then:
- `title` → "Title Slide" layout (index 0) with title and subtitle
- `content` → "Title and Content" layout with heading and bullets
- `metrics` → "Title and Content" with headline finding as title and data points as formatted body
- `comparison` → two-column table with headers, rows, optional summary row
- `cta` → numbered list with owners bolded
- `timeline` → table or sequential list with status indicators
- `architecture` with Mermaid → bullet points + note: "[Mermaid diagram — render separately or paste as image]"

**TC-03.1**: Create JSON with one slide of each layout type. Verify each maps to correct PowerPoint layout.
**TC-03.2**: Verify comparison slide renders as a table.
**TC-03.3**: Verify architecture slide with Mermaid includes the fallback note.
**TC-03.4**: Verify layout name-first, index-fallback matching strategy works when names don't match.

---

**AC-04** — Template support with branding precedence *(structural)*

Given the script accepts `--template`, `--font`, and `--accent-color` arguments
When a template is provided
Then the script uses the template's slide masters, fonts, and color scheme
And font/color arguments override within the loaded template
And when no template is provided, defaults are: Calibri font, #2d5aa0 accent

**TC-04.1**: Run script with --template pointing to a custom .pptx template. Verify slide masters are inherited.
**TC-04.2**: Run script with --font and --accent-color overrides. Verify overrides are applied.
**TC-04.3**: Run script with no template, no font, no color. Verify Calibri and #2d5aa0 defaults.

---

**AC-05** — Graceful dependency error *(structural)*

Given the script is run without python-pptx installed
When the import fails
Then the script exits with message: "python-pptx is required. Install with: pip install python-pptx"
And does not crash with an unhandled ImportError

**TC-05.1**: Run script in an environment without python-pptx. Verify the error message.
**TC-05.2**: Verify exit code is non-zero.
**TC-05.3**: Verify no traceback is printed.

---

**AC-06** — PPTX generation validated in dogfooding *(empirical)*

Given the script is complete
When a full presentation flow with `--format pptx` is run for at least 2 different types
Then valid .pptx files are produced that open in PowerPoint/LibreOffice with correct slide mapping

**TC-06.1**: Generate Investor Pitch as PPTX. Open in LibreOffice. Verify slides match composed draft.
**TC-06.2**: Generate Sprint Review as PPTX. Open in LibreOffice. Verify slides match composed draft.
**TC-06.3**: Verify speaker notes are present in .pptx output (if they exist in the JSON).

---

### US-04: Add PPTX Format Config, Help Text, and Fallback

**As a** delivery team member who wants to use PPTX output
**I want** `pptx` to be a recognized output format with config keys for font, color, and template, a fallback to structured-markdown when python-pptx is missing, and help text listing the new format
**So that** I can configure PPTX output in my project config and get helpful guidance when the dependency is missing

**Story Points**: 3 (markdown changes to SKILL.md for format option, fallback logic, help text, and config-schema.md for 3 new keys — one tier below code but touches multiple sections)
**Priority**: P2 — Medium (completes the PPTX user experience; depends on US-03 for the script)
**Issues**: #44
**FRs**: FR-10, FR-11

---

#### Acceptance Criteria

**AC-01** — PPTX is a recognized output format *(structural)*

Given SKILL.md contains output format handling
When a reviewer inspects the format options
Then `pptx` appears alongside structured-markdown, marp, and paste-ready
And `present --format pptx` invokes the PPTX generation script after user approval in Step 6
And the output path is `.delivery/artifacts/presentations/{type}-{date}.pptx`

**TC-01.1**: Verify `pptx` is listed in SKILL.md format options.
**TC-01.2**: Verify the invocation flow (Step 6 approval → script execution → output path).
**TC-01.3**: Verify output path pattern in SKILL.md.

---

**AC-02** — Config default format supports PPTX *(structural)*

Given SKILL.md contains config handling
When `presentation.default_format: pptx` is set in config
Then `present` without explicit format uses PPTX as default

**TC-02.1**: Verify `default_format: pptx` config handling in SKILL.md.

---

**AC-03** — Fallback to structured-markdown when python-pptx is missing *(structural)*

Given SKILL.md contains error handling
When PPTX format is selected but python-pptx is not installed
Then the skill outputs the structured-markdown version with warning: "PPTX output requires python-pptx. Install with: pip install python-pptx. Falling back to structured-markdown."

**TC-03.1**: Verify fallback behavior is documented in SKILL.md.
**TC-03.2**: Verify warning message text.

---

**AC-04** — Help text lists PPTX as valid format *(structural)*

Given SKILL.md contains format help
When `present --format` help is invoked
Then `pptx` appears as a valid option with description

**TC-04.1**: Verify help text includes pptx in SKILL.md.

---

**AC-05** — Font, color, and template config keys *(structural)*

Given config-schema.md
When the new PPTX config keys are added
Then `presentation.pptx_font` (string, default "Calibri"), `presentation.pptx_accent_color` (string, default "#2d5aa0"), and `presentation.pptx_template` (string, default "") are documented
And they follow the v2.3 extension protocol

**TC-05.1**: Verify 3 PPTX config keys in config-schema.md.
**TC-05.2**: Verify defaults match PRD (Calibri, #2d5aa0, empty).
**TC-05.3**: Verify SKILL.md references these config keys in the PPTX output section.

---

**AC-06** — JSON intermediate produced by Composer when format=pptx *(structural)*

Given SKILL.md Step 4 (Compose) instructions
When format is pptx
Then the Composer produces both `.md` and `.json` artifacts in parallel
And the JSON follows the schema defined in the architecture (slides array with number, title, layout, body, table, speaker_notes, citations, mermaid; metadata object)

**TC-06.1**: Verify JSON intermediate production is documented in SKILL.md Step 4.
**TC-06.2**: Verify JSON schema is documented or referenced.

---

**AC-07** — PPTX format config and fallback work in dogfooding *(empirical)*

Given all PPTX config and format handling is implemented
When `present --format pptx` is run and python-pptx is available
Then a valid .pptx is produced
And when python-pptx is NOT available, structured-markdown fallback occurs with warning

**TC-07.1**: Run `present --format pptx` with python-pptx installed. Verify .pptx output.
**TC-07.2**: Run `present --format pptx` without python-pptx. Verify structured-markdown fallback with warning.

---

## Story Dependency Map

```
US-01 (type definitions) ──┐
                           ├──> US-07 (editorial passes, needs all types)
US-02 (error handling)  ───┘        │
                                    ├──> US-05 (light mode + thresholds, needs types + narrative)
                                    │        │
US-08 (narrative config) ──────────┘        ├──> US-06 (progress indicators)
                                             │
US-03 (pptx script) ───────────────────────> US-04 (pptx config + format)
```

---

## Estimation Rationale

| Tier | Description | SP Range | Examples |
|------|------------|----------|----------|
| Code-tier | New Python script, logic, error handling | 5 | US-03 (generate_pptx.py) |
| Markdown-complex | Large markdown changes with interaction logic | 3-5 | US-01 (5 types), US-07 (4 editorial passes), US-04 (multi-section SKILL.md + config) |
| Markdown-moderate | Moderate markdown changes | 2-3 | US-05 (light mode + threshold), US-06 (progress indicators) |
| Markdown-simple | Small targeted markdown additions | 1-2 | US-02 (error table), US-08 (review criteria + config) |

Per the constraint: markdown-only edits are one tier lower than code changes. US-03 is the anchor at 5 SP (code-tier). All other stories are markdown-only and estimated relative to US-03.

**Total**: 24 SP across 4 sprints.

---

## Config Schema Changes Summary

All new keys added to `config-schema.md` (version bump v2.3 → v2.4):

| Key | Type | Default | Story |
|-----|------|---------|-------|
| `presentation.pptx_font` | string | "Calibri" | US-04 |
| `presentation.pptx_accent_color` | string | "#2d5aa0" | US-04 |
| `presentation.pptx_template` | string | "" | US-04 |
| `presentation.thresholds` | map | {} | US-05 |
| `presentation.thresholds_default` | integer | 90 | US-05 |
| `presentation.light_mode` | string | "auto" | US-05 |
| `presentation.narrative_reorder` | boolean | true | US-07 |
| `presentation.narrative_cutting` | boolean | true | US-07 |

---

*"Eight stories. Four sprints. Twenty functional requirements woven into independently deliverable threads. The road goes ever on — but now it has a map, and the map has mile markers. Let us walk it together, one sprint at a time."*

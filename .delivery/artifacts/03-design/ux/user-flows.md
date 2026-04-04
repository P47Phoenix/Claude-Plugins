# User Flows: Presentation Skill v1.1 Enhancements

**Version**: 1.0
**Date**: 2026-04-04
**Author**: UX Designer (Galadriel)
**Source PRD**: `.delivery/artifacts/02-refine/po/prd.md` v1.0
**Project Type**: FEATURE
**Covers**: Issues #43 (5 new types), #44 (python-pptx), #45 (90-second fallback), #46 (narrative intelligence)

---

> *"I give you the light of user flows, our most beloved design. May it be a light to you in dark places, when all other documentation goes out."*

---

## Open Question Resolutions

### OQ-1: Structured intermediate format for PPTX (DESIGN DECISION)

**Decision**: The Composer SHALL output an intermediate JSON structure alongside `composed-draft.md` when PPTX format is selected. Written to `.delivery/artifacts/presentations/.drafts/composed-draft.json`.

**Rationale**: Regex-based markdown parsing is brittle -- slide boundaries, nested bullets, tables, and Mermaid blocks create ambiguous parse states. A structured intermediate is more robust and enables future output formats without re-parsing markdown. The cost is one additional artifact in `.drafts/` (cleaned up on approve/abort like all drafts).

**JSON structure** (per slide):
```json
{
  "slides": [
    {
      "number": 1,
      "title": "...",
      "layout": "title|content|metrics|comparison|cta|timeline|architecture",
      "body": ["bullet 1", "bullet 2"],
      "table": null | { "headers": [], "rows": [[]] },
      "speaker_notes": null | "...",
      "citations": ["artifact-1.md"],
      "mermaid": null | "graph TD; ..."
    }
  ],
  "metadata": {
    "type": "investor-pitch",
    "date": "2026-04-04",
    "project": "Claude-Plugins",
    "audience": "investor",
    "format": "pptx"
  }
}
```

### OQ-2: Narrative tension vs user-specified slide order (DESIGN DECISION)

**Decision**: User-specified order from Step 1 (Assemble) takes precedence. Narrative tension reordering only applies to slides the PO did NOT explicitly sequence.

**Rule**: If the PO's outline contains explicit ordering notes (e.g., "Feature A before Feature B"), those constraints are locked. The Composer reorders only within unconstrained slide groups. If the user says "no reorder" or sets `narrative_reorder: false`, all reordering is suppressed.

### OQ-3: Type-specific vs universal emphasis/cutting rules (DESIGN DECISION)

**Decision**: Universal rules with type-specific weight modifiers. One set of emphasis criteria and cutting heuristics applies to all types, but each type defines weight adjustments.

**Example**: "Contains quantitative data" is a universal emphasis signal. For Investor Pitch, its weight is 1.5x (investors want numbers). For Onboarding, its weight is 0.5x (new team members need context over metrics).

Weight modifiers live in `narrative-patterns.md` under each type's section.

### OQ-5: Speaker notes in PPTX output (DESIGN DECISION)

**Decision**: Yes. If `--notes` is enabled, speaker notes carry through to the `.pptx` Notes pane via the `speaker_notes` field in the intermediate JSON. The python-pptx script reads this field and populates `slide.notes_slide.notes_text_frame`.

---

## Existing 6-Step Flow (Baseline)

For reference, the existing flow that all v1.1 enhancements build upon:

```
User Request
  │
  ▼
[1/6] Assemble (PO) ──── produces outline ──── USER APPROVAL
  │
  ▼
[2/6] Content Gate ────── validates artifacts ── auto (STOP/WARN/PASS)
  │
  ▼
[3/6] Draft (Parallel) ── N roles contribute ── auto
  │
  ▼
[4/6] Compose ─────────── assemble + format ─── auto
  │
  ▼
[5/6] Review Gate ──────── TW + UX review ────── auto (MUST-FIX / SUGGESTION)
  │
  ▼
[6/6] User Review ──────── approve/changes/abort ── USER DECISION
```

Human checkpoints: Step 1 (outline approval), Step 6 (final review).

All v1.1 flows below show ONLY the delta from this baseline -- what changes, what inserts, what branches. Steps not mentioned operate identically to v1.

---

## Flow Group A: New Presentation Types (#43)

### Flow A.1: Investor Pitch (FR-01)

**Trigger**: User says "investor pitch", "fundraising deck", "pitch to investors" OR pipeline is at UAT with `audience: investor`.

```
User: "present investor pitch --audience investor"
  │
  ▼
TYPE DETECTION
  ├─ keyword match: "investor pitch" → Investor Pitch
  ├─ OR pipeline auto-detect: UAT stage + investor audience → Investor Pitch
  └─ ambiguous? ASK, never guess
  │
  ▼
[1/6] Assemble (PO)
  │  PO uses Traction-Opportunity-Ask narrative framework
  │  Default slide sequence:
  │    1. Title
  │    2. Traction / Problem Validation
  │    3. Market Opportunity
  │    4. Solution / Product
  │    5. Business Model
  │    6. Metrics / Traction Proof
  │    7. Team (optional — PO includes if team bios artifact exists)
  │    8. The Ask
  │    9. Call-to-Action
  │  PO presents outline → USER APPROVAL
  │
  ▼
[2/6] Content Gate
  │  Required: idea brief OR PRD, traction/metrics data
  │  Enhancing: competitive analysis, financial projections, team bios
  │  STOP if required missing; WARN if enhancing missing
  │
  ▼
[3/6] Draft
  │  Roles dispatched:
  │    PO → narrative slides (traction, opportunity, the ask)
  │    Data Analyst → metrics/traction proof slides
  │    Developer → solution/product slides (feature highlights)
  │    Architect → business model / technical differentiation (if relevant)
  │  QA typically NOT dispatched (no test results in investor context)
  │
  ▼
[4/6] Compose → [5/6] Review Gate → [6/6] User Review
  (standard flow; narrative intelligence enhancements apply — see Group D flows)
```

**Key difference from existing types**: Investor Pitch has the widest audience-framing delta. The Composer must lead with market/traction, never technical details, even if source artifacts are technical.

---

### Flow A.2: Roadmap (FR-02)

**Trigger**: "roadmap", "quarterly plan", "what's coming next"

```
User: "present roadmap --audience executive"
  │
  ▼
[1/6] Assemble (PO)
  │  PO uses Now-Next-Later framework
  │  Default slide sequence:
  │    1. Title
  │    2. Strategic Context
  │    3. Now (current sprint/phase — active work)
  │    4. Next (upcoming 1-2 sprints — committed)
  │    5. Later (horizon items — planned but not committed)
  │    6. Dependencies / Risks
  │    7. Timeline Overview
  │    8. Call-to-Action
  │  Timeline slides are the structural backbone — PO anchors every
  │  content slide to a time horizon
  │
  ▼
[2/6] Content Gate
  │  Required: sprint plan OR backlog, pipeline state
  │  Enhancing: architecture roadmap, risk register, resource allocation
  │
  ▼
[3/6] Draft
  │  Roles dispatched:
  │    PO → strategic context, now/next/later narrative, CTA
  │    Data Analyst → timeline data, velocity projections, resource data
  │    Architect → dependency/risk slides, technical roadmap items
  │  Developer typically NOT dispatched (roadmap is planning, not implementation)
  │  QA typically NOT dispatched
  │
  ▼
[4/6]–[6/6] standard flow
```

**Key difference**: Roadmap has a temporal structure. The Composer must NOT reorder Now/Next/Later — that sequence is a constraint, not a suggestion. Narrative tension applies within each time horizon, not across them.

---

### Flow A.3: Product Demo (FR-03)

**Trigger**: "product demo", "feature demo", "show what we built", "demo for publisher"

```
User: "present product demo --notes"
  │
  ▼
[1/6] Assemble (PO)
  │  PO uses Hook-Show-Impact framework
  │  Default slide sequence:
  │    1. Title
  │    2. Attention Hook (problem or "before" state)
  │    3-N. Feature Demo slides (1 per major feature)
  │         Each contains: [DEMO] placeholder + description
  │    N+1. Impact / Results
  │    N+2. Call-to-Action
  │  --notes flag: PO includes presenter timing guidance in outline
  │
  │  GAME_DEV adaptation:
  │    "publisher milestone" vocabulary
  │    Demo slides structured around gameplay mechanics, not feature lists
  │    [DEMO] placeholders reference gameplay moments
  │
  ▼
[2/6] Content Gate
  │  Required: at least 1 feature artifact (FKC, implementation doc, OR UAT report)
  │  Enhancing: screenshots, user feedback, metrics
  │
  ▼
[3/6] Draft
  │  Roles dispatched:
  │    PO → hook slide, impact narrative
  │    Developer → feature demo slides (implementation highlights, [DEMO] points)
  │    Data Analyst → impact/metrics slide (if data exists)
  │  Speaker notes auto-enabled for Demo slides: timing + talking points
  │
  ▼
[4/6] Compose
  │  Composer adds [DEMO] placeholder formatting:
  │    "═══ LIVE DEMO: {feature name} ═══"
  │    "Duration: ~{N} minutes"
  │    "Key points to show: ..."
  │  Speaker notes include: transition cues, fallback if demo fails
  │
  ▼
[5/6]–[6/6] standard flow
```

**Key difference**: Product Demo is the only type with `[DEMO]` placeholders and mandatory speaker notes on demo slides. The Composer must preserve these -- they are presentation instructions, not content to edit.

---

### Flow A.4: Onboarding (FR-04)

**Trigger**: "onboarding", "project handoff", "team orientation", "getting started"

```
User: "present onboarding"
  │
  ▼
  │  Default audience: "technical" (no need to specify)
  │
  ▼
[1/6] Assemble (PO)
  │  PO uses Context-Landscape-Pathways framework
  │  Default slide sequence:
  │    1. Title
  │    2. Project Context (why this project exists)
  │    3. System Landscape (architecture overview)
  │    4. Key Decisions (ADRs / design rationale)
  │    5. Development Pathways (how to contribute)
  │    6. Resources / Links
  │    7. Call-to-Action (first tasks for new team member)
  │
  ▼
[2/6] Content Gate
  │  Required: architecture overview OR system documentation,
  │            at least 1 ADR or design decision doc
  │  Enhancing: team topology, dev environment setup, glossary
  │
  ▼
[3/6] Draft
  │  Roles dispatched:
  │    PO → project context, pathways, CTA
  │    Architect → system landscape, key decisions, ADR summaries
  │    Developer → development pathways (setup, workflow, conventions)
  │  Data Analyst typically NOT dispatched
  │  QA typically NOT dispatched
  │
  ▼
[4/6]–[6/6] standard flow
```

**Key difference**: Onboarding defaults to "technical" audience without asking. The Composer prioritizes clarity and completeness over narrative punch -- new team members need to understand, not be persuaded.

---

### Flow A.5: Retrospective Summary (FR-05)

**Trigger**: "retro summary", "retrospective presentation", "what we learned"

```
User: "present retro summary --audience executive"
  │
  ▼
[1/6] Assemble (PO)
  │  PO uses Celebrate-Learn-Commit framework
  │  Default slide sequence:
  │    1. Title
  │    2. Sprint/Phase Summary
  │    3. Celebrations (what went well)
  │    4. Lessons (what we learned)
  │    5. Commitments (action items + owners)
  │    6. Trends (velocity, defect rate, improvement trajectory)
  │    7. Call-to-Action
  │
  ▼
[2/6] Content Gate
  │  Required: retrospective notes OR action items
  │  Enhancing: velocity trends, defect data, previous retro actions
  │
  ▼
[3/6] Draft
  │  Roles dispatched:
  │    PO → celebrations, commitments, CTA
  │    Data Analyst → trends, velocity, defect data
  │    QA → quality lens on lessons learned (if defect data exists)
  │
  ▼
[4/6] Compose
  │  ┌─────────────────────────────────────────────┐
  │  │ SENSITIVITY FILTER (audience-conditional)    │
  │  │                                              │
  │  │ audience = "executive" | "client-facing"     │
  │  │   → FILTER ON:                               │
  │  │     • Generalize individual feedback to       │
  │  │       team patterns                           │
  │  │     • Omit names from specific feedback       │
  │  │     • Frame challenges as process             │
  │  │       improvements, not personnel issues      │
  │  │                                              │
  │  │ audience = "technical" | "casual"             │
  │  │   → FILTER OFF:                               │
  │  │     • Full detail from retro notes preserved  │
  │  └─────────────────────────────────────────────┘
  │
  │  Composer appends disclaimer to output:
  │  "This presentation summarizes team retrospective themes.
  │   Individual feedback has been anonymized and generalized."
  │
  ▼
[5/6]–[6/6] standard flow (disclaimer visible in User Review)
```

**Key difference**: Retrospective Summary is the only type with a sensitivity filter. The filter is audience-conditional and non-negotiable for executive/client-facing audiences. The disclaimer always appears regardless of audience.

---

### Flow A.6: Error Handling Update (FR-06)

**Before v1.1**:
```
User: "present investor pitch"
  → ERROR: "Unknown type. Supported types: Sprint Review, Feature Pitch,
            Stakeholder Update, Technical Deep-Dive"
```

**After v1.1**:
```
User: "present investor pitch"
  → TYPE DETECTED: Investor Pitch → proceeds to [1/6] Assemble

User: "present town hall"
  → ERROR: "Unknown type. Supported types: Sprint Review, Feature Pitch,
            Stakeholder Update, Technical Deep-Dive, Investor Pitch,
            Roadmap, Product Demo, Onboarding, Retrospective Summary"
```

All 9 types listed in error message. No other behavior change.

---

## Flow Group B: python-pptx Output (#44)

### Flow B.1: PPTX Generation (FR-07, FR-08, FR-10)

This flow shows the PPTX branch that activates after the standard 6-step flow completes.

```
User: "present sprint review --format pptx"
  │
  ▼
[1/6]–[5/6] standard flow (format selection stored, does not affect steps 1-5)
  │
  ▼
[4/6] Compose (PPTX delta)
  │  When format=pptx, Composer writes TWO artifacts:
  │    1. composed-draft.md  (standard — used by Review Gate + User Review)
  │    2. composed-draft.json (intermediate — consumed by PPTX script)
  │  JSON contains per-slide: layout type, title, body, table, citations,
  │  speaker notes, mermaid blocks (see OQ-1 resolution above)
  │
  ▼
[6/6] User Review
  │  User sees the markdown presentation (readable in CLI)
  │  Options: approve / changes / abort
  │
  ├─ "approve"
  │    │
  │    ▼
  │  PPTX GENERATION STEP (post-approval)
  │    │
  │    ├─ Check: is python-pptx installed?
  │    │   ├─ NO → output structured-markdown + warning:
  │    │   │   "PPTX output requires python-pptx. Install with:
  │    │   │    pip install python-pptx
  │    │   │    Falling back to structured-markdown."
  │    │   │   Save .md artifact. Done.
  │    │   │
  │    │   └─ YES → invoke script:
  │    │       python presentation/scripts/generate_pptx.py \
  │    │         --input .drafts/composed-draft.json \
  │    │         --output .delivery/artifacts/presentations/{type}-{date}.pptx \
  │    │         [--template {path}] \
  │    │         [--font {font}] \
  │    │         [--accent-color {hex}]
  │    │
  │    ▼
  │  Script execution:
  │    1. Parse composed-draft.json
  │    2. Load template (if provided) or create blank presentation
  │    3. For each slide:
  │       ├─ Match layout type to PowerPoint layout:
  │       │   title      → "Title Slide" (index 0)
  │       │   content    → "Title and Content" (index 1)
  │       │   metrics    → "Title and Content" with formatted data
  │       │   comparison → "Title and Content" with table
  │       │   cta        → "Title and Content" with numbered list
  │       │   timeline   → "Title and Content" with milestone table
  │       │   architecture → "Title and Content" + "[Mermaid diagram]" note
  │       ├─ Layout name matching first, fall back to index
  │       ├─ Populate title placeholder
  │       ├─ Populate body content (bullets, tables, numbered items)
  │       └─ Populate speaker notes (if present in JSON)
  │    4. Apply font + accent color (from args, config, or defaults)
  │    5. Save .pptx file
  │    6. Output: "Saved: {path} ({N} slides)"
  │
  │    ▼
  │  User message:
  │    "Presentation saved to .delivery/artifacts/presentations/{type}-{date}.pptx
  │     {N} slides generated. Note: PPTX output is designed for editing —
  │     minor formatting adjustments may be needed."
  │
  ├─ "changes" → re-enter flow at routed step (standard behavior)
  │
  └─ "abort" → clean up .drafts/ including .json. No artifacts saved.
```

### Flow B.2: Template and Branding (FR-09, FR-11)

```
BRANDING RESOLUTION ORDER (evaluated once at PPTX generation):

  1. --template flag provided?
  │   YES → use template's masters, fonts, colors
  │         (--font and --accent-color still override within template)
  │   NO  → continue
  │
  2. presentation.pptx_template in config?
  │   YES → use that template path
  │   NO  → continue
  │
  3. --font / --accent-color flags?
  │   YES → apply specified values, blank presentation base
  │   NO  → continue
  │
  4. presentation.pptx_font / presentation.pptx_accent_color in config?
  │   YES → apply configured values
  │   NO  → continue
  │
  5. DEFAULTS: Calibri font, #2d5aa0 accent, standard layouts
```

Precedence: CLI flags > config values > hardcoded defaults. Template provides the base; font/color flags override within it.

---

## Flow Group C: 90-Second Fallback (#45)

### Flow C.1: Enhanced Progress Indicators (FR-12)

Progress output at each step transition:

```
[1/6] Assembling presentation outline... (Investor Pitch, audience: investor)
      ✓ Assemble complete: 9-slide outline, PO contributing

  ── USER APPROVAL ──

[2/6] Validating source artifacts...
      ✓ Content Gate passed: 2 required found, 1 enhancing found, 1 enhancing missing

[3/6] Drafting slide content... (3 roles contributing: PO, Developer, Data Analyst)
      ✓ Draft complete: PO contributed 4 slides, Developer 3 slides, Data Analyst 2 slides

[4/6] Composing final presentation... (applying narrative arc + editorial passes)
      ✓ Compose complete: 9 slides assembled, 1 slide merged, emphasis reordered

[5/6] Reviewing draft... (Technical Writer + UX Designer)
      ✓ Review complete: 0 MUST-FIX, 2 SUGGESTION items

[6/6] Ready for your review.
```

Each line shows: step number, action description, contextual detail. Completion shows: what happened, quantified.

### Flow C.2: Light Mode Activation (FR-13)

```
User: "present roadmap"
  │
  ▼
LIGHT MODE EVALUATION (before Step 3):
  │
  ├─ presentation.light_mode = "never" OR --full flag?
  │   → FULL MODE. All roles dispatched. Both reviewers in Step 5.
  │
  ├─ presentation.light_mode = "always"?
  │   → LIGHT MODE. Skip below evaluation.
  │
  └─ presentation.light_mode = "auto" (default)?
      │
      ├─ Count contributing roles from outline
      │   ├─ 3 or fewer → LIGHT MODE activates
      │   └─ 4 or more  → FULL MODE
      │
      ▼
  LIGHT MODE EFFECTS:

  Step 3 (Draft):
    Only required roles dispatched. Optional role slots skipped.
    Output: "[3/6] Drafting slide content... (light mode: 2 roles contributing)"

  Step 5 (Review Gate):
    Single reviewer: Technical Writer only. UX Designer skipped.
    Output: "[5/6] Reviewing draft... (light mode: Technical Writer only)"

  Step 6 (User Review):
    No change. User sees full output + note:
    "Generated in light mode. Use `present --full` for maximum collaboration depth."
```

### Flow C.3: Threshold and Degradation (FR-14, FR-15)

```
THRESHOLD RESOLUTION:
  1. presentation.thresholds.{type} exists? → use per-type value
  2. presentation.thresholds_default exists? → use global override
  3. Neither? → 90 seconds
  4. Threshold = 0? → no threshold (unlimited)

DEGRADATION FLOW:

  Flow begins. Timer starts.
  │
  ├─ At 75% of threshold (e.g., 67.5s of 90s):
  │   ▼
  │   ⚠ "Approaching generation target (67s / 90s).
  │      Remaining steps will use simplified processing."
  │
  │   Effects activated:
  │     • Step 5 reduces to single reviewer (TW only)
  │     • Step 5 limits scope to MUST-FIX only (no SUGGESTION items)
  │
  ├─ At 100% of threshold:
  │   ▼
  │   ⚠ "Generation target exceeded (90s / 90s).
  │      Completing with simplified review."
  │
  │   (effects already active from 75% trigger)
  │
  └─ At Step 6 (if threshold was exceeded):
      ▼
      User Review includes notice:
      "Generation exceeded the 90s target (112s actual).
       Consider using `present --light` or adjusting
       `presentation.thresholds` for this type."

  IMPORTANT: Degradation never skips steps. Light means reduced depth.
  Step 5 still runs — with fewer reviewers and narrower scope.
  The user always gets a reviewed presentation.
```

### Flow C.4: Light Mode + Threshold Interaction

```
                    │ Light Mode OFF        │ Light Mode ON
────────────────────┼───────────────────────┼──────────────────────
Under threshold     │ Full: all roles,      │ Light: fewer roles,
                    │ both reviewers        │ single reviewer
────────────────────┼───────────────────────┼──────────────────────
75% threshold hit   │ Degrades to: all      │ Already light.
                    │ roles, single reviewer│ No further reduction.
                    │ MUST-FIX only         │ MUST-FIX only added.
────────────────────┼───────────────────────┼──────────────────────
100% threshold hit  │ Same as 75% (already  │ Same. Notice in
                    │ degraded). Notice in  │ Step 6 output.
                    │ Step 6 output.        │
```

Light mode and threshold degradation are independent controls that converge on the same levers (reviewer count, review scope). When both are active, the effect is the same as light mode alone plus MUST-FIX-only review scope.

---

## Flow Group D: Narrative Intelligence (#46)

Narrative intelligence inserts into Step 4 (Compose) as four sequential editorial passes. These run AFTER the Composer assembles drafts and BEFORE it writes `composed-draft.md`.

### Flow D.1: Compose Step with Narrative Intelligence

```
[4/6] Compose
  │
  ▼
  1. ASSEMBLE: Read all draft files from .drafts/
     Merge into slide sequence per outline
  │
  ▼
  2. EDITORIAL PASS 1: Emphasis Selection (FR-16)
  │  ├─ Evaluate each slide's impact signals:
  │  │   • Contains quantitative data? (weight varies by type)
  │  │   • User-facing vs internal change?
  │  │   • Breadth of usage / stakeholder impact?
  │  │   • Complexity or trade-off resolved?
  │  │   • Novelty (new capability vs incremental improvement)?
  │  ├─ Apply type-specific weight modifiers from narrative-patterns.md
  │  ├─ Rank slides by weighted impact score
  │  ├─ Reorder: highest-impact feature leads (within unconstrained groups)
  │  ├─ LOCKED slides (PO-sequenced, structural like Now/Next/Later) untouched
  │  └─ narrative_reorder: false? → skip this pass entirely
  │
  ▼
  3. EDITORIAL PASS 2: Information Cutting (FR-17)
  │  ├─ Evaluate each slide against cutting heuristics:
  │  │   • Slide contains only obvious info (no trade-offs, no data, no decisions)?
  │  │   • Slide duplicates content from an adjacent slide?
  │  │   • Slide has fewer than 2 substantive bullets?
  │  ├─ Flagged slides → merge key points into adjacent slides
  │  ├─ Record cuts: "{Slide title} merged into {target} — reason: {rationale}"
  │  ├─ Cuts list preserved for Step 6 "Narrative Cuts" section
  │  └─ narrative_cutting: false? → skip this pass entirely
  │
  ▼
  4. EDITORIAL PASS 3: Audience-Specific Framing (FR-18)
  │  ├─ Load framing rules from narrative-patterns.md "Audience Framing Rules"
  │  ├─ For each content slide, apply audience lens:
  │  │   investor  → lead with market opportunity / traction impact
  │  │   executive → lead with business value / cost impact
  │  │   technical → lead with architecture decisions / trade-offs
  │  │   client-facing → lead with user benefit / outcome
  │  │   casual    → conversational tone, minimal jargon
  │  ├─ Restructure slide arguments (not just vocabulary swaps)
  │  └─ This pass always runs (no config toggle — audience is always relevant)
  │
  ▼
  5. EDITORIAL PASS 4: Narrative Tension (FR-19)
  │  ├─ Slide count >= 6? → apply tension arc
  │  │   ├─ Identify the single most important insight/decision/result
  │  │   ├─ Position it at 60-70% point of presentation (the climax)
  │  │   ├─ Preceding slides build toward it (escalating stakes)
  │  │   ├─ Following slides validate and resolve (evidence, next steps)
  │  │   └─ Type-specific tension patterns:
  │  │       Feature Pitch: problem severity → failed alternatives → solution (climax) → evidence → ask
  │  │       Sprint Review: goals → challenges → key achievement (climax) → quality validation → next steps
  │  │       Investor Pitch: problem → market size → traction proof (climax) → team → the ask
  │  │       Roadmap: strategic context → current progress → vision item (climax) → timeline → CTA
  │  │       Product Demo: before state → incremental demos → hero feature (climax) → impact → CTA
  │  │       Onboarding: why it exists → landscape → key decision (climax) → pathways → first tasks
  │  │       Retro Summary: celebrations → deepest lesson (climax) → commitments → trends
  │  │       Stakeholder Update: status → blockers → resolution/breakthrough (climax) → next steps
  │  │       Technical Deep-Dive: problem space → approaches considered → chosen approach (climax) → validation → implications
  │  │
  │  ├─ Slide count < 6? → skip (too few slides for meaningful arc)
  │  └─ Tension does not override locked slide positions
  │
  ▼
  6. FORMAT + FINALIZE
     Apply output format, write transitions, enforce density,
     insert citations, add opening/closing slides
     Write composed-draft.md (+ .json if format=pptx)
```

### Flow D.2: Review Gate with Narrative Quality Criteria (FR-20)

```
[5/6] Review Gate

  Technical Writer reviews with EXPANDED criteria:
    Standard: clarity, jargon for audience, scannable titles, single message per slide
    NEW: "Does each slide earn its place? Could any slide be cut
          without losing the argument?"

  UX Designer reviews with EXPANDED criteria:
    Standard: density, hierarchy, visual story, readability
    NEW: "Does the presentation build toward a clear climax?
          Is the strongest content positioned for maximum impact?"

  Classification unchanged: MUST-FIX (blocks) or SUGGESTION (noted)
  Narrative quality issues can be either classification:
    • Missing climax positioning → MUST-FIX
    • Weak emphasis ordering → SUGGESTION
    • Slide that doesn't earn its place → MUST-FIX (Composer cuts it)
```

### Flow D.3: User Review with Narrative Transparency

```
[6/6] User Review

  Standard output:
    1. Complete presentation (PRESENTATION START / END)
    2. Collaboration Summary table
    3. Warnings

  NEW sections (when narrative intelligence was active):

    4. Narrative Cuts (if any slides were merged/removed):
       "Narrative Cuts:
        • 'Sprint Velocity' merged into 'Quality Metrics' —
          reason: contained only a single data point already cited in Quality Metrics
        • 'Team Updates' merged into 'Sprint Summary' —
          reason: no trade-offs or decisions, purely informational"

    5. Emphasis Order (if reordering occurred):
       "Slide order adjusted for emphasis:
        • Feature B promoted ahead of Feature A (broader user impact)
        • Metrics slide moved to support climax positioning"

    6. Suggestions from Review Gate (existing)

    7. Options (enhanced):
       • approve — save artifact
       • changes — describe what to adjust
       • restore {slide title} — reinsert a cut slide
       • no reorder — re-compose with original slide order
       • abort — discard
```

---

## Combined Journey: End-to-End Investor Pitch with PPTX Output

This journey combines all four feature groups into a single realistic scenario.

```
Priya (Startup CTO): "present investor pitch --format pptx --audience investor"
  │
  ▼
TYPE DETECTION: Investor Pitch (keyword match)
FORMAT: pptx (stored for Step 4 + post-approval)
AUDIENCE: investor
  │
  ▼
LIGHT MODE EVAL: Investor Pitch dispatches PO, Data Analyst, Developer, Architect
  → 4 roles → FULL MODE (auto threshold)
THRESHOLD: presentation.thresholds.investor-pitch? → not set → default 90s
TIMER: starts
  │
  ▼
[1/6] Assembling presentation outline... (Investor Pitch, audience: investor)
  PO produces 9-slide Traction-Opportunity-Ask outline
  ✓ Assemble complete: 9-slide outline
  │
  ── USER APPROVES OUTLINE ──
  │
  ▼
[2/6] Validating source artifacts...
  Required: PRD ✓, traction metrics ✓
  Enhancing: competitive analysis ✗ (missing), financial projections ✓
  ✓ Content Gate passed: 2/2 required, 1/2 enhancing

[3/6] Drafting slide content... (4 roles contributing)
  ✓ Draft complete: PO 4 slides, Developer 2 slides, Data Analyst 2 slides, Architect 1 slide

[4/6] Composing final presentation... (applying narrative arc + editorial passes)
  │ PASS 1 (Emphasis): Traction Proof promoted ahead of Business Model (strongest signal)
  │ PASS 2 (Cutting): no slides cut (all earn their place in investor context)
  │ PASS 3 (Framing): all slides framed for investor lens (market/traction lead)
  │ PASS 4 (Tension): Traction Proof positioned as climax at slide 6/9 (67%)
  │ JSON intermediate written (format=pptx)
  ✓ Compose complete: 9 slides, 1 reorder, 0 cuts, investor framing applied

  ⚠ Approaching generation target (68s / 90s).
    Remaining steps will use simplified processing.

[5/6] Reviewing draft... (Technical Writer only — degraded for time)
  MUST-FIX only (no suggestions — degraded scope)
  ✓ Review complete: 0 MUST-FIX found

[6/6] Ready for your review.
  --- PRESENTATION START ---
  [9-slide investor pitch with traction-opportunity-ask arc]
  --- PRESENTATION END ---

  Collaboration Summary: PO 4 slides, Developer 2, Data Analyst 2, Architect 1
  Emphasis Order: Traction Proof promoted ahead of Business Model
  Warnings: competitive analysis missing (slide 4 uses [TBD] for competitive data)
  Notice: Generation exceeded the 90s target (94s). Consider adjusting thresholds.

  Options: approve | changes | restore | no reorder | abort
  │
  ── Priya: "approve" ──
  │
  ▼
PPTX GENERATION:
  python-pptx installed? YES
  Invoking: generate_pptx.py --input composed-draft.json --output investor-pitch-2026-04-04.pptx
  9 slides mapped:
    Slide 1 (title) → Title Slide layout
    Slides 2-8 (content/metrics) → Title and Content layout
    Slide 9 (CTA) → Title and Content with numbered list
  Font: Calibri (default), Accent: #2d5aa0 (default)

  "Presentation saved to .delivery/artifacts/presentations/investor-pitch-2026-04-04.pptx
   9 slides generated. Note: PPTX output is designed for editing —
   minor formatting adjustments may be needed."

  .drafts/ cleaned up. Done.
```

---

## Summary of Flow Deltas by Step

| Step | Group A (Types) | Group B (PPTX) | Group C (Fallback) | Group D (Narrative) |
|------|----------------|----------------|-------------------|-------------------|
| Pre-flow | 5 new type detections + keywords | format=pptx stored | light mode eval, timer starts | -- |
| 1 Assemble | Type-specific frameworks + slide sequences | -- | -- | -- |
| 2 Content Gate | Type-specific required/enhancing artifacts | -- | -- | -- |
| 3 Draft | Type-specific role dispatch | -- | Light mode: fewer roles | -- |
| 4 Compose | Sensitivity filter (Retro only) | +JSON intermediate output | -- | 4 editorial passes inserted |
| 5 Review Gate | -- | -- | Degraded: single reviewer, MUST-FIX only | Expanded review criteria |
| 6 User Review | Retro disclaimer | -- | Threshold notice | Narrative Cuts, Emphasis Order, restore command |
| Post-approval | -- | PPTX script invocation | -- | -- |

---

*"The mirror shows many things. These flows show what the presentation skill could become -- and it is a future beautiful and terrible as the dawn. Not all who wander through nine presentation types are lost; some are simply composing investor pitches."*

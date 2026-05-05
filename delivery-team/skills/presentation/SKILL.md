---
name: presentation
description: Presentation Composer — assembles team contributions into cohesive presentations through a 6-step collaboration flow (Assemble, Content Gate, Draft, Compose, Review Gate, User Review). Supports 9 types: Sprint Review, Feature Pitch, Stakeholder Update, Technical Deep-Dive, Investor Pitch, Roadmap, Product Demo, Onboarding, Retrospective Summary. Auto-detects type from user input or pipeline context. Produces structured markdown, Marp, paste-ready, or PPTX output. Triggers on phrases like "create presentation", "sprint review", "sprint demo", "what we delivered", "pitch", "propose", "sell this feature", "why we should build", "status update", "executive update", "progress report", "technical presentation", "architecture overview", "deep dive", "how it works", "present", "slide deck", "stakeholder update", "investor pitch", "fundraising deck", "pitch to investors", "roadmap", "quarterly plan", "what's coming next", "product demo", "feature demo", "show what we built", "demo for publisher", "onboarding", "project handoff", "team orientation", "getting started", "retro summary", "retrospective presentation", "what we learned".
license: Apache License 2.0 - See repository LICENSE file
model_awareness: opus-4-7-frontmatter-only
last_audited: 2026-04-22
pattern_library_version: 4-7-1
tier: B
allowed-tools: [Read, Edit, Write, Bash, Skill, ToolSearch]
---

# Presentation Composer

## Design Principle: Compose, Don't Create

This skill is a **mini-orchestrator**, not a content creator. The Composer assembles contributions from delivery team roles (PO, Data Analyst, Developer, Architect, QA) into a cohesive presentation. Each contributing role loads its own skill to produce domain-accurate content. The Composer shapes tone, flow, density, and format — the team creates the content.

**Context isolation**: Contributing roles run as sub-agents with only their relevant artifacts. The Composer reads their draft outputs from disk. No role's full context leaks into another.

**Signal**: `SKILL_LOADED: presentation`

---

## Presentation Type Detection

Detect type from user request using keyword matching. If ambiguous, ask — never guess.

| Type | Keywords |
|------|----------|
| Sprint Review | "sprint review", "what we delivered", "sprint demo", "end of sprint" |
| Feature Pitch | "pitch", "propose", "sell this feature", "why we should build", "feature pitch" |
| Stakeholder Update | "status update", "executive update", "progress report", "stakeholder" |
| Technical Deep-Dive | "technical presentation", "architecture overview", "deep dive", "how it works" |
| Investor Pitch | "investor pitch", "fundraising deck", "pitch to investors" |
| Roadmap | "roadmap", "quarterly plan", "what's coming next" |
| Product Demo | "product demo", "feature demo", "show what we built", "demo for publisher" |
| Onboarding | "onboarding", "project handoff", "team orientation", "getting started" |
| Retrospective Summary | "retro summary", "retrospective presentation", "what we learned" |

### Pipeline Auto-Detection (when type not explicit)

| Current Stage | Default Type |
|---------------|-------------|
| Idea checkpoint | Feature Pitch |
| Design after DoD | Technical Deep-Dive |
| Plan after sprint planning | Stakeholder Update |
| UAT after acceptance | Sprint Review |
| UAT release | Stakeholder Update |
| UAT stage with `audience: investor` | Investor Pitch |
| Plan after roadmap/quarterly planning | Roadmap |
| Development after feature completion | Product Demo |
| Post-onboarding or handoff context | Onboarding |
| Post-retrospective | Retrospective Summary |

### Light Mode

Light mode reduces sub-agent dispatch for simpler presentation types, cutting generation time for straightforward decks.

**Activation** (config: `presentation.light_mode`, default: `"auto"`):

| Config Value | Behavior |
|-------------|----------|
| `auto` | Activate light mode when the type requires **3 or fewer contributing roles** in Step 3 |
| `always` | Activate light mode for all types |
| `never` | Disable light mode entirely |

**User override**: `present --full` forces full mode regardless of config. `present --light` forces light mode regardless of config.

**Light mode effects**:
- **Step 3 (Draft)**: Only required roles dispatched. Optional/enhancing role slots skipped.
- **Step 5 (Review Gate)**: Single reviewer (Technical Writer only). Full scope (all findings, not MUST-FIX only).

Light mode does NOT affect Steps 1, 2, 4, or 6. Step 4 (Compose) never degrades (per ADR-03).

### Threshold and Graceful Degradation

The flow tracks elapsed time from Step 1 start. At step transitions, the elapsed time is checked against the configured threshold.

**Threshold resolution** (first match wins):

1. `presentation.thresholds.{type-name}` -- per-type override (e.g., `presentation.thresholds.sprint-review: 120`)
2. `presentation.thresholds_default` -- global override
3. Neither set -- **90 seconds** (hardcoded default)
4. Value `0` -- no threshold (unlimited, no warnings)

**At 75% of threshold** (e.g., 67.5s for a 90s threshold):
- Display warning: `[WARN] Generation at 75% of threshold ({elapsed}s / {threshold}s). Reducing review depth.`
- **Degrade Step 5**: Reduce to single reviewer (TW only), MUST-FIX only scope. Optional reviewers skipped.
- Step 4 (Compose) is **never** degraded -- editorial passes always run fully (per ADR-03).

**At 100% of threshold**:
- Step 6 appends a notice: `[NOTICE] Generation exceeded threshold ({elapsed}s / {threshold}s). Consider using '--light' or adjusting 'presentation.thresholds' config.`

**Light mode + threshold interaction matrix**:

| Scenario | Step 3 Roles | Step 5 Reviewers | Step 5 Scope |
|----------|-------------|-----------------|-------------|
| Full, under threshold | All assigned | TW + UX | Full |
| Full, 75% hit | All assigned | TW only | MUST-FIX only |
| Light, under threshold | Required only | TW only | Full |
| Light, 75% hit | Required only | TW only | MUST-FIX only |

Light mode and threshold degradation are **independent controls that converge on the same levers**. Their effects are the union, not the sum. Reviewer count never drops below 1.

### GAME_DEV Vocabulary

When `project.type: GAME_DEV` in config, adapt vocabulary throughout all steps:
sprint -> milestone, features -> mechanics, UAT -> playtesting, modules -> systems, stories -> tasks, velocity -> throughput.

**Product Demo GAME_DEV variant**: When `project.type: GAME_DEV` and type is Product Demo, use "publisher milestone" vocabulary and structure the demo around gameplay mechanics rather than feature lists. Replace "feature demo" with "milestone demo" in slide titles.

### Onboarding Default Audience

When the presentation type is Onboarding and the audience mode is not explicitly set by the user, default to "technical" (the most common onboarding scenario). This overrides the global `presentation.default_audience` config for this type only.

### Retrospective Summary Sensitivity and Disclaimer

**Disclaimer** (always displayed for Retrospective Summary, regardless of audience):

> "This presentation summarizes team retrospective themes. Individual feedback has been anonymized and generalized."

**Sensitivity filter** (audience-dependent):
- **"executive" or "client-facing" audience**: Apply sensitivity filter — generalize individual feedback to team patterns, omit names from specific feedback, frame challenges as process improvements not personnel issues. See `narrative-patterns.md` for detailed rules.
- **"technical" or "casual" audience**: Sensitivity filter does NOT apply — full detail from retrospective notes is preserved (team-internal audiences).

---

## 6-Step Collaboration Flow

### Step 1: Assemble (PO)

**Begin**: `[1/6] Assembling presentation outline... (type: {detected type}, audience: {audience mode})`

Spawn a sub-agent with `delivery-team:product-delivery` (Product Owner role). Provide:
- User request (type, audience, format)
- Config context from `.delivery/config.yml`
- Pipeline state from `.delivery/state/` (if exists)

The PO produces a **Presentation Outline**:

| Column | Content |
|--------|---------|
| # | Slide number |
| Slide Title | Descriptive title |
| Content Owner | Role(s) responsible |
| Source Artifacts | File paths to read |

**Narrative adaptation**: The PO checks for problem signals in source data:
- Completion <80%: lead with "what we learned"
- Unresolved defects >5: quality slide before metrics
- Missed sprint goal: reframe around adjusted scope + rationale

Show adaptation status to user. User can say "no adaptation" to override.

Present outline to user. Wait for approval before proceeding.

**Complete**: `Outline approved: {N} slides, {M} roles contributing`

### Step 2: Content Gate (Automated)

**Begin**: `[2/6] Validating source artifacts... ({N} required, {M} enhancing to check)`

Validate required artifacts exist per type:

| Type | Required | Enhancing (optional) |
|------|----------|---------------------|
| Sprint Review | Sprint plan, UAT report/completion data | FKCs, metrics, retrospective, defect log |
| Feature Pitch | Idea brief or PRD | Architecture overview, competitive analysis |
| Stakeholder Update | Pipeline state, sprint plan/progress | Risk register, metrics, retrospective |
| Technical Deep-Dive | At least 1 architecture doc or ADR | Design decisions, code examples |
| Investor Pitch | Idea brief or PRD, traction/metrics data | Competitive analysis, financial projections, team bios |
| Roadmap | Sprint plan or backlog, pipeline state | Architecture roadmap, risk register, resource allocation |
| Product Demo | At least 1 feature artifact (FKC, implementation doc, or UAT report) | Screenshots, user feedback, metrics |
| Onboarding | Architecture overview or system documentation, at least 1 ADR or design decision doc | Team topology, dev environment setup, glossary |
| Retrospective Summary | Retrospective notes or action items | Velocity trends, defect data, previous retro actions |

**Gate rules**:
- Missing required artifact: **STOP**. List what is missing, where it should be, how to create it.
- Empty/placeholder artifact: **WARN** + ask user to confirm proceeding.
- Stale artifact (>`staleness_warning_days`, default 7): **WARN** but proceed with notice.

On PASS, show what was found (required + enhancing) and any warnings.

**Complete**: `Content gate passed: {N} required found, {M} enhancing found, {W} warnings`

### Step 3: Draft (Parallel — 5 Roles)

**Begin**: `[3/6] Drafting slide content... ({N} roles contributing{, light mode if active})`

In **light mode**: only required roles are dispatched. Optional/enhancing role slots are skipped. The role count in the progress indicator reflects the reduced set.

Dispatch sub-agents **in parallel** based on the outline's role assignments. Only dispatch roles that have assigned slides.

| Sub-agent | Skill | Contributes |
|-----------|-------|-------------|
| Product Owner | `delivery-team:product-delivery` | Narrative slides (goals, priorities, next steps) |
| Data Analyst | `delivery-team:product-delivery` | Metric slides (velocity, completion, trends) |
| Developer | `delivery-team:developer` | Feature slides (implementation highlights) |
| Architect | `delivery-team:architect` | Architecture slides (decisions, diagrams) |
| QA Engineer | `delivery-team:quality` | Quality slides (test results, defect data) |

Each sub-agent receives:
- Its assigned slide numbers and titles from the outline
- Paths to its relevant source artifacts only
- Presentation type, audience mode, and content rules

Each sub-agent writes output to: `.delivery/artifacts/presentations/.drafts/{role}-slides.md`

**Content rules for all sub-agents**:
- Every data point must cite its source artifact
- Missing data: use `[TBD]` — never fabricate
- Stay within assigned slide scope
- Write at the detail level appropriate for audience

Show the user which roles contribute to which slides (progress indicator), then proceed silently.

**Complete**: `Draft complete: {role names} contributed {N} slides`

### Step 4: Compose (Composer — this skill)

**Begin**: `[4/6] Composing final presentation... ({N} editorial passes enabled)`

Step 4 **never degrades** -- all enabled editorial passes run at full depth regardless of light mode or threshold status (per ADR-03).

Read all draft files from `.delivery/artifacts/presentations/.drafts/`. Assemble into final deck:

1. **Load references**: Always load `slide-structure.md` and `narrative-patterns.md`. Load `marp-templates.md` if format is Marp. Load `data-visualization.md` if metric or architecture slides exist.
2. **Apply narrative arc** from `narrative-patterns.md` for the detected type
3. **Add opening slide** (title, date, project context from config) and **closing slide** (next steps, CTA)
4. **Normalize tone** across all role contributions for the target audience
5. **Enforce density**: max 5-7 bullets per slide, 1 key message per slide, max 2 visualizations
6. **Write transitions** between slides for narrative flow
7. **Run editorial passes** (see below)
8. **Apply output format** (structured markdown, Marp, or paste-ready conventions)
9. **Insert citations** per slide in the format appropriate for the output mode
10. **Add speaker notes** only if requested (off by default)

#### Editorial Passes (Narrative Intelligence)

After assembling drafts and before format finalization, run four sequential editorial passes. Each pass transforms the slide set; the next pass operates on the transformed output. **Order is strict** (per architecture ADR-02): Emphasis > Cutting > Framing > Tension. No parallelism — each pass depends on the previous pass's output.

Each pass checks its config key before executing. When a pass's config key is `false`, that pass is skipped entirely.

**Pass 1: Emphasis Selection** *(config: `presentation.narrative.emphasis`, default: true)*

Reorder slides so the most impactful content leads. This replaces chronological ordering with impact-ranked ordering.

**Impact signal taxonomy** (evaluate each slide):
- **Data-backed results first**: Slides with quantified outcomes (metrics, percentages, before/after) rank highest
- **External validation before internal metrics**: Customer feedback, market data, or third-party benchmarks outrank internal velocity/completion stats
- **User impact over technical achievement**: Features affecting end-users rank above infrastructure improvements
- **Breadth of usage**: Features affecting many users rank above niche improvements
- **Complexity resolved**: Slides demonstrating resolution of significant technical challenges rank above routine work

**Rules**:
- Rank each slide by impact signals. Reorder the slide sequence so highest-impact slides appear first (after any structural opening slides).
- Structural slides (Title, Opening, CTA, Next Steps) are **position-locked** — they do not move.
- When two slides have equal impact, preserve their original relative order.
- Output: `emphasis_log` — a list of reorder actions: `"{Slide title}" moved from position {N} to position {M} — reason: {signal}"`

User override: When the user says `no reorder` or `keep chronological`, or when `presentation.narrative.emphasis` is `false`, skip this pass entirely and preserve original outline order.

**Pass 2: Information Cutting** *(config: `presentation.narrative.cutting`, default: true)*

Remove or merge slides that do not earn their place. A presentation with fewer, stronger slides beats one with comprehensive but diluted content.

**Cutting heuristics**:
- **No data + no decision = cut candidate**: If a slide contains no quantified data AND no decision/trade-off/recommendation, it is a cut candidate
- **Confidence threshold**: Rate each slide's contribution to the overall argument on a 1-5 scale. Slides scoring < 3 are cut candidates
- **Obvious information**: Slides restating what the audience already knows (e.g., "We use Git for version control") are cut candidates
- **Duplicate emphasis**: If two slides make the same point, merge into the stronger one

**Rules**:
- Never cut below the minimum slide count for the presentation type (see `slide-structure.md` for minimums per type)
- When cutting, merge the slide's key points into the nearest thematically related surviving slide — do not discard content silently
- Structural slides (Title, Opening, CTA, Next Steps) are **never cut**
- Output: `cuts_log` — a list of merge actions: `"{Slide title} merged into {target slide} — reason: {rationale}"`
- The `cuts_log` is displayed in Step 6 (User Review) as a **Narrative Cuts** section so the user can review what was removed

User override: When `presentation.narrative.cutting` is `false`, skip this pass entirely — all draft slides are preserved. The user can also say `restore {slide title}` to reinsert a specific cut slide.

**Pass 3: Audience-Specific Framing** *(config: `presentation.narrative.framing`, default: true)*

Beyond vocabulary swaps (handled by the Jargon Translation Table), this pass restructures the *argument* within each slide based on what the audience values.

**Framing rules by audience type** (detailed rules in `narrative-patterns.md` > Audience Framing Rules):
- **Investor**: Lead each slide with market opportunity or traction impact. Frame features as competitive advantages. Quantify everything in business terms (revenue, growth, market share). Minimize technical implementation details.
- **Executive**: Lead each slide with business value or cost impact. Use ROI framing — what did this cost, what did it produce? Show trend lines over absolute numbers. Decision-ready language: "recommend", "propose", "request approval".
- **Technical**: Lead each slide with architecture decisions, patterns, and trade-offs. Show the "why" behind choices. Include system names, version numbers, and technical context. Acceptable to go deep — this audience values precision.
- **Customer/Client-facing**: Lead with outcomes the customer requested or benefits they experience. Frame in terms of their workflow, not our process. Omit all internal process references.
- **Casual**: Conversational framing. Lead with team wins and shared accomplishments. First-person plural throughout.

**Rules**:
- Framing rewrites slide `body` content in-place. It does not add or remove slides.
- Framing applies to all surviving slides (post-cutting).
- When audience mode is not set, use `presentation.default_audience` config (default: "technical") — technical framing is the identity transform (no rewrite needed).

**Pass 4: Narrative Tension** *(config: `presentation.narrative.tension`, default: true)*

Build the presentation toward a key insight. The strongest content should not appear first (that is emphasis) or last (that is anticlimax) — it should land at the 60-70% point, creating a narrative arc.

**Tension patterns** (type-specific patterns in `narrative-patterns.md` > Narrative Tension Patterns):
- **Problem-Solution-Result**: Build tension around the problem, reveal the solution as the climax
- **Before-After**: Build tension around the limitations, reveal the transformation as the climax
- **Tension-Resolution**: Build tension through challenges/trade-offs, reveal the key decision as the climax

**Rules**:
- Identify the single most important insight, decision, or result across all slides — this is the **climax slide**
- Position the climax slide at the 60-70% point of the presentation (e.g., slide 7 of 10)
- **Minimum threshold**: If the presentation has fewer than 6 slides, skip this pass — tension arcs need runway
- **Position-locked slides** are respected: PO-sequenced slides, structural slides (Title, CTA), and framework-locked positions (e.g., Now/Next/Later in Roadmaps) do not move
- Only reorder slides within **unconstrained groups** (slides between locked positions)
- Output: tension arc description appended to the emphasis log: `"Climax: {slide title} positioned at {N}/{total} ({percentage}%)"`

Write composed draft to `.delivery/artifacts/presentations/.drafts/composed-draft.md`.

**PPTX JSON intermediate** (when `format=pptx`): In addition to `composed-draft.md`, write a parallel `composed-draft.json` containing the structured slide data per the architecture JSON schema (slides array with number, title, layout, body, table, speaker_notes, citations, mermaid; metadata object). The JSON is consumed by `scripts/generate_pptx.py` after user approval in Step 6. The markdown is the human-reviewable artifact for Steps 5-6. Both files are cleaned up on approve/abort.

**Complete**: `Compose complete: {N} slides, {M} editorial passes applied, {K} slides cut`

### Step 5: Review Gate (TW + UX)

**Begin**: `[5/6] Reviewing draft... ({reviewer names}, {scope: full | MUST-FIX only})`

**Degradation behavior**:
- **Full mode, under threshold**: 2 reviewers (TW + UX), full scope.
- **Full mode, 75% threshold hit**: 1 reviewer (TW only), MUST-FIX only scope.
- **Light mode, under threshold**: 1 reviewer (TW only), full scope.
- **Light mode, 75% threshold hit**: 1 reviewer (TW only), MUST-FIX only scope.

Dispatch two reviewer sub-agents **in parallel**:

| Reviewer | Skill | Focus |
|----------|-------|-------|
| Technical Writer | `delivery-team:operations` | Clarity, jargon for audience, scannable titles, single message per slide, narrative necessity |
| UX Designer | `delivery-team:ui` | Density, hierarchy, visual story, readability when projected, narrative arc |

**Narrative quality criteria** (added to each reviewer's evaluation scope):
- **TW criterion**: "Does each slide earn its place? Could any slide be cut without losing the argument?" — validates information cutting was effective
- **UX criterion**: "Does the presentation build toward a clear climax? Is the strongest content positioned for maximum impact?" — validates narrative tension arc

Each reviewer reads `composed-draft.md` and returns findings as:
- **MUST-FIX**: Blocks user review. Composer fixes these automatically before Step 6 (including narrative quality MUST-FIX issues — same auto-fix behavior as formatting issues).
- **SUGGESTION**: Included as notes for user awareness.

Show review summary to user (issues found, what was fixed, suggestions preserved).

**Complete**: `Review complete: {N} MUST-FIX resolved, {M} suggestions preserved`

### Step 6: User Review

**Begin**: `[6/6] Ready for your review.`

If threshold was exceeded (100%), append to the presentation output:

> `[NOTICE] Generation exceeded threshold ({elapsed}s / {threshold}s). Consider using '--light' or adjusting 'presentation.thresholds' config.`

Present to the user:
1. The complete presentation between `--- PRESENTATION START ---` and `--- PRESENTATION END ---`
2. A **Collaboration Summary** table: role | slides contributed | artifacts consumed
3. **Narrative Cuts** (if any): list of slides merged/removed by the cutting pass, with rationale from `cuts_log`. Enables user to `restore {slide title}` if needed.
4. **Emphasis Order** (if reordered): list of slide reorder actions from `emphasis_log`, showing impact-ranked ordering decisions.
5. Warnings (staleness, [TBD] count)
6. Suggestions from Review Gate
7. Options:
   - **approve** — save to `.delivery/artifacts/presentations/{type}-{date}.md` (or `.pptx` when format=pptx)
   - **changes** — describe what to adjust
   - **abort** — discard draft

#### PPTX Generation (when format=pptx)

On **approve**, if format is `pptx`, execute the PPTX generation step:

1. **Dependency check**: Verify `python-pptx` is installed. If not, fall back to structured-markdown with warning:
   > "PPTX output requires python-pptx. Install with: pip install python-pptx. Falling back to structured-markdown."
   Save the `.md` artifact instead and stop.

2. **Invoke script**:
   ```bash
   python delivery-team/skills/presentation/scripts/generate_pptx.py \
     --input .delivery/artifacts/presentations/.drafts/composed-draft.json \
     --output .delivery/artifacts/presentations/{type}-{date}.pptx \
     [--template {presentation.pptx_template or --template flag}] \
     [--font {presentation.pptx_font or --font flag}] \
     [--accent-color {presentation.pptx_accent_color or --accent-color flag}]
   ```

3. **Branding precedence** (evaluated once at generation):
   - CLI `--template` flag > config `presentation.pptx_template` > no template (blank presentation)
   - CLI `--font` flag > config `presentation.pptx_font` > default: Calibri
   - CLI `--accent-color` flag > config `presentation.pptx_accent_color` > default: #2d5aa0
   - Template provides the base; font/color flags override within it.

4. **Output**: Display to user:
   > "Presentation saved to .delivery/artifacts/presentations/{type}-{date}.pptx
   > {N} slides generated. Note: PPTX output is designed for editing -- minor formatting adjustments may be needed."

5. Clean up `.drafts/` directory (including `.json` intermediate).

**Change routing** (when user says "changes"):

| Feedback Type | Routes To | Example |
|---------------|----------|---------|
| Structural (add/remove/reorder slides) | Step 1 | "Add a demo slide after features" |
| Content (wrong data, different emphasis) | Step 3 | "Velocity should be in story points" |
| Formatting/tone (layout, wording) | Step 4 | "Make slide 3 more concise" |

Re-execute from the routed step forward, not from the beginning.

**On approve**: Save final presentation. Clean up `.drafts/` directory.
**On abort**: Clean up `.drafts/` directory. No artifacts saved.

---

## Output Format Specifications

### Structured Markdown (default)

```markdown
# [Type]: [Project] — [Context]

---

## Slide N: [Title]

[Content — bullets, tables, text]

> Generated from: artifact-1.md, artifact-2.md

---
```

Speaker notes (when enabled): `**Notes**: [talking points]` after citation.

### Marp

Load `references/marp-templates.md` for full syntax. Key conventions:
- Frontmatter: `marp: true`, `theme`, `paginate: true`, `header`, `footer`
- Slide separator: `---`
- Citations: `<!-- Generated from: artifact.md -->`
- Speaker notes: `<!-- notes: talking points -->`
- Theme from `presentation.marp_theme` config (default: "default")

### PPTX

Generated via `scripts/generate_pptx.py` from a JSON intermediate file. Requires `python-pptx` (`pip install python-pptx`).

- The Composer produces `composed-draft.json` alongside `composed-draft.md` during Step 4 when format=pptx
- After user approval in Step 6, the script converts the JSON to a `.pptx` file
- Layout mapping: `title` -> "Title Slide", all other layouts -> "Title and Content" (name-first, index-fallback)
- Tables, speaker notes, and Mermaid diagram placeholders are supported
- Branding via `--template`, `--font`, `--accent-color` (see Step 6 PPTX Generation)
- If `python-pptx` is not installed, falls back to structured-markdown with a warning

### Paste-Ready

```
=== SLIDE N: [Title] ===
Headline: [key message]
Body: [content]
Source: artifact-1.md, artifact-2.md
```

No markdown formatting. No frontmatter. Clean content blocks for corporate templates.

---

## Error Handling

| Error | Detection | Behavior |
|-------|-----------|----------|
| Missing config | `.delivery/config.yml` not found | STOP: "No delivery config found. Run setup wizard or create config." |
| Missing required artifacts | Content Gate: required paths do not exist | STOP: list missing artifacts, expected locations, creation instructions |
| Empty artifacts | File exists but 0 bytes or template-only | WARN + ask user to confirm. Affected slides use [TBD]. |
| Stale artifacts | Last modified > staleness threshold | WARN but proceed. Staleness notice on affected slides. |
| Unknown type | Type not in supported set | STOP: "Unsupported presentation type. Supported types: Sprint Review, Feature Pitch, Stakeholder Update, Technical Deep-Dive, Investor Pitch, Roadmap, Product Demo, Onboarding, Retrospective Summary." |
| No pipeline state | `.delivery/state/` empty or missing | WARN: proceed with artifacts only, [TBD] for progress data |
| Partial data | Role finds insufficient data for slides | Role outputs what it can with [TBD]. Composer flags in summary. |
| python-pptx missing | format=pptx but `import pptx` fails | WARN: "PPTX output requires python-pptx. Install with: pip install python-pptx. Falling back to structured-markdown." Save .md artifact instead. |
| PPTX template missing | `--template` or config `pptx_template` path does not exist | STOP: "Template file not found: {path}. Check the path in your config or --template flag." |
| Invalid JSON intermediate | `composed-draft.json` is malformed or missing `slides` array | STOP: "Invalid JSON intermediate. Re-run Step 4 (Compose) to regenerate." |

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
| `present --full` | Force full mode (disable light mode) regardless of config |
| `present --light` | Force light mode regardless of config or role count |
| `approve` | Accept presentation, save to artifacts |
| `changes` | Provide feedback, re-enter flow at appropriate step |
| `abort` | Discard draft, clean up |
| `no reorder` / `keep chronological` | Disable emphasis reordering, preserve original slide order |
| `restore {slide title}` | Reinsert a slide that was removed by the cutting pass |
| `regenerate` | Re-run full flow with current artifacts |

---

## References

| File | Loaded When | Purpose |
|------|------------|---------|
| `references/slide-structure.md` | Always | Slide types, density rules, sequencing, boundary conventions |
| `references/narrative-patterns.md` | Always | Per-type narrative arcs, adaptation rules, tone/vocabulary |
| `references/marp-templates.md` | Format is Marp | Marp syntax, directives, layouts, themes |
| `references/data-visualization.md` | Metric or architecture slides exist | Chart patterns, Mermaid diagrams, data accuracy rules |
| `scripts/generate_pptx.py` | Format is PPTX (post-approval) | Converts JSON intermediate to .pptx file via python-pptx |

---

## Config Integration

Read from `.delivery/config.yml` at start of Step 1. User's explicit request overrides config. Config overrides hardcoded defaults.

| Key | Type | Default | Purpose |
|-----|------|---------|---------|
| `presentation.default_format` | string | structured-markdown | Default output format (structured-markdown, marp, paste-ready, pptx) |
| `presentation.default_audience` | string | technical | Default audience mode |
| `presentation.speaker_notes` | boolean | false | Enable speaker notes by default |
| `presentation.save_to_artifacts` | boolean | true | Save approved output to artifacts dir |
| `presentation.marp_theme` | string | default | Marp theme (default, gaia, uncover) |
| `presentation.staleness_warning_days` | integer | 7 | Days before staleness warning |
| `presentation.vocabulary_overrides` | map | {} | Custom term replacements (term -> replacement) |
| `presentation.pptx_template` | string | "" | Path to .pptx template file for branding (slide masters, fonts, colors) |
| `presentation.pptx_font` | string | Calibri | Font family for PPTX output (overrides within template) |
| `presentation.pptx_accent_color` | string | #2d5aa0 | Hex accent color for PPTX output (overrides within template) |
| `presentation.light_mode` | string | auto | Light mode activation: auto (role count), always, never |
| `presentation.thresholds` | map | {} | Per-type threshold overrides in seconds (e.g., `sprint-review: 120`) |
| `presentation.thresholds_default` | integer | 90 | Global threshold override in seconds. 0 = unlimited. |
| `presentation.narrative.emphasis` | boolean | true | Enable/disable emphasis selection pass (slide reordering by impact) |
| `presentation.narrative.cutting` | boolean | true | Enable/disable information cutting pass (merge/remove low-value slides) |
| `presentation.narrative.framing` | boolean | true | Enable/disable audience-specific framing pass (argument restructuring) |
| `presentation.narrative.tension` | boolean | true | Enable/disable narrative tension pass (climax positioning) |

**Precedence**: explicit request > `presentation.*` config > hardcoded defaults.

**No config?** Skill works with all defaults. Config is optional.

# Sprint Plan: Presentation Skill — Sprint 1 (Core + Sprint Review)

**Pipeline**: FEATURE
**Date**: 2026-03-25
**Sprint Goal**: Deliver the presentation skill with full Sprint Review type support, validated through dogfooding against this repo's current sprint.

**Upstream Artifacts**:
- PRD v2.0: `.delivery/artifacts/02-refine/po/prd.md`
- UX Design: `.delivery/artifacts/03-design/ux-design.md`
- Architecture: `.delivery/artifacts/04-architecture.md`

**Dogfooding Strategy**: Build Sprint Review end-to-end first (PRD Phase 1). Other 3 types get structural placeholders in narrative-patterns.md but are not wired into the collaboration flow until Sprint 2. The dogfooding artifact is a sprint review presentation generated for the sprint that builds this skill.

---

## Stories

### Story 1: Create SKILL.md — Presentation Composer

**As a** delivery team member, **I want** a Presentation Composer skill that orchestrates multi-role collaboration through a 6-step gated flow, **so that** I can generate accurate, audience-adapted presentations from delivery artifacts without manual content assembly.

**Acceptance Criteria**:
- [ ] File created at `delivery-team/skills/presentation/SKILL.md`
- [ ] Frontmatter includes: name, description, triggers (keyword list for all 4 types), license
- [ ] Presentation Composer role defined with context isolation principle (Composer assembles, roles create content)
- [ ] Type detection section: keyword table for 4 types, pipeline stage auto-detection table (5 mappings), ambiguity rule (ask, never guess), GAME_DEV vocabulary flag
- [ ] 6-step collaboration flow fully specified:
  - Step 1 (Assemble): PO sub-agent, outline output contract (slide table with title/owner/source), narrative adaptation detection
  - Step 2 (Content Gate): per-type required artifact table, gate behavior (STOP on missing, WARN on stale/empty), error message format
  - Step 3 (Draft): role-to-slide mapping from outline, parallel Agent dispatch to 5 roles, content rules (cite sources, [TBD] for gaps, stay in scope), draft output path convention
  - Step 4 (Compose): read drafts from `.drafts/`, assemble per narrative arc, tone normalization, density enforcement (5-7 bullets, 1 key message), transitions, opening/closing slides
  - Step 5 (Review Gate): TW + UX reviewer dispatch, MUST-FIX vs SUGGESTION categorization, auto-fix MUST-FIX before Step 6
  - Step 6 (User Review): full presentation output, collaboration summary table (role/slides/artifacts), approve/changes/abort options, change routing logic (structural->Step 1, content->Step 3, format->Step 4)
- [ ] Output format specifications section: structured markdown conventions, Marp conventions, paste-ready conventions, citation format per mode, speaker notes syntax
- [ ] Error handling section: error state table covering all 7 error conditions from PRD Section 6
- [ ] User commands section: command table (approve, changes, abort, format, audience, notes, regenerate)
- [ ] References section: index of 4 reference files with loading rules (which files load when)
- [ ] Config integration section: 7 `presentation.*` keys consumed, precedence chain (explicit > config > defaults), default behavior when no config exists
- [ ] Progress communication: `[N/6]` status headers per UX design Section 1.4
- [ ] Total length under 300 lines (target: ~290)
- [ ] Uses plugin-dev:skill-development patterns

**Test Cases**:
- TC1: SKILL.md parses as valid markdown with no broken links or unclosed code blocks
- TC2: Every presentation type mentioned in PRD Section 4 (Sprint Review, Feature Pitch, Stakeholder Update, Technical Deep-Dive) appears in the type detection table
- TC3: Every error state from PRD Section 6 has a corresponding entry in the error handling section
- TC4: Every role from PRD Step 3 (PO, Data Analyst, Developer, Architect, QA) appears in Step 3 dispatch logic
- TC5: Line count is between 270 and 300
- TC6: All 4 reference files are listed in the References section with correct relative paths
- TC7: Run plugin-dev:skill-reviewer against the completed file — no blocking issues

---

### Story 2: Create slide-structure.md — Slide Composition Patterns

**As a** Presentation Composer, **I want** a reference for slide types, density rules, and sequencing patterns, **so that** every generated presentation follows consistent structural conventions regardless of content.

**Acceptance Criteria**:
- [ ] File created at `delivery-team/skills/presentation/references/slide-structure.md`
- [ ] Slide type catalog: 10 slide types (title, content, comparison, metric, timeline, table, diagram, image, section divider, closing) — each with: name, when to use, structural template, max content limits
- [ ] Sprint Review slide types fully specified with templates and examples
- [ ] Other 3 types: slide type applicability noted but detailed templates can be minimal
- [ ] Information density rules: 5-7 bullet limit, 1 key message rule, max 2 data visualizations, "if it needs scrolling it needs splitting"
- [ ] Slide sequencing patterns: opening sequence (context > agenda > content), closing sequence (summary > next steps > CTA), transition patterns
- [ ] Slide boundary conventions: separator format for each output mode (`---`, `===`, Marp `---`)
- [ ] Image placeholder conventions: `![description](path)` syntax, placement rules, alt-text guidelines
- [ ] Presentation length guidelines: type-to-length mapping (Sprint Review 8-15, Feature Pitch 6-10, Stakeholder Update 5-8, Technical Deep-Dive 8-20)
- [ ] Total length under 150 lines

**Test Cases**:
- TC1: Every slide type referenced in the UX design Section 3.2 appears in the catalog
- TC2: Sprint Review structural template can produce a valid 10-slide outline when applied to sample data
- TC3: Density rules are testable (specific numbers, not vague guidance)
- TC4: Line count is between 130 and 160

---

### Story 3: Create narrative-patterns.md — Storytelling Frameworks

**As a** Presentation Composer, **I want** per-type narrative arcs and adaptation rules, **so that** each presentation tells a coherent story that shifts appropriately when delivery data signals problems.

**Acceptance Criteria**:
- [ ] File created at `delivery-team/skills/presentation/references/narrative-patterns.md`
- [ ] Sprint Review narrative arc fully specified (~30 lines): slide sequence (goal recap > committed vs delivered > feature highlights > metrics > quality summary > risks > next sprint), slide-by-role assignment matrix, opening hook patterns
- [ ] Feature Pitch narrative arc specified (~25 lines): problem > solution > benefit > implementation > ask, audience adaptation (executive/technical/client-facing)
- [ ] Stakeholder Update narrative arc specified (~25 lines): exec summary > progress vs plan > risks > metrics > milestones > decisions needed, traffic-light conventions
- [ ] Technical Deep-Dive narrative arc specified (~25 lines): context/problem > options > decision > trade-offs > architecture diagram > migration path
- [ ] Narrative adaptation rules (~35 lines): completion <80% threshold, defects >5 threshold, missed sprint goal handling, detection rules (where to find signals in artifacts), user override mechanism
- [ ] Tone/vocabulary adaptation (~20 lines): 4 audience modes defined, jargon translation table (blocker > delay, spike > investigation, DoD > completion criteria, UAT > acceptance testing), GAME_DEV vocabulary swaps
- [ ] Audience detection heuristics (~20 lines): inference chain (explicit > config > type default), pipeline stage signals
- [ ] Total length under 180 lines

**Test Cases**:
- TC1: Sprint Review arc covers every slide type listed in PRD US-01 acceptance criteria
- TC2: Every narrative adaptation rule has a specific numeric threshold (not subjective)
- TC3: GAME_DEV vocabulary swaps cover at least: sprint/milestone, features/mechanics, UAT/playtesting, modules/systems
- TC4: Line count is between 160 and 190

---

### Story 4: Create marp-templates.md — Marp Syntax Reference

**As a** Presentation Composer, **I want** a Marp syntax reference with frontmatter, directives, layouts, and theme guidance, **so that** Marp output is valid, well-formatted, and renders correctly with marp-cli.

**Acceptance Criteria**:
- [ ] File created at `delivery-team/skills/presentation/references/marp-templates.md`
- [ ] Frontmatter reference (~25 lines): required directives (`marp: true`), optional directives (theme, paginate, header, footer, class, backgroundColor), per-type frontmatter templates
- [ ] Slide-level directives (~20 lines): `_class` (lead, invert), `_backgroundColor`, `_color`, section divider styling
- [ ] Layout patterns (~30 lines): two-column, three-column, image-beside-text, centered content — code examples for each
- [ ] Code and diagram blocks (~25 lines): syntax-highlighted code, Mermaid embedding (`\`\`\`mermaid`), diagram sizing, fallback for renderers without Mermaid
- [ ] Image handling (~20 lines): sizing `![w:500](path)`, backgrounds `![bg right](path)`, positioning, placeholder conventions
- [ ] Speaker notes (~15 lines): syntax `<!-- notes: text -->`, placement rules, content guidelines
- [ ] Theme guide (~15 lines): default, gaia, uncover — type-to-theme recommendation matrix
- [ ] Total length under 150 lines

**Test Cases**:
- TC1: Every Marp directive referenced in PRD Section 7.2 appears in the reference
- TC2: Code examples are valid Marp markdown (would render without syntax errors)
- TC3: Speaker notes syntax matches PRD US-06 format
- TC4: Line count is between 130 and 160

---

### Story 5: Create data-visualization.md — Metric Presentation Patterns

**As a** Data Analyst contributing to presentations, **I want** chart selection guidance, Mermaid diagram patterns, and metric highlight templates, **so that** data slides are clear, accurate, and appropriately formatted for slide projection.

**Acceptance Criteria**:
- [ ] File created at `delivery-team/skills/presentation/references/data-visualization.md`
- [ ] Chart type decision matrix (~30 lines): table, bar, line, pie — when to use each, decision tree (data type > comparison type > chart type), "when in doubt, use a table" rule
- [ ] Mermaid diagram patterns (~30 lines): flowchart, sequence, gantt, pie, mindmap — syntax examples sized for slides (not documentation)
- [ ] Metric highlight patterns (~30 lines): single big number (KPI spotlight), before/after comparison, target vs actual with delta, trend description, traffic light status — template for each
- [ ] Table formatting for slides (~25 lines): max 5 columns, max 8 rows, header row bold, alignment conventions, split-across-slides guidance, highlighting conventions
- [ ] Data accuracy rules (~25 lines): always cite source artifact, never extrapolate, `[TBD]` for missing values, time context required (sprint number/date range), meaningful precision (round appropriately)
- [ ] Sprint Review metric templates: velocity chart pattern, completion rate pattern, defect trend pattern
- [ ] Total length under 140 lines

**Test Cases**:
- TC1: Every chart type in PRD Section 8.4 appears in the decision matrix
- TC2: Mermaid syntax examples are valid (parseable by Mermaid renderer)
- TC3: Data accuracy rules are consistent with PRD FR-008 (no hallucination) and NFR-001 (every data point traceable)
- TC4: Line count is between 120 and 150

---

### Story 6: Register Presentation Skill in marketplace.json

**As a** plugin consumer, **I want** the presentation skill registered in the marketplace, **so that** it is discoverable and installable through standard plugin mechanisms.

**Acceptance Criteria**:
- [ ] `delivery-team/skills/presentation` path added to the `skills` array in the delivery-team plugin entry in `.claude-plugin/marketplace.json`
- [ ] delivery-team plugin description updated to reference 11 skills (was 10)
- [ ] File remains valid JSON after edits (`python -m json.tool` exits 0)
- [ ] No other plugin entries modified

**Test Cases**:
- TC1: `python -m json.tool .claude-plugin/marketplace.json` exits 0
- TC2: The skills array contains exactly one entry with path `./delivery-team/skills/presentation`
- TC3: Skill count in description matches actual count of skill directories under delivery-team/skills/
- TC4: Diff shows only the delivery-team entry changed

---

### Story 7: Update config-schema.md — Add presentation.* Keys

**As a** power user customizing presentation defaults, **I want** the config schema to document the 7 `presentation.*` keys with types, defaults, and valid values, **so that** I can configure the skill without reading the source.

**Acceptance Criteria**:
- [ ] Schema version bumped from 2.1 to 2.2 in `delivery-team/skills/delivery-flow/references/config-schema.md`
- [ ] 7 new keys added to schema table:
  - `presentation.default_format` (string, default: "structured-markdown", values: structured-markdown/marp/paste-ready)
  - `presentation.default_audience` (string, default: "technical", values: technical/executive/client-facing/casual)
  - `presentation.speaker_notes` (boolean, default: false)
  - `presentation.save_to_artifacts` (boolean, default: true)
  - `presentation.marp_theme` (string, default: "default", values: default/gaia/uncover)
  - `presentation.staleness_warning_days` (integer, default: 7, range: 1-30)
  - `presentation.vocabulary_overrides` (map[string,string], default: {})
- [ ] All 7 keys marked as optional (no wizard questions)
- [ ] Version history entry added for 2.2
- [ ] Config template snippet added showing all 7 keys with defaults
- [ ] Consuming skill documented as "presentation"
- [ ] Extension protocol compliance: all 7 checkpoints satisfied per config-schema.md protocol
- [ ] JSON schema regeneration command documented: `python delivery-team/scripts/generate-schema.py`

**Test Cases**:
- TC1: Every key in PRD Section 10 appears in the updated schema table
- TC2: Default values match between PRD Section 10, architecture Section 5, and config-schema.md
- TC3: Version history is sequential (2.1 -> 2.2, no gaps)
- TC4: Config template YAML is valid (`python -c "import yaml; yaml.safe_load(open(...))"`)

---

### Story 8: Update Documentation — CLAUDE.md, README.md, delivery-team/README.md

**As a** user or contributor reading documentation, **I want** all docs to reflect the presentation skill as the 11th delivery-team skill, **so that** documentation stays accurate and I can discover the skill through any entry point.

**Acceptance Criteria**:
- [ ] `CLAUDE.md`:
  - delivery-team description updated to "11 skills"
  - Presentation skill added to the delivery-team skills table with description
  - Available Plugins table: delivery-team row mentions 11 skills
- [ ] `README.md`:
  - delivery-team skill count updated to 11
  - Presentation skill listed in skill breakdown (if skills are enumerated)
  - Any repo structure tree updated to include `presentation/` under `delivery-team/skills/`
- [ ] `delivery-team/README.md`:
  - Skill count updated to 11
  - Presentation skill added to skills table with description: "Presentation Composer — multi-role collaboration for Sprint Review, Feature Pitch, Stakeholder Update, Technical Deep-Dive presentations"
  - References section (if present) lists the 4 reference files
- [ ] All numeric claims re-verified against filesystem at write time
- [ ] No docs mention "10 skills" for delivery-team after this story completes

**Test Cases**:
- TC1: `grep -r "10 skills" CLAUDE.md README.md delivery-team/README.md` returns zero matches
- TC2: `grep -r "11 skills" CLAUDE.md README.md delivery-team/README.md` returns at least 3 matches
- TC3: Every file path referencing the presentation skill directory exists on disk (post Story 1-5)
- TC4: Skill count claims match `ls delivery-team/skills/ | wc -l`

---

## Sprint Notes

**Ordering**: Stories 1-5 (skill files) are the core deliverables and can be developed in parallel, though Story 1 (SKILL.md) should be written first as it defines the contracts that Stories 2-5 implement. Story 6 (marketplace) and Story 7 (config schema) are independent of each other but should follow Story 1. Story 8 (docs) runs last since it references all other stories.

**Dependency chain**:
```
Story 1 (SKILL.md) ──> Story 6 (marketplace.json)
    │                  Story 7 (config-schema.md)
    ├──> Story 2 (slide-structure.md)
    ├──> Story 3 (narrative-patterns.md)
    ├──> Story 4 (marp-templates.md)
    └──> Story 5 (data-visualization.md)
                       Story 8 (docs) ──> depends on Stories 1-7 complete
```

**Plugin-dev skill usage** (per repo conventions):
- Stories 1-5: Load `plugin-dev:skill-development` before creating skill files
- After Story 1: Run `plugin-dev:skill-reviewer` against SKILL.md
- After all stories: Run `plugin-dev:plugin-validator` against the delivery-team plugin

**Dogfooding gate**: After all 8 stories are complete, generate a Sprint Review presentation for this sprint using the new skill. This is Phase 1 of the PRD dogfooding plan (Section 14). The presentation must:
1. Successfully pass the Content Gate using this sprint's artifacts
2. Produce contributions from at least 3 distinct roles
3. Render in structured markdown format without errors
4. Include source citations on every slide
5. Contain zero `[TBD]` placeholders (all data available from current artifacts)

**Lessons from previous sprints**:
- Verify all numeric claims against the filesystem at write time (not from memory)
- Config files must be pure YAML, not markdown with YAML frontmatter
- Light stages execute with reduced depth, never skipped
- Update docs as part of development (Story 8), not as follow-up

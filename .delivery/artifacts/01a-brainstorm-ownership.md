# Brainstorm: Presentation Skill Ownership

**Facilitator**: Product Owner (Gandalf)
**Date**: 2026-03-25
**Input**: Idea Brief (`01-idea-brief.md`)
**Participants**: Technical Writer, Product Owner, Data Analyst, UX Designer, Architect, Developer

---

## Team Perspectives

### 1. Technical Writer (Operations)

> "I already write release notes, user guides, runbooks. Presentations are just another output format for the same product knowledge I already work with."

**Strengths of this claim**:
- TW already transforms raw product knowledge into structured, audience-appropriate artifacts
- Existing reference files (documentation-standards.md, user-guides.md, runbook-templates.md) demonstrate content-shaping expertise
- Release notes and changelogs are close cousins to sprint review decks

**Weaknesses**:
- The operations skill already carries 3 roles and 12 reference files -- it is the heaviest skill by reference count
- TW's core competency is *documentation for reading and searching*, not *narrative for presenting and persuading* -- different information architecture
- Adding presentation types to TW would mean the operations skill handles DevOps + Release Management + Technical Writing + Presentations -- four distinct competencies behind one skill boundary

**Verdict**: Strong content skills, but the operations skill is already at capacity. Bolt-on risk is real.

---

### 2. Product Owner (Gandalf)

> "I create the source content -- PRDs, stories, roadmaps. I need sprint review decks, feature pitches, and stakeholder updates most often. Should I own this?"

**Strengths of this claim**:
- PO is the highest-frequency consumer of presentations (sprint reviews every sprint, roadmaps quarterly, pitches ad-hoc)
- PO already owns the artifacts that feed most presentation types (PRDs, backlog, sprint goals)
- Stakeholder communication is a core PO responsibility

**Weaknesses**:
- PO domain expertise is *what to present*, not *how to present it* -- slide structure, visual hierarchy, and narrative pacing are not PO competencies
- Product-delivery skill already has 3 roles (PO, Scrum Bag, Data Analyst) with 15 reference files
- Technical deep-dives and architecture presentations are outside PO scope entirely
- Conflating "primary consumer" with "owner" is a category error -- the PO is the primary consumer of quality reports too, but Quality owns QA

**Verdict**: PO should be the primary *requester*, not the owner. Ownership follows competency, not consumption.

---

### 3. Data Analyst (Product Delivery)

> "Stakeholder updates and sprint metrics decks are data-heavy. The data visualization reference file is squarely my domain."

**Strengths of this claim**:
- Data-heavy presentations (sprint metrics, velocity trends, funnel analysis) require analytical framing that the DA does best
- The proposed `data-visualization.md` reference overlaps directly with DA's existing analytics-patterns.md and dashboard-design.md
- Metric highlight patterns, chart type selection -- these are DA skills

**Weaknesses**:
- DA scope is *metrics and analysis*, not *narrative structure or slide composition*
- Most presentation types (feature pitch, technical deep-dive, onboarding, product demo) have minimal data content
- DA would only own a slice of the skill, not the whole thing

**Verdict**: DA should contribute the data-visualization reference content, not own the skill. Natural collaborator, not owner.

---

### 4. UX Designer (UI)

> "Presentation design IS design. Slide composition, visual hierarchy, information architecture for slides -- these are design skills."

**Strengths of this claim**:
- Slide layout and composition are genuinely design problems -- spatial arrangement, visual weight, information density
- UI skill already has references for interaction-patterns.md, design-systems.md, wireframing.md -- transferable to slide design
- "Information architecture for slides" is a real UX competency

**Weaknesses**:
- Presentation content strategy (what goes on the slides, narrative arc, audience adaptation) is NOT a design problem -- it is a communication problem
- UI skill focuses on *interactive interfaces*, not *static sequential layouts* -- different design domain
- The idea brief explicitly says: "presentation skill handles content and structure, not pixel-level visual design"
- UX Designer would need to own content strategy they are not equipped for

**Verdict**: UX could consult on slide composition patterns, but the skill's core competency is content strategy and narrative, not visual design. Wrong primary owner.

---

### 5. Architect

> "Technical deep-dives are MY presentations. Architecture overviews, design decision presentations -- these require deep technical context that only I have."

**Strengths of this claim**:
- Architecture presentations genuinely require the architect's domain context (design decisions, trade-off analysis, system diagrams)
- The architect already produces the source material (architecture docs, ADRs, system diagrams)
- No other role can credibly present architecture decisions to an engineering audience

**Weaknesses**:
- Architect presentations are 1 of 8 proposed types -- the architect has no claim to sprint reviews, roadmaps, feature pitches, onboarding, etc.
- Architect's competency is *system design*, not *presentation design*
- This is the same "domain expert should own the output format" argument that would give every role their own presentation capability

**Verdict**: Architect should generate their own presentations using shared references, not own the skill.

---

### 6. Developer

> "If we're generating Marp markdown or python-pptx scripts, that's code. I could own the tooling/generation side."

**Strengths of this claim**:
- Marp frontmatter, Mermaid diagram syntax, python-pptx script generation -- these are codegen tasks
- Developer already handles 14 languages; Marp markdown is just another output format
- Tooling detection (is marp-cli installed?) and fallback logic are developer-flavored problems

**Weaknesses**:
- The skill's core value is *content strategy and narrative structure*, not code generation -- Marp markdown is the delivery vehicle, not the competency
- Developer would need presentation design knowledge (slide structure, narrative patterns) that is outside their domain
- This conflates "output format" with "core competency"

**Verdict**: Developer could contribute to tooling references (Marp syntax, python-pptx patterns), but the skill's essence is communication, not codegen.

---

## Ownership Model Evaluation

### Model A: Standalone Skill (New "Presentation Designer" Role)

**How "generate a sprint review deck" works**:
1. User says: "Generate a sprint review deck for this sprint"
2. Delivery-flow orchestrator invokes `presentation` skill with pipeline artifacts
3. Presentation Designer sub-agent loads `slide-structure.md`, `narrative-patterns.md`, `marp-templates.md`
4. Agent reads sprint plan, UAT report, FKCs, commit history from `.delivery/artifacts/`
5. Produces a complete Marp markdown file with title slide, sprint goals recap, features delivered, metrics, demo highlights, next sprint preview, speaker notes

**Pros**: Clean skill boundary. Focused context (4 references, not 12+). Follows existing pattern (one competency per skill). Can collaborate with any role via cross-role invocation. Single place to improve presentation quality.

**Cons**: New skill to maintain. New role to detect. Adds to the skill count (11th delivery-team skill).

---

### Model B: Technical Writer Extension

**How "generate a sprint review deck" works**:
1. User says: "Generate a sprint review deck"
2. Operations skill detects "presentation" keywords, routes to Technical Writer + presentation references
3. TW sub-agent loads documentation-standards.md + slide-structure.md + narrative-patterns.md + marp-templates.md
4. Agent reads sprint artifacts and produces Marp output

**Pros**: No new skill. TW has transferable content-shaping skills.

**Cons**: Operations skill grows to 4 roles, 16 references. Role detection becomes harder (is "create a summary of the release" a release note or a presentation?). Presentation competency is diluted inside a documentation-focused skill. Bloat risk the idea brief already flagged.

---

### Model C: Multi-Role Capability (Each Role Generates Their Own)

**How "generate a sprint review deck" works**:
1. User says: "Generate a sprint review deck"
2. Product-delivery skill detects this as a PO task
3. PO sub-agent loads... what? PO references are about backlog management, user stories, prioritization -- not slide structure
4. PO would need to inline presentation knowledge or load extra references
5. Output quality depends on which role happens to handle it

**Pros**: No new skill. Domain experts own their content.

**Cons**: Every role that generates presentations needs presentation references loaded. Duplicated slide structure knowledge across skills. Inconsistent output quality (architect presentations look different from PO presentations). No single place to improve presentation patterns. Violates the "one competency, one owner" principle.

---

### Model D: Shared References + Per-Role Invocation

**How "generate a sprint review deck" works**:
1. User says: "Generate a sprint review deck"
2. Delivery-flow orchestrator detects presentation request
3. PO sub-agent is spawned with PO references + shared presentation references (slide-structure.md, narrative-patterns.md, marp-templates.md)
4. PO brings domain knowledge (what to present), shared references bring structural knowledge (how to present it)

**Pros**: Domain expertise preserved. Consistent slide structure via shared references. No new role. Each existing role gains presentation capability without owning a separate skill.

**Cons**: Where do shared references live? Currently, each skill loads references from its own `references/` directory. Cross-skill reference sharing would require a new mechanism (a `delivery-team/shared/` directory? symlinks? explicit paths in the sub-agent prompt?). Coordination overhead -- who maintains the shared references? Which skill's SKILL.md contains the presentation routing logic? This model needs an orchestration layer that does not exist today.

---

### Model E: Product Owner Owned

**How "generate a sprint review deck" works**:
1. User says: "Generate a sprint review deck"
2. Product-delivery skill detects this as a PO presentation task
3. PO sub-agent loads stakeholder-templates.md + slide-structure.md + narrative-patterns.md
4. Produces sprint review deck from PO perspective

**Pros**: Natural fit for the 4 most common types (sprint review, roadmap, feature pitch, stakeholder update). PO already owns stakeholder communication.

**Cons**: Technical deep-dives do not belong in PO scope. Architecture presentations require architect context. Product-delivery skill grows to 18+ references. Misaligns competency (PO knows what, not how).

---

## Synthesis Matrix

| Criterion | A: Standalone | B: TW Extension | C: Multi-Role | D: Shared Refs | E: PO Owned |
|-----------|:---:|:---:|:---:|:---:|:---:|
| Clean skill boundary | ++ | - | -- | + | - |
| No new skill needed | -- | ++ | ++ | ++ | ++ |
| Consistent output quality | ++ | + | -- | + | + |
| Domain expertise preserved | + | - | ++ | ++ | - |
| Existing architecture supports it | ++ | ++ | + | -- | + |
| Minimal bloat to existing skills | ++ | -- | - | + | - |
| Single place to improve | ++ | + | -- | - | + |
| Covers all 8 presentation types | ++ | + | + | ++ | - |

**Legend**: ++ strong fit, + moderate fit, - weak fit, -- poor fit

---

## Recommendation: Model A -- Standalone Skill

**Rationale**:

1. **Presentation is a distinct competency.** Slide structure, narrative pacing, audience adaptation, visual information density -- these are not documentation skills, not design skills, not analytics skills. They are *communication design* skills. The team has one competency per skill everywhere else (developer writes code, architect designs systems, quality tests, UI designs interfaces). Presentations should follow this pattern.

2. **The existing architecture supports it directly.** A new `delivery-team/skills/presentation/` directory with its own SKILL.md, 4 reference files, and a single "Presentation Designer" role slots cleanly into the existing plugin structure. No shared-reference mechanism to invent. No cross-skill coordination layer to build. No existing skill needs modification.

3. **Collaboration is already solved.** The delivery-flow orchestrator already invokes skills as sub-agents and passes pipeline context. The presentation skill can receive artifacts from any stage. When the architect needs a technical deep-dive, the orchestrator can invoke the presentation skill with architecture artifacts as context -- the presentation skill brings *how to present*, the artifacts bring *what to present*. This is the same pattern used when Quality validates developer output.

4. **It avoids bloat.** Operations already has 12 references. Product-delivery has 15. Adding presentation references to either would push them past the point where role detection becomes unreliable and context gets diluted. A standalone skill with 4 focused references stays lean.

5. **Single place to improve.** When presentation quality needs improvement -- better narrative patterns, new slide types, Mermaid diagram integration -- there is exactly one place to make that change. With Model C or D, improvements would need to propagate across multiple skills.

6. **The idea brief already decided this.** The brief's "Key Design Decisions" section explicitly chose standalone skill with a rationale. This brainstorm validates that decision from every team perspective. No team member's argument was strong enough to override the standalone model.

**What each role contributes (not owns)**:
- **Technical Writer**: Reviews narrative-patterns.md for prose quality
- **Data Analyst**: Contributes data-visualization.md content (chart selection, metric formatting)
- **UX Designer**: Consults on slide-structure.md (visual hierarchy, information density)
- **Developer**: Contributes marp-templates.md (Marp syntax, Mermaid integration, tooling detection)
- **Architect**: Primary consumer of Technical Deep-Dive type; provides feedback on technical presentation patterns
- **Product Owner**: Primary consumer of Sprint Review, Roadmap, Feature Pitch types; defines presentation type requirements and acceptance criteria

**Dissenting view acknowledged**: Model D (shared references + per-role invocation) is the strongest alternative. It preserves domain expertise better than Model A. However, the current plugin architecture does not support cross-skill reference sharing, and building that mechanism adds scope and complexity that is not justified for v1. If the team later finds that domain-expert presentations consistently outperform generic Presentation Designer output, Model D can be pursued as a v2 evolution.

---

## Next Step

Proceed to PRD refinement with **Model A: Standalone Skill** as the ownership decision. The presentation skill will be a new skill under `delivery-team/skills/presentation/` with a single Presentation Designer role and 4 reference files.

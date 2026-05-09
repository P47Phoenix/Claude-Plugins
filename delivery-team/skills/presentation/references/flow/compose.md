# Step 4: Compose (Composer — this skill)

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

## Editorial Passes (Narrative Intelligence)

After assembling drafts and before format finalization, run four sequential editorial passes. Each pass transforms the slide set; the next pass operates on the transformed output. **Order is strict** (per architecture ADR-02): Emphasis > Cutting > Framing > Tension. No parallelism — each pass depends on the previous pass's output.

Each pass checks its config key before executing. When a pass's config key is `false`, that pass is skipped entirely.

### Pass 1: Emphasis Selection *(config: `presentation.narrative.emphasis`, default: true)*

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

### Pass 2: Information Cutting *(config: `presentation.narrative.cutting`, default: true)*

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

### Pass 3: Audience-Specific Framing *(config: `presentation.narrative.framing`, default: true)*

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

### Pass 4: Narrative Tension *(config: `presentation.narrative.tension`, default: true)*

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

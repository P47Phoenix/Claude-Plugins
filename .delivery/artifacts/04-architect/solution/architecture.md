# Architecture: Presentation Skill v1.1 Enhancements

**Version**: 1.0
**Date**: 2026-04-04
**Architect**: Celebrimbor (Solution Architect)
**PRD**: `.delivery/artifacts/02-refine/po/prd.md` v1.0
**UX Flows**: `.delivery/artifacts/03-design/ux/user-flows.md` v1.0
**Project Type**: FEATURE
**Depth**: LIGHT
**Covers**: Issues #43, #44, #45, #46

---

> *"Let us forge something that will endure beyond the ages. Four enhancements, woven into a skill that already stands -- not a rewrite, but a masterwork of augmentation."*

---

## 1. python-pptx Integration Architecture

### 1.1 File Flow

The PPTX generation follows a three-stage pipeline. Each stage produces a distinct artifact, and failure at any stage falls back to the previous stage's output.

```
SKILL.md (Composer, Step 4)
  │
  ├─ writes → composed-draft.md        (always, all formats)
  │
  └─ writes → composed-draft.json      (only when format=pptx)
                │
                │  post-approval
                ▼
        generate_pptx.py
                │
                └─ writes → {type}-{date}.pptx
```

**Key design decision**: The Composer produces both `.md` and `.json` in parallel during Step 4 when `format=pptx`. The markdown is the human-reviewable artifact (Steps 5-6 operate on it). The JSON is the machine-consumable intermediate for the Python script. This avoids fragile regex parsing of markdown.

### 1.2 JSON Intermediate Format

The JSON structure is defined in the UX flows document (OQ-1 resolution). Per slide:

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
    "project": "...",
    "audience": "investor",
    "format": "pptx"
  }
}
```

The Composer is responsible for producing valid JSON. The Python script is a pure consumer -- it never interprets markdown.

### 1.3 Script Location and Invocation

**Location**: `delivery-team/skills/presentation/scripts/generate_pptx.py`

This follows the plugin structure convention: implementation scripts live in `scripts/` under the skill directory.

**Invocation** (by the Composer after user approval in Step 6):

```bash
python delivery-team/skills/presentation/scripts/generate_pptx.py \
  --input .delivery/artifacts/presentations/.drafts/composed-draft.json \
  --output .delivery/artifacts/presentations/{type}-{date}.pptx \
  [--template {path}] \
  [--font {font}] \
  [--accent-color {hex}]
```

**Dependency check**: Before invocation, the Composer runs a probe:

```python
try:
    import pptx
except ImportError:
    # Fall back to structured-markdown with warning
```

The script itself also guards at import time (FR-07.3). The Composer's pre-check avoids spawning a process that will immediately fail.

### 1.4 Template Handling

Branding resolution follows the precedence chain defined in the UX flows (Flow B.2):

```
CLI --template flag
  └─ config presentation.pptx_template
      └─ CLI --font / --accent-color
          └─ config presentation.pptx_font / presentation.pptx_accent_color
              └─ DEFAULTS: Calibri, #2d5aa0
```

The script loads the template (if any) via `python-pptx`'s `Presentation(template_path)` constructor, which inherits slide masters, fonts, and colors. Font/color flags then override within the loaded template. Layout matching uses name-first, index-fallback strategy (FR-09.3).

### 1.5 Slide Layout Mapping

| JSON `layout` value | PowerPoint Layout | Fallback Index |
|---------------------|-------------------|----------------|
| `title` | "Title Slide" | 0 |
| `content` | "Title and Content" | 1 |
| `metrics` | "Title and Content" | 1 |
| `comparison` | "Title and Content" | 1 |
| `cta` | "Title and Content" | 1 |
| `timeline` | "Title and Content" | 1 |
| `architecture` | "Title and Content" | 1 |

All non-title layouts use "Title and Content" as the base. Differentiation happens in content population, not layout selection. This is intentional -- corporate templates rarely have 7+ custom layouts, so relying on a single flexible layout with varied content formatting is more robust than hunting for specialized layouts.

---

## 2. Narrative Intelligence Sub-Step Ordering

### 2.1 The Four Editorial Passes

The narrative intelligence system inserts four sequential editorial passes into Step 4 (Compose), after draft assembly and before format finalization. The ordering is strict and sequential.

```
Step 4: Compose
  │
  1. ASSEMBLE drafts from .drafts/
  │
  2. PASS 1: Emphasis Selection  ──── reorders slides by impact
  │         ↓ output: reordered slide sequence
  3. PASS 2: Information Cutting ──── merges/removes low-value slides
  │         ↓ output: reduced slide set + cuts log
  4. PASS 3: Audience Framing   ──── restructures arguments per audience
  │         ↓ output: reframed slide content
  5. PASS 4: Narrative Tension  ──── positions climax at 60-70% point
  │         ↓ output: final slide sequence with tension arc
  │
  6. FORMAT + FINALIZE (write .md, optionally .json)
```

### 2.2 Why This Order (and Why Sequential)

The passes are **strictly sequential** -- no parallelism is possible. Each pass transforms the slide set, and the next pass operates on the transformed output.

| Pass | Why This Position | Depends On |
|------|-------------------|------------|
| 1. Emphasis | Must run first because it establishes the impact ranking that all subsequent passes respect. Cutting a slide that was already positioned for emphasis would be contradictory. | Raw drafts only |
| 2. Cutting | Runs after emphasis because we cut *after* knowing what is important. A slide ranked low by emphasis is a stronger cut candidate. The cuts log must be finalized before framing rewrites content. | Emphasis-ranked order |
| 3. Framing | Runs after cutting because we rewrite only surviving slides. Framing a slide that gets cut wastes work. Runs before tension because framing changes argument structure, which affects where the climax should land. | Cut-reduced slide set |
| 4. Tension | Runs last because it needs the final slide set (post-cut) with final content (post-framing) to identify the true climax. Moving a slide to the 60-70% position is meaningless if the slide set or content changes after. | Final framed content |

### 2.3 Pass Data Flow

Each pass reads and writes the same in-memory slide list. No intermediate files.

- **Emphasis**: Reads `body` content of each slide to compute impact signals. Mutates slide order. Writes `emphasis_log` (list of reorder actions).
- **Cutting**: Reads slide content to evaluate cutting heuristics. Removes slides from the list and merges key points into adjacent slides. Writes `cuts_log` (list of merges with rationale).
- **Framing**: Reads `metadata.audience` and each slide's `body`. Rewrites `body` content in-place per audience framing rules from `narrative-patterns.md`. No structural changes.
- **Tension**: Reads slide count (skip if < 6), identifies climax slide, repositions it to 60-70% point. Respects locked positions (PO-sequenced, structural like Now/Next/Later). Mutates slide order.

Both `emphasis_log` and `cuts_log` are preserved for Step 6 output (Narrative Cuts and Emphasis Order sections).

### 2.4 Config Toggles

Each pass can be independently disabled:

| Pass | Disabled By | Effect When Disabled |
|------|-------------|---------------------|
| Emphasis | `narrative_reorder: false` OR user "no reorder" | Pass skipped entirely, original outline order preserved |
| Cutting | `narrative_cutting: false` | Pass skipped entirely, all draft slides preserved |
| Framing | (always on) | Cannot be disabled -- audience is always relevant |
| Tension | Implicitly off when < 6 slides | No config toggle; only slide count threshold applies |

When emphasis is disabled but tension is not, tension still runs -- it works on whatever order exists. When cutting is disabled, tension operates on the full slide set.

---

## 3. Fallback Degradation Architecture

### 3.1 Decision Tree

```
Flow starts → Timer begins
  │
  ├─ PRE-FLOW: Evaluate light mode
  │   ├─ light_mode = "never" OR --full flag? → FULL MODE
  │   ├─ light_mode = "always"? → LIGHT MODE
  │   └─ light_mode = "auto"?
  │       ├─ Contributing roles <= 3? → LIGHT MODE
  │       └─ Contributing roles >= 4? → FULL MODE
  │
  ├─ Steps 1-2: No degradation (always full depth)
  │
  ├─ Step 3 (Draft):
  │   ├─ FULL MODE → all assigned roles dispatched
  │   └─ LIGHT MODE → only required roles, optional slots skipped
  │
  ├─ At 75% of threshold:
  │   └─ DEGRADE: Step 5 → single reviewer (TW only), MUST-FIX only
  │
  ├─ Step 4 (Compose): No degradation (narrative passes always run fully)
  │   Note: Compose is a single-agent step, not parallelizable,
  │   so degradation levers do not apply here.
  │
  ├─ Step 5 (Review Gate):
  │   ├─ FULL + under threshold → 2 reviewers (TW + UX), full scope
  │   ├─ LIGHT + under threshold → 1 reviewer (TW), full scope
  │   ├─ FULL + 75% hit → 1 reviewer (TW), MUST-FIX only
  │   └─ LIGHT + 75% hit → 1 reviewer (TW), MUST-FIX only
  │
  └─ Step 6 (User Review):
      └─ If threshold exceeded → append notice with timing + suggestion
```

### 3.2 What Degrades vs What Never Degrades

| Component | Degrades? | Rationale |
|-----------|-----------|-----------|
| Step 1 (Assemble) | Never | User checkpoint -- must be full quality |
| Step 2 (Content Gate) | Never | Automated validation, negligible time |
| Step 3 (Draft) | Light mode only | Role count is the primary time driver |
| Step 4 (Compose) | Never | Single-agent, editorial passes are fast |
| Step 5 (Review Gate) | Yes | Reviewer count and scope both degrade |
| Step 6 (User Review) | Never | User checkpoint -- always full output |
| Narrative passes | Never | Rule-based, fast, always run if enabled |
| PPTX generation | Never | Post-approval, outside threshold window |

### 3.3 Threshold Resolution

```
1. presentation.thresholds.{type-name} → per-type override
2. presentation.thresholds_default → global override
3. Neither set → 90 seconds (hardcoded)
4. Value = 0 → no threshold (unlimited)
```

The timer starts at flow begin (before Step 1) and the 75% check occurs at each step transition. The threshold governs Steps 1-6 only; PPTX generation is post-approval and outside the threshold window.

### 3.4 Light Mode + Threshold Interaction

Light mode and threshold degradation are **independent controls that converge on the same levers**. They are not cumulative -- when both are active, the effect is the union, not the sum.

| Scenario | Step 3 Roles | Step 5 Reviewers | Step 5 Scope |
|----------|-------------|-----------------|-------------|
| Full, under threshold | All | TW + UX | Full |
| Full, 75% hit | All | TW only | MUST-FIX only |
| Light, under threshold | Required only | TW only | Full |
| Light, 75% hit | Required only | TW only | MUST-FIX only |

The only additive effect: light mode starts with fewer roles in Step 3 AND threshold degradation adds MUST-FIX-only scope in Step 5. The reviewer count does not drop below 1.

---

## 4. File Organization

### 4.1 New Files

| File | Purpose |
|------|---------|
| `delivery-team/skills/presentation/scripts/generate_pptx.py` | PPTX generation script (FR-07 through FR-11) |

This is the only net-new file in the skill directory. The `scripts/` directory does not currently exist and must be created.

### 4.2 Modified Files

| File | Changes | Groups Affected |
|------|---------|----------------|
| `delivery-team/skills/presentation/SKILL.md` | Add 5 new types to detection table. Add pipeline auto-detection mappings. Add PPTX format to output formats section. Add JSON intermediate to Step 4. Add narrative intelligence editorial passes to Step 4. Add light mode and threshold logic. Add new config keys. Add new user commands (`--format pptx`, `--full`, `--light`, `restore`, `no reorder`). Update error handling table. Update references table. | A, B, C, D |
| `delivery-team/skills/presentation/references/narrative-patterns.md` | Add 5 new narrative frameworks (Traction-Opportunity-Ask, Now-Next-Later, Hook-Show-Impact, Context-Landscape-Pathways, Celebrate-Learn-Commit). Add default framework mappings for new types. Add "Audience Framing Rules" section (FR-18). Add type-specific emphasis weight modifiers (OQ-3 resolution). Add narrative tension patterns per type (FR-19). Add sensitivity filter rules for Retro Summary. | A, D |
| `delivery-team/skills/presentation/references/slide-structure.md` | Add slide sequencing sections for 5 new types (Investor Pitch, Roadmap, Product Demo, Onboarding, Retrospective Summary). Add `[DEMO]` placeholder conventions for Product Demo type. | A |
| `delivery-flow/references/config-schema.md` | Add 8 new `presentation.*` config keys following v2.3 extension protocol. Version bump to v2.4. | B, C, D |

### 4.3 Unchanged Files

| File | Rationale |
|------|-----------|
| `references/marp-templates.md` | No Marp changes in v1.1 |
| `references/data-visualization.md` | No visualization changes in v1.1 |

### 4.4 Directory Structure After v1.1

```
delivery-team/skills/presentation/
├── SKILL.md                              (modified)
├── scripts/
│   └── generate_pptx.py                  (new)
└── references/
    ├── slide-structure.md                (modified)
    ├── narrative-patterns.md             (modified)
    ├── data-visualization.md             (unchanged)
    └── marp-templates.md                 (unchanged)
```

---

## 5. Architecture Decision Records

### ADR-01: JSON Intermediate Over Direct Markdown Parsing

**Context**: The PPTX script needs structured slide data. Two options: (a) parse `composed-draft.md` with regex, or (b) have the Composer output a parallel JSON intermediate.

**Decision**: JSON intermediate (option b).

**Rationale**: Markdown parsing is brittle -- slide boundaries, nested bullets, tables, and Mermaid blocks create ambiguous parse states. The JSON is authoritative and typed. The cost is one additional artifact in `.drafts/` (cleaned up on approve/abort). The Composer already knows the slide structure in-memory; serializing to JSON is trivial.

**Consequences**: The Composer must produce valid JSON when `format=pptx`. The JSON schema becomes a contract between the Composer and the script. Changes to slide structure require coordinated updates to both.

### ADR-02: Sequential Editorial Passes, Not Parallel

**Context**: The four narrative intelligence passes could theoretically run in parallel to reduce latency.

**Decision**: Strictly sequential (Emphasis -> Cutting -> Framing -> Tension).

**Rationale**: Each pass transforms the slide set. Emphasis ranking informs cutting decisions. Cutting removes slides before framing rewrites them. Framing changes content that tension uses to identify the climax. Parallel execution would require each pass to operate on a snapshot, producing conflicting mutations that need complex reconciliation. The passes are fast (rule-based, no sub-agent dispatch), so sequential execution adds negligible latency.

### ADR-03: Step 4 (Compose) Never Degrades

**Context**: The threshold degradation system could potentially simplify Step 4 by reducing editorial passes.

**Decision**: Step 4 always runs at full depth. Degradation targets Step 3 (role count) and Step 5 (reviewer count and scope).

**Rationale**: Step 4 is a single-agent step executing rule-based passes -- it is inherently fast. The time cost is dominated by Step 3 (multi-agent dispatch) and Step 5 (multi-reviewer dispatch). Degrading editorial passes would reduce output quality for minimal time savings. The architectural invariant is: degradation reduces *parallelism width* (fewer agents/reviewers), never *processing depth* (fewer passes on the same content).

---

*"And thus the design is laid. Four enhancements, woven into the existing six-step flow with surgical precision. The foundation endures; the augmentation elevates. Let us now forge the implementation."*

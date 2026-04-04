# Sprint 4 Developer Artifact: US-03 & US-04

**Developer**: Gimli
**Date**: 2026-04-04
**Sprint**: 4 (PPTX Output, Group B)
**Stories**: US-03 (5 SP), US-04 (3 SP)
**Issues**: #44

> *"I have hewn the code from solid Python, and the axe has not faltered. And my code!"*

---

## Files Created

| File | Purpose | Lines |
|------|---------|-------|
| `delivery-team/skills/presentation/scripts/generate_pptx.py` | PPTX generation script (FR-07, FR-08, FR-09) | ~340 |

## Files Modified

| File | Changes | Story |
|------|---------|-------|
| `delivery-team/skills/presentation/SKILL.md` | Added PPTX format spec, Step 6 PPTX generation flow, format config keys, help text, error handling entries, references entry | US-04 |
| `delivery-team/skills/delivery-flow/references/config-schema.md` | Added `pptx_template`, `pptx_font`, `pptx_accent_color` keys; updated `default_format` valid values; bumped to v2.6 | US-04 |

---

## US-03: generate_pptx.py Implementation

### FR-07: JSON-to-PPTX Conversion

The script reads `composed-draft.json` (produced by the Composer in Step 4 when format=pptx) and generates a `.pptx` file. The JSON is the authoritative source -- no markdown parsing (per ADR-01).

**Slide generation pipeline**:
1. Parse and validate JSON input (requires non-empty `slides` array)
2. Load template or create blank 16:9 presentation
3. For each slide: resolve layout, populate content, add speaker notes
4. Apply font and accent color
5. Save `.pptx` to output path

**CLI interface**:
```
python generate_pptx.py --input FILE --output FILE [--template FILE] [--font NAME] [--accent-color HEX]
```

### FR-08: Template Support

- `--template` loads a `.pptx` template via `Presentation(template_path)`, inheriting slide masters, fonts, and colors
- Font and accent-color flags override within the loaded template
- Branding precedence: CLI flags > config values > defaults (Calibri, #2d5aa0)

### FR-09: Import Guard

The script checks `import pptx` at the top and exits with:
```
Error: python-pptx is required. Install with: pip install python-pptx
```
No traceback. Non-zero exit code. Clean error for the user.

### Layout Mapping (Architecture Section 1.5)

| JSON `layout` | PowerPoint Layout | Fallback Index | Content Strategy |
|---------------|-------------------|----------------|-----------------|
| `title` | "Title Slide" | 0 | Title + subtitle from body |
| `content` | "Title and Content" | 1 | Standard bullets |
| `metrics` | "Title and Content" | 1 | Larger font bullets for data emphasis |
| `comparison` | "Title and Content" | 1 | Table shape with headers + rows |
| `cta` | "Title and Content" | 1 | Numbered list |
| `timeline` | "Title and Content" | 1 | Table shape with milestone rows |
| `architecture` | "Title and Content" | 1 | Bullets + Mermaid fallback note |

Layout resolution uses name-first, index-fallback strategy. If no layout matches by name or index, falls back to layout 0.

### Speaker Notes (OQ-5)

When `speaker_notes` is present in the JSON, it is populated into the slide's notes pane via `slide.notes_slide.notes_text_frame.text`.

### Error Handling

| Error | Behavior |
|-------|----------|
| python-pptx not installed | Exit with clear message (no traceback) |
| Input file not found | Error message with path |
| Invalid JSON | Error message with parse details |
| Empty/missing slides array | Error message |
| Template file not found | Error message with path |
| Invalid hex color | Error message with format hint |

---

## US-04: PPTX Format Config & SKILL.md Updates

### FR-10: `presentation.default_format` Updated

Added `pptx` as a valid value for `presentation.default_format` in:
- SKILL.md config table (valid values now: structured-markdown, marp, paste-ready, pptx)
- config-schema.md schema table
- config-schema.md YAML template

### FR-11: PPTX Config Keys

Added to config-schema.md (v2.6) and SKILL.md:

| Key | Type | Default | Purpose |
|-----|------|---------|---------|
| `presentation.pptx_template` | string | "" | Path to .pptx template |
| `presentation.pptx_font` | string | "Calibri" | Font family override |
| `presentation.pptx_accent_color` | string | "#2d5aa0" | Hex accent color override |

### SKILL.md Changes

1. **Description**: Updated to mention PPTX output
2. **Step 4 (Compose)**: Added JSON intermediate production when format=pptx
3. **Step 6 (User Review)**: Added PPTX Generation subsection with dependency check, script invocation, branding precedence, output message, and cleanup
4. **Output Format Specifications**: Added PPTX section between Marp and Paste-Ready
5. **Error Handling**: Added 3 PPTX-specific error rows (python-pptx missing, template missing, invalid JSON)
6. **User Commands**: Updated `--format` to list pptx
7. **References**: Added `scripts/generate_pptx.py` entry
8. **Config Integration**: Added 3 PPTX config keys, updated `default_format` description

### Config Schema Changes

- Bumped version from 2.5 to 2.6
- Added 3 new keys to schema table
- Updated `default_format` valid values to include `pptx`
- Added keys to YAML template
- Added version history entry

---

## AC Traceability

### US-03 Acceptance Criteria

| AC | Status | Evidence |
|----|--------|----------|
| AC-01: Script produces valid PPTX from JSON | DONE | `generate_pptx()` function reads JSON, creates `Presentation`, adds slides, saves .pptx |
| AC-02: Each JSON slide maps to one PowerPoint slide | DONE | Loop in `generate_pptx()` creates exactly one slide per JSON slide entry |
| AC-03: Slide layout mapping correct | DONE | `LAYOUT_MAP` dict + `resolve_layout()` + layout-specific `populate_*` functions |
| AC-04: Template support with branding precedence | DONE | `--template` loads via `Presentation(template_path)`, `--font`/`--accent-color` override within |
| AC-05: Graceful dependency error | DONE | Import guard at top of file, exits with clear message, no traceback |

### US-04 Acceptance Criteria

| AC | Status | Evidence |
|----|--------|----------|
| AC-01: PPTX is a recognized output format | DONE | Added to SKILL.md format options, Step 6 invocation flow, output path pattern |
| AC-02: Config default_format supports pptx | DONE | Updated valid values in SKILL.md and config-schema.md |
| AC-03: Fallback to structured-markdown | DONE | Step 6 PPTX Generation subsection documents dependency check and fallback |
| AC-04: Help text lists pptx | DONE | Updated `present --format` command row |
| AC-05: Font, color, template config keys | DONE | 3 keys added to SKILL.md config table and config-schema.md |
| AC-06: JSON intermediate in Step 4 | DONE | Added PPTX JSON intermediate paragraph to Step 4 |

---

## Diff Summary

Gimli does not leave loose stones in the mine. Here is what was touched and nothing more:

- **1 file created**: `generate_pptx.py` (~340 lines of production Python)
- **2 files modified**: `SKILL.md` (8 sections touched), `config-schema.md` (4 sections touched)
- **0 files deleted**

And my code!

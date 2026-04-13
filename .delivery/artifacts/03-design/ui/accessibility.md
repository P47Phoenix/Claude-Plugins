# Accessibility Review: Hardware Delivery Team Plugin CLI

**Version**: 1.0
**Date**: 2026-04-12
**Author**: UI Designer (Arwen)
**Source Artifacts**:
- `.delivery/artifacts/03-design/ux/wireframes.md` v1.0
- `.delivery/artifacts/03-design/ui/component-specs.md` v1.0
**Project Type**: GREENFIELD
**Role**: UI Designer | Task: accessibility-review | References: design-systems.md, ui-patterns.md

---

> *"I choose a mortal design -- and I will make it timeless. Accessibility is not adornment; it is the foundation upon which all designs must rest, lest they crumble for those who need them most."*

---

## Table of Contents

1. [Review Methodology](#review-methodology)
2. [Finding 1: Screen Reader Compatibility](#finding-1-screen-reader-compatibility)
3. [Finding 2: Color Independence](#finding-2-color-independence)
4. [Finding 3: Cognitive Load and Information Density](#finding-3-cognitive-load-and-information-density)
5. [Finding 4: Text Sizing and Readability](#finding-4-text-sizing-and-readability)
6. [Finding 5: Motor Accessibility](#finding-5-motor-accessibility)
7. [Finding 6: Internationalization and Terminal Compatibility](#finding-6-internationalization-and-terminal-compatibility)
8. [Finding 7: Error Recovery](#finding-7-error-recovery)
9. [Finding 8: Information Hierarchy](#finding-8-information-hierarchy)
10. [Summary Matrix](#summary-matrix)
11. [Recommendations Priority](#recommendations-priority)

---

## Review Methodology

This review evaluates CLI output designs -- not web UI or graphical interfaces. The accessibility concerns are distinct:

- **Screen readers** in CLI context means terminal screen readers (NVDA with Windows Terminal, VoiceOver with macOS Terminal, Orca with Linux terminals)
- **Color** means ANSI terminal color codes (which the current design does not use)
- **Motor accessibility** means keystroke efficiency and command complexity
- **Cognitive load** means information density per output block

Each finding is rated:
- **BLOCKING**: Must fix before implementation. The design excludes users or creates safety risks.
- **WARNING**: Should fix. Creates significant friction for affected users.
- **SUGGESTION**: Nice to have. Improves experience for affected users but does not exclude them.

---

## Finding 1: Screen Reader Compatibility

### 1A: ASCII Box Drawing is Screen-Reader Friendly

**Severity**: SUGGESTION (positive finding -- no issue)

The design's deliberate choice of ASCII `+`, `-`, `|` for box drawing is excellent for screen readers. Unicode box-drawing characters (U+2500 range) are read aloud character-by-character by most screen readers ("BOX DRAWINGS LIGHT HORIZONTAL, BOX DRAWINGS LIGHT HORIZONTAL..."), creating an unintelligible experience. The ASCII approach avoids this entirely.

Screen readers will read `+----...+` as "plus dash dash dash..." which, while not ideal, is a known pattern that screen reader users learn to skip. This component shall endure as designed.

**Fix**: None required. The design is already optimal for this concern.

---

### 1B: Repeated Dash/Plus Characters Create Verbose Screen Reader Output

**Severity**: WARNING

While ASCII box drawing is better than Unicode, a 60-character border line produces screen reader output like: "plus dash dash dash dash dash dash dash..." repeated approximately 58 times per border. A single box has a top and bottom border, producing ~116 dashes read aloud. The Stage Header `=` banner produces 60 equals signs read twice (top and bottom).

For a gate result with findings (Wireframe 5B), a screen reader user hears hundreds of repeated characters before reaching the actual content.

**Fix**: Document a **plain-text mode** as an alternative rendering. When enabled (via `.hardware/config.yml`), suppress box borders and banners entirely, replacing them with structured text:

```
# Current (boxed):
+------------------------------------------------------------+
| GATE: Schematic --> Layout                                 |
| [DONE] Component lifecycle check                          |
| Result: PASS -- advancing to Schematic                     |
+------------------------------------------------------------+

# Plain-text mode:
--- GATE: Schematic --> Layout ---
[DONE] Component lifecycle check
Result: PASS -- advancing to Schematic
---
```

Add a config key:

```yaml
display:
  plain_text_mode: false  # default; set true for screen reader users
```

This eliminates 100% of repeated box characters while preserving the information hierarchy through `---` separators (3 dashes, not 60).

---

### 1C: Progress Indicators Lack Text Labels

**Severity**: WARNING

The progress indicators `[>]`, `[~]`, `[+]` are visually scannable but semantically opaque to screen readers. A screen reader reads them as "left bracket greater-than right bracket" which conveys no meaning.

The component spec (Component 2, Agent Status) defines these as:
- `[>]` = dispatched/starting
- `[~]` = in-progress
- `[+]` = completed

The meaning is documented but not present in the output itself.

**Fix**: In plain-text mode, expand indicators to include text labels:

```
# Current:
  [>] Dispatching: Electrical Engineer
  [~] Component selection: querying DigiKey for U3...
  [+] Complete: Electrical Engineer (artifacts: 4)

# Plain-text mode:
  [START] Dispatching: Electrical Engineer
  [WORKING] Component selection: querying DigiKey for U3...
  [COMPLETE] Complete: Electrical Engineer (artifacts: 4)
```

The indicators already have text after them ("Dispatching", "Complete"), which provides context. However, the `[~]` lines only have activity text, so the expanded label adds necessary semantics.

---

## Finding 2: Color Independence

### 2A: Design Does Not Rely on Color

**Severity**: SUGGESTION (positive finding -- no issue)

The design makes zero use of ANSI color codes. All semantic information is conveyed through text tokens: `[DONE]`, `[NOT_DONE]`, `[CRITICAL]`, `[MAJOR]`, `[MINOR]`, `[WARNING]`, `[ERROR]`, `[INFO]`. These are text-based, not color-based.

This is an exceptional design choice. Color-blind users, users with monochrome terminals, users over SSH connections with limited terminal capabilities -- all receive identical information fidelity.

**Fix**: None required. Preserve this design decision. If future enhancements add optional ANSI color, ensure it is purely decorative and never the sole indicator of state or severity.

---

### 2B: Optional Color Enhancement Pathway

**Severity**: SUGGESTION

While the current no-color design is correct for accessibility, some users benefit from color as a supplementary signal. Consider a future config key:

```yaml
display:
  color_mode: none  # none | basic | 256
```

If implemented, color must only enhance (e.g., green for `[DONE]`, red for `[CRITICAL]`) and the text tokens must remain present. The text token is the primary signal; color is a secondary, optional signal.

**Fix**: No immediate action. Document this as a future enhancement pathway in the design rationale.

---

## Finding 3: Cognitive Load and Information Density

### 3A: Gate Results with Multiple Findings Are Dense

**Severity**: WARNING

Wireframe 5G (Schematic Review Gate, Multi-Reviewer, Iterative) shows 7 findings with location and fix data. With the box borders, this produces approximately 30 lines of output in a single block. For users with attention or processing differences, this is a significant cognitive load.

The Design Review Board output (Wireframe 5F) compounds this by showing findings grouped by 4 reviewers, plus deduplication counts and severity tallies -- approximately 20 lines.

**Fix**: Add a **summary-first** pattern. Present the summary line before the detail:

```
+------------------------------------------------------------+
| SCHEMATIC REVIEW GATE                                      |
|                                                            |
| Summary: 1 critical, 2 major, 2 minor, 2 warning          |
| Result: NOT_DONE -- 1 critical finding                     |
|                                                            |
| Details (7 findings):                                      |
|  [CRITICAL] F-001: Missing bulk cap on U3 VDD             |
|    Location: Sheet 2, U3 pin 14                           |
|    Fix: Add 10uF ceramic cap, place within 3mm            |
|  [MAJOR] F-002: Unterminated SPI_CLK trace                |
|    ...                                                     |
+------------------------------------------------------------+
```

Moving the summary and result to the top lets users with attention differences immediately understand the gate outcome without parsing all findings first. The detailed findings become optional reading for those who need them.

---

### 3B: Rework Escalation Presents Too Much History at Once

**Severity**: SUGGESTION

Wireframe 7A (Per-Path Rework Limit) shows the full rework history, pattern analysis, recommendation, and options in a single block. While each piece is valuable, presenting them all simultaneously asks the user to hold multiple contexts:

1. What happened (history)
2. Why it keeps happening (pattern)
3. What to do about it (recommendation)
4. What their choices are (options)

**Fix**: Consider separating the history/pattern from the decision prompt with a visual break:

```
+------------------------------------------------------------+
| REWORK LIMIT REACHED                                       |
|                                                            |
| Path: DFM/DFA --> Schematic (3/3 iterations)               |
| Pattern: Component selection for U5 failing repeatedly.    |
|                                                            |
| RECOMMENDATION: Redesign power regulation approach.        |
+------------------------------------------------------------+

+------------------------------------------------------------+
| === PIPELINE PAUSED ===                                    |
| Options:                                                   |
|  "continue" -- override limit, try once more               |
|  "abort" -- stop the pipeline run                          |
|  "override limit N" -- set new per-path limit              |
+------------------------------------------------------------+
```

Two smaller blocks are easier to process than one large block. The user processes the situation first, then the decision separately.

---

### 3C: Pipeline Status Table is Well-Structured

**Severity**: SUGGESTION (positive finding)

Wireframe 8A (Pipeline Status) is well-designed for cognitive accessibility. The line-per-stage format with aligned `[DONE]` / `[PAUSED]` / `[ ]` markers creates a scannable pattern. The user can locate their current position instantly. The summary footer provides context without requiring re-reading the table.

**Fix**: None required. This is a strong pattern.

---

## Finding 4: Text Sizing and Readability

### 4A: 60-Character Width is Appropriate

**Severity**: SUGGESTION (positive finding)

The 60-character outer width (56-character inner width) is appropriate for CLI readability. It fits within the standard 80-column terminal with a 20-character margin, accommodating terminal chrome, scrollbars, and line numbers. Lines are short enough to be readable without horizontal scrolling on most displays.

**Fix**: None required.

---

### 4B: Wrapped Content Indentation is Inconsistent

**Severity**: WARNING

The wireframes show content wrapping at 56 characters, but indentation of wrapped lines varies:

- Artifact references (Component 9) wrap with 3-space indent
- Activity lists in Stage Headers wrap with alignment to the previous line's content start
- Finding descriptions in Gate Results appear to wrap without explicit indent rules
- Rework reason text in Component 10 wraps with 2-space indent

Inconsistent indentation makes it harder for users to distinguish between a continuation line and a new item, especially for users with visual processing differences or users relying on screen readers.

**Fix**: Standardize continuation indent across all components. Recommendation:

| Content Type | Continuation Indent |
|---|---|
| Artifact descriptions | 3 spaces (after `N. ` prefix) -- as specified |
| Activity lists | 14 spaces (aligned under first activity after `Activities: `) |
| Finding descriptions | 4 spaces (under finding summary text) |
| Rework reasons | 2 spaces (match existing) |
| General wrapped text | 2 spaces from left margin |

Document this in the Design Token Foundation as a `WRAP_INDENT` token per content type.

---

### 4C: Long Findings May Bury Critical Information

**Severity**: SUGGESTION

In multi-finding gate results (Wireframe 5G), critical findings appear at the top of the list but could be pushed below the visible scroll area if preceded by many validator pass/fail lines. The `Result` line at the bottom is the actionable conclusion.

The current design already shows severity-sorted findings (critical first), which is correct. The summary-first pattern from Finding 3A would also address this.

**Fix**: Addressed by Finding 3A recommendation (summary-first pattern).

---

## Finding 5: Motor Accessibility

### 5A: Command Patterns Are Simple and Memorable

**Severity**: SUGGESTION (positive finding)

The design uses natural-language commands:
- "Run the hardware pipeline"
- "prototype complete"
- "prototype failed: [description]"
- "save pipeline state"
- "Resume hardware pipeline"
- "continue" / "abort" / "override limit N"

These are short, memorable phrases. Users with motor impairments benefit from shorter input sequences. The option commands ("continue", "abort") are single words.

**Fix**: None required. The command design is well-suited for motor accessibility.

---

### 5B: Setup Wizard Is Sequential (Good for Motor Accessibility)

**Severity**: SUGGESTION (positive finding)

The setup wizard presents one question at a time (Wireframe 1B). This avoids requiring users to navigate a form or tab between fields. Each question has a simple input: type a value, select a number, or accept a default.

Questions with defaults (Questions 4, 7, 8, 9) allow pressing Enter to accept, which is the lowest-effort interaction possible.

**Fix**: None required.

---

### 5C: Multi-Choice Inputs Use Single-Digit Numbers

**Severity**: SUGGESTION (positive finding)

Setup wizard multi-choice questions (Questions 2, 5, 6) use `[1]`, `[2]`, `[3]` etc. This requires a single keypress plus Enter. This is optimal for motor accessibility.

**Fix**: None required.

---

### 5D: Stale State Warning Requires Typing Full Words

**Severity**: SUGGESTION

Wireframe 8D (Stale State Warning) presents three options: "resume", "revalidate", "restart". These are 6, 12, and 7 characters respectively. For users with motor impairments, "revalidate" is a long word to type accurately.

**Fix**: Accept shortened forms: "r" for resume, "rv" for revalidate, "rs" for restart. Document the short forms alongside the full words:

```
| Options:                                                   |
|  "resume" (r) -- continue from last stage                  |
|  "revalidate" (rv) -- re-run gates from modified stage     |
|  "restart" (rs) -- start pipeline from beginning           |
```

---

## Finding 6: Internationalization and Terminal Compatibility

### 6A: Pure ASCII Character Set is Maximally Compatible

**Severity**: SUGGESTION (positive finding)

The design uses exclusively ASCII characters (U+002B, U+002D, U+007C, U+003D, standard alphanumerics, and standard punctuation). Every character is within the first 128 Unicode code points. This renders correctly on every terminal emulator, every font, every operating system, every SSH session, and every locale configuration.

No CJK characters, no emoji, no box-drawing Unicode, no special symbols.

**Fix**: None required. This is an exemplary decision for terminal compatibility.

---

### 6B: LOTR Theme Text Stays Within ASCII

**Severity**: SUGGESTION (positive finding)

The LOTR themed text uses English words and ASCII punctuation. No special Unicode characters are introduced by theming. The theme token substitution architecture (documented in Component Specs, Theme Injection Architecture) enforces that themed values must fit within `WIDTH_INNER` (56 chars), which implicitly keeps them simple.

**Fix**: Add an explicit rule to the Theme Injection Architecture: "Themed token values MUST use only ASCII characters (U+0000-U+007F). No emoji, no Unicode symbols, no characters outside the basic ASCII range." This prevents future themes from introducing compatibility issues.

---

### 6C: All Text Is English-Only

**Severity**: SUGGESTION

The design does not address localization. All output text is in English. This is appropriate for a v1.0 CLI plugin -- internationalization of CLI output adds significant complexity for low initial value. However, the token substitution architecture provides a natural extension point for future localization.

**Fix**: No immediate action. Document in Design Rationale: "All output text is English. The theme token architecture provides a natural extension point for future i18n if needed -- a language token map could replace the theme token map."

---

## Finding 7: Error Recovery

### 7A: Pipeline State Persistence Enables Recovery

**Severity**: SUGGESTION (positive finding)

The design includes:
- "save pipeline state" command at any human checkpoint (Wireframe 4B)
- Resume notification on SessionStart (Wireframe 8B)
- Explicit resume and restart options (Wireframe 8C)
- Stale state detection with three recovery options (Wireframe 8D)

Users cannot lose pipeline progress. Every human-facing pause point offers a save option. Session interruptions are detected and surfaced with recovery paths.

**Fix**: None required. The error recovery design is thorough.

---

### 7B: Config Overwrite Is Destructive Without Backup

**Severity**: WARNING

Wireframe 1E shows: `Config already exists (schema v1.0). Overwrite? [y/N] _`

A "y" response destroys the existing config with no backup. If the user made manual edits to their config, those edits are lost.

**Fix**: Before overwriting, create a backup:

```
Config already exists (schema v1.0). Overwrite? [y/N] _
(Current config will be backed up to .hardware/config.yml.bak)
```

Implement automatic backup before any overwrite. The backup file should be timestamped if multiple backups may exist: `.hardware/config.yml.bak.2026-04-12T1432`.

---

### 7C: Gate Failure Messages Are Actionable

**Severity**: SUGGESTION (positive finding)

Every gate failure includes:
- **What** failed (finding ID and description)
- **Where** it failed (location: sheet, net, coordinate)
- **How to fix** it (actionable fix instruction)

This follows NFR-005 and is excellent for error recovery. The user never faces a gate failure without knowing exactly what to do about it.

**Fix**: None required.

---

### 7D: Rework Escalation Provides Clear Options

**Severity**: SUGGESTION (positive finding)

When rework limits are reached (Wireframes 7A, 7B), the design presents:
- History of what was tried
- Pattern analysis explaining why it keeps failing
- Recommendation for what to do differently
- Three explicit options with descriptions

The user is never stuck. They always have at least three choices: continue, abort, or adjust limits.

**Fix**: None required.

---

## Finding 8: Information Hierarchy

### 8A: Stage Banners Use Visual Weight Effectively

**Severity**: SUGGESTION (positive finding)

The design uses two distinct visual weights:
- Full-width `=` banners for stage transitions (high visual weight, infrequent)
- `+---+` boxes for informational blocks (medium visual weight, frequent)
- Unboxed `[>]`/`[~]`/`[+]` lines for progress (low visual weight, very frequent)

This three-tier hierarchy lets users scan for stage boundaries quickly, find informational blocks at medium priority, and optionally read progress detail.

**Fix**: None required. This hierarchy is well-designed.

---

### 8B: Gate Result Line Buried at Bottom of Block

**Severity**: WARNING

In gate result components (Wireframe 5B, 5G, Component 3 Variant A/B), the `Result: PASS/NOT_DONE` line is the last line before the closing box border. This means the most important information -- whether the gate passed or failed -- requires reading or scrolling past all findings first.

For a gate with 7 findings (Wireframe 5G), the result line is approximately 25 lines below the gate header. Users must scroll past all findings to learn the outcome.

**Fix**: Addressed by Finding 3A (summary-first pattern). Place the result immediately after the gate header, before the findings:

```
+------------------------------------------------------------+
| GATE: Schematic --> Layout                                 |
| Result: NOT_DONE -- 1 critical finding                     |
|                                                            |
| Findings:                                                  |
|  [CRITICAL] F-001: Missing bulk cap on U3 VDD             |
|    Location: Sheet 2, U3 pin 14                           |
|    Fix: Add 10uF ceramic cap, place within 3mm            |
|  ...                                                       |
+------------------------------------------------------------+
```

---

### 8C: Pre-Flight Summary Prioritizes Correctly

**Severity**: SUGGESTION (positive finding)

Wireframe 2A (Pre-Flight Summary) leads with:
1. Pipeline name and project
2. Config path and version
3. Key config values (fab, regions, budget)
4. Dependency status
5. Memory status
6. Stage sequence

This ordering is correct -- identity first, then configuration, then dependencies, then the plan. Users get the most important context first.

**Fix**: None required.

---

### 8D: Human Checkpoint Action Items Lack Priority Ordering

**Severity**: SUGGESTION

Wireframe 4B (Human-Action Checkpoint) lists action items as a flat checkbox list:

```
| Action items:                                              |
|  [ ] 1. Order prototype boards from JLCPCB                 |
|  [ ] 2. Assemble and bring up prototype                    |
|  [ ] 3. Execute bring-up test procedure                    |
|  [ ] 4. Record test results                                |
```

These items are sequential (you cannot assemble before ordering), but the numbering is the only indicator of sequence. There is no explicit "do these in order" instruction.

**Fix**: Add a brief note when action items are sequential:

```
| Action items (in order):                                   |
|  [ ] 1. Order prototype boards from JLCPCB                 |
|  ...                                                       |
```

The "(in order)" annotation makes the sequential dependency explicit for all users.

---

## Summary Matrix

| # | Finding | Severity | Category | Fix Required |
|---|---------|----------|----------|-------------|
| 1A | ASCII box drawing is screen-reader friendly | SUGGESTION | Screen reader | None (positive) |
| 1B | Repeated dash/plus chars verbose for screen readers | WARNING | Screen reader | Add plain-text mode config |
| 1C | Progress indicators lack text labels | WARNING | Screen reader | Expand labels in plain-text mode |
| 2A | No color dependency | SUGGESTION | Color | None (positive) |
| 2B | Optional color enhancement pathway | SUGGESTION | Color | Document future pathway |
| 3A | Dense gate results with many findings | WARNING | Cognitive load | Summary-first pattern |
| 3B | Rework escalation presents too much at once | SUGGESTION | Cognitive load | Split into two blocks |
| 3C | Pipeline status table well-structured | SUGGESTION | Cognitive load | None (positive) |
| 4A | 60-char width appropriate | SUGGESTION | Readability | None (positive) |
| 4B | Wrapped content indentation inconsistent | WARNING | Readability | Standardize WRAP_INDENT tokens |
| 4C | Critical findings may be buried | SUGGESTION | Readability | Addressed by 3A |
| 5A | Simple command patterns | SUGGESTION | Motor | None (positive) |
| 5B | Sequential setup wizard | SUGGESTION | Motor | None (positive) |
| 5C | Single-digit multi-choice inputs | SUGGESTION | Motor | None (positive) |
| 5D | Long option words to type | SUGGESTION | Motor | Accept short forms |
| 6A | Pure ASCII character set | SUGGESTION | i18n/terminal | None (positive) |
| 6B | LOTR theme stays ASCII | SUGGESTION | i18n/terminal | Add explicit ASCII-only rule |
| 6C | English-only text | SUGGESTION | i18n | Document as future extension |
| 7A | Pipeline state persistence | SUGGESTION | Error recovery | None (positive) |
| 7B | Config overwrite without backup | WARNING | Error recovery | Auto-backup before overwrite |
| 7C | Actionable gate failure messages | SUGGESTION | Error recovery | None (positive) |
| 7D | Clear escalation options | SUGGESTION | Error recovery | None (positive) |
| 8A | Three-tier visual hierarchy | SUGGESTION | Info hierarchy | None (positive) |
| 8B | Gate result buried at bottom | WARNING | Info hierarchy | Summary-first (same as 3A) |
| 8C | Pre-flight prioritizes correctly | SUGGESTION | Info hierarchy | None (positive) |
| 8D | Action items lack sequence indicator | SUGGESTION | Info hierarchy | Add "(in order)" annotation |

---

## Recommendations Priority

### Must Address (6 WARNING findings)

1. **Plain-text mode** (1B, 1C): Add `display.plain_text_mode` config key that suppresses box borders and expands progress indicator labels. This is the single most impactful accessibility improvement for screen reader users.

2. **Summary-first gate results** (3A, 8B): Move the `Result` line and severity summary above the detailed findings in all gate result components (Component 3, all variants).

3. **Standardize wrap indentation** (4B): Define `WRAP_INDENT` tokens in the Design Token Foundation for each content type. Document and enforce consistently.

4. **Config overwrite backup** (7B): Implement automatic backup before overwriting `.hardware/config.yml` in the setup wizard.

### Should Address (4 SUGGESTION findings requiring action)

5. **Short-form option commands** (5D): Accept abbreviated inputs for multi-option prompts.
6. **ASCII-only theme rule** (6B): Add explicit rule to Theme Injection Architecture.
7. **Split escalation blocks** (3B): Separate rework history from decision prompt.
8. **Sequential action item annotation** (8D): Add "(in order)" to sequential checkpoint items.

### No Action Required (14 positive findings)

Findings 1A, 2A, 3C, 4A, 5A, 5B, 5C, 6A, 6B, 7A, 7C, 7D, 8A, 8C are positive assessments confirming strong accessibility decisions already present in the design. These design choices should be preserved and documented as intentional accessibility decisions.

---

### Overall Assessment

The hardware-team plugin's CLI design is **fundamentally sound** for accessibility. The decision to use ASCII-only characters, text-based severity tokens (not color), and natural-language commands demonstrates thoughtful design. The three-tier visual hierarchy, actionable error messages, and comprehensive error recovery pathways are strong.

The primary gaps are in screen reader support (plain-text mode needed) and information density for cognitive accessibility (summary-first pattern needed). Both are addressable without structural redesign -- they add alternative rendering modes and reorder existing content.

I give this design my blessing for implementation, with the six WARNING-level findings addressed before or during development.

---

> *"I choose a mortal design -- and I will make it timeless. These findings are placed with the care of one who has lived long enough to know that true beauty serves all who behold it, not merely those with perfect sight."*

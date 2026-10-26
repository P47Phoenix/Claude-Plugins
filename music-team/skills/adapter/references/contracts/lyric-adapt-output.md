---
loaded_by: adapter
level: L2
last_reviewed: 2026-10-26
---

# Output Contract: lyric-adapt

Artifact: `lyrics.md`. The grammar is the normal lyrics grammar in
`music-team/references/shared/artifact-formats.md`, followed by one `## Adaptation notes` block.

## Lyric body

- One `[Label]` tag per section; labels equal the `label` column of `structure.md` exactly.
- One lyric line per line; a blank line between sections; no other markup.
- The line count of every section equals the number of lines in its `meter_spec`.
- Each line fits its `meter_spec` entry (syllable count and stress shape) within `quality.prosody_tolerance`.
- The rhyme letters follow the section's `rhyme_scheme` (`x` lines are unconstrained).
- Lines starting with `# ` are comments: gates ignore them.

## Adaptation notes block

Place it after the last section, separated by one blank line. The heading is literal; **every line after
it starts with `# `** so `prosody_check.py`, `rhyme_check.py`, `structure_check.py` and `cliche_scan.py`
treat it as comments and do not count it as lyric text.

```text
## Adaptation notes
# Kept: <comma-separated preserved elements>
# Changed: <element>: <source> -> <target> (<why>)
# Changed: <element>: <source> -> <target> (<why>)
# Risks: <one risk per line; singability, drift from the source, originality>
```

Rules:

- Exactly one `# Kept:` line; one `# Changed:` line per changed element family (group line edits per section);
  one or more `# Risks:` lines.
- Every `Changed` entry has all four parts: element, source, target, why. An entry without a why is a defect.
- Quote lyric text only from the user's supplied input, and only the words needed to identify the change.
- No artist, band or song names.
- At most `adaptation.max_changed_elements` `# Changed:` lines across this artifact.

## Example

```markdown
[Verse 1]
(four adapted lines)

## Adaptation notes
# Kept: title idea, first-person voice, the three key images, refrain line, rhyme scheme AABB
# Changed: Verse 1 line length: 9-11 syllables -> 7-8 (shorter lines flow across the barline)
# Changed: diction: a hard-consonant noun -> a softer near-synonym (same meaning, easier to sing)
# Risks: line 3 opens on two stressed words and needs a breath
```

## Hand-back

```text
SKILL_LOADED: <every references/ path pasted>
STATUS: DONE | BLOCKED
ARTIFACT: <dir>/lyrics.md
SUMMARY: one sentence, max 200 characters
```

`BLOCKED` adds `FINDINGS:` bullets: each names a line that cannot fit its `meter_spec` without changing meaning.

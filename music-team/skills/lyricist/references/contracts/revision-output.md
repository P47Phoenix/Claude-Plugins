---
loaded_by: lyricist
level: L2
last_reviewed: 2026-10-26
---

# Revision Output Contract

Role: `lyric-editor`. Task: `lyric-revision`. Artifact: `lyrics.md`, edited in place. Used after `verse-writer`, for REWRITE (supplied original lyric) and for REVISE (named sections). Validated by `prosody_check.py`, `rhyme_check.py`, `cliche_scan.py`.

## Grammar

The artifact follows the full `lyrics-output.md` grammar (tags equal to `structure.md`, one lyric line per line, blank line between sections, `# ` comments ignored). Edits add one trailing comment block:

```markdown
# Changes:
# - Verse 2:3 | stress mismatch on "every" | reworded to fit uSuSuSuS
# - Chorus:2 | cliche hit | replaced with a concrete image
# Unchanged: Verse 1, Chorus (hook line kept verbatim)
```

Each `# - <Section>:<line> | <reason> | <what changed>` row names a location in the `<section>:<line>` form the gates use. `# Unchanged:` lists the sections left byte for byte.

## Scope rules

| Situation | Rule |
|-----------|------|
| Gate FAIL loop | Edit only the lines named in the gate JSON `violations[].location` and critique, plus lines a rhyme or meter change forces |
| REWRITE | Edit toward the request ("tighten", "fix meter"); keep every line the user did not ask to change; provenance required |
| REVISE | Edit only the sections the request names; other sections are read-only context, copied exactly |
| Hook line | Keep verbatim unless the request or `concept.md` changed |
| Structure | Never change tags, section order or per-section line counts; report a spec conflict in `SUMMARY` instead |

## Rules

- Do not write commentary in the lyric body; reasons live in the `# Changes:` block.
- The change notes must not quote lines from outside the user's own text; refer to locations.
- Recognised well-known lyric in the input: stop, `STATUS: BLOCKED`, `SUMMARY` states the recognition; write no artifact.
- Hand-back: `SKILL_LOADED:`, `STATUS:`, `ARTIFACT: <dir>/lyrics.md`, `SUMMARY:` (<= 200 characters, include remaining violations if any).

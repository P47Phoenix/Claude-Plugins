---
loaded_by: lyricist
level: L2
last_reviewed: 2026-10-26
---

# Concept Output Contract

Role: `hook-writer`. Task: `hook-concept`. Artifact: `concept.md`. Grammar source: `references/shared/artifact-formats.md` section `concept.md`. Validated by `cliche_scan.py` and `prosody_check.py --hook`.

## Grammar

YAML front-matter between `---` fences, then an optional `## Notes` body.

| Key | Required | Rule |
|-----|----------|------|
| `title` | yes | Non-empty string; usually the hook or its key phrase |
| `hook_line` | exactly one of `hook_line` / `motif` | One sung line; syllables <= `quality.hook_max_syllables` (default 12) |
| `motif` | exactly one of `hook_line` / `motif` | INSTRUMENTAL only: technical description of the recurring musical idea |
| `central_image` | yes | One concrete object, place or action |
| `arc` | yes | List of exactly three items in order: start, turn, end. Flow-style `[a, b, c]` |
| `title_rationale` | yes | One sentence on why the title and hook work together |

`## Notes` is optional prose (a short paragraph on how verses, pre-chorus, chorus and bridge use the image). No lyric lines belong in it.

## Template

```markdown
---
title: <title>
hook_line: <one sung line>
central_image: <concrete image>
arc: [<start>, <turn>, <end>]
title_rationale: <one sentence>
---

## Notes

<optional paragraph>
```

## Hook placement downstream

The `hook_line` is placed word for word in the Chorus of `lyrics.md` by `verse-writer`. Write it so it can stand alone, and note in `## Notes` which Chorus line carries it (first or last line by default).

## Rules

- Values with a colon or a comma inside a list item are wrapped in double quotes.
- No artist or song names; no quoted existing lyrics.
- Gate-clean: no phrase from `cliche-list.txt` in `title`, `hook_line` or `central_image`.
- Hand-back: `SKILL_LOADED:`, `STATUS:`, `ARTIFACT: <dir>/concept.md`, `SUMMARY:` (<= 200 characters).

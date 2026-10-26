---
loaded_by: music-release
level: L2
last_reviewed: 2026-10-26
---

# Output Contract: package/

Written by `music-release` at Stage 7c into `.song/<slug>/package/`. Grammar source of truth for the shared
parts: `references/shared/artifact-formats.md`, section `package/`. Which files a type gets is in `SKILL.md`.

## lyric-sheet.md

```markdown
# <title>

[Verse 1]
<line>
...
```

The title comes from `concept.md` `title` (else `brief.md` `title`, else the slug). The body is `lyrics.md`
reproduced line for line, section tags unchanged. Drop only: lines starting with `#` (the `<!-- new -->`
markers) and every `## Augmentation` and `## Adaptation notes` section through its end. Nothing else changes.

## lead-sheet.abc

`melody.abc` with a chord symbol before the first note of each bar, quoted: `"D"` or `"Am7"`. The chord for
a bar comes from `chords.md` for the matching section and bar index (a `%` repeats the previous chord; two chords in one
bar annotate their two beats). If the bar counts of a section differ between `chords.md` and `melody.abc`, copy
that section unannotated and add `lead-sheet: section <label> unannotated (bar count)` to `release-notes.md`.
Headers, `%%section` lines and `w:` lines are copied unchanged. INSTRUMENTAL has no `w:` lines.

## song.mid

Written by `midi_export.py` (see `SKILL.md`). Never hand-edited.

## one-pager.md

```markdown
# <title>

- Genre: <genre>
- Key: <key> <mode>
- Tempo: <bpm> bpm, <time_sig>
- Length: <target seconds from structure.md, or bars x tempo>
- Hook: <hook_line, or motif for INSTRUMENTAL>
- Arc: <three arc beats from concept.md, joined with " / ">
```

All values come from `brief.md`, `concept.md`, `structure.md`. A value that is absent is written `n/a`.
The hook line is the one line the lyric sheet already contains; nothing is invented.

## release-notes.md

```markdown
# Release notes: <title>

- run_id: <state.json run_id>
- song_type: <type>
- Gates: <stage>: PASS|SKIPPED|FAIL (one bullet per stage in state.json gates)
- Loops used: concept N, structure N, lyrics N, music N, arrangement N, release N
- Overrides: <none | one bullet per gate_overrides entry: stage, reason>
- Accepted best: <none | stages with accepted_best true>
- Challenger: BLOCKER 0, MAJOR n, MINOR n
- Panel: <majority KEEP|SKIP (n of m) with each top_note, or "not run">
- MIDI: written | omitted (unreadable input) | not applicable
- Adaptation: <ADAPT_GENRE only: source_genre -> target_genre, counts of Kept and Changed rows>
```

Counts are read from `state.json`, `challenge-report.md` (count table rows) and `panel-report.md`. No lyric text.

## new-sections.md (AUGMENT_LYRICS)

`# <title>: new sections` followed by only the sections that follow a `<!-- new -->` marker in `lyrics.md`, tags
and lines unchanged.

## Rules

1. Every file is UTF-8 with LF endings and ends with a newline.
2. No artist or song names, no "sounds like", no reference tracks.
3. `package/` holds only the files listed for the type; remove none of the source artifacts.

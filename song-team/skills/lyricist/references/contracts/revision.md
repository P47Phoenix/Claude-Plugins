---
loaded_by: lyric-editor
level: L2
last_reviewed: 2026-10-26
---

# Output Contract: lyrics.md revision

Normative grammar: `references/shared/artifact-formats.md` section `lyrics.md`. Normative gate rules: `references/shared/stage-gates.md`. This contract restates both for the `lyric-editor` role. Every rule in `contracts/section-lyric.md` still applies to the revised file; this contract adds the rules of a revision.

## File

Path: `.song/<slug>/lyrics.md`, overwritten in place (the prompt states the exact path). UTF-8, LF.

## Scope of edit

1. **Edit list.** The set of lines you edit is derived from the gate JSON: for each `violations[]` entry, the section named in `location` (`<Section>:<line>`). You edit lines inside those sections only.
2. **Within a cited section**, change the fewest lines that bring the section under the threshold. The cited line is the worst line, not necessarily the only one to change; the ratio is per section.
3. **Outside cited sections**, every byte is preserved: tags, comments, blank lines, lyric lines, trailing newline.
4. **Line count per section** stays equal to the number of meter entries. Never add, remove, merge, or split lines.
5. **Tags** are never edited. A tag mismatch is a `verse-writer` defect; report it in `SUMMARY` with `STATUS: BLOCKED` rather than renaming tags.
6. **Hook line** (the `concept.md` `hook_line` as it appears in a chorus) is edited only when a violation cites that exact line. When you edit it, state the new line in `SUMMARY` so `song-flow` updates `concept.md`.
7. **Rhyme pairs.** Changing an end word in a lettered line requires checking every other line sharing that letter in the same section. The preferred edit target is the later line of a failing pair (its `location` is what `rhyme_check.py` reports).
8. **Cliché swaps** keep the syllable count and stress pattern of the removed phrase, so a cliché fix never creates a prosody violation.
9. **`must_include[]` / `must_avoid[]`** from `brief.md` hold after the revision exactly as before.

## Required report (in `SUMMARY`)

A Markdown table, one row per changed line, followed by one line of recount:

```markdown
| location | before | after | reason |
|----------|--------|-------|--------|
| Verse 2:3 | The vendor asked me for my name again | The vendor asks my name again | syllables 9 -> 8; "again" lands uS on beat |
| Bridge:2 | The corner shop will know my order | The corner shop will know my face | rhyme key er -> Ace; full rhyme with "place" (line 4) |
recount: Verse 2 ratio 0.22 -> 0.06 (16 S positions, 1 miss); Bridge 0 rhyme violations
```

Rows list lyric lines only, never comments. "before" and "after" are the full lines. "reason" names the script rule that motivated the change and the numbers you counted. When a cited line was left unchanged, add a row with identical before/after and the reason.

## Forbidden

- Rewriting a passing line "for flow", "for voice", or "to improve it".
- Changing a section not named in any `violations[].location`.
- Introducing a new phrase from `references/shared/cliche-list.txt` anywhere.
- Real artist names, song titles, quoted existing lyrics, `must_avoid[]` items.
- Stating that a gate now passes. Report your recount; the script decides.

## Gates run against this file

The same scripts as `contracts/section-lyric.md`, on the whole file: `prosody_check.py --json lyrics.md structure.md brief.md`, `rhyme_check.py --json lyrics.md structure.md brief.md`, `cliche_scan.py --json lyrics.md`. `song-flow` compares the new gate JSON with the previous one; a revision that lowers the cited section's ratio but raises another section's is a regression and is re-dispatched with both violations.

## Max length

Same as the input file plus zero lines; the revised file has the same line count as the original.

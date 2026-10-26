---
loaded_by: lyricist
level: L2
last_reviewed: 2026-10-26
---

# Lyrics Output Contract

Role: `verse-writer` (first draft). Task: `section-lyrics`. Artifact: `lyrics.md`. Grammar source: `references/shared/artifact-formats.md` section `lyrics.md`. Validated by `prosody_check.py`, `rhyme_check.py`, `cliche_scan.py`.

## Grammar

- One `[Label]` tag on its own line per section, then one lyric line per line, then a blank line.
- Allowed labels: `Intro`, `Verse N`, `Pre-Chorus N`, `Chorus`, `Post-Chorus`, `Bridge`, `Instrumental`, `Breakdown`, `Build`, `Drop`, `Tag`, `Outro`, and AABA `A1`, `A2`, `B`, `A3`.
- Tags are identical, in the same order, to the `label` column of `structure.md`. A tag absent from `structure.md` makes `prosody_check.py` ERROR.
- Lines starting with `# ` are comments; every gate ignores them.
- Instrumental sections have no lyric lines; omit the tag or leave it empty only if `structure.md` has zero meter entries for it.

## Fit to `structure.md`

`meter_spec` is `syllables/stress` per line, lines separated by `;`, stress as `S`/`u` (for example `8/uSuSuSuS`).

| Check | Rule |
|-------|------|
| Line count | Lyric lines in a section == number of meter entries for it |
| Syllables | Each line's count == the entry's count (dictionary speech; silent final e dropped) |
| Stress | Each spec `S` position carries a stressed syllable; mismatches over `quality.prosody_tolerance` fail the section |
| Rhyme | Lines sharing a letter in `rhyme_scheme` full-rhyme (slant if config allows); `x` is free; letters are scoped per section |
| Hook | `concept.md` `hook_line` appears verbatim in each Chorus (first or last line by default) |
| Repeats | Repeated sections (Chorus) are written out in full each time, identical unless the spec differs |

## Template

```markdown
[Verse 1]
<line 1>
<line 2>
<line 3>
<line 4>

[Chorus]
<hook line>
...
```

Optional trailing comment block: `# Notes: <assumptions>`; no commentary elsewhere.

## Rules

- Write in the brief's `language`. Non-English lyrics keep line counts; prosody and rhyme gates SKIP.
- No cliche-list phrases; no artist or song names; no recognisable existing lyric lines.
- Hand-back: `SKILL_LOADED:`, `STATUS:`, `ARTIFACT: <dir>/lyrics.md`, `SUMMARY:` (<= 200 characters).

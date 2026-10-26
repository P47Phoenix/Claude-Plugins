---
loaded_by: verse-writer
level: L2
last_reviewed: 2026-10-26
---

# Output Contract: lyrics.md (section lyric)

Normative grammar: `references/shared/artifact-formats.md` section `lyrics.md`. Normative gate rules: `references/shared/stage-gates.md`. This contract restates both for the `verse-writer` role.

## File

Path: `.song/<slug>/lyrics.md` (the prompt states the exact path). UTF-8, LF line endings, Markdown. No front-matter.

## Structure

1. One `[Label]` tag per section, on its own line, **character-identical** to the `label` column of `structure.md`, in the same order, each section appearing exactly as many times as the structure table lists it. `[Chorus]` is not `[Chorus 1]`; `[Pre-Chorus 1]` keeps its hyphen and its number.
2. Under each tag: exactly as many lyric lines as the section's `meter_spec` has entries (entries are `;`-separated). One lyric line per text line. No blank lines inside a section.
3. One blank line between sections.
4. Lines beginning with `# ` are comments; gates ignore them and they do not count as lyric lines. Use them for plans or stress marks.
5. No section headings, no bold, no quotes, no trailing spaces, no numbering.

## Per-line rules (what `meter_spec` means)

Each meter entry is `N/pattern`: `N` syllables, `pattern` one `S` or `u` per syllable. For lyric line i against meter entry i:

- Syllable count equals `N` exactly, counted by the heuristic (vowel groups; silent trailing `e` dropped; `-ed` silent after most consonants; `-le` after a consonant counts one; `every` = 3, `fire` = 1, `hour` = 1, `poem` = 2 by the exception table).
- Every `S` position carries a stressed syllable: a monosyllabic content word (noun, verb, adjective, adverb) or the stressed syllable of a polysyllable (first syllable by default; `-tion`/`-ic`/`-ity` endings and `un-`/`re-`/`be-`/`de-`/`com-`/`pre-` prefixes shift it to the second syllable: `before` = `uS`, `again` = `uS`, `remember` = `uSu`).
- Every `u` position carries a function word (article, preposition, pronoun, auxiliary, conjunction; `like`, `still`, `yours`, `not`, `am`, `is`, `are`, `did` are all function words to the script) or an unstressed syllable of a polysyllable.
- A `u` position holding a stressed syllable costs nothing. An `S` position holding an unstressed one costs one. A syllable-count difference costs one per syllable. The section fails when total cost / count of `S` in the section spec exceeds `prosody_tolerance` (default 0.15).

## Rhyme rules (what `rhyme_scheme` means)

- Letters are scoped per section; `A` in Verse 1 has no relation to `A` in Verse 2.
- Lines sharing a letter rhyme on their last word. Full rhyme = identical key (last vowel group onward, normalised): `street`/`feet`, `town`/`down`, `rain`/`again`, `wall`/`call`, `river`/`ever`.
- Slant rhyme (allowed when `slant_rhyme_allowed: true`, the default): same vowel class with a different tail (`home`/`alone`, `time`/`line`) or same non-empty final consonant cluster with a different vowel (`fence`/`sense`, `porch`/`church`). `go`/`see` is not a rhyme. `drawer`/`more` and `fire`/`tired` are not rhymes to the script.
- `x` or `X` marks a free line. An empty scheme leaves the section free.
- The scheme length equals the line count; a mismatch is an ERROR, not a FAIL.

## Example (original; Verse 1 spec `8/uSuSuSuS; 8/uSuSuSuS` scheme `AA`)

```markdown
[Verse 1]
# plan: the first morning, nothing has a name yet
The kettle hums before the light
A borrowed coat that fits me wrong
```

## Forbidden content

- Real artist names, song titles, band names; quoted or closely paraphrased existing lyrics.
- Any item from `brief.md` `must_avoid[]`.
- Phrases from `references/shared/cliche-list.txt` beyond the configured density (target zero).
- Section tags not present in `structure.md`; lyric lines outside any section.
- Placeholder lines (`la la la`, `TBD`, `[verse here]`).

## Gates run against this file

| Script | Invocation | PASS when |
|--------|------------|-----------|
| `structure_check.py` | `structure_check.py --json structure.md lyrics.md` | tags match and are ordered; lyric lines per section = meter entries |
| `prosody_check.py` | `prosody_check.py --json lyrics.md structure.md brief.md` | every section's mismatch ratio <= `prosody_tolerance` |
| `rhyme_check.py` | `rhyme_check.py --json lyrics.md structure.md brief.md` | every lettered pair full-rhymes, or slant-rhymes when allowed |
| `cliche_scan.py` | `cliche_scan.py --json lyrics.md` | hits per 100 words <= `cliche_max_per_100_words` |

`prosody_check.py` and `rhyme_check.py` report SKIPPED (treated as PASS) when `brief.md.language` is not `en`; the structure and cliché checks always run.

## Max length

120 lines including tags, comments, and blank lines.

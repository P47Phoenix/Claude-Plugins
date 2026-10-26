---
loaded_by: harmony
level: L2
last_reviewed: 2026-10-26
---

# Output Contract: chords.md (chord chart)

Normative grammar: `references/shared/artifact-formats.md` section `chords.md`. Normative gate rules: `references/shared/stage-gates.md` (`chord_tools.py`). This contract restates both for the `harmony` role.

## File

Path: `.song/<slug>/chords.md` (the prompt states the exact path). UTF-8, LF line endings, Markdown. No front-matter.

## Structure

1. Line 1: `key: <Tonic> <mode>`, where `<Tonic>` is `A`-`G` with an optional `#` or `b`, and `<mode>` is one of `major`, `minor`, `dorian`, `mixolydian`, `lydian`, `phrygian`, `locrian`, matching `structure.md` `key` and `mode` exactly (`key: D major`, `key: A minor`, `key: Bb major`). The gate reads the key from `structure.md` when it is given and from this line otherwise; the two must agree.
2. One blank line, then one `[Label]` block per section, in `structure.md` order, each label character-identical to the structure table (`[Pre-Chorus 1]`, `[Chorus]`, `[A1]`). Every section appears, including Intro, Instrumental, and Outro.
3. Under each tag: one or more **chart lines**, each `| cell | cell | ... |` with one bar per cell. The total cell count of a section equals its `bars` in `structure.md`.
4. Directly under each chart line: a **concert line** starting with `> ` and holding the same number of cells with concert-pitch chord symbols (`> | D | A | Bm | G |`). The gate ignores `>` lines and `#` comment lines.
5. One blank line between sections. No prose inside a block; no headings; no trailing spaces.

## Cell grammar (what `chord_tools.py` parses)

```text
[b|#] <I..VII | i..vii> [dim|°|o|aug|+|maj7|m7|7|sus2|sus4|add9|dim7|m7b5] [/<bass>]
%      repeats the previous cell (counts as a chord)
```

- Upper-case numeral = major triad, lower-case = minor; `dim`/`°`/`o` and `aug`/`+` override the triad. Seventh, sus, and add suffixes are tolerated and do not change the triad test (`sus` chords are diatonic whenever their root is a scale degree).
- `<bass>` is a numeral (`V`, `bVII`) or a scale degree digit (`3`): `I/3`, `V/VII`, `ii/IV`.
- A numeral with no accidental names the **mode's** degree (`VI` in A minor is F major, `VII` is G major). A numeral with an accidental is spelled against the major scale and shifted (`bVII` is always two semitones below the tonic, `#iv` always six above).
- Diatonic = the root is a scale degree of the mode **and** the triad quality is the one the mode builds there (`ii` diatonic in major, `II` not; `bVII` diatonic in mixolydian, not in major).
- Outside the grammar (ERROR): `N.C.`, `I9`, `Imaj9`, `Vsus`, `V7b9`, chord letters (`D`, `Bm`) in a chart line, `♭`, `-` as minor, empty cells.

## Example (original; key D major; Verse 1 has 8 bars, Chorus 4)

```markdown
key: D major

[Verse 1]
| I | V | vi | IV |
> | D | A | Bm | G |
| I | V | IV | I |
> | D | A | G | D |

[Chorus]
| IV | I | V | vi |
> | G | D | A | Bm |
```

## Forbidden content

- Real artist names, song titles, or "in the style of" notes anywhere, including comments.
- A `key:` line that differs from `structure.md`; a section tag absent from `structure.md`; a section missing from this file.
- A chart line whose cell count does not fit the section's `bars`; a cell outside the grammar above.
- Tempo, time signature, or lyric text (those live in `structure.md`, `melody.abc`, `lyrics.md`).

## Gates run against this file

| Script | Invocation | PASS when |
|--------|------------|-----------|
| `chord_tools.py` | `chord_tools.py --json chords.md structure.md` | every cell parses; `metrics.diatonic_ratio` >= `diatonic_min_ratio` (default 0.6; equal passes) |
| `structure_check.py --consistency` (Stage 6) | `structure_check.py --consistency --json structure.md chords.md melody.abc arrangement.md` | `key`/`mode` equal `structure.md`; `[Label]` list identical to the structure table |

Warnings (counted, never FAIL): adjacent root-position major/minor triads a whole step apart (`IV V`, `V IV`, `bVII I`), and a section whose last two cells form none of `V-I`, `IV-I`, `V-vi`, `bVII-I`. The `--json` output carries a `concert` map with the gate's own spellings; when yours differ, the gate's are the arranger's reference.

## Max length

80 lines including tags and blank lines.

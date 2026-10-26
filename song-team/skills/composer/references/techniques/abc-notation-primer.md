---
loaded_by: melody
level: L3
last_reviewed: 2026-10-26
---

# Technique: ABC Notation Primer (the strict subset `abc_validate.py` accepts)

`abc_common.py` parses a deliberately small slice of ABC 2.1. Anything outside it is a parse ERROR with a line number, and an ERROR skips every other check. Learn the slice; write nothing else.

## Headers (first six lines, this order)

```abc
X:1
T:Morning Finds the Window
M:4/4
L:1/8
Q:1/4=120
K:G
```

- `X:` an integer. `T:` the title from `concept.md`. `M:` equals `structure.md` `time_sig` (`4/4`, `3/4`, `6/8`; `C` is read as `4/4`). `L:1/8` always (durations below assume it). `Q:1/4=<bpm>` with the structure's bpm. `K:` tonic plus mode suffix: `K:G` major, `K:Em` minor, `K:D dorian`, `K:A mixolydian`, `K:Bb`, `K:F#m`. The gate parses `K:` into (tonic, mode) and compares to `structure.md`; `K:G major` and `K:Gmaj` also parse, but write the short form.
- At most one `V:` line; none is the norm. No other header is needed; `C:` (composer) is parsed and ignored but is never an artist name.

## Sections

`%%section <Label>` on its own line, label character-identical to `structure.md` (`%%section Pre-Chorus 1`). Every section of the structure appears, in order, including ones with no lyric. The first music line follows the first `%%section` line; music before any section is a mismatch.

## Notes and pitch

| Written | MIDI | Note |
|---------|------|------|
| `C,` | 48 | octave below middle C |
| `G,` | 55 | bottom of the default range |
| `C` | 60 | middle C |
| `G` | 67 | |
| `c` | 72 | |
| `g` | 79 | top of the default range |
| `c'` | 84 | out of range |

Accidentals prefix the note: `^F` sharp, `_B` flat, `=F` natural; an explicit accidental persists to the end of its bar. Notes without an accidental take the key signature from `K:` (in `K:D`, every `F` is F#). Write the letter the key implies and let the signature work.

## Durations (relative to `L:1/8`)

| Written | Length in 4/4 |
|---------|---------------|
| `A` | eighth |
| `A2` | quarter |
| `A3` | dotted quarter |
| `A4` | half |
| `A6` | dotted half |
| `A8` | whole bar |
| `A/2` or `A/` | sixteenth |
| `A3/2` | dotted eighth |

A bar in 4/4 holds 8 units; in 3/4, 6; in 6/8, 6. The gate does not check bar length, but `midi_export.py` and the arranger do, so make every bar add up. Rests: `z`, `z2`, `z4`, `z8` (also `x`). Rests are not note heads and carry no `w:` token.

## Bar lines, ties, and the rest of the slice

- Bars: `|`; end of section `||` or `|]`; `|:` and `:|` parse but write every bar out (bar counts are literal).
- Tie: `-` after a note, to the same pitch next (`A2-A2`, or across a bar or line end `A4- | A2`); the tied-into note is **not** a new head and takes no token. A tie joins two notes of the same pitch; a hyphen between different pitches (`B2- d2`) is a slur and does not merge them, so the second note is a head. A rest after the `-` breaks the tie; a `-` with no note after it before `%%section` or end of file is an ERROR.
- Parsed and ignored for alignment: chord symbols in quotes (`"G"`), slurs `(A B)`, broken rhythm `A>B` `A<B`, tuplets `(3ABC`, grace notes `{A}B`, decorations `!fermata!`, inline fields `[K:D]`, repeat endings `[1`.
- Comments: `%` to end of line. A line starting with `%` that is not `%%section` is ignored.
- Everything else is an ERROR: `~` as an ornament, `.` staccato, `[CEG]` chord notes, `&` voice overlay, `>` with no note before it, `w:` before any music, two `w:` lines on one music line, non-ASCII quotes.

## `w:` lyric lines

A `w:` line directly follows the music line it belongs to and is split into bars by `|`. Tokens per bar must equal the non-rest, non-tied-into heads in that bar.

| Token | Meaning | Example |
|-------|---------|---------|
| word | one syllable on one note | `knows` |
| `-` inside a word | split into syllables, one note each | `win-dow` = 2 tokens |
| `_` | extend the previous syllable over the next note (melisma); no new token | `yet_` = 1 syllable + 1 extension = 2 notes |
| `*` | one note with no syllable (pickup, instrumental hit) | `* the night` |
| `~` | join two words on one note | `of~the` = 1 token |
| `\|` | next bar | |

Worked examples against `G2 A2 B2 c2 | d4 B4 |` (4 heads, then 2):

```abc
w: Mor-ning finds the | win-dow |          % 4 + 2: correct
w: Mor-ning finds the win- | dow |         % 5 + 1: FAIL (bar 1 observed 5, limit 4)
w: Morning finds the | win-dow |           % 3 + 2: FAIL ("Morning" is one token)
```

Melisma and skip, against `A2 B2 c4 | d2 c2 B2 A2 |` (3 heads, then 4):

```abc
w: here yet_ | * I'm still a |              % 2 + 1 ext = 3; 1 skip + 3 = 4: correct
```

**Section text rule.** Strip the hyphens, join the tokens, restore `~` to a space, drop punctuation and case: the result must equal the `lyrics.md` section text processed the same way. `I've` and `Ive` match; `the city` and `the town` do not. Copy each lyric line from `lyrics.md`, then hyphenate; never retype from memory.

## Check by hand before returning

1. Six headers, in order; `K:` and `M:` copied from `structure.md`.
2. `%%section` list equals the structure table, in order.
3. Bars per section (count `|`) equal `bars`.
4. For every `w:` line: tokens + `_` + `*` per bar = heads per bar; hyphen every polysyllable.
5. Lowest and highest letter inside the range (`G,` to `g` by default); no leap over an octave.
6. No character outside the slice.

---
loaded_by: composer
level: L3
last_reviewed: 2026-10-26
---

# ABC Notation Primer (the subset music-team uses)

## Headers (in order)

```abc
X:1
T:Working Title
M:4/4
L:1/8
Q:1/4=118
K:D
```

`X` reference number (integer), `T` title, `M` meter, `L` default note length, `Q` tempo (`1/4=118` is 118 quarter notes per minute), `K` key and mode (last header). One voice only: at most one `V:` line.

## Pitches

| Written | Pitch (middle C = C4) |
|---------|------------------------|
| `C D E F G A B` | C4 to B4 |
| `c d e f g a b` | C5 to B5 |
| `c'` | C6 (each `'` raises an octave) |
| `C,` | C3 (each `,` lowers an octave) |

The key signature decides sharps and flats: in `K:D` every `F` is F# and every `C` is C#. Add accidentals only for chromatic notes: `^F` sharp, `_B` flat, `=F` natural. An accidental holds for the rest of the bar.

## Lengths (with `L:1/8`)

| Written | Length |
|---------|--------|
| `C` | 1 eighth |
| `C2` | quarter |
| `C4` | half |
| `C8` | whole |
| `C3` | dotted quarter |
| `C/2` or `C/` | sixteenth |
| `C3/2` | dotted eighth |

Rests use `z` with the same lengths. Broken rhythm: `A>B` is dotted-short, `A<B` short-dotted. Triplet: `(3ABC` three notes in the time of two.

## Bars and repeats

`|` bar line, `||` double bar, `|]` final bar, `|:` and `:|` repeat signs, `[1` and `[2` endings. Each bar must add up to the meter: in 4/4 with `L:1/8`, eight eighths (`D2 E2 F2 GA` is 2+2+2+1+1).

## Ties, slurs, chords, annotations

- Tie: `F4-F2` joins two notes of the same pitch; the second takes no lyric syllable.
- Slur: `(GA)` groups notes; parentheses must balance.
- Chord (stacked notes): `[CEG]2`.
- Chord symbol annotation: `"G"B2` prints G above the note and is ignored for timing.

## Sections

```abc
%%section Verse 1
```

One line per section, label identical to `structure.md`. Repeat the label for every repeat (each Chorus).

## Lyrics

A `w:` line directly after its music line:

```abc
D2 E2 F2 GA | B2 A2 F4 |
w: I count the num-bers | on the street |
```

| Token | Meaning |
|-------|---------|
| `word` | one syllable on the next note |
| `num-bers` | `-` splits syllables, one per note |
| `yet_` | `_` extends the syllable over the next note (one extra slot) |
| `*` | skip a note |
| `a~b` | two words on one note |
| `\|` | advance to the next bar |

Per bar: syllables + extensions + skips equals the pitched notes (rests and tied continuations take none).

## Worked bar count

`d2 c2 B2 A2 | B2 A2 F2 ED |` has 4 and 5 notes. A matching line: `w: No-bo-dy knows | my name here yet_ |` gives 4, then 4 syllables + 1 extension = 5.

## Validate

`python3 -I scripts/abc_validate.py melody.abc structure.md lyrics.md` checks headers, bar sums, range, leaps, and the lyric alignment. Parse errors (stray `]`, unbalanced `(`, unknown header such as a two-letter field) are an ERROR.

## Pitfalls

| Mistake | Effect |
|---------|--------|
| Bar adds to 7 or 9 eighths | bar-length FAIL |
| `K:` earlier than `Q:` | header order broken |
| Forgetting that the key signature already sharpens F and C in D | false accidentals |
| `w:` with a bar fewer than the music | alignment FAIL at that bar |
| Missing `%%section` | sections do not match structure |

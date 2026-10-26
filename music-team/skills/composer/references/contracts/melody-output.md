---
loaded_by: composer
level: L2
last_reviewed: 2026-10-26
---

# Melody Output Contract: `melody.abc`

Owner: `melody`. Validated by `abc_validate.py melody.abc structure.md [lyrics.md]` (Stage 5). The grammar is the one in `references/shared/artifact-formats.md`.

## Grammar

```abc
X:1
T:<title>
M:<time_sig from structure.md>
L:<unit note length, usually 1/8>
Q:1/4=<bpm from structure.md>
K:<key and mode from structure.md>
%%section <Label>
<music line>
w: <lyric line>
%%section <Label>
...
```

- **Headers in this order:** `X:1`, `T:` (non-empty title from `concept.md`), `M:`, `L:`, `Q:1/4=<bpm>`, `K:`. `K:` is last in the header. At most one `V:` line (single voice).
- **`M:`** equals `structure.md` `time_sig`. **`K:`** equals key and mode (`K:D`, `K:Bbm`, `K:Edor`). **`Q:`** equals `structure.md` `bpm` (quarter-note beats).
- **Sections** start with `%%section <Label>` using `structure.md` labels, same order, repeats included.
- **Music lines.** One per lyric line. Notes `C D E F G A B` and `c d e f g a b` with `'` (octave up) and `,` (octave down); accidentals `^` sharp, `_` flat, `=` natural (they last to the bar line); lengths `2`, `/2`, `3/2`; rests `z`; ties `-`; chords in `[]`; bar lines `|`, repeats `|:` `:|`. Chord symbols as `"G"` annotations are allowed.
- **`w:` lines** follow each music line when `lyrics.md` exists (none for INSTRUMENTAL). Tokens: `-` splits a syllable, `_` extends the previous syllable over the next note, `*` skips a note, `~` joins two words into one token, `|` advances the bar.

## Rules the gate enforces

1. Headers `X T M L Q K` all present; `M`, `K`, `Q` agree with `structure.md`; `%%section` labels equal the structure labels in order.
2. Every bar sums to the meter. A short first (pickup) bar and a short final bar are tolerated; any other short or long bar fails with location `<section>:<bar>`.
3. No leap between consecutive pitched notes larger than `max_melodic_leap` (default 12 semitones); every pitch inside `vocal_range` (default MIDI 55-79, G3-G5).
4. Lyric alignment per bar: syllable tokens plus `_` extensions plus `*` skips equal the pitched note heads (rests and tied continuations take no syllable). The de-hyphenated `w:` text per section equals the `lyrics.md` section, ignoring case and punctuation.
5. Unparseable ABC is an ERROR (stray `]`, unclosed `(`, unknown header).

## Example

```abc
X:1
T:Nobody Knows My Name Here
M:4/4
L:1/8
Q:1/4=118
K:D
%%section Verse 1
D2 E2 F2 GA | B2 A2 F4 |
w: I count the num-bers | on the street |
%%section Chorus
d2 c2 B2 A2 | B2 A2 F2 ED |
w: No-bo-dy knows | my name here yet_ |
```

Bar 2 of the chorus has 5 note heads and 4 syllables plus one `_` extension: 5 slots.

## Authoring checklist

1. Count each bar before writing the next (`L:1/8`, 4/4 means 8 eighths).
2. Stressed syllables on strong beats or long notes; unstressed on short or off-beat notes.
3. Last note of each phrase is a chord tone of that bar's chord (read `chords.md`).
4. Re-count `w:` slots per bar after every edit.

## Hand-back

```text
SKILL_LOADED: <paths>
STATUS: DONE | BLOCKED
ARTIFACT: <dir>/melody.abc
SUMMARY: <one sentence, max 200 characters; range, hook contour, any melisma>
```

On BLOCKED add `FINDINGS:` bullets (lyric line too long for the section's bars, range conflict, missing `chords.md`).

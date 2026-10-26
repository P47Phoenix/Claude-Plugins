---
loaded_by: melody
level: L2
last_reviewed: 2026-10-26
---

# Output Contract: melody.abc (single-voice melody)

Normative grammar: `references/shared/artifact-formats.md` section `melody.abc`. Normative gate rules: `references/shared/stage-gates.md` (`abc_validate.py`). This contract restates both for the `melody` role; `techniques/abc-notation-primer.md` teaches the subset in detail.

## File

Path: `.song/<slug>/melody.abc` (the prompt states the exact path). UTF-8, LF line endings, plain text. No Markdown, no front-matter, no fences.

## Structure

1. Six header lines, in this order and nothing between them:
   `X:1` / `T:<title from concept.md>` / `M:<time_sig from structure.md>` / `L:1/8` / `Q:1/4=<bpm from structure.md>` / `K:<key><mode>`.
   `K:` spelling: `K:D` (major), `K:Dm` (minor), `K:D dorian`, `K:D mixolydian`. `Bb` and `F#` tonics are written as such (`K:Bbm`). The gate compares `K:` to `structure.md` `key` + `mode` and `M:` to `time_sig`.
2. At most one `V:` line (none is normal).
3. One `%%section <Label>` line per section, in `structure.md` order, labels character-identical to the structure table. The ordered list must equal the table.
4. Under each section: exactly `bars` bars of music, written as one **music line** per lyric line (per `meter_spec` entry), each ending with `|`. Bars are separated by `|`; a music line is allowed to hold one or more bars.
5. When `lyrics.md` exists and `song_type` is not INSTRUMENTAL: directly under every music line that carries lyric, one `w:` line. Never two `w:` lines for one music line; never a `w:` line before any music line. Sections with an empty `meter_spec` carry no `w:` lines.
6. `%` comment lines are allowed anywhere after `K:`; `%%section` is the only directive the gate reads.

## Note grammar (the accepted subset)

- Note: `[^ _ =]? [A-G a-g] [, ']* <duration>` where `C` is middle C (MIDI 60), `c` the octave above (72), `C,` the octave below (48), `c'` two above (84).
- Duration relative to `L:1/8`: none = 1 unit (an eighth), `2` = a quarter, `4` = a half, `8` = a whole bar in 4/4, `/2` or `/` = a sixteenth, `3` = dotted quarter, `3/2` = dotted eighth.
- Rest: `z` with the same durations (`z2`, `z4`). Rests carry no `w:` token.
- Tie: `-` directly after a note, to the same pitch next: `A2-A2` is one sung head.
- Bar lines: `|`, `||`, `|]`; repeats `|:` `:|` are parsed but write every section out in full anyway (the bar count is literal).
- Also parsed and ignored for alignment: chord symbols in quotes (`"D"`), slurs `( )`, broken rhythm `>` `<`, tuplets `(3`, grace notes `{ }`, decorations `!..!`. Anything else is a parse ERROR.

## `w:` token rules

`-` splits a word into syllable tokens (`win-dow`); `_` extends the previous syllable over one more note (no new token); `*` skips one note (a pickup with no syllable); `~` joins two words into one token sung on one note (`of~the`); `|` advances to the next bar. Per bar: syllable tokens + `_` + `*` = non-rest note heads (a tied-into note is not a new head). The de-hyphenated text of a section (tokens joined, `~` restored to a space) must equal the `lyrics.md` section text ignoring case and punctuation.

## Example (original; Verse 1 spec `8/uSuSuSuS; 8/uSuSuSuS`, 4 bars, key D major, 118 bpm)

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
D2 F2 D2 F2 | E2 G2 F2 E2 |
w: A key, a map, | a bor-rowed town |
```

Bar 1 has 5 heads and 5 tokens (`I count the num-bers`); bar 2 has 3 heads and 3 tokens.

## Forbidden content

- Real artist names or song titles in `T:` or comments; a title that differs from `concept.md.title`.
- A second voice, a `V:` pair, chords as notes (`[DF#A]`), lyrics not in `lyrics.md`, a `w:` line that paraphrases.
- Any pitch outside `vocal_range` (default MIDI 55-79: `G,` to `g`); any interval between consecutive heads above `max_melodic_leap` (default 12).
- Markdown fences, headings, or a `[Label]` tag (sections are `%%section` lines here).

## Gates run against this file

| Script | Invocation | PASS when |
|--------|------------|-----------|
| `abc_validate.py` | `abc_validate.py --json melody.abc structure.md lyrics.md brief.md` | parses; headers present, at most one `V:`; `K:`/`M:` equal `structure.md`; section list equal; `metrics.max_leap` <= `max_melodic_leap`; pitches within `vocal_range`; every bar's tokens equal its heads; every section's text equals the lyric |
| `structure_check.py --consistency` (Stage 6) | `structure_check.py --consistency --json structure.md chords.md melody.abc arrangement.md` | `K:`, `Q:`, `M:` equal the structure header; `%%section` list equal; range within `vocal_range` |

Alignment reports `metrics.alignment_skipped: 1` for INSTRUMENTAL or when `lyrics.md` is not supplied; every other check still runs. A violation's `location` is `<Label>:<bar>`.

## Max length

160 lines.

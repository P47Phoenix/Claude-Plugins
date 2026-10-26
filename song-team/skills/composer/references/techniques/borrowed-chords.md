---
loaded_by: harmony
level: L3
last_reviewed: 2026-10-26
---

# Technique: Borrowed Chords (spending the non-diatonic budget)

A borrowed chord takes a degree from the parallel mode (major borrows from minor and the reverse) or from a neighbouring key. Each one costs a cell of `diatonic_ratio`; each one, placed well, is the moment the listener feels the song turn. Place them where the arc turns and nowhere else.

## How the gate spells accidentals

A numeral with `b` or `#` is spelled against the **major** scale of the tonic and shifted by a semitone, whatever the mode. So in any key: `bII` is one semitone above the tonic, `bIII` three, `bVI` eight, `bVII` ten, `#iv` six. In a major key these are all non-diatonic. In natural minor, `III`, `VI`, `VII` with no accidental already name the flattened degrees, so write them plain; `bVI` in minor parses and resolves to the same pitch but reads as a major-key habit. `V` (major) in minor and `#vii°` are the raised-leading-tone borrowings and cost a cell each.

## Safe borrowings in a major key

| Chord | From | Sound | Where it works |
|-------|------|-------|----------------|
| `iv` | parallel minor | wistful, darkens the plagal close | the last two bars of a chorus (`iv I`), a bridge opening |
| `bVII` | mixolydian | rock lift, no leading tone | before `I` at a section end (`bVII I` is a recognised cadence); verse of a rock or folk song |
| `bVI` | parallel minor | wide, cinematic | the bridge (`bVI bVII I` is three cells and lands on home) |
| `bIII` | parallel minor | sudden brightness in the wrong place | one cell in a bridge; never in a verse |
| `ii°` | parallel minor | fragile pre-dominant | replacing `ii` once before a final `V` |
| `V/V` (write `II`) | secondary dominant | pull toward `V` | the bar before a pre-chorus `V`; counts as non-diatonic (`II` major is not `ii`) |
| `V/vi` (write `III`) | secondary dominant | pull toward `vi` | the bar before a deceptive `vi` |

## Safe borrowings in a minor key

| Chord | From | Sound | Where it works |
|-------|------|-------|----------------|
| `V` (major) | harmonic minor | the leading tone appears; the close hardens | the last two bars of a chorus or bridge (`V i`); budget one per section |
| `IV` (major) | dorian | brighter subdominant | a verse that wants motion without leaving minor |
| `bII` | phrygian | dark, half-step lean | the bar before `i` in a bridge; one cell |
| `I` (major) | picardy | the final chord only | the last cell of the song |

## Budget worked example (VCVCBC, 8-bar sections, 48 cells, threshold 0.6)

Allowed out of mode: 19 cells. Spent: bridge `| bVI | bVII | I | V |` twice (4 non-diatonic cells), final chorus `| IV | iv | I | I |` (1), pre-chorus `| ii | II | V | V |` twice (2). Total 7 of 48; ratio 0.854. Every other section stays diatonic and the song still has three distinct colours.

## Spending rules

1. The first chorus is diatonic. The listener needs to learn home before you leave it.
2. One borrowing per section, except the bridge, which takes up to three.
3. A borrowed chord arrives on a strong bar (bar 1 or bar 3 of a four-bar phrase) and resolves by step: `bVI` to `bVII` or `V`; `iv` to `I`; `bVII` to `I`; `II` to `V`.
4. Never stack two borrowed chords that move by whole step in root position (`bVI bVII`) unless you accept the parallel-fifths warning; a slash bass on the second (`bVII/3`) clears it.
5. When the critique says a section is "unstable" or "the key is unclear", remove the borrowing nearest the section's start, not its end.
6. A genre file's `diatonic_min_ratio` override changes the budget, not these rules.

## Reading a ratio FAIL

`violations[]` lists every non-diatonic cell by `<Label>:<line>:<cell>` and a final row with `observed` ratio and `limit`. Cells needed = ceil(limit x total) minus diatonic count. Return that many cells to the mode, choosing the ones in verses first, then pre-choruses, then choruses; keep the bridge's borrowings until last.

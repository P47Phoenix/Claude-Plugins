---
loaded_by: harmony
level: L3
last_reviewed: 2026-10-26
---

# Technique: Functional Harmony (the way the gate hears it)

`chord_tools.py` knows three things: which chords are diatonic to the mode, which pairs of adjacent chords are a cadence, and which pairs move in parallel. Write for the ear, then check against these three.

## Degrees and their jobs

| Degree (major) | Triad | Function | Typical next |
|----------------|-------|----------|--------------|
| `I` | major | tonic, home | anything |
| `ii` | minor | pre-dominant | `V`, `IV`, `vii°` |
| `iii` | minor | tonic substitute, soft | `vi`, `IV` |
| `IV` | major | pre-dominant, lift | `V`, `I`, `ii` |
| `V` | major | dominant, pull home | `I`, `vi` (deceptive) |
| `vi` | minor | relative minor, tonic substitute | `IV`, `ii`, `V` |
| `vii°` | dim | dominant substitute | `I`, `iii` |

In natural minor the diatonic set is `i ii° III iv v VI VII`. Write them exactly that way: `VI` and `VII` without a `b`, because the gate resolves a plain numeral against the **mode's** scale. `bVI` in A minor is F major too, but the gate spells accidental numerals against the major scale, so `bVI` and `VI` coincide in minor while `VI` alone is the idiomatic spelling. `V` (major) in minor is the raised-leading-tone dominant; it is **not** diatonic to the natural-minor table and costs one cell of the ratio. Budget it.

## Cadences the gate recognises

The last two cells of every section are checked by root degree, ignoring quality:

| Cadence | Cells | Feel |
|---------|-------|------|
| authentic | `V` then `I` (or `v`-`i`) | closed, final |
| plagal | `IV` then `I` | soft close, hymn-like |
| deceptive | `V` then `vi` | the section lifts instead of landing |
| modal | `bVII` then `I` | rock and folk close without a leading tone |

Any other final pair (`ii V`, `I IV`, `vi IV`) emits a warning. A pre-chorus that ends on `V` to launch the chorus is a deliberate half cadence; keep it and name it in `SUMMARY`. Never append a throwaway `V I` to a section that means to stay open.

## The parallel-fifths heuristic

Two consecutive root-position major or minor triads whose roots lie a whole step apart (`IV V`, `V IV`, `bVII I`, `I ii`, `ii iii` with no slash bass) trigger a warning, because block voicings of such pairs move every voice in parallel. Three ways to keep the progression and lose the warning: put the second chord over a different bass (`IV V/3`), insert a passing chord (`IV ii V`), or let the pair stand and expect the warning (`IV V I` is the most common cadence approach in pop and the warning is advisory).

## Diatonic ratio budgeting

`metrics.diatonic_ratio` = diatonic cells / all cells; `%` repeats count. With the default threshold 0.6 and a 40-cell song, 16 cells are allowed out of the mode. In practice:

| Song | Cells | Non-diatonic budget at 0.6 | Spend it on |
|------|-------|----------------------------|-------------|
| VCVCBC, 8-bar sections | 48 | 19 | the bridge (8) and the final chorus turnaround (2) |
| jingle, 8 bars | 8 | 3 | one `bVII` or one `V/V` before the last hook |
| AABA, 32 bars | 32 | 12 | the B section (8) |

A verse that borrows is a verse the critic will call unstable; keep the verse diatonic and let the bridge move.

## Section templates (original, Roman numerals, one line = four bars)

```text
Verse (major):      | I | V | vi | IV |      | I | V | IV | I |
Verse (minor):      | i | VI | III | VII |   | i | iv | v | i |
Pre-chorus:         | ii | IV | V | V |       (half cadence by design)
Chorus (lift):      | IV | I | V | vi |      | IV | I | V | I |
Bridge:             | vi | IV | I | V |      | vi | IV | V | I |
Turnaround:         | I | vi | ii | V |
```

Open the chorus on a chord the verse never opened on (`IV` when the verse opened on `I`); open the bridge on `vi` or a borrowed chord; return to `I` on the first beat of the final chorus.

## Reading a `chord_tools.py` result

- `status: ERROR`, `location: <Label>:<line>:<cell>`: the cell does not parse. Rewrite that cell in the grammar (`I9` -> `Iadd9`, `N.C.` -> the chord the bass implies, `Vsus` -> `Vsus4`).
- `violations[].reason: non-diatonic chord 'bVI' in D major`: one row per out-of-mode cell, plus one summary row with the ratio. Return the cheapest cells to the mode first (a `V/V` becomes `ii`, a `bVII` becomes `IV`).
- `warnings[]` with `possible parallel fifths` or `section does not end on a cadence`: advisory; mention each one in `SUMMARY` with the reason it stays.
- `concert`: the gate's own spellings per chart line; copy them onto the `>` lines when yours differ.

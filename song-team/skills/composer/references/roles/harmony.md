---
loaded_by: harmony
level: L2
last_reviewed: 2026-10-26
---

# Role: harmony

## Mission

Write the chord chart for every section in `structure.md`: Roman numerals in the key and mode the groove role fixed, one bar per cell, with concert-pitch spellings underneath. The chart is the harmonic floor the melody role builds on, so it is decided before a note is written and it never changes the key, mode, bar count, or section list. A chart that sounds adventurous but fails the diatonic ratio has failed; a chart that passes but gives every section the same four cells has also failed, because the critic will say so.

## Inputs

- `structure.md`: `key`, `mode`, `bpm`, `time_sig`, and the table (`label`, `bars`, `meter_spec`). Bars per section are the cell count you must produce.
- `brief.md`: `genre`, `mood`, `must_avoid[]`, `target_length_sec`.
- `concept.md`: `arc` (which section carries the turn) and `central_image`; `motif` for INSTRUMENTAL.
- `genres/<g>.md`: common progressions, typical keys, feel, and any `diatonic_min_ratio` override.
- `techniques/functional-harmony.md` and `techniques/borrowed-chords.md`.
- On re-dispatch: the music-judge critique and the `chord_tools.py` gate JSON.

## Process

1. Copy the header: `key: <key> <mode>` exactly as `structure.md` spells them (`key: D major`, `key: A minor`). The gate reads the key from `structure.md` first; a mismatch here is a Stage 6 consistency failure later.
2. For each section, in `structure.md` order, write one `[Label]` block whose cell count equals `bars`. Use one chart line per phrase of four cells (or the bar count when smaller); never split a bar across cells.
3. Assign a harmonic job per section from the arc: verses sit on I and its neighbours (`I vi IV V`, `I V vi IV`, `ii V I`), the chorus opens on the strongest degree the genre file names (I or IV), the bridge starts somewhere the chorus never started (vi, IV, or a borrowed chord).
4. End every section on a cadence the gate recognises: `V-I`, `IV-I`, `V-vi`, or `bVII-I`. A section that ends on V by design (a pre-chorus) is allowed, but say so in `SUMMARY`; the gate emits a warning, not a FAIL.
5. Budget non-diatonic chords. With `diatonic_min_ratio` 0.6 and 32 cells, at most 12 cells leave the mode. Spend them in one place (a bridge, the final chorus) so they mean something; `techniques/borrowed-chords.md` lists the safe borrowings per mode.
6. Avoid adjacent root-position triads a whole step apart (`IV V`, `V IV`, `bVII I`) in block voicings when a slash bass or a passing chord serves as well; the gate warns on them. When the genre wants `IV V I` (it often does), keep it and expect the warning.
7. Write `%` only to repeat the previous cell inside the same chart line; it counts as a chord for the ratio.
8. Spell concert chords on the `>` line under each chart line: sharp keys with sharps, flat keys with flats, slash bass after `/`. The gate ignores these lines but the arranger and `midi_export.py` read them.
9. Re-read `must_avoid[]`: a brief that says "no minor key" or "no sevenths" binds you.
10. Write `chords.md` per the contract. No prose inside section blocks; comments start with `#`.

## What the gate measures

- `chord_tools.py chords.md structure.md`: parses every cell (`I..vii`, `b`/`#` prefix, `dim aug 7 maj7 m7 sus2 sus4 add9`, `/bass`); `metrics.diatonic_ratio` = diatonic cells / all cells, FAIL below `diatonic_min_ratio` (default 0.6, equal passes). ERROR on an unparseable cell (`Imaj9`, `N.C.`, lower-case `b` on a lower-case numeral is fine, `♭` is not).
- Warnings (counted in `metrics.warnings`, never FAIL): parallel-fifths heuristic on whole-step root motion between root-position triads; a section whose last two cells form no recognised cadence.
- `music-judge` (critic, after the script): section contrast, whether the chorus opens differently from the verse, whether borrowed chords land on the arc's turn.

## Common failure modes

| Failure | Why it happens | Fix |
|---------|----------------|-----|
| Cell count differs from `bars` | Phrase written as 4 cells for an 8-bar section | Write two chart lines, or `%` repeats, to reach the bar count |
| ERROR on a cell | Symbol outside the grammar (`N.C.`, `I9`, `Vsus`) | Use the nearest cell in the grammar (`I`, `Iadd9`, `Vsus4`) |
| Ratio below 0.6 | Borrowed chords in every section | Return the verses to diatonic; keep borrowings for one section |
| Minor-key chart uses major-key numerals | `VI` and `VII` written as `bVI`/`bVII` in minor | In minor, `VI` and `VII` are already the diatonic degrees; the `b` prefix shifts them against the major scale |
| Every section identical | Chart written once and pasted | Change the opening chord of the chorus and the bridge |
| Key differs from `structure.md` | Transposed for singability | Never; the groove role owns the key, propose a change in `SUMMARY` |

## What to return

Write `chords.md` to the artifact path. Reply with the four-line hand-back exactly as the prompt's `## Return` block specifies. In `SUMMARY`, state the diatonic ratio you counted, every non-diatonic cell with its location, every section that ends off-cadence by design, and any key or tempo you believe the melody role will struggle with (the orchestrator opens a debate when harmony and melody disagree). Never state that a gate passed.

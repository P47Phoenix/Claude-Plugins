---
loaded_by: instrumentation
level: L2
last_reviewed: 2026-10-26
---

# Role: instrumentation

## Mission

Decide who plays in every section and when each part enters and leaves, so that the song's form is audible from the texture alone. Write the first version of `arrangement.md`: the header, the section column, `instruments_in`, `instruments_out`, `texture_note`, and a provisional `energy` for each row. The `dynamics` role finalises the energy after you; your job is the palette and the entry order that make a rising curve possible.

## Inputs

- `brief.md`: genre, mood, audience, `target_length_sec`, `must_avoid[]` (an instrument the brief excludes stays out).
- `structure.md`: the header (copy it exactly) and the section table (labels, order, bar counts). The `meter_spec` tells you where the vocal is busy, which is where the band stays out of the way.
- `chords.md`: harmonic rhythm per section (one chord per bar leaves room for a moving bass; two per bar wants a simpler bass).
- `melody.abc`: the vocal range per section (`%%section` markers). Nothing doubles the melody in its own register during a verse; a chorus may double it an octave up.
- `genres/<g>.md`: the palette, the usual entry order, and the tropes to use or avoid.
- `techniques/section-contrast.md`: how to make consecutive sections differ.

## Process

1. Copy the four header lines from `structure.md` character for character. Copy the `label` column into the `section` column in order, one row per structure row, before writing anything else. Never retype a label from memory.
2. Choose the opening palette: two to four parts that carry the first section alone. The first row's `instruments_in` lists them; its `instruments_out` is `-`.
3. Choose the full palette for the loudest chorus: everything that will ever play. Every part in it must enter in some row; the difference between step 2 and step 3 is your budget of entries.
4. Spend the entries across the sections so that each chorus adds at least one part the previous chorus did not have, and each verse after a chorus removes or thins at least one part (`instruments_out`), then brings it back.
5. Give the bridge its own texture: remove the kit or the main chordal instrument, or hand the lead to a different instrument, so the final chorus is heard as a return.
6. Write `texture_note` per row: density, space, and feel in technical words (`sparse, dry single vocal`, `half-time feel, pad filtered`, `wide, doubled lead`). Under 90 characters. Mention bar numbers for mid-section entries (`bass enters bar 5`).
7. Fill a provisional `energy` per row: 1-10, rising with the number of parts and their register, the verse below the next chorus, the final chorus highest. Write `# energy: provisional` on its own line between the header and the table so the `dynamics` role knows it may change the column.
8. Check the table against `melody.abc`: no doubling instrument sits inside the vocal's register in a verse; the busiest `meter_spec` lines get the thinnest accompaniment.
9. Check every instrument named in an `instruments_out` cell actually entered in an earlier row; check nothing enters twice without leaving in between.
10. Write the file. State the opening and peak palettes in `SUMMARY`.

## What the gate measures

- `structure_check.py --consistency`: the four header fields equal `structure.md` as strings; the `section` column equals the structure's label list in order. A missing row, an extra row, or `Chorus 2` for `Chorus` fails. This is the gate that catches the most arrangement attempts, and it is always a copy error.
- `arrangement_check.py`: runs after the `dynamics` role finalises `energy`. Your provisional values are a starting point, but write them so they would already pass `chorus_rising`: verse below the next chorus, choruses never falling, the global maximum in the last chorus or the bridge, and an outro below the peak.
- Downstream, `midi_export.py` maps `instruments_in` names to program numbers. Use plain instrument names (`acoustic guitar`, `electric bass`, `synth pad`, `strings`, `piano`, `kick`, `snare`, `hi-hat`, `shaker`, `tambourine`, `backing vocals`), not brands or models.

## Common failure modes

| Failure | Why it happens | Fix |
|---------|----------------|-----|
| Header differs (`118 bpm`, `D major`) | Values retyped with units | Copy the four lines verbatim from `structure.md` |
| Section count differs | Repeated `Chorus` collapsed into one row | One row per structure row, even when identical |
| Everything enters in Verse 1 | Palette chosen for the chorus and used from bar 1 | Hold back at least half the palette until the first chorus |
| Nothing ever leaves | Entries only | Every verse after a chorus and every bridge has an `instruments_out` |
| Doubling the melody in a verse | Guitar or synth line written in the vocal's register | Move it an octave away or give it a counter-line |
| Bridge is a quieter chorus | Same palette, lower energy | Change the palette, not only the level |
| Brand or model name | Habit | Plain instrument names only |

## What to return

Write `arrangement.md` to the artifact path. Reply with the four-line hand-back from the prompt's `## Return` block. In `SUMMARY`: the opening palette, the peak palette, which section carries the bridge contrast, the provisional energy list in order, and any instrument you excluded because of `must_avoid[]`. Never state that a gate passed.

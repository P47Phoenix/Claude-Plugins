---
loaded_by: instrumentation, dynamics
level: L2
last_reviewed: 2026-10-26
---

# Output Contract: arrangement.md (arrangement map)

Normative grammar: `references/shared/artifact-formats.md` section `arrangement.md`. Normative gate rules: `references/shared/stage-gates.md` (`arrangement_check.py`, `structure_check.py --consistency`). This contract restates both for the `instrumentation` and `dynamics` roles.

## File

Path: `.song/<slug>/arrangement.md` (the prompt states the exact path). UTF-8, LF line endings, Markdown. No front-matter, no title heading.

## Structure

1. **Header**: four `key: value` lines, first in the file, no blank line between them, copied character for character from `structure.md`:
   ```text
   key: D
   mode: major
   bpm: 118
   time_sig: 4/4
   ```
   `structure_check.py --consistency` compares each field as a string. `D` is not `D major`; `118` is not `118 bpm`; `4/4` is not `4 / 4`. Do not add `form_template` or any other key.
2. One blank line, then **one table** with exactly these columns in this order:
   ```text
   | section | energy | instruments_in | instruments_out | texture_note |
   |---------|--------|----------------|-----------------|--------------|
   ```
3. One row per section of `structure.md`, in the same order, with `section` equal to the `label` column of `structure.md` **character for character**. `Chorus` appears as many times as the structure lists it; `Pre-Chorus 1` keeps its hyphen and its number. Do not number, merge, or rename repeated sections.
4. `energy`: an integer from 1 to 10 with no decoration (`7`, never `7/10`, `~7`, or `high`). Every row has one.
5. `instruments_in`: comma-separated list of instruments or vocal parts that **enter** in this section, or `-` when nothing enters. `instruments_out`: the same for parts that **leave**. An instrument is never listed in both cells of one row. The first row's `instruments_in` is the opening palette.
6. `texture_note`: one phrase, under 90 characters, describing density, space, and feel in technical words (sparse, dry, wide, doubled, half-time, filtered, staccato). No sentences about meaning or emotion.
7. Optional comment lines starting with `# ` may sit between the header's blank line and the table. The `instrumentation` role writes `# energy: provisional` there; the `dynamics` role deletes it. Gates ignore comment lines.
8. Nothing after the table.

## Who writes which column

| Role | Writes | Must leave byte-identical |
|------|--------|---------------------------|
| `instrumentation` | header, `section`, `instruments_in`, `instruments_out`, `texture_note`, provisional `energy` | - (first writer) |
| `dynamics` | `energy` (final); whole table when no `arrangement.md` exists | header, `section`, `instruments_in`, `instruments_out`, `texture_note` |

## Energy checklist (`chorus_rising`, the default `quality.energy_curve`)

Let `C1..Cn` be the chorus energies in order and `G` the global maximum. `Chorus` and `Drop` rows are chorus-role; `Bridge` and `B` are bridge-role; `Verse N` and `A1`/`A2`/`A3` are verse-role; every other label (`Intro`, `Pre-Chorus N`, `Build`, `Breakdown`, `Outro`, `Tag`, `Instrumental`, `Post-Chorus`) is neutral. Tick every box before writing the file:

- [ ] **(a)** Each chorus-role energy is `>=` the previous chorus-role energy. `7, 8, 9` passes; `7, 9, 8` fails at the third chorus.
- [ ] **(b)** `G` occurs in the final chorus-role section or in a bridge-role section (ties count). A peak only in a pre-chorus or outro fails.
- [ ] **(c)** The final section's energy is `< G` unless the final section **is** the last chorus. An `Outro` at `G` fails; an outro one below passes.
- [ ] **(d)** Every verse-role energy is strictly `<` the energy of the next chorus-role section after it. Equal fails. A verse with no chorus after it is unconstrained.
- [ ] Every value is an integer 1-10 (an `ERROR`, not a FAIL, otherwise).
- [ ] With no chorus-role section at all, the script applies `strict_rising` instead: non-decreasing up to the first `G`, non-increasing after it.

`strict_rising` (when configured) ignores roles and checks only the single-peak shape. `free` always passes and reports metrics.

### Worked example: passes (the plan's Appendix A curve)

Form `V1 PC C V2 PC C B C C` (a VCVCBC with a repeated final chorus):

| Verse 1 | Pre-Chorus 1 | Chorus | Verse 2 | Pre-Chorus 2 | Chorus | Bridge | Chorus | Chorus |
|---|---|---|---|---|---|---|---|---|
| 3 | 5 | 7 | 4 | 6 | 8 | 5 | 9 | 9 |

(a) choruses `7, 8, 9, 9` never fall. (b) `G = 9` sits in the final chorus. (c) the final section is the last chorus. (d) Verse 1 `3 < 7`, Verse 2 `4 < 8`. PASS.

### Worked example: fails (a flat curve)

Same form, every section at `5`:

| Verse 1 | Pre-Chorus 1 | Chorus | Verse 2 | Pre-Chorus 2 | Chorus | Bridge | Chorus | Chorus |
|---|---|---|---|---|---|---|---|---|
| 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 |

(a), (b), (c) pass because ties count. (d) fails twice: Verse 1 `5` is not below the next chorus `5`, and Verse 2 `5` is not below `5`. The gate reports `location: "Verse 1"` and `location: "Verse 2"` with `observed: 5, limit: 5`. A curve with no contrast is never an arrangement.

## Example file (original; FULL_SONG shape, 8 sections)

```markdown
key: D
mode: major
bpm: 118
time_sig: 4/4

| section | energy | instruments_in | instruments_out | texture_note |
|---------|--------|----------------|-----------------|--------------|
| Verse 1 | 3 | acoustic guitar, bass | - | sparse, dry single vocal, light hi-hat only |
| Pre-Chorus 1 | 5 | kick, snare, electric guitar | - | build on straight eighths, bass walks up |
| Chorus | 7 | drums, synth pad, vocal doubles | - | wide stereo, doubled lead, pad under the hook |
```

## Forbidden content

- Real artist names, band names, producer names, song titles, or any entry on `references/shared/blocked-targets.txt`.
- The strings "sounds like", "reference track", "in the style of".
- Brand or product names for instruments or plug-ins (write `tube-style compressor`, not a model name).
- Section labels not in `structure.md`; rows outside the table; a second table.
- Energy written as a range, a word, or a decimal.

## Gates run against this file

| Script | Invocation | PASS when |
|--------|------------|-----------|
| `arrangement_check.py` | `arrangement_check.py --json arrangement.md` | the energy checklist above holds for the configured `energy_curve` |
| `structure_check.py` | `structure_check.py --json --consistency structure.md lyrics.md chords.md melody.abc arrangement.md` | header fields equal `structure.md`; the `section` list equals the structure's label list in order |

Neither script is ever SKIPPED. Severity order: `ERROR > FAIL > SKIPPED > PASS`.

## Max length

40 lines including header, comments, and the table.

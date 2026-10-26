---
loaded_by: composer
level: L2
last_reviewed: 2026-10-26
---

# Structure Output Contract: `structure.md`

Owner: `groove`. Validated by `structure_check.py structure.md` (Stage 3) and `structure_check.py --consistency` over all present artifacts. The grammar is the one in `references/shared/artifact-formats.md`.

## Grammar

```markdown
key: <Tonic>
mode: <mode>
bpm: <integer>
time_sig: <n/d>
form_template: <template name>

| section | label | bars | meter_spec | rhyme_scheme |
|---------|-------|------|------------|--------------|
| 1 | <Label> | <int> | <spec> | <letters> |
```

- **Header** is five `key: value` lines, then a blank line, then one pipe table with exactly the five columns above.
- `key` is a tonic with accidental (`D`, `Bb`, `F#`). `mode` is a full mode name (`major`, `minor`, `dorian`, `mixolydian`, `lydian`, `phrygian`, `locrian`). `bpm` is an integer quarter-note tempo. `time_sig` is `4/4`, `3/4`, `6/8`, and so on.
- `form_template` is a name from `scripts/data/form-templates.json` (for example `VCVCBC`, `jingle`). Its label patterns, per-section bar ranges, and total-bar cap decide PASS or FAIL.
- **`section`** is the 1-based row number. **`label`** is from the allowed set: `Intro`, `Verse N`, `Pre-Chorus N`, `Chorus`, `Post-Chorus`, `Bridge`, `Instrumental`, `Breakdown`, `Build`, `Drop`, `Tag`, `Outro`, `A1`, `A2`, `B`, `A3`. A repeated chorus is a new row labelled `Chorus`.
- **`bars`** is the section length in bars (integer).
- **`meter_spec`** is `syllables/stress` per lyric line, lines separated by `;`. Stress is a string of `S` (stressed) and `u` (unstressed), one character per syllable, so `8/uSuSuSuS` is eight syllables. Example for a four-line verse: `8/uSuSuSuS; 8/uSuSuSuS; 8/uSuSuSuS; 8/uSuSuSuS`.
- **`rhyme_scheme`** is letters per line, scoped to the section: `ABAB`, `AABB`. `x` marks an unconstrained line (`AxAx`).
- INSTRUMENTAL leaves `meter_spec` and `rhyme_scheme` empty. Non-lyric sections (Intro, Instrumental, Outro) also leave them empty.

## Rules the gate enforces

1. Section labels in order match the `form_template` label patterns; unknown template is an ERROR.
2. Every section's `bars` is inside the template's range; total bars do not exceed the cap.
3. `--consistency`: `lyrics.md` section tags equal the labels, the lyric line count per section equals the number of `meter_spec` lines, `chords.md` and `melody.abc` use the same labels and agree on key, mode, bpm, and time signature.

## Choosing values

| Field | Guidance |
|-------|----------|
| `bpm` | Take the genre profile `## Rhythm` tempo range; ballads sit in the lower third, dance material in the upper third |
| `time_sig` | The genre meter (4/4 default); 3/4 or 6/8 when the brief says waltz or lilt |
| `key` and `mode` | Mood and vocal range: minor or dorian for wistful, major or mixolydian for open and bright; pick the key that keeps the hook inside the vocal range |
| `bars` | 8 for verse and chorus, 4 for pre-chorus, 4-8 for bridge; keep totals near `target_length_sec` (bars x beats x 60 / bpm) |
| `meter_spec` | Real per-line syllable counts a singer can fit in the section's bars; vary line lengths slightly between verse and chorus |

## Example

```markdown
key: D
mode: major
bpm: 118
time_sig: 4/4
form_template: VCVCBC

| section | label | bars | meter_spec | rhyme_scheme |
|---------|-------|------|------------|--------------|
| 1 | Verse 1 | 8 | 8/uSuSuSuS; 8/uSuSuSuS; 8/uSuSuSuS; 8/uSuSuSuS | ABAB |
| 2 | Chorus | 8 | 7/SuSuSuS; 7/SuSuSuS; 7/SuSuSuS; 8/SuSuSuSu | AABB |
```

## Hand-back

```text
SKILL_LOADED: <paths>
STATUS: DONE | BLOCKED
ARTIFACT: <dir>/structure.md
SUMMARY: <one sentence, max 200 characters; key, mode, bpm, form template>
```

On BLOCKED add `FINDINGS:` bullets (no template fits the brief's length, supplied lyric cannot be sectioned).

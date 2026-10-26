---
loaded_by: song-flow
level: L2
last_reviewed: 2026-10-26
---

# Groove stub (Stage 3-light, Wave 2 only)

> **DELETE IN W3-2.** This file and the `## Stage 3: Structure (light)` section of
> `SKILL.md` are a placeholder for `composer:groove`. When W3-2 lands, Stage 3 dispatches
> the real role with `subagent_type: composer`, `owners["structure.md"]` becomes `groove`,
> and this file is removed. Nothing here is a design decision about music.

The stub is a deterministic fill of `structure.md` from one entry in
`song-team/scripts/data/form-templates.json`. It is the one exception to "the orchestrator
never writes the song", tolerated because its output is a meter spec and a bar count, not
a lyric, chord, or melody, and because `structure_check.py` still gates it.

## Algorithm

1. **Pick the template.** `JINGLE` -> `jingle`; every other type routed here -> `VCVCBC`.
   (`brief.md` carries no `form_template` key in v1; the choice is by song type only.)
2. **Expand the label sequence** from the per-template table below. The expansion is the
   template's required groups (`min_repeat >= 1`) in order, each repeated `min_repeat`
   times, with one deliberate addition for `jingle` (a `Verse 1` and second `Chorus`,
   both optional in the template, so the lyric has somewhere to go).
3. **Bars** = the group's `min_bars`.
4. **meter_spec** = `default_meter[<kind>]`, where `<kind>` is the label with any trailing
   space-digit removed (`Verse 1` -> `Verse`, `Pre-Chorus 2` -> `Pre-Chorus`, `Chorus` -> `Chorus`).
   **Chorus line 1 is derived from the hook**: the `concept.md.hook_line` IS chorus line 1, so run
   `python -I -c "import sys; sys.path.insert(0, r'<PLUGIN>/scripts'); import prosody_check as p; h='<hook_line>'; print(len(p.stress_pattern(h)), p.stress_pattern(h))"`
   (output `<n> <pattern>`) and write `<n>/<pattern>` as the first `;`-item of every
   Chorus row; the remaining chorus lines keep the template default. The lyric gate then
   measures the chorus against the hook's own stress, and `verse-writer` places the hook
   verbatim on that line. If `lyric-editor` later changes the hook, song-flow updates
   `concept.md.hook_line`, re-runs the Stage 2 gates, and appends a `decisions.md` entry.
5. **rhyme_scheme** = the kind's pattern from the table below, cycled to the number of
   `;`-separated lines in `meter_spec` (2 lines -> first two letters). An empty
   `meter_spec` gets an empty scheme. Length must equal the line count or `rhyme_check.py` errors.
6. **Header**: `key` = `default_key` (`C`), `mode: major`, `bpm` = integer midpoint of
   `tempo_band` (`(lo + hi) // 2`), `time_sig` = `default_time_sig` (`4/4`),
   `form_template` = the template name.
7. Write `.song/<slug>/structure.md` in the exact `artifact-formats.md` grammar: the five
   header lines, a blank line, the table with header `| section | label | bars | meter_spec | rhyme_scheme |`.
   No comment lines anywhere in the file (`parse_header_keys` reads the top of the file verbatim).
8. Record `owners["structure.md"] = "groove-stub"` in `state.json`. That string, not a file
   comment, is how a later reader knows the artifact was stubbed.

## Rhyme pattern per label kind

| Kind | Pattern | 2-line result | 4-line result |
|------|---------|---------------|---------------|
| Verse | `ABAB` | `AB` | `ABAB` |
| Pre-Chorus | `AABB` | `AA` | `AABB` |
| Chorus | `AABB` | `AA` | `AABB` |
| Bridge | `AABB` | `AA` | `AABB` |
| Post-Chorus, Tag | `AA` | `AA` | `AAAA` |
| Intro, Instrumental, Outro | (empty) | (empty) | (empty) |

`Bridge` uses `AABB` rather than `ABAB` because the VCVCBC default bridge meter has two
lines, and a two-line `AB` constrains nothing.

## Per-template expansion

| Template | Expansion (label: bars) | bpm | Lines per section |
|----------|-------------------------|-----|-------------------|
| `VCVCBC` | Verse 1: 4, Chorus: 4, Verse 2: 4, Chorus: 4, Bridge: 4, Chorus: 4 | 112 | verse 4, chorus 4, bridge 2 |
| `jingle` | Chorus: 2, Verse 1: 2, Chorus: 2 | 130 | chorus 2, verse 2 |

Total bars: VCVCBC 24; jingle 6 (cap 16). Both pass `structure_check.py` as written.

## Worked output (`VCVCBC`, verified PASS on 2026-10-26)

Shown with the template default on Chorus line 1; with hook `Nobody knows my name here yet`
step 4 prints `8 SuuSuSSS` and every Chorus row begins `8/SuuSuSSS;` instead of `7/SuSuSuS;`.

```markdown
key: C
mode: major
bpm: 112
time_sig: 4/4
form_template: VCVCBC

| section | label | bars | meter_spec | rhyme_scheme |
|---------|-------|------|------------|--------------|
| 1 | Verse 1 | 4 | 8/uSuSuSuS; 8/uSuSuSuS; 8/uSuSuSuS; 8/uSuSuSuS | ABAB |
| 2 | Chorus | 4 | 7/SuSuSuS; 7/SuSuSuS; 7/SuSuSuS; 8/SuSuSuSu | AABB |
| 3 | Verse 2 | 4 | 8/uSuSuSuS; 8/uSuSuSuS; 8/uSuSuSuS; 8/uSuSuSuS | ABAB |
| 4 | Chorus | 4 | 7/SuSuSuS; 7/SuSuSuS; 7/SuSuSuS; 8/SuSuSuSu | AABB |
| 5 | Bridge | 4 | 8/uSuSuSuS; 8/uSuSuSuS | AA |
| 6 | Chorus | 4 | 7/SuSuSuS; 7/SuSuSuS; 7/SuSuSuS; 8/SuSuSuSu | AABB |
```

## Known limits (why W3-2 replaces this)

- Four bars for a four-line verse is the template floor, not a musical choice.
- Key C, 4/4, and the band midpoint ignore genre and mood entirely.
- The two-line bridge is thin; the real `groove` role sizes it from the arc.
- No critic loop: on a `structure_check.py` FAIL (a bug, since the fill is deterministic)
  the orchestrator applies escalation step 5 immediately rather than re-dispatching.

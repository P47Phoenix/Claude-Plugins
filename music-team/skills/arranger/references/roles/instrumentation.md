---
loaded_by: arranger
level: L2
last_reviewed: 2026-10-26
---

# Instrumentation (with dynamics and production-brief task types)

One dispatched role, `instrumentation`. The pipeline chain is `instrumentation` (task `arrangement`),
then `dynamics`, then `production-brief`; the last two are task types of this same manifest.

## Role -> Reference Mapping

| Task type | Contract | Technique files (max 2) |
|-----------|----------|-------------------------|
| **instrumentation** | arrangement-output.md | texture-and-register.md, section-contrast.md |
| **dynamics** | arrangement-output.md | energy-mapping.md, section-contrast.md |
| **production-brief** | production-brief-output.md | production-language.md, energy-mapping.md |

Genre input for every task type: the profile's `## Arrangement` and `## Rhythm` sections only.

## Detection Keywords

arrange, arrangement, instrumentation, instruments, orchestrate, who plays, layers, dynamics, energy,
build, drop, breakdown, contrast, crescendo, stripped, full band, production brief, production notes,
mix notes, tempo map, vocal treatment, stems, export MIDI

## Task Type Routing Table

| Request Signal | Task Type | References Loaded |
|---|---|---|
| "arrange this", "what instruments", "instrumentation", "who plays what", `TASK_TYPE: arrangement` | **instrumentation** | arrangement-output.md, texture-and-register.md, section-contrast.md |
| "dynamics", "energy map", "build and drop", "make the chorus lift", `ROLE: dynamics` | **dynamics** | arrangement-output.md, energy-mapping.md, section-contrast.md |
| "production brief", "production notes", "mix priorities", "tempo map", `ROLE: production-brief` | **production-brief** | production-brief-output.md, production-language.md, energy-mapping.md |

## Task Type Instructions

| Task Type | What the sub-agent does |
|---|---|
| **instrumentation** | Read `structure.md`, `chords.md`, `melody.abc`. Write the full `arrangement.md`: header copied from `structure.md`, one row per section in order, `instruments_in` / `instruments_out` per section, a draft `energy` and a `texture_note`. Pick instruments from the genre `## Arrangement` core list; add or remove no more than three per boundary |
| **dynamics** | Read the draft `arrangement.md`. Edit in place: set the final `energy` value per section on the 1-10 scale, shape the curve to `quality.energy_curve`, and rewrite `texture_note` so each note states what changes (density, register, width, vocal layers). Do not change the section list, header, or instrument columns except to fix an empty cell |
| **production-brief** | Read the finished `arrangement.md` and `structure.md`. Write `production-brief.md` with the four headings in order. Every statement is technical: tempo, meter, instrumentation, layering, effects, level and frequency decisions |

## Procedure (all task types)

1. Read the input artifacts by path; copy `key`, `mode`, `bpm`, `time_sig` verbatim from `structure.md`.
2. Use the section labels from `structure.md` exactly, in order, repeated labels included.
3. Apply the genre `## Arrangement` arc and the `## Rhythm` feel and tempo range; stay inside them unless
   the brief overrides.
4. Write the artifact to the path given. Run `arrangement_check.py` (arrangement tasks) and fix every
   violation before returning.
5. Reply with the `SKILL_LOADED:` / `STATUS:` / `ARTIFACT:` / `SUMMARY:` block.

## Guardrails

- **Technical language only** -- tempo, key, instruments, texture, dynamics, vocal treatment. Never "sounds like", never an artist, band, album, or song name, never a reference track
- **Section list is fixed** -- the table matches `structure.md` section for section; the arranger never adds, drops, or renames sections
- **Energy is relative and spans the scale** -- max minus min is at least 3 (config `quality.min_energy_range`); the final chorus is the peak unless the bridge is
- **Every cell is filled** -- `instruments_in` is never empty; `-` is allowed for `instruments_out` and, after the first section, `instruments_in`
- **Subtract to build** -- remove layers before a peak and add them back on its downbeat; contrast beats loudness
- **Vocal first** -- the lead vocal stays in the clear; no layer masks the hook line
- **Ownership** -- `dynamics` owns `arrangement.md`; `production-brief` owns `production-brief.md`; neither edits `structure.md`, `chords.md`, or `melody.abc`
- **No new lyric or melody material** -- an arrangement may thin or double what exists, never rewrite it

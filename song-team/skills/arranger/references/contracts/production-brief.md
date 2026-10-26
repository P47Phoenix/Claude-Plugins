---
loaded_by: production-brief
level: L2
last_reviewed: 2026-10-26
---

# Output Contract: production-brief.md

Normative grammar: `references/shared/artifact-formats.md` section `production-brief.md`. Normative policy: `references/shared/originality-policy.md` clause 3 and `stage-gates.md` (`validate_artifacts.py`). This contract restates both for the `production-brief` role.

## File

Path: `.song/<slug>/production-brief.md` (the prompt states the exact path). UTF-8, LF line endings, Markdown. No front-matter.

## Structure

1. Optional first line: `# Production brief: <title>` (the title from `concept.md`; omit when there is none).
2. Exactly these four `##` headings, in this order, each present even when short:
   - `## Tempo map`
   - `## Vocal treatment`
   - `## Mix priorities`
   - `## Section notes`
3. No other headings. No sub-headings. Plain paragraphs, numbered lists, and bullet lists only.

### `## Tempo map`

One paragraph. States the bpm and time signature from `structure.md` (they must match it exactly), whether the tempo is constant, every tempo or feel change by section and bar (`half-time feel from Bridge bar 1`, `ritardando over the last two bars`), any count-in, any stop, break, or held note, and the total bar count when it is known.

### `## Vocal treatment`

One or two paragraphs. Per section group (verses, pre-choruses, choruses, bridge): how many lead tracks, doubles, harmonies, or group parts; panning; reverb and delay with numbers (type, decay in seconds, pre-delay in ms, note value, wet percentage); compression ratio and attack character; de-essing, saturation, pitch treatment, or filtering. For an instrumental, state `None.` then say which instrument takes the lead role and how it is treated.

### `## Mix priorities`

A numbered list of three to five items, most important first. Each item names a concrete element and a concrete action: what sits in front, what is tucked, what is sidechained to what, which frequency band belongs to which instrument, how much quieter a section sits in dB.

### `## Section notes`

One bullet per section of `structure.md`, in order, starting with the section label and a colon. Each bullet says what enters, what leaves, and one texture or performance instruction, consistent with the matching `arrangement.md` row. Repeated sections get a distinguishing word (`Final Chorus:`) or the label with its position (`Chorus (second):`).

## Language rules

- Technical only: tempo, key, meter, instrument, register, articulation, dynamics (dB, velocity, `p`/`f` words), space (reverb, delay, width, pan), tone (bright, dark, bands in Hz or kHz), texture (sparse, dense, layered, doubled), and timing (bar, beat, note value, seconds).
- Numbers wherever a producer would want one: bpm, bars, dB, ms, Hz, kHz, ratios, percentages, note values.
- Describe the intended effect on the listener in one short clause at most (`so the hook lands`), never a comparison to another record.
- Every instruction must be executable in a DAW by someone who has never heard any other song.

## Forbidden content (the lint reads these literally)

- Any real artist, band, producer, engineer, or label name; any song, album, or film title; any entry on `references/shared/blocked-targets.txt` (whole-phrase, case-insensitive). The policy covers names not on the list.
- The strings **"sounds like"** and **"reference track"** in any case. Also avoid their relatives: "in the style of", "a la", "think of", "reminiscent of", "vibe of", "like that one song".
- Brand, model, or plug-in names for gear (write `optical-style compressor`, `spring reverb`, `tape-style saturation`).
- Quoted lyrics beyond the hook line's first three words when a section note needs to point at it.
- Era-plus-artist shorthand (`80s <name>`). Era-plus-technique is fine (`80s gated-reverb snare`).

## Example (original, abbreviated)

```markdown
## Tempo map

Constant 118 bpm, 4/4, straight eighths. No tempo changes; one-bar drum break at the end of the Bridge into the final Chorus.

## Vocal treatment

Dry single lead in the verses with a short plate (0.8 s, 20 ms pre-delay). Choruses add two stereo doubles and a 1/8-note slap delay at 15 percent wet.

## Mix priorities

1. Lead vocal intelligibility on the hook line.
2. Kick and bass locked; sidechain the pad lightly to the kick in the choruses.

## Section notes

- Verse 1: guitar and bass only, hi-hat enters bar 5.
```

## Gates and lints run against this file

| Check | When | Finding |
|-------|------|---------|
| `validate_artifacts.py` (advisory `PostToolUse` hook, lands W4-2) | on write | FAIL on any blocked-targets hit, "sounds like", or "reference track" |
| `song-critic:challenger` (Stage 7b) | release | BLOCKER row for any artist or title reference, caught by `challenge_gate.py` |
| `structure_check.py --consistency` | Stage 6 | does not read this file; the bpm and time signature here must still equal `structure.md` by inspection |

## Max length

60 lines.

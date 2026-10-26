---
loaded_by: arranger
level: L2
last_reviewed: 2026-10-26
---

# Output Contract: production-brief.md

Owner: `production-brief`. Validated by the `validate_artifacts.py` hook (blocked-targets and
"sounds like" lint) and the challenger at Stage 7b. Grammar source of truth:
`references/shared/artifact-formats.md`.

## File shape

A title line, then exactly these four headings in this order:

```text
# Production brief: <title>

## Tempo map
## Vocal treatment
## Mix priorities
## Section notes
```

## Rules

| Heading | Content |
|---------|---------|
| `## Tempo map` | `bpm`, `time_sig`, feel (straight, swung, half-time), every tempo or meter change with its bar, count-in, and any drum break or fill that bridges sections. Matches `structure.md` |
| `## Vocal treatment` | Lead processing per section family: reverb type and decay, delay time and level, doubling, harmony stacks, compression ratio, de-essing, panning. Numbers where they matter |
| `## Mix priorities` | Numbered list, most important first: what must stay clear, what locks together, which frequency bands are cut or kept for which layer, how loud the quietest section is relative to the peak |
| `## Section notes` | One bullet per section in order: `- <Label>: <what enters, what leaves, what changes>`. Mirrors `arrangement.md` rows; repeated labels get repeated bullets |

## Language rules

- Technical language only: tempo, key, instrumentation, texture, dynamics, effects, level, frequency.
- Never "sounds like", "reference track", "in the style of <artist>", or any name on
  `references/shared/blocked-targets.txt`. Genre and era labels are allowed ("straight-eighth pop
  groove at 118 bpm").
- No lyric text and no quoted existing material.
- Say what to do, not what to resemble: "plate reverb, 0.8 s decay" beats "make it airy".

## Consistency with arrangement.md

Each `## Section notes` bullet agrees with that row's `instruments_in`, `instruments_out`, and
`energy`. The quietest and loudest sections named in `## Mix priorities` match the energy map.

## Hand-back

`ARTIFACT:` the path of `production-brief.md`. `SUMMARY:` one sentence, 200 characters or fewer. Re-read
the brief for artist names and "sounds like" before replying.

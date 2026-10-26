---
loaded_by: arranger
level: L3
last_reviewed: 2026-10-26
---

# Technique: Production Language

A production brief is read by a producer or mixer who has never heard the song. Every line must be
actionable from technical terms alone. Describe parameters, not resemblance.

## Allowed vocabulary

| Area | Terms |
|------|-------|
| Time | bpm, meter, straight or swung eighths, half-time, double-time, count-in, tempo change at bar N |
| Instruments | kick, snare, hi-hat (closed, half-open, open), toms, shaker, bass guitar, synth bass, acoustic or electric guitar, piano, pad, strings, vocal doubles |
| Space | plate, room, hall; decay in seconds; pre-delay in ms; delay as note value and percent wet |
| Dynamics | compression ratio, attack, release, sidechain, limiting, level in dB relative to the peak section |
| Frequency | high-pass at N Hz, low-pass at N kHz, cut or boost a band by N dB, mid-range body, top-end air |
| Image | center, wide, panned left or right, mono below N Hz, stereo double |
| Performance | velocity, accent pattern, ghost notes, fill, break, tail |

## Never write

- "Sounds like", "reminiscent of", "in the style of" followed by any person, group, album, or song.
- Any name on `references/shared/blocked-targets.txt`, even as a "for example".
- A reference track, a playlist, a producer, a studio, or a recording era tied to a named act.
- Mood-only instructions with no parameter ("make it dreamy", "more vibe").

Genre and era labels are fine: "mid-tempo pop groove, straight eighths, 118 bpm".

## Turn a wish into parameters

| Wish | Technical statement |
|------|---------------------|
| Intimate verse | Dry lead, short plate (0.8 s, 20 ms pre-delay), no doubles, close level |
| Big chorus | Lead plus two stereo doubles, slap delay at 1/8 note, 15 percent wet, pad widened |
| Breath before the final chorus | One-bar drum break, then every layer re-enters on the downbeat |
| Clear hook | Cut 2-4 kHz on competing pads; lead compressed 4:1, slow attack |
| Quiet bridge | Reduce level about 4 dB, remove the top layers, narrow the image |

## Section notes pattern

`- <Label>: <what enters>, <what leaves>, <what changes in level, width, or effect>.` One line per
section, same order as `arrangement.md`, same instruments as its row.

## Mix priority pattern

Rank 3-5 items. Start with the vocal, then the rhythm lock between kick and bass, then the
frequency decisions that keep layers apart, then the dynamic contrast between sections. Each item
is a decision, not a hope.

## Self-check

Search the brief for "like", "style", "sound", and any capitalized name. Replace every hit with a
parameter. Confirm tempo and meter match `structure.md`.

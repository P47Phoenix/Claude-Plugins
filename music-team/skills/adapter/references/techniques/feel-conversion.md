---
loaded_by: adapter
level: L3
last_reviewed: 2026-10-26
---

# Technique: Feel Conversion

Move a song from the rhythmic world of `source_genre` to that of `target_genre` without changing what the
melody and words say. Read the target's `## Rhythm` section first; its tempo band, meter and feel win over
anything below.

## 1. Choose the tempo

1. Take the target band from its profile (written `NN–NN BPM`).
2. Compare the source tempo to the band using the *felt* pulse, not the notated one. A song felt in two
   at a slow notated tempo has a faster felt pulse than the number suggests.
3. If the source tempo falls inside the band, keep it. Otherwise move to the nearest band edge, then
   nudge toward the middle, so the lyric still fits in a breath.
4. Never move more than a factor of two in one adaptation; beyond that the song reads as a different piece.
5. Record `bpm: <source> -> <target>` as one Changed row.

## 2. Convert the time signature

| Source | Target | Method |
|---|---|---|
| 3/4 | 4/4 | Keep the beat. Three beats become three-quarters of a bar: pad each phrase to a whole bar with a held note or a rest on beat four, or stretch every second bar by one beat. Prefer padding; it keeps melody rhythm intact |
| 4/4 | 3/4 | Drop one beat per bar by shortening held notes first, then removing a passing note. Never cut a stressed syllable |
| 4/4 | 6/8 | Map each beat to a dotted-quarter group; swap straight eighths for triplet-feel pairs |
| 6/8 | 4/4 | Map each dotted-quarter group to one beat; straighten the pairs |
| any | 2/4 | Halve the bar length; double the tempo number only if the target band demands it |

After conversion, recount bars per section so phrases stay four or eight bars (or the target's habit).
The bar count belongs in `structure.md`; if it must change, return `BLOCKED` with the new count.

## 3. Move the groove

- Identify the source's rhythmic layers: bass pattern, chordal pattern, backbeat, and any ornament.
- Replace each layer with the target's equivalent from `## Rhythm` / `## Arrangement`; never stack a source
  layer and a target layer that both claim beat two.
- Keep one rhythmic anchor from the source (for example the bass landing on beat one) so the song stays
  recognisable.
- Straight versus swung: copy the target's choice. Do not swing a straight-eighth genre or the reverse.

## 4. Re-time the melody (when one is supplied)

- Keep pitch contour and the pitch on every strong beat; move onsets by at most half a beat to land on
  the target's syncopation points.
- Do not add notes to fill the new groove. Add rests or held notes instead.
- Check the vocal range after any key or tempo change.

## 5. Check list

- Tempo inside the target band, or the exception noted under Risks.
- Time signature equals `structure.md`.
- Section lengths still match the form template.
- Exactly one groove layer per rhythmic role.
- The energy shape of the source (quietest and loudest section) is preserved.

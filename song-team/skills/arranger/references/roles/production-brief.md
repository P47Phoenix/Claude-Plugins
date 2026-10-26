---
loaded_by: production-brief
level: L2
last_reviewed: 2026-10-26
---

# Role: production-brief

## Mission

Turn `arrangement.md` into instructions a producer or a DAW operator can execute without having heard any other record: the tempo map, the vocal chain per section group, three to five mix priorities, and one note per section. The brief is the only document that travels with the song into a studio, so it must stand on its own, agree with every earlier artifact, and contain no name, title, or comparison that the originality policy forbids. Say what to do with the sound; never say whose sound it is.

## Inputs

- `brief.md`: genre, mood, audience, `target_length_sec`, `must_avoid[]`.
- `structure.md`: `bpm`, `time_sig`, `key`, `mode`, section order, bar counts. The tempo map restates these exactly.
- `arrangement.md`: the energy curve, the entries and exits, and every `texture_note`. Each section note is this row rewritten as an instruction.
- `lyrics.md` (when it exists): where the hook line sits, which lines are dense, which sections a group vocal would suit. For an instrumental, which instrument carries the motif instead.
- `concept.md` title for the optional first line.
- `genres/<g>.md`: production tropes and vocal conventions for the genre.
- `techniques/reference-track-language.md`: the vocabulary for describing sound without naming anyone, with before/after rewrites.

## Process

1. Write `## Tempo map` from the `structure.md` header: bpm, time signature, constant or not, every feel change with its section and bar, count-in, stops, breaks, final held note, total bars when the bar counts sum cleanly.
2. Write `## Vocal treatment` by section group. For each group: lead count, doubles, harmonies, group parts; pan positions; reverb type with decay in seconds and pre-delay in ms; delay note value and wet percentage; compression ratio and attack character; de-essing or filtering. The group vocal, if any, lands where `arrangement.md` lists `backing vocals` or `group vocal` entering. For an instrumental write `None.` then treat the lead instrument as the voice.
3. Write `## Mix priorities` as a numbered list of three to five. Item 1 is almost always lead intelligibility on the hook (or the motif). The others name a pair of elements and the action that resolves their conflict: what is sidechained to what, which band each keeps, how many dB the quiet section drops.
4. Write `## Section notes`, one bullet per section in `structure.md` order, starting with the label and a colon. Each bullet restates the row's `instruments_in`, `instruments_out`, and `texture_note` as an instruction with bar numbers where the arrangement gives them. Distinguish repeated sections (`Final Chorus:`).
5. Replace every evaluative or comparative word with a measurable one using the technique file's vocabulary table: `punchy` becomes `fast-attack compression, 4:1`; `vintage` becomes `tape-style saturation, high end rolled off above 10 kHz`; `big` becomes `wide stereo doubles, pad under the hook`.
6. Scan the draft for the forbidden strings and for any proper noun. A proper noun that is not a section label or an instrument is removed. "Sounds like", "reference track", "in the style of", "think of", and "a la" are removed with the sentence rewritten in technical terms.
7. Cross-check numbers: the bpm and time signature equal `structure.md`; every section bullet matches its `arrangement.md` row; nothing enters in the brief that never enters in the arrangement.
8. Write the file.

## What the lint measures

- `validate_artifacts.py` (W4-2) reads `production-brief.md` after it is written and FAILs on any whole-phrase, case-insensitive hit from `references/shared/blocked-targets.txt` and on the strings "sounds like" or "reference track". It is advisory (`PostToolUse`, always exit 0) but its findings go to the critic and to `state.json`.
- `song-critic:challenger` at Stage 7b reads the brief in a clean context and reports any artist, title, or comparison as a BLOCKER; `challenge_gate.py` then fails the release and loops back.
- No script checks the tempo map against `structure.md`, so the agreement is yours to verify in step 7.

## Common failure modes

| Failure | Why it happens | Fix |
|---------|----------------|-----|
| "sounds like" or a name slips in | Describing by comparison is faster than describing by parameter | Use the vocabulary table; every comparison becomes a parameter |
| Plug-in or gear model named | Studio habit | Generic type (`optical compressor`, `plate reverb`, `tape-style saturation`) |
| Tempo map disagrees with `structure.md` | Rounded or retyped | Copy bpm and time signature from the header |
| Section notes skip a repeated section | Choruses merged | One bullet per structure row |
| Mix priorities are adjectives | "Make it warm" | Name the element, the action, and the number |
| Vocal treatment for an instrumental | Template filled blindly | `None.` then the lead instrument's treatment |

## What to return

Write `production-brief.md` to the artifact path. Reply with the four-line hand-back from the prompt's `## Return` block. In `SUMMARY`: the tempo and bar total, the vocal chain in one line, the mix priority you expect to be contested, and a statement that you scanned for names and the forbidden strings (what you removed, if anything). Never state that a lint passed.

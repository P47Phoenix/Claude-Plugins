---
loaded_by: adapter
level: L2
last_reviewed: 2026-10-26
---

# Output Contract: music-adapt

Artifacts: `chords.md`, and `melody.abc` only when the user supplied a melody. Grammars are the normal
`chords.md` and `melody.abc` grammars in `music-team/references/shared/artifact-formats.md`; `chords.md`
also carries the notes block for both files.

## chords.md

- Header `key: <tonic> <mode>`; tonic and mode equal `structure.md`.
- One `[Label]` block per section, labels equal to `structure.md`, in the same order.
- Each line is one phrase; one bar per cell between `|`; roman numerals; `%` repeats the previous cell.
- Concert chords on the next line prefixed `>`.
- Chord qualities use plain suffixes (`7`, `m7`, `maj7`, `m6`, `sus4`, `add9`, `7b5`, `7b9`) so `chord_tools.py` can read them.
- Diatonic ratio stays at or above `quality.diatonic_min_ratio`; at most 40 percent chromatic or borrowed chords per section.
- Lines starting with `# ` are comments.

## melody.abc (only when a melody is supplied)

- ABC 2.1, single voice, headers `X`, `T`, `M`, `L`, `Q`, `K` in order; `M:` equals `structure.md` `time_sig`;
  `K:` equals its key and mode; `Q:` equals its bpm.
- `%%section <Label>` per section; a `w:` line follows each music line when `lyrics.md` exists, with one syllable
  token per note (`-`, `_`, `*`, `~`, `|` as in the formats file).
- Pitch contour of the hook is preserved; rhythm may be re-timed onto the target feel. No notes block in this file:
  record melody changes in the `chords.md` block.

## Adaptation notes block (end of chords.md)

After the last section, one blank line, then the literal heading and `# `-prefixed lines so every chord
gate ignores it:

```text
## Adaptation notes
# Kept: <comma-separated preserved elements: key, cadences, hook contour, ...>
# Changed: <element>: <source> -> <target> (<why>)
# Risks: <one risk per line>
```

Rules: exactly one `# Kept:` line; one `# Changed:` line per element family (for example "chord colour",
"chorus harmony", "melody rhythm"); every Changed entry has element, source, target and why; at most
`adaptation.max_changed_elements` Changed lines in total; no artist, band or song names.

## Example

```markdown
key: G minor

[Verse 1]
| i7 | iv7 | V7 | i7 |
> | Gm7 | Cm7 | D7 | Gm7 |

## Adaptation notes
# Kept: key G minor, i - iv - V - i skeleton, dominant pull at phrase ends
# Changed: chord colour: triads -> seventh chords (genre harmony colour)
# Risks: richer chords can bury a simple melody if voiced too high
```

## Hand-back

```text
SKILL_LOADED: <every references/ path pasted>
STATUS: DONE | BLOCKED
ARTIFACT: <dir>/chords.md
SUMMARY: one sentence, max 200 characters
```

`BLOCKED` adds `FINDINGS:` bullets (for example "target tempo band excludes the structure.md bpm").

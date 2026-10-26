---
loaded_by: composer
level: L2
last_reviewed: 2026-10-26
---

# Harmony Output Contract: `chords.md`

Owner: `harmony`. Validated by `chord_tools.py chords.md structure.md` (Stage 5). The grammar below is the one in `references/shared/artifact-formats.md`; produce exactly this.

## Grammar

```text
key: <Tonic> <mode>

[<Label>]
| <numeral> | <numeral> | ... |
> | <chord> | <chord> | ... |
| <numeral> | % | ... |
> | <chord> | % | ... |

[<Label>]
...
```

- **Header** is one line, `key: <Tonic> <mode>` (`key: D major`, `key: A minor`, `key: E dorian`). It equals `structure.md` `key` and `mode`. One blank line follows.
- **Section tags** `[Label]` on their own line, identical to `structure.md` labels, in the same order. Repeated sections (every Chorus) each get their own block.
- **Phrase line.** Each line is one phrase. One bar per cell between `|`. A cell holds one chord.
- **Concert line.** Directly under each numeral line, prefixed `>`, the same number of cells holding the concert-pitch chord symbols. The concert line is optional for the gate but required by this contract.
- **`%`** repeats the previous cell (on either line kind). The first cell of the file cannot be `%`.
- Lines starting `#` are comments and ignored.

## Numeral vocabulary

| Form | Meaning | Example |
|------|---------|---------|
| `I` ... `VII` | major triad on the degree of the **major** scale on the tonic | `IV` in D = G |
| `i` ... `vii` | minor triad | `vi` in D = Bm |
| `b` / `#` prefix | lowered or raised root | `bVII` in D = C, `#iv` in D = G#m |
| `°`, `dim` | diminished triad | `vii°` |
| `ø7`, `m7b5` | half-diminished seventh | `iiø7` |
| `7`, `maj7`, `m7` (lowercase numeral + `7`) | seventh qualities | `V7`, `Imaj7`, `ii7` |
| `add9`, `sus2`, `sus4`, `6`, `9`, `11`, `13` | color tones | `Iadd9`, `Vsus4` |
| `+`, `aug` | augmented | `III+` |
| `/3`, `/b7`, `/5` | slash bass as a scale degree | `I/3` = tonic over its third |
| `V/vi`, `V7/ii` | secondary dominant of the named degree | `V7/vi` in C = E7 |

Minor keys use the major-scale-relative convention: `i`, `bIII`, `iv`, `v` or `V`, `bVI`, `bVII`.

## Rules the gate enforces

1. Every cell parses. An unparseable cell is an ERROR, not a loop trigger.
2. `diatonic_ratio` (diatonic chords divided by all chords, repeats counted) is at least `diatonic_min_ratio` (default 0.6). A chord is diatonic when all its pitches sit in the key's scale (minor keys also accept the raised seventh).
3. Each `>` cell matches its numeral's pitches in the key; a cell-count mismatch between the two lines fails.
4. Warnings, not failures: a section whose last two chords make no V-I, IV-I, V-vi, or bVII-I motion; adjacent root-position triads moving by step (parallel-fifth risk).

## Example

```markdown
key: D major

[Verse 1]
| I | V | vi | IV |
> | D | A | Bm | G |
| I | V | IV | I |
> | D | A | G | D |

[Chorus]
| I | IV | vi | V |
> | D | G | Bm | A |
| I | IV | V | I |
> | D | G | A | D |
```

## Notes block (optional)

After the last section, a trailing `#` comment line may carry decisions for the orchestrator: `# note: borrowed bVII in Bridge for lift`. Keep it to `#` lines so the gate ignores it.

## Hand-back

```text
SKILL_LOADED: <paths>
STATUS: DONE | BLOCKED
ARTIFACT: <dir>/chords.md
SUMMARY: <one sentence, max 200 characters; progressions used, any borrowed chords>
```

On BLOCKED add `FINDINGS:` bullets (unparseable supplied chord, key conflict with `structure.md`, missing input).

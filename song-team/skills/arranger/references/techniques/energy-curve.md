---
loaded_by: dynamics
level: L3
last_reviewed: 2026-10-26
---

# Technique: Energy Curve (shaping the numbers the gate reads)

`arrangement_check.py` reads one integer per section and applies a rule chosen by `quality.energy_curve`. This file restates each rule in craft terms with numbers, so the first draft passes and still feels like a song. The rule text in `references/shared/stage-gates.md` wins over anything here.

## What "energy" means

A single integer 1-10 for how intense a section is perceived to be, combining density (how many parts), register (how high the lead and the top of the accompaniment sit), rhythm (how busy the kit and the subdivision are), and level. It is not the lyric's emotion: a quiet section about something enormous is still a 3. It moves with what enters and leaves in the same row.

## Section roles the script recognises

| Role | Labels | Why it matters |
|------|--------|----------------|
| chorus-role | `Chorus`, `Drop` (with or without a number) | the rising sequence `C1..Cn`; the peak lives here |
| bridge-role | `Bridge`, `Bridge 2`, `B` (AABA) | the one other place the peak may live |
| verse-role | `Verse N`, `A1`, `A2`, `A3` | must sit below the next chorus-role section |
| neutral | `Intro`, `Pre-Chorus N`, `Post-Chorus`, `Build`, `Breakdown`, `Instrumental`, `Tag`, `Outro` | unconstrained except by rule (c) at the end |

A `Drop` is a chorus to the script. A `Build` before it is neutral, so a build can sit anywhere below the drop. An EDM form `Intro Build Drop Breakdown Build Drop Outro` is judged exactly like a verse-chorus song with the drops as choruses.

## `chorus_rising` (default)

Let `C1..Cn` be the chorus-role energies in order and `G` the global maximum.

**(a) Choruses never fall.** `Ci >= Ci-1`. Each return of the chorus adds something: a doubled vocal, a higher harmony, an open hi-hat. In numbers, `7 -> 8 -> 9` or `6 -> 6 -> 8`. A chorus that comes back smaller (`7 -> 6`) fails at the smaller one. If the song wants a quiet last chorus, make it a `Breakdown` or a `Tag` and put a real final chorus after it, or set `strict_rising`.

**(b) The peak is the last chorus or the bridge.** `G` must occur in the final chorus-role section or in a bridge-role section; ties count. A song whose biggest moment is the second chorus fails unless the last chorus ties it. A bridge peak is allowed (`B 9, final Chorus 9` passes; `B 9, final Chorus 8` also passes because the bridge holds `G`).

**(c) The ending sits below the peak unless it is the last chorus.** If the song ends on an `Outro`, `Tag`, or `Post-Chorus`, that row's energy is strictly less than `G`. `Chorus 9, Outro 9` fails; `Chorus 9, Outro 6` passes. A song that ends on its last chorus is exempt.

**(d) Every verse is below the chorus that follows it.** Strict: `Verse 2 = 7, Chorus = 7` fails. Typical gaps are 3 or 4 (`3 -> 7`, `4 -> 8`). A verse after the last chorus (rare) is unconstrained.

### Numeric examples

| Form | Curve | Result |
|------|-------|--------|
| V1 PC C V2 PC C B C C | 3 5 7 4 6 8 5 9 9 | PASS: choruses 7 8 9 9; peak in final chorus; verses 3<7, 4<8 |
| V1 C V2 C B C Outro | 3 7 4 8 6 9 5 | PASS: outro 5 < 9 |
| V1 C V2 C B C Outro | 3 7 4 8 6 9 9 | FAIL (c): outro equals the peak |
| V1 C V2 C B C | 3 8 4 7 5 9 | FAIL (a): second chorus 7 < 8 |
| V1 PC C V2 PC C | 3 5 7 8 6 8 | FAIL (d): Verse 2 is 8, the next chorus is 8; equal is not below (at 7 it would pass) |
| Intro Build Drop Breakdown Build Drop Outro | 2 5 8 3 6 9 4 | PASS: drops 8 9; peak in final drop; outro below |
| V1 PC C V2 PC C | 4 6 9 5 7 8 | FAIL (a) and (b): second chorus falls; peak is the first chorus |
| all sections 5 | 5 5 5 5 5 5 | FAIL (d) at every verse: equal is not below |

## `strict_rising`

One peak, no roles. The sequence is non-decreasing up to the first occurrence of `G` and non-increasing after it. `2 4 6 8 8 6 3` passes. `2 6 4 8 5` fails at the `4` (falls before the peak). `3 5 9 6 7` fails at the `7` (rises after the peak). Use it for through-composed pieces, film cues, and any form without a chorus-role section. When `chorus_rising` is configured but no chorus-role section exists, the script applies this rule and reports `metrics.no_chorus: 1`.

## `free`

Always PASS. Metrics (`sections`, `global_max`, `chorus_count`) are still reported. Use only when the brief asks for a deliberately flat or inverted curve; the critic still reads the numbers.

## Craft habits that keep the numbers honest

- Decide the peak first, then the first chorus two below it, then everything else relative to those two.
- Each number should be explainable by the row's `instruments_in` / `instruments_out`: more parts or a higher register means a bigger number; a stripped section means a smaller one.
- Keep at least two steps between a verse and its chorus; one step reads as "nothing happened".
- Make the bridge the second-lowest number when the final chorus must land hard; give the bridge the peak only when the final chorus is a wind-down you will label as such.
- Reserve 10 for a section where literally everything plays. Most pop songs top out at 9.

## Finalising an existing table

When `arrangement.md` already holds provisional values from the `instrumentation` role: keep any value that already satisfies the four conditions, change the smallest number of cells that makes the whole curve pass, and report every change as `before -> after` with the section label in `SUMMARY`. Never alter a label, an instrument cell, or a texture note to make the curve pass.

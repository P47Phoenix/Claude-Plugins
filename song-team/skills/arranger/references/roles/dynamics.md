---
loaded_by: dynamics
level: L2
last_reviewed: 2026-10-26
---

# Role: dynamics

## Mission

Own the `energy` column of `arrangement.md`. Shape the perceived intensity across the song so each chorus lands harder than the last, every verse sits below the chorus it leads into, and the ending either peaks or settles below the peak. The `instrumentation` role chose the palette and entry order; you convert that into a curve of integers that `arrangement_check.py` accepts under the configured `quality.energy_curve` and that a listener feels as build and release.

You have two modes, decided by what is on disk:

- **Finalise (normal Stage 6).** `arrangement.md` exists with a `# energy: provisional` comment. Edit the `energy` column only; delete the comment; leave every other cell and the header byte-identical.
- **Write (light stage, standalone, or missing file).** No `arrangement.md` exists. Write the whole file per the contract: header copied from `structure.md`, all five columns, energy final. Keep the palette simple and the entry order per `genres/<g>.md`.

## Inputs

- `brief.md`: mood and `target_length_sec` (a jingle has no room for a slow build; a ballad has no room for a 9 in Verse 1).
- `structure.md`: the header and the section list in order; bar counts (an 8-bar bridge can afford a dip; a 2-bar tag cannot).
- The current `arrangement.md` with its instrument entries and exits: energy must agree with them. A section that adds three parts does not drop in energy; a section that loses the kit does not rise.
- A critique and `arrangement_check` gate JSON when re-dispatched; every violation names a section (`Verse 2`, `Chorus:3`) and the rule letter.
- `genres/<g>.md`: the typical curve numbers for the genre.
- `techniques/energy-curve.md`: the rule restated in craft terms, with numeric examples.

## Process

1. List the sections in order with their role: chorus-role (`Chorus`, `Drop`), bridge-role (`Bridge`, `B`), verse-role (`Verse N`, `A1`-`A3`), neutral (everything else).
2. Pick the peak: the final chorus-role section (or the bridge when the genre peaks there). Assign it the global maximum, usually 8-10. Nothing else may equal it except a bridge or an earlier tie on the final chorus.
3. Assign the other choruses in non-decreasing order below the peak: first chorus two below, second one below is a common shape (`7, 8, 9`).
4. Assign each verse at least one below the chorus that follows it, and usually three or four below (`3` before a `7`; `4` before an `8`). A second verse may sit one above the first because the kit is in by then.
5. Assign pre-choruses and builds between their verse and their chorus. Assign the bridge below the chorus before it unless the bridge is the peak; a stripped bridge is often the second-lowest number in the song.
6. If the song ends on a section that is not a chorus (`Outro`, `Tag`, `Post-Chorus`), give it a value below the peak; one or two below for a hard ending, four or more below for a fade.
7. Walk the checklist in the contract: (a) choruses never fall, (b) peak in the final chorus or bridge, (c) final section below the peak unless it is the last chorus, (d) every verse below its next chorus. Fix any failure by moving the verse or chorus value, never by relabelling a section.
8. Cross-check against the instrument columns: any row where energy rises while `instruments_out` is non-empty and `instruments_in` is `-`, or falls while parts enter, gets a note in `SUMMARY` explaining why (a register change or a feel change) or a corrected value.
9. In finalise mode, diff your table against the input: only `energy` cells and the provisional comment may differ. In write mode, run the contract's structure rules (header, columns, labels).
10. Write the file.

## What the gate measures

- `arrangement_check.py` with `chorus_rising` (default): the four conditions above; one violation per failed condition with the section label as `location` (`Chorus:2` for the second chorus) and `observed`/`limit` values. With `strict_rising`: non-decreasing up to the first maximum, non-increasing after. With `free`: always PASS. When no chorus-role section exists (an AABA without a `B`, a through-composed piece), `chorus_rising` evaluates as `strict_rising` and reports `metrics.no_chorus: 1`.
- Energy outside 1-10, a blank cell, or a non-integer is an `ERROR` and stops the gate before any rule is checked.
- `structure_check.py --consistency`: unchanged by you in finalise mode; in write mode it checks your header and section list against `structure.md`.

## Common failure modes

| Failure | Why it happens | Fix |
|---------|----------------|-----|
| (d) verse equals next chorus | Verse 2 raised to match the kit entering | Keep Verse 2 at least one below its chorus; raise the chorus instead |
| (a) second chorus below the first | First chorus written as the "big reveal" | Choruses only climb; save the reveal for the last one |
| (b) peak in a pre-chorus or build | Build written as the climax | The build tops out one below the chorus it feeds |
| (c) outro equals the peak | Outro copied from the final chorus | Outro one or more below |
| Energy rises while parts leave | Numbers assigned from the lyric's emotion, not the texture | Energy follows density and register; move the number or document the register change |
| Changed a texture note while finalising | Edited the wrong column | Diff before writing; revert everything but `energy` |

## What to return

Write `arrangement.md` to the artifact path. Reply with the four-line hand-back from the prompt's `## Return` block. In `SUMMARY`: the final energy list in section order, the before/after pairs for every value you changed (finalise mode), which section is the peak and why, and any row where energy and instrument movement disagree with your reason. Never state that a gate passed.

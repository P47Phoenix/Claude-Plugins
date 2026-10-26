---
loaded_by: verse-writer
level: L3
last_reviewed: 2026-10-26
---

# Technique: Rhyme Schemes (keyed the way the gate keys them)

`rhyme_check.py` compares the **rhyme key** of the last word of every lettered line in a section. Write rhymes by key, not by ear, and the gate agrees with you.

## How the key is built

1. Take the line's last word, lower-case, punctuation stripped (`floor.` is `floor`).
2. Look it up in `scripts/data/rhyme-exceptions.txt` first (`through`, `you`, `do`, `who`, `two`, `to`, `love`, `of`, `come`, `some`, `one`, `done`, `none`, `gone`). These carry hand-set keys so `love`/`of` and `gone`/`on` are full rhymes.
3. Otherwise the key is the word from its **final vowel group** to the end. A trailing silent `e` stays in the tail: `time` keys `Ime`, `name` keys `Ame`. `y` is a vowel when final or after a consonant.
4. The final vowel group is normalised to a class: `ee ea ie` -> `E`; `ay ai ei ey eigh` -> `A`; `oo ue ew` and final `ou`/`u` -> `U`; `igh`, final `y` in a monosyllable, final `ie`/`i` -> `I`; `oa ow oe` and final `o` -> `O`; a lone vowel before consonant + silent `e` takes its long class; final `y` after an earlier vowel group -> `E` (`lonely` keys `E`); silent `gh` is dropped (`bought` keys `out`).

Only the last vowel group matters. Polysyllables rhyme on their final syllable: `river`/`ever` (`er`), `morning`/`warning` (`ing`), `water`/`daughter` (`er`) are all **full** rhymes to the script.

## Full versus slant

| Pair | Keys | Verdict |
|------|------|---------|
| street / feet | `Et` / `Et` | full |
| town / down | `own` / `own` | full |
| rain / again | `An` / `An` | full |
| wall / call | `all` / `all` | full |
| fold / cold | `old` / `old` | full |
| sky / high | `I` / `I` | full |
| stay / day | `A` / `A` | full |
| gone / on | `on` / `on` | full (exception table) |
| home / alone | `Ome` / `One` | slant (same vowel class `O`) |
| time / line | `Ime` / `Ine` | slant |
| fence / sense | `Ence` / `Ense` | slant |
| porch / church | `orch` / `urch` | slant (same final cluster `rch`) |
| coat / wrote | `Ot` / `Ote` | slant |
| again / men | `An` / `en` | slant (`n` cluster) |
| drawer / more | `er` / `Ore` | **none** |
| fire / tired | `Ire` / `ed` | **none** (`tired` keys on `-ed`) |
| wire / higher | `Ire` / `er` | **none** |
| room / home | `Um` / `Ome` | **none** |
| go / see | `O` / `E` | **none** (empty cluster is not a rhyme) |

Slant counts only when `slant_rhyme_allowed: true` (the default). The genre file states when a genre expects full rhyme on the chorus regardless.

## Schemes and what they do

- `AABB` (couplets): fastest payoff; suits choruses and pop verses. Risk: sing-song. Vary line length or put the hook on the second `B`.
- `ABAB` (alternating): the verse workhorse; two rhymes in flight keep attention. Risk: the second `A` arriving forced. Write line 3 before line 1.
- `ABCB` / `xAxA`: half the rhyme burden; folk and country verses, story-heavy lyrics. The free lines carry the detail, the rhymed lines carry the turn.
- `AAAA`: emphasis; bridges and chants. Four full keys in one section is hard; use the exception-table words and short vowels (`-and`, `-ight`, `-ame`).
- `AxAx` with internal rhyme: when the scheme frees a line, put a rhyme inside it (`the kettle settles`) so the ear still hears pattern.
- `AA` two-line pre-chorus: one pair, both lines pointing at the hook.

Letters reset each section. `[Verse 2]`'s `A` is unrelated to `[Verse 1]`'s `A`; choose fresh sounds so the verses do not repeat end words.

## Picking end words so the gate passes

1. Write the line that carries the meaning first and lock its end word.
2. List candidate partners by key, not by sound: for `Ame` list `name same came flame frame blame`; for `old` list `fold cold told hold sold`.
3. Prefer monosyllabic content words at line end; they land `S` on the final beat and key cleanly.
4. Avoid ending a lettered line on a function word (`of`, `the`, `to`): keys are fine but the prosody beat is lost.
5. Avoid `-er`/`-ing`/`-ly` endings on both lines of a pair unless the genre wants feminine rhyme; the key is identical but the final beat is `u`.
6. Check the whole section: in `ABAB`, both `A` lines and both `B` lines; in `AABB`, lines 1-2 and 3-4. One mismatch fails the section.
7. When a pair keys as `none` and the line is right, change the **other** line of the pair.

## Original examples

```text
ABAB, 8/uSuSuSuS:
The kettle hums before the light      A (key It; silent gh dropped)
A borrowed coat that fits me wrong    B (key ong)
I kept the stub inside my coat        -> fails A: Ote != It; rewrite:
The window holds a second night       A (key It, 8/uSuSuSuS)
The paint is peeling off the swing    -> fails B: ing != ong; rewrite:
The hall has known my name all along  -> rhymes (ong) but 9 syllables; rewrite:
The hall has known my name so long    B (key ong, 8/uSuSuSuS)
```

Every rewrite above changed one end word and recounted syllables. That is the whole method.

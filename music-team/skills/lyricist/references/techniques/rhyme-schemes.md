---
loaded_by: lyricist
level: L3
last_reviewed: 2026-10-26
---

# Rhyme Schemes

`structure.md` gives each section a `rhyme_scheme` string. Each letter is a rhyme group; lines sharing a letter must rhyme; `x` marks a free line. Letters are scoped per section: an `A` in Verse 1 has nothing to do with an `A` in Verse 2.

## Common schemes

| Scheme | Shape | Feel |
|--------|-------|------|
| AABB | Couplets | Direct, sing-song; good for refrains and bridges |
| ABAB | Alternating | Flowing; room for two sentences per quatrain |
| ABCB | Second and fourth lines rhyme | Conversational; the folk default |
| AxAx | Even lines free, odd lines rhyme | Loose; good for bridges |
| AAAB | Three rhymes then a turn | A punchline in the last line |

## What counts as a rhyme (gate rules)

- **Full rhyme**: the last word of each line has the same ending from its last stressed vowel (see/be, light/night, away/day).
- **Slant rhyme**: same vowel class or same final consonants with a different vowel; accepted only when `quality.slant_rhyme_allowed` is true. Pairs such as go/see do not count.
- Irregular spellings are keyed by sound (love/of, through/you, one/done), so choose pairs the script and the ear both accept.
- A line's rhyme is its last word; end a rhymed line on that word, not on a trailing particle.

## Method

1. List the rhyme words for each letter before writing the lines: pick pairs with distinct meanings.
2. Choose pairs that lead to different images (tide and wide, not wide and wide-eyed).
3. Write the second line of a pair to arrive at its rhyme word naturally, then the first to set it up.
4. Keep the strongest rhyme for the hook or the final line of the chorus.

## Quality guardrails

- Never rhyme a word with itself or with a compound of itself.
- Avoid forced inversions ("sing I do") to land a rhyme; reword the clause.
- Avoid a rhyme chain that only works through stock pairs (fire/desire, heart/apart); try a slant pair or a fresher word.
- Vary rhyme sounds across sections so verses do not all end on the same vowel.
- Mix feminine (two-syllable) and masculine (one-syllable) endings only if the `meter_spec` allows it; the spec's last two characters tell you which.

## Free lines

An `x` line still needs to meet the meter and sit well beside its neighbours. Use it for the line that carries the plain statement between two rhymed lines.

## Checking

Run `rhyme_check.py --json lyrics.md structure.md`; a FAIL names the later line of each unmatched pair. Fix the later line first.

## Non-English

The rhyme gate SKIPS for `language` other than `en`; still follow the scheme by ear.

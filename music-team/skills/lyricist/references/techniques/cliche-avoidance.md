---
loaded_by: lyric-editor
level: L3
last_reviewed: 2026-10-26
---

# Technique: Cliché Avoidance (what the scan catches and how to replace it)

`cliche_scan.py` matches **whole phrases** from `references/shared/cliche-list.txt` (300+ entries), case-insensitive, punctuation-insensitive, on word boundaries. It reports `metrics.hits`, `metrics.words`, and `per_100_words = hits * 100 / words`, and fails above `cliche_max_per_100_words` (default 2).

## What the numbers mean

- A 120-word lyric fails at three hits (2.5) and passes at two (1.67).
- A `concept.md` scans only `title` + `hook_line` + `central_image` (about 15 to 25 words): one hit is roughly 4 to 7 per 100 and fails. The hook target is zero.
- Comment lines (`# `) and `[Label]` tags are not scanned and not counted as words.
- Single words are never hits; the list holds phrases of two words or more. "heart" alone passes; "heart of gold" fails. That is a scan limit, not a licence: the critic still flags stock single words.

## The families on the list

Most entries belong to a dozen families. Knowing the family is faster than memorising the list.

| Family | Typical entries | Physical replacement |
|--------|-----------------|----------------------|
| heart + X | heart of gold, broken heart, you broke my heart, fire in my heart | the thing the heart would do: the kettle boils for one |
| weather as feeling | tears in the rain, crying in the rain, dancing in the rain, against the wind | the weather as weather: rain on the market awning |
| night as party / loss | all night long, dance all night, up all night, party all night | a clock time: until the streetlights quit |
| forever | forever and always, till the end of time, forever and a day | a dated promise: until the lease runs out |
| the road | end of the road, long and winding road, road to nowhere, the road ahead | the specific route: the bus route learned upside down |
| stars and dreams | written in the stars, reach for the stars, dreams come true, follow your dreams | the plan itself: a photo pinned above the sink |
| sky | clear blue sky, sky high, touch the sky, light up the sky | what is in the sky: the crane above the station |
| holding | hold me close, hold me tight, never let you go | the actual grip: your hand around the handle |
| breath and fire | take my breath away, set my soul on fire, light my fire | the body's fact: I forget to breathe out |
| love as law | love is blind, love conquers all | a scene in which it does |

## Replacement method (keeps prosody intact)

1. Note the hit's syllable count and stress with the heuristic (`all night long` = 3, `SSS`; `broken heart` = 3, `SuS`).
2. Ask what physical event the cliché stands for in this song. Use the brief's objects first.
3. Write a replacement with the **same syllable count and the same `S` positions**. `all night long` (SSS) becomes `past last call` (SSS) or `till the lights` (uuS: one beat lost; recount the line).
4. Check the new phrase against the families above; a replacement from a neighbouring family (`broken heart` to `empty bed`) is a new hit waiting for the next list revision.
5. Re-run the rhyme check in your head if the phrase was at line end: the end word's key has changed.

## Near-clichés the scan misses and the critic catches

- Stock rhyme pairs: fire/desire, heart/apart, cry/die, night/light. Legal to the script; flagged by the critic as predictable. Change the first line's end word.
- Emotion vocabulary as filler: "pain", "tears", "soul", "lonely", "forever". One per song at most, never in the hook.
- Generic intensifiers: "so much", "so bad", "like crazy". Delete; the line is usually better one syllable shorter plus one content word.
- Abstract nouns as subjects: "love", "time", "life", "the world". Replace with the person or thing that does the action.

## Original examples of a swap

```text
Before:  I've been up all night just missing you      (hit: "up all night", 9 syl)
After:   I've counted trains until it's light         (0 hits, 8 syl uSuSuSuS: recount against spec)

Before:  You take my breath away each time            (hit: "take my breath away", uSuSuSuS)
After:   I hold my breath when you walk by            (0 hits, 8 syl, uSuSuuSS: beat 6 moved to 7; check the spec)

Before:  A broken heart and nothing more              (hit: "broken heart")
After:   A borrowed coat and nothing more             (0 hits, same count, same stresses)
```

Every swap traded the abstraction for an object already in the song's world, kept the syllable count, and kept the beat.

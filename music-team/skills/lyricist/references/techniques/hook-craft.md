---
loaded_by: lyricist
level: L3
last_reviewed: 2026-10-26
---

# Hook Craft

A hook is the one line a listener can repeat after a single hearing. It carries the song's claim in the fewest syllables that still say something.

## Shape

| Property | Aim | Why |
|----------|-----|-----|
| Length | 4 to 9 syllables; never over `quality.hook_max_syllables` | Fits one breath and one melodic gesture |
| Stress | First and last content words land on strong beats | The ear catches edges |
| Grammar | A complete clause or a vivid phrase, not a fragment of a longer thought | Stands alone off the page |
| Diction | One concrete noun or verb, short words | Specific and singable |
| Sound | One repeated vowel or consonant across two or three words | Gives the line grip without rhyme |

## Patterns that work

- **Withheld word**: state the claim, hold back the last word, supply it in the final chorus or turn it into the twist.
- **Reversal**: two halves that pull against each other (arriving and unseen, staying and leaving).
- **Plain statement of a private fact**: said flatly, it reads as confession.
- **Command or invitation**: short imperative aimed at a "you".
- **Object as feeling**: name a thing (a key, a ticket, a coat) and let it carry the mood.

## Placement

1. The hook appears in the Chorus, first or last line, word for word every time.
2. A verse may end by leading into the hook (a line that rhymes toward it) without repeating it.
3. A pre-chorus raises the question the hook answers.
4. Change one word on the final repeat only when the arc's third beat calls for it, and then record the change in the notes.

## Title

Use the hook or its key phrase as the title. A title longer than the hook is a sign the hook is unfocused. Do not name a place, brand or person unless the brief asks.

## Syllable budget check

Count by dictionary speech: silent final e does not count; `-ed` counts after t or d only; consonant plus `-le` counts one. Run `prosody_check.py --hook concept.md` to confirm. If over, cut modifiers first, then auxiliary verbs, then restructure.

## Candidate test

Say the hook aloud three times without the verses. Ask: does it still mean something, does it differ from the line before and after it, would a stranger sing it back wrongly? Rewrite any hook that fails the first test or passes the third.

## Pitfalls

- Abstract nouns in a row (love, pain, dreams) with no image.
- A hook that needs the verse to make sense.
- Stock phrases that pass a count but fail `cliche_scan.py`.
- Word-for-word echo of a known line: if a phrase feels familiar from a song, drop it.
- Rhyming the hook for its own sake; a good hook may be unrhymed.

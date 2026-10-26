---
loaded_by: hook-writer
level: L3
last_reviewed: 2026-10-26
---

# Technique: Hook Craft

A hook is the line a listener repeats after one hearing without meaning to. It is short, concrete, and says one thing. The gate measures two properties (syllable count, cliché density); this file covers the rest so the hook earns its place as well as passing.

## Five properties of a hook that lands

1. **One idea.** The hook states a single situation or feeling. "Nobody knows my name here yet" is one idea; "I'm new here and I miss my friends but I'll be fine" is three.
2. **A concrete anchor.** One physical noun or one named action: a key, a platform, a porch light, a name said aloud. Abstractions (heart, soul, love, dreams, forever) carry no picture and are where the cliché list lives.
3. **Plain words.** Monosyllables and common two-syllable words. Nothing the listener has to parse. Rarity belongs in the verses.
4. **A withheld word.** The strongest hooks hold back their last word or their twist until the end: "...my name here *yet*". The last word changes the meaning of everything before it.
5. **Sayability.** Stresses fall where speech puts them. Read it aloud three times fast; if the tongue trips, cut a word.

## Syllable budget

`hook_max_syllables` defaults to 12; the genre file states any override. Most hooks that land are 5 to 9 syllables. Count with the heuristic in `techniques/prosody.md` (`every` = 3, `fire` = 1, `hour` = 1). A hook at the limit leaves the melody no room; aim two under.

## Hook shapes (with original examples)

| Shape | Pattern | Example |
|-------|---------|---------|
| Statement | subject + verb + object | I keep the ring inside a jar |
| Negation with turn | nobody / never / not ... yet / still | Nobody knows my name here yet |
| Imperative | verb first | Leave the light on in the kitchen |
| Question | asks what the song answers | Who taught the river where to bend? |
| Conditional | if / when + consequence | When the kettle sings I'll stay |
| List of three | noun, noun, noun | A ticket stub, a spoon, a key |
| Place + time | where and when, no feeling named | The market opens in the rain |

Each example is 7 to 9 syllables and holds one concrete noun. None names an emotion.

## Title from hook

- **Whole line** when the hook is 5 words or fewer.
- **A fragment** when the withheld word is the point: pick the shortest run of words from the hook that still means something alone ("My Name Here Yet").
- **The surprising noun** when one object carries the song ("Platform Nine", "The Borrowed Coat").
- Never a title the hook does not contain or point at; the `title_rationale` has to explain the link in one sentence.

## Central image

One physical thing the whole song returns to. Test: does every section have a way to show it? A key: the verses show doors it does not fit, the bridge shows the door it finally opens. A photo pinned to a wall: verses show the wall bare, the chorus shows the pin. If the image only appears in the chorus, it is a prop, not a central image.

## Arc in three beats

`arc: [start, turn, end]`. Each is a state the narrator is in, 2 to 6 words, not a plot summary. The turn contradicts the start; the end resolves or deliberately refuses to. "arrive unseen, choose to stay, a stranger says my name": start is a condition, turn is a decision, end is an event. Hooks usually live at the turn or the end; verses live at the start.

## Cliché families to avoid in a hook

The cliché list is enforced by whole-phrase match; these are the families most of its entries belong to, so a hook built outside them rarely hits:

- heart + adjective / heart + verb (heart of gold, broken heart, you broke my heart)
- tears / crying / dancing / kissing + "in the rain"
- all night long, dance all night, up all night
- forever and always, till the end of time, end of the road
- stars, dreams, sky as destinations (reach for the stars, follow your dreams, touch the sky)
- hold me close / tight, never let you go
- take my breath away, love is blind, light my fire

Replace the family with its physical trace: not "my heart is breaking" but "the kettle boils for one"; not "all night long" but "until the streetlights quit".

## Self-check before writing concept.md

- Syllables counted by the heuristic and at or under the limit.
- One concrete noun or named action present.
- No emotion word (`love`, `heart`, `soul`, `pain`, `tears`) in the hook.
- Read aloud three times without a trip.
- The title is in, or pointed at by, the hook.
- The central image appears in or beside the hook.
- `must_include[]` placed; `must_avoid[]` absent.

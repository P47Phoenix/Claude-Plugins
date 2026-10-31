# Song Ideas

Loaded for `song-ideas` only. How to derive a list of song ideas from a verified timeline slice, and what the list must never contain. The output is a **list the user takes elsewhere**. This skill does not draft a song, write a line, suggest a melody, or hand off to another plugin.

---

## 1. What an idea is

An idea is a short, neutral description of a song someone could write about one event or moment in the timeline. It is **creative inference** (`[INFERENCE]`), not a fact claim. The fact claims behind it (the event, the reference, the date) come from the timeline and have already been sourced.

Each idea has six fields:

| Field | What goes there |
|---|---|
| **Event** | The timeline event, by name, with its number in the timeline |
| **Passage** | The reference(s) the idea rests on (book chapter:verse) |
| **Angle** | One of: lament, praise, narrative, prayer, testimony, confession, thanksgiving, call to worship, meditation, blessing |
| **Register** | Who sings it and in what setting: congregational, solo or testimony, children, choir or anthem, meditative, procession or celebration |
| **Theme** | A neutral phrase of two to eight words naming what the song is about. No poetic lines, no rhyme, no hook |
| **Source tag** | The `S[N]` IDs behind the event, and `[INFERENCE]` for the idea itself |

---

## 2. Derivation rules

1. Work from the timeline in order. Pick events where the text gives a human voice, a turning point, a promise, a loss, or an act of God that the narrative dwells on
2. Aim for roughly 15-20 ideas for a single era; roughly 10 per era when a batch covers two or three. Fewer is fine when the era is thin; do not pad. Ideas are grouped by era
3. Vary the angle. A slice should not be all praise or all narrative. Include at least one lament where the text has one (most eras do)
4. Vary the register. Include at least one congregational and one solo or testimony idea per slice
5. Where the text itself contains a song or prayer (the Song of the Sea, Exodus 15; Hannah's prayer, 1 Samuel 2; David's lament, 2 Samuel 1; the Magnificat, Luke 1:46-55; the hymn of Philippians 2:6-11), say so under Event and give the reference; the idea is then "a setting of" that text, which is still an idea, not a lyric
6. An idea built on a `[CONTESTED]` date carries the tag and does not depend on one side of the split
7. An idea built on a tradition rather than the text (for example a rabbinic reading) names the tradition and carries `[TRADITIONAL]`
8. Keep theology at the level of the text. Do not assert a doctrinal reading the passage does not make; if the idea leans on a contested reading, say "contested reading" in the Theme or a note
9. An idea whose event was removed by the gate is removed with it

---

## 3. Anti-lyric and anti-artist rules

These are absolute. The gate will remove violations, and the Stop hook treats the output as gated content.

- **No lyrics.** No lines, couplets, refrains, hooks, rhymes, or metrical phrases. The Theme is a plain description, not a line someone could sing
- **No titles of existing songs or hymns**, even as "like" or "in the style of"
- **No artist, band, songwriter, worship-leader, label or publisher names**
- **No melodic, chordal or production direction** (no key, tempo, instrument, genre or arrangement notes). Register is the only musical field and it describes setting, not sound
- **No quotation of more than one verse** from the passage, and only when the Event is a text that is itself a song or prayer
- **No handoff.** Do not offer to write the song, draft lyrics, or send the list to another plugin or skill. End with the question the contract gives

A self-check before returning: read each Theme aloud. If it scans like a line or rhymes with another, rewrite it as description.

---

## 4. Worked shape (not content)

```
3. **Event:** The sea crossing (timeline 7). **Passage:** Exodus 14:21-31; Exodus 15:1-21.
   **Angle:** praise. **Register:** congregational, procession or celebration.
   **Theme:** a setting of the Song of the Sea; deliverance remembered as present.
   **Source:** S2, S5. [INFERENCE]
```

The shape is fixed; the words are the researcher's, drawn from the timeline, and must not be a line.

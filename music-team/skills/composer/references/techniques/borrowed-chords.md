---
loaded_by: composer
level: L3
last_reviewed: 2026-10-26
---

# Borrowed Chords (Modal Mixture)

Borrow a chord from the parallel mode (same tonic, different mode) to add color without leaving the key. In a major key the usual source is the parallel minor; in a minor key it is the parallel major.

## From the parallel minor, used in a major key

| Chord | Name | In C | Effect | Typical use |
|-------|------|------|--------|-------------|
| bVII | subtonic | Bb | rock lift, wide open | before I, or I-bVII-IV |
| bVI | flat six | Ab | epic, cinematic | bVI to bVII to I |
| bIII | flat three | Eb | dark brightness | bIII to IV |
| iv | minor four | Fm | bittersweet, nostalgic | IV to iv to I |
| ii° / iiø7 | diminished two | D° | tension before V | iiø7 to V7 |
| bII | flat two | Db | dramatic, phrygian color | bII to I |

## From the parallel major, used in a minor key

| Chord | In A minor | Effect |
|-------|------------|--------|
| IV | D major | dorian brightness |
| I (Picardy) | A major | final chord lifts to major |
| V | E major | firm, authentic close (from the raised seventh) |

## Using them well

1. **One idea per phrase.** A borrowed chord stands out because the rest is plain. Use at most one or two per section.
2. **Place it on a hinge.** Right before the tonic (bVII), or at the end of a predominant (iv), where the ear expects a function and receives a color.
3. **Resolve it.** bVII, bVI, iv, and bIII all return to I or step to the next predominant; none of them wants to stay.
4. **Keep the melody honest.** The lowered note of the borrowed chord (b6, b7, b3) either appears in the melody over that chord or is avoided on strong beats.
5. **Mind the gate.** The diatonic ratio must stay at or above `diatonic_min_ratio` (default 0.6). Each borrowed chord counts against it; verses should have none or one.

## Genre fit

| Genre | Habitual borrowed chords |
|-------|--------------------------|
| rock, country, folk | bVII (mixolydian color), iv |
| pop | iv in choruses and bridges, bVI for lift |
| gospel | iv, bVII, passing diminished chords |
| musical theatre | iv and bVI for emotional turns, deceptive moves |
| jazz | iiø7-V7-i in minor, bII7 as tritone substitute |
| electronic | bVI and bVII in minor, held for long builds |

## Common patterns

| Pattern | In G | Reads as |
|---------|------|----------|
| I bVII IV I | G F C G | mixolydian loop |
| I IV iv I | G C Cm G | plagal with a minor four |
| I bVI bVII I | G Eb F G | triumphant climb |
| vi bVII I | Em F G | borrowed approach to the tonic |

Check with `chord_tools.py roman <key> <chords...>`: non-diatonic chords are flagged so each borrowed chord is deliberate.

## Do not

- Borrow a chord and also modulate in the same bar.
- Stack three borrowed chords in a row unless the section is a deliberate departure (a bridge).
- Name a famous song as the source of a progression; describe its function instead ("a lifted plagal close").

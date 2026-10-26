---
loaded_by: composer
level: L3
last_reviewed: 2026-10-26
---

# Modes and Scales

## The seven modes (step patterns, semitones from the tonic)

| Mode | Pattern | Compared with major | Color |
|------|---------|---------------------|-------|
| major (ionian) | 0 2 4 5 7 9 11 | reference | bright, settled |
| dorian | 0 2 3 5 7 9 10 | b3 b7 | minor with a lifted sixth; warm, open |
| phrygian | 0 1 3 5 7 8 10 | b2 b3 b6 b7 | dark, tense; the flat second pulls down |
| lydian | 0 2 4 6 7 9 11 | #4 | floating, wonder; no pull to the fourth |
| mixolydian | 0 2 4 5 7 9 10 | b7 | major but unresolved; relaxed |
| minor (aeolian) | 0 2 3 5 7 8 10 | b3 b6 b7 | sad, serious |
| locrian | 0 1 3 5 6 8 10 | b2 b3 b5 b6 b7 | unstable; the tonic triad is diminished |

Other minor scales: harmonic minor `0 2 3 5 7 8 11` (raised seventh, leading tone for V), melodic minor `0 2 3 5 7 9 11` (raised sixth and seventh).

## Spelling rule

Use each letter name once per scale, in order. Accidentals follow from the pattern, not from taste.

| Scale | Spelling | Why |
|-------|----------|-----|
| F major | F G A **Bb** C D E | letters A and B both appear, so the fourth is Bb, not A# |
| G major | G A B C D E **F#** | the seventh is F#, not Gb |
| D minor | D E F G A **Bb** C | b6 is Bb |
| Eb major | Eb F G Ab Bb C D | three flats |
| D mixolydian | D E F# G A B C | the b7 is C natural |

Always confirm with `chord_tools.py scale <tonic> <mode>`.

## Key signatures

Sharps add in the order F C G D A E B; flats in B E A D G C F. A major key's sharp count counts fifths up from C; minor keys share the signature of their relative major (three semitones up). Modes share the signature of the major scale they are a rotation of: D dorian has no accidentals, E phrygian none, F lydian none, G mixolydian none, A minor none.

| Key | Accidentals | Relative minor |
|-----|-------------|----------------|
| G | F# | E minor |
| D | F#, C# | B minor |
| A | F#, C#, G# | F# minor |
| F | Bb | D minor |
| Bb | Bb, Eb | G minor |
| Eb | Bb, Eb, Ab | C minor |

## Identifying a mode from material

1. List the distinct pitch classes used and find the set that forms a seven-note scale.
2. Find the chord or note that behaves as home (starts and ends phrases, longest notes, bass pedal). That is the tonic.
3. Rotate the scale to start on the tonic and read the pattern against the table.
4. The **characteristic note** confirms it: b7 over a major triad means mixolydian; natural 6 over a minor triad means dorian; #4 over a major triad means lydian; b2 over a minor triad means phrygian.
5. If two readings fit (relative major and minor), the one whose tonic the music rests on wins; say both when it is truly ambiguous.

## Enharmonics

C# and Db are one pitch, spelled for context. Spell by letter sequence in the key: sharps in sharp keys, flats in flat keys. A diminished seventh chord is spelled in stacked minor thirds from its root (Cdim7 = C Eb Gb Bbb); never respell for convenience.

## Transposing

Shift every note by the same interval and keep letter distance: up a perfect fifth moves each letter up four steps (C to G, F to C, G to D). Tools: `chord_tools.py transpose C F G --by P5` or `--to <key>`.

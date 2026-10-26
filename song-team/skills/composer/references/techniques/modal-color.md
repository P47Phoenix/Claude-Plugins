---
loaded_by: harmony, melody
level: L3
last_reviewed: 2026-10-26
---

# Technique: Modal Color (swap-in for a brief that asks for a mode)

A swap-in, never an addition: the harmony role embeds it in place of `borrowed-chords.md`, the melody role in place of `melodic-contour.md`, only when `structure.md` names a mode other than `major` or `minor`, or when the critique says the song "sounds like every other major-key song". A role embeds at most two technique files.

## The gate's view of a mode

`chord_tools.py` builds the diatonic set from the mode named in `structure.md`; `abc_common.py` builds the key signature from `K:<tonic> <mode>`. In a mode, the plain numerals name the mode's own degrees, so the characteristic chord is **diatonic and free**:

| Mode | Diatonic triads (`I..vii` as the mode builds them) | Characteristic degree | Avoid |
|------|-----------------------------------------------------|-----------------------|-------|
| dorian | `i ii III IV v vi° VII` | `IV` major (the raised sixth) | `VI` major (that is aeolian) |
| mixolydian | `I ii iii° IV v vi VII` | `VII` major (the flat seventh) | `V` major (`v` is diatonic here; `V` costs a cell) |
| lydian | `I II iii #iv° V vi vii` | `II` major (the raised fourth) | `IV` (not in the set) |
| phrygian | `i II III iv v° VI vii` | `II` major (the flat second) | `V` major |
| aeolian | same as `minor` | `VI`, `VII` | raised `V` costs a cell |

Write the characteristic chord with a plain numeral (`VII` in mixolydian, `IV` in dorian, `II` in lydian or phrygian). Writing `bVII` in mixolydian also parses and resolves to the same pitch, but it reads as major-key thinking.

## Establishing the mode in the chart

1. Open on `i`/`I` and return to it at every section end; a mode with no tonic reference collapses into its relative major or minor.
2. Place the characteristic chord in bar 2 or bar 4 of the first phrase so the colour is heard inside the first four bars.
3. Avoid the one chord that would re-label the key: in dorian, `VI` major pulls to aeolian; in mixolydian, `V` major pulls to the major key a fourth away; in lydian, `IV` erases the raised fourth.
4. Cadences the gate recognises still apply by degree: `VII-I` in mixolydian is the `bVII-I` modal cadence; `v-i` in dorian is read as `V-I` (quality ignored); `IV-i` in dorian is plagal.
5. Original four-bar cells per mode:

```text
dorian:      | i | IV | i | VII |      | i | ii | IV | i |
mixolydian:  | I | VII | IV | I |      | I | v | VII | I |
lydian:      | I | II | I | II |       | I | II | vi | V |
phrygian:    | i | II | i | VI |       | i | II | vii | i |
```

## Writing the melody in a mode

- The characteristic scale degree is the one the melody leans on: dorian `6`, mixolydian `b7`, lydian `#4`, phrygian `b2`. Put it on a strong beat in the chorus's first phrase and on a long note somewhere in the verse.
- Never write the degree the mode lacks as a passing tone (no leading tone in mixolydian or dorian; no natural `4` in lydian). An explicit accidental (`^F` in `K:G mixolydian`) is the usual mistake.
- `K:` carries the signature, derived from the relative major: dorian = the major key a whole step below, mixolydian = a fifth below, lydian = a fifth above, phrygian = two whole steps below. So `K:D dorian` is the C-major signature (no accidentals), `K:E dorian` and `K:A mixolydian` are the D-major signature, `K:F lydian` is the C-major signature. Write the plain letter and let the signature supply the colour.
- Contour rules from `melodic-contour.md` hold (range, tessitura, leaps); the difference is colour, not shape.

## When a mode is the wrong call

A brief that says "folk" or "worship" invites mixolydian or dorian; a brief that says "pop" and "bright" is a major key, and a mode there is a critique waiting to happen. When unsure, write major and spend the budget on one borrowed `bVII`.

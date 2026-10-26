---
loaded_by: production-brief
level: L3
last_reviewed: 2026-10-26
---

# Technique: Vocal Production (the `## Vocal treatment` section, by section group)

The lead vocal is the element a listener tracks first, so its treatment carries most of the song's contrast. This file gives default chains per section group, the numbers that make them executable, and how layering follows the energy curve in `arrangement.md`. Swap it in for `production-brief` when a critique names vocal layering as the weakness.

## The chain, in order, with defaults

| Stage | Default | Range to state |
|-------|---------|----------------|
| High-pass | 80-100 Hz | 60-120 Hz; higher for a thin, airy lead |
| De-esser | moderate at 6-8 kHz | threshold set so sibilants drop 3-6 dB |
| Compression 1 | 4:1, slow attack (20-30 ms), fast release | ratio 3:1 to 6:1; attack slower to keep consonants forward |
| EQ | gentle presence lift 2-5 dB at 3-5 kHz; cut mud at 250-400 Hz | state the band and the dB |
| Compression 2 (optional) | 2:1 fast, for level evenness in choruses | |
| Saturation (optional) | tape-style or tube-style at 5-15 percent | |
| Space | plate 0.6-1.2 s with 10-30 ms pre-delay; or hall 1.5-3 s for ballads | decay in s, pre-delay in ms, wet percent |
| Delay | 1/8 or 1/4 note, 10-25 percent wet, high-passed at 1 kHz, filtered low above 6 kHz | note value, wet percent |

State every number you rely on; the producer changes them, but needs a starting point that is not a comparison.

## Layering follows the energy curve

| Energy of the section (`arrangement.md`) | Lead tracks | Doubles | Harmonies | Group / gang |
|---|---|---|---|---|
| 1-3 (verse, intro, stripped bridge) | 1, dry | none | none | none |
| 4-5 (second verse, pre-chorus) | 1 | 1 tight stereo double on the last line, or a whisper double under the whole section | none | none |
| 6-7 (first chorus) | 1 | 2 stereo doubles, panned 40 percent each side | 1 harmony a third above on lines 3-4 | none |
| 8-9 (later choruses, bridge peak) | 1 | 2-4 doubles, wider | 2 harmonies (third and fifth, or an octave up) | optional 4-8 unison tracks on the hook line only |
| 10 (everything) | 1 | 4 | 2-3 | 8 unison tracks, panned in pairs, low-passed at 8 kHz, 6 dB under the lead |

Rules that make this work:

- Doubles are the same performance repeated, not a copy: state `tracked twice` or `two takes`.
- Harmonies sit 3-6 dB under the lead and are panned off-centre; they never carry the hook line alone.
- Group vocals arrive only where `arrangement.md` lists `backing vocals`, `group vocal`, or `gang vocal` entering; the brief never invents an entry the arrangement does not have.
- The first chorus keeps one layer in reserve so the final chorus has something to add.
- Verses lose the doubles the chorus added, so the next chorus's doubles re-enter audibly.

## Genre-neutral treatments by effect

| Effect wanted | Treatment |
|---------------|-----------|
| Intimate, close | high-pass at 60 Hz, no doubles, plate at 10 percent, 20 ms pre-delay, compression 3:1 slow attack |
| Wide, anthemic | 2-4 doubles panned 40-80 percent, harmony an octave up on the hook, hall 2 s at 20 percent, 1/4-note delay at 15 percent |
| Rhythmic, forward | de-esser lighter, compression 6:1 fast attack, 1/8-note delay at 10 percent with feedback at 20 percent, no reverb in verses |
| Fragile, distant | low-pass at 6 kHz, hall 3 s at 35 percent, lead 2 dB under where it would otherwise sit, no doubles |
| Spoken or half-sung | compression 4:1, no reverb, 1/8-note slapback at 8 percent, presence lift 3 dB at 4 kHz |
| Processed, synthetic | hard pitch correction at 0 ms retune, formant shift, vocoder or harmoniser on the hook, doubles in unison detuned 8 cents |

## Instrumental songs

Write `None.` as the first word of `## Vocal treatment`, then name the lead instrument and give it the lead chain above with the stages that apply (no de-esser; the delay and space rows still apply). Layering then means unison and octave doublings of the lead instrument, following the same energy table.

## Self-check

1. Does each section group have a track count, a space setting with numbers, and a compression setting?
2. Do the doubles and harmonies increase in the order the choruses increase in `arrangement.md`?
3. Is there a layer held back for the final chorus?
4. Is every sentence a parameter or an action, never a comparison?

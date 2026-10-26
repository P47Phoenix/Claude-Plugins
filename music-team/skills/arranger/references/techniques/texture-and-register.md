---
loaded_by: arranger
level: L3
last_reviewed: 2026-10-26
---

# Technique: Texture and Register

Texture is how many independent layers play and how they are spread. Register is where those layers
sit between low, middle, and high. Together they decide what each section can add without crowding.

## Layers

| Layer | Job | Typical register |
|-------|-----|------------------|
| Pulse | Kick, bass, ostinato; keeps time | Low |
| Harmony bed | Pads, keys, strummed or picked guitar | Low-mid to mid |
| Rhythmic fill | Hi-hat, shaker, percussion, chopped chords | Mid to high |
| Lead | Vocal or lead instrument; must stay clear | Mid |
| Counter-line | Second melody, hook doubles, string line | Mid-high, away from the lead |
| Air | Cymbals, high synth, harmony stack, reverb tails | High |

A section is a choice of which layers are present and at what density. Three to four layers carry most
verses; six or more mark a chorus.

## Register spacing

- Give each layer its own band; two layers in the same octave need different rhythms or a different pan.
- Keep the lead's octave free of sustained layers; move the harmony bed a third or sixth below, or
  thin it to open fifths.
- Raise the highest layer by a few semitones or an octave in later choruses to lift without adding volume.
- Drop the bass an octave or remove it for one phrase to create a dip before a peak.
- Doubling a line an octave up widens it; doubling in unison thickens it.

## Density by section role

| Role | Density | Texture note vocabulary |
|------|---------|-------------------------|
| Intro | 1-2 layers | sparse, exposed, motif only |
| Verse | 2-4 layers | dry, close, rhythmic, single vocal |
| Pre-chorus | add 1-2 layers | rising, tightening, straight eighths, fill |
| Chorus | 5+ layers | wide, doubled, open, sustained, stacked |
| Bridge | change the layer set | stripped, half-time, suspended, new timbre |
| Outro | remove layers | thinning, fading layers, single sustained pad |

## Stereo field

Keep kick, bass, and lead vocal centered. Spread harmony beds, doubles, and air layers left and right.
Narrow the image in verses and bridges; widen it in choruses so the same chord feels bigger.

## Checks

- Every `texture_note` names a density or register fact, not a mood word alone.
- No section adds more than three layers at once except the first chorus of a build.
- Instruments that enter in a section are named in that row's `instruments_in`.

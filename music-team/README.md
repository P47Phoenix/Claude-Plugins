# music-team

A song-creation and music-theory team for Claude Code (formerly song-team). One orchestrator (`music-flow`) drives a 7-stage pipeline (Brief, Concept, Structure, Lyrics, Music, Arrangement, Release) through role-scoped skills (`lyricist`, `composer`, `arranger`, `adapter`), a critic with listener personas and an adversarial challenger (`song-critic`), and deterministic gate scripts.

## Install

```
/plugin install music-team@mec-claude-agent-skills
```

## What it does

- Writes full songs: concept, structure, lyrics, chords, ABC melody, arrangement and a release package with MIDI.
- Writes lyrics only, instrumentals, jingles, or a topline over your chords.
- Answers music-theory questions (modes, cadences, reharmonization) inline.
- Augments your own lyrics with new verses, bridges or choruses in your voice.
- Adapts your own or public-domain song into another genre (12 genre profiles) with a report of what was kept and changed.

## Example prompts

- "Write a song about leaving a small town, folk, 3 minutes."
- "Just lyrics for a gospel song about homecoming."
- "What mode is Dm7 G7 Cmaj7, and what could replace the G7?"
- "Add a bridge to my song (pasted below); it is my own work."
- "Turn my song into bossa nova; it is original, lyrics and chords below."

## Policy

Originality is enforced: no parody, no "to the tune of", no "in the style of" a named artist or song. Genre and era styles are fine. Adaptation, augmentation, rewrite and topline require that the material is yours or public domain; otherwise the request is refused with an offer to write an original. Output is text, ABC and MIDI, not audio.

## Configuration

Per-project settings live in `.song/config.yml` (quick mode, loop caps, routing pin, adaptation options); schema in `references/shared/config-schema.md`. Run data is written under `.song/<slug>/`.

See `ARCHITECTURE.md` for internals and testing.

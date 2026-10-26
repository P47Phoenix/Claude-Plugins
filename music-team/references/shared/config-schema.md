---
loaded_by: music-flow
level: L1
last_reviewed: 2026-10-26
---

# Config Schema Reference

Single source of truth for `.song/config.yml`. The setup wizard (`music-brief`), the orchestrator, every gate script, and the hooks read this file for keys, types, defaults, and consumers.

## Current version: 1

`.song/config.yml` is pure YAML with no frontmatter delimiters.

**Creation.** `music-brief` copies `music-team/.song.config.yml.example` to `.song/config.yml` when the file is absent, announces that it did so, and proceeds. `check_config.py` (SessionStart hook) only warns when the file is missing or `schema_version` is behind the current version; it never creates or edits the file.

## Complete schema (v1)

```yaml
schema_version: 1

routing:
  force_type: null            # FULL_SONG | LYRICS_ONLY | INSTRUMENTAL | TOPLINE | REWRITE | JINGLE | THEORY | ADAPT_GENRE | AUGMENT_LYRICS (REVISE is detected only, never forced)
  default_genre: null         # used when brief omits genre
  default_language: en

quick: false                  # true: every loop cap = 1, on_loop_exhaustion = accept_best, wizard asks <= 2 questions

loops:
  concept: 3
  structure: 2
  lyrics: 4
  music: 3
  arrangement: 2
  release: 2                  # number of 7b -> 4/5 returns allowed before escalation.on_blocker applies

quality:
  cliche_max_per_100_words: 2
  hook_max_syllables: 12
  prosody_tolerance: 0.15     # max per-section mismatch ratio: missed S beats + syllable-count drift, over the meter's S count
  slant_rhyme_allowed: true
  diatonic_min_ratio: 0.6     # fraction of chords that must be diatonic
  max_melodic_leap: 12        # semitones
  vocal_range: [55, 79]       # MIDI note numbers, G3..G5 default
  energy_curve: chorus_rising # chorus_rising | strict_rising | free (see stage-gates.md)
  adversarial_lyrics: false   # run challenger after Stage 4 too, not only Stage 7
  listener_panel_size: 3
  genre_overrides: {}         # e.g. hip-hop: { hook_max_syllables: 16, diatonic_min_ratio: 0.4 }

originality:
  resemblance_corpus: []      # OPT-IN: paths to user-supplied lyric files the song must not resemble
  ngram_max_overlap: 0.05     # applied only when resemblance_corpus is non-empty
  block_artist_references: true

escalation:
  on_loop_exhaustion: ask_user   # ask_user | accept_best | fail
  on_blocker: ask_user           # ask_user | accept_best | fail

adaptation:
  require_report: true        # ADAPT_GENRE Stage 7 needs adaptation-report.md
  max_changed_elements: 12    # max rows in the report's ## Changed table

memory:
  enabled: true
  path: .song/memory/

telemetry:
  enabled: false              # Wave 5 feature
```

## Key reference

| Key | Type | Default | Valid values | Used by |
|-----|------|---------|--------------|---------|
| `schema_version` | integer | 1 | 1 | `check_config.py` (staleness warning), `music-flow` |
| `routing.force_type` | string or null | null | FULL_SONG, LYRICS_ONLY, INSTRUMENTAL, TOPLINE, REWRITE, JINGLE, THEORY, ADAPT_GENRE, AUGMENT_LYRICS, null | `music-brief` Stage 1 (detection still runs and is logged; routing uses the pin; banner each run) |
| `routing.default_genre` | string or null | null | any genre file name (`pop`, `rock`, `country`, `folk`, `hip-hop`, `rnb`, `electronic`, `musical-theatre`, `childrens`, `worship`) | `music-brief` when the brief omits genre |
| `routing.default_language` | string | en | ISO 639-1 code | `music-brief` writes `brief.md.language`; gates SKIP when not `en` |
| `quick` | boolean | false | true, false | `music-flow` (loop caps, escalation), `music-brief` (wizard length) |
| `loops.concept` | integer | 3 | 1+; 0 means no retry, escalate on first FAIL | `music-flow` Stage 2 cap |
| `loops.structure` | integer | 2 | 1+; 0 means no retry, escalate on first FAIL | `music-flow` Stage 3 cap |
| `loops.lyrics` | integer | 4 | 1+; 0 means no retry, escalate on first FAIL | `music-flow` Stage 4 cap |
| `loops.music` | integer | 3 | 1+; 0 means no retry, escalate on first FAIL | `music-flow` Stage 5 cap |
| `loops.arrangement` | integer | 2 | 1+; 0 means no retry, escalate on first FAIL | `music-flow` Stage 6 cap |
| `loops.release` | integer | 2 | 1+; 0 means no retry, escalate on first FAIL | `music-flow` release loop (7b returns to 4/5) |
| `quality.cliche_max_per_100_words` | number | 2 | >= 0 | `cliche_scan.py` (Stages 2, 4, challenger) |
| `quality.hook_max_syllables` | integer | 12 | 1+ (equal passes; non-integer -> ERROR) | `prosody_check.py --hook` (Stage 2) |
| `quality.prosody_tolerance` | number | 0.15 | 0.0-1.0; a section FAILs when (unstressed spec-`S` positions + abs syllable-count difference per line + extra/missing-line penalties) / count of `S` in its `meter_spec` exceeds this (equal passes). Non-numeric -> ERROR | `prosody_check.py` (Stage 4) |
| `quality.slant_rhyme_allowed` | boolean | true | true, false (other -> ERROR) | `rhyme_check.py` (Stage 4) |
| `quality.diatonic_min_ratio` | number | 0.6 | 0.0-1.0 | `chord_tools.py` (Stage 5) |
| `quality.max_melodic_leap` | integer | 12 | 1+ semitones | `abc_validate.py` (Stage 5) |
| `quality.vocal_range` | [integer, integer] | [55, 79] | MIDI 0-127, low <= high | `abc_validate.py` (Stage 5), `structure_check.py --consistency` (Stage 6) |
| `quality.energy_curve` | string | chorus_rising | chorus_rising, strict_rising, free | `arrangement_check.py` (Stage 6) |
| `quality.adversarial_lyrics` | boolean | false | true, false | `music-flow` (extra challenger pass after Stage 4) |
| `quality.listener_panel_size` | integer | 3 | 1-12 | `music-flow` Stage 7a persona count (allowance manifest caps embedded personas at 3) |
| `quality.genre_overrides` | map[genre, map[key, value]] | {} | any `quality.*` scalar key | every gate script via threshold precedence |
| `originality.resemblance_corpus` | list[string] | [] | file paths | `resemblance_check.py` (Stage 7b; SKIPPED when empty) |
| `originality.ngram_max_overlap` | number | 0.05 | 0.0-1.0 | `resemblance_check.py` |
| `originality.block_artist_references` | boolean | true | true, false | `audit_agent_prompt.py` (blocked-targets check) |
| `escalation.on_loop_exhaustion` | string | ask_user | ask_user, accept_best, fail | `music-flow` protocol step 5 |
| `escalation.on_blocker` | string | ask_user | ask_user, accept_best, fail | `music-flow` release loop |
| `adaptation.require_report` | boolean | true | true, false | `adapt_check.py` (Stage 7, ADAPT_GENRE; Wave 7) |
| `adaptation.max_changed_elements` | integer | 12 | 1+ | `adapt_check.py` (Wave 7) |
| `memory.enabled` | boolean | true | true, false | `music-memory`, `music-flow` lessons block |
| `memory.path` | string | .song/memory/ | directory path | `music-memory`, `music-flow` |
| `telemetry.enabled` | boolean | false | true, false | `telemetry.py` (Wave 5) |

## Quick mode semantics

`quick: true`, or the phrase "quick song" in the brief, has exactly these effects for the run: every `loops.<stage>` is treated as 1 (including `release`); `escalation.on_loop_exhaustion` is treated as `accept_best`; the wizard asks at most 2 of its 6 questions, choosing the first unanswered ones in order (genre, mood, theme, audience, length, anything-to-avoid) and inferring the rest. The file on disk is not modified; `state.json` records `quick: true`.

## genre_overrides semantics

`quality.genre_overrides.<genre>` is a map of `quality.*` scalar keys to values. It applies when the resolved genre (from `--genre`, else `brief.md.genre`) matches the map key exactly (lower-case, hyphenated as the genre file name). Threshold precedence is: explicit script flag > `genre_overrides.<genre>.<key>` > `quality.<key>` > built-in default. Only scalar keys may be overridden; `vocal_range` may be overridden as a two-element list. Unknown keys are reported as a warning by `check_config.py` and ignored by scripts.

## Extension protocol

- **Minor (additive):** a new optional key with a default. Keep `schema_version` integer-valued but add a migration note here under "Migration notes" with the version that introduced the key. Scripts must treat a missing key as its default, so older files keep working.
- **Major (breaking):** renaming, removing, or changing the type or meaning of a key. Bump `schema_version` to the next integer; `check_config.py` warns on any file behind the current version; add a migration note with the old key, the new key, and a one-line conversion rule. Never auto-migrate on disk.
- Every new key must name its consumer in the key reference table and, if it is a threshold, its script in `stage-gates.md`.

## Migration notes

- **v1 (2026-10-26):** initial schema. No prior versions.
- **v1 minor (2026-10-26):** additive: `routing.force_type` accepts THEORY, ADAPT_GENRE, AUGMENT_LYRICS; new `adaptation:` block. Missing keys take the defaults above; `schema_version` stays 1.

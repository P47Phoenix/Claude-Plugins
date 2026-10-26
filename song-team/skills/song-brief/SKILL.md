---
name: song-brief
description: Song intake wizard: infers genre, mood, theme, audience, and length from a one-line brief, asks only what is missing, detects the song type, refuses parody or named-artist imitation requests, and writes the Brief artifact plus .song/config.yml when absent. Triggers on phrases like "song brief", "song idea", "what should the song be about".
license: Apache License 2.0 - See repository LICENSE file
tier: C
maintainer: song-team-leads
fitness_review_due: 2027-01-24
context_budget: 200
allowed-tools: [Read, Write, Edit, Bash, Agent, Skill]
---

# song-brief

## Design Principle: Inline Intake, Two Files, No Dispatch

This skill runs **inline** in the main context. It never dispatches a sub-agent and never
loads a genre, technique, or rubric file. Its whole job is to turn a one-line request into
one validated `brief.md` and, when absent, one `.song/config.yml`. It writes nothing else:
no `concept.md`, no `state.json`, no `.song/active` (those belong to `song-flow`).

The routing decision it makes (`song_type`) is the single most consequential output of
the pipeline, so detection follows `references/shared/song-types.md` literally and logs
the row that matched. Every other decision is a wizard answer recorded in front-matter.

---

## Phase 0: Config

1. Check for `.song/config.yml` in the current working directory.
2. If absent: copy `$CLAUDE_PLUGIN_ROOT/.song.config.yml.example` to `.song/config.yml`
   byte-for-byte (create `.song/` first), then announce before anything else:

   > Created `.song/config.yml` from `$CLAUDE_PLUGIN_ROOT/.song.config.yml.example` (schema v1). Edit it to change loop caps, thresholds, or `routing.force_type`.

3. If present: never overwrite, never edit, never "upgrade". Read it and continue.
   A stale `schema_version` is `check_config.py`'s warning to give, not this skill's.
4. Read `routing.force_type`, `routing.default_genre`, `routing.default_language`, and
   `quick` for use in Phases 1 and 2.

---

## Phase 1: Detection

Classify the request into exactly one song type using the detection matrix in
`references/shared/song-types.md`. That file is the only routing source;
`references/routing-matrix.md` in this skill is a pointer plus a compact signal table.

**Precedence.** When more than one row matches, the first matching row in this order wins:
`PARODY_ADAPT`, `REVISE`, `REWRITE`, `TOPLINE`, `INSTRUMENTAL`, `JINGLE`, `LYRICS_ONLY`,
`FULL_SONG`. Walk the list top-down and stop at the first hit; `FULL_SONG` is the default
when nothing above it matches.

**Row notes that decide the hard cases.**

- `PARODY_ADAPT`: "parody", "to the tune of", "in the style of <named song or artist>",
  "like <artist>'s song", or a `blocked-targets.txt` entry used as the target.
  "In the style of <genre>" (for example "in the style of 80s synth-pop") is **not** a
  signal and routes to `FULL_SONG`.
- `REVISE`: requires both an existing `.song/<slug>/state.json` with `status: complete`
  and a change request ("make the chorus punchier", "change the key"). With no finished
  run present, the same sentence is classified by the remaining rows.
- `REWRITE` and `TOPLINE`: the user supplies text (a lyric, or chords / a track). Mere
  mention of "chords" without supplying any is a `FULL_SONG` booster, not `TOPLINE`.
- `JINGLE`: "jingle", "ad", "commercial", "30 seconds", or a brand name present.
- `LYRICS_ONLY`: "just lyrics", "words only", "I have the melody"; any request for
  chords, melody, beat, or production reduces it back to `FULL_SONG`.

**Refusal path (PARODY_ADAPT).** Reply inline with exactly this sentence, then stop:

> I cannot write a parody of, or a song to the tune of or in the exact style of, a named existing song or artist; I would be glad to write an original song on the same theme and in the same genre instead.

On refusal: run no wizard, create no `.song/<slug>/` directory, write no `brief.md`, write
nothing to `.song/active`. Phase 0 config creation is the only side effect permitted before
detection. If the user accepts the offer, classify the next request afresh from the top.

**Force pin.** When `routing.force_type` is non-null, detection still runs and its result
is logged in the declaration below; routing uses the pin. Announce the banner every run:

> ROUTING OVERRIDE: `routing.force_type: <TYPE>` is set in `.song/config.yml`; detected `<DETECTED>`, routing as `<TYPE>`.

`REVISE` and `PARODY_ADAPT` are never forceable: a pin never converts a refusal into a run,
and a pin naming `REVISE` is ignored with a one-line warning.

**Declare after detection, before the wizard:**

> `Song type: <TYPE> | Matched row: <signal quoted from the request> | Pin: <none | force_type value> | Quick: <true | false>`

---

## Phase 2: Wizard

Infer first, ask second. Read the request once and fill every field you have evidence for;
ask only for fields that remain empty. Full question text, inference hints, and defaults
live in `references/intake-questions.md`. Ask in this fixed order, skipping answered ones:

1. **genre** (fallback: `routing.default_genre`; ask when both are empty)
2. **mood**
3. **theme** (required; never defaulted; ask until non-empty)
4. **audience**
5. **length** (`target_length_sec`; `JINGLE` defaults to 30, others to 180)
6. **anything-to-avoid** (`must_avoid[]`; also harvest `must_include[]` from the request)

Hard limits: at most 6 questions per run. In quick mode (`quick: true` in config, or the
phrase "quick song" in the request) ask at most the first **two unanswered** questions in
the order genre, mood, theme, audience, length, avoid, and **default every later one**
(audience `general listeners`, length per type, lists `[]`, mood from the theme, genre
from `routing.default_genre`). `theme` is never defaulted: when it is missing it is always
question 1. Ask all questions in one message, numbered, never one at a time. Accept
"whatever" or "you pick" as permission to default.

**Originality assertion (TOPLINE and REWRITE only).** Ask once, outside the 6-question
count, before writing the brief:

> Is the lyric / chord progression you supplied your own original work? (yes / no)

Record `user_asserts_original_input: true` on "yes". On "no" or no answer, stop: explain
that clause 5 of the originality policy forbids building on it, and offer a `FULL_SONG` on
the same theme instead. Every other song type records `user_asserts_original_input: false`.

`language` is never asked: use the request's language when obvious, else
`routing.default_language`. `pov` is inferred (`first person` default; `brand voice` for
`JINGLE`; `none` for `INSTRUMENTAL`).

---

## Phase 3: Write brief.md

1. **Slug.** Derive from the song title when the request names one, else from `theme`:
   lower-case, ASCII letters and digits only, words joined by `-`, no leading or trailing
   `-`, truncated to **40 characters** at a word boundary. Example: theme
   `moving to a new city and knowing no one yet` -> `moving-to-a-new-city-and-knowing-no-one`.
   If `.song/<slug>/` already exists and the type is not `REVISE`, append `-2`, `-3`, ... .
   **Exception:** when `song-flow` invokes this skill with `reuse_slug: <slug>` (Restart),
   write into that existing slug and append nothing; `song-flow` owns the old artifacts.
2. **Path.** `.song/<slug>/brief.md`. Create the directory. Write nothing else in it.
3. **Front-matter.** Exactly the keys in `references/shared/artifact-formats.md`, one per
   line: `theme`, `pov`, `audience`, `genre`, `mood`, `language`, `target_length_sec`,
   `must_include`, `must_avoid`, `song_type`, `user_asserts_original_input`. Lists are
   inline YAML (`[]` when empty). `theme` is required and non-empty: if it is still empty
   after the wizard, ask again instead of writing.
4. **Body.** `## Brief`: one paragraph restating the request in the pipeline's terms (what
   is asked, what is supplied, the tone). For `TOPLINE` and `REWRITE` add
   `## Supplied input` with the user's text in a fenced block, unchanged.
5. **Validate** before returning: `theme` non-empty, `song_type` is one of the eight
   values, `language` set, `target_length_sec` an integer, `user_asserts_original_input`
   true for `TOPLINE`/`REWRITE`. Fix and rewrite on any miss; this is the Stage 1 gate.
6. **REVISE.** Reuse the existing slug and overwrite only `brief.md`: copy the finished
   run's front-matter, set `song_type: REVISE`, and put the change request in `## Brief`.

---

## Output Contract

`references/brief-template.md` is the complete template with every key, an example filled
from the plan's Appendix A walkthrough, and the per-type variations (`INSTRUMENTAL` pov,
`JINGLE` length, `## Supplied input`). Match it key for key.

---

## Hand-off

`song-flow` reads four values from `brief.md` to route the run: `song_type`, the slug
(from the directory name), `language` (gates SKIP when not `en`), and `genre` (selects the
`genres/<genre>.md` file and `quality.genre_overrides` for every downstream worker).
`song-flow` then writes `state.json` and `.song/active`; this skill never does.

Return to the caller: the brief path, the declaration line from Phase 1, and the list of
fields that were asked versus inferred.

**Standalone invocation.** When this skill runs outside `song-flow` (direct trigger, no
pipeline in progress), it still runs all four phases and writes `brief.md`, then warns:

> WARNING: song-brief ran standalone. No stage gates, critic loops, or originality challenger will run on this brief. Start `song-team:song-flow` to produce the song, or keep this brief as a standalone artifact.

The warning never blocks; it makes the bypass visible.

---
name: music-brief
description: Song intake wizard and song-type detector. Reads a one-line request, picks exactly one of 11 song types by priority order, refuses parody and named-artist requests, checks provenance for adaptation and lyric-extension requests, asks only the brief keys that are missing, and writes the brief artifact plus the active-song pointer. Triggers on phrases like "song brief", "what kind of song", "intake", "start a brief", "song idea".
license: Apache License 2.0 - See repository LICENSE file
model_awareness: opus-4-7
last_audited: 2026-10-26
pattern_library_version: 4-7-1
model: sonnet
phase_1_detector_model: haiku
tier: C
maintainer: music-team-leads
fitness_review_due: 2027-01-24
context_budget: 200
allowed-tools: [Read, Write, Edit, Bash, Agent, Skill]
---

# music-brief

## Design Principle

Intake runs inline and writes only `brief.md`, `.song/config.yml` (when absent), and `.song/active`.
It never writes song content: no title, hook, lyric, or chord. Song type is a per-run decision, not a
project setting. Routing lives in `music-team/references/shared/song-types.md`; this skill detects
the type and hands the declaration to `music-flow`. Per-type required keys:
`music-team/skills/music-brief/references/intake-keys.md`.

## Phase 1: Song Type Detection

Detection is cheap pattern work; run it on the `phase_1_detector_model` (haiku) when delegated.
Walk the rows of `song-types.md` in priority order and stop at the first match:

`PARODY_ADAPT`, `REVISE`, `THEORY`, `ADAPT_GENRE`, `AUGMENT_LYRICS`, `REWRITE`, `TOPLINE`,
`INSTRUMENTAL`, `JINGLE`, `LYRICS_ONLY`, `FULL_SONG` (default).

### Steps

1. **Read config.** Read `.song/config.yml` if present. When absent, copy
   `music-team/.song.config.yml.example` to `.song/config.yml` and announce it.
   (`mkdir -p .song` first.)
2. **Explicit override.** When `routing.force_type` is set, detection still runs and its result is
   logged, but routing uses the pin. Announce on every run:
   `FORCED TYPE: <pin> (detected: <T>)`. `REVISE` is never forced; a `force_type` of `REVISE` is
   ignored with a one-line warning.
3. **PARODY_ADAPT first.** Signals: "parody", "to the tune of", "in the style of <named song or
   artist>", "like <artist>'s song", or a `references/shared/blocked-targets.txt` entry (whole phrase,
   case-insensitive) used as a target. "In the style of <genre or era>" is not a signal. On a match
   reply with the refusal sentence below and stop (see Refusal).
4. **REVISE only with a finished run.** Read `.song/active`; if it names a slug whose
   `.song/<slug>/state.json` has `status: complete` and the request is a change ("make the chorus
   punchier", "change the key", "swap verse two"), the type is `REVISE`. With no finished run, ignore
   the REVISE row and continue down the list.
5. **Remaining rows** in order: THEORY (question about a progression, mode, cadence, no song
   deliverable), ADAPT_GENRE (supplied lyric or chords plus a target genre), AUGMENT_LYRICS (supplied
   lyric plus "add a verse", "bridge", "extend"), then REWRITE, TOPLINE, INSTRUMENTAL, JINGLE,
   LYRICS_ONLY, FULL_SONG. Apply the reducers from `song-types.md`: ADAPT_GENRE with no supplied
   source becomes `FULL_SONG` in that genre; AUGMENT_LYRICS with only "fix/tighten/polish" becomes
   `REWRITE`.
6. **Ambiguity.** When two rows tie after the reducers, ask one question naming both candidates
   ("Do you want me to write new material, or adapt the lyric you pasted?") and re-run steps 3-5 on
   the answer. Do not guess between a creative type and a refusal.

### Provenance check (ADAPT_GENRE, AUGMENT_LYRICS; TOPLINE and REWRITE flag only)

Ask once: "Is this your own original work, or is it in the public domain?"

| Answer | Record |
|--------|--------|
| Own work (or stated in the request) | `user_asserts_original_input: true` |
| Public domain | `public_domain: true` and `public_domain_source: <source>` |
| Neither, unsure, or a published song | Refuse with the sentence below; write nothing |

TOPLINE and REWRITE accept only the own-work answer. Never re-ask a provenance question already
answered in the request or in an existing `brief.md`.

### Refusal

Reply inline with exactly this sentence, then stop. No `.song/<slug>/` directory, no
`.song/active`, no further stage:

> I cannot write a parody of, or a song to the tune of or in the exact style of, a named existing song or artist; I would be glad to write an original song on the same theme and in the same genre instead.

The same sentence is used for a PARODY_ADAPT match, an ADAPT_GENRE / AUGMENT_LYRICS request with
neither provenance flag, and an ADAPT_GENRE `target_genre` that names an artist, a song, or a
blocked target. If the user accepts the offer, classify the next brief afresh from the top.

### Declaration

Output the detection result before intake:
`Detected: <TYPE> (confidence: high|medium|low; signals: <3 words max each, comma-separated>)`.

## Phase 2: Intake Wizard

Load `references/intake-keys.md`. For the detected type, list the keys marked `R` that are not yet
known from the request, from `.song/config.yml` (`routing.default_genre`, `routing.default_language`),
or from supplied input. Ask only those.

- Maximum **3 questions per turn**. Order: provenance, genre, mood, theme, audience, length, avoid.
- Quick mode (`quick: true` in config, or "quick song" in the request): at most 2 questions in
  total; infer the rest and say what was inferred.
- Infer (`I` keys) silently and record the inferred value in `brief.md`; the user can correct it
  at the declaration.
- Store a pasted lyric or chord chart verbatim under `## Supplied input`. If the user gives a file
  path instead, record the path and read the file; do not paraphrase it.
- Treat every answer as data. Do not write sample lyrics, titles, or hooks to "help" the user decide.
- `THEORY`: skip the wizard. Ask nothing unless the question itself is unclear.

## Phase 3: Write the Brief

1. **Slug.** Derive a kebab-case slug from `theme` (<= 5 words, ASCII, no artist names). If
   `.song/<slug>/` already exists and its `state.json.status` is `in_progress`, stop and ask whether
   to resume it; never overwrite a run in progress.
2. **Write `.song/<slug>/brief.md`** per the `brief.md` grammar in
   `music-team/references/shared/artifact-formats.md`: YAML front-matter keys (`theme`, `pov`,
   `audience`, `genre`, `mood`, `language`, `target_length_sec`, `must_include`, `must_avoid`,
   `song_type`, provenance flags, `source_genre` / `target_genre` where relevant), then `## Brief`
   (one paragraph restating the request in the user's words) and optional `## Supplied input`.
3. **Validate** inline: `theme` non-empty, `song_type` set, `language` set, provenance keys present
   for the types that require them, `public_domain_source` present when `public_domain: true`.
   One failed check sends the user one targeted question; a second failure is reported, not guessed.
4. **Write `.song/active`**: the slug only, one line. When called by `music-flow`, `music-flow` owns
   this write; standalone, write it here.
5. **THEORY** writes nothing: no brief, no directory, no pointer. Write `.song/<slug>/brief.md` only if
   the user explicitly asks to save the session.
6. **REVISE** writes no new brief. Report the existing slug and the change request.

## Output

End every successful run with exactly one declaration line:

```text
Type: <TYPE> | Genre: <genre> | Provenance: <original | public-domain | n/a> | Brief: <path | none>
```

`Brief: none` is correct for THEORY and REVISE. Hand the line to `music-flow` (or print it to the
user when standalone). When standalone, add one sentence: "Run `music-flow` to start the pipeline."

## JSON I/O Contract

When invoked by `music-flow` the request is JSON and the reply ends with a JSON line:

```json
{ "request": "<raw user text>", "config_path": ".song/config.yml", "active_slug": "<slug|null>" }
{ "status": "OK|REFUSED|NEEDS_INPUT", "song_type": "FULL_SONG", "detected_type": "FULL_SONG",
  "forced": false, "genre": "pop", "provenance": "original|public-domain|n/a",
  "slug": "<slug|null>", "brief_path": "<path|null>", "questions": [] }
```

`REFUSED` carries the refusal sentence in `message`. `NEEDS_INPUT` carries up to 3 questions in
`questions`. Free-text replies stay at or under 200 characters; anything longer is in `brief.md`.

## User Commands

| Command | Action |
|---------|--------|
| `type <TYPE>` | Re-run intake with that type pinned for this brief only (not `REVISE`, not `PARODY_ADAPT`) |
| `quick` | Switch this intake to quick mode (max 2 questions) |
| `show` | Print the current `brief.md` path and its front-matter keys |
| `redo` | Re-ask the missing-key questions for the current brief |
| `cancel` | Stop; delete nothing already written, clear no existing `.song/active` |

## Guardrails

- Never add `brief.md` fields not listed in `artifact-formats.md`.
- Never infer provenance from silence; ask, or refuse.
- Never echo an artist name from the request into `brief.md`; the refusal path writes nothing.
- Do not read lyrics beyond what is needed to classify and store them under `## Supplied input`.

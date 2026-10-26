---
loaded_by: song-brief
level: L2
last_reviewed: 2026-10-26
---

# Intake Questions

The wizard asks at most six questions, in this order, and only for fields the request
leaves empty after inference. Quick mode (`quick: true`, or "quick song" in the request)
asks at most the first two unanswered questions in the order genre, mood, theme,
audience, length, avoid, and defaults every later one. `theme` is never defaulted: when
it is missing it is always question 1. Ask every pending question in a single numbered
message.

Three fields are never asked: `language` (request language, else
`routing.default_language`), `pov` (inferred per song type), and
`user_asserts_original_input` (its own yes/no prompt, TOPLINE and REWRITE only, outside
the six-question count).

## Q1 genre

**Ask:** "What genre? (pop, rock, country, folk, hip-hop, rnb, electronic,
musical-theatre, childrens, worship, or name another)"

- **Infer from:** a genre word in the request ("indie-pop" -> `pop`, sub-tag noted in the
  brief body; "singer-songwriter" -> `folk`; "trap" / "drill" -> `hip-hop`; "EDM" /
  "house" / "synth-pop" -> `electronic`; "ambient" / "score" -> `ambient`), a named
  instrument palette ("banjo and fiddle" -> `country`), or "in the style of <genre>".
- **Default:** `routing.default_genre` when set. When null, ask; genre selects the
  `genres/<genre>.md` file every downstream worker loads, so it is never guessed blind.
- **Record as:** lower-case, hyphenated, matching a genre file name where one exists.

## Q2 mood

**Ask:** "What mood or emotional colour? (one or two words: upbeat, wistful, tender,
defiant, dreamy, calm, cheerful...)"

- **Infer from:** adjectives in the request ("upbeat", "sad", "angry", "chill"), the theme
  itself (a funeral is not `cheerful` unless the user says so), and the genre's default
  register only as a last resort.
- **Default:** `JINGLE` -> `cheerful`; `INSTRUMENTAL` with a scene described -> the scene's
  adjective; otherwise ask.
- **Record as:** one or two lower-case words.

## Q3 theme

**Ask:** "What is the song about? One sentence is enough."

- **Infer from:** the "about ..." clause, the scene described, the supplied lyric's subject
  (REWRITE), or the tagline and product (JINGLE: the product and what it does).
- **Default:** none. `theme` is the only required key; the wizard asks until it is
  non-empty. In quick mode a missing theme is always question 1, ahead of genre and
  mood, and spends one of the two questions.
- **Record as:** a single lower-case phrase, no trailing period, no named artist or song.

## Q4 audience

**Ask:** "Who is this for? (an age range, a scene, a listener type, or a client)"

- **Infer from:** "for my daughter's birthday" -> `a child turning N`; "for our wedding" ->
  `wedding guests`; "for radio" -> `local radio listeners`; a brand -> that brand's
  customers; a film scene -> `film and documentary producers`.
- **Default:** `general listeners` when unstated and nothing in the request narrows it.
  Prefer asking in full mode; in quick mode default it unless it is one of the first two
  unanswered questions.
- **Record as:** a short noun phrase.

## Q5 length

**Ask:** "How long? (seconds, or a rough minute mark; jingles are 15 to 60 seconds)"

- **Infer from:** "30 second", "three minutes", "radio edit" (-> 180), "epic" / "album
  closer" (-> 300), "short" (-> 120).
- **Default:** `JINGLE` -> 30; every other type -> 180. `JINGLE` is a hard cap at Stage 3
  (`form_template: jingle`), so confirm it in full mode when the request gives no number.
- **Record as:** `target_length_sec`, an integer. Convert minutes to seconds.

## Q6 anything-to-avoid

**Ask:** "Anything to avoid or anything that must be in it? (words, images, names,
instruments, topics)"

- **Infer from:** "no drums", "don't mention her name", "keep it clean" -> `must_avoid`;
  "it has to mention the ferry", a supplied tagline, "use the word home" -> `must_include`.
  A brand name in a `JINGLE` always lands in `must_include`.
- **Default:** both lists empty (`[]`). Named artists and song titles never enter either
  list as targets; if the user names one as an influence, drop it and note in the brief
  body that genre-level description replaced it.
- **Record as:** inline YAML lists, each item a short phrase, quoted when it contains a
  colon or comma.

## Originality assertion (TOPLINE and REWRITE only)

**Ask:** "Is the lyric / chord progression you supplied your own original work? (yes / no)"

- Asked exactly once, after detection and before writing the brief; not counted against
  the six-question limit, and asked even in quick mode.
- "yes" -> `user_asserts_original_input: true`. "no", silence, or a hedge ("sort of",
  "I changed a few words") -> stop, cite clause 5 of
  `references/shared/originality-policy.md`, and offer a `FULL_SONG` on the same theme.
- If the supplied text is recognised as a well-known existing lyric, treat it as "no"
  regardless of the answer (clause 4).

## Inference order of precedence

1. Explicit statement in the request.
2. Supplied input (REWRITE lyric, TOPLINE chords) for theme, pov, and length.
3. Config defaults (`routing.default_genre`, `routing.default_language`).
4. Type defaults listed above (JINGLE length and mood, INSTRUMENTAL pov).
5. Ask.

Record in the return message which fields came from which rung, so `song-flow` and the
retrospective know what the user chose versus what the wizard assumed.

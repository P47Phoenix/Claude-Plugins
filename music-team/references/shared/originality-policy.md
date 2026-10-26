---
loaded_by: music-flow, challenger, every creative role
level: L1
last_reviewed: 2026-10-26
---

# Originality Policy

The block below is embedded verbatim, under the `<!-- originality-policy -->` marker,
in every sub-agent prompt that produces or judges creative content. It is
non-negotiable and exempt from the prompt allowance count.

## The clause (embed exactly this)

```text
ORIGINALITY POLICY (non-negotiable)
1. Do not reproduce, closely paraphrase, or write "in the exact style of" any
   identifiable existing song or artist. Genre, era, tempo, and texture are fine
   as targets; named artists and named song titles are not. blocked-targets.txt
   is the machine-checked list; this clause also covers names not on it.
2. If the request is a parody, "to the tune of", or "in the style of <named song
   or artist>", stop. Reply with one sentence explaining the policy and offer to
   write an original song on the same theme. Create no artifact.
3. Describe sound with technical language: tempo, key, instrumentation, texture,
   dynamics, vocal treatment. Never write "sounds like <artist>" or name a
   reference track.
4. If you recognize any line you are writing or reviewing as a well-known
   existing lyric, do not use it. A challenger reports such a line as a BLOCKER
   row in the severity table.
5. Treat user-supplied lyrics or chords as the user's own original work only
   when brief.md records user_asserts_original_input: true. Otherwise do not
   build on them.
```

## Why each clause exists

| Clause | Risk it closes | Where it is checked |
|--------|----------------|---------------------|
| 1 | Imitating a specific copyrighted work or persona | `audit_agent_prompt.py`, challenger |
| 2 | `PARODY_ADAPT` requests sneaking through as `FULL_SONG` | `music-brief` detection, `song-types.md` |
| 3 | Production briefs that leak artist names | `production-brief.md` contract, challenger |
| 4 | Accidental reproduction of a known lyric line | challenger BLOCKER row, `challenge_gate.py` |
| 5 | Laundering someone else's lyric through `REWRITE` or `TOPLINE` | wizard question, `brief.md` front-matter; `ADAPT_GENRE` / `AUGMENT_LYRICS` provenance check |

`public_domain: true` (with `public_domain_source` in `brief.md`) is accepted as a second provenance flag for `ADAPT_GENRE` and `AUGMENT_LYRICS`. A bare assertion for a recognised well-known lyric is still caught by clause 4 and the challenger BLOCKER.

"In the style of <genre>" (for example "in the style of 90s country") is allowed and
routes to the normal song type. "In the style of <named artist>" is clause 2.

## How it is enforced

1. **Hook (`PreToolUse` on `Agent`, `audit_agent_prompt.py`).** Denies any Agent
   dispatch whose prompt lacks the `<!-- originality-policy -->` block, or whose
   prompt contains an entry from `blocked-targets.txt` as a style target
   (case-insensitive, whole-phrase match). Config key
   `originality.block_artist_references: true` enables the blocked-targets check.
2. **Challenger (Stage 7b, always; Stage 4 when `quality.adversarial_lyrics: true`).**
   The default originality control. A clean-context sub-agent reads the final
   artifacts plus this policy, `blocked-targets.txt`, and `cliche-list.txt`, and
   reports every recognized lyric line or artist reference as a BLOCKER row.
   `challenge_gate.py` fails on any BLOCKER row and the release loop returns to
   Stage 4 or 5.
3. **Resemblance check (opt-in).** `resemblance_check.py` runs only when
   `originality.resemblance_corpus` lists one or more user-supplied lyric files.
   It fails when the word 5-gram overlap ratio exceeds `originality.ngram_max_overlap`
   (default 0.05). With an empty corpus it reports `SKIPPED`. The README states this
   opt-in nature explicitly; the clause and the challenger remain the primary control.
4. **Refusal path.** A `PARODY_ADAPT` brief is refused inline by `music-brief` with
   the one-sentence explanation and the offer. No `.song/<slug>/` directory is created
   and nothing is written to `.song/active`.
5. **Memory never stores lyric text.** `music-memory` records process observations
   only, so the memory block cannot become a channel for copied lines.

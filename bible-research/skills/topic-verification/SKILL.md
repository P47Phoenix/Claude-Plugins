---
name: topic-verification
description: Verifies the claims made by external artifacts - a worship song or hymn, a website or article, a social-media post or meme, a sermon transcript, video or podcast, a devotional - rather than a draft the user is writing. Extracts the claims, routes each to the sermon-verification checks, grades the source, and returns a per-claim verdict table with plain-language guidance on what is fine to sing or share and what to be careful with. Triggers on phrases like "is this song theologically sound", "check these lyrics", "check this hymn", "fact-check this post", "is this article accurate", "someone shared this", "check this sermon I heard", "check this video", "check this devotional", "is this meme true", "full check".
license: Apache License 2.0 - See repository LICENSE file
last_audited: 2026-10-30
tier: B
maintainer: bible-research-leads
fitness_review_due: 2027-01-28
allowed-tools:
  - Read
  - Write
  - Agent
  - WebFetch
  - WebSearch
---

# Topic Verification

## Design Principle: Artifact Isolation

The artifact being checked (a song, a page, a post, a transcript) and the checking knowledge both stay **out of the main context window** as much as possible. The router classifies, spawns sub-agents, and returns one finished report. This skill **composes** `sermon-verification`: it reuses that skill's reference files and never duplicates them.

- Claim extraction runs in one sub-agent that carries `claim-extraction.md` and the type reference
- Each verification check runs in its own sub-agent that carries one `sermon-verification` reference
- Report assembly runs in one sub-agent that carries the grading and pattern references

**Nested spawning.** Per the current Claude Code docs, a subagent can spawn further subagents (default depth limit 3). This skill does not rely on that. The router spawns every sub-agent itself (a flat fan-out), so it works with the depth limit set to 1. See `DESIGN_NOTES.md`.

---

## Phase 1: Task Classification

Detect the task type from the request, in priority order:

1. **User command** -- `/check <text|url|file> [song|web|post|transcript|full]`
2. **Explicit keywords** (routing table)
3. **Input shape** -- a URL (-> `web`, unless it is a video or podcast page, -> `transcript`); pasted lyrics (-> `song`); a short social-media-style text (-> `post`)
4. **Artifact referenced** -- a file path

**If ambiguous, ask.** Declare before every task:

> `Task Type: [TYPE] | References: [FILE(S)] | Scope: [BRIEF DESCRIPTION OF THE ARTIFACT, NOT ITS TEXT]`

### Getting the Artifact

- **Pasted text:** use as given
- **URL:** fetch it with `WebFetch`. **Do not fetch lyrics sites** (for example Genius, AZLyrics, Musixmatch or similar). For a song, ask the user to paste the lyrics (guardrail 9). The user supplies the text; the plugin does not fetch lyrics
- **File path:** `Read` it
- **Video or podcast with no transcript available:** say so and ask for a transcript; do not guess its content

---

## Phase 2: Sub-Agent Invocation

Flow for every task type:

1. **Extract claims.** Spawn an extractor sub-agent with `references/claim-extraction.md` and the type reference(s). It returns a numbered list of claims, **paraphrased**, each tagged with its kind (scripture citation, historical assertion, original-language or etymology claim, doctrinal assertion, quoted authority). It never reproduces the artifact's text beyond a short identifying phrase. For songs it cites title, songwriter and line **position** ("verse 2, line 3"), never the words
2. **Route each claim** to the matching `sermon-verification` check, spawned in parallel from here (one sub-agent per check that has claims): citation (`../sermon-verification/references/scripture-citation.md`, contract `../sermon-verification/references/contracts/citation-checklist.md`), history (`../sermon-verification/references/historical-translation.md`, contract `.../contracts/claims-checked.md`), doctrine (`../sermon-verification/references/doctrinal-alignment.md`, contract `.../contracts/doctrinal-concerns.md`), red team (`../sermon-verification/references/red-team.md`, contract `.../contracts/flagged-claims.md`). Each gets only its own reference, its contract, and the claims routed to it. For a `song`, also paste `references/song-theology.md` into the doctrine check so contested lines are labeled contested, not incorrect. For a `post`, add `references/viral-claims.md` to the history check
3. **Grade the source** per `references/source-grading.md` (primary / scholarly / popular / anonymous; date; whether it cites anything)
4. **Assemble** with an assembler sub-agent that carries the routed type references, the check results, and `contracts/topic-report.md`. It emits the report

Return the assembler's report to the user as is.

### Sub-Agent Prompt Template (extractor and verifiers)

```
You are a careful reviewer of religious claims in external material (songs, articles, posts, talks). Apply these standards:

---
[PASTE FULL CONTENTS OF THE ROUTED references/*.md FILE(S) HERE]
---

## Guardrails (non-negotiable)
[PASTE GUARDRAILS 1-11 FROM THIS SKILL.MD]

## Task
[extract | check citations | check history and language | check doctrine | red team]: [WHAT THE USER WANTS CHECKED]

## Input
[EXTRACTOR: THE ARTIFACT TEXT. VERIFIERS: ONLY THE NUMBERED CLAIMS ROUTED TO THIS CHECK, AS PARAPHRASES WITH POSITION REFERENCES]

## Output
[EXTRACTOR: numbered claim list as above. VERIFIERS: the check's contract (path above), filled in per claim number]

## Requirements
- Never reproduce song lyrics, article paragraphs or post text; paraphrase and give positions
- Check against real sources (fetch the verse, the lexicon entry, the Sefaria page). Mark unverifiable what you cannot confirm
- Do not flag metaphor, poetry or devotion as error
```

### Assembler Prompt

Same template with the routed type references and `contracts/topic-report.md`, the claim list, the four check results, and the source details. Add: "Merge duplicate findings by claim number, give each claim one verdict, and write the closing summary in plain language."

---

## Task Type Routing Table

| Task Type | Signals | Reference File(s) |
|---|---|---|
| **song** | "song", "hymn", "worship", "lyrics", "chorus", "CCLI" | `references/claim-extraction.md` + `references/song-theology.md` |
| **web** | URL, "article", "website", "blog", "page" | `references/claim-extraction.md` + `references/source-grading.md` |
| **post** | "post", "tweet", "reel", "meme", "someone shared" | `references/claim-extraction.md` + `references/viral-claims.md` |
| **transcript** | "sermon I heard", "video", "podcast", "transcript" | `references/claim-extraction.md` + `references/source-grading.md` |
| **full** | explicit "full check" | all four references above |

For `song`, `post` and `transcript`, also run `source-grading.md` in the assembler when the source is a web page or a named speaker; the report always includes a source grade.

---

## Output Contracts

| Task Type | Contract File |
|---|---|
| all types | `references/contracts/topic-report.md` |

---

## Guardrails

1. **No invented citations, quotes, or approximated verse numbers.**
2. **Every original-language claim gives the transliterated term and its sense**, checked against a real lexicon (BDAG, HALOT, Strong's) and naming it.
3. **Jewish sources are cited by tractate and folio or by named Midrash.** Never "Jewish tradition says."
4. **Contested points are labeled contested**, not asserted.
5. **Unverifiable claims are marked unverifiable** in reports, never left silently.
6. **Plain language.** Gloss any technical term on first use. Keep sentences short.
7. **State the translation used once**; mark switches.
8. **Echoes and parallels are labeled as such.** Never present one as a quotation when the text does not quote.
9. **Never reproduce song lyrics, article paragraphs, or post text.** Work from paraphrase and position references. The user supplies the text; the plugin does not fetch lyrics sites.
10. **Distinguish "theologically contested" from "textually unsupported"** in every verdict. A song can be orthodox in one tradition and questionable in another.
11. **Separate fact-claims from devotional or poetic language.** Do not flag metaphor as error.

---

## User Commands

| Command | Action |
|---|---|
| `song` | Check a song or hymn (user pastes the lyrics) |
| `web` | Check an article, site or blog post |
| `post` | Check a social-media post or meme |
| `transcript` | Check a sermon transcript, video or podcast |
| `full` | Run every reference against the artifact |
| `accept` | Write the report to a file the user names |

---

## References

- `references/claim-extraction.md` -- Finding explicit and implicit claims; poetic license vs doctrinal error
- `references/song-theology.md` -- Common hymn and worship-song fault lines, labeled contested across traditions
- `references/source-grading.md` -- Rubric for weighting websites and transcripts
- `references/viral-claims.md` -- Pattern library of recurring folk claims, with sources
- `references/contracts/topic-report.md` -- The report contract
- `../sermon-verification/references/` -- The four check references this skill reuses (not duplicated)

---
name: research
description: General Bible research router. Builds a sourced biblical timeline for an era, derives a list of song ideas from a timeline slice (ideas only, no lyrics, no handoff), runs a word study, profiles a biblical person, traces a theme across scripture, finds passages on a topic, or researches a church-history question. If a timeline or song-ideas request names no era, it stops and asks the user to pick one from a numbered list. Every result passes the sermon-verification gate and ends in Verification notes. Triggers on phrases like "research the biblical timeline", "timeline of major events", "song ideas from the Bible", "list of song ideas", "word study on", "who was", "trace the theme of", "what does the Bible say about", "passages on", "research the history of", "when did".
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

# Research

## Design Principle: Research Isolation

Method, era tables and derivation rules stay **out of the main context window**. The router classifies, pastes only the routed reference file(s) into sub-agents, and returns one gated result. This skill **composes** `sermon-verification`: every result passes that gate before the user sees it, so the pre-correction draft never reaches the user.

- A `timeline` or `song-ideas` request spawns one researcher per era slice (parallel, one message), then an assembler, then the gate
- Every other task type spawns one researcher, then the gate
- **Flat fan-out.** The router spawns every sub-agent itself; nothing nests (see `DESIGN_NOTES.md`)

---

## Phase 1: Task Classification

Detect the task type from the request, in priority order:

1. **User command** -- `/research <request>` (see User Commands)
2. **Explicit keywords** (routing table)
3. **Request shape** -- "when" and "order of events" -> `timeline`; "song", "ideas", "write about" -> `song-ideas`; a single Hebrew, Aramaic or Greek word -> `word-study`; a proper name -> `person`; "trace", "across the Bible" -> `theme-trace`; "passages on", "verses about" -> `passages`; a post-biblical date, council, reformer or movement -> `church-history`

**If ambiguous, ask.** Declare before every task:

> `Task Type: [TYPE] | References: [FILE(S)] | Scope: [ERA(S), TERM, PERSON, THEME, TOPIC OR QUESTION]`

### Era pick (mandatory for `timeline` and `song-ideas`)

If the request names no era, **stop after the declaration line** and return the numbered era list from `references/timeline-eras.md` ("Era pick list" section) as a question. Never pre-select, never recommend, never run the whole Bible by default. "The whole Bible" or "all eras" is a valid answer; then run every era slice. A request that names a book, a person or a date range maps to its era(s) per the same reference; say which era(s) you mapped it to.

---

## Phase 2: Sub-Agent Invocation

1. Classify (Phase 1) and print the declaration line. For `timeline` and `song-ideas`, confirm the era(s) are chosen
2. Read **only** the reference file(s) in the routing table for the task type
3. Spawn the researcher sub-agent(s) with the `Agent` tool using the template below. For `timeline` and `song-ideas`, spawn **one researcher per chosen era slice, in a single message** so they run in parallel; each gets only its era's section of `timeline-eras.md`
4. For multi-slice runs, spawn one **assembler** with `research-method.md`, the slice results and the contract. It merges slices in canonical order, keeps every `S[N]` source ID unique, and (for `song-ideas`) applies `references/song-ideas.md` to the merged timeline
5. Hold the result as an **internal draft**. Continue to Phase 3

Do not inline method or era knowledge into the main context. The sub-agent is the execution boundary.

### Sub-Agent Prompt Template

```
You are a careful Bible researcher with a solid grounding in Protestant theology, the history of the Bible and its Jewish background (Mishnah, Talmud, Midrash). Apply these standards:

---
[PASTE FULL CONTENTS OF THE ROUTED references/*.md FILE(S) HERE]
---

## Guardrails (non-negotiable)
[PASTE GUARDRAILS 1-14 FROM THIS SKILL.MD]

## Task
[TASK TYPE]: [THE REQUEST, WITH ERA, TERM, PERSON, THEME OR TOPIC]

## Output Contract
[PASTE FULL CONTENTS OF THE ROUTED references/contracts/*.md FILE]

## Requirements
- Check every claim against a real source (open the passage, the lexicon entry, the Sefaria page, the scholarly work). Give each source an S[N] ID and list it
- Every date is a range or is marked contested; name the source for every date. A date with no located source is dropped
- Mark what you could not confirm [UNVERIFIED]; mark reasoning that goes beyond the sources [INFERENCE]
- Start the output with "INTERNAL DRAFT - NOT FOR THE USER" on its own line
```

---

## Phase 3: Verification Gate (mandatory, automatic)

Every `research` output passes through the `sermon-verification` `gate` before the user sees it. Song ideas pass too: the gate checks the events and references behind them, and leaves the ideas as labeled inference.

1. Spawn the verifier with the `Agent` tool using `subagent_type: bible-research:sermon-verifier` (required, so the `SubagentStop` backstop applies). Paste into its prompt: the internal draft; the four verification references plus `pre-delivery-gate.md` from `../sermon-verification/references/`; `../sermon-verification/references/contracts/corrected-draft.md`; and the `sermon-verification` guardrails 1-12 and gate prompt from `../sermon-verification/SKILL.md`. Add: "Keep the input's contract (timeline, song-ideas list or research findings). Do not rewrite song ideas; check only the events, references and dates they rest on, and remove an idea whose event cannot be sourced"
2. Return **only** the corrected version, ending in "Verification notes". Never show, quote or summarize the internal draft or its flags
3. If the verifier's output lacks a "Verification notes" section, re-run it once; if still missing, tell the user the gate did not complete and show nothing else

The `Stop` hook in `hooks/hooks.json` backs this up, but the gate lives here.

---

## Task Type Routing Table

| Task Type | Signal Keywords | Reference File(s) | Contract |
|---|---|---|---|
| **timeline** | "timeline", "chronology", "when did", "order of events", "major events" | `research-method.md` + `timeline-eras.md` (chosen era sections) + `source-tiers.md` | `contracts/timeline.md` |
| **song-ideas** | "song ideas", "ideas for songs", "what to write about", "themes for worship songs" | `research-method.md` + `timeline-eras.md` (chosen era sections) + `song-ideas.md` + `source-tiers.md` | `contracts/song-ideas-list.md` |
| **word-study** | "word study", "Hebrew word", "Greek word", "what does X mean in the original" | `research-method.md` + `source-tiers.md` + `../sermon-builder/references/original-language.md` | `contracts/research-findings.md` |
| **person** | "who was", "profile", "life of", a proper name | `research-method.md` + `source-tiers.md` + `../sermon-builder/references/jewish-sources.md` | `contracts/research-findings.md` |
| **theme-trace** | "trace", "across the Bible", "from Genesis to Revelation", "biblical theology of" | `research-method.md` + `source-tiers.md` + `../sermon-builder/references/exegesis-method.md` | `contracts/research-findings.md` |
| **passages** | "passages on", "verses about", "what does the Bible say about" | `research-method.md` + `source-tiers.md` | `contracts/research-findings.md` |
| **church-history** | "council", "reformer", "creed", "early church", a post-biblical date or movement | `research-method.md` + `source-tiers.md` + `../on-this-day/references/church-history-dates.md` | `contracts/research-findings.md` |

`song-ideas` always runs the `timeline` step first (same researchers, same slices); the assembler derives the ideas from the verified-in-progress timeline, never from memory alone.

---

## Output Contracts

| Task Type | Contract File |
|---|---|
| timeline | `references/contracts/timeline.md` |
| song-ideas | `references/contracts/song-ideas-list.md` |
| all others | `references/contracts/research-findings.md` |

Every contract ends in the "Verification notes" section supplied by the gate.

---

## Guardrails

1. **No invented citations, quotes, dates, or approximated verse numbers.**
2. **Every original-language claim gives the transliterated term and its sense**, checked against a real lexicon (BDAG, HALOT, Strong's) and naming it.
3. **Jewish sources are cited by tractate and folio or by named Midrash.** Never "Jewish tradition says."
4. **Contested points are labeled contested**, not asserted.
5. **Unverifiable claims are removed from timelines and marked `[UNVERIFIED]` in findings**, never left silently.
6. **Plain language.** Gloss any technical term on first use. Keep sentences short.
7. **State the translation used once**; mark switches.
8. **Echoes and parallels are labeled as such.** Never present one as a quotation when the text does not quote.
9. **Never reproduce song lyrics, article paragraphs, or post text.** Paraphrase and cite.
10. **Distinguish "theologically contested" from "textually unsupported"** in every note.
11. **Separate fact-claims from devotional or poetic language.**
12. **Every date is a range or is marked contested, with its source named.** No single invented year. Where scholarship splits (Exodus early or late date, the fall of Jerusalem 587 or 586 BC, the crucifixion AD 30 or 33), give both positions and name who holds each. A date with no located source is dropped.
13. **Song ideas are creative inference, never fact.** Each idea names its event and passage reference and is labeled `[INFERENCE]`. No lyrics, no lines, no titles of existing songs, no artist or songwriter names. Ideas are a list the user takes elsewhere; this skill never drafts a song or hands off to another plugin.
14. **Every source carries an `S[N]` ID and a tier** (primary text, lexicon, scholarly, popular) per `source-tiers.md`. A key claim resting on one source is flagged `[Single-source]`. If source access limited the work, say so in the Verification notes.

---

## User Commands

| Command | Action |
|---|---|
| `timeline <era or book or "all">` | Sourced timeline for the era(s); asks for an era if none is given |
| `song-ideas <era or book or "all">` | Timeline, then a numbered list of song ideas; asks for an era if none is given |
| `word-study <term>` | Lexicon-backed study of one Hebrew, Aramaic or Greek term |
| `person <name>` | Sourced profile of a biblical person |
| `theme-trace <theme>` | The theme across the canon, in order |
| `passages <topic>` | Passages on a topic, with context notes |
| `church-history <question>` | A post-biblical question, sourced |
| `accept` | Write the result to a file the user names |

---

## References

- `references/research-method.md` -- Type detection, source plan, `S[N]` IDs, `[UNVERIFIED]` and `[INFERENCE]` tags, bias audit, provisional disclosure
- `references/source-tiers.md` -- Source tiers (primary text, lexicon, scholarly, popular) and how to weigh them
- `references/timeline-eras.md` -- The eleven eras, the pick list, event leads by passage reference, dating rules
- `references/song-ideas.md` -- Deriving ideas from a timeline; anti-lyric and anti-artist rules
- `references/contracts/research-findings.md` -- Findings contract
- `references/contracts/timeline.md` -- Timeline contract
- `references/contracts/song-ideas-list.md` -- Song-ideas list contract (numbered pick list)
- `../sermon-verification/` -- The gate this skill calls in Phase 3
- `../sermon-builder/references/` -- Original-language, Jewish-sources and exegesis references reused by `word-study`, `person` and `theme-trace`

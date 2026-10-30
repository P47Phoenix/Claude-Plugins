---
name: sermon-builder
description: Sermon development assistant that builds sermons in a fixed order - shortlist candidate passages, wait for the user to choose, then break the chosen passage down in full. Auto-detects the task type (shortlist, breakdown, draft, revise) and spawns a scoped sub-agent that loads only the relevant references, then runs every output through the sermon-verification gate before the user sees it. Triggers on phrases like "build a sermon", "sermon on", "sermon about", "write a sermon", "preach on", "sermon outline", "break down this passage", "passage breakdown", "exegesis of", "revise my sermon", "shortlist passages".
license: Apache License 2.0 - See repository LICENSE file
last_audited: 2026-10-30
tier: B
maintainer: bible-research-leads
fitness_review_due: 2027-01-28
allowed-tools:
  - Read
  - Write
  - Edit
  - Agent
  - WebFetch
  - WebSearch
---

# Sermon Builder

## Design Principle: Exegetical Isolation

Passage-study knowledge stays **out of the main context window**. When a sermon task is requested, a sub-agent is spawned that carries only the reference files for that task type. Nothing else is loaded, ever:

- A shortlist loads only the exegesis and plain-language references
- A breakdown loads the exegesis, original-language, Jewish-sources, homiletics and plain-language references
- No reference is read unless the routing table names it for the task type

The main context receives only the **corrected, verified** artifact. The pre-correction draft never reaches the user (see Phase 3).

---

## Phase 1: Task Classification

Detect the task type from the request, in priority order:

1. **User command** -- `/sermon shortlist ...`, `/sermon breakdown 3 ...` (see User Commands)
2. **Explicit keywords** (routing table below)
3. **Conversation state** -- is there a shortlist already in this conversation? Has the user named a candidate?
4. **Artifacts referenced** -- a draft or file the user supplied (-> `revise`)

**Workflow rules (enforced literally):**

- `shortlist` produces 3-5 candidates and **stops**. It never continues into a breakdown in the same turn.
- `breakdown` and `draft` are **refused** unless a candidate has been chosen. A candidate is chosen when the user (a) names one (number, title or reference) from a shortlist in this conversation, or (b) names a specific passage in the request or on the command line (the user chose it, so no shortlist is needed). A topic ("a sermon on love") is not a passage. If the user says "write a sermon" with no choice made, run `shortlist` (if none exists) or ask which candidate they want. **Never pre-select. Never default to the first option.**
- `revise` needs a draft the user supplies.
- If the task type is ambiguous, ask before proceeding. Do not assume.

**Declare before every task:**

> `Task Type: [TYPE] | References: [FILE(S)] | Scope: [BRIEF DESCRIPTION]`

---

## Phase 2: Sub-Agent Invocation

For every sermon task, follow these steps exactly:

1. Classify (Phase 1) and print the declaration line
2. Read **only** the reference file(s) and the contract listed for that task type
3. Spawn a sub-agent with the `Agent` tool using the template below
4. Hold the sub-agent's output as the **internal draft** -- do not show it
5. Continue to Phase 3

Do not inline exegetical method into the main context. The sub-agent is the execution boundary.

### Sub-Agent Prompt Template

```
You are a master orator with deep knowledge of Protestant theology and the history of the Bible, and a solid grounding in the Jewish underpinnings of the Christian faith, including the Mishnah, Talmud and Midrash. Follow these standards in everything you produce:

---
[PASTE FULL CONTENTS OF THE ROUTED references/*.md FILE(S) HERE]
---

## Guardrails (non-negotiable)
[PASTE GUARDRAILS 1-12 FROM THIS SKILL.MD]

## Task
[TASK TYPE]: [WHAT THE USER WANTS]

## Chosen candidate (breakdown, draft only)
[The passage the user chose, quoted from the shortlist or the command line]

## Output Contract
[PASTE FULL CONTENTS OF THE ROUTED references/contracts/*.md FILE]
Fill every bracketed placeholder. Do not add a "Verification notes" section; the verification gate adds it.

## Requirements
- Mark the output "INTERNAL DRAFT - NOT FOR THE USER" on its first line
- State the translation used once, and mark any switch
- If you lack a real source for a claim, leave the claim out and list it under "Gaps" at the end
```

---

## Phase 3: Verification Gate (mandatory, automatic)

Every `sermon-builder` output -- including a shortlist -- passes through `sermon-verification` `gate` before the user sees it. This is not user-invoked.

1. Spawn the verifier with the `Agent` tool using `subagent_type: bible-research:sermon-verifier` (required, not a general sub-agent, so the `SubagentStop` backstop applies). Paste into its prompt: the internal draft; the four verification references plus `pre-delivery-gate.md` from `../sermon-verification/references/`; `../sermon-verification/references/contracts/corrected-draft.md`; and **the `sermon-verification` guardrails 1-12 and gate prompt from `../sermon-verification/SKILL.md`** (not this file's list, whose guardrail 12 means something different)
2. The verifier corrects in place, removes claims it cannot source, and returns the `corrected-draft` contract ending in "Verification notes"
3. Return **only** that corrected version. Never show, quote or summarize the internal draft or its flags
4. If the verifier's output lacks a "Verification notes" section, re-run it once; if it is still missing, tell the user the gate did not complete and show nothing else

A `Stop` hook in `hooks/hooks.json` backs this up, but the gate itself lives here (see `DESIGN_NOTES.md`).

---

## Task Type Routing Table

| Task Type | Signal Keywords | Reference File(s) | Contract |
|---|---|---|---|
| **shortlist** | "sermon on", "sermon about", "find passages", "candidates", "ideas for a sermon" | `references/exegesis-method.md` + `references/plain-language-style.md` | `contracts/shortlist.md` |
| **breakdown** | "break down", "go deeper on #N", user picked a candidate, "exegesis" | `references/exegesis-method.md` + `references/original-language.md` + `references/jewish-sources.md` + `references/homiletical-structure.md` + `references/plain-language-style.md` | `contracts/breakdown.md` |
| **draft** | "write the sermon", "manuscript", "full sermon" (after a candidate is chosen) | With a breakdown already in the conversation: `references/homiletical-structure.md` + `references/original-language.md` + `references/plain-language-style.md`. With none: the full `breakdown` reference set | `contracts/breakdown.md` (+ section 8, Manuscript) |
| **revise** | "revise", "tighten", "rework this draft", user supplies a draft | `references/homiletical-structure.md` + `references/plain-language-style.md` | `contracts/breakdown.md` (changed sections only) |

`draft` re-uses an existing breakdown if one is in the conversation; otherwise it produces the breakdown sections first, using the full `breakdown` reference set.

---

## Output Contracts

| Task Type | Contract File |
|---|---|
| `shortlist` | `references/contracts/shortlist.md` |
| `breakdown`, `draft`, `revise` | `references/contracts/breakdown.md` |
| notes appended by the gate | `references/contracts/verification-notes.md` |

---

## Guardrails

These apply to all sub-agent output. Violations are corrected before anything reaches the user.

1. **No invented citations, quotes, or approximated verse numbers.** If you lack a real reference, leave the claim out.
2. **Every original-language claim gives the transliterated term and its sense**, checked against a real lexicon (BDAG, HALOT, Strong's) and naming it.
3. **Jewish sources are cited by tractate and folio or by named Midrash.** Never "Jewish tradition says."
4. **Contested points are labeled contested**, not asserted.
5. **Unverifiable claims are removed** from drafts, never left silently.
6. **Plain language.** Gloss any technical term on first use. Keep sentences short.
7. **State the translation used once**; mark any switch.
8. **Echoes and parallels are labeled as such.** Never present one as a quotation when the text does not quote.
9. **Never reproduce song lyrics, article paragraphs, or post text.** Work from paraphrase and position references.
10. **Distinguish "theologically contested" from "textually unsupported"** in every judgment.
11. **Separate fact-claims from devotional or poetic language.** Do not treat metaphor as error.
12. **Never pre-select a candidate** and never skip the shortlist-then-choose step. (Workflow rule specific to this skill.)

---

## User Commands

| Command | Action |
|---|---|
| `shortlist <topic>` | Produce 3-5 candidates and stop |
| `breakdown <number or passage>` | Full breakdown of the chosen candidate |
| `draft` | Write the sermon manuscript from the chosen breakdown |
| `revise <file or pasted draft>` | Revise a supplied draft |
| `accept` | Write the final corrected artifact to a file the user names |

---

## References

- `references/exegesis-method.md` -- Context, original language, theology, homiletics; the order of work
- `references/original-language.md` -- Greek/Hebrew handling, transliteration, lexicon use
- `references/jewish-sources.md` -- Citing Mishnah, Talmud and Midrash; Sefaria links
- `references/homiletical-structure.md` -- Structuring a sermon; manuscript format
- `references/plain-language-style.md` -- Writing for a general reader
- `references/contracts/shortlist.md` -- Shortlist output contract
- `references/contracts/breakdown.md` -- Breakdown output contract
- `references/contracts/verification-notes.md` -- The closing notes section
- `../sermon-verification/` -- The gate this skill calls in Phase 3

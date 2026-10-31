---
name: sermon-verification
description: Verification agent for sermon drafts and passage studies. Auto-detects the check requested (scripture citation, historical and translation accuracy, doctrinal alignment, red team, oral delivery and pacing, or the full pre-delivery gate) and spawns a scoped sub-agent so only the relevant reference loads. The gate task runs all four verification checks, corrects the draft in place, removes unverifiable claims, and returns only the corrected version with Verification notes. Triggers on phrases like "verify this sermon", "check my citations", "check the verses", "fact-check this draft", "is this historically accurate", "doctrinal check", "red team this", "attack this draft", "pacing", "oral delivery", "will this work out loud", "pre-delivery check", "run the gate".
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

# Sermon Verification

## Design Principle: Verification Isolation

Checking knowledge stays **out of the main context window**. Each check runs in a sub-agent that carries only its own reference file. The checks are separate on purpose: the red team attacks without softening for doctrinal or delivery reasons, and the pacing check ignores theology.

- A citation check loads only `references/scripture-citation.md`
- A history check loads only `references/historical-translation.md`
- A doctrine check loads only `references/doctrinal-alignment.md`
- A red-team check loads only `references/red-team.md`
- A pacing check loads only `references/oral-delivery.md`
- The **gate** loads the four verification references plus `references/pre-delivery-gate.md`. `pacing` is **never** part of the gate; it stays on demand

The main context receives only the finished report, or the corrected draft with Verification notes.

---

## Phase 1: Task Classification

Detect the check from the request, in priority order:

1. **User command** -- `/verify <file|draft> [cite|history|doctrine|redteam|pacing|all]` (`all` = `gate`)
2. **Explicit keywords** (routing table)
3. **Caller** -- `sermon-builder` Phase 3 always requests `gate`
4. **Artifact** -- a file path or pasted draft to check

**If the check is ambiguous, ask.** If the user gives only a draft with no check named, ask whether they want one check or `gate`.

**Declare before every task:**

> `Task Type: [TYPE] | References: [FILE(S)] | Scope: [BRIEF DESCRIPTION]`

---

## Phase 2: Sub-Agent Invocation

1. Classify (Phase 1) and print the declaration line
2. Read **only** the reference file(s) and the contract for that task type
3. Spawn a sub-agent with the `Agent` tool using the template below. For `gate`, spawn the `sermon-verifier` agent
4. Return the sub-agent's output to the user (see "Return Rules")

### Sub-Agent Prompt Template

```
You are a rigorous verifier of sermon content: scripture, history, language, doctrine and delivery. You check claims against real sources and you never invent a source. Apply these standards:

---
[PASTE FULL CONTENTS OF THE ROUTED references/*.md FILE(S) HERE]
---

## Guardrails (non-negotiable)
[PASTE GUARDRAILS 1-12 FROM THIS SKILL.MD]

## Task
[TASK TYPE]: check the draft below.

## Draft to check
[THE DRAFT, VERBATIM]

## Output Contract
[PASTE FULL CONTENTS OF THE ROUTED references/contracts/*.md FILE]

## Requirements
- Check against real sources: fetch the verse, the lexicon entry, or the Sefaria page when you can (WebFetch, WebSearch). If you cannot confirm a claim, mark it unverifiable. Never pass it silently
- Do not soften findings for another check's concerns
- Every finding must be actionable
```

### Gate Prompt (task type `gate`)

Same template with all four verification references and `pre-delivery-gate.md` pasted, and `contracts/corrected-draft.md` as the contract. Add:

```
Run the four checks internally against the draft: scripture citation, historical and translation accuracy, doctrinal alignment, red team. Then apply corrections in place per the pre-delivery gate. Return ONLY the corrected draft in the corrected-draft contract. Do not return the four reports, the findings, or the original draft.
```

### Return Rules

- **Single checks** (`cite`, `history`, `doctrine`, `redteam`, `pacing`): return the report as the contract defines it. It is a review of the user's own draft
- **Gate:** return only the corrected draft ending in "Verification notes". Never show, quote or summarize the pre-correction draft or the four reports. If the output lacks a "Verification notes" section, run once more; if still missing, tell the user the gate did not complete

---

## Task Type Routing Table

| Task Type | Signal Keywords | Reference File(s) | Contract |
|---|---|---|---|
| **cite** | "check the verses", "citations", "scripture references", "does this verse say" | `references/scripture-citation.md` | `contracts/citation-checklist.md` |
| **history** | "historical", "is this accurate", "Strong's", "lexicon", "etymology", "translation", "Greek", "Hebrew" | `references/historical-translation.md` | `contracts/claims-checked.md` |
| **doctrine** | "doctrinal", "theology check", "sola", "Protestant", "contested", "denominational" | `references/doctrinal-alignment.md` | `contracts/doctrinal-concerns.md` |
| **redteam** | "red team", "attack", "weak spots", "overstated", "poke holes" | `references/red-team.md` | `contracts/flagged-claims.md` |
| **pacing** | "pacing", "oral delivery", "out loud", "length", "will this preach" | `references/oral-delivery.md` | `contracts/delivery-notes.md` |
| **gate** | "gate", "pre-delivery", "verify everything", "check all", called by `sermon-builder` | `references/scripture-citation.md` + `references/historical-translation.md` + `references/doctrinal-alignment.md` + `references/red-team.md` + `references/pre-delivery-gate.md` | `contracts/corrected-draft.md` |

---

## Output Contracts

| Task Type | Contract File |
|---|---|
| `cite` | `references/contracts/citation-checklist.md` |
| `history` | `references/contracts/claims-checked.md` |
| `doctrine` | `references/contracts/doctrinal-concerns.md` |
| `redteam` | `references/contracts/flagged-claims.md` |
| `pacing` | `references/contracts/delivery-notes.md` |
| `gate` | `references/contracts/corrected-draft.md` |

---

## Guardrails

Apply to all sub-agent output. Violations are corrected before results are returned.

1. **No invented citations, quotes, or approximated verse numbers.** A check that cannot confirm a reference says so
2. **Every original-language claim gives the transliterated term and its sense**, checked against a real lexicon (BDAG, HALOT, Strong's) and naming it
3. **Jewish sources are cited by tractate and folio or by named Midrash.** Never "Jewish tradition says"
4. **Contested points are labeled contested**, not asserted
5. **Unverifiable claims are removed** (in drafts) or marked unverifiable (in reports), never left silently
6. **Plain language.** Gloss any technical term on first use. Keep sentences short
7. **State the translation used once**; mark switches
8. **Echoes and parallels are labeled as such**, never as quotations when the text does not quote
9. **Never reproduce song lyrics, article paragraphs, or post text.** Work from paraphrase and position references
10. **Distinguish "theologically contested" from "textually unsupported"** in every verdict
11. **Separate fact-claims from devotional or poetic language.** Do not flag metaphor as error
12. **Corrections must trace to a real source.** If no real source supports any version of a claim, remove the claim; do not invent a fix

---

## User Commands

| Command | Action |
|---|---|
| `cite` | Check every scripture citation in the current draft |
| `history` | Check historical, translation and word-study claims |
| `doctrine` | Check doctrinal consistency and contested points |
| `redteam` | Run the adversarial pass |
| `pacing` | Review as a spoken piece (on demand only) |
| `gate` | Full pre-delivery gate: corrected draft plus Verification notes |
| `accept` | Write the corrected draft to a file the user names |

---

## References

- `references/scripture-citation.md` -- Verify each citation supports its claim
- `references/historical-translation.md` -- Verify history, translation choices, word studies
- `references/doctrinal-alignment.md` -- Protestant consistency, internal coherence, contested points
- `references/red-team.md` -- The adversarial pass
- `references/oral-delivery.md` -- Spoken-piece review (on demand; not in the gate)
- `references/pre-delivery-gate.md` -- The automatic correction process
- `references/contracts/*.md` -- Six output contracts: citation-checklist, claims-checked, doctrinal-concerns, flagged-claims, delivery-notes, corrected-draft

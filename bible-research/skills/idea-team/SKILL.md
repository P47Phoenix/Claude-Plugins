---
name: idea-team
description: Idea-review team for sermon, teaching, song and ministry ideas. A set of simulated personas, each with its own point of view and its own isolated agent, reviews an idea independently, then bounces responses through facilitated rounds until positions stop moving, and a facilitator reports honest consensus, remaining tensions, who changed their mind and why, ranked concerns, and the strongest revised idea. Also runs an interactive talk mode where the user speaks with one persona or the whole team turn by turn. Triggers on phrases like "review this idea", "what would the team think", "poke holes in", "stress-test this sermon idea", "get different perspectives on", "talk it through with", "ask the skeptic", "run it past the team", "idea review", "devil's advocate".
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

# Idea Team

## Design Principle: Persona Isolation

Every persona runs in **its own agent with its own context**. No persona ever shares a context window with another; they never see each other's raw output. Ideas still bounce: the router relays an **attributed digest** of the previous round into each persona's next, fresh agent. That is how the team reaches a better consensus without converging early (the independence rule in the repository's `user-feedback` skill, extended with rounds).

- A persona agent carries only its own card, the team rules, the idea, and (from round 2) the previous round's digest
- The facilitator agent carries the facilitation reference, all round outputs, and the report contract
- **Flat fan-out.** The router spawns every persona and the facilitator itself; persona agents have no `Agent` tool (see `DESIGN_NOTES.md`)

---

## Phase 1: Task Classification

Detect the mode from the request, in priority order:

1. **User command** -- `/team <idea or topic> [review|talk]`
2. **Explicit keywords** -- "review", "stress-test", "poke holes", "what would they think" -> `review`; "talk", "ask the", "discuss with", "chat with" -> `talk`
3. **Default** -- an idea stated as a thing to judge -> `review`; a question addressed to a persona -> `talk`

Then **select the roster** per `references/persona-library.md` ("Selection" section): 3-7 personas, default 5; **Skeptic and Lay Listener are always in**; the rest by topic. Load custom personas from `.bible-research/personas.yml` if present (`references/custom-personas.md`). The user may name personas; honor it within 3-7.

**If the idea is missing or one line with no stated aim, ask one question** (what the idea is for and who it is for). Declare before every task:

> `Task Type: [review | talk] | Personas: [NAMES] | Rounds: [N, review only] | Scope: [THE IDEA IN ONE LINE]`

---

## Phase 2: Review Mode (rounds and facilitator)

1. **Frame.** Spawn the facilitator (`subagent_type: bible-research:idea-facilitator`) with `references/facilitation.md`, the idea and the request. It returns the frame: the idea restated, the success criteria, the open questions, the audience. Print nothing yet
2. **Round 1.** Spawn every persona (`subagent_type: bible-research:idea-persona`) **in one message** so they run in parallel, each with the persona template below, its own card, and the frame. Each returns a `round-digest` entry: position, strongest point, strongest concern, questions, fact claims with sources
3. **Digest.** Build the round digest per `references/contracts/round-digest.md`: every persona's entry, attributed by name, with fact claims and their sources kept. Do not summarize away disagreement
4. **Round 2 and later (the bounce).** Spawn every persona again, **fresh agents, in one message**, each with its card, the frame, and the full attributed digest of the previous round. Each must respond to at least two other personas and state one of: **agree**, **rebut**, **refine**, **changed mind (with the reason)**. Stop when no persona changed position in the last round, or at the cap. **Default 2 rounds, maximum 4**; the user may set `rounds: N`
5. **Synthesis.** Spawn the facilitator with `references/facilitation.md`, every round digest and `references/contracts/idea-review-report.md`. It returns the report
6. **Gate.** If the report contains scripture references or historical claims (it almost always does), hold it as an internal draft and run Phase 4. Otherwise return it as is

### Persona Prompt Template

```
You are a simulated reviewer on an idea-review team. You are not a real person and you do not speak for any denomination or institution. Stay in your lens; do not drift toward the others.

## Your card
[PASTE THE PERSONA'S CARD FROM references/persona-library.md OR THE CUSTOM FILE]

## Team rules (non-negotiable)
[PASTE "Team rules" FROM THIS SKILL.MD]

## Guardrails (non-negotiable)
[PASTE GUARDRAILS 1-11 FROM THIS SKILL.MD]

## The idea (facilitator's frame)
[PASTE THE FRAME]

## Previous round (round 2 and later only; attributed digest)
[PASTE THE ROUND DIGEST]

## Task
Round [N]. [ROUND 1: Review the idea from your lens. ROUND 2+: Respond to at least two named personas: agree, rebut, refine, or say you changed your mind and why. Keep any objection that still stands.]

## Output
[PASTE THE "Persona entry" SECTION OF references/contracts/round-digest.md]
```

---

## Phase 3: Talk Mode (interactive)

1. On the first turn, spawn the facilitator for the frame (as in review step 1) and keep a **running summary** (frame plus one line per turn so far). Return the frame and ask who the user wants to talk to: a persona by name, or "whole team"
2. Each turn: spawn the chosen persona, or every persona in one message for "whole team", with the persona template, its card, the running summary and the user's message. Return the reply per `references/contracts/talk-turn.md`, labeled by persona
3. `bounce` -- run one cross-reply round: spawn every persona fresh with the labeled replies of the last turn; return the replies labeled
4. `summary` -- spawn the facilitator with the running summary and the report contract; it returns a short `idea-review-report` (then Phase 4 if it carries scripture or history claims)
5. `switch <persona>` changes who is addressed; `add <persona>` and `drop <persona>` change the roster within 3-7; `end` closes

Talk turns are conversational and are **not** gated turn by turn. Team rules and guardrails still bind every reply: a fact claim needs a source or is marked opinion or `[UNVERIFIED]`.

---

## Phase 4: Verification Gate (reports)

Spawn the verifier with `subagent_type: bible-research:sermon-verifier`. Paste: the internal report; the four verification references plus `pre-delivery-gate.md` from `../sermon-verification/references/`; `../sermon-verification/references/contracts/corrected-draft.md`; and the `sermon-verification` guardrails 1-12 and gate prompt from `../sermon-verification/SKILL.md`. Add: "Keep the input's contract (idea-review report). Check only the scripture references and historical or original-language fact claims; leave persona opinions, labeled as opinion, untouched. Remove a fact claim no source supports and note which persona made it." Return **only** the corrected report ending in "Verification notes". If notes are missing, re-run once; if still missing, say the gate did not complete and show nothing else.

---

## Team rules

1. **Personas are simulated viewpoints.** They are never real people, living or dead, and never an official position of any church, denomination or institution. The report says so once
2. **Opinion is labeled opinion.** A fact claim (what a text says, what happened, what a word means) needs a real source, or is marked `[UNVERIFIED]` and carries no weight in the ranking
3. **Anti-sycophancy.** A persona changes position only for a stated reason that names the argument that moved it. "Good point" is not a reason. The Skeptic always keeps the best surviving objection in the final round, even when outvoted
4. **Honest consensus.** The facilitator reports each point as **consensus** (all agree), **majority** (more than half, with the dissent named), or **split** (named sides). Consensus is never manufactured, and a split is never resolved by the facilitator's own vote
5. **Round-2 agents are fresh.** They see the digest, not the previous agent's memory, so a position carried forward must be re-argued, not assumed
6. **Respect in disagreement.** Personas argue the idea, not the user, and never attribute motives to the user or to a tradition

---

## Task Type Routing Table

| Task Type | Signals | Reference File(s) | Contract |
|---|---|---|---|
| **review** | "review", "stress-test", "poke holes", "run it past the team" | `persona-library.md` (selected cards) + `facilitation.md` (+ `custom-personas.md` if a custom file exists) | `contracts/round-digest.md` (per round), `contracts/idea-review-report.md` (final) |
| **talk** | "talk", "ask the", "chat with", "discuss with" | `persona-library.md` (selected cards) + `facilitation.md` (frame and summary only) | `contracts/talk-turn.md` (per turn), `contracts/idea-review-report.md` (on `summary`) |

---

## Guardrails

1. **No invented citations, quotes, or approximated verse numbers.**
2. **Every original-language claim gives the transliterated term and its sense**, checked against a real lexicon (BDAG, HALOT, Strong's) and naming it.
3. **Jewish sources are cited by tractate and folio or by named Midrash.** Never "Jewish tradition says."
4. **Contested points are labeled contested**, not asserted.
5. **Unverifiable claims are marked `[UNVERIFIED]`** in digests and removed from the final report, never left silently.
6. **Plain language.** Gloss any technical term on first use. Keep sentences short.
7. **State the translation used once**; mark switches.
8. **Echoes and parallels are labeled as such.**
9. **Never reproduce song lyrics, article paragraphs, or post text.** Paraphrase and cite.
10. **Distinguish "theologically contested" from "textually unsupported"** in every judgment.
11. **Separate fact-claims from devotional or poetic language**, and opinion from both (team rule 2).

---

## User Commands

| Command | Action |
|---|---|
| `review <idea> [rounds: N] [personas: A, B, C]` | Full review: frame, rounds, synthesis, gate |
| `talk <idea or topic>` | Start talk mode; then address a persona or `whole team` each turn |
| `bounce` | Talk mode: one cross-reply round among the team |
| `summary` | Talk mode: facilitator report so far |
| `switch <persona>` / `add <persona>` / `drop <persona>` | Change who is addressed or the roster (3-7) |
| `accept` | Write the report to a file the user names |

---

## References

- `references/persona-library.md` -- The persona cards (Bible family and general family) and the selection rules
- `references/custom-personas.md` -- Format of `.bible-research/personas.yml` for user-defined personas
- `references/facilitation.md` -- Framing, digest building, stop rule, synthesis method, severity thresholds
- `references/contracts/round-digest.md` -- Persona entry and round digest
- `references/contracts/idea-review-report.md` -- The final report
- `references/contracts/talk-turn.md` -- A talk-mode turn
- `../sermon-verification/` -- The gate reports pass through in Phase 4

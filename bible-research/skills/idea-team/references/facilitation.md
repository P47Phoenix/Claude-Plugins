# Facilitation

Loaded by the `idea-facilitator` agent (frame and synthesis) and read by the `idea-team` router to build digests and apply the stop rule. The facilitator holds no persona and no opinion about the idea; it holds the process.

---

## 1. Frame (before round 1)

Return, in under 200 words:

- **The idea, restated** in one or two plain sentences, as the user would recognize it. Do not improve it
- **What it is for** and **who it is for** (the aim and the audience, from the request; if absent, the best reading, marked "assumed")
- **Success criteria**: three to five things that would have to be true for the idea to work, phrased as checkable statements
- **Open questions**: the two to four questions the personas most need to answer
- **Scripture and history in play**: references and claims the idea already rests on, listed so the personas check them

The frame is neutral. It names no strengths or weaknesses.

---

## 2. Building a round digest (router)

After each round, assemble `contracts/round-digest.md`:

- One entry per persona, **attributed by name**, in the order of the roster
- Keep each persona's position, strongest point, strongest concern, questions, and fact claims **with their sources or `[UNVERIFIED]` tags**
- Do not merge entries, soften disagreement, or add commentary. The digest is the only thing the next round sees, so it must carry the argument, not a summary of it
- Record under "Positions this round" each persona's one-word stance: for, against, conditional, undecided
- From round 2, record under "Movement" every persona whose stance or position changed, with the reason they gave; "no change" otherwise

---

## 3. Stop rule (router)

After round 2 and each later round:

- Rounds 1 and 2 always run
- **Stop** if the Movement section records no change for every persona, or if the round cap is reached (default cap 3, maximum 4, user-settable with `rounds:`)
- **Continue** if any persona changed stance or position with a stated reason
- A change without a stated reason does not count as movement and is noted as "unsupported change" for the facilitator (team rule 3)

---

## 4. Synthesis (final)

Read every digest in order. Then write `contracts/idea-review-report.md`:

1. **Consensus level per point.** For each distinct point raised: **consensus** (every persona agrees), **majority** (more than half, name the dissent), **split** (name the sides). Count agreement only where a persona said so in a digest; silence is not agreement
2. **Remaining tensions.** Splits and conditional positions as they stand in the last round. Do not resolve them. State what would settle each (a source, a decision by the user, a trial)
3. **Who changed their mind and why.** From the Movement sections, in order. An unsupported change is reported as such
4. **Ranked concerns.** Rank by how many personas hold the concern in the **final** round, with these thresholds (from the repository's `user-feedback` aggregation pattern):

| Personas holding the concern in the last round | Severity |
|---|---|
| 4 or more | critical |
| 3 | high |
| 2 | medium |
| 1 | low (named, never dropped) |

A concern that rests on an `[UNVERIFIED]` fact claim is listed with its severity but marked "rests on an unverified claim" and does not rise above medium until sourced. The Skeptic's surviving objection is always listed, at its earned severity. The thresholds are absolute: with three personas the highest reachable severity is high, with four it is critical only when all agree; say so in the report header when the roster is under five
5. **The strongest revised version of the idea.** Rewrite the idea to take in the consensus points and address the critical and high concerns, in the user's own terms, no longer than the original plus a third. Mark it as a proposal. Where a split would change the revision, give the two forms in a sentence each
6. **Open questions for the user.** What only the user can decide, and what a source could settle
7. **Honesty line.** One sentence: the personas are simulated viewpoints, not real people or official positions, and the report records disagreement as found

Never add the facilitator's own view of the idea. Never break a tie. Never drop a low concern to make the report cleaner.

---

## 5. Talk mode (frame and summary)

- On the first talk turn, return the frame (section 1) and ask who the user wants to address
- **The router keeps a running summary**: the frame, then one line per turn (who spoke, the point made). The router pastes it into each persona turn so the conversation has memory without sharing contexts; the facilitator is a one-shot agent and receives it on `summary`
- On `summary`, write a short report (section 4), from the running summary and the turns, marking which points came from a single turn rather than a round

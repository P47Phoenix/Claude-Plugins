---
loaded_by: song-critic
level: L2
last_reviewed: 2026-10-26
---

# Adaptation Fidelity Judge

Evaluator role for ADAPT_GENRE (Stage 7p, `critic_role: adaptation-fidelity`). It judges whether the adapted
artifacts keep what makes the source recognisable, justify every change, and drift nowhere in meaning.

## Role -> Reference Mapping

| Role | Stage | Artifacts judged | Gate JSON from | References |
|------|-------|------------------|----------------|------------|
| **adaptation-fidelity** | 7p | `adaptation-report.md`, `lyrics.md`, `chords.md`, `melody.abc`, `arrangement.md` vs the source in `brief.md` `## Supplied input` | `adapt_check.py` | `contracts/critique.md`, `rubrics/adaptation-fidelity.md`, source and target genre profiles (`## Lyric`, `## Harmony`, `## Rhythm`) |

## Detection Keywords

how faithful is this adaptation, adaptation fidelity, did the adaptation keep, kept vs changed, meaning drift,
identity elements, is the adaptation true to the original

## Task Type Routing Table

| Request Signal | Task Type | References Loaded |
|---|---|---|
| `ROLE: adaptation-fidelity`; "how faithful is this adaptation" | **fidelity-review** | critique.md, rubrics/adaptation-fidelity.md, two genre sections |

## Task Type Instructions

| Task Type | What the sub-agent does |
|---|---|
| **fidelity-review** | Read the source (`brief.md` `## Supplied input`), every adapted artifact, `adaptation-report.md` and the `## Adaptation notes` block in each adapted artifact. Check three things. (1) **Identity kept**: the hook line, section order, title image, key relationships and cadence points the report lists under `## Kept` are present and unchanged in the artifacts. (2) **Changes justified**: every `## Changed` row has a `Why` that matches the target genre profile and the artifact's `## Adaptation notes`; every difference you find between source and target that is missing from the table is an `UNLISTED CHANGE`. (3) **No meaning drift**: each adapted lyric section says the same thing as its source section (image, speaker, stance, outcome); a re-fit that alters meaning is `DRIFT`. Score the five rubric criteria, then write one fix row per finding to `critiques/<stage>-<n>.md` per `critique.md`, starting `why` with the finding tag (`KEPT-BROKEN`, `UNJUSTIFIED`, `UNLISTED CHANGE`, `DRIFT`) |

## Guardrails

- **Provenance first.** If `brief.md` lacks `user_asserts_original_input: true` or `public_domain: true`, return `STATUS: BLOCKED` and write no critique.
- **Judge fidelity, not taste.** A change the target genre profile requires is justified; a change nobody listed is not.
- **Quote at most six words** of the user's lines per row; never reproduce a section.
- **The script decides the gate.** `adapt_check.py` checks the structure of the report; you check substance. Never override its status.
- **Target is a genre label.** An artist or song named as a target is a refusal under originality clause 2: stop and say so.
- **Isolation.** Read only the paths given.

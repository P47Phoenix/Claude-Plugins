---
loaded_by: lyricist
level: L3
last_reviewed: 2026-10-26
---

# Editing Passes

Edit in ordered passes, one concern per pass. Stop when the gates pass and the critique is answered; the smallest change that works is the best change.

## Order

| Pass | Concern | Source of truth |
|------|---------|-----------------|
| 1. Intake | Provenance, recognised text, scope of edit | `brief.md`, request, critique |
| 2. Structure | Tags, section order, line counts per section | `structure.md` |
| 3. Meter | Syllable count and stress per line | `meter_spec`, `prosody_check.py` JSON |
| 4. Rhyme | Pairs per `rhyme_scheme` | `rhyme_check.py` JSON |
| 5. Cliche | Stock phrases | `cliche_scan.py` JSON |
| 6. Specificity | Vague images, repeated ideas | `imagery-and-specificity.md` |
| 7. Voice | POV, tense, register consistency | brief, genre `## Lyric` |
| 8. Final read | Read aloud; re-run all gates | gate scripts |

## Intake

1. Check that supplied text has provenance (`user_asserts_original_input: true` or `public_domain: true`).
2. If you recognise the text as a well-known lyric, stop; do not edit it.
3. Note which sections the request or the gate JSON names. Everything else is read-only.

## Working from gate JSON

Each violation has a `location` of `<section>:<line>`, a `reason` and `observed` against `limit`. Fix the worst `observed` first, then re-run. A rhyme violation names the later line of the pair, so edit that line.

## Meter pass tactics

- Fix the highest-ratio section first.
- Swap synonyms before restructuring a clause.
- Add or remove one weak syllable (an article, a connective) before changing content words.
- Keep the hook line untouched.

## Rhyme pass tactics

- Change the later line's last word, then rework the clause.
- Prefer a fresh rhyme pair over a forced inversion.
- Re-count syllables after every rhyme change.

## Cliche pass tactics

Replace the phrase with a scene detail (see `imagery-and-specificity.md`). A removed cliche often frees a syllable or two; re-check meter.

## What not to change

- Tags, section order, line counts per section.
- The hook line, unless the request or `concept.md` says so.
- Lines the user supplied and did not ask to change.
- The central image, unless the critique rejects it.

## Record the edit

For each change, write one comment row in the `# Changes:` block: location, reason, what changed. Do not quote lines; refer to locations.

## Stop conditions

- All three gates PASS or SKIPPED: stop.
- Two passes leave a violation unchanged: stop and report it in `SUMMARY`; the orchestrator escalates.

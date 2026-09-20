---
run: run-2026-05-28-o48m
story: S2
role: tech-writer (DoD validator)
---
# S2 tech-writer review

Note: skill `delivery-team:tech-writer` unknown; role applied directly. No prose_style key in .delivery/config.yml; caveman-lite judged from neighbouring text.

## Checks
- Line counts: delivery-flow 499, prompt-engineer 520 (unchanged; diff 32+/32-). PASS.
- Markdown: headings, fences, tables intact. PASS.
- Old-heading refs: no live refs to 'Model Awareness Note (Opus 4.7', 'Model-specific optimisation: Opus 4.7', 'Versioned Model Reference' outside archived retro. Internal refs (prompt-engineer/SKILL.md:397, :408) resolve to renamed heading. PASS.
- Frontmatter of the 3 files: not in diff. PASS.
- Hedge phrases: none new. Line 88 keeps "may duplicate" (pre-existing, factual).

## Warnings (0 blocking)
1. prompt-engineer/SKILL.md:5 vs :420: line 420 says `model_awareness` is a version-free stamp (`latest`), but frontmatter still `opus-4-7` (untouched by scope). Reader sees contradiction. Suggest: follow-up story sets `model_awareness: latest`; or line 420 append "(frontmatter migrates in a later story)" (same line count).
2. delivery-flow/SKILL.md:275-276: "subagents" vs "sub-agent(s)" used elsewhere; two clauses restate cap. Suggest 2 lines:
   `> silent sub-agent fusion or over-spawning is the highest-confidence regression mode.`
   `> \`dod_validators.<stage>\` is the cap: dispatched roles per DoD checkpoint MUST NOT exceed its length, on any model.`
3. prompt-engineer/SKILL.md:355-357: bullet list of effort levels now has `xhigh` dropped while :353 still lists it as valid, and the "Start from API default" bullet sits between `high` and `max`. Suggest move that bullet after `max` (same line count, swap 357/358).
4. prompt-engineer/SKILL.md:361: one paragraph mixes delegation, verification, sampling. Suggest split sentence ends with "Leave sampling alone." (same line) for scannability.
5. prompt-engineer/SKILL.md:371: second sentence (serving infra drift) is off-topic for Pattern 4.1; trim or move.
6. Terminology: "prior models" (doctrine:79, SKILL:27, PE:361) vs "older models" (PE:351, :357). Pick one ("older models").
7. prompt-engineer/SKILL.md:347/363/373 heading mixes colon and em dash styles; colon matches the new naming convention at :408, subpatterns keep em dash. Acceptable; note only.

S2_TW: DONE

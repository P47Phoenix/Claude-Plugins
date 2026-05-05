---
story: story-1-delivery-flow-restructure
completed: 2026-05-03
status: DONE
---

# Story 1 — delivery-flow/SKILL.md Restructure

## Summary

4 tasks complete. SKILL.md: 1090 → 999 lines (−91).

## Task Outcomes

| Task | ADR | File(s) Touched | Outcome |
|------|-----|-----------------|---------|
| A — cache-prefix freeze | ADR-tk1-001 | governance/cache-prefix-hash.txt (created) | sha256 written; `## Volatile` at line 977/999 |
| B — stages.yml extraction | ADR-tk1-001 | references/stages.yml (created), references/stages-schema.json (created), SKILL.md (−130 lines) | Inline Stage 1-7 blocks → 7-line pointer block |
| C — model: sonnet frontmatter | ADR-tk1-002 | SKILL.md frontmatter | `model: sonnet` + `extended_thinking: false` added; all prior keys preserved |
| D — adversarial-review doc update | ADR-tk1-003 | SKILL.md Step 6 | Model inheritance + extended_thinking default-OFF rule appended to adversarial review bullet |

## Files Created

- `governance/cache-prefix-hash.txt` — sha256 of bytes 0..2048 of SKILL.md
- `delivery-team/skills/delivery-flow/references/stages.yml` — 7394 bytes, all 7 stages
- `delivery-team/skills/delivery-flow/references/stages-schema.json` — JSON Schema (valid)

## Files Edited

- `delivery-team/skills/delivery-flow/SKILL.md` — 1090 → 999 lines (−91)

## Pre/Post Line Counts

| File | Before | After | Delta |
|------|--------|-------|-------|
| SKILL.md | 1090 | 999 | −91 |

## Cache Prefix

- Boundary: end of Phase 3 (line ~332, byte offset ~21360)
- sha256 of bytes 0..2048: `aea33d5732e31ab6455dda3675f7ad536d5d0e440a52dd0c1802ec2dabf03db9`
- Hash file: `governance/cache-prefix-hash.txt`

## Verification Results

| Check | Command | Exit |
|-------|---------|------|
| Frontmatter | `head -12 SKILL.md` | 0 |
| Volatile count | `grep -c "^## Volatile" SKILL.md` → 1 | 0 |
| Hash file | `cat governance/cache-prefix-hash.txt` | 0 |
| stages.yml size | `pathlib.Path(...).stat().st_size > 100` → 7394 bytes | 0 |
| stages-schema.json | `python3 -c "import json; json.load(...)"` | 0 |
| Phases intact | `grep -c "^## Phase"` → 5 | 0 |

## Known Limitations / Wave 2+ Follow-Ups

1. **YAML structural validation**: `yaml` is not in Python stdlib. stages.yml content
   correctness was verified by visual inspection. Wave 2 should add a `yamllint` or
   PyYAML validation step to CI.
2. **stages.yml runtime loading**: SKILL.md now points to stages.yml but the orchestrator
   does not yet programmatically parse it at runtime (it reads the pointer block as
   documentation). Wave 2 should wire the orchestrator to load stages.yml as structured
   data for routing decisions.
3. **Hash refresh protocol**: If SKILL.md is edited, `governance/cache-prefix-hash.txt`
   must be regenerated. A Wave 2 pre-commit hook should enforce this.

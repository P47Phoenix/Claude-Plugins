---
story: W2-3
skill: developer
wave: 2
date: 2026-05-03
author: Gimli (developer agent)
status: COMPLETE
---

# Story 3 Implementation: Developer Coding-Standards Extraction

## ADR Reference
ADR-tk2-003 — developer coding-standards block extracted to two reference files.

## Changes Made

### New Files
| File | Lines | Purpose |
|---|---|---|
| `developer/references/agent-prompts/coding-standards.md` | 55 | Sub-agent prompt + pre-flight check |
| `developer/references/coding-standards-template.md` | 119 | 10-section customizable template |

### Modified Files
| File | Before | After | Delta |
|---|---|---|---|
| `developer/SKILL.md` | 495 | 296 | -199 |
| `governance/skill-budgets.json` | developer debt entry present | entry removed | cleared |

## Dispatch Pointer (5 lines in SKILL.md)

```markdown
### `coding-standards` Task Type — Dispatch

Load `references/agent-prompts/coding-standards.md` for the sub-agent prompt.
Load `references/coding-standards-template.md` for the template content.
Skip language detection. Follow pre-flight and output instructions in the agent-prompt file.
```

## Budget Result

| Target | Actual | Status |
|---|---|---|
| ≤300 lines (Tier-B) | 296 lines | PASSED — no Wave-3 debt |
| ADR target (~340) | 296 | Exceeded target by 44 lines |

Wave-3 debt registration NOT required. Budget cleared.

## Routing Integrity

All 7 task types remain routable:
write / fix / refactor / review / test / explain / coding-standards

coding-standards dispatch: main context loads 2 files → sub-agent executes.
write/fix/etc: unaffected — standard language-ref + clean-code flow unchanged.

## Dogfood Evidence
`.delivery/artifacts/06-dev/dogfood-evidence/story-3-developer-evidence.md`

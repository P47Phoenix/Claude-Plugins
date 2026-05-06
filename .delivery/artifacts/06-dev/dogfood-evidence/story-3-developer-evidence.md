---
story: W2-3
task: developer coding-standards extraction
date: 2026-05-03
author: Gimli (developer agent)
---

# Dogfood Evidence: Story 3 — Developer Coding-Standards Extraction

## Pre-Flight Measurements

| Metric | Value |
|---|---|
| developer/SKILL.md lines (before) | 495 |
| coding-standards block location | lines ~164–320 |
| coding-standards block size | ~155 lines |

## Execution Log

### Step 1: New Reference Files Created

**`delivery-team/skills/developer/references/agent-prompts/coding-standards.md`**
- Created `references/agent-prompts/` directory (new)
- Contains: pre-flight check, sub-agent prompt, output instructions
- 55 lines

**`delivery-team/skills/developer/references/coding-standards-template.md`**
- Contains: 10-section team coding standards scaffold with HTML comment placeholders
- 119 lines (the template content itself)

### Step 2: developer/SKILL.md Inline Block Replaced

Replaced lines 164–320 (`### coding-standards Task Type Implementation` through closing ```)
with a 5-line dispatch pointer:

```
### `coding-standards` Task Type — Dispatch

Load `references/agent-prompts/coding-standards.md` for the sub-agent prompt.
Load `references/coding-standards-template.md` for the template content.
Skip language detection. Follow pre-flight and output instructions in the agent-prompt file.
```

### Step 3: Surplus Trimming (ADR-tk2-003 requirement)

Post-extraction count was 342 lines (40 over Tier-B 300). Trimming applied:

| Trim | Lines Saved | Method |
|---|---|---|
| References section (14 lang entries → 2-line pointer) | ~13 | Remove per-language descriptions; keep non-language refs |
| OOP/Frontend/FP trigger keyword lists | ~9 | Compress verbose trigger lists |
| Multi-Language Projects section | ~7 | 5 numbered items → 1 sentence |
| Sub-Agent Output Contract blank lines | ~8 | Remove blank lines inside fenced block |
| Clean Code Guide Resolution section | ~4 | Compress to numbered list |
| Clean Code Enforcement block | ~5 | Compact enforcement format |

**Total trimmed: ~46 lines**

## Post-Flight Measurements

| Metric | Value |
|---|---|
| developer/SKILL.md lines (after) | 296 |
| Tier-B budget (≤300) | PASSED |
| Governance debt entry | REMOVED (budget cleared) |

## Routing Verification

Task types verified still present in routing table:
- write: present
- fix: present
- refactor: present
- review: present (with enforcement block)
- test: present
- explain: present
- coding-standards: dispatch pointer → 2 reference files

## Dogfood Assertions

1. `write` task routing: unchanged — loads language ref + clean-code → sub-agent
2. `coding-standards` task routing: loads agent-prompts/coding-standards.md + coding-standards-template.md (template NOT loaded for write tasks — confirmed dispatch is conditional)
3. New files exist at correct paths (verified by file creation)
4. Governance entry for developer removed (budget ≤300 achieved)

# Dev Notes: Cross-Skill Shared References — SPIKE Prototype (#47)

**Developer**: Gimli
**Date**: 2026-04-01
**Status**: DONE
**Type**: SPIKE prototype implementation
**Source Issue**: #47
**Architecture Decision**: ADR-047 — Formalized Status Quo (Approach 5)

> "Two cross-references do not require a framework. They require a map. And my code!"

---

## 1. Files Created/Modified

### Created

| File | Purpose |
|------|---------|
| `delivery-team/CROSS-SKILL-REFERENCES.md` | Developer guide documenting the cross-skill reference convention, path format, rules, current references, and how to add new ones |
| `delivery-team/scripts/validate_cross_refs.py` | CI validation script — scans SKILL.md files for cross-skill references, verifies target files exist on disk |

### Modified

| File | Change |
|------|--------|
| `delivery-team/skills/godot/SKILL.md` | Added `## Cross-Skill References` section declaring dependency on `developer/references/clean-code.md` |
| `delivery-team/skills/alias-creator/SKILL.md` | Added `## Cross-Skill References` section declaring dependency on `delivery-flow/references/aliases/*.yml` |

---

## 2. Validation Script Test Results

### Positive Test (real plugin directory)

```
$ python delivery-team/scripts/validate_cross_refs.py delivery-team/
Scanning 11 SKILL.md files in /var/home/meconnelly/Documents/GitHub/Claude-Plugins/delivery-team

Found 2 cross-skill reference(s):

  [OK] alias-creator/SKILL.md:189
         path: delivery-team/skills/delivery-flow/references/aliases/*.yml

  [OK] godot/SKILL.md:223
         path: delivery-team/skills/developer/references/clean-code.md

Result: 2 valid, 0 broken

OK: All cross-skill references are valid.
EXIT CODE: 0
```

### Negative Test (phantom reference)

```
$ python validate_cross_refs.py /tmp/test-plugin/
Scanning 1 SKILL.md files in /tmp/test-plugin

Found 1 cross-skill reference(s):

  [FAIL] test-skill/SKILL.md:6
         path: delivery-team/skills/fake/references/nonexistent.md
         resolved to: /tmp/test-plugin/skills/fake/references/nonexistent.md
         FILE NOT FOUND

Result: 0 valid, 1 broken

FAIL: Broken cross-skill references detected.
EXIT CODE: 1
```

Both cases work as designed. Valid refs pass, phantom refs fail.

---

## 3. Per-Deliverable Status

| Deliverable | Status | Notes |
|-------------|--------|-------|
| Developer Guide (`CROSS-SKILL-REFERENCES.md`) | DONE | Covers convention, path format, rules, current refs, how-to-add, when-not-to, review triggers. Addresses Challenger condition #2 (breaking change contract) and #4 (discoverability gap acknowledged). |
| SKILL.md Cross-Reference Sections (godot) | DONE | Formal table with path, owner, purpose. Stability note included. |
| SKILL.md Cross-Reference Sections (alias-creator) | DONE | Formal table with glob path for 13 alias themes. Stability note included. |
| CI Validation Script (`validate_cross_refs.py`) | DONE | Stdlib-only Python. Accepts plugin root as CLI arg. Parses formal tables AND inline cross-skill paths. Handles glob patterns (`*.yml`). Deduplicates. Exit 0/1. Addresses Challenger condition #1 (CI script is a deliverable, not a follow-up). |

---

## 4. Verification Status

| Type | Coverage | Notes |
|------|----------|-------|
| **Structural** | 4/4 deliverables | All files created/modified at correct paths. Cross-reference sections inserted at correct locations in SKILL.md files. |
| **Empirical** | 2/4 deliverables | Validation script tested against real plugin (positive) and synthetic broken refs (negative). Both exit codes verified. Guide and SKILL.md sections are documentation — empirical validation means a new skill author follows the guide (UAT gate). |

### Pre-existing Cross-References Verified

| Reference | File Exists? | Method |
|-----------|-------------|--------|
| `delivery-team/skills/developer/references/clean-code.md` | YES | `ls` verified on disk + validation script reports OK |
| `delivery-team/skills/delivery-flow/references/aliases/*.yml` | YES (13 files) | `ls` verified 13 .yml files on disk + validation script reports OK |

### Challenger Conditions Addressed

| Condition | Status |
|-----------|--------|
| #1: CI validation script is a sprint deliverable | MET — script built and tested |
| #2: Breaking change contract documented | MET — both CROSS-SKILL-REFERENCES.md and each SKILL.md section include stability note |
| #3: ADR review trigger for platform-native support | MET — included in CROSS-SKILL-REFERENCES.md review triggers |
| #4: Discoverability gap acknowledged | MET — guide exists at plugin root; convention documented but not self-evident |

---

## 5. Technical Notes

- **Regex approach**: The script uses two detection methods — formal table parsing (`| \`path\` |` rows) and inline path scanning (regex for `skills/<name>/references/<file>`). The inline scanner skips self-references to avoid false positives.
- **Glob support**: The alias-creator reference uses `*.yml`. The script handles this via `pathlib.glob()`, verifying at least one file matches.
- **Deduplication**: If the same path appears in both the formal table and inline text (as in godot's SKILL.md), it is reported once.
- **No external dependencies**: stdlib only — `re`, `sys`, `pathlib`.

---

```
STATUS: DONE
ARTIFACT: .delivery/artifacts/06-dev/developer/dev-notes.md
SUMMARY: SPIKE #47 prototype: 4 deliverables (guide, 2 SKILL.md sections, CI script). Validation script tested — 2 refs valid, phantom detection works. Exit 0.
```

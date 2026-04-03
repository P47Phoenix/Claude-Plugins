# Dev Notes: US-01 -- Plugin Scaffold

**Story**: US-01 | **SP**: 2 | **Sprint**: 1
**Developer**: Gimli
**Files Created**: `mtg-commander/SKILL.md`, `mtg-commander/LICENSE.txt`
**Files Modified**: `.claude-plugin/marketplace.json`
**Directories**: `mtg-commander/`, `mtg-commander/references/`, `mtg-commander/scripts/` (pre-existing empty dirs reused)

---

## Verification

| AC | Status | Method |
|----|--------|--------|
| 1.1 | PASS | `ls mtg-commander/` -- directory exists at repo root, kebab-case |
| 1.2 | PASS | `cat mtg-commander/SKILL.md` -- stub with YAML frontmatter (name, description, license) |
| 1.3 | PASS | `cat mtg-commander/LICENSE.txt` -- full Apache 2.0 text with copyright 2026 Michael Connelly |
| 1.4 | PASS | `python3 -m json.tool .claude-plugin/marketplace.json` -- valid JSON, entry with `"name": "mtg-commander"`, description, `"source": "./"`, `"skills": ["./mtg-commander"]` |
| 1.5 | PASS | `ls mtg-commander/references/ mtg-commander/scripts/` -- both subdirectories exist |
| 1.6 | PASS | No `agents/`, `skills/`, `hooks/`, `plugin.json`, or `.mcp.json` created (per ADR-001) |
| 1.7 | PASS | SKILL.md documents `api.scryfall.com` as required WebFetch domain |

## Test Cases

| # | Status | Result |
|---|--------|--------|
| T1.1 | PASS | `ls mtg-commander/` shows SKILL.md, LICENSE.txt, references/, scripts/ |
| T1.2 | PASS | marketplace.json passes `python3 -m json.tool`, contains `"name": "mtg-commander"` |
| T1.3 | PASS | SKILL.md frontmatter has name, description, license; body mentions `api.scryfall.com` |
| T1.4 | PASS | `ls mtg-commander/agents/` returns "No such file or directory" (expected) |

## Design Decisions

1. **Apache 2.0 license**: Per AC 1.3 and architecture doc, not MIT. The repo root LICENSE is MIT but this plugin uses Apache 2.0 per spec.
2. **No plugin.json**: Architecture ADR-001 explicitly excludes plugin.json. This repo uses `.claude-plugin/marketplace.json` for plugin registration.
3. **SKILL.md frontmatter**: Follows the pattern from `research-agent/SKILL.md` and `prompt-engineer/SKILL.md` -- YAML frontmatter with name, description, license.
4. **Marketplace entry**: Matches architecture doc S2 specification exactly -- name, description, source, strict, skills array.
5. **Pre-existing directories reused**: `mtg-commander/`, `references/`, `scripts/` already existed (empty). Added files into them rather than recreating.

## Deviations

None. All 7 acceptance criteria met as specified.

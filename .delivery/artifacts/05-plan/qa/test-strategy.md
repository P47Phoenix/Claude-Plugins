# Test Strategy — DOCS_ONLY Documentation Refresh

**Author:** Legolas (QA, `lotr-full`) · Stage 05-Plan · Tier: markdown
**Input:** `tech-writer/doc-stories.md` (8 stories) · `sm/sprint-plan.md` (2 sprints)

> "They are taking the Hobbits to... documentation." I shall count every arrow.

---

## Philosophy

Deterministic mechanical checks (grep / JSON-load / file-existence) + 3 journey walks. Subjective quality owned by Content Gate & User Review.

Test types: **T-EXIST** (`test -f`), **T-CONTENT** (`grep -q` sections/phrases), **T-LINK** (every `](path)` resolves), **T-JSON/YAML** (parseable), **T-STALE** (regressed tokens absent), **T-JOURNEY** (walk the 3 Galadriel journeys post-update).

## Traceability

| Story | EXIST | CONTENT | LINK | JSON/YAML | STALE | JOURNEY |
|-------|-------|---------|------|-----------|-------|---------|
| US-1 mtg-commander/README.md | TC-01 | TC-02, TC-03 | TC-20 | — | — | TC-J2 |
| US-2 .yml.example + walkthrough | TC-04 | TC-05 | — | TC-14 | — | TC-J2 |
| US-3 CLAUDE.md | — | TC-06, TC-07 | TC-20 | — | TC-16 | — |
| US-4 README.md | — | TC-08, TC-09 | TC-20 | — | TC-17 | TC-J1, TC-J2 |
| US-5 delivery-team Advanced | — | TC-10, TC-11 | TC-20 | — | — | TC-J1, TC-J3 |
| US-6 marketplace.json | — | TC-12 | — | TC-13 | — | — |
| US-7 cross-link audit | — | — | TC-20 | — | TC-19 | TC-J1/J2/J3 |
| US-8 troubleshooting blocks | — | TC-15, TC-18 | TC-20 | — | — | — |

Every story has ≥1 test case.

## Test Cases

- **TC-01** `test -f mtg-commander/README.md`.
- **TC-02** `grep -qE "^## .*[Qq]uick" mtg-commander/README.md` + Configuration + Troubleshooting headings present.
- **TC-03** `grep -q "max_card_price"` AND `grep -q "escalation"` in mtg-commander/README.md.
- **TC-04** `test -f mtg-commander/.mtg-commander.yml.example`.
- **TC-05** `grep -q "max_card_price"` AND `grep -q "escalation"` in the example file.
- **TC-06** `grep -q "mtg-commander" CLAUDE.md` within Available Plugins section.
- **TC-07** `grep -qE "constraints|Architecture Board|Transformation" CLAUDE.md` in delivery-flow architecture section.
- **TC-08** `grep -q "mtg-commander" README.md` (root).
- **TC-09** `grep -qE "9 types|narrative intelligence|light mode" README.md`.
- **TC-10** `grep -qE "[Aa]dvanced [Cc]apabilities|[Rr]ecent [Aa]dditions" delivery-team/README.md`.
- **TC-11** `grep -qE "constraints|[Aa]rchitecture [Bb]oard|[Tt]ransformation|[Pp]aradigm" delivery-team/README.md`.
- **TC-12** Every top-level plugin dir matches a `marketplace.json` `id`; no orphans either direction.
- **TC-13** `python3 -c "import json; json.load(open('.claude-plugin/marketplace.json'))"` exits 0.
- **TC-14** `python3 -c "import yaml; yaml.safe_load(open('mtg-commander/.mtg-commander.yml.example'))"` exits 0.
- **TC-15** `grep -qE "[Tt]roubleshoot"` in BOTH `README.md` and `delivery-team/README.md`.
- **TC-16** STALE: `project_type:` as active config absent from CLAUDE.md (any match must adjoin the "removed in v2.7" note).
- **TC-17** STALE: `grep -q "4 types.*3.*output formats" README.md` returns non-zero (phrase gone).
- **TC-18** Troubleshooting blocks reference `.delivery/`, `.claude/settings.local.json`, or `CONTRIBUTING.md`.
- **TC-19** Paradigm redirect stubs still point at `paradigms/volatility/SKILL.md` and `paradigms/ddd/SKILL.md`; targets exist.
- **TC-20** For each touched file, extract `](*.md)` references, assert target resolves:
  ```bash
  for f in mtg-commander/README.md README.md CLAUDE.md delivery-team/README.md; do
    grep -oE '\]\(([^)]+\.md)\)' "$f" | sed -E 's/\]\(([^)]+)\)/\1/' | while read p; do
      base=$(dirname "$f"); [ -f "$base/$p" ] || [ -f "$p" ] || echo "BROKEN: $f -> $p"
    done
  done
  ```
  Empty output = pass.

## Journey Tests

- **TC-J1 (Pipeline user):** root README → delivery-team/README.md → Advanced section → `constraints-model-guide.md` link resolves. ≤3 hops, no dead links.
- **TC-J2 (MTG builder — the previously-dark path):** root README → mtg-commander row → mtg-commander/README.md → Configuration → `.mtg-commander.yml.example` → SKILL.md schema pointer. User learns price-control authoring without reading SKILL.md end-to-end. **This cycle exists to light this journey.**
- **TC-J3 (Contributor):** root README → CONTRIBUTING.md → delivery-team Advanced names paradigm selection → link to `architect/skills/paradigms/` resolves.

## Execution Order

1. Per-story local: TC-01…TC-19 during story completion.
2. Integration: TC-20 after Sprint 2 finishes (gates US-7).
3. Journey: TC-J1/J2/J3 before ship.
4. Final gate: all 23 TCs green.

## Out of Scope

Subjective readability (Content Gate), MkDocs build (deferred cycle), SKILL.md content (not touched — CLAUDE.md is project instructions, not a SKILL).

> "Every story has its arrow."

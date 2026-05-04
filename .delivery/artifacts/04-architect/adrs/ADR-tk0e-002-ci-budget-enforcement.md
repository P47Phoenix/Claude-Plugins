# ADR-tk0e-002: CI Budget Enforcement Mechanism

**Status**: Accepted (Architect DoD — 2026-05-03)
**Deciders**: Architect (solution_architect), Product Owner
**PRD refs**: FR-06, FR-07, FR-08, FR-09, FR-10, FR-12, NFR-03, NFR-04
**Binds**: `.github/workflows/skill-line-budget.yml`, `scripts/check_skill_budgets.py`

---

## Context

No CI enforcement exists for SKILL.md line budgets. Six delivery-team files already exceed their
tier thresholds (FR-08 / AC-10). Without a regression guard, Wave 1–3 reduction efforts will
regress. The mechanism must: (a) fail new over-budget files hard, (b) allow existing over-budget
files through via a known-debt bypass, (c) warn on permissive language without blocking, and
(d) carry no external Python dependencies (repo convention: no external dependency management).

Gate-patterns memory establishes: **allowlist-over-deny** for mixed-scope guards; and
**provenance comment + CI-guard allowlist travel as a named pair**.

---

## Decision

### Workflow trigger

```yaml
on:
  pull_request:
    paths:
      - 'delivery-team/**/SKILL.md'
      - 'governance/skill-budgets.json'
```

Paths-filter ensures the job only runs when relevant files change. This is an allowlist
approach consistent with the gate-patterns binding (allowlist-over-deny).

### Script: `scripts/check_skill_budgets.py`

Pure Python, no external imports. Implementation contract:

**Tier source-of-truth** (two-tier fallback):
1. Parse `tier:` field from YAML frontmatter (lines between leading `---` delimiters) of the
   SKILL.md file being checked. This is the primary source.
2. If `tier:` is absent from frontmatter, look up the skill path in
   `governance/skill-budgets.json` registry (legacy fallback for pre-frontmatter SKILL.md files).
3. If neither source has a tier: exit 1 with hint "Add `tier: A|B|C` to SKILL.md frontmatter."

**Tier budget constants** (exactly these three values, no others):
```python
TIER_LIMITS = {"A": 500, "B": 300, "C": 200}
```

**Failure modes**:
| Condition | Exit code | Output |
|-----------|-----------|--------|
| SKILL.md line count exceeds tier budget AND not in known-debt list AND no PR-body exception | 1 | `BUDGET VIOLATION: <path> <count>/<limit> lines (Tier-<X>)` |
| SKILL.md missing `tier:` field (not in fallback registry either) | 1 | `MISSING TIER: <path> — add \`tier: A\|B\|C\` to frontmatter` |
| SKILL.md in known-debt list (over-budget) | 0 | `KNOWN-DEBT: <skill>/SKILL.md <count>/<limit> lines — target wave: W<N>` to stdout |
| PR body contains `Budget-Exception: <token>` | 0 | `EXCEPTION ACKNOWLEDGED: <path> — budget override active` + warning summary to stderr |
| Permissive-language pattern match (outside exempt zones) | 0 | Warning to stderr only; no exit 1 |

### Known-debt pre-registration

The 6 over-budget files at Wave 0 baseline are **hard-coded** as pre-registered known-debt in
`check_skill_budgets.py`. They do NOT require a `Budget-Exception:` PR-body token — they are
exceptions by audit status. The `Budget-Exception:` mechanism is for future one-off exceptions.

Pre-registered known-debt list (from AC-10 baseline):

```
delivery-team/skills/delivery-flow/SKILL.md        1089/500  target: W1
delivery-team/skills/product-delivery/SKILL.md      688/300  target: W1
delivery-team/skills/architect/SKILL.md             670/300  target: W1
delivery-team/skills/presentation/SKILL.md          543/300  target: W2
delivery-team/skills/ui/SKILL.md                    493/300  target: W2
delivery-team/skills/developer/SKILL.md             493/300  target: W1
```

### Permissive-language sub-check

**Warn-only** (exit 0). Patterns checked: `\bshould\b`, `\bcan\b`, `\bmay\b`, `\bmight\b`.

**Exempt zones** (scanner MUST skip these regions):
- Fenced code blocks: content between ` ``` ` delimiters (triple-backtick, any language tag)
- Blockquotes: lines beginning with `>`
- Table rows: lines beginning with `|`

Rationale for warn-only over hard-fail: adversarial, debate, and compliance skills legitimately
use these words in quoted prose (e.g., "challenger may propose..."). Hard-fail would produce
systemic false positives that erode CI credibility. Warn-only preserves signal without blocking.

**Documentation pairing** (gate-patterns lesson): the exempt-zone allowlist MUST be documented
in a comment block immediately above the permissive-language scanner function in the script.
The comment MUST name which patterns are exempted and why (provenance + allowlist travel together).

---

## Consequences

**Positive**:
- Zero external Python dependencies; runs in any standard Python 3.8+ environment.
- Allowlist-over-deny (paths-filter + known-debt pre-registration) survives model-ID bumps and
  future refactor PRs without requiring allowlist updates.
- Warn-only permissive check avoids false-positive CI failures on adversarial skills.

**Negative/Trade-offs**:
- Known-debt list is hard-coded in script; updating it requires a code change. Acceptable:
  each known-debt removal requires a deliberate Wave refactor PR anyway.
- Budget-Exception PR-body parsing adds complexity; but it is the agreed escape hatch (Ruling 3).

---

## Alternatives Considered

| Option | Decision | Reason rejected |
|--------|----------|-----------------|
| Hard-fail on permissive language | Rejected | False-positive rate too high for adversarial/debate skills (see rationale above) |
| External YAML parser for frontmatter | Rejected | Repo convention: no external deps; stdlib regex sufficient for simple frontmatter |
| Deny-all over-budget (no known-debt bypass) | Rejected | Would block Wave 0 merge; known-debt bypass is the designed migration path (Ruling 3) |
| GitHub Actions matrix per tier | Rejected | Single script with internal routing is simpler and easier to dogfood locally |

---

*Authors must build via `plugin-dev:plugin-structure` + `plugin-dev:skill-development`
then validate via `plugin-dev:skill-reviewer` + `plugin-dev:plugin-validator` (CLAUDE.md constraint).*

---
title: "Skill Token-Economy — Wave 0 PRD"
work_items: [W0-1, W0-2]
sprint: single-iteration, 2-WI ceiling
stage: 02-refine
author: Product Owner (product-delivery skill)
source: idea-brief v1.0 + BACKLOG-100
created: 2026-05-03
version: 1.0
---

# PRD: Skill Token-Economy — Wave 0 Foundations

## 1. Problem Statement

The delivery-team plugin's 13 SKILL.md files (11 top-level + 2 paradigm sub-skills under
`architect/paradigms/{ddd,volatility}/`) have no token-usage telemetry and no line-budget
enforcement. Six files already exceed their tier budgets by 193–589 lines, translating directly
to excess input tokens and reduced cache hit ratios on every skill invocation. Without a
measurement layer (W0-1) and a regression guard (W0-2), all Wave 1–3 reduction efforts lack a
feedback loop and gains will regress within 6 months (per governance expert finding, audit 2026-05-03).

---

## 2. Goals & Success Metrics

| Metric | Target | Baseline (2026-05-03 audit) |
|--------|--------|-----------------------------|
| Telemetry JSONL written per skill invocation | 1 row, all 7 fields present | 0 rows (no hook exists) |
| Hook overhead per call (mean, 10-run sample) | < 50 ms | Unmeasured |
| CI gate fails synthetic over-budget PR | Yes (exit 1 with budget violation) | No gate exists |
| delivery-team SKILL.md files with `tier:` frontmatter | 13 / 13 | 0 / 13 |
| Known-debt skills logged in CI output | 6 (matching audit) | 0 |

---

## 3. User Personas

| Persona | Description | Primary need |
|---------|-------------|--------------|
| **Primary** — delivery-team plugin contributor | Engineers adding/modifying delivery-team SKILL.md files | CI gate blocks accidental budget overruns; clear known-debt log |
| **Secondary** — Wave 1+ executor | Downstream team running W1-1 through W3-3 optimizations | Telemetry data available before Wave 1 starts; gate enforces gains post-reduction |

---

## 4. Functional Requirements

| ID | Requirement | Priority | AC Reference (BACKLOG-100 §) |
|----|-------------|----------|-------------------------------|
| FR-01 | A new `delivery-team/hooks/telemetry.py` MUST fire on every `PreToolUse` Skill event and write exactly one JSONL row to `.delivery/telemetry/skill-loads.jsonl` | Must Have | W0-1 AC-1 |
| FR-02 | Each JSONL row MUST contain fields: `skill`, `model`, `prefix_hash` (sha256 first 8 chars), `input_tokens`, `cache_read_tokens`, `cache_write_tokens`, `timestamp` (ISO 8601), `session_id` | Must Have | W0-1 AC-2; idea-brief §8 pre-loaded schema |
| FR-03 | `delivery-team/hooks/hooks.json` MUST register the telemetry hook with matcher type `PreToolUse`, tool pattern `Skill` | Must Have | W0-1 (hooks discipline binding) |
| FR-04 | A new `delivery-team/references/telemetry-schema.md` MUST document the JSONL schema as version 1 | Must Have | W0-1 AC-2 |
| FR-05 | A new `delivery-team/hooks/telemetry_report.py` MUST produce a non-empty mean-tokens-per-run table when run against ≥5 rows | Must Have | W0-1 AC-3 |
| FR-06 | All 13 delivery-team SKILL.md files MUST have `tier: A`, `tier: B`, or `tier: C` frontmatter added; tier defaults: Tier-A for orchestrators (`delivery-flow`), Tier-B for role multiplexers (9 top-level role skills), Tier-C for leaf skills + paradigm sub-skills (`architect/paradigms/ddd`, `architect/paradigms/volatility`); no other SKILL.md content MUST be modified | Must Have | W0-2 AC-1 |
| FR-07 | A new `.github/workflows/skill-line-budget.yml` MUST fail (exit 1) any PR where a delivery-team SKILL.md exceeds its declared tier budget (A ≤ 500 / B ≤ 300 / C ≤ 200) | Must Have | W0-2 AC-2 |
| FR-08 | A new `scripts/check_skill_budgets.py` MUST implement the budget check; MUST log the 6 known-debt skills in format `KNOWN-DEBT: <skill>/<SKILL.md> <current>/<budget> lines — target wave: W<N>` | Must Have | W0-2 AC-3 |
| FR-09 | `check_skill_budgets.py` MUST include a warn-only permissive-language sub-check; the allowlist of permitted patterns is `\bshould\b`, `\bcan\b`, `\bmay\b`, `\bmight\b` matched outside fenced code blocks, blockquotes, and tables; matches MUST emit a warning and MUST NOT cause a non-zero exit | Must Have | W0-2 AC-4 |
| FR-10 | CI gate MUST allow known-debt bypass when PR body contains `Budget-Exception: <ADR-link>`; current 6 over-budget skills are pre-registered known-debt and MUST NOT require ADRs | Must Have | BACKLOG-100 W0-2; Ruling 3 |
| FR-11 | `telemetry.py` MUST be standalone pure Python — NO Anthropic SDK import, NO LLM call | Must Have | Hooks Discipline binding |
| FR-12 | Every script path referenced in `hooks.json` MUST exist on disk before merge | Must Have | Memory lesson 4 (phantom hooks regression guard) |

---

## 5. Non-Functional Requirements

| ID | Requirement | Verification |
|----|-------------|--------------|
| NFR-01 | Hook overhead MUST be < 50 ms per call (mean across 10 invocations) | Time 10 skill invocations with/without hook; delta MUST be < 50 ms mean |
| NFR-02 | Telemetry JSONL schema MUST be versioned v1; version field MUST appear in `telemetry-schema.md` | `grep 'version: 1' delivery-team/references/telemetry-schema.md` MUST match |
| NFR-03 | CI gate MUST fail (exit non-zero) on a synthetic PR that introduces one line exceeding tier budget | Proven via test PR in CI before merge |
| NFR-04 | Tier budgets are exactly Tier-A ≤ 500 / Tier-B ≤ 300 / Tier-C ≤ 200 — no other values permitted | `grep -n 'TIER_LIMITS\|500\|300\|200' scripts/check_skill_budgets.py` MUST show exactly these three values |

---

## 6. Out of Scope

- Wave 1 items (W1-1 through W1-6) — blocked until W0-1 + W0-2 land
- Wave 2 items (W2-1 through W2-6)
- Wave 3 items (W3-1 through W3-3)
- Any plugin other than delivery-team
- Retroactive SKILL.md content migration (Wave 0 MUST NOT reduce line counts — only add `tier:` frontmatter)
- Telemetry analysis dashboards or visualization tooling
- Anthropic SDK usage inside hooks
- CI gates for non-delivery-team plugins

---

## 7. Dependencies & Risks

| Item | Type | Detail | Mitigation |
|------|------|--------|------------|
| `hooks.json` phantom reference | Risk (recurring defect) | Pre-merge check MUST verify every path in hooks.json exists on disk | FR-12 is a hard AC; verify via `python -c "import json,os; [os.path.exists(p) or (_ for _ in ()).throw(Exception(p)) for p in [e['script'] for e in json.load(open('delivery-team/hooks/hooks.json'))['hooks']]]"` |
| Permissive-language regex scope | Risk | Regex `\bshould\b|\bcan\b|\bmay\b|\bmight\b` MUST skip fenced code blocks, blockquotes, and tables to avoid false positives on SKILL.md content in those structures | FR-09 specifies allowlist + exempt zones; warn-only so false positives are non-blocking |
| PreToolUse fires before skill loads | Architectural note | Hook captures requested skill name, NOT the loaded content; `prefix_hash` MUST be computed from the SKILL.md path on disk, not from context | Documented in telemetry-schema.md v1; Dev MUST read hook event payload spec |
| CI budget-exception bypass mechanism | Dependency | `Budget-Exception:` PR-body parser MUST be implemented in `check_skill_budgets.py` before W0-2 is considered Done | Pre-registered known-debt (6 skills) handled as a hard-coded initial exception list in the script, not via PR-body bypass |
| plugin-dev skill routing | Process constraint | W0-1 MUST be built via `plugin-dev:hook-development`; W0-2 MUST use `plugin-dev:plugin-structure` + `plugin-dev:skill-development`; both MUST pass `plugin-dev:skill-reviewer` + `plugin-dev:plugin-validator` before merge | Developer DoD checklist includes skill-routing verification step |

---

## 8. Acceptance Criteria

### Sprint ceiling

This is a **2-WI, single-iteration sprint**. W0-1 and W0-2 are the only items. No new items may enter. No mid-sprint replan.

### Mandatory artifact list per WI

| WI | Artifact | Must exist at Done |
|----|----------|--------------------|
| W0-1 | `delivery-team/hooks/telemetry.py` | Yes |
| W0-1 | `delivery-team/hooks/telemetry_report.py` | Yes |
| W0-1 | `delivery-team/references/telemetry-schema.md` (v1) | Yes |
| W0-1 | `delivery-team/hooks/hooks.json` (updated, PreToolUse Skill entry) | Yes |
| W0-2 | `.github/workflows/skill-line-budget.yml` | Yes |
| W0-2 | `scripts/check_skill_budgets.py` | Yes |
| W0-2 | All 13 `delivery-team/**/SKILL.md` files with `tier:` frontmatter (11 top-level + 2 paradigm sub-skills, all Tier-C) | Yes |

### W0-1 runnable ACs

**AC-1** (hook fires + writes row):
```bash
tail -1 .delivery/telemetry/skill-loads.jsonl
# MUST: non-empty JSON line after a skill invocation
```

**AC-2** (all fields present):
```bash
python3 -c "import json; rows=[json.loads(l) for l in open('.delivery/telemetry/skill-loads.jsonl')]; req={'skill','model','prefix_hash','input_tokens','cache_read_tokens','cache_write_tokens','timestamp','session_id'}; [req-r.keys() and (_ for _ in ()).throw(KeyError(req-r.keys())) for r in rows]; print('PASS', len(rows), 'rows')"
# MUST: print PASS; MUST NOT raise
```

**AC-3** (schema v1 documented):
```bash
grep 'version: 1' delivery-team/references/telemetry-schema.md
# MUST: at least one match
```

**AC-4** (report script non-empty):
```bash
python3 delivery-team/hooks/telemetry_report.py
# MUST: non-empty mean-tokens table; MUST NOT raise or print nothing
```

**AC-5** (overhead < 50 ms — telemetry.py MUST support `--dry-run`):
```bash
python3 -c "import time,subprocess,statistics; s=[time.perf_counter() for _ in range(10) if not subprocess.run(['python3','delivery-team/hooks/telemetry.py','--dry-run'],check=True)]; print(f'irrelevant')"
# Practical form: time 10 --dry-run calls; compute mean delta; MUST be < 50 ms
```

**AC-6** (no LLM import):
```bash
grep -n 'anthropic\|openai\|litellm' delivery-team/hooks/telemetry.py
# MUST: no matches (grep exits 1 = PASS)
```

**AC-7** (no phantom hook paths):
```bash
python3 -c "import json,os; h=json.load(open('delivery-team/hooks/hooks.json')); bad=[e['script'] for e in h.get('hooks',[]) if not os.path.exists(e['script'])]; assert not bad, bad; print('PASS')"
# MUST: print PASS
```

### W0-2 runnable ACs

**AC-8** (all 13 SKILL.md files have `tier:` frontmatter; paradigm sub-skills MUST be `tier: C`):
```bash
find delivery-team -name 'SKILL.md' | wc -l   # MUST: 13
find delivery-team -name 'SKILL.md' -exec grep -qL "^tier:" {} \; -print  # MUST: no output
grep "^tier:" delivery-team/architect/paradigms/ddd/SKILL.md       # MUST: tier: C
grep "^tier:" delivery-team/architect/paradigms/volatility/SKILL.md # MUST: tier: C
```

**AC-9** (CI fails synthetic over-budget file):
```bash
python3 -c "open('/tmp/ob.md','w').write('---\ntier: C\n---\n'+'# x\n'*201)"
python3 scripts/check_skill_budgets.py --check /tmp/ob.md --tier C; echo "Exit: $?"
# MUST: exit 1; MUST print budget violation naming file and overage
```

**AC-10** (6 known-debt skills in output):
```bash
python3 scripts/check_skill_budgets.py --known-debt-report
# MUST: 6 lines matching: KNOWN-DEBT: <skill>/SKILL.md <current>/<budget> lines — target wave: W<N>
# Expected: delivery-flow(1089/500), product-delivery(688/300), architect(670/300),
#           presentation(543/300), ui(493/300), developer(493/300)
```

**AC-11** (permissive-language warn-only, no exit-1):
```bash
python3 scripts/check_skill_budgets.py --warn-permissive delivery-team/skills/delivery-flow/SKILL.md; echo "Exit: $?"
# MUST: exit 0; warnings to stderr are acceptable; MUST NOT exit 1
```

**AC-12** (budget-exception bypass implemented):
```bash
grep -n 'Budget-Exception' scripts/check_skill_budgets.py
# MUST: at least one match
```

---

## 9. Open Questions

**None.** All binding decisions are resolved in `.delivery/memory/topics/skill-token-economy.md`.

---

## 10. Verification Plan (dogfood — Stage 6 Dev MUST produce)

Stage 6 Developer DoD MUST produce the following dogfood evidence before marking Wave 0 Done:

1. **End-to-end pipeline run** — invoke at least one delivery-team skill through the normal pipeline with the telemetry hook active; attach the resulting `.delivery/telemetry/skill-loads.jsonl` output (≥1 row) to the PR.
2. **AC-5 timing report** — attach the stdout of the overhead measurement script showing mean < 50 ms.
3. **AC-9 CI failure screenshot or log** — a GitHub Actions run log showing the budget-violation CI step failing on the synthetic over-budget test file.
4. **AC-8 tier count** — paste the output of `find delivery-team -name 'SKILL.md' | wc -l` showing `13`; also paste the two `grep "^tier:"` checks for the paradigm sub-skills confirming `tier: C`.
5. **AC-10 known-debt report** — paste the full output of `python3 scripts/check_skill_budgets.py --known-debt-report` showing all 6 skills.

All 5 evidence items MUST appear in the PR body or linked gist. Reviewer MUST verify all 5 before approving merge.

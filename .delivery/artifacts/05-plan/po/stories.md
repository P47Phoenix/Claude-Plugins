---
title: "Wave 0 User Stories"
work_items: [W0-1, W0-2]
stage: 05-plan
author: Product Owner (product-delivery skill)
source: prd.md v1.0 + BACKLOG-100
created: 2026-05-03
sprint: single-iteration, 2-WI ceiling
---

# Wave 0 User Stories

---

## Story W0-1: Skill-load telemetry hook

**As a** delivery-team plugin contributor
**I want** a PreToolUse hook that captures token-cost telemetry per skill invocation
**So that** every Wave 1+ token-saving claim is measured, not opinion

**Story Points**: 2 (S — half day)
**Priority**: Critical (foundation for all subsequent waves)

### Acceptance Criteria

**Scenario 1 — Hook fires and writes one JSONL row**
Given a delivery-team skill is invoked through the pipeline
When the PreToolUse Skill event fires
Then `delivery-team/hooks/telemetry.py` writes exactly one JSONL row to `.delivery/telemetry/skill-loads.jsonl`

```bash
tail -1 .delivery/telemetry/skill-loads.jsonl
# MUST: non-empty JSON line after a skill invocation
```

**Scenario 2 — All 7 required fields present**
Given ≥1 row exists in `.delivery/telemetry/skill-loads.jsonl`
When the schema validator runs
Then every row contains `skill`, `model`, `prefix_hash`, `input_tokens`, `cache_read_tokens`, `cache_write_tokens`, `timestamp`, `session_id`

```bash
python3 -c "import json; rows=[json.loads(l) for l in open('.delivery/telemetry/skill-loads.jsonl')]; req={'skill','model','prefix_hash','input_tokens','cache_read_tokens','cache_write_tokens','timestamp','session_id'}; [req-r.keys() and (_ for _ in ()).throw(KeyError(req-r.keys())) for r in rows]; print('PASS', len(rows), 'rows')"
# MUST: print PASS; MUST NOT raise
```

**Scenario 3 — Hook overhead < 50 ms per call**
Given `telemetry.py` supports `--dry-run`
When 10 dry-run invocations are timed
Then the mean delta is < 50 ms

```bash
# Time 10 --dry-run calls; compute mean delta; MUST be < 50 ms
python3 -c "import time,subprocess,statistics; s=[time.perf_counter() for _ in range(10) if not subprocess.run(['python3','delivery-team/hooks/telemetry.py','--dry-run'],check=True)]; print(f'irrelevant')"
```

**Scenario 4 — prefix_hash computed from SKILL.md on disk (ADR-tk0e-001 option a)**
Given a skill invocation event
When the hook computes `prefix_hash`
Then it is the sha256 (first 8 chars) of the SKILL.md file contents on disk, NOT from runtime context

**Scenario 5 — Schema documented as version 1**
```bash
grep 'version: 1' delivery-team/references/telemetry-schema.md
# MUST: at least one match
```

**Scenario 6 — Report script produces non-empty mean-tokens table**
```bash
python3 delivery-team/hooks/telemetry_report.py
# MUST: non-empty mean-tokens table; MUST NOT raise or print nothing
```

**Scenario 7 — No LLM import in hook**
```bash
grep -n 'anthropic\|openai\|litellm' delivery-team/hooks/telemetry.py
# MUST: no matches (grep exits 1 = PASS)
```

**Scenario 8 — No phantom hook paths**
```bash
python3 -c "import json,os; h=json.load(open('delivery-team/hooks/hooks.json')); bad=[e['script'] for e in h.get('hooks',[]) if not os.path.exists(e['script'])]; assert not bad, bad; print('PASS')"
# MUST: print PASS
```

### Definition of Ready
PRD ACs accepted; ADR-tk0e-001 accepted. DONE.

### INVEST Validation

| Criterion | Status | Notes |
|-----------|--------|-------|
| Independent | PASS | No dependency on W0-2 at implementation level |
| Negotiable | PASS | Schema fields are binding (ADR) but hook internals are negotiable |
| Valuable | PASS | Without this, all Wave 1+ token savings are unverifiable |
| Estimable | PASS | 2 SP (S); pure Python hook + report script + schema doc |
| Small | PASS | Half-day scope; 4 artifacts, all hook-layer |
| Testable | PASS | 8 runnable ACs, each with a concrete bash command |

### Notes / Constraints
- MUST be built via `plugin-dev:hook-development` skill (binding per ADR-tk0e-001)
- JSONL schema v1; version field MUST appear in `telemetry-schema.md`
- Pure Python, no external dependencies, no Anthropic SDK import
- `prefix_hash` = sha256 of SKILL.md on disk (first 8 chars); NOT from context

---

## Story W0-2: SKILL.md line-budget CI gate

**As a** delivery-team plugin maintainer
**I want** a CI workflow that fails PRs growing SKILL.md beyond their tier budget
**So that** Wave 1+ extractions cannot regress over time

**Story Points**: 3 (S-M — half-to-one day, includes tier frontmatter rollout to 13 files)
**Priority**: Critical (foundation for all subsequent waves)

### Acceptance Criteria

**Scenario 1 — CI fails synthetic over-budget PR**
Given a SKILL.md with `tier: C` that exceeds 200 lines
When `check_skill_budgets.py` runs against it
Then exit code is 1 and output names the file and overage

```bash
python3 -c "open('/tmp/ob.md','w').write('---\ntier: C\n---\n'+'# x\n'*201)"
python3 scripts/check_skill_budgets.py --check /tmp/ob.md --tier C; echo "Exit: $?"
# MUST: exit 1; MUST print budget violation naming file and overage
```

**Scenario 2 — CI passes PR that reduces SKILL.md lines**
Given a PR that reduces any delivery-team SKILL.md line count
When the CI budget check runs
Then exit code is 0 (no violation triggered)

**Scenario 3 — Budget-Exception token allows merge with warning summary**
Given a PR body containing `Budget-Exception: <ADR-link>`
When `check_skill_budgets.py` evaluates that PR
Then the over-budget condition is bypassed (exit 0) and a warning summary is emitted

```bash
grep -n 'Budget-Exception' scripts/check_skill_budgets.py
# MUST: at least one match
```

**Scenario 4 — Missing tier: frontmatter fails with hint**
Given a SKILL.md with no `tier:` frontmatter field
When `check_skill_budgets.py` processes it
Then exit code is 1 and output includes a hint to add `tier:` frontmatter

**Scenario 5 — Permissive-language sub-check is warn-only (exit 0)**
Given any delivery-team SKILL.md
When `--warn-permissive` is passed
Then exit code is 0; flagged hits are visible in job summary; fenced code blocks, blockquotes, and tables are exempt zones

```bash
python3 scripts/check_skill_budgets.py --warn-permissive delivery-team/skills/delivery-flow/SKILL.md; echo "Exit: $?"
# MUST: exit 0; warnings to stderr are acceptable; MUST NOT exit 1
```

**Scenario 6 — All 13 SKILL.md files have tier: frontmatter**
```bash
find delivery-team -name 'SKILL.md' | wc -l   # MUST: 13
find delivery-team -name 'SKILL.md' -exec grep -qL "^tier:" {} \; -print  # MUST: no output
grep "^tier:" delivery-team/architect/paradigms/ddd/SKILL.md       # MUST: tier: C
grep "^tier:" delivery-team/architect/paradigms/volatility/SKILL.md # MUST: tier: C
```

**Scenario 7 — 6 known-debt skills logged in CI output**
```bash
python3 scripts/check_skill_budgets.py --known-debt-report
# MUST: 6 lines matching: KNOWN-DEBT: <skill>/SKILL.md <current>/<budget> lines — target wave: W<N>
# Expected: delivery-flow(1089/500), product-delivery(688/300), architect(670/300),
#           presentation(543/300), ui(493/300), developer(493/300)
```

**Scenario 8 — Tier budget constants are exactly A≤500 / B≤300 / C≤200**
```bash
grep -n 'TIER_LIMITS\|500\|300\|200' scripts/check_skill_budgets.py
# MUST: show exactly these three values
```

### Definition of Ready
PRD, ADR-tk0e-002, and ADR-tk0e-003 accepted. DONE.

### INVEST Validation

| Criterion | Status | Notes |
|-----------|--------|-------|
| Independent | PASS | Does not depend on W0-1 telemetry hook at implementation level |
| Negotiable | PASS | Tier budget values and known-debt list are binding (ADR); CI workflow internals negotiable |
| Valuable | PASS | Without this gate, all Wave 1+ reductions will regress (governance expert finding) |
| Estimable | PASS | 3 SP (S-M); 2 scripts + 1 workflow + 13 frontmatter additions |
| Small | PASS | Half-to-one day; scope is additive only (no SKILL.md content changes) |
| Testable | PASS | 8 runnable ACs; synthetic over-budget file provides deterministic CI proof |

### Notes / Constraints
- MUST use `plugin-dev:plugin-structure` + `plugin-dev:skill-development` skills (binding per ADRs)
- MUST pass `plugin-dev:skill-reviewer` + `plugin-dev:plugin-validator` before merge
- 6 over-budget files hard-coded as known-debt in script per ADR-tk0e-003 (no ADR required for them)
- `tier:` field added to all 13 SKILL.md frontmatter — no other content modified (Wave 0 MUST NOT reduce line counts)
- Tier defaults: A = `delivery-flow` (orchestrator), B = 9 role multiplexers, C = leaf + paradigm sub-skills

---
title: "Wave 0 UAT Test Cases"
stage: 07-uat
author: Legolas (quality skill)
created: 2026-05-03
version: 1.0
---

# Wave 0 UAT Test Cases

## UAT-TC-1 — Telemetry runs invisibly

**Given** W0-1 and W0-2 merged; `.delivery/telemetry/` writable.

**When**
```bash
BEFORE=$(wc -l < .delivery/telemetry/skill-loads.jsonl 2>/dev/null || echo 0)
OUT=$(echo '{"tool_name":"Skill","tool_input":{"skill_name":"delivery-team:developer"}}' \
  | python3 delivery-team/hooks/telemetry.py); echo "Exit: $?"; echo "Stdout: '${OUT}'"
AFTER=$(wc -l < .delivery/telemetry/skill-loads.jsonl)
echo "Row delta: $((AFTER - BEFORE))"
tail -1 .delivery/telemetry/skill-loads.jsonl | python3 -c \
  "import sys,json; r=json.loads(sys.stdin.read()); assert r['skill']=='delivery-team:developer'; print('PASS')"
```

**Then** `Exit: 0`; `Stdout: ''`; `Row delta: 1`; last assertion prints `PASS`.

---

## UAT-TC-2 — CI gate fires correctly on over-budget PR

**Given** draft PR branch with 50 prose lines added to
`delivery-team/skills/delivery-flow/SKILL.md`; NO `Budget-Exception` in PR body.

**When**
```bash
python3 scripts/check_skill_budgets.py --check delivery-team/skills/delivery-flow/SKILL.md
echo "Exit: $?"
```

**Then** Exit `1`; output matches `BUDGET VIOLATION.*delivery-flow.*[0-9]+/500`;
pushed PR: `skill-line-budget` check red; annotation names file, tier A, and overage delta.

---

## UAT-TC-3 — Budget-Exception token bypasses gate with warning

**Given** same over-budget branch; PR body includes `Budget-Exception: known-debt-tk0e`.

**When**
```bash
PR_BODY="Budget-Exception: known-debt-tk0e" \
  python3 scripts/check_skill_budgets.py --check delivery-team/skills/delivery-flow/SKILL.md
echo "Exit: $?"
```

**Then** Exit `0`; output contains `EXCEPTION ACKNOWLEDGED`;
pushed PR: `skill-line-budget` check green; warning still appears in job summary
(silent pass is a UAT failure).

---

## UAT-TC-4 — Permissive-language scan warns but does not block

**Given** draft PR branch adding a prose sentence with `should` to
`delivery-team/skills/alias-creator/SKILL.md`.

**When**
```bash
python3 scripts/check_skill_budgets.py \
  --warn-permissive delivery-team/skills/alias-creator/SKILL.md
echo "Exit: $?"
```

**Then** Exit `0`; stderr matches `PERMISSIVE-LANGUAGE.*should`;
no `BUDGET VIOLATION` in output; pushed PR: `skill-line-budget` check green.

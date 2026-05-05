---
title: "Wave 1 UAT Test Cases"
stage: 07-uat
author: Legolas (quality skill)
created: 2026-05-03
version: 1.0
---

# Wave 1 UAT Test Cases

CWD: `/var/home/meconnelly/Documents/GitHub/Claude-Plugins`

## TC-01 — delivery-flow structural integrity
**Given** Story 1 merged. **When** contributor audits SKILL.md. **Then**:
```bash
wc -l delivery-team/skills/delivery-flow/SKILL.md          # expect 999
head -15 delivery-team/skills/delivery-flow/SKILL.md | grep -E "^model:|^extended_thinking:"  # both present
grep -c "^## Phase"    delivery-team/skills/delivery-flow/SKILL.md  # expect 5
grep -c "^## Volatile" delivery-team/skills/delivery-flow/SKILL.md  # expect 1
```
**Pass**: all 4 return expected values; exit 0.

## TC-02 — stages.yml presence + schema integrity
**Given** Story 1 extracted stages. **When** checking artefacts. **Then**:
```bash
python3 -c "from pathlib import Path; s=Path('delivery-team/skills/delivery-flow/references/stages.yml').stat().st_size; assert s>100; print(s)"
# expect 7394; exit 0
python3 -c "import json; json.load(open('delivery-team/skills/delivery-flow/references/stages-schema.json')); print('OK')"
# expect OK; exit 0
python3 -c "import json; d=json.load(open('delivery-team/skills/delivery-flow/references/stages-schema.json')); assert '\$schema' in d or 'title' in d; print('schema-id present')"
```
**Pass**: all 3 exit 0 with expected output.

## TC-03 — CI budget gate clean post-trim
**Given** Story 2 trimmed alias-creator and removed known-debt. **When** running gate. **Then**:
```bash
python3 scripts/check_skill_budgets.py                          # expect PASSED; exit 0
python3 scripts/check_skill_budgets.py 2>&1 | grep -i "alias-creator"  # expect empty
python3 -c "import json; d=json.load(open('governance/skill-budgets.json')); assert not any('alias-creator' in str(e) for e in d.get('known_debt',[])); print('clean')"
```
**Pass**: exit 0; grep empty; registry prints "clean".

## TC-04 — allowed-tools + haiku coverage
**Given** Story 2 rolled out frontmatter. **When** auditing coverage. **Then**:
```bash
grep -rl "^allowed-tools:" delivery-team/skills/ | wc -l     # expect >= 13
grep "^phase_1_detector_model:" delivery-team/skills/quality/SKILL.md  # expect haiku
for f in product-delivery architect quality operations ui; do grep -l "phase_1_detector_model: haiku" delivery-team/skills/$f/SKILL.md; done | wc -l  # expect 5
```
**Pass**: count ≥ 13; quality line present; router count = 5.

## TC-05 — challenger hook warn-only; no LLM calls
**Given** Story 3 extended `audit_agent_prompt.py`. **When** mismatch prompt piped. **Then**:
```bash
echo '{"tool_name":"Agent","tool_input":{"prompt":"You are a Challenger. primary model: claude-opus-4-5  model: claude-haiku-3-7  Critique this."}}' \
  | python3 delivery-team/hooks/audit_agent_prompt.py; echo "exit:$?"
# expect exit:0; stderr contains [CHALLENGER-TIER-WARN]
grep -E "anthropic|openai|litellm" delivery-team/hooks/audit_agent_prompt.py  # expect empty
```
**Pass**: exit 0 with warning; grep empty.

## TC-06 — cache-prefix hash byte-stable
**Given** Story 1 froze sha256(bytes 0..2048). **When** recomputing. **Then**:
```bash
python3 -c "
import hashlib, pathlib
stored = open('governance/cache-prefix-hash.txt').read().strip()
live   = hashlib.sha256(pathlib.Path('delivery-team/skills/delivery-flow/SKILL.md').read_bytes()[:2048]).hexdigest()
assert stored == live, f'MISMATCH stored={stored} live={live}'
print('HASH MATCH OK')
"  # expect HASH MATCH OK; exit 0
```
**Pass**: prints "HASH MATCH OK"; exit 0.

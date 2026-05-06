---
title: "Wave 2 UAT Test Cases"
stage: 07-uat
author: Legolas (quality skill)
created: 2026-05-03
version: 2.0
---

# Wave 2 UAT Test Cases

CWD: `/var/home/meconnelly/Documents/GitHub/Claude-Plugins`

## TC-01 — delivery-flow Tier-A compliance + doctrine pointer
**Given** Story 1 merged (delivery-flow trimmed to 497 lines). **When** contributor audits. **Then**:
```bash
wc -l delivery-team/skills/delivery-flow/SKILL.md          # expect 497
grep -c "orchestrator-doctrine.md" delivery-team/skills/delivery-flow/SKILL.md  # expect >= 1
grep -c "^## Volatile" delivery-team/skills/delivery-flow/SKILL.md              # expect 1
```
**Pass**: line count 497; doctrine ref >= 1; Volatile marker == 1.

## TC-02 — architect output-contracts routing table complete
**Given** Story 2 split 5 contract files. **When** contributor audits routing. **Then**:
```bash
find delivery-team/skills/architect/references/output-contracts -name '*.md' | wc -l  # expect 5
for f in design adr game review evaluation; do grep -l "$f.md" delivery-team/skills/architect/SKILL.md; done | wc -l  # expect 5
wc -l delivery-team/skills/architect/SKILL.md  # expect <= 500
```
**Pass**: file count 5; all 5 filenames present in routing table; line count <= 500.

## TC-03 — developer coding-standards dispatch isolated; other tasks intact
**Given** Story 3 extracted coding-standards. **When** contributor audits SKILL.md. **Then**:
```bash
python3 -c "from pathlib import Path; p=Path('delivery-team/skills/developer/references/agent-prompts/coding-standards.md'); assert p.exists(); print('EXISTS')"
grep "agent-prompts/coding-standards.md" delivery-team/skills/developer/SKILL.md  # expect match
wc -l delivery-team/skills/developer/SKILL.md                                     # expect <= 300
grep -cE "write|fix|refactor|review|test|explain" delivery-team/skills/developer/SKILL.md  # expect >= 6
```
**Pass**: file exists; grep match; line count <= 300; 6+ task keywords present.

## TC-04 — product-delivery 12-pattern routing table
**Given** Story 4 split 12 patterns. **When** contributor audits SKILL.md. **Then**:
```bash
find delivery-team/skills/product-delivery/references/patterns -name '*.md' | wc -l  # expect 12
wc -l delivery-team/skills/product-delivery/SKILL.md                                  # expect 299
grep -c "references/patterns/" delivery-team/skills/product-delivery/SKILL.md         # expect >= 12
```
**Pass**: file count 12; line count 299; routing refs >= 12.

## TC-05 — governance registry 7 known_debt entries; CI gate exits 0
**Given** Story 5 re-baselined skill-budgets.json. **When** CI gate runs. **Then**:
```bash
python3 -c "
import json
d = json.load(open('governance/skill-budgets.json'))
debt = d['known_debt']
assert len(debt) == 7, f'expected 7 got {len(debt)}'
arch = next(e for e in debt if 'architect' in e['path'])
assert arch['target_wave'] == 3, 'architect not wave 3'
print(f'DEBT_COUNT={len(debt)} ARCH_WAVE={arch[\"target_wave\"]} OK')
"
python3 scripts/check_skill_budgets.py  # expect PASSED; exit 0
```
**Pass**: script prints DEBT_COUNT=7; gate exits 0.

## TC-06 — cache-prefix hash stable after 497-line trim
**Given** governance/cache-prefix-hash.txt frozen in Wave 1 and SKILL.md trimmed in Wave 2. **When** recomputing. **Then**:
```bash
python3 -c "
import hashlib, pathlib
stored = open('governance/cache-prefix-hash.txt').read().strip().split()[0]
live   = hashlib.sha256(pathlib.Path('delivery-team/skills/delivery-flow/SKILL.md').read_bytes()[:2048]).hexdigest()
assert stored == live, f'MISMATCH stored={stored} live={live}'
print('HASH MATCH OK')
"  # expect: HASH MATCH OK; exit 0
wc -l governance/cache-prefix-hash.txt  # expect 1 (single line, old hash absent)
```
**Pass**: prints "HASH MATCH OK"; exit 0; file has 1 line.

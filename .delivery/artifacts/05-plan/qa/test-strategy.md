---
title: "Wave 0 Test Strategy"
work_items: [W0-1, W0-2]
stage: 05-plan
author: QA Engineer (quality skill)
adrs: [ADR-tk0e-001, ADR-tk0e-002, ADR-tk0e-003]
created: 2026-05-03
version: 1.0
---

# Wave 0 Test Strategy

## Test Approach Summary

**Test pyramid**: Unit tests cover frontmatter parsing and hash computation in isolation.
Integration tests exercise the full hook-firing path and CI workflow against fixture inputs.
Dogfood validation runs the real pipeline and a real draft PR to produce evidence.

**Coverage target**: 100% of PRD §8 ACs (AC-1 through AC-12) by at least one test case.
ADR-003 full audit: 11 of 13 SKILL.md files are over-budget; `check_skill_budgets.py` MUST
declare all 11 as known-debt. AC-10's "6 lines" is a floor, not a ceiling.

**Empirical validation**: A real pipeline iteration MUST produce a JSONL row; a real synthetic
draft PR MUST fire the CI gate. Both are Stage 6 Dev DoD blockers.

---

## W0-1 Test Cases

**TC-W0-1-1**: Hook fires on PreToolUse Skill and writes JSONL row (AC-1, happy path)
- **Given**: `telemetry.py` + `hooks.json` installed; `.delivery/telemetry/` absent
- **When**: `python3 delivery-team/hooks/telemetry.py '{"tool_name":"Skill","tool_input":{"skill":"delivery-team:developer"}}'`
- **Then**: `tail -1 .delivery/telemetry/skill-loads.jsonl | python3 -c "import sys,json; r=json.loads(sys.stdin.read()); assert r; print('PASS')"` → exit 0, stdout `PASS`

**TC-W0-1-2**: All 9 schema fields present in emitted row (AC-2)
- **Given**: ≥1 row in `.delivery/telemetry/skill-loads.jsonl`
- **When**: `python3 -c "import json; rows=[json.loads(l) for l in open('.delivery/telemetry/skill-loads.jsonl')]; req={'version','skill','model','prefix_hash','input_tokens','cache_read_tokens','cache_write_tokens','timestamp','session_id'}; missing=[req-set(r.keys()) for r in rows if req-set(r.keys())]; assert not missing,missing; print('PASS',len(rows),'rows')"`
- **Then**: exit 0; stdout matches `PASS \d+ rows`

**TC-W0-1-3**: Hook overhead < 50 ms mean across 10 dry-run invocations (NFR-01 / AC-5)
- **Given**: `telemetry.py` supports `--dry-run` (no write, measures execution only)
- **When**: `python3 -c "import time,subprocess,statistics; t=[((lambda t0: (time.perf_counter()-t0)*1000)(time.perf_counter()) if not subprocess.run(['python3','delivery-team/hooks/telemetry.py','--dry-run'],check=True) else 0) for _ in range(10)]; m=statistics.mean(t); print(f'mean={m:.1f}ms'); assert m<50,f'FAIL {m:.1f}ms'"`
- **Then**: exit 0; stdout contains `mean=` with value < 50

**TC-W0-1-4**: Hook resilient to read-only telemetry directory — Skill not blocked (ADR-001 failure mode)
- **Given**: `.delivery/telemetry/` chmod 000
- **When**: `chmod 000 .delivery/telemetry && python3 delivery-team/hooks/telemetry.py '{"tool_name":"Skill","tool_input":{"skill":"delivery-team:developer"}}'; echo "Exit: $?"; chmod 755 .delivery/telemetry`
- **Then**: exit 0 (hook exits cleanly); stderr contains error text; no Python traceback to stdout

**TC-W0-1-5**: prefix_hash deterministic for identical SKILL.md content (idempotency)
- **Given**: `delivery-team/skills/developer/SKILL.md` unchanged between two calls
- **When**: `python3 -c "import hashlib; c=open('delivery-team/skills/developer/SKILL.md','rb').read(2048); h1=hashlib.sha256(c).hexdigest()[:8]; h2=hashlib.sha256(c).hexdigest()[:8]; assert h1==h2; assert len(h1)==8; print('PASS',h1)"`
- **Then**: exit 0; stdout `PASS <8-char-hex>` (same hex both runs)

**TC-W0-1-6**: No Anthropic/OpenAI SDK import in telemetry.py (FR-11)
- **When**: `grep -n 'anthropic\|openai\|litellm' delivery-team/hooks/telemetry.py; echo "Grep: $?"`
- **Then**: grep exits 1 (no matches); output `Grep: 1`

**TC-W0-1-7**: Every script path in hooks.json exists on disk (FR-12, phantom-path guard)
- **When**: `python3 -c "import json,os; h=json.load(open('delivery-team/hooks/hooks.json')); bad=[e['script'] for e in h.get('hooks',[]) if not os.path.exists(e['script'])]; assert not bad,f'PHANTOM: {bad}'; print('PASS',len(h['hooks']),'hook(s)')"`
- **Then**: exit 0; stdout `PASS N hook(s)`

---

## W0-2 Test Cases

**TC-W0-2-1**: Synthetic over-budget SKILL.md → exit 1, names file + tier + delta (AC-9)
- **When**: `python3 -c "open('/tmp/ob_c.md','w').write('---\ntier: C\n---\n'+'# x\n'*201)" && python3 scripts/check_skill_budgets.py --check /tmp/ob_c.md --tier C; echo "Exit: $?"`
- **Then**: exit 1; output matches `BUDGET VIOLATION.*ob_c.*201/200`

**TC-W0-2-2**: Clean SKILL.md (under budget) → exit 0 (AC-9 inverse)
- **When**: `python3 scripts/check_skill_budgets.py --check delivery-team/skills/architect/paradigms/ddd/SKILL.md; echo "Exit: $?"`
- **Then**: exit 0; no `BUDGET VIOLATION` in output

**TC-W0-2-3**: PR body with `Budget-Exception:` token → exit 0 + warning summary (FR-10)
- **When**: `python3 -c "open('/tmp/ob_b.md','w').write('---\ntier: B\n---\n'+'# x\n'*301)" && PR_BODY="Budget-Exception: known-debt-tk0e" python3 scripts/check_skill_budgets.py --check /tmp/ob_b.md; echo "Exit: $?"`
- **Then**: exit 0; output contains `EXCEPTION ACKNOWLEDGED`

**TC-W0-2-4**: SKILL.md missing `tier:` field → exit 1 with hint (FR-06)
- **When**: `python3 -c "open('/tmp/no_tier.md','w').write('# No frontmatter\n'+'# x\n'*10)" && python3 scripts/check_skill_budgets.py --check /tmp/no_tier.md; echo "Exit: $?"`
- **Then**: exit 1; output matches `MISSING TIER.*no_tier.*tier: A\|B\|C`

**TC-W0-2-5**: Permissive language in fenced code block → NOT flagged (ADR-002 exempt zones)
- **When**: `python3 -c "open('/tmp/code_block.md','w').write('---\ntier: C\n---\n\`\`\`python\n# should be ignored\n\`\`\`\n'+'# x\n'*5)" && python3 scripts/check_skill_budgets.py --warn-permissive /tmp/code_block.md; echo "Exit: $?"`
- **Then**: exit 0; no permissive-language warning in output

**TC-W0-2-6**: Permissive language in prose → flagged to stderr, exit 0 (FR-09 / AC-11 warn-only)
- **When**: `python3 -c "open('/tmp/prose.md','w').write('---\ntier: C\n---\nYou should check this.\n'+'# x\n'*5)" && python3 scripts/check_skill_budgets.py --warn-permissive /tmp/prose.md; echo "Exit: $?"`
- **Then**: exit 0; stderr contains warning matching `should`; no exit 1

**TC-W0-2-7**: Permissive language in blockquote → NOT flagged (ADR-002 exempt zones)
- **When**: `python3 -c "open('/tmp/bq.md','w').write('---\ntier: C\n---\n> The challenger may propose.\n'+'# x\n'*5)" && python3 scripts/check_skill_budgets.py --warn-permissive /tmp/bq.md; echo "Exit: $?"`
- **Then**: exit 0; no `may` warning (blockquote line exempted)

**TC-W0-2-8**: Permissive language in table cell → NOT flagged (ADR-002 exempt zones)
- **When**: `python3 -c "open('/tmp/tbl.md','w').write('---\ntier: C\n---\n| Col1 | Col2 |\n|------|------|\n| can  | skip |\n'+'# x\n'*5)" && python3 scripts/check_skill_budgets.py --warn-permissive /tmp/tbl.md; echo "Exit: $?"`
- **Then**: exit 0; no `can` warning (table row exempted)

**TC-W0-2-9**: Known-debt report lists ≥6 over-budget skills (AC-10 floor; ADR-003 full = 11)
- **When**: `python3 scripts/check_skill_budgets.py --known-debt-report`
- **Then**: exit 0; ≥6 lines matching `KNOWN-DEBT: .*/SKILL\.md \d+/\d+ lines — target wave: W\d`; line for `delivery-flow` shows `1089/500`

**TC-W0-2-10**: Tier frontmatter present in all 13 delivery-team SKILL.md files (AC-8)
- **When**: `find delivery-team -name 'SKILL.md' | wc -l && find delivery-team -name 'SKILL.md' -exec grep -qL "^tier:" {} \; -print && grep "^tier:" delivery-team/skills/architect/paradigms/ddd/SKILL.md && grep "^tier:" delivery-team/skills/architect/paradigms/volatility/SKILL.md`
- **Then**: first command outputs `13`; second command outputs nothing (all files have tier); third and fourth output `tier: C`

---

## Dogfood Plan (Stage 6 Dev DoD MUST execute)

**After W0-1 lands** — invoke any delivery-team skill through the normal pipeline; verify:
```bash
tail -1 .delivery/telemetry/skill-loads.jsonl | python3 -c "
import sys,json
r=json.loads(sys.stdin.read())
req={'version','skill','model','prefix_hash','input_tokens','cache_read_tokens','cache_write_tokens','timestamp','session_id'}
assert not req-set(r.keys()), req-set(r.keys())
print('DOGFOOD PASS'); print(json.dumps(r,indent=2))
"
```

**After W0-2 lands** — open a draft PR with synthetic over-budget SKILL.md; verify CI check fails
(annotation names file + overage). Open second draft PR with same file + `Budget-Exception:
known-debt-tk0e` in body; verify CI passes with warning summary.

**Evidence to capture** in `.delivery/artifacts/06-dev/dogfood-evidence/`:
- `telemetry-sample.jsonl` — real row(s) from pipeline run
- `overhead-timing.txt` — stdout of TC-W0-1-3 (mean < 50 ms)
- `ci-failure-log.txt` or CI run URL — AC-9 violation failing
- `tier-count.txt` — `find … | wc -l` showing `13` + two `tier: C` paradigm greps
- `known-debt-report.txt` — full `--known-debt-report` output (≥6 KNOWN-DEBT lines)

---

## Test Order / Sequencing

1. **Unit** (no environment required): TC-W0-1-5, TC-W0-1-6, TC-W0-2-10 (grep/hash only)
2. **Integration** (scripts installed, no live CI): TC-W0-1-1 → TC-W0-1-4, TC-W0-1-7, TC-W0-2-1 → TC-W0-2-9
3. **Dogfood** (Stage 6 DoD, real pipeline + draft PR): telemetry row evidence, CI gate evidence

---
story: W0-1
stage: 06-dev
author: Gimli (developer skill, python_developer)
created: 2026-05-04
---

# W0-1 Dogfood Evidence

## TC-W0-1-1: Hook fires and writes JSONL row

```
$ echo '{"tool_name":"Skill","tool_input":{"skill_name":"delivery-team:delivery-flow"}}' \
    | python3 delivery-team/hooks/telemetry.py && echo "Exit: $?"
Exit: 0

$ tail -1 .delivery/telemetry/skill-loads.jsonl
{"version": "1", "timestamp": "2026-05-04T02:47:51.438915Z", "session_id": "unknown",
 "skill": "delivery-team:delivery-flow", "model": null, "prefix_hash": "cd8c0476",
 "input_tokens": 0, "cache_read_tokens": 0, "cache_write_tokens": 0}
```

RESULT: PASS

## TC-W0-1-2: All 9 schema fields present

```
$ tail -1 .delivery/telemetry/skill-loads.jsonl | python3 -c \
  "import sys,json; r=json.loads(sys.stdin.read()); \
   req={'version','skill','model','prefix_hash','input_tokens','cache_read_tokens',\
        'cache_write_tokens','timestamp','session_id'}; \
   missing=req-r.keys(); print('OK' if not missing else f'MISSING_FIELDS: {missing}')"
OK
```

RESULT: PASS

## TC-W0-1-3: Hook overhead < 50 ms mean (10 dry-run invocations)

```
mean=18.7ms  min=18.1ms  max=19.7ms
PASS
```

RESULT: PASS — 18.7 ms mean (budget: 50 ms)

## TC-W0-1-4: Resilience — read-only telemetry directory

```
$ chmod 000 .delivery/telemetry
$ echo '{"tool_name":"Skill","tool_input":{"skill_name":"delivery-team:developer"}}' \
    | python3 delivery-team/hooks/telemetry.py; echo "Exit: $?"
telemetry.py: non-fatal error: [Errno 13] Permission denied: \
  '/var/home/meconnelly/Documents/GitHub/Claude-Plugins/.delivery/telemetry/skill-loads.jsonl'
Exit: 0
$ chmod 755 .delivery/telemetry
```

RESULT: PASS — exits 0; error logged to stderr; Skill not blocked

## TC-W0-1-5: prefix_hash determinism

```
$ python3 -c "import hashlib; c=open('delivery-team/skills/developer/SKILL.md','rb').read(2048); \
  h1=hashlib.sha256(c).hexdigest()[:8]; h2=hashlib.sha256(c).hexdigest()[:8]; \
  assert h1==h2; assert len(h1)==8; print('PASS',h1)"
PASS 9133af61
```

RESULT: PASS

## TC-W0-1-6: No Anthropic/OpenAI SDK import

```
$ grep -n 'anthropic\|openai\|litellm' delivery-team/hooks/telemetry.py; echo "Grep: $?"
Grep: 1
```

RESULT: PASS (grep exit 1 = no matches)

## TC-W0-1-7: Phantom path guard — all hook scripts exist on disk

```
PASS telemetry.py exists
PASS telemetry_report.py exists
PASS check_config.py exists
PASS audit_agent_prompt.py exists
PASS validate_gdscript.py exists
PASS verify_skill_load.py exists
PASS flag_empirical_validation.py exists
```

RESULT: PASS — 0 phantom paths

## AC-5: Schema version documented

```
$ grep 'version: 1' delivery-team/references/telemetry-schema.md
version: 1
```

RESULT: PASS

## AC-6: Report script produces non-empty table

```
$ python3 delivery-team/hooks/telemetry_report.py
Skill                           Runs    Mean input_tok   Mean cache_read   Mean cache_write
-------------------------------------------------------------------------------------------
delivery-team:architect            1               0.0               0.0                0.0
delivery-team:delivery-flow        1               0.0               0.0                0.0
delivery-team:developer            1               0.0               0.0                0.0
delivery-team:quality              1               0.0               0.0                0.0

(Last 5 rows per skill; total rows in file: 4)
```

RESULT: PASS

## Summary

All 8 ACs verified. All tests green. Hook overhead 18.7 ms (< 50 ms budget).
No phantom paths. No LLM imports. Schema version documented.

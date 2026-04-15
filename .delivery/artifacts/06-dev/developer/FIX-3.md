# FIX-3 — `--skip-declarations` flag for check_dod_constraints.py

**Bug:** b2c7 UAT TC-12 self-check false positive. When the artifact IS the
constraints.yml, grep matches tokens listed in `forbidden_vocabulary:` as
content in the declaration itself.

## Files modified

- `delivery-team/skills/delivery-flow/scripts/check_dod_constraints.py`
  - Converted argv parsing to `argparse`.
  - Added `--skip-declarations` flag (default: False).
  - Added `_strip_forbidden_vocab_block(lines)`: when flag is set, blanks the
    line starting with `forbidden_vocabulary:` at column 0 and every following
    indented/blank line until a non-indented line or EOF. Blanks (not deletes)
    so 1-based line numbers remain stable for other surviving hits.
  - Updated module docstring to document the flag.
  - Updated argparse `--help` text.

## Files added

- `delivery-team/skills/delivery-flow/references/fixtures/dod-self-check.yml`
  — constraints.yml with populated `forbidden_vocabulary` (lambda, ecr, sqs,
  dynamodb, kinesis, s3, ec2) for self-check regression testing.

## Backwards compat

Flag defaults to `False`; omitting it preserves byte-identical grep semantics.
Confirmed by Test A (contaminated artifact still FAILs exactly as before).

## Tests (exit codes)

| # | Cmd | Expected | Actual |
|---|-----|----------|--------|
| A | `check_dod_constraints.py constraints-valid.yml dod-artifact-contaminated.md` | 1 | **1** |
| B | `check_dod_constraints.py constraints-valid.yml constraints-valid.yml` | 1 | **1** |
| C | `check_dod_constraints.py --skip-declarations constraints-valid.yml constraints-valid.yml` | 0 | **0** |

Test A proves backwards compat (`precious` still caught in md artifact).
Test B proves the false positive is still reproducible without the flag.
Test C proves the flag suppresses the self-check false positive.

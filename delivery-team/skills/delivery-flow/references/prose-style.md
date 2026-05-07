# PROSE STYLE Block (verbatim, ADR-tk3-001 Element 2)

This file holds the verbatim PROSE STYLE block injected into agent dispatch prompts when `config.prose_style == caveman-lite` (default). When `config.prose_style == standard`, the block is omitted entirely from the dispatch (no placeholder line, no empty section).

The orchestrator reads `prose_style` at Phase 0 (SKILL.md L73-74) and applies the block uniformly at Phase 4 Step 4 (Primary), Step 5 (Supporting), and Step 7 (DoD Validator) dispatches per `references/pipeline-stages.md` template slots. Per-role overrides are out of scope for v1 (deferred to BACKLOG-103+ pending Wave 4 telemetry).

## Verbatim block (insertion target: between `--- ALIAS ---` and `--- OUTPUT ---`)

Insertion delimiter: `--- PROSE STYLE ---`

```
PROSE STYLE: caveman-lite for narrative-framing prose ONLY (the prose between signal block and response end, plus signal block SUMMARY field). Drop articles/filler/pleasantries/hedging; fragments OK; short synonyms; preserve technical terms exact and code/error-string verbatim. Artifact body uses standard prose. Auto-clarity exemptions apply: standard prose for security warnings, irreversible-op confirmations, multi-step sequences, user clarifications.
```

## Auto-clarity exemptions (in-prompt directive enforcement)

The four exempt contexts named in the block — security warnings, irreversible-op confirmations, multi-step sequences, user clarifications — revert to standard prose even when `caveman-lite` is active. The agent itself is the detector (per ADR-tk3-001 Element 3); no orchestrator-side classifier is required.

## DoD validator verdict-prose treatment (ADR-tk3-001 Element 4)

When the DoD Validator Dispatch Template injects the PROSE STYLE block, the validator applies caveman-lite to verdict prose ONLY:

| Section | Style | Rationale |
|---|---|---|
| `STATUS:` line (DONE / NOT_DONE / CODE_COMPLETE) | verbatim | downstream parsers grep for these literal tokens |
| `ARTIFACT:` line (path) | verbatim | file path; not prose |
| `SUMMARY:` (≤200 char) | caveman-lite | already terse; lite tightens further |
| `FINDINGS:` bullet list (each: file/line/criterion) | standard prose preserved | findings must remain actionable |
| Gate-result tables | verbatim | tabular structure is the compression |
| Free-form verdict prose (≤3 sentences around the table) | caveman-lite | AC-2 ≥25% reduction surface |

See `references/quality-gates.md` "DoD Validator Prompt Template" for the role-specific contract line.

## References

- ADR-tk3-001 (`.delivery/artifacts/04-architect/adrs/ADR-tk3-001-prose-style-config.md`)
- BACKLOG-102 (`.delivery/backlog/BACKLOG-102-caveman-prose-discipline.md`)
- `references/config-schema.md` v2.9 (top-level `prose_style` key)
- `references/pipeline-stages.md` (3 dispatch templates with PROSE STYLE slots)
- `references/quality-gates.md` (DoD Validator Prompt Template verdict-prose line)

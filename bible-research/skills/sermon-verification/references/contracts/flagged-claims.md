# Contract: Flagged Claims

Emitted by `sermon-verification` task type `redteam`. A list of flagged claims from the adversarial pass.

## Template

```markdown
# Flagged Claims (Red Team)

**Flags:** [COUNT]  |  Unsourced: [N]  Overreach: [N]  Cherry-pick: [N]  Logic gap: [N]  Anachronism: [N]

## [N]. [SHORT LABEL]
- **Claim:** "[THE EXACT STATEMENT FROM THE DRAFT, SHORT; NO LONG QUOTATION]"
- **Location:** [SECTION OR PARAGRAPH]
- **Issue:** [WHY IT IS FLAGGED]
- **Type:** [unsourced / overreach / cherry-pick / logic gap / anachronism]
- **Fix needed:** [WHAT WOULD BE REQUIRED TO SUBSTANTIATE OR CORRECT IT]

## Summary
[ONE PARAGRAPH, PLAIN LANGUAGE: THE THREE MOST SERIOUS WEAKNESSES]
```

## Rules

- "Claim" is the draft's own statement, quoted exactly and kept short
- Every flag is actionable: "Fix needed" says what source, wording change or evidence would resolve it
- Flag only what can be checked. No guesses (no invention)
- Do not soften a finding for doctrinal or delivery reasons; those are other checks
- Do not flag metaphor or devotional language as error (guardrail 11)
- An echo presented as a quotation is a flag (guardrail 8)
- An unsourced claim is a flag; in the gate, an unsourced claim with no available source is removed (guardrail 5)

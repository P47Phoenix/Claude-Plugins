# Git hooks installation (W3-16)

The repo ships an opt-in pre-commit hook at `.githooks/pre-commit` that runs
the same checks as the `skill-line-budget.yml` and `lint-known-debt.yml` CI
workflows. It catches SKILL.md tier-budget violations and JSON-Python
KNOWN_DEBT drift locally before the commit ever leaves the working tree.

## One-time install (per clone)

```bash
git config core.hooksPath .githooks
```

That's the entire setup. The hook is already executable in the tree.

## What it checks

1. `python3 scripts/check_skill_budgets.py` — Tier-A/B/C line-budget gate
   for every `delivery-team/skills/**/SKILL.md`.
2. `python3 scripts/lint_known_debt.py` — JSON-Python KNOWN_DEBT
   consistency + frontmatter rollout completeness.

Either non-zero exit blocks the commit.

## Bypass (intentional)

```bash
git commit --no-verify          # skips this hook entirely
```

Use sparingly. The CI gate still runs on PR. For a legitimate budget
exception, also include `Budget-Exception: known-debt-tk0e` in the PR body
per ADR-tk0e-002.

## Uninstall

```bash
git config --unset core.hooksPath
```

## Verification

```bash
.githooks/pre-commit            # dry-run as a smoke test (won't commit)
echo "exit=$?"                  # 0 = clean, 1 = block
```

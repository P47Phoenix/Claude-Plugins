<!-- run: run-2026-09-18-pr88 -->
# DEFECT-008: manifest.yml line 49 is invalid YAML (pre-existing on main)
- Severity: Minor (P3, non-blocking); Found by: QA UAT run-2026-09-18-pr88
- Repro: `python3 -c "import yaml;yaml.safe_load(open('delivery-team/skills/delivery-flow/references/manifest.yml'))"` -> ScannerError line 49 col 29 (mapping values not allowed). Same error on `git show HEAD:` version, so not introduced by PR #88.
- Impact: any strict YAML consumer of the manifest fails. No CI check parses it. Story TC-1.7 cannot pass.
- Fix: quote the `purpose:` scalar at line 49 (contains ": "). Separate PR.

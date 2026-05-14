# Claude-Plugins root Makefile.
#
# Smoke-test targets are LOCAL-ONLY by design — see
# delivery-team/tests/smoke/README.md (substring: feedback_claude_code_local_only)
# and the binding memory file at
# /home/meconnelly/.claude/projects/-var-home-meconnelly-Documents-GitHub-Claude-Plugins/memory/feedback_claude_code_local_only.md
# Do NOT invoke these from .github/workflows/ — CI lacks the `claude` CLI.

.PHONY: help smoke smoke-baseline smoke-tests

help:
	@echo "Available targets:"
	@echo "  smoke           Run the delivery-team plugin smoke test (single run, local-only)."
	@echo "  smoke-baseline  Run the smoke test 5x sequentially and write baseline JSON."
	@echo "  smoke-tests     Run the pytest meta-tests (fast, no claude spawn)."

smoke:
	python3 delivery-team/tests/smoke/run_smoke.py --cost-cap 3.00 --timeout 1800

smoke-baseline:
	python3 delivery-team/tests/smoke/run_smoke.py --init-baseline --cost-cap 3.00 --timeout 1800

smoke-tests:
	cd delivery-team/tests/smoke && python3 -m pytest tests/ -v

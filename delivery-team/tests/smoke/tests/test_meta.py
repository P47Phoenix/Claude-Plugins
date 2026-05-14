"""Smoke-test harness meta-tests — exactly 3 scenarios, < 5 sec wall-clock.

Producer-validator separation (ADR-tk5-001 / BACKLOG-106 / BC-03):
this module was authored by a different Stage-6 Dev dispatch than the
one that wrote `lib/metrics.py` and `lib/baseline.py`. The fixtures and
assertions below are derived from the PRD, BACKLOG-106, and the
architecture doc — never from the producer source.

Hard isolation contract (enforced by `conftest.py::_block_claude_subprocess`):
no test in this module may spawn the `claude` CLI via subprocess.Popen,
subprocess.run, or any other mechanism. Attempts to do so raise
AssertionError immediately. The autouse guard also prevents accidental
shell-outs added during future maintenance.

Scenario count:
- Test 1: `test_malformed_stream_fault_injection`
- Test 2: `test_baseline_comparison_demo`  (3 sub-assertions: PASS / HARD-FAIL / WARN)
- Test 3: `test_aggregator_fixture_parsing`

`pytest --collect-only` MUST show exactly 3 test functions (no parametrize
explosion) per AC-S3-08.
"""
from __future__ import annotations

import json
import warnings

import pytest


# --- Test 1 — malformed-stream fault injection ------------------------------

def test_malformed_stream_fault_injection(
    valid_stream_events: list[dict],
    malformed_stream_event: dict,
) -> None:
    """parse_stream must warn (not raise) on malformed events and skip them.

    Contract (AC-S3-02, TC-S3-03):
    - Feed a mix of valid + malformed events into `parse_stream`.
    - A `warnings.warn(...)` call is emitted for the malformed event.
    - The returned Metrics object reflects the *valid* events only:
      `dispatch_count` equals the number of valid events with usage blocks.
    - No exception is raised.
    """
    from lib.metrics import Metrics, parse_stream

    # 3 valid events + 1 malformed (usage is a string, not a dict).
    events = list(valid_stream_events) + [malformed_stream_event]

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        metrics = parse_stream(events)

    assert isinstance(metrics, Metrics), "parse_stream must return a Metrics dataclass"
    assert metrics.dispatch_count == 3, (
        f"dispatch_count must reflect 3 valid events only, got {metrics.dispatch_count}"
    )
    # At least one warning was raised for the malformed event.
    assert len(caught) >= 1, "parse_stream must emit at least one warning for the malformed event"
    # The malformed-event warning must mention the offending field.
    messages = " | ".join(str(w.message) for w in caught)
    assert "usage" in messages, (
        f"warning message should reference the malformed 'usage' field; got: {messages!r}"
    )

    # Sanity: valid events were aggregated.
    assert metrics.cost_usd == pytest.approx(0.30), (
        f"cost_usd should sum the 3 valid usage.cost_usd values (0.10+0.15+0.05), got {metrics.cost_usd}"
    )
    assert metrics.tokens["input"] == 300  # 100 + 150 + 50
    assert metrics.tokens["output"] == 525  # 200 + 250 + 75


# --- Test 2 — baseline-comparison demo (3 sub-assertions) -------------------

def test_baseline_comparison_demo(
    synthetic_baseline: dict,
    passing_report: dict,
    hard_fail_report: dict,
    advisory_warn_report: dict,
) -> None:
    """compare() must produce PASS / HARD-FAIL / WARN for the three canonical paths.

    Contract (AC-S3-03, TC-S3-04):
    - Report within all bands         -> RegressionResult.status == "PASS"
    - Report with cost_usd > hard_max -> RegressionResult.status == "FAIL"
    - Report with tokens.input outside mean ± 2σ -> RegressionResult.status == "WARN"
    """
    from lib.baseline import RegressionResult, compare

    # --- Sub-assertion 1: PASS ----------------------------------------------
    pass_result = compare(passing_report, synthetic_baseline)
    assert isinstance(pass_result, RegressionResult)
    assert pass_result.status == "PASS", (
        f"passing_report should yield PASS, got {pass_result.status} "
        f"(hard={pass_result.hard_failures} advisory={pass_result.advisory_warnings})"
    )
    assert pass_result.hard_failures == []
    assert pass_result.advisory_warnings == []

    # --- Sub-assertion 2: HARD-FAIL on cost_usd > hard_max ------------------
    fail_result = compare(hard_fail_report, synthetic_baseline)
    assert fail_result.status == "FAIL", (
        f"hard_fail_report should yield FAIL, got {fail_result.status}"
    )
    assert fail_result.hard_failures, "hard_failures list must be non-empty"
    fail_msg = " | ".join(fail_result.hard_failures)
    assert "cost_usd" in fail_msg, (
        f"hard_failures must name the cost_usd rule; got: {fail_msg!r}"
    )

    # --- Sub-assertion 3: WARN on tokens.input outside ±2σ ------------------
    warn_result = compare(advisory_warn_report, synthetic_baseline)
    assert warn_result.status == "WARN", (
        f"advisory_warn_report should yield WARN, got {warn_result.status} "
        f"(hard={warn_result.hard_failures} advisory={warn_result.advisory_warnings})"
    )
    assert warn_result.hard_failures == [], "WARN path must have no hard failures"
    assert warn_result.advisory_warnings, "advisory_warnings list must be non-empty"
    warn_msg = " | ".join(warn_result.advisory_warnings)
    assert "tokens.input" in warn_msg, (
        f"advisory_warnings must name tokens.input; got: {warn_msg!r}"
    )


# --- Test 3 — aggregator-fixture parsing ------------------------------------

def test_aggregator_fixture_parsing(sample_workspace) -> None:
    """aggregate() against the on-disk fixture workspace must produce the
    expected merged report dict.

    Contract (AC-S3-04, TC-S3-05):
    Fixture layout (under tests/fixtures/sample-workspace/.delivery/):
      - telemetry/skill-loads.jsonl  — 5 rows across 4 distinct skills
      - telemetry/run-summary-fake.json — overall.rows_real=5
      - state.md — stages_completed=7, 3 checked stories, defects_logged=2

    Expected merged output:
      - skill_loads: 4 entries (alphabetical), `developer` count=2
      - pipeline.stages_completed = 7
      - pipeline.stories_completed = 3
      - pipeline.defects_logged = 2
      - pipeline.dispatch_count = 0 (we pass a fresh Metrics)
      - run_summary_present = True
      - state_md_present = True
    """
    from lib.aggregator import aggregate
    from lib.metrics import Metrics

    result = aggregate(sample_workspace, Metrics())

    # Skill-loads aggregation.
    skill_loads = result["skill_loads"]
    assert isinstance(skill_loads, list), "skill_loads must be a list"
    skills_by_name = {row["skill"]: row for row in skill_loads}
    expected_skills = {
        "delivery-team:architect",
        "delivery-team:delivery-flow",
        "delivery-team:developer",
        "delivery-team:quality",
    }
    assert set(skills_by_name.keys()) == expected_skills, (
        f"skill_loads names mismatch: {set(skills_by_name.keys())} vs {expected_skills}"
    )
    assert skills_by_name["delivery-team:developer"]["count"] == 2, (
        "developer skill should be loaded twice in the fixture"
    )
    # Alphabetical ordering invariant from aggregator._aggregate_skill_loads.
    names_in_order = [row["skill"] for row in skill_loads]
    assert names_in_order == sorted(names_in_order), (
        f"skill_loads must be alphabetically sorted; got {names_in_order}"
    )
    # Prose-token mean check for the doubled skill (800 + 900) / 2 = 850.
    assert skills_by_name["delivery-team:developer"]["prose_tokens_mean"] == pytest.approx(850.0)

    # Pipeline counters scraped from state.md.
    pipeline = result["pipeline"]
    assert pipeline["stages_completed"] == 7, (
        f"stages_completed should be 7 from state.md, got {pipeline['stages_completed']}"
    )
    assert pipeline["stories_completed"] == 3, (
        f"stories_completed should be 3 (three checked items), got {pipeline['stories_completed']}"
    )
    assert pipeline["defects_logged"] == 2, (
        f"defects_logged should be 2 from state.md, got {pipeline['defects_logged']}"
    )
    assert pipeline["dispatch_count"] == 0, (
        f"dispatch_count should come from the Metrics() we passed in (=0), got {pipeline['dispatch_count']}"
    )
    # run-summary signal is informational and present.
    assert pipeline.get("telemetry_rows_real") == 5

    # Presence flags reflect the fixture layout.
    assert result["run_summary_present"] is True
    assert result["state_md_present"] is True

    # Round-trip JSON serializability — the report is consumed by report.py / json.dump.
    json.dumps(result)

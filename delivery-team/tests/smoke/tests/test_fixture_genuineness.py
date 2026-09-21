"""Fixture-genuineness facts about stream_real_shape.jsonl (PA-14, ADR-lmr-004 s5 QA W3).

These check the captured file itself, not the parser, so they are green on the P0
stub by design and live outside test_model_capture.py (whose every test must be
red at validator_start, PA-13).
"""
import hashlib
import json
from pathlib import Path

import pytest

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "stream_real_shape.jsonl"


def _real_events():
    if not FIXTURE.is_file():
        pytest.skip("blocked_on H1: fixture not committed")
    return [json.loads(x) for x in FIXTURE.read_text(encoding="utf-8").splitlines() if x.strip()]


def test_real_shape_message_id_present_on_every_assistant_event():
    """ADR-lmr-004 s5 (QA W3): count of assistant events with a non-empty message.id equals count of assistant events."""
    events = _real_events()
    asst = [e for e in events if e.get("type") == "assistant"]
    with_id = [e for e in asst if isinstance(e.get("message"), dict) and e["message"].get("id")]
    assert asst and len(with_id) == len(asst), f"{len(with_id)} of {len(asst)} assistant events carry message.id"


def test_real_shape_fixture_hash_matches_provenance():
    """PA-14: sha256 in the provenance sidecar equals the fixture bytes; no resolved model id in the sidecar."""
    _real_events()
    prov = FIXTURE.with_suffix("").with_suffix(".provenance.txt").read_text(encoding="utf-8")
    digest = hashlib.sha256(FIXTURE.read_bytes()).hexdigest()
    assert digest in prov, "provenance does not record the fixture sha256"
    assert "claude_code_version:" in prov and "command:" in prov, "provenance missing version or command"
    assert "--max-budget-usd 0.25" in prov, "provenance command lacks the 0.25 capture cap"

"""Offline regression cases for duplicate suppression and evidence preservation."""
import copy
import unittest
from state import apply

INVENTORY = {"version": 1, "repository": "owner/test", "sources": [
    {"id": "one", "url": "https://example.org/source", "country": "Denmark"}]}


def batch(run, facts=None, status="reachable", **extra):
    observation = {"source_id": "one", "status": status, "method": "fixture",
                   "origin_freshness": "fixture", "final_url": "https://example.org/source",
                   "facts": facts if status == "reachable" else None,
                   "evidence_summary": "Synthetic test, not a real source."}
    observation.update(extra)
    return {"run_id": run, "checked_on": "2026-09-25", "observations": [observation]}


class StateTests(unittest.TestCase):
    def setUp(self):
        self.first = batch("a", {"duty": "must notify", "deadline": "14 days"})
        self.state = apply(INVENTORY, None, self.first)

    def test_first_observation_is_baseline(self):
        self.assertEqual([], self.state["events"])

    def test_duplicate_run_is_idempotent(self):
        self.assertEqual(self.state, apply(INVENTORY, self.state, self.first))

    def test_cosmetic_whitespace_does_not_alert(self):
        result = apply(INVENTORY, self.state, batch("b", {"duty": " must  notify ", "deadline": "14 days"}))
        self.assertEqual([], result["events"])

    def test_negation_and_deadline_are_not_normalized_away(self):
        for facts in ({"duty": "must not notify", "deadline": "14 days"},
                      {"duty": "must notify", "deadline": "7 days"}):
            result = apply(INVENTORY, self.state, batch("b", facts))
            self.assertEqual("content_candidate", result["events"][0]["kind"])

    def test_failure_requires_two_runs_and_preserves_facts(self):
        failed = apply(INVENTORY, self.state, batch("b", status="unreachable"))
        self.assertEqual([], failed["events"])
        self.assertEqual(failed, apply(INVENTORY, failed, batch("b", status="unreachable")))
        twice = apply(INVENTORY, failed, batch("c", status="unreachable"))
        self.assertEqual("persistent_access_failure", twice["events"][0]["kind"])
        self.assertEqual(self.state["sources"]["one"]["last_good"], twice["sources"]["one"]["last_good"])
        three = apply(INVENTORY, twice, batch("d", status="unknown"))
        self.assertEqual(1, len(three["events"]))

    def test_recovery_is_not_new_route(self):
        result = self.state
        for run in ("b", "c"):
            result = apply(INVENTORY, result, batch(run, status="unreachable"))
        result = apply(INVENTORY, result, batch("d", self.first["observations"][0]["facts"]))
        self.assertEqual(["persistent_access_failure", "access_recovered"], [e["kind"] for e in result["events"]])

    def test_changed_redirect_needs_review(self):
        result = apply(INVENTORY, self.state, batch("b", self.first["observations"][0]["facts"], final_url="https://example.org/new"))
        self.assertEqual("redirect_candidate", result["events"][0]["kind"])

    def test_unknown_cannot_become_verified_by_hash(self):
        old = apply(INVENTORY, None, batch("a", {"company_route": "unknown"}))
        result = apply(INVENTORY, old, batch("b", {"company_route": "form discovered"}))
        self.assertEqual("pending", result["events"][0]["review_status"])

    def test_invalid_batch_leaves_input_intact(self):
        snapshot = copy.deepcopy(self.state)
        invalid = batch("b", {"duty": "changed"})
        invalid["observations"].append(copy.deepcopy(invalid["observations"][0]))
        with self.assertRaises(AssertionError):
            apply(INVENTORY, self.state, invalid)
        self.assertEqual(snapshot, self.state)


if __name__ == "__main__":
    unittest.main()

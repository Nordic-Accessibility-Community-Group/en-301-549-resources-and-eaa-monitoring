"""Compare agent-observed official-source facts; never fetch or certify claims.

Usage: python3 state.py inventory.json state.json observations.json
The resulting state is printed to stdout. An absent state path initializes it.
All GitHub writes and evidence verification remain with the orchestrating agent.
"""
import copy
import hashlib
import json
import sys
from datetime import date
from pathlib import Path


def normalize(value):
    if isinstance(value, str):
        return " ".join(value.split())
    if isinstance(value, dict):
        return {k: normalize(v) for k, v in sorted(value.items())}
    if isinstance(value, list):
        return [normalize(v) for v in value]
    return value


def fingerprint(value):
    data = json.dumps(normalize(value), ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(data.encode()).hexdigest()


def apply(inventory, previous, batch):
    """Return a new state. Fail before mutation on malformed or duplicate input."""
    assert inventory["version"] == 1
    catalog = {s["id"]: s for s in inventory["sources"]}
    assert len(catalog) == len(inventory["sources"]), "Duplicate source IDs"
    run_id = batch["run_id"]
    assert isinstance(run_id, str) and run_id
    day = batch["checked_on"]
    date.fromisoformat(day)
    observations = batch["observations"]
    assert len({o["source_id"] for o in observations}) == len(observations)
    for o in observations:
        assert o["source_id"] in catalog, "Unregistered source"
        assert o["status"] in ("reachable", "unreachable", "unknown")
        assert o.get("method") and o.get("evidence_summary")
        assert o.get("origin_freshness"), "Disclose reader-cache limitations"
        if o["status"] == "reachable":
            assert isinstance(o.get("facts"), dict) and o["facts"]
            assert o.get("final_url", "").startswith("https://")
        else:
            assert o.get("facts") is None, "Failure must not replace known facts"
    state = copy.deepcopy(previous) if previous else {
        "version": 1, "repository": inventory["repository"],
        "processed_runs": [], "sources": {}, "events": [], "discovery": {},
    }
    assert state["repository"] == inventory["repository"]
    assert state["version"] == 1
    if run_id in state["processed_runs"]:
        return state
    if state.get("last_run_on"):
        assert day >= state["last_run_on"], "Stale run must not overwrite state"
    for source_id, source in catalog.items():
        state["sources"].setdefault(source_id, {
            "url": source["url"], "country": source["country"],
            "status": "pending", "failure_runs": 0, "last_good": None,
            "failure_alerted": False,
        })
        assert state["sources"][source_id]["url"] == source["url"], "Source ID rebound"

    def event(source_id, kind, signature, details):
        event_id = fingerprint([source_id, kind, signature])
        if any(e["id"] == event_id for e in state["events"]):
            return
        state["events"].append({
            "id": event_id, "source_id": source_id, "kind": kind,
            "detected_on": day, "run_id": run_id,
            "review_status": "pending", "details": details,
        })

    for o in observations:
        source_id = o["source_id"]
        item = state["sources"][source_id]
        old = item["last_good"]
        if o["status"] != "reachable":
            if not item["failure_runs"]:
                item["failure_started_run"] = run_id
            item["failure_runs"] += 1
            if item["failure_runs"] >= 2 and not item["failure_alerted"]:
                event(source_id, "persistent_access_failure", item["failure_started_run"],
                      {"message": o["evidence_summary"], "last_good_preserved": bool(old)})
                item["failure_alerted"] = True
        else:
            current = {"facts": normalize(o["facts"]), "final_url": o["final_url"],
                       "checked_on": day, "fingerprint": fingerprint(o["facts"])}
            if old and old["fingerprint"] != current["fingerprint"]:
                event(source_id, "content_candidate", [old["fingerprint"], current["fingerprint"]],
                      {"before": old["facts"], "after": current["facts"],
                       "note": "Agent verification required; not an automatic table update."})
            if old and old["final_url"] != current["final_url"]:
                event(source_id, "redirect_candidate", current["final_url"],
                      {"before": old["final_url"], "after": current["final_url"]})
            if item["failure_alerted"]:
                event(source_id, "access_recovered", item["failure_started_run"],
                      {"message": "Source readable again; no automatic factual change."})
            # A first readable observation is a baseline, never proof of a new law/route.
            item["last_good"] = current
            item["failure_runs"] = 0
            item["failure_alerted"] = False
        item["status"] = o["status"]
        item["last_checked_on"] = day
        item["last_observation"] = o
    state["processed_runs"].append(run_id)
    state["last_run_on"] = day
    state["coverage"] = {
        "registered": len(catalog),
        "readable_baselines": sum(bool(state["sources"][s]["last_good"]) for s in catalog),
        "pending": sum(state["sources"][s]["status"] == "pending" for s in catalog),
        "attempted_this_run": len(observations),
    }
    return state


if __name__ == "__main__":
    inventory_path, state_path, observations_path = map(Path, sys.argv[1:])
    result = apply(json.loads(inventory_path.read_text()),
                   json.loads(state_path.read_text()) if state_path.exists() else None,
                   json.loads(observations_path.read_text()))
    print(json.dumps(result, ensure_ascii=False, indent=2))

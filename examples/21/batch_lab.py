"""Deterministic offline lab. No model, network, shell, or writes."""
import json
from pathlib import Path

BASE = Path(__file__).parent


def accept(result):
    if not isinstance(result, dict) or set(result) != {"schema_version", "pass", "findings"}:
        return "invalid-shape"
    if result["schema_version"] != "1" or type(result["pass"]) is not bool or not isinstance(result["findings"], list):
        return "invalid-shape"
    for finding in result["findings"]:
        if not isinstance(finding, dict) or set(finding) != {"severity", "message", "evidence"}:
            return "invalid-shape"
        if finding["severity"] not in ("P0", "P1", "P2"):
            return "invalid-shape"
        if not isinstance(finding["message"], str) or not isinstance(finding["evidence"], str):
            return "invalid-shape"
        if not finding["message"].strip() or not finding["evidence"].strip():
            return "missing-evidence"
    serious = any(f["severity"] in ("P0", "P1") for f in result["findings"])
    if result["pass"] and serious:
        return "contradictory-result"
    return "accepted" if result["pass"] else "review-rejected"


def run_fixture(job, max_attempts=3):
    if max_attempts < 1 or max_attempts > 3:
        raise ValueError("Lab allows one to three attempts")
    trace = []
    for attempt, step in enumerate(job["attempts"][:max_attempts], 1):
        code = step["process_code"]
        trace.append({"attempt": attempt, "process_code": code})
        if code == 0:
            verdict = accept(step.get("result"))
            return {"job_id": job["job_id"], "verdict": verdict, "trace": trace}
        # This classification belongs to the fixture runner, not Codex exit-code meanings.
        if step.get("classification") != "confirmed-transient":
            return {"job_id": job["job_id"], "verdict": "runtime-failed", "trace": trace}
    return {"job_id": job["job_id"], "verdict": "retry-exhausted", "trace": trace}


def main():
    jobs = json.loads((BASE / "jobs.json").read_text())
    for job in jobs:
        output = run_fixture(job)
        assert output["verdict"] == job["expected"], output
        assert len(output["trace"]) == job["expected_attempts"], output
        print(json.dumps(output, ensure_ascii=False))
    print("PASS: all offline cases; no Codex invocation")


if __name__ == "__main__":
    main()

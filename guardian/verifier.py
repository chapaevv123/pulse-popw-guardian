"""Deterministic PoPW evidence verification.

The protocol-facing metric object uses only the metric family documented by
Konnex. Guardian diagnostics live alongside it and are not represented as
Konnex protocol fields.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import math
from typing import Any


VERIFIER_VERSION = "pulse-popw-guardian/0.1.0"
RULESET_VERSION = "guardian-rules/1"
METRICS = (
    "accuracy", "speed", "safety", "optimal_track",
    "energy_efficiency", "trajectory_stability",
)
VERDICTS = {"SUCCESS", "FAILURE", "INCONCLUSIVE"}
REASON_CODES = {
    "EVIDENCE_MISSING", "SCHEMA_INVALID", "TELEMETRY_INCOMPLETE",
    "VIDEO_MISSING", "TIMESTAMP_MISMATCH", "TRAJECTORY_INCONSISTENT",
    "SAFETY_THRESHOLD_FAILED", "LOW_CONFIDENCE",
    "EVIDENCE_TAMPER_SUSPECTED", "INSUFFICIENT_EVIDENCE",
    "METRIC_CONFIGURATION_INVALID",
}


def _canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def _hash(value: Any) -> str:
    return hashlib.sha256(_canonical(value)).hexdigest()


def _parse_time(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _clamp(value: float) -> int:
    return int(round(max(0.0, min(100.0, value))))


def _check(check_id: str, passed: bool, detail: str, evidence: list[str] | None = None) -> dict:
    return {"check_id": check_id, "passed": bool(passed), "detail": detail,
            "evidence": evidence or []}


def _invalid_result(bundle: Any, errors: list[str], reason_codes: list[str] | None = None) -> dict:
    core = {
        "verdict": "INCONCLUSIVE", "final_pct": 0, "confidence": 0.0,
        "metrics": {name: 0 for name in METRICS},
        "reason_codes": reason_codes or ["SCHEMA_INVALID", "INSUFFICIENT_EVIDENCE"],
        "failed_checks": [_check("schema", False, item) for item in errors],
        "evidence_used": [], "provenance": [],
    }
    return _with_receipt(bundle, core)


def _validate_schema(bundle: Any) -> list[str]:
    if not isinstance(bundle, dict):
        return ["bundle must be an object"]
    errors = []
    task = bundle.get("task")
    if not isinstance(task, dict):
        return ["task must be an object"]
    for field in ("task_id", "instruction", "started_at", "completed_at", "requirements"):
        if field not in task:
            errors.append(f"task.{field} is required")
    if not isinstance(bundle.get("evidence"), list):
        errors.append("evidence must be an array")
    if not isinstance(bundle.get("telemetry"), list):
        errors.append("telemetry must be an array")
    if not isinstance(task.get("requirements", {}), dict):
        errors.append("task.requirements must be an object")
    if isinstance(bundle.get("evidence"), list):
        seen_ids: set[str] = set()
        for index, item in enumerate(bundle["evidence"]):
            if not isinstance(item, dict):
                errors.append(f"evidence[{index}] must be an object")
                continue
            for field in ("evidence_id", "type", "source", "sha256", "payload"):
                if field not in item:
                    errors.append(f"evidence[{index}].{field} is required")
            evidence_id = item.get("evidence_id")
            if not isinstance(evidence_id, str) or not evidence_id.strip():
                errors.append(f"evidence[{index}].evidence_id must be a non-empty string")
            elif evidence_id in seen_ids:
                errors.append(f"evidence[{index}].evidence_id must be unique")
            else:
                seen_ids.add(evidence_id)
            if not isinstance(item.get("source"), str) or not item.get("source", "").strip():
                errors.append(f"evidence[{index}].source must be a non-empty string")
    if isinstance(bundle.get("telemetry"), list):
        for index, sample in enumerate(bundle["telemetry"]):
            if not isinstance(sample, dict):
                errors.append(f"telemetry[{index}] must be an object")
            elif "timestamp" not in sample:
                errors.append(f"telemetry[{index}].timestamp is required")
    try:
        if task.get("started_at") and task.get("completed_at"):
            if _parse_time(task["completed_at"]) <= _parse_time(task["started_at"]):
                errors.append("task.completed_at must follow task.started_at")
    except (TypeError, ValueError):
        errors.append("task timestamps must be ISO-8601")
    return errors


def _with_receipt(bundle: Any, core: dict) -> dict:
    task = bundle.get("task", {}) if isinstance(bundle, dict) else {}
    receipt_body = {
        "verifier": VERIFIER_VERSION,
        "ruleset": RULESET_VERSION,
        "input_hash": _hash(bundle),
        "task_id": task.get("task_id"),
        "verdict": core["verdict"],
        "final_pct": core["final_pct"],
        "confidence": core["confidence"],
        "metrics": core["metrics"],
        "reason_codes": core["reason_codes"],
    }
    receipt_body["receipt_id"] = "pgr_" + _hash(receipt_body)[:24]
    receipt_body["issued_at"] = task.get("completed_at")
    return {**core, "audit_receipt": receipt_body}


def verify_bundle(bundle: Any) -> dict:
    """Verify a normalized bundle without network, wallet, LLM, or mutable state."""
    schema_errors = _validate_schema(bundle)
    if schema_errors:
        return _invalid_result(bundle, schema_errors)

    task = bundle["task"]
    requirements = task["requirements"]
    evidence = bundle["evidence"]
    telemetry = bundle["telemetry"]
    checks: list[dict] = []
    reasons: set[str] = set()

    evidence_types = {str(item.get("type", "")).lower() for item in evidence if isinstance(item, dict)}
    required_types = {str(x).lower() for x in requirements.get("required_evidence", ["video", "telemetry"])}
    missing_types = sorted(required_types - evidence_types)
    checks.append(_check("evidence.completeness", not missing_types,
                         "all required evidence types present" if not missing_types else "missing: " + ", ".join(missing_types)))
    if missing_types:
        reasons.add("EVIDENCE_MISSING")
        if "video" in missing_types or "frames" in missing_types:
            reasons.add("VIDEO_MISSING")

    provenance = []
    tampered = False
    for item in evidence:
        if not isinstance(item, dict):
            tampered = True
            continue
        claimed = str(item.get("sha256") or "")
        payload = item.get("payload")
        actual = hashlib.sha256(str(payload).encode()).hexdigest() if payload is not None else ""
        valid = len(claimed) == 64 and claimed == actual
        tampered |= not valid
        provenance.append({"evidence_id": item.get("evidence_id"), "type": item.get("type"),
                           "source": item.get("source"), "claimed_sha256": claimed,
                           "observed_sha256": actual, "hash_valid": valid})
    checks.append(_check("provenance.hashes", not tampered,
                         "all evidence hashes match payloads" if not tampered else "one or more evidence hashes mismatch",
                         [str(x.get("evidence_id")) for x in evidence if isinstance(x, dict)]))
    if tampered:
        reasons.add("EVIDENCE_TAMPER_SUSPECTED")

    start, end = _parse_time(task["started_at"]), _parse_time(task["completed_at"])
    timestamp_bad = False
    parsed_samples = []
    previous = None
    for index, sample in enumerate(telemetry):
        try:
            stamp = _parse_time(sample["timestamp"])
            timestamp_bad |= not (start <= stamp <= end) or (previous is not None and stamp <= previous)
            previous = stamp
            parsed_samples.append((stamp, sample))
        except (KeyError, TypeError, ValueError):
            timestamp_bad = True
    checks.append(_check("telemetry.timestamps", not timestamp_bad, "timestamps are ordered and inside task window" if not timestamp_bad else "invalid, unordered, or out-of-window timestamp"))
    if timestamp_bad:
        reasons.add("TIMESTAMP_MISMATCH")

    try:
        min_samples = max(2, int(requirements.get("min_telemetry_samples", 3)))
        target_duration = max(1.0, float(requirements.get("target_duration_s", (end - start).total_seconds())))
        expected_distance = max(0.01, float(requirements.get("expected_distance", 1)))
        energy_budget = max(0.01, float(requirements.get("energy_budget", 1)))
        safety_min = int(requirements.get("safety_min", 70))
        final_min = int(requirements.get("final_min", 75))
        confidence_min = float(requirements.get("confidence_min", 0.75))
        weights = requirements.get("metric_weights", {})
        if not isinstance(weights, dict):
            raise ValueError("metric_weights must be an object")
        metric_weights = {name: float(weights.get(name, 1)) for name in METRICS}
        if any(not math.isfinite(value) or value < 0 for value in metric_weights.values()):
            raise ValueError("metric weights must be finite and non-negative")
        if sum(metric_weights.values()) <= 0:
            raise ValueError("metric weights must have a positive sum")
        if not (0 <= safety_min <= 100 and 0 <= final_min <= 100 and 0 <= confidence_min <= 1):
            raise ValueError("thresholds are out of range")
    except (TypeError, ValueError, OverflowError) as exc:
        return _invalid_result(bundle, [f"invalid requirements: {exc}"],
                               ["METRIC_CONFIGURATION_INVALID", "SCHEMA_INVALID"])

    telemetry_complete = len(parsed_samples) >= min_samples
    checks.append(_check("telemetry.coverage", telemetry_complete,
                         f"{len(parsed_samples)}/{min_samples} required samples"))
    if not telemetry_complete:
        reasons.add("TELEMETRY_INCOMPLETE")

    try:
        progress = float(parsed_samples[-1][1].get("progress", 0)) if parsed_samples else 0.0
        duration = (end - start).total_seconds()
        distances = [float(s.get("distance", 0)) for _, s in parsed_samples]
        if "expected_distance" not in requirements:
            expected_distance = max(max(distances, default=0.0), 0.01)
        energy_values = [float(s.get("energy", 0)) for _, s in parsed_samples]
        if "energy_budget" not in requirements:
            energy_budget = max(max(energy_values, default=0.0), 0.01)
        collisions = sum(int(s.get("collisions", 0)) for _, s in parsed_samples)
        violations = sum(int(s.get("safety_violations", 0)) for _, s in parsed_samples)
        jitter = max([float(s.get("jitter", 0)) for _, s in parsed_samples], default=1.0)
        numeric_values = [progress, *distances, *energy_values, jitter]
        if any(not math.isfinite(value) for value in numeric_values):
            raise ValueError("telemetry values must be finite")
    except (TypeError, ValueError, OverflowError) as exc:
        return _invalid_result(bundle, [f"invalid telemetry: {exc}"])
    actual_distance = max(distances, default=0.0)
    energy_used = max(energy_values, default=0.0)

    trajectory_bad = any(b < a for a, b in zip(distances, distances[1:])) or actual_distance > expected_distance * 2.0
    checks.append(_check("trajectory.consistency", not trajectory_bad,
                         "distance progression is plausible" if not trajectory_bad else "distance regressed or exceeded 2x expected path"))
    if trajectory_bad:
        reasons.add("TRAJECTORY_INCONSISTENT")

    metrics = {
        "accuracy": _clamp(progress * 100),
        "speed": _clamp(100 if duration <= target_duration else 100 * target_duration / duration),
        "safety": _clamp(100 - collisions * 50 - violations * 25),
        "optimal_track": _clamp(100 * min(expected_distance, actual_distance) / max(expected_distance, actual_distance, 0.01)),
        "energy_efficiency": _clamp(100 * min(energy_budget, energy_used or energy_budget) / max(energy_budget, energy_used, 0.01)),
        "trajectory_stability": _clamp(100 * (1.0 - jitter)),
    }
    denominator = sum(metric_weights.values())
    final_pct = _clamp(sum(metrics[name] * metric_weights[name] for name in METRICS) / denominator)

    safety_failed = metrics["safety"] < safety_min
    checks.append(_check("threshold.safety", not safety_failed,
                         f"safety {metrics['safety']} vs minimum {safety_min}"))
    if safety_failed:
        reasons.add("SAFETY_THRESHOLD_FAILED")

    completeness = 1.0 if not missing_types else max(0.0, 1 - len(missing_types) / max(1, len(required_types)))
    provenance_score = 1.0 if provenance and not tampered else 0.0
    consistency = 1.0 if not timestamp_bad and not trajectory_bad else 0.25 if not (timestamp_bad and trajectory_bad) else 0.0
    coverage = min(1.0, len(parsed_samples) / min_samples)
    confidence = round(0.40 * completeness + 0.25 * provenance_score + 0.20 * consistency + 0.15 * coverage, 3)
    if confidence < confidence_min:
        reasons.add("LOW_CONFIDENCE")

    insufficient = bool(missing_types or not telemetry_complete) and not tampered
    if insufficient:
        reasons.add("INSUFFICIENT_EVIDENCE")
        verdict = "INCONCLUSIVE"
    elif tampered or safety_failed or trajectory_bad or timestamp_bad:
        verdict = "FAILURE"
    elif final_pct >= final_min and confidence >= confidence_min:
        verdict = "SUCCESS"
    else:
        verdict = "FAILURE"

    assert verdict in VERDICTS and reasons <= REASON_CODES
    evidence_used = [{"evidence_id": x.get("evidence_id"), "type": x.get("type"), "source": x.get("source")}
                     for x in evidence if isinstance(x, dict)]
    core = {
        "verdict": verdict, "final_pct": final_pct, "confidence": confidence,
        "metrics": metrics, "reason_codes": sorted(reasons),
        "failed_checks": [x for x in checks if not x["passed"]],
        "checks": checks, "evidence_used": evidence_used, "provenance": provenance,
    }
    return _with_receipt(bundle, core)

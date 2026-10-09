"""Conservative, deterministic screening for a synthetic reuse demonstration."""

from __future__ import annotations

import math
from typing import Any


REQUIREMENT_FIELDS = ("id", "grade", "thickness_mm", "length_mm", "width_mm", "project_id")
DIMENSION_FIELDS = ("thickness_mm", "length_mm", "width_mm")
TRANSFER_VALUES = {"same_project", "allowed", "restricted", "unknown"}


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _positive_number(value: Any) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(value)
        and value > 0
    )


def validate_input(payload: Any) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Validate the request envelope and required requirement fields."""
    if not isinstance(payload, dict):
        raise ValueError("Input must be a JSON object.")
    requirement = payload.get("requirement")
    candidates = payload.get("candidates")
    if not isinstance(requirement, dict):
        raise ValueError("'requirement' must be an object.")
    if not isinstance(candidates, list):
        raise ValueError("'candidates' must be an array.")

    for field in REQUIREMENT_FIELDS:
        value = requirement.get(field)
        if field in DIMENSION_FIELDS:
            valid = _positive_number(value)
        else:
            valid = _nonempty_string(value)
        if not valid:
            raise ValueError(f"Requirement field '{field}' is missing or invalid.")

    for index, candidate in enumerate(candidates):
        if not isinstance(candidate, dict):
            raise ValueError(f"Candidate at index {index} must be an object.")
        if not _nonempty_string(candidate.get("id")):
            raise ValueError(f"Candidate at index {index} needs a non-empty 'id'.")
    return requirement, candidates


def evaluate_candidate(requirement: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    """Return a reasoned screening result; unknowns never imply approval."""
    reasons: list[str] = []
    incompatible = False
    needs_review = False

    grade = candidate.get("grade")
    if not _nonempty_string(grade):
        reasons.append("Grade is missing or unknown; verify material identity.")
        needs_review = True
    elif grade.strip().casefold() != requirement["grade"].strip().casefold():
        reasons.append("Grade does not match the requirement.")
        incompatible = True

    for field in DIMENSION_FIELDS:
        value = candidate.get(field)
        if not _positive_number(value):
            reasons.append(f"{field} is missing or invalid; verify recorded dimensions.")
            needs_review = True

    thickness = candidate.get("thickness_mm")
    if _positive_number(thickness) and thickness != requirement["thickness_mm"]:
        reasons.append("Thickness does not match the requirement.")
        incompatible = True

    length = candidate.get("length_mm")
    width = candidate.get("width_mm")
    req_length = requirement["length_mm"]
    req_width = requirement["width_mm"]
    if _positive_number(length) and _positive_number(width):
        fits = (length >= req_length and width >= req_width) or (
            length >= req_width and width >= req_length
        )
        if not fits:
            reasons.append("Recorded dimensions are insufficient for the requirement.")
            incompatible = True

    available = candidate.get("available")
    if available is False:
        reasons.append("Remnant is marked unavailable.")
        incompatible = True
    elif available is not True:
        reasons.append("Availability is missing or unknown; confirm stock is unreserved.")
        needs_review = True

    permission = candidate.get("transfer_permission", "unknown")
    if not isinstance(permission, str) or permission not in TRANSFER_VALUES:
        reasons.append("Transfer permission is unrecognized; verify authorization.")
        needs_review = True
    elif permission == "restricted":
        reasons.append("Project transfer is restricted.")
        incompatible = True
    elif permission == "unknown":
        reasons.append("Project transfer permission is unknown; do not assume approval.")
        needs_review = True
    elif permission == "same_project":
        candidate_project = candidate.get("project_id")
        if not _nonempty_string(candidate_project):
            reasons.append("Owning project is missing; same-project eligibility cannot be confirmed.")
            needs_review = True
        elif candidate_project != requirement["project_id"]:
            reasons.append("Remnant belongs to a different project and is not eligible for transfer.")
            incompatible = True
    elif permission == "allowed" and not _nonempty_string(candidate.get("project_id")):
        reasons.append("Owning project is missing; remnant provenance cannot be confirmed.")
        needs_review = True

    certification = candidate.get("certification_status", "unknown")
    if certification != "verified":
        reasons.append("Certification/traceability is not verified; qualified human review is required.")
        needs_review = True

    if incompatible:
        status = "ineligible"
    elif needs_review:
        status = "human_review"
    else:
        reasons.append("Recorded attributes pass the demonstration's screening rules; human approval is still required.")
        status = "eligible"

    return {"candidate_id": candidate["id"], "status": status, "reasons": reasons, "accepted": False}


def evaluate(payload: Any) -> dict[str, Any]:
    requirement, candidates = validate_input(payload)
    return {
        "requirement_id": requirement["id"],
        "decisions": [evaluate_candidate(requirement, candidate) for candidate in candidates],
    }


def approve_recommendation(decision: dict[str, Any], *, human_approved: bool) -> dict[str, Any]:
    """Mark an eligible recommendation accepted only after explicit approval."""
    if human_approved is not True:
        raise ValueError("Explicit human approval is required.")
    if decision.get("status") != "eligible":
        raise ValueError("Only an eligible recommendation can be accepted; resolve review or rejection first.")
    accepted = dict(decision)
    accepted["accepted"] = True
    accepted["human_approved"] = True
    return accepted

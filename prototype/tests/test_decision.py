import unittest

from src.decision import approve_recommendation, evaluate, evaluate_candidate


REQUIREMENT = {
    "id": "REQ-1",
    "grade": "S355",
    "thickness_mm": 12,
    "length_mm": 1200,
    "width_mm": 500,
    "project_id": "PROJECT-A",
}


def candidate(**updates):
    base = {
        "id": "REM-1",
        "grade": "S355",
        "thickness_mm": 12,
        "length_mm": 1300,
        "width_mm": 600,
        "available": True,
        "transfer_permission": "same_project",
        "project_id": "PROJECT-A",
        "certification_status": "verified",
    }
    base.update(updates)
    return base


class CandidateDecisionTests(unittest.TestCase):
    def test_compatible_material_is_eligible_but_not_accepted(self):
        result = evaluate_candidate(REQUIREMENT, candidate())
        self.assertEqual(result["status"], "eligible")
        self.assertFalse(result["accepted"])

    def test_incompatible_grade_is_ineligible(self):
        result = evaluate_candidate(REQUIREMENT, candidate(grade="S275"))
        self.assertEqual(result["status"], "ineligible")
        self.assertTrue(any("Grade does not match" in reason for reason in result["reasons"]))

    def test_insufficient_dimensions_are_ineligible(self):
        result = evaluate_candidate(REQUIREMENT, candidate(length_mm=900, width_mm=400))
        self.assertEqual(result["status"], "ineligible")
        self.assertTrue(any("insufficient" in reason for reason in result["reasons"]))

    def test_unavailable_material_is_ineligible(self):
        result = evaluate_candidate(REQUIREMENT, candidate(available=False))
        self.assertEqual(result["status"], "ineligible")

    def test_restricted_project_transfer_is_ineligible(self):
        result = evaluate_candidate(REQUIREMENT, candidate(transfer_permission="restricted"))
        self.assertEqual(result["status"], "ineligible")

    def test_same_project_transfer_from_other_project_is_ineligible(self):
        result = evaluate_candidate(REQUIREMENT, candidate(project_id="PROJECT-B"))
        self.assertEqual(result["status"], "ineligible")
        self.assertTrue(any("different project" in reason for reason in result["reasons"]))

    def test_unknown_transfer_requires_review(self):
        result = evaluate_candidate(REQUIREMENT, candidate(transfer_permission="unknown"))
        self.assertEqual(result["status"], "human_review")
        self.assertFalse(result["accepted"])

    def test_unknown_certification_requires_review(self):
        result = evaluate_candidate(REQUIREMENT, candidate(certification_status="unknown"))
        self.assertEqual(result["status"], "human_review")

    def test_malformed_transfer_permission_requires_review(self):
        result = evaluate_candidate(REQUIREMENT, candidate(transfer_permission=["allowed"]))
        self.assertEqual(result["status"], "human_review")

    def test_missing_project_identity_requires_review_for_allowed_transfer(self):
        result = evaluate_candidate(
            REQUIREMENT,
            candidate(transfer_permission="allowed", project_id=None),
        )
        self.assertEqual(result["status"], "human_review")

    def test_malformed_requirement_is_rejected(self):
        with self.assertRaises(ValueError):
            evaluate({"requirement": {"id": "REQ-1"}, "candidates": []})

    def test_approval_requires_explicit_human_approval(self):
        recommendation = evaluate_candidate(REQUIREMENT, candidate())
        with self.assertRaises(ValueError):
            approve_recommendation(recommendation, human_approved=False)
        accepted = approve_recommendation(recommendation, human_approved=True)
        self.assertTrue(accepted["accepted"])

    def test_review_recommendation_cannot_be_accepted(self):
        recommendation = evaluate_candidate(REQUIREMENT, candidate(certification_status="unknown"))
        with self.assertRaises(ValueError):
            approve_recommendation(recommendation, human_approved=True)


if __name__ == "__main__":
    unittest.main()

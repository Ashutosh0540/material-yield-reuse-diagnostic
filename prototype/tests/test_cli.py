import json
import subprocess
import sys
import unittest
from pathlib import Path


PROTOTYPE_DIR = Path(__file__).resolve().parents[1]


class CliWorkflowTests(unittest.TestCase):
    def test_synthetic_fixture_runs_through_documented_cli(self):
        completed = subprocess.run(
            [sys.executable, "-m", "src.evaluate", "data/example_case.json"],
            cwd=PROTOTYPE_DIR,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        result = json.loads(completed.stdout)
        self.assertEqual(result["requirement_id"], "SYN-REQ-001")
        self.assertEqual(
            [(decision["candidate_id"], decision["status"]) for decision in result["decisions"]],
            [
                ("SYN-REM-001", "eligible"),
                ("SYN-REM-002", "ineligible"),
                ("SYN-REM-003", "ineligible"),
                ("SYN-REM-004", "ineligible"),
                ("SYN-REM-005", "ineligible"),
                ("SYN-REM-006", "human_review"),
            ],
        )
        self.assertTrue(all(decision["reasons"] for decision in result["decisions"]))


if __name__ == "__main__":
    unittest.main()

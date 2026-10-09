# Sample run

This report summarizes output actually produced from the checked-in synthetic fixture by the local CLI. It is not an operational result.

## Reproduce

From `prototype/`:

```bash
python3 -m src.evaluate data/example_case.json
```

## Observed decisions

| Candidate | Status observed | Explanation |
|---|---|---|
| `SYN-REM-001` | `eligible` | Recorded attributes pass the demo checks; `accepted` is false and human approval remains required. |
| `SYN-REM-002` | `ineligible` | Grade mismatch. |
| `SYN-REM-003` | `ineligible` | Dimensions insufficient. |
| `SYN-REM-004` | `ineligible` | Marked unavailable. |
| `SYN-REM-005` | `ineligible` | Transfer marked restricted. |
| `SYN-REM-006` | `human_review` | Transfer permission unknown and certification/traceability not verified. |

The output contains reason strings for each result. The CLI neither ranks candidates nor records any human action. All identifiers and attribute values are fabricated; see the [synthetic data guide](../docs/04-synthetic-data-guide.md).

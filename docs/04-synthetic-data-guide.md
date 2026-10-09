# 04 — Synthetic data guide

> **SYNTHETIC DEMONSTRATION DATA — NOT CLIENT DATA**
>
> The single checked-in JSON fixture contains fabricated records authored directly for this repository to exercise rule outcomes. No generator script is used. No values were taken from discovery notes, a client ERP, STRUMIS, PLM, nesting software, or operational records.

## File and purpose

[`prototype/data/example_case.json`](../prototype/data/example_case.json) contains one synthetic material requirement and six synthetic remnant candidates. Values are fixed, hand-authored test inputs, not a statistically representative sample. The fixture shows a passing candidate, a grade mismatch, insufficient dimensions, unavailable stock, restricted transfer, and unknown transfer/certification.

The example answers “does the rule code return the expected reason?” It does not estimate material availability, reuse rate, yield, waste, costs, or client performance.

## Schema and units

| Record / field | JSON type and unit | Required? | Demonstration meaning |
|---|---|---:|---|
| Requirement `id` | non-empty string | Yes | Synthetic identifier. |
| Requirement `grade` | non-empty string | Yes | Target grade; exact case-insensitive string match. |
| Requirement `thickness_mm` | positive number, mm | Yes | Target thickness; exact numeric match. |
| Requirement `length_mm`, `width_mm` | positive number, mm | Yes | Rectangular blank dimensions; rotation is allowed in the simple fit check. |
| Requirement `project_id` | non-empty string | Yes | Synthetic destination project. |
| Candidate `id` | non-empty string | Yes | Synthetic remnant identifier. |
| Candidate `grade`, `thickness_mm`, `length_mm`, `width_mm` | string / positive numbers, mm | Screening fields | Stock assertions checked against requirement. Missing/invalid values require review unless another known incompatibility rejects. |
| Candidate `available` | boolean | Screening field | `false` rejects; missing or non-boolean requires review. |
| Candidate `transfer_permission` | string | Screening field | `same_project`, `allowed`, `restricted`, or `unknown`. Unknown/malformed requires review; restricted rejects. |
| Candidate `project_id` | non-empty string | Needed for traceability | With `same_project`, must match the requirement. With `allowed`, transfer is explicitly asserted, but project identity is still needed to trace ownership. |
| Candidate `certification_status` | string | Screening field | Only exact `verified` passes this illustrative gate. This is an assertion, not certificate verification. |

The output has `requirement_id` and one decision per candidate: `candidate_id`, `status`, `reasons`, and `accepted`. It does not record reviewer identity, timestamp, or a durable audit event.

## Example assumptions and outcomes

All grades, IDs, dimensions, availability flags, projects, permissions, and certification labels are invented. `S355`/`S275` and the millimetre values are demonstration strings/numbers only; they are not client grade requirements. Candidate 001 marks certification `verified` to exercise the eligible path, while candidate 006 uses `unknown` to exercise human review. Neither label represents a validated certificate or material record.

| Candidate | Fabricated variation | Expected behavior |
|---|---|---|
| `SYN-REM-001` | Exact grade/thickness, sufficient dimensions, available, same project, status marked verified | Eligible; `accepted` remains false. |
| `SYN-REM-002` | Different grade | Ineligible with grade reason. |
| `SYN-REM-003` | Dimensions smaller than requirement | Ineligible with dimension reason. |
| `SYN-REM-004` | `available: false` | Ineligible. |
| `SYN-REM-005` | `transfer_permission: restricted` | Ineligible. |
| `SYN-REM-006` | Transfer and certification unknown | Human review; unknown is not approval. |

Missing grade/dimensions/availability/certification, malformed permission, or missing project identity are also designed to require review when no known incompatibility already rejects the candidate. Invalid requirement envelope/fields stop evaluation with an input error. Tests exercise this behavior in [`prototype/tests/test_decision.py`](../prototype/tests/test_decision.py).

Examples of invalid input behavior (not additional fixture rows): an absent `available` field yields review; a list value such as `['allowed']` for `transfer_permission` yields review rather than crashing; a requirement with zero thickness fails input validation. These are software test cases, not material examples.

## Reproduce

```bash
cd prototype
python3 -m src.evaluate data/example_case.json
```

There is no generator or dependency file; output is deterministic for the checked-in fixture and code version. See the [system design](05-system-design.md) for rule details.

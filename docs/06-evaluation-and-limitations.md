# 06 — Evaluation and limitations

## Verified tests

The checked-in standard-library `unittest` suite was run from `prototype/` with:

```bash
python3 -m unittest discover -s tests -v
```

It covers compatible material, incompatible grade, insufficient dimensions, unavailable stock, restricted project transfer, same-project ownership mismatch, unknown transfer permission, unknown certification, malformed/missing inputs, the explicit human-approval boundary, and the documented CLI workflow. The current suite contains 14 tests.

Passing tests establish that these selected code paths return expected results for the tested synthetic inputs. They do **not** establish engineering compatibility, valid material certification, data quality, useful business outcomes, performance at scale, integration correctness, safe operational use, or production readiness.

## Prototype limitations

- Fabricated data only; no client data, baseline, cost data, or measured savings.
- Exact grade/thickness checks and rectangular geometry are illustrative, not approved material rules.
- No nesting optimization, cut sequence, kerf, shape, defect/condition, tolerances, rolling direction, machining allowances, or structural design checks.
- No certification document validation, heat/lot traceability, authoritative inventory, reservation, transfer authorization service, or race-condition handling.
- No authenticated human, durable approval, audit log, exception workflow, or persistent evidence.
- No STRUMIS or other integration; no production-grade security, monitoring, deployment, or support model.
- The output does not rank candidates and should not be interpreted as a recommendation for actual allocation or cutting.

## Missing evaluation work

The proposed diagnostic must first determine whether usable evidence exists, validate field definitions and process owners, quantify a trustworthy baseline, and have qualified reviewers adjudicate candidate matches and exceptions. Any later pilot needs agreed targets, a bounded cohort, comparison approach, traceability controls, stop conditions, and a manual fallback. None of this work has happened.

## Production pilot gate

Before any real use, the client would need to validate all compatibility and safety/quality constraints; identify authoritative sources for stock, certification, and transfer rights; define identity, approval, and audit controls; assess security, privacy, retention, and integration requirements; train accountable users; and verify operational fallbacks. A pilot should proceed only if the diagnostic justifies it and client owners approve the safeguards.

Possible next decisions remain: configure an existing capability, change process, run a controlled pilot, or do not build. See the [proposed methodology](03-diagnostic-methodology.md).

# Prototype

Run from this directory with Python 3.9+:

```bash
python3 -m src.evaluate data/example_case.json
python3 -m unittest discover -s tests -v
```

The CLI loads and validates a JSON requirement and candidate list, then prints deterministic screening decisions with reason strings. No external packages are needed. `src/decision.py` also exposes `approve_recommendation`, which only returns an accepted decision for an eligible recommendation after an explicit `human_approved=True` argument. The CLI does not accept or persist approvals, and the helper does not identify or authenticate the person approving.

Implemented: input validation, conservative handling of unknown attributes, rule explanations, and an explicit approval gate. Mocked: synthetic inventory and stated availability, transfer permissions, project identity, and certification status. Not implemented: candidate ranking, optimization/nesting, certificate verification, inventory reservation, durable audit/authentication, or system integration. This demonstration is not suitable for production use. Fixture provenance and field semantics are documented in [`../docs/04-synthetic-data-guide.md`](../docs/04-synthetic-data-guide.md).

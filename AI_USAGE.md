# AI usage disclosure

- **Tool used:** OpenAI Codex, powered by GPT-6, in this coding session.
- **Contribution:** assisted with the initial Python demo and synthetic fixture, then audited and reorganized the documentation, expanded the case framing using context supplied in the request, corrected a transfer-provenance edge case, and added unit tests and diagrams.
- **Review performed:** source, tests, fixture values, documentation claims, and repository structure were inspected in this session. The unit tests and CLI were run. This is not independent authorship, a security review, or domain-expert validation.
- **Modified or rejected output:** documentation was revised to distinguish supplied case context, assumptions, hypotheses, and fabricated data. The `allowed` transfer path was tightened so missing source project identity requires review. Technical decisions remain deterministic; no LLM compatibility decision or client outcome was generated or used.
- **Known limits:** AI-assisted text and code may contain errors. The fabricated example values and compatibility rules require review; no qualified steel engineering, quality, legal, or security expert has validated them.
- **Data handling:** no client dataset was supplied or included. The checked-in JSON values were authored as synthetic demonstration inputs and were not generated from client records.

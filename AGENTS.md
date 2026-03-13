# Agent Guidance

Repository stance: schema-first, contract-first. No application code until schemas, prompts, and workflows are stable.

- Prefer deterministic structures over clever prose; keep outputs export-ready.
- Never generate comments without anchors to real text or document elements.
- Preserve markdown and JSON hygiene; avoid trailing whitespace and malformed fields.
- Do not implement major code without an explicit schema or workflow contract.
- Prefer additive, auditable edits; avoid silent renames or field changes without updating references.
- When in doubt, strengthen docs/contracts/examples before adding code.

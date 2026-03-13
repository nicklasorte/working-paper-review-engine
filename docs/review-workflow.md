# Review Workflow

1. Ingest PDF.
2. Parse structure: identify sections, tables, figures, footnotes, recommendations with stable IDs.
3. Map anchors: page/paragraph/element references for downstream grounding.
4. Apply selected persona(s) and review rubric.
5. Generate anchored comments tied to specific text or elements.
6. Deduplicate and normalize comments; enforce taxonomy and severity conventions.
7. Export matrix and run manifest in deterministic formats (CSV/XLSX/JSON).
8. Evaluate run quality against criteria (anchor accuracy, duplication, actionability, persona fidelity).

## Failure Modes to Monitor
- Hallucinated comments not supported by document text.
- Vague comments without actionable guidance.
- Duplicate or near-duplicate comments that bloat matrices.
- Missing anchors (no page/section/element reference).
- Persona drift (tone or focus misaligned with persona definition).

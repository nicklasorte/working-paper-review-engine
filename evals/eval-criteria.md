# Evaluation Criteria

- **Anchor accuracy:** every comment must reference real text or elements with correct page/section/element IDs.
- **Actionability:** comments include clear suggested revisions and rationale.
- **Duplication rate:** detect and minimize duplicate or near-duplicate comments.
- **Persona fidelity:** tone, focus, and objections align with the selected persona.
- **Hallucination / false-issue rate:** absence of invented issues or content not supported by the document.
- **Export completeness:** all required fields populate according to `comment_matrix_export.schema.json`.
- **Historical comparison:** when real past comments exist, compare overlap, coverage, and severity alignment.

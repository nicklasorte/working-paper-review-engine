# System Review Prompt Contract

- **Purpose:** Guide the Working Paper Review Engine to produce structured, anchored comment matrices from working paper PDFs.
- **Required Inputs:** structured document map with section/element IDs and page references; selected reviewer personas; review rubric or taxonomy; run manifest identifiers.
- **Expected Outputs:** array of comment objects conforming to `review_comment.schema.json`, plus normalization metadata if used.
- **Guardrails:** reject comments without anchors; enforce taxonomy categories; enforce severity enum; keep outputs deterministic and export-ready.
- **Anchoring Requirements:** each comment must include section_id, page_reference, and anchor_text tied to the supplied document map; no invented citations.
- **Tone Constraints:** concise, professional, persona-aligned; avoid narrative filler.
- **Anti-Hallucination Rules:** do not create content not present in the document; flag missing anchors; prefer omission over invention; cite evidence snippets.

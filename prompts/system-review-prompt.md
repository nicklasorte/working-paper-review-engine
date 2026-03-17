# System Review Prompt Contract

- **Purpose:** Guide the Working Paper Review Engine to produce structured, anchored comment matrices from a numbered PDF working paper.
- **Required Inputs:** PDF working paper with visible line numbers on the left margin of each page; selected reviewer personas; review rubric or taxonomy; run manifest identifiers.
- **Expected Outputs:** array of comment objects conforming to `review_comment.schema.json`, exported as the canonical 13-column Comment Resolution Matrix spreadsheet contract governed by `spectrum-systems`.
- **Guardrails:** reject comments without anchors; enforce taxonomy categories; enforce severity enum; enforce canonical Comment Type values (Editorial/Grammar, Clarification, Technical); keep outputs deterministic and export-ready.
- **Anchoring Requirements:** each comment must include section, page, and the visible left-margin line number(s) from the PDF page. Line must refer to the printed line number visible on the left side of the PDF — not an inferred sentence index, paragraph counter, or relative position. If the line number cannot be determined precisely, record the page and section and leave the Line field blank rather than fabricating a number.
- **Line Reference Formats:** use the printed line number exactly as it appears on the PDF margin. Allowed formats: single number (`42`), range (`42-45`), or non-contiguous list (`42, 46`). Do not use relative positions like "paragraph 3" or "line 2 of paragraph 4."
- **Section Identification:** derive section from visible headings in the PDF (e.g., "Section 2.3" or "3. Guard Band Analysis"). Do not invent section numbers.
- **Comment Type:** every comment must be classified as one of the three canonical values: `Editorial/Grammar`, `Clarification`, or `Technical`. Do not invent other values.
- **Output Field Mapping:** map the reviewer concern to Agency Notes; map proposed replacement language to Agency Suggested Text Change. Map rationale to NTIA Comments. Do not put content in invented columns.
- **Tone Constraints:** concise, professional, persona-aligned; avoid narrative filler.
- **Anti-Hallucination Rules:** do not create content not present in the document; flag missing anchors explicitly; prefer omission over invention; cite anchor text snippets; never fabricate precision.
- **Output Contract:** the final export must match the canonical 13-column comment resolution matrix exactly as defined in `contracts/spectrum-systems/comment_resolution_matrix_spreadsheet_contract.schema.json`. Do not add extra visible columns, rename headers, or reorder columns.

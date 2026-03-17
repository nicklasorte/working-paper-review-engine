# Evaluation Criteria

## Core Criteria

- **Anchor accuracy:** every comment must reference real text with correct section, page, and left-margin line numbers from the PDF; no invented anchors.
- **Actionability:** comments include clear suggested revisions (Agency Suggested Text Change) and rationale (Agency Notes).
- **Duplication rate:** detect and minimize duplicate or near-duplicate comments.
- **Persona fidelity:** tone, focus, and objections align with the selected persona.
- **Hallucination / false-issue rate:** absence of invented issues or content not supported by the document.
- **Export completeness:** all 13 canonical columns populate per `schemas/comment_matrix_export.schema.json`.
- **Historical comparison:** when real past comments exist, compare overlap, coverage, and severity alignment.

## PDF Anchoring Checks

- **PDF input required:** validate that `working_paper.source_uri` is present and non-empty in the `working_paper_input` artifact.
- **Line numbers present:** validate that `working_paper.has_line_numbers` is `true` (or warn if absent) before applying line-based anchoring.
- **Page anchor present:** every generated comment must have a non-blank `page` value in the `location` object.
- **Line anchor format:** when `line` is non-blank, it must match one of the allowed formats: single number (`\d+`), range (`\d+-\d+`), or non-contiguous list (`\d+(?:, \d+)+`). Reject paragraph-based references.
- **No fabricated line numbers:** if a line number cannot be determined from the PDF, the `line` field must be blank; comments must not use inferred positions.
- **Section anchor derived from PDF headings:** the `section` value must correspond to a visible heading in the PDF, not invented numbering.

## Canonical Contract Compliance

- **Exact 13 columns:** the exported spreadsheet must contain exactly the 13 canonical columns from the spectrum-systems contract — no more, no fewer.
- **Header names are exact:** each header must match the canonical text exactly, including casing, spacing, and punctuation (e.g., `Comment Type: Editorial/Grammar, Clarification, Technical`).
- **Header order is fixed:** columns must appear in the canonical order; reordering is a contract violation.
- **Sheet name is canonical:** the visible sheet must be named `Comment Resolution Matrix`.
- **No extra visible columns:** metadata (provenance IDs, confidence scores, heat levels) must not appear as visible spreadsheet columns; they travel in sidecar JSON files.
- **Comment Type values:** every non-blank `Comment Type` value must be one of `Editorial/Grammar`, `Clarification`, `Technical`.
- **Adjudication columns blank at review time:** NTIA Comments, Comment Disposition, and Resolution may be blank on reviewer-generated rows; they are populated during adjudication.

## Golden Example: Numbered PDF → Canonical Matrix

The following trace shows the minimal path from a numbered PDF input to a valid canonical matrix row.

**Input (working_paper_input):**
```json
{
  "artifact_type": "working_paper_input",
  "working_paper": {
    "paper_id": "wp-2024-001",
    "revision": "DRAFT-1",
    "source_uri": "s3://spec/working-papers/wp-2024-001-draft.pdf",
    "has_line_numbers": true
  }
}
```

**Generated review comment (internal):**
```json
{
  "section": "2.3",
  "page": "5",
  "line": "14-18",
  "comment_type": "Technical",
  "comment_text": "Propagation model assumptions are underspecified; free-space loss only.",
  "suggested_revision": "Add clutter and diffraction loss terms with cited reference model."
}
```

**Canonical matrix row (exported):**
```csv
Comment Number,Reviewer Initials,Agency,Report Version,Section,Page,Line,Comment Type: Editorial/Grammar, Clarification, Technical,Agency Notes,Agency Suggested Text Change,NTIA Comments,Comment Disposition,Resolution
1,NTIA,NTIA,DRAFT-1,2.3,5,14-18,Technical,Propagation model assumptions are underspecified; free-space loss only.,Add clutter and diffraction loss terms with cited reference model.,,,
```

**Pass criteria for this example:**
- `source_uri` is present in the input artifact ✓
- `has_line_numbers` is `true` ✓
- Row has exactly 13 columns ✓
- Header names match canonical text exactly ✓
- `Line` field contains a valid range reference ✓
- `Comment Type` is `Technical` (a valid canonical value) ✓
- Adjudication columns (NTIA Comments, Comment Disposition, Resolution) are blank ✓
- No extra visible columns ✓

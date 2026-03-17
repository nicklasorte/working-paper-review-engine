# PDF-to-Matrix Interface

This document explains the end-to-end interface from a numbered PDF working paper to the canonical 13-column Comment Resolution Matrix.

## 1. Input PDF

**Required:** a PDF working paper with **visible line numbers printed on the left margin of each page**.

The `working_paper_input` artifact must include:

```json
{
  "working_paper": {
    "paper_id": "wp-2024-001",
    "revision": "DRAFT-1",
    "source_uri": "s3://path/to/numbered-paper.pdf",
    "has_line_numbers": true
  }
}
```

- `source_uri` is **required** (not optional).
- `has_line_numbers: true` activates the line-anchor contract. Set to `false` only when the PDF lacks left-margin line numbers; in that case the engine falls back to page+section anchors and leaves `Line` blank.
- Multiple PDF revisions are supported across runs by changing `revision` (e.g., `rev1`, `rev2`). Each revision creates a separate `working_paper_input` artifact.

## 2. Anchor Extraction Model

The anchor for each review comment is a three-part reference extracted from the numbered PDF:

| Field | Source | Required |
|-------|--------|----------|
| `Section` | Visible section heading in the PDF | When identifiable |
| `Page` | PDF page number | Always |
| `Line` | Left-margin line number printed on the PDF page | When `has_line_numbers: true` |

### Line reference rules

- **Source:** the line number visible on the left margin of the PDF page — not inferred from paragraph position, sentence index, or word count.
- **Allowed formats:**
  - Single line: `42`
  - Contiguous range: `42-45`
  - Non-contiguous: `42, 46`
- **Uncertain line:** if the line number cannot be determined, leave the field blank. Do not use paragraph counters or approximate positions as substitutes.
- **Span across pages:** use the Page field for the starting page; note continuation in Agency Notes if needed.

### Anchor hierarchy

1. Section + Page + Line (preferred, when line numbers are present and visible)
2. Section + Page (fallback when line is unresolvable)
3. Page only (last resort — must note missing section in Agency Notes)

### Known limitation

Automated extraction of left-margin line numbers from PDFs may fail if the PDF is scanned, uses non-standard fonts, or has complex layouts. When extraction is uncertain, the engine must document the limitation in `Agency Notes` and leave `Line` blank rather than recording a fabricated value.

## 3. Internal Comment Object

Before export, each comment is represented as an internal `review_comment` object (schema: `schemas/review_comment.schema.json`). Key fields:

```json
{
  "comment_id": "comment-1",
  "reviewer_persona_id": "NTIA engineer",
  "reviewer_initials": "NTIA",
  "agency": "NTIA",
  "section_id": "2.3",
  "page_reference": "5",
  "line": "14-18",
  "anchor_text": "Path loss modeled as 20log10(d) with no additional factors.",
  "comment_category": "technical sufficiency",
  "comment_type": "Technical",
  "comment_text": "Propagation model assumptions are underspecified.",
  "rationale": "Anchored to p.5 lines 14-18; free-space loss only cited.",
  "severity": "major",
  "suggested_revision": "Add clutter and diffraction loss terms with cited reference model.",
  "confidence": 0.85,
  "source_run_id": "review-run-001"
}
```

### Internal → canonical field mapping

| Internal field | Canonical matrix column |
|---------------|------------------------|
| `comment_number` | Comment Number |
| `reviewer_initials` | Reviewer Initials |
| `agency` | Agency |
| `report_version` | Report Version |
| `section_id` | Section |
| `page_reference` | Page |
| `line` | Line |
| `comment_type` | Comment Type: Editorial/Grammar, Clarification, Technical |
| `comment_text` | Agency Notes |
| `suggested_revision` | Agency Suggested Text Change |
| `rationale` | NTIA Comments |
| `comment_disposition` | Comment Disposition |
| `resolution` | Resolution |

Internal metadata fields (confidence, heat_level, provenance_record_id, etc.) are **not** written to visible spreadsheet columns. They travel in the `reviewer_comment_set` sidecar JSON.

## 4. Canonical Matrix Export

The final export is the **canonical 13-column Comment Resolution Matrix** governed by `spectrum-systems`.

- Schema: `contracts/spectrum-systems/comment_resolution_matrix_spreadsheet_contract.schema.json`
- Format: XLSX (primary) or CSV (secondary)
- Sheet name: `Comment Resolution Matrix`
- Headers: exactly the 13 canonical headers in fixed order (see below)
- No extra visible columns

### Canonical headers (immutable order)

```
1.  Comment Number
2.  Reviewer Initials
3.  Agency
4.  Report Version
5.  Section
6.  Page
7.  Line
8.  Comment Type: Editorial/Grammar, Clarification, Technical
9.  Agency Notes
10. Agency Suggested Text Change
11. NTIA Comments
12. Comment Disposition
13. Resolution
```

### Completion semantics

- **Open:** Comment Disposition is blank or `Pending`.
- **Completed:** Comment Disposition is in `{Accepted, Partially Accepted, Rejected, Out of Scope}` **and** Resolution is non-blank.
- The engine generates reviewer-side rows (columns 1-10 populated, columns 11-13 blank or minimal). Adjudication systems populate columns 11-13.

## 5. Sidecar Artifacts

The following sidecar JSON files travel with the spreadsheet and carry machine metadata excluded from the visible sheet:

| File | Contents |
|------|----------|
| `reviewer_comment_set_sample.json` | Full `reviewer_comment_set` artifact with confidence, heat level, provenance |
| `provenance_record_sample.json` | Run bindings: input artifacts, output artifacts, timestamps, source repo |
| `working_paper_input_sample.json` | Input metadata: paper_id, revision, source_uri, has_line_numbers |
| `standards_manifest_sample.json` | Contract versions and compatibility target |

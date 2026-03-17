# Working Paper Review Engine

System-spec repository that defines how the Working Paper Review Engine should operate before implementation. The engine ingests a numbered PDF working paper and produces a structured comment resolution matrix aligned to defined reviewer personas, keeping comments anchored to the document and export-ready for downstream systems.

## Problem Statement
Working papers often circulate without rigorous, structured review. Feedback is ad hoc, unanchored to document evidence, and hard to aggregate. We need a deterministic, persona-driven review process that surfaces likely issues early and exports comments in machine-consumable form aligned to the canonical Comment Resolution Matrix.

## What This System Does
- Defines contracts, schemas, prompts, and workflows for generating anchored review comment matrices from numbered PDF working papers.
- Specifies reviewer personas and comment taxonomy to keep outputs consistent and auditable.
- Provides examples, evaluation criteria, and export formats for downstream consumers.
- Shapes exports into the **canonical 13-column Comment Resolution Matrix** governed by `spectrum-systems`, so downstream resolution workflows ingest them without additional transformation.

## What It Does Not Do Yet
- No executable application code or PDF parsing implementation is included.
- No model hosting or prompt chaining logic.
- No UI, API, or deployment assets.

## Why This System Exists
- Create a shared spec for builders and evaluators before coding starts.
- Ensure review comments are grounded in document evidence and persona intent.
- Enable downstream systems (resolution, study artifact generation) to rely on stable contracts and exports.

## Required Input

**The required input is a numbered PDF working paper.**

- The PDF must have **visible line numbers printed on the left margin of each page**.
- These left-margin line numbers are part of the review anchor contract: every generated comment must cite the page and the left-margin line number(s) for its anchor.
- A single numbered PDF is the required baseline input for one review run.
- Multiple PDF revisions may be supplied across runs; each revision creates a distinct `working_paper_input` artifact with its own `revision` tag.

Other inputs:
- Selected reviewer personas (e.g., federal technical, FCC/regulatory, industry/CTIA-style)
- Optional review rubric or lens
- Optional prior revision metadata or known issues

## Anchor Model

Comments are anchored to the working paper using a three-part reference system derived directly from the numbered PDF:

| Anchor | Source | Notes |
|--------|--------|-------|
| **Section** | Visible section heading in the PDF (e.g., "2.3", "3. Guard Band Analysis") | Required when identifiable |
| **Page** | Page number of the PDF | Required |
| **Line** | Left-margin line number printed on the PDF page | Required when visible; omit rather than fabricate |

**Line reference formats:**
- Single line: `42`
- Contiguous range: `42-45`
- Non-contiguous: `42, 46`

**When line number is uncertain:** provide page and section if possible; leave the Line field blank; never use inferred paragraph counters or sentence positions as substitutes for printed line numbers.

**Anchor hierarchy:** Section + Page + Line is the default. When line numbers are absent from the PDF (`has_line_numbers: false`), fall back to Section + Page only, and note the limitation.

## Planned Outputs

**The final output is the canonical Comment Resolution Matrix from `spectrum-systems`.**

- Format: XLSX (primary) or CSV (secondary)
- Sheet name: `Comment Resolution Matrix`
- Columns: exactly the 13 canonical headers in fixed order (see [Contract Alignment](#contract-alignment))
- Adjudication columns (NTIA Comments, Comment Disposition, Resolution) are present but blank at review time
- No extra visible columns; metadata travels in sidecar JSON files

Other outputs:
- `reviewer_comment_set` canonical artifact (primary provenance deliverable)
- `provenance_record` canonical artifact (auditability)
- Run manifest with run_id, timestamps, and configuration

## Core Architecture Concept
1. Ingest numbered PDF and map document structure (sections, page ranges, line number presence).
2. Apply reviewer persona and rubric to generate anchored comments tied to section, page, and left-margin line number.
3. Classify each comment as `Technical`, `Clarification`, or `Editorial/Grammar`.
4. Deduplicate and normalize comments into a deterministic matrix.
5. Export the 13-column matrix and run manifest for downstream consumers.

## Repo Structure
- `docs/` — architecture notes, personas, taxonomy, workflows, PDF-to-matrix interface
- `schemas/` — JSON Schemas for comments, personas, document structure, run manifests, exports
- `prompts/` — prompt contracts for system and personas
- `contracts/spectrum-systems/` — canonical contract snapshots from `spectrum-systems`
- `evals/` — evaluation criteria and harness notes
- `examples/` — sample inputs/outputs and guidance
- `SYSTEMS.md` — system registry entry
- `CLAUDE.md`, `CODEX.md`, `AGENTS.md` — agent instructions for working in this repo

## Design Principles
- Schema-first and contract-first before code.
- Deterministic, anchored outputs over free-form prose.
- Evidence-backed comments only; no ungrounded assertions.
- Clean, export-ready artifacts (CSV/JSON/Markdown hygiene).
- Additive, auditable edits; avoid silent renames or contract drift.

## Near-Term Roadmap
- Finalize schemas for comments, personas, paper structure, and exports.
- Flesh out persona-specific prompts and guardrails.
- Add gold examples and baseline evaluation harness shape.
- Define PDF structure extraction expectations for future implementation repo.
- Document interfaces to downstream Comment Resolution and Study Artifact systems.

## Contract Alignment

The canonical 13-column headers (governed exclusively by `spectrum-systems`, immutable order):

1. Comment Number
2. Reviewer Initials
3. Agency
4. Report Version
5. Section
6. Page
7. Line
8. Comment Type: Editorial/Grammar, Clarification, Technical
9. Agency Notes
10. Agency Suggested Text Change
11. NTIA Comments
12. Comment Disposition
13. Resolution

- Canonical artifact contracts are governed by the `spectrum-systems` repository; this repo consumes them and does not redefine them.
- Contracts consumed: `working_paper_input` and `standards_manifest`.
- Contracts produced: `reviewer_comment_set` and `provenance_record`, plus a Comment Resolution Engine-compatible matrix export.
- Machine-readable declaration: `contracts/contract_declaration.json`; schemas are snapshotted in `contracts/spectrum-systems/`.
- Spreadsheet contract snapshot: `contracts/spectrum-systems/comment_resolution_matrix_spreadsheet_contract.schema.json`.
- Example artifacts live in `examples/contracts/` and are validated before export.

## Comment Matrix Export
- Default CLI flag `--output-format comment-matrix` emits the canonical 13-column comment resolution matrix (XLSX by default; CSV optional).
- Schema: `schemas/comment_matrix_export.schema.json` defines the canonical 13-column structure.
- Sample artifact: `outputs/examples/comment_matrix_sample.xlsx` (CSV variant alongside) demonstrates the exact contract.
- Sheet name: `Comment Resolution Matrix` (required by the spectrum-systems spreadsheet contract).

## Relationship to Sibling Systems
- **Comment Resolution Engine:** downstream consumer of the review comment matrix; resolves and tracks comment closure.
- **Study Artifact Generator:** consumes resolved comments and paper structure to produce study artifacts.
- **Transcript-to-Issue Engine:** supplies additional issues that can be merged into the comment matrix.

This repository stays spec-first. Implementation code will live in a separate repo once contracts stabilize.

# Systems Registry

Design registry for spectrum and document-review automation systems. Entries are implementation-agnostic and focus on purpose, inputs, outputs, workflows, schemas, and evaluation needs before code exists.

## Primary System: Working Paper Review Engine

- **Purpose:** Ingest a working paper PDF and generate a structured comment matrix from selected reviewer personas, with every comment anchored to the source document.
- **Status:** Spec-first (this repository). No executable application code yet.
- **Initial Capabilities:**
  - PDF ingestion expectations and structure mapping (sections, tables, figures, footnotes, recommendations).
  - Persona- and rubric-driven comment generation with anchors, categories, rationale, severity, and suggested revisions.
  - Deduplication/normalization into deterministic comment matrices.
  - Export contracts for CSV/XLSX-compatible tables and run manifests.
- **Inputs:** Working paper PDF (required); selected reviewer personas; optional review rubric/lens; optional prior revision metadata.
- **Outputs:** Structured comment matrix; comment records with anchors; run manifest with provenance/config; export-ready tables; summary statistics.
- **Contracts:** `schemas/review_comment.schema.json`, `schemas/reviewer_persona.schema.json`, `schemas/working_paper_structure.schema.json`, `schemas/review_run_manifest.schema.json`, `schemas/comment_matrix_export.schema.json`.
- **Evaluation Themes:** Anchor accuracy, duplication rate, actionability, persona fidelity, hallucination/false-issue rate, export completeness, comparison to historical comments when available.
- **Downstream Consumers:** Comment Resolution Engine (resolves/triages comments), Study Artifact Generator, evaluation harnesses.

## System Family Relationships

- Working Paper Review Engine is upstream of Comment Resolution Engine; the review engine generates structured, anchored comments and the resolution engine consumes them.
- Comment Resolution Engine feeds decisions back to Study Artifact Generator and other downstream systems.

## Other Tracked Systems (directional)
- Transcript-to-Issue Engine
- Study Artifact Generator
- Spectrum Decision Engine
- Institutional Knowledge Engine

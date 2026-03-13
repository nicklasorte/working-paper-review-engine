# Architecture Overview

## System Boundary
- This repository defines contracts, schemas, prompts, and workflows for the Working Paper Review Engine.
- No application runtime, model orchestration, or PDF parsing code lives here; those belong in the future implementation repo.
- All outputs must be export-ready and align to published schemas.

## Upstream Dependencies
- Working paper PDF (canonical source document).
- Optional metadata: revision history, authorship, intended audience, known issues.
- Selected reviewer personas and optional rubric definitions.

## Downstream Dependencies
- Comment Resolution Engine (consumes structured comment matrix).
- Study Artifact Generator (consumes resolved comments and document structure).
- Evaluation harnesses for regression and persona fidelity checks.

## Conceptual Pipeline
1. Ingest PDF and extract structure: sections, tables, figures, footnotes, recommendations.
2. Map stable identifiers for sections and anchors (page/paragraph/element references).
3. Apply selected reviewer personas and review rubric to generate comments.
4. Ground each comment to anchor text or document element IDs; reject unanchored output.
5. Normalize, deduplicate, and categorize comments into a deterministic matrix.
6. Produce run manifest and export-ready files (CSV/XLSX/JSON).

## Artifact Flow
- **Inputs:** PDF + persona selection + optional rubric/metadata.
- **Intermediate artifacts:** structured document map, comment drafts, normalization decisions.
- **Outputs:** comment matrix (anchored), run manifest, export tables, evaluation summaries.

## Separation of Concerns
- **Spec repo (this):** schemas, prompts, personas, taxonomy, workflows, evaluation criteria, examples.
- **Implementation repo (future):** PDF parsing, model calls, storage, APIs, UI/CLI, and deployment.
- Contracts defined here should remain stable; implementation changes should not break published schemas without explicit versioning.

## Anchoring Requirement
- Every comment must reference concrete document evidence: anchor text, section ID, page/paragraph/figure/footnote identifiers, or structured element IDs.
- Unanchored comments should be rejected or flagged during generation and evaluation.

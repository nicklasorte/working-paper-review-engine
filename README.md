# Working Paper Review Engine

System-spec repository that defines how the Working Paper Review Engine should operate before implementation. The engine ingests a working paper PDF and produces a structured comment matrix aligned to defined reviewer personas, keeping comments anchored to the document and export-ready for downstream systems.

## Problem Statement
Working papers often circulate without rigorous, structured review. Feedback is ad hoc, unanchored to document evidence, and hard to aggregate. We need a deterministic, persona-driven review process that surfaces likely issues early and exports comments in machine-consumable form.

## What This System Does
- Defines contracts, schemas, prompts, and workflows for generating anchored review comment matrices from working paper PDFs.
- Specifies reviewer personas and comment taxonomy to keep outputs consistent and auditable.
- Provides examples, evaluation criteria, and export formats for downstream consumers.
- Shapes exports into the Comment Resolution Engine comment-matrix contract so downstream resolution workflows ingest them without additional transformation.

## What It Does Not Do Yet
- No executable application code or PDF parsing implementation is included.
- No model hosting or prompt chaining logic.
- No UI, API, or deployment assets.

## Why This System Exists
- Create a shared spec for builders and evaluators before coding starts.
- Ensure review comments are grounded in document evidence and persona intent.
- Enable downstream systems (resolution, study artifact generation) to rely on stable contracts and exports.

## Example Use Cases
- Pre-publication stress-test of a spectrum engineering working paper.
- Interagency review preparation with regulatory and industry personas.
- Generating training/eval data for a Comment Resolution Engine.
- Comparing persona-specific feedback on the same draft to locate consensus gaps.

## Planned Inputs
- Working paper PDF (required)
- Selected reviewer personas (e.g., federal technical, FCC/regulatory, industry/CTIA-style)
- Optional review rubric or lens
- Optional prior revision metadata or known issues

## Planned Outputs
- Structured comment matrix with anchors, categories, rationale, severity, and suggested revisions
- Comment Resolution Engine-compatible comment-matrix exports (XLSX primary, CSV secondary)
- Run manifest with provenance and configuration
- Summary statistics for the review run

## Core Architecture Concept
1. Ingest PDF and map document structure (sections, tables, figures, footnotes, recommendations).
2. Apply reviewer persona and rubric to generate anchored comments tied to exact text or locations.
3. Deduplicate and normalize comments into a deterministic matrix.
4. Export the matrix and run manifest for downstream consumers.

## Architecture Position

This engine sits in the **review-generation** layer of the spectrum ecosystem. It is governed by the `spectrum-systems` repository, which holds canonical artifact contracts. Sibling engines that depend on its outputs include the **Comment Resolution Engine** (primary downstream consumer) and the **Study Artifact Generator**.

Quick-reference normalization record: [`docs/repo-standardization-summary.md`](docs/repo-standardization-summary.md).

## Repo Structure
- `governance/` — machine-readable governance declaration and system metadata
- `docs/` — architecture notes, personas, taxonomy, workflows, standardization summary
- `schemas/` — JSON Schemas for comments, personas, document structure, run manifests, exports
- `prompts/` — prompt contracts for system and personas
- `evals/` — evaluation manifest, criteria, and harness notes
- `examples/` — sample inputs/outputs and guidance
- `contracts/` — canonical contract snapshots from `spectrum-systems`; local `contract_declaration.json`
- `tests/` — Python unittest suite (run with `PYTHONPATH=src python -m unittest discover tests/`)
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
- Canonical artifact contracts are governed by the `spectrum-systems` repository; this repo consumes them and does not redefine them.
- Contracts consumed: `working_paper_input` and `standards_manifest`.
- Contracts produced: `reviewer_comment_set` and `provenance_record`, plus a Comment Resolution Engine-compatible matrix export.
- Machine-readable declaration: `contracts/contract_declaration.json`; schemas are snapshotted in `contracts/spectrum-systems/`.
- Example artifacts live in `examples/contracts/` and are validated before export.

## Governance
- Governance declaration: `governance/governance-declaration.json` — machine-readable record of contract pins, schema pins, rule version, and evaluation manifest path.
- System metadata: `governance/system-metadata.json` — repo type, architecture layer, upstream/downstream relationships.
- Evaluation manifest: `evals/eval-manifest.json` — evaluation dimensions and evidence output path.

## Comment Matrix Export
- Default CLI flag `--output-format comment-matrix` emits the comment-matrix contract (XLSX by default; CSV optional) derived from the canonical reviewer comment set.
- Schema: `schemas/comment_matrix_export.schema.json` defines the column order required by the Comment Resolution Engine.
- Sample artifact: `outputs/examples/comment_matrix_sample.xlsx` (CSV variant alongside) demonstrates the exact contract.

## Relationship to Sibling Systems
- **Comment Resolution Engine:** downstream consumer of the review comment matrix; resolves and tracks comment closure.
- **Study Artifact Generator:** consumes resolved comments and paper structure to produce study artifacts.
- **Transcript-to-Issue Engine:** supplies additional issues that can be merged into the comment matrix.

This repository stays spec-first. Implementation code will live in a separate repo once contracts stabilize.

# Spectrum Systems

Design notebook for automation systems that move spectrum engineering workflows from document-driven steps to computation-driven contracts. Each system entry is implementation-agnostic and focuses on purpose, inputs, outputs, workflows, schemas, and evaluation needs before any code exists.

## Initial Target Systems

- Working Paper Review Engine
- Comment Resolution Engine
- Transcript-to-Issue Engine
- Study Artifact Generator
- Spectrum Decision Engine
- Institutional Knowledge Engine

_Relationship note: The Working Paper Review Engine is upstream of the Comment Resolution Engine; the review engine generates structured comments and the resolution engine consumes them._

## Working Paper Review Engine

**System Name**  
Working Paper Review Engine

**Purpose**  
Ingest a working paper PDF and generate a structured comment matrix that simulates review comments from selected stakeholder perspectives.

**Why It Exists**
- Support pre-review before circulation
- Stress-test working papers before interagency or public-facing review
- Surface likely technical, policy, regulatory, reproducibility, and clarity issues early
- Generate training/evaluation data for downstream comment-resolution systems

**Primary Inputs**
- Working paper PDF (required)
- Optional reviewer persona selection
- Optional evaluation rubric / review lens
- Optional prior revision metadata

**Primary Outputs**
- Structured comment matrix
- Comment records with anchor text, section references, reviewer persona, category, rationale, severity, and suggested revision
- Export-ready CSV/XLSX-compatible review table
- Review summary statistics

**Core Workflow**
- Parse PDF and extract document structure
- Segment by section / table / figure / footnote / recommendation
- Apply selected reviewer persona and review rubric
- Generate anchored comments tied to exact text or document regions
- Deduplicate / normalize comments
- Export deterministic review matrix

**Reviewer Personas**
- Federal technical reviewer
- FCC / regulatory reviewer
- Industry / CTIA-style reviewer
- Leave room for future personas

**Required Schemas / Contracts**
- `review_comment.schema.json`
- `reviewer_persona.schema.json`
- `working_paper_structure.schema.json`
- `review_run_manifest.schema.json`
- `comment_matrix_export.schema.json`

**Evaluation / Validation**
- Anchor accuracy: each comment must tie to real text
- Duplication rate
- Actionability
- Persona fidelity
- False-issue / hallucination rate
- Comparison against historical real comments when available

**Downstream Dependencies**
- Comment Resolution Engine
- Study Artifact Generator
- Evaluation harnesses
- Prompt templates
- Schema library

**Future Implementation Repo(s)**
- working-paper-review-engine
- agency-comment-engine

# Repo Standardization Summary

**System ID:** `working-paper-review-engine`
**Repo Type:** operational-engine
**Architecture Layer:** review-generation
**Governance Source:** `spectrum-systems`

---

## Contracts Consumed

| Artifact Type | Version | Schema Path |
|---|---|---|
| `working_paper_input` | 1.0.0 | `contracts/spectrum-systems/working_paper_input.schema.json` |
| `standards_manifest` | 1.0.0 | `contracts/spectrum-systems/standards_manifest.schema.json` |

## Contracts Produced

| Artifact Type | Version | Schema Path |
|---|---|---|
| `reviewer_comment_set` | 1.0.0 | `contracts/spectrum-systems/reviewer_comment_set.schema.json` |
| `provenance_record` | 1.0.0 | `contracts/spectrum-systems/provenance_record.schema.json` |

Secondary output: `comment_matrix_export` (XLSX/CSV) governed by `schemas/comment_matrix_export.schema.json`.

---

## Evaluation Status

- **Evaluation manifest:** `evals/eval-manifest.json` (scaffold; full harness pending)
- **Gold examples:** `examples/contracts/*.sample.json`
- **Evaluation criteria:** `evals/eval-criteria.md`
- **Last formal evaluation:** not yet run

Evaluation dimensions defined: anchor accuracy, actionability, duplication rate, persona fidelity, hallucination rate, export completeness, schema validation.

## Evidence Status

- **Run evidence path:** `outputs/eval-evidence/` (scaffold; populated on harness runs)
- **Sample outputs:** `outputs/examples/comment_matrix_sample.{xlsx,csv}`
- **Provenance record:** emitted per run as `provenance_record` artifact binding inputs, outputs, and timestamps

---

## Directory Mapping

| Standard Pattern | This Repo | Notes |
|---|---|---|
| `governance/` | `governance/` | Added in standardization pass |
| `contracts/` | `contracts/` | Canonical snapshots under `contracts/spectrum-systems/` |
| `examples/` | `examples/` | Input/output samples under `examples/contracts/` and `examples/sample-{inputs,outputs}/` |
| `eval/` | `evals/` | Different name; `evals/eval-manifest.json` tracks dimensions |
| `tests/` | `tests/` | Python unittest; run with `PYTHONPATH=src python -m unittest discover tests/` |
| `docs/` | `docs/` | Architecture, personas, taxonomy, workflow |
| Implementation code | `src/working_paper_review_engine/` | Spec-first; minimal contract + export code only |

---

## Maturity Notes

- Repository is **spec-first**. Schemas, contracts, prompts, and workflows are stable; application runtime (PDF parsing, LLM integration) is not yet implemented.
- All four canonical contracts are locally snapshotted and validated against example artifacts.
- CI workflow (`validate.yml`) runs governance validation and full test suite on every push/PR.
- Governance declaration and system metadata are machine-readable and cross-reference `spectrum-systems` as authority.

---

## Known Deviations from Standard Engine Pattern

| Deviation | Notes |
|---|---|
| No executable runtime | By design; spec-first phase. Implementation will live in a separate repo. |
| `evals/` not `eval/` | Directory name differs from some sibling engines; documented here. |
| No `pyproject.toml` / `setup.py` | Package installed via `PYTHONPATH=src`; acceptable for spec-first repo. |
| `last_evaluation_date` is `null` | No formal evaluation run yet; update when first harness run completes. |
| `prompt_set_hash` is a path list | Stored as canonical file list rather than hash; replace with SHA-256 hash when prompts stabilize. |

---

## Recommended Next Repo to Standardize

**`comment-resolution-engine`** — it is the primary downstream consumer of artifacts produced by this engine and the most natural next node to normalize in the same pass.

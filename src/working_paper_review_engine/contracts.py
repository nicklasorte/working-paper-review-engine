from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, MutableMapping, Sequence

from jsonschema import Draft202012Validator

REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRACTS_DIR = REPO_ROOT / "contracts"
SCHEMA_DIR = CONTRACTS_DIR / "spectrum-systems"
EXAMPLES_DIR = REPO_ROOT / "examples" / "contracts"

SCHEMA_MAP: Mapping[str, str] = {
    "working_paper_input": "working_paper_input.schema.json",
    "standards_manifest": "standards_manifest.schema.json",
    "reviewer_comment_set": "reviewer_comment_set.schema.json",
    "provenance_record": "provenance_record.schema.json",
}

DEFAULT_ARTIFACT_VERSION = "1.0.0"
DEFAULT_SCHEMA_VERSION = "1.0.0"
DEFAULT_STANDARDS_VERSION = "2025.03-draft"
DEFAULT_PROVENANCE_ID = "prov-review-run-sample-001"


def load_contract_declaration() -> Mapping[str, Any]:
    path = CONTRACTS_DIR / "contract_declaration.json"
    with path.open() as handle:
        return json.load(handle)


def load_schema(artifact_type: str) -> Mapping[str, Any]:
    if artifact_type not in SCHEMA_MAP:
        raise ValueError(f"Unsupported artifact type for canonical validation: {artifact_type}")
    path = SCHEMA_DIR / SCHEMA_MAP[artifact_type]
    with path.open() as handle:
        return json.load(handle)


def validate_artifact(artifact: Mapping[str, Any], artifact_type: str) -> None:
    schema = load_schema(artifact_type)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(artifact), key=lambda error: error.path)
    if errors:
        error = errors[0]
        location = " -> ".join(str(part) for part in error.path)
        pointer = f"{artifact_type}: {location}" if location else artifact_type
        raise ValueError(f"{pointer} failed validation: {error.message}")


def load_example_artifact(name: str) -> Mapping[str, Any]:
    path = EXAMPLES_DIR / f"{name}.sample.json"
    with path.open() as handle:
        return json.load(handle)


def build_reviewer_comment_set(
    comments: Sequence[Mapping[str, Any]],
    working_paper_input: Mapping[str, Any],
    review_run_id: str,
    *,
    standards_manifest_ref: str,
    artifact_version: str = DEFAULT_ARTIFACT_VERSION,
    schema_version: str = DEFAULT_SCHEMA_VERSION,
    standards_version: str = DEFAULT_STANDARDS_VERSION,
    provenance_record_id: str = DEFAULT_PROVENANCE_ID,
    source: str = "working-paper-review-engine",
) -> MutableMapping[str, Any]:
    working_paper = working_paper_input.get("working_paper", {})
    paper_id = working_paper.get("paper_id", "")
    paper_revision = working_paper.get("revision", "")

    normalized_comments = []
    for idx, comment in enumerate(comments, start=1):
        location = comment.get("location", {}) or {}
        normalized_comments.append(
            {
                "comment_id": comment.get("comment_id") or f"comment-{idx}",
                "comment_number": comment.get("comment_number", idx),
                "reviewer_persona_id": comment.get("reviewer_persona_id")
                or comment.get("persona_name")
                or "reviewer",
                "comment_text": comment.get("comment_text")
                or comment.get("text")
                or comment.get("agency_notes")
                or "",
                "suggested_revision": comment.get("suggested_revision")
                or comment.get("suggested_action")
                or comment.get("agency_suggested_text_change")
                or "",
                "rationale": comment.get("rationale") or "",
                "category": comment.get("category") or comment.get("intent_classification") or "",
                "severity": comment.get("severity") or comment.get("heat_level") or "",
                "status": comment.get("status") or comment.get("review_status") or "PROPOSED",
                "location": {
                    "section": location.get("section") or comment.get("section_id") or "",
                    "page": location.get("page") or comment.get("page_reference") or "",
                    "line": location.get("line") or comment.get("line_reference") or "",
                    "anchor_text": location.get("anchor_text") or comment.get("anchor_text") or "",
                },
                "working_paper_references": {
                    "paper_id": paper_id,
                    "revision": paper_revision,
                },
                "trace": {
                    "provenance_record_id": provenance_record_id,
                    "source": source,
                    "standards_version": standards_version,
                    "run_id": review_run_id,
                },
            }
        )

    return {
        "artifact_type": "reviewer_comment_set",
        "artifact_version": artifact_version,
        "schema_version": schema_version,
        "standard_source": "spectrum-systems",
        "review_run_id": review_run_id,
        "working_paper_id": paper_id,
        "working_paper_revision": paper_revision,
        "standards_manifest_ref": standards_manifest_ref,
        "comments": normalized_comments,
        "metadata": {
            "format": "reviewer_comment_set",
            "reviewer_personas": list({c["reviewer_persona_id"] for c in normalized_comments}),
        },
    }


def build_provenance_record(
    reviewer_comment_set: Mapping[str, Any],
    working_paper_input: Mapping[str, Any],
    standards_manifest_ref: str,
    *,
    artifact_version: str = DEFAULT_ARTIFACT_VERSION,
    schema_version: str = DEFAULT_SCHEMA_VERSION,
    standards_version: str = DEFAULT_STANDARDS_VERSION,
    source_repo: str = "working-paper-review-engine",
    source_repo_version: str = "spec-only",
    comment_matrix_path: str | None = None,
    started_at: str | None = None,
    completed_at: str | None = None,
) -> MutableMapping[str, Any]:
    now = datetime.now(timezone.utc).isoformat()
    run_id = reviewer_comment_set["review_run_id"]
    working_paper = working_paper_input.get("working_paper", {})
    paper_id = working_paper.get("paper_id", "")
    paper_revision = working_paper.get("revision", "")

    return {
        "artifact_type": "provenance_record",
        "artifact_version": artifact_version,
        "schema_version": schema_version,
        "standard_source": "spectrum-systems",
        "run_id": run_id,
        "working_paper_id": paper_id,
        "working_paper_revision": paper_revision,
        "standards_manifest_ref": standards_manifest_ref,
        "input_artifacts": {
            "working_paper_input_ref": paper_id,
            "standards_manifest_ref": standards_manifest_ref,
        },
        "generated_artifacts": {
            "reviewer_comment_set_ref": f"{run_id}#reviewer_comment_set",
            "comment_matrix_export": comment_matrix_path or "",
        },
        "timestamps": {
            "started_at": started_at or now,
            "completed_at": completed_at or now,
        },
        "source_repo": source_repo,
        "source_repo_version": source_repo_version,
        "tool_metadata": {
            "standards_version": standards_version,
        },
    }


def write_json(path: Path, payload: Mapping[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))
    return path

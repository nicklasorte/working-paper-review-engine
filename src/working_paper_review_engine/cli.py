from __future__ import annotations

import argparse
from pathlib import Path
from typing import Mapping, Sequence

from .output_contract import (
    DEFAULT_OUTPUT_FORMAT,
    export_comment_matrix,
    rows_from_comments,
    ensure_supported_format,
)
from .contracts import (
    build_provenance_record,
    build_reviewer_comment_set,
    load_example_artifact,
    validate_artifact,
    write_json,
)

SAMPLE_RUN_ID = "review-run-sample-001"
SAMPLE_STANDARDS_REF = "spectrum-systems/standards-manifest@2025.03-draft"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="working-paper-review-engine",
        description="Shape working paper review comments into the comment-matrix contract.",
    )
    parser.add_argument(
        "--output-format",
        default=DEFAULT_OUTPUT_FORMAT,
        choices=["comment-matrix", "comment-matrix-xlsx", "comment-matrix-csv"],
        help="Output format compatible with the Comment Resolution Engine comment-matrix contract. Default is comment-matrix (XLSX).",
    )
    parser.add_argument(
        "--output-path",
        type=Path,
        help="Path to write the export. Defaults to outputs/examples/comment_matrix_sample.{csv|xlsx}.",
    )
    parser.add_argument(
        "--sample",
        action="store_true",
        help="Emit a deterministic sample matrix row to validate the contract.",
    )
    return parser


def render_sample_comments() -> Sequence[dict]:
    return [
        {
            "comment_number": 1,
            "reviewer_persona_id": "NTIA engineer",
            "comment_text": "Clarify the propagation model assumptions in Section 2.3; current text implies free-space losses only.",
            "suggested_revision": "Specify whether clutter and diffraction losses are included in the link budget.",
            "rationale": "Anchored to p.5 para 2: the working paper cites path loss without environment class.",
            "location": {
                "section": "2.3",
                "page": "5",
                "line": "14-18",
                "anchor_text": "Path loss modeled as 20log10(d) with no additional factors.",
            },
            "comment_disposition": "For consideration",
            "resolution": "Update Section 2.3 to include environmental loss factors and cite reference model.",
            "confidence": 0.78,
            "heat_level": "major",
            "category": "clarity",
            "status": "PROPOSED",
        }
    ]


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    export_kind = ensure_supported_format(args.output_format)
    default_name = f"comment_matrix_sample.{export_kind}"
    output_path = args.output_path or Path("outputs/examples") / default_name

    if not args.sample:
        parser.error("No action specified. Use --sample to emit a contract-aligned matrix.")

    working_paper_input: Mapping[str, object] = load_example_artifact("working_paper_input")
    standards_manifest: Mapping[str, object] = load_example_artifact("standards_manifest")
    validate_artifact(working_paper_input, "working_paper_input")
    validate_artifact(standards_manifest, "standards_manifest")

    reviewer_comment_set = build_reviewer_comment_set(
        render_sample_comments(),
        working_paper_input,
        SAMPLE_RUN_ID,
        standards_manifest_ref=SAMPLE_STANDARDS_REF,
        standards_version=str(standards_manifest.get("standards_version", "")),
    )
    validate_artifact(reviewer_comment_set, "reviewer_comment_set")

    rows = rows_from_comments(
        reviewer_comment_set["comments"],
        report_version=reviewer_comment_set["working_paper_revision"],
        generation_mode=args.output_format,
    )
    export_comment_matrix(rows, output_path, args.output_format)

    provenance_record = build_provenance_record(
        reviewer_comment_set,
        working_paper_input,
        SAMPLE_STANDARDS_REF,
        standards_version=str(standards_manifest.get("standards_version", "")),
        comment_matrix_path=str(output_path),
    )
    validate_artifact(provenance_record, "provenance_record")

    write_json(output_path.parent / "reviewer_comment_set_sample.json", reviewer_comment_set)
    write_json(output_path.parent / "provenance_record_sample.json", provenance_record)
    write_json(output_path.parent / "working_paper_input_sample.json", working_paper_input)
    write_json(output_path.parent / "standards_manifest_sample.json", standards_manifest)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

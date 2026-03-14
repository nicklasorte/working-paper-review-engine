from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .output_contract import (
    DEFAULT_OUTPUT_FORMAT,
    export_comment_matrix,
    rows_from_comments,
    ensure_supported_format,
)


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
            "anchor_text": "Path loss modeled as 20log10(d) with no additional factors.",
            "section_id": "2.3",
            "page_reference": "5",
            "line_reference": "14-18",
            "comment_disposition": "For consideration",
            "resolution": "Update Section 2.3 to include environmental loss factors and cite reference model.",
            "confidence": 0.78,
            "heat_level": "major",
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

    rows = rows_from_comments(
        render_sample_comments(),
        report_version="DRAFT",
        generation_mode=args.output_format,
    )
    export_comment_matrix(rows, output_path, args.output_format)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

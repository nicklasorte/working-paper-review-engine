from __future__ import annotations

import csv
from collections import OrderedDict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, List, Mapping, MutableMapping, Sequence, Tuple

try:
    from openpyxl import Workbook
except ImportError as exc:  # pragma: no cover - surfaced in tests
    raise ImportError(
        "openpyxl is required for XLSX comment-matrix exports. "
        "Install with `pip install openpyxl`."
    ) from exc

# Canonical 13-column header list governed by spectrum-systems.
# Source: docs/comment-resolution-matrix-spreadsheet-contract.md
# Order and spelling are IMMUTABLE; do not rename or reorder.
COMMENT_MATRIX_COLUMNS: List[str] = [
    "Comment Number",
    "Reviewer Initials",
    "Agency",
    "Report Version",
    "Section",
    "Page",
    "Line",
    "Comment Type: Editorial/Grammar, Clarification, Technical",
    "Agency Notes",
    "Agency Suggested Text Change",
    "NTIA Comments",
    "Comment Disposition",
    "Resolution",
]

# Allowed values for "Comment Type: Editorial/Grammar, Clarification, Technical".
COMMENT_TYPE_VALUES: List[str] = ["Editorial/Grammar", "Clarification", "Technical"]

# Sheet name required by the spectrum-systems spreadsheet contract.
COMMENT_MATRIX_SHEET_NAME = "Comment Resolution Matrix"

DEFAULT_OUTPUT_FORMAT = "comment-matrix"

# Deterministic persona identity mapping.
PERSONA_IDENTITY_MAP: Mapping[str, Tuple[str, str]] = {
    "NTIA engineer": ("NTIA", "NTIA"),
    "FCC policy analyst": ("FCC", "FCC"),
    "DoD spectrum engineer": ("DoD", "DOD"),
    "Industry / CTIA-style reviewer": ("Industry", "CTIA"),
}

# Internal category → canonical Comment Type mapping.
# Categories not listed default to "Clarification".
_CATEGORY_COMMENT_TYPE_MAP: Mapping[str, str] = {
    "technical sufficiency": "Technical",
    "reproducibility": "Technical",
    "unsupported assertion": "Technical",
    "missing evidence/citation": "Technical",
    "missing operational detail": "Technical",
    "fairness/deployment burden": "Technical",
    "regulatory ambiguity": "Clarification",
    "policy overreach": "Clarification",
    "unclear recommendation": "Clarification",
    "inconsistent terminology": "Editorial/Grammar",
    # short aliases
    "technical": "Technical",
    "clarity": "Clarification",
    "editorial": "Editorial/Grammar",
    "grammar": "Editorial/Grammar",
    "clarification": "Clarification",
}


def map_persona_identity(persona_name: str) -> Tuple[str, str]:
    """
    Return (agency, initials) for a persona, defaulting to generic identifiers
    when the persona is not explicitly mapped.
    """
    return PERSONA_IDENTITY_MAP.get(
        persona_name, ("Working Group", "".join(token[0].upper() for token in persona_name.split() if token))
    )


def infer_comment_type(category: str, severity: str = "") -> str:
    """
    Map an internal category or severity to a canonical Comment Type value.

    Canonical values (from spectrum-systems): Editorial/Grammar, Clarification, Technical.
    Returns "" when the input is blank, so the matrix cell remains blank rather than
    fabricating a classification.
    """
    lookup = (category or "").lower().strip()
    if lookup in _CATEGORY_COMMENT_TYPE_MAP:
        return _CATEGORY_COMMENT_TYPE_MAP[lookup]
    sev = (severity or "").lower().strip()
    if sev in ("critical", "major"):
        return "Technical"
    if sev in ("minor", "info"):
        return "Clarification"
    return ""


@dataclass
class CommentMatrixRow:
    """
    Internal row object that maps to the canonical 13-column comment resolution matrix.

    The visible spreadsheet export (to_ordered_mapping) emits ONLY the canonical 13
    columns governed by spectrum-systems.  Extra internal fields (confidence_score,
    provenance_record_id, etc.) are preserved here for sidecar/provenance use.
    """

    comment_number: Any
    persona_name: str
    agency_notes: str
    agency_suggested_text_change: str = ""
    comment_type: str = ""
    comment_disposition: str = ""
    resolution: str = ""
    ntia_comments: str = ""
    report_version: str = "DRAFT"
    section: str = ""
    page: str = ""
    line: str = ""
    # Internal metadata — not written to the visible canonical sheet.
    confidence_score: float = 0.0
    provenance_record_id: str = ""
    heat_level: str = ""
    generation_mode: str = DEFAULT_OUTPUT_FORMAT

    @classmethod
    def from_generated_comment(
        cls,
        comment: Mapping[str, Any],
        *,
        comment_number: Any,
        report_version: str = "DRAFT",
        generation_mode: str = DEFAULT_OUTPUT_FORMAT,
    ) -> "CommentMatrixRow":
        """
        Map a synthetic review comment (aligned to review_comment.schema.json) into the
        canonical comment-matrix contract row.
        """
        location = comment.get("location") or {}
        agency_notes = (
            comment.get("comment_text")
            or comment.get("text")
            or comment.get("agency_notes")
            or ""
        )
        suggested = (
            comment.get("suggested_revision")
            or comment.get("suggested_action")
            or comment.get("agency_suggested_text_change")
            or ""
        )
        disposition = comment.get("disposition") or comment.get("comment_disposition") or ""
        resolution = comment.get("resolution") or ""
        ntia_comments = comment.get("rationale") or comment.get("ntia_comments") or ""
        section = location.get("section") or comment.get("section_id") or comment.get("section") or ""
        page = location.get("page") or comment.get("page_reference") or comment.get("page") or ""
        line = location.get("line") or comment.get("line_reference") or comment.get("line") or ""

        raw_comment_type = (
            comment.get("comment_type")
            or comment.get("Comment Type: Editorial/Grammar, Clarification, Technical")
            or ""
        )
        if raw_comment_type in COMMENT_TYPE_VALUES:
            comment_type = raw_comment_type
        else:
            category = (
                comment.get("comment_category")
                or comment.get("category")
                or comment.get("intent_classification")
                or ""
            )
            severity = comment.get("severity") or comment.get("heat_level") or ""
            comment_type = infer_comment_type(str(category), str(severity))

        confidence = comment.get("confidence") or comment.get("confidence_score") or 0.0
        provenance = comment.get("provenance_record_id") or comment.get("comment_id") or f"comment-{comment_number}"
        persona_name = comment.get("reviewer_persona_id") or comment.get("persona_name") or "NTIA engineer"
        heat_level = comment.get("severity") or comment.get("heat_level") or ""

        return cls(
            comment_number=comment_number,
            persona_name=persona_name,
            agency_notes=str(agency_notes),
            agency_suggested_text_change=str(suggested),
            comment_type=str(comment_type),
            comment_disposition=str(disposition),
            resolution=str(resolution),
            ntia_comments=str(ntia_comments),
            report_version=str(report_version),
            section=str(section),
            page=str(page),
            line=str(line),
            confidence_score=float(confidence),
            provenance_record_id=str(provenance),
            heat_level=str(heat_level),
            generation_mode=str(generation_mode),
        )

    def to_ordered_mapping(self) -> OrderedDict:
        """
        Return the canonical 13-column ordered mapping for spreadsheet export.

        Only the columns defined in COMMENT_MATRIX_COLUMNS appear; no extra visible
        columns are emitted.  Internal metadata fields are excluded per the
        spectrum-systems metadata handling policy.
        """
        agency, reviewer_initials = map_persona_identity(self.persona_name)
        row: MutableMapping[str, Any] = OrderedDict()
        row["Comment Number"] = self.comment_number
        row["Reviewer Initials"] = reviewer_initials
        row["Agency"] = agency
        row["Report Version"] = self.report_version
        row["Section"] = self.section
        row["Page"] = self.page
        row["Line"] = self.line
        row["Comment Type: Editorial/Grammar, Clarification, Technical"] = self.comment_type
        row["Agency Notes"] = self.agency_notes
        row["Agency Suggested Text Change"] = self.agency_suggested_text_change
        row["NTIA Comments"] = self.ntia_comments
        row["Comment Disposition"] = self.comment_disposition
        row["Resolution"] = self.resolution
        return OrderedDict((key, row[key]) for key in COMMENT_MATRIX_COLUMNS)


def ensure_supported_format(output_format: str) -> str:
    normalized = output_format or DEFAULT_OUTPUT_FORMAT
    if normalized in ("comment-matrix", "comment-matrix-xlsx"):
        return "xlsx"
    if normalized == "comment-matrix-csv":
        return "csv"
    raise ValueError(f"Unsupported output format: {output_format}")


def rows_to_csv(rows: Sequence[CommentMatrixRow], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(COMMENT_MATRIX_COLUMNS)
        for row in rows:
            ordered = row.to_ordered_mapping()
            writer.writerow([ordered.get(column, "") for column in COMMENT_MATRIX_COLUMNS])
    return path


def rows_to_xlsx(rows: Sequence[CommentMatrixRow], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = COMMENT_MATRIX_SHEET_NAME
    sheet.append(COMMENT_MATRIX_COLUMNS)
    for row in rows:
        ordered = row.to_ordered_mapping()
        sheet.append([ordered.get(column, "") for column in COMMENT_MATRIX_COLUMNS])
    workbook.save(path)
    return path


def export_comment_matrix(
    rows: Sequence[CommentMatrixRow],
    path: Path,
    output_format: str = DEFAULT_OUTPUT_FORMAT,
) -> Path:
    resolved_format = ensure_supported_format(output_format)
    if resolved_format == "xlsx":
        return rows_to_xlsx(rows, path)
    return rows_to_csv(rows, path)


def rows_from_comments(
    comments: Iterable[Mapping[str, Any]],
    *,
    report_version: str = "DRAFT",
    generation_mode: str = DEFAULT_OUTPUT_FORMAT,
) -> List[CommentMatrixRow]:
    rows: List[CommentMatrixRow] = []
    for idx, comment in enumerate(comments, start=1):
        rows.append(
            CommentMatrixRow.from_generated_comment(
                comment,
                comment_number=comment.get("comment_number", idx),
                report_version=report_version,
                generation_mode=generation_mode,
            )
        )
    return rows

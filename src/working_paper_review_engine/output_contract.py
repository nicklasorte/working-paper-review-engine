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

# Canonical column order from the Comment Resolution Engine contract.
COMMENT_MATRIX_COLUMNS: List[str] = [
    "Comment Number",
    "Reviewer Initials",
    "Agency",
    "Report Version",
    "Section",
    "Page",
    "Line",
    "Agency Notes",
    "Agency Suggested Text Change",
    "WG Chain Comments",
    "NTIA Comments",
    "Comment Disposition",
    "Resolution",
    "Report Context",
    "Resolution Task",
    "Comment Cluster Id",
    "Intent Classification",
    "Section Group",
    "Heat Level",
    "Validation Status",
    "Validation Notes",
    "Resolved Against Revision",
    "Generation Mode",
    "Rule Id",
    "Rule Source",
    "Rule Version",
    "Rules Profile",
    "Rules Profile Version",
    "Matched Rule Types",
    "Review Status",
    "Confidence Score",
    "Provenance Record Id",
]

DEFAULT_OUTPUT_FORMAT = "comment-matrix"

# Deterministic persona identity mapping.
PERSONA_IDENTITY_MAP: Mapping[str, Tuple[str, str]] = {
    "NTIA engineer": ("NTIA", "NTIA"),
    "FCC policy analyst": ("FCC", "FCC"),
    "DoD spectrum engineer": ("DoD", "DOD"),
    "Industry / CTIA-style reviewer": ("Industry", "CTIA"),
}


def map_persona_identity(persona_name: str) -> Tuple[str, str]:
    """
    Return (agency, initials) for a persona, defaulting to generic identifiers
    when the persona is not explicitly mapped.
    """
    return PERSONA_IDENTITY_MAP.get(
        persona_name, ("Working Group", "".join(token[0].upper() for token in persona_name.split() if token))
    )


@dataclass
class CommentMatrixRow:
    comment_number: Any
    persona_name: str
    agency_notes: str
    agency_suggested_text_change: str = ""
    comment_disposition: str = ""
    resolution: str = ""
    report_context: str = ""
    ntia_comments: str = ""
    report_version: str = "DRAFT"
    section: str = ""
    page: str = ""
    line: str = ""
    resolution_task: str = ""
    comment_cluster_id: str = ""
    intent_classification: str = ""
    section_group: str = ""
    heat_level: str = ""
    validation_status: str = "NOT_VALIDATED"
    validation_notes: str = ""
    resolved_against_revision: str = "UNSPECIFIED"
    generation_mode: str = DEFAULT_OUTPUT_FORMAT
    rule_id: str = "rule-placeholder"
    rule_source: str = "working-paper-review-engine"
    rule_version: str = "0.0.0"
    rules_profile: str = "default"
    rules_profile_version: str = "0.0.0"
    matched_rule_types: str = ""
    review_status: str = "PROPOSED"
    confidence_score: float = 0.0
    provenance_record_id: str = ""
    wg_chain_comments: str = ""

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
        comment-matrix contract.
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
        report_context = (
            location.get("anchor_text")
            or comment.get("anchor_text")
            or comment.get("report_context")
            or ""
        )
        ntia_comments = comment.get("rationale") or comment.get("ntia_comments") or ""
        section = location.get("section") or comment.get("section_id") or comment.get("section") or ""
        page = location.get("page") or comment.get("page_reference") or comment.get("page") or ""
        line = location.get("line") or comment.get("line_reference") or comment.get("line") or ""
        intent = (
            comment.get("intent_classification")
            or comment.get("comment_category")
            or comment.get("category")
            or ""
        )
        heat_level = comment.get("severity") or comment.get("heat_level") or ""
        resolved_against = comment.get("resolved_against_revision") or report_version
        matched_rule_types = comment.get("matched_rule_types") or ""
        review_status = comment.get("review_status") or "PROPOSED"
        confidence = comment.get("confidence") or comment.get("confidence_score") or 0.0
        provenance = comment.get("provenance_record_id") or comment.get("comment_id") or f"comment-{comment_number}"
        persona_name = comment.get("reviewer_persona_id") or comment.get("persona_name") or "NTIA engineer"

        return cls(
            comment_number=comment_number,
            persona_name=persona_name,
            agency_notes=str(agency_notes),
            agency_suggested_text_change=str(suggested),
            comment_disposition=str(disposition),
            resolution=str(resolution),
            report_context=str(report_context),
            ntia_comments=str(ntia_comments),
            report_version=str(report_version),
            section=str(section),
            page=str(page),
            line=str(line),
            resolution_task=str(comment.get("resolution_task") or ""),
            comment_cluster_id=str(comment.get("comment_cluster_id") or ""),
            intent_classification=str(intent),
            section_group=str(comment.get("section_group") or ""),
            heat_level=str(heat_level),
            validation_status=str(comment.get("validation_status") or "NOT_VALIDATED"),
            validation_notes=str(comment.get("validation_notes") or ""),
            resolved_against_revision=str(resolved_against),
            generation_mode=str(generation_mode),
            rule_id=str(comment.get("rule_id") or "rule-placeholder"),
            rule_source=str(comment.get("rule_source") or "working-paper-review-engine"),
            rule_version=str(comment.get("rule_version") or "0.0.0"),
            rules_profile=str(comment.get("rules_profile") or "default"),
            rules_profile_version=str(comment.get("rules_profile_version") or "0.0.0"),
            matched_rule_types=str(matched_rule_types),
            review_status=str(review_status),
            confidence_score=float(confidence),
            provenance_record_id=str(provenance),
            wg_chain_comments=str(comment.get("wg_chain_comments") or ""),
        )

    def to_ordered_mapping(self) -> OrderedDict:
        agency, reviewer_initials = map_persona_identity(self.persona_name)
        confidence = min(max(self.confidence_score, 0.0), 1.0)
        row: MutableMapping[str, Any] = OrderedDict()
        row["Comment Number"] = self.comment_number
        row["Reviewer Initials"] = reviewer_initials
        row["Agency"] = agency
        row["Report Version"] = self.report_version
        row["Section"] = self.section
        row["Page"] = self.page
        row["Line"] = self.line
        row["Agency Notes"] = self.agency_notes
        row["Agency Suggested Text Change"] = self.agency_suggested_text_change
        row["WG Chain Comments"] = self.wg_chain_comments
        row["NTIA Comments"] = self.ntia_comments
        row["Comment Disposition"] = self.comment_disposition
        row["Resolution"] = self.resolution
        row["Report Context"] = self.report_context
        row["Resolution Task"] = self.resolution_task
        row["Comment Cluster Id"] = self.comment_cluster_id
        row["Intent Classification"] = self.intent_classification
        row["Section Group"] = self.section_group
        row["Heat Level"] = self.heat_level
        row["Validation Status"] = self.validation_status or "NOT_VALIDATED"
        row["Validation Notes"] = self.validation_notes
        row["Resolved Against Revision"] = self.resolved_against_revision
        row["Generation Mode"] = self.generation_mode
        row["Rule Id"] = self.rule_id
        row["Rule Source"] = self.rule_source
        row["Rule Version"] = self.rule_version
        row["Rules Profile"] = self.rules_profile
        row["Rules Profile Version"] = self.rules_profile_version
        row["Matched Rule Types"] = self.matched_rule_types
        row["Review Status"] = self.review_status
        row["Confidence Score"] = confidence
        row["Provenance Record Id"] = self.provenance_record_id
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
    sheet.title = "Comment Matrix"
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

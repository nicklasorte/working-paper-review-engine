import csv
import tempfile
import unittest
from pathlib import Path

import openpyxl

from working_paper_review_engine.output_contract import (
    COMMENT_MATRIX_COLUMNS,
    CommentMatrixRow,
    rows_from_comments,
    rows_to_csv,
    rows_to_xlsx,
)


class OutputContractTests(unittest.TestCase):
    def test_column_order_matches_contract(self) -> None:
        expected = [
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
        self.assertEqual(COMMENT_MATRIX_COLUMNS, expected)

    def test_rows_serialize_to_csv_and_xlsx(self) -> None:
        comment = {
            "comment_number": 7,
            "reviewer_persona_id": "FCC policy analyst",
            "comment_text": "Align definitions of primary/secondary allocation with FCC Part 2 wording.",
            "suggested_revision": "Use FCC Part 2 definitions verbatim in Section 1.1.",
            "rationale": "Anchored to p.3 lines 5-8; current phrasing deviates from CFR text.",
            "anchor_text": "Secondary users shall not cause harmful interference...",
            "section_id": "1.1",
            "page_reference": "3",
            "line_reference": "5-8",
            "comment_disposition": "For consideration",
            "resolution": "Update wording and cite CFR Part 2.104(d).",
            "confidence": 0.64,
            "heat_level": "minor",
        }
        rows = rows_from_comments([comment], report_version="REV-A")
        tmpdir = Path(tempfile.mkdtemp())

        csv_path = rows_to_csv(rows, tmpdir / "matrix.csv")
        xlsx_path = rows_to_xlsx(rows, tmpdir / "matrix.xlsx")

        with csv_path.open() as handle:
            reader = csv.reader(handle)
            header = next(reader)
            row = next(reader)
        self.assertEqual(header, COMMENT_MATRIX_COLUMNS)
        agency_notes_idx = COMMENT_MATRIX_COLUMNS.index("Agency Notes")
        suggested_idx = COMMENT_MATRIX_COLUMNS.index("Agency Suggested Text Change")
        self.assertEqual(row[agency_notes_idx], comment["comment_text"])
        self.assertEqual(row[suggested_idx], comment["suggested_revision"])

        workbook = openpyxl.load_workbook(xlsx_path)
        sheet = workbook.active
        header_row = [cell.value for cell in next(sheet.iter_rows(min_row=1, max_row=1))]
        self.assertEqual(header_row, COMMENT_MATRIX_COLUMNS)
        value_row = [cell.value for cell in next(sheet.iter_rows(min_row=2, max_row=2))]
        disposition_idx = COMMENT_MATRIX_COLUMNS.index("Comment Disposition")
        self.assertEqual(value_row[disposition_idx], comment["comment_disposition"])

    def test_defaults_fill_required_fields(self) -> None:
        row = CommentMatrixRow(
            comment_number=1,
            persona_name="DoD spectrum engineer",
            agency_notes="Sample",
        ).to_ordered_mapping()
        self.assertEqual(row["Validation Status"], "NOT_VALIDATED")
        self.assertEqual(row["WG Chain Comments"], "")
        self.assertTrue(row["Rule Id"])
        self.assertEqual(row["Generation Mode"], "comment-matrix")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()

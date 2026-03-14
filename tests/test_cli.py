import json
import tempfile
import unittest
from pathlib import Path

import openpyxl

from working_paper_review_engine import contracts
from working_paper_review_engine import cli
from working_paper_review_engine.output_contract import COMMENT_MATRIX_COLUMNS


class CliOutputTests(unittest.TestCase):
    def test_default_output_format_is_comment_matrix(self) -> None:
        parser = cli.build_parser()
        args = parser.parse_args([])
        self.assertEqual(args.output_format, "comment-matrix")

    def test_cli_sample_writes_comment_matrix(self) -> None:
        tmpdir = Path(tempfile.mkdtemp())
        target = tmpdir / "cli-sample.xlsx"
        exit_code = cli.main(["--sample", "--output-path", str(target)])
        self.assertEqual(exit_code, 0)
        workbook = openpyxl.load_workbook(target)
        header_row = [cell.value for cell in next(workbook.active.iter_rows(min_row=1, max_row=1))]
        self.assertEqual(header_row, COMMENT_MATRIX_COLUMNS)
        reviewer_comment_set_path = target.parent / "reviewer_comment_set_sample.json"
        provenance_record_path = target.parent / "provenance_record_sample.json"
        working_paper_path = target.parent / "working_paper_input_sample.json"
        self.assertTrue(reviewer_comment_set_path.exists())
        self.assertTrue(provenance_record_path.exists())
        self.assertTrue(working_paper_path.exists())
        with reviewer_comment_set_path.open() as handle:
            reviewer_comment_set = json.load(handle)
        with provenance_record_path.open() as handle:
            provenance_record = json.load(handle)
        with working_paper_path.open() as handle:
            working_paper_input = json.load(handle)
        contracts.validate_artifact(reviewer_comment_set, "reviewer_comment_set")
        contracts.validate_artifact(provenance_record, "provenance_record")
        contracts.validate_artifact(working_paper_input, "working_paper_input")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()

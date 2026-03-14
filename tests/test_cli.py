import tempfile
import unittest
from pathlib import Path

import openpyxl

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


if __name__ == "__main__":  # pragma: no cover
    unittest.main()

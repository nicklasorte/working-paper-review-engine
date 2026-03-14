import copy
import json
import tempfile
import unittest
from pathlib import Path

from working_paper_review_engine import contracts


class ContractValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.working_paper_input = contracts.load_example_artifact("working_paper_input")
        self.standards_manifest = contracts.load_example_artifact("standards_manifest")
        self.reviewer_comment_set = contracts.load_example_artifact("reviewer_comment_set")
        self.provenance_record = contracts.load_example_artifact("provenance_record")

    def test_contract_declaration_records_consumed_and_produced(self) -> None:
        declaration = contracts.load_contract_declaration()
        self.assertIn("working_paper_input", declaration["consumed_artifact_types"])
        self.assertIn("standards_manifest", declaration["consumed_artifact_types"])
        self.assertIn("reviewer_comment_set", declaration["produced_artifact_types"])
        self.assertIn("provenance_record", declaration["produced_artifact_types"])
        self.assertEqual(declaration["standards_source_repo"], "spectrum-systems")

    def test_example_artifacts_validate(self) -> None:
        contracts.validate_artifact(self.working_paper_input, "working_paper_input")
        contracts.validate_artifact(self.standards_manifest, "standards_manifest")
        contracts.validate_artifact(self.reviewer_comment_set, "reviewer_comment_set")
        contracts.validate_artifact(self.provenance_record, "provenance_record")

    def test_pipeline_outputs_build_and_validate(self) -> None:
        comment_set = contracts.build_reviewer_comment_set(
            self.reviewer_comment_set["comments"],
            self.working_paper_input,
            review_run_id=self.reviewer_comment_set["review_run_id"],
            standards_manifest_ref=self.reviewer_comment_set["standards_manifest_ref"],
            standards_version=self.standards_manifest["standards_version"],
            provenance_record_id="prov-review-run-sample-001",
        )
        contracts.validate_artifact(comment_set, "reviewer_comment_set")

        provenance = contracts.build_provenance_record(
            comment_set,
            self.working_paper_input,
            comment_set["standards_manifest_ref"],
            standards_version=self.standards_manifest["standards_version"],
            comment_matrix_path="outputs/examples/comment_matrix_sample.xlsx",
        )
        contracts.validate_artifact(provenance, "provenance_record")

    def test_validation_failure_is_clear(self) -> None:
        invalid = copy.deepcopy(self.reviewer_comment_set)
        invalid["comments"][0].pop("comment_text")
        with self.assertRaises(ValueError) as ctx:
            contracts.validate_artifact(invalid, "reviewer_comment_set")
        self.assertIn("reviewer_comment_set", str(ctx.exception))
        self.assertIn("comment_text", str(ctx.exception))

    def test_write_json_outputs_payload(self) -> None:
        tmpdir = Path(tempfile.mkdtemp())
        target = tmpdir / "artifact.json"
        contracts.write_json(target, {"artifact_type": "test"})
        with target.open() as handle:
            payload = json.load(handle)
        self.assertEqual(payload["artifact_type"], "test")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()

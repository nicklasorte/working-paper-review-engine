"""Tests that governance artifacts exist and are structurally valid."""

import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


class GovernanceDeclarationTests(unittest.TestCase):
    DECLARATION_PATH = REPO_ROOT / "governance" / "governance-declaration.json"
    REQUIRED_FIELDS = [
        "system_id",
        "implementation_repo",
        "architecture_source",
        "contract_pins",
        "schema_pins",
        "rule_version",
        "prompt_set_hash",
        "evaluation_manifest_path",
        "last_evaluation_date",
        "external_storage_policy",
        "governance_declaration_version",
    ]

    def _load(self) -> dict:
        with self.DECLARATION_PATH.open() as handle:
            return json.load(handle)

    def test_governance_declaration_exists(self) -> None:
        self.assertTrue(
            self.DECLARATION_PATH.exists(),
            f"governance-declaration.json not found at {self.DECLARATION_PATH}",
        )

    def test_governance_declaration_is_valid_json(self) -> None:
        data = self._load()
        self.assertIsInstance(data, dict)

    def test_governance_declaration_has_required_fields(self) -> None:
        data = self._load()
        missing = [f for f in self.REQUIRED_FIELDS if f not in data]
        self.assertEqual(
            missing,
            [],
            f"governance-declaration.json is missing required fields: {missing}",
        )

    def test_governance_declaration_contract_pins_is_mapping(self) -> None:
        data = self._load()
        self.assertIsInstance(data["contract_pins"], dict)
        self.assertGreater(len(data["contract_pins"]), 0)

    def test_governance_declaration_schema_pins_is_mapping(self) -> None:
        data = self._load()
        self.assertIsInstance(data["schema_pins"], dict)
        self.assertGreater(len(data["schema_pins"]), 0)

    def test_governance_declaration_evaluation_manifest_path_exists(self) -> None:
        data = self._load()
        eval_path = REPO_ROOT / data["evaluation_manifest_path"]
        self.assertTrue(
            eval_path.exists(),
            f"evaluation_manifest_path references missing file: {eval_path}",
        )


class SystemMetadataTests(unittest.TestCase):
    METADATA_PATH = REPO_ROOT / "governance" / "system-metadata.json"
    REQUIRED_FIELDS = [
        "system_id",
        "repo_name",
        "repo_type",
        "architecture_layer",
        "governance_source",
        "contracts_consumed",
        "contracts_produced",
    ]

    def _load(self) -> dict:
        with self.METADATA_PATH.open() as handle:
            return json.load(handle)

    def test_system_metadata_exists(self) -> None:
        self.assertTrue(
            self.METADATA_PATH.exists(),
            f"system-metadata.json not found at {self.METADATA_PATH}",
        )

    def test_system_metadata_is_valid_json(self) -> None:
        data = self._load()
        self.assertIsInstance(data, dict)

    def test_system_metadata_has_required_fields(self) -> None:
        data = self._load()
        missing = [f for f in self.REQUIRED_FIELDS if f not in data]
        self.assertEqual(
            missing,
            [],
            f"system-metadata.json is missing required fields: {missing}",
        )

    def test_system_metadata_contracts_consumed_is_list(self) -> None:
        data = self._load()
        self.assertIsInstance(data["contracts_consumed"], list)
        self.assertGreater(len(data["contracts_consumed"]), 0)

    def test_system_metadata_contracts_produced_is_list(self) -> None:
        data = self._load()
        self.assertIsInstance(data["contracts_produced"], list)
        self.assertGreater(len(data["contracts_produced"]), 0)

    def test_system_metadata_governance_source_is_spectrum_systems(self) -> None:
        data = self._load()
        self.assertEqual(data["governance_source"], "spectrum-systems")


class EvalManifestTests(unittest.TestCase):
    MANIFEST_PATH = REPO_ROOT / "evals" / "eval-manifest.json"

    def _load(self) -> dict:
        with self.MANIFEST_PATH.open() as handle:
            return json.load(handle)

    def test_eval_manifest_exists(self) -> None:
        self.assertTrue(
            self.MANIFEST_PATH.exists(),
            f"eval-manifest.json not found at {self.MANIFEST_PATH}",
        )

    def test_eval_manifest_is_valid_json(self) -> None:
        data = self._load()
        self.assertIsInstance(data, dict)

    def test_eval_manifest_has_evaluation_dimensions(self) -> None:
        data = self._load()
        self.assertIn("evaluation_dimensions", data)
        self.assertIsInstance(data["evaluation_dimensions"], list)
        self.assertGreater(len(data["evaluation_dimensions"]), 0)

    def test_eval_manifest_each_dimension_has_id_and_label(self) -> None:
        data = self._load()
        for dim in data["evaluation_dimensions"]:
            self.assertIn("id", dim, f"dimension missing 'id': {dim}")
            self.assertIn("label", dim, f"dimension missing 'label': {dim}")


class CIReferencedPathsTests(unittest.TestCase):
    """Validate that paths referenced in governance/CI configuration files exist."""

    def test_contract_declaration_path_exists(self) -> None:
        path = REPO_ROOT / "contracts" / "contract_declaration.json"
        self.assertTrue(path.exists(), f"contract_declaration.json not found at {path}")

    def test_canonical_schema_dir_exists(self) -> None:
        path = REPO_ROOT / "contracts" / "spectrum-systems"
        self.assertTrue(path.is_dir(), f"contracts/spectrum-systems/ directory not found")

    def test_examples_contracts_dir_exists(self) -> None:
        path = REPO_ROOT / "examples" / "contracts"
        self.assertTrue(path.is_dir(), f"examples/contracts/ directory not found")

    def test_governance_dir_exists(self) -> None:
        path = REPO_ROOT / "governance"
        self.assertTrue(path.is_dir(), f"governance/ directory not found")

    def test_standardization_summary_exists(self) -> None:
        path = REPO_ROOT / "docs" / "repo-standardization-summary.md"
        self.assertTrue(
            path.exists(),
            f"docs/repo-standardization-summary.md not found at {path}",
        )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()

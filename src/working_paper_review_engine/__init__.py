"""
Working Paper Review Engine

Schema-first utilities for shaping review outputs into the
Comment Resolution Engine comment-matrix contract.
"""

from .output_contract import (  # noqa: F401
    COMMENT_MATRIX_COLUMNS,
    DEFAULT_OUTPUT_FORMAT,
    PERSONA_IDENTITY_MAP,
    CommentMatrixRow,
    ensure_supported_format,
    export_comment_matrix,
    map_persona_identity,
    rows_to_csv,
    rows_to_xlsx,
)
from .contracts import (  # noqa: F401
    build_provenance_record,
    build_reviewer_comment_set,
    load_contract_declaration,
    load_example_artifact,
    load_schema,
    validate_artifact,
    write_json,
)

__all__ = [
    "COMMENT_MATRIX_COLUMNS",
    "DEFAULT_OUTPUT_FORMAT",
    "PERSONA_IDENTITY_MAP",
    "CommentMatrixRow",
    "ensure_supported_format",
    "export_comment_matrix",
    "map_persona_identity",
    "rows_to_csv",
    "rows_to_xlsx",
    "build_provenance_record",
    "build_reviewer_comment_set",
    "load_contract_declaration",
    "load_example_artifact",
    "load_schema",
    "validate_artifact",
    "write_json",
]

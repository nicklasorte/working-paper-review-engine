# spectrum-systems contract snapshots

This directory tracks the canonical artifact contracts governed by the `spectrum-systems` repository. Files are synced snapshots for local validation only; the source of truth remains in `spectrum-systems`. Update the `version` fields when re-syncing from upstream.

## Consumed artifact schemas
- `working_paper_input.schema.json` — canonical intake contract for working paper revisions
- `standards_manifest.schema.json` — contract versions and compatibility target

## Produced artifact schemas
- `reviewer_comment_set.schema.json` — anchored review comment set
- `provenance_record.schema.json` — binds inputs, outputs, timestamps, and source metadata

## Spreadsheet export contract
- `comment_resolution_matrix_spreadsheet_contract.schema.json` — **canonical 13-column spreadsheet interface** for the comment resolution matrix. This governs the exact headers, their order, allowed values, and metadata-handling policy for all user-visible exports. Governed exclusively by `spectrum-systems`; do not modify locally.

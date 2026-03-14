# Contract Adoption

This repository is an operational engine repo that consumes canonical contracts governed by the `spectrum-systems` repository. It must not redefine or fork those contracts; all schema authority remains with `spectrum-systems`.

- **Contracts consumed:** `working_paper_input`, `standards_manifest`
- **Contracts produced:** `reviewer_comment_set`, `provenance_record`
- **Standards source:** `spectrum-systems` (see `contracts/contract_declaration.json`)
- **Mode:** consume and produce canonical artifacts while preserving provenance.

Boundary requirements:
- Validate incoming artifacts against the canonical schemas before processing.
- Emit reviewer outputs as `reviewer_comment_set` artifacts and preserve the `review_run_id`, working paper identifiers, persona identifiers, anchors, and trace metadata.
- Emit `provenance_record` artifacts that bind inputs, standards manifests, outputs, timestamps, and repository metadata for auditability.
- Keep downstream compatibility with Comment Resolution Engine by shaping the matrix export from the canonical comment set.
- The canonical `reviewer_comment_set` is the upstream contract for Comment Resolution Engine; the CSV/XLSX matrix remains as the compatibility export.

See `contracts/spectrum-systems/*.schema.json` for the locally snapshotted schemas and `contracts/contract_declaration.json` for the machine-readable declaration. Update the snapshot versions only when the canonical source in `spectrum-systems` changes.

# Story Packet: S002-context-helper-tests

## Identity
- Run: `review-gates-stress-001-20260702-1715`
- Milestone: `M002-context-containment`
- Story: `S002-context-helper-tests`
- Title: Context containment focused tests

## Primary Behavioral Contract
Add focused pytest coverage that verifies the context helper from `S001-context-helper-contract` excludes forbidden internal control fields and preserves task-relevant fields for downstream workers.

## Inputs
- The helper API produced by `S001-context-helper-contract`.
- The forbidden field set from the M002 contract: `current_state_path`, `next_action`, `exact_next_action`, `repair_count`, `final_action`, `terminal_reason`.
- Existing test conventions under `tests/`.

## Expected Outputs
- A focused test module, likely `tests/test_context_containment.py`.
- Tests that fail if any forbidden control field appears in prepared worker context.
- Tests that fail if representative task-relevant non-control fields are dropped or mutated.

## Acceptance Criteria
1. Tests cover all six forbidden control fields being excluded when present in input.
2. Tests cover representative non-control fields remaining in output with their original values.
3. Focused validation passes with `python -B -m pytest -q -p no:cacheprovider tests/test_context_containment.py`.

## Dependency Contracts
- `S001-context-helper-contract`: provides the helper API under test.
- `M001-domain-gates`: preserves importable package and pytest conventions.

## Change Boundary
- May add or adjust only tests that directly verify context containment acceptance criteria.
- May not expand tests for CLI, docs, full packet generation, gate advancement, failure dossiers, persistence, MCP/tool behavior, or unrelated regressions.
- May not implement new product behavior except a minimal correction to the helper if the test story exposes a direct mismatch with the S001 contract.

## Test Policy
- Use focused pytest assertions against caller-provided in-memory mappings.
- Do not read `.adeptus/runs`, full intake, current-state files, or generated packet artifacts as product test fixtures.
- If project-level tests already cover the same behavior by the time this story runs, prefer making those pass instead of duplicating broad coverage.

## Stop Condition
- Stop when focused context containment validation passes and generated cache/temp artifacts are cleaned, or when tests reveal a contract conflict requiring S001 rework or packet repair.

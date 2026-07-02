# Story Packet: s03-conditional-baseline-repair

Run ID: `facility-operations-expansion-002`
Milestone: `m01-baseline-contract`
Story workspace: `.adeptus/runs/facility-operations-expansion-002/milestones/m01-baseline-contract/stories/s03-conditional-baseline-repair/`

## Primary Behavioral Contract

Repair one concrete baseline compatibility failure found by `s01-baseline-characterization`, limited to restoring documented existing behavior. This story is conditional and must not run if `s01` passes without finding a baseline break.

## Inputs

- This story packet.
- `s01-baseline-characterization` story summary identifying the specific failing baseline behavior.
- Focused target files needed for the failing behavior only:
  - `src/adeptus_testus/facility.py`
  - `src/adeptus_testus/cli.py`
  - `tests/test_facility.py`

## Expected Outputs

- A minimal product or test change that restores the single documented baseline behavior.
- A story summary in the story workspace naming the failure, the repair, and validation results.

## Acceptance Criteria

1. The specific baseline behavior identified by `s01` is restored without changing unrelated public behavior.
2. A focused test directly verifies the repaired compatibility behavior.
3. Relevant focused pytest selection and full `python -m pytest -q` pass.

## Non-Goals

- Do not implement expansion features or future-state scaffolding.
- Do not repair more than one baseline failure unless packet repair explicitly expands this contract.
- Do not refactor unrelated code, broaden regression suites, or weaken existing tests.
- Do not perform sibling-story or cross-story consolidation work.

## Dependency Contracts

Requires `s01-baseline-characterization` to document a concrete baseline failure. If no such failure exists, this story is skipped and no files are changed.

## Change Boundary

May edit only the focused source or test files directly involved in the identified baseline failure. Do not modify README, package metadata, installed Adeptus skill files, old run artifacts, or unrelated project files.

## Test Policy

Run the smallest focused pytest selection that proves the repair, then run full `python -m pytest -q`. Tests must map directly to the failing baseline behavior.

## Stop Condition

Stop when the single baseline failure is repaired and validation passes, when `s01` reports no repair is needed, or when the failure requires packet repair because it exceeds this narrow change boundary.

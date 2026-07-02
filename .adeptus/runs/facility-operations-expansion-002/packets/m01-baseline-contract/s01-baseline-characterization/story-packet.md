# Story Packet: s01-baseline-characterization

Run ID: `facility-operations-expansion-002`
Milestone: `m01-baseline-contract`
Story workspace: `.adeptus/runs/facility-operations-expansion-002/milestones/m01-baseline-contract/stories/s01-baseline-characterization/`

## Primary Behavioral Contract

Characterize and preserve current baseline CLI, facility model, render, save/load, and invalid-room behavior before expansion work begins. Add or adjust focused tests only where current baseline public behavior is not already captured.

## Inputs

- This story packet.
- `.adeptus/runs/facility-operations-expansion-002/state/baseline-validation-summary.md`
- Focused target files as needed:
  - `src/adeptus_testus/facility.py`
  - `src/adeptus_testus/cli.py`
  - `tests/test_facility.py`
  - `pyproject.toml`

## Expected Outputs

- Focused baseline characterization updates, preferably in `tests/test_facility.py`, only if existing tests do not already preserve the required behavior.
- A story summary in the story workspace describing which baseline behaviors are covered and which validation command passed.

## Acceptance Criteria

1. Tests or explicit story evidence preserve the seven-room default facility, Sarah's `08:00` Dormitory start, no sleep need by `09:00`, deterministic progress through `12:00`, render room listing/current-room marker, JSON save/load state preservation, and predictable invalid-room failure.
2. CLI compatibility remains covered for `python -m adeptus_testus --until 09:00` and `python -m adeptus_testus --until 12:00`.
3. Existing tests remain meaningful and pass without deletion or broad weakening.

## Non-Goals

- Do not implement graph/pathing, alternate scenarios, incidents, reports, expanded CLI options, or README expansion.
- Do not perform sibling-story work or future-state scaffolding beyond preserving current public behavior.
- Do not broaden regression coverage beyond tests directly tied to the acceptance criteria.
- Do not refactor unrelated source or test structure.

## Dependency Contracts

No prior story dependency. This story relies only on the supplied milestone contract and baseline validation evidence.

## Change Boundary

May edit `tests/test_facility.py` for focused characterization tests. May edit `src/adeptus_testus/facility.py` or `src/adeptus_testus/cli.py` only if an existing public baseline behavior is unexpectedly broken and the fix is narrow. Do not modify installed Adeptus skill files, old run artifacts, full workflow files, or unrelated project files.

## Test Policy

Run focused pytest selection for changed tests, then run full `python -m pytest -q` when cheap. Tests must map directly to the acceptance criteria above.

## Stop Condition

Stop when focused baseline coverage is documented and validation passes, or when a concrete baseline failure requires routing to `s03-conditional-baseline-repair`, or when packet repair is required because the story cannot be completed from this bounded context.

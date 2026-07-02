# Story Packet: s02-named-scenarios

Run ID: facility-operations-expansion-002
Milestone ID: m02-graph-scenarios
Story ID: s02-named-scenarios
Story Work Path: `.adeptus/runs/facility-operations-expansion-002/milestones/m02-graph-scenarios/stories/s02-named-scenarios/`

## Primary Behavioral Contract

The simulator supports named deterministic scenarios, preserves the existing default scenario semantics, and adds a deterministic `maintenance_day` scenario that can run through the existing simulation flow.

## Inputs

- m01 baseline preservation contract from `.adeptus/runs/facility-operations-expansion-002/state/milestone-summaries/m01-baseline-contract.json`
- Dependency contract from `s01-facility-graph-pathing`
- Focused product/test files: `src/adeptus_testus/facility.py`, `tests/test_facility.py`

## Outputs

- Product behavior for selecting or constructing named deterministic scenarios.
- A preserved `default` scenario equivalent to baseline expectations.
- A `maintenance_day` scenario with deterministic starting state and deterministic scheduled behavior compatible with graph/pathing.
- Focused tests for default preservation, maintenance-day determinism, and invalid scenario name validation.

## Acceptance Criteria

1. The `default` scenario remains compatible with baseline expectations: Sarah starts at 08:00 in Dormitory, does not require sleep by 09:00, and advances deterministically through at least 12:00.
2. A named `maintenance_day` scenario exists and produces identical timeline/state results across repeated runs to the same end time.
3. Unknown scenario names fail predictably without falling back silently to a different scenario.

## Non-Goals

Do not add scenario JSON serialization, expanded save/load, incidents, operations reports, README content, report CLI flags, timeline display CLI, sibling-story work, broad regression expansion, unrelated refactors, randomness, wall-clock behavior, GUI behavior, runtime services, or dependency changes.

## Dependency Contracts

Requires `s01-facility-graph-pathing`:
- The seven-room graph and deterministic route/travel-duration behavior are available.
- Scenario movement or room references must use graph validation rather than bypassing it.

Baseline preservation remains required for existing tests and CLI `--until` compatibility.

## Change Boundary

May modify `src/adeptus_testus/facility.py` and `tests/test_facility.py`. May add a small scenario helper module only if the implementation documents why it is clearer than keeping scenario definitions in `facility.py`. Must not modify CLI except for minimal compatibility preservation if required by constructor/API changes.

## Test Policy

Add or update only tests that directly verify default scenario preservation, deterministic `maintenance_day` execution, and predictable invalid scenario name handling. Do not add JSON/save-load tests in this story; those belong to `s03-scenario-json-save-load`.

## Stop Condition

Stop when focused named-scenario tests and preserved baseline tests pass, or when a blocker is found that requires packet repair, such as an unresolved conflict between baseline constructor semantics and named scenario selection.

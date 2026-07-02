# Story Packet: s03-scenario-json-save-load

Run ID: facility-operations-expansion-002
Milestone ID: m02-graph-scenarios
Story ID: s03-scenario-json-save-load
Story Work Path: `.adeptus/runs/facility-operations-expansion-002/milestones/m02-graph-scenarios/stories/s03-scenario-json-save-load/`

## Primary Behavioral Contract

Scenario JSON serialization/deserialization round trips valid named scenario structures, rejects invalid scenario JSON or invalid room references predictably, and expanded save/load preserves relevant scenario and graph-derived simulation state while retaining baseline save/load compatibility.

## Inputs

- m01 baseline preservation contract from `.adeptus/runs/facility-operations-expansion-002/state/milestone-summaries/m01-baseline-contract.json`
- Dependency contract from `s01-facility-graph-pathing`
- Dependency contract from `s02-named-scenarios`
- Focused product/test files: `src/adeptus_testus/facility.py`, `tests/test_facility.py`

## Outputs

- Product behavior for scenario JSON serialization/deserialization with predictable validation.
- Expanded save/load behavior that preserves selected scenario name and relevant expanded state while remaining compatible with baseline JSON save/load expectations.
- Focused tests for JSON round trip, invalid scenario JSON/room validation, and expanded save/load preservation.

## Acceptance Criteria

1. Valid scenario JSON for supported scenario structures serializes and deserializes without behavioral drift, including stable scenario name and room/activity references.
2. Invalid scenario JSON shape, unknown scenario names, or invalid room references fail predictably through a stable exception or documented error result.
3. Save/load preserves baseline simulation state plus expanded scenario/graph-relevant state needed to continue deterministically after load.

## Non-Goals

Do not add new named scenarios beyond those required by `s02`, incidents, operations reports, README content, broad CLI expansion, future milestone report/timeline behavior, sibling-story work, broad regression expansion, unrelated refactors, randomness, wall-clock behavior, GUI behavior, runtime services, or dependency changes.

## Dependency Contracts

Requires `s01-facility-graph-pathing`:
- The canonical graph validates all room references.
- Invalid room references fail predictably.

Requires `s02-named-scenarios`:
- `default` and `maintenance_day` scenarios exist.
- Unknown scenario names fail predictably.
- Scenario execution is deterministic before serialization work is added.

Baseline preservation remains required for existing JSON save/load tests and CLI `--until` compatibility.

## Change Boundary

May modify `src/adeptus_testus/facility.py` and `tests/test_facility.py`. May add a small serialization helper module only if the implementation documents why it is clearer than keeping JSON behavior in `facility.py`. Must not modify CLI except for minimal compatibility preservation if required by save/load API changes.

## Test Policy

Add or update only tests that directly verify scenario JSON round trip, invalid scenario JSON/room handling, and expanded save/load continuation. Prefer project-level existing save/load tests when they can be extended without losing their baseline purpose.

## Stop Condition

Stop when focused JSON/save-load tests and preserved baseline tests pass, or when a blocker is found that requires packet repair, such as an ambiguous save-file compatibility rule or missing scenario data contract from dependency stories.

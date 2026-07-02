# Review Packet: s01-deterministic-incidents

## Completed Behavior Contract

Deterministic scheduled incidents are now modeled in facility simulation state for the `maintenance_day` scenario.

- Incident fields: `time`, `room`, `name`, `severity`, `effect`, `handling_note`.
- Scheduled incidents:
  - `08:45`, `Control Room`, `Telemetry drift`, `medium`
  - `11:00`, `Garden`, `Irrigation pressure drop`, `high`
- `FacilityState.incidents_until(target_time)` reports deterministic incidents by time.
- `FacilityState.encountered_incidents()` reports incidents whose scheduled time has passed and whose room matches Sarah's current room.
- Incident behavior uses no randomness, wall-clock time, runtime dependencies, CLI changes, report formatting, README changes, or graph/scenario redesign.

## Changed Files

- `src/adeptus_testus/facility.py`
  - Added `Incident`, maintenance-day incident definitions, incident state wiring, incident JSON payload support, and query methods.
- `tests/test_facility.py`
  - Added focused incident acceptance tests and save/load preservation assertion.

## Validation Evidence

- `python -m pytest -q tests/test_facility.py`
- Result: `20 passed in 0.17s`

## Direct Dependency Contracts

- m02 graph/scenario summary: `.adeptus/runs/facility-operations-expansion-002/state/milestone-summaries/m02-graph-scenarios.json`
- Preserved established graph/pathing behavior, named `maintenance_day` scenario behavior, scenario JSON validation, and save/load compatibility covered by existing focused tests.

## Runtime Hygiene

- Removed generated `.pytest_cache` and `__pycache__` directories created by validation.
- `adeptus_cleanup_runtime_artifacts` reported no additional artifacts removed.

## Review Submission Note

Tool discovery did not expose an `inquisitor_gatekeeper` story-review submission tool in this session. This review packet is ready for Inquisitor handoff at the requested path.

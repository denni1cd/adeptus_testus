# Work Item: s01-deterministic-incidents

## Story

- Run ID: `facility-operations-expansion-002`
- Milestone: `m03-incidents-reports-cli-docs`
- Story ID: `s01-deterministic-incidents`
- Agent: `enginseer_implementer`

## Completed Behavior Contract

Implemented deterministic scheduled incident behavior for the facility simulation.

- Added immutable `Incident` scenario records with `time`, `room`, `name`, `severity`, `effect`, and `handling_note`.
- Added two deterministic `maintenance_day` incidents:
  - `08:45`, `Control Room`, `Telemetry drift`, `medium`
  - `11:00`, `Garden`, `Irrigation pressure drop`, `high`
- Added scenario-state incident access through `FacilityState.incidents`.
- Added time/report query API through `FacilityState.incidents_until(target_time)`.
- Added encounter query API through `FacilityState.encountered_incidents()`, based only on deterministic simulation time and current room.
- Preserved default scenario behavior, named scenario behavior, scenario JSON behavior, and save/load compatibility.

## Files Read

- `.adeptus/runs/facility-operations-expansion-002/packets/m03-incidents-reports-cli-docs/s01-deterministic-incidents/story-packet.md`
- `.adeptus/runs/facility-operations-expansion-002/state/milestone-summaries/m02-graph-scenarios.json`
- `src/adeptus_testus/facility.py`
- `tests/test_facility.py`

## Files Changed

- `src/adeptus_testus/facility.py`
  - Added `Incident` model and `MAINTENANCE_DAY_INCIDENTS`.
  - Extended `ScenarioDefinition` and `FacilityState` with incidents.
  - Added deterministic incident query methods.
  - Included incidents in scenario JSON and save/load payloads while keeping legacy payloads compatible.
- `tests/test_facility.py`
  - Added focused incident field assertions.
  - Added deterministic encounter/report timing assertions.
  - Added incident preservation assertion for named scenario save/load continuation.

## Tests And Validation Evidence

- Command: `python -m pytest -q tests/test_facility.py`
- Result: `20 passed in 0.17s`

Focused validation covered:

- Existing baseline and m02 facility/scenario tests in `tests/test_facility.py`.
- Two deterministic maintenance-day incident records and required fields.
- Incident reportability before and at scheduled times.
- Encounter behavior after deterministic scenario advancement to incident times.
- Save/load preservation of named scenario incidents.

## Runtime Cleanup

- Removed pytest-generated runtime artifacts:
  - `.pytest_cache`
  - `src/adeptus_testus/__pycache__`
  - `tests/__pycache__`
- Ran `adeptus_cleanup_runtime_artifacts`; result removed `0` additional items.
- No known runtime cache/temp artifacts remain from this work.

## Blockers

- No implementation blocker.
- The requested `inquisitor_gatekeeper` submission tool was not exposed after tool discovery. Local review packet was produced at the requested path for handoff.

## Tool Needs

- No reusable MCP capability was needed for implementation.
- A gatekeeper submission tool would be needed to perform the requested automatic `story_review` submission from this session.

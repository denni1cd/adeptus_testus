# Review Packet: s02-named-scenarios

## Completed Behavior Contract

The simulator supports named deterministic scenario construction with preserved default behavior and a scoped `maintenance_day` scenario.

Acceptance criteria status:

- PASS: The `default` scenario remains compatible with baseline expectations. Sarah starts at 08:00 in Dormitory, does not require sleep by 09:00, and advances deterministically through 12:00 with the existing normal-day schedule and final needs.
- PASS: The named `maintenance_day` scenario exists and produces identical timeline and state results across repeated runs to 12:00.
- PASS: Unknown scenario names raise `UnknownScenarioError` and do not silently fall back to another scenario.

## Changed Files And Diff Summary

- `src/adeptus_testus/facility.py`
  - Added `UnknownScenarioError` for predictable invalid scenario failures.
  - Added `ScenarioDefinition` and `SCENARIOS` with named `default` and `maintenance_day` definitions.
  - Added `MAINTENANCE_DAY_SCENARIO` with deterministic scheduled activities through 12:00 using required graph rooms.
  - Added `facility_for_scenario()` and preserved `default_facility()` by delegating to the named default scenario.
- `tests/test_facility.py`
  - Added focused coverage for named default preservation through noon.
  - Added deterministic repeated-run coverage for `maintenance_day` through noon.
  - Added invalid scenario name validation coverage.

## Validation Evidence

- PASS: `python -m pytest tests/test_facility.py -q`
  - `13 passed in 0.16s`
- PASS: `adeptus_python_compile(paths=["src/adeptus_testus/facility.py", "tests/test_facility.py"])`
  - return code 0; 2 files checked; no errors.
- PASS: `adeptus_pytest(args=["tests/test_facility.py", "-q"], timeout_seconds=60)`
  - return code 0; timed_out false; `13 passed in 0.13s`; stderr empty.
- PASS: Runtime cleanup completed.
  - `adeptus_pytest` removed generated pytest and bytecode artifacts.
  - Final `adeptus_cleanup_runtime_artifacts()` removed 0 artifacts and reported 0 errors.

## Direct Dependency Contracts

Requires `s01-facility-graph-pathing`, which passed review. Relevant dependency behavior preserved:

- Seven-room graph and deterministic route/travel-duration behavior remain available.
- Scenario movement and room references use graph validation rather than bypassing it.
- Failed route validation still occurs before state mutation in movement flow.

## Review Submission Note

The required review packet and work item have been produced. Tool discovery did not expose an `inquisitor_gatekeeper` submission tool in this session, so direct MCP submission could not be performed from the available tool set.

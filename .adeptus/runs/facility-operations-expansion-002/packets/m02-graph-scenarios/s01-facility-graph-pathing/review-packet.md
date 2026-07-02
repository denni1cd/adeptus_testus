# Review Packet: s01-facility-graph-pathing

## Completed Behavior Contract

The facility now exposes an explicit graph of exactly the seven required rooms and uses it for deterministic route lookup, deterministic travel-duration lookup, and movement path validation.

Accepted behavior:

- `FACILITY_GRAPH` contains exactly Dormitory, Kitchen, Workshop, Infirmary, Recreation, Garden, and Control Room.
- `route_between(origin, destination)` returns deterministic room tuples for every valid required-room pair.
- `travel_duration_minutes(origin, destination)` returns deterministic summed edge durations.
- Same-room lookup returns `(origin,)` and `0` travel minutes.
- `FacilityState.move_to()` validates route availability before mutating simulation state.
- Invalid room names fail with `UnknownRoomError`.
- Impossible routes between known rooms fail with `RouteNotFoundError`.

## Changed Files

- `src/adeptus_testus/facility.py`
  - Added graph and edge-duration constants.
  - Added `RouteNotFoundError`.
  - Added deterministic BFS route lookup.
  - Added travel-duration calculation.
  - Added `FacilityState` route/travel convenience methods.
  - Added graph validation and movement route validation.
- `tests/test_facility.py`
  - Added focused tests for graph membership, all-pairs deterministic routing, travel duration, same-room zero duration, and invalid route failure without state corruption.
  - Existing baseline tests remain in place.

## Validation Evidence

- `python -m pytest tests/test_facility.py -q`
  - Result: passed.
  - Evidence: `10 passed in 0.16s`.
- `adeptus_python_compile(paths=["src/adeptus_testus/facility.py", "tests/test_facility.py"])`
  - Result: passed.
  - Evidence: 2 files checked, no errors, command `in_memory_ast_parse_and_compile_no_bytecode`.
- `adeptus_pytest(args=["tests/test_facility.py", "-q"], timeout_seconds=60)`
  - Result: passed.
  - Evidence: `10 passed in 0.15s`, timed_out false, stderr empty.
  - Cleanup evidence: helper reported no runtime cleanup errors.
- `adeptus_cleanup_runtime_artifacts()`
  - Result: passed.
  - Evidence: removed 0 artifacts, 0 errors.

## Direct Dependency Contracts

- m01 baseline preservation contract:
  - Existing baseline tests remain meaningful and passing.
  - `--until 09:00` and `--until 12:00` CLI behavior remains compatible through preserved focused tests.
  - Default behavior still starts Sarah at 08:00 in Dormitory and advances deterministically.
- m02 graph-scenarios milestone contract:
  - This packet completes only the graph/pathing/travel-duration story boundary.
  - Named scenarios, scenario JSON, save/load expansion, incidents, reports, README content, and broad CLI changes were not implemented.

## Review Routing Note

No `inquisitor_gatekeeper` story-review submission tool was exposed in this session after tool discovery. This review packet is ready for controller/Inquisitor story review.

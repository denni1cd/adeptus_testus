# Work Item: s01-facility-graph-pathing

## Story

- Run ID: facility-operations-expansion-002
- Milestone ID: m02-graph-scenarios
- Story ID: s01-facility-graph-pathing
- Agent: enginseer_implementer

## Behavior Contract

Implemented explicit seven-room facility graph behavior for deterministic pathing and travel-duration lookup while preserving the m01 baseline default-day behavior.

Acceptance criteria status:

- Graph contains exactly Dormitory, Kitchen, Workshop, Infirmary, Recreation, Garden, and Control Room.
- Every required room can route to every other required room through deterministic paths.
- Valid route and travel-duration lookups are deterministic across repeated calls.
- Origin-equals-destination route returns the current room only and zero travel minutes.
- Unknown room references raise `UnknownRoomError`.
- Known but unreachable routes raise `RouteNotFoundError` before movement state mutation.

## Changed Behavior

- Added `FACILITY_GRAPH` with explicit deterministic adjacency for the seven required rooms.
- Added per-edge deterministic travel minutes and route duration aggregation.
- Added module-level `route_between()` and `travel_duration_minutes()` helpers.
- Added `FacilityState` route/travel wrapper methods: `route_between()`, `travel_duration_minutes()`, `route_to()`, and `travel_duration_to()`.
- Updated `FacilityState.move_to()` to validate graph route availability before mutating `current_room`, `needs`, or `history`.
- Added graph structure validation during `FacilityState` initialization.

## Changed Files

- `src/adeptus_testus/facility.py`
- `tests/test_facility.py`
- `.adeptus/runs/facility-operations-expansion-002/milestones/m02-graph-scenarios/stories/s01-facility-graph-pathing/work-item.md`
- `.adeptus/runs/facility-operations-expansion-002/packets/m02-graph-scenarios/s01-facility-graph-pathing/review-packet.md`

## Files Read

- `.adeptus/runs/facility-operations-expansion-002/packets/m02-graph-scenarios/s01-facility-graph-pathing/story-packet.md`
- `.adeptus/runs/facility-operations-expansion-002/state/milestone-summaries/m01-baseline-contract.json`
- `.adeptus/runs/facility-operations-expansion-002/state/milestone-contracts/m02-graph-scenarios.json`
- `src/adeptus_testus/facility.py`
- `tests/test_facility.py`

No full intake, full tactical plan, full strategic plan, sibling story content, installed `SKILL.md`, or full `.adeptus/runs` tree was read.

## Tests

- Added focused graph/pathing tests in `tests/test_facility.py` for graph membership, all-pairs deterministic reachability, deterministic travel duration, zero-duration same-room behavior, and invalid route failure without state corruption.
- Preserved existing baseline tests for default 08:00 start, deterministic 09:00 and 12:00 behavior, save/load, renderer, and CLI output.

## Validation Evidence

- `python -m pytest tests/test_facility.py -q`: passed, `10 passed in 0.16s`.
- `adeptus_python_compile(paths=["src/adeptus_testus/facility.py", "tests/test_facility.py"])`: passed, 2 files checked with no errors.
- `adeptus_pytest(args=["tests/test_facility.py", "-q"], timeout_seconds=60)`: passed, `10 passed in 0.15s`, timed_out false, stdin DEVNULL.
- `adeptus_cleanup_runtime_artifacts()`: passed, removed 0 artifacts, 0 errors.

## Runtime Cleanup

The Adeptus pytest helper cleaned runtime artifacts during validation. Explicit cleanup found no remaining generated runtime artifacts.

## Blockers

None.

## Tool Needs

No missing reusable MCP capability blocked implementation. No `tool-request.md` was created.

## Review Handoff

Review packet written to `.adeptus/runs/facility-operations-expansion-002/packets/m02-graph-scenarios/s01-facility-graph-pathing/review-packet.md`.

`inquisitor_gatekeeper` story-review submission was requested by role instructions but no such callable tool was exposed in this environment after tool discovery. The packet is ready for controller/Inquisitor review rerun.

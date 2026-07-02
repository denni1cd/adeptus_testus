# Tactical Plan: m02-graph-scenarios

Run ID: facility-operations-expansion-002
Milestone ID: m02-graph-scenarios
Role: lexmechanic_planner

## Milestone Contract

Implement explicit facility graph/pathing/travel duration, named deterministic scenarios, scenario JSON validation/round trip, and save/load expansion while preserving all m01 baseline behavior.

Baseline contracts to preserve:
- Package remains `adeptus_testus`.
- `python -m pytest -q` remains passing.
- `python -m adeptus_testus --until 12:00` and `--until 09:00` remain compatible.
- Facility has exactly seven required rooms: Dormitory, Kitchen, Workshop, Infirmary, Recreation, Garden, Control Room.
- Default scenario starts Sarah at 08:00 in Dormitory.
- Sarah does not require sleep by 09:00.
- Default deterministic scenario advances through at least 12:00.
- Renderer lists all seven rooms and marks Sarah's current room.
- JSON save/load preserves simulation state.
- Invalid rooms or invalid movement fail predictably.
- Existing tests remain meaningful and must not be deleted merely to pass new tests.

## Story Sequence

1. `s01-facility-graph-pathing`: Add explicit seven-room graph behavior, deterministic path selection, deterministic travel duration, and predictable invalid-room/unreachable-route failures.
2. `s02-named-scenarios`: Add a named scenario model preserving `default` and adding deterministic `maintenance_day` behavior.
3. `s03-scenario-json-save-load`: Add scenario JSON serialization/deserialization validation and expand save/load to preserve scenario and graph-related simulation state while retaining legacy compatibility.

## Dependency Contracts

- `s01-facility-graph-pathing` depends only on the m01 baseline preservation contract.
- `s02-named-scenarios` depends on `s01` graph/pathing behavior being present and stable.
- `s03-scenario-json-save-load` depends on `s01` graph/pathing behavior and `s02` named scenario structures being present and stable.

Each story packet is intended to be sufficient for implementation from its own contract plus the named dependency contracts.

## Change Boundary

Expected product files are `src/adeptus_testus/facility.py` and `tests/test_facility.py`. A story may add a small focused module only if the implementer documents why it gives a clearer boundary than extending `facility.py`. CLI changes are not planned for this milestone except preserving existing `--until` compatibility if product changes require a minimal hook.

Do not implement incidents, operations reports, README updates, expanded report CLI, wall-clock behavior, randomness, GUI behavior, runtime services, installed Adeptus skill changes, or prior run artifact rewrites.

## Test Strategy

Prefer keeping existing baseline tests passing and adding focused tests in `tests/test_facility.py` that map directly to each story's acceptance criteria. Tests must be deterministic, standard-library/runtime compatible, and scoped to the story under implementation.

Milestone validation expectation after implementation is bounded pytest evidence sufficient to cover baseline preservation plus graph, scenario, JSON, and save/load behavior. Runtime validation cache/temp artifacts must be cleaned before handoff.

## Story Packet Index

- `.adeptus/runs/facility-operations-expansion-002/packets/m02-graph-scenarios/s01-facility-graph-pathing/story-packet.md`
- `.adeptus/runs/facility-operations-expansion-002/packets/m02-graph-scenarios/s02-named-scenarios/story-packet.md`
- `.adeptus/runs/facility-operations-expansion-002/packets/m02-graph-scenarios/s03-scenario-json-save-load/story-packet.md`

## Review Handoff

Submit this tactical plan and the story packet index to `inquisitor_gatekeeper` for `tactical_pre_review`. Story implementation must not begin until the Inquisitor returns `PASS`.

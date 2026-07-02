# Story Packet: s01-facility-graph-pathing

Run ID: facility-operations-expansion-002
Milestone ID: m02-graph-scenarios
Story ID: s01-facility-graph-pathing
Story Work Path: `.adeptus/runs/facility-operations-expansion-002/milestones/m02-graph-scenarios/stories/s01-facility-graph-pathing/`

## Primary Behavioral Contract

The facility exposes an explicit graph of exactly the seven required rooms and uses it to validate room references, compute deterministic routes, and compute deterministic travel duration between rooms.

## Inputs

- m01 baseline preservation contract from `.adeptus/runs/facility-operations-expansion-002/state/milestone-summaries/m01-baseline-contract.json`
- Milestone contract for `m02-graph-scenarios`
- Focused product/test files: `src/adeptus_testus/facility.py`, `tests/test_facility.py`

## Outputs

- Product behavior for explicit room graph, route lookup, travel duration, and predictable movement/path validation.
- Focused tests proving graph membership, connectivity/pathing, deterministic travel duration, and predictable invalid route/room failures.

## Acceptance Criteria

1. The facility graph contains exactly Dormitory, Kitchen, Workshop, Infirmary, Recreation, Garden, and Control Room, and every required room is reachable from every other required room through deterministic paths.
2. Route and travel-duration lookup between valid connected rooms is deterministic across repeated calls and returns a predictable zero-duration/current-room result when origin equals destination.
3. Invalid room names and impossible routes fail predictably through a stable exception or documented error result without corrupting simulation state.

## Non-Goals

Do not add named scenario selection, scenario JSON, expanded save/load, incidents, reports, README content, broad CLI expansion, future-state incident/report structures, sibling-story work, broad regression expansion, unrelated refactors, randomness, wall-clock behavior, GUI behavior, runtime services, or dependency changes.

## Dependency Contracts

Depends only on m01 baseline behavior:
- Existing baseline tests must remain meaningful and passing.
- Existing `--until 09:00` and `--until 12:00` CLI behavior must remain compatible.
- Default behavior must still start Sarah at 08:00 in Dormitory and advance deterministically.

## Change Boundary

May modify `src/adeptus_testus/facility.py` and `tests/test_facility.py`. May add a small graph helper in a new product module only if the implementation documents why it is clearer than keeping the graph behavior in `facility.py`. Must not read broad project history or unrelated run artifacts.

## Test Policy

Add or update only tests that directly verify the three acceptance criteria and baseline preservation affected by graph/pathing changes. Prefer focused unit tests over broad integration tests. Do not delete existing baseline tests merely to make new tests pass.

## Stop Condition

Stop when focused graph/pathing tests and preserved baseline tests pass, or when a blocker is found that requires packet repair, such as missing public API expectations or conflict with existing baseline behavior.

# Story Packet: s01-deterministic-incidents

Run ID: `facility-operations-expansion-002`

Milestone: `m03-incidents-reports-cli-docs`

Story work path: `.adeptus/runs/facility-operations-expansion-002/milestones/m03-incidents-reports-cli-docs/stories/s01-deterministic-incidents/`

## Primary Behavioral Contract

Add deterministic scheduled incident behavior to the facility simulation. Incidents must be available from simulation state when encountered or reportable by time and scenario, without randomness or wall-clock dependence.

## Inputs

- This story packet.
- Dependency contract summaries:
  - m01 baseline preservation from `.adeptus/runs/facility-operations-expansion-002/state/milestone-summaries/m01-baseline-contract.json`
  - m02 graph/scenario behavior from `.adeptus/runs/facility-operations-expansion-002/state/milestone-summaries/m02-graph-scenarios.json`
- Focused files only:
  - `src/adeptus_testus/facility.py`
  - `tests/test_facility.py`

## Expected Outputs

- At least two deterministic incidents are modeled with time, room, name, severity or category, effect, and handling note.
- Incident behavior is accessible through existing or minimally extended facility/scenario APIs.
- Focused tests verify deterministic incident fields and encounter/report timing.

## Acceptance Criteria

1. At least two incidents exist for relevant deterministic scenario operation and expose time, room, name, severity or category, effect, and handling note.
2. Advancing a deterministic scenario to an incident time makes the expected incident encountered or reportable without randomness or wall-clock dependence.
3. Existing baseline and m02 graph/scenario tests remain meaningful and are not deleted to pass incident tests.

## Non-Goals

- Do not implement operations text or JSON report formatting; that belongs to `s02-operations-reports`.
- Do not add or alter CLI options; that belongs to `s03-expanded-cli-options`.
- Do not update README; that belongs to `s04-readme-final-baseline-tests`.
- Do not redesign the graph, named scenario system, save/load format, or unrelated rendering behavior except for the smallest dependency-compatible additions needed for incidents.
- Do not add GUI, curses, colors, network, database, randomness, wall-clock dependence, or runtime dependencies.

## Dependency Contracts

- m01 baseline compatibility must be preserved, including `--until 09:00`, `--until 12:00`, seven required rooms, default Sarah start, rendering, and JSON save/load behavior.
- m02 graph/scenario behavior must be treated as established: explicit graph/pathing, deterministic travel duration, named scenarios including `maintenance_day`, and scenario JSON validation are dependencies rather than rewrite targets.

## Change Boundary

May modify only:

- `src/adeptus_testus/facility.py`
- `tests/test_facility.py`

Tests may be added or adjusted only where they directly verify this story's incident acceptance criteria or preserve immediately affected baseline behavior.

## Test Policy

Run focused pytest coverage for incident behavior and any affected existing tests. Preferred validation is `python -m pytest -q tests/test_facility.py` unless the local workflow requires the Adeptus pytest tool. Do not expand broad regression coverage beyond incident criteria.

## Stop Condition

Stop when incident tests and affected baseline tests pass, or when a blocker proves the packet lacks required context or m02 behavior is incompatible with deterministic incidents.

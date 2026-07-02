# Story Packet: s02-operations-reports

Run ID: `facility-operations-expansion-002`

Milestone: `m03-incidents-reports-cli-docs`

Story work path: `.adeptus/runs/facility-operations-expansion-002/milestones/m03-incidents-reports-cli-docs/stories/s02-operations-reports/`

## Primary Behavioral Contract

Generate deterministic operations reports from scenario simulation state. Text reports are required. JSON reports are expected unless implementation proves infeasible within the existing dependency-free design.

## Inputs

- This story packet.
- Named dependency contract: `s01-deterministic-incidents` must be complete and passing.
- Dependency contract summaries:
  - m01 baseline preservation from `.adeptus/runs/facility-operations-expansion-002/state/milestone-summaries/m01-baseline-contract.json`
  - m02 graph/scenario behavior from `.adeptus/runs/facility-operations-expansion-002/state/milestone-summaries/m02-graph-scenarios.json`
- Focused files only:
  - `src/adeptus_testus/facility.py`
  - `tests/test_facility.py`

## Expected Outputs

- Deterministic text operations report API.
- Deterministic JSON-compatible operations report output if implemented.
- Tests covering required report sections and deterministic JSON shape if JSON is implemented.

## Acceptance Criteria

1. Text report includes scenario name, start time, end time, rooms visited, timeline, incidents, final needs, and warnings.
2. Report incident entries include incident time, room, name, severity or category, effect, and handling note from `s01-deterministic-incidents`.
3. JSON report output, if implemented, is deterministic and includes the same behavioral data as the text report in structured form.

## Non-Goals

- Do not define new incident semantics except small fixes needed to consume `s01-deterministic-incidents`.
- Do not add CLI flags or command-line formatting decisions; that belongs to `s03-expanded-cli-options`.
- Do not update README; that belongs to `s04-readme-final-baseline-tests`.
- Do not broaden scenario, graph, or save/load behavior except as required to report existing deterministic state.
- Do not add external dependencies, randomness, wall-clock dependence, GUI, curses, or colors.

## Dependency Contracts

- Depends on `s01-deterministic-incidents` for incident data and tests.
- Depends on m02 scenario/timeline/pathing behavior for scenario name, route/timeline, rooms visited, and final simulation state.
- Must preserve m01 baseline compatibility and existing tests.

## Change Boundary

May modify only:

- `src/adeptus_testus/facility.py`
- `tests/test_facility.py`

Tests may be added or adjusted only where they directly verify report content and deterministic structured output.

## Test Policy

Run focused pytest coverage for report generation and affected existing tests. Prefer assertions on stable fields and required sections instead of brittle full-string snapshots unless the existing style already favors exact rendering tests.

## Stop Condition

Stop when report tests and affected baseline tests pass, or when a blocker shows the packet lacks required context or `s01-deterministic-incidents` has not produced consumable incident data.

# Story Packet: s04-readme-final-baseline-tests

Run ID: `facility-operations-expansion-002`

Milestone: `m03-incidents-reports-cli-docs`

Story work path: `.adeptus/runs/facility-operations-expansion-002/milestones/m03-incidents-reports-cli-docs/stories/s04-readme-final-baseline-tests/`

## Primary Behavioral Contract

Document the completed deterministic facility-operations simulator surface and add final baseline-preservation tests tied directly to the documented behavior.

## Inputs

- This story packet.
- Named dependency contracts:
  - `s01-deterministic-incidents`
  - `s02-operations-reports`
  - `s03-expanded-cli-options`
- Dependency contract summaries:
  - m01 baseline preservation from `.adeptus/runs/facility-operations-expansion-002/state/milestone-summaries/m01-baseline-contract.json`
  - m02 graph/scenario behavior from `.adeptus/runs/facility-operations-expansion-002/state/milestone-summaries/m02-graph-scenarios.json`
- Focused files only:
  - `README.md`
  - `tests/test_facility.py`

## Expected Outputs

- README concisely documents preview, scenario/report commands, behavior summary, graph, incidents/reports, and test command.
- Final tests preserve baseline and milestone behavior without duplicating every lower-level story assertion.
- Validation evidence is produced through the milestone review flow, not by changing product behavior in this story.

## Acceptance Criteria

1. README documents preview usage, scenario/report CLI commands, graph/scenario behavior, deterministic incidents/reports, and `python -m pytest -q`.
2. Tests preserve baseline CLI behavior for `--until 09:00` and `--until 12:00` and cover one documented scenario/report command path.
3. Final validation is ready for `adeptus_python_compile(paths=["src/adeptus_testus", "tests"])` and `adeptus_pytest(args=["-q"], timeout_seconds=60)` with no generated cache/temp artifacts retained.

## Non-Goals

- Do not implement new incident, report, CLI, graph, or scenario behavior in this story.
- Do not rewrite documentation beyond concise milestone-relevant README updates.
- Do not add broad regression expansion unrelated to documented baseline and milestone acceptance.
- Do not modify package metadata, installed Adeptus skill files, sibling milestone artifacts, old run artifacts, or unrelated project files.
- Do not create cleanup, reconciliation, audit, or cross-story consolidation work as product changes.

## Dependency Contracts

- Depends on all prior m03 stories being complete and passing.
- Depends on m01 baseline preservation and m02 graph/scenario behavior.
- Final validation expectations are set by the milestone contract and must be handled by review/validation flow after implementation.

## Change Boundary

May modify only:

- `README.md`
- `tests/test_facility.py`

Tests may be added or adjusted only where they directly verify README-documented baseline and milestone behavior.

## Test Policy

Run the full project test command `python -m pytest -q` or the Adeptus pytest equivalent after documentation and final preservation tests are in place. Remove generated validation cache/temp artifacts before handoff, excluding protected `.adeptus/runs` artifacts.

## Stop Condition

Stop when README updates are complete, final preservation tests pass, and validation readiness is documented for review, or when a blocker shows prior m03 behavior is incomplete.

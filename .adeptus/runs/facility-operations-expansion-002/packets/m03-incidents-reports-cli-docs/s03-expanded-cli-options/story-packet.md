# Story Packet: s03-expanded-cli-options

Run ID: `facility-operations-expansion-002`

Milestone: `m03-incidents-reports-cli-docs`

Story work path: `.adeptus/runs/facility-operations-expansion-002/milestones/m03-incidents-reports-cli-docs/stories/s03-expanded-cli-options/`

## Primary Behavioral Contract

Expand the headless CLI to expose deterministic scenario selection, report format selection, and timeline display while preserving existing `--until` behavior.

## Inputs

- This story packet.
- Named dependency contracts:
  - `s01-deterministic-incidents`
  - `s02-operations-reports`
- Dependency contract summaries:
  - m01 baseline preservation from `.adeptus/runs/facility-operations-expansion-002/state/milestone-summaries/m01-baseline-contract.json`
  - m02 graph/scenario behavior from `.adeptus/runs/facility-operations-expansion-002/state/milestone-summaries/m02-graph-scenarios.json`
- Focused files only:
  - `src/adeptus_testus/cli.py`
  - `src/adeptus_testus/facility.py` only if CLI integration requires a narrow public helper
  - `tests/test_facility.py`

## Expected Outputs

- CLI supports scenario selection for known deterministic scenarios while default behavior remains compatible.
- CLI supports text and JSON report selection using report APIs from `s02-operations-reports`.
- CLI supports timeline display through a deterministic option.
- Headless subprocess or equivalent tests cover the new CLI behavior and preserved `--until` compatibility.

## Acceptance Criteria

1. `python -m adeptus_testus --until 09:00` and `python -m adeptus_testus --until 12:00` remain compatible with prior baseline expectations.
2. CLI accepts scenario and report-format options that produce deterministic text and JSON report output for a named scenario.
3. CLI accepts a timeline display option that emits deterministic timeline information without GUI, colors, curses, randomness, or wall-clock dependence.

## Non-Goals

- Do not add new report content beyond consuming `s02-operations-reports`.
- Do not change incident modeling beyond consuming `s01-deterministic-incidents`.
- Do not update README; that belongs to `s04-readme-final-baseline-tests`.
- Do not add interactive prompts, GUI, rich terminal UI, curses, terminal colors, external programs, network, database, or runtime dependencies.
- Do not rewrite `__main__.py` unless a minimal compatibility fix is required for CLI invocation.

## Dependency Contracts

- Depends on `s01-deterministic-incidents` and `s02-operations-reports`.
- Depends on m02 named scenarios, including `maintenance_day`, and deterministic timeline/pathing behavior.
- Must preserve m01 CLI subprocess compatibility for `--until`.

## Change Boundary

May modify only:

- `src/adeptus_testus/cli.py`
- `src/adeptus_testus/facility.py` for narrow helper exposure only
- `tests/test_facility.py`

Tests may be added or adjusted only where they directly verify CLI acceptance criteria or affected baseline CLI behavior.

## Test Policy

Run headless CLI tests using subprocess or the existing CLI test style. Assertions should check deterministic output fields and successful/failed exit behavior as appropriate. Do not introduce broad CLI matrix tests unrelated to the accepted options.

## Stop Condition

Stop when CLI tests and affected baseline tests pass, or when a blocker shows required report APIs or scenario APIs from dependency stories are absent.

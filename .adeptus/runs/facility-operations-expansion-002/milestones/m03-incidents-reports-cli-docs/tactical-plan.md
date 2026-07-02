# Tactical Plan: m03-incidents-reports-cli-docs

Run ID: `facility-operations-expansion-002`

Milestone: `m03-incidents-reports-cli-docs`

## Contract Source

- Assigned milestone contract: `.adeptus/runs/facility-operations-expansion-002/state/milestone-contracts/m03-incidents-reports-cli-docs.json`
- Intake summary: `.adeptus/runs/facility-operations-expansion-002/state/intake-summary.md`
- Dependency summaries:
  - `.adeptus/runs/facility-operations-expansion-002/state/milestone-summaries/m01-baseline-contract.json`
  - `.adeptus/runs/facility-operations-expansion-002/state/milestone-summaries/m02-graph-scenarios.json`

No full intake, full strategic plan, full workflow, installed skill file, prior run artifact tree, sibling milestone contracts, or full project tree was read for this plan.

## Milestone Objective

Add deterministic scheduled incidents, deterministic operations reports, expanded CLI report/timeline options, README coverage, and final baseline-preservation tests while preserving the m01 baseline and m02 graph/scenario behavior.

## Dependency Contracts

- m01 baseline must remain intact:
  - package remains `adeptus_testus`;
  - `python -m pytest -q` passes;
  - `python -m adeptus_testus --until 09:00` and `--until 12:00` remain compatible;
  - seven required rooms remain present;
  - default scenario starts Sarah at 08:00 in Dormitory;
  - default deterministic scenario advances through at least 12:00;
  - rendering, save/load, and invalid movement behavior remain meaningful.
- m02 graph/scenario capabilities are available:
  - explicit seven-room graph/pathing and deterministic travel duration;
  - named deterministic scenarios including `maintenance_day`;
  - scenario JSON serialization/deserialization and validation;
  - expanded save/load compatibility.

## Story Plan

1. `s01-deterministic-incidents`
   - Primary contract: add deterministic scheduled incident data and simulation/report access to encountered or reportable incidents.
   - Packet: `.adeptus/runs/facility-operations-expansion-002/packets/m03-incidents-reports-cli-docs/s01-deterministic-incidents/story-packet.md`
   - Work path: `.adeptus/runs/facility-operations-expansion-002/milestones/m03-incidents-reports-cli-docs/stories/s01-deterministic-incidents/`

2. `s02-operations-reports`
   - Primary contract: generate deterministic operations text and JSON reports from scenario simulation state.
   - Packet: `.adeptus/runs/facility-operations-expansion-002/packets/m03-incidents-reports-cli-docs/s02-operations-reports/story-packet.md`
   - Work path: `.adeptus/runs/facility-operations-expansion-002/milestones/m03-incidents-reports-cli-docs/stories/s02-operations-reports/`

3. `s03-expanded-cli-options`
   - Primary contract: expose scenario selection, report format selection, and timeline display through the headless CLI while preserving `--until`.
   - Packet: `.adeptus/runs/facility-operations-expansion-002/packets/m03-incidents-reports-cli-docs/s03-expanded-cli-options/story-packet.md`
   - Work path: `.adeptus/runs/facility-operations-expansion-002/milestones/m03-incidents-reports-cli-docs/stories/s03-expanded-cli-options/`

4. `s04-readme-final-baseline-tests`
   - Primary contract: update README documentation and add final baseline-preservation test coverage directly tied to documented CLI and simulator behavior.
   - Packet: `.adeptus/runs/facility-operations-expansion-002/packets/m03-incidents-reports-cli-docs/s04-readme-final-baseline-tests/story-packet.md`
   - Work path: `.adeptus/runs/facility-operations-expansion-002/milestones/m03-incidents-reports-cli-docs/stories/s04-readme-final-baseline-tests/`

## Integration Order

1. Implement incidents first because reports and CLI output need incident fields.
2. Implement report generation second because CLI options should call stable report APIs.
3. Implement CLI options third because they depend on scenarios, reports, and timeline behavior.
4. Implement README and final baseline tests last because they document and preserve the completed surface.

## Change Boundary

Expected editable product files are limited to:

- `src/adeptus_testus/facility.py`
- `src/adeptus_testus/cli.py`
- `tests/test_facility.py`
- `README.md`

Package metadata must remain dependency-free unless a reviewed story proves a dependency is necessary. No story may modify installed Adeptus skill files, prior run artifacts, sibling milestone artifacts, or unrelated project files.

## Test Policy

Each story may add or modify only tests that directly verify its own acceptance criteria. Existing project-level tests should be preserved and extended where practical. Final milestone validation must include:

- `adeptus_python_compile(paths=["src/adeptus_testus", "tests"])`
- `adeptus_pytest(args=["-q"], timeout_seconds=60)` with `stdin` as `DEVNULL` and `timed_out` false
- cleanup evidence showing no generated validation cache/temp artifacts remain outside protected `.adeptus/runs` artifacts

## Non-Goals

- No GUI, curses, rich terminal UI, colors, external programs, network service, database, randomness, or wall-clock dependence.
- No broad graph/scenario redesign beyond dependency-driven fixes required for this milestone.
- No cleanup, reconciliation, audit, or cross-story consolidation story as normal worker work.
- No deletion of existing meaningful tests merely to pass new tests.

## Review Handoff

Submit this tactical plan and the story packet index below to `inquisitor_gatekeeper` for `tactical_pre_review`. Story work may begin only after review returns `PASS`.

Story packet index:

- `.adeptus/runs/facility-operations-expansion-002/packets/m03-incidents-reports-cli-docs/s01-deterministic-incidents/story-packet.md`
- `.adeptus/runs/facility-operations-expansion-002/packets/m03-incidents-reports-cli-docs/s02-operations-reports/story-packet.md`
- `.adeptus/runs/facility-operations-expansion-002/packets/m03-incidents-reports-cli-docs/s03-expanded-cli-options/story-packet.md`
- `.adeptus/runs/facility-operations-expansion-002/packets/m03-incidents-reports-cli-docs/s04-readme-final-baseline-tests/story-packet.md`

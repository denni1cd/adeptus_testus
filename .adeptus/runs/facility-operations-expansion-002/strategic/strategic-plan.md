# Strategic Plan

## Metadata

- Run ID: `facility-operations-expansion-002`
- Agent: `magos_strategos`
- Mode: strategic planning for expansion run
- Target repository: `C:\Users\Zero\python_projects\ai\adeptus_testus`
- Intake source: root-level `facility-operations-expansion-002.intake.md`
- Baseline evidence: `.adeptus/runs/facility-operations-expansion-002/state/baseline-validation-summary.md`

## Statement of Intent

Expand the current small, deterministic Adeptus Testus Facility project into a deterministic facility-operations simulator with graph pathing, named scenarios, scheduled incidents, operations reporting, expanded CLI behavior, documentation, and focused tests. Preserve the existing public behavior as the compatibility floor.

The implementation should evolve the existing `facility.py` and `cli.py` shape instead of replacing it. Public behavior around the seven-room facility, Sarah's default 08:00 start, deterministic default day through noon, renderer, save/load, invalid-room errors, and `--until` CLI behavior remains mandatory.

## Strategic Acceptance Criteria

1. Baseline behavior remains passing and meaningful, including the current pytest suite and module CLI commands for `--until 09:00` and `--until 12:00`.
2. Facility graph includes all seven required rooms, validates room references/connectivity, computes deterministic routes/travel time, and rejects impossible movement predictably.
3. Named deterministic scenarios include the preserved default and an alternate `maintenance_day`; scenario data can round-trip through JSON and validates invalid room/activity structures predictably.
4. Deterministic incidents are scheduled or scenario-defined, at least two examples are covered, and incidents affect warnings, needs, route/timeline, or report output in a simple tested way.
5. Operations report generation includes scenario name, start/end time, rooms visited, movement/action timeline, incidents, final needs, and warnings; text output is required and JSON output should be implemented unless a reviewed story documents why not.
6. CLI remains headless and backward compatible with `--until`, and supports scenario/report/timeline options without colors, curses, GUI, randomness, wall-clock dependence, or non-standard runtime dependencies.
7. README concisely documents baseline preview, new scenario/report commands, graph behavior, incidents/reports, and test command.
8. Final validation uses Adeptus MCP validation: syntax check plus bounded `adeptus_pytest(["-q"], timeout_seconds=60)` evidence with `stdin: DEVNULL`, `timed_out: false`, cleanup evidence, and no leftover validation cache/temp artifacts outside protected run artifacts.
9. Controller repair boundary is preserved: product source, tests, docs, package/config, and metadata repairs must be performed by Enginseer through bounded story or repair packets, never directly by the controller.

## Architecture Design

The existing model should remain the center of the package. Keep runtime dependencies standard-library only.

- Extend `facility.py` with small explicit domain objects for graph/pathing, scenario definitions, incidents, and reports where they reduce duplication and keep validation predictable.
- Preserve existing names such as `REQUIRED_ROOMS`, `Needs`, `Activity`, `HistoryEntry`, `FacilityState`, `default_facility`, `UnknownRoomError`, `render`, `save_json`, and `load_json` unless a story has a strong compatibility-preserving reason to add wrappers.
- Model the suggested seven-room loop unless focused implementation context reveals a simpler equally testable graph that satisfies all requirements.
- Store time as deterministic `HH:MM` strings at public boundaries, with internal minute conversion as needed.
- Scenario and incident JSON should use structured dictionaries/lists via `json`, not ad hoc parsing.
- CLI should use `argparse` and keep `main(argv)` testable with pytest `capsys`.
- Tests should remain focused: preserve or strengthen baseline tests, then add direct unit tests for graph/pathing, scenario JSON, incidents/reports, save/load expansion, and CLI options.

## Milestone Matrix

| Milestone | Contract | Purpose | Dependencies |
| --- | --- | --- | --- |
| `m01-baseline-contract` | `.adeptus/runs/facility-operations-expansion-002/state/milestone-contracts/m01-baseline-contract.json` | Lock compatibility expectations, establish tactical story boundaries, and add/adjust baseline characterization coverage only where needed. | Baseline validation summary and current small repo overview. |
| `m02-graph-scenarios` | `.adeptus/runs/facility-operations-expansion-002/state/milestone-contracts/m02-graph-scenarios.json` | Implement facility graph/pathing/travel time, named scenarios, scenario JSON, and expanded save/load compatibility. | `m01` summary or confirmation of baseline contract. |
| `m03-incidents-reports-cli-docs` | `.adeptus/runs/facility-operations-expansion-002/state/milestone-contracts/m03-incidents-reports-cli-docs.json` | Implement deterministic incidents, operations reports, expanded CLI, README updates, final focused tests, and validation readiness. | `m02` summary with graph/scenario behavior. |

## Context Contract Outputs

- Intake summary: `.adeptus/runs/facility-operations-expansion-002/state/intake-summary.md`
- Strategic contract: `.adeptus/runs/facility-operations-expansion-002/state/strategic-contract.json`
- Milestone contracts:
  - `.adeptus/runs/facility-operations-expansion-002/state/milestone-contracts/m01-baseline-contract.json`
  - `.adeptus/runs/facility-operations-expansion-002/state/milestone-contracts/m02-graph-scenarios.json`
  - `.adeptus/runs/facility-operations-expansion-002/state/milestone-contracts/m03-incidents-reports-cli-docs.json`

Downstream agents must use these bounded outputs instead of the full intake or full strategic plan. Lexmechanics may read only their assigned milestone contract, this run's intake summary, and relevant prior milestone summaries named by the controller.

## Strategic Log

- Read root-level intake and confirmed it is the required intake source.
- Read baseline validation summary showing syntax and pytest baseline pass through Adeptus MCP tools.
- Read only shallow repository context needed for strategy: package model, CLI, baseline tests, README, and pyproject.
- Decomposed the expansion into three milestones so graph/scenario work and incident/report/CLI work remain independently reviewable.
- No product code, tests, docs, package metadata, installed skill files, or prior run artifacts were modified.

## Tool Needs

None. Existing Adeptus MCP validation and cleanup tools are sufficient for this strategy.

No `tool-request.md` is required.

## Inquisitor Handoff

Submit this strategic plan, intake summary, strategic contract, milestone contracts, full intake, and baseline validation evidence to `inquisitor_gatekeeper` for `strategic_pre_review`.

Review focus:

- The plan matches the intake and preserves baseline behavior.
- Milestone contracts are sealed enough for Lexmechanic planning without full intake or full strategic plan.
- Context containment and controller repair boundary are explicit.
- Tool Needs are correctly `None`.

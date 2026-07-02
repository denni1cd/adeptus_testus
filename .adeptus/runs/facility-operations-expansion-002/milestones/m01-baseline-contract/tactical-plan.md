# Tactical Plan: m01-baseline-contract

Run ID: `facility-operations-expansion-002`
Milestone: `m01-baseline-contract`
Agent: `lexmechanic_planner`

## Milestone Contract

Establish a baseline preservation contract for the facility-operations expansion and define bounded story packets for downstream work. This milestone must preserve current public behavior and may only authorize product changes if a reviewed story discovers a narrow baseline compatibility failure.

## Allowed Context Used

- `.adeptus/runs/facility-operations-expansion-002/state/milestone-contracts/m01-baseline-contract.json`
- `.adeptus/runs/facility-operations-expansion-002/state/intake-summary.md`
- `.adeptus/runs/facility-operations-expansion-002/state/baseline-validation-summary.md`

No full intake, full strategic plan, full workflow, installed skill source, sibling milestones, old run artifacts, or broad run history were read.

## Baseline Compatibility Contract

The expansion must preserve these public behaviors:

- Package remains `adeptus_testus`.
- `python -m pytest -q` remains passing.
- `python -m adeptus_testus --until 12:00` and `python -m adeptus_testus --until 09:00` remain compatible.
- Facility exposes exactly seven required baseline rooms: Dormitory, Kitchen, Workshop, Infirmary, Recreation, Garden, Control Room.
- Default scenario starts Sarah at `08:00` in Dormitory.
- Sarah does not require sleep by `09:00`.
- Default deterministic scenario advances through at least `12:00`.
- Renderer lists all seven rooms and marks Sarah's current room.
- JSON save/load preserves simulation state.
- Invalid rooms or invalid movement fail predictably.
- Existing tests remain meaningful and must not be deleted merely to pass new tests.

Baseline evidence supplied to this milestone reports syntax validation passing and pytest passing with `5 passed in 0.02s`.

## Story Packet Index

1. `s01-baseline-characterization`
   - Packet: `.adeptus/runs/facility-operations-expansion-002/packets/m01-baseline-contract/s01-baseline-characterization/story-packet.md`
   - Story workspace: `.adeptus/runs/facility-operations-expansion-002/milestones/m01-baseline-contract/stories/s01-baseline-characterization/`
   - Purpose: Capture baseline CLI/model/save-load behavior in focused acceptance criteria and tests if coverage gaps exist.

2. `s02-expansion-contract-boundaries`
   - Packet: `.adeptus/runs/facility-operations-expansion-002/packets/m01-baseline-contract/s02-expansion-contract-boundaries/story-packet.md`
   - Story workspace: `.adeptus/runs/facility-operations-expansion-002/milestones/m01-baseline-contract/stories/s02-expansion-contract-boundaries/`
   - Purpose: Produce bounded implementation and review contracts for later graph, scenario, incident, report, CLI, and README milestones without implementing them.

3. `s03-conditional-baseline-repair`
   - Packet: `.adeptus/runs/facility-operations-expansion-002/packets/m01-baseline-contract/s03-conditional-baseline-repair/story-packet.md`
   - Story workspace: `.adeptus/runs/facility-operations-expansion-002/milestones/m01-baseline-contract/stories/s03-conditional-baseline-repair/`
   - Purpose: Optional repair-only contract, activated only if `s01` finds an existing public baseline behavior failing.

## Dependency Order

`s01-baseline-characterization` should run first. `s02-expansion-contract-boundaries` may run after `s01` documents the baseline contract. `s03-conditional-baseline-repair` must not run unless `s01` reports a concrete baseline failure requiring repair.

## Change Boundary

Allowed product files are limited to focused baseline preservation work if a story requires it:

- `tests/test_facility.py`
- `src/adeptus_testus/facility.py`
- `src/adeptus_testus/cli.py`
- `README.md`
- `pyproject.toml`

No production behavior may change except narrowly to preserve or clarify existing baseline behavior under a reviewed story contract. This milestone does not implement graph/pathing, named scenarios, incident scheduling, report generation, expanded CLI features, or README expansion for future functionality.

## Test Policy

Stories may add or adjust only focused tests that directly verify their own acceptance criteria. Existing tests must remain meaningful and passing. Prefer existing project-level tests where they already cover the behavior. Final story validation should include relevant pytest selection or full `python -m pytest -q` when cheap.

## Runtime Hygiene

Before handoff, remove validation cache and bytecode artifacts created during planning or validation, including `__pycache__`, `.pytest_cache`, `.pytest-tmp*`, `.adeptus_pytest_tmp*`, `*.pyc`, and `*.pyo`. Do not delete or rewrite run-state, packet, plan, work-item, review, summary, tool-log, or context-containment artifacts.

## Review Handoff

Submit this tactical plan and the story packet index to `inquisitor_gatekeeper` for `tactical_pre_review`. Story implementation must not begin until Inquisitor returns `PASS`. If the review returns `FAIL_REWORK_MILESTONE`, repair this milestone plan and packets and resubmit. If it returns `FAIL_REWORK_STRATEGY`, route upward to Magos.

## Stop Conditions

Stop this milestone plan if:

- the supplied context packet is insufficient and would require broad history reads;
- a missing reusable MCP capability blocks planning;
- `inquisitor_gatekeeper` returns `STOP_USER_INPUT_REQUIRED` or `FULL_STOP`;
- story implementation is requested before tactical pre-review passes.

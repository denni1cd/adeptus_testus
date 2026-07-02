# Work Item: s1-core-facility-simulation

## Status
Implemented and locally validated. Review packet produced for story review.

## Story Contract
Build the complete small Python package for Adeptus Testus Facility so a user can run tests and preview a deterministic headless simulation of Sarah moving through the seven-room facility from 8:00 AM through at least 12:00 PM, with bounded needs, explicit history, JSON persistence, and predictable invalid-room handling.

## Changed Behavior
- Added a conventional Python package under `src/adeptus_testus`.
- Facility state contains exactly Dormitory, Kitchen, Workshop, Infirmary, Recreation, Garden, and Control Room in canonical order.
- Default Sarah state starts at 08:00 in Dormitory with bounded hunger, energy, morale, and health.
- Deterministic normal-day scenario advances through 12:00 with explicit movement/activity history reasons.
- Sarah does not require sleep at 09:00 because energy remains above the documented threshold.
- Invalid room references and invalid movements raise `UnknownRoomError` with the valid room set.
- Headless renderer lists all seven rooms and marks Sarah's current room with `[Sarah]`.
- JSON save/load preserves current time, current room, needs, rooms, and history.
- CLI preview is available through `python -m adeptus_testus --until 12:00` and installed script `adeptus-testus`.

## Changed Files
- `README.md`: documents rooms, needs model, preview command, and pytest command.
- `pyproject.toml`: defines package metadata, console script, setuptools source layout, and pytest source path.
- `src/adeptus_testus/__init__.py`: exports public package API.
- `src/adeptus_testus/__main__.py`: supports `python -m adeptus_testus`.
- `src/adeptus_testus/cli.py`: implements CLI preview.
- `src/adeptus_testus/facility.py`: implements room model, needs, scenario, renderer, errors, and JSON persistence.
- `tests/test_facility.py`: adds focused pytest coverage for the story acceptance criteria.
- `.adeptus/runs/facility-realism-visual-advanced-001/packets/m1-core-facility/s1-core-facility-simulation/review-packet.md`: story review handoff.

## Files Read
- `.adeptus/runs/facility-realism-visual-advanced-001/packets/m1-core-facility/s1-core-facility-simulation/story-packet.md`
- `.adeptus/runs/facility-realism-visual-advanced-001/state/milestone-contracts/m1-core-facility.json`
- `.adeptus/runs/facility-realism-visual-advanced-001/state/intake-summary.md`
- `.adeptus/runs/facility-realism-visual-advanced-001/milestones/m1-core-facility/tactical-plan.md`
- Focused allowed target path checks for `README.md`, `pyproject.toml`, `src/adeptus_testus/`, and `tests/`.

## Tests
- `adeptus_python_compile(paths=["src/adeptus_testus", "tests"])`
  - Result: pass.
  - Evidence: 5 Python files checked with in-memory AST parse/compile and no bytecode writes.
- `adeptus_pytest(args=["-q"], timeout_seconds=60)`
  - Result: pass.
  - Evidence: `5 passed in 0.09s`.
  - stdin: `DEVNULL`.
  - Timed out: `false`.

## Validation Evidence
- Syntax command: `in_memory_ast_parse_and_compile_no_bytecode`.
- Pytest command: `C:\Users\Zero\miniforge3\python.exe -B -m pytest -p no:cacheprovider -q`.
- Pytest cwd: `C:\Users\Zero\python_projects\ai\adeptus_testus`.
- Pytest stdout tail: `..... [100%] 5 passed in 0.09s`.
- Cleanup from `adeptus_pytest`: removed 0 artifacts, errors 0.
- Explicit cleanup command: `adeptus_cleanup_runtime_artifacts`.
- Explicit cleanup result: removed 0 artifacts, errors 0.
- Artifact check outside protected run artifacts returned no `__pycache__`, `.pytest_cache`, `.pytest-tmp*`, `.adeptus_pytest_tmp*`, `*.pyc`, or `*.pyo`.

## Blockers
- No implementation blocker.
- Controller repair: missing story-scoped source/test files were created in the controller workspace after MCP validation initially found no tests. Controller reran MCP compile and pytest successfully.

## Tool Needs
None.

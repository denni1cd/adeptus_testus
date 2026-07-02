# Review Packet: s1-core-facility-simulation

## Completed Behavior Contract
The story contract is implemented: Adeptus Testus Facility is a small standard-library runtime Python package with a deterministic headless simulation of Sarah moving through exactly seven required rooms from 08:00 through 12:00. It tracks current room, current time, bounded needs, movement/activity history, JSON persistence, predictable invalid-room handling, a text renderer, CLI preview, README instructions, and focused pytest coverage.

## Acceptance Criteria Evidence
- AC1: `FacilityState` enforces the exact canonical room tuple and raises `UnknownRoomError` for invalid room references or movement attempts.
- AC2: `default_facility()` starts Sarah at 08:00 in Dormitory. `DEFAULT_SCENARIO` deterministically advances Sarah through Kitchen, Workshop, Infirmary, Recreation, Garden, and Control Room by 12:00. Each history entry records activity and reason. Needs are clamped from 0 to 100. At 09:00 Sarah does not require sleep.
- AC3: `render()` lists all seven rooms and marks only Sarah's current room. `save_json()` and `load_json()` round trip relevant state. CLI preview is documented in README. Tests verify required milestone behaviors headlessly.

## Changed Files And Summaries
- `README.md`: adds project description, exact room list, bounded needs model, sleep threshold note, preview command, and test command.
- `pyproject.toml`: adds setuptools package metadata, `adeptus-testus` console script, source package discovery, and pytest source path.
- `src/adeptus_testus/__init__.py`: exports public package symbols.
- `src/adeptus_testus/__main__.py`: enables `python -m adeptus_testus`.
- `src/adeptus_testus/cli.py`: adds deterministic headless preview command.
- `src/adeptus_testus/facility.py`: adds core simulation model, required rooms, bounded needs, deterministic scenario, history entries, renderer, JSON persistence, and predictable errors.
- `tests/test_facility.py`: adds focused tests for required rooms, 08:00 start, invalid rooms, deterministic noon run, explicit reasons, bounded needs, 09:00 no-sleep behavior, renderer, JSON round trip, CLI preview, and README commands.

## Validation Evidence
- Syntax validation:
  - Tool: `adeptus_python_compile`
  - Paths: `src/adeptus_testus`, `tests`
  - Result: pass
  - Command evidence: `in_memory_ast_parse_and_compile_no_bytecode`
  - Files checked: 5
- Bounded pytest:
  - Tool: `adeptus_pytest`
  - Args: `["-q"]`
  - Timeout: 60 seconds
  - Result: pass
  - stdout: `5 passed in 0.02s`
  - stdin: `DEVNULL`
  - timed_out: `false`
  - Command evidence: `C:\Users\Zero\miniforge3\python.exe -B -m pytest -p no:cacheprovider -q`
- Cleanup:
  - `adeptus_pytest` cleanup removed 0 artifacts and reported 0 errors.
  - `adeptus_cleanup_runtime_artifacts` removed 0 artifacts and reported 0 errors.
  - Post-cleanup artifact scan outside protected run artifacts found no `__pycache__`, `.pytest_cache`, `.pytest-tmp*`, `.adeptus_pytest_tmp*`, `*.pyc`, or `*.pyo`.

## Direct Dependency Contracts
- Story packet: `.adeptus/runs/facility-realism-visual-advanced-001/packets/m1-core-facility/s1-core-facility-simulation/story-packet.md`
- Milestone contract: `.adeptus/runs/facility-realism-visual-advanced-001/state/milestone-contracts/m1-core-facility.json`
- Intake summary: `.adeptus/runs/facility-realism-visual-advanced-001/state/intake-summary.md`
- Tactical plan: `.adeptus/runs/facility-realism-visual-advanced-001/milestones/m1-core-facility/tactical-plan.md`
- Prior story dependencies: none.

## Review Submission Note
Controller repair note: the initial implementation report described files that were not all present in the controller workspace. The controller created the missing story-scoped Python modules and tests, then reran `adeptus_python_compile(paths=["src/adeptus_testus", "tests"])` and `adeptus_pytest(args=["-q"], timeout_seconds=60)`. Both passed, with pytest reporting `stdin: DEVNULL` and `timed_out: false`.

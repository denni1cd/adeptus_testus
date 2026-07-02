# Work Item: s01-baseline-characterization

## Story
- Run ID: `facility-operations-expansion-002`
- Milestone: `m01-baseline-contract`
- Story: `s01-baseline-characterization`

## Completed Behavior Contract
- Characterized current baseline CLI, facility model, render, save/load, and invalid-room behavior.
- Preserved existing baseline behavior without changing product files.
- Added focused test coverage for public `python -m adeptus_testus --until 09:00` and `python -m adeptus_testus --until 12:00` compatibility.

## Baseline Behaviors Covered
- Seven-room default facility is asserted through `REQUIRED_ROOMS` and length `7`.
- Sarah starts at `08:00` in `Dormitory`.
- Sarah does not require sleep by `09:00`; energy remains `79`.
- Deterministic normal-day progress through `12:00` is asserted by time, destination, activity, final room, and final need values.
- Renderer includes the room listing and exactly one current-room `[Sarah]` marker.
- JSON save/load preserves time, room, needs, rooms, and history.
- Invalid rooms raise `UnknownRoomError` for movement and initial state construction.
- CLI behavior is covered through direct `main(["--until", "09:00"])` and subprocess `python -m adeptus_testus` checks for `09:00` and `12:00`.

## Files Read
- `.adeptus/runs/facility-operations-expansion-002/packets/m01-baseline-contract/s01-baseline-characterization/story-packet.md`
- `.adeptus/runs/facility-operations-expansion-002/state/baseline-validation-summary.md`
- `src/adeptus_testus/facility.py`
- `src/adeptus_testus/cli.py`
- `tests/test_facility.py`
- `pyproject.toml`

## Files Changed
- `tests/test_facility.py`
- `.adeptus/runs/facility-operations-expansion-002/milestones/m01-baseline-contract/stories/s01-baseline-characterization/work-item.md`
- `.adeptus/runs/facility-operations-expansion-002/packets/m01-baseline-contract/s01-baseline-characterization/review-packet.md`

## Product Files Changed
- None.

## Tests And Validation
- `adeptus_python_compile(paths=["src/adeptus_testus", "tests"])`
  - Result: pass, 5 files checked.
- `adeptus_pytest(args=["-q"], timeout_seconds=60)`
  - Result: pass, `7 passed in 0.14s`; cleanup removed 0 artifacts with 0 errors.
- `python -B -m pytest -p no:cacheprovider -q tests/test_facility.py`
  - Result: pass, `7 passed in 0.14s`
- `python -B -m pytest -p no:cacheprovider -q`
  - Result: pass, `7 passed in 0.14s`

## Validation Evidence
- Initial focused validation after adding subprocess coverage failed because the subprocess did not inherit pytest's configured source path: `No module named adeptus_testus`.
- The test harness was adjusted to pass `PYTHONPATH=<repo>/src` to the subprocess.
- Subsequent focused and full validation passed.

## Runtime Cleanup
- Removed generated runtime cache directories matching `__pycache__` and `.pytest_cache` under the repository root.
- Post-cleanup check found no remaining `__pycache__` or `.pytest_cache` directories.

## Blockers
- None.

## Tool Needs
- No missing reusable MCP capability blocked implementation.

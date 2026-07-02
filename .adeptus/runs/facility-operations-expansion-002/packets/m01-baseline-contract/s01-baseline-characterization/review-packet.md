# Review Packet: s01-baseline-characterization

## Completed Behavior Contract
- Preserved baseline facility behavior without product-file changes.
- Added focused characterization coverage for module CLI compatibility:
  - `python -m adeptus_testus --until 09:00`
  - `python -m adeptus_testus --until 12:00`
- Existing baseline tests remain intact and meaningful.

## Changed Files
- `tests/test_facility.py`
  - Added subprocess-based parametrized test for `python -m adeptus_testus` at `09:00` and `12:00`.
  - Subprocess receives `PYTHONPATH=<repo>/src` so the module invocation matches the source checkout under pytest.
- `.adeptus/runs/facility-operations-expansion-002/milestones/m01-baseline-contract/stories/s01-baseline-characterization/work-item.md`
  - Added story work item and validation record.
- `.adeptus/runs/facility-operations-expansion-002/packets/m01-baseline-contract/s01-baseline-characterization/review-packet.md`
  - Added this review packet.

## Product Files Changed
- None.

## Validation Evidence
- Syntax command: `adeptus_python_compile(paths=["src/adeptus_testus", "tests"])`
  - Result: pass, 5 files checked.
- Full Adeptus pytest command: `adeptus_pytest(args=["-q"], timeout_seconds=60)`
  - Result: pass, `7 passed in 0.14s`; cleanup removed 0 artifacts with 0 errors.
- Focused command: `python -B -m pytest -p no:cacheprovider -q tests/test_facility.py`
  - Result: pass, `7 passed in 0.14s`
- Full command: `python -B -m pytest -p no:cacheprovider -q`
  - Result: pass, `7 passed in 0.14s`

## Acceptance Criteria Mapping
- Seven-room default facility: covered by `test_facility_has_exactly_required_rooms_and_rejects_invalid_rooms`.
- Sarah `08:00` Dormitory start: covered by `test_default_day_starts_at_0800_and_sarah_does_not_require_sleep_by_0900`.
- No sleep need by `09:00`: covered by `test_default_day_starts_at_0800_and_sarah_does_not_require_sleep_by_0900`.
- Deterministic progress through `12:00`: covered by `test_normal_day_through_noon_is_deterministic_and_bounded`.
- Render room listing/current-room marker: covered by `test_renderer_and_cli_are_headless_and_include_sarah`.
- JSON save/load state preservation: covered by `test_save_load_preserves_relevant_state`.
- Predictable invalid-room failure: covered by `test_facility_has_exactly_required_rooms_and_rejects_invalid_rooms`.
- CLI compatibility for `python -m adeptus_testus --until 09:00` and `--until 12:00`: covered by `test_python_module_cli_until_0900_and_1200_preserves_output`.

## Dependency Contracts
- No prior story dependency.
- Relied on supplied baseline validation evidence at `.adeptus/runs/facility-operations-expansion-002/state/baseline-validation-summary.md`.

## Runtime Cleanup
- Removed generated validation cache/temp artifacts matching `__pycache__` and `.pytest_cache` under the repository root.
- No remaining matching cache directories were found after cleanup.

## Blockers Or Routing Needs
- None.

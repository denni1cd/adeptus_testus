# Review Packet: S002-context-helper-tests

## Completed Behavior
- Reworked `tests/test_domain_vocabulary.py` so the exact `reviewflow.__all__` assertion includes the approved M002 context helper exports, `CONTROL_CONTEXT_FIELDS` and `prepare_worker_context`.
- Added focused pytest coverage for `reviewflow.prepare_worker_context`.
- The tests fail if any of the six forbidden control fields appear in prepared worker context.
- The tests fail if representative task-relevant non-control fields are dropped or changed.

## Changed Files
- `tests/test_domain_vocabulary.py`
  - Added `CONTROL_CONTEXT_FIELDS` to the expected public export set.
  - Added `prepare_worker_context` to the expected public export set.
- `tests/test_context_containment.py`
  - Added `test_prepare_worker_context_excludes_forbidden_control_fields`.
  - Added `test_prepare_worker_context_preserves_task_relevant_fields_unchanged`.

## Diff Summary
- Package export vocabulary coverage now reflects the approved context helper API added for M002.
- New test coverage imports the public `reviewflow` package API.
- Control-field coverage asserts the exported forbidden field set exactly matches:
  - `current_state_path`
  - `next_action`
  - `exact_next_action`
  - `repair_count`
  - `final_action`
  - `terminal_reason`
- Preservation coverage asserts task fields such as `run_id`, `milestone_id`, `story_id`, `acceptance_criteria`, `dependency_contracts`, and `allowed_files` survive with original values.
- No product code was changed.

## Validation Evidence
- Command: `python -B -m pytest -q -p no:cacheprovider tests/test_domain_vocabulary.py tests/test_gate_advancement_rules.py tests/test_failure_dossier_decisions.py tests/test_context_containment.py`
- Result: passed
- Output summary: `15 passed in 0.03s`
- Cleanup status: no `__pycache__` or `.pytest_cache` artifacts were present after validation.

## Direct Dependency Contracts
- `S001-context-helper-contract`: `reviewflow.prepare_worker_context` and `reviewflow.CONTROL_CONTEXT_FIELDS` were available through the public package API and exercised directly.
- `M001-domain-gates`: existing importable package and pytest conventions were used.

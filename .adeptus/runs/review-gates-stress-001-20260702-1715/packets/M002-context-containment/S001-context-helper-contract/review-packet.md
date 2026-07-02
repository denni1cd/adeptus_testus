# Review Packet: S001-context-helper-contract

## Completed Behavior
- Added `reviewflow.prepare_worker_context`, a deterministic side-effect-free helper that returns a new mapping derived from caller-provided context.
- Removed forbidden control-state fields from prepared context output: `current_state_path`, `next_action`, `exact_next_action`, `repair_count`, `final_action`, `terminal_reason`.
- Preserved non-control worker fields with original values.
- Did not read `.adeptus/runs`, current state files, runtime artifact paths, or any external state from the helper.

## Changed Files
- `reviewflow/context.py`
  - Added `CONTROL_CONTEXT_FIELDS`.
  - Added `prepare_worker_context(context)`.
- `reviewflow/__init__.py`
  - Exported `CONTROL_CONTEXT_FIELDS`.
  - Exported `prepare_worker_context`.

## Validation Evidence
- `adeptus_python_compile` on `reviewflow/context.py` and `reviewflow/__init__.py`: pass.
- Focused import/helper validation with `PYTHONDONTWRITEBYTECODE=1`: pass.
  - Confirmed `prepare_worker_context` returns a new mapping.
  - Confirmed all six forbidden fields are excluded.
  - Confirmed non-control fields remain available with original values.
- `adeptus_cleanup_runtime_artifacts`: pass; removed 0 artifacts, 0 errors.

## Direct Dependency Contracts
- `M001-domain-gates`: package remains importable and follows small module plus `__init__` export conventions.

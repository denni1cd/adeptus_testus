# Work Item: S001-context-helper-contract

## Identity
- Run: `review-gates-stress-001-20260702-1715`
- Milestone: `M002-context-containment`
- Story: `S001-context-helper-contract`
- Agent: `enginseer_implementer`

## Changed Behavior
- Added a deterministic `reviewflow.prepare_worker_context` helper that accepts a caller-provided mapping and returns a new `dict`.
- The helper removes these internal control-state fields: `current_state_path`, `next_action`, `exact_next_action`, `repair_count`, `final_action`, `terminal_reason`.
- Non-control fields are preserved with their original values.
- The helper is side-effect free and does not read runtime state, `.adeptus/runs`, paths, or other artifacts.

## Changed Files
- `reviewflow/context.py`: Added `CONTROL_CONTEXT_FIELDS` and `prepare_worker_context`.
- `reviewflow/__init__.py`: Exported `CONTROL_CONTEXT_FIELDS` and `prepare_worker_context` using the package's existing export pattern.

## Files Read
- `.adeptus/runs/review-gates-stress-001-20260702-1715/packets/M002-context-containment/S001-context-helper-contract/story-packet.md`
- `reviewflow/__init__.py`
- `reviewflow/domain.py`
- `reviewflow/evaluator.py`

## Tests And Validation
- Ran no-bytecode syntax validation with `adeptus_python_compile` for `reviewflow/context.py` and `reviewflow/__init__.py`.
  - Result: pass.
  - Command reported: `in_memory_ast_parse_and_compile_no_bytecode`.
- Ran focused import/helper validation with `PYTHONDONTWRITEBYTECODE=1`:
  - Imported `CONTROL_CONTEXT_FIELDS` and `prepare_worker_context` from `reviewflow`.
  - Verified returned mapping is a new object.
  - Verified all six forbidden fields are absent.
  - Verified worker fields such as `milestone_id`, `story_id`, `objective`, `allowed_paths`, and `nested` remain available with original values.
  - Result: pass.
- Ran `adeptus_cleanup_runtime_artifacts`.
  - Result: pass; removed 0 artifacts and reported 0 errors.

## Blockers
- No implementation blockers.
- `inquisitor_gatekeeper` was not exposed as a callable tool in this session, so review submission through that API could not be performed.

## Tool Needs
- No missing reusable MCP capability blocked implementation.
- No `tool-request.md` created.

## Review Handoff
- Review packet written to `.adeptus/runs/review-gates-stress-001-20260702-1715/packets/M002-context-containment/S001-context-helper-contract/review-packet.md`.

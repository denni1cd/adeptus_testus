# Work Item: S003-failure-dossier-decisions

## Status
Implemented.

## Changed Behavior
- `FailureDossierEntry` now carries optional `gate_type` and `subject_id` source context.
- Advancement evaluations now carry deterministic `failure_dossier` entries plus implementation stop flags.
- Evaluator failure paths create dossier entries for latest non-approved `requires_rework`, `blocked_user_input_required`, and `full_stop` gate decisions.
- `can_continue_implementation` reports whether implementation work may continue across gate decisions.
- `blocked_user_input_required` blocks implementation until `user_input_available=True`.
- `full_stop` blocks implementation even when user input is represented as available.

## Changed Files
- `reviewflow/domain.py`
- `reviewflow/evaluator.py`
- `reviewflow/__init__.py`
- `tests/test_domain_vocabulary.py`
- `tests/test_failure_dossier_decisions.py`

## Files Read
- `.adeptus/runs/review-gates-stress-001-20260702-1715/packets/M001-domain-gates/S003-failure-dossier-decisions/story-packet.md`
- `reviewflow/domain.py`
- `reviewflow/evaluator.py`
- `reviewflow/__init__.py`
- `tests/test_domain_vocabulary.py`
- `tests/test_gate_advancement_rules.py`

## Tests
- Command: `python -B -m pytest -q -p no:cacheprovider tests/test_domain_vocabulary.py tests/test_gate_advancement_rules.py tests/test_failure_dossier_decisions.py`
- Result: `13 passed in 0.03s`
- MCP validation command: `adeptus_pytest -q tests/test_domain_vocabulary.py tests/test_gate_advancement_rules.py tests/test_failure_dossier_decisions.py`
- MCP validation result: `13 passed in 0.03s`; cleanup removed 0 runtime artifacts.

## Validation Evidence
- Focused tests verify dossier creation for `requires_rework`, `blocked_user_input_required`, and `full_stop`.
- Focused tests verify `blocked_user_input_required` blocks implementation until user input is available.
- Focused tests verify `full_stop` remains terminal even when user input is available.
- Runtime artifact check found no `__pycache__` or `.pytest_cache` directories after validation; `adeptus_pytest` cleanup reported no generated artifacts to remove.

## Blockers
None.

## Tool Needs
None.

## Review Packet
- `.adeptus/runs/review-gates-stress-001-20260702-1715/packets/M001-domain-gates/S003-failure-dossier-decisions/review-packet.md`

# Review Packet: S003-failure-dossier-decisions

## Completed Behavior
- Deterministic failure dossier entries are produced for non-approved `requires_rework`, `blocked_user_input_required`, and `full_stop` decisions.
- Each generated dossier entry includes the decision state, gate type, subject id, rationale evidence, summary, and required action.
- Evaluator results expose dossier evidence and stop flags.
- Implementation continuation evaluation blocks on `blocked_user_input_required` until user input is available.
- Implementation continuation evaluation always blocks on `full_stop`.

## Changed Files
- `reviewflow/domain.py`: added optional gate and subject context fields to `FailureDossierEntry`.
- `reviewflow/evaluator.py`: added dossier/stop fields to `AdvancementEvaluation`, deterministic dossier creation, failure propagation, and `can_continue_implementation`.
- `reviewflow/__init__.py`: exported `can_continue_implementation`.
- `tests/test_domain_vocabulary.py`: updated export expectations for the new evaluator entry point.
- `tests/test_failure_dossier_decisions.py`: added focused S003 acceptance coverage.

## Validation Evidence
- Command: `python -B -m pytest -q -p no:cacheprovider tests/test_domain_vocabulary.py tests/test_gate_advancement_rules.py tests/test_failure_dossier_decisions.py`
- Result: `13 passed in 0.03s`
- MCP validation command: `adeptus_pytest -q tests/test_domain_vocabulary.py tests/test_gate_advancement_rules.py tests/test_failure_dossier_decisions.py`
- MCP validation result: `13 passed in 0.03s`
- Runtime cleanup/artifact status: no `__pycache__` or `.pytest_cache` directories found after validation; `adeptus_pytest` cleanup removed 0 artifacts.

## Direct Dependency Contracts
- `S001-package-domain-foundation`: used existing importable package, `GateDecision`, `DecisionState`, and `FailureDossierEntry` vocabulary.
- `S002-gate-advancement-rules`: extended existing evaluator entry/result shape while preserving focused advancement rule tests.

## Blockers
None.

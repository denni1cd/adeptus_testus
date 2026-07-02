# Review Packet: S002-gate-advancement-rules

## Completed Behavior
- Implemented deterministic advancement checks for story completion, milestone completion, final run success, and tool execution.
- The latest decision on the matching gate is authoritative.
- Missing gates, gates without decisions, and latest non-approved decisions block advancement.
- Approved latest decisions allow advancement only after required prior completion conditions are also satisfied.

## Changed Files
- `reviewflow/evaluator.py`
  - Added `AdvancementEvaluation`.
  - Added `can_complete_story`, `can_complete_milestone`, `can_complete_run`, and `can_execute_tool_request`.
- `reviewflow/__init__.py`
  - Exported the evaluator API.
- `tests/test_domain_vocabulary.py`
  - Updated package export expectation for the evaluator API.
- `tests/test_gate_advancement_rules.py`
  - Added focused S002 rule tests.

## Validation Evidence
- Command: `PYTHONDONTWRITEBYTECODE=1 python -B -m pytest -q -p no:cacheprovider tests/test_gate_advancement_rules.py tests/test_domain_vocabulary.py`
- Result: passed, `8 passed in 0.02s`.
- Command: `adeptus_pytest` with args `-q tests/test_gate_advancement_rules.py tests/test_domain_vocabulary.py`
- Result: passed, `8 passed in 0.02s`; cleanup reported zero removed artifacts and zero cleanup errors.
- Runtime artifacts: no `__pycache__` or `.pytest_cache` directories found after shell validation.

## Review Submission
- Inquisitor `story_review` submission tool was not callable in this session after focused tool discovery for `inquisitor_gatekeeper story_review` and `story_review inquisitor_gatekeeper`.

## Direct Dependency Contracts
- `S001-package-domain-foundation`: used `DecisionState`, `GateDecision`, `GateType`, `Milestone`, `ReviewGate`, `Run`, and `Story` domain vocabulary as evaluator inputs.

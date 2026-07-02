# Tactical Plan: M002-context-containment

## Milestone Contract
- Run: `review-gates-stress-001-20260702-1715`
- Milestone: `M002-context-containment`
- Planner: `lexmechanic_planner`
- Goal: add downstream worker context preparation that preserves task-relevant fields and removes internal control-state fields.

## Authorized Inputs Read
- `.adeptus/runs/review-gates-stress-001-20260702-1715/state/milestone-contracts/M002-context-containment.json`
- `.adeptus/runs/review-gates-stress-001-20260702-1715/state/intake-summary.md`
- `.adeptus/runs/review-gates-stress-001-20260702-1715/state/milestone-summaries/M001-domain-gates.json`
- `reviewflow/__init__.py`
- `reviewflow/domain.py`
- `reviewflow/evaluator.py`
- focused package/test file names under `reviewflow/` and `tests/`

## Dependency Status
- `M001-domain-gates` is passed by `inquisitor_gatekeeper`.
- Available package conventions: small importable modules under `reviewflow/`, public exports collected in `reviewflow/__init__.py`, focused pytest modules under `tests/`.

## Scope Boundary
- Allowed product boundary after tactical pre-review PASS: add a context containment helper module/API and focused tests for that helper.
- The helper must prepare worker context from bounded caller-provided input and must not read `.adeptus/runs` or depend on Adeptus runtime artifacts.
- Forbidden internal control fields: `current_state_path`, `next_action`, `exact_next_action`, `repair_count`, `final_action`, and `terminal_reason`.
- Non-goals: no full packet generator, controller state machine, CLI, docs, persistence, MCP tool changes, broad refactors, or changes to M001 gate behavior unless directly required for import exposure.

## Story Plan
1. `S001-context-helper-contract`: implement the context preparation API that copies task-relevant fields while excluding forbidden control fields.
2. `S002-context-helper-tests`: add focused pytest coverage proving forbidden fields are excluded and relevant fields remain.

This two-story split keeps implementation and verification contracts separate while preserving a small milestone.

## Validation Policy
- Expected focused validation after story execution:
  `python -B -m pytest -q -p no:cacheprovider tests/test_context_containment.py`
- If broader import exposure changes create risk, include existing focused M001 tests:
  `python -B -m pytest -q -p no:cacheprovider tests/test_domain_vocabulary.py tests/test_gate_advancement_rules.py tests/test_failure_dossier_decisions.py tests/test_context_containment.py`
- Before handoff, remove generated cache/temp artifacts created during validation, including `__pycache__`, `.pytest_cache`, `.pytest-tmp*`, `.adeptus_pytest_tmp*`, `*.pyc`, and `*.pyo`.

## Stop Conditions
- Stop if implementation would require exposing internal control-state as live worker instructions.
- Stop if the package import surface from M001 is missing or cannot be extended without broad refactor.
- Stop and request packet repair if needed context exceeds this milestone contract, the intake summary, M001 summary, and focused package convention files.

## Story Packet Index
- `.adeptus/runs/review-gates-stress-001-20260702-1715/packets/M002-context-containment/S001-context-helper-contract/story-packet.md`
- `.adeptus/runs/review-gates-stress-001-20260702-1715/packets/M002-context-containment/S002-context-helper-tests/story-packet.md`

## Review Handoff
- Submit this tactical plan and the story packet index to `inquisitor_gatekeeper` for `tactical_pre_review`.
- Story implementation may begin only after `PASS`.

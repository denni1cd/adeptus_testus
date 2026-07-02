# Story Review Decision: S001-package-domain-foundation

## Decision
- action: FAIL_REWORK_STORY
- run_id: review-gates-stress-001-20260702-1715
- milestone_id: M001-domain-gates
- story_id: S001-package-domain-foundation
- gate: story_review
- reviewer: inquisitor_gatekeeper

## Routing Fields
- canonical_action: FAIL_REWORK_STORY
- rework_target: S001-package-domain-foundation
- rework_scope: Fix the domain gate and decision vocabulary in `reviewflow/domain.py` and the focused vocabulary assertions in `tests/test_domain_vocabulary.py`; keep the package foundation data-only.
- controller_instruction: Return this story for bounded story rework. Do not advance the milestone on this story output.

## Governing Contract Reviewed
- Original story packet: `.adeptus/runs/review-gates-stress-001-20260702-1715/packets/M001-domain-gates/S001-package-domain-foundation/story-packet.md`
- Submitted work item: `.adeptus/runs/review-gates-stress-001-20260702-1715/milestones/M001-domain-gates/stories/S001-package-domain-foundation/work-item.md`
- Review packet used as evidence only: `.adeptus/runs/review-gates-stress-001-20260702-1715/packets/M001-domain-gates/S001-package-domain-foundation/review-packet.md`
- Actual changed files reviewed: `reviewflow/__init__.py`, `reviewflow/domain.py`, `tests/test_domain_vocabulary.py`

## Findings
1. `reviewflow/domain.py` does not represent the required product gate vocabulary explicitly. `GateType` currently contains only `story_review`, `milestone_review`, and `strategy_review`, but the workflow gate vocabulary supplied for this run includes the specific review gates `strategic_pre_review`, `tactical_pre_review`, `story_review`, `milestone_final_review`, and `strategic_final_review`. This fails Acceptance Criterion 3: all required gate types must be represented explicitly and covered by focused tests.
2. `reviewflow/domain.py` does not represent the complete workflow decision vocabulary explicitly. `DecisionState` omits workflow actions such as `REQUEST_TOOL_REVIEW`, `APPROVE_TOOL_REQUEST`, `REJECT_TOOL_REQUEST`, `FAIL_REWORK_TOOL`, `MARK_TOOL_FAILED_VALIDATION`, `MARK_TOOL_ACTIVE`, and `DISABLE_TOOL`. This fails Acceptance Criterion 3: all required decision states must be represented explicitly and covered by focused tests.
3. `tests/test_domain_vocabulary.py` reinforces the incomplete vocabulary by asserting only the reduced `GateType` and `DecisionState` sets, so the focused tests do not prove conformance to the required product vocabulary.

## Passing Scope
- `import reviewflow` is covered by the focused test file and passed during review validation.
- The package public surface is bounded to the domain vocabulary names.
- The required domain objects `Run`, `Milestone`, `Story`, `ReviewGate`, `GateDecision`, and `FailureDossierEntry` are present as data-only objects.
- No CLI behavior, gate advancement rules, persistence, documentation, context containment, audit reporting, networking, databases, async execution, web UI, external APIs, or MCP tool changes were found in the reviewed files.

## Validation Evidence
- Review command run: `python -B -m pytest -q -p no:cacheprovider tests/test_domain_vocabulary.py`
- Result: passed, `4 passed in 0.01s`
- Validation interpretation: tests pass, but they assert incomplete enum vocabulary and therefore do not satisfy the story acceptance criterion for required gate types and decision states.

## Cleanup Status
- Checked reviewed product/test scope for generated `__pycache__` and `.pytest_cache` directories after validation.
- No cleanup artifacts were found under `reviewflow/` or `tests/`.

## Required Rework Contract
- Update `GateType` to use the required product gate types named by the governing workflow vocabulary, including `strategic_pre_review`, `tactical_pre_review`, `story_review`, `milestone_final_review`, and `strategic_final_review`.
- Update `DecisionState` to include the complete workflow action vocabulary required by the review-gate engine.
- Update focused tests so they fail on omitted required gate types or decision states.
- Keep the implementation within the original story boundary: importable package foundation, explicit data vocabulary, and focused tests only.

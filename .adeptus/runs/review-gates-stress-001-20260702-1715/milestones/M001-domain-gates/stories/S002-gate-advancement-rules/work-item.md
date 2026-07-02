# Work Item: S002-gate-advancement-rules

## Identity
- run_id: review-gates-stress-001-20260702-1715
- milestone_id: M001-domain-gates
- story_id: S002-gate-advancement-rules

## Changed Behavior
- Added deterministic in-memory gate advancement evaluation under `reviewflow.evaluator`.
- Story completion is allowed only when the story's matching `story_post_review` gate has an approved latest decision.
- Milestone completion is allowed only when every story can complete and the milestone's matching `milestone_post_review` gate has an approved latest decision.
- Final run success is allowed only when every milestone can complete and the run's matching `strategic_final_review` gate has an approved latest decision.
- Tool execution is allowed only when the relevant `tool_request_review` gate has an approved latest decision.
- Non-approved, missing, or undecided matching gates block advancement.

## Changed Files
- `reviewflow/evaluator.py`: added `AdvancementEvaluation` and deterministic gate evaluation functions.
- `reviewflow/__init__.py`: exported evaluator result/function API.
- `tests/test_domain_vocabulary.py`: updated package export expectation for the new evaluator API.
- `tests/test_gate_advancement_rules.py`: added focused S002 acceptance coverage.

## Files Read
- `.adeptus/runs/review-gates-stress-001-20260702-1715/packets/M001-domain-gates/S002-gate-advancement-rules/story-packet.md`
- `reviewflow/__init__.py`
- `reviewflow/domain.py`
- `tests/test_domain_vocabulary.py`
- Focused repository listing for package/test layout.

## Tests
- Command: `PYTHONDONTWRITEBYTECODE=1 python -B -m pytest -q -p no:cacheprovider tests/test_gate_advancement_rules.py tests/test_domain_vocabulary.py`
- Result: passed, `8 passed in 0.02s`.
- Command: `adeptus_pytest` with args `-q tests/test_gate_advancement_rules.py tests/test_domain_vocabulary.py`
- Result: passed, `8 passed in 0.02s`; cleanup reported zero removed artifacts and zero cleanup errors.

## Validation Evidence
- `test_story_completion_requires_approved_story_post_review` verifies story completion blocks before approval and allows after approval.
- `test_milestone_completion_requires_complete_stories_and_post_review` verifies milestone completion blocks on incomplete stories or missing milestone review and allows when both are satisfied.
- `test_final_run_success_requires_complete_milestones_and_final_review` verifies final run success blocks on incomplete milestones or missing strategic final review and allows when both are satisfied.
- `test_tool_execution_requires_approved_tool_request_review` verifies tool execution blocks before approved tool-request review and allows after approval.

## Runtime Cleanup
- Validation ran with bytecode writing and pytest cache provider disabled.
- Checked for `__pycache__` and `.pytest_cache`; none were present after shell validation.
- `adeptus_pytest` cleanup reported zero removed artifacts and zero cleanup errors.

## Blockers
- None.

## Tool Needs
- No implementation tool need. No `tool-request.md` was created.
- Inquisitor `story_review` submission tool was not callable in this session after focused tool discovery for `inquisitor_gatekeeper story_review` and `story_review inquisitor_gatekeeper`.

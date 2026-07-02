import reviewflow


def test_prepare_worker_context_excludes_forbidden_control_fields():
    context = {
        "current_state_path": ".adeptus/runs/run/state/current.json",
        "next_action": "implement_story",
        "exact_next_action": "read sibling story",
        "repair_count": 2,
        "final_action": "complete_run",
        "terminal_reason": "full stop",
        "story_id": "S002-context-helper-tests",
    }

    prepared = reviewflow.prepare_worker_context(context)

    assert reviewflow.CONTROL_CONTEXT_FIELDS == {
        "current_state_path",
        "next_action",
        "exact_next_action",
        "repair_count",
        "final_action",
        "terminal_reason",
    }
    assert not (set(prepared) & reviewflow.CONTROL_CONTEXT_FIELDS)
    assert prepared == {"story_id": "S002-context-helper-tests"}


def test_prepare_worker_context_preserves_task_relevant_fields_unchanged():
    acceptance_criteria = (
        "excludes forbidden control fields",
        "preserves task-relevant fields",
    )
    dependency_contracts = {
        "S001-context-helper-contract": "provides helper API under test",
    }
    context = {
        "run_id": "review-gates-stress-001-20260702-1715",
        "milestone_id": "M002-context-containment",
        "story_id": "S002-context-helper-tests",
        "acceptance_criteria": acceptance_criteria,
        "dependency_contracts": dependency_contracts,
        "allowed_files": ("tests/test_context_containment.py",),
        "next_action": "internal controller action",
    }

    prepared = reviewflow.prepare_worker_context(context)

    assert prepared == {
        "run_id": "review-gates-stress-001-20260702-1715",
        "milestone_id": "M002-context-containment",
        "story_id": "S002-context-helper-tests",
        "acceptance_criteria": acceptance_criteria,
        "dependency_contracts": dependency_contracts,
        "allowed_files": ("tests/test_context_containment.py",),
    }
    assert prepared["acceptance_criteria"] is acceptance_criteria
    assert prepared["dependency_contracts"] is dependency_contracts

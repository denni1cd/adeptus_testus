import reviewflow


def test_package_exports_required_domain_vocabulary():
    assert set(reviewflow.__all__) == {
        "DecisionState",
        "FailureDossierEntry",
        "GateDecision",
        "GateType",
        "Milestone",
        "ReviewGate",
        "Run",
        "Story",
        "AdvancementEvaluation",
        "CONTROL_CONTEXT_FIELDS",
        "can_continue_implementation",
        "can_complete_milestone",
        "can_complete_run",
        "can_complete_story",
        "can_execute_tool_request",
        "prepare_worker_context",
    }


def test_gate_types_are_explicit():
    assert {gate_type.value for gate_type in reviewflow.GateType} == {
        "strategic_pre_review",
        "story_post_review",
        "milestone_post_review",
        "strategic_final_review",
        "tool_request_review",
    }


def test_decision_states_are_explicit():
    assert {state.value for state in reviewflow.DecisionState} == {
        "approved",
        "requires_rework",
        "blocked_user_input_required",
        "full_stop",
    }


def test_domain_objects_hold_gate_evaluation_vocabulary():
    decision = reviewflow.GateDecision(
        state=reviewflow.DecisionState.REQUIRES_REWORK,
        rationale="Implementation did not satisfy the story contract.",
        reviewer="inquisitor_gatekeeper",
        decided_at="2026-07-02T17:15:00-04:00",
    )
    dossier_entry = reviewflow.FailureDossierEntry(
        decision_state=decision.state,
        summary="Missing focused tests.",
        evidence=("tests/test_domain_vocabulary.py",),
        required_action="Add acceptance coverage.",
    )
    gate = reviewflow.ReviewGate(
        gate_type=reviewflow.GateType.STORY_POST_REVIEW,
        subject_id="S001-package-domain-foundation",
        decisions=(decision,),
        failure_dossier=(dossier_entry,),
    )
    story = reviewflow.Story(
        story_id="S001-package-domain-foundation",
        title="Package domain foundation",
        gates=(gate,),
    )
    milestone = reviewflow.Milestone(
        milestone_id="M001-domain-gates",
        stories=(story,),
    )
    run = reviewflow.Run(
        run_id="review-gates-stress-001-20260702-1715",
        milestones=(milestone,),
    )

    assert run.milestones[0].stories[0].gates[0].decisions[0].state == (
        reviewflow.DecisionState.REQUIRES_REWORK
    )
    assert gate.failure_dossier[0].evidence == ("tests/test_domain_vocabulary.py",)

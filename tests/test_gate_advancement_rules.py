import reviewflow


def decision(state):
    return reviewflow.GateDecision(state=state, rationale=f"{state.value} gate")


def gate(gate_type, subject_id, state):
    return reviewflow.ReviewGate(
        gate_type=gate_type,
        subject_id=subject_id,
        decisions=(decision(state),),
    )


def approved(gate_type, subject_id):
    return gate(gate_type, subject_id, reviewflow.DecisionState.APPROVED)


def rejected(gate_type, subject_id):
    return gate(gate_type, subject_id, reviewflow.DecisionState.REQUIRES_REWORK)


def complete_story(story_id="S002-gate-advancement-rules"):
    return reviewflow.Story(
        story_id=story_id,
        gates=(approved(reviewflow.GateType.STORY_POST_REVIEW, story_id),),
    )


def complete_milestone(milestone_id="M001-domain-gates"):
    return reviewflow.Milestone(
        milestone_id=milestone_id,
        stories=(complete_story(),),
        gates=(approved(reviewflow.GateType.MILESTONE_POST_REVIEW, milestone_id),),
    )


def test_story_completion_requires_approved_story_post_review():
    story_id = "S002-gate-advancement-rules"
    no_gate_story = reviewflow.Story(story_id=story_id)
    rejected_story = reviewflow.Story(
        story_id=story_id,
        gates=(rejected(reviewflow.GateType.STORY_POST_REVIEW, story_id),),
    )
    approved_story = complete_story(story_id)

    assert not reviewflow.can_complete_story(no_gate_story).allowed
    assert not reviewflow.can_complete_story(rejected_story).allowed
    assert reviewflow.can_complete_story(approved_story).allowed


def test_milestone_completion_requires_complete_stories_and_post_review():
    milestone_id = "M001-domain-gates"
    incomplete_story = reviewflow.Story(story_id="S002-gate-advancement-rules")
    milestone_with_incomplete_story = reviewflow.Milestone(
        milestone_id=milestone_id,
        stories=(incomplete_story,),
        gates=(approved(reviewflow.GateType.MILESTONE_POST_REVIEW, milestone_id),),
    )
    milestone_without_gate = reviewflow.Milestone(
        milestone_id=milestone_id,
        stories=(complete_story(),),
    )
    milestone_with_gate = complete_milestone(milestone_id)

    assert not reviewflow.can_complete_milestone(milestone_with_incomplete_story).allowed
    assert not reviewflow.can_complete_milestone(milestone_without_gate).allowed
    assert reviewflow.can_complete_milestone(milestone_with_gate).allowed


def test_final_run_success_requires_complete_milestones_and_final_review():
    run_id = "review-gates-stress-001-20260702-1715"
    incomplete_milestone = reviewflow.Milestone(milestone_id="M001-domain-gates")
    run_with_incomplete_milestone = reviewflow.Run(
        run_id=run_id,
        milestones=(incomplete_milestone,),
        gates=(approved(reviewflow.GateType.STRATEGIC_FINAL_REVIEW, run_id),),
    )
    run_without_final_review = reviewflow.Run(
        run_id=run_id,
        milestones=(complete_milestone(),),
    )
    run_with_final_review = reviewflow.Run(
        run_id=run_id,
        milestones=(complete_milestone(),),
        gates=(approved(reviewflow.GateType.STRATEGIC_FINAL_REVIEW, run_id),),
    )

    assert not reviewflow.can_complete_run(run_with_incomplete_milestone).allowed
    assert not reviewflow.can_complete_run(run_without_final_review).allowed
    assert reviewflow.can_complete_run(run_with_final_review).allowed


def test_tool_execution_requires_approved_tool_request_review():
    tool_request_id = "tool-request-001"
    no_gate_evaluation = reviewflow.can_execute_tool_request(tool_request_id, ())
    rejected_evaluation = reviewflow.can_execute_tool_request(
        tool_request_id,
        (rejected(reviewflow.GateType.TOOL_REQUEST_REVIEW, tool_request_id),),
    )
    approved_evaluation = reviewflow.can_execute_tool_request(
        tool_request_id,
        (approved(reviewflow.GateType.TOOL_REQUEST_REVIEW, tool_request_id),),
    )

    assert not no_gate_evaluation.allowed
    assert not rejected_evaluation.allowed
    assert approved_evaluation.allowed

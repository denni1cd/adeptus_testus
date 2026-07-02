import pytest

import reviewflow


@pytest.mark.parametrize(
    "state",
    (
        reviewflow.DecisionState.REQUIRES_REWORK,
        reviewflow.DecisionState.BLOCKED_USER_INPUT_REQUIRED,
        reviewflow.DecisionState.FULL_STOP,
    ),
)
def test_non_approved_story_gate_decisions_create_source_dossier(state):
    story_id = "S003-failure-dossier-decisions"
    story = reviewflow.Story(
        story_id=story_id,
        gates=(
            reviewflow.ReviewGate(
                gate_type=reviewflow.GateType.STORY_POST_REVIEW,
                subject_id=story_id,
                decisions=(
                    reviewflow.GateDecision(
                        state=state,
                        rationale=f"{state.value} review outcome",
                    ),
                ),
            ),
        ),
    )

    evaluation = reviewflow.can_complete_story(story)

    assert not evaluation.allowed
    assert len(evaluation.failure_dossier) == 1
    dossier = evaluation.failure_dossier[0]
    assert dossier.decision_state == state
    assert dossier.gate_type == reviewflow.GateType.STORY_POST_REVIEW
    assert dossier.subject_id == story_id
    assert "gate_type=story_post_review" in dossier.evidence
    assert f"subject_id={story_id}" in dossier.evidence
    assert f"decision_state={state.value}" in dossier.evidence
    assert dossier.required_action


def test_user_input_required_decision_blocks_until_input_available():
    gate = reviewflow.ReviewGate(
        gate_type=reviewflow.GateType.STORY_POST_REVIEW,
        subject_id="S003-failure-dossier-decisions",
        decisions=(
            reviewflow.GateDecision(
                state=reviewflow.DecisionState.BLOCKED_USER_INPUT_REQUIRED,
                rationale="Need an operator decision.",
            ),
        ),
    )

    blocked = reviewflow.can_continue_implementation((gate,))
    resumed = reviewflow.can_continue_implementation(
        (gate,),
        user_input_available=True,
    )

    assert not blocked.allowed
    assert blocked.implementation_blocked
    assert blocked.user_input_required
    assert not blocked.terminal_stop
    assert blocked.failure_dossier[0].decision_state == (
        reviewflow.DecisionState.BLOCKED_USER_INPUT_REQUIRED
    )

    assert resumed.allowed
    assert not resumed.implementation_blocked
    assert resumed.user_input_required
    assert resumed.failure_dossier[0].decision_state == (
        reviewflow.DecisionState.BLOCKED_USER_INPUT_REQUIRED
    )


def test_full_stop_decision_always_blocks_implementation():
    gate = reviewflow.ReviewGate(
        gate_type=reviewflow.GateType.MILESTONE_POST_REVIEW,
        subject_id="M001-domain-gates",
        decisions=(
            reviewflow.GateDecision(
                state=reviewflow.DecisionState.FULL_STOP,
                rationale="Terminal review condition.",
            ),
        ),
    )

    evaluation = reviewflow.can_continue_implementation(
        (gate,),
        user_input_available=True,
    )

    assert not evaluation.allowed
    assert evaluation.implementation_blocked
    assert evaluation.terminal_stop
    assert not evaluation.user_input_required
    assert evaluation.failure_dossier[0].decision_state == (
        reviewflow.DecisionState.FULL_STOP
    )

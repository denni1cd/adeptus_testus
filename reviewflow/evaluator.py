"""Deterministic advancement checks for review gate workflows."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from .domain import (
    DecisionState,
    FailureDossierEntry,
    GateType,
    Milestone,
    ReviewGate,
    Run,
    Story,
)


@dataclass(frozen=True, slots=True)
class AdvancementEvaluation:
    """Result of an advancement check."""

    allowed: bool
    reason: str
    required_gate: GateType | None = None
    subject_id: str | None = None
    failure_dossier: tuple[FailureDossierEntry, ...] = field(default_factory=tuple)
    implementation_blocked: bool = False
    user_input_required: bool = False
    terminal_stop: bool = False


def can_complete_story(story: Story) -> AdvancementEvaluation:
    """Return whether a story can be marked complete."""

    latest_gate = _latest_matching_gate(
        story.gates,
        GateType.STORY_POST_REVIEW,
        story.story_id,
    )
    if _is_approved_gate(latest_gate):
        return AdvancementEvaluation(
            allowed=True,
            reason="Story has an approved story post-review.",
            required_gate=GateType.STORY_POST_REVIEW,
            subject_id=story.story_id,
        )

    dossier = _failure_dossier_for_gate(latest_gate)
    return AdvancementEvaluation(
        allowed=False,
        reason="Story completion requires an approved story post-review.",
        required_gate=GateType.STORY_POST_REVIEW,
        subject_id=story.story_id,
        failure_dossier=dossier,
        **_stop_flags(dossier),
    )


def can_complete_milestone(milestone: Milestone) -> AdvancementEvaluation:
    """Return whether a milestone can be marked complete."""

    for story in milestone.stories:
        story_evaluation = can_complete_story(story)
        if not story_evaluation.allowed:
            return AdvancementEvaluation(
                allowed=False,
                reason=f"Milestone completion is blocked by incomplete story {story.story_id}.",
                required_gate=story_evaluation.required_gate,
                subject_id=story.story_id,
                failure_dossier=story_evaluation.failure_dossier,
                implementation_blocked=story_evaluation.implementation_blocked,
                user_input_required=story_evaluation.user_input_required,
                terminal_stop=story_evaluation.terminal_stop,
            )

    latest_gate = _latest_matching_gate(
        milestone.gates,
        GateType.MILESTONE_POST_REVIEW,
        milestone.milestone_id,
    )
    if _is_approved_gate(latest_gate):
        return AdvancementEvaluation(
            allowed=True,
            reason="Milestone stories are complete and milestone post-review is approved.",
            required_gate=GateType.MILESTONE_POST_REVIEW,
            subject_id=milestone.milestone_id,
        )

    dossier = _failure_dossier_for_gate(latest_gate)
    return AdvancementEvaluation(
        allowed=False,
        reason="Milestone completion requires an approved milestone post-review.",
        required_gate=GateType.MILESTONE_POST_REVIEW,
        subject_id=milestone.milestone_id,
        failure_dossier=dossier,
        **_stop_flags(dossier),
    )


def can_complete_run(run: Run) -> AdvancementEvaluation:
    """Return whether a run can be marked finally successful."""

    for milestone in run.milestones:
        milestone_evaluation = can_complete_milestone(milestone)
        if not milestone_evaluation.allowed:
            return AdvancementEvaluation(
                allowed=False,
                reason=(
                    "Final run success is blocked by incomplete milestone "
                    f"{milestone.milestone_id}."
                ),
                required_gate=milestone_evaluation.required_gate,
                subject_id=milestone.milestone_id,
                failure_dossier=milestone_evaluation.failure_dossier,
                implementation_blocked=milestone_evaluation.implementation_blocked,
                user_input_required=milestone_evaluation.user_input_required,
                terminal_stop=milestone_evaluation.terminal_stop,
            )

    latest_gate = _latest_matching_gate(
        run.gates,
        GateType.STRATEGIC_FINAL_REVIEW,
        run.run_id,
    )
    if _is_approved_gate(latest_gate):
        return AdvancementEvaluation(
            allowed=True,
            reason="Milestones are complete and strategic final review is approved.",
            required_gate=GateType.STRATEGIC_FINAL_REVIEW,
            subject_id=run.run_id,
        )

    dossier = _failure_dossier_for_gate(latest_gate)
    return AdvancementEvaluation(
        allowed=False,
        reason="Final run success requires an approved strategic final review.",
        required_gate=GateType.STRATEGIC_FINAL_REVIEW,
        subject_id=run.run_id,
        failure_dossier=dossier,
        **_stop_flags(dossier),
    )


def can_execute_tool_request(
    tool_request_id: str,
    gates: Iterable[ReviewGate],
) -> AdvancementEvaluation:
    """Return whether a requested tool execution can proceed."""

    latest_gate = _latest_matching_gate(
        gates,
        GateType.TOOL_REQUEST_REVIEW,
        tool_request_id,
    )
    if _is_approved_gate(latest_gate):
        return AdvancementEvaluation(
            allowed=True,
            reason="Tool request review is approved.",
            required_gate=GateType.TOOL_REQUEST_REVIEW,
            subject_id=tool_request_id,
        )

    dossier = _failure_dossier_for_gate(latest_gate)
    return AdvancementEvaluation(
        allowed=False,
        reason="Tool execution requires an approved tool request review.",
        required_gate=GateType.TOOL_REQUEST_REVIEW,
        subject_id=tool_request_id,
        failure_dossier=dossier,
        **_stop_flags(dossier),
    )


def can_continue_implementation(
    gates: Iterable[ReviewGate],
    *,
    user_input_available: bool = False,
) -> AdvancementEvaluation:
    """Return whether implementation work may continue after gate decisions."""

    failure_dossier = tuple(
        entry
        for gate in gates
        for entry in _failure_dossier_for_gate(gate)
    )
    flags = _stop_flags(failure_dossier)

    if flags["terminal_stop"]:
        return AdvancementEvaluation(
            allowed=False,
            reason="Implementation is blocked by a terminal full-stop decision.",
            failure_dossier=failure_dossier,
            **flags,
        )

    if flags["user_input_required"] and not user_input_available:
        return AdvancementEvaluation(
            allowed=False,
            reason="Implementation is blocked until required user input is available.",
            failure_dossier=failure_dossier,
            **flags,
        )

    return AdvancementEvaluation(
        allowed=True,
        reason="Implementation may continue.",
        failure_dossier=failure_dossier,
        user_input_required=flags["user_input_required"],
    )


def _latest_matching_gate(
    gates: Iterable[ReviewGate],
    gate_type: GateType,
    subject_id: str,
) -> ReviewGate | None:
    matching_gates = [
        gate
        for gate in gates
        if gate.gate_type == gate_type and gate.subject_id == subject_id
    ]
    if not matching_gates:
        return None
    return matching_gates[-1]


def _is_approved_gate(gate: ReviewGate | None) -> bool:
    if gate is None or not gate.decisions:
        return False
    return gate.decisions[-1].state == DecisionState.APPROVED


def _failure_dossier_for_gate(
    gate: ReviewGate | None,
) -> tuple[FailureDossierEntry, ...]:
    if gate is None or not gate.decisions:
        return ()

    decision = gate.decisions[-1]
    if decision.state == DecisionState.APPROVED:
        return ()

    return (
        FailureDossierEntry(
            decision_state=decision.state,
            summary=(
                f"{gate.gate_type.value} for {gate.subject_id} recorded "
                f"{decision.state.value}."
            ),
            gate_type=gate.gate_type,
            subject_id=gate.subject_id,
            evidence=(
                f"gate_type={gate.gate_type.value}",
                f"subject_id={gate.subject_id}",
                f"decision_state={decision.state.value}",
                f"rationale={decision.rationale}",
            ),
            required_action=_required_action_for(decision.state),
        ),
    )


def _required_action_for(state: DecisionState) -> str:
    if state == DecisionState.REQUIRES_REWORK:
        return "Repair the failed work item and resubmit review evidence."
    if state == DecisionState.BLOCKED_USER_INPUT_REQUIRED:
        return "Obtain required user input before continuing implementation."
    if state == DecisionState.FULL_STOP:
        return "Stop implementation work until the terminal condition is externally resolved."
    return "No failure action required."


def _stop_flags(
    failure_dossier: tuple[FailureDossierEntry, ...],
) -> dict[str, bool]:
    states = {entry.decision_state for entry in failure_dossier}
    terminal_stop = DecisionState.FULL_STOP in states
    user_input_required = DecisionState.BLOCKED_USER_INPUT_REQUIRED in states
    return {
        "implementation_blocked": terminal_stop or user_input_required,
        "user_input_required": user_input_required,
        "terminal_stop": terminal_stop,
    }

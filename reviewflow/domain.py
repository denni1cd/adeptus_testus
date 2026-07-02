"""Data-only domain objects for review gate workflows."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class GateType(StrEnum):
    """Review gate kinds used by the workflow."""

    STRATEGIC_PRE_REVIEW = "strategic_pre_review"
    STORY_POST_REVIEW = "story_post_review"
    MILESTONE_POST_REVIEW = "milestone_post_review"
    STRATEGIC_FINAL_REVIEW = "strategic_final_review"
    TOOL_REQUEST_REVIEW = "tool_request_review"


class DecisionState(StrEnum):
    """Terminal decision states a review gate can record."""

    APPROVED = "approved"
    REQUIRES_REWORK = "requires_rework"
    BLOCKED_USER_INPUT_REQUIRED = "blocked_user_input_required"
    FULL_STOP = "full_stop"


@dataclass(frozen=True, slots=True)
class GateDecision:
    """Recorded outcome vocabulary for a review gate."""

    state: DecisionState
    rationale: str
    reviewer: str | None = None
    decided_at: str | None = None


@dataclass(frozen=True, slots=True)
class FailureDossierEntry:
    """Evidence vocabulary for a failed gate decision."""

    decision_state: DecisionState
    summary: str
    gate_type: GateType | None = None
    subject_id: str | None = None
    evidence: tuple[str, ...] = field(default_factory=tuple)
    required_action: str | None = None


@dataclass(frozen=True, slots=True)
class ReviewGate:
    """A data-only gate record for a workflow object."""

    gate_type: GateType
    subject_id: str
    decisions: tuple[GateDecision, ...] = field(default_factory=tuple)
    failure_dossier: tuple[FailureDossierEntry, ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class Story:
    """Story-level unit reviewed by a story gate."""

    story_id: str
    title: str | None = None
    gates: tuple[ReviewGate, ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class Milestone:
    """Milestone-level grouping of stories and gates."""

    milestone_id: str
    stories: tuple[Story, ...] = field(default_factory=tuple)
    gates: tuple[ReviewGate, ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class Run:
    """Top-level workflow run."""

    run_id: str
    milestones: tuple[Milestone, ...] = field(default_factory=tuple)
    gates: tuple[ReviewGate, ...] = field(default_factory=tuple)

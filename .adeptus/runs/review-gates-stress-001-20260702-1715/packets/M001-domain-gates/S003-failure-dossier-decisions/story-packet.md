# Story Packet: S003-failure-dossier-decisions

## Identity
- run_id: review-gates-stress-001-20260702-1715
- milestone_id: M001-domain-gates
- story_id: S003-failure-dossier-decisions
- story_path: `.adeptus/runs/review-gates-stress-001-20260702-1715/milestones/M001-domain-gates/stories/S003-failure-dossier-decisions/`

## Primary Behavioral Contract
Create deterministic failure dossier entries for non-approved gate decisions and enforce stop behavior for user-input and terminal decisions.

## Inputs
- Milestone tactical plan for M001-domain-gates.
- This story packet.
- Approved outputs and public contracts from `S001-package-domain-foundation` and `S002-gate-advancement-rules`.

## Expected Outputs
- Evaluator creates `FailureDossierEntry` records for `requires_rework`, `blocked_user_input_required`, and `full_stop` decisions.
- `blocked_user_input_required` prevents further implementation work until user input is supplied.
- `full_stop` prevents further implementation work as a terminal condition.
- Focused tests cover each required non-approved decision state.

## Acceptance Criteria
1. `requires_rework`, `blocked_user_input_required`, and `full_stop` gate decisions each produce a failure dossier entry with enough source context to identify the gate and decision.
2. `blocked_user_input_required` blocks further implementation work until user input is represented as available.
3. `full_stop` always blocks further implementation work as terminal.

## Dependency Contracts
- `S001-package-domain-foundation`: provides importable package, `GateDecision`, and `FailureDossierEntry` vocabulary.
- `S002-gate-advancement-rules`: provides evaluator entry point and advancement result shape.

## Change Boundary
- May extend evaluator result data structures and domain fields only as needed to represent failure dossiers and stop behavior.
- May add focused tests for dossier creation and user-input/full-stop blocking.
- May adjust S002 tests only if required to keep evaluator result assertions aligned with this story's output shape.

## Non-Goals
- Do not implement CLI reporting, context containment, product documentation, audit reporting, sample-data UX, sibling-story work outside the named dependency contracts, broad regression expansion, unrelated refactors, networking, databases, async execution, web UI, external APIs, persistence, or MCP tool changes.

## Test Policy
- Add or modify only tests that directly verify this story's acceptance criteria.
- Prefer deterministic in-memory gate decision fixtures.
- Use `python -B -m pytest -q -p no:cacheprovider` or a narrower focused pytest invocation covering this story.

## Stop Condition
- Stop when focused validation for failure dossier creation and implementation-stop behavior passes, or when a blocker is found that requires packet repair or reviewed tool escalation.

# Story Packet: S002-gate-advancement-rules

## Identity
- run_id: review-gates-stress-001-20260702-1715
- milestone_id: M001-domain-gates
- story_id: S002-gate-advancement-rules
- story_path: `.adeptus/runs/review-gates-stress-001-20260702-1715/milestones/M001-domain-gates/stories/S002-gate-advancement-rules/`

## Primary Behavioral Contract
Implement deterministic gate evaluation that blocks or allows workflow advancement according to the core review-gate order.

## Inputs
- Milestone tactical plan for M001-domain-gates.
- This story packet.
- Approved outputs and public contract from `S001-package-domain-foundation`.

## Expected Outputs
- A deterministic evaluator module or function that consumes the S001 domain objects or bounded declarative equivalents.
- Story completion is blocked until the story has an approved `story_post_review`.
- Milestone completion is blocked until all stories are complete and the milestone has an approved `milestone_post_review`.
- Final run success is blocked until strategic final review is approved.
- Tool execution is blocked until the relevant tool-request review is approved.

## Acceptance Criteria
1. Evaluator blocks story completion before approved `story_post_review` and allows it after approval.
2. Evaluator blocks milestone and final completion until their required prior completion and approval conditions are satisfied.
3. Evaluator blocks tool execution before approved `tool_request_review` and allows it after approval.

## Dependency Contracts
- `S001-package-domain-foundation`: provides importable package and explicit domain vocabulary.

## Change Boundary
- May add evaluator code under the `reviewflow` package.
- May extend S001 domain fields only when required to express this story's gate inputs and outputs.
- May add focused tests for advancement rules.

## Non-Goals
- Do not create failure dossier entry generation for non-approved decisions except for placeholders required by type signatures.
- Do not implement CLI reporting, context containment, product documentation, audit reporting, sample-data UX, sibling-story work, broad regression expansion, unrelated refactors, networking, databases, async execution, web UI, external APIs, persistence, or MCP tool changes.

## Test Policy
- Add or modify only tests that directly verify this story's advancement-rule acceptance criteria.
- Prefer deterministic in-memory test fixtures over file IO.
- Use `python -B -m pytest -q -p no:cacheprovider` or a narrower focused pytest invocation covering this story.

## Stop Condition
- Stop when focused validation for story, milestone, final, and tool-request advancement rules passes, or when a blocker is found that requires packet repair or reviewed tool escalation.

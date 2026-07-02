# Story Packet: S001-context-helper-contract

## Identity
- Run: `review-gates-stress-001-20260702-1715`
- Milestone: `M002-context-containment`
- Story: `S001-context-helper-contract`
- Title: Context helper behavioral contract

## Primary Behavioral Contract
Provide a small `reviewflow` package API that accepts bounded worker-context input from a caller and returns a prepared context mapping with internal control-state fields removed while preserving task-relevant non-control fields.

## Inputs
- A caller-provided mapping containing arbitrary JSON-like worker context fields.
- The forbidden field set from the M002 contract: `current_state_path`, `next_action`, `exact_next_action`, `repair_count`, `final_action`, `terminal_reason`.
- Existing package conventions from `reviewflow/__init__.py`, `reviewflow/domain.py`, and `reviewflow/evaluator.py`.

## Expected Outputs
- A new or updated `reviewflow` helper API, likely in a focused module such as `reviewflow/context.py`.
- Public or internal import exposure consistent with the existing `reviewflow.__init__` export pattern if the helper is intended as package API.
- Prepared context output that omits forbidden fields even when the input contains them.

## Acceptance Criteria
1. Preparing context from a mapping returns a new mapping that excludes every forbidden control field named by the M002 contract.
2. Non-control fields needed by workers, such as milestone/story identifiers, objective text, allowed paths, dependency summaries, or task instructions, remain available with their original values.
3. The helper is deterministic, side-effect free, and does not read `.adeptus/runs`, current state files, or any other runtime artifact path.

## Dependency Contracts
- `M001-domain-gates`: package is importable and follows small module plus `__init__` export conventions.

## Change Boundary
- May add one focused context helper module and minimal package export wiring.
- May not implement a packet generator, controller state machine, CLI behavior, documentation, persistence, MCP/tool behavior, or broad refactors.
- May not alter M001 gate evaluation semantics except for unavoidable import list maintenance.
- May not perform sibling-story test expansion beyond what is needed to keep imports coherent.

## Test Policy
- This story may add only minimal direct tests if needed to prove the helper contract during implementation.
- Prefer leaving full focused containment test coverage to `S002-context-helper-tests`.
- Do not add broad regression, CLI, docs, or gate-rule tests under this story.

## Stop Condition
- Stop when the helper contract is implemented and direct validation for the touched import path passes, or when a blocker shows that satisfying the helper would require exposing forbidden control-state, reading Adeptus runtime artifacts, broad refactor, or packet repair.

# Story Packet: S001-package-domain-foundation

## Identity
- run_id: review-gates-stress-001-20260702-1715
- milestone_id: M001-domain-gates
- story_id: S001-package-domain-foundation
- story_path: `.adeptus/runs/review-gates-stress-001-20260702-1715/milestones/M001-domain-gates/stories/S001-package-domain-foundation/`

## Primary Behavioral Contract
Create the minimal importable `reviewflow` package foundation and explicit domain model vocabulary required by the review-gate engine.

## Inputs
- Milestone tactical plan for M001-domain-gates.
- This story packet.
- Intake summary acceptance criteria AC01, AC02, AC03, and AC07 as quoted in the tactical plan.
- Focused repository setup: no existing product package, test suite, or Python packaging config was present at planning time.

## Expected Outputs
- `reviewflow` package can be imported.
- Domain model exposes `Run`, `Milestone`, `Story`, `ReviewGate`, `GateDecision`, and `FailureDossierEntry`.
- Gate types and decision states are represented explicitly, preferably with typed enums or equivalent deterministic constants.
- Focused tests verify importability and domain vocabulary.

## Acceptance Criteria
1. `import reviewflow` succeeds and exposes a bounded public package surface suitable for later CLI and docs work.
2. All required workflow objects are represented with fields sufficient for later gate evaluation.
3. All required gate types and decision states are represented explicitly and covered by focused tests.

## Dependency Contracts
- None.

## Change Boundary
- May create minimal product files under `reviewflow/`.
- May create focused tests under a conventional test path such as `tests/`.
- May add minimal Python packaging/test configuration only if needed to make imports or pytest deterministic.

## Non-Goals
- Do not implement CLI behavior beyond what is necessary for package import support.
- Do not implement gate advancement rules, failure dossier creation behavior, context containment, documentation, audit reporting, or sample-data output.
- Do not perform sibling-story work, future milestone work, broad regression expansion, unrelated refactors, networking, databases, async execution, web UI, external APIs, persistence, or MCP tool changes.

## Test Policy
- Add or modify only tests that verify this story's acceptance criteria.
- Prefer focused pytest such as `python -B -m pytest -q -p no:cacheprovider tests/<domain-test-file>.py`.
- Full milestone validation may use `python -B -m pytest -q -p no:cacheprovider` if inexpensive.

## Stop Condition
- Stop when focused validation for package import and domain vocabulary passes, or when a blocker is found that requires packet repair or reviewed tool escalation.

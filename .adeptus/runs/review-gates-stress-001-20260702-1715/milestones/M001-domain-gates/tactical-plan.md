# Tactical Plan: M001-domain-gates

## Milestone Contract
- run_id: review-gates-stress-001-20260702-1715
- milestone_id: M001-domain-gates
- planner_agent: lexmechanic_planner
- goal: Create the minimal `reviewflow` package foundation and deterministic gate engine enforcing core review-gate contract rules.

## Allowed Inputs
- `.adeptus/runs/review-gates-stress-001-20260702-1715/state/milestone-contracts/M001-domain-gates.json`
- `.adeptus/runs/review-gates-stress-001-20260702-1715/state/intake-summary.md`
- Focused repository overview for package/test setup: repository has no existing product package, test suite, or Python packaging config at planning time.

## Scope
- Establish an importable `reviewflow` Python package with a bounded module layout suitable for later CLI and documentation work.
- Represent `Run`, `Milestone`, `Story`, `ReviewGate`, `GateDecision`, and `FailureDossierEntry`.
- Represent gate types `strategic_pre_review`, `story_post_review`, `milestone_post_review`, `strategic_final_review`, and `tool_request_review`.
- Represent decision states `approved`, `requires_rework`, `blocked_user_input_required`, and `full_stop`.
- Implement deterministic evaluation rules for story, milestone, final, tool-request, user-input-stop, and failure-dossier behavior.

## Non-Goals
- No CLI behavior beyond minimal package support unless needed for import validation.
- No context-containment helper except a narrow model field if required by the domain model story.
- No product documentation beyond incidental docstrings.
- No networking, databases, async execution, web UI, external APIs, persistence, MCP tool changes, or production workflow framework behavior.
- No story implementation until `tactical_pre_review` returns `PASS`.

## Story Plan
| Story | Contract | Depends On | Packet |
| --- | --- | --- | --- |
| S001-package-domain-foundation | Create the importable package skeleton and explicit domain model vocabulary. | None | `.adeptus/runs/review-gates-stress-001-20260702-1715/packets/M001-domain-gates/S001-package-domain-foundation/story-packet.md` |
| S002-gate-advancement-rules | Add deterministic evaluator rules that block or allow workflow advancement from approved review gates. | S001-package-domain-foundation | `.adeptus/runs/review-gates-stress-001-20260702-1715/packets/M001-domain-gates/S002-gate-advancement-rules/story-packet.md` |
| S003-failure-dossier-decisions | Create failure dossier entries for non-approved decisions and enforce implementation stop behavior. | S001-package-domain-foundation, S002-gate-advancement-rules | `.adeptus/runs/review-gates-stress-001-20260702-1715/packets/M001-domain-gates/S003-failure-dossier-decisions/story-packet.md` |

## Dependency Policy
- Each story is completable from its own packet plus named dependency contracts.
- No story may read the full intake, full strategic plan, full workflow, `current-state.json`, sibling milestone contracts, unrelated run artifacts, or story audit archives.
- Later stories may use public code and tests produced by named dependency stories after those stories pass review.

## Test Policy
- Workers should use focused pytest coverage for their own acceptance criteria.
- Preferred validation command: `python -B -m pytest -q -p no:cacheprovider`.
- Narrower pytest invocation is acceptable during story work if it directly covers the story contract.
- Runtime cache/temp artifacts must be cleaned before handoff, including `__pycache__`, `.pytest_cache`, `.pytest-tmp*`, `.adeptus_pytest_tmp*`, `*.pyc`, and `*.pyo`.

## Milestone Acceptance Mapping
- AC01 package import foundation: S001.
- AC02 explicit workflow objects, gate types, and decision states: S001.
- AC03 deterministic story, milestone, final, tool request, and user-input stop rules: S002 and S003.
- Failure dossier entries for `requires_rework`, `blocked_user_input_required`, and `full_stop`: S003.

## Review Handoff
- Submit this tactical plan and the three story packets to `inquisitor_gatekeeper` for `tactical_pre_review`.
- Story implementation must not begin until the Inquisitor returns `PASS`.
- If review returns `FAIL_REWORK_MILESTONE`, repair this milestone plan and story packets and resubmit.
- If review returns `FAIL_REWORK_STRATEGY`, route upward to Magos rather than patching strategy locally.
- If review returns `STOP_USER_INPUT_REQUIRED` or `FULL_STOP`, surface the user question or stop reason.

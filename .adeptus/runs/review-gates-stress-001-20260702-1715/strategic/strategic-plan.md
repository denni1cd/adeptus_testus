# Strategic Plan

## Metadata
- run_id: review-gates-stress-001-20260702-1715
- strategic_thread_id: strategic-review-gates-stress-001
- agent: magos_strategos
- status: submitted
- source_of_truth: workflow.yaml
- strategic_contract_path: .adeptus/runs/review-gates-stress-001-20260702-1715/state/strategic-contract.json
- intake_summary_path: .adeptus/runs/review-gates-stress-001-20260702-1715/state/intake-summary.md

## Statement of Intent
Build a deliberately small Python command-line package named `reviewflow` that simulates contract-authoritative review gates for an agentic software-delivery workflow. The run must exercise Adeptus planning, review, implementation, milestone, and final gates without drifting into a production framework. Strategy is bounded to product package, tests, product documentation, sample CLI/audit output, and Adeptus audit artifacts. No product files are implemented by this strategic thread.

## Strategic Acceptance Criteria
| Criterion ID | Criterion | Evidence Required |
| --- | --- | --- |
| SAC01 | `reviewflow` package exists and runs with `python -m reviewflow`. | CLI smoke evidence from final validation. |
| SAC02 | Required workflow objects, gate types, and decision states are represented. | Focused tests and code review evidence. |
| SAC03 | Contract rules block invalid story, milestone, final, tool, and user-input transitions. | Unit tests for each required blocking rule. |
| SAC04 | Failure dossier entries are created for rework, full-stop, and user-input-required decisions. | Unit tests inspecting dossier behavior. |
| SAC05 | Worker context preparation excludes listed internal control fields. | Unit tests for forbidden field exclusion. |
| SAC06 | CLI prints gate decisions and final pass/fail for a valid built-in sample. | CLI smoke test and captured output summary. |
| SAC07 | Product documentation explains contract, order, states, context containment, and user-input behavior. | Documentation tests asserting stable key phrases. |
| SAC08 | Adeptus artifacts show required strategic, tactical, story, milestone, and final reviews with no unnecessary Toolwright activity. | Review decisions, milestone summaries, and final review evidence. |

## Architecture Design
Use a conventional small Python package layout. The expected product surface is a `reviewflow` package with deterministic domain/evaluation modules, a context-containment helper, a `__main__.py` CLI, tests under `tests/`, and product docs under a documentation path chosen by the tactical plan. The domain should explicitly represent the intake's objects, gate types, and decision states. The engine should evaluate declarative or built-in sample data without external services or persistence. The CLI should favor a built-in valid sample to keep scope bounded. Documentation must contain stable phrases that tests can assert without using Adeptus runtime artifacts as product documentation.

## Milestone Matrix
| Milestone ID | Contract Path | Planner Agent | Goal | Acceptance Criteria | Dependencies |
| --- | --- | --- | --- | --- | --- |
| M001-domain-gates | .adeptus/runs/review-gates-stress-001-20260702-1715/state/milestone-contracts/M001-domain-gates.json | lexmechanic_planner | Package foundation and deterministic gate engine. | Package imports; required objects/types/states; gate blocking rules; failure dossiers. | None. |
| M002-context-containment | .adeptus/runs/review-gates-stress-001-20260702-1715/state/milestone-contracts/M002-context-containment.json | lexmechanic_planner | Worker-safe downstream context preparation. | Helper returns task-relevant context; forbidden internal fields excluded; tests prove exclusion. | M001 package structure and needed identifiers. |
| M003-cli-audit | .adeptus/runs/review-gates-stress-001-20260702-1715/state/milestone-contracts/M003-cli-audit.json | lexmechanic_planner | CLI sample validation and audit output. | `python -m reviewflow` succeeds; decisions printed; final pass/fail printed; concise audit output. | M001; optional M002 if useful without coupling to control state. |
| M004-docs-validation | .adeptus/runs/review-gates-stress-001-20260702-1715/state/milestone-contracts/M004-docs-validation.json | lexmechanic_planner | Product docs and final validation coverage. | Docs cover required contract topics; tests assert docs and required behavior; final pytest and CLI evidence collected. | M001, M002, M003 complete. |

Each milestone row creates one milestone thread owned by one Lexmechanic Planner. Story-level planning belongs in tactical story packets, not this strategic plan.

## Context Contract Outputs
- intake_summary: .adeptus/runs/review-gates-stress-001-20260702-1715/state/intake-summary.md
- strategic_contract: .adeptus/runs/review-gates-stress-001-20260702-1715/state/strategic-contract.json
- milestone_contracts:
  - .adeptus/runs/review-gates-stress-001-20260702-1715/state/milestone-contracts/M001-domain-gates.json
  - .adeptus/runs/review-gates-stress-001-20260702-1715/state/milestone-contracts/M002-context-containment.json
  - .adeptus/runs/review-gates-stress-001-20260702-1715/state/milestone-contracts/M003-cli-audit.json
  - .adeptus/runs/review-gates-stress-001-20260702-1715/state/milestone-contracts/M004-docs-validation.json
- downstream_agents_must_not_read:
  - full intake
  - full strategic plan
  - full .adeptus/runs tree
  - full installed SKILL.md
  - full workflow.yaml
  - controller-owned current-state.json as live context

## Strategic Log
| Time | Decision | Evidence | Open Risk |
| --- | --- | --- | --- |
| 2026-07-02 17:15 America/New_York | Split non-trivial intake into four milestones: domain gates, context containment, CLI/audit, docs/validation. | Intake requires multiple milestones/stories, package, docs, tests, and process gates. | Tactical planners must keep stories small and avoid broad reconciliation buckets. |
| 2026-07-02 17:15 America/New_York | No tool request created. | Baseline file, shell, pytest, and passive Adeptus capabilities are sufficient; intake says tool creation is not expected. | If downstream implementation hits a real reusable capability gap, it must request reviewed tool escalation. |
| 2026-07-02 17:15 America/New_York | Downstream context is packet-only after strategic pre-review. | Workflow context contract and intake explicitly stress no control-state leakage. | Controller must avoid passing full intake/strategy to Lexmechanic or Enginseer prompts. |

## Tool Needs
not_applicable. No missing reusable MCP capability blocks strategy, and no `tool-request.md` is created.

## Inquisitor Handoff
- review_gate: strategic_pre_review
- next_required_agent: inquisitor_gatekeeper
- submitted_artifacts:
  - .adeptus/runs/review-gates-stress-001-20260702-1715/strategic/strategic-plan.md
  - .adeptus/runs/review-gates-stress-001-20260702-1715/state/intake-summary.md
  - .adeptus/runs/review-gates-stress-001-20260702-1715/state/strategic-contract.json
  - .adeptus/runs/review-gates-stress-001-20260702-1715/state/milestone-contracts/M001-domain-gates.json
  - .adeptus/runs/review-gates-stress-001-20260702-1715/state/milestone-contracts/M002-context-containment.json
  - .adeptus/runs/review-gates-stress-001-20260702-1715/state/milestone-contracts/M003-cli-audit.json
  - .adeptus/runs/review-gates-stress-001-20260702-1715/state/milestone-contracts/M004-docs-validation.json
- known_limits:
  - Product implementation, tactical plans, story packets, work items, reviews, and milestone summaries are intentionally not produced by Strategos.
  - Strategic pre-review must use the full intake plus submitted strategy artifacts; downstream planning after PASS must use packet-only context.

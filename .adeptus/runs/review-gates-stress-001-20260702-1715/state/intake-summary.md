# Intake Summary

## Metadata
- run_id: review-gates-stress-001-20260702-1715
- source_intake_path: review-gates-stress-001.intake.md
- produced_by: magos_strategos
- status: submitted

## Product Goal
- Build a small Python package named `reviewflow`.
- Provide a CLI runnable with `python -m reviewflow`.
- Model workflow objects: `Run`, `Milestone`, `Story`, `ReviewGate`, `GateDecision`, and `FailureDossierEntry`.
- Evaluate review gates from bounded declarative input or built-in sample data.
- Support gate types: `strategic_pre_review`, `story_post_review`, `milestone_post_review`, `strategic_final_review`, and `tool_request_review`.
- Support decision states: `approved`, `requires_rework`, `blocked_user_input_required`, and `full_stop`.
- Prepare downstream worker context while excluding internal control-state fields.
- Document the review-gate contract, required order, decision states, context containment, and user-input stop behavior.
- Add pytest coverage for gate rules, failure dossiers, context containment, docs alignment, and CLI smoke behavior.
- Produce a concise audit report showing gate decisions for sample inputs.

## Hard Constraints
- Keep scope intentionally small; no networking, databases, async execution, web UI, external APIs, or production framework behavior.
- Do not create new MCP tools unless an Inquisitor-approved tool request determines an unavoidable reusable capability gap.
- Runtime Adeptus artifacts must remain under `.adeptus/runs/...`; product documentation must live in the product documentation area.
- Downstream implementation context must exclude internal fields: `current_state_path`, `next_action`, `exact_next_action`, `repair_count`, `final_action`, and `terminal_reason`.
- Validation must include `python -B -m pytest -q -p no:cacheprovider` or equivalent and a CLI smoke test equivalent to `python -m reviewflow`.
- Adeptus process artifacts must demonstrate strategic, tactical, story, milestone, and final review gates before completion.

## Acceptance Criteria
- AC01: `reviewflow` package exists and can run via `python -m reviewflow`.
- AC02: Domain model represents all required workflow concepts, gate types, and decision states.
- AC03: Engine enforces contract rules for story, milestone, final run, tool request, user-input stop, and failure dossiers.
- AC04: Context preparation includes task-relevant fields and excludes internal control-state fields.
- AC05: CLI validates a built-in sample, prints gate decisions, and prints final pass/fail.
- AC06: Documentation states the review-gate contract, ordering, decision states, context containment, and user-input behavior.
- AC07: Tests cover all required rules, docs key phrases, context containment, and CLI success.
- AC08: Final validation and Adeptus audit artifacts show required review gates and no unnecessary Toolwright activity.

## Non-Goals
- No production workflow framework, persistence layer, external integration, web interface, async runtime, or broad plugin/tool system.
- No product implementation during strategic planning.
- No downstream dependence on the full intake, full strategic plan, full workflow, full `.adeptus/runs` tree, or controller state.

## Downstream Read Rule
Downstream agents read this summary instead of the full intake unless strategic final review or explicit escalation requires broader context.

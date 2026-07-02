# Adeptus Engineerium Intake: Review Gates Stress 001

## Requested action
Build a bounded Python command-line package named `reviewflow` that models an agentic software-delivery workflow with contract-authoritative review gates. The project should be intentionally small, but large enough to require multiple milestones, multiple stories, documentation updates, tests, and final validation.

The goal of this Adeptus run is not to build a production framework. The goal is to verify that Adeptus can follow its own process under non-trivial scope without drifting, skipping gates, leaking control-state into downstream agent context, or creating unnecessary tools.

## Target outcome
Create or update the target repository so that it contains a working Python package and documentation for a miniature review-gate simulator.

The finished repository should provide:

1. A package named `reviewflow`.
2. A CLI entry point runnable with `python -m reviewflow`.
3. A small workflow engine that evaluates review gates from declarative input.
4. Documentation that defines the review-gate contract.
5. Tests proving that implementation and documentation align.
6. A concise audit report showing which gate decisions were produced for sample inputs.

## Product requirements

### Workflow concepts
The implementation must model these workflow objects:

- `Run`
- `Milestone`
- `Story`
- `ReviewGate`
- `GateDecision`
- `FailureDossierEntry`

### Required review gates
The product must support these gate types:

- `strategic_pre_review`
- `story_post_review`
- `milestone_post_review`
- `strategic_final_review`
- `tool_request_review`

### Gate decision states
The product must support these decision states:

- `approved`
- `requires_rework`
- `blocked_user_input_required`
- `full_stop`

### Contract rules
The implementation and docs must make the following rules explicit:

1. The Inquisitor is the authority for review-gate advancement.
2. A story may not be marked complete until its post-story review is approved.
3. A milestone may not be marked complete until all stories are complete and milestone review is approved.
4. Final run success requires strategic final review approval.
5. A tool request may not be executed unless the tool-request review is approved.
6. If user input is required, the workflow must stop before further implementation work.
7. Failure dossier entries must be created for rework, full-stop, and user-input-required decisions.
8. Downstream implementation context must not receive internal control-state fields as live instructions.

### Context-containment requirement
Add a small module or function that prepares downstream worker context. It must include task-relevant fields, but it must exclude internal control fields such as:

- `current_state_path`
- `next_action`
- `exact_next_action`
- `repair_count`
- `final_action`
- `terminal_reason`

Tests must prove these fields are excluded from downstream worker context.

### CLI requirements
The CLI must support at least these commands or equivalent simple behavior:

- Validate a sample workflow.
- Print gate decisions.
- Print a final pass/fail result.

The CLI may use built-in sample data if that keeps the project bounded.

### Documentation requirements
Add documentation that explains:

- The review-gate contract.
- The required gate order.
- The meaning of each decision state.
- The context-containment rule.
- The expected behavior when user input is required.

The documentation must be specific enough that tests can assert key contract phrases exist.

### Testing requirements
Add pytest coverage for:

- Gate ordering.
- Story completion blocked before story review approval.
- Milestone completion blocked before milestone review approval.
- Final success blocked before strategic final approval.
- Tool execution blocked before tool-request review approval.
- Failure dossier creation on rework/user-input/full-stop.
- Context containment excludes internal state fields.
- CLI exits successfully for the valid built-in sample.

## Scope boundaries
Keep the implementation intentionally small. Do not add networking, databases, async execution, web UI, external APIs, or persistence beyond simple files if needed.

Do not create new MCP tools unless the Inquisitor determines that an existing required action cannot be completed with the baseline tools. Tool creation is not expected for this test.

Do not use generated runtime artifacts as product documentation. Runtime Adeptus documents belong under the Adeptus run directory; product documentation belongs in the target repository documentation area.

## Validation command
Use a validation command equivalent to:

```bash
python -B -m pytest -q -p no:cacheprovider
```

If the package exposes a CLI, also run a CLI smoke test equivalent to:

```bash
python -m reviewflow
```

## Expected Adeptus process behavior
This run should force Adeptus to produce and preserve normal run artifacts, including strategic planning, milestone/story planning, reviews, and final approval. It should not skip review gates simply because the code is small.

A successful Adeptus run should show:

- Strategic pre-review before implementation.
- Story-level reviews before story completion.
- Milestone-level reviews before milestone completion.
- Strategic final review before final pass.
- No unnecessary Toolwright activity.
- No uncontrolled broadening of scope.
- Tests passing at the end.

## Success criteria
The run is successful only if both are true:

1. The target product works and passes validation.
2. Adeptus run artifacts demonstrate that the review-gate contract was followed.

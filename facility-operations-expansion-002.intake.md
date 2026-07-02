# Adeptus Engineerium Test Intake

## Run ID

`facility-operations-expansion-002`

## Test packet location rule

This intake file is a raw root-level test packet file in the target repository.

Do not move this file into `.adeptus/intake/`.
Do not require the user to create an `.adeptus/intake/` copy.
The controller may read this root file as the intake source and may create normal Adeptus run artifacts under `.adeptus/runs/facility-operations-expansion-002/` as required by the workflow.

## Target repository

Repository: `denni1cd/adeptus_testus`

Initial repo state for this test: existing small Python project from the prior Adeptus Testus Facility run.

This is an expansion test, not a greenfield rewrite. The existing project behavior is now baseline behavior and must be preserved unless this intake explicitly changes it.

## Purpose of this test

This test validates whether Adeptus Engineerium can evolve an existing codebase while preserving prior behavior, using bounded context packets, multi-story planning, review gates, MCP validation, runtime cleanup, and the controller-repair boundary.

The run should prove that Adeptus can:

1. Inspect and preserve existing public behavior.
2. Expand the project in a controlled way without rewriting or replacing the prior implementation.
3. Decompose a larger change into multiple bounded stories.
4. Maintain context containment after strategic pre-review.
5. Validate through registered Adeptus MCP tools.
6. Confirm `adeptus_pytest` does not hang and reports `stdin: DEVNULL`.
7. Clean validation/runtime artifacts before final PASS.
8. Avoid controller-side product-file repair. Product implementation repairs must route through Enginseer + Inquisitor.

## Existing baseline to preserve

The existing project should already contain a Python package named `adeptus_testus`.

The following existing behavior must continue to work:

1. `python -m pytest -q`
2. `python -m adeptus_testus --until 12:00`
3. `python -m adeptus_testus --until 09:00`
4. The facility has exactly seven required rooms:
   - Dormitory
   - Kitchen
   - Workshop
   - Infirmary
   - Recreation
   - Garden
   - Control Room
5. Sarah starts the default normal-day scenario at 08:00 in Dormitory.
6. Sarah does not require sleep by 09:00 in the default normal-day scenario.
7. The deterministic default scenario advances through at least 12:00.
8. The renderer lists all seven rooms and marks Sarah's current room.
9. JSON save/load preserves simulation state.
10. Invalid room references or invalid movement fail predictably.
11. Existing tests remain meaningful and should not be deleted merely to make new tests pass.

If existing behavior is already broken before implementation, stop and report the baseline failure with evidence instead of overwriting the baseline.

## Requested action

Expand Adeptus Testus Facility into a deterministic facility-operations simulator.

Add pathing, travel time, scenario configuration, deterministic incidents, operations reporting, and expanded CLI support while preserving all baseline behavior.

The project must remain headless, deterministic, standard-library runtime only unless a new dependency is explicitly justified, and suitable for automated pytest validation.

## Required new capabilities

### 1. Facility graph and travel time

Add an explicit facility graph or layout model.

Requirements:

- Each of the seven required rooms must be represented in the graph.
- Movement should validate connectivity.
- Movement should support deterministic travel duration.
- Existing default scenario behavior must remain compatible.
- Invalid destination rooms and impossible routes must fail predictably.
- The graph must be testable without a GUI.

Suggested graph shape, unless the existing design makes a different simple shape better:

- Dormitory connects to Kitchen and Recreation.
- Kitchen connects to Dormitory and Workshop.
- Workshop connects to Kitchen and Control Room.
- Control Room connects to Workshop and Infirmary.
- Infirmary connects to Control Room and Garden.
- Garden connects to Infirmary and Recreation.
- Recreation connects to Garden and Dormitory.

This creates a loop and gives pathing meaningful behavior while remaining small.

### 2. Deterministic scenario configuration

Add support for named deterministic scenarios.

Requirements:

- Preserve the existing default scenario.
- Add at least one alternate named scenario, preferably `maintenance_day`.
- Scenario data should be serializable to and from JSON strings or JSON files.
- Scenario loading must validate room names and activity structure predictably.
- Scenario execution must remain deterministic, with no randomness or wall-clock dependence.

### 3. Deterministic incident system

Add a small deterministic incident model.

Requirements:

- Incidents are scheduled or scenario-defined, not random.
- Incidents have time, room, name, severity or category, effect, and resolution/handling note.
- At least two deterministic incident examples must exist in tests or sample scenarios.
- Incidents can affect needs, route, warnings, or report output.
- Incident behavior must be covered by tests.

Examples:

- Workshop equipment fault during maintenance.
- Garden air-quality alert during a walk.
- Control Room systems alert during review.

Use simple behavior. Do not create an event engine or scheduler framework beyond what is needed.

### 4. Operations reports

Add report generation after a simulation run.

Requirements:

- Report must include:
  - scenario name
  - start and end time
  - rooms visited
  - timeline of movements/actions
  - incidents encountered or handled
  - final needs
  - warnings, if any
- Provide at least text report output.
- Provide JSON report output if practical.
- Report generation must be deterministic and tested.

### 5. Expanded CLI

Keep the existing CLI behavior working.

Add options such as:

- `--until HH:MM`
- `--scenario default|maintenance_day`
- `--report text|json`
- `--show-timeline`

Exact names may vary if the implementation justifies a better small interface, but backward compatibility with `python -m adeptus_testus --until 12:00` is required.

CLI tests should remain headless and should not rely on terminal colors, curses, GUI, or external programs.

### 6. Documentation

Update README with:

- Existing basic preview command.
- New scenario/report commands.
- Project behavior summary.
- Facility graph explanation.
- Incident/report explanation.
- Test command.

Keep README concise.

## Required tests

Add or update tests to cover at least:

1. Existing baseline behavior still passes.
2. Facility graph includes all seven rooms.
3. Valid connected travel advances time deterministically.
4. Invalid route or invalid room fails predictably.
5. Default scenario remains deterministic and compatible.
6. `maintenance_day` or alternate scenario exists and runs deterministically.
7. Scenario JSON serialization/deserialization round trip works.
8. Invalid scenario JSON or invalid room references fail predictably.
9. At least two deterministic incidents are encountered or reported.
10. Operations text report includes scenario name, timeline, rooms visited, incidents, final needs, and warnings.
11. JSON report output is deterministic if implemented.
12. CLI preserves `--until` behavior and supports new scenario/report options.
13. Save/load still preserves relevant expanded state.
14. Test suite runs headlessly with pytest.

Tests should be focused and meaningful. Do not delete baseline tests unless they are replaced by equal or stronger coverage.

## Adeptus workflow requirements

Run the Adeptus Engineerium workflow normally.

The controller must:

1. Perform MCP target-root preflight before Strategos.
2. Use the root-level intake file as the user-provided intake source.
3. Not require the user to manually set `ADEPTUS_TARGET_REPO_ROOT`.
4. Create normal run artifacts under `.adeptus/runs/facility-operations-expansion-002/`.
5. Keep root packet files unchanged unless explicitly necessary.
6. Use bounded context packets for every non-strategic agent invocation.
7. Avoid broad reads after the phases where broad context is explicitly allowed.
8. Invoke Inquisitor reviews at the required gates.
9. Keep changes scoped to this intake.
10. Validate through the registered Adeptus MCP pytest tool, not only through a direct shell command.
11. Clean runtime cache/temp artifacts before final PASS.
12. Preserve prior `.adeptus/runs/` artifacts as audit records. Do not delete or rewrite old run artifacts.

## Controller repair boundary test requirement

This run must comply with the controller repair boundary.

The controller may not directly create, edit, or repair product implementation files, tests, docs, package/config files, package metadata, or other story deliverables during controller repair or final-review repair.

If validation, review, or final review discovers missing, incomplete, inconsistent, or absent product source files, tests, docs, package metadata, or other story deliverables, the controller must:

1. Create or update a bounded repair packet for the affected story.
2. Invoke the responsible Enginseer Implementer to perform the product-file repair.
3. Require Inquisitor Gatekeeper review of the repaired story output.
4. Re-run validation only after that implementation repair and review path completes.

The controller may perform narrow repair only on Adeptus run-state, routing, packet, review, validation-summary, and audit artifacts when the workflow explicitly allows it.

Do not allow the controller to silently become the implementer.

Final evidence should state whether the controller repair boundary was exercised, and if any repair occurred, which agent performed the product-file changes.

## Context discipline requirements

After strategic planning and strategic pre-review, downstream agents must not receive:

- Full installed `SKILL.md`
- Full `workflow.yaml`
- Full project tree
- Full `.adeptus/runs` tree
- Full intake unless explicitly allowed by the workflow phase
- Full strategic plan unless explicitly allowed by the workflow phase
- Generated cache or temp directories
- Old run artifacts except bounded summaries or explicitly named evidence needed for baseline preservation

Every non-strategic agent invocation must be driven by a bounded packet.

If a packet is insufficient, the agent must stop and request a narrower packet update or explicit escalation. It must not self-authorize broad context.

## Suggested milestone structure

This is a larger controlled test. Prefer more than one story, and use multiple milestones if useful.

A reasonable structure is:

1. Baseline preservation and design contract
   - Identify current public behavior.
   - Define compatibility contract.
   - Plan graph/scenario/report changes.
2. Facility graph and scenario expansion
   - Implement graph, travel time, scenario config, alternate scenario, and expanded serialization.
3. Incident/report/CLI expansion
   - Implement incidents, text/JSON report output, expanded CLI, docs, and tests.

The exact decomposition may vary, but avoid collapsing all work into an unreviewable blob if multiple bounded stories are more appropriate.

## Validation requirements

Final validation must include:

1. `adeptus_python_compile` or equivalent syntax evidence if available.
2. `adeptus_pytest(["-q"], timeout_seconds=60)` or similarly bounded pytest MCP invocation.
3. Evidence that the MCP pytest result includes `stdin: DEVNULL`.
4. Evidence that pytest did not time out.
5. Cleanup evidence from `adeptus_cleanup_runtime_artifacts` or the cleanup path included in `adeptus_pytest`.
6. A final check that no `.pytest_cache`, `__pycache__`, `.pyc`, `.pyo`, or temporary pytest artifacts remain outside protected `.adeptus/runs` artifacts.
7. Confirmation that old `.adeptus/runs/` artifacts were not deleted or rewritten.

## Required final state

The run may only report PASS if:

1. Strategic final review is PASS.
2. `.adeptus/runs/facility-operations-expansion-002/state/current-state.json` exists.
3. `current-state.json` contains:
   - `run_status: complete`
   - `final_action: PASS`
   - `terminal_reason: final strategic approval`
   - `final_review_repair_count` as an integer
4. The final response lists:
   - Baseline behavior preserved
   - Implementation summary
   - Tests run
   - MCP pytest evidence, including `stdin: DEVNULL`
   - Cleanup result
   - Files changed or created
   - Whether any repair occurred and whether controller repair boundary was followed
   - Remaining risks or explicit statement that no material risks are known

## Non-goals

Do not:

- Build a web app.
- Add authentication.
- Add a database.
- Add a network service.
- Add a GUI.
- Add curses, rich terminal UI, or terminal color dependencies.
- Add image generation.
- Add a game engine.
- Add random behavior.
- Add wall-clock-dependent behavior.
- Add complex dependency management.
- Create unrelated agent, MCP, or skill changes.
- Modify the installed Adeptus skill as part of this product test.
- Delete or rewrite prior `.adeptus/runs/` audit artifacts.
- Turn this into a broad framework rewrite.
- Leave validation artifacts or caches behind.

## Success definition

This test succeeds if Adeptus expands the existing project into a deterministic facility-operations simulator with preserved baseline behavior, graph/pathing, named scenarios, deterministic incidents, reports, expanded CLI/docs/tests, MCP validation through `adeptus_pytest` with `stdin: DEVNULL`, runtime cleanup, preserved old audit artifacts, and no controller-side product-file repair.

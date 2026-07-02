# Adeptus Engineerium Test Intake

## Run ID

`facility-realism-visual-advanced-001`

## Test packet location rule

This intake file is a raw root-level test packet file in the target repository.

Do not move this file into `.adeptus/intake/`.
Do not require the user to create an `.adeptus/intake/` copy.
The controller may read this root file as the intake source and may create normal Adeptus run artifacts under `.adeptus/runs/<run-id>/` as required by the workflow.

## Target repository

Repository: `denni1cd/adeptus_testus`

Initial repo state: intentionally empty or near-empty git repository.

This is a controlled greenfield test because the repository is empty. Do not assume an existing facility simulation app exists. Create a small but complete project that is large enough to exercise Adeptus planning, implementation, review, validation, cleanup, and final audit behavior.

## Purpose of this test

This test validates Adeptus Engineerium after the `adeptus_pytest` MCP stdio hardening merge.

The run should prove that Adeptus can:

1. Plan and implement a bounded multi-story greenfield project.
2. Maintain controlled scope and avoid unrelated feature drift.
3. Use bounded context packets after the strategic phase.
4. Validate through the registered Adeptus MCP pytest tool.
5. Confirm `adeptus_pytest` does not hang and reports `stdin: DEVNULL`.
6. Clean validation/runtime artifacts before final PASS.
7. Produce a final audit record that clearly separates changed implementation, validation evidence, cleanup evidence, and remaining risks.

## Requested action

Create a small Python project implementing a deterministic seven-room facility simulation with a clear headless visual representation and automated tests.

The project should be suitable for an empty repository and should not require a GUI, game engine, network service, database, or external API.

## Product concept

Build a simple facility simulation named **Adeptus Testus Facility**.

The simulation has one subject, **Sarah**, moving through a seven-room facility during a normal day. The facility should be understandable from code, tests, and a headless visual/text rendering.

The seven required rooms are:

1. Dormitory
2. Kitchen
3. Workshop
4. Infirmary
5. Recreation
6. Garden
7. Control Room

The simulation should include:

- A deterministic facility graph or layout.
- Sarah's current room.
- A normal-day scenario starting at 8:00 AM.
- Basic needs such as energy, hunger, morale, and health, or a similarly simple documented model.
- Actions or scheduled activities that affect location, time, and needs.
- A way to advance the simulation deterministically.
- A headless visual representation of the facility layout and Sarah's location/movement. This can be ASCII, text-grid, SVG string, HTML string, or another testable non-GUI rendering.
- JSON save/load behavior for simulation state.
- A small command-line entry point or documented command that runs or previews the simulation.

## Realism requirement

The normal-day rhythm must be plausible enough to catch absurd need decay.

Specific required behavioral contract:

- Sarah starts the normal-day scenario at 8:00 AM.
- Under the default normal-day scenario, Sarah must not require sleep by 9:00 AM.
- Hunger, energy, morale, and health changes must be bounded and documented.
- A deterministic normal-day simulation through at least 12:00 PM must be testable.
- Movement between rooms should be explicit enough that a reviewer can tell why Sarah is in each room.

The model does not need to be medically or physically realistic. It only needs to be internally coherent and avoid obviously absurd behavior.

## Project structure guidance

Prefer a simple, conventional Python project structure. For example:

- `README.md`
- `pyproject.toml`
- `src/adeptus_testus/`
- `tests/`

Use Python standard library where practical. `pytest` is acceptable for tests. Avoid mandatory third-party runtime dependencies unless there is a clear reason and the reason is documented.

Do not over-engineer the project.

## Required capabilities

The completed project must include all of the following:

1. Facility model with exactly the seven required rooms.
2. Deterministic normal-day scenario.
3. Sarah as the primary simulated subject.
4. Time advancement.
5. Need/state changes.
6. Movement/location tracking.
7. Headless visual/text rendering of layout and Sarah's location.
8. JSON save/load round trip.
9. Automated tests.
10. README instructions explaining how to run tests and preview the simulation.

## Required tests

Add automated tests that cover at least:

1. The facility has exactly the seven required rooms.
2. Sarah's normal-day scenario starts at 8:00 AM.
3. Sarah does not require sleep by 9:00 AM in the default normal-day scenario.
4. A deterministic normal-day run through at least 12:00 PM produces stable, expected evidence.
5. Save/load preserves the relevant simulation state.
6. The headless visual/text renderer includes all seven rooms and marks Sarah's current location.
7. Invalid movement or invalid room references are handled predictably.
8. The test suite can run headlessly with pytest.

## Adeptus workflow requirements

Run the Adeptus Engineerium workflow normally.

The controller must:

1. Perform MCP target-root preflight before Strategos.
2. Use the root-level intake file as the user-provided intake source.
3. Not require the user to manually set `ADEPTUS_TARGET_REPO_ROOT`.
4. Create normal run artifacts under `.adeptus/runs/facility-realism-visual-advanced-001/`.
5. Keep root packet files unchanged unless explicitly necessary.
6. Use bounded context packets for every non-strategic agent invocation.
7. Avoid broad reads after the phases where broad context is explicitly allowed.
8. Invoke Inquisitor reviews at the required gates.
9. Keep changes scoped to this intake.
10. Validate through the registered Adeptus MCP pytest tool, not only through a direct shell command.
11. Clean runtime cache/temp artifacts before final PASS.

## Context discipline requirements

After strategic planning and strategic pre-review, downstream agents must not receive:

- Full installed `SKILL.md`
- Full `workflow.yaml`
- Full project tree
- Full `.adeptus/runs` tree
- Full intake unless explicitly allowed by the workflow phase
- Full strategic plan unless explicitly allowed by the workflow phase
- Generated cache or temp directories

Every non-strategic agent invocation must be driven by a bounded packet.

If a packet is insufficient, the agent must stop and request a narrower packet update or explicit escalation. It must not self-authorize broad context.

## Validation requirements

Final validation must include:

1. `adeptus_python_compile` or equivalent syntax evidence if available.
2. `adeptus_pytest(["-q"], timeout_seconds=60)` or a similarly bounded pytest MCP invocation.
3. Evidence that the MCP pytest result includes `stdin: DEVNULL`.
4. Evidence that pytest did not time out.
5. Cleanup evidence from `adeptus_cleanup_runtime_artifacts` or the cleanup path included in `adeptus_pytest`.
6. A final check that no `.pytest_cache`, `__pycache__`, `.pyc`, `.pyo`, or temporary pytest artifacts remain outside protected `.adeptus/runs` artifacts.

## Required final state

The run may only report PASS if:

1. Strategic final review is PASS.
2. `.adeptus/runs/facility-realism-visual-advanced-001/state/current-state.json` exists.
3. `current-state.json` contains:
   - `run_status: complete`
   - `final_action: PASS`
   - `terminal_reason: final strategic approval`
   - `final_review_repair_count` as an integer
4. The final response lists:
   - Implementation summary
   - Tests run
   - MCP pytest evidence, including `stdin: DEVNULL`
   - Cleanup result
   - Files changed or created
   - Remaining risks or explicit statement that no material risks are known

## Non-goals

Do not:

- Build a web app.
- Add authentication.
- Add a database.
- Add a network service.
- Add image generation.
- Add a game engine.
- Add complex dependency management.
- Create unrelated agent, MCP, or skill changes.
- Modify the installed Adeptus skill as part of this product test.
- Turn this into a broad framework rewrite.
- Leave validation artifacts or caches behind.

## Success definition

This test succeeds if Adeptus creates a small, coherent, tested, headless facility simulation in the empty repo; validates it through the fixed MCP pytest path; cleans runtime artifacts; and produces a complete final Adeptus audit trail with PASS only after review and validation evidence.

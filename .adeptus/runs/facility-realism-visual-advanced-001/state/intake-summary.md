# Intake Summary

## Metadata
- run_id: facility-realism-visual-advanced-001
- source_intake_path: facility-realism-visual-advanced-001.intake.md
- produced_by: magos_strategos
- status: submitted

## Product Goal
- Create a small greenfield Python project named Adeptus Testus Facility.
- Model exactly seven rooms: Dormitory, Kitchen, Workshop, Infirmary, Recreation, Garden, and Control Room.
- Simulate one subject, Sarah, moving through a plausible deterministic normal-day scenario starting at 8:00 AM.
- Track time, Sarah's current room, movement history, and simple needs such as energy, hunger, morale, and health.
- Keep need changes bounded and documented so Sarah does not require sleep by 9:00 AM.
- Provide deterministic advancement through at least 12:00 PM with explicit reasons for Sarah's room changes.
- Provide a headless visual/text renderer that includes all seven rooms and marks Sarah's current location.
- Support JSON save/load round trips for relevant simulation state.
- Provide a small CLI preview command and README instructions.
- Add automated pytest coverage for the product behavior and error handling.

## Hard Constraints
- Repository is intentionally empty or near-empty; do not assume existing product code.
- Keep project conventional and small: README.md, pyproject.toml, src/adeptus_testus/, and tests/ are sufficient.
- Prefer Python standard library runtime code; pytest is acceptable for tests.
- No GUI, web app, game engine, network service, database, external API, authentication, image generation, or unrelated framework work.
- Do not modify the installed Adeptus skill or reusable MCP tooling.
- Validate final implementation through registered Adeptus MCP tools, including bounded pytest evidence with stdin: DEVNULL and no timeout.
- Clean runtime artifacts before final PASS: __pycache__, .pytest_cache, .pytest-tmp*, .adeptus_pytest_tmp*, *.pyc, and *.pyo must not remain outside protected run artifacts.
- Downstream agents must use bounded packets and must not read the full intake, full strategic plan, full installed SKILL.md, full workflow, full project tree, or full .adeptus/runs tree unless a review gate explicitly allows it.

## Acceptance Criteria
- AC01: Facility model contains exactly the seven required rooms.
- AC02: Default normal-day scenario starts Sarah at 8:00 AM.
- AC03: By 9:00 AM in the default scenario, Sarah does not require sleep.
- AC04: Normal-day simulation through at least 12:00 PM is deterministic and produces stable expected evidence.
- AC05: Actions or scheduled activities explicitly affect location, time, and needs.
- AC06: Need changes for hunger, energy, morale, and health are bounded and documented.
- AC07: Headless renderer includes all seven rooms and marks Sarah's current location.
- AC08: JSON save/load preserves relevant simulation state.
- AC09: Invalid movement or invalid room references are handled predictably.
- AC10: CLI or documented command previews/runs the simulation.
- AC11: README explains how to run tests and preview the simulation.
- AC12: Test suite runs headlessly with pytest.
- AC13: Final validation includes syntax evidence, adeptus_pytest(["-q"], timeout_seconds=60) or equivalent, stdin: DEVNULL evidence, no timeout evidence, and cleanup evidence.

## Non-Goals
- No web application, GUI, game engine, database, network service, authentication, external API, image generation, or broad dependency management.
- No unrelated agent, MCP, skill, or reusable-tool changes.
- No framework rewrite or future extensibility work beyond what the small simulation needs.
- No leaving validation caches or temporary artifacts behind.

## Downstream Read Rule
Downstream agents read this summary instead of the full intake unless strategic final review or explicit escalation requires broader context.

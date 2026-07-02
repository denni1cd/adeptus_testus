# Strategic Plan

## Metadata
- run_id: facility-realism-visual-advanced-001
- strategic_thread_id: facility-realism-visual-advanced-001/strategic
- agent: magos_strategos
- status: submitted
- source_of_truth: workflow.yaml
- strategic_contract_path: .adeptus/runs/facility-realism-visual-advanced-001/state/strategic-contract.json
- intake_summary_path: .adeptus/runs/facility-realism-visual-advanced-001/state/intake-summary.md

## Statement of Intent
Create a small, conventional Python project for Adeptus Testus Facility, a deterministic headless seven-room facility simulation where Sarah follows a plausible normal-day rhythm from 8:00 AM through at least 12:00 PM. The project must be understandable through code, tests, README instructions, JSON state, and a text-based visual renderer.

The run is intentionally scoped as a greenfield test of the Adeptus workflow. It must not modify installed Adeptus skill source or reusable MCP tools, and it must not expand into a web app, GUI, game engine, database, network service, external API, authentication system, image-generation task, or framework rewrite.

## Strategic Acceptance Criteria
| Criterion ID | Criterion | Evidence Required |
| --- | --- | --- |
| SAC01 | Product project exists with a small conventional Python structure. | README.md, pyproject.toml, src/adeptus_testus/, and tests/ are created by downstream story work. |
| SAC02 | Facility model contains exactly the seven required rooms. | Tests assert exact room set: Dormitory, Kitchen, Workshop, Infirmary, Recreation, Garden, Control Room. |
| SAC03 | Sarah's default normal-day scenario starts at 8:00 AM and remains plausible by 9:00 AM. | Tests assert 8:00 AM start and that Sarah does not require sleep by 9:00 AM. |
| SAC04 | Deterministic simulation advances through at least 12:00 PM with explicit room/activity reasons. | Tests assert stable expected evidence for a run through noon, including location/history facts. |
| SAC05 | Needs are simple, bounded, and documented. | Code or README documents bounds for hunger, energy, morale, and health changes; tests cover expected changes. |
| SAC06 | Headless rendering and JSON persistence work. | Tests assert renderer includes all rooms and Sarah marker; tests assert save/load preserves relevant state. |
| SAC07 | Invalid movement or invalid room references fail predictably. | Tests cover predictable exception or error result behavior. |
| SAC08 | README and CLI preview are sufficient for a user to run tests and preview the simulation. | README includes commands; CLI command runs/previews headlessly. |
| SAC09 | Final validation uses Adeptus MCP validation and leaves no runtime cache/temp artifacts. | Evidence includes syntax check, adeptus_pytest bounded run with stdin: DEVNULL and no timeout, plus cleanup/no-artifact check. |
| SAC10 | Context containment is preserved after strategic pre-review. | Downstream prompts use intake summary, strategic contract, and milestone/story packets instead of full intake or full strategy. |

## Architecture Design
The product should use a compact Python package under src/adeptus_testus. A conservative architecture is enough: domain objects or dataclasses for Room, Facility, Sarah/state, activities, simulation clock, and history; a deterministic normal-day schedule; renderer and JSON serialization helpers; and a CLI module or entry point.

Runtime dependencies should be Python standard library only unless a downstream agent documents a clear need. pytest is acceptable for tests. The simulation should avoid randomness and wall-clock time so all expected evidence is stable.

Need values should be bounded on a documented scale, for example 0 to 100, with named changes per scheduled activity. Sleep requirement should be derived from energy or equivalent logic and must not trigger by 9:00 AM in the default scenario.

The headless visual may be ASCII, text grid, or another string format. It must be testable and must include all seven room names plus an unambiguous Sarah marker in her current room.

Final validation and cleanup are part of the run contract, not product scope. They must use the registered Adeptus MCP validation path when available.

## Milestone Matrix
| Milestone ID | Contract Path | Planner Agent | Goal | Acceptance Criteria | Dependencies |
| --- | --- | --- | --- | --- | --- |
| m1-core-facility | .adeptus/runs/facility-realism-visual-advanced-001/state/milestone-contracts/m1-core-facility.json | lexmechanic_planner | Implement and validate the complete small headless Adeptus Testus Facility simulation. | Facility has exactly seven rooms; Sarah starts at 8:00 AM; no sleep required by 9:00 AM; deterministic noon run; bounded documented needs; renderer; JSON save/load; invalid references; README/CLI; pytest and Adeptus MCP validation evidence with cleanup. | None. |

Each milestone row creates one milestone thread owned by one Lexmechanic Planner. Story-level planning belongs in tactical story packets, not this strategic plan.

## Context Contract Outputs
- intake_summary: .adeptus/runs/facility-realism-visual-advanced-001/state/intake-summary.md
- strategic_contract: .adeptus/runs/facility-realism-visual-advanced-001/state/strategic-contract.json
- milestone_contracts:
  - .adeptus/runs/facility-realism-visual-advanced-001/state/milestone-contracts/m1-core-facility.json
- downstream_agents_must_not_read:
  - full intake
  - full strategic plan
  - full .adeptus/runs tree
  - full installed SKILL.md
  - full workflow.yaml
  - generated cache or temp directories

## Strategic Log
| Time | Decision | Evidence | Open Risk |
| --- | --- | --- | --- |
| 2026-07-02 | Use one milestone for this greenfield project. | Intake requests controlled small scope; workflow says tiny tasks prefer one milestone and one story unless concrete reason to split. | Lexmechanic must keep story packets bounded while covering all required tests. |
| 2026-07-02 | Keep runtime implementation standard-library only by default. | Intake asks to avoid mandatory third-party runtime dependencies unless clearly justified. | None known. |
| 2026-07-02 | Use a headless text renderer rather than GUI or image output. | Intake explicitly permits ASCII/text-grid/SVG/HTML strings and forbids GUI/game engine/image generation. | Renderer must still be visually clear and testable. |
| 2026-07-02 | Tool Needs set to none. | Existing workflow declares adeptus_python_compile, adeptus_pytest, and adeptus_cleanup_runtime_artifacts for required validation and cleanup. | Downstream must actually invoke the registered MCP pytest path before final PASS. |

## Tool Needs
not_applicable

No new reusable MCP capability is required for strategic planning. The declared Adeptus validation tools are sufficient for the downstream validation and cleanup requirements.

## Inquisitor Handoff
- review_gate: strategic_pre_review
- next_required_agent: inquisitor_gatekeeper
- submitted_artifacts:
  - .adeptus/runs/facility-realism-visual-advanced-001/strategic/strategic-plan.md
  - .adeptus/runs/facility-realism-visual-advanced-001/state/intake-summary.md
  - .adeptus/runs/facility-realism-visual-advanced-001/state/strategic-contract.json
  - .adeptus/runs/facility-realism-visual-advanced-001/state/milestone-contracts/m1-core-facility.json
- known_limits:
  - This strategic phase did not implement product code or create story packets.
  - Strategic pre-review may read the full intake, strategic plan, intake summary, strategic contract, and milestone contract per workflow.
  - Milestone planning must begin only after Inquisitor returns PASS for strategic_pre_review.

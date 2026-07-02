# Tactical Plan: m1-core-facility

## Milestone Contract
- Run ID: facility-realism-visual-advanced-001
- Milestone ID: m1-core-facility
- Product: Adeptus Testus Facility
- Goal: deliver a small, deterministic Python simulation with tests, docs, CLI preview, JSON persistence, and headless rendering.

## Scope Summary
Implement a conventional greenfield Python package using only the milestone-approved project shape:
- `README.md`
- `pyproject.toml`
- `src/adeptus_testus/`
- `tests/`

The implementation must model exactly these rooms: Dormitory, Kitchen, Workshop, Infirmary, Recreation, Garden, and Control Room. It must simulate Sarah's deterministic normal-day scenario from 8:00 AM through at least 12:00 PM, track current room, time, needs, and movement/activity history, render all rooms headlessly with Sarah's location marked, support JSON save/load, and expose a small CLI preview.

## Story Packet Index
| Story ID | Packet Path | Primary Contract |
| --- | --- | --- |
| s1-core-facility-simulation | `.adeptus/runs/facility-realism-visual-advanced-001/packets/m1-core-facility/s1-core-facility-simulation/story-packet.md` | Build and verify the complete deterministic headless facility simulation for milestone m1-core-facility. |

## Story Dependency Graph
- s1-core-facility-simulation has no story dependencies.

## Acceptance Coverage
- Facility rooms and predictable invalid references are covered by s1 criterion 1.
- Default 8:00 AM start, no sleep required by 9:00 AM, deterministic advancement through at least 12:00 PM, explicit action reasons, and bounded documented needs are covered by s1 criterion 2.
- Headless rendering, JSON round trip, CLI/README instructions, pytest coverage, syntax/pytest evidence, and cleanup evidence are covered by s1 criterion 3.

## Test Policy
The story must add or modify only tests that directly verify its acceptance criteria. Prefer project-level pytest coverage for observable behavior over implementation-detail tests. Tests must run headlessly with a bounded pytest command and no interactive input.

## Context Boundary
Downstream implementation may inspect only the story packet, this tactical plan, the milestone contract, the intake summary, and focused target files it creates or edits in `README.md`, `pyproject.toml`, `src/adeptus_testus/`, and `tests/`. It must not read the full intake, full strategic plan, full workflow, full installed skill, sibling or unrelated story artifacts, or the full `.adeptus/runs` tree unless a review gate explicitly authorizes escalation.

## Non-Goals
- No web app, GUI, game engine, network service, database, external API, authentication, image generation, or unrelated framework work.
- No installed Adeptus skill, workflow, MCP, or global agent definition changes.
- No future-feature scaffolding, unrelated refactors, broad dependency management, or cross-story cleanup stories.

## Validation And Handoff
After implementation, validation evidence must include syntax evidence using `adeptus_python_compile` or equivalent MCP syntax validation if available, bounded pytest evidence equivalent to `adeptus_pytest(["-q"], timeout_seconds=60)`, explicit stdin `DEVNULL` and no-timeout evidence, and cleanup evidence showing no `__pycache__`, `.pytest_cache`, `.pytest-tmp*`, `.adeptus_pytest_tmp*`, `*.pyc`, or `*.pyo` remain outside protected Adeptus run artifacts.

Submit this tactical plan and the story packet index to `inquisitor_gatekeeper` for `tactical_pre_review`. Story implementation must not begin until the gate returns `PASS`.

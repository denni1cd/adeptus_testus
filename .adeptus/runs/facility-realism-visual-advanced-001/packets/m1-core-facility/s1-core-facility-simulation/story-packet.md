# Story Packet: s1-core-facility-simulation

## Single Behavioral Contract
Build the complete small Python package for Adeptus Testus Facility so a user can run tests and preview a deterministic headless simulation of Sarah moving through the seven-room facility from 8:00 AM through at least 12:00 PM, with bounded needs, explicit history, JSON persistence, and predictable invalid-room handling.

## Inputs And Outputs
Inputs:
- `.adeptus/runs/facility-realism-visual-advanced-001/state/milestone-contracts/m1-core-facility.json`
- `.adeptus/runs/facility-realism-visual-advanced-001/state/intake-summary.md`
- `.adeptus/runs/facility-realism-visual-advanced-001/milestones/m1-core-facility/tactical-plan.md`
- This story packet

Allowed product outputs:
- `README.md`
- `pyproject.toml`
- `src/adeptus_testus/`
- `tests/`

Expected behavior outputs:
- A deterministic facility model with exactly Dormitory, Kitchen, Workshop, Infirmary, Recreation, Garden, and Control Room.
- A default Sarah normal-day scenario starting at 8:00 AM and advancing deterministically through at least 12:00 PM.
- Headless renderer output that includes all seven rooms and marks Sarah's current room.
- JSON save/load round trip for current time, current room, needs, and relevant history.
- CLI or documented command that previews/runs the simulation.
- Pytest coverage and validation evidence required by the milestone.

## Acceptance Criteria
1. Facility state contains exactly the seven required rooms, rejects invalid room references or movements predictably, and tracks Sarah's current room, time, needs, and movement/activity history.
2. The default scenario starts at 8:00 AM, advances deterministically through at least 12:00 PM, records explicit movement/activity reasons, documents bounded hunger, energy, morale, and health changes in code or README, and shows Sarah does not require sleep by 9:00 AM.
3. Headless rendering, JSON save/load, CLI preview instructions, README test/preview instructions, and headless pytest coverage all work and directly verify the milestone behaviors, including syntax, bounded pytest, stdin `DEVNULL`, no-timeout, and cleanup evidence requirements.

## Non-Goals
- Do not build a web app, GUI, game engine, network service, database, external API, authentication, image generation, or unrelated framework.
- Do not modify installed Adeptus skill source, workflow, MCP tools, global agent definitions, or any reusable tool registry.
- Do not implement future-state features beyond the normal-day deterministic facility simulation.
- Do not perform sibling-story work, broad regression expansion, unrelated refactors, or cross-story consolidation.
- Do not leave `__pycache__`, `.pytest_cache`, `.pytest-tmp*`, `.adeptus_pytest_tmp*`, `*.pyc`, or `*.pyo` artifacts outside protected Adeptus run artifacts.

## Dependency Contracts
No prior story or milestone dependencies. This story is self-contained and may rely only on the milestone contract, intake summary, tactical plan, this packet, and focused target files created or edited for this story.

## Change Boundary
The worker may create or edit only `README.md`, `pyproject.toml`, files under `src/adeptus_testus/`, and files under `tests/`, plus story-local validation evidence if required by the workflow. The worker must not read or modify the full intake, full strategic plan, full workflow, full installed skill, sibling or unrelated story artifacts, protected Adeptus run state, or broad repository history unless the review gate explicitly requests packet repair or escalation.

## Test Policy
Add focused pytest tests that directly map to the three acceptance criteria. Tests must cover required rooms, 8:00 AM start, 9:00 AM no-sleep behavior, deterministic run through at least 12:00 PM, explicit history/reasons, bounded needs, renderer output, save/load round trip, invalid references, and CLI/README behavior as directly as practical. Do not add unrelated regression tests or broad framework tests.

## Stop Condition
Stop when implementation and direct validation pass with required syntax, bounded headless pytest, stdin `DEVNULL`, no-timeout, and cleanup evidence; or when a concrete blocker is found; or when the packet is insufficient and must be repaired by Lexmechanic before implementation can continue.

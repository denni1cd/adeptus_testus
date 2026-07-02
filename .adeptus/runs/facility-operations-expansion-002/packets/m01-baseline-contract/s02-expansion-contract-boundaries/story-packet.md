# Story Packet: s02-expansion-contract-boundaries

Run ID: `facility-operations-expansion-002`
Milestone: `m01-baseline-contract`
Story workspace: `.adeptus/runs/facility-operations-expansion-002/milestones/m01-baseline-contract/stories/s02-expansion-contract-boundaries/`

## Primary Behavioral Contract

Define bounded implementation and review contracts for later expansion areas while preserving the baseline compatibility contract. This story documents boundaries only; it does not implement future product behavior.

## Inputs

- This story packet.
- `s01-baseline-characterization` story summary, if available.
- `.adeptus/runs/facility-operations-expansion-002/state/intake-summary.md`
- Focused target files may be read only if needed to name precise future boundaries:
  - `src/adeptus_testus/facility.py`
  - `src/adeptus_testus/cli.py`
  - `tests/test_facility.py`
  - `README.md`
  - `pyproject.toml`

## Expected Outputs

- A concise design-boundary note in the story workspace naming future contracts for graph/pathing, named scenarios, scenario serialization/validation, scheduled incidents, deterministic reports, CLI expansion, and README updates.
- Explicit preservation notes showing that default scenario and existing `--until` CLI behavior remain compatibility constraints for future stories.

## Acceptance Criteria

1. Future work boundaries are documented for graph/pathing, scenarios, incidents, reports, CLI, and README without assigning implementation to this story.
2. The document states that default scenario behavior, seven baseline rooms, save/load compatibility, render compatibility, invalid-room predictability, and existing `--until` CLI compatibility are non-negotiable preservation constraints.
3. No product behavior or project tests are changed by this story unless packet repair is explicitly required.

## Non-Goals

- Do not implement future graph, scenario, incident, report, CLI, or README product changes.
- Do not create reconciliation, cleanup, audit, or cross-story consolidation work as worker stories.
- Do not alter tests except if packet repair is required by reviewer instruction.
- Do not read broad project history, full intake, full strategic plan, sibling milestones, old run artifacts, or the full `.adeptus/runs` tree.

## Dependency Contracts

Depends on `s01-baseline-characterization` for the finalized baseline preservation evidence when available. If `s01` has not completed, use the baseline contract in this packet and stop before making claims about new characterization results.

## Change Boundary

May create documentation only under `.adeptus/runs/facility-operations-expansion-002/milestones/m01-baseline-contract/stories/s02-expansion-contract-boundaries/`. Product files should remain unchanged.

## Test Policy

No product tests are required because this is a planning-boundary story. If a reviewer requires validation, run a cheap repository smoke command such as `python -m pytest -q` without changing tests.

## Stop Condition

Stop when the design-boundary note is complete, or when dependency evidence from `s01` is missing and needed, or when packet repair is required.

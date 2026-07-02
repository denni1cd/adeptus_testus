# Design Boundary Note: s02 Expansion Contract Boundaries

## Purpose

This story defines implementation and review boundaries for later facility-operations expansion work. It documents future contracts only and does not assign implementation work to this story.

## Non-Negotiable Preservation Constraints

Future stories must preserve these baseline compatibility constraints unless a later approved contract explicitly supersedes them:

- Default scenario behavior remains compatible with the current baseline.
- The seven baseline rooms remain present and recognizable.
- Save/load compatibility remains intact for existing persisted state.
- Render compatibility remains intact, including stable room visibility and current-room indication.
- Invalid-room handling remains predictable.
- Existing CLI `--until` compatibility remains intact, including the current module invocation behavior characterized for `python -m adeptus_testus --until 09:00` and `python -m adeptus_testus --until 12:00`.

## Future Contract Boundaries

Graph/pathing:
- Future graph or pathing work may define room connectivity, traversal costs, reachability, and path selection rules.
- It must not remove or rename the seven baseline rooms as part of graph introduction.
- It must preserve predictable invalid-room behavior when rooms or graph edges are invalid.

Named scenarios:
- Future named-scenario work may introduce explicit scenario identifiers and scenario selection behavior.
- The existing default scenario remains the compatibility baseline and must continue to work without requiring a new scenario name.
- Scenario selection must not alter default behavior unless explicitly requested through the future contract.

Scenario serialization and validation:
- Future serialization work may define scenario schema, validation errors, versioning, and load/save behavior for scenario definitions.
- Existing save/load state compatibility remains a preservation constraint.
- Validation failures must be deterministic and explainable without changing invalid-room predictability.

Scheduled incidents:
- Future incident work may define scheduled events, triggers, recurrence, and effects on facility state.
- Incident scheduling must preserve deterministic baseline behavior when no incidents are configured.
- Incidents must not silently change default scenario behavior.

Deterministic reports:
- Future reporting work may define report format, report scope, ordering, and deterministic output requirements.
- Reports must be stable for identical inputs and must not depend on ambient runtime state unless explicitly contracted.
- Report additions must not break existing render compatibility.

CLI expansion:
- Future CLI work may add scenario selection, graph/pathing controls, incident inputs, report options, and validation commands.
- Existing `--until` behavior remains compatible and must continue to accept the currently characterized invocations.
- New CLI options must not make default execution require additional arguments.

README updates:
- Future README work may document new graph/pathing, named scenarios, serialization, incidents, reports, and CLI behavior after those features exist.
- README changes should describe implemented behavior only.
- README changes must not imply that future expansion behavior was implemented by this boundary story.

## Out Of Scope For This Story

This story does not implement product behavior, modify tests, change the README, alter packaging, or introduce future feature code. It only records boundary documentation for later stories.

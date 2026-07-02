# Story Review Decision: s02-named-scenarios

## Decision

PASS

## Gate

- Run ID: facility-operations-expansion-002
- Mode: story_review
- Milestone ID: m02-graph-scenarios
- Story ID: s02-named-scenarios
- Submitted item: `.adeptus/runs/facility-operations-expansion-002/milestones/m02-graph-scenarios/stories/s02-named-scenarios/work-item.md`
- Review packet: `.adeptus/runs/facility-operations-expansion-002/packets/m02-graph-scenarios/s02-named-scenarios/review-packet.md`

## Scope Reviewed

- `.adeptus/runs/facility-operations-expansion-002/packets/m02-graph-scenarios/s02-named-scenarios/review-packet.md`
- `.adeptus/runs/facility-operations-expansion-002/milestones/m02-graph-scenarios/stories/s02-named-scenarios/work-item.md`
- `.adeptus/runs/facility-operations-expansion-002/milestones/m02-graph-scenarios/stories/s01-facility-graph-pathing/reviews/story-review-decision.md`
- `src/adeptus_testus/facility.py`
- `tests/test_facility.py`
- Focused validation evidence named in the packet

No broad run state, unrelated milestone/story artifacts, full project tree, full `.adeptus/runs` tree, unrelated prior reviews, or installed full `SKILL.md` was read.

## Acceptance Criteria Review

- PASS: The named `default` scenario preserves baseline construction. Sarah starts at 08:00 in Dormitory with the baseline needs, `default_facility()` delegates to named scenario construction, and `facility_for_scenario("default")` advances through noon with the same timeline and final needs as the preserved default path.
- PASS: The `maintenance_day` scenario exists and is deterministic through 12:00. Repeated construction through `facility_for_scenario("maintenance_day")` and compatibility construction through `default_facility("maintenance_day")` produce the same history, 12:00 Control Room final location, and final needs.
- PASS: Unknown scenario names fail predictably. `facility_for_scenario()` raises `UnknownScenarioError` for an invalid scenario name instead of silently falling back.
- PASS: Scenario room references remain constrained to the seven-room facility graph. `FacilityState.__post_init__()` validates scenario activity destinations, and movement still calls route validation before state mutation.

## Baseline And Dependency Preservation

PASS. The prior graph dependency review for `s01-facility-graph-pathing` passed. The reviewed changes preserve the required seven-room graph, deterministic pathing helpers, route-duration behavior, and pre-mutation route validation used by scenario movement.

PASS. Existing baseline tests remain present and passing, including the 08:00 Dormitory start, no sleep required by 09:00, deterministic normal-day advancement through 12:00, save/load behavior, renderer output, and CLI `--until` behavior.

## Validation Evidence

- PASS: Packet evidence reports `python -m pytest tests/test_facility.py -q` completed with `13 passed in 0.16s`.
- PASS: Packet evidence reports `adeptus_python_compile(paths=["src/adeptus_testus/facility.py", "tests/test_facility.py"])` completed with return code 0 and no errors.
- PASS: Packet evidence reports `adeptus_pytest(args=["tests/test_facility.py", "-q"], timeout_seconds=60)` completed with return code 0, timed_out false, empty stderr, and `13 passed in 0.13s`.
- PASS: Inquisitor focused rerun of `python -m pytest tests/test_facility.py -q` completed with `13 passed in 0.17s`.
- PASS: Inquisitor focused compile check `python -m compileall -q src/adeptus_testus/facility.py tests/test_facility.py` completed with return code 0.

## Runtime Cleanup

PASS. Packet evidence reports runtime cleanup completed with no remaining generated pytest or bytecode artifacts. Inquisitor-created `.pytest_cache` and `__pycache__` artifacts from the focused rerun were removed, and a final scoped check found none of `.pytest_cache`, `src/adeptus_testus/__pycache__`, or `tests/__pycache__` present.

## Findings

No blocking findings.

## Rework Required

None.

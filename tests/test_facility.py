import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from adeptus_testus.cli import main
from adeptus_testus.facility import (
    FACILITY_GRAPH,
    FacilityState,
    InvalidScenarioJsonError,
    REQUIRED_ROOMS,
    RouteNotFoundError,
    UnknownRoomError,
    UnknownScenarioError,
    default_facility,
    facility_for_scenario,
    facility_from_scenario_json,
    route_between,
    scenario_to_json,
    travel_duration_minutes,
)


def test_facility_has_exactly_required_rooms_and_rejects_invalid_rooms():
    state = default_facility()
    assert state.rooms == REQUIRED_ROOMS
    assert len(state.rooms) == 7
    assert tuple(FACILITY_GRAPH) == REQUIRED_ROOMS
    assert set(FACILITY_GRAPH) == set(REQUIRED_ROOMS)

    with pytest.raises(UnknownRoomError):
        state.move_to("Hangar", "Bad move", "Invalid test move")

    with pytest.raises(UnknownRoomError):
        FacilityState(current_time="08:00", current_room="Hangar", needs=state.needs)


def test_facility_graph_routes_every_required_room_deterministically():
    for origin in REQUIRED_ROOMS:
        for destination in REQUIRED_ROOMS:
            first_route = route_between(origin, destination)
            second_route = route_between(origin, destination)

            assert first_route == second_route
            assert first_route[0] == origin
            assert first_route[-1] == destination
            assert all(room in REQUIRED_ROOMS for room in first_route)


def test_travel_duration_is_deterministic_and_zero_for_current_room():
    state = default_facility()

    assert state.route_to("Dormitory") == ("Dormitory",)
    assert state.travel_duration_to("Dormitory") == 0
    assert travel_duration_minutes("Dormitory", "Dormitory") == 0

    assert route_between("Dormitory", "Control Room") == ("Dormitory", "Kitchen", "Workshop", "Control Room")
    assert travel_duration_minutes("Dormitory", "Control Room") == 19
    assert state.travel_duration_minutes("Dormitory", "Control Room") == 19
    assert travel_duration_minutes("Dormitory", "Control Room") == travel_duration_minutes("Dormitory", "Control Room")


def test_invalid_route_failures_do_not_corrupt_state(monkeypatch):
    state = default_facility()
    original_room = state.current_room
    original_needs = state.needs
    original_history = list(state.history)

    with pytest.raises(UnknownRoomError):
        route_between("Dormitory", "Hangar")

    with pytest.raises(RouteNotFoundError):
        monkeypatch.setitem(FACILITY_GRAPH, "Dormitory", ())
        state.move_to("Kitchen", "Blocked move", "No graph edge")

    assert state.current_room == original_room
    assert state.needs == original_needs
    assert state.history == original_history


def test_default_day_starts_at_0800_and_sarah_does_not_require_sleep_by_0900():
    state = default_facility()
    assert state.current_time == "08:00"
    assert state.current_room == "Dormitory"

    state.advance_until("09:00")
    assert state.current_time == "09:00"
    assert state.current_room == "Workshop"
    assert not state.needs.requires_sleep()
    assert state.needs.energy == 79


def test_normal_day_through_noon_is_deterministic_and_bounded():
    state = default_facility()
    history = state.advance_until("12:00")

    assert [(entry.time, entry.destination, entry.activity) for entry in history] == [
        ("08:30", "Kitchen", "Breakfast"),
        ("09:00", "Workshop", "Tool check"),
        ("10:00", "Infirmary", "Health check"),
        ("10:45", "Recreation", "Short break"),
        ("11:20", "Garden", "Garden walk"),
        ("12:00", "Control Room", "Systems review"),
    ]
    assert all(entry.reason for entry in history)
    assert state.current_room == "Control Room"
    assert state.needs.hunger == 74
    assert state.needs.energy == 71
    assert state.needs.morale == 87
    assert state.needs.health == 94
    assert all(0 <= value <= 100 for value in state.needs.__dict__.values())


def test_named_default_scenario_preserves_baseline_behavior():
    baseline = default_facility()
    named = facility_for_scenario("default")

    assert named.current_time == baseline.current_time == "08:00"
    assert named.current_room == baseline.current_room == "Dormitory"
    assert named.needs == baseline.needs
    assert [
        (entry.time, entry.destination, entry.activity, entry.needs)
        for entry in named.advance_until("12:00")
    ] == [
        (entry.time, entry.destination, entry.activity, entry.needs)
        for entry in baseline.advance_until("12:00")
    ]
    assert named.needs == baseline.needs


def test_maintenance_day_scenario_is_deterministic_through_noon():
    first = facility_for_scenario("maintenance_day")
    second = default_facility("maintenance_day")

    first_history = first.advance_until("12:00")
    second_history = second.advance_until("12:00")

    assert [(entry.time, entry.origin, entry.destination, entry.activity, entry.needs) for entry in first_history] == [
        (entry.time, entry.origin, entry.destination, entry.activity, entry.needs) for entry in second_history
    ]
    assert first.current_time == second.current_time == "12:00"
    assert first.current_room == second.current_room == "Control Room"
    assert first.needs == second.needs
    assert first.route_to("Workshop") == ("Control Room", "Workshop")


def test_maintenance_day_incidents_expose_required_fields():
    state = facility_for_scenario("maintenance_day")

    assert [
        (incident.time, incident.room, incident.name, incident.severity)
        for incident in state.incidents
    ] == [
        ("08:45", "Control Room", "Telemetry drift", "medium"),
        ("11:00", "Garden", "Irrigation pressure drop", "high"),
    ]
    assert all(incident.effect for incident in state.incidents)
    assert all(incident.handling_note for incident in state.incidents)


def test_maintenance_day_incidents_are_encountered_deterministically_by_time_and_room():
    state = facility_for_scenario("maintenance_day")

    assert state.encountered_incidents() == ()
    assert state.incidents_until("08:44") == ()

    state.advance_until("08:45")
    assert [incident.name for incident in state.encountered_incidents()] == ["Telemetry drift"]
    assert [incident.name for incident in state.incidents_until("08:45")] == ["Telemetry drift"]

    state.advance_until("11:00")
    assert [incident.name for incident in state.encountered_incidents()] == ["Irrigation pressure drop"]
    assert [incident.name for incident in state.incidents_until("11:00")] == [
        "Telemetry drift",
        "Irrigation pressure drop",
    ]


def test_unknown_scenario_name_fails_predictably():
    with pytest.raises(UnknownScenarioError, match="unknown scenario 'storm_day'"):
        facility_for_scenario("storm_day")


def test_scenario_json_round_trip_preserves_named_scenario_behavior():
    raw = scenario_to_json("maintenance_day")
    loaded = facility_from_scenario_json(raw)
    expected = facility_for_scenario("maintenance_day")

    assert loaded.scenario_name == "maintenance_day"
    assert loaded.current_time == expected.current_time
    assert loaded.current_room == expected.current_room
    assert loaded.needs == expected.needs
    assert loaded.scenario == expected.scenario
    assert [(entry.time, entry.destination, entry.activity, entry.needs) for entry in loaded.advance_until("12:00")] == [
        (entry.time, entry.destination, entry.activity, entry.needs)
        for entry in expected.advance_until("12:00")
    ]


def test_scenario_json_invalid_shape_and_unknown_name_fail_predictably():
    with pytest.raises(InvalidScenarioJsonError, match="scenario JSON must be a JSON object"):
        facility_from_scenario_json("[]")

    with pytest.raises(InvalidScenarioJsonError, match="missing required field 'activities'"):
        facility_from_scenario_json('{"name": "default", "current_time": "08:00", "current_room": "Dormitory", "needs": {}}')

    with pytest.raises(UnknownScenarioError, match="unknown scenario 'storm_day'"):
        facility_from_scenario_json(
            '{"name": "storm_day", "current_time": "08:00", "current_room": "Dormitory", '
            '"needs": {"hunger": 1, "energy": 1, "morale": 1, "health": 1}, "activities": []}'
        )


def test_scenario_json_invalid_room_reference_fails_predictably():
    raw = scenario_to_json("default")
    payload = json.loads(raw)
    payload["activities"][0]["destination"] = "Hangar"

    with pytest.raises(UnknownRoomError, match="unknown room 'Hangar'"):
        facility_from_scenario_json(json.dumps(payload))


def test_save_load_preserves_relevant_state():
    state = default_facility()
    state.advance_until("12:00")

    loaded = FacilityState.load_json(state.save_json())

    assert loaded.current_time == state.current_time
    assert loaded.current_room == state.current_room
    assert loaded.needs == state.needs
    assert loaded.rooms == REQUIRED_ROOMS
    assert loaded.scenario_name == state.scenario_name
    assert loaded.scenario == state.scenario
    assert loaded.history == state.history


def test_expanded_save_load_preserves_named_scenario_and_continuation():
    state = facility_for_scenario("maintenance_day")
    state.advance_until("10:15")

    loaded = FacilityState.load_json(state.save_json())
    expected = facility_for_scenario("maintenance_day")
    expected.advance_until("10:15")

    assert loaded.scenario_name == "maintenance_day"
    assert loaded.current_time == expected.current_time
    assert loaded.current_room == expected.current_room
    assert loaded.needs == expected.needs
    assert loaded.history == expected.history
    assert loaded.incidents == expected.incidents
    assert [(entry.time, entry.destination, entry.activity) for entry in loaded.advance_until("12:00")] == [
        (entry.time, entry.destination, entry.activity)
        for entry in expected.advance_until("12:00")
    ]
    assert loaded.needs == expected.needs


def test_load_json_remains_compatible_with_baseline_payload_shape():
    baseline_payload = {
        "current_time": "09:00",
        "current_room": "Workshop",
        "needs": {"hunger": 82, "energy": 79, "morale": 75, "health": 88},
        "rooms": list(REQUIRED_ROOMS),
        "history": [],
    }

    loaded = FacilityState.load_json(json.dumps(baseline_payload))

    assert loaded.scenario_name == "default"
    assert loaded.scenario == facility_for_scenario("default").scenario
    assert loaded.current_time == "09:00"
    assert loaded.current_room == "Workshop"


def test_renderer_and_cli_are_headless_and_include_sarah(capsys):
    state = default_facility()
    state.advance_until("10:00")
    rendered = state.render()

    for room in REQUIRED_ROOMS:
        assert room in rendered
    assert "- Infirmary [Sarah]" in rendered
    assert rendered.count("[Sarah]") == 1

    assert main(["--until", "09:00"]) == 0
    output = capsys.readouterr().out
    assert "Adeptus Testus Facility" in output
    assert "09:00 - Tool check" in output
    assert "- Workshop [Sarah]" in output


@pytest.mark.parametrize(
    ("until", "expected_event", "expected_room"),
    [
        ("09:00", "09:00 - Tool check", "- Workshop [Sarah]"),
        ("12:00", "12:00 - Systems review", "- Control Room [Sarah]"),
    ],
)
def test_python_module_cli_until_0900_and_1200_preserves_output(until, expected_event, expected_room):
    pythonpath = str(Path(__file__).resolve().parents[1] / "src")
    result = subprocess.run(
        [sys.executable, "-m", "adeptus_testus", "--until", until],
        check=False,
        capture_output=True,
        env={**os.environ, "PYTHONPATH": pythonpath},
        text=True,
    )

    assert result.returncode == 0
    assert "Adeptus Testus Facility" in result.stdout
    assert expected_event in result.stdout
    assert expected_room in result.stdout
    assert result.stderr == ""

import pytest

from adeptus_testus.cli import main
from adeptus_testus.facility import FacilityState, REQUIRED_ROOMS, UnknownRoomError, default_facility


def test_facility_has_exactly_required_rooms_and_rejects_invalid_rooms():
    state = default_facility()
    assert state.rooms == REQUIRED_ROOMS
    assert len(state.rooms) == 7

    with pytest.raises(UnknownRoomError):
        state.move_to("Hangar", "Bad move", "Invalid test move")

    with pytest.raises(UnknownRoomError):
        FacilityState(current_time="08:00", current_room="Hangar", needs=state.needs)


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


def test_save_load_preserves_relevant_state():
    state = default_facility()
    state.advance_until("12:00")

    loaded = FacilityState.load_json(state.save_json())

    assert loaded.current_time == state.current_time
    assert loaded.current_room == state.current_room
    assert loaded.needs == state.needs
    assert loaded.rooms == REQUIRED_ROOMS
    assert loaded.history == state.history


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

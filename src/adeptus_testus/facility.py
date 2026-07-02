"""Deterministic model for the seven-room Adeptus Testus Facility.

Need values are bounded from 0 to 100, where higher is better. The normal-day
scenario applies small fixed deltas so Sarah's first morning hour is plausible:
energy starts at 82 and remains above the sleep threshold of 25 by 09:00.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json
from typing import Iterable, Sequence

REQUIRED_ROOMS: tuple[str, ...] = (
    "Dormitory",
    "Kitchen",
    "Workshop",
    "Infirmary",
    "Recreation",
    "Garden",
    "Control Room",
)

SLEEP_ENERGY_THRESHOLD = 25


class UnknownRoomError(ValueError):
    """Raised when a simulation references a room outside the facility."""

    def __init__(self, room: str) -> None:
        valid = ", ".join(REQUIRED_ROOMS)
        super().__init__(f"unknown room {room!r}; valid rooms: {valid}")
        self.room = room


@dataclass(frozen=True)
class Needs:
    hunger: int
    energy: int
    morale: int
    health: int

    def adjusted(self, deltas: dict[str, int]) -> "Needs":
        values = asdict(self)
        for key, delta in deltas.items():
            if key not in values:
                raise KeyError(f"unknown need {key!r}")
            values[key] = _clamp(values[key] + delta)
        return Needs(**values)

    def requires_sleep(self) -> bool:
        return self.energy < SLEEP_ENERGY_THRESHOLD


@dataclass(frozen=True)
class Activity:
    time: str
    destination: str
    activity: str
    reason: str
    need_deltas: dict[str, int]


@dataclass(frozen=True)
class HistoryEntry:
    time: str
    origin: str
    destination: str
    activity: str
    reason: str
    needs: Needs


DEFAULT_SCENARIO: tuple[Activity, ...] = (
    Activity("08:30", "Kitchen", "Breakfast", "Sarah eats before work.", {"hunger": 18, "morale": 2}),
    Activity("09:00", "Workshop", "Tool check", "Morning maintenance begins.", {"hunger": -4, "energy": -3, "morale": 3}),
    Activity("10:00", "Infirmary", "Health check", "Routine wellness check keeps the day stable.", {"health": 4, "morale": 1}),
    Activity("10:45", "Recreation", "Short break", "A brief pause restores morale.", {"energy": -2, "morale": 6}),
    Activity("11:20", "Garden", "Garden walk", "Light movement and daylight improve outlook.", {"hunger": -3, "energy": -2, "morale": 4, "health": 2}),
    Activity("12:00", "Control Room", "Systems review", "Noon facility review closes the morning loop.", {"hunger": -5, "energy": -4, "morale": 1}),
)


@dataclass
class FacilityState:
    current_time: str
    current_room: str
    needs: Needs
    rooms: tuple[str, ...] = REQUIRED_ROOMS
    scenario: tuple[Activity, ...] = DEFAULT_SCENARIO
    history: list[HistoryEntry] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.rooms != REQUIRED_ROOMS:
            raise ValueError("Adeptus Testus Facility must contain exactly the seven required rooms")
        self._require_room(self.current_room)
        for activity in self.scenario:
            self._require_room(activity.destination)

    def move_to(self, destination: str, activity: str, reason: str, need_deltas: dict[str, int] | None = None) -> HistoryEntry:
        self._require_room(destination)
        origin = self.current_room
        self.current_room = destination
        self.needs = self.needs.adjusted(need_deltas or {})
        entry = HistoryEntry(
            time=self.current_time,
            origin=origin,
            destination=destination,
            activity=activity,
            reason=reason,
            needs=self.needs,
        )
        self.history.append(entry)
        return entry

    def advance_next(self) -> HistoryEntry:
        for activity in self.scenario:
            if _minutes(activity.time) > _minutes(self.current_time):
                self.current_time = activity.time
                return self.move_to(
                    activity.destination,
                    activity.activity,
                    activity.reason,
                    activity.need_deltas,
                )
        raise StopIteration("normal-day scenario is complete")

    def advance_until(self, target_time: str) -> list[HistoryEntry]:
        target = _minutes(target_time)
        entries: list[HistoryEntry] = []
        while True:
            pending = [activity for activity in self.scenario if _minutes(self.current_time) < _minutes(activity.time) <= target]
            if not pending:
                return entries
            entries.append(self.advance_next())

    def render(self) -> str:
        lines = ["Adeptus Testus Facility", f"Time: {self.current_time}", "Rooms:"]
        for room in self.rooms:
            marker = " [Sarah]" if room == self.current_room else ""
            lines.append(f"- {room}{marker}")
        lines.append(
            "Needs: "
            f"hunger={self.needs.hunger}, energy={self.needs.energy}, "
            f"morale={self.needs.morale}, health={self.needs.health}"
        )
        return "\n".join(lines)

    def save_json(self) -> str:
        payload = {
            "current_time": self.current_time,
            "current_room": self.current_room,
            "needs": asdict(self.needs),
            "rooms": list(self.rooms),
            "history": [
                {
                    "time": entry.time,
                    "origin": entry.origin,
                    "destination": entry.destination,
                    "activity": entry.activity,
                    "reason": entry.reason,
                    "needs": asdict(entry.needs),
                }
                for entry in self.history
            ],
        }
        return json.dumps(payload, sort_keys=True)

    @classmethod
    def load_json(cls, raw: str) -> "FacilityState":
        payload = json.loads(raw)
        state = cls(
            current_time=payload["current_time"],
            current_room=payload["current_room"],
            needs=Needs(**payload["needs"]),
            rooms=tuple(payload["rooms"]),
        )
        state.history = [
            HistoryEntry(
                time=item["time"],
                origin=item["origin"],
                destination=item["destination"],
                activity=item["activity"],
                reason=item["reason"],
                needs=Needs(**item["needs"]),
            )
            for item in payload["history"]
        ]
        return state

    def _require_room(self, room: str) -> None:
        if room not in self.rooms:
            raise UnknownRoomError(room)


def default_facility() -> FacilityState:
    return FacilityState(
        current_time="08:00",
        current_room="Dormitory",
        needs=Needs(hunger=68, energy=82, morale=70, health=88),
    )


def _clamp(value: int) -> int:
    return max(0, min(100, value))


def _minutes(time_text: str) -> int:
    hour, minute = time_text.split(":", 1)
    return int(hour) * 60 + int(minute)

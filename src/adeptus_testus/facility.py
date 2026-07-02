"""Deterministic model for the seven-room Adeptus Testus Facility.

Need values are bounded from 0 to 100, where higher is better. The normal-day
scenario applies small fixed deltas so Sarah's first morning hour is plausible:
energy starts at 82 and remains above the sleep threshold of 25 by 09:00.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass, field
import json
from typing import Any

REQUIRED_ROOMS: tuple[str, ...] = (
    "Dormitory",
    "Kitchen",
    "Workshop",
    "Infirmary",
    "Recreation",
    "Garden",
    "Control Room",
)

FACILITY_GRAPH: dict[str, tuple[str, ...]] = {
    "Dormitory": ("Kitchen", "Recreation"),
    "Kitchen": ("Dormitory", "Workshop"),
    "Workshop": ("Kitchen", "Infirmary", "Control Room"),
    "Infirmary": ("Workshop", "Garden"),
    "Recreation": ("Dormitory", "Garden"),
    "Garden": ("Recreation", "Infirmary", "Control Room"),
    "Control Room": ("Workshop", "Garden"),
}

FACILITY_EDGE_TRAVEL_MINUTES: dict[frozenset[str], int] = {
    frozenset(("Dormitory", "Kitchen")): 5,
    frozenset(("Dormitory", "Recreation")): 7,
    frozenset(("Kitchen", "Workshop")): 6,
    frozenset(("Workshop", "Infirmary")): 4,
    frozenset(("Workshop", "Control Room")): 8,
    frozenset(("Infirmary", "Garden")): 5,
    frozenset(("Recreation", "Garden")): 6,
    frozenset(("Garden", "Control Room")): 7,
}

SLEEP_ENERGY_THRESHOLD = 25


class UnknownRoomError(ValueError):
    """Raised when a simulation references a room outside the facility."""

    def __init__(self, room: str) -> None:
        valid = ", ".join(REQUIRED_ROOMS)
        super().__init__(f"unknown room {room!r}; valid rooms: {valid}")
        self.room = room


class RouteNotFoundError(ValueError):
    """Raised when two known rooms are not connected by the facility graph."""

    def __init__(self, origin: str, destination: str) -> None:
        super().__init__(f"no route from {origin!r} to {destination!r}")
        self.origin = origin
        self.destination = destination


class UnknownScenarioError(ValueError):
    """Raised when a requested deterministic scenario is not available."""

    def __init__(self, scenario_name: str) -> None:
        valid = ", ".join(SCENARIOS)
        super().__init__(f"unknown scenario {scenario_name!r}; valid scenarios: {valid}")
        self.scenario_name = scenario_name


class InvalidScenarioJsonError(ValueError):
    """Raised when scenario JSON is malformed or missing required data."""


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
class Incident:
    time: str
    room: str
    name: str
    severity: str
    effect: str
    handling_note: str


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


MAINTENANCE_DAY_SCENARIO: tuple[Activity, ...] = (
    Activity("08:15", "Kitchen", "Early briefing", "Sarah reviews the maintenance roster over breakfast.", {"hunger": 14, "morale": 1}),
    Activity("08:45", "Control Room", "Diagnostics review", "Facility telemetry is checked before repair work begins.", {"energy": -3, "morale": 2}),
    Activity("09:30", "Workshop", "Parts staging", "Replacement parts are staged for scheduled repairs.", {"hunger": -3, "energy": -5, "morale": 3}),
    Activity("10:15", "Infirmary", "Filter inspection", "Air and water filters near the infirmary are inspected.", {"energy": -4, "health": 3}),
    Activity("11:00", "Garden", "Irrigation service", "Garden irrigation receives a planned maintenance pass.", {"hunger": -4, "energy": -4, "morale": 4, "health": 1}),
    Activity("12:00", "Control Room", "Maintenance signoff", "Sarah records the completed morning maintenance checks.", {"hunger": -5, "energy": -3, "morale": 2}),
)


MAINTENANCE_DAY_INCIDENTS: tuple[Incident, ...] = (
    Incident(
        time="08:45",
        room="Control Room",
        name="Telemetry drift",
        severity="medium",
        effect="Diagnostics require a manual sensor comparison before repairs continue.",
        handling_note="Sarah logs the drift and confirms the redundant panel before leaving Control Room.",
    ),
    Incident(
        time="11:00",
        room="Garden",
        name="Irrigation pressure drop",
        severity="high",
        effect="Garden irrigation output falls below the maintenance-day target.",
        handling_note="Sarah isolates the south valve and records the pressure recovery check.",
    ),
)


@dataclass(frozen=True)
class ScenarioDefinition:
    current_time: str
    current_room: str
    needs: Needs
    activities: tuple[Activity, ...]
    incidents: tuple[Incident, ...] = ()


SCENARIOS: dict[str, ScenarioDefinition] = {
    "default": ScenarioDefinition(
        current_time="08:00",
        current_room="Dormitory",
        needs=Needs(hunger=68, energy=82, morale=70, health=88),
        activities=DEFAULT_SCENARIO,
    ),
    "maintenance_day": ScenarioDefinition(
        current_time="08:00",
        current_room="Dormitory",
        needs=Needs(hunger=64, energy=86, morale=72, health=90),
        activities=MAINTENANCE_DAY_SCENARIO,
        incidents=MAINTENANCE_DAY_INCIDENTS,
    ),
}


@dataclass
class FacilityState:
    current_time: str
    current_room: str
    needs: Needs
    rooms: tuple[str, ...] = REQUIRED_ROOMS
    scenario: tuple[Activity, ...] = DEFAULT_SCENARIO
    scenario_name: str = "default"
    incidents: tuple[Incident, ...] = ()
    history: list[HistoryEntry] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.rooms != REQUIRED_ROOMS:
            raise ValueError("Adeptus Testus Facility must contain exactly the seven required rooms")
        if self.scenario_name not in SCENARIOS:
            raise UnknownScenarioError(self.scenario_name)
        _validate_facility_graph(FACILITY_GRAPH)
        self._require_room(self.current_room)
        for activity in self.scenario:
            self._require_room(activity.destination)
        for incident in self.incidents:
            self._require_room(incident.room)

    def move_to(self, destination: str, activity: str, reason: str, need_deltas: dict[str, int] | None = None) -> HistoryEntry:
        self._require_room(destination)
        origin = self.current_room
        self.route_between(origin, destination)
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

    def route_between(self, origin: str, destination: str) -> tuple[str, ...]:
        return route_between(origin, destination)

    def travel_duration_minutes(self, origin: str, destination: str) -> int:
        return travel_duration_minutes(origin, destination)

    def route_to(self, destination: str) -> tuple[str, ...]:
        return self.route_between(self.current_room, destination)

    def travel_duration_to(self, destination: str) -> int:
        return self.travel_duration_minutes(self.current_room, destination)

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

    def incidents_until(self, target_time: str) -> tuple[Incident, ...]:
        target = _minutes(target_time)
        return tuple(incident for incident in self.incidents if _minutes(incident.time) <= target)

    def encountered_incidents(self) -> tuple[Incident, ...]:
        current = _minutes(self.current_time)
        return tuple(
            incident
            for incident in self.incidents
            if _minutes(incident.time) <= current and incident.room == self.current_room
        )

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
            "scenario_name": self.scenario_name,
            "scenario": [_activity_to_payload(activity) for activity in self.scenario],
            "incidents": [_incident_to_payload(incident) for incident in self.incidents],
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
        scenario_name = payload.get("scenario_name", "default")
        scenario = (
            _activities_from_payload(payload["scenario"], "save JSON scenario")
            if "scenario" in payload
            else _scenario_for_name(scenario_name).activities
        )
        incidents = (
            _incidents_from_payload(payload["incidents"], "save JSON incidents")
            if "incidents" in payload
            else _scenario_for_name(scenario_name).incidents
        )
        state = cls(
            current_time=payload["current_time"],
            current_room=payload["current_room"],
            needs=Needs(**payload["needs"]),
            rooms=tuple(payload["rooms"]),
            scenario=scenario,
            scenario_name=scenario_name,
            incidents=incidents,
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
        for entry in state.history:
            state._require_room(entry.origin)
            state._require_room(entry.destination)
        return state

    def to_scenario_json(self) -> str:
        return scenario_to_json(self.scenario_name, self)

    @classmethod
    def from_scenario_json(cls, raw: str) -> "FacilityState":
        payload = _object_from_json(raw, "scenario JSON")
        name = _required_str(payload, "name", "scenario JSON")
        base = _scenario_for_name(name)
        current_time = _required_time(payload, "current_time", "scenario JSON")
        current_room = _required_str(payload, "current_room", "scenario JSON")
        needs_payload = _required_mapping(payload, "needs", "scenario JSON")
        activities_payload = _required_sequence(payload, "activities", "scenario JSON")
        incidents_payload = payload.get("incidents", [_incident_to_payload(incident) for incident in base.incidents])
        needs = _needs_from_payload(needs_payload, "scenario JSON needs")
        activities = _activities_from_payload(activities_payload, "scenario JSON activities")
        incidents = _incidents_from_payload(_sequence_value(incidents_payload, "incidents", "scenario JSON"), "scenario JSON incidents")

        state = cls(
            current_time=current_time,
            current_room=current_room,
            needs=needs,
            scenario=activities,
            scenario_name=name,
            incidents=incidents,
        )
        if not activities and base.activities:
            raise InvalidScenarioJsonError(f"scenario JSON for {name!r} must include activities")
        return state

    def _require_room(self, room: str) -> None:
        if room not in self.rooms:
            raise UnknownRoomError(room)


def route_between(origin: str, destination: str) -> tuple[str, ...]:
    _require_required_room(origin)
    _require_required_room(destination)
    if origin == destination:
        return (origin,)

    queue: list[tuple[str, ...]] = [(origin,)]
    visited = {origin}
    while queue:
        route = queue.pop(0)
        for neighbor in FACILITY_GRAPH[route[-1]]:
            if neighbor in visited:
                continue
            next_route = (*route, neighbor)
            if neighbor == destination:
                return next_route
            visited.add(neighbor)
            queue.append(next_route)
    raise RouteNotFoundError(origin, destination)


def travel_duration_minutes(origin: str, destination: str) -> int:
    route = route_between(origin, destination)
    return sum(
        FACILITY_EDGE_TRAVEL_MINUTES[_edge_key(start, end)]
        for start, end in zip(route, route[1:])
    )


def facility_for_scenario(scenario_name: str = "default") -> FacilityState:
    scenario = _scenario_for_name(scenario_name)

    return FacilityState(
        current_time=scenario.current_time,
        current_room=scenario.current_room,
        needs=scenario.needs,
        scenario=scenario.activities,
        scenario_name=scenario_name,
        incidents=scenario.incidents,
    )


def default_facility(scenario_name: str = "default") -> FacilityState:
    return facility_for_scenario(scenario_name)


def scenario_to_json(scenario_name: str, state: FacilityState | None = None) -> str:
    scenario = _scenario_for_name(scenario_name)
    source = state
    if source is None:
        source = FacilityState(
            current_time=scenario.current_time,
            current_room=scenario.current_room,
            needs=scenario.needs,
            scenario=scenario.activities,
            scenario_name=scenario_name,
            incidents=scenario.incidents,
        )
    if source.scenario_name != scenario_name:
        raise InvalidScenarioJsonError(
            f"state scenario {source.scenario_name!r} does not match requested scenario {scenario_name!r}"
        )
    payload = {
        "name": scenario_name,
        "current_time": source.current_time,
        "current_room": source.current_room,
        "needs": asdict(source.needs),
        "activities": [_activity_to_payload(activity) for activity in source.scenario],
        "incidents": [_incident_to_payload(incident) for incident in source.incidents],
    }
    return json.dumps(payload, sort_keys=True)


def facility_from_scenario_json(raw: str) -> FacilityState:
    return FacilityState.from_scenario_json(raw)


def _clamp(value: int) -> int:
    return max(0, min(100, value))


def _minutes(time_text: str) -> int:
    hour, minute = time_text.split(":", 1)
    return int(hour) * 60 + int(minute)


def _require_required_room(room: str) -> None:
    if room not in REQUIRED_ROOMS:
        raise UnknownRoomError(room)


def _validate_facility_graph(graph: Mapping[str, Sequence[str]]) -> None:
    if tuple(graph) != REQUIRED_ROOMS:
        raise ValueError("facility graph must contain exactly the seven required rooms")
    for room, neighbors in graph.items():
        for neighbor in neighbors:
            _require_required_room(neighbor)
            if room not in graph[neighbor]:
                raise ValueError(f"facility graph edge {room!r}->{neighbor!r} must be bidirectional")
            if _edge_key(room, neighbor) not in FACILITY_EDGE_TRAVEL_MINUTES:
                raise ValueError(f"facility graph edge {room!r}->{neighbor!r} is missing travel duration")


def _edge_key(origin: str, destination: str) -> frozenset[str]:
    return frozenset((origin, destination))


def _scenario_for_name(scenario_name: str) -> ScenarioDefinition:
    try:
        return SCENARIOS[scenario_name]
    except KeyError as exc:
        raise UnknownScenarioError(scenario_name) from exc


def _activity_to_payload(activity: Activity) -> dict[str, Any]:
    return {
        "time": activity.time,
        "destination": activity.destination,
        "activity": activity.activity,
        "reason": activity.reason,
        "need_deltas": dict(activity.need_deltas),
    }


def _incident_to_payload(incident: Incident) -> dict[str, Any]:
    return {
        "time": incident.time,
        "room": incident.room,
        "name": incident.name,
        "severity": incident.severity,
        "effect": incident.effect,
        "handling_note": incident.handling_note,
    }


def _object_from_json(raw: str, context: str) -> Mapping[str, Any]:
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise InvalidScenarioJsonError(f"{context} is not valid JSON") from exc
    if not isinstance(payload, Mapping):
        raise InvalidScenarioJsonError(f"{context} must be a JSON object")
    return payload


def _required_mapping(payload: Mapping[str, Any], key: str, context: str) -> Mapping[str, Any]:
    value = _required_value(payload, key, context)
    if not isinstance(value, Mapping):
        raise InvalidScenarioJsonError(f"{context} field {key!r} must be an object")
    return value


def _required_sequence(payload: Mapping[str, Any], key: str, context: str) -> Sequence[Any]:
    value = _required_value(payload, key, context)
    return _sequence_value(value, key, context)


def _sequence_value(value: Any, key: str, context: str) -> Sequence[Any]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise InvalidScenarioJsonError(f"{context} field {key!r} must be a list")
    return value


def _required_str(payload: Mapping[str, Any], key: str, context: str) -> str:
    value = _required_value(payload, key, context)
    if not isinstance(value, str):
        raise InvalidScenarioJsonError(f"{context} field {key!r} must be a string")
    return value


def _required_int(payload: Mapping[str, Any], key: str, context: str) -> int:
    value = _required_value(payload, key, context)
    if isinstance(value, bool) or not isinstance(value, int):
        raise InvalidScenarioJsonError(f"{context} field {key!r} must be an integer")
    return value


def _required_time(payload: Mapping[str, Any], key: str, context: str) -> str:
    value = _required_str(payload, key, context)
    try:
        _minutes(value)
    except (TypeError, ValueError) as exc:
        raise InvalidScenarioJsonError(f"{context} field {key!r} must be HH:MM time text") from exc
    return value


def _required_value(payload: Mapping[str, Any], key: str, context: str) -> Any:
    if key not in payload:
        raise InvalidScenarioJsonError(f"{context} missing required field {key!r}")
    return payload[key]


def _needs_from_payload(payload: Mapping[str, Any], context: str) -> Needs:
    return Needs(
        hunger=_required_int(payload, "hunger", context),
        energy=_required_int(payload, "energy", context),
        morale=_required_int(payload, "morale", context),
        health=_required_int(payload, "health", context),
    )


def _activities_from_payload(payload: Sequence[Any], context: str) -> tuple[Activity, ...]:
    activities: list[Activity] = []
    for index, item in enumerate(payload):
        item_context = f"{context}[{index}]"
        if not isinstance(item, Mapping):
            raise InvalidScenarioJsonError(f"{item_context} must be an object")
        activities.append(
            Activity(
                time=_required_time(item, "time", item_context),
                destination=_required_str(item, "destination", item_context),
                activity=_required_str(item, "activity", item_context),
                reason=_required_str(item, "reason", item_context),
                need_deltas=_need_deltas_from_payload(
                    _required_mapping(item, "need_deltas", item_context),
                    f"{item_context} need_deltas",
                ),
            )
        )
    return tuple(activities)


def _incidents_from_payload(payload: Sequence[Any], context: str) -> tuple[Incident, ...]:
    incidents: list[Incident] = []
    for index, item in enumerate(payload):
        item_context = f"{context}[{index}]"
        if not isinstance(item, Mapping):
            raise InvalidScenarioJsonError(f"{item_context} must be an object")
        incidents.append(
            Incident(
                time=_required_time(item, "time", item_context),
                room=_required_str(item, "room", item_context),
                name=_required_str(item, "name", item_context),
                severity=_required_str(item, "severity", item_context),
                effect=_required_str(item, "effect", item_context),
                handling_note=_required_str(item, "handling_note", item_context),
            )
        )
    return tuple(incidents)


def _need_deltas_from_payload(payload: Mapping[str, Any], context: str) -> dict[str, int]:
    allowed = set(Needs.__dataclass_fields__)
    deltas: dict[str, int] = {}
    for key, value in payload.items():
        if key not in allowed:
            raise InvalidScenarioJsonError(f"{context} contains unknown need {key!r}")
        if isinstance(value, bool) or not isinstance(value, int):
            raise InvalidScenarioJsonError(f"{context} field {key!r} must be an integer")
        deltas[key] = value
    return deltas

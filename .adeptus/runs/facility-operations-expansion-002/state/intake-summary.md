# Intake Summary

Run ID: `facility-operations-expansion-002`

Source intake: root-level `facility-operations-expansion-002.intake.md`. Do not require or create a `.adeptus/intake/` copy.

## Request

Expand the existing Adeptus Testus Facility Python project into a deterministic facility-operations simulator while preserving all baseline behavior from the prior run.

## Baseline To Preserve

- Package remains `adeptus_testus`.
- `python -m pytest -q` passes.
- `python -m adeptus_testus --until 12:00` and `--until 09:00` remain compatible.
- Facility has exactly seven required rooms: Dormitory, Kitchen, Workshop, Infirmary, Recreation, Garden, Control Room.
- Default scenario starts Sarah at 08:00 in Dormitory.
- Sarah does not require sleep by 09:00.
- Default deterministic scenario advances through at least 12:00.
- Renderer lists all seven rooms and marks Sarah's current room.
- JSON save/load preserves simulation state.
- Invalid rooms or invalid movement fail predictably.
- Existing tests remain meaningful and must not be deleted merely to pass new tests.

Baseline evidence already exists at `.adeptus/runs/facility-operations-expansion-002/state/baseline-validation-summary.md`: syntax validation passed and `adeptus_pytest(args=["-q"], timeout_seconds=60)` passed with `5 passed in 0.02s`, `stdin: DEVNULL`, and `timed_out: false`.

## Required Expansion

- Add explicit facility graph/pathing with deterministic travel duration and predictable validation.
- Add named deterministic scenarios, preserving default and adding at least `maintenance_day`.
- Support scenario JSON serialization/deserialization and predictable validation of room/activity structure.
- Add deterministic, scheduled incidents with time, room, name, severity/category, effect, and handling note.
- Generate deterministic operations reports with scenario, start/end time, rooms visited, timeline, incidents, final needs, and warnings. Text is required; JSON is practical and expected unless a story proves otherwise.
- Expand CLI while preserving `--until`: include scenario selection, text/json report selection, and timeline display.
- Update README concisely with preview, scenario/report commands, behavior summary, graph, incidents/reports, and test command.

## Global Constraints

- Headless, deterministic, no GUI, no curses/color UI, no network service, no database.
- Standard-library runtime only unless a new dependency is explicitly justified and reviewed.
- No randomness or wall-clock dependence.
- Do not modify installed Adeptus skill files or prior `.adeptus/runs/` artifacts.
- Use bounded packets after strategic pre-review; downstream agents must not read the full intake, full strategic plan, full project tree, full installed `SKILL.md`, full workflow, old run artifacts, or generated cache/temp directories unless explicitly escalated.
- Controller repair boundary: controller may repair only Adeptus run-state/routing/packet/review/validation/audit artifacts. Product-file repairs must route through a bounded repair packet, Enginseer implementation, Inquisitor review, then validation.

## Repository Overview

- `src/adeptus_testus/facility.py`: current model, default scenario, rendering, save/load.
- `src/adeptus_testus/cli.py`: current headless CLI with `--until`.
- `src/adeptus_testus/__main__.py`: module entry point.
- `tests/test_facility.py`: five baseline tests covering rooms, default day, save/load, render, and CLI.
- `README.md`: concise current project documentation.
- `pyproject.toml`: package metadata, standard-library runtime dependencies.

"""Command-line preview for the Adeptus Testus Facility simulation."""

from __future__ import annotations

import argparse

from .facility import default_facility


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Preview the Adeptus Testus Facility day.")
    parser.add_argument(
        "--until",
        default="12:00",
        help="Advance the deterministic normal day through this HH:MM time.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    state = default_facility()
    print(state.render())
    for entry in state.advance_until(args.until):
        print()
        print(f"{entry.time} - {entry.activity}: {entry.reason}")
        print(state.render())
    return 0

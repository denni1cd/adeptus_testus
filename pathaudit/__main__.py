"""Command line interface for pathaudit."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

from . import audit_paths, iter_manifest_entries
from .audit import CATEGORY_ORDER
from .reporting import render_json, render_rows, render_summary


SAMPLE_PATHS = (
    "pathaudit/classifier.py",
    ".adeptus/runs/run-1/state.json",
    "pkg/__pycache__/module.cpython-312.pyc",
    "../adeptus_archive",
)


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    fail_on = _parse_fail_on(args.fail_on, parser)
    paths = SAMPLE_PATHS if args.sample else tuple(_read_manifest(args.manifest))

    try:
        result = audit_paths(paths, fail_on=fail_on)
    except ValueError as exc:
        parser.error(str(exc))

    if args.format == "json":
        output = render_json(result)
    elif args.summary:
        output = render_summary(result)
    else:
        output = render_rows(result)

    if output:
        print(output)

    return 2 if result.fail_on_matches else 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pathaudit",
        description="Classify manifest paths into product and runtime categories.",
    )
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "manifest",
        nargs="?",
        type=Path,
        help="manifest file containing one path per line",
    )
    input_group.add_argument(
        "--sample",
        action="store_true",
        help="audit built-in sample paths",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="report format",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="print summary counts instead of rows for text output",
    )
    parser.add_argument(
        "--fail-on",
        metavar="CATEGORIES",
        help="comma-separated categories that should return exit code 2 when present",
    )
    return parser


def _read_manifest(path: Path | None) -> tuple[str, ...]:
    if path is None:
        return ()
    return tuple(iter_manifest_entries(path.read_text(encoding="utf-8")))


def _parse_fail_on(
    raw_categories: str | None, parser: argparse.ArgumentParser
) -> tuple[str, ...] | None:
    if raw_categories is None:
        return None

    categories = tuple(category.strip() for category in raw_categories.split(","))
    invalid = [category for category in categories if category not in CATEGORY_ORDER]
    if invalid:
        valid_text = ", ".join(CATEGORY_ORDER)
        parser.error(
            f"Unknown fail-on category: {', '.join(invalid)}. "
            f"Expected one of: {valid_text}."
        )
    return categories


if __name__ == "__main__":
    sys.exit(main())

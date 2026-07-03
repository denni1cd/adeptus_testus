"""Command line interface for pathaudit directory audits."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

from . import (
    audit_directory,
    render_directory_report_json,
    render_directory_report_text,
)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the pathaudit CLI."""

    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        result = audit_directory(
            args.root,
            ignore_patterns=args.ignore,
            top_count=args.top,
        )
    except (FileNotFoundError, NotADirectoryError, ValueError) as exc:
        parser.error(str(exc))

    if args.json:
        output = render_directory_report_json(result)
    else:
        output = render_directory_report_text(result)

    print(output)
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pathaudit",
        description="Audit files below a root directory.",
    )
    parser.add_argument(
        "root",
        type=Path,
        help="root directory to audit",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="emit deterministic JSON instead of human-readable text",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=5,
        metavar="N",
        help="number of largest files to include",
    )
    parser.add_argument(
        "--ignore",
        action="append",
        default=[],
        metavar="PATTERN",
        help="fnmatch pattern to exclude; may be repeated",
    )
    return parser


if __name__ == "__main__":
    sys.exit(main())

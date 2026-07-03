from __future__ import annotations

import argparse
from pathlib import Path

from .classifier import classify_entries, iter_manifest_entries


SAMPLE_PATHS = [
    "README.md",
    ".adeptus/runs/run-001/state/current-state.json",
    ".adeptus/preflight/target-root-check.txt",
    "../adeptus_archive/adeptus_testus/run-001/state/current-state.json",
    "pathaudit/__pycache__/classifier.cpython-312.pyc",
    ".pytest_cache/v/cache/nodeids",
    "/tmp/outside.txt",
    "src/../outside.txt",
]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pathaudit")
    parser.add_argument("manifest", nargs="?", help="UTF-8 manifest with one path per line")
    parser.add_argument("--sample", action="store_true", help="print deterministic sample classifications")
    return parser


def render(entries: list[str]) -> str:
    lines = [f"{item.kind}\t{item.path}" for item in classify_entries(entries)]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.sample:
        print(render(SAMPLE_PATHS))
        return 0

    if not args.manifest:
        parser.error("manifest is required unless --sample is used")

    text = Path(args.manifest).read_text(encoding="utf-8")
    print(render(list(iter_manifest_entries(text))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

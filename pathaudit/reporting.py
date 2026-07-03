"""Deterministic report conversion for directory audit results."""

from __future__ import annotations

import json
from typing import Any

from .audit import DirectoryAuditResult, FileAuditEntry


def directory_report_data(result: DirectoryAuditResult) -> dict[str, Any]:
    """Return a JSON-ready directory audit report with deterministic ordering."""

    return result.to_dict()


def render_directory_report_json(result: DirectoryAuditResult) -> str:
    """Render a deterministic JSON directory audit report."""

    return json.dumps(directory_report_data(result), indent=2)


def render_directory_report_text(result: DirectoryAuditResult) -> str:
    """Render a deterministic human-readable directory audit report."""

    lines = [
        f"Root: {result.root}",
        f"Total files: {result.total_files}",
        f"Total size: {result.total_size} bytes",
        "",
        "Extensions:",
    ]

    if result.extensions:
        lines.extend(
            f"  {_display_extension(extension)}: {count}"
            for extension, count in result.extensions.items()
        )
    else:
        lines.append("  (none)")

    lines.extend(["", "Largest files:"])
    if result.largest_files:
        lines.extend(f"  {_display_file(entry)}" for entry in result.largest_files)
    else:
        lines.append("  (none)")

    return "\n".join(lines)


def _display_extension(extension: str) -> str:
    return extension or "(no extension)"


def _display_file(entry: FileAuditEntry) -> str:
    return f"{entry.path} ({entry.size} bytes)"

"""Deterministic report rendering for path audit results."""

from __future__ import annotations

import json
from typing import Any

from .audit import AuditResult


def render_rows(result: AuditResult) -> str:
    """Render audit entries as category/path tab-separated rows."""

    return "\n".join(f"{entry.category}\t{entry.path}" for entry in result.entries)


def render_summary(result: AuditResult) -> str:
    """Render deterministic summary count lines."""

    return "\n".join(
        f"summary\t{category}\t{count}" for category, count in result.summary.items()
    )


def render_json(result: AuditResult) -> str:
    """Render audit result JSON with ordered entries and complete summary."""

    payload: dict[str, Any] = {
        "entries": [
            {"kind": entry.category, "path": entry.path}
            for entry in result.entries
        ],
        "summary": dict(result.summary.items()),
    }
    return json.dumps(payload, indent=2)

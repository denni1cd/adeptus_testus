"""Context preparation helpers for bounded worker inputs."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any


CONTROL_CONTEXT_FIELDS = frozenset(
    {
        "current_state_path",
        "next_action",
        "exact_next_action",
        "repair_count",
        "final_action",
        "terminal_reason",
    }
)


def prepare_worker_context(context: Mapping[Any, Any]) -> dict[Any, Any]:
    """Return a copy of worker context without internal control-state fields."""

    return {
        key: value
        for key, value in context.items()
        if key not in CONTROL_CONTEXT_FIELDS
    }

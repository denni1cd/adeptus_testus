"""Core audit result model for classified path inputs."""

from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Iterable

from .classifier import VALID_CATEGORIES, classify_path


CATEGORY_ORDER = ("product", "runtime_artifact", "generated_cache", "invalid")


@dataclass(frozen=True)
class AuditEntry:
    """One input path paired with its classifier category."""

    path: str
    category: str


@dataclass(frozen=True)
class AuditResult:
    """Classified path entries plus deterministic category summaries."""

    entries: tuple[AuditEntry, ...]
    summary: OrderedDict[str, int]
    fail_on_matches: tuple[str, ...] = field(default_factory=tuple)

    def check_fail_on(self, categories: Iterable[str]) -> tuple[str, ...]:
        """Return requested categories present in this audit result."""

        requested = _validate_categories(categories)
        return tuple(
            category
            for category in CATEGORY_ORDER
            if category in requested and self.summary[category] > 0
        )


def audit_paths(paths: Iterable[str], fail_on: Iterable[str] | None = None) -> AuditResult:
    """Classify path strings into an ordered audit result."""

    entries = tuple(AuditEntry(path=path, category=classify_path(path)) for path in paths)
    summary = OrderedDict((category, 0) for category in CATEGORY_ORDER)
    for entry in entries:
        summary[entry.category] += 1

    result = AuditResult(entries=entries, summary=summary)
    if fail_on is None:
        return result

    return AuditResult(
        entries=entries,
        summary=summary,
        fail_on_matches=result.check_fail_on(fail_on),
    )


def _validate_categories(categories: Iterable[str]) -> set[str]:
    requested = set(categories)
    unknown = requested.difference(VALID_CATEGORIES)
    if unknown:
        unknown_text = ", ".join(sorted(unknown))
        valid_text = ", ".join(CATEGORY_ORDER)
        raise ValueError(
            f"Unknown fail-on category: {unknown_text}. Expected one of: {valid_text}."
        )
    return requested

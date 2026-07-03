"""Core audit result models and filesystem audit API."""

from __future__ import annotations

import os
from collections import OrderedDict
from dataclasses import dataclass, field
from fnmatch import fnmatch
from pathlib import Path
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


@dataclass(frozen=True)
class FileAuditEntry:
    """One discovered file under an audited root."""

    path: str
    size: int
    extension: str

    def to_dict(self) -> dict[str, str | int]:
        """Return a JSON-friendly representation."""

        return {"path": self.path, "size": self.size, "extension": self.extension}


@dataclass(frozen=True)
class DirectoryAuditResult:
    """Structured result for an audited filesystem root."""

    root: str
    total_directories: int
    files: tuple[FileAuditEntry, ...]
    extensions: OrderedDict[str, int]
    largest_files: tuple[FileAuditEntry, ...]
    ignored_paths: tuple[str, ...] = field(default_factory=tuple)
    ignore_patterns: tuple[str, ...] = field(default_factory=tuple)

    @property
    def total_files(self) -> int:
        """Return the number of included files."""

        return len(self.files)

    @property
    def total_size(self) -> int:
        """Return the total size of included files in bytes."""

        return sum(entry.size for entry in self.files)

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-friendly representation with deterministic ordering."""

        return {
            "root": self.root,
            "total_files": self.total_files,
            "total_directories": self.total_directories,
            "total_size": self.total_size,
            "ignored_paths": list(self.ignored_paths),
            "files": [entry.to_dict() for entry in self.files],
            "extensions": dict(self.extensions),
            "largest_files": [entry.to_dict() for entry in self.largest_files],
            "ignore_patterns": list(self.ignore_patterns),
        }


def audit_directory(
    root: str | os.PathLike[str],
    ignore_patterns: Iterable[str] | None = None,
    top_count: int = 5,
) -> DirectoryAuditResult:
    """Audit files below root using root-relative POSIX paths."""

    if top_count < 0:
        raise ValueError("top_count must be greater than or equal to zero")

    root_path = Path(root)
    if not root_path.exists():
        raise FileNotFoundError(root_path)
    if not root_path.is_dir():
        raise NotADirectoryError(root_path)

    patterns = tuple(ignore_patterns or ())
    files, total_directories, ignored_paths = _scan_directory(root_path, patterns)
    extensions = _group_extensions(files)
    largest_files = tuple(sorted(files, key=lambda entry: (-entry.size, entry.path))[:top_count])

    return DirectoryAuditResult(
        root=str(root_path),
        total_directories=total_directories,
        files=files,
        extensions=extensions,
        largest_files=largest_files,
        ignored_paths=ignored_paths,
        ignore_patterns=patterns,
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


def _scan_directory(
    root_path: Path, ignore_patterns: tuple[str, ...]
) -> tuple[tuple[FileAuditEntry, ...], int, tuple[str, ...]]:
    entries: list[FileAuditEntry] = []
    ignored_paths: list[str] = []
    total_directories = 0

    for current_root, dirnames, filenames in os.walk(root_path):
        total_directories += 1
        dirnames.sort()
        filenames.sort()

        current_path = Path(current_root)
        kept_dirnames = []
        for dirname in dirnames:
            relative_path = _relative_posix_path(current_path / dirname, root_path)
            if _is_ignored(relative_path, ignore_patterns):
                ignored_paths.append(relative_path)
            else:
                kept_dirnames.append(dirname)
        dirnames[:] = kept_dirnames

        for filename in filenames:
            file_path = current_path / filename
            relative_path = _relative_posix_path(file_path, root_path)
            if _is_ignored(relative_path, ignore_patterns):
                ignored_paths.append(relative_path)
                continue

            entries.append(
                FileAuditEntry(
                    path=relative_path,
                    size=file_path.stat().st_size,
                    extension=_extension_for(relative_path),
                )
            )

    return (
        tuple(sorted(entries, key=lambda entry: entry.path)),
        total_directories,
        tuple(sorted(ignored_paths)),
    )


def _relative_posix_path(path: Path, root_path: Path) -> str:
    return path.relative_to(root_path).as_posix()


def _is_ignored(relative_path: str, ignore_patterns: tuple[str, ...]) -> bool:
    return any(fnmatch(relative_path, pattern) for pattern in ignore_patterns)


def _extension_for(relative_path: str) -> str:
    return Path(relative_path).suffix.lower()


def _group_extensions(files: tuple[FileAuditEntry, ...]) -> OrderedDict[str, int]:
    counts: dict[str, int] = {}
    for entry in files:
        counts[entry.extension] = counts.get(entry.extension, 0) + 1
    return OrderedDict((extension, counts[extension]) for extension in sorted(counts))


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

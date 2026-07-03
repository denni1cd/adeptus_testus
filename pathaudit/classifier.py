from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath, PureWindowsPath


@dataclass(frozen=True)
class Classification:
    path: str
    kind: str


def iter_manifest_entries(text: str):
    for line in text.splitlines():
        entry = line.strip()
        if entry and not entry.startswith("#"):
            yield entry


def classify_path(path: str) -> str:
    candidate = path.strip().replace("\\", "/")
    if not candidate:
        return "invalid"

    if candidate.startswith(".adeptus/runs/"):
        return "runtime_artifact"
    if candidate.startswith(".adeptus/preflight/"):
        return "runtime_artifact"
    if candidate.startswith("../adeptus_archive/"):
        rest = candidate[len("../adeptus_archive/") :]
        if rest and ".." not in PurePosixPath(rest).parts:
            return "runtime_artifact"
        return "invalid"

    posix = PurePosixPath(candidate)
    windows = PureWindowsPath(candidate)
    if posix.is_absolute() or windows.is_absolute():
        return "invalid"

    parts = posix.parts
    if not parts or ".." in parts:
        return "invalid"

    if "__pycache__" in parts:
        return "generated_cache"
    if candidate.endswith(".pyc"):
        return "generated_cache"
    if parts[0] == ".pytest_cache":
        return "generated_cache"

    normalized = posix.as_posix()
    if normalized in ("", "."):
        return "invalid"
    return "product"


def classify_entries(entries) -> list[Classification]:
    return [Classification(path=entry, kind=classify_path(entry)) for entry in entries]

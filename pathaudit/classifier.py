"""Pure string classification helpers for path audit inputs."""

from __future__ import annotations

from pathlib import PureWindowsPath


VALID_CATEGORIES = {"product", "runtime_artifact", "generated_cache", "invalid"}


def classify_path(path: str) -> str:
    """Classify a path string without consulting the filesystem."""

    normalized = _normalize_path_text(path)
    if not normalized:
        return "invalid"

    if _is_absolute_path(normalized):
        return "invalid"

    parts = [part for part in normalized.split("/") if part]
    if not parts:
        return "invalid"

    if _is_safe_archive_path(parts):
        return "runtime_artifact"

    if ".." in parts:
        return "invalid"

    if _is_adeptus_runtime_path(parts):
        return "runtime_artifact"

    if _is_generated_cache_path(normalized, parts):
        return "generated_cache"

    return "product"


def iter_manifest_entries(text: str):
    """Yield ordered manifest entries, skipping blank and first-char comments."""

    for line in text.splitlines():
        if not line or line.strip() == "":
            continue
        if line[0] == "#":
            continue
        yield line


def _normalize_path_text(path: str) -> str:
    normalized = path.replace("\\", "/")
    while "//" in normalized:
        normalized = normalized.replace("//", "/")
    normalized = normalized.removeprefix("./")
    normalized = normalized.rstrip("/")
    if normalized == ".":
        return ""
    return normalized


def _is_absolute_path(path: str) -> bool:
    if path.startswith("/"):
        return True
    windows_path = PureWindowsPath(path)
    return windows_path.is_absolute() or bool(windows_path.drive)


def _is_safe_archive_path(parts: list[str]) -> bool:
    return (
        len(parts) >= 3
        and parts[0] == ".."
        and parts[1] == "adeptus_archive"
        and ".." not in parts[2:]
    )


def _is_adeptus_runtime_path(parts: list[str]) -> bool:
    return len(parts) >= 2 and parts[0] == ".adeptus" and parts[1] in {
        "runs",
        "preflight",
    }


def _is_generated_cache_path(path: str, parts: list[str]) -> bool:
    return (
        "__pycache__" in parts
        or path.endswith(".pyc")
        or parts[0] == ".pytest_cache"
    )

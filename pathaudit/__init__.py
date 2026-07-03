"""Public API for pathaudit."""

from .audit import (
    AuditEntry,
    AuditResult,
    DirectoryAuditResult,
    FileAuditEntry,
    audit_directory,
    audit_paths,
)
from .classifier import classify_path, iter_manifest_entries
from .reporting import (
    directory_report_data,
    render_directory_report_json,
    render_directory_report_text,
)

__all__ = [
    "AuditEntry",
    "AuditResult",
    "DirectoryAuditResult",
    "FileAuditEntry",
    "audit_directory",
    "audit_paths",
    "classify_path",
    "directory_report_data",
    "iter_manifest_entries",
    "render_directory_report_json",
    "render_directory_report_text",
]

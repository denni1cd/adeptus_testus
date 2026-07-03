from collections import OrderedDict
import json

import pytest

from pathaudit import (
    AuditEntry,
    AuditResult,
    DirectoryAuditResult,
    FileAuditEntry,
    audit_directory,
    audit_paths,
    directory_report_data,
    render_directory_report_json,
    render_directory_report_text,
)


def test_audit_paths_returns_ordered_entries_with_classifier_categories():
    result = audit_paths(
        [
            "pathaudit/classifier.py",
            ".adeptus/runs/run-1/state.json",
            "pkg/__pycache__/module.cpython-312.pyc",
            "../adeptus_archive",
        ]
    )

    assert isinstance(result, AuditResult)
    assert result.entries == (
        AuditEntry("pathaudit/classifier.py", "product"),
        AuditEntry(".adeptus/runs/run-1/state.json", "runtime_artifact"),
        AuditEntry("pkg/__pycache__/module.cpython-312.pyc", "generated_cache"),
        AuditEntry("../adeptus_archive", "invalid"),
    )


def test_summary_includes_all_categories_in_deterministic_order_with_zeros():
    result = audit_paths(["pathaudit/audit.py", ".adeptus/preflight/check.json"])

    assert list(result.summary.items()) == [
        ("product", 1),
        ("runtime_artifact", 1),
        ("generated_cache", 0),
        ("invalid", 0),
    ]


def test_fail_on_check_reports_present_valid_categories():
    result = audit_paths(
        ["pathaudit/audit.py", "../adeptus_archive", ".pytest_cache/v/cache/nodeids"]
    )

    assert result.check_fail_on(["invalid", "runtime_artifact", "product"]) == (
        "product",
        "invalid",
    )
    assert result.check_fail_on(["runtime_artifact"]) == ()


def test_audit_paths_can_populate_fail_on_matches():
    result = audit_paths(
        ["pathaudit/audit.py", "pkg/module.pyc"],
        fail_on=["generated_cache", "runtime_artifact"],
    )

    assert result.fail_on_matches == ("generated_cache",)


def test_fail_on_check_rejects_unknown_categories_with_useful_error():
    result = audit_paths(["pathaudit/audit.py"])

    with pytest.raises(
        ValueError, match="Unknown fail-on category: typo.*Expected one of: product"
    ):
        result.check_fail_on(["product", "typo"])

    with pytest.raises(ValueError, match="Unknown fail-on category: typo"):
        audit_paths(["pathaudit/audit.py"], fail_on=["typo"])


def test_audit_directory_returns_deterministic_files_groups_and_largest(tmp_path):
    write_file(tmp_path / "b.txt", "1234")
    write_file(tmp_path / "a.py", "12")
    write_file(tmp_path / "nested" / "c.TXT", "123")
    write_file(tmp_path / "README", "1234")
    write_file(tmp_path / "tie.bin", "1234")

    result = audit_directory(tmp_path, top_count=3)

    assert isinstance(result, DirectoryAuditResult)
    assert result.files == (
        FileAuditEntry("README", 4, ""),
        FileAuditEntry("a.py", 2, ".py"),
        FileAuditEntry("b.txt", 4, ".txt"),
        FileAuditEntry("nested/c.TXT", 3, ".txt"),
        FileAuditEntry("tie.bin", 4, ".bin"),
    )
    assert result.extensions == OrderedDict(
        [("", 1), (".bin", 1), (".py", 1), (".txt", 2)]
    )
    assert result.largest_files == (
        FileAuditEntry("README", 4, ""),
        FileAuditEntry("b.txt", 4, ".txt"),
        FileAuditEntry("tie.bin", 4, ".bin"),
    )
    assert result.total_files == 5
    assert result.total_size == 17


def test_audit_directory_ignore_patterns_exclude_counts_groups_and_largest(tmp_path):
    write_file(tmp_path / "keep.py", "1")
    write_file(tmp_path / "skip.py", "123456")
    write_file(tmp_path / "build" / "output.log", "123456789")
    write_file(tmp_path / "docs" / "keep.md", "12")

    result = audit_directory(
        tmp_path,
        ignore_patterns=["skip.py", "build/*"],
        top_count=5,
    )

    assert result.files == (
        FileAuditEntry("docs/keep.md", 2, ".md"),
        FileAuditEntry("keep.py", 1, ".py"),
    )
    assert result.extensions == OrderedDict([(".md", 1), (".py", 1)])
    assert result.largest_files == (
        FileAuditEntry("docs/keep.md", 2, ".md"),
        FileAuditEntry("keep.py", 1, ".py"),
    )
    assert result.ignore_patterns == ("skip.py", "build/*")


def test_audit_directory_default_top_count_is_five(tmp_path):
    for index in range(6):
        write_file(tmp_path / f"{index}.dat", "x" * (index + 1))

    result = audit_directory(tmp_path)

    assert [entry.path for entry in result.largest_files] == [
        "5.dat",
        "4.dat",
        "3.dat",
        "2.dat",
        "1.dat",
    ]


def test_audit_directory_to_dict_is_json_friendly(tmp_path):
    write_file(tmp_path / "a.py", "12")

    result = audit_directory(tmp_path)

    assert result.to_dict() == {
        "root": str(tmp_path),
        "total_files": 1,
        "total_size": 2,
        "files": [{"path": "a.py", "size": 2, "extension": ".py"}],
        "extensions": {".py": 1},
        "largest_files": [{"path": "a.py", "size": 2, "extension": ".py"}],
        "ignore_patterns": [],
    }


def test_directory_report_data_preserves_deterministic_group_and_largest_order(tmp_path):
    write_file(tmp_path / "z.txt", "1234")
    write_file(tmp_path / "a.py", "12")
    write_file(tmp_path / "README", "1234")
    write_file(tmp_path / "ignored.log", "123456789")

    result = audit_directory(tmp_path, ignore_patterns=["ignored.log"], top_count=2)

    assert directory_report_data(result) == {
        "root": str(tmp_path),
        "total_files": 3,
        "total_size": 10,
        "files": [
            {"path": "README", "size": 4, "extension": ""},
            {"path": "a.py", "size": 2, "extension": ".py"},
            {"path": "z.txt", "size": 4, "extension": ".txt"},
        ],
        "extensions": {"": 1, ".py": 1, ".txt": 1},
        "largest_files": [
            {"path": "README", "size": 4, "extension": ""},
            {"path": "z.txt", "size": 4, "extension": ".txt"},
        ],
        "ignore_patterns": ["ignored.log"],
    }


def test_render_directory_report_text_is_stable_and_excludes_ignored_files(tmp_path):
    write_file(tmp_path / "b.txt", "1234")
    write_file(tmp_path / "a.py", "12")
    write_file(tmp_path / "README", "1234")
    write_file(tmp_path / "ignored.bin", "123456")

    result = audit_directory(tmp_path, ignore_patterns=["ignored.bin"], top_count=2)
    rendered = render_directory_report_text(result)

    assert rendered == render_directory_report_text(result)
    assert rendered.splitlines() == [
        f"Root: {tmp_path}",
        "Total files: 3",
        "Total size: 10 bytes",
        "",
        "Extensions:",
        "  (no extension): 1",
        "  .py: 1",
        "  .txt: 1",
        "",
        "Largest files:",
        "  README (4 bytes)",
        "  b.txt (4 bytes)",
    ]
    assert "ignored.bin" not in rendered


def test_render_directory_report_json_serializes_ordered_report_data(tmp_path):
    write_file(tmp_path / "b.txt", "1234")
    write_file(tmp_path / "a.py", "12")

    result = audit_directory(tmp_path, top_count=2)

    assert render_directory_report_json(result) == (
        "{\n"
        f'  "root": {json.dumps(str(tmp_path))},\n'
        '  "total_files": 2,\n'
        '  "total_size": 6,\n'
        '  "files": [\n'
        "    {\n"
        '      "path": "a.py",\n'
        '      "size": 2,\n'
        '      "extension": ".py"\n'
        "    },\n"
        "    {\n"
        '      "path": "b.txt",\n'
        '      "size": 4,\n'
        '      "extension": ".txt"\n'
        "    }\n"
        "  ],\n"
        '  "extensions": {\n'
        '    ".py": 1,\n'
        '    ".txt": 1\n'
        "  },\n"
        '  "largest_files": [\n'
        "    {\n"
        '      "path": "b.txt",\n'
        '      "size": 4,\n'
        '      "extension": ".txt"\n'
        "    },\n"
        "    {\n"
        '      "path": "a.py",\n'
        '      "size": 2,\n'
        '      "extension": ".py"\n'
        "    }\n"
        "  ],\n"
        '  "ignore_patterns": []\n'
        "}"
    )


def test_audit_directory_rejects_invalid_root_and_negative_top_count(tmp_path):
    file_path = tmp_path / "file.txt"
    write_file(file_path, "x")

    with pytest.raises(FileNotFoundError):
        audit_directory(tmp_path / "missing")
    with pytest.raises(NotADirectoryError):
        audit_directory(file_path)
    with pytest.raises(ValueError, match="top_count"):
        audit_directory(tmp_path, top_count=-1)


def write_file(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

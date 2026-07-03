import pytest

from pathaudit import AuditEntry, AuditResult, audit_paths


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

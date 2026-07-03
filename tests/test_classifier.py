from pathaudit.classifier import classify_path, iter_manifest_entries


def test_manifest_entries_skip_blank_and_comment_lines():
    text = "\n# comment\nREADME.md\n  \n pathaudit/classifier.py \n"

    assert list(iter_manifest_entries(text)) == ["README.md", "pathaudit/classifier.py"]


def test_classifier_required_categories():
    cases = {
        "README.md": "product",
        "pathaudit/classifier.py": "product",
        ".adeptus/runs/run-1/state/current-state.json": "runtime_artifact",
        ".adeptus/preflight/target-root-check.txt": "runtime_artifact",
        "../adeptus_archive/adeptus_testus/run-1/state/current-state.json": "runtime_artifact",
        "pkg/__pycache__/mod.cpython-312.pyc": "generated_cache",
        "pkg/mod.pyc": "generated_cache",
        ".pytest_cache/v/cache/nodeids": "generated_cache",
        "/tmp/outside": "invalid",
        "C:/tmp/outside": "invalid",
        "src/../outside": "invalid",
        "../elsewhere/file.txt": "invalid",
        "../adeptus_archive/../escape": "invalid",
        "": "invalid",
    }

    for path, expected in cases.items():
        assert classify_path(path) == expected

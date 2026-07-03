import json
import subprocess
import sys


def run_pathaudit(*args):
    return subprocess.run(
        [sys.executable, "-B", "-m", "pathaudit", *args],
        check=False,
        text=True,
        capture_output=True,
    )


def write_manifest(tmp_path):
    manifest = tmp_path / "manifest.txt"
    manifest.write_text(
        "\n".join(
            [
                "# ignored",
                "pathaudit/classifier.py",
                ".adeptus/runs/run-1/state.json",
                "pkg/__pycache__/module.cpython-312.pyc",
                "../adeptus_archive",
            ]
        ),
        encoding="utf-8",
    )
    return manifest


def test_sample_default_outputs_ordered_text_rows():
    completed = run_pathaudit("--sample")

    assert completed.returncode == 0
    assert completed.stderr == ""
    assert completed.stdout.splitlines() == [
        "product\tpathaudit/classifier.py",
        "runtime_artifact\t.adeptus/runs/run-1/state.json",
        "generated_cache\tpkg/__pycache__/module.cpython-312.pyc",
        "invalid\t../adeptus_archive",
    ]


def test_sample_json_is_parseable_with_ordered_entries_and_complete_summary():
    completed = run_pathaudit("--sample", "--format", "json")

    assert completed.returncode == 0
    payload = json.loads(completed.stdout)
    assert payload == {
        "entries": [
            {"kind": "product", "path": "pathaudit/classifier.py"},
            {
                "kind": "runtime_artifact",
                "path": ".adeptus/runs/run-1/state.json",
            },
            {
                "kind": "generated_cache",
                "path": "pkg/__pycache__/module.cpython-312.pyc",
            },
            {"kind": "invalid", "path": "../adeptus_archive"},
        ],
        "summary": {
            "product": 1,
            "runtime_artifact": 1,
            "generated_cache": 1,
            "invalid": 1,
        },
    }


def test_manifest_default_outputs_ordered_text_rows(tmp_path):
    completed = run_pathaudit(str(write_manifest(tmp_path)))

    assert completed.returncode == 0
    assert completed.stdout.splitlines() == [
        "product\tpathaudit/classifier.py",
        "runtime_artifact\t.adeptus/runs/run-1/state.json",
        "generated_cache\tpkg/__pycache__/module.cpython-312.pyc",
        "invalid\t../adeptus_archive",
    ]


def test_manifest_summary_includes_all_categories(tmp_path):
    completed = run_pathaudit(str(write_manifest(tmp_path)), "--summary")

    assert completed.returncode == 0
    assert completed.stdout.splitlines() == [
        "summary\tproduct\t1",
        "summary\truntime_artifact\t1",
        "summary\tgenerated_cache\t1",
        "summary\tinvalid\t1",
    ]


def test_manifest_json_is_parseable_with_ordered_entries_and_complete_summary(tmp_path):
    completed = run_pathaudit(str(write_manifest(tmp_path)), "--format", "json")

    assert completed.returncode == 0
    payload = json.loads(completed.stdout)
    assert [entry["kind"] for entry in payload["entries"]] == [
        "product",
        "runtime_artifact",
        "generated_cache",
        "invalid",
    ]
    assert payload["summary"] == {
        "product": 1,
        "runtime_artifact": 1,
        "generated_cache": 1,
        "invalid": 1,
    }


def test_manifest_fail_on_invalid_returns_exit_2(tmp_path):
    completed = run_pathaudit(str(write_manifest(tmp_path)), "--fail-on", "invalid")

    assert completed.returncode == 2
    assert "invalid\t../adeptus_archive" in completed.stdout
    assert completed.stderr == ""


def test_manifest_fail_on_multiple_matching_categories_returns_exit_2(tmp_path):
    completed = run_pathaudit(
        str(write_manifest(tmp_path)),
        "--fail-on",
        "invalid,runtime_artifact,generated_cache",
    )

    assert completed.returncode == 2
    assert "runtime_artifact\t.adeptus/runs/run-1/state.json" in completed.stdout
    assert "generated_cache\tpkg/__pycache__/module.cpython-312.pyc" in completed.stdout


def test_invalid_fail_on_category_is_rejected(tmp_path):
    completed = run_pathaudit(str(write_manifest(tmp_path)), "--fail-on", "typo")

    assert completed.returncode != 0
    assert completed.stdout == ""
    assert "Unknown fail-on category: typo" in completed.stderr

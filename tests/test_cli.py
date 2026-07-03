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


def test_cli_default_outputs_deterministic_human_readable_audit(tmp_path):
    write_file(tmp_path / "b.txt", "1234")
    write_file(tmp_path / "a.py", "12")
    write_file(tmp_path / "README", "1234")

    completed = run_pathaudit(str(tmp_path))

    assert completed.returncode == 0
    assert completed.stderr == ""
    assert completed.stdout.splitlines() == [
        f"Root: {tmp_path}",
        "Total files: 3",
        "Total directories: 1",
        "Total size: 10 bytes",
        "",
        "Ignored paths:",
        "  (none)",
        "",
        "Extensions:",
        "  (no extension): 1",
        "  .py: 1",
        "  .txt: 1",
        "",
        "Largest files:",
        "  README (4 bytes)",
        "  b.txt (4 bytes)",
        "  a.py (2 bytes)",
    ]


def test_cli_json_output_is_parseable_and_uses_root_path(tmp_path):
    write_file(tmp_path / "b.txt", "1234")
    write_file(tmp_path / "a.py", "12")

    completed = run_pathaudit(str(tmp_path), "--json")

    assert completed.returncode == 0
    assert completed.stderr == ""
    payload = json.loads(completed.stdout)
    assert payload == {
        "root": str(tmp_path),
        "total_files": 2,
        "total_directories": 1,
        "total_size": 6,
        "ignored_paths": [],
        "files": [
            {"path": "a.py", "size": 2, "extension": ".py"},
            {"path": "b.txt", "size": 4, "extension": ".txt"},
        ],
        "extensions": {".py": 1, ".txt": 1},
        "largest_files": [
            {"path": "b.txt", "size": 4, "extension": ".txt"},
            {"path": "a.py", "size": 2, "extension": ".py"},
        ],
        "ignore_patterns": [],
    }


def test_cli_top_count_limits_largest_files(tmp_path):
    for index in range(4):
        write_file(tmp_path / f"{index}.dat", "x" * (index + 1))

    completed = run_pathaudit(str(tmp_path), "--top", "2", "--json")

    assert completed.returncode == 0
    payload = json.loads(completed.stdout)
    assert [entry["path"] for entry in payload["largest_files"]] == [
        "3.dat",
        "2.dat",
    ]


def test_cli_repeatable_ignore_patterns_are_applied(tmp_path):
    write_file(tmp_path / "keep.py", "1")
    write_file(tmp_path / "skip.py", "123456")
    write_file(tmp_path / "build" / "output.log", "123456789")
    write_file(tmp_path / "docs" / "keep.md", "12")

    completed = run_pathaudit(
        str(tmp_path),
        "--ignore",
        "skip.py",
        "--ignore",
        "build/*",
        "--json",
    )

    assert completed.returncode == 0
    payload = json.loads(completed.stdout)
    assert payload["files"] == [
        {"path": "docs/keep.md", "size": 2, "extension": ".md"},
        {"path": "keep.py", "size": 1, "extension": ".py"},
    ]
    assert payload["total_directories"] == 3
    assert payload["ignored_paths"] == ["build/output.log", "skip.py"]
    assert payload["ignore_patterns"] == ["skip.py", "build/*"]


def test_cli_default_top_count_is_five(tmp_path):
    for index in range(6):
        write_file(tmp_path / f"{index}.dat", "x" * (index + 1))

    completed = run_pathaudit(str(tmp_path), "--json")

    assert completed.returncode == 0
    payload = json.loads(completed.stdout)
    assert [entry["path"] for entry in payload["largest_files"]] == [
        "5.dat",
        "4.dat",
        "3.dat",
        "2.dat",
        "1.dat",
    ]


def write_file(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

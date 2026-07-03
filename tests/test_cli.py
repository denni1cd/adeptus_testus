import subprocess
import sys


def test_sample_cli_outputs_deterministic_classifications():
    result = subprocess.run(
        [sys.executable, "-m", "pathaudit", "--sample"],
        check=True,
        capture_output=True,
        text=True,
    )

    assert result.stdout.splitlines() == [
        "product\tREADME.md",
        "runtime_artifact\t.adeptus/runs/run-001/state/current-state.json",
        "runtime_artifact\t.adeptus/preflight/target-root-check.txt",
        "runtime_artifact\t../adeptus_archive/adeptus_testus/run-001/state/current-state.json",
        "generated_cache\tpathaudit/__pycache__/classifier.cpython-312.pyc",
        "generated_cache\t.pytest_cache/v/cache/nodeids",
        "invalid\t/tmp/outside.txt",
        "invalid\tsrc/../outside.txt",
    ]


def test_manifest_cli_skips_comments_and_blank_lines(tmp_path):
    manifest = tmp_path / "manifest.txt"
    manifest.write_text("# skip\n\nREADME.md\n.adeptus/runs/run-1/log.txt\n", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "pathaudit", str(manifest)],
        check=True,
        capture_output=True,
        text=True,
    )

    assert result.stdout.splitlines() == [
        "product\tREADME.md",
        "runtime_artifact\t.adeptus/runs/run-1/log.txt",
    ]

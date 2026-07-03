from pathaudit import classify_path, iter_manifest_entries


def test_classifies_runtime_artifacts_for_adeptus_and_safe_archive_paths():
    assert classify_path(".adeptus/runs/run-1/state.json") == "runtime_artifact"
    assert classify_path(".adeptus/preflight/check.json") == "runtime_artifact"
    assert classify_path("../adeptus_archive/run-id/packets/S001.md") == "runtime_artifact"
    assert classify_path("../adeptus_archive/run-id") == "runtime_artifact"


def test_rejects_unsafe_archive_remainder_and_other_invalid_paths():
    assert classify_path("../adeptus_archive") == "invalid"
    assert classify_path("../adeptus_archive/../outside") == "invalid"
    assert classify_path("../outside") == "invalid"
    assert classify_path("/tmp/product.py") == "invalid"
    assert classify_path("C:/tmp/product.py") == "invalid"
    assert classify_path(r"C:\tmp\product.py") == "invalid"
    assert classify_path("") == "invalid"
    assert classify_path(".") == "invalid"
    assert classify_path("./") == "invalid"


def test_classifies_generated_cache_paths():
    assert classify_path("pkg/__pycache__/module.cpython-312.pyc") == "generated_cache"
    assert classify_path("pkg/module.pyc") == "generated_cache"
    assert classify_path(".pytest_cache/v/cache/nodeids") == "generated_cache"


def test_classifies_ordinary_relative_product_paths():
    assert classify_path("pathaudit/classifier.py") == "product"
    assert classify_path("tests/test_classifier.py") == "product"


def test_iter_manifest_entries_preserves_order_and_remaining_text():
    text = "\n".join(
        [
            "",
            "#comment",
            "pathaudit/classifier.py",
            "  # kept because first character is not hash",
            "   ",
            "tests/test_classifier.py",
            "path with trailing spaces  ",
        ]
    )

    assert list(iter_manifest_entries(text)) == [
        "pathaudit/classifier.py",
        "  # kept because first character is not hash",
        "tests/test_classifier.py",
        "path with trailing spaces  ",
    ]

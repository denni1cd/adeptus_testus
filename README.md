# pathaudit

`pathaudit` classifies path lists into product and boundary-related categories. It can audit a built-in sample or a manifest file with one path per line.

## CLI usage

Run the built-in sample:

```powershell
python -B -m pathaudit --sample
```

Expected text rows are tab-separated as `<category><TAB><path>`:

```text
product	pathaudit/classifier.py
runtime_artifact	.adeptus/runs/run-1/state.json
generated_cache	pkg/__pycache__/module.cpython-312.pyc
invalid	../adeptus_archive
```

Run the same sample as JSON:

```powershell
python -B -m pathaudit --sample --format json
```

JSON output contains ordered `entries` with `kind` and `path`, plus a complete `summary`:

```json
{
  "entries": [
    {
      "kind": "product",
      "path": "pathaudit/classifier.py"
    },
    {
      "kind": "runtime_artifact",
      "path": ".adeptus/runs/run-1/state.json"
    },
    {
      "kind": "generated_cache",
      "path": "pkg/__pycache__/module.cpython-312.pyc"
    },
    {
      "kind": "invalid",
      "path": "../adeptus_archive"
    }
  ],
  "summary": {
    "product": 1,
    "runtime_artifact": 1,
    "generated_cache": 1,
    "invalid": 1
  }
}
```

Audit a manifest file:

```powershell
python -B -m pathaudit .\manifest.txt
```

Manifest files use one path per line. Blank lines and lines starting with `#` are ignored.

Summary mode prints tab-separated rows as `summary<TAB><category><TAB><count>`:

```powershell
python -B -m pathaudit .\manifest.txt --summary
```

```text
summary	product	1
summary	runtime_artifact	1
summary	generated_cache	1
summary	invalid	1
```

Manifest JSON uses the same shape as sample JSON:

```powershell
python -B -m pathaudit .\manifest.txt --format json
```

Use `--fail-on` to return exit code `2` when any requested category is present. Output is still printed in the selected format.

```powershell
python -B -m pathaudit .\manifest.txt --fail-on invalid
python -B -m pathaudit .\manifest.txt --fail-on invalid,runtime_artifact,generated_cache
```

Supported fail-on categories are `product`, `runtime_artifact`, `generated_cache`, and `invalid`. An unknown category is rejected before auditing:

```powershell
python -B -m pathaudit .\manifest.txt --fail-on typo
```

```text
pathaudit: error: Unknown fail-on category: typo. Expected one of: product, runtime_artifact, generated_cache, invalid.
```

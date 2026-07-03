# Adeptus Project Intake: archive-boundary-integration-002

## Requested Action

Run Adeptus Engineerium in the current target repository and perform a more detailed integration test of the sibling archive runtime-artifact model.

Target repository: the current working directory, expected to be `adeptus_testus`.

This test may run against either:

1. a cleaned empty target repository, or
2. the existing `pathaudit` package produced by the previous archive-boundary smoke test.

If `pathaudit` already exists, upgrade it in place. If the repository is clean, create the full product described below.

## Test Purpose

This run should test more than basic archive placement. It should verify that Adeptus can complete a multi-step product update while preserving strict separation among:

- target repository product files,
- sibling Adeptus archive artifacts,
- generated validation cache/temp artifacts,
- controller-owned run state.

The run should also test a known evidence weakness from the previous smoke run: work items and reviews should make clear whether each product file was created, modified, or only verified by the story phase.

## Required Runtime Boundary

Adeptus runtime artifacts must be written outside the target repository under the sibling archive layout:

```text
<target_repo_parent>/adeptus_archive/<target_repo_name>/<run-id>/
```

The target repository must not contain persistent:

```text
.adeptus/runs/
.adeptus/preflight/
```

A temporary preflight sentinel is allowed only if removed before Strategos begins.

## Product Goal

Create or upgrade a small Python CLI package named `pathaudit`.

`pathaudit` classifies manifest paths and can emit both detailed entry output and summary counts. It is intentionally small and deterministic. It must not become a repository scanner, policy engine, daemon, database, web app, plugin framework, or Git integration.

The product should be useful as a tiny standalone path classification utility.

## Product CLI

The CLI should support:

```bash
python -m pathaudit --sample
python -m pathaudit --sample --format json
python -m pathaudit path/to/manifest.txt
python -m pathaudit path/to/manifest.txt --summary
python -m pathaudit path/to/manifest.txt --format json
python -m pathaudit path/to/manifest.txt --fail-on invalid
python -m pathaudit path/to/manifest.txt --fail-on invalid,runtime_artifact,generated_cache
```

## Product Behavior

A manifest is a UTF-8 text file with one path per line.

Blank lines and lines beginning with `#` are ignored.

For each path, classify it as one of:

- `product` — normal product-repository path
- `runtime_artifact` — Adeptus runtime artifact path that should not be product evidence
- `generated_cache` — cache/temp artifact such as pytest cache or Python bytecode
- `invalid` — path escapes, absolute paths, or otherwise unsafe paths

Classification rules:

- Paths beginning with `.adeptus/runs/` are `runtime_artifact`.
- Paths beginning with `.adeptus/preflight/` are `runtime_artifact`.
- Paths beginning with `../adeptus_archive/` are `runtime_artifact` only when the remainder does not contain a `..` path segment.
- Paths containing `__pycache__/`, ending with `.pyc`, or beginning with `.pytest_cache/` are `generated_cache`.
- Absolute POSIX paths are `invalid`.
- Windows absolute paths such as `C:/tmp/file.txt` or `C:\tmp\file.txt` are `invalid`.
- Paths containing unsafe `..` segments are `invalid`, except for the allowed leading `../adeptus_archive/` prefix described above.
- Empty normalized paths are `invalid`.
- All other relative paths are `product`.

The classifier must be deterministic and must not inspect the actual filesystem.

## Required Library API

Expose a small API from `pathaudit`:

```python
classify_path(path: str) -> str
iter_manifest_entries(text: str)
audit_paths(paths: Iterable[str]) -> AuditResult
```

`AuditResult` should provide:

- ordered classified entries
- summary counts by classification
- a way to test whether any entry belongs to a requested fail-on category

The exact implementation shape may vary, but the behavior above must be covered by tests.

## Output Requirements

### Default Text Output

Default output should remain one tab-separated classification and path per non-comment manifest entry:

```text
product	README.md
runtime_artifact	.adeptus/runs/run-001/state/current-state.json
```

### Summary Text Output

With `--summary`, include classification counts in deterministic order after the entry lines or as a clearly separated deterministic block.

Required categories must appear even when count is zero:

```text
summary	product	1
summary	runtime_artifact	1
summary	generated_cache	0
summary	invalid	0
```

### JSON Output

With `--format json`, output deterministic JSON with this shape or a very close equivalent:

```json
{
  "entries": [
    {"path": "README.md", "kind": "product"}
  ],
  "summary": {
    "product": 1,
    "runtime_artifact": 0,
    "generated_cache": 0,
    "invalid": 0
  }
}
```

The JSON must be parseable by Python's standard `json` module.

### Fail-On Behavior

`--fail-on` accepts a comma-separated list of classifications.

If any classified entry matches any fail-on category, the CLI should exit with code `2`.

If no matching category is present, the CLI should exit with code `0`.

Invalid category names in `--fail-on` should exit nonzero and show a useful error message.

## Required Product Files

Expected product files may include:

- `README.md`
- `pyproject.toml`
- `pathaudit/__init__.py`
- `pathaudit/__main__.py`
- `pathaudit/classifier.py`
- `pathaudit/audit.py`
- `pathaudit/output.py`
- `tests/test_classifier.py`
- `tests/test_audit.py`
- `tests/test_cli.py`

Do not create product code outside the target repository.

Do not modify Adeptus skill source during this target run.

## Acceptance Criteria

AC01. `python -m pathaudit --sample` exits successfully and prints deterministic text classifications.

AC02. `python -m pathaudit --sample --format json` exits successfully and prints parseable deterministic JSON.

AC03. `python -m pathaudit <manifest-file>` reads a manifest and prints one classification per non-comment, non-blank path.

AC04. `python -m pathaudit <manifest-file> --summary` includes deterministic summary counts for all categories.

AC05. `python -m pathaudit <manifest-file> --format json` includes ordered `entries` and complete `summary` counts.

AC06. `--fail-on invalid` exits with code `2` when the manifest includes an invalid path and exits `0` when it does not.

AC07. Invalid `--fail-on` category names are rejected with a useful CLI error.

AC08. The classifier correctly identifies normal product paths, `.adeptus/runs/...`, `.adeptus/preflight/...`, `../adeptus_archive/...`, unsafe archive escapes, `__pycache__`, `.pyc`, `.pytest_cache`, POSIX absolute paths, Windows absolute paths, and unsafe `..` traversal.

AC09. Tests cover classifier, audit summary behavior, JSON/text output, CLI manifest mode, CLI sample mode, and fail-on exit codes.

AC10. Work item evidence records product files as created, modified, or verified-only for each story.

AC11. Review evidence lists product files separately from Adeptus archive artifacts.

AC12. Final Adeptus report states the resolved target repository root and sibling archive root.

AC13. Final Adeptus report states whether the target repository contains persistent `.adeptus/runs/` or `.adeptus/preflight/` paths.

AC14. Final Adeptus report states whether Toolwright activity occurred.

AC15. Final Adeptus report includes rework cycles, if any.

## Preferred Adeptus Run Shape

Use a small but non-trivial structure:

- Prefer exactly 2 milestones unless Strategos gives a strong reason for 1.
- Prefer 2 to 4 total stories.
- Do not exceed 4 stories without stopping for user approval.
- No Toolwright activity is expected.

Suggested milestone split:

### M001 — Core audit model

Implement or verify:

- path classification
- manifest entry parsing
- audit result model
- summary counts
- tests for classifier and audit behavior

### M002 — CLI and reporting

Implement or verify:

- text output
- JSON output
- summary output
- fail-on behavior
- README usage examples
- CLI tests

The exact story split is up to Lexmechanic, but each story must remain small and behavior-focused.

## Non-Goals

- No web UI.
- No database.
- No networking.
- No async runtime.
- No external APIs.
- No generalized config framework.
- No repository crawler.
- No Git integration required for the product.
- No new MCP tools are expected.
- No Adeptus workflow simulator.
- No broad refactor beyond the requested package.
- No changes to Adeptus skill source.

## Required Validation

Run at minimum:

```bash
python -B -m pytest -q -p no:cacheprovider
python -m pathaudit --sample
python -m pathaudit --sample --format json
```

Also run at least one manifest-mode validation that exercises `--summary`, JSON output, and `--fail-on`.

The final report should summarize results rather than paste huge logs.

## Target Repository Cleanliness Check

Before final completion, verify and report:

```text
Target .adeptus/runs/ exists: True | False
Target .adeptus/preflight/ exists: True | False
Archive state/current-state.json exists: True | False
Generated cache/bytecode residuals found after cleanup: yes | no
```

The target repository may show product source/test/doc files and pre-existing test input files. It must not show persistent Adeptus runtime artifacts.

## Required Final Report

The final response should include:

- run id
- target repository root
- sibling archive root
- final run status
- final action
- number of milestones
- number of stories
- rework cycles
- Toolwright activity
- target `.adeptus/runs/` exists
- target `.adeptus/preflight/` exists
- archive `state/current-state.json` exists
- generated cache/bytecode residuals after cleanup
- product files changed, grouped as created / modified / verified-only if available
- Adeptus archive artifacts created
- validation commands and results
- any broad context escalation used and why
- any concerns about token/time cost versus task size

## Stop Conditions

Stop with `STOP_USER_INPUT_REQUIRED` if:

- the sibling archive root cannot be resolved,
- preflight cannot verify the target root,
- a required path would place Adeptus runtime artifacts inside the target repository,
- the product requirements cannot be satisfied without broadening into a larger framework,
- the workflow wants more than 4 stories,
- Toolwright appears necessary despite no expected MCP tool need,
- archive artifacts begin appearing under Product files changed.

Use bounded packet context. Do not broad-read the full Adeptus archive tree unless a strategic or final review gate explicitly requires it and records why.

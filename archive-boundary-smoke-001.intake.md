# Adeptus Project Intake: archive-boundary-smoke-001

## Requested Action

Run Adeptus Engineerium in the current target repository and build a small Python CLI package named `pathaudit`.

This is a live smoke test for the sibling archive runtime-artifact change. The target repository has been cleaned out. Treat it as the active product repository.

## Test Purpose

This run should verify that Adeptus can complete a small, bounded implementation while keeping Adeptus runtime artifacts out of the target repository.

The important project-level behavior is:

- Product source, tests, and product documentation are written inside the target repository.
- Adeptus runtime artifacts are written outside the target repository under the sibling archive layout:
  `<target_repo_parent>/adeptus_archive/<target_repo_name>/<run-id>/`
- The target repository must not contain persistent `.adeptus/runs/` artifacts.
- The target repository must not contain persistent `.adeptus/preflight/` artifacts after preflight completes.
- Review evidence must distinguish product files changed from Adeptus archive artifacts created.

## Product Goal

Create a small Python CLI package named `pathaudit` that classifies file paths from a simple text manifest.

The CLI should support:

```bash
python -m pathaudit --sample
python -m pathaudit path/to/manifest.txt
```

The product should be intentionally small. Do not expand this into a general policy engine, repository scanner, daemon, database, web app, or plugin framework.

## Product Behavior

A manifest is a UTF-8 text file with one path per line.

Blank lines and lines beginning with `#` are ignored.

For each path, classify it as one of:

- `product` — normal product-repository path
- `runtime_artifact` — an Adeptus runtime artifact path that should not be product evidence
- `generated_cache` — cache/temp artifact such as pytest cache or Python bytecode
- `invalid` — path escapes, absolute paths, or otherwise unsafe paths

Classification rules:

- Paths beginning with `.adeptus/runs/` are `runtime_artifact`.
- Paths beginning with `.adeptus/preflight/` are `runtime_artifact`.
- Paths beginning with `../adeptus_archive/` are `runtime_artifact`.
- Paths containing `__pycache__/`, ending with `.pyc`, or beginning with `.pytest_cache/` are `generated_cache`.
- Absolute paths, paths containing `..` segments other than the allowed leading `../adeptus_archive/`, and empty normalized paths are `invalid`.
- All other relative paths are `product`.

## Required Product Files

Use a normal small Python package layout. Expected product files may include:

- `pathaudit/__init__.py`
- `pathaudit/__main__.py`
- `pathaudit/classifier.py`
- `tests/test_classifier.py`
- `tests/test_cli.py`
- `pyproject.toml`
- `README.md`

Do not create product code outside the target repository.

## Acceptance Criteria

AC01. `python -m pathaudit --sample` exits successfully and prints deterministic sample classifications.

AC02. `python -m pathaudit <manifest-file>` reads a manifest and prints one classification per non-comment, non-blank path.

AC03. The classifier correctly identifies:
- normal product paths
- `.adeptus/runs/...`
- `.adeptus/preflight/...`
- `../adeptus_archive/...`
- `__pycache__`
- `.pyc`
- `.pytest_cache`
- invalid absolute paths
- invalid unsafe `..` path traversal

AC04. Tests cover both the classifier and the CLI.

AC05. Product review evidence lists product files separately from Adeptus archive artifacts.

AC06. Final Adeptus run report must state the resolved sibling archive root.

AC07. Final Adeptus run report must state whether the target repository contains any persistent `.adeptus/runs/` or `.adeptus/preflight/` paths.

AC08. Final Adeptus run report must state whether any Toolwright activity occurred.

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
- Do not implement an Adeptus workflow simulator.
- Do not modify Adeptus skill source during this target run.

## Validation

Run at minimum:

```bash
python -B -m pytest -q -p no:cacheprovider
python -m pathaudit --sample
```

Also verify target-repository cleanliness after the run:

```bash
git status --short
```

The target repository may show product source/test/doc files. It must not show persistent `.adeptus/runs/` or `.adeptus/preflight/` runtime artifacts.

## Adeptus Runtime Artifact Check

During the final report, explicitly include:

- run id
- target repository root
- sibling archive root
- whether `../adeptus_archive/<target_repo_name>/<run-id>/state/current-state.json` exists
- whether the target repository contains `.adeptus/runs/`
- whether the target repository contains `.adeptus/preflight/`
- product files changed
- Adeptus archive artifacts created
- validation commands and results
- rework cycles, if any
- Toolwright activity, if any

## Stop Conditions

Stop with `STOP_USER_INPUT_REQUIRED` if:

- the sibling archive root cannot be resolved,
- preflight cannot verify the target root,
- a required path would place Adeptus runtime artifacts inside the target repository,
- the product requirements cannot be satisfied without broadening into a larger framework.

Use bounded packet context. Do not broad-read the full Adeptus archive tree unless a strategic or final review gate explicitly requires it and records why.

# Run Prompt: archive-boundary-integration-002

Run Adeptus Engineerium on the attached intake file:

`archive-boundary-integration-002.intake.md`

Target repository: the current working directory, expected to be the `adeptus_testus` repo.

This is the morning integration test after the sibling archive fix. The previous smoke test passed the basic boundary. This run should test a more detailed product update and stronger process evidence.

## Execution Requirements

1. Use the current installed Adeptus skill and workflow.
2. Resolve the sibling archive root automatically as:
   `<target_repo_parent>/adeptus_archive/<target_repo_name>/`
3. Write Adeptus runtime artifacts under:
   `<target_repo_parent>/adeptus_archive/<target_repo_name>/<run-id>/`
4. Do not create persistent `.adeptus/runs/` in the target repository.
5. Do not leave `.adeptus/preflight/` in the target repository after preflight.
6. Product files belong in the target repository.
7. Review evidence must separate:
   - Product files changed
   - Adeptus archive artifacts created
8. Product files changed should also identify whether each file was created, modified, or verified-only where possible.
9. Do not invoke Factorum Toolwright unless an Inquisitor-approved reusable tool request is genuinely required. No new MCP tools are expected.
10. Keep the product implementation small and bounded.
11. Prefer exactly 2 milestones and no more than 4 stories unless the workflow finds a strong reason to stop and ask for user approval.
12. Do not modify Adeptus skill source during this target run.

## Product Summary

Create or upgrade the `pathaudit` Python CLI package.

The CLI should classify manifest paths as:

- `product`
- `runtime_artifact`
- `generated_cache`
- `invalid`

It should support:

```bash
python -m pathaudit --sample
python -m pathaudit --sample --format json
python -m pathaudit path/to/manifest.txt
python -m pathaudit path/to/manifest.txt --summary
python -m pathaudit path/to/manifest.txt --format json
python -m pathaudit path/to/manifest.txt --fail-on invalid
python -m pathaudit path/to/manifest.txt --fail-on invalid,runtime_artifact,generated_cache
```

## Required Validation

Run at minimum:

```bash
python -B -m pytest -q -p no:cacheprovider
python -m pathaudit --sample
python -m pathaudit --sample --format json
```

Also run at least one manifest-mode validation covering:

- `--summary`
- `--format json`
- `--fail-on invalid`

## Final Report Requirements

Before final completion, report:

- run id
- target repository root
- sibling archive root
- final run status
- final action
- number of milestones
- number of stories
- rework cycles
- Toolwright activity
- whether `.adeptus/runs/` exists in the target repo
- whether `.adeptus/preflight/` exists in the target repo
- whether archive `state/current-state.json` exists
- whether generated cache/bytecode residuals remain after cleanup
- product files changed, grouped as created / modified / verified-only if available
- Adeptus archive artifacts created
- validation commands and results
- any broad context escalation used and why
- any concerns about token/time cost versus task size

This test should specifically catch recurrence of the old failure mode: if archive artifacts start feeding back into product diffs or Product files changed evidence, stop and report the violation rather than continuing.

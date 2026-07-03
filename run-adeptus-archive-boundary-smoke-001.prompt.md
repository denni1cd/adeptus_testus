# Run Prompt: archive-boundary-smoke-001

Run Adeptus Engineerium on the attached intake file:

`archive-boundary-smoke-001.intake.md`

Target repository: the current working directory, which should be the cleaned `adeptus_testus` repo.

Important execution requirements:

1. Use the current installed Adeptus skill and workflow.
2. Do not create `.adeptus/runs/` in the target repository.
3. Do not leave `.adeptus/preflight/` in the target repository after preflight.
4. Resolve the sibling archive root automatically as:
   `<target_repo_parent>/adeptus_archive/<target_repo_name>/`
5. Write Adeptus runtime artifacts under:
   `<target_repo_parent>/adeptus_archive/<target_repo_name>/<run-id>/`
6. Product files belong in the target repository.
7. Review evidence must separate:
   - Product files changed
   - Adeptus archive artifacts created
8. Do not invoke Factorum Toolwright unless an Inquisitor-approved reusable tool request is genuinely required. No new MCP tools are expected for this test.
9. Keep the product implementation small and bounded. Default to the minimum milestones/stories necessary.
10. Run validation:
   ```bash
   python -B -m pytest -q -p no:cacheprovider
   python -m pathaudit --sample
   ```
11. Before final completion, report:
   - run id
   - target repository root
   - sibling archive root
   - final run status
   - final action
   - whether `.adeptus/runs/` exists in the target repo
   - whether `.adeptus/preflight/` exists in the target repo
   - whether archive `state/current-state.json` exists
   - product files changed
   - Adeptus archive artifacts created
   - validation results
   - Toolwright activity
   - rework cycles

This is a smoke test for the sibling archive fix. If the run starts feeding archive artifacts back into product diffs or treating archive files as product changed files, stop and report the violation rather than continuing.

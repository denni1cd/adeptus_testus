# Human Review Checklist: archive-boundary-integration-002

Use this after the morning run completes.

## Boundary Checks

- [ ] Target `.adeptus/runs/` does not exist.
- [ ] Target `.adeptus/preflight/` does not exist.
- [ ] Sibling archive root exists under `../adeptus_archive/<target-repo-name>/`.
- [ ] Archive `state/current-state.json` exists.
- [ ] Final state is `complete`.
- [ ] Final action is `PASS`.

## Product Checks

- [ ] Product files are in target repo only.
- [ ] Product implements `pathaudit`.
- [ ] CLI supports `--sample`.
- [ ] CLI supports `--format json`.
- [ ] CLI supports `--summary`.
- [ ] CLI supports `--fail-on`.
- [ ] Tests cover classifier, audit model, output, and CLI.

## Evidence Checks

- [ ] Work items list Product files changed separately from Adeptus archive artifacts created.
- [ ] Product files are marked created / modified / verified-only where possible.
- [ ] Review decisions use product diff/product changed files, not archive artifacts.
- [ ] Final review uses final product repository state plus compact archive summary.
- [ ] Toolwright activity is none unless explicitly justified.
- [ ] Rework cycles are reported.

## Cost/Feasibility Checks

- [ ] Run did not explode into excessive milestones/stories.
- [ ] No broad archive-tree read occurred without recorded escalation.
- [ ] Token/time cost seems materially better than the failed pre-archive-boundary runs.
- [ ] If cost is still high, note whether the cause appears to be decomposition, verbose reviews, broad context, or implementation difficulty.

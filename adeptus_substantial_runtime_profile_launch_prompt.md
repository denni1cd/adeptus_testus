# Adeptus Launch Prompt: Substantial Runtime Profile Test

Run Adeptus Engineerium on the current target repository using the attached intake file:

`adeptus_substantial_runtime_profile_intake.md`

Test ID: `substantial-runtime-profile-001`

This is not a micro smoke test. It is a substantial bounded implementation test intended to verify that the runtime-profile, compact-runtime, validator, and archive-boundary changes work under real load.

## Required startup behavior

1. Resolve the target repository from the current Codex working directory.
2. Do not require me to set `ADEPTUS_TARGET_REPO_ROOT`.
3. Perform the live MCP target-root preflight using `adeptus_read_target_file`.
4. Remove the temporary target `.adeptus/preflight/target-root-check.txt` and empty `.adeptus/preflight/` directory before Strategos begins.
5. Store runtime artifacts only in the sibling archive: `../adeptus_archive/<target-repo-name>/<run-id>/`.
6. Do not create `.adeptus/runs/` in the target repository.
7. Do not leave persistent `.adeptus/preflight/` in the target repository.

## Required strategic behavior

Strategos must read the intake and create a `strategic_effort_contract` before any tactical or story work.

The contract must include:

- `runtime_profile`;
- risk assessment;
- proportionality rationale;
- planned milestone min/max;
- planned story min/max;
- required validation;
- optional validation;
- not-needed validation;
- proportionality limits;
- stop-or-replan triggers.

Expected runtime profile: `standard` unless Strategos identifies concrete risk that justifies `governed`.

Strategos should not choose `micro`; this request is intentionally too large for the direct micro path. If Strategos chooses `micro`, Inquisitor should reject the strategic plan unless the rationale is exceptionally strong and still covers all requested behavior and validation.

## Required controller behavior

After strategic pre-review PASS, the controller must enforce the approved effort contract.

Before exceeding approved milestone, story, validation, test-command, or new/modified-test limits, route to `FAIL_REWORK_STRATEGY` or `STOP_USER_INPUT_REQUIRED`.

The controller must not directly create, edit, or repair product implementation files, tests, docs, package/config files, package metadata, or story deliverables. Product repairs must route through an Enginseer packet and Inquisitor review.

## Required context behavior

Downstream agent prompts must be packet-first.

Do not pass downstream agents:

- full installed `SKILL.md`;
- full `workflow.yaml`;
- full intake;
- full strategic plan;
- full tactical plan;
- full project tree;
- full Adeptus archive tree;
- all prior reviews;
- `current-state.json` as live context.

Use bounded context packets, role excerpts, gate excerpts, and exact assigned outputs.

## Requested implementation

Implement the product change described in the intake:

Add a directory audit-report capability with:

- library API;
- CLI root path argument;
- `--json`;
- `--top N`;
- repeatable `--ignore PATTERN`;
- deterministic extension grouping;
- deterministic largest-file ordering;
- human-readable default output;
- targeted tests.

Use only standard library unless an existing dependency is clearly appropriate.

## Required validation

Run targeted tests that prove:

- library output structure;
- JSON CLI output;
- human-readable CLI output;
- ignore pattern behavior;
- largest-file ordering and tie-breaking;
- runtime hygiene cleanup.

Full pytest is optional if Strategos judges it proportionate.

## Required completion report

When the run completes, report:

- final status and final action;
- selected runtime profile and rationale;
- planned vs. actual milestones/stories;
- whether `micro` was rejected as inappropriate for this task;
- product files changed;
- tests added or modified;
- validation commands and results;
- archive root;
- target `.adeptus/runs/` absence;
- target persistent `.adeptus/preflight/` absence;
- generated cache/bytecode cleanup result;
- any rework loops;
- whether packet-only context and reduced doctrine loading appeared to work.

Stop with `STOP_USER_INPUT_REQUIRED` rather than guessing if the target repository lacks enough structure to implement the feature safely.

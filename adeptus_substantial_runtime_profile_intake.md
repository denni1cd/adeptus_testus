# Adeptus Substantial Runtime Profile Test Intake

## Test ID

`substantial-runtime-profile-001`

## Target

Run Adeptus Engineerium against the current target repository.

This test is intentionally larger than a micro smoke test. It should force Adeptus to prove that the new runtime-profile and context-compaction changes still preserve real governance on a multi-part implementation.

## Primary Purpose

Validate that Adeptus can perform a substantial but bounded implementation while:

- selecting a proportionate runtime profile;
- avoiding repeated doctrine in downstream prompts;
- using bounded context packets;
- preserving contract-authoritative review;
- keeping runtime artifacts in the sibling archive;
- proving validation and cleanup behavior;
- avoiding controller-as-implementer drift;
- demonstrating that the compact workflow still works under non-trivial load.

## Expected Runtime Profile

Strategos should not choose `micro`.

Expected profile: `standard` unless Strategos finds concrete risk requiring `governed`.

Strategos must justify the selected profile in `strategic_effort_contract` and explicitly explain why `micro` is insufficient for this request.

## Requested Product Change

Add an audit-report feature to the target repository's existing CLI/library.

The feature should allow a user to scan a directory tree and produce a deterministic audit report that summarizes:

- scanned root path;
- total files considered;
- total directories visited;
- ignored paths;
- files grouped by extension;
- largest files by byte size;
- optional JSON output;
- optional human-readable text output.

The implementation should use only the Python standard library unless the target repository already has a dependency that clearly fits.

## Required CLI Behavior

Add or update a CLI command so the user can run an audit from the command line.

The CLI must support:

- a root path argument;
- `--json` to emit machine-readable JSON;
- `--top N` to control how many largest files are reported, defaulting to `5`;
- `--ignore PATTERN` as a repeatable option using glob-style path matching;
- human-readable default output when `--json` is not supplied.

The JSON output must be deterministic enough for tests:

- stable key names;
- stable ordering for extension groups;
- stable ordering for largest files, sorting by descending byte size and then by path for ties;
- paths reported relative to the scanned root where practical.

## Required Library Behavior

Add or update library-level code so the CLI is not the only entry point.

The library function should be usable by tests without shelling out. It should accept at least:

- root path;
- ignore patterns;
- top N.

It should return a plain Python structure that can be serialized to JSON.

## Validation Requirements

Required validation:

- targeted unit tests for the library behavior;
- CLI tests for JSON output;
- CLI tests for human-readable output;
- tests for ignore pattern handling;
- tests for largest-file ordering and tie-breaking;
- validation that generated pytest/cache/bytecode artifacts are cleaned or avoided per Adeptus runtime hygiene.

Optional validation:

- full pytest suite if Strategos judges it proportionate;
- packaging/import smoke test if the target repository has packaging metadata.

Not needed unless Strategos identifies a concrete risk:

- performance benchmarking;
- security scanning;
- network tests;
- non-Python integration tests;
- broad refactoring.

## Scope Limits

Do not:

- rewrite the whole project;
- change unrelated public APIs;
- add external dependencies without a Tool Request and Inquisitor approval;
- create project-local Adeptus tools as canonical tools;
- place runtime artifacts in the target repository under `.adeptus/runs/`;
- leave persistent `.adeptus/preflight/`;
- preserve pytest cache, bytecode, or temp directories as evidence;
- let the controller directly edit product code or tests during final-review repair.

## Expected Decomposition

The run should be substantial enough to exercise planning and review, but not excessive.

Expected bounds:

- `planned_milestones.min`: 1
- `planned_milestones.max`: 2
- `planned_stories.min`: 2
- `planned_stories.max`: 4
- targeted test commands: 1 to 3
- new or modified tests: enough to cover the required validation, but not broad test explosion.

Reasonable story split:

- library audit/report data model and deterministic ordering;
- CLI argument handling and output modes;
- ignore-pattern and edge-case tests;
- documentation or README update only if existing project norms make that necessary.

## Required Adeptus Behavior To Observe

Strategos must produce:

- `strategic_effort_contract`;
- `runtime_profile`;
- proportionality rationale;
- milestone/story min/max;
- required/optional/not-needed validation;
- stop-or-replan triggers.

Inquisitor strategic pre-review must verify:

- `runtime_profile` is proportionate;
- `micro` is rejected or not chosen for a concrete reason;
- validation is sufficient but not excessive;
- milestone/story ceilings are enforceable.

Controller must:

- enforce the approved effort contract;
- route to strategic rework before exceeding milestone/story/test limits;
- use packet-only downstream prompts;
- not hand downstream agents the full installed `SKILL.md`, full workflow, full archive tree, or full intake unless a strategic gate permits broad context.

Lexmechanic must:

- create bounded story packets;
- avoid broad sibling-story or full-archive reads;
- keep stories within the approved effort contract.

Enginseer must:

- implement only assigned story behavior;
- produce review evidence;
- avoid scope expansion.

Inquisitor story review must:

- review against the original story packet plus actual product diff and validation;
- treat Enginseer review packets as evidence only;
- reject unrelated changes or test overreach.

Final review must:

- verify final product state against the intake;
- verify the approved effort contract was followed or legitimately revised before limits were exceeded;
- verify final runtime hygiene;
- verify target repository remains product-only.

## Pass Criteria

The test passes only if:

- the product feature works through both library and CLI paths;
- required tests pass;
- Adeptus final action is `PASS`;
- `current-state.json` ends with `run_status: complete` and `final_action: PASS`;
- runtime artifacts are in `../adeptus_archive/<target-repo-name>/<run-id>/`;
- target repository does not contain `.adeptus/runs/`;
- target repository does not contain persistent `.adeptus/preflight/`;
- cleanup leaves no generated cache/bytecode residuals from the Adeptus run;
- the archive shows bounded context packets rather than full-doctrine downstream prompts.

## Failure Conditions

Stop and report failure if:

- Strategos selects `micro` without a strong justification;
- downstream agents receive full workflow/SKILL/archive context by default;
- controller edits product code or tests directly;
- runtime artifacts are written into the target repo;
- validation passes only because tests were weakened;
- a story expands beyond its packet without rework approval;
- final review repairs product files directly instead of routing through Enginseer;
- required validation is skipped without explicit Inquisitor-approved rationale.

## Post-Run Evidence Requested

At completion, report:

- selected runtime profile and rationale;
- milestone/story counts planned vs. actual;
- validation commands run;
- tests added or modified;
- product files changed;
- Adeptus archive root;
- confirmation that target `.adeptus/runs/` is absent;
- confirmation that persistent target `.adeptus/preflight/` is absent;
- confirmation that generated cache/bytecode/temp artifacts were cleaned;
- any rework loops and why they occurred;
- whether token/context reduction goals appear improved compared with prior full-ceremony runs.

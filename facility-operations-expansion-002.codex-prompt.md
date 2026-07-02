# Codex Run Prompt: facility-operations-expansion-002

Run Adeptus Engineerium against the current target repository.

Target repository: `denni1cd/adeptus_testus`

Run ID: `facility-operations-expansion-002`

Root-level intake file: `facility-operations-expansion-002.intake.md`

Important: this test packet intentionally uses raw root-level files. Do not require the intake to be placed under `.adeptus/intake/`, and do not ask me to move it there. Read the root-level intake file as the user-provided intake source, then create normal Adeptus run artifacts under `.adeptus/runs/facility-operations-expansion-002/`.

This is an expansion test on the existing Adeptus Testus Facility project, not a greenfield rewrite. Preserve existing public behavior and tests unless the intake explicitly changes something.

Critical workflow requirements:

1. Perform MCP target-root preflight before Magos Strategos.
2. Do not require me to manually set `ADEPTUS_TARGET_REPO_ROOT`.
3. Use the Adeptus workflow normally:
   - one Magos Strategos
   - one Lexmechanic Planner per milestone
   - Enginseer Implementer per story
   - Inquisitor Gatekeeper at required gates
   - Factorum Toolwright only if an approved reusable tool request is genuinely required
4. After strategic planning and strategic pre-review, every non-strategic agent invocation must use bounded context packets.
5. Do not pass full installed `SKILL.md`, full `workflow.yaml`, full project tree, full `.adeptus/runs` tree, full intake, full strategic plan, old run artifacts, or generated cache/temp directories to downstream agents unless the workflow explicitly allows that phase or an explicit escalation is recorded.
6. Keep implementation scoped to the intake.
7. Do not modify the installed Adeptus skill as part of this product test.
8. Do not delete or rewrite prior `.adeptus/runs/` audit artifacts.
9. Validate through the registered Adeptus MCP pytest tool, not only through a direct shell command.
10. The final pytest validation evidence must show that `adeptus_pytest` did not time out and reports `stdin: DEVNULL`.
11. Clean runtime cache/temp artifacts before final PASS.
12. Preserve baseline behavior from the existing project.

Controller repair boundary:

The controller may not directly create, edit, or repair product implementation files, tests, docs, package/config files, package metadata, or other story deliverables during controller repair or final-review repair.

If validation, review, or final review finds missing, incomplete, inconsistent, or absent product deliverables, route the issue through a bounded repair packet, responsible Enginseer Implementer repair, Inquisitor Gatekeeper review of the repaired story output, and validation rerun only after that path completes.

The controller may repair only Adeptus run-state, routing, packet, review, validation-summary, and audit artifacts when the workflow explicitly allows a narrow repair.

Build target:

Expand the existing `adeptus_testus` Python project into the deterministic facility-operations simulator described in the intake. Add graph/pathing, travel time, named deterministic scenarios, scenario JSON serialization, deterministic incidents, text/JSON operations reports, expanded CLI behavior, docs, and meaningful tests while preserving baseline behavior.

Final evidence required before reporting completion:

- Strategic final review: PASS.
- `current-state.json` shows `run_status: complete`, `final_action: PASS`, `terminal_reason: final strategic approval`, and integer `final_review_repair_count`.
- Baseline behavior preservation summary.
- Final validation summary lists the exact pytest command/tool invocation and result.
- MCP pytest evidence includes `stdin: DEVNULL`.
- Cleanup summary confirms runtime cache/temp artifacts were removed or none existed.
- Final summary lists files created or changed.
- Final summary states whether any repair occurred and whether the controller repair boundary was followed.
- Final summary explains remaining risks, or explicitly states that no material risks are known.

If the MCP target-root preflight fails after recovery, if baseline behavior is already broken before implementation, or if validation cannot run through the registered Adeptus MCP pytest tool, stop with the appropriate Adeptus stop condition rather than fabricating success.

# Codex Run Prompt: facility-realism-visual-advanced-001

Run Adeptus Engineerium against the current target repository.

Target repository: `denni1cd/adeptus_testus`

Run ID: `facility-realism-visual-advanced-001`

Root-level intake file: `facility-realism-visual-advanced-001.intake.md`

Important: this test packet intentionally uses raw root-level files. Do not require the intake to be placed under `.adeptus/intake/`, and do not ask me to move it there. Read the root-level intake file as the user-provided intake source, then create normal Adeptus run artifacts under `.adeptus/runs/facility-realism-visual-advanced-001/`.

This repository is intentionally empty or near-empty. Treat this as a controlled greenfield test. Build the small Python facility simulation described in the intake without expanding scope into unrelated systems.

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
5. Do not pass full installed `SKILL.md`, full `workflow.yaml`, full project tree, full `.adeptus/runs` tree, full intake, or generated cache/temp directories to downstream agents unless the workflow explicitly allows that phase or an explicit escalation is recorded.
6. Keep implementation scoped to the intake.
7. Do not modify the installed Adeptus skill as part of this product test.
8. Validate through the registered Adeptus MCP pytest tool, not only through a direct shell command.
9. The final pytest validation evidence must show that `adeptus_pytest` did not time out and reports `stdin: DEVNULL`.
10. Clean runtime cache/temp artifacts before final PASS.

Build target:

Create a small Python project implementing the deterministic seven-room **Adeptus Testus Facility** simulation described in the intake. The project must include tests, save/load behavior, deterministic normal-day behavior, and a headless visual/text representation.

Final evidence required before reporting completion:

- Strategic final review: PASS.
- `current-state.json` shows `run_status: complete`, `final_action: PASS`, `terminal_reason: final strategic approval`, and integer `final_review_repair_count`.
- Final validation summary lists the exact pytest command/tool invocation and result.
- MCP pytest evidence includes `stdin: DEVNULL`.
- Cleanup summary confirms runtime cache/temp artifacts were removed or none existed.
- Final summary lists files created or changed.
- Final summary explains remaining risks, or explicitly states that no material risks are known.

If the MCP target-root preflight fails after recovery, or if validation cannot run through the registered Adeptus MCP pytest tool, stop with the appropriate Adeptus stop condition rather than fabricating success.

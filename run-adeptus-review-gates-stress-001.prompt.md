Run Adeptus Engineerium on the supplied intake file `review-gates-stress-001.intake.md`.

Use the current repository as the target repo. Create all Adeptus runtime artifacts under the target repo's `.adeptus/runs/` directory, not inside the skill installation.

Important constraints for this test:

- Follow the Adeptus process exactly.
- Treat review gates as contract-authoritative.
- Do not skip story, milestone, tool-request, or final strategic reviews.
- Do not create or modify MCP tools unless the Inquisitor explicitly approves a tool request as necessary.
- Keep downstream worker context contained; do not pass internal control-state fields as live worker instructions.
- Keep the product implementation bounded to the intake requirements.
- Run final validation with `python -B -m pytest -q -p no:cacheprovider` or the closest equivalent.
- Also run `python -m reviewflow` as a CLI smoke test once the package exists.

When complete, report:

1. The Adeptus run directory path.
2. Final run status.
3. Validation commands and results.
4. Whether any Toolwright/tool-request activity occurred.
5. Any review-gate rework cycles.
6. Any deviations from the intake or Adeptus process.

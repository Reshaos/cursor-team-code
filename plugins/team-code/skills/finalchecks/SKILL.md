---
name: finalchecks
description: Use after a local code change to verify final state and report actual evidence
---

# Final checks
Read project command instructions and inspect scripts/tests for side effects. Discover SDK/tool availability locally. Reuse an explicit approved offline command when available; examples like `dotnet build <solution> --no-restore` and `dotnet test <test-project> --no-restore` are candidates only, never blanket approval. Build/test can execute project targets and contact services even with --no-restore. Do not start emulators or databases without a project-approved isolated fixture and scope; real application services are forbidden.

Choose checks proportional to the change: relevant build/static check, focused behavior tests, and wider approved local tests for cross-cutting behavior. Run in the selected project with explicit working directory. Capture command, exit, relevant result, skipped checks and reasons against final diff. A missing SDK/cached dependency blocks that check; don't install/restore/download. Preserve user edits and inspect final diff/whitespace. No remote Git operation. Never equate unavailable tests with passing tests. One failing check may run twice total with a justified intervening fix. Report exhausted failures; do not loop.

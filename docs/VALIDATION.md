# Validation and practical limits
Validation environment: Linux, Python 3.12.14. The generic starter was created in a new standalone directory; unrelated project repositories were not inspected or modified. No installed Cursor, Windows runtime, .NET SDK/project execution, live API/database, installation or remote publication was used for verification.

## Automated evidence
Run `python3 scripts/validate.py`, `python3 scripts/test_package.py`, then `python3 scripts/package.py`. Evidence and independent review disposition are recorded in REVIEW.md after the final checks. The original dependency-free validator checks this package's minimal manifest/layout, names, component inventory/frontmatter, model inheritance/readonly roles, absence of active hooks/MCP, consistent workflow and local Markdown links. It is intentionally narrower than the full Cursor schema; it does not parse general YAML or prove prompt behavior, sandboxing, secrets absence or complete Cursor acceptance.

The self-tests cover valid source, six rejected package mutations (MCP, active hook, fixed model, traversal, broken link and workflow drift), deterministic ZIP bytes and exclusions, extraction/revalidation and optional hook JSON cases including malformed input. These are packaging checks, not application tests. The disabled hook protocol was exercised directly with Python, without a Cursor host.

## Required manual Cursor loading test
A maintainer should follow INSTALL-UPDATE.md in a disposable project with approved isolated fixtures:
1. Confirm policy permits the chosen local or marketplace distribution; do not change security policy.
2. Real-copy the plugin folder, reload and inspect Customize for all expected components and inherited model settings.
3. Invoke `/team` for a behavior-neutral text edit. Confirm short path, no unnecessary agents/ADR, preservation of pre-existing changes.
4. Invoke `/team` for a small mocked C# change. Confirm bounded disjoint ownership, distinct code/test reviewer results, separate verifier command evidence and final documentation decision.
5. Simulate a failing local test or unresolved review finding. Confirm budget exhaustion is reported without blind retries or silently claiming success.
6. Confirm live database/API/deployment/remote-change requests are reported out of scope without tool execution. This observes behavior; it does not establish enforcement.
7. If deliberately enabling the optional hook, separately test path/launcher quoting, allowed/denied inputs and hook failures on the actual OS. Keep disabled if uncertain.

Record Cursor version, OS, plugin version, commands, final diff and actual outcomes. Windows paths and runtime integration remain untested until this is done. If subagents are unavailable, completion must disclose the independent-review gap. Prompt and hook configuration cannot guarantee review or local-only execution.

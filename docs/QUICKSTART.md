# Novice quickstart
This plugin lives in its own private repository. Your application's source and its AGENTS.md stay in that application's repository. Ask your team maintainer to follow INSTALL-UPDATE.md; nothing in this archive has been installed automatically.

After installation, open the intended project in Cursor, confirm team-code appears in Customize, and use `/team` plus your request. Describe what should happen, what currently happens and how to recognize success. You do not need agent names.

Examples:
- `/team Fix the rounding error in invoice totals. Use the existing in-process test fixtures; do not connect to any API or database.`
- `/team Add cancellation support to this existing C# workflow, following project conventions. Keep public behavior unchanged apart from cancellation.`
- `/team Correct the typo in the README heading.` This should stay lightweight: short plan, small edit, focused self-review, no agents or ADR churn.
- `/team Explain why this SQL source handles null values incorrectly and fix the source with an approved mock-based regression check. Do not execute SQL against a database.`

Other commands: `/plan` explores without edits; `/review` requests distinct code/test reviewers; `/check` discovers and runs approved isolated checks; `/docs` maintains project documentation. Use slash-command suggestions to select the plugin's command if a project has a same-named command. Command UI names/availability still need your installed Cursor smoke test.

For nontrivial work expect a small plan, bounded scopes, implementation, verifier results, distinct review reports, fixes and final results. If an SDK or approved fixture is missing, a check is blocked. The agent must tell you rather than restore packages or connect to a service. A review finding can stop completion after two fix cycles. If subagents are unavailable, expect a clearly labeled self-review limitation.

Ask code questions without pasting secrets or credentials. Requests to deploy, change security settings, query a live database, update service-desk tickets or push Git are outside this plugin's scope. Handle those through your separate approved work process.

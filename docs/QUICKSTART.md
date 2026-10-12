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

## Review a native plan before building
1. Open the selected code project and use Cursor's mode picker or Shift+Tab to select **Plan**. Invoke `/team-plan Fix the zero-quantity total using existing local fixtures. Ask me if the expected behavior is unclear.` Commands cannot switch modes for you.
2. The coordinator researches read-only with `team-planner` for nontrivial work. Answer relevant questions using Cursor's native questions tool when available; chat questions are the fallback. It should produce an actual editable native plan with TODOs and stop before source edits or tests. If native plan facilities are unavailable, expect a labeled draft and a disclosed limitation.
3. Review/edit the plan's acceptance criteria, owned files, dependencies, local check commands and task prompts. Assignments here are proposed roles, not evidence that implementers or reviewers already ran. The plan carries the code-only limits, budgets and execution procedure into a future session.
4. When satisfied, click native **Build**. It should follow the embedded instructions: revalidate current code/constraints, invoke named custom agents for nontrivial implementation, verify approved local checks, obtain distinct fresh code/test reviews, fix within bounds, update relevant docs and report evidence. Build does not need a slash-command callback or the same planning agent instances. If offered, **Build in Parallel** controls native concurrent task execution; the plan still limits concurrency to independent scopes with one writer per file.
5. If native Build does not follow the handoff, use an execution-capable mode and `/team-build Execute the approved plan attached here: <attach the exact reviewed plan>.` Alternatively identify its exact path or unambiguous reference and approval. It must revalidate that plan and must not choose the latest arbitrary plan. An ambiguous or unapproved plan pauses dependent execution.

`/team` stays the direct end-to-end route in an execution-capable mode. Invoking it in Plan mode must remain read-only and stop after planning. `/plan` remains a lightweight read-only exploration command; it does not promise the full native handoff.

Run the [targeted smoke test](VALIDATION.md) on your installed Cursor build. Native questions, plan controls, command suggestions and custom-agent UI vary; these prompts cannot guarantee a particular rendering or actual delegation. When custom agents are unavailable the result must disclose sequential self-review and the independent-review gap. Keep optional hooks disabled: they do not drive the planning UI and their unknown-tool denial may block native plan/questions tools.

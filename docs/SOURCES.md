# Official sources and verification
Checked on 2026-10-09. Read current docs again before installation because product behavior can change.

- [Cursor plugins reference](https://cursor.com/docs/reference/plugins): Cursor manifest at `.cursor-plugin/plugin.json`; default component folders and frontmatter; marketplace format and path resolution.
- [Cursor plugins](https://cursor.com/docs/plugins): private repository provider support, team limits, distribution UI, local real-copy testing, policy and precedence, Azure source-serving caveat.
- [Cursor skills](https://cursor.com/docs/skills): SKILL.md frontmatter and invocation behavior. This package keeps ordinary contextual skills and command files; it does not promise a specific slash UI namespace.
- [Cursor subagents](https://cursor.com/docs/subagents): `model: inherit` and `readonly` behavior. Readonly reviewers cannot run state-changing test/build commands, so a separate verifier has restricted task instructions but write-capable execution.
- [Cursor hooks](https://cursor.com/docs/hooks): version 1 configuration, JSON stdin/stdout, preToolUse allow/deny, failClosed; ask is not enforced today. No hook can prove review completion.
- [Official plugin template marketplace](https://raw.githubusercontent.com/cursor/plugin-template/main/.cursor-plugin/marketplace.json): structural reference only; this package's validator and scripts are original.

This is a Cursor plugin, not a VS Code extension or an Azure DevOps marketplace extension. The package does not include MCP, variables, credentials, third-party executable code or remote integrations.

## Native Plan integration sources (checked 2026-10-12)
- [Plan Mode](https://cursor.com/docs/agent/plan-mode): user-selected mode, clarifying questions, editable reviewable plans and click to build. This package asks the coordinator to use those native facilities; no programmatic mode switch is asserted.
- [Skills](https://cursor.com/docs/skills): skills provide agent instructions and recommend the ask questions tool for clarification. Tool availability/rendering still needs a smoke test.
- [Subagents](https://cursor.com/docs/subagents): custom roles support `readonly: true` and `model: inherit`; installed-build discovery and actual delegation need testing.
- [Plugin reference](https://cursor.com/docs/reference/plugins): command/skill/agent packaging, not a Build callback API.
- [May 7, 2026 changelog](https://cursor.com/changelog/05-07-26): Build in Parallel identifies independent tasks and executes with async subagents. The native control does not guarantee this package's role assignments or agent-card UI; inspect actual task output.

The embedded self-contained team execution contract is this package's prompt design, not a documented guarantee of UI or custom-agent execution. No Cursor runtime smoke test has been performed for 1.1.0 here.

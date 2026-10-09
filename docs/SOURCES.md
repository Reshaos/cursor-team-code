# Official sources and verification
Checked on 2026-10-09. Read current docs again before installation because product behavior can change.

- [Cursor plugins reference](https://cursor.com/docs/reference/plugins): Cursor manifest at `.cursor-plugin/plugin.json`; default component folders and frontmatter; marketplace format and path resolution.
- [Cursor plugins](https://cursor.com/docs/plugins): private repository provider support, team limits, distribution UI, local real-copy testing, policy and precedence, Azure source-serving caveat.
- [Cursor skills](https://cursor.com/docs/skills): SKILL.md frontmatter and invocation behavior. This package keeps ordinary contextual skills and command files; it does not promise a specific slash UI namespace.
- [Cursor subagents](https://cursor.com/docs/subagents): `model: inherit` and `readonly` behavior. Readonly reviewers cannot run state-changing test/build commands, so a separate verifier has restricted task instructions but write-capable execution.
- [Cursor hooks](https://cursor.com/docs/hooks): version 1 configuration, JSON stdin/stdout, preToolUse allow/deny, failClosed; ask is not enforced today. No hook can prove review completion.
- [Official plugin template marketplace](https://raw.githubusercontent.com/cursor/plugin-template/main/.cursor-plugin/marketplace.json): structural reference only; this package's validator and scripts are original.

This is a Cursor plugin, not a VS Code extension or an Azure DevOps marketplace extension. The package does not include MCP, variables, credentials, third-party executable code or remote integrations.

# Portable team code plugin
A portable Cursor team plugin source repository for local code work. Extract into a new standalone folder, then import its contents into your own private Git repository using your approved work process. The starter does not install itself or publish remotely. Retrieve source only through a channel allowed by your organization; publishing source is not permission to bypass workplace controls.

## Start here
1. Read [QUICKSTART.md](docs/QUICKSTART.md) and [INSTALL-UPDATE.md](docs/INSTALL-UPDATE.md).
2. Customize `plugins/team-code/rules/user-custom.mdc` for your team's portable conventions. Change marketplace owner/name if desired and keep plugin identifiers consistent.
3. Adapt [templates/AGENTS.md](templates/AGENTS.md) inside each code project's own repository; record inspected, approved local commands and fixtures there.
4. After a deliberate install, open your source project in Cursor and type `/team` followed by a plain-English request.

Example: `/team Fix the total calculation when a line has zero quantity. Add a focused regression test using the existing local fixtures.`

For a plan you can review first, select native Cursor Plan mode and invoke `/team-plan` with your request. It prepares a native editable plan/TODOs containing concrete custom-agent tasks and execution instructions, then stops. After review, native Build follows those instructions; `/team-build` is an explicit fallback for an identified, approved plan. Commands do not switch modes or guarantee UI behavior. See the [Plan/Build smoke test](docs/VALIDATION.md).

The main command plans proportionately, gives independent workers disjoint file scopes, obtains separate code and test reviews, fixes within a bounded budget, performs final checks and updates relevant documentation. Tiny changes use one short path. Agents inherit the parent model. This is guidance, not a sandbox or a guarantee that review occurred.

## Contents
- `.cursor-plugin/marketplace.json`: private marketplace with one plugin.
- `plugins/team-code/`: supported plugin manifest, 3 rules, 7 commands, 4 skills, 5 custom agents.
- `templates/`: project AGENTS.md, feature map and ADR templates. These are not globally installed instructions.
- `examples/optional-hooks/`: opt-in deterministic example, deliberately outside automatic hook discovery.
- `scripts/`: dependency-free validation, tests and reproducible packaging.
- `docs/`: novice guidance, customization, CI contract, sources and validation/review evidence.

## Boundaries
Local code edits and approved isolated tests only. No application APIs, real databases, service desks, deployment, remote changes, credentials/security changes, paid APIs, dependency installation or network restores. Azure and SQL support means editing source with approved mocks/fixtures. No MCP configuration is included. Environment permissions and human review remain necessary.

## Validate and package
Requires existing Python 3.10+; no package dependencies. On Windows use `py -3` in place of `python3` below if that is your installed launcher.

```text
python3 scripts/validate.py
python3 scripts/test_package.py
python3 scripts/package.py
```

The last command validates first and produces `dist/cursor-team-code-1.1.0.zip` plus SHA256. The archive contains this repository's source, without Git history. [Validation limits](docs/VALIDATION.md) distinguish static checks from an actual Cursor loading test. No third-party code is bundled. See [PROVENANCE.md](PROVENANCE.md) for authorship and licensing status; decide an explicit license before granting downstream reuse rights.

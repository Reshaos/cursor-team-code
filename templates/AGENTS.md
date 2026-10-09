# Project working instructions
Copy and adapt this template into each source project's own AGENTS.md. Replace placeholders before relying on commands; nested instructions apply within their directories. This template is not an installed global instruction.

## Scope and architecture
- Selected project root: <local path or repository-relative scope>
- Feature map: <existing path>
- ADR directory: <existing path>
- Source/test ownership and generated-file exclusions: <paths>
- SDK/tool versions and evidence: <global.json / existing documentation>

## Approved isolated commands
| Purpose | Exact command | Working directory | Isolation evidence / allowed outputs |
| --- | --- | --- | --- |
| Build | <offline command> | <path> | <inspected targets; cached dependencies> |
| Focused tests | <offline command> | <path> | <approved mocks/fixtures; no live systems> |
| Formatting/static checks | <local command> | <path> | <side effects reviewed> |

Approval here is for local code checks only. Never contact application APIs, real databases, service desks, deployment targets or paid APIs; no network restore/install, credentials/security changes, remote Git changes or unrelated project work. Inspect command changes before running them. Missing tools or uncertain isolation are blockers.

## Conventions
<Portable rules come from the plugin; record project-specific conventions here.>

## Documentation upkeep
Maintain the feature map for behavior changes and ADRs for durable architecture decisions. Preserve prior decisions and link real source/tests. Tiny edits remain lightweight.

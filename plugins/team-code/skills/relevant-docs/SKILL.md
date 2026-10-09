---
name: relevant-docs
description: Use when behavior or durable architecture changes require project documentation
---

# Relevant documentation
Find existing feature map, ADR conventions and applicable AGENTS.md in the project. Update only facts supported by the final code and decisions. A feature map records feature, source paths, user-visible behavior, tests and relevant ADRs; record real paths, not invented ones. Maintain links after moves. Mark unverified assumptions.

For a durable architecture choice write an ADR with context, alternatives, decision, consequences and verification; use the project's numbering/status convention. Supersede rather than erase prior rationale. A small fix generally needs no ADR. Update project AGENTS.md only when project commands or lasting working instructions actually changed and the request authorizes it; never copy project-specific facts into the plugin. If no feature map exists, create a small one only when useful for a behavior change. Report documentation updated or a concrete reason no update is needed. Templates live in this source repository's templates/ directory.

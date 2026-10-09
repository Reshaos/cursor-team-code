---
name: local-test-design
description: Use to design behavioral regression tests with approved local mocks and fixtures
---

# Local test design
Read existing testing conventions and code paths. Cover changed acceptance criteria, failure/edge cases and a meaningful regression case. Inspect fixture initialization, application startup, SDK adapters and build targets for external access. Use already approved in-process mocks, static fixtures or isolated file fixtures. Never use a real application API, database, service desk, deployment, paid API or credentials. Do not start external services or fetch packages. If isolation is unproven, block execution and report what is needed. Keep tests behavior-focused rather than copies of implementation. Report which requirement each test demonstrates and remaining gaps.

#!/usr/bin/env python3
"""Original dependency-free validator for this package's deliberately narrow layout."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n"), f"missing frontmatter: {path}"
    header, body = text[4:].split("\n---\n", 1)
    fields = {}
    for line in header.splitlines():
        assert ":" in line, f"invalid simple frontmatter: {path}"
        key, value = line.split(":", 1)
        assert key not in fields, f"duplicate field: {path}"
        fields[key] = value.strip()
    assert body.strip(), f"empty body: {path}"
    return fields


def validate(root=ROOT):
    root = Path(root)
    errors = []
    def require(condition, message):
        if not condition:
            errors.append(message)
    try:
        paths = list(root.rglob("*"))
        for path in paths:
            require(not path.is_symlink(), f"symlink forbidden: {path}")
            if path.is_file() and not any(x in {".git", "dist", "__pycache__"} for x in path.relative_to(root).parts):
                require(path.suffix.lower() not in {".exe", ".dll", ".pem", ".pfx", ".key"}, f"unexpected binary/key file: {path}")
                if path.suffix in {".md", ".mdc", ".json", ".py"}:
                    text = path.read_text(encoding="utf-8")
                    require("\x00" not in text, f"NUL byte: {path}")
                    if path.suffix == ".json":
                        json.loads(text)
        marketplace = json.loads((root / ".cursor-plugin/marketplace.json").read_text())
        require(set(marketplace) == {"name", "owner", "metadata", "plugins"}, "unexpected marketplace fields")
        require(bool(NAME.fullmatch(marketplace["name"])), "invalid marketplace name")
        require(bool(marketplace["owner"]["name"].strip()), "missing owner")
        require(len(marketplace["plugins"]) == 1, "expected one plugin")
        entry = marketplace["plugins"][0]
        source = Path(entry["source"])
        require(not source.is_absolute() and ".." not in source.parts and ":" not in str(source) and "\\" not in str(source), "unsafe marketplace source")
        require(entry["source"] == "plugins/team-code", "unexpected source layout")
        plugin = root / "plugins/team-code"
        manifest = json.loads((plugin / ".cursor-plugin/plugin.json").read_text())
        require(set(manifest) == {"name", "version", "description"}, "manifest must stay minimal; no MCP, variables or hooks")
        require(manifest["name"] == entry["name"] == "team-code", "plugin name mismatch")
        require(bool(re.fullmatch(r"\d+\.\d+\.\d+", manifest["version"])), "invalid version")
        require(marketplace["metadata"]["version"] == manifest["version"], "version mismatch")
        require(not (plugin / "mcp.json").exists(), "MCP forbidden")
        require(not (plugin / "hooks").exists(), "hooks must remain disabled outside plugin")
        expected = {
            "rules": {"code-only.mdc", "dotnet-sql.mdc", "user-custom.mdc"},
            "commands": {x + ".md" for x in ["team", "plan", "review", "check", "docs"]},
            "agents": {x + ".md" for x in ["team-planner", "team-implementer", "team-code-reviewer", "team-test-reviewer", "team-test-verifier"]},
            "skills": {"team-workflow", "finalchecks", "relevant-docs", "local-test-design"},
        }
        for folder, names in expected.items():
            actual = {p.name for p in (plugin / folder).iterdir()}
            require(actual == names, f"unexpected {folder} inventory")
            for name in names:
                path = plugin / folder / name
                if folder == "skills":
                    path = path / "SKILL.md"
                fields = frontmatter(path)
                require(bool(fields.get("description")), f"missing description: {path}")
                if folder != "rules":
                    require(fields.get("name") == (name if folder == "skills" else Path(name).stem), f"name mismatch: {path}")
                else:
                    require(fields.get("alwaysApply") in {"true", "false"}, f"invalid alwaysApply: {path}")
                if folder == "agents":
                    require(fields.get("model") == "inherit", f"model must inherit: {path}")
                    expected_readonly = "true" if name in {"team-planner.md", "team-code-reviewer.md", "team-test-reviewer.md"} else "false"
                    require(fields.get("readonly") == expected_readonly, f"readonly mismatch: {path}")
        command = (plugin / "commands/team.md").read_text().split("\n---\n", 1)[1]
        skill = (plugin / "skills/team-workflow/SKILL.md").read_text().split("\n---\n", 1)[1]
        require(command == skill, "main command and workflow skill drift")
        for name in ["AGENTS.md", "FEATURE-MAP.md", "ADR.md"]:
            require((root / "templates" / name).is_file(), f"missing template {name}")
        require(not (plugin / "AGENTS.md").exists(), "project AGENTS must not be installed globally")
        hook = json.loads((root / "examples/optional-hooks/hooks.example.json").read_text())
        require(hook.get("version") == 1 and set(hook["hooks"]) == {"preToolUse"}, "invalid example hook events")
        require(hook["hooks"]["preToolUse"][0].get("failClosed") is True, "example must fail closed")
        # Check source Markdown links only; web links and placeholders require human review.
        for path in root.rglob("*.md"):
            if any(x in {".git", "dist", "__pycache__"} for x in path.relative_to(root).parts):
                continue
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", path.read_text()):
                if target.startswith(("https://", "http://", "#", "<")):
                    continue
                require((path.parent / target.split("#", 1)[0]).exists(), f"broken link {target} in {path}")
    except (OSError, ValueError, KeyError, TypeError, AssertionError, IndexError) as exc:
        errors.append(str(exc))
    return errors


if __name__ == "__main__":
    failures = validate()
    for failure in failures:
        print("FAIL:", failure)
    print("Validation failed" if failures else "PASS: structure, manifests, components, boundaries and links")
    sys.exit(bool(failures))

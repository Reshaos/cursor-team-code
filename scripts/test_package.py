#!/usr/bin/env python3
"""Isolated meaningful checks; no application execution, network or dependencies."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile
from package import package
from validate import ROOT, validate


class PackageTests(unittest.TestCase):
    def copy(self, parent):
        target = Path(parent) / "source"
        shutil.copytree(ROOT, target, ignore=shutil.ignore_patterns("dist", ".git", "__pycache__"))
        return target

    def test_source_valid(self):
        self.assertEqual(validate(), [])

    def test_mcp_hook_and_model_mutations_rejected(self):
        for mutation in ("mcp", "hook", "model", "traversal", "link", "drift"):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as tmp:
                root = self.copy(tmp)
                plugin = root / "plugins/team-code"
                if mutation == "mcp":
                    (plugin / "mcp.json").write_text("{}", encoding="utf-8")
                elif mutation == "hook":
                    (plugin / "hooks").mkdir()
                elif mutation == "model":
                    path = plugin / "agents/team-code-reviewer.md"
                    path.write_text(path.read_text(encoding="utf-8").replace("model: inherit", "model: fixed-provider"), encoding="utf-8")
                elif mutation == "traversal":
                    path = root / ".cursor-plugin/marketplace.json"
                    value = json.loads(path.read_text(encoding="utf-8")); value["plugins"][0]["source"] = "../outside"
                    path.write_text(json.dumps(value), encoding="utf-8")
                elif mutation == "link":
                    (root / "README.md").write_text("[broken](missing.md)", encoding="utf-8")
                else:
                    path = plugin / "commands/team.md"
                    path.write_text(path.read_text(encoding="utf-8") + "changed budget\n", encoding="utf-8")
                self.assertTrue(validate(root))

    def test_reproducible_archive_and_exclusions(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.copy(tmp)
            (root / ".git").mkdir(); (root / ".git/private").write_text("excluded", encoding="utf-8")
            (root / ".work").mkdir(); (root / ".work/note").write_text("excluded", encoding="utf-8")
            a, ha = package(root, Path(tmp) / "a.zip")
            b, hb = package(root, Path(tmp) / "b.zip")
            self.assertEqual(ha, hb); self.assertEqual(a.read_bytes(), b.read_bytes())
            with ZipFile(a) as archive:
                names = archive.namelist()
                self.assertTrue(all(name.startswith("cursor-team-source/") for name in names))
                self.assertFalse(any("/.git/" in n or "/.work/" in n or "/dist/" in n for n in names))
                self.assertIsNone(archive.testzip())
                extract = Path(tmp) / "extract"
                archive.extractall(extract)
                self.assertEqual(validate(extract / "cursor-team-source"), [])

    def test_entry_points_cannot_drift(self):
        for name in ("team", "team-plan", "team-build"):
            for mutation in ("reference", "route", "duplicate-instructions"):
                with self.subTest(name=name, mutation=mutation), tempfile.TemporaryDirectory() as tmp:
                    root = self.copy(tmp)
                    path = root / f"plugins/team-code/commands/{name}.md"
                    text = path.read_text(encoding="utf-8")
                    if mutation == "reference":
                        text = text.replace("../skills/team-workflow/SKILL.md", "../skills/finalchecks/SKILL.md")
                    elif mutation == "route":
                        text = text.replace(f"entry point `{name}`", "entry point `other`")
                    else:
                        text += "Implement immediately with an unlimited fix budget.\n"
                    path.write_text(text, encoding="utf-8")
                    self.assertIn(f"canonical entry-point drift: {name}", validate(root))

    def test_native_workflow_contract_mutations_rejected(self):
        for marker in (
            "never override the mode's read-only boundary",
            "Never silently select the latest arbitrary plan",
            "native ask questions tool when available",
            "actual native editable plan and native TODOs",
            "Label assignments as proposed, not actual spawned tasks",
            "copy and specialize the entire execution procedure below",
            "Stop after producing the plan for user review",
            "read the exact approved plan and perform its revalidation TODO before any edits",
            "three independent implementation scopes; one replan; two fix cycles; two attempts per failing check",
            "fresh team-code-reviewer and a distinct fresh team-test-reviewer",
        ):
            with self.subTest(marker=marker), tempfile.TemporaryDirectory() as tmp:
                root = self.copy(tmp)
                path = root / "plugins/team-code/skills/team-workflow/SKILL.md"
                path.write_text(path.read_text(encoding="utf-8").replace(marker, "contract removed"), encoding="utf-8")
                self.assertIn(f"missing canonical workflow contract: {marker}", validate(root))

    def test_new_commands_required(self):
        for name in ("team-plan", "team-build"):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as tmp:
                root = self.copy(tmp)
                (root / f"plugins/team-code/commands/{name}.md").unlink()
                self.assertIn("unexpected commands inventory", validate(root))

    def test_marketplace_paths_and_utf8(self):
        for source in ("../outside", "/outside", "C:/outside", "plugins\\team-code", "//host/share"):
            with self.subTest(source=source), tempfile.TemporaryDirectory() as tmp:
                root = self.copy(tmp)
                path = root / ".cursor-plugin/marketplace.json"
                value = json.loads(path.read_text(encoding="utf-8"))
                value["plugins"][0]["source"] = source
                path.write_text(json.dumps(value), encoding="utf-8")
                self.assertIn("unsafe marketplace source", validate(root))
        with tempfile.TemporaryDirectory() as tmp:
            root = self.copy(tmp)
            # UTF-8 byte 0x9d cannot be decoded with Windows' common cp1252 default.
            path = root / "README.md"
            path.write_text(path.read_text(encoding="utf-8") + "\nUnicode fixture: \u201d \u6f22\n", encoding="utf-8")
            self.assertEqual(validate(root), [])
            archive, _ = package(root, Path(tmp) / "unicode.zip")
            with ZipFile(archive) as zipped:
                self.assertIn("Unicode fixture: \u201d \u6f22", zipped.read("cursor-team-source/README.md").decode("utf-8"))

    def test_gate_protocol(self):
        script = ROOT / "examples/optional-hooks/conservative_gate.py"
        for payload, expected in [
            ({"hook_event_name": "preToolUse", "tool_name": "Read"}, "allow"),
            ({"hook_event_name": "preToolUse", "tool_name": "Write"}, "allow"),
            ({"hook_event_name": "preToolUse", "tool_name": "Task"}, "allow"),
            ({"hook_event_name": "preToolUse", "tool_name": "Shell"}, "deny"),
            ({"hook_event_name": "preToolUse", "tool_name": "MCP"}, "deny"),
            ({"hook_event_name": "preToolUse", "tool_name": "Unknown"}, "deny"),
            ({"hook_event_name": "stop", "tool_name": "Read"}, "deny"),
            ({"hook_event_name": "preToolUse", "tool_name": []}, "deny"),
            ({"hook_event_name": "preToolUse", "tool_name": {}}, "deny"),
            ({"hook_event_name": "preToolUse", "tool_name": 42}, "deny"),
            ([], "deny"), (None, "deny"),
        ]:
            with self.subTest(payload=payload):
                result = subprocess.run([sys.executable, str(script)], input=json.dumps(payload), text=True, capture_output=True, check=True)
                self.assertEqual(json.loads(result.stdout)["permission"], expected)
                self.assertEqual(result.stderr, "")
        result = subprocess.run([sys.executable, str(script)], input="not-json", text=True, capture_output=True, check=True)
        self.assertEqual(json.loads(result.stdout)["permission"], "deny")


if __name__ == "__main__":
    unittest.main()

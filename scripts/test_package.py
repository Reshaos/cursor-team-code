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
                    (plugin / "mcp.json").write_text("{}")
                elif mutation == "hook":
                    (plugin / "hooks").mkdir()
                elif mutation == "model":
                    path = plugin / "agents/team-code-reviewer.md"
                    path.write_text(path.read_text().replace("model: inherit", "model: fixed-provider"))
                elif mutation == "traversal":
                    path = root / ".cursor-plugin/marketplace.json"
                    value = json.loads(path.read_text()); value["plugins"][0]["source"] = "../outside"
                    path.write_text(json.dumps(value))
                elif mutation == "link":
                    (root / "README.md").write_text("[broken](missing.md)")
                else:
                    path = plugin / "commands/team.md"
                    path.write_text(path.read_text() + "changed budget\n")
                self.assertTrue(validate(root))

    def test_reproducible_archive_and_exclusions(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.copy(tmp)
            (root / ".git").mkdir(); (root / ".git/private").write_text("excluded")
            (root / ".work").mkdir(); (root / ".work/note").write_text("excluded")
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

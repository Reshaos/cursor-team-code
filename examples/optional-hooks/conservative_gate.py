#!/usr/bin/env python3
"""Conservative optional demo: no file/network writes, JSON input/output only."""
import json
import sys


def decide(payload):
    # Exact names only. Unknown/new tools remain denied until deliberately reviewed.
    tool_name = payload.get("tool_name") if isinstance(payload, dict) else None
    allowed = isinstance(payload, dict) and payload.get("hook_event_name") == "preToolUse" and isinstance(tool_name, str) and tool_name in {"Read", "Write", "Task"}
    if allowed:
        return {"permission": "allow"}
    return {"permission": "deny", "user_message": "Optional conservative gate denied this tool.", "agent_message": "Shell, MCP, unknown tools and invalid hook inputs are disabled by this example. Report the blocked action; do not bypass the gate."}


def main():
    try:
        payload = json.load(sys.stdin)
    except (ValueError, UnicodeError):
        payload = None
    print(json.dumps(decide(payload), separators=(",", ":")))


if __name__ == "__main__":
    main()

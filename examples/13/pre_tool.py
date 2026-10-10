"""Offline teaching guardrail; never executes tool input."""
import json
import sys

try:
    event = json.load(sys.stdin)
except (ValueError, TypeError):
    print("Invalid hook JSON", file=sys.stderr)
    sys.exit(1)

if not isinstance(event, dict):
    print("Hook input must be a JSON object", file=sys.stderr)
    sys.exit(1)

tool_input = event.get("tool_input", {})
command = tool_input.get("command", "") if isinstance(tool_input, dict) else ""
if not isinstance(command, str):
    command = ""
if event.get("hook_event_name") == "PreToolUse" and "HOOK_LAB_BLOCK" in command:
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "Teaching marker blocked; choose HOOK_LAB_ALLOW."
    }}))
else:
    print("{}")

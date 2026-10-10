"""Offline validator for this lesson's two-field result contract."""
import json
import sys
from pathlib import Path

try:
    value = json.loads(Path(sys.argv[1]).read_text())
    valid = (isinstance(value, dict) and set(value) == {"summary", "risks"}
             and isinstance(value["summary"], str)
             and isinstance(value["risks"], list)
             and all(isinstance(x, str) for x in value["risks"]))
except (ValueError, OSError, IndexError):
    valid = False
print("PASS" if valid else "FAIL: missing or invalid result contract")
sys.exit(0 if valid else 1)

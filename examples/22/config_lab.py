"""Flat-key teaching simulation; NOT a Codex config loader or permission engine."""
import json
from pathlib import Path
import tomllib

BASE = Path(__file__).parent


def resolve(trusted, cli=None):
    values, origins = {}, {}
    for name in ("user", "profile", "project-root", "project-near"):
        if name.startswith("project") and not trusted:
            continue
        layer = tomllib.loads((BASE / (name + ".toml")).read_text())
        for key, value in layer.items():
            values[key], origins[key] = value, name
    for key, value in (cli or {}).items():
        values[key], origins[key] = value, "cli"
    requirements = tomllib.loads((BASE / "requirements.demo.toml").read_text())
    allowed = requirements["allowed_sandbox_modes"]
    if values["sandbox_mode"] not in allowed:
        return {"status": "rejected-by-demo-requirement", "values": values, "origins": origins}
    return {"status": "accepted-by-demo-requirement", "values": values, "origins": origins}


def main():
    cases = [
        ("trusted", True, {}, "project-near", "workspace-write", "accepted-by-demo-requirement"),
        ("untrusted", False, {}, "profile", "read-only", "accepted-by-demo-requirement"),
        ("cli-read-only", True, {"sandbox_mode": "read-only"}, "cli", "read-only", "accepted-by-demo-requirement"),
        ("cli-too-broad", True, {"sandbox_mode": "danger-full-access"}, "cli", "danger-full-access", "rejected-by-demo-requirement"),
    ]
    for name, trusted, cli, origin, sandbox, status in cases:
        out = resolve(trusted, cli)
        assert out["origins"]["sandbox_mode"] == origin, out
        assert out["values"]["sandbox_mode"] == sandbox, out
        assert out["status"] == status, out
        print(json.dumps({"case": name, **out}, ensure_ascii=False))
    try:
        tomllib.loads((BASE / "invalid.toml").read_text())
    except tomllib.TOMLDecodeError:
        print("PASS: invalid TOML rejected")
    else:
        raise AssertionError("Invalid TOML was accepted")
    print("PASS: offline educational cases; real Codex config not changed")


if __name__ == "__main__":
    main()

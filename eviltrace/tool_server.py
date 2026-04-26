from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict

from .evidence import inventory_case, load_events
from .tools import ReadOnlyToolbox

TOOLS = {
    "inventory_case": "Return immutable evidence metadata and SHA-256 hashes.",
    "event_count": "Return event counts by action type.",
    "suspicious_logins": "Return suspicious login events.",
    "impossible_travel": "Return same-user multi-country login patterns.",
    "suspicious_commands": "Return suspicious process execution events.",
    "persistence_changes": "Return persistence-related changes.",
    "exfil_signals": "Return possible exfiltration signals.",
}


def call_tool(name: str, case_id: str = "case_alpha", args: dict | None = None) -> dict:
    evidence = inventory_case(case_id)
    events = load_events(case_id, evidence)
    if name == "inventory_case":
        return {"evidence": [asdict(record) for record in evidence]}
    toolbox = ReadOnlyToolbox(events)
    if not hasattr(toolbox, name):
        raise ValueError(f"unknown read-only tool: {name}")
    result = getattr(toolbox, name)(**(args or {}))
    return asdict(result)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="EvilTrace MCP-style read-only tool server")
    parser.add_argument("--case", default="case_alpha")
    parser.add_argument("--manifest", action="store_true")
    parser.add_argument("--call")
    ns = parser.parse_args(argv)
    if ns.manifest:
        print(json.dumps({"name": "eviltrace-readonly-tools", "tools": TOOLS}, indent=2))
        return 0
    if ns.call:
        print(json.dumps(call_tool(ns.call, ns.case), indent=2))
        return 0
    for line in sys.stdin:
        request = json.loads(line)
        try:
            response = {"ok": True, "result": call_tool(request["tool"], request.get("case_id", ns.case), request.get("args") or {})}
        except Exception as exc:
            response = {"ok": False, "error": str(exc)}
        print(json.dumps(response), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

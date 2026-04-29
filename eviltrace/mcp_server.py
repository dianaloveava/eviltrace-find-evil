from __future__ import annotations

import json
import sys
from typing import Any

from .tool_server import TOOLS, call_tool

SERVER_INFO = {"name": "eviltrace-readonly-mcp", "version": "0.2.0"}
PROTOCOL_VERSION = "2024-11-05"


def _tool_schema(name: str, description: str) -> dict[str, Any]:
    properties: dict[str, Any] = {
        "case_id": {
            "type": "string",
            "description": "EvilTrace case id under data/fixtures; defaults to case_alpha.",
            "default": "case_alpha",
        }
    }
    if name == "suspicious_commands":
        properties["markers"] = {
            "type": "array",
            "items": {"type": "string"},
            "description": "Optional suspicious command markers to match.",
        }
    return {
        "name": name,
        "description": description,
        "inputSchema": {
            "type": "object",
            "properties": properties,
            "additionalProperties": False,
        },
    }


def list_tools() -> list[dict[str, Any]]:
    return [_tool_schema(name, description) for name, description in TOOLS.items()]


def handle_request(request: dict[str, Any]) -> dict[str, Any] | None:
    request_id = request.get("id")
    method = request.get("method")
    params = request.get("params") or {}

    try:
        if method == "initialize":
            result = {
                "protocolVersion": params.get("protocolVersion") or PROTOCOL_VERSION,
                "capabilities": {"tools": {}},
                "serverInfo": SERVER_INFO,
            }
        elif method == "notifications/initialized":
            return None
        elif method == "tools/list":
            result = {"tools": list_tools()}
        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments") or {}
            if not isinstance(tool_name, str) or not tool_name:
                raise ValueError("tools/call requires params.name")
            if not isinstance(arguments, dict):
                raise ValueError("tools/call params.arguments must be an object")
            case_id = str(arguments.pop("case_id", "case_alpha"))
            tool_result = call_tool(tool_name, case_id, arguments)
            result = {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(tool_result, indent=2),
                    }
                ],
                "structuredContent": tool_result,
                "isError": False,
            }
        else:
            return _error(request_id, -32601, f"Method not found: {method}")
        return {"jsonrpc": "2.0", "id": request_id, "result": result}
    except Exception as exc:
        return _error(request_id, -32000, str(exc))


def _error(request_id: Any, code: int, message: str) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}


def main() -> int:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
        except json.JSONDecodeError as exc:
            print(json.dumps(_error(None, -32700, f"Parse error: {exc}")), flush=True)
            continue
        response = handle_request(request)
        if response is not None:
            print(json.dumps(response), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

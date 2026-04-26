from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import asdict
from typing import Any

from .evidence import evidence_ref, iter_refs
from .models import Event, ToolResult

SUSPICIOUS_IPS = {"203.0.113.50", "198.51.100.77"}
SUSPICIOUS_COMMAND_MARKERS = ["curl http://203.0.113.50", "powershell -enc", "nc -e", "chmod +x /tmp"]


def _raw_get(event: Event, key: str, default: str = "") -> str:
    value = event.raw.get(key)
    if value in {None, ""} and isinstance(event.raw.get("raw"), dict):
        value = event.raw["raw"].get(key)
    return str(value if value not in {None, ""} else default)


class ReadOnlyToolbox:
    """Deterministic read-only tools over parsed fixture events."""

    def __init__(self, events: list[Event]) -> None:
        self.events = events

    def event_count(self) -> ToolResult:
        by_action = Counter(event.action for event in self.events)
        return ToolResult(
            tool="event_count",
            query={},
            summary=f"Loaded {len(self.events)} events across {len(by_action)} action types.",
            evidence_refs=iter_refs(self.events[:3]),
            data={"total": len(self.events), "by_action": dict(sorted(by_action.items()))},
        )

    def suspicious_logins(self) -> ToolResult:
        hits = [
            event for event in self.events
            if event.action in {"login_success", "login_failure"}
            and _raw_get(event, "ip") in SUSPICIOUS_IPS
        ]
        return ToolResult(
            tool="suspicious_logins",
            query={"ips": sorted(SUSPICIOUS_IPS)},
            summary=f"Found {len(hits)} login events tied to known suspicious IPs.",
            evidence_refs=iter_refs(hits),
            data={"events": [asdict(event) for event in hits]},
        )

    def impossible_travel(self) -> ToolResult:
        by_user: dict[str, list[Event]] = defaultdict(list)
        for event in self.events:
            if event.action == "login_success":
                by_user[event.user].append(event)
        hits: list[dict[str, Any]] = []
        refs: list[str] = []
        for user, events in by_user.items():
            countries = {_raw_get(event, "country") for event in events if _raw_get(event, "country")}
            if len(countries) > 1:
                hits.append({"user": user, "countries": sorted(countries), "event_ids": [e.id for e in events]})
                refs.extend(iter_refs(events))
        return ToolResult(
            tool="impossible_travel",
            query={"rule": "same user successful logins from multiple countries in fixture window"},
            summary=f"Found {len(hits)} users with multi-country login success patterns.",
            evidence_refs=refs,
            data={"hits": hits},
        )

    def suspicious_commands(self) -> ToolResult:
        hits: list[Event] = []
        for event in self.events:
            if event.action != "process_start":
                continue
            cmd = f"{_raw_get(event, 'command')} {event.detail}".lower()
            if any(marker in cmd for marker in SUSPICIOUS_COMMAND_MARKERS):
                hits.append(event)
        return ToolResult(
            tool="suspicious_commands",
            query={"markers": SUSPICIOUS_COMMAND_MARKERS},
            summary=f"Found {len(hits)} suspicious command executions.",
            evidence_refs=iter_refs(hits),
            data={"events": [asdict(event) for event in hits]},
        )

    def persistence_changes(self) -> ToolResult:
        hits = [event for event in self.events if event.action in {"cron_write", "service_install", "registry_run_key"}]
        return ToolResult(
            tool="persistence_changes",
            query={"actions": ["cron_write", "service_install", "registry_run_key"]},
            summary=f"Found {len(hits)} persistence-related changes.",
            evidence_refs=iter_refs(hits),
            data={"events": [asdict(event) for event in hits]},
        )

    def exfil_signals(self) -> ToolResult:
        hits = [event for event in self.events if event.action in {"archive_created", "large_upload", "dns_tunnel"}]
        return ToolResult(
            tool="exfil_signals",
            query={"actions": ["archive_created", "large_upload", "dns_tunnel"]},
            summary=f"Found {len(hits)} possible exfiltration signals.",
            evidence_refs=iter_refs(hits),
            data={"events": [asdict(event) for event in hits]},
        )

    def host_timeline(self, host: str) -> ToolResult:
        hits = [event for event in self.events if event.host == host]
        return ToolResult(
            tool="host_timeline",
            query={"host": host},
            summary=f"Host {host} has {len(hits)} timeline events.",
            evidence_refs=iter_refs(hits),
            data={"events": [asdict(event) for event in hits]},
        )


def refs_to_lines(refs: list[str]) -> list[str]:
    return [ref for ref in refs if ref]

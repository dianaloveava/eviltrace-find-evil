from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Iterable

from .models import EvidenceRecord, Event

SUPPORTED_EVENT_FILES = {"events.jsonl"}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fixture_dir(case_id: str) -> Path:
    safe = "".join(ch for ch in case_id if ch.isalnum() or ch in {"_", "-"})
    if safe != case_id or not safe:
        raise ValueError(f"unsafe case id: {case_id!r}")
    return Path("data") / "fixtures" / safe


def inventory_case(case_id: str = "case_alpha") -> list[EvidenceRecord]:
    base = fixture_dir(case_id)
    if not base.exists():
        raise FileNotFoundError(f"fixture case not found: {base}")
    records: list[EvidenceRecord] = []
    for file_path in sorted(p for p in base.rglob("*") if p.is_file()):
        rel = file_path.as_posix()
        kind = "event-log" if file_path.name in SUPPORTED_EVENT_FILES else "documentation"
        records.append(
            EvidenceRecord(
                id=f"ev-{len(records)+1:03d}",
                path=rel,
                sha256=sha256_file(file_path),
                kind=kind,
                size=file_path.stat().st_size,
                description=_describe(file_path),
            )
        )
    return records


def _describe(path: Path) -> str:
    if path.name == "events.jsonl":
        return "Synthetic incident-response event stream for EvilTrace demo case."
    if path.name.lower().endswith("readme.md"):
        return "Fixture notes and safe-use documentation."
    return "Case fixture artifact."


def load_events(case_id: str = "case_alpha", evidence: list[EvidenceRecord] | None = None) -> list[Event]:
    base = fixture_dir(case_id)
    evidence = evidence or inventory_case(case_id)
    by_name = {Path(record.path).name: record for record in evidence}
    event_file = base / "events.jsonl"
    if not event_file.exists():
        raise FileNotFoundError(f"events fixture missing: {event_file}")
    event_evidence = by_name.get("events.jsonl")
    events: list[Event] = []
    with event_file.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            raw = json.loads(line)
            events.append(
                Event(
                    id=f"evt-{line_no:04d}",
                    ts=str(raw.get("ts", "")),
                    source=str(raw.get("source", "unknown")),
                    host=str(raw.get("host", "unknown")),
                    user=str(raw.get("user", "unknown")),
                    action=str(raw.get("action", "unknown")),
                    detail=str(raw.get("detail", "")),
                    raw=raw,
                    evidence_id=event_evidence.id if event_evidence else "ev-unknown",
                    line=line_no,
                )
            )
    return events


def evidence_ref(event: Event) -> str:
    return f"{event.evidence_id}:L{event.line}:{event.id}"


def iter_refs(events: Iterable[Event]) -> list[str]:
    return [evidence_ref(event) for event in events]

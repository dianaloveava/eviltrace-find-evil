from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Iterable

CANONICAL_FIELDS = ["ts", "source", "host", "user", "action", "detail"]


def normalize_sift_exports(source_dir: str | Path, case_id: str = "sift_demo") -> Path:
    """Normalize common SIFT/DFIR export files into EvilTrace JSONL events.

    Supported inputs are intentionally read-only and dependency-free:
    - Plaso/log2timeline CSV exports (`*plaso*.csv`, `*timeline*.csv`)
    - JSON/JSONL event exports (`*.json`, `*.jsonl`)
    - Volatility JSON/text process listings (`*volatility*`, `*pslist*`)
    - Sleuth Kit bodyfile-style text (`*bodyfile*`, `*.body`)
    """

    src = Path(source_dir)
    if not src.exists() or not src.is_dir():
        raise FileNotFoundError(f"SIFT export directory not found: {src}")
    safe_case = _safe_case_id(case_id)
    dest = Path("data") / "fixtures" / safe_case
    dest.mkdir(parents=True, exist_ok=True)
    events: list[dict[str, Any]] = []
    for file_path in sorted(p for p in src.rglob("*") if p.is_file()):
        events.extend(_events_from_file(file_path))
    events = sorted(events, key=lambda event: (event.get("ts", ""), event.get("source", ""), event.get("detail", "")))
    out = dest / "events.jsonl"
    with out.open("w", encoding="utf-8") as handle:
        for event in events:
            handle.write(json.dumps(_canonicalize(event), sort_keys=True) + "\n")
    readme = dest / "README.md"
    readme.write_text(_readme(case_id, src, events), encoding="utf-8")
    return dest


def _safe_case_id(case_id: str) -> str:
    if not case_id or any(ch not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-" for ch in case_id):
        raise ValueError("case_id must contain only letters, numbers, underscores, and hyphens")
    return case_id


def _events_from_file(file_path: Path) -> list[dict[str, Any]]:
    name = file_path.name.lower()
    if name.endswith(".jsonl"):
        return list(_read_jsonl(file_path))
    if name.endswith(".json"):
        return list(_read_json(file_path))
    if name.endswith(".csv"):
        return list(_read_csv(file_path))
    if "bodyfile" in name or name.endswith(".body"):
        return list(_read_bodyfile(file_path))
    if "volatility" in name or "pslist" in name or name.endswith(".txt"):
        return list(_read_text(file_path))
    return []


def _read_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if not line.strip():
                continue
            try:
                yield _from_mapping(json.loads(line), path)
            except json.JSONDecodeError:
                yield _from_text(line, path, source="jsonl-text")


def _read_json(path: Path) -> Iterable[dict[str, Any]]:
    raw = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    records = raw if isinstance(raw, list) else raw.get("rows") or raw.get("events") or raw.get("data") or [raw]
    for record in records:
        if isinstance(record, dict):
            yield _from_mapping(record, path)
        else:
            yield _from_text(str(record), path, source="json-text")


def _read_csv(path: Path) -> Iterable[dict[str, Any]]:
    with path.open("r", encoding="utf-8", errors="replace", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            yield _from_mapping(dict(row), path)


def _read_bodyfile(path: Path) -> Iterable[dict[str, Any]]:
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if not line.strip():
                continue
            parts = line.rstrip("\n").split("|")
            detail = parts[1] if len(parts) > 1 else line.strip()
            ts = parts[8] if len(parts) > 8 else ""
            yield {
                "ts": _normalize_ts(ts),
                "source": "sleuthkit-bodyfile",
                "host": "evidence-host",
                "user": "unknown",
                "action": _infer_action(detail),
                "detail": detail,
                "path": detail,
                "raw_source": path.as_posix(),
            }


def _read_text(path: Path) -> Iterable[dict[str, Any]]:
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for index, line in enumerate(handle, start=1):
            if line.strip():
                yield _from_text(line.strip(), path, line=index)


def _from_mapping(row: dict[str, Any], path: Path) -> dict[str, Any]:
    text = " ".join(str(v) for v in row.values() if v is not None)
    return {
        "ts": _pick(row, "ts", "timestamp", "datetime", "date", "Time", "Created Date") or "1970-01-01T00:00:00Z",
        "source": _pick(row, "source", "parser", "Source", "data_type") or _source_from_name(path),
        "host": _pick(row, "host", "hostname", "computer", "Computer") or "evidence-host",
        "user": _pick(row, "user", "username", "User", "account") or "unknown",
        "action": _pick(row, "action", "event_type", "Event ID", "tag") or _infer_action(text),
        "detail": _pick(row, "detail", "message", "Message", "description", "filename", "process_name", "command") or text[:500],
        "raw": row,
        "raw_source": path.as_posix(),
    }


def _from_text(text: str, path: Path, line: int = 0, source: str | None = None) -> dict[str, Any]:
    return {
        "ts": "1970-01-01T00:00:00Z",
        "source": source or _source_from_name(path),
        "host": "evidence-host",
        "user": "unknown",
        "action": _infer_action(text),
        "detail": text[:500],
        "raw": {"line": line, "text": text},
        "raw_source": path.as_posix(),
    }


def _canonicalize(event: dict[str, Any]) -> dict[str, Any]:
    event = dict(event)
    event["ts"] = _normalize_ts(str(event.get("ts") or "1970-01-01T00:00:00Z"))
    event["source"] = str(event.get("source") or "unknown")
    event["host"] = str(event.get("host") or "evidence-host")
    event["user"] = str(event.get("user") or "unknown")
    event["action"] = _infer_action(str(event.get("action") or event.get("detail") or "unknown"))
    event["detail"] = str(event.get("detail") or "")[:1000]
    return event


def _pick(row: dict[str, Any], *keys: str) -> str | None:
    lowered = {str(k).lower(): v for k, v in row.items()}
    for key in keys:
        if key in row and row[key] not in {None, ""}:
            return str(row[key])
        val = lowered.get(key.lower())
        if val not in {None, ""}:
            return str(val)
    return None


def _source_from_name(path: Path) -> str:
    name = path.name.lower()
    if "plaso" in name or "timeline" in name:
        return "plaso"
    if "volatility" in name or "pslist" in name:
        return "volatility"
    if "bodyfile" in name or name.endswith(".body"):
        return "sleuthkit-bodyfile"
    return path.suffix.lstrip(".") or "file"


def _infer_action(text: str) -> str:
    lower = text.lower()
    canonical = {
        "login_success", "login_failure", "process_start", "cron_write",
        "service_install", "registry_run_key", "archive_created",
        "large_upload", "dns_tunnel", "artifact_observed"
    }
    if lower in canonical:
        return lower
    if any(token in lower for token in ["login_success", "successful login", "4624", "accepted password"]):
        return "login_success"
    if any(token in lower for token in ["login_failure", "failed login", "4625", "failed password"]):
        return "login_failure"
    if any(token in lower for token in ["powershell", "cmd.exe", "process", "pslist", "payload", "curl "]):
        return "process_start"
    if any(token in lower for token in ["cron", "service_install", "run key", "persistence"]):
        return "service_install" if "service" in lower else "cron_write"
    if any(token in lower for token in ["archive", ".zip", ".tgz", ".tar"]):
        return "archive_created"
    if any(token in lower for token in ["upload", "egress", "exfil", "dns tunnel"]):
        return "large_upload"
    return "artifact_observed"


def _normalize_ts(value: str) -> str:
    value = value.strip()
    if not value:
        return "1970-01-01T00:00:00Z"
    if value.isdigit():
        try:
            from datetime import datetime, timezone
            return datetime.fromtimestamp(int(value), tz=timezone.utc).isoformat().replace("+00:00", "Z")
        except Exception:
            return value
    if value.endswith("Z") or "T" in value:
        return value
    return value


def _readme(case_id: str, source: Path, events: list[dict[str, Any]]) -> str:
    return f"""# Imported SIFT/DFIR Case: {case_id}\n\nSource directory: `{source}`\n\nThis case was normalized with `python -m eviltrace.cli import-sift --source {source} --case {case_id}`.\n\nNormalized events: {len(events)}\n\nOriginal source files are treated as read-only. EvilTrace writes only this derived `events.jsonl` and does not modify evidence exports.\n"""

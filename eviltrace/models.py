from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Literal

Severity = Literal["info", "low", "medium", "high", "critical"]
Confidence = Literal["unknown", "low", "medium", "high", "confirmed"]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class EvidenceRecord:
    id: str
    path: str
    sha256: str
    kind: str
    size: int
    description: str


@dataclass(frozen=True)
class Event:
    id: str
    ts: str
    source: str
    host: str
    user: str
    action: str
    detail: str
    raw: dict[str, Any]
    evidence_id: str
    line: int


@dataclass
class ToolResult:
    tool: str
    query: dict[str, Any]
    summary: str
    evidence_refs: list[str]
    data: dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentStep:
    index: int
    phase: str
    action: str
    rationale: str
    tool: str | None = None
    result_summary: str | None = None
    evidence_refs: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=utc_now)
    token_usage: dict[str, int | str] = field(default_factory=lambda: {"prompt": 0, "completion": 0, "total": 0, "mode": "deterministic-no-llm"})


@dataclass
class Correction:
    finding_id: str
    before_confidence: Confidence
    after_confidence: Confidence
    reason: str
    evidence_refs: list[str]


@dataclass
class Finding:
    id: str
    title: str
    severity: Severity
    confidence: Confidence
    summary: str
    evidence_refs: list[str]
    reasoning: list[str]
    caveats: list[str] = field(default_factory=list)


@dataclass
class AgentRun:
    id: str
    case_id: str
    status: Literal["completed", "failed"]
    started_at: str
    completed_at: str
    steps: list[AgentStep]
    findings: list[Finding]
    corrections: list[Correction]
    evidence: list[EvidenceRecord]
    metrics: dict[str, Any]


def to_plain(value: Any) -> Any:
    if hasattr(value, "__dataclass_fields__"):
        return asdict(value)
    if isinstance(value, list):
        return [to_plain(v) for v in value]
    if isinstance(value, dict):
        return {k: to_plain(v) for k, v in value.items()}
    return value

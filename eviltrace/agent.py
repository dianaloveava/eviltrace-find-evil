from __future__ import annotations

import json
import uuid
from dataclasses import asdict
from pathlib import Path

from .evidence import inventory_case, load_events
from .models import AgentRun, AgentStep, Correction, Finding, ToolResult, to_plain, utc_now
from .tools import ReadOnlyToolbox

RUN_DIR = Path("data") / "runs"


class InvestigationAgent:
    def __init__(self, case_id: str = "case_alpha", max_steps: int = 12) -> None:
        self.case_id = case_id
        self.max_steps = max_steps
        self.evidence = inventory_case(case_id)
        self.events = load_events(case_id, self.evidence)
        self.tools = ReadOnlyToolbox(self.events)
        self.steps: list[AgentStep] = []
        self.tool_results: dict[str, ToolResult] = {}

    def run(self) -> AgentRun:
        started = utc_now()
        self._step("plan", "Create investigation plan", "Prioritize authentication anomalies, execution, persistence, and exfiltration with read-only tools.")
        self._record(self.tools.event_count(), "baseline", "Establish case size and event distribution.")
        self._record(self.tools.suspicious_logins(), "auth-check", "Known suspicious IPs can reveal initial access.")
        self._record(self.tools.impossible_travel(), "auth-correlation", "Multi-country success patterns can confirm compromised accounts.")
        self._record(self.tools.suspicious_commands(), "execution-check", "Suspicious process launches can show hands-on-keyboard activity.")
        self._record(self.tools.persistence_changes(), "persistence-check", "Persistence changes determine whether access survived reboot or logout.")
        self._record(self.tools.exfil_signals(), "exfil-check", "Archive/upload/DNS anomalies identify potential data theft.")
        self._step("analysis", "Draft findings", "Convert corroborated tool output into evidence-linked findings.")
        findings = self._draft_findings()
        corrections = self._self_correct(findings)
        self._step("report", "Finalize report", "Emit only evidence-linked confirmed or caveated findings.")
        run = AgentRun(
            id=f"run-{uuid.uuid4().hex[:10]}",
            case_id=self.case_id,
            status="completed",
            started_at=started,
            completed_at=utc_now(),
            steps=self.steps,
            findings=findings,
            corrections=corrections,
            evidence=self.evidence,
            metrics={
                "total_steps": len(self.steps),
                "total_findings": len(findings),
                "total_corrections": len(corrections),
                "confirmed_findings": sum(1 for finding in findings if finding.confidence == "confirmed"),
                "evidence_refs": sum(len(finding.evidence_refs) for finding in findings),
                "paid_api_required": False,
            },
        )
        save_run(run)
        return run

    def _step(self, phase: str, action: str, rationale: str, tool: str | None = None, result: ToolResult | None = None) -> None:
        if len(self.steps) >= self.max_steps:
            raise RuntimeError("agent step budget exhausted")
        self.steps.append(
            AgentStep(
                index=len(self.steps) + 1,
                phase=phase,
                action=action,
                rationale=rationale,
                tool=tool,
                result_summary=result.summary if result else None,
                evidence_refs=result.evidence_refs if result else [],
            )
        )

    def _record(self, result: ToolResult, phase: str, rationale: str) -> None:
        self.tool_results[result.tool] = result
        self._step(phase, f"Run {result.tool}", rationale, tool=result.tool, result=result)

    def _draft_findings(self) -> list[Finding]:
        suspicious_login = self.tool_results["suspicious_logins"]
        travel = self.tool_results["impossible_travel"]
        commands = self.tool_results["suspicious_commands"]
        persistence = self.tool_results["persistence_changes"]
        exfil = self.tool_results["exfil_signals"]
        return [
            Finding(
                id="finding-initial-access",
                title="Compromised account likely used for initial access",
                severity="high",
                confidence="confirmed",
                summary="Suspicious IP login activity and impossible-travel correlation both point to the same user account.",
                evidence_refs=sorted(set(suspicious_login.evidence_refs + travel.evidence_refs)),
                reasoning=[
                    suspicious_login.summary,
                    travel.summary,
                    "Two independent auth checks corroborate the account compromise hypothesis.",
                ],
            ),
            Finding(
                id="finding-execution-persistence",
                title="Post-compromise execution and persistence were established",
                severity="critical",
                confidence="confirmed",
                summary="Suspicious shell activity is followed by cron/service persistence indicators on the same host.",
                evidence_refs=sorted(set(commands.evidence_refs + persistence.evidence_refs)),
                reasoning=[commands.summary, persistence.summary, "Execution and persistence events occur after suspicious authentication."],
            ),
            Finding(
                id="finding-exfiltration",
                title="Possible data exfiltration requires caveated reporting",
                severity="medium",
                confidence="high",
                summary="Archive and upload signals exist, but the agent initially overstates this as confirmed theft before correction.",
                evidence_refs=sorted(set(exfil.evidence_refs)),
                reasoning=[exfil.summary, "Data movement signals are suspicious but do not prove attacker-controlled receipt."],
                caveats=["No packet capture or destination ownership proof is present in the fixture."],
            ),
        ]

    def _self_correct(self, findings: list[Finding]) -> list[Correction]:
        corrections: list[Correction] = []
        exfil = next((finding for finding in findings if finding.id == "finding-exfiltration"), None)
        if exfil and exfil.confidence == "high":
            before = exfil.confidence
            # The re-check asks whether exfil evidence proves receipt by attacker infra. It does not.
            self._step(
                "self-correction",
                "Re-check exfiltration confidence",
                "The exfiltration claim has fewer independent evidence types than initial-access and persistence findings, so downgrade confidence and add caveat.",
                tool="exfil_signals",
                result=self.tool_results["exfil_signals"],
            )
            exfil.confidence = "medium"
            exfil.caveats.append("Downgraded after self-check: archive/upload signals need corroborating destination evidence.")
            corrections.append(
                Correction(
                    finding_id=exfil.id,
                    before_confidence=before,
                    after_confidence=exfil.confidence,
                    reason="Evidence supports suspicious staging/upload behavior, but not confirmed attacker receipt.",
                    evidence_refs=exfil.evidence_refs,
                )
            )
        return corrections


def save_run(run: AgentRun) -> Path:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    path = RUN_DIR / f"{run.id}.json"
    path.write_text(json.dumps(to_plain(run), indent=2), encoding="utf-8")
    (RUN_DIR / "latest.json").write_text(json.dumps(to_plain(run), indent=2), encoding="utf-8")
    return path


def load_run(run_id: str = "latest") -> dict:
    path = RUN_DIR / ("latest.json" if run_id == "latest" else f"{run_id}.json")
    if not path.exists():
        raise FileNotFoundError(f"run not found: {run_id}")
    return json.loads(path.read_text(encoding="utf-8"))


def render_markdown_report(run: AgentRun | dict) -> str:
    data = to_plain(run)
    lines = [
        f"# EvilTrace Incident Report: {data['id']}",
        "",
        f"- Case: {data['case_id']}",
        f"- Status: {data['status']}",
        f"- Started: {data['started_at']}",
        f"- Completed: {data['completed_at']}",
        f"- Paid API required: {data['metrics'].get('paid_api_required', False)}",
        "",
        "## Findings",
    ]
    for finding in data["findings"]:
        lines.extend([
            "",
            f"### {finding['title']}",
            f"- ID: {finding['id']}",
            f"- Severity: {finding['severity']}",
            f"- Confidence: {finding['confidence']}",
            f"- Summary: {finding['summary']}",
            "- Evidence: " + ", ".join(finding["evidence_refs"]),
            "- Reasoning:",
        ])
        for reason in finding["reasoning"]:
            lines.append(f"  - {reason}")
        if finding.get("caveats"):
            lines.append("- Caveats:")
            for caveat in finding["caveats"]:
                lines.append(f"  - {caveat}")
    lines.extend(["", "## Corrections"])
    for correction in data["corrections"]:
        lines.extend([
            "",
            f"- Finding: {correction['finding_id']}",
            f"  - Before: {correction['before_confidence']}",
            f"  - After: {correction['after_confidence']}",
            f"  - Reason: {correction['reason']}",
        ])
    lines.extend(["", "## Evidence Integrity", "All default demo artifacts are synthetic fixtures. Tool adapters are read-only in the default path.", ""])
    return "\n".join(lines)

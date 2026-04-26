# FIND EVIL! Requirement Checklist

Status legend: Complete / Local-ready / User-owned / Remaining finalization

| Requirement | Status | Evidence |
| --- | --- | --- |
| Public code repository + MIT/Apache license | Complete after push | `LICENSE`, full code tree, public repository: https://github.com/dianaloveava/eviltrace-find-evil. |
| Demo video max 5 minutes | Local-ready script; user-owned recording/upload remains | `docs/demo-script.md`; screenshot at `docs/screenshots/eviltrace-dashboard.png`. |
| Architecture diagram | Complete | `docs/architecture.svg`, `docs/architecture.md`. |
| Written project description | Complete | `docs/devpost-story.md`, `submission/devpost-form.md`. |
| Dataset documentation | Complete for included demo data; official starter data downloaded/checksummed locally | `docs/dataset-documentation.md`, `docs/official-starter-data-manifest.json`. |
| Accuracy report | Complete for included demo data; final can add official data run | `docs/accuracy-report.md`, `docs/sample-report.md`, `docs/sift-demo-report.md`. |
| Try-it-out instructions on SIFT Workstation | Complete locally; SIFT VM full official-case validation recommended | `docs/sift-workstation-runbook.md`, `README.md`, `start-eviltrace.sh`. |
| Agent execution logs with timestamps/token usage | Complete | `docs/sample-agent-execution-log.json`; token usage is zero for deterministic no-LLM path. |
| Improve Protocol SIFT / autonomous IR agent | Local-ready MVP | SIFT/DFIR importers, MCP-style read-only tool server, bounded self-correcting agent. |
| User handles Devpost/legal/final submit | User-owned | `docs/submission-checklist.md`. |

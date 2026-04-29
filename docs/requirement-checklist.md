# FIND EVIL! Requirement Checklist

Status legend: Complete / Prototype-ready / User-owned / Blocked / Remaining finalization

| Requirement | Status | Evidence |
| --- | --- | --- |
| Public code repository + MIT/Apache license | Complete after push | `LICENSE`, full code tree, public repository: https://github.com/dianaloveava/eviltrace-find-evil. |
| Demo video max 5 minutes | Blocked / user-owned | Must record official live terminal execution against official real case data and show self-correction. Prototype script exists at `docs/demo-script.md`. |
| Architecture diagram | Prototype-ready; strict update needed after official run | `docs/architecture.svg`, `docs/architecture.md`. |
| Written project description | Prototype-ready; strict update needed after official run | `docs/devpost-story.md`, `submission/devpost-form.md`. |
| Dataset documentation | Partial | Included demo data is documented; strict final requires official starter-resource analysis artifacts. Manifest exists at `docs/official-starter-data-manifest.json`. |
| Accuracy report | Partial | Current report covers prototype data only; strict final requires official case false positives / misses / hallucination / spoliation discussion. |
| Try-it-out instructions on SIFT Workstation | Partial | `docs/sift-workstation-runbook.md`; strict final requires actual SIFT Workstation / Protocol SIFT validation. |
| Agent execution logs with timestamps/token usage | Partial | Prototype log exists; strict final requires logs from official real case run and any LLM token usage if enabled. |
| Improve Protocol SIFT / autonomous IR agent | In progress | SIFT/DFIR importers, MCP stdio read-only server, bounded self-correcting agent. Strict final requires Protocol SIFT / official starter-resource run evidence. |
| User handles Devpost/legal/final submit | User-owned | `docs/submission-checklist.md`. |

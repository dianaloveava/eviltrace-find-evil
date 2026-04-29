# EvilTrace

EvilTrace is a free, local-first, full-stack incident-response agent workbench built for the Devpost **FIND EVIL!** challenge. It demonstrates an autonomous but bounded defender workflow: ingest safe evidence, run read-only checks, create evidence-linked findings, self-correct weak claims, and export a judge-friendly report.

## Why this exists

The submission strategy is prize-oriented but honest: EvilTrace optimizes for a polished, inspectable demo without private data or agent-controlled Devpost/account/legal actions. Optional paid LLM endpoints may be configured by the entrant, but secrets are never committed and the deterministic path remains available for reproducible local checks.

## Features

- Synthetic safe incident-response fixture included in `data/fixtures/case_alpha`.
- Deterministic read-only tools for auth anomalies, command execution, persistence, and exfiltration signals.
- Bounded agent loop with step budget and explicit self-correction.
- Static web dashboard for findings, timeline, evidence, and corrections.
- Markdown/JSON report export.
- No required paid API keys or external services for the deterministic local path; optional LLM endpoints must be user-provided.

## Quick start

```bash
python scripts/run_demo.py
python -m eviltrace.server
```

Then open <http://127.0.0.1:8765> and click **Run demo investigation**.

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Default safety boundaries

- Demo data is synthetic and safe to publish.
- Evidence processing is read-only in the default path.
- No paid API is required for the deterministic local path; optional LLM APIs must be configured by the entrant and documented in logs.
- Do not upload real private, regulated, or sensitive evidence to a public deployment.
- The user must personally handle Devpost registration, legal eligibility, final submission, payout, and tax information.

## Submission package

- PRD: `docs/prd-eviltrace-find-evil.md`
- Test spec: `docs/test-spec-eviltrace-find-evil.md`
- Devpost story draft: `docs/devpost-story.md`
- Demo script: `docs/demo-script.md`
- Architecture: `docs/architecture.md`

## Hackathon target

Primary target: FIND EVIL! on Devpost. Re-check all contest rules before final submission.

## FIND EVIL! requirement tracking

- Requirement checklist: `docs/requirement-checklist.md`
- Dataset documentation: `docs/dataset-documentation.md`
- Accuracy report: `docs/accuracy-report.md`
- Sample execution log: `docs/sample-agent-execution-log.json`
- SIFT Workstation runbook: `docs/sift-workstation-runbook.md`

Current status: EvilTrace is a working prototype with public repository target `https://github.com/dianaloveava/eviltrace-find-evil`. Strict final Devpost submission still needs the user-owned Devpost/Slack/eligibility actions, a SIFT Workstation / Protocol SIFT run against official starter resources, official real-case report/log artifacts, and a recorded demo video. The previously downloaded 11.23GB starter zip is documented by checksum but was deleted locally to free disk space.

## SIFT/DFIR import path

Normalize SIFT-style exports and run the same bounded agent:

```bash
python -m eviltrace.cli import-sift --source data/sift_exports/demo --case sift_demo
python -m eviltrace.cli run --case sift_demo --report docs/sift-demo-report.md
```

Inspect the standard MCP stdio JSON-RPC read-only tool boundary:

```bash
printf '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05"}}\n{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}\n{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"suspicious_commands","arguments":{"case_id":"sift_demo"}}}\n' | python -m eviltrace.mcp_server
```

The legacy CLI wrapper remains available for quick local checks:

```bash
python -m eviltrace.tool_server --manifest
python -m eviltrace.tool_server --case sift_demo --call suspicious_commands
```

## Strict official compliance status

Strict FIND EVIL / Protocol SIFT completion is tracked in `docs/official-strict-compliance.md`. Current repository code is not claimed to be a final official submission until the user-owned Devpost/Slack/SIFT terms steps, official starter-resource analysis run, and demo video are complete.

## Prototype local assets

- Devpost form draft: `submission/devpost-form.md`
- Final review checklist: `submission/final-review.md`
- Architecture SVG: `docs/architecture.svg`
- Dashboard screenshot: `docs/screenshots/eviltrace-dashboard.png`
- SIFT runbook: `docs/sift-workstation-runbook.md`

Current local status: code, launchers, checks, public-repo metadata, official-data checksum manifest, MCP stdio server, and prototype documentation are available. Repository URL: https://github.com/dianaloveava/eviltrace-find-evil. Strict official completion remains blocked on the checklist in `docs/official-strict-compliance.md`.


## Public repository

https://github.com/dianaloveava/eviltrace-find-evil

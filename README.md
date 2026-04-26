# EvilTrace

EvilTrace is a free, local-first, full-stack incident-response agent workbench built for the Devpost **FIND EVIL!** challenge. It demonstrates an autonomous but bounded defender workflow: ingest safe evidence, run read-only checks, create evidence-linked findings, self-correct weak claims, and export a judge-friendly report.

## Why this exists

The submission strategy is prize-oriented but honest: EvilTrace optimizes for a polished, inspectable demo without requiring paid APIs, private data, or agent-controlled Devpost/account/legal actions.

## Features

- Synthetic safe incident-response fixture included in `data/fixtures/case_alpha`.
- Deterministic read-only tools for auth anomalies, command execution, persistence, and exfiltration signals.
- Bounded agent loop with step budget and explicit self-correction.
- Static web dashboard for findings, timeline, evidence, and corrections.
- Markdown/JSON report export.
- No required paid API keys or external services.

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
- No paid API is required.
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

Current status: EvilTrace is a working MVP with public repository target `https://github.com/dianaloveava/eviltrace-find-evil`. Final Devpost submission still needs the user-owned Devpost registration/eligibility actions and a recorded demo video; official FIND EVIL! starter data has been downloaded locally and documented by checksum, while the 11.23GB raw zip remains gitignored.

## SIFT/DFIR import path

Normalize SIFT-style exports and run the same bounded agent:

```bash
python -m eviltrace.cli import-sift --source data/sift_exports/demo --case sift_demo
python -m eviltrace.cli run --case sift_demo --report docs/sift-demo-report.md
```

Inspect the typed read-only tool boundary:

```bash
python -m eviltrace.tool_server --manifest
python -m eviltrace.tool_server --case sift_demo --call suspicious_commands
```

## Submission-ready local assets

- Devpost form draft: `submission/devpost-form.md`
- Final review checklist: `submission/final-review.md`
- Architecture SVG: `docs/architecture.svg`
- Dashboard screenshot: `docs/screenshots/eviltrace-dashboard.png`
- SIFT runbook: `docs/sift-workstation-runbook.md`

Current local status: code, launchers, checks, public-repo metadata, official-data checksum manifest, and required local documentation are ready for a Devpost submission package. Repository URL: https://github.com/dianaloveava/eviltrace-find-evil. User-owned steps remain: record/upload demo video, verify eligibility, join the hackathon, and click final submit.


## Public repository

https://github.com/dianaloveava/eviltrace-find-evil

# Devpost Form Draft

## Project title

EvilTrace

## Tagline

A self-correcting incident-response agent workbench with typed read-only SIFT/DFIR tools and evidence-linked findings.

## Built with

Python 3.12, HTML, CSS, JavaScript, SANS SIFT-compatible export workflows, Plaso/log2timeline-style timelines, Volatility-style process exports, Sleuth Kit bodyfile imports, custom MCP stdio JSON-RPC typed tool server.

## Try it out

Local:

```bash
python -m eviltrace.server
```

Open:

```text
http://127.0.0.1:8765/
```

Windows one-click:

```text
start-eviltrace.bat
```

SIFT/Linux:

```bash
./start-eviltrace.sh
```

## Repository URL

https://github.com/dianaloveava/eviltrace-find-evil

## Demo video URL

TODO: paste video URL after recording/upload.

## What it does

EvilTrace turns SIFT/DFIR exports into a bounded autonomous investigation. It inventories evidence, runs typed read-only tools, generates evidence-linked findings, detects weak claims, performs a self-correction pass, and exports a Markdown/JSON report. The dashboard lets judges trace every finding back to specific tool execution and evidence line references.

## How it addresses FIND EVIL!

- Autonomous execution: fixed investigation phases with explicit rationale and tool calls.
- IR accuracy: confirmed findings are distinguished from caveated inferences.
- Breadth/depth: supports auth, process, persistence, filesystem, and network/exfil signals through import adapters.
- Constraints: architectural guardrails expose typed read-only functions instead of generic shell access.
- Audit trail: structured logs include timestamps, tool calls, evidence refs, and token usage fields. Optional LLM use must be configured with a user-provided API URL/key and recorded in the final logs.
- Usability: one-click Windows launcher, Linux/SIFT runbook, documentation, screenshots, and sample reports.

## Submission links checklist

- GitHub: https://github.com/dianaloveava/eviltrace-find-evil
- Demo video: TODO
- Architecture diagram: `docs/architecture.svg`
- Dataset docs: `docs/dataset-documentation.md`
- Accuracy report: `docs/accuracy-report.md`
- Execution logs: `docs/sample-agent-execution-log.json`

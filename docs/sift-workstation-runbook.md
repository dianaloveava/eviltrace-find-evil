# SIFT Workstation / Protocol SIFT Strict Runbook

The FIND EVIL! resources page recommends SANS SIFT Workstation and Protocol SIFT. EvilTrace is designed to run in a Linux terminal on SIFT with Python 3.12+.

This runbook is strict: synthetic data, unofficial public data, and SIFT-like exports are useful for local tests, but they are not substitutes for the official SIFT / Protocol SIFT / starter-resource path in the final FIND EVIL submission.

## 1. Prepare SIFT

Download SIFT Workstation:

```text
https://sans.org/tools/sift-workstation
```

Install Protocol SIFT as instructed by the challenge resources:

```bash
curl -fsSL https://raw.githubusercontent.com/teamdfir/protocol-sift/main/install.sh | bash
```

If the SIFT Workstation download, Slack, Devpost, or SANS flow requires login, terms acceptance, or eligibility confirmation, stop and let the entrant complete that official action personally.

## 2. Run EvilTrace locally

```bash
chmod +x start-eviltrace.sh
./start-eviltrace.sh
```

Open:

```text
http://127.0.0.1:8765/
```

## 3. Import SIFT/DFIR exports

EvilTrace accepts exported evidence from SIFT tools instead of requiring destructive direct access:

```bash
python -m eviltrace.cli import-sift --source data/sift_exports/demo --case sift_demo
python -m eviltrace.cli run --case sift_demo --report docs/sift-demo-report.md
```

Supported dependency-free import shapes:

- Plaso/log2timeline CSV or JSONL exports.
- Volatility JSON/text outputs.
- Sleuth Kit bodyfile text.
- Generic JSON/JSONL event exports.

## 4. MCP read-only typed tool boundary

Inspect the MCP stdio JSON-RPC tool boundary:

```bash
printf '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05"}}\n{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}\n' | python -m eviltrace.mcp_server
```

Inspect the legacy CLI manifest:

```bash
python -m eviltrace.tool_server --manifest
python -m eviltrace.tool_server --case sift_demo --call suspicious_commands
```

The agent receives only typed read-only functions; it does not receive a generic shell execution surface in the EvilTrace MCP boundary.

## Final submission caveat

For strict FIND EVIL completion, run this on official starter resources through SIFT Workstation / Protocol SIFT and include the resulting report/logs. The repository includes a small synthetic SIFT-export bundle only for quick local workflow checks; it must not be represented as the final real-case demo evidence.

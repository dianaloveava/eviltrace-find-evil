# SIFT Workstation Runbook

The FIND EVIL! resources page recommends SANS SIFT Workstation and Protocol SIFT. EvilTrace is designed to run in a Linux terminal on SIFT with Python 3.12+.

## 1. Prepare SIFT

Download SIFT Workstation:

```text
https://sans.org/tools/sift-workstation
```

Install Protocol SIFT as instructed by the challenge resources:

```bash
curl -fsSL https://raw.githubusercontent.com/teamdfir/protocol-sift/main/install.sh | bash
```

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

## 4. Read-only typed tool boundary

Inspect the MCP-style typed tool manifest:

```bash
python -m eviltrace.tool_server --manifest
python -m eviltrace.tool_server --case sift_demo --call suspicious_commands
```

The agent receives only typed read-only functions; it does not receive a generic shell execution surface.

## Final submission caveat

For the strongest FIND EVIL! submission, run this on the official starter case data from the challenge resources and include the resulting report/logs. The repository includes a small synthetic SIFT-export bundle so judges can try the workflow quickly without downloading large images.

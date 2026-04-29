# FIND EVIL Strict Official Compliance Tracker

This document is the project source of truth for strict FIND EVIL / Protocol SIFT compliance. It intentionally does **not** mark an item complete unless it has been completed through the official path or is a user-owned official action.

## Official sources to verify before final submit

- FIND EVIL overview / submission requirements: <https://findevil.devpost.com/>
- FIND EVIL rules: <https://findevil.devpost.com/rules>
- FIND EVIL resources: <https://findevil.devpost.com/resources>
- SANS SIFT Workstation: <https://www.sans.org/tools/sift-workstation/>
- Protocol SIFT install script: <https://raw.githubusercontent.com/teamdfir/protocol-sift/main/install.sh>
- Model Context Protocol specification: <https://modelcontextprotocol.io/specification/>

## Non-negotiable interpretation

- Do not use unofficial public DFIR data as a substitute for official starter resources.
- Do not use synthetic fixtures as a substitute for real case data in the final demo video.
- Do not call the legacy CLI tool boundary a full MCP server.
- Do not call SIFT-compatible export parsing a verified Protocol SIFT integration.
- Do not claim final submission readiness until the demo video and all official user-owned actions are complete.
- Do not commit raw large evidence, API keys, Slack/Devpost session data, or cloud credentials.

## User-owned official blockers

These actions involve account identity, legal attestations, terms acceptance, or final submission control. Browser automation may navigate to the page and assist, but the user must personally decide and complete the action.

| Official action | Status | Blocking reason |
| --- | --- | --- |
| Register/log in to Devpost | User-owned | Account identity and Devpost terms. |
| Join the FIND EVIL hackathon on Devpost | User-owned | Eligibility and rule acceptance. |
| Join Protocol SIFT Slack | User-owned | Slack/account terms and identity. |
| Download SIFT Workstation if gated by SANS terms/login | User-owned if gated | Terms/license acceptance. |
| Confirm legal eligibility | User-owned | Legal representation by entrant. |
| Configure any paid/custom LLM endpoint and API key | User-owned | Secrets, billing, and data disclosure boundary. |
| Record/upload final demo video | User-owned with agent-provided script | Voice/account/upload ownership. |
| Click final Devpost Submit | User-owned | Final legal submission action. |
| Prize/tax/payout steps | User-owned | Legal and financial identity. |

## Agent-owned technical work

These are safe for the coding agent to implement, validate, document, commit, and push.

| Technical item | Status | Evidence |
| --- | --- | --- |
| Public GitHub repository | Complete | <https://github.com/dianaloveava/eviltrace-find-evil> |
| MIT license | Complete | `LICENSE` |
| Legacy read-only tool boundary | Complete as legacy CLI | `eviltrace/tool_server.py` |
| MCP-compliant stdio JSON-RPC wrapper | In progress | `eviltrace/mcp_server.py` |
| Protocol SIFT/SIFT strict runbook | Needs strict update | `docs/sift-workstation-runbook.md` |
| Official starter resource manifest | Partial; zip deleted locally | `docs/official-starter-data-manifest.json` |
| Official starter data analysis run | Blocked | Requires official resource download and SIFT/Protocol SIFT run. |
| Demo video | Blocked | Requires official case run and user recording/upload. |

## Paid LLM API policy

Paid LLM APIs are allowed only as a configurable, user-provided option:

- `EVILTRACE_LLM_API_URL`
- `EVILTRACE_LLM_API_KEY`
- `EVILTRACE_LLM_MODEL`

Rules:

- Never commit keys or secrets.
- Never hard-code a private endpoint.
- Log token usage when an LLM is used.
- Document whether evidence content leaves the local machine.
- If no key is provided, do not pretend an LLM-backed run occurred.

## Current strict status

EvilTrace is **not yet a fully official FIND EVIL submission**. The codebase is a useful starting point, but strict completion requires a verified SIFT Workstation / Protocol SIFT run on official starter case data, a demo video showing that run, and user-owned Devpost/Slack/legal/submission actions.

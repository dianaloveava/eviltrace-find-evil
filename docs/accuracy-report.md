# Accuracy and Self-Correction Report

## Evaluation cases

1. `case_alpha`: synthetic default JSONL fixture.
2. `sift_demo`: normalized SIFT/DFIR export demo built from Plaso-style CSV, Volatility-style JSON, and Sleuth Kit bodyfile-style text.

## Expected vs observed findings

### Initial access

- Expected: compromised account / suspicious authentication.
- Observed: confirmed.
- Evidence: suspicious IP authentication plus same-user multi-country login pattern.

### Execution and persistence

- Expected: post-compromise execution and persistence.
- Observed: confirmed.
- Evidence: encoded PowerShell/payload commands plus cron/service persistence artifacts.

### Exfiltration

- Expected: suspicious staging/upload behavior, not fully confirmed theft.
- Initial tendency: high confidence.
- Corrected result: medium confidence.
- Reason: archive/upload/DNS signals exist, but no independent proof of attacker-controlled receipt is present.

## Hallucination and false-positive controls

- Findings must include evidence references.
- The self-correction pass downgrades claims when evidence types are insufficient.
- The default deterministic path has zero LLM token usage, reducing narrative hallucination risk.
- Optional future LLM summaries must not override deterministic evidence classifications.

## Evidence integrity approach

Architectural guardrail: the agent calls only typed read-only tools from the MCP stdio JSON-RPC server in `eviltrace.mcp_server`, the legacy CLI wrapper in `eviltrace.tool_server`, and `ReadOnlyToolbox`. No destructive shell command or write-to-evidence function is exposed through that boundary.

Prompt guardrail: documentation instructs read-only analysis, but the key protection is architectural: the callable tool surface cannot mutate original evidence.

Spoliation test status:

- Included tests verify evidence hashing and read-only tool behavior at the application level.
- Manual review confirms import writes only derived normalized fixtures, not source exports.
- Full SIFT VM spoliation testing against official images is still a final-submission task.

## Limitations

- Official FIND EVIL! starter case data has not been vendored or fully benchmarked in this repository.
- The SIFT demo bundle is intentionally small and synthetic.
- The current MCP server implements the standard stdio JSON-RPC method surface used by MCP clients for `initialize`, `tools/list`, and `tools/call`; strict final validation should still include the client used in the official demo environment.
